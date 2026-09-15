# Skill instruction review — finding dispositions

- 기준 리뷰: [인덱스](./README.md), 기준 commit `be6c5a1f014b3e37d386127966b0bb6de3549587`.
- 대조 대상: 2026-09-15 작업트리의 스킬·직접 reference diff. 통합 검증·최종 gate 결과는 아래 별도 항목에 기록한다.
- `적용`은 문면 수정 확인, `정리`는 의미·소유권·중복 정렬, `미적용`은 근거에 따른 제외, `PENDING`은 반영 확인 대기를 뜻한다. 적용 표시는 실제 설치본 행동이나 성능 검증을 뜻하지 않는다.
- 각 절의 소스 링크 아래 위치는 해당 스킬 폴더 기준이다. 별도 runtime 표기가 없으면 두 runtime에 적용하며, `git`·`second-opinion`은 Claude 전용이다.

## discussion

[리뷰](./discussion.md) · [Claude](../../../.claude/skills/discussion/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/discussion/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| discussion-01 | 적용 | 정체 fallback도 종료를 Gate 3→4로 연결. | SKILL.md §3.5.1; references/discussion-question-guide.md §Stagnation Handling |
| discussion-02 | 적용 | 사용자 지정 대안 생략을 coverage 충족으로 구분. | SKILL.md §3.2.1·3.2.2; references/discussion-question-guide.md |
| discussion-03 | 적용 | 입력만으로 토픽 gate가 닫히면 추가 확인 없이 진행. | SKILL.md §Step 1 |
| discussion-04 | 적용 | 기존 분류·종료 동의를 소비하고 새 미결·변경 분류만 확인. | SKILL.md §Gate 3→4 |
| discussion-05 | 적용 | Codex는 종료 포함 총 2–3개 옵션을 사용. | Codex SKILL.md §Step 3·Gate 3→4; references/discussion-question-guide.md |
| discussion-06 | 적용 | 중단·부분 저장을 정상 완료와 분리하고 소급 보완 금지. | SKILL.md §Error Handling·Final Check |
| discussion-07 | 적용 | 예시 값을 슬롯으로 바꾸고 반복·조건부 항목 처리 명시. | references/summary-template.md; SKILL.md §Step 4 |

## feature-draft

[리뷰](./feature-draft.md) · [Claude](../../../.claude/skills/feature-draft/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/feature-draft/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| feature-draft-01 | 적용 | 확정 선행 산출물·census 소비 허용; 미래 판정 의존은 경계 재설계. | SKILL.md §Process 3 |
| feature-draft-02 | 정리 | AC3 검산은 현재 feature, 나머지 scope는 Part 1에 보존. | SKILL.md §Acceptance Criteria·분할 규칙 |

## git

[리뷰](./git.md) · [Claude](../../../.claude/skills/git/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| git-01 | 적용 | 모드별 적용 AC와 clean 상태의 잔여 작업을 구분. | SKILL.md §Acceptance Criteria·Edge Cases·Shorthand Modes |
| git-02 | 적용 | 계획을 제시하되 기존 승인을 행동별로 판정. | SKILL.md §Phase 3: CONFIRM |
| git-03 | 적용 | 기존 staging 보존 및 commit 직전 현재 그룹의 index 확인. | SKILL.md §Phase 4: EXECUTE |
| git-04 | 적용 | rebase 전 dirty 전제조건과 변경 보존·복원 순서 명시. | SKILL.md §Phase 2·4; references/safety-rules.md §Stash Safety |
| git-05 | 정리 | 파괴적 작업 목록에서 Force Push 소유 절로 참조. | references/safety-rules.md §Destructive Operations·Force Push |
| git-06 | 적용 | Git이 해석한 상태 경로로 진행 중 작업을 확인. | SKILL.md §Phase 1: ASSESS |
| git-07 | 정리 | 충돌 정책 상세는 safety reference만 소유. | SKILL.md §Conflict Resolution; references/safety-rules.md §Conflict Resolution |

## goal-init

[리뷰](./goal-init.md) · [Claude](../../../.claude/skills/goal-init/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/goal-init/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| goal-init-01 | 적용 | Codex 질문 수단은 활성 runtime을 따르고 승인 응답 대기. | Codex SKILL.md §Step 1 |
| goal-init-02 | 적용 | 허용 검증·기존 evidence·미실행 사유와 최종 증거 요구를 분리. | references/harness-templates.md §검증 레시피·Loop Protocol; examples/sample-goal-init-session.md |
| goal-init-03 | 적용 | 성공 종료와 STOP/STUCK 미완료 종료를 구분. | references/harness-templates.md §Loop Protocol |
| goal-init-04 | 적용 | 예제 사용자 원문에 실제 자율 신호를 추가. | examples/sample-goal-init-session.md §1. Goal Intake |
| goal-init-05 | 정리 | Codex 실행법을 SKILL Step 5에서 채우는 슬롯으로 통합. | Codex references/harness-templates.md §실행법; SKILL.md §Step 5 |

## guide-create

[리뷰](./guide-create.md) · [Claude](../../../.claude/skills/guide-create/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/guide-create/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| guide-create-01 | 적용 | 표시 언어 번역은 계층·순서·필드 의미 보존 범위로 허용. | references/output-format.md 도입부; SKILL.md §Step 5 |
| guide-create-02 | 정리 | 가이드 산출물 범위와 상위 하네스 기록 의무 구분. | SKILL.md §Hard Rules·Final Check |

## implementation

[리뷰](./implementation.md) · [Claude](../../../.claude/skills/implementation/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/implementation/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| implementation-01 | 적용 | read-only task를 fresh 검증으로 닫고 FAIL은 구현 task로 귀속. | SKILL.md §Read-only 검증 task·Implementation Ledger·AC2 |
| implementation-02 | 적용 | source draft 또는 inline AC·현재 범위를 게이트에 전달. | SKILL.md §마감 3; ../implementation-review/SKILL.md §기준 문서 적응 |
| implementation-03 | 적용 | 과거 RED·위임 위반은 미충족으로 남기고 현재 검증과 분리. | SKILL.md §Acceptance Criteria |

## implementation-review

[리뷰](./implementation-review.md) · [Claude](../../../.claude/skills/implementation-review/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/implementation-review/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| implementation-review-01 | 적용 | working tree·index·untracked 합집합과 명시 base fallback 사용. | SKILL.md §읽기 범위 (3단 계단) |
| implementation-review-02 | 적용 | env 부재 시 확인된 다른 검증 명령 사용; 실행 불가 AC만 UNTESTED. | SKILL.md §Fresh Verification + 증거 결속 |
| implementation-review-03 | 적용 | Medium+ 객관 증명과 소유 차원 내 Low advisory를 분리. | references/simplicity-contract.md §Hard Rules·Severity Rules |
| implementation-review-04 | 적용 | dispatch 실패·과거 위반은 제한 보고로 종료; 재dispatch로 소급 금지. | SKILL.md §Acceptance Criteria·Error Handling |

## investigate

[리뷰](./investigate.md) · [Claude](../../../.claude/skills/investigate/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/investigate/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| investigate-01 | 적용 | 환경 제약은 UNTESTED·미충족 AC2·잔여 검증을 보고하고 반환. | Claude SKILL.md §Final Check |
| investigate-02 | 적용 | 조사 lane에 증상·재현 조건·기대 동작·배제 가설·scope digest 전달. | SKILL.md §Step 2; Codex Runtime Adapter 예시 |
| investigate-03 | 정리 | fan-out 가능 여부·fallback은 Runtime Adapter로 통합. | Codex SKILL.md §Step 2·Runtime Adapter |

## plan-review

[리뷰](./plan-review.md) · [Claude](../../../.claude/skills/plan-review/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/plan-review/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| plan-review-01 | 적용 | 미수행 누락만 보완; 과거 위반은 미완료 반환하고 producer로 복귀. | SKILL.md §Acceptance Criteria·반환·Integration; ../feature-draft/SKILL.md §품질 게이트 |
| plan-review-02 | 정리 | Codex 독립 읽기·검색을 한 메시지에 배칭하는 지시로 정렬. | Codex SKILL.md §읽기 지침 |

## pr-review

[리뷰](./pr-review.md) · [Claude](../../../.claude/skills/pr-review/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/pr-review/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| pr-review-01 | 적용 | headRefOid baseline과 읽기·실행 증거 SHA 결속. | SKILL.md §Step 0·1·3; PR Review Input |
| pr-review-02 | 적용 | diff에 spec 변경이 없어도 baseline tree에서 spec 탐색. | SKILL.md §Step 2 |
| pr-review-03 | 적용 | ABSENT와 UNREADABLE 분리; 후자는 제한 리포트. | SKILL.md §Step 2·4; Error Handling |
| pr-review-04 | 적용 | canonical index 우선, verdict에 영향을 주는 모호성만 질문. | SKILL.md §Step 2; Edge Cases |
| pr-review-05 | 적용 | 누락 렌즈·외부 blocker를 LIMITED로 보고하고 종료. | SKILL.md §Error Handling·Final Check; Output Format |
| pr-review-06 | 적용 | 기존 리포트 보존 및 빈 순번 suffix 사용. | SKILL.md §Step 1; Edge Cases |
| pr-review-07 | 적용 | 문제 AC ledger를 리포트 §4에 연결하고 MET은 축약. | SKILL.md §Correctness 리뷰·Output Format; examples/sample-review.md |

## ralph-loop-init

[리뷰](./ralph-loop-init.md) · [Claude](../../../.claude/skills/ralph-loop-init/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/ralph-loop-init/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| ralph-loop-init-01 | 적용 | 결과를 바꿀 미확정 정보만 질문하고 확정 내용은 진행. | SKILL.md §Step 2 |
| ralph-loop-init-02 | 적용 | 동일 초기화 호출의 수정·재검증 상한을 Step 8이 소유. | SKILL.md §Step 8·Error Handling·Final Check |
| ralph-loop-init-03 | 적용 | SETUP·DONE 예약 이름 보존, 중간 phase만 변경. | SKILL.md §State Machine Reference·Step 3·6 |
| ralph-loop-init-04 | 적용 | 실패 LLM 턴의 state를 복원하고 미확정 action 제거. | SKILL.md §Step 6 run.sh template: LLM_EXIT 실패 분기 |
| ralph-loop-init-05 | 적용 | reset 쓰기·삭제 전에 lock 획득과 cleanup 등록. | SKILL.md §Step 6 run.sh template: acquire_lock 이후 RESET 분기 |

실행 순서 변경의 fixture 검증 결과는 통합 검증란에서 별도로 확정한다.

## sdd-autopilot

[리뷰](./sdd-autopilot.md) · [Claude](../../../.claude/skills/sdd-autopilot/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/sdd-autopilot/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| sdd-autopilot-01 | 적용 | 실패·중단과 과거 경계 위반을 정상 완료에서 분리. | SKILL.md §Final Check·Step 3 |
| sdd-autopilot-02 | 정리 | goal-init Handoff를 relay로 소비하고 이미 표시한 항목은 반복하지 않음. | SKILL.md §Step 3 |

## second-opinion

[리뷰](./second-opinion.md) · [Claude](../../../.claude/skills/second-opinion/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| second-opinion-01 | 적용 | 외부 adapter 가용성 확인과 좁은 독립 Codex 예외 명시. | SKILL.md §Step 1·3 |
| second-opinion-02 | 적용 | 외부 prompt에 read-only·재spawn 금지·실행 한계 반환을 전달. | SKILL.md §Hard Rules·Step 3 |
| second-opinion-03 | 적용 | 외부 실패를 분석 결과로 대체하지 않고 미완료 종료. | SKILL.md §Step 4·Final Check |
| second-opinion-04 | 정리 | 정리 제목을 실제 동작인 임시 파일 경로로 변경. | SKILL.md §Hard Rules |

## spec-create

[리뷰](./spec-create.md) · [Claude](../../../.claude/skills/spec-create/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/spec-create/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| spec-create-01 | 적용 | 선택한 bootstrap만 실행·검증하고 선택된 하네스의 훅 의무 유지. | SKILL.md §Hard Rules·Step 3·5 |
| spec-create-02 | 적용 | 허용 치환 목록에 branch 슬롯 추가. | SKILL.md §Step 3a |
| spec-create-03 | 적용 | 식별되고 흡수된 legacy 생성물만 제거; 불확실 원문 보존. | SKILL.md §Step 3c |
| spec-create-04 | 적용 | runtime별 registered/skipped 검증과 partial 종료 분리. | references/hook-installation.md §Malformed JSON·Verification and Report; SKILL.md §Final Check |
| spec-create-05 | 적용 | 설치 준비와 runtime acceptance를 분리하고 trust 증거 없으면 pending. | references/hook-installation.md §Codex Trust Boundary·Verification and Report |
| spec-create-06 | 정리 | 템플릿 원칙 수의 중복 재서술 제거. | SKILL.md §Step 3a |
| spec-create-07 | 정리 | description을 생성·초기화 의도로 한정. 실제 오라우팅 여부는 미검증. | SKILL.md frontmatter description |

## spec-review

[리뷰](./spec-review.md) · [Claude](../../../.claude/skills/spec-review/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/spec-review/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| spec-review-01 | 적용 | 현행 task/AC evidence와 legacy delta ID 연결을 구분. | SKILL.md §Step 3: Code Drift Audit |
| spec-review-02 | 적용 | 독립 read-only 호출 배칭과 범위 확대 금지 명시. | SKILL.md §Process |

## spec-rewrite

[리뷰](./spec-rewrite.md) · [Claude](../../../.claude/skills/spec-rewrite/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/spec-rewrite/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| spec-rewrite-01 | 적용 | 품질 검토만 요청하면 spec-review로 라우팅. | SKILL.md frontmatter description |
| spec-rewrite-02 | 적용 | global 분할 규칙을 global portion으로 한정. | SKILL.md §Step 3 |
| spec-rewrite-03 | 정리 | temporary exact shape 복제 제거; same-runtime feature-draft 계약 참조. | SKILL.md §Step 3; references/spec-format.md·template-compact.md·rewrite-checklist.md |

## spec-snapshot

[리뷰](./spec-snapshot.md) · [Claude](../../../.claude/skills/spec-snapshot/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/spec-snapshot/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| spec-snapshot-01 | 적용 | 번역 요청의 목표 언어 미확정 때만 질문; 일반 snapshot은 원본 언어. | SKILL.md §Step 1 |

## spec-summary

[리뷰](./spec-summary.md) · [Claude](../../../.claude/skills/spec-summary/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/spec-summary/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| spec-summary-01 | 적용 | README marker 경계·최초 생성·불완전 경계 보류 규칙 정의. | SKILL.md §Step 7 |
| spec-summary-02 | 정리 | summary/README 산출물 범위와 하네스 기록 의무 분리. | SKILL.md §Hard Rules·Final Check |

## spec-sync

[리뷰](./spec-sync.md) · [Claude](../../../.claude/skills/spec-sync/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/spec-sync/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| spec-sync-01 | 적용 | 소비 완료 일회성·명시 지정 입력만 rename; 코드·진행 draft·evidence·history 보존. | SKILL.md §Step 5 |
| spec-sync-02 | 적용 | 실행 시작 bytes를 기준으로 append-only delta 검증. | SKILL.md §Step 1·6·Final Check |

## spec-upgrade

[리뷰](./spec-upgrade.md) · [Claude](../../../.claude/skills/spec-upgrade/SKILL.md) · [Codex](../../../plugins/sdd-skills-codex/skills/spec-upgrade/SKILL.md)

| Finding | 처리 | 반영 내용 | 현재 파일·절 |
|---|---|---|---|
| spec-upgrade-01 | 적용 | 이관·비대상 종료와 migration AC 분리; partial은 제한 보고. | SKILL.md §Step 1·Acceptance Criteria·Final Check; references/hook-installation.md |
| spec-upgrade-02 | 적용 | spec-create와 같은 legacy 식별·흡수 예외 적용. | SKILL.md §Step 6 |
| spec-upgrade-03 | 적용 | reference의 test/lint 부재 조건부 삭제를 명시적으로 허용. | SKILL.md §Step 6 |

## 통합 검증과 최종 gate

- 문서 coverage·링크·권한: 20개 리뷰의 73개 finding ID가 중복·누락 없이 대응하고 모든 문서 링크 대상이 존재함을 확인했다. 파일 권한은 0644다.
- 실행 검증: `python3 tools/test-ralph-templates.py` — 7 tests / 양 runtime 16개 시나리오 PASS (최종 7.352초). 실제 SKILL의 run.sh를 추출해 가짜 CLI·임시 파일로 실행했다. 실패 DONE·lock 거부 전 reset·백업 저장 실패를 기존 동작에서 RED로 확인한 뒤 수정했고, 정상 action→DONE·재시작·reset도 검증했다. 양 template `bash -n` PASS.
- 정적 검증: 38개 SKILL frontmatter YAML parse PASS. `quick_validate.py` 33 PASS, 나머지 5개는 기존 `argument-hint`/`user_invocable` 미지원으로 baseline과 동일 실패(회귀 0). 18개 runtime 짝의 diff를 대조하고 의도된 adapter·CLI 차이를 유지했다. 공통 template/reference 3짝 및 hook installation 4미러 byte parity PASS. 새 상대 파일 링크 오류·권한 오류 없음, `git diff --check` PASS.
- 변경량: 스킬·직접 자산 74파일 수정. 문장을 무조건 줄이기보다 충돌을 없애고 필요한 조건을 명시했다. 기존 사용자 dirty 파일 2개는 bytes를 보존했다.
- implementation-review gate 1 (gpt-6-astra): correctness C0/H0/M2/L0 + simplicity C0/H0/M1/L0. 총 M3으로 gate 2 임계 미달. 세 finding 모두 수정했다: 백업 실패를 숨기던 shell 명령, 제작 규범의 슬롯-only 설명, 테스트의 단일 사용처 추출 helper. fix 후 7개 회귀·양 bash 문법·diff 검사를 통과했다.
- 리뷰 절차 제한: 참조 leaf에 전달한 계약에서 원문에 없는 `그중` 한 단어가 추가되어 verbatim 전달 요건은 미충족이다. 두 leaf의 차원·read-only 범위와 반환은 확보했지만 과거 절차를 소급 충족으로 표시하지 않는다. 산문은 diff hunk와 인접 계약 대조 중심이며 전 스킬의 실제 대화 재현은 아니다.
- 설치본 행동·성능: Astra/Fable 실제 세션 비교·슬래시 호출·외부 adapter·PR 원격 작업·hook trust는 미실행. 설치된 plugin cache는 갱신하지 않았다.
