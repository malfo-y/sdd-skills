# Specification Summary Template

This template shows the structure and placeholders for generating spec summaries.

## Placeholder Syntax

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `[Project Name]` | Name of the project | "User Authentication Service" |
| `X%` | Percentage value | "75%" |
| `N개` / `N` | Count/number | "5개", "5 features" |
| `YYYY-MM-DD` | Date in ISO format | "2026-02-07" |
| `HH:MM` | Time in 24-hour format | "14:30" |
| `[brief description]` | 1 sentence description | "Validates user credentials securely" |
| `[Why/Impact]` | Reason or consequence | "Improves user experience" |
| `Q[N] YYYY` | Quarter and year | "Q2 2026" |

## Conditional Sections

Some sections should only appear if data is available:

| Section | Condition | Action if Missing |
|---------|-----------|-------------------|
| Implementation Progress | `IMPLEMENTATION_PROGRESS.md` exists | Omit from Quick Reference |
| Implementation Progress (Phases) | Any `IMPLEMENTATION_PROGRESS_PHASE_<n>.md` exists | Include **latest phase** in Quick Reference; omit if none |
| Implementation Review | `IMPLEMENTATION_REVIEW.md` exists | Omit from Quick Reference |
| Split Specs | Index spec links to other `_sdd/spec/*.md` files | Include linked sub-specs in Quick Reference; omit if not split |
| Summary Backup | `_sdd/spec/SUMMARY.md` already exists | Create `_sdd/spec/prev/PREV_SUMMARY_<timestamp>.md` before overwriting |
| On Hold Features | Any ⏸️ markers in spec | Omit "On Hold" subsection |
| High Priority Issues | Any high-priority items | Show "No high-priority issues" |
| Architecture Diagram | 2+ components | Generate ASCII diagram |

## Full Template

```markdown
# [Project Name] - Specification Summary

**생성일** (Generated): [YYYY-MM-DD] [HH:MM]
**스펙 버전** (Spec Version): [X.Y.Z or "N/A"]
**최종 업데이트** (Last Updated): [YYYY-MM-DD from file mtime]

---

## 🎯 Executive Summary (비기술 담당자용)

### What (무엇을)
[1-2 sentences: Extract from spec's Goal/목표 section or project description]
[Keep non-technical: avoid jargon, acronyms, technical terms]

### Why (왜)
[1-2 sentences: Problem statement or value proposition]
[Focus on business value or user benefit]

### Status (현재 상태)
- **전체 진행률** (Overall Progress): [X]%
  - Formula: (✅ count / (✅ + 🚧 + 📋 count)) * 100
- **완료된 기능** (Completed): [N]개
  - Count of ✅ markers
- **진행중인 기능** (In Progress): [M]개
  - Count of 🚧 markers
- **계획된 기능** (Planned): [K]개
  - Count of 📋 markers

---

## 🏗️ Architecture at a Glance (아키텍처 개요)

### Core Components (3-5 key components only)

[IF 2+ components: Generate ASCII diagram]
```
[Example structure:]
Frontend (React)
     |
     v
API Gateway ──> Auth Service
     |              |
     v              v
Database       Cache (Redis)
```

[IF 1 component: Skip diagram]

| Component | Purpose | Status |
|-----------|---------|--------|
| [Component Name] | [1 sentence: what it does] | [✅/🚧/📋 from spec] |
| [Component Name] | [1 sentence: what it does] | [✅/🚧/📋] |
| ... | ... | ... |

[RULES for component extraction:]
- Maximum 5 components
- Choose most important: user-facing, data layer, core logic
- Extract from "아키텍처 개요" or "컴포넌트 상세" section
- Simplify: group related modules into single component

### Tech Stack
- **Language** (언어): [Primary language from spec]
- **Framework** (프레임워크): [Main framework if any]
- **Key Libraries** (핵심 라이브러리): [Top 3 most important libraries]

[Extract from "환경 및 의존성" section]
[IF no dependency section: Mark as "Not specified"]

---

## 📊 Feature Status Dashboard

[Extract features from spec's Goal/목표 section]
[Group by status marker]

### Completed Features ✅
[IF no completed features: Show "- None yet"]
- **[Feature Name]** - [Brief description from spec or infer from name]
- **[Feature Name]** - [Brief description]
- ...

### In Progress 🚧
[IF no in-progress features: Show "- None currently"]
- **[Feature Name]** - [Brief description] [IF % known: "([X]% complete)"]
- **[Feature Name]** - [Brief description]
- ...

### Planned 📋
[IF no planned features: Show "- None scheduled"]
- **[Feature Name]** - [Brief description]
- **[Feature Name]** - [Brief description]
- ...

### On Hold ⏸️
[ONLY show this section IF ⏸️ markers exist]
[IF no on-hold features: OMIT this section entirely]
- **[Feature Name]** - [Brief description] (Reason: [Extract reason if available])
- ...

---

## ⚠️ Open Issues & Improvements (우선순위순)

[Extract from "발견된 이슈 및 개선 필요사항" section]
[Categorize by priority: High/Medium/Low]

[PRIORITY INFERENCE RULES:]
- High 🔴: "critical", "blocking", "urgent", "security", "data loss", "crash"
- Medium 🟡: "important", "performance", "usability", "should"
- Low 🟢: "nice-to-have", "enhancement", "refactor", "future"
[IF no keywords: Default to Medium]

### High Priority 🔴
[IF no high-priority items: Show "- No critical issues identified ✅"]

1. **[Issue/Improvement Title]** (Category: [Bug/Enhancement/Tech Debt])
   - **Impact** (영향): [Explain why this matters - user impact, business impact, technical impact]
   - **Location** (위치): [File path or component name if mentioned in spec]
   - **Suggested Fix** (해결 방안): [Brief suggestion if spec provides one, else "TBD"]

2. **[Next issue]**
   - ...

### Medium Priority 🟡
[IF no medium-priority items: Show "- No medium-priority items"]

[Same format as High Priority]

### Low Priority 🟢
[IF no low-priority items: Show "- No low-priority improvements"]

[Same format as High Priority]

---

## 🚀 Recommended Next Steps

[GENERATE based on current state analysis]

### 1. Immediate Actions (이번 주)

[LOGIC:]
- IF high-priority issues exist → "Fix [issue title]"
- IF features at 80%+ progress → "Complete [feature name]"
- IF blockers in IMPLEMENTATION_REVIEW.md → "Unblock [task]"
- IF no urgent items → "Continue current work"

- [ ] **[Action item with verb]** - [Why this matters / Expected outcome]
- [ ] **[Action item with verb]** - [Why this matters / Expected outcome]
- [ ] **[Action item with verb]** - [Why this matters / Expected outcome]

[Examples:]
- [ ] **Fix authentication timeout bug** - Blocks user login (high-priority issue)
- [ ] **Complete API endpoint tests** - Feature at 90%, last step for delivery
- [ ] **Review PR #123** - Waiting 2 days, blocks integration

### 2. Short-term Goals (이번 달)

[LOGIC:]
- IF planned features with no blockers → "Start implementing [feature]"
- IF medium-priority improvements → "Refactor [component]"
- IF tech debt accumulating → "Clean up [area]"
- IF testing gaps → "Add tests for [component]"

- [ ] **[Goal with measurable outcome]** - [Expected benefit]
- [ ] **[Goal with measurable outcome]** - [Expected benefit]

[Examples:]
- [ ] **Implement user profile page** - Next planned feature, dependencies ready
- [ ] **Optimize database queries** - Reduce API latency by 50%
- [ ] **Add integration tests** - Improve test coverage to 80%

### 3. Long-term Roadmap (분기/연간)

[LOGIC:]
- IF major planned features → "Milestone: [feature set] by [date]"
- IF architectural improvements → "Migrate to [new tech/pattern]"
- IF tech debt > 5 items → "Quarterly cleanup sprint"

- [ ] **[Milestone or major initiative]** - [Target: Q[N] YYYY]
- [ ] **[Milestone or major initiative]** - [Target: Q[N] YYYY]

[Examples:]
- [ ] **Launch mobile app** - Target: Q3 2026
- [ ] **Migrate to microservices architecture** - Target: Q4 2026
- [ ] **Achieve SOC 2 compliance** - Target: Q2 2026

---

## 📚 Quick Reference

### Key Files
[List actual file paths from project]
- **Spec Index** (메인 스펙): `_sdd/spec/<project>.md`
- **Sub-specs** (분할된 스펙, 선택): `_sdd/spec/<project>_API.md`, `_sdd/spec/<project>_DATA_MODEL.md`, ...
- **Implementation Plan** (구현 계획): `_sdd/implementation/IMPLEMENTATION_PLAN.md` [IF exists, else OMIT]
- **Implementation Progress** (구현 진행): `_sdd/implementation/IMPLEMENTATION_PROGRESS.md` [IF exists, else OMIT]
- **Implementation Progress (Latest Phase)** (구현 진행 - 최신 phase): `_sdd/implementation/IMPLEMENTATION_PROGRESS_PHASE_<n>.md` [IF exists, else OMIT]
- **Latest Review** (최근 리뷰): `_sdd/implementation/IMPLEMENTATION_REVIEW.md` [IF exists, else OMIT]

### Related Commands
- `/spec-update-todo` - Add new features to spec
- `/implementation-plan` - Create implementation plan from spec
- `/spec-update-done` - Sync spec with code changes
- `/spec-summary` - Regenerate this summary

---

**Summary 생성 방법**: `/spec-summary`를 실행하면 이 파일이 자동 생성/갱신됩니다.
**How to Generate**: Run `/spec-summary` to automatically create/update this file.
```

## Template Usage Guide

### Step 1: Read Spec
```bash
# List candidate spec files (exclude generated/backup files)
candidates=$(find _sdd/spec -path "*/prev/*" -prune -o -name "*.md" \
  -not -name "SUMMARY.md" \
  -not -name "PREV_*.md" \
  -print)

echo "$candidates"

# Prefer an index/main spec like: _sdd/spec/<project>.md
# If multiple candidates exist, choose explicitly (do NOT rely on `head -n 1`).
```

**If spec is split**: read the index spec first, then follow its links to `_sdd/spec/<project>_*.md` sub-specs.
Avoid guessing split files solely by globbing patterns; prefer **index/link-based discovery**.

### Step 2: Extract Metadata
```yaml
Project Name: [From # heading or filename]
Version: [From spec frontmatter or "목표" section]
Last Updated: [File mtime]
```

### Step 3: Parse Status
```bash
# Count markers in spec
completed=$(grep -c "✅" "$spec_file")
in_progress=$(grep -c "🚧" "$spec_file")
planned=$(grep -c "📋" "$spec_file")
on_hold=$(grep -c "⏸️" "$spec_file")

# Calculate percentage
total=$((completed + in_progress + planned))
if [ $total -gt 0 ]; then
  progress=$((completed * 100 / total))
else
  progress=0
fi
```

### Step 4: Extract Sections
```yaml
Goal: [Text after "## 목표" or "## Goal"]
Architecture: [Text after "## 아키텍처 개요" or "## Architecture Overview"]
Components: [Parse component names from architecture section]
Issues: [Text after "## 발견된 이슈" or "## Issues"]
Dependencies: [Text after "## 환경 및 의존성" or "## Dependencies"]
```

### Step 5: Prioritize Issues
```python
def prioritize(issue_text):
    high_keywords = ["critical", "blocking", "urgent", "security", "data loss", "crash"]
    low_keywords = ["nice-to-have", "enhancement", "refactor", "future"]

    text_lower = issue_text.lower()
    if any(kw in text_lower for kw in high_keywords):
        return "High"
    elif any(kw in text_lower for kw in low_keywords):
        return "Low"
    else:
        return "Medium"
```

### Step 6: Generate Recommendations
```python
recommendations = {
    "immediate": [],
    "short_term": [],
    "long_term": []
}

# Immediate (this week)
if high_priority_issues:
    recommendations["immediate"].append(f"Fix {high_priority_issues[0]}")
if in_progress_features_near_completion:
    recommendations["immediate"].append(f"Complete {feature_name}")

# Short-term (this month)
if planned_features_with_no_blockers:
    recommendations["short_term"].append(f"Start implementing {feature_name}")
if medium_priority_improvements:
    recommendations["short_term"].append(f"Improve {area}")

# Long-term (quarter/year)
if major_planned_features:
    recommendations["long_term"].append(f"Milestone: {feature_set} by Q{quarter}")
if tech_debt_count > 5:
    recommendations["long_term"].append("Quarterly tech debt cleanup sprint")
```

### Step 7: Apply Template
```markdown
Replace placeholders:
[Project Name] → extracted_project_name
[X]% → calculated_progress
[N]개 → counted_completed_features
... etc
```

### Step 8: Validate Output
```python
checklist = [
    "Executive summary is non-technical",
    "Architecture has 3-5 components max",
    "Status percentages are accurate",
    "Issues are categorized by priority",
    "Next steps are actionable and specific",
    "Conditional sections handled correctly"
]
```

## Common Pitfalls

| Pitfall | How to Avoid |
|---------|--------------|
| Too technical in executive summary | Use plain language, avoid jargon |
| Listing all components | Limit to 3-5 most important |
| Vague next steps | Make specific and time-bound |
| Wrong status calculation | Exclude ⏸️ from total count |
| Summarizing generated/backup files | Exclude `SUMMARY.md` and `prev/PREV_*.md` from spec inputs; pick the index spec explicitly |
| Missing split sub-specs | Prefer index/link-based discovery and read linked `_sdd/spec/<project>_*.md` files |
| Missing conditional sections | Check if data exists before adding section |
| Hardcoded file paths | Use actual project file paths |

## Quality Checklist

- [ ] Executive summary readable by non-developers
- [ ] Architecture shows only 3-5 core components
- [ ] Status percentages match marker counts
- [ ] All issues have priority assigned
- [ ] Next steps have timeframes (week/month/quarter)
- [ ] Conditional sections handled correctly
- [ ] No placeholder syntax left unreplaced
- [ ] File paths point to real files
- [ ] Language matches spec document
- [ ] Visual markers used consistently
