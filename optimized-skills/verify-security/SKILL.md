---
name: verify-security
description: Perform read-only security verification against user-provided specs or code summaries
metadata:
  short-description: Optimized preview for verify-security
  source-package: "verify-security"
  source-repository: "Aurite-ai/agent-verifier"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# verify-security

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Perform read-only security verification against user-provided specs or code summaries.

## Use When

- The user explicitly asks for: verify security and compliance properties.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read selected code/specs/docs.
- Check security claims against policy and evidence.
- Write verification findings.

Ask first:
- Running active scans or exploit tests.
- Reading secrets or credential stores.
- Editing code.

Denied by default:
- Treating review as operational access.
- Scanning unrelated systems.
- Publishing sensitive findings.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move deterministic red-lines and severity schemas into validators.

Selection plan: Trigger for security verification, not general quality, language, or pattern review.

## Source Attribution

- Upstream source repository: `Aurite-ai/agent-verifier`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 39
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
