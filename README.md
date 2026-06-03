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

- local AI Skill audits across Codex, Claude Code, Cursor, and other Agent environments
- Skill registry and marketplace review
- install-time permission gates
- enterprise approval workflows
- hackathon and demo judging
- Skill authoring, token efficiency, and taxonomy optimization

## Benchmark Snapshot

SkillTrust was run against 28 representative packages from popular public AI Skill, Claude Skill, Cursor rule, and Agent instruction ecosystems.

Preliminary static benchmark result:

- 24 allow
- 4 warn
- 0 block

The benchmark found no broad malicious pattern in the sampled packages. Its stronger finding is that even high-quality packages benefit from intent-bound governance: connector scopes, user-confirmation gates, semantic false-positive handling, reference splitting, token efficiency, and taxonomy clarity.

See [Popular AI Skill Ecosystem Benchmark](docs/benchmarks/popular-skills-benchmark.md).

## Install

### Universal One-Prompt Agent Install

Paste this prompt into any local AI Agent, including Codex, Claude Code, Cursor, or another coding Agent:

```text
Install SkillTrust from https://github.com/qybaihe/SkillTrust for the current AI Agent environment. First detect whether this environment is Codex, Claude Code, Cursor, or another local Agent. If the host has a user-level Skills, extensions, rules, or reusable-agent-instructions directory, install SkillTrust there; otherwise install it as a general local tool. Verify that SkillTrust is usable, detect the current Agent's local Skills/extensions/rules root if one exists, then run a read-only first audit of that local Agent package ecosystem. If no local Agent root exists, audit the included demo fixtures and explain how I can pass a target Skill directory. Do not modify, rename, or remediate any existing local Skill, rule, extension, or Agent instruction automatically; only generate reports, policy overlays, and approval plans. After the audit, summarize allow/warn/block counts, dangerous or overprivileged findings, and the next safest remediation steps.
```

This is the recommended installation path because SkillTrust is meant to be used by whichever host Agent is running it. The Agent installs it, verifies it, detects the local Agent package root when available, audits the local Skill or instruction ecosystem, and keeps all real packages unchanged unless you explicitly approve follow-up edits.

### After Installation

Ask your Agent:

```text
Use SkillTrust to run a read-only audit of my local AI Agent Skills, rules, extensions, or reusable instructions, and tell me which ones are overprivileged, dangerous, ambiguous, or worth optimizing.
```

## Use

SkillTrust is meant to be used through natural-language requests to your Agent. Copy one of these prompts.

### Audit All Local Agent Packages

```text
Use SkillTrust to audit all local AI Agent Skills, rules, extensions, and reusable instructions in this environment. Keep the audit read-only. Tell me which packages are allow, warn, or block, and highlight the most important permission overreach, dangerous data-flow, ambiguity, and optimization findings.
```

### Audit One Skill

```text
Use SkillTrust to audit this Skill or Agent package: <paste the path, repository, or folder here>. Explain what it claims to do, what permissions it really needs, what behavior it exposes, whether anything exceeds its intent, and whether I should allow, warn, or block it.
```

### Check Before Installing

```text
Use SkillTrust as an install-time gate for this Skill package: <paste the path, repository, or folder here>. Give me a clear allow, warn, or block decision, and explain the evidence behind it.
```

### Generate A Reviewable Remediation Plan

```text
Use SkillTrust to create a reviewable remediation plan for this Skill package: <paste the path, repository, or folder here>. Do not modify the original package. Generate the least-privilege policy overlay, narrowed permission recommendations, and the safest next edits for me to approve.
```

### Add Host-Agent Semantic Review

```text
Use SkillTrust's host-Agent semantic review for this Skill package: <paste the path, repository, or folder here>. First read the core documents fully, then compare declared intent against observed behavior, preserve deterministic evidence, and produce the fused trust decision.
```

SkillTrust does **not** call OpenAI, Anthropic, or any external model API. No API key is required. The semantic reviewer is the Agent already running SkillTrust.

### Optimize Skill Quality

```text
Use SkillTrust to review this Skill ecosystem for authoring quality, token efficiency, and taxonomy clarity. Keep all changes as recommendations or approval plans unless I explicitly approve edits.
```

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
