# second-opinion 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/second-opinion/SKILL.md). Codex runtime 짝 없음(의도된 플랫폼 범위).
- 판정 요약: 수정 필요 3 / 정리 후보 1 / 실행 검증 필요 0

## 역할과 유지할 계약

질문에 필요한 코드·파일을 모아 Codex의 독립 분석을 요청하고 응답 원문을 사용자에게 전달한다. [components](../../../_sdd/spec/components.md) 42행의 read-only 역할과 54행의 Claude 전용 계약을 유지한다. 독립 Codex 분석을 메인 에이전트의 자체 답변으로 조용히 대체하거나 Codex runtime 짝을 새로 요구하지 않는다. 성공 시 AC 자체 검증과 원문 전달을 유지하며, 실패는 성공과 구별해 보고한다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | second-opinion-02: read-only 지시가 수집 단계에만 적용된다. 사용자 트리거와 질문·컨텍스트 수집 범위는 명확하다. |
| 2. 충돌과 우선순위 | second-opinion-01: 외부 custom agent 호출과 global spec의 내장 agent 전용 규칙이 충돌한다. |
| 3. 확인·승인 경계 | 불필요한 재확인 gate는 없다. second-opinion-02의 reviewer 수정 권한 범위를 명확히 해야 한다. |
| 4. 중복과 소유권 | second-opinion-01: 외부 reviewer 의존성을 누가 제공하는지 미정이다. second-opinion-04: 임시 파일 규칙의 제목과 실제 내용 정리 후보. |
| 5. 완료·복구 조건 | second-opinion-03: 외부 실행 불가 상태에서 AC를 만족시키지 못할 때의 실패 종료 경로가 없다. |
| 6. 절차의 필요성 | 컨텍스트 수집→포장→독립 분석→원문 전달은 역할에 필요한 최소 흐름이다. 2,000자 분기나 4단계 자체를 결함으로 판정할 근거는 없다. |

## Findings

### second-opinion-01 — external agent 의존성과 내장 agent 전용 계약이 충돌한다 [수정 필요]

- 기준: 2, 4.
- 적용 runtime: Claude.
- 근거: [SKILL](../../../.claude/skills/second-opinion/SKILL.md) 50행: “`Agent(subagent_type="codex:codex-rescue")`로 enriched 프롬프트를 전달한다.” [global spec](../../../_sdd/spec/main.md) 91행: “스킬의 dispatch는 런타임 내장 agent type(Claude `general-purpose`, Codex `explorer`)만 사용한다.” [marketplace](../../../.claude-plugin/marketplace.json) 17–38행에는 skills만 등록돼 있고 이 agent 제공·설치 계약은 없다.
- 문제 상황: 사용자가 이 스킬을 호출하면 SKILL은 `codex:codex-rescue` type을 요구하지만 global spec은 내장 type만 허용한다. 외부 플러그인이 설치된 환경이어도 두 문서 사이에 예외·우선순위 정의가 없다.
- 예상 영향: 실행자는 필수 호출과 dispatch guardrail 중 하나를 어겨야 한다. 외부 의존성 없는 설치에서는 추가로 실행이 막힐 가능성이 있으나, 실제 설치 부재·호출 실패를 관측한 것은 아니다.
- 최소 수정안: 먼저 지원 경로를 결정한다. 외부 Codex adapter를 유지한다면 global spec에 이 스킬의 좁은 예외와 dependency 확인·실패 보고 계약을 정한다. 내장 agent 전용 정책을 유지한다면 실제 Codex 접근 수단을 확인한 후 그 경로로 연결하도록 수정한다. 단순히 `general-purpose`로 이름만 바꿔 같은 모델의 답변을 Codex 결과로 전달하면 안 된다.
- 유지할 계약: 독립 Codex 분석, 결과 원문 전달, read-only, 설치된 외부 자산을 repo 번들 custom agent로 잘못 설명하지 않기.
- 소유자: `second-opinion` SKILL과 global dispatch 계약 소유자.
- 검증 상태: source/spec 문면 충돌 확인. 외부 `codex:codex-rescue` 정의·실제 runtime은 미검토. **spec 결정 필요**: 현재 계약의 예외인지, 호출 경로를 바꿀지 선택해야 한다.

### second-opinion-02 — read-only 범위가 Step 1–2에서 끝나고 외부 reviewer에 전달되지 않는다 [수정 필요]

- 기준: 1, 3.
- 적용 runtime: Claude에서 호출하는 Codex reviewer.
- 근거: [SKILL](../../../.claude/skills/second-opinion/SKILL.md) 18행: “**읽기 전용**: Step 1-2에서 코드를 수정하지 않는다. 컨텍스트 수집만 한다.” 54–57행의 전달 프롬프트는 “독립적인 second opinion을 제공하라.”와 컨텍스트 참조만 포함한다. [components](../../../_sdd/spec/components.md) 42행은 스킬 전체를 “Claude Code 전용, read-only”로 정의한다.
- 문제 상황: 사용자가 코드나 디버깅 접근에 대한 의견을 요청하고, Step 3의 외부 reviewer가 컨텍스트를 읽는다. 이 단계에는 대상 파일 수정·명령 실행 권한 경계가 명시되지 않았으며, 부모의 Step 1–2 제한도 prompt에 포함되지 않는다.
- 예상 영향: 외부 agent의 기본 행동이 수정까지 포함한다면 의견 요청이 파일 변경으로 번질 수 있다. 외부 agent가 실제로 수정한다는 사실 주장은 아니다. 여기서 확인된 결함은 스킬의 read-only 계약 전달 누락이다.
- 최소 수정안: read-only 규칙을 전체 분석 흐름으로 확대하고 Step 3 prompt에 “분석만 수행한다. 대상 코드·문서를 수정하지 않고 하위 agent를 생성하지 않는다”를 포함한다. 부모가 만드는 컨텍스트 임시 파일은 명시적 예외로 유지한다. 실행 증거가 필요한 경우 허용된 read-only 검증 범위를 별도로 지시하고 실제 실행 여부를 반환에 표시한다.
- 유지할 계약: 컨텍스트 수집과 임시 파일 생성, 독립 분석, 원문 전달, nesting 1단계 제한. 모델의 실제 권한을 검증하지 않은 채 기술적으로 강제된다고 표현하지 않는다.
- 소유자: `second-opinion` Hard Rules와 Codex forwarding prompt. 외부 reviewer 구현 변경을 전제할 필요는 없다.
- 검증 상태: read-only 단계 한정과 전달 prompt를 정적으로 대조했다. 실제 외부 실행·파일 변경은 없었다. 기존 read-only 계약 보강이므로 spec 결정 불필요.

### second-opinion-03 — 외부 실행 실패 때 최종 AC 재진입을 끝낼 조건이 없다 [수정 필요]

- 기준: 5.
- 적용 runtime: Claude.
- 근거: [SKILL](../../../.claude/skills/second-opinion/SKILL.md) 13–14행은 Codex 전달과 결과 원문 전달을 완료 조건으로 삼고, 66행은 “미충족 항목이 있으면 해당 단계로 돌아가 수정한다.”라고 한다. Step 3과 Step 4 사이에 실패 처리 규칙은 없다.
- 문제 상황: 선택된 Codex adapter가 인증 오류를 반환하거나, 요청은 전달됐지만 분석 결과가 생성되지 않는다. AC2/AC3를 만족시키려면 해당 단계를 재시도해야 하지만 같은 원인 상태가 계속될 때 종료 기준이 없다.
- 예상 영향: 변하지 않은 외부 오류에 반복 호출하거나 오류 메시지를 성공적인 분석 결과처럼 전달해 AC를 닫을 수 있다. 실제 무한 재시도가 발생했다고 주장하지 않는다.
- 최소 수정안: “Codex 분석 결과가 없으면 실패 원인과 미충족 AC를 보고하고 종료한다. 복구 가능한 누락은 수정 후 재시도하되, 원인이 바뀌지 않은 외부 실행 오류는 자동 재시도하지 않는다”를 추가한다. 원래 질문을 자체 답변으로 대체하지 않는다.
- 유지할 계약: 정상 경로의 최종 자체 검증·Codex 원문 전달. 실패한 분석을 성공으로 표시하지 않는다. 불필요한 사용자 승인 gate나 고정 polling 루프를 추가하지 않는다.
- 소유자: `second-opinion` Error Handling/Final Check.
- 검증 상태: 성공 AC와 무조건 재진입 지시 사이의 실패 분기 누락 확인. 인증·외부 호출 실패는 실제로 유발하지 않았다. spec 결정 불필요.

### second-opinion-04 — ‘임시 파일 정리’ 규칙은 실제로 저장 경로만 지정한다 [정리 후보]

- 기준: 4.
- 적용 runtime: Claude.
- 근거: [SKILL](../../../.claude/skills/second-opinion/SKILL.md) 20행: “**임시 파일 정리**: 컨텍스트 임시 파일 생성 시 `/tmp/second-opinion-*.md`에 저장한다.” 46행도 동일 경로군의 생성·전달만 설명한다.
- 문제 상황: 제목은 삭제나 cleanup 의무처럼 보이지만 본문에는 정리 시점·대상·명령이 없다. 저장 위치를 따르는 것만으로 이 규칙을 충족하는지 읽는 사람이 다르게 해석할 수 있다.
- 예상 영향: 별도 cleanup 의무를 추측하거나 필요 없는 작업을 추가할 수 있다. 삭제 누락으로 실제 피해가 발생했다는 finding은 아니다.
- 최소 수정안: 제목을 “임시 파일 경로”로 바꾼다. 이 수정은 현재 명시된 동작과 동일하며 새 삭제 절차를 추가하지 않는다.
- 유지할 계약: 긴 컨텍스트를 지정된 `/tmp` 경로군에 저장해 전달하는 동작.
- 소유자: `second-opinion` Hard Rules.
- 검증 상태: 제목/본문 의미 차이를 정적으로 확인했다. runtime 비용 변화는 측정하지 않았다. spec 결정 불필요.

## 런타임 차이와 의존성

- Claude 전용 SKILL 전문을 읽었다. `references/` 등 local 직접 참조 파일은 없다. Codex 짝 부재는 [components](../../../_sdd/spec/components.md) 54행에 명시된 정상 계약이다.
- AGENTS.md, `_sdd/env.md`, 공통 review 기준, global spec의 dispatch·read-only·AC 관련 절, components의 해당 스킬/플랫폼 행, marketplace 등록과 README 183행을 확인했다.
- `codex:codex-rescue`는 호출 이름만 저장소에 존재하고 그 정의를 이 저장소에서 찾지 못했다. 외부 설치 위치, 인증, 도구 권한, 같은 `/tmp` namespace 접근 여부, 응답 형식과 실제 Codex 모델 실행은 미검토다. 이 제한을 agent가 없거나 지원되지 않는다는 단정으로 바꾸지 않았다.
- `Agent(Explore)` 수집 위임은 SKILL의 명시된 선택지이며, 이번 리뷰에서는 agent를 만들지 않았다. 소유권·반환 원문 계약을 확인하는 데 필요하지 않은 다른 스킬은 확장 탐색하지 않았다.

## 권장 처리 순서와 검증

1. second-opinion-01의 dependency/dispatch 정책을 먼저 결정한다. 지원되는 호출 경로가 확정되기 전에는 agent 이름만 바꾸지 않는다.
2. second-opinion-02/03을 반영한다. 짧은 인라인 컨텍스트와 긴 파일 컨텍스트 각각에서 read-only 제약·질문 원문이 전달되고, 정상 응답을 편집 없이 반환하는지 확인한다. 대상 파일이 바뀌지 않아야 한다.
3. 외부 adapter 미가용·인증 오류·컨텍스트 파일 접근 실패를 모의 응답으로 확인한다. 원인이 그대로인 동안 재시도하지 않고 실패와 미충족 AC를 명시해야 한다. second-opinion-04는 제목 한 곳만 정리하면 된다.

이번 리뷰는 외부 reviewer CLI나 스킬을 실행하지 않았고 제안을 적용하지 않았다. 보고서 상대 링크·파일 권한·whitespace만 정적으로 검증한다.
