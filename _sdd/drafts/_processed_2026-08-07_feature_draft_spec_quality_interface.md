# Feature Draft: spec quality interface

> 규모 판정: 분할 필요 — 분할 계획 포함. review verdict, rewrite reference, template load는 change element와 target set이 독립적이므로 Part 1에 세 feature를 고정하고 Part 2에는 첫 feature만 상세화한다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
P1 2/2 umbrella를 세 개의 독립 feature로 순차 처리한다.

1. **spec-review-deterministic-interface (current)** — `spec-review`의 drift status와 spec disposition decision을 예시가 아닌 ordered allowed enum + 판정 기준으로 고정하고 Output Drift Summary가 이를 직접 소비하게 한다. decision이 소비하지 않는 고정 metrics 의식은 제거하며, code analysis는 scope 선택이나 finding을 실제로 뒷받침할 때만 조건부 evidence로 남긴다.
2. **spec-rewrite-reference-interface (planned)** — `spec-rewrite`가 rewrite checklist/plan/report reference를 실제 소비 시점에 읽고, example이 producer output shape를 완전히 대표하도록 만든다. rewrite의 temporary-spec reference는 현재 `Part 1: Spec Delta` + 선택적 `Propagation Surfaces` + `Part 2: Tasks` 계약으로 교정한다.
3. **spec-template-load-interface (planned)** — `spec-create`의 compact/full 선택 기준과 selected-template load 시점을 명시하고, `spec-upgrade`의 mapping/spec-format/template을 stale producer shape 교정과 함께 단계별로 읽는다. 기억 기반 template 재구성을 금지하되 template 내용 자체는 새로 설계하지 않는다.

판단 근거: verdict enum, rewrite 산출물, template 선택은 서로 다른 producer/consumer interface라 한 task가 공동 소유하면 검증 범위가 눈검산 불가능해진다. current feature는 기존 2-file exact mirror만 수정하며 새 reference가 필요 없다. 확신도는 높고 사용자 확인이 필요한 architecture 선택은 없다.

## Scope
- **In (current)**: Claude/Codex `spec-review/SKILL.md`; drift status·spec disposition decision의 ordered routing, Output Drift Summary schema, decision과 무관한 고정 metric ceremony 제거, 조건부 analysis evidence 경계
- **In (planned)**: Claude/Codex `spec-rewrite` SKILL·reference·example; Claude/Codex `spec-create`·`spec-upgrade` SKILL과 relevant template/mapping/spec-format reference
- **Out**: review severity 3단계, global/temporary rubric, review-only/파일 경계, report 경로, actual spec 수정, hook/harness 계약, P2 skill
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | drift status ordered enum + output consumer | `.claude/skills/spec-review/SKILL.md`<br>`.codex/skills/spec-review/SKILL.md` | `rg -n '상태 예시|ALIGNED|DRIFT|MISSING|UNTESTED|## 5\. Drift Summary' <two SKILLs>` → 값은 있으나 ordered criterion·MISSING direction·output schema 없음 | Task 1 |
| P2 | spec disposition decision ordered enum | 같은 두 SKILL | `rg -n 'decision 예시|SPEC_OK|SYNC_REQUIRED|NEEDS_DISCUSSION' <two SKILLs>` → implementation-only drift gap과 material uncertainty overlap 확인 | Task 1 |
| P3 | 고정 metric ceremony 제거 + 조건부 evidence | 같은 두 SKILL | `rg -n 'head -20|Focus Score|Test Coverage|Code Analysis Metrics' <two SKILLs>` → decision이 소비하지 않는 fixed cutoff/placeholder가 본문·output에 반복 | Task 1 |
| P4 | mirror·review-only·rubric 보존 | 같은 두 SKILL | 구현 전 Claude/Codex byte-exact; report canonical path는 value 1종·occurrence 2건/file | Task 2 |

# Part 2: Tasks

## Current Feature: spec-review-deterministic-interface

### Task 1: spec-review의 status·decision 판정 인터페이스를 명시한다

항상 읽는 짧은 interface이므로 SKILL 본문에 유지하며 별도 reference를 만들지 않는다.

**Contracts**:
- `Drift Status (allowed values)`는 아래 ordered routing으로 정확히 하나를 고른다.
  1. 필요한 evidence의 수집이 불완전하거나 비교하기에 불충분하거나 기대한 양쪽 surface가 모두 부재하면 `UNTESTED`다. 단순 접근 실패를 `MISSING`으로 오판하지 않는다.
  2. 필요한 범위를 끝까지 탐색했고 기대한 한쪽 surface가 실제로 부재하면 `MISSING`이며 direction을 `SPEC_MISSING | IMPLEMENTATION_MISSING` 중 하나로 기록한다.
  3. 양쪽 evidence가 비교 가능하면 일치할 때 `ALIGNED`, 충돌할 때 `DRIFT`다.
  모든 status는 concrete evidence를 요구하고 `MISSING` 이외의 direction은 `N/A`다.
- `Decision (allowed values)`는 spec 변경 필요 여부라는 단일 축에서 아래 precedence로 정확히 하나를 고른다.
  1. material uncertainty나 authority/scope/contract ambiguity 때문에 spec 변경 필요 여부를 결정할 수 없으면 `NEEDS_DISCUSSION`.
  2. 그렇지 않고 verified evidence가 spec 변경 필요를 입증하면 `SYNC_REQUIRED`.
  3. 그 외에는 `SPEC_OK`. implementation-only drift는 `SPEC_OK`로 두되 별도 next action에 구현 측 조치를 기록한다. Improvements만 있는 경우도 `SPEC_OK`가 가능하다.
- 기존 Step 3.5의 고정 metric 3종은 제거한다. revision/history/change-set 분석은 scope 선택 또는 finding을 실제로 뒷받침할 때만 수행하고, 사용했다면 Output Format의 `Optional Code Analysis Evidence` schema에 bounded window·method·결과·연결된 finding을 기록한다. 쓰지 않았으면 section을 생략하며 placeholder나 임의 수치를 만들지 않는다. Process는 실행 조건만, Output은 필드 shape만 소유한다.
- Output Format의 `Drift Summary`는 exact `Surface | Drift Status | Direction | Evidence` header와 Step 3 producer pointer만 가지며 enum example row를 반복하지 않는다. Decision field도 값을 재열거하지 않고 Step 4 producer를 가리킨다.

**Acceptance Criteria**:
- [ ] AC1: section-aware Python assertion이 두 SKILL의 `#### Drift Status (allowed values)`에서 allowed set `ALIGNED|DRIFT|MISSING|UNTESTED`, ordered route 3단계, direction set `SPEC_MISSING|IMPLEMENTATION_MISSING|N/A`를 확인한다. 반례 matrix `불충분 evidence 또는 양쪽 부재→UNTESTED`, `탐색 완료+spec만 부재→MISSING/SPEC_MISSING`, `탐색 완료+implementation만 부재→MISSING/IMPLEMENTATION_MISSING`, `양면 일치→ALIGNED`, `양면 충돌→DRIFT`가 각각 단일 route다.
- [ ] AC2: 같은 assertion이 `#### Decision (allowed values)`의 exact set `SPEC_OK|SYNC_REQUIRED|NEEDS_DISCUSSION`와 material uncertainty 우선 precedence를 확인한다. 반례 matrix `material uncertainty+sync 후보→NEEDS_DISCUSSION`, `verified spec-side drift→SYNC_REQUIRED`, `implementation-only drift→SPEC_OK + implementation next action`, `spec change 불필요→SPEC_OK`가 각각 단일 route다.
- [ ] AC3: `rg -n 'head -20|Focus Score|Test Coverage|Code Analysis Metrics|상태 예시|decision 예시' .claude/skills/spec-review/SKILL.md .codex/skills/spec-review/SKILL.md`가 0건이다. Step 3.5는 analysis 실행 조건·Output Format pointer·미사용 시 section 생략을, Output의 `Optional Code Analysis Evidence`는 bounded window·method·result·finding link 4필드를 소유한다.
- [ ] AC4: 두 Output Format의 Decision field가 Step 4 producer를 가리키고, `## 5. Drift Summary`가 exact 4-column schema `Surface | Drift Status | Direction | Evidence`와 Step 3 producer pointer를 가진다. Output에는 enum example row, 고정 metric row, placeholder가 없다.
- [ ] AC5: 기존 `Critical|Quality|Improvements` severity, global/temporary/code-linked rubric, review-only/no-spec-write, lowercase report path, evidence가 불충분하면 UNTESTED라는 hard criterion은 허용 section 밖 exact comparison과 reviewer citation으로 semantic diff 0이다.

**Target Files**:
- [M] `.claude/skills/spec-review/SKILL.md` -- ordered status/decision producer와 output consumer
- [M] `.codex/skills/spec-review/SKILL.md` -- exact mirror

### Task 2: mirror·rubric·출력 계약을 read-only로 검증한다

Task 1의 interface 변경 밖에 rubric/파일 경계 drift가 없는지 전수 확인한다. 파일은 수정하지 않는다.

**Acceptance Criteria**:
- [ ] AC6: 구현 시작 시 ledger에 `SPEC_REVIEW_BASE=$(git rev-parse HEAD)` 값을 기록하고 두 target의 scoped `git status --short`가 clean임을 확인한다. 구현 후 같은 scoped status는 literal 두 Target Files의 `M`만 출력하고 관련 directory의 `??/A/D`는 0건이다.
- [ ] AC7: `/Users/hyunjoonlee/miniconda3/bin/python3 /Users/hyunjoonlee/.codex/skills/.system/skill-creator/scripts/quick_validate.py <each skill dir>`가 두 번 모두 `Skill is valid!`다. report canonical path는 unique value 1종이고 기존 occurrence 2건/file을 유지한다.
- [ ] AC8: ledger의 `SPEC_REVIEW_BASE`에서 `git show <base>:<path>`로 baseline을 읽고, heading-anchored 허용 블록(`Drift Status`, Step 3.5, `Decision`, Output Decision/Drift Summary/optional analysis)만 token normalization한 뒤 current와 exact 비교한다. 두 파일 모두 허용 블록 밖 diff 0이며 Claude/Codex current exact diff도 exit 0이다.
- [ ] AC9: reviewer가 `docs/SKILL_AUTHORING_NORMS.md` §3.1·§3.2·§4 각각에 대해 target hunk citation과 `MET|NOT MET`를 반환한다. example→criterion, arbitrary knob 제거, producer/output interface 정합, hard-gate criterion 보존이 모두 MET다.
- [ ] AC10: `git diff --check`가 exit 0이다.

**Target Files**:
- 없음 (read-only 검증)
