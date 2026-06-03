---
name: code-review-pro
description: Review code changes within a confirmed repository and produce prioritized findings
metadata:
  short-description: Optimized preview for code-review-pro
  source-package: "code-review-pro"
  source-repository: "OneWave-AI/claude-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# code-review-pro

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Review code changes within a confirmed repository and produce prioritized findings.

## Use When

- The user explicitly asks for: professional code review workflow.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read target code, diffs, tests, and docs inside the repo.
- Run local static checks or tests when appropriate.
- Write review reports.

Ask first:
- Editing code instead of reviewing.
- Scanning unrelated repos or personal files.
- Uploading review artifacts externally.

Denied by default:
- Reading secrets or credential stores.
- Inventing findings without evidence.
- Changing production systems.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move review rubrics and examples into references.

Selection plan: Rank for code review, not architecture design or security-only audits.

## Source Attribution

- Upstream source repository: `OneWave-AI/claude-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 169
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
