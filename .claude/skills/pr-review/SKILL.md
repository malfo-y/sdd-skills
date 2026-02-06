---
name: pr-review
description: This skill should be used when the user asks to "review PR", "PR review", "review PR against spec", "PR 리뷰", "PR 검증", "스펙 기반 PR 리뷰", "PR 승인 검토", or wants to verify a pull request's implementation against the specification and spec patch draft.
version: 1.0.0
---

# PR Review - 스펙 기반 PR 검증 및 판정

PR 구현을 원본 스펙과 스펙 패치 초안 대비 검증하여 구조화된 리뷰 리포트(`.sdd/pr/PR_REVIEW.md`)를 생성합니다.

## Overview

이 스킬은 PR의 구현 내용을 현재 스펙 문서(`.sdd/spec/`)와 스펙 패치 초안(`.sdd/pr/spec_patch_draft.md`)을 기준으로 검증하여, 수용 기준 충족 여부, 스펙 준수 상태, 갭 분석 결과를 포함한 구조화된 리뷰 리포트를 생성합니다. 최종 판정(Approve / Request Changes / Needs Discussion)을 제공합니다.

## Workflow Position

```
implementation → PR → pr-spec-patch → pr-review → 승인/수정 → spec-update
                          ↑              ↑↓
                     현재 스펙       검증 및 판정
                  (.sdd/spec/)     (.sdd/pr/PR_REVIEW.md)
```

## Language

Use Korean (한국어) for all communications with the user.
모든 내용은 한국어로 작성합니다.

## LLM Model to use

Use the default, most capable model (e.g. Opus 4.5) to review the PR otherwise mentioned by the user.
Report the model used at the beginning of the review.

## When to Use This Skill

- PR 생성 후 머지 전 검증
- 스펙 관점에서 PR 구현 리뷰
- 패치 초안의 수용 기준 클레임 검증
- 스펙 준수 확인 및 위반 감지
- 이미 머지된 PR에 대한 소급 리뷰

## Prerequisites

- `gh` CLI 인증 완료 (`gh auth status`로 확인)
- `.sdd/spec/` 디렉토리에 스펙 문서 존재 (권장)
- `.sdd/pr/spec_patch_draft.md` 존재 (권장, 필수 아님)
- PR이 존재하는 GitHub 저장소

## Input Sources

1. **현재 스펙 (`.sdd/spec/`)**: 기존 스펙 요구사항 및 아키텍처 기준
2. **스펙 패치 초안 (`.sdd/pr/spec_patch_draft.md`)**: PR에서 클레임한 변경사항 및 수용 기준
3. **PR 데이터 (`gh` CLI)**: PR 메타데이터, diff, 커밋 정보
4. **테스트 결과**: CI 상태 또는 로컬 테스트 실행 결과

## Output

**파일 위치**: `.sdd/pr/PR_REVIEW.md`

**형식**: 판정(Verdict) + 메트릭 요약 + 수용 기준 검증 + 스펙 준수 검증 + 갭 분석 + 권장 사항

## Process

### Mode 1: Preferred (패치 초안 있음)

#### Step 1: 사전 조건 확인

```
1. `gh auth status` 실행하여 인증 상태 확인
2. `.sdd/spec/` 디렉토리에서 스펙 파일 탐색
3. `.sdd/pr/spec_patch_draft.md` 존재 확인
4. PR 번호 확인 (자동 감지 또는 사용자 입력)
5. `.sdd/pr/` 디렉토리 없으면 생성
```

**패치 초안의 PR 번호 불일치 시:**
- 경고: "패치 초안이 다른 PR(#X)에 대한 것입니다."
- 패치 초안 무시하고 degraded mode 실행, 또는 `/pr-spec-patch` 재실행 권장

#### Step 2: 컨텍스트 로드

```
1. 현재 스펙 파일 읽기 (여러 파일이면 AskUserQuestion으로 선택)
2. 패치 초안 읽기 → 수용 기준(Acceptance Criteria) 추출
3. PR 메타데이터 수집 (gh pr view)
4. PR diff 수집 (gh pr diff)
```

PR 데이터 수집 명령어는 `pr-spec-patch/references/gh-commands.md` 참조:

```bash
# PR 번호 자동 감지
gh pr view --json number --jq '.number'

# PR 메타데이터
gh pr view [PR_NUMBER] --json title,body,author,state,url,additions,deletions,changedFiles,headRefName,baseRefName,commits,comments,reviews

# PR diff
gh pr diff [PR_NUMBER]

# 변경 파일 목록
gh pr diff [PR_NUMBER] --name-only
```

#### Step 3: 수용 기준 검증

패치 초안의 각 Feature/Improvement/Bug Fix에 대해:

```
각 수용 기준(Acceptance Criterion)에 대해:
1. PR diff에서 해당 구현 찾기 → 파일:라인 참조
2. 관련 테스트 찾기 → 테스트 이름
3. 테스트 통과 여부 확인 (CI 또는 로컬)
4. 상태 판정:
   - ✓ 충족: 구현 존재 + 테스트 통과
   - ✗ 미충족: 구현 없음 또는 테스트 실패
   - △ 부분 충족: 구현은 있으나 테스트 없음, 또는 부분적 구현
```

#### Step 4: 스펙 준수 검증

```
1. 기존 스펙의 주요 요구사항 목록 추출
2. PR 변경사항이 기존 요구사항을 위반하는지 확인
3. Breaking changes 식별
4. API 계약 변경 확인
```

#### Step 5: 갭 분석

세 가지 관점에서 갭 분석:

**(a) 패치 초안 vs PR 구현:**
- 패치에서 클레임했으나 PR에 미구현된 항목
- PR에 있으나 패치에 미기재된 변경사항

**(b) 테스트 갭:**
- 수용 기준 중 테스트되지 않은 항목
- 실패하는 테스트

**(c) 문서 갭:**
- 새 설정/환경변수가 문서화되지 않은 항목
- API 변경사항이 문서화되지 않은 항목

#### Step 6: 판정 결정

| 판정 | 조건 |
|------|------|
| **APPROVE** | 모든 수용 기준 충족 + 스펙 위반 없음 + 모든 테스트 통과 |
| **REQUEST CHANGES** | 중요 수용 기준 미충족 / 스펙 위반 / 테스트 실패 / 보안 이슈 |
| **NEEDS DISCUSSION** | 의도적 스펙 변경 / 설계 트레이드오프 / 스코프 모호성 / 새로운 아키텍처 결정 필요 |

#### Step 7: 리포트 생성

1. 기존 `PR_REVIEW.md`가 있으면 `PREV_PR_REVIEW_<timestamp>.md`로 아카이브
2. 아래 [Output Format](#output-format) 형식으로 `.sdd/pr/PR_REVIEW.md` 생성
3. 사용자에게 요약 제시 및 다음 단계 안내

### Mode 2: Degraded (패치 초안 없음)

패치 초안이 없는 경우 degraded mode로 실행:

```
경고 메시지:
"패치 초안 없이 리뷰합니다. `/pr-spec-patch` 실행 후 다시 리뷰하면 더 정확한 결과를 얻을 수 있습니다."
```

**차이점:**
- Step 2: 패치 초안 로드 건너뜀
- Step 3: 수용 기준을 PR diff에서 추론 (커밋 메시지, PR 설명 기반)
- Step 5: 갭 분석에서 패치 vs PR 비교 불가 → PR vs 스펙만 비교
- 리포트의 "Patch Draft" 필드: "Not Found"
- 전체적으로 낮은 확신도 명시

나머지 Step 4, 6, 7은 동일하게 수행.

## Output Format

```markdown
# PR Review Report

**PR**: #<number> - <title>
**PR Author**: <author>
**Review Date**: YYYY-MM-DD
**Reviewer**: Claude (<model>)
**Spec Version**: <version>
**Patch Draft**: Found / Not Found

---

## 검토 결과 (Verdict)

**[APPROVE / REQUEST CHANGES / NEEDS DISCUSSION]**

**근거**: <1-2 sentence rationale>
**주요 발견사항**:
- <finding 1>
- <finding 2>

---

## 메트릭 요약

| 항목 | 수치 |
|------|------|
| 수용 기준 총 개수 | N |
| 충족됨 (✓) | X (Y%) |
| 미충족 (✗) | A (B%) |
| 부분 충족 (△) | C (D%) |
| 스펙 위반 | E |
| 테스트 통과율 | F% |

---

## 수용 기준 검증

### Feature: <이름>
**Source**: Patch Draft - <section>

| # | 수용 기준 | PR 구현 | 테스트 | 상태 | 비고 |
|---|----------|---------|--------|------|------|
| 1 | <criterion> | `file:line` | test_name | ✓/✗/△ | note |

**평가**: X/Y 충족 ✓/✗

(각 Feature/Improvement/Bug Fix에 대해 반복)

---

## 스펙 준수 검증

### 기존 스펙 요구사항 검증

| 스펙 섹션 | 요구사항 | PR 영향 | 상태 | 비고 |
|----------|---------|---------|------|------|

### 스펙 위반 사항
(목록 또는 "없음")

---

## 갭 분석

### 패치 초안 vs PR 구현

#### 패치에서 클레임했으나 미구현
1. <item with file:line refs>

#### PR에 있으나 패치에 미기재
1. <item with file:line refs>

### 테스트 갭
1. <untested criteria or failing tests>

---

## 테스트 상태

### 테스트 실행 결과

| 테스트 파일 | 테스트 수 | 통과 | 실패 | 스킵 |
|------------|----------|------|------|------|

### 실패 테스트 상세
(실패 테스트별: 파일, 오류, 관련 수용 기준, 심각도, 조치)

---

## 권장 사항

### 머지 전 필수 (Blockers)
| Priority | 항목 | 심각도 | 위치 | 조치 |
|----------|------|--------|------|------|

### 머지 전 권장 (Recommended)
| Priority | 항목 | 심각도 | 조치 |
|----------|------|--------|------|

### 선택적 개선 (Optional)
| Priority | 항목 | 이점 |
|----------|------|------|

---

## 리뷰어 노트

### 설계 결정 사항
### 스펙 업데이트 필요 항목
### 후속 작업 제안

---

## 다음 단계

1. [ ] Verdict에 따른 조치
2. [ ] (if Request Changes) 수정 후 재리뷰: `/pr-review`
3. [ ] (if Approve) 머지 후 `/spec-update` 실행

---

## 메타데이터

**리뷰 버전**: <count>
**PR 커밋 SHA**: <sha>
**스펙 파일**: <path>
**패치 초안 파일**: <path or "없음">
**생성 시각**: YYYY-MM-DD HH:MM:SS
```

## Edge Cases

| 상황 | 대응 |
|------|------|
| 패치 초안 없음 | Degraded mode 실행, `/pr-spec-patch` 실행 권장 |
| 스펙 파일 없음 | 경고, `/spec-create` 권장, PR diff만으로 최소 리뷰 |
| PR 없음 / `gh` 미인증 | 오류 감지, 설치/인증 안내 |
| 여러 스펙 파일 | AskUserQuestion으로 선택 |
| 기존 리뷰 파일 존재 | `PREV_PR_REVIEW_<timestamp>.md`로 아카이브 후 새로 생성 |
| 다른 PR의 패치 초안 | 경고, 패치 초안 무시하고 degraded mode 또는 `/pr-spec-patch` 재실행 권장 |
| 이미 머지된 PR | 허용 (소급 리뷰), 머지 상태 명시 |
| 대규모 PR (50+ 파일) | 스펙 관련 컴포넌트에 집중, 디렉토리별 요약 |
| 테스트 없음 / CI 없음 | 테스트 섹션 "확인 불가"로 표시, 로컬 실행 안내 |

## Best Practices

### 효과적인 리뷰

- **증거 기반**: 모든 판정에 구체적 파일:라인 참조 포함
- **수용 기준 중심**: 패치 초안의 수용 기준을 체계적으로 하나씩 검증
- **스펙 대비 검증**: 새 기능뿐 아니라 기존 스펙 요구사항 위반 여부도 확인
- **테스트 연계**: 각 수용 기준에 대응하는 테스트 존재 및 통과 여부 확인

### 판정 기준

- **보수적 판정**: 확신이 없으면 NEEDS DISCUSSION으로 판정
- **블로커 명확화**: REQUEST CHANGES 시 반드시 구체적 블로커 목록 제시
- **설계 토론 분리**: 기능적 이슈와 설계 결정 사항을 구분하여 기재

### 파일 관리

- **아카이브 우선**: 기존 리뷰 파일은 항상 아카이브 후 새로 생성
- **리뷰 버전 추적**: 재리뷰 시 버전 번호 증가
- **패치 초안 연계**: 패치 초안 파일 경로를 메타데이터에 기록

## Language Handling

- **SKILL.md**: 영어 (스킬 정의)
- **리뷰 리포트 출력**: 한국어 (Korean)
- **스펙 언어 따르기**: 스펙이 한국어이면 리뷰도 한국어로 작성
- **PR 내용 보존**: PR 제목/설명은 원문 유지, 필요시 번역 병기

## Error Handling

| 상황 | 대응 |
|------|------|
| `gh` CLI 미설치 | 설치 안내: `brew install gh` |
| `gh auth` 실패 | `gh auth login` 실행 안내 |
| PR 번호 잘못됨 | 오류 메시지 표시, 올바른 PR 번호 요청 |
| 네트워크 오류 | 재시도 안내 |
| 스펙 파일 파싱 실패 | 오류 위치 표시, 수동 확인 요청 |
| `.sdd/pr/` 디렉토리 없음 | 자동 생성 |

## Additional Resources

### Reference Files
- **`references/review-checklist.md`** - PR 리뷰 체크리스트
- **`pr-spec-patch/references/gh-commands.md`** - `gh` CLI 명령어 레퍼런스

### Example Files
- **`examples/sample-review.md`** - PR 리뷰 세션 예시
