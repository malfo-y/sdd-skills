---
name: second-opinion
description: "Use this skill when the user asks for a \"second opinion\", \"세컨드 오피니언\", \"다른 관점\", \"codex에게 물어봐\", \"ask codex\", \"codex opinion\", or wants an independent review/analysis from Codex on a question, design decision, code, or debugging approach."
version: 1.0.0
---

# Second Opinion — Codex를 통한 독립적 분석

사용자의 질문에 대해 관련 컨텍스트를 수집·요약한 후, Codex에게 독립적인 분석을 요청하고 결과를 그대로 전달한다.

## Acceptance Criteria

- [ ] AC1: 사용자 질문에서 언급된 파일/코드가 모두 수집되었다
- [ ] AC2: 컨텍스트가 구조화된 요약으로 Codex에 전달되었다
- [ ] AC3: Codex 결과가 가공 없이 사용자에게 전달되었다

## Hard Rules

1. **읽기 전용**: Step 1-2에서 코드를 수정하지 않는다. 컨텍스트 수집만 한다.
2. **Codex 결과 원문 전달**: Codex 출력을 요약·편집하지 않는다.
3. **임시 파일 정리**: 컨텍스트 임시 파일 생성 시 `/tmp/second-opinion-*.md`에 저장한다.

## Process

### Step 1: Context Gathering

사용자 입력에서 다음을 추출하고 수집한다:

- **명시된 파일**: 언급된 파일 경로를 `Read`로 읽는다
- **암시된 컨텍스트**: 주제 관련 코드를 `Grep`, `Glob`으로 탐색한다. 범위가 넓으면 `Agent(Explore)`를 사용한다
- **질문 핵심**: 사용자가 Codex에게 판단받고 싶은 것이 무엇인지 파악한다

### Step 2: Context Packaging

수집된 컨텍스트를 구조화한다:

```markdown
## Context
[파일 내용, 코드 스니펫, 아키텍처 정보 등]

## Question
[사용자의 원래 질문]
```

**분기 기준**:
- 요약이 짧으면 (< 2000자): 프롬프트에 인라인으로 포함
- 요약이 길면: `/tmp/second-opinion-context-<timestamp>.md`에 저장하고, Codex 프롬프트에 `"Read /tmp/second-opinion-context-<timestamp>.md for full context."` 형태로 파일 경로를 전달

### Step 3: Codex Forwarding

`Agent(subagent_type="codex:codex-rescue")`로 enriched 프롬프트를 전달한다.

프롬프트 구성:
```
<task>
독립적인 second opinion을 제공하라.
[인라인 컨텍스트 또는 파일 참조]
</task>
```

### Step 4: Result Delivery

Codex 응답을 사용자에게 그대로 전달한다.

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
