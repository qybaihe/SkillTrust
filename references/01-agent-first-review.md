# Agent-First Review Protocol

SkillTrust should feel like an Agent reading and governing a Skill, not a code rule engine making shallow judgments.

## Principle

Deterministic scanning is an evidence pack:

- line numbers
- file hashes
- observed permission surfaces
- suspicious data-flow signals
- reproducible findings
- initial policy and report drafts

The host Agent owns the deeper semantic review:

- declared task boundary
- reasonable minimum permissions
- whether behavior is necessary, optional, excessive, or ambiguous
- whether the package is too long, too short, under-specified, or over-specified
- what constraints make it installable

## Full-Document First Pass

Before judging findings, read the package's core documents end-to-end:

- `SKILL.md`
- `README.md`
- package manifests
- workflow documents referenced by the core docs
- important scripts or configs referenced by the workflow

Do not start from finding snippets alone. Snippets tell you where to look; they do not define the task boundary.

## Semantic Boundary Extraction

After the full-document pass, write down:

- the declared user-facing task
- expected inputs
- expected outputs
- in-scope data
- out-of-scope data
- permissions that are task-critical
- permissions that are optional
- permissions that require explicit user confirmation
- permissions that are unjustified

## Dynamic Judgment Rules

Avoid hard-coded length or keyword thresholds as final judgments. Treat them as triage signals only.

A Skill may be too short when it lacks:

- clear trigger purpose
- user input assumptions
- output contract
- data boundaries
- permission expectations
- safety or consent boundaries

A Skill may be too long when it mixes:

- trigger-critical instructions
- long examples
- style libraries
- schema details
- command sequences
- troubleshooting logs
- large checklists
- deterministic procedures that should be scripts or config

Long is not always bad. Short is not always good. Judge whether the Agent can correctly activate, understand, and safely use the Skill without loading irrelevant context.

## Finding Semantics

For every deterministic finding, assign one semantic role:

- `necessary`: required for the declared task
- `acceptable_with_policy`: acceptable only if constrained by explicit policy
- `overreach`: exceeds the declared task boundary
- `likely_false_positive`: rule matched but full-context reading makes risk unlikely
- `needs_human_review`: context is insufficient or risk depends on user intent

Always explain why.
