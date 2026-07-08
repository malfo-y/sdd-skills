---
name: pr-review
description: "Use this skill when the user asks to \"review PR\", \"PR review\", \"PR 리뷰\", \"PR 검증\", \"PR spec patch\", \"PR 스펙 패치\", \"PR 리뷰 준비\", or wants to verify a pull request against the specification or codebase."
version: 3.2.1
argument-hint: ["[--model <sonnet|opus|haiku|fable>]"]
---

# PR Review (2-Reviewer Orchestrator + Verdict)

이 스킬은 PR 검증 orchestrator다. PR 데이터·spec을 수집한 뒤 표적이 disjoint한 두 read-only reviewer agent를 **병렬 dispatch**하고, 두 리포트 요약을 합쳐 **verdict**(APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)를 합성해 통합 리뷰 리포트(`_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`)를 생성한다.

- `sdd-skills:pr-review-agent` — **correctness** 렌즈 (PR/spec 정합·AC·버그·보안·테스트·정확성-중복)
- `sdd-skills:simplicity-review-agent` — **clarity** 렌즈 (동작-불변 형태 품질: 중복·죽은 코드·단일 사용처 추상화·도달 불가 에러 처리·과잉압축)

전체 리뷰 프로세스·findings-first severity·리포트 형식은 각 agent가 단일 소스로 보유한다. 이 orchestrator는 맥락을 모아 전달하고 두 리포트를 합쳐 verdict를 합성한다.

> **경계**: 검증·findings 분류·detail 리포트 작성은 각 agent의 Process가 수행한다(중복 금지). orchestrator는 PR 데이터/spec 수집 + dispatch + verdict 합성 + 통합 리포트 작성만 소유한다. implementation gate의 fix → re-review loop나 합집합 자동 exit는 도입하지 않는다 — PR review는 인간 리뷰 보조다.

## Acceptance Criteria

- [ ] AC1: `_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md` 통합 리뷰 리포트가 Output Format에 맞게 생성되었다
- [ ] AC2: Verdict(APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)가 두 렌즈 요약을 근거로 부여되었다
- [ ] AC3: `pr-review-agent`를 PR 변경 파일 컨텍스트로 dispatch했고, correctness 검증(코드 품질·에러 처리·테스트·보안, spec 존재 시 spec AC·compliance·gap)이 그 리포트에서 수행되었다
- [ ] AC4: `simplicity-review-agent`를 같은 PR 변경 파일 컨텍스트로 dispatch했다
- [ ] AC5: 두 agent의 finding이 verdict 정책(correctness Critical/High → blocker, simplicity Medium+ → rationale 기여, Low → Suggested Improvements, 자동 강제 없음)대로 통합 리포트에 합류했다
- [ ] AC6: `--model <name>` 인자가 있으면 두 agent dispatch **모두**에 model을 적용했다

## Hard Rules

- `_sdd/spec/` 파일은 **읽기 전용**. 수정이 필요하면 리포트에 기록하고 `/spec-sync` 사용을 안내한다.
- 리뷰 리포트 언어는 spec 언어를 따른다. Spec 없으면 한국어.
- PR title/description은 원문 유지.
- **단일 작성자 불변식**: 두 reviewer는 각자 자기 리포트(`_sdd/pr/..._pr_correctness_...` / `_sdd/implementation/..._simplicity_review_...`)만 write하고, orchestrator는 통합 리포트(`_sdd/pr/..._pr_review_...`)만 write한다.

## 병렬 안전성 근거

두 reviewer는 sub-agent를 spawn하지 않는 leaf이고 **입력 코드·spec를 수정하지 않는다** — 각자 자기 리포트만 쓴다. correctness reviewer는 테스트 실행을 위해 `Bash`를, 두 reviewer 모두 자기 리포트 저장을 위해 `Write`를 갖지만(`pr-review-agent`: `["Read","Write","Glob","Grep","Bash"]`, `simplicity-review-agent`: `["Read","Write","Glob","Grep"]`), 그 write 대상은 각자의 리포트뿐이고 **서로 다른 경로**(`*_pr_correctness_*` vs `*_simplicity_review_*`)라 충돌이 없다. 따라서 한 메시지에서 동시 dispatch해도 안전하다.

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

`_sdd/pr/` 디렉토리가 없으면 생성. 세 리포트가 공유할 `slug`를 여기서 정한다 (소문자 snake_case — 영문 소문자, 숫자, `_`만). 이 slug를 두 agent와 통합 리포트에 모두 전달해 `_pr_correctness_<slug>` / `_simplicity_review_<slug>` / `_pr_review_<slug>`가 정렬되게 한다.

### Step 2: Load Spec (from-branch 우선)

from-branch(head)의 spec을 검증 기준으로 전달한다.

1. `gh pr diff [PR] --name-only`에서 `_sdd/spec/` 경로 파일 확인
2. 존재하면 `git show origin/[headRefName]:_sdd/spec/main.md`로 from-branch spec 읽기
3. from-branch에 spec 없으면 → **code-only 모드** (spec 컨텍스트 없이 dispatch)

> to-branch spec은 이전 계약이므로 검증 기준으로 사용하지 않는다. 변경 비교 참고용으로만 읽을 수 있다.

### Step 3: Parallel Dispatch (두 렌즈)

> **Model override**: `$ARGUMENTS`에 `--model <name>`이 있으면 아래 두 `Agent(...)` dispatch **모두**에 `model=<name>`을 추가한다. `<name>`은 `sonnet`·`opus`·`haiku`·`fable` 중 하나여야 하며, 그 외 값이면 dispatch하지 않고 사용자에게 허용값을 안내한다. 미지정 시 model을 생략한다(세션 기본값 상속).

**한 메시지에서 두 reviewer를 병렬 dispatch한다** (read-only leaf라 동시 실행 안전 — 위 근거). `sdd-skills:` prefix 필수(`.claude/skills/implementation/SKILL.md`와 정합):

```
Agent(subagent_type="sdd-skills:pr-review-agent")
Agent(subagent_type="sdd-skills:simplicity-review-agent")
```

두 dispatch message에 공통으로 다음을 전달한다:

- Step 1에서 수집한 `gh pr diff [PR] --name-only` **변경 파일 목록**을 리뷰 대상 경로로 명시 전달한다. 이는 각 agent의 Scope 입력으로 진입해 리뷰 범위를 PR 변경분으로 **고정**한다 (glob/legacy fallback 회피).
- PR metadata(title/body/commits/SHA)와 `gh pr diff [PR]` 본문.
- **PR 코멘트·review 코멘트(디스커션 내용)** — Step 1에서 `gh pr view ... comments,reviews`로 수집한 것을 두 agent 모두에 전달한다. 저자 해명·기지(旣知) 이슈·리뷰어 우려가 리뷰 컨텍스트가 된다. review 승인/verdict **상태 자체는 전달하지 않는다** (리뷰어는 verdict를 독립 판정한다).
- Step 2의 from-branch spec 컨텍스트 (code-only 모드면 생략).
- Step 1에서 정한 공유 `slug`.

각 agent는 자기 경로에 findings-first 리포트를 저장하고 요약을 반환한다:
- `pr-review-agent` → `_sdd/pr/<YYYY-MM-DD>_pr_correctness_<slug>.md` + correctness 신호(AC 충족 현황·spec 위반·test pass rate·blocker findings). **verdict는 내지 않는다.**
- `simplicity-review-agent` → `_sdd/implementation/<YYYY-MM-DD>_simplicity_review_<slug>.md` + severity별 finding 요약(High/Medium gating/Low advisory).

### Step 4: Verdict

두 agent 반환 요약을 합쳐 verdict를 합성한다.

| Verdict | 조건 |
|---------|------|
| **APPROVE** | 모든 AC 충족 + spec 위반 없음 + 테스트 통과 |
| **REQUEST CHANGES** | Critical AC 미충족 / spec 위반 / 테스트 실패 / 보안 이슈 |
| **NEEDS DISCUSSION** | 의도적 spec 변경 / 설계 트레이드오프 / 범위 모호 |

**Finding 합류 규칙** (자동 강제 아님 — 인간 리뷰 보조):

- **correctness Critical/High**: REQUEST CHANGES rationale의 주 근거. Pre-merge Blockers에 귀속.
- **simplicity Medium+ (falsifiable gating)**: REQUEST CHANGES rationale에 **기여**한다 (correctness 신호와 함께 인간 리뷰어가 판단). 단독으로 verdict를 강제하지 않는다.
- **simplicity Low (주관) / correctness 권고**: Suggested Improvements에 귀속.

implementation gate의 `critical=high=medium=0` 합집합 자동 exit는 **PR review에 적용하지 않는다** — PR review는 verdict 권고이지 자동 게이트가 아니다.

### Step 5: Report Generation

`_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`를 Output Format에 맞게 생성한다. 이 통합 리포트는 verdict + 두 렌즈 **요약** + 두 detail 리포트 **경로 참조**를 담는다 (correctness/simplicity detail은 각 agent 리포트에 있으므로 여기서는 재작성하지 않는다).

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
| Correctness findings (Crit/High/Med/Low) | .. |
| Simplicity findings (High/Med/Low) | .. |

---

## Correctness (pr-review-agent)
<!-- pr-review-agent 리포트 통합 요약. 상세는 리포트 참조 -->
**Report**: `_sdd/pr/<YYYY-MM-DD>_pr_correctness_<slug>.md`
**Mode**: code-only / spec-based

| Severity | Count | Findings (요약) |
|----------|-------|-----------------|
| Critical | N | |
| High | N | |
| Medium | N | |
| Low | N | |

- **AC 충족 현황**: MET X / NOT MET A / PARTIAL C / UNTESTED U
- **Spec 위반**: E (spec-based 모드)
- **Test pass rate**: F%

---

## Simplicity (simplicity-review-agent)
<!-- simplicity-review-agent 리포트 통합 요약. 상세는 리포트 참조 -->
**Report**: `_sdd/implementation/<YYYY-MM-DD>_simplicity_review_<slug>.md`

| Severity | Count | Findings (요약) |
|----------|-------|-----------------|
| High | N | |
| Medium (gating) | N | |
| Low (advisory) | N | |

> correctness Critical/High + simplicity Medium+ finding은 REQUEST CHANGES rationale에 기여(자동 강제 아님), Low는 Suggested Improvements에 귀속.

---

## Recommendations

### Pre-merge Blockers
<!-- correctness Critical/High + simplicity Medium+ finding(rationale 기여) -->
| Priority | Item | Severity | Lens | Action |
|----------|------|----------|------|--------|

### Suggested Improvements
<!-- correctness 권고 + simplicity Low finding -->
| Priority | Item | Lens | Benefit |
|----------|------|------|---------|

---

## Next Steps

1. [ ] Take action based on Verdict
2. [ ] (if Approve) After merge, run `/spec-sync` if spec updates needed

---

## Metadata

**Review version**: <count>
**PR commit SHA**: <sha>
**Spec source**: from-branch / none
**Correctness report**: `_sdd/pr/<YYYY-MM-DD>_pr_correctness_<slug>.md`
**Simplicity report**: `_sdd/implementation/<YYYY-MM-DD>_simplicity_review_<slug>.md`
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

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Source**: correctness 계약·프로세스·출력 형식은 `.claude/agents/pr-review-agent.md`가, simplicity 계약·5개 차원·falsifiable severity는 `.claude/agents/simplicity-review-agent.md`가 각각 단일 소스로 보유한다. 이 orchestrator는 PR 데이터/spec 수집 + dispatch + verdict 합성 + 통합 리포트만 소유한다 (orchestrator↔agent; 동일 본문 mirror 아님).
