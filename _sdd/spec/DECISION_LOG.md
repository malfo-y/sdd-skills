# Decision Log

## 2026-03-17 - Codex Autopilot Parity Restoration and Validation Guide Consolidation

### Context

Codex custom agent backbone과 `sdd-autopilot` 구조는 도입되었지만, Codex 쪽 autopilot 문서 세트가 Claude 원본보다 과도하게 축약되어 있었다. 특히 main skill, scale assessment, pipeline templates, sample orchestrator에서 review-fix, test strategy, error handling, final report artifact 같은 실행 계약이 충분히 드러나지 않았다. 또한 Codex dry-run 체크리스트가 `docs/CODEX_AGENT_VALIDATION.md`로 분리되어 있어 운영 가이드와 검증 가이드가 분산되어 있었다.

### Decision

1. **Codex autopilot parity 복원**: `.codex/skills/sdd-autopilot/`의 main skill, references, example을 Claude 원본 대비 의미 보존 수준으로 확장
2. **Final report artifact 명시**: Codex autopilot 산출물 계약에 `_sdd/pipeline/report_<topic>_<timestamp>.md`를 포함
3. **Validation guide 통합**: Codex dry-run 체크리스트를 `docs/AUTOPILOT_GUIDE.md`의 "Codex 검증 체크리스트" 섹션으로 흡수하고 별도 `docs/CODEX_AGENT_VALIDATION.md`는 제거
4. **Spec sync**: `_sdd/spec/main.md`에서도 Codex wrapper -> custom agent 실행 모델, autopilot report artifact, validation guide 위치를 최신 상태로 반영

### Rationale

- Codex 쪽도 실행 계약이 충분히 구체적이어야 generated orchestrator 품질과 운영 가이드를 신뢰할 수 있다
- final report artifact가 문서/예시/가이드에 모두 명시돼야 autopilot completion contract가 일관된다
- validation 체크리스트는 사용자-facing 운영 가이드 안에 있을 때 찾기 쉽고 유지보수 포인트가 줄어든다

### Changes

- `.codex/skills/sdd-autopilot/SKILL.md` -- use/do-not-use, richer execution/test/error handling, final report contract 복원
- `.codex/skills/sdd-autopilot/references/pipeline-templates.md` -- generated orchestrator minimum contract 복원
- `.codex/skills/sdd-autopilot/references/scale-assessment.md` -- 판단 프로세스, 경계 사례, examples 복원
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- review-fix, test, error handling, final report 예시 복원
- `docs/AUTOPILOT_GUIDE.md` -- Codex 검증 체크리스트 섹션 추가, validation guide 흡수
- `_sdd/spec/main.md` -- Codex wrapper/custom-agent 실행 모델, final report artifact, validation guide 위치 동기화

### References

- 드래프트: `_sdd/drafts/feature_draft_autopilot_parity_review.md`
- 드래프트: `_sdd/drafts/feature_draft_codex_agent_backbone_autopilot_parity.md`
- 구현 리포트: `_sdd/implementation/features/autopilot-parity-review/SYNC_20260317_230000_IMPLEMENTATION_REPORT.md`

## 2026-03-17 - Codex Custom Agent Backbone and Autopilot Spawn Model

### Context

초기 Codex 정렬 작업으로 `sdd-autopilot`, generated orchestration skill, `write-phased` utility 설명은 추가되었지만, 실제로 generated orchestrator가 spawn할 repo-local custom agent 레이어가 없었다. 이 상태에서는 "오케스트레이터가 실행 단위를 재사용한다"는 설명은 가능했지만, Claude Code의 `wrapper -> agent -> nested write-phased` 구조와 동등한 실행 backbone은 비어 있었다.

### Decision

1. **Codex custom agent layer 도입**: `.codex/agents/` 아래에 기존 SDD 핵심 역할 8개와 `write_phased`를 custom agent로 정의
2. **wrapper parity 채택**: `.codex/skills/*/SKILL.md`는 사용자 진입점과 handoff contract를 유지하고, 실제 spawned execution unit은 `.codex/agents/*.toml`이 담당
3. **Autopilot spawn 모델 명시**: generated orchestration skill은 skill이 아니라 custom agent를 직접 spawn
4. **nested `write_phased` 1차 범위 확정**: `feature_draft`, `implementation_plan`, `implementation_review`, `spec_review`가 장문 산출물 생성 시 `write_phased`를 nested 사용
5. **Pre-flight 확장**: `_sdd/env.md`와 `.codex/config.toml`을 함께 읽고, 최소 `agents.max_depth >= 2`를 확인

### Rationale

- custom agent 레이어가 있어야 Codex autopilot이 실제로 end-to-end 파이프라인을 실행할 수 있다
- wrapper skill을 유지해야 기존 사용자 호출 인터페이스를 깨지 않으면서 agent spawn 모델을 도입할 수 있다
- planning/review 계열은 long-form writing 품질 이득이 커서 nested `write_phased`의 우선 대상이다
- config 기반 pre-flight가 없으면 nested spawn 구조가 환경에 따라 조용히 실패할 수 있다

### Changes

- `.codex/config.toml` -- agent execution config 신규 추가
- `.codex/agents/` -- 9개 custom agent 정의 신규 추가
- `.codex/skills/feature-draft/`, `.codex/skills/implementation-plan/`, `.codex/skills/implementation/`, `.codex/skills/implementation-review/`, `.codex/skills/spec-update-done/`, `.codex/skills/spec-update-todo/`, `.codex/skills/spec-review/`, `.codex/skills/ralph-loop-init/`, `.codex/skills/write-phased/` -- wrapper/custom-agent parity 반영
- `.codex/skills/sdd-autopilot/` -- custom agent spawn 모델과 pre-flight 반영
- `_sdd/spec/main.md`, `docs/AUTOPILOT_GUIDE.md`, `docs/SDD_QUICK_START.md`, `docs/SDD_WORKFLOW.md` -- custom agent 구조 반영

### References

- 드래프트: `_sdd/drafts/feature_draft_codex_agent_backbone_autopilot_parity.md`
- 드래프트: `_sdd/drafts/feature_draft_autopilot_meta_skill.md`
- 토론: `_sdd/discussion/discussion_autopilot_meta_skill.md`
- 토론: `_sdd/discussion/discussion_write_phased_skill_design.md`

## 2026-03-17 - Codex Autopilot Orchestration and Write-Phased Utility Alignment

### Context

Claude Code용 autopilot 메타스킬과 래퍼/에이전트 구조는 이미 정리되어 있었지만, Codex 쪽에는 대응되는 `sdd-autopilot` 메타스킬과 orchestration contract가 없었다. 또한 `write-phased`는 Claude에서는 에이전트 중심 전략으로 쓰였지만, Codex에서는 공용 long-form writing utility로 어떤 스킬들이 활용해야 하는지 명확히 정리되지 않았다.

### Decision

1. **Codex `sdd-autopilot` 지원 추가**: `.codex/skills/sdd-autopilot/`를 추가하여 기존 execution skill들을 재사용하는 generated orchestration skill 패턴을 지원
2. **오케스트레이터 라이프사이클 하이브리드 정책**: 실행 중에는 `.codex/skills/orchestrator_<topic>/SKILL.md`에 활성 상태로 유지하고, 완료 후에는 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`로 아카이브
3. **Codex binding 책임 분리**: repo는 wrapper/orchestration contract만 정의하고, 실제 wrapper/agent binding은 Codex 런타임/환경 레이어 책임으로 둔다
4. **`write-phased` 승격**: Codex `write-phased`를 `spec-create`, `guide-create`, `pr-spec-patch`, `pr-review`, `spec-summary`, `spec-upgrade`, `sdd-autopilot`이 재사용하는 공용 long-form writing utility로 정의
5. **범위 제한**: `feature-draft -> write-phased` 직접 연동은 후속 최적화로 미루고 이번 결정 범위에서는 제외 **> Superseded by 2026-03-17 custom agent backbone decision: nested write_phased parity를 1차 범위에 포함**

### Rationale

- 기존에 정의한 SDD execution unit들을 유지하면서 Codex에서도 autopilot 메타스킬을 도입하는 편이 가장 낮은 전환 비용으로 구조적 일관성을 확보한다
- 활성 스킬 디렉토리와 아카이브 디렉토리를 분리하면 resume 가능성과 active skill 공간 관리 사이의 균형을 맞출 수 있다
- Codex는 Claude와 다른 orchestration/runtime 모델을 가지므로, repo-local binding까지 고정하는 것보다 contract만 명세하는 편이 유지보수성이 높다
- 긴 문서/대형 코드 출력은 write-phased의 skeleton → fill 전략을 공용 유틸리티로 재사용하는 것이 품질과 안정성에 유리하다

### Changes

- `.codex/skills/sdd-autopilot/` -- 메타스킬 신규 추가
- `.codex/skills/write-phased/` -- 공용 long-form writing utility로 역할 재정의
- `.codex/skills/feature-draft/`, `.codex/skills/implementation-plan/`, `.codex/skills/implementation/`, `.codex/skills/implementation-review/`, `.codex/skills/spec-update-done/`, `.codex/skills/spec-update-todo/`, `.codex/skills/spec-review/`, `.codex/skills/ralph-loop-init/` -- orchestration mode guidance 추가
- `.codex/skills/spec-create/`, `.codex/skills/guide-create/`, `.codex/skills/pr-spec-patch/`, `.codex/skills/pr-review/`, `.codex/skills/spec-summary/`, `.codex/skills/spec-upgrade/` -- long-form writing strategy 반영
- `docs/AUTOPILOT_GUIDE.md`, `docs/SDD_WORKFLOW.md`, `docs/SDD_QUICK_START.md`, `_sdd/spec/main.md` -- Codex autopilot/orchestrator/write-phased 설명 동기화

### References

- 드래프트: `_sdd/drafts/feature_draft_codex_autopilot_orchestration.md`
- 토론: `_sdd/discussion/discussion_autopilot_meta_skill.md`
- 토론: `_sdd/discussion/discussion_autopilot_open_questions.md`
- 토론: `_sdd/discussion/discussion_autopilot_resume_and_partial_execution.md`

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
2. **sdd-autopilot 메타스킬 추가**: 적응형 오케스트레이터를 생성하여 에이전트 파이프라인을 end-to-end 자율 실행
3. **오케스트레이터 저장 위치**: `_sdd/pipeline/`에 저장 (초기 토론에서 `.claude/skills/`로 결정했으나, 후속 토론에서 변경 — 일회성 실행 계획이므로 스킬 디렉토리 오염 방지) **> Superseded by 2026-03-17 decision: `.claude/skills/orchestrator_<topic>/SKILL.md`로 원복 (재사용성 + 재개 기능)**
4. **Codex는 기존 유지**: Agent 도구 제한으로 래퍼 패턴 불가. Codex 동기화는 별도 후속 작업 **> Superseded by 2026-03-17 decision: Codex `sdd-autopilot` + orchestration contract 지원 추가**

### Rationale

- 사용자 인터페이스(`/스킬명`) 하위 호환성 유지가 필수 → 래퍼 스킬 유지
- sdd-autopilot의 서브에이전트 호출을 위해 에이전트 레이어 필요 → Agent Wrapper 패턴
- 선행 집중형 사용자 인터랙션(Phase 1 interactive, Phase 2 autonomous) → 2-Phase Orchestration 패턴
- Discussion은 AskUserQuestion이 핵심이므로 에이전트 전환 불필요 → 스킬 유지

### Changes

- `_sdd/spec/main.md` — v2.1.0 → v3.0.0
- `.claude/agents/` — 8개 에이전트 정의 신규 생성
- `.claude/skills/*/SKILL.md` — 8개 래퍼 전환
- `.claude/skills/sdd-autopilot/` — 메타스킬 신규 생성
- `_sdd/spec/prev/PREV_main_20260316_120000.md` — 백업 생성

### References

- 토론: `_sdd/discussion/discussion_autopilot_meta_skill.md`
- 후속 토론: `_sdd/discussion/discussion_autopilot_open_questions.md`
- Feature Draft: `_sdd/drafts/feature_draft_autopilot_meta_skill.md`

## 2026-03-17 - Autopilot Resume, Partial Execution, and Enhanced Pipeline Log (v3.1.0 → v3.2.0)

### Context

sdd-autopilot이 e2e 전제로 설계되어 있어, 기존 미완료 파이프라인 재개, 기존 산출물 활용(중간 진입), 파이프라인 일부만 실행하는 시나리오가 불가능했다. 또한 오케스트레이터가 `_sdd/pipeline/`에 저장되어 스킬로서 재사용이 불가능하고, 파이프라인 로그에 구조화된 상태 추적이 없었다.

### Decision

1. **Step 0 (Pipeline State Detection) 추가**: autopilot 시작 시 `_sdd/pipeline/log_*.md`를 스캔하여 미완료 파이프라인을 감지하고, 사용자에게 재개/새로 시작 선택을 제시
2. **Step 1.4 (산출물 스캔 + 시작점/종료점 감지) 추가**: 사용자 요청에서 시작/종료 힌트를 파싱하고, `_sdd/` 기존 산출물과의 관련성을 판단하여 파이프라인 범위 조절
3. **Pipeline Log Format 강화**: Meta 섹션(request, orchestrator 참조, scale, started, pipeline) + Status 테이블(5개 상태값: pending/in_progress/completed/failed/skipped) 추가
4. **오케스트레이터 저장 위치 변경**: `_sdd/pipeline/` → `.claude/skills/orchestrator_<topic>/SKILL.md` (변경 이력: `.claude/skills/` → `_sdd/pipeline/` → `.claude/skills/`)

### Rationale

- 오케스트레이터를 `.claude/skills/`에 저장하면 스킬로서 재사용 가능하고, 재개 시 파이프라인 정의 역할을 수행할 수 있다
- 로그의 Status 테이블로 재개 시 첫 번째 미완료 스텝을 빠르게 찾을 수 있다
- 산출물 스캔으로 기존 작업 결과를 활용하여 불필요한 반복을 방지한다
- 자동 감지 + 사용자 선택 방식으로 재개를 구현하여, Phase 1이 이미 interactive이므로 질문 추가 비용이 낮다

### Changes

- `.claude/skills/sdd-autopilot/SKILL.md` -- Step 0, Step 1.4, Pipeline Log Format 강화, 오케스트레이터 경로 변경
- `_sdd/drafts/feature_draft_autopilot_meta_skill.md` -- Acceptance Criteria 추가 (재개, 부분 실행, 산출물 스캔, 로그 메타데이터)
- `_sdd/spec/main.md` -- v3.1.0 → v3.2.0

### References

- 토론: `_sdd/discussion/discussion_autopilot_resume_and_partial_execution.md`
- 후속 반영: `_sdd/discussion/discussion_autopilot_open_questions.md` (오케스트레이터 위치 결정 변경)

## 2026-03-17 - Agent Non-Interactive Conversion (AskUserQuestion 제거) (v3.0.0 → v3.1.0)

### Context

v3.0에서 8개 스킬을 에이전트로 전환했으나, 에이전트 정의 내에 AskUserQuestion 호출이 남아 있었다. sdd-autopilot의 Phase 2에서 서브에이전트로 호출할 때 사용자 인터랙션이 발생하면 파이프라인이 중단되어 자율 실행이 불가능했다.

### Decision

8개 파이프라인 에이전트(feature-draft, implementation-plan, implementation, implementation-review, ralph-loop-init, spec-review, spec-update-done, spec-update-todo)에서 AskUserQuestion을 완전 제거하고, **Autonomous Decision-Making 패턴**으로 대체한다.

### Rationale

- 서브에이전트는 부모 에이전트(sdd-autopilot)의 컨텍스트 내에서 실행되며, 사용자와 직접 인터랙션할 수 없다
- 모호한 상황에서는 가용 정보로 최선 추론 → 판단 근거를 출력에 기록 → 추론 불가 항목은 Open Questions에 남기는 3단계 전략 적용
- discussion, sdd-autopilot은 풀 스킬이므로 AskUserQuestion 유지 (사용자 인터랙션이 핵심 기능)
- 래퍼 스킬 경유 호출 시에도 에이전트가 non-interactive로 동작하지만, 부모 세션에서 사용자가 결과를 확인할 수 있으므로 문제 없음

### Changes

- `.claude/agents/feature-draft.md` -- AskUserQuestion → 자율 판단 로직
- `.claude/agents/implementation-plan.md` -- AskUserQuestion → 자율 판단 로직
- `.claude/agents/implementation-review.md` -- Tools에서 AskUserQuestion 제거
- `.claude/agents/ralph-loop-init.md` -- AskUserQuestion → 자동 선택/오류 보고
- `.claude/agents/spec-review.md` -- Tools에서 AskUserQuestion 제거
- `.claude/agents/spec-update-done.md` -- AskUserQuestion → 자동 선택/Quick Sync 전환
- `.claude-plugin/marketplace.json` -- sdd-autopilot 스킬 + 8개 에이전트 등록
- `_sdd/spec/main.md` -- v3.0.0 → v3.1.0

## 2026-03-17 - Mandatory Review-Fix Cycle (Hard Rule #9) (v3.2.0 → v3.3.0)

### Context

sdd-autopilot의 review-fix 루프가 선택적으로 동작하여, 리뷰만 실행하고 수정 없이 파이프라인이 종료되는 경우가 발생할 수 있었다. 특히 부분 파이프라인("리뷰만 해줘")이나 재개 시나리오에서 review → fix → re-review 사이클이 보장되지 않았다. 또한 `implementation-review`가 비핵심 단계로 분류되어 있어, 리뷰 실패 시 건너뛸 수 있었다.

### Decision

1. **Hard Rule #9 (Review-Fix 사이클 필수)**: 파이프라인에 review 단계가 포함되면 review → fix → re-review 사이클을 필수 실행. 전체/부분/재개 파이프라인 모두 적용
2. **implementation-review 조건부 핵심 단계 승격**: review가 포함된 파이프라인에서 `implementation-review`는 핵심 단계로 취급하며, 실패 시 건너뛸 수 없음 (최대 3회 재시도 후 실패 시 파이프라인 중단)

### Rationale

- 리뷰 없이 수정을 건너뛰면 발견된 이슈가 방치되어 품질 리스크가 누적된다
- 부분 파이프라인에서도 동일한 품질 기준을 적용하여 일관성 확보
- `implementation-review`가 비핵심이면 리뷰-수정 사이클 자체가 무력화될 수 있다

### Changes

- `.claude/skills/sdd-autopilot/SKILL.md` -- Hard Rule #9 추가, Review-Fix 루프 필수 사이클 강화, implementation-review 조건부 핵심 단계
- `.claude/skills/sdd-autopilot/references/pipeline-templates.md` -- 모든 템플릿에 Hard Rule #9 적용, 핵심 단계에 implementation-review 추가
- `_sdd/spec/main.md` -- v3.2.0 → v3.3.0
