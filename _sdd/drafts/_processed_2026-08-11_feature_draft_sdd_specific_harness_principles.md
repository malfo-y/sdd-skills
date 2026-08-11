# Feature Draft: SDD 전용 하네스 작업 원칙

> 규모 판정: 적격 — §0 계약 하나를 하네스 5개 표면에 동일 전파하는 변경이며 전수 surface가 눈검산 가능하다. rename/전파 잔존은 마지막 read-only census task로 닫는다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
`AGENTS.md` §0을 일반 agent 작업 원칙에서 SDD 고유 실패 방지 불변식으로 교체한다. 새 contract는 세 가지다: repo-wide truth와 change-specific execution detail을 lifetime으로 분리하고, goal·AC evidence가 있는 outcome만 current truth로 승격하며, 다음 단계·세션 재개에 필요한 결정과 evidence만 artifact로 보존한다.

## Scope
- **In**: `AGENTS.md`와 spec-create/spec-upgrade의 Claude·Codex harness template 4벌에서 §0 일반 원칙·일반 보조 문면을 제거하고 합의한 SDD 3원칙을 exact wording으로 배포
- **Out**: `plan-review` reviewer-local rubric, §1~§5 workflow/검증/work-log 계약, `docs/agentic_coding_principle.md` 파일 자체, 과거 draft·implementation·decision/changelog 이력
<!-- spec-update-todo-input-end -->

# Propagation Surfaces
| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | §0 일반 원칙 4개 + 상세 포인터 + 일반 보조 2개를 SDD 전용 3원칙으로 교체 | `AGENTS.md`; `.claude/skills/{spec-create,spec-upgrade}/references/agents-harness-template.md`; `.codex/skills/{spec-create,spec-upgrade}/references/agents-harness-template.md` | `rg -n -uu -e 'Think Before Coding' -e 'Simplicity First' -e 'Surgical Changes' -e 'Goal-Driven Execution' -e '원칙별 자기점검 질문' -e '무인 실행' -e '더 나은 방법' AGENTS.md .claude/skills/{spec-create,spec-upgrade}/references/agents-harness-template.md .codex/skills/{spec-create,spec-upgrade}/references/agents-harness-template.md`는 현재 각 원칙 5건·포인터 1건·보조 문면 각 5건이며, 새 3원칙은 0건. 변경 후 구 문면 0건·새 원칙별 5건 | Task 1 |

# Part 2: Tasks

### Task 1: 하네스 §0을 SDD 전용 3원칙으로 교체
토론에서 확정한 실패 방지 불변식만 §0에 남기고, 일반 agent 원칙과 그 해설 포인터·보조 문면은 제거한다.

**Contracts**: §0의 원칙 목록은 아래 exact wording 3개만 갖는다.

- **Separate Truth by Lifetime**: Keep repo-wide decisions in the global spec and change-specific execution detail in temporary artifacts.
- **Evidence Before Promotion**: Promote outcomes to current truth only after goals and acceptance criteria are verified; otherwise keep them planned or unverified.
- **Persist Handoffs, Not Process**: Record only the decisions and evidence needed by the next stage or a resumed session, not reproducible process narration.

**Acceptance Criteria**:
- [ ] AC1: 다섯 live harness surface에서 새 원칙 이름 `Separate Truth by Lifetime`·`Evidence Before Promotion`·`Persist Handoffs, Not Process`가 각각 정확히 5건이고, 각 이름의 설명은 위 Contracts 문장과 exact match한다.
- [ ] AC2: 같은 다섯 surface에서 `Think Before Coding|Simplicity First|Surgical Changes|Goal-Driven Execution|원칙별 자기점검 질문|무인 실행|더 나은 방법` census가 0건이다.
- [ ] AC3: 네 `agents-harness-template.md`의 SHA-256이 1종이며, `git diff --unified=0`에서 다섯 target의 변경 hunk가 §0과 §1 사이에만 존재한다.

**Target Files**:
- [M] `AGENTS.md` -- repo instance §0 교체
- [M] `.claude/skills/spec-create/references/agents-harness-template.md` -- Claude 생성 template §0 교체
- [M] `.claude/skills/spec-upgrade/references/agents-harness-template.md` -- Claude upgrade template §0 교체
- [M] `.codex/skills/spec-create/references/agents-harness-template.md` -- Codex 생성 template §0 교체
- [M] `.codex/skills/spec-upgrade/references/agents-harness-template.md` -- Codex upgrade template §0 교체

### Task 2: 구 원칙과 전파 잔존을 census로 검증
과거 이력과 일반 원칙 참고 문서는 보존하되, live harness에서만 구 §0 문면이 사라지고 새 contract가 전수 배포됐는지 확인한다.

**Acceptance Criteria**:
- [ ] AC1: Task 1의 exact census·template hash·§0 hunk 범위 검사를 fresh 실행해 모두 통과하고, `docs/agentic_coding_principle.md` diff가 0이며, 두 `plan-review` agent의 reviewer-local 6-smell rubric parity와 기존 `KISS/YAGNI/DRY/Scope Discipline/Verifiability` 매핑이 유지되고, `git diff --check`가 무출력이다.

**Target Files**:
- 없음 (read-only 검증)
