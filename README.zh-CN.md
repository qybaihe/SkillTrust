# SkillTrust

[English](README.md) · [安装](#安装) · [使用](#使用) · [输出](#输出)

![SkillTrust 封面](docs/assets/skilltrust-cover.png)

**面向 AI Skills 的意图绑定权限治理层。**

SkillTrust 可以把一个不可信的 AI Skill 包转换成：意图绑定、最小权限、可审计的治理包。

它不是只问：

> 这个 Skill 危不危险？

SkillTrust 问的是更适合安装前判断的问题：

> 这个 Skill 要完成它声称的任务，最少需要哪些权限？它实际暴露的行为是否超过了这个边界？

## 一图看懂

![SkillTrust 中文流程图](docs/assets/skilltrust-flow.zh-CN.png)

SkillTrust 结合两层判断：

- **确定性证据**：可复现 findings、文件证据、hash、权限面、数据流信号、信任评分、policy 和 audit receipt。
- **宿主 Agent 语义审查**：当前运行 SkillTrust 的 Agent 先全文阅读 Skill 核心文档，再判断这些权限和行为是否真的符合声明意图。

最终决策是保守的：

- deterministic findings 不会被删除
- likely false positive 可以被标注，但证据仍然保留
- critical sensitive-data-to-network flow 不能被语义审查洗成安全
- 最终安装决策始终是 `allow`、`warn` 或 `block`

## SkillTrust 是做什么的

SkillTrust 用来在使用或安装 Skill 前回答五个问题：

- 这个 Skill 声称要做什么？
- 完成这个任务真正需要哪些权限？
- 它实际暴露了哪些 filesystem、network、shell、environment、dependency、connector、prompt 或 data-flow 行为？
- 实际行为是否超出了声明意图？
- 如何把它收敛成更安全、可审计、可安装的 Skill？

它适合：

- 本地 Codex Skills 安全审计
- Skill registry / marketplace 审查
- 安装前权限门禁
- 企业内部审批流程
- 比赛与 demo 展示
- Skill 编写质量、token 效率和 taxonomy 优化

## 安装

### 一句话交给 AI Agent 安装

把下面这段提示词发给 Codex 或其他本地 coding Agent：

```text
请把 SkillTrust 从 https://github.com/qybaihe/SkillTrust 安装为本地 Codex Skill。将仓库 clone 或更新到 ~/.codex/skills/skilltrust，配置好本地 skilltrust 命令，并验证 skilltrust --help 可以运行。安装完成后，请立即运行一次只读的本地 Skill 组合审计：skilltrust audit-local --skills-root ~/.codex/skills --out ~/.codex/skills/skilltrust/reports/local-all。不要自动修改、重命名或修复任何现有本地 Skill，只生成报告、policy overlay 和需要用户审批的计划。最后请总结 allow/warn/block 数量、危险或越权 findings，以及下一步最安全的 remediation 建议。
```

这是推荐安装方式，因为 SkillTrust 本来就是给宿主 Agent 使用的。Agent 会完成安装、验证、本地 Skill 生态审计，并且在你明确批准之前不会改动任何真实 Skill。

### 安装后使用

对 Agent 说：

```text
请使用 SkillTrust 对我的本地 Codex Skills 做一次只读审计，告诉我哪些 Skill 可能越权、危险，或者值得优化。
```

## 使用

### 审计所有本地 Skills

```bash
skilltrust audit-local --skills-root ~/.codex/skills --out reports/local-all
```

用于检查整个本地 Skill 生态，生成 `allow`、`warn`、`block` 总览。

### 审计单个 Skill

```bash
skilltrust analyze ./path/to/skill --out reports/skill-audit
```

用于在信任、安装、发布或提交某个 Skill 前做权限治理审查。

### 安装前门禁

```bash
skilltrust install-check ./path/to/skill --out reports/install-check
```

用于获得直接的 `allow`、`warn` 或 `block` 安装决策。

### 生成可审查的修复包

```bash
skilltrust remediate ./path/to/skill --out reports/remediated
```

这个命令不会静默修改目标 Skill，而是生成 policy overlay、收敛后的权限清单、修复计划和可审查草稿。

### 加入宿主 Agent 语义审查

```bash
skilltrust analyze ./path/to/skill --agent-review-request --out reports/agent-review
```

然后宿主 Agent 会读取生成的语义审查请求，完整阅读列出的核心文档，写出 `semantic_review.json`，再和确定性证据融合：

```bash
skilltrust fuse reports/agent-review/analysis.json reports/agent-review/semantic_review.json --out reports/agent-review-fused
```

SkillTrust **不调用 OpenAI、Anthropic 或任何外部模型 API**，也**不需要 API Key**。语义审查者就是当前运行 SkillTrust 的宿主 Agent。

### 优化 Skill 质量

```bash
skilltrust authoring-audit ./path/to/skill --out reports/authoring
skilltrust token-optimize ./path/to/skill --out reports/token
skilltrust taxonomy-audit --skills-root ~/.codex/skills --out reports/taxonomy
```

用于优化 Skill 结构、减少 activation token 浪费，或者修复 Skill 命名和触发描述的歧义。

## 输出

SkillTrust 可以生成：

- `permission_manifest.json`：根据声明意图推断的最小权限模型
- `skilltrust-policy.json`：filesystem、network、environment、shell、connector、dependency、prompt 和 semantic 约束策略
- `trust_report.md`：确定性审计报告
- `fused_trust_report.md`：融合宿主 Agent 语义审查后的报告
- `audit_receipt.json`：包含 hash 和规则版本的可复现审计凭证
- `remediation_plan.md`：把 Skill 收敛到最小权限的具体建议
- `install_decision.json`：安装前 `allow`、`warn` 或 `block`
- `local_skills_report.md`：本地 Skill 组合审计总览
- `authoring_report.md`：Skill harness 和 references 拆分建议
- `token_efficiency_report.md`：token 浪费和 scriptification 优化机会
- `skill_taxonomy_report.md`：命名、description 和路由歧义 findings

## Trust Fit Score

SkillTrust 使用 0 到 100 分：

| 分数 | 等级 |
| ---: | --- |
| 85-100 | Trusted |
| 70-84 | Mostly Trusted |
| 50-69 | Needs Review |
| 30-49 | Overprivileged |
| 0-29 | Critical Risk |

评分会考虑声明意图清晰度、权限必要性、越权程度、敏感面、数据流安全、安装时风险、prompt integrity、可执行性和可审计性。

## 安全边界

- 默认进行静态分析。
- 不执行目标 Skill。
- 不调用外部模型 API。
- 不需要 API Key。
- semantic fusion 会保留 deterministic evidence。
- 对本地 Skill 的修复、重命名和描述更新默认只生成审批计划。
- 本地审计报告可能包含本地路径或私有 evidence，不建议直接公开。

## Demo Fixtures

| Fixture | 声明意图 | 分数 | 风险等级 | 安装门禁 |
| --- | --- | ---: | --- | --- |
| `fixtures/benign-pdf-skill` | PDF summarization | 100 | Trusted | allow |
| `fixtures/overprivileged-research-skill` | Research/reporting | 45 | Overprivileged | warn |
| `fixtures/malicious-like-writing-skill` | Writing assistant | 25 | Critical Risk | block |

这些 fixtures 展示了低风险 Skill、初衷合理但权限过大的 Skill，以及存在敏感数据流的 malicious-like Skill。

## 核心叙事

SkillTrust 不是关键词 scanner，而是 AI Skills 的安装前信任治理层：

> SkillTrust combines reproducible evidence with host-Agent semantic permission reasoning to make AI Skills installable with intent-bound trust.
