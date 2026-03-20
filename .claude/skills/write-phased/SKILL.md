---
name: write-phased
description: Use this skill when the user asks to write, create, or generate a document or code file. Triggers on "write-phased", "문서 작성", "작성해줘", "만들어줘", "코드 작성", "파일 생성", "구현해줘", "write a document", "create a file", "generate code", "implement", or any request to produce a markdown document, code file, config file, or technical writing.
version: 2.0.0
---

# write-phased — Skeleton + Fill Orchestration

`sdd-skills:write-skeleton` agent로 파일을 생성하고, 필요하면 직접 Edit으로 내용을 채운다. 모든 중간 과정이 메인 대화에서 실행되어 사용자에게 보인다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: 요청된 파일이 완성된 상태로 저장되어 있다
- [ ] AC2: TODO/Phase 마커가 남아있지 않다
- [ ] AC3: 사용자 요청 언어를 따랐다

## Process

### Step 1: Skeleton 생성

`sdd-skills:write-skeleton` agent를 호출하여 파일을 생성한다:

```
result = Agent(subagent_type="sdd-skills:write-skeleton", prompt="[사용자 요청 전문]")
```

### Step 2: 반환값 분기

**COMPLETE인 경우**: 파일이 이미 완성됨. Step 4로 건너뛴다.

**SKELETON_ONLY인 경우**: 반환된 `Sections Remaining` 목록을 확인하고 Step 3으로 진행한다.

### Step 3: Fill (SKELETON_ONLY일 때만)

반환된 미완성 섹션 목록을 보고 Edit으로 채운다:

- **의존 섹션** (앞 섹션 내용에 의존): 순서대로 Edit
- **독립 섹션** 2개 이상: 병렬 Agent dispatch 가능
- **다중 파일**: 파일별 독립 fill 가능

각 섹션의 TODO 마커를 찾아 Edit으로 교체한다:
```
Edit(old_string="<!-- TODO: ... -->", new_string="[실제 내용]")
```

### Step 4: 마커 정리 및 완료

- 파일에 남은 `<!-- TODO -->`, `# TODO:`, `<!-- Phase 2 -->` 등 모든 마커를 제거한다.
- 완료 결과를 사용자에게 보고한다.

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
