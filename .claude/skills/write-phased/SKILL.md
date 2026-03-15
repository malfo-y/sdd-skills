---
name: write-phased
description: Use this skill when the user asks to write, create, or generate a document or code file. Triggers on "write-phased", "문서 작성", "작성해줘", "만들어줘", "코드 작성", "파일 생성", "구현해줘", "write a document", "create a file", "generate code", "implement", or any request to produce a markdown document, code file, config file, or technical writing.
version: 1.1.0
---

# write-phased (Wrapper)

이 스킬은 `write-phased` 서브에이전트에 작업을 위임한다.

## 실행 방법

사용자의 요청을 그대로 `write-phased` 서브에이전트에 전달한다:

```
Agent(
  subagent_type="write-phased",
  prompt="[사용자의 원래 요청 전체를 그대로 전달]"
)
```

## 규칙

1. 이 스킬에서 직접 파일을 작성하지 않는다.
2. 사용자의 요청을 요약하거나 변형하지 말고 원문 그대로 서브에이전트에 전달한다.
3. 서브에이전트의 결과를 받아 사용자에게 보고한다.
