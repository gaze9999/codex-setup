#!/usr/bin/env python3
"""Build and verify the Codex MCP server wheels for a repository release."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile


PRODUCER = "codex-setup.prepare_mcp_release.v1"
MANIFEST = "mcp-release-manifest.json"
PROJECTS = (
    (Path("."), "codex-local-documents-mcp", (Path("pyproject.toml"), Path("mcp_servers/local_documents"))),
    (Path("mcp_servers/workspace_inspection"), "codex-workspace-inspection-mcp", (Path("mcp_servers/workspace_inspection"),)),
)
VERSION = re.compile(r"v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?")
PROJECT_VERSION = re.compile(r'(?m)^version\s*=\s*"([^"]+)"\s*$')


def normalize_tag(value: str) -> str:
    if not VERSION.fullmatch(value):
        raise ValueError(f"Invalid release tag: {value}")
    return value if value.startswith("v") else "v" + value


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def package_versions(repo: Path) -> dict[str, str]:
    versions = {}
    for relative, name, _sources in PROJECTS:
        match = PROJECT_VERSION.search((repo / relative / "pyproject.toml").read_text(encoding="utf-8"))
        if not match:
            raise ValueError(f"Package version not found: {repo / relative / 'pyproject.toml'}")
        versions[name] = match.group(1)
    return versions


def source_hashes(repo: Path) -> dict[str, str]:
    files: set[Path] = set()
    for _relative, _name, sources in PROJECTS:
        for source in sources:
            path = repo / source
            files.update(path.rglob("*")) if path.is_dir() else files.add(path)
    result = {}
    for path in sorted(files, key=lambda item: item.as_posix().casefold()):
        if not path.is_file() or path.is_symlink() or any(part in {"build", "dist", "__pycache__"} or part.endswith(".egg-info") for part in path.parts):
            continue
        result[path.relative_to(repo).as_posix()] = digest(path.read_bytes())
    return result


def wheel_metadata(data: bytes) -> dict[str, str]:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if archive.testzip() is not None:
            raise ValueError("Wheel CRC validation failed")
        names = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        if len(names) != 1:
            raise ValueError("Wheel must contain exactly one METADATA file")
        text = archive.read(names[0]).decode("utf-8")
    metadata = {}
    for field in ("Name", "Version"):
        match = re.search(rf"(?m)^{field}:\s*(.+)$", text)
        if not match:
            raise ValueError(f"Wheel metadata is missing {field}")
        metadata[field.casefold()] = match.group(1).strip()
    return metadata


def build(repo: Path) -> dict[str, bytes]:
    with tempfile.TemporaryDirectory(prefix="codex-mcp-release-") as directory:
        temporary = Path(directory)
        source = temporary / "source"
        wheels = temporary / "wheels"
        shutil.copytree(
            repo,
            source,
            ignore=shutil.ignore_patterns(".git", "dist", "build", "__pycache__", "*.egg-info", "*.pyc", ".env", ".env.*"),
        )
        wheels.mkdir()
        for relative, _name, _sources in PROJECTS:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "wheel", "--no-deps", "--no-build-isolation", "--wheel-dir", str(wheels), str(source / relative)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=180,
                check=False,
            )
            if result.returncode:
                raise ValueError(f"MCP wheel build failed for {relative}: {(result.stderr or result.stdout).strip()}")
        built = {path.name: path.read_bytes() for path in sorted(wheels.glob("*.whl"))}
    seen = {metadata["name"]: metadata["version"] for metadata in map(wheel_metadata, built.values())}
    expected = package_versions(repo)
    if seen != expected:
        raise ValueError(f"Built MCP wheels do not match package projects: {seen!r} != {expected!r}")
    return built


def prepare(repo: Path, tag: str, output_root: Path, dry_run: bool = False) -> dict[str, object]:
    repo = repo.resolve()
    tag = normalize_tag(tag)
    wheels = build(repo)
    manifest = {
        "producer": PRODUCER,
        "tag": tag,
        "packages": package_versions(repo),
        "sources": source_hashes(repo),
        "assets": [{"name": name, "size": len(data), "sha256": digest(data)} for name, data in sorted(wheels.items())],
    }
    output = output_root.resolve() / tag
    result = {"tag": tag, "output": str(output), "assets": len(wheels), "dry_run": dry_run}
    if dry_run:
        return result
    if output.exists():
        check_output(output, tag)
        shutil.rmtree(output)
    output.mkdir(parents=True)
    for name, data in wheels.items():
        (output / name).write_bytes(data)
    (output / MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def check_output(output: Path, tag: str) -> None:
    if output.is_symlink() or not output.is_dir():
        raise ValueError(f"MCP release output must be a regular directory: {output}")
    manifest = json.loads((output / MANIFEST).read_text(encoding="utf-8"))
    if manifest.get("producer") != PRODUCER or manifest.get("tag") != tag:
        raise ValueError("MCP release output belongs to another producer or tag")
    assets = manifest.get("assets")
    if not isinstance(assets, list) or {path.name for path in output.iterdir()} != {MANIFEST} | {item.get("name") for item in assets if isinstance(item, dict)}:
        raise ValueError("MCP release output contains missing or unmanaged files")
    for item in assets:
        path = output / item["name"]
        data = path.read_bytes()
        if len(data) != item.get("size") or digest(data) != item.get("sha256"):
            raise ValueError(f"MCP release asset changed independently: {path.name}")


def verify(repo: Path, tag: str, output_root: Path) -> list[Path]:
    tag = normalize_tag(tag)
    output = output_root.resolve() / tag
    manifest = json.loads((output / MANIFEST).read_text(encoding="utf-8"))
    if manifest.get("producer") != PRODUCER or manifest.get("tag") != tag:
        raise ValueError("MCP release manifest has the wrong producer or tag")
    if manifest.get("packages") != package_versions(repo) or manifest.get("sources") != source_hashes(repo):
        raise ValueError("MCP release manifest does not match current source")
    assets = manifest.get("assets")
    if not isinstance(assets, list) or {path.name for path in output.iterdir()} != {MANIFEST} | {item.get("name") for item in assets if isinstance(item, dict)}:
        raise ValueError("MCP release folder contains missing or unexpected files")
    paths = []
    seen = {}
    for item in assets:
        path = output / item["name"]
        data = path.read_bytes()
        if len(data) != item.get("size") or digest(data) != item.get("sha256"):
            raise ValueError(f"MCP release asset changed: {path.name}")
        metadata = wheel_metadata(data)
        seen[metadata["name"]] = metadata["version"]
        paths.append(path)
    if seen != manifest["packages"]:
        raise ValueError("MCP wheel metadata does not match the manifest")
    return sorted(paths)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag")
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        result = prepare(args.repo, args.tag, args.output_dir or args.repo / "dist" / "mcp", args.dry_run)
    except (OSError, ValueError, json.JSONDecodeError, zipfile.BadZipFile) as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1
    print(f"{'PREVIEW' if args.dry_run else 'READY'} {result['tag']}; MCP wheels={result['assets']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
