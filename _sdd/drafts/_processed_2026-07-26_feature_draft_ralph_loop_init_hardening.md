# Feature Draft: ralph-loop-init 런타임 안전장치 · 자체검증 실효화

> 규모 판정: 적격 — 수정 대상이 `.claude`/`.codex` 두 SKILL.md(+ skill.json 2개)로 닫히고, 9개 finding이 각각 독립 task에 1:1 대응해 coverage 눈검산이 가능하다. 단, 미러 2벌 전파는 census형 신호이므로 Part 2 마지막에 read-only census 검증 task를 둔다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

`ralph-loop-init` 스킬 리뷰(2026-07-26)에서 확인된 런타임 안전장치 부재와 자체검증 헐거움을 수정한다. 스킬 본체의 워크플로우(8 step)와 상태 머신 설계는 그대로 두고, **스킬이 생성하는 산출물 템플릿(run.sh / config.sh / PROMPT.md / CHECKS.md / state.md)과 AC·검증 절차**만 손본다.

동기는 셋이다. (1) 생성된 루프가 `--dangerously-skip-permissions` + `while true`로 도는데 wall-clock 예산도 iteration 상한도 없고 종료 압력이 전적으로 LLM 자기판단이다. (2) DONE 감지가 action 실행보다 앞서 있어 마지막 iteration의 action이 조용히 유실되며, 이 경로에서 AC6(final_report 강제)가 init 시점엔 통과하고 런타임에 깨진다. (3) placeholder 검사·template fidelity가 실효 없는 형태라 init 시점 자체검증이 통과해도 산출물이 깨져 있을 수 있다.

새로 생기는 contract:
- **생성 산출물이 5파일 → 6파일**이 된다 (`ralph/decisions.md` 추가). AC1과 Step 8 요약 출력이 이 목록의 단일 소스다.
- **`config.sh` 고정 루프 제어 변수가 4개**가 된다 (`LLM_TIMEOUT_SECONDS`, `MAX_LLM_FAILURES`, `MAX_RUNTIME_MINUTES`, `MAX_ITERATIONS`). 프로젝트별 변수와 무관하게 항상 포함된다. 두 상한의 축이 다르다 — **`MAX_RUNTIME_MINUTES`는 실행 1회 기준(재실행 시 예산 리셋)**이고 **`MAX_ITERATIONS`는 누적 기준(재시작 간 이어짐)**이다.
- **`run.sh` iteration 루프의 DONE 판정 위치는 action.sh 실행 이후**다. 즉 "phase를 DONE으로 바꾼 iteration의 action.sh도 실행되고 archive된다"가 보장된다.
- **init 시점 placeholder 검사 범위 (단일 소스)**: 검사 대상은 `config.sh`·`run.sh`·`state.md`·`CHECKS.md` **전 문면**과 `PROMPT.md`의 **문서 시작부터 `## Iteration Protocol` 직전까지 + `## Known Errors` 섹션**이다. 이 범위에 미충전 `<...>` 슬롯이 0이어야 한다. 머리말을 범위에 넣는 이유는 H1 제목의 `<project name>`이 이 task의 동기가 된 대표 슬롯이기 때문이다(구현 리뷰 correctness M2 반영 — 초안의 "4개 `##` 섹션" 범위는 첫 `##` 앞의 H1을 놓쳤다). `PROMPT.md`의 나머지(`## action.sh Rules`의 `tee ralph/results/<name>.log`, `## Final Report` 이하)는 루프 LLM을 향한 서식 지시이지 미충전 슬롯이 아니므로 검사하지 않는다. `CHECKS.md`가 자기 자신을 검사 대상으로 삼으므로, `CHECKS.md`의 이 검사 항목 문장은 리터럴 꺾쇠(`<`…`>`)를 쓰지 않고 서술한다. 이 문단이 범위의 단일 소스이며, 다른 곳은 재서술하지 않고 참조만 한다.

## Scope

- **In**: `.claude/skills/ralph-loop-init/SKILL.md`, `.codex/skills/ralph-loop-init/SKILL.md` 및 두 `skill.json`의 version. 두 미러 동시 반영이 기본이며, codex 미러의 Codex CLI 적응 delta(`codex exec` 호출부, `--dangerously-bypass-approvals-and-sandbox`, `-o` last-message 처리)는 보존한다.
- **Out**: ralph 상태 머신 phase 구성 변경, Step 1~2 discovery 로직 변경, 생성된 `ralph/` 산출물의 실제 런타임 검증(격리 환경 필요). `sdd-autopilot`에 ralph 진입 힌트를 재도입할지는 사용자 결정 대기 항목이므로 이번 범위 밖이다.
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: wall-clock 예산(`MAX_RUNTIME_MINUTES`) + iteration backstop 도입

무한 `while true` 루프에 기계적 상한을 준다. 현재 유일한 종료 압력인 "같은 원인 3회 실패 → DONE"은 LLM 자기판단이라, 판단이 흔들리면 skip-permissions 루프가 무한히 돈다. 주 상한은 **wall-clock**이다 — ralph는 한 iteration이 5분일 수도 6시간일 수도 있어서 iteration 수가 "얼마나 오래 도는가"의 대리지표로 못 쓴다. iteration 상한은 폭주 감지용 backstop으로만 남긴다(LLM이 매번 성공하면서 action.sh를 안 쓰는 무진전 공회전은 시간이 아니라 토큰을 태우므로 wall-clock이 못 막는다).

**Contracts**: `config.sh` 고정 루프 제어 변수가 4개가 된다. 두 상한의 축이 다르다 — `MAX_RUNTIME_MINUTES`는 **실행 1회 기준**으로 run.sh 시작 시각부터 재며 재실행하면 예산이 리셋되고, `MAX_ITERATIONS`는 **누적 기준**으로 `state.md`의 `iteration:`을 이어받는다(claude 433-435줄 / codex 425-427줄). wall-clock 판정은 **soft**다 — iteration 경계에서만 판정하므로 진행 중인 `action.sh`는 중단하지 않고 끝까지 두며, 따라서 총 실행 시간이 마지막 action 길이만큼 예산을 초과할 수 있다. 어느 상한이든 도달 시 run.sh는 **`phase:`를 건드리지 않고** `notes`에 도달한 상한의 종류를 남긴 뒤 비-0 exit로 종료한다. phase를 보존하는 이유는 재개 경로를 살리기 위함이다 — 결과를 지우는 `--reset` 없이 중단 지점부터 이어갈 수 있다.

**Acceptance Criteria**:
- [ ] AC1: 두 미러의 Step 4 고정 변수 블록에 `MAX_RUNTIME_MINUTES`(기본 720 = 12시간)와 `MAX_ITERATIONS`(기본 200)가 각각 주석과 함께 포함되고, 주석이 둘의 역할 차이(주 예산 / 폭주 backstop)와 기준 축 차이(실행 1회 / 누적)를 밝힌다.
- [ ] AC2: 두 미러의 run.sh 템플릿에 두 변수의 기본값 fallback과 정수 유효성 검사가 `MAX_LLM_FAILURES` 검사와 동일한 형태로 존재한다.
- [ ] AC3: run.sh 템플릿이 lock 획득 전에 시작 시각을 기록하고 `DEADLINE = 시작 + MAX_RUNTIME_MINUTES * 60`을 계산한다.
- [ ] AC4: while 루프 진입부(ITERATION 증가 전)에 두 상한 판정 분기가 있다 — 현재 시각이 `DEADLINE` 이상이거나 다음 `ITERATION`이 `MAX_ITERATIONS`를 넘으면, `state.md`의 `notes:`에 어느 상한에 걸렸는지 기록하고 재실행으로 이어갈 수 있다는 안내를 출력한 뒤 `exit 1`한다. 이 분기는 `phase:` 값을 변경하지 않는다.
- [ ] AC5: run.sh 템플릿에 진행 중인 `action.sh`를 시간 예산으로 중단시키는 코드가 없다(soft 판정 — `timeout`으로 action.sh를 감싸지 않는다).
- [ ] AC6: 두 미러의 CHECKS.md 템플릿 `## config.sh` 절에 두 변수의 정의 여부 항목이 추가된다.
- [ ] AC7: Step 4에서 고정 변수를 열거하는 곳이 코드 블록 1곳뿐이다. (초안은 산문 bullet도 4개 변수를 가리키도록 갱신하는 안이었으나, 블록 제목이 이미 "항상 포함"을 선언하므로 이중 진술을 제거하는 편이 "서로 어긋나지 않는다"를 더 강하게 달성한다 — simplicity 리뷰 M3 반영.)

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md` -- Step 3 CHECKS 템플릿, Step 4 고정 변수, Step 6 run.sh 템플릿
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- 동일 3개 지점

---

### Task 2: DONE 판정을 action.sh 실행 이후로 이동

`phase: DONE`으로 전환한 iteration이 함께 쓴 `action.sh`가 실행도 archive도 되지 않고 유실되는 경로를 없앤다. ANALYZING이 `final_report.md`를 action.sh로 생성하면 리포트가 아예 안 만들어진다. **이 task를 가장 먼저 적용한다** — 유일한 구조 이동이라, 나중에 하면 Task 1·3·6·7의 run.sh 편집과 diff가 겹친다.

**Contracts**: iteration 1회의 순서가 `루프 진입 DONE 가드 → 상한 판정 → LLM 사고 → state 검증 → action.sh 실행/archive → DONE 판정 → (DONE이면 break)`로 고정된다. DONE iteration에도 action.sh가 있으면 실행되고 `results/action_iter<N>.sh`로 archive된다. **DONE 판정 지점은 2곳이다** — 이미 `phase: DONE`인 state로 재실행할 때 LLM 턴을 쓰지 않고 즉시 끝내는 *진입 가드*(exit 0)와, 현재 run을 끝내는 *사후 판정*이다. 역할이 다르므로 복제가 아니다. (초안에서 "판정 1회"로 잡았던 계약은 틀렸다 — 이동만 하면 DONE 상태 재실행이 무인 LLM 턴 1회와 임의 action.sh 실행을 추가로 받는다.)

**Acceptance Criteria**:
- [ ] AC1: 두 미러의 run.sh 템플릿에서 `phase: DONE` grep 분기가 action.sh 실행 블록 **뒤**, iteration 종료 `sleep` **앞**에 위치한다 (DONE 시 sleep 없이 break).
- [ ] AC2: LLM 스텝 실패 retry 경로와 state.md 손상 retry 경로의 `continue`가 DONE 판정보다 앞에 남아, 실패 iteration에서 action 실행·DONE 판정이 모두 건너뛰어진다.
- [ ] AC3: run.sh 상단 주석의 "Flow per iteration" 4줄이 바뀐 순서를 반영한다.
- [ ] AC4: 두 미러의 run.sh 템플릿에서 `phase:` 값을 DONE인지 판정하는 grep 분기가 정확히 2곳 — 루프 진입 가드(LLM 호출 전, `break`)와 action 실행 뒤 사후 판정 — 에 나타나고, 그 외에는 없다.

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md` -- Step 6 run.sh 템플릿(헤더 주석 + while 루프 본문)
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- 동일 지점

---

### Task 3: claude 미러를 codex 미러 수준으로 parity backport

codex 미러에만 들어간 3건은 Codex CLI 적응 delta가 아니라 순수 개선이다. claude 미러에 반영하고, 그 과정에서 오진을 유도하는 실패 메시지를 고친다. claude 템플릿은 stream-json 파서로 `python3`를 무조건 사용하므로 `python3` preflight가 codex 쪽보다 더 필요하다(codex는 timeout fallback 경로에서만 사용).

**Acceptance Criteria**:
- [ ] AC1: claude 미러 run.sh 템플릿에 `command -v claude`와 `command -v python3` preflight가 lock 획득 전에 존재하고, 부재 시 각각 무엇이 없는지 명시하며 `exit 1`한다.
- [ ] AC2: claude 미러의 LLM 연속 실패 abort 메시지에서 원인을 단정하는 문구(`Check: claude CLI installed? API key valid? Network OK?`)가 제거되거나, preflight가 이미 검사한 항목을 재질문하지 않는 문구로 대체된다.
- [ ] AC3: claude 미러 Hard Rules에 codex 미러 Hard Rule 6과 동등한 "run.sh는 `#!/usr/bin/env bash` shebang과 실행 권한을 가진다" 규칙이 추가된다.
- [ ] AC4: claude 미러 CHECKS.md 템플릿 `## run.sh` 절에 CLI 호출 존재 확인 항목(claude CLI invocation present)이 추가된다.

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md` -- Hard Rules, Step 3 CHECKS 템플릿, Step 6 run.sh 템플릿

---

### Task 4: placeholder 검사를 실효 있는 형태로 교체

현재 AC4/CHECKS는 리터럴 문자열 `<placeholder>`만 본다. 템플릿이 실제로 남기는 미충전 슬롯은 `<main execution command>`·`<project name>` 형태라, 핵심 슬롯이 비어 있어도 통과한다.

**Contracts**: 검사 범위의 정의는 Part 1 "init 시점 placeholder 검사 범위 (단일 소스)" 문단이다. 아래 AC는 그 범위를 재서술하지 않고 참조한다.

**Acceptance Criteria**:
- [ ] AC1: 두 미러의 AC4가 리터럴 `<placeholder>` 대신 "Part 1 범위에 미충전 슬롯 0"을 기술하며, 검사 대상 파일·섹션이 스킬 본문 한 곳(Step 8)에만 열거된다.
- [ ] AC2: 두 미러의 Hard Rules "No Placeholders" 항목이 같은 기준으로 갱신되고, 범위는 Step 8을 가리키기만 한다(목록 복제 없음).
- [ ] AC3: 두 미러의 CHECKS.md 템플릿에서 `No <placeholder> strings remain` 항목이 교체되며, 교체된 문장에 리터럴 꺾쇠가 0개다(자기 자신을 매치시키지 않는다).
- [ ] AC4: 두 미러 Step 8에 검사 수단이 실행 가능한 형태로 기술된다 — `config.sh`·`run.sh`·`state.md`·`CHECKS.md`는 파일 전체를 `grep -nE '<[^>]+>'` 하고, `PROMPT.md`는 지정된 4개 섹션만 추출해 같은 패턴을 적용하며, 그 4개 섹션 밖은 검사하지 않음이 명시된다.
- [ ] AC5: 두 미러 전체에서 리터럴 `<placeholder>`를 검사 기준으로 삼는 문장이 0건 남는다.

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md` -- Acceptance Criteria, Hard Rules, Step 3 CHECKS 템플릿, Step 8
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- 동일 4개 지점

---

### Task 5: 문법 검사 도입 + AC2/AC3를 falsifiable하게 재작성

"Template Fidelity"가 산문 규칙으로만 강제되고 있어, 생성된 스크립트가 bash 문법 수준에서 깨져도 init 자체검증이 통과한다. 동시에 AC2("상태 머신이 정상 전환")·AC3("run.sh가 패턴을 정확히 구현")은 루프를 돌리기 전엔 판정 불가한 진술이라 다시 쓴다. 이 task가 덮는 것은 **bash 문법 범위까지**다 — 인용이 균형인 채 내용만 훼손된 경우(예: claude 미러의 인라인 python 필터)는 `bash -n`이 잡지 못하며, 그 위험은 Step 6의 기존 verbatim 복사 규칙이 담당한다.

**Acceptance Criteria**:
- [ ] AC1: 두 미러 Step 8에 `bash -n ralph/run.sh`와 `bash -n ralph/config.sh`를 실행하고 실패 시 해당 파일을 수정 후 재검증하는 절차가 추가된다.
- [ ] AC2: 두 미러의 CHECKS.md 템플릿 `## run.sh` 절에 `bash -n` 통과 항목이 추가된다.
- [ ] AC3: 두 미러 스킬 AC2가 "PROMPT.md에 7개 phase(또는 커스터마이즈된 등가 집합) 각각의 목적·실행 명령·전환 조건이 기술되고, `VALID_PHASES`가 그 집합과 일치한다"처럼 init 시점 관찰로 판정 가능한 문장으로 교체된다.
- [ ] AC4: 두 미러 스킬 AC3가 "run.sh가 `bash -n`을 통과하고 실행 권한을 가진다"처럼 init 시점 관찰로 판정 가능한 문장으로 교체된다.

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md` -- Acceptance Criteria, Step 3 CHECKS 템플릿, Step 8
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- 동일 3개 지점

---

### Task 6: `ralph/decisions.md` 생성 + tail 읽기 지침

PROMPT.md의 Iteration Protocol 3/10이 `decisions.md`를 읽고 쓰는데 어떤 Step도 이 파일을 만들지 않아, 첫 iteration이 없는 파일을 읽는다. 또 append-only 로그에서 "최근 15개"를 요구하면서 읽기 방법이 없어, 장기 루프에서 전체 로그를 읽는 컨텍스트 비대가 생긴다.

**Contracts**: 생성 산출물이 6파일이 된다. `decisions.md`는 append-only이며, 읽기는 항상 파일 끝 일부만 읽는다(로테이션 메커니즘은 두지 않는다).

**Acceptance Criteria**:
- [ ] AC1: 두 미러 **Step 7**에 `ralph/decisions.md`를 헤더 + 초기 엔트리로 생성하는 지시가 추가된다(두 미러 모두 같은 Step 번호에 위치한다).
- [ ] AC2: 두 미러의 AC1(5개 파일)이 `decisions.md`를 포함한 6개 파일로 갱신된다.
- [ ] AC3: 두 미러 Step 8 요약 출력의 "Files created" 목록에 `ralph/decisions.md`가 한 줄 추가된다.
- [ ] AC4: 두 미러 PROMPT.md 템플릿의 Iteration Protocol 3번이 "최근 15개 읽기" 대신 파일 끝 일부만 읽는 실행 가능한 지시(예: `tail -n 200 ralph/decisions.md`)로 교체된다.
- [ ] AC5: 두 미러 run.sh 템플릿의 `--reset` 블록이 `decisions.md`를 초기 상태로 되돌린다(잔존 결정 로그가 새 루프에 섞이지 않는다).
- [ ] AC6: 두 미러 CHECKS.md 템플릿에 `## decisions.md` 절이 추가되어 파일 존재 + 헤더/초기 엔트리를 확인한다 — 스킬 AC5("CHECKS.md의 모든 항목 통과")가 이 파일을 커버하게 한다.

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md` -- Acceptance Criteria, Step 3 CHECKS 템플릿, Step 5 PROMPT 템플릿, Step 6 run.sh `--reset` 블록, Step 7, Step 8
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- 동일 6개 지점

---

### Task 7: `state.md` dead schema 필드 제거

`errors` / `last_checkpoint` / `validation_results` 세 필드는 run.sh도 PROMPT.md도 읽거나 쓰지 않는다. 매 iteration LLM이 읽는 파일에 남은 미사용 스키마는 오해와 잡음이다.

**Acceptance Criteria**:
- [ ] AC1: 두 미러 Step 7의 `state.md` 초기 내용에서 세 필드가 제거되고 `phase`·`iteration`·`initialized_at`·`notes`만 남는다.
- [ ] AC2: 두 미러 run.sh 템플릿 `--reset` 블록의 state.md heredoc이 Step 7과 동일한 필드 집합을 쓴다.
- [ ] AC3: 두 미러 전체에서 제거된 세 필드명을 언급하는 문장이 0건 남는다(CHECKS.md 템플릿 포함).

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md` -- Step 6 run.sh `--reset` 블록, Step 7
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- 동일 2개 지점

---

### Task 8: "언제 쓰지 말 것" 경계 명시

`investigate`와 `goal-init`은 각자 ralph와의 경계를 선언해 뒀는데 ralph 본인만 침묵한다. 세션 하나 안에서 끝나는 루프까지 ralph로 끌고 오면 격리 환경 준비와 skip-permissions 비용을 헛되이 치른다.

**Acceptance Criteria**:
- [ ] AC1: 두 미러 도입부에 ralph 적합 조건(세션 수명 초과, 무인·격리 실행, iteration마다 fresh context 필요, 시간 단위 단일 실행)과 부적합 조건(단일 세션 안에서 닫히는 반복 작업)을 구분하는 2~3줄이 추가된다.
- [ ] AC2: 부적합 조건에서 대신 쓸 경로가 이름으로 지시된다 — 단발 디버깅은 `investigate`, 조건 충족까지의 세션 내 반복은 네이티브 `/goal`(그 조건·하네스 셋업은 `goal-init`).
- [ ] AC3: 추가된 문장이 `investigate`·`goal-init` SKILL.md의 기존 경계 진술과 모순되지 않는다.

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md` -- 도입부
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- 도입부

---

### Task 9: version lockstep 범프 (4필드)

repo 관행대로 SKILL.md frontmatter 2개 + skill.json 2개를 동시에 올린다. 생성 산출물 집합(5→6파일)과 `config.sh` 고정 변수 집합이 바뀌므로 patch가 아니라 minor다.

**Acceptance Criteria**:
- [ ] AC1: 네 곳(`{.claude,.codex}/skills/ralph-loop-init/{SKILL.md,skill.json}`)의 version이 모두 `4.1.0`이다.
- [ ] AC2: 네 값이 서로 불일치하지 않는다(grep 1회로 4건 모두 `4.1.0` 확인).

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md` -- frontmatter version
- [M] `.claude/skills/ralph-loop-init/skill.json` -- version
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- frontmatter version
- [M] `.codex/skills/ralph-loop-init/skill.json` -- version

---

### Task 10: 미러 대칭성 census 검증 (read-only)

두 벌 전파는 이 repo에서 잔존이 반복 재발한 패턴이다. Task 1~9가 한쪽 미러에만 반영된 항목이 없는지 전수 확인한다.

**Acceptance Criteria**:
- [ ] AC1: `MAX_RUNTIME_MINUTES`·`MAX_ITERATIONS`·`DEADLINE`·`decisions.md`·`bash -n`·`command -v` 각 키워드의 출현 건수를 두 미러에서 grep으로 대조하고, 비대칭이면 Codex CLI 적응 delta로 설명되는지 1줄씩 판정한다.
- [ ] AC2: 두 미러에서 리터럴 `<placeholder>`, `errors:`, `last_checkpoint`, `validation_results` 잔존이 각각 0건임을 grep으로 확인한다.
- [ ] AC3: 두 미러의 스킬 AC 목록(AC1~AC6)이 개수와 의미에서 대응하며, codex 미러 AC3의 Codex 적응 표현을 제외하면 문면이 일치함을 확인한다.
- [ ] AC4: codex 미러의 Codex CLI delta(`codex exec` 호출부, `--dangerously-bypass-approvals-and-sandbox`, `-o` last-message 처리, `command -v codex`)가 이번 수정으로 훼손되지 않았음을 확인한다.
- [ ] AC5: 잔존/비대칭 발견 시 해당 task로 돌아가 수정한 뒤 재검증한다(최대 2회).

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- **버전 범프 폭**: `4.1.0`(minor)으로 정했다. 직전 관행은 산문 제거에 patch(4.0.1)였으나 이번엔 생성 산출물 집합과 `config.sh` 고정 변수 집합이 바뀐다. 사용자 확인 불요 — 이견 있으면 Task 9만 조정.
- **상한 축**: 사용자 결정으로 wall-clock(`MAX_RUNTIME_MINUTES`, 기본 720 = 반나절)이 주 상한이고 `MAX_ITERATIONS`(기본 200)는 폭주 backstop이다. 시간 단위를 분으로 잡은 것은 정수 산술로 12시간(720)·하루(1440)·30분짜리 스모크 루프를 모두 표현하기 위함이다 — 시간 단위로 하면 1시간 미만을 못 준다. 사용자 확인 불요.
- **wall-clock은 soft 판정**: 사용자 결정. iteration 경계에서만 판정하므로 진행 중인 학습·빌드를 죽이지 않는 대신, 총 실행 시간이 마지막 action 길이만큼 예산을 초과할 수 있다(6시간짜리 action이 도는 루프에 12시간을 걸면 최대 18시간). 사용자 확인 불요.
- **상한 도달 시 동작**: `phase`는 보존하고 `notes`에만 기록한 뒤 `exit 1`로 정했다(plan-review High-1 반영). 무인 실행에서 상한 도달은 정상 완료가 아니므로 비-0이어야 하고, phase를 DONE으로 강제하면 상한을 올려도 재개가 안 되어 결과를 지우는 `--reset` 외에 회복 수단이 없어진다. 사용자 확인 불요.
- **plan-review 반영 완료**: High 2건(상한 의미론 미확정, placeholder 검사 자기참조·범위 이중 진술) 및 Medium 2건, Low 4건을 위 task에 반영했다. Low 중 "Task 2를 먼저 적용" 권고는 Task 2 본문에 편집 순서로 기록했다.
