---
name: discussion
description: This skill should be used when the user asks to "discuss", "discussion", "토론", "토론하자", "let's discuss", "brainstorm", "논의", "의견 나누기", or wants a structured iterative discussion with research support.
version: 1.0.0
---

# Structured Discussion - 구조화된 토론 진행

구조화된 반복 토론을 진행한다. 프로빙 질문으로 주제를 심층 탐구하고, sub-agent를 활용해 코드베이스 탐색 및 웹 리서치를 수행하며, 토론 종료 시 구조화된 요약을 텍스트로 출력한다. **파일 생성/수정 없이 텍스트 출력만** 수행한다.

## When to Use This Skill

- 기술적 주제에 대해 깊이 있는 토론이 필요할 때
- 아키텍처/설계 결정을 논의할 때
- 기술 선택지를 비교·분석할 때
- 아이디어를 브레인스토밍할 때
- 문제 해결 방향을 함께 탐색할 때

## Hard Rules

1. **코드 수정 금지**: `Edit`, `Write`, `Bash`(mutation 명령) 사용을 금지한다. 읽기 전용 도구만 사용한다.
2. **파일 생성 금지**: 어떤 파일도 생성하지 않는다. 최종 요약은 대화 내 텍스트로만 출력한다.
3. **읽기 전용 도구만 허용**: `Read`, `Glob`, `Grep`, `AskUserQuestion`, `Agent`(sub-agent)만 사용 가능하다.
4. **한국어 기본**: 토론 내용과 요약은 한국어로 작성한다 (사용자가 다른 언어 지정 시 해당 언어 사용).
5. **토론 종료 옵션 항상 포함**: Step 3의 매 질문에 "토론 종료 / 정리해줘" 옵션을 반드시 포함한다.

## Process

### Step 1: Topic Selection (토픽 선택)

**Tools**: `AskUserQuestion`

사용자에게 토론 주제를 확인한다.

1. 사용자 입력에서 토픽이 이미 명시된 경우:
   - 토픽을 요약하여 확인 질문

2. 토픽이 불명확한 경우:
   ```
   AskUserQuestion: "어떤 주제에 대해 토론하고 싶으신가요?"
   옵션:
   1. "코드베이스 관련 (구조, 패턴, 리팩토링 등)"
   2. "아키텍처 설계 (시스템 설계, 컴포넌트 구조 등)"
   3. "기술 선택 (라이브러리, 프레임워크, 도구 비교)"
   ```

3. 선택된 토픽에 대해 구체적인 범위를 확인:
   ```
   AskUserQuestion: "[선택 카테고리]에서 구체적으로 어떤 부분을 논의하고 싶으신가요?"
   - 자유 형식 응답 수용
   ```

**Decision Gate 1→2**:
```
topic_defined = 토론 주제가 명확하게 정의됨
scope_clear = 토론 범위가 적절히 한정됨

IF topic_defined AND scope_clear → Step 2 진행
ELSE → AskUserQuestion으로 보완 (최대 2라운드)
```

### Step 2: Context Gathering (맥락 수집)

**Tools**: `Agent` (Explore, general-purpose), `Read`, `Glob`, `Grep`

토픽에 따라 자동으로 관련 자료를 수집한다.

#### 2.1 토픽 유형별 자동 리서치

| 토픽 유형 | 자동 액션 | Sub-agent 유형 |
|-----------|----------|----------------|
| 코드베이스 관련 | 코드베이스 구조/패턴/관련 파일 탐색 | Explore |
| 아키텍처 설계 | 현재 아키텍처 파악 + 관련 패턴 리서치 | Explore + general-purpose (병렬) |
| 기술 선택 | 후보 기술 비교 자료 수집 | general-purpose |
| Other | 사용자 입력 기반 판단 | 필요시 Explore 또는 general-purpose |

#### 2.2 Sub-agent Dispatch

코드베이스 관련 토픽:
```
Agent(
  subagent_type="Explore",
  prompt="다음 토픽에 관련된 코드베이스 정보를 수집하세요: [토픽]

  수집 대상:
  - 관련 파일/디렉토리 구조
  - 주요 패턴 및 컨벤션
  - 관련 코드 스니펫 (핵심부만)
  - 의존성 관계

  결과를 구조화된 형태로 보고하세요."
)
```

기술 선택 / 아키텍처 토픽:
```
Agent(
  subagent_type="general-purpose",
  prompt="다음 토픽에 대한 리서치를 수행하세요: [토픽]

  수집 대상:
  - 관련 기술/패턴의 장단점
  - 업계 best practices
  - 대안 비교 (있는 경우)

  결과를 구조화된 형태로 보고하세요."
)
```

병렬 디스패치: 아키텍처 토픽의 경우 두 sub-agent를 동시에 호출하여 코드베이스 현황과 외부 리서치를 병렬로 수집한다.

#### 2.3 맥락 요약

수집된 정보를 사용자에게 간략히 보고:
```
## 수집된 맥락
| 항목 | 내용 |
|------|------|
| 관련 파일 | N개 식별 |
| 주요 패턴 | ... |
| 외부 참고 | ... (있는 경우) |
```

**Decision Gate 2→3**:
```
context_available = 맥락 정보가 최소 1개 이상 수집됨
topic_still_valid = 맥락 수집 후에도 토픽이 유효함

IF context_available AND topic_still_valid → Step 3 진행
IF NOT context_available → 맥락 없이 토론 진행 가능 여부 AskUserQuestion
IF NOT topic_still_valid → Step 1로 돌아가 토픽 재조정
```

### Step 3: Iterative Discussion (반복 토론)

**Tools**: `AskUserQuestion`, `Agent` (Explore, general-purpose), `Read`, `Glob`, `Grep`

핵심 토론 루프. 사용자와 반복적으로 심층 질문-답변을 수행한다.

#### 3.1 토론 루프 구조

```
내부 상태 추적:
  key_points = []      # 핵심 논점
  decisions = []       # 결정 사항
  open_questions = []  # 미결 질문
  action_items = []    # 실행 항목
  round = 0
  MAX_ROUNDS = 10      # 안전 제한

WHILE round < MAX_ROUNDS:
  round += 1

  1. 현재 맥락 기반으로 probing question 생성
  2. AskUserQuestion으로 질문 제시 (옵션 3개 + "토론 종료")
  3. 사용자 응답 분석
  4. key_points/decisions/open_questions/action_items 업데이트
  5. 필요 시 mid-discussion sub-agent 리서치 수행

  IF 사용자가 "토론 종료" 선택 OR "정리해줘" 입력:
    → Step 4 진행
```

#### 3.2 질문 생성 전략

| 토론 단계 | 질문 유형 | 예시 |
|-----------|----------|------|
| 초반 (round 1-3) | 범위 확인, 목표 정의 | "이 결정의 주요 목표는 무엇인가요?" |
| 중반 (round 4-6) | 트레이드오프, 대안 탐색 | "A 방식과 B 방식의 트레이드오프를 어떻게 보시나요?" |
| 후반 (round 7+) | 합의 도출, 결정 확인 | "지금까지 논의를 바탕으로 X로 결정해도 될까요?" |

#### 3.3 AskUserQuestion 형식

매 라운드 질문 형식:
```
AskUserQuestion: "[probing question]"
옵션:
1. "[관련 선택지 A]"
2. "[관련 선택지 B]"
3. "[관련 선택지 C]"
4. "토론 종료 / 정리해줘"
```

자유 형식 답변이 필요한 경우:
```
AskUserQuestion: "[open-ended question]"
옵션:
1. "[힌트/방향 A]"
2. "[힌트/방향 B]"
3. "잘 모르겠어요 (추가 리서치 필요)"
4. "토론 종료 / 정리해줘"
```

#### 3.4 Mid-Discussion Research

토론 중 근거가 필요하면 sub-agent를 즉시 디스패치:

트리거 조건:
- 사용자가 "잘 모르겠어요 (추가 리서치 필요)" 선택
- 사용자가 사실 확인이 필요한 주장을 함
- 코드베이스 특정 부분에 대한 확인이 필요

```
코드 확인 필요 시:
Agent(subagent_type="Explore", prompt="토론 중 다음 사항을 확인: [확인 사항]")

외부 정보 필요 시:
Agent(subagent_type="general-purpose", prompt="다음 사항에 대한 리서치: [리서치 주제]")
```

독립적인 리서치 2건 이상이면 병렬 디스패치.

#### 3.5 라운드별 중간 상태 추적

매 3라운드마다 (또는 사용자 요청 시) 중간 요약 제시:
```
## 토론 중간 요약 (Round N)
| 항목 | 내용 |
|------|------|
| 핵심 논점 | N개 |
| 결정 사항 | N개 |
| 미결 질문 | N개 |
| 실행 항목 | N개 |
```

### Step 4: Discussion Summary (토론 정리)

**Tools**: 없음 (텍스트 출력만)

토론 종료 시 구조화된 요약을 대화 내 텍스트로 출력한다.

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

## 토론 흐름 (Discussion Flow)
Round 1: [주제] → [결론/방향]
Round 2: [주제] → [결론/방향]
...
```

## Progressive Disclosure (완료 시)

```
1. 완료 요약 테이블 제시:
   | 항목 | 내용 |
   |------|------|
   | 토론 주제 | [토픽] |
   | 총 라운드 | N |
   | 결정 사항 | N개 |
   | 미결 질문 | N개 |
   | 실행 항목 | N개 |
   | 리서치 수행 | N건 |

2. AskUserQuestion: "요약 내용을 확인하시겠습니까?"
   옵션:
   1. "전체 요약 보기" → 전체 요약 출력
   2. "결정 사항만 보기" → 결정 사항 섹션만 출력
   3. "실행 항목만 보기" → 실행 항목 섹션만 출력
   4. "확인 완료" → 종료
```

## Context Management

### 토론 상태 크기 관리

| 라운드 수 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 5 | 전체 추적 | 모든 논점, 결정, 질문을 내부 상태로 유지 |
| 5-8 | 요약 추적 | 핵심 논점만 유지, 세부 사항은 요약 |
| > 8 | 압축 추적 | 중간 요약 생성 후 이전 라운드 상세 내용 압축 |

### Sub-agent 결과 관리

- Sub-agent 결과는 핵심 발견만 추출하여 토론 맥락에 통합
- 전체 리서치 결과는 요약 시 "리서치 결과 요약" 섹션에 포함
- 동일 주제 재리서치 방지: 이전 리서치 주제 목록 유지

## Error Handling

| 상황 | 대응 |
|------|------|
| 사용자가 토픽을 정하지 못함 | 카테고리별 예시 제시, 최대 2라운드 질문 후 자유 주제로 진행 |
| Sub-agent 실패 | 실패 사실 보고, 토론은 수집된 맥락으로 계속 진행 |
| 사용자 응답 없음/중단 | 현재까지의 토론 내용으로 부분 요약 생성 |
| 토론이 범위를 벗어남 | 원래 토픽 리마인드, 범위 재조정 질문 |
| MAX_ROUNDS 도달 | 자동으로 Step 4 진행, 안내 메시지 출력 |
| 코드베이스 접근 불가 | Explore agent 스킵, 외부 리서치만으로 진행 |
| 다국어 혼재 | 사용자 주 사용 언어 감지, 해당 언어로 전환 |

## Best Practices

### 효과적인 토론 진행
- 한 번에 하나의 논점에 집중한다
- 사용자 답변을 paraphrase하여 이해 확인
- 트레이드오프를 명시적으로 제시한다
- 결정 사항은 즉시 추적 상태에 기록한다

### 질문 품질
- 열린 질문과 닫힌 질문을 적절히 혼합한다
- 옵션은 상호 배타적이고 포괄적이어야 한다
- 사용자가 이미 답한 내용을 재질문하지 않는다

### Sub-agent 활용
- 리서치가 토론 흐름을 방해하지 않도록 한다
- 동일 주제를 반복 리서치하지 않는다
- 독립 리서치는 병렬 디스패치한다

## Integration with Other Skills

이 스킬은 다른 SDD 스킬과 독립적으로 동작하지만, 토론 결과를 후속 작업에 활용할 수 있다:

- **spec-create**: 토론에서 도출된 요구사항을 바탕으로 스펙 문서 생성
- **feature-draft**: 토론에서 결정된 기능 방향을 기반으로 기능 초안 작성
- **implementation-plan**: 토론에서 합의된 아키텍처로 구현 계획 수립

> 참고: 토론 스킬은 파일을 생성하지 않으므로, 토론 결과를 후속 스킬에 활용하려면 사용자가 요약 내용을 참조하여 해당 스킬을 별도로 실행해야 한다.

## Additional Resources

### Reference Files
- **`references/discussion-question-guide.md`** - 토론 질문 템플릿 및 전략 가이드

### Example Files
- **`examples/sample-discussion-session.md`** - 구조화된 토론 세션 예시
