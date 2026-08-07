# Feature Draft: norms P1 spec lifecycle

> 규모 판정: 분할 필요 — 분할 계획 포함. P1 네 component는 같은 규범 감사에서 나왔지만 bootstrap disclosure와 quality interface가 독립적으로 구현·검증될 수 있다. Part 1에 두 feature를 고정하고 Part 2에는 현재 feature만 상세화한다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
P1을 두 개의 독립 feature로 순차 처리한다.

1. **spec-bootstrap-disclosure (current)** — `spec-create`와 `spec-upgrade`의 Step·Validation·Output에 길게 흩어진 hook 설치 상세를 실행 시점에 읽는 self-contained rich reference로 옮긴다. 두 skill은 각각 독립 배포될 수 있으므로 로컬 reference를 가지되 `.claude/skills/spec-create/references/hook-installation.md`를 authoring canonical로 두고 나머지 세 사본은 exact 배포 mirror로 고정한다. 본문은 trigger·upgrade 고유 책임·reference pointer만 소유하고, hook 이벤트·matcher·JSON merge·trust·검증·보고 계약은 reference가 소유한다.
2. **spec-quality-interface (planned)** — `spec-review`의 판정 기준·상태/decision 허용값을 deterministic interface로 만들고, `spec-create`·`spec-rewrite`·`spec-upgrade`의 template/reference/example 선택 기준과 load timing 및 산출물 shape를 완결한다. `spec-rewrite`·`spec-upgrade` reference의 legacy 7-section temporary-spec 설명을 현재 producer의 `Part 1: Spec Delta` + 선택적 `Propagation Surfaces` + `Part 2: Tasks` 계약으로 고친 뒤에만 해당 reference를 load하도록 한다.

판단 근거: hook 설치 상세는 하네스를 다룰 때만 필요하고 100줄 이상이므로 조건부 reference가 맞다. 반면 실행 trigger와 upgrade-only repair ownership은 소비 지점의 본문에 남긴다. quality interface는 hook 설치와 change element·검증면이 겹치지 않고, 현재 `spec-format.md`는 아직 stale하므로 별도 feature로 분리한다. cross-skill 단일 파일은 독립 배포를 깨므로 기각하고, 하나의 authoring home에서 세 배포 mirror로 전파하는 방식을 선택했다. 확신도는 높고 기존 동작을 이동·명료화할 뿐 새 동작을 만들지 않으므로 추가 사용자 확인은 필요하지 않다.

## Scope
- **In (current)**: Claude/Codex `spec-create`·`spec-upgrade` SKILL, package-local `references/hook-installation.md`; top-level AC/Hard Rule·Step·Validation·Output의 hook 설치 상세 single-home, 조건부 Read 시점, authoring canonical·배포 mirror parity
- **In (planned)**: Claude/Codex `spec-review`·`spec-rewrite` SKILL과 관련 reference/example, `spec-create` template selection, `spec-upgrade` mapping/template/temporary-spec reference; criterion/enums/load interface/current producer shape
- **Out**: hook script·template 본문·harness template의 동작 변경, hook event/matcher/command/trust 정책 변경, spec 작성 구조 재설계, P0/P2 skill, discussion
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | hook 설치 상세의 authoring single-home + 배포 mirror | `.claude/skills/spec-create/{SKILL.md,references/hook-installation.md}`<br>`.codex/skills/spec-create/{SKILL.md,references/hook-installation.md}`<br>`.claude/skills/spec-upgrade/{SKILL.md,references/hook-installation.md}`<br>`.codex/skills/spec-upgrade/{SKILL.md,references/hook-installation.md}` | `rg -n '훅 자산|PreToolUse|PostToolUse|SessionStart|hooks.json|project trust' <four SKILLs>` → 구현 전 Step·Validation·Output에 분산, new reference 0개; 기대 구현 후 literal 8 target | Task 1 |
| P2 | top-level AC/Hard Rule·Step·Validation·Output 상세의 reference pointer 전환 | `.claude/skills/spec-create/SKILL.md`<br>`.codex/skills/spec-create/SKILL.md`<br>`.claude/skills/spec-upgrade/SKILL.md`<br>`.codex/skills/spec-upgrade/SKILL.md` | `rg -n '바깥 그룹 객체 전체|fallback map|0\.124\.0\+|runtime별.*skip' <four SKILLs>`와 해당 section inspection → 같은 hook 계약의 반복 확인 | Task 1 |
| P3 | runtime/package parity와 protected asset 불변 | P1의 8 target + 네 skill root 각각의 `references/hooks/*.sh` 4개, `references/agents-harness-template.md` 1개, `references/template-{compact,full}.md` 2개(총 28 protected files) | `find <four roots>/references -path '*/hooks/*.sh' -o -name 'agents-harness-template.md' -o -name 'template-compact.md' -o -name 'template-full.md'` → 28개; 두 runtime SKILL은 구현 전 exact mirror | Task 2 |

# Part 2: Tasks

## Current Feature: spec-bootstrap-disclosure

### Task 1: hook 설치 계약을 조건부 rich reference로 추출한다

항상 읽는 본문에는 실행 경계와 load trigger만 남기고, 하네스를 생성/병합할 때에만 필요한 완전한 hook 설치 계약을 local reference에서 읽는다.

**Contracts**:
- `references/hook-installation.md`는 `Trigger and Inputs`, `Hook Asset Matrix`, `Verbatim Script Copy`, `Idempotent Settings Merge`(absent/existing/mixed/malformed cases), `Runtime Definitions`(두 complete JSON examples), `Codex Trust Boundary`, `Verification and Report`의 실행 가능한 section을 갖고 기존 hook 계약을 빠짐없이 소유한다.
- `spec-create` Step 3e는 `AGENTS.md` 하네스를 생성/병합할 때 local reference를 **Read하고 전부 적용한다**는 dispatcher만 남긴다. Companion Assets에 reference를 등록하고, top-level AC/Hard Rule·Validation·Output Contract의 hook 상세는 trigger/guardrail과 local `Verification and Report` pointer로 축약한다.
- `spec-upgrade` Step 6은 `#### Hook Assets` 실제 heading 아래 local reference를 Read한다. upgrade 고유 책임인 partial/legacy 설치를 current dual-runtime 상태로 보완하고 재실행 diff를 없애는 판단만 본문에 남긴다. Companion Assets·top-level AC·Validation·Output Contract도 local reference pointer로 바꾸며 `spec-create` 존재 여부에 의존하지 않는다.
- `.claude/skills/spec-create/references/hook-installation.md`가 authoring canonical이고 나머지 세 local reference는 exact 배포 mirror다. 모든 skill은 실행할 때 자기 package의 local reference만 읽으므로 독립 배포가 유지된다.

**Acceptance Criteria**:
- [ ] AC1: 네 `references/hook-installation.md`가 존재하고 authoring-canonical 표기와 배포-mirror 관계를 설명하며, canonical 대 나머지 세 파일의 `diff -u`가 모두 exit 0이다.
- [ ] AC2: `sed -n '/#### 3e\. 훅 자산 설치/,/### Step 4:/p'`로 추출한 `spec-create` 두 section은 local reference를 Read·전부 적용하는 trigger를 각 1건 포함하고, embedded JSON fence·merge case 상세·hook command는 0건이다.
- [ ] AC3: `sed -n '/#### Hook Assets/,/### Step 7:/p'`로 추출한 `spec-upgrade` 두 section은 local reference Read, partial/legacy 보완, 두 runtime, 재실행 diff 제거를 각각 포함한다. `spec-create` 의존·fallback map·command table은 0건이다.
- [ ] AC4: new reference의 일곱 required heading과 asset matrix 4행·settings case 4종·runtime JSON example 2개가 structure-aware check로 확인된다. `0.124.0+`, project trust, `/hooks`, trust 자동 승인 금지는 exact runtime anchors로 유지된다.
- [ ] AC5: 구현 ledger의 preservation matrix가 기존 hook clause 각각을 `old section → new reference section → remaining dispatcher/pointer`로 대응시켜 trigger, 두 runtime 동시 설치, script verbatim, absent/existing/mixed/malformed settings, non-SDD 설정 보존, 반대 runtime 계속, trust 경계, runtime별 report의 누락 0건을 보인다.
- [ ] AC6: 네 SKILL의 top-level AC/Hard Rule·`Validation`·`Output Contract` hook 상세는 trigger/guardrail과 local reference의 `Verification and Report` pointer로 축약되고, `rg -n 'fallback map|바깥 그룹 객체 전체|```json' <four SKILLs>`가 embedded implementation detail 0건을 출력한다.
- [ ] AC7: `.claude`/`.codex` `spec-create/SKILL.md` exact diff와 `spec-upgrade/SKILL.md` exact diff가 각각 exit 0이다.

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md` -- hook dispatcher와 Validation/Output pointer
- [M] `.codex/skills/spec-create/SKILL.md` -- exact mirror
- [C] `.claude/skills/spec-create/references/hook-installation.md` -- authoring canonical conditional contract
- [C] `.codex/skills/spec-create/references/hook-installation.md` -- exact distribution mirror
- [M] `.claude/skills/spec-upgrade/SKILL.md` -- local hook dispatcher, upgrade-only repair ownership, Validation/Output pointer
- [M] `.codex/skills/spec-upgrade/SKILL.md` -- exact mirror
- [C] `.claude/skills/spec-upgrade/references/hook-installation.md` -- portable exact distribution mirror
- [C] `.codex/skills/spec-upgrade/references/hook-installation.md` -- portable exact distribution mirror

### Task 2: mirror·reference·보호 계약을 read-only로 전수 검증한다

Task 1의 이동이 새 drift나 동작 손실을 만들지 않았는지 target과 protected assets를 분리해 검사한다. 파일은 수정하지 않는다.

**Acceptance Criteria**:
- [ ] AC8: 구현 전 baseline 뒤, 네 skill root에서 `git diff --name-only`와 `git ls-files --others --exclude-standard`의 합집합을 구해 literal 8 Target Files와 정확히 일치시킨다. 신규 reference의 untracked 상태를 포함하고 target 밖 추가 변경은 0건이다.
- [ ] AC9: `/Users/hyunjoonlee/miniconda3/bin/python3 /Users/hyunjoonlee/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>`를 네 directory에 실행해 모두 exit 0과 `Skill is valid!`를 얻는다. 네 SKILL의 local new-reference path는 실제 파일로 resolve된다.
- [ ] AC10: 구현 전 ledger에 기록한 28 protected files의 SHA-256 manifest와 구현 후 manifest가 exact match다. hook script·harness·template 자산 자체의 coverage delta는 0이다.
- [ ] AC11: frontmatter `name`·`description`, hook extraction과 무관한 Hard Rules, Step 순서와 non-hook Validation/Output 항목은 semantic diff 0이다. Companion·top-level hook AC/Hard Rule·Step·Validation·Output의 hook 상세만 Task 1이 허용한 pointer로 바뀐다.
- [ ] AC12: target diff를 `docs/SKILL_AUTHORING_NORMS.md` §3.1·§3.2·§3.3 기준으로 리뷰했을 때 single-home, criterion preservation, progressive disclosure, rich reference가 각각 MET이고 관측 근거가 있는 hard gate 약화가 0건이다.
- [ ] AC13: `git diff --check`가 exit 0이다.

**Target Files**:
- 없음 (read-only 검증)
