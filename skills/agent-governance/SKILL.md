---
name: agent-governance
description: Create, audit, or simplify project AGENTS.md layers and Codex subagent roles. Use for agent-governance work, including a new project setup, not ordinary implementation or general code review.
metadata:
  short-description: Agent governance, role boundaries, and instruction minimization
  version: "v0.4.5"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Agent Governance

Keep the smallest instruction set that preserves authorization, contracts, project knowledge, and completion criteria. Prefer removing, merging, or relocating rules over adding them.

## Scope and evidence

- Treat an audit or recommendation as read-only. Edit only when requested, normally within `AGENTS.md`, role configuration, and directly related governance documents; do not expand into application code or external actions.
- When edits are requested, complete and verify them. Deliver only a prompt, plan, review, report, or handoff when the user explicitly requests that artifact.
- Read applicable instruction layers, role files, live references, Git status, and relevant diffs before editing. Preserve concurrent work and inspect ignored governance files directly.
- Consult current official OpenAI documentation when changing discovery, configuration, model, reasoning, or subagent behavior. Label human reports as anecdotal and project observations as local evidence.

## Start a new project setup

- Read user-provided files or uploads and inspect the target repository before choosing an instruction structure. Do not require this repository or a fixed source path to be available.
- For an authorized new setup, read [project-starter/README.md](assets/project-starter/README.md) and select only relevant templates for the confirmed project type and tool support. Fill verified facts, remove placeholders, and keep the always-loaded root and nested files brief.
- Start with built-in agents; add custom roles only for a durable difference in ownership, permissions, tools, or expected output. Keep Model and reasoning choices unset until the target environment supports and needs a specific override.
- Put task routing detail in a conditional guide when needed. Do not turn templates into standing instructions for every turn or treat a template as authorization to create tasks or delegate.

## Put each rule at the narrowest durable layer

| Layer | Keep here |
|---|---|
| Global or user | Stable cross-project preferences, safety boundaries, execution and evidence principles |
| Repository root | Cross-module architecture and contracts, shared safety, generic ownership, common verification |
| Nested repository | Directory-specific runtime, commands, conventions, public interfaces, and focused checks |
| Role | Only behavior or restrictions that differ for that role |
| Task guide or Skill reference | Procedures needed only for a specific task type |
| Current task | Goal, authorization, progress, exceptions, concurrency, blockers, stop condition |

- Judge where guidance will execute, not where it is authored. Do not copy project rules into portable guidance merely because the file is being edited outside that project.
- Treat paths, installed tools, versions, model availability, and environment reachability as facts to resolve at runtime unless they are verified project contracts.
- Linked references should have clear loading triggers. Do not require unconditional reading of entire documentation folders.

## Simplify without losing decisions

- Keep a rule only when it changes a meaningful decision, belongs at that layer, and is not reliably recoverable from source, configuration, or tooling.
- Merge inherited duplicates and repeated workflow prose while preserving exact contractual wording, authorization gates, public-interface boundaries, and project-specific completion criteria.
- Remove old-model scaffolding, fixed output quotas, repeated status rituals, blanket rereads, unconditional checklists, and failure-specific workarounds that no longer change a decision.
- Prefer repository tooling, tests, linters, or CI for mechanically enforceable behavior. Do not add dependencies merely to reorganize instructions.
- Before retiring a guide or role, map all live references and unique rules. Move surviving content first, then verify dead links and callers; historical mentions may remain when they are not live instructions.
- Preserve explicit user choices and safety boundaries. Never claim that a shorter file improves quality, cost, or runtime behavior without measured evidence.

## Preserve maintainability decisions

- Keep explicit equivalent-syntax, return-type, explicit-public and responsibility-based member-order preferences at the user/global layer; do not replace them with a generic Clean Code style. Preserve equivalent behavior, clear reading and applicable tooling support
- When recording extraction or inlining rules, judge the full helper call chain, meaningful abstraction boundaries and navigation cost. Avoid pass-through layers, but do not inline into hard-to-read or overly long callers; do not invent fixed function-length or layer-count limits
- Place type/file cohesion and single-state-owner principles at their durable layer. Keep framework-specific Component/Service placement in applicable project guidance, and record concrete refactor candidates as task work items rather than implementation authorization

## Load detailed guidance only when needed

- When creating, splitting, or relocating global, root, nested, or tool-specific agent instructions, read [instruction-layering.md](references/instruction-layering.md).
- When changing delegation, worker ownership, subagent context, or model/reasoning routing, read [delegation-routing.md](references/delegation-routing.md).
- When changing role context, compaction, task switching, handoffs, memory, or Context Brief policy, read [context-continuity.md](references/context-continuity.md).

## Verify and deliver

- Review the final instruction hierarchy for contradictions, unreachable references, duplicated authority, ambiguous ownership, and rules placed above their valid scope.
- Start with readback and relevant syntax, metadata, reference, and mirror checks for changed governance files and their affected callers. Expand only for concrete unresolved risk, insufficient or failing focused checks, or applicable required gates. Use application builds or E2E only when governance changes affect application behavior; avoid unrelated suites and new test infrastructure for text-only changes.
- If synchronized copies were requested, compare paths and content after the copy. Syntax checks do not prove that a client reloaded the new guidance.
- Report changed files, rules retained or moved, rules removed, actual checks, unresolved assumptions, and any runtime behavior not verified.
