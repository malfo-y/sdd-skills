---
name: spec-summary
description: This skill should be used when the user asks to "summarize spec", "spec summary", "show spec overview", "스펙 요약", "스펙 개요", "show spec status", "스펙 현황", "project overview", "프로젝트 개요", "what's the current state", "현재 상태는", or wants a human-readable summary of the current specification for quick understanding.
version: 1.3.0
---

# spec-summary: Specification Summary Generator

| Workflow | Position | When |
|----------|----------|------|
| Any | Standalone | 프로젝트 현황 파악, 스테이크홀더 미팅, 온보딩 |
| Any | After spec-update-todo/done | 스펙 변경 후 요약 갱신 |

## Overview

The **spec-summary** skill generates human-readable summaries of SDD (Spec-Driven Development) specification documents. It creates a layered, scannable document that helps both technical and non-technical stakeholders quickly understand:

- **Project motivation and goals** (What and Why)
- **Key features explained clearly** (feature-by-feature plain text paragraphs)
- **High-level architecture** (key components, bird's-eye view)
- **Current status and progress** (completion percentage, feature dashboard)
- **Open issues and improvements** (prioritized by impact)
- **Recommended next steps** (immediate, short-term, long-term)
- **Project README snapshot** (optional, marker-based update on request)

### Output

- **Primary file**: `_sdd/spec/SUMMARY.md`
- **Optional file**: `README.md` (only when user explicitly requests README create/update)
- **Format**: Layered markdown (executive summary → technical details)
- **Audience**: Mixed (stakeholders + developers)
- **Language**: Follows spec document language (Korean/English/bilingual)

## Hard Rules

1. **Spec read-only**: `_sdd/spec/*.md` 파일은 읽기 전용이다 (`SUMMARY.md` 제외). 스펙 내용을 수정하지 않는다.
2. **README sync on explicit request only**: README 업데이트는 사용자가 명시적으로 요청할 때만 수행한다.
3. **언어 규칙**: 기존 스펙/문서의 언어를 따른다. 새 프로젝트(기존 스펙 없음)는 한국어 기본. 사용자 명시 지정 시 해당 언어 사용.
4. **백업 후 덮어쓰기**: 기존 `SUMMARY.md` 존재 시 `prev/PREV_SUMMARY_<timestamp>.md`로 백업 후 새로 생성한다.

## When to Use This Skill

Trigger `/spec-summary` in these scenarios:

1. **Before stakeholder meetings** - Quick status brief
2. **Onboarding new team members** - Project overview
3. **After major spec updates** - Show what changed
4. **After spec review** - Sync results summary
5. **Periodic status checks** - Weekly/monthly progress reports
6. **Before implementation planning** - Understand current state

### Trigger Phrases

The skill auto-activates when the user says:
- "summarize spec" / "스펙 요약"
- "spec summary" / "spec overview"
- "show spec status" / "스펙 현황"
- "project overview" / "프로젝트 개요"
- "what's the current state" / "현재 상태는"
- "README도 같이 업데이트" / "update README too"
- "README 만들어줘" / "create README from summary"

## Input Sources

The skill reads information from multiple sources:

### Primary Source
- **Main spec**: `_sdd/spec/<project>.md` or `_sdd/spec/main.md`
- **Sub-specs**: Prefer sub-spec files referenced/linked from the index/main spec.
  - Common convention: `_sdd/spec/<project>_*.md` (e.g. `<project>_API.md`, `<project>_DATA_MODEL.md`)
  - Important: exclude generated/backup files such as `SUMMARY.md` and `prev/PREV_*.md`

### Secondary Sources (Optional)
- **Implementation progress**: `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`
- **Implementation progress (phases)**: `_sdd/implementation/IMPLEMENTATION_PROGRESS_PHASE_<n>.md` (if present, prefer the latest phase for “current status”)
- **Implementation review**: `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
- **Project README**: `README.md` (only when README sync is requested)
- **Status markers in spec**: 📋 (계획됨), 🚧 (진행중), ✅ (완료), ⏸️ (보류)
- **Execution/test environment guide**: `_sdd/env.md` (only when local validation commands/tests are needed)

### Spec Document Structure Expected

The skill expects spec documents to follow SDD format:

```markdown
# [Project Name]

## 목표 (Goal)
- ✅ Feature 1
- 🚧 Feature 2 (진행중)
- 📋 Feature 3 (계획됨)

## 아키텍처 개요 (Architecture Overview)
[Component descriptions]

## 컴포넌트 상세 (Component Details)
[Detailed component information]

## 환경 및 의존성 (Environment & Dependencies)
[Tech stack and dependencies]

## 발견된 이슈 및 개선 필요사항 (Issues & Improvements)
[Known issues and improvement ideas]

## 사용 예시 (Usage Examples)
[Code examples]
```

## Summary Generation Process

### Step 1: Locate Spec Documents

**Tools**: `Glob`, `Read`

1. Search for main spec in `_sdd/spec/`:
   - `<project>.md` (named after project)
   - `main.md` (generic name)
   - If still ambiguous: list candidates and ask the user which should be treated as the index/main spec
   - Do **not** auto-select generated/backup files:
     - `SUMMARY.md`
     - `prev/PREV_*.md`
2. If spec is split:
   - Identify sub-spec files via index/links
   - Read all linked/related specs for a complete picture
   - If the index does not link clearly, prefer `_sdd/spec/<project>_*.md` (excluding `SUMMARY.md` and `prev/PREV_*.md`) and confirm the intended set with the user
3. Check for implementation files:
   - `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`
   - `_sdd/implementation/IMPLEMENTATION_PROGRESS_PHASE_<n>.md` (if multiple exist, summarize all phases)
   - `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
4. If local runtime/test validation is needed for summary evidence, read `_sdd/env.md` and apply setup before running commands.

**Error Handling**: If no spec found → suggest `/spec-create` first

**Decision Gate 1→2**:
```
spec_found = 스펙 문서 발견
spec_readable = 스펙 파일 읽기 가능

IF spec_found AND spec_readable → Step 2 진행
ELSE IF NOT spec_found → `/spec-create` 먼저 실행 권장
ELSE → 오류 메시지 출력 후 중지: "스펙 파일에 접근할 수 없습니다. 파일 경로와 권한을 확인해 주세요."
```

### Step 2: Extract Key Information

**Tools**: `Read`, `Glob`, `Grep`

#### From Spec Document(s)

1. **Metadata**
   - Project name (from heading or filename)
   - Version (if specified)
   - Last modified date

2. **Goal Section** → "What" and "Why"
   - Parse 목표 (Goal) section
   - Extract purpose statement
   - Identify problem being solved

3. **Key Feature Explanations (Feature-by-Feature)** → Narrative Paragraphs
   - Select representative features from Goal and feature sections
   - For each feature, capture: what it does, how it works, why it matters, and current status
   - Write plain-text explanations (paper paragraph style)
   - If details are incomplete, keep wording explicit and mark status as `Unknown`

4. **Feature List with Status** → Progress Calculation
   ```
   Parse status markers:
   - ✅ (완료/completed) → count as done
   - 🚧 (진행중/in-progress) → count as active
   - 📋 (계획됨/planned) → count as planned
   - ⏸️ (보류/on-hold) → exclude from total

   Calculate completion %:
   (completed / (completed + in-progress + planned)) * 100
   ```

5. **Architecture Overview** → Core Components
   - Extract component names and purposes
   - **Limit to key components** (not all details)
   - Identify relationships between components
   - Extract tech stack information

6. **Issues & Improvements** → Prioritized List
   - Parse 발견된 이슈 및 개선 필요사항 section
   - Categorize: Bug, Enhancement, Tech Debt
   - Infer priority from spec order or keywords

#### From Implementation Files (If Exist)

1. **IMPLEMENTATION_PROGRESS.md**
   - Current task status
   - Blockers or challenges
   - Recent milestones

2. **IMPLEMENTATION_REVIEW.md**
   - Review findings
   - Quality issues
   - Recommended actions

### Step 3: Analyze Status

**Tools**: — (계산/분석, 도구 불필요)

Calculate project health metrics:

```
Feature Metrics:
- Total features = completed + in-progress + planned
- Completion rate = (completed / total) * 100
- Active work items = in-progress count
- Backlog size = planned count

Issue Metrics:
- High priority issues = bugs + critical improvements
- Technical debt items = refactoring/cleanup needs
- Enhancement requests = new feature ideas
```

### Step 4: Generate Recommendations

**Tools**: — (분석 기반 권장 사항 생성, 도구 불필요)

Based on current state, suggest actionable next steps:

#### Immediate Actions (This Week)
- **High-priority issues** → "Fix [issue] affecting [component]"
- **In-progress features near completion** → "Complete [feature] (80% done)"
- **Blockers from implementation review** → "Unblock [task] by resolving [dependency]"

#### Short-term Goals (This Month)
- **Planned features with dependencies resolved** → "Start implementing [feature]"
- **Medium-priority improvements** → "Refactor [component] for better [quality attribute]"
- **Testing/documentation gaps** → "Add tests for [component]"

#### Long-term Roadmap (Quarter/Year)
- **Major planned features** → "Milestone: [feature set] by Q[N]"
- **Architectural improvements** → "Migrate to [new architecture] for [benefit]"
- **Tech debt cleanup** → "Quarterly cleanup sprint for [area]"

**Recommendation Logic**:
```text
Pseudo-logic:

- If high priority issues > 0:
  - Immediate: Address critical issues first
- If in-progress items > 0:
  - Immediate: Complete active features before starting new ones
- If completion rate > 80% and planned items > 0:
  - Short-term: Start next planned feature set
- If tech debt items > 5:
  - Long-term: Schedule tech debt cleanup sprint
```

### Step 4.5: 요약 초안 제시

요약 초안 테이블을 사용자에게 제시한 후 바로 Step 5로 진행한다 (사용자 확인을 기다리지 않는다):

```
| 항목 | 내용 |
|------|------|
| 프로젝트명 | ... |
| 전체 진행률 | N% |
| 완료/진행중/계획 | X / Y / Z |
| 핵심 기능 수 | N개 |
| 이슈 수 | High N / Medium N / Low N |
| 권장 다음 단계 | N개 |
```

**Decision Gate 5→6**:
```
summary_created = SUMMARY.md 생성 완료
readme_requested = 사용자가 README 업데이트 요청

IF summary_created AND readme_requested → Step 6 진행
ELSE IF summary_created AND NOT readme_requested → 완료
ELSE → Step 5 재실행
```

### Step 5: Create Summary Document

**Tools**: `Write`, `Bash (mkdir -p)`

1. Apply summary template (see `references/summary-template.md`)
2. Fill in extracted information
3. If `_sdd/spec/SUMMARY.md` already exists, create a versioned backup before overwriting:
   - `_sdd/spec/prev/PREV_SUMMARY_<timestamp>.md` (create `_sdd/spec/prev/` if missing)
4. Generate or update `_sdd/spec/SUMMARY.md`
5. Add generation timestamp and metadata
6. Preserve human-readable formatting (tables, emojis, visual markers)

### Step 6: Optional README Sync (On Request Only)

**Tools**: `Read`, `Edit`, `Write`

1. Trigger only when user explicitly asks to create/update README
2. Use marker block strategy for safe partial updates:
   - Start marker: `<!-- spec-summary:start -->`
   - End marker: `<!-- spec-summary:end -->`
3. If markers exist in `README.md`, replace only content between markers
4. If markers do not exist:
   - Insert a new marker block after the first H1 (`# ...`) when present
   - Otherwise append the block to the end of `README.md`
5. Never overwrite the entire README; preserve all non-marker content
6. Keep README concise and link back to `_sdd/spec/SUMMARY.md` for full details

## Output Format

The generated summary follows this layered structure:

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

### Status (현재 상태)
- **전체 진행률** (Overall Progress): X%
- **완료된 기능** (Completed): N개
- **진행중인 기능** (In Progress): M개
- **계획된 기능** (Planned): K개

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
- [ ] **[Action item 3]** - [Why/Impact]

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
- **Implementation Plan** (구현 계획): `_sdd/implementation/IMPLEMENTATION_PLAN.md` (if exists)
- **Implementation Progress** (구현 진행): `_sdd/implementation/IMPLEMENTATION_PROGRESS.md` (if exists)
- **Latest Review** (최근 리뷰): `_sdd/implementation/IMPLEMENTATION_REVIEW.md` (if exists)

### Related Commands
- `/spec-update-todo` - Add new features to spec
- `/implementation-plan` - Create implementation plan from spec
- `/spec-update-done` - Sync spec with code changes
- `/spec-summary` - Regenerate this summary

---

**Summary 생성 방법**: `/spec-summary`를 실행하면 이 파일이 자동 생성/갱신됩니다.
**How to Generate**: Run `/spec-summary` to automatically create/update this file.
```

### Optional README Block Output

When README sync is requested, generate/update this marker block in `README.md`:

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

1. **Layered Information**
   - Executive summary first (non-technical)
   - Technical details follow
   - Each section standalone and scannable

2. **Visual Hierarchy**
   - Emojis for quick scanning (🎯, ✨, 🏗️, 📊, ⚠️, 🚀, 📚)
   - Tables for structured data
   - Checkboxes for actionable items
   - Priority colors (🔴 🟡 🟢)

3. **Bilingual Headers**
   - Korean/English for mixed teams
   - Terminology follows spec document

4. **Conciseness**
   - Executive summary: 1-2 sentences per item
   - Key features: feature-level paragraphs 
   - Architecture: key components first
   - README block: short snapshot + link to full summary
   - Next steps: Specific and time-bound

## Best Practices

### For Executors

1. **Keep Executive Summary Non-Technical**
   - ❌ Bad: "Implements REST API with JWT authentication and PostgreSQL"
   - ✅ Good: "Securely manages user data and access permissions"

2. **Limit Architecture to Core Components**
   - Don't list every class/module
   - Show only key components that matter to understanding
   - Focus on relationships and data flow

3. **Explain Key Features Feature-by-Feature**
   - Each paragraph should read like a mini abstract (what/how/why/status)
   - Keep explanations concrete and tied to feature names
   - Keep exhaustive counts and raw lists in the status dashboard

4. **Prioritize Issues by Impact**
   - Not just spec order
   - Consider: user impact, security, performance, tech debt cost
   - High priority = blocks progress or affects users

5. **Make Next Steps Concrete and Time-Bound**
   - ❌ Bad: "Improve performance"
   - ✅ Good: "Profile database queries and optimize top 3 slow endpoints (this week)"

6. **Use Visual Markers for Scannability**
   - Tables > long paragraphs
   - Emojis > text labels (when appropriate)
   - Checkboxes > bulleted lists (for action items)

7. **When validating with local execution, use the documented environment**
   - If local commands/tests are required, follow `_sdd/env.md` first
   - If `_sdd/env.md` is missing/incomplete, ask the user and proceed with document-only summary until clarified

8. **Use Marker-Based README Updates**
   - Update only the `spec-summary` marker block in `README.md`
   - Do not rewrite unrelated README sections
   - Always include a link to `_sdd/spec/SUMMARY.md`

### For Spec Authors

1. **Use Status Markers Consistently**
   - ✅ for completed features
   - 🚧 for work in progress
   - 📋 for planned features
   - ⏸️ for on-hold items

2. **Maintain Issues Section**
   - Update as you discover problems
   - Remove resolved issues
   - Add priority indicators if helpful

3. **Keep Architecture Section Current**
   - Update when major components change
   - Remove obsolete components
   - Document component relationships

## Integration with Other Skills

```
Workflow Integration:

spec-create ──> spec-summary
    │               ↑
    ↓               │
spec-update-todo ────────┘
    │
    ↓
implementation-plan ──> implementation ──> implementation-review ──> spec-update-done
                                                                          │
                                                                          ↓
                                                                    spec-summary
```

### Trigger Points

1. **After spec-update-todo**
   - Show what features were added
   - Update progress metrics
   - Adjust recommendations

2. **After spec-update-done**
   - Show sync results
   - Highlight drift areas
   - Update implementation progress

3. **Before implementation-plan**
   - Understand current state
   - Identify what's left to do
   - Inform planning decisions

4. **On-demand**
   - Status check meetings
   - New team member onboarding
   - Periodic reports

### Integration Examples

```bash
# Workflow 1: Update spec → summarize
/spec-update-todo
# (User adds new features)
/spec-summary
# → Summary shows new planned features

# Workflow 2: Review → summarize
/spec-update-done
# (Claude syncs spec with code)
/spec-summary
# → Summary shows updated completion status

# Workflow 3: Before planning
/spec-summary
# (Review current state)
/implementation-plan
# (Plan next iteration based on summary insights)
```

## Language Handling

The skill adapts to the spec document's language:

| Spec Language | Summary Language | Headers |
|---------------|------------------|---------|
| Korean | Korean | Bilingual (Korean + English) |
| English | English | English only |
| Mixed | Follow majority | Bilingual |

**Preservation Rules**:
- Keep technical terms from spec (don't translate)
- Maintain consistent terminology
- Preserve spec's tone and formality

## Error Handling

| Situation | Action | Message to User |
|-----------|--------|-----------------|
| No spec found | Suggest `/spec-create` | "No spec document found in `_sdd/spec/`. Run `/spec-create` first to generate a specification." |
| Empty spec | Generate minimal summary with warning | "Spec document is empty or minimal. Summary will be basic. Consider running `/spec-update-todo` to add features." |
| No status markers | Mark as "status unknown" | "No status markers found (✅, 🚧, 📋). Progress calculation unavailable. Add markers to feature list for tracking." |
| Multiple main specs | Ask user which to summarize | "Found multiple spec files: [list]. Which should I summarize? Or say 'all' to merge." |
| No architecture section | Skip architecture section | "No architecture section found. Summary will omit architecture overview." |
| No issues section | Show "No open issues documented" | Creates empty issues section with note. |
| README sync requested but `README.md` not found | Create minimal README with marker block | "README.md not found. I'll create one and insert a spec-summary block." |
| README has no marker block | Insert new marker block safely | "README exists without spec-summary markers. I'll insert a new managed block and preserve other content." |
| `_sdd/env.md` missing/incomplete (while local validation requested) | Skip local execution and ask user | "Local validation requested, but `_sdd/env.md` is missing/incomplete. I'll proceed with document-based summary unless you provide runtime setup details." |

## Advanced Usage

### Summarizing Split Specs

For projects with multiple spec files:

```
_sdd/spec/
  ├── <project>.md (index/overview)
  ├── <project>_API.md
  ├── <project>_DATA_MODEL.md
  └── <project>_COMPONENTS.md
```

**Behavior**:
1. Read the index spec (`<project>.md` or `main.md`) for overview
2. Follow links and aggregate key points/features from referenced sub-specs
3. Merge issues from all specs
4. Calculate combined progress
5. Generate unified summary

**User Control**:
```bash
/spec-summary
# If you want a full merged view across all linked sub-specs, say:
# - "모든 서브 스펙까지 포함해서 요약해줘" / "include all sub-specs"
# If you want to focus on a specific area, say:
# - "API 쪽만 요약해줘" / "Summarize only the API spec"
```

### Custom Summary Scope

Users can request focused summaries:

```bash
/spec-summary
# "이슈만 요약해줘" / "Only issues and recommendations"
# "진행률만 보여줘" / "Only progress dashboard"
# "아키텍처만 요약해줘" / "Only architecture overview"
# "핵심 기능 상세만 요약해줘" / "Only key feature explanations"
# "README도 같이 업데이트해줘" / "Also update README snapshot"
```

This generates a shorter summary with only requested sections.

## Examples

See `examples/summary-output.md` for a complete example summary.

See `references/summary-template.md` for the template with placeholders.

## Success Criteria (Glob 기반 검증 포함)

A good summary should:

- [ ] `Glob("_sdd/spec/SUMMARY.md")` → 파일 존재 확인
- [ ] Be scannable in < 2 minutes
- [ ] Answer "What/Why/Status" in executive summary
- [ ] Explain features with clear plain-text paragraph (what/how/why/status)
- [ ] Show core components (not all details)
- [ ] Calculate accurate completion percentage
- [ ] Prioritize issues by impact
- [ ] Provide concrete, time-bound next steps
- [ ] Serve both technical and non-technical readers
- [ ] Update smoothly when spec changes
- [ ] (If requested) README marker block is updated without damaging other README content

## Version History

- **1.3.0** (2026-02): Added optional README create/update flow
  - Added explicit README trigger phrases and optional output target
  - Added marker-based README sync strategy (`<!-- spec-summary:start/end -->`)
  - Added README snapshot output block template and error handling
- **1.2.0** (2026-02): Switched key features to feature-by-feature narrative subsections
  - Replaced high-level key-feature table with paper-like per-feature explanations
  - Updated extraction rules for plain-text what/how/why/status descriptions
  - Added focused scope phrase for key-feature explanation-only summaries
- **1.1.0** (2026-02): Added high-level key features section
  - New "Key Features (High-Level)" output section
  - Capability extraction guidance in summary generation process
  - Scope option for key-feature-only summaries
- **1.0.0** (2026-02): Initial release
  - Layered summary format
  - Status dashboard
  - Prioritized issues
  - Actionable recommendations
  - Bilingual support
