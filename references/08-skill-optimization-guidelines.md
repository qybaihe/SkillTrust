# Skill Optimization Guidelines

Use this reference when SkillTrust or a host Agent turns an uploaded Skill into an optimized preview package.

The goal is not to make a Skill look safe. The goal is to make it more useful under an auditable, least-privilege boundary:

- fewer activation tokens
- faster and more deterministic execution
- higher Agent selection accuracy
- clearer permissions and policy gates
- reviewable artifacts that do not auto-install

## Core Optimization Loop

1. Read the original `SKILL.md` and core references.
2. Run deterministic SkillTrust analysis and preserve every finding.
3. Identify what the Skill truly needs to do its declared task.
4. Move deterministic logic into code, schemas, or config.
5. Shorten the activation harness without deleting safety boundaries.
6. Add direct reference navigation for details that are not always needed.
7. Generate a preview package with policy overlays and an optimization summary.
8. Keep all source edits reviewable; never install automatically.

## Token Efficiency

A good Skill should not load all of its knowledge on every activation.

Prefer:

- short trigger and scope description
- concise workflow skeleton
- direct links to one-level references
- examples loaded only when needed
- schemas and config for repeated structure
- scripts for deterministic transforms

Avoid:

- long tutorials in `SKILL.md`
- repeated examples that the Agent does not need for routing
- giant style galleries at activation time
- full troubleshooting trees in the main harness
- tables that could be config

## Execution Efficiency

A good Skill should use model reasoning for judgment, not for repeating deterministic machinery.

Move these into scripts, schemas, or config:

- validation checklists
- output field contracts
- parsing, conversion, rendering, export, and download steps
- command sequences with fixed order
- routing tables and decision matrices
- filename/path normalization
- report or artifact packaging

Keep these in `SKILL.md`:

- when to use the Skill
- safety boundaries
- user-facing tradeoffs
- judgment rules that require context
- what references to read for each variant

## Selection Accuracy

The host Agent should be able to choose the Skill quickly and correctly.

Improve:

- `name`: short, specific, hyphen-case
- `description`: trigger-oriented, with clear inputs and outputs
- boundaries: when not to use the Skill
- neighbor routing: which nearby Skill handles adjacent tasks
- first heading: aligned with the Skill's actual job

Watch for:

- generic names such as `assistant`, `helper`, or `tool`
- descriptions that overlap with many other Skills
- missing frontmatter
- a folder name that conflicts with the declared name
- broad claims that exceed the actual workflow

## Permission Governance

The optimized Skill package must stay intent-bound.

Include:

- `skilltrust/permission_manifest.json`
- `skilltrust/skilltrust-policy.json`
- `skilltrust/optimization_summary.md`
- `skilltrust/skill_optimization_plan.json`

Preserve:

- deterministic findings
- sensitive data-flow warnings
- denied-by-default credential paths
- denied unrelated network sinks
- human confirmation gates for risky actions

Never:

- delete evidence to make a package look like `allow`
- convert a critical data-flow finding into safe wording
- auto-install the optimized preview package
- read unrelated user secrets while optimizing

## Agent-Assisted Rewrite Standard

When an AI reviewer rewrites a Skill, it should optimize for measurable outcomes:

- activation body tokens before and after
- number of deterministic steps moved to scripts/schemas/config
- number of direct references with read-when-needed conditions
- final `allow`, `warn`, or `block` decision
- policy gates included in the preview package

The reviewer may downgrade presentation priority for a likely false positive, but it must not remove the original finding.
