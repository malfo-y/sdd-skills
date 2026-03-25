# SDD Skills 전체 리뷰 결과

**날짜**: 2026-03-21
**대상**: `.claude/skills/` 아래 전체 스킬 (19개)

## 수정 완료 스킬 (이전 작업)

| 스킬 | 수정 내용 |
|------|----------|
| spec-create | write-skeleton prefix, 멀티파일 구조 규칙 |
| spec-rewrite | write-skeleton prefix, 멀티파일 구조 규칙, write-skeleton 위임 위치 이동 |
| spec-upgrade | write-skeleton prefix, 멀티파일 구조 규칙, write-skeleton 위임 위치 이동 |
| spec-update-todo | 멀티파일 배치 로직 (AC5, Hard Rule 7-8, File Placement Decision) |
| spec-update-done | 멀티파일 배치 로직 (AC5, Hard Rule 6-7, File Placement Decision) |

## 미수정 스킬 리뷰 결과

### write-skeleton prefix 누락 (10개)

모든 `write-skeleton` 참조에 `sdd-skills:` prefix가 필요함.

| 스킬 | prefix 누락 | 기타 이슈 |
|------|:-----------:|----------|
| feature-draft | 1곳 | 없음 |
| implementation-plan | 1곳 | 없음 |
| implementation | **없음** | 없음 |
| implementation-review | 1곳 | 없음 |
| ralph-loop-init | **없음** | 없음 |
| discussion | **없음** | 없음 |
| spec-review | 1곳 | 없음 |
| spec-summary | 1곳 | 없음 |
| spec-snapshot | 1곳 | 없음 |
| guide-create | 1곳 | 없음 |
| git | **없음** | 없음 |
| pr-review | 1곳 | 없음 |
| pr-spec-patch | 1곳 | 없음 |
| write-phased | 1곳 | 없음 |

**요약**: 14개 스킬 중 **10개**에서 `write-skeleton` prefix 누락. 4개(implementation, ralph-loop-init, discussion, git)는 write-skeleton을 사용하지 않아 해당 없음.

### 멀티파일 스펙 구조 규칙

| 스킬 | 멀티파일 규칙 | 필요 여부 |
|------|:-----------:|----------|
| feature-draft | 없음 | Low — 스펙 패치 초안 생성이라 직접 스펙 구조를 다루지 않음 |
| implementation-plan | phase-split 규칙 있음 | 충분 |
| implementation | 없음 | 불필요 — 실행 단계 |
| implementation-review | 없음 | 불필요 — 리뷰 단계 |
| ralph-loop-init | 없음 | 불필요 — ralph 디렉토리 생성 |
| discussion | 없음 | 불필요 — 토론 전용 |
| spec-review | 없음 | Low — 읽기 전용, 수정 안 함 |
| spec-summary | 있음 | 충분 |
| spec-snapshot | 있음 | 충분 |
| guide-create | 암묵적 | 충분 |
| git | 없음 | 불필요 |
| pr-review | 없음 | 불필요 — PR 리뷰 전용 |
| pr-spec-patch | 없음 | 불필요 — 패치 초안 생성 |
| write-phased | 없음 | 불필요 — 범용 작성 도구 |

### 구조 품질 평가

| 스킬 | AC | Hard Rules | Process | Error Handling | 종합 |
|------|:--:|:----------:|:-------:|:--------------:|:----:|
| feature-draft | 5/5 | 충분 | 6 Step | 있음 | Good |
| implementation-plan | 5/5 | 충분 | 6 Step | 있음 | Excellent |
| implementation | 4/4 | 충분 | 복잡 | 있음 | Excellent |
| implementation-review | 4/4 | 충분 | Tier 3 | 있음 | Good |
| ralph-loop-init | 5/5 | 충분 | State machine | 있음 | Excellent |
| discussion | 4/4 | 충분 | 4 Step | 있음 | Excellent |
| spec-review | 5/5 | 충분 | 6 Step | 있음 | Good |
| spec-summary | 7/7 | 충분 | 4 Step | 있음 | Excellent |
| spec-snapshot | 4/4 | 충분 | 5 Step | 있음 | Good |
| guide-create | 5/5 | 충분 | 6 Step | 있음 | Excellent |
| git | 4/4 | 충분 | 5 Phase | 있음 | Excellent |
| pr-review | 5/5 | 충분 | 7 Step + Mode 2 | 있음 | Excellent |
| pr-spec-patch | 3/3 | 충분 | 6 Step | 있음 | Excellent |
| write-phased | 3/3 | 충분 | 4 Step | 있음 | Good |

## Action Items

### High Priority — write-skeleton prefix 일괄 수정

10개 스킬의 `write-skeleton` → `sdd-skills:write-skeleton` 변경:

1. feature-draft
2. implementation-plan
3. implementation-review
4. spec-review
5. spec-summary
6. spec-snapshot
7. guide-create
8. pr-review
9. pr-spec-patch
10. write-phased

### Low Priority — 추가 개선

- 없음. 구조/AC/Hard Rules/Error Handling 모두 양호.
