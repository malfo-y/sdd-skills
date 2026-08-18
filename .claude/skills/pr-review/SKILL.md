---
name: pr-review
description: "Use this skill when the user asks to \"review PR\", \"PR review\", \"PR 리뷰\", \"PR 검증\", \"PR spec patch\", \"PR 스펙 패치\", \"PR 리뷰 준비\", or wants to verify a pull request against the specification or codebase."
argument-hint: ["[--model <sonnet|opus|haiku|fable>]"]
---

# PR Review (직접 correctness + simplicity dispatch + Verdict)

이 스킬은 PR 데이터·spec을 수집한 뒤, **correctness 리뷰를 메인 루프가 직접 수행**하고 **clarity 렌즈만** 범용 subagent(`Agent(subagent_type="general-purpose")`)로 dispatch한다 (동작-불변 형태 품질 — 계약·차원·severity는 `implementation-review` 스킬의 `references/simplicity-contract.md`가 단일 소스이며, dispatch prompt에 전문을 verbatim 포함한다). 두 렌즈 결과를 합쳐 **verdict**(APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)를 합성해 통합 리뷰 리포트(`_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`) 하나를 작성한다.

> **경계**: 자동 게이트는 도입하지 않는다 — PR review는 인간 리뷰 보조다. verdict는 두 렌즈 신호를 모두 쥔 메인 루프가 합성한다.

## Acceptance Criteria

- [ ] AC1: `_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md` 통합 리뷰 리포트가 Output Format에 맞게 생성되었다
- [ ] AC2: Verdict(APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)가 두 렌즈 요약을 근거로 부여되었다
- [ ] AC3: correctness 검증(코드 품질·에러 처리·테스트·보안, spec 존재 시 spec AC·compliance·gap)을 메인 루프가 Correctness 리뷰 절의 절차대로 직접 수행했다
- [ ] AC4: simplicity 계약(reference 전문 verbatim)을 담은 범용 subagent를 PR 변경 파일 컨텍스트(PR Review Input)로 dispatch했다
- [ ] AC5: 두 렌즈의 finding이 Step 4 합류 규칙대로 통합 리포트에 합류했다
- [ ] AC6: `--model <name>` 인자가 있으면 simplicity dispatch에 model을 적용했다 (correctness는 메인 루프 직접 수행이라 적용 대상이 아니다 — 그 사실을 안내)

## Hard Rules

- `_sdd/spec/` 파일은 **읽기 전용**. 수정이 필요하면 리포트에 기록하고 `/spec-sync` 사용을 안내한다.
- 리뷰 리포트 언어는 spec 언어를 따른다. Spec 없으면 한국어.
- PR title/description은 원문 유지.
- **단일 작성자 불변식**: simplicity reviewer는 파일을 쓰지 않는다(경량 반환). 파일 작성은 메인 루프의 통합 리포트(`_sdd/pr/..._pr_review_...`) 하나뿐이다.
- **from-branch 기준**: 검증 기준은 from-branch spec이다. to-branch(base) spec은 검증 기준이 아니며 변경 비교 참고용으로만 읽는다.

## PR Review Input

simplicity reviewer의 `## Input Data`에는 아래 필드를 이 순서로 전달한다 (correctness는 메인 루프가 같은 수집 결과를 직접 소비한다).

- **Changed Files**: 비어 있지 않은 PR 변경 파일 목록
- **PR Diff**: 비어 있지 않은 PR diff
- **PR Metadata**: `title`, `body`, `commits`, `headRefOid`, `headRefName`, `baseRefName` key
- **PR Discussion**: comment/review의 `author` + `body`만 담은 목록, 없으면 `NONE` (approval/verdict state 제외)
- **Spec Context**: from-branch spec bundle 또는 `NONE (code-only)`
- **Validation Evidence**: `CI: <statusCheckRollup summary | NONE>; Local: NOT_RUN`
- **Report Slug**: 비어 있지 않은 소문자 snake_case

## Process

### Step 0: Branch Check

현재 브랜치가 PR의 from-branch(head)인지 확인한다.

```bash
gh pr view [PR] --json headRefName --jq '.headRefName'
git branch --show-current
```

현재 브랜치 ≠ headRefName → 사용자에게 `git checkout [headRefName]` 후 다시 실행하라고 안내하고 **즉시 종료**한다. from-branch에서 실행해야 로컬 spec과 코드가 정확하다.

### Step 1: Collect PR Data

PR 번호 미지정 시 현재 브랜치에서 자동 감지.

```bash
gh auth status
gh pr view --json number --jq '.number'
gh pr view [PR] --json title,body,author,state,url,additions,deletions,changedFiles,headRefName,headRefOid,baseRefName,commits,statusCheckRollup
gh pr view [PR] --json comments,reviews --jq '{comments: [.comments[] | {author: .author.login, body}], reviews: [.reviews[] | {author: .author.login, body}]}'
gh pr diff [PR]
gh pr diff [PR] --name-only
```

`_sdd/pr/` 디렉토리가 없으면 생성. 통합 리포트의 `slug`를 여기서 정한다 (소문자 snake_case — 영문 소문자, 숫자, `_`만).

### Step 2: Load Spec (from-branch 우선)

from-branch(head)의 spec을 검증 기준으로 삼는다.

1. `gh pr diff [PR] --name-only`에서 `_sdd/spec/` 경로 파일 확인
2. 존재하면 `git show origin/[headRefName]:_sdd/spec/main.md`로 from-branch spec 읽기
3. from-branch에 spec 없으면 → **code-only 모드** (spec 컨텍스트 없이 진행)

### Step 3: Simplicity Dispatch + 직접 Correctness

**simplicity dispatch를 먼저 띄운다**:

```
Agent(subagent_type="general-purpose")
```

dispatch prompt는 `../implementation-review/references/simplicity-contract.md`(이 스킬 디렉토리 기준 상대 경로 — sibling 스킬의 reference)를 Read해 **계약 전문을 verbatim으로 앞에 싣고**(요약·재구성 금지, 차원 한정 없음 — 전체 4차원), 이어서 Step 1·2의 결과로 채운 `PR Review Input`을 전달한다. `--model <name>`이 있으면 이 dispatch에 적용한다 — `<name>`은 `sonnet`·`opus`·`haiku`·`fable` 중 하나여야 하며, 그 외 값이면 dispatch하지 않고 허용값을 안내한다.

**agent가 도는 동안 메인 루프가 correctness 리뷰를 직접 수행한다** (아래 Correctness 리뷰). 반환을 수거하면 Step 4 verdict로 간다. 서로 독립인 Read/Grep은 한 메시지에 배칭하고, `Grep`으로 좌표를 먼저 잡은 뒤 관련 구간만 선택적으로 `Read`한다.

## Correctness 리뷰 (메인 루프 직접 수행, 단일 패스)

`Changed Files`로 리뷰 범위를 고정한다. discussion은 저자 해명·기지 이슈·리뷰어 우려의 컨텍스트로만 쓴다. 범위가 큰 PR(50+ files)이면 디렉토리/컴포넌트 수준으로 축약하고 spec 관련 파일에 집중하며 가정을 리포트에 적는다.

**표적 경계**: 형태-중복(추출 가능한 동일 로직 반복) 등 동작-불변 형태 품질은 simplicity 소관이다. 단, 정확성-중복(중복된 보안 검증 누락·일관성 깨진 중복 분기 등 로직 버그성)은 correctness에 잔존한다.

**Review Dimensions** — Code-only 항목은 항상, Spec-based 항목은 from-branch spec이 있을 때만.

| Code-only (항상) | 내용 |
|------|------|
| AC 추론 | PR title, body, commit 메시지 + 기존 PR/review 코멘트에서 의도된 변경 사항·기지 이슈·저자 해명을 반영해 AC를 추론 |
| 코드 품질 | 네이밍, 패턴, 프로젝트 컨벤션 (형태-중복은 simplicity 소관) |
| 에러 처리 | 일관된 응답 형식, 로깅, graceful degradation |
| 테스트 | 새 코드에 대한 테스트 존재 여부, 테스트 통과 여부 (CI 또는 로컬) |
| 보안 | OWASP Top 10, hardcoded secrets, 인증/인가 |
| 성능 | N+1 쿼리, 불필요 I/O, async 블로킹 |
| 문서화 | 새 env vars, API 변경, breaking changes 문서화 여부 |

| Spec-based (spec 존재 시 추가) | 내용 |
|------|------|
| Spec AC 검증 | spec의 각 Feature/Improvement/Bug Fix에 대해 구현 + 테스트 확인. MET(✓) / NOT MET(✗) / PARTIAL(△) |
| Spec Compliance | 기존 spec 요구사항 위반 여부, breaking changes, API contract 변경 |
| Gap Analysis | spec에 있으나 미구현 항목, PR에 있으나 spec에 없는 항목 |

존재/범위 확인에 더해 구현된 코드의 correctness(경계·null·에러 경로·동시성 등 로직 결함)를 능동적으로 검토한다.

**Fresh Verification + 증거 결속**:

1. `Validation Evidence`에 CI 실행 output이 있으면 사용한다.
2. CI 실행 output이 없으면 `_sdd/env.md`가 가리키는 실행 가능한 local validation을 시도한다.
3. 두 경로 모두 실행 evidence가 없으면 test-dependent criterion과 correctness test signal을 사유 포함 `UNTESTED`로 둔다. Non-test-dependent criterion과 명시적 N/A는 제외한다.
4. Code citation만으로 Test/MET를 만들지 않는다. 실패 output은 해당 finding의 severity와 ledger에 결속한다.
- 표적 test/check는 30초가 지나면 중단한다. Timeout 후에는 test target, fixture, 또는 관련 구현이 바뀌기 전까지 같은 명령을 다시 실행하지 않는다.
- 느리다고 알려진 test는 repo 또는 사용자가 명시한 checkpoint에서만 실행한다. checkpoint evidence가 없는 slow 의존 AC는 임의 실행하지 않고 `UNTESTED`(사유: slow — checkpoint 대기)로 보고한다.

**Findings 분류**:

- **Critical**: 핵심 기능 누락, 실패 테스트, 보안 취약점, 데이터 손실 위험, breaking change
- **High**: 핵심 AC 일부 불충족, 주요 에러 처리 갭, 중요한 통합 깨짐, spec 위반
- **Medium**: 비핵심 테스트 누락, 중간 수준 성능/유지보수성 우려, 후속 수정이 필요한 품질 문제
- **Low**: 문서화, 선택적 엣지 케이스, 추후 개선 권고

권고는 검출된 실제 결함 또는 측정된 위험에 직접 대응해야 한다 — "future-proof / extensible / configurable" 같은 사변적 권고 금지.

**AC 검증 ledger**: 문제 있는 verdict(NOT MET·PARTIAL·UNTESTED·FAIL)만 행으로 낸다 — `| # | Criterion | Implementation | Test | Status | Evidence |` (Inferred AC는 항상, Spec AC는 spec-based 모드에서 추가 판정). 통과(MET) AC는 `MET: #1–#N` 꼴 축약 한 줄로 접는다 — 판정은 전 AC 증거 기반으로 수행하되(증거 없는 MET 금지), 통과 증거는 리포트에 전사하지 않는다.

### Step 4: Verdict

두 렌즈 요약을 합쳐 verdict를 합성한다.

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

`_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`를 Output Format에 맞게 생성한다. 이 통합 리포트만으로 독자가 행동할 수 있어야 한다 — **행동 대상 finding은 Step 4 합류 규칙대로 전문 승격**한다. finding 개수·AC 충족률 통계 표는 만들지 않는다 (분포는 Verdict의 Signals 한 줄로 충분). AC 검증 요지·차원 판정은 §3(확인된 것)에 산문으로 요약한다.

현재 콘텍스트에서 skeleton을 먼저 기록한 뒤, 같은 흐름에서 Edit으로 내용을 채운다.

## Output Format

```markdown
# PR Review Report

**PR**: #<number> - <title>
**PR Author**: <author>
**Review Date**: YYYY-MM-DD
**Reviewer**: Claude (<model>)
**Spec**: Found (from-branch) / Not Found (code-only mode)

---

## Verdict

**[APPROVE / REQUEST CHANGES / NEEDS DISCUSSION]**

**Rationale**: <1-2 sentence rationale — 두 렌즈 신호 종합>
**Signals**: correctness Crit N·High N·Med N·Low N / simplicity High N·Med N·Low N / AC MET X of N / test pass F% (또는 UNTESTED: <reason>) — 한 줄, 표 없음

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

<!-- 통과 신호를 산문 2-3줄로: AC 충족 현황과 증거, 테스트 결과, spec compliance. 표·퍼센트 없음 -->

---

## Metadata

**PR commit SHA**: <sha>
**Spec source**: from-branch / none
**Generated at**: YYYY-MM-DD HH:MM:SS
```

## Edge Cases

| 상황 | 대응 |
|------|------|
| No spec in from-branch | Code-only mode. spec 컨텍스트 없이 진행 |
| No PR / `gh` not authenticated | 설치/인증 안내 |
| Multiple spec files in from-branch | AskUserQuestion으로 선택 |
| Existing review file | 날짜+slug로 구분되므로 별도 처리 불필요 |
| Already merged PR | 허용 (retroactive review). merge 상태 표기 |
| Large PR (50+ files) | 디렉토리/컴포넌트 수준 요약으로 축약 (Correctness 리뷰 절·agent Scope) |

## Error Handling

| 상황 | 대응 |
|------|------|
| `gh` CLI not installed | `brew install gh` 안내 |
| `gh auth` failure | `gh auth login` 안내 |
| Wrong PR number | 에러 메시지, 올바른 번호 요청 |
| from-branch spec 읽기 실패 | code-only mode로 fallback |
| simplicity 반환 실패 | correctness 렌즈로 통합 리포트를 작성하되 누락 렌즈를 명시하고 재실행을 안내 |

## Additional Resources

- **`references/review-checklist.md`** - PR 리뷰 체크리스트 (human reference)
- **`references/gh-commands.md`** - `gh` CLI 커맨드 레퍼런스
- **`examples/sample-review.md`** - 통합 `pr-review` 예시 세션

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Source**: simplicity 계약·4개 차원·falsifiable severity는 `implementation-review` 스킬의 `references/simplicity-contract.md`가 단일 소스로 보유한다. correctness 계약·verdict 합성·통합 리포트는 이 SKILL.md가 단일 소스다.
