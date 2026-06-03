---
name: switching-projects
description: Switch active project only after the user confirms the target path and scope change
metadata:
  short-description: Optimized preview for switching-projects
  source-package: "switching-projects"
  source-repository: "spencerpauly/awesome-cursor-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# switching-projects

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Switch active project only after the user confirms the target path and scope change.

## Use When

- The user explicitly asks for: cursor workspace/project switching workflow.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- List or inspect candidate workspaces only when requested.
- Prepare a switch plan for the chosen target.
- Update local context notes after confirmation.

Ask first:
- Changing the active workspace.
- Opening or modifying a new project.
- Persisting cross-workspace memory.

Denied by default:
- Searching unrelated personal directories broadly.
- Switching projects silently.
- Copying files between projects without approval.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Encode output format and switch checks in schema/config.

Selection plan: Rank for explicit project-switching requests only.

## Source Attribution

- Upstream source repository: `spencerpauly/awesome-cursor-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 367
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
