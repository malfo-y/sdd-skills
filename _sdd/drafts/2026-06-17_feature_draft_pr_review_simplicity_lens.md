# Feature Draft: pr-review에 simplicity 렌즈 추가 (PR 차원 직교 2-렌즈 review)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

`pr-review` 스킬을 자체 correctness 검증(PR/spec/보안/테스트/verdict)은 그대로 유지하면서 `simplicity-review-agent`를 추가 dispatch하는 **PR 차원 직교 2-렌즈 review**로 확장한다. pr-review가 자체 PR/spec correctness를 검증하는 동안, 같은 PR diff의 변경 파일을 `simplicity-review-agent`(read-only leaf, 동작-불변 형태 품질 렌즈)가 병렬로 본다. simplicity 차원을 pr-review가 자체 복제하지 않고 기존 단일 소스 agent를 재사용한다(DRY).

동기: implementation review-gate에 이미 적용된 직교 2-렌즈 패턴(correctness ∥ simplicity 병렬 dispatch, 표적 disjoint)을 PR review 진입점에도 적용한다. pr-review는 인간 리뷰 보조이므로 simplicity finding을 verdict에 강제로 묶지 않고, falsifiable gating finding(Medium+)은 REQUEST CHANGES rationale에 기여하고 주관적(Low)은 Suggested Improvements로 흘린다.

## Scope Delta

### In-scope (delta)
- `pr-review` 스킬을 자체 correctness 검증 + `simplicity-review-agent` 추가 dispatch를 수행하는 **review-only orchestrator**로 승격한다. 기존 Step 0(branch check)~6(report) 골격, verdict 기준, 리포트 경로(`_sdd/pr/<date>_pr_review_<slug>.md`)는 유지한다. simplicity dispatch는 추가 레인이다.
- pr-review가 PR diff 변경 파일 목록 + from-branch 컨텍스트를 simplicity reviewer에 전달해 동작-불변 형태를 falsifiable-only gating으로 리뷰하게 한다.
- simplicity 리포트는 simplicity-review-agent의 자기 경로(`_sdd/implementation/<date>_simplicity_review_<slug>.md`)에 저장된다(단일 작성자 불변식 유지). pr-review는 그 리포트의 finding 요약을 받아 자기 리포트(`_sdd/pr/...`)의 신규 Simplicity 섹션에 통합한다.
- 표적 disjoint 경계 (falsifiable): pr-review 자체 렌즈=correctness(PR/spec 정합·보안·테스트·verdict + **정확성-중복**: 중복된 보안 검증 누락·일관성 깨진 중복 분기 등 로직 버그성 중복), simplicity-review-agent=동작-불변 형태(**형태-중복**: 동일 로직 반복·추출 가능한 중복 구현·죽은 코드·단일 사용처 추상화·도달 불가 에러 처리·과잉압축). 기존 pr-review Code-only "코드 품질: 중복" 항목 중 형태-중복만 simplicity reviewer로 위임하고, 정확성-중복은 correctness 자체 검증에 잔존시키며 Code-only의 단독 "중복" 표적 단어는 제거한다.
- verdict 통합 정책(아래 Persistent Spec Implications에 계약으로 명시): falsifiable gating simplicity finding(Medium+)은 REQUEST CHANGES rationale에 기여, 주관적(Low)은 Suggested Improvements.

### Out-of-scope (delta)
- `simplicity-review-agent` 자체는 변경하지 않는다(단일 소스 재사용). 5개 차원·falsifiable-only gating·re-review mode·리포트 경로 계약을 그대로 소비한다.
- `spec-review` gate는 simplicity 렌즈로 확장하지 않는다(코드 형태 품질이라 spec 문서 품질에 부적합 — 기존 spec 제약 유지).
- pr-review에 fix → re-review loop를 도입하지 않는다. pr-review는 인간 리뷰 보조이며 verdict + 리포트로 닫는다(autopilot의 implementation review-fix loop와 다른 경로).

### Guardrail delta
- 단일 작성자 불변식 유지: simplicity reviewer는 자기 리포트(`_sdd/implementation/...`)만 쓰고, pr-review는 자기 리포트(`_sdd/pr/...`)만 쓴다. 두 리포트가 별도 경로라 병렬 dispatch 시 write 충돌이 없다.
- nesting 1단계 유지: simplicity reviewer는 read-only leaf이며 sub-agent를 spawn하지 않는다. pr-review가 leaf를 dispatch하는 orchestrator가 된다.
- 병렬 안전성: pr-review 자체 검증과 simplicity reviewer dispatch는 모두 read 기반이라 동시 진행이 안전하다.

## Persistent Spec Implications

persistent spec(`_sdd/spec/main.md`)에 남아야 하는 계약/불변식/검증 의도:

- **simplicity 렌즈 적용 범위 확장 (surgical: 절 교체 아닌 절 추가)**: 현재 `_sdd/spec/main.md` L71은 implementation review-gate 항목 본문 끝에 종속 절로 `simplicity 렌즈는 `spec-review`로 확장하지 않는다(코드 형태 품질이라 spec 문서 품질에 부적합)`를 담는다. 이 spec-review 비확장 종속 절은 **그대로 유지**하고, PR review로의 확장은 별도 bullet/절 추가로 surgical 반영한다 — 추가할 내용: **"simplicity 렌즈는 implementation-scoped review-gate에 더해 PR review(`pr-review` 스킬)에도 적용한다 — `pr-review`는 자체 correctness 검증 ∥ `simplicity-review-agent` 병렬 dispatch의 PR 차원 직교 2-렌즈 review이며, simplicity finding은 verdict를 자동 강제하지 않고 falsifiable gating finding(Medium+)이 REQUEST CHANGES rationale에 기여한다."** L71 기존 문구를 교체·재작성하지 않으며 spec-review 비확장 제약을 손대지 않는다.
- **PR 차원 직교 2-렌즈 review 계약**: `pr-review`는 자체 correctness 렌즈(PR/spec 정합·보안·테스트·verdict)와 simplicity 렌즈(`simplicity-review-agent` — 동작-불변 형태)를 병렬로 적용한다. 두 렌즈는 표적 disjoint다. simplicity reviewer는 read-only leaf, 자기 리포트(`_sdd/implementation/...`)만 write.
- **PR verdict 통합 정책**: simplicity finding은 verdict를 강제하지 않고 다음으로 합류한다 — falsifiable gating finding(Medium+)은 REQUEST CHANGES rationale에 기여, 주관적 취향(Low)은 Suggested Improvements. pr-review는 인간 리뷰 보조이므로 implementation gate의 `critical=high=medium=0` 합집합 exit 같은 자동 gating을 적용하지 않는다.
- **falsifiable-only gating 재사용**: PR review에서도 simplicity finding의 Medium=gating / Low=advisory 분류는 `simplicity-review-agent`의 falsifiable-only gating 계약을 그대로 따른다(신규 계약 복제 없음).

<!-- spec-update-todo-input-end -->

# Part 2: Implementation and Validation Plan

## Overview

이 plan은 Part 1의 PR 차원 직교 2-렌즈 계약을 `pr-review` 스킬 두 surface(claude+codex)에 구현한다. 신규 agent를 만들지 않고 기존 `simplicity-review-agent`(단일 소스)를 재사용하므로 Target은 `pr-review` 스킬 본문 2개로 한정된다. 변경 골자: Process에 simplicity reviewer dispatch 레인 추가(Step 1에서 수집한 PR diff 변경 파일 + from-branch 컨텍스트를 message로 전달), Code-only 검증의 "중복" 표적을 simplicity reviewer로 위임해 표적 disjoint 정리, verdict 정책에 simplicity finding 합류 규칙 추가, Output Format에 Simplicity 섹션 추가, codex 미러는 `spawn_agent` 표현으로 동형 적용.

`pr-review`가 dispatch하는 leaf agent는 `simplicity-review-agent` 하나이며 그 계약(5개 차원·falsifiable-only gating·리포트 경로·read-only leaf)은 그대로 소비한다 — 이번 변경에서 agent 본문은 read-only 참조다.

## Scope

### In Scope
- `.claude/skills/pr-review/SKILL.md`: simplicity reviewer dispatch 레인 추가, Code-only 중복 표적 위임, verdict 정책 확장, Output Format Simplicity 섹션 추가
- `.codex/skills/pr-review/SKILL.md`: 동일 변경을 codex `spawn_agent`/`wait_agent`/`close_agent` 표현으로 미러

### Out of Scope
- `simplicity-review-agent`(`.claude/agents/simplicity-review-agent.md`, `.codex/agents/simplicity-review-agent.toml`) 변경 — 단일 소스 재사용, read-only 참조
- `_sdd/spec/main.md` 갱신 — Part 1 Spec Delta로만 명시하며 구현 Target 아님(`spec-update-done`이 처리)
- `spec-review` 스킬/agent 변경 (Part 1 out-of-scope)
- pr-review fix → re-review loop 도입 (Part 1 out-of-scope)

## Contract/Invariant Delta and Coverage

| ID | Type | Change | Covered By | Validated By |
|----|------|--------|------------|--------------|
| C1 | Modify | `pr-review`가 자체 correctness 검증 ∥ `simplicity-review-agent` 병렬 dispatch의 review-only orchestrator로 동작한다. Step 0~6 골격·verdict 기준·리포트 경로는 유지하고 simplicity는 추가 레인. frontmatter version bump(2.0.0→3.0.0) 동반 | T1, T2 | V1a, V1b, V1c, V8 |
| C2 | Modify | `pr-review`가 PR diff 변경 파일 목록 + from-branch 컨텍스트를 simplicity reviewer message로 전달한다 | T1, T2 | V2 |
| C3 | Add | verdict 통합 정책 (**default 권장안, 구현 전 사용자 확인 게이트 — Q2**): simplicity gating finding(Medium+)은 REQUEST CHANGES rationale에 기여, 주관(Low)은 Suggested Improvements. verdict 자동 강제는 없음(인간 리뷰 보조). 통합 강도 확정은 Q2 사용자 확인 후 — 본 plan은 권장안을 default로 명세하되 구현 task가 확정 게이트를 통과해야 한다 | T1, T2 | V3 |
| C4 | Add | Output Format에 Simplicity 섹션 추가 + simplicity 리포트 경로(`_sdd/implementation/<date>_simplicity_review_<slug>.md`) 참조 | T1, T2 | V4 |
| C5 | Modify | 표적 disjoint (falsifiable 경계): **형태-중복**(동작 불변 — 동일 로직 반복, 추출 가능한 중복 구현 → simplicity reviewer 소관)을 Code-only에서 simplicity로 위임하고, **정확성-중복**(로직 버그성 — 중복된 보안 검증 누락·일관성 깨진 중복 분기 등 동작에 영향 → correctness 소관)은 pr-review 자체 검증에 잔존시킨다. Code-only 검증의 단독 "중복" 표적 단어는 제거하고 두 측면을 각 렌즈로 분리 명시 | T1, T2 | V5 |
| I1 | Invariant | 단일 작성자 불변식 유지 — simplicity reviewer는 자기 리포트(`_sdd/implementation/...`)만, pr-review는 자기 리포트(`_sdd/pr/...`)만 write. 별도 경로라 병렬 write 충돌 없음 | T1, T2 | V1d, V6 |
| I2 | Invariant | claude/codex 미러 정합 — 두 surface가 동일 계약(dispatch 레인·verdict 정책·Simplicity 섹션·표적 disjoint)을 담는다 | T1, T2 | V7 |

## Touchpoints

현재 코드 기준으로 재확인한 변경 지점 (각 항목은 read로 검증함):

- **`.claude/skills/pr-review/SKILL.md`** — agent dispatch가 전혀 없는 단일 스킬(v2.0.0). 갱신 지점: (a) Process Step 3 "Code-only 검증" 테이블의 "코드 품질: ... 중복" 항목(L67) — 동작-불변 형태 중복을 simplicity reviewer로 위임(표적 disjoint, C5). (b) Step 5 Verdict 테이블 전후 — simplicity finding 합류 정책 추가(C3). (c) Step 1과 Step 5 사이 또는 Step 4 다음에 simplicity reviewer dispatch 레인 추가(C1/C2) — Step 1에서 이미 수집하는 `gh pr diff [PR] --name-only`(L45) 변경 파일 목록 + from-branch spec 컨텍스트를 message로 전달. (d) Output Format(L100-192)에 Simplicity 섹션 + simplicity 리포트 경로 참조 추가(C4). (e) AC 섹션(L13-16)에 simplicity dispatch AC 추가.
- **`.codex/skills/pr-review/SKILL.md`** — 동일 본문에 `Codex Runtime Adapter` 컨벤션. **dispatch canonical 표현은 surface별로 다르다(`implementation` SKILL 현행 코드 기준)**: claude는 `Agent(subagent_type="sdd-skills:simplicity-review-agent")` (**`sdd-skills:` prefix 필수** — `.claude/skills/implementation/SKILL.md` L197/L221, spec L77과 정합), codex는 `spawn_agent({agent_type: "simplicity-review-agent", message: ...})` → `wait_agent` → `close_agent` (**prefix 없음** — codex kebab-case canonical, `.codex/skills/implementation/SKILL.md` L20/L234와 정합). Step 2 from-branch spec 로딩 로직이 claude보다 상세(L50-64)하나 simplicity dispatch 추가 지점은 claude와 동형. Hard Rules의 `$spec-update-todo` codex 표기(L19)는 무변경.
- **`.claude/agents/simplicity-review-agent.md` / `.codex/agents/simplicity-review-agent.toml`** (read-only 참조, Target 아님) — 입력 우선순위가 "사용자 경로 → implementation_plan glob → legacy fallback → 변경된 코드 파일"(Step 1 Scope)이며, pr-review가 변경 파일 경로를 message로 명시 전달하면 그 경로를 리뷰 대상으로 받는다. 리포트 경로 `_sdd/implementation/<date>_simplicity_review_<slug>.md`, re-review mode는 기존 리포트 경로 입력 시 동작. agent 변경 없이 이 계약을 그대로 소비한다.
- **`.codex/agents/README.md`** (read-only 참조) — `simplicity-review-agent`가 이미 Agent Set(L26)·Inline Writing(L40)에 등재됨. Invocation Contract(L43-55)가 `spawn_agent`/`wait_agent`/`close_agent` 규약 정의. codex pr-review dispatch 표현이 이 규약을 따른다.

## Implementation Phases

### Phase 1: pr-review 스킬 2-렌즈 확장 (claude → codex)

| Task | 목적 | Dependencies |
|------|------|--------------|
| T1 | `.claude/skills/pr-review/SKILL.md`에 simplicity dispatch 레인 + verdict 정책 + 표적 disjoint + Simplicity 섹션 추가 | - |
| T2 | `.codex/skills/pr-review/SKILL.md`에 동일 변경 미러(codex spawn_agent 표현) | T1 |

## Task Details

### Task T1: pr-review (claude) PR 차원 2-렌즈 확장
**Priority**: P0
**Type**: Feature

**Description**: `.claude/skills/pr-review/SKILL.md`를 자체 correctness 검증 ∥ `simplicity-review-agent` 병렬 dispatch의 review-only orchestrator로 확장한다. 기존 Step 0(branch check)~6(report) 골격, verdict 3종(APPROVE/REQUEST CHANGES/NEEDS DISCUSSION) 기준, 리포트 경로(`_sdd/pr/<date>_pr_review_<slug>.md`)는 유지하고 다음을 추가/수정한다:

1. **simplicity dispatch 레인 추가**: 새 Process 단계로 `simplicity-review-agent`를 dispatch한다. **claude canonical dispatch 표현은 `Agent(subagent_type="sdd-skills:simplicity-review-agent")` — `sdd-skills:` prefix를 포함한다**(`.claude/skills/implementation/SKILL.md` L197/L221, spec L77 Claude canonical과 정합). Step 1에서 이미 수집하는 `gh pr diff [PR] --name-only` 변경 파일 목록과 from-branch spec 컨텍스트를 message로 전달해, 변경 파일을 simplicity reviewer의 리뷰 대상 경로로 명시한다(agent Step 1 Scope의 "사용자 경로" 입력 경로로 진입). simplicity reviewer가 read-only leaf라 pr-review 자체 검증과 동시 진행이 안전함을 명시한다. simplicity 리포트는 agent 자기 경로(`_sdd/implementation/<date>_simplicity_review_<slug>.md`)에 저장되고, pr-review는 그 finding 요약(severity별)을 받아 통합한다.
2. **표적 disjoint 정리 (falsifiable 경계)**: Step 3 Code-only 검증 테이블의 "코드 품질" 행에서 **형태-중복(동작 불변 — 동일 로직 반복·추출 가능한 중복 구현)**을 simplicity reviewer 소관으로 위임하고, **정확성-중복(로직 버그성 — 중복된 보안 검증 누락·일관성 깨진 중복 분기 등 동작에 영향)**은 pr-review correctness 자체 검증에 잔존시킨다. Code-only의 단독 "중복" 표적 단어는 제거하고, pr-review Code-only는 correctness 표적(네이밍/패턴/컨벤션·에러 처리·테스트·보안·성능·문서 + 정확성-중복)만 남긴다. 두 측면 분리 경계를 한 줄로 명시한다(R2 누수 차단).
3. **verdict 정책 확장 (default 권장안 — Q2 확인 게이트)**: Step 5 Verdict에 simplicity finding 합류 규칙을 추가한다 — falsifiable gating finding(Medium+)은 REQUEST CHANGES rationale에 기여(인간 리뷰 보조라 자동 강제는 아님), 주관(Low)은 Suggested Improvements로 흐른다. implementation gate의 `critical=high=medium=0` 합집합 자동 exit를 PR review에 적용하지 않음을 명시한다. **이 통합 강도는 Q2(`User confirmation needed=Yes`)의 권장 default이며, 구현 착수 전 사용자 verdict 정책 확인을 거친다 — 확인 결과 강도가 바뀌면(예: 자동 강제 채택 / 완전 분리) 본 description의 합류 규칙을 그에 맞춰 조정한다.**
4. **Output Format Simplicity 섹션**: Output Format에 Simplicity 섹션(severity별 finding 요약 + simplicity 리포트 경로 링크)을 추가한다. Recommendations의 Pre-merge Blockers / Suggested Improvements 매핑에 simplicity finding이 어느 쪽으로 가는지 반영한다.
5. **AC 추가**: simplicity reviewer가 dispatch되고 그 finding이 verdict 정책대로 합류했다는 AC를 Acceptance Criteria에 추가한다.

**Non-Goals**: `simplicity-review-agent` 본문을 수정하지 않는다(단일 소스 재사용). pr-review에 fix → re-review loop를 도입하지 않는다(verdict + 리포트로 닫는 인간 리뷰 보조). `spec-review`로 simplicity를 확장하지 않는다. Step 0~6 기본 골격·verdict 3종·리포트 경로 계약을 바꾸지 않는다.

**Acceptance Criteria**:
- [ ] Process에 `simplicity-review-agent` dispatch 단계가 있고 claude canonical 표현 `Agent(subagent_type="sdd-skills:simplicity-review-agent")`(`sdd-skills:` prefix 포함)을 쓴다. 그 단계가 `gh pr diff [PR] --name-only` 변경 파일 목록 + from-branch 컨텍스트를 message로 전달함을 명시한다 (`grep -n 'sdd-skills:simplicity-review-agent' .claude/skills/pr-review/SKILL.md`로 prefix 포함 canonical 이름 존재 확인 — prefix 없는 비-canonical 표기는 통과 불가 + diff 입력 전달 문구 grep)
- [ ] simplicity reviewer가 read-only leaf라 pr-review 자체 correctness 검증과 동시 진행 안전하다는 근거가 적혀 있다
- [ ] Step 3 Code-only "코드 품질" 행에서 **형태-중복(동작 불변)**이 simplicity reviewer로 위임되고 **정확성-중복(로직 버그성 — 중복된 보안 검증 누락 등)**은 correctness 자체 검증에 잔존함이 명시되며, 단독 "중복" 표적 단어가 Code-only 테이블에서 제거된다 (`grep -n '중복' .claude/skills/pr-review/SKILL.md`로 Code-only 행에 위임/잔존 경계 없는 단독 "중복" 표적이 남지 않음 확인)
- [ ] Step 5 Verdict에 "simplicity gating finding(Medium+) → REQUEST CHANGES rationale 기여, 주관(Low) → Suggested Improvements"가 명시되고, PR review가 simplicity finding으로 verdict를 자동 강제하지 않음(인간 리뷰 보조)이 적혀 있다
- [ ] **(Q2 확인 게이트)** verdict 통합 강도가 Q2 default 권장안임을 인지하고, 구현 착수 전 사용자 verdict 정책 확인을 거친다 — 확인 전에는 권장안(Medium+ → rationale 기여, 자동 강제 아님)을 default로 두되, 확정 결과에 따라 합류 규칙을 조정할 수 있음이 task 진행 메모에 반영된다
- [ ] Output Format에 Simplicity 섹션(severity별 finding 요약 + 리포트 경로 `_sdd/implementation/<date>_simplicity_review_<slug>.md` 참조)이 추가된다
- [ ] simplicity 리포트가 agent 자기 경로에 저장되고 pr-review는 자기 리포트(`_sdd/pr/...`)에만 통합 요약을 쓴다(단일 작성자 불변식)는 점이 명시된다
- [ ] Acceptance Criteria 섹션에 simplicity dispatch + finding 합류 AC가 추가된다
- [ ] Step 0(branch check)~6(report) 골격·verdict 3종(APPROVE/REQUEST CHANGES/NEEDS DISCUSSION)·리포트 경로(`_sdd/pr/<date>_pr_review_<slug>.md`)가 보존된다 (기존 verdict 3종 grep 잔존, 리포트 경로 무변경)
- [ ] frontmatter version이 2.0.0 → 3.0.0으로 bump된다 (`grep -n 'version:' .claude/skills/pr-review/SKILL.md`로 3.0.0 확인 — dispatch 동작 추가로 스킬 인터페이스가 바뀌므로)

**Target Files**:
- [M] `.claude/skills/pr-review/SKILL.md` -- simplicity dispatch 레인 + 표적 disjoint + verdict 정책 + Simplicity 섹션 추가

**Technical Notes**: Covers C1, C2, C3, C4, C5, I1; validated by V1a, V1b, V1c, V1d, V2~V6, V8. `simplicity-review-agent`는 read-only 참조 — Min-Code: 신규 계약 복제 없이 기존 agent의 5개 차원·falsifiable-only gating·리포트 경로를 그대로 소비한다. pr-review가 변경 파일 경로를 message로 명시 전달하는 이유: agent Step 1 Scope 입력 우선순위가 "사용자 경로"를 최우선으로 받으므로, PR diff 파일을 그 경로로 넘기면 리뷰 대상이 PR 범위로 고정된다(전체 변경 코드 glob fallback 회피). frontmatter version bump(2.0.0 → 3.0.0) 동반 — dispatch 동작이 추가돼 스킬 인터페이스가 바뀐다.

**Dependencies**: -

---

### Task T2: pr-review (codex) 미러
**Priority**: P0
**Type**: Feature

**Description**: `.codex/skills/pr-review/SKILL.md`에 T1과 동일 계약을 codex 표현으로 미러한다. simplicity dispatch는 codex Invocation Contract(`.codex/agents/README.md` L43-55)에 따라 `spawn_agent({agent_type: "simplicity-review-agent", message: ...})` → `wait_agent(...)` → 결과 기록 → `close_agent({target: ...})` 순서로 표현한다. message에 PR diff 변경 파일 목록 + from-branch 컨텍스트를 담는다. 표적 disjoint(중복 위임), verdict 정책(Medium+ → rationale, Low → Suggested Improvements), Output Format Simplicity 섹션, AC 추가를 T1과 1:1로 미러한다. codex 고유 표기(`$spec-update-todo` 등 L19)는 무변경.

**Acceptance Criteria**:
- [ ] simplicity dispatch가 `spawn_agent`/`wait_agent`/`close_agent` 규약으로 표현되고 `agent_type: "simplicity-review-agent"`(**codex는 prefix 없는 kebab-case canonical** — `.codex/skills/implementation/SKILL.md` L20/L234와 정합) message에 PR diff 변경 파일 + from-branch 컨텍스트가 담긴다 (`grep -n 'agent_type: "simplicity-review-agent"' .codex/skills/pr-review/SKILL.md`로 확인 — claude의 `sdd-skills:` prefix를 codex에 잘못 옮기지 않음)
- [ ] 표적 disjoint(중복 위임)·verdict 정책(Medium+ → rationale / Low → Suggested Improvements)·Output Format Simplicity 섹션·simplicity 리포트 경로 참조가 T1(claude)과 1:1 대응한다 (I2)
- [ ] Acceptance Criteria 섹션에 simplicity dispatch + finding 합류 AC가 T1과 동형으로 추가된다
- [ ] Step 0~6 골격·verdict 3종·리포트 경로가 보존된다 (claude와 동일)
- [ ] frontmatter version이 2.0.0 → 3.0.0으로 bump된다 (`grep -n 'version:' .codex/skills/pr-review/SKILL.md`로 3.0.0 확인 — claude T1과 동일 정책)

**Target Files**:
- [M] `.codex/skills/pr-review/SKILL.md` -- T1 동형 미러 (codex spawn_agent 표현)

**Technical Notes**: Covers C1, C2, C3, C4, C5, I1, I2; validated by V1a, V1b, V1c, V1d, V2~V8. claude `.md`와 codex `.md`는 dispatch 호출 표현(claude `Agent(subagent_type="sdd-skills:simplicity-review-agent")` prefix 포함 vs codex `spawn_agent({agent_type: "simplicity-review-agent"})` prefix 없음)만 다르고 계약은 동일하다 — 미러 정합(I2)이 V7 검증 대상. codex frontmatter version도 T1과 동일 정책으로 bump.

**Dependencies**: T1

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1a | C1 (dispatch 배선) | test (1등급 정량) | `grep -n 'sdd-skills:simplicity-review-agent' .claude/skills/pr-review/SKILL.md` 및 `grep -n 'agent_type: "simplicity-review-agent"' .codex/skills/pr-review/SKILL.md`가 각 1+ 매치 → simplicity dispatch 레인이 surface별 canonical 표현으로 배선됨. 0 매치면 NOT MET. 증거=grep 출력 |
| V1b | C1 (PR 범위 고정) | review (2등급 정성) | 리뷰어가 dispatch 단계 본문을 읽어 `gh pr diff [PR] --name-only` 변경 파일을 simplicity reviewer 리뷰 대상 경로로 명시 전달함을 확인 — PR diff 파일 전달 문구가 없으면 NOT MET. 증거=인용한 message 구성 문장 (V2와 동일 표적, C1 PR 범위 고정 관점 판정) |
| V1c | C1 (골격 보존) | test (1등급 정량) | `grep -nE 'APPROVE\|REQUEST CHANGES\|NEEDS DISCUSSION' .claude/skills/pr-review/SKILL.md`로 verdict 3종 잔존, `grep -n '_sdd/pr/.*_pr_review_' .claude/skills/pr-review/SKILL.md`로 리포트 경로 무변경, Step 0~6 heading 잔존 확인. 셋 중 하나라도 누락이면 NOT MET. 증거=grep 출력 (codex 동일) |
| V1d | I1 (단일 작성자) | review (2등급 정성) | 리뷰어가 본문을 읽어 simplicity reviewer가 자기 경로(`_sdd/implementation/...`)에만 write하고 pr-review는 자기 리포트(`_sdd/pr/...`)에만 통합 요약을 쓴다는 단일 작성자 불변식이 명시됐고 read-only leaf 동시 진행 안전 근거가 적혔는지 확인 — 단일 작성자 위반 표현(pr-review가 simplicity 경로에 write)이 있으면 NOT MET. 증거=인용한 작성자/경로 문장 (V6 grep과 상호 보강) |
| V2 | C2 | review (2등급 정성) | dispatch 단계가 `gh pr diff [PR] --name-only` 변경 파일 목록 + from-branch 컨텍스트를 simplicity reviewer message로 전달함을 리뷰어가 본문 인용으로 확인. message에 PR diff 파일 입력 전달 문구가 없으면 NOT MET. 증거=인용한 message 구성 문장 |
| V3 | C3 | review (2등급 정성) | Step 5 Verdict 본문을 리뷰어가 읽어 default 권장안 "Medium+ → REQUEST CHANGES rationale 기여, Low → Suggested Improvements, simplicity로 verdict 자동 강제 안 함"이 모두 적혔는지 + 이 통합 강도가 Q2 사용자 확인 게이트 대상(구현 전 확인)임이 명시됐는지 확인. 셋 중 하나라도 빠지거나, 자동 gating(`critical=high=medium=0` 합집합 exit)을 PR에 적용하는 표현이 있거나, Q2 확인 게이트 없이 통합 강도를 구현 확정으로 굳히면 NOT MET. 증거=인용한 verdict 정책 문장 + Q2 확인 게이트 문장 |
| V4 | C4 | review (2등급 정성) | Output Format을 리뷰어가 읽어 Simplicity 섹션(severity별 finding 요약 + 리포트 경로 `_sdd/implementation/<date>_simplicity_review_<slug>.md` 참조)이 존재하는지 확인. 섹션 또는 경로 참조가 없으면 NOT MET. 증거=인용한 Output Format 섹션 |
| V5 | C5 | review (2등급 정성) | Step 3 Code-only 검증 테이블을 리뷰어가 읽어 (a) 형태-중복(동작 불변)이 simplicity reviewer로 위임, (b) 정확성-중복(로직 버그성 — 중복 보안 검증 누락 등)이 correctness 자체 검증에 잔존, (c) 단독 "중복" 표적 단어 제거 — 세 경계가 모두 명시됐는지 확인. 형태-중복이 correctness에 잔존하거나 정확성-중복이 simplicity로 새어 누수되면(R2) NOT MET. 증거=인용한 Code-only 테이블 행 + 형태/정확성 분리 경계 문장 |
| V6 | I1 | test (1등급 정량) | `grep -n "_sdd/pr/" .claude/skills/pr-review/SKILL.md`로 pr-review write 경로가 자기 리포트 경로뿐임을 확인, `grep -n "_sdd/implementation/.*simplicity_review" .claude/skills/pr-review/SKILL.md`로 simplicity 경로가 참조(read/통합)로만 등장하고 pr-review가 거기에 write한다는 문구가 없음을 확인. codex 동일. 증거=grep 출력(write 대상은 `_sdd/pr/`만, simplicity 경로는 참조 문맥) |
| V7 | I2 | review (2등급 정성) | `.claude/skills/pr-review/SKILL.md` ↔ `.codex/skills/pr-review/SKILL.md`를 리뷰어가 대조해 (a) simplicity dispatch 레인, (b) 표적 disjoint(형태/정확성 중복 분리), (c) verdict 정책, (d) Output Format Simplicity 섹션, (e) AC 추가 5개 계약 항목이 1:1 대응하는지 확인. 한 항목이라도 한쪽에만 있으면 NOT MET. 증거=항목별 양 surface 인용 또는 불일치 지목 |
| V8 | C1 (version bump) | test (1등급 정량) | `grep -n 'version:' .claude/skills/pr-review/SKILL.md` 및 `grep -n 'version:' .codex/skills/pr-review/SKILL.md`가 양쪽 모두 `3.0.0`(2.0.0에서 bump). 한쪽이라도 2.0.0 잔존이면 NOT MET. 증거=양 surface grep 출력 |

## Parallel Execution Summary

| Phase | Tasks | 병렬 가능 | 충돌/dependency 근거 |
|-------|-------|-----------|----------------------|
| Phase 1 | T1, T2 | 순차 (T1 → T2) | T2(codex 미러)는 T1(claude) 계약 텍스트에 종속 — claude 본문이 미러 source. ④ API contract 생산-소비 패턴(T1이 계약 생산, T2가 소비). Target Files는 disjoint하나 의미적 종속을 dependency edge로 인코딩 |

> 이 draft는 단일 Phase·2 task로, agent 신규 생성이 없어 분기 폭이 작다. `simplicity-review-agent`는 read-only 참조라 Target에 포함되지 않으므로 두 task의 write 대상은 pr-review 스킬 2개 파일뿐이며 서로 disjoint하다.

# Risks/Mitigations and Open Questions

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| R1: pr-review가 PR diff 변경 파일 경로를 명시 전달하지 못하면 simplicity reviewer가 전체 변경 코드 glob fallback으로 PR 범위 밖을 리뷰 | PR과 무관한 finding이 verdict rationale에 섞임 | T1 AC가 `gh pr diff [PR] --name-only` 목록을 message로 명시 전달하도록 강제(V2). agent Step 1 Scope의 "사용자 경로" 최우선 입력 경로로 PR 파일을 고정 |
| R2: 기존 Code-only "중복" 표적을 simplicity로 위임할 때 correctness 측 중복(예: 중복된 보안 검증 누락 같은 정확성 결함)까지 함께 넘어가 표적 누수 | correctness 중복 결함이 어느 렌즈에서도 검출 안 됨 | 위임 대상을 "동작-불변 형태 중복"으로 한정하고 경계 문장을 본문에 명시(C5/V5). simplicity=동작-불변 형태, correctness=정확성 결함은 pr-review 자체 검증에 잔존 |
| R3: simplicity 리포트가 별도 경로에 생기는데 pr-review가 그 경로를 읽어 통합하는 순서가 본문에 불명확하면 finding이 verdict에 반영 안 됨 | Simplicity 섹션이 비거나 verdict 정책이 미적용 | dispatch → wait → finding 요약 수신 → 통합 순서를 본문에 명시(C1/C4). codex는 `wait_agent` 후 결과 기록을 명시(README Invocation Contract) |
| R4: claude/codex 미러 중 한쪽만 갱신돼 플랫폼 parity 깨짐 | codex pr-review에서 simplicity 미작동 | I2를 V7 전용 대조 검증으로 분리, T2 AC가 5개 계약 항목 1:1 대응을 강제 |
| R5: pr-review version bump가 기존 호출/문서 참조를 깨뜨림 | 진입점 description 트리거는 무변경이라 영향 낮음 | dispatch 추가는 인터페이스 확장이지 트리거(description) 변경이 아니므로 사용자 진입점 무영향. version bump만 동반 |

## Open Questions

### Q1. simplicity 리포트를 별도 경로에 두고 pr-review가 통합 요약만 가질 것인가, 아니면 pr-review 리포트 단일 파일에 흡수할 것인가
- **Decision taken**: simplicity reviewer는 자기 경로(`_sdd/implementation/<date>_simplicity_review_<slug>.md`)에 리포트를 저장하고, pr-review는 그 finding 요약을 자기 리포트(`_sdd/pr/...`)의 Simplicity 섹션에 통합한다(두 파일). 이유: `simplicity-review-agent`의 단일 작성자 불변식(자기 리포트만 write)을 변경 없이 재사용해야 하며, 병렬 dispatch에서 같은 파일에 두 작성자가 쓰면 write race + 불변식 위반. pr-review는 finding 요약을 읽어 통합 + verdict 정책 적용만 한다.
- **Alternatives considered**: (a) pr-review 단일 리포트에 simplicity 섹션을 pr-review가 직접 작성 — simplicity reviewer를 dispatch하지 않고 차원을 자체 복제하는 셈이라 DRY 위반 + 단일 소스 재사용 취지 무력화. 기각. (b) simplicity reviewer가 pr-review 리포트에 직접 append — 단일 작성자 불변식 위반 + 병렬 write race. 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q2. simplicity gating finding(Medium+)이 PR verdict를 자동으로 REQUEST CHANGES로 강제할 것인가, rationale 기여에 그칠 것인가
- **Decision taken**: 자동 강제하지 않고 REQUEST CHANGES rationale에 기여한다. pr-review는 인간 리뷰 보조이며 implementation review-fix loop처럼 자동 수렴 gate가 아니다(`critical=high=medium=0` 합집합 exit 미적용). Medium+ simplicity finding은 verdict 근거로 노출되고 최종 판단은 인간 리뷰어가 한다. 주관(Low)은 Suggested Improvements.
- **Alternatives considered**: (a) Medium+ simplicity finding이 있으면 자동 REQUEST CHANGES — pr-review가 자동 gate가 아니라 인간 보조라는 성격과 충돌. 단순성은 동작-불변 형태라 merge 차단 사유로 강제하면 false-block 위험. 기각. (b) simplicity finding을 verdict와 완전 분리(Suggested Improvements only) — Medium+ falsifiable 위반이 verdict 근거에서 빠져 검출 가치 저하. 기각.
- **Confidence**: MEDIUM
- **User confirmation needed**: Yes (verdict 통합 강도는 pr-review 운영 정책 판단이며 사용자 digest가 "권장: rationale 기여"를 제시했으나 확정 권한은 사용자에 있음). plan은 이 권장안을 C3/T1·T2 AC의 **default + 구현 전 확인 게이트**로 인코딩하며, 확정 결과에 따라 합류 규칙을 조정할 수 있게 둔다 — 통합 강도를 구현 확정으로 굳히지 않는다.

### Q3. pr-review의 simplicity dispatch를 from-branch에 spec이 없는 code-only 모드에서도 항상 실행할 것인가
- **Decision taken**: spec 유무와 무관하게 항상 실행한다. simplicity는 동작-불변 형태 품질이라 from-branch spec 존재 여부와 직교하며, code-only 모드에서도 코드 형태 리뷰 가치가 동일하다. 표적 disjoint 2-렌즈는 spec 유무에 의존하지 않는다.
- **Alternatives considered**: spec 존재 시에만 simplicity dispatch — simplicity가 spec과 무관한 코드 형태 렌즈라 조건부로 둘 근거가 없고, code-only 모드에서 오히려 형태 리뷰가 더 유용. 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No
