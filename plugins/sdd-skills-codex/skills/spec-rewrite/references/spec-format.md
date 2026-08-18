# Spec Format Reference

## Global Spec Core

| Order | Section | Required |
|------|---------|----------|
| 1 | Background & High-Level Concept | Yes |
| 2 | Scope / Non-goals / Guardrails | Yes |
| 3 | Core Design & Key Decisions | Yes |

Optional support layers:

- reference information
- appendix-level code map
- guide links
- repo-wide invariant wording embedded in guardrails or key decisions

Global anti-patterns:

- feature-level usage guide in main body
- feature-level contract/validation in main body
- exhaustive architecture/component inventory as default structure
- code-obvious explanation copied into the spec

## Temporary Spec Reference

Temporary spec은 change 실행 청사진이다. exact structure, optional block trigger, field order, rolling split rule의 단일 소스는 `template-compact.md`의 `Temporary Spec Target Shape`다. target이 temporary spec이거나 mixed 문서의 temporary portion을 비교할 때 그 section을 읽는다.
