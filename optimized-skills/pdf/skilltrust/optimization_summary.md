# Optimization Summary: pdf

This is a SkillTrust-generated optimized preview package.

## Source

- Repository: `anthropics/skills`
- Source sample and download links: see `../../manifest.json`
- GitHub stars at benchmark time: 145,914

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

Keep common PDF workflow in SKILL.md; defer form, rendering, and advanced validation details to references/scripts.

## Selection Precision Optimization

Trigger only for PDF-specific tasks; avoid competing with generic document-writing Skills.

## Important Caveat

This preview is not an official upstream release and does not claim that upstream adopted these changes. It is a reviewable SkillTrust optimization artifact intended for testing and demonstration.
