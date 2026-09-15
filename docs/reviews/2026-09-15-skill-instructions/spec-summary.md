# spec-summary 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/spec-summary/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/spec-summary/SKILL.md)
- 판정 요약: 수정 필요 1 / 정리 후보 1 / 실행 검증 필요 0

## 역할과 유지할 계약

현재 spec과 확인한 코드 근거를 `_sdd/spec/summary.md`의 설명용 whitepaper로 엮는다. global truth를 대체하지 않으며, active draft/ledger에 근거한 계획·진행 정보는 선택 부록으로만 둔다. runtime-local template의 제목·heading·순서, 원본 spec 보호, 명시적으로 요청한 README block만 갱신하는 경계, 종료 전 AC 검증을 유지한다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | spec-summary-01: README sync의 요청 조건은 명확하지만 대상 block의 식별·부재 분기가 없다. |
| 2. 충돌과 우선순위 | spec-summary-02: 산출물 write allowlist와 상위 하네스의 work log 의무를 구분하면 해석 충돌을 줄일 수 있다. |
| 3. 확인·승인 경계 | 수정 필요 없음. README sync는 명시 요청으로 활성화하며 추가 승인 요구가 없다. |
| 4. 중복과 소유권 | 수정 필요 없음. output 형식은 local reference가 소유하고 본문은 이를 소비한다. 두 runtime의 배포 mirror는 결함이 아니다. |
| 5. 완료·복구 조건 | spec-summary-01: block이 없는 README의 최초 sync를 어떻게 완료할지 정해져 있지 않다. spec 없음·약한 근거의 종료/축소 경로와 자체 검증은 있다. |
| 6. 절차의 필요성 | 수정 필요 없음. 근거 탐색, optional 입력 선별, template 적용, AC 대조는 산출물 계약과 직접 연결된다. 길이·단계 수 자체를 결함으로 보지 않는다. |

## Findings

### spec-summary-01 — README managed block의 경계와 최초 생성 규칙이 없다 [수정 필요]

- 기준: 1, 5. Runtime: Claude, Codex.
- 근거: [Claude SKILL](../../../.claude/skills/spec-summary/SKILL.md) 30, 81, 90행과 [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-summary/SKILL.md) 동일 행. 원문: “사용자가 README sync를 명시적으로 요청한 경우에만 `spec-summary` managed block을 갱신하고, block 밖 내용은 보존한다.”
- 직접 reference: [Claude template](../../../.claude/skills/spec-summary/references/summary-template.md), [Codex template](../../../plugins/sdd-skills-codex/skills/spec-summary/references/summary-template.md) 전체 1–41행에는 summary 본문 skeleton만 있고 README marker 정의가 없다.
- 문제 상황: 사용자가 README sync를 처음 요청했지만 README에는 `spec-summary` block이 없다. 또는 유사한 이름의 주석은 있으나 명확한 시작·끝 쌍이 없다. 어느 bytes가 허용된 write 영역인지, block을 새로 추가해도 되는지 계약만으로 결정할 수 없다.
- 예상 영향: 실행마다 서로 다른 marker를 새로 만들거나 기존 일반 summary 절을 managed block으로 해석할 여지가 있다. 안전하게 쓰기를 보류하면 이미 요청된 최초 sync가 미완료로 남는다. 이는 문면상 분기 누락이며 실제 오수정 관측은 아니다.
- 최소 수정안: Step 7에 고유한 시작·끝 marker 한 쌍을 정의한다. 정상 block은 내부만 교체하고, block이 없으면 명시 sync 요청 범위에서 EOF에 한 번 추가한다. 중복·불완전 marker는 README 수정만 보류하고 위치와 이유를 보고하되 summary 생성은 마친다.
- 유지할 계약: README 요청 조건, 기존 block 외 bytes 보존, 재실행 시 하나의 block만 유지, 기본 출력 경로 불변.
- 소유자: `spec-summary` Step 7의 Claude/Codex 짝. 다른 스킬 변경은 필요 없다. 상위 설계 변경 없이 빠진 write 경계를 구체화할 수 있다.
- 검증 상태: 정적 문면·직접 reference 대조 완료. 정상 block·block 없음·중복/불완전 block fixture에서의 실제 호출은 미실행.

### spec-summary-02 — 산출물 write 범위와 하네스 기록 의무의 층을 구분한다 [정리 후보]

- 기준: 2. Runtime: Claude, Codex.
- 근거: [Claude SKILL](../../../.claude/skills/spec-summary/SKILL.md) 30행과 [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-summary/SKILL.md) 30행. 원문: “나머지 `_sdd/spec/`·repository surface는 read-only다.”
- 연결 근거: [AGENTS.md](../../../AGENTS.md) §5 및 [하네스 canonical template](../../../.claude/skills/spec-create/references/agents-harness-template.md) 49행. 원문: “각 작업 단위 종료 시 예외 없이 `_sdd/work_log/<yyyy-mm-dd>.md`에 항목을 append 한다”. 같은 행은 독립 커밋도 작업 단위로 정의한다.
- 문제 상황: 하네스가 설치된 repo에서 사용자가 summary 생성과 해당 변경의 커밋을 요청한다. 산출물 보호를 repository 전체 read-only로 표현했기 때문에 별도 상위 의무인 work log append까지 금지하는 문장으로 읽힐 수 있다.
- 예상 영향: 상위 사용자·하네스 지시를 적용하면 해결할 수 있으므로 실행 불능 결함으로 단정하지 않는다. 다만 로그 생략이나 불필요한 확인을 유발할 수 있는 해석 여지가 남는다.
- 최소 수정안: “이 스킬이 생성·갱신하는 산출물은 summary와 요청된 README block으로 한정한다. 상위 하네스의 작업 기록 의무는 별도로 따른다.”로 scope를 명확히 한다. 로그 형식·작성 절차를 스킬에 복제하지 않는다.
- 유지할 계약: summary 작성 중 원본 spec·코드 보호, README opt-in, work log의 하네스 단독 소유, 상위 사용자 지시 우선.
- 소유자: 수정 위치는 `spec-summary` Hard Rules. cross-skill 의무의 소유자는 `spec-create`의 하네스 template이며 `spec-upgrade` 등에 배포된다. 공통 write allowlist 이슈로 통합 검토할 수 있다.
- 검증 상태: 정적 대조 완료. 상위 지시로 이미 해결 가능한 모호성의 정리 제안이며 동작 효과는 미검증.

## 런타임 차이와 의존성

- 두 SKILL.md와 두 `references/summary-template.md`는 각각 byte-identical임을 `cmp`로 확인했다. runtime 고유 도구·agent lifecycle에 의존하는 분기는 없다.
- 직접 reference는 두 runtime의 summary template 전부를 읽었다. 필요한 이웃 계약으로 하네스 canonical template §5, global spec의 document producer output interface, components의 `spec-summary` 행, spec definition의 summary 역할을 대조했다.
- 다른 스킬 전체 실행 계약과 외부 runtime 기능은 리뷰하지 않았다. `spec-upgrade` 하네스 배포 mirror의 byte parity는 이번 문서에서 검증하지 않았다.
- active draft/ledger가 없으면 부록을 생략하는 정책과 fenced skeleton의 verbatim 적용은 현행 spec의 명시적 설계다. 이를 status memo로 바꾸거나 reference 로드를 없애는 제안은 하지 않는다.

## 권장 처리 순서와 검증

1. Step 7에 README marker와 부재·손상 분기만 추가하고 양 runtime을 함께 맞춘다.
2. Hard Rules의 write 범위를 산출물 범위로 명확히 하되 하네스의 로그 계약은 포인터로만 인정한다.
3. 별도 임시 repo에서 README sync 미요청·정상 block·block 없음·손상 block을 각각 실행해 summary 생성, block 밖 bytes 보존, 재실행 멱등성, 필요한 로그 작성을 확인한다. 마지막에 template heading/order와 `git diff --check`를 확인한다.

이번 리뷰는 정적 검토와 리뷰 문서 작성만 수행했다. 대상 스킬 실행, 대상 스킬·reference 수정, 동작 검증은 하지 않았다.
