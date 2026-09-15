# spec-rewrite 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/spec-rewrite/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/spec-rewrite/SKILL.md)
- 판정 요약: 수정 필요 2 / 정리 후보 1 / 실행 검증 필요 0

## 역할과 유지할 계약

기존 spec의 구조를 정리하는 transformer다. rewrite 전에 계획을 저장하고, rationale·citation·navigation hint를 보존하며, 없는 내용을 창작하지 않는다. global은 개념·경계·결정을, temporary는 변경의 task·AC·Target Files를 유지한다. 잘 구조화된 입력은 진단 후 종료하고, 실제 rewrite를 했다면 링크·보존 여부·계획 대비 deviation을 검증해 보고한다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | spec-rewrite-01: review-only 의도도 선택될 수 있는 trigger. spec-rewrite-02: global 분할 규칙의 타입 조건 누락. |
| 2. 충돌과 우선순위 | spec-rewrite-01: spec-review의 읽기 전용 경계와 충돌. spec-rewrite-02: temporary 보존 계약과 global-only 지시가 충돌. |
| 3. 확인·승인 경계 | 독립적인 수정 필요 없음. Hard Rules 4는 계획 저장 후 필요한 확인만 요구하며, 명시적인 무조건 재승인 의무는 없다. review 요청의 수정 권한 문제는 01에 통합했다. |
| 4. 중복과 소유권 | spec-rewrite-03: feature-draft와 temporary exact shape의 단일 소스가 중복 선언된다. 런타임 배포 mirror는 결함으로 세지 않았다. |
| 5. 완료·복구 조건 | 수정 필요 없음. plan/report 검증 항목, 깨진 링크 수정, missing core warning이 있다. Step 1의 명시적 no-rewrite exit는 해당 경로에서 Steps 2–4의 작성 의무를 면제하는 것으로 읽힌다. |
| 6. 절차의 필요성 | 독립적인 수정 필요 없음. 진단 후 단계별 reference를 읽고 불필요한 rewrite를 중단한다. 계획 선저장과 보존 검증은 문서 재배치의 목적에 연결된다. |

## Findings

### spec-rewrite-01 — 읽기 전용 품질 검토가 rewrite trigger에 포함된다 [수정 필요]

- 기준: 1, 2, 3.
- 적용 runtime: Claude, Codex.
- 근거: [Claude SKILL](../../../.claude/skills/spec-rewrite/SKILL.md) 및 [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-rewrite/SKILL.md) L3의 `"review spec quality"`; 같은 파일 L103–115의 `### Step 3: Rewrite the Spec`와 `구조를 재배치한다.`
- 이웃 근거: [Claude spec-review](../../../.claude/skills/spec-review/SKILL.md), [Codex spec-review](../../../plugins/sdd-skills-codex/skills/spec-review/SKILL.md) L3의 `review-only analysis of spec quality`, L20–21의 `리뷰와 리포트 생성만 수행한다.` 및 spec 생성/수정/삭제 금지.
- 문제 상황: 사용자가 “review spec quality”라고만 요청하고 실제 spec의 구조가 좋지 않은 경우다. description은 rewrite를 직접 적용하도록 선택될 수 있지만, 본문은 rewrite 필요 진단 뒤 수정 단계로 진행한다. 잘 구조화된 spec에만 적용되는 no-rewrite exit는 이 경우를 막지 않는다. 동일한 의도는 spec-review의 읽기 전용 진입점에도 해당한다.
- 예상 영향: 품질 검토를 요청한 사용자의 의도와 달리 spec을 고치는 실행 경로가 열리거나, 같은 요청의 스킬 선택에 따라 쓰기 권한 범위가 달라진다. 실제 수정 발생을 관측한 것은 아니다.
- 최소 수정안: rewrite description에서 독립 trigger인 `review spec quality`를 제거하고, “구조 재작성·분할·정리를 요청할 때 사용; 품질 검토만 요청하면 spec-review”로 경계를 명시한다. 이미 재작성까지 요청한 사용자에게 별도 확인을 추가하지 않는다.
- 유지할 계약: 명시적 rewrite 요청은 진단→계획 저장→rewrite→검증까지 진행한다. 품질 검토는 읽기 전용으로 남는다.
- 소유자: spec-rewrite description. cross-skill 연결은 spec-review의 review-only 진입점이며, spec-review 본문 변경은 필요하지 않다.
- 검증 상태: 양 runtime의 원문과 이웃 진입점 대조 완료. 스킬 선택·쓰기 동작은 미실행. 기존 역할 경계의 정렬이며 spec 결정 변경 불필요.

### spec-rewrite-02 — 파일 분할 규칙이 temporary 내용까지 global 결정으로 제한한다 [수정 필요]

- 기준: 1, 2.
- 적용 runtime: Claude, Codex.
- 근거: [Claude SKILL](../../../.claude/skills/spec-rewrite/SKILL.md), [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-rewrite/SKILL.md) L94의 `multi-file 분할이 필요할 때 축 선택:`과 L101의 `어떤 축이든 각 파일에 담는 건 global-level 결정만이다.`
- 반대 계약: 같은 SKILL L70–73은 global/temporary 타입을 함께 진단한다. [Claude checklist](../../../.claude/skills/spec-rewrite/references/rewrite-checklist.md), [Codex checklist](../../../plugins/sdd-skills-codex/skills/spec-rewrite/references/rewrite-checklist.md) L23은 `Are execution details kept in the temporary artifact rather than lifted into the global spec?`라고 요구한다. [spec 정의](../../../docs/SDD_SPEC_DEFINITION.md) L147–160 역시 temporary에 feature-level contract·AC·Target Files를 둔다.
- 문제 상황: global 결정과 feature task·AC가 한 파일에 섞여 있어 global main과 temporary artifact로 분리하는 rewrite다. Step 2의 문면대로라면 “각 파일”에 global 결정만 남겨야 하므로, 새 temporary 파일에 task·AC를 보존하는 순간 해당 지시를 위반한다.
- 예상 영향: temporary 내용을 삭제·누락하거나 global 결정으로 잘못 승격할 수 있다. 올바르게 보존하려면 실행자가 문면에 없는 global-only 적용 범위를 스스로 보충해야 한다.
- 최소 수정안: L94–101을 “global portion을 여러 global 문서로 분할할 때”로 한정하고, 마지막 문장을 “이 global 분할 파일에는 global-level 결정만 담는다”로 바꾼다. temporary portion은 기존 temporary shape와 보존 checklist를 그대로 따른다.
- 유지할 계약: global 본문은 thin truth로 유지하고, 변경 실행 상세는 temporary surface에 보존한다. missing content 창작과 planning scope 확장은 하지 않는다.
- 소유자: spec-rewrite Step 2 양 runtime. cross-skill 변경 없음.
- 검증 상태: 본문과 reference·정의 문서의 상충 조건 대조 완료. mixed spec 분할 동작은 미실행. spec 결정 변경 불필요.

### spec-rewrite-03 — temporary exact shape를 별도 단일 소스로 복제한다 [정리 후보]

- 기준: 4.
- 적용 runtime: Claude, Codex.
- 근거: [Claude spec-format](../../../.claude/skills/spec-rewrite/references/spec-format.md), [Codex spec-format](../../../plugins/sdd-skills-codex/skills/spec-rewrite/references/spec-format.md) L27의 `exact structure, optional block trigger, field order, rolling split rule의 단일 소스는`이라는 선언이 local template을 가리킨다. [Claude template](../../../.claude/skills/spec-rewrite/references/template-compact.md), [Codex template](../../../plugins/sdd-skills-codex/skills/spec-rewrite/references/template-compact.md) L19–56이 그 shape와 rolling split 규칙을 소유한다.
- 이웃 근거: [Claude feature-draft](../../../.claude/skills/feature-draft/SKILL.md), [Codex feature-draft](../../../plugins/sdd-skills-codex/skills/feature-draft/SKILL.md) L55–94는 `아래 fenced template이 산출물 구조의 단일 소스다.`라고 선언한다. [spec 정의](../../../docs/SDD_SPEC_DEFINITION.md) L153도 `feature-draft`의 Required Output을 canonical 소스로 지정한다.
- 문제 상황: feature-draft의 canonical heading·marker·조건부 필드가 향후 바뀌면 rewrite는 자기 local shape를 verbatim 적용하도록 지시받는다. 두 “단일 소스”를 함께 유지해야 한다. 현재 fenced temporary skeleton은 동일하므로 이미 shape가 어긋났다고 판단하지 않는다.
- 예상 영향: 후속 변경 시 동기화해야 하는 계약 지점이 늘고, 한쪽만 갱신하면 rewrite가 canonical draft를 과거 shape로 되돌릴 수 있다. 현재 행동 결함이나 성능 비용을 측정한 것은 아니다.
- 최소 수정안: temporary exact shape는 same-runtime feature-draft의 Required Output을 읽도록 pointer로 통합한다. local template에는 global shape만 유지하고, checklist는 temporary 원본 보존 및 canonical shape 준수 확인을 유지한다. feature-draft를 실제 호출하거나 planning gate를 중복 실행하라는 지시로 바꾸지 않는다.
- 유지할 계약: 현재 temporary heading·marker·field order·conditional block·rolling split 결과는 바꾸지 않는다. 런타임 간 배포 mirror와 런타임 내부 authoring ownership을 구분한다.
- 소유자: spec-rewrite references와 Step 3의 asset-load 문장. cross-skill canonical owner는 feature-draft이며 본문 변경은 필요하지 않다.
- 검증 상태: 현재 skeleton과 canonical 선언 대조 완료. 동일 결과를 유지하는 정리 제안이며 적용·실행 미검증. 기존 canonical 소유권 준수이므로 spec 결정 변경 불필요.

## 런타임 차이와 의존성

- 두 SKILL.md, spec-format, rewrite-checklist는 byte-identical하다. template-compact의 차이는 guide-create 안내의 Claude `/guide-create`와 Codex `$guide-create`뿐이며 정당한 invocation 표기 차이다.
- 전문 검토: 두 runtime의 spec-rewrite SKILL과 직접 reference 3종, AGENTS.md, env.md, 공통 리뷰 기준.
- 관련 계약 검토: global spec의 경계·template ownership·artifact 계약, docs/SDD_SPEC_DEFINITION.md §6·§8·§10, 두 runtime feature-draft의 Required Output·AC 규칙, 두 runtime spec-review의 description·Goal·Hard Rules.
- 미검토: Companion Assets가 가리키는 외부 GitHub docs 디렉터리의 원격 최신본, 이웃 스킬의 본 리뷰와 무관한 나머지 실행 절, 설치본과 실제 런타임 행동. canonical 판단에는 저장소의 기준 커밋 문서를 사용했다.
- 이번 검토는 대상 스킬의 실행이 아니며 코드·스킬·global spec은 수정하지 않았다.

## 권장 처리 순서와 검증

1. description의 review-only 경계를 먼저 정렬한다. 후속 실행 확인에서는 “review spec quality” 입력이 spec 원본을 수정하지 않는지, “rewrite spec” 입력이 승인된 재작성까지 진행하는지 구분한다.
2. Step 2의 global 분할 조건을 한정한다. 작은 mixed fixture에서 global 결정은 main에, 기존 task·AC·Target Files는 temporary에 남고 상호 링크가 유효한지 확인한다.
3. temporary shape 참조를 canonical owner로 통합한다. 현재 source와 rewritten draft의 heading·marker·field order·내용 보존을 대조하고 runtime 표기 차이만 남는지 확인한다.

이번 리뷰에서는 위 동작 검증을 실행하지 않았다. 보고서 파일의 링크 대상 존재 여부·파일 권한·diff 공백 검증만 수행했다.
