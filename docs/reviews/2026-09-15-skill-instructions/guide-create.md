# guide-create 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/guide-create/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/guide-create/SKILL.md)
- 판정 요약: 수정 필요 1 / 정리 후보 1 / 실행 검증 필요 0

## 역할과 유지할 계약

특정 기능의 spec과 code evidence를 연결하는 구현·리뷰 가이드를 만든다. 기능별 dated slug 문서, 작성 직전 runtime-local output reference 읽기, main loop 직접 작성·검증, 확인된 claim과 unknown/assumption 분리, 기존 동명 파일 보존을 유지한다. 가이드는 global spec의 새 source of truth가 아니며 code/config/test를 변경하지 않는다.

## 기준별 판정

| 기준 | 판정과 근거 |
|---|---|
| 1. 적용 조건 | 수정 필요 없음. 기능·scope가 바뀌는 ambiguity만 질문하며, spec/code 부족 시 제한적 작성 경로와 표기법이 있다. |
| 2. 충돌과 우선순위 | guide-create-01: 사용자 지정 언어와 고정 한국어 skeleton 지시의 적용 경계가 충돌한다. guide-create-02: guide 쓰기 제한과 상위 하네스 기록 의무의 범위를 명시할 수 있다. |
| 3. 확인·승인 경계 | 수정 필요 없음. 별도 작성 승인을 요구하지 않으며 동명 파일은 구체적인 slug로 피해 원본을 보존한다. |
| 4. 중복과 소유권 | guide-create-02 정리 후보. output shape/rubric은 reference 한 곳이 소유한다. runtime mirror 자체는 결함이 아니다. |
| 5. 완료·복구 조건 | guide-create-01의 비한국어 작성 시 자체 검증 모순 외 수정 필요 없음. AC와 output interface 대조, placeholder 제거, evidence 한계 보고가 명시돼 있다. |
| 6. 절차의 필요성 | 수정 필요 없음. feature별 순차 작성과 skeleton/fill/finalize는 현행 spec 결정이다. source 없는 error/scenario의 고정 개수를 요구하지 않는다. |

## Findings

### guide-create-01 — 지정 언어와 한국어 skeleton 보존이 동시에 요구된다 [수정 필요]

- 기준: 2, 5
- 적용 runtime: Claude, Codex
- 근거: 양 runtime [SKILL](../../../.claude/skills/guide-create/SKILL.md) / [Codex SKILL](../../../plugins/sdd-skills-codex/skills/guide-create/SKILL.md) 30행은 “문서 언어는 사용자 지정을 우선”이라고 한다. 65행은 “fenced required skeleton을 verbatim 복사해 heading·field order를 유지”하도록 한다. [Claude output-format](../../../.claude/skills/guide-create/references/output-format.md) / [Codex output-format](../../../plugins/sdd-skills-codex/skills/guide-create/references/output-format.md) 17행은 “title·metadata·section order를 유지하고 placeholder만 source-grounded content로 치환한다.”라고 한정한다. 같은 reference 27–48행의 실제 제목·metadata label·section heading은 `# 기능 기술 보고서`, `**생성일**`, `## §1 배경 및 동기` 등 한국어다.
- 문제 상황: 사용자가 “제목과 항목명까지 영어로 가이드를 작성해줘”라고 요청한다. 본문만 영어로 채우면 언어 요구가 미충족이고, 제목·항목명을 번역하면 placeholder-only/verbatim 조건이 미충족이다. 사용자 요청의 우선순위로 작업 자체는 진행할 수 있으나 스킬 내부의 완료 기준이 그 결과를 수용하지 못한다.
- 예상 영향: 혼합 언어 산출물 또는 언어 요구를 맞추고도 format AC가 미충족인 결과를 낼 수 있다. 실제 모델의 선택은 이번 리뷰에서 관측하지 않았다.
- 최소 수정안: reference의 verbatim 적용 문장에 “사용자가 언어를 지정하면 제목·표시 label·heading은 번역하되 계층·순서·필드 의미를 보존한다”는 예외를 한 곳에서 정의하고 SKILL Step 5는 그 예외를 참조한다. 새 언어별 template은 만들지 않는다.
- 유지할 계약: 작성 직전 local reference 읽기, 동일한 5개 section과 metadata 의미·순서, placeholder 제거, source grounding.
- 소유자: `guide-create` output-format 및 SKILL. [global spec](../../../_sdd/spec/main.md) 137행이 verbatim interface를 설계 결정으로 고정하므로 **spec 결정 필요**: 표시 문구 번역이 허용되는 보존 범위를 먼저 명시한다. 다른 producer의 번역 허용 여부는 이 finding으로 자동 변경하지 않는다.
- 검증 상태: 두 runtime 원문과 reference의 한국어 literal을 대조한 정적 finding. 실행 미검증.

### guide-create-02 — guide 산출물 제한과 하네스 기록 의무의 범위를 구분할 수 있다 [정리 후보]

- 기준: 2, 4
- 적용 runtime: Claude, Codex
- 근거: 양 runtime [SKILL](../../../.claude/skills/guide-create/SKILL.md) / [Codex SKILL](../../../plugins/sdd-skills-codex/skills/guide-create/SKILL.md) 29행은 “생성 가능한 파일은 `_sdd/guides/<YYYY-MM-DD>_guide_<slug>.md`뿐”이라고 하며 91행은 “allowed output 외 repository surface가 수정되지 않았는지 확인”한다. [AGENTS.md](../../../AGENTS.md) 45행은 “각 작업 단위 종료 시 예외 없이 `_sdd/work_log/<yyyy-mm-dd>.md`에 항목을 append”하도록 한다. 소비 repo에 배포되는 [Claude 하네스](../../../.claude/skills/spec-create/references/agents-harness-template.md) / [Codex 하네스](../../../plugins/sdd-skills-codex/skills/spec-create/references/agents-harness-template.md) 49행에도 동일한 의무가 있다.
- 문제 상황: guide 작성 작업을 독립 커밋 단위로 마감하며 하네스의 work log를 함께 기록한다. guide 파일과 별도 작업 기록이라는 구분을 하지 않으면 Final Check의 전체 surface 제한을 위반한 것처럼 읽힌다.
- 예상 영향: 상위 하네스를 우선하고 작업 기록을 별도 의무로 해석하면 해결된다. 따라서 실제 불필요한 중단이나 로그 누락을 단정하지 않고, 현재 계약을 분명하게 하는 정리 후보로 분류한다.
- 최소 수정안: Hard Rules의 주어를 “이 스킬이 소유하는 기능 가이드 산출물”로 좁히고 Final Check는 “이 스킬이 만든 변경”에 적용한다. 상위 하네스가 요구하는 작업 기록은 하네스가 소유한다는 포인터를 둔다. work log 형식·주기를 SKILL에 복제하지 않는다.
- 유지할 계약: guide 외 임의 산출물 생성 금지, global spec/code/config/test read-only, 상위 하네스 작업 기록, 기존 사용자 변경 보존.
- 소유자: `guide-create` 쓰기 범위 문구. 연결 소유자는 하네스 배포자 `spec-create` / `spec-upgrade`; 하네스 기록 의무 자체를 약화할 필요는 없다.
- 검증 상태: SKILL·실제 AGENTS·spec-create 양 runtime 하네스 문구를 대조했다. `spec-upgrade` mirror 전문과 hook 동작은 미검토이며 이 finding은 hook 실패를 주장하지 않는다.

## 런타임 차이와 의존성

- Claude/Codex SKILL 및 output-format은 각각 파일 비교에서 동일했다. 별도 runtime adapter나 helper lifecycle이 없으며, runtime-local reference를 읽는 구조가 적절하다.
- 읽은 직접 reference: 양 runtime `guide-create/references/output-format.md` 전문.
- 경계 판단에 읽은 자료: `AGENTS.md`, `_sdd/spec/main.md`의 관련 Guardrails와 document producer 결정, `_sdd/env.md`, `_sdd/spec/components.md`의 guide-create 역할, `spec-create` 양 runtime 하네스의 작업 기록 절.
- 다른 스킬을 호출하는 실행 의존성은 없다. `spec-summary` 등의 전체 본문, `spec-upgrade` 하네스 mirror, hook 실행 환경은 미검토다. 이 문서는 그 영역의 결함을 판정하지 않는다.

## 권장 처리 순서와 검증

1. guide-create-01의 언어 번역 예외를 spec에서 결정한 뒤 output reference와 SKILL의 포인터에 반영한다. 표준 한국어 입력과 제목·label까지 영어로 요구하는 입력을 각각 실행해 5개 section·metadata 의미·evidence 표기가 유지되는지 확인한다.
2. guide-create-02는 다른 스킬의 쓰기 경계 finding과 통합해 필요할 때 함께 정리한다. 하네스가 있는 임시 repo에서 guide와 의무 work log만 바뀌고 code/config/test는 그대로인지 확인한다.
3. 변경 시 양 runtime parity와 `git diff --check`를 확인한다. 이번 리뷰에서는 대상 스킬을 실행하거나 제안을 적용하지 않았다.
