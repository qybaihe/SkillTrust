---
name: ms365-tenant-manager
description: Plan and perform tenant-scoped Microsoft 365 actions with dry-run defaults and explicit approval gates
metadata:
  short-description: Optimized preview for ms365-tenant-manager
  source-package: "ms365-tenant-manager"
  source-repository: "alirezarezvani/claude-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# ms365-tenant-manager

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Plan and perform tenant-scoped Microsoft 365 actions with dry-run defaults and explicit approval gates.

## Use When

- The user explicitly asks for: microsoft 365 tenant administration workflow.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read user-provided tenant context and requested admin scope.
- Generate PowerShell/Graph plans and dry-run scripts.
- Write local admin plans, manifests, and rollback notes.

Ask first:
- Any Graph, PowerShell, or tenant write action.
- User, group, policy, license, or security setting changes.
- Using admin credentials or connector sessions.

Denied by default:
- Tenant-wide changes without named scope.
- Reading unrelated local credentials.
- Executing production changes without dry-run and approval.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move PowerShell templates and troubleshooting into references/scripts.

Selection plan: Rank for explicit M365 tenant administration, not generic cloud or compliance tasks.

## Source Attribution

- Upstream source repository: `alirezarezvani/claude-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 17,004
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
