---
name: angular-architecture
description: Analyze or change Angular application architecture, DI and state ownership, reactive data flow, routing, rendering, or host/custom-element integration. Use for an explicit architecture question or a change crossing those boundaries, not routine member ordering or a simple template edit.
metadata:
  version: "v0.4.7"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Angular Architecture

Start from the affected feature and its callers. Resolve the actual Angular, TypeScript, RxJS and build-tool versions, application entrypoints, compilation targets, providers and relevant project instructions; a mixed-version workspace may contain separate runtimes.

## Trace the behavior before proposing a boundary

- Map the user event through component, form, service/store, request and render. Identify the single owner and lifetime of each persisted or shared state; distinguish derived state from independently mutable flags.
- Follow provider placement and injector scope, including lazy routes, component providers and dynamically loaded elements. Moving a service or provider can change instance identity and lifetime even when the API is unchanged.
- Follow observable subscriptions, cancellation, signal dependencies and asynchronous results across navigation, input changes and teardown. Do not treat Signals and RxJS as interchangeable or assume a newer API exists in the current runtime.
- For Host/custom-element boundaries, inspect both owners: selector, properties/attributes, events and detail, routing/session ownership, shared assets and bundle loading. Local UI success does not establish Host or backend integration.
- For rendering or performance questions, identify the exercised change-detection/render path and actual measurements before recommending memoization, state migration, SSR or hydration changes.

## Choose the smallest useful structure

Keep screen coordination, local form interaction and DOM/lifecycle behavior near the component. Place shared state, request lifetime and API access with the existing feature service/store owner; place reusable pure transformations near their feature. Do not move everything into a service or add wrappers only to reduce component length.

Compare a proposed boundary with the current structure using change coupling, lookup cost, lifetime and testability. Preserve initialization, mutation/reference behavior, event order and public interfaces. A framework upgrade, new state library or cross-owner API change requires task scope that includes it.

## Deliver evidence at the requested level

For analysis, provide the current flow, concrete problem, viable alternatives and trade-offs, unresolved requirements and a minimal next step; a small Mermaid diagram can clarify ownership. Do not implement when only analysis was requested.

For authorized changes, verify affected behavior with the smallest sufficient existing checks. Distinguish static checks, local component tests, actual request/persistence behavior and cross-runtime integration; name unverified boundaries. Report files/symbols and source revision rather than unsupported generic architecture findings.
