---
name: guide-create
description: This skill should be used when the user asks to "guide create", "create guide", "feature guide", "write guide", "가이드 작성", "기능 가이드", "가이드 문서 만들어줘", or wants to generate an implementation/review guide document for a specific feature from spec and code context.
---

# guide-create

## Goal

spec과 code evidence를 바탕으로 특정 feature의 deep-dive 기술 가이드를 `_sdd/guides/<YYYY-MM-DD>_guide_<slug>.md`에 만든다. guide는 global spec을 대체하지 않고 사용 시나리오, interface, 구현·리뷰 판단을 기능 단위로 구체화한다.

## Acceptance Criteria

- [ ] target feature, scope, output slug를 결정했다.
- [ ] 관련 spec context와 code/test/interface evidence를 수집했다.
- [ ] 확인된 claim을 source citation과 연결하고 unknown/assumption을 구분했다.
- [ ] runtime-local output interface의 fenced skeleton과 rubric을 적용했다.
- [ ] feature마다 별도 guide를 생성했다.
- [ ] `_sdd/spec/`, code, config, test를 수정하지 않았다.

## SDD Lens

- guide는 feature-specific companion document이며 global spec의 새 source of truth가 아니다.
- spec은 purpose/boundary/decision의 primary source이고 code는 concrete behavior의 근거다.
- 확인되지 않은 behavior는 사실처럼 채우지 않는다.

## Hard Rules

1. 생성 가능한 파일은 `_sdd/guides/<YYYY-MM-DD>_guide_<slug>.md`뿐이며 `_sdd/spec/`, application code, config, test는 read-only다.
2. 문서 언어는 사용자 지정을 우선하고, 없으면 existing spec/docs를 따른다.

## Input Sources

1. 사용자 요청
2. `_sdd/spec/main.md` 또는 project index
3. target feature에 연결된 split/supporting spec
4. 관련 code, test, interface, type, schema, config
5. 실행·검증 맥락이 실제로 필요할 때만 `_sdd/env.md`

## Process

### Step 1: Identify Feature and Output

- target feature와 boundary를 고른다.
- slug는 lowercase snake_case로 만든다.
- 여러 feature면 output path를 feature별로 열거하고 첫 파일부터 순서대로 완료한다.
- feature 또는 scope를 바꾸는 ambiguity가 남으면 질문 한 번으로 닫는다.

### Step 2: Gather Spec Context

feature의 problem, value, scope, guardrail, decision을 관련 spec에서 수집한다. usable spec가 없으면 근거 한계를 알리고 spec 생성 권장 또는 assumption을 명시한 진행 중 현재 요청에 맞는 쪽을 고른다.

### Step 3: Gather Code Evidence

관련 implementation, test, interface, type/schema를 찾아 exact path와 symbol 중심의 evidence index를 만든다. 구현 상태는 confirmed, partial, spec-only로 구분한다.

### Step 4: Resolve Evidence Gaps

- name/value gap은 user phrase와 spec에서 해결한다.
- implementation detail gap은 repository convention과 확인된 code를 우선한다.
- 근거가 없는 API, error, scenario, invariant는 만들지 않고 unknown/assumption으로 표시한다.

### Step 5: Load the Output Interface and Write

작성 직전에 runtime-local `references/output-format.md`를 **Read**한다. 그 reference의 fenced required skeleton을 verbatim 복사해 heading·field order를 유지하고 source evidence로 slot을 채운다. 근거 없는 optional appendix는 제거하고, schema·citation·confidence 판단은 reference rubric을 적용한다. reference 내용을 기억이나 이 본문으로 재구성하지 않는다.

장문이면 main loop가 skeleton을 먼저 저장하고 section slot을 순서대로 채운 뒤 placeholder를 제거해 finalize한다. 여러 feature면 현재 파일의 검증까지 끝낸 후 다음 파일로 간다.

### Step 6: Verify and Save

- output directory를 준비한다.
- `<YYYY-MM-DD>_guide_<slug>.md`에 저장한다.
- output interface와 Acceptance Criteria를 대조한다.
- 생성 경로와 evidence 한계를 보고한다.

## Output Contract

- `_sdd/guides/<YYYY-MM-DD>_guide_<slug>.md`
- 여러 feature면 feature당 한 파일

## Error Handling

| 상황 | 대응 |
|---|---|
| usable spec 없음 | spec 생성 권장 또는 명시적 assumption을 둔 제한적 guide |
| code evidence 부족 | unsupported claim을 쓰지 않고 한계를 표시 |
| 기존 같은 날짜/slug 파일 존재 | overwrite하지 않고 더 구체적인 slug 사용 |

## Final Check

Acceptance Criteria를 모두 만족하고 allowed output 외 repository surface가 수정되지 않았는지 확인한다.
