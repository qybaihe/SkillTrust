# Popular AI Skill Ecosystem Benchmark

Date: 2026-06-03

This benchmark is a preliminary, static-only sample audit of popular public AI Skill, Agent rule, and reusable instruction ecosystems.

SkillTrust did **not** modify any third-party project. The benchmark is framed as governance research, not as a claim that the audited projects are malicious.

## Scope

Because local GitHub clone access was unreliable during this run, several targets were audited in `network-limited` mode using accessible raw files, public page snapshots, or installable package snapshots. Results should be read as representative sample findings, not complete repository-wide findings.

| Source | Ecosystem | Sample Count | Allow | Warn | Block | Audit Mode |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| [anthropics/skills](https://github.com/anthropics/skills) | Claude Skills | 3 | 2 | 1 | 0 | network-limited raw snapshot |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Claude Skills collection | 3 | 3 | 0 | 0 | network-limited raw snapshot |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Claude Skills collection | 4 | 4 | 0 | 0 | network-limited page snapshot |
| [OneWave-AI/claude-skills](https://github.com/OneWave-AI/claude-skills) | Claude Skills collection | 4 | 4 | 0 | 0 | network-limited page snapshot |
| [chriscox/agent-skills](https://github.com/chriscox/agent-skills) | Agent Skills | 2 | 2 | 0 | 0 | network-limited raw snapshot |
| [spencerpauly/awesome-cursor-skills](https://github.com/spencerpauly/awesome-cursor-skills) | Cursor Skills collection | 4 | 4 | 0 | 0 | network-limited raw snapshot |
| [tonynguyennvt/cursor-rules-awesome](https://github.com/tonynguyennvt/cursor-rules-awesome) | Cursor rules | 3 | 0 | 3 | 0 | installable npm package snapshot |
| [aurite-ai/agent-verifier](https://github.com/aurite-ai/agent-verifier) | Agent verification Skills | 5 | 5 | 0 | 0 | network-limited page snapshot |

Total sampled packages: 28

Full evaluated package catalog with source links, download links, and GitHub star counts: [Evaluated Skills Catalog](evaluated-skills-catalog.md). Chinese version: [被评测 Skill 清单](evaluated-skills-catalog.zh-CN.md).

Decision summary:

- Allow: 24
- Warn: 4
- Block: 0

## Representative Packages

Sampled packages included:

- `skill-creator`
- `mcp-builder`
- `pdf`
- `content-research-writer`
- `invoice-organizer`
- `googledrive-automation`
- `skill-security-auditor`
- `playwright-pro`
- `ms365-tenant-manager`
- `senior-architect`
- `agent-army`
- `code-review-pro`
- `compliance-checker`
- `incident-responder`
- `docs-sync`
- `project-planner`
- `auditing-security`
- `switching-projects`
- `saving-workspace-context`
- `visual-qa-testing`
- `cursor-rules-awesome` slices
- `agent-verifier` verification family

## What The Benchmark Shows

### 1. Popular Skills Are Often Safe, But Still Need Governance

Most sampled packages were not malicious and did not produce install-time blockers. SkillTrust still found concrete governance improvements:

- authoring split opportunities
- activation-token reduction opportunities
- policy overlays for high-impact actions
- explicit user-confirmation gates
- connector and OAuth scope constraints
- taxonomy and routing improvements

This supports SkillTrust's positioning as a trust and permission governance layer, not merely a malware scanner.

For before/after optimization metrics, selection-precision ranking, and charts, see [SkillTrust Value Proof](value-proof.md). Chinese version: [SkillTrust 价值证明](value-proof.zh-CN.md).

### 2. Deterministic Evidence Alone Is Not Enough

Several samples demonstrate why host-Agent semantic review is necessary.

Examples:

- `mcp-builder` produced a `warn` because reference/example code contained shell, environment, and path-like signals. A human or host Agent should read the full context and distinguish reference code from active Skill runtime behavior while preserving the evidence.
- `cursor-rules-awesome` contains security guidance examples mentioning cookies, keychains, `.env.example`, and route strings like `/users/{id}`. Deterministic scanning correctly surfaced risk-shaped language, but semantic review is needed to decide which findings are coding-standard examples rather than real permission requests.
- `skill-security-auditor` includes prompt-injection attack strings as examples to detect. These should be marked as untrusted examples, not interpreted as instructions to follow.

### 3. High-Impact Domains Need Intent-Bound Policy Even With Clean Static Findings

Some packages had no deterministic findings but still require semantic governance because their declared tasks are powerful.

Examples:

- `ms365-tenant-manager`: needs tenant scoping, dry-run defaults, role checks, and confirmation before Graph or PowerShell write actions.
- `incident-responder`: may need Bash, Edit, WebFetch, and WebSearch, but production-facing actions should be confirmation-gated.
- `agent-army`: multi-agent fan-out and continuous mode should have concurrency caps, file ownership boundaries, and approval thresholds.
- `googledrive-automation`: static files were clean, but runtime connector scope, OAuth grants, and destructive Drive actions need explicit policy.

### 4. High-Quality Packages Can Still Be More Installable

SkillTrust surfaced improvements even for high-scoring packages:

- `content-research-writer`: trusted, but monolithic; should split workflows and review rubrics into references.
- `skill-creator`: mostly trusted, but token-heavy; should defer examples and deep authoring heuristics.
- `docs-sync`: trusted, but should bind GitHub CLI, branch, commit, and document writes to a confirmed repository root.
- `visual-qa-testing`: browser, screenshots, console, and network inspection are task-critical, but navigation should stay local or user-authorized.
- `agent-verifier`: clean permission profile, but specialized `verify-*` Skills have taxonomy overlap.

## Product Improvements Discovered

This benchmark also revealed concrete SkillTrust roadmap items:

- parse Claude-style `tools:` frontmatter as requested permission surface
- detect multi-Agent fan-out and continuous orchestration as governance risks
- classify high-impact domains such as cloud tenant admin, compliance, incident response, production operations, browser automation, and connector management
- distinguish reference/example code from active runtime behavior while preserving evidence
- add connector allowlists and destructive-action confirmation gates
- improve taxonomy analysis for large `verify-*`, `*-automation`, or rule-family ecosystems

## Public Framing

Recommended framing:

> SkillTrust can audit popular AI Skill and rule ecosystems, distinguish deterministic evidence from semantic context, and recommend how to make even high-quality packages more intent-bound, token-efficient, and install-safe.

Avoid framing this benchmark as:

> These popular projects are dangerous.

The stronger and more accurate claim is:

> Popular AI Skills can be good and still need intent-bound permission governance before installation or use.

## Generated Local Artifacts

Detailed local reports were generated under `reports/benchmarks/`. Those reports are intentionally not committed because local audit artifacts can contain local paths and downloaded third-party snapshots.
