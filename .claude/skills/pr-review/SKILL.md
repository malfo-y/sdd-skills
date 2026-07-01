---
name: pr-review
description: "Use this skill when the user asks to \"review PR\", \"PR review\", \"PR 리뷰\", \"PR 검증\", \"PR spec patch\", \"PR 스펙 패치\", \"PR 리뷰 준비\", or wants to verify a pull request against the specification or codebase."
version: 3.1.0
argument-hint: ["[--model <sonnet|opus|haiku|fable>]"]
---

# PR Review - Unified PR Verification and Verdict

PR의 코드 품질을 검증하고, from-branch에 spec이 있으면 spec 기반 추가 검증을 수행한 뒤, 구조화된 리뷰 리포트(`_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`)를 생성한다.

## Acceptance Criteria

- [ ] AC1: `_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md` 리뷰 리포트가 Output Format에 맞게 생성되었다
- [ ] AC2: Verdict(APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)가 근거와 함께 부여되었다
- [ ] AC3: Code-only 검증(코드 품질, 에러 처리, 테스트, 보안)이 항상 수행되었다
- [ ] AC4: from-branch에 spec 존재 시 spec 기반 AC 검증, compliance, gap analysis가 추가 수행되었다
- [ ] AC5: `simplicity-review-agent`를 PR 변경 파일 컨텍스트로 dispatch했고, 그 finding이 verdict 정책(Medium+ → rationale 기여, Low → Suggested Improvements, 자동 강제 없음)대로 리포트에 합류했다
## Hard Rules

- `_sdd/spec/` 파일은 **읽기 전용**. 수정이 필요하면 리포트에 기록하고 `/spec-sync` 사용을 안내한다.
- 리뷰 리포트 언어는 spec 언어를 따른다. Spec 없으면 한국어.
- PR title/description은 원문 유지.
- **Subagent Model Override**: `$ARGUMENTS`에 `--model <name>`이 있으면 `simplicity-review-agent` dispatch에 `model=<name>`을 추가한다. `<name>`은 `sonnet`·`opus`·`haiku`·`fable` 중 하나여야 하며, 그 외 값이면 dispatch하지 않고 사용자에게 허용값을 안내한다. 미지정 시 model을 생략한다(세션 기본값 상속).

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
gh pr view [PR] --json title,body,author,state,url,additions,deletions,changedFiles,headRefName,baseRefName,commits,comments,reviews
gh pr diff [PR]
gh pr diff [PR] --name-only
```

`_sdd/pr/` 디렉토리가 없으면 생성.

### Step 2: Load Spec (from-branch 우선)

from-branch(head)의 spec을 검증 기준으로 사용한다.

1. `gh pr diff [PR] --name-only`에서 `_sdd/spec/` 경로 파일 확인
2. 존재하면 `git show origin/[headRefName]:_sdd/spec/main.md`로 from-branch spec 읽기
3. from-branch에 spec 없으면 → **code-only 모드**로 진행 (to-branch spec은 사용하지 않음)

> to-branch spec은 이전 계약이므로 검증 기준으로 사용하지 않는다. 변경 비교 참고용으로만 읽을 수 있다.

### Step 3: Code-only 검증 (항상 실행)

PR diff와 코드를 기반으로 다음을 검증한다:

| 항목 | 내용 |
|------|------|
| AC 추론 | PR title, body, commit 메시지에서 의도된 변경 사항과 AC를 추론 |
| 코드 품질 | 네이밍, 패턴, 프로젝트 컨벤션 (중복 경계는 Step 4.5 참조) |
| 에러 처리 | 일관된 응답 형식, 로깅, graceful degradation |
| 테스트 | 새 코드에 대한 테스트 존재 여부, 테스트 통과 여부 (CI 또는 로컬) |
| 보안 | OWASP Top 10, hardcoded secrets, 인증/인가 |
| 성능 | N+1 쿼리, 불필요 I/O, async 블로킹 |
| 문서화 | 새 env vars, API 변경, breaking changes 문서화 여부 |

`_sdd/env.md` 존재 시 환경 설정을 적용하여 로컬 테스트를 실행한다.

### Step 4: Spec-based 검증 (from-branch spec 존재 시 추가)

Step 3 위에 다음을 추가 수행:

| 항목 | 내용 |
|------|------|
| AC 검증 | spec의 각 Feature/Improvement/Bug Fix에 대해 구현 + 테스트 확인. MET(✓) / NOT MET(✗) / PARTIAL(△) |
| Spec Compliance | 기존 spec 요구사항 위반 여부, breaking changes, API contract 변경 |
| Gap Analysis | spec에 있으나 미구현 항목, PR에 있으나 spec에 없는 항목 |

### Step 4.5: Simplicity Dispatch (병렬 레인)

PR 변경 파일을 **동작-불변 형태 품질** 렌즈로 리뷰하기 위해 `simplicity-review-agent`를 dispatch한다. 이 레인은 pr-review의 correctness 자체 검증(Step 3~4)과 **동시 진행해도 안전하다**: `simplicity-review-agent`는 `Read/Glob/Grep`만 쓰는 read-only leaf라 코드·리포트를 변경하지 않고 자기 리포트만 write하므로 자체 검증과 경합하지 않는다.

**중복 경계** — 형태-중복(동작 불변·추출 가능한 동일 로직 반복)은 이 simplicity 레인에 위임한다. 정확성-중복(중복된 보안 검증 누락·일관성 깨진 중복 분기 등 로직 버그성)은 Step 3의 correctness 자체 검증에 잔존한다.

canonical dispatch 표현(`sdd-skills:` prefix 필수 — `.claude/skills/implementation/SKILL.md`와 정합):

```
Agent(subagent_type="sdd-skills:simplicity-review-agent")
```

dispatch message에 다음을 전달한다:

- Step 1에서 수집한 `gh pr diff [PR] --name-only` **변경 파일 목록**을 리뷰 대상 경로로 명시 전달한다. 이는 agent Step 1 Scope의 "사용자 경로" 입력으로 진입해 리뷰 범위를 PR 변경분으로 **고정**한다 (glob/legacy fallback 회피).
- from-branch spec이 있으면 그 spec 컨텍스트를 함께 전달한다 (code-only mode면 생략).

`simplicity-review-agent`는 자기 경로 `_sdd/implementation/<YYYY-MM-DD>_simplicity_review_<slug>.md`에 리포트를 저장하고, severity별 finding 요약(High/Medium gating/Low advisory)을 반환한다. pr-review는 그 요약을 받아 Verdict(Step 5)와 Output Format Simplicity 섹션에 통합한다. **simplicity 리포트는 agent가 자기 경로에 write하며, pr-review는 자기 리포트(`_sdd/pr/...`)에만 통합 요약을 write한다 — 단일 작성자 불변식을 유지한다.**

### Step 5: Verdict

| Verdict | 조건 |
|---------|------|
| **APPROVE** | 모든 AC 충족 + spec 위반 없음 + 테스트 통과 |
| **REQUEST CHANGES** | Critical AC 미충족 / spec 위반 / 테스트 실패 / 보안 이슈 |
| **NEEDS DISCUSSION** | 의도적 spec 변경 / 설계 트레이드오프 / 범위 모호 |

**Simplicity finding 합류 규칙**: simplicity reviewer의 finding은 verdict를 자동 강제하지 않는다 (인간 리뷰 보조).

- **Medium+ (falsifiable gating finding)**: REQUEST CHANGES **rationale에 기여**한다 (다른 correctness 신호와 함께 인간 리뷰어가 판단). 단독으로 verdict를 강제하지 않는다.
- **Low (주관)**: Suggested Improvements에 귀속한다.

implementation gate의 `critical=high=medium=0` 합집합 자동 exit는 **PR review에 적용하지 않는다** — PR review는 verdict 권고이지 자동 게이트가 아니다.

### Step 6: Report Generation

`_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`를 Output Format에 맞게 생성한다. `slug`는 소문자 snake_case (영문 소문자, 숫자, `_`만 사용).

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

**Rationale**: <1-2 sentence rationale>
**Key Findings**:
- <finding 1>
- <finding 2>

---

## Metrics Summary

| Item | Count |
|------|-------|
| Acceptance criteria | N (inferred) or N (from spec) |
| Met (✓) | X (Y%) |
| Not met (✗) | A (B%) |
| Partially met (△) | C (D%) |
| Spec violations | E |
| Test pass rate | F% |

---

## Code-only Verification

### Inferred Acceptance Criteria
| # | Criterion (from PR description) | Implementation | Test | Status | Notes |
|---|--------------------------------|----------------|------|--------|-------|

### Code Quality
[findings]

### Security & Performance
[findings]

---

## Spec-based Verification
<!-- 이 섹션은 from-branch에 spec이 있을 때만 포함 -->

### Spec AC Verification
| # | Acceptance Criterion (from spec) | Implementation | Test | Status | Notes |
|---|----------------------------------|----------------|------|--------|-------|

### Spec Compliance
[violations or "None"]

### Gap Analysis
#### In spec but not in PR
#### In PR but not in spec

---

## Simplicity
<!-- simplicity-review-agent finding 통합 요약. 상세는 리포트 참조 -->
**Report**: `_sdd/implementation/<YYYY-MM-DD>_simplicity_review_<slug>.md`

| Severity | Count | Findings (요약) |
|----------|-------|-----------------|
| High | N | |
| Medium (gating) | N | |
| Low (advisory) | N | |

> Medium+ finding은 REQUEST CHANGES rationale에 기여(자동 강제 아님), Low는 Suggested Improvements에 귀속.

---

## Recommendations

### Pre-merge Blockers
<!-- correctness blocker + simplicity Medium+ finding(rationale 기여) -->
| Priority | Item | Severity | Action |
|----------|------|----------|--------|

### Suggested Improvements
<!-- correctness 권고 + simplicity Low finding -->
| Priority | Item | Benefit |
|----------|------|---------|

---

## Next Steps

1. [ ] Take action based on Verdict
2. [ ] (if Approve) After merge, run `/spec-sync` if spec updates needed

---

## Metadata

**Review version**: <count>
**PR commit SHA**: <sha>
**Spec source**: from-branch / none
**Generated at**: YYYY-MM-DD HH:MM:SS
```

## Edge Cases

| 상황 | 대응 |
|------|------|
| No spec in from-branch | Code-only mode. to-branch spec은 사용하지 않음 |
| No PR / `gh` not authenticated | 설치/인증 안내 |
| Multiple spec files in from-branch | AskUserQuestion으로 선택 |
| Existing review file | 날짜+slug로 구분되므로 별도 처리 불필요 |
| Already merged PR | 허용 (retroactive review). merge 상태 표기 |
| Large PR (50+ files) | 디렉토리/컴포넌트 수준 요약, spec 관련 파일 집중 |

## Error Handling

| 상황 | 대응 |
|------|------|
| `gh` CLI not installed | `brew install gh` 안내 |
| `gh auth` failure | `gh auth login` 안내 |
| Wrong PR number | 에러 메시지, 올바른 번호 요청 |
| from-branch spec 읽기 실패 | code-only mode로 fallback |
| `_sdd/pr/` directory missing | 자동 생성 |

## Additional Resources

- **`references/review-checklist.md`** - PR 리뷰 체크리스트
- **`references/gh-commands.md`** - `gh` CLI 커맨드 레퍼런스

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
