---
name: project-planner
description: Plan project work and create reviewable proposals before any GitHub or branch mutation
metadata:
  short-description: Optimized preview for project-planner
  source-package: "project-planner"
  source-repository: "chriscox/agent-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# project-planner

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Plan project work and create reviewable proposals before any GitHub or branch mutation.

## Use When

- The user explicitly asks for: project planning, proposal, issue, and branch workflow.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read project docs, issue templates, and current git state.
- Write local proposals, plans, and issue drafts.
- Prepare GitHub issue payloads without submitting.

Ask first:
- Creating GitHub issues or GraphQL sub-issues.
- Creating branches, committing, or pushing.
- Changing repo state.

Denied by default:
- Mutating GitHub without user approval.
- Planning across unrelated repos.
- Reading credentials or private accounts.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move proposal checklist and issue workflow mechanics into references/scripts.

Selection plan: Rank for planning/proposal tasks, not broad GitHub automation.

## Source Attribution

- Upstream source repository: `chriscox/agent-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 10
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
