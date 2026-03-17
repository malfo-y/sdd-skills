---
name: write-phased
description: This skill should be used when the user asks to "write-phased", "문서 작성", "작성해줘", "만들어줘", "코드 작성", "파일 생성", "구현해줘", "write a document", "create a file", "generate code", "implement", or any request to produce a markdown document, code file, config file, or technical writing. Applies a 2-phase strategy: skeleton first, then fill.
version: 1.2.0
---

# write-phased: 2-Phase Writing Strategy (Wrapper)

이 스킬은 `write_phased` custom agent에 작업을 위임합니다.

## Hard Rules

1. 이 wrapper는 직접 구현 로직이나 장문 workflow 본문을 들고 있지 않는다.
2. 사용자의 요청과 관련 artifact 경로를 가능한 한 그대로 `write_phased`에 전달한다.
3. 결과는 custom agent의 산출물을 기준으로 사용자에게 보고한다.

## Output Contract

- 기본 산출물: the target file or files requested by the caller
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `write_phased` agent 정의가 담당한다.

## Execution

생성된 orchestrator나 직접 호출 흐름 모두 `write_phased` custom agent를 실행 단위로 사용한다.
