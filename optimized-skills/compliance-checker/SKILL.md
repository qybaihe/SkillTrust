---
name: compliance-checker
description: Check compliance evidence inside a named scope and write reviewable reports only
metadata:
  short-description: Optimized preview for compliance-checker
  source-package: "compliance-checker"
  source-repository: "OneWave-AI/claude-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# compliance-checker

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Check compliance evidence inside a named scope and write reviewable reports only.

## Use When

- The user explicitly asks for: compliance review and evidence/report generation.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read user-selected evidence, policies, docs, and code.
- Run local discovery commands limited to the target scope.
- Write compliance reports and evidence maps.

Ask first:
- Writing or changing compliance controls.
- Accessing external systems or customer data.
- Using Bash beyond discovery commands.

Denied by default:
- Reading unrelated employee/customer records.
- Making legal conclusions without caveats.
- Uploading evidence without approval.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move compliance matrices and checklists into references/schemas.

Selection plan: Rank for compliance assessment, not incident response or general security scanning.

## Source Attribution

- Upstream source repository: `OneWave-AI/claude-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 169
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
