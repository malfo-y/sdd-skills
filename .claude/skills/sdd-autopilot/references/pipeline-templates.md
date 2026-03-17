# Pipeline Templates -- 규모별 파이프라인 템플릿

autopilot이 오케스트레이터를 생성할 때 참조하는 규모별 파이프라인 템플릿이다.

---

## 소규모 파이프라인

### 적용 조건

- 영향 파일 1-3개
- 스펙 변경 없음
- 신규 컴포넌트 0-1개
- 단일 함수/클래스 수정 수준

### 파이프라인 구조

```
implementation agent → 인라인 테스트 → (완료)
```

### 오케스트레이터 예시

```markdown
# Orchestrator: <기능명>

**생성일**: <timestamp>
**규모**: 소규모
**생성자**: autopilot

## 기능 설명

<사용자 요청 원문>

### 구체화된 요구사항
- <요구사항>

## Pipeline Steps

### Step 1: implementation

**에이전트**: implementation
**입력 파일**: (없음 -- 직접 코드 수정)
**출력 파일**: <수정 대상 파일 목록>

**프롬프트**:
다음 기능을 구현하세요: <기능 설명>

수정 대상 파일:
- <파일 경로 1>

요구사항:
- <요구사항 1>

구현 완료 후 테스트를 실행하고, 실패하는 테스트가 있으면 수정하세요.
테스트 명령: <테스트 명령>
최대 수정-재실행 5회.

사용자 원래 요청: <사용자 요청 원문>

## Review-Fix Loop

> **Hard Rule #9**: 파이프라인에 review가 포함되면 review-fix 사이클은 필수.
> 소규모에서도 review가 포함된 경우(사용자 요청, 부분 파이프라인 등) 동일하게 적용.

- 소규모 기본: review 미포함 (implementation 에이전트가 자체 테스트로 품질 확보)
- **단, review가 포함되면**: review → fix → re-review 사이클 필수 실행 (최대 3회)

## Test Strategy

- **방식**: 인라인 디버깅 (implementation 에이전트 내)
- **테스트 명령**: <프로젝트 테스트 명령>

## Error Handling

- **재시도 횟수**: 3회
- **핵심 단계**: implementation, implementation-review (review 포함 시)
```

---

## 중규모 파이프라인

### 적용 조건

- 영향 파일 4-10개
- 기존 스펙 섹션 패치 필요
- 신규 컴포넌트 1-3개
- 여러 모듈 연동 수준

### 파이프라인 구조

```
feature-draft agent → implementation-plan agent → implementation agent
→ review-fix loop (max 3회) → 인라인 테스트 → spec-update-done agent
```

### 오케스트레이터 예시

```markdown
# Orchestrator: <기능명>

**생성일**: <timestamp>
**규모**: 중규모
**생성자**: autopilot

## 기능 설명

<사용자 요청 원문>

### 구체화된 요구사항
- <요구사항 1>
- <요구사항 2>

### 제약 조건
- <제약 1>

## Pipeline Steps

### Step 1: feature-draft

**에이전트**: feature-draft
**입력 파일**: (없음)
**출력 파일**: `_sdd/drafts/feature_draft_<topic>.md`

**프롬프트**:
다음 기능에 대한 feature draft를 작성하세요: <기능 설명>

요구사항:
- <요구사항 1>
- <요구사항 2>

제약 조건:
- <제약 1>

기존 스펙 문서: `_sdd/spec/main.md`
기존 코드베이스 구조: <프로젝트 구조 요약>

사용자 원래 요청: <사용자 요청 원문>

### Step 2: implementation-plan

**에이전트**: implementation-plan
**입력 파일**: `_sdd/drafts/feature_draft_<topic>.md`
**출력 파일**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

**프롬프트**:
다음 feature draft를 기반으로 구현 계획을 작성하세요.

Feature draft: `_sdd/drafts/feature_draft_<topic>.md`
기존 스펙: `_sdd/spec/main.md`

사용자 원래 요청: <사용자 요청 원문>

### Step 3: implementation

**에이전트**: implementation
**입력 파일**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
**출력 파일**: <코드 파일 목록>

**프롬프트**:
다음 구현 계획을 실행하세요.

구현 계획: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

사용자 원래 요청: <사용자 요청 원문>

### Step 4: review-fix loop (필수 사이클)

(autopilot이 직접 관리 -- review-fix loop 섹션 참조)
**Hard Rule #9 적용**: review → fix → re-review 사이클 필수. 리뷰만 하고 끝나지 않음.

### Step 5: spec-update-done

**에이전트**: spec-update-done
**입력 파일**: `_sdd/spec/main.md`, <구현된 코드 파일 목록>
**출력 파일**: `_sdd/spec/main.md` (업데이트)

**프롬프트**:
구현이 완료되었습니다. 스펙 문서를 실제 구현과 동기화하세요.

스펙 문서: `_sdd/spec/main.md`
구현 계획: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
구현된 주요 파일: <파일 목록>

사용자 원래 요청: <사용자 요청 원문>

## Review-Fix Loop (필수 사이클)

> **Hard Rule #9**: review → fix → re-review 사이클 필수. 리뷰만 하고 끝나지 않음.

- **최대 반복**: 3회
- **종료 조건**: critical = 0 AND high = 0
- **수정 대상**: critical/high만 (medium/low는 로그 기록)
- **사이클 필수**: 이슈 발견 시 fix → re-review 반드시 실행. 단일 리뷰로 종료 불가.

## Test Strategy

- **방식**: 인라인 디버깅
- **테스트 명령**: <프로젝트 테스트 명령>
- **최대 재시도**: 5회

## Error Handling

- **재시도 횟수**: 3회
- **핵심 단계**: feature-draft, implementation-plan, implementation, implementation-review (review-fix 사이클 포함)
- **비핵심 단계**: spec-update-done
```

---

## 대규모 파이프라인

### 적용 조건

- 영향 파일 10개+
- 신규 스펙 섹션 추가 필요
- 신규 컴포넌트 3개+
- 아키텍처 레벨 변경 수준

### 파이프라인 구조

```
feature-draft agent → spec-update-todo agent → implementation-plan agent
→ implementation agent → review-fix loop (max 3회)
→ 테스트 (인라인 or ralph-loop-init) → spec-update-done agent
→ spec-review agent (선택)
```

### 오케스트레이터 예시

```markdown
# Orchestrator: <기능명>

**생성일**: <timestamp>
**규모**: 대규모
**생성자**: autopilot

## 기능 설명

<사용자 요청 원문>

### 구체화된 요구사항
- <요구사항 1>
- <요구사항 2>
- <요구사항 3>

### 제약 조건
- <제약 1>
- <제약 2>

## Pipeline Steps

### Step 1: feature-draft

**에이전트**: feature-draft
**입력 파일**: (없음)
**출력 파일**: `_sdd/drafts/feature_draft_<topic>.md`

**프롬프트**:
다음 대규모 기능에 대한 feature draft를 작성하세요: <기능 설명>

요구사항:
- <요구사항 목록>

제약 조건:
- <제약 목록>

기존 스펙 문서: `_sdd/spec/main.md`
기존 코드베이스 구조: <프로젝트 구조 요약>

이 기능은 대규모로, 신규 스펙 섹션 추가가 필요합니다.

사용자 원래 요청: <사용자 요청 원문>

### Step 2: spec-update-todo

**에이전트**: spec-update-todo
**입력 파일**: `_sdd/drafts/feature_draft_<topic>.md`
**출력 파일**: `_sdd/spec/main.md` (업데이트)

**프롬프트**:
Feature draft의 스펙 패치를 스펙 문서에 반영하세요.

Feature draft: `_sdd/drafts/feature_draft_<topic>.md`
스펙 문서: `_sdd/spec/main.md`

사용자 원래 요청: <사용자 요청 원문>

### Step 3: implementation-plan

**에이전트**: implementation-plan
**입력 파일**: `_sdd/drafts/feature_draft_<topic>.md`, `_sdd/spec/main.md`
**출력 파일**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

**프롬프트**:
Feature draft와 업데이트된 스펙을 기반으로 상세 구현 계획을 작성하세요.

Feature draft: `_sdd/drafts/feature_draft_<topic>.md`
스펙 문서: `_sdd/spec/main.md`
규모: 대규모 (10개+ 파일 예상)

병렬 실행 가능한 태스크를 식별하고 Target Files를 명시하세요.

사용자 원래 요청: <사용자 요청 원문>

### Step 4: implementation

**에이전트**: implementation
**입력 파일**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
**출력 파일**: <코드 파일 목록>

**프롬프트**:
구현 계획을 실행하세요.

구현 계획: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

대규모 구현이므로 Phase별로 진행하세요.
각 Phase 완료 후 중간 테스트를 실행하세요.

사용자 원래 요청: <사용자 요청 원문>

### Step 5: review-fix loop

(autopilot이 직접 관리)

### Step 6: 테스트

(테스트 전략에 따라 인라인 or ralph-loop-init)

### Step 7: spec-update-done

**에이전트**: spec-update-done
**입력 파일**: `_sdd/spec/main.md`, <구현된 코드 파일 목록>
**출력 파일**: `_sdd/spec/main.md` (업데이트)

**프롬프트**:
대규모 구현이 완료되었습니다. 스펙 문서를 실제 구현과 동기화하세요.

스펙 문서: `_sdd/spec/main.md`
구현 계획: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
Feature draft: `_sdd/drafts/feature_draft_<topic>.md`
구현된 주요 파일: <파일 목록>

사용자 원래 요청: <사용자 요청 원문>

### Step 8: spec-review (선택)

**에이전트**: spec-review
**입력 파일**: `_sdd/spec/main.md`
**출력 파일**: 리뷰 리포트 (텍스트)

**프롬프트**:
업데이트된 스펙 문서의 품질을 리뷰하세요.

스펙 문서: `_sdd/spec/main.md`

특히 다음을 확인하세요:
- 새로 추가된 섹션의 완성도
- 기존 섹션과의 일관성
- 구현과의 정합성

## Review-Fix Loop (필수 사이클)

> **Hard Rule #9**: review → fix → re-review 사이클 필수. 리뷰만 하고 끝나지 않음.

- **최대 반복**: 3회
- **종료 조건**: critical = 0 AND high = 0
- **수정 대상**: critical/high만 (medium/low는 로그 기록)
- **사이클 필수**: 이슈 발견 시 fix → re-review 반드시 실행. 단일 리뷰로 종료 불가.

## Test Strategy

- **방식**: <인라인 디버깅 / ralph-loop-init>
- **테스트 명령**: <프로젝트 테스트 명령>
- **최대 재시도**: 5회 (인라인) / 설정에 따름 (ralph-loop-init)

## Error Handling

- **재시도 횟수**: 3회
- **핵심 단계**: feature-draft, implementation-plan, implementation, implementation-review (review-fix 사이클 포함)
- **비핵심 단계**: spec-update-todo, spec-update-done, spec-review
```
