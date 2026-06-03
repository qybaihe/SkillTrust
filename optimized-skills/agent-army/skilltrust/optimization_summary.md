# Optimization Summary: agent-army

This is a SkillTrust-generated optimized preview package.

## Source

- Repository: `OneWave-AI/claude-skills`
- Source sample and download links: see `../../manifest.json`
- GitHub stars at benchmark time: 169

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

Move orchestration templates and role matrices into config/references.

## Selection Precision Optimization

Rank for explicit multi-agent delegation, not ordinary task planning.

## Important Caveat

This preview is not an official upstream release and does not claim that upstream adopted these changes. It is a reviewable SkillTrust optimization artifact intended for testing and demonstration.
