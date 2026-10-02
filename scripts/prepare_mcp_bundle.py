#!/usr/bin/env python3
"""Assemble an unpublished local bootstrap bundle from verified built wheels."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys

from bootstrap_mcp import ROOT, digest, wheel_info


def prepare(wheel_dirs, output):
    preset = json.loads((ROOT/"mcp_servers/presets/baseline.json").read_text())
    required = {name: version for server in preset["servers"] if server["kind"] == "python" for name, version in server["packages"].items()}
    found = {}
    for directory in wheel_dirs:
        for path in directory.glob("*.whl"):
            info = wheel_info(path)
            if required.get(info["name"]) == info["version"]:
                if info["name"] in found and found[info["name"]][1]["sha256"] != info["sha256"]:
                    raise ValueError("Ambiguous wheel content: " + info["name"])
                found[info["name"]] = (path, info)
    missing = set(required)-set(found)
    if missing:
        raise ValueError("Missing exact built wheels: " + ", ".join(sorted(missing)))
    if output.exists():
        raise ValueError("Output exists; select a new directory to preserve the previous bundle")
    output.mkdir(parents=True)
    entries = []
    for name, (path, info) in sorted(found.items()):
        shutil.copyfile(path, output/path.name)
        entries.append(info | {"file": path.name})
    manifest = {"version": 1, "status": "local_unpublished_bundle", "preset_sha256": digest(json.dumps(preset, sort_keys=True, separators=(",", ":")).encode()), "wheels": entries}
    (output/"bundle.json").write_text(json.dumps(manifest, indent=2)+"\n")
    # A portable folder keeps the same paths as the checkout; no checkout is needed at runtime
    portable = output/"installer"
    (portable/"scripts").mkdir(parents=True)
    shutil.copyfile(ROOT/"scripts/bootstrap_mcp.py", portable/"scripts/bootstrap_mcp.py")
    (portable/"mcp_servers/presets").mkdir(parents=True)
    shutil.copyfile(ROOT/"mcp_servers/presets/baseline.json", portable/"mcp_servers/presets/baseline.json")
    shutil.copytree(ROOT/"skills/jev-evaluation", portable/"skills/jev-evaluation", ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.egg-info", "build", "dist", ".env*", "*.key", "*.pem"))
    for filename in ("bootstrap-mcp.cmd", "bootstrap-mcp.sh"):
        shutil.copyfile(ROOT/filename, portable/filename)
    return {"status":"prepared", "output":str(output), "packages":required, "published":False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel-dir", action="append", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=ROOT/"dist/mcp/bootstrap")
    args=parser.parse_args(argv)
    try:
        print(json.dumps(prepare(args.wheel_dir,args.output.resolve()),ensure_ascii=True,indent=2))
        return 0
    except (OSError,ValueError) as error:
        print("error: "+str(error),file=sys.stderr);return 1


if __name__=="__main__":raise SystemExit(main())
