# Sample goal-init Session

이 예제는 "flaky 통합 테스트 안정화" 목표에 대한 goal-init 스킬 실행 세션을 보여줍니다.
열린 원인 탐색에서 필요한 정보를 확인하고 하네스를 작성해
4파일 하네스 + 분업형 조건 문자열이 나오는지 1개 시나리오로 보입니다.

## Session Flow

### 1. Goal Intake — 목표 수집 + 적합성 gate

이 단계는 목표를 받아 "verifiable end state가 있는 멀티턴 작업인가" hard gate를 적용합니다.

```
User: /goal 셋업하고 싶어요

Claude: 네이티브 /goal에 걸 완료조건과 4파일 실행 하네스를 함께 셋업합니다.
달성하려는 목표가 무엇인가요?

User: CI에서 가끔 깨지는 통합 테스트 스위트가 있어요. 알아서 안정화해줘.
반복 통합 검증은 수정 후보가 준비된 checkpoint에서 실행해요.

Claude: 적합성을 확인합니다.
- 종료 상태가 transcript에서 판정 가능한가? → "테스트를 N회 연속 실행해 전부 통과" 형태로 판정 가능
- 한 번의 답변으로 끝나지 않는 반복 작업인가? → flaky 원인을 가설별로 시도/검증하는 반복 작업

두 기준을 모두 만족하므로 /goal 적합 목표입니다. (단발 작업이었다면 여기서 중단)

확인할 종료 기준 1가지: 몇 회 연속 통과를 "안정화"로 볼까요?

1. "20회 연속 통과"
2. "50회 연속 통과"
3. Other (직접 입력)

User: 1 (20회)
```


### 2. Divergence — AI가 접근/가설을 능동 발산

이 예제는 원인이 열려 있어 권장안과 구별되는 가설을 비교하고 `experiments.md` pending 백로그로 모읍니다.

```
Claude: 안정화 접근을 먼저 발산합니다 (권장안 먼저).

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


### 3. Condition Crafting — 분업형 조건 문자열 응축 + 평가자 self-check

이 단계는 5요소(목표/측정 가능 AC/증명/제약/종료 경계)를 `DONE WHEN`/`CONSTRAINTS`/`STOP` 분업형으로 응축하고,
브리틀 검증 디테일(명령·기대 출력·수치)은 `goal.md` `검증 레시피`로, 루프 행동(HOW)은 `Loop Protocol`로 분리합니다.
그 후 평가자 적합성 3항목 self-check를 적용합니다.

```
Claude: 조건 문자열로 응축합니다. 재설정 litmus를 적용합니다 — "이 디테일이 어긋나면 goal을
다시 세우는 게 마땅한가?" Yes → 인라인, No → 검증 레시피.
- "20회 연속 통과"라는 outcome, 대상 스위트 경로 → 어긋나면 목표가 바뀜 → 인라인 (anchor).
- pytest 정확한 명령·passed 기대 개수 → 옵션·테스트 수가 바뀌어도 목표는 그대로 → 검증 레시피.

DONE WHEN: tests/integration 스위트가 20회 연속 전부 통과한다. 증명: `goal.md` 검증 레시피의
  명령 실제 출력이 transcript에 surface되고 전 항목 PASS다 (failed/error 0건이 출력에 보인다).
CONSTRAINTS: 검증 레시피 변경 시 변경 diff·사유를 transcript에 표시하며, 판정을 약화하는 변경은
  사용자 승인이 필요하다. `goal.md` 자율 수행 위임의 사전 승인 범위에 있는 행동에 대해 사용자 확인을 요청하며 턴을 끝내지 않는다. 테스트를 skip/xfail 처리하거나 retry 플러그인으로 재시도해 통과시키지 않는다 (원인 수정으로만).
STOP: after 6 turns without progress.

평가자 적합성 self-check:
- (a) 도구 없이 transcript만으로 판정 가능한가 → 예. 20회 실행된 대상·passed 개수·failed/error 0건이 출력에 보임.
- (b) evidence가 매 턴 surface되는가 → 예. 허용된 검증의 실제 출력 또는 기존 evidence·미실행 사유를 매 턴 표시.
- (c) 4,000자 이하인가 → 예.

3항목 모두 통과 → 응축 확정.
```


### 4. Harness Setup — 4파일 생성

이 단계에서만 파일을 생성합니다. 경로는 `_sdd/goal/2026-06-22_stabilize-flaky-integration-tests/` 입니다.

생성된 4파일:

| 파일 | 경로 | 내용 |
|------|------|------|
| `goal.md` | `_sdd/goal/2026-06-22_stabilize-flaky-integration-tests/goal.md` | 확정 조건 문자열 + 검증 레시피 + Loop Protocol + 실행법(Claude 슬롯) |
| `experiments.md` | `_sdd/goal/2026-06-22_stabilize-flaky-integration-tests/experiments.md` | 가설 A, B를 pending 백로그로 기입 |
| `journal.md` | `_sdd/goal/2026-06-22_stabilize-flaky-integration-tests/journal.md` | append-only, 초기 빈 헤더 |
| `report.md` | `_sdd/goal/2026-06-22_stabilize-flaky-integration-tests/report.md` | conclusion-first, Status: STUCK(초기) |

`goal.md` 핵심 (조건 문자열 / 검증 레시피 / Loop Protocol 3분법):

```markdown
# Goal: flaky 통합 테스트 스위트 안정화

## `/goal` 조건 문자열
(Step 3에서 확정한 `DONE WHEN`/`CONSTRAINTS`/`STOP` 조건 문자열을 그대로 기입)

## 검증 레시피
매 턴 이번 진척에 필요한 허용된 검증을 실행하고 실제 출력을 표시한다. 실행하지 않은 필수 검증은 기존 evidence와 그 유효성·미실행 사유를 표시한다. repo의 slow/checkpoint·timeout 재실행 제한을 따른다. 최종 PASS에는 모든 필수 검증의 유효한 실행 증거가 필요하다.

- 안정성 판정: `pytest tests/integration --count=20 -q` → passed 수 = 스위트 테스트 수 × 20, failed/error 0. pytest-repeat가 설치된 예제 환경을 전제한다.
- 실행 checkpoint: 사용자 지정대로 수정 후보가 준비된 시점. 매 턴 이 통합 명령을 재실행하지 않는다.

## 자율 수행 위임
- 수준: unattended ("알아서 안정화해줘" 원문 신호)
- 사전 승인: 브랜치 생성·commit·feature 브랜치 push·PR 생성 / pytest·스크립트 실행 / repo 안 파일 수정 / 검증 레시피의 동등·강화 변경
- 항상 확인(제외): main 직접 push·force-push / PR merge / 판정 약화 레시피 변경 / 시크릿 취급

## Loop Protocol
매 턴 다음을 수행한다 (메인 에이전트용 HOW, 조건 문자열에 넣지 않는다):
1. `experiments.md`의 pending 가설 하나를 골라 시도한다.
2. 검증 레시피의 실행 규칙에 따라 해당 가설의 evidence를 대화에 표시한다.
3. 시도·결과를 `journal.md`에 append한다.
4. 모든 DONE WHEN 검증을 통과하면 성공 종료한다. STOP/STUCK 경계면 사유를 report.md에 기록하고 미완료로 종료한다. native goal lifecycle은 활성 런타임 규범을 따른다.
5. 그 외에는 pending 큐가 비었으면 새 가설을 추가하고 다음 턴을 진행한다.

## 실행법
### Claude Code
1. workspace를 trust하고 hooks를 활성화한다.
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


### 5. Handoff — 조건 문자열 + Claude 실행법 제시 (스킬은 /goal 비발동)

```
Claude: 셋업 완료. 아래를 검토 후 직접 /goal에 거세요. (스킬은 /goal을 직접 발동하지 않습니다.)

[최종 분업형 조건 문자열 — /goal에 그대로 입력]
DONE WHEN: tests/integration 스위트가 20회 연속 전부 통과한다. 증명: `goal.md` 검증 레시피의 명령 실제 출력이 transcript에 surface되고 전 항목 PASS다 (failed/error 0건이 출력에 보인다).
CONSTRAINTS: 검증 레시피 변경 시 변경 diff·사유를 transcript에 표시하며, 판정을 약화하는 변경은 사용자 승인이 필요하다. `goal.md` 자율 수행 위임의 사전 승인 범위에 있는 행동에 대해 사용자 확인을 요청하며 턴을 끝내지 않는다. 테스트를 skip/xfail 처리하거나 retry 플러그인으로 재시도해 통과시키지 않는다 (원인 수정으로만).
STOP: after 6 turns without progress.

[Claude /goal 실행법]
1. workspace trust + hooks 활성화 확인.
2. `/goal DONE WHEN: ... STOP: after 6 turns without progress.` 로 발동.
3. 루프 중단 후 재개는 `--resume`/`--continue`로 복원.

하네스:
- _sdd/goal/2026-06-22_stabilize-flaky-integration-tests/goal.md
- _sdd/goal/2026-06-22_stabilize-flaky-integration-tests/experiments.md
- _sdd/goal/2026-06-22_stabilize-flaky-integration-tests/journal.md
- _sdd/goal/2026-06-22_stabilize-flaky-integration-tests/report.md
goal을 활성화하지 않았으며 기존 goal 상태도 변경하지 않았다.
검토 후 발동 여부는 형님이 결정하세요.
```


## 핵심 포인트 (이 예제가 보여주는 것)

- **상황에 맞는 진행**: 아래 대화는 한 예다. 접근과 검증이 이미 정해져 있으면 재수집·대안 개수 채우기 없이 조건을 점검하고 하네스를 완성한다.
- **3분법 조건 문자열**: `DONE WHEN`은 outcome + anchor + "검증 레시피 출력 surface·전 항목 PASS" 표준 문구, 브리틀 검증 디테일(pytest 명령·기대 문자열)은 `goal.md`의 `검증 레시피`로, 루프 HOW는 `Loop Protocol`로 분리. `CONSTRAINTS`에 drift 가드(레시피 변경 diff 표시·약화는 사용자 승인) 기본 포함.
- **평가자 적합성 3항목**: 도구 없이 판정 · evidence 매 턴 surface · 4,000자 이하 — 모두 통과해야 Handoff.
- **4파일 산출 경로**: `_sdd/goal/<YYYY-MM-DD>_<slug>/`의 `goal.md`/`experiments.md`/`journal.md`/`report.md`.
- **자율 수행 위임**: 원문의 "알아서" 신호로 `unattended` 확정 → `goal.md`에 사전 승인/제외 목록 기입. 루프 중 commit·push는 이 위임으로 확인 없이 진행되고, 제외 목록만 사용자 승인 대상.

## 접근이 확정된 입력

사용자가 “정해진 API 교체 계획대로 진행하고, 제공한 회귀 명령 통과를 완료조건으로 goal 하네스를 만들어줘. 자율 수행 범위도 아래와 같아”라고 요청하면 해당 정보로 조건과 권한을 확인한다. 새 대안 2개를 요구하지 않고 선택된 접근을 experiments에 기록한다. 적합성과 조건 self-check를 통과한 뒤 네 파일과 조건 전문을 전달하며 goal을 활성화하지 않는다.
