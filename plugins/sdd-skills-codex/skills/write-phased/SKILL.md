---
name: write-phased
description: 'This skill should be used when the user asks to "write-phased", "문서 작성", "작성해줘", "만들어줘", "코드 작성", "파일 생성", "구현해줘", "write a document", "create a file", "generate code", "implement", or any request to produce a markdown document, code file, config file, or technical writing. The caller writes the skeleton inline first, then fills and finalizes in the same flow.'
---

# write-phased — Inline 2-Phase Writing

별도 writing helper agent를 spawn하지 않는다. 호출자가 현재 콘텍스트에서 먼저 skeleton/outline/TODO marker를 파일에 기록하고, 같은 흐름에서 내용을 채우고 finalize한다.

## Codex Runtime Adapter

이 스킬은 기본적으로 helper agent 없이 인라인 작성한다. 런타임이 skill-internal helper dispatch를 허용하고 독립 섹션 때문에 bounded helper가 필요할 때만 `default` / `worker` helper를 사용할 수 있다. 현재 런타임 정책이 명시적 sub-agent 허가를 추가로 요구하면, dispatch 전에 사용자에게 위임 허가를 요청한다.

helper dispatch 전 active tool schema에서 lifecycle contract 하나를 선택한다. Mailbox(Desktop/current CLI: `task_name`/`fork_turns`가 필요하거나 wait에 `targets` 없음)는 invocation마다 짧은 lowercase `run_id`를 만들고 같은 parent tree의 재실행까지 고유한 `task_name`에 넣은 뒤, `fork_turns: "none"`, `message`로 spawn한다. target 없는 wait를 반복하며 완료 agent를 닫지 않는다. Target/close(legacy CLI schema: wait에 `targets` 지원 + `close_agent` 노출)는 `message` spawn, target wait, 완료 handle close를 사용한다. `agent_type`은 선택적 role selector다 — active schema가 `"worker"` 값을 지원할 때만 spawn payload에 추가하고, 없으면 섹션 책임·쓰기 집합·skeleton 계약을 `message`에 직접 넣어 일반 sub-agent를 사용한다. 실행 surface 이름이 아니라 schema로 lifecycle을 선택한다. lifecycle contract가 불완전하거나 모호하면 helper를 쓰지 않고 인라인 작성한다. `agent_type` 부재만으로는 인라인 fallback하지 않으며, 없는 lifecycle tool을 `tool_search`로 찾거나 두 contract를 혼용하지 않는다.

실제 Codex 호출은 `prompt`가 아니라 `message`를 사용한다:

```text
Mailbox: spawn_agent({task_name: "write_phased_r7f3a_api_section", fork_turns: "none", message: "<대상 파일 + 섹션 책임 + 쓰기 집합 + 유지할 skeleton>"})  // r7f3a는 invocation마다 교체
Mailbox: wait_agent({timeout_ms: 600000})  // final까지 반복, close 없음
Target/close: spawn_agent({message: "<대상 파일 + 섹션 책임 + 쓰기 집합 + 유지할 skeleton>"})
Target/close: wait_agent({targets: ["<agent_id>"], timeout_ms: 600000}) → final 기록 → close_agent({target: "<완료 agent_id>"})
```

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: 요청된 파일이 완성된 상태로 저장되어 있다
- [ ] AC2: TODO/Phase 마커가 남아있지 않다
- [ ] AC3: 사용자 요청 언어를 따랐다
- [ ] AC4: skeleton 작성과 fill이 같은 호출 흐름 안에서 수행되었다

## Hard Rules

1. skeleton 생성과 fill은 같은 호출 흐름에서 수행한다. helper agent로 skeleton ownership을 넘기지 않는다.
2. 긴 문서일수록 먼저 outline/heading/placeholder를 저장한 뒤 내용을 채운다.
3. bounded helper를 쓰더라도 caller가 skeleton 구조와 최종 통합 책임을 유지한다.
4. 독립 섹션이 아니면 병렬화하지 않는다.

## Process

### Step 1: Skeleton 작성

대상 파일에 skeleton/outline을 직접 기록한다. 최소한 다음 중 필요한 것을 먼저 만든다.

- 문서 제목
- 주요 섹션 헤더
- 빈 목록/표 골격
- `TODO`, `TBD`, `<!-- TODO -->` 같은 placeholder

### Step 2: Fill

같은 호출 흐름에서 skeleton의 각 섹션을 채운다.

- **의존 섹션** 또는 작은 단일 파일: caller가 순서대로 채운다
- **독립 섹션** 2개 이상: 필요 시 `default` 또는 `worker` agent를 bounded helper로 사용할 수 있다
- **다중 파일**: 공통 의존성이 큰 파일을 먼저 채우고, 겹치지 않는 파일만 병렬 fill

helper를 쓰는 경우에도 최소한 아래를 넘긴다.

- 대상 파일 경로
- 채워야 할 섹션 또는 책임 범위
- 유지해야 할 skeleton 구조
- helper agent를 spawn했다면 위 Runtime Adapter가 final status를 반환한 뒤에만 결과를 반영한다. timeout은 완료로 간주하지 않는다.
- 언어/톤/출력 형식
- placeholder를 실제 내용으로 치환하라는 지시

### Step 3: Finalize

- 파일에 남은 `<!-- TODO -->`, `# TODO:`, `<!-- Phase 2 -->` 등 모든 마커를 제거한다.
- 다중 파일이면 파일 간 이름, import, 참조 관계를 교차 검증한다.
- 완료 결과를 사용자에게 보고한다.

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
