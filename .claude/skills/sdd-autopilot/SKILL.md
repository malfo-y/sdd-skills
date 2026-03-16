---
name: sdd-autopilot
description: "적응형 오케스트레이터 메타스킬. /sdd-autopilot으로 호출하여 요구사항 분석부터 스펙 동기화까지 end-to-end SDD 파이프라인을 자율 실행한다."
version: 1.0.0
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
    |                 ├── Inline Discussion (AskUserQuestion)
    |                 ├── Explore agent (코드베이스 탐색)
    |                 └── Scale Assessment
    |
    v
[sdd-autopilot] -----> Phase 1.5 (Checkpoint)
    |                 └── 오케스트레이터 생성 + 사용자 확인
    |
    v
[sdd-autopilot] -----> Phase 2 (Autonomous Execution)
                      ├── feature-draft agent     → _sdd/drafts/
                      ├── implementation-plan agent → _sdd/implementation/
                      ├── implementation agent      → 코드 생성/수정
                      ├── implementation-review agent → 리뷰 리포트
                      │   └── [review-fix loop max 3회]
                      ├── 테스트/디버깅 (인라인 or ralph-loop-init)
                      └── spec-update-done agent   → _sdd/spec/ 동기화
```

**입력**: 사용자의 기능 요청 (자연어)
**출력**: 구현 완료된 코드 + 동기화된 스펙 + 파이프라인 로그 (`_sdd/pipeline/`)

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
4. **오케스트레이터는 `_sdd/pipeline/`에 저장**: 생성된 오케스트레이터 파일은 `.claude/skills/`가 아닌 `_sdd/pipeline/orchestrator_<topic>_<timestamp>.md`에 저장한다. 일회성 실행 계획이므로 스킬 디렉토리를 오염시키지 않는다.
5. **공유 로그 파일 필수**: 파이프라인 실행 시 `_sdd/pipeline/log_<topic>_<timestamp>.md`를 생성하고, 각 에이전트 완료 후 핵심 결정사항을 추출하여 기록한다. 에이전트는 로그 파일의 존재를 모른다.
6. **한국어 기본, 사용자 언어 따름**: 사용자가 영어로 요청하면 영어로, 한국어로 요청하면 한국어로 진행한다.
7. **파일 기반 상태 전달**: 각 에이전트에는 파일 경로만 전달한다. 에이전트의 전체 출력을 부모 컨텍스트에 누적하지 않는다. 에이전트 결과에서 핵심 정보(출력 파일 경로, 주요 결정사항)만 추출한다.
8. **에이전트 호출 시 원문 전달**: 에이전트에 프롬프트를 전달할 때 사용자의 원래 요청과 관련 컨텍스트 파일 경로를 포함한다. 요약하지 않는다.

## Process

### Step 1: Request Analysis (요청 분석)

**Tools**: 없음 (내부 분석)

사용자 요청을 파싱하여 초기 방향을 설정한다.

1. **요청 파싱**: 사용자 입력에서 다음을 추출한다:
   - 기능 설명 (무엇을 만들려는가)
   - 기술적 키워드 (프레임워크, 라이브러리, 패턴 등)
   - 명시된 제약 조건 (있는 경우)
   - 기존 코드와의 관계 (신규 vs 수정 vs 확장)

2. **초기 복잡도 예측**: 요청만으로 대략적인 규모를 예측한다 (Step 4에서 정밀 판단):
   - 키워드가 1-2개, 범위가 좁음 → 소규모 예측
   - 여러 컴포넌트 언급, 중간 범위 → 중규모 예측
   - 시스템 레벨 변경, 넓은 범위 → 대규모 예측

3. **Discussion 필요도 판단**:
   - 요구사항이 명확하고 범위가 좁으면 → Step 2를 축소 (1-2 질문)
   - 요구사항이 모호하거나 범위가 넓으면 → Step 2를 전체 실행 (3-5 질문)

**Decision Gate 1 -> 2**:
```
request_parsed = 기능 설명이 추출됨
initial_direction = 초기 복잡도 예측 완료

IF request_parsed → Step 2 진행
ELSE → 사용자에게 기능 설명 요청 (AskUserQuestion)
```

### Step 2: Inline Discussion (인라인 토론)

**Tools**: `AskUserQuestion`

> **중요**: 이 단계는 서브에이전트가 아닌 autopilot 스킬 내에서 인라인으로 실행한다. Discussion 에이전트를 호출하지 않는다.

사용자와 대화하여 요구사항을 구체화한다. Step 1의 초기 분석 결과에 따라 질문 횟수를 조절한다.

#### 2.1 질문 전략

| 초기 복잡도 | 질문 횟수 | 초점 |
|-------------|----------|------|
| 소규모 | 1-2회 | 정확한 범위 확인, 제약 조건 |
| 중규모 | 2-3회 | 기능 범위, 기술 선택, 우선순위 |
| 대규모 | 3-5회 | 아키텍처 방향, 단계별 전략, 리스크 |

#### 2.2 AskUserQuestion 형식

```
AskUserQuestion: "[구체적인 질문]"
옵션:
1. "[선택지 A]"
2. "[선택지 B]"
3. "[선택지 C]"
4. "충분합니다 — 진행해주세요"
```

매 질문에 "충분합니다 -- 진행해주세요" 옵션을 반드시 포함한다. 사용자가 이를 선택하면 즉시 Step 3으로 진행한다.

#### 2.3 수집 대상 정보

- **기능 범위**: 정확히 어디까지 구현할 것인가
- **기술 제약**: 특정 기술 스택, 라이브러리, 패턴 요구사항
- **우선순위**: MVP vs 완성도 높은 구현
- **테스트 요구사항**: 테스트 범위, 필수 테스트 시나리오
- **스펙 변경 여부**: 기존 스펙에 추가/수정이 필요한지

#### 2.4 내부 상태 기록

Discussion 중 다음을 내부적으로 추적한다 (파일로 저장하지 않음):

```
requirements = []       # 확정된 요구사항
constraints = []        # 제약 조건
technical_decisions = [] # 기술적 결정
test_requirements = []   # 테스트 요구사항
```

**Decision Gate 2 -> 3**:
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

**Decision Gate 3 -> 4**:
```
analysis_complete = 프로젝트 구조와 관련 파일이 식별됨

IF analysis_complete → Step 4 진행
IF Explore agent 실패 → 직접 탐색으로 보완 후 Step 4 진행
```

### Step 4: Scale Assessment (규모 판단)

**Tools**: 없음 (내부 분석)

Step 2-3에서 수집한 정보를 기반으로 규모를 판단하고, 적절한 파이프라인과 테스트 전략을 결정한다.

> 상세 판단 기준은 [Scale Assessment Criteria (상세)](#scale-assessment-criteria-상세) 섹션 참조.
> 파이프라인 템플릿은 `references/scale-assessment.md` 참조.

#### 4.1 규모 판단

| 규모 | 영향 파일 수 | 스펙 변경 | 신규 컴포넌트 | 파이프라인 |
|------|-------------|----------|-------------|----------|
| **소규모** | 1-3개 | 없음 | 0-1개 | implementation → 인라인 테스트 |
| **중규모** | 4-10개 | 패치 필요 | 1-3개 | feature-draft → impl-plan → impl → review → 인라인 테스트 → spec-sync |
| **대규모** | 10개+ | 신규 섹션 | 3개+ | full pipeline (모든 agent) |

#### 4.2 테스트 전략 결정

| 조건 | 전략 | 설명 |
|------|------|------|
| 테스트 1회 실행 < 수 분 | **인라인 디버깅** | implementation 에이전트가 테스트-수정-재시도 루프를 직접 실행 |
| 테스트 1회 실행 > 수십 분 | **ralph-loop-init** | ralph-loop-init 에이전트로 장시간 자동 디버깅 루프 설정 |

테스트 전략 판단 기준:
- 단위 테스트, 통합 테스트 → 인라인 디버깅 (대부분의 경우)
- ML 학습 루프, 대규모 빌드, E2E 테스트 → ralph-loop-init

#### 4.3 파이프라인 선택

규모에 따라 사용할 에이전트 조합을 결정한다:

**소규모 파이프라인**:
```
implementation agent → 인라인 테스트 → (완료)
```

**중규모 파이프라인**:
```
feature-draft agent → implementation-plan agent → implementation agent
→ review-fix loop (max 3회) → 인라인 테스트 → spec-update-done agent
```

**대규모 파이프라인**:
```
feature-draft agent → spec-update-todo agent → implementation-plan agent
→ implementation agent → review-fix loop (max 3회)
→ 테스트 (인라인 or ralph-loop-init) → spec-update-done agent
→ spec-review agent (선택)
```

**Decision Gate 4 -> 5**:
```
scale_determined = 규모가 소/중/대 중 하나로 결정됨
pipeline_selected = 사용할 에이전트 조합이 결정됨
test_strategy_decided = 테스트 전략이 결정됨

IF scale_determined AND pipeline_selected → Step 5 진행
```

### Step 5: Orchestrator Generation (오케스트레이터 생성)

**Tools**: `Write`

규모에 맞는 맞춤형 오케스트레이터 파일을 생성하여 `_sdd/pipeline/`에 저장한다.

> 오케스트레이터 표준 포맷은 [Orchestrator Template](#orchestrator-template) 섹션 참조.
> 규모별 구체적 예시는 `references/pipeline-templates.md` 참조.
> 완성된 오케스트레이터 예시는 `examples/sample-orchestrator.md` 참조.

#### 5.1 파일 경로

```
_sdd/pipeline/orchestrator_<topic>_<timestamp>.md
```

- `<topic>`: 기능명을 영문 snake_case로 변환 (e.g., "인증 시스템" → `auth_system`)
- `<timestamp>`: `YYYYMMDD_HHmmss` 형식

#### 5.2 생성 절차

1. `_sdd/pipeline/` 디렉토리 생성 (없으면 `mkdir -p`)
2. `references/pipeline-templates.md`를 Read하여 해당 규모의 템플릿을 참조
3. Step 2-4에서 수집한 정보를 템플릿에 반영하여 오케스트레이터 생성
4. `examples/sample-orchestrator.md`를 Read하여 품질 기준 참조
5. 오케스트레이터 파일을 `Write`로 저장

#### 5.3 오케스트레이터에 포함할 정보

- **기능 설명**: 사용자 요청 원문 + 구체화된 요구사항
- **파이프라인 단계**: 에이전트 호출 순서와 각 단계의 프롬프트
- **컨텍스트 파일 경로**: 각 에이전트에 전달할 `_sdd/` 파일 경로
- **Review-fix 루프 설정**: 최대 반복 횟수, 종료 조건
- **테스트 전략**: 인라인 vs ralph-loop-init
- **에러 핸들링**: 에이전트별 실패 시 대응 방침
- **필요 리소스**: Pre-flight Check에서 확인된 리소스 목록 (Step 5.4 참조)

#### 5.4 Pre-flight Check (리소스 사전 점검)

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
    status = "✅ 확인됨 (env.md)"
  else:
    status = "❌ 미확인"

→ Pre-flight Check 테이블 생성
```

Pre-flight Check 결과는 Step 6 (User Checkpoint)에서 파이프라인 요약과 함께 사용자에게 제시한다.

**Decision Gate 5 -> 6**:
```
orchestrator_created = 오케스트레이터 파일이 _sdd/pipeline/에 저장됨

IF orchestrator_created → Step 6 진행
```

### Step 6: User Checkpoint (사용자 확인)

**Tools**: `AskUserQuestion`, `Read`, `Edit`

생성된 오케스트레이터를 사용자에게 제시하고, 확인/수정 후 실행 승인을 받는다.

> **이 단계가 Phase 1(Interactive)의 마지막이다.** 승인 후 Phase 2(Autonomous)로 진입하면 사용자 중단 없이 완료까지 진행한다.

#### 6.1 파이프라인 요약 + Pre-flight Check 제시

파이프라인 요약과 Pre-flight Check 결과를 함께 제시한다:

```
## 생성된 파이프라인 요약

| 항목 | 내용 |
|------|------|
| 기능 | [기능 설명] |
| 규모 | [소/중/대] |
| 파이프라인 | [agent1] → [agent2] → ... |
| 예상 에이전트 수 | N개 |
| Review 최대 횟수 | 3회 |
| 테스트 전략 | [인라인 디버깅 / ralph-loop-init] |
| 오케스트레이터 경로 | _sdd/pipeline/orchestrator_xxx.md |

## Pre-flight Check

| 리소스 | 상태 | 출처 | 필요 단계 |
|--------|------|------|----------|
| [런타임/환경] | ✅/❌ | env.md / 미확인 | [어떤 에이전트에서 필요] |
| [테스트 프레임워크] | ✅/❌ | env.md / 미확인 | implementation |
| [외부 서비스] | ✅/❌ | env.md / 미확인 | implementation |
| [환경 변수] | ✅/❌ | env.md / 미확인 | implementation |
```

- ✅ 항목만 있으면 → 바로 실행 가능
- ❌ 항목이 있으면 → 사용자에게 해결 방법을 제시

#### 6.2 사용자 확인

```
AskUserQuestion: "위 파이프라인과 리소스를 확인해 주세요."
옵션:
1. "모두 준비됨 — 실행해주세요"
2. "env.md에 추가할 정보가 있습니다" → 사용자 입력을 받아 env.md Edit 후 재확인
3. "❌ 리소스 없이 진행 (mock 처리)" → 해당 리소스를 mock/skip으로 처리하도록 오케스트레이터 수정
4. "취소합니다"
```

#### 6.3 수정 처리

사용자가 수정을 요청하면:
1. 수정 사항을 파악
2. 오케스트레이터 파일을 `Edit`으로 수정
3. 수정된 요약을 다시 제시
4. 재확인 (최대 3회 반복)

**Decision Gate 6 -> 7**:
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
   로그 파일 초기 내용은 [Pipeline Log Format](#pipeline-log-format) 참조.

2. **오케스트레이터 읽기**: `Read`로 오케스트레이터 파일을 읽어 파이프라인 단계를 확인한다.

3. **마일스톤 출력**:
   ```
   [sdd-autopilot] 파이프라인 실행을 시작합니다.
   규모: <소/중/대> | 단계: N개 | 시작: <timestamp>
   ```

#### 7.2 파이프라인 실행 루프

오케스트레이터에 정의된 순서대로 각 에이전트를 호출한다.

```
FOR EACH step IN pipeline_steps:
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
  4. 결과 처리:
     - 에이전트 결과에서 핵심 정보 추출 (출력 파일 경로, 주요 결정사항)
     - 로그에 완료 기록 + 핵심 결정사항 추가 (Edit)
  5. 마일스톤 출력: "[sdd-autopilot] Step N/M: <agent-name> 완료 -- <출력 파일 경로>"
  6. 에러 발생 시: Error Handling 절차 실행 (7.5절)
```

#### 7.3 Review-Fix 루프

implementation 에이전트 완료 후 implementation-review 에이전트로 리뷰를 수행한다.

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

     IF review_count == MAX_REVIEW:
       → 마일스톤: "[sdd-autopilot] 리뷰 루프 종료 (최대 3회 도달) -- 잔여 이슈 로그 기록"
       → 잔여 이슈를 로그에 기록하고 다음 단계 진행
       → BREAK

  4. 수정 실행:
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
```

#### 7.4 테스트 실행

리뷰 완료 후 테스트를 실행한다. 오케스트레이터에 정의된 테스트 전략에 따라 분기한다.

**인라인 디버깅** (대부분의 경우):
```
implementation 에이전트에 테스트 실행을 포함하여 호출:
Agent(
  subagent_type="implementation",
  prompt="구현된 코드의 테스트를 실행하고, 실패하는 테스트가 있으면 수정하세요.

  테스트 실행 명령: <프로젝트의 테스트 명령>
  수정 대상 코드: <구현된 파일 목록>

  테스트 통과까지 수정-재실행 루프를 반복하세요 (최대 5회)."
)
```

**ralph-loop-init** (장시간 테스트):
```
Agent(
  subagent_type="ralph-loop-init",
  prompt="다음 기능의 자동 디버깅 루프를 설정하세요.

  기능 설명: <기능 설명>
  테스트 명령: <테스트 실행 명령>
  관련 파일: <구현된 파일 목록>"
)
```

#### 7.5 에러 핸들링

에이전트 호출 중 에러가 발생하면 다음 절차를 따른다.

> 상세 에러 유형별 대응은 [Error Handling (상세)](#error-handling-상세) 섹션 참조.

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
    4. 마일스톤: "[sdd-autopilot] <agent-name> 실패 -- 최대 재시도(3회) 초과. 다음 단계로 진행합니다."
    5. 해당 단계를 건너뛰고 다음 단계로 진행
       (단, 핵심 단계 실패 시 파이프라인 중단 가능 -- 아래 참조)
```

**핵심 단계 실패 시 파이프라인 중단 기준:**
- `implementation` 에이전트 실패 → 파이프라인 중단 (구현 없이 진행 불가)
- `feature-draft` 에이전트 실패 → 파이프라인 중단 (계획 없이 구현 불가)
- 기타 에이전트 실패 → 건너뛰고 진행 (로그에 기록)

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

파이프라인 완료 후 로그 파일을 마무리하고, 최종 결과를 사용자에게 보고한다.

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

#### 8.2 사용자에게 최종 보고

```
## SDD Autopilot 실행 완료

| 항목 | 결과 |
|------|------|
| 기능 | <기능 설명> |
| 규모 | <소/중/대> |
| 파이프라인 | <실행된 에이전트 목록> |
| 생성/수정 파일 | N개 |
| Review 결과 | N회 (critical/high 0건) |
| 테스트 | 통과 N/N |
| 스펙 동기화 | 완료 |
| 로그 파일 | _sdd/pipeline/log_<topic>_<timestamp>.md |
| 오케스트레이터 | _sdd/pipeline/orchestrator_<topic>_<timestamp>.md |

### 주요 산출물
- <산출물 1 경로 및 설명>
- <산출물 2 경로 및 설명>

### 잔여 이슈 (있는 경우)
- <이슈 목록>

### 후속 작업 제안 (있는 경우)
- <제안 1>
- <제안 2>
```

## Orchestrator Template

autopilot이 Step 5에서 생성하는 오케스트레이터 파일의 표준 포맷이다. SKILL.md 표준을 따르되, 파이프라인 실행에 특화된 구조를 갖는다.

```markdown
# Orchestrator: <기능명>

**생성일**: <timestamp>
**규모**: <소/중/대>
**생성자**: autopilot

## 기능 설명

<사용자 요청 원문>

### 구체화된 요구사항
- <요구사항 1>
- <요구사항 2>

### 제약 조건
- <제약 1>

## Pipeline Steps

### Step 1: <agent-name>

**에이전트**: <subagent_type>
**입력 파일**: <_sdd/ 경로 목록>
**출력 파일**: <예상 출력 경로>

**프롬프트**:
```
<에이전트에 전달할 프롬프트 전문>
```

### Step 2: <agent-name>
...

## Review-Fix Loop

- **최대 반복**: 3회
- **종료 조건**: critical = 0 AND high = 0
- **수정 대상**: critical/high만 (medium/low는 로그 기록)

## Test Strategy

- **방식**: <인라인 디버깅 / ralph-loop-init>
- **테스트 명령**: <프로젝트 테스트 실행 명령>
- **최대 재시도**: 5회

## Error Handling

- **재시도 횟수**: 3회
- **핵심 단계**: <실패 시 중단할 에이전트 목록>
- **비핵심 단계**: <건너뛸 수 있는 에이전트 목록>
```

> 완성된 예시는 `examples/sample-orchestrator.md`를 참조한다.

## Pipeline Log Format

파이프라인 실행 중 `_sdd/pipeline/log_<topic>_<timestamp>.md`에 기록하는 표준 포맷이다.

### 로그 파일 초기 구조

```markdown
# Pipeline Log: <기능명>

**시작**: <timestamp>
**규모**: <소/중/대>
**파이프라인**: <agent1> -> <agent2> -> ...
**오케스트레이터**: _sdd/pipeline/orchestrator_<topic>_<timestamp>.md

## 실행 로그

(각 에이전트 완료 시 아래에 엔트리 추가)
```

### 에이전트 완료 엔트리

```markdown
### <agent-name> -- <완료/실패/스킵>
- **시간**: <시작 HH:mm:ss> ~ <완료 HH:mm:ss> (<소요 시간>)
- **출력**: `<출력 파일 경로>`
- **핵심 결정사항**:
  - <결정 1>
  - <결정 2>
- **이슈**: <있으면 기록, 없으면 "없음">
```

### Review-Fix 루프 엔트리

```markdown
### review-fix -- Round N/3
- **리뷰 결과**: critical N건, high N건, medium N건, low N건
- **수정 대상**: <critical/high 이슈 목록>
- **수정 결과**: 완료 / 부분 완료
```

### 에러 엔트리

```markdown
### ERROR: <agent-name> -- 재시도 N/3
- **에러 내용**: <에러 메시지>
- **원인 분석**: <분석 결과>
- **조치**: <수행한 조치>
- **결과**: 해결 / 미해결
```

### 핵심 결정사항 추출 방식

autopilot은 각 에이전트의 결과 텍스트에서 핵심 결정사항을 추출하여 로그에 기록한다. 에이전트는 로그 파일의 존재를 모른다.

추출 기준:
1. 에이전트가 "결정", "선택", "방향", "전략", "채택" 등의 단어와 함께 기술한 내용
2. 에이전트가 생성한 파일의 핵심 구조 (e.g., "3개 모듈로 분리", "TDD 방식 채택")
3. 추출이 어려운 경우 에이전트의 주요 행동을 1-3줄로 요약

## Scale Assessment Criteria (상세)

> 상세 판단 가이드라인과 경계 사례 예시는 `references/scale-assessment.md`를 Read하여 참조한다.

### 정량적 기준

| 기준 | 소규모 | 중규모 | 대규모 |
|------|--------|--------|--------|
| 영향 파일 수 | 1-3 | 4-10 | 10+ |
| 신규 파일 수 | 0-1 | 1-5 | 5+ |
| 신규 컴포넌트/모듈 | 0-1 | 1-3 | 3+ |
| 스펙 변경 | 없음 | 기존 섹션 패치 | 신규 섹션 추가 |
| 예상 코드 줄 수 | < 200 | 200-1000 | 1000+ |

### 정성적 기준

| 기준 | 소규모 | 중규모 | 대규모 |
|------|--------|--------|--------|
| 복잡도 | 단일 함수/클래스 수정 | 여러 모듈 연동 | 아키텍처 레벨 변경 |
| 의존성 | 기존 코드 내 수정 | 새 의존성 1-2개 | 새 의존성 3개+ |
| 테스트 범위 | 단위 테스트 몇 개 | 통합 테스트 포함 | E2E 테스트 필요 |
| 리스크 | 낮음 (로컬 변경) | 중간 (모듈 간 영향) | 높음 (시스템 전체 영향) |

### 경계 사례 처리

- 정량적 기준과 정성적 기준이 다른 규모를 가리키면 → **더 큰 규모를 선택**
- 확신이 없으면 → 중규모를 기본값으로 사용
- 사용자가 "빠르게 해줘", "간단히" 등을 언급하면 → 규모를 한 단계 낮추는 것을 고려
- 기존 코드 수정 없이 순수 신규 생성이면 → 파일 수 기준을 한 단계 완화

### 테스트 전략 판단 기준

| 조건 | 판단 근거 | 전략 |
|------|----------|------|
| 단위 테스트, 통합 테스트 | 실행 시간 수 초 ~ 수 분 | 인라인 디버깅 |
| 빌드 + 전체 테스트 스위트 | 실행 시간 수 분 ~ 10분 | 인라인 디버깅 |
| ML 학습 루프 | 실행 시간 수십 분 ~ 수 시간 | ralph-loop-init |
| 대규모 E2E 테스트 | 실행 시간 30분+ | ralph-loop-init |
| CI/CD 파이프라인 | 외부 시스템 의존 | ralph-loop-init |

## Error Handling (상세)

### 에러 유형별 대응

| 에러 유형 | 원인 | 대응 |
|----------|------|------|
| 에이전트 실행 실패 | 서브에이전트가 에러를 반환 | 에러 내용 분석 → 입력 수정 → 재시도 |
| 파일 접근 실패 | 경로 오류 또는 파일 미존재 | 경로 확인/수정 → 재시도 |
| 출력 품질 미달 | 에이전트 결과가 기대와 다름 | 프롬프트 보완 → 재시도 |
| 컨텍스트 윈도우 소진 | 에이전트에 전달한 컨텍스트가 과다 | 컨텍스트 축소 후 재시도 |
| 의존 파일 미존재 | 이전 에이전트가 예상 출력을 생성하지 않음 | 이전 단계 확인 → 수동 생성 or 이전 단계 재실행 |

### 재시도 절차

```
ON ERROR at step N:
  1. 에러 상세를 로그에 기록
  2. 에러 원인 분석:
     - 에러 메시지 확인
     - 관련 파일/경로 확인
     - 입력 프롬프트 검증
  3. 원인에 따라 수정:
     - 파일 경로 오류 → 경로 수정
     - 입력 부족 → 추가 컨텍스트 포함
     - 프롬프트 문제 → 프롬프트 개선
  4. 수정된 입력으로 에이전트 재호출
  5. 최대 3회까지 반복
```

### 핵심 단계 vs 비핵심 단계

**핵심 단계** (실패 시 파이프라인 중단):
- `feature-draft`: 계획 없이 구현 불가
- `implementation-plan`: 구현 계획 없이 구현 불가
- `implementation`: 코드 생성 자체가 실패

**비핵심 단계** (실패 시 건너뛰고 진행):
- `implementation-review`: 리뷰 없이 진행 가능 (품질 리스크 로그)
- `spec-update-done`: 스펙 동기화는 수동으로 가능
- `spec-review`: 선택적 품질 검사
- `ralph-loop-init`: 인라인 디버깅으로 대체 가능

### 파이프라인 중단 시 보고

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

## Integration with SDD Agents

autopilot이 파이프라인에서 호출할 수 있는 에이전트 목록이다.

### 에이전트 목록

| 에이전트 | subagent_type | 역할 | 입력 경로 | 출력 경로 |
|---------|---------------|------|----------|----------|
| feature-draft | `"feature-draft"` | 스펙 패치 초안 + 구현 계획 초안 | (사용자 요청) | `_sdd/drafts/feature_draft_<topic>.md` |
| implementation-plan | `"implementation-plan"` | 상세 구현 계획 | `_sdd/drafts/` | `_sdd/implementation/IMPLEMENTATION_PLAN.md` |
| implementation | `"implementation"` | TDD 코드 구현 | `_sdd/implementation/` | 코드 파일들 |
| implementation-review | `"implementation-review"` | 코드 리뷰 | `_sdd/implementation/` + 코드 파일 | 리뷰 리포트 (텍스트) |
| ralph-loop-init | `"ralph-loop-init"` | 장시간 디버깅 루프 설정 | 코드 파일 + 테스트 명령 | `ralph/` 디렉토리 |
| spec-update-done | `"spec-update-done"` | 구현 완료 후 스펙 동기화 | `_sdd/spec/` + 코드 파일 | `_sdd/spec/` 업데이트 |
| spec-update-todo | `"spec-update-todo"` | 계획된 기능을 스펙에 추가 | `_sdd/drafts/` | `_sdd/spec/` 업데이트 |
| spec-review | `"spec-review"` | 스펙 문서 품질 리뷰 | `_sdd/spec/` | 리뷰 리포트 (텍스트) |

### 에이전트 호출 포맷

```
Agent(
  subagent_type="<agent-name>",
  prompt="<task description>

  컨텍스트 파일:
  - <파일 경로 1>
  - <파일 경로 2>

  사용자 원래 요청: <사용자 요청 원문>"
)
```

### 에이전트 간 의존 관계

```
feature-draft ──→ spec-update-todo (선택)
     │
     └──→ implementation-plan ──→ implementation ──→ implementation-review
                                       │                    │
                                       │←── (review-fix) ──←┘
                                       │
                                       └──→ 테스트 ──→ spec-update-done ──→ spec-review (선택)
```

### 보조 에이전트

| 에이전트 | subagent_type | 역할 | 사용 시점 |
|---------|---------------|------|----------|
| Explore | `"Explore"` | 코드베이스 탐색 | Step 3 (코드베이스 탐색) |
| general-purpose | `"general-purpose"` | 범용 리서치 | 필요 시 (기술 리서치 등) |

### 상태 전달 경로 요약

```
_sdd/discussion/discussion_<topic>.md    → (참조용, autopilot이 생성하지 않음)
_sdd/drafts/feature_draft_<topic>.md     → feature-draft 출력 → implementation-plan 입력
_sdd/implementation/IMPLEMENTATION_PLAN.md → impl-plan 출력 → implementation 입력
_sdd/pipeline/orchestrator_<topic>_<ts>.md → autopilot이 생성, Step 7에서 참조
_sdd/pipeline/log_<topic>_<ts>.md         → autopilot이 생성/갱신
```

## Additional Resources

### Reference Files

- **`references/pipeline-templates.md`** -- 소/중/대 규모별 파이프라인 템플릿. 오케스트레이터 생성 시 참조.
- **`references/scale-assessment.md`** -- 규모 판단 상세 가이드라인 및 경계 사례. Step 4에서 참조.

### Example Files

- **`examples/sample-orchestrator.md`** -- 중규모 기능(인증 시스템)에 대한 완성된 오케스트레이터 예시. 오케스트레이터 생성 품질 기준으로 사용.
