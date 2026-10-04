# Goal: 하네스를 오케스트레이터 기반 multi-agent로 전면 재편하고 실측으로 교체한다

## 목표 서술
SDD 하네스를 SDD 철학(spec 중심 루프와 검증, Claude·Codex 공통 계약, 산출물 원칙)만 남기고 오케스트레이터 기반 multi-agent 방식으로 재편한다. 오케스트레이터 스킬(메인 루프)이 단계별 worker를 띄우고, 인계는 digest(방법·이유)와 state(상태, 리뷰어에게 주지 않음) 2파일로 하며, 구현은 task별 worker로 조건부 병렬 실행한다. 새 경로를 기존 옆에 만들고, Claude 쪽에서 신·구를 실측 비교해 합격하면 기본 경로로 교체하고 구 경로를 삭제한다.

왜 중요한가: 메인 맥락 보호와 병렬 벽시계 단축이 동기다. 과거 agent 기반 경로는 "메인 루프가 가진 맥락을 다시 파악하는 비용"으로 폐지됐으나, 2026-10-04 실측에서 그 비용의 실체(방법을 다시 알아내는 턴)와 해법(레시피형 digest로 cold start 약 4초)이 확인됐다. 설계 결정의 출처는 `_sdd/discussion/2026-10-04_discussion_orchestrator_harness_redesign.md`와 `_sdd/discussion/2026-10-04_discussion_subagent_cold_start.md`다.

## `/goal` 조건 문자열
> 아래 블록을 `/goal <조건>`에 그대로 넣는다. 평가자는 도구 없이 transcript만으로 판정하므로 자족적이어야 한다 — 단 자족의 단위는 outcome이다. 검증 명령·기대 출력·수치 등 브리틀 디테일은 여기 넣지 않고 아래 `검증 레시피` 섹션에 둔다.

DONE WHEN: 오케스트레이터 기반 multi-agent 하네스(오케스트레이터 스킬, digest·state 2파일 인계, task별 조건부 병렬 구현 worker, 작성자와 분리된 리뷰 worker)가 Claude·Codex 두 런타임의 스킬로 존재하는 기본 경로이고, 구 직접 실행 경로는 삭제되었으며, 변경이 `refactor/orchestrator-harness` 브랜치에 push되고 PR이 생성되었다(anchor: `gh pr view` 출력의 PR URL과 head 브랜치명 `refactor/orchestrator-harness`, state OPEN). 증명: `goal.md` 검증 레시피의 명령 실제 출력이 transcript에 surface되고 전 항목 PASS다.
DONE WHEN: Claude 쪽 신·구 경로 실측 비교가 끝나 검증 레시피의 합격 지표가 전부 PASS이고, 총 토큰과 체인 벽시계는 신·구 수치로 보고되었다(anchor: `/Users/hyunjoonlee/github/sdd_skills/_sdd/goal/2026-10-04_orchestrator_harness_redesign/report.md`의 Status가 PASS이고 측정 표가 있다). 증명: `goal.md` 검증 레시피의 명령 실제 출력이 transcript에 surface되고 전 항목 PASS다.
DONE WHEN: global spec(`_sdd/spec/`)이 새 하네스를 현재 진실로 기술하도록 spec-sync가 완료되었고, 재편과 충돌하던 구 Guardrail 문장이 남아 있지 않다. 증명: `goal.md` 검증 레시피의 명령 실제 출력이 transcript에 surface되고 전 항목 PASS다.
CONSTRAINTS: 검증 레시피 변경 시 변경 diff·사유를 transcript에 표시하며, 판정을 약화하는 변경은 사용자 승인이 필요하다. `goal.md` 자율 수행 위임의 사전 승인 범위에 있는 행동에 대해 사용자 확인을 요청하며 턴을 끝내지 않는다. SDD 철학 3종(spec 중심 루프와 검증, Claude·Codex 공통 계약, 산출물 원칙)을 어기지 않는다. 신 경로가 실측 합격하기 전에는 구 경로의 동작을 바꾸거나 삭제하지 않는다. Codex는 실측하지 않고 미러 정적 검사만 한다. PR merge와 main 브랜치 push는 하지 않는다.
STOP: after 3 turns without progress.

## 검증 레시피
매 턴 이번 진척에 필요한 허용된 검증을 실행하고 실제 출력을 대화에 표시한다. 실행하지 않은 필수 검증은 기존 evidence와 그 유효성·미실행 사유를 표시한다. repo의 slow/checkpoint·timeout 재실행 제한을 따르며, 매 턴 전체 명령을 재실행하지 않는다. 최종 PASS에는 모든 필수 검증의 유효한 실행 증거가 필요하다.

실행 checkpoint: R4(벤치마크 실측)는 10초를 넘는 느린 검증이다. 실측 feature를 닫을 때와 최종 PASS 직전에만 실행하고, 그 사이 턴에는 기존 evidence와 유효성을 표시한다. R1·R2·R3·R5는 수 초 이내라 해당 변경이 있는 턴에 실행한다.

### R1. 브랜치와 PR (DONE WHEN 1)
- `git -C /Users/hyunjoonlee/github/sdd_skills branch --show-current` → `refactor/orchestrator-harness`
- `git -C /Users/hyunjoonlee/github/sdd_skills status --short` → 미커밋 변경 없음(목표 시작 전부터 있던 `_COMMENTS.md`·`_sdd/work_log/2026-09-11.md`·`_sdd/work_log/2026-09-15.md` 변경은 제외)
- `gh pr view refactor/orchestrator-harness --json url,headRefName,state` → `state: OPEN`, `headRefName: refactor/orchestrator-harness`

### R2. 구조 (DONE WHEN 1)
- 새 오케스트레이터 스킬의 SKILL.md가 `.claude/skills/<이름>/`과 `plugins/sdd-skills-codex/skills/<이름>/` 두 곳에 있다. `<이름>`과 worker 계약 파일 목록은 첫 구조 feature의 draft가 정하고, 이 레시피에 동등 변경으로 기록한다.
- 구 직접 실행 경로의 census 목록(삭제 대상 스킬·절·문장)은 교체 feature의 draft가 정하고 여기에 기록한다. 판정: 그 목록의 `grep -rn -F '<리터럴>' .claude plugins docs` 결과가 모두 0건.

### R3. 정적 검증 (DONE WHEN 1)
- `git diff --check main...HEAD` → 출력 없음
- `claude plugin validate <plugin 경로>` → PASS. 정확한 경로는 첫 턴에 확인해 기록한다.
- Codex 미러: 짝마다 `/usr/bin/diff`(셸의 `diff`는 래퍼 함수라 쓰지 않는다)로 claude↔codex를 비교한다. hunk 수가 각 draft가 정한 기준선과 같고, 초과 hunk가 0이다.

### R4. 실측 (DONE WHEN 2, Claude만)
- 벤치마크 기능: PR #87 `review_evidence_floor`(base `97f3ea4^1`), PR #88 `goal_autonomy_grant`(base `d5c39b3^1`). 각 기능의 draft를 입력으로, base commit의 대상 worktree에서 구 경로와 신 경로를 각각 2회 실행한다. 두 회의 합격·불합격이 갈리면 1회 더 실행한다.
- 실행 방식: `claude -p`로 새 세션을 띄운다. harness는 `--plugin-dir`로 로드한다(구 = main, 신 = 브랜치 worktree). `--session-id`로 transcript 경로를 고정한다. 확정 명령: `bench/run.sh <87|88> <old|new> <rep> <plugin dir>`(대상 worktree의 bare 프로젝트 스킬은 `--disallowedTools`로 차단, 독립 리뷰는 `bench/review.sh`). 신 경로 plugin dir은 `bench/mkplug.sh <브랜치 worktree> <out>`으로 만든 래퍼다 — marketplace 루트를 그대로 주면 설치된 `sdd-skills`(main과 같은 커밋 `bee82a5` 캐시)가 로드되므로, 구 경로 run은 그 캐시가 곧 main 하네스다. 신 경로 run은 transcript의 `Base directory for this skill:`이 래퍼 경로인지 확인한다. headless(`-p`)에서 worker는 foreground로 실행되고 메인이 결과를 받은 뒤 진행한다(H2).
- 지표: transcript를 jq로 계측하고 경로별 중앙값을 쓴다. 판정 표는 `report.md`에 남긴다.
  - M1 메인 맥락 증가: 메인 세션의 (마지막 턴 input + cache_read + cache_creation) − (첫 턴 같은 합). 합격: 신 ≤ 구 × 0.5
  - M2 오케스트레이터 일탈: 신 경로 메인 세션에서 대상 파일에 대한 `Edit`·`Write` tool_use 수 + 파일을 쓰는 `Bash` 명령 수(리다이렉트·`sed -i`·`tee`·`cp`/`mv`/`rm`·스크립트 내 파일 쓰기, `bench/metrics.py`의 `bash_writes`)(digest·state·`_sdd/goal/`·`_sdd/implementation/`·`_sdd/work_log/`·임시 경로 제외). 합격: 0
  - M3 cold start: 각 worker를 띄운 뒤 첫 실질 작업(digest·draft 읽기를 제외한 첫 검사·편집 tool_use)까지의 시간. 합격: 중앙값 ≤ 10초
  - M4 품질: 신 경로 결과물에서 draft의 AC가 전부 fresh 검증으로 MET이다. 그리고 별도로 띄운 새 agent 단독 독립 리뷰(지시문 고정, 맥락 미제공)에서 Critical·High가 0이다. 합격: 둘 다 충족
  - M5 보고만(합격 기준 없음): 총 토큰(입력 + 출력 + cache read + cache creation)의 신/구 비율, 체인 벽시계의 신/구 비율

### R5. spec (DONE WHEN 3)
- `grep -n '^\*\*Spec Version' /Users/hyunjoonlee/github/sdd_skills/_sdd/spec/main.md` → main 대비 버전이 올라갔다.
- 구 Guardrail census: 아래 리터럴이 `_sdd/spec/main.md`·`_sdd/spec/components.md`에서 0건이다. spec 갱신 feature가 목록을 확정·보강한다.
  - `코드·테스트는 메인 루프가 직접 작성`
  - `custom agent는 **0종**`
  - `reviewer들은 ledger를 소비하지 않는다`
  - `ledger MET 접기` — `main.md`에서만 센다(`:76`·`:82`의 stale 참조). `components.md`의 pr-review 행에 있는 같은 말은 현재 유효한 계약이라 제외한다.

## 자율 수행 위임
이 섹션은 루프 중 행동에 대한 사용자의 사전 승인이다. 하류 스킬·런타임 규범이 요구하는 '실행 전 확인'은 사전 승인 목록에 있는 행동에 한해 이 섹션으로 충족된다.

사용자 확인이 필요해 보이는 행동은 이 섹션으로 판정한다.
- 사전 승인 범위 안: 확인 없이 수행하고 결정·근거를 `journal.md`에 남긴다.
- 범위 밖: 그 행동 없이 진척 가능한 일을 먼저 한다.
- 범위 밖이고 그 행동 없이는 진척 불가: `report.md` Status를 `STUCK`으로 두고 사유를 적은 뒤 미완료로 종료한다.

- 수준: unattended
- 사전 승인: 브랜치 생성·commit·feature 브랜치 push·PR 생성 / 테스트·빌드·스크립트 실행(`claude -p` 벤치마크 세션 포함)·의존성 설치 / repo 안 파일 생성·수정·삭제(구 경로 삭제는 실측 합격 후) / scratchpad·git worktree 생성·삭제 / `spec-sync` 실행 / 검증 레시피의 동등·강화 변경
- BC 리소스 상한: 해당 없음
- 비용 상한: 없음. 총 토큰과 벽시계는 보고만 한다.
- 항상 확인(제외, 수준 무관): main/protected 브랜치 직접 push·force-push·history rewrite / PR merge / 원격·공유 자원 삭제(브랜치·인스턴스·스토리지) / 리소스·비용 상한 초과 / 판정을 약화하는 레시피 변경 / 시크릿 취급 / repo 밖 외부 발신

## Loop Protocol
매 턴 다음을 순서대로 수행한다 (이 섹션은 메인 에이전트용 HOW이며 조건 문자열에 넣지 않는다):
1. 아직 충족되지 않은 `DONE WHEN` 또는 실패한 final integration proof가 드러낸 gap에서 가장 작은 next feature를 고른다. `experiments.md`의 pending 가설은 접근 후보로만 참고한다.
2. 그 feature의 reviewed draft가 없으면 `feature-draft`를 실행한다. draft가 분할되면 현재 native goal 안에서 가장 작은 next unit을 고르고 nested `goal-init`은 만들지 않는다.
3. 선택한 draft를 `implementation`으로 구현하고 producer-owned 품질 게이트 결과까지 닫는다.
4. persistent 변경이 있으면 `spec-sync`를 실행한다.
5. `검증 레시피`의 실행 규칙에 따라 evidence를 대화에 표시하고 evidence·완료 feature·남은 gap·next action을 `journal.md`에 append한 뒤 `report.md`를 갱신한다.
6. 모든 `DONE WHEN`과 final integration proof가 통과했을 때만 성공 종료한다. STOP 또는 위임 범위의 STUCK 경계에 도달하면 `report.md`에 사유를 기록하고 미완료로 종료한다. native goal lifecycle 처리는 활성 런타임 규범을 따른다. 그 외에는 1단계로 돌아간다.

> Setup invariant: goal을 활성화하지 않았으며 기존 goal 상태도 변경하지 않았다.

## 실행법
<!-- SKILL.md Handoff의 실행법으로 자기 런타임 슬롯만 채운다. 다른 런타임 슬롯은 placeholder로 둔다. -->

### Claude Code
- (a) workspace trust + hooks가 활성화되어 있어야 `/goal` 루프가 동작한다.
- (b) 라이프사이클은 `/goal set`(목표 설정)·`/goal status`(진행 확인)·`/goal clear`(종료)이며, `clear`는 별칭(`stop`·`off`·`reset` 등)으로도 호출할 수 있다.
- (c) 세션을 멈췄다 `--resume`/`--continue`로 이어가면 active goal이 복원되며 턴·타이머·토큰 카운터가 리셋된다.
- (d) 평가자는 조건 문자열을 4,000자 상한으로 읽으므로, 그 안에서 도구 없이 판정 가능한 evidence가 매 턴 surface되어야 한다.

### Codex
<Codex 스킬이면 SKILL.md Handoff의 Codex 실행법 4요소를 기입; 아니면 placeholder 유지>
