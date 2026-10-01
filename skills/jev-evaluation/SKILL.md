---
name: jev-evaluation
description: Rank retrieved context candidates or evaluate bounded semantic choices with TypeSafe Jev when a shortlist needs comparison. Use for Jev setup or diagnosis too, not as a preflight for ordinary coding.
metadata:
  short-description: Optional candidate ranking and typed semantic evaluation
  version: "v0.4.5"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Jev Evaluation

Prefer the installed `jev` MCP server for bounded evaluation on Windows, macOS or Linux. It exposes only `jev_rank`, `jev_evaluate` and `jev_status`; verify actual availability and schema before calling. Keep usage decisions here and API execution in the shared Python client. Python 3.10+ is required; MCP uses the pinned official SDK, while the CLI needs only the standard library.

## Choose useful work

- Retrieve locally first. Use Jev for a shortlist needing semantic relevance ranking or an atomic finite choice/ordered rubric; complete small or already-settled work directly.
- Main retains requirements, architecture, delegation, implementation and acceptance. Jev signals do not establish API compatibility, permissions, persistence, correctness or test coverage.
- Keep mandatory instructions, governing specifications, acceptance criteria, confirmed decisions and unresolved blockers in Main's context. Ranking changes reading order, not source authority or required verification.
- Supply only approved, necessary excerpts or sanitized summaries. Setup authorization and installing this Skill do not authorize uploading company source, private specifications, logs or customer data. A decision needing unapproved proprietary context stays with Main.

## Run without expanding context

- For first installation, credentials, Mac/Windows commands or API diagnosis, read [usage.md](references/usage.md). Otherwise use the helper without reading its implementation or repeating setup.
- For relevance, call `jev_rank` with `query` and `candidates` containing opaque `id` and approved `text`; mark mandatory entries `required: true`. Required entries need no text and are never sent to Jev; every candidate ID remains in the result.
- Keep source path/line or document-page pointers locally by candidate ID. Send bounded excerpts, not repository dumps, conversation history or full instructions; batch independent questions when useful and open the relevant originals after ranking.
- For a finite choice, boolean probability or ordered rubric, call `jev_evaluate`; read only its schema section in the usage reference when needed. Do not generate code, explanations or history summaries with Jev.
- If MCP is unavailable, use `scripts/jev.py rank --input <file>` or `evaluate` from this installed Skill when permitted; otherwise return to Main. Do not install dependencies, reconfigure the client or repeat credential setup during ordinary coding.
- Consume the compact result: candidate IDs/probabilities or typed answers, resolved model, usage, latency and status. Do not echo inputs, raw HTTP errors or credentials into the chat.
- Noul probability is not confidence. Choice/Score include provider confidence; calibrate any action threshold against representative domain and language examples. Sorting is advisory and never automatically discards low-ranked or uncertain sources.
- `status: fallback`, malformed results, missing credentials or uncertain judgments return to the existing Main workflow. Keep unknowns explicit; do not interpret failed evaluation as low risk or automatically create tasks, reviewers or retries with another model.

## Maintain one source

Edit the version-controlled Skill, validate changed behavior, then synchronize only its managed installed copy. Keep credentials outside repositories and Skill archives. Installation readback does not prove an already-open client refreshed its Skill list; no performance or context savings are established without measurement.
