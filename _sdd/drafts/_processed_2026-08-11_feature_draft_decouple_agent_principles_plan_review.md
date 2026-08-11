# Feature Draft: AGENTS 작업 원칙과 plan-review 분리

> 규모 판정: 적격 — 결합 문면의 live surface가 하네스 5곳·reviewer 2곳·global spec 1곳으로 전수 열거 가능하며, census형 sweep은 마지막 read-only task로 닫는다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
`AGENTS.md` §0의 네 작업 원칙은 repo 작업 규범으로만 유지하고 `plan-review` finding 분류 어휘와의 이름 결합을 제거한다. `plan-review`는 자체 rubric(KISS/YAGNI/DRY/scope discipline/verifiability)을 독립적으로 소유하며, global spec은 두 계약 사이의 이름 불변식을 더 이상 선언하지 않는다.

## Scope
- **In**: 하네스 인스턴스·배포 템플릿의 결합 설명 제거, plan-review rubric의 repo 작업 원칙 이름 제거, global spec의 이름 결합 결정 supersede, live surface census 검증
- **Out**: §0 네 원칙 자체의 삭제·개명·의미 변경, `Principle Link` 반환 필드 삭제, 과거 draft·implementation·decision/changelog 이력 재작성
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | 하네스가 plan-review `Principle Link`의 이름 앵커라는 결합 제거 | `AGENTS.md`; `.claude/skills/{spec-create,spec-upgrade}/references/agents-harness-template.md`; `.codex/skills/{spec-create,spec-upgrade}/references/agents-harness-template.md` | `rg -n -uu '네 원칙은 리뷰 단계|이름을 바꾸면.*인용' AGENTS.md .claude/skills .codex/skills` 결과가 현재 5개 surface이며 변경 후 0 | Task 1 |
| P2 | plan-review rubric을 하네스 원칙 이름에서 독립된 reviewer-local 근거로 교체 | `.claude/agents/plan-review-agent.md`; `.codex/agents/plan-review-agent.toml` | `rg -n 'Think Before Coding|Simplicity First|Surgical Changes|Goal-Driven Execution' .claude/agents/plan-review-agent.md .codex/agents/plan-review-agent.toml`이 현재 rubric 이름을 반환하며 변경 후 0 | Task 1 |

# Part 2: Tasks

### Task 1: 작업 원칙과 reviewer 분류 어휘의 결합 제거
§0 네 원칙은 그대로 두되, 하네스 설명과 plan-review rubric에서 서로를 이름으로 참조하는 계약만 최소 변경한다. global spec current truth와 append-only 기록은 구현 검증 후 `spec-sync`가 갱신한다.

reviewer-local 목표 매핑은 `Scope Creep → YAGNI, KISS, Scope Discipline`; `New File Justification → KISS, Scope Discipline`; `Single-use Abstraction → KISS, YAGNI`; `Task Boundary Drift → Scope Discipline`; `DRY Risk → DRY, KISS`; `Verification Weakness → Verifiability`로 고정한다. 이는 기존 smell 의미를 일반 용어로 옮기는 변경이라 사용자 확인이 불필요하며 확신도는 높음이다.

**Acceptance Criteria**:
- [ ] AC1: `rg -n -uu '네 원칙은 리뷰 단계|이름을 바꾸면.*인용' AGENTS.md .claude/skills .codex/skills`가 0건이고, `AGENTS.md`에는 네 원칙과 `docs/agentic_coding_principle.md` 포인터가 그대로 남는다.
- [ ] AC2: `rg -n 'Think Before Coding|Simplicity First|Surgical Changes|Goal-Driven Execution' .claude/agents/plan-review-agent.md .codex/agents/plan-review-agent.toml`이 0건이고, 두 agent의 6-smell 표가 위 reviewer-local 목표 매핑과 정확히 일치한다.
- [ ] AC3: 네 harness template의 SHA-256이 1종이고, Claude/Codex plan-review agent의 대응 rubric 행이 동일하다.

**Target Files**:
- [M] `AGENTS.md` -- §0의 plan-review 결합 문장만 제거하고 상세 원칙 포인터 보존
- [M] `.claude/skills/spec-create/references/agents-harness-template.md` -- 배포 템플릿 결합 문장 제거
- [M] `.claude/skills/spec-upgrade/references/agents-harness-template.md` -- 배포 템플릿 결합 문장 제거
- [M] `.codex/skills/spec-create/references/agents-harness-template.md` -- 배포 템플릿 결합 문장 제거
- [M] `.codex/skills/spec-upgrade/references/agents-harness-template.md` -- 배포 템플릿 결합 문장 제거
- [M] `.claude/agents/plan-review-agent.md` -- rubric을 reviewer-local 분류 어휘로 변경
- [M] `.codex/agents/plan-review-agent.toml` -- Codex mirror rubric 변경

### Task 2: 전파 잔존을 census로 검증
과거 이력은 보존한 채 live 계약 표면에서 구 결합 문면과 reviewer의 하네스 원칙 이름이 남지 않았음을 전수 확인한다.

**Acceptance Criteria**:
- [ ] AC1: P1·P2의 exact query가 각각 0건이고, `git status --short _sdd/drafts _sdd/implementation`에서 이번 draft·ledger 외 과거 파일이 0건이다. global spec current truth와 append-only 기록은 Part 1 delta를 소비하는 후속 `spec-sync` 단계가 검증한다.

**Target Files**:
- 없음 (read-only 검증)
