---
name: saving-workspace-context
description: Persist useful context inside the current workspace unless the user approves global memory
metadata:
  short-description: Optimized preview for saving-workspace-context
  source-package: "saving-workspace-context"
  source-repository: "spencerpauly/awesome-cursor-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# saving-workspace-context

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Persist useful context inside the current workspace unless the user approves global memory.

## Use When

- The user explicitly asks for: save and restore workspace memory/context.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read current project notes, docs, and relevant conversation summary.
- Append or update workspace-local context files.
- Generate restore summaries for the same workspace.

Ask first:
- Creating global rules, Skills, or cross-workspace memory.
- Writing outside the workspace.
- Deleting or overwriting memory files.

Denied by default:
- Saving secrets, tokens, private keys, or unrelated personal data.
- Cross-project leakage.
- Silent global persistence.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move routing rules and memory schema into config.

Selection plan: Rank for workspace-memory tasks, not project switching or documentation sync.

## Source Attribution

- Upstream source repository: `spencerpauly/awesome-cursor-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 367
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
