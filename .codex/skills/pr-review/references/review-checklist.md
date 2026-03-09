# PR Review Checklist

탐색형 스펙 기준으로 PR을 검증할 때 쓰는 체크리스트다.

## 1) Preconditions

- [ ] `gh auth status` 확인
- [ ] PR 번호 확인
- [ ] 메인 스펙 식별 (`_sdd/spec/main.md` 또는 `_sdd/spec/<project>.md`)
- [ ] 관련 컴포넌트 스펙 식별
- [ ] `_sdd/pr/spec_patch_draft.md` 존재 여부 확인
- [ ] 로컬 테스트가 필요하면 `_sdd/env.md` 확인

## 2) Acceptance Criteria

- [ ] 패치 초안의 Feature 항목별 acceptance criteria 확인
- [ ] Improvement / Bug Fix 항목 확인
- [ ] 각 criterion에 구현 근거(`file:line`) 연결
- [ ] 각 criterion에 테스트 근거 연결
- [ ] `✓ / ✗ / △` 상태 판정

## 3) Existing Spec Compliance

- [ ] 기존 핵심 계약을 PR이 깨지 않음
- [ ] 보안/권한/데이터 무결성 invariant 위반 없음
- [ ] breaking change가 있으면 명시됨
- [ ] 기존 컴포넌트 책임 경계와 충돌 여부 확인

## 4) Exploration-First Spec Impact

- [ ] 새 경로/디렉터리가 `Repository Map`에 반영되어야 하는지 확인
- [ ] 새 요청/이벤트/배치 흐름이 `Runtime Map`에 반영되어야 하는지 확인
- [ ] 새 컴포넌트/책임 변화가 `Component Index`에 반영되어야 하는지 확인
- [ ] 컴포넌트 동작 개요/설계 의도 변화가 `Component Details > Overview`에 반영되어야 하는지 확인
- [ ] 운영/디버깅 시작점 변화가 `Common Change Paths`에 반영되어야 하는지 확인
- [ ] 새 미확정 사항이 `Open Questions`에 들어가야 하는지 확인
- [ ] 중요한 설계 이유 변화가 `DECISION_LOG.md` 후보인지 확인
- [ ] 각 항목을 `MUST update` / `CONSIDER` / `NO update`로 분류

## 5) Gap Analysis

- [ ] patch draft에는 있으나 PR에는 없는 항목 식별
- [ ] PR에는 있으나 patch draft/스펙에는 없는 항목 식별
- [ ] 테스트 갭 식별
- [ ] 설정/관측성/문서화 갭 식별

## 6) Verdict

- [ ] `APPROVE`
  - blocker 없음
  - 핵심 criterion 충족
- [ ] `REQUEST CHANGES`
  - 미충족 criterion 또는 blocker 존재
- [ ] `NEEDS DISCUSSION`
  - 설계 결정 또는 의도적 스펙 변경 논의 필요

## 7) Report Completeness

- [ ] Verdict와 근거 포함
- [ ] Metrics Summary 포함
- [ ] Acceptance Criteria Verification 포함
- [ ] Spec Compliance Verification 포함
- [ ] Exploration-First Spec Impact 포함
- [ ] Merge Blockers 포함
- [ ] Post-Merge Spec Sync 포함
- [ ] Items Requiring Spec Update 포함
- [ ] Open Questions 포함
- [ ] Next Steps 포함
