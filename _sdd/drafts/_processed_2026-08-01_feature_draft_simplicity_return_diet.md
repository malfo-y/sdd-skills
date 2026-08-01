# Feature Draft: simplicity-review-agent 반환 다이어트 (plan-review 울타리 이식)

> 규모 판정: 적격 — 변경 요소는 규칙 1문장 + AC 한정어 흡수 × 미러 2벌(2파일)로 task 1개에 1:1 대응, 눈검산 가능.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

plan-review 반환 다이어트(v4.6.28)의 울타리 규칙을 `simplicity-review-agent`에 적응 이식한다. simplicity의 반환 구조는 plan-review와 동형(Findings + 차원 판정 PASS 접기 + Assumptions)인데 "finding이 아닌 확인 결과 비열거" 울타리가 없어, 스캔했으나 문제 없음으로 확인한 지점·파일 목록이 반환에 열거될 통로가 열려 있다. 시간은 "적어야 할 양"이 결정한다는 동일 진단이 근거다(구현 게이트에서 simplicity 참조 묶음 279s가 벽시계를 결정한 관측 있음).

- 계약 추가(기존 계약의 출력 제약 강화, 새 invariant 아님): simplicity-review-agent의 반환은 Step 4의 3항목(Findings·차원 판정·Assumptions)이 전부이며, 확인했으나 finding이 아닌 스캔 결과는 열거하지 않는다. 차원 한정 여부와 무관하게 적용되고, 줄이는 것은 출력이지 Step 2 스캔 범위가 아니다.
- 전파 범위 결정: 세 reviewer 실측 대조 결과 simplicity만 이번 범위. `implementation-review-agent`·`pr-review-agent`는 Verification ledger(MET 행도 증거 결속)가 계약이라 ledger 예외 문장이 필요한 **별도 feature**로 남긴다.

## Scope
- **In**: `.claude/agents/simplicity-review-agent.md` + `.codex/agents/simplicity-review-agent.toml`의 Step 4(Classify + Return) 규칙 1문장 추가, 자체 검증 AC3에 준수 흡수(범위 한정어 포함).
- **Out**: implementation-review-agent·pr-review-agent(별도 feature — ledger 예외 필요), SKILL orchestrator 4벌(반환 relay만 하므로 무변경), spec 표면(`main.md`·`components.md` — spec-sync 소관), 차원 정의·severity·묶음 한정 계약 일체.
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: simplicity-review-agent 미러 2벌에 반환 울타리 규칙 추가

plan-review v4.6.28의 두 편집을 simplicity 문맥으로 적응 이식한다 — 반환 항목명·스캔 단계 참조·조건화 축을 simplicity 것(3항목·Step 2·차원 한정)으로 치환하고, plan-review 게이트 fix에서 배운 범위 한정어를 처음부터 포함한다.

**Contracts**: 반환 울타리 — 확인했으나 finding이 아닌 스캔 결과(문제 없음을 확인한 지점·파일 목록 등)는 열거하지 않으며, 반환은 Step 4의 3항목이 전부다. 이 규칙은 차원 한정 여부와 무관하고, 줄이는 것은 출력이지 Step 2 스캔 범위가 아니다. 자체 검증 AC3이 이 준수를 "Step 4 항목 밖에" 범위 한정어와 함께 점검한다(PASS 접기 줄·Assumptions 삭제 오독 차단).

**Acceptance Criteria**:
- [ ] AC1: 두 미러의 `### Step 4: Classify + Return` 섹션(반환 3항목 뒤)에 규칙 문장이 있고 4요소를 모두 담는다 — (a) 금지 대상("확인했으나 finding이 아닌 스캔 결과" + "열거하지 않는다"), (b) 항목 불축소("반환은 위 항목이 전부다"), (c) 무조건 적용("차원 한정 여부와 무관"), (d) 스캔 범위 불변("Step 2 스캔 범위"). — grep으로 각 요소 문자열 실재 판정.
- [ ] AC2: 두 미러의 자체 검증 AC3이 "Step 4 항목 밖에 finding이 아닌 확인 결과를 열거하지 않았다"를 포함하도록 확장됐고(범위 한정어 필수), 자체 검증 AC 항목 수는 3으로 불변이다.
- [ ] AC3: 기존 계약 앵커가 보존된다 — `## 호출자 차원 한정`, `## Review Dimensions`, `## Severity Rules`, `### Step 2: Per-dimension Scan`, `## Hard Rules`, `Source Pointer`, 그리고 Step 4의 기존 반환 3항목(`**Findings**`·`**차원 판정**`·`**Assumptions**`). `.codex` TOML은 파싱 유효.
- [ ] AC4: 변경 격리 — git diff가 두 미러의 Step 4 섹션·AC3 행 밖을 건드리지 않고, 두 미러·이 draft·오늘 work log 외 파일 변경이 없다.
- [ ] AC5: 두 미러의 Step 4 섹션 본문과 AC3 행이 문면 동일하다(diff 0).

**Target Files**:
- [M] `.claude/agents/simplicity-review-agent.md` -- Step 4 규칙 1문장 + AC3 흡수
- [M] `.codex/agents/simplicity-review-agent.toml` -- 동일 편집(행 정렬 미러)

# Open Questions

- **게이트 = 다이어트 첫 관측**: 이 draft의 plan-review 게이트가 플러그인 발효 후 첫 게이트라, plan-review 다이어트 효과의 첫 관측 표본이다. 실측 렌즈 시간과 반환 하단 확인 목록 소멸 여부를 함께 기록한다. 사용자 확인 불필요(관측 계획).
- **implementation-review·pr-review 전파**: ledger 예외 문장이 필요해 이번 범위에서 제외하기로 사용자가 결정했다. 추후 별도 feature. 사용자 확인 불필요(이미 결정됨).
