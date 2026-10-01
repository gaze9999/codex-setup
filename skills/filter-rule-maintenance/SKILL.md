---
name: filter-rule-maintenance
description: Add, modify, diagnose, or verify AdGuard, uBlock Origin, DNS filter, hosts, proxy, or similar blocking and rewrite rules with parser-aware minimal matching and false-positive control. Do not use for generic YAML, JSON, or TOML editing.
metadata:
  version: "v0.4.5"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Filter Rule Maintenance

Maintain filtering rules from the actual engine, syntax, evidence, and desired behavior. Prefer the narrowest rule that solves the observed problem without unrelated blocking.

## Establish the rule environment

- Identify the engine and version, rule-list type, parser, supported syntax, load order, platform, client application, and any generated-file or update-header conventions.
- Read nearby rules and repository guidance. Check for equivalent, overlapping, shadowed, disabled, exception, or conflicting rules before adding another.
- Determine the exact target behavior from available request, DNS, network, element, application, or test evidence. Do not invent a hostname, path, selector, parameter, process, or protocol from a visual symptom alone.
- Keep private endpoints, query values, account identifiers, cookies, tokens, and unredacted traffic logs out of source and reports.

## Change minimally

- Match only the necessary domain, subdomain, path, query parameter, resource type, application, or element. Avoid broad wildcards, root-domain blocks, regex, or cosmetic selectors when a narrower native rule works.
- Use engine-native syntax before regex. When regex is necessary, anchor it, escape it for the actual parser, and consider case, encoding, separators, ports, schemes, and query ordering.
- Preserve rule order, comments, grouping, exceptions, metadata, and generated sections unless their change is required.
- Add a short comment only when the rule's purpose, evidence, or exception is not evident from the rule itself.
- Do not combine unrelated targets in one rule merely to shorten the file. Keep allow/exception behavior explicit when the engine's precedence makes it significant.

## Verify

- Use the engine's validator, parser, test UI, dry run, or deterministic fixture when available. Text appearance alone does not prove that the rule parses or wins precedence.
- Test the intended match and representative near misses, including parent/sibling domains, unrelated paths, required assets, authentication, media, notifications, and application startup when relevant.
- Distinguish syntax validity, matching behavior, list loading, cache or DNS propagation, client refresh, and observed UI/network effect.
- Update timestamps, checksums, generated output, or release metadata only when required by the repository's established process.
- Report the exact rule and engine tested, evidence used, actual matches and non-matches, and any device, platform, cache, network, or visual behavior not verified.
