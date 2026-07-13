# Feature Draft: intra-draft 재진술 다이어트 (Part 2 정보 단일 홈 배치)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

feature-draft 산출물(draft) 한 파일 안에서 같은 정보가 Part 2의 여러 섹션(`Touchpoints` ↔ Task `Description` ↔ `Acceptance Criteria` ↔ `Validation Plan`의 `V*`)에 2~3회 중복 서술되는 것을 구조적으로 금지한다. 방법은 두 갈래다: (1) `feature-draft-agent`의 authoring 규칙에 **정보 단일 홈 배치**(각 정보 유형의 canonical 위치를 하나로 고정하고 다른 섹션은 참조로 갈음)와 **line number 금지 규칙**(AC/Description은 content anchor로만 지목, line number는 Touchpoints 전용)을 추가하고, (2) `plan-review-agent`의 기존 smell(`DRY Risk`·`Verification Weakness`)을 확장해 재진술과 stale line anchor를 finding으로 잡아 review-fix loop가 회귀를 막게 한다.

근거: 이 repo의 알려진 병목은 draft 작성(추론)이며 출력량 감소가 생성·review-fix loop 양쪽의 속도 레버라는 운영 합의. 실측(2026-07-09 draft, 아래 Part 2 Overview 참조)에서 draft의 30~40%가 제약 손실 없이 제거 가능한 중복으로 추정됐다. 제약 수위(AC falsifiability, Target Files, census 요구)는 낮추지 않는다 — 목표는 "각 정보는 한 곳에만"이다.

## Scope Delta

**In scope**
- `feature-draft-agent` 짝(.md/.toml): Part 2 정보 단일 홈 배치 규칙 + line number 금지 규칙 + Step 8 교정 항목 + 자체 AC self-check 항목 추가.
- `plan-review-agent` 짝(.md/.toml): `DRY Risk`에 intra-draft 재진술 점검(Description↔AC 미러링, census 다중 서술), `Verification Weakness`에 AC/Description line number 지목 점검 추가.
- claude ↔ codex 미러 짝 동시 반영.

**Out of scope**
- 신규 smell 카테고리 추가(6-smell 개수 불변 — Q1).
- 실행 파이프라인(`task-ordering-agent`·`implementation` SKILL의 전사/leaf dispatch prompt) 변경(Q2).
- 기존 draft 산출물의 소급 수정.

**Guardrail delta**
- 불가침 3종을 명시 보존한다: **Target Files 계약**(병렬 wave file-disjoint 가드레일이 소비), **falsifiable AC + `V*` 1:1 linkage**(test-author-agent가 AC에서 테스트를 뽑는 메커니즘), **census 요구 자체**(rename 잔존·§섹션 propagation·agent 등록 갭 실패 클래스 방어). 이번 변경은 census의 **서술 위치**만 Touchpoints 1곳으로 고정하고 요구 수위는 유지한다.

## Persistent Spec Implications

`_sdd/spec/main.md` §2 Guardrails에 남아야 하는 계약·불변식·검증 의도:

- **Part 2 정보 단일 홈 배치 불변식**: feature-draft Part 2에서 각 정보 유형은 canonical 위치 하나만 가진다 — `Touchpoints` = 코드 지점 + 변경 이유 + 탐색 증거(census, line number 유일 허용처), Task `Description` = 의도 + 비자명한 근거, `Acceptance Criteria` = 충족 정의 checklist(content anchor로 지목), `V*` = 판정 조건(grep 토큰·기대 hit·명령·rubric). 다른 섹션은 참조로 갈음하고 산문으로 재서술하지 않는다.
- **plan-review 감사 계약**: plan-review는 intra-draft 재진술(Description↔AC 미러링, census 다중 서술)과 AC/Description의 line number 지목(stale anchor)을 plan smell로 잡는다.
- **제약 수위 불변**: 위 다이어트는 AC falsifiability·Target Files·census 요구를 약화하지 않는다.
<!-- spec-update-todo-input-end -->

# Part 2: Implementation and Validation Plan

## Overview

이 변경은 SDD skill/agent 지시문 4파일(2 미러 짝)을 수정해 draft authoring 계약과 plan review rubric을 바꾼다. 핵심 용어(문서 전체 1회 정의):

- **intra-draft restatement**: 한 draft 안에서 같은 정보가 Part 2의 두 섹션 이상(Touchpoints·Description·AC·`V*`)에 산문으로 반복 서술되는 것.
- **정보 단일 홈 배치**: Part 1 `Persistent Spec Implications`의 배치 불변식 — 각 정보 유형의 canonical 위치 하나 + 나머지는 참조.
- **census**: rename/propagation류 변경에서 편집 대상 전수를 검색 변형(kebab/underscore/공백/글롭 등)까지 포함해 확정한 탐색 결과(토큰·hit 수·위치). 이 repo의 실증된 실패 클래스(rename 잔존·§섹션 propagation·agent 등록 갭) 방어 장치.
- **content anchor**: line number 대신 구현 시점에도 안정적인 지목 수단(heading·고유 문구·토큰).
- **stale anchor**: draft 작성 시점의 line number가 구현 시점 파일 변경으로 실제 위치와 어긋난 지목.

실측 근거(작성 세션 분석, `_sdd/drafts/2026-07-09_feature_draft_task_ordering_late_binding.md` 51K): T5의 orchestrator-contract census가 3곳에 반복됐고(Touchpoints 항목 + T5 Description의 (1)~(6) 열거 + V5 grep 조건의 배경 서술), T1 Description의 (a)~(e) 열거를 AC 체크박스가 거의 그대로 미러링했으며, AC가 "line 138"·"line 320" 같은 line number로 지목해 stale 위험을 안았다. 현행 `feature-draft-agent` Hard Rule 11의 재진술 금지는 용어 정의·Part 1↔Part 2 관계만 겨냥해 Part 2 내부 섹션 간 재진술은 어느 규칙도 잡지 않고, `plan-review-agent` smell 목록에도 없다 — 이 갭을 닫는다.

## Scope

**In scope**: Part 1 Scope Delta의 in-scope 전부(C1~C3으로 전개).
**Out of scope**: Part 1 Scope Delta의 out-of-scope 전부(Q1·Q2).

## Contract/Invariant Delta and Coverage

| ID | Type | Change | Covered By | Validated By |
|----|------|--------|------------|--------------|
| C1 | Add | `feature-draft-agent`가 Part 2 정보 단일 홈 배치(Description·census·`V*` 3배치)를 authoring 규칙으로 강제하고 Step 8 교정·자체 AC self-check로 뒷받침 — 충족 정의는 T1 AC1~AC5 | T1 | V1 |
| C2 | Add | line number 규칙 — AC/Description에서 line number 지목 금지(content anchor 사용), line number는 Touchpoints(탐색 증거 기록처) 전용 | T1 | V1 |
| C3 | Modify | `plan-review-agent` smell 확장 — `DRY Risk`가 intra-draft 재진술(Description↔AC 미러링·census 다중 서술)을, `Verification Weakness`가 AC/Description의 line number 지목(stale anchor)을 점검. smell 개수는 6으로 불변 | T2 | V2 |
| I1 | Preserve | 제약 수위 불변 — AC falsifiability·`V*` 1:1 linkage·Target Files 계약·census 요구를 서술하는 기존 규칙 문구가 약화 없이 잔존 | T1, T2 | V3 |
| I2 | Preserve | claude ↔ codex 미러 parity — 변경 컴포넌트마다 양 플랫폼 짝 동시 반영 | T1, T2 | V4 |

## Touchpoints

현재 코드 재확인 기준(4파일 + 읽기 전용 근거 2건, 2026-07-13 read로 확정):

- `.claude/agents/feature-draft-agent.md` — Hard Rule 11(line 43-46)의 셋째 bullet "같은 산출물 안에서 재진술 금지"가 용어 정의·Part 1↔Part 2·risks/open questions만 겨냥하고 Part 2 섹션 간은 미포함 → C1/C2 확장 지점. 반영 표면: Step 6 필수 규칙 + "AC와 Validation 작성 위계" 블록(line 150-170)·task 템플릿(line 193-210), Step 8 대표 교정 목록(line 263-269), Acceptance Criteria 목록(line 18-29).
- `.codex/agents/feature-draft-agent.toml` — Hard Rule 11이 Rule 1~4 구조(line 52-58)로, "Rule 4 (No Intra-Document Restatement)"(line 56)가 claude 셋째 bullet의 대응 지점. Step 6(line 195-251), Step 8(line 287-295), AC 목록(line 27-38). Self-Containment Check(line 345-353)는 외부 참조 grounding 검증 전용이라 비대상.
- `.claude/agents/plan-review-agent.md` — Review Rubric 표(line 110-119)의 `DRY Risk`(line 118)·`Verification Weakness`(line 119) Check 문구, Principle Mapping 표(line 100-108)의 `DRY` 행. §2/§5 출력 템플릿의 "재진술 금지" 주석은 리포트 자체 규칙이라 비대상.
- `.codex/agents/plan-review-agent.toml` — 동일 표(line 110-119)·Principle Mapping(line 100-108). Check 문구가 claude와 동일함을 확인.
- (읽기 전용 근거 — Target Files 아님) `.claude/agents/task-ordering-agent.md`: 전사 대상 목록(AC line 21: task 정의·Coverage·Validation Plan)에 Touchpoints가 없어 ordered plan에서 Touchpoints는 소실된다. `.claude/skills/implementation/SKILL.md`: leaf dispatch prompt(test-author line 145-163 = AC·`V*`·Contract Delta·Target Files / impl line 187-206 = Description·AC·Technical Notes·Target Files·고정 테스트)에 Touchpoints 미전달. 이 실측이 Q2 결정(falsifiable 판정 조건은 AC/`V*`에 유지)의 근거다.
- (읽기 전용 증거 sample — Target Files 아님) `_sdd/drafts/2026-07-09_feature_draft_task_ordering_late_binding.md`: Overview에 인용한 3중 census·AC 미러링·line number 실측의 출처.

## Task Details

### Task T1: feature-draft-agent에 정보 단일 홈 배치 + line number 규칙 추가
**Priority**: P0
**Type**: Refactor

**Description**: `.claude/agents/feature-draft-agent.md`와 `.codex/agents/feature-draft-agent.toml`의 authoring 규칙에 C1(정보 단일 홈 배치)과 C2(line number 규칙)를 추가한다. 규칙의 홈은 Hard Rule 11의 재진술 금지 항목(Touchpoints 참조: claude 셋째 bullet ↔ codex Rule 4 — 구조가 달라 각자의 형식에 맞게 같은 의미를 얹는다)이고, Step 6·Step 8·자체 AC 목록은 그 규칙의 적용/점검 표면이다. 규칙은 산문으로 적는다(이 repo 제작 규범: 지시문은 산문 규칙이 의사코드보다 잘 지켜짐). 방어적 negative 재천명은 피하되, 실재하는 유혹을 막는 negative("Description이 AC를 산문으로 재열거하지 않는다")는 유지 가치가 있어 명시한다.

**Non-Goals**: 기존 AC 작성 위계(목표→AC→평가방법)·Target Files 규격·Part 1 관련 규칙은 바꾸지 않는다. plan-review 쪽 감사 규칙은 T2 소관.

**Acceptance Criteria**:
- [ ] 두 파일의 Hard Rule 11 재진술 금지 항목이 Part 2 섹션 간(Touchpoints↔Description↔AC↔`V*`) 정보 단일 홈 배치를 명시한다 — ① Description은 의도+비자명한 근거만 담고 열거형 편집 목록(checklist성 항목)은 AC에만 두며 AC를 산문으로 미러링하지 않는다, ② census는 Touchpoints에 1회만 서술하고 Description은 "Touchpoints의 <대상> census 참조" 구절로 갈음한다, ③ `V*`는 판정 조건(토큰·기대 hit/0-hit·명령·rubric)만 적고 census 배경을 재서술하지 않는다 — 세 배치가 각각 문장으로 존재한다. (V1)
- [ ] 두 파일에 line number 규칙이 문장으로 존재한다: line number는 draft 작성 시점 탐색 증거일 뿐 구현 시점엔 stale하므로 Touchpoints에만 허용하고, AC/Description은 content anchor(heading·문구·토큰)로만 코드 지점을 지목한다. (V1)
- [ ] census 기반 AC의 압축형 지침이 존재한다: AC는 census 배경을 재서술하지 않고 "Touchpoints census가 확정한 N곳 전체 + 잔존 0" 형태로 범위를 참조하며 세부 판정은 대응 `V*`에 위임한다. (V1)
- [ ] Step 8 대표 교정 목록에 재진술 교정 항목이 추가된다(Description↔AC 미러링 해소, census 다중 서술의 Touchpoints 참조화, AC/Description line number의 content anchor 치환). (V1)
- [ ] 두 파일의 Acceptance Criteria 목록에 단일 홈 배치 self-check 항목이 추가된다(Step 8 단일 검증 패스가 이 목록을 점검 기준으로 쓰므로 여기 있어야 실효). (V1)
- [ ] 기존 제약 문구가 변경 없이 잔존한다: "falsifiable하며 평가방법(`V*`)에 1:1 대응"(AC 목록), "모든 task에는 `**Target Files**`"(Hard Rule 8) — 양 파일. (V3)
- [ ] claude `.md`와 codex `.toml`이 같은 의미를 담는다. (V4)

**Target Files**:
- [M] `.claude/agents/feature-draft-agent.md` -- 단일 홈 배치 + line number 규칙 추가
- [M] `.codex/agents/feature-draft-agent.toml` -- 동일 (codex 미러, Rule 4 구조에 맞춤)

**Technical Notes**: Covers C1, C2, I1(기존 제약 문구 보존), I2(미러). validated by V1, V3, V4. Description 다이어트로 의도까지 지우면 leaf 구현 품질이 떨어지므로(R1) 규칙 문구에 "Description은 의도+비자명 근거를 여전히 소유(빈 Description 금지)"를 함께 명시한다.

### Task T2: plan-review-agent smell 확장 — 재진술·stale anchor 점검
**Priority**: P0
**Type**: Refactor

**Description**: `.claude/agents/plan-review-agent.md`와 `.codex/agents/plan-review-agent.toml`의 Review Rubric에서 기존 smell 2개를 확장해 C3을 반영한다. 신규 smell을 추가하지 않고 기존 smell에 귀속시키는 이유는 Q1(카운트 리터럴 propagation 회피 + 개념 귀속의 자연스러움) 참조. 점검 문구는 falsifiable 3패턴(Description↔AC 미러링, 같은 census의 다중 서술, AC/Description의 line number 지목)으로 한정해 인상평 finding을 막는다(기존 Hard Rule 8 Evidence Required와 정합 — R3 완화).

**Non-Goals**: severity 표·findings 출력 형식·Step 절차는 바꾸지 않는다(확장된 Check 문구만으로 기존 흐름이 그대로 동작). draft authoring 규칙은 T1 소관.

**Acceptance Criteria**:
- [ ] 두 파일 Review Rubric의 `DRY Risk` Check 문구가 intra-draft 재진술 점검 질문을 포함한다: 리뷰 대상 plan/draft 문서 자체가 같은 정보를 여러 섹션에 재서술하는가 — Task Description이 AC를 산문으로 미러링하는가, 같은 census가 Touchpoints 외 섹션(Description·`V*`)에 다시 서술되는가. (V2)
- [ ] 두 파일 `Verification Weakness` Check 문구가 stale anchor 점검 질문을 포함한다: AC/Description이 content anchor 대신 line number로 코드 지점을 지목하는가(Touchpoints 밖 line number는 구현 시점 stale 위험). 기존 검사 문구(AC↔`V*` 1:1 대응, falsifiability, 평가방법 등급+증거형태, Validation Plan 전사)는 그대로 잔존한다. (V2, V3)
- [ ] Principle Mapping의 `DRY` 행이 plan 문서 자체의 재진술 점검을 포함하도록 갱신된다. (V2)
- [ ] smell 개수는 6으로 불변이다 — "6개 smell"·"6-smell"·"6 Plan Smells" 문자열이 변경 전과 동일하게 잔존하고 rubric 표의 행 수가 6이다. (V2)
- [ ] claude `.md`와 codex `.toml`이 같은 의미를 담는다. (V4)

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- DRY Risk·Verification Weakness Check 확장 + Principle Mapping DRY 행 갱신
- [M] `.codex/agents/plan-review-agent.toml` -- codex 미러

**Technical Notes**: Covers C3, I1(기존 검사 문구 보존), I2(미러). validated by V2, V3, V4. 재진술 finding의 severity는 기존 표의 Medium 정의("구현 품질을 떨어뜨릴 가능성… 즉시 차단까지는 불필요")에 자연 귀속되므로 severity 표는 손대지 않는다 — Medium은 review-fix loop exit(`critical=high=medium=0`)에 포함되므로 다이어트가 실제로 강제된다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, C2 | 1등급 (정량 측정형): 두 feature-draft-agent 파일 각각에 대해 grep — 단일 홈 배치 3배치 문장의 고유 토큰(예: "단일 홈"/"미러링하지 않"/"census"+"Touchpoints"/"판정 조건"), line number 규칙 토큰("content anchor" 및 "line number"+"Touchpoints"), census 기반 AC 압축형 지침 토큰(예: "잔존 0" 또는 "위임" 계열 신규 문구), Step 8 교정 항목·AC self-check 항목의 신규 문구가 각 파일 hit ≥1 | grep 명령 출력(파일별 hit 수). 토큰 부재 = 미충족. grep은 문구 존재만 판정 — 신규 규칙 문구의 의미 적정성은 review-fix loop re-review의 2등급 판정에 의존 |
| V2 | C3 | 1등급 (정량 측정형): 두 plan-review-agent 파일 각각에 대해 grep — `DRY Risk` 행에 재진술 점검 토큰(예: "미러링"·"재서술"), `Verification Weakness` 행에 stale anchor 토큰(예: "line number"·"content anchor")이 hit ≥1, Principle Mapping `DRY` 행에 재진술 점검 토큰(예: "재진술")이 hit ≥1; "6 Plan Smells"/"6개 smell"/"6-smell" 문자열이 변경 전후 동일(diff 없음), rubric 표 행 수 = 6 | grep/diff 출력. 카운트 문자열 변경 또는 행 수 ≠6 = 미충족 |
| V3 | I1 | 1등급 + 2등급 혼합: (a) grep — T1/T2 AC가 지정한 기존 제약 앵커 문구("falsifiable하며 평가방법(`V*`)에 1:1 대응", "모든 task에는 `**Target Files**`", `Verification Weakness`의 기존 검사 문구)가 4파일에서 변경 전과 동일하게 hit; (b) 2등급 rubric: 리뷰어가 변경 diff에서 제약 수위를 낮추는 문구 변경(요구 삭제·완화 표현)을 지목하지 못하면 충족 | (a) grep 출력, (b) 리뷰 판정 + 인용한 diff 지점. 위반 사례 1건 지목 = 미충족 |
| V4 | I2 | 2등급 (정성 rubric 판정형): 리뷰어가 각 미러 짝(.md ↔ .toml)의 변경 부분을 대조해 의미 불일치(한쪽에만 있는 규칙·상반된 서술)를 지목하지 못하면 충족. claude/codex 구조 차이(Hard Rule 11 bullet ↔ Rule 4)에 따른 표현 차이는 불일치가 아님 | 판정 + 인용한 대조 지점 |

# Risks/Mitigations and Open Questions

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| R1: Description 과박화 — 다이어트 규칙을 과잉 적용해 의도·근거까지 지우면 leaf agent(대화 맥락 없이 task 하나만 수신)가 의도를 잃음 | 구현 품질 저하 | T1 규칙 문구에 "Description은 의도+비자명 근거를 여전히 소유(빈 Description 금지)"를 명시 — 금지 대상은 AC 열거의 산문 미러링뿐 |
| R2: census 판정 조건을 AC로 옮기며 AC가 재비대 | 다이어트 효과 상실 | T1에 census 기반 AC 압축형("census N곳 전체 + 잔존 0 + `V*` 위임") 지침 포함 |
| R3: 재진술 finding이 Medium으로 gating되어(loop exit `critical=high=medium=0`) 문체 수준 지적으로 loop 반복 증가 | review-fix 처리 시간 증가 | T2에서 점검을 falsifiable 3패턴으로 한정 — 인상평 finding은 기존 Evidence Required 규칙으로 차단 |

## Open Questions

### Q1. plan-review 반영 방식 — 신규 7번째 smell vs 기존 smell 확장
- **Decision taken**: 기존 smell 확장 — 재진술(미러링·census 다중 서술)은 `DRY Risk`에, line number stale anchor는 `Verification Weakness`에 귀속.
- **Alternatives considered**: 신규 "Plan Restatement" smell 추가 (기각 — "6개 smell"·"6-smell"·"6 Plan Smells" 카운트 리터럴이 양 플랫폼의 AC 목록·rubric heading·Step 5·Tier 3 서술·Error Handling에 분산돼 있어 신규 smell은 카운트 propagation census를 추가로 요구한다. 개념적으로도 재진술은 문서 DRY 위반, line number는 검증 anchor 약점이라 기존 smell에 자연 귀속됨).
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q2. census를 Touchpoints 1곳으로 옮기면 leaf agent에 전달이 끊기는가
- **Decision taken**: falsifiable 판정 조건(대상 N곳·토큰·기대 hit/0-hit)은 AC와 `V*`에 남긴다. Touchpoints 실측(task-ordering-agent가 Task Details·Validation Plan은 전사하지만 Touchpoints는 전사하지 않고, implementation SKILL leaf prompt도 AC·`V*`·Description·Technical Notes만 전달)에 따라 leaf 실행 표면은 AC/`V*`로 유지되고, Touchpoints census는 탐색 증거(검색 변형·hit 수·line number) 전용이 된다 — census "요구"는 불가침, "배경 서술 위치"만 1곳.
- **Alternatives considered**: ① task-ordering-agent가 Touchpoints를 전사하고 implementation SKILL leaf prompt에 포함 (기각 — 4파일 밖 파이프라인 2짝 추가 수정, AC/`V*`로 충분한데 최소 변경 위반). ② leaf가 draft 파일을 직접 read (기각 — "leaf는 재탐색하지 않음" 계약 위반).
- **Confidence**: HIGH
- **User confirmation needed**: No
