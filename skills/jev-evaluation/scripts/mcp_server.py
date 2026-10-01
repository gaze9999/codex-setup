#!/usr/bin/env python3
"""Expose the existing bounded Jev client through the official MCP SDK."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key-file", type=Path, help="Override the local credential file, never pass the key itself.")
    args = parser.parse_args()

from mcp.server import MCPServer
from mcp_types import ToolAnnotations
from pydantic import BaseModel, ConfigDict, StrictBool

import jev


class Candidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    text: str | None = None
    required: StrictBool = False


def build_server(key_file: Path | None = None) -> MCPServer:
    server = MCPServer("Jev", instructions="Optional bounded semantic evaluation. Send approved excerpts only; Main retains mandatory context and acceptance.")
    annotations = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=False, openWorldHint=True)

    def evaluate(data: dict, model: str | None, rank: bool) -> dict:
        try:
            result, _ = jev.evaluate_data(data, model or os.environ.get("TYPESAFE_MODEL", "jev-latest"), rank=rank, key_file=key_file)
            return result
        except jev.Problem as exc:
            return {"status": "fallback", "reason": str(exc)}
        except (OSError, ValueError, RecursionError):
            return {"status": "fallback", "reason": "local_operation_unavailable"}

    @server.tool(annotations=annotations)
    def jev_rank(query: str, candidates: list[Candidate], model: str | None = None) -> dict[str, Any]:
        """Rank approved candidate excerpts; required IDs stay local and every ID is retained. Failure preserves original order."""
        return evaluate({"query": query, "candidates": [candidate.model_dump(exclude_none=True) for candidate in candidates]}, model, True)

    @server.tool(annotations=annotations)
    def jev_evaluate(state: str | dict[str, Any] | list[Any], questions: dict[str, dict[str, Any]], model: str | None = None) -> dict[str, Any]:
        """Evaluate bounded noul, choice or score questions using TypeSafe's typed schema; returns validated signals and usage."""
        return evaluate({"state": state, "questions": questions}, model, False)

    @server.tool(annotations=annotations)
    def jev_status(online: bool = False) -> dict[str, Any]:
        """Check credential availability without revealing it; online additionally queries models and does not submit project data."""
        try:
            return jev.run(SimpleNamespace(command="doctor", key_file=key_file, online=online, timeout=8, retries=1))[0]
        except jev.Problem as exc:
            return {"status": "fallback", "reason": str(exc)}
        except OSError:
            return {"status": "fallback", "reason": "local_operation_unavailable"}

    return server


if __name__ == "__main__":
    build_server(args.key_file).run(transport="stdio")
