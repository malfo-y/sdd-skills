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

> **⚠️ Superseded by 2026-03-13 decision below**

## 2026-03-13 - Platform primary target reassessment (.claude/ as source of truth)

### Context

2026-03-09 결정에서 `.codex/skills/`를 주 기준으로 설정했으나, 이후 모든 스킬 변경이 양 플랫폼 동시 적용되고 Claude Code가 더 많은 스킬을 보유(19 vs 17)하게 되었다. 스펙 자체도 `.claude/` 경로를 기준으로 기술하고 있어 실제 운영과 이전 결정이 불일치.

### Decision

`.claude/skills/`를 원본(source of truth)으로, `.codex/skills/`를 파생본으로 정의한다. 동기화 방향은 `.claude/` → `.codex/`.

### Rationale

Claude Code가 기능 상위 집합(19개 vs 17개)이고, Claude Code 전용 스킬(git, sdd-upgrade, discussion)이 존재하며, 스펙과 커밋 히스토리 모두 `.claude/` 기준으로 운영되고 있다.

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

## 2026-03-16 - Dual Architecture: Skill + Agent Layer (v2.1.0 → v3.0.0)

### Context

기존 SDD Skills는 스킬 전용(skills-only) 아키텍처로, 20개 스킬이 `.claude/skills/*/SKILL.md`에 전체 로직을 포함하고 있었다. 사용자가 대규모 기능을 구현하려면 6-7개 스킬을 수동으로 순서대로 호출해야 하며, 중간에 맥락이 유실되거나 단계를 빠뜨릴 위험이 있었다. `write-phased` 에이전트가 `tools: ["Agent"]`로 서브에이전트 호출이 가능함을 증명하였다.

### Decision

1. **스킬 + 에이전트 이중 아키텍처 도입**: 8개 파이프라인 필수 스킬을 `.claude/agents/*.md` 에이전트 정의로 분리하고, 기존 SKILL.md는 Agent Wrapper 래퍼로 전환
2. **autopilot 메타스킬 추가**: 적응형 오케스트레이터를 생성하여 에이전트 파이프라인을 end-to-end 자율 실행
3. **오케스트레이터 저장 위치**: `_sdd/pipeline/`에 저장 (초기 토론에서 `.claude/skills/`로 결정했으나, 후속 토론에서 변경 — 일회성 실행 계획이므로 스킬 디렉토리 오염 방지)
4. **Codex는 기존 유지**: Agent 도구 제한으로 래퍼 패턴 불가. Codex 동기화는 별도 후속 작업

### Rationale

- 사용자 인터페이스(`/스킬명`) 하위 호환성 유지가 필수 → 래퍼 스킬 유지
- autopilot의 서브에이전트 호출을 위해 에이전트 레이어 필요 → Agent Wrapper 패턴
- 선행 집중형 사용자 인터랙션(Phase 1 interactive, Phase 2 autonomous) → 2-Phase Orchestration 패턴
- Discussion은 AskUserQuestion이 핵심이므로 에이전트 전환 불필요 → 스킬 유지

### Changes

- `_sdd/spec/main.md` — v2.1.0 → v3.0.0
- `.claude/agents/` — 8개 에이전트 정의 신규 생성
- `.claude/skills/*/SKILL.md` — 8개 래퍼 전환
- `.claude/skills/autopilot/` — 메타스킬 신규 생성
- `_sdd/spec/prev/PREV_main_20260316_120000.md` — 백업 생성

### References

- 토론: `_sdd/discussion/discussion_autopilot_meta_skill.md`
- 후속 토론: `_sdd/discussion/discussion_autopilot_open_questions.md`
- Feature Draft: `_sdd/drafts/feature_draft_autopilot_meta_skill.md`
