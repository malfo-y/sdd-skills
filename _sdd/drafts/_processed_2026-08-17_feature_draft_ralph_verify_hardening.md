# Feature Draft: ralph-loop-init 검증 구조화 (verify.sh 분리 + DONE 게이트)

> 규모 판정: 적격 — 변경 표면이 SKILL.md 2벌(claude/codex 미러)로 닫히고 요소↔task 대응이 눈검산 가능

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
ralph-loop-init이 생성하는 무인 루프의 "자가 성공 선언" 경로를 프롬프트 순종이 아닌 구조로 차단한다. (1) init 시점에 확정된 검증 명령을 루프 LLM이 편집하지 않는 고정 `ralph/verify.sh`로 굳히고, (2) run.sh가 DONE 수용 시 `final_report.md` 존재·`Final status:` 라인을 확인하며 status가 PASS일 때만 verify.sh exit 0을 추가 요구한다(STUCK/FAIL 에스컬레이션 DONE은 verify 없이 수용). (3) PROMPT.md Self-correction의 targeted edit에서 Success Criteria·Escalation 섹션과 verify.sh를 편집 금지 구역으로 명시하고, 기준이 틀렸다고 판단되면 수정 대신 STUCK 에스컬레이션하게 한다. (4) 에스컬레이션 경로도 final_report.md 작성 후 DONE 전환을 의무화한다. (5) action.sh Rules에 장기 실행 in-run 조기 중단 가드 지침, (6) PROMPT.md 상단에 `_sdd/` 수정 금지, (7) 마감 요약에 final_report 회수 경로를 추가한다.

새 contract: **ralph 생성물의 판정 단일 소스는 `ralph/verify.sh`(exit code)이며, run.sh의 DONE 게이트 계약은 "final_report.md의 `Final status:` 존재 + (PASS 주장 시) verify.sh exit 0"이다.**

## Scope
- **In**: `.claude/skills/ralph-loop-init/SKILL.md`·`.codex/skills/ralph-loop-init/SKILL.md`의 생성 절차(Step 4·8)·run.sh 템플릿·PROMPT.md 템플릿·CHECKS.md 템플릿·AC/Hard Rules 문면
- **Out**: 기존에 이미 생성된 소비 repo의 ralph/ 디렉토리 마이그레이션, goal-init·다른 스킬, run.sh의 락·타임아웃·예산 등 기존 컨트롤 로직 변경
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: run.sh 템플릿에 DONE 구조 게이트를 넣는다
run.sh의 DONE 감지(`phase: DONE` grep) 지점에서 phase 문자열만으로 루프가 종료되는 경로를 막는다.

**Contracts**: DONE 게이트 — `ralph/results/final_report.md`가 존재하고 비어있지 않고 `Final status:` 라인을 가져야 DONE을 수용한다. `Final status: PASS`이면 추가로 `bash ralph/verify.sh` exit 0을 요구한다. 불충족 시 phase를 `ADJUST_PHASE` 변수(run.sh 상단 정의, 기본 `ADJUSTING`)의 값으로 되돌리고 `notes:`에 reject 사유를 기록한 뒤 루프를 계속한다(같은 원인 반복은 LLM측 3회 에스컬레이션 규칙이 흡수). phase 커스터마이즈와의 충돌을 막기 위해 Step 6의 허용 수정 문면을 "`VALID_PHASES`와 `ADJUST_PHASE`를 PROMPT.md phase 집합에 맞춘다"로 확장한다. PASS가 아닌 status(FAIL/STUCK/UNKNOWN ERROR)는 verify 없이 수용한다. 사전 루프의 "already DONE" 체크는 재실행 no-op 경로이므로 게이트를 적용하지 않는다.

**Acceptance Criteria**:
- [ ] AC1: claude SKILL.md의 run.sh 템플릿 fenced block을 추출해 `bash -n`이 통과한다. 평가: 추출 스크립트 실행 + exit 0 출력. (1등급)
- [ ] AC2: 추출한 템플릿에 DONE 게이트 로직이 존재한다 — `Final status:` grep과 `verify.sh` 실행이 DONE 감지 블록 안에 있다. 평가: `grep -n 'Final status:'`·`grep -n 'verify.sh'` 결과가 DONE 체크 함수/블록 내부 줄 번호를 가리킴. (1등급)

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md` -- Step 6 run.sh 템플릿에 DONE 게이트 추가

### Task 2: verify.sh 생성 절차와 셋업 표면을 갱신한다
Step 2 hard gate에서 확정한 "명령어 + 판정 조건"을 고정 실행 파일로 굳히고, 생성 파일 수 변화를 스킬의 자기 검증 표면(AC·Hard Rules·CHECKS.md 템플릿·Step 8·마감 요약)에 반영한다.

**Contracts**: Step 4가 `config.sh`와 함께 `ralph/verify.sh`를 생성한다(shebang·`set -euo pipefail`·Step 2 확정 명령·exit code 판정·chmod +x). 파일 수는 6→7. Step 8 검사(문법·슬롯)에 verify.sh가 들어가고, CHECKS.md 템플릿에 verify.sh 항목과 Task 1·3 산출물의 검증 항목(run.sh DONE 게이트·PROMPT.md 편집 금지 구역·in-run 가드·escalation report 의무)이 들어가며, 마감 요약 Files created에 verify.sh, Next steps에 `ralph/results/final_report.md` 회수 안내가 들어간다.

**Acceptance Criteria**:
- [ ] AC1: claude SKILL.md에서 verify.sh가 스킬 AC(7개 파일)·Step 4 생성 절차·Step 8 검사 범위·CHECKS.md 템플릿·마감 요약 5개 섹션 각각에 등장하고, CHECKS.md 템플릿에 DONE 게이트·편집 금지 구역·in-run 가드·escalation report 검증 항목이 존재한다. 평가: 섹션별 anchor grep 히트 확인. (1등급)
- [ ] AC2: 마감 요약 Next steps에 `final_report.md` 경로 안내 라인이 존재한다. 평가: `grep -n 'final_report.md'`가 Step 8 요약 fenced block 내부를 가리킴. (1등급)

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md` -- AC·Hard Rules·Step 4·Step 8·CHECKS.md 템플릿 갱신

### Task 3: PROMPT.md 템플릿에 편집 금지 구역과 루프 행동 규칙을 넣는다
루프 LLM을 향한 규칙 5종을 PROMPT.md 골격에 추가한다.

**Contracts**: (a) Success Criteria 판정의 단일 소스는 `bash ralph/verify.sh` exit 0이며 CHECKING 계열 phase가 이를 실행한다. (b) Self-correction의 PROMPT.md targeted edit에서 Success Criteria·Escalation 섹션과 `ralph/verify.sh`는 편집 금지 — 기준이 잘못됐다고 판단되면 수정하지 않고 STUCK 에스컬레이션한다. (c) 에스컬레이션(STUCK/UNKNOWN ERROR/외부 조치)도 `Final status:`를 담은 final_report.md를 쓴 뒤 DONE으로 전환한다. (d) action.sh Rules에 장기 실행 명령의 in-run 가드(로그 주기 감시로 발산·NaN·정체 시 조기 kill) 지침 1줄. (e) 상단 IMPORTANT에 `_sdd/` 수정 금지 1줄.

**Acceptance Criteria**:
- [ ] AC1: PROMPT.md 템플릿 fenced block 안에 (a)~(e) 각각에 대응하는 문면이 존재한다. 평가: 항목별 anchor grep(`verify.sh`·`편집 금지`(또는 등가 영문)·`Final status`·in-run 가드 문구·`_sdd/`) 5건 모두 히트. (1등급)
- [ ] AC2: 기존 Escalation 3회 규칙·self-correction 허용 자체는 유지된다(금지 구역만 추가). 평가: `같은 원인 3회`·`targeted edit` 문구 잔존 grep. (1등급)

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md` -- Step 5 PROMPT.md 골격 + State Machine Reference Escalation 문면 갱신

### Task 4: codex 미러에 3-way 전파한다
Task 1~3의 새 본문을 codex 적응 delta(codex CLI invocation·spawn 어휘 등) 위에 재적용한다 — 단순 복사 금지.

**Acceptance Criteria**:
- [ ] AC1: Task 1~3의 각 AC grep을 codex SKILL.md에 적용해 동일하게 통과한다. 평가: 동일 grep 세트 재실행 출력. (1등급)
- [ ] AC2: codex 고유 요소(`codex exec` invocation, `codex` CLI 체크)가 변경 후에도 잔존한다. 평가: `grep -n 'codex exec'`·`grep -n 'command -v codex'` 히트. (1등급)

**Target Files**:
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- 3-way merge 전파

### Task 5: 미러 동등성·잔존 검증 (read-only)
변경 구간의 claude/codex 문면 차이가 의도된 codex 적응 delta뿐인지, 파일 수 표기(6개)가 잔존하지 않는지 검증한다.

**Acceptance Criteria**:
- [ ] AC1: 두 SKILL.md의 verify.sh·DONE 게이트·PROMPT.md 규칙 구간 diff에서 비적응 차이가 0건이다. 평가: 해당 구간 추출 후 `diff` 출력 검토(적응 delta 목록 명시). (2등급 — rubric: CLI 이름·spawn 어휘 외 차이 없음)
- [ ] AC2: 두 파일에서 생성 파일 수를 6으로 세는 문면이 0건이다. 평가: `grep -n '6개 파일' .claude/skills/ralph-loop-init/SKILL.md .codex/skills/ralph-loop-init/SKILL.md` 무히트(exit 1). (1등급)

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- DONE reject 시 복귀 phase는 `ADJUST_PHASE` 변수(기본 ADJUSTING)로 결정 — 직전 phase 복원은 state 백업 시점 문제로 복잡도만 늘리고, 진단·수정 phase 복귀가 의미상 맞으며, 변수화로 phase 커스터마이즈와의 충돌을 해소(gate 1 High 반영). 사용자 확인 불필요.
- verify.sh 실패가 반복되며 LLM이 계속 PASS 주장 DONE을 시도하는 무한 reject는 별도 카운터 없이 LLM측 "같은 원인 3회 → STUCK" 규칙과 MAX_ITERATIONS 백스톱에 맡김 — run.sh에 카운터를 더 두는 것은 YAGNI로 판단. 사용자 확인 불필요.
