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
   - implementation: draft Part 2 task를 `병렬 규칙`대로 task worker로 띄운다.
   - implementation-review: 구현 게이트(`품질 게이트`)를 실행한다.
   - spec-sync: spec-sync worker 1개를 띄운다.
   - 단계를 닫을 때마다 state의 단계를 갱신한다.
4. `마감`으로 닫는다.

## 역할 경계

메인 루프가 직접 하는 일:
- 사용자 질문. 계획 worker를 띄우기 전에, 아키텍처·범위·Target Files를 바꾸는 unknown만 한 번에 하나씩 묻는다. feature-draft worker의 최초 반환과 fix 반환에서도 Open Questions와 사용자 확인 사항을 회수한다. 새 미승인 구조 결정에 사용자 확인이 필요하면 사용자에게 확인하고, 그 결정에 의존하는 구현 dispatch를 확인 전까지 보류한다. 이미 승인된 결정과 routine 선택은 다시 묻지 않는다. 사용자가 무인 실행을 맡겼으면 묻지 않고 합당한 결정을 내린다. 결정·제약은 digest에 반영하고, 결정 때문에 draft를 바꿔야 하면 feature-draft worker에 fix로 맡긴 뒤 계획 게이트 규칙을 따른다.
- digest·state 작성, 단계·게이트 순서와 병렬 판단, worker 반환 집계, 마감 보고.
- 상위 하네스에 work log 규약이 있으면 단계를 닫을 때 그 규약대로 기록한다.

메인 루프가 하지 않는 일:
- 대상 파일(코드·테스트·draft·spec) 수정. 작은 수정도 worker에게 맡긴다.
- worker 일의 대리 수행. worker가 실패해도 대신 고치거나 대신 검증하지 않는다. 확인이 필요하면 worker를 띄운다.
- 대상 파일·diff의 탐색적 읽기. 판단에 필요한 사실은 worker 반환으로 받는다. 읽어도 되는 것은 `references/handoff-templates.md`, `references/worker-boundary.md`, draft, `_sdd/env.md`, digest·state뿐이다. `references/workers/`의 계약은 worker가 읽는 문서라 메인 루프는 읽지 않는다.
- 환경(명령·도구·셸 동작)의 직접 탐색. 환경 함정은 `_sdd/env.md`와 worker 반환의 `digest 변경분`에서 받아 digest에 쌓는다.
- git 쓰기. 사용자가 따로 요청할 때만 한다.

## 인계 파일

위치는 `_sdd/implementation/<YYYY-MM-DD>_<slug>/`이다. slug는 draft slug를 쓰고, draft가 없으면 요청 요약을 snake_case로 쓴다. 같은 slug 디렉터리가 있으면 새로 만들지 않고 이어 쓴다. 처음 만들기 직전에 `references/worker-boundary.md`의 `digest 내용 계약`과 `references/handoff-templates.md`를 함께 읽고 그 템플릿을 출발 구조로 쓴다.

- **digest.md**: 모든 worker가 읽는 방법과 이유다. 허용 내용과 제외 내용은 `references/worker-boundary.md`의 `digest 내용 계약`이 단독 소유한다. 같은 AC의 명령이 구체화되면 기존 레시피를 교체하고, 정정된 환경 사실은 해당 항목을 고친다. finding 하나만 검증하는 fix 전용 check 행은 메인 루프가 fix worker의 표적 재실행 통과를 state에 반영할 때 지운다(증거는 state가 가진다).
- **state.md**: 재개용 상태다. 단계, task 상태, RED·GREEN 신호, 게이트 결과, 계획 이탈·발견, AC→증거를 담는다. 메인 루프만 읽는다. spec-sync worker는 구현 증거로 읽을 수 있다. 리뷰 worker에게는 주지 않는다. 명령 출력 전문과 진행 서술은 복사하지 않는다.
- 두 파일의 작성자는 메인 루프 하나다. worker는 반환 끝의 `digest 변경분`으로만 digest를 바꾼다. 메인 루프는 반환의 `digest 변경분`을 공통 내용 계약으로 분류해 허용 변경분만 다음 dispatch 전에 digest에 반영한다. 완료·통과·다음 조치 등 상태 정보가 섞여 있으면 digest에서 제외하고 state 갱신 대상으로 분리한다. 일회성 입력은 `Worker dispatch` 입력으로만 넘긴다. state는 단계를 닫을 때 그 단계의 반환을 모아 한 번에 갱신한다(반환마다 고치지 않는다). 처음 만든 뒤에는 받은 변경분과 관련된 행·항목만 갱신하며, 매 반환마다 전체 digest를 재심사하거나 별도 게이트를 만들지 않는다. 실행이 겹친 worker의 변경분이 이미 반영한 변경분과 모순되면 나중 변경분을 반영하지 않고 모순을 state에 적은 뒤 해당 task를 다시 계획한다.
- **digest 초기화**: 계획 단계를 거치면 feature-draft worker 반환의 `digest 변경분`과 `_sdd/env.md`로 만든다. draft로 진입하면 draft AC의 검증 명령, `_sdd/env.md`, 대화에서만 나온 결정으로 메인 루프가 만든다. 이때 대상 파일을 탐색하지 않는다.

## 단계와 진입

| 단계 | worker 계약 | 입력 | 산출물 |
|------|-------------|------|--------|
| feature-draft | `references/workers/feature-draft.md` | 요청·결정(digest), fix할 findings | `_sdd/drafts/` draft |
| plan-review | `references/workers/plan-review.md` | draft 경로 | findings 반환 |
| implementation | `references/workers/implementation.md` | draft 경로 + task ID 하나, 또는 fix할 findings | 대상 파일 변경 |
| implementation-review | `references/workers/implementation-review.md` + simplicity 계약 `references/simplicity-contract.md` | draft 경로, 구현 시작점(base) | AC verdict·findings 반환 |
| spec-sync | `references/workers/spec-sync.md` | draft 경로, state 경로, draft 소비 여부 | `_sdd/spec/` 변경, `_sdd/env.md` 승격 |

draft의 Part 2 task가 모두 닫혔고 남은 분할 feature가 없으면, spec-sync 입력에 "draft 소비 완료 — `_processed_` rename 대상"을 넣는다. 소비 rename이 반환되면 메인 루프는 digest의 draft 출처를 새 경로로 갱신한다.

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

- worker 결과를 기다리려고 sleep·until 루프나 출력 파일 감시(폴링)를 하지 않는다. 띄운 뒤에는 메인 루프 자신의 일(digest·state 갱신, 사용자 대화, 의존이 풀린 worker dispatch)을 하고, 할 일이 없으면 `Runtime: worker dispatch` 절의 방식으로 다음 반환을 받는다. worker의 일은 대신하지 않는다.
- worker 옵션: 단계·필드(model, Codex에서는 effort도)마다 호출 지정 > `_sdd/env.md` `## Worker Model Defaults` 절의 현재 runtime 하위 절 값 > 값 없음 순으로 적용값을 정한다. 값이 없는 필드는 생략해 런타임 기본 동작을 따른다.
  - 지정: `--model <단계>=<모델>[,<단계>=<모델>…]`, Codex에서는 독립적인 `--effort <단계>=<effort>[,<단계>=<effort>…]`도 받는다. 동등한 자연어 지정도 받는다(예: "계획은 <모델 A>, 구현·리뷰는 <모델 B>", Codex에서는 "리뷰 effort는 <effort>"). model만·effort만·둘 다 지정할 수 있다.
  - env.md 기본값: `## Worker Model Defaults` 아래 `### Claude Code` 표(`단계 | model`)와 `### Codex` 표(`단계 | model | effort`)를 둔다. 행은 다섯 단계 이름이다. 빈 칸이거나 행·하위 절·절이 없으면 값 없음이다.
  - 범위: 단계 이름은 `단계와 진입` 표의 다섯 단계다. implementation-review 적용값은 correctness 1개와 simplicity 2개 모두에 적용한다. 각 단계의 fix 재dispatch에도 같은 옵션을 쓴다.
  - 확인·기록: 시작할 때 env.md 절을 읽고, 호출 지정과 합친 적용값의 필드·지원값을 Runtime 절로 검증한다(env.md 값도 같은 검증을 거친다). effort가 있으면 모델별 조합도 확인한다. 이후 적용할 단계별 옵션을 digest의 결정·제약에 적어 재개 때도 같은 값을 쓴다. 호출 지정과 env.md 어디에도 없는 값을 임의로 고정하거나 env.md 밖에 별도 설정 파일을 만들지 않는다.
  - 필드 미지원·지원값 미확정·잘못된 값/조합은 원인과 확인 가능한 허용값을 구분해 알리고 고쳐 받는다. 해결 전에는 해당 단계 dispatch를 보류한다. 무인 실행이면 묻지 않고 그 단계의 override를 생략해 런타임 기본값으로 실행하며, fallback 결정은 digest에, 발생 사실은 state와 마감 보고에 적는다.
- fix를 맡길 때는 `품질 게이트`의 fix 정책으로 고른 findings만 입력으로 넘긴다. worker는 받은 findings를 모두 반영한다.
- worker가 실패하거나 반환이 계약 형식을 벗어나면 같은 입력으로 1회 다시 띄운다. 또 실패하면 멈추고 사용자에게 보고한다.
- task worker가 계약 오류 반복(implementation 계약의 `중단 규칙`)으로 BLOCKED를 반환하면, 그 task를 계획 단계로 되돌린다(feature-draft worker에 fix 입력으로 보낸다).

## 병렬 규칙

- task worker는 task당 1개다.
- 시작할 때, 그리고 worker가 반환할 때마다(반환의 `digest 변경분`은 먼저 digest에 반영한다) 아래 조건을 모두 만족하는 task를 바로 띄운다.
  - 선행 task가 모두 DELTA_CLOSED다.
  - Target Files가 실행 중인 worker 및 함께 띄우는 worker의 것과 서로소다.
  - 그 worker들의 task와 `Contracts`를 공유하지 않는다.
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
- 게이트 반환 자체는 사용자 입력 대기 지점이 아니다. 다만 `역할 경계`의 새 미승인 결정 확인은 최초/fix draft 모두에 적용하며 의존 구현 dispatch를 막는다. 그 외에는 그 게이트의 리뷰 worker가 모두 반환하면 바로 fix와 gate 2 판정을 한다(raw 합산이 필요해 먼저 온 반환만으로 판정하지 않는다).

## 재개

state.md를 읽어 다음 행동을 정한다. DELTA_CLOSED가 아닌 task는 state를 믿지 않고 task worker를 띄워 fresh로 다시 판정한다. DELTA_CLOSED task는 믿는다. 게이트 단계에서 멈췄으면 그 게이트를 다시 실행한다.

## 마감

1. state의 AC→증거 표를 리뷰 worker의 fresh verdict 포인터로 채운다. fix 뒤 바뀐 AC는 fix worker의 표적 재실행 증거로 갱신한다. 증거가 없는 AC는 충족으로 적지 않는다.
2. 채팅에는 다음만 보고한다: 실행한 단계, 게이트 호출별 severity·fix·검증, 미충족·보류 AC, 사용자 확인이 필요한 Open Questions, state 경로.

## Runtime: worker dispatch

- 스킬 내부 dispatch를 허용하는 런타임에서 이 호출은 worker 위임 요청으로 처리한다. 상위 정책이 별도 허가를 요구하면 먼저 확보한다.
- active tool schema로 아래 두 contract 중 **완전하게 지원되는 하나**를 선택한다. surface 이름으로 추정하거나 없는 lifecycle 도구를 검색하지 않는다. 두 contract의 필드를 섞지 않고, 하나로 확정할 수 없으면 schema blocker로 멈추고 보고한다.
  - **Mailbox** (spawn의 task_name·fork_turns·message와 target 없는 mailbox wait가 있을 때): worker마다 parent tree에서 고유한 task_name과 `fork_turns: "none"`으로 spawn한다. mailbox wait로 final이 올 때마다 그 반환을 처리하고 완료 agent는 닫지 않는다. 중단이 필요할 때만 노출된 interrupt_agent를 쓴다.
  - **Target/close** (message 기반 spawn, targets를 받는 wait, close_agent가 있을 때): spawn 후 실행 중인 worker 전부를 targets로 wait하고, final이 올 때마다 그 반환을 처리하고 그 handle을 닫는다.
- spawn message는 `Worker dispatch` 형식을 그대로 쓴다. `Worker dispatch` 우선순위로 정한 단계별 적용값의 model은 `model`, effort는 `reasoning_effort`에만 매핑한다. 둘 다 값이 없으면 둘 다 생략하고, model만 있으면 `model`만, effort만 있으면 `reasoning_effort`만, 둘 다 있으면 두 필드를 넣는다. 값이 없는 필드는 런타임 기본 동작을 따른다. 모델만 바꾸면 그 모델의 기본 effort가 적용될 수 있으므로 부모 effort 상속을 보장하지 않는다.
- 적용값이 있는 필드는 선택한 spawn schema에 있어야 한다(없으면 **미지원**). 지원값은 schema enum 또는 활성 도구 설명의 명시 목록으로 확인한다. enum이 없어도 설명에 목록이 있으면 정상 검증하고, 양쪽 모두 없으면 **미확정**으로 처리한다. 명시 목록 밖의 값은 **잘못된 값**이다. effort가 있으면 모델별 지원 차이도 대조해 각각 허용되는 값이라도 조합이 불가능하면 **잘못된 조합**으로 처리한다. effort만 있는 경우에는 런타임이 상속할 모델을 기준으로 조합을 확인하며, 그 모델이나 지원 조합을 확인할 수 없으면 미확정이다. 처리 방식은 `Worker dispatch`의 옵션 정책을 따른다. 별도 고정 allowlist는 두지 않는다.
- 동시에 띄울 worker는 연달아 spawn한다. 반환 하나를 처리하면 `병렬 규칙`대로 의존이 풀린 worker를 spawn한 뒤 다시 wait한다. spawn이 동시 실행 상한으로 거부되면 final을 하나 받은 뒤 spawn한다.
- wait timeout을 완료로 간주하지 않는다. 실행 중인 worker의 final을 다시 기다리거나, 통제된 중단과 미완료 상태를 보고한다.

## Final Check

선택한 경로에 해당하는 Acceptance Criteria를 한 번 점검한다. 보완 가능한 기록 누락은 고치고, 대상 파일 수정이 필요한 누락은 worker를 띄워 처리한다. 이미 일어난 경계 위반은 사실과 영향을 보고하며 소급 충족하지 않는다. 외부 blocker나 중단은 미충족 AC·사유·다음 조치로 보고한다.
