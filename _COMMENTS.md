# _COMMENTS

Generated at: 2026-03-20T01:25:54.320Z
Total comments: 2

## Comments

### .codex/skills/write-phased/SKILL.md:L7-L9

얘는 다른 스킬들처럼 AC 기반 -> final check 등이 안 들어가 있어. 다른 스킬과 형식 맞춰 줘.

- anchor.hash: 5416f797
- anchor.snippet: # write-phased: Skeleton → Fill Orchestration

이 스킬은 `write_skeleton` agent를 호출해 골조를 만들고, SKELETON_ONLY이면 호출자(이 스킬)가 직접 채운다.
- createdAt: 2026-03-20T01:25:29.037Z

---

### .codex/skills/write-phased/SKILL.md:L60-L62

이건 틀린 말이야. 스킬은 스킬에서 호출 못 하잖아.

- anchor.hash: b098de30
- anchor.snippet: Integration Targets


- anchor.before: 다.

## Multi-File Strategy

여러 파일이 필요하면:

1. `write_skeleton`에 모든 대상 파일의 skeleton 작성을 요청한다.
2. 공통 타입, 기반 모듈, shared helper처럼 선행 의존성이 큰 파일부터 채운다.
3. 의존성이 낮은 파일은 조사나 초안 단계를 병렬화한다.
4. 마지막에 import, 링크, 참조 경로를 한 번에 검증한다.

## 
- anchor.after: 이 스킬은 사용자 직접 호출도 가능하지만, 다른 스킬이나 오케스트레이터가 장문 산출물에 적용하는 전략이기도 하다.

- primary producer targets: `spec-create`, `guide-create`, `pr-spec-patch`, `pr-review`, `spec-summary`, `spec-upgrade`
- nested producer targets: `feature
- createdAt: 2026-03-20T01:25:40.398Z
