# Local Portfolio Audit

Use this when the user asks to inspect all local Agent Skills, rules, extensions, or reusable instructions.

## Root Detection

Ask the host Agent to identify the relevant local package root for the current environment. Examples include:

- Skills folders
- rules folders
- extensions folders
- reusable Agent instruction folders
- workspaces containing Skill-like packages

If no local package root exists, audit the bundled fixtures and explain how the user can provide a target package path.

## Read Before Ranking

For each package, deterministic scanning may triage quickly. Before making a final `warn` or `block` recommendation, read that package's core documents enough to understand its declared task boundary.

For high-risk or ambiguous packages, do a full-document pass before final summary.

## Portfolio Output

Summarize:

- total packages reviewed
- `allow`, `warn`, and `block` counts
- highest-risk packages
- overprivileged packages
- packages with suspicious data flow
- packages needing explicit policy overlays
- packages needing authoring, token, or taxonomy optimization
- where generated reports are located

## Read-Only Rule

Do not change local packages during a portfolio audit. Remediation, rename, or description updates must stay as approval plans until the user approves them.
