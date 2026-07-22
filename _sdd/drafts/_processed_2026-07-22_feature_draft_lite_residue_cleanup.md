# Feature Draft (Lite): 잔재 정리 + full 어휘 census (F4)

> Lite 적격: 적격 — 대상이 폐기물 2종 + 이월 advisory 6건 + read-only census로 전수 열거되고 1:1 눈검산 가능, 단일 세션 규모. census형 신호는 Task 4가 곧 census다. (분할 계획 원본: `_sdd/drafts/2026-07-22_feature_draft_lite_full_lane_removal.md`의 F4 — F5 개명은 후속 feature로 분리, 사용자 확정)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
full 레인 삭제의 잔재를 정리한다: 삭제된 표면을 검증하던 check 스크립트와 무의미해진 미구현 draft를 폐기하고, F1~F3에서 이월된 advisory finding을 일괄 sweep하고, repo 전체 full 어휘 census로 F1~F4 삭제의 완결을 검증한다. persistent invariant 신설 없음 — 기존 invariant의 잔재 소거만.

## Scope
- **In**: `_sdd/tests/` 폐기, test-free triage 확대 draft 폐기, 이월 advisory 6건(fdl description·마커 3회 서술, impl-review description, AGENTS §3 문장 5미러, Quick Review 섹션, codex pr-review sample drift), repo 전체 full 어휘 census
- **Out**: `-lite` 개명·개념 어휘 교체·`docs/SDD_SPEC_DEFINITION.md` 정합(전부 F5), lite 체인 기능 변경
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: 폐기 — check 스크립트와 무의미해진 draft
`_sdd/tests/` 20 스크립트는 삭제된 full 표면(feature-draft-agent·implementation SKILL·orchestrator-contract)을 grep하는 검증물이라 전부 file-not-found로 죽었고(F2 실측 0/20), test-free triage 확대 draft는 대상 표면(test-author-agent·implementation SKILL RED 게이트)이 삭제되어 무의미해진 미구현 계획이다. git 히스토리가 보존하므로 삭제한다.

**Acceptance Criteria**:
- [ ] AC1: `_sdd/tests/` 디렉토리가 부재한다 (`ls` 실패).
- [ ] AC2: `_sdd/drafts/2026-07-21_feature_draft_test_free_triage_expansion.md`가 부재한다.

**Target Files**:
- [D] `_sdd/tests/` -- 20 check 스크립트 (untracked)
- [D] `_sdd/drafts/2026-07-21_feature_draft_test_free_triage_expansion.md` -- 미구현·무의미화된 full 시대 draft

### Task 2: 이월 advisory sweep (문구 5건)
F1~F3 리뷰들이 Low로 이월한 잔재 표현을 일괄 정리한다.

**Acceptance Criteria**:
- [ ] AC1: feature-draft-lite 쌍(SKILL frontmatter + skill.json)에 "full coverage-index/validation ceremony" 문구가 없다 (lite 대비 대상이던 full이 소멸 — 자립 서술로 교체).
- [ ] AC2: feature-draft-lite SKILL 쌍의 Integration spec-sync 항목에서 마커 소비 재서술 문장만 제거됐다 — 잔여 2곳(분할 방법 절 = 규칙, Part 1 템플릿 주석 = 작성 안내)은 각자 고유 기능으로 존치 (plan-review M2 실측 반영).
- [ ] AC3: implementation-review SKILL 쌍 description이 "implementation plan"(space-variant) 대신 draft/plan 중립 표현이다 (F3 L2).
- [ ] AC4: AGENTS.md + 하네스 템플릿 4미러의 spec-sync 문장이 과잉압축 해소 형태("spec-sync는 단일 진입점으로, 분할 draft의 planned todo 고정(조건부)과 구현 후 동기화를 evidence 유무로 구분해 수행한다")로 5곳 동일하다 (슬라이스 2 L4).
- [ ] AC5: implementation-review-agent 쌍에 Quick Review 섹션이 없다 (도달 경로 소멸 — F3 simplicity L1 다이어트).
- [ ] AC6: spec-sync-agent·spec-review-agent 쌍(4파일)에서 full draft 구조 참조(Part 2 "coverage index"·"Covered By"·task "Touchpoints" 검사·routing 서술)가 lite 기준으로 재서술되고, full 구조 읽기는 "legacy 기록물 fallback"으로 한정 표기됐다 (plan-review H1a 편입).

**Target Files**:
- [M] `.claude/skills/feature-draft-lite/SKILL.md` / [M] `.claude/skills/feature-draft-lite/skill.json` / [M] `.codex/skills/feature-draft-lite/SKILL.md` / [M] `.codex/skills/feature-draft-lite/skill.json`
- [M] `.claude/skills/implementation-review/SKILL.md` / [M] `.codex/skills/implementation-review/SKILL.md`
- [M] `AGENTS.md` / [M] `.claude/skills/spec-create/references/agents-harness-template.md` / [M] `.codex/skills/spec-create/references/agents-harness-template.md` / [M] `.claude/skills/spec-upgrade/references/agents-harness-template.md` / [M] `.codex/skills/spec-upgrade/references/agents-harness-template.md`
- [M] `.claude/agents/implementation-review-agent.md` / [M] `.codex/agents/implementation-review-agent.toml`
- [M] `.claude/agents/spec-sync-agent.md` / [M] `.codex/agents/spec-sync-agent.toml` -- Input Sources·routing의 full 구조 참조 lite화 (H1a)
- [M] `.claude/agents/spec-review-agent.md` / [M] `.codex/agents/spec-review-agent.toml` -- full 구조 검사 항목 lite화 (H1a)

### Task 3: codex pr-review sample을 현행 계약으로 재작성
codex sample이 구세대 단일 흐름(메인 컨텍스트 직접 검증)으로 서술돼 2-reviewer dispatch·verdict 합성 내레이션이 없는 기존 미러 drift (F3 correctness L3). claude sample을 기준으로 codex 적응(spawn_agent 어휘)해 재작성한다.

**Acceptance Criteria**:
- [ ] AC1: codex sample에 2-reviewer spawn(pr-review-agent·simplicity-review-agent 경량 반환)과 verdict 합성·통합 리포트 1파일 흐름이 서술된다.
- [ ] AC2: claude sample과의 diff가 codex 적응(spawn 어휘·경로)뿐이다.

**Target Files**:
- [M] `.codex/skills/pr-review/examples/sample-review.md` -- 전면 재작성

### Task 4: 잔존 검증 (read-only) — repo 전체 full 어휘 최종 census
F1~F4 삭제의 완결 검증. python lookahead로 실행한다.

**Acceptance Criteria** (plan-review M1의 2계층 분리 채택):
- [ ] AC1 (엄격 계층): live 표면(`.claude/`·`.codex/`·`.claude-plugin/`·`docs/`·`README.md`·`AGENTS.md`)에서 **full 레인 고유 식별자** 잔존 0 — 패턴: "feature-draft-agent|task[-_]ordering|test[-_]author|implementation-agent|Phase 1\.5|full 레인|Full 레인|Orchestrator Review|Iteration History|re-review|오케스트레이터". 허용 예외: ① 기록물(`_sdd/drafts/`·`_sdd/work_log/`·`_sdd/discussion/`·`_sdd/implementation/`·`.sdd-workbench/`; `_sdd/spec/`은 기록물이 아니라 live global spec이며 개념 어휘 정리가 F5 소관이라 제외 — plan-review L1) ② AUTOPILOT_GUIDE ko·en의 tag 복구 FAQ ③ `docs/SDD_SPEC_DEFINITION.md` ko·en(F5 소관).
- [ ] AC2 (판정 계층): **동음이의 다발 어휘** "orchestrator|checkpoint|Phase 2|Touchpoints|coverage index"는 히트 파일 목록 + 판정 요약을 증거화한다 — 판정 기준: full 레인 산출물·절차를 지칭하면 잔존(fix 또는 이월), 일반 의미(호출자·ralph 단계·문서 섹션명 등)면 통과.
- [ ] AC3: census가 새 잔존을 발견하면 — 문구 수준은 이 feature의 fix로 즉시 반영하고 대상 파일 밖 수정으로 기록, 규모가 있으면 후속 lite feature로 이월해 최종 보고에 남긴다 (read-only는 census 실행 자체에만 적용).
- [ ] AC4: grep 명령·결과가 마감 증거 테이블에 남았다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- Quick Review 삭제(AC5): F3 simplicity가 "실사용 신호 없으면 다이어트 후보"로 이월한 것을 삭제로 확정 — 빠른 확인은 메인 루프가 직접 답하는 게 lite 체인 구조와 정합. 확인 불요로 판단.
- test-free triage draft 폐기: 보존(기록) 대신 삭제 — git 히스토리 + work log가 기록을 보유. 확인 불요로 판단.
