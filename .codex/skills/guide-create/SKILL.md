---
name: guide-create
description: This skill should be used when the user asks to "guide create", "create guide", "feature guide", "write guide", "가이드 작성", "기능 가이드", "가이드 문서 만들어줘", or wants to generate an implementation/review guide document for a specific feature from spec and code context.
version: 2.2.0
---

# Guide Create - Feature Technical Report Generator

| Workflow | Position | When |
|----------|----------|------|
| Any | Standalone | 기능별 기술 보고서 생성 |
| Any | Post-spec-create | 스펙 작성 후 구현 착수 전 기능 deep-dive 정리 |

## Overview

The `guide-create` skill generates a feature-focused **technical report** aligned with the SDD whitepaper philosophy (`docs/SDD_SPEC_DEFINITION.md`).

글로벌 스펙이 프로젝트 전체의 SSOT 화이트페이퍼라면, 기능 가이드는 **단일 기능에 대한 deep-dive 기술 보고서**다. 기능의 배경과 설계 서사를 포함하되, **시나리오별 사용 가이드**와 **API 레퍼런스**를 구체적이고 자세하게 작성하는 데 특화한다.

| | 글로벌 스펙 | 기능 가이드 |
|---|---|---|
| 범위 | 프로젝트 전체 | 단일 기능 deep-dive |
| 성격 | SSOT 화이트페이퍼 | 기능별 기술 보고서 |
| 강점 | 설계 서사 + 전체 구조 | **시나리오 가이드 + API 상세** |
| 독자 | 설계 이해 | 구현자 / 사용자 / 리뷰어 |

- **Target type**: feature only
- **Mode**: non-interactive by default
- **Primary use**: feature deep-dive report with scenario guides and API reference

## Hard Rules

1. **Spec and code are read-only**: Never modify `_sdd/spec/`, application code, configuration files, or tests.
2. **Allowed outputs are limited**: You may create or replace only:
   - `_sdd/guides/guide_<slug>.md`
   - `_sdd/guides/prev/PREV_guide_<slug>_<timestamp>.md`
3. **Feature-only in v1**: Do not create component guides in this version.
4. **Non-interactive by default**: Infer missing details with deterministic defaults. Do not ask follow-up questions unless the user explicitly requests discussion.
5. **Spec-first grounding**: Treat `_sdd/spec/` as the primary source. Use code only to refine implementation detail, naming, file references, and symbol references.
6. **No fake certainty**: If evidence is incomplete, state assumptions or unknowns explicitly in the guide.
7. **Per-feature output**: If multiple features are detected, generate one guide file per feature instead of combining them into a single document.
8. **Backup before overwrite**: If the target guide already exists, create a timestamped backup in `_sdd/guides/prev/` before writing the new file.
9. **Language rule**: 기존 스펙/문서의 언어를 따른다. 사용자 명시 지정 시 해당 언어 사용. 새 프로젝트(기존 스펙 없음)는 한국어 기본.

## When to Use This Skill

- When the user wants a **feature-focused technical report**
- When a feature needs a **deep-dive document** with scenario guides and API reference
- When the user wants a **feature implementation/review guide** with design context
- When a feature exists in spec but needs a detailed usage guide and API documentation
- When a team wants a derived deep-dive without changing the SSOT spec

### Trigger Phrases

Examples of requests that should trigger this skill:

- "guide create"
- "create guide"
- "feature guide"
- "write guide for this feature"
- "가이드 작성"
- "기능 가이드"
- "가이드 문서 만들어줘"
- "이 기능 구현 가이드 써줘"
- "이 스펙 기준으로 리뷰 가이드 정리해줘"

## Input Sources

### Primary Sources

1. **User conversation**
   - feature name
   - target scope
   - explicit constraints
2. **Spec documents**
   - `_sdd/spec/<project>.md`
   - `_sdd/spec/main.md`
   - linked or split sub-specs under `_sdd/spec/`

### Supporting Sources

3. **Relevant code**
   - source files that implement or partially implement the feature
   - tests that reveal intended behavior
   - interfaces, types, or schemas referenced by the feature
4. **Optional execution context**
   - `_sdd/env.md` when command or validation context is relevant

### Exclusions

- Ignore generated or backup documents such as:
  - `_sdd/guides/prev/PREV_*.md`
  - `_sdd/spec/prev/PREV_*.md`
  - `_sdd/spec/SUMMARY.md`

## Process

### Step 1: Identify the Target Feature

**Tools**: `Read`, `Glob`, `Grep`, `Bash (read-only)`

1. Parse the user request and detect target feature candidates.
2. If multiple features are requested, keep all candidates and plan one output file per feature.
3. Normalize each output name to an English slug for `guide_<slug>.md`.
4. Determine the user's active language for the output.

### Step 2: Locate and Validate Spec Context

**Tools**: `Read`, `Glob`, `Grep`

1. Find the main spec in `_sdd/spec/`.
2. If the spec is split, follow linked or convention-based sub-specs relevant to the feature.
3. Extract the most relevant feature description, related sections, constraints, and acceptance-style language.
4. If no usable spec exists:
   - `AskUserQuestion`으로 사용자에게 선택지 제공 (spec-create 실행 / 스펙 없이 Low 신뢰도로 계속)

> **Decision Gate 2→3**: See `references/tool-and-gates.md` § Gate 2→3: Spec Grounding

### Step 3: Gather Code Evidence

**Tools**: `Grep`, `Glob`, `Read`, `Bash (read-only)`

1. Search for related implementation files, tests, interfaces, schemas, and symbols.
2. Capture only evidence that helps make the guide actionable:
   - file paths
   - function/class/component/type names
   - test cases or existing patterns
3. **Build a citation index**: 발견된 핵심 파일/심볼에 대해 `[filepath:symbol]` 형식의 citation 목록을 작성한다. 이 목록은 Step 5에서 §2-§5 전체에 걸쳐 인라인 citation으로 사용된다.
4. Distinguish between:
   - confirmed implementation behavior
   - partially implemented behavior
   - spec-only intended behavior

### Step 3.5: Generation Strategy Decision

**Tools**: — (판단 단계)

Step 3에서 수집한 관련 소스 파일 수에 따라 생성 전략을 결정한다.

```
related_files = Step 3에서 식별한 기능 관련 소스 파일 수 (테스트/설정 파일 제외)

IF related_files < 10 → 1-페이즈 (Step 5에서 단일 패스로 전체 작성)
IF related_files >= 10 → 2-페이즈 (Step 5에서 골조 생성 → 내용 채우기)
```

> **참고**: 기능 가이드는 단일 기능 deep-dive이므로 프로젝트 전체 스펙(spec-create)보다 낮은 임계값(10개)을 사용한다.

### Step 4: Resolve Gaps with Deterministic Defaults

**Tools**: deterministic defaults (non-interactive)

When information is missing, fill gaps conservatively:

- **Feature name unclear**: derive from the most explicit spec heading or user phrase
- **User value unclear**: summarize from the goal/problem statement in spec
- **Implementation rule unclear**: prefer existing codebase conventions over generic best practice
- **Example weak**: create one positive example grounded in the spec and mark assumptions
- **Reference incomplete**: include the best available file/section references and explicitly mark unknown symbols

Never invent confirmed behavior that is unsupported by spec or code.

### Step 5: Generate the Technical Report

**Tools**: `Write`, `Edit`, `Agent` (2-페이즈 병렬 실행 시)

> **1-페이즈** (related_files < 10): 아래 required sections 구조로 단일 패스 작성.
> **2-페이즈** (related_files >= 10): 아래 절차를 먼저 수행한 후, 최종 결과를 동일한 구조로 저장.

#### 2-페이즈 실행 절차 (related_files >= 10일 때만)

> 1-페이즈인 경우 이 절차를 건너뛰고 아래 required sections로 직접 작성한다.

### 파일 작성 위임

출력 문서 작성 시 `write-phased` 서브에이전트에 작업을 위임한다. 서브에이전트 호출 시 아래 Required sections 전체와 작성에 필요한 맥락(스펙 컨텍스트, 코드 증거, Step 2-3 분석 결과 등)을 프롬프트에 포함한다. `references/template-compact.md`의 Writing Rules와 §1-§5 구조를 준수하도록 지시한다.

```
Agent(
  subagent_type="write-phased",
  prompt="다음 문서를 작성해주세요.

  파일 경로: [target guide path - _sdd/guides/guide_<slug>.md]
  참조 템플릿: references/template-compact.md (Writing Rules, § 구조 준수)

  [아래 Required sections(§1-§5)과 Step 2-3에서 수집한 맥락을 여기에 포함]"
)
```

#### Required sections

Write one guide per feature using the required structure from `references/output-format.md`.

Required sections:

- **§1 배경 및 동기 / Background & Motivation**
   - 이 기능이 해결하는 문제
   - 왜 이 접근을 택했는가
   - 대안 대비 선택 이유 (스펙에서 확인 가능한 경우)
- **§2 핵심 설계 / Core Design**
   - 기능의 핵심 아이디어 또는 알고리즘
   - 설계 결정과 그 이유
   - 인라인 citation: 본문에서 `[filepath:symbol]` 형식으로 코드 참조
   - 코드 발췌: `# [filepath:functionName]` 헤더 부착 (≤30줄 전문, >30줄 시그니처+핵심)
- **§3 사용 시나리오 가이드 / Usage Scenario Guide** ★특화
   - 시나리오별 end-to-end 사용 흐름
   - 각 시나리오: 전제 조건 → 입력 → 처리 흐름 → 기대 결과
   - 정상 시나리오 + 예외/에러 시나리오
   - 가능하면 구체적 데이터 예시 포함
   - **인라인 citation**: 처리 흐름 단계에서 관련 함수/메서드를 `[filepath:symbol]` 형식으로 참조
- **§4 API 레퍼런스 / API Reference** ★특화
   - 엔드포인트/함수/인터페이스 상세
   - 파라미터 (이름, 타입, 필수/선택, 설명)
   - 리턴값/응답 구조
   - 에러 코드 및 에러 응답
   - 코드 예시 (요청/응답 또는 호출 예시)
   - **인라인 citation**: 각 API/함수의 구현 소스를 `[filepath:symbol]` 형식으로 참조
- **§5 구현 가이드 / Implementation Guide**
   - 핵심 구현 규칙 및 제약
   - 체크리스트 (구현 전/중/후)
   - 안티패턴
   - **인라인 citation**: 핵심 규칙과 안티패턴에서 관련 코드를 `[filepath:symbol]` 형식으로 참조

Optional appendix:

- spec references with section names
- code references with file + symbol names
- assumptions / open points

#### Inline Citation Rules (모든 섹션 공통)

> spec-create의 Best Practices > Writing Quality와 동일한 규칙을 guide-create에서도 강제한다.

- **Code Excerpts**: 코드 발췌 시 `# [filepath:functionName]` 헤더를 코드 블록 첫 줄에 부착. ≤30줄 함수는 전문, >30줄 함수는 시그니처+핵심 로직만.
- **Inline Citations**: 본문에서 코드를 참조할 때 `[filepath:functionName]` 형식 사용. 예: "상태 검증은 `[src/payments/payment_service.ts:confirmPayment]`에서 수행한다."
- **Citation 밀도**: §2에만 한정하지 않고 §3 처리 흐름, §4 API 소스, §5 핵심 규칙/안티패턴에서도 코드 근거가 있으면 반드시 인라인 citation을 사용한다.
- **Source Field**: 컴포넌트 설명 시 `<path>`: ClassName, function_name() 형식. 코드베이스가 없으면 생략.
- **Low 신뢰도 예외**: 코드 근거가 없는 Low 신뢰도 가이드에서는 citation 대신 "코드 미확인" 표기.

### Step 6: Save with Backup Semantics

**Tools**: `Bash (mkdir -p, cp/mv)`, `Write`

For each feature guide:

1. Ensure `_sdd/guides/` exists.
2. If target file exists:
   - ensure `_sdd/guides/prev/` exists
   - create `PREV_guide_<slug>_<timestamp>.md`
3. Write the new `guide_<slug>.md`
4. Report the generated path(s) to the user

## Output Format

### File Location

- `_sdd/guides/guide_<slug>.md`

### Required Document Schema

```markdown
# 기능 기술 보고서: <feature>

**Version**: X.Y.Z
**Status**: Draft | In Review | Approved | Deprecated
**생성일**: YYYY-MM-DD
**입력 소스**: [conversation/spec/code]
**대상 기능**: <feature>
**신뢰도**: High/Medium/Low

## §1 배경 및 동기
...

## §2 핵심 설계
...

## §3 사용 시나리오 가이드
...

## §4 API 레퍼런스
...

## §5 구현 가이드
...

## 부록 (선택)
...
```

Full formatting details, slug rules, backup rules, and reference notation rules are defined in `references/output-format.md`.

## Error Handling

| Situation | Response |
|----------|----------|
| `_sdd/spec/` missing | `AskUserQuestion`으로 사용자에게 선택지 제공 (spec-create 실행 / 스펙 없이 Low 신뢰도로 계속) |
| Main spec not found | `AskUserQuestion`으로 사용자에게 선택지 제공 (spec-create 실행 / 스펙 없이 Low 신뢰도로 계속) |
| Feature is too ambiguous | Use the strongest available spec phrasing and record assumptions |
| Code evidence is missing | Generate a spec-grounded report and mark code references as unavailable |
| Multiple features requested | Generate separate guide files per feature |
| Existing guide file found | Backup to `_sdd/guides/prev/` before overwriting |
| Mixed language signals | 기존 스펙/문서의 언어를 따른다. 사용자 명시 지정 시 해당 언어 사용. 새 프로젝트는 한국어 기본. |

## Additional Resources

- `references/template-compact.md` — canonical guide generation template with Writing Rules and §1-§5 structure
- `references/output-format.md` — required guide structure and notation rules
- `references/tool-and-gates.md` — tool mapping, decision gates, and context management
- `examples/feature-guide-example.md` — sample output (Medium confidence, spec+code mixed)
- `examples/feature-guide-example-high.md` — sample output (High confidence, spec+code fully confirmed)
- `examples/feature-guide-example-low.md` — sample output (Low confidence, spec-only, no code evidence)
