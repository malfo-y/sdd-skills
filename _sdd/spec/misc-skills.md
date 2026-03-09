# Misc Skills

## Responsibility

- 이 그룹은 핵심 spec/implementation/PR 워크플로우 바깥에 있는 보조 스킬을 다룬다.
- 현재 범위에는 `discussion`과 `ralph-loop-init`이 포함된다.
- 이 그룹은 메인 SDD 개발 루프를 대체하지 않고, 방향 탐색이나 특수한 자동화 워크플로우를 보조한다.

## Owned Paths

- `.claude/skills/discussion/`
- `.codex/skills/ralph-loop-init/`
- `.claude/skills/ralph-loop-init/`
- `_sdd/discussion/`

## Key Symbols / Entry Points

- `.claude/skills/discussion/SKILL.md`
- `.codex/skills/ralph-loop-init/SKILL.md`
- `.claude/skills/ralph-loop-init/SKILL.md`
- `_sdd/discussion/discussion_two_level_spec_concept.md`
- `_sdd/discussion/discussion_concept_implementation_step.md`

## Interfaces / Contracts

### discussion

- 현재 Claude 전용 스킬이다.
- 역할: 요구사항/방향이 불명확할 때 구조화된 의사결정 토론을 수행한다.
- 기대 산출물: 결정, 미결, 후속 액션이 정리된 토론 결과
- 후속 연결: `feature-draft` 또는 `implementation-plan`의 입력으로 들어간다.

### ralph-loop-init

- Codex와 Claude 양쪽에 존재한다.
- 역할: 장기 실행 ML training/debug loop를 위한 `ralph/` 디렉터리 구조를 생성한다.
- 기대 산출물: 훈련/디버그 루프 운영에 필요한 문서와 스캐폴드
- 후속 연결: 일반 SDD 워크플로우와는 느슨하게 연결된다.

## Dependencies

### Upstream

- `README.md`
- `docs/SDD_WORKFLOW.md`
- `_sdd/discussion/` 메모

### Downstream

- `discussion` 결과는 `feature-draft`, `implementation-plan`로 이어질 수 있다.
- `ralph-loop-init`은 독립적인 운영 루프를 만들기 때문에 core spec sync chain과 직접 연결되지는 않는다.

## Change Recipes

### discussion 스킬을 바꿀 때

1. `.claude/skills/discussion/SKILL.md`를 먼저 수정한다.
2. `README.md`, `docs/SDD_WORKFLOW.md`에 토론 게이트 설명이 맞는지 확인한다.
3. `_sdd/discussion/`의 개념 메모가 여전히 유효한지 점검한다.

### ralph-loop-init 스킬을 바꿀 때

1. `.codex/skills/ralph-loop-init/`와 `.claude/skills/ralph-loop-init/`를 함께 확인한다.
2. 플랫폼별 설명, 예시, 참조 문서가 같은 구조를 유지하는지 본다.
3. core SDD 스킬과 무관한 내용이 main spec에 새어 나오지 않게 한다.

## Tests / Observability

- `rg "discussion|ralph" .claude/skills .codex/skills README.md docs/SDD_WORKFLOW.md`
- Claude 전용 스킬 여부와 Codex/Claude 공통 스킬 여부가 문서에 일관되게 적혀 있는지 확인
- `_sdd/discussion/` 문서가 실제 워크플로우 설명과 모순되지 않는지 검토

## Risks / Invariants

- `discussion`은 현재 `.claude/skills/`에만 존재하므로, Codex 경로를 가정하면 안 된다.
- `ralph-loop-init`은 core SDD 루프의 일부가 아니므로, main workflow와 동일 선상으로 다루면 문서가 산만해질 수 있다.
- misc 스킬은 존재 이유와 연결 지점을 짧고 분명하게 적는 편이 메인 인덱스 탐색성에 유리하다.

## Open Questions

- `discussion`을 Codex 쪽에도 제공할지 아직 결정되지 않았다.
- `ralph-loop-init`을 계속 misc 그룹으로 둘지, 별도 ML automation 그룹으로 분리할지 검토가 필요하다.
