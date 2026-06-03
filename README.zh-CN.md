# SkillTrust

[English](README.md) · [安装部署](#安装部署) · [快速开始](#快速开始) · [Host-Agent 语义审查](#host-agent-语义审查)

![SkillTrust 封面](docs/assets/skilltrust-cover.png)

**面向 AI Skills 的意图绑定权限治理层。**

它可以把一个不可信的 Skill 包转换成：最小权限清单、安装前策略覆盖、审计凭证、可信报告和保守的安装决策。

它不是简单的关键词扫描器，而是回答一个更关键的问题：

> 这个 Skill 要完成它声称的任务，最少需要哪些权限？它实际触达的行为是否超出了这个意图边界？

## 一图看懂

![SkillTrust 中文流程图](docs/assets/skilltrust-flow.zh-CN.png)

SkillTrust 不是普通安全扫描器，而是一条安装前权限治理链路：

- 把 Skill 包当作不可信 evidence 来读取。
- 用确定性扫描提取声明意图、实际行为、行号、hash 和 findings。
- 让宿主 Agent 先全文阅读核心文档，再给出语义权限判断。
- 用保守融合层合并两类证据，并保持 deterministic evidence 的权威性。
- 最终输出可用于 `allow`、`warn` 或 `block` 的最小权限治理包。

主要输出：

```text
permission_manifest.json
skilltrust-policy.json
trust_report.md / fused_trust_report.md
audit_receipt.json
remediation_plan.md
install_decision.json / fused_install_decision.json
```

## 为什么需要 SkillTrust

AI Skills 正在变成可复用的操作单元：浏览器流程、Gmail 助手、调研 Agent、PDF 总结器、表单填写器、文档生成器和本地自动化工具。

这个生态不能只靠“危险关键词”判断风险：

- `curl` 对调研 Skill 可能合理，但对 PDF 总结 Skill 就不一定合理。
- 浏览器权限对表单填写可能必要，但对本地文档格式化不必要。
- 调研 Skill 可以需要公开网页访问，但不应该读取 `.env`、SSH key、浏览器 cookies 或无关 telemetry endpoint。
- 写作助手如果读取 token 并发送到 webhook，即使 README 写得很正常，也应该被拦截。

SkillTrust 提供的是缺失的安装前信任层：**意图绑定、最小权限、可审计的权限治理**。

## 架构

SkillTrust 结合了确定性证据采集和宿主 Agent 语义审查。它**不调用 OpenAI、Anthropic 或任何外部模型 API**，也**不需要 API Key**。

1. **Deterministic scanner**

   Python 负责采集可复现证据：声明意图、推断所需权限、观察到的权限、文件/行号 findings、hash、基础分数、policy、manifest 和 receipt。

2. **Host-Agent semantic review**

   当前运行 SkillTrust 的 Agent 读取 `semantic_review_request.json` 和 `semantic_review_instructions.md`，先完整阅读列出的 `SKILL.md` / README 核心文档，再写出 `semantic_review.json`。

3. **Conservative fusion layer**

   Python 融合 `analysis.json` 和 `semantic_review.json`，保留所有确定性证据，加入语义标签和策略优化，最后输出保守的 allow/warn/block 安装决策。

## 核心能力

- **Intent vs behavior 分析**：比较 Skill 声称要做什么，以及实际文件触达了什么。
- **最小权限推断**：把声明意图转换成 filesystem、network、shell、connector、dependency、prompt 等权限边界。
- **权限越界检测**：识别“初衷合理但权限过大”的 Skill。
- **宿主 Agent 语义审查**：让当前 Agent 先全文读核心文档，再审查 findings，不需要任何 API Key。
- **保守融合**：语义审查可以标注 findings，但不能删除证据，也不能覆盖 critical data-flow block。
- **安装前门禁**：输出 `allow`、`warn` 或 `block`。
- **策略覆盖**：生成 `skilltrust-policy.json`，包含 filesystem、network、environment、shell、connector、dependency、prompt 和 semantic refinements。
- **可复现审计凭证**：记录文件 hash、规则版本、结果 hash 和证据 hash。
- **Skill authoring optimizer**：检查 `SKILL.md` 是否应该拆成 compact harness + `references/`。
- **Token efficiency optimizer**：识别哪些 instruction 应该变成 scripts/config/schema/validator。
- **Skill taxonomy optimizer**：检查 Skill 命名、description overlap 和路由冲突。

## 安装部署

### 环境要求

- Python 3.10+
- Git
- 可选：如果要重新渲染 Excalidraw 流程图，需要 Node.js

SkillTrust 不依赖 OpenAI、Anthropic 或外部 LLM SDK。

### 克隆仓库

```bash
git clone https://github.com/qybaihe/SkillTrust.git
cd SkillTrust
```

### 直接运行

```bash
python -m skilltrust --help
python -m skilltrust analyze fixtures/overprivileged-research-skill
```

### 安装 CLI

```bash
python -m pip install -e .
skilltrust --help
skilltrust analyze fixtures/overprivileged-research-skill
```

### 作为本地 Codex Skill 安装

如果希望宿主 Agent 能把 SkillTrust 当成本地 Skill 使用，可以克隆到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/qybaihe/SkillTrust.git ~/.codex/skills/skilltrust
cd ~/.codex/skills/skilltrust
python -m pip install -e .
```

之后可以让 Agent 使用 `SkillTrust` 审计某个 Skill 包。根目录的 `SKILL.md` 里写了完整工作流。

## 快速开始

运行主 demo fixture：

```bash
skilltrust analyze fixtures/overprivileged-research-skill --out reports/demo-overprivileged
```

预期结果：

```text
SkillTrust score: 45/100 (Overprivileged)
Declared intent: research, document generation
Findings: 5
```

生成文件：

```text
reports/demo-overprivileged/
  analysis.json
  trust_report.md
  permission_manifest.json
  skilltrust-policy.json
  audit_receipt.json
  remediation_plan.md
```

## Host-Agent 语义审查

SkillTrust 的语义审查不调用模型 API。它会给“当前正在运行 SkillTrust 的 Agent”准备一个本地 evidence bundle。

生成语义审查请求：

```bash
skilltrust analyze fixtures/overprivileged-research-skill \
  --agent-review-request \
  --out reports/demo-agent-overprivileged
```

这会生成：

```text
reports/demo-agent-overprivileged/
  analysis.json
  semantic_review_request.json
  semantic_review_instructions.md
```

宿主 Agent 接下来应该：

- 读取 `semantic_review_request.json`
- 读取 `semantic_review_instructions.md`
- 完整阅读 `core_documents_to_read` 中列出的每个文件
- 逐条评估 deterministic findings
- 写出 `semantic_review.json`

为了离线 demo 和测试，可以用 SkillTrust 生成一个 draft review，不调用任何 API：

```bash
skilltrust draft-semantic-review \
  reports/demo-agent-overprivileged/semantic_review_request.json \
  --out reports/demo-agent-overprivileged/semantic_review.json
```

融合 deterministic evidence 和 semantic review：

```bash
skilltrust fuse \
  reports/demo-agent-overprivileged/analysis.json \
  reports/demo-agent-overprivileged/semantic_review.json \
  --out reports/demo-agent-overprivileged-fused
```

预期结果：

```text
Fused install decision: warn (45 +0 -> 45)
```

融合输出：

```text
reports/demo-agent-overprivileged-fused/
  fused_analysis.json
  fused_trust_report.md
  fused_install_decision.json
  skilltrust-policy.json
  semantic_review_summary.md
```

## CLI 命令

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

## Fixture 结果

| Fixture | 声明意图 | 分数 | 风险等级 | 安装门禁 |
| --- | --- | ---: | --- | --- |
| `fixtures/benign-pdf-skill` | PDF summarization | 100 | Trusted | allow |
| `fixtures/overprivileged-research-skill` | Research/reporting | 45 | Overprivileged | warn |
| `fixtures/malicious-like-writing-skill` | Writing assistant | 25 | Critical Risk | block |

## Critical Data-Flow 保护

语义审查不能删除确定性证据。

如果 deterministic scanner 发现 critical sensitive-source-to-network-sink 证据，fusion 会保持 block：

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

预期结果：

```text
Fused install decision: block (25 +0 -> 25)
critical_dataflow_protected = true
```

## 本地 Skill 生态审计

审计本地 Skill 集合：

```bash
skilltrust audit-local --skills-root ~/.codex/skills --out reports/local-all
```

这个流程会给每个 Skill 生成治理包，并生成总览：

```text
reports/local-all/
  local_skills_report.md
  local_skills_summary.json
  skills/<skill-name>/
```

在原始开发环境中，SkillTrust 审计过 56 个本地 Skills：

| Total | Allow | Warn / Overlay Required | Block |
| ---: | ---: | ---: | ---: |
| 56 | 36 | 19 | 1 |

这些本地报告不会提交到仓库，因为它们可能包含本地路径或私有 profile evidence。

## Trust Fit Score

SkillTrust 使用 0 到 100 分：

| 分数 | 等级 |
| ---: | --- |
| 85-100 | Trusted |
| 70-84 | Mostly Trusted |
| 50-69 | Needs Review |
| 30-49 | Overprivileged |
| 0-29 | Critical Risk |

评分维度包括：

- Intent Clarity
- Permission Necessity
- Overreach Ratio
- Sensitive Surface
- Data Flow Safety
- Install-Time Safety
- Prompt Integrity
- Enforceability
- Auditability

Critical data-flow 会把结果限制在 Critical Risk。多个高危敏感越权 findings 会把结果限制在 Overprivileged。

## Policy Model

`skilltrust-policy.json` 表达安装前权限边界：

- filesystem allow/deny scopes
- network allow/deny domains and methods
- environment variable deny patterns
- shell command allow/deny lists
- connector consent requirements
- dependency and postinstall constraints
- prompt-integrity constraints
- host-Agent semantic refinements
- audit logging requirements

它是一个治理合约，未来可以接到 Skill installer、runner、registry 或 sandbox adapter。

## 安全边界

- 默认静态分析。
- 不执行目标 Skill。
- 不调用外部模型 API。
- 不需要 API Key。
- 不访问网络验证 endpoint。
- 把目标包文件视为不可信 evidence。
- semantic fusion 会保留 deterministic findings。
- 真实本地 Skill 审计报告不应直接公开。

## 开发

运行测试：

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
```

预期：

```text
15 passed
```

重新渲染英文/中文手绘流程图：

```bash
node ~/.codex/skills/excalidraw/scripts/render.js \
  docs/diagrams/skilltrust-flow.excalidraw \
  docs/assets/skilltrust-flow.png

node ~/.codex/skills/excalidraw/scripts/render.js \
  docs/diagrams/skilltrust-flow.zh-CN.excalidraw \
  docs/assets/skilltrust-flow.zh-CN.png
```

## 比赛叙事

SkillTrust 不只是 scanner，而是 AI Skills 的安装前信任治理层：

> SkillTrust combines reproducible static evidence with host-Agent semantic permission reasoning to make AI Skills installable with intent-bound trust.

它适合 Skill registry、Agent marketplace、企业审批流程和本地开发者工具链。
