# 토론 요약: implementation 3개 스킬을 agentic_coding_principle.md 기준으로 정합화

**날짜**: 2026-04-30
**라운드 수**: 5
**참여 방식**: 구조화된 토론 (discussion skill)
**대상 파일**: `.claude/skills/implementation-plan/SKILL.md`, `.claude/skills/implementation/SKILL.md`, `.claude/skills/implementation-review/SKILL.md` (각각 `.claude/agents/` 미러 동시)

## 핵심 논점 (Key Discussion Points)

1. **시작 항목 선택**: 5개 갭 중 어디부터 — P0-1 (implementation-plan Min-Code)을 시작점으로. upstream 효과 + feature-draft 템플릿 재사용 가능.
2. **Min-Code 도입 패턴**: 3개 스킬에 일관된 enforcement 체인 필요. plan→implement→review가 모두 같은 원칙을 표현해야 enforcement loop가 닫힘.
3. **inline 질문 제거 vs 유지**: implementation-plan은 하류 비용이 크지만, feature-draft에서 user가 "best-effort + surface"를 채택. 일관성 우선.
4. **Review가 자기 권고도 구속해야 함**: reviewer가 사변적 권고("future-proof X 추가")를 만들면 self-defeating. Recommendations 자체에 Min-Code 적용.
5. **Surface fatigue 관리**: implementation은 long-running. Surface timing은 시작 전 1회 + Phase 후 예외 기반 — 총 fatigue를 낮추되 critical events는 노출.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | P0-1 implementation-plan: Hard Rule 12 (task Min-Code) + Hard Rule 10 보강 (phase 분리 조건) + AC + Step 4 self-check + Step 7 review | feature-draft Rule 10 패턴 미러로 일관성 확보. phase axis는 implementation-plan 고유라 Hard Rule 10에 한 줄 보강 | 1, 2 |
| 2 | P0-2 implementation: Hard Rule (Min-Code) + AC + sub-agent prompt 규칙 4 + Phase Review "Speculative Code" 카테고리 | 4-layer enforcement (declaration / verification / execution / integration). REFACTOR 단계도 단일 사용처 추상화 금지 명시 | 2 |
| 3 | P1-1 implementation-plan: Hard Rule 2 교체 (best-effort + 스키마) + Open Questions 스키마 + Step 8 (Surface) + AC + Error Handling 갱신 | feature-draft 패턴 full mirror. inline 질문 제거 — 일관성 > 안전망 | 3 |
| 4 | P1-2 implementation-review: Step 5 Assessment에 Speculative Code 축 + Step 6 Findings 명시 분류 + Hard Rule (Recommendations Min-Code) + AC + Output Format 가이드 | enforcement loop 완성. reviewer 자기 권고 구속으로 self-defeating 방지 | 4 |
| 5 | P2 implementation: Step 1 끝 "Surface Plan Assumptions" + Step 6 끝 "Surface Phase Surprises" + AC | 시작 전 1회 + Phase 후 예외 기반. fatigue 관리 + critical event 노출 균형. Hard Rule 미추가, Process+AC만 | 5 |
| 6 | 모든 변경은 SKILL.md + agent.md 미러 동시 적용 | 이미 9쌍 완전 미러 정합 상태. drift 재발 방지 | (전반) |

## 미결 질문 (Open Questions)

| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| 1 | 구현 순서 (P0-1→P0-2→P1-1→P1-2→P2 vs 파일별 묶음) | deferred-deliberately | 다음 세션에서 결정 (auto-labeled, please review) |
| 2 | 변경 후 실제 feature를 한 번 돌려 enforcement loop가 작동하는지 verify할지 | deferred-deliberately | 다음 세션 또는 별도 검증 task (auto-labeled, please review) |

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | implementation-plan SKILL.md + agent.md에 P0-1 + P1-1 적용 | High | 다음 세션 |
| 2 | implementation SKILL.md + agent.md에 P0-2 + P2 적용 | High | 다음 세션 |
| 3 | implementation-review SKILL.md + agent.md에 P1-2 적용 | High | 다음 세션 |
| 4 | 변경 후 9쌍 미러 정합성 재검증 (diff 4 이하) | Medium | 다음 세션 |

## 리서치 결과 요약 (Research Findings)

- **agentic_coding_principle.md** 4원칙: Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution.
- **3개 스킬 현 상태**: Surgical Changes + Goal-Driven Execution은 모범 적용. Simplicity First가 chain 전체에서 미적용 — 가장 큰 시스템적 갭.
- **feature-draft 선례**: 2.3.0에서 Hard Rule 10 (Minimum-Code Mandate), Hard Rule 4 (best-effort + Open Q schema), Step 8 (Surface) 도입 완료. 본 토론의 design template.

## 토론 흐름 (Discussion Flow)

Round 1: 시작 항목 선택 → P0-1 (upstream 효과)
Round 2: P0-1 도입 방식 → feature-draft 패턴 미러
Round 3: P0-1 적용 범위 → Task + Phase level
Round 4: P0-2 적용 레이어 → 4곳 미러링
Round 5: P1-1 / P1-2 / P2 동일 패턴 미러로 합의

## 부록: 대화 로그 (Conversation Log)

### Round 1 — 시작 항목

**Q**: 5개 항목 중 어디부터 논의할까요?
**Options**: P0-1 (Recommended) / P0-2 / 묶음 / 우선순위 먼저
**A**: P0-1
**Follow-up**: implementation-plan을 upstream 처음부터 깔끔하게 → 하류 자연 전파

### Round 2 — P0-1 도입 방식

**Q**: implementation-plan에 Min-Code 어떻게 도입할까요?
**Options**: feature-draft 패턴 미러 (Recommended) / Lightweight / Conditional
**A**: feature-draft 패턴 미러
**Follow-up**: Hard Rule 12 신규 + AC + Step 4/7 self-check. 비판적 review로 룰 필요성(standalone, deeper breakdown, legacy plan) 검증.

### Round 3 — P0-1 적용 범위

**Q**: Min-Code 룰의 적용 범위는?
**Options**: Task-only / Task+Phase (Recommended) / Task+Phase+Validation
**A**: Task+Phase (Hard Rule 10에 phase 분리 조건 한 줄 보강)
**Follow-up**: Validation Plan은 ID linkage가 이미 강제적이라 과잉. Phase는 implementation-plan 고유 axis라 커버 필요.

### Round 4 — P0-2 적용 레이어

**Q**: P0-2 적용 레이어는?
**Options**: 4곳 미러링 (Recommended) / 2곳 / 1곳
**A**: 4곳 미러링 (Hard Rule + AC + sub-agent prompt + Phase Review)
**Follow-up**: TDD REFACTOR 단계도 단일 사용처 추상화 금지로 명시. sub-agent self-check 필드는 추가하지 않음 (Phase Review가 catch).

### Round 5 — P1-1 / P1-2 / P2

**Q**: P1-1 어떻게? → Full mirror of feature-draft (Recommended) → inline 질문 제거, 스키마+Surface 패턴
**Q**: P1-2 범위? → 완전체 (Assessment 축 + Findings 분류 + Recommendations 구속) (Recommended)
**Q**: P2 surface 타이밍? → 시작 전 + Phase 후 예외 기반 (Recommended)

**최종 합의**: 5개 설계, 6개 파일 (3쌍 미러), 다음 세션에서 구현.
