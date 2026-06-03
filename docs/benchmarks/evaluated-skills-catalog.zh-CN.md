# 被评测 Skill 清单

日期：2026-06-03

英文版：[Evaluated Skills Catalog](evaluated-skills-catalog.md)。

这份清单列出了 SkillTrust benchmark 中使用的公开 Skill、rules 和 reusable-agent-instruction packages。它的作用是让评测范围更透明、更可复现，也更有公信力。

GitHub Stars 通过 GitHub API 在 2026-06-03 查询。Stars 是当时的流行度信号，会随时间变化。

## 按 Stars 排序的来源仓库

| 排名 | 来源 | Stars | Forks | 这是什么 | 样本数 | 下载 |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 1 | [anthropics/skills](https://github.com/anthropics/skills) | 145,914 | 17,194 | Anthropic 公开 Agent Skills 仓库 | 3 | [ZIP](https://github.com/anthropics/skills/archive/refs/heads/main.zip) |
| 2 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 63,040 | 6,924 | Claude Skills、resources 和 workflow tools 集合 | 3 | [ZIP](https://github.com/ComposioHQ/awesome-claude-skills/archive/refs/heads/master.zip) |
| 3 | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 17,004 | 2,329 | 面向 Claude Code、Codex、Gemini CLI、Cursor 等 Agent 的大型 skill/plugin 集合 | 4 | [ZIP](https://github.com/alirezarezvani/claude-skills/archive/refs/heads/main.zip) |
| 4 | [spencerpauly/awesome-cursor-skills](https://github.com/spencerpauly/awesome-cursor-skills) | 367 | 60 | Cursor skills 和 workflows 集合 | 4 | [ZIP](https://github.com/spencerpauly/awesome-cursor-skills/archive/refs/heads/main.zip) |
| 5 | [OneWave-AI/claude-skills](https://github.com/OneWave-AI/claude-skills) | 169 | 24 | Production-ready Claude Code Skills 集合 | 4 | [ZIP](https://github.com/OneWave-AI/claude-skills/archive/refs/heads/main.zip) |
| 6 | [Aurite-ai/agent-verifier](https://github.com/Aurite-ai/agent-verifier) | 39 | 5 | 面向代码质量、安全、模式和语言检查的 Agent verification Skill family | 5 | [ZIP](https://github.com/Aurite-ai/agent-verifier/archive/refs/heads/main.zip) |
| 7 | [chriscox/agent-skills](https://github.com/chriscox/agent-skills) | 10 | 2 | 可复用 AI coding agent skills，支持 Claude Code、Codex、Gemini CLI、OpenClaw 等 | 2 | [ZIP](https://github.com/chriscox/agent-skills/archive/refs/heads/main.zip) |
| 8 | [tonynguyennvt/cursor-rules-awesome](https://github.com/tonynguyennvt/cursor-rules-awesome) | 4 | 2 | 综合 Cursor rules package，也以 npm package 分发 | 3 | [ZIP](https://github.com/tonynguyennvt/cursor-rules-awesome/archive/refs/heads/master.zip)，[npm](https://www.npmjs.com/package/cursor-rules-awesome) |

## 具体评测 Package 清单

| # | Package / Skill | 来源 | Stars | 这个 Skill 是什么 | SkillTrust Gate | 来源 / 下载 |
| ---: | --- | --- | ---: | --- | --- | --- |
| 1 | `skill-creator` | `anthropics/skills` | 145,914 | 创建、验证和打包 Agent Skills 的 Skill | allow | [source](https://github.com/anthropics/skills/tree/main/skills/skill-creator) |
| 2 | `mcp-builder` | `anthropics/skills` | 145,914 | 构建 MCP servers 和参考实现的 Skill | warn | [source](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) |
| 3 | `pdf` | `anthropics/skills` | 145,914 | PDF 阅读、表单和文档处理 Skill | allow | [source](https://github.com/anthropics/skills/tree/main/skills/pdf) |
| 4 | `content-research-writer` | `ComposioHQ/awesome-claude-skills` | 63,040 | research + long-form writing workflow | allow | [source](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/content-research-writer) |
| 5 | `invoice-organizer` | `ComposioHQ/awesome-claude-skills` | 63,040 | invoice 文档整理和信息抽取 Skill | allow | [source](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/invoice-organizer) |
| 6 | `googledrive-automation` | `ComposioHQ/awesome-claude-skills` | 63,040 | 通过 connector / tool integration 做 Google Drive automation | allow | [source](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/composio-skills/googledrive-automation) |
| 7 | `skill-security-auditor` | `alirezarezvani/claude-skills` | 17,004 | 审计 Skill 安全问题和 prompt-injection patterns | allow | [source](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/skill-security-auditor) |
| 8 | `playwright-pro` | `alirezarezvani/claude-skills` | 17,004 | Playwright 测试和 browser automation skill pack | allow | [source](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/playwright-pro) |
| 9 | `ms365-tenant-manager` | `alirezarezvani/claude-skills` | 17,004 | Microsoft 365 tenant administration workflow | allow | [source](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/ms365-tenant-manager) |
| 10 | `senior-architect` | `alirezarezvani/claude-skills` | 17,004 | 架构分析和系统设计指导 Skill | allow | [source](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/senior-architect) |
| 11 | `agent-army` | `OneWave-AI/claude-skills` | 169 | multi-agent orchestration 和并行执行 workflow | allow | [source](https://github.com/OneWave-AI/claude-skills/tree/main/agent-army) |
| 12 | `code-review-pro` | `OneWave-AI/claude-skills` | 169 | 专业 code review workflow | allow | [source](https://github.com/OneWave-AI/claude-skills/tree/main/code-review-pro) |
| 13 | `compliance-checker` | `OneWave-AI/claude-skills` | 169 | 合规审查、证据整理和报告生成 workflow | allow | [source](https://github.com/OneWave-AI/claude-skills/tree/main/compliance-checker) |
| 14 | `incident-responder` | `OneWave-AI/claude-skills` | 169 | incident response 和 operational investigation workflow | allow | [source](https://github.com/OneWave-AI/claude-skills/tree/main/incident-responder) |
| 15 | `docs-sync` | `chriscox/agent-skills` | 10 | 文档同步和 repo-aware 文档更新 Skill | allow | [source](https://github.com/chriscox/agent-skills/tree/main/skills/docs-sync) |
| 16 | `project-planner` | `chriscox/agent-skills` | 10 | 项目规划、proposal、issue 和 branch workflow | allow | [source](https://github.com/chriscox/agent-skills/tree/main/skills/project-planner) |
| 17 | `auditing-security` | `spencerpauly/awesome-cursor-skills` | 367 | 面向 codebase 和 dependencies 的 security-audit workflow | allow | [source](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/auditing-security) |
| 18 | `switching-projects` | `spencerpauly/awesome-cursor-skills` | 367 | Cursor workspace / project switching workflow | allow | [source](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/switching-projects) |
| 19 | `saving-workspace-context` | `spencerpauly/awesome-cursor-skills` | 367 | 保存和恢复 workspace memory / context | allow | [source](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/saving-workspace-context) |
| 20 | `visual-qa-testing` | `spencerpauly/awesome-cursor-skills` | 367 | 使用 browser、screenshots、console 和 network inspection 的 visual QA workflow | allow | [source](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/visual-qa-testing) |
| 21 | `cursor-rules-awesome / monolithic-rules` | `tonynguyennvt/cursor-rules-awesome` | 4 | 覆盖大量领域和框架的完整 `.cursorrules` 规则库 | warn | [source](https://github.com/tonynguyennvt/cursor-rules-awesome/blob/master/.cursorrules)，[npm](https://www.npmjs.com/package/cursor-rules-awesome) |
| 22 | `cursor-rules-awesome / installer-package` | `tonynguyennvt/cursor-rules-awesome` | 4 | npm installer 和写入 `.cursorrules` 的 CLI | warn | [source](https://github.com/tonynguyennvt/cursor-rules-awesome/tree/master/bin)，[npm](https://www.npmjs.com/package/cursor-rules-awesome) |
| 23 | `cursor-rules-awesome / security-compliance-slice` | `tonynguyennvt/cursor-rules-awesome` | 4 | security、privacy、compliance、production-ops rules excerpts | warn | [source](https://github.com/tonynguyennvt/cursor-rules-awesome/blob/master/.cursorrules)，[npm](https://www.npmjs.com/package/cursor-rules-awesome) |
| 24 | `verification` | `Aurite-ai/agent-verifier` | 39 | 多维 verification orchestrator | allow | [source](https://github.com/Aurite-ai/agent-verifier/tree/main/skills/verification) |
| 25 | `verify-security` | `Aurite-ai/agent-verifier` | 39 | security 和 compliance verification | allow | [source](https://github.com/Aurite-ai/agent-verifier/tree/main/skills/verify-security) |
| 26 | `verify-patterns` | `Aurite-ai/agent-verifier` | 39 | pattern 和 consistency verification | allow | [source](https://github.com/Aurite-ai/agent-verifier/tree/main/skills/verify-patterns) |
| 27 | `verify-quality` | `Aurite-ai/agent-verifier` | 39 | quality 和 readiness verification | allow | [source](https://github.com/Aurite-ai/agent-verifier/tree/main/skills/verify-quality) |
| 28 | `verify-language` | `Aurite-ai/agent-verifier` | 39 | language、ambiguity 和 wording verification | allow | [source](https://github.com/Aurite-ai/agent-verifier/tree/main/skills/verify-language) |

## 为什么这份清单重要

这次 benchmark 同时覆盖了超高 star 仓库和较小但专业的新兴 Skill 生态：

- 高 star 来源证明 SkillTrust 不是只测 toy fixtures，而是在审计真实公开 Skill 生态。
- 小型专业来源证明 SkillTrust 也能处理较新的 Agent package formats、Cursor rules、npm-distributed rule packs 和 verification Skill families。
- 混合结果比“恐吓式 benchmark”更可信：大部分 package 可以安装，但很多仍有 token efficiency、policy precision、taxonomy 和 semantic review 优化空间。

## 范围说明

- SkillTrust 没有修改任何第三方项目。
- 部分目标因为本地 clone / ZIP 网络访问不稳定，采用了 `network-limited` 审计。
- `cursor-rules-awesome` 样本来自可安装 npm package snapshot 和公开仓库 metadata。
- Stars 和仓库 metadata 查询于 2026-06-03，之后可能变化。
- `warn` 不代表 malicious。它表示 package 在使用前需要 review、scoping、semantic clarification 或 policy overlay。
