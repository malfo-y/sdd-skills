---
name: second-opinion
description: "Use this skill when the user asks for a \"second opinion\", \"세컨드 오피니언\", \"다른 관점\", \"codex에게 물어봐\", \"ask codex\", \"codex opinion\", or wants an independent review/analysis from Codex on a question, design decision, code, or debugging approach."
---

# Second Opinion — Codex를 통한 독립적 분석

사용자의 질문에 대해 관련 컨텍스트를 수집·요약한 후, Codex에게 독립적인 분석을 요청하고 결과를 그대로 전달한다.

## Acceptance Criteria

- [ ] AC1: 사용자 질문에서 언급된 파일/코드가 모두 수집되었다
- [ ] AC2: 컨텍스트가 구조화된 요약으로 Codex에 전달되었다
- [ ] AC3: Codex 결과가 가공 없이 사용자에게 전달되었다

## Hard Rules

1. **읽기 전용**: 수집부터 외부 분석까지 대상 코드·문서를 수정하지 않는다. 부모의 컨텍스트 임시 파일 생성만 예외다. 모든 위임 프롬프트에 분석 전용·파일 수정 금지·하위 agent 생성 금지를 전달한다.
2. **Codex 결과 원문 전달**: Codex 출력을 요약·편집하지 않는다.
3. **임시 파일 경로**: 컨텍스트 임시 파일 생성 시 `/tmp/second-opinion-*.md`에 저장한다.

## Process

### Step 1: Context Gathering

먼저 활성 런타임에서 외부 `codex:codex-rescue` adapter를 호출할 수 있는지 확인한다. 이 adapter는 별도 외부 설치 자산이며 이 번들이 제공하지 않는다. 독립 Codex 분석에 한한 dispatch 예외이며, 미가용이면 미완료로 보고한다. 다른 agent나 자체 답변에 Codex 이름을 붙여 대체하지 않는다.

사용자 입력에서 다음을 추출하고 수집한다:

- **명시된 파일**: 언급된 파일 경로를 `Read`로 읽는다
- **암시된 컨텍스트**: 주제 관련 코드를 `Grep`, `Glob`으로 탐색한다. 범위가 넓으면 `Agent(subagent_type="general-purpose")`에 필요한 탐색만 위임할 수 있다
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

확인된 `Agent(subagent_type="codex:codex-rescue")`에 아래 제약과 enriched 프롬프트를 전달한다. 긴 컨텍스트의 파일 참조는 adapter가 해당 경로를 읽을 수 있을 때 사용한다. 접근할 수 없으면 전달 가능한 인라인 컨텍스트로 보완하거나 접근 실패를 보고한다.

프롬프트 구성:
```
<task>
독립적인 second opinion을 제공하라. 분석만 수행하고 대상 코드·문서를 수정하지 마라.
하위 agent를 생성하지 마라. 명령은 읽기 전용 조사 범위에서만 실행하고, 실제 실행 여부와 검증 한계를 결과에 표시하라.
[Context와 사용자 원래 Question: 인라인 또는 접근 가능한 파일 참조]
</task>
```

### Step 4: Result Delivery

정상 Codex 분석 응답을 사용자에게 그대로 전달한다. 오류를 분석 결과나 성공으로 표시하지 않는다.

분석 결과가 없으면 원인과 미충족 AC를 보고하고 종료한다. 수집·전달의 복구 가능한 누락은 보완하되, 미가용·인증 오류 등 원인이 그대로인 외부 실패는 자동 재시도하지 않는다.

## Final Check

성공 경로는 AC1–3을 검증하고 보완 가능한 누락을 수정한다. 외부 blocker가 남으면 미완료와 미충족 AC를 보고한다. 원문 전달·read-only 위반을 소급 충족시키거나 자체 답변으로 AC를 닫지 않는다.
