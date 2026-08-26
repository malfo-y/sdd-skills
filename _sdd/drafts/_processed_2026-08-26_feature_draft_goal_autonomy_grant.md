# Feature Draft: goal 하네스 자율 수행 위임(Autonomy Grant)

> 규모 판정: 적격 — 변경 요소 7종(goal-init 본문·템플릿·예제·autopilot·git·가이드 ko/en·미러)이 각각 한 task에 1:1 귀속, 전파형이라 census 검증 task를 마지막에 둔다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
native `/goal` 루프 중 에이전트가 commit·push·BC 태스크 제출 같은 행동 앞에서 사용자 확인을 요청하며 턴을 끝내는 일이 반복된다. 확인 요청의 출처는 goal-init이 아니라 하류다 — `git` 스킬의 CONFIRM 승인 대기(AC3·AC4), 런타임·도구 규범("되돌리기 어려운 행동은 확인"), bc-mcp의 quota 안내. `/goal` 루프에서는 사용자가 답할 수 없으므로 이 대기는 곧 무진척이다.

**새 contract**: `goal.md`에 `자율 수행 위임` 섹션을 둔다. 이 섹션은 루프 중 행동에 대한 **durable authorization**이다 — 사용자가 setup 시 정한 수준(`unattended` | `attended`)과 사전 승인/제외 행동 목록을 담고, 하류 스킬·런타임 규범의 "확인 후 실행"은 이 섹션의 사전 승인으로 충족된다. `git` 스킬은 이 위임을 인정한다(위임이 commit/push를 승인하면 CONFIRM은 계획 표시만 하고 대기 없이 EXECUTE). `goal-init` Goal Intake는 자율 수준을 확정한다 — 사용자 원문에 "알아서/자율/무인/확인 없이" 신호가 있으면 `unattended`, 없으면 1회 질문. Loop Protocol(generic·SDD 양쪽)에 질문 대체 규칙이 들어간다 — 위임 범위 내 애매함은 가장 합당한 선택 후 `journal.md`에 결정·근거 기록, 범위 밖은 그 행동 없이 진척 가능한 일을 먼저 하고 블로킹이면 `report.md` `STUCK`으로 종료. 조건 문자열 `CONSTRAINTS` 표준 문구에 "위임 범위 내 행동에 대해 사용자 확인을 요청하며 턴을 끝내지 않는다"가 추가된다(평가자가 transcript만으로 판정 가능). 기존 "판정 약화 레시피 변경은 사용자 승인" 불변 — 위임 수준과 무관하게 항상 제외 목록.

## Scope
- **In**: `goal-init` SKILL(Step 1·Step 4·Key Principles·AC4)·`references/harness-templates.md`(goal.md 템플릿 섹션 + CONSTRAINTS 표준 문구 + 두 payload의 질문 대체 단계)·`examples/sample-goal-init-session.md`(섹션 예시 + 핵심 포인트 1줄), `sdd-autopilot` SKILL(Step 3 relay에 위임 범위), `git` SKILL(위임 인정 1절), `docs/AUTOPILOT_GUIDE.md` ko/en(§4 경계 1줄·§5 사용자 역할 1행), codex 미러(goal-init·sdd-autopilot; git은 codex 부재).
- **Out**: `AGENTS.md`(spec-sync 확인 문구 — SDD payload가 spec-sync를 직접 실행하므로 무관), bc-mcp 서버 지시문(외부), `ralph-loop-init`, 런타임 permission 설정(settings.json allowlist — 하네스 밖 관심사), spec surface(`spec-sync` 단계).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: harness-templates에 자율 수행 위임 섹션·표준 문구·질문 대체 단계 추가
템플릿이 단일 소스이므로 shape는 여기서 먼저 확정한다.

**Contracts**:
- `goal.md` 템플릿에 `## 자율 수행 위임` 섹션(위치: `검증 레시피` 다음, `Loop Protocol` 앞). 슬롯: `수준: <unattended | attended>`, `사전 승인:` 목록, `항상 확인(제외):` 목록, 그리고 고정 문장 "이 섹션은 루프 중 행동에 대한 사용자의 사전 승인이다. 하류 스킬·런타임 규범이 요구하는 '실행 전 확인'은 사전 승인 목록에 있는 행동에 한해 이 섹션으로 충족된다." `attended`면 사전 승인 목록을 비우고 제외 목록만 둔다.
- 기본 사전 승인(unattended): 브랜치 생성·commit·feature 브랜치 push·PR 생성 / 테스트·빌드·스크립트 실행·의존성 설치 / repo 안 파일 생성·수정·삭제 / `spec-sync` 실행 / 검증 레시피의 동등·강화 변경 / BC 태스크 제출·인스턴스 생성(quota는 표시하되 대기 없음, 사용자가 정한 리소스 상한 내).
- 기본 항상 확인(제외, 수준 무관): main/protected 브랜치 직접 push·force-push·history rewrite / PR merge / 원격·공유 자원 삭제(브랜치·인스턴스·스토리지) / 리소스·비용 상한 초과 / 판정을 약화하는 레시피 변경 / 시크릿 취급 / repo 밖 외부 발신.
- `CONSTRAINTS` 표준 문구 끝에 추가: "`goal.md` 자율 수행 위임의 사전 승인 범위에 있는 행동에 대해 사용자 확인을 요청하며 턴을 끝내지 않는다."
- 질문 대체 규칙은 섹션 고정 문장이 소유한다(payload에는 넣지 않는다 — gate 1 simplicity M1로 정정: 두 payload verbatim 복제 제거, 예제·가이드 §3 단계 열거도 그대로 유효): "사용자 확인이 필요해 보이는 행동은 이 섹션으로 판정한다 — 사전 승인 범위면 확인 없이 수행하고 결정·근거를 `journal.md`에 남긴다. 범위 밖이면 그 행동 없이 진척 가능한 일을 먼저 하고, 그것 없이는 진척이 불가능하면 `report.md` Status를 `STUCK`으로 두고 사유를 적은 뒤 종료한다."

**Acceptance Criteria**:
- [ ] AC1 (1등급): claude·codex 템플릿 모두 `grep -c '^## 자율 수행 위임'` = 1, 섹션이 `## 검증 레시피`와 `## Loop Protocol` 사이에 위치(`grep -n` 줄 순서 비교).
- [ ] AC2 (1등급): 두 템플릿에서 `grep -c '사용자 확인을 요청하며 턴을 끝내지 않는다'` = 1(CONSTRAINTS 줄), `grep -c '이 섹션으로 판정한다'` = 1(섹션 고정 문장), payload 구간의 `자율 수행 위임` 언급 0.
- [ ] AC3 (1등급): `rtk proxy diff` claude↔codex 템플릿 hunk 수 = 2(변경 전 실측 — 실행법 슬롯 구간 40·46-48행; rtk 필터 diff는 오탐이라 proxy 필수).

**Target Files**:
- [M] `.claude/skills/goal-init/references/harness-templates.md` -- 섹션·표준 문구·payload 단계
- [M] `plugins/sdd-skills-codex/skills/goal-init/references/harness-templates.md` -- 동일 변경(기존 delta는 실행법 슬롯 2 hunk뿐)

### Task 2: goal-init SKILL에 자율 수준 확정과 섹션 기입 규칙
Step 1에서 수준을 정하고 Step 4에서 섹션을 채운다. 새 AC를 추가하지 않고 AC4(4파일 생성)에 섹션 기입을 흡수한다.

**Contracts**:
- Step 1 Goal Intake에 항목 추가: 사용자 원문에 자율 수행 신호("알아서", "자율", "무인", "확인 없이", "묻지 말고" 등)가 있으면 `unattended`로 확정하고 되묻지 않는다. 신호가 없으면 Decision Gate 1→2 전에 `AskUserQuestion` 1회로 `unattended`(권장 — 루프 중 사용자가 답할 수 없음) | `attended`를 정한다. 사용자가 사전 승인/제외 목록을 조정하면 반영한다.
- Step 4에 항목 추가: `goal.md` `자율 수행 위임` 섹션을 확정 수준·목록으로 기입한다(템플릿 기본 목록 + 사용자 조정).
- Key Principles에 1항목: **위임은 durable authorization** — 루프 중 확인 요청은 사용자가 답할 수 없어 무진척과 같다. 확인이 필요한 행동은 setup에서 미리 위임 범위로 정한다.
- AC4를 "4파일이 생성되었고 `goal.md`에 확정 수준의 `자율 수행 위임` 섹션이 있다"로 개정.

**Acceptance Criteria**:
- [ ] AC1 (1등급): claude·codex SKILL 모두 `grep -c 'unattended'` ≥ 2줄(Step 1·AC4 — Step 4는 gate 1 simplicity M2로 템플릿 슬롯 참조만 남김), `grep -n '^- \[ \] AC4:'` 출력에 "자율 수행 위임" 포함.
- [ ] AC2 (2등급): Step 1의 신호 목록에 "알아서"가 있고, 신호 부재 시 질문이 정확히 1회임이 문면에 있다(`grep -c '1회'` Step 1 구간 ≥ 1).
- [ ] AC3 (1등급): `rtk proxy diff` claude↔codex SKILL hunk 수 = 6(변경 전 실측 — 런타임 어휘 6곳).

**Target Files**:
- [M] `.claude/skills/goal-init/SKILL.md` -- Step 1·Step 4·Key Principles·AC4
- [M] `plugins/sdd-skills-codex/skills/goal-init/SKILL.md` -- 동일

### Task 3: git 스킬이 위임을 인정
루프 중 commit/push 대기의 직접 원인 제거. codex에는 git 스킬이 없다.

**Contracts**: Phase 3 CONFIRM 첫 단락 뒤에 1절 — "**예외(goal 위임)**: 활성 goal 하네스의 `goal.md` `자율 수행 위임` 섹션이 commit·push를 사전 승인하면, 계획은 동일하게 표시하되 승인 대기 없이 EXECUTE로 진행한다. 이때 AC3·AC4의 '승인'은 그 위임으로 충족된다. 제외 목록(main 직접 push·force-push 등)은 위임과 무관하게 승인 대상이다." 활성 goal 하네스 식별: 이번 대화에서 Loop Protocol로 읽고 있는 `goal.md`(조건 문자열에 경로가 없어도 메인 에이전트가 매 턴 읽는 파일).

**Acceptance Criteria**:
- [ ] AC1 (1등급): `.claude/skills/git/SKILL.md`에서 `grep -c '자율 수행 위임'` ≥ 1이고 그 줄이 `## Phase 3: CONFIRM`과 `## Phase 4: EXECUTE` 사이에 있다.
- [ ] AC2 (1등급): AC3·AC4·Hard Rule·Phase 4 서두가 "(또는 Phase 3 goal 위임)"을 in-place로 담고, CONFIRM 절에 AC 원격 재해석 문장이 없다(`grep -c "AC3·AC4"` = 0) — gate 2 simplicity로 원안(AC 불변 + 재해석)을 정정.

**Target Files**:
- [M] `.claude/skills/git/SKILL.md` -- Phase 3 예외 절

### Task 4: sdd-autopilot relay·예제·가이드 갱신
표면 동기화. 로직 추가 없음.

**Contracts**:
- `sdd-autopilot` Step 3 relay 항목에 "자율 수행 위임의 수준과 사전 승인 범위"를 추가(AC4 relay 목록에도).
- 예제 `goal.md`에 `## 자율 수행 위임` 4줄 예시(unattended), 핵심 포인트에 1줄.
- `docs/AUTOPILOT_GUIDE.md` ko/en §4 경계에 "자율 수행 위임" 1줄, §5 사용자 역할 표에 "Goal Intake — 자율 수준(unattended/attended)과 위임 범위 확정" 행.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `grep -c '자율 수행 위임'`이 claude·codex `sdd-autopilot/SKILL.md` ≥ 1, claude·codex 예제 ≥ 2(goal.md 섹션 + 핵심 포인트), `docs/AUTOPILOT_GUIDE.md` ≥ 2; `docs/en/AUTOPILOT_GUIDE.md`에 `grep -c 'Autonomy Grant'` ≥ 2.
- [ ] AC2 (1등급): 예제 codex `rtk proxy diff` hunk 수 = 10(변경 전 실측) — 새 줄은 양쪽 동일.
- [ ] AC3 (1등급): sdd-autopilot claude↔codex `rtk proxy diff` hunk 수 = 3(변경 전 실측).

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md`, `plugins/sdd-skills-codex/skills/sdd-autopilot/SKILL.md`
- [M] `.claude/skills/goal-init/examples/sample-goal-init-session.md`, `plugins/sdd-skills-codex/skills/goal-init/examples/sample-goal-init-session.md`
- [M] `docs/AUTOPILOT_GUIDE.md`, `docs/en/AUTOPILOT_GUIDE.md`

### Task 5: census (read-only)
전파형 변경 — 용어 변형과 미러 짝을 전수로 닫는다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `grep -rn '자율 수행 위임' .claude plugins docs` 파일 집합 = Task 1~4 Target Files 전체(git·en 제외 시 `Autonomy Grant`로 대체) — 누락 파일 0.
- [ ] AC2 (1등급): 변형 표기(`자율수행 위임`, `자율 수행위임`, `Autonomy grant`, `autonomy-grant`) grep 0건.
- [ ] AC3 (1등급): `git diff --check` 무출력.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- 기본 사전 승인 목록에 "BC 태스크 제출·인스턴스 생성"을 포함(리소스 상한은 사용자가 Goal Intake에서 지정, 미지정이면 quota 표시 후 최소 구성). 사용자 확인 불필요 — 형님 원문("BC 제출이나 커밋")이 근거.
- `attended` 수준에서도 제외 목록은 항상 유지. 확인 불필요.
