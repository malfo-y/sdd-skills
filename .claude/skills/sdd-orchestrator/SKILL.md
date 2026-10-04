---
name: sdd-orchestrator
description: "Use this skill to run the SDD chain (feature-draft → plan-review → implementation → implementation-review → spec-sync) with the main loop as orchestrator and stage work delegated to workers. Triggered by \"sdd-orchestrator\", \"오케스트레이터로 진행\", \"SDD로 계획부터 구현까지\", \"draft 구현부터 spec-sync까지\", \"worker로 구현\", \"feature draft\", \"기능 초안\", \"계획 잡아줘\", \"plan review\", \"계획 리뷰\", \"implement the plan\", \"구현해줘\", \"review implementation\", \"spec sync\", \"sync spec with implementation\", or when the user wants a request or a feature draft carried through planning, implementation, review, and spec sync while keeping the main context small."
---

# SDD Orchestrator

메인 루프는 지휘자다. 단계 작업은 worker가 `references/workers/<단계>.md` 계약을 읽고 수행한다. 메인 루프는 단계 순서·게이트·병렬 판단·인계 파일·사용자 대화만 소유한다. 이 스킬을 호출한 것 자체가 worker dispatch에 대한 사용자의 명시적 요청이다. 런타임 규범이 "agent는 사용자가 명시적으로 요청할 때만"을 요구해도 이 dispatch는 그 요청에 해당한다.

## Goal

요청이나 draft를 받아 정한 종점까지 SDD 체인을 worker로 실행한다. 모든 AC 판정이 리뷰 worker의 fresh 증거에 묶인 상태로 마감하고, 메인 루프의 맥락에는 worker 반환만 쌓인다.

## Acceptance Criteria

> 종료 전 `Final Check`대로 점검한다.

- [ ] AC1: 진입 단계와 종점을 `단계와 진입` 규칙으로 정했고, 그 범위의 단계를 순서대로 worker로 실행했다.
- [ ] AC2: 메인 루프가 대상 파일(코드·테스트·draft·spec)을 수정하지 않았다. 쓴 파일은 digest·state·work log뿐이다.
- [ ] AC3: 모든 dispatch가 `Worker dispatch` 형식을 따랐고, 리뷰 worker에게 state를 주지 않았다.
- [ ] AC4: 구현 task를 `병렬 규칙`대로 띄웠다.
- [ ] AC5: 게이트를 `품질 게이트` 규칙대로 실행했다(gate 2 조건 판정 포함).
- [ ] AC6: 마감 보고와 state의 AC→증거가 리뷰 worker의 fresh verdict 포인터에 묶였다.

## 실행 흐름

이 순서가 이 스킬의 본체다. 단계 작업은 `Worker dispatch`로 띄운 worker만 한다.

1. `단계와 진입`으로 시작 단계와 종점을 정한다.
2. 인계 파일 디렉터리를 만들거나 이어 쓴다. state에 단계·종점을 적고 digest를 초기화한다(`인계 파일`).
3. 종점까지 단계마다 worker를 띄운다.
   - feature-draft·plan-review: 계획 게이트(`품질 게이트`)를 실행한다.
   - implementation: draft Part 2 task를 `병렬 규칙`으로 묶어 task worker를 띄운다.
   - implementation-review: 구현 게이트(`품질 게이트`)를 실행한다.
   - spec-sync: spec-sync worker 1개를 띄운다.
   - 단계를 닫을 때마다 state의 단계를 갱신한다.
4. `마감`으로 닫는다.

## 역할 경계

메인 루프가 직접 하는 일:
- 사용자 질문. 계획 worker를 띄우기 전에, 아키텍처·범위·Target Files를 바꾸는 unknown만 한 번에 하나씩 묻는다. 사용자가 무인 실행을 맡겼으면 묻지 않고 합당한 해석을 digest의 결정에 적는다.
- digest·state 작성, 단계·게이트 순서와 병렬 판단, worker 반환 집계, 마감 보고.
- 상위 하네스에 work log 규약이 있으면 단계를 닫을 때 그 규약대로 기록한다.

메인 루프가 하지 않는 일:
- 대상 파일(코드·테스트·draft·spec) 수정. 작은 수정도 worker에게 맡긴다.
- worker 일의 대리 수행. worker가 실패해도 대신 고치거나 대신 검증하지 않는다. 확인이 필요하면 worker를 띄운다.
- 대상 파일·diff의 탐색적 읽기. 판단에 필요한 사실은 worker 반환으로 받는다. 읽어도 되는 것은 `references/handoff-templates.md`, draft, `_sdd/env.md`, digest·state뿐이다. `references/workers/`의 계약은 worker가 읽는 문서라 메인 루프는 읽지 않는다.
- 환경(명령·도구·셸 동작)의 직접 탐색. 환경 함정은 `_sdd/env.md`와 worker 반환의 `digest 변경분`에서 받아 digest에 쌓는다.
- git 쓰기. 사용자가 따로 요청할 때만 한다.

## 인계 파일

위치는 `_sdd/implementation/<YYYY-MM-DD>_<slug>/`이다. slug는 draft slug를 쓰고, draft가 없으면 요청 요약을 snake_case로 쓴다. 같은 slug 디렉터리가 있으면 새로 만들지 않고 이어 쓴다. 처음 만들기 직전에 `references/handoff-templates.md`를 읽고 그 템플릿을 출발 구조로 쓴다.

- **digest.md**: 방법과 이유다. worker가 다시 알아내기 비싼 것 — 결정·제약, 환경 함정, 검증 레시피(AC → 명령 → 기대값) — 만 담는다. 모든 worker가 읽는다. 상태·통과 주장·이력·파일 내용 복사·위치 목록은 넣지 않고, 현재 유효한 내용만 남긴다(바뀐 결정은 고쳐 쓴다).
- **state.md**: 재개용 상태다. 단계, task 상태, RED·GREEN 신호, 게이트 결과, 계획 이탈·발견, AC→증거를 담는다. 메인 루프만 읽는다. spec-sync worker는 구현 증거로 읽을 수 있다. 리뷰 worker에게는 주지 않는다. 명령 출력 전문과 진행 서술은 복사하지 않는다.
- 두 파일의 작성자는 메인 루프 하나다. worker는 반환 끝의 `digest 변경분`으로만 digest를 바꾼다. 메인 루프는 반환을 받을 때마다 변경분을 digest에 반영하고 state를 갱신한다. 처음 만든 뒤에는 바뀐 행·항목만 고치고 파일 전체를 다시 쓰지 않는다. 동시에 받은 변경분이 서로 모순되면 둘 다 반영하지 않고 모순을 state에 적은 뒤 해당 task를 다시 계획한다.
- **digest 초기화**: 계획 단계를 거치면 feature-draft worker 반환의 `digest 변경분`으로 만든다. draft로 진입하면 draft AC의 검증 명령, `_sdd/env.md`, 대화에서만 나온 결정으로 메인 루프가 만든다. 이때 대상 파일을 탐색하지 않는다.

## 단계와 진입

| 단계 | worker 계약 | 입력 | 산출물 |
|------|-------------|------|--------|
| feature-draft | `references/workers/feature-draft.md` | 요청·결정(digest), fix할 findings | `_sdd/drafts/` draft |
| plan-review | `references/workers/plan-review.md` | draft 경로 | findings 반환 |
| implementation | `references/workers/implementation.md` | draft 경로 + task ID 하나, 또는 fix할 findings | 대상 파일 변경 |
| implementation-review | `references/workers/implementation-review.md` + simplicity 계약 `references/simplicity-contract.md` | draft 경로, 구현 시작점(base) | AC verdict·findings 반환 |
| spec-sync | `references/workers/spec-sync.md` | draft 경로, state 경로, draft 소비 여부 | `_sdd/spec/` 변경 |

draft의 Part 2 task가 모두 닫혔고 남은 분할 feature가 없으면, spec-sync 입력에 "draft 소비 완료 — `_processed_` rename 대상"을 넣는다.

진입 규칙:
- 요청만 있으면 feature-draft부터 시작한다.
- draft 경로가 있으면, state나 사용자 말로 plan-review 완료가 확인될 때 implementation부터 시작한다. 확인되지 않으면 plan-review부터 시작한다.
- 사용자가 단계만 지정하면(예: "spec-sync만", "리뷰만", "계획 리뷰만") 그 단계만 실행한다. 리뷰만 실행하면 findings를 보고하고 fix는 하지 않는다.
- 기본 종점은 spec-sync 완료다. 사용자가 종점을 지정하면 그 단계에서 멈춘다.
- discussion은 이 스킬 밖이다. discussion 요약 파일은 입력 포인터로만 쓴다.

## Worker dispatch

모든 worker는 아래 형식의 prompt 하나로 띄운다. 이 형식이 단일 소스다. 공통 경계와 반환 규칙은 `references/worker-boundary.md`가 단일 소스다. worker는 이번 대화를 읽지 못하므로 필요한 맥락은 digest와 입력에 담는다. 계약 파일 절대 경로는 이 스킬 디렉터리(스킬을 로드할 때 주어지는 base directory)에 `단계와 진입` 표의 상대 경로를 붙여 만든다.

```text
너는 sdd-orchestrator가 띄운 <단계> worker다.
계약: <계약 파일 절대 경로> — 그대로 따른다.
공통 경계: <references/worker-boundary.md 절대 경로> — 그대로 따른다.
digest: <digest.md 절대 경로> — 결정·환경 함정·검증 레시피다.
시작: 계약·공통 경계·digest·입력 문서를 한 메시지에서 함께 읽는다.
입력:
- <draft 경로 / task ID / 리뷰 범위와 base / fix할 findings / 차원 묶음 한정 등>
- 동시에 실행 중인 다른 worker의 Target Files: <목록 또는 없음>
```

- 띄운 worker가 모두 반환한 뒤 다음 행동을 정한다. 기다리는 동안 worker의 일을 대신하지 않는다.
- worker 모델: 기본은 세션 모델을 상속한다(지정하지 않는다). 사용자가 단계별 모델을 지정하면(예: "계획은 fable, 구현·리뷰·spec-sync는 sonnet" 또는 `--model <단계>=<모델>[,<단계>=<모델>…]`) 그 단계의 worker에만 적용한다. 단계 이름은 `단계와 진입` 표의 다섯 단계이고, implementation-review 지정은 correctness·simplicity worker 모두에, 각 단계의 fix 재dispatch에도 같은 모델을 쓴다. 시작할 때 지정값을 Runtime 절의 허용값으로 확인하고, 단계별 모델을 digest의 결정·제약에 적어 재개 때도 같은 값을 쓴다. 허용값 밖이면 허용값을 알리고 고쳐 받는다. 무인 실행이면 묻지 않고 그 단계는 세션 모델을 상속하며 마감 보고에 적는다.
- fix를 맡길 때는 `품질 게이트`의 fix 정책으로 고른 findings만 입력으로 넘긴다. worker는 받은 findings를 모두 반영한다.
- worker가 실패하거나 반환이 계약 형식을 벗어나면 같은 입력으로 1회 다시 띄운다. 또 실패하면 멈추고 사용자에게 보고한다.
- task worker가 계약 오류 반복(implementation 계약의 `중단 규칙`)으로 BLOCKED를 반환하면, 그 task를 계획 단계로 되돌린다(feature-draft worker에 fix 입력으로 보낸다).

## 병렬 규칙

- task worker는 task당 1개다.
- Target Files가 서로소이고, `Contracts`를 공유하지 않고, 산출물 의존(선행 task)이 없는 task들만 한 번에 동시에 띄운다. 나머지는 의존 순서대로 띄운다.
- read-only 검증 task(Target Files `없음`)는 다른 task의 결과를 검사하므로, 같은 draft의 변경 task가 모두 닫힌 뒤 띄운다. FAIL을 반환하면 원인 task의 worker를 그 판정과 함께 fix로 다시 띄운 뒤 검증 task를 다시 띄운다.
- 동시 실행 수 상한은 두지 않고 런타임에 맡긴다.
- 모든 worker는 같은 작업 트리를 쓴다.

## 품질 게이트

게이트 순서와 fix는 메인 루프가 소유한다. 리뷰 worker는 작성 worker와 다른 새 worker다.

- **계획 게이트**: feature-draft worker → plan-review worker → fix는 feature-draft worker를 findings와 함께 다시 띄운다.
- **구현 게이트**: 모든 task가 DELTA_CLOSED가 되면 리뷰 worker 3개를 동시에 띄운다.
  - correctness worker 1개: digest 검증 레시피를 fresh 실행해 전체 회귀를 대신한다.
  - simplicity worker 2개(차원 묶음 참조 1개, 국소 1개): 다른 worker처럼 계약 파일 경로를 읽고, 입력으로 차원 묶음 한정을 받는다.
  - fix: finding 위치 파일을 가진 task worker를 findings와 함께 다시 띄운다. 어느 task에도 속하지 않는 파일이면 그 파일을 대상으로 한 fix worker를 implementation 계약으로 띄운다. fix worker는 커버리지 델타와 표적 재실행까지 하고 반환한다.
- **fix 정책**(게이트 공통):
  - Critical·High·Medium은 반영한다.
  - correctness Low와 계획 Low는 저비용이고 명백히 이득이며 현재 scope 안일 때만 반영한다.
  - simplicity Low는 advisory로만 남긴다.
- **gate 2**:
  - gate 1은 항상 실행하고 fix 1을 한다.
  - 조건: gate 1의 fix 전 raw finding을 그 게이트의 리뷰 worker 전부에 걸쳐 합산한다(Low 제외, dedup 없음). `Critical+High ≥ 3` 또는 `Medium ≥ 5`면 조건 충족이다.
  - 조건 충족이면 fix 1 뒤에 같은 게이트를 한 번 더 실행하고 같은 fix 정책으로 fix 2를 한다. gate 3은 없다.
  - gate 2의 raw 합산도 조건을 충족하면 마감에서 후속 리뷰 1회를 권고한다.
- **미완료 게이트**: 리뷰 worker가 미완료를 반환하면 확보된 findings만 fix 정책으로 처리한다. 사유와 남은 작업을 보고한다. 그 호출은 횟수에 넣되 통과로 세지 않는다.
- 게이트 반환은 사용자 입력 대기 지점이 아니다. 반환 직후 fix와 gate 2 판정을 이어서 한다.

## 재개

state.md를 읽어 다음 행동을 정한다. DELTA_CLOSED가 아닌 task는 state를 믿지 않고 task worker를 띄워 fresh로 다시 판정한다. DELTA_CLOSED task는 믿는다. 게이트 단계에서 멈췄으면 그 게이트를 다시 실행한다.

## 마감

1. state의 AC→증거 표를 리뷰 worker의 fresh verdict 포인터로 채운다. fix 뒤 바뀐 AC는 fix worker의 표적 재실행 증거로 갱신한다. 증거가 없는 AC는 충족으로 적지 않는다.
2. 채팅에는 다음만 보고한다: 실행한 단계, 게이트 호출별 severity·fix·검증, 미충족·보류 AC, 사용자 확인이 필요한 Open Questions, state 경로.

## Runtime: worker dispatch

- worker는 `Agent` 도구로 `subagent_type: "general-purpose"`를 띄운다. 도구 schema에 `run_in_background`가 있으면 `run_in_background: false`로 둔다 — 백그라운드 실행은 dispatch마다 안내문과 결과 포장을 메인 맥락에 더한다. prompt는 `Worker dispatch` 형식이다. worker 모델이 지정된 단계만 `model`에 그 값을 넣는다(허용값 `sonnet`·`opus`·`haiku`·`fable`). 지정하지 않은 단계는 `model`을 생략해 세션 기본값을 따른다.
- 동시에 띄울 worker는 한 메시지에 여러 `Agent` 호출로 낸다. 함께 실행되고 결과가 한 번에 돌아온다. 백그라운드로만 실행되는 환경이면 모든 worker의 결과를 받은 뒤 다음 행동으로 간다.

## Final Check

선택한 경로에 해당하는 Acceptance Criteria를 한 번 점검한다. 보완 가능한 기록 누락은 고치고, 대상 파일 수정이 필요한 누락은 worker를 띄워 처리한다. 이미 일어난 경계 위반은 사실과 영향을 보고하며 소급 충족하지 않는다. 외부 blocker나 중단은 미충족 AC·사유·다음 조치로 보고한다.
