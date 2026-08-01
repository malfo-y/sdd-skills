# Feature Draft: plan-review 반환 다이어트 — finding이 아닌 확인 결과 비열거

> 규모 판정: 적격 — 변경 요소 1개(반환 규칙 1문장 + 그 자체 검증)가 미러 2벌에만 걸린다. census형 sweep 신호는 없다(변형 표기가 흩어진 대상이 아니라 신규 문장 1개이며, **확인 결과 열거를 요구하는 표면이 0건**임을 실측 확인 — `plan-review` SKILL 미러 2벌은 병합 규칙에서 반환 **항목명**만 참조하고 relay 계약은 불변이라 무변경이다) — 따라서 별도 read-only census task를 두지 않고 파급 0 확인을 Task 1 AC에 넣는다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

`plan-review` 게이트의 벽시계는 리포트 작성량이 결정한다(시간의 54~68%). 오늘 실측에서 그 작성량의 상당 부분이 **판정에 기여하지 않는 확인 결과의 열거**임이 드러났다 — 실재가 확인된 Target Files·content anchor 목록, 대조했으나 반증되지 않은(지지된) 사실 전제 목록이 반환 하단에 통째로 실린다. 이 습성은 특정 렌즈나 dispatch 형태에 매인 것이 아니라 **실측 계열 dispatch 전반**에서 관측됐다.

이 변경은 그 열거를 반환 계약 차원에서 금지한다. 판정 결과는 이미 `Findings`와 `Smell 판정`(PASS 접기 포함)이 전부 담으므로, 별도 확인 목록은 중복이다.

- **반환 계약 갱신 (`Step 6: Return`)**: 확인했으나 finding이 아닌 대조 결과는 반환에 열거하지 않는다 — 반환은 명시된 항목이 전부다. 검출력은 그대로 두고 출력량만 줄이는 무조건 규칙이며, 정밀 서술은 Task 1 Contracts가 소유한다.
- **자체 검증 갱신**: 이 규칙 준수를 기존 AC5(산출물 형태)에 흡수한다 — 새 AC를 만들지 않는다.

**되돌린 대안 (기록)**: 같은 목표를 실측 렌즈의 묶음 분할(검증 ∥ 전제, 3-dispatch)로 치려 했으나 커밋 전 전량 되돌렸다 — 벽시계 353s로 재고 밴드, shard 합 738s로 총량 보존이 처음 붕괴, 검출 품질 개선 근거 없음, 계약 표면만 증가(`_sdd/work_log/2026-08-01.md` `## 1`~`## 3`). 나눠서 양을 분배하는 것보다 **덜 쓰게 하는 편**이 계약 표면을 늘리지 않고 같은 목표를 친다는 것이 이번 채택의 근거다.

## Scope

- **In**: `plan-review-agent` 미러 2벌의 `Step 6: Return` 규칙 1문장 + AC5 흡수.
- **Out**: 렌즈 구조(실측 ∥ 판단 2-렌즈)·`호출자 렌즈 한정` 절·6-smell rubric·severity·Step 1~5·Hard Rules 무변경. `plan-review` SKILL 미러 2벌 무변경. 다른 reviewer agent(`implementation-review-agent`·`simplicity-review-agent`·`pr-review-agent`)에 같은 규칙을 전파하는 것은 이번 범위 밖(별건 — 효과 관측 후 판단). spec 표면 갱신은 `spec-sync` 소관.
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: plan-review-agent 미러 2벌에 반환 다이어트 규칙 추가

`Step 6: Return`에 비열거 규칙 1문장을 넣고, 그 준수를 기존 AC5에 흡수한다. 렌즈·rubric·Step 1~5는 건드리지 않는다.

**Contracts**:
- 반환에는 `Step 6`에 명시된 항목만 싣는다 — 명시 항목 밖에, 확인했으나 finding이 아닌 대조 결과(실재가 확인된 Target Files·content anchor, 반증되지 않은 사실 전제)를 열거하지 않는다. 기존 4개 항목은 그대로 남는다.
- 이 규칙은 무조건이다 — 렌즈 한정 여부와 무관하게 모든 dispatch에 적용된다.
- 대조(Step 3 계단) 자체의 범위는 바뀌지 않는다. 줄이는 것은 출력이지 검증이 아니다.

**Acceptance Criteria**:
- [ ] AC1: 두 미러의 `Step 6: Return` 절에 비열거 규칙이 문장으로 있고, 그 문장이 네 요소를 함께 명시한다 — (a) 금지 대상이 "확인했으나 finding이 아닌 대조 결과"임, (b) 대조 범위는 불변임((b)가 없으면 "덜 읽어라"로 오독된다), (c) **렌즈 한정 여부와 무관하게 적용**됨(같은 파일 `호출자 렌즈 한정` 절이 일부 자체 검증 항목을 렌즈별로 조건화하고 있어, 무조건성이 없으면 실측 렌즈 dispatch가 이 규칙도 조건부로 오독할 수 있다), (d) 기존 4개 반환 항목을 축소하지 않음.
- [ ] AC2: 두 미러의 자체 검증 `AC5`가 이 규칙 준수를 포함한다. 새 AC 항목(AC6 이상)은 추가되지 않았다 — 자체 검증 목록의 항목 수가 변경 전과 같다.
- [ ] AC3: 계약 앵커가 보존된다 — `^## 호출자 렌즈 한정`, `^## Review Rubric: 6 Plan Smells`, `^## Severity`, `^## 규모 판정 검사`, `^### Step 3: Read Supporting Context`, `^## Hard Rules`, `Source Pointer`가 두 미러에 그대로 있고 `Step 6` 본문의 기존 4개 반환 항목(`Blocker Status`·`Findings`·`규모 판정 검사 결과`·`Smell 판정`)이 모두 남아 있으며, `.toml`이 파싱된다.
- [ ] AC4: 파급 0 — 변경 파일이 이 2개 미러 + 프로세스 산출물(`_sdd/drafts/2026-08-01_feature_draft_plan_review_return_diet.md`, `_sdd/work_log/2026-08-01.md`)로 격리되고, 두 미러의 diff가 `Step 6` 절과 AC5 줄 밖을 건드리지 않는다.
- [ ] AC5: 미러 문면 동일 — 두 미러의 `Step 6: Return` 절 본문과 자체 검증 `AC5` 줄이 바이트 동일하다. 이 전제는 실측으로 확인됐다(게이트 실측 렌즈: `Step 6: Return`이 양쪽 106행, 본문 108~113행과 자체 검증 `AC5` 20행이 문면 동일, 자체 검증 항목 수 5개). 구현 착수 시 대조에서 어긋나면 판정 기준을 **의미 동일 + codex 적응 delta 보존**으로 낮추고 그 사실을 마감 요약에 남긴다.

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- `Step 6: Return` 절에 규칙 추가, 자체 검증 `AC5` 흡수
- [M] `.codex/agents/plan-review-agent.toml` -- 같은 두 지점의 codex 미러 반영

# Open Questions

- **이 게이트는 대조군이다 (사용자 확인 불요)**: 이 draft의 `plan-review` 게이트는 플러그인 발효 전이라 다이어트가 **미적용** 상태로 돌아간다 → 2-렌즈 대조 표본 4가 된다(실측 ∥ 판단 시간을 마감 요약에 기록). 다이어트 효과의 첫 관측은 다음 feature의 게이트이며, 판정은 `실측 렌즈 시간`과 `반환에 확인 목록이 실렸는지` 두 가지를 함께 본다.
- **다른 reviewer로의 전파는 별건 (결정: 이번 범위 밖)**: 같은 열거 습성이 `implementation-review-agent`·`simplicity-review-agent` 반환에도 있는지는 이번에 확인하지 않았다. 효과가 확인되면 그때 전파를 별도 feature로 판단한다.
