# SkillTrust Value Proof

Date: 2026-06-03

This page turns the public benchmark into a value proof: SkillTrust does not only decide `allow`, `warn`, or `block`. It also generates an optimization plan that can make AI Skill packages more compact, more intent-bound, and easier for Agents to select precisely.

Chinese version: [SkillTrust 价值证明](value-proof.zh-CN.md).

Optimized preview package: [optimized-skills](../../optimized-skills/).

The numbers below come from the preliminary static benchmark of 28 representative public AI Skill, Claude Skill, Cursor rule, and Agent instruction packages. Several targets were audited in `network-limited` mode, so the results are best read as a representative sample rather than a full supply-chain audit.

## Evaluation Dimensions

SkillTrust evaluates value across seven dimensions:

| Dimension | What It Measures | Why It Matters |
| --- | --- | --- |
| Install safety | `allow`, `warn`, or `block` | Shows whether a package can be installed or needs review. |
| Activation efficiency | Always-loaded instruction tokens that can move to references, scripts, schemas, validators, or config | Reduces context load and makes Skills easier to activate precisely. |
| Harness structure | Whether `SKILL.md` is a compact trigger harness or a monolithic manual | Improves Agent activation and reduces irrelevant context. |
| Policy precision | Connector scopes, workspace binding, user-confirmation gates, destructive-action gates | Converts broad capability into intent-bound permission governance. |
| Semantic precision | Whether AI full-document reading can distinguish true risk from examples or reference code | Reduces noisy scanner results while preserving evidence. |
| Taxonomy accuracy | Naming and description overlap across related Skills | Helps the Agent select the right package. |
| Selection precision / rankability | Positive triggers, negative triggers, scope-bound activation signals, and specialization boundaries | Helps the right optimized Skill rank above generic or overlapping packages. |

## Governance Coverage

![SkillTrust governance coverage](../assets/value-proof-governance.svg)

In a 28-package public sample, SkillTrust mostly validated popular packages as installable while still finding optimization work:

- 24 packages were `allow`
- 4 packages were `warn`
- 0 packages were `block`
- 20 packages had token-saving opportunities
- 17 reference extraction candidates were found
- 26 scriptification candidates were found
- 9 taxonomy findings were found

This is the core value proof: safe packages can still become more precise, more compact, and more governable.

## Activation Token Reduction

![SkillTrust token reduction](../assets/value-proof-token-reduction.svg)

Across the 28 sampled packages:

- Before optimization plan: 30,699 estimated activation-body tokens
- Estimated tokens moved out of always-loaded instructions: 6,832
- After SkillTrust first-pass plan: 23,867 estimated activation-body tokens
- Estimated reduction: 22.3%

This is an activation-context estimate, not a production billing benchmark. The value is that SkillTrust identifies what can move out of always-loaded instructions and into deferred references, scripts, schemas, validators, or config.

## Optimization Surface

![SkillTrust optimization surface](../assets/value-proof-optimization-surface.svg)

The benchmark found multiple improvement surfaces:

- authoring findings
- scriptification candidates
- reference extraction candidates
- taxonomy findings
- approval-plan items
- install-time warn decisions

This demonstrates that SkillTrust is a governance layer, not just a scanner. It can validate safe packages and still produce concrete plans to make them safer and leaner.

## Selection Precision Ranking

![SkillTrust selection precision](../assets/value-proof-selection-precision.svg)

SkillTrust also ranks which packages are likely to gain the most selection precision after optimization. This is not a claim of measured production accuracy. It is a reviewable rankability signal based on taxonomy findings, trigger overlap, monolithic always-on context, missing negative triggers, and missing scope boundaries.

| Rank | Package / Portfolio | Baseline Selection Problem | SkillTrust Optimization Plan | Projected Selection Effect |
| ---: | --- | --- | --- | --- |
| 1 | `agent-verifier` | Clean permission profile, but `verify-*` Skills overlap heavily; taxonomy score was `0` in the sampled portfolio | Keep `verification` as orchestrator; sharpen `verify-security`, `verify-quality`, `verify-patterns`, and `verify-language` descriptions with positive and negative triggers | Target overlap findings drop from `6` to `0`; projected taxonomy score target is `80+` after re-audit |
| 2 | `cursor-rules-awesome` | A 4,861-line monolithic rules file makes many unrelated domains compete in the same activation context | Replace the blanket rules file with a short router plus domain references for security, backend, frontend, SRE, compliance, mobile, data, and API | Task-specific rules can rank above generic all-purpose rules; projected taxonomy score target is `100` |
| 3 | `project-planner` | Planning, GitHub issue creation, GraphQL sub-issues, branch creation, and push behavior can blur into general GitHub automation | Add repo-root binding and explicit confirmation gates for GitHub mutations | The planner remains a planning Skill instead of becoming a broad repository automation Skill |
| 4 | `skill-creator` | Broad authoring and evaluation guidance creates a token-heavy activation body | Move deep evaluation guidance into references, schemas, and command wrappers | The Skill becomes easier to trigger only when creating, updating, or validating Skills |
| 5 | `content-research-writer` | Trusted but monolithic research workflow can mix research, writing, and connector behavior | Split rubrics/workflows into references and clarify connector scope | The host Agent can distinguish research-writing intent from drive/document automation intent |

The ranking is useful for demos because it shows a second kind of product value: SkillTrust can recommend where optimization will most improve Agent behavior, not just where security risk exists.

## Representative Before / After Cases

| Package | Baseline | SkillTrust Optimization Plan | Value Signal |
| --- | --- | --- | --- |
| `skill-creator` | 8,156 activation-body tokens, token-heavy, mostly trusted | First-pass plan saves 1,346 tokens; compact preview target saves 6,156 tokens | Shows large token reduction from references, schemas, and command wrappers. |
| `content-research-writer` | Trusted but monolithic | First-pass plan saves 1,215 tokens and splits workflows/rubrics into references | Shows that high-trust Skills can still be made easier to activate. |
| `project-planner` | `allow`, 96/100 trust score | Adds user confirmation gates for GitHub issue creation, GraphQL sub-issues, branch creation, and push behavior | Shows policy precision beyond pass/fail. |
| `cursor-rules-awesome` | 4,861-line monolithic rules file, `warn` | Router plus references can load only relevant slices; estimated context reduction is 95.8%-98.6% for task-specific use | Shows dramatic context reduction and semantic false-positive handling. |
| `agent-verifier` | Clean permission profile | Taxonomy fixes and about 896 estimated activation tokens saved | Shows that `allow` packages can still improve selection accuracy and efficiency. |

## What Changed After SkillTrust

| Before | After SkillTrust Plan |
| --- | --- |
| A package gets a simple pass/fail-style review | The package gets an install decision plus manifest, policy, receipt, report, and remediation plan |
| Long instruction files stay always loaded | Details move to references, schemas, validators, scripts, or config |
| Broad tools are accepted as implicit authority | High-impact actions get workspace binding, connector scope, and user confirmation gates |
| Scanner findings can be noisy | Host-Agent full-document review can mark likely false positives while preserving evidence |
| Similar Skills can overlap in triggers | Taxonomy plans propose clearer names and descriptions pending user approval |
| Multiple Skills compete for the same user request | Selection precision ranking identifies which optimized Skills need sharper triggers, anti-triggers, and scope boundaries |

## Public Caveats

- This benchmark is preliminary and static-only.
- Some repositories were audited from network-limited raw/page/package snapshots because full clone access was unreliable.
- SkillTrust did not modify third-party projects.
- Estimated token savings are optimization-plan estimates, not measured production billing savings.
- Selection precision ranking is a projected rankability signal, not an end-to-end production accuracy benchmark.
- `warn` does not mean malicious. It means review, scoping, semantic clarification, or policy overlay is needed before use.

## Summary

The benchmark supports a stronger claim than "SkillTrust can find risky packages":

> SkillTrust can turn popular AI Skill packages into more intent-bound, token-efficient, policy-constrained, and selection-accurate packages before installation or use.
