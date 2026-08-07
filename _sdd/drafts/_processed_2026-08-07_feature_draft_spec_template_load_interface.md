# Feature Draft: spec template load interface

> 규모 판정: 적격 — 기존 8개 파일 안에서 create와 upgrade를 두 구현 task로 닫고, 마지막 cross-task validation gate가 baseline·parity·asset census를 통합 검증한다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

**spec-template-load-interface (current)** — `spec-create`는 compact/full 선택 기준과 selected-only verbatim load를 Step 4에 고정한다. `spec-upgrade`는 boundary mapping→current global format 또는 current feature-draft producer→selected template을 실제 소비 시점에만 읽고, stale temporary-spec 설명본을 제거한다. Claude `spec-create` template을 existing authoring canonical로 보존하고 Codex distribution mirror는 runtime invocation token만 다르게 맞춘다.

판단 근거: template 선택과 load는 producer가 실제 문서를 쓰기 직전 알아야 하는 짧은 interface이고, mapping/format은 upgrade 단계별 rich reference다. Claude template은 authoring comment·optional-slot 의미를 보존해 규범의 rich reference/interface 기준에 더 가깝고, 이를 유지하면 Codex 두 파일만 맞추면 된다. Codex의 축약본을 양쪽에 적용하면 의미를 삭제하고 공통 canonical 파일을 새로 만들면 배포 구조가 늘어나므로 채택하지 않는다. 이 판단의 확신도는 높고, 새 구조나 사용자-facing 기능을 고르는 일이 아니므로 별도 사용자 확인은 필요하지 않다. 이 feature가 완료되면 P1 planned item은 남지 않는다.

## Scope

- **In**: Claude/Codex `spec-create`·`spec-upgrade` SKILL; compact/full criterion; selected-only point-of-use read; verbatim/slot-only apply; upgrade mapping/global-format/current-producer staged load; stale temporary-spec 설명 제거; Codex spec-create template semantic parity
- **Out**: hook/harness 계약, spec global core 재설계, template 신규 section/field 설계, examples 정리, 실제 consumer repo spec 생성/upgrade, P2 skill
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | spec-create compact/full selection + selected load | `.claude/skills/spec-create/SKILL.md`<br>`.codex/skills/spec-create/SKILL.md`<br>`.claude/skills/spec-create/references/template-compact.md` (read-only canonical)<br>`.claude/skills/spec-create/references/template-full.md` (read-only canonical)<br>`.codex/skills/spec-create/references/template-compact.md`<br>`.codex/skills/spec-create/references/template-full.md` | `rg -n 'references/template-(compact\|full)\.md' <two SKILLs>` → Companion list 4건, Step 4 load 0; template diff는 compact/full 모두 comments·slot guidance semantic drift + `/guide-create`↔`$guide-create` runtime line | Task 1 |
| P2 | spec-upgrade staged rich reference load | `.claude/skills/spec-upgrade/SKILL.md`<br>`.codex/skills/spec-upgrade/SKILL.md` | `rg -n 'references/(upgrade-mapping\|spec-format\|template-compact\|template-full)\.md|\.\./feature-draft/SKILL\.md' <two SKILLs>` → Companion list 8건, Step 1/2/5 load 0 | Task 2 |
| P3 | temporary producer single home | `.claude/skills/spec-upgrade/references/spec-format.md`<br>`.codex/skills/spec-upgrade/references/spec-format.md`<br>`.claude/skills/feature-draft/SKILL.md` (read-only producer)<br>`.codex/skills/feature-draft/SKILL.md` (read-only producer) | two spec-format files contain legacy temporary table row 12건; current Required Output은 feature-draft 두 runtime에 exact mirror로 존재 | Task 2 |
| P4 | protected asset·runtime parity | four package roots; expected current-feature changed set = four SKILL + two Codex create templates + two upgrade spec-format | initial scoped status에는 prior P1의 four SKILL `M` + four hook reference `??`만 존재. upgrade mapping pair·full template pair exact, compact template pair는 guide invocation 1-line delta | Task 3 |

# Part 2: Tasks

> **Implementation precondition (Task 1보다 먼저 실행):** ledger에 `SPEC_TEMPLATE_BASE=$(git rev-parse HEAD)`와 scoped status exact set을 기록하고, 아래 baseline을 SHA-256으로 고정한다: Claude create template 2개, upgrade mapping/template 6개, protected hook/harness asset 24개, four SKILL normalized text 4개. protected manifest는 four package roots(`.claude|.codex` × `spec-create|spec-upgrade`)와 six exact relative paths(`references/hook-installation.md`, `references/agents-harness-template.md`, `references/hooks/worklog-gate.sh`, `references/hooks/worklog-context.sh`, `references/hooks/harness-context.sh`, `references/hooks/agent-watchdog.sh`)의 Cartesian product다. normalizer는 UTF-8 bytes와 기존 EOL을 그대로 두고 (a) create에서 exact template asset-list line 2개, upgrade에서 exact mapping/format/template asset-list line 4개를 삭제하며, (b) 아래 허용 block이 있으면 start heading부터 exclusive end heading 직전까지만 삭제한다. 그 밖의 whitespace나 text는 정규화하지 않는다. 각 existing end anchor는 pre/post 정확히 1개여야 하고, start anchor는 pre 0개·post 1개여야 한다.

| SKILL | Allowed block start | Exclusive end |
|---|---|---|
| `spec-create` | `#### Template Selection and Load` | `### Step 5: Validate and Save` |
| `spec-upgrade` | `#### Asset Load: Upgrade Mapping` | `### Step 2: Legacy-to-Canonical Gap Analysis` |
| `spec-upgrade` | `#### Asset Load: Current Format` | `### Step 3: Evidence Collection` |
| `spec-upgrade` | `#### Template Selection and Load` | `### Step 6: Harness Merge (AGENTS.md / CLAUDE.md / .gitignore / 훅 자산)` |

### Task 1: spec-create의 template 선택과 소비 계약을 고정한다

single/multi-file Structure Decision과 compact/full content template 선택을 분리한다.

**Contracts**:

- compact가 기본값이다. source input에 project motivation 또는 evaluated-alternative rationale가 명시돼 있고 compact의 existing named slot에 그 고유한 rationale 역할을 보존할 수 없을 때만 full을 고른다.
- Step 4 작성 직전에 선택한 runtime-local template만 Read한다.
- 선택한 template 파일의 전체 skeleton을 verbatim 복사해 heading·field order를 보존하고, source evidence로 placeholder를 치환하며 evidence가 없는 optional block은 제거한다. 기억이나 SKILL 본문으로 재구성하지 않는다.
- Claude template pair는 existing authoring canonical로 무변경 유지한다. Codex pair는 같은 content의 distribution mirror이며 `/guide-create`만 `$guide-create`로 바꾼다.
- 두 template path는 Companion Assets 중복 목록에서 제거하고 Step 4 selection table이 유일한 local path map을 소유한다.

**Acceptance Criteria**:

- [ ] AC1: 두 SKILL의 Step 4 `Template Selection and Load` section-aware assertion이 compact default, project-motivation/evaluated-alternative rationale와 semantic-loss criterion, selected-only Read, 전체 template skeleton의 verbatim heading/order, evidence-based placeholder/optional removal, 재구성 금지를 모두 확인한다.
- [ ] AC2: 각 SKILL에서 `references/template-compact.md`·`references/template-full.md`가 Step 4 table에 각각 정확히 1번 존재하고 Companion Assets에는 0건이다. template selection은 Structure Decision의 single/multi-file 결과와 독립임을 명시한다.

**Target Files**:

- [M] `.claude/skills/spec-create/SKILL.md` — selection/load owner
- [M] `.codex/skills/spec-create/SKILL.md` — exact semantic mirror
- [M] `.codex/skills/spec-create/references/template-compact.md` — Claude canonical distribution mirror + runtime invocation
- [M] `.codex/skills/spec-create/references/template-full.md` — Claude canonical distribution mirror + runtime invocation

### Task 2: spec-upgrade reference를 단계별로 읽고 current format을 쓴다

upgrade는 rich reference를 startup preload하지 않고 판정·gap·migration 소비 지점에만 읽는다.

**Contracts**:

- Step 1 본문만으로 upgrade↔rewrite boundary 또는 legacy destination이 닫히지 않을 때만 `references/upgrade-mapping.md`를 읽는다.
- Step 2에서 exact current global shape 비교가 필요할 때는 `references/spec-format.md`, global에 섞인 temporary portion 판정이 필요할 때는 current runtime의 `../feature-draft/SKILL.md` `Required Output`을 읽는다.
- Step 5는 Task 1과 같은 closed compact/full criterion을 사용하고, migration 작성 직전에 선택한 `template-compact.md | template-full.md`만 Read해 verbatim/slot-only로 적용하며 source evidence가 있는 slot만 채운다.
- 네 local reference path는 Companion Assets 중복 목록에서 제거하고 Step 1/2/5 mapping이 단일 홈이다. temporary portion의 shape는 sibling producer가 단독 소유한다.
- `spec-format`의 stale `Temporary Spec Reference` block은 제거하고 global format reference만 남긴다.
- upgrade mapping과 compact/full template 내용은 변경하지 않는다.

**Acceptance Criteria**:

- [ ] AC3: 두 SKILL에서 Step 1 conditional→`upgrade-mapping`, Step 2 exact global→`spec-format`·mixed temporary→sibling `feature-draft` Required Output, Step 5 selection→compact/full 중 하나의 exact staged mapping을 assertion한다. 각 path literal은 stage-local home에 정확히 1회, Companion Assets에 0건이다.
- [ ] AC4: Step 5 criterion이 compact default, project-motivation/evaluated-alternative rationale와 semantic-loss criterion, selected-only, verbatim/slot-only를 Task 1과 semantic exact로 공유한다. 두 `spec-format`은 global reference를 byte-exact로 유지하고 `Temporary Spec Reference` heading과 legacy 7-section literal은 0건이며, sibling `feature-draft` Required Output 두 runtime은 exact mirror다.

**Target Files**:

- [M] `.claude/skills/spec-upgrade/SKILL.md` — staged load + selected template owner
- [M] `.codex/skills/spec-upgrade/SKILL.md` — exact semantic mirror
- [M] `.claude/skills/spec-upgrade/references/spec-format.md` — current temporary shape
- [M] `.codex/skills/spec-upgrade/references/spec-format.md` — exact mirror

### Task 3: cross-task baseline·protected surfaces·parity를 read-only로 검증한다

prior P1 bootstrap 변경을 보존하면서 이번 feature가 만든 delta만 분리 검증한다. 파일은 수정하지 않는다.

**Acceptance Criteria**:

- [ ] AC5: implementation precondition은 target edit보다 먼저 실행됐고 ledger가 base commit, scoped status exact set(four SKILL `M` + four hook refs `??`), Claude create template 2개·upgrade mapping/template 6개·protected manifest 24개 SHA-256, deterministic normalizer의 four pre-hash를 path별로 출력한다.
- [ ] AC6: 구현 후 scoped status set difference는 two upgrade spec-format `M` + two Codex create template `M`뿐이다. four prior SKILL `M`·four hook `??`는 유지되고 그 외 `A/D/??` 증가는 0이다.
- [ ] AC7: 같은 normalizer의 pre/post digest가 `NORMALIZED_SKILL_PASS 4/4`, protected manifest pre/post digest가 `PROTECTED_ASSETS_PASS 24/24`를 출력한다. 이 비교가 hook-installation pointer를 포함한 허용 block 밖 SKILL text와 package-local hook/harness assets를 단독 기준으로 보호한다.
- [ ] AC8: pinned `quick_validate.py`가 four skill dirs에서 4/4 `Skill is valid!`; stage-local asset path 14개(local reference 12 + same-runtime producer 2)가 resolve되어 `ASSET_PATHS_PASS 14/14`를 출력한다.
- [ ] AC9: reviewer가 `docs/SKILL_AUTHORING_NORMS.md` §3.1–§3.4에 대해 selected-only load, criteria-not-example, rich reference, verbatim interface, single-home path map을 target citation과 `MET|NOT MET`로 반환한다. NOT MET는 unresolved AC다.
- [ ] AC10: Claude/Codex four SKILL current byte-exact, upgrade spec-format exact, create template two pairs는 `` `/guide-create` `` ↔ `` `$guide-create` `` token normalization 후 byte-exact, Claude create template와 upgrade mapping/template 8개는 baseline-preserved이며 `git diff --check`가 exit 0이다.

**Target Files**:

- 없음 (read-only 검증)
