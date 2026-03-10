---
name: discussion
description: This skill should be used when the user asks to "discuss", "discussion", "토론", "토론하자", "let's discuss", "brainstorm", "논의", "의견 나누기", or wants a structured iterative discussion with research support.
version: 1.0.0
---

# Structured Discussion - Codex Interactive Discussion

구조화된 반복 토론을 진행한다. 프로빙 질문으로 주제를 심층 탐구하고, 코드베이스 탐색과 필요 시 웹 리서치를 병행하며, 토론 종료 시 구조화된 요약을 출력하고 최종 요약 파일만 저장한다.

## Workflow Position

| Workflow | Position | When |
|----------|----------|------|
| Any | Standalone | 기술적 주제에 대한 구조화된 토론 |
| Any | Pre-feature-draft | 방향/요구사항이 불명확할 때 토론 후 후속 스킬 연계 |

## When to Use This Skill

- 기술적 주제에 대해 깊이 있는 토론이 필요할 때
- 아키텍처/설계 결정을 논의할 때
- 기술 선택지를 비교·분석할 때
- 아이디어를 브레인스토밍할 때
- 문제 해결 방향을 함께 탐색할 때

## Hard Rules

1. **Interactive only**: 이 스킬은 반드시 `request_user_input`을 사용해야 한다. 현재 모드에서 `request_user_input`이 불가능하면 짧게 이유를 설명하고 즉시 중단한다.
2. **코드 수정 금지**: 구현 코드, 스펙 문서, 설정 파일을 수정하지 않는다. 마지막 Step 4에서 토론 요약 파일만 생성할 수 있다.
3. **Step 1-3은 읽기 전용**: `rg`, `Glob`, `Read`, 읽기 전용 `Bash`, `web`, `multi_tool_use.parallel`만 사용한다.
4. **언어 규칙**: 질문, 맥락 요약, 중간 요약, 최종 요약 출력, 저장 파일 내용은 모두 사용자의 활성 입력 언어를 따른다. 한국어로 시작하면 한국어, English로 시작하면 English, 그 외 언어로 시작하면 가능한 한 그 언어로 자연스럽게 진행한다. 토론 중 사용자가 언어를 전환하면 이후 대화와 최종 저장 파일도 그 언어를 따른다. 사용자가 별도의 출력 언어를 명시한 경우에만 예외를 둔다.
5. **종료 옵션 필수**: Step 1과 Step 3의 모든 `request_user_input` 질문에는 `정리/종료` 성격의 선택지를 반드시 포함한다.
6. **한 번에 한 질문**: `request_user_input`은 라운드당 정확히 1개의 질문만 사용한다.
7. **불안정한 사실은 검증**: 최신성이나 사실 검증이 필요한 내용은 웹 검색 또는 로컬 근거 확인 후 토론에 반영한다.
8. **최종 산출물 제한**: 생성 가능한 파일은 `_sdd/discussion/discussion_<title>.md` 하나뿐이다.

## Process

### Step 1: Topic Selection (토픽 선택)

**Tools**: `request_user_input`

사용자에게 토론 주제를 확인한다.

언어 처리:
- 첫 `request_user_input`을 만들기 전에 사용자의 최근 입력 언어를 식별한다.
- 이후 모든 질문 텍스트와 선택지 설명은 그 언어로 작성한다.
- 사용자가 중간에 언어를 바꾸면 다음 라운드부터 즉시 반영한다.

1. 사용자 입력에서 토픽이 이미 명시된 경우:
   - 토픽을 한 문장으로 재진술한다.
   - 바로 범위를 좁히는 1개 질문을 `request_user_input`으로 제시한다.

2. 토픽이 불명확한 경우:
   - 카테고리 질문을 `request_user_input`으로 제시한다.
   - 기본 선택지는 다음 세 가지를 사용한다:
     - 코드베이스 관련
     - 아키텍처 설계
     - 정리/종료
   - `request_user_input`의 자동 자유 입력을 통해 기술 선택, 기타 주제, 직접 입력을 받는다.

3. 범위 확인:
   - 두 번째 `request_user_input`으로 구체적인 범위를 좁힌다.
   - 예: "이번 토론에서 가장 먼저 정할 축은 무엇인가요?"

**Decision Gate 1→2**:
```
topic_defined = 토론 주제가 명확하게 정의됨
scope_clear = 토론 범위가 적절히 한정됨

IF topic_defined AND scope_clear → Step 2 진행
ELSE → request_user_input으로 최대 2라운드 보완
IF 2라운드 후에도 불명확 → 짧게 이유를 설명하고 스킬 중단
```

### Step 2: Context Gathering (맥락 수집)

**Tools**: `rg`, `Glob`, `Read`, 읽기 전용 `Bash`, `web`, `multi_tool_use.parallel`

토픽에 따라 필요한 맥락을 수집한다.

#### 2.1 토픽 유형별 자동 리서치

| 토픽 유형 | 자동 액션 | 우선 소스 |
|-----------|----------|-----------|
| 코드베이스 관련 | 구조, 관련 파일, 패턴, 의존성 탐색 | 로컬 코드베이스 |
| 아키텍처 설계 | 현재 구조 파악 + 관련 패턴 조사 | 로컬 코드베이스 + 웹 |
| 기술 선택 | 공식 문서/1차 자료 비교 | 웹 (공식/1차 자료 우선) |
| Other | 사용자 입력 기준으로 판단 | 로컬 또는 웹 |

#### 2.2 조사 전략

코드베이스 관련 토픽:
```
1. `rg`/`Glob`로 관련 파일과 디렉토리 찾기
2. `Read`로 핵심 파일만 읽기
3. 패턴, 컨벤션, 의존성 관계를 요약
```

기술 선택 / 아키텍처 토픽:
```
1. 로컬 구조 확인이 필요하면 코드베이스 탐색
2. 외부 정보가 필요하면 공식 문서/1차 자료 위주로 웹 리서치
3. 독립적인 로컬 탐색과 웹 리서치는 병렬로 수행
```

#### 2.3 맥락 요약

수집된 정보를 사용자에게 간략히 보고한다:

```markdown
## 수집된 맥락
| 항목 | 내용 |
|------|------|
| 관련 파일 | N개 식별 |
| 주요 패턴 | ... |
| 외부 참고 | ... (있는 경우) |
| 확인이 필요한 쟁점 | ... |
```

**Decision Gate 2→3**:
```
context_available = 맥락 정보가 최소 1개 이상 수집됨
topic_still_valid = 맥락 수집 후에도 토픽이 유효함

IF context_available AND topic_still_valid → Step 3 진행
ELSE → request_user_input으로
  1. 현재 맥락만으로 토론 진행
  2. 범위를 더 좁힘
  3. 정리/종료
```

### Step 3: Iterative Discussion (반복 토론)

**Tools**: `request_user_input`, `rg`, `Glob`, `Read`, 읽기 전용 `Bash`, `web`, `multi_tool_use.parallel`

핵심 토론 루프. 사용자와 반복적으로 심층 질문-답변을 수행한다.

> **라운드 정의**: 1라운드 = `request_user_input` 1회 + 사용자 응답 수신 + 응답 분석/반영

#### 3.1 토론 루프 구조

```
내부 상태 추적:
  key_points = []
  decisions = []
  open_questions = []
  action_items = []
  research_log = []
  conversation_log = []
  round = 0
  MAX_ROUNDS = 10

WHILE round < MAX_ROUNDS:
  round += 1

  1. 현재 맥락 기반 probing question 생성
  2. request_user_input으로 질문 제시
  3. 사용자 응답 분석
  4. key_points/decisions/open_questions/action_items 업데이트
  5. conversation_log에 {question, options, answer, follow_up} 기록
  6. 필요 시 추가 리서치 수행

  IF 사용자가 정리/종료 선택 OR "정리해줘" 입력:
    → Step 4 진행
```

#### 3.2 질문 생성 전략

| 토론 단계 | 질문 유형 | 예시 |
|-----------|----------|------|
| 초반 (round 1-3) | 범위 확인, 목표 정의 | "이번 결정에서 가장 중요한 목표는 무엇인가요?" |
| 중반 (round 4-6) | 트레이드오프, 대안 탐색 | "A와 B 중 어떤 비용을 더 감수할 수 있나요?" |
| 후반 (round 7+) | 합의 도출, 결정 확인 | "지금까지 논의를 바탕으로 X 방향으로 정리할까요?" |

#### 3.3 `request_user_input` 형식

매 라운드 질문 형식:

```text
question: "[probing question]"
options:
1. "[선택지 A]"
2. "[선택지 B]"
3. "정리/종료"
```

규칙:
- 옵션은 총 2-3개만 사용한다.
- 실질 선택지는 최대 2개로 제한하고, 마지막 1개는 `정리/종료`로 둔다.
- 명시적인 `Other` 옵션은 만들지 않는다. 자유 입력은 `request_user_input`의 자동 입력 경로를 사용한다.
- 사용자가 자유 입력으로 "추가 리서치 필요"를 적으면 Mid-Discussion Research로 연결한다.

#### 3.4 Mid-Discussion Research

토론 중 근거가 필요하면 즉시 조사한다.

트리거 조건:
- 사용자가 자유 입력으로 추가 리서치를 요청함
- 사용자가 사실 확인이 필요한 주장을 함
- 코드베이스 특정 부분에 대한 확인이 필요함
- 최신성 있는 외부 정보가 필요함

조사 방식:
```
코드 확인 필요 시:
  - `rg`/`Glob`/`Read`로 관련 코드 재탐색

외부 정보 필요 시:
  - 공식 문서, 1차 자료, 최신 소스를 우선해 웹 검색

독립적인 조사 2건 이상이면 병렬 수행
```

#### 3.5 라운드별 중간 상태 추적

매 3라운드마다 또는 사용자 요청 시 중간 요약을 제시한다:

```markdown
## 토론 중간 요약 (Round N)
| 항목 | 내용 |
|------|------|
| 핵심 논점 | N개 |
| 결정 사항 | N개 |
| 미결 질문 | N개 |
| 실행 항목 | N개 |
```

### Step 4: Discussion Summary (토론 정리)

**Tools**: `Bash (mkdir -p)`, `Write` 또는 `apply_patch` 상당 수단

토론 종료 시 구조화된 요약을 생성하고, `_sdd/discussion/discussion_<title>.md`로 저장한다.

#### 파일명 생성 규칙

- 소문자, 숫자, `_`만 사용
- 특수문자와 공백은 `_`로 대체
- 최대 50자
- 파일명은 항상 영문 slug 사용

#### 요약 언어 규칙

- 대화에 출력하는 최종 요약과 저장 파일 내용은 모두 사용자의 마지막 활성 입력 언어로 작성한다.
- 사용자가 토론 중간에 언어를 바꿨다면, 최종 요약과 저장 파일은 마지막으로 사용한 언어를 따른다.
- 사용자가 저장 언어를 별도로 명시한 경우에만 그 지시를 우선한다.

#### 완료 절차

1. 완료 요약 테이블을 먼저 제시한다.
2. 전체 요약을 대화에 출력한다.
3. `_sdd/discussion/`가 없으면 생성한다.
4. `_sdd/discussion/discussion_<title>.md`에 저장한다.
5. 추가 확인을 기다리지 않는다.

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
- [ ] [질문 2]: [맥락]

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | ... | High/Medium/Low | ... |

## 리서치 결과 요약 (Research Findings)
- [수집 항목 1]: [핵심 발견]

## Sources
- [source name](https://...)

## 토론 흐름 (Discussion Flow)
Round 1: [주제] → [결론/방향]
Round 2: [주제] → [결론/방향]
```

## Context Management

| 라운드 수 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 5 | 전체 추적 | 모든 논점, 결정, 질문을 내부 상태로 유지 |
| 5-8 | 요약 추적 | 핵심 논점만 유지, 세부 사항은 요약 |
| > 8 | 압축 추적 | 이전 라운드 세부 사항을 압축하고 결정 중심으로 유지 |

## Error Handling

| 상황 | 대응 |
|------|------|
| `request_user_input` 사용 불가 | 짧게 이유 설명 후 즉시 중단 |
| 사용자가 토픽을 정하지 못함 | 최대 2라운드까지 범위 질문 후 중단 |
| 로컬 맥락 부족 | 범위를 더 좁히거나 현재 정보만으로 진행할지 `request_user_input`으로 확인 |
| 외부 리서치 실패 | 실패 사실을 밝히고 수집된 맥락만으로 계속 진행 |
| MAX_ROUNDS 도달 | 자동으로 Step 4 진행 |
| 다국어 혼재 | 사용자 주 사용 언어로 통일 |

## Integration with Other Skills

이 스킬은 다른 SDD 스킬과 독립적으로 동작하지만, 결과를 후속 작업에 연결하기 좋다.

- **spec-create**: 토론에서 도출된 요구사항을 바탕으로 스펙 문서 생성
- **feature-draft**: 토론에서 정리된 기능 방향을 기반으로 기능 초안 작성
- **implementation-plan**: 토론에서 합의된 아키텍처로 구현 계획 수립

> 참고: 이 스킬은 마지막에 토론 요약 파일만 생성한다. 후속 스킬은 해당 요약을 입력 맥락으로 사용하면 된다.

## Additional Resources

- `references/discussion-question-guide.md` - 질문 전략과 `request_user_input` 설계 가이드
- `examples/sample-discussion-session.md` - 구조화된 토론 세션 예시
