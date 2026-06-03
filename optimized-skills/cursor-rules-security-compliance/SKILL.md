---
name: cursor-rules-security-compliance
description: Use security/compliance rules as guidance while preventing credential-store overreach
metadata:
  short-description: Optimized preview for cursor-rules-awesome / security-compliance-slice
  source-package: "cursor-rules-awesome / security-compliance-slice"
  source-repository: "tonynguyennvt/cursor-rules-awesome"
  original-gate: "warn"
  optimized-posture: "warn-until-semantic-review-and-policy-approval"
---

# cursor-rules-awesome / security-compliance-slice

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Use security/compliance rules as guidance while preventing credential-store overreach.

## Use When

- The user explicitly asks for: security, privacy, compliance, and production-ops rule excerpts.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read current project files relevant to the security/compliance task.
- Load selected security or compliance guidance references.
- Write review notes and checklists.

Ask first:
- Scanning secrets or credential stores.
- Running production security tools.
- Changing security policy or configs.

Denied by default:
- Reading keychains, cookies, .env secrets, SSH keys, or cloud credentials unless explicitly scoped.
- Treating example paths as active filesystem access.
- Running external scans without approval.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Keep a small security router and defer detailed rules to references.

Selection plan: Rank for security/compliance coding-standard tasks only.

## Source Attribution

- Upstream source repository: `tonynguyennvt/cursor-rules-awesome`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 4
- Original SkillTrust gate: `warn`
- Optimized preview posture: `warn-until-semantic-review-and-policy-approval`
