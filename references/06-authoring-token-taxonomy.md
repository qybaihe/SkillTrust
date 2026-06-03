# Authoring, Token Efficiency, And Taxonomy

Use this when the user asks whether a Skill or Agent package is too long, too short, inefficient, ambiguous, or poorly routed.

## Dynamic Authoring Review

Do not judge length by a single number. Length is a signal, not a verdict.

Judge whether the package gives the Agent:

- enough context to activate correctly
- enough boundaries to avoid unsafe behavior
- enough workflow detail to complete the task
- too much irrelevant context at activation time
- too many examples that should be deferred
- too much deterministic procedure that should become code or config

## Too Short Signals

The package may be too short if it lacks:

- purpose
- trigger scenarios
- expected inputs and outputs
- scope boundaries
- permission assumptions
- safety constraints
- reference navigation

## Too Long Signals

The package may be too long if it includes:

- long tutorials
- style galleries
- many examples
- repeated command sequences
- schemas and validators
- troubleshooting trees
- deterministic parsing or rendering steps
- large domain references loaded at activation

## Reference Split Rules

Keep `SKILL.md` as a compact harness:

- trigger purpose
- when to use it
- high-level workflow
- safety boundary pointer
- reference navigation

Move deeper material into references:

- detailed workflow variants
- schemas
- examples
- domain rules
- troubleshooting
- style guides
- evaluation rubrics

## Token Efficiency

Prefer scripts, config, or schemas for:

- validation checklists
- repeated command sequences
- deterministic transforms
- routing tables
- output format validation
- parse/convert/render/export flows

## Taxonomy

Assess whether name and description help the Agent choose the right package.

Watch for:

- generic names
- overlapping descriptions
- duplicate trigger terms
- mismatched folder and frontmatter names
- namespace collisions
- missing differentiators between related Skills
