# SkillTrust

[简体中文](README.zh-CN.md) · [Installation](#installation) · [Quick Start](#quick-start) · [Host-Agent Semantic Review](#host-agent-semantic-review)

![SkillTrust cover](docs/assets/skilltrust-cover.png)

**Intent-bound permission governance for AI Skills.**

It turns an untrusted Skill package into a least-privilege permission manifest, an install-time policy overlay, an audit receipt, a trust report, and a conservative install decision.

Unlike a simple keyword scanner, SkillTrust asks a harder question:

> What is the minimum permission set required for this Skill to do what it claims, and does its observed behavior exceed that intent-bound boundary?

## At A Glance

![SkillTrust architecture flow](docs/assets/skilltrust-flow.png)

SkillTrust is not a normal security scanner. It is an install-time governance pipeline:

- It reads the Skill package as untrusted evidence.
- It extracts declared intent and scans observed behavior deterministically.
- It asks the host Agent to read the core documents end-to-end and produce semantic permission judgment.
- It fuses both layers conservatively, keeping deterministic evidence authoritative.
- It emits a least-privilege governance bundle that can drive `allow`, `warn`, or `block`.

Primary outputs:

```text
permission_manifest.json
skilltrust-policy.json
trust_report.md / fused_trust_report.md
audit_receipt.json
remediation_plan.md
install_decision.json / fused_install_decision.json
```

## Why This Exists

AI Skills are becoming reusable operational packages: browser workflows, Gmail assistants, research agents, PDF summarizers, form fillers, document generators, and local automation tools.

That ecosystem needs more than "dangerous keyword" detection:

- `curl` may be justified for research, but not for a PDF summarizer.
- Browser access may be necessary for form filling, but not for local document formatting.
- A research Skill may need public web access, but not `.env`, SSH keys, browser cookies, or unrelated telemetry endpoints.
- A writing Skill that reads a token and posts to a webhook should be blocked even if its README sounds harmless.

SkillTrust provides the missing install-time trust layer: **intent-bound, least-privilege, auditable permission governance**.

## Architecture

SkillTrust combines deterministic evidence collection with host-Agent semantic review. It does **not** call OpenAI, Anthropic, or any external model API. It does **not** require an API key.

1. **Deterministic scanner**

   Python collects reproducible evidence: declared intent, inferred required permissions, observed permissions, file/line findings, hashes, base score, policy, manifest, and receipt.

2. **Host-Agent semantic review**

   The current Agent reads `semantic_review_request.json` and `semantic_review_instructions.md`, reads the listed `SKILL.md` / README core documents end-to-end, then writes `semantic_review.json`.

3. **Conservative fusion layer**

   Python fuses `analysis.json` and `semantic_review.json`, preserves every deterministic finding, applies semantic labels and policy refinements, and emits a final allow/warn/block install decision.

## Key Features

- **Intent vs behavior analysis**: compares what the Skill claims with what its files actually request.
- **Least-privilege permission inference**: converts declared intent into minimum required filesystem, network, shell, connector, dependency, and prompt boundaries.
- **Permission overreach detection**: catches good-intent Skills that ask for too much access.
- **Host-Agent semantic review**: lets the running Agent read full core documents before judging findings, without any API key.
- **Conservative fusion**: semantic review can annotate findings, but cannot delete evidence or override critical data-flow blocks.
- **Install-time gate**: returns `allow`, `warn`, or `block`.
- **Policy overlay**: emits `skilltrust-policy.json` with filesystem, network, environment, shell, connector, dependency, prompt, and semantic refinements.
- **Reproducible audit receipt**: records file hashes, rules version, result hash, and evidence hashes.
- **Skill authoring optimizer**: checks whether `SKILL.md` should be split into a compact harness plus `references/`.
- **Token efficiency optimizer**: finds instructions that should become scripts, config, schema, or validators.
- **Skill taxonomy optimizer**: detects ambiguous names, overlapping descriptions, and routing conflicts across a Skill ecosystem.

## Repository Layout

```text
skilltrust/
  cli.py                 # CLI entry point
  analyzer.py            # deterministic analysis pipeline
  semantic.py            # host-Agent review request and fusion layer
  findings.py            # static permission behavior scanner
  permissions.py         # least-privilege permission inference
  scoring.py             # Trust Fit Score
  policy.py              # permission manifest and policy overlay
  receipt.py             # reproducible audit receipt
  reporting.py           # markdown/json outputs
  governance.py          # local Skill portfolio audit
  authoring.py           # SKILL.md harness optimizer
  token_optimizer.py     # token/scriptification optimizer
  taxonomy.py            # Skill naming and trigger taxonomy optimizer
fixtures/
  benign-pdf-skill/
  overprivileged-research-skill/
  malicious-like-writing-skill/
docs/
  assets/
  diagrams/
tests/
SKILL.md
pyproject.toml
```

## Installation

### Requirements

- Python 3.10+
- Git
- Optional: Node.js only if you want to re-render the Excalidraw diagram assets

SkillTrust has no runtime dependency on OpenAI, Anthropic, or external LLM SDKs.

### Clone

```bash
git clone https://github.com/qybaihe/SkillTrust.git
cd SkillTrust
```

### Run Directly

```bash
python -m skilltrust --help
python -m skilltrust analyze fixtures/overprivileged-research-skill
```

### Install The CLI

```bash
python -m pip install -e .
skilltrust --help
skilltrust analyze fixtures/overprivileged-research-skill
```

### Install As A Local Codex Skill

#### One-Prompt Agent Install

Paste this prompt into Codex or another local coding Agent:

```text
Install SkillTrust as a local Codex Skill from https://github.com/qybaihe/SkillTrust. Clone or update it at ~/.codex/skills/skilltrust, install the CLI with python -m pip install -e ., verify both skilltrust --help and python -m skilltrust --help, then run a read-only local Skill portfolio audit with skilltrust audit-local --skills-root ~/.codex/skills --out ~/.codex/skills/skilltrust/reports/local-all. Do not modify, rename, or remediate any existing local Skill automatically; only generate reports, policy overlays, and approval plans. After the audit, summarize allow/warn/block counts, dangerous or overprivileged findings, and the next safest remediation steps.
```

This gives the host Agent a complete setup goal: install SkillTrust, verify the command, audit the local Skill ecosystem, and keep all real Skills unchanged unless the user explicitly approves follow-up edits.

#### Manual Install

If you want to install it yourself, clone it into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/qybaihe/SkillTrust.git ~/.codex/skills/skilltrust
cd ~/.codex/skills/skilltrust
python -m pip install -e .
```

Then ask your Agent:

```text
Use SkillTrust to run a read-only audit of my local Codex Skills and tell me which ones are overprivileged, dangerous, or worth optimizing.
```

The root `SKILL.md` explains the workflow the Agent should follow after SkillTrust is loaded.

## Quick Start

Run the main demo fixture:

```bash
skilltrust analyze fixtures/overprivileged-research-skill --out reports/demo-overprivileged
```

Expected result:

```text
SkillTrust score: 45/100 (Overprivileged)
Declared intent: research, document generation
Findings: 5
```

Generated artifacts:

```text
reports/demo-overprivileged/
  analysis.json
  trust_report.md
  permission_manifest.json
  skilltrust-policy.json
  audit_receipt.json
  remediation_plan.md
```

## Host-Agent Semantic Review

SkillTrust's semantic review does not call a model API. It prepares a local evidence bundle for the Agent that is already running the Skill.

Generate a review request:

```bash
skilltrust analyze fixtures/overprivileged-research-skill \
  --agent-review-request \
  --out reports/demo-agent-overprivileged
```

This writes:

```text
reports/demo-agent-overprivileged/
  analysis.json
  semantic_review_request.json
  semantic_review_instructions.md
```

The host Agent should then:

- read `semantic_review_request.json`
- read `semantic_review_instructions.md`
- read every file listed in `core_documents_to_read` end-to-end
- assess every deterministic finding
- write `semantic_review.json`

For offline demos and tests, SkillTrust can create a draft review without any API call:

```bash
skilltrust draft-semantic-review \
  reports/demo-agent-overprivileged/semantic_review_request.json \
  --out reports/demo-agent-overprivileged/semantic_review.json
```

Fuse deterministic evidence with semantic review:

```bash
skilltrust fuse \
  reports/demo-agent-overprivileged/analysis.json \
  reports/demo-agent-overprivileged/semantic_review.json \
  --out reports/demo-agent-overprivileged-fused
```

Expected result:

```text
Fused install decision: warn (45 +0 -> 45)
```

Fused outputs:

```text
reports/demo-agent-overprivileged-fused/
  fused_analysis.json
  fused_trust_report.md
  fused_install_decision.json
  skilltrust-policy.json
  semantic_review_summary.md
```

## CLI Commands

```bash
skilltrust analyze <skill-path> [--out reports/name] [--agent-review-request]
skilltrust review-request <skill-path> --out reports/name
skilltrust draft-semantic-review <semantic_review_request.json> --out <semantic_review.json>
skilltrust fuse <analysis.json> <semantic_review.json> --out reports/fused
skilltrust install-check <skill-path> --out reports/install-check
skilltrust remediate <skill-path> --out reports/remediated
skilltrust audit-local --skills-root ~/.codex/skills --out reports/local-all
skilltrust authoring-audit <skill-path> --out reports/authoring
skilltrust token-optimize <skill-path> --out reports/token
skilltrust taxonomy-audit --skills-root ~/.codex/skills --out reports/taxonomy
```

## Fixture Results

| Fixture | Declared Intent | Score | Risk Level | Install Gate |
| --- | --- | ---: | --- | --- |
| `fixtures/benign-pdf-skill` | PDF summarization | 100 | Trusted | allow |
| `fixtures/overprivileged-research-skill` | Research/reporting | 45 | Overprivileged | warn |
| `fixtures/malicious-like-writing-skill` | Writing assistant | 25 | Critical Risk | block |

## Critical Data-Flow Protection

Semantic review is intentionally not allowed to erase deterministic evidence.

If the deterministic scanner finds critical sensitive-source-to-network-sink evidence, fusion keeps the final decision blocked:

```bash
skilltrust analyze fixtures/malicious-like-writing-skill \
  --agent-review-request \
  --out reports/demo-agent-critical

skilltrust draft-semantic-review \
  reports/demo-agent-critical/semantic_review_request.json \
  --out reports/demo-agent-critical/semantic_review.json

skilltrust fuse \
  reports/demo-agent-critical/analysis.json \
  reports/demo-agent-critical/semantic_review.json \
  --out reports/demo-agent-critical-fused
```

Expected result:

```text
Fused install decision: block (25 +0 -> 25)
critical_dataflow_protected = true
```

## Local Skill Portfolio Audit

Audit a local Skill ecosystem:

```bash
skilltrust audit-local --skills-root ~/.codex/skills --out reports/local-all
```

The local portfolio workflow writes one governance bundle per Skill and a dashboard:

```text
reports/local-all/
  local_skills_report.md
  local_skills_summary.json
  skills/<skill-name>/
```

In the original development workspace, SkillTrust audited 56 local Skills:

| Total | Allow | Warn / Overlay Required | Block |
| ---: | ---: | ---: | ---: |
| 56 | 36 | 19 | 1 |

The generated local reports are not committed to this repository because they may contain local paths or private profile evidence.

## Trust Fit Score

SkillTrust scores packages from 0 to 100:

| Score | Level |
| ---: | --- |
| 85-100 | Trusted |
| 70-84 | Mostly Trusted |
| 50-69 | Needs Review |
| 30-49 | Overprivileged |
| 0-29 | Critical Risk |

The score combines:

- Intent Clarity
- Permission Necessity
- Overreach Ratio
- Sensitive Surface
- Data Flow Safety
- Install-Time Safety
- Prompt Integrity
- Enforceability
- Auditability

Critical data-flow evidence caps the result at Critical Risk. Multiple high-severity sensitive overreach findings cap the result at Overprivileged.

## Policy Model

`skilltrust-policy.json` expresses an install-time boundary:

- filesystem allow/deny scopes
- network allow/deny domains and methods
- environment variable deny patterns
- shell command allow/deny lists
- connector consent requirements
- dependency and postinstall constraints
- prompt-integrity constraints
- host-Agent semantic refinements
- audit logging requirements

The policy is a governance contract. It can be enforced by a future Skill installer, runner, registry, or sandbox adapter.

## Safety Boundaries

- SkillTrust performs static analysis by default.
- It does not execute target Skills.
- It does not call external model APIs.
- It does not require API keys.
- It does not make network calls to validate endpoints.
- It treats target package files as untrusted evidence.
- It preserves deterministic findings during semantic fusion.
- Real local Skill audits should avoid publishing private reports.

## Development

Run tests:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
```

Expected:

```text
15 passed
```

Re-render the hand-drawn architecture diagrams:

```bash
node ~/.codex/skills/excalidraw/scripts/render.js \
  docs/diagrams/skilltrust-flow.excalidraw \
  docs/assets/skilltrust-flow.png

node ~/.codex/skills/excalidraw/scripts/render.js \
  docs/diagrams/skilltrust-flow.zh-CN.excalidraw \
  docs/assets/skilltrust-flow.zh-CN.png
```

## Hackathon Narrative

SkillTrust is not just a scanner. It is an install-time trust layer for AI Skills:

> SkillTrust combines reproducible static evidence with host-Agent semantic permission reasoning to make AI Skills installable with intent-bound trust.

That makes it useful for Skill registries, Agent marketplaces, enterprise approval workflows, and local developer toolchains.
