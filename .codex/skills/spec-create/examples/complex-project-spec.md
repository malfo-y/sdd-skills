# Platform Global Spec

**Version**: 1.0.0
**Last Updated**: 2026-04-04
**Status**: In Review

## 1. 배경 및 high-level concept

이 플랫폼은 여러 ingestion job을 같은 운영 규칙 아래에서 관리하는 것을 목표로 한다. repo를 읽는 기본 관점은 "공통 운영 경계는 global spec에, feature execution detail은 temporary artifact에"다.

## 2. Scope / Non-goals / Guardrails

### In Scope
- 공통 운영 경계
- shared scheduling assumptions
- cross-cutting failure handling

### Non-goals
- 모든 잡의 세부 사용법 설명
- 각 도메인별 validation 절차를 global에 수록

### Guardrails
- repo-wide 운영 규칙만 global에 남긴다.
- feature-level contract/validation은 domain temp spec 또는 guide로 보낸다.

## 3. 핵심 설계와 주요 결정

- central orchestration과 domain logic를 분리한다.
- decision drift를 막기 위해 repo-wide rules는 명시하되, feature detail은 supporting surface로 분리한다.
- code-obvious inventory는 문서 기본 본문에 복제하지 않는다.

## Optional Supporting Notes

### Supporting References
- README.md
- docs/operations.md
