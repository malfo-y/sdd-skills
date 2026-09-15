# spec-upgrade 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/spec-upgrade/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/spec-upgrade/SKILL.md)
- 판정 요약: 수정 필요 3 / 정리 후보 0 / 실행 검증 필요 0
- 집계 주의: spec-upgrade-02는 `spec-create`와 공유하는 하네스 병합 finding이다. 전체 집계에서는 소유자 기준으로 중복 제거한다.

## 역할과 유지할 계약

기존 section/inventory 중심 스펙을 thin global model로 옮긴다. migration과 구조 재편의 경계를 먼저 판정하고, 중요한 근거를 보존하면서 feature 실행 정보는 적절한 supporting/temporary surface로 내린다. 선택한 local template을 작성 직전에 읽으며, 하네스와 양 runtime 훅을 함께 보완한다. 구현 코드 read-only, 사용자 설정·원문 보존, Codex trust 수동 경계, runtime-local reference의 독립 배포를 유지한다.

## 기준별 판정

| 기준 | 판정과 근거 |
|---|---|
| 1. 적용 조건 | spec-upgrade-01: rewrite/no-spec 경로가 있으나 해당 경로의 종료와 AC 적용 범위가 닫히지 않는다. mapping·format·template의 조건부 읽기 조건은 명확하다. |
| 2. 충돌과 우선순위 | spec-upgrade-02: 마커 밖 절대 보존과 중복본 제거가 같은 입력에서 상충한다. spec-upgrade-01: reference가 허용한 partial 결과와 전체 Verify 통과 의무가 충돌한다. spec-upgrade-03: 하네스 template의 조건부 줄 삭제 예외가 consumer의 삭제 금지에 반영되지 않았다. |
| 3. 확인·승인 경계 | 수정 필요 없음. Migration Checkpoint는 보고할 내용을 열거하며 별도 승인 대기를 강제하지 않는다. Codex trust는 필요한 사용자 경계로 유지한다. |
| 4. 중복과 소유권 | spec-upgrade-02는 spec-create 소유 공통 병합 정책으로 통합할 대상이다. hook contract를 본문에 재구현하지 않고 local reference에 위임하는 구조는 적절하다. |
| 5. 완료·복구 조건 | spec-upgrade-01: 성공, 이관/비대상, 외부 입력이 필요한 partial 결과를 같은 전체 AC 복귀 규칙으로 처리한다. |
| 6. 절차의 필요성 | 수정 필요 없음. 7단계는 경계 판정·자료 수집·쓰기·하네스·검증 역할로 나뉜다. compact 기본과 조건부 full, local asset load는 현행 spec 결정이며 단계 수만으로 줄일 근거는 없다. |

## Findings

### spec-upgrade-01 — 이관·비대상·partial 결과에도 전체 migration 완료를 요구한다 [수정 필요]

- 기준: 1, 2, 5
- 적용 runtime: Claude, Codex
- 근거: 양 runtime [SKILL](../../../.claude/skills/spec-upgrade/SKILL.md) / [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-upgrade/SKILL.md) 58행은 “rewrite 성격이 우세하면 upgrade로 밀어붙이지 말고 `spec-rewrite`로 분기한다.”라고 한다. Error Handling 208행은 spec이 없으면 “`/spec-create` 먼저 권장”, 212행은 구조 재편이 핵심이면 “`spec-rewrite` 후보로 보고”하도록 한다. 반면 216행은 “Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.”라고 하며 AC 20–28행은 migration 및 하네스·훅 완료를 요구한다.
- partial 설치의 직접 근거: SKILL 189행은 local reference의 “`Verify` checklist를 모두 만족하고 partial 설치가 보완”되었는지 검사한다. [Claude hook contract](../../../.claude/skills/spec-upgrade/references/hook-installation.md) / [Codex hook contract](../../../plugins/sdd-skills-codex/skills/spec-upgrade/references/hook-installation.md) 63행은 malformed JSON이면 “preserve its bytes and skip registration for that runtime” 후 다른 runtime을 계속하고 partial failure를 보고하라고 한다. 같은 reference 152행은 각 runtime의 완전한 group 일치를 요구한다.
- 문제 상황: (a) 도메인 재분할이 핵심이라 upgrade를 중단하고 rewrite로 이관해야 한다. 이관을 마쳐도 upgrade 자체의 migration/harness AC는 미충족이다. (b) 스펙이 없어 spec-create를 권장한다. (c) 한 runtime 설정 JSON이 깨져 보존·skip했는데 전체 Verify를 통과할 수 없다. 세 경로 모두 현행 Final Check를 문자 그대로 적용하면 해결할 단계가 없는 상태에서 복귀 지시가 남는다.
- 예상 영향: 범위 밖 migration을 계속하거나 같은 partial 상태를 재시도할 수 있으며, 정상적인 이관·제한 결과를 완료/미완료 중 무엇으로 보고할지 일관되지 않다. 실제 재시도나 설정 손상은 관측하지 않았다.
- 최소 수정안: Step 1/Error Handling에 rewrite 이관과 no-spec 권장 후 종료를 명시하고 후속 migration 단계 및 그 AC를 적용하지 않는다. migration을 수행한 실행에는 기존 전체 AC를 유지한다. malformed settings처럼 현재 권한·입력으로 해소할 수 없는 항목은 reference대로 보존·partial 보고하고 종료하며, 성공으로 표시하지 않는다. 재실행은 원인 입력이 바뀐 후로 제한한다. 새 상태 파일이나 별도 승인 단계는 필요 없다.
- 유지할 계약: 실제 upgrade의 AC 검증, evidence 없는 완료 금지, rewrite 경계, malformed 파일 원문 보존, 반대 runtime 설치 계속, trust 자동 승인 금지.
- 소유자: upgrade의 분기 종료·최종 검증 적용 범위는 `spec-upgrade` SKILL. partial Verify 자체의 공통 정책은 `spec-create`가 소유하는 canonical hook reference와 조정한다. trust 완료 의미는 global spec의 기존 경계를 따르며 partial을 성공으로 바꾸지 않는다.
- 검증 상태: 두 SKILL, local hook reference, 이관 대상 `spec-rewrite`의 진입·no-rewrite 종료 규칙을 정적으로 대조했다. 런타임 실행 미검증.

### spec-upgrade-02 — 마커 밖 보존과 중복 제거가 같은 범위를 동시에 지시한다 [수정 필요]

- 기준: 2, 4
- 적용 runtime: Claude, Codex
- 근거: 양 runtime [SKILL](../../../.claude/skills/spec-upgrade/SKILL.md) / [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-upgrade/SKILL.md) 141행은 “마커 밖 기존 내용은 아래에 그대로 보존한다.”, 142행은 “마커 밖 내용은 건드리지 않는다.”라고 한다. 바로 다음 143행은 기존 테스트 명령 등 하네스 슬롯과 겹치는 항목이나 legacy `## SDD란` 정보를 흡수하고 “마커 밖 중복본은 제거한다.”라고 한다. 150행과 AC 26행은 중복 `## SDD란`이 남지 않는 것을 완료 조건으로 둔다.
- 문제 상황: 기존 SDD-HARNESS 마커 밖에 과거 생성된 `## SDD란` 블록과 테스트 명령이 있다. 마커-only 교체로 외부 내용을 보존하면 중복 제거 AC에 실패하고, 중복본을 제거하면 마커 밖 불변 지시를 위반한다. 사용자 작성 SDD 설명이 섞여 있으면 무엇을 삭제 가능한 legacy 산출물로 인정할지도 중요해진다.
- 예상 영향: legacy 중복 잔존 또는 보존 범위를 과도하게 좁힌 삭제가 가능하다. 실제 파일 삭제를 관측한 finding은 아니다.
- 최소 수정안: “마커 밖은 보존하되, 아래 중복 흡수 조건으로 식별한 생성 블록만 예외”처럼 예외 우선순위를 명시한다. legacy 생성물로 식별되지 않거나 사용자 수정이 섞인 블록은 원문을 보존하고 미해결 중복을 보고한다. 삭제가 필요한 사용자 내용은 기존 파괴적 변경 승인 경계를 따른다.
- 유지할 계약: verbatim 하네스 병합, 멱등성, 식별 가능한 legacy 중복 정리, 사용자 고유 내용 보존. 하네스 설치를 새 opt-in으로 바꾸지 않는다.
- 소유자: **공통 정책 owner `spec-create`**. spec-upgrade는 기존 소비 repo의 legacy 흡수 경로를 가진 적용 지점이다. [spec-create 리뷰](./spec-create.md)와 통합해 한 finding으로 집계하고, 결정된 예외를 두 producer·두 runtime에 일관되게 적용한다.
- 검증 상태: spec-upgrade 양 runtime 지시의 동일 입력 충돌을 확인했다. spec-create 전체 병합 경로 평가는 해당 리뷰가 소유한다. 실행 미검증.

### spec-upgrade-03 — 하네스의 test/lint 부재 예외가 verbatim 적용 규칙에서 빠졌다 [수정 필요]

- 기준: 2, 4
- 적용 runtime: Claude, Codex
- 근거: 양 runtime [SKILL](../../../.claude/skills/spec-upgrade/SKILL.md) / [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-upgrade/SKILL.md) 136행은 “`<…>` 꺾쇠 슬롯만 repo 값으로 치환하고, 그 외 어떤 줄도 추가·삭제·재배열·요약하지 않는다.”라고 한다. [Claude 하네스 template](../../../.claude/skills/spec-upgrade/references/agents-harness-template.md) / [Codex 하네스 template](../../../plugins/sdd-skills-codex/skills/spec-upgrade/references/agents-harness-template.md) 21행은 테스트·린트 명령에 대해 “repo 변수, 없으면 줄 삭제”를 지시한다.
- 문제 상황: 테스트·린트 명령이 없는 문서 전용 repo를 upgrade한다. template대로 줄을 삭제하면 SKILL의 줄 삭제 금지를 어기고, 유지하면 reference가 정한 조건부 삭제를 따르지 못한다.
- 예상 영향: 명령이 없는 placeholder나 무의미한 테스트 줄을 남기거나 verbatim 검증에 실패할 수 있다. 실제 산출물은 미관측이다.
- 최소 수정안: Step 6의 보존 규칙에서 “reference가 명시한 조건부 줄 삭제는 허용한다”는 예외를 선언한다. 허용 대상을 임의 편집 전체로 넓히지 않는다.
- 유지할 계약: local 하네스 전문 읽기, 허용된 슬롯 치환과 조건부 삭제 외 원문 보존, §0–§5 구조, 재실행 멱등성.
- 소유자: **spec-upgrade 고유 consumer 누락**. [Claude spec-create](../../../.claude/skills/spec-create/SKILL.md) / [Codex spec-create](../../../plugins/sdd-skills-codex/skills/spec-create/SKILL.md) 161–167행에는 일반 삭제 금지 뒤 슬롯별 test/lint 줄 삭제 예외가 이미 있다. canonical template 수정이나 spec-create의 별도 branch 슬롯 문제와 합치지 않는다.
- 검증 상태: 하네스 template 및 두 producer의 해당 절을 직접 대조했다. 실행 미검증.

## 런타임 차이와 의존성

- 양 runtime SKILL은 동일하다. `template-compact.md`의 `/guide-create` 대 `$guide-create`는 의도된 invocation 차이이며, 그 외 조사한 spec-upgrade 자산은 byte 비교에서 동일했다.
- 읽은 reference: 양 runtime의 `upgrade-mapping.md`, `spec-format.md`, `template-compact.md`, `template-full.md`, `agents-harness-template.md`, `hook-installation.md`. Claude 전문을 읽고 Codex 동일성 및 compact의 실제 차이를 대조했다. `examples/after-upgrade.md`도 읽었다.
- 필요한 이웃 계약: 양 runtime `feature-draft`의 `Required Output`과 그 규칙, Claude `spec-rewrite`의 진입·경계·no-rewrite 종료 절. 스킬을 실행하지 않았다.
- hook reference와 하네스 template은 spec-create canonical과 byte-identical했다. 설치 자산인 4개 hook script는 runtime parity만 비교했으며, 스크립트 본문의 correctness와 호스트 hook 지원·실제 lifecycle은 미검토다. Codex 기능 부재를 추정하지 않는다.
- spec-create의 하네스 복사·슬롯 처리 절도 대조했다. spec-upgrade-03은 canonical template의 결함이 아니라 consumer의 예외 누락으로 분리했다.
- 언어 보존과 영문 template heading의 범위도 살폈다. 기존 문서가 혼합 언어 heading을 허용할 수 있어, 이 스킬 문면만으로 모든 영문 heading을 요구 위반이라고 단정하지 않았다.

## 권장 처리 순서와 검증

1. spec-upgrade-01에서 이관·no-spec·partial 종료를 성공과 구분한다. fixtures는 rewrite가 핵심인 문서, spec 없는 repo, 한 runtime만 malformed JSON인 repo 세 가지면 된다. 각각 후속 migration의 실행 여부·원문 보존·정확한 잔여 항목 보고를 확인한다.
2. spec-upgrade-02는 spec-create 소유 공통 정책으로 통합한다. 마커 밖의 식별 가능한 legacy 블록과 사용자 수정 블록을 함께 둔 fixture에서 보존·제거 경계를 확인하고 두 번째 병합의 무변경을 확인한다.
3. spec-upgrade-03의 예외를 반영하고 test/lint 명령이 없는 repo에서 조건부 줄만 제거되는지 확인한다. 실제 migration 성공 경로에서는 기존 전체 AC와 양 runtime 설치 검증을 유지한다. 변경 후 mirror parity와 `git diff --check`를 확인한다. 이번 리뷰는 정적 지시 검토이며 위 실행은 수행하지 않았다.
