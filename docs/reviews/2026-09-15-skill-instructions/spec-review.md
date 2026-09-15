# spec-review 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/spec-review/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/spec-review/SKILL.md)
- 판정 요약: 수정 필요 2 / 정리 후보 0 / 실행 검증 필요 0

## 역할과 유지할 계약

Global/temporary spec을 구분해 문서 품질과 코드 정합성을 감사하고, spec 본문을 수정하지 않은 채 `_sdd/spec/logs/spec_review_report.md`에 결과를 남긴다. 메인 직접 실행, 공통 4축 rubric, evidence 기반 severity, `UNTESTED` 우선 drift 판정, spec 변경 필요 여부만 나타내는 Decision, 후속 조치 제안과 종료 전 AC 자체 검증을 유지한다. Simplicity dispatch와 producer 품질 게이트를 추가하지 않는다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | spec-review-01: 현행/legacy를 구분한 quality rubric과 달리 delta ID 검사는 무조건 적용된다. |
| 2. 충돌과 우선순위 | spec-review-01: 현행 feature-draft의 AC 중심 계약과 맞지 않는다. spec-review-02: global spec이 요구한 review SKILL 배칭 지시가 없다. Drift Status와 Decision의 우선순위 자체는 명확하다. |
| 3. 확인·승인 경계 | 수정 필요 없음. 별도 승인 질문을 강제하지 않으며, spec 변경은 후속 제안으로 남기는 명시적인 review-only 역할이다. |
| 4. 중복과 소유권 | 수정 필요 없음. 판정은 Step 3/4가 소유하고 출력은 이를 참조한다. runtime 짝의 동일 문면은 배포 mirror다. feature-draft 수정 없이 소비자 검사만 고치면 된다. |
| 5. 완료·복구 조건 | 수정 필요 없음. evidence 부족·접근 실패·양쪽 부재를 UNTESTED로 구분하고, 입력 부족은 한계 보고로 처리한다. AC 자체 검증이 있다. 실제 종료 동작은 검증하지 않았다. |
| 6. 절차의 필요성 | spec-review-02: 독립 읽기 호출을 묶으라는 현행 계약이 배포 본문에 빠졌다. Optional Code Analysis는 finding을 뒷받침할 때만 수행하므로 고정 metric 의무는 없다. |

## Findings

### spec-review-01 — 현행 draft에도 delta ID 연결을 무조건 요구함 [수정 필요]

- **기준 / runtime**: 1, 2 / Claude·Codex 공통.
- **위치와 원문**: [Claude SKILL](../../../.claude/skills/spec-review/SKILL.md) 117행, [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-review/SKILL.md) 117행: “delta ID와 validation evidence의 연결 확인”. 같은 파일 76행은 구형 구조 점검을 “legacy full draft 기록물을 감사할 때만”으로 제한한다.
- **직접 대조**: [Claude feature-draft](../../../.claude/skills/feature-draft/SKILL.md) 및 [Codex feature-draft](../../../plugins/sdd-skills-codex/skills/feature-draft/SKILL.md) 59–94행의 정본 template은 Change Summary·Scope·Task·Contracts·AC·Target Files를 정의하며 delta ID를 요구하지 않는다. [SDD_SPEC_DEFINITION](../../../docs/SDD_SPEC_DEFINITION.md) 162–173행은 각 task의 AC를 검증의 단일 정의 지점으로 두고 구형 매핑은 기록물에만 적용한다.
- **문제 상황**: 현행 template으로 작성된 정상 draft와 구현의 AC 증거를 리뷰한다. quality 단계에서는 현행 rubric을 고르지만 drift 단계는 존재하지 않는 delta ID를 통한 연결 확인을 다시 요구한다.
- **예상 영향**: AC로 확인 가능한 정합성에 구형 앵커 검사를 추가한다. 불필요한 누락/UNTESTED 판단이나 delta ID 추가 권고로 이어질 여지가 있다. 실제 오판 발생은 관측하지 않았다.
- **최소 수정안**: 해당 bullet을 “현행 draft는 task/AC와 validation evidence의 연결을 확인한다. delta ID가 있는 legacy 기록물은 해당 ID의 연결을 확인한다”로 제한한다. 구체적인 현행 output 구조는 same-runtime feature-draft의 Required Output을 참조한다.
- **유지할 계약**: 검증 증거 연결을 생략하지 않는다. legacy 기록물의 기존 ID 추적도 유지하고, 새 draft에 필드를 추가하지 않는다.
- **소유자**: spec-review 양 runtime. Cross-skill 계약 소유자는 feature-draft이며 producer 변경은 불필요하다. 현행 spec 결정을 바꾸는 제안이 아니다.
- **검증 상태**: 양 runtime의 정확한 문면과 producer template을 대조한 정적 finding. 대상 스킬 미실행.

### spec-review-02 — review SKILL에 요구된 독립 읽기 배칭 지시가 없음 [수정 필요]

- **기준 / runtime**: 2, 6 / Claude·Codex 공통.
- **위치와 원문**: [Claude SKILL](../../../.claude/skills/spec-review/SKILL.md) 및 [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-review/SKILL.md) 87–119행은 “다음 입력을 찾는다”, “코드/테스트/구현 문서와 대조한다”로 읽기를 지시하지만, 전체 220행에 독립 read-only 호출의 배칭 규칙이 없다. [global spec](../../../_sdd/spec/main.md) 62행은 “review·구현 계열 SKILL은 **서로 의존하지 않는 read-only 호출의 한 메시지 배칭을 지시형으로 요구한다**”고 명시한다.
- **문제 상황**: 사용자 지정 spec과 이미 확정된 구현·테스트 경로처럼 서로 결과를 기다릴 필요가 없는 입력을 읽는다. spec-review 배포 본문에는 global spec이 요구한 실행 규칙이 전달되지 않는다.
- **예상 영향**: 저장소에서 선언한 review 실행 계약과 배포 SKILL 지시가 불일치한다. 이 누락 때문에 실제 호출이 직렬화되었다거나 배칭이 시간을 절감한다고 주장하는 finding은 아니다.
- **최소 수정안**: Process에 한 번만 “서로 의존하지 않는 read-only 호출은 한 메시지로 묶는다. 앞 결과로 대상이 정해지는 호출과 쓰기·상태 변경은 분리하며, 배칭 때문에 읽을 범위를 넓히지 않는다”를 추가한다.
- **유지할 계약**: 메인 직접 실행, 기존 scope, 의존 관계 순서, 단일 리포트 작성. Subagent나 추가 분석 절차를 도입하지 않는다.
- **소유자**: spec-review 양 runtime. 공통 계약 소유자는 global spec Guardrails이며 정책 변경은 불필요하다.
- **검증 상태**: 전체 본문과 global spec을 대조한 계약 누락. 모델 행동·시간 효과 미검증.

## 런타임 차이와 의존성

- 두 spec-review SKILL은 `diff -u` 결과가 없으며 byte-identical하다. 이 스킬은 dispatch가 없으므로 별도 lifecycle adapter를 요구하지 않는다.
- 읽은 범위: AGENTS.md, global spec의 관련 Guardrails·설계 결정·운영 제약, `_sdd/env.md`, 공통 리뷰 기준, 두 spec-review 본문 전체, 두 feature-draft Required Output 및 AC 규칙, SDD_SPEC_DEFINITION의 temporary spec 정의.
- 별도 runtime-local reference 파일 링크는 없다. `spec-sync`·`implementation-review`는 실행 위임이 아닌 후속 제안 목록이다. 이번 판정에 그 실행 계약 전체가 필요하지 않아 전문은 미검토했으며, 해당 스킬의 동작에 대한 판정은 하지 않는다.

## 권장 처리 순서와 검증

1. spec-review-01의 소비자 앵커를 현행 AC / legacy delta ID로 나눈다. 현행 정상 draft에서 delta ID 부재가 결함으로 보고되지 않고 AC 증거가 연결되는지, legacy 기록물에서는 기존 ID 연결이 유지되는지 확인한다.
2. spec-review-02의 배칭 문구를 양 runtime 같은 위치에 추가한다. 동일 source 범위와 의존성을 유지하는지 diff로 확인한다. 행동 효과를 판단하려면 설치본이 갱신된 별도 실행의 실제 tool 호출을 관찰해야 한다.
3. 양 runtime parity와 `git diff --check`를 확인한다. 이번 리뷰는 보고서만 작성했으며 위 변경과 스킬 실행 검증은 하지 않았다.
