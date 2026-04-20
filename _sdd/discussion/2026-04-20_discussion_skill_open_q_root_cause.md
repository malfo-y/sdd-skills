# 토론 요약: discussion 스킬 종료 후 미결 질문 잔존 원인

**날짜**: 2026-04-20
**라운드 수**: 3
**참여 방식**: 구조화된 토론 (discussion skill, meta)

## 핵심 논점 (Key Discussion Points)

1. **실태 진단**: `_sdd/discussion/` 산출물 7건 표본 분석. 5/7은 깔끔히 종료, 2/7에 미결 질문 잔존. 한 건은 followup 토론 파일을 별도 생성(`spec_skill_open_questions_followup.md`).
2. **잔존 미결 질문의 카테고리화**:
   - 의존성 체인: 상위 Q가 미해결이라 하위 Q들이 자동으로 미결 (`global_spec_role_balance`)
   - 구현 시점으로 떠넘김: AC/Final Check wording을 "구현하면서 정리"로 미룸
   - 명시적 deferral (정상): 다른 토론으로 분리 합의
3. **숨은 압력 요인**: 사용자가 추가로 지적 — 토론이 길어지면 fatigue로 빠르게 수렴하려는 경향. 즉 스킬의 수렴 신호(3.5)와 stagnation fallback(3.5.1)이 fatigue를 타고 조기 종료를 보상.
4. **약점이 누적되는 메커니즘**: Gate 3→4의 "그대로 정리(미결로 기록)" 출구가 너무 매끄러움 + 수렴 신호에 `open_questions > 0` 가드 부재 + AI가 묵시적 deferral("나중에")을 그 자리에서 도전하지 않음.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | 방향성: **A(상류 차단) + C(수렴 가드)** 조합 채택 | 게이트 강화(B)만으로는 fatigue를 못 이김. 미결이 쌓이는 것 자체를 줄이는 A가 근본, C는 자동 안전망 | 3, 4 |
| 2 | A는 **Soft 모드**로 적용 — 분류는 AI 내부 추론만, 표면에 메타-질문 노출 금지 | 매 deferral마다 사용자에게 "이거 (a/b/c) 중 뭐죠?"를 물으면 그 자체가 fatigue 가속, 사용자가 우회 | 3 |
| 3 | C는 수렴 신호(3.5)와 stagnation fallback(3.5.1)에 "in-scope open_q > 0이면 종료 권유 보류" 가드 추가 | 자동화 가드라 사용자 부담 0. 하지만 보조적 — A가 메인 | 4 |

## 미결 질문 (Open Questions)

- (없음 — 이번 토론은 진단 및 방향 합의가 목표였고, 구현 설계는 별도 작업)

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | `discussion/SKILL.md` 3.2/3.2.2에 "묵시적 deferral 감지 시 AI가 (a) 지금 답 가능한 한 가지로 좁혀 재질문 (b/c) 조용히 기록" 가이드 추가 | High | TBD |
| 2 | `discussion/SKILL.md` 3.5와 3.5.1에 "in-scope `open_questions` > 0이면 수렴 권유 보류" 가드 명시 | High | TBD |
| 3 | Gate 3→4의 "그대로 정리(미결로 기록)" 옵션 옆에 미결 카테고리(out-of-scope/needs-data/deferred-deliberately/blocked-by) 강제 라벨 추가 | Medium | TBD |
| 4 | 변경 후 1-2주간 `_sdd/discussion/` 신규 산출물에서 미결 질문 발생률 추적, followup 파일 생성률 비교 | Medium | TBD |

## 리서치 결과 요약 (Research Findings)

- **표본 7건 분석 표** (Explore subagent):
  - 깔끔 종료(open_q=0): 5건 — `discussion_autopilot_meta_skill`, `discussion_autopilot_open_questions`, `discussion_implementation_review_loop`, `discussion_autopilot_reasoning_harness`, `discussion_spec_whitepaper_open_questions`(상속분 모두 해결)
  - 잔존: 2건 — `2026-04-13_discussion_global_spec_role_balance`(4건, 의존성 체인), `2026-04-13_discussion_spec_skill_open_questions_followup`(3건, wording deferred)
- **Followup 추적성 약점**: 7건 중 3건이 followup을 낳았지만 부모-자식 backlink 명시는 1건에만 존재.
- **스킬 코드 자체 점검**: Gate 3→4 정의는 있으나 의존성 체인 자동 탐지 로직은 부재. 수렴 신호(3.5)에 `open_questions` 가드도 부재.

## 토론 흐름 (Discussion Flow)

- Round 1: 표본 분석 결과 공유 → 사용자가 "구현 시점 떠넘김 + 의존성 체인 + 길어지면 빨리 수렴" 세 가지 모두 인정. 세 번째가 깊이 신호로 들어옴.
- Round 2: 3가지 대안(A 상류/B 게이트/C 가드) 제시, 권장 A+C → 사용자가 A+C 채택.
- Round 3: 비판적 검토 — A가 fatigue를 오히려 키울 위험. Soft/Hard/Trigger-based 중 → 사용자가 Soft 선택. 수렴.

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 위 패턴 중 어떤 게 본인이 겪은 '미결 질문 잔존'에 가장 가까우신가요?
**Options**: 1) 구현 시점으로 떠넘김 2) 의존성 체인 3) 수렴 신호 오발화 4) 전부 다
**A**: "1번과 2번; 구현 시점으로 떠넘김과 의존성 체인. 그리고 토론이 길어지면 그냥 빠르게 수렴하려는 현상"
**Follow-up**: 세 번째 응답이 깊이 신호. fatigue가 스킬의 수렴 메커니즘을 타고 조기 종료로 밀어붙이는 구조로 진단 격상.

### Round 2
**Q**: 세 대안 중 어떤 방향으로 가고 싶으신가요?
**Options**: 1) A+C(권장) 2) A만 3) B만 4) 비판적 검토
**A**: A+C 선택.
**Follow-up**: 비판적 검토(3.2.2) 차례 — A의 약점 도전 필요.

### Round 3
**Q**: A의 'deferral 분류 강제'를 어떻게 적용하면 fatigue를 안 키울까요?
**Options**: 1) Soft(권장) 2) Hard 3) Trigger-based
**A**: Soft 선택.
**Follow-up**: 수렴 신호 충족 → Step 4 정리.
