# Tool Mapping, Decision Gates & Context Management

`SKILL.md`의 각 Step에서 사용할 도구, Step 간 전환 조건, 컨텍스트 관리 전략을 정의한다.

---

## 1. Tool Mapping Per Step

### Step별 도구 테이블

| Step | Primary Tools | When to Use |
|------|--------------|-------------|
| Step 1: Input Analysis | `Read`, `Glob`, `Bash (git diff)` | 기존 파일 확인, 코드 변경 분석 |
| Step 2: Context Gathering | `Glob`, `Read`, `rg` | 스펙 읽기, 코드베이스 탐색 |
| Step 3: Adaptive Clarification | `request_user_input (Plan mode) / direct question (Default mode)` | 사용자 추가 질문 |
| Step 4: Feature Design | `rg`, `Glob` | Target Files 매핑 시 파일 경로 확인 |
| Step 5: Spec Patch Generation | — | 출력 생성 (도구 불필요) |
| Step 5.5: Part 1 Checkpoint | `request_user_input (Plan mode) / direct question (Default mode)` | 사용자 확인 |
| Step 6: Implementation Plan | — | 출력 생성 (도구 불필요) |
| Step 7: Review & Confirm | `Write`, `Bash (mkdir/mv)`, `request_user_input (Plan mode) / direct question (Default mode)`, `Glob` | 파일 저장, 사용자 확인, Target Files 검증 |

### 도구 선택 가이드: rg vs Glob

| 상황 | 도구 | 이유 |
|------|------|------|
| "어떤 파일이 인증을 처리하나?" | `rg` | 패턴 기반 검색, 키워드로 관련 파일 식별 |
| "src/auth/ 디렉토리에 어떤 파일이 있나?" (패턴 기반 검색) | `Glob` | 정확한 경로/패턴을 알 때 |
| "`authenticate()` 함수를 호출하는 곳은?" (정확한 문자열 검색) | `rg` | 특정 식별자의 모든 참조를 찾을 때 |
| "이 프로젝트의 테스트 구조는?" | `Glob` | 파일 구조/패턴으로 탐색 |
| "conftest.py 파일 목록" (파일명 검색) | `Glob` | 파일명 패턴이 명확할 때 |

### Step별 도구 사용 상세

**Step 1: Input Analysis**
- `Glob("_sdd/spec/user_draft.md")` — 기존 드래프트 존재 여부 확인
- `Glob("_sdd/spec/user_spec.md")` — 사용자 스펙 존재 여부 확인
- `Glob("_sdd/implementation/user_input.md")` — 구현 입력 존재 여부 확인
- `Bash("git diff --name-only")` — 코드 변경 파일 목록 확인
- `Read` — 발견된 입력 파일 내용 읽기

**Step 2: Context Gathering**
- `Glob("_sdd/spec/*.md")` — 스펙 파일 목록 확인
- `Read` — 스펙 파일 읽기 (크기별 전략은 Context Management 참조)
- `Glob` — 코드베이스 구조 파악, 기존 파일 패턴 확인
- `Glob("_sdd/spec/DECISION_LOG.md")` — 의사결정 로그 존재 여부 확인

**Step 4: Feature Design**
- `rg` — "이 기능과 관련된 기존 코드는?" 형태의 패턴 검색
- `Glob` — Target Files 후보 경로 검증 (파일 존재 여부)

**Step 7: Review & Confirm**
- `Glob` — [M] 파일 존재 확인, [C] 파일 미존재 확인
- `Write` — 최종 드래프트 파일 저장
- `Bash("mkdir -p _sdd/drafts/prev")` — 디렉토리 생성
- `Bash("mv ...")` — 기존 파일 아카이브
- `request_user_input (Plan mode) / direct question (Default mode)` — 사용자에게 요약 제시 및 상세 확인 질문

---

## 2. Decision Gates

각 Step 전환점에서 다음 조건을 확인하고 분기한다.

### Gate 1→2: 스펙 존재 여부 확인

```
AFTER Step 1:
  spec_exists = Glob("_sdd/spec/*.md") returns results (excluding user_draft, user_spec, DECISION_LOG)

  IF spec_exists:
    → Step 2 (정상 진행)
  ELSE:
    → request_user_input (Plan mode) / direct question (Default mode):
        "스펙 문서가 없습니다. 어떻게 진행할까요?"
        옵션:
        1. "spec-create 먼저 실행" — 스킬 종료, spec-create 안내
        2. "Part 2만 생성" — Step 2에서 스펙 읽기 스킵, Part 1 생략 모드로 진행
```

### Gate 3→4: 최소 정보 체크리스트

```
AFTER Step 3:
  has_feature_name = feature name이 명확한가?
  has_description = feature 설명이 충분한가?
  has_type = 유형 분류가 가능한가? (New Feature / Improvement / Bug / etc.)

  IF has_feature_name AND has_description AND has_type:
    → Step 4 (정상 진행)
  ELSE:
    missing = 미충족 항목 목록
    round = 0
    WHILE missing is not empty AND round < 2:
      → request_user_input (Plan mode) / direct question (Default mode): missing 항목에 대해 질문
      round += 1
      missing 재평가
    IF missing is still not empty:
      → 사용 가능한 정보로 Step 4 진행 (누락 항목은 Open Questions에 기록)
```

### Gate 4→5: 설계 완료 확인

```
AFTER Step 4:
  has_classification = 요구사항이 유형별로 분류되었는가?
  has_target_sections = 각 항목에 Target Section이 매핑되었는가?
  has_target_files_draft = Target Files 초안이 작성되었는가?

  IF has_classification AND has_target_sections AND has_target_files_draft:
    → Step 5 (정상 진행)
  ELSE:
    → 미완료 항목 보완 후 재확인
```

### Gate 5→5.5→6: Part 1 확인 후 Part 2 진행

```
AFTER Step 5:
  → Step 5.5: Part 1 요약 테이블 제시
  → request_user_input (Plan mode) / direct question (Default mode): "Part 1 내용을 확인해 주세요. 진행/수정?"

  IF 사용자 확인 (진행):
    → Step 6
  ELSE IF 수정 요청:
    round = 0
    WHILE 수정 요청 AND round < 2:
      → Part 1 수정 반영
      → 수정된 부분 재제시
      round += 1
    → Step 6
```

### Gate 6→7: 전체 출력 완료 확인

```
AFTER Step 6:
  has_part1 = Part 1 (Spec Patch) 생성 완료 (또는 Part 2 only 모드)
  has_part2 = Part 2 (Implementation Plan) 생성 완료
  has_parallel_summary = 병렬 실행 요약 생성 완료

  IF has_part1 AND has_part2 AND has_parallel_summary:
    → Step 7 (정상 진행)
  ELSE:
    → 미완료 파트 생성 후 재확인
```

---

## 3. Context Management

### 스펙 크기별 읽기 전략

| 스펙 크기 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 200줄 | 전체 읽기 | `Read`로 전체 파일 읽기 |
| 200-500줄 | 전체 읽기 가능 | `Read`로 전체 읽기, 필요 시 섹션별 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 | 상위 50줄(TOC) 읽기 → 관련 섹션만 `Read(offset, limit)` |
| > 1000줄 | 인덱스만, 타겟 최대 3개 | 인덱스/TOC만 읽기 → 타겟 섹션 최대 3개 선택적 읽기 |

### 코드베이스 크기별 탐색 전략

| 코드베이스 크기 | 전략 | 구체적 방법 |
|----------------|------|-------------|
| < 50 파일 | 자유 탐색 | `Glob` + `Read` 자유롭게 사용 |
| 50-200 파일 | 타겟 탐색 | `rg`/`Glob`으로 후보 식별 → 타겟 `Read` |
| > 200 파일 | 타겟 탐색 | `rg`/`Glob` 위주 → 최소한의 `Read` |

### 판단 기준

```
스펙 파일 크기 판단:
  spec_files = Glob("_sdd/spec/*.md")
  total_lines = sum(각 파일의 줄 수)
  → 위 테이블에 따라 전략 선택

코드베이스 크기 판단:
  소스 파일 수 = Glob("**/*.{py,js,ts,jsx,tsx,go,rs,java}")의 결과 수
  → 위 테이블에 따라 전략 선택
```
