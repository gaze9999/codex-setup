---
name: coding-prompt
description: Create a concise cross-project coding-agent prompt and model recommendation only when the user explicitly asks for a prompt or handoff; do not use for direct implementation requests.
metadata:
  short-description: Concise cross-project coding prompt
  version: "v0.4.4"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Coding Prompt

Create a minimal handoff-ready prompt when the requested deliverable is the prompt itself. Do not execute the generated prompt. User instructions override these defaults.

## Activation

- Use only when the user explicitly asks for a coding-agent prompt, delegation prompt, portable handoff, or a model recommendation packaged with that prompt
- For investigation, review, diagnosis, implementation, or fixes, perform the requested work instead of returning a prompt

## Prompt content

- Include only the information needed to perform this task: the objective, task-specific scope, confirmed contracts, essential source pointers, explicit prohibitions, and observable completion criteria
- Prefer positive gates that state what to implement, preserve, verify, or deliver. Use negative wording only for files, modules, behaviors, external systems, or actions that must not be touched
- Mention a document as required reading only when the task actually depends on it. Do not add broad repository, specification, history, or instruction-reading checklists
- Omit routine repository discovery, Git operations, generic coding/style/safety rules, standard verification checklists, and reminders to follow project instructions. The destination agent and project instruction layers provide them
- Keep task-specific exceptions, exact contract values or messages, required compatibility boundaries, known concurrent-work constraints, and explicit stop conditions when they materially affect execution
- Preserve the requested authority boundary. Do not turn a review, diagnosis, or plan into implementation, or add external actions the user did not authorize
- Do not invent paths, APIs, versions, commands, mappings, requirements, or completed results. Keep unresolved decisions explicit and block only dependent work
- Consolidate repetition and omit background or rationale that does not change an implementation decision

## Execution context

- Write for the environment where the prompt will run, not where it is created
- For a known project, identify only the target area and task-specific sources needed to act. Do not copy project governance into the prompt
- For an unknown or non-project destination, provide the minimum context needed to stand alone without assuming access to this chat or local files
- Include ownership, batching, delegation, or handoff mechanics only when the task requires them

## Model recommendation

- Complete the prompt first, then recommend exactly one model and supported reasoning level for the resulting task
- Preserve an explicit user selection. Otherwise base the choice on task uncertainty, interacting logic, risk, context, coordination, and verification burden
- Prefer an efficient supported model for an explicitly bounded task with a known approach. Choose a stronger reasoner when the task still requires deciding the approach, root cause, or architecture; do not use progressively higher reasoning levels to retry the same unresolved problem
- Verify current model availability when a concrete model name is required. If it cannot be verified, give concise selection criteria and mark the concrete choice unresolved
- Keep the recommendation outside the copyable prompt. A recommendation does not switch models or change project routing

## Output

- Use the language requested by the user or target project. Otherwise use concise Traditional Chinese for Chinese context, or concise English for English context
- Return the complete prompt as one uninterrupted Markdown `text` fenced code block so the app can show its code-block copy control on mobile, including for long prompts. Do not split the prompt or wrap it in a writing block, quote, list, or table. Use short sentences or compact bullets, omit empty sections, and add headings only when they improve comprehension
- Put only task instructions inside the block. Keep the model and reasoning recommendation immediately after it
- Do not add commentary around the prompt unless a brief availability or unresolved-contract note is necessary
- Never execute the generated prompt as part of this workflow
