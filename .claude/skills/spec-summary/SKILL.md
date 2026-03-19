---
name: spec-summary
description: This skill should be used when the user asks to "summarize spec", "spec summary", "show spec overview", "스펙 요약", "스펙 개요", "show spec status", "스펙 현황", "project overview", "프로젝트 개요", "what's the current state", "현재 상태는", or wants a human-readable summary of the current specification for quick understanding.
version: 1.4.0
---

# spec-summary: Specification Summary Generator

| Workflow | Position | When |
|----------|----------|------|
| Any | Standalone | 프로젝트 현황 파악, 스테이크홀더 미팅, 온보딩 |
| Any | After spec-update-todo/done | 스펙 변경 후 요약 갱신 |

## Acceptance Criteria
> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: `Glob("_sdd/spec/SUMMARY.md")` → 파일 존재 확인
- [ ] AC2: SUMMARY.md가 정확한 진행률(완료/진행중/계획)을 포함한다
- [ ] AC3: 핵심 기능별 plain-text 설명(what/how/why/status)이 포함된다
- [ ] AC4: 권장 다음 단계(Immediate/Short-term/Long-term)가 구체적이고 time-bound이다
- [ ] AC5: Executive Summary에서 What/Why/Status를 2분 내 파악 가능하다
- [ ] AC6: 기존 SUMMARY.md가 있었으면 `prev/PREV_SUMMARY_<timestamp>.md`로 백업되었다
- [ ] AC7: (README 요청 시) marker block만 업데이트되고 다른 README 내용은 보존된다

## Overview

**spec-summary**는 SDD 스펙 문서로부터 layered, scannable 요약 문서를 생성한다.

### Output

| 항목 | 값 |
|------|-----|
| Primary file | `_sdd/spec/SUMMARY.md` |
| Optional file | `README.md` (사용자 명시 요청 시만) |
| Format | Layered markdown (executive summary → technical details) |
| Audience | Mixed (stakeholders + developers) |
| Language | 스펙 문서 언어를 따름 |

## Hard Rules

1. **Spec read-only**: `_sdd/spec/*.md` 파일은 읽기 전용이다 (`SUMMARY.md` 제외). 스펙 내용을 수정하지 않는다.
2. **README sync on explicit request only**: README 업데이트는 사용자가 명시적으로 요청할 때만 수행한다.
3. **언어 규칙**: 기존 스펙/문서의 언어를 따른다. 새 프로젝트(기존 스펙 없음)는 한국어 기본. 사용자 명시 지정 시 해당 언어 사용.
4. **백업 후 덮어쓰기**: 기존 `SUMMARY.md` 존재 시 `prev/PREV_SUMMARY_<timestamp>.md`로 백업 후 새로 생성한다.

## Input Sources

### Primary Source
- **Main spec**: `_sdd/spec/<project>.md` 또는 `_sdd/spec/main.md`
- **Sub-specs**: index/main spec에서 참조하는 하위 스펙 파일 (e.g. `<project>_API.md`, `<project>_DATA_MODEL.md`)
  - `SUMMARY.md`, `prev/PREV_*.md`는 제외

### Secondary Sources (Optional)

| Source | Path | Usage |
|--------|------|-------|
| Implementation progress | `_sdd/implementation/IMPLEMENTATION_PROGRESS.md` | 현재 진행 상황 |
| Implementation progress (phases) | `_sdd/implementation/IMPLEMENTATION_PROGRESS_PHASE_<n>.md` | 최신 phase 우선 |
| Implementation review | `_sdd/implementation/IMPLEMENTATION_REVIEW.md` | 리뷰 결과 |
| Project README | `README.md` | README sync 요청 시만 |
| Environment guide | `_sdd/env.md` | 로컬 검증 필요 시 |

### Status Markers

| Marker | 의미 | 진행률 계산 |
|--------|------|-------------|
| ✅ | 완료 | completed |
| 🚧 | 진행중 | in-progress |
| 📋 | 계획됨 | planned |
| ⏸️ | 보류 | 제외 |

진행률 = `completed / (completed + in-progress + planned) * 100`

### Spec Document Structure

Whitepaper-style (§1~§8)과 legacy 포맷 모두 지원. Whitepaper 섹션은 optional.

**Whitepaper section → summary 매핑:**
- §1 Background & Motivation → Executive Summary "Why" 강화
- §2 Core Design → Core Design Highlights (없으면 생략)
- §5 Usage Guide → Usage Scenarios (없으면 생략)

## Summary Generation Process

### Step 1: Locate Spec Documents

**Tools**: `Glob`, `Read`

1. `_sdd/spec/`에서 main spec 검색: `<project>.md` → `main.md` → 후보 제시
2. Split spec: index/links 따라 sub-spec 수집
3. Implementation 파일 확인: `IMPLEMENTATION_PROGRESS*.md`, `IMPLEMENTATION_REVIEW.md`
4. 로컬 검증 필요 시 `_sdd/env.md` 참조

> No spec found → `/spec-create` 권장. 읽기 불가 → 오류 메시지 후 중지.

### Step 2: Extract Key Information

**Tools**: `Read`, `Glob`, `Grep`

#### From Spec Document(s)

1. **Metadata**: 프로젝트명, 버전, 최종 수정일
2. **Goal Section → What/Why**
   - §1 존재 시 Problem Statement + Core Value Proposition으로 "Why" 강화
3. **Core Design (§2) → Core Design Highlights** (conditional)
   - Key Idea (1-3문장), Design Rationale (1-2문장), 인라인 코드 참조
   - §2 없으면 skip
4. **Usage Guide (§5) → Usage Scenarios** (conditional)
   - 2-3개 시나리오 (action + expected result)
   - §5 없으면 skip
5. **Key Feature Explanations** → 대표 기능별 plain-text (what/how/why/status)
6. **Feature List with Status** → 진행률 계산
7. **Architecture Overview** → 핵심 컴포넌트만 (관계, 기술 스택)
8. **Issues & Improvements** → 카테고리(Bug/Enhancement/Tech Debt) + 우선순위

#### From Implementation Files (If Exist)

- `IMPLEMENTATION_PROGRESS.md`: 현재 태스크, 블로커, 마일스톤
- `IMPLEMENTATION_REVIEW.md`: 리뷰 결과, 품질 이슈, 권장 액션

### Step 3: Analyze Status

진행률 및 이슈 메트릭 계산:
- Feature: total, completion rate, active, backlog
- Issue: high priority(bugs + critical), tech debt, enhancement requests

### Step 4: Generate Recommendations

| 시간대 | 기준 | 예시 |
|--------|------|------|
| Immediate (이번 주) | high-priority 이슈, 거의 완료된 진행중 기능, 블로커 | "Fix [issue] affecting [component]" |
| Short-term (이번 달) | 의존성 해결된 계획 기능, 중간 우선순위 개선, 테스트 갭 | "Start implementing [feature]" |
| Long-term (분기/연간) | 대규모 계획 기능, 아키텍처 개선, 기술 부채 정리 | "Milestone: [feature set] by Q[N]" |

**권장 로직**: high-priority issues > 0 → 즉시 대응 / in-progress > 0 → 완료 우선 / completion > 80% → 다음 기능 시작 / tech debt > 5 → 정리 스프린트

### Step 4.5: 요약 초안 제시

사용자에게 초안 테이블 제시 후 바로 Step 5로 진행 (확인 대기 없음):

```
| 항목 | 내용 |
|------|------|
| 프로젝트명 | ... |
| 전체 진행률 | N% |
| 완료/진행중/계획 | X / Y / Z |
| 핵심 설계 (§2) | 있음 / 없음 |
| 핵심 기능 수 | N개 |
| 사용 시나리오 (§5) | 있음 / 없음 |
| 이슈 수 | High N / Medium N / Low N |
| 권장 다음 단계 | N개 |
```

### Step 5: Create Summary Document

**Tools**: `Write`, `Bash (mkdir -p)`

출력 문서 작성 시 `write-phased` 서브에이전트에 위임한다. Output Format 전체와 수집 맥락을 프롬프트에 포함.

1. Summary template 적용 (`references/summary-template.md`)
   - §2 존재 → Core Design Highlights 포함, 없으면 생략
   - §5 존재 → Usage Scenarios 포함, 없으면 생략
   - §1 존재 → Executive Summary "Why" 강화
2. 기존 `SUMMARY.md` → `prev/PREV_SUMMARY_<timestamp>.md` 백업
3. `_sdd/spec/SUMMARY.md` 생성
4. 타임스탬프/메타데이터 추가

> SUMMARY.md 생성 완료 + README 요청 → Step 6 / README 미요청 → 완료 / 미생성 → Step 5 재실행

### Step 6: Optional README Sync (On Request Only)

**Tools**: `Read`, `Edit`, `Write`

1. 사용자 명시 요청 시만 실행
2. Marker block: `<!-- spec-summary:start -->` ~ `<!-- spec-summary:end -->`
3. Marker 존재 → 사이 내용만 교체
4. Marker 미존재 → 첫 H1 뒤에 삽입 (없으면 문서 끝에 추가)
5. Marker 밖 내용은 절대 변경하지 않음

## Output Format

생성되는 summary의 layered 구조:

```markdown
# [Project Name] - Specification Summary

**생성일** (Generated): YYYY-MM-DD HH:MM
**스펙 버전** (Spec Version): X.Y.Z
**최종 업데이트** (Last Updated): YYYY-MM-DD

---

## 🎯 Executive Summary (비기술 담당자용)

### What (무엇을)
[1-2 sentences: What this project does in plain language]

### Why (왜)
[1-2 sentences: The problem it solves or value it provides]
[IF §1 Background & Motivation exists: enrich with Problem Statement + Core Value Proposition]

### Status (현재 상태)
- **전체 진행률** (Overall Progress): X%
- **완료된 기능** (Completed): N개
- **진행중인 기능** (In Progress): M개
- **계획된 기능** (Planned): K개

---

## 💡 Core Design Highlights (핵심 설계 요약)

[ONLY if §2 Core Design exists in spec; otherwise OMIT entirely]

### Key Idea (핵심 아이디어)
[1-3 sentences from §2 Core Design > Key Idea]

### Design Rationale (설계 근거)
[1-2 sentences from §2 Core Design > Design Rationale]

### Key Code Reference (핵심 코드 참조)
[IF inline citations exist: show key `[filepath:functionName]` references]

---

## ✨ Key Feature Explanations (기능별 상세 설명)

[Explain representative features as paper-like subsections. Use plain language and avoid heavy jargon.]

### 1. [Feature Name]
**Status**: ✅ / 🚧 / 📋 / ✅+🚧 / Unknown
[plain-text explanation]
- what this feature does.
- how it works end-to-end in simple terms.
- why this matters (user/business impact).
- (optional): current limitation, blocker, or next step.

### 2. [Feature Name]
**Status**: ✅ / 🚧 / 📋 / ✅+🚧 / Unknown
[plain-text explanation following the same pattern]

[Selection rules]
- Choose representative features (prefer user-facing + actively developed)
- Do not collapse major features into one generic capability name
- Keep terminology simple; define unavoidable technical terms once
- If evidence is weak, mark status as `Unknown` and state assumptions explicitly

---

## 🏗️ Architecture at a Glance (아키텍처 개요)

### Core Components (key components only)

```
[ASCII diagram showing component relationships]
Component A ──> Component B
     │              │
     └──> Component C
```

| Component | Purpose | Status |
|-----------|---------|--------|
| Component A | [What it does] | ✅ / 🚧 / 📋 |
| Component B | [What it does] | ✅ / 🚧 / 📋 |
| Component C | [What it does] | ✅ / 🚧 / 📋 |

### Tech Stack
- **Language** (언어): [주 언어]
- **Framework** (프레임워크): [주요 프레임워크]
- **Key Libraries** (핵심 라이브러리): [핵심 라이브러리 3개 이하]

---

## 📊 Feature Status Dashboard

### Completed Features ✅
- **[Feature 1]** - [brief description]
- **[Feature 2]** - [brief description]

### In Progress 🚧
- **[Feature 3]** - [brief description] ([X]% complete)
- **[Feature 4]** - [brief description]

### Planned 📋
- **[Feature 5]** - [brief description]
- **[Feature 6]** - [brief description]

### On Hold ⏸️
- **[Feature 7]** - [brief description] (Reason: [why on hold])

---

## 📖 Usage Scenarios (주요 사용 시나리오)

[ONLY if §5 Usage Guide & Expected Results exists in spec; otherwise OMIT entirely]

### Scenario 1: [Name]
- **Action**: [What the user does]
- **Expected Result**: [Observable outcome]

### Scenario 2: [Name]
- **Action**: [What the user does]
- **Expected Result**: [Observable outcome]

---

## ⚠️ Open Issues & Improvements (우선순위순)

### High Priority 🔴
1. **[Issue/Improvement Title]** (Category: Bug/Enhancement/Tech Debt)
   - **Impact** (영향): [Why it matters]
   - **Location** (위치): [File/Component if known]
   - **Suggested Fix** (해결 방안): [Brief suggestion if available]

### Medium Priority 🟡
[Same format as high priority]

### Low Priority 🟢
[Same format as high priority]

---

## 🚀 Recommended Next Steps

Based on current spec state and progress:

### 1. Immediate Actions (이번 주)
- [ ] **[Action item 1]** - [Why/Impact]
- [ ] **[Action item 2]** - [Why/Impact]

### 2. Short-term Goals (이번 달)
- [ ] **[Goal 1]** - [Expected outcome]
- [ ] **[Goal 2]** - [Expected outcome]

### 3. Long-term Roadmap (분기/연간)
- [ ] **[Milestone 1]** - [Target: Q[N] YYYY]
- [ ] **[Milestone 2]** - [Target: Q[N] YYYY]

---

## 📚 Quick Reference

### Key Files
- **Spec Document** (스펙 문서): `_sdd/spec/<project>.md`
- **Implementation Progress** (구현 진행): `_sdd/implementation/IMPLEMENTATION_PROGRESS.md` (if exists)
- **Latest Review** (최근 리뷰): `_sdd/implementation/IMPLEMENTATION_REVIEW.md` (if exists)

### Related Commands
- `/spec-update-todo` - Add new features to spec
- `/implementation-plan` - Create implementation plan from spec
- `/spec-update-done` - Sync spec with code changes
- `/spec-summary` - Regenerate this summary

---

**Summary 생성 방법**: `/spec-summary`를 실행하면 이 파일이 자동 생성/갱신됩니다.
```

### Optional README Block Output

README sync 요청 시 `README.md`에 삽입/갱신하는 marker block:

```markdown
<!-- spec-summary:start -->
## Project Snapshot

### What
[1-2 sentence summary]

### Current Status
- Overall Progress: X%
- Completed / In Progress / Planned: N / M / K

### Key Feature Explanations
### 1. [Feature Name]
[Plain-text what/how/why/status paragraph]

### 2. [Feature Name]
[Plain-text what/how/why/status paragraph]

More details: [`_sdd/spec/SUMMARY.md`](_sdd/spec/SUMMARY.md)
<!-- spec-summary:end -->
```

### Key Formatting Principles

| 원칙 | 적용 |
|------|------|
| Layered Information | Executive summary (non-technical) → technical details, 각 섹션 독립적 |
| Visual Hierarchy | 이모지 헤더, 테이블, 체크박스, 우선순위 색상 (🔴🟡🟢) |
| Bilingual Headers | 한영 병기 (mixed team 대응) |
| Conciseness | Executive: 1-2문장, Feature: paragraph, Architecture: 핵심만, Next steps: 구체적+기한 |

## Language Handling

| Spec Language | Summary Language | Headers |
|---------------|------------------|---------|
| Korean | Korean | Bilingual (Korean + English) |
| English | English | English only |
| Mixed | Follow majority | Bilingual |

기술 용어는 스펙 원문 유지, 톤/격식 보존.

## Error Handling

| Situation | Action | Message to User |
|-----------|--------|-----------------|
| No spec found | Suggest `/spec-create` | "No spec document found in `_sdd/spec/`. Run `/spec-create` first." |
| Empty spec | Minimal summary + warning | "Spec is empty/minimal. Consider `/spec-update-todo`." |
| No status markers | Mark "status unknown" | "No status markers found. Progress unavailable." |
| Multiple main specs | Ask user | "Found multiple spec files: [list]. Which to summarize?" |
| No architecture section | Skip section | "No architecture section found. Omitting." |
| No issues section | Empty section + note | "No open issues documented." |
| README not found (sync requested) | Create minimal README | "README.md not found. Creating with spec-summary block." |
| README has no markers | Insert new block | "Inserting spec-summary block, preserving other content." |
| `_sdd/env.md` missing (validation needed) | Skip execution, ask user | "env.md missing. Proceeding with document-only summary." |

## Advanced Usage

### Summarizing Split Specs

1. index spec (`<project>.md` / `main.md`) 읽기
2. 링크된 sub-spec 수집 및 집계
3. 이슈 병합, 진행률 통합
4. 통합 summary 생성

### Custom Summary Scope

사용자 요청에 따라 특정 섹션만 생성 가능: 이슈만, 진행률만, 아키텍처만, 핵심 기능만, README 포함 등.

## Examples

See `examples/summary-output.md` for a complete example summary.

See `references/summary-template.md` for the template with placeholders.

**Integration**: `spec-create` / `spec-update-todo` / `spec-update-done` → `spec-summary` 순서로 연계 사용.

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

