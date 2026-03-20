---
name: spec-update-todo
description: "This skill should be used when the user asks to \"update spec with features\", \"add features to spec\", \"update spec from input\", \"add requirements to spec\", \"spec update\", \"expand spec\", \"add to-do to spec\", \"add to-implement to spec\", or mentions adding new features, requirements, or planned improvements to an existing specification document."
version: 2.1.0
---

# Spec Update from User Input

사용자 입력/파일로부터 새로운 기능·요구사항을 파싱하여 기존 스펙 문서에 "to-add / to-implement" 항목으로 반영한다.

| Workflow | Position | When |
|----------|----------|------|
| Large | Step 2 of 6 | feature-draft 후 스펙에 사전 반영 (드리프트 방지) |
| Medium | — | feature-draft가 통합 처리 |
| Small | — | 직접 구현 |

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: 3가지 입력 소스 (대화, `user_spec.md`, `user_draft.md`) 중 하나 이상을 파싱하여 요구사항 추출
- [ ] AC2: 스펙 백업(`prev/PREV_*`) → 섹션 매핑 → 업데이트 적용 → 버전(patch) 증가 완료
- [ ] AC3: 처리된 입력 파일에 `_processed_` 접두사 추가 및 처리 메타데이터 기록
- [ ] AC4: 업데이트 요약 보고(변경 섹션·항목 테이블, 입력 파일 상태, 후속 안내) 출력
- [ ] AC5: 분할 스펙에서 각 항목이 의미적으로 적합한 파일에 배치되고, 신규 파일 생성 시 main.md 인덱스에 링크 추가됨

## Hard Rules

1. **백업 필수**: 스펙 수정 전 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
2. **입력 파일 리네임**: 처리 완료 시 `_processed_` 접두사로 이름 변경한다.
3. **언어 규칙**: 기존 스펙 언어를 따른다. 새 프로젝트는 한국어 기본. 사용자 명시 시 해당 언어. 섹션 내 언어 혼합 금지.
4. **스펙 구조 보존**: 기존 구조·스타일 유지, 필요한 항목만 추가한다.
5. **DECISION_LOG 최소화**: 결정 기록은 `DECISION_LOG.md`에만. 추가 문서는 사용자 요청 시에만 생성한다.
6. **양 파일 공존 시**: `user_draft.md` 우선, `user_spec.md` 보조 병합. 가정은 Update Plan에 기록한다.
7. **main.md 인덱스 동기화**: 새 sub-spec 파일 생성 시 반드시 main.md 인덱스에 링크를 추가한다. 고아 파일 금지.
8. **기존 스펙 구조 보존**: 기존 파일 분할 구조를 변경하지 않는다. 파일 추가만 허용, 기존 구조 재편성 금지.

## Input Sources

| 소스 | 경로 / 출처 | 설명 |
|------|------------|------|
| 대화 | 현재 대화 | 기능 설명, 요구사항, 개선 요청 등 |
| user_spec.md | `_sdd/spec/user_spec.md` | 사용자 작성 스펙 입력 (구조화/자유 형식 모두 가능) |
| user_draft.md | `_sdd/spec/user_draft.md` | 사용자 작성 초안 |
| DECISION_LOG | `_sdd/spec/DECISION_LOG.md` | (optional) 기존 결정·제약 참조용 |

## Process

### Step 1: 입력 소스 확인

**Tools**: `Glob`, `Read`

1. 대화에서 요구사항 유무 확인
2. `_sdd/spec/user_draft.md` → `_sdd/spec/user_spec.md` 순으로 파일 존재 확인
3. 입력이 하나도 없으면 → 짧은 보고 후 종료

### Step 2: 현재 스펙 로드 & 입력 파싱

**Tools**: `Read`, `Glob`

1. 메인 스펙 탐색 우선순위: `<project>.md` → `main.md` → 단일 `.md` → 2개 이상이면 인덱스 역할 파일 선택 (근거 기록)
2. 스펙 내용 읽기
   - 단일 파일: 해당 파일 읽기
   - 분할 스펙: main.md 인덱스에서 링크된 sub-spec 파일 목록 구성, 각 파일의 주제·섹션 구조 파악
3. `DECISION_LOG.md` 존재 시 참조
4. 입력에서 기능명, 설명, 우선순위, 수용 기준 등 구조화 정보 추출

### Step 3: 섹션 매핑 & Update Plan

**Tools**: — (분류·보고 단계)

입력 항목을 스펙 섹션에 매핑한다.

| Category | Target Section | Update Type |
|----------|---------------|-------------|
| Background/Motivation | 배경 및 동기 (§1) | Update narrative |
| Design Change | 핵심 설계 (§2) | Update design |
| New Feature | 목표 > 주요 기능 | Add to list |
| Enhancement | 개선 필요사항 > 개선 제안 | Add with priority |
| Bug Fix | 발견된 이슈 > 버그 | Add to issues |
| Component Change | 컴포넌트 상세 (§4) | Update/add section |
| Usage Scenario | 사용 가이드 (§5) | Add scenario |
| Configuration | 설정 (§8) | Add options |
| API Change | API 레퍼런스 (§7) | Add endpoints |

#### File Placement Decision (분할 스펙 전용)

단일 파일 스펙이면 건너뛴다.

1. **기존 파일 매칭**: 항목의 컴포넌트/기능이 기존 sub-spec 파일과 일치 → 해당 파일에 배치
2. **Cross-cutting 항목**: 환경변수, 글로벌 설정 등은 해당 §이 위치한 파일에 배치
3. **신규 파일 생성**: 매칭 없으면 새 파일 생성 (파일명 = 컴포넌트명, 예: `proxy.md`). main.md 인덱스에 링크 필수
4. **소규모 병합**: 생성될 내용이 50줄 미만이면 가장 관련도 높은 기존 파일에 병합 (소규모 = 잘못된 분할)

Update Plan에 파일 배치 결정을 포함한다:

| Item | Target File | Action | Reason |
|------|------------|--------|--------|

Update Plan을 작업 로그로 출력한 뒤 Step 4로 자동 진행한다.

### Step 4: 업데이트 적용

**Tools**: `Edit`, `Write`, `Bash (mkdir -p, mv)`

1. `mkdir -p _sdd/spec/prev/` → 백업 생성
2. 적절한 섹션에 항목 삽입 (기존 스타일·언어 유지)
   2-1. 신규 sub-spec 파일 생성 시: 파일 생성 → main.md 인덱스에 링크 추가
3. 버전 patch 증가 (X.Y.Z → X.Y.Z+1), 날짜 갱신, Changelog 항목 추가
4. 필요 시 `DECISION_LOG.md`에 항목 추가
5. 처리된 입력 파일을 `_processed_` 접두사로 이름 변경, 처리 메타데이터 추가

### Step 5: 검증 & 요약 보고

**Tools**: `Glob`

검증 체크리스트:
- 수정된 스펙 파일 존재
- Changelog 항목·버전 증가·백업 파일 존재
- 입력 파일 `_processed_` 리네임 완료
- (분할 스펙) 신규 파일이 main.md 인덱스에 링크됨

## Update Template

새 항목 삽입 시 기존 스타일에 맞추되, 아래를 기본 형식으로 참조한다.

```markdown
N. **[NEW] 항목명**: 설명  <!-- 추가됨: YYYY-MM-DD -->
   - 수용 기준 / 상세 (있을 경우)
```

상태 마커: 📋 계획됨 (새 항목 기본값) · 🚧 진행중 · ✅ 완료 · ⏸️ 보류

## Output Format

```markdown
## Spec Update Complete

**File**: `_sdd/spec/<spec>.md`
**Version**: X.Y.Z → X.Y.(Z+1)
**Date**: YYYY-MM-DD

### Applied Changes

| File | Section | Change | Item |
|------|---------|--------|------|
| ... | ... | ADD | ... |

### Input File Status
- [x] `user_draft.md` → `_processed_user_draft.md` (if used)
- [x] `user_spec.md` → `_processed_user_spec.md` (if used)

### Next Steps
- Run `/spec-update-done` after implementation to sync spec with code
```

## Error Handling

| Situation | Action |
|-----------|--------|
| Spec file not found | `spec-create` 먼저 실행 안내 |
| Ambiguous input | 최선 해석으로 진행, 판단 불가 시 Open Questions에 기록 |
| Conflicting requirements | Update Plan + Open Questions에 기록, 비파괴적 방향만 적용 |
| Invalid input file format | 파싱 오류 보고, 수정 제안 |
| 백업 디렉토리 미존재 | `mkdir -p` 자동 생성 |
| 섹션 매핑 불가 | 보수적 섹션에 반영, 불확실 항목은 Open Questions에 기록 |
| 파일 배치 판단 모호 | 가장 관련도 높은 기존 파일에 보수적 배치, Update Plan에 근거 기록 |

## Integration

```
Large:  feature-draft → spec-update-todo → implementation-plan → implementation → implementation-review → spec-update-done
Medium: feature-draft → implementation → spec-update-done
Small:  직접 구현 (→ spec-update-done)
```

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
