# Feature Draft: digest 운영 개선 — 환경 함정의 env.md 승격, 일회성 입력 금지

> 규모 판정: 적격 — 변경 요소 6개(spec-sync 계약 ×2 runtime, SKILL 단계 표 행, SKILL digest 초기화 문장, SKILL 인계 파일 digest.md 규칙, `_sdd/env.md` 시드)가 각각 owner task 하나(T1: 앞 셋, T2: digest.md 규칙, T3: 시드)에 배정되어 눈으로 검산된다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
`sdd-orchestrator` 인계 digest의 두 가지 운영 결함을 고친다. (1) 실행 중 알아낸 환경 함정이 digest와 함께 사라져 다음 실행이 같은 시행착오를 반복한다. (2) fix findings·task 한정 지시 같은 일회성 입력과 닫힌 fix 전용 check 행이 digest에 쌓여, 모든 worker가 읽는 digest가 현재 유효하지 않은 내용을 담는다. 이와 함께 이 저장소의 `_sdd/env.md`에 사용자가 승인한 환경 사실 7개를 시드한다.

- 새 invariant: 실행 끝(spec-sync 단계)에 spec-sync worker가 digest `환경 함정` 중 저장소 작업 전반에 반복 적용되는 사실을 `_sdd/env.md`로 승격한다. 메인 루프는 `_sdd/env.md`를 쓰지 않는다. 다음 실행은 digest 초기화에서 진입 경로(계획 단계·draft 진입)와 관계없이 `_sdd/env.md`의 환경 함정을 받는다.
- 새 invariant: digest에는 일회성 입력(fix할 findings·task 한정 지시)을 넣지 않는다. 이들은 `Worker dispatch` 입력으로만 넘긴다. finding 하나만 검증하는 fix 전용 check 행은 그 fix가 닫히면 digest 검증 레시피에서 지운다.

## Scope
- **In**: 양 runtime `sdd-orchestrator`의 `references/workers/spec-sync.md`(승격 규칙), `SKILL.md`의 `단계와 진입` 표 spec-sync 행, `인계 파일`의 digest 초기화 문장(계획 단계 경로에 env.md 추가)과 digest.md 규칙. 이 저장소 `_sdd/env.md`에 승인 7개 사실 시드.
- **Out**: 새 worker나 새 계약 파일. `역할 경계`의 env.md 읽기 규칙(이미 env.md 읽기를 허용한다). `handoff-templates.md`(규칙은 SKILL `인계 파일` 절이 소유). spec-create의 env.md 생성 템플릿. global spec 반영(이 실행의 spec-sync 단계가 맡는다).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: spec-sync worker가 digest 환경 함정을 `_sdd/env.md`로 승격하게 한다
승격 주체를 spec-sync worker로 정한다. 이 worker는 기본 종점의 마지막 단계이고, 이미 digest를 읽으며, "persistent repo-wide information만 가장 맞는 surface에 보수적으로 반영"하는 같은 원칙을 쓴다. 그래서 새 worker나 계약이 필요 없다. env.md의 절 이름은 고정하지 않는다(다른 task와 상수를 공유하지 않게 한다).

**Contracts**:
- `spec-sync.md` `### Step 5: Apply Updates`에 항목 하나를 추가하고 도입 문장의 표면 수를 맞춘다. 승격 기준의 단일 소유자는 이 항목이다. 아래 여섯 요소를 담는다.
  1. 대상: digest `환경 함정` 중 이번 기능을 넘어 저장소 작업에 반복 적용되는 사실.
  2. 위치: `_sdd/env.md`에서 가장 맞는 기존 절. 맞는 절이 없으면 새 절을 만든다.
  3. 중복: 이미 있는 사실은 다시 쓰지 않는다. 어긋나는 기존 항목은 고쳐 쓴다.
  4. 커밋 파일 규칙: 비밀값을 적지 않는다. 환경마다 다를 수 있는 사실은 조건(셸·OS·도구 버전 등)과 함께 쓴다.
  5. 제외: 기능별 결정, 검증 레시피 행, 임시 경로(scratchpad 등), 파일별 수치(예: 미러 hunk 수), 조건 없이 어디서나 성립하는 셸 지식. 셸·OS·도구에 따라 달라지는 사실은 제외하지 않고 4에 따라 조건과 함께 쓴다.
  6. 파일이 없으면 상단에 비밀값 금지 경고를 두고 만든다.
- `## Hard Rules` 1의 쓰기 대상에 `_sdd/env.md`를 추가한다.
- `## Input Sources` 4에 digest `환경 함정`을 추가한다(합집합 개수는 그대로 6종).
- `## 반환`에 "`_sdd/env.md`에 승격한 항목(없으면 없음)" 1줄을 추가한다.
- `SKILL.md` `단계와 진입` 표의 spec-sync 행 산출물에 `_sdd/env.md` 승격을 추가한다(규칙은 재서술하지 않는다).
- `SKILL.md` `인계 파일`의 **digest 초기화** 문장에서, 계획 단계 경로("계획 단계를 거치면 …" 문장)에도 `_sdd/env.md` 환경 함정을 입력으로 넣는다. 승격한 사실이 기본 진입 경로(요청 → feature-draft)의 다음 실행에도 닿게 하기 위해서다. draft 진입 문장은 바꾸지 않는다. 양 runtime 같은 문구.
- 양 runtime 동일: `references/`는 claude↔codex 동일본으로 둔다. `SKILL.md`는 `## Runtime: worker dispatch` 절 하나만 다르다(hunk 1).

**Acceptance Criteria**:
- [ ] AC1 (1등급): claude `spec-sync.md`의 네 위치에 반영되었다. 아래 네 명령이 각각 `1`, `≥1`, `≥1`, `≥1`을 출력한다(현재 0·0·0·0).
  - `/usr/bin/grep -c '^1\. .*_sdd/env.md' .claude/skills/sdd-orchestrator/references/workers/spec-sync.md`
  - `/usr/bin/sed -n '/^### Step 5/,/^### Step 6/p' .claude/skills/sdd-orchestrator/references/workers/spec-sync.md | /usr/bin/grep -c '_sdd/env.md'`
  - `/usr/bin/sed -n '/^## Input Sources$/,/^## /p' .claude/skills/sdd-orchestrator/references/workers/spec-sync.md | /usr/bin/grep -c '환경 함정'`
  - `/usr/bin/sed -n '/^## 반환$/,$p' .claude/skills/sdd-orchestrator/references/workers/spec-sync.md | /usr/bin/grep -c 'env.md'`
- [ ] AC2 (2등급): reviewer가 Step 5 승격 항목을 읽고 Contracts의 여섯 요소가 모두 있는지 판정한다. 각 요소의 `file:line`을 인용한다. 같은 기준이 Hard Rules·Input Sources·반환·SKILL에 재서술되어 있으면 NOT MET이다.
- [ ] AC3 (1등급): `/usr/bin/diff -r .claude/skills/sdd-orchestrator/references plugins/sdd-skills-codex/skills/sdd-orchestrator/references`가 아무것도 출력하지 않고 exit 0이다.
- [ ] AC4 (1등급): `/usr/bin/grep -c '^| spec-sync |.*_sdd/env.md' .claude/skills/sdd-orchestrator/SKILL.md plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md`가 두 파일 모두 `1`이다(현재 0). `/usr/bin/diff .claude/skills/sdd-orchestrator/SKILL.md plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md | /usr/bin/grep -c '^[0-9]'`가 `1`이다.
- [ ] AC5 (1등급): `/usr/bin/grep -c '^- \*\*digest 초기화\*\*: 계획 단계를 거치면[^.]*_sdd/env' .claude/skills/sdd-orchestrator/SKILL.md plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md`가 두 파일 모두 `1`이다(현재 0). `[^.]*`는 env.md가 계획 단계 문장 안에 있어야 맞게 한다. `.*`로 쓰면 뒤의 draft 진입 문장에 걸려 지금도 `1`이 나온다.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/references/workers/spec-sync.md` -- 승격 규칙(Step 5)과 쓰기 대상·입력·반환 갱신
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/workers/spec-sync.md` -- codex 동일본 미러
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- `단계와 진입` 표 spec-sync 산출물, `인계 파일` digest 초기화 문장
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- codex 미러(Runtime 절 밖이라 동일 문구)

### Task 2: digest에서 일회성 입력을 막고 닫힌 fix 전용 check 행을 지운다
digest는 모든 worker가 읽는 "현재 유효한 방법과 이유"이므로, 한 worker에게만 해당하는 입력과 이미 닫힌 fix의 check는 넣거나 남기지 않는다.

**Contracts**:
- `SKILL.md` `## 인계 파일` 절의 **digest.md** 항목에 반영한다(새 bullet로 같은 규칙을 재서술하지 않는다).
  - 기존 "넣지 않는 것" 목록에 일회성 입력(fix할 findings·task 한정 지시)을 추가한다. 이들은 `Worker dispatch` 입력으로만 넘긴다.
  - 검증 레시피에서 finding 하나만 검증하는 fix 전용 check 행은, 그 fix가 닫히면 지운다. 닫힘 = 메인 루프가 fix worker의 표적 재실행 통과를 state에 반영한 시점이다. 증거는 state가 가진다.
- 양 runtime 동일 문구(Runtime 절 밖).

**Acceptance Criteria**:
- [ ] AC1 (1등급): 아래 명령이 `findings`·`task 한정`·`fix 전용` 각각 `≥1`을 출력한다(현재 0·0·0). 대상은 claude·codex `SKILL.md` 각각이다.
  - `for t in 'findings' 'task 한정' 'fix 전용'; do /usr/bin/sed -n '/^## 인계 파일$/,/^## /p' <SKILL.md> | /usr/bin/grep -c "$t"; done` (bash로 실행)
- [ ] AC2 (2등급): reviewer가 `인계 파일` 절의 digest.md 항목을 읽고 판정한다. (a) findings·task 한정 지시를 dispatch 입력으로만 넘기고 digest에 넣지 않는다고 적었다. (b) fix 전용 check 행을 지우는 시점이 "fix worker의 표적 재실행 통과를 state에 반영할 때"로 적혔다. (c) 기존 digest.md 항목 안에 통합되었다. 세 가지 모두 `file:line`으로 인용되면 MET이다.
- [ ] AC3 (1등급): `/usr/bin/diff .claude/skills/sdd-orchestrator/SKILL.md plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md | /usr/bin/grep -c '^[0-9]'`가 `1`이다.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- `인계 파일` digest.md 규칙
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- codex 미러

### Task 3: `_sdd/env.md`에 사용자 승인 환경 사실 7개를 시드한다
승인 내용은 그대로 두고 표현만 env.md 문체(한국어 bullet)에 맞춘다. 명령·필요 도구(4·7)는 기존 `Setup Commands`·`Runtime` 절에, 나머지 함정(1·2·3·5·6)은 새 절 하나에 둔다. 기존 줄은 지우지 않는다.

**Contracts**: 승인 7개(입력 원문 기준)
1. git 제외 pathspec은 `':(exclude)_…'`로 쓴다. `':!_…'`는 "Unimplemented pathspec magic" 오류다(이 저장소는 `_sdd/`·`_COMMENTS.md`처럼 `_`로 시작하는 경로가 많다).
2. 이 저장소 하네스를 `claude -p --plugin-dir`로 시험할 때 marketplace 루트를 그대로 주면 설치된 `sdd-skills`를 덮어쓰지 못한다. plugin.json + skills symlink 래퍼가 필요하다(`_sdd/goal/2026-10-04_orchestrator_harness_redesign/bench/mkplug.sh`, git 추적 파일).
3. claude↔codex 미러 비교는 `/usr/bin/diff`의 hunk 수로 판정한다.
4. 플러그인 manifest 검증: `claude plugin validate .`
5. census·0건 판정은 `/usr/bin/grep`으로 한다. 조건: Claude Code 셸에서는 `grep`·`diff`가 래퍼 함수일 수 있다(ugrep은 재귀 검색에서 gitignore 파일을 건너뛴다).
6. 조건: macOS 기본 도구. `/bin/bash`는 3.2, BSD grep의 `--exclude-dir`는 경로 앞에 둔다, BSD awk는 한글 heading 매칭이 깨진다, 한국어 locale에서 `sort | uniq`가 다른 줄을 묶는다.
7. 조건: `tools/tests`는 pytest가 필요하다(기본 python3 3.14에는 없다).

**Acceptance Criteria**:
- [ ] AC1 (1등급): 아래 bash 명령이 아무것도 출력하지 않는다(현재 15줄 MISSING).
  - `/bin/bash -c 'for p in ":(exclude)" "Unimplemented pathspec magic" "--plugin-dir" "mkplug.sh" "/usr/bin/diff" "hunk" "claude plugin validate ." "/usr/bin/grep" "ugrep" "3.2" "--exclude-dir" "awk" "uniq" "pytest" "tools/tests"; do /usr/bin/grep -qF -- "$p" _sdd/env.md || echo "MISSING: $p"; done'`
- [ ] AC2 (1등급): `git diff --numstat -- _sdd/env.md | cut -f2`가 `0`이다(기존 줄 삭제 없음). `/usr/bin/grep -nE 'scratchpad|/private/tmp|====' _sdd/env.md`가 아무것도 출력하지 않는다(exit 1). `git diff --check -- _sdd/env.md`가 아무것도 출력하지 않는다.
- [ ] AC3 (2등급): reviewer가 env.md diff를 Contracts 7개와 대조해 판정한다. (a) 7개 각각의 의미가 더해지거나 빠지지 않았다. (b) 5·6·7이 조건과 함께 적혔다. (c) 비밀값이 없다. (d) 기존 절 구조가 유지되었다. 항목별로 diff 줄을 인용하면 MET이다.

**Target Files**:
- [M] `_sdd/env.md` -- 승인 7개 시드

# Open Questions
- 승격 주체를 spec-sync worker로 정했다. 종점이 spec-sync 전이면 그 실행에서는 승격하지 않는다. 같은 slug로 재개해 spec-sync를 실행할 때 승격한다. 사용자 확인 불필요.
- 이 실행의 spec-sync worker도 Task 1의 새 계약을 읽고 digest `환경 함정`을 승격하려 한다. 승인 7개 밖 내용(예: 해결 명령, zsh `====` 함정)이 올라가면 "내용 고정" 승인을 넘는다. 결정: 메인 루프가 이번 spec-sync dispatch 입력에 "env.md 승격은 Task 3 시드(승인 7개)로 끝났다. 추가 승격 없음"을 일회성 입력으로 넣는다. 사용자 확인 불필요.
- "fix가 닫힘"을 fix worker의 표적 재실행 통과를 state에 반영한 시점으로 정했다. gate 2의 correctness worker는 AC 행으로 다시 검증하므로 finding 전용 행이 없어도 된다. 사용자 확인 불필요.
