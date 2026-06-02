---
name: feature-draft
description: This skill should be used when the user asks to "feature draft", "draft feature", "feature plan", "plan feature", "draft and plan", "feature draft parallel", "parallel feature draft", "병렬 기능 초안", "parallel feature plan", or wants to combine requirements gathering, spec patch drafting, and implementation planning with Target Files for parallel execution support.
version: 3.0.0
---

# Feature Draft (Entrypoint Wrapper — Mode B)

이 스킬은 entrypoint wrapper다. 사용자의 feature-draft 요청을 `feature_draft_agent`에 위임하고 그 결과를 사용자에게 전달한다. temporary spec 7섹션·Part 2 작성 규칙·Hard Rules·출력 형식은 agent가 단일 소스로 보유한다.

## 실행 (Mode B: context-forwarding)

feature-draft는 **입력이 대화에서 태어나는** 스킬이다. agent는 파일은 read하지만 **이번 세션의 대화는 못 읽으므로**, wrapper가 대화 맥락을 정리해 전달한다.

1. 다음을 수집한다:
   - 사용자 요청 원문 + 인자
   - 이미 아는 경로·산출물(관련 `_sdd/spec/*`, 직전 draft/discussion 경로 등)
   - **대화에만 있는 맥락 digest**: 이번 세션에서 합의된 요구사항·결정·제약·기각한 대안을 주제 기준으로 정리.
2. `spawn_agent(agent_type="feature_draft_agent", prompt=<요청 + 경로 + 대화 맥락 digest>)`로 dispatch하고 `wait_agent`로 결과를 수거한다.
3. agent의 반환(draft 경로 `_sdd/drafts/<YYYY-MM-DD>_feature_draft_<slug>.md`, Step 8에서 노출하는 Confidence=LOW/User-confirmation=Yes 결정)을 사용자에게 그대로 relay한다.

> **경계**: wrapper는 *대화 맥락을 모아 전달*까지만 한다. 요구사항 분석·delta 설계·Target Files 결정은 agent의 Input Analysis/Delta Design 단계가 수행한다(중복 금지).

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(feature-draft 호출)와 draft 산출 경로 계약은 이 wrapper가 유지한다.
- 실제 작성은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 핵심 결정(Step 8 Surface)을 wrapper가 relay해 보존한다.

> Source: 전체 계약·temporary spec 7섹션·작성 규칙은 `.codex/agents/feature-draft-agent.toml`이 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
