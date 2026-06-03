# Policy And Remediation

Use this when the user wants to make a package safer or installable.

## Policy Goal

Constrain the package to the minimum permissions needed for its declared task.

Policy should cover:

- filesystem reads and writes
- network destinations
- environment variables
- shell commands
- connectors and account access
- dependency and install-time behavior
- prompt-integrity boundaries
- explicit user confirmations

## Remediation Style

Generate reviewable changes. Do not silently edit the original package.

Good remediation output includes:

- narrowed permission manifest
- policy overlay
- reasons each allowed permission is necessary
- denied or user-confirmation scopes
- edits that would reduce overreach
- remaining risks
- approval checklist

## Least-Privilege Questions

For every permission, ask:

- What declared task requires this?
- Can the task succeed with a narrower scope?
- Is this permission optional?
- Should the user confirm it every time?
- Should it be denied by default?

## Approval Boundary

Real local packages should not be changed until the user explicitly approves a concrete plan.
