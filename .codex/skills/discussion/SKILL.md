---
name: discussion
description: This skill should be used when the user asks to "discuss", "discussion", "토론", "토론하자", "let's discuss", "brainstorm", "논의", "의견 나누기", or wants a structured iterative discussion with research support.
version: 1.2.0
---

# discussion

## Goal

구조화된 반복 토론으로 주제를 좁히고, 필요한 맥락을 수집하며, 최종적으로 `_sdd/discussion/<YYYY-MM-DD>_discussion_<slug>.md`에 토론 요약을 저장한다. 구현이나 스펙 수정은 하지 않고, 후속 스킬이 사용할 수 있는 결정과 open question을 정리하는 데 집중한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: 토론 주제와 범위를 명확히 했다.
- [ ] AC2: 필요한 로컬 맥락 또는 최신 외부 사실을 수집했다.
- [ ] AC3: 반복 토론 중간에 핵심 논점, 결정, 미결 질문을 추적했다.
- [ ] AC4: `_sdd/discussion/<YYYY-MM-DD>_discussion_<slug>.md`를 생성했다.
- [ ] AC5: 최종 요약에 논점, 결정, open question, action item이 포함되었다.

## Companion Assets

- `references/discussion-question-guide.md`
- `examples/sample-discussion-session.md`

## Hard Rules

1. 이 스킬은 interactive-only다. `request_user_input`을 사용할 수 없으면 즉시 중단한다.
2. 코드, 스펙, 설정 파일은 수정하지 않는다. 생성 가능한 파일은 `_sdd/discussion/<YYYY-MM-DD>_discussion_<slug>.md` 하나뿐이다.
3. Step 1-3은 읽기 전용 탐색만 사용한다.
4. 모든 질문에는 `정리/종료` 성격의 선택지를 넣는다.
5. 라운드당 질문은 정확히 1개만 한다.
6. 최신성이나 사실 검증이 필요한 내용은 웹 또는 로컬 근거로 먼저 확인한다.
7. 출력 언어와 저장 파일 언어는 사용자의 활성 입력 언어를 따른다.

## Process

### Step 1: Define the Topic

- 사용자 요청에서 토픽이 이미 있으면 재진술 후 범위를 좁히는 질문 1개를 한다.
- 불명확하면 카테고리 수준에서 묻고, 최대 2라운드 안에 범위를 정한다.
- 범위를 정하지 못하면 이유를 설명하고 중단한다.

**Decision Gate 1 -> 2**: `topic_defined AND scope_clear` -> Step 2 진행. ELSE -> 보완 질문 (최대 2라운드).

### Step 2: Gather Context

토픽 유형에 따라 필요한 맥락을 수집한다.

- 코드베이스 관련: 관련 파일, 패턴, 의존성
- 아키텍처/기술 선택: 로컬 구조 + 공식 자료/1차 자료
- 기타 주제: 사용자 맥락 기준으로 탐색

이후 짧은 context summary를 제시한다.

**Decision Gate 2 -> 3**: `context_available AND topic_still_valid` -> Step 3 진행. 맥락 없으면 사용자에게 확인. 토픽 무효화 시 Step 1 복귀.

### Step 3: Run Iterative Discussion

#### 3.1 토론 루프 구조

```
내부 상태 추적:
  key_points, decisions, open_questions, action_items, conversation_log
  round = 0

  coverage:
    exploration:
      motivation, current_state, constraints, ideal_outcome
    analysis:
      alternatives, tradeoffs, priorities, critical_review
    convergence:
      conclusion, risks, action_items

LOOP:
  round += 1
  1. 질문 선택 (아래 3.2 전략)
  2. ask로 질문 제시 (옵션 2-3개 + "토론 종료")
  3. 사용자 응답 분석 → 내부 상태 + coverage 업데이트
  4. 필요 시 mid-discussion 리서치 수행
  5. 수렴 신호 감지 시 → 종료 권유 (아래 3.5)

  IF 사용자가 "토론 종료" 선택 OR "정리해줘" 입력 → Gate 3→4
```

#### 3.2 질문 선택 전략 (커버리지 기반 하이브리드)

라운드 번호가 아닌 **커버리지 달성도**가 페이즈를 결정한다.

**매 라운드 질문 선택 로직:**

```
1. 직전 답변에서 "깊이 신호" 감지?
   → YES: 페이즈를 무시하고 후속 질문 (깊이 우선)
   → NO:  2단계로

2. 커버리지 맵에서 현재 페이즈 판정:
   - exploration 미확인 항목 있음 → 탐색 질문
   - exploration 완료, analysis 미확인 있음 → 분석 질문
   - 둘 다 완료 → 수렴 질문
```

**깊이 신호 (페이즈 무시하고 파고드는 트리거):**

| 신호 | 예시 |
|------|------|
| 모순 발견 | "빠르게 만들고 싶은데 확장성도 중요해요" |
| 불확실성 표현 | "잘 모르겠는데...", "아마..." |
| 새 제약조건 등장 | "아, 근데 레거시 API랑 호환돼야 해요" |
| 강한 의견 | "이건 절대 안 돼요" → 이유를 파고들기 |

**수렴 전 안전장치:** 수렴 페이즈 진입 전 exploration/analysis에 미확인 항목이 있으면 사용자에게 "아직 [항목]을 다루지 않았는데, 넘어가도 괜찮을까요?" 확인.

#### 3.2.1 비판적 개입 (Critical Review)

분석 페이즈에서는 최소 1회 **비판적 질문**으로 약점이나 숨은 가정을 검증한다.

- 사용자가 특정 방향에 합의/선호를 표현하면 그 방향에 대해 비판적 질문을 우선 제시한다.
- 사용자가 끝까지 중립 비교 상태라면, 현재 가장 가능성이 높은 방향이나 공통 가정을 임시 가설로 잡고 비판적 질문을 1회 수행한다.
- 임시 가설도 성립하지 않으면 "가장 우려되는 실패 시나리오" 또는 "지금 가정이 틀리면 무엇이 깨지는지"를 묻는 방식으로 `critical_review`를 충족한다.

**비판적 개입 유형:**

| 유형 | 언제 | 예시 |
|------|------|------|
| 약점 지적 | 방향이 정해졌을 때 | "이 방식이면 X 상황에서 문제가 될 수 있는데, 어떻게 생각하세요?" |
| 반례 제시 | 장점만 언급될 때 | "비슷한 접근을 한 Y 사례에서는 Z 문제가 있었어요" |
| 숨은 가정 질문 | 전제가 검증 안 됐을 때 | "이건 A라는 가정 위에 서 있는데, 그게 깨지면요?" |
| 대안 제안 | 탐색 범위가 좁을 때 | "다른 관점에서 보면 이런 접근도 가능한데, 고려해 보셨나요?" |
| 스케일 도전 | 현재 규모만 고려할 때 | "지금은 괜찮지만 10배 커지면 이 구조가 버틸까요?" |

**강도 조절 규칙:**

1. 연속 2라운드 이상 비판 금지 → 반드시 건설적 질문 삽입
2. 비판 후에는 대안이나 보완책을 함께 제시
3. 사용자가 이미 반박한 약점은 재차 제기하지 않음
4. 비판은 "질문" 형태로 — 단정이 아니라 탐색 유도

**커버리지 체크:** `critical_review`는 분석 페이즈에서 최소 1회 비판적 개입이 이루어지고 사용자가 응답했을 때 완료로 표시한다. 선호가 없는 비교형 토론도 fallback 비판 질문으로 완료 가능해야 한다. 비판적 검토 없이 수렴으로 넘어가는 것을 방지한다.

#### 3.3 Mid-Discussion Research

토론 중 근거가 필요하면 리서치를 즉시 수행:

| 트리거 | 액션 |
|--------|------|
| "추가 리서치 필요" 선택 | 웹/외부 자료 검색 |
| 코드베이스 확인 필요 | 로컬 파일 탐색 |
| 사실 확인 필요한 주장 | 공식 문서/1차 자료 확인 |

독립적인 리서치 2건 이상이면 병렬 수행.

#### 3.4 중간 상태 추적

매 3라운드마다 (또는 사용자 요청 시) 핵심 논점/결정 사항/미결 질문/실행 항목 카운트를 중간 요약 테이블로 제시.

#### 3.5 수렴 신호 감지 및 종료 유도

라운드 수 제한 없이, 아래 **수렴 신호**가 충분히 감지되면 종료를 권유한다.

**수렴 신호:**

| 신호 | 감지 기준 |
|------|----------|
| 반복 합의 | 사용자가 연속 2라운드 이상 동의/확인 응답 |
| 새 정보 없음 | 직전 라운드에서 key_points/decisions에 추가된 항목 없음 |
| 명시적 만족 | "좋아요", "그걸로 하죠", "충분해요" 등 |
| 커버리지 충족 | exploration + analysis 항목 모두 완료 |

**2개 이상 신호 동시 감지 시:**
```
"지금까지 [N]개 논점을 다루고 [M]개 결정을 내렸습니다.
 정리해도 좋을 것 같은데, 더 논의할 내용이 있으신가요?"
 1) "정리해줘"
 2) "[추가 논의 주제 제안]"
```

사용자가 추가 논의를 선택하면 계속 진행한다. 종료를 강제하지 않는다.

#### 3.5.1 Stagnation Fallback

토론이 길어지더라도 **단순 라운드 수로 종료하지 않는다**. 대신 아래 정체(stagnation) 신호를 본다.

**stagnation 신호:**

| 신호 | 감지 기준 |
|------|----------|
| 새 정보 없음 | 연속 라운드에서 `key_points`나 `decisions`가 늘지 않음 |
| 미결 질문 정체 | 같은 open question이 재진술되지만 진전이 없음 |
| 반복 유보 | 사용자가 연속적으로 모호한 답변, 유보, "더 봐야 할 것 같아요" 류 응답을 함 |

**stagnation 대응 규칙:**

1. stagnation 신호가 2회 연속 감지되면 질문 범위를 강제로 좁힌다.
2. 이때 질문은 아래 둘 중 하나만 제시한다.
   - "지금까지 정리"
   - "남은 미결 1개만 더 논의"
3. 사용자가 "남은 미결 1개만 더 논의"를 선택했는데 다음 라운드도 stagnation이면, 남은 쟁점은 open question으로 기록하고 Step 4로 이동한다.
4. 이 fallback은 토론을 강제로 닫기 위한 것이 아니라, 진전 없는 반복을 요약 가능한 상태로 전환하기 위한 것이다.

**Gate 3→4**: 미결 질문(open_questions)을 확인한다.
- 0건 → Step 4 진행
- 1건+ → 미결 질문 목록을 제시하고 추가 논의 여부를 확인한다. 추가 논의 선택 시 Step 3 루프 복귀, 그대로 정리 선택 시 Step 4 진행.

### Step 4: Write the Discussion Summary

`_sdd/discussion/<YYYY-MM-DD>_discussion_<slug>.md`에 아래를 저장한다.

- 핵심 논점
- 결정 사항
- 미결 질문
- 실행 항목
- 리서치 결과 요약
- sources
- 토론 흐름

파일명은 영문 slug를 사용하고, `_sdd/discussion/`가 없으면 생성한다.

## Output Contract

기본 산출물: `_sdd/discussion/<YYYY-MM-DD>_discussion_<slug>.md`

파일명은 `<YYYY-MM-DD>_discussion_<slug>.md` 패턴을 사용한다. slug는 영문 소문자, 특수문자는 `_`로 대체, 최대 50자 (예: "인증 시스템 설계" → `2026-04-10_discussion_auth_system_design.md`).

#### 요약 출력 형식

```markdown
# 토론 요약: [토픽]

**날짜**: YYYY-MM-DD
**라운드 수**: N
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)
1. [논점 1]: [요약]
2. [논점 2]: [요약]

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | ... | ... | ... |

## 미결 질문 (Open Questions)
- [ ] [질문 1]: [맥락]

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | ... | High/Medium/Low | ... |

## 리서치 결과 요약 (Research Findings)
- [수집 항목 1]: [핵심 발견]

## 토론 흐름 (Discussion Flow)
Round 1: [주제] → [결론/방향]
...

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: [질문 내용]
**Options**: 1) ... 2) ... 3) ... 4) 토론 종료
**A**: [사용자 응답 요약]
**Follow-up**: [AI 분석/코멘트 요약]
...
```

## Error Handling

| 상황 | 대응 |
|------|------|
| `request_user_input` 불가 | 즉시 중단 |
| 토픽 불명확 | 최대 2라운드 범위 질문 후 중단 |
| 로컬 맥락 부족 | 범위를 좁히거나 현재 정보 기준으로 계속할지 확인 |
| 외부 리서치 실패 | 실패 사실을 밝히고 수집된 맥락만으로 진행 |
| 토론이 지나치게 길어짐 | stagnation 신호를 확인하고 "지금 정리 / 미결 1개만 더 논의"로 범위를 축소 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
