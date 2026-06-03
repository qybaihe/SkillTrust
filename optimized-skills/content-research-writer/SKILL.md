---
name: content-research-writer
description: Produce research-backed writing inside a user-confirmed project folder with clear source handling
metadata:
  short-description: Optimized preview for content-research-writer
  source-package: "content-research-writer"
  source-repository: "ComposioHQ/awesome-claude-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# content-research-writer

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Produce research-backed writing inside a user-confirmed project folder with clear source handling.

## Use When

- The user explicitly asks for: research and write long-form content.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read user-provided briefs, notes, and source documents.
- Write drafts, outlines, and revision notes inside the chosen workspace.
- Use web research only when the user asks for current or external evidence.

Ask first:
- Creating new writing folders outside the workspace.
- Publishing, emailing, or uploading drafts.
- Using connector accounts or private documents.

Denied by default:
- Reading unrelated personal files.
- Inventing citations or copying long copyrighted passages.
- Treating Drive or document automation as implied permission.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move rubrics, examples, style libraries, and review workflows into references.

Selection plan: Distinguish research-writing from Drive automation, document formatting, and generic summarization.

## Source Attribution

- Upstream source repository: `ComposioHQ/awesome-claude-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 63,040
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
