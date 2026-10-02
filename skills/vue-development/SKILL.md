---
name: vue-development
description: Implement, refactor, diagnose, or review Vue, Nuxt, or Vite-based applications while preserving the detected framework versions, component contracts, state, routing, SSR or hydration, styling, and build behavior.
metadata:
  version: "v0.4.6"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Vue Development

Work from the repository's actual Vue ecosystem and conventions. Do not assume Vue 3, Nuxt, Vite, Pinia, Composition API, TypeScript, SSR, or a particular package manager until verified.

## Discover the application

- Inspect manifests and lockfiles, Vue/Nuxt/Vite configuration, TypeScript settings, routing, state management, test targets, lint/format settings, build/deploy configuration, and nearby components.
- Resolve framework and compiler versions, SFC syntax, Options or Composition API usage, `<script setup>`, reactivity transform assumptions, auto-imports, server/client boundaries, UI library, and styling strategy.
- Identify public component contracts: props, emits, `v-model`, slots, exposed members, provide/inject keys, route params, store shape, API models, and CSS variables.
- Reuse existing composables, components, stores, tokens, validation, loading, error, and data-fetching patterns before creating feature-local alternatives.

## Implement the smallest complete change

- Keep props and emitted events typed where the stack supports it. Preserve event names, `v-model` arguments, slot contracts, defaults, and attribute fallthrough unless the task changes that API.
- Preserve Vue reactivity semantics. Check the installed compiler before changing destructuring: Vue 3.5+ reactive `defineProps` destructure differs from ordinary `reactive()` state and earlier Vue versions. Preserve ref identity, lifecycle ownership, and reactive sources passed to watchers or composables.
- When changing async effects, prevent stale results and preserve cleanup and watcher flush timing. Watchers created in async callbacks need explicit ownership/cleanup; use APIs supported by the installed Vue version.
- Keep local state local. Use a composable or store only when ownership, reuse, lifecycle, and persistence justify it; do not move state globally for convenience.
- For Nuxt or SSR, separate server-only and client-only APIs, avoid request state leaking across users, and preserve hydration-compatible initial output. Guard browser globals and side effects.
- Preserve router guards, lazy-loading, error boundaries, loading states, empty states, forms, keyboard/focus behavior, and existing accessibility.
- Prefer scoped or project-standard styling and existing design tokens. Avoid broad global selectors, accidental deep styling, or a new UI pattern for one component.
- Migrate API style, state library, router, bundler, or UI library only when explicitly requested.

## Verify

- Select the repository's smallest sufficient existing check for the changed behavior: type/template compilation, a focused component test, lint, or build as applicable. Expand only for an affected integration or unresolved risk; use actual project scripts or workspace targets.
- Add or update focused tests for changed component contracts, reactivity, routing, store behavior, SSR/hydration, or user interaction when the task warrants them.
- Use a browser or component runner for behavior that static checks cannot prove. Record the route, state, actions, expected result, actual result, and console/network issues.
- Report actual checks and keep unverified API, deployment, browser, SSR, performance, and accessibility boundaries distinct.
