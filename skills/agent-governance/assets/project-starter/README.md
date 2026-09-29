# Project agent starter

Use these files only when creating or revising governance for a specific project. Start with the project's actual source, configuration, existing instructions and user-provided material. Treat these files as examples, not active instructions or a required layout.

1. Select relevant concerns from [project-types.md](project-types.md). A repository may fit several types.
2. Fill [root/AGENTS.md](root/AGENTS.md) with verified repository-wide facts. Remove every `<placeholder>` and any rule that does not change a decision.
3. Add [nested/AGENTS.md](nested/AGENTS.md) only in directories with distinct runtime, ownership, public interfaces or checks. Rename `nested` to the real directory when copying.
4. Add [root/.codex/agent-guidance/tasks.md](root/.codex/agent-guidance/tasks.md) only if the project needs task routing or handoff rules beyond the global setup. The root file loads it only for relevant work.
5. Prefer available built-in subagents. Copy only useful files from `root/.codex/agents/`, then specialize their names and boundaries. The portable TOML files omit model pins so each slice can choose a supported model and use a maintained subagent fallback; effort is optional. A target project may pin a model for a stable narrow role when current evidence justifies it. Verify the effective configuration; a role pin overrides a spawn choice and a model-only pin retains previously resolved effort in current Codex.
6. Check the target coding agent's current instruction discovery and role configuration before installing. Other agents may ignore Codex TOML or nested `AGENTS.md`.

Keep the always-loaded root and nested files short. Put task-specific procedures in conditional guides or skills, and current goals, decisions, progress and permissions in the current task. Do not copy private paths, organization names, secrets, endpoints, unverified versions or commands into public files. A template does not grant permission to spawn subagents, create tasks, change dependencies or publish work.

Before delivery, validate active instruction order from the repository root and affected subdirectories, parse selected TOML, inspect Git status and ignored files, and confirm that an agent run loads the intended files. Existing sessions may need to restart before new guidance is active.
