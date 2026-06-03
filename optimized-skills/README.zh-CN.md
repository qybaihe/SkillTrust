# SkillTrust 优化版 Skill 包

日期：2026-06-03

英文版：[SkillTrust Optimized Skill Pack](README.md)。

这个目录包含 28 个由 SkillTrust 生成的优化版 Skill preview packages，来源于公开 benchmark 样本。它们展示了 SkillTrust 在审计热门 AI Skills、Cursor rules 和 reusable Agent instructions 后可以产出的东西：intent-bound permissions、token-efficient activation、更精准的触发边界，以及可审查的 policy overlays。

这些不是上游官方版本，而是 SkillTrust 生成的 preview packages，用来测试和展示优化能力。

## 包含什么

每个 package 包含：

- `SKILL.md`：精简后的优化版 Skill harness
- `skilltrust/permission_manifest.json`：最小权限 manifest
- `skilltrust/skilltrust-policy.json`：runtime policy overlay
- `skilltrust/optimization_summary.md`：来源、优化点、token plan 和 selection-precision plan

## 怎么测试

把下面这段话发给任意本地 Agent：

```text
请克隆 https://github.com/qybaihe/SkillTrust，打开 optimized-skills 目录，选择一个 SkillTrust 优化版 preview package，先阅读它的 SKILL.md 和 skilltrust policy 文件，然后用一个小型安全测试任务试用它。除非 package 明确向我请求确认，否则所有动作都保持在当前 workspace 内。
```

## 自审结果

SkillTrust 在生成后审计了这个优化包：

- 扫描 28 个优化版 preview packages
- 26 allow
- 2 warn
- 0 block
- 0 个 authoring needs split
- 0 个 token-heavy Skills

剩下的 2 个 warn 是刻意保守的 Cursor security/rules preview，仍需要 semantic review 和 policy approval。

## Package Index

| # | 优化版 Package | 原始样本 | 来源 | Stars | 原始 Gate | 优化后姿态 | 目录 |
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

## 公开说明

- 这些 packages 由 SkillTrust 生成，不是上游 maintainers 官方发布。
- 它们不会修改第三方项目。
- 它们避免大段复制上游 instruction，而是提供 compact optimized harness 和 policy overlays。
- 在正式使用前，请先审查上游 license 和生成的 policy。
- `warn` 不代表 malicious，而是表示 package 在使用前需要 review、scoping、semantic clarification 或 policy overlay。
