# 전체 스킬 지시 리뷰 — 2026-09-15

**20/20 스킬의 정적 리뷰와 문서 기록 완료.** 각 스킬 문서에 원문·위치·문제 상황·최소 수정안·유지할 계약·검증 상태를 남겼다. 각 리뷰는 수정 전 기준의 기록이며, 실제 스킬 실행이나 모델 행동 개선을 검증한 결과는 아니다.

**수정 결과:** [73개 항목의 처리 내역과 검증](./implementation-dispositions.md). 아래 원문 위치·미적용 표현·manifest는 리뷰 당시 snapshot으로 보존한다.

- 모델: gpt-6-astra. 기준 커밋: `be6c5a1f014b3e37d386127966b0bb6de3549587`.
- 대상: Claude 20개 + Codex 18개 = SKILL.md 38개, 이름 기준 20종. `git`·`second-opinion`의 Codex 짝 부재는 정상 배포 범위다. 사용자의 전역 설치 스킬은 범위 밖이다.
- 방법: 스킬별 runtime 짝을 묶은 병렬 리뷰 → 메인 작성자의 문서 검토·공유 계약 대조·중복 소유권 통합. 같은 모델의 병렬 리뷰이므로 모델 다양성 검증은 아니다.
- [공통 기준](./review-criteria.md): 적용 조건 / 충돌·우선순위 / 확인·승인 / 중복·소유권 / 완료·복구 / 절차 필요성.
- [원본 manifest](./source-manifest.json): SKILL·reference·example·script 파일 116개의 SHA-256. 모든 reference/script를 전문 감사했다는 뜻은 아니며, 실제 읽은 범위는 각 문서에 기록했다.
- 항목 수: 수정 필요 **60**, 정리 후보 **12**, 실행 검증 필요 **1**. 아래는 **스킬별 기록 수**이며 공유 원인·위치 중복을 포함한다. 독립 결함 수, 심각도 점수, 수정 우선순위 또는 모델 성능 수치로 사용하지 않는다.

## 먼저 볼 항목

1. **원본·실행 상태 보호**: [ralph-loop-init](./ralph-loop-init.md) `04·05`의 실패 DONE 및 reset/lock, [spec-sync](./spec-sync.md) `01`의 rename 범위, [git](./git.md) `03`의 기존 index 혼입.
2. **검증 대상의 정확성**: [pr-review](./pr-review.md) `01–03`의 head/spec 기준, [implementation-review](./implementation-review.md) `01`의 staged/untracked 범위, [implementation](./implementation.md) `02`의 inline AC 인계.
3. **확인과 중단의 범위**: [discussion](./discussion.md) `03·04`, [git](./git.md) `02`, [goal-init](./goal-init.md) `02–04`. 공통 AC 복구 정책은 아래에서 한 번 결정할 사안으로 묶었다.

이 순서는 예상 영향에 따른 후속 검토 제안이다. 원문 수정·설계 결정·실행 검증은 아직 남아 있다.

## 스킬별 문서

| 스킬 | 런타임 | 수정 필요 | 정리 후보 | 실행 검증 필요 | 핵심 내용 |
|---|---|---:|---:|---:|---|
| [discussion](./discussion.md) | Claude·Codex | 7 | 0 | 0 | 종료·coverage 예외, 재확인, 질문 선택지, 템플릿 슬롯 |
| [feature-draft](./feature-draft.md) | Claude·Codex | 1 | 1 | 0 | task 독립성과 census, 롤링 분할 AC 범위 |
| [git](./git.md) | Claude 전용 | 5 | 2 | 0 | 모드별 AC, 행동별 승인, 기존 index·dirty rebase·worktree |
| [goal-init](./goal-init.md) | Claude·Codex | 4 | 1 | 0 | 검증 재실행·STOP 경계, 질문 도구, 예제의 승인 근거 |
| [guide-create](./guide-create.md) | Claude·Codex | 1 | 1 | 0 | 언어와 verbatim skeleton, work log 쓰기 범위 |
| [implementation](./implementation.md) | Claude·Codex | 3 | 0 | 0 | read-only census의 RED 요구, inline AC 인계, 과거 위반 처리 |
| [implementation-review](./implementation-review.md) | Claude·Codex | 4 | 0 | 0 | 변경 집합, env 없는 검증, Low 정책, 제한 결과 종료 |
| [investigate](./investigate.md) | Claude·Codex | 2 | 1 | 0 | UNTESTED 종료, leaf 맥락 전달, fallback 소유권 |
| [plan-review](./plan-review.md) | Claude·Codex | 1 | 1 | 0 | 과거 순서 위반 복구, 배칭 문구 정렬 |
| [pr-review](./pr-review.md) | Claude·Codex | 7 | 0 | 0 | head SHA·spec 탐색/오류, 질문·종료·파일 충돌·AC ledger |
| [ralph-loop-init](./ralph-loop-init.md) | Claude·Codex | 5 | 0 | 0 | reset 전 lock, 실패 DONE 복구, phase·재시도·확인 경계 |
| [sdd-autopilot](./sdd-autopilot.md) | Claude·Codex | 1 | 1 | 0 | 실패/과거 위반 종료, Handoff 출력 책임 |
| [second-opinion](./second-opinion.md) | Claude 전용 | 3 | 1 | 0 | 외부 adapter와 spec 경계, read-only 전달, 실패 종료 |
| [spec-create](./spec-create.md) | Claude·Codex | 5 | 1 | 1 | 조건부 bootstrap, 하네스 슬롯·legacy, hook partial/trust |
| [spec-review](./spec-review.md) | Claude·Codex | 2 | 0 | 0 | 현행 AC와 legacy delta ID, 배칭 지시 |
| [spec-rewrite](./spec-rewrite.md) | Claude·Codex | 2 | 1 | 0 | review/rewrite 진입점, global/temporary 경계, shape 소유권 |
| [spec-snapshot](./spec-snapshot.md) | Claude·Codex | 1 | 0 | 0 | 목표 언어 없는 명시적 번역 요청 |
| [spec-summary](./spec-summary.md) | Claude·Codex | 1 | 1 | 0 | README block 경계, work log 쓰기 범위 |
| [spec-sync](./spec-sync.md) | Claude·Codex | 2 | 0 | 0 | 처리 완료 rename 범위, 기존 미커밋 변경과 검증 기준점 |
| [spec-upgrade](./spec-upgrade.md) | Claude·Codex | 3 | 0 | 0 | 이관/비대상 종료, 공유 legacy 문제, test/lint 삭제 예외 |

## 공통 문제와 수정 소유자

같은 원인을 스킬마다 별도 정책으로 고치지 않도록 아래 연결을 사용한다. 각 스킬 문서의 위치별 증거는 남기고, 공통 정책이나 reference는 소유자 한 곳에서 결정한다.

| 묶음 | 관련 증거 | 통합 처리와 보존할 경계 |
|---|---|---|
| AC 재시도와 실패·비대상·과거 위반 | [sdd-autopilot](./sdd-autopilot.md) 01, [implementation](./implementation.md) 03, [implementation-review](./implementation-review.md) 04, [plan-review](./plan-review.md) 01, [pr-review](./pr-review.md) 05, [investigate](./investigate.md) 01, [discussion](./discussion.md) 06, [ralph-loop-init](./ralph-loop-init.md) 02, [second-opinion](./second-opinion.md) 03, [spec-upgrade](./spec-upgrade.md) 01 | global spec §2의 공통 자체 검증 의미를 먼저 정렬한다. 성공/제한 결과/비대상과 복구 가능성을 구분하되 AC·gate·검증 의무를 삭제하지 않는다. 오류 분기가 이미 있는 스킬에서는 그 분기를 명시적으로 연결하는 최소 보완으로 충분할 수 있다. |
| census 생산·소비와 inline AC 인계 | [feature-draft](./feature-draft.md) 01, [implementation](./implementation.md) 01·02 | census 생산자는 feature-draft, 검증-only task의 소비자는 implementation, gate 기준 선택은 implementation-review. task 독립성·RED 적용 경계·검증 기준 전달은 서로 다른 의무라 하나를 고쳐도 나머지가 자동 해소되지 않는다. |
| 하네스 legacy 병합과 hook partial/trust | [spec-create](./spec-create.md) 03–05, [spec-upgrade](./spec-upgrade.md) 01·02 | legacy 예외는 두 producer에 일관되게 적용한다. spec-upgrade-02와 spec-create-03은 동일 공통 문제로 다룬다. hook canonical은 spec-create의 hook-installation이며 4미러에 전파한다. 손상 설정 보존·사용자 trust는 유지한다. |
| 템플릿 소비 예외와 슬롯 | [discussion](./discussion.md) 07, [guide-create](./guide-create.md) 01, [spec-create](./spec-create.md) 02·06, [spec-upgrade](./spec-upgrade.md) 03 | 각 template 소유자가 치환·반복·번역 범위를 정의한다. spec-upgrade의 test/lint 삭제 누락은 spec-create에 이미 예외가 있는 consumer 고유 문제이므로 branch 슬롯 문제와 합치지 않는다. |
| 스킬 산출물과 상위 work log | [guide-create](./guide-create.md) 02, [spec-summary](./spec-summary.md) 02 | 동일한 범위 명료화 후보다. 각 스킬은 자신이 만드는 산출물 범위를 정하고, work log는 하네스가 소유한다. 로그 절차를 모든 스킬에 복제하지 않는다. |
| 반복 정의·출력 | [sdd-autopilot](./sdd-autopilot.md) 02, [goal-init](./goal-init.md) 05, [spec-rewrite](./spec-rewrite.md) 03, [git](./git.md) 07 | 이미 제공된 Handoff 재사용, 실행법·temporary shape·충돌 정책의 단일 소유권을 확인한다. 배포 mirror나 소비 지점의 짧은 검증 참조는 그 자체로 삭제하지 않는다. |
| simplicity 객관적 gate와 주관적 advisory | [implementation-review](./implementation-review.md) 03 | implementation-review의 simplicity reference가 소유한다. pr-review·implementation은 같은 계약을 소비한다. 기존 Medium+ 객관 근거와 Low 비게이팅 경계를 보존한다. |
| 사전 승인과 외부 위임 경계 | [git](./git.md) 02, [goal-init](./goal-init.md) 04, [investigate](./investigate.md) 02, [second-opinion](./second-opinion.md) 01·02 | 승인은 행동별로 소비하고 없는 사용자 신호를 만들지 않는다. 외부 reviewer에는 관련 맥락·read-only 범위를 전달한다. second-opinion의 외부 adapter는 spec 결정 대상이며 내장 agent로 이름만 바꿔 독립 Codex 결과로 포장하지 않는다. |

## 통합 검토에서 정리한 판단

- `sdd-autopilot`의 goal-init 5단계 언급은 위임 포인터다. 이를 절차 중복 실행 결함으로 세지 않았다. 실제 사용자 출력 책임 중첩만 정리 후보로 남겼다.
- `git-05`는 “확인 없이 실행하지 말라”가 “확인하면 허용”을 뜻하지 않으므로 확정 모순에서 정리 후보로 낮췄다. `--force` 금지를 약화하는 제안이 아니다.
- spec-create에는 test/lint 없는 경우 줄 삭제 예외가 이미 있다. 동일 예외가 빠진 spec-upgrade consumer만 별도 finding으로 남겼다.
- 명시적인 배포 차이(`git`·`second-opinion` Claude 전용, investigate의 Codex diagnose-only)와 native goal setup-only, producer-owned gate, mandatory leaf 구조는 유지했다.
- 전역 AC 정책을 바꾸거나 기존 verbatim·외부 dispatch 계약을 바꾸는 수정은 spec 결정과 연결한다. 현재 문서의 제안만으로 global spec이 변경되거나 승인된 것으로 취급하지 않는다.

## 검증과 한계

- 20개 이름에 대한 문서 존재, 38개 runtime entrypoint 연결, 6개 기준별 판정, finding 분류와 요약 개수의 일치를 확인했다.
- 문서의 상대 링크 대상, 파일 권한 0644, whitespace를 확인했다. 원본 manifest와 재비교해 대상 자산 변경이 없음을 확인했다.
- 전체 20개 리포트는 메인 작성자가 읽고 공통 계약·핵심 인용을 대조했다. 원문 모든 줄의 독립적인 두 번째 감사나 모든 reference의 완전 검토는 수행하지 않았다.
- 실제 스킬 호출, 외부 reviewer/PR/goal/hook 동작, 제안 수정 및 수정 후 행동 검증은 수행하지 않았다. 성능·시간·질문 횟수 개선은 주장하지 않는다.
- 후속 수정 시 각 문서 마지막의 검증 시나리오를 사용한다. 설치본에 수정이 반영된 새 세션인지 확인하고, 관측된 결과를 해당 finding ID에 연결한다.
