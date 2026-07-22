# Feature Draft (Lite): reviewer full 기계장치 트림 (F3)

> Lite 적격: 적격 — 대상이 reviewer agent 3종 쌍 + skill 3종 쌍으로 전수 열거되고 task 대응이 눈검산 가능, 단일 세션 규모. full 기계장치 어휘가 표면에 흩어진 census형 신호는 마지막 검증 task(Task 6)로 대응. (분할 계획 원본: `_sdd/drafts/2026-07-22_feature_draft_lite_full_lane_removal.md`의 F3)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
reviewer들에서 full 레인 잔재를 제거하고 **경량 반환을 유일 mode로** 만든다 (사용자 확정 3건): ① plan-review-agent의 full rubric(Tier 1/2·coverage index·V* 1:1·Touchpoints census·planning precedence·Orchestrator Review Mode) 전부 삭제 — Tier 2-lite rubric이 유일 기준으로 승격. ② reviewer 3종의 리포트 파일 mode + re-review mode 삭제. ③ pr-review는 오케스트레이션 스킬로서 agent들로부터 경량 반환을 받고 **통합 리포트 1파일만 스킬(메인 루프)이 직접 작성** — 3파일→1파일.

- **새 invariant**: reviewer agent는 판정만 반환하는 read-only leaf다(`Write` 권한 제거) — 파일 작성은 호출자 소관(작성자 불변식의 reviewer 적용).
- **새 invariant**: 리뷰는 단일 패스가 유일하다 — re-review·iteration 기계장치 없음, finding 반영은 호출자 fix 1회.

## Scope
- **In**: plan-review-agent·implementation-review-agent·simplicity-review-agent·pr-review-agent 쌍(계 8파일), plan-review·implementation-review·pr-review SKILL 쌍(계 6파일), agent frontmatter tools
- **Out**: spec full 서술 트림·잔재 폐기(F4), spec-review-agent·spec-sync-agent(레인 무관 유지), ralph
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: plan-review-agent 쌍 재작성 — lite draft 전용 단일 mode
Tier 구분·full rubric·파일 mode를 삭제하고, 현 Tier 2-lite의 내용(AC falsifiability·Target Files 실측·task boundary·scope + 6-smell + Lite 적격 검사·분할 권고)을 유일 rubric으로 승격한다.

**Contracts**:
- 리뷰 대상 = lite feature draft (유일 생산물이므로 자가 식별 불요). 대상 파일이 없으면 "리뷰 대상 없음 + `feature-draft-lite` 안내" 1줄 반환 (구 Tier 3 input-readiness report 폐지).
- 반환 = 경량 반환 유일: severity별 finding + Lite 적격 검사 결과 + smell 6행 1줄 판정. 리포트 파일·re-review 없음.
- frontmatter tools에서 `Write` 제거.

**Acceptance Criteria**:
- [ ] AC1: 쌍에서 "Tier 1|Tier 2|Tier 3|Orchestrator Review|coverage index|V\*|Touchpoints|planning precedence|task-ordering|Iteration|Current Status|re-review|리포트.*저장" grep 잔존 0 (Tier 2-lite 명칭 자체도 소멸 — 유일 mode라 이름 불요).
- [ ] AC2: tools 배열에 Write가 없다.
- [ ] AC3: codex TOML 3-way 적용, 신규 본문 parity (잔여 diff는 기존 적응 delta뿐).

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- 전면 재작성 (264줄 → 대폭 축소)
- [M] `.codex/agents/plan-review-agent.toml` -- 3-way

### Task 2: implementation-review-agent 쌍 — 경량 반환 유일화
파일 mode(리포트 경로 계약·Output Format 템플릿·Current Status·Iteration History)·re-review mode를 삭제한다. 검증 기준(Fresh Verification·증거 결속·severity·Tier graceful degradation의 입력 적응)은 유지하되, 입력 우선순위의 `*_implementation_plan_*` glob은 legacy fallback으로 강등한다(생산자 소멸 — simplicity L1 대칭). `implementation-plan` Integration 줄(:194)을 제거한다. `Bash`(테스트 실행)는 유지, `Write`는 제거.

**Acceptance Criteria**:
- [ ] AC1: 쌍에서 "re-review|Iteration History|Current Status|경량 반환 mode(분기 서술)|리포트.*저장|implementation-plan" grep 잔존 0 — 경량 반환이 유일이므로 "mode" 분기 어휘 자체가 사라진다.
- [ ] AC2: tools = Read·Glob·Grep·Bash (Write 없음).
- [ ] AC3: codex 3-way, boundary 예문(:8)의 삭제 이름 정리 포함.

**Target Files**:
- [M] `.claude/agents/implementation-review-agent.md` -- 재작성
- [M] `.codex/agents/implementation-review-agent.toml` -- 3-way

### Task 3: simplicity-review-agent 쌍 — 경량 반환 유일화
Task 2와 대칭: 파일 mode·re-review·Output Format 템플릿 삭제, 5개 차원·falsifiability gate·severity 유지, plan glob legacy 강등, `Write` 제거. 호출자가 pr-review일 때도 동일하게 경량 반환한다(호출자 무관 단일 계약).

**Acceptance Criteria**:
- [ ] AC1: 쌍에서 "re-review|Iteration History|Current Status|리포트.*저장" grep 잔존 0.
- [ ] AC2: tools = Read·Glob·Grep.
- [ ] AC3: codex 3-way parity.

**Target Files**:
- [M] `.claude/agents/simplicity-review-agent.md` -- 재작성
- [M] `.codex/agents/simplicity-review-agent.toml` -- 3-way

### Task 4: SKILL wrapper·소비자 표면 정합
wrapper들을 경량 반환 유일 계약에 맞춘다: plan-review SKILL의 리포트 경로 relay 계약 제거 + **skill.json 쌍의 "report" stale description 교체**(plan-review H1·M1), implementation-review SKILL의 경량/파일 분기·예외 조항 제거, 병렬 안전성 근거를 "read-only leaf(Write 없음)"로 갱신 — codex SKILL :50의 tools 사실 불일치도 이때 자연 해소. **"Tier 2-lite" 명칭의 외부 소비자 정합**: autopilot 쌍(:38 다이어그램·:84 체인 step 2·:93 canonical bullet)과 AUTOPILOT_GUIDE ko·en(:82)의 "Tier 2-lite 자가 식별" 서술을 "단일 패스 경량 반환"으로 교체 (명칭 소멸의 소비자 잔존 방지 — H1).

**Acceptance Criteria**:
- [ ] AC1: 두 SKILL 쌍에서 "리포트 경로|파일 mode|re-review|예외" 분기 서술 잔존 0, relay 대상 = 경량 반환 내용만.
- [ ] AC2: 병렬 안전성 근거가 실제 tools(Write 없음)와 일치한다.
- [ ] AC3: plan-review skill.json 쌍 description에 "report" 어휘가 없다.
- [ ] AC4: autopilot 쌍·AUTOPILOT_GUIDE 쌍에서 "Tier 2-lite" 잔존 0.

**Target Files**:
- [M] `.claude/skills/plan-review/SKILL.md` / [M] `.codex/skills/plan-review/SKILL.md`
- [M] `.claude/skills/plan-review/skill.json` / [M] `.codex/skills/plan-review/skill.json` -- description 교체 (M1)
- [M] `.claude/skills/implementation-review/SKILL.md` / [M] `.codex/skills/implementation-review/SKILL.md`
- [M] `.claude/skills/sdd-autopilot/SKILL.md` / [M] `.codex/skills/sdd-autopilot/SKILL.md` -- Tier 2-lite 명칭 3곳 (H1)
- [M] `docs/AUTOPILOT_GUIDE.md` / [M] `docs/en/AUTOPILOT_GUIDE.md` -- 동일 1곳씩 (H1)

### Task 5: pr-review 재설계 — agent 경량 반환 + 스킬 작성 통합 리포트 1파일
사용자 확정 설계: 두 reviewer(pr-review-agent·simplicity-review-agent)는 경량 반환으로 findings를 응답하고, pr-review 스킬(메인 루프)이 `_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md` 통합 리포트 하나만 직접 작성한다. 통합 리포트가 finding 전문을 게재한다(기존 "detail은 agent 리포트 참조" 구조 폐지 — 참조할 파일이 없어짐). **반환 payload 계약**: 기존 SKILL :95-97의 승격 재료 계약(finding별 위치·문제·수정 제안)을 agent 반환 계약으로 이전한다 — 반환이 통합 리포트의 유일 소스이므로 (plan-review M3). pr-review-agent에서 파일 작성 계약·`Write` 제거.

**Acceptance Criteria**:
- [ ] AC1: pr-review SKILL 쌍에서 `_pr_correctness_`·`_simplicity_review_` 리포트 경로 계약이 없고, 통합 리포트 1파일 계약과 "agent는 경량 반환" 서술이 있다.
- [ ] AC2: pr-review-agent 쌍에서 리포트 파일 작성 계약 잔존 0, tools에 Write 없음 (Bash는 필요시 유지 — 구현 시 실측).
- [ ] AC3: codex 3-way parity.

**Target Files**:
- [M] `.claude/skills/pr-review/SKILL.md` / [M] `.codex/skills/pr-review/SKILL.md` -- dispatch·리포트 계약 재작성
- [M] `.claude/agents/pr-review-agent.md` / [M] `.codex/agents/pr-review-agent.toml` -- 경량 반환 유일화
- [M] `.claude/skills/pr-review/examples/sample-review.md` / [M] `.codex/skills/pr-review/examples/sample-review.md` -- 리포트 경로 예시 정합 (구현 시 실측)

### Task 6: 잔존 검증 (read-only) — full 기계장치 어휘 census
Task 1~5 완료 후. python lookahead로 실행한다 (BSD grep --pcre2 함정 — F2 교훈).

**Acceptance Criteria**:
- [ ] AC1: 검사 대상 20파일 — agent 쌍 8(plan-review·implementation-review·simplicity-review·pr-review) + SKILL 쌍 6(plan-review·implementation-review·pr-review) + pr-review sample 쌍 2 + autopilot 쌍 2 + AUTOPILOT_GUIDE ko·en 2 — 에서 "Tier|Orchestrator Review|coverage index|V\*|1:1|Touchpoints|planning precedence|task[-_]ordering|re-review|Iteration|Current Status|implementation-plan|리포트 저장|report path" 잔존 0. 허용 예외: ① 기록물(`_sdd/`·`.sdd-workbench/`) ② `docs/SDD_SPEC_DEFINITION.md`(F4) ③ pr-review 통합 리포트 자체의 파일 계약(스킬 소유 — 정당).
- [ ] AC2: grep 명령·결과가 마감 증거 테이블에 남았다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- 세 결정(full rubric 전부 삭제 / 파일·re-review 삭제 / pr-review = agent 경량 + 스킬 통합 1파일)은 사용자 확정. 통합 리포트의 finding 전문 게재는 그 따름정리로 결정 — 확인 불요.
- 구 Tier 3(input-readiness) 폐지: "대상 없음 + 안내 1줄"로 대체 — 소비자였던 full 파이프라인이 없고, lite draft는 1분이면 만들 수 있어 별도 report가 과잉. 확인 불요로 판단.
