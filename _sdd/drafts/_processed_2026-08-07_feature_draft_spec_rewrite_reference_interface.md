# Feature Draft: spec rewrite reference interface

> 규모 판정: 단일 컨텍스트 적격 — 기존 12개 파일만 수정하며 point-of-use load, temporary-spec shape, producer example을 네 task로 독립 검증할 수 있다. 후속 template-load feature는 Part 1에만 유지한다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

P1의 남은 두 feature를 순차 처리한다.

1. **spec-rewrite-reference-interface (current)** — `spec-rewrite`의 format·checklist·target template을 실제 소비 시점에 읽고, temporary-spec exact skeleton은 복사 가능한 template 한 곳만 소유하게 한다. 단일 사용처에서 producer interface를 재구현하던 plan/report example은 제거한다.
2. **spec-template-load-interface (planned)** — `spec-create`의 compact/full 선택·selected-template load와 `spec-upgrade`의 mapping·format·template 단계별 load 계약 및 stale producer shape를 별도 feature로 닫는다.

판단 근거: rewrite assets는 한 실행에서 함께 소비되는 interface이고 Claude/Codex package의 동일 asset set을 동시에 바꿔야 producer/consumer drift가 닫힌다. template 선택은 다른 skill pair와 target set을 가지므로 이번 범위에서 제외한다. architecture 선택은 없으며 확신도는 높다.

## Scope

- **In (current)**: Claude/Codex `spec-rewrite` SKILL, `rewrite-checklist`, `spec-format`, `template-compact`; point-of-use load timing; no-rewrite exit; current temporary-spec verbatim skeleton; redundant plan/report example 삭제; runtime invocation delta 보존
- **In (planned)**: Claude/Codex `spec-create`·`spec-upgrade`의 template/mapping/format load interface
- **Out**: rewrite diagnosis axes·Hard Rules·output artifact paths 변경, 새 rewrite 기능/metric, 실제 repo spec rewrite, template 내용 신규 설계, P2 skill
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | point-of-use rich asset load | `.claude/skills/spec-rewrite/SKILL.md`<br>`.codex/skills/spec-rewrite/SKILL.md` | `rg -n 'references/(template-compact\|spec-format\|rewrite-checklist)\|examples/(rewrite-plan\|rewrite-report)' <two SKILLs>` → baseline 10건이 Companion Assets에만 있고 Step-local path 0건 | Task 1 |
| P2 | current temporary-spec producer shape | `.claude/skills/spec-rewrite/references/rewrite-checklist.md`<br>`.claude/skills/spec-rewrite/references/spec-format.md`<br>`.claude/skills/spec-rewrite/references/template-compact.md`<br>`.codex/skills/spec-rewrite/references/rewrite-checklist.md`<br>`.codex/skills/spec-rewrite/references/spec-format.md`<br>`.codex/skills/spec-rewrite/references/template-compact.md` | `rg -n 'Scope Delta\|Contract/Invariant Delta\|Touchpoints\|Implementation Plan\|Validation Plan\|Risks / Open Questions' <six paths>` → legacy 이름 24건 | Task 2 |
| P3 | redundant single-use examples | `.claude/skills/spec-rewrite/examples/rewrite-plan.md`<br>`.claude/skills/spec-rewrite/examples/rewrite-report.md`<br>`.codex/skills/spec-rewrite/examples/rewrite-plan.md`<br>`.codex/skills/spec-rewrite/examples/rewrite-report.md` | 각 example은 SKILL Step 2/4의 단일 소비처에서 producer field를 재열거하고 baseline report에는 producer taxonomy 밖 metric 3개가 있음 | Task 3 |
| P4 | runtime parity·hard contract preservation | `.claude/skills/spec-rewrite/**`<br>`.codex/skills/spec-rewrite/**` (baseline union 12; expected current change set 8 `M` + 4 `D`) | scoped baseline status 0; sha256 pair census → SKILL·checklist·format·plan/report 5쌍 exact; `diff -u <template pair>` → Claude `/guide-create` ↔ Codex `$guide-create` 1-line runtime delta만 존재 | Task 4 |

# Part 2: Tasks

## Current Feature: spec-rewrite-reference-interface

### Task 1: SKILL에 point-of-use asset load interface를 둔다

Local asset census는 각 소비 단계가 직접 소유한다. Companion Assets에는 외부 SDD 정의 link만 남긴다.

**Contracts**:

- Step 1의 본문 기준만으로 global/temporary/mixed type이나 target shape 비교가 닫히지 않을 때만 `references/spec-format.md`를 읽는다.
- 잘 구조화되어 rewrite가 불필요하면 개선점만 보고 종료하며 Steps 2–4와 그 단계 asset을 읽거나 실행하지 않는다.
- rewrite가 필요해 Step 2에 진입할 때만 `references/rewrite-checklist.md`를 읽어 보존 기준을 고정한다.
- Step 3에서 실제 target shape를 재구성할 때만 `references/template-compact.md`를 읽고, fenced skeleton을 verbatim 복사해 heading·marker·field order를 보존한다. placeholder 치환·필요한 row/task 반복·조건부 block 제거만 허용한다.
- SDD 정의 URL은 기존 companion link로 유지하며 이번 feature가 fetch 정책을 만들지 않는다.

**Acceptance Criteria**:

- [ ] AC1: section-aware assertion이 두 SKILL에서 Step 1 conditional→`spec-format`, no-rewrite→Steps 2–4 종료, rewrite/Step 2 entry→`rewrite-checklist`, Step 3 actual reshape→`template-compact`의 three-asset/three-stage mapping과 각 조건을 확인한다. Step 3은 `verbatim`, heading·marker·field order 보존, 허용 치환/반복/제거를 포함한다.
- [ ] AC2: `rg -n 'examples/(rewrite-plan|rewrite-report)' <two SKILLs>`가 0건이고, 세 package-local path는 각 SKILL의 자기 `Asset load` line에 정확히 한 번만 존재한다. Companion Assets에는 local asset list가 없고 SDD definition link만 유지된다.
- [ ] AC3: ledger baseline/current의 `Companion Assets` 절, `> Asset load:`·`> No-rewrite exit:` prefix line만 sentinel 치환한 뒤 두 SKILL을 exact 비교한다. 기존 Acceptance Criteria 7개, SDD Lens 6개, Hard Rules 6개, diagnosis axes 8개, Output Contract 3개, Error Handling 5행, Final Check의 허용 밖 diff가 0이어야 한다.

**Target Files**:

- [M] `.claude/skills/spec-rewrite/SKILL.md` — point-of-use load producer
- [M] `.codex/skills/spec-rewrite/SKILL.md` — exact semantic mirror

### Task 2: rewrite reference를 current canonical shape로 교정한다

`template-compact`가 exact temporary skeleton을 단독 소유하고 다른 두 reference는 자기 고유 역할과 pointer만 가진다.

**Contracts**:

- `template-compact`는 feature-draft Required Output의 `# Feature Draft`, 규모 판정, marker, Part 1, 조건부 5-column propagation table, Part 2 task, optional `Contracts`, AC, Target Files, 조건부 Open Questions를 복사 가능한 fenced skeleton으로 소유한다.
- oversized rolling split은 Part 1의 각 current/planned feature에 one-line intent+scope를 보존하고 Part 2에는 current feature task만 상세화한다. legacy 7-section 표는 제거한다.
- `spec-format`은 temporary spec의 역할과 `template-compact` pointer만 소유하고 exact schema를 반복하지 않는다.
- `rewrite-checklist`는 exact template 보존, 조건부 block trigger, AC evidence, body placement, rolling intent/scope를 묻고 schema를 반복하지 않는다.

**Acceptance Criteria**:

- [ ] AC4: `rg -n 'Scope Delta|Contract/Invariant Delta|Touchpoints|Implementation Plan|Validation Plan|Risks / Open Questions' <six literal reference paths>`가 heading/table/list 형식과 무관하게 0건이다.
- [ ] AC5: 두 `template-compact` fenced block이 feature-draft Required Output과 field/heading/marker order를 exact 비교해 placeholder·설명 값 외 semantic diff 0이다. propagation table은 header+delimiter+example row를 갖고 `Contracts`와 Open Questions는 conditional이다. 두 `spec-format`과 `rewrite-checklist`는 `template-compact.md` pointer를 각각 한 번 가지며 exact schema field census를 반복하지 않는다.
- [ ] AC6: template pair가 rolling split의 feature별 one-line intent+scope와 Part 2 current-only 경계를 명시하고, checklist pair가 그 보존 여부를 묻는다. spec-format은 rolling rule을 재서술하지 않고 template pointer로 위임한다.
- [ ] AC7: ledger baseline/current에서 각 reference의 `## Temporary Spec` heading부터 EOF만 `<TEMPORARY_SPEC>`로 치환해 exact 비교한다. 세 global-spec section의 required order, global anti-pattern 4개, checklist Shared/Global 항목, template global shape의 허용 밖 diff는 0이어야 한다.

**Target Files**:

- [M] `.claude/skills/spec-rewrite/references/rewrite-checklist.md`
- [M] `.codex/skills/spec-rewrite/references/rewrite-checklist.md`
- [M] `.claude/skills/spec-rewrite/references/spec-format.md`
- [M] `.codex/skills/spec-rewrite/references/spec-format.md`
- [M] `.claude/skills/spec-rewrite/references/template-compact.md`
- [M] `.codex/skills/spec-rewrite/references/template-compact.md`

### Task 3: 단일 사용처 plan/report example을 제거한다

Output field의 단일 소스는 SKILL Step 2·4다. 이를 한 소비처에서 재구현하는 example 자산과 load pointer를 제거한다.

**Contracts**:

- Claude/Codex `examples/rewrite-plan.md`·`rewrite-report.md` 네 파일을 삭제한다.
- 두 SKILL의 Companion Assets와 Process에서 `examples/` pointer는 0건이다.
- Step 2 plan field와 Step 4 validation/report field는 기존 producer list를 그대로 소유하며 example 삭제를 이유로 새 field·metric·threshold를 추가하지 않는다.

**Acceptance Criteria**:

- [ ] AC8: 네 example path가 모두 absent이고 scoped status에서 exact `D` set으로 나타난다.
- [ ] AC9: baseline/current SKILL의 Step 2 `plan에는 아래를 포함한다` list와 Step 4 validation/report list를 exact 비교해 semantic diff 0이다. `rg -n 'examples/|Repo Purpose Clarity|Contamination Control|Decision visibility' <two SKILLs>`가 0건이다.
- [ ] AC10: reviewer가 deleted example의 unique decision-bearing content가 0인지, producer interface가 SKILL에 완전하게 남았는지 `REDUNDANT_REMOVAL_MET | CONTENT_LOSS:<items>`로 판정하며 두 runtime 모두 `REDUNDANT_REMOVAL_MET`이다.

**Target Files**:

- [D] `.claude/skills/spec-rewrite/examples/rewrite-plan.md`
- [D] `.codex/skills/spec-rewrite/examples/rewrite-plan.md`
- [D] `.claude/skills/spec-rewrite/examples/rewrite-report.md`
- [D] `.codex/skills/spec-rewrite/examples/rewrite-report.md`

### Task 4: target census와 runtime parity를 read-only로 검증한다

Task 1–3 밖의 skill contract나 runtime-specific invocation이 바뀌지 않았는지 전수 확인한다. 파일은 수정하지 않는다.

**Acceptance Criteria**:

- [ ] AC11: 구현 시작 시 ledger에 `SPEC_REWRITE_BASE=$(git rev-parse HEAD)`와 `git status --short -- .claude/skills/spec-rewrite .codex/skills/spec-rewrite`의 empty output을 기록한다. 구현 후 같은 command는 surviving eight Target Files의 literal `M`과 four example Target Files의 literal `D`만 출력하고 `??/A`는 0건이다.
- [ ] AC12: Claude/Codex SKILL·checklist·spec-format 세 쌍은 byte-exact다. template pair의 유일한 semantic delta는 Claude `` `/guide-create` `` ↔ Codex `` `$guide-create` `` invocation 한 줄이고 나머지는 normalization 후 exact다. deleted example pair는 양 runtime 모두 absent다.
- [ ] AC13: `/Users/hyunjoonlee/miniconda3/bin/python3 /Users/hyunjoonlee/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>`를 `.claude/skills/spec-rewrite`, `.codex/skills/spec-rewrite`에 각각 실행해 2/2 `Skill is valid!`이다. Python path resolver가 두 SKILL의 stage-local Markdown path 6개를 package-local 기준으로 resolve해 `ASSET_PATHS_PASS 6/6`을 출력한다.
- [ ] AC14: 단일 Python checker가 ledger baseline을 `git show`로 읽고 (a) SKILL은 `Companion Assets` 절과 `> Asset load:`·`> No-rewrite exit:` prefix line, (b) 세 reference는 `## Temporary Spec` heading부터 EOF를 sentinel로 치환해 surviving eight files의 허용 밖 diff 0을 확인한다. 네 example은 baseline에 존재하고 current에는 absent인지 별도 확인한다. 모두 통과하면 `SPEC_REWRITE_ALLOWED_DIFF_PASS surviving=8 deleted=4`를 출력한다.
- [ ] AC15: reviewer가 `docs/SKILL_AUTHORING_NORMS.md` §3.1·§3.2·§3.3·§3.4에 대해 target citation과 evidence-backed `MET|NOT MET`를 반환한다. `NOT MET`가 있으면 unresolved AC로 남긴다. conditional load, template verbatim/slot-only 적용, schema·producer interface single-home, redundant example 제거를 포함한다.
- [ ] AC16: `git diff --check`가 exit 0이다.

**Target Files**:

- 없음 (read-only 검증)
