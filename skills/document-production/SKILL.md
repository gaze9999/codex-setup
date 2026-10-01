---
name: document-production
description: Create finished document artifacts from user requirements and source material; default to PDF when no format is specified.
metadata:
  short-description: Default-PDF document production pipeline with DOCX and Markdown support
  version: "v0.4.5"
  author: "gaze9999"
  repository: "https://github.com/gaze9999/codex-setup"
---

# Document Production

Turn user content, sources, and constraints into deliverable documents rather than drafts or generation prompts. Default to PDF; honor explicit DOCX, Markdown, or multi-format requests.
Activate only when the user explicitly requests a finished downloadable artifact. For chat-only drafting, summaries, translation, or planning, use the corresponding workflow instead.

## Core workflow

- Derive the goal, audience, existing material, required sources, and constraints from the request before building the information architecture; ask only for gaps that materially affect the artifact.
- When external information is required, use reliable sources that directly support the claim and verify time-sensitive facts first.
- Create an actual openable artifact. Preserve user-supplied facts, figures, terminology, and citations; do not invent unsupported information.
- Read [Document Production Guidelines](references/document-production-guidelines.md) when format-specific or layout guidance is needed.

## Format and quality

- PDF: preserve selectable text and correct Traditional Chinese or Japanese rendering; inspect contents, headings, tables, and whitespace when rendering is available.
- DOCX: use native Heading, TOC, and page-number fields; render when needed to confirm pagination and contents.
- Markdown: keep a continuous heading hierarchy and do not simulate pagination or fixed paper layout.
- Across formats, keep facts, sections, and citations consistent while allowing format-specific layout differences.

For scientific, medical, health, pharmaceutical, or psychological content, use APA 7 in-text citations and references. All other factual claims also require traceable sources that directly support them.

## On-demand verification

When a compatible Python runtime is available, resolve and run the matching validator relative to this Skill: `scripts/validate_pdf.py`, `scripts/validate_docx.py`, `scripts/validate_markdown.py`, or `scripts/validate_apa7.py`. Otherwise use equivalent available inspection and report the bundled validator as not run. Install optional tooling only with user authorization. When rendering or another check cannot be completed, mark it unverified with the reason rather than claiming success.

In the final response, list only deliverable links, formats, completed checks, and unverified items.
