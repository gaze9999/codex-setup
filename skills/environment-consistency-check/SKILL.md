---
name: environment-consistency-check
description: Compare local Skills, runtime mirrors, or environment trees without synchronizing them. Use for versioned file drift, missing or extra files, and hash-based consistency checks.
metadata:
  short-description: "Compare Skills and environment mirrors without writes"
  version: "v0.4.6"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Environment Consistency Check

Use `workspace_inspection.compare_environment` for bounded read-only comparison. If MCP is unavailable and `my-py-tools` is already available, use `python -m maintenance.environment_consistency`

- Compare by relative path, size and SHA-256. Report missing, extra and changed files separately; do not reduce all differences to one pass/fail label
- Default exclusions intentionally omit VCS internals, caches, `.env`, credentials and key material. Expand scope only when the user names the required files and their contents may be read safely
- A difference does not authorize synchronization. Inspect ownership, source direction, version and backup expectations before proposing or performing a write
- Repository source and installed mirrors have different roles. State which side was treated as source, and do not assume the newer timestamp is authoritative
