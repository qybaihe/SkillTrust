# Reporting

Use this when writing the final answer to the user.

## Summary Shape

Prefer:

- outcome
- key evidence
- semantic interpretation
- install recommendation
- safest next step
- report locations

Avoid overwhelming the user with raw logs or long command output.

## Explain The Hybrid Model

Say clearly:

- code collected evidence
- the Agent read and interpreted the package
- findings were preserved
- final recommendations are intent-bound
- no external model API or API key was required

## Local Audit Summary

For portfolio audits, include:

- total packages
- allow / warn / block counts
- top risks
- blocked packages
- packages needing policy overlay
- packages needing authoring, token, or taxonomy optimization
- whether any action requires user approval

## Single Package Summary

For one package, include:

- declared task boundary
- necessary permissions
- observed behavior
- overreach or mismatch
- semantic caveats
- final action: `allow`, `warn`, or `block`
- policy and remediation recommendations
