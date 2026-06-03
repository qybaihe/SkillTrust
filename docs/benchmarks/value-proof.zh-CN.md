# SkillTrust 价值证明

日期：2026-06-03

英文版：[SkillTrust Value Proof](value-proof.md)。

优化版 preview package：[optimized-skills](../../optimized-skills/)。

这份报告把公开 benchmark 从“是否 allow / warn / block”升级为价值证明：SkillTrust 不只是判断一个 AI Skill package 能不能安装，还会生成优化计划，让它更精简、更受意图约束、更容易被 Agent 精准选择。

下面的数据来自 28 个具有代表性的公开 AI Skill、Claude Skill、Cursor rules 和 Agent instruction packages。部分目标是在 `network-limited` 模式下通过 raw file、页面快照或 package snapshot 审计，因此这些数字适合理解为代表性静态样本，而不是完整供应链审计。

## 评估维度

SkillTrust 从七个维度评估价值：

| 维度 | 衡量什么 | 为什么重要 |
| --- | --- | --- |
| 安装安全性 | package 是 `allow`、`warn` 还是 `block` | 判断是否可以安装，或是否需要进一步审查。 |
| Activation 效率 | 哪些常驻 instruction tokens 可以移到 references、scripts、schemas、validators 或 config | 减少上下文负担，让 Skill 更容易被精准激活。 |
| Harness 结构 | `SKILL.md` 是精简触发 harness，还是巨大的手册 | 提升 Agent 激活质量，减少无关上下文。 |
| Policy 精准度 | connector scope、workspace binding、用户确认门禁、破坏性动作门禁 | 把宽泛能力变成 intent-bound permission governance。 |
| 语义精准度 | AI 全文阅读后，能否区分真实风险、示例代码和参考文本 | 降低 noisy scanner findings，同时保留证据链。 |
| Taxonomy 准确性 | 相关 Skills 的命名和 description 是否重叠 | 帮助 Agent 选中正确 package。 |
| Selection precision / rankability | 正向触发条件、负向触发条件、scope-bound activation signals、专业边界 | 让优化后的正确 Skill 在相似 package 中排序更靠前。 |

## Governance 覆盖

![SkillTrust governance coverage](../assets/value-proof-governance.svg)

在 28 个公开样本中，SkillTrust 大体确认热门 package 是可安装的，同时仍然发现了大量优化空间：

- 24 个 package 是 `allow`
- 4 个 package 是 `warn`
- 0 个 package 是 `block`
- 20 个 package 有 token-saving 机会
- 发现 17 个 reference extraction candidates
- 发现 26 个 scriptification candidates
- 发现 9 个 taxonomy findings

这就是核心价值证明：安全不等于已经优化。一个 package 即使可以安装，也仍然可以变得更精准、更精简、更可治理。

## Activation Token 降低

![SkillTrust token reduction](../assets/value-proof-token-reduction.svg)

在 28 个样本中：

- 优化计划前：预计 30,699 个 activation-body tokens
- SkillTrust 识别出可以移出常驻 instruction 的 tokens：6,832
- 应用首轮 SkillTrust plan 后：预计 23,867 个 activation-body tokens
- 预计降低：22.3%

这不是生产环境账单或延迟 benchmark，而是 activation context 估算。它证明 SkillTrust 能识别哪些内容应该从常驻 instruction 移到延迟加载的 references、scripts、schemas、validators 或 config。

## Optimization Surface

![SkillTrust optimization surface](../assets/value-proof-optimization-surface.svg)

这次 benchmark 找到了多种优化面：

- authoring findings
- scriptification candidates
- reference extraction candidates
- taxonomy findings
- approval-plan items
- install-time warn decisions

这说明 SkillTrust 是治理层，而不是普通 scanner。它可以确认 package 基本安全，同时继续生成让 package 更安全、更轻、更精准的计划。

## Selection Precision Ranking

![SkillTrust selection precision](../assets/value-proof-selection-precision.svg)

SkillTrust 还会对“哪些 package 优化后最能提升 Agent 选择精准度”做排序。这里不宣称已经测得生产环境准确率提升，而是给出可审查的 rankability signal：taxonomy findings、trigger overlap、monolithic always-on context、缺少 negative triggers、缺少 scope boundaries。

| 排名 | Package / Portfolio | 优化前的选择问题 | SkillTrust 优化计划 | 预期选择效果 |
| ---: | --- | --- | --- | --- |
| 1 | `agent-verifier` | 权限很干净，但 `verify-*` Skills 高度重叠；样本 portfolio 的 taxonomy score 是 `0` | 保留 `verification` 作为 orchestrator；为 `verify-security`、`verify-quality`、`verify-patterns`、`verify-language` 补充正向触发、负向触发和 delegation rules | overlap findings 目标从 `6` 降到 `0`；重新审计后的 taxonomy score 目标是 `80+` |
| 2 | `cursor-rules-awesome` | 4,861 行 monolithic rules file 让许多无关领域挤在同一个 activation context 里 | 用短 router 加 domain references 替代全量规则，例如 security、backend、frontend、SRE、compliance、mobile、data、API | 任务相关 rules 可以排在泛化 rules 前面；taxonomy score 目标是 `100` |
| 3 | `project-planner` | planning、GitHub issue、GraphQL sub-issues、branch、push 行为容易和通用 GitHub automation 混淆 | 增加 repo-root binding，并对 GitHub mutation 加用户确认门禁 | 让它保持 planner 身份，而不是变成宽泛 repository automation Skill |
| 4 | `skill-creator` | authoring / evaluation 指导范围很宽，activation body 很重 | 把深层 evaluation guidance 移到 references、schemas 和 command wrappers | 更容易只在创建、更新或验证 Skills 时被触发 |
| 5 | `content-research-writer` | 可信但 monolithic，research、writing 和 connector 行为容易混在一起 | 拆分 rubrics / workflows 到 references，并明确 connector scope | Agent 更容易区分 research-writing intent 和 drive/document automation intent |

这个排序很适合比赛展示：它证明 SkillTrust 不只是发现安全问题，还能告诉你哪些优化最可能提升 Agent 的实际使用效果。

## 代表性 Before / After 案例

| Package | Baseline | SkillTrust 优化计划 | 价值信号 |
| --- | --- | --- | --- |
| `skill-creator` | 8,156 activation-body tokens，token-heavy，基本可信 | 首轮 plan 节省 1,346 tokens；compact preview target 节省 6,156 tokens | 通过 references、schemas、command wrappers 显著降低 activation 成本。 |
| `content-research-writer` | 可信但 monolithic | 首轮 plan 节省 1,215 tokens，并把 workflows / rubrics 拆到 references | 说明高可信 Skill 也可以继续优化激活质量。 |
| `project-planner` | `allow`，96/100 trust score | 为 GitHub issue creation、GraphQL sub-issues、branch creation、push behavior 增加用户确认门禁 | 展示 pass/fail 之外的 policy precision。 |
| `cursor-rules-awesome` | 4,861 行 monolithic rules file，`warn` | 用 router + references 只加载相关 slice；任务级 context reduction 预计 95.8%-98.6% | 展示 dramatic context reduction 和 semantic false-positive handling。 |
| `agent-verifier` | 权限 profile 干净 | taxonomy fixes，并预计节省约 896 activation tokens | 说明 `allow` package 也能继续提升 selection accuracy 和 efficiency。 |

## SkillTrust 之后发生了什么

| 优化前 | SkillTrust plan 之后 |
| --- | --- |
| package 只得到简单 pass/fail 审查 | package 得到 install decision、manifest、policy、receipt、report 和 remediation plan |
| 很长的 instruction files 一直常驻加载 | 细节移动到 references、schemas、validators、scripts 或 config |
| 宽泛工具能力被默认为隐式授权 | 高影响动作加入 workspace binding、connector scope 和用户确认门禁 |
| scanner findings 可能 noisy | Host-Agent 全文阅读后可以标记 likely false positives，同时保留 evidence |
| 相似 Skills 的 trigger 可能重叠 | taxonomy plan 提出更清晰的 name 和 description，等待用户审批 |
| 多个 Skills 对同一个用户请求竞争 | selection precision ranking 找出最需要 sharpen triggers、anti-triggers 和 scope boundaries 的 package |

## 公开说明与边界

- 这次 benchmark 是 preliminary static benchmark。
- 部分仓库因为 clone / ZIP / 网络访问不稳定，采用了 network-limited raw / page / package snapshots。
- SkillTrust 没有修改第三方项目。
- token savings 是 optimization-plan estimate，不是生产账单或延迟实测。
- selection precision ranking 是 projected rankability signal，不是端到端生产准确率 benchmark。
- `warn` 不代表 malicious。它表示 package 在使用前需要 review、scoping、semantic clarification 或 policy overlay。

## 总结

这次 benchmark 支持的核心结论比“SkillTrust 能找风险”更强：

> SkillTrust can turn popular AI Skill packages into more intent-bound, token-efficient, policy-constrained, and selection-accurate packages before installation or use.

换句话说，SkillTrust 的价值不是让所有东西都变成 `block`，而是让可以安装的 Skills 继续变得更可控、更省上下文、更容易被 Agent 精准调用。
