# External Baseline Benchmark

Date: 2026-06-08

This benchmark compares SkillTrust with well-known security scanners, supply-chain tools, and LLM guardrail/evaluation tools. The point is not to claim that one tool replaces the others. The point is to show where SkillTrust adds a missing layer: install-time, intent-bound permission governance for AI Skill packages, plus optimization guidance that can reduce always-loaded Skill tokens.

Chinese version: [外部基线 Benchmark](external-baseline-benchmark.zh-CN.md).

## Headline Result

- Compared tools: 17
- SkillTrust governance capabilities covered: 15 / 15
- Best external baseline coverage on these Skill-governance dimensions: 7 / 15
- Fixture install decisions matched expected outcomes: 3 / 3
- Optimized Skill packages measured: 28
- Published first-pass activation-token reduction on the original 28-package sample: 30699 -> 23867, saving 6832 tokens (22.3%)
- Optimized preview pack rescan: only 250 residual tokens left to save (1.5%), which indicates the preview pack is already compact

## Fixture Decision Benchmark

| Fixture | Scenario | Expected | SkillTrust | Score | Risk | Findings | Token Saved |
| --- | --- | --- | --- | ---: | --- | ---: | ---: |
| `benign-pdf-skill` | low-risk PDF summarization Skill with local-only file handling | `allow` | `allow` | 100 | Trusted | 0 | 0 |
| `overprivileged-research-skill` | research Skill that asks for broader network, home, shell, and credential surfaces than its declared intent needs | `warn` | `warn` | 45 | Overprivileged | 5 | 0 |
| `malicious-like-writing-skill` | writing Skill fixture with sensitive local credential and network exfiltration-shaped behavior | `block` | `block` | 25 | Critical Risk | 6 | 0 |

## Capability Matrix

Legend: `yes` means the capability is a direct target of the tool class; `partial` means it can contribute evidence but does not produce the SkillTrust-style artifact or decision; `no` means outside the tool's main scope.

| Tool | Category | Local Status | Skill Package | Intent | Overreach | Agent Review | Decision | Policy | Optimized Skill | Token Saving | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SkillTrust | AI Skill governance | available | yes | yes | yes | yes | yes | yes | yes | yes | purpose-built for install-time AI Skill intent and permission governance |
| SkillGuard | AI Skill / agent safety research | not_run | yes | yes | yes | no | yes | no | no | no | closest conceptual baseline for AI Skill risk review when available |
| Scandar | AI agent / Skill scanner | not_run | yes | yes | yes | no | yes | no | no | no | specialized scanner-style baseline for AI agent instructions and tools |
| [Socket.dev](https://docs.socket.dev/) | software supply-chain security | not_installed | no | no | no | no | no | no | no | no | excellent package/dependency risk scanner; not an AI Skill intent-governance layer |
| [Semgrep](https://docs.semgrep.dev/) | SAST | not_installed | no | no | no | no | no | no | no | no | strong source-code pattern and SAST baseline; does not infer AI Skill declared intent |
| [CodeQL](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql) | semantic code analysis | not_installed | no | no | no | no | no | no | no | no | deep semantic source-code analysis baseline; not an install-time Skill permission model |
| [Gitleaks](https://github.com/gitleaks/gitleaks) | secret scanning | not_installed | no | no | no | no | no | no | no | no | secret detection baseline; catches leaked credentials, not permission overreach |
| [TruffleHog](https://github.com/trufflesecurity/trufflehog) | secret scanning | not_installed | no | no | no | no | no | no | no | no | secret detection baseline; useful for repository history and verified credential checks |
| [OSV-Scanner](https://google.github.io/osv-scanner/) | dependency vulnerability scanning | not_installed | no | no | no | no | no | no | no | no | known-vulnerability baseline for lockfiles/SBOMs; not an AI Skill intent scanner |
| [Trivy](https://trivy.dev/) | vulnerability / misconfiguration scanning | not_installed | no | no | no | no | no | no | no | no | broad CVE, IaC, container, and secret scanning baseline |
| [Grype](https://github.com/anchore/grype) | vulnerability scanning | not_installed | no | no | no | no | no | no | no | no | SBOM/package vulnerability scanning baseline |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) | project security posture | not_installed | no | no | no | no | no | no | no | no | repository health and supply-chain best-practice baseline |
| OpenSSF Package Analysis | dynamic package behavior analysis | not_run | no | no | no | no | no | no | no | no | dynamic package install behavior baseline; useful for dependency ecosystem risk |
| [promptfoo](https://www.promptfoo.dev/docs/intro/) | LLM red teaming / evals | not_installed | no | no | no | yes | no | no | no | no | LLM app evaluation and red-team baseline; tests model behavior, not install-time Skill permissions |
| [garak](https://github.com/NVIDIA/garak) | LLM vulnerability scanning | not_installed | no | no | no | yes | no | no | no | no | LLM vulnerability scanner; targets deployed model/app behavior rather than Skill package governance |
| [Lakera Guard](https://www.lakera.ai/guard) | LLM security guardrail | not_run | no | no | no | yes | no | no | no | no | runtime prompt-injection and content-risk guardrail; not a package optimizer |
| [NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/latest/index.html) | LLM guardrails framework | not_installed | no | no | no | yes | no | no | no | no | runtime conversational guardrails framework; not an AI Skill permission analyzer |

## Detailed Governance Dimensions

| Capability | SkillTrust | Best External Baselines | Why It Matters For AI Skills |
| --- | --- | --- | --- |
| AI Skill package | yes | SkillGuard, Scandar | The unit under review is a reusable AI Skill package, not only a repository or dependency graph. |
| declared intent | yes | SkillGuard, Scandar | A Skill should be judged against what it claims to do. |
| required permissions | yes | none directly | Least privilege requires inferring the minimum permission set needed for that intent. |
| observed permission surface | yes | SkillGuard, Scandar, Socket.dev, Semgrep, CodeQL, ... | Observed filesystem, shell, environment, network, connector, dependency, and prompt surfaces must remain visible. |
| intent vs permission overreach | yes | SkillGuard, Scandar | The core governance question is whether observed/requested permissions exceed declared intent. |
| line-level evidence | yes | SkillGuard, Scandar, Socket.dev, Semgrep, CodeQL, ... | Reviewers need reproducible evidence, not only a score. |
| Agent semantic review | yes | promptfoo, garak, Lakera Guard, NeMo Guardrails | A host Agent can read examples and docs end-to-end to mark likely false positives without deleting evidence. |
| allow/warn/block decision | yes | SkillGuard, Scandar | Install-time gates need a conservative action. |
| critical data-flow guard | yes | SkillGuard, Scandar, promptfoo, garak, Lakera Guard, ... | Sensitive local data to network-like sinks cannot be semantically upgraded to safe. |
| permission manifest | yes | none directly | The review should produce an installable least-privilege contract. |
| policy overlay | yes | none directly | A policy overlay lets a host runtime enforce or display the boundary. |
| audit receipt | yes | none directly | Receipts make the review replayable with hashes and rule versions. |
| remediation plan | yes | none directly | Governance should explain how to converge the Skill to least privilege. |
| optimized Skill package | yes | none directly | SkillTrust can emit a preview package rather than only a finding list. |
| token efficiency | yes | none directly | Moving deterministic detail out of always-loaded instructions can lower activation context cost. |

## Token-Saving Benchmark

SkillTrust has two token-efficiency measurements in this repository:

- Original public benchmark sample: `30699` -> `23867` estimated activation-body tokens, saving `6832` tokens (`22.3%`).
- Optimized preview pack rescan: `16583` -> `16333` estimated activation-body tokens, with only `250` residual tokens left to save (`1.5%`).

The first number shows the product value: SkillTrust finds token waste in the original packages. The second number is a regression check: after SkillTrust emits optimized preview packages, the remaining always-loaded token waste is much smaller.

- Original skills with token-saving opportunities: 20 / 28
- Original scriptification candidates: 26
- Original reference extraction candidates: 17
- Optimized preview packages with remaining token-saving opportunities: 5 / 28
- Remaining scriptification/config candidates after preview optimization: 5

Top residual opportunities after the optimized preview pack rescan:

| Skill | Activation Tokens | Estimated Saved | Token Score |
| --- | ---: | ---: | ---: |
| `compliance-checker` | 587 | 50 | 91 |
| `verify-language` | 568 | 50 | 91 |
| `verify-patterns` | 540 | 50 | 91 |
| `verify-quality` | 554 | 50 | 91 |
| `verify-security` | 560 | 50 | 91 |

## Interpretation

- SAST, CVE, secret scanning, package behavior analysis, and LLM red-team tools remain valuable complements.
- SkillTrust's differentiated layer is the AI Skill install boundary: declared intent, least-privilege permission inference, overreach detection, conservative fusion with Agent review, policy artifacts, remediation, and optimized preview packages.
- The token-saving metric is an activation-context estimate, not a billing guarantee. It is still useful because Skill packages often load instruction text before any task-specific evidence is needed.

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python scripts/external_baseline_benchmark.py
```

This regenerates:

- `docs/benchmarks/external-baseline-results.json`
- `docs/benchmarks/external-baseline-benchmark.md`
- `docs/benchmarks/external-baseline-benchmark.zh-CN.md`

## Caveats

- External tools are not forced through network installs. If a local CLI is unavailable, the result is marked `not_installed` or `not_run`.
- Specialized scanners should be evaluated on their native tasks before making broad security claims.
- SkillTrust benchmark claims are limited to AI Skill package governance and token-efficiency planning.
