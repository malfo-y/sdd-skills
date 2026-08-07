# Feature Draft: pr-review boundary and UNTESTED diet

> 규모 판정: 적격 — 기존 공통 입력 6종+validation evidence를 형식화하고 반환·read-only·verdict 중복을 8개 표면의 단일 owner task로 눈검산할 수 있다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
`pr-review`가 두 reviewer에게 전달하는 payload를 기존 공통 입력 6종 + CI/local validation 상태의 고정 7필드 `PR Review Input`으로 형식화한다. wrapper는 agent 반환 형식을 재정의하지 않고 각 agent의 계약을 소비하며, reviewer의 read-only 반환 경계는 한 곳으로 모은다. 실행 evidence가 없어 correctness test signal이 `UNTESTED`이면(non-test-dependent 또는 명시적 N/A 항목 제외) 자동 APPROVE나 실패로 취급하지 않고 `NEEDS DISCUSSION`으로 라우팅한다.

## Scope
- **In**: Claude/Codex `pr-review` wrapper의 input producer·CI 수집/redaction·verdict 경로·반환 경계, 양 reviewer agent의 input consumer/read-only 경계, correctness Fresh Verification/UNTESTED, verdict checklist 포인터, mirror/runtime parity 검증
- **Out**: 두 reviewer topology와 severity 정책 변경, simplicity-review 5차원·return 계약 변경, 통합 PR report schema 변경, 실제 PR review 실행, checklist 외 reference/example 내용 개편
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | `PR Review Input` producer 계약 | `.claude/skills/pr-review/SKILL.md`, `.codex/skills/pr-review/SKILL.md` | `rg -l 'PR metadata\(title/body/commits/SHA\)|PR changed file list' .claude/skills/pr-review/SKILL.md .codex/skills/pr-review/SKILL.md` → 두 wrapper | Task 1 |
| P2 | `PR Review Input` correctness consumer 계약 | `.claude/agents/pr-review-agent.md`, `.codex/agents/pr-review-agent.toml` | `rg -l 'PR metadata\(title/body/commits/SHA\)|PR 변경 파일 목록' .claude/agents/pr-review-agent.md .codex/agents/pr-review-agent.toml` → correctness agent 두 미러 | Task 2 |
| P3 | `PR Review Input` simplicity consumer 계약 | `.claude/agents/simplicity-review-agent.md`, `.codex/agents/simplicity-review-agent.toml` | `rg -l '호출자 지정 경로/범위' .claude/agents/simplicity-review-agent.md .codex/agents/simplicity-review-agent.toml` → simplicity agent 두 미러 | Task 3 |
| P4 | 반환 재정의 제거 + UNTESTED verdict 경로 | `.claude/skills/pr-review/SKILL.md`, `.codex/skills/pr-review/SKILL.md` | `rg -l '각 agent는 \*\*경량 반환|test pass F% \(또는 UNTESTED\)' .claude/skills/pr-review .codex/skills/pr-review` → wrapper 두 파일 | Task 1 |
| P5 | verdict criteria 단일 홈 | `.claude/skills/pr-review/references/review-checklist.md`, `.codex/skills/pr-review/references/review-checklist.md` | `rg -l '^## Verdict Criteria$|All tests pass|^### NEEDS DISCUSSION$' .claude/skills/pr-review .codex/skills/pr-review` → wrapper 2 + checklist 2; checklist는 pointer로 전환 | Task 1 |
| P6 | correctness read-only/Fresh Verification 단일 홈 | `.claude/agents/pr-review-agent.md`, `.codex/agents/pr-review-agent.toml` | `rg -l 'read-only reviewer|파일을 생성하지 않았다|어떤 파일도 생성/수정/삭제|Fresh Verification' .claude/agents/pr-review-agent.md .codex/agents/pr-review-agent.toml` → correctness agent 두 미러 | Task 2 |

# Part 2: Tasks

### Task 1: wrapper 입력·verdict 경계를 얇게 만든다
두 wrapper에서 공통 dispatch payload를 필드 계약으로 고정하고, agent 반환의 상세 형식 나열은 agent source pointer로 대체한다. 통합 report `Output Format`과 verdict/finding 합류 정책은 wrapper 소유이므로 보존한다.

**Contracts**: 두 reviewer의 `## Input Data`에는 `## PR Review Input` 아래 `Changed Files`, `PR Diff`, `PR Metadata`, `PR Discussion`, `Spec Context`, `Validation Evidence`, `Report Slug` 일곱 필드가 이 순서로 정확히 한 번씩 있다. `PR Metadata`는 title/body/commits/`headRefOid`/head ref/base ref key를 갖는다. `PR Discussion`은 author+body만 보존하고 review approval/verdict state는 제거하며, 없으면 `NONE`이다. `Spec Context`는 from-branch bundle 또는 `NONE (code-only)`, `Validation Evidence`는 CI `statusCheckRollup` 요약 + local `NOT_RUN` 초기값(없으면 CI `NONE`), slug는 비어 있지 않다. 실행 evidence 부재로 correctness test signal이 `UNTESTED`이면(non-test-dependent/명시적 N/A 제외) verdict는 `NEEDS DISCUSSION`이다.

**Acceptance Criteria**:
- [ ] AC1: 두 wrapper에 `## PR Review Input` heading 1건과 다음 `## ` heading 전까지 일곱 exact field prefix가 고정 순서·각 1건이다. metadata subkeys, discussion redaction, spec/CI `NONE`, local `NOT_RUN` 조건도 같은 block에 있다.
- [ ] AC2: Step 3은 두 reviewer에게 같은 `PR Review Input`을 전달하고 각 agent의 반환 계약을 그대로 수거한다고만 명시한다. correctness/simplicity 반환 필드·finding 블록 구조를 wrapper가 다시 나열한 현행 두 bullet은 없다.
- [ ] AC3: Step 1이 `headRefOid`·`statusCheckRollup`을 수집하고, discussion용 별도 query/transform은 comments/reviews에서 author+body만 남겨 state를 제거한다. 그 결과를 일곱 필드에 연결한다.
- [ ] AC4: Verdict 표의 `NEEDS DISCUSSION` 조건은 correctness test signal `UNTESTED`로 닫히고 non-test-dependent/명시적 N/A 예외를 적는다. `Signals`의 `UNTESTED` 사유, 테스트 실패=`REQUEST CHANGES`, evidence 있는 통과=`APPROVE`를 보존한다.
- [ ] AC5: read-only 병렬 안전성은 single-writer Hard Rule을 근거로 한 절 한 곳에서만 설명한다. intro·Step 3은 안전 조건을 재서술하지 않으며 two-reviewer parallel dispatch와 Claude/Codex runtime adapter는 보존된다.
- [ ] AC6: checklist 두 미러의 `Verdict Criteria` 복제 표는 제거되고 각 runtime wrapper의 Step 4를 canonical으로 가리킨다.
- [ ] AC7: 통합 report `Output Format`, finding 합류 규칙, model override, from-branch spec 우선, agent failure fallback의 보호 anchor(`## Output Format`, `Finding 합류 규칙`, Claude `Model override`/Codex `Subagent model override`, `### Step 2: Load Spec`, `한 agent만 반환 실패`)가 HEAD와 동일하게 존재한다.

**Target Files**:
- [M] `.claude/skills/pr-review/SKILL.md` -- Claude input producer·UNTESTED verdict·wrapper diet
- [M] `.codex/skills/pr-review/SKILL.md` -- Codex runtime adapter를 보존한 동형 변경
- [M] `.claude/skills/pr-review/references/review-checklist.md` -- verdict 복제 표를 Claude wrapper 포인터로 교체
- [M] `.codex/skills/pr-review/references/review-checklist.md` -- verdict 복제 표를 Codex wrapper 포인터로 교체

### Task 2: correctness agent의 소비·검증·read-only 경계를 단일화한다
두 agent에서 같은 input 필드를 consumer 계약으로 받고, validation source의 유무에 따라 test signal을 evidence-backed status로 결정한다. 파일 비작성은 Hard Rule 1을 canonical home으로 두고 나머지는 포인터로 줄인다.

**Contracts**: `PR Review Input` 일곱 필드는 wrapper와 동일하다. Fresh Verification은 (1) `Validation Evidence`의 CI output, (2) `_sdd/env.md`가 가리키는 실행 가능한 local validation 순으로 사용한다. 어느 쪽에도 실행 evidence가 없으면 test-dependent ledger status와 correctness signal은 사유를 붙인 `UNTESTED`이며, non-test-dependent/명시적 N/A criterion은 이 signal에서 제외한다. code citation만으로 Test/MET를 만들지 않는다. file write 금지는 Hard Rule 1이 단일 홈이다.

**Acceptance Criteria**:
- [ ] AC8: 두 correctness agent의 `PR Review Input` block이 wrapper와 동일한 일곱 exact field prefix·순서·subschema를 가진다. Step 1은 이 block을 소비해 scope/mode를 정하며 입력 목록을 재서술하지 않는다.
- [ ] AC9: Fresh Verification은 `_sdd/env.md` 존재 자체가 아니라 실제 CI/local 실행 evidence 유무로 판정한다. evidence가 없으면 test-dependent status와 correctness signal을 사유 포함 `UNTESTED`로 두고, non-test/N/A 제외와 실패 evidence 경로를 보존한다.
- [ ] AC10: read-only/no-report 계약의 구체 정의는 Hard Rule 1에만 있다. intro는 “최종 응답 반환 reviewer”, AC4는 Hard Rule 1 준수 포인터, Process/Source Pointer는 소유 관계만 말하며 파일 비작성 금지를 재서술하지 않는다.
- [ ] AC11: 보호 anchor `## Review Dimensions`, `## Findings Classification`, `### Step 4: Return`, `## Final Check`가 HEAD와 동일하게 존재하고, correctness/simplicity 표적 disjoint·verdict 미판정·from-branch 의미가 보존된다.
- [ ] AC12: Claude/Codex correctness agent core는 Codex `Agent Boundary`와 TOML wrapper/source 문구만 제외해 exact match하고 Codex TOML이 parse된다.

**Target Files**:
- [M] `.claude/agents/pr-review-agent.md` -- input consumer·UNTESTED evidence 기준·read-only 단일 홈
- [M] `.codex/agents/pr-review-agent.toml` -- 같은 의미의 Codex agent 미러

### Task 3: simplicity reviewer가 공통 input 계약을 소비하게 한다
두 simplicity agent에 공통 payload consumer block만 추가하고 기존 scope priority와 5차원·return 계약은 바꾸지 않는다.

**Contracts**: `PR Review Input` 일곱 필드는 wrapper와 동일하다. simplicity는 `Changed Files`와 `PR Diff`로 범위를 고정하고 나머지를 PR 맥락으로만 사용하며 validation status를 correctness처럼 재판정하지 않는다.

**Acceptance Criteria**:
- [ ] AC13: 두 simplicity agent의 `PR Review Input` block에 동일한 일곱 exact field prefix·순서·subschema가 있고 Step 1은 해당 block의 Changed Files/PR Diff를 우선 소비한다.
- [ ] AC14: 5개 차원, 호출자 차원 한정, falsifiability, severity, return, Final Check의 보호 anchor와 의미는 HEAD와 동일하고 runtime 전용부 제외 core parity·TOML parse가 PASS다.

**Target Files**:
- [M] `.claude/agents/simplicity-review-agent.md` -- PR 공통 payload 최소 consumer 계약
- [M] `.codex/agents/simplicity-review-agent.toml` -- 같은 의미의 Codex consumer 미러

### Task 4: 전파·잔존 중복·runtime parity를 read-only 검증한다
8개 표면에서 input interface·verdict pointer 전파와 삭제 대상 재서술의 잔존 0건을 구현 task와 분리해 확인한다.

**Acceptance Criteria**:
- [ ] AC15: section-aware extractor가 wrapper 2 + reviewer agent 4에서 `PR Review Input` heading 1·일곱 field prefix 고정 순서·각 1을 assert한다. `rg -l '^## PR Review Input$' <6 target>` 집합도 정확히 일치한다.
- [ ] AC16: checklist 두 미러의 `Verdict Criteria` section이 wrapper Step 4 포인터 1문장만 갖고 복제 anchor(`^### APPROVE$`, `^### REQUEST CHANGES$`, `^### NEEDS DISCUSSION$`, exact verdict-list `All tests pass`)는 그 section 안 0건이다.
- [ ] AC17: wrapper agent-return 재정의 bullet 0, correctness agent Hard Rule 1 밖 file-write 금지 구문 0, `UNTESTED` agent→wrapper verdict 경로 양 mirror 존재, 보호 anchor census, agent core parity, TOML 2개 parse, `git diff --check`가 모두 PASS다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- 사용자 확인 불필요(확신도 높음): 대안은 correctness payload만 형식화해 simplicity agent를 그대로 두는 것이나, 두 reviewer가 동일 message를 받는 현행 dispatch와 제작 규범 §3.4에 어긋나 기각했다. simplicity agent에는 공통 7필드 consumer만 추가하고 새 validation 판정 의무는 주지 않는다.
