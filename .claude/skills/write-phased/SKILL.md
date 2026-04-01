---
name: write-phased
description: Use this skill when the user asks to write, create, or generate a document or code file. Triggers on "write-phased", "문서 작성", "작성해줘", "만들어줘", "코드 작성", "파일 생성", "구현해줘", "write a document", "create a file", "generate code", "implement", or any request to produce a markdown document, code file, config file, or technical writing. The caller writes the skeleton inline first, then fills and finalizes in the same flow.
version: 3.0.0
---

# write-phased — Inline 2-Phase Writing

별도 writing helper agent를 호출하지 않는다. 호출자가 현재 콘텍스트에서 먼저 skeleton/outline/TODO marker를 파일에 기록하고, 같은 흐름에서 내용을 채우고 finalize한다. 모든 중간 과정이 메인 대화에서 실행되어 사용자에게 보인다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: 요청된 파일이 완성된 상태로 저장되어 있다
- [ ] AC2: TODO/Phase 마커가 남아있지 않다
- [ ] AC3: 사용자 요청 언어를 따랐다
- [ ] AC4: skeleton 작성과 fill이 같은 호출 흐름 안에서 수행되었다

## Process

### Step 1: Skeleton 작성

대상 파일에 skeleton/outline을 직접 기록한다. 최소한 다음 중 필요한 것을 먼저 만든다.

- 문서 제목
- 주요 섹션 헤더
- 빈 목록/표 골격
- `TODO`, `TBD`, `<!-- TODO -->` 같은 placeholder

긴 문서일수록 처음부터 완성본을 한 번에 쓰지 말고, 구조를 먼저 저장한다.

### Step 2: Fill

같은 호출 흐름에서 skeleton의 각 섹션을 채운다.

- **의존 섹션**: 앞 섹션이 정리된 뒤 순서대로 채운다
- **독립 섹션** 2개 이상: 병렬 보조가 필요하면 bounded helper를 쓸 수 있지만, skeleton ownership은 caller가 유지한다
- **다중 파일**: 공통 계약이 큰 파일부터 먼저 고정하고, 겹치지 않는 파일만 병렬화한다

각 섹션의 placeholder를 실제 내용으로 교체한다:
```
Edit(old_string="<!-- TODO: ... -->", new_string="[실제 내용]")
```

### Step 3: Finalize

- 파일에 남은 `<!-- TODO -->`, `# TODO:`, `<!-- Phase 2 -->` 등 모든 마커를 제거한다.
- 섹션 순서, 표/목록/링크, 파일 간 cross-reference를 다시 확인한다.
- 완료 결과를 사용자에게 보고한다.

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
