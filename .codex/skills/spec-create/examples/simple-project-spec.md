# Demo Project Global Spec

**Version**: 0.1.0
**Last Updated**: 2026-04-04
**Status**: Draft

## 1. 배경 및 high-level concept

작은 내부 도구 저장소에서 반복되는 수동 배치 작업을 줄이는 것이 목표다. 이 repo는 작업 정의를 얇은 선언형 입력으로 받고, 실행 책임은 코드와 런타임에 둔다.

## 2. Scope / Non-goals / Guardrails

### In Scope
- 배치 작업 정의와 실행 entrypoint
- 공통 실패 처리 규칙

### Non-goals
- 범용 워크플로우 엔진화
- 사용자별 UI 제공

### Guardrails
- repo-wide retry 정책은 중앙 실행기에서만 결정한다.
- feature별 실행 detail은 global spec이 아니라 code와 temporary spec에 둔다.

## 3. 핵심 설계와 주요 결정

- global spec은 thin decision memo로 유지한다.
- 배치 정의 파싱과 실행은 분리한다.
- repo-wide invariant가 필요한 경우 guardrail wording으로 남긴다.
