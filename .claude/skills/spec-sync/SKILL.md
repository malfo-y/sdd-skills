---
name: spec-sync
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "add to-do to spec", "add to-implement to spec", "add requirements to spec", "update spec from input", "spec update", "expand spec", "update spec from code", "sync spec with implementation", "apply implementation changes to spec", "reflect completed work in spec", "refresh spec after implementation", "implementation done sync", or mentions adding new features/requirements/planned improvements to a specification document, or maintaining the spec document tied to completed code changes.
---

# Spec Sync (Planned + Implemented) (표면 묶음 Orchestrator)

이 스킬은 orchestrator entrypoint다. 사용자의 spec-sync 요청을 `sdd-skills:spec-sync-agent`에 위임하고 그 결과를 사용자에게 전달한다. 단일 진입점으로 구현 전(planned)·구현 후(implemented) 책임을 모두 이 agent에 위임하되, **evidence 있는 implemented sync는 표면 묶음 2개(본문 ∥ 기록)로 분할 병렬 dispatch**한다 — 묶음 정의·쓰기 서로소 불변식(작성자 병렬의 안전 근거)은 agent의 `호출자 표면 한정` 절이 단일 소스다. 전체 sync 프로세스·status 분류·Repo-wide Invariant Test는 agent가 단일 소스로 보유한다.

## Implemented Sync Digest

아래 네 필드는 모두 비어 있지 않아야 하고, `Spec Version`은 SemVer다.

- **Delta List**: 변경 항목 목록
- **Classification Basis**: 코드와 validation evidence에 근거한 분류 요약
- **Spec Version**: 신규 spec 버전
- **Decision Title**: decision log 제목

## 실행

1. 사용자 요청 + 대상 경로(있으면 temporary spec / feature draft / user input / implementation artifact / spec 경로)와 이미 아는 결정을 수집한다 (orchestrator는 새 분석 read를 하지 않는다 — 아래 선고정의 버전 grep 1회만 명시 예외).
2. evidence 유무로 분기한다:
   - **구현 전(planned 반영)**: 현행대로 `Agent(subagent_type="sdd-skills:spec-sync-agent", prompt=<요청 + 알려진 경로/컨텍스트>)` **1회** dispatch. 대상 경로가 불명확하면 agent가 Input Sources 우선순위로 자체 탐색하도록 위임한다.
   - **구현 후(implemented sync)**: **선고정** — `Implemented Sync Digest`를 완성한다(버전이 대화에서 미상이면 `main.md` 헤더 버전만 targeted grep **1회** 허용). 그 뒤 **한 메시지에서 동일 digest를 넣은 두 표면 묶음을 병렬 dispatch한다**:
     - `Agent(subagent_type="sdd-skills:spec-sync-agent", prompt=<요청 + 경로 + 선고정 digest + 본문 묶음 한정>)`
     - `Agent(subagent_type="sdd-skills:spec-sync-agent", prompt=<요청 + 경로 + 선고정 digest + 기록 묶음 한정>)`
3. **사후 정합 검사** (implemented 분할 경로만, grep 2종): ① `main.md` 헤더 버전과 `logs/changelog.md` 최신 entry 버전의 **일치**, ② `git diff`에서 `decision_log.md`·`changelog.md`의 **삭제 줄 0**(append-only). 불일치는 relay에 명시한다 — orchestrator는 gating하지 않는다(fix는 호출자 소관).
4. relay: 각 agent의 final과 사후 정합 검사 결과를 사용자에게 전달한다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(planned 반영 호출 + implemented sync 호출)와 `_sdd/spec/*.md` 동기화 계약은 이 orchestrator가 유지한다.
- 실제 status 분류·drift 분석·spec 수정은 agent가 수행한다. input file 처리 범위도 agent의 `호출자 표면 한정`을 따른다. agent가 지원하지 않는 동작을 orchestrator가 흉내내지 않는다.

> Source: 전체 계약·status 분류·Repo-wide Invariant Test는 `.claude/agents/spec-sync-agent.md`가 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
