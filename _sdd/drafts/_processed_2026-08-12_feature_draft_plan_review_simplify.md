# Feature Draft: plan-review 단순화 — 규모 판정 검사 제거 · Hard Rules 다이어트 · rubric 재정리

> 규모 판정: 적격 — 변경 요소 4개(규모 판정 제거·Hard Rules 축약·rubric 재정리·Step 3/4 축약)가 agent 짝 1쌍 + wrapper 2벌에만 걸리고 요소↔task 대응이 1:1로 눈검산된다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
`plan-review`가 계약을 늘려온 결과 리뷰어가 rubric 밖에서 수행하는 검사(규모 판정 검사, Step 4 Decision and Assumption)와 rubric과 중복되는 Hard Rules가 쌓였고, rubric 자체는 5 smell 중 4개가 simplicity 축이라 "사용자 요청↔task/AC 정합성" 같은 계획 리뷰의 본령이 rubric에 없었다. 이 변경은 검사 표면을 rubric 한 곳으로 모으고 rubric의 축을 재배분한다.

새 contract/invariant:
- **규모 판정 검사 폐지**: `plan-review`는 draft 상단 `> 규모 판정:` 줄을 더 이상 대조하지 않는다. 분할 판정·census 검증 task 규칙의 소유자는 `feature-draft` SKILL 단독이 되고, agent 반환에서 `규모 판정 검사 결과` 항목이 사라진다.
- **rubric 축 재배분(5 smell 유지)**: `Requirement Fit`(요청↔task/AC 정합성, 누락·과잉 양방향) / `Task Boundary Drift`(유지) / `Hidden Decision`(신설 — 구 Step 4와 Hard Rule 6 흡수) / `Over-engineering`(구 `DRY Risk` + `New File Justification` 통합) / `Verification Weakness`(유지).
- **Hard Rules 범위 축소**: Hard Rules는 rubric과 겹치지 않는 작성 룰만 보유한다(read-only·출력 언어·Blocker Policy·recommendation 크기·producer 계약 재구성 금지). 검사 술어는 rubric이 단독 소유한다.
- **자체 검증 AC 5→3**: 규모 판정 AC와 Step 4 AC가 사라지고, 렌즈별 AC 제외 규정도 함께 사라진다.

## Scope
- **In**: `plan-review-agent` 짝(claude md + codex toml)의 intro 목적 문장·AC·Hard Rules·렌즈 절·rubric·Step 3~6·Error Handling, `plan-review` wrapper 2벌의 규모 판정 문구와 목적 서술(description).
- **Out**: `feature-draft`의 분할 규칙과 draft 템플릿 `> 규모 판정:` 줄(그대로 유지 — 소유자가 producer로 단일화될 뿐), severity 표, 2-렌즈 dispatch 구조, smell 개수 리터럴(5 smell·나머지 4 smell 유지), spec 표면(`spec-sync` 소관).
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | 규모 판정 검사 제거 (claude 소스) | `.claude/agents/plan-review-agent.md` | `grep -rn "규모 판정" --include="*.md" --include="*.toml" .` → `_sdd/`·`_COMMENTS.md`·`.sdd-workbench/` 제외 시 이 파일 8줄 | Task 1 |
| P2 | 규모 판정 검사 제거 (codex 미러) | `.codex/agents/plan-review-agent.toml` | 위 동일 query → 이 파일 8줄 | Task 2 |
| P3 | 규모 판정 검사 제거 (wrapper 2벌) | `.claude/skills/plan-review/SKILL.md`, `.codex/skills/plan-review/SKILL.md` | 위 동일 query → 각 파일 1줄(병합 규칙 문장). 같은 query의 나머지 히트인 `feature-draft`/`spec-rewrite` 템플릿·`docs/**/SDD_SPEC_DEFINITION.md`의 `> 규모 판정:` draft 리터럴은 변경 대상 아님 | Task 3 |
| P4 | agent 본문 재구성(AC·Hard Rules·rubric·Step) 미러 전파 | `.codex/agents/plan-review-agent.toml` | `diff <(sed -n '/^## Acceptance Criteria/,/^## Final Check/p' .claude/agents/plan-review-agent.md) <(sed -n '/^## Acceptance Criteria/,/^## Final Check/p' .codex/agents/plan-review-agent.toml)` → 빈 출력 | Task 2 |

# Claim Manifest

| ID | Claim | Query | Expected |
|---|---|---|---|
| CM1 | 구 smell 이름(`Scope Creep`, `New File Justification`, `DRY Risk`)은 agent 짝 밖에서 참조되지 않아 개명이 짝 안에 갇힌다 | `grep -rn "Scope Creep\|New File Justification\|DRY Risk" --include="*.md" --include="*.toml" .` (`_sdd/`·`_COMMENTS.md`·`.sdd-workbench/`·`agents/plan-review-agent` 제외) | 0건 |
| CM2 | `규모 판정 검사` 문구는 agent 짝과 wrapper 2벌에만 있고, `> 규모 판정:` draft 리터럴은 별개 표면이다 | `grep -rn "규모 판정" --include="*.md" --include="*.toml" .` (동일 제외) | agent 짝·wrapper 2벌 + `feature-draft/SKILL.md`·`spec-rewrite/references/template-compact.md`·`docs/**/SDD_SPEC_DEFINITION.md`의 `> 규모 판정:` 줄 |
| CM3 | 개수 리터럴은 5 smell 유지라 변경 대상이 아니다 | `grep -rn "5 smell\|5-smell\|5 Plan Smells\|나머지 4 smell" --include="*.md" --include="*.toml" .` (`_sdd/`·`_COMMENTS.md`·`.sdd-workbench/` 제외) | agent 짝 + wrapper 2벌에만 존재, 값 변경 없음 |
| CM4 | 변경 전 rubric 행 이름과 Step 헤딩 전수는 git baseline에서 도출한다(하드코딩 열거 금지) | `git show HEAD:.claude/agents/plan-review-agent.md \| sed -n '/^## Review Rubric/,/^## Severity/p' \| grep "^| "` + 같은 파일 `grep -n "^### Step"` | 헤더 1행 + rubric 5행(Scope Creep·New File Justification·Task Boundary Drift·DRY Risk·Verification Weakness); `### Step 1`~`### Step 6` 6줄 |
| CM5 | 변경 전 비헤딩 `Step N` 상호참조는 7줄/8건이며 Step 번호 재배치의 갱신 대상 전수다 | `git show HEAD:.claude/agents/plan-review-agent.md \| grep -n "Step [0-9]" \| grep -v "^[0-9]*:### Step"` | 7줄 — L18(Step 4 점검), L20(Step 6 항목), L43(Step 3 계단 + (Step 3)), L44(Step 3 계단), L46(Step 4(AC3)), L124(Step 3 대조 범위), L132(Step 3 계단의 4단계) |

# Part 2: Tasks

### Task 1: `plan-review-agent.md` 본문 재구성

검사 표면을 rubric 한 곳으로 모으고 rubric 축을 재배분한다. 이 파일이 plan-review 계약의 단일 소스이므로 여기서 최종 문면을 확정하고 Task 2가 그대로 미러한다.

**Contracts**: Part 1의 "새 contract/invariant" 4줄이 이 task가 확정하는 계약의 단일 소스다. 여기서는 그 계약이 문면으로 닫히는 지점만 덧붙인다.
- Hard Rule ④는 현행 `Evidence-backed Minimum Code`의 두 술어를 모두 보존한다 — 가장 작은 plan change + "새 capability는 current requirement 또는 measured risk에 직접 추적될 때만 권고". 라벨만 recommendation 작성 룰로 정렬하고 길이 제약은 두지 않는다.
- 흡수 매핑: 구 `Scope Creep`의 추적 가능성 검사 → `Requirement Fit`, 구 `New File Justification`의 `[C]` 근거 검사와 구 `DRY Risk` 전 술어 → `Over-engineering`, 구 Step 4의 4개 점검 항목과 구 Hard Rule 6 → `Hidden Decision`. 검사 술어 무손실.
- 새 3행의 Principle Link 값은 이 짝 안에서 이미 쓰이는 어휘로 고정한다 — `Requirement Fit` = `Scope Discipline, YAGNI`, `Hidden Decision` = `Verifiability, Scope Discipline`, `Over-engineering` = `DRY, KISS, YAGNI`.
- 실측 렌즈 소유 = Step 3 + `Verification Weakness` + 사실 주장 repo 대조, 판단 렌즈 소유 = 나머지 4 smell. 렌즈별 AC 제외 규정은 사라진다.

**Acceptance Criteria**:
- [ ] AC1: `grep -c "규모 판정" .claude/agents/plan-review-agent.md` → `0`.
- [ ] AC2: `## Acceptance Criteria` 섹션에 `- [ ] AC1:`~`- [ ] AC3:`만 있고 `AC4`·`AC5` 행이 없다 (`grep -n "^- \[ \] AC" .claude/agents/plan-review-agent.md` → 3줄). 남은 AC3은 "파일 생성 없음"과 "Return 항목 밖에 finding이 아닌 확인 결과 열거 없음" 두 절을 모두 갖는다.
- [ ] AC3: `## Hard Rules` 섹션의 번호 항목이 5개이고, 그 안에 `New File Justification`·`Decision and Assumption Surfacing` 라벨이 없다. `Blocker Policy`·`Producer Contract Verification` 라벨과 "가장 작은 plan change"·"measured risk" 술어는 남아 있다.
- [ ] AC4: CM4로 도출한 baseline rubric 행 전수가 새 5행 중 하나에 귀속됐고, rubric 표의 행 이름이 `Requirement Fit`·`Task Boundary Drift`·`Hidden Decision`·`Over-engineering`·`Verification Weakness` 5개이며 baseline 행 이름 문자열이 파일에 0건이다. 새 3행의 Principle Link 셀 값이 Contracts가 고정한 값과 일치한다 — reviewer 판정 + baseline 열거 인용.
- [ ] AC5: 흡수 무손실 — CM4 baseline에서 도출한 구 Step 4 점검 항목 전수(`git show HEAD:` 파일의 `### Step 4` 섹션 불릿)가 `Hidden Decision` Check 셀 안에서 모두 식별되고, baseline `DRY Risk`·`New File Justification` Check 셀의 술어 전수가 `Over-engineering` Check 셀 안에서 모두 식별된다 — reviewer 판정 + baseline 인용.
- [ ] AC6: `### Step 4: Review Decisions and Assumptions` 헤딩이 없고, Process 헤딩이 `Step 1`~`Step 5`로 연속하며 `Step 5`가 Return이다 (`grep -n "^### Step" .claude/agents/plan-review-agent.md` → 5줄).
- [ ] AC7: Step 3 본문에 번호 계단 목록(`1.`~`4.` 단계 열거)이 없고 산문 룰로 압축됐으며, 보존 술어 5개(manifest 행 전수 순회 / `CM<n>` 미참조 주장의 `Verification Weakness` 귀속 / legacy fallback / 근거 부족 시 `UNKNOWN`+limitation 1줄 / producer 계약 read)가 각각 식별된다 — reviewer 판정 + 인용.
- [ ] AC8: Step 5(Return) 항목 목록에 `규모 판정 검사 결과` 행이 없고 Blocker Status·Findings·Smell 판정 3항목만 남으며, 그 아래 비열거 규칙 문장이 보존된다 (`grep -c "반환은 위 항목이 전부다" .claude/agents/plan-review-agent.md` → `1`).
- [ ] AC9: `Step N` 상호참조 정합 — CM5가 열거한 baseline 7줄이 전부 처리됐고, `grep -n "Step [0-9]" .claude/agents/plan-review-agent.md` 결과 전수가 실재하는 새 Step 번호·문면을 가리키며, 해체된 계단을 가리키는 `4단계` 리터럴이 0건이다.
- [ ] AC10: 개수 리터럴 보존 — `grep -c "5 smell 전부" .claude/agents/plan-review-agent.md` 등 CM3의 네 리터럴이 각각 `1`이다(Out 선언 표면의 무변경 확인).
- [ ] AC11: intro 목적 문장이 새 rubric 축과 정합한다 — `grep -c "KISS, YAGNI, DRY, 검증 약점" .claude/agents/plan-review-agent.md` → `0`이고, 목적 서술에 요청 정합성·숨은 결정 축이 드러난다 (reviewer 판정 + 인용).

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- 계약 단일 소스 본문 재구성

### Task 2: codex TOML 미러 반영

Task 1의 확정 문면을 codex 미러에 3-way로 반영한다 — codex 적응 델타(Codex Agent Boundary 절, `spawn_agent` description, codex Source Pointer)는 보존하고 본문만 갈아끼운다(CM3).

**Acceptance Criteria**:
- [ ] AC1: `grep -c "규모 판정" .codex/agents/plan-review-agent.toml` → `0`.
- [ ] AC2: codex 델타 3곳이 보존됐다 — `grep -c "Codex Agent Boundary" .codex/agents/plan-review-agent.toml` → `1`, `grep -c "spawn_agent" .codex/agents/plan-review-agent.toml` → `2` 이상, Source Pointer 줄에 `.codex/skills/plan-review/SKILL.md`가 있다.
- [ ] AC3: P4의 `Discovery evidence` query(양쪽 `## Acceptance Criteria`~`## Final Check` 구간 `diff`)가 빈 출력이다.
- [ ] AC4: TOML이 파싱된다 — `python3 -c "import tomllib,sys; tomllib.load(open('.codex/agents/plan-review-agent.toml','rb'))"` 종료코드 0.

**Target Files**:
- [M] `.codex/agents/plan-review-agent.toml` -- 미러 본문 반영

### Task 3: wrapper 2벌 규모 판정 문구 제거

wrapper의 병합 규칙에서 규모 판정 검사 결과 relay 문구를 걷어내고, trigger description의 목적 서술을 새 rubric 축과 맞춘다(P3). wrapper는 thin entrypoint이므로 이 둘 외에는 손대지 않는다.

**Acceptance Criteria**:
- [ ] AC1: `grep -c "규모 판정" .claude/skills/plan-review/SKILL.md .codex/skills/plan-review/SKILL.md` → 양쪽 `0`.
- [ ] AC2: 병합 규칙 문장에 Blocker Status 병합·findings 합산·smell 판정 합집합 3요소가 그대로 남아 있다(`grep -n "합집합"` 양쪽 1건 이상).
- [ ] AC3: `5-smell` 리터럴이 양쪽에 그대로 있다(CM3 — 개수 불변).
- [ ] AC4: frontmatter `description`의 원칙 나열이 새 rubric 축을 반영한다 — `KISS/YAGNI/DRY` 나열만으로 목적을 서술하지 않고 요청 정합성·검증 축이 함께 드러난다(reviewer 판정 + 인용). trigger 문구(`plan review`·`계획 리뷰` 등)는 변경하지 않는다.

**Target Files**:
- [M] `.claude/skills/plan-review/SKILL.md` -- 규모 판정 relay 문구 제거
- [M] `.codex/skills/plan-review/SKILL.md` -- 동일

### Task 4: 전수 census 검증 (read-only)

규모 판정 검사 제거와 smell 개명은 변형 표기가 흩어지는 sweep이므로 잔존을 전수 grep으로 닫는다. census 문자열 목록은 CM4의 baseline 열거에서 도출한다. **In 표면 4파일 밖의 모든 히트는 수정하지 않고 이관·잔존 항목으로 보고하며 census 통과로 간주한다** — 이 task의 수정 권한은 In 표면 4파일뿐이다.

**Acceptance Criteria**:
- [ ] AC1: `grep -rni "규모 판정 검사\|규모판정\|scale verdict check" --include="*.md" --include="*.toml" .` 결과에 In 표면 4파일 히트가 0건이다(그 밖의 히트는 이관·잔존 목록으로 보고).
- [ ] AC2: baseline smell 라벨 census — `grep -rn "| Scope Creep |\|| New File Justification |\|| DRY Risk |\|Decision and Assumption Surfacing" --include="*.md" --include="*.toml" .` 결과에 In 표면 4파일 히트가 0건이다(라벨 형태로 좁힌다 — `scope creep` 산문은 `skills/spec-create/references/template-full.md` 등 무관 표면에 실재한다).
- [ ] AC3: `> 규모 판정:` draft 리터럴은 살아 있다 — `grep -rn "> 규모 판정:" --include="*.md" .` 이 `feature-draft`/`spec-rewrite` 템플릿과 `docs/**/SDD_SPEC_DEFINITION.md`에서 여전히 매칭된다(CM2 — 제거 대상 아님).

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- 구 Step 4의 4개 점검 술어를 (a) 규모 판정처럼 완전 삭제할지 (b) `Hidden Decision` rubric 행으로 이관할지: **(b) 이관으로 결정, 확신도 높음**. 근거는 사용자 코멘트가 두 표면을 다르게 지시했다는 점이다 — 규모 판정에는 "그냥 하지 말자"(삭제), Hard Rule 6(Decision and Assumption Surfacing)에는 "루브릭으로 가야 할까?"(이관 제안)이고, Step 4는 그 Hard Rule의 실행 절차다. 사용자 확인 불필요.
- rubric 행 수를 5행으로 유지할지 6행으로 늘릴지(구 `New File Justification`을 독립 행으로 존치): **5행 유지로 결정, 확신도 중**. 근거는 개수 리터럴 4곳(`5 smell 전부`·`전체(5 smell)`·`5 Plan Smells`·`나머지 4 smell`)의 blast radius를 피하고 `[C]` 근거 검사가 과잉 설계 축과 같은 판단을 공유한다는 점이다. 술어 무손실은 Task 1 AC5가 검증한다. 사용자 확인 불필요.
- rubric 이름을 한글이 아닌 영문 라벨(`Requirement Fit`·`Hidden Decision`·`Over-engineering`)로 둘지: 기존 5 smell이 모두 영문 라벨이므로 일관성을 위해 영문 유지로 결정. 사용자 확인 불필요.
- 규모 판정 검사가 사라지면 "분할 없이 강행된 draft"를 잡는 리뷰어가 없어진다: 사용자 지시가 명시적("규모 판정 검사는 그냥 하지 말자")이므로 그대로 제거하고, 분할 판정은 `feature-draft` producer가 단독 소유하는 것으로 결정. 사용자 확인 불필요(지시 자체가 확인).
