# Feature Draft: env.md 단계별 worker 기본 모델

> 규모 판정: 적격 — 변경 요소 5개(Worker dispatch 옵션 규칙, Claude·Codex Runtime 절, env.md 절, README)가 task 2개에 겹침 없이 대응해 눈검산된다. rename/census형 sweep 아님(spec 문장은 spec-sync 단계 소유).

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
`sdd-orchestrator` worker 모델을 호출 때만 지정하던 방식에서, 저장소 `_sdd/env.md`에 runtime별 단계 기본값을 두고 호출 지정이 없는 단계에 그 값을 쓰는 방식으로 바꾼다. 사용자 요청으로 decision_log `2026-10-05 - sdd-orchestrator worker 단계별 모델 선택 (v4.35.0)`의 기각 2건(단계별 기본값 고정, repo 설정 파일)을 뒤집는다. 근거: 메인 루프가 시작 때 이미 `_sdd/env.md`를 읽고, 이 파일은 저장소마다 커밋되므로 별도 설정 파일이 필요 없다. 허용값은 계속 runtime 계약이 정해 저장소 allowlist가 되지 않는다.

새 contract/invariant:
- worker 옵션 값은 단계·필드(model, Codex는 effort도)별로 호출 지정(`--model`/`--effort`/자연어) > `_sdd/env.md` `## Worker Model Defaults` 절의 현재 runtime 하위 절 값 > 값 없음(필드 생략, 런타임 기본 동작) 순으로 정한다.
- `## Worker Model Defaults` 형식: `### Claude Code` 표(`단계 | model`), `### Codex` 표(`단계 | model | effort`). 행은 다섯 단계 이름이다. 빈 칸, 행·하위 절·절이 없으면 값 없음이다.
- env.md 기본값도 호출 지정과 같은 Runtime 검증(지원값·effort 조합)과 미지원·잘못된 값 정책을 거친다. 시작 때 적용한 단계별 값은 digest 결정·제약에 적어 재개 때 같은 값을 쓴다.
- env.md 밖 별도 설정 파일과 고정 allowlist는 두지 않는다.
- 이 저장소 값: Claude Code feature-draft=fable, plan-review=opus, implementation=sonnet, implementation-review=opus, spec-sync=sonnet. Codex는 비운다.

spec 반영 대상: `main.md` §2 `sdd-orchestrator` 옵션 문장("지정값은 digest에 보존하며 미지정 필드는 생략한다"), 같은 bullet의 금지 문장("고정 allowlist·단계별 기본값·repo 설정 파일·Claude effort 지원은 추가하지 않는다" → "고정 allowlist·env.md 밖 설정 파일·Claude effort 지원은 추가하지 않는다"), 결정 표 `subagent model override` 행("호출 단위 per-call option", "고정 기본값·repo allowlist 없이"), `usage-guide.md` sdd-orchestrator 옵션 설명("미지정 필드는 생략한다"), decision_log 새 entry(위 v4.35.0 entry의 기각 2건 대체), changelog.

## Scope
- **In**: 두 `sdd-orchestrator/SKILL.md`의 `Worker dispatch` worker 옵션 규칙과 `## Runtime: worker dispatch` 절, `_sdd/env.md` 새 절, `README.md`의 sdd-orchestrator 모델 지정 설명.
- **Out**: `pr-review` 모델 옵션(호출 단위 유지), 다른 스킬이 만드는 env.md 템플릿에 절 추가, 기본값을 한 번 끄는 opt-out 문법, Codex 기본값 채우기, plugin manifest 버전.
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: orchestrator가 env.md 단계 기본값을 읽어 적용하게 한다
`Worker dispatch` worker 옵션 규칙에 env.md 기본값의 위치·우선순위를 넣고, 두 Runtime 절이 그 적용값을 매핑하게 하고, 이 저장소 `_sdd/env.md`에 기본값 절을 만든다. 규칙과 첫 인스턴스(형식)를 한 task가 가져 형식 계약이 갈라지지 않게 한다.

**Contracts**:
- 우선순위(단계·필드별): 호출 지정 > `_sdd/env.md` `## Worker Model Defaults`의 현재 runtime 하위 절 값 > 값 없음(필드 생략 → 런타임 기본 동작). 기존 `범위` 규칙(각 단계 fix 재dispatch, implementation-review worker 3개)이 기본값에도 그대로 적용된다.
- env.md 형식: `## Worker Model Defaults` 아래 `### Claude Code` 표 열 `단계 | model`, `### Codex` 표 열 `단계 | model | effort`. 행은 `단계와 진입` 표의 다섯 단계 이름. 빈 칸, 행·하위 절·절이 없으면 값 없음. 절 머리에 소비 스킬과 빈 칸 의미를 1줄 적는다(우선순위 규칙은 SKILL이 단독 소유).
- 읽기·검증·기록: 시작할 때 메인 루프가 이 절을 읽고, 호출 지정과 합친 적용값을 기존 Runtime 검증(지원값·effort 조합)에 넣는다. 실패하면 기존 필드 미지원·잘못된 값 정책을 그대로 따른다(대화형: 알리고 고쳐 받기, 그 단계 dispatch 보류. 무인: 그 단계 override 생략, fallback은 digest, 발생 사실은 state·마감 보고). 적용값은 digest 결정·제약에 적는다.
- 금지 문장 교체: "미지정 모델을 임의로 고정하거나 별도 설정 파일을 만들지 않는다"를, 호출 지정과 env.md 어디에도 없는 값을 임의로 고정하지 않고 env.md 밖 설정 파일을 만들지 않는다는 뜻으로 바꾼다.
- Runtime 절: Claude는 적용된 model 값이 있는 단계만 `model`에 넣고, 없으면 생략해 세션 기본값을 따른다. Codex는 적용된 model·effort를 각각 `model`·`reasoning_effort`에 매핑한다("사용자가 지정한" 한정을 없앤다). 두 SKILL.md는 Runtime 절 외 동일하다.
- 이 저장소 값: `### Claude Code` feature-draft=fable, plan-review=opus, implementation=sonnet, implementation-review=opus, spec-sync=sonnet. `### Codex` 5행 model·effort 모두 빈 칸.

**Acceptance Criteria**:
- [ ] AC1: (1등급) 두 SKILL.md 모두 env.md 기본값 절을 참조하고 옛 금지 문장이 없다. 명령: `for f in .claude/skills/sdd-orchestrator/SKILL.md plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md; do /usr/bin/grep -c 'Worker Model Defaults' $f; /usr/bin/grep -c '미지정 모델을 임의로 고정하거나 별도 설정 파일을 만들지 않는다' $f; done` → 파일마다 `≥1`, `0` (현재 `0`, `1`).
- [ ] AC2: (2등급) `Worker dispatch`의 worker 옵션 규칙이 Contracts의 우선순위·env.md 형식·읽기·검증·기록·금지 문장 교체를 모두 서술한다. rubric: 항목마다 인용 줄이 있고 Contracts와 뜻이 같으면 MET, 하나라도 없거나 다르면 NOT MET. 증거: `/usr/bin/sed -n '/^## Worker dispatch$/,/^## 병렬 규칙$/p' .claude/skills/sdd-orchestrator/SKILL.md` 인용.
- [ ] AC3: Runtime 절이 호출 지정에 한정하지 않고 적용값을 매핑한다. (1등급) `/usr/bin/sed -n '/^## Runtime: worker dispatch$/,/^## Final Check$/p' plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md | /usr/bin/grep -c '사용자가 지정한'` → `0` (현재 `1`). (2등급) 두 Runtime 절의 model(Codex는 effort도) 넣기·생략 문장이 Contracts의 Runtime 항목과 같은 뜻인지 인용으로 판정한다.
- [ ] AC4: (1등급) env.md 절과 값. `/usr/bin/grep -c '^## Worker Model Defaults$' _sdd/env.md` → `1`. `/usr/bin/sed -n '/^### Claude Code$/,/^### /p' _sdd/env.md | /usr/bin/grep -cE '^\| *(feature-draft *\| *fable|plan-review *\| *opus|implementation *\| *sonnet|implementation-review *\| *opus|spec-sync *\| *sonnet) *\|$'` → `5`. `/usr/bin/sed -n '/^### Codex$/,/^## /p' _sdd/env.md | /usr/bin/grep -cE '^\| *(feature-draft|plan-review|implementation|implementation-review|spec-sync) *\| *\| *\|$'` → `5`.
- [ ] AC5: (1등급) 회귀. `/usr/bin/diff .claude/skills/sdd-orchestrator/SKILL.md plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md | /usr/bin/grep -c '^[0-9]'` → `1`. `/usr/bin/diff -r .claude/skills/sdd-orchestrator/references plugins/sdd-skills-codex/skills/sdd-orchestrator/references` → 무출력, exit 0. `git diff --check` → 무출력, exit 0. `claude plugin validate .` → `Validation passed`.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- `Worker dispatch` worker 옵션 규칙, Claude `## Runtime: worker dispatch` 절
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- 같은 `Worker dispatch` 변경(미러), Codex `## Runtime: worker dispatch` 절
- [M] `_sdd/env.md` -- `## Worker Model Defaults` 절 신설(이 저장소 Claude 값, Codex 빈 표)

### Task 2: README에 env.md 기본값과 우선순위를 적는다
README의 sdd-orchestrator 모델 지정 설명이 호출 지정만 다뤄서, 사용자가 env.md 기본값과 우선순위를 알 수 없다. 내용은 Task 1 Contracts를 따른다.

**Acceptance Criteria**:
- [ ] AC1: (1등급) `/usr/bin/grep -c 'Worker Model Defaults' README.md` → `≥1` (현재 `0`).
- [ ] AC2: (2등급) README sdd-orchestrator 모델 설명이 (a) 사용 저장소 `_sdd/env.md` `## Worker Model Defaults` 절의 runtime별 표(`### Claude Code`: 단계·model, `### Codex`: 단계·model·effort)로 단계 기본값을 둘 수 있다, (b) 우선순위는 호출 지정 > env.md > 런타임 기본 동작, (c) env.md 값도 같은 검증을 거친다, (d) Codex spawn 인자 표의 `생략` 행과 표 바로 뒤 문장("미지정 필드는 런타임 기본 동작을 따른다")이 호출 지정과 env.md 값이 모두 없는 경우로 읽힌다(env.md 값이 있는데 런타임 기본 동작을 따르는 것으로 읽히면 NOT MET) — 네 항목을 인용으로 판정한다. 하나라도 없거나 Task 1 Contracts와 다르면 NOT MET.
- [ ] AC3: (1등급) `git diff --check` → 무출력, exit 0.

**Target Files**:
- [M] `README.md` -- sdd-orchestrator 모델 지정 단락, Codex spawn 인자 표와 표 바로 뒤 문단("미지정 필드는 런타임 기본 동작을 따른다", 163~187행 부근)

# Open Questions
- 우선순위를 단계 단위가 아니라 단계·필드 단위로 정했다. Codex에서 호출이 effort만 주면 model은 env.md 값을 쓰고 그 조합을 검증한다. digest 우선순위를 필드에 적용한 해석이라 확인 불필요.
- 무인 실행에서 적용값이 허용값 밖이면 env.md 값으로 대체하지 않고 기존 정책대로 그 단계 override를 생략한다(digest 결정 그대로). 확인 불필요.
- 기본값을 한 번 끄고 세션 모델을 상속하는 opt-out 문법은 두지 않는다(요청 밖). 다른 값은 호출 지정으로 줄 수 있다. 확인 불필요.
