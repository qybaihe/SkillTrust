# Evaluated Skills Catalog

Date: 2026-06-03

Chinese version: [被评测 Skill 清单](evaluated-skills-catalog.zh-CN.md).

This catalog lists the public Skill, rule, and reusable-agent-instruction packages used in the SkillTrust benchmark. It is meant to make the evaluation scope explicit and reproducible.

Star counts were queried from the GitHub API on 2026-06-03. They are a point-in-time popularity signal and will change over time.

## Source Repositories By Stars

| Rank | Source | Stars | Forks | What It Is | Sample Count | Download |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 1 | [anthropics/skills](https://github.com/anthropics/skills) | 145,914 | 17,194 | Public Agent Skills repository from Anthropic | 3 | [ZIP](https://github.com/anthropics/skills/archive/refs/heads/main.zip) |
| 2 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 63,040 | 6,924 | Curated Claude Skills, resources, and workflow tools | 3 | [ZIP](https://github.com/ComposioHQ/awesome-claude-skills/archive/refs/heads/master.zip) |
| 3 | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 17,004 | 2,329 | Large multi-agent skill/plugin collection for Claude Code, Codex, Gemini CLI, Cursor, and other agents | 4 | [ZIP](https://github.com/alirezarezvani/claude-skills/archive/refs/heads/main.zip) |
| 4 | [spencerpauly/awesome-cursor-skills](https://github.com/spencerpauly/awesome-cursor-skills) | 367 | 60 | Curated Cursor skills and workflows | 4 | [ZIP](https://github.com/spencerpauly/awesome-cursor-skills/archive/refs/heads/main.zip) |
| 5 | [OneWave-AI/claude-skills](https://github.com/OneWave-AI/claude-skills) | 169 | 24 | Production-ready Claude Code Skills collection | 4 | [ZIP](https://github.com/OneWave-AI/claude-skills/archive/refs/heads/main.zip) |
| 6 | [Aurite-ai/agent-verifier](https://github.com/Aurite-ai/agent-verifier) | 39 | 5 | Agent verification Skill family for code quality, security, patterns, and language checks | 5 | [ZIP](https://github.com/Aurite-ai/agent-verifier/archive/refs/heads/main.zip) |
| 7 | [chriscox/agent-skills](https://github.com/chriscox/agent-skills) | 10 | 2 | Reusable skills for AI coding agents including Claude Code, Codex, Gemini CLI, and OpenClaw | 2 | [ZIP](https://github.com/chriscox/agent-skills/archive/refs/heads/main.zip) |
| 8 | [tonynguyennvt/cursor-rules-awesome](https://github.com/tonynguyennvt/cursor-rules-awesome) | 4 | 2 | Comprehensive Cursor rules package, also distributed as an npm package | 3 | [ZIP](https://github.com/tonynguyennvt/cursor-rules-awesome/archive/refs/heads/master.zip), [npm](https://www.npmjs.com/package/cursor-rules-awesome) |

## Evaluated Package List

| # | Package / Skill | Source | Stars | What It Does | SkillTrust Gate | Source / Download |
| ---: | --- | --- | ---: | --- | --- | --- |
| 1 | `skill-creator` | `anthropics/skills` | 145,914 | Helps create, validate, and package effective Agent Skills | allow | [source](https://github.com/anthropics/skills/tree/main/skills/skill-creator) |
| 2 | `mcp-builder` | `anthropics/skills` | 145,914 | Guides building MCP servers and related reference implementations | warn | [source](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) |
| 3 | `pdf` | `anthropics/skills` | 145,914 | PDF reading, form, and document-processing Skill | allow | [source](https://github.com/anthropics/skills/tree/main/skills/pdf) |
| 4 | `content-research-writer` | `ComposioHQ/awesome-claude-skills` | 63,040 | Research and long-form content-writing workflow | allow | [source](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/content-research-writer) |
| 5 | `invoice-organizer` | `ComposioHQ/awesome-claude-skills` | 63,040 | Organizes and extracts information from invoice documents | allow | [source](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/invoice-organizer) |
| 6 | `googledrive-automation` | `ComposioHQ/awesome-claude-skills` | 63,040 | Google Drive automation through connector/tool integration | allow | [source](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/composio-skills/googledrive-automation) |
| 7 | `skill-security-auditor` | `alirezarezvani/claude-skills` | 17,004 | Audits Skills for security issues and prompt-injection patterns | allow | [source](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/skill-security-auditor) |
| 8 | `playwright-pro` | `alirezarezvani/claude-skills` | 17,004 | Playwright testing and browser automation skill pack | allow | [source](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/playwright-pro) |
| 9 | `ms365-tenant-manager` | `alirezarezvani/claude-skills` | 17,004 | Microsoft 365 tenant administration workflow | allow | [source](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/ms365-tenant-manager) |
| 10 | `senior-architect` | `alirezarezvani/claude-skills` | 17,004 | Architecture analysis and system-design guidance | allow | [source](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/senior-architect) |
| 11 | `agent-army` | `OneWave-AI/claude-skills` | 169 | Multi-agent orchestration and parallel execution workflow | allow | [source](https://github.com/OneWave-AI/claude-skills/tree/main/agent-army) |
| 12 | `code-review-pro` | `OneWave-AI/claude-skills` | 169 | Professional code review workflow | allow | [source](https://github.com/OneWave-AI/claude-skills/tree/main/code-review-pro) |
| 13 | `compliance-checker` | `OneWave-AI/claude-skills` | 169 | Compliance review and evidence/report generation workflow | allow | [source](https://github.com/OneWave-AI/claude-skills/tree/main/compliance-checker) |
| 14 | `incident-responder` | `OneWave-AI/claude-skills` | 169 | Incident response workflow with operational investigation steps | allow | [source](https://github.com/OneWave-AI/claude-skills/tree/main/incident-responder) |
| 15 | `docs-sync` | `chriscox/agent-skills` | 10 | Documentation synchronization and repo-aware doc updates | allow | [source](https://github.com/chriscox/agent-skills/tree/main/skills/docs-sync) |
| 16 | `project-planner` | `chriscox/agent-skills` | 10 | Project planning, proposal, issue, and branch workflow | allow | [source](https://github.com/chriscox/agent-skills/tree/main/skills/project-planner) |
| 17 | `auditing-security` | `spencerpauly/awesome-cursor-skills` | 367 | Security-audit workflow for codebases and dependencies | allow | [source](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/auditing-security) |
| 18 | `switching-projects` | `spencerpauly/awesome-cursor-skills` | 367 | Cursor workspace/project switching workflow | allow | [source](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/switching-projects) |
| 19 | `saving-workspace-context` | `spencerpauly/awesome-cursor-skills` | 367 | Saves and restores workspace memory/context | allow | [source](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/saving-workspace-context) |
| 20 | `visual-qa-testing` | `spencerpauly/awesome-cursor-skills` | 367 | Visual QA workflow using browser, screenshots, console, and network inspection | allow | [source](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/visual-qa-testing) |
| 21 | `cursor-rules-awesome / monolithic-rules` | `tonynguyennvt/cursor-rules-awesome` | 4 | Full `.cursorrules` rules library with many domains and frameworks | warn | [source](https://github.com/tonynguyennvt/cursor-rules-awesome/blob/master/.cursorrules), [npm](https://www.npmjs.com/package/cursor-rules-awesome) |
| 22 | `cursor-rules-awesome / installer-package` | `tonynguyennvt/cursor-rules-awesome` | 4 | npm installer and CLI that writes `.cursorrules` | warn | [source](https://github.com/tonynguyennvt/cursor-rules-awesome/tree/master/bin), [npm](https://www.npmjs.com/package/cursor-rules-awesome) |
| 23 | `cursor-rules-awesome / security-compliance-slice` | `tonynguyennvt/cursor-rules-awesome` | 4 | Security, privacy, compliance, and production-ops rule excerpts | warn | [source](https://github.com/tonynguyennvt/cursor-rules-awesome/blob/master/.cursorrules), [npm](https://www.npmjs.com/package/cursor-rules-awesome) |
| 24 | `verification` | `Aurite-ai/agent-verifier` | 39 | Orchestrator for multi-review verification | allow | [source](https://github.com/Aurite-ai/agent-verifier/tree/main/skills/verification) |
| 25 | `verify-security` | `Aurite-ai/agent-verifier` | 39 | Security and compliance verification | allow | [source](https://github.com/Aurite-ai/agent-verifier/tree/main/skills/verify-security) |
| 26 | `verify-patterns` | `Aurite-ai/agent-verifier` | 39 | Pattern and consistency verification | allow | [source](https://github.com/Aurite-ai/agent-verifier/tree/main/skills/verify-patterns) |
| 27 | `verify-quality` | `Aurite-ai/agent-verifier` | 39 | Quality and readiness verification | allow | [source](https://github.com/Aurite-ai/agent-verifier/tree/main/skills/verify-quality) |
| 28 | `verify-language` | `Aurite-ai/agent-verifier` | 39 | Language, ambiguity, and wording verification | allow | [source](https://github.com/Aurite-ai/agent-verifier/tree/main/skills/verify-language) |

## Why This Catalog Matters

This benchmark intentionally includes both very high-star repositories and smaller emerging Skill ecosystems:

- High-star sources prove that SkillTrust can evaluate real public Skill ecosystems rather than only local toy fixtures.
- Smaller specialized sources prove that SkillTrust can handle newer Agent package formats, Cursor rules, npm-distributed rule packs, and verification Skill families.
- The mixed results are more credible than a fear-based benchmark: most packages were installable, but many still had optimization opportunities around token efficiency, policy precision, taxonomy, and semantic review.

## Scope Notes

- SkillTrust did not modify any third-party project.
- Several targets were audited in `network-limited` mode because full local clone/ZIP access was unreliable.
- The `cursor-rules-awesome` sample was audited from the installable npm package snapshot as well as public repository metadata.
- Star counts and repository metadata were queried on 2026-06-03 and may change.
- `warn` does not mean malicious. It means the package needs review, scoping, semantic clarification, or policy overlay before use.
