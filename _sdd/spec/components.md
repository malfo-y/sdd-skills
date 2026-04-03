# Component Details

> 각 스킬/에이전트의 상세 정보. 카테고리 요약은 [main.md](./main.md#component-details)를 참고한다.
> 모든 컴포넌트에 Purpose(What), Why, Source(How) 트라이어드를 포함한다.

---

## sdd-autopilot

| Aspect | Description |
|--------|-------------|
| **Purpose** | 사용자 요청을 분석하여 reasoning 기반 적응형 오케스트레이터를 생성하고, 플랫폼별 에이전트 파이프라인을 end-to-end 자율 실행 |
| **Why** | 대규모 기능 구현 시 6-7개 스킬을 수동 호출하면 맥락 유실과 단계 누락 위험이 있다. sdd-autopilot이 SDD 철학을 이해하고 상황에 맞는 파이프라인을 동적으로 구성하여 사용자는 요구사항만 전달하면 된다. |
| **Input** | 사용자의 기능 요청 (자연어) |
| **Output** | 구현 완료된 코드 + 동기화된 스펙 + 활성 오케스트레이터(`.claude/skills/orchestrator_<topic>/SKILL.md` 또는 `.codex/skills/orchestrator_<topic>/SKILL.md`) + `_sdd/pipeline/log_<topic>_<ts>.md` + `_sdd/pipeline/report_<topic>_<ts>.md` + 완료 시 `_sdd/pipeline/orchestrators/<topic>_<ts>/` 아카이브 |
| **Source** | `.claude/skills/sdd-autopilot/SKILL.md` (v2.0.0) |
|            | `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`: SDD 철학 + 스킬 카탈로그 (reasoning 기반 파이프라인 구성의 핵심 입력) |
|            | `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`: 오케스트레이터 예시 |
|            | `.codex/skills/sdd-autopilot/SKILL.md` (v2.2.0) |
|            | `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`: Codex용 SDD 철학 + 스킬 카탈로그 |
|            | `docs/AUTOPILOT_GUIDE.md`: 사용 가이드 + Codex 검증 체크리스트 |
| **Process** | Step 0 (Pipeline State Detection): 기존 미완료 파이프라인 감지 → 재개/새로 시작 선택 → Phase 1 (Interactive): Step 1 Reference Loading (SDD 철학 + 스킬 카탈로그 내재화) → Step 2 요청 분석 + 인라인 discussion (시작점/종료점 감지, 산출물 스캔, Review-Fix 사이클 필수 검증) → Step 3 코드베이스 탐색 → Step 4 Reasoning 기반 오케스트레이터 생성 + Pre-flight Check(`_sdd/env.md`) → Step 5 Orchestrator Verification (구조 6항목 + 철학 6항목 = 12항목 검증, Producer-Reviewer 패턴) → Phase 1.5 (Checkpoint): 검증 결과 + 파이프라인 요약 + Pre-flight Check → 사용자 확인 → Phase 2 (Autonomous): Claude는 `.claude/agents/`, Codex는 `.codex/agents/`를 직접 사용해 자율 파이프라인 실행 (Execute -> Verify 루프) + 마일스톤 로그 (Meta + Status 테이블). 장문 planning/review 단계의 산출물은 각 producer가 inline 2-phase writing으로 직접 작성한다. 완료 후 오케스트레이터를 `_sdd/pipeline/orchestrators/<topic>_<ts>/`로 아카이브. **Hard Rule #9**: review 포함 시 review -> fix -> re-review 사이클 필수. **Hard Rule #10**: 모든 단계에 Execute -> Verify 필수. `implementation-review`는 조건부 핵심 단계 |
| **Dependencies** | 글로벌 스펙(`_sdd/spec/main.md`) 존재 필수. 스펙이 없으면 오케스트레이터 생성을 중단하고 `/spec-create` 실행을 안내 |
| **실행 형태** | 풀 스킬 (사용자 인터랙션이 핵심이므로 에이전트 전환 불필요). Codex는 generated orchestration skill이 `.codex/agents/` custom agents를 직접 spawn |
| **완료** | **Audit Trail + Taste Decision**: Step 7.2 실행 루프에서 모든 자동 결정을 로그에 기록 (판단 근거 포함). Taste decision(`[DECISION] <what> -- <why> -- <taste: yes/no>`)은 Step 8 최종 보고서에 표면화. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |

## spec-create

| Aspect | Description |
|--------|-------------|
| **Purpose** | 프로젝트 코드 분석 또는 사용자 초안을 기반으로 SDD 스펙 문서 생성 |
| **Why** | 스펙이 없으면 AI 에이전트가 일관된 코드를 생성할 수 없다. 워크플로우의 시작점으로서 Single Source of Truth를 생성하는 역할을 분리했다. |
| **Input** | 프로젝트 코드베이스, user_draft.md, 사용자 대화 |
| **Output** | `_sdd/spec/<project>.md`, CLAUDE.md, AGENTS.md, _sdd/env.md (부트스트랩) |
| **Source** | `.claude/skills/spec-create/SKILL.md` |
| **Process** | Step 1 정보 수집 → Step 2 분석 → Step 2.5 Checkpoint → Step 2.7 생성 전략 → Step 3 부트스트랩 + 작성 |
| **Dependencies** | 없음 (워크플로우 시작점) |

## feature-draft

| Aspect | Description |
|--------|-------------|
| **Purpose** | 요구사항 수집 → 스펙 패치 초안(Part 1) + 구현 계획(Part 2)을 단일 파일로 생성 |
| **Why** | 스펙 수정과 구현 계획을 별도로 진행하면 반복 작업이 발생한다. 두 산출물을 한 번에 생성하여 워크플로우 효율을 높인다. |
| **Input** | 기존 스펙, 사용자 요구사항, 코드베이스 |
| **Output** | `_sdd/drafts/feature_draft_<name>.md` |
| **Source** | `.claude/agents/feature-draft.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/feature-draft/SKILL.md` (래퍼) |
| **Process** | 7단계: 입력 분석 → 맥락 수집 → 질문 → 설계 → Part 1 → Part 2 → 저장 |
| **Dependencies** | spec-create (스펙이 있어야 Part 1 생성 가능) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |
| **완료** | **Failure Modes 테이블**: Part 1 스펙 패치에 경량 Failure Modes 테이블 섹션을 항상 포함. 간단하면 N/A 또는 1-2행, 복잡하면 3-5행 (시나리오/실패 시/사용자 가시성/처리 방안). <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |

## spec-update-todo

| Aspect | Description |
|--------|-------------|
| **Purpose** | 새 기능/요구사항을 스펙에 사전 반영 (구현 전 드리프트 방지) |
| **Why** | 구현 후에만 스펙을 업데이트하면 스펙-코드 간 드리프트가 누적된다. 사전 반영으로 스펙이 항상 의도를 정확히 반영하도록 한다. |
| **Input** | user_spec.md 또는 feature-draft Part 1 |
| **Output** | 스펙 파일 직접 수정 + 변경 요약 리포트 |
| **Source** | `.claude/agents/spec-update-todo.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/spec-update-todo/SKILL.md` (래퍼) |
| **Dependencies** | spec-create (스펙 존재 필수) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |

## spec-update-done

| Aspect | Description |
|--------|-------------|
| **Purpose** | 구현 완료 후 코드 변경사항을 스펙에 반영 |
| **Why** | 구현 과정에서 스펙과 다르게 구현된 부분을 감지하고 스펙을 최신 상태로 동기화한다. |
| **Input** | 구현 리포트, 코드 diff, 기존 스펙 |
| **Output** | 스펙 파일 업데이트 + 아카이브 |
| **Source** | `.claude/agents/spec-update-done.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/spec-update-done/SKILL.md` (래퍼) |
| **Dependencies** | implementation 완료 후 실행 |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |

## spec-review

| Aspect | Description |
|--------|-------------|
| **Purpose** | 스펙 품질 검증 + 코드-스펙 드리프트 감지 (read-only) |
| **Why** | 스펙 수정 없이 현재 상태를 객관적으로 진단하는 역할을 분리했다. 수정과 진단을 같은 스킬에서 하면 사용자가 의도치 않은 변경을 받을 위험이 있다. |
| **Input** | 스펙 파일, 코드베이스 |
| **Output** | `_sdd/spec/logs/spec_review_report.md` |
| **Source** | `.claude/agents/spec-review.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/spec-review/SKILL.md` (래퍼) |
| **판정** | SPEC_OK / SYNC_REQUIRED / NEEDS_DISCUSSION 3단계 |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |
| **완료** | **Code Analysis Metrics**: 핫스팟(자주 변경 파일), Focus Score(변경 집중도), Test Coverage(스펙 기능별 테스트 현황) 지표를 Step 3.5에 추가하여 데이터 기반 리뷰 우선순위 판단. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |

## spec-rewrite

| Aspect | Description |
|--------|-------------|
| **Purpose** | 과도하게 긴/복잡한 스펙을 8개 품질 metric과 whitepaper 기준으로 진단한 뒤 구조 재정리 (파일 분할, 부록 이동, 탐색성 개선) |
| **Why** | 스펙이 커지면 AI 에이전트가 전체를 컨텍스트에 로드하기 어렵고, 사용자도 목적/구조/사용법을 빠르게 파악하기 힘들다. `spec-rewrite`를 단순 정리 도구가 아니라 품질 진단 기반 재작성 스킬로 분리하여, readability와 spec-as-whitepaper 성질을 함께 보호한다. |
| **Input** | 기존 스펙 파일, linked sub-spec, `_sdd/spec/decision_log.md`, `_sdd/implementation/` 산출물, `docs/SDD_SPEC_DEFINITION.md` |
| **Output** | 재구성된 스펙 파일 + `_sdd/spec/logs/rewrite_report.md` |
| **Source** | `.claude/skills/spec-rewrite/SKILL.md` |
| **진단 기준** | `Component Separation`, `Findability`, `Repo Purpose Clarity`, `Architecture Clarity`, `Usage Completeness`, `Environment Reproducibility`, `Ambiguity Control`, `Why/Decision Preservation` |
| **운영 규칙** | 질문형 rubric은 `references/rewrite-checklist.md`를 canonical source로 사용하고, `spec-rewrite`는 missing whitepaper narrative를 자동 생성하지 않고 경고/보존/재배치에 집중한다. transition 기간에는 `decision_log.md`와 implementation artifact를 lowercase canonical 우선, legacy uppercase fallback으로 읽는다. |

## spec-summary

| Aspect | Description |
|--------|-------------|
| **Purpose** | 스펙의 인간 친화적 요약본 생성 |
| **Why** | 전체 스펙을 읽지 않고도 현재 프로젝트 상태를 파악하거나, 새 팀원 온보딩에 활용할 수 있도록 요약을 분리했다. |
| **Input** | 스펙 파일, 구현 진행 현황 |
| **Output** | `_sdd/spec/summary.md`, 선택적 README 블록 |
| **Source** | `.claude/skills/spec-summary/SKILL.md` |

## spec-upgrade

| Aspect | Description |
|--------|-------------|
| **Purpose** | 구 형식 스펙을 whitepaper §1-§8 구조로 변환 |
| **Why** | SDD_SPEC_DEFINITION 제정 이전에 만든 레거시 스펙을 표준 형식으로 마이그레이션하는 전용 스킬. 업그레이드와 일반 리라이트는 관심사가 다르다. |
| **Input** | 기존 스펙 파일, 코드베이스 |
| **Output** | whitepaper 형식으로 변환된 스펙 파일 |
| **Source** | `.claude/skills/spec-upgrade/SKILL.md` |

## guide-create

| Aspect | Description |
|--------|-------------|
| **Purpose** | 스펙에서 특정 기능의 구현/리뷰 가이드 문서 생성 |
| **Why** | 전체 스펙은 방대하므로, 특정 기능에 집중한 가이드를 생성하여 구현자나 리뷰어가 필요한 정보만 빠르게 참조할 수 있도록 한다. |
| **Input** | 스펙 파일, 기능명 |
| **Output** | `_sdd/guides/guide_<feature>.md` |
| **Source** | `.claude/skills/guide-create/SKILL.md` |

## implementation-plan

| Aspect | Description |
|--------|-------------|
| **Purpose** | 대규모 구현을 위한 Phase별 구현 계획 수립 |
| **Why** | 복잡한 구현을 단일 세션에서 수행하면 맥락 유실과 품질 저하가 발생한다. Target Files 기반 병렬 실행 분석으로 효율적 구현을 계획한다. |
| **Input** | 스펙, feature-draft Part 2, 코드베이스 |
| **Output** | `_sdd/implementation/implementation_plan.md` |
| **Source** | `.claude/agents/implementation-plan.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/implementation-plan/SKILL.md` (래퍼) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |
| **완료** | **Test Coverage Mapping**: Target Files에 [M] 마커가 있을 때 해당 파일의 기존 테스트 커버리지를 매핑. [C] 전용이면 스킵. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |

## implementation

| Aspect | Description |
|--------|-------------|
| **Purpose** | 구현 계획에 따른 TDD 기반 코드 작성 실행 |
| **Why** | AI 에이전트의 구현 실행을 계획에 따라 체계적으로 수행하고, Target Files 기반 병렬 Agent 실행으로 효율을 높인다. |
| **Input** | 구현 계획, 코드베이스 |
| **Output** | 구현된 코드 + `_sdd/implementation/implementation_report.md` |
| **Source** | `.claude/agents/implementation.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/implementation/SKILL.md` (래퍼) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |
| **완료** | **Verification Gate Iron Rule**: "should work" 금지, 코드 변경 후 테스트 재실행 필수, 이전 결과 재사용 금지를 Hard Rule로 추가. env.md 미존재 시 코드 분석 기반 fallback은 허용하되, `UNTESTED`는 테스트 불가 사유와 코드 분석 근거가 리포트에 명시된 경우에만 허용한다. implementation artifact는 lowercase canonical로 쓰고, transition 기간에는 legacy uppercase를 fallback input으로 허용한다. <!-- 추가됨: 2026-03-24, 보정됨: 2026-04-01 --> |
| **완료** | **Regression Iron Rule**: 기존 테스트 실패 시 테스트 업데이트 + 회귀 방지 테스트 추가를 필수 단계로 강제. 사용자 확인 없이 자동. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |
| **완료** | **Iteration Review Loop**: 모든 phase 완료 후 Skeptical Evaluator 자세로 Plan의 각 Task별 Acceptance Criteria를 재검증하고, `NOT_MET AC 관련 Task ∪ Critical/High 이슈 관련 Task`만 최대 5회까지 재실행한다. `implementation_report.md`에는 Iteration History와 필요한 `UNTESTED` 근거를 포함한다. <!-- 추가됨: 2026-04-01, 보정됨: 2026-04-01 --> |
| **완료** | **Retry Handoff Contract**: iteration 재실행 prompt에는 `failed_ac`, `failure_reason`, `open_critical_high_issues`를 반드시 포함하고, worker/sub-agent는 이전 실패를 어떻게 해소했는지 보고한다. Claude/Codex runtime 모두 동일 계약을 사용한다. <!-- 추가됨: 2026-04-01 --> |

## implementation-review

| Aspect | Description |
|--------|-------------|
| **Purpose** | 구현 계획 대비 실제 구현 진행 검증 |
| **Why** | 구현 중간/후에 계획 대비 진행률과 품질을 객관적으로 검증하여, 누락이나 이탈을 조기에 발견한다. |
| **Input** | 구현 계획, 구현 리포트, 코드 |
| **Output** | 검증 리포트 + 다음 단계 제안 |
| **Source** | `.claude/agents/implementation-review.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/implementation-review/SKILL.md` (래퍼) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |
| **완료** | **Fresh Verification**: 코드를 읽고 "맞다"가 아니라 테스트 실행 출력을 근거로 판단. "should work" 금지. 테스트 실행 불가 시(env.md 미존재) fallback 명시. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |

## pr-review

| Aspect | Description |
|--------|-------------|
| **Purpose** | PR 코드 품질 검증 + spec 존재 시 spec 기반 추가 검증(spec-patch 포함) 및 APPROVE/REQUEST CHANGES 판정 |
| **Why** | 스펙 기반 PR 리뷰를 자동화하여 일관된 품질 기준을 적용한다. 기존 pr-spec-patch를 통합하여 단일 스킬로 코드 품질 검증과 spec 검증을 함께 수행한다. |
| **Input** | PR 번호, 스펙 (존재 시) |
| **Output** | `_sdd/pr/pr_review.md` |
| **Source** | `.claude/skills/pr-review/SKILL.md` (v2.0.0) |
| **완료** | **pr-spec-patch 통합**: 기존 별도 스킬이었던 pr-spec-patch를 pr-review에 통합. from-branch에 spec 존재 시 자동으로 spec 기반 추가 검증 수행. <!-- 통합됨: 2026-04 --> |
| **완료** | **Scope Drift Detection**: PR diff 변경 파일 vs 스펙 패치 초안 범위를 비교하는 Step 2.5 pre-step 추가. CLEAN/DRIFT/MISSING 판정을 리포트 상단에 표시. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |
| **완료** | **Code Quality Fix-First**: Step 5.5로 누락된 에러 처리, 타입 불일치, 미사용 import 등을 AUTO-FIX(즉시 수정) / 목록 기록(수정 불가) 분류. 스펙 레이어 verdict(APPROVE/REQUEST CHANGES/NEEDS DISCUSSION)는 유지. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |

## discussion

| Aspect | Description |
|--------|-------------|
| **Purpose** | 구조화된 의사결정 토론 (맥락 수집 + 선택지 비교 + 결정/미결/실행항목 정리) |
| **Why** | 기술 선택, 아키텍처 결정 등 복잡한 의사결정을 구조화된 프로세스로 진행하여 결정의 품질과 추적 가능성을 높인다. |
| **Input** | 토픽, 코드베이스(선택) |
| **Output** | 토론 요약 (터미널 출력 또는 파일 저장) |
| **Source** | `.claude/skills/discussion/SKILL.md`, `.codex/skills/discussion/SKILL.md` |
| **제한** | 듀얼 플랫폼 지원. Claude Code는 `AskUserQuestion`, Codex는 `request_user_input` 기반 반복 토론 사용. discussion은 풀 스킬이므로 AskUserQuestion 유지 (에이전트 전환 대상 아님) |

## ralph-loop-init

| Aspect | Description |
|--------|-------------|
| **Purpose** | 장기 실행 프로세스(ML 트레이닝, e2e 테스트, 빌드 파이프라인, 통합 테스트 등)의 자동화 디버그 루프 디렉토리/파일 생성 |
| **Why** | 장기 실행 프로세스의 반복 디버그 루프를 표준화하여 일관된 실험/테스트 환경을 빠르게 구성한다. |
| **Input** | 프로젝트 코드, 대상 프로세스 스크립트 |
| **Output** | `ralph/` 디렉토리 (`config.sh`, `PROMPT.md`, `run.sh`, `state.md`, `CHECKS.md`) |
| **Source** | `.claude/agents/ralph-loop-init.md` (에이전트 정의, 전체 로직) |
|            | `.claude/skills/ralph-loop-init/SKILL.md` (래퍼) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |

## investigate

| Aspect | Description |
|--------|-------------|
| **Purpose** | 범용 체계적 디버깅 에이전트 (근본원인 우선, 단발성 문제 해결) |
| **Why** | 코드 문제 해결 시 체계적 프로세스 없이 임의 수정을 반복하면 근본원인을 놓치고 시간이 소모된다. 근본원인 우선(Iron Law), 3-strike 에스컬레이션, scope lock, blast radius gate, fresh verification, 독립 Agent 교차 검증을 포함하는 범용 디버깅 에이전트로 체계적 접근을 강제한다. |
| **Input** | 문제 설명, 코드베이스, 에러 로그/스택트레이스 |
| **Output** | Investigation Report (근본원인, 수정 내용, blast radius, 검증 결과, 범위 밖 발견사항) + 수정된 코드 |
| **Source** | `.claude/agents/investigate.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/investigate/SKILL.md` (래퍼) |
| **Process** | 6단계: Step 1 Problem Definition (증상/재현조건/기대동작 추출, scope lock 기준 확정) → Step 2 Evidence Collection (에러/스택트레이스/관련 코드/변경 이력 수집) → Step 3 Hypothesis & Cross-Verification (Agent A 가설 기반 + Agent B 독립 탐지 병렬 교차 검증, 단순 문제는 교차 검증 생략 가능) → Step 4 Blast Radius Assessment (변경 파일/의존 모듈/관련 테스트 나열) → Step 5 Fix & Verify (근본원인 수정 + 테스트 재실행 + 회귀 방지) → Step 6 Report |
| **Dependencies** | 없음 (독립 실행 가능) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |
| **차별점** | ralph-loop-init과 차별화: investigate는 범용/단발 문제 해결, ralph-loop-init은 장시간 반복 프로세스 전용 |

## git

| Aspect | Description |
|--------|-------------|
| **Purpose** | staged/unstaged 변경 분석 → 의미 단위 커밋 자동 생성, 브랜치 관리, 리베이스 |
| **Why** | AI 에이전트가 생성한 다수의 변경사항을 Conventional Commits 규칙에 맞게 논리적으로 묶어 커밋하려면 전용 자동화가 필요하다. |
| **Input** | git 작업 트리 상태, 사용자 지시 |
| **Output** | 커밋, 브랜치, 리베이스 등 git 작업 수행 |
| **Source** | `.claude/skills/git/SKILL.md` |
| **제한** | Claude Code 전용 (Codex 미지원) |

## spec-snapshot

| Aspect | Description |
|--------|-------------|
| **Purpose** | 현재 스펙의 타임스탬프 스냅샷 생성 + 선택적 번역 |
| **Why** | 스펙의 특정 시점 상태를 보존하거나, 다국어 팀을 위해 번역본을 생성할 때 원본 스펙을 변경하지 않고 별도 스냅샷으로 관리한다. |
| **Input** | `_sdd/spec/` 현재 파일, 대상 언어 |
| **Output** | `_sdd/snapshots/<timestamp>_<lang>/` 디렉토리에 스냅샷 복사 |
| **Source** | `.claude/skills/spec-snapshot/SKILL.md` |

## second-opinion

| Aspect | Description |
|--------|-------------|
| **Purpose** | 사용자의 질문에 대해 관련 컨텍스트를 수집·요약한 후, Codex에게 독립적인 분석을 요청하고 결과를 그대로 전달 |
| **Why** | 복잡한 설계 결정이나 디버깅에서 AI 에이전트의 단일 관점에 의존하면 편향이 발생할 수 있다. Codex를 통한 독립적 second opinion으로 다각적 분석을 제공한다. |
| **Input** | 사용자 질문, 관련 코드/파일 |
| **Output** | Codex 분석 결과 (원문 전달) |
| **Source** | `.claude/skills/second-opinion/SKILL.md` (v1.0.0) |
| **Process** | 4단계: Context Gathering → Context Packaging → Codex Forwarding (`codex:codex-rescue`) → Result Delivery |
| **제한** | Claude Code 전용 (Codex에서는 미지원). 읽기 전용 — 코드 수정 불가 |

---

## Appendix: Code Reference Index

이 프로젝트의 "코드"는 SKILL.md와 에이전트 정의 파일이다.

### 풀 스킬 (SKILL.md에 전체 로직)

| File | Skill | Referenced In |
|------|-------|---------------|
| `.claude/skills/sdd-autopilot/SKILL.md` | sdd-autopilot | Core Design, Component Details, Workflow |
| `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` | sdd-autopilot (reference) | Component Details (SDD 철학 + 스킬 카탈로그) |
| `.claude/skills/spec-create/SKILL.md` | spec-create | Core Design, Component Details |
| `.claude/skills/spec-rewrite/SKILL.md` | spec-rewrite | Component Details |
| `.claude/skills/spec-summary/SKILL.md` | spec-summary | Component Details |
| `.claude/skills/spec-upgrade/SKILL.md` | spec-upgrade | Component Details |
| `.claude/skills/guide-create/SKILL.md` | guide-create | Component Details |
| `.claude/skills/pr-review/SKILL.md` | pr-review | Component Details |
| `.claude/skills/second-opinion/SKILL.md` | second-opinion | Component Details |
| `.claude/skills/discussion/SKILL.md` | discussion | Component Details |
| `.claude/skills/git/SKILL.md` | git | Component Details |
| `.claude/skills/spec-snapshot/SKILL.md` | spec-snapshot | Component Details |

### 래퍼 스킬 + 에이전트 정의

> v3.6: 모든 래퍼 스킬의 `references/`, `examples/` 디렉토리가 삭제됨. 에이전트가 self-contained로 핵심 내용을 인라인 포함.

| Wrapper (SKILL.md) | Agent Definition | Skill | Referenced In |
|--------------------|------------------|-------|---------------|
| `.claude/skills/feature-draft/SKILL.md` | `.claude/agents/feature-draft.md` | feature-draft | Core Design, Component Details |
| `.claude/skills/implementation-plan/SKILL.md` | `.claude/agents/implementation-plan.md` | implementation-plan | Component Details |
| `.claude/skills/implementation/SKILL.md` | `.claude/agents/implementation.md` | implementation | Component Details |
| `.claude/skills/implementation-review/SKILL.md` | `.claude/agents/implementation-review.md` | implementation-review | Component Details |
| `.claude/skills/ralph-loop-init/SKILL.md` | `.claude/agents/ralph-loop-init.md` | ralph-loop-init | Component Details |
| `.claude/skills/spec-review/SKILL.md` | `.claude/agents/spec-review.md` | spec-review | Component Details |
| `.claude/skills/spec-update-done/SKILL.md` | `.claude/agents/spec-update-done.md` | spec-update-done | Component Details |
| `.claude/skills/spec-update-todo/SKILL.md` | `.claude/agents/spec-update-todo.md` | spec-update-todo | Component Details |
| `.claude/skills/investigate/SKILL.md` | `.claude/agents/investigate.md` | investigate | Component Details |

### 유틸리티 Writing Contract

| File | Skill | Referenced In |
|------|-------|---------------|
| `.claude/skills/write-phased/SKILL.md` | write-phased | Component Details |
| `.codex/skills/write-phased/SKILL.md` | write-phased | Component Details |
