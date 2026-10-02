---
name: environment-consistency-check
description: Compare local Skills, runtime mirrors, or environment trees without synchronizing them. Use for versioned file drift, missing or extra files, and hash-based consistency checks.
metadata:
  short-description: "Compare Skills and environment mirrors without writes"
  version: "v0.4.7"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Environment Consistency Check

Resolve two existing absolute, non-nested directory roots and the requested include/exclude scope. Use `workspace_inspection.compare_environment` within its configured read roots; if unavailable and `my-py-tools` is already available, inspect `python -m maintenance.environment_consistency --help` and use its supported comparison options

- Compare by relative path, size and SHA-256. Report missing, extra and changed files separately; do not reduce all differences to one pass/fail label
- Default exclusions intentionally omit VCS internals, caches, `.env`, credentials and key material. Expand scope only when the user names the required files and their contents may be read safely
- A difference does not authorize synchronization. Inspect ownership, source direction, version and backup expectations before proposing or performing a write
- Repository source and installed mirrors have different roles. State which side was treated as source, and do not assume the newer timestamp is authoritative
- State comparison scope and exclusions. A file limit, unreadable path, missing dependency, or changing tree leaves the affected comparison incomplete; do not report full equality or bypass read-root boundaries to finish it
