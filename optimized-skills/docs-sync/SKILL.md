---
name: docs-sync
description: Sync docs within a confirmed repository root and keep writes reviewable
metadata:
  short-description: Optimized preview for docs-sync
  source-package: "docs-sync"
  source-repository: "chriscox/agent-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# docs-sync

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Sync docs within a confirmed repository root and keep writes reviewable.

## Use When

- The user explicitly asks for: documentation synchronization and repo-aware doc updates.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read docs, README, config, templates, and git status in the repo.
- Write doc updates inside approved doc paths.
- Run local documentation checks.

Ask first:
- Branch creation, commits, pushes, or GitHub issue/PR actions.
- Writing outside approved doc paths.
- Deleting docs.

Denied by default:
- Scanning unrelated repos.
- Uploading private docs externally.
- Changing source code unless explicitly requested.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move detailed quality checklists into references/config.

Selection plan: Rank for documentation sync, not general writing or project planning.

## Source Attribution

- Upstream source repository: `chriscox/agent-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 10
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
