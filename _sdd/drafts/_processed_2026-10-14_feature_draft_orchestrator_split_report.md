# Feature Draft: sdd-orchestrator "분할 필요" 처리 규칙과 마감 보고의 남은 분할 feature 목록

> 규모 판정: 적격 — 변경 요소 3개(실행 흐름 규칙 1문장, 마감 보고 항목 2문장, Codex 미러 동기화)가 task 1개에 1:1로 대응하고 눈검산이 닫힌다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
sdd-orchestrator 메인 루프는 feature-draft worker의 규모 판정 "분할 필요"를 처리하는 규칙이 없다. 분할 규칙은 worker 계약(`references/workers/feature-draft.md`)에만 있고 메인 루프는 그 계약을 읽지 않으므로, 첫 feature가 끝나면 체인이 닫히고 남은 분할 feature가 마감 보고에 나오지 않는다. SKILL.md(Claude + Codex 미러)에 옵션 A(보고하고 멈춤)를 2~3문장으로 넣는다.

- 새 약속 1: 규모 판정이 "분할 필요"면 메인 루프는 draft Part 2(첫 feature)만 정한 종점까지 진행하고 멈춘다. 남은 분할 feature를 자동으로 이어가지 않는다.
- 새 약속 2: 마감 보고는 남은 분할 feature 목록(draft Part 1 마커 내부의 분할 feature 목록에서 첫 feature를 뺀 나머지)을 포함하고, 남은 feature가 있으면 "남은 feature를 무인으로 이어 구현하려면 `sdd-autopilot`을 쓴다" 안내 1줄을 붙인다.

## Scope
- **In**: `.claude/skills/sdd-orchestrator/SKILL.md`와 `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md`의 `실행 흐름` 3단계 feature-draft 행과 `마감` 2항 문장 추가.
- **Out**: 옵션 B(다음 feature 자동 연속). 새 파일·새 절·새 state 필드. worker 계약(`references/workers/feature-draft.md`)·`handoff-templates.md`·`worker-boundary.md` 변경. `_processed_` rename 규칙(이미 "남은 분할 feature가 없으면"을 조건으로 가짐) 변경.
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: sdd-orchestrator SKILL.md에 "분할 필요" 처리 규칙과 마감 보고 항목을 추가한다 (Claude + Codex 미러)
메인 루프가 읽는 유일한 문서(SKILL.md)에 옵션 A를 넣는다. 두 파일은 `## Runtime: worker dispatch` 절 앞까지 동일하므로 같은 문장을 같은 위치에 넣는다(단순 파일 복사 금지 — Runtime 절이 다르다).

**Contracts**: 아래 문장을 그대로 넣는다(두 파일 동일).
- `## 실행 흐름` 3단계의 `feature-draft·plan-review: 계획 게이트(`품질 게이트`)를 실행한다.` 행 끝에 추가: `feature-draft worker의 규모 판정이 "분할 필요"면 draft Part 2(첫 feature)만 정한 종점까지 진행하고 멈춘다. 남은 분할 feature는 자동으로 이어가지 않는다.`
- `## 마감` 2항의 보고 목록 `state 경로` 뒤에 추가: `, 남은 분할 feature 목록(규모 판정이 "분할 필요"일 때 — draft Part 1 마커 내부의 분할 feature 목록에서 첫 feature를 뺀 나머지).` 이어서 문장 추가: `남은 분할 feature가 있으면 "남은 feature를 무인으로 이어 구현하려면 `sdd-autopilot`을 쓴다" 안내 1줄을 붙인다.`

**Acceptance Criteria**:
- [ ] AC1 (1등급): 두 파일의 `## 실행 흐름` 절에 "분할 필요" 규칙이 1회 있다. 명령: `for f in .claude/skills/sdd-orchestrator/SKILL.md plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md; do /usr/bin/sed -n '/^## 실행 흐름$/,/^## /p' "$f" | /usr/bin/grep -c "분할 필요"; done` → `1` 두 줄.
- [ ] AC2 (1등급): 두 파일의 `## 마감` 절에 남은 분할 feature 목록과 `sdd-autopilot` 안내가 있다. 명령(파일마다 grep 2개): `for f in .claude/skills/sdd-orchestrator/SKILL.md plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md; do /usr/bin/sed -n '/^## 마감$/,/^## /p' "$f" | /usr/bin/grep -c "남은 분할 feature 목록"; /usr/bin/sed -n '/^## 마감$/,/^## /p' "$f" | /usr/bin/grep -c "sdd-autopilot"; done` → 네 줄 모두 `1` 이상.
- [ ] AC3 (1등급): Claude판과 Codex 미러가 Runtime 절 앞까지 동일하다. 명령: `/usr/bin/diff <(/usr/bin/sed -n '1,/^## Runtime/p' .claude/skills/sdd-orchestrator/SKILL.md) <(/usr/bin/sed -n '1,/^## Runtime/p' plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md); echo $?` → 출력 없음, `0`.
- [ ] AC4 (1등급): 변경이 두 파일에만 있고 새 절(`## `)·새 파일이 없다. 시작 시 dirty 파일(`_COMMENTS.md`, `_sdd/work_log/*`)은 이번 작업과 무관하므로 제외한다. 명령: `git diff --name-only -- ':(exclude)_COMMENTS.md' ':(exclude)_sdd/work_log'` → 위 두 경로만; `git diff -- .claude plugins | /usr/bin/grep -c '^+## '` → `0`; `git status --porcelain -- .claude plugins | /usr/bin/grep -c '^??'` → `0`.
- [ ] AC5 (1등급): `git diff --check` → 출력 없음, exit 0.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- `실행 흐름` 3단계 행과 `마감` 2항에 문장 추가
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- 같은 문장을 같은 위치에 추가 (Codex 미러)

# Open Questions
- 마감 보고의 남은 분할 feature 목록은 종점이 spec-sync가 아니어도(예: 호출 이름 `feature-draft`로 계획 게이트에서 멈춤) 적용한다 — `마감` 절은 모든 종점에 공통이므로 별도 조건을 두지 않았다. 사용자 확인 불필요.
- 남은 feature 목록의 출처는 draft Part 1 마커 내부로 고정했다(메인 루프가 읽어도 되는 문서이고, worker 반환보다 재개 때도 남아 있음). 사용자 확인 불필요.
