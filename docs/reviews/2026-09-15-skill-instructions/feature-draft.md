# feature-draft 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/feature-draft/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/feature-draft/SKILL.md)
- 판정 요약: 수정 필요 1 / 정리 후보 1 / 실행 검증 필요 0

## 역할과 유지할 계약

대화의 요구를 실측 Target Files와 반증 가능한 AC를 가진 task로 바꾸고, draft 하나와 producer 소유 plan-review 게이트 결과를 남긴다. 전체 변경이 감당되지 않으면 Part 1에 분할 feature 목록을 남기고 Part 2는 첫 feature만 구체화한다.

AC 자체 검증, dated slug와 마커 쌍, minimum-code, 필수 census 검증, 직접 작성, gate 1과 조건부 gate 2의 고정 임계·최대 두 번·producer fix를 유지한다. gate를 제거하거나 임계를 바꾸는 제안은 없다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | feature-draft-02: 분할 전 전체 범위와 분할 후 현재 feature의 task 범위를 명시하면 AC3의 해석이 쉬워진다. 질문은 로컬 탐색으로 닫히지 않고 설계·범위·파일에 영향을 주는 unknown으로 제한되어 있다. |
| 2. 충돌과 우선순위 | feature-draft-01: 다른 task 결과를 보는 완료 판정 금지와 선행 산출물 의존·마지막 census task 허용 사이의 경계가 빠져 있다. |
| 3. 확인·승인 경계 | 수정 필요 없음. 질문 발동 조건과 무인 대체가 있고, 게이트 반환 직후 fix·조건부 재호출을 사용자 입력 없이 계속하도록 명시한다. |
| 4. 중복과 소유권 | 수정 필요 없음. output은 fenced template, 규모는 producer, review는 plan-review, 수정은 producer가 소유한다. 런타임 짝은 배포 mirror다. |
| 5. 완료·복구 조건 | feature-draft-01·02의 범위 해석을 제외하면 수정 필요 없음. 자체 AC, gate 호출 상한, gate 2 후 재확인·미해소 보고가 명시되어 있다. |
| 6. 절차의 필요성 | 수정 필요 없음. 열거→배정→순서는 coverage와 단일 owner를 위한 절차다. census task와 두 번째 gate의 발동 조건도 구체적이다. 단순한 길이·강제어 수로 결함을 만들지 않았다. |

## Findings

### feature-draft-01 — 선행 산출물 의존과 완료 판정 금지의 경계 누락 [수정 필요]

- **기준 / runtime**: 2, 5 / Claude·Codex 공통.
- **근거**: [Claude](../../../.claude/skills/feature-draft/SKILL.md) 및 [Codex](../../../plugins/sdd-skills-codex/skills/feature-draft/SKILL.md), 양쪽 35–36·51행.
  - 35행: “다른 task의 결과를 봐야 완료를 판정할 수 있어도 다시 긋는다.”
  - 36행: “뒤 task가 앞 task의 산출물을 쓰면 그 순서로 놓고”
  - 51행: “Part 2 마지막에 read-only 검증 task”를 “필수로 둔다.”
- **문제 상황**: rename task가 파일들을 수정하고 마지막 census task가 그 파일에 구 표기가 남지 않았음을 검사한다. 마지막 task는 자기 AC의 grep 출력으로 완료를 판정하지만, 그 출력은 앞 task의 수정 결과를 확인한 것이다. 35행의 무조건적인 문면은 이 task를 다시 나누도록 요구하고, 51행은 바로 그 검증 task를 요구한다. 일반적인 선행 산출물 소비에서도 같은 해석 문제가 생긴다.
- **예상 영향**: 허용된 순차 의존을 task 경계 오류로 오인하거나 필수 검증 task를 제거·불필요하게 재분할할 수 있다. 실제로 발생했다는 실행 관측은 아니다.
- **최소 수정안**: 35행 마지막 조건을 “선행 task의 확정된 산출물을 입력으로 쓰는 것은 허용하되, 자기 AC로 판정하지 못하고 다른 task의 미완료 작업이나 향후 판정에 기대면 경계를 다시 긋는다”로 좁힌다. 필요하면 census는 이 허용 사례임을 같은 자리에서 짧게 연결한다.
- **유지할 계약**: 한 task의 단일 의도·단일 owner·자기 AC에 의한 판정, 산출물 의존 순서, 필수 census 검증 task. 필수 검증 task 삭제는 해결책이 아니다.
- **소유자**: `feature-draft`. 연결 소비자는 [plan-review](../../../.claude/skills/plan-review/SKILL.md) 44–46행과 [implementation](../../../.claude/skills/implementation/SKILL.md) 31–36행이다. reviewer rubric이나 implementation에 예외 상세를 복제하지 않고 producer에서 뜻을 확정한다.
- **검증 상태**: 원문과 소비자 계약의 정적 대조 완료. 동작 미검증. 허용 의존을 명료화하는 수정이며 gate·규모·task 단일성의 spec 결정 변경은 요구하지 않는다.

### feature-draft-02 — 분할 후 AC3의 적용 범위를 한곳에서 명시 [정리 후보]

- **기준 / runtime**: 1, 5 / Claude·Codex 공통.
- **근거**: [Claude](../../../.claude/skills/feature-draft/SKILL.md) 및 [Codex](../../../plugins/sdd-skills-codex/skills/feature-draft/SKILL.md), 양쪽 22·34–35·49행.
  - 22행: “모든 변경 요소에 owner task가 정확히 하나 배정되었고”
  - 34행: “이번 변경이 만들거나 바꾸는 요소를 먼저 전수 열거한다”
  - 49행: “Part 2에는 **첫 feature의 task만** 작성한다.”
- **문제 상황**: 세 feature로 나눈 draft에서 Part 1은 전체 변경을, Part 2는 첫 feature만 담는다. AC3의 “모든 변경 요소”가 전체 요청인지 현재 feature인지 명시되지 않았다. 초기 내부 분석에서 전체 owner를 배정하고 첫 feature만 출력하는 해석은 가능하므로, 현 문면을 필연적 충돌로 판정하지 않았다.
- **예상 영향**: 후속 feature의 상세 task를 지금도 작성해야 하는지, 첫 feature 범위만 자체 검증하면 되는지 판단이 갈릴 여지가 있다. 실제 과잉 작성이나 반복은 관측하지 않았다.
- **최소 수정안**: 분할 방법에 “분할 뒤 Part 2와 AC3의 task 단위 검산은 현재 feature 범위에 적용하고, 나머지 변경 범위는 Part 1의 feature별 scope에 보존한다”를 명시하고 AC3는 해당 규칙을 참조한다. 새 표·coverage 산출물은 추가하지 않는다.
- **유지할 계약**: 초기 전수 열거, 변경 범위 보존, 현재 feature의 정확히 한 owner, Part 2 첫 feature 한정, 나머지 feature는 차례에 새 draft 작성.
- **소유자**: `feature-draft`. [spec-sync](../../../.claude/skills/spec-sync/SKILL.md) 65·81행은 Part 1 분할 목록을 소비하는 연결점이며 변경 대상은 아니다.
- **검증 상태**: 정적 범위 모호성 확인. 현재 롤링 분할의 동등한 명료화 후보이며 실행 결함이나 성능 개선을 주장하지 않는다.

## 런타임 차이와 의존성

- `feature-draft` Claude/Codex 파일은 byte-identical하다. 이 스킬은 도구 이름·agent lifecycle에 의존하는 별도 adapter가 필요하지 않다.
- 직접 의존성으로 양 runtime의 `plan-review` 본문을 대조했다. 리뷰는 직접 실행·단일 pass·읽기 전용이고 draft 수정은 feature-draft가 소유한다. plan-review의 런타임별 표현 차이는 별도 리뷰 소유자에게 속한다.
- 양 runtime `implementation`의 입력·의존 순서·중단/분할·Integration 구간, `spec-sync`의 Part 1 입력·상태 분류·분할 feature별 planned 반영 구간을 확인했다. 선행 산출물 의존 및 분할 마커의 소비 계약은 연결되어 있다.
- 공통 근거로 `AGENTS.md`, `_sdd/env.md`, `_sdd/spec/main.md`의 관련 guardrail·품질 게이트·롤링 분할 결정을 읽었다. feature-draft 전용 reference 파일은 없다.
- 미검토: 다른 스킬의 전체 실행 흐름, 설치본과 작업트리 일치, 실제 호출 transcript. `spec-sync`가 입력을 소비한다는 설명만으로 feature-draft 호출이 언제나 global spec까지 수정한다고 단정하지 않았다.

## 권장 처리 순서와 검증

1. feature-draft-01의 한 문장부터 양 runtime에 동일하게 명료화한다. rename 수정 task + 마지막 census task, 선행 API 산출물을 소비하는 후속 task, 향후 미완료 task에 판정을 미루는 잘못된 task를 비교해 앞의 두 경우는 유지하고 마지막 경우만 경계 재설계가 되는지 확인한다.
2. feature-draft-02는 같은 편집에서 범위 한 줄로 정리할 수 있다. 세 feature 분할 입력에서 Part 1은 세 scope를 보존하고 Part 2는 첫 feature만 상세화하는지 확인한다.
3. mirror diff와 `git diff --check`를 수행한다. 이후 실제 skill 검증에서는 설치본에 수정이 발효된 새 세션을 사용하고, gate 1 항상·임계값에 따른 gate 2·최대 두 번·producer fix가 유지되는지 확인한다.

이번 리뷰는 대상 스킬을 호출하거나 수정하지 않았고, 위 실행 확인은 수행하지 않았다.
