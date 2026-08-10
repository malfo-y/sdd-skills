# Feature Draft: 과다 finding 회차의 bounded second review-fix

> 규모 판정: 적격 — 동일 gate 정책을 producer skill 2종의 Claude/Codex 미러와 사용자 문서 2쌍에 전파하는 2개 작성 task + 1개 read-only census로, 변경 요소와 owner task 대응을 눈으로 검산할 수 있다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
`feature-draft`와 `implementation`의 현행 `gate 1회 → fix 1회 → finding 과다 시 추가 gate 권고` 계약을 bounded conditional retry로 바꾼다.

- 각 gate 호출 자체는 reviewer가 소유한 **단일 패스**다. producer가 첫 호출과 fix를 항상 수행하고, fix 전 합산 finding이 기존 임계값(`Critical+High ≥ 3` 또는 `Medium ≥ 5`, Low 제외, `implementation-review` shard 합산은 dedup 없음)에 도달한 경우에만 같은 gate를 한 번 더 호출한다.
- 두 번째 호출의 Critical/High/Medium finding은 producer가 fix 2로 반영한다. Low는 첫 호출과 같은 렌즈별 정책을 적용한다.
- fix 2 뒤에는 finding별 표적 검증과 producer별 마감 검증을 수행하고 종료한다. 세 번째 gate 호출은 금지한다. 해소할 수 없는 finding은 숨기지 않고 잔존으로 보고한다.
- `implementation`의 fix 2는 fix diff에 커버리지 델타를 적용한 뒤 회귀를 재실행하고 AC→증거 테이블을 갱신한다. `feature-draft`의 fix 2는 final draft에서 finding이 인용한 평가조건을 다시 확인하고 검증 evidence를 마감에 남긴다.
- gate 소유자는 계속 producer이며 `sdd-autopilot`·사용자는 gate를 별도 호출하거나 fix하지 않는다. `plan-review`·`implementation-review`와 reviewer agent의 호출당 single-pass/read-only/relay 계약은 변경하지 않는다.
- 기존 과다-finding advisory 문구는 자동 두 번째 호출로 대체된다. 최종 보고는 두 호출의 severity와 fix/검증 결과를 구분해 표시한다.

Global spec 반영은 `spec-sync` 소관이다. `_sdd/spec/main.md`의 producer gate guardrail·결정 표, `_sdd/spec/components.md`의 `sdd-autopilot`/`plan-review`/`implementation`/`implementation-review` 행, `_sdd/spec/usage-guide.md`의 수동·autopilot 시나리오를 새 계약에 맞추고 decision log·changelog에 기존 v4.6.30 advisory-only 결정을 supersede하는 이력을 남긴다.

## Scope
- **In**: `feature-draft`·`implementation` producer의 조건부 두 번째 gate/fix, fix 2 후 표적 검증·마감 검증, 최대 2회 상한, 최종 보고, Claude/Codex producer 미러, 한·영 workflow/autopilot 안내, 후속 global spec sync.
- **Out**: 임계값 수치·합산 방식 변경, reviewer agent·review orchestrator의 단일 호출 내부 구조 변경, third review, PR review 정책, goal-init/rolling goal 전환, unrelated `investigate` fix loop.
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | producer-owned conditional second gate/fix + hard stop after fix 2 | `.claude/skills/{feature-draft,implementation}/SKILL.md`; `.codex/skills/{feature-draft,implementation}/SKILL.md` | `rg -l 'Critical\+High ≥ 3|Medium ≥ 5|finding이 많았으니' .claude/skills .codex/skills`의 해당 producer 기대 집합 = 4파일 | Task 1 |
| P2 | 사용자에게 보이는 gate 횟수·무승인 ownership·비용 설명 | `docs/{SDD_WORKFLOW,AUTOPILOT_GUIDE}.md`; `docs/en/{SDD_WORKFLOW,AUTOPILOT_GUIDE}.md` | `rg -l -i 'fix 1회|one fix|single fix|review-fix loop|재리뷰 없음|review loop는 돌리지|내부에서 1회 수행|추가 실행을 권장|finding이 많았으니|~1분' docs` 기대 집합 = 정확히 4파일 | Task 2 |

# Part 2: Tasks

### Task 1: Producer 두 종에 최대 2회 review-fix 계약 적용
두 producer의 gate controller를 bounded conditional retry 계약으로 정렬한다.

**Contracts**: 첫 gate는 항상 1회, fix 1은 항상 C/H/M 대상이다. fix 전 raw 합산이 `C+H ≥ 3 OR M ≥ 5`일 때만 gate 2와 fix 2를 수행한다(Low 제외, implementation shard dedup 없음). gate 2 뒤에는 gate 3 없이 표적 검증으로 종료한다. gate 2를 호출했으면 두 호출의 finding/fix/검증을 구분해 보고하고, gate 2를 호출하지 않았으면 기존 1회 경로를 유지한다.

**Acceptance Criteria**:
- [ ] AC1: 네 producer SKILL 모두 첫 gate→fix 1, 기존 임계값 판정, 임계값 도달 시 같은 gate의 두 번째 호출→fix 2, gate 3 금지의 순서를 명시한다. 평가: 네 파일의 gate 절을 인용한 구조 rubric에서 네 단계가 모두 존재하고 순서가 어긋난 사례가 0건이며, `각 gate 호출은 단일 패스`라는 허용 문면과 `producer 전체가 gate/fix를 총 1회만 수행`한다는 금지 문면을 구분해 후자 모순이 0건이면 PASS; evidence = 파일별 anchor와 line citation.
- [ ] AC2: 임계값과 합산 semantics가 현행과 동일하다 — `Critical+High ≥ 3 OR Medium ≥ 5`, Low 제외, implementation-review는 shard 합산 dedup 없음. 평가: Claude/Codex 두 producer 쌍에서 값·연산·dedup 문면을 추출한 결과가 pair별 동일하고 기존 `_sdd/spec/main.md` current truth와 불일치 0건이면 PASS; evidence = scoped `rg` 출력.
- [ ] AC3: fix 2의 검증·Low 처리·보고가 producer별로 닫힌다. feature-draft는 gate 2 finding이 인용한 평가조건을 final draft에서 재확인하고 evidence/잔존을 보고한다. implementation은 fix 2 diff에 커버리지 델타를 적용한 뒤 회귀 재실행과 AC→증거 갱신을 수행한다. 두 producer 모두 gate 2 Low에 자기 gate 1의 기존 정책을 동일 적용하고, gate 2 경로의 최종 보고에서 호출 1/2의 severity·fix·검증을 구분한다. 평가: 각 producer의 fix 2 블록에서 검증 순서·Low 동일성·호출별 보고·잔존 보고를 인용한 이진 rubric의 누락 0건이면 PASS.
- [ ] AC4: 기존 과다-finding advisory-only 문구가 네 producer 파일에서 0건이고, gate 2를 producer가 자체 실행한다. 평가: `rg -n '추가 실행을 권장|권고 출력만|실행 여부는 사용자 판단|advisory-only'`를 네 파일에 실행한 출력이 비어 있으면 PASS.
- [ ] AC5: 호출자 ownership과 reviewer 경계가 보존된다. `sdd-autopilot`·사용자는 gate/fix를 별도 실행하지 않으며, `plan-review`·`implementation-review`와 reviewer agent는 변경되지 않는다. 평가: producer final contract 인용 + `git diff --exit-code main -- .claude/skills/plan-review .codex/skills/plan-review .claude/skills/implementation-review .codex/skills/implementation-review .claude/agents/plan-review-agent.md .codex/agents/plan-review-agent.toml .claude/agents/implementation-review-agent.md .codex/agents/implementation-review-agent.toml .claude/agents/simplicity-review-agent.md .codex/agents/simplicity-review-agent.toml`가 exit 0이면 PASS.
- [ ] AC6: Claude/Codex producer 미러가 byte-identical이다. 평가: `diff -u .claude/skills/feature-draft/SKILL.md .codex/skills/feature-draft/SKILL.md`와 implementation 짝 diff가 모두 출력 없이 exit 0이면 PASS.

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md` -- plan-review gate의 조건부 두 번째 호출·fix 2·표적 검증 계약
- [M] `.codex/skills/feature-draft/SKILL.md` -- Claude producer와 byte-identical mirror
- [M] `.claude/skills/implementation/SKILL.md` -- implementation-review gate의 조건부 두 번째 호출·fix 2 hygiene·마감 보고
- [M] `.codex/skills/implementation/SKILL.md` -- Claude producer와 byte-identical mirror

### Task 2: 한·영 workflow 문서를 bounded retry semantics로 정렬
한·영 사용자 문서를 새 gate 횟수와 ownership에 맞춘다.

**Contracts**: 기본 경로는 gate 1회+fix 1회, 과다 finding 경로만 gate 2회+fix 2회다. autopilot은 두 경로 모두 gate를 직접 호출하거나 fix하지 않는다. reviewer는 각 호출마다 single-pass다.

**Acceptance Criteria**:
- [ ] AC7: `docs/SDD_WORKFLOW.md`와 영문 미러의 체인 도식이 `기본 1회, 임계값 도달 시 최대 2회` 의미를 표현하고, 한·영의 단계·상한·ownership 의미가 일치한다. 평가: 두 파일의 chain 블록과 설명을 나란히 인용한 semantic rubric에서 누락/모순 0건이면 PASS.
- [ ] AC8: `docs/AUTOPILOT_GUIDE.md`와 영문 미러가 producer-owned conditional second pass, no third pass, autopilot no-recall/no-fix, 두 호출 결과의 최종 보고를 설명하고 고정 `~1분`·`loop 없음`·`single fix로 안 닫힌 finding은 그대로 최종 보고` 문면을 제거한다. 평가: 네 개념의 positive anchor 존재 + stale anchor scoped `rg` 0건이면 PASS.
- [ ] AC9: AUTOPILOT_GUIDE 한·영 버전·날짜가 같은 새 값으로 정렬되고 관련 스킬 절의 `plan-review`·`implementation-review` 설명도 조건부 최대 2회와 모순되지 않는다. 평가: metadata와 관련 스킬 행 대조에서 차이 0건이면 PASS.

**Target Files**:
- [M] `docs/SDD_WORKFLOW.md` -- 한국어 workflow gate 상한 설명
- [M] `docs/en/SDD_WORKFLOW.md` -- 영문 semantic mirror
- [M] `docs/AUTOPILOT_GUIDE.md` -- 한국어 autopilot gate/보고/비용 설명
- [M] `docs/en/AUTOPILOT_GUIDE.md` -- 영문 semantic mirror

### Task 3: Bounded retry 전파와 잔존 문구를 전수 검증
작성 표면을 모두 닫은 뒤 scope 밖 reviewer를 건드리지 않았고, 변경 대상에 advisory-only 계약이 남지 않았는지 read-only census로 확인한다.

**Acceptance Criteria**:
- [ ] AC10: P1·P2의 required surface 8파일이 모두 변경되고 그 밖의 `.claude/skills`·`.codex/skills`·`docs/` 파일 변경은 0건이다. 평가: `git diff --name-only main -- .claude/skills .codex/skills docs` 출력 집합이 P1+P2 exact 8파일이면 PASS.
- [ ] AC11: required surface 8파일에서 producer 전체가 gate/fix를 총 1회만 수행한다고 뜻하는 stale contract가 0건이다. 평가: `rg -n -i 'finding이 많았으니|추가 실행을 권장|권고 출력만|실행 여부는 사용자 판단|advisory-only|review loop는 돌리지|재리뷰 없음|내부에서 1회 수행하고 fix도 1회|스킬 1회로.*점검|fix 1회로|게이트 \+ fix 1회|There are no review-fix loops|single fix|one fix' <8 files>` 출력이 비어 있고, 별도 rubric이 남은 `단일 패스/single pass` 표현을 호출당 reviewer 속성으로만 해석할 수 있음을 확인하면 PASS.
- [ ] AC12: positive contract가 두 runtime producer와 한·영 문서에 모두 존재한다. 평가: 파일별로 `임계값/threshold`, `두 번째/second`, `최대 2/max(imum) 2`, `세 번째 없음/no third`, `producer/autopilot ownership` 의미 anchor를 검사해 8/8 파일 PASS를 출력한다.
- [ ] AC13: Part 1의 global spec handoff 표면이 후속 `spec-sync` 입력으로 명시되고 Part 2 Target Files에는 `_sdd/spec/`가 없다. 평가: draft marker 내부에 `main.md`·`components.md`·`usage-guide.md`·decision log·changelog가 열거되고 `rg -n '^\- \[[MCD]\] `_sdd/spec/'` 출력이 비어 있으면 PASS.
- [ ] AC14: `git diff --check`가 출력 없이 exit 0이다.

**Target Files**:
- 없음 (read-only 검증)
