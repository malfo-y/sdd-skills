---
name: discussion
description: This skill should be used when the user asks to "discuss", "discussion", "토론", "토론하자", "let's discuss", "brainstorm", "논의", "의견 나누기", or wants a structured iterative discussion with research support.
version: 1.1.0
---

# discussion

## Goal

구조화된 반복 토론으로 주제를 좁히고, 필요한 맥락을 수집하며, 최종적으로 `_sdd/discussion/discussion_<title>.md`에 토론 요약을 저장한다. 구현이나 스펙 수정은 하지 않고, 후속 스킬이 사용할 수 있는 결정과 open question을 정리하는 데 집중한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: 토론 주제와 범위를 명확히 했다.
- [ ] AC2: 필요한 로컬 맥락 또는 최신 외부 사실을 수집했다.
- [ ] AC3: 반복 토론 중간에 핵심 논점, 결정, 미결 질문을 추적했다.
- [ ] AC4: `_sdd/discussion/discussion_<title>.md`를 생성했다.
- [ ] AC5: 최종 요약에 논점, 결정, open question, action item이 포함되었다.

## Companion Assets

- `references/discussion-question-guide.md`
- `examples/sample-discussion-session.md`

## Hard Rules

1. 이 스킬은 interactive-only다. `request_user_input`을 사용할 수 없으면 즉시 중단한다.
2. 코드, 스펙, 설정 파일은 수정하지 않는다. 생성 가능한 파일은 `_sdd/discussion/discussion_<title>.md` 하나뿐이다.
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
  round = 0, MAX_ROUNDS = 10

WHILE round < MAX_ROUNDS:
  round += 1
  1. 현재 맥락 기반으로 probing question 생성
  2. ask로 질문 제시 (옵션 3개 + "토론 종료")
  3. 사용자 응답 분석 → 내부 상태 업데이트
  4. 필요 시 mid-discussion 리서치 수행

  IF 사용자가 "토론 종료" 선택 OR "정리해줘" 입력 → Gate 3→4
```

#### 3.2 질문 생성 전략

초반(1-3) 범위/목표 확인 → 중반(4-6) 트레이드오프/대안 탐색 → 후반(7+) 합의/결정 확인. 옵션은 상호 배타적이고 포괄적으로 구성하며, 이미 답한 내용은 재질문하지 않는다.

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

**Gate 3→4**: 미결 질문(open_questions)을 확인한다.
- 0건 → Step 4 진행
- 1건+ → 미결 질문 목록을 제시하고 추가 논의 여부를 확인한다. 추가 논의 선택 시 Step 3 루프 복귀, 그대로 정리 선택 시 Step 4 진행.

### Step 4: Write the Discussion Summary

`_sdd/discussion/discussion_<title>.md`에 아래를 저장한다.

- 핵심 논점
- 결정 사항
- 미결 질문
- 실행 항목
- 리서치 결과 요약
- sources
- 토론 흐름

파일명은 영문 slug를 사용하고, `_sdd/discussion/`가 없으면 생성한다.

## Output Contract

기본 산출물: `_sdd/discussion/discussion_<title>.md`

파일명은 영문 slug를 사용한다 (예: "인증 시스템 설계" -> `discussion_auth_system_design.md`). 소문자, 특수문자는 `_`로 대체, 최대 50자.

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
| 최대 라운드 도달 | 자동으로 요약 단계로 이동 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

