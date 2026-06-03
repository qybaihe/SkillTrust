---
name: agent-army
description: Coordinate bounded multi-agent work with file ownership, concurrency caps, and approval thresholds
metadata:
  short-description: Optimized preview for agent-army
  source-package: "agent-army"
  source-repository: "OneWave-AI/claude-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# agent-army

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Coordinate bounded multi-agent work with file ownership, concurrency caps, and approval thresholds.

## Use When

- The user explicitly asks for: multi-agent orchestration and parallel execution.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Plan parallel subtasks inside the current workspace.
- Spawn or coordinate agents only when the host supports it and the user asks for it.
- Write reports or patches in assigned file scopes.

Ask first:
- More than three concurrent agents.
- Continuous or autonomous mode.
- Any task that touches credentials, production, or external accounts.

Denied by default:
- Unbounded fan-out.
- Agents modifying overlapping files without coordination.
- Background work beyond the user-approved scope.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move orchestration templates and role matrices into config/references.

Selection plan: Rank for explicit multi-agent delegation, not ordinary task planning.

## Source Attribution

- Upstream source repository: `OneWave-AI/claude-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 169
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
