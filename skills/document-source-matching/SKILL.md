---
name: document-source-matching
description: Locate and assess Markdown extracts for an original local document by recorded source path and SHA-256. Use when choosing an extracted Markdown aid or deciding whether the original must be checked again.
metadata:
  short-description: Match Markdown extracts to original sources
  version: "v0.4.7"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Document Source Matching

Use `local_documents.locate_markdown_extracts` to retrieve bounded candidates by source path or SHA-256 within the identified source/workspace scope. If MCP is unavailable and `my-py-tools` is already available, use `python -m documents.locate_markdown_extracts`; otherwise use available local path/metadata inspection and report matching limits. Do not install or reconfigure tools during ordinary lookup

- Treat `current` as metadata and hash agreement, `stale` as the same recorded path with different content, and `candidate` as a weaker filename-only or incomplete metadata match. Hash agreement does not prove extraction completeness, correct OCR/tables or semantic accuracy
- Preserve each candidate's path, recorded source, hash, extraction time and match reasons; do not choose by filename alone when a hash is available
- Original PDF, Office file or other source remains authoritative. Start from relevant extract sections; reopen only needed original sections for visual evidence, missing/unclear content, stale or conflicting versions, or an explicit original-source check. Validation rules do not by themselves require routine original rereading when the extract is usable; label extract-only evidence separately from inspected originals
- Lookup is read-only. Do not regenerate, overwrite, synchronize or delete a Markdown file without separate authorization
