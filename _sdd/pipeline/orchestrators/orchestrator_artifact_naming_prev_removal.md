# Orchestrator: 아티팩트 파일명 패턴 변경 및 prev/ 백업 제거

**생성일**: 2026-04-10
**규모**: 중규모 (definition/docs overhaul)
**생성자**: autopilot
**Discussion**: `_sdd/discussion/discussion_artifact_naming_and_prev_removal.md`

## 기능 설명

SDD 스킬/에이전트 정의에서 prev/ 백업 로직을 전면 제거하고, 6개 스킬의 산출물 파일명을 slug 기반 `<YYYY-MM-DD>_<filename>_<slug>.md` 패턴으로 통일한다. `.claude/skills/`, `.claude/agents/`, `.codex/skills/`, `.codex/agents/` 4개 디렉토리에 동시 적용한다.

## Acceptance Criteria

- [ ] AC1: 모든 스킬/에이전트 정의에서 prev/ 백업 로직이 제거되었다 (grep `prev/` 결과 0건 — 단, spec-snapshot의 prev/ 제외 규칙도 함께 제거)
- [ ] AC2: slug 전환 대상 6개 스킬(feature-draft, implementation-plan, implementation-review, implementation, pr-review, guide-create)의 출력 파일명이 `<YYYY-MM-DD>_<filename>_<slug>.md` 패턴으로 변경되었다
- [ ] AC3: slug 파일을 읽는 5개 스킬(implementation, implementation-review, spec-update-done, spec-summary, sdd-autopilot)의 입력 경로/glob 패턴이 새 파일명 형식에 맞게 업데이트되었다
- [ ] AC4: global spec (`_sdd/spec/main.md`)의 prev/ guardrail이 새 정책을 반영하도록 업데이트되었다
- [ ] AC5: `.claude/`와 `.codex/` 간 미러 정합성이 유지된다 (동일한 변경이 양쪽에 적용)
- [ ] AC6: DECISION_LOG, changelog, 과거 로그 등 역사적 기록은 수정하지 않았다

## Reasoning Trace

- 토론에서 결정은 완료되었으나, ~25개 파일에 걸친 변경이므로 feature-draft로 temporary spec + implementation plan을 먼저 고정한다.
- 대상이 스킬 정의 문서(SKILL.md, agent .md/.toml)이므로 전통적 테스트 프레임워크 대신 inline grep 검증을 사용한다.
- global spec의 guardrail 1건도 수정 대상이므로 spec-update-done을 파이프라인에 포함한다.
- review-fix loop으로 미러 정합성과 누락된 참조를 검증한다.
- `Spec-first` 원칙 적용: global spec guardrail을 구현 결과에 맞게 동기화한다.

## Pipeline Steps

### Step 1: feature-draft
**Claude subagent_type**: `feature-draft`
**입력 파일**: `_sdd/discussion/discussion_artifact_naming_and_prev_removal.md`, `_sdd/spec/main.md`
**출력 파일**: `_sdd/drafts/feature_draft_artifact_naming_prev_removal.md`

**프롬프트**:
`_sdd/discussion/discussion_artifact_naming_and_prev_removal.md` 토론 결과를 기반으로 feature draft를 작성하세요.
Part 1에는 temporary spec 7섹션을 포함하고, Part 2에는 Target Files 기반 implementation plan을 작성하세요.

변경 내용 요약:
1. 모든 스킬/에이전트에서 prev/ 백업 로직 완전 제거
2. 6개 스킬의 산출물 파일명을 `<YYYY-MM-DD>_<filename>_<slug>.md` 패턴으로 전환
3. downstream 스킬의 입력 경로/glob 패턴 업데이트
4. 4개 디렉토리 동시 적용: `.claude/skills/`, `.claude/agents/`, `.codex/skills/`, `.codex/agents/`

대상 파일 목록 (탐색 결과 기반):

**prev/ 제거 대상 (쓰기 스킬):**
- `.claude/skills/implementation-review/SKILL.md` (lines 23, 59, 158)
- `.claude/agents/implementation-review.md` (lines 24, 59, 158)
- `.codex/skills/implementation-review/SKILL.md` (lines 57, 190)
- `.codex/agents/implementation-review.toml` (lines 54, 187)
- `.claude/skills/implementation/SKILL.md` (line 227)
- `.claude/agents/implementation.md` (line 228)
- `.codex/skills/implementation/SKILL.md` (line 194)
- `.codex/agents/implementation.toml` (line 191)
- `.claude/skills/pr-review/SKILL.md` (lines 17, 50, 203)
- `.codex/skills/pr-review/SKILL.md` (lines 17, 50, 209)
- `.claude/skills/pr-review/examples/sample-review.md` (line 352)
- `.claude/skills/guide-create/SKILL.md` (lines 24, 30, 34, 132, 167)
- `.claude/skills/guide-create/references/output-format.md` (lines 17-18)
- `.codex/skills/guide-create/SKILL.md` (lines 42, 47, 128)
- `.codex/skills/guide-create/references/output-format.md` (lines 17-18)

**prev/ 제거 대상 (spec 스킬):**
- `.claude/skills/spec-update-todo/SKILL.md` (line 27)
- `.claude/agents/spec-update-todo.md` (line 22)
- `.codex/skills/spec-update-todo/SKILL.md` (line 27)
- `.codex/agents/spec-update-todo.toml` (line 24)
- `.claude/skills/spec-update-done/SKILL.md` (lines 28, 158)
- `.claude/agents/spec-update-done.md` (lines 23, 128)
- `.codex/skills/spec-update-done/SKILL.md` (lines 28, 166)
- `.codex/agents/spec-update-done.toml` (lines 25, 163)
- `.claude/skills/spec-upgrade/SKILL.md` (lines 20, 49, 88)
- `.codex/skills/spec-upgrade/SKILL.md` (lines 20, 49, 88)
- `.claude/skills/spec-rewrite/SKILL.md` (lines 19, 43, 98-99)
- `.codex/skills/spec-rewrite/SKILL.md` (lines 19, 43, 98-99)
- `.claude/skills/spec-summary/SKILL.md` (line 40)
- `.codex/skills/spec-summary/SKILL.md` (line 40)
- `.claude/skills/spec-create/SKILL.md` (lines 57, 188)
- `.codex/skills/spec-create/SKILL.md` (lines 66, 196)

**prev/ 제외 규칙 제거 (spec-snapshot):**
- `.claude/skills/spec-snapshot/SKILL.md` (lines 20, 30, 65)
- `.codex/skills/spec-snapshot/SKILL.md` (lines 19, 27, 41)

**slug 기반 파일명 전환 (쓰기 경로):**
- feature-draft: `.claude/skills/feature-draft/SKILL.md`, `.codex/skills/feature-draft/SKILL.md`
- implementation-plan: `.claude/skills/implementation-plan/SKILL.md`, `.claude/agents/implementation-plan.md`, `.codex/skills/implementation-plan/SKILL.md`, `.codex/agents/implementation-plan.toml`
- implementation-review: (위 prev/ 제거와 동시 처리)
- implementation: (위 prev/ 제거와 동시 처리)
- pr-review: (위 prev/ 제거와 동시 처리)
- guide-create: (위 prev/ 제거와 동시 처리)

**읽기 경로 업데이트:**
- implementation: `.claude/skills/implementation/SKILL.md` (lines 66-69), `.claude/agents/implementation.md`, `.codex/skills/implementation/SKILL.md` (lines 69-72), `.codex/agents/implementation.toml`
- implementation-review: `.claude/skills/implementation-review/SKILL.md` (line 71), `.claude/agents/implementation-review.md`, `.codex/skills/implementation-review/SKILL.md` (line 103), `.codex/agents/implementation-review.toml`
- spec-update-done: `.claude/skills/spec-update-done/SKILL.md` (lines 42-46), `.claude/agents/spec-update-done.md`, `.codex/skills/spec-update-done/SKILL.md` (lines 61-64), `.codex/agents/spec-update-done.toml`
- spec-summary: `.claude/skills/spec-summary/SKILL.md` (line 55), `.codex/skills/spec-summary/SKILL.md` (line 54)
- sdd-autopilot: `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` (lines 39, 48, 66), `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`

역사적 기록(`_sdd/spec/DECISION_LOG.md`, `_sdd/spec/logs/changelog.md` 등)은 수정하지 않는다.

Part 2에서 각 파일별 정확한 변경 내용을 Target Files로 정리하세요.

**Exit Criteria**: feature draft 파일이 생성되고, Part 1 temporary spec 7섹션과 Part 2 implementation plan이 모두 포함됨.

### Step 2: implementation
**Claude subagent_type**: `implementation`
**입력 파일**: `_sdd/drafts/feature_draft_artifact_naming_prev_removal.md`, `_sdd/discussion/discussion_artifact_naming_and_prev_removal.md`
**출력 파일**: 수정된 스킬/에이전트 파일들

**프롬프트**:
feature draft의 Part 2 implementation plan을 따라 모든 스킬/에이전트 정의 파일을 수정하세요.

핵심 규칙:
1. prev/ 관련 로직(mkdir, mv, 아카이브 설명, AC, Hard Rule, Error Handling)을 모두 제거
2. slug 전환 대상 스킬의 출력 파일명을 `<YYYY-MM-DD>_<filename>_<slug>.md` 패턴으로 변경
3. downstream 스킬의 입력 경로를 새 패턴에 맞게 업데이트 (glob 패턴 포함)
4. `.claude/`와 `.codex/` 양쪽에 동일하게 적용
5. 역사적 기록은 절대 수정하지 않음
6. ralph-loop-init의 state_backup은 prev/와 무관하므로 수정하지 않음

**Exit Criteria**: 모든 대상 파일 수정 완료, implementation report 생성.

### Step 3: review-fix loop
(autopilot 직접 관리)

### Step 4: spec-update-done
**Claude subagent_type**: `spec-update-done`
**입력 파일**: `_sdd/spec/main.md`, `_sdd/spec/components.md`, 수정된 스킬 파일들
**출력 파일**: `_sdd/spec/main.md`

**프롬프트**:
아티팩트 파일명 패턴 변경 및 prev/ 백업 제거가 완료되었습니다. global spec을 동기화하세요.

변경 사항:
1. `main.md` line 63의 prev/ guardrail을 제거하거나 새 정책 반영: "spec mutation은 target file을 식별한 뒤에만 수행한다. 변경 이력은 git으로 관리한다."
2. `components.md`에서 spec-rewrite의 "백업" 언급이 있으면 업데이트
3. temporary execution detail은 global spec에 올리지 않는다

**Exit Criteria**: global spec 업데이트 완료, prev/ guardrail이 새 정책 반영.

## Review-Fix Loop

- **최대 반복 횟수**: 2
- **종료 조건**: critical = 0 AND high = 0 AND medium = 0
- **수정 대상**: critical / high / medium
- **MAX 도달 시**: critical/high 잔존 → 중단, medium만 잔존 → 로그 기록 후 계속

## Test Strategy

- **방식**: inline grep/diff 검증
- **선택 근거**: 이 저장소는 전통적 테스트 프레임워크를 사용하지 않으며, 스킬 정의 문서 변경이므로 패턴 매칭 검증이 적합
- **실행 명령**:
  1. `rg -n "prev/" .claude/skills/ .claude/agents/ .codex/skills/ .codex/agents/ --glob '!*.toml'` → 0건 확인 (spec-snapshot의 prev/ 제외 규칙도 포함)
  2. `rg -n "prev/" .codex/agents/` → 0건 확인 (toml 파일)
  3. `rg -n "<YYYY-MM-DD>_" .claude/skills/feature-draft/ .claude/skills/implementation-plan/ .claude/skills/implementation-review/ .claude/skills/implementation/ .claude/skills/pr-review/ .claude/skills/guide-create/` → 각 스킬에서 새 패턴 존재 확인
  4. `rg -n "prev/" _sdd/spec/main.md` → 0건 확인
  5. `.claude/` vs `.codex/` 미러 정합성: 핵심 패턴 diff 비교
- **사용자 보고 형식**: 검증 항목별 통과/실패 테이블

## Error Handling

- **재시도 횟수**: 각 step 최대 1회
- **핵심 단계**: Step 1 (feature-draft), Step 2 (implementation), Step 3 (review-fix)
- **비핵심 단계**: Step 4 (spec-update-done) — 실패 시 로그 기록 후 수동 처리 안내
