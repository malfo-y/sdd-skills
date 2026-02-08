---
name: pr-spec-patch
description: This skill should be used when the user asks to "create spec patch from PR", "PR spec patch", "compare PR with spec", "PR to spec", "PR 스펙 패치", "PR 리뷰 준비", "스펙 패치 생성", "PR 변경사항 스펙 반영", or wants to generate a spec patch document by comparing a pull request against the current specification.
version: 1.0.0
---

# PR Spec Patch - PR 기반 스펙 패치 초안 생성

PR(Pull Request)과 현재 스펙을 비교하여 구조화된 스펙 패치 초안을 생성하고, 대화를 통해 정제합니다.

## Overview

이 스킬은 PR의 변경사항을 분석하여 현재 스펙 문서와 비교하고, 스펙에 반영해야 할 변경사항을 구조화된 패치 초안(`_sdd/pr/spec_patch_draft.md`)으로 생성합니다. 출력의 "스펙 패치 내용" 섹션은 `spec-update-todo` 스킬의 입력 형식("Spec Update Input")과 호환되므로, 확정된 패치는 `spec-update-todo`로 바로 반영할 수 있습니다.

## 하드 룰: 이 스킬은 스펙을 직접 수정하지 않습니다 (중요)

- `_sdd/spec/` 아래의 스펙 파일은 **절대** 생성/수정/삭제하지 않습니다.
- 이 스킬의 산출물은 오직 `_sdd/pr/spec_patch_draft.md` 입니다.
- 스펙 반영은 **반드시** `/spec-update-todo`로 진행합니다.

## When to Use This Skill

- PR을 기반으로 스펙 패치 초안을 생성할 때
- PR 리뷰 전 스펙 관점에서 변경사항을 정리할 때
- PR 변경사항을 대화를 통해 정제하여 스펙에 반영할 때
- 이미 머지된 PR을 소급하여 스펙에 반영할 때

## Prerequisites

- `gh` CLI 인증 완료 (`gh auth status`로 확인)
- `_sdd/spec/` 디렉토리에 스펙 문서 존재 (권장, 필수는 아님)
- PR이 존재하는 GitHub 저장소

## Input Sources

1. **현재 스펙 (`_sdd/spec/`)**: 비교 기준이 되는 메인 스펙 문서
2. **PR 데이터 (`gh` CLI)**: PR 메타데이터, 변경 파일, diff
3. **사용자 대화 (현재 세션)**: 패치 초안 정제 및 확정
4. **기존 초안 (`_sdd/pr/spec_patch_draft.md`)**: 이전 초안이 있으면 업데이트 모드

## Output

**파일 위치**: `_sdd/pr/spec_patch_draft.md`

**형식**: PR 요약 + "Spec Update Input" 호환 패치 내용 + 질문 및 제안

## Process

### Mode 1: 초기 생성 (기존 초안 없음)

#### Step 1: 사전 조건 확인

```
1. `gh auth status` 실행하여 인증 상태 확인
2. `_sdd/spec/` 디렉토리에서 스펙 파일 탐색
3. `_sdd/pr/` 디렉토리 없으면 생성
```

**스펙 파일이 없는 경우:**
- 사용자에게 경고: "스펙 문서가 없습니다. `/spec-create`로 먼저 생성하는 것을 권장합니다."
- 사용자가 계속 진행을 원하면 비교 기준 없이 생성 (baseline 없음 명시)

#### Step 2: 현재 스펙 읽기

```
1. `_sdd/spec/` 내 메인 스펙 파일 로드
2. 여러 스펙 파일이 있으면 AskUserQuestion으로 선택 요청
3. 스펙의 컴포넌트, 기능, 섹션 구조 파악
```

#### Step 3: PR 데이터 수집

PR 번호가 지정되지 않은 경우 현재 브랜치에서 자동 감지:

```bash
# PR 번호 자동 감지 (현재 브랜치 기반)
gh pr view --json number --jq '.number'

# PR 메타데이터 수집
gh pr view [PR_NUMBER] --json title,body,author,state,url,additions,deletions,changedFiles,headRefName,baseRefName,commits,comments,reviews

# PR diff 수집
gh pr diff [PR_NUMBER]

# 변경된 파일 목록
gh pr diff [PR_NUMBER] --name-only
```

**대규모 PR 처리 (changedFiles > 50):**
- 디렉토리/컴포넌트별 요약으로 전환
- 스펙에 문서화된 컴포넌트에 집중
- 사용자에게 대규모 PR임을 알리고 핵심 변경사항 위주로 진행

#### Step 4: 변경사항 분석

PR의 파일 변경사항을 스펙 컴포넌트에 매핑:

| 분류 | 판별 기준 | 예시 |
|------|----------|------|
| New Features | 새 파일/모듈 추가, 새 엔드포인트, 새 클래스 | 새 서비스 클래스, 새 API 엔드포인트 |
| Improvements | 기존 파일 수정, 성능 개선, 리팩토링 | 함수 최적화, 코드 정리 |
| Bug Fixes | 버그 수정 커밋, 에러 핸들링 추가 | 예외 처리 추가, 조건문 수정 |
| Component Changes | 컴포넌트 구조 변경, 인터페이스 변경 | 새 메서드 추가, 시그니처 변경 |
| Configuration Changes | 설정 파일 변경, 환경변수 추가 | .env 변경, config 파일 수정 |

#### Step 5: 패치 초안 생성

수집/분석된 정보를 `_sdd/pr/spec_patch_draft.md`에 구조화하여 저장합니다.

출력 형식은 아래 [Output Format](#output-format) 섹션을 참조하세요.

#### Step 6: 사용자에게 제시

1. 생성된 패치 초안 요약을 보여줌
2. 질문 및 제안 섹션의 주요 항목을 하이라이트
3. 다음 단계 안내:
   - 내용 정제가 필요하면 대화 계속
   - 확정되면 `/spec-update-todo`로 반영 가능

### Mode 2: 대화 기반 업데이트 (기존 초안 있음)

#### Step 1: 기존 초안 로드

```
1. `_sdd/pr/spec_patch_draft.md` 내용 읽기
2. 초안의 PR 번호와 현재 요청 비교
3. 다른 PR의 초안인 경우: AskUserQuestion으로 처리 방법 확인
   - 기존 초안 아카이브 후 새로 생성
   - 작업 중단
```

#### Step 2: 사용자 의도 확인

AskUserQuestion을 사용하여 작업 유형 확인:

- **내용 정제**: 기존 패치 내용 수정/보완
- **질문 해결**: 질문 및 제안 섹션의 항목에 답변
- **항목 추가**: 새로운 변경사항 추가
- **항목 제거**: 불필요한 항목 삭제
- **재생성**: PR 데이터 다시 수집하여 초안 재생성
- **확정**: 현재 초안을 최종 확정

#### Step 3: 변경 적용

사용자 피드백에 따라 해당 섹션 업데이트:
- 패치 내용 수정/추가/삭제
- 질문 항목 해결 처리
- 스펙 갭 업데이트

#### Step 4: 저장

- 초안 파일 업데이트
- 메타데이터의 대화 라운드 증가
- 타임스탬프 갱신

## Output Format

```markdown
# PR Spec Patch Draft

**Date**: YYYY-MM-DD
**PR**: #<number> - <title>
**PR Author**: <author>
**PR URL**: <url>
**Target Spec**: <spec filename>
**Status**: 초안 / 검토됨 / 확정됨

---

## PR 요약

**브랜치**: <head> → <base>
**변경 규모**: +<additions> -<deletions>, <changedFiles>개 파일
**주요 변경사항**:
- <change 1>
- <change 2>
- <change 3>

---

## 스펙 패치 내용

<!-- spec-update-todo의 "Spec Update Input" 형식과 호환 -->

### New Features

#### Feature: <기능 이름>
**Priority**: High/Medium/Low
**Category**: <카테고리>
**Target Component**: <대상 컴포넌트>
**Source**: PR #<number>

**Description**:
<기능 설명>

**Acceptance Criteria**:
- [ ] 기준 1
- [ ] 기준 2

**PR 근거**:
- `<file>:<line>` - <변경 내용 요약>

---

### Improvements

#### Improvement: <개선 이름>
**Priority**: High/Medium/Low
**Current State**: <현재 상태>
**Proposed**: <제안 내용>
**Reason**: <개선 이유>
**Source**: PR #<number>

**PR 근거**:
- `<file>:<line>` - <변경 내용 요약>

---

### Bug Reports

#### Bug Fix: <버그 수정 이름>
**Severity**: High/Medium/Low
**Location**: <파일:라인>
**Source**: PR #<number>

**Description**:
<수정된 버그 설명>

**Fix Approach**:
<수정 방법>

**PR 근거**:
- `<file>:<line>` - <변경 내용 요약>

---

### Component Changes

#### New Component: <컴포넌트 이름>
**Purpose**: <목적>
**Input**: <입력>
**Output**: <출력>
**Source**: PR #<number>

**Planned Methods**:
- `method_name()` - 설명

#### Update Component: <컴포넌트 이름>
**Change Type**: Enhancement/Refactor/Fix
**Source**: PR #<number>

**Changes**:
- 변경 사항 1
- 변경 사항 2

---

### Configuration Changes

#### New Config: <설정 이름>
**Type**: Environment Variable / Config File
**Required**: Yes/No
**Default**: <기본값>
**Description**: <설명>
**Source**: PR #<number>

---

### Notes

#### Context
<PR의 배경 및 맥락>

#### Constraints
<제약 사항>

---

## 질문 및 제안

### 확인 필요 사항

1. **[섹션: <스펙 섹션명>]** <질문 내용>
   - 맥락: <왜 이 질문이 필요한지>
   - 제안: <권장 방안>

2. **[섹션: <스펙 섹션명>]** <질문 내용>
   - 맥락: <왜 이 질문이 필요한지>
   - 제안: <권장 방안>

### 스펙 갭

| # | 설명 | 스펙 섹션 | PR 근거 | 제안 |
|---|------|----------|---------|------|
| 1 | <갭 설명> | <관련 스펙 섹션> | `<file>:<line>` | <제안> |

### 모호한 사항

- <모호한 점 1>
- <모호한 점 2>

---

## 메타데이터

**생성일**: YYYY-MM-DD HH:MM
**스펙 버전**: <version>
**PR 커밋**: <HEAD SHA>
**대화 라운드**: <count>
```

## Edge Cases

| 상황 | 대응 |
|------|------|
| 스펙 파일 없음 | 경고 후 `/spec-create` 권장, 사용자 동의 시 baseline 없이 생성 |
| PR 없음 / `gh` 미인증 | 오류 감지, `gh auth login` 안내 |
| 여러 스펙 파일 존재 | AskUserQuestion으로 비교 대상 선택 |
| 다른 PR의 기존 초안 | AskUserQuestion: 아카이브 후 새로 생성 / 작업 중단 |
| 이미 머지된 PR | 허용 (소급 스펙 유지보수), 머지 상태 명시 |
| 대규모 PR (50+ 파일) | 디렉토리/컴포넌트별 요약, 스펙 관련 컴포넌트 집중 |
| PR에 스펙 관련 변경 없음 | 사용자에게 알림, 최소한의 패치 초안 생성 |

## Workflow Integration

```
implementation → PR → pr-spec-patch → (사용자 정제) → spec-update-todo
                          ↑                              │
                     현재 스펙                        메인 스펙 업데이트
                  (_sdd/spec/)                     (_sdd/spec/)
```

1. **pr-spec-patch** (이 스킬): PR과 스펙을 비교하여 패치 초안 생성
2. **사용자 정제**: 대화를 통해 초안을 검토/수정/확정
3. **spec-update-todo**: 확정된 패치를 메인 스펙에 반영

## Best Practices

### 효과적인 패치 생성

- **PR 근거 명시**: 모든 패치 항목에 PR diff의 구체적 파일:라인 참조 포함
- **스펙 섹션 매핑**: 각 변경사항이 스펙의 어느 섹션에 해당하는지 명확히 표시
- **우선순위 설정**: PR의 변경 규모와 영향도를 기반으로 우선순위 부여
- **질문 구체화**: 확인이 필요한 사항은 맥락과 제안을 함께 제시

### 대화 기반 정제

- **점진적 개선**: 한 번에 완벽한 초안보다 반복적 정제를 지향
- **질문 해결 우선**: 미해결 질문이 있으면 먼저 해결 후 확정
- **변경 이력 추적**: 대화 라운드를 통해 수정 이력 관리

### 파일 관리

- **단일 초안 유지**: PR당 하나의 패치 초안 파일 유지
- **아카이브**: 다른 PR의 초안은 아카이브 후 새로 생성
- **확정 후 처리**: 확정된 패치는 `spec-update-todo`로 반영 후 관리

## Language Handling

- **SKILL.md**: 영어 (스킬 정의)
- **패치 초안 출력**: 한국어 (Korean)
- **스펙 언어 따르기**: 스펙이 한국어이면 패치도 한국어로 작성
- **PR 내용 보존**: PR 제목/설명은 원문 유지, 필요시 번역 병기

## Error Handling

| 상황 | 대응 |
|------|------|
| `gh` CLI 미설치 | 설치 안내: `brew install gh` |
| `gh auth` 실패 | `gh auth login` 실행 안내 |
| PR 번호 잘못됨 | 오류 메시지 표시, 올바른 PR 번호 요청 |
| 네트워크 오류 | 재시도 안내 |
| 스펙 파일 파싱 실패 | 오류 위치 표시, 수동 확인 요청 |
| `_sdd/pr/` 디렉토리 없음 | 자동 생성 |

## Additional Resources

### Reference Files
- **`references/gh-commands.md`** - `gh` CLI 명령어 레퍼런스

### Example Files
- **`examples/spec_patch_draft.md`** - 패치 초안 출력 예시
