---
name: incident-responder
description: Investigate incidents within a declared scope while gating production-facing actions
metadata:
  short-description: Optimized preview for incident-responder
  source-package: "incident-responder"
  source-repository: "OneWave-AI/claude-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# incident-responder

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Investigate incidents within a declared scope while gating production-facing actions.

## Use When

- The user explicitly asks for: incident response workflow with operational investigation.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read user-provided logs, alerts, runbooks, and relevant code.
- Draft timelines, hypotheses, and response checklists.
- Write local incident notes and postmortem drafts.

Ask first:
- Status-page updates, customer communications, deploy changes, or remediation actions.
- Using external incident systems.
- Running Bash/Edit commands that change state.

Denied by default:
- Changing production without approval.
- Accessing unrelated accounts or logs.
- Publishing incident details externally.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move response playbooks and communication templates into references.

Selection plan: Rank for declared incident response, not generic debugging or compliance.

## Source Attribution

- Upstream source repository: `OneWave-AI/claude-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 169
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
