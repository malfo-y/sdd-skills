# 토론 요약: sdd-autopilot에 harness 철학 도입 — reasoning 기반 오케스트레이션

**날짜**: 2026-03-18
**라운드 수**: 5
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)

1. **Reasoning 수준**: 템플릿 매칭이 아닌, SDD 철학을 이해하고 상황에 맞게 스킬을 조합하는 동적 reasoning
2. **Reference 문서 구조**: docs/ 3개 문서(~1600줄)를 철학 + 스킬 카탈로그로 압축
3. **오케스트레이터 생성 방식**: 현재 패턴(SKILL.md 파일 생성) 유지
4. **기존 로직 처리**: 전면 교체 + Hard Rules 유지
5. **안전장치**: 생성-검증 루프로 구조 의존성 + 철학 정합성 검증

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | autopilot 4단계 구조: reference 읽기 → 태스크 분석 → 오케스트레이터 생성 → 실행 | 사람이 docs/ 읽고 reasoning하듯이 autopilot도 동일한 과정을 거쳐야 함 | 논점 1 |
| 2 | reference 구조 = 철학 + 스킬 카탈로그 | 철학으로 "왜"를 이해하고, 카탈로그로 "무엇을 조합할지" 판단 | 논점 2 |
| 3 | reference는 references/에 분리 | SKILL.md 경량화, 필요시에만 Read로 로드하여 토큰 절약 | 논점 2 |
| 4 | 오케스트레이터 = 현재 패턴(SKILL.md 파일 생성) 유지 | 검증된 패턴 재활용 | 논점 3 |
| 5 | 기존 autopilot 전면 교체 + Hard Rules 유지 | review-fix 루프, Execute→Verify, 파일 기반 상태 전달 등 검증된 규칙은 보존 | 논점 4 |
| 6 | 생성-검증 루프로 안전장치 (구조 + 철학 검증) | 동적 생성의 리스크를 Producer-Reviewer 패턴으로 관리 | 논점 5 |

## 미결 질문 (Open Questions)

- (없음 — 모든 논점이 결정됨)

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 설명 |
|---|------|---------|------|
| 1 | 압축 reference 문서 생성 | High | docs/ 3개 문서(~1600줄)를 SDD 철학 + 스킬 카탈로그로 압축하여 `references/sdd-reasoning-reference.md` 생성 |
| 2 | autopilot SKILL.md 리라이트 | High | reference 기반 reasoning + 생성-검증 루프 + Hard Rules 유지로 전면 교체 |

## 리서치 결과 요약 (Research Findings)

- **현재 autopilot 구조**: 8단계 파이프라인(Step 0~8), 규모별 템플릿(소/중/대), review-fix 루프(최대 3회), Execute→Verify 패턴, 파이프라인 resume 기능. 1227줄의 SKILL.md + references/(scale-assessment.md, pipeline-templates.md) + examples/(sample-orchestrator.md)
- **harness 스킬**: 에이전트 팀 + 스킬 생성 메타스킬. 4가지 아키텍처 패턴(파이프라인, 팬아웃/팬인, 전문가 풀, 생성-검증). 에이전트="누가 하는가", 스킬="어떻게 하는가" 분리 철학

## 아키텍처 요약

```
[autopilot 메타스킬 SKILL.md]
  │
  ├─ Read: references/sdd-reasoning-reference.md  ← 압축 철학 + 스킬 카탈로그
  │
  ├─ Step 1: reference 읽고 SDD 이해
  ├─ Step 2: 사용자 태스크 분석 + 인라인 토론
  ├─ Step 3: reasoning → orchestrator_<topic>/SKILL.md 동적 생성
  ├─ Step 4: 검증 에이전트 (구조 의존성 + SDD 철학 정합성)
  │           └─ 문제시 Step 3 재시도
  ├─ Step 5: 사용자 체크포인트 (승인)
  └─ Step 6: 오케스트레이터 실행 (Hard Rules 적용)
               ├─ Execute → Verify 루프
               ├─ Review-Fix 사이클
               └─ 파일 기반 상태 전달
```

### 현재 vs 목표 비교

| | 현재 autopilot | 목표 autopilot |
|---|---|---|
| 지식 | 하드코딩된 규모별 템플릿 | reference 문서를 읽고 SDD 철학을 이해 |
| 판단 | 규모 분류 → 템플릿 매칭 | 태스크 분석 → reasoning 기반 스킬 조합 |
| 산출물 | 고정 파이프라인 실행 | 동적 오케스트레이터 스킬 생성 → 실행 |
| 안전장치 | 사용자 체크포인트 | 생성-검증 루프 + 사용자 체크포인트 |
| 유연성 | 소/중/대 3가지 경로 | 상황에 맞는 무한한 조합 가능 |

## 토론 흐름 (Discussion Flow)

Round 1: Reasoning 수준 → 4단계 구조 결정 (reference 공부 → 분석 → 오케스트레이터 생성 → 실행)
Round 2: Reference 문서 구조 → 철학 + 스킬 카탈로그 선택
Round 3: 오케스트레이터 생성 방식 → 현재 패턴 유지 + 토큰 전략(references/에 분리)
Round 4: 기존 로직 처리 → 전면 교체 + Hard Rules 유지
Round 5: 안전장치 + 실행 계획 → 생성-검증 루프(구조+철학) + reference 문서 먼저 작성

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 현재 autopilot은 규모별로 파이프라인 템플릿이 하드코딩되어 있잖아요. 여기에 "reasoning"을 추가한다는 건 구체적으로 어떤 수준을 기대하시나요?
**Options**: 1) 템플릿 선택의 근거 추가 2) 동적 파이프라인 구성 3) 하이브리드 4) 토론 종료
**A**: autopilot 메타스킬은: 1) sdd가 뭔지 reference 문서를 보고 공부; 2) 이걸 바탕으로 사람이 주어진 태스크를 sdd 스킬/에이전트들을 이용해 어떻게 해결할지 분석; 3) 이를 바탕으로 에이전트들을 지휘하는 오케스트레이터 스킬 생성; 4) 오케스트레이터 스킬 실행
**Follow-up**: 사실상 "동적 파이프라인 구성"이지만 더 구체적 — harness의 팀 아키텍처 설계를 SDD 도메인에 특화

### Round 2
**Q**: 압축 reference 문서의 범위와 구조를 어떻게 잡을까요?
**Options**: 1) 철학 + 스킬 카탈로그 2) 의사결정 트리 3) 원칙 + 예시 기반 4) 토론 종료
**A**: 철학 + 스킬 카탈로그
**Follow-up**: Part 1(철학): 스펙 중요성, 두 단계 구조, 화이트페이퍼형 스펙 / Part 2(카탈로그): 역할, 입력/출력, 의존성, 사용 조건

### Round 3
**Q**: 오케스트레이터 생성 방식 / 토큰 효율
**Options (2 questions)**: SKILL.md 패턴 유지 vs 에이전트 기반 vs 하이브리드 / 인라인 vs 분리 vs 계층화
**A**: 현재 패턴 유지 + references/에 분리
**Follow-up**: SKILL.md 가볍게 유지하면서 필요시에만 Read

### Round 4
**Q**: 현재 autopilot SKILL.md(1227줄)의 기존 로직은 어떻게 할까요?
**Options**: 1) 전면 교체 2) Hard Rules만 유지 3) 병존 4) 토론 종료
**A**: 전면 교체하되 Hard Rules 유지
**Follow-up**: 검증된 규칙(review-fix, Execute→Verify, 파일 기반 상태 전달) 보존, 오케스트레이션 로직만 reasoning으로 교체

### Round 5
**Q**: 안전장치 + 검증 기준 + 실행 계획
**Options (3 questions combined)**: 사용자 체크포인트 vs 생성-검증 루프 vs Hard Rules / 구조 vs 철학 vs 둘 다 / reference 먼저 vs SKILL.md 먼저 vs 병렬
**A**: 생성-검증 루프 + 둘 다(구조+철학) + reference 문서 먼저
**Follow-up**: Producer-Reviewer 패턴으로 오케스트레이터 생성 자체를 검증, 구현 순서는 reference → SKILL.md
