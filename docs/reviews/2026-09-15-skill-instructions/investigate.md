# investigate 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/investigate/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/investigate/SKILL.md)
- 판정 요약: 수정 필요 2 / 정리 후보 1 / 실행 검증 필요 0

## 역할과 유지할 계약

단발 문제의 증거를 수집하고 근본원인과 영향 범위를 설명하는 스킬이다. 넓고 모호한 탐색만 read-only leaf로 나누며, 원인 종합과 수정·검증은 메인 루프가 소유한다. 초기 수정 범위, spec 파일 불가침, 수정 전 영향 평가, fresh verification을 유지한다.

Codex의 diagnose-only/fix 구분은 의도된 런타임 차이다. [components.md](../../../_sdd/spec/components.md) 54행이 Claude에는 이 경계를 적용하지 않았다고 명시하므로 단순 parity 누락으로 판정하지 않았다. Codex에서는 명시적 수정 요청 또는 후속 승인을 보존하고, 근거 없는 확정이나 제품 수정을 막아야 한다.

## 기준별 판정

| 기준 | 판정과 근거 |
| --- | --- |
| 1. 적용 조건 | 수정 필요 없음. 단발 조사와 장시간 반복 프로세스를 구분하며, Codex는 intent별 실행 단계와 AC 적용 범위를 명시한다. |
| 2. 충돌과 우선순위 | investigate-01: Claude의 허용된 `UNTESTED` 경로가 종료 AC와 충돌한다. investigate-03: Codex fallback 설명의 소유권을 정리할 수 있다. |
| 3. 확인·승인 경계 | 수정 필요 없음. Codex는 이미 명시된 수정 요청을 fix mode 권한으로 인정한다. 런타임이 추가 위임 승인을 요구하는 경우에만 별도 질문하도록 제한한다. |
| 4. 중복과 소유권 | investigate-02: 대화 맥락 추출은 있으나 leaf 전달 의무가 빠졌다. investigate-03: fallback 조건은 Runtime Adapter를 단일 기준으로 삼을 수 있다. |
| 5. 완료·복구 조건 | investigate-01: 검증 불가 상태를 성공으로 승격하지 않으면서 반환할 경로가 필요하다. Codex는 `UNCONFIRMED`, mode별 AC, fan-out remaining 처리를 명시한 점이 다르다. |
| 6. 절차의 필요성 | 수정 필요 없음. 여섯 단계는 증거→원인→영향→수정→보고로 목적이 구분되고, fan-out과 fix 단계는 조건부다. 가설 lane의 독립 탐지 하나는 선택한 anti-anchoring 방식의 일부이므로 수만으로 결함 판정하지 않았다. |

## Findings

### investigate-01 — Claude의 UNTESTED 예외로는 Final Check를 끝낼 수 없다 [수정 필요]

- 기준: 2, 5
- 적용 runtime: Claude
- 근거: [Claude SKILL](../../../.claude/skills/investigate/SKILL.md) 17행 `AC2: 수정 후 테스트가 통과한다 (Fresh Verification)`; 28행 `_sdd/env.md 미존재 시 코드 분석 기반 검증을 허용하되, 리포트에 UNTESTED 표기`(원문의 `UNTESTED`는 코드 서식); 80행 `미충족 항목이 있으면 해당 단계로 돌아가 수정한다.`
- 문제 상황: `_sdd/env.md`가 없고 실행 가능한 테스트 환경도 없는 저장소에서 원인 수정 후 허용된 코드 분석을 수행했다. 보고 상태는 `UNTESTED`지만 AC2의 테스트 통과는 충족할 수 없다. Final Check는 재진입만 요구하고, 외부 검증 조건이 바뀌지 않는 경우의 반환은 정의하지 않는다.
- 예상 영향: 허용된 예외를 따른 작업도 반복 수정·검증으로 돌아가거나, 종료하려고 실행하지 않은 테스트를 통과로 취급하는 문면상 압력이 생긴다. 실제 반복이나 허위 통과를 관측한 것은 아니다.
- 최소 수정안: 자체 검증을 유지하되, 코드 수정으로 해결할 수 없는 검증 제약은 `UNTESTED`와 필요한 환경·잔여 검증을 보고하고 반환하도록 Final Check에 한 분기를 둔다. AC2는 미충족으로 남기며 성공 완료로 표시하지 않는다. 실행 가능한 실패 테스트는 기존 수정·fresh verification 경로로 돌아간다.
- 유지할 계약: fresh evidence, 증거 없는 PASS 금지, 잔여 이슈 명시. `UNTESTED`를 성공으로 인정하자는 제안이 아니다.
- 소유자: `investigate` Claude 본문의 AC·Final Check. cross-skill 변경 불필요.
- 검증 상태: 정적 문구 대조 완료 / 동작 미검증. 기존 [global spec](../../../_sdd/spec/main.md) 70행의 명시적 잔여 이슈 보고 허용과 일치하는 보완이며 새로운 성공 기준을 도입하지 않는다.

### investigate-02 — 대화에서 추출한 조사 맥락을 leaf에 전달하는 계약이 없다 [수정 필요]

- 기준: 4
- 적용 runtime: Claude, Codex
- 근거: [Claude SKILL](../../../.claude/skills/investigate/SKILL.md) 36행 및 [Codex SKILL](../../../plugins/sdd-skills-codex/skills/investigate/SKILL.md) 53행 `이 입력은 대화에서 태어나므로 sub-agent가 못 읽는다 — orchestrator가 직접 정리한다.`; Claude 44–47행과 Codex 65–68행은 lane 분할만 지시한다. Codex 21행의 dispatch 예시는 `fork_turns: "none"`와 `<구체적 read-only 탐색 질문 + read-only 경계>`만 제시한다. [global spec](../../../_sdd/spec/main.md) 68행은 `dispatch되는 leaf에는 입력이 대화에서 태어난 맥락을 digest로 forwarding해야 한다`고 명시한다.
- 문제 상황: 사용자가 대화에서만 재현 조건과 이미 배제한 가설을 제공했다. 메인은 이를 Step 1에서 정리했으나 Step 2의 lane별 질문만 보낸다. 특히 Codex의 `fork_turns: "none"`에서는 해당 정보가 파일에 없다면 leaf가 별도로 복구할 수 없다. 현재 지시는 메인의 정리만으로 충족 가능하고 전달까지 요구하지 않는다.
- 예상 영향: leaf가 이미 배제한 가설을 재검토하거나 다른 재현 조건으로 증거를 수집할 수 있다. 원인 판정 실패를 실측한 것은 아니지만, 필수 입력 전달이 빠지는 실행 경로는 문면상 존재한다.
- 최소 수정안: Step 2의 dispatch 지시에 한 문장으로 “각 lane에 Step 1에서 정리한 관련 증상·재현 조건·기대 동작·이미 시도한 가설과 scope를 짧은 digest로 전달한다”를 추가하고, Codex 예시의 message 자리표시자도 이를 포함한다. 전체 대화·장문 리포트 복사는 요구하지 않는다.
- 유지할 계약: 필요한 경우만 fan-out, leaf read-only, 역할별 탐색 분리, 종합·수정은 메인 소유, `fork_turns: "none"` lifecycle.
- 소유자: 양 runtime `investigate` Step 2와 Codex dispatch 예시. 상위 digest 원칙은 global spec이 이미 소유하며 새 공용 reference나 다른 스킬 수정은 필요 없다.
- 검증 상태: 정적 계약 누락 확인 / 동작 미검증. 대화에만 있는 재현 조건을 실제 dispatch payload가 전달하는지 후속 실행에서 확인할 수 있다.

### investigate-03 — Codex fallback 조건을 Runtime Adapter 한 곳으로 모을 수 있다 [정리 후보]

- 기준: 2, 4
- 적용 runtime: Codex
- 근거: [Codex SKILL](../../../plugins/sdd-skills-codex/skills/investigate/SKILL.md) 16행 `agent_type 부재만으로는 degrade하지 않으며`와 70행 `런타임에 explorer 역할이 미가용하면 순차 인라인 증거 수집으로 graceful degrade`(원문의 `agent_type`, `explorer`는 코드 서식).
- 문제 상황: lifecycle 도구는 있고 `agent_type` 필드만 없는 schema를 읽는 경우다. Adapter는 framed-message generic leaf를 쓰도록 명확히 정하지만 Step 2에는 별도로 “역할 미가용”이라는 표현이 남아 있다. 이 표현이 전체 dispatch 불가를 뜻한다면 동일 규칙의 중복이고, 전용 role selector 부재로 읽히면 다른 fallback을 암시한다.
- 예상 영향: 유지보수 시 조건이 다시 어긋날 여지가 있다. 현재 Adapter가 `agent_type` 부재를 명시적으로 제외하므로 확정적인 모순이나 실제 dispatch 생략으로 판정하지 않았다.
- 최소 수정안: 70행의 첫 문장을 “fan-out 가능 여부와 fallback은 Codex Runtime Adapter를 따른다”로 대체한다. 단순 버그의 인라인 조건은 그대로 둔다.
- 유지할 계약: active schema 기반 lifecycle 선택, optional role selector, 불완전 lifecycle에서만 인라인 fallback. 기능·완료 기준 변경 없음.
- 소유자: `investigate` Codex Step 2. cross-skill 변경 불필요.
- 검증 상태: 동등한 포인터 문구 제안 / 동작 미검증. 이번 활성 schema의 모양을 영구 런타임 지원 범위로 일반화하지 않았다.

## 런타임 차이와 의존성

- Claude는 단발 수정 흐름, Codex는 diagnose-only/fix 흐름과 추가 보고 필드를 가진다. 이 차이는 [components.md](../../../_sdd/spec/components.md) 31·54행이 의도한 계약이다. 통일하려면 별도 spec 결정이 필요하며 이번 최소 수정안에 포함하지 않는다.
- Codex는 mailbox와 target/close adapter 및 remaining set을 소유한다. Claude의 도구 표현이 다르다는 사실만으로 같은 adapter 추가를 요구하지 않았다.
- 두 SKILL 전체와 [AGENTS.md](../../../AGENTS.md), [main.md](../../../_sdd/spec/main.md)의 관련 guardrail·실행 분리·운영 제약, [env.md](../../../_sdd/env.md), [components.md](../../../_sdd/spec/components.md)의 investigate 및 platform-only 항목, [공통 리뷰 기준](./review-criteria.md)을 읽었다. 대상 디렉터리에는 별도 reference 파일이 없다.
- `ralph-loop-init`은 장시간 반복 프로세스의 대안으로만 언급되며 본 스킬이 호출하지 않는다. 그 구현, 호스트 Explore 도구의 실제 권한, 설치본 runtime, 실제 조사 transcript는 미검토다. 이 범위의 미검토를 기능 부재로 판정하지 않았다.

## 권장 처리 순서와 검증

1. Claude Final Check에 `UNTESTED` 잔여 보고 반환을 명시한다. 테스트 환경이 없는 입력과 실제 실패 테스트가 있는 입력을 구분하여 전자는 미검증 상태로 반환하고 후자는 수정·재검증으로 이어지는지 확인한다.
2. 양 runtime의 leaf 입력에 관련 대화 digest를 결속한다. 파일에는 없는 재현 조건·이미 배제한 가설을 준 뒤, 실제 dispatch payload에 포함되는지 확인한다. 단순 단일파일 문제에서는 fan-out이 없어야 한다.
3. Codex Step 2의 fallback 설명을 Adapter 포인터로 정리한다. lifecycle은 유효하지만 role selector가 없는 경우에는 generic framed-message leaf를, lifecycle이 불완전한 경우에는 인라인 탐색을 선택하는지 확인한다.

이번 리뷰에서는 스킬 실행·수정·설치본 갱신을 하지 않았다. 후속 문구 변경은 diff와 `git diff --check`로 확인하고, 행동 검증은 변경한 계약이 실제 로드된 설치본과 새 세션에서 수행해야 한다.
