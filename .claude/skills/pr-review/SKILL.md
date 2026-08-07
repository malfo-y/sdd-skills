---
name: pr-review
description: "Use this skill when the user asks to \"review PR\", \"PR review\", \"PR 리뷰\", \"PR 검증\", \"PR spec patch\", \"PR 스펙 패치\", \"PR 리뷰 준비\", or wants to verify a pull request against the specification or codebase."
argument-hint: ["[--model <sonnet|opus|haiku|fable>]"]
---

# PR Review (2-Reviewer Orchestrator + Verdict)

이 스킬은 PR 검증 orchestrator다. PR 데이터·spec을 수집한 뒤 표적이 disjoint한 두 reviewer agent를 **병렬 dispatch**하고, 두 **경량 반환**을 합쳐 **verdict**(APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)를 합성해 통합 리뷰 리포트(`_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`) 하나를 orchestrator가 직접 작성한다.

- `sdd-skills:pr-review-agent` — **correctness** 렌즈 (PR/spec 정합·AC·버그·보안·테스트·정확성-중복)
- `sdd-skills:simplicity-review-agent` — **clarity** 렌즈 (동작-불변 형태 품질: 중복·죽은 코드·단일 사용처 추상화·도달 불가 에러 처리·과잉압축)

전체 리뷰 프로세스·findings-first severity·반환 형식은 각 agent가 단일 소스로 보유한다. 이 orchestrator는 맥락을 모아 전달하고 두 반환을 합쳐 verdict를 합성한다.

> **경계**: 검증·findings 분류는 각 agent의 Process가 수행한다(중복 금지). orchestrator는 PR 데이터/spec 수집 + dispatch + verdict 합성 + 통합 리포트 작성만 소유한다. 자동 게이트는 도입하지 않는다 — PR review는 인간 리뷰 보조다.

## Acceptance Criteria

- [ ] AC1: `_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md` 통합 리뷰 리포트가 Output Format에 맞게 생성되었다
- [ ] AC2: Verdict(APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)가 두 렌즈 요약을 근거로 부여되었다
- [ ] AC3: `pr-review-agent`를 PR 변경 파일 컨텍스트로 dispatch했고, correctness 검증(코드 품질·에러 처리·테스트·보안, spec 존재 시 spec AC·compliance·gap)이 그 반환에서 수행되었다
- [ ] AC4: `simplicity-review-agent`를 같은 PR 변경 파일 컨텍스트로 dispatch했다
- [ ] AC5: 두 agent의 finding이 Step 4 합류 규칙대로 통합 리포트에 합류했다
- [ ] AC6: `--model <name>` 인자가 있으면 두 agent dispatch **모두**에 model을 적용했다

## Hard Rules

- `_sdd/spec/` 파일은 **읽기 전용**. 수정이 필요하면 리포트에 기록하고 `/spec-sync` 사용을 안내한다.
- 리뷰 리포트 언어는 spec 언어를 따른다. Spec 없으면 한국어.
- PR title/description은 원문 유지.
- **단일 작성자 불변식**: 두 reviewer는 파일을 쓰지 않는다(경량 반환). 파일 작성은 orchestrator의 통합 리포트(`_sdd/pr/..._pr_review_...`) 하나뿐이다. 관측 실패: 병렬 reviewer가 report를 쓰면 write race와 불완전한 통합본이 생긴다.

## 병렬 안전성 근거

Hard Rules의 단일 작성자 불변식이 두 reviewer의 동시 dispatch를 안전하게 한다.

## PR Review Input

두 reviewer의 `## Input Data`에는 아래 필드를 이 순서로 전달한다.

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

from-branch(head)의 spec을 검증 기준으로 전달한다.

1. `gh pr diff [PR] --name-only`에서 `_sdd/spec/` 경로 파일 확인
2. 존재하면 `git show origin/[headRefName]:_sdd/spec/main.md`로 from-branch spec 읽기
3. from-branch에 spec 없으면 → **code-only 모드** (spec 컨텍스트 없이 dispatch)

> to-branch spec은 이전 계약이므로 검증 기준으로 사용하지 않는다. 변경 비교 참고용으로만 읽을 수 있다.

### Step 3: Parallel Dispatch (두 렌즈)

> **Model override**: `$ARGUMENTS`에 `--model <name>`이 있으면 아래 두 `Agent(...)` dispatch **모두**에 `model=<name>`을 추가한다. `<name>`은 `sonnet`·`opus`·`haiku`·`fable` 중 하나여야 하며, 그 외 값이면 dispatch하지 않고 사용자에게 허용값을 안내한다. 미지정 시 model을 생략한다(세션 기본값 상속).

**한 메시지에서 두 reviewer를 병렬 dispatch한다.** `sdd-skills:` prefix 필수(plugin 설치 스킬의 agent 호출 규약):

```
Agent(subagent_type="sdd-skills:pr-review-agent")
Agent(subagent_type="sdd-skills:simplicity-review-agent")
```

Step 1·2의 결과로 `PR Review Input`을 채워 두 dispatch message에 동일하게 전달한다. 반환은 각 agent의 source contract 그대로 수거하며, Step 4 verdict와 Step 5 report가 이를 소비한다.

### Step 4: Verdict

두 agent 반환 요약을 합쳐 verdict를 합성한다.

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

`_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`를 Output Format에 맞게 생성한다. 이 통합 리포트만으로 독자가 행동할 수 있어야 한다 — **행동 대상 finding은 Step 4 합류 규칙대로 전문 승격**한다. finding 개수·AC 충족률 통계 표는 만들지 않는다 (분포는 Verdict의 Signals 한 줄로 충분). AC 검증 요지·차원 판정은 §3(확인된 것)에 산문으로 요약한다. 반환에 승격 재료가 빠졌으면 PR 변경 파일을 직접 Read해 보충한다.

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
| No spec in from-branch | Code-only mode. spec 컨텍스트 없이 dispatch |
| No PR / `gh` not authenticated | 설치/인증 안내 |
| Multiple spec files in from-branch | AskUserQuestion으로 선택 후 dispatch에 전달 |
| Existing review file | 날짜+slug로 구분되므로 별도 처리 불필요 |
| Already merged PR | 허용 (retroactive review). merge 상태 표기 |
| Large PR (50+ files) | 각 agent가 디렉토리/컴포넌트 수준 요약으로 축약 (agent Scope에 위임) |

## Error Handling

| 상황 | 대응 |
|------|------|
| `gh` CLI not installed | `brew install gh` 안내 |
| `gh auth` failure | `gh auth login` 안내 |
| Wrong PR number | 에러 메시지, 올바른 번호 요청 |
| from-branch spec 읽기 실패 | code-only mode로 fallback |
| `_sdd/pr/` directory missing | 자동 생성 |
| 한 agent만 반환 실패 | 반환된 렌즈로 통합 리포트를 작성하되 누락 렌즈를 명시하고 재실행을 안내 |

## Additional Resources

- **`references/review-checklist.md`** - PR 리뷰 체크리스트 (human reference)
- **`references/gh-commands.md`** - `gh` CLI 커맨드 레퍼런스
- **`examples/sample-review.md`** - 통합 `pr-review` 예시 세션

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Source**: correctness 계약·프로세스·출력 형식은 `.claude/agents/pr-review-agent.md`가, simplicity 계약·5개 차원·falsifiable severity는 `.claude/agents/simplicity-review-agent.md`가 각각 단일 소스로 보유한다. 이 orchestrator는 PR 데이터/spec 수집 + dispatch + verdict 합성 + 통합 리포트만 소유한다 (orchestrator↔agent; 동일 본문 mirror 아님).
