---
name: validation-evidence-review
description: Review existing local validation evidence without rerunning commands. Use for run result summaries, baseline checks, partial coverage, and deciding what still needs verification.
metadata:
  short-description: Review existing validation evidence and gaps
  version: "v0.4.7"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Validation Evidence Review

Use `workspace_inspection.validation_evidence` for bounded read-only indexing. If MCP is unavailable and `my-py-tools` is already available, use `python -m validation.validation_evidence_index`; do not infer that missing evidence passed

- Separate recorded commands and results from checks that were not run, skipped, malformed or based on another source baseline
- A valid index proves only that evidence was parsed. Decide whether it covers the current diff, affected dependencies and acceptance criteria before treating it as sufficient
- Do not rerun build, test, lint, browser or remote checks unless the user request authorizes that work
- Preserve source, baseline, log references and malformed-run errors when summarizing; never turn partial evidence into a repository-wide pass claim
