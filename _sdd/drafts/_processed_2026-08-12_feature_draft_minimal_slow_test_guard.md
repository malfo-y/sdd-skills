# Feature Draft: Minimal Slow Test Guard

> 규모 판정: 적격 — 세 규칙을 테스트 실행 주체의 Claude/Codex 미러에 동일하게 반영하는 단일 task다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
테스트 반복 비용을 제한하기 위해 다음 세 실행 규칙을 추가한다.

- 표적 test/check는 30초가 지나면 중단한다.
- Timeout 후에는 test target, fixture, 또는 관련 구현이 바뀌기 전까지 같은 명령을 다시 실행하지 않는다.
- 느리다고 알려진 test는 repo 또는 사용자가 명시한 checkpoint에서만 실행한다.

## Scope
- **In**: implementation, implementation-review, pr-review의 테스트 실행 지침과 Claude/Codex 미러
- **Out**: TDD/리뷰 gate 밖의 skill, timeout 도구·설정 schema·fixture API·manifest·checker·CI 변경
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | Slow test guard 3 rules | `.claude/skills/implementation/SKILL.md`, `.codex/skills/implementation/SKILL.md`, `.claude/agents/implementation-review-agent.md`, `.codex/agents/implementation-review-agent.toml`, `.claude/agents/pr-review-agent.md`, `.codex/agents/pr-review-agent.toml` | `rg -l 'Fresh Verification|## 마감' <six exact paths>` → the same six paths | Task 1 |

# Part 2: Tasks

### Task 1: Add the three slow-test execution rules
실제로 테스트를 실행하는 세 역할과 각 미러에 같은 의미의 세 줄만 추가한다.

**Contracts**: 표적 test/check는 30초가 지나면 중단한다. Timeout 후에는 test target, fixture, 또는 관련 구현이 바뀌기 전까지 같은 명령을 다시 실행하지 않는다. 느리다고 알려진 test는 repo 또는 사용자가 명시한 checkpoint에서만 실행한다.

**Acceptance Criteria**:
- [ ] AC1: 변경 전 여섯 exact target에서 `rg -l '표적 test/check는 30초가 지나면 중단한다'` 결과가 0개다(RED).
- [ ] AC2: 변경 후 세 contract 문장 각각의 `rg -l` 결과가 정확히 같은 여섯 target이다(GREEN).
- [ ] AC3: 세 mirror pair가 동일한 contract 문장 세 개를 포함하고, diff에는 그 외 실행 장치가 없으며, `git diff --check`가 통과한다(`rg -n` + diff review + command output).

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- implementation 실행 규칙
- [M] `.codex/skills/implementation/SKILL.md` -- Codex mirror
- [M] `.claude/agents/implementation-review-agent.md` -- implementation review 실행 규칙
- [M] `.codex/agents/implementation-review-agent.toml` -- Codex mirror
- [M] `.claude/agents/pr-review-agent.md` -- PR review 실행 규칙
- [M] `.codex/agents/pr-review-agent.toml` -- Codex mirror

# Open Questions
관련 변경은 해당 test target·fixture·관련 구현의 변경으로 한정하고, checkpoint는 repo 또는 사용자가 명시한 것만 인정한다. `investigate`는 TDD 구현/리뷰 gate 밖이므로 제외한다. 모두 사용자 요청에서 닫힌 결정이며 추가 확인은 필요 없다.
