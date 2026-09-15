# plan-review 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/plan-review/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/plan-review/SKILL.md)
- 판정 요약: 수정 필요 1 / 정리 후보 1 / 실행 검증 필요 0

## 역할과 유지할 계약

feature draft의 요청 정합성·task 경계·숨은 결정·과잉 설계·검증 약점을 메인 루프가 한 번씩 감사한다. draft와 코드는 수정하지 않으며 Blocker Status와 findings만 반환한다. 외부 사실은 판정 전에 실재 대조하고, 그래도 근거가 부족하면 탐색을 확장하거나 finding을 만들지 않는다.

직접 실행과 분할 금지, 단일 패스, 리포트 파일 없음, Critical/High만 implementation blocker라는 계약을 유지한다. producer인 `feature-draft`가 fix와 조건부 두 번째 호출을 소유하고, 리뷰 반환 직후 사용자 입력을 기다리지 않고 producer로 복귀하는 구조도 유지한다. 현재 고정 임계나 호출 상한은 변경 제안 대상이 아니다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | plan-review-01: 자체 검증 복구 지시가 과거 순서 위반에도 적용되는 문면이다. 대상 부재 시 1줄 종료는 Input과 AC1에 명시되어 있다. |
| 2. 충돌과 우선순위 | plan-review-01: 해당 단계 복귀와 재점검 금지 사이의 실패 처리 우선순위가 없다. plan-review-02는 배칭 문면 정리 후보다. |
| 3. 확인·승인 경계 | 수정 필요 없음. 불필요한 사용자 확인을 요구하지 않으며, gate 반환 직후 fix 단계 복귀가 명시되어 있다. |
| 4. 중복과 소유권 | 수정 필요 없음. reviewer는 판정 술어를, producer는 작성 상세와 fix를 소유한다. AC의 자체 검증용 재진술과 runtime mirror 자체는 결함으로 보지 않는다. |
| 5. 완료·복구 조건 | plan-review-01: 사후에 충족시킬 수 없는 이력 조건과 현재 보완 가능한 누락의 구분이 필요하다. |
| 6. 절차의 필요성 | 수정 필요 없음. 5 smell, 외부 사실 대조, 최소 읽기, 짧은 반환은 각기 명시된 검토·범위 계약을 수행한다. 직접 실행을 분할로 바꾸는 제안은 하지 않는다. |

## Findings

### plan-review-01 — 과거 순서 위반까지 단계 복귀로 복구하도록 지시한다 [수정 필요]

- **기준:** 1, 2, 5.
- **적용 runtime:** Claude, Codex.
- **근거:** [Claude SKILL](../../../.claude/skills/plan-review/SKILL.md) 16–21행, [Codex SKILL](../../../plugins/sdd-skills-codex/skills/plan-review/SKILL.md) 16–21행.
  - 16행: “미충족 항목은 해당 단계로 돌아가 수정한다.”
  - 19행: “재점검 루프 없음”, “smell 판정에 **앞서** 실제로 있었다”.
  - 21행: Claude는 “서브에이전트 dispatch”, Codex는 “agent spawn”이 없었음을 완료 조건으로 둔다.
- **문제 상황:** reviewer가 smell 하나를 판정한 뒤 해당 외부 사실의 사전 대조를 빠뜨렸다고 자체 검증에서 발견한다. 뒤늦게 읽더라도 ‘판정에 앞서 호출이 있었다’는 이력은 충족되지 않는다. 해당 smell을 다시 판정하면 재점검 금지와 충돌한다. 이미 금지된 dispatch를 했다면 돌아가더라도 AC4의 이력을 복구할 수 없다.
- **예상 영향:** 완료할 수 없는 AC를 충족하려고 내부 재점검을 반복하거나, 순서 위반을 사후 읽기로 해소했다고 잘못 보고할 경로가 생긴다. 실제 반복 실행을 관측했다는 뜻은 아니다.
- **최소 수정안:** 자체 검증 안내를 “미수행 점검과 반환 형식 누락만 단일 패스 범위에서 보완한다. 이미 발생한 순서·권한 경계 위반은 재실행으로 소급 충족하지 말고 미완료 사유를 반환한다”로 좁힌다. 반환 절에는 이 예외에 한해 계약 미충족 사유 1줄을 허용하고, producer 호출 시에는 해당 사유와 함께 복귀하도록 연결한다. 대상 부재는 기존 지정 1줄 종료를 그대로 유지한다.
- **유지할 계약:** 종료 전 자체 검증, 5 smell 점검, 사전 실재 대조, evidence 없는 완료 금지, 단일 패스, reviewer read-only, producer의 재호출 상한. 새 자동 재시도나 자동 원상복구는 추가하지 않는다.
- **소유자:** `plan-review`의 AC·반환 절. `feature-draft`는 계약 미완료 반환을 성공 gate로 세지 않는지 연결 확인이 필요하다. 고정 임계나 producer 소유권 변경은 필요 없다.
- **검증 상태:** 문면 간 충돌을 확인한 정적 finding. 실패 경로 실행은 미검증. 과거 위반을 완료로 승격하지 않는 오류 반환을 명시하는 보완이며, 게이트 구조 변경을 제안하지 않는다.

### plan-review-02 — Codex 배칭 문구를 공통 계약과 같은 지시형으로 정리할 수 있다 [정리 후보]

- **기준:** 2.
- **적용 runtime:** Codex; Claude는 대조 기준.
- **근거:** [Codex SKILL](../../../plugins/sdd-skills-codex/skills/plan-review/SKILL.md) 32행: “서로 독립인 파일 읽기·검색은 가능한 한 함께 배칭한다”. [Claude SKILL](../../../.claude/skills/plan-review/SKILL.md) 32행: “서로 독립인 Read/Grep은 **한 메시지에 배칭**한다”. [global spec](../../../_sdd/spec/main.md) 62행: “서로 의존하지 않는 read-only 호출의 한 메시지 배칭을 지시형으로 요구한다”.
- **문제 상황:** 다음 두 읽기 대상이 이미 확정되어 있고 서로 의존하지 않는 경우다. Codex 문구는 배칭을 지시하지만 ‘가능한 한’의 적용 조건과 묶는 단위를 별도로 설명하지 않는다. 이 표현이 실제 직렬 실행을 유발한다고 단정할 근거는 없다.
- **예상 영향:** runtime별 문구를 유지·검토할 때 같은 배칭 계약인지 해석해야 한다. 성능·지연 개선 수치는 주장하지 않는다.
- **최소 수정안:** Codex 첫 문장을 “서로 독립인 파일 읽기·검색은 한 메시지에 배칭한다”로 맞추고, 뒤의 결과 의존 호출 예외는 유지한다. 특정 tool 이름이나 새 도구 탐색 절차는 추가하지 않는다.
- **유지할 계약:** read-only 독립 호출만 배칭, 앞 결과로 대상이 정해지는 호출은 다음 턴, 읽기 범위 확대 금지. 의미를 새로 강화하기보다 이미 정해진 global 계약을 명료하게 표현하는 정리다.
- **소유자:** `plan-review` Codex mirror. 다른 리뷰 스킬에 같은 문구가 있는지 전수 변경하는 작업은 이 finding의 범위가 아니다.
- **검증 상태:** 문구와 global 계약을 정적 대조했다. 해당 표현의 실제 행동 효과는 측정하지 않았다.

## 런타임 차이와 의존성

- 양쪽 SKILL 전문을 확인했다. 자체 reference 파일은 없으며 두 본문이 전체 계약을 소유한다.
- Claude의 Read/Grep과 dispatch 용어를 Codex의 일반 읽기·검색과 spawn으로 바꾼 점은 정당한 runtime 적응이다. Codex 도입부의 “custom agent”보다 AC4의 “agent spawn 없음”이 넓지만, AC4와 직접 수행 지시를 함께 읽으면 범용 subagent 허용으로 해석할 필요가 없다. 별도 finding을 만들지 않는다.
- `--model`·`--effort` 무시는 실제 dispatch 대상이 없는 현재 직접 실행 설계와 맞는다. runtime API의 지원 여부를 조사하거나 부재를 주장하지 않았다.
- [Claude feature-draft](../../../.claude/skills/feature-draft/SKILL.md)의 Process·Required Output·규칙·Integration을 확인했고, [Codex 짝](../../../plugins/sdd-skills-codex/skills/feature-draft/SKILL.md)은 diff로 본문 동일함을 확인했다. 108–112행에서 gate→fix, 최대 2회, 사용자 대기 없는 지속 계약이 reviewer 87행과 연결된다. gate의 Medium advisory와 producer의 Medium 반영 의무는 각각 implementation blocker 여부와 fix 정책을 뜻하므로 모순이 아니다.
- [global spec](../../../_sdd/spec/main.md) Guardrails 및 관련 §3 결정과 [components](../../../_sdd/spec/components.md)의 feature-draft 설명을 대조했다. `plan-review` 직접 실행·분할 금지 및 producer/verifier 소유권을 보존했다.
- 추가로 [spec-sync](../../../.claude/skills/spec-sync/SKILL.md)의 Input Sources와 [spec 정의](../../../docs/SDD_SPEC_DEFINITION.md)의 legacy draft 관련 검색 결과를 확인했다. legacy discovery의 전체 소비 체인은 검토하지 않았으며, 이번 finding으로 확대하지 않았다.
- `implementation`, `spec-review` 전체 실행 계약과 실제 설치 runtime의 behavior는 미검토다. 이 문서는 두 스킬의 독립 리뷰를 대신하지 않는다.

## 권장 처리 순서와 검증

1. `plan-review-01`의 실패 처리만 AC와 반환에 좁게 반영하고 양 runtime을 맞춘다. 정상 완료·대상 부재·사전 대조 누락을 각각 입력으로 삼아, 정상 반환은 기존 형식이고 과거 위반은 재점검 없이 미완료로 표시되는지 확인한다. dispatch 위반은 실제 금지 행동을 실행하지 않고 해당 이력이 주어진 재개 fixture로 확인한다.
2. `feature-draft` gate 호출에서 정상 반환 직후 fix가 이어지고, 계약 미완료를 성공으로 오인하지 않는지 확인한다. gate 횟수와 임계는 그대로 둔다.
3. `plan-review-02`는 같은 수정에서 문장 하나만 정리한다. diff와 `git diff --check`로 변경 범위를 확인한다. 행동 효과를 주장하려면 대상 설치본이 로드된 새 세션의 실제 읽기 호출을 따로 관측한다.

이번 리뷰에서는 대상 스킬 실행, runtime 실험, 스킬 수정, global spec 수정은 하지 않았다. 제안 문서의 형식·링크·파일 권한만 확인한다.
