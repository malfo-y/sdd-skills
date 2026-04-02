# 토론 요약: pr-spec-patch + pr-review 통합

**날짜**: 2026-04-02
**라운드 수**: 5
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)

1. **두 스킬 통합 필요성**: pr-spec-patch(Step 1)와 pr-review(Step 2)는 항상 순차 실행되므로 하나로 합침
2. **산출물 구조**: 중간 산출물(spec_patch_draft.md) 제거, PR_REVIEW.md 1개로 통합
3. **Spec Patch Content 불필요**: from-branch에 spec이 있으면 이미 반영됨, 없으면 머지 후 /spec-update-todo로 해결
4. **spec 선택 로직**: to-branch spec은 "예전 스펙"이므로 from-branch spec을 기준으로 검증
5. **spec 없을 때 검증 범위**: 단순 confidence 표기가 아닌 코드 품질 전반 검증

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | 산출물: PR_REVIEW.md 1개 | 중간 산출물(spec_patch_draft.md) 불필요 | 2, 3 |
| 2 | patch-only 모드 없음 | 항상 patch 분석 + review를 한 번에 실행 | 1 |
| 3 | 스킬 이름: pr-review | 기존 이름 유지, 트리거 키워드 그대로 | 1 |
| 4 | 기존 pr-spec-patch, pr-review 삭제 | 통합 스킬이 대체 | 1 |
| 5 | 컨텍스트: PR diff + spec | base 브랜치 코드는 diff에서 추론, 별도 체크아웃 불필요 | - |
| 6 | Spec Patch Content 섹션 제거 | from-branch에 spec 있으면 이미 반영, 없으면 머지 후 /spec-update-todo | 3 |
| 7 | spec 선택: from-branch spec 우선 | to-branch spec은 이전 계약. from-branch가 머지 후 상태를 나타냄 | 4 |
| 8 | spec 없을 때: 코드 품질 전반 검증 | 에러 처리, 테스트, 보안 등 포함. 기존 degraded mode 강화 | 5 |

## 미결 질문 (Open Questions)

- 없음

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | 통합 pr-review SKILL.md 작성 | High | 구현 담당 |
| 2 | 기존 pr-spec-patch 디렉토리 삭제 | High | 구현 담당 |
| 3 | 기존 pr-review 덮어쓰기 | High | 구현 담당 |
| 4 | marketplace.json에서 pr-spec-patch 제거 | High | 구현 담당 |
| 5 | _sdd/pr/spec_patch_draft.md 관련 참조 정리 | Medium | 구현 담당 |

## 통합 스킬 설계 요약

### 프로세스 흐름

```
PR 주소/번호 입력
  → PR 메타데이터 수집 (gh pr view)
  → spec 로딩 (from-branch 우선, to-branch 비교용)
  → PR diff 분석
  → 코드 품질 검증 (항상) + from-branch spec 기반 검증 (spec 있을 때)
  → verdict (APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)
  → PR_REVIEW.md 생성
  → (머지 후 필요 시 /spec-update-todo)
```

### spec 선택 로직

from-branch spec 있으면 사용, 없으면 code-only.

### 검증 모드

code-only가 베이스. spec-based는 code-only 위에 추가 검증을 얹는 구조.

| 모드 | 조건 | 검증 항목 |
|------|------|----------|
| Code-only (베이스) | 항상 실행 | PR 설명 기반 AC 추론, 코드 품질, 에러 처리, 테스트, 보안 |
| Spec-based (추가) | from-branch에 spec 존재 시 | code-only + from-branch spec 기반 AC 검증, spec compliance, gap analysis |

## 토론 흐름 (Discussion Flow)

Round 1: 산출물 구조 + patch-only 모드 → 파일 1개 통합, patch-only 불필요
Round 2: 스킬 이름 + 기존 스킬 처리 → pr-review 유지, 기존 두 스킬 삭제
Round 3: 컨텍스트 수집 범위 → PR diff + spec (기존 방식 유지)
Round 4: Spec Patch Content 필요성 → 불필요 (머지 후 spec-update-todo로 처리)
Round 5: spec 선택 로직 → from-branch spec 우선, to-branch는 비교용만 + spec 없을 때 코드 품질 전반 검증
