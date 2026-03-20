---
name: write-phased
description: 'This skill should be used when the user asks to "write-phased", "문서 작성", "작성해줘", "만들어줘", "코드 작성", "파일 생성", "구현해줘", "write a document", "create a file", "generate code", "implement", or any request to produce a markdown document, code file, config file, or technical writing. Orchestrates skeleton-first writing: spawns write_skeleton for structure, then fills sections.'
version: 2.1.0
---

# write-phased — Skeleton + Fill Orchestration

`write_skeleton` agent로 파일을 생성하고, SKELETON_ONLY이면 직접 섹션을 채운다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: 요청된 파일이 완성된 상태로 저장되어 있다
- [ ] AC2: TODO/Phase 마커가 남아있지 않다
- [ ] AC3: 사용자 요청 언어를 따랐다

## Hard Rules

1. 다른 skill을 중첩 호출하지 않는다. skeleton 생성은 `write_skeleton` agent만 사용한다.
2. fill 책임은 이 skill에 있다. `SKELETON_ONLY`이면 `default` 또는 `worker` agent를 사용해 남은 섹션을 채운다.
3. `spawn_agent(...)` 결과는 항상 `wait_agent(ids=[...])`로 수집한다.
4. 독립 섹션이 아니면 병렬화하지 않는다.

## Process

### Step 1: Skeleton 생성

`write_skeleton` agent를 spawn한다:

```
writer_id = spawn_agent(agent_type="write_skeleton", message="[사용자 요청 전문]")
wait_agent(ids=[writer_id])
```

### Step 2: 반환값 분기

**COMPLETE인 경우**: 파일이 이미 완성됨. Step 4로 건너뛴다.

**SKELETON_ONLY인 경우**: 반환된 `Sections Remaining` 목록을 확인하고 Step 3으로 진행한다.

### Step 3: Fill (SKELETON_ONLY일 때만)

반환된 미완성 섹션 목록을 보고 채운다:

- **의존 섹션** 또는 작은 단일 파일: `spawn_agent(agent_type="default", message="...")`로 순차 fill
- **독립 섹션** 2개 이상: 섹션별 또는 파일별로 `spawn_agent(agent_type="worker", message="...")`를 병렬 호출
- **다중 파일**: 공통 의존성이 큰 파일을 먼저 채우고, 겹치지 않는 파일만 병렬 fill

fill agent에 전달할 최소 정보:

- 대상 파일 경로
- `Sections Remaining` 목록
- 유지해야 할 기존 skeleton 구조
- 언어/톤/출력 형식
- TODO 마커를 실제 내용으로 치환하라는 지시

### Step 4: 마커 정리 및 완료

- 파일에 남은 `<!-- TODO -->`, `# TODO:`, `<!-- Phase 2 -->` 등 모든 마커를 제거한다.
- 다중 파일이면 파일 간 이름, import, 참조 관계를 교차 검증한다.
- 완료 결과를 사용자에게 보고한다.

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
