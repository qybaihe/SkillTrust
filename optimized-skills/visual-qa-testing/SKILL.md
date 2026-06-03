---
name: visual-qa-testing
description: Run visual QA only against local or user-specified URLs and keep captured artifacts scoped
metadata:
  short-description: Optimized preview for visual-qa-testing
  source-package: "visual-qa-testing"
  source-repository: "spencerpauly/awesome-cursor-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# visual-qa-testing

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Run visual QA only against local or user-specified URLs and keep captured artifacts scoped.

## Use When

- The user explicitly asks for: visual qa using browser, screenshots, console, and network inspection.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Navigate to local or explicitly user-approved URLs.
- Collect screenshots, console errors, and network observations.
- Write QA reports and annotated findings.

Ask first:
- Accessing authenticated or unrelated sites.
- Changing application state or submitting forms.
- Uploading screenshots/traces.

Denied by default:
- Reading browser cookies or credential stores.
- Testing unrelated websites.
- Capturing personal data without user scope.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move procedural visual QA steps into references/schema.

Selection plan: Rank for visual QA, not generic browser automation.

## Source Attribution

- Upstream source repository: `spencerpauly/awesome-cursor-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 367
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
