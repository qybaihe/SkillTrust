---
name: cursor-rules-router
description: Route to only the relevant domain rules instead of loading every rule into every task
metadata:
  short-description: Optimized preview for cursor-rules-awesome / monolithic-rules
  source-package: "cursor-rules-awesome / monolithic-rules"
  source-repository: "tonynguyennvt/cursor-rules-awesome"
  original-gate: "warn"
  optimized-posture: "warn-until-semantic-review-and-policy-approval"
---

# cursor-rules-awesome / monolithic-rules

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Route to only the relevant domain rules instead of loading every rule into every task.

## Use When

- The user explicitly asks for: large all-purpose cursor rules library.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read the current project stack and task intent.
- Load one to three relevant rule references.
- Write a scoped rule-selection report.

Ask first:
- Installing or writing .cursorrules into a project.
- Loading broad security/compliance rules for unrelated tasks.
- Changing project configuration.

Denied by default:
- Treating examples about cookies, keychains, or .env files as permission to read local secrets.
- Loading all 4,861 lines as always-on context.
- Automatic project mutation.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Replace monolithic always-on rules with a short router plus domain references.

Selection plan: Rank relevant domain rules above generic all-purpose rules.

## Source Attribution

- Upstream source repository: `tonynguyennvt/cursor-rules-awesome`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 4
- Original SkillTrust gate: `warn`
- Optimized preview posture: `warn-until-semantic-review-and-policy-approval`
