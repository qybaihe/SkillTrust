# Single Package Audit

Use this when the user gives one Skill, rule, extension, repository, or folder to review.

## Review Order

1. Load safety boundaries from `references/00-safety-boundaries.md`.
2. Read the target package's core documents end-to-end.
3. Summarize the declared task boundary.
4. Infer the minimum permissions needed for that task.
5. Use deterministic evidence to locate observed or requested behavior.
6. Reconcile every finding against the declared boundary.
7. Produce an install recommendation: `allow`, `warn`, or `block`.

## Intent-Bound Permission Questions

Ask:

- Does the package need filesystem read access? To what exact user-provided files?
- Does it need filesystem write access? To what exact outputs?
- Does it need network access? To which declared destinations?
- Does it need shell commands? Are they bounded and understandable?
- Does it need environment variables? Which ones and why?
- Does it need connectors, browser access, cookies, or account state?
- Does it ask for personal data that is unnecessary for its declared task?

## Semantic Decision

Prefer `allow` when:

- intent is clear
- permissions are narrow
- behavior matches the declared task
- no sensitive data flow is present

Prefer `warn` when:

- behavior is useful but overbroad
- a policy overlay or user confirmation would make it safe
- deterministic findings are plausible but need context
- authoring is unclear enough to affect safety

Prefer `block` when:

- sensitive data is sent to undeclared destinations
- the package hides actions from the user
- install-time behavior is dangerous
- the declared intent and actual behavior materially conflict
