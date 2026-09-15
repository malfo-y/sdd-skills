# discussion 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/discussion/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/discussion/SKILL.md)
- 판정 요약: 수정 필요 7 / 정리 후보 0 / 실행 검증 필요 0

## 역할과 유지할 계약

사용자와 읽기 전용 토론을 진행하고, 확인한 맥락·결정·미결 질문·후속 실행 항목을 요약 파일에 남긴다. 구현·스펙 수정 금지, 근거 유형 구분, 사용자의 종료 선택, 미결 사항을 해결된 사실로 승격하지 않는 경계, 런타임별 대화형 도구, 요약 템플릿의 단일 소스와 필수 섹션을 유지한다. work log 예외는 호출 환경의 규약에 한정된다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | discussion-02: 방향 고정 예외가 coverage 완료 조건에 연결되지 않음. discussion-03: 이미 명확한 토픽에도 질문 강제. |
| 2. 충돌과 우선순위 | discussion-01: 종료 선택지와 stagnation 분기 충돌. discussion-05: Codex 옵션 수 충돌. discussion-06: Claude 오류 복구와 정상 게이트 충돌. |
| 3. 확인·승인 경계 | discussion-03, discussion-04: 범위 및 종료 의사를 이미 명시한 입력에도 재확인 경로가 강제됨. |
| 4. 중복과 소유권 | discussion-01, discussion-05: question guide가 본문과 다른 실행 규칙을 소유함. 배포 mirror 자체는 결함으로 보지 않음. |
| 5. 완료·복구 조건 | discussion-02, discussion-06, discussion-07: 생략 상태·부분 완료·실제 값 치환 경계가 닫히지 않음. |
| 6. 절차의 필요성 | discussion-03, discussion-04: 답이 이미 주어진 특정 입력에서는 질문이 새 정보를 만들지 않음. 최소 1회 비판적 개입, 근거 유형, 필수 요약 섹션은 별도 결함 근거 없음. |

## Findings

### discussion-01 — 종료 선택지와 정체 복구의 지시가 서로 다름 [수정 필요]

- **기준 / runtime:** 2·4·5 / Claude·Codex.
- **근거:** [Claude 본문](../../../.claude/skills/discussion/SKILL.md) 25행은 `Step 3의 매 질문에 "토론 종료 / 정리해줘" 옵션을 반드시 포함한다.`라고 하지만 257행은 in-scope 미결이 있을 때 `"남은 미결 1개만 더 논의: [질문 요약]" 만`을 지시한다. [Codex 본문](../../../plugins/sdd-skills-codex/skills/discussion/SKILL.md) 32·224행에도 같은 충돌이 있다. [Claude guide](../../../.claude/skills/discussion/references/discussion-question-guide.md) 139·143행과 [Codex guide](../../../plugins/sdd-skills-codex/skills/discussion/references/discussion-question-guide.md) 174·178행은 요약 없는 `"미결 1개만 더 논의"`와 `요약 단계로 이동한다.`를 지시한다. 본문 252·260행 / 219·227행은 구체 질문 요약과 Gate 3→4 경유를 요구한다.
- **문제 상황:** in-scope 미결 1건이 반복 정체되어 fallback 질문을 만들 때 종료 선택지를 넣고 동시에 계속 선택지만 넣을 수 없다. guide를 그대로 쓰면 구체 질문 표시와 종료 게이트도 누락된다.
- **예상 영향:** 사용자의 종료 경로를 숨기거나, 반대로 미결 확인 게이트를 건너뛰는 상반된 경로가 문면상 열린다. 실제 행동은 관측하지 않았다.
- **최소 수정안:** fallback에도 `정리/종료 → Gate 3→4` 선택지를 둔다. guide의 fallback 실행 규칙은 본문 §3.5.1 포인터와 일치하는 질문 예시로 교체한다.
- **유지할 계약:** 종료 선택은 즉시 미결을 해결 처리하는 것이 아니다. Gate에서 미결을 보존하고 필요한 명시적 종료 동의를 받는 경계는 유지한다.
- **소유자 / 검증 상태:** discussion 본문과 question guide / 정적 충돌 확인, 실행 미검증. cross-skill 수정 불필요.

### discussion-02 — 방향 고정 시 대안 생략을 coverage가 수용하지 않음 [수정 필요]

- **기준 / runtime:** 1·2·5 / Claude·Codex.
- **근거:** [Claude](../../../.claude/skills/discussion/SKILL.md) 147행 / [Codex](../../../plugins/sdd-skills-codex/skills/discussion/SKILL.md) 114행: `사용자가 이미 명시적으로 특정 방향을 고정했다면 이 단계를 건너뛰고 바로 비판적 개입(3.2.2)으로 진행한다.` 같은 파일 151행 / 118행: `` `alternatives` 항목은 이 능동 제시가 수행되고 사용자 응답이 있은 뒤에만 완료로 표시한다. `` Claude 155행은 추가로 `3.2.1의 Alternatives Initiation이 완료된 뒤 수행한다.`라고 한다. 페이즈 판정은 Claude 130행 / Codex 97행의 미확인 coverage에 의존한다.
- **문제 상황:** 사용자가 “SQLite 사용은 확정했고, 이 선택의 운영 위험만 토론하자”고 명시하면 대안 제시를 생략해야 하지만 `alternatives`를 완료할 수 없다. Claude에서는 비판적 개입의 선행 조건도 충족되지 않는다.
- **예상 영향:** 고정한 선택을 다시 비교하거나, 분석 미완료로 남겨 추가 생략 확인을 요구할 수 있다.
- **최소 수정안:** 명시적으로 고정한 방향에는 `alternatives = skipped (사용자 지정)`를 기록하고 페이즈 판정에서 충족으로 취급한다. Claude의 비판적 개입 선행 조건을 “대안 제시 완료 또는 사용자 지정 생략 후”로 한정한다.
- **유지할 계약:** 방향이 열려 있으면 2–3안과 권장안을 제시한다. 고정한 방향도 비판적 검토를 수행하며 생략 사유를 보존한다.
- **소유자 / 검증 상태:** discussion coverage·대안 제시 절과 guide의 coverage 예시 / 정적 충돌 확인, 실행 미검증.

### discussion-03 — 토픽과 범위가 충분해도 시작 확인이 강제됨 [수정 필요]

- **기준 / runtime:** 1·3·6 / Claude·Codex.
- **근거:** [Claude](../../../.claude/skills/discussion/SKILL.md) 49–50행: `사용자 입력에서 토픽이 이미 명시된 경우:` / `토픽을 요약하여 확인 질문`. [Codex](../../../plugins/sdd-skills-codex/skills/discussion/SKILL.md) 52행: `사용자 요청에서 토픽이 이미 있으면 재진술 후 범위를 좁히는 질문 1개를 한다.` 두 버전의 Gate 1→2는 이미 `topic_defined AND scope_clear AND scope_is_atomic`을 판정한다(Claude 69행 / Codex 57행).
- **문제 상황:** “단일 서비스의 SQLite WAL 백업 방식만 토론하자. DB 선택과 배포는 제외하고 실패 복구부터 보자”처럼 주제·범위·제외·첫 논점이 모두 주어져도 확인 질문 또는 추가 범위 축소가 필요하다.
- **예상 영향:** 다음 행동을 바꿀 정보가 없는 확인 턴이 생기거나, 사용자가 지정한 범위를 불필요하게 더 좁힌다.
- **최소 수정안:** Gate 조건을 입력만으로 충족하면 범위를 한 문장으로 재진술하고 Step 2로 진행한다. 빠진 범위 결정이 있을 때만 그 한 가지를 질문한다.
- **유지할 계약:** 불명확한 범위의 보완과 scope atomicity 점검을 생략하지 않는다. 대화형 토론 자체를 자동 실행 작업으로 바꾸지 않는다.
- **소유자 / 검증 상태:** discussion Step 1 / 정적 불필요 질문 경로 확인, 실행 미검증.

### discussion-04 — 이미 분류·종료 승인된 미결도 다시 질문함 [수정 필요]

- **기준 / runtime:** 3·6 / Claude·Codex.
- **근거:** [Claude](../../../.claude/skills/discussion/SKILL.md) 266·272·278행 / [Codex](../../../plugins/sdd-skills-codex/skills/discussion/SKILL.md) 233·237·243행은 미결 1건 이상이면 추가 논의 여부 확인 → `모든 미결 질문`의 카테고리 질문 → in-scope 잔존 시 `정말 그대로 종료하시겠어요?`의 경로를 지시한다. 반면 Claude 179행 / Codex 146행은 토론 중 `deferred-deliberately` 또는 `needs-data`로 이미 기록할 수 있게 한다.
- **문제 상황:** 사용자가 “Q1은 벤치마크가 없어서 needs-data로 남기고, 이 미결을 그대로 기록한 채 지금 종료하자”고 명시해도 동일한 Q1에 논의 여부·분류·종료 확인을 다시 요구한다.
- **예상 영향:** 미결의 존재와 결과를 이해한 종료 승인 후에도 같은 정보를 재입력해야 한다.
- **최소 수정안:** 기존 라벨과 명시적 종료 의사를 먼저 소비한다. 라벨이 없는 항목만 분류하고, 사용자가 아직 인지·동의하지 않은 in-scope 미결이 있을 때만 최종 확인한다. 새 미결이나 바뀐 라벨은 새로 확인한다.
- **유지할 계약:** 모든 미결의 분류·기록, 자동 추정 표시, in-scope 미결을 알고 종료한다는 명시적 사용자 동의. 무응답을 승인으로 간주하지 않는다.
- **소유자 / 검증 상태:** discussion Gate 3→4 / 정적 재확인 경로 확인, 실행 미검증. 기존 사용자 동의를 인정하는 문구 수정이며 종료 동의 계약 자체를 제거하는 제안이 아니다.

### discussion-05 — Codex 질문 개수가 아니라 선택지 계약이 맞지 않음 [수정 필요]

- **기준 / runtime:** 2·4 / Codex.
- **근거:** [본문](../../../plugins/sdd-skills-codex/skills/discussion/SKILL.md) 91행은 `옵션 2-3개 + "토론 종료"`를 지시한다. 237–241행은 미결별 `별도 단일선택 질문`에 네 종류 카테고리를 제시한다. 32행은 모든 질문에 종료 선택지도 요구한다. [guide](../../../plugins/sdd-skills-codex/skills/discussion/references/discussion-question-guide.md) 98행은 `옵션은 총 2-3개만 사용한다.`라고 제한한다. 이번 세션의 활성 `request_user_input`도 질문당 2–3개 선택지를 요구한다.
- **문제 상황:** 접근 3개를 제시하는 라운드에는 종료까지 4개, 카테고리 네 종류를 그대로 선택지에 넣으면 종료까지 5개가 된다. 호출당 질문을 최대 3개로 나누는 237행의 배치는 질문당 선택지 수 문제를 해결하지 않는다.
- **예상 영향:** 본문·guide를 동시에 지키는 payload를 만들 수 없다. 특정 런타임에서 실제 호출이 거부되었다는 주장은 아니다.
- **최소 수정안:** 일반 라운드의 총 옵션 수를 2–3개로 일치시킨다. 접근 3개는 본문에서 비교하고 질문은 권장안·대안 탐색·종료로 나눈다. 라벨 질문은 맥락상 가능한 라벨 최대 2개와 종료를 제공하고, 나머지 라벨은 자유 입력 또는 후속 질문으로 받는 식으로 활성 schema를 따른다. 네 카테고리의 의미는 유지한다.
- **유지할 계약:** 모든 미결에 한 카테고리, 대안의 충분한 설명, 종료 진입 경로, runtime-local question guide. Claude의 영구 도구 제한은 이번 검토에서 단정하지 않는다.
- **소유자 / 검증 상태:** discussion Codex adapter·question guide / 문면 및 현재 활성 schema 대조, 실제 호출 미검증.

### discussion-06 — Claude 오류 복구가 정상 게이트를 다시 요구할 수 있음 [수정 필요]

- **기준 / runtime:** 2·5 / Claude.
- **근거:** [본문](../../../.claude/skills/discussion/SKILL.md) 69행은 명확하고 atomic한 토픽만 Step 2에 진입시킨다. 301행은 `최대 2라운드 질문 후 자유 주제로 진행`한다. 303행은 `사용자 응답 없음/중단`에 `현재까지의 토론 내용으로 부분 요약 생성`을 지시한다. 27행은 in-scope 미결의 Gate 외 종료를 금지하고, 278행은 명시적 종료 동의를 요구한다. 17행의 최소 1라운드 AC와 320행의 `미충족 항목이 있으면 해당 단계로 돌아가 수정한다.`에는 부분 산출물 예외가 없다.
- **문제 상황:** 두 번 물어도 토픽을 정하지 못하거나, 사용자가 첫 라운드 전에 중단하면 오류 표는 진행·부분 저장을 요구하지만 토픽 게이트와 완료 AC를 만족할 수 없다. 토론 중 in-scope 미결을 남긴 채 응답이 끊긴 경우에는 부분 요약과 명시 종료 동의의 관계도 불명확하다.
- **예상 영향:** 오류 복구를 위해 생성한 부분 요약을 정상 완료로 오인하거나, 사용자가 중단한 토론을 다시 시작해 AC를 채우려는 경로가 생긴다.
- **최소 수정안:** 토픽 미확정 시 자유 주제로 진행하려면 사용자 선택을 받도록 하고, 그렇지 않으면 미완료로 종료한다. 응답 중단의 부분 요약은 `중단/미완료` 상태와 미충족 AC를 기록하는 저장 동작으로 정의하여 정상 완료·미결 종료 승인과 구별한다. Final Check의 복귀는 복구 가능한 정상 진행 상황에 한정한다.
- **유지할 계약:** 부분 맥락 보존, 사용자 중단 존중, 증거 없는 AC 완료 금지. 정상 토론 종료의 in-scope 확인 게이트는 유지한다.
- **소유자 / 검증 상태:** discussion Claude Error Handling·Final Check / 정적 경계 충돌 확인, 실행 미검증. Codex는 토픽 미정 2라운드 후 중단을 명시하므로 동일 토픽 finding에 포함하지 않는다.

### discussion-07 — 슬롯만 치환하라는 템플릿에 비슬롯 예시 값이 남아 있음 [수정 필요]

- **기준 / runtime:** 2·5 / Claude·Codex.
- **근거:** [Claude 본문](../../../.claude/skills/discussion/SKILL.md) 293행 / [Codex 본문](../../../plugins/sdd-skills-codex/skills/discussion/SKILL.md) 261행: `Read 후 코드블록을 verbatim 복사`하고 `` `[...]` 슬롯만 치환한다 ``. byte-identical한 [Claude template](../../../.claude/skills/discussion/references/summary-template.md) / [Codex template](../../../plugins/sdd-skills-codex/skills/discussion/references/summary-template.md)의 8–9행은 `YYYY-MM-DD`와 `N`, 26행은 `...`와 고정 `사용자 판단`, 37–38행은 고정 카테고리·의존 관계, 45행은 `...`와 `High/Medium/Low`다.
- **문제 상황:** 결정 근거가 코드 확인이고 미결이 없거나 3개 이상인 토론을 요약하려면 대괄호 슬롯 외의 예시 값·행 수도 바꿔야 한다. 슬롯만 바꾸는 literal 해석으로는 실제 날짜·결정·미결 목록을 온전히 표현할 수 없다.
- **예상 영향:** 예시 행이 실제 미결처럼 남거나, 반대로 모델이 문면을 어겨 템플릿을 암묵적으로 재해석해야 한다. 실제 placeholder 잔존은 관측하지 않았다.
- **최소 수정안:** 예시 값을 모두 명시적 슬롯으로 바꾸고 반복 행·빈 목록의 치환 규칙을 한 곳에 정의한다. 필수 제목은 유지하되 행 수는 실제 항목 수를 따른다고 명시한다.
- **유지할 계약:** Step 4에서 runtime-local 템플릿을 읽고 필수 섹션을 보존하는 계약. [components.md](../../../_sdd/spec/components.md) 37행에도 슬롯 치환 방식이 있으므로 문구의 의미를 바꾸는 방식이면 supporting spec을 함께 정합화한다. 권장안은 기존 슬롯 방식에 템플릿을 맞추므로 global 설계 변경은 필요 없다.
- **소유자 / 검증 상태:** discussion summary-template와 본문의 소비 지시 / 정적 불일치 확인, 생성 실행 미검증.

## 런타임 차이와 의존성

- Claude는 리서치 subagent를 지정하고, Codex는 로컬·웹 탐색을 직접 기술한다. 이는 정당한 runtime adaptation으로 보며 다름 자체를 finding으로 삼지 않았다. 하위 agent의 실제 권한·모델·lifecycle 지원 여부는 검증하지 않았다.
- Codex의 interactive-only와 도구 미노출 시 중단은 명시적 계약이다. 현재 `request_user_input`이 노출되어 있으므로 “Codex에서 대화형 도구를 사용할 수 없다”는 결론을 내리지 않았다.
- 읽은 직접 reference: 양쪽 `references/summary-template.md` 전문과 `references/discussion-question-guide.md` 전문. summary-template은 byte-identical이고 question guide는 런타임에 맞게 다르다.
- 기준 문서: `AGENTS.md`, `_sdd/env.md`, `_sdd/spec/main.md`의 관련 Guardrails·결정·운영 제약, `_sdd/spec/components.md` discussion 및 interactive surface 행, 공통 review-criteria.
- 미검토 범위: human reference로 명시된 `examples/sample-discussion-session.md`, 후속 `feature-draft`·`spec-create` 전문, 과거 토론 로그·실행 transcript. 본문은 후속 스킬을 자동 실행하지 않으며 요약이 입력 경계이므로 이번 finding에 후속 스킬 내부 분석은 필요하지 않았다.
- cross-skill 소유자: 없음. discussion-07의 supporting spec 행은 문구 정합화 시 문서 소유자와 함께 확인할 연결점이다.

## 권장 처리 순서와 검증

1. 종료 분기와 guide를 한 계약으로 맞추고, 기존 종료 동의를 재사용한다(discussion-01·04). in-scope 미결이 있어도 종료 선택은 Gate에 도달하고, 승인하지 않은 미결은 자동 완료되지 않아야 한다.
2. 방향 고정·명확한 입력·부분 중단을 독립 시나리오로 처리한다(discussion-02·03·06). 명확한 토픽에는 재확인을 하지 않고, 생략 coverage와 미완료 상태를 사실대로 기록해야 한다.
3. Codex 선택지 수와 템플릿 슬롯을 정합화한다(discussion-05·07). 활성 schema에 맞는 질문 payload와 실제 항목 수·근거 유형의 요약이 나와야 한다.
4. 변경 후 `git diff --check`와 양 runtime 문면 대조를 하고, 검토된 변경이 로드된 별도 세션에서 위 입력 시나리오를 실행한다. 요약 파일 및 transcript로 중복 질문, Gate 경유, 라벨 보존, 미완료 표시, placeholder 잔존 여부를 확인한다.

이번 리뷰는 대상 스킬을 실행하지 않았다. 모든 finding은 문면·현재 schema의 정적 대조 결과이며 실제 모델 행동, 시간 절감, 개선 효과는 미검증이다.
