# Component Reference & Strategic Code Map

> 이 문서는 [main.md](./main.md)에서 분리된 reference-only supporting surface다.
> normative decision-bearing truth는 `main.md`에 두고, 여기에는 각 컴포넌트의 `Purpose / Why / Source`와 최소한의 navigation note만 남긴다.
> 상세 Input/Output/Process/완료 이력은 각 스킬 원문과 관련 artifact에서 확인한다.

---

## Orchestration & Spec Lifecycle

| Component | Purpose | Why | Primary Source | Notes |
|-----------|---------|-----|----------------|-------|
| `sdd-autopilot` | reasoning 기반으로 SDD 파이프라인을 조합하고 end-to-end 실행한다 | 대규모 작업에서 수동 handoff와 단계 누락을 줄인다 | `.claude/skills/sdd-autopilot/SKILL.md`<br>`.codex/skills/sdd-autopilot/SKILL.md` | 풀 스킬. non-trivial planning은 `feature-draft`를 기본 entry로 사용하고, multi-phase plan이면 `per-phase` gate와 `final integration review`를 집행한다 |
| `spec-create` | 초기 global spec과 workspace guidance를 부트스트랩한다 | 스펙 부재 상태에서 workflow 시작점을 만들고, thin global 기본 구조를 고정한다 | `.claude/skills/spec-create/SKILL.md` | 워크플로우 시작점. 기본값은 `_sdd/spec/main.md` 단일 파일이며, multi-file은 structure rationale이 있을 때만 연다 |
| `feature-draft` | spec patch 초안과 구현 계획 초안을 한 번에 만든다 | spec 수정과 구현 계획의 반복 작업을 줄인다 | `.claude/agents/feature-draft.md`<br>`.claude/skills/feature-draft/SKILL.md` | wrapper -> agent 패턴 |
| `spec-update-todo` | 구현 전 planned persistent truth를 global spec에 반영한다 | spec-code drift를 사전에 줄인다 | `.claude/agents/spec-update-todo.md`<br>`.claude/skills/spec-update-todo/SKILL.md` | wrapper -> agent 패턴 |
| `spec-update-done` | 구현 evidence를 검토해 검증된 지속 정보만 global spec에 올린다 | 임시 실행 메모와 검증된 truth를 분리한다 | `.claude/agents/spec-update-done.md`<br>`.claude/skills/spec-update-done/SKILL.md` | delta status 분류 기반 sync. lowercase canonical artifact를 우선 읽고 legacy path를 fallback으로 허용한다 |
| `spec-review` | 스펙 품질과 코드-스펙 drift를 read-only로 진단한다 | 수정 없이 현재 상태를 객관적으로 점검하고, global/temporary rubric을 섞어 오탐하는 것을 줄인다 | `.claude/agents/spec-review.md`<br>`.claude/skills/spec-review/SKILL.md` | wrapper -> agent 패턴. rubric separation과 evidence strictness를 기준으로 본다 |
| `spec-rewrite` | 비대한 스펙을 canonical-fit 기준으로 재구성한다 | global/spec surface의 구조적 오염을 줄이되 판단 근거를 잃지 않는다 | `.claude/skills/spec-rewrite/SKILL.md`<br>`.codex/skills/spec-rewrite/SKILL.md` | 계획 파일과 rewrite report를 먼저/함께 남긴다. body에는 최소 rationale만 남기고 정리 메모는 log/report로 내린다 |
| `spec-summary` | global spec, supporting surface, 필요한 code grounding을 엮어 reader-facing whitepaper를 작성한다 | 문제, 동기, 핵심 설계, 코드 근거, 사용/기대 결과를 한 문서에서 이해하게 한다 | `.claude/skills/spec-summary/SKILL.md` | `_sdd/spec/summary.md` 생성용. 관련 draft/implementation artifact가 있으면 planned/progress 신호를 appendix에만 짧게 덧붙일 수 있다 |
| `spec-upgrade` | legacy global spec을 current canonical model로 마이그레이션한다 | 오래된 section-map과 inventory-heavy 구조를 정리하되, rewrite가 필요한 구조 재편은 분리한다 | `.claude/skills/spec-upgrade/SKILL.md`<br>`.codex/skills/spec-upgrade/SKILL.md` | 구조 업그레이드 전용. 시작 시 rewrite boundary를 먼저 판정한다 |
| `guide-create` | 특정 기능의 구현/리뷰용 deep-dive guide를 생성한다 | thin global spec 밖의 세부 설명 surface가 필요하다 | `.claude/skills/guide-create/SKILL.md`<br>`.codex/skills/guide-create/SKILL.md` | compact template pair를 같이 확인한다 |

## Delivery & Review

| Component | Purpose | Why | Primary Source | Notes |
|-----------|---------|-----|----------------|-------|
| `implementation-plan` | 대규모 구현을 phase/task 단위로 나눈다 | 한 세션에 모든 구현을 몰아넣을 때 생기는 품질 저하를 줄인다 | `.claude/agents/implementation-plan.md`<br>`.claude/skills/implementation-plan/SKILL.md` | `feature-draft` 후속 확장 단계. phase metadata가 autopilot의 execution gate source가 된다 |
| `implementation` | 구현 계획을 따라 코드를 작성하고 검증한다 | execute와 verify를 분리하지 않는 delivery step이 필요하다 | `.claude/agents/implementation.md`<br>`.claude/skills/implementation/SKILL.md` | wrapper -> agent. AC-first와 재검증 loop가 핵심 |
| `implementation-review` | 구현 결과를 계획/AC 기준으로 다시 검증한다 | 누락과 품질 이탈을 조기에 드러낸다 | `.claude/agents/implementation-review.md`<br>`.claude/skills/implementation-review/SKILL.md` | wrapper -> agent. fresh verification 중시 |
| `pr-review` | PR 코드 품질과 spec 준수 여부를 함께 판정한다 | 코드 리뷰와 spec 기반 검증을 한 surface로 묶는다 | `.claude/skills/pr-review/SKILL.md`<br>`.codex/skills/pr-review/SKILL.md` | findings-first. spec 존재 시 추가 검증 |
| `investigate` | 범용 근본원인 분석과 수정/검증을 수행한다 | 임의 수정 반복 대신 root-cause-first 디버깅을 강제한다 | `.claude/agents/investigate.md`<br>`.claude/skills/investigate/SKILL.md` | wrapper -> agent. blast radius와 fresh verification 포함 |

## Discussion & Utilities

| Component | Purpose | Why | Primary Source | Notes |
|-----------|---------|-----|----------------|-------|
| `discussion` | 구조화된 의사결정 토론을 진행한다 | 설계 선택과 open question을 추적 가능하게 만든다 | `.claude/skills/discussion/SKILL.md`<br>`.codex/skills/discussion/SKILL.md` | 풀 스킬. 양 플랫폼 모두 대화형 입력 사용. 결과는 `_sdd/discussion/<YYYY-MM-DD>_discussion_<slug>.md`에 저장한다 |
| `ralph-loop-init` | 장기 실행 프로세스용 자동화 디버그 루프를 만든다 | 반복 실험/테스트 환경을 표준화한다 | `.claude/agents/ralph-loop-init.md`<br>`.claude/skills/ralph-loop-init/SKILL.md` | wrapper -> agent 패턴 |
| `git` | 변경을 의미 단위로 정리해 커밋/브랜치 작업을 돕는다 | AI가 만든 변경을 의도 단위로 정리해야 한다 | `.claude/skills/git/SKILL.md` | Claude Code 전용 |
| `spec-snapshot` | 스펙 상태를 타임스탬프 스냅샷으로 보존한다 | 원본을 건드리지 않고 특정 시점 상태나 번역본을 관리한다 | `.claude/skills/spec-snapshot/SKILL.md`<br>`.codex/skills/spec-snapshot/SKILL.md` | snapshot/export 성격 |
| `second-opinion` | 관련 맥락을 모아 Codex의 독립 분석을 요청한다 | 단일 에이전트 관점 편향을 줄인다 | `.claude/skills/second-opinion/SKILL.md` | Claude Code 전용, read-only |

## Platform Notes

| Surface | What To Remember | Source |
|---------|------------------|--------|
| Claude wrapper/agent split | 다수의 execution-heavy skill은 wrapper가 사용자 entrypoint를 지키고 agent가 실제 실행 단위를 담당한다 | `.claude/skills/`, `.claude/agents/` |
| Codex custom agent runtime | Codex는 `.codex/agents/`와 `.codex/config.toml`의 nested-agent 설정이 중요하다 | `.codex/agents/`, `.codex/config.toml` |
| Artifact path convention | 신규 temporary artifact는 lowercase canonical 경로를 기본으로 하고, skill-defined output surface는 dated slug naming을 사용한다. reader는 legacy uppercase/fixed-name path를 fallback으로 읽는다 | 관련 `SKILL.md`, `_sdd/implementation/implementation_progress.md` |
| Full-skill exceptions | `sdd-autopilot`, `discussion`처럼 사용자 상호작용이 핵심인 surface는 풀 스킬로 유지된다 | 관련 `SKILL.md` |
| Platform-only features | `git`, `second-opinion`은 Claude Code 전용이며, Codex parity 대상이 아니다 | 관련 `SKILL.md` |

---

## Appendix A. Strategic Code Map

전수형 파일 inventory 대신, 변경 시 먼저 봐야 할 navigation-critical path만 남긴다.

| Type | Path | Why Start Here |
|------|------|----------------|
| Canonical model | `docs/SDD_SPEC_DEFINITION.md` | global spec과 temporary spec의 shape를 고정한다 |
| Workflow contract | `docs/SDD_WORKFLOW.md` | 스킬 역할, update order, artifact 배치를 가장 빠르게 확인할 수 있다 |
| Thin global spec | `_sdd/spec/main.md` | repo-wide decision-bearing truth와 supporting surface 책임이 여기서 정해진다 |
| Component reference | `_sdd/spec/components.md` | 개별 컴포넌트의 compact reference를 모아 둔다 |
| Usage scenarios | `_sdd/spec/usage-guide.md` | 실제 사용 흐름과 expected result를 빠르게 확인한다 |
| Claude orchestration hotspot | `.claude/skills/sdd-autopilot/SKILL.md` | reasoning-based pipeline semantics와 hard rules가 모인다 |
| Codex orchestration hotspot | `.codex/skills/sdd-autopilot/SKILL.md` | spawn contract와 Codex runtime semantics가 모인다 |
| Claude reusable execution | `.claude/agents/` | wrapper-backed execution의 실제 동작 단위를 찾는 위치다 |
| Codex reusable execution | `.codex/agents/` | custom agent spawn 대상과 parity 확인 지점이다 |
| Codex runtime prerequisite | `.codex/config.toml` | nested agent depth와 concurrency 전제가 고정된다 |
| Environment/pre-flight | `_sdd/env.md` | 로컬 작업, PR verification, pre-flight assumption의 기준이다 |
