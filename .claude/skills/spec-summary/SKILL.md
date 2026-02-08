---
name: spec-summary
description: This skill should be used when the user asks to "summarize spec", "spec summary", "show spec overview", "스펙 요약", "스펙 개요", "show spec status", "스펙 현황", "project overview", "프로젝트 개요", "what's the current state", "현재 상태는", or wants a human-readable summary of the current specification for quick understanding.
version: 1.0.0
---

# spec-summary: Specification Summary Generator

## Overview

The **spec-summary** skill generates human-readable summaries of SDD (Spec-Driven Development) specification documents. It creates a layered, scannable document that helps both technical and non-technical stakeholders quickly understand:

- **Project motivation and goals** (What and Why)
- **High-level architecture** (3-5 key components, bird's-eye view)
- **Current status and progress** (completion percentage, feature dashboard)
- **Open issues and improvements** (prioritized by impact)
- **Recommended next steps** (immediate, short-term, long-term)

### Output

- **File**: `_sdd/spec/SUMMARY.md`
- **Format**: Layered markdown (executive summary → technical details)
- **Audience**: Mixed (stakeholders + developers)
- **Language**: Follows spec document language (Korean/English/bilingual)

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

## Input Sources

The skill reads information from multiple sources:

### Primary Source
- **Main spec**: `_sdd/spec/<project>.md` or `_sdd/spec/main.md`
- **Sub-specs**: Prefer sub-spec files referenced/linked from the index/main spec.
  - Common convention: `_sdd/spec/<project>_*.md` (e.g. `<project>_API.md`, `<project>_DATA_MODEL.md`)
  - Important: exclude generated/backup files such as `SUMMARY.md` and `PREV_*.md`

### Secondary Sources (Optional)
- **Implementation progress**: `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`
- **Implementation progress (phases)**: `_sdd/implementation/IMPLEMENTATION_PROGRESS_PHASE_<n>.md` (if present, prefer the latest phase for “current status”)
- **Implementation review**: `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
- **Status markers in spec**: 📋 (계획됨), 🚧 (진행중), ✅ (완료), ⏸️ (보류)

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

1. Search for main spec in `_sdd/spec/`:
   - `<project>.md` (named after project)
   - `main.md` (generic name)
   - If still ambiguous: list candidates and ask the user which should be treated as the index/main spec
   - Do **not** auto-select generated/backup files:
     - `SUMMARY.md`
     - `PREV_*.md`
2. If spec is split:
   - Identify sub-spec files via index/links
   - Read all linked/related specs for a complete picture
   - If the index does not link clearly, prefer `_sdd/spec/<project>_*.md` (excluding `SUMMARY.md` and `PREV_*.md`) and confirm the intended set with the user
3. Check for implementation files:
   - `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`
   - `_sdd/implementation/IMPLEMENTATION_PROGRESS_PHASE_<n>.md` (if multiple exist, prefer the latest phase; ask the user if they want all phases summarized)
   - `_sdd/implementation/IMPLEMENTATION_REVIEW.md`

**Error Handling**: If no spec found → suggest `/spec-create` first

### Step 2: Extract Key Information

#### From Spec Document(s)

1. **Metadata**
   - Project name (from heading or filename)
   - Version (if specified)
   - Last modified date

2. **Goal Section** → "What" and "Why"
   - Parse 목표 (Goal) section
   - Extract purpose statement
   - Identify problem being solved

3. **Feature List with Status** → Progress Calculation
   ```
   Parse status markers:
   - ✅ (완료/completed) → count as done
   - 🚧 (진행중/in-progress) → count as active
   - 📋 (계획됨/planned) → count as planned
   - ⏸️ (보류/on-hold) → exclude from total

   Calculate completion %:
   (completed / (completed + in-progress + planned)) * 100
   ```

4. **Architecture Overview** → Core Components
   - Extract component names and purposes
   - **Limit to 3-5 key components** (not all details)
   - Identify relationships between components
   - Extract tech stack information

5. **Issues & Improvements** → Prioritized List
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

### Step 5: Create Summary Document

1. Apply summary template (see `references/summary-template.md`)
2. Fill in extracted information
3. If `_sdd/spec/SUMMARY.md` already exists, create a versioned backup before overwriting:
   - `_sdd/spec/PREV_SUMMARY_<timestamp>.md`
4. Generate or update `_sdd/spec/SUMMARY.md`
5. Add generation timestamp and metadata
6. Preserve human-readable formatting (tables, emojis, visual markers)

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

## 🏗️ Architecture at a Glance (아키텍처 개요)

### Core Components (3-5 key components only)

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

### Key Formatting Principles

1. **Layered Information**
   - Executive summary first (non-technical)
   - Technical details follow
   - Each section standalone and scannable

2. **Visual Hierarchy**
   - Emojis for quick scanning (🎯, 🏗️, 📊, ⚠️, 🚀, 📚)
   - Tables for structured data
   - Checkboxes for actionable items
   - Priority colors (🔴 🟡 🟢)

3. **Bilingual Headers**
   - Korean/English for mixed teams
   - Terminology follows spec document

4. **Conciseness**
   - Executive summary: 1-2 sentences per item
   - Architecture: 3-5 components max
   - Next steps: Specific and time-bound

## Best Practices

### For Executors

1. **Keep Executive Summary Non-Technical**
   - ❌ Bad: "Implements REST API with JWT authentication and PostgreSQL"
   - ✅ Good: "Securely manages user data and access permissions"

2. **Limit Architecture to Core Components**
   - Don't list every class/module
   - Show only 3-5 key components that matter to understanding
   - Focus on relationships and data flow

3. **Prioritize Issues by Impact**
   - Not just spec order
   - Consider: user impact, security, performance, tech debt cost
   - High priority = blocks progress or affects users

4. **Make Next Steps Concrete and Time-Bound**
   - ❌ Bad: "Improve performance"
   - ✅ Good: "Profile database queries and optimize top 3 slow endpoints (this week)"

5. **Use Visual Markers for Scannability**
   - Tables > long paragraphs
   - Emojis > text labels (when appropriate)
   - Checkboxes > bulleted lists (for action items)

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
```

This generates a shorter summary with only requested sections.

## Examples

See `examples/summary-output.md` for a complete example summary.

See `references/summary-template.md` for the template with placeholders.

## Success Criteria

A good summary should:

- [ ] Be scannable in < 2 minutes
- [ ] Answer "What/Why/Status" in executive summary
- [ ] Show 3-5 core components (not all details)
- [ ] Calculate accurate completion percentage
- [ ] Prioritize issues by impact
- [ ] Provide concrete, time-bound next steps
- [ ] Serve both technical and non-technical readers
- [ ] Update smoothly when spec changes

## Version History

- **1.0.0** (2026-02): Initial release
  - Layered summary format
  - Status dashboard
  - Prioritized issues
  - Actionable recommendations
  - Bilingual support
