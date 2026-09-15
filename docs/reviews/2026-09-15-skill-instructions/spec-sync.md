# spec-sync 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/spec-sync/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/spec-sync/SKILL.md)
- 판정 요약: 수정 필요 2 / 정리 후보 0 / 실행 검증 필요 0

## 역할과 유지할 계약

메인 루프가 입력 delta를 코드와 validation evidence에 따라 분류하고, 지속할 가치가 있는 정보만 global spec의 적절한 표면으로 반영한다. 코드와 구현 문서는 수정하지 않으며, verified만 current truth로 승격하고 planned와 미검증 정보는 표식 또는 Open Questions로 분리한다. 분할 feature별 planned 항목, invariant 판정, 기존 구조 보존, 기록 append-only, 버전 정합성, 종료 전 자체 검증을 유지한다.

## 기준별 판정

| 기준 | 판정과 근거 |
|---|---|
| 1. 적용 조건 | spec-sync-01: 읽는 입력의 합집합과 rename할 일회성 입력의 경계가 없다. |
| 2. 충돌과 우선순위 | spec-sync-01: 코드·구현 문서 불변 및 canonical history 경로와 모든 사용 input rename이 충돌한다. |
| 3. 확인·승인 경계 | 불필요한 재승인 지시는 없다. rename 범위 및 목적지 충돌 처리는 spec-sync-01에서 다룬다. |
| 4. 중복과 소유권 | 수정 필요 없음. status·discovery·쓰기·검증의 소유 절이 분리돼 있고 양 runtime 배포본은 byte 동일하다. |
| 5. 완료·복구 조건 | spec-sync-02: 전체 작업트리 diff의 과거 삭제를 이번 실행의 append-only 위반으로 판정할 수 있다. |
| 6. 절차의 필요성 | 수정 필요 없음. 여섯 단계가 입력→분류→배치→쓰기→검증에 대응한다. Final Check는 Step 6이 검증 패스임을 명시해 추가 변경 없는 중복 검증을 막는다. |

## Findings

### spec-sync-01 — 읽은 입력 전체와 처리 완료 rename 대상이 구분되지 않는다 [수정 필요]

- **기준 / runtime**: 1·2·3 / Claude·Codex 공통.
- **위치**: [Claude](../../../.claude/skills/spec-sync/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/spec-sync/SKILL.md), 양쪽 27·59–70·138–141행.
- **정확한 원문**:
  - 27행: “코드와 구현 문서를 직접 수정하지 않는다.”
  - 68행: “lowercase canonical `_sdd/spec/decision_log.md`, legacy uppercase `_sdd/spec/DECISION_LOG.md` fallback”
  - 141행: “이번 sync에 사용한 input file을 `_processed_` prefix로 rename한다.”
- **문제 상황**: 구현 후 sync가 코드·구현 report·feature draft·decision history를 읽는다. 이들은 모두 Input Sources에 속하므로 141행을 그대로 적용하면 일회성 `user_spec.md`뿐 아니라 이 파일들까지 rename 대상이 된다. 특히 같은 Step 5에서 append한 canonical `decision_log.md`를 곧바로 `_processed_decision_log.md`로 바꾸면 다음 실행의 명시 discovery와 기존 링크가 깨진다. 구현 전 split draft도 아직 Part 2 실행에 필요한 상태인데 경로가 변경될 수 있다. 이미 `_processed_`인 파일 재소비와 목적지 동명 파일 존재 시의 처리도 정해져 있지 않다.
- **예상 영향**: 불변 대상과 기록 경로를 보존하려면 실행자가 문서에 없는 예외를 추론해야 한다. 넓게 적용하면 코드 경로·handoff pointer·history discovery를 훼손할 수 있다. 실제 rename 발생을 관측했다는 뜻은 아니다.
- **최소 수정안**: Step 5가 rename 대상 집합을 명시적으로 소유하게 한다. 예를 들어 일회성 제출물인 `user_spec.md`·`user_draft.md` 또는 사용자가 소비 후 rename 대상으로 지정한 파일만 대상으로 삼고, 코드·구현 evidence·진행 중 draft·canonical history는 제외한다. 성공적으로 반영 또는 보류 위치를 기록한 뒤에만 rename하고, 이미 처리된 파일은 재접두하지 않으며 목적지가 있으면 덮어쓰지 않고 미처리 사유를 남긴다.
- **유지할 계약**: 일회성 입력의 처리 표식, 코드·구현 문서 불변, canonical history 경로, planned/verified 분류와 원본 내용 보존.
- **소유자**: 수정은 `spec-sync` Step 5. `feature-draft`·`implementation`은 보존해야 할 draft/evidence 경로의 소비자이며 동일 rename 규칙을 재소유하지 않는다.
- **spec 결정 필요**: `_processed_` 대상 집합은 현 문면에 확정돼 있지 않다. [components.md](../../../_sdd/spec/components.md) 16행도 넓은 표현을 반복하므로 대상 범위를 결정하고 그 설명을 함께 맞춰야 한다. rename 계약 자체를 임의 삭제하는 제안은 아니다.
- **검증 상태**: 문면·직접 이웃 경로 계약 대조 완료. 동작 미검증.

### spec-sync-02 — append-only 검증의 기준점이 이번 실행 이전 변경을 포함한다 [수정 필요]

- **기준 / runtime**: 5 / Claude·Codex 공통.
- **위치**: [Claude](../../../.claude/skills/spec-sync/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/spec-sync/SKILL.md), 양쪽 138·156·178행.
- **정확한 원문**:
  - 138행: “기존 entry는 수정·삭제하지 않고 신규 entry만 **append-only**로 추가한다.”
  - 156행: “기록 파일을 썼다면 `git diff`에서 `decision_log.md`·`logs/changelog.md`의 **삭제 줄이 0**인가 (append-only 위반 탐지)”
  - 178행: “미충족 항목이 있으면 해당 단계로 돌아가 수정한다.”
- **문제 상황**: 실행 시작 전에 사용자가 `decision_log.md`의 문장을 미커밋 수정해 삭제 줄이 이미 존재한다. 이번 sync는 새 entry만 정상 append했지만, 일반 `git diff`에는 기존 삭제도 포함돼 검증이 계속 실패한다. 반대로 index 대비 diff만 검사하면 시작 전에 staged된 변경과 실행 범위의 관계를 설명하지 못한다.
- **예상 영향**: 이번 실행이 만들지 않은 변경을 고쳐야만 종료할 수 있는 경로가 생긴다. 사용자 변경 복원·재수정은 append-only 및 기존 작업 보존과 충돌하고, 그대로 두면 강제 재수정 루프에 남는다.
- **최소 수정안**: 기록 파일의 실행 시작 시 내용을 기준점으로 확보하고, 종료 시 그 기준점에서 이번 실행이 추가한 delta에 삭제·기존 entry 수정이 없는지 검사한다. 시작 전 삭제는 별도 잔여 이슈로 보고하고 건드리지 않는다. 시작 기준점이 없어서 범위를 입증하지 못하면 과거 변경을 복구하려 하지 말고 검증 제한으로 명시한다.
- **유지할 계약**: 이번 sync의 기록 변경은 append-only이고, 버전과 changelog의 일치 검증 및 AC 자체 검증은 그대로 유지한다. 검증 실패를 무조건 통과로 바꾸지 않는다.
- **소유자**: `spec-sync` Step 6. 외부 reviewer 호출이나 새 gate는 필요 없다.
- **spec 결정 필요**: [components.md](../../../_sdd/spec/components.md) 16행에 `git diff` 삭제 줄 0이 명시돼 있다. append-only 불변식은 유지하되 검증 범위를 invocation delta로 정한다는 설명을 함께 반영해야 한다.
- **검증 상태**: Git 비교 기준과 문면상의 완료 경로 대조 완료. 해당 입력의 실제 스킬 실행은 하지 않았다.

## 런타임 차이와 의존성

양 runtime SKILL.md는 각각 178줄이며 `diff -u` 결과 차이가 없다. 직접 실행 스킬이라 agent lifecycle이나 도구 schema 분기 문제는 없다. byte 동일한 배포 짝 자체를 중복 결함으로 보지 않았다.

읽은 범위:

- [AGENTS.md](../../../AGENTS.md), [global spec](../../../_sdd/spec/main.md)의 guardrail·sync 결정·운영 제약, [env.md](../../../_sdd/env.md).
- [components.md](../../../_sdd/spec/components.md) 15–17행: producer, sync 쓰기/검증, reviewer 계약.
- [feature-draft](../../../.claude/skills/feature-draft/SKILL.md) 본문: Part 1 입력 마커, 49행 split handoff, 57행 산출물 경로, 119행 sync integration.
- [implementation](../../../.claude/skills/implementation/SKILL.md) 31·51–57·149행: 사용자 지정 draft 경로와 ledger source pointer 및 sync 입력 연결.
- [SDD_SPEC_DEFINITION.md](../../../docs/SDD_SPEC_DEFINITION.md) 156행, [SDD_WORKFLOW.md](../../../docs/SDD_WORKFLOW.md) 93행, [usage-guide.md](../../../_sdd/spec/usage-guide.md) sync 사용 시나리오.

`spec-sync`가 직접 읽도록 지시하는 별도 `references/` 문서는 없다. 이웃 `implementation-review`·`spec-review`의 전체 검증 알고리즘과 Codex 이웃 스킬 본문은 이번 leaf의 검토 범위가 아니다. Integration의 `spec-review` 표기는 별도 강제 호출로 단정하지 않았으며 중복 게이트 finding을 만들지 않았다.

## 권장 처리 순서와 검증

1. rename 대상을 확정하고 양 runtime Step 5와 component 설명을 함께 정리한다. 격리 fixture에서 일회성 user input·코드·구현 evidence·진행 중 split draft·canonical history를 함께 입력해 의도한 파일만 rename되는지 확인한다. 재실행·목적지 충돌에서도 덮어쓰기와 prefix 누적이 없어야 한다.
2. append-only 비교 기준을 실행 시작점으로 명시한다. clean fixture와 history에 기존 미커밋 수정이 있는 fixture 모두에서 정상 append는 통과하고, 이번 실행이 기존 entry를 바꾸면 실패해야 한다. 기존 사용자 변경은 보존돼야 한다.
3. 두 fixture에서 verified·planned·unverified delta를 섞어 current 승격, Planned 표식, Open Questions가 각각 유지되는지 확인한다. 양 runtime mirror diff와 `git diff --check`로 마감한다.

이번 리뷰는 정적 대조와 보고서 작성만 수행했다. 제안 수정, fixture 실행, 대상 스킬 호출은 수행하지 않았다.
