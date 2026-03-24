---
name: spec-upgrade
description: This skill should be used when the user asks to "upgrade spec", "convert spec to whitepaper", "migrate spec format", "spec upgrade", "스펙 업그레이드", "스펙 변환", "스펙 마이그레이션", "whitepaper 형식으로 변환", or wants to convert old-format spec documents to the whitepaper-style §1-§8 structure defined in SDD_SPEC_DEFINITION.md.
version: 1.3.0
---

# Spec Upgrade - 구 형식 스펙을 Whitepaper 형식으로 변환

| Workflow | Position | When |
|----------|----------|------|
| Migration | Standalone | 기존 스펙이 whitepaper §1-§8 구조가 아닐 때 |
| Any | Pre-step | spec-rewrite/spec-review 전 구조 변환이 필요할 때 |

구 형식 스펙 문서를 SDD whitepaper 형식(§1-§8)으로 변환한다. 기존 내용을 보존하면서 빠진 서사 섹션(배경/동기, 핵심 설계, 사용 가이드)을 코드 분석 기반으로 보충하고, 전체 코드 citation을 매핑한다.

## Acceptance Criteria
> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: §1-§8 필수 섹션이 모두 존재하며 서사 섹션(§1, §2, §5)에 실질적 내용이 있다
- [ ] AC2: 코드 citation `[filepath:functionName]`이 주요 함수/클래스에 삽입되어 있다
- [ ] AC3: 백업 파일 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`가 존재한다
- [ ] AC4: 기존 스펙 내용이 삭제 없이 §1-§8에 재배치되었다
- [ ] AC5: Appendix: Code Reference Index에 모든 인라인 citation이 정리되어 있다
- [ ] AC6: 인라인 citation의 filepath가 실제 파일로 존재한다
- [ ] AC7: CLAUDE.md, AGENTS.md가 존재한다 (미존재 시 생성)

## Hard Rules

1. **코드 파일 수정 금지**: `src/`, `tests/` 등 구현 코드 파일은 수정하지 않는다.
2. **언어 규칙**: 기존 스펙의 언어를 따른다. 한국어 스펙이면 한국어로, 영어 스펙이면 영어로 업그레이드한다.
3. **기존 내용 보존**: 구 형식 스펙의 기존 내용은 최대한 보존한다. 삭제하지 않고 §1-§8에 재배치한다.
4. **백업 필수**: 변환 전 반드시 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
5. **Checkpoint 필수**: Step 3에서 Gap 분석 결과와 업그레이드 계획을 먼저 보고한다. 대상 파일이나 구조가 모호할 때만 사용자 확인을 요청한다.
6. **DECISION_LOG.md 보존**: 기존 DECISION_LOG.md가 있으면 보존한다. 업그레이드 과정의 주요 결정도 추가 기록한다.
7. **In-place 덮어쓰기**: 업그레이드 결과는 기존 파일 경로에 덮어쓴다 (백업 후).

## Process

### Step 1: Gap Analysis (기존 스펙 진단)

**Tools**: `Read`, `Glob`, `Grep`

1. `Glob("_sdd/spec/**/*.md")`로 스펙 파일 식별, 멀티파일 여부 확인
2. **`references/spec-format.md`를 Read**하여 whitepaper §1-§8 구조 확인
3. 각 섹션의 존재/품질 진단:

| # | Section | 진단 기준 |
|---|---------|----------|
| §1 | Background & Motivation | Problem statement, why, value proposition |
| §2 | Core Design | Key idea narrative, algorithm flow, design rationale |
| §3 | Architecture Overview | System diagram, tech stack, design decisions |
| §4 | Component Details | Per-component purpose/why/source |
| §5 | Usage Guide & Expected Results | Scenario-based usage with outcomes |
| §6 | Data Models | Entity definitions (해당 시) |
| §7 | API Reference | Endpoints/schemas (해당 시) |
| §8 | Environment & Dependencies | Directory structure, deps, config |
| - | Code Reference Index | Inline citations 존재 여부 |

4. 이미 whitepaper 형식이면 부족한 항목만 보강 대상으로 표시

**Gate 1→2**: `spec_found AND gap_identified AND targets_resolved → Step 2`. 스펙 미존재 시 "spec-create를 먼저 실행하세요" 출력 후 종료.

### Step 2: Code Analysis (코드베이스 분석)

**Tools**: `Agent` (Explore), `Read`, `Glob`, `Grep`

1. `Glob("**/*.{py,ts,js,java,go,rs,tsx,jsx}")`로 구현 파일 확인 (미존재 → 스킵)
2. 빠진 섹션에 따라 코드 분석:

| 빠진 섹션 | 수집 대상 |
|-----------|----------|
| §1 배경/동기 | README, docs, 커밋 히스토리, 프로젝트 구조 |
| §2 핵심 설계 | 핵심 알고리즘, 메인 로직 흐름, 진입점 |
| §5 사용 가이드 | CLI 인터페이스, API 엔드포인트, 테스트 시나리오 |
| Code citation | 모든 주요 파일/클래스/함수 매핑 |

3. 멀티파일 스펙이면 서브 파일 내용을 읽고 §1-§8 매핑 위치·중복·통합 순서 결정

**Gate 2→3**: `code_analyzed AND gap_plan_ready → Step 3`

### Step 3: Checkpoint (분석 결과 보고)

**Tools**: — (보고 단계), `AskUserQuestion` (only if risky ambiguity remains)

Gap 분석 결과를 아래 형식으로 보고 후 자동 진행:

```markdown
## 스펙 업그레이드 분석 결과

### 기존 스펙 현황
| 파일 | 줄 수 | 주요 섹션 |
|------|-------|----------|

### §1-§8 Gap 분석
| # | Section | 현재 상태 | 조치 |
|---|---------|----------|------|
| §1-§8 | ... | ❌/⚠️/✅ | 신규/보강/유지 |

### 보충 방향
- §1/§2/§5: [요약], Citation: [매핑 대상 N개]
```

사용자 확인이 필요한 경우: canonical spec 후보 2+개, split spec 구조 불명, 구조 재편이 더 적절(`spec-rewrite` 전환 여부).

**Gate 3→4**: `report_presented AND ambiguity_resolved → Step 4`

### Step 4: Backup & Upgrade (백업 및 업그레이드 실행)

**Tools**: `Read`, `Write`, `Bash` (mkdir, cp)

#### 4.1 백업 생성

```
1. mkdir -p _sdd/spec/prev/
2. 각 스펙 파일을 prev/PREV_<filename>_<YYYYMMDD_HHMMSS>.md로 복사
```

#### 4.2 멀티파일 업그레이드 (해당 시)

**멀티파일 구조 규칙:**

1. **main.md = 인덱스 + 공통 섹션**: §1 Background, §2 Core Design, §3 Architecture는 main.md에 인라인. §4 이하 컴포넌트는 링크로 분리.
2. **컴포넌트 파일명 = 컴포넌트명**: `auth.md`, `scheduler.md` 등 접두사 없이 직관적으로 명명.
3. **main.md 링크 형식**: §4 영역에 `See [Component Name](./component.md)` 형태로 링크. 모든 sub-spec 파일은 main.md에서 링크되어야 함.
4. **Cross-cutting 섹션**: §7 API, §8 Config 등 여러 컴포넌트에 걸치는 내용은 main.md에 유지하거나 별도 `api.md`, `config.md`로 분리 (규모에 따라 판단).

추가 규칙:
- 기존 서브 파일 삭제 금지. 구조 재편 필요 시 `spec-rewrite` 후보로 보고
- 공통 서사(§1,§2,§3,§5,§8)는 main.md에 보강, 컴포넌트 상세(§4,§6,§7)는 서브 파일에 유지

#### 파일 작성 위임

`sdd-skills:write-skeleton` 서브에이전트에 위임한다. 반환값이 SKELETON_ONLY이면 Sections Remaining 목록을 보고 Edit으로 채운다.
- 독립 섹션 2개+ → 병렬 Agent dispatch 가능
- 의존 섹션 → 순서대로 Edit
- 완료 후 TODO/Phase 마커 제거

Step 4.3 변환 규칙 + Gap/코드 분석 결과 + 기존 스펙 내용을 프롬프트에 포함.

- **단일 파일**: `Agent(subagent_type="sdd-skills:write-skeleton", prompt="[target path] + 변환 규칙 + 분석 결과")`
- **멀티파일**: main.md 먼저(§1,§2,§3,§5,§8) → 서브 파일 병렬(§4 보강). 독립 서브 파일 2개 이상이면 병렬 디스패치.

#### 4.3 Whitepaper 구조 변환

> **순서대로 Read**: `references/template-compact.md` → `references/template-full.md` → `references/upgrade-mapping.md`

| 단계 | 작업 |
|------|------|
| 1. 재배치 | upgrade-mapping.md 규칙에 따라 기존 내용을 §1-§8에 재배치 (삭제 금지) |
| 2. 서사 생성 | §1 배경/동기, §2 핵심 설계, §5 사용 가이드를 코드 분석 기반으로 작성 |
| 3. Citation | `[filepath:functionName]` 인라인 citation 삽입. 30줄 이하 전체 발췌, 초과 시 시그니처+핵심만. 코드 블록에 `# [filepath:fn]` 헤더. §4 Source 필드 보강 |
| 4. Index | Appendix: Code Reference Index — 모든 인라인 citation을 파일별 테이블로 정리 |
| 5. 메타 | Version, Last Updated, Status, ToC 갱신 |

#### 4.4 DECISION_LOG.md 업데이트

```markdown
## YYYY-MM-DD - Spec Upgrade to Whitepaper Format
- Context: 구 형식 스펙을 whitepaper §1-§8 구조로 변환
- Decision: [통합/재배치/신규 생성 사항]
- Rationale: SDD_SPEC_DEFINITION.md 기준 whitepaper 형식 준수
- Changes: [변경된 파일 목록]
```

#### 4.5 Workspace Guidance 파일 보충

구 버전 SDD에서는 CLAUDE.md, AGENTS.md가 없을 수 있다. 미존재 시 생성:

1. `AGENTS.md` 미존재 → 생성:
   ```markdown
   # Workspace Guidance
   - 프로젝트 스펙 문서는 `_sdd/spec/`를 기준으로 확인합니다. 프로젝트 내 기능이나 구현을 확인하고 수정할 때는 관련된 스펙 문서를 함께 읽고 참조합니다.
   - 환경 관련 설정/실행 방법은 `_sdd/env.md`를 기준으로 확인합니다. 의존성 설치, 테스트 스크립트 실행 등의 작업 시 이 파일을 참조합니다.
   ```
2. `CLAUDE.md` 미존재 → 동일 문구로 생성
3. 이미 존재하면 스킵

### Step 5: Validation & Completion (검증 및 완료)

**Tools**: `Glob`, `Read`

#### 5.1 구조 검증

- 단일 파일: §1-§5, §8 필수 섹션 존재 확인
- Split spec: top-level에 §1,§2,§3,§5,§8 + 링크, 서브에 §4 상세 확인
- 선택: §6, §7, Appendix: Code Reference Index (해당 시)

#### 5.2 Citation 검증

인라인 citation `[filepath:functionName]` 추출 → 각 filepath를 `Glob`으로 실존 확인 → 무효 목록 보고

#### 5.3 백업 검증

`Glob("_sdd/spec/prev/PREV_*.md")` → 백업 파일 존재 확인

#### 5.4 완료 보고

| 항목 | 내용 |
|------|------|
| 업그레이드 파일 | `<target path(s)>` |
| 백업 파일 | `_sdd/spec/prev/PREV_<name>_<ts>.md` |
| 변환 전/후 줄 수 | N줄 → N줄 |
| 신규/보강 섹션 | §1, §2, §5 등 |
| 코드 citation | N개 |
| 검증 결과 | 통과/이슈 N건 |

후속: spec-rewrite(정리/분할), spec-review(품질 검증), spec-update-done(코드-스펙 동기화)

## Error Handling

| 상황 | 대응 |
|------|------|
| 스펙 파일 미존재 | "spec-create를 먼저 실행하세요" 후 종료 |
| 이미 whitepaper 형식 | 부족한 항목만 보강 |
| 코드베이스 미존재 | 코드 분석 스킵, 기존 스펙 기반 서사 작성 |
| 멀티파일 통합 실패 | 개별 파일 상태 보고, 수동 통합 안내 |
| canonical spec 모호 | 최소 확인 후 진행 |
| 코드 citation 경로 무효 | 무효 목록 보고, TODO 마커 삽입 |
| DECISION_LOG.md 충돌 | 기존 보존, 새 항목만 추가 |
| 백업 디렉토리 생성 실패 | 오류 보고, 업그레이드 중단 |

## Additional Resources

- **`references/template-compact.md`** — §1-§8 generation template (What/Why/How triad, Modular Spec Guide)
- **`references/spec-format.md`** — Whitepaper §1-§8 구조 및 보존 규칙
- **`references/template-full.md`** — 전체 스펙 템플릿 (citation 형식 상세 예시)
- **`references/upgrade-mapping.md`** — 구 형식 → whitepaper 섹션 매핑 가이드
- **`examples/before-upgrade.md`** / **`examples/after-upgrade.md`** — 업그레이드 전후 예시

후속 스킬: spec-create(스펙 신규), spec-rewrite(정리/분할), spec-review(품질 검증), spec-update-done(코드-스펙 동기화)

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

