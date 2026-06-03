---
name: mcp-builder
description: Help build MCP servers with explicit runtime boundaries, generated-code labels, and least-privilege defaults
metadata:
  short-description: Optimized preview for mcp-builder
  source-package: "mcp-builder"
  source-repository: "anthropics/skills"
  original-gate: "warn"
  optimized-posture: "warn-until-semantic-review-and-policy-approval"
---

# mcp-builder

This is a SkillTrust-generated optimized preview, not an official upstream release. Before using it in production, review `skilltrust/permission_manifest.json`, `skilltrust/skilltrust-policy.json`, and the upstream source.

## Declared Intent

Help build MCP servers with explicit runtime boundaries, generated-code labels, and least-privilege defaults.

## Use When

- The user explicitly asks for: guide mcp server creation and reference implementations.
- The target workspace, document set, connector scope, or runtime boundary is named or can be confirmed.
- A least-privilege, reviewable workflow is preferred over broad implicit permission.

## Do Not Use When

- The request needs a different specialized Skill with a narrower trigger.
- The user has not confirmed the target scope for reads, writes, connectors, or external systems.
- The task would require unrelated local secrets, credential stores, browser profiles, or production mutation without approval.

## Minimal Permission Contract

Allowed by default:
- Read and write MCP project files inside the user-confirmed workspace.
- Generate server templates, schemas, and local test scripts.
- Read named environment variable names without printing secret values.

Ask first:
- Installing dependencies or running generated servers.
- Adding external API endpoints or network egress.
- Writing credentials, tokens, or deployment config.

Denied by default:
- Printing or exfiltrating secret values.
- Treating reference/example code as permission to access the host filesystem.
- Broad filesystem reads outside the MCP project.

## Optimized Workflow

1. Restate the user's requested intent and target scope.
2. Read only the files, documents, tools, or connector surfaces needed for that intent.
3. Apply the minimal permission contract above.
4. If a requested action falls into "Ask first", pause and request explicit confirmation.
5. Produce a concise result plus any evidence, manifest, or review notes needed for auditability.

## Token And Selection Optimization

Token plan: Keep server-type routing in the Skill; move Node/Python templates, evaluation checklists, and best practices into references/scripts.

Selection plan: Rank for MCP server-building tasks only; avoid triggering on generic API docs or package setup.

## Source Attribution

- Upstream source repository: `anthropics/skills`
- Source sample and download links: see `../manifest.json`
- GitHub stars at benchmark time: 145,914
- Original SkillTrust gate: `warn`
- Optimized preview posture: `warn-until-semantic-review-and-policy-approval`
