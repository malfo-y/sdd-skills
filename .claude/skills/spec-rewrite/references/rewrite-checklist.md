# Rewrite Checklist

## Shared Core Axes

- Is the rewritten body thinner than before without losing decision-bearing truth?
- Did we keep only statements that actually change repo-level or change-level judgment?
- Did we remove duplicated material that belongs in code, README, guides, or temporary specs?
- Did every retained block end up on the surface that fits it best?

## Global Spec

- Does the main body clearly state concept, boundaries, and decisions?
- Is feature-level usage/reference/validation moved out of the default body?
- Are repo-wide invariants embedded only when they truly matter?
- Are appendix and reference sections supporting rather than replacing the core?
- Did we preserve important rationale, citation, and code excerpt headers while removing low-value inventory?
- Did we move migration history, pruning justification, and other body-thickening explanation to `decision_log` or `rewrite_report`?

## Temporary Spec

- Are delta, touchpoints, implementation, and validation still explicit?
- Is validation linkage preserved?
- Are execution details kept in the temporary artifact rather than lifted into the global spec?
