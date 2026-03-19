# 토론 요약: ralph-loop-init 범용화

**날짜**: 2026-03-19
**라운드 수**: 4
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)

1. **ralph의 스코프 한계**: 현재 ralph-loop-init은 ML 학습 디버깅 전용으로 구현되어 있어, autopilot이 일반 e2e 테스트에 활용하기 어렵다. 워크플로우 테이블에 "ML 학습/e2e 테스트 등"이라고 적혀 있지만, 실제 구현(Step 1~4)은 `train*.py` 탐색, 하이퍼파라미터, GPU 설정 등 ML 전용이다.
2. **핵심 메커니즘은 범용적**: ralph의 코어(state machine + action.sh loop + LLM 반복 디버깅)는 ML에 한정되지 않는 범용 자동화 메커니즘이다.
3. **phase machine 일반화**: 현재 ML 전용 phases(TRAINING, VALIDATING 등)를 프로젝트 타입에 따라 유연하게 커스터마이징할 수 있어야 한다.
4. **autopilot 연결**: autopilot의 "인라인 디버깅 vs ralph" 고정 분기를 제거하고, 프로젝트 특성에 따른 자율 판단으로 전환한다.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | ralph 자체를 범용화한다 (별도 스킬 생성 X) | 코어 메커니즘이 이미 범용적이므로, Step 1의 탐색 로직만 일반화하면 된다. 별도 스킬은 중복 | 1, 2 |
| 2 | phase machine: 고정 레퍼런스 + LLM 동적 커스터마이징 | 유연성(프로젝트별 phase 최적화)과 가이드라인(레퍼런스 phase set) 양립 | 3 |
| 3 | autopilot: 인라인/ralph 분기 조건을 고정하지 않고 자율 판단에 위임 | 프로젝트 특성에 따라 최적 전략이 달라지므로 고정 규칙보다 판단 위임이 적합 | 4 |
| 4 | 기존 ML 사용자 호환성 유지: ML 템플릿을 보존한다 | 범용화하더라도 ML이 가장 빈번한 유스케이스이므로 기존 동작이 깨지면 안 됨 | 1 |

## 미결 질문 → 해소 (Resolved Open Questions)

| # | 질문 | 결정 |
|---|------|------|
| 1 | 레퍼런스 phase set 구성 | **SETUP / SMOKE_TEST / EXECUTING / CHECKING / ANALYZING / ADJUSTING / DONE** 7개를 hint로 제공. LLM이 프로젝트를 분석해서 자유롭게 phase를 구성하되, 일반적으로 이런 phase들이 있다는 가이드 역할. |
| 2 | Step 1 프로젝트 타입 자동 감지 기준 | **LLM 판단에 위임**. 고정 파일 패턴 매칭(train*.py 등) 대신 LLM이 프로젝트를 분석해서 적절한 탐색 전략을 직접 결정. |
| 3 | `ralph-loop-concept.md` 범용화 여부 | **그대로 유지**. ML 예시 기반으로 남기되, agent 문서에 "범용 프로세스에 맞게 변환/수정하여 활용 가능"하다고 명시. |
| 4 | config.sh 변수 구조 | **루프 제어 변수만 고정** (`LLM_TIMEOUT_SECONDS`, `MAX_LLM_FAILURES` 등), 나머지는 LLM이 프로젝트에 맞게 생성. ML 전용 변수(MODEL_ID 등)는 ML 프로젝트일 때만 LLM이 추가. |
| 5 | autopilot 자율 판단 가이드 | **힌트 제공 방식**. "장시간 실행, 반복 디버깅, 환경 격리 필요 시 ralph 고려" 정도의 가이드라인을 명시하고, 최종 판단은 autopilot에 위임. |

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | ralph-loop-init 스킬/에이전트의 description 범용화 | High | feature-draft |
| 2 | Step 1을 "프로세스 탐색"으로 일반화 (ML 탐색은 타입별 분기로 보존) | High | feature-draft |
| 3 | 레퍼런스 phase set 정의 + phase 커스터마이징 가이드 추가 | High | feature-draft |
| 4 | PROMPT.md 템플릿을 타입별로 분기 가능하게 구조화 | Medium | feature-draft |
| 5 | autopilot에서 인라인/ralph 고정 분기 제거, 자율 판단 가이드로 교체 | Medium | feature-draft |
| 6 | 기존 ML 시나리오 회귀 테스트 (범용화 후 ML 유스케이스 동작 확인) | Medium | 검증 |

## 리서치 결과 요약 (Research Findings)

- **ralph-loop-init agent**: Step 0~7 전체가 ML 전용 (train*.py 탐색, 하이퍼파라미터, TRAINING/VALIDATING phase 등). 단, 워크플로우 테이블은 이미 "ML/e2e" 범용 의도 표시
- **autopilot**: Step 4.1에서 "인라인 테스트 vs ralph-loop" 분기 존재. Hard Rule #10으로 ralph 설정만 만들고 실행 건너뛰기 방지
- **메모리**: `feedback_autopilot_ralph_skip.md` — autopilot이 ralph loop 생성 후 실제 실행/디버깅을 건너뛰는 기존 문제 기록됨

## 토론 흐름 (Discussion Flow)

Round 1: ralph 회피 원인 → "ML로 스코프가 한정되어 있어서 e2e에 적용이 안 됨"
Round 2: 확장 방향 → "ralph 자체를 범용화 (별도 스킬 생성 X)"
Round 3: phase machine → "고정 레퍼런스 + LLM 동적 커스터마이징"
Round 4: autopilot 연결 → "고정 분기 제거, 자율 판단 위임" + "토론 정리 후 구현"

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: ralph를 회피하려는 이유가 뭐였나요?
**Options**: 1) 오버헤드 문제 2) 실행 불안정 3) 둘 다 4) 토론 종료
**A**: "ralph의 목적을 너무 한정적으로 잡아서. ML 학습 뿐 아니라 모든 시간이 걸리는 e2e 테스트에서 활용하는 스킬로 만들어야 하는데."
**Follow-up**: 문제는 회피가 아니라 스코프 한계. ralph의 핵심 메커니즘은 범용적이나 구현이 ML 전용.

### Round 2
**Q**: ralph의 핵심 메커니즘은 범용적인데 Step 1~4의 파이프라인 탐색이 ML 전용. 어떻게 확장?
**Options**: 1) ralph 자체를 범용화 2) autopilot이 직접 커스터마이즈 3) 별도 e2e 스킬 생성 4) 토론 종료
**A**: "ralph 자체를 범용화"
**Follow-up**: Step 1을 프로세스 타입 감지 → 타입별 탐색 분기로 구조화.

### Round 3
**Q**: phase machine을 어떻게 처리할까요?
**Options**: 1) 고정 phase + alias 2) 타입별 템플릿 3) LLM 동적 생성 4) 토론 종료
**A**: "LLM이 동적 생성하되, 고정 phase + alias를 레퍼런스로 줘서 참고하게"
**Follow-up**: 하이브리드 접근 — 유연성 + 가이드라인 양립.

### Round 4
**Q**: autopilot의 인라인/ralph 분기를 어떻게 바꿀까요?
**Options**: 1) 항상 ralph 2) 복잡도 기준 분기 유지 3) autopilot 판단 위임 4) 토론 종료
**A**: "autopilot 판단에 위임"
**Follow-up**: 고정 조건 제거, 프로젝트 특성 기반 자율 판단으로 전환.
