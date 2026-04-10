---
name: guide-create
description: This skill should be used when the user asks to "guide create", "create guide", "feature guide", "write guide", "가이드 작성", "기능 가이드", "가이드 문서 만들어줘", or wants to generate an implementation/review guide document for a specific feature from spec and code context.
version: 2.2.0
---

# Guide Create - Feature Technical Report Generator

글로벌 스펙이 프로젝트 전체의 SSOT 화이트페이퍼라면, 기능 가이드는 **단일 기능에 대한 deep-dive 기술 보고서**다. **시나리오별 사용 가이드**와 **API 레퍼런스**를 구체적이고 자세하게 작성하는 데 특화한다.

| | 글로벌 스펙 | 기능 가이드 |
|---|---|---|
| 범위 | 프로젝트 전체 | 단일 기능 deep-dive |
| 성격 | SSOT 화이트페이퍼 | 기능별 기술 보고서 |
| 강점 | 설계 서사 + 전체 구조 | **시나리오 가이드 + API 상세** |
| 독자 | 설계 이해 | 구현자 / 사용자 / 리뷰어 |

## Acceptance Criteria
> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: `_sdd/guides/<YYYY-MM-DD>_guide_<slug>.md` 파일이 생성되었다
- [ ] AC2: §1-§5 required sections가 모두 포함되어 있다
- [ ] AC3: 메타데이터에 신뢰도(High/Medium/Low)가 표시되어 있다
- [ ] AC4: `_sdd/spec/`, 애플리케이션 코드, 설정 파일, 테스트를 수정하지 않았다

## Hard Rules

1. **Spec/code read-only**: `_sdd/spec/`, 애플리케이션 코드, 설정, 테스트 수정 금지.
2. **Allowed outputs**: `_sdd/guides/<YYYY-MM-DD>_guide_<slug>.md`만 생성.
3. **Non-interactive**: 추론 가능하면 묻지 않는다. 확인 불가 시 가정을 명시한다.
4. **Spec-first**: `_sdd/spec/`이 primary source. 코드는 구현 디테일 보완용.
5. **Per-feature output**: 복수 기능 → 기능당 1 파일.
6. **Language rule**: 기존 스펙/문서의 언어를 따른다. 사용자 명시 지정 시 해당 언어. 새 프로젝트는 한국어 기본.

## Process

### Step 1: Identify the Target Feature

**Tools**: `Read`, `Glob`, `Grep`, `Bash (read-only)`

1. 사용자 요청에서 대상 기능 후보 파악.
2. 복수 기능 → 기능당 1 출력 파일 계획.
3. 출력 파일명을 English slug로 정규화: `<YYYY-MM-DD>_guide_<slug>.md`.
4. 출력 언어 결정.

### Step 2: Locate and Validate Spec Context

**Tools**: `Read`, `Glob`, `Grep`

1. `_sdd/spec/`에서 메인 스펙 탐색. 분할 스펙이면 관련 서브스펙 추적.
2. 기능 설명, 제약, AC 등 핵심 컨텍스트 추출.
3. 스펙 없음 → `AskUserQuestion`으로 선택지 제공 (spec-create 실행 / Low 신뢰도로 계속).

> **Decision Gate 2->3**: `references/tool-and-gates.md` § Gate 2->3: Spec Grounding 참조.

### Step 3: Gather Code Evidence

**Tools**: `Grep`, `Glob`, `Read`, `Bash (read-only)`

1. 관련 구현 파일, 테스트, 인터페이스, 스키마 탐색.
2. 핵심 증거 수집: file paths, function/class/type names, test cases.
3. **Citation index 작성**: `[filepath:symbol]` 형식 목록 → Step 5에서 §2-§5 인라인 citation으로 사용.
4. 구현 상태 구분: confirmed / partially implemented / spec-only.

### Step 3.5: Generation Strategy Decision

관련 소스 파일 수(테스트/설정 제외)에 따라 전략 결정:

| 조건 | 전략 |
|------|------|
| `related_files < 10` | 1-페이즈: Step 5에서 단일 패스 작성 |
| `related_files >= 10` | 2-페이즈: 골조 생성 -> 내용 채우기 |

### Step 4: Resolve Gaps with Deterministic Defaults

누락 정보는 보수적으로 채운다:

| 누락 항목 | 기본값 전략 |
|-----------|-------------|
| Feature name | 스펙 제목 또는 사용자 표현에서 추출 |
| User value | 스펙 goal/problem statement 요약 |
| Implementation rule | 코드베이스 기존 컨벤션 우선 |
| Example | 스펙 기반 positive example + 가정 표기 |
| Reference | 확인 가능한 파일/섹션 + 미확인 심볼 표기 |

확인되지 않은 동작을 확정적으로 기술하지 않는다.

### Step 5: Generate the Technical Report

**Tools**: `Write`, `Edit`, `Agent` (2-페이즈 시)

> 1-페이즈: required sections 구조로 단일 패스 작성.
> 2-페이즈: 골조 생성 후 내용 채우기, 동일 구조로 저장.

#### 파일 작성 위임

현재 콘텍스트에서 먼저 guide skeleton/섹션 헤더를 기록한 뒤, 같은 흐름에서 Edit으로 내용을 채운다.
- 독립 섹션 2개+ → 병렬 Agent dispatch 가능
- 의존 섹션 → 순서대로 Edit
- 완료 후 TODO/Phase 마커 제거

호출 시 Required sections 전체와 맥락(스펙, 코드 증거, Step 2-3 분석)을 포함. `references/template-compact.md`의 Writing Rules와 §1-§5 구조 준수.

- **단일 기능**: Agent 1회 호출로 `<YYYY-MM-DD>_guide_<slug>.md` 작성.
- **복수 기능** (Hard Rule #5): 기능별 Agent 병렬 디스패치.

#### Required Sections

`references/output-format.md`의 구조를 따른다.

- **§1 배경 및 동기**: 해결 문제, 접근 이유, 대안 대비 선택 이유
- **§2 핵심 설계**: 핵심 아이디어/알고리즘, 설계 결정, 인라인 citation, 코드 발췌
- **§3 사용 시나리오 가이드** (특화): 시나리오별 end-to-end 흐름 (전제->입력->처리->결과), 정상+예외, 인라인 citation
- **§4 API 레퍼런스** (특화): 엔드포인트/함수 상세, 파라미터, 리턴값, 에러 코드, 코드 예시, 인라인 citation
- **§5 구현 가이드**: 핵심 규칙/제약, 체크리스트, 안티패턴, 인라인 citation

Optional appendix: spec references, code references, assumptions/open points

#### Inline Citation Rules

- **Code Excerpts**: 코드 블록 첫 줄에 `# [filepath:functionName]` 헤더. <=30줄 전문, >30줄 시그니처+핵심.
- **Inline Citations**: 본문에서 `[filepath:functionName]` 형식. §2-§5 전체에서 코드 근거가 있으면 반드시 사용.
- **Low 신뢰도**: citation 대신 "코드 미확인" 표기.

### Step 6: Save

**Tools**: `Bash (mkdir -p)`, `Write`

1. `_sdd/guides/` 존재 확인 (mkdir -p).
2. `<YYYY-MM-DD>_guide_<slug>.md` 작성. `slug`는 소문자 snake_case (영문 소문자, 숫자, `_`만 사용).
3. 생성 경로를 사용자에게 보고.

## Output Format

- **File**: `_sdd/guides/<YYYY-MM-DD>_guide_<slug>.md`
- **Schema**: `references/output-format.md` 참조

```markdown
# 기능 기술 보고서: <feature>

**Version**: X.Y.Z
**Status**: Draft | In Review | Approved | Deprecated
**생성일**: YYYY-MM-DD
**입력 소스**: [conversation/spec/code]
**대상 기능**: <feature>
**신뢰도**: High/Medium/Low

## §1 배경 및 동기
## §2 핵심 설계
## §3 사용 시나리오 가이드
## §4 API 레퍼런스
## §5 구현 가이드
## 부록 (선택)
```

## Error Handling

| Situation | Response |
|----------|----------|
| `_sdd/spec/` 또는 메인 스펙 없음 | `AskUserQuestion`으로 선택지 제공 (spec-create / Low 신뢰도 계속) |
| Feature 모호 | 스펙에서 가장 명확한 표현 사용 + 가정 기록 |
| 코드 증거 없음 | 스펙 기반 보고서 생성, 코드 참조 unavailable 표기 |
| 복수 기능 요청 | 기능별 별도 가이드 파일 생성 |
| 기존 가이드 파일 존재 | 날짜+slug로 구분되므로 별도 처리 불필요 |
| 언어 혼재 | 기존 스펙/문서 언어 따름. 사용자 지정 시 해당 언어. 새 프로젝트는 한국어. |

## References

- `references/template-compact.md` -- Writing Rules + §1-§5 구조
- `references/output-format.md` -- 필수 구조 및 표기 규칙
- `references/tool-and-gates.md` -- 도구 매핑, 의사결정 게이트
- `examples/` -- 신뢰도별 샘플 (High / Medium / Low)

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
