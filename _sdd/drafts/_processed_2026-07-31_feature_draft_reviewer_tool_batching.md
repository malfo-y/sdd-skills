# Feature Draft: agent tool call 배칭 규칙

> 규모 판정: 적격 — 변경 요소는 동일 문면의 Hard Rule 1개를 agent 5종 × 미러 2벌 = 10파일에 전파하고 `plan-review` 짝에만 계단 1문장을 더하는 것이며, 요소↔task 대응이 눈검산된다(claude 5 / codex 5 / 행동 계측 1).

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

reviewer/producer agent가 **서로 의존하지 않는 read-only tool call을 한 메시지에 모으지 않고 한 개씩 직렬로 호출**하고 있다. 런타임은 배칭을 지원하는데 agent 본문에 그 지시가 없다(10파일 전량 grep 확인 — 배칭 문면 0건).

실측(2026-07-30 `implementation-review` 게이트 1회, subagent transcript 계수):

| agent | 벽시계 | tool_use | assistant 턴 | 최대 연속 실행 |
|---|---|---|---|---|
| `implementation-review-agent` | 430s | 17 (Bash 12 + Read 5) | 31 | **1** |
| `simplicity-review-agent` | 177s | 3 (Read 3) | 7 | **1** |

배칭 0회다. correctness의 17콜 중 앞 9개(`git status`·스킬 diff·draft Read·SKILL.md Read·`env.md`·`git show <hash>`·spec 라인 `sed`·census grep 2개)는 **호출자 digest만 보고 대상이 정해지는** 것들로 서로 의존하지 않는다 — 읽기 범위 계단 ①이 "이 범위는 전문 Read 보장"이라 선언해둔 파일들을 한 개씩 꺼내 읽고 있었다.

- **새 contract**: agent는 서로 의존하지 않는 **read-only** tool call(`Read`·`Grep`·`Glob`·부작용 없는 조회 명령)을 **한 메시지에서** 함께 낸다. 앞 결과를 봐야 대상이 정해지는 호출만 다음 턴으로 미룬다. 파일을 쓰거나 상태를 바꾸는 호출은 배칭 대상이 아니다.
- **새 contract**: **배칭은 읽을 대상을 늘리지 않는다** — 이미 읽기로 결정한 호출을 한 메시지에 모을 뿐이며, "미리 다 읽어두자"로 확장하지 않는다. 이 조항이 없으면 배칭 지시가 읽기량 팽창으로 번져 입력 상한(도구 계단·읽기 범위 계단)을 잠식한다.
- **새 contract**: `plan-review-agent`의 **도구 계단**은 조기 종료가 본질이므로, 배칭은 계단의 **같은 단 안에서만** 한다. 이 제약의 소유자는 Hard Rule이 아니라 계단 자신(Step 3)이다 — 계단 규칙을 Hard Rule에 복제하지 않는다. `implementation-review-agent`의 읽기 **범위** 계단은 순서가 아니라 범위를 규정하므로 배칭과 직교하고, 예외 조항이 필요 없다.
- 병목의 정체가 갱신된다: 이 계열의 지연은 subagent dispatch 왕복도, 입력 읽기량도 아니라 **턴 수만큼 반복되는 추론**이다. nesting 제한(agent가 sub-agent를 못 띄움)은 원인이 아니며, 설령 허용돼도 자식마다 컨텍스트를 적재해 배칭보다 비싸다 — 해소 수단은 fan-out이 아니라 턴 접기다.
- 적용 표면: `.claude/agents/` 5종 + `.codex/agents/` 동명 TOML 5종.

## Scope

- **In**: 위 10파일에 Hard Rule 1개 추가(기존 `출력 절약(내레이션 억제)` 규칙과 같은 실행 경제 계열, 그 다음 번호), `plan-review-agent` 짝의 Step 3 계단에 배칭 제약 1문장, 구현 마감 게이트 실행을 그대로 관측해 배칭 발생 계측.
- **Out**:
  - 도구 계단·읽기 범위 계단의 **내용 변경 없음** — 배칭은 "무엇을 읽는가"가 아니라 "몇 턴에 나눠 읽는가"만 바꾼다.
  - reviewer의 rubric·severity·반환 형식 무변경.
  - 모델·effort 티어 강등은 재제안 금지 대상이라 다루지 않는다.
  - 출력 다이어트 추가 시도 없음 — 전체의 1% 미만으로 이미 측정 종료.
  - `sdd-autopilot`·wrapper 스킬 본문은 대상 아님. 배칭 주체는 agent 자신이다.
  - 계측을 위한 **별도 재dispatch를 하지 않는다** — 구현 마감이 어차피 돌리는 게이트가 관측 대상이다(중복 실행 회피).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: claude agent 5종에 배칭 Hard Rule 추가 + plan-review 계단에 제약 1문장

각 파일 `## Hard Rules` 목록의 **마지막 항목이 `출력 절약(내레이션 억제)`이고 번호가 파일마다 다르다** — 실측: `implementation-review` 8 / `plan-review` 8 / `simplicity-review` 8 / `pr-review` 10 / `spec-sync` 13. 새 규칙은 각 파일의 그 다음 번호로 붙인다(구현자가 재조사하지 않도록 실측값을 여기 적어둔다).

**Contracts**:
- Hard Rule 문면의 필수 4요소 — (i) 서로 의존하지 않는 read-only 호출은 **한 메시지에서** 함께 낸다(**지시형**), (ii) 앞 결과에 의존하는 호출만 다음 턴, (iii) 쓰기·상태 변경 호출은 배칭 대상 아님, (iv) 배칭은 읽을 대상을 늘리지 않는다.
- 문면은 **tool 이름에 의존하지 않는 서술**로 쓴다(런타임별 호출 표현이 달라도 성립해야 한다).
- 어휘는 repo 선례에 맞춘다 — `implementation-review`·`pr-review` SKILL과 `investigate` SKILL이 모두 "**한 메시지에서**"를 쓴다. 새 표현을 만들지 않는다.
- 계단 제약은 Hard Rule이 아니라 `plan-review-agent.md` **Step 3 계단 절**에 1문장으로 넣는다(계단 소유권 단일화). Hard Rule 본문은 5종 동일 문면이다.

**Acceptance Criteria**:
- [ ] AC1: 5개 파일 각각에서 `## Hard Rules` 절(다음 `## ` 헤딩 전까지)의 번호 항목 수가 HEAD 대비 정확히 +1이고, 증가한 항목이 목록 마지막이며 배칭 규칙이다. 번호는 파일별로 9/9/9/11/14다.
- [ ] AC2: 5개 파일 전부에서 필수 4요소가 문장으로 확인되고, 요소 (i)이 **허가형이 아니라 지시형**이다 — "배칭해도 된다"류면 미충족, "한 메시지에서 함께 낸다"류면 충족(문장 인용으로 판정). repo 기존 배칭 문장이 전부 허가형이라 이 구분이 실제 위험이다.
- [ ] AC3: 계단 제약 문장이 `plan-review-agent.md`의 Step 3 절 안에만 존재하고, 5개 파일의 Hard Rules 절 어디에도 없다 (grep으로 판정).
- [ ] AC4: 5개 파일의 `git diff -U0` +/- 라인이 (a) 새 Hard Rule 항목과 (b) `plan-review`의 Step 3 문장 1개뿐이다 — +/- 라인 전량을 인용해 판정한다. 기존 규칙 본문·번호 훼손 0.

**Target Files**:
- [M] `.claude/agents/implementation-review-agent.md` -- Hard Rule 9 추가
- [M] `.claude/agents/plan-review-agent.md` -- Hard Rule 9 추가 + Step 3 계단 제약 1문장
- [M] `.claude/agents/simplicity-review-agent.md` -- Hard Rule 9 추가
- [M] `.claude/agents/pr-review-agent.md` -- Hard Rule 11 추가
- [M] `.claude/agents/spec-sync-agent.md` -- Hard Rule 14 추가

### Task 2: codex TOML 미러 5종에 3-way merge 반영

codex 미러는 claude 본문의 단순 복사가 아니라 codex 적응 delta를 보존한 3-way merge다. 번호 분포는 claude 짝과 동일하다(8/8/8/10/13 → 9/9/9/11/14).

**Contracts**:
- 규칙 **주문장은 tool 이름에 의존하지 않는 서술**을 쓴다. `multi_tool_use.parallel`은 `.codex/agents/README.md:44`가 정한 codex 관용이므로 **표현 예시로만** 덧붙인다 — 주문장을 tool 이름에 걸면 런타임이 그 이름을 노출하지 않을 때 규칙이 실패하는 호출 지시가 된다.
- `plan-review-agent.toml`에만 계단 제약 문장(claude 짝과 동일 비대칭).

**Acceptance Criteria**:
- [ ] AC1: TOML 5종 각각에 배칭 규칙이 있고 필수 4요소 + 지시형 조건(Task 1 AC2와 동일 기준)이 충족된다.
- [ ] AC2: 5개 TOML 전부 `tomllib`로 파싱된다.
- [ ] AC3: 5개 TOML의 `git diff -U0` +/- 라인이 배칭 규칙 추가분(+ `plan-review`의 계단 문장)뿐임을 전량 인용으로 판정한다 — 기존 codex 적응 delta 보존.
- [ ] AC4: claude 짝과 codex 짝의 배칭 규칙이 **의미상 동일**하다(문면은 codex 어휘 적응으로 다를 수 있음). 4요소 각각이 양쪽에 대응함을 인용으로 대조한다.

**Target Files**:
- [M] `.codex/agents/implementation-review-agent.toml`
- [M] `.codex/agents/plan-review-agent.toml`
- [M] `.codex/agents/simplicity-review-agent.toml`
- [M] `.codex/agents/pr-review-agent.toml`
- [M] `.codex/agents/spec-sync-agent.toml`

### Task 3: 행동 계측 — 규칙이 실제로 배칭을 만드는가 (read-only)

문면 존재는 동작을 증명하지 않는다. **별도 재dispatch를 하지 않고**, 구현 마감이 어차피 1회 돌리는 `implementation-review` 게이트 실행을 그대로 관측 대상으로 삼는다.

**Contracts**:
- 관측 대상: 마감 게이트에서 background로 dispatch되는 두 reviewer. transcript 경로는 dispatch 결과가 반환하는 output file이다.
- 계수 규칙 **(구현 중 교정 — 최초 규칙은 무효였다)**: transcript JSONL은 **한 메시지의 content 블록을 줄 단위로 쪼개 기록**한다(같은 assistant 메시지의 `text`와 `tool_use`가 별도 줄). 따라서 "메시지당 tool_use/tool_result 수"는 **항상 1**이 나와 배칭을 원리적으로 탐지하지 못한다. 유효 규칙은 **연속 실행 길이**다 — user의 `tool_result` 줄이 끼어들지 않고 이어지는 assistant `tool_use` 줄의 연속 개수를 세고, 그 최대값이 2 이상이면 배칭이다. 이 규칙은 양성 대조로 검증됐다: 같은 날 `plan-review-agent` 회차가 최대 연속 2(구간 1개)로 잡히고, correctness·simplicity 회차는 4회차 전부 1이다. transcript 본문은 읽지 않고 계수만 한다.
- 기록 위치: 구현 **마감 보고**에 baseline과 나란한 표로 싣는다(파일 산출물 없음).

**Acceptance Criteria**:
- [ ] AC1: 두 reviewer 각각의 **최대 연속 실행 길이**(위 교정된 계수 규칙)를 계측해 보고한다. **2 이상이면 배칭 발생**이다. 전부 1이면 규칙이 동작을 바꾸지 못한 것이므로 미충족으로 보고한다. 단 위 전제조건이 충족되지 않은 회차는 `UNTESTED`로 닫고 사유를 병기한다 — 규칙이 로드되지 않은 실행은 규칙의 반증이 아니다.
- [ ] AC2: 결과 표에 baseline(correctness 17콜/31턴/430s, simplicity 3콜/7턴/177s)을 나란히 싣고, 이번 회차의 tool_use 수·assistant 턴 수·벽시계를 함께 적는다. 턴 수가 줄지 않았어도 수치를 그대로 보고한다 — 개선 없음도 결과다.
- [ ] AC3: 판정의 **비대칭**을 결과에 1줄로 명시한다 — 배칭 발생(양성)은 규칙 효과의 증명이 아니라 정합 관측이다(baseline과 repo 상태·리뷰 대상이 달라 인과 귀속 불가, 단일 표본). 반대로 배칭 0(음성)은 n=1에서도 규칙 무효의 반증력을 갖는다.

**Target Files**:
- 없음 (read-only 계측)

**전제조건 (구현 중 발견 — 이게 없으면 계측이 무효다)**: dispatch되는 agent는 작업트리가 아니라 **plugin 설치본**(`~/.claude/plugins/cache/sdd-skills/`, 푸시된 커밋 SHA 기준)에서 로드된다. 따라서 이 feature의 계측은 (a) 커밋·푸시 후 plugin이 갱신되고, (b) 호출자 digest에 배칭 논의를 넣지 않은 **새 세션의 게이트**를 대상으로 해야 한다. 두 조건 중 하나라도 빠지면 결과를 규칙에 귀속할 수 없다.

# Open Questions

- **적용 범위의 근거 비대칭**: 배칭 부재는 10파일 전량 grep으로 확인했지만 **실측은 claude 2종**(`implementation-review`·`simplicity-review`)이고, Task 3의 행동 계측도 그 2종만 커버한다. `pr-review`·`spec-sync`는 문면 전파만이며, **codex 미러 5파일은 이번 feature에서 실측 검증 경로가 0이다** — 다음 codex 실행 시 사후 확인 대상. 규칙이 해가 되는 경로가 없고(읽을 대상은 그대로, 모으기만 함) 파일당 1문장이라 확인 불요.
- **단일 표본 한계**: Task 3은 1회 관측이라 벽시계 차이를 유의미한 절감으로 주장할 수 없다. 배칭 발생 여부는 이분 판정이라 1회로 족하지만 시간 절감 폭은 추정치로만 남긴다. 사용자 확인 불요.
