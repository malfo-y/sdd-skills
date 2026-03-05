---
name: discussion
description: This skill should be used when the user asks to "discuss", "discussion", "토론", "토론하자", "let's discuss", "brainstorm", "논의", "의견 나누기", or wants a structured iterative discussion with research support in Plan mode.
version: 1.0.0
---

# Structured Discussion (Plan Mode Only) - 구조화된 토론 진행

구조화된 반복 토론을 진행한다. 질문-응답 루프로 주제를 심층 탐구하고, 필요 시 코드베이스 탐색 및 선택적 웹 리서치를 통해 근거를 보강한다. 토론 종료 시 구조화된 요약을 대화 내 텍스트로 출력하며, 원할 경우 Plan mode 종료 후 저장할 수 있도록 저장 핸드오프를 생성한다.

## When to Use This Skill

- 기술적 주제에 대해 깊이 있는 토론이 필요할 때
- 아키텍처/설계 결정을 논의할 때
- 기술 선택지를 비교/분석할 때
- 아이디어를 브레인스토밍할 때
- 문제 해결 방향을 함께 탐색할 때

## Hard Rules

1. **Plan mode 전용**: 이 스킬의 질문 루프는 Plan mode에서만 동작한다.
2. **Default mode 즉시 종료(강제)**: Default mode에서 호출되면 아래 문구를 **그대로 1회만 출력**하고 즉시 종료한다.
   - "`discussion` 스킬은 Plan mode 전용입니다. Shift+Tab으로 Plan mode로 전환 후 다시 실행해 주세요."
3. **Default mode 추가 동작 금지(강제)**: Default mode에서는 추가 설명, 후속 질문, 요약, 코드베이스 탐색, 웹 리서치, 파일 작업, 다른 스킬 연계를 수행하지 않는다.
4. **Plan mode 내 파일 변경 금지**: Plan mode 중에는 파일 생성/수정/삭제를 수행하지 않는다. 토론 결과는 텍스트로 출력한다.
5. **도구 제한**: `request_user_input`(Plan mode), `Read`, `Glob`, `rg`, `Bash`(read-only), 선택적 웹 리서치(`search_query`, `open`)만 사용한다.
6. **질문 옵션 규칙**: `request_user_input`의 옵션은 2~3개를 유지하고, 권장 구성은 `실질 선택지 2개 + 토론 종료/정리 1개`다.
7. **언어 규칙**: 기본 출력 언어는 한국어로 한다. 사용자가 다른 언어를 명시하면 해당 언어를 따른다.
8. **저장 방식 규칙**: 저장은 Plan mode에서 직접 실행하지 않고, Plan mode 종료 후 실행할 저장 핸드오프(경로 + 내용 + 실행 프롬프트)를 생성한다.

## Process

### Step 0: Mode Check

**Tools**: 없음

1. 현재 실행 모드를 확인한다.
2. If Plan mode:
   - Step 1로 진행.
3. If Default mode:
   - Hard Rule 2의 안내 문구를 그대로 1회 출력한다.
   - 즉시 종료한다.
   - Step 1 이후 단계를 절대 수행하지 않는다.

간단 의사코드:

```text
IF mode != Plan:
  OUTPUT "`discussion` 스킬은 Plan mode 전용입니다. Shift+Tab으로 Plan mode로 전환 후 다시 실행해 주세요."
  STOP
ELSE:
  CONTINUE Step 1
```

### Step 1: Topic Selection (토픽 선택)

**Tools**: `request_user_input` (Plan mode)

1. 사용자 입력에서 토픽이 명확하면 간단히 범위를 재확인한다.
2. 토픽이 불명확하면 카테고리 선택 질문으로 시작한다.
3. 아래 4개를 확보한다.
   - 토픽
   - 목표
   - 범위(in/out)
   - 제약(시간/리스크/기술)

예시 질문:

```text
질문: "어떤 관점으로 토론할지 선택해 주세요."
옵션:
1. "코드베이스 중심 (구조/패턴/리팩토링)"
2. "설계/기술 선택 중심 (아키텍처/도구 비교)"
3. "토론 종료 / 정리"
```

**Decision Gate 1→2**:

```text
topic_defined = 토픽이 명확히 정의됨
goal_defined = 토론 목표가 정의됨
scope_defined = 범위(in/out)가 정의됨

IF topic_defined AND goal_defined AND scope_defined -> Step 2 진행
ELSE -> request_user_input으로 최대 2라운드 보완
```

### Step 2: Context Gathering (맥락 수집)

**Tools**: `Read`, `Glob`, `rg`, `Bash` (read-only), 선택적 `search_query`, `open`

로컬 코드베이스를 우선 탐색하고, 최신성 또는 외부 비교가 필요할 때만 웹 리서치를 수행한다.

#### 2.1 로컬 우선 탐색

1. `rg`/`Glob`로 관련 파일 후보를 수집한다.
2. `Read`로 핵심 파일만 읽어 현재 구조/패턴/제약을 파악한다.
3. 관련 근거를 "사실"과 "추론"으로 구분해 메모한다.

#### 2.2 선택적 웹 리서치

아래 조건에서만 웹 리서치를 추가한다.

- 라이브러리/프레임워크/표준의 최신 정보가 핵심일 때
- 코드베이스 내부 근거만으로 대안 비교가 불충분할 때
- 버전/정책/호환성 등 변동 가능성이 높은 사실 검증이 필요할 때

#### 2.3 맥락 요약 제시

```markdown
## 수집된 맥락
| 항목 | 내용 |
|------|------|
| 관련 파일 | N개 식별 |
| 핵심 패턴 | ... |
| 확인된 제약 | ... |
| 외부 참고 | ... (수행 시) |
```

**Decision Gate 2→3**:

```text
context_available = 최소 1개 이상의 유효 근거 확보

IF context_available -> Step 3 진행
ELSE -> "근거 부족"을 명시하고 Step 3에서 탐색 가정 기반 토론으로 진행
```

### Step 3: Iterative Discussion (반복 토론)

**Tools**: `request_user_input` (Plan mode), `Read`, `Glob`, `rg`, `Bash` (read-only), 선택적 `search_query`, `open`

토론 루프를 실행하며 논점을 수렴한다.

```text
내부 상태:
  key_points = []
  decisions = []
  open_questions = []
  action_items = []
  round = 0
  MAX_ROUNDS = 10

WHILE round < MAX_ROUNDS:
  round += 1

  1) 현재 맥락 기준으로 probing question 생성
  2) request_user_input으로 질문 제시 (옵션 2~3개)
  3) 응답 반영: key_points/decisions/open_questions/action_items 업데이트
  4) 근거 부족 시 Step 2 방식으로 추가 탐색 또는 선택적 웹 리서치

  IF 사용자가 "토론 종료 / 정리"를 선택:
    -> Step 4 진행

IF round == MAX_ROUNDS:
  -> 자동으로 Step 4 진행
```

#### 질문 설계 가이드

- 초반(1-3): 목표/범위/제약 확인
- 중반(4-6): 대안/트레이드오프 비교
- 후반(7+): 결정 확정/남은 리스크 점검

라운드 질문 예시:

```text
질문: "다음 단계에서 우선 검증할 관점을 선택해 주세요."
옵션:
1. "리스크 우선 (실패 가능성 높은 가정 검증)"
2. "가치 우선 (사용자 임팩트 큰 방향 먼저)"
3. "토론 종료 / 정리"
```

### Step 4: Discussion Summary (토론 정리)

**Tools**: 없음 (텍스트 출력)

토론 종료 시 아래 형식으로 요약을 출력한다.

```markdown
# 토론 요약: [토픽]

**날짜**: YYYY-MM-DD
**라운드 수**: N
**참여 방식**: Structured Discussion (Codex Plan mode)

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
- 로컬 코드 근거: [핵심 발견]
- 외부 리서치: [핵심 발견] (수행 시)

## 토론 흐름 (Discussion Flow)
Round 1: [주제] -> [결론/방향]
Round 2: [주제] -> [결론/방향]
...
```

### Step 5: Save Handoff (선택)

**Tools**: `request_user_input` (Plan mode)

Step 4 요약 출력 직후 저장 여부를 확인한다.

```text
질문: "토론 요약을 파일로 저장할까요?"
옵션:
1. "저장하지 않음"
2. "기본 경로로 저장 준비"
3. "경로 지정 후 저장 준비"
```

- 옵션 1: 저장 없이 종료.
- 옵션 2: 기본 경로를 `"_sdd/discussion/DISCUSSION_<topic_slug>_<YYYYMMDD>.md"`로 설정하고 저장 핸드오프를 출력.
- 옵션 3: 추가 질문으로 경로를 확정한 뒤 저장 핸드오프를 출력.
  - 기본 질문 옵션 예시:
    1. `"_sdd/discussion/" 사용`
    2. `"_sdd/" 루트에 저장`
    3. `다른 경로 지정` (자유 입력)

저장 핸드오프 출력 형식:

```markdown
## Save Handoff (Plan mode -> Default mode)
- target_path: [확정 경로]
- overwrite_policy: [create|backup-and-replace]
- content_source: "Step 4 토론 요약 전체"

다음 단계:
1. Plan mode를 종료한다.
2. 아래 요청을 그대로 실행한다.

"방금 discussion 요약을 [target_path]에 저장해 줘. 파일이 있으면 prev 백업 후 덮어써."
```

## Progressive Disclosure (완료 시)

1. 완료 요약 테이블을 먼저 제시한다.
2. Plan mode에서는 `request_user_input`으로 후속 표시 범위를 선택한다.
   - "전체 요약 보기"
   - "결정 사항만 보기"
   - "실행 항목만 보기"
   - "저장 준비 (Plan mode 종료 후)"

## Context Management

### 토론 상태 크기 관리

| 라운드 수 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 5 | 전체 추적 | 모든 논점/결정/미결/액션 항목 유지 |
| 5-8 | 요약 추적 | 핵심 논점 중심으로 압축 |
| > 8 | 압축 추적 | 중간 요약 후 이전 상세를 압축 |

### 리서치 결과 관리

- 리서치 결과는 핵심 발견만 토론 상태에 반영한다.
- 동일 주제 재탐색을 피하기 위해 탐색 로그를 유지한다.
- 웹 리서치 사용 시 출처를 명시한다.

## Error Handling

| 상황 | 대응 |
|------|------|
| Default mode에서 호출됨 | 안내 문구 1회 출력 후 즉시 종료 (추가 동작 금지) |
| 사용자가 토픽을 정하지 못함 | 카테고리 질문으로 최대 2라운드 보완 |
| 로컬 맥락 수집 실패 | 근거 부족 명시 후 가정 기반 토론 진행 |
| 웹 리서치 실패 | 실패 사실 명시, 로컬 근거 중심으로 진행 |
| 사용자 응답 중단 | 현재까지 내용으로 부분 요약 생성 |
| 토론이 범위를 벗어남 | 범위 재확인 질문으로 복귀 |
| MAX_ROUNDS 도달 | 자동으로 Step 4 요약 출력 |
| 저장 요청됨(Plan mode) | Step 5 저장 핸드오프 출력 후 Plan mode 종료 안내 |

## Integration with Other Skills

토론 결과는 후속 스킬 입력으로 활용할 수 있다.

- `spec-create`: 토론에서 정리된 요구사항으로 초기 스펙 생성
- `feature-draft`: 합의된 방향으로 스펙 패치 초안 + 구현 계획 작성
- `implementation-plan`: 결정된 아키텍처를 phase 계획으로 상세화

## Additional Resources

### Reference Files

- `references/discussion-question-guide.md` - 질문 설계 템플릿 및 라운드 전략

### Example Files

- `examples/sample-discussion-session.md` - Plan mode 전용 토론 세션 예시
