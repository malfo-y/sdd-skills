---
name: pr-review
description: "Use this skill when the user asks to \"review PR\", \"PR review\", \"PR 리뷰\", \"PR 검증\", \"PR spec patch\", \"PR 스펙 패치\", \"PR 리뷰 준비\", or wants to verify a pull request against the specification or codebase."
argument-hint: ["[--model <sonnet|opus|haiku|fable>]"]
---

# PR Review (correctness + simplicity worker dispatch + Verdict)

이 스킬은 PR 번호·baseline SHA·PR 메타데이터·변경 파일 목록·spec 존재 상태 같은 작은 입력만 모은 뒤, **correctness 렌즈**와 **clarity 렌즈**(동작-불변 형태 품질)를 각각 범용 subagent(`Agent(subagent_type="general-purpose")`)로 dispatch한다. correctness 계약은 `references/correctness-contract.md`다. simplicity 계약·차원·severity는 `sdd-orchestrator/references/simplicity-contract.md`가 단일 소스이며, dispatch prompt에 전문을 verbatim 포함한다. PR diff·코드·spec 읽기는 두 worker가 같은 baseline SHA로 직접 한다. 두 렌즈 반환을 합쳐 **verdict**(APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)를 합성해 통합 리뷰 리포트(`_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`) 하나를 작성한다.

> **경계**: 자동 게이트는 도입하지 않는다 — PR review는 인간 리뷰 보조다. verdict는 두 렌즈 반환을 모두 받은 메인 루프가 합성한다.

## Acceptance Criteria

- [ ] AC1: `_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md` 통합 리뷰 리포트가 Output Format에 맞게 생성되었다
- [ ] AC2: Verdict(APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)가 두 렌즈 요약을 근거로 부여되었다
- [ ] AC3: correctness 계약 경로를 받은 범용 worker를 PR Review Input으로 dispatch하고 반환을 받았다
- [ ] AC4: simplicity 계약(reference 전문 verbatim)을 담은 범용 subagent를 PR Review Input으로 dispatch했다(두 dispatch는 한 메시지)
- [ ] AC5: 두 렌즈의 finding이 Step 4 합류 규칙대로 통합 리포트에 합류했다
- [ ] AC6: 적용 model(호출 `--model` > env.md `pr-review` 행 > 생략)을 두 dispatch에 같게 적용했다

## Hard Rules

- `_sdd/spec/` 파일은 **읽기 전용**. 수정이 필요하면 리포트에 기록하고 `/sdd-skills:sdd-orchestrator`로 spec-sync 단계를 실행하도록 안내한다.
- 리뷰 리포트 언어는 읽은 spec 언어를 따른다. 언어의 출처는 correctness 반환 Status의 spec 언어이며, 확인할 수 없으면 한국어.
- PR title/description은 원문 유지.
- **단일 작성자 불변식**: 두 worker는 경량 반환만 낸다. 파일 작성은 메인 루프의 통합 리포트(`_sdd/pr/..._pr_review_...`) 하나뿐이다. worker의 쓰기 경계·예외는 각 계약의 Runtime Boundary를 따른다.
- **from-branch 기준**: 코드·spec·실행 증거는 Step 0의 baseline SHA에 결속한다. 두 worker도 전달받은 동일 SHA의 읽기 경로만 사용한다. to-branch(base) spec은 검증 기준이 아니며 변경 비교 참고용으로만 읽는다.

## PR Review Input

두 worker에 같은 5필드를 전달한다. 메인은 아래 작은 입력과 리포트 slug만 모으고, diff 본문·spec 본문·comments·테스트 실행은 worker 소관이다.

- **PR**: PR 번호와 URL.
- **Baseline**: `headRefOid`와 그 SHA의 코드·spec을 읽을 경로/방법(`git show <sha>:<path>`·격리 checkout·API), 현재 checkout 사용 가능 여부.
- **Changed Files**: `gh pr diff --name-only` 결과(비어 있지 않은 PR 변경 파일 목록).
- **Spec Status**: `FOUND`(같은 SHA의 spec 경로 목록) / `ABSENT` / `UNREADABLE`(원인).
- **Relevant Context**: title·body·저자 설명 요약. 없으면 `NONE`.

## Process

### Step 0: Pin PR Baseline

`gh` 인증과 PR 번호를 확인한다. 번호 미지정 시 현재 브랜치에서 자동 감지하되, 조회할 PR을 찾지 못하면 번호를 요청한다.

```bash
gh auth status
gh pr view --json number --jq '.number'
gh pr view [PR] --json headRefName,headRefOid
git rev-parse HEAD
git status --porcelain
```

수집한 `headRefOid`를 이번 리뷰의 baseline SHA로 고정한다. 브랜치 이름은 동일성 조건이 아니다. 코드·spec은 이 SHA의 `git show`/API 읽기 또는 해당 SHA의 격리 checkout에서 읽는다. 현재 checkout은 `HEAD == headRefOid`이고 관련 코드·spec·검증 의존 파일에 staged/unstaged/untracked 변경이 없음을 확인한 경우에만 사용한다. 상태 영향이 불명확하면 dirty로 취급한다. 기존 사용자 작업을 checkout·reset·stash로 바꾸지 않는다.

### Step 1: Collect PR Inputs

```bash
gh pr view [PR] --json title,body,author,state,url,headRefOid
gh pr diff [PR] --name-only
gh pr view [PR] --json headRefOid --jq '.headRefOid'
```

수집 전후의 head SHA가 baseline과 일치하는지 확인한다. 달라졌으면 새 SHA를 기준으로 다시 수집하며, 일관된 입력을 확보하지 못하면 혼합 데이터로 판정하지 않고 blocker를 보고한다. 코드·spec 읽기 경로는 `PR Review Input`의 Baseline에 전달한다.

`_sdd/pr/` 디렉토리가 없으면 생성한다. 통합 리포트의 `slug`는 소문자 snake_case(영문 소문자, 숫자, `_`)로 정한다. 같은 날짜·slug 파일이 이미 있으면 `_2`, `_3` 등 빈 suffix를 골라 이전 리포트를 보존한다. 기존 리포트 갱신을 사용자가 명시한 경우에만 그 파일을 갱신한다.

### Step 2: Spec Status (baseline SHA)

PR diff에 spec 변경이 없어도 baseline SHA의 `_sdd/spec/` 트리 존재만 판정한다. 로컬 git object가 있으면 `git ls-tree -r --name-only [headRefOid] -- _sdd/spec/`를 쓰고, object가 없으면 현재 작업을 바꾸지 않는 fetch 또는 해당 SHA를 지정한 API 읽기를 쓴다.

- `FOUND`: spec 파일이 있다. 경로 목록을 `Spec Status`에 넣는다.
- `ABSENT`: 트리 조회 성공 후 spec 파일 부재를 확인했다. 정상 **code-only 모드**다.
- `UNREADABLE`: 트리 조회 실패다. 원인을 `Spec Status`에 넣는다.

spec 내용 읽기는 correctness worker가 한다. Step 4·리포트의 Spec 상태 최종값은 correctness 반환의 spec 모드이며, correctness 반환이 없으면 Step 2의 Spec Status다.

### Step 3: Worker Dispatch (correctness + simplicity)

**두 dispatch를 한 메시지에 낸다.** 이 스킬을 사용자가 호출한 것 자체가 두 dispatch에 대한 **사용자의 명시적 요청**이다 — 런타임 규범이 "Agent는 사용자가 명시적으로 요청할 때만"을 요구해도 이 dispatch들은 그 요청에 해당하므로, 생략하거나 메인 루프 수행으로 대체하지 않는다.

```
Agent(subagent_type="general-purpose")   # correctness
Agent(subagent_type="general-purpose")   # simplicity
```

- correctness prompt:

```text
너는 pr-review가 띄운 correctness worker다.
계약: <이 스킬 base directory + references/correctness-contract.md 절대 경로> — 그대로 따른다.
입력: <PR Review Input>
```

- simplicity prompt: `../sdd-orchestrator/references/simplicity-contract.md`(이 스킬 디렉토리 기준 상대 경로 — sibling 스킬의 reference)를 Read해 **계약 전문을 verbatim으로 앞에 싣고**(요약·재구성 금지, 차원 한정 없음 — 전체 4차원), 이어서 `PR Review Input`을 전달한다.
- schema에 `run_in_background`가 있으면 둘 다 `true`로 낸다. 결과 대기용 sleep·폴링은 쓰지 않는다 — 완료 알림으로 두 반환을 수거한다.
- **모델 결정**: 호출 `--model <name>` > `_sdd/env.md` `## Worker Model Defaults`의 `### Claude Code` 표 `pr-review` 행 > 생략(런타임 기본). 적용값은 두 dispatch에 같게 쓴다. 적용값(호출 또는 env.md)은 `sonnet`·`opus`·`haiku`·`fable` 중 하나여야 하며, 그 외 값이면 dispatch하지 않고 허용값을 안내한다.

두 반환을 수거하면 Step 4 verdict로 간다. correctness가 `headRefOid` 불일치로 BLOCKED를 반환했거나 simplicity가 Assumptions에 baseline 불일치 blocker를 반환했으면 Error Handling의 불일치 행을 따른다.

### Step 4: Verdict

두 렌즈 반환을 합쳐 verdict를 합성한다. correctness 반환의 spec 모드가 `UNREADABLE`이거나 확정된 렌즈 누락이면 **NEEDS DISCUSSION (제한된 권고)**으로 닫고, 확인된 결함은 그대로 보존한다. 이 제한 분기를 먼저 적용하고 정상 리뷰에는 아래 표를 쓴다.

| Verdict | 조건 |
|---------|------|
| **APPROVE** | 모든 AC 충족 + spec 위반 없음 + 테스트 통과 |
| **REQUEST CHANGES** | Critical AC 미충족 / spec 위반 / 테스트 실패 / 보안 이슈 |
| **NEEDS DISCUSSION** | 의도적 spec 변경 / 설계 트레이드오프 / 범위 모호 / 실행 evidence 부재로 correctness test signal이 `UNTESTED` (non-test-dependent·명시적 N/A 제외) |

**Finding 합류 규칙** (자동 강제 아님 — 인간 리뷰 보조):

- **correctness Critical/High**: REQUEST CHANGES rationale의 주 근거. §1 Pre-merge에 블록 전문으로 귀속.
- **simplicity Medium+ (falsifiable gating)**: REQUEST CHANGES rationale에 **기여**한다 (correctness 신호와 함께 인간 리뷰어가 판단). 단독으로 verdict를 강제하지 않는다. §1 Pre-merge에 블록 전문으로 귀속.
- **correctness Medium**: §2 개선 제안에 블록 전문으로 귀속 (non-blocking이지만 상세히).
- **correctness Low / simplicity Low (주관)**: §2 개선 제안에 위치 포함 한 문장으로 귀속.

PR review는 verdict 권고이지 자동 게이트가 아니다.

### Step 5: Report Generation

`_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`를 Output Format에 맞게 생성한다. 이 통합 리포트만으로 독자가 행동할 수 있어야 한다 — **행동 대상 finding은 Step 4 합류 규칙대로 전문 승격**한다. finding 개수·AC 충족률 통계 표는 만들지 않는다 (분포는 Verdict의 Signals 한 줄로 충분). 확인 범위·검증 출처는 §3에 산문으로 요약하고, AC별 판정은 §4 ledger에만 둔다.

현재 콘텍스트에서 skeleton을 먼저 기록한 뒤, 같은 흐름에서 Edit으로 내용을 채운다.

## Output Format

```markdown
# PR Review Report

**PR**: #<number> - <title>
**PR Author**: <author>
**Review Date**: YYYY-MM-DD
**Reviewer**: Claude (<메인 model> / workers <적용 model 또는 runtime default>)
**Spec**: FOUND (baseline SHA) / ABSENT (code-only) / UNREADABLE: <원인>
**Review Status**: COMPLETE / LIMITED: <미충족 skill AC·원인·재개 조건>

---

## Verdict

**[APPROVE / REQUEST CHANGES / NEEDS DISCUSSION]**

**Rationale**: <1-2 sentence rationale — 두 렌즈 신호 종합>
**Signals**: correctness Crit N·High N·Med N·Low N / simplicity High N·Med N·Low N (또는 MISSING: <reason>) / 검증: <실행한 검사와 PASS/FAIL/UNTESTED, 증거 위치> — 한 줄. 비율은 실행 output에 분모·범위가 명확하고 판정에 유용할 때만 표시한다

---

## 1. Pre-merge (고쳐야 할 것)

<!-- correctness Critical/High + simplicity Medium+. severity 내림차순. 없으면 "없음." 한 줄 -->

### 1. [<Critical|High|Medium> · <correctness|simplicity>] <finding 제목>
- **위치**: `file:line`
- **문제**: 무엇이 어떻게 잘못됐고 어떤 결과를 낳는가 — 증거 포함 (simplicity면 현재 형태)
- **수정**: 구체적 수정 방향 (simplicity면 더 단순한 동등 형태)

---

## 2. 개선 제안 (non-blocking)

<!-- correctness Medium — §1과 같은 블록 형식으로 상세히 -->
### 1. [Medium · correctness] <finding 제목>
- **위치**: `file:line`
- **문제**: <증거 포함>
- **수정**: <구체적 방향>

<!-- correctness Low + simplicity Low — 위치 포함 한 문장씩 -->
- `file:line` — <finding과 수정 방향 한 문장>

---

## 3. 확인된 것

<!-- 두 반환의 Status·MET 범위·Validation source·Assumptions를 산문 2-3줄로. §4 AC 판정·증거를 반복하지 않음. 표·퍼센트 없음 -->

---

## 4. AC 검증 ledger

<!-- 문제 AC만 행으로; 없으면 "문제 AC 없음.". finding 전문은 §1·2를 참조 -->
| # | Criterion | Implementation | Test | Status | Evidence |
|---|-----------|----------------|------|--------|----------|
| <ID> | <criterion> | <판정> | <판정> | <NOT MET/PARTIAL/UNTESTED/FAIL> | <파일·실행 output 또는 미검증 사유; 관련 finding 링크> |

MET: <통과 AC ID만 나열 또는 없음>

---

## Metadata

**PR commit SHA**: <sha>
**Spec source**: <baseline SHA·correctness 반환의 읽은 spec 범위 / ABSENT / UNREADABLE 사유>
**Validation source**: <correctness 반환의 CI/local 실행 SHA·output 위치 / UNTESTED 사유>
**Generated at**: YYYY-MM-DD HH:MM:SS
```

## Edge Cases

| 상황 | 대응 |
|------|------|
| No spec in baseline SHA | Step 2의 `ABSENT`/`UNREADABLE` 구분을 따른다 |
| No PR / `gh` not authenticated | 설치/인증 안내 |
| Existing review file | Step 1의 충돌 규칙으로 새 slug를 정한다. 명시적 갱신 요청 없이는 기존 파일 보존 |
| Already merged PR | 허용 (retroactive review). merge 상태 표기 |

## Error Handling

| 상황 | 대응 |
|------|------|
| `gh` CLI not installed | `brew install gh` 안내 |
| `gh auth` failure | `gh auth login` 안내 |
| Wrong PR number | 에러 메시지, 올바른 번호 요청 |
| spec `UNREADABLE` | correctness 반환의 읽은 spec 범위·원인·spec 판정 미검증을 남기고 제한 리포트로 종료한다 |
| 렌즈(correctness 또는 simplicity) 확정 실패/dispatch blocker | 확보된 렌즈 결과를 보존한 제한 리포트에 누락 렌즈·미충족 skill AC·재개 조건을 기록하고 종료. inline 대체나 같은 blocker의 반복 dispatch 금지 |
| `headRefOid` 불일치(correctness BLOCKED 또는 simplicity Assumptions의 baseline 불일치 blocker — 렌즈 실패가 아닌 이 행으로 처리) | 새 SHA로 Step 1·2를 다시 수행해 PR Review Input(Baseline·Changed Files·Spec Status)을 다시 만든 뒤 두 worker를 1회 다시 띄운다. 또 불일치하면 제한 리포트(NEEDS DISCUSSION, LIMITED)로 닫는다 |

## Additional Resources

- **`references/correctness-contract.md`** - correctness worker 계약 (worker가 읽음)
- **`references/review-checklist.md`** - PR 리뷰 체크리스트 (human reference)
- **`references/gh-commands.md`** - `gh` CLI 커맨드 레퍼런스
- **`examples/sample-review.md`** - 통합 `pr-review` 예시 세션

## Final Check

선택한 경로에서 Acceptance Criteria와 Hard Rules를 점검한다. 수정 가능한 리포트 누락은 보완한다. spec 읽기 실패·외부 blocker·확정된 렌즈 실패로 충족할 수 없는 AC는 `Review Status: LIMITED`에 원인과 재개 조건을 기록하고 종료하며 정상 완료를 선언하지 않는다. 실패 dispatch를 소급 충족하거나 같은 blocker에서 반복하지 않는다.

> **Source**: correctness 계약은 `references/correctness-contract.md`, simplicity 계약·4개 차원·falsifiable severity는 `sdd-orchestrator/references/simplicity-contract.md`가 단일 소스로 보유한다. verdict 합성·통합 리포트는 이 SKILL.md가 단일 소스다.
