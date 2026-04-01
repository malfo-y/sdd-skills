# 토론 요약: write_skeleton 제거와 inline writing 전환

**날짜**: 2026-04-01
**라운드 수**: 4
**주제**: `write_skeleton` 같은 writing helper agent가 필요한지, 아니면 호출자가 inline 2-phase 방식으로 직접 골격 작성과 내용 채우기를 수행하는 편이 더 적절한지 논의

## 핵심 논점

1. skeleton 생성이 부모 콘텍스트에 강하게 의존할 때 별도 subagent 분리가 실제로 이득이 있는가
2. `write_skeleton` handoff contract, `fork_context`, outline ownership 같은 추가 비용이 사용성 저하로 이어지는가
3. 기본 writing backbone을 helper agent로 둘지, producer/caller의 inline orchestration으로 둘지
4. `write_skeleton` 제거 시 `write-phased`를 어떤 역할로 재정의해야 하는지

## 결정 사항

1. `write_skeleton` 같은 helper agent는 기본 writing 경로에 필요하지 않다.
2. 골격 작성은 별도 subagent에 위임하기보다, 현재 콘텍스트를 가장 잘 가진 호출자가 inline으로 직접 수행하는 편이 더 낫다.
3. 이유는 handoff contract 설계, `fork_context` 의존, 콘텍스트 재설명 비용이 실제 이득을 상쇄하기 때문이다.
4. 따라서 일반 writing 흐름은 `파일에 먼저 skeleton/섹션 제목 작성 -> 섹션별 fill -> TODO/Phase 마커 정리`를 호출자가 직접 수행하는 **inline 2-phase writing**으로 정리한다.
5. `write_skeleton`은 deprecated 유지 대신 **완전 제거** 방향이 더 적절하다.
6. `write-phased`는 helper agent를 호출하는 오케스트레이터가 아니라, subagent 없이 호출자가 직접 수행하는 **inline 2-phase writing 규칙 스킬**로 재정의한다.

## open questions

없음. 현재 논의 범위의 open question은 모두 결정되었다.

## action items

1. `write_skeleton` 전제 호출부와 문서를 점검해 inline 2-phase writing 지시로 치환한다.
2. `write-phased`를 `spawn_agent(write_skeleton)` 기반 설명에서, 호출자 직접 skeleton 작성 규칙으로 재작성한다.
3. `implementation`, `sdd-autopilot`, 기타 producer 스킬에서 writing helper agent 전제를 제거할지 검토한다.
4. 이 결론을 반영한 feature draft 또는 spec patch가 필요하면 후속 문서로 확장한다.

## 리서치 결과 요약

- 현재 저장소의 `write_skeleton` 사용은 helper 분리 자체보다 handoff contract 품질에 크게 좌우된다.
- subagent 분리 시 caller가 충분한 콘텍스트를 다시 말아서 전달해야 하므로, skeleton 생성처럼 문맥 의존성이 큰 작업은 오히려 inline 처리 쪽이 더 자연스럽다.
- `implementation` 및 `sdd-autopilot` 계열은 최근에도 추상적인 agent 호출을 실제 Codex-native 문법으로 구체화하는 논의가 있었고, 이는 helper 분리의 실행 비용을 다시 드러내는 사례다.

## sources

- `/Users/hyunjoonlee/github/sdd_skills/.codex/skills/implementation/SKILL.md`
- `/Users/hyunjoonlee/github/sdd_skills/.codex/skills/sdd-autopilot/SKILL.md`
- `/Users/hyunjoonlee/github/sdd_skills/.codex/skills/write-phased/SKILL.md`
- `/Users/hyunjoonlee/github/sdd_skills/.codex/agents/write-skeleton.toml`
- 본 대화의 사용자 판단과 후속 토론

## 토론 흐름

1. 사용자는 `write_skeleton` 같은 agent는 사실 필요 없고, 호출자에게 inline으로 "골격을 먼저 적고 내용을 채워라"라고 지시하는 편이 더 낫다는 판단을 제시했다.
2. 논의 범위를 `write_skeleton` 전반으로 넓혀, helper agent 분리의 이득과 비용을 비교했다.
3. handoff contract, `fork_context`, outline ownership 같은 추가 복잡도가 사용성 저하를 일으킨다는 점을 확인했다.
4. 그 결과 기본 경로에서는 helper agent를 제거하고, caller가 자신의 콘텍스트에서 직접 inline 2-phase writing을 수행하는 쪽이 더 낫다고 합의했다.
5. 후속 구조로는 `write-phased`를 helper orchestrator가 아니라 inline writing 규칙 스킬로 재정의하는 방향을 택했다.
