---
name: pr-review
description: "Use this skill when the user asks to \"review PR\", \"PR review\", \"PR 리뷰\", \"PR 검증\", \"PR spec patch\", \"PR 스펙 패치\", \"PR 리뷰 준비\", or wants to verify a pull request against the specification or codebase."
version: 2.0.0
---

# PR Review - Unified PR Verification and Verdict

PR의 코드 품질을 검증하고, from-branch에 spec이 있으면 spec 기반 추가 검증을 수행한 뒤, 구조화된 리뷰 리포트(`_sdd/pr/pr_review.md`)를 생성한다.

## Acceptance Criteria

- [ ] AC1: `_sdd/pr/pr_review.md` 리뷰 리포트가 Output Format에 맞게 생성되었다
- [ ] AC2: Verdict(APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)가 근거와 함께 부여되었다
- [ ] AC3: Code-only 검증(코드 품질, 에러 처리, 테스트, 보안)이 항상 수행되었다
- [ ] AC4: from-branch에 spec 존재 시 spec 기반 AC 검증, compliance, gap analysis가 추가 수행되었다
- [ ] AC5: 기존 리뷰 파일이 있으면 `_sdd/pr/prev/`로 아카이브되었다

## Hard Rules

- `_sdd/spec/` 파일은 **읽기 전용**. 수정이 필요하면 리포트에 기록하고 `/spec-update-todo` 사용을 안내한다.
- 리뷰 리포트 언어는 spec 언어를 따른다. Spec 없으면 한국어.
- PR title/description은 원문 유지.

## Process

### Step 0: Branch Check

현재 브랜치가 PR의 from-branch(head)인지 확인한다.

```bash
gh pr view [PR] --json headRefName --jq '.headRefName'
git branch --show-current
```

현재 브랜치 ≠ `headRefName` → 사용자에게 `git checkout [headRefName]` 후 다시 실행하라고 안내하고 **즉시 종료**한다. from-branch에서 실행해야 로컬 spec과 코드가 정확하다.

### Step 1: Collect PR Data

PR 번호 미지정 시 현재 브랜치에서 자동 감지.

```bash
gh auth status
gh pr view --json number --jq '.number'
gh pr view [PR] --json title,body,author,state,url,additions,deletions,changedFiles,headRefName,baseRefName,commits,comments,reviews
gh pr diff [PR]
gh pr diff [PR] --name-only
```

`_sdd/pr/` 디렉토리가 없으면 생성. 기존 `pr_review.md`가 있으면 `_sdd/pr/prev/prev_pr_review_<timestamp>.md`로 아카이브.

### Step 2: Load Spec (from-branch 우선)

from-branch(head)의 spec을 검증 기준으로 사용한다.

1. Step 1에서 수집한 PR metadata에서 `headRefName`, `headRefOid`, `baseRefName`를 확보한다.
2. PR diff에 spec 변경이 없더라도, from-branch 트리에 `_sdd/spec/`가 존재하는지 별도로 확인한다.
3. 우선순위대로 from-branch spec 파일 집합을 찾는다.
   - 현재 checkout이 PR head면 working tree의 `_sdd/spec/`
   - 로컬에 head ref가 있으면 `git ls-tree -r --name-only [headRefName] _sdd/spec`
   - 없으면 `headRefOid` 또는 PR head ref를 fetch한 뒤 동일하게 확인
   - fork PR 등으로 로컬 ref 확인이 어렵다면 `gh api` 또는 동등한 읽기 경로로 PR head의 `_sdd/spec/`를 조회
4. spec 파일이 있으면 `main.md` 또는 명시적 index spec을 baseline으로 읽고, 링크된 하위 spec도 함께 로드한다.
5. from-branch에 spec 파일이 전혀 없을 때만 → **code-only 모드**로 진행한다. (to-branch spec은 검증 기준으로 사용하지 않음)

> to-branch spec은 이전 계약이므로 검증 기준으로 사용하지 않는다. 변경 비교 참고용으로만 읽을 수 있다.

### Step 3: Code-only 검증 (항상 실행)

PR diff와 코드를 기반으로 다음을 검증한다:

| 항목 | 내용 |
|------|------|
| AC 추론 | PR title, body, commit 메시지에서 의도된 변경 사항과 AC를 추론 |
| 코드 품질 | 네이밍, 패턴, 중복, 프로젝트 컨벤션 |
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

### Step 5: Verdict

| Verdict | 조건 |
|---------|------|
| **APPROVE** | 모든 AC 충족 + spec 위반 없음 + 테스트 통과 |
| **REQUEST CHANGES** | Critical AC 미충족 / spec 위반 / 테스트 실패 / 보안 이슈 |
| **NEEDS DISCUSSION** | 의도적 spec 변경 / 설계 트레이드오프 / 범위 모호 |

### Step 6: Report Generation

`_sdd/pr/pr_review.md`를 Output Format에 맞게 생성한다.

현재 콘텍스트에서 skeleton을 먼저 기록한 뒤, 같은 흐름에서 Edit으로 내용을 채운다.

## Output Format

```markdown
# PR Review Report

**PR**: #<number> - <title>
**PR Author**: <author>
**Review Date**: YYYY-MM-DD
**Reviewer**: Codex (<model>)
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

## Recommendations

### Pre-merge Blockers
| Priority | Item | Severity | Action |
|----------|------|----------|--------|

### Suggested Improvements
| Priority | Item | Benefit |
|----------|------|---------|

---

## Next Steps

1. [ ] Take action based on Verdict
2. [ ] (if Approve) After merge, run `/spec-update-todo` if spec updates needed

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
| Multiple spec files in from-branch | `_sdd/spec/main.md` 또는 명시적 index spec 우선. 여전히 모호하고 verdict에 영향이 크면 `request_user_input`으로 짧게 확인, 아니면 canonical index를 선택하고 가정을 기록 |
| Existing review file | `_sdd/pr/prev/`로 아카이브 후 생성 |
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
- **`examples/sample-review.md`** - 통합 `pr-review` 예시 세션

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
