# Example: After Upgrade (Current Canonical Model)

이 예시는 `before-upgrade.md`의 구 형식 스펙을 현재 SDD canonical global spec model로 마이그레이션한 결과다. old inventory-heavy structure를 얇은 글로벌 스펙 + explicit CIV + decision-bearing structure + appendix code map으로 바꿨다.

---

# TaskRunner

> YAML로 정의한 태스크를 의존성 순서에 따라 실행하는 CLI 도구

**Version**: 1.0.0
**Last Updated**: 2026-04-04
**Status**: Approved

## 1. 배경 및 high-level concept

반복적인 빌드, 테스트, 배포 태스크는 의존 관계를 가진다. 단순 스크립트로는 순서와 병렬화 규칙이 암묵적으로 흩어지고, 실행 결과 추적도 어렵다.

TaskRunner의 high-level concept는 "태스크 실행을 선언 -> 정렬 -> 실행 -> 기록의 네 단계로 분리해, 정의와 실행 정책을 명시적으로 고정한다"는 것이다.

## 2. Scope / Non-goals / Guardrails

### In Scope

- YAML 기반 태스크 정의
- 의존성 기반 실행 순서 계산
- 병렬 실행
- 실행 결과 로깅

### Non-goals

- 분산 워커 스케줄링
- UI 대시보드
- 장기 실행 job orchestration

### Guardrails

- 순환 의존성은 실행 전에 감지되어야 한다.
- 실행 순서 결정과 실제 실행 엔진은 같은 책임을 가지면 안 된다.

## 3. 핵심 설계와 주요 결정

TaskRunner는 파싱, 스케줄링, 실행, 로깅을 하나의 거대한 CLI 함수로 두지 않는다. 대신 각 단계를 분리해 테스트 가능성과 정책 교체 가능성을 확보한다.

| Decision | Why | What Must Stay True |
|----------|-----|---------------------|
| Parser / Scheduler / Executor / Logger 분리 | 입력 형식과 실행 정책을 독립적으로 바꾸기 위해 | CLI는 orchestration만 담당 |
| Scheduler가 병렬 그룹을 계산 | execution engine이 의존성 해석 책임을 가지지 않도록 | dependency ordering contract가 scheduler에 고정 |

## 4. Contract / Invariants / Verifiability

### Contract

| ID | Subject | Inputs/Outputs | Preconditions | Postconditions | Failure Guarantees |
|----|---------|----------------|---------------|----------------|--------------------|
| C1 | Parse task file | YAML file -> TaskGraph | 입력 파일이 유효한 YAML이어야 한다 | 실행 가능한 TaskGraph가 생성된다 | invalid spec이면 실행 전에 실패한다 |
| C2 | Build execution groups | TaskGraph -> ordered task groups | 그래프에 순환이 없어야 한다 | dependency-safe group sequence가 생성된다 | 순환 존재 시 실행을 시작하지 않는다 |
| C3 | Execute groups | ordered task groups -> execution result | scheduler output이 유효해야 한다 | 각 그룹이 순서대로 실행된다 | 실패 결과가 로그에 남는다 |

### Invariants

| ID | Scope | Invariant | Why It Matters |
|----|-------|-----------|----------------|
| I1 | Scheduling | dependency가 있는 task는 선행 task보다 먼저 실행되면 안 된다 | 실행 의미 보존 |
| I2 | Logging | 실행 결과는 성공/실패와 관계없이 기록된다 | 운영 추적성 확보 |

### Verifiability

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1 | test | YAML parsing 및 validation 테스트 |
| V2 | C2, I1 | test, review | topological sort와 cycle detection 검증 |
| V3 | C3, I2 | review | execution -> log write 연결 리뷰 |

## 5. 사용 가이드 & 기대 결과

### Scenario: 기본 실행

**Setup**: 사용자가 YAML task file을 준비한다.

**Action**: `taskrunner run tasks.yaml`

**Expected Result**: dependency-safe 순서로 task group이 실행되고, 결과가 로그에 기록된다.

## 6. Decision-bearing structure

- 시스템 경계: task definition, ordering, execution, logging까지를 포함한다.
- ownership: Parser는 input contract, Scheduler는 ordering contract, Executor는 run contract를 담당한다.
- cross-component contract: Scheduler output은 Executor가 그대로 소비할 수 있는 group sequence여야 한다.
- extension point: alternate task file format, alternate execution backend
- invariant hotspot: `topological_sort`, execution-to-log handoff

## 7. 참조 정보

### Data Models

- `Task`
- `TaskGraph`
- `ExecutionResult`

### Environment & Dependencies

- Python 3.11
- Click
- PyYAML
- asyncio

## Appendix A. Strategic Code Map

| Kind | Path / Symbol | Why It Matters |
|------|----------------|----------------|
| Entrypoint | `src/cli.py:run` | CLI orchestration 진입점 |
| Invariant Hotspot | `src/scheduler.py:topological_sort` | dependency ordering invariant 핵심 |
| Change Hotspot | `src/executor.py:execute` | parallel execution policy 핵심 |
| Change Hotspot | `src/logger.py:log` | execution result persistence 경계 |
