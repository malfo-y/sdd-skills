# ralph-loop-init 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/ralph-loop-init/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/ralph-loop-init/SKILL.md)
- 판정 요약: 수정 필요 5 / 정리 후보 0 / 실행 검증 필요 0

## 역할과 유지할 계약

장기 실행 작업을 위한 `ralph/` 7파일과 결과 디렉터리를 메인 루프가 직접 생성하고, 생성물의 구조·문법·슬롯을 검증하는 초기화 스킬이다. 생성된 자동화 루프는 격리 환경에서 실행하며, 성공 판정은 초기화 시 확정한 `verify.sh`에 고정한다. 짧은 세션 내 반복과 장기 무인 루프의 경계, 최소 범위 초기 실행, 검증 명령 미확정 시 중단, 상태·결정 기록, 모든 종료 경로의 근거 보고서 의무를 유지한다.

아래 템플릿 finding은 스킬이 생성하도록 지시한 실행 순서를 정적으로 대조한 결과다. 실제 CLI나 루프를 실행하여 관측한 결함으로 주장하지 않는다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | ralph-loop-init-03: phase 이름 변경 허용 범위가 템플릿의 고정 시작·종료 이름보다 넓다. 장기 작업 진입 조건과 검증 명령 hard gate 자체는 명확하다. |
| 2. 충돌과 우선순위 | ralph-loop-init-02, 03, 04: 재시도 상한과 Final Check, 커스터마이즈 허용과 고정 이름, 실패 재시도와 DONE 빠른 종료의 우선순위가 맞지 않는다. |
| 3. 확인·승인 경계 | ralph-loop-init-01: Claude는 필요한 정보가 모두 확정된 경우에도 확인 요청을 요구한다. 검증 방법 미확정 시 확인은 유지해야 한다. |
| 4. 중복과 소유권 | 수정 필요 없음. 스킬 본문이 생성 템플릿·CHECKS의 단일 소유자이며, 배포 짝과 완료 체크리스트를 갖는 것 자체는 중복 결함이 아니다. |
| 5. 완료·복구 조건 | ralph-loop-init-02, 04, 05: 초기화 검증의 재시도 종료, 실패한 LLM 턴의 상태 복구, reset의 lock 경계에 빈틈이 있다. |
| 6. 절차의 필요성 | 수정 필요 없음. 발견→검증 방법 확정→파일 생성→구조 검증의 각 단계에 소비자가 있다. 템플릿 길이나 7파일 수만으로 축소를 권고하지 않는다. |

## Findings

### ralph-loop-init-01 — 확정된 초기화 요청에도 포괄 확인을 요구한다 [수정 필요]

- 기준: 3, 1
- 적용 runtime: Claude. Codex의 동등 단계는 조건부 확인이다.
- 증거: [Claude SKILL](../../../.claude/skills/ralph-loop-init/SKILL.md) 90–105행: “분석 결과 요약 테이블을 제시하고 사용자 확인을 요청한다”, “사용자가 확인하면 (또는 auto-proceed 가능하면) 다음 단계로 진행한다.” [Codex SKILL](../../../plugins/sdd-skills-codex/skills/ralph-loop-init/SKILL.md) 97–99행은 “핵심 정보가 비어 있으면 사용자 확인을 요청할 수 있다”와 검증 방법 hard gate를 분리한다.
- 문제 상황: 사용자가 진입점·검증 명령·판정 조건·환경을 명시하여 초기화를 요청하고, 발견 결과도 일치한다. Claude 본문은 다시 확인을 요청하라고 하면서 auto-proceed가 가능한 조건은 정의하지 않는다.
- 예상 영향: 정보가 충분하고 이미 승인된 생성 작업이 불필요한 확인 대기에서 멈추거나 런타임마다 다르게 진행된다.
- 최소 수정안: Step 2의 일반 확인을 “미확정 핵심 정보가 있을 때만 질문하고, 이미 확인된 내용은 요약 후 진행한다”로 좁힌다. 검증 명령 hard gate는 별도로 그대로 둔다.
- 유지할 계약: 명령어와 판정 조건을 확정하기 전 파일 생성으로 넘어가지 않는다. autonomous 경로에서 이를 확정할 수 없으면 `BLOCKED`다.
- 소유자: ralph-loop-init Claude Step 2. [components.md](../../../_sdd/spec/components.md) 39행의 “검증 방법 확정 사용자 확인 게이트”는 검증 방법이 확정되지 않은 경우의 게이트로 유지할 수 있어 새 spec 결정은 필요하지 않다.
- 검증 상태: 문구·런타임 짝 대조 완료. 실제 확인 요청 빈도는 미관측.

### ralph-loop-init-02 — 최대 2회 뒤에도 Final Check가 수정 단계로 되돌린다 [수정 필요]

- 기준: 2, 5
- 적용 runtime: Claude, Codex
- 증거: [Claude SKILL](../../../.claude/skills/ralph-loop-init/SKILL.md) 723·727·759행은 수정 후 재검증 “최대 2회”를 지시하지만 764행은 “미충족 항목이 있으면 해당 단계로 돌아가 수정한다.” [Codex SKILL](../../../plugins/sdd-skills-codex/skills/ralph-loop-init/SKILL.md) 대응 위치는 673·677·709·714행이다.
- 문제 상황: 문법 또는 CHECKS 검증이 두 번의 수정 후에도 실패한다. 상한 도달 시 잔여 문제를 보고하고 끝내는 분기가 없고, Final Check는 다시 해당 단계로 돌아가도록 요구한다.
- 예상 영향: 재진입 때 상한을 새로 세는 반복 또는 어느 규칙을 우선할지 임의 판단이 생긴다. 완료 요약에는 성공 형식만 있어 미완료 결과를 일관되게 반환할 경로도 약하다.
- 최소 수정안: Step 8에 동일 초기화 호출의 재시도 상한 소진 시 실패 항목·근거·생성된 파일 상태를 보고하고 미완료로 종료한다고 명시한다. Error Handling과 Final Check는 이 한 곳의 복구 규칙을 참조한다.
- 유지할 계약: 종료 전 AC 자체 검증과 가능한 수정은 수행한다. 실패한 항목을 체크 완료로 바꾸거나 verified 성공 요약을 출력하지 않는다. 최대 2회 자체는 유지한다.
- 소유자: ralph-loop-init 양 runtime의 Step 8·Error Handling·Final Check.
- 검증 상태: 상충 지시와 누락 분기를 정적으로 확인. 실제 모델의 무한 반복은 관측하지 않았다.

### ralph-loop-init-03 — phase 변경 허용이 고정된 SETUP·DONE까지 포함한다 [수정 필요]

- 기준: 1, 2
- 적용 runtime: Claude, Codex
- 증거: [Claude SKILL](../../../.claude/skills/ralph-loop-init/SKILL.md) 68행 “Phase 이름은 프로젝트에 맞게 변경 가능”, 265행 “허용 수정은 둘뿐이다” 뒤 `VALID_PHASES`·`ADJUST_PHASE`만 맞추도록 지시한다. 초기 상태는 318·705행에서 `phase: SETUP`, 종료 감지는 523·669행에서 `DONE`으로 고정돼 있다. [Codex SKILL](../../../plugins/sdd-skills-codex/skills/ralph-loop-init/SKILL.md) 대응 위치는 66·259·312·655·506·619행이다.
- 문제 상황: 프로젝트 용어에 맞춰 SETUP을 PREPARING, DONE을 COMPLETE로 바꾸고 허용된 두 변수만 맞춘다. 초기 `state.md`는 허용 phase 집합과 다르고, COMPLETE는 상태 검증에 통과해도 종료 감지에 걸리지 않는다.
- 예상 영향: 허용된 커스터마이즈를 따른 생성물이 정상 초기화·완료를 표현하지 못한다. AC2의 “커스터마이즈된 등가 집합”만으로는 이 불일치를 드러내지 못한다.
- 최소 수정안: 이름 변경 범위를 중간 처리 phase로 명시하고 `SETUP`·`DONE`은 예약 이름으로 유지한다. CHECKS에서 두 예약 이름의 보존을 확인한다. 새 시작·종료 변수 도입은 필요하지 않다.
- 유지할 계약: 실행·검증·조정 단계의 프로젝트별 이름 변경, `VALID_PHASES` 정합성, `ADJUST_PHASE` 멤버십, 고정 템플릿의 최소 수정.
- 소유자: ralph-loop-init 양 runtime의 State Machine Reference·AC2·Step 6. 현재 예시가 바꾸는 TRAINING/VALIDATING 등 중간 phase의 의미는 그대로다.
- 검증 상태: 허용 문구와 하드코딩된 소비 지점 대조 완료. 커스텀 phase 생성·실행은 미실시.

### ralph-loop-init-04 — 실패한 LLM 턴의 DONE 상태가 다음 회차에서 완료로 처리된다 [수정 필요]

- 기준: 2, 5
- 적용 runtime: Claude, Codex
- 증거: [Claude SKILL](../../../.claude/skills/ralph-loop-init/SKILL.md) 601–615행의 `LLM_EXIT` 실패 분기는 백업 복원 없이 `continue`한다. 523–525행은 상태가 DONE이면 곧바로 `break`한다. final report와 PASS 검증은 669–691행에만 있다. [Codex SKILL](../../../plugins/sdd-skills-codex/skills/ralph-loop-init/SKILL.md) 대응 위치는 556–569·506–508·619–640행이다. 양쪽 AC7은 보고서 확인과 PASS의 `verify.sh` exit 0을 요구한다.
- 문제 상황: LLM이 DONE을 `state.md`에 쓴 뒤 리포트 작성을 마치기 전에 timeout 또는 오류로 끝난다. 실패 분기가 다음 회차로 이동하면 진입 DONE 가드가 종료하여 사후 게이트에 도달하지 않는다. 부분 작성된 `action.sh`도 그 경로에서는 실행·검증되지 않는다.
- 예상 영향: “LLM 실패 → 재시도”가 “미검증 DONE → 종료”로 바뀐다. 리포트 없는 DONE을 reject한다는 스킬의 생성 계약을 충족하지 못한다.
- 최소 수정안: 비정상 LLM 종료 시에도 기존 백업을 이용해 상태를 복원하고, 실패한 턴의 미확정 `action.sh`를 다음 실행 대상으로 넘기지 않는 복구 규칙을 템플릿에 넣는다. 정상 완료 상태의 빠른 재실행 종료와 action 이후 DONE 게이트 순서는 유지한다.
- 유지할 계약: LLM 연속 실패 상한, 누적 iteration, 검증된 DONE의 불필요한 LLM 호출 방지, 모든 정상 DONE 전환의 보고서·PASS 검증. 실패 복원은 실제 실행된 외부 작업을 되돌렸다고 주장해서는 안 된다.
- 소유자: ralph-loop-init 양 runtime의 `run.sh` 템플릿. [components.md](../../../_sdd/spec/components.md) 39행의 진입 DONE 가드→사후 DONE 게이트 순서는 변경하지 않는 최소안이다. 그 순서를 바꾸는 대안을 택한다면 spec 결정이 먼저 필요하다.
- 검증 상태: 실패 분기에서 종료까지의 정적 제어 흐름을 확인. 실제 CLI timeout·부분 쓰기 빈도는 미관측.

### ralph-loop-init-05 — reset이 실행 중인 다른 루프를 확인하기 전에 산출물을 지운다 [수정 필요]

- 기준: 5, 2
- 적용 runtime: Claude, Codex
- 증거: [Claude SKILL](../../../.claude/skills/ralph-loop-init/SKILL.md) 312–330행은 reset 시 `rm -rf ralph/results`, `rm -f ralph/action.sh`, state·decisions 재작성을 먼저 수행한다. 다른 실행을 거부하는 `acquire_lock || exit 1`은 428행에 있다. [Codex SKILL](../../../plugins/sdd-skills-codex/skills/ralph-loop-init/SKILL.md) 대응 위치는 306–324·411행이다.
- 문제 상황: 한 루프가 실행 중인 같은 디렉터리에서 두 번째 `bash ralph/run.sh --reset`을 실행한다. 두 번째 프로세스가 정상적으로 lock 거부를 받아도 그 전에 첫 루프의 결과·대기 action·상태·결정 기록을 삭제하거나 초기화한다.
- 예상 영향: 동시 실행 거부가 기존 실행의 산출물을 보호하지 못하고, 첫 루프의 진행과 근거 기록을 훼손한다. reset 자체의 의도된 삭제와 별개로 실행 중인 다른 소유자의 데이터를 변경한다.
- 최소 수정안: reset의 첫 쓰기·삭제 전에 lock 획득과 cleanup 등록을 완료하도록 템플릿 순서를 옮긴다. lock 거부 경로는 결과·state·decisions를 변경하지 않아야 한다.
- 유지할 계약: 명시적인 `--reset`의 새 실행 의미, 정상 재개의 누적 iteration·결과 보존, 단일 루프 소유권. 새 확인 절차를 추가할 필요는 없다.
- 소유자: ralph-loop-init 양 runtime의 `run.sh` 템플릿.
- 검증 상태: 삭제와 lock 획득의 순서를 정적으로 확인. 실행 중 reset을 실제 수행하지 않았다.

## 런타임 차이와 의존성

- Claude의 `claude -p` stream-json 처리와 Codex의 `codex exec --json`·최종 메시지 파일은 의도된 런타임 차이다. 각 CLI 플래그의 현재 지원 여부는 조사하지 않았으며, 기능 부재 finding을 만들지 않았다.
- Codex의 “Do NOT delegate to other agents”와 Claude의 Skill tool 금지는 각 생성 프롬프트의 독립 루프 경계를 표현한다. 이번 리뷰는 실제 재귀·위임 행동을 검증하지 않았다.
- Step 2의 포괄 승인 차이는 CLI 차이에서 필연적으로 생기는 계약이 아니므로 finding 01로 분리했다.
- 읽은 직접 근거: 양 runtime의 `ralph-loop-init/SKILL.md` 본문·인라인 템플릿, [AGENTS.md](../../../AGENTS.md), [global spec](../../../_sdd/spec/main.md)의 관련 guardrail·결정, [env.md](../../../_sdd/env.md), [components.md](../../../_sdd/spec/components.md) 39행 및 실행 분리 설명, [공통 리뷰 기준](./review-criteria.md).
- 이 스킬은 별도 로컬 reference 파일을 필수로 읽도록 지시하지 않는다. `investigate`·`goal-init`은 경계 안내 대상으로만 언급되며 이번 finding이 그 구현에 의존하지 않아 본문 검토를 확대하지 않았다. 소비 프로젝트·생성된 실물 파일·설치본 CLI·기존 장기 실행 기록은 미검토다.
- cross-skill 수정 소유자 없음. spec에 이미 고정된 실행 순서 자체를 바꾸는 확대안은 ralph-loop-init 변경과 spec 결정으로 함께 다뤄야 한다.

## 권장 처리 순서와 검증

1. 템플릿의 reset 전 lock과 비정상 LLM 종료 복원을 먼저 수정한다(05·04). 후속 검증은 임시 디렉터리와 가짜 CLI로 수행한다. 실행 중인 lock의 소유자를 만들어 reset 전후 결과·state·decisions 해시가 같음을 확인하고, 가짜 CLI가 DONE을 쓴 뒤 nonzero로 끝날 때 보고서 게이트를 우회하여 완료되지 않는지 확인한다.
2. phase 변경 범위를 예약 이름과 중간 이름으로 나눈다(03). 중간 phase만 바꾼 생성물의 상태 집합·초기값·종료 소비 지점을 정적으로 대조한다.
3. Step 2의 질문 조건과 Step 8의 상한 소진 결과를 명시한다(01·02). 정보가 모두 주어진 초기화 입력과 두 번 수정해도 CHECKS가 실패하는 입력에서 각각 재확인 없이 생성, 미완료 결과 보고로 닫히는지 후속 관측한다.

이번 리뷰에서는 대상 스킬이나 생성 루프를 실행하지 않았고 제안도 적용하지 않았다. 보고서의 상대 링크·인용 위치·파일 권한·diff 공백만 점검한다.
