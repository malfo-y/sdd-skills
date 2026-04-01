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
- `investigate`
- `spec_update_todo`
- `spec_update_done`
- `spec_review`
- `ralph_loop_init`

## Inline Writing

장문 산출물은 별도 writing helper agent에 넘기지 않는다. caller가 같은 흐름에서 skeleton -> fill -> finalize를 수행하고, 필요할 때만 `default` 또는 `worker`를 bounded helper로 사용한다.

- `feature_draft`
- `implementation_plan`
- `implementation_review`
- `spec_review`

## Invocation Contract

Codex custom agent 문서는 **실제 Codex tool contract**를 기준으로 작성한다.

- sub-agent fan-out은 `spawn_agent(...)`로 시작한다.
- spawned agent 결과 수집은 반드시 `wait_agent(...)`로 명시한다.
- 중간 보완 지시가 필요할 때만 `send_input(...)`을 사용한다.
- 여러 agent 결과를 합칠 때는 `spawn -> wait -> verify -> integrate` 순서를 명시한다.
- 읽기 전용 병렬화는 `multi_tool_use.parallel` 또는 read-only explorer fan-out으로 표현한다.

다음 표현은 더 이상 권장하지 않는다:

- `Agent(...)`
- `Task(...)`
- `subagent_type="general-purpose"`

대신 아래처럼 Codex-native 역할을 사용한다:

- `spawn_agent(agent_type="explorer")` for read-only investigation
- `spawn_agent(agent_type="worker")` for bounded implementation / translation / execution tasks
- `spawn_agent(agent_type="default")` for bounded sequential drafting or fill assistance when the caller keeps ownership

## Ownership Rules for Fan-out

병렬로 여러 agent를 띄울 때는 각 agent의 책임 경계를 명시한다.

- 각 worker/explorer는 **서로 겹치지 않는 파일/모듈/질문 범위**를 가진다.
- write 작업이 있는 경우 소유 파일 목록을 프롬프트에 명시한다.
- merge는 부모 agent가 수행하고, spawned agent끼리 서로의 출력을 직접 가정하지 않는다.
- spawned agent가 불완전한 결과를 내면 부모가 `wait_agent` 이후 재시도 또는 순차 fallback을 결정한다.
