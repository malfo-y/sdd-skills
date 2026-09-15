# goal-init 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/goal-init/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/goal-init/SKILL.md)
- 판정 요약: 수정 필요 4 / 정리 후보 1 / 실행 검증 필요 0

## 역할과 유지할 계약

멀티턴 목표를 평가자가 transcript로 판정할 조건 문자열과 4파일 하네스로 바꾸는 setup 스킬이다. Goal Intake → Divergence → Condition Crafting → Harness Setup → Handoff의 5단계, 2개 이상 접근 가설, 조건 자족성·매 턴 evidence·4,000자 self-check를 유지한다. 파일은 Step 4에서 지정 디렉터리에 생성하며, native goal을 발동하거나 status를 조회하지 않는다. `preset=sdd`는 HOW payload만 바꾸고 producer 실행은 사용자 activation 뒤에 시작한다. 이 계약은 [global spec](../../../_sdd/spec/main.md) 93–97행에 고정돼 있다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | goal-init-01: Codex 질문 수단 지정에 활성 도구 조건이 없다. 적합성 gate와 setup-only 적용 조건은 명확하다. |
| 2. 충돌과 우선순위 | goal-init-02: 매 턴 레시피 실행과 slow/checkpoint·timeout 재실행 경계 충돌. goal-init-03: SDD 계속 조건과 STOP/STUCK 종료의 우선순위 누락. |
| 3. 확인·승인 경계 | goal-init-04: 예제가 사용자 원문에 없는 자율 승인 신호를 근거로 삼는다. 본문의 자율 신호 재질문 생략과 제외 목록은 유지한다. |
| 4. 중복과 소유권 | goal-init-05: Codex 실행법 단일 소스 선언과 reference의 고정 실행법 중복은 정리 후보다. Claude/Codex 배포 짝 자체는 결함이 아니다. |
| 5. 완료·복구 조건 | goal-init-03: 실패 종료와 성공 종료를 분리해야 한다. 정상 setup 완료 AC와 출력 의무는 판정 가능하다. |
| 6. 절차의 필요성 | 5단계·4파일·2개 가설은 현행 계약이므로 축소를 제안하지 않는다. goal-init-02의 무조건 재실행 범위만 줄이면 검증 계약을 유지할 수 있다. |

## Findings

### goal-init-01 — Codex Intake에 Claude 질문 도구명이 남아 있다 [수정 필요]

- 기준: 1, 2, 3.
- 적용 runtime: Codex.
- 근거: [Codex SKILL](../../../plugins/sdd-skills-codex/skills/goal-init/SKILL.md) 64행: “신호가 없으면 `AskUserQuestion` 1회로 `unattended`(권장) | `attended`를 정한다.” 같은 문서 12행은 도구 중립적인 “ask 기반 단일 대화 루프”다.
- 문제 상황: 자율 신호 없는 `/goal 셋업` 입력을 `AskUserQuestion`이 노출되지 않은 Codex 활성 schema에서 처리한다. 이번 리뷰 세션에는 `request_user_input`과 일반 대화가 제공되지만 `AskUserQuestion`은 없다. 본문에는 이에 대한 질문 수단 선택 규칙이 없다.
- 예상 영향: 필수 1회 질문을 지원되지 않는 이름으로 시도하거나 불필요하게 막혔다고 판단할 여지가 있다. 실제 호출 실패가 관측됐다는 뜻은 아니다.
- 최소 수정안: “신호가 없으면 활성 런타임에서 허용하는 질문 수단으로 1회 확인한다. 전용 도구가 없으면 일반 대화를 사용한다”로 바꾼다. 승인 성격의 질문에는 해당 런타임의 승인 질문 규칙을 따른다.
- 유지할 계약: 자율 신호가 있으면 되묻지 않고, 없으면 수준을 한 번 확정한다. 질문 생략이나 임의 `unattended` 승격을 허용하지 않는다.
- 소유자: `goal-init` Codex SKILL. Claude의 지원 도구 표기를 일괄 변경할 필요는 없다.
- 검증 상태: 문면과 이번 활성 schema 대조 완료. 다른 Codex surface의 영구 지원 여부는 미검증. spec 결정 불필요.

### goal-init-02 — 매 턴 전체 검증 레시피 실행이 기존 실행 경계와 충돌한다 [수정 필요]

- 기준: 1, 2, 6.
- 적용 runtime: Claude, Codex.
- 근거: [Claude template](../../../.claude/skills/goal-init/references/harness-templates.md), [Codex template](../../../plugins/sdd-skills-codex/skills/goal-init/references/harness-templates.md) 각 10행: “메인 에이전트가 매 턴 실행하고 출력을 대화에 surface한다.” 각 32행: “AC별 검증 명령·기대 출력·수치 임계·허용 델타 열거 등 브리틀 디테일 전부. 메인 에이전트가 매 턴 실행하고 출력을 대화에 surface한다.” [global spec](../../../_sdd/spec/main.md) 59행은 slow test를 명시 checkpoint로 제한하고, timeout된 같은 명령은 target·fixture·관련 구현 변경 전 재실행을 금지한다.
- 문제 상황: 레시피에 checkpoint 전용 통합 검증이 있거나 직전 턴에 30초 timeout이 발생했다. 다음 턴이 draft 작성 등 관련 구현을 바꾸지 않은 작업이어도 템플릿은 같은 검증을 다시 실행하라고 한다. SDD payload 사용 시에도 `goal.md`의 공통 레시피 지시는 남는다.
- 예상 영향: 반복 루프가 checkpoint 또는 재실행 금지 경계를 우회하거나, 두 지시 사이에서 선택해야 한다. “매 턴 evidence 표시”를 “모든 명령 매 턴 재실행”으로 불필요하게 확대한다.
- 최소 수정안: “매 턴 이번 진척에 필요한 허용된 검증을 실행하고 실제 출력 또는 기존 evidence·미실행 사유를 표시한다. slow/checkpoint 및 timeout 재실행 제한을 따른다. 최종 PASS에는 전체 필수 검증의 유효한 증거가 필요하다”로 레시피 실행 문구를 한 곳에서 정하고 슬롯은 이를 참조한다.
- 유지할 계약: 매 턴 transcript evidence, 증거 없는 완료 금지, 최종 integration proof, 30초 timeout·10초 분리·fast-only 마감. slow 검증을 삭제하거나 PASS로 간주하지 않는다.
- 소유자: `goal-init` template와 해당 예제. `implementation`/리뷰 스킬의 검증 경계는 소비 계약이며, 그쪽에 예외를 추가해 해결하지 않는다.
- 검증 상태: 문면 충돌 확인. 실제 slow 명령은 실행하지 않았다. 기존 guardrail 적용을 명시하는 수정에는 spec 결정 불필요.

### goal-init-03 — SDD payload가 성공하지 않으면 항상 반복해 STOP/STUCK과 충돌한다 [수정 필요]

- 기준: 2, 5.
- 적용 runtime: Claude, Codex의 `preset=sdd`.
- 근거: [Claude template](../../../.claude/skills/goal-init/references/harness-templates.md) 84행 / [Codex template](../../../plugins/sdd-skills-codex/skills/goal-init/references/harness-templates.md) 86행: “모든 `DONE WHEN`과 final integration proof가 통과했을 때만 종료한다. 아니면 1단계로 돌아간다.” 양쪽 29행은 “STOP: after <N> turns without progress.”이며, 40행은 “범위 밖이고 그 행동 없이는 진척 불가: `report.md` Status를 `STUCK`으로 두고 사유를 적은 뒤 종료한다.”
- 문제 상황: N턴 무진척이거나, 사용자 제외 목록에 있는 행동 외에는 더 진행할 수 없다. DONE WHEN은 미충족이므로 HOW 마지막 문장은 반복을 요구하지만 STOP/위임 절은 종료를 요구한다.
- 예상 영향: 실패 종료가 성공 종료 규칙에 가려져 불필요한 반복 또는 권한 경계 재판정이 생길 수 있다.
- 최소 수정안: 마지막 항목을 “모든 DONE WHEN과 final integration proof가 통과했을 때만 성공 종료한다. STOP 또는 위임 범위의 STUCK 경계에 도달하면 사유를 기록하고 미완료 종료한다. 그 외에는 1단계로 돌아간다”로 한정한다. 실제 native goal lifecycle 처리는 활성 런타임 규범을 따른다.
- 유지할 계약: 전 항목 증거 없는 성공 종료 금지, 기존 STOP·권한 제외, 사용자 activation 전 비발동, producer-owned gate. STOP 횟수나 native 상태 변경 API를 새로 고정하지 않는다.
- 소유자: `goal-init`의 runtime-local template. `sdd-autopilot`은 이를 호출·relay하는 소비자이므로 자체 payload나 별도 종료 루프를 만들지 않는다.
- 검증 상태: 동일 산출물 내부의 문면 충돌 확인. 활성 goal로 재현하지 않았다. 성공/미완료 구분 명시에 spec 결정 불필요.

### goal-init-04 — 예제가 없는 사용자 자율 신호를 근거로 사전 승인을 만든다 [수정 필요]

- 기준: 2, 3.
- 적용 runtime: Claude, Codex.
- 근거: [Claude example](../../../.claude/skills/goal-init/examples/sample-goal-init-session.md), [Codex example](../../../plugins/sdd-skills-codex/skills/goal-init/examples/sample-goal-init-session.md) 각 19행의 사용자 원문은 “CI에서 가끔 깨지는 통합 테스트 스위트가 있어요. 이걸 안정화하고 싶어요.”다. 각 117행은 “수준: unattended (\"알아서 안정화해줘\" 원문 신호)”이고, 118행은 commit·feature 브랜치 push·PR 생성 사전 승인을 기입한다. 각 SKILL 64행은 신호가 없으면 수준을 질문하도록 한다.
- 문제 상황: 예제에 표시된 실제 대화에는 “알아서” 신호나 자율 수준 질문·응답이 없는데, 하네스는 존재하지 않는 원문을 근거로 승인을 확정한다. 175행도 같은 설명을 반복한다.
- 예상 영향: 예제를 모방하면 단순 목표 요청만으로 승인 범위를 확대하는 경로가 생긴다. 본문의 올바른 확인 규칙과 예시가 서로 다른 행동을 가르친다.
- 최소 수정안: 예제 19행의 사용자 요청에 실제 자율 신호를 추가해 117행의 근거와 맞추거나, Step 1에 수준 질문과 명시 응답을 추가한다. 기존 시나리오를 유지하려면 첫 방법이 가장 작다.
- 유지할 계약: 원문 신호에 따른 질문 생략, 신호가 없을 때 1회 확인, 사전 승인·항상 확인 목록의 구분. 승인 없는 행동을 예외로 허용하지 않는다.
- 소유자: `goal-init` Claude/Codex examples.
- 검증 상태: 예제의 전체 대화와 해당 산출물 대조 완료. 실행 재현 없이 확인 가능한 문서 불일치다. spec 결정 불필요.

### goal-init-05 — Codex 실행법의 단일 소스 선언과 고정 템플릿 본문이 중복된다 [정리 후보]

- 기준: 4.
- 적용 runtime: Codex.
- 근거: [Codex SKILL](../../../plugins/sdd-skills-codex/skills/goal-init/SKILL.md) 103행: “실행법 4요소는 Step 5 Handoff에 단일 소스로 정의한다.” 실제 정의는 113행이다. [Codex template](../../../plugins/sdd-skills-codex/skills/goal-init/references/harness-templates.md) 60–62행도 활성화 명령·lifecycle·continuation/evidence 설명을 고정 본문으로 포함한다. 6행은 슬롯 외 텍스트를 그대로 유지하도록 한다.
- 문제 상황: Step 5 실행법을 수정하면 reference 고정 본문도 함께 바꾸지 않는 한 화면 handoff와 생성된 goal.md의 설명이 갈라질 수 있다. 현재 두 설명의 내용 충돌을 주장하는 finding은 아니다.
- 예상 영향: 하나의 runtime 안에서 같은 실행법의 갱신 지점이 둘이다. 배포 mirror의 존재와는 별개다.
- 최소 수정안: Codex template의 실행법을 “SKILL.md Step 5의 Codex 실행법 4요소로 채우는 슬롯”으로 바꾸고 Step 4가 이를 채우도록 한다. Claude template처럼 문서 구조는 그대로 유지한다.
- 유지할 계약: 해당 runtime 슬롯만 채우기, 생성된 파일과 최종 handoff에 실행법 제공, 다른 runtime 슬롯 placeholder, setup-only.
- 소유자: `goal-init` Codex SKILL/template.
- 검증 상태: 단일 소스 선언과 고정 본문 중복을 정적으로 확인했다. 실행 성능 개선은 측정하지 않았다. spec 결정 불필요.

## 런타임 차이와 의존성

- 두 SKILL 전문과 runtime-local `references/harness-templates.md`, `examples/sample-goal-init-session.md`를 검토했다. 기본 process/AC는 같고, runtime 실행법과 자기 슬롯 채우기는 정당한 차이다.
- 직접 이웃은 [Codex sdd-autopilot](../../../plugins/sdd-skills-codex/skills/sdd-autopilot/SKILL.md) 전문을 읽었다. 23행의 template 소유권, 24–25행의 setup-only·native 불간섭, 41–45행의 relay 경계는 goal-init 계약과 일치한다. Claude sdd-autopilot 본문과 하류 producer 전문은 이 리뷰에서 미검토다.
- global spec의 59행 검증 경계, 93–97행 goal 계약을 적용했다. `review-criteria.md`, AGENTS.md, `_sdd/env.md`도 읽었다. 과거 work log는 읽지 않았다.
- native `/goal`의 CLI subcommand·설정 키·평가자 구현은 직접 실행하거나 조사하지 않았다. SKILL 113행의 runtime 안내가 현재 모든 surface에서 유효한지는 판정 범위 밖이다. 이번 schema에서 특정 도구가 없다는 관측을 제품 전체의 영구 지원 여부로 확대하지 않았다.
- goal-init-02/03의 수정 소유자는 goal-init이다. sdd-autopilot이나 implementation 쪽에서 별도 예외·중복 HOW를 만드는 해결은 권장하지 않는다.

## 권장 처리 순서와 검증

1. goal-init-04와 goal-init-01을 먼저 수정한다. 예제 원문이 실제 승인 근거를 포함하는지, Codex에서 허용된 질문 수단으로 정확히 한 번 수준을 확인하는지 본다.
2. goal-init-02/03을 양쪽 template에 반영한다. timeout 후 관련 변경 없는 턴, checkpoint 대기, N턴 무진척, 위임 범위 밖 필수 행동을 각각 입력한 모의 실행에서 무조건 재실행·무조건 반복이 나오지 않아야 한다. 미완료 종료를 PASS로 처리하지 않아야 한다.
3. goal-init-05를 정리한 뒤 산출물 검토로 파일과 화면의 실행법 4요소가 일치하는지 확인한다. 정상 generic/sdd setup에서 5단계·4파일·조건 전문·개별 경로·비발동 불변식을 함께 확인한다.

이번 리뷰는 스킬을 실행하지 않았으며 제안을 적용하지 않았다. 보고서의 상대 링크·인용 위치·파일 권한과 whitespace만 정적으로 검증한다.
