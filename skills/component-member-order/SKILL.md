---
name: component-member-order
description: Organize Angular component class members by responsibility and feature flow while preserving decorators, comments, initialization behavior, and public interfaces. Use when reordering or standardizing members in one or more .component.ts files, optionally migrating decorator inputs and outputs to signal APIs when explicitly requested, or when generating a scoped handoff prompt for that work.
metadata:
  short-description: Safe Angular component member ordering
  version: "v0.4.2"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Component Member Order

Organize only the requested Angular component classes. Do not treat this as permission to move files, rename symbols, change component metadata, rewrite logic, or format unrelated code.

## Choose the mode

- Apply mode: inspect and edit the requested `.component.ts` files when the user asks for the organization to be performed
- Prompt mode: when the user asks for a reusable handoff prompt, run `scripts/generate_component_member_order_prompt.py` against the requested target and return the generated prompt without editing the components
- Signal I/O mode: only when explicitly requested, also migrate eligible decorator-based inputs and outputs to Angular signal APIs; read [references/signal-io-migration.md](references/signal-io-migration.md) before editing or generating the prompt

In either mode, discover applicable project instructions and inspect the current Git status and relevant diff before acting. Preserve concurrent changes and narrow the file set to the requested feature, application, or directory.

## Order class members

Use this top-level order when the corresponding members exist:

1. `static readonly` constants
2. Component inputs, using `input()` or `input.required()` in Signal I/O mode and otherwise preserving the existing declaration style
3. Component outputs, using `output()` in Signal I/O mode and otherwise preserving the existing declaration style
4. `@ViewChild`, `@ViewChildren`, `@ContentChild`, and `@ContentChildren`
5. Template-facing `public readonly` constants and options
6. Public view state and forms
7. Public getters and setters
8. Injected `private readonly` dependencies
9. Private internal state
10. Constructor
11. Angular lifecycle hooks
12. Template event handlers
13. Other public operations
14. Private loading, synchronization, validation, construction, and transformation helpers

Keep paired getters/setters and overloads adjacent. Order lifecycle hooks by Angular execution order: `ngOnChanges`, `ngOnInit`, `ngDoCheck`, `ngAfterContentInit`, `ngAfterContentChecked`, `ngAfterViewInit`, `ngAfterViewChecked`, then `ngOnDestroy`.

## Group methods by feature flow

Do not sort methods alphabetically.

- First group them by actual screen section or end-to-end feature flow, using template order or the primary user flow when that is evident
- Within each feature group, prefer event handler, operation entry, data loading, state synchronization, validation, then construction or transformation
- A private helper used by only one feature may remain directly after that feature's public methods
- Put shared private helpers used by multiple flows near the end of the class
- Prefer feature cohesion over a rigid public/private split, but never change member visibility
- Create only groups supported by the component's real behavior; do not invent placeholder sections or methods

Examples of possible feature groups include query, create case, detail, note, timeline, export, and approval. These are examples, not required headings.

## Preserve behavior and comments

Class field initializers execute in declaration order. Trace initializer references before moving fields and preserve any required dependency order. If the preferred order would change runtime behavior, keep the safe order and report the exception.

- Move a member together with its decorators, existing JSDoc, and directly associated comments
- Do not rewrite, remove, merge, or reposition existing JSDoc and comments relative to their member
- Do not change names, types, access modifiers, initial values, parameters, return types, or method bodies
- Do not add pass-through helpers or unrelated refactors
- Preserve public interfaces, template bindings, Angular lifecycle behavior, and reactive state ownership

## Format groups

- Keep consecutive members in the same group together without blank lines between them
- Use one blank line between different groups
- Add a concise JSDoc group heading before each non-empty group, such as `/** Component inputs */`, `/** View state and forms */`, or `/** Query flow */`
- Follow the project's established comment language and terminology; if none is evident, follow the user's language
- Describe only the group's responsibility
- If the first member already has JSDoc, place the new group heading before the existing JSDoc without changing the existing text

## Verify and report

Review the final diff for behavior changes, initializer-order risks, misplaced decorators, and comment loss. Run the project's smallest sufficient type check or compile check for the affected scope plus its normal diff-whitespace check when available. Do not install or upgrade dependencies merely to run validation.

Report changed files, any ordering exceptions, checks actually run, and checks that remain blocked or unverified. Never report an unrun check as passed.
