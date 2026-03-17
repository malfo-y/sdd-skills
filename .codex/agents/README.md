# Codex Custom Agents

이 디렉토리는 Codex `sdd-autopilot`과 generated orchestrator가 직접 spawn하는 custom agent 정의를 담는다.

## Naming

- 파일명은 skill 대응 관계가 바로 보이도록 `kebab-case`를 사용한다.
- `name` 필드는 spawn 안정성을 위해 `snake_case`를 사용한다.
- wrapper skill은 `.codex/skills/<skill-name>/`에 남고, 실행 backbone은 여기의 custom agent가 맡는다.

## Ownership

- wrapper skill: 사용자 직접 호출 진입점 + handoff contract
- custom agent: 상세 workflow 본문 + spawned execution unit
- generated orchestrator: custom agents만 직접 spawn

즉, `.codex/skills/<skill-name>/SKILL.md`는 얇은 wrapper이고, 실제 동작 보장은 `.codex/agents/*.toml`의 `developer_instructions`가 담당한다.

## Agent Set

- `feature_draft`
- `implementation_plan`
- `implementation`
- `implementation_review`
- `spec_update_todo`
- `spec_update_done`
- `spec_review`
- `ralph_loop_init`
- `write_phased`

## Nested Writing

장문 산출물이 핵심인 아래 agent는 필요 시 `write_phased`를 nested spawn한다.

- `feature_draft`
- `implementation_plan`
- `implementation_review`
- `spec_review`

이 구조를 사용하려면 `.codex/config.toml`의 `agents.max_depth`가 최소 2여야 한다.
