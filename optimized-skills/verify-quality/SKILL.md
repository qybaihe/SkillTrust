---
name: verify-quality
description: Assess quality/readiness evidence without changing implementation
metadata:
  short-description: Optimized preview for verify-quality
  source-package: "verify-quality"
  source-repository: "Aurite-ai/agent-verifier"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# verify-quality

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Assess quality/readiness evidence without changing implementation.

## Use When

- The user explicitly asks for: verify quality and readiness.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read selected code, specs, test summaries, and docs.
- Assess quality criteria and readiness risks.
- Write quality verification reports.

Ask first:
- Running tests or build commands.
- Editing code.
- Changing release status.

Denied by default:
- Approving release without evidence.
- Reading unrelated secrets.
- Replacing human approval for high-risk launches.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move quality criteria and report schema into references/config.

Selection plan: Trigger for quality/readiness verification, not security or language-only review.

## Source Attribution

- Upstream source repository: `Aurite-ai/agent-verifier`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 39
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
