# Changelog

> 이 파일은 `_sdd/spec/main.md`의 버전별 변경 기록이다.

#### v4.1.8 (2026-04-13)

- **spec lifecycle shared-core sync**: `spec-create`, `spec-review`, `spec-rewrite`, `spec-upgrade`의 공통 코어 4축과 스킬별 1차 추가 축을 supporting surface 설명에 반영
- **`spec-create` expected result 보정**: `/spec-create` expected result를 thin global core + single-file default 기준으로 정리하고 old canonical(`CIV`, `usage`, `decision-bearing structure`) wording 제거
- **component notes 보정**: `spec-review`에 rubric separation + evidence strictness, `spec-rewrite`에 rationale preservation + body/log placement, `spec-upgrade`에 rewrite boundary judgment를 반영
- 입력: `_sdd/drafts/2026-04-13_feature_draft_spec_lifecycle_core_checklist_alignment.md`, `_sdd/implementation/2026-04-13_implementation_review_spec_lifecycle_core_checklist_alignment.md`

#### v4.1.7 (2026-04-13)

- **spec-summary whitepaper 정렬**: `spec-summary`를 `summary.md`용 reader-facing whitepaper surface로 정리
- **section spine 반영**: `Executive Summary`, `Background / Motivation`, `Core Design`, `Code Grounding`, `Usage / Expected Results`, `Further Reading / References`를 expected result 기준으로 반영
- **appendix rule 고정**: planned/progress 정보는 관련 artifact가 있을 때만 appendix로 짧게 유지
- **supporting docs sync**: `components.md`, `usage-guide.md`, `DECISION_LOG.md`를 whitepaper semantics에 맞게 동기화
- 입력: `_sdd/drafts/2026-04-13_feature_draft_spec_summary_whitepaper_surface.md`, `_sdd/implementation/2026-04-13_implementation_review_spec_summary_whitepaper_surface.md`

#### v4.1.6 (2026-04-13)

- **spec-summary canonical overview 정렬**: `spec-summary`를 global/temporary 요약기보다 `global overview + optional planned/progress snapshot` surface로 재정의
- **summary output shape 갱신**: template/example에 `Where Details Live`를 도입하고 planned/progress snapshot을 보조 섹션으로 정리
- **supporting docs sync**: `components.md`, `usage-guide.md`, definition/workflow 문서, autopilot reasoning reference에 새 semantics 반영
- **metadata sync**: `.claude` / `.codex` `spec-summary` `skill.json` 버전을 `2.0.0`으로 정렬
- 입력: `_sdd/drafts/2026-04-13_feature_draft_spec_summary_canonical_overview_alignment.md`, `_sdd/implementation/2026-04-13_implementation_review_spec_summary_canonical_overview_alignment.md`

#### v4.1.5 (2026-04-10)

- **autopilot planning semantics sync**: non-trivial planning entry를 `feature-draft` 기본값으로, `implementation-plan`을 후속 확장 단계로 global spec에 반영
- **phase-gated execution rule 반영**: multi-phase plan을 `per-phase` review-fix + `final integration review` 실행 게이트로 정리
- **artifact naming/history invariant 반영**: lowercase canonical artifact, skill-defined dated slug output, legacy fallback read, git-history-first 추적 규칙을 global surface에 추가
- **usage guide 정렬**: autopilot active orchestrator 경로를 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`로 갱신하고 manual/auto scenario의 optional expansion path를 보정
- 입력: `ee4e1cd`, `d32686a`, `aa92c83`, `0725c25`, `_sdd/implementation/2026-04-10_implementation_review_autopilot_planning_phase_gates.md`

#### v4.1.4 (2026-04-07)

- **externalized skill cleanup**: 현재 저장소에서 제거된 독립 관리 스킬 참조를 active spec surface에서 제거
- **current surface 정리**: `main.md`, `components.md`, `usage-guide.md`가 이 저장소가 직접 관리하는 skill/workflow만 설명하도록 정리
- 백업: `_sdd/spec/prev/prev_main_20260407_184001.md`, `_sdd/spec/prev/prev_components_20260407_184001.md`, `_sdd/spec/prev/prev_usage-guide_20260407_184001.md`, `_sdd/spec/prev/prev_changelog_20260407_184001.md`
- 입력: workspace 현재 상태

#### v4.1.3 (2026-04-07)

- **Codex connector workflow output path 변경**: 외부 connector 기반 분석 workflow의 기본 저장 경로를 작업 디렉토리 기준으로 정렬
- **artifact path sync**: 관련 persistent handoff canonical path와 supporting surface의 기본 산출물 경로를 새 위치로 정렬
- 백업: `_sdd/spec/prev/prev_main_20260407_182819.md`, `_sdd/spec/prev/prev_components_20260407_182819.md`, `_sdd/spec/prev/prev_usage-guide_20260407_182819.md`, `_sdd/spec/prev/prev_changelog_20260407_182819.md`
- 입력: Codex connector workflow source

#### v4.1.2 (2026-04-07)

- **Codex connector workflow spec sync**: 새 외부 connector 기반 분석 workflow를 spec surface에 반영
- **artifact path 반영**: 관련 persistent handoff canonical path와 supporting surface reference를 확장
- **component/usage reference 확장**: component catalog와 usage scenario에 connector-backed 분석 흐름을 추가
- 백업: `_sdd/spec/prev/prev_main_20260407_180017.md`, `_sdd/spec/prev/prev_components_20260407_180017.md`, `_sdd/spec/prev/prev_usage-guide_20260407_180017.md`, `_sdd/spec/prev/prev_changelog_20260407_180017.md`
- 입력: Codex connector workflow source

#### v4.1.1 (2026-04-04)

- **components compact rewrite**: `components.md`를 category-based compact catalog로 재작성 (`284줄 -> 71줄`)
- **reference density 축소**: component별 Input/Output/Process/완료 이력 재복제를 제거하고 `Purpose / Why / Primary Source / Notes`만 유지
- **platform note 분리**: wrapper/agent split, full-skill 예외, Claude-only feature를 별도 `Platform Notes` table로 정리
- **strategic code map 유지**: 전수형 inventory는 늘리지 않고 navigation-critical appendix만 유지
- 백업: `_sdd/spec/prev/prev_components_20260404_130827.md`, `_sdd/spec/prev/prev_spec-rewrite-plan_20260404_130827.md`, `_sdd/spec/prev/prev_rewrite_report_20260404_130827.md`, `_sdd/spec/prev/prev_DECISION_LOG_20260404_130827.md`, `_sdd/spec/prev/prev_changelog_20260404_130827.md`
- 입력: `_sdd/spec/main.md`, `_sdd/spec/logs/spec-rewrite-plan.md`

#### v4.1.0 (2026-04-04)

- **global thin rewrite**: `main.md`를 3개 mandatory core 중심으로 재압축 (`257줄 -> 111줄`)
- **standalone 상세 제거**: `Contract / Invariants / Verifiability`, usage summary, decision-bearing structure 대형 표, reference/code-map appendix를 main body에서 제거
- **판단 기준 흡수 유지**: repo-wide invariant와 구조 판단은 `Guardrails`, `핵심 설계`, `주요 결정`에 압축 보존
- **supporting surface 정합성 보정**: `components.md`, `usage-guide.md` 도입부에서 legacy `§5`, `§7`, appendix 참조 제거
- 백업: `_sdd/spec/prev/prev_main_20260404_130259.md`, `_sdd/spec/prev/prev_components_20260404_130259.md`, `_sdd/spec/prev/prev_usage-guide_20260404_130259.md`, `_sdd/spec/prev/prev_DECISION_LOG_20260404_130259.md`
- 입력: `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md`, `_sdd/spec/logs/spec-rewrite-plan.md`

#### v4.0.1 (2026-04-04)

- **canonical rollout 후속 spec sync 반영**: `FD-05`~`FD-07` 구현 완료 사실을 active `_sdd/spec/` surface에 동기화
- **운영 규칙 명시**: canonical rollout/update order를 `definition -> generators/transformers -> consumers/planners -> docs -> english mirrors/examples -> audit`로 global spec에 고정
- **reference surface 확장**: `docs/en/` semantic mirror layer와 `guide-create` compact template pair를 main spec reference에 추가
- **component sync**: `spec-update-done`를 delta status 분류 + change report 기반 sync agent로, `guide-create`를 current canonical language를 재사용하는 guide generator로 설명 보정
- 백업: `_sdd/spec/prev/prev_main_20260404_021113.md`, `_sdd/spec/prev/prev_components_20260404_021113.md`, `_sdd/spec/prev/prev_changelog_20260404_021113.md`
- 입력: `_sdd/implementation/IMPLEMENTATION_PLAN.md`, `_sdd/implementation/IMPLEMENTATION_REPORT.md`, `_sdd/implementation/implementation_review.md`, `_sdd/spec/logs/spec_review_report_canonical_model_rollout.md`

#### v4.0.0 (2026-04-04)

- **current canonical global spec model로 업그레이드**: `main.md`를 canonical 1~7 + appendix 구조로 재작성
- **CIV 복구**: `Contract / Invariants / Verifiability`를 독립 표 구조로 추가하고 `_sdd/` artifact contract, wrapper/agent split, verification semantics를 명시
- **Decision-bearing structure 분리**: 시스템 경계, ownership, cross-component contract, extension point, invariant hotspot을 별도 section으로 승격
- **supporting file 역할 정리**: `components.md`를 reference-only 보조 문서로 명시하고, 전수형 code reference index를 strategic code map으로 축약
- **usage guide 정렬**: `usage-guide.md`를 section 5 보조 문서로 재정렬하고 expected result를 current model 기준으로 보정
- 백업: `_sdd/spec/prev/prev_main_20260404_015836.md`, `_sdd/spec/prev/prev_components_20260404_015836.md`, `_sdd/spec/prev/prev_usage-guide_20260404_015836.md`, `_sdd/spec/prev/prev_DECISION_LOG_20260404_015836.md`, `_sdd/spec/prev/prev_changelog_20260404_015836.md`
- 입력: `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md`

#### v3.9.1 (2026-04-03)

- **pr-spec-patch → pr-review 통합 반영**: pr-spec-patch 관련 잔존 참조 12+건 제거 (Category Overview, Artifact Map, PR 워크플로우, Directory Structure, Design Patterns, components.md, usage-guide.md, Code Reference Index)
- **second-opinion 스킬 문서화**: Claude Code 전용 second-opinion 스킬을 Category Overview, components.md, Directory Structure, Code Reference Index에 추가
- **Codex 스킬 수 수정**: 20개 → 19개 (pr-spec-patch 삭제 반영)
- **pr-review 컴포넌트 갱신**: v2.0.0 Unified PR Verification — code-only + spec-based 통합 검증으로 설명 갱신
- 백업: `_sdd/spec/prev/prev_main_20260403_103801.md`, `_sdd/spec/prev/prev_components_20260403_103801.md`, `_sdd/spec/prev/prev_usage-guide_20260403_103801.md`
- 입력: `_sdd/spec/logs/spec_review_report.md`

#### v3.9.0 (2026-04-03)

- **spec-rewrite 실행: 단일 파일 → 인덱스 + 서브 파일 구조로 전환**: main.md 1206줄을 668줄 인덱스로 경량화
- **신규 파일 3개 생성**: `components.md` (§4 Component Details + Code Reference Index, 303줄), `usage-guide.md` (§5 Usage Guide, 84줄), `logs/changelog.md` (Changelog 이동, 152줄)
- **해결 완료 이슈 정리**: #1-4, #8-16번 해결 완료 항목을 본문에서 제거 (changelog에서 추적 가능)
- **Directory Structure 갱신**: 새 파일 구조 반영
- **metric 개선**: Component Separation 2→3, Findability 2→3
- 백업: `_sdd/spec/prev/prev_main.md_20260403_000930.md`
- 진단/계획: `_sdd/spec/logs/spec-rewrite-plan.md`, `_sdd/spec/logs/rewrite_report.md`

#### v3.8.2 (2026-04-02)

- **spec-rewrite 품질 진단 강화**: `spec-rewrite`를 단순 prune/split 도구에서 8개 핵심 metric 기반 진단 후 재작성하는 스킬로 설명 갱신
- **question-style rubric 반영**: component 분리, 탐색성, 레포 목적 이해도, 아키텍처 이해도, 사용법 완결성, 환경 재현성, 모호성 통제, Why/decision 보존도를 기준 축으로 명시
- **spec-as-whitepaper 정렬**: `docs/SDD_SPEC_DEFINITION.md`를 상위 평가 기준으로 반영하고, missing whitepaper narrative는 `spec-rewrite`가 자동 생성하지 않고 경고만 남긴다는 경계 추가
- **artifact path 수정**: `rewrite_report` 경로를 `_sdd/spec/logs/rewrite_report.md`로 정정
- 백업: `_sdd/spec/prev/PREV_main_20260402_210232.md`
- 입력: `_sdd/implementation/IMPLEMENTATION_REPORT.md`, `_sdd/drafts/feature_draft_spec_rewrite_quality_rubric.md`

#### v3.8.1 (2026-04-01)

- **implementation review loop gate 보정**: `UNTESTED`를 raw PASS 상태로 두지 않고, 테스트 불가 사유 + 코드 분석 근거가 리포트에 기록된 경우에만 종료 조건에 포함되도록 정리
- **retry handoff contract 강화**: iteration 재실행 시 `failed_ac`, `failure_reason`, `open_critical_high_issues`를 다음 worker/sub-agent prompt에 필수 전달
- **Claude/Codex parity sync**: `.claude/skills/implementation/`, `.claude/agents/implementation.md`, `.codex/skills/implementation/`, `.codex/agents/implementation.toml`에 동일 review loop semantics 반영
- 백업: `_sdd/spec/prev/PREV_main_20260401_164618.md`, `_sdd/spec/prev/PREV_DECISION_LOG_20260401_164618.md`
- 입력: `_sdd/implementation/IMPLEMENTATION_REPORT.md`, `_sdd/implementation/IMPLEMENTATION_REVIEW.md`

#### v3.8.0 (2026-04-01)

- **write_skeleton 완전 제거**: `.claude/agents/write-skeleton.md`, `.codex/agents/write-skeleton.toml` 삭제
- **write-phased 재정의**: helper orchestrator가 아니라 producer-owned inline 2-phase writing contract로 역할 변경
- **current runtime 동기화**: writing helper를 전제하던 Claude/Codex caller 문구를 "직접 skeleton 작성 -> fill -> finalize" 규칙으로 치환
- **spec/runtime 정합성 수정**: 에이전트 수 10+10 -> 9+9, utility agent 설명 제거, directory structure와 component inventory를 현재 파일 구조에 맞게 갱신
- 백업: `_sdd/implementation/prev/PREV_IMPLEMENTATION_REPORT_20260401_153552.md`
- 입력: `_sdd/drafts/feature_draft_remove_write_skeleton_inline_writing.md`, `_sdd/discussion/discussion_write_skeleton_removal_and_inline_writing.md`

#### v3.7.0 (2026-03-24)

- **gstack Patterns 구현 완료 (spec-update-done)**: v3.6.1에서 계획(📋)으로 반영된 9개 결정 사항이 모두 구현되어 완료(✅)로 갱신
- **investigate 스킬 구현 완료**: `.claude/agents/investigate.md` (AC-First + self-contained, 6단계 프로세스) + `.claude/skills/investigate/SKILL.md` (래퍼) 생성. 근본원인 우선(Iron Law), 3-strike 에스컬레이션, scope lock, blast radius gate, fresh verification, Agent A/B 교차 검증 포함
- **기존 스킬 기능 구현 완료** (8개):
  - implementation: Verification Gate Iron Rule + Regression Iron Rule (Hard Rules 추가)
  - implementation-review: Fresh Verification (Hard Rule #8 추가)
  - feature-draft: Failure Modes 테이블 (Part 1 템플릿에 섹션 추가)
  - implementation-plan: Test Coverage Mapping (Step 3 뒤 조건부 하위 단계)
  - pr-review: Scope Drift Detection (Step 2.5) + Code Quality Fix-First (Step 5.5)
  - spec-review: Code Analysis Metrics (Step 3.5 + Output Format 지표 테이블)
  - sdd-autopilot: Audit Trail (Step 7.2) + Taste Decision (Step 8.2)
- **Mirror Notice 동기화 완료**: 5개 래퍼 스킬(implementation, implementation-review, feature-draft, implementation-plan, spec-review)의 SKILL.md에 에이전트 변경사항 반영
- **Identified Issues 8-16번 해결 완료로 이동**
- **investigate Component Details 상세 업데이트**: 실제 구현(6단계 프로세스, Agent A/B 교차 검증, Investigation Report 출력 형식)에 맞게 반영
- 백업: `_sdd/spec/prev/prev_main_20260324_180000.md`
- 입력: `_sdd/implementation/implementation_plan.md`, `_sdd/implementation/implementation_report.md`, `_sdd/drafts/feature_draft_gstack_patterns.md`

#### v3.6.1 (2026-03-24)

- **gstack Patterns 스펙 사전 반영 (spec-update-todo)**: feature_draft_gstack_patterns.md Part 1의 9개 결정 사항을 계획(📋) 상태로 스펙에 반영
- **신규 스킬 계획**: investigate (범용 체계적 디버깅 에이전트 + 래퍼 스킬) -- Component Details, Category Overview, Agent 목록, Directory Structure, Code Reference Index에 추가
- **기존 스킬 계획된 기능 추가** (9개):
  - sdd-autopilot: Audit Trail + Taste Decision (P1-High)
  - feature-draft: Failure Modes 테이블 (P2-Medium)
  - implementation-plan: Test Coverage Mapping (P2-Medium)
  - implementation: Verification Gate Iron Rule (P1-High), Regression Iron Rule (P2-Medium)
  - implementation-review: Fresh Verification (P1-High)
  - pr-review: Scope Drift Detection (P2-Medium), Code Quality Fix-First (P1-High)
  - spec-review: Code Analysis Metrics (P3-Low)
- **Identified Issues 섹션에 계획됨 목록 추가**: 8-16번 항목 (gstack patterns 전체)
- 백업: `_sdd/spec/prev/prev_main_20260324_120000.md`
- 입력: `_sdd/drafts/feature_draft_gstack_patterns.md` (Part 1)

#### v3.6.0 (2026-03-20)

- **AC-First + Self-Contained 전면 리팩토링**: 모든 9개 Claude agent + 11개 Claude full skill + 9개 Codex agent + 10개 Codex full skill을 AC-First 구조로 전면 재작성
  - Agent: AC 섹션 + 자체 검증 지시 + Final Check 추가, 핵심 reference 인라인 (self-contained)
  - Full Skill: AC 섹션 + 자체 검증 지시 + Final Check 추가, Best Practices/Context Management/When to Use 등 공통 bloat 제거
  - Claude agent: 4,365줄 -> 1,961줄 (55% 감축), Full skill: 5,042줄 -> 2,718줄 (46% 감축)
- **래퍼 스킬 references/examples 삭제**: Claude 9개 + Codex 8개 wrapper skill에서 미사용 references/examples 총 48개 파일 삭제
- **신규 디자인 패턴 2개**: AC-First 패턴 (AC + 자체 검증 + Final Check), Self-Contained 패턴 (핵심 reference 인라인)
- **ralph-loop-init 범용화**: "ML 트레이닝 디버그 루프" -> "장기 실행 프로세스(ML, e2e, 빌드 등) 자동화 디버그 루프"
- **SDD workflow 세부 변경**: implementation-plan Target Files 충돌 규칙 수정 (동일 파일 참조 시 마커 종류 무관하게 충돌), spec-update-todo 새 항목 기본 상태 마커 📋 명시, implementation-plan/implementation-review 리팩토링 메타 AC 삭제
- **Codex Smoke Check/Final Check 통일**: 기존 Final Smoke Check 제거, Final Check으로 통일
- **sdd-upgrade 스킬 제거 반영**: 이전에 삭제된 `sdd-upgrade` 스킬의 잔존 스펙 참조 정리 (21개 -> 20개 스킬)
- 백업: `_sdd/spec/prev/prev_main_20260320_120000.md`
- 드래프트: `_sdd/drafts/feature_draft_agent_self_containment.md`, `feature_draft_agent_self_containment_phase2.md`, `feature_draft_full_skills_ac_first.md`

#### v3.5.0 (2026-03-19)

- **sdd-autopilot v2.0.0 reasoning 리라이트**: 규모별 템플릿 매칭에서 SDD 철학 기반 reasoning + 동적 파이프라인 구성으로 전면 교체
- **Reference 파일 교체**: `references/pipeline-templates.md`, `references/scale-assessment.md` 삭제 -> `references/sdd-reasoning-reference.md` 신규 생성 (SDD 철학 + 스킬 카탈로그를 ~310줄로 압축)
- **Step 구조 변경**: Step 1(Reference Loading), Step 4(Reasoning -> Orchestrator Generation), Step 5(Orchestrator Verification) 신규 추가
- **Hard Rule #10 추가**: Execute -> Verify 필수 -- 모든 파이프라인 단계에 실행 + 검증 두 페이즈 필수
- **비오케스트레이션 스킬 재분류**: spec-create, discussion, guide-create를 autopilot 오케스트레이터 파이프라인에 넣지 않는 스킬로 명시
- **Orchestrator Template에 Reasoning Trace 섹션 추가**: 스킬 선택 근거, 순서 결정, 적용된 SDD 원칙을 기록
- **Dependencies 변경**: "스펙 없어도 실행 가능" -> "글로벌 스펙 존재 필수, 없으면 /spec-create 안내"
- **Codex 동기화**: `.codex/skills/sdd-autopilot/SKILL.md` (v2.0.1)도 동일 reasoning 아키텍처로 동기화 (Codex 차이점 보존)
- **변경**: 2-Phase Orchestration 패턴, sdd-autopilot Component Details, Design Rationale, Success Criteria, Scenario 2b, Code Reference Index 업데이트
- 백업: `_sdd/spec/prev/prev_main_20260319_120000.md`
- 토론: `_sdd/discussion/discussion_autopilot_reasoning_harness.md`

#### v3.4.1 (2026-03-17)

- **Codex autopilot parity 복원**: `.codex/skills/sdd-autopilot/`의 main skill, pipeline templates, scale assessment, sample orchestrator에 Claude 기준 실행 계약 복원
- **autopilot report artifact 명시**: `_sdd/pipeline/report_<topic>_<ts>.md`를 Artifact Map과 sdd-autopilot output contract에 반영
- **validation guide 통합**: 별도 `docs/CODEX_AGENT_VALIDATION.md` 대신 `docs/AUTOPILOT_GUIDE.md`의 "Codex 검증 체크리스트" 섹션을 운영 기준으로 사용
- **스펙 드리프트 수정**: Codex wrapper -> custom agent 실행 모델 설명과 상단 버전/산출물 설명을 최신 구조와 일치시킴

#### v3.4.0 (2026-03-17)

- **Codex custom agent backbone 도입**: `.codex/agents/`에 9개 custom agent 정의 추가 (feature_draft, implementation_plan, implementation, implementation_review, spec_update_todo, spec_update_done, spec_review, ralph_loop_init, write_phased)
- **Codex wrapper parity 강화**: 핵심 pipeline skill을 user entry wrapper로 명시하고, generated orchestrator가 custom agents를 직접 spawn하도록 모델 전환
- **nested write-phased parity**: `feature_draft`, `implementation_plan`, `implementation_review`, `spec_review`가 장문 산출물 생성 시 `write_phased`를 nested 사용하도록 구조 반영
- **Pre-flight 확장**: `_sdd/env.md`와 `.codex/config.toml`을 함께 읽어 `agents.max_depth`, `agents.max_threads` 등 실행 가능성을 점검
- **문서 갱신**: Platform Differences, Architecture Overview, AUTOPILOT_GUIDE, QUICK_START, WORKFLOW를 custom agent spawn 모델 기준으로 갱신
- 백업: 없음 (문서/구조 정렬)

#### v3.3.0 (2026-03-17)

- **Hard Rule #9 (Review-Fix 사이클 필수) 반영**: sdd-autopilot에 추가된 Hard Rule #9을 스펙에 반영 -- review 포함 파이프라인에서 review → fix → re-review 사이클 필수, 리뷰만 하고 끝나는 것 불허
- **implementation-review 단계 재분류**: "비핵심 단계"에서 "조건부 핵심 단계"로 승격 (review 포함 파이프라인에서는 핵심 단계로 취급, 실패 시 건너뛸 수 없음)
- **변경**: Common Hard Rules에 sdd-autopilot 전용 Hard Rule #9 추가, 2-Phase Orchestration 패턴 설명 보강, sdd-autopilot Process 필드 업데이트, Scenario 2b 설명 보강
- 백업: `_sdd/spec/prev/prev_main_20260317_180000.md`

#### v3.2.0 (2026-03-17)

- **sdd-autopilot 재개/부분 실행**: Step 0 (Pipeline State Detection) 추가 -- 기존 미완료 파이프라인 감지 및 재개/새로 시작 선택 지원
- **산출물 스캔 및 시작점/종료점 감지**: Step 1.4 추가 -- 사용자 요청에서 시작/종료 힌트 파싱, `_sdd/` 기존 산출물 관련성 판단으로 파이프라인 범위 조절
- **Pipeline Log Format 강화**: Meta 섹션(request, orchestrator 참조, scale, started, pipeline) + Status 테이블(5개 상태값: pending/in_progress/completed/failed/skipped) 추가
- **오케스트레이터 저장 위치 변경**: `_sdd/pipeline/` -> `.claude/skills/orchestrator_<topic>/SKILL.md` (재사용성 + 재개 기능 위해)
- **변경**: Artifact Map, Data Flow, Scenario 2b, Directory Structure 등 오케스트레이터 경로 일괄 업데이트
- 백업: `_sdd/spec/prev/prev_main_20260317_150000.md`

#### v3.1.0 (2026-03-17)

- **에이전트 non-interactive 전환**: 8개 파이프라인 에이전트에서 AskUserQuestion 완전 제거, Autonomous Decision-Making 패턴으로 대체
- **신규 디자인 패턴**: Autonomous Decision-Making 패턴 추가 (Core Design > Design Patterns)
- **변경**: 에이전트가 모호한 상황에서 자율 판단 후 근거를 출력에 기록하고, 추론 불가 항목은 Open Questions에 기록
- **변경**: marketplace.json에 sdd-autopilot 스킬 1개 + 에이전트 8개 등록
- **변경**: 스킬 디렉토리명 `autopilot` -> `sdd-autopilot` 리네임
- **변경**: Platform Differences 테이블에서 AskUserQuestion이 풀 스킬에서만 사용됨을 명시
- 백업: `_sdd/spec/prev/prev_main_20260317_120000.md`

#### v3.0.0 (2026-03-16)

- **아키텍처 변경**: 스킬 전용 → 스킬 + 에이전트 이중 아키텍처(dual architecture) 전환
- **신규**: sdd-autopilot 적응형 오케스트레이터 메타스킬 추가 (`.claude/skills/sdd-autopilot/`)
- **신규**: 8개 에이전트 정의 파일 생성 (`.claude/agents/`)
- **변경**: 8개 스킬을 Agent Wrapper 래퍼로 전환 (feature-draft, implementation-plan, implementation, implementation-review, ralph-loop-init, spec-review, spec-update-done, spec-update-todo)
- **신규**: `_sdd/pipeline/` 오케스트레이터 + 파이프라인 로그 시스템 설계
- **신규**: `docs/AUTOPILOT_GUIDE.md` sdd-autopilot 사용 가이드 추가
- **신규**: `_sdd/env.md`에 SDD-Autopilot Resources 섹션 추가
- **신규 디자인 패턴**: Agent Wrapper 패턴, 2-Phase Orchestration 패턴 추가
- 스킬 수: 19 → 20 (sdd-autopilot 추가), 에이전트 수: 1 → 9 (8개 파이프라인 에이전트 + write-phased)
- 백업: `_sdd/spec/prev/prev_main_20260316_120000.md`

#### v2.1.0 (2026-03-13)

- spec-create, spec-rewrite, spec-upgrade에 2-Phase Generation 패턴 추가
- 3개 미문서 스킬 추가 (spec-snapshot, guide-create, write-phased)
