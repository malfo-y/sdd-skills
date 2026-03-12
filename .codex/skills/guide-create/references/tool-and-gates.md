# Tool Mapping & Decision Gates

`SKILL.md` step execution map with deterministic gates and no mid-process user prompts.

---

## 1) Tool Mapping Per Step

| Step | Primary Tools | When to Use |
|------|---------------|-------------|
| Step 1: Identify Target Feature | `Read`, `Glob`, `rg` | 사용자 요청에서 기능 후보 파악 |
| Step 2: Locate Spec Context | `Read`, `Glob`, `rg` | 스펙 존재 확인 및 관련 섹션 추출 |
| Step 3: Gather Code Evidence | `rg`, `Glob`, `Read`, `Bash (read-only)` | 관련 구현/테스트/타입 탐색 |
| Step 4: Resolve Gaps | `deterministic defaults (non-interactive)` | 누락 정보 보수적 보완 |
| Step 5: Generate Guide | — | 가이드 문서 작성 |
| Step 6: Save with Backup | `Bash (mkdir -p, cp/mv)`, `Write` | 저장/백업/경로 보고 |

---

## 2) Decision Gates

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
    -> 스펙에 기능 언급이 부족함을 안내하고 중단
       (spec-update-todo 선행 권고)
  ELSE:
    -> 스펙 자체가 없음을 안내하고 중단
       (spec-create 선행 권고)
```

### Gate 3→4: Evidence Sufficiency

```text
AFTER Step 3:
  has_code_evidence = 관련 파일/심볼/테스트 중 1개 이상 발견

  IF has_code_evidence:
    -> 신뢰도 High/Medium 후보로 Step 4
  ELSE:
    -> 신뢰도 Low 후보로 Step 4
       (코드 레퍼런스 "확인 불가" 표기 예정)
```

### Gate 5→6: Output Completeness

```text
AFTER Step 5:
  has_explanation  = 설명 섹션 작성됨
  has_rules        = 규칙 섹션 작성됨
  has_checklist    = 체크리스트 섹션 작성됨
  has_examples     = 예시 섹션 작성됨 (최소 1개 긍정 예시)

  IF all true:
    -> Step 6
  ELSE:
    -> 누락 섹션 자동 보완 후 재검증
```

---

## 3) Context Management

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
| 50–200 files | 타겟 탐색 | `rg`/`Glob` 후보 선별 후 `Read` |
| > 200 files | 최소 탐색 | `rg` 키워드 중심, 최소 `Read` |
