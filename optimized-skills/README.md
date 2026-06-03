# SkillTrust Optimized Skill Pack

Date: 2026-06-03

Chinese version: [优化版 Skill 包](README.zh-CN.md).

This folder contains 28 SkillTrust-optimized preview packages generated from the public benchmark sample. They show what SkillTrust can produce after auditing popular AI Skills, Cursor rules, and reusable Agent instructions: intent-bound permissions, token-efficient activation, sharper selection triggers, and reviewable policy overlays.

These are not official upstream releases. They are generated preview packages for testing SkillTrust's optimization approach.

## What Is Included

Each package includes:

- `SKILL.md`: compact optimized Skill harness
- `skilltrust/permission_manifest.json`: least-privilege permission manifest
- `skilltrust/skilltrust-policy.json`: runtime policy overlay
- `skilltrust/optimization_summary.md`: source, changes, token plan, and selection-precision plan

## How To Test

Paste this into any local Agent:

```text
Clone https://github.com/qybaihe/SkillTrust, open the optimized-skills directory, choose one SkillTrust-optimized preview package, read its SKILL.md and skilltrust policy files, then use it on a small safe test task. Keep all actions inside the current workspace unless the package explicitly asks me for confirmation.
```

## Self-Audit Result

SkillTrust audited this optimized pack after generation:

- 28 optimized preview packages scanned
- 26 allow
- 2 warn
- 0 block
- 0 authoring needs split
- 0 token-heavy Skills

The two remaining warn packages are intentionally conservative Cursor security/rules previews that still require semantic review and policy approval.

## Package Index

| # | Optimized Package | Original Sample | Source | Stars | Original Gate | Optimized Posture | Folder |
| ---: | --- | --- | --- | ---: | --- | --- | --- |
| 1 | `agent-army` | `agent-army` | `OneWave-AI/claude-skills` | 169 | allow | allow-with-policy | [folder](agent-army/) |
| 2 | `auditing-security` | `auditing-security` | `spencerpauly/awesome-cursor-skills` | 367 | allow | allow-with-policy | [folder](auditing-security/) |
| 3 | `code-review-pro` | `code-review-pro` | `OneWave-AI/claude-skills` | 169 | allow | allow-with-policy | [folder](code-review-pro/) |
| 4 | `compliance-checker` | `compliance-checker` | `OneWave-AI/claude-skills` | 169 | allow | allow-with-policy | [folder](compliance-checker/) |
| 5 | `content-research-writer` | `content-research-writer` | `ComposioHQ/awesome-claude-skills` | 63,040 | allow | allow-with-policy | [folder](content-research-writer/) |
| 6 | `cursor-rules-installer` | `cursor-rules-awesome / installer-package` | `tonynguyennvt/cursor-rules-awesome` | 4 | warn | warn-until-semantic-review-and-policy-approval | [folder](cursor-rules-installer/) |
| 7 | `cursor-rules-router` | `cursor-rules-awesome / monolithic-rules` | `tonynguyennvt/cursor-rules-awesome` | 4 | warn | warn-until-semantic-review-and-policy-approval | [folder](cursor-rules-router/) |
| 8 | `cursor-rules-security-compliance` | `cursor-rules-awesome / security-compliance-slice` | `tonynguyennvt/cursor-rules-awesome` | 4 | warn | warn-until-semantic-review-and-policy-approval | [folder](cursor-rules-security-compliance/) |
| 9 | `docs-sync` | `docs-sync` | `chriscox/agent-skills` | 10 | allow | allow-with-policy | [folder](docs-sync/) |
| 10 | `googledrive-automation` | `googledrive-automation` | `ComposioHQ/awesome-claude-skills` | 63,040 | allow | allow-with-policy | [folder](googledrive-automation/) |
| 11 | `incident-responder` | `incident-responder` | `OneWave-AI/claude-skills` | 169 | allow | allow-with-policy | [folder](incident-responder/) |
| 12 | `invoice-organizer` | `invoice-organizer` | `ComposioHQ/awesome-claude-skills` | 63,040 | allow | allow-with-policy | [folder](invoice-organizer/) |
| 13 | `mcp-builder` | `mcp-builder` | `anthropics/skills` | 145,914 | warn | warn-until-semantic-review-and-policy-approval | [folder](mcp-builder/) |
| 14 | `ms365-tenant-manager` | `ms365-tenant-manager` | `alirezarezvani/claude-skills` | 17,004 | allow | allow-with-policy | [folder](ms365-tenant-manager/) |
| 15 | `pdf` | `pdf` | `anthropics/skills` | 145,914 | allow | allow-with-policy | [folder](pdf/) |
| 16 | `playwright-pro` | `playwright-pro` | `alirezarezvani/claude-skills` | 17,004 | allow | allow-with-policy | [folder](playwright-pro/) |
| 17 | `project-planner` | `project-planner` | `chriscox/agent-skills` | 10 | allow | allow-with-policy | [folder](project-planner/) |
| 18 | `saving-workspace-context` | `saving-workspace-context` | `spencerpauly/awesome-cursor-skills` | 367 | allow | allow-with-policy | [folder](saving-workspace-context/) |
| 19 | `senior-architect` | `senior-architect` | `alirezarezvani/claude-skills` | 17,004 | allow | allow-with-policy | [folder](senior-architect/) |
| 20 | `skill-creator` | `skill-creator` | `anthropics/skills` | 145,914 | allow | allow-with-policy | [folder](skill-creator/) |
| 21 | `skill-security-auditor` | `skill-security-auditor` | `alirezarezvani/claude-skills` | 17,004 | allow | allow-with-policy | [folder](skill-security-auditor/) |
| 22 | `switching-projects` | `switching-projects` | `spencerpauly/awesome-cursor-skills` | 367 | allow | allow-with-policy | [folder](switching-projects/) |
| 23 | `verification` | `verification` | `Aurite-ai/agent-verifier` | 39 | allow | allow-with-policy | [folder](verification/) |
| 24 | `verify-language` | `verify-language` | `Aurite-ai/agent-verifier` | 39 | allow | allow-with-policy | [folder](verify-language/) |
| 25 | `verify-patterns` | `verify-patterns` | `Aurite-ai/agent-verifier` | 39 | allow | allow-with-policy | [folder](verify-patterns/) |
| 26 | `verify-quality` | `verify-quality` | `Aurite-ai/agent-verifier` | 39 | allow | allow-with-policy | [folder](verify-quality/) |
| 27 | `verify-security` | `verify-security` | `Aurite-ai/agent-verifier` | 39 | allow | allow-with-policy | [folder](verify-security/) |
| 28 | `visual-qa-testing` | `visual-qa-testing` | `spencerpauly/awesome-cursor-skills` | 367 | allow | allow-with-policy | [folder](visual-qa-testing/) |

## Public Caveats

- These packages are generated by SkillTrust, not by the upstream maintainers.
- They do not modify third-party projects.
- They avoid copying long upstream instructions and instead provide compact optimized harnesses plus policy overlays.
- Use them as preview/demo packages unless you have reviewed the upstream project license and the generated policy.
- `warn` does not mean malicious; it means review, scoping, semantic clarification, or policy overlay is needed.
