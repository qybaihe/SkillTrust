# SkillTrust

[简体中文](README.zh-CN.md) · [Install](#install) · [Use](#use) · [Outputs](#outputs)

![SkillTrust cover](docs/assets/skilltrust-cover.png)

**Intent-bound permission governance for AI Skills.**

SkillTrust turns an untrusted AI Skill package into an intent-bound, least-privilege, auditable governance bundle.

It is not just a scanner asking:

> Is this Skill dangerous?

SkillTrust asks the more useful install-time question:

> What is the minimum permission set required for this Skill to do what it claims, and does its observed behavior exceed that boundary?

## At A Glance

![SkillTrust architecture flow](docs/assets/skilltrust-flow.png)

SkillTrust combines two layers:

- **Deterministic evidence**: reproducible findings, file evidence, hashes, permission surfaces, data-flow signals, trust score, policy, and audit receipt.
- **Host-Agent semantic review**: the current Agent reads the Skill's core documents end-to-end and judges whether requested behavior is actually necessary for the declared intent.

The final result is conservative:

- deterministic findings are never deleted
- likely false positives can be marked, but evidence remains visible
- critical sensitive-data-to-network flow cannot be upgraded to safe
- the final install decision is always `allow`, `warn`, or `block`

## What SkillTrust Does

SkillTrust helps answer five questions before using or installing a Skill:

- What does this Skill claim to do?
- What permissions are truly required for that task?
- What filesystem, network, shell, environment, dependency, connector, prompt, or data-flow behavior does it expose?
- Does observed behavior exceed the declared intent?
- How can the Skill be constrained into a safer, auditable, installable package?

It is designed for:

- local Codex Skill audits
- Skill registry and marketplace review
- install-time permission gates
- enterprise approval workflows
- hackathon and demo judging
- Skill authoring, token efficiency, and taxonomy optimization

## Install

### One-Prompt Agent Install

Paste this prompt into Codex or another local coding Agent:

```text
Install SkillTrust as a local Codex Skill from https://github.com/qybaihe/SkillTrust. Clone or update it at ~/.codex/skills/skilltrust, set up the local skilltrust command, verify skilltrust --help works, then run a read-only local Skill portfolio audit with skilltrust audit-local --skills-root ~/.codex/skills --out ~/.codex/skills/skilltrust/reports/local-all. Do not modify, rename, or remediate any existing local Skill automatically; only generate reports, policy overlays, and approval plans. After the audit, summarize allow/warn/block counts, dangerous or overprivileged findings, and the next safest remediation steps.
```

This is the recommended installation path because SkillTrust is meant to be used by the host Agent. The Agent installs it, verifies it, audits the local Skill ecosystem, and keeps all real Skills unchanged unless you explicitly approve follow-up edits.

### After Installation

Ask your Agent:

```text
Use SkillTrust to run a read-only audit of my local Codex Skills and tell me which ones are overprivileged, dangerous, or worth optimizing.
```

## Use

### Audit All Local Skills

```bash
skilltrust audit-local --skills-root ~/.codex/skills --out reports/local-all
```

Use this to review your whole local Skill ecosystem. It produces a portfolio dashboard with `allow`, `warn`, and `block` decisions.

### Audit One Skill

```bash
skilltrust analyze ./path/to/skill --out reports/skill-audit
```

Use this before trusting, installing, publishing, or submitting a Skill.

### Install-Time Check

```bash
skilltrust install-check ./path/to/skill --out reports/install-check
```

Use this when you want a direct `allow`, `warn`, or `block` install decision.

### Generate A Reviewable Remediation Bundle

```bash
skilltrust remediate ./path/to/skill --out reports/remediated
```

This does not silently edit the target Skill. It generates policy overlays, narrowed permission manifests, remediation plans, and reviewable drafts.

### Add Host-Agent Semantic Review

```bash
skilltrust analyze ./path/to/skill --agent-review-request --out reports/agent-review
```

Then the host Agent reads the generated semantic review request, reads the listed core documents fully, writes `semantic_review.json`, and fuses it with deterministic evidence:

```bash
skilltrust fuse reports/agent-review/analysis.json reports/agent-review/semantic_review.json --out reports/agent-review-fused
```

SkillTrust does **not** call OpenAI, Anthropic, or any external model API. No API key is required. The semantic reviewer is the Agent already running SkillTrust.

### Optimize Skill Quality

```bash
skilltrust authoring-audit ./path/to/skill --out reports/authoring
skilltrust token-optimize ./path/to/skill --out reports/token
skilltrust taxonomy-audit --skills-root ~/.codex/skills --out reports/taxonomy
```

Use these when you want to improve Skill structure, reduce activation-token waste, or fix ambiguous Skill naming and routing.

## Outputs

SkillTrust can generate:

- `permission_manifest.json`: least-privilege permission model inferred from declared intent
- `skilltrust-policy.json`: policy overlay for filesystem, network, environment, shell, connector, dependency, prompt, and semantic constraints
- `trust_report.md`: human-readable deterministic trust report
- `fused_trust_report.md`: deterministic evidence plus host-Agent semantic review
- `audit_receipt.json`: reproducible audit receipt with hashes and rule metadata
- `remediation_plan.md`: concrete steps to converge the Skill to least privilege
- `install_decision.json`: install-time `allow`, `warn`, or `block`
- `local_skills_report.md`: local Skill portfolio dashboard
- `authoring_report.md`: Skill harness and reference-splitting recommendations
- `token_efficiency_report.md`: token waste and scriptification opportunities
- `skill_taxonomy_report.md`: naming, description, and routing ambiguity findings

## Trust Fit Score

SkillTrust scores packages from 0 to 100:

| Score | Level |
| ---: | --- |
| 85-100 | Trusted |
| 70-84 | Mostly Trusted |
| 50-69 | Needs Review |
| 30-49 | Overprivileged |
| 0-29 | Critical Risk |

The score considers intent clarity, permission necessity, overreach, sensitive surfaces, data-flow safety, install-time safety, prompt integrity, enforceability, and auditability.

## Safety Boundaries

- SkillTrust performs static analysis by default.
- It does not execute target Skills.
- It does not call external model APIs.
- It does not require API keys.
- It preserves deterministic evidence during semantic fusion.
- It keeps local Skill remediation and rename actions pending user approval.
- Real local audit reports may contain local paths or private evidence, so avoid publishing them directly.

## Demo Fixtures

| Fixture | Declared Intent | Score | Risk Level | Install Gate |
| --- | --- | ---: | --- | --- |
| `fixtures/benign-pdf-skill` | PDF summarization | 100 | Trusted | allow |
| `fixtures/overprivileged-research-skill` | Research/reporting | 45 | Overprivileged | warn |
| `fixtures/malicious-like-writing-skill` | Writing assistant | 25 | Critical Risk | block |

These fixtures show the difference between a benign Skill, a good-intent but overprivileged Skill, and a malicious-like Skill with sensitive data flow.

## Core Narrative

SkillTrust is not a keyword scanner. It is an install-time trust layer for AI Skills:

> SkillTrust combines reproducible evidence with host-Agent semantic permission reasoning to make AI Skills installable with intent-bound trust.
