---
name: write-phased
description: 'This skill should be used when the user asks to "write-phased", "문서 작성", "작성해줘", "만들어줘", "코드 작성", "파일 생성", "구현해줘", "write a document", "create a file", "generate code", "implement", or any request to produce a markdown document, code file, config file, or technical writing. The caller writes the skeleton inline first, then fills and finalizes in the same flow.'
version: 3.0.0
---

# write-phased — Inline 2-Phase Writing

별도 writing helper agent를 spawn하지 않는다. 호출자가 현재 콘텍스트에서 먼저 skeleton/outline/TODO marker를 파일에 기록하고, 같은 흐름에서 내용을 채우고 finalize한다.

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
- 언어/톤/출력 형식
- placeholder를 실제 내용으로 치환하라는 지시

### Step 3: Finalize

- 파일에 남은 `<!-- TODO -->`, `# TODO:`, `<!-- Phase 2 -->` 등 모든 마커를 제거한다.
- 다중 파일이면 파일 간 이름, import, 참조 관계를 교차 검증한다.
- 완료 결과를 사용자에게 보고한다.

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
