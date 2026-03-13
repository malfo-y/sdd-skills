---
name: spec-upgrade
description: This skill should be used when the user asks to "upgrade spec", "convert spec to whitepaper", "migrate spec format", "spec upgrade", "스펙 업그레이드", "스펙 변환", "스펙 마이그레이션", "whitepaper 형식으로 변환", or wants to convert old-format spec documents to the whitepaper-style §1-§8 structure defined in SDD_SPEC_DEFINITION.md.
version: 1.0.0
---

# Spec Upgrade - 구 형식 스펙을 Whitepaper 형식으로 변환

| Workflow | Position | When |
|----------|----------|------|
| Migration | Standalone | 기존 스펙이 whitepaper §1-§8 구조가 아닐 때 |
| Any | Pre-step | spec-rewrite/spec-review 전 구조 변환이 필요할 때 |

구 형식 스펙 문서를 SDD whitepaper 형식(§1-§8)으로 변환한다. 기존 내용을 보존하면서 빠진 서사 섹션(배경/동기, 핵심 설계, 사용 가이드)을 코드 분석 기반으로 보충하고, 전체 코드 citation을 매핑한다.

## When to Use This Skill

- 기존 스펙이 whitepaper §1-§8 구조가 아닐 때
- 배경/동기(§1), 핵심 설계 서사(§2), 사용 가이드(§5) 등 서사 섹션이 빠진 스펙
- 코드 citation (`[filepath:functionName]`) 이 없는 스펙
- `SDD_SPEC_DEFINITION.md` 제정 이전에 만든 레거시 스펙

## Hard Rules

1. **코드 파일 수정 금지**: `src/`, `tests/` 등 구현 코드 파일은 수정하지 않는다.
2. **언어 규칙**: 기존 스펙의 언어를 따른다. 한국어 스펙이면 한국어로, 영어 스펙이면 영어로 업그레이드한다.
3. **기존 내용 보존**: 구 형식 스펙의 기존 내용은 최대한 보존한다. 삭제하지 않고 §1-§8에 재배치한다.
4. **백업 필수**: 변환 전 반드시 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
5. **Checkpoint 필수**: Step 3에서 Gap 분석 결과와 보충 방향을 사용자에게 반드시 확인받는다.
6. **DECISION_LOG.md 보존**: 기존 DECISION_LOG.md가 있으면 보존한다. 업그레이드 과정의 주요 결정도 추가 기록한다.
7. **In-place 덮어쓰기**: 업그레이드 결과는 기존 파일 경로에 덮어쓴다 (백업 후).

## Process

### Step 1: Gap Analysis (기존 스펙 진단)

**Tools**: `Read`, `Glob`, `Grep`

기존 스펙을 읽고 whitepaper §1-§8 대비 gap을 분석한다.

#### 1.1 스펙 파일 탐색

```
1. Glob("_sdd/spec/**/*.md")로 모든 스펙 파일 식별
2. 멀티파일 여부 확인 (main.md + 서브 파일 구조인지)
3. 각 파일의 섹션 구조를 파악
```

#### 1.2 §1-§8 매핑 분석

> **먼저 `references/spec-format.md`를 Read로 읽는다.** 이 파일에 whitepaper §1-§8 구조와 보존 규칙이 정의되어 있다.

각 섹션의 존재 여부와 품질을 진단:

| # | Section | 진단 기준 |
|---|---------|----------|
| §1 | Background & Motivation | Problem statement, why this approach, core value proposition 존재 여부 |
| §2 | Core Design | Key idea narrative, algorithm/logic flow, design rationale 존재 여부 |
| §3 | Architecture Overview | System diagram, tech stack, design decisions 존재 여부 |
| §4 | Component Details | Per-component purpose/why/source 구조 여부 |
| §5 | Usage Guide & Expected Results | Scenario-based usage with expected outcomes 존재 여부 |
| §6 | Data Models | Entity definitions (해당 시) |
| §7 | API Reference | Endpoints/schemas (해당 시) |
| §8 | Environment & Dependencies | Directory structure, deps, config 존재 여부 |
| - | Code Reference Index | Inline citations 존재 여부 |

#### 1.3 이미 Whitepaper 형식 감지

§1-§8 필수 섹션이 모두 존재하고 서사 섹션(§1, §2, §5)이 충분한 내용을 가지면:

```
텍스트 출력: "이 스펙은 이미 whitepaper 형식에 가깝습니다."

AskUserQuestion:
  "이미 whitepaper 형식에 가까운 스펙입니다. 계속 업그레이드를 진행할까요?"
  옵션:
  1. "계속 진행" - 부족한 부분 보강
  2. "중단" - 업그레이드 불필요
  3. "spec-review로 전환" - 품질 검증만 수행
```

**Decision Gate 1→2**:
```
spec_found = 스펙 파일이 1개 이상 존재
gap_identified = §1-§8 대비 빠진 섹션 또는 부족한 섹션 식별 완료
user_confirmed = 이미 whitepaper 형식인 경우 사용자가 "계속 진행" 선택

IF spec_found AND gap_identified AND (NOT already_whitepaper OR user_confirmed) → Step 2
IF NOT spec_found → "스펙 파일이 없습니다. spec-create를 먼저 실행하세요." 출력 후 종료
```

### Step 2: Code Analysis (코드베이스 분석)

**Tools**: `Agent` (Explore), `Read`, `Glob`, `Grep`

빠진 섹션을 채우기 위한 코드베이스 분석을 수행한다.

#### 2.1 코드베이스 존재 확인

```
Glob("**/*.{py,ts,js,java,go,rs,tsx,jsx}")로 구현 파일 확인
- 존재 → 코드 분석 진행
- 미존재 → 코드 분석 스킵, 사용자 입력 기반으로 진행
```

#### 2.2 Gap별 코드 분석

빠진 섹션에 따라 필요한 정보를 수집:

| 빠진 섹션 | 수집 대상 | Sub-agent |
|-----------|----------|-----------|
| §1 배경/동기 | README, CLAUDE.md, 커밋 히스토리, 프로젝트 구조 | Explore |
| §2 핵심 설계 | 핵심 알고리즘, 메인 로직 흐름, 진입점 | Explore |
| §5 사용 가이드 | CLI 인터페이스, API 엔드포인트, 테스트 시나리오 | Explore |
| Code citation | 모든 주요 파일/클래스/함수 매핑 | Explore |

```
Agent(
  subagent_type="Explore",
  prompt="다음 프로젝트의 코드베이스를 분석하세요: [프로젝트 경로]

  수집 대상:
  1. 프로젝트의 핵심 목적과 해결하는 문제 (README, docs 기반)
  2. 핵심 알고리즘/로직 흐름 (진입점부터 주요 처리 경로)
  3. 주요 파일/클래스/함수 목록 (코드 citation용)
  4. 사용 방법과 주요 시나리오 (CLI, API, 테스트 기반)
  5. 기술 스택과 의존성

  각 항목을 구조화된 형태로 보고하세요."
)
```

#### 2.3 멀티파일 통합 준비

멀티파일 스펙인 경우:
```
1. 모든 서브 파일의 내용을 읽기
2. 섹션별로 §1-§8에 매핑할 위치 결정
3. 중복 내용 식별
4. 통합 순서 결정
```

**Decision Gate 2→3**:
```
code_analyzed = 코드베이스 분석 완료 (또는 코드 없음 확인)
gap_fillable = 빠진 섹션을 채울 자료가 최소 1개 수집됨

IF code_analyzed AND gap_fillable → Step 3
IF code_analyzed AND NOT gap_fillable → 사용자에게 부족한 정보 요청 후 Step 3
```

### Step 3: Checkpoint (사용자 확인)

**Tools**: `AskUserQuestion`

Gap 분석 결과와 보충 방향을 사용자에게 제시하고 승인을 받는다.

#### 3.1 Gap 분석 결과 테이블 출력

텍스트로 다음 테이블을 출력:

```markdown
## 스펙 업그레이드 분석 결과

### 기존 스펙 현황
| 파일 | 줄 수 | 주요 섹션 |
|------|-------|----------|
| main.md | N줄 | ... |
| (서브파일) | N줄 | ... |

### §1-§8 Gap 분석
| # | Section | 현재 상태 | 조치 |
|---|---------|----------|------|
| §1 | Background & Motivation | ❌ 없음 / ⚠️ 부족 / ✅ 존재 | 신규 생성 / 보강 / 유지 |
| §2 | Core Design | ... | ... |
| §3 | Architecture Overview | ... | ... |
| §4 | Component Details | ... | ... |
| §5 | Usage Guide & Expected Results | ... | ... |
| §6 | Data Models | ... | ... |
| §7 | API Reference | ... | ... |
| §8 | Environment & Dependencies | ... | ... |
| - | Code Reference Index | ... | ... |

### 보충 방향
- §1: [코드/README에서 추출한 프로젝트 목적 요약]
- §2: [핵심 로직 흐름 요약]
- §5: [사용 시나리오 요약]
- Citation: [매핑 대상 파일 N개]
```

#### 3.2 사용자 승인

```
AskUserQuestion:
  "분석 결과를 확인해 주세요. 업그레이드를 진행할까요?"
  옵션:
  1. "확인, 진행" - 제시된 방향으로 업그레이드
  2. "수정 필요" - 피드백 후 방향 조정
  3. "중단" - 업그레이드 취소
```

수정 피드백 시 최대 2라운드 조정 후 진행.

**Decision Gate 3→4**:
```
user_approved = 사용자가 "확인, 진행" 선택
feedback_resolved = 수정 피드백이 있었다면 반영 완료

IF user_approved OR feedback_resolved → Step 4
IF 사용자가 "중단" 선택 → 종료
```

### Step 4: Backup & Upgrade (백업 및 업그레이드 실행)

**Tools**: `Read`, `Write`, `Bash` (mkdir, cp)

#### 4.1 백업 생성

```
1. mkdir -p _sdd/spec/prev/
2. 각 스펙 파일을 prev/PREV_<filename>_<YYYYMMDD_HHMMSS>.md로 복사
```

#### 4.2 멀티파일 통합 (해당 시)

멀티파일 스펙인 경우:
```
1. 모든 서브 파일 내용을 §1-§8 순서로 통합
2. 중복 내용 제거
3. 상호 참조 링크를 인라인으로 변환
4. 통합 결과를 main.md로 저장
5. 기존 서브 파일은 백업에만 보존 (삭제)
```

#### 4.3 Whitepaper 구조 변환

> **먼저 `references/template-full.md`를 Read로 읽는다.** 이 템플릿에 전체 섹션 구조와 코드 citation 형식이 정의되어 있다.
> **그다음 `references/upgrade-mapping.md`를 Read로 읽는다.** 이 파일에 구 형식 → whitepaper 섹션 매핑 규칙이 정의되어 있다.

변환 순서:

```
1. 기존 내용을 §1-§8에 재배치
   - upgrade-mapping.md의 매핑 규칙에 따라 기존 섹션을 적절한 위치로 이동
   - 기존 내용은 삭제하지 않고 재배치

2. 빠진 서사 섹션 생성 (코드 분석 결과 기반)
   - §1 Background & Motivation: 문제, 동기, 핵심 가치
   - §2 Core Design: 핵심 아이디어 서사, 알고리즘/로직 흐름, 설계 근거
   - §5 Usage Guide & Expected Results: 시나리오 기반 사용법과 기대 결과

3. 코드 citation 삽입
   - 핵심 함수/클래스에 [filepath:functionName] 인라인 citation 추가
   - 30줄 이하 핵심 코드는 전체 발췌, 초과 시 시그니처 + 핵심 로직만
   - 코드 블록에 # [filepath:functionName] 헤더 추가
   - Component Details의 Source 필드 추가/보강

4. Appendix: Code Reference Index 생성
   - 모든 인라인 citation을 파일별로 정리한 테이블

5. 메타데이터 업데이트
   - Version, Last Updated, Status 필드 갱신
   - Table of Contents 업데이트
```

#### 4.4 DECISION_LOG.md 업데이트

업그레이드 과정의 주요 결정을 기록:
```markdown
## YYYY-MM-DD - Spec Upgrade to Whitepaper Format
- Context: 구 형식 스펙을 whitepaper §1-§8 구조로 변환
- Decision: [통합/재배치/신규 생성 사항]
- Rationale: SDD_SPEC_DEFINITION.md 기준 whitepaper 형식 준수
- Changes: [변경된 파일 목록]
```

### Step 5: Validation & Completion (검증 및 완료)

**Tools**: `Glob`, `Read`

#### 5.1 구조 검증

```
1. Glob("_sdd/spec/main.md") → 파일 존재 확인
2. 필수 섹션 포함 확인:
   - §1 Background & Motivation ✅
   - §2 Core Design ✅
   - §3 Architecture Overview ✅
   - §4 Component Details ✅
   - §5 Usage Guide & Expected Results ✅
   - §8 Environment & Dependencies ✅
3. 선택 섹션 확인 (해당 시):
   - §6 Data Models
   - §7 API Reference
   - Appendix: Code Reference Index
```

#### 5.2 Citation 검증

```
1. 인라인 citation [filepath:functionName] 패턴 추출
2. 각 filepath가 실제 존재하는지 Glob으로 확인
3. 유효하지 않은 citation 목록 보고
```

#### 5.3 백업 검증

```
Glob("_sdd/spec/prev/PREV_*.md") → 백업 파일 존재 확인
```

## Progressive Disclosure (완료 시)

```
완료 요약 테이블을 제시한 후 상세 내용을 출력한다:

1. 완료 요약 테이블:
   | 항목 | 내용 |
   |------|------|
   | 업그레이드 파일 | `_sdd/spec/main.md` |
   | 백업 파일 | `_sdd/spec/prev/PREV_<name>_<ts>.md` |
   | 변환 전 줄 수 | N줄 |
   | 변환 후 줄 수 | N줄 |
   | 신규 생성 섹션 | §1, §2, §5 (예시) |
   | 보강 섹션 | §4 Source 필드 (예시) |
   | 코드 citation | N개 |
   | 검증 결과 | 통과/이슈 N건 |

2. 섹션별 변경 요약 출력

3. 후속 스킬 안내:
   - 스펙 정리/분할이 필요하면 → spec-rewrite
   - 스펙 품질 검증이 필요하면 → spec-review
   - 코드와 스펙 동기화가 필요하면 → spec-update-done
```

## Context Management

### 스펙 크기별 전략

| 스펙 크기 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 200줄 | 전체 읽기 | `Read`로 전체 파일 읽기 |
| 200-500줄 | 전체 읽기 가능 | `Read`로 전체 읽기, 필요 시 섹션별 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 | 상위 50줄(TOC) 읽기 → 관련 섹션만 `Read(offset, limit)` |
| > 1000줄 | 인덱스만, 타겟 최대 3개 | 인덱스/TOC만 읽기 → 타겟 섹션 최대 3개 선택적 읽기 |

### 코드베이스 크기별 전략

| 코드베이스 크기 | 전략 | 구체적 방법 |
|----------------|------|-------------|
| < 50 파일 | 자유 탐색 | `Glob` + `Read` 자유롭게 사용 |
| 50-200 파일 | 타겟 탐색 | `Grep`/`Glob`으로 후보 식별 → 타겟 `Read` |
| > 200 파일 | Explore agent | Sub-agent로 탐색 위임, 핵심만 보고 |

## Error Handling

| 상황 | 대응 |
|------|------|
| 스펙 파일 미존재 | "스펙 파일이 없습니다. spec-create를 먼저 실행하세요." 출력 후 종료 |
| 이미 whitepaper 형식 | 경고 + AskUserQuestion으로 계속/중단/spec-review 전환 선택 |
| 코드베이스 미존재 | 코드 분석 스킵, 사용자 입력 기반으로 서사 섹션 작성 |
| 멀티파일 통합 실패 | 개별 파일 상태 보고, 수동 통합 안내 |
| 사용자 Checkpoint 중단 | 분석 결과까지만 보존, 스펙 파일 미변경 |
| 코드 citation 경로 무효 | 무효 경로 목록 보고, 스펙에 TODO 마커 삽입 |
| 대형 스펙 (1000줄+) | 타겟 섹션만 읽기, Explore agent 활용 |
| DECISION_LOG.md 충돌 | 기존 항목 보존, 새 항목만 추가 |
| 백업 디렉토리 생성 실패 | 오류 보고, 업그레이드 중단 |

## Additional Resources

### Reference Files
- **`references/spec-format.md`** - Whitepaper §1-§8 구조 및 보존 규칙
- **`references/template-full.md`** - 전체 스펙 템플릿 (섹션 구조, citation 형식)
- **`references/upgrade-mapping.md`** - 구 형식 → whitepaper 섹션 매핑 가이드

### Example Files
- **`examples/before-upgrade.md`** - 업그레이드 전 구 형식 스펙 예시
- **`examples/after-upgrade.md`** - 업그레이드 후 whitepaper 형식 스펙 예시

## Integration with Other Skills

이 스킬은 migration 전용이며, 다른 SDD 스킬과 독립적으로 동작한다:

- **spec-create**: 스펙이 아예 없을 때 → spec-create 먼저 실행
- **spec-rewrite**: 업그레이드 후 스펙이 길어졌을 때 → spec-rewrite로 정리/분할
- **spec-review**: 업그레이드 결과의 품질 검증 → spec-review로 확인
- **spec-update-done**: 코드와 스펙 동기화 → spec-update-done으로 보정
