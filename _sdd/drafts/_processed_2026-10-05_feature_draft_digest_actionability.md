# Feature Draft: 필요한 맥락과 실행 가능한 digest 검증 레시피

> 규모 판정: 적격 — 내용 선택·갱신·reviewer 소비 계약과 양 runtime 미러는 Task 1, PR96 시범 적용을 위한 검증·반환은 Task 2가 소유하며 대응을 눈으로 검산할 수 있다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
다음 worker가 다시 조사하거나 잘못 판단할 내용을 digest에 남기고, 검증 레시피를 기존 구현·검증에서 실제 사용한 명령으로 구체화한다. 소유권은 기존 계약에 통합한다.

- `worker-boundary.md`는 항목별 재조사·오판 방지 필요성, 실행 가능한 레시피, 조건부 환경 사실의 내용 기준을 소유한다. 의미 판단은 정확한 rubric 참조를 허용한다.
- `SKILL.md`는 관련 변경분만 교체·삭제하고 소비된 draft 출처를 갱신하는 메인의 책임을 소유한다. 실제 실행 결과는 state에 남긴다.
- `implementation-review.md`는 레시피를 최소 검증 목록으로 사용하면서 변경 코드와 관련 경계의 독립 correctness 검토를 유지한다. 읽기 범위·fresh evidence·30초 한도는 유지한다.

## Scope
- **In**: 기존 계약 3개와 각 runtime 미러, 최신 `_sdd/implementation/2026-10-05_pr96_review_fixes/digest.md` 하나의 시범 개선. Task 2는 실행·정리 제안을 반환하고, 메인이 기존 digest 작성 권한으로 적용한 후 기존 correctness 게이트가 반영된 행과 결과를 검증한다.
- **Out**: 새 gate·agent·스키마·계측 프레임워크, 문구 존재 테스트, 과거 6개 digest 소급 정리, 새 모델/성능 실험, benchmark 계측기·보고서 수정, commit/push. 일상 digest 생성·갱신은 해당 작업의 구현·검증에서 얻은 명령을 재사용하며, digest 작성만을 위한 추가 조사·실행·스크립트 생성은 하지 않는다. global spec의 Planned 반영과 완료 승격은 별도 spec-sync 소유이며 아래 구현 Target Files에 포함하지 않는다.
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: 기존 소유 계약에 digest 선택·갱신·소비 기준을 통합한다
각 기준을 현재 소유 문서에만 보강해 맥락 손실과 검증 방법 재구성을 줄인다.

**Contracts**: Part 1의 세 계약을 변경한다. 공통 내용 기준을 개별 worker나 템플릿에 복제하지 않으며, main-only digest 작성과 worker의 변경분 반환 경계를 유지한다.

**Acceptance Criteria**:
- [ ] AC1: reviewer가 `worker-boundary.md`의 내용 계약을 인용해 다음 사례를 모두 판정한다: ① 없으면 필요한 재조사·오판이 생기는 결정/제약은 유지 ② draft·공통 계약과 겹치는 요약은 참조로 축소하되 핵심 조건은 보존 ③ 한 worker 전용 지시는 dispatch ④ 상태·통과 주장은 state. rubric은 이 네 사례이며, 단순 문구 존재가 아닌 각 사례의 귀속 근거가 evidence다.
- [ ] AC2: reviewer가 같은 내용 계약으로 ① 계획의 제안 명령은 구현·검증에서 실제 사용한 명령·입력·기대값으로 보완 ② 일상 digest 생성·갱신은 해당 작업의 구현·검증에서 얻은 명령을 재사용하며, digest 작성만을 위한 추가 조사·실행·스크립트 생성은 하지 않는다. 기존 검사 호출/짧은 명령을 재사용하고 의미 판단은 정확한 rubric 참조를 허용한다 ③ 환경 함정은 조건→문제→사용법과 이번 작업에 필요한 env 항목만 전달 ④ 좁은 관측의 일반화를 금지하는 흐름을 판정한다. 네 조건의 근거를 인용하면 MET이다.
- [ ] AC3: reviewer가 `SKILL.md`의 인계 파일·소비 흐름에서 ① 동일 AC의 명령 교체 ② 정정된 환경 사실 수정 ③ 닫힌 fix 전용 행 삭제 ④ draft 소비 rename 후 출처 갱신을 추적한다. 받은 변경분과 관련 항목만 갱신하고 매 반환 전체 digest 재심사·새 gate를 요구하지 않아야 한다. main-only 작성, 상태 분리, 다음 dispatch 전 반영을 유지한 인용 근거가 evidence다.
- [ ] AC4: reviewer가 `implementation-review.md`의 회귀·읽기 범위·Fresh Verification을 대조해, 레시피 실행 후에도 변경 코드와 관련 경계의 correctness를 검토할 수 있고 해야 하며 레시피가 검사 상한이 아님을 판정한다. 기존 3단 읽기 범위, state·이전 통과 주장 미열람, fresh 증거, 30초/slow 규칙이 함께 유지되어야 한다. 관련 절의 인용으로 MET/NOT MET을 판정한다.
- [ ] AC5: `/usr/bin/diff -r .claude/skills/sdd-orchestrator/references plugins/sdd-skills-codex/skills/sdd-orchestrator/references`는 무출력 exit 0이다. 두 SKILL의 `## Runtime: worker dispatch`부터 다음 `## Final Check` 직전까지 제거한 본문도 동일하고, `git diff --check`는 이번 변경에 공백 오류가 없다. 비교에 실제 사용한 짧은 명령을 반환한다.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/references/worker-boundary.md` -- 내용 선택·레시피·환경 사실의 단일 소유 계약
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/worker-boundary.md` -- 동일 계약 미러
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- 메인의 초기화·변경분 갱신·출처 갱신 책임
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- Runtime 밖 동일 본문 미러
- [M] `.claude/skills/sdd-orchestrator/references/workers/implementation-review.md` -- 최소 검증 목록과 독립 correctness 검토의 관계
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/workers/implementation-review.md` -- 동일 계약 미러

### Task 2: PR96 시범 digest에 넣을 레시피와 정리 변경분을 검증해 반환한다
Task 1의 확정된 계약으로 최신 PR96 digest의 실행 불가능한 두 행을 실제 검증하고, 메인이 적용할 변경분만 반환한다.

**Contracts**: worker는 이전/현재 digest를 직접 수정하지 않는다. 이 task는 검증과 변경 제안의 정확성으로 닫으며, 메인은 반환을 PR96 digest에 적용한 뒤 기존 correctness 게이트에 해당 digest를 명시적 검증 입력으로 전달한다. 별도 적용 task·reviewer·gate를 만들지 않는다.

**Acceptance Criteria**:
- [ ] AC1: PR96 Task 3 행의 대체 레시피는 아래 명령의 실제 입력과 16개 run을 포함하며 worker가 30초 한도 안에서 실행한다. 입력 `logs/runs.tsv`와 해당 sid transcript가 존재하고 결과에 요청한 16개 run이 각각 한 번씩 있으면 실행 가능한 레시피로 판정한다. `M2_main_edits`, `M2_unknown`, `M2_status`를 기존 report의 run별 값과 대조하고 불일치는 반환 본문의 제한/잔여 이슈로 보고한다. benchmark의 FAIL/UNVERIFIED와 레시피 실행 실패를 혼동하지 않는다. 입력 누락·timeout이면 해당 검증을 UNTESTED와 구체적 사유로 반환하며 새 모델 실행이나 무조건 반복으로 메우지 않는다.
  `python3 _sdd/goal/2026-10-04_orchestrator_harness_redesign/bench/metrics.py /tmp/claude-501/-Users-hyunjoonlee-github-sdd-skills/18bd1d97-361d-4d25-9233-2699074f6e25/scratchpad/bench 87-old-1 87-old-2 88-old-1 88-old-2 87-new-1 87-new-2 88-new-1 88-new-2 87-new-3 87-new-4 88-new-3 88-new-4 87-new-5 87-new-6 88-new-5 88-new-6`
- [ ] AC2: PR96 Task 1 미러 본문 행의 대체 레시피는 두 실제 SKILL 경로와 Runtime 제외 경계를 포함한 복사 실행 가능한 짧은 명령이다. worker가 fresh 실행해 동일 본문·exit 0을 확인하고 명령과 기대값만 digest 변경분에 반환한다. 실행 결과는 반환 본문에 둔다.
- [ ] AC3: worker는 PR96 digest에 대해 Task 1 AC1–3 rubric을 적용한 행별 유지·참조 축소·교체·삭제 제안을 반환한다. 변경 근거가 없는 행을 다시 쓰지 않고, 출처 draft의 현재 경로가 존재하며, Task 3·Task 1 미러 본문 행에 미해결 placeholder나 자연어만의 실행 지시가 없어야 한다. 조건부 입력 누락 대응과 필요한 env 항목은 남기되 상태·통과 주장·일회성 편집 지시는 제거한다. 이 AC는 반환한 제안의 rubric 판정과 출처 존재 확인으로 닫고 메인의 후속 쓰기에 의존하지 않는다.

**Target Files**:
- 없음 (read-only 검증). 읽기 대상은 PR96 digest, 그 출처 draft, Task 1의 변경 계약·SKILL, 기존 `bench/metrics.py`·`report.md`, 위 AC가 지정한 재계측 입력이다. 메인이 수정하는 PR96 digest는 worker Target Files가 아니다.

# Open Questions
- 사용자 확인 필요: 없음. 기존 handoff template과 implementation worker 반환은 공통 내용 계약을 이미 참조하므로 수정하지 않는다. 문서 의미 검증은 rubric+인용, 구조 동일성은 기존 diff와 짧은 본문 비교로 닫는다.
- 기존 report와 재계측 결과가 다르면 레시피의 유효성과 기존 보고의 정확성을 분리해 보고한다. 보고서·계측기 수정은 이번 범위 밖이며 메인이 잔여 이슈로 남긴다.
