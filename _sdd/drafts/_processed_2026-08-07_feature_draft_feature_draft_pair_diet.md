# Feature Draft: feature-draft producer and plan-review verifier diet

> 규모 판정: 적격 — producer 2면, verifier 2면, read-only wrapper 2면이 세 owner task로 닫히며 변경 요소와 task 대응을 눈검산할 수 있다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
P0 4/5 `feature-draft-pair-diet`를 구현한다. `feature-draft`는 Propagation Surfaces 계약과 inline output template의 canonical home을 유지하고, 작성 단계가 template 코드블록을 verbatim 복사하게 한다. template은 매 실행 소비되므로 별도 reference로 분리하지 않는다. 질문 단계에는 답이 아키텍처·범위를 바꾸는 unknown을 한 번에 하나씩 우선 확인하는 기준을 추가하고, AC에는 재현 가능한 check와 명시 rubric을 모두 허용하는 평가방법 2등급을 형식화한다. `plan-review-agent`는 Propagation·평가방법 계약을 복제하지 않고 producer 계약을 읽어 검증하며, minimum-code recommendation은 evidence-backed 최소 변경 기준 한 곳으로 합친다.

새 contract: feature draft `Required Output`의 inline fenced template이 output structure의 단일 소스다. draft 작성 단계는 이를 출발 skeleton으로 verbatim 복사해 heading·marker·field order를 보존하고, placeholder 치환과 필요한 Propagation row·task block·AC·Target File row 반복을 허용한다. 조건부 `Propagation Surfaces`·`Open Questions` 섹션만 producer 규칙에 따라 제거할 수 있다.

## Scope
- **In**: Claude/Codex `feature-draft` SKILL, Claude/Codex `plan-review-agent`, Claude/Codex `plan-review` wrapper의 규범 감사와 runtime parity 검증
- **Out**: rolling split·census·single-pass plan gate·6-smell/severity/return 계약 변경, 새 reviewer/dispatch topology, `discussion`, 실제 feature draft forward-test 산출물 생성
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | inline output template verbatim 소비 | `.claude/skills/feature-draft/SKILL.md`<br>`.codex/skills/feature-draft/SKILL.md` | `rg -l '^## Required Output$' .claude/skills/feature-draft/SKILL.md .codex/skills/feature-draft/SKILL.md` 및 `rg -l '^# Feature Draft: \[title\]$' .claude/skills/feature-draft/SKILL.md .codex/skills/feature-draft/SKILL.md` → 각각 정확히 같은 두 SKILL | Task 1 |
| P2 | 질문 우선순위·평가방법 2등급·minimum-code 기준 | `.claude/skills/feature-draft/SKILL.md`<br>`.codex/skills/feature-draft/SKILL.md` | `rg -l '^## Process$' .claude/skills/feature-draft/SKILL.md .codex/skills/feature-draft/SKILL.md`, `rg -l 'AC가 핵심이다' .claude/skills/feature-draft/SKILL.md .codex/skills/feature-draft/SKILL.md`, `rg -l 'Minimum-Code Mandate' .claude/skills/feature-draft/SKILL.md .codex/skills/feature-draft/SKILL.md` → 각 query의 기대 집합은 두 SKILL | Task 1 |
| P3 | Propagation·평가방법 검증 pointer + recommendation 단일 홈 | `.claude/agents/plan-review-agent.md`<br>`.codex/agents/plan-review-agent.toml` | `rg -l 'Propagation Surface Coverage' .claude/agents/plan-review-agent.md .codex/agents/plan-review-agent.toml`, `rg -l 'Minimum-Code Recommendations' .claude/agents/plan-review-agent.md .codex/agents/plan-review-agent.toml`, `rg -l 'Evidence Required' .claude/agents/plan-review-agent.md .codex/agents/plan-review-agent.toml` → 각 query의 기대 집합은 두 agent (`평가방법`은 현행 0면인 gap) | Task 2 |
| P4 | thin plan-review entrypoint 감사 | `.claude/skills/plan-review/SKILL.md`<br>`.codex/skills/plan-review/SKILL.md` | `rg --files .claude/skills/plan-review .codex/skills/plan-review -g 'SKILL.md'` → wrapper 2면 | Task 3 |

# Part 2: Tasks

### Task 1: feature-draft producer의 template 소비와 판단 기준을 얇게 만든다
매번 쓰는 inline skeleton은 본문에 유지하되 기억으로 재구성하지 않도록 소비 방식을 기계화하고, 질문·평가·minimum-code 기준을 보강한다.

**Contracts**: `Required Output`의 fenced markdown이 output structure의 단일 소스다. 작성 단계는 이를 출발 skeleton으로 verbatim 복사해 heading·marker·field order를 보존하고, placeholder 치환과 필요한 Propagation row·task block·AC·Target File row 반복을 허용한다. producer가 명시한 조건부 섹션 두 개만 삭제 가능하다. AC 평가방법은 1등급(재현 가능한 test/check 출력) 또는 2등급(명시 rubric + reviewer 판정 + 인용 근거)이며, 둘 다 이진 판정·외부 증거·제3자 반박 가능성을 충족한다.

**Acceptance Criteria**:
- [ ] AC1: 두 SKILL의 `## Required Output` 아래 inline fenced template과 `# Feature Draft: [title]`·marker·task/AC/Target Files·Open Questions skeleton이 보존되고 byte-identical이다.
- [ ] AC2: 두 SKILL의 draft 작성 단계가 `Required Output` fenced template을 출발 skeleton으로 verbatim 복사하고 heading·marker·field order를 보존한다. placeholder 치환, 필요한 Propagation row·task block·AC·Target File row 반복, 조건부 두 section 삭제만 허용한다.
- [ ] AC3: 질문 단계는 locally discoverable하지 않고 답이 아키텍처·범위·Target Files를 바꾸는 unknown에만 발동하며, 한 번에 한 질문·영향이 큰 질문 우선이다. 무인 실행은 합리적 가정을 골라 `Open Questions`에 결정·근거를 기록한다.
- [ ] AC4: `AC가 핵심이다` 규칙이 1등급과 2등급의 필수 evidence 형태 및 공통 이진·외부증거·반박가능 기준을 한 곳에서 정의하고, template은 별도 Validation Plan/`V*` 구조를 신설하지 않는다.
- [ ] AC5: Minimum-Code는 요청 동작 또는 관측 위험에 직접 추적되는 최소 변경이라는 positive criterion 1곳으로 남고, 현행 negative inventory(`요청되지 않은 기능·옵션·설정 가능성`, `단일 사용처 추상화`, `발생할 수 없는 시나리오`)는 두 SKILL에서 0건이다.
- [ ] AC6: rolling split, census verification task, `spec-update-todo-input` marker, 조건부 Propagation 5열·single-owner·owner AC/Target Files 연접, single-pass plan-review gate와 fix/advisory 임계치의 보호 anchor가 보존된다.
- [ ] AC7: Claude/Codex SKILL이 exact match하며 두 skill folder가 system `skill-creator`의 `quick_validate.py`를 통과한다.

**Evaluation**:
- AC1·AC2·AC4·AC5·AC6·AC7은 1등급: section-aware token/count·byte diff·`quick_validate.py`의 재현 가능한 exit/output으로 이진 판정한다.
- AC3은 2등급: 작성 비참여 reviewer가 질문 발동·우선순위·무인 fallback 문장을 인용하고, locally discoverable하거나 결과 방향을 바꾸지 않는 질문까지 강제하는 반례를 지목하면 NOT MET다.
- AC4·AC5·AC6의 의미 보존은 2등급 보조: reviewer가 2등급 공통 기준·minimum-code 추적성·보호 gate 완화 사례를 diff 인용으로 하나라도 지목하면 NOT MET다.

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md` -- template 소비·질문·평가·minimum-code 기준
- [M] `.codex/skills/feature-draft/SKILL.md` -- 동형 producer 변경

### Task 2: plan-review-agent를 producer 계약의 verifier로 얇게 만든다
Propagation·평가방법의 상세 판단을 agent에서 재정의하지 않고 current producer source를 필요할 때 읽어 검증한다. recommendation guard는 evidence와 최소 변경의 한 기준으로 합친다.

**Contracts**: draft에 `Propagation Surfaces`가 있거나 AC 평가방법을 검증할 때 runtime의 current `feature-draft` producer rule을 읽는다. source를 읽을 수 없으면 계약을 기억으로 재구성하지 않고 `Verification Weakness=UNKNOWN`과 limitation을 반환한다.

**Acceptance Criteria**:
- [ ] AC8: 두 agent의 상세 Propagation 재정의(`필수 열`, `ID / Change element / Required surfaces / Discovery evidence / Owner task`, 발동·비발동·소유·연접 bullet inventory)는 0건이다. Hard Rules에는 producer 계약을 검증하고 위반을 `Verification Weakness`가 소유한다는 pointer만 1곳에 남는다.
- [ ] AC9: Step 3은 draft에 조건부 표가 있거나 평가방법 판정이 필요할 때 runtime의 current feature-draft producer rule을 Read하고, source 부재 시 `UNKNOWN`으로 닫는다. Step 2와 Verification Weakness rubric은 상세 열/등급을 재열거하지 않고 producer 계약 충족 여부만 묻는다.
- [ ] AC10: `Minimum-Code Recommendations`와 `Evidence Required` 두 규칙은 cited evidence를 해결하는 가장 작은 plan change라는 한 규칙으로 합쳐지고, 새 capability는 current requirement 또는 measured risk에 직접 추적될 때만 허용된다. `future-proof / extensible / configurable` 예시 목록은 0건이다.
- [ ] AC11: 보호 anchor `## Review Rubric: 6 Plan Smells`, `## Severity`, `## 호출자 렌즈 한정`, `## 규모 판정 검사`, `### Step 3: Read Supporting Context`, `### Step 6: Return`, `## Final Check`와 intro의 `최종 응답으로만 반환`이 양 agent에 각각 1건 존재한다. 작성 비참여 reviewer가 HEAD 대조에서 6 smell·severity·lens·규모·계단·return·read-only 의미 완화 사례를 하나라도 인용하면 NOT MET다.
- [ ] AC12: Claude frontmatter와 Codex TOML wrapper/`## Codex Agent Boundary` section, 양 runtime의 마지막 `Source Pointer` 줄을 제외하면 agent core가 exact match한다. Codex `developer_instructions`는 `tomllib`로 추출·parse하고 Source Pointer는 각 runtime wrapper/lifecycle anchor가 보존됐는지 별도 확인한다.

**Evaluation**:
- AC8·AC9·AC10·AC12는 1등급: section-scoped 잔존 count, producer-read/UNKNOWN token, 규칙 heading count, normalized core diff, TOML parse의 재현 가능한 output으로 판정한다.
- AC11은 1등급 anchor census + 위에 명시한 2등급 reviewer/HEAD diff rubric을 함께 충족해야 MET다.

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- canonical producer pointer·minimum-code guard 통합
- [M] `.codex/agents/plan-review-agent.toml` -- 같은 verifier 의미의 Codex 미러

### Task 3: thin wrapper와 전체 전파를 read-only 검증한다
현재 `plan-review` wrapper가 producer 판단 계약을 복제하지 않는 thin orchestrator인지 감사하고, P1–P4의 mirror/reference 전파와 잔존 중복을 전수 확인한다.

**Acceptance Criteria**:
- [ ] AC13: 두 plan-review wrapper는 2-lens single-pass dispatch·merge relay·runtime adapter만 소유하고 Propagation 5열, 평가방법 2등급, minimum-code 상세 판단을 0건 보유한다. agent source pointer와 runtime별 model/dispatch 계약은 보존돼 wrapper disposition이 `NO_CHANGE`로 닫힌다.
- [ ] AC14: pre-implementation baseline에서 여섯 implementation/audit target은 모두 clean이고, 기존 P0 1~3·spec·goal 변경은 별도 dirty로 기록한다. 구현 후 target-scoped `git diff --name-only` 집합은 feature-draft SKILL 2 + plan-review-agent 2이고 audited wrapper 2는 diff 0이다. feature 귀속 outside-target 변경은 0이다.
- [ ] AC15: inline template 보존, agent 상세 Propagation inventory·old minimum-code negative inventory 잔존 0, producer pointer·2등급 evaluation·interview 기준의 파일별 exact count, agent core parity, TOML parse, `quick_validate.py` 2면, `git diff --check`가 모두 PASS다.

**Evaluation**:
- AC13은 1등급 상세 판단 token 0/count + 2등급 wrapper 책임 rubric이다. reviewer가 두 wrapper에서 producer 판단의 재정의 또는 2-lens/runtime 계약 손실을 인용하면 NOT MET다.
- AC14·AC15는 1등급: 시작 `git status --short -- <6 target>` 빈 출력, target-scoped name set, section-aware residual/count, normalized diff, parse/validator/diff-check exit로 이진 판정한다.

**Target Files**:
- 없음 (read-only 감사·검증)

# Open Questions
- template은 매 draft 작성 때 항상 소비되므로 별도 reference로 분리하지 않고 inline canonical을 유지한다. verbatim base, 명시된 가변 row/block 반복, optional section 두 개의 제한적 삭제로 재구성 유실과 cardinality 모순을 함께 막는다 — `SKILL_AUTHORING_NORMS` §3.2/§5 및 implementation-review C1 반영, 사용자 확인 불필요(높은 확신).
- plan-review wrapper 두 면은 이미 얇은 entrypoint이고 P3 판단을 복제하지 않아 `NO_CHANGE`가 예상된다. plan-review 게이트가 반증하면 해당 finding만 현재 scope에서 반영한다 — 사용자 확인 불필요.
