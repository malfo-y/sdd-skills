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

Temporary spec은 change 실행 청사진이다. exact structure와 field order는 same-runtime `feature-draft`의 `Required Output`이 소유한다. temporary 또는 mixed 문서의 temporary portion을 비교할 때 해당 section과 연결된 조건부 block·분할 규칙을 읽는다. 위치 확인과 미가용 시 처리는 `SKILL.md` Step 3을 따른다.
