# Sample goal-init Session

이 예제는 "flaky 통합 테스트 안정화" 목표에 대한 goal-init 스킬 실행 세션을 보여줍니다.
5단계(Goal Intake → Divergence → Condition Crafting → Harness Setup → Handoff)가 어떻게 진행되어
4파일 하네스 + 분업형 조건 문자열이 나오는지 1개 시나리오로 보입니다.

## Session Flow

### 1. Goal Intake — 목표 수집 + 적합성 gate

이 단계는 목표를 받아 "verifiable end state가 있는 멀티턴 작업인가" hard gate를 적용합니다.

```
User: /goal 셋업하고 싶어요

Codex: 네이티브 /goal에 걸 완료조건과 4파일 실행 하네스를 함께 셋업합니다.
달성하려는 목표가 무엇인가요?

User: CI에서 가끔 깨지는 통합 테스트 스위트가 있어요. 이걸 안정화하고 싶어요.

Codex: 적합성을 확인합니다.
- 종료 상태가 transcript에서 판정 가능한가? → "테스트를 N회 연속 실행해 전부 통과" 형태로 판정 가능
- 한 번의 답변으로 끝나지 않는 반복 작업인가? → flaky 원인을 가설별로 시도/검증하는 반복 작업

두 기준을 모두 만족하므로 /goal 적합 목표입니다. (단발 작업이었다면 여기서 중단)

확인할 종료 기준 1가지: 몇 회 연속 통과를 "안정화"로 볼까요?

1. "20회 연속 통과"
2. "50회 연속 통과"
3. Other (직접 입력)

User: 1 (20회)
```

**Decision Gate 1→2 통과**: verifiable end state(20회 연속 통과) 있는 멀티턴 작업 확정.

### 2. Divergence — AI가 접근/가설을 능동 발산

이 단계는 권장안을 먼저 말하고 2개 이상 접근/가설을 발산해 `experiments.md` pending 백로그로 모읍니다.

```
Codex: 안정화 접근을 먼저 발산합니다 (권장안 먼저).

[권장] 가설 A — 비결정적 대기(sleep/race)가 원인.
  검증: `pytest tests/integration -x -p no:randomly` 를 반복해 타이밍 의존 케이스 격리.
  트레이드오프: 가장 흔한 flaky 원인이라 ROI 높음. 단 명시적 wait 도입 리팩터 필요.

가설 B — 테스트 간 상태 공유(DB/전역) 누수가 원인.
  검증: `pytest tests/integration -p no:randomly` vs 랜덤 순서 결과 비교.
  트레이드오프: 순서 의존이면 격리로 깔끔히 해결. 누수 지점 추적 비용 있음.

가설 C — 외부 서비스 호출이 mock 안 되어 네트워크 변동에 노출.
  트레이드오프: 발생 빈도는 낮지만 한번 잡으면 확실. 우선순위 후순위.

A를 1순위로 권장합니다. B를 함께 백로그에 둘까요?

User: A, B 둘 다 백로그에 넣고 A부터 시작하죠.
```

**Decision Gate 2→3 통과**: pending 가설 2개 이상(A, B; C는 후보) 확보.

### 3. Condition Crafting — 분업형 조건 문자열 응축 + 평가자 self-check

이 단계는 5요소(목표/측정 가능 AC/증명/제약/종료 경계)를 `DONE WHEN`/`CONSTRAINTS`/`STOP` 분업형으로 응축하고,
루프 행동(HOW)은 조건 문자열에 넣지 않습니다. 그 후 평가자 적합성 3항목 self-check를 적용합니다.

```
Codex: 조건 문자열로 응축합니다. 증명은 명령·기대 출력을 transcript에 surface하는 형태로 인라인합니다.

DONE WHEN: tests/integration 스위트가 20회 연속 통과한다.
  증명: `pytest tests/integration --count=20 -q` shows `100 passed` (혹은 동일 수의 passed, 0 failed)
  20번 반복 출력에서 failed/error 0건임이 transcript에 보인다.
CONSTRAINTS: 테스트를 skip/xfail 처리하거나 retry 플러그인으로 재시도해 통과시키지 않는다 (원인 수정으로만).
STOP: after 6 turns without progress.

평가자 적합성 self-check:
- (a) 도구 없이 transcript만으로 판정 가능한가 → 예. `100 passed`/`0 failed` 문자열만 보면 판정됨.
- (b) evidence가 매 턴 surface되는가 → 예. 매 턴 pytest 출력을 대화에 표시(Loop Protocol에 규정).
- (c) 4,000자 이하인가 → 예 (실측 보고는 세션 말미).

3항목 모두 통과 → 응축 확정.
```

**Decision Gate 3→4 통과**: self-check 3항목(도구 없이 판정 · evidence 매 턴 surface · 4,000자 이하) 통과.

### 4. Harness Setup — 4파일 생성

이 단계에서만 파일을 생성합니다. 경로는 `_sdd/goal/2026-06-22_stabilize-flaky-integration-tests/` 입니다.

생성된 4파일:

| 파일 | 경로 | 내용 |
|------|------|------|
| `goal.md` | `_sdd/goal/2026-06-22_stabilize-flaky-integration-tests/goal.md` | 확정 조건 문자열 + Loop Protocol + 실행법(Codex 슬롯) |
| `experiments.md` | `_sdd/goal/2026-06-22_stabilize-flaky-integration-tests/experiments.md` | 가설 A, B를 pending 백로그로 기입 |
| `journal.md` | `_sdd/goal/2026-06-22_stabilize-flaky-integration-tests/journal.md` | append-only, 초기 빈 헤더 |
| `report.md` | `_sdd/goal/2026-06-22_stabilize-flaky-integration-tests/report.md` | conclusion-first, Status: STUCK(초기) |

`goal.md` 핵심 (조건 문자열 슬롯 + Loop Protocol 분리):

```markdown
# Goal: flaky 통합 테스트 스위트 안정화

## `/goal` 조건 문자열
(Step 3에서 확정한 `DONE WHEN`/`CONSTRAINTS`/`STOP` 조건 문자열을 그대로 기입)

## Loop Protocol
매 턴 다음을 수행한다 (메인 에이전트용 HOW, 조건 문자열에 넣지 않는다):
1. `experiments.md`의 pending 가설 하나를 골라 시도한다.
2. 검증 명령을 실행하고 출력을 대화에 그대로 표시한다.
3. 시도·결과를 `journal.md`에 append한다.
4. pending 큐가 비었는데 미완이면 새 가설을 brainstorm해 pending에 append한다.

## 실행법
### Codex
1. goals 기능 활성화: `codex features enable goals` (features.goals).
2. 위 조건 문자열을 `/goal <조건>`에 넣어 발동한다.
```

`experiments.md` 핵심:

```markdown
# Experiments

## Pending
- [ ] 비결정적 대기(race/sleep)가 원인 | 검증: `pytest tests/integration -x -p no:randomly` → 타이밍 케이스 격리
- [ ] 테스트 간 상태 공유 누수가 원인 | 검증: 고정순서 vs 랜덤순서 결과 비교 → 순서 의존이면 격리

## Done
```

**Decision Gate 4→5 통과**: 4파일 생성 완료.

### 5. Handoff — 조건 문자열 + Codex 실행법 제시 (스킬은 /goal 비발동)

```
Codex: 셋업 완료. 아래를 검토 후 직접 /goal에 거세요. (스킬은 /goal을 직접 발동하지 않습니다.)

[최종 분업형 조건 문자열 — /goal에 그대로 입력]
DONE WHEN: tests/integration 스위트가 20회 연속 통과한다. 증명: `pytest tests/integration --count=20 -q` shows `100 passed` (0 failed) in the transcript.
CONSTRAINTS: skip/xfail/retry로 통과시키지 않는다 (원인 수정으로만).
STOP: after 6 turns without progress.

[Codex /goal 실행법]
1. goals 기능 활성화: `codex features enable goals` (또는 config의 features.goals).
2. 라이프사이클: `/goal set <조건>`(목표 설정)·`/goal status`(진행 확인)·`/goal clear`(종료). 위 조건 문자열을 set에 그대로 넣어 발동.
3. 중간에 멈췄다 이어가려면 `/goal pause`·`/goal resume`. continuation은 thread-scoped이며 안전 경계 안에서 evidence-based로 이어간다.

하네스: _sdd/goal/2026-06-22_stabilize-flaky-integration-tests/ (4파일)
검토 후 발동 여부는 형님이 결정하세요.
```

**Decision Gate (종료)**: 조건 문자열 + Codex 실행법 제시 완료 → 종료.

## 핵심 포인트 (이 예제가 보여주는 것)

- **5단계 고정 진행**: Goal Intake(적합성 gate) → Divergence(AI 능동 발산) → Condition Crafting(분업형 응축 + self-check) → Harness Setup(4파일 생성) → Handoff(비발동).
- **분업형 조건 문자열**: `DONE WHEN`은 명령·기대 출력을 transcript-surface 형태로 인라인(`pytest ... shows 100 passed in the transcript`), 루프 HOW는 `goal.md`의 `Loop Protocol`로 분리.
- **평가자 적합성 3항목**: 도구 없이 판정 · evidence 매 턴 surface · 4,000자 이하 — 모두 통과해야 Handoff.
- **4파일 산출 경로**: `_sdd/goal/<YYYY-MM-DD>_<slug>/`의 `goal.md`/`experiments.md`/`journal.md`/`report.md`.
