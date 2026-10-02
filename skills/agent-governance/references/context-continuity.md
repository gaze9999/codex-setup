# Context continuity

Use this reference only when governance work changes role context, compaction, task switching, handoffs, memory or Context Brief behavior.

- Do not impose fixed message, compaction, token or elapsed-time thresholds for another task. Continue while one outcome remains active and retained state is reliable; a model change alone does not require a new task.
- Recommend a separate task for a distinct deliverable or when stale accumulated context causes repeated contradictions or lost constraints. Create it only with explicit authorization for a large, independently reviewable phase likely to need multiple turns. Fork only when that authorized task needs prior history; a fresh task and compact handoff serve clean-context needs.
- Use a Context Brief only for reusable implementation requirements from identified specifications, APIs, schemas, integration guides or acceptance criteria. Keep transcripts and routine progress out of it.

## Match context to the recipient

| Recipient | Provide | Expected return |
|---|---|---|
| Explorer | One concrete question, source scope, relevant constraints and known findings | Answer, exact files/symbols, confirmed evidence and unknowns |
| Worker | Goal, confirmed requirements and decisions, source pointers, owned files, exclusions, worktree/concurrency state, acceptance and stop condition | Changed behavior/files, checked revision or diff state, actual results and open boundaries |
| Reviewer | Original requirements, acceptance, applicable rules, actual diff/revision, related code and necessary environment evidence | Concrete defects or questions with triggers, impact and evidence; no findings is valid |
| Consultant | Decision to resolve, constraints, supported facts and relevant failed attempts; fuller history when it is necessary | Options and reasoning grounded in evidence, with unresolved assumptions |
| Continuing task owner | Current goal/authorization, decisions/sources, repository/branch/HEAD, relevant uncommitted/ignored files, active ownership, completed work, checks, failures and next action | Resumed execution based on verified current state |

- Choose fresh context, selected history or fuller history according to the recipient's actual need and supported tools. Do not universally require full inheritance or an extremely short summary. Keep routine logs out; preserve failure evidence when it prevents repeated investigation.
- A review needs the original acceptance basis and current code, without a leading narrative asserting that the implementation is correct. Advice on failed approaches may need more history than a review.
- Reuse verification only within its source revision, relevant diff and environment limits. Recheck changed facts and affected behavior; a prior agent's passing checks do not cover later edits.
- A fork does not receive later decisions automatically. Communicate changed governing sources and affected work through an authorized channel or progress record; do not assume task names or completion notices establish acceptance.

## Preserve work across owners

- Keep one current record in the existing authorized progress destination or task context, with owner/ID, scope, dependencies, acceptance, result evidence, outstanding decisions and next action. Do not create duplicate handoff documents or store transcripts as requirements.
- Before handoff or compaction, reconcile every active item as running, blocked, returned/pending acceptance or accepted. Include unresolved user corrections and who must receive them; short context must not omit constraints, source conflicts, failure evidence or incomplete checks.
- Notifications are hints, not durable acceptance or guaranteed wakeups. Use supported event/wait mechanisms; on resumption, read outstanding owners and reconcile their actual artifacts before starting dependent work. A background continuation needs an explicit supported mechanism, otherwise state that user follow-up is needed.
- Only the assigned writer edits a coupled slice. Confirm the prior writer stopped or completed before replacement; use version/hash evidence to detect concurrent changes. Required work remains pending when a thread is interrupted, archived or inaccessible.
