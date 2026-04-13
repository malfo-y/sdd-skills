# What an SDD Spec Is

This document defines what a spec is in SDD, what the global and temporary specs are each responsible for, and which shared baseline the spec lifecycle skills must follow.

Related documents:
- [SDD_CONCEPT.md](SDD_CONCEPT.md)
- [SDD_WORKFLOW.md](SDD_WORKFLOW.md)
- [SDD_QUICK_START.md](SDD_QUICK_START.md)
- [sdd.md](sdd.md)

---

## 1. What a spec is

In SDD, a spec is a document that lets code, humans, and agents share the same judgment criteria.

A spec should answer these questions.

- What problem does this project or change solve?
- What does it own?
- What is intentionally out of scope?
- Which judgments must survive later changes?

So a spec is not the sum of all explanations. It is a document that fixes judgment.

## 2. Definition of the global spec

The global spec is the repo-wide Single Source of Truth. Its role is to fix the concepts, boundaries, and decisions that must survive over time.

Its mandatory core is only these three things.

1. Background and high-level concept
2. Scope / Non-goals / Guardrails
3. Core design and key decisions

### A. Background and high-level concept

- What is being solved
- Why this approach is used
- Which framing should be used to read the repo

### B. Scope / Non-goals / Guardrails

- Responsibility boundary
- Intentional non-goals
- Repo-wide operating rules
- Boundaries shared across features

### C. Core design and key decisions

- Structural judgments that must survive
- Decisions whose loss would create repo-level drift
- Choices that constrain extension direction

## 3. The shared core checklist axes

All spec lifecycle skills share these four checklist axes. The source of truth for those axes is this document.

1. `Thinness`
2. `Decision-bearing truth`
3. `Anti-duplication`
4. `Navigation + surface fit`

Each axis means the following.

### A. Thinness

- The global spec keeps only the minimal repo-wide core.
- The temporary spec keeps only the delta needed to execute this change.
- The body must not be thickened by details that belong on another surface.

### B. Decision-bearing truth

- Keep only statements whose falsity would change repo-level or change-level judgment.
- Code-obvious inventory and simple reference material are not mandatory body truth unless they change decisions.
- Every spec sentence should be able to answer why it must live there.

### C. Anti-duplication

- Do not restate code, README, guides, supporting docs, or temporary specs without a strong reason.
- If duplication is necessary, keep only the minimum summary that fixes judgment.
- Avoid scattering the same truth across multiple surfaces and creating drift.

### D. Navigation + surface fit

- Put information on the surface that fits it best.
- Decide first whether something belongs in the global spec, temporary spec, guide, summary, supporting docs, or code/tests.
- Readers and agents should be able to find the next surface naturally.

## 4. What does not belong in the default global core

The following may still exist, but they are not the mandatory global core.

- usage or expected-results sections
- reference information
- manual code-map appendix
- standalone contract/invariant/verification tables
- feature-level contract, validation, and expected result
- detailed inventory that can be recovered directly from code

That information should move to the surface that matches its role.

- feature execution: temporary spec
- implementation or review aid: on-demand guide
- installation or reference detail: README or separate docs
- actual behavior and detailed structure: code + tests + targeted review

## 5. How repo-wide invariants are handled

If a real repo-wide invariant is needed, keep it in the global spec. But do not force a standalone table as the default global shape.

Preferred forms:

- absorb it into guardrail wording
- keep it as a key decision that states what must stay true
- move non-shared invariants down to temporary specs or guides

Use this rule.

> Keep it in the global spec only if it is not easily recoverable from code, applies across multiple features, and would distort repo-level judgment if wrong.

## 6. Definition of the temporary spec

A temporary spec is not a compressed copy of the global spec. It is the execution blueprint for a change.

Feature-level contract, validation, touchpoints, and task sequencing belong there.

Canonical 7 sections:

1. `Change Summary`
2. `Scope Delta`
3. `Contract/Invariant Delta`
4. `Touchpoints`
5. `Implementation Plan`
6. `Validation Plan`
7. `Risks / Open Questions`

Its purpose is to handle what changes now, what gets touched, and how the change will be verified.

## 7. Information placement rules

| Information | Default home | Why |
|-------------|--------------|-----|
| project problem and framing | global spec | repo-wide judgment |
| scope / non-goals / guardrails | global spec | shared boundaries |
| core design and key decisions | global spec | long-term intent |
| reader-facing problem / motivation / design / usage narrative | `_sdd/spec/summary.md` generated by `spec-summary` | a whitepaper surface for humans grounded in the global spec and code |
| feature-level contract / validation | temporary spec | execution blueprint |
| usage examples / expected results | guide, README, temporary spec | feature or user-facing context |
| data model / API / environment detail | README or reference docs | support information |
| code map / inventory | appendix or code | on-demand navigation |

## 8. AC / Final Check mapping rules

The four shared checklist axes must be absorbed into the Acceptance Criteria and Final Check of spec lifecycle skills. Do not require a reusable `Shared Core Checklist` block.

Mapping rules:

- `Thinness`: encode it as checks that prevent the wrong surface from being inflated.
- `Decision-bearing truth`: encode it as checks that keep only statements that change judgment and reject weak or code-obvious claims.
- `Anti-duplication`: encode it as checks that reduce duplication across code, guides, README, supporting docs, and temporary specs.
- `Navigation + surface fit`: encode it as checks that move information to the right surface and verify placement, links, and path clarity.

Operating rules:

- Each skill should make those four axes self-contained through its own AC and Final Check wording.
- Skills may add one primary extra axis on top of the shared core.
- That primary extra axis sharpens the skill role. It does not replace the shared core.

Current primary extra axes:

- `spec-create`: structure rationale + `single-file default`
- `spec-review`: rubric separation + evidence strictness
- `spec-rewrite`: rationale preservation + body/log placement
- `spec-upgrade`: rewrite boundary judgment

## 9. Recommended structure

### Global Spec

```markdown
# Project Global Spec

## 1. Background and High-Level Concept
## 2. Scope / Non-goals / Guardrails
## 3. Core Design and Key Decisions

## Optional Appendix or Supporting Docs
- reference notes
- code map
- guide links
```

### Temporary Spec

```markdown
# Feature Temporary Spec

## 1. Change Summary
## 2. Scope Delta
## 3. Contract/Invariant Delta
## 4. Touchpoints
## 5. Implementation Plan
## 6. Validation Plan
## 7. Risks / Open Questions
```

## 10. What this means for skills

- `spec-create`: create a thin global spec that satisfies the four shared core axes. The default shape is a single `_sdd/spec/main.md` file, and splitting is allowed only when navigation + surface fit provides a written rationale.
- `spec-review`: apply the rubric that matches the spec type. Feature-level contamination in a global spec is `Quality` by default, and becomes `Critical` only when it creates document-type confusion or wrong repo-wide truth. Every finding must carry spec, code, or doc evidence, and weakly supported claims should stay `UNTESTED`.
- `spec-summary`: write `_sdd/spec/summary.md` as a reader-facing whitepaper. It should explain the problem, background or motivation, why this approach was chosen over alternatives, core design, code grounding, usage or expected results, and deeper reading surfaces. It should read like a technical whitepaper rather than a status memo, with a short appendix only when relevant draft or implementation signals exist.
- `spec-rewrite`: restructure the spec so the four shared core axes are more visible. Preserve rationale, citations, and code excerpt headers while moving migration history and execution-log style explanations out of the body and into `decision_log` or the rewrite report.
- `spec-upgrade`: migrate a legacy spec to the current model. If the real need is structural redesign, large repartitioning, or role rebundling, branch to `spec-rewrite` instead of stretching upgrade.
- generator, planner, and update skills must not reconstruct a thicker global spec by default.
- guides are companion surfaces, not authoritative spec layers.

## 11. Declaration

In SDD, the global spec is the declaration that fixes repo-wide judgment.

In SDD, the temporary spec is the concrete execution blueprint for a change.

They do not replace each other, and support information is delegated to code, guides, README, and reference docs.
