# Optimization Summary: cursor-rules-awesome / installer-package

This is a SkillTrust-generated optimized preview package.

## Source

- Repository: `tonynguyennvt/cursor-rules-awesome`
- Source sample and download links: see `../../manifest.json`
- GitHub stars at benchmark time: 4

## What Changed

- Converted the package into a compact, intent-bound `SKILL.md` preview.
- Added an explicit minimal permission contract.
- Added confirmation gates for high-impact actions.
- Added denied-by-default boundaries for unrelated secrets, credential stores, broad filesystem access, and unapproved external writes.
- Added token and selection-precision optimization notes.

## Original Gate

`warn`

## Optimized Preview Posture

`warn-until-semantic-review-and-policy-approval`

## Token Optimization

Move installer behavior into explicit init policy and short setup checklist.

## Selection Precision Optimization

Rank only for installing Cursor rules, not using rules during coding.

## Important Caveat

This preview is not an official upstream release and does not claim that upstream adopted these changes. It is a reviewable SkillTrust optimization artifact intended for testing and demonstration.
