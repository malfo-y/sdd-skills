# Implementation Review Checklist

구현 리뷰와 스펙 후속 작업 연결을 위한 체크리스트다.

## 1) Preconditions

- [ ] 구현 계획 식별
- [ ] 진행 문서 식별
- [ ] 스펙 entry point 식별
- [ ] 로컬 실행이 필요하면 `_sdd/env.md` 확인

## 2) Task Verification

- [ ] 각 task의 기대 산출물 확인
- [ ] 구현 위치 확인
- [ ] 상태를 `COMPLETE` / `PARTIAL` / `MISSING`으로 구분

## 3) Acceptance Criteria

- [ ] 각 criterion에 code evidence 연결
- [ ] 각 criterion에 test evidence 연결
- [ ] `MET` / `NOT MET` / `UNTESTED` 판정

## 4) Issues

- [ ] Critical issue 식별
- [ ] Quality issue 식별
- [ ] Improvement 후보 식별

## 5) Spec Sync Follow-ups

- [ ] `Goal` 반영 필요 여부 확인
- [ ] `Runtime Map` 반영 필요 여부 확인
- [ ] `Component Index` 반영 필요 여부 확인
- [ ] `Component Details > Overview` 반영 필요 여부 확인
- [ ] `Common Change Paths` 반영 필요 여부 확인
- [ ] `Environment & Dependencies` 반영 필요 여부 확인
- [ ] `Open Questions` 반영 필요 여부 확인
- [ ] `DECISION_LOG.md` 제안 필요 여부 확인
- [ ] 각 항목을 `MUST update` / `CONSIDER` / `NO update`로 분류
- [ ] 기본 후속 액션이 `spec-update-done`인지 판단

## 6) Output

- [ ] Progress Overview 포함
- [ ] Acceptance Criteria Assessment 포함
- [ ] Issues Found 포함
- [ ] Test Status 포함
- [ ] Spec Sync Follow-ups 포함
- [ ] Recommended Spec Action 포함
- [ ] Recommended Next Steps 포함
- [ ] Open Questions 포함
