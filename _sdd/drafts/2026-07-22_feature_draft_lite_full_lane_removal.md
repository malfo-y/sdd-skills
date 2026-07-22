# Feature Draft (Lite): full 레인 실체 삭제

> Lite 적격: 분할 필요 — 분할 계획 포함. 삭제 범위(autopilot full 파트 + agent 4종·스킬 3종 쌍 + reviewer 트림 + 잔재·spec 정리)가 단일 세션을 넘고, full 어휘가 다층 표면에 흩어진 census형 — feature 4개로 분할, 각 feature에 read-only 검증 task 포함.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
full 레인(orchestrator 기반 파이프라인)을 repo에서 삭제하고 lite 체인을 유일 실행 경로로 만든다. 근거: lite 품질이 full 대비 동등한데 훨씬 빠름 / full급 복잡도는 분할로 해소하는 것이 더 안전 / 분기 제거로 하네스 단순화·전파 표면 축소. 복구 보험은 삭제 직전 git tag `full-lane-final`.

분할 feature 목록 (순차 실행, 각 feature는 자기 차례에 lite draft를 새로 만든다):

1. **F1 — sdd-autopilot full 파트 제거** (이 draft의 Part 2): SKILL을 lite 체인 전용으로 재작성(v3.0.0), 부속(references·examples·scripts) 삭제, AUTOPILOT_GUIDE 재작성, tag `full-lane-final` 선행. Scope: `.claude/.codex` autopilot 디렉토리 + docs.
2. **F2 — full 전용 agent·스킬 삭제 + 등록 표면 정리**: feature-draft-agent·task-ordering-agent·test-author-agent·implementation-agent 쌍 8파일, 스킬 feature-draft·implementation·implementation-plan 쌍 6디렉토리, marketplace.json skills/agents 배열, `.codex/agents/README.md`, 루트 README 표. Scope: 삭제 + 등록 정리 (reviewer·spec 계열·pr-review·ralph는 유지).
3. **F3 — reviewer full 기계장치 트림**: plan-review-agent의 full Tier 검사(coverage index·V* 1:1·Touchpoints)·Orchestrator Review Mode, correctness·simplicity reviewer의 파일 mode/re-review mode 소비자 재검토, pr-review-agent의 full 의존 확인. Scope: 판단 항목이 많아 자기 draft에서 유지/삭제를 결정한다.
4. **F4 — 잔재 정리 + 최종 census**: 미구현 test-free triage 확대 draft·`_sdd/tests/` RED baseline 폐기, advisory 잔존 sweep(feature-draft-lite description "full ceremony" 표현 등), spec의 full 서술 트림(main.md §2 orchestrator guardrails·components·usage-guide), repo 전체 full 어휘 최종 census.

## Scope
- **In**: 위 4개 feature의 합집합 — full 레인 실행 경로·산출 계약·등록·문서·spec 서술 전부
- **Out**: lite 체인 자체의 기능 변경, spec 파이프라인(spec-create/sync/review)·pr-review·ralph·discussion 등 레인 무관 스킬, `-lite` 접미사 개명(삭제 완료 후 별도 판단)
<!-- spec-update-todo-input-end -->

# Part 2: Tasks (F1 — sdd-autopilot full 파트 제거)

### Task 1: tag `full-lane-final` 생성
삭제 직전 보험 — full 레인 전체가 담긴 마지막 커밋을 태그로 고정한다 (비용 0의 복구 경로).

**Acceptance Criteria**:
- [ ] AC1: `git tag -l full-lane-final` 이 현 브랜치의 slice-1 완료 커밋을 가리킨다 (`git rev-parse full-lane-final` = 삭제 커밋 이전).

**Target Files**:
- 없음 (git tag)

### Task 2: autopilot SKILL을 lite 체인 전용으로 재작성 (v3.0.0)
Lane 판정·full 레인을 제거하고 Step 0(축소)→Step 2→Step L만 남긴다. full 명시 요청에 대한 방어 문구는 두지 않는다(부재가 곧 답).

**Contracts**:
- 유지: Step L 체인(draft→plan gate+fix→구현→impl gate+fix→spec-sync→최종 보고), 분할 규칙, AC-L1~L4, Hard Rules 중 두 레인 공통이던 것(spec 직접 수정 금지·원문 전달·Execute→Verify·lifecycle·언어·path·spec-less·prefix).
- 삭제: Step 1(레퍼런스 로딩)·Step 3~8, Hard Rules full 전용(무중단·orchestrator 저장·Review-Fix 사이클·checkpoint gate·pre-flight approval·로그 상태·contract 우선), AC1~8, Workflow 다이어그램 full 분기, Lane 판정, Reference Files 섹션.
- Step 0 축소: pipeline log 스캔 분기 삭제(lite는 log를 만들지 않음), 기존 `_sdd/drafts/` 산출물 재활용 스캔만 유지. legacy full 로그가 발견되면 기록물로 무시한다.
- skill.json description을 lite 체인 서술로 갱신, 버전 3.0.0 (frontmatter·skill.json 동기).

**Acceptance Criteria**:
- [ ] AC1: SKILL.md 쌍에서 "orchestrator|Full 레인|full 레인|Phase 1.5|Phase 2|checkpoint" grep 잔존 0 (codex는 Codex Runtime Adapter의 reviewer dispatch 서술 제외 — implementation-review 스킬 소유 어휘).
- [ ] AC2: Step 구조가 0(축소)→2→L이고, references/examples/scripts 참조가 본문에 없다.
- [ ] AC3: frontmatter·skill.json 버전 3.0.0 일치, description에 orchestrator 서술 없음.
- [ ] AC4: codex 미러 동일 지점 3-way 적용 (잔여 diff는 기존 적응 delta뿐).

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md` -- 재작성
- [M] `.claude/skills/sdd-autopilot/skill.json` -- description·버전
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- 3-way 재작성
- [M] `.codex/skills/sdd-autopilot/skill.json` -- 동일

### Task 3: autopilot 부속 파일 삭제
full 레인 전용 자산 — 소비자가 T2에서 사라진다.

**Acceptance Criteria**:
- [ ] AC1: 아래 [D] 경로가 모두 부재하고(`ls` 실패), `__pycache__` 등 파생물도 남지 않는다.
- [ ] AC2: `orchestrator-contract.md|sdd-reasoning-reference.md|sample-orchestrator.md|validate_orchestrator.py` 참조 grep 잔존이 기록물(`_sdd/`)과 **후행 feature 표면**(F2 예정: feature-draft·implementation·implementation-plan 스킬 쌍 / F3 예정: plan-review-agent 쌍)뿐이다 — spec-summary example 쌍은 이 task에서 함께 수정하므로 잔존 0. (순차 롤링에서 후행 feature 표면의 참조는 그 feature의 몫이다.)

**Target Files**:
- [D] `.claude/skills/sdd-autopilot/references/` -- orchestrator-contract.md, sdd-reasoning-reference.md
- [D] `.claude/skills/sdd-autopilot/examples/` -- sample-orchestrator.md
- [D] `.claude/skills/sdd-autopilot/scripts/` -- validate_orchestrator.py (+__pycache__)
- [D] `.codex/skills/sdd-autopilot/references/` -- 동일
- [D] `.codex/skills/sdd-autopilot/examples/` -- 동일
- [D] `.codex/skills/sdd-autopilot/scripts/` -- 동일
- [M] `.claude/skills/spec-summary/examples/summary-output.md` -- L33의 sdd-reasoning-reference 참조 1줄 제거 (dangling 방지 — plan-review M1)
- [M] `.codex/skills/spec-summary/examples/summary-output.md` -- 동일

### Task 4: AUTOPILOT_GUIDE를 lite 체인 기준으로 재작성
구형 full 흐름(2-Phase·오케스트레이터·implementation-plan expanded path·규모표)을 서술하는 사용자 가이드를 lite 체인 문서로 교체한다 — 기존 drift(폐기된 implementation-plan 서술)도 이번에 함께 해소된다.

**Acceptance Criteria**:
- [ ] AC1: 가이드에 lite 체인(draft→plan gate+fix 1회→구현→impl gate+fix 1회→spec-sync→최종 보고), 분할(롤링·spec todo), 무승인 원칙이 서술된다.
- [ ] AC2: "오케스트레이터|Phase 1.5|implementation-plan|규모별 파이프라인" 서술이 없다 (tag `full-lane-final` 언급 1회는 복구 안내로 허용).

**Target Files**:
- [M] `docs/AUTOPILOT_GUIDE.md` -- 전면 재작성

### Task 5: 잔존 검증 (read-only) — F1 표면 full 어휘 census
T2~T4 완료 후 실행. 변형 표기까지 전수 grep한다.

**Acceptance Criteria**:
- [ ] AC1: autopilot 디렉토리 쌍 + AUTOPILOT_GUIDE에서 "orchestrator|오케스트레이터|full 레인|Full 레인|Phase 1.5|Phase 2|checkpoint|task_ordering|task-ordering" 잔존 0 (허용 예외: GUIDE의 tag 복구 안내 1회, codex Adapter의 reviewer dispatch 어휘).
- [ ] AC2: grep 명령·결과가 마감 증거 테이블에 남았다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- F2에서 `implementation` 스킬 삭제 시 "implement the plan" 계열 트리거가 사라짐 — implementation-lite description이 그 트리거를 흡수할지는 F2 draft에서 결정. 사용자 확인은 그때.
- full 명시 요청 처리: 방어 문구 없이 부재로 답한다(방어적 사족 금지 규범) — 결정 완료, 확인 불요.
- autopilot 스킬명 유지: "autopilot"이라는 이름은 lite 체인 자동 실행 의미로 여전히 유효 — 결정 완료, 확인 불요.
