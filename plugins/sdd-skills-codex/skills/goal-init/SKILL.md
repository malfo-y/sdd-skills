---
name: goal-init
description: This skill should be used when the user asks to set up a "/goal", "goal 조건", "goal init", "goal-init", "set up goal", "goal helper", "goal 설정", "goal 목표", wants to craft a good `/goal` completion condition, or to scaffold the 4-file goal harness for a native `/goal` loop. Conversational helper that crafts the condition string and harness; it does not invoke `/goal` itself.
---

# Goal Init

## Goal

네이티브 `/goal`에 사용할 자족적 완료조건과 4파일 실행 하네스를 대화형으로 준비한다. 사용자가 이미 제공한 목표·접근·제약은 재사용하고, 결과를 바꿀 미확정 정보만 확인한다. 질문은 활성 런타임의 질문 수단을 사용하며 메인 루프가 직접 수행한다.

## Boundaries

- setup은 조건·하네스 준비와 Handoff까지다. `/goal` 활성화는 사용자가 한다. 기존 goal 상태를 조회·변경하거나 active goal 때문에 setup을 막지 않는다.
- `preset=sdd`는 하네스의 Loop Protocol만 선택한다. setup 중 feature-draft·implementation·spec-sync나 initial feature를 실행하지 않는다.
- 산출물은 `_sdd/goal/<YYYY-MM-DD>_<slug>/`의 `goal.md`·`experiments.md`·`journal.md`·`report.md`다. 다른 경로의 산출물이나 ralph의 bash 루프·run.sh·컨테이너를 추가하지 않는다. 상위 하네스의 work log는 그 규약을 따른다.

## Decision Criteria

대화 순서는 상황에 맞게 정한다. 다음 기준을 충족하는 데 이미 충분한 정보가 있으면 추가 질문이나 형식적인 단계 전이 없이 하네스를 작성한다.

- **적합성**: transcript의 증거로 종료 상태를 판정할 수 있는 멀티턴 작업이어야 한다. 단발 작업이면 그 사실을 안내한다. 종료 상태가 모호하면 구체화를 돕고, 끝내 정할 수 없으면 setup 미완료로 종료한다.
- **자율 수준 확정**: 이미 확정한 수준·승인/제외 범위는 재사용한다. 수준이 미정일 때 사용자 원문에 자율 수행 신호("알아서", "자율", "무인", "확인 없이", "묻지 말고" 등)가 있으면 `unattended`로 확정하고 되묻지 않는다. 수준도 신호도 없으면 활성 런타임에서 허용하는 질문 수단으로 1회 확인해 `unattended`(권장) | `attended`를 정한다. 승인 질문을 허용하는 전용 도구가 없으면 일반 대화로 묻고 답을 기다린다. 무응답을 승인으로 해석하지 않는다. 사용자가 사전 승인/제외 목록(템플릿 기본값)을 조정하면 반영한다.
- **접근 선택**: 원인이나 해결 경로가 열려 있으면 구별되는 가설·검증법·트레이드오프를 비교하고 권장안을 제시한다. 접근이 확정돼 있으면 선택된 접근과 남은 불확실성만 기록한다. 가설 수를 채우기 위해 대안을 만들지 않는다. Generic 루프에는 실행 가능한 다음 시도가 있어야 하며, SDD 루프의 접근 후보는 미충족 목표에서 다음 feature를 선택하는 데 참고한다.
- **완료조건과 실행의 분리**: outcome은 조건 문자열에, 검증 명령·기대 출력·수치 임계 등 실행 세부사항은 `goal.md`의 검증 레시피에, 루프 행동은 Loop Protocol에 둔다. 세부사항이 현실과 달라졌을 때 목표를 다시 정해야 하면 조건에, 검증 방법만 바꾸면 되면 레시피에 둔다.

## Condition Self-check

조건 문자열은 `DONE WHEN`(outcome과 위조 어려운 anchor 1–2개), `CONSTRAINTS`(제약·레시피 drift 가드·위임), `STOP`(무진척 종료 경계)으로 작성한다. template의 표준 증명·제약 문구를 사용하고 다음을 모두 확인한다.

1. 도구 없이 transcript만 보는 평가자가 목표 달성 여부를 판정할 수 있다.
2. 매 턴 허용된 검증의 실제 출력 또는 기존 evidence의 유효성·미실행 사유를 표시하고, 최종 PASS에는 모든 필수 검증의 유효한 증거를 요구한다.
3. 조건 문자열이 4,000자 이하다.

미충족이면 조건을 보완한다. 입력·환경 부족으로 해결할 수 없으면 누락과 필요한 다음 조치를 알리고 미완료로 종료한다.

## Harness Setup

목표·권한·검증 기준이 정해졌으면 작성 직전에 `references/harness-templates.md`를 읽고 4파일을 만든다. template의 슬롯·반복 규칙을 따르며, 선택한 Loop Protocol payload를 정확히 하나 적용한다.

- `goal.md`: 조건 문자열, 검증 레시피, 확정한 자율 수행 위임, generic 또는 `preset=sdd` Loop Protocol, 아래 Handoff의 자기 런타임 실행법.
- `experiments.md`: 선택한 접근과 필요한 가설을 검증 방법과 함께 기록한다. 항목 수는 실제 다음 시도에 맞춘다.
- `journal.md`: append-only 기록의 초기 구조.
- `report.md`: 아직 목표 달성을 검증하지 않았음을 표시하는 초기 보고 구조.

## Handoff

조건 문자열 전문을 생략·요약 없이 별도 코드 블록으로 화면에 출력하고, 아래 실행법과 생성한 4파일의 개별 경로를 제시한다. `goal.md` 경로만으로 조건 문자열을 대신하지 않는다.

- **Codex 실행법**: (a) `codex features enable goals`(또는 config의 `features.goals`)로 goals 기능을 활성화한다. (b) 라이프사이클은 `set`(목표 설정)·`status`(진행 확인)·`clear`(종료)이며, 중간에 멈췄다 이어가려면 `pause`·`resume`를 쓴다. (c) continuation은 thread-scoped state로 유지되며, 안전 경계(turn 종료·idle·no queued input) 안에서만 다음 턴으로 이어진다. (d) 진행은 evidence-based다 — 매 턴 검증 레시피의 실행 경계에 따라 evidence를 대화에 surface하고, 평가자는 그 증거로 완료를 판정한다.
- setup 경계를 실제로 지켰으면 “goal을 활성화하지 않았으며 기존 goal 상태도 변경하지 않았다”를 명시한다. 위반이 있었다면 사실과 미충족 기준을 보고하며 성공으로 표시하지 않는다.

## Acceptance Criteria

- [ ] 목표·권한·접근 선택이 Decision Criteria에 부합하고 사용자 선호를 임의로 만들지 않았다.
- [ ] 조건 문자열이 Condition Self-check를 통과했다.
- [ ] 4파일이 Harness Setup 계약대로 생성됐고 선택한 preset과 자율 수행 위임이 반영됐다.
- [ ] Handoff의 조건 전문·런타임 실행법·개별 경로·실제 setup 상태를 전달했다.
- [ ] Boundaries를 지켰다.

## Final Check

완료 전에 적용되는 Acceptance Criteria를 한 번 점검한다. 수정 가능한 누락은 보완하고, 비대상·입력 부족·사용자 중단은 이유와 남은 일을 보고한다. 이미 발생한 경계 위반은 사후 수행으로 소급 충족하지 않는다.
