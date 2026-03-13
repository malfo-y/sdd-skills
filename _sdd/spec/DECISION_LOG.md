# Decision Log

## 2026-03-09 - Exploration-first spec adopted for the SDD skills repo

### Context

이 저장소는 스킬 프롬프트와 문서를 다루기 때문에, 코드 설명서보다 "어디를 보고 무엇을 함께 바꿔야 하는지"가 더 중요하다.

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

이 저장소의 핵심 변경 축은 개별 스킬보다 "workflow group" 단위로 움직이는 경우가 많다. 그룹 스펙이 현재 탐색성과 유지보수성의 균형이 더 좋다.

## 2026-03-09 - Codex skill tree treated as the primary spec target

### Context

최근 정렬 작업과 버전 보강은 `.codex/skills/`를 기준으로 진행되었고, `.claude/skills/`는 평행 구조이지만 완전 동기화 기준은 아직 문서로 확정되지 않았다.

### Decision

현재 저장소 스펙은 `.codex/skills/`를 주 기준으로 설명하고, `.claude/skills/`는 배포/변형 레이어로 다룬다.

### Rationale

현재 실제 정렬 작업과 품질 기준이 Codex 쪽에 집중되어 있으므로, 메인 스펙의 기준선도 여기에 두는 편이 더 명확하다. 플랫폼 parity의 범위는 `Open Questions`로 남긴다.

## 2026-03-13 - Spec Upgrade to Whitepaper Format (v1.1.0 → v2.0.0)

### Context

기존 스펙(`main.md` v1.1.0, 598줄)이 whitepaper §1-§8 구조에 근접했으나 완전히 준수하지 않았다. 서사 섹션(§1 Background & Motivation, §2 Core Design)이 부족하고, 컴포넌트별 Why/Source 필드가 없었으며, Code Reference Index가 없었다.

### Decision

- 기존 멀티파일 구조(main.md + 3 서브 스펙)에서 단일 파일 구조로 이미 통합된 상태를 유지
- 기존 내용을 §1-§8에 재배치: 목표→§1, 공통 패턴→§2, 워크플로우/아티팩트 맵→§3, 플랫폼 차이/설치→§8
- 모든 16개 컴포넌트에 Why와 Source 필드 추가
- Code Reference Index 부록 신규 생성 (16개 SKILL.md 파일 매핑)
- 2-Phase Generation 패턴을 §2 Core Design에 추가 (신규 도입된 패턴)
- 스킬 수 14→16 업데이트 (spec-upgrade, guide-create 반영)

### Rationale

SDD_SPEC_DEFINITION.md 기준 whitepaper 형식 준수. spec-upgrade 스킬의 2-phase 전략 적용 (598줄 >= 300줄 threshold). 기존 내용 최대 보존 원칙에 따라 삭제 없이 재배치.

### Changes

- `_sdd/spec/main.md` — v1.1.0 → v2.0.0 (598줄 → 672줄)
- `_sdd/spec/prev/PREV_sdd_skills_20260313_120859.md` — 백업 생성
