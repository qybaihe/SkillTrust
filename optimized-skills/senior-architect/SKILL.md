---
name: senior-architect
description: Analyze architecture inside user-confirmed project boundaries and produce design recommendations
metadata:
  short-description: Optimized preview for senior-architect
  source-package: "senior-architect"
  source-repository: "alirezarezvani/claude-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# senior-architect

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Analyze architecture inside user-confirmed project boundaries and produce design recommendations.

## Use When

- The user explicitly asks for: architecture analysis and system-design guidance.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read code, docs, and configs in the selected project.
- Run local dependency or architecture analysis tools.
- Write diagrams, tradeoff notes, and decision records.

Ask first:
- Scanning outside the project root.
- Changing architecture files or build configs.
- Running external dependency scans or uploads.

Denied by default:
- Reading unrelated secrets or personal files.
- Changing production infrastructure.
- Treating architecture review as deployment permission.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move pattern libraries and decision frameworks into references.

Selection plan: Rank for architecture/design tasks, not code review or project planning.

## Source Attribution

- Upstream source repository: `alirezarezvani/claude-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 17,004
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
