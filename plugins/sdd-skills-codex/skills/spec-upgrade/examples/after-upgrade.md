# Example Project Global Spec

**Version**: 1.0.0
**Last Updated**: 2026-05-22
**Status**: Draft

## 1. Background and High-Level Concept

이 repo는 여러 feature를 공통 운영 규칙 아래에서 다루기 위한 thin global decision layer를 제공한다. 업그레이드 후 global spec은 프로젝트의 문제 정의, 책임 경계, 장기 설계 판단만 고정한다.

## 2. Scope / Non-goals / Guardrails

### In Scope

- repo-wide 경계와 공통 운영 규칙
- 장기적으로 유지해야 하는 설계 결정

### Non-goals

- feature별 사용법 복제
- endpoint별 validation detail 수록
- 전수형 파일 inventory 유지

### Guardrails

- global은 repo-wide 경계만 다룬다.
- feature execution detail은 temporary spec 또는 guide로 보낸다.
- code-obvious detail은 코드나 supporting surface에 둔다.

## 3. Core Design and Key Decisions

### Core Design

- global spec은 `개념 + 경계 + 결정`만 기본 코어로 유지한다.
- feature-level execution detail은 `_sdd/drafts/`, `_sdd/implementation/`, guide surface로 분리한다.

### Key Decisions

- repo-wide invariant가 필요하면 guardrail 또는 key decision wording으로 남긴다.
- legacy file inventory는 삭제하거나 supporting surface로 내린다.
- navigation-critical hint만 compact `Strategic Code Map`으로 보존한다.

## Optional Supporting Notes

### Strategic Code Map

| Change Path / Area | Start Here | Contract / Hotspot | Validation Surface | Why |
|--------------------|------------|--------------------|--------------------|-----|
| Core workflow | `src/main.py` | `src/contracts.py` | `tests/test_workflow.py` | repo-wide 흐름과 contract 판단이 모이는 시작점이다. |

긴 map이나 per-path 설명이 필요하면 `_sdd/spec/components.md` 또는 `_sdd/spec/code-map.md` 같은 supporting surface로 분리한다.

### Supporting References

- README.md
- docs/architecture.md
