# Tool Mapping & Decision Gates

`SKILL.md` step execution map with deterministic gates.

---

## 1) Tool Mapping Per Step

| Step | Primary Tools | When to Use |
|------|---------------|-------------|
| Step 1: Identify Target Feature | `Read`, `Glob`, `Grep` | 사용자 요청에서 기능 후보 파악 |
| Step 2: Locate Spec Context | `Read`, `Glob`, `Grep` | 스펙 존재 확인 및 관련 섹션 추출 |
| Step 3: Gather Code Evidence | `Grep`, `Glob`, `Read`, `Bash (read-only)` | 관련 구현/테스트/타입 탐색 |
| Step 4: Resolve Gaps | `deterministic defaults (non-interactive)` | 누락 정보 보수적 보완 |
| Step 5: Generate Guide | — | 가이드 문서 작성 |
| Step 6: Save with Backup | `Bash (mkdir -p, cp/mv)`, `Write` | 저장/백업/경로 보고 |

---

## 2) 도구 선택 가이드: Grep vs Glob

| 상황 | 도구 | 이유 |
|------|------|------|
| "어떤 파일이 이 기능을 구현하나?" | Grep | 패턴 기반 검색 |
| "src/payments/ 구조 확인" | Glob | 경로/패턴 기반 탐색 |
| "confirmPayment 함수 참조 위치" | Grep | 특정 식별자 검색 |
| "*.test.ts 파일 목록" | Glob | 파일 패턴 매칭 |
| "이 에러 메시지가 어디서 나오나?" | Grep | 문자열 검색 |
| "components/ 하위 디렉토리 구조" | Glob | 디렉토리 탐색 |

---

## 3) Decision Gates

### Gate 1→2: Feature Identified

```text
AFTER Step 1:
  has_feature_candidate = 사용자 요청 또는 스펙에서 기능명 파싱 성공

  IF has_feature_candidate:
    -> Step 2
  ELSE:
    -> 사용자 요청을 재해석하여 최대 1회 재시도
    -> 여전히 불명확하면 가장 가까운 스펙 헤딩을 후보로 채택하고
       가정 사항으로 기록 후 Step 2 진행
```

### Gate 2→3: Spec Grounding

```text
AFTER Step 2:
  spec_found    = _sdd/spec/ 내 메인 또는 관련 스펙 파일 존재
  feature_grounded = 대상 기능의 목적/범위를 설명할 스펙 근거 존재

  IF spec_found AND feature_grounded:
    -> Step 3
  ELSE IF spec_found AND NOT feature_grounded:
    -> AskUserQuestion으로 사용자에게 선택지 제공:
       1) spec-update-todo를 실행하여 스펙에 기능을 추가한 뒤 다시 시도
       2) 스펙 근거 없이 Low 신뢰도로 가이드 생성 계속
  ELSE:
    -> AskUserQuestion으로 사용자에게 선택지 제공:
       1) spec-create를 실행하여 스펙을 먼저 작성
       2) 스펙 없이 Low 신뢰도로 가이드 생성 계속
```

### Gate 3→4: Evidence Sufficiency

```text
AFTER Step 3:
  has_code_evidence = 관련 파일/심볼/테스트 중 1개 이상 발견

  IF has_code_evidence:
    -> 신뢰도 High/Medium 후보로 Step 4
  ELSE:
    -> AskUserQuestion으로 사용자에게 확인:
       "코드 근거가 없습니다. 스펙 기반 Low 신뢰도 가이드를 생성할까요?"
    -> 사용자 동의 시 신뢰도 Low 후보로 Step 4
       (코드 레퍼런스 "확인 불가" 표기 예정)
```

### Gate 5→6: Output Completeness

```text
AFTER Step 5:
  has_background       = 배경 및 동기 섹션 작성됨
  has_core_design      = 핵심 설계 섹션 작성됨
  has_scenarios         = 사용 시나리오 가이드 작성됨 (정상 1개 + 예외 1개 이상)
  has_api_reference     = API 레퍼런스 작성됨
  has_impl_guide        = 구현 가이드 작성됨

  IF all true:
    -> Step 6
  ELSE:
    -> 누락 섹션 자동 보완 후 재검증
```

---

## 4) Context Management

### Spec Size Strategy

| 스펙 크기 | 전략 | 방법 |
|-----------|------|------|
| < 200줄 | 전체 읽기 | `Read` 전체 |
| 200–500줄 | 전체 + 선택 | 전체 읽기 + 관련 섹션 재확인 |
| > 500줄 | TOC 우선 | TOC 파악 후 관련 섹션만 정독 |

### Code Search Strategy

| 코드베이스 크기 | 전략 | 방법 |
|----------------|------|------|
| < 50 files | 자유 탐색 | `Glob` + `Read` |
| 50–200 files | 타겟 탐색 | `Grep`/`Glob` 후보 선별 후 `Read` |
| > 200 files | 최소 탐색 | `Grep` 키워드 중심, 최소 `Read` |
