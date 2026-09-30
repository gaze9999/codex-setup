---
name: vue-development
description: Implement, refactor, diagnose, or review Vue, Nuxt, or Vite-based applications while preserving the detected framework versions, component contracts, state, routing, SSR or hydration, styling, and build behavior.
metadata:
  version: "v0.4.3"
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
- Preserve Vue reactivity semantics. Do not destructure reactive state, replace refs, or move effects across lifecycle boundaries without checking dependency tracking and cleanup.
- Keep local state local. Use a composable or store only when ownership, reuse, lifecycle, and persistence justify it; do not move state globally for convenience.
- For Nuxt or SSR, separate server-only and client-only APIs, avoid request state leaking across users, and preserve hydration-compatible initial output. Guard browser globals and side effects.
- Preserve router guards, lazy-loading, error boundaries, loading states, empty states, forms, keyboard/focus behavior, and existing accessibility.
- Prefer scoped or project-standard styling and existing design tokens. Avoid broad global selectors, accidental deep styling, or a new UI pattern for one component.
- Migrate API style, state library, router, bundler, or UI library only when explicitly requested.

## Verify

- Run the repository's narrowest applicable type, unit/component, lint, and build checks. Do not invent generic package-manager commands when project scripts or workspace targets exist.
- Add or update focused tests for changed component contracts, reactivity, routing, store behavior, SSR/hydration, or user interaction when the task warrants them.
- Use a browser or component runner for behavior that static checks cannot prove. Record the route, state, actions, expected result, actual result, and console/network issues.
- Report actual checks and keep unverified API, deployment, browser, SSR, performance, and accessibility boundaries distinct.
