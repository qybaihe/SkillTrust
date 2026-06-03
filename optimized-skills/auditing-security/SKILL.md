---
name: auditing-security
description: Audit only the target codebase and keep secret scanning inside user-approved scope
metadata:
  short-description: Optimized preview for auditing-security
  source-package: "auditing-security"
  source-repository: "spencerpauly/awesome-cursor-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# auditing-security

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Audit only the target codebase and keep secret scanning inside user-approved scope.

## Use When

- The user explicitly asks for: security-audit workflow for codebases and dependencies.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read target code, dependencies, configs, and docs.
- Run local security/dependency checks in the target repo.
- Write security reports and remediation plans.

Ask first:
- Scanning outside the target repo.
- Running exploit or network tests.
- Editing code or configs.

Denied by default:
- Reading unrelated SSH keys, cloud credentials, browser profiles, or home-directory secrets.
- Uploading findings without approval.
- Treating security audit as permission to attack external systems.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move deterministic audit checklists into validators/scripts.

Selection plan: Rank for codebase security audit, not Skill package audit or compliance-only review.

## Source Attribution

- Upstream source repository: `spencerpauly/awesome-cursor-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 367
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
