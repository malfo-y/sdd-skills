---
name: sdd-autopilot
description: "적응형 오케스트레이터 메타스킬. /sdd-autopilot으로 호출하여 요구사항 분석부터 스펙 동기화까지 end-to-end SDD 파이프라인을 자율 실행한다."
version: 2.0.0
---

# SDD Autopilot -- 적응형 오케스트레이터 메타스킬

## Workflow Position

| Workflow | Position | When |
|----------|----------|------|
| SDD Full Pipeline | Orchestrator (최상위) | end-to-end 자율 구현이 필요할 때 |
| Standalone | 독립 실행 | 사용자가 `/sdd-autopilot`으로 직접 호출할 때 |

```
User Request
    |
    v
[sdd-autopilot] -----> Phase 1 (Interactive)
    |                 ├── Reference Loading
    |                 ├── Task Analysis + Inline Discussion
    |                 ├── Explore agent (코드베이스 탐색)
    |                 ├── Reasoning → Orchestrator Generation
    |                 └── Orchestrator Verification
    |
    v
[sdd-autopilot] -----> Phase 1.5 (Checkpoint)
    |                 └── 검증 결과 + 파이프라인 요약 → 사용자 확인
    |
    v
[sdd-autopilot] -----> Phase 2 (Autonomous Execution)
                      ├── 파이프라인 단계 순차 실행
                      ├── review-fix loop
                      ├── 테스트 (인라인 or ralph)
                      └── 최종 요약 + 보고
```

**입력**: 사용자의 기능 요청 (자연어)
**출력**: 구현 완료된 코드 + 동기화된 스펙 + 파이프라인 로그 + 최종 정리 보고서 (`_sdd/pipeline/`)

## When to Use

**사용하는 경우:**
- 기능 구현을 처음부터 끝까지 자동화하고 싶을 때
- "이 기능 구현해줘"처럼 범위가 넓은 구현 요청
- discussion부터 spec sync까지 전체 SDD 파이프라인을 한 번에 실행하고 싶을 때
- 여러 에이전트를 순차적으로 호출해야 하는 복잡한 작업

**사용하지 않는 경우:**
- 단일 스킬로 완료 가능한 작업 (e.g., 스펙 리뷰만, 구현 계획만)
- 이미 구현 계획이 있고 구현만 실행하면 되는 경우 → `/implementation` 직접 호출
- 토론만 필요한 경우 → `/discussion` 직접 호출
- 스펙 문서만 업데이트하는 경우 → `/spec-update-done` 또는 `/spec-update-todo` 직접 호출

**트리거 키워드**: "sdd-autopilot", "autopilot", "자동 구현", "end-to-end 구현", "전체 파이프라인", "자동으로 구현해줘", "처음부터 끝까지"

## Hard Rules

1. **Discussion은 인라인으로 실행**: Step 2의 사용자 대화는 서브에이전트로 위임하지 않고, autopilot 스킬 내에서 `AskUserQuestion`으로 직접 수행한다.
2. **`_sdd/spec/` 직접 수정 금지**: 스펙 파일은 반드시 `spec-update-done` 또는 `spec-update-todo` 에이전트에 위임하여 수정한다.
3. **Phase 2에서 사용자 중단 없이 실행**: Phase 2(자율 실행) 진입 후에는 `AskUserQuestion`을 호출하지 않는다. 마일스톤 텍스트 출력만 수행한다.
4. **오케스트레이터는 `.claude/skills/`에 저장**: 생성된 오케스트레이터 파일은 `.claude/skills/orchestrator_<topic>/SKILL.md`에 저장한다. 스킬로서 재사용 가능하며, 재개(resume) 시 파이프라인 정의로 활용된다.
5. **공유 로그 파일 필수**: 파이프라인 실행 시 `_sdd/pipeline/log_<topic>_<timestamp>.md`를 생성하고, 각 에이전트 완료 후 핵심 결정사항을 추출하여 기록한다. 에이전트는 로그 파일의 존재를 모른다.
6. **한국어 기본, 사용자 언어 따름**: 사용자가 영어로 요청하면 영어로, 한국어로 요청하면 한국어로 진행한다.
7. **파일 기반 상태 전달**: 각 에이전트에는 파일 경로만 전달한다. 에이전트의 전체 출력을 부모 컨텍스트에 누적하지 않는다. 에이전트 결과에서 핵심 정보(출력 파일 경로, 주요 결정사항)만 추출한다.
8. **에이전트 호출 시 원문 전달**: 에이전트에 프롬프트를 전달할 때 사용자의 원래 요청과 관련 컨텍스트 파일 경로를 포함한다. 요약하지 않는다.
9. **Review-Fix 사이클 필수**: 파이프라인에 review 단계(implementation-review 또는 모든 형태의 코드 리뷰)가 포함되면, 반드시 review → fix → re-review 사이클을 실행해야 한다. 리뷰만 하고 끝나는 것은 허용하지 않는다. 이 규칙은 전체 파이프라인, 부분 파이프라인, 중간부터 시작하는 파이프라인, 재개(resume) 모두에 적용된다. review가 포함된 파이프라인에서 `implementation-review`는 핵심 단계로 취급하며, 실패 시 건너뛸 수 없다.
10. **Execute → Verify 필수**: 모든 파이프라인 단계는 반드시 (1) 실행(Execute)과 (2) 검증(Verify) 두 페이즈를 거쳐야 한다. 에이전트를 호출한 것만으로 완료로 간주하지 않는다. 검증 페이즈에서 Exit Criteria를 만족하는지 확인하고, 만족하지 않으면 다음 단계로 넘어가지 않는다. 이 규칙은 생성 에이전트(ralph-loop-init 등)에도 동일하게 적용된다 — 설정을 생성한 후 실제로 실행하여 결과를 확인해야 한다.

## Process

### Step 0: Pipeline State Detection (파이프라인 상태 감지)

**Tools**: `Glob`, `Read`

autopilot이 호출되면 가장 먼저 기존 파이프라인 상태를 확인한다.

#### 0.1 로그 스캔

```
Glob: _sdd/pipeline/log_*.md
```

발견된 로그 파일들의 Status 테이블을 읽어 미완료 스텝(`pending`, `in_progress`, `failed`)이 있는 로그를 필터링한다.

#### 0.2 기존 산출물 스캔

```
Glob: _sdd/drafts/feature_draft_*.md
Glob: _sdd/implementation/IMPLEMENTATION_PLAN.md
```

로그 없이도 기존 산출물이 존재하면, 사용자 요청과의 관련성을 판단하여 활용 여부를 결정한다.

#### 0.3 상태별 분기

```
IF 미완료 로그 == 0 AND 관련 산출물 없음:
  → Step 1로 진행 (새 파이프라인)

IF 미완료 로그 == 1:
  → 사용자에게 제시:
    "이전 파이프라인이 있습니다: <로그의 request 요약>
     마지막 완료 스텝: <agent-name>
     1. 이어서 진행
     2. 새로 시작"
  → 사용자가 재개 선택 시: 오케스트레이터 읽기 → 마지막 completed 다음 스텝부터 Step 7로 진행
  → 사용자가 새로 시작 선택 시: Step 1로 진행

IF 미완료 로그 > 1:
  → 미완료 로그 목록 제시 + "새로 시작" 옵션
  → 사용자가 선택한 로그로 재개 또는 새로 시작

IF 미완료 로그 == 0 AND 관련 산출물 있음:
  → Step 1에서 산출물 활용 여부를 자연어 파싱으로 판단
```

**Decision Gate 0 -> 1 (or 7)**:
```
resume_selected = 사용자가 기존 파이프라인 재개를 선택함

IF resume_selected → Step 7 진행 (재개 모드)
ELSE → Step 1 진행 (새 파이프라인)
```

### Step 1: Reference Loading (레퍼런스 로딩)

**Tools**: `Read`

파이프라인 구성의 기반이 되는 SDD 철학과 스킬 카탈로그를 로딩한다.

#### 1.1 레퍼런스 읽기

```
Read: references/sdd-reasoning-reference.md  (철학 + 스킬 카탈로그)
Read: examples/sample-orchestrator.md        (오케스트레이터 품질 기준)
```

#### 1.2 내재화할 핵심

읽은 레퍼런스에서 다음을 내재화한다:

- **SDD 원칙 3개**: spec-as-SoT, 결정 고정, 검증 기준
- **스킬 의존성 그래프**: 어떤 스킬이 어떤 출력을 만드는지 (input/output/pre-condition)
- **파이프라인 구성 가이드라인**: 소/중/대 + 특수 상황 (부분 파이프라인, 팬아웃 병렬, 재개 등)
- **테스트 전략 판단 기준**: 인라인 디버깅 vs ralph-loop-init 결정 근거

**Decision Gate 1 → 2**:
```
reference_loaded = sdd-reasoning-reference.md 읽기 성공

IF reference_loaded → Step 2
ELSE → 에러 (reference 파일 누락)
```

### Step 2: Task Analysis + Discussion (요청 분석 + 인라인 토론)

**Tools**: `AskUserQuestion`

> **중요**: 이 단계는 서브에이전트가 아닌 autopilot 스킬 내에서 인라인으로 실행한다. Discussion 에이전트를 호출하지 않는다.

기존의 요청 분석과 인라인 토론을 하나의 스텝으로 통합하여 수행한다.

#### 2.1 요청 파싱

사용자 입력에서 다음을 추출한다:

- 기능 설명 (무엇을 만들려는가)
- 기술적 키워드 (프레임워크, 라이브러리, 패턴 등)
- 명시된 제약 조건 (있는 경우)
- 기존 코드와의 관계 (신규 vs 수정 vs 확장)
- 시작점/종료점 감지: 사용자 요청에서 시작/종료 힌트를 추출한다 ("구현부터", "리뷰까지만" 등)
- 기존 산출물 스캔:
  - `_sdd/drafts/feature_draft_*.md` → feature-draft 완료 여부
  - `_sdd/implementation/IMPLEMENTATION_PLAN.md` → implementation-plan 완료 여부
  - 관련성 높음 → 해당 산출물을 활용하여 이후 스텝부터 파이프라인 구성
  - 관련성 불확실 → 2.2에서 사용자에게 "기존 산출물을 활용할까요?" 확인
  - 관련성 없음 → 무시하고 처음부터 시작
- **Review-Fix 사이클 필수 검증**: 파이프라인 범위에 review 단계가 포함되면, 반드시 implementation + review-fix loop이 함께 포함되어야 한다. "리뷰만" 요청하더라도 review → fix → re-review 사이클을 강제한다.

#### 2.2 인라인 토론

사용자와 대화하여 요구사항을 구체화한다. 요청 명확도에 따라 질문 횟수를 적응적으로 조절한다 (1-5회).

**AskUserQuestion 형식**:
```
AskUserQuestion: "[구체적인 질문]"
옵션:
1. "[선택지 A]"
2. "[선택지 B]"
3. "[선택지 C]"
4. "충분합니다 — 진행해주세요"
```

매 질문에 "충분합니다 -- 진행해주세요" 옵션을 반드시 포함한다. 사용자가 이를 선택하면 즉시 Step 3으로 진행한다.

**수집 대상 정보**:
- 기능 범위: 정확히 어디까지 구현할 것인가
- 기술 제약: 특정 기술 스택, 라이브러리, 패턴 요구사항
- 우선순위: MVP vs 완성도 높은 구현
- 테스트 요구사항: 테스트 범위, 필수 테스트 시나리오
- 스펙 변경 여부: 기존 스펙에 추가/수정이 필요한지

#### 2.3 내부 상태 기록

Discussion 중 다음을 내부적으로 추적한다 (파일로 저장하지 않음):

```
requirements = []       # 확정된 요구사항
constraints = []        # 제약 조건
technical_decisions = [] # 기술적 결정
test_requirements = []   # 테스트 요구사항
```

**Decision Gate 2 → 3**:
```
requirements_clear = 핵심 요구사항이 1개 이상 확정됨
user_ready = 사용자가 "충분합니다" 선택 OR 최대 질문 횟수 도달

IF requirements_clear AND user_ready → Step 3 진행
ELSE IF 최대 질문 횟수 도달 → 현재까지 수집된 정보로 Step 3 진행
ELSE → 추가 질문
```

### Step 3: Codebase Exploration (코드베이스 탐색)

**Tools**: `Agent` (Explore), `Read`, `Glob`, `Grep`

코드베이스 구조와 관련 파일을 분석하여 규모 판단의 근거를 수집한다.

#### 3.1 Explore 에이전트 호출

```
Agent(
  subagent_type="Explore",
  prompt="다음 기능 구현을 위해 코드베이스를 분석하세요: [기능 설명]

  수집 대상:
  1. 프로젝트 전체 구조 (디렉토리 트리)
  2. 관련 파일/모듈 목록 및 역할
  3. 기존 패턴 및 컨벤션 (코딩 스타일, 아키텍처 패턴)
  4. 의존성 관계 (import/require 체인)
  5. 기존 테스트 구조 (테스트 프레임워크, 패턴)
  6. _sdd/spec/ 문서 현황 (관련 스펙 섹션 식별)

  결과를 구조화된 형태로 보고하세요."
)
```

#### 3.2 직접 탐색 (보조)

Explore 에이전트 결과가 부족한 경우 직접 보완한다:

- `Glob`: 관련 파일 패턴 검색 (e.g., `**/*.py`, `**/*.ts`)
- `Grep`: 키워드 기반 관련 코드 검색
- `Read`: 핵심 파일 내용 확인 (스펙 문서, 설정 파일)

#### 3.3 분석 결과 정리

```
codebase_analysis = {
  project_structure: "디렉토리 구조 요약",
  related_files: ["경로1", "경로2", ...],   # 수정/생성 대상 파일
  existing_patterns: "기존 패턴 요약",
  test_structure: "테스트 구조 요약",
  spec_status: "관련 스펙 섹션 존재 여부",
  estimated_file_count: N,                    # 영향받는 파일 수
  new_components: N,                          # 신규 생성 컴포넌트 수
  spec_change_needed: true/false              # 스펙 변경 필요 여부
}
```

**Decision Gate 3 → 4**:
```
analysis_complete = 프로젝트 구조와 관련 파일이 식별됨

IF analysis_complete → Step 4 진행
IF Explore agent 실패 → 직접 탐색으로 보완 후 Step 4 진행
```

### Step 4: Reasoning → Orchestrator Generation (추론 → 오케스트레이터 생성)

**Tools**: `Write`

> **이전**: 규모 판단(정량+정성 기준) → 소/중/대 분류 → 템플릿 매칭
> **이후**: reference 기반 reasoning → 동적 파이프라인 구성

#### 4.1 Reasoning (내부, reference 기반)

Step 1에서 내재화한 SDD 철학 + 스킬 카탈로그를 바탕으로 다음을 추론한다:

a) **스펙 상태 판단**: 스펙 존재? → 없으면 오케스트레이터 생성 중단, 사용자에게 `/spec-create` 실행 안내
b) **변경 범위 판단**: 스펙 패치? 신규 섹션? → spec-update-todo 필요 여부
c) **계획 깊이**: 직접 구현? feature-draft? impl-plan까지?
d) **검증 수준**: 인라인 테스트? ralph-loop? review 포함?
e) **스킬 의존성 순서**: 카탈로그의 input/output/pre-condition으로 결정
f) **특수 패턴**: 부분 파이프라인, 팬아웃 병렬, 재개 등

#### 4.2 파이프라인 구성

- 의존성 그래프 기반 동적 조합 (가이드라인 참조, 템플릿 아님)
- 비표준 조합 가능 (reference의 가이드라인 범위 내에서)

#### 4.3 오케스트레이터 SKILL.md 생성

- 오케스트레이터 형식은 `references/orchestrator-contract.md`의 계약을 따른다.
- `Reasoning Trace`는 3-6개 bullet로 간결하게 작성한다.

파일 경로:
```
.claude/skills/orchestrator_<topic>/SKILL.md
```

- `<topic>`: 기능명을 영문 snake_case로 변환 (e.g., "인증 시스템" → `auth_system`)

생성 절차:
1. `.claude/skills/orchestrator_<topic>/` 디렉토리 생성 (없으면 `mkdir -p`)
2. Step 1에서 로딩한 `references/sdd-reasoning-reference.md`의 스킬 카탈로그를 참조하여 파이프라인 구성
3. `examples/sample-orchestrator.md`를 품질 기준으로 참조
4. `references/orchestrator-contract.md`의 섹션/필드 계약을 충족하도록 생성
5. Step 2-3에서 수집한 정보를 반영하여 오케스트레이터 생성
6. 오케스트레이터 파일을 `Write`로 저장

#### 4.4 Pre-flight Check (리소스 사전 점검)

오케스트레이터 생성 후, 파이프라인 실행에 필요한 리소스를 추정하고 `_sdd/env.md`와 대조하여 갭을 분석한다.

**1단계: env.md 읽기**
```
Read: _sdd/env.md
→ 이미 확보된 리소스 추출:
  - 런타임 환경 (Python, Node, conda env 등)
  - 환경 변수 (API 키, DB URL 등)
  - 테스트 프레임워크 및 실행 명령
  - 외부 서비스 (DB, Redis, 메시지 큐 등)
```

**2단계: 필요 리소스 추정**

오케스트레이터의 각 에이전트 단계를 분석하여 필요한 리소스를 추정한다:

| 에이전트 | 필요 리소스 유형 |
|---------|----------------|
| implementation | 런타임, 패키지 매니저, 테스트 프레임워크, 외부 서비스, 환경 변수 |
| implementation (테스트) | 테스트 DB, mock 서비스, 테스트 데이터 |
| ralph-loop-init | GPU (ML), 학습 데이터, 장시간 실행 환경 |
| spec-update-done | git (diff 확인용) |
| feature-draft, impl-plan, impl-review | 추가 리소스 불필요 (읽기 위주) |

추정 방법:
- Step 2 (Discussion)에서 수집한 기술 키워드 분석 (e.g., "Redis 캐시" → Redis 서버 필요)
- Step 3 (Codebase Exploration)에서 발견한 의존성 분석 (e.g., `import redis` → Redis 필요)
- 오케스트레이터의 프롬프트에 언급된 기술 스택 분석

**3단계: 갭 분석**
```
for resource in required_resources:
  if resource in env_md_resources:
    status = "확인됨 (env.md)"
  else:
    status = "미확인"

→ Pre-flight Check 테이블 생성
```

Pre-flight Check 결과는 Step 6 (User Checkpoint)에서 파이프라인 요약과 함께 사용자에게 제시한다.

**Decision Gate 4 → 5**:
```
orchestrator_created = 오케스트레이터 파일이 .claude/skills/orchestrator_<topic>/에 저장됨

IF orchestrator_created → Step 5 진행
```

### Step 5: Orchestrator Verification (오케스트레이터 검증)

**Tools**: `Read`

생성된 오케스트레이터의 구조적 정합성과 SDD 철학 준수 여부를 검증한다. Producer-Reviewer 패턴을 적용한다.

#### 5.1 구조 검증 (6항목)

a) 모든 step이 유효한 에이전트명을 참조 (8개 에이전트 목록 대조)
b) 각 step에 에이전트명/입력 파일/출력 파일/프롬프트가 있음
c) 산출물 handoff 정합성 (step N 출력 = step N+1 입력)
d) Review-fix loop 섹션 존재 (review 포함 시)
e) Test strategy 섹션 존재
f) Error handling 섹션 존재 (핵심/비핵심 분류)

#### 5.2 철학 검증 (6항목 -- reference 재참조)

a) **Spec-first**: 스펙이 없으면 오케스트레이터 생성을 중단하고 `/spec-create` 안내?
b) **드리프트 방지**: 대규모 변경에 spec-update-todo 포함?
c) **Review-fix 완전성**: review가 단독 종료되지 않음?
d) **Execute → Verify**: 핵심 실행 step과 review/test phase에 Exit Criteria가 정의됨?
e) **파일 기반 handoff**: 프롬프트에 파일 경로만, 전체 컨텍스트 없음?
f) **스펙 직접 수정 금지**: spec 변경이 spec-update-todo/done으로만?

#### 5.3 결과 분기

```
IF 12/12 통과:
  → Step 6 진행

IF 구조 이슈:
  → 자동 수정 (Edit, 최대 2회) → 재검증

IF 철학 위반:
  → Step 4.1 재실행 (위반 사항 피드백, 최대 1회)

IF 재시도 후에도 실패:
  → Step 6에서 경고 표시 후 사용자 판단에 위임
```

### Step 6: User Checkpoint (사용자 확인)

**Tools**: `AskUserQuestion`, `Read`, `Edit`

생성된 오케스트레이터를 사용자에게 제시하고, 확인/수정 후 실행 승인을 받는다.

> **이 단계가 Phase 1(Interactive)의 마지막이다.** 승인 후 Phase 2(Autonomous)로 진입하면 사용자 중단 없이 완료까지 진행한다.

#### 6.1 파이프라인 요약 + 검증 결과 + Pre-flight Check 제시

```
## 파이프라인 요약

| 항목 | 내용 |
|------|------|
| 기능 | [기능 설명] |
| 파이프라인 | [agent1] → [agent2] → ... |
| 검증 결과 | 통과 (12/12) 또는 N건 경고 |
| 예상 에이전트 수 | N개 |
| Review 최대 횟수 | 3회 |
| 테스트 전략 | [인라인 디버깅 / ralph-loop-init] |
| 오케스트레이터 경로 | .claude/skills/orchestrator_xxx/SKILL.md |

## Pre-flight Check

| 리소스 | 상태 | 출처 | 필요 단계 |
|--------|------|------|----------|
| [런타임/환경] | 확인됨/미확인 | env.md / 미확인 | [어떤 에이전트에서 필요] |
| [테스트 프레임워크] | 확인됨/미확인 | env.md / 미확인 | implementation |
| [외부 서비스] | 확인됨/미확인 | env.md / 미확인 | implementation |
| [환경 변수] | 확인됨/미확인 | env.md / 미확인 | implementation |
```

- 확인됨 항목만 있으면 → 바로 실행 가능
- 미확인 항목이 있으면 → 사용자에게 해결 방법을 제시

#### 6.2 사용자 확인

```
AskUserQuestion: "위 파이프라인과 리소스를 확인해 주세요."
옵션:
1. "모두 준비됨 — 실행해주세요"
2. "env.md에 추가할 정보가 있습니다" → 사용자 입력을 받아 env.md Edit 후 재확인
3. "미확인 리소스 없이 진행 (mock 처리)" → 해당 리소스를 mock/skip으로 처리하도록 오케스트레이터 수정
4. "취소합니다"
```

#### 6.3 수정 처리

사용자가 수정을 요청하면:
1. 수정 사항을 파악
2. 오케스트레이터 파일을 `Edit`으로 수정
3. 수정된 요약을 다시 제시
4. 재확인 (최대 3회 반복)

**Decision Gate 6 → 7**:
```
user_approved = 사용자가 "실행해주세요" 선택
user_cancelled = 사용자가 "취소합니다" 선택

IF user_approved → Step 7 진행 (Phase 2 진입)
IF user_cancelled → 종료 (오케스트레이터 파일은 유지)
ELSE → 수정 후 재확인
```

### Step 7: Autonomous Execution (자율 실행)

**Tools**: `Agent`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`

> **Phase 2 진입**: 이 단계부터 `AskUserQuestion`을 호출하지 않는다. 마일스톤 텍스트 출력만 수행한다.

승인된 오케스트레이터를 기반으로 파이프라인을 자율 실행한다.

#### 7.1 파이프라인 초기화

1. **로그 파일 생성**:
   ```
   mkdir -p _sdd/pipeline/
   Write: _sdd/pipeline/log_<topic>_<timestamp>.md
   ```
   로그 파일 초기 내용은 `references/orchestrator-contract.md`의 Pipeline Log Contract를 따른다.

2. **오케스트레이터 읽기**: `Read`로 오케스트레이터 파일을 읽어 파이프라인 단계를 확인한다.

3. **마일스톤 출력**:
   ```
   [sdd-autopilot] 파이프라인 실행을 시작합니다.
   단계: N개 | 시작: <timestamp>
   ```

#### 7.2 파이프라인 실행 루프 (Execute → Verify)

> **Hard Rule #10 적용**: 모든 단계는 Execute(실행)와 Verify(검증) 두 페이즈를 반드시 거친다. 에이전트 호출만으로 완료로 간주하지 않는다.

오케스트레이터에 정의된 순서대로 각 에이전트를 호출한다.

```
FOR EACH step IN pipeline_steps:

  ## Phase A: Execute (실행)
  1. 마일스톤 출력: "[sdd-autopilot] Step N/M: <agent-name> 시작..."
  2. 로그 기록: 시작 시간 기록 (Edit)
  3. 에이전트 호출:
     Agent(
       subagent_type="<agent-name>",
       prompt="<오케스트레이터에 정의된 프롬프트>

       컨텍스트 파일:
       - <이전 에이전트의 출력 파일 경로>
       - <관련 _sdd/ 파일 경로>

       사용자 원래 요청: <사용자 요청 원문>"
     )

  ## Phase B: Verify (검증)
  4. Exit Criteria 검증:
     - 해당 단계의 Exit Criteria(7.2.1 참조)를 하나씩 확인한다
     - 산출물 파일이 존재하는지 Glob/Read로 확인한다
     - 산출물 내용이 비어있거나 형식이 틀리지 않은지 확인한다
     - 실행이 필요한 단계(테스트, ralph loop 등)는 실제 실행 결과를 확인한다

  5. 검증 결과 분기:
     IF 모든 Exit Criteria 만족:
       → 로그에 완료 기록 + 핵심 결정사항 추가 (Edit)
       → 마일스톤: "[sdd-autopilot] Step N/M: <agent-name> 검증 통과 -- <출력 파일 경로>"
       → 다음 단계로 진행
     IF Exit Criteria 미충족:
       → 로그에 미충족 항목 기록
       → 마일스톤: "[sdd-autopilot] Step N/M: <agent-name> 검증 실패 -- <미충족 항목>"
       → Error Handling 절차 실행 (7.5절) -- 재시도 또는 보완 후 Phase B 재실행
```

#### 7.2.1 단계별 Exit Criteria

각 에이전트의 완료 조건이다. **Verify 페이즈에서 이 조건들을 모두 확인해야 다음 단계로 넘어갈 수 있다.**

| 에이전트 | Exit Criteria |
|---------|--------------|
| `feature-draft` | `_sdd/drafts/feature_draft_<topic>.md` 파일 존재 + 요구사항/제약조건 섹션이 비어있지 않음 |
| `implementation-plan` | `_sdd/implementation/IMPLEMENTATION_PLAN.md` 파일 존재 + 태스크가 1개 이상 정의됨 |
| `implementation` | 구현 대상 파일이 생성/수정됨 + 구문 에러 없음 (lint/parse 통과) |
| `implementation-review` | 리뷰 결과에 심각도 분류(critical/high/medium/low)가 포함됨 |
| `ralph-loop-init` | `ralph/` 디렉토리 존재 + `ralph/run.sh` 실행 가능 + `ralph/state.md` 존재 |
| ralph loop 실행 | `ralph/state.md`의 phase가 `DONE` + 최종 테스트 결과가 기록됨 |
| 인라인 테스트 | 테스트 명령 실행 완료 + 전체 테스트 통과 (또는 최대 재시도 후 결과 기록) |
| `spec-update-done` | `_sdd/spec/` 파일이 업데이트됨 + 구현 내용이 스펙에 반영됨 |
| `spec-update-todo` | `_sdd/spec/` 파일이 업데이트됨 + 계획된 기능이 스펙에 추가됨 |
| `spec-review` | 리뷰 결과가 텍스트로 반환됨 + 드리프트/품질 이슈가 분류됨 |

#### 7.3 Review-Fix 루프 (필수 사이클)

> **Hard Rule #9 적용**: 파이프라인에 review가 포함되면, review → fix → re-review 사이클은 필수다. 리뷰만 하고 끝나는 것은 허용하지 않는다. 이 규칙은 전체/부분/재개 파이프라인 모두에 적용된다.

implementation 에이전트 완료 후 implementation-review 에이전트로 리뷰를 수행한다.

**사이클 필수 조건**: 첫 번째 리뷰에서 이슈가 발견되면 반드시 fix 후 re-review를 실행해야 한다. 이슈가 0건일 때만 사이클이 종료된다.

```
review_count = 0
MAX_REVIEW = 3

WHILE review_count < MAX_REVIEW:
  review_count += 1

  1. implementation-review 에이전트 호출:
     Agent(
       subagent_type="implementation-review",
       prompt="구현 결과를 리뷰하세요.

       구현 계획: <_sdd/implementation/ 경로>
       리뷰 대상: <구현된 코드 파일 목록>

       리뷰 결과에 critical/high/medium/low 심각도를 반드시 포함하세요."
     )

  2. 리뷰 결과 분석:
     - critical/high 이슈 수 추출
     - 로그에 리뷰 결과 기록

  3. 종료 조건 확인:
     IF critical_count == 0 AND high_count == 0:
       → 마일스톤: "[sdd-autopilot] 리뷰 통과 (Round N) -- critical/high 이슈 없음"
       → BREAK

     IF review_count == MAX_REVIEW AND (critical_count > 0 OR high_count > 0):
       → 마일스톤: "[sdd-autopilot] 리뷰 루프 종료 (최대 3회 도달) -- critical/high 미해결, 파이프라인 중단"
       → 잔여 이슈를 로그에 기록
       → **파이프라인 중단** (Exit Criteria 미충족 -- Hard Rule #9, #10)
       → BREAK

  4. 수정 실행 (필수 -- 이슈 발견 시 건너뛸 수 없음):
     - critical/high 이슈만 수정 대상 (medium/low는 로그에만 기록)
     - implementation 에이전트 재호출:
       Agent(
         subagent_type="implementation",
         prompt="리뷰에서 발견된 critical/high 이슈를 수정하세요.

         리뷰 리포트: <리뷰 결과 요약>
         수정 대상 이슈:
         - [critical/high 이슈 목록]

         medium/low 이슈는 무시하세요."
       )

  5. 마일스톤: "[sdd-autopilot] Review-Fix Round N/3 완료"
  6. → 루프 상단으로 돌아가 re-review 실행 (이것이 사이클의 핵심)
```

**부분 파이프라인에서의 Review-Fix 사이클**:

사용자가 "리뷰만 해줘", "리뷰부터 시작" 등으로 review만 요청하더라도:
1. 먼저 implementation-review를 실행한다
2. 이슈가 발견되면 → implementation 에이전트로 fix 실행
3. fix 후 → re-review 실행 (사이클 반복)
4. critical/high = 0이면 종료
5. MAX_REVIEW 도달 시에도 critical/high > 0이면 → **파이프라인 중단**

리뷰 결과 이슈 0건인 경우에만 단일 리뷰로 종료가 가능하다.

#### 7.4 테스트 실행 (Execute → Verify)

리뷰 완료 후 테스트를 실행한다. 오케스트레이터에 정의된 테스트 전략에 따라 분기한다.

> **Hard Rule #10 적용**: 테스트 단계도 Execute → Verify를 반드시 거친다. 설정만 생성하고 실행하지 않는 것은 허용하지 않는다.

**인라인 디버깅** (대부분의 경우):

```
## Phase A: Execute
implementation 에이전트에 테스트 실행을 포함하여 호출:
Agent(
  subagent_type="implementation",
  prompt="구현된 코드의 테스트를 실행하고, 실패하는 테스트가 있으면 수정하세요.

  테스트 실행 명령: <프로젝트의 테스트 명령>
  수정 대상 코드: <구현된 파일 목록>

  테스트 통과까지 수정-재실행 루프를 반복하세요 (최대 5회)."
)

## Phase B: Verify
Exit Criteria 확인:
  - 테스트 명령이 실제로 실행되었는가 (에이전트 결과에서 실행 로그 확인)
  - 테스트 결과가 보고되었는가 (통과/실패 건수)
  - 실패 테스트가 있다면 수정이 시도되었는가

IF 테스트 전체 통과 → 다음 단계 진행
IF 최대 재시도 후에도 실패 → 실패한 테스트 목록을 로그에 기록 → **파이프라인 중단** (Exit Criteria 미충족 -- Hard Rule #10)
IF 테스트가 실행조차 되지 않음 → Error Handling (7.5절) → 재시도 실패 시 **파이프라인 중단**
```

**ralph-loop-init** (장시간 테스트):

> **주의**: ralph-loop-init은 설정 생성(Phase A-1)과 실제 실행+결과 확인(Phase A-2, Phase B)이 모두 완료되어야 한다. 설정만 만들고 넘어가는 것은 **Hard Rule #10 위반**이다.

```
## Phase A-1: Execute (설정 생성)
ralph-loop-init 에이전트로 설정 생성:
Agent(
  subagent_type="ralph-loop-init",
  prompt="다음 기능의 자동 디버깅 루프를 설정하세요.

  기능 설명: <기능 설명>
  테스트 명령: <테스트 실행 명령>
  관련 파일: <구현된 파일 목록>"
)

## Phase B-1: Verify (설정 검증)
Exit Criteria 확인:
  - ralph/ 디렉토리가 존재하는가
  - ralph/run.sh 파일이 존재하고 실행 가능한가
  - ralph/state.md 파일이 존재하는가

IF 미충족 → Error Handling (7.5절)으로 재시도
IF 충족 → Phase A-2로 진행

## Phase A-2: Execute (실제 실행)
ralph loop를 background로 실행:
Bash(
  command="bash ralph/run.sh 2>&1",
  run_in_background=true
)
→ 마일스톤: "[sdd-autopilot] ralph loop 실행 중 (background)..."
→ background 작업 완료 알림을 기다린다 (polling/sleep 하지 않음)

## Phase B-2: Verify (실행 결과 검증)
완료 알림 수신 후 Exit Criteria 확인:
  - ralph/state.md의 phase 값 확인
  - 최종 테스트 결과가 기록되어 있는가
  - 디버깅 루프가 실제로 실행되었는가 (iteration 횟수 > 0)

IF phase == DONE AND 테스트 결과 기록됨:
  → 마일스톤: "[sdd-autopilot] ralph loop 완료 -- 결과: <요약>"
  → 다음 단계(spec-update-done) 진행
IF phase != DONE:
  → 로그에 실패 상세 기록 (phase 값, 마지막 에러, iteration 횟수)
  → 마일스톤: "[sdd-autopilot] ralph loop 미완료 -- phase: <값>, 파이프라인 중단"
  → **파이프라인 중단** (Exit Criteria 미충족 -- Hard Rule #10)
```

#### 7.5 에러 핸들링

에이전트 호출 중 에러가 발생하면 다음 절차를 따른다.

```
retry_count = 0
MAX_RETRY = 3

ON ERROR:
  retry_count += 1
  1. 로그에 에러 상세 기록 (에이전트명, 에러 내용, 타임스탬프)
  2. 마일스톤: "[sdd-autopilot] 에러 발생 -- <agent-name>: <에러 요약> (재시도 N/3)"

  IF retry_count <= MAX_RETRY:
    3. 에러 원인 분석 (에러 메시지, 관련 파일 확인)
    4. 가능하면 원인 수정 (파일 수정, 경로 수정 등)
    5. 에이전트 재호출
  ELSE:
    3. 로그에 실패 기록
    4. IF 현재 단계가 비핵심 단계:
         마일스톤: "[sdd-autopilot] <agent-name> 실패 -- 최대 재시도(3회) 초과. 비핵심 단계이므로 로그에 기록 후 다음 단계로 진행합니다."
    5. IF 현재 단계가 비핵심 단계:
         해당 단계를 건너뛰고 다음 단계로 진행
       ELSE:
         파이프라인 중단
         (핵심 단계 실패 시 중단 기준은 아래 참조)
```

**핵심 단계 실패 시 파이프라인 중단 기준:**
- `feature-draft` 에이전트 실패 → 파이프라인 중단 (계획 없이 구현 불가)
- `implementation-plan` 에이전트 실패 → 파이프라인 중단 (구현 계획 없이 구현 불가)
- `implementation` 에이전트 실패 → 파이프라인 중단 (구현 없이 진행 불가)
- `implementation-review` 에이전트 실패 (파이프라인에 review 포함 시) → 파이프라인 중단 (Hard Rule #9 -- review-fix 사이클 필수)
- 테스트 단계 실패 (인라인/ralph 모두) → 파이프라인 중단 (Hard Rule #10 -- Exit Criteria 미충족)
- `spec-update-done` / `spec-review` 실패 → 건너뛰고 진행 (로그에 기록, 수동 수행 가능)

**파이프라인 중단 시 보고:**

핵심 단계 실패로 파이프라인이 중단되면:

```
## SDD Autopilot 파이프라인 중단

| 항목 | 내용 |
|------|------|
| 중단 원인 | <에이전트명>: <에러 요약> |
| 재시도 횟수 | 3/3 (최대) |
| 완료된 단계 | Step 1-N |
| 미완료 단계 | Step N+1 ~ M |
| 로그 파일 | _sdd/pipeline/log_<topic>_<timestamp>.md |

### 부분 산출물
- <완료된 단계까지의 산출물 목록>

### 권장 후속 조치
- <수동으로 해결할 수 있는 방법>
- <재실행 시 참고사항>
```

#### 7.6 마일스톤 보고

각 에이전트 호출 전후에 텍스트를 출력하여 사용자에게 진행 상황을 알린다.

마일스톤 포맷:
```
[sdd-autopilot] Step N/M: <agent-name> <상태>
  └── <부가 정보 (출력 파일 경로, 소요 시간 등)>
```

예시:
```
[sdd-autopilot] Step 1/6: feature-draft 시작...
[sdd-autopilot] Step 1/6: feature-draft 완료 -- _sdd/drafts/feature_draft_auth_system.md
[sdd-autopilot] Step 2/6: implementation-plan 시작...
[sdd-autopilot] Step 2/6: implementation-plan 완료 -- _sdd/implementation/IMPLEMENTATION_PLAN.md
[sdd-autopilot] Step 3/6: implementation 시작...
[sdd-autopilot] Step 3/6: implementation 완료 -- 15개 파일 생성/수정
[sdd-autopilot] Review-Fix Round 1/3: critical 2건, high 1건 발견 -- 수정 중...
[sdd-autopilot] Review-Fix Round 2/3: critical 0건, high 0건 -- 리뷰 통과
[sdd-autopilot] Step 5/6: 인라인 테스트 시작...
[sdd-autopilot] Step 5/6: 테스트 통과 (12/12)
[sdd-autopilot] Step 6/6: spec-update-done 시작...
[sdd-autopilot] Step 6/6: spec-update-done 완료 -- _sdd/spec/main.md 업데이트
```

#### 7.7 로그 파일 관리

각 에이전트 완료 후 로그 파일을 `Edit`으로 업데이트한다.

로그 엔트리 추가 방식:
```
Edit: _sdd/pipeline/log_<topic>_<timestamp>.md

추가할 내용:
### <agent-name> -- <상태>
- **시간**: <시작> ~ <완료> (<소요 시간>)
- **출력**: <출력 파일 경로>
- **핵심 결정사항**:
  - <에이전트 결과에서 추출한 주요 결정 1>
  - <에이전트 결과에서 추출한 주요 결정 2>
- **이슈**: <있으면 기록, 없으면 "없음">
```

> **핵심 결정사항 추출**: 에이전트 결과 텍스트에서 "결정", "선택", "방향", "전략" 등의 키워드를 포함하는 문장을 추출한다. 추출이 어려우면 에이전트의 주요 행동을 1-3줄로 요약한다.

### Step 8: Final Summary (최종 요약)

**Tools**: `Edit`, `Write`

파이프라인 완료 후 로그 파일을 마무리하고, 최종 정리 보고서를 작성하여 사용자에게 보고한다.

#### 8.1 로그 파일 마무리

로그 파일에 최종 요약 섹션을 추가한다:

```
Edit: _sdd/pipeline/log_<topic>_<timestamp>.md

추가할 내용:
## 최종 요약
- **완료 시간**: <timestamp>
- **총 소요 시간**: <시작~종료>
- **실행 결과**: 성공 / 부분 성공 / 실패
- **생성/수정 파일 수**: N개
- **Review 횟수**: N회
- **테스트 결과**: 통과 N/N
- **스펙 동기화**: 완료 / 미완료
- **잔여 이슈**: <있으면 목록, 없으면 "없음">
```

#### 8.2 최종 정리 보고서 작성

파이프라인 완료(또는 중단/실패) 시 독립된 보고서 파일을 작성한다:

```
Write: _sdd/pipeline/report_<topic>_<timestamp>.md
```

보고서에 반드시 포함할 세 가지:

1. **뭘 했는가 (What was done)**:
   - 실행된 파이프라인 단계와 spawn된 에이전트 목록
   - 생성/수정된 산출물 파일 경로
   - review-fix 사이클 횟수, 테스트 실행 여부

2. **어떻게 나왔는가 (Results)**:
   - 각 단계의 성공/실패 여부와 결과 요약
   - review에서 발견된 이슈와 해결 상태
   - 테스트 통과율, 스펙 동기화 완료 여부

3. **뭘 더 해야 하는가 (Remaining work)**:
   - 미완료 단계 및 사유
   - 알려진 제한사항, 리스크
   - 후속 작업 제안 (수동 확인, 추가 테스트, 배포 등)

> 파이프라인이 실패/중단된 경우에도 반드시 보고서를 작성한다. 현재까지 진행 상황과 실패 원인을 기록한다.

#### 8.3 사용자에게 최종 보고

보고서 파일 작성 후, 핵심 내용을 텍스트로 출력하여 사용자에게 보고한다:

```
## SDD Autopilot 실행 완료

| 항목 | 결과 |
|------|------|
| 기능 | <기능 설명> |
| 파이프라인 | <실행된 에이전트 목록> |
| 생성/수정 파일 | N개 |
| Review 결과 | N회 (critical/high 0건) |
| 테스트 | 통과 N/N |
| 스펙 동기화 | 완료 |
| 로그 파일 | _sdd/pipeline/log_<topic>_<timestamp>.md |
| 정리 보고서 | _sdd/pipeline/report_<topic>_<timestamp>.md |
| 오케스트레이터 | .claude/skills/orchestrator_<topic>/SKILL.md |

### 주요 산출물
- <산출물 1 경로 및 설명>
- <산출물 2 경로 및 설명>

### 잔여 이슈 (있는 경우)
- <이슈 목록>

### 후속 작업 제안 (있는 경우)
- <제안 1>
- <제안 2>
```

## Reference Files

- `references/sdd-reasoning-reference.md`: SDD 철학, skill catalog, 규모별 reasoning 기준
- `references/orchestrator-contract.md`: 오케스트레이터/로그 최소 계약
- `examples/sample-orchestrator.md`: 중규모 기본형 + 대규모 차이점 예시
