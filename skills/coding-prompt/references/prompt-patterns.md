# Coding prompt patterns

Read this reference when creating reusable prompt templates or choosing an unfamiliar handoff shape. These are compact shapes, not required headings or repository rules. Replace bracketed fields with confirmed task content and omit irrelevant lines before delivery; keep the complete finished prompt in one `text` fenced block as specified by `SKILL.md`.

## Implementation with a confirmed approach

```text
Complete [observable outcome] in [owned feature/module].
Use [relevant source path/section] for [specific fields or behavior]; preserve [confirmed interface or compatibility boundary].
Follow [confirmed approach] and retain [known concurrent edits or behavior].
Verify [task-specific acceptance] with [existing relevant check, if known]; report actual results, pending criteria and affected files.
[Unresolved decision] blocks only [dependent behavior]; continue independent authorized work.
```

## Read-only investigation or review

```text
Investigate/review [specific trigger or question] in [bounded source/revision]. Keep the work read-only.
Compare [expected behavior from identified requirement] with the actual call/state/data flow.
Return concrete findings with file/symbol, trigger, impact and evidence, or no findings. Separate confirmed defects from unresolved questions.
Identify the smallest next action and any verification gap; do not infer approval to implement repairs.
```

## Continuing work with another owner

```text
Continue [authorized outcome] from [current source/revision and relevant uncommitted state].
Own [coupled scope]; [other owner] retains [neighboring scope or shared decision].
Confirmed decisions: [only decisions that change execution, with current source pointers].
Accepted work: [effective artifacts and checked state]. Pending work: [unfinished criteria, returned/pending acceptance, blockers and updates not yet adopted].
Preserve [independent edits and must-retain evidence]. Reconcile [prior ownership or changed baseline] before dependent writes.
Complete [remaining acceptance and focused checks], then report checked source state, criterion status, actual results and unresolved items.
```

A handoff transfers useful state; it does not authorize a new chat, cross-chat messages, external actions or broader ownership. Include failed approaches only when the next owner would otherwise repeat them. Keep Main's acceptance responsibility and distinguish source inspection from runtime or deployment verification.
