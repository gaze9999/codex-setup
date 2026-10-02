# Doc Update Rules

Use these rules only when updating documentation or memos after concrete implementation changes.

This reference is not for general Notion organization, ordinary document writing, standalone summaries, pre-implementation spec summarization, Markdown / Notion synchronization unrelated to code changes, or polished document artifact production.

## Hard activation gate

Before using the post-implementation updater, all conditions must be true:

1. The user requested an update, sync, refresh, reconciliation, or alignment of existing documentation, memo, changelog, API reference, Notion page, Markdown file, or Codex context brief.
2. The update is grounded in implementation-change evidence available in the current task: diff, commit, PR, release, migration, changed files, completed refactor, or pasted code-change summary.
3. At least one target surface is identifiable: a repo docs path, README, changelog, Markdown file, Notion page/database item, API reference, or Codex context brief.

If any condition is missing, do not proceed as a post-implementation update. Ask for the missing evidence or target, or route to the appropriate document, Notion, context-brief, or coding-prompt workflow.

Do not activate this workflow solely because the request mentions `Notion`, `docs`, `Markdown`, `memo`, `API`, `Codex`, `release`, or `sync`.

## Evidence-first policy

Documentation updates must be grounded in observable implementation evidence:

- diff hunks
- changed file paths
- commit / PR descriptions
- existing docs that name the affected feature, API, workflow, or configuration
- release notes or migration notes supplied by the user
- user-provided code-change summaries when no direct diff is available

Evidence confidence:

| Evidence | Confidence | Rule |
|---|---|---|
| Diff hunks + changed files | Highest | Supports implementation-change claims; runtime, deployment and acceptance claims still need their own evidence. |
| PR / commit + changed-file list | High | Use commit text carefully; inspect relevant files when available. |
| Release or migration note tied to code changes | Medium | Mark unsupported details as unresolved. |
| User-provided implementation summary only | Lower | Label updates as summary-based and avoid claiming direct verification. |

Do not invent behavior, file paths, flags, APIs, versions, or user-facing guarantees. Preserve governing specifications and confirmed decisions when code conflicts with them; record the conflict instead of silently replacing requirements with implementation behavior. Tie verification claims to their checked source state and retain pending acceptance.

## Routing boundaries

Use the stricter route when the request overlaps with other workflows:

| User intent | Correct workflow |
|---|---|
| Read a spec / API doc and make a reusable Codex brief before coding | Context Brief |
| Make a polished PDF / DOCX / Markdown artifact | Document Production |
| Organize, move, rename, classify, or restructure Notion pages/databases | Notion workflow, not this Skill |
| Convert a coding requirement into a single task prompt | Coding Prompt |
| Update existing docs or memos from a concrete diff / PR / commit / release / migration | Doc Updater |

## Impact classification

Use `yes`, `maybe`, or `no` for documentation impact.

### `yes`

Use `yes` when the change affects documented contracts or user-observable behavior:

- public API, endpoint, SDK, CLI, event, schema, or integration contract
- environment variable, config key, setup command, build command, deploy step, or migration path
- user-facing UI behavior, validation, permissions, copy, state, error, or workflow
- breaking change, compatibility change, limitation, deprecation, or operational risk

### `maybe`

Use `maybe` when the file path or diff suggests a possible doc impact but the behavior is not clear:

- internal module restructuring that may affect architecture docs
- UI refactor touching labels or state names
- dependency upgrade with possible setup or compatibility impact
- generated type changes without visible source context

### `no`

Use `no` when the change is unlikely to require docs:

- tests only
- formatting only
- lint-only changes
- internal variable rename with no public contract impact
- generated artifacts with no semantic change
- local tooling changes not exposed to users or maintainers

## Documentation target selection

Choose the smallest documentation surface that keeps knowledge aligned.

| Change type | Likely target |
|---|---|
| user-facing feature | README, docs, memo, Notion page only if requested |
| public API change | API reference, Codex context brief, changelog |
| config / env change | setup docs, deployment docs, README |
| breaking change | changelog, migration guide, release note |
| internal architecture change | architecture doc, Codex context brief, memo |
| bug fix with user-visible effect | changelog or memo when relevant |

Create a new documentation surface only when the user requests one or no existing target can represent the necessary update. Prefer patching the smallest existing section.

## Local-first documentation and Notion

Update local documentation by default. Notion discovery, access, comparison, validation, writes, and status reporting require the current request to explicitly mention Notion or name a Notion target. General sync wording, a local file containing a Notion link or page ID, an uploaded snapshot, a paired target, a prior sync arrangement, or bidirectional metadata does not satisfy this gate.

- Do not copy local filesystem paths or relative Markdown links into Notion. Replace them with a Notion page mention or link only when that exact Notion target has been confirmed; otherwise retain the label as plain text and omit the local path.

Complete authorized local updates independently. Preserve relationship metadata only when it lies inside an edited local target, but do not infer remote state or change sync timestamps.

When the user explicitly requests Notion synchronization, that request authorizes the identified targets; do not request duplicate confirmation:

1. Resolve the exact targets and canonical source from the request and current task; ask only when ambiguity would change scope or overwrite risk. Use Notion as canonical only when the user specifies it.
2. Read current content and compare relevant sections before writing. Follow `notion-sync-reader-writer-contract.md`.
3. Resolve independent changes without blindly overwriting either side.
4. Make the smallest authorized update and preserve unrelated content, page IDs, links, and metadata.
5. Verify each updated target and distinguish local completion from remote synchronization.

## Current-state and historical records

When a target set separates current status from history or archives, preserve that division:

- Keep the current document focused on current behavior, active work, unresolved decisions, and the latest verification boundary.
- Put completed or superseded work, dated execution details, detailed check results, version hashes, sync events, and obsolete links in the history target.
- Before removing content from the current document, confirm that unique evidence is already present in history or move it there. Avoid duplicating the same full record in both places.
- If the user specifies an identifier format, apply it consistently to current records and record an old-to-new mapping in history. Rewrite historical identifiers and anchors only on explicit user request.
- Keep each new history entry to one or two concise paragraphs when possible. Combine the outcome, material evidence, and remaining verification limits; link to detailed evidence instead of copying command sequences or check-by-check narration. Use a longer entry only when necessary to retain unique information or when the user explicitly requests detail.

## Safe update style

- Use concise language.
- Preserve exact public names: endpoint paths, fields, enums, config keys, commands, file paths, and error names.
- Separate confirmed behavior from assumptions.
- Mark unresolved items with `Open question`.
- Mark unsupported or conflicting evidence with `Conflict`.
- Avoid documenting speculative future behavior.
- Avoid leaking secrets, tokens, credentials, or unnecessary personal data.

## Validation expectations

Before finalizing, confirm:

- the hard activation gate is satisfied
- every meaningful doc change traces back to implementation evidence
- evidence confidence is stated when the evidence is indirect or summary-based
- every affected target is listed in the update plan or final summary
- important no-update decisions are recorded
- breaking changes and migrations are clearly marked
- any Notion access or dual-target update had explicit user authorization
- Notion and Markdown targets are semantically aligned when both are updated
- unverified items are explicitly labeled
