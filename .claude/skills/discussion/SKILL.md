---
name: discussion
description: This skill should be used when the user asks to "discuss", "discussion", "토론", "토론하자", "let's discuss", "brainstorm", "논의", "의견 나누기", or wants a structured iterative discussion with research support.
version: 1.0.0
---

# Structured Discussion - 구조화된 토론 진행

| Workflow | Position | When |
|----------|----------|------|
| Any | Standalone | 기술적 주제에 대한 구조화된 토론 |
| Any | Pre-feature-draft | 방향/요구사항 불명확 시 논의 후 feature-draft 연계 |

구조화된 반복 토론을 진행한다. 프로빙 질문으로 주제를 심층 탐구하고, sub-agent를 활용해 코드베이스 탐색 및 웹 리서치를 수행하며, 토론 종료 시 구조화된 요약을 텍스트로 출력한다. **마지막 Step 4에서 토론 요약 파일만 생성할 수 있으며, 그 외 단계에서는 파일 생성/수정을 하지 않는다.**

## Acceptance Criteria
> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.
- [ ] AC1: 구조화된 토론이 최소 1라운드 이상 진행되었다
- [ ] AC2: key decisions / action items가 내부 상태에 추적·정리되었다
- [ ] AC3: 토론 요약 파일이 `_sdd/discussion/discussion_<title>.md`에 저장되었다
- [ ] AC4: 요약에 핵심 논점, 결정 사항, 미결 질문, 실행 항목 섹션이 모두 포함되었다

## Hard Rules

1. **코드 수정 금지**: `Edit`, `Bash`(mutation 명령) 사용을 금지한다. 읽기 전용 도구만 사용한다.
2. **파일 생성은 Step 4에서만 허용**: Step 1-3에서는 파일을 생성하지 않는다. Step 4 (토론 정리)에서만 `Write`로 요약 파일을 저장할 수 있다. `mkdir -p _sdd/discussion/` 디렉토리 생성은 허용한다.
3. **읽기 전용 도구만 허용 (Step 1-3)**: `Read`, `Glob`, `Grep`, `AskUserQuestion`, `Agent`(sub-agent)만 사용 가능하다. Step 4에서는 `Write` 추가 허용.
4. **언어 규칙**: 사용자가 토론을 시작한 언어를 따른다. 토론 중 사용자가 언어를 전환하면 따라간다.
5. **토론 종료 옵션 항상 포함**: Step 3의 매 질문에 "토론 종료 / 정리해줘" 옵션을 반드시 포함한다.
6. **AskUserQuestion 도구 필수**: Step 3 토론 루프에서 사용자에게 질문할 때 반드시 `AskUserQuestion` 도구를 사용한다.

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
   4. "Other (직접 입력)"
   ```

3. 선택된 토픽에 대해 구체적인 범위를 확인 (자유 형식 응답 수용)

**Decision Gate 1→2**: `topic_defined AND scope_clear` → Step 2 진행. ELSE → AskUserQuestion으로 보완 (최대 2라운드).

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

#### 2.2 맥락 요약

수집된 정보를 사용자에게 간략히 보고:
```
## 수집된 맥락
| 항목 | 내용 |
|------|------|
| 관련 파일 | N개 식별 |
| 주요 패턴 | ... |
| 외부 참고 | ... (있는 경우) |
```

**Decision Gate 2→3**: `context_available AND topic_still_valid` → Step 3 진행. 맥락 없으면 사용자에게 확인. 토픽 무효화 시 Step 1 복귀.

### Step 3: Iterative Discussion (반복 토론)

**Tools**: `AskUserQuestion`, `Agent` (Explore, general-purpose), `Read`, `Glob`, `Grep`

핵심 토론 루프. 사용자와 반복적으로 심층 질문-답변을 수행한다.

#### 3.1 토론 루프 구조

```
내부 상태 추적:
  key_points, decisions, open_questions, action_items, conversation_log
  round = 0, MAX_ROUNDS = 10

WHILE round < MAX_ROUNDS:
  round += 1
  1. 현재 맥락 기반으로 probing question 생성
  2. AskUserQuestion으로 질문 제시 (옵션 3개 + "토론 종료")
  3. 사용자 응답 분석 → 내부 상태 업데이트
  4. 필요 시 mid-discussion sub-agent 리서치 수행

  IF 사용자가 "토론 종료" 선택 OR "정리해줘" 입력 → Step 4
```

#### 3.2 질문 생성 전략

초반(1-3) 범위·목표 확인 → 중반(4-6) 트레이드오프·대안 탐색 → 후반(7+) 합의·결정 확인. 옵션은 상호 배타적이고 포괄적으로 구성하며, 이미 답한 내용은 재질문하지 않는다.

#### 3.3 Mid-Discussion Research

토론 중 근거가 필요하면 sub-agent를 즉시 디스패치:

| 트리거 | Sub-agent |
|--------|-----------|
| "추가 리서치 필요" 선택 | general-purpose |
| 코드베이스 확인 필요 | Explore |
| 사실 확인 필요한 주장 | general-purpose |

독립적인 리서치 2건 이상이면 병렬 디스패치.

#### 3.4 중간 상태 추적

매 3라운드마다 (또는 사용자 요청 시) 핵심 논점·결정 사항·미결 질문·실행 항목 카운트를 중간 요약 테이블로 제시.

### Step 4: Discussion Summary (토론 정리)

**Tools**: `Write`

토론 종료 시 구조화된 요약을 생성하고, `_sdd/discussion/discussion_<title>.md`로 자동 저장한다.

- **파일명**: 소문자, 특수문자는 `_`로 대체, 최대 50자, 항상 영문 (예: "인증 시스템 설계" → `discussion_auth_system_design.md`)
- **언어**: 토론에서 사용된 언어로 작성

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

완료 시 요약 테이블을 제시한 후 전체 요약을 출력하고 파일로 저장한다 (사용자 확인을 기다리지 않는다).

## Error Handling

| 상황 | 대응 |
|------|------|
| 사용자가 토픽을 정하지 못함 | 카테고리별 예시 제시, 최대 2라운드 질문 후 자유 주제로 진행 |
| Sub-agent 실패 | 실패 사실 보고, 토론은 수집된 맥락으로 계속 진행 |
| 사용자 응답 없음/중단 | 현재까지의 토론 내용으로 부분 요약 생성 |
| 토론이 범위를 벗어남 | 원래 토픽 리마인드, 범위 재조정 질문 |
| MAX_ROUNDS 도달 | 자동으로 Step 4 진행, 안내 메시지 출력 |
| 코드베이스 접근 불가 | Explore agent 스킵, 외부 리서치만으로 진행 |

## Integration with Other Skills

토론 결과를 후속 스킬(spec-create, feature-draft, implementation-plan)에 활용하려면 사용자가 요약 파일을 참조하여 별도 실행한다.

## Additional Resources

- **`references/discussion-question-guide.md`** - 토론 질문 템플릿 및 전략 가이드
- **`examples/sample-discussion-session.md`** - 구조화된 토론 세션 예시

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

