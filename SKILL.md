---
name: skilltrust
description: Use when auditing, installing, reviewing, or governing AI Skill packages, Agent rules, extensions, or reusable instructions for intent-bound least-privilege permissions, overprivileged behavior, dangerous data flows, host-Agent semantic review, policy overlays, remediation plans, token efficiency, or taxonomy conflicts.
---

# SkillTrust

SkillTrust is an Agent-first trust and permission governance Skill for AI Skills, rules, extensions, and reusable Agent instructions.

Use it to answer:

- What does this package claim to do?
- What permissions are actually necessary for that intent?
- What behavior is requested or observable?
- Does behavior exceed the declared intent boundary?
- How should the package be constrained before use or installation?

## Required Reference Loading

Do not treat this `SKILL.md` as the full rulebook. Load the relevant reference file before each step:

- Always start with `references/00-safety-boundaries.md`.
- For the Agent-first review philosophy, read `references/01-agent-first-review.md`.
- For local portfolio audits, read `references/02-local-portfolio-audit.md`.
- For one-package audits, read `references/03-single-package-audit.md`.
- For host-Agent semantic review and fusion, read `references/04-semantic-fusion.md`.
- For permission policy and remediation planning, read `references/05-policy-remediation.md`.
- For authoring length, token efficiency, and taxonomy optimization, read `references/06-authoring-token-taxonomy.md`.
- For user-facing summaries, read `references/07-reporting.md`.

## Core Operating Stance

SkillTrust is not a keyword-only scanner. Deterministic code is used to collect evidence, line numbers, hashes, reproducible findings, and policy drafts. The host Agent must read the target package content, understand the declared intent, and make the deeper semantic permission judgment.

When evidence and semantics disagree, preserve the evidence, explain the disagreement, and keep any real remediation or rename action pending user approval.
