---
name: googledrive-automation
description: Perform session-scoped Google Drive actions that match the user request and connector consent
metadata:
  short-description: Optimized preview for googledrive-automation
  source-package: "googledrive-automation"
  source-repository: "ComposioHQ/awesome-claude-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# googledrive-automation

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Perform session-scoped Google Drive actions that match the user request and connector consent.

## Use When

- The user explicitly asks for: automate google drive tasks through connector tools.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- List, search, read, create, or update Drive files only when requested.
- Use connector tools authorized by the current session.
- Write local summaries or manifests for performed actions.

Ask first:
- Deleting, sharing, moving, or overwriting Drive files.
- Changing permissions or external visibility.
- Touching files outside the user-selected Drive scope.

Denied by default:
- Using OAuth grants as open-ended authority.
- Accessing unrelated Drive folders.
- Exporting Drive data to unapproved destinations.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Keep connector intent and safety boundaries in SKILL.md; move operation maps into policy/config.

Selection plan: Rank for explicit Google Drive tasks, not generic writing or file organization.

## Source Attribution

- Upstream source repository: `ComposioHQ/awesome-claude-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 63,040
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
