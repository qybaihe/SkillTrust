# Host-Agent Semantic Review And Fusion

Use this when generating or reviewing `semantic_review_request.json`, `semantic_review.json`, or fused outputs.

## Role Split

Deterministic scanner:

- collects reproducible evidence
- records line numbers and hashes
- finds suspicious permission surfaces
- drafts policy and reports

Host Agent:

- reads core documents fully
- understands the package's intent
- judges whether each permission is necessary
- dynamically evaluates authoring quality and package scope
- recommends policy refinements and final install action

## Required Reading

The Agent must read all core documents listed in the review request before judging individual findings.

Record:

- document path
- hash
- read scope
- boundary notes
- uncertainties

## Fusion Rules

- Deterministic findings remain visible.
- Semantic review can lower display priority but cannot delete evidence.
- Critical data-flow evidence stays protected.
- Semantic review can make the final action stricter.
- Semantic review can explain why a deterministic finding is likely benign, but the final output must preserve the audit trail.

## Dynamic Review Additions

The semantic review should also assess:

- whether the package is under-specified
- whether the package is over-specified
- whether long instructions should move to references
- whether repeated deterministic logic should become scripts or config
- whether names and descriptions are clear enough for correct Agent routing

These are semantic judgments. Do not rely on a fixed length threshold alone.
