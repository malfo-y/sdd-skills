# Feature Draft: 예전 단계 스킬 이름 5개의 호환 별칭 스킬

> 규모 판정: 적격 — 변경 요소 6종(호출 이름 표·description·별칭 10파일·marketplace 등록·README·검증)이 task 4개에 1:1로 배정되고 전부 문서 편집이다. 별칭 파일이 5이름 × 2 runtime으로 흩어지는 census형 신호가 있어 read-only 검증 task를 마지막에 둔다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

`sdd-orchestrator`로 통합하며 삭제한 예전 단계 스킬 이름 5개(`feature-draft`·`plan-review`·`implementation`·`implementation-review`·`spec-sync`)를 호환 별칭 스킬로 되살린다. 별칭은 Claude(`.claude/skills/<이름>/`)·Codex(`plugins/sdd-skills-codex/skills/<이름>/`) 양 runtime에 두고, 본문은 다른 스킬을 호출하지 않고 형제 경로 `../sdd-orchestrator/SKILL.md`를 읽어 "호출 이름 = <이름>"으로 따르는 얇은 지시 + "이 이름은 sdd-orchestrator 별칭" 안내 한 줄이다. 단계 규칙은 `sdd-orchestrator` `단계와 진입`의 **호출 이름 표** 한 곳에만 둔다. 기존 결정 "구 단계 스킬 삭제(별칭 스킬 없음, 구 이름 요청은 description 트리거가 받는다)"를 "삭제하되 호환 별칭 유지"로 대체한다.

새 contract/invariant:
- `sdd-orchestrator` `단계와 진입`의 호출 이름 표가 예전 스킬 동작 재현의 단일 소스다. 호출 이름이 주어지면(별칭 스킬 경유 또는 사용자가 이름을 지정) 표의 행이 시작 단계·종점·게이트·fix 범위를 정하고, `sdd-orchestrator`의 진입 규칙·실행 흐름·품질 게이트보다 우선한다. 범위: `feature-draft`=draft 작성 + 계획 게이트까지(spec-sync 없음) / `plan-review`=계획 리뷰만, fix 없음(draft 없으면 최신 draft) / `implementation`=draft가 있으면 plan-review 완료로 보고 구현 + 구현 게이트까지, 요청만 있으면 feature-draft worker가 draft만 쓰고(계획 게이트 없음) 구현 + 구현 게이트까지(spec-sync 없음) / `implementation-review`=구현 리뷰만, fix 없음(draft 없으면 worker 계약의 기준 문서 적응, base는 git 기록) / `spec-sync`=spec-sync만(draft 없으면 최신 draft, state 없으면 코드 증거).
- 별칭 스킬 본문에는 단계 로직이 없다(worker·게이트 어휘 0). Claude·Codex 별칭 본문은 runtime 절 없이 동일본이다. 별칭의 frontmatter description은 하이픈 이름과 별칭 관계만 트리거로 가지며, 자연어 트리거("기능 초안"·"계획 리뷰" 등)는 `sdd-orchestrator` description이 계속 소유한다.
- 등록: Claude는 `.claude-plugin/marketplace.json` `skills` 배열에 경로 5개 추가. Codex는 `plugins/sdd-skills-codex/.codex-plugin/plugin.json`의 `"skills": "./skills/"` 디렉터리 자동 발견이라 등록 변경 없음(번들 설치 스크립트 `_discover_skills`도 디렉터리 열거). `tools/uninstall-codex-skill-bundle.py` `LEGACY_SKILL_NAMES`는 번들 스킬 전체 이름 목록이라 별칭 5개가 들어 있는 현행 그대로 맞다(변경 없음).

spec 반영 대상(spec-sync 단계 소유, 이 draft의 Target Files 아님): `_sdd/spec/main.md` §2 "SDD 체인…의 기본이자 유일한 실행 경로" bullet의 문장 "구 단계 스킬 이름의 요청(…)은 `sdd-orchestrator` description의 트리거가 받는다(별칭 스킬 없음)" → 호환 별칭 5개 + 호출 이름 표 우선 규칙으로 갱신; `_sdd/spec/components.md` `Claude skill/agent split` 행의 "구 직접 실행 단계 스킬(…)은 삭제됐고" → "삭제하되 호환 별칭 유지(본문은 `../sdd-orchestrator/SKILL.md` 참조, 로직 없음)"; `_sdd/spec/decision_log.md`·`_sdd/spec/logs/changelog.md` 신규 entry; `_sdd/spec/usage-guide.md` Scenario 2 명령 예시에 별칭 호출 1줄(선택).

## Scope
- **In**: `sdd-orchestrator/SKILL.md` 양 runtime의 `단계와 진입` 호출 이름 표·우선 규칙과 frontmatter description(하이픈 이름 5개), 별칭 SKILL.md 10파일 생성, `.claude-plugin/marketplace.json` skills 5항목, `README.md`(스킬 수 표·Quick Start 문장·Skills 절 별칭 표).
- **Out**: `_sdd/spec/`(spec-sync 소유), `sdd-orchestrator/references/`(무변경 — 미러 동일본 유지), AGENTS.md와 하네스 템플릿 4미러의 "plan-review·implementation-review는 게이트로 수행하므로 별도로 호출하지 않는다" 문장(체인 안 지침이라 별칭과 충돌하지 않음, 현행 유지), `tools/` 설치·제거 스크립트, `docs/`·`docs/en/`, plugin version bump(marketplace 1.0.0 / codex 1.0.1 유지), `_sdd/goal/2026-10-04_*`·`docs/reviews/` 이력 문서, 실제 `/plan-review`·`/spec-sync` 호출 확인(마감 뒤 사용자와 메인이 수행).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: sdd-orchestrator `단계와 진입`에 호출 이름 표 추가 + description에 하이픈 이름 5개 (Claude + Codex 미러)
별칭이 참조할 단일 소스를 만든다. 두 미러의 차이는 `## Runtime: worker dispatch` 절뿐이므로 같은 편집을 두 파일에 적용한다.

**Contracts**:
- `## 단계와 진입` 절 안, 기존 "진입 규칙:" 목록 **뒤**에 소절 `### 호출 이름`을 둔다. 첫 문단: "예전 단계 스킬 이름으로 호출되면(별칭 스킬 경유 또는 사용자가 호출 이름을 지정) 아래 표의 행이 시작 단계·종점·게이트·fix 범위를 정하고, 이 스킬의 진입 규칙·실행 흐름·품질 게이트보다 우선한다. 표의 범위 밖 단계는 실행하지 않는다." 이어서 표 `| 호출 이름 | 시작 | 범위·종점 |` 5행(호출 이름 칸은 기존 단계 표처럼 백틱 없이 적는다):
  - `feature-draft` | feature-draft worker | 계획 게이트(gate 1 + fix 1, 조건부 gate 2)까지 실행하고 멈춘다. spec-sync 없음.
  - `plan-review` | plan-review worker. draft 경로가 없으면 최신 draft(`_sdd/drafts/`에서 `_processed_` 접두가 없는 `*_feature_draft_*` 중 가장 최근 파일) | 계획 리뷰만. findings를 보고하고 fix 없음.
  - `implementation` | draft 경로가 있으면 plan-review 완료로 보고 implementation부터. 요청만 있으면 feature-draft worker로 draft만 쓰고(계획 게이트 없음) implementation | 구현 게이트(리뷰 worker 3개 + fix 1, 조건부 gate 2)까지 실행하고 멈춘다. spec-sync 없음. task worker 입력은 항상 draft 경로 + task ID다.
  - `implementation-review` | 리뷰 worker 3개. draft 경로가 없으면 worker 계약의 기준 문서 적응(spec·코드 변경)으로 판정하고 base는 git 기록으로 식별한다 | 구현 리뷰만. findings를 보고하고 fix 없음.
  - `spec-sync` | spec-sync worker. draft 경로가 없으면 최신 draft, state가 없으면 코드 증거 | spec-sync만.
- 표 밖의 기존 진입 규칙·게이트·마감 규칙은 바꾸지 않는다. `## 실행 흐름`·`## 품질 게이트`·`인계 파일`에 별칭 관련 문장을 추가하지 않는다 — 호출 이름이 그 절들보다 우선한다는 것은 위 첫 문단 한 곳이 말한다.
- frontmatter description: `Triggered by "sdd-orchestrator",` 바로 뒤에 `"feature-draft", "plan-review", "implementation", "implementation-review", "spec-sync",`를 끼워 넣는다. 그 밖의 description 문면은 불변.

**Acceptance Criteria**:
- [ ] AC1 (1등급): 두 파일 각각 `/usr/bin/sed -n '/^## 단계와 진입$/,/^## Worker dispatch$/p' <f> | /usr/bin/grep -c '^| \(feature-draft\|plan-review\|implementation\|implementation-review\|spec-sync\) |'` → `10`(기존 단계 표 5 + 호출 이름 표 5), `/usr/bin/grep -c '^### 호출 이름$' <f>` → `1`.
- [ ] AC2 (1등급): 두 파일 각각 `/usr/bin/grep -c '^description:.*"sdd-orchestrator", "feature-draft", "plan-review", "implementation", "implementation-review", "spec-sync",' <f>` → `1`.
- [ ] AC3 (1등급): 미러 불변 — `/usr/bin/diff .claude/skills/sdd-orchestrator/SKILL.md plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md | /usr/bin/grep -c '^[0-9]'` → `1`(Runtime 절 hunk 하나뿐).
- [ ] AC4 (2등급): reviewer가 `### 호출 이름` 표 5행을 인용해 Contracts의 범위 문구(종점·fix 유무·draft/state 부재 fallback·implementation의 "요청만 있으면 계획 게이트 없음")가 행마다 빠짐없이 있고, 표 앞 첫 문단에 우선 규칙 문구 "아래 표의 행이 시작 단계·종점·게이트·fix 범위를 정하고, 이 스킬의 진입 규칙·실행 흐름·품질 게이트보다 우선한다"가 그대로 있음을 확인한다.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- `### 호출 이름` 소절·표, description 하이픈 이름 5개
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- 같은 편집(Runtime 절만 다른 미러 유지)

### Task 2: 별칭 스킬 10파일 생성 (5이름 × Claude·Codex, 동일본)
예전 이름으로 호출해도 "스킬 없음" 없이 sdd-orchestrator의 해당 범위가 실행되게 한다. 스킬 안 스킬 호출은 runtime마다 동작이 달라 형제 경로 읽기(pr-review가 양 runtime에서 쓰는 `../sdd-orchestrator/...`)를 쓴다.

**Contracts**:
- 파일 본문은 아래 템플릿에서 `<이름>` 슬롯만 치환한 것이다. 10파일 모두 이 템플릿이고 Claude·Codex 짝은 바이트 동일이다.

```markdown
---
name: <이름>
description: "sdd-orchestrator의 호환 별칭. 예전 단계 스킬 이름 \"<이름>\"으로 부를 때 사용한다 — sdd-orchestrator를 호출 이름 <이름> 범위로 실행한다."
---

# <이름> (sdd-orchestrator 별칭)

이 이름은 `sdd-orchestrator`의 호환 별칭이다. 단계 규칙과 범위는 `sdd-orchestrator`가 단일 소스이고 이 파일에는 없다.

1. 사용자에게 한 줄 알린다: "`<이름>`은 `sdd-orchestrator`의 별칭이다 — 호출 이름 `<이름>` 범위로 실행한다."
2. 이 스킬 디렉터리의 형제 경로 `../sdd-orchestrator/SKILL.md`를 읽고, 호출 이름 = `<이름>`으로 그 스킬의 `단계와 진입` 호출 이름 표 행을 그대로 따른다. 그 스킬이 말하는 "이 스킬 디렉터리"(base directory)는 `../sdd-orchestrator/`다. 사용자의 요청·인자(draft 경로, `--model` 등)는 그대로 넘긴다. 다른 스킬을 호출하지 않는다.
```

- description은 하이픈 이름과 별칭 관계만 담는다. 자연어 트리거·범위 설명은 넣지 않는다(트리거 소유는 `sdd-orchestrator` description).
- 본문에 `worker`·`게이트`·`gate` 어휘와 단계 범위 서술을 두지 않는다(로직 복제 금지의 검사 가능 형태).

**Acceptance Criteria**:
- [ ] AC1 (1등급): `for s in feature-draft plan-review implementation implementation-review spec-sync; do /usr/bin/diff -q .claude/skills/$s/SKILL.md plugins/sdd-skills-codex/skills/$s/SKILL.md || exit 1; done` → 무출력, exit 0(존재 + 동일본).
- [ ] AC2 (1등급): 각 Claude 별칭 파일에서 `/usr/bin/grep -c "^name: $s$"` → `1`, `/usr/bin/grep -c '\.\./sdd-orchestrator/SKILL\.md'` → `1`, `/usr/bin/grep -c '별칭'` ≥ `3`(description·제목·안내 문장), `/usr/bin/grep -c -i 'worker\|게이트\|gate'` → `0`.
- [ ] AC3 (1등급): 새 파일 위생 — 각 파일 `/usr/bin/grep -c '[[:space:]]$' <f>` → `0`(`git diff --check`는 untracked를 검사하지 않음).
- [ ] AC4 (2등급): reviewer가 한 파일(예: `plan-review`)을 이 task Contracts의 템플릿과 줄 단위로 대조해 슬롯 치환 외 추가·삭제 줄이 0임을 인용 확인한다.

**Target Files**:
- [C] `.claude/skills/feature-draft/SKILL.md` -- Claude Code는 스킬을 디렉터리 단위(`<이름>/SKILL.md`)로 발견하므로 기존 파일 수정으로는 새 호출 이름을 만들 수 없다
- [C] `.claude/skills/plan-review/SKILL.md` -- 상동
- [C] `.claude/skills/implementation/SKILL.md` -- 상동
- [C] `.claude/skills/implementation-review/SKILL.md` -- 상동
- [C] `.claude/skills/spec-sync/SKILL.md` -- 상동
- [C] `plugins/sdd-skills-codex/skills/feature-draft/SKILL.md` -- Codex 번들은 `.claude/skills/` 밖이라 동일본 배포 필요(plugin.json `skills: ./skills/` 자동 발견)
- [C] `plugins/sdd-skills-codex/skills/plan-review/SKILL.md` -- 상동
- [C] `plugins/sdd-skills-codex/skills/implementation/SKILL.md` -- 상동
- [C] `plugins/sdd-skills-codex/skills/implementation-review/SKILL.md` -- 상동
- [C] `plugins/sdd-skills-codex/skills/spec-sync/SKILL.md` -- 상동

### Task 3: Claude marketplace 등록 + README 별칭 표
Claude Code는 `marketplace.json` `skills` 배열에 명시된 경로만 설치하므로 별칭 5경로를 등록하고, 사용자 문서에 별칭을 알린다. Codex는 디렉터리 자동 발견이라 등록 변경이 없다(Part 1).

**Contracts**:
- `.claude-plugin/marketplace.json` `skills` 배열 끝(`./.claude/skills/second-opinion` 뒤)에 `./.claude/skills/feature-draft`, `./.claude/skills/plan-review`, `./.claude/skills/implementation`, `./.claude/skills/implementation-review`, `./.claude/skills/spec-sync` 5항목을 추가한다. 다른 필드·version 불변.
- `README.md`:
  - 런타임 표 `스킬 수` 칸: Claude `16` → `16 + 호환 별칭 5`, Codex `14` → `14 + 호환 별칭 5`.
  - Quick Start 문단의 문장 "plan-review와 implementation-review 단계는 오케스트레이터가 품질 게이트로 실행하므로 별도로 호출할 필요가 없다." → "plan-review와 implementation-review 단계는 체인 안에서 오케스트레이터가 품질 게이트로 실행한다. 예전 단계 스킬 이름 5개는 호환 별칭으로 남아 있다([Skills](#skills) 절 표)."
  - `## Skills` 절의 목적별 표 아래, "Claude Code에는 `git`과 …" 문단 **앞**에 소제목 없이 문단 1개 + 표를 둔다. 문단: "예전 단계 스킬 이름 5개는 `sdd-orchestrator`의 호환 별칭이다. 별칭은 로직 없이 `sdd-orchestrator`를 그 호출 이름 범위로 실행하며, 범위의 단일 소스는 `sdd-orchestrator` SKILL.md `단계와 진입`의 호출 이름 표다." 표 `| 별칭 | Claude Code | Codex | 실행 범위 |` 5행 — Claude 칸 `/sdd-skills:<이름>`, Codex 칸 `$<이름>`, 실행 범위 칸은 호출 이름 표의 범위를 한 구절로(예: `feature-draft` → "draft 작성 + 계획 게이트까지", `plan-review` → "계획 리뷰만(fix 없음)", `implementation` → "구현 + 구현 게이트까지", `implementation-review` → "구현 리뷰만(fix 없음)", `spec-sync` → "spec-sync만").

**Acceptance Criteria**:
- [ ] AC1 (1등급): `/usr/bin/grep -c '"./.claude/skills/\(feature-draft\|plan-review\|implementation\|implementation-review\|spec-sync\)"' .claude-plugin/marketplace.json` → `5`; `claude plugin validate .` → `Validation passed`.
- [ ] AC2 (1등급): `/usr/bin/grep -c '별도로 호출할 필요가 없다' README.md` → `0`; `/usr/bin/grep -c '^| `\(feature-draft\|plan-review\|implementation\|implementation-review\|spec-sync\)` | `/sdd-skills:[a-z-]*` | `\$[a-z-]*` |' README.md` → `5`; `/usr/bin/grep -c '호환 별칭 5' README.md` → `2`.
- [ ] AC3 (1등급): `git diff --check` → 무출력, exit 0.

**Target Files**:
- [M] `.claude-plugin/marketplace.json` -- skills 배열 5경로
- [M] `README.md` -- 스킬 수 표, Quick Start 문장, Skills 절 별칭 표

### Task 4: 별칭 파일 전수 census (read-only)
5이름 × 2 runtime으로 흩어진 별칭 파일이 빠짐없이, 그리고 그것만 생겼는지 센다. Task 1~3의 AC는 재실행하지 않는다(구현 게이트가 digest 레시피로 fresh 실행). 앞 task가 모두 닫힌 뒤 실행한다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): 전수 존재 — `for s in feature-draft plan-review implementation implementation-review spec-sync; do for r in .claude/skills plugins/sdd-skills-codex/skills; do test -f "$r/$s/SKILL.md" || { echo "missing $r/$s"; exit 1; }; done; done; echo ok` (bash) → `ok`, exit 0.
- [ ] AC2 (1등급): 추가 파일 0 — `git status --porcelain -uall | /usr/bin/grep -c '^?? .*skills/\(feature-draft\|plan-review\|implementation\|implementation-review\|spec-sync\)/'` → `10`(`-uall`로 디렉터리가 아닌 파일 단위로 센다; 10을 넘으면 별칭 디렉터리에 의도치 않은 파일이 있다).

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- README 스킬 수 표기를 "16 + 호환 별칭 5"/"14 + 호환 별칭 5"로 정했다(별칭을 공통 스킬 14개에 섞지 않음). 사용자 확인 필요 없음.
- 별칭 description은 하이픈 이름만 트리거로 둔다 — 자연어 요청은 계속 `sdd-orchestrator`가 받아 두 스킬이 같은 요청을 다투지 않게 한다. 사용자 확인 필요 없음.
- AGENTS.md·하네스 템플릿 4미러(`spec-create`·`spec-upgrade` `references/agents-harness-template.md`)의 "plan-review·implementation-review 단계는 … 별도로 호출하지 않는다"는 체인 안 지침이라 그대로 둔다(별칭은 호환 진입점). 사용자 확인 필요 없음.
- `tools/uninstall-codex-skill-bundle.py` `LEGACY_SKILL_NAMES`에 예전 이름 5개가 이미 있다 — 목록이 번들 스킬 전체 이름이라 별칭도 같은 취급이 맞아 변경하지 않는다. `tools/tests/test_uninstall_codex_skill_bundle.py`의 `spec-sync` fixture도 그대로 유효하다. 사용자 확인 필요 없음.
- 지난 goal(`_sdd/goal/2026-10-04_*`)의 "구 스킬 디렉터리 부재·marketplace 0건" 검사는 이력 문서에만 있고 활성 hook·tools·spec 검사에는 없다(`.claude/hooks/*`·`.codex/hooks.json`·`tools/*.py` 실측). 충돌 없음.
