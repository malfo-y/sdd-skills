---
name: investigate
description: "Use this skill when the user asks to \"investigate\", \"debug\", \"find root cause\", \"diagnose\", \"why is this failing\", \"track down bug\", \"근본원인 분석\", \"디버깅\", or wants systematic one-shot debugging of a specific issue. For long-running iterative debugging processes, use ralph-loop-init instead."
---

# Investigate

문제 하나의 근본 원인을 찾아 고치고, 고친 것이 맞는지 검사로 확인한다. 무엇을 어떤 순서로 조사할지는 문제에 맞게 스스로 정한다. 오래 반복해서 돌려야 하는 디버깅은 `ralph-loop-init`을 쓴다.

## Acceptance Criteria

- [ ] AC1: 근본 원인을 증거와 함께 식별했고, 증상만 가리는 수정을 하지 않았다.
- [ ] AC2: 고치기 전에 영향 범위를 확인했다.
- [ ] AC3: 고친 뒤 검사를 다시 실행해 통과를 확인했다. 실행하지 못했으면 `UNTESTED`로 보고했다.
- [ ] AC4: 처음 정한 문제 범위 밖은 고치지 않았다.

## 규칙

1. **범위를 먼저 고정한다.** 증상, 재현 조건, 기대 동작, 이미 시도했거나 배제한 가설을 대화에서 정리한다. 범위 밖에서 찾은 문제는 고치지 않고 보고에만 적는다.
2. **원인을 확인한 뒤에 고친다.** 에러 메시지, 스택, 코드 경로, 최근 변경 같은 증거로 원인을 확인하기 전에는 고치지 않는다. 가설이 여럿이면 가설을 정하지 않은 탐색도 한 번 해서, 첫 가설에 맞는 증거만 모으지 않게 한다.
3. **같은 접근이 3번 실패하면 바꾼다.** 가설, 도구, 범위 중 하나를 바꾼다.
4. **고치기 전에 영향 범위를 본다.** 바꿀 파일, 그 코드를 부르는 곳, 관련 테스트를 확인한다.
5. **고친 뒤 검사를 다시 실행한다.** 이전 실행 결과로 대신하지 않는다. `_sdd/env.md`가 있으면 그 실행 방법을 따른다. 환경 때문에 실행할 수 없으면 코드 분석 근거를 적고 `UNTESTED`로 보고하며, 테스트 통과로 적지 않는다. 이 결함을 잡는 테스트가 없었으면 회귀 테스트를 더한다.
6. **`_sdd/spec/` 파일은 만들거나 고치거나 지우지 않는다.**

## 보고

```markdown
## Investigation Report

**Problem**: [1문장 요약]
**Root Cause**: [근본원인과 근거]
**Fix**: [수정 내용 + 파일:라인]
**Blast Radius**: [영향 범위]
**Verification**: PASS / FAIL / UNTESTED
**Out-of-Scope Findings**: [범위 밖 발견사항, 있는 경우]
```

## Final Check

Acceptance Criteria를 한 번 점검한다. 실행할 수 있는 검사가 실패했거나 보완할 수 있는 누락이 있으면 고치고 다시 실행한다. 환경 제약으로 검사를 실행할 수 없으면 `UNTESTED`와 필요한 환경, 남은 검증을 보고하고 끝낸다. 같은 제약을 이유로 수정을 반복하지 않는다.
