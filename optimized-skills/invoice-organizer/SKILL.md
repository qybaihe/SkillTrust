---
name: invoice-organizer
description: Organize only user-selected invoice files while preserving originals and protecting financial metadata
metadata:
  short-description: Optimized preview for invoice-organizer
  source-package: "invoice-organizer"
  source-repository: "ComposioHQ/awesome-claude-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# invoice-organizer

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Organize only user-selected invoice files while preserving originals and protecting financial metadata.

## Use When

- The user explicitly asks for: organize invoice files and extract invoice metadata.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read user-selected invoice files or folders.
- Extract invoice metadata for local reports.
- Write organized copies and manifests to approved output folders.

Ask first:
- Moving, renaming, deleting, or overwriting originals.
- Uploading invoices or metadata.
- Processing folders recursively.

Denied by default:
- Reading unrelated financial, tax, or banking files.
- Printing sensitive invoice data into public logs.
- External transmission without explicit approval.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move extraction schemas, naming rules, and checklist logic into config/validators.

Selection plan: Trigger only for invoice organization and metadata extraction, not broad finance advice.

## Source Attribution

- Upstream source repository: `ComposioHQ/awesome-claude-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 63,040
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
