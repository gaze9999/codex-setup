# Task routing and handoff

Read only when deciding whether to create or fork a task, delegate to a subagent, or hand work to another owner.

- Continue here for small, connected or unresolved work. A long conversation alone does not require a new task.
- Create a user-owned task only with explicit authorization for a large, independently reviewable phase likely to need multiple turns. A conditional user instruction authorizes creation only when its conditions are met.
- Fork only when that authorized task needs completed conversation history. A fresh task with a short handoff usually needs less inherited context. A worktree handoff moves the same task; it does not create one.
- Use a subagent only when permitted for a bounded independent slice with clear ownership and acceptance. Keep each coupled feature and its related checks with one owner; parallel writes also require settled shared interfaces and isolated mutable runtime resources. Use the fewest agents that improve quality, elapsed time or context isolation.
- Handoff: goal, confirmed decisions and sources, owned files, exclusions, checkout or worktree state, relevant uncommitted or ignored files, acceptance, open questions and stop condition; include failed attempts when needed for a decision, and tailor context to explorer, worker, reviewer or consultant needs. Use `threadId` for cross-task messages when available; titles may change.
- When specifications or guidance change, notify affected owners with the changed decision and work to revisit. A fork does not receive later decisions automatically.
- The coordinator may end its turn after dispatch. On return, read the execution result, inspect the diff and actual checks against the checked revision or relevant diff state, then update progress. A completion notice alone is not acceptance.
