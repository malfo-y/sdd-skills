# SDD-Autopilot 사용 가이드

**버전**: 3.0.0
**날짜**: 2026-08-10

## 1. 개요

`sdd-autopilot`은 기능을 즉시 구현하는 독립 runner가 아니라 **SDD 전용 goal harness 셋업 entrypoint**입니다. 기능 목표를 `goal-init(preset=sdd)`에 전달해 자족적 완료조건과 `_sdd/goal/<날짜>_<slug>/` 4파일을 만들고, 사용자가 검토한 뒤 native goal을 직접 활성화하도록 안내합니다.

실제 planning·implementation·spec sync 반복은 setup 중이 아니라 사용자가 활성화한 native goal 안에서 수행됩니다.

## 2. 셋업과 실행 흐름

```text
/sdd-autopilot <기능 목표>
  → goal-init(preset=sdd)
  → Goal Intake → Divergence → Condition Crafting → Harness Setup → Handoff
  → 조건 문자열 + 4-file harness 제시 (아직 비활성)

사용자가 검토 후 native /goal 활성화
  → SDD Loop Protocol이 필요한 feature별 SDD path를 반복
  → 모든 DONE WHEN + final integration proof 통과 시 종료
```

`goal-init`의 기존 5단계, evaluator self-check(도구 없이 판정·evidence surface·4,000자 이하), 4파일 형식은 generic 경로와 같습니다. SDD preset은 `goal.md`의 Loop Protocol payload만 바꿉니다.

## 3. SDD Loop Protocol

활성화된 native goal은 매 턴 다음 순서를 따릅니다.

1. 아직 충족되지 않은 `DONE WHEN` 또는 실패한 final integration proof가 드러낸 gap에서 가장 작은 next feature를 고릅니다.
2. reviewed draft가 없으면 `feature-draft`를 실행합니다. draft가 분할되면 현재 goal 안에서 가장 작은 next unit을 고릅니다.
3. 선택한 draft를 `implementation`으로 구현하고 producer-owned 품질 게이트까지 닫습니다.
4. persistent 변경이 있으면 `spec-sync`를 실행합니다.
5. 검증 출력을 대화에 표시하고 evidence·완료 feature·남은 gap·next action을 journal/report에 기록합니다.
6. 모든 `DONE WHEN`과 final integration proof가 통과했을 때만 종료합니다. 아니면 1단계로 돌아갑니다.

`feature-draft`가 실행 중 다시 분할돼도 nested `goal-init`을 만들지 않습니다. 현재 native goal이 같은 Loop Protocol에서 다음 최소 feature를 계속 선택합니다.

## 4. 경계

- **Setup only**: `/sdd-autopilot` 호출 중 initial `feature-draft`·`implementation`·`spec-sync`는 실행되지 않습니다.
- **사용자 activation**: 스킬은 native goal을 직접 발동하지 않습니다.
- **기존 goal 불간섭**: current goal status를 조회하지 않고, 기존 goal을 변경·clear·pause·replace·merge하거나 active goal 때문에 setup을 차단하지 않습니다.
- **Handoff 불변식**: 결과에는 “goal을 활성화하지 않았으며 기존 goal 상태도 변경하지 않았다”가 항상 표시됩니다.
- **Producer ownership**: 활성화 후 각 feature의 계획·구현 품질 게이트와 fix는 계속 `feature-draft`·`implementation`이 소유합니다.
- **기존 harness 재사용**: `goal.md`·`experiments.md`·`journal.md`·`report.md`의 역할과 형식을 유지하며 별도 queue/state-machine schema를 만들지 않습니다.

## 5. 사용법

```text
/sdd-autopilot <검증 가능한 멀티턴 기능 목표>
```

예:

```text
/sdd-autopilot JWT 기반 인증 시스템을 구현해줘. 로그인, 로그아웃, 토큰 갱신과 통합 검증 포함.
/sdd-autopilot legacy 결제 모듈을 새 API로 마이그레이션하고 회귀 테스트와 문서 동기화까지 완료해줘.
```

`/goal`은 verifiable end state가 있는 멀티턴 작업에 적합합니다. 한 줄 수정 같은 단발 작업이면 `goal-init` 적합성 gate가 재정의 또는 단발 작업 전환을 안내하며, autopilot이 구현을 자동 시작하지 않습니다.

### 사용자 역할

| 시점 | 사용자가 하는 것 |
|------|----------------|
| Goal Intake/Condition Crafting | 목표와 DONE WHEN을 확정하는 질문에 답변 |
| Handoff | 조건 문자열과 4파일 harness 검토 |
| Activation | native `/goal`을 직접 활성화할지와 시점을 결정 |
| 실행 중 | 필요할 때 `/goal status`·`pause`·`resume`·`clear` 사용 |

## 6. 산출물

| 산출물 | 위치 / 의미 |
|--------|-------------|
| `goal.md` | 완료조건 + SDD Loop Protocol + runtime 실행법 |
| `experiments.md` | 접근 가설 pending/done 백로그 |
| `journal.md` | evidence·완료 feature·남은 gap·next action append-only 기록 |
| `report.md` | 현재 결론과 integration proof 상태 |

네 파일은 `_sdd/goal/<YYYY-MM-DD>_<slug>/`에 생성됩니다. setup 직후 draft·코드·implementation ledger·spec 변경은 생기지 않습니다. 해당 산출물은 사용자가 native goal을 활성화한 뒤 Loop Protocol이 feature별로 만듭니다.

## 7. FAQ

- **spec이 없는 repo에서도 되나요?** — goal harness setup은 가능합니다. 활성화 후 persistent spec이 없으면 해당 loop의 `spec-sync` 처리 여부는 producer contract와 repo 상태에 따라 결정됩니다.

## 8. 관련 스킬

- `goal-init` — 5단계 condition/harness setup의 canonical owner; SDD preset payload 포함
- `feature-draft` — 활성 goal이 선택한 next feature의 명세와 분할 규칙
- `implementation` — draft를 RED→GREEN으로 구현하고 내부 품질 게이트 수행
- `spec-sync` — persistent 변경의 global spec 동기화
