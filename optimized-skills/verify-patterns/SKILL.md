---
name: verify-patterns
description: Check whether code/specs follow stated patterns and architectural conventions
metadata:
  short-description: Optimized preview for verify-patterns
  source-package: "verify-patterns"
  source-repository: "Aurite-ai/agent-verifier"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# verify-patterns

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Check whether code/specs follow stated patterns and architectural conventions.

## Use When

- The user explicitly asks for: verify pattern and consistency requirements.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read selected files or summaries.
- Compare against user-provided patterns.
- Write consistency findings.

Ask first:
- Editing code.
- Scanning unrelated repos.
- Running tools that mutate state.

Denied by default:
- Making security claims outside pattern scope.
- Reading secrets.
- Broad filesystem traversal.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move checklist patterns into structured config.

Selection plan: Trigger for pattern consistency, not security or language review.

## Source Attribution

- Upstream source repository: `Aurite-ai/agent-verifier`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 39
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
