---
name: pdf
description: Process only user-specified PDF files and write outputs to user-approved locations
metadata:
  short-description: Optimized preview for pdf
  source-package: "pdf"
  source-repository: "anthropics/skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# pdf

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Process only user-specified PDF files and write outputs to user-approved locations.

## Use When

- The user explicitly asks for: read, inspect, and process pdf documents.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read user-selected PDF files.
- Render, extract, summarize, or validate PDF content.
- Write derived reports, images, or form outputs to the current workspace.

Ask first:
- Editing or overwriting original PDFs.
- Reading folders of PDFs recursively.
- Uploading PDF content to external systems.

Denied by default:
- Reading unrelated documents or personal directories.
- Accessing credential stores or browser profiles.
- Deleting original documents.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Keep common PDF workflow in SKILL.md; defer form, rendering, and advanced validation details to references/scripts.

Selection plan: Trigger only for PDF-specific tasks; avoid competing with generic document-writing Skills.

## Source Attribution

- Upstream source repository: `anthropics/skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 145,914
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
