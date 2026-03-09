---
name: pr-review
description: This skill should be used when the user asks to "review PR", "PR review", "review PR against spec", "PR 리뷰", "PR 검증", "스펙 기반 PR 리뷰", "PR 승인 검토", or wants to verify a pull request's implementation against the specification and spec patch draft.
version: 1.1.0
---

# PR Review

PR 구현이 현재 스펙과 스펙 패치 초안에 맞는지 검증하고 `_sdd/pr/PR_REVIEW.md`를 생성한다.

이 스킬은 기능 구현 여부만 보는 리뷰가 아니다. 탐색형 스펙 관점에서 아래도 함께 검토한다.

- 새 흐름이 `Runtime Map`에 반영되어야 하는가
- 새 컴포넌트/경로가 `Component Index`에 반영되어야 하는가
- 운영/디버깅 경로가 `Common Change Paths`에 반영되어야 하는가
- 구현이 스펙의 불변 조건과 결정 맥락을 깨지 않는가

## Hard Rules

1. `_sdd/spec/` 아래 스펙은 직접 수정하지 않는다.
2. 산출물은 `_sdd/pr/PR_REVIEW.md` 리뷰 리포트다.
3. 스펙 수정 필요 사항은 리포트의 `Items Requiring Spec Update`에만 기록한다.
4. 가능한 한 모든 핵심 판단은 `file:line`, 테스트명, diff 근거와 연결한다.
5. 기본 출력 언어는 한국어다.

## Inputs

- 현재 스펙: `_sdd/spec/main.md` 또는 `_sdd/spec/<project>.md`
- 링크된 컴포넌트 스펙
- `_sdd/pr/spec_patch_draft.md` (있으면 우선 사용)
- PR 메타데이터와 diff (`gh`)
- 테스트 결과 또는 로컬 실행 결과
- `_sdd/env.md` (로컬 실행이 필요할 때만)

## Review Axes

### 1. Acceptance Criteria

패치 초안에 있는 각 Feature / Improvement / Bug Fix가 실제로 구현되었는지 본다.

### 2. Spec Compliance

현재 스펙의 핵심 계약과 불변 조건을 PR이 어기지 않는지 본다.

### 3. Exploration-First Spec Impact

PR이 아래를 바꿨는지 본다.

- `Repository Map`
- `Runtime Map`
- `Component Index`
- `Common Change Paths`
- `Open Questions`
- `DECISION_LOG.md` 후보

## Process

### Step 1: Verify prerequisites

1. `gh auth status`
2. PR 번호 확인
3. `_sdd/pr/` 디렉터리 준비
4. 패치 초안 존재 여부 확인
5. 테스트를 로컬에서 돌릴 계획이면 `_sdd/env.md` 먼저 확인

### Step 2: Load review context

1. 메인 스펙과 관련 컴포넌트 스펙 로드
2. 패치 초안에서 acceptance criteria와 예상 spec impact 추출
3. PR 메타데이터, changed files, 핵심 diff 로드
4. 기존 스펙의 `Repository Map`, `Runtime Map`, `Component Index`, `Common Change Paths` 추출

패치 초안이 없으면 degraded mode로 진행하되, PR 설명과 diff에서 기준을 유추하고 리포트에 신뢰도 저하를 명시한다.

### Step 3: Verify acceptance criteria

각 acceptance criterion에 대해 아래를 정리한다.

- 구현 위치
- 관련 테스트
- 상태: `✓ Met` / `✗ Not Met` / `△ Partial`
- 메모

### Step 4: Verify spec impact and drift

아래 관점으로 PR을 본다.

- 새 디렉터리/파일/엔트리포인트가 생겼는가
- 기존 요청/이벤트/배치 흐름이 달라졌는가
- 컴포넌트 책임 경계가 바뀌었는가
- 변경/디버깅 시작점이 달라졌는가
- 새 미확정 사항이 생겼는가
- 구현이 기존 spec invariant를 위반하는가

### Step 5: Gap analysis

세 가지 갭을 정리한다.

1. 패치 초안에는 있는데 PR에 없는 것
2. PR에는 있는데 패치 초안/스펙에 없는 것
3. 테스트/문서화/관측성 갭

### Step 6: Decide verdict

| Verdict | 기준 |
|---------|------|
| `APPROVE` | 핵심 acceptance criteria 충족, 치명적 spec 위반 없음, blocker 없음 |
| `REQUEST CHANGES` | acceptance criteria 미충족, 테스트 실패, spec 위반, 보안/신뢰성 blocker |
| `NEEDS DISCUSSION` | 의도적 spec 변경, 설계 trade-off, 문서화 전 결정 필요 |

### Step 7: Write report

리포트에는 최소한 아래가 있어야 한다.

1. Verdict
2. 메트릭 요약
3. Acceptance Criteria Verification
4. Spec Compliance Verification
5. Exploration-First Spec Impact
6. Gap Analysis
7. Items Requiring Spec Update
8. Open Questions
9. Next Steps

기존 `PR_REVIEW.md`가 있으면 `_sdd/pr/prev/PREV_PR_REVIEW_<timestamp>.md`로 백업한다.

## Output Notes

좋은 PR 리뷰 리포트는 "통과/실패"만 말하지 않는다. 아래를 분명히 해야 한다.

- 어떤 spec section이 후속 업데이트가 필요한가
- 어떤 새 경로/컴포넌트/흐름이 문서에서 빠져 있는가
- merge 전 blocker와 merge 후 spec sync 작업이 무엇인가

## References

- 체크리스트: [`references/review-checklist.md`](references/review-checklist.md)
- 예시: [`examples/sample-review.md`](examples/sample-review.md)
- PR 명령 참고: [`../pr-spec-patch/references/gh-commands.md`](../pr-spec-patch/references/gh-commands.md)
