---
name: investigate
description: "Use this skill when the user asks to \"investigate\", \"debug\", \"find root cause\", \"diagnose\", \"why is this failing\", \"track down bug\", \"근본원인 분석\", \"디버깅\", or wants systematic one-shot debugging of a specific issue. For long-running iterative debugging processes, use ralph-loop-init instead."
version: 1.0.0
---

# Investigate -- Systematic Debugging

범용 체계적 디버깅 스킬. 증상이 아닌 근본원인을 찾아 수정하고, 수정이 올바른지 검증한다.

> ralph-loop-init과 차별화: investigate는 범용/단발 디버깅, ralph-loop-init은 장시간 반복 프로세스 전용.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: 근본원인이 식별되었다 (증상 패치가 아닌 원인 수정)
- [ ] AC2: 수정 후 테스트가 통과한다 (Fresh Verification)
- [ ] AC3: 수정 영향 범위(blast radius)가 사전 평가되었다
- [ ] AC4: 초기 범위를 벗어나는 수정이 없다 (scope lock)

## Hard Rules

1. **근본원인 우선 (Iron Law)**: 증상 패치 금지. 근본원인을 찾아 수정한다.
2. **3-Strike Escalation**: 같은 접근 3회 실패 시 전략을 변경한다 (다른 가설, 다른 도구, 다른 범위).
3. **Scope Lock**: 초기 범위(사용자가 지정한 문제)를 벗어나는 수정 금지. 발견한 추가 이슈는 리포트에 기록만 한다.
4. **Blast Radius Gate**: 수정 전 영향 범위를 평가한다. 변경 파일 수, 의존하는 모듈, 관련 테스트를 나열하고 수정을 진행한다.
5. **Fresh Verification**: 수정 후 반드시 테스트를 재실행한다. 이전 결과 재사용 금지. `_sdd/env.md` 미존재 시 코드 분석 기반 검증을 허용하되, 리포트에 `UNTESTED` 표기.
6. **Spec 파일 불가침**: `_sdd/spec/` 하위 파일을 생성/수정/삭제하지 않는다.

## Process

### Step 1: Problem Definition

1. 사용자 입력에서 증상, 재현 조건, 기대 동작을 추출한다.
2. `_sdd/env.md` 존재 시 환경 설정을 적용한다.
3. 문제 범위를 확정하고 기록한다 (scope lock 기준).

### Step 2: Evidence Collection

`Grep`, `Glob`, `Read`, `Bash`로 증거를 수집한다:
- 에러 메시지, 스택 트레이스, 로그
- 관련 코드 경로, 최근 변경 이력 (`git log`, `git diff`)
- 관련 테스트 파일/결과

### Step 3: Hypothesis & Cross-Verification

1. **가설 수립**: 수집된 증거(에러 메시지, 스택 트레이스, 코드 변경 이력)로 근본원인 가설을 세운다.
2. **독립 코드 분석**: 가설과 무관하게 관련 코드를 독립적으로 읽어 이상을 탐지한다 (앵커링 바이어스 방지).
3. **교차 검증**: 가설 기반 결론과 독립 분석 결론을 비교한다. 불일치 시 추가 증거를 수집한다.
4. **3-Strike 적용**: 같은 가설/접근이 3회 실패하면 즉시 전략을 변경한다 (다른 가설, 다른 범위, 다른 도구).

> 단순한 문제(에러 메시지가 명확, 단일 파일 관련)에서는 교차 검증을 생략하고 직접 수정으로 진행할 수 있다.

### Step 4: Blast Radius Assessment

수정 대상 파일과 영향 범위를 평가한다:
- 변경 파일 목록
- 의존하는 모듈/함수 (`Grep`으로 import/호출 검색)
- 관련 테스트 목록

### Step 5: Fix & Verify

1. 근본원인을 수정한다.
2. 테스트를 재실행하여 수정을 검증한다.
3. 기존 테스트가 실패하면 회귀 방지 테스트를 추가한다.

### Step 6: Report

```markdown
## Investigation Report

**Problem**: [1문장 요약]
**Root Cause**: [근본원인]
**Fix**: [수정 내용 + 파일:라인]
**Blast Radius**: [영향 범위]
**Verification**: PASS / FAIL / UNTESTED
**Out-of-Scope Findings**: [범위 밖 발견사항, 있는 경우]
```

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
