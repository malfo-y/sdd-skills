# Orchestrator: gstack 패턴 sdd-skills 적용

**기능명**: gstack 패턴의 sdd-skills 적용 (토론 결과 10개 결정 사항 구현)
**생성일**: 2026-03-24
**생성자**: sdd-autopilot

## 기능 설명

**사용자 요청 원문**: "그럼 이제 sdd 스킬들을 sdd 스킬들로 업데이트 해 볼까!"

**구체화된 요구사항**:
gstack 분석 토론(`_sdd/discussion/discussion_gstack_patterns_for_sdd_skills.md`)에서 도출된 10개 결정 사항을 sdd-skills의 에이전트/스킬 파일에 반영한다.

수정 대상 (7개 기존 + 1개 신규):
1. `.claude/agents/feature-draft.md` — 경량 Failure Modes 테이블 추가
2. `.claude/agents/implementation-plan.md` — Test Coverage Diagram 조건부 도입
3. `.claude/agents/implementation.md` — Verification Gate + Regression Iron Rule
4. `.claude/agents/implementation-review.md` — Verification Gate Iron Rule
5. `.claude/agents/spec-review.md` — 코드 분석 지표 추가
6. `.claude/skills/pr-review/SKILL.md` — Fix-First 계층 분리 + Scope Drift Detection
7. `.claude/skills/sdd-autopilot/SKILL.md` + references — Audit Trail + Taste Decision
8. 신규: `.claude/agents/investigate.md` + `.claude/skills/investigate/SKILL.md`

**제약 조건**:
- 스킬 작성 4원칙 준수: SDD docs 준수, AC 정의/준수, Self-contained, Conciseness (context dilution 방지)
- `_sdd/spec/` 직접 수정 금지 (spec-update-done으로 위임)
- 기존 AC/Hard Rules/Process 구조 유지하면서 최소한의 추가

## Acceptance Criteria

- [ ] AC1: feature-draft에 Failure Modes 테이블 섹션이 Part 1에 추가됨 (항상 포함, 간단하면 N/A)
- [ ] AC2: implementation-plan에 [M] 마커 대상 Test Coverage Diagram 단계가 추가됨
- [ ] AC3: implementation에 Verification Gate ("should work" 금지, 재검증 필수) + Regression Iron Rule (기존 테스트 실패 시 자동 회귀 테스트) 추가됨
- [ ] AC4: implementation-review에 fresh verification 규칙 추가됨 (테스트 출력을 근거로)
- [ ] AC5: spec-review에 핫스팟/Focus Score/Test Coverage 지표 기반 우선순위 단계 추가됨
- [ ] AC6: pr-review에 Fix-First 계층 (코드 품질 AUTO-FIX + 목록 기록) + Scope Drift Detection 추가됨
- [ ] AC7: sdd-autopilot에 Audit Trail + Taste Decision 표면화 메커니즘 추가됨
- [ ] AC8: investigate 스킬/에이전트가 생성됨 (근본원인 우선, 3-strike, scope lock, fresh verification, 독립 Agent 교차 검증)
- [ ] AC9: 스펙(main.md)이 변경 사항을 반영하여 업데이트됨

## Reasoning Trace

- **대규모 파이프라인**: 10개 결정 사항 × 8+파일 = 10+파일 영향, 신규 컴포넌트 1개
- **feature-draft 필요**: 각 수정의 스펙 패치를 정리하고 구현 계획을 세워야 함
- **spec-update-todo 필요**: 대규모이므로 드리프트 방지를 위해 계획 사전 등록
- **인라인 테스트**: 마크다운 스킬 파일 수정이므로 구조 검증 위주 (런타임 테스트 아님)
- **Conciseness 원칙 강제**: 모든 수정이 "이 문장이 없으면 AI가 못 하는가?" 기준 통과해야 함

## Pipeline Steps

### Step 1: Feature Draft
- **에이전트**: `sdd-skills:feature-draft`
- **입력 파일**: `_sdd/spec/main.md`, `_sdd/discussion/discussion_gstack_patterns_for_sdd_skills.md`
- **출력 파일**: `_sdd/drafts/feature_draft_gstack_patterns.md`
- **프롬프트**: |
    토론 결과 `_sdd/discussion/discussion_gstack_patterns_for_sdd_skills.md`의 10개 결정 사항을 기반으로 feature draft를 작성해줘.

    수정 대상 파일 8개:
    1. `.claude/agents/feature-draft.md` — Part 1 스펙 패치에 Failure Modes 테이블 섹션 추가. 항상 포함, 간단하면 N/A 또는 1-2행. 복잡하면 3-5행 (시나리오/실패 시/사용자 가시성/처리 방안).
    2. `.claude/agents/implementation-plan.md` — Target Files에 [M] 마커가 있을 때만 해당 파일의 기존 테스트 커버리지 매핑. [C] 전용이면 스킵.
    3. `.claude/agents/implementation.md` — Hard Rules에 Verification Gate ("should work" 금지, 코드 변경 후 테스트 재실행 필수, 이전 결과 재사용 금지) + Regression Iron Rule (기존 테스트 실패 시 테스트 업데이트 + 회귀 방지 테스트 추가 필수, 사용자 확인 없이 자동).
    4. `.claude/agents/implementation-review.md` — fresh verification: 코드를 읽고 "맞다"가 아니라 테스트 실행 출력을 근거로 판단. "should work" 금지.
    5. `.claude/agents/spec-review.md` — Step 2 또는 Step 3에 코드 분석 지표 추가: 핫스팟(자주 변경 파일), Focus Score(변경 집중도), Test Coverage(스펙 기능별 테스트 현황). 이 지표로 "어디를 더 깊이 봐야 하는지" 데이터 기반 판단.
    6. `.claude/skills/pr-review/SKILL.md` — (a) Step 2.5로 Scope Drift Detection pre-step 추가: PR diff 변경 파일 vs 스펙 패치 초안 범위 비교, CLEAN/DRIFT/MISSING 판정, 리포트 상단 표시. (b) Step 5.5로 코드 품질 Fix-First 추가: 누락된 에러 처리/타입 불일치/미사용 import 등을 AUTO-FIX(즉시 수정) / 목록 기록(수정 불가) 분류. AskUserQuestion 없이 처리.
    7. `.claude/skills/sdd-autopilot/SKILL.md` — Step 7.2의 실행 루프에서 모든 자동 결정을 로그에 기록 (판단 근거 포함). Taste decision(합리적으로 다르게 판단 가능한 것)은 Step 8 최종 보고서에 표면화.
    8. 신규: `.claude/agents/investigate.md` + `.claude/skills/investigate/SKILL.md` — 범용 체계적 디버깅 스킬. 근본원인 먼저/수정은 나중(Iron Law), 3-strike 에스컬레이션, scope lock(수정 범위 제한), blast radius gate(5+파일 경고), fresh verification(원본 시나리오 재현), 독립 Agent 교차 검증(Agent A: 가설 기반, Agent B: 코드만 독립 탐지).

    핵심 원칙: Conciseness — 추가하는 모든 문장에 대해 "이 문장이 없으면 AI가 못 하는가?" 기준 적용. Self-contained — 외부 참조 최소화.

### Step 2: Spec Update Todo
- **에이전트**: `sdd-skills:spec-update-todo`
- **입력 파일**: `_sdd/drafts/feature_draft_gstack_patterns.md`, `_sdd/spec/main.md`
- **출력 파일**: `_sdd/spec/main.md` (업데이트)
- **프롬프트**: |
    feature draft `_sdd/drafts/feature_draft_gstack_patterns.md`의 Part 1 스펙 패치를 글로벌 스펙에 계획 상태로 반영해줘. investigate 신규 스킬을 Component Details에 추가하고, 기존 스킬 설명에 새 기능을 📋계획됨으로 표시.

### Step 3: Implementation Plan
- **에이전트**: `sdd-skills:implementation-plan`
- **입력 파일**: `_sdd/drafts/feature_draft_gstack_patterns.md`, `_sdd/spec/main.md`
- **출력 파일**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- **프롬프트**: |
    feature draft `_sdd/drafts/feature_draft_gstack_patterns.md`의 Part 2를 기반으로 상세 구현 계획을 수립해줘.

    수정 대상 파일(Target Files)은 다음과 같다:
    - [M] `.claude/agents/feature-draft.md`
    - [M] `.claude/agents/implementation-plan.md`
    - [M] `.claude/agents/implementation.md`
    - [M] `.claude/agents/implementation-review.md`
    - [M] `.claude/agents/spec-review.md`
    - [M] `.claude/skills/pr-review/SKILL.md`
    - [M] `.claude/skills/sdd-autopilot/SKILL.md`
    - [C] `.claude/agents/investigate.md`
    - [C] `.claude/skills/investigate/SKILL.md`

    병렬화: 에이전트 파일 수정은 파일 간 의존성이 없으므로 병렬 가능. investigate 신규 생성도 독립적. pr-review와 sdd-autopilot 스킬 수정도 독립적.

    핵심 원칙: Conciseness — 각 수정은 AC 항목 또는 Hard Rule 1-2줄 수준으로 최소화.

### Step 4: Implementation
- **에이전트**: `sdd-skills:implementation`
- **입력 파일**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- **출력 파일**: 수정된 에이전트/스킬 파일들
- **프롬프트**: |
    구현 계획에 따라 각 에이전트/스킬 파일을 수정해줘.

    핵심 원칙:
    - Conciseness: "이 문장이 없으면 AI가 못 하는가?" 기준. 불필요한 설명 추가 금지.
    - Self-contained: 외부 참조 대신 필요한 규칙을 파일 내에 명시.
    - AC-First: 새 기능은 AC 항목으로 추가.
    - 기존 구조 유지: AC/Hard Rules/Process 섹션 패턴 유지.

### Step 5: Review-Fix Loop
- **review**: `sdd-skills:implementation-review`
- **fix**: `sdd-skills:implementation`
- **최대 반복**: 3회
- **종료 조건**: critical==0 AND high==0 AND medium==0
- **수정 대상**: critical/high/medium
- **MAX 도달 시**: critical/high > 0 → 중단, medium만 → 계속

### Step 6: Spec Update Done
- **에이전트**: `sdd-skills:spec-update-done`
- **입력 파일**: `_sdd/spec/main.md`, 수정된 에이전트/스킬 파일들
- **출력 파일**: `_sdd/spec/main.md` (업데이트)
- **프롬프트**: |
    구현 완료된 변경 사항을 글로벌 스펙에 반영해줘. 📋계획됨 상태를 ✅완료로 업데이트하고, investigate 스킬의 상세 설명을 추가해줘.

## Test Strategy

- **방식**: inline
- **실행 명령**: 구조 검증 — 각 수정된 파일에서 AC 섹션/Hard Rules/Process 구조가 유지되는지 확인. 마크다운 문법 오류 없는지 확인.
- **선택 근거**: 스킬 프로젝트는 마크다운 파일 수정이므로 런타임 테스트 대신 구조적 정합성 검증.
- **사용자 보고 형식**: 수정된 파일 수, 추가된 AC/Hard Rule 수, 구조 검증 통과 여부.

## Error Handling

- **재시도 횟수**: 3
- **핵심 단계**: feature-draft, implementation-plan, implementation, implementation-review
- **비핵심 단계**: spec-update-todo, spec-update-done
