# Decision Log

## 2026-03-09 - Exploration-first spec adopted for the SDD skills repo

### Context

이 저장소는 스킬 프롬프트와 문서를 다루기 때문에, 코드 설명서보다 “어디를 보고 무엇을 함께 바꿔야 하는지”가 더 중요하다.

### Decision

이 저장소의 스펙도 일반 코드베이스와 같은 탐색형 기준을 적용한다. 메인 문서는 entry point 역할을 하고, 상세는 그룹 스펙으로 분리한다.

### Rationale

스킬 간 계약, 앵커 섹션, spec sync 분류 같은 공통 규칙은 코드보다 문서 사이의 연결을 더 잘 보여줘야 안전하게 바뀔 수 있다.

## 2026-03-09 - Grouped component specs preferred over per-skill specs

### Context

`.codex/skills/`에는 13개의 Codex 스킬이 있고, 이를 곧바로 13개 컴포넌트 스펙으로 쪼개면 메인 스펙보다 탐색 비용이 커질 수 있다.

### Decision

초기 스펙은 `spec lifecycle`, `implementation lifecycle`, `PR lifecycle`의 3개 그룹 스펙으로 시작한다.

### Rationale

이 저장소의 핵심 변경 축은 개별 스킬보다 “workflow group” 단위로 움직이는 경우가 많다. 그룹 스펙이 현재 탐색성과 유지보수성의 균형이 더 좋다.

## 2026-03-09 - Codex skill tree treated as the initial alignment baseline

### Context

최근 정렬 작업과 버전 보강은 `.codex/skills/`를 기준으로 진행되었고, `.claude/skills/`는 평행 구조이지만 완전 동기화 기준은 아직 문서로 확정되지 않았다.

### Decision

초기 정렬 작업과 버전 보강은 `.codex/skills/`를 기준으로 먼저 진행한다.

### Rationale

실제 정렬 작업이 Codex 쪽에 먼저 집중되었기 때문에, 초기 기준선을 여기에 두는 것이 작업 순서를 관리하기 쉬웠다. 다만 이 결정은 “문서 설명 범위”와는 분리되어야 한다.

## 2026-03-09 - Repository spec widened to cover both Codex and Claude skill trees

### Context

초기 메인/그룹 스펙은 `.codex/skills/` 경로를 중심으로 써서, 실제 저장소가 가진 `.claude/skills/` 트리와 `discussion` 같은 Claude 전용 스킬을 충분히 드러내지 못했다.

### Decision

현재 저장소 스펙은 `.codex/skills/`와 `.claude/skills/`를 모두 다루고, 공통 스킬은 양쪽 경로를 함께 적는다. `discussion`, `ralph-loop-init` 같은 비핵심 보조 스킬은 `misc-skills.md`로 분리한다.

### Rationale

이 저장소는 실제로 두 플랫폼 배포 구조를 함께 운영한다. 메인 스펙과 그룹 스펙이 한쪽만 설명하면 탐색성과 변경 안전성이 떨어진다. 보조 스킬은 별도 그룹으로 분리하는 편이 메인 인덱스를 더 읽기 쉽게 만든다.
