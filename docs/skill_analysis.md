# SDD 스킬 에코시스템 분석 문서

**작성일**: 2026-03-04
**대상**: SDD Skills 12개 (deprecated 4개 제거 후)
**분석 기준**: Purpose 4개 + Orchestration 7개 = 11개 기준

> **제거된 스킬 (deprecated)**:
> - `feature-draft-sequential` — `feature-draft`가 대체
> - `implementation-sequential` — `implementation`이 대체
> - `implementation-plan-sequential` — `implementation-plan`이 대체
> - `spec-draft` — `feature-draft`에 흡수

---

## 섹션 1: SDD 스킬 에코시스템 개요

### SDD(Spec-Driven Development)란?

SDD는 **스펙 문서를 Single Source of Truth**로 사용하는 개발 방법론이다. 스펙을 먼저 작성하고, 스펙에 기반하여 구현 계획을 세우고, TDD로 구현한 후, 구현 결과를 다시 스펙에 동기화하는 순환 구조를 갖는다.

### 스킬의 역할

각 스킬은 **Claude Code / Codex 환경에서 multi sub-agent를 오케스트레이션하는 프롬프트**이다. SKILL.md 파일이 스킬의 동작 방식, 입출력, 프로세스를 정의하며, LLM이 이를 읽고 해당 워크플로우를 실행한다.

### 전체 워크플로우 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│                    Core 4-Step Workflow                       │
│                                                              │
│  spec-create → feature-draft → implementation → spec-update-done │
│     (Step 1)     (Step 2)       (Step 3)         (Step 4)    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    PR Workflow                                │
│                                                              │
│  implementation → PR → pr-spec-patch → pr-review →           │
│  spec-update-todo                                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              Standalone Review / Audit                        │
│                                                              │
│  spec-review: 스펙 품질 감사 (read-only)                      │
│  spec-rewrite: 스펙 구조 개편                                 │
│  spec-summary: 스펙 요약 생성                                 │
│  implementation-review: 구현 진행 리뷰 (standalone audit)     │
│  implementation-plan: 독립 구현 계획                          │
└─────────────────────────────────────────────────────────────┘
```

### 12개 스킬 목적 요약

| # | 스킬 | 카테고리 | 목적 |
|---|------|----------|------|
| 1 | `spec-create` | Core Step 1 | 초기 스펙 문서 생성 |
| 2 | `feature-draft` | Core Step 2 | 스펙 패치 + 구현 계획 (Target Files 포함) ✅ 개선 완료 |
| 3 | `implementation` | Core Step 3 | TDD 병렬 실행 (sub-agent dispatch) ✅ 참조 구현 |
| 4 | `spec-update-done` | Core Step 4 | 스펙-코드 동기화, 아카이브 |
| 5 | `implementation-plan` | Standalone Planning | 독립 구현 계획 (Target Files 포함) |
| 6 | `implementation-review` | Standalone Review | 구현 진행 리뷰 (standalone audit) |
| 7 | `spec-review` | Standalone Audit | 스펙 품질 감사 (read-only, no edits) |
| 8 | `spec-rewrite` | Standalone Audit | 스펙 구조 개편 (prune, split, report) |
| 9 | `spec-summary` | Standalone Audit | 스펙 요약 생성 (SUMMARY.md + optional README) |
| 10 | `spec-update-todo` | Spec Input | 스펙 업데이트 (user input → spec 반영, PR workflow에서 사용) |
| 11 | `pr-spec-patch` | PR Workflow | PR → 스펙 패치 초안 생성 |
| 12 | `pr-review` | PR Workflow | PR 스펙 기반 검증 + 판정 |

---

## 섹션 2: 분석 기준 + 스킬별 분석

### 분석 기준 (2개 차원, 11개 기준)

| ID | 차원 | 기준 | 설명 |
|----|------|------|------|
| **P1** | Purpose | 목적 명확성 | Overview, When to Use 섹션이 명확한가 |
| **P2** | Purpose | 출력 포맷 명세 | Output 형식이 구체적으로 정의되어 있는가 |
| **P3** | Purpose | Hard Rules 명시 | 스펙 read-only 등 불변 규칙이 명시되어 있는가 |
| **P4** | Purpose | 워크플로우 위치 | 전체 워크플로우에서의 위치가 명시되어 있는가 |
| **O1** | Orchestration | Step별 도구 매핑 | 각 Step에서 사용할 도구(Read, Glob, codebase-retrieval 등)가 명시되어 있는가 |
| **O2** | Orchestration | Decision Gates | IF/ELSE 분기로 다음 단계 진입 조건이 정의되어 있는가 |
| **O3** | Orchestration | 체크포인트 | 사용자 확인(AskUserQuestion) 포인트가 정의되어 있는가 |
| **O4** | Orchestration | 검증 방법 | Glob/Grep 기반 파일 존재 검증 등 구체적 검증 로직이 있는가 |
| **O5** | Orchestration | 컨텍스트 관리 | 스펙/코드 크기별 읽기 전략이 정의되어 있는가 |
| **O6** | Orchestration | 점진적 공개 | 사용자에게 요약→상세 순으로 제시하는 전략이 있는가 |
| **O7** | Orchestration | 에러 복구 | 에러 상황별 대응 테이블이 정의되어 있는가 |

### 평가 기호

- ✅ 충분히 구현됨
- ⚠️ 부분적 / 개선 여지 있음
- ❌ 미구현 또는 누락

---

### 1. `spec-create` — 초기 스펙 생성 ✅ 개선 완료

| 기준 | 평가 | 근거 |
|------|------|------|
| P1 목적 명확성 | ✅ | Overview, When to Use 섹션 명확 |
| P2 출력 포맷 | ✅ | 상세 템플릿 제공 (Goal, Architecture, Components 등) |
| P3 Hard Rules | ✅ | Hard Rules 섹션 추가 (한국어 작성, 출력 위치, 기존 코드 수정 금지 등) |
| P4 워크플로우 위치 | ✅ | Step 1 of 4 명시, 테이블 제공 |
| O1 도구 매핑 | ✅ | Step 1-3 도구 매핑 추가 (Read, Glob, codebase-retrieval, AskUserQuestion 등) |
| O2 Decision Gates | ✅ | Decision Gate 1→2, 2→3 추가 — IF/ELSE 분기 정의 |
| O3 체크포인트 | ✅ | Step 2.5 Checkpoint 추가 — 스펙 초안 사용자 확인 |
| O4 검증 방법 | ✅ | Glob 검증 추가 — 출력 파일 존재 확인 로직 |
| O5 컨텍스트 관리 | ✅ | Context Management 테이블 추가 — 크기별 읽기 전략 정의 |
| O6 점진적 공개 | ✅ | Progressive Disclosure 추가 — 요약→상세 순서 제시 전략 |
| O7 에러 복구 | ✅ | Error Handling 테이블 추가 — 상황별 대응 정의 |

**핵심 발견**: 목적과 출력 포맷이 잘 정의되어 있고, 오케스트레이션 패턴(P3, O1-O7) 전파 완료로 11/11 달성.

---

### 2. `feature-draft` — 스펙 패치 + 구현 계획 ✅ 개선 완료

| 기준 | 평가 | 근거 |
|------|------|------|
| P1 목적 명확성 | ✅ | Overview, When to Use, 3스킬 통합 설명 명확 |
| P2 출력 포맷 | ✅ | Part 1 (Spec Patch) + Part 2 (Implementation Plan) 상세 템플릿 |
| P3 Hard Rules | ✅ | 6개 Hard Rules 명시 (read-only, 출력 위치, 한국어, Target Files 등) |
| P4 워크플로우 위치 | ✅ | Step 2 of 4 명시 |
| O1 도구 매핑 | ✅ | 각 Step에 Tools 명시 (Read, Glob, Bash, codebase-retrieval, AskUserQuestion) |
| O2 Decision Gates | ✅ | Gate 1→2, 3→4, 4→5, 6→7 정의 (IF/ELSE 의사코드) |
| O3 체크포인트 | ✅ | Step 5.5 (Part 1 Checkpoint), Step 7 (Review & Confirm) |
| O4 검증 방법 | ✅ | Step 7에서 Glob 기반 Target Files 검증 ([M]→존재확인, [C]→미존재확인) |
| O5 컨텍스트 관리 | ✅ | 스펙/코드 크기별 읽기 전략 테이블 (4단계) |
| O6 점진적 공개 | ✅ | 요약 테이블 먼저 → 상세 요청 시 해당 섹션만 출력 |
| O7 에러 복구 | ✅ | 8개 상황별 에러 테이블 |

**핵심 발견**: 7가지 오케스트레이션 개선이 모두 적용된 참조 구현. 모든 기준에서 ✅.

---

### 3. `implementation` — TDD 병렬 실행 ✅ 참조 구현

| 기준 | 평가 | 근거 |
|------|------|------|
| P1 목적 명확성 | ✅ | Overview, Quick Start 명확 |
| P2 출력 포맷 | ✅ | Progress Summary, Quality Assessment, Phase/Final Report 템플릿 |
| P3 Hard Rules | ✅ | "Hard Rule: Never Modify Spec Files" 명시 |
| P4 워크플로우 위치 | ✅ | Step 3 of 4 명시 |
| O1 도구 매핑 | ✅ | Sub-agent dispatch (Task tool), codebase-retrieval, AskUserQuestion |
| O2 Decision Gates | ✅ | Step 3 Target Files 유무 분기, Step 6.4 Phase Decision Gate, Step 7.2 Final Gate |
| O3 체크포인트 | ✅ | Step 3.5 Parallelization Plan 사용자 제시, AskUserQuestion 포인트 목록 |
| O4 검증 방법 | ✅ | Step 5 Post-Group 검증 (전체 테스트, Unplanned Dependencies, 파일 무결성) |
| O5 컨텍스트 관리 | ⚠️ | env.md 기반 환경 관리는 있으나 스펙/코드 크기별 읽기 전략은 없음 |
| O6 점진적 공개 | ✅ | 병렬 실행 계획 요약 → Phase 진행 → Final Report |
| O7 에러 복구 | ✅ | Sub-agent 실패, 파일 위반, Unplanned Dependency 등 상세 복구 로직 |

**핵심 발견**: 병렬 실행 오케스트레이션이 매우 상세하다. 컨텍스트 관리(스펙 크기별 읽기 전략)만 추가하면 완벽.

---

### 4. `spec-update-done` — 스펙-코드 동기화 ✅ 개선 완료

| 기준 | 평가 | 근거 |
|------|------|------|
| P1 목적 명확성 | ✅ | Overview, When to Use, 다양한 Input Sources 명세 |
| P2 출력 포맷 | ✅ | Change Report, Updated Spec, Archive 포맷 정의 |
| P3 Hard Rules | ✅ | Hard Rules 섹션 추가 (업데이트 범위, 백업 필수, 사용자 승인 규칙 등) |
| P4 워크플로우 위치 | ✅ | Step 4 of 4 명시 |
| O1 도구 매핑 | ✅ | 6개 Step 도구 매핑 추가 (Read, Glob, Bash, git diff, codebase-retrieval 등) |
| O2 Decision Gates | ✅ | Decision Gate 1→2, 3→4, 5→6 추가 — IF/ELSE 분기 정의 |
| O3 체크포인트 | ✅ | "Report before changing" 원칙, 사용자 승인 후 적용 |
| O4 검증 방법 | ✅ | Step 5 Validate Updates (파일 경로, 의존성, API 매치 검증) |
| O5 컨텍스트 관리 | ✅ | Context Management 테이블 추가 — 크기별 읽기 전략 정의 |
| O6 점진적 공개 | ✅ | Progressive Disclosure 강화 — 요약→상세 단계 명확화 |
| O7 에러 복구 | ✅ | Error Handling 테이블 추가 — 상황별 대응 정의 |

**핵심 발견**: 다양한 입력 소스와 검증 프로세스가 있다. P3, O1, O2, O5-O7 개선으로 11/11 달성.

---

### 5. `implementation-plan` — 독립 구현 계획 ✅ 개선 완료

| 기준 | 평가 | 근거 |
|------|------|------|
| P1 목적 명확성 | ✅ | Overview, When to Ask 섹션 명확 |
| P2 출력 포맷 | ✅ | Plan Output Format 상세 템플릿 (Parallel Execution Summary 포함) |
| P3 Hard Rules | ✅ | "Hard Rule: Spec Documents Are Read-Only" 명시 |
| P4 워크플로우 위치 | ✅ | Standalone이나 워크플로우 연결 설명 있음 |
| O1 도구 매핑 | ✅ | 5개 Step 도구 매핑 추가 (Read, Glob, Bash, codebase-retrieval 등) |
| O2 Decision Gates | ✅ | Decision Gate 1→2, 3→4, 4→5 추가 — IF/ELSE 분기 정의 |
| O3 체크포인트 | ✅ | Step 3.5 Checkpoint 추가 — 구현 계획 초안 사용자 확인 |
| O4 검증 방법 | ✅ | Glob Target Files 검증 강화 — [M]/[C] 존재 확인 로직 |
| O5 컨텍스트 관리 | ✅ | Context Management 테이블 추가 — 크기별 읽기 전략 정의 |
| O6 점진적 공개 | ✅ | Progressive Disclosure 추가 — 요약→상세 순서 제시 전략 |
| O7 에러 복구 | ✅ | Error Handling 테이블 추가 — 상황별 대응 정의 |

**핵심 발견**: Target Files 스펙이 잘 정의되어 있고 feature-draft 패턴 이식 완료. O1-O7 모두 개선으로 11/11 달성.

---

### 6. `implementation-review` — 구현 진행 리뷰 ✅ 개선 완료

| 기준 | 평가 | 근거 |
|------|------|------|
| P1 목적 명확성 | ✅ | Overview, When to Use, 5단계 Review Process 다이어그램 |
| P2 출력 포맷 | ✅ | Review Output Template 상세 (Progress, Assessment, Issues, Recommendations) |
| P3 Hard Rules | ✅ | 스펙 수정 금지 Hard Rule (한국어로 명시) |
| P4 워크플로우 위치 | ✅ | Standalone audit 역할 설명 |
| O1 도구 매핑 | ✅ | 5개 Step 도구 매핑 추가 (Read, Glob, Bash, codebase-retrieval 등) |
| O2 Decision Gates | ✅ | Decision Gate 1→2, 2→3, severity-based 3→4 추가 — IF/ELSE 분기 정의 |
| O3 체크포인트 | ✅ | Step 2.5 Checkpoint 추가 — 중간 사용자 확인 포인트 |
| O4 검증 방법 | ✅ | Step 2-3에서 코드 검증, 테스트 검증, Acceptance Criteria 검증 상세 |
| O5 컨텍스트 관리 | ✅ | Context Management 테이블 추가 — 크기별 읽기 전략 정의 |
| O6 점진적 공개 | ✅ | Quick Review Mode → Full Review 2단계 제공 |
| O7 에러 복구 | ✅ | Error Handling 테이블 추가 — 상황별 대응 정의 |

**핵심 발견**: 검증 프로세스가 상세하고 Quick/Full 모드가 좋다. O1, O2, O3, O5, O7 개선으로 11/11 달성.

---

### 7. `spec-review` — 스펙 품질 감사 ✅ 개선 완료

| 기준 | 평가 | 근거 |
|------|------|------|
| P1 목적 명확성 | ✅ | Overview (2개 차원 설명), When to Use 명확 |
| P2 출력 포맷 | ✅ | Report Format 상세 (Severity, Drift Notes, Decision Log Follow-ups) |
| P3 Hard Rules | ✅ | "Hard Rule: No Spec Edits" 명시 + Guardrails 섹션 |
| P4 워크플로우 위치 | ✅ | Integration 섹션에서 관련 스킬 연결 |
| O1 도구 매핑 | ✅ | 5개 Step 도구 매핑 추가 (Read, Glob, Bash, codebase-retrieval, git diff 등) |
| O2 Decision Gates | ✅ | Step 4에서 SPEC_OK / SYNC_REQUIRED / NEEDS_DISCUSSION 판정 |
| O3 체크포인트 | ✅ | Step 3.5 Drift Checkpoint 추가 — 중간 사용자 확인 포인트 |
| O4 검증 방법 | ✅ | 6가지 Drift 유형 검증 (Architecture, Feature, API, Config, Issue, Decision-log) |
| O5 컨텍스트 관리 | ✅ | Context Management 테이블 추가 — 크기별 읽기 전략 정의 |
| O6 점진적 공개 | ✅ | Progressive Disclosure 강화 — Severity별 단계적 제시 전략 추가 |
| O7 에러 복구 | ✅ | Error Handling 테이블 추가 — 상황별 대응 정의 |

**핵심 발견**: 3단계 판정(SPEC_OK/SYNC_REQUIRED/NEEDS_DISCUSSION)이 좋은 Decision Gate 패턴. O1, O3, O5-O7 개선으로 11/11 달성.

---

### 8. `spec-rewrite` — 스펙 구조 개편 ✅ 개선 완료

| 기준 | 평가 | 근거 |
|------|------|------|
| P1 목적 명확성 | ✅ | Overview (3가지 목표), When to Use 명확 |
| P2 출력 포맷 | ✅ | Rewrite Report 포맷 + Quality Checklist |
| P3 Hard Rules | ✅ | Hard Rules 섹션 추가 (백업 필수, 구조 변경 범위, 사용자 승인 규칙 등) |
| P4 워크플로우 위치 | ✅ | Integration 섹션에서 관련 스킬 연결 |
| O1 도구 매핑 | ✅ | 6개 Step 도구 매핑 추가 (Read, Glob, Bash, codebase-retrieval 등) |
| O2 Decision Gates | ✅ | Decision Gate IF/ELSE 강화 — Step 전환 조건 명시 |
| O3 체크포인트 | ✅ | Step 2 "Propose Rewrite Plan First" — 사용자 확인 후 진행 |
| O4 검증 방법 | ✅ | Quality Checklist (6개 항목) |
| O5 컨텍스트 관리 | ✅ | Context Management 테이블 추가 — 크기별 읽기 전략 정의 |
| O6 점진적 공개 | ✅ | Rewrite Plan 제안 → 사용자 확인 → 실행 순서 |
| O7 에러 복구 | ✅ | Error Handling 테이블 추가 — 상황별 대응 정의 |

**핵심 발견**: "Plan First" 패턴이 좋은 체크포인트 사례. P3, O1, O2, O5, O7 개선으로 11/11 달성.

---

### 9. `spec-summary` — 스펙 요약 생성 ✅ 개선 완료

| 기준 | 평가 | 근거 |
|------|------|------|
| P1 목적 명확성 | ✅ | Overview, When to Use, Trigger Phrases 매우 상세 |
| P2 출력 포맷 | ✅ | 6개 섹션 상세 템플릿 (Executive Summary, Features, Architecture, Dashboard, Issues, Next Steps) |
| P3 Hard Rules | ✅ | Hard Rules 섹션 추가 (read-only 원칙, 출력 위치, 마커 규칙 등) |
| P4 워크플로우 위치 | ✅ | Integration 다이어그램 + Trigger Points 상세 |
| O1 도구 매핑 | ✅ | 6개 Step 도구 매핑 추가 (Read, Glob, codebase-retrieval 등) |
| O2 Decision Gates | ✅ | Decision Gate 1→2, 5→6 추가 — IF/ELSE 분기 정의 |
| O3 체크포인트 | ✅ | Step 4.5 Checkpoint 추가 — 요약 초안 사용자 확인 |
| O4 검증 방법 | ✅ | Glob 검증 강화 — 자동 검증 로직 추가 |
| O5 컨텍스트 관리 | ⚠️ | Split spec 처리 전략은 있으나 크기별 읽기 전략이 아닌 구조적 전략 |
| O6 점진적 공개 | ✅ | "Layered Information" 원칙 — Executive Summary → Technical Details |
| O7 에러 복구 | ✅ | 8개 상황별 에러 테이블 (가장 상세한 수준) |

**핵심 발견**: P3, O1-O4 개선으로 10/11 달성. O5는 구조적 전략(⚠️)으로 유지 — 크기별 읽기 전략보다 split spec 구조 전략이 이 스킬에 적합.

---

### 10. `spec-update-todo` — 스펙 업데이트 ✅ 개선 완료

| 기준 | 평가 | 근거 |
|------|------|------|
| P1 목적 명확성 | ✅ | Overview, When to Use, Input Sources 명확 |
| P2 출력 포맷 | ✅ | Update Summary, Update Templates 상세 |
| P3 Hard Rules | ✅ | Hard Rules 섹션 추가 (스펙 수정 범위, 백업 규칙 등) |
| P4 워크플로우 위치 | ✅ | PR workflow에서의 역할 명시 |
| O1 도구 매핑 | ✅ | 7개 Step 도구 매핑 추가 (Read, Glob, Bash, codebase-retrieval 등) |
| O2 Decision Gates | ✅ | Decision Gate 1→2, 5→6 추가 — IF/ELSE 분기 정의 |
| O3 체크포인트 | ✅ | Step 5 Generate Update Plan → 사용자 확인 → Step 6 Apply |
| O4 검증 방법 | ✅ | Post-Update Glob 검증 추가 — 자동 검증 로직 강화 |
| O5 컨텍스트 관리 | ✅ | Context Management 테이블 추가 — 크기별 읽기 전략 정의 |
| O6 점진적 공개 | ✅ | Update Plan 먼저 제시 → 사용자 승인 → Apply |
| O7 에러 복구 | ✅ | 4개 상황별 에러 테이블 |

**핵심 발견**: "Update Plan → Approve → Apply" 패턴이 좋은 체크포인트 사례. P3, O1, O2, O4, O5 개선으로 11/11 달성.

---

### 11. `pr-spec-patch` — PR → 스펙 패치 생성 ✅ 개선 완료

| 기준 | 평가 | 근거 |
|------|------|------|
| P1 목적 명확성 | ✅ | Overview, When to Use, 2개 Mode (Initial/Update) 설명 |
| P2 출력 포맷 | ✅ | Output Format 매우 상세 (PR Summary, Patch Content, Questions, Metadata) |
| P3 Hard Rules | ✅ | "Hard Rule: This skill does NOT modify specs" 명시 |
| P4 워크플로우 위치 | ✅ | PR Workflow 다이어그램 |
| O1 도구 매핑 | ✅ | gh CLI 명령어 구체 명시 (gh pr view, gh pr diff) |
| O2 Decision Gates | ✅ | Decision Gate 3→4, 4→5 추가 — Step 내부 IF/ELSE 강화 |
| O3 체크포인트 | ✅ | Mode 2에서 사용자 의도 확인 (Refine/Resolve/Add/Remove/Regenerate/Finalize) |
| O4 검증 방법 | ✅ | Step 5.5 PR Evidence 검증 추가 — 출력 검증 로직 강화 |
| O5 컨텍스트 관리 | ✅ | Context Management + PR 크기별 전략 테이블 추가 |
| O6 점진적 공개 | ✅ | Summary → Highlight → Guide next steps |
| O7 에러 복구 | ✅ | 7개 Edge Cases + 6개 Error Handling 테이블 |

**핵심 발견**: gh CLI 도구 매핑이 좋은 O1 사례. O2 Decision Gate, O4 PR Evidence 검증, O5 Context Management 개선으로 11/11 달성.

---

### 12. `pr-review` — PR 스펙 기반 검증 ✅ 개선 완료

| 기준 | 평가 | 근거 |
|------|------|------|
| P1 목적 명확성 | ✅ | Overview, When to Use, 2개 Mode (Preferred/Degraded) |
| P2 출력 포맷 | ✅ | PR_REVIEW.md 매우 상세 (Verdict, Metrics, Acceptance, Compliance, Gap, Recommendations) |
| P3 Hard Rules | ✅ | "Hard Rule: This skill does NOT modify specs" 명시 |
| P4 워크플로우 위치 | ✅ | PR Workflow 다이어그램 |
| O1 도구 매핑 | ✅ | gh CLI 명령어 구체 명시 |
| O2 Decision Gates | ✅ | Step 6 Verdict 판정 (APPROVE/REQUEST CHANGES/NEEDS DISCUSSION) 조건 테이블 |
| O3 체크포인트 | ✅ | Step 4.5 Checkpoint 추가 — 중간 사용자 확인 포인트 |
| O4 검증 방법 | ✅ | Step 3-5 상세 검증 (Acceptance Criteria, Spec Compliance, Gap Analysis) |
| O5 컨텍스트 관리 | ✅ | Context Management + PR 크기별 전략 테이블 추가 |
| O6 점진적 공개 | ✅ | Progressive Disclosure 강화 — 사용자 선택적 공개 전략 추가 |
| O7 에러 복구 | ✅ | 8개 Edge Cases + 6개 Error Handling 테이블 |

**핵심 발견**: Verdict 판정 시스템이 좋은 Decision Gate 패턴. O3 Checkpoint, O5 Context Management, O6 Progressive Disclosure 개선으로 11/11 달성.

---

## 섹션 3: 요약 매트릭스 + 우선순위 권고

### 12×11 매트릭스

| 스킬 | P1 | P2 | P3 | P4 | O1 | O2 | O3 | O4 | O5 | O6 | O7 | ✅ | ⚠️ | ❌ |
|------|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| spec-create | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** | 0 | 0 |
| **feature-draft** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** | 0 | 0 |
| **implementation** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | **10** | 1 | 0 |
| spec-update-done | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** | 0 | 0 |
| impl-plan | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** | 0 | 0 |
| impl-review | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** | 0 | 0 |
| spec-review | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** | 0 | 0 |
| spec-rewrite | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** | 0 | 0 |
| spec-summary | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | **10** | 1 | 0 |
| spec-update-todo | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** | 0 | 0 |
| pr-spec-patch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** | 0 | 0 |
| pr-review | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** | 0 | 0 |

### 기준별 충족률

| 기준 | ✅ 수 | ⚠️ 수 | ❌ 수 | 충족률 | 이전 |
|------|-------|-------|-------|--------|------|
| P1 목적 명확성 | 12 | 0 | 0 | **100%** | 100% |
| P2 출력 포맷 | 12 | 0 | 0 | **100%** | 100% |
| P3 Hard Rules | 12 | 0 | 0 | **100%** | 67% |
| P4 워크플로우 위치 | 12 | 0 | 0 | **100%** | 100% |
| O1 도구 매핑 | 12 | 0 | 0 | **100%** | 33% |
| O2 Decision Gates | 12 | 0 | 0 | **100%** | 33% |
| O3 체크포인트 | 12 | 0 | 0 | **100%** | 50% |
| O4 검증 방법 | 12 | 0 | 0 | **100%** | 58% |
| O5 컨텍스트 관리 | 10 | 2 | 0 | **83%** | 8% |
| O6 점진적 공개 | 12 | 0 | 0 | **100%** | 58% |
| O7 에러 복구 | 12 | 0 | 0 | **100%** | 58% |

### 핵심 인사이트

1. **Purpose 차원(P1-P4)**: 평균 100% 충족 — 모든 스킬이 목적, 포맷, Hard Rules, 워크플로우 위치를 완전히 정의
2. **Orchestration 차원(O1-O7)**: 평균 97.6% 충족 (이전 43%) — feature-draft/implementation 패턴 전파 완료
3. **유일한 미충족**: O5 컨텍스트 관리 83% — `implementation`(env.md 기반)과 `spec-summary`(구조적 전략)가 ⚠️ 유지
4. **개선 효과**: 10개 스킬에 오케스트레이션 패턴을 전파하여 전체 평균이 65% → 99.2%로 상승

### 우선순위별 개선 권고 — 개선 완료 현황

#### Tier 1: 긴급 (Core Workflow 스킬) — ✅ 완료

| 스킬 | 이전 점수 | 현재 점수 | 상태 |
|------|----------|----------|------|
| `spec-create` | 3/11 | **11/11** ✅ | 완료 — P3, O1-O7 모두 개선 |
| `spec-update-done` | 5/11 | **11/11** ✅ | 완료 — P3, O1, O2, O5-O7 개선 |

#### Tier 2: 중요 (활발히 사용되는 스킬) — ✅ 완료

| 스킬 | 이전 점수 | 현재 점수 | 상태 |
|------|----------|----------|------|
| `implementation-plan` | 4/11 | **11/11** ✅ | 완료 — O1-O7 모두 개선 |
| `implementation-review` | 6/11 | **11/11** ✅ | 완료 — O1, O2, O3, O5, O7 개선 |
| `spec-review` | 6/11 | **11/11** ✅ | 완료 — O1, O3, O5-O7 개선 |

#### Tier 3: 낮음 (Standalone / 이미 양호) — ✅ 완료

| 스킬 | 이전 점수 | 현재 점수 | 상태 |
|------|----------|----------|------|
| `spec-update-todo` | 6/11 | **11/11** ✅ | 완료 — P3, O1, O2, O4, O5 개선 |
| `spec-rewrite` | 6/11 | **11/11** ✅ | 완료 — P3, O1, O2, O5, O7 개선 |
| `spec-summary` | 5/11 | **10/11** ✅ | 완료 — P3, O1-O4 개선 (O5는 ⚠️ 유지) |
| `pr-spec-patch` | 8/11 | **11/11** ✅ | 완료 — O2, O4, O5 개선 |
| `pr-review` | 8/11 | **11/11** ✅ | 완료 — O3, O5, O6 개선 |

### 전파할 패턴 목록

`feature-draft`와 `implementation`에서 추출한 5가지 핵심 패턴:

| # | 패턴 | 출처 | 적용 방법 |
|---|------|------|----------|
| 1 | **Step별 도구 매핑** | feature-draft Step 1-7 | 각 Step에 `**Tools**: Read, Glob, codebase-retrieval` 형식으로 명시 |
| 2 | **Decision Gates (IF/ELSE)** | feature-draft Gate 1→2, 3→4, 4→5, 6→7 | Step 전환 시 의사코드 형태의 진입 조건 추가 |
| 3 | **중간 체크포인트** | feature-draft Step 5.5 | Part/Phase 완료 시 사용자에게 요약 테이블 제시 + AskUserQuestion |
| 4 | **Glob 기반 검증** | feature-draft Step 7 | `[M]` 파일 존재 확인, `[C]` 파일 미존재 확인, 상위 디렉토리 확인 |
| 5 | **컨텍스트 관리 전략** | feature-draft Context Management | 스펙/코드 크기별 4단계 읽기 전략 테이블 (< 200줄 / 200-500 / 500-1000 / > 1000) |

### 추가 권장 패턴 (implementation에서 추출)

| # | 패턴 | 출처 | 적용 방법 |
|---|------|------|----------|
| 6 | **Severity 기반 Decision Gate** | implementation Step 6.4 | Critical → 수정 필수, Quality → 문서화, Improvement → 나중에 |
| 7 | **Sub-agent 실패 복구** | implementation Step 5 | FAILED/PARTIAL 상태 처리, 순차 재시도, 사용자 보고 |
