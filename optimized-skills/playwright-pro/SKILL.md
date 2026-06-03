---
name: playwright-pro
description: Generate, run, and debug Playwright tests inside a confirmed project and target URL scope
metadata:
  short-description: Optimized preview for playwright-pro
  source-package: "playwright-pro"
  source-repository: "alirezarezvani/claude-skills"
  original-gate: "allow"
  optimized-posture: "allow-with-policy"
---

# playwright-pro

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Generate, run, and debug Playwright tests inside a confirmed project and target URL scope.

## Use When

- The user explicitly asks for: playwright testing and browser automation workflows.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read test files and app code in the chosen repo.
- Run local Playwright commands and collect screenshots/traces.
- Write tests and reports in the workspace.

Ask first:
- Using BrowserStack, TestRail, or external test services.
- Navigating to credentialed or unrelated websites.
- Changing production data.

Denied by default:
- Reading browser profiles, cookies, or unrelated credentials.
- Running destructive browser flows without approval.
- Leaking screenshots or traces externally.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Move command catalogs and integration setup into references/scripts.

Selection plan: Rank for Playwright-specific test tasks, not all browser automation.

## Source Attribution

- Upstream source repository: `alirezarezvani/claude-skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 17,004
- Original SkillTrust gate: `allow`
- Optimized preview posture: `allow-with-policy`
