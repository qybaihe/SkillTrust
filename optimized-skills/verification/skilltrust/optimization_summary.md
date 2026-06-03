# Optimization Summary: verification

This is a SkillTrust-generated optimized preview package.

## Source

- Repository: `Aurite-ai/agent-verifier`
- Source sample and download links: see `../../manifest.json`
- GitHub stars at benchmark time: 39

## What Changed

- Converted the package into a compact, intent-bound `SKILL.md` preview.
- Added an explicit minimal permission contract.
- Added confirmation gates for high-impact actions.
- Added denied-by-default boundaries for unrelated secrets, credential stores, broad filesystem access, and unapproved external writes.
- Added token and selection-precision optimization notes.

## Original Gate

`allow`

## Optimized Preview Posture

`allow-with-policy`

## Token Optimization

Move repeated severity schema and report templates into references/config.

## Selection Precision Optimization

Use as orchestrator; delegate to specialized verify-* Skills rather than competing with them.

## Important Caveat

This preview is not an official upstream release and does not claim that upstream adopted these changes. It is a reviewable SkillTrust optimization artifact intended for testing and demonstration.
