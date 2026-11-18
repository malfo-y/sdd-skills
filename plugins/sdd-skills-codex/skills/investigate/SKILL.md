---
name: investigate
description: "Use this skill when the user asks to \"investigate\", \"debug\", \"find root cause\", \"diagnose\", \"why is this failing\", \"track down bug\", \"근본원인 분석\", \"디버깅\", or wants systematic one-shot diagnosis or an explicitly authorized fix for a specific issue. For long-running iterative debugging processes, use ralph-loop-init instead."
---

# Investigate

문제 하나의 근본 원인을 증거로 확인한다. 사용자가 수정을 요청했을 때만 고치고, 고친 것이 맞는지 검사로 확인한다. 무엇을 어떤 순서로 조사할지는 문제에 맞게 스스로 정한다. 오래 반복해서 돌려야 하는 디버깅은 `ralph-loop-init`을 쓴다.

## Acceptance Criteria

- [ ] AC1: 근본 원인을 증거와 함께 식별했다. 근거가 부족하면 `UNCONFIRMED`로 보고했다.
- [ ] AC2: diagnose-only에서는 제품·소스·spec 수정과 회귀 테스트 추가가 0건이다.
- [ ] AC3: fix에서는 고치기 전에 영향 범위를 확인했고, 고친 뒤 검사를 다시 실행했다. 실행하지 못했으면 `UNTESTED`로 보고했다.
- [ ] AC4: 처음 정한 문제 범위 밖은 분석하거나 고치지 않았다.

## 모드

- **diagnose-only**가 기본이다. `investigate`·`debug`·`diagnose`·원인 설명 요청은 여기에 든다. 진단 보고서를 파일로 써 달라는 요청도 제품 수정 권한이 아니다.
- **fix**는 조사 대상의 `fix`·`repair`·`patch`·`수정해줘`·`고쳐줘`를 명시적으로 요청했거나, 진단 뒤에 사용자가 수정을 승인했을 때다. 승인 뒤에는 모은 증거를 그대로 쓰고 fix로 넘어간다. 권고만으로 쓰기 권한을 추론하지 않는다.
- diagnose-only에서는 제품·소스·spec 파일을 만들거나 고치거나 지우지 않고 회귀 테스트도 더하지 않는다. 상위 repo 규칙이 강제하는 기록(work log 등)만 예외다. 그 규칙이 정한 최소 대상에 그 규칙의 방식대로 쓰고(덧붙이기 규칙이면 기존 내용을 보존하고 덧붙인다), 보고에 밝힌다.

## 규칙

1. **범위를 먼저 고정한다.** 증상, 재현 조건, 기대 동작, 이미 시도했거나 배제한 가설을 대화에서 정리한다. 범위 밖에서 찾은 문제는 고치지 않고 보고에만 적는다.
2. **원인을 증거로 확인한다.** 에러 메시지, 스택, 코드 경로, 최근 변경 같은 증거로 확인한다. fix 요청을 받았어도 원인을 확인하기 전에는 고치지 않고, 확인하지 못하면 `UNCONFIRMED`로 보고한다. 가설이 여럿이면 가설을 정하지 않은 탐색도 한 번 해서, 첫 가설에 맞는 증거만 모으지 않게 한다.
3. **같은 접근이 3번 실패하면 바꾼다.** 가설, 도구, 범위 중 하나를 바꾼다.
4. **영향 범위를 본다.** 관련 파일, 그 코드를 부르는 곳, 관련 테스트를 확인한다. diagnose-only에서는 영향 범위와 권고만 적는다. fix에서는 바꿀 파일을 정한 뒤에 고친다.
5. **fix에서는 고친 뒤 검사를 다시 실행한다.** 이전 실행 결과로 대신하지 않는다. `_sdd/env.md`가 있으면 그 실행 방법을 따른다. 환경 때문에 실행할 수 없으면 코드 분석 근거를 적고 `UNTESTED`로 보고하며, 테스트 통과로 적지 않는다. 이 결함을 잡는 테스트가 없었으면 회귀 테스트를 더한다.
6. **두 모드 모두 `_sdd/spec/` 파일은 만들거나 고치거나 지우지 않는다.**

## 보고

필드 이름을 그대로 쓰고, 고른 모드의 값 하나만 적는다.

```markdown
## Investigation Report

**Mode**: diagnose-only | fix
**Problem**: [1문장 요약]
**Root Cause**: [근본원인]
**Evidence**: [근본원인 근거]
**Fix**: [모드에 맞는 값]
**Impact / Blast Radius**: [영향 범위]
**Verification**: [모드에 맞는 값]
**Governance Writes**: None | [상위 repo 규칙이 강제한 기록]
**Out-of-Scope Findings**: [범위 밖 발견사항, 있는 경우]
```

| Mode | Fix | Verification |
| --- | --- | --- |
| diagnose-only | `Not applied (diagnose-only)` | `CONFIRMED` 또는 `UNCONFIRMED` |
| fix | 수정 내용 + 파일:라인 | `PASS`, `FAIL`, 또는 `UNTESTED` |

## Final Check

고른 모드에 해당하는 Acceptance Criteria를 한 번 점검한다. diagnose-only에는 AC3를, fix에는 AC2를 적용하지 않는다. 보완할 수 있는 누락은 고치고, 환경 제약으로 검사를 실행할 수 없으면 `UNTESTED`와 필요한 환경, 남은 검증을 보고하고 끝낸다.
