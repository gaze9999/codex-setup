---
name: task-guide
description: Create or refresh feature-specific coding task guides from a project's actual instructions, identified sources and confirmed decisions. Use for reusable task rules, stable work-item IDs and concise history snapshots with source authority and verification boundaries; not agent role assignment, ordinary summaries or implementation work.
metadata:
  short-description: Create portable feature-specific coding task guides
  version: "v0.4.5"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Task Guide

Create a concise, conditionally loaded guide for a feature, transaction or workflow. Its job is to tell a future coding agent which evidence to read, which boundaries apply and what delivery requires; it is not a copy of the specification, a progress log or an agent roster.

## Evidence and scope

- Inspect the target project's applicable instructions, Git status/diff when available, relevant configuration, current owners and identified source documents. Determine the real stack and naming rather than copying an example project's rules.
- Resolve the requested feature and destination from the task. Ask only when a missing source, ownership or decision prevents a correct guide; keep independent coverage usable and unresolved behavior explicit.
- Distinguish original specifications, explicit user decisions, navigation/extraction aids and current implementation evidence. Assign source authority by topic; do not invent one overall latest-source order or promote a missing field, example or existing behavior into a requirement.
- Preserve actual authorization and module/interface boundaries. Creating a guide does not authorize application changes, source regeneration, delegation, publication or external data transfer.

## Create or refresh

- For installation, first use or concrete examples, read [README.md](README.md); its guide, corrected-ID and commit/no-commit snapshot examples are bundled with this Skill and explicitly fictional.
- Read [task-guide.md](references/task-guide.md) for the format and generator input. Use its sections only where the target project needs them; omit unsupported procedures rather than importing another project's conventions.
- Keep the entrypoint small: scope, task-to-evidence navigation, source authority, non-obvious implementation constraints, focused verification and applicable document triggers. Link to the maintained source for detailed fields, changing decisions, current status and history.
- Write generated guides and snapshots in concise Traditional Chinese, preserving technical names and exact source identifiers. Use Chinese headings and labels; do not copy a source's verbosity into the guide.
- Order sections by their headings' importance to the task. Put authorization, decisive source rules and active blockers early; present the main tables next and detailed bullet explanations later. Use `section_order` for that priority rather than moving every table ahead of every paragraph; essential context stays before its table.
- Prefer project-relative paths or named reference/document roots resolved from the active task/workspace. Do not embed drive letters, usernames, assumed tools, fixed model names or a sample project's identifiers.
- For a new guide, assemble the confirmed content into a local JSON input and run Skill-relative `scripts/create_task_guide.py <input.json> --output <guide.md>`. Python 3.10+ and the standard library suffice; no API or MCP is required. The generator validates structure and formats supplied content; it cannot establish source truth.
- Honor an explicit destination; otherwise use `.codex/agent-guidance/<feature>.md` in the target project, following its established layout when different. If making the guide discoverable is within the requested governance scope, add one task-specific loading pointer to the applicable `AGENTS.md`; do not make every feature guide an unconditional prerequisite.
- Refresh an existing guide by editing only affected sections after reading its current contents and callers. The create-only generator refuses to overwrite files; preserve unique decisions and concurrent work instead of regenerating over them.
- When Python is unavailable, write the same evidence-grounded format directly and report the generator as not run. Structured-source extraction may use available document tools; it is not a requirement to install dependencies.

## Work-item IDs

- Inspect the maintained current records, relevant history and live references before creating IDs. These identify tracked work items, not customer/database/API identities or generated application UUIDs.
- Reuse the project's existing grouping and ID syntax. When none exists, choose meaningful groups from the actual feature and record the scheme; do not prescribe a sample project's prefixes. Keep each existing ID stable through title, priority, status, owner or display-order changes.
- For numeric groups, reserve all existing and retired IDs and allocate after each group's greatest recorded serial; do not fill historical gaps or reuse completed/deleted IDs. Reuse the same ID for the same work item; keep relationships, scope, source pointers and acceptance evidence in its maintained record.
- In current work tables, retain corrected items and their original IDs, displaying a fully corrected ID as `~~ID~~`. This is presentation only; references and logical IDs remain unchanged. Keep remaining work for partial completion, and never replace or recycle a corrected ID for another item.
- Record old-to-new relationships when an authorized split, merge or renumbering needs new IDs. Preserve historical identifiers and anchors unless rewriting them is explicitly requested.
- Use the generator's `--allocate-ids` mode for a declared prefix/serial scheme; its output is a proposal based only on supplied reservations. Recheck and register IDs in the authorized record before using them, with one registration owner when work is concurrent. The helper does not update that record or guarantee uniqueness against unseen changes.
- Keep the guide's ID scheme, group table, registry pointer and stable rules; keep item status in the maintained registry. For other established ID formats, retain them and use their current allocation process rather than forcing numeric IDs.

## History snapshots

- When a snapshot is requested or the project's established document trigger applies, append a bounded record to its maintained history target; creating this guide alone does not authorize application history or status changes. Keep current records and history separate.
- Use concise Chinese for the title, concrete change/decision, actual verification boundary and material remaining work. Resolve the current time in the user's/task's timezone, to the minute as `yyyy-mm-dd hh:mm`; do not infer it from a host with an unknown timezone.
- Include an actually confirmed source commit as its unique short SHA; the agent verifies it from source evidence or read-only Git inspection. Without a confirmed commit, omit the Git line and record the content directly; do not invent a SHA or imply HEAD includes uncommitted changes. For a confirmed committed base plus uncommitted changes, mark both explicitly.
- A committed snapshot must also describe that commit's actual relevant changes, based on its diff; a SHA or vague commit title does not replace the change summary. Distinguish any additional uncommitted changes and their checks from the committed portion.
- Use Skill-relative `scripts/record_history.py <entry.json> --output <history.md>` after reading the target; its schema and preview mode are in [task-guide.md](references/task-guide.md). The helper appends without rewriting old bytes and rejects an identical timestamp/title; one owner coordinates concurrent history writes. It validates format, not source truth or commit coverage.

## Verify and deliver

- Check source locations and cited sections, retained decisions, unresolved gates, applicable boundaries and any conditional loading pointer against the actual target project. Structural generation alone does not prove semantic correctness or runtime loading.
- Review the final diff or direct readback for ignored files. Do not advance application progress, claim application tests passed or add history entries solely because a task guide was created.
- Deliver the guide location, source coverage, actual checks and material unresolved items. When this Skill itself is updated, keep repository source and any requested installed mirror consistent.
