---
name: skill-creator
description: Help an Agent create or improve a Skill package while keeping the activation harness compact and testable
metadata:
  short-description: Optimized preview for skill-creator
  source-package: "skill-creator"
  source-repository: "anthropics/skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# skill-creator

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Help an Agent create or improve a Skill package while keeping the activation harness compact and testable.

## Use When

- The user explicitly asks for: create, update, package, and validate agent skills.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read and edit files inside the user-confirmed Skill package only.
- Create references, scripts, assets, and validation artifacts inside that package.
- Run local validation commands requested by the user or required by the package.

Ask first:
- Creating or deleting files outside the active Skill package.
- Running sub-agent evaluation or benchmark workflows.
- Packaging artifacts for publication.

Denied by default:
- Reading unrelated home-directory secrets, browser profiles, SSH keys, or cloud credentials.
- Publishing or installing generated Skills without explicit user approval.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move examples, rubrics, and evaluation depth into references; keep SKILL.md as a compact router.

Selection plan: Use positive triggers around Skill creation/update/validation and negative triggers for unrelated document or app generation.

## Source Attribution

- Upstream source repository: `anthropics/skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 145,914
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
