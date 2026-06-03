---
name: cursor-rules-installer
description: Make rule installation explicit, reversible, and user-approved
metadata:
  short-description: Optimized preview for cursor-rules-awesome / installer-package
  source-package: "cursor-rules-awesome / installer-package"
  source-repository: "tonynguyennvt/cursor-rules-awesome"
  original-gate: "warn"
  optimized-posture: "warn-until-semantic-review-and-policy-approval"
---

# cursor-rules-awesome / installer-package

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Make rule installation explicit, reversible, and user-approved.

## Use When

- The user explicitly asks for: npm installer and cli for writing .cursorrules.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read package metadata and installer intent.
- Prepare an install plan and backup plan.
- Write .cursorrules only after user confirmation.

Ask first:
- Running postinstall/init commands.
- Overwriting existing .cursorrules.
- Creating backups or changing project root files.

Denied by default:
- Silent postinstall mutation.
- Reading secrets during install.
- Network egress unrelated to package retrieval.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move installer behavior into explicit init policy and short setup checklist.

Selection plan: Rank only for installing Cursor rules, not using rules during coding.

## Source Attribution

- Upstream source repository: `tonynguyennvt/cursor-rules-awesome`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 4
- Original SkillTrust gate: `warn`
- Optimized preview posture: `warn-until-semantic-review-and-policy-approval`
