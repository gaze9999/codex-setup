---
name: document-source-matching
description: Locate and assess Markdown extracts for an original local document by recorded source path and SHA-256. Use when choosing an extracted Markdown aid or deciding whether the original must be checked again.
metadata:
  short-description: Match Markdown extracts to original sources
  version: "v0.4.6"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Document Source Matching

Use `local_documents.locate_markdown_extracts` to retrieve bounded candidates by source path or SHA-256. If MCP is unavailable and `my-py-tools` is already available, use `python -m documents.locate_markdown_extracts`; do not install or reconfigure tools during ordinary lookup

- Treat `current` as metadata and hash agreement, `stale` as the same recorded path with different content, and `candidate` as a weaker filename-only or incomplete metadata match
- Preserve each candidate's path, recorded source, hash, extraction time and match reasons; do not choose by filename alone when a hash is available
- Original PDF, Office file or other source remains authoritative. Use an extract for search and orientation, then reopen the original when layout, missing content, validation rules or conflicting versions matter
- Lookup is read-only. Do not regenerate, overwrite, synchronize or delete a Markdown file without separate authorization
