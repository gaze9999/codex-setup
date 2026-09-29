---
name: task-routing
description: Choose between continuing a Codex task, creating a separate task, forking a conversation, and using subagents, then prepare a compact handoff when needed. Use for explicit routing questions, conditional routing instructions in a user turn, or an authorized continuing coordinator, not ordinary implementation or AGENTS.md maintenance.
metadata:
  short-description: Task routing and context handoff
  version: "v0.4.2"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Task Routing

Keep execution with the smallest owner that can complete and verify the outcome. A task title does not establish a coordinator role or require delegation, and a long conversation does not by itself require a new task.

## Check authority and capabilities

- Identify the current outcome, what the user authorized, whether a continuing coordinator role was assigned, and which decisions remain unresolved.
- Check whether the current environment actually supports creating tasks, forking conversations, using subagents, and choosing a checkout or worktree. This skill does not grant permission to use any of them. Create a separate user-owned task only when the user explicitly authorized that action; follow current user, project, and runtime limits for subagents and forks.
- Distinguish a request to recommend a route from an instruction to carry it out. Invoking this skill or asking which route fits does not itself authorize a new user-owned task. A user instruction in the current turn to create and assign a separate task if it fits stated conditions is explicit conditional authorization, not a mandate to create one; apply the large, multi-turn phase threshold below and execute that route only when the conditions and available tools permit. Apply the same distinction to a requested fork or subagent delegation.
- If the selected route is unavailable or unauthorized, continue the work that remains in scope and describe the required handoff. Do not silently substitute a subagent for a requested user-owned task.
- Produce only a prompt or plan when the user requested that artifact. Otherwise complete authorized work or start the authorized execution route directly.

## Choose the owner

1. Continue in the current task when one outcome remains active, the steps depend on each other, or the task can still use its retained decisions reliably. A continuing coordinator may directly complete small connected work and keep the current decisions, progress, and next-step order.
2. Create a separate task only for a large, independently reviewable phase likely to need multiple turns of execution and follow-up, when the user authorized task creation. A continuing coordinator may keep that role, but must inspect the execution task's result before advancing its plan.
3. For an authorized separate phase, fork a conversation when the execution needs the completed history of the current conversation. Give the fork its own concrete assignment and confirm critical decisions against current sources; inherited history alone does not define its work or restore details lost through compaction. A fork does not clear stale context. When the aim is a clean context, use a fresh task with a compact handoff instead.
4. Use a subagent for a bounded slice inside the current task when independent ownership, parallel speed, or context isolation outweighs coordination and review cost. Keep dependent steps and shared-file edits with one owner. The parent integrates and verifies the returned work.
5. Use a temporary side conversation only when the user requests a separate focused detour and that feature is available.

Do not route work by a fixed number of turns, tokens, compactions, elapsed hours, or phase names. Resolve uncertain architecture or requirements with a capable owner before handing a known execution method to another agent. Do not claim a cost or quality gain without measured evidence.

## Transfer only useful state

- State the objective, confirmed decisions and source pointers, owned files or modules, must-preserve constraints, exclusions, acceptance criteria, unresolved questions, and stop condition. Include attempts and failure evidence when the next owner would otherwise repeat them.
- Name the execution environment: repository, branch, current checkout or new worktree, relevant uncommitted changes, and ignored or untracked instructions or files that must be present. Check the actual starting state; do not assume a new worktree inherits every local file.
- For a separate execution task that may report back, record the coordinator's `threadId` in the handoff when available. A task title is only a display label and may change; if only a title is known, resolve and verify the target `threadId` before sending a cross-task message. Do not guess the destination.
- Send a compact task-specific handoff rather than the entire transcript or routine tool output. Fork only when carrying completed conversation history is useful.
- When a governing specification, `AGENTS.md`, or agent role changes during execution, identify the current source and version or modification time, the superseded decision, affected tasks, whether the change is confirmed or proposed, and which work or checks must be revisited. Notify affected execution tasks through an available channel, or leave the change in the authorized progress record for their next turn. Have them read the current governing files; a fork does not inherit decisions made after it branched. Do not copy the whole document into the handoff.
- The coordinator may finish its turn after dispatch instead of waiting or polling. The execution task should return its source revision or starting state, changed files, actual checks and outcomes, unresolved questions, and next action. If cross-task messaging is available, it may send one completion notice; do not assume that notice resumes the coordinator or is guaranteed background delivery. When the coordinator next runs, read the task's final status and result, then check the relevant diff, verification, and open boundaries before integration. A completion message or finished task alone does not establish acceptance.
- A worktree handoff moves the same conversation and Git state between Local and Worktree. It is not a new task or a context reset. Keep project-specific document updates and model or role choices under their own instructions.
