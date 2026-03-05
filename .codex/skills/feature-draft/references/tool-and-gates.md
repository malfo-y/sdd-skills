# Tool Mapping, Decision Gates & Context Management (Non-Interactive)

`SKILL.md` step execution map with deterministic gates and no mid-process user prompts.

---

## 1) Tool Mapping Per Step

| Step | Primary Tools | When to Use |
|------|---------------|-------------|
| Step 1: Input Analysis | `Read`, `Glob`, `Bash (git diff)` | 입력 파일/코드 변경 확인 |
| Step 2: Context Gathering | `Glob`, `Read`, `rg` | 스펙/코드베이스 구조 파악 |
| Step 3: Adaptive Completion | `deterministic defaults (non-interactive)` | 누락 정보 자동 보완 |
| Step 4: Feature Design | `rg`, `Glob` | Target Files 및 섹션 매핑 |
| Step 5: Spec Patch Generation | — | Part 1 생성 |
| Step 5.5: Part 1 Internal Check | `deterministic defaults (non-interactive)` | Part 1 품질 점검/보정 |
| Step 6: Implementation Plan | — | Part 2 생성 |
| Step 7: Review & Save | `Write`, `Bash (mkdir/mv)`, `Glob` | 저장/아카이브/무결성 검증 |

---

## 2) Decision Gates

### Gate 1->2: Spec Availability

```text
AFTER Step 1:
  spec_exists = Glob("_sdd/spec/*.md") 결과 존재 (user_* / DECISION_LOG 제외)

  IF spec_exists:
    -> Step 2
  ELSE:
    -> deterministic defaults:
         - "spec-create 먼저 실행" 경로를 기본 권고로 기록
         - 또는 Part 2 only 모드로 계속 진행
```

### Gate 3->4: Minimum Information

```text
AFTER Step 3:
  has_feature_name
  has_description
  has_type

  IF all true:
    -> Step 4
  ELSE:
    -> 최대 2라운드 내부 보완 수행
       (휴리스틱/기존 패턴/코드 근거)
    -> 여전히 누락이면 Open Questions 기록 후 진행
```

### Gate 4->5: Design Completeness

```text
AFTER Step 4:
  has_classification
  has_target_sections
  has_target_files_draft

  IF all true:
    -> Step 5
  ELSE:
    -> 누락 항목 보완 후 재검증
```

### Gate 5->6: Part 1 Internal Check

```text
AFTER Step 5:
  validate_part1 = 필수 섹션/근거/우선순위/Open Questions 점검

  IF validate_part1:
    -> Step 6
  ELSE:
    -> Part 1 자동 보정 후 Step 6
```

### Gate 6->7: Output Completeness

```text
AFTER Step 6:
  has_part1 (or Part 2 only mode)
  has_part2
  has_parallel_summary

  IF all true:
    -> Step 7
  ELSE:
    -> 미완료 항목 보완 후 재검증
```

---

## 3) Context Management

### Spec Size Strategy

| 스펙 크기 | 전략 | 방법 |
|-----------|------|------|
| < 200줄 | 전체 읽기 | `Read` 전체 |
| 200-500줄 | 전체+선택 | 전체 읽기 + 섹션 재확인 |
| 500-1000줄 | TOC 우선 | TOC 후 관련 섹션 |
| > 1000줄 | 인덱스 우선 | 인덱스 + 타겟 섹션 최대 3개 |

### Codebase Size Strategy

| 코드베이스 크기 | 전략 | 방법 |
|----------------|------|------|
| < 50 files | 자유 탐색 | `Glob` + `Read` |
| 50-200 files | 타겟 탐색 | `rg`/`Glob` 후보 후 `Read` |
| > 200 files | 최소 탐색 | `rg`/`Glob` 중심, 최소 `Read` |

---

## 4) Output Integrity Checks

Before final save:

- 모든 Task에 `Target Files` 존재
- `[M]` 파일은 실제 존재 확인
- `[C]` 파일은 충돌 여부 확인
- 중복 충돌 파일은 순차 실행 표기
- 저신뢰 추정은 `Open Questions`에 근거와 함께 기록
