# implementation 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/implementation/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/implementation/SKILL.md)
- 판정 요약: 수정 필요 3 / 정리 후보 0 / 실행 검증 필요 0

## 역할과 유지할 계약

계획 또는 inline task를 메인 루프가 직접 구현하고, Triage→RED→GREEN→커버리지 델타와 producer 소유 품질 게이트로 닫는 스킬이다. 코드·테스트 작성 위임 금지, 의미 있는 실패의 선행 관찰, 테스트 약화 금지, 변이 확인, resume ledger, 증거 없는 충족 금지, slow-test 실행 경계를 유지한다. 고정 gate 임계값과 최대 두 번 호출은 이번 리뷰의 변경 대상이 아니다.

양 runtime의 `implementation/SKILL.md`는 149행으로 byte-identical하다. 같은 문면이 각 배포에 존재한다는 이유로 중복 결함을 만들지 않았다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | implementation-01: producer가 만드는 read-only 검증 task와 모든 task에 대한 RED 적용 범위가 맞지 않는다. |
| 2. 충돌과 우선순위 | implementation-01, implementation-02: task 종류 및 inline 기준의 하류 소비 경계가 불완전하다. |
| 3. 확인·승인 경계 | 수정 필요 없음. 마감 3은 gate 반환 후 이미 승인된 fix·조건 판정·gate 2를 재질문 없이 이어 가도록 명시한다. 파괴적 동작 승인 완화는 제안하지 않는다. |
| 4. 중복과 소유권 | implementation-02: producer가 받은 inline AC가 reviewer의 기준 선택에 명시되어 있지 않다. gate/fix 소유권 자체는 명확하다. |
| 5. 완료·복구 조건 | implementation-03: 사후 복구할 수 없는 절차 위반에도 동일한 단계 복귀를 요구한다. gate 횟수 상한과 계약 오류 2회 중단은 명시되어 있다. |
| 6. 절차의 필요성 | 수정 필요 없음. Triage의 (c) 경로, resume-only ledger, delta 변이 확인은 현행 설계 목적과 연결된다. 길이나 강제어 수를 결함으로 판단하지 않았다. |

## Findings

### implementation-01 — read-only census task를 RED 없이 완료할 소비 경로가 없다 [수정 필요]

- **기준 / runtime**: 1·2·5 / Claude·Codex.
- **근거**: [implementation Claude](../../../.claude/skills/implementation/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/implementation/SKILL.md) 각 77–91행. “각 task를 셋 중 하나로 분류한다”, “(a)/(b) task는 구현 전에 테스트/check를 작성하고 **실제 실행해 실패를 관찰한다**.” AC2(21행)도 이 순서를 완료 조건으로 묶는다.
- **직접 이웃 근거**: [feature-draft Claude](../../../.claude/skills/feature-draft/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/feature-draft/SKILL.md) 각 51행. “Part 2 마지막에 read-only 검증 task(변형 표기 전수 grep census를 AC로, Target Files `없음 (read-only 검증)`)를 필수로 둔다.”
- **문제 상황**: rename 작업의 앞선 구현 task들이 정상 완료되어, 마지막 read-only task의 전수 잔존 검사가 처음부터 통과한다. 전수 검사는 실제 누락을 잡을 수 있으므로 동어반복뿐인 (c)에 해당하지 않는다. 그러나 (b)에 넣으면 요구 동작의 미충족인 RED를 관찰해야 하고, 해당 task에는 변경할 대상도 없다.
- **예상 영향**: 정상적인 검증 task를 완료하지 못하거나, RED를 만들기 위해 앞선 변경을 일시적으로 되돌리거나, 의미 있는 검사를 (c)로 잘못 분류할 수 있는 지시 경로다. 실제 실행에서 이런 행동이 관측됐다는 뜻은 아니다.
- **최소 수정안**: producer가 명시한 read-only 검증 task의 소비 규칙을 `implementation` 입력/Triage에 둔다. 해당 task는 요구된 검사를 fresh 실행해 PASS/FAIL 증거로 닫고, FAIL이면 관련 구현 task로 귀속한다. 실제 변경을 수행하는 task의 RED 선행은 그대로 둔다. ledger와 AC2가 이 경계를 참조하도록 정합시킨다.
- **유지할 계약**: 3-way triage의 기존 분류 의미, 구현 task의 test-first, census 전수검증 의무, 코드·테스트 단일 작성자. RED를 생략하는 일반 편의 경로를 만들지 않는다.
- **소유자**: `implementation`이 소비 규칙 소유. `feature-draft`는 read-only task 생산 계약 연결 대상. [feature-draft 리뷰](./feature-draft.md)의 feature-draft-01은 완료 독립성에 관한 별도 생산 계약 finding이므로 이 RED 소비 문제와 구분한다.
- **spec 결정 필요**: [global spec](../../../_sdd/spec/main.md) 86행의 “task별” test-first와 104행의 census 검증 task 소유권이 함께 성립하도록 검증-only 경계를 명시해야 한다. 단순 문구 축약으로 처리하지 않는다.
- **검증 상태**: 양 runtime 원문과 직접 producer 계약 대조 완료. 스킬 실행 미수행.

### implementation-02 — inline task AC가 마감 reviewer의 기준 선택에서 빠진다 [수정 필요]

- **기준 / runtime**: 2·4 / Claude·Codex.
- **근거**: [implementation Claude](../../../.claude/skills/implementation/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/implementation/SKILL.md) 각 32행은 “대화에서 직접 받은 inline task 목록”을 정식 입력으로 허용하고 AC를 보완하게 한다. 136행은 “`implementation-review`를 호출하고 finding을 직접 반영한다”라고 하지만, inline AC와 대상 범위를 reviewer 기준으로 넘기는 인계는 명시하지 않는다.
- **직접 이웃 근거**: [implementation-review Claude](../../../.claude/skills/implementation-review/SKILL.md) 37–45행, [Codex](../../../plugins/sdd-skills-codex/skills/implementation-review/SKILL.md) 82–90행. “**draft/plan 있음**: 호출자 지정 경로 또는 `_sdd/drafts/*_feature_draft_*.md` 최신”, 이후 “**spec만 있음**”, “**둘 다 없음**” 순이다. inline AC는 선택지에 없다.
- **문제 상황**: 파일 draft 없이 현재 대화의 AC 두 개로 구현했다. repo에는 이전 기능의 유효한 최신 draft가 있거나 global spec만 있다. reviewer의 명시 우선순위대로면 이전 draft의 task AC 또는 repo 요구사항이 선택되며, 이번 inline AC 두 개를 gate가 직접 검증한다는 계약이 사라진다. 같은 메인 루프가 대화를 기억하더라도 문서 우선순위와의 충돌은 남는다.
- **예상 영향**: 구현 자체의 증거 테이블은 있어도 gate가 다른 요구사항을 검증하거나, 현재 변경과 무관한 finding을 producer가 자동 fix하는 경로가 열린다. simplicity digest는 범위·형태 리뷰용이므로 correctness의 기준 누락을 대체하지 않는다.
- **최소 수정안**: producer가 정한 source task AC·현재 scope를 gate 입력으로 명시한다. reviewer의 기준 적응은 “호출자가 지정한 draft 또는 inline task AC”를 우선하고, 그것이 없을 때 기존 파일 discovery 순서를 사용한다. 새 draft나 별도 manifest 생성은 요구하지 않는다.
- **유지할 계약**: inline 구현 진입, graceful degradation, reviewer의 fresh verification, producer-owned gate/fix. producer ledger의 과거 실행 결과를 reviewer가 재사용하게 만들지 않는다.
- **소유자**: 기준 선택은 `implementation-review`, 전달 의무는 `implementation`. 중복 집계 시 이 두 스킬의 handoff finding으로 통합한다.
- **spec 결정 필요 여부**: 새 리뷰 모드나 gate 정책 변경은 필요 없다. 기존 inline 입력과 AC-first 계약을 소비 경계에 연결하는 보완이다.
- **검증 상태**: 양 runtime의 입력·gate 호출·reviewer 기준 적응을 대조했다. 실제 오선택 실행은 미관측.

### implementation-03 — 과거 절차 위반을 현재 산출물 누락과 같은 방식으로 복구하게 한다 [수정 필요]

- **기준 / runtime**: 5 / Claude·Codex.
- **근거**: [implementation Claude](../../../.claude/skills/implementation/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/implementation/SKILL.md) 각 18행. “미충족 항목은 해당 단계로 돌아가 수정한다.” 대상 AC에는 21행의 “RED 실패를 관찰한 뒤에만 구현을 시작”, 24행의 “코드·테스트 작성을 위임하지 않았다”가 포함된다.
- **문제 상황**: 마감 자체 검증에서 RED 관찰 전에 이미 구현했거나, 이미 코드 작성을 위임했다는 사실을 발견한다. 누락된 증거 테이블을 보완하는 것과 달리, 지금 RED를 만들거나 코드를 다시 직접 써도 과거의 순서·위임 사실은 바뀌지 않는다.
- **예상 영향**: 지시대로 완료 조건을 참으로 만들 수 없다. 불필요한 재구현·재위임 취소 시도 또는 사후 수행을 과거 준수로 잘못 보고하는 경로가 생긴다. test-first 위반을 허용해야 한다는 주장은 아니다.
- **최소 수정안**: 복구 가능한 산출물 누락은 해당 단계에서 고치되, 이미 발생한 절차·권한 위반은 위반 사실과 현재 결과를 분리해 보고하고 해당 프로세스 AC를 미충족으로 유지한다. 필요한 현재 상태 검증만 수행하며, 사후 검증을 선행 RED나 위임 금지 준수로 소급하지 않는 종료 경로를 명시한다.
- **유지할 계약**: AC 섹션, 종료 전 자체 검증, RED 선행·작성자 불변식, 증거 없는 완료 금지. 위반을 정상 완료로 승격하지 않는다.
- **소유자**: `implementation`의 구체 AC와 복구 문구. 공통 자체 검증 문구를 정비한다면 global spec/authoring norms 소유자와 연계한다.
- **spec 결정 필요**: [global spec](../../../_sdd/spec/main.md) 92행도 미충족 항목의 단계 복귀를 공통 완료 계약으로 정의한다. “복구 가능한 누락”과 “되돌릴 수 없는 위반”의 처리 구분을 공통 정책으로 정할 필요가 있다.
- **검증 상태**: 명시된 과거 사실형 AC와 복구 명령의 정적 충돌 확인. 실행 중 위반이나 복구 반복을 실제 관측하지 않았다.

## 런타임 차이와 의존성

- 대상 SKILL 본문은 byte-identical하다. Codex/Claude의 도구나 모델 지원 차이는 본문에 없으며 영구 capability 부재를 주장하지 않는다.
- `implementation`에는 별도 직접 reference 파일이 없다. 인계 검토를 위해 `feature-draft` 양 runtime의 분할·census·Required Output·gate/integration, `implementation-review` Claude 본문과 Codex 기준 적응·읽기 범위·실행 순서를 읽었다.
- [simplicity-contract Claude](../../../.claude/skills/implementation-review/references/simplicity-contract.md)의 Runtime Boundary·Hard Rules·Scope·차원·severity를 읽고 Codex mirror와 차이 없음을 확인했다. 이 reference는 correctness AC를 재판정하지 않는 소유권의 근거로만 사용했다. 반환 세부 품질은 이번 대상 밖이다.
- [spec-sync Claude](../../../.claude/skills/spec-sync/SKILL.md)의 입력·상태 분류·초기 절차를 읽어 Integration이 evidence-driven 승격과 연결됨을 확인했다. spec-sync 전체·Codex 짝, gate runtime lifecycle의 실제 지원 및 hook 실행은 미검토다.
- `AGENTS.md`, `_sdd/env.md`, global spec의 관련 Guardrails·품질 게이트·test-first·ledger·census·운영 제약을 검토했다. 과거 로그 및 동작 계측 자료를 새로 재분석하지 않았다.

## 권장 처리 순서와 검증

1. **read-only task 소비 경계 결정**: rename 구현 task와 마지막 census task가 있는 작은 draft로, 정상 경로에서 기존 동작을 깨뜨리지 않고 census PASS 증거와 gate까지 닫는지 확인한다. census FAIL 입력은 수정해야 할 구현 task로 귀속되는지 확인한다.
2. **inline AC handoff 보완**: 현재 inline AC와 무관하지만 유효한 최신 draft를 함께 둔 입력으로, gate ledger가 현재 inline AC만을 기준으로 선택하고 fresh 검증하는지 확인한다.
3. **복구 정책 구분**: 산출물 누락 입력은 보완 후 완료되고, 이미 발생한 RED 선행·작성 위임 위반 입력은 사실을 소급하지 않고 미충족으로 보고되는지 확인한다.

이번 작업은 지시의 정적 리뷰와 보고서 작성만 수행했다. 위 실행 시나리오는 후속 검증안이며 실행 결과가 아니다. 후속 변경 시 양 runtime mirror·관련 spec 문구·`git diff --check`를 확인하고, 설치본이 새 문면을 로드한 환경에서 동작을 검증한다.
