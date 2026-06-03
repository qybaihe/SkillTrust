# Optimization Summary: mcp-builder

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

`warn`

## Optimized Preview Posture

`warn-until-semantic-review-and-policy-approval`

## Token Optimization

Keep server-type routing in the Skill; move Node/Python templates, evaluation checklists, and best practices into references/scripts.

## Selection Precision Optimization

Rank for MCP server-building tasks only; avoid triggering on generic API docs or package setup.

## Important Caveat

This preview is not an official upstream release and does not claim that upstream adopted these changes. It is a reviewable SkillTrust optimization artifact intended for testing and demonstration.
