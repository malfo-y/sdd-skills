# sdd-autopilot 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/sdd-autopilot/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/sdd-autopilot/SKILL.md)
- 판정 요약: 수정 필요 1 / 정리 후보 1 / 실행 검증 필요 0

## 역할과 유지할 계약

사용자 기능 목표와 context를 설치된 runtime-local `goal-init(preset=sdd)`에 전달하는 setup adapter다. 목표 수집·조건 self-check·5단계·4파일·SDD Loop Protocol의 소유권은 `goal-init`에 유지하고, 조건과 실행법·파일 경로를 사용자에게 전달한 뒤 끝낸다. setup 중 producer 실행·native goal 활성화·status 조회·상태 변경을 하지 않으며, 이미 active goal이 있어도 setup을 막지 않는다. 활성화 여부와 시점은 사용자가 결정한다.

근거: [global spec](../../../_sdd/spec/main.md) 92–97행, 138행. 5단계·4파일 자체를 줄이는 제안은 이번 리뷰 대상이 아니다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | `sdd-autopilot-01`: 성공 완료용 AC 재시도가 명시적 실패 종료와 과거 위반에도 무조건 적용되는 문면이다. setup-only 진입 범위 자체는 명확하다. |
| 2. 충돌과 우선순위 | `sdd-autopilot-01`: setup 실패 때 종료하라는 지시와 미충족 AC가 있으면 돌아가라는 지시 사이 우선순위가 없다. |
| 3. 확인·승인 경계 | 수정 필요 없음. wrapper는 추가 승인을 요구하지 않으며 native goal activation을 사용자에게 남긴다. 자율 수준·사전 승인 수집은 `goal-init`에 위임되어 있다. |
| 4. 중복과 소유권 | `sdd-autopilot-02`: 사용자 Handoff 출력 의무가 위임 스킬과 wrapper에 각각 있다. intake·self-check·파일 생성 절차는 재구현 금지와 포인터로 결속되어 있어 중복 실행 결함으로 판정하지 않는다. |
| 5. 완료·복구 조건 | `sdd-autopilot-01`: 수정 가능한 누락, 실패 종료, 되돌릴 수 없는 과거 경계 위반을 구분해야 한다. |
| 6. 절차의 필요성 | 수정 필요 없음. wrapper의 입력 구성→위임→relay는 역할에 맞는다. AC 섹션과 종료 전 자체 검증, 5단계·4파일은 현행 spec 계약이다. |

## Findings

### sdd-autopilot-01 — 실패 종료와 과거 경계 위반을 AC 재시도에서 구분하지 않는다 [수정 필요]

- 기준: 1, 2, 5.
- 적용 runtime: Claude, Codex.
- 근거: [Claude](../../../.claude/skills/sdd-autopilot/SKILL.md) 14, 16–18, 52–57행; [Codex](../../../plugins/sdd-skills-codex/skills/sdd-autopilot/SKILL.md) 14, 16–18, 51–56행.
- 정확한 원문:
  - Error Handling: “4파일 setup 실패” → “실패를 보고하고 종료한다.”
  - Final Check: “미충족 항목이 있으면 해당 단계로 돌아가 수정한다.”
  - AC3: “setup 중 initial `feature-draft`·`implementation`·`spec-sync` 실행, current native goal status 조회, native goal 상태 변경이 모두 0건이다.”
- 문제 상황: 쓰기 권한 부족 등으로 `goal-init`이 4파일 생성을 실패한 경우 AC1·AC2가 미충족이므로, Error Handling은 종료를 지시하고 Final Check는 같은 setup 단계로 복귀시킨다. 별도로 setup 중 status 조회가 이미 1회 일어났다면, 이후 산출물을 고쳐도 그 실행의 AC3는 0건이 될 수 없다. 일반 수정 루프는 이 과거 위반을 복구할 수 없다.
- 예상 영향: 명시적인 실패 결과를 반복 setup으로 바꾸거나, 과거 위반을 해소할 수 없는 재시도를 유도할 수 있다. 실제 반복 실행 또는 허위 완료가 관측되었다는 뜻은 아니다.
- 최소 수정안: 성공 완료 전 자체 검증은 유지하되, “정상 완료 경로에서 수정 가능한 누락은 해당 단계로 돌아간다. Error Handling의 실패·중단 경로는 사유와 미충족 AC를 보고하고 종료한다. 이미 발생한 AC3 위반은 복구 완료로 표시하지 않고 발생 사실을 보고한다”로 분기한다. 위반이 실제 발생했으면 Handoff의 고정 불변식 문장도 사실과 다르게 그대로 출력하지 않도록 한다.
- 유지할 계약: AC를 생략하거나 실패를 성공으로 인정하지 않는다. 정상 setup 누락은 수정한다. producer 실행·goal 조회·변경 금지와 실패 시 우회 금지는 그대로 유지한다.
- 소유자: `sdd-autopilot` SKILL 짝. 공통 AC 문구의 해석은 [global spec](../../../_sdd/spec/main.md) 92행 소유자와 함께 정리해야 한다. `goal-init`에도 동일한 실패 중단/Final Check 결합이 있으므로 그 리뷰 소유자와 연결한다([Claude goal-init](../../../.claude/skills/goal-init/SKILL.md) 62, 123, 130행; [Codex goal-init](../../../plugins/sdd-skills-codex/skills/goal-init/SKILL.md) 동일 행).
- 검증 상태: 정적 문구 충돌 확인. 실패 종료를 성공 완료와 구분하는 공통 문구 조정은 **spec 결정 필요**다. 실패 주입·실제 스킬 실행은 하지 않았다.

### sdd-autopilot-02 — goal-init Handoff와 wrapper relay의 출력 책임을 합칠 수 있다 [정리 후보]

- 기준: 4.
- 적용 runtime: Claude, Codex.
- 근거: [Claude sdd-autopilot](../../../.claude/skills/sdd-autopilot/SKILL.md) 38, 42–44행; [Codex sdd-autopilot](../../../plugins/sdd-skills-codex/skills/sdd-autopilot/SKILL.md) 37, 41–43행; [Claude goal-init](../../../.claude/skills/goal-init/SKILL.md) 109–117행; [Codex goal-init](../../../plugins/sdd-skills-codex/skills/goal-init/SKILL.md) 동일 행.
- 정확한 원문:
  - wrapper Step 2: “기존 5단계와 모든 Decision Gate를 통과하고 4파일을 생성할 때까지”
  - `goal-init` Step 5: “확정한 **조건 문자열 전문**” 및 “개별 경로”를 “사용자에게 제시한다.”
  - wrapper Step 3: “`goal-init`이 확정한 조건 문자열”과 실행법·개별 경로를 “사용자에게 제시한다.”
- 문제 상황: 위임한 `goal-init`이 Step 5까지 사용자에게 전문·실행법·경로·불변식을 출력한 뒤 wrapper Step 3으로 돌아오는 경로에서 동일한 출력 의무가 다시 나타난다. 현재 문면은 이미 표시한 Handoff를 wrapper relay의 충족 증거로 인정하는지 명시하지 않는다.
- 예상 영향: 같은 긴 조건 문자열과 경로가 중복 표시될 여지가 있다. 실제 표시 횟수와 비용은 측정하지 않았으므로 중복 실행 결함으로 단정하지 않는다. 5단계 자체를 wrapper가 다시 수행하라는 지시는 없다.
- 최소 수정안: Step 3을 “`goal-init`의 Handoff를 최종 relay로 사용한다. 이미 사용자에게 표시된 항목은 다시 출력하지 않고, 자율 수행 위임 등 아직 전달하지 않은 필수 항목만 보충한다. 사용자에게 아직 노출되지 않은 반환이면 Handoff 전문을 전달한다”로 명확히 한다.
- 유지할 계약: `goal-init`은 독립 호출에서도 5단계 전체를 수행한다. wrapper 최종 전달에는 조건 문자열 전문·자율 수행 위임·runtime 실행법·4파일 개별 경로·setup 불변식이 모두 있어야 한다. relay 의무나 AC 섹션을 삭제하지 않는다.
- 소유자: `sdd-autopilot` Step 3. `goal-init` Step 5는 독립 호출 Handoff의 소유자이며, wrapper가 그 결과를 재사용하는 방향이면 변경할 필요가 없다.
- 검증 상태: 정적 출력 의무 중첩 확인. 후보 문구의 목표는 결과 유지와 책임 정리이며, 실제 이중 출력 관측은 없다.

## 런타임 차이와 의존성

- Claude는 `sdd-skills:goal-init`의 plugin prefix를 강제한다. Codex는 active installed skill catalog에서 이름으로 고르고 workspace-relative 경로를 가정하지 않는다. [global spec](../../../_sdd/spec/main.md) 93행의 정당한 runtime 차이다.
- 두 wrapper는 runtime 실행법 이름 외에 같은 setup·relay·AC 계약을 가진다. 둘 사이 배포 mirror 자체는 finding이 아니다.
- 직접 검토: runtime별 `sdd-autopilot/SKILL.md`, `goal-init/SKILL.md`, [Claude harness template](../../../.claude/skills/goal-init/references/harness-templates.md), [Codex harness template](../../../plugins/sdd-skills-codex/skills/goal-init/references/harness-templates.md). template는 공통 본문과 runtime diff를 대조했다. 공통 SDD payload와 4파일 구조는 같은 계약이며, 실행법 슬롯은 runtime에 맞게 다르다.
- 판단 기준으로 `AGENTS.md`, `_sdd/env.md`, global spec의 AC·goal·gate 관련 절, [공통 리뷰 기준](review-criteria.md), [제작 규범](../../SKILL_AUTHORING_NORMS.md)을 읽었다.
- `goal-init`이 소유하는 질문·가설 수·native goal 실행법·template loop의 개별 정확성은 별도 `goal-init` 리뷰의 범위다. 이번 wrapper 리뷰는 실행법의 실제 runtime 지원 여부나 모델 행동 효과를 주장하지 않는다.
- 미검토: 실제 설치본/host runtime, producer 스킬의 실행, native goal 활성화 이후 전체 루프. setup 단계에서 실행하지 않는 하류 producer를 추가로 조사하지 않았다.

## 권장 처리 순서와 검증

1. 공통 AC 소유자와 실패 종료·과거 위반의 처리 의미를 정하고, 양쪽 wrapper Final Check에 정상 완료와 실패 종료의 경계를 반영한다. 적합성 실패, 파일 생성 실패, 과거 AC3 위반 각각이 성공으로 표시되지 않는지 확인한다.
2. wrapper Step 3의 Handoff 재사용 문구를 정리한다. `goal-init` 독립 호출과 `sdd-autopilot` 경유 호출 모두 사용자에게 필수 Handoff가 한 번 온전히 전달되는지 확인한다.
3. 후속 변경 시 짝 diff와 `git diff --check`를 확인한다. 동작 검증은 변경본이 로드되는 별도 세션에서 정상 setup·쓰기 실패·적합성 실패를 실행해 transcript로 종료 분기와 출력 횟수를 확인한다. native goal 상태 조회·변경 없이 setup을 마치는 계약은 그대로 둔다.

이번 작업에서는 보고서만 작성했으며 대상 스킬의 실행·수정 및 위 동작 검증은 하지 않았다.
