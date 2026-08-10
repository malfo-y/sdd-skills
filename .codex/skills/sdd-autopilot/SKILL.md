---
name: sdd-autopilot
description: "SDD goal harness 셋업 entrypoint. /sdd-autopilot으로 기능 목표를 goal-init(preset=sdd)에 전달해 4-file harness와 조건을 만들고, 사용자가 native goal을 직접 활성화하도록 안내한다."
---

# SDD Autopilot

## Goal

사용자의 기능 목표를 기존 `goal-init`의 SDD preset으로 전달하는 thin entrypoint다. 이 스킬은 구현을 시작하지 않고, SDD producer chain을 반복할 inert 4-file goal harness와 자족적 조건 문자열을 준비해 사용자 activation 경계에서 종료한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: 사용자 원문과 관련 context를 `goal-init(preset=sdd)`에 전달하고, `goal-init`의 기존 5단계·condition self-check·4파일 setup을 완료했다.
- [ ] AC2: 생성된 `goal.md`가 runtime-local `goal-init` template의 SDD Loop Protocol payload를 사용한다.
- [ ] AC3: setup 중 initial `feature-draft`·`implementation`·`spec-sync` 실행, current native goal status 조회, native goal 상태 변경이 모두 0건이다.
- [ ] AC4: 조건 문자열·runtime 실행법·4파일의 개별 경로·setup 불변식을 relay했고, native goal 활성화 여부와 시점은 사용자가 결정한다.

## Hard Rules

1. **Thin entrypoint**: goal intake·조건 self-check·harness shape·Loop Protocol payload의 단일 소스는 runtime-local `goal-init` package다. 이 스킬에 해당 본문을 복제하거나 변형하지 않는다.
2. **Setup only**: initial `feature-draft`·`implementation`·`spec-sync`를 호출하거나 코드를 수정하지 않는다. producer chain은 사용자가 활성화한 native goal의 SDD Loop Protocol만 실행한다.
3. **Native goal 불간섭**: `/goal`을 발동하지 않고 current goal status도 조회하지 않는다. existing goal을 set·clear·pause·resume·replace·merge하지 않으며 active goal 때문에 setup을 차단하지 않는다.
4. **원문 전달**: 사용자의 원래 요청과 관련 context 파일 경로를 `preset=sdd` 입력과 함께 `goal-init`에 전달한다. 의미를 잃을 정도로 축약하지 않는다.
5. 한국어를 기본으로 하되 사용자 언어를 따른다.

## Process

### Step 1: SDD preset 입력 구성

사용자의 기능 목표·제약·known context를 모아 `preset=sdd`를 명시한다. current native goal status는 수집하지 않는다.

### Step 2: goal-init 실행

active skill catalog에서 설치된 `goal-init`을 이름으로 선택해 `preset=sdd` 입력으로 수행한다. workspace-relative source-tree 경로를 가정하지 않는다. 기존 5단계와 모든 Decision Gate를 통과하고 4파일을 생성할 때까지 산출물 정의를 이 스킬에서 재구현하지 않는다.

### Step 3: Handoff relay

`goal-init`이 확정한 조건 문자열, Codex `/goal` 실행법, 생성한 `goal.md`·`experiments.md`·`journal.md`·`report.md`의 개별 경로를 사용자에게 제시한다. 마지막에 다음 사실을 그대로 표시하고 종료한다.

> goal을 활성화하지 않았으며 기존 goal 상태도 변경하지 않았다.

사용자가 내용을 검토한 뒤 native goal 활성화 여부와 시점을 직접 결정한다.

## Error Handling

| 상황 | 대응 |
|------|------|
| 목표가 `/goal` 적합성 gate를 통과하지 못함 | `goal-init`의 재정의 안내 또는 중단 결과를 그대로 relay한다. 단발 구현으로 자동 전환하지 않는다. |
| 4파일 setup 실패 | 실패를 보고하고 종료한다. producer 실행이나 native goal 발동으로 우회하지 않는다. |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
