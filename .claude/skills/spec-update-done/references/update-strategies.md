# Spec Update Strategies

Different strategies for updating spec documents based on the type and scope of changes.

---

## Strategy Selection Matrix

| Scenario | Strategy | Time | Risk |
|----------|----------|------|------|
| Bug fix, no behavior change | Skip Update | 0 | None |
| Minor config change | Patch Update | 5 min | Low |
| New feature added | Section Update | 30 min | Low |
| API changes | Versioned Update | 1 hr | Medium |
| Architecture change | Full Rewrite | 2+ hr | High |
| Major refactor | Staged Update | Multi-session | Medium |

---

## 1. Skip Update Strategy

**When to Use:**
- Internal refactoring with no external changes
- Bug fixes that don't change documented behavior
- Code style/formatting changes
- Test additions only

**Actions:**
- No spec changes needed
- Optionally update "Last Reviewed" date
- Note in changelog only if significant

---

## 2. Patch Update Strategy

**When to Use:**
- Minor version bumps in dependencies
- Small configuration changes
- Typo fixes in code that affect docs
- Adding missing details

**Process:**
```
1. Identify specific line(s) to change
2. Make targeted edit
3. Increment patch version (X.Y.Z → X.Y.Z+1)
4. Update "Last Updated" date
5. No changelog entry needed
```

**Example:**
```markdown
# Before
Python 3.10+

# After
Python 3.11+
```

---

## 3. Section Update Strategy

**When to Use:**
- New feature implemented
- Component behavior changed
- New configuration options
- Additional usage examples

**Process:**
```
1. Identify affected section(s)
2. Read current content
3. Draft updates preserving structure
4. Add new subsections if needed
5. Update cross-references
6. Increment minor version (X.Y.Z → X.Y+1.0)
7. Add changelog entry
```

**Template for New Feature:**
```markdown
### New: [Feature Name]

**Added in version X.Y.0**

[Description of feature]

**Usage:**
```code
example
```

**Configuration:**
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| ... | ... | ... | ... |
```

---

## 4. Versioned Update Strategy

**When to Use:**
- Breaking API changes
- Removed features
- Changed data formats
- Migration required

**Process:**
```
1. Document the breaking change clearly
2. Provide migration guide
3. Update all affected sections
4. Increment major version (X.Y.Z → X+1.0.0)
5. Create detailed changelog entry
6. Consider maintaining version branches
```

**Migration Guide Template:**
```markdown
## Migration from vX to vY

### Breaking Changes

1. **[Change Name]**
   - Before: [old behavior]
   - After: [new behavior]
   - Migration: [steps to migrate]

### Deprecated Features

| Feature | Replacement | Removal Version |
|---------|-------------|-----------------|
| ... | ... | ... |

### New Requirements

- [New dependency or requirement]
```

---

## 5. Full Rewrite Strategy

**When to Use:**
- Major architecture change
- Spec significantly out of sync
- Project pivot or redesign
- Initial documentation of legacy code

**Process:**
```
1. Archive current spec as `_sdd/spec/prev/PREV_<name>_<date>.md`
2. Start fresh using template
3. Analyze current codebase thoroughly
4. Document actual state (not planned)
5. Have user review before finalizing
6. Reset version to 1.0.0 or increment major
```

**Rewrite Checklist:**
- [ ] All components documented
- [ ] All APIs documented
- [ ] All config options listed
- [ ] Examples tested and working
- [ ] Architecture diagram current
- [ ] Dependencies accurate
- [ ] Issues list current

---

## 6. Staged Update Strategy

**When to Use:**
- Large ongoing refactor
- Phased migration
- Multiple related changes over time
- Team collaboration on docs

**Process:**
```
Phase 1: Mark sections as "Under Review"
Phase 2: Update completed sections incrementally
Phase 3: Remove "Under Review" markers
Phase 4: Final review and version bump
```

**Section Markers:**
```markdown
> ⚠️ **Under Review**: This section is being updated.
> Last accurate version: v2.3.0

[Current content - may be outdated]

> 📝 **Proposed Update** (PR #123):
> [New content preview]
```

---

## Update Workflow

### Pre-Update

1. **Backup**
   ```bash
   spec_file="_sdd/spec/<spec-file>.md"
   mkdir -p _sdd/spec/prev
   cp "$spec_file" "_sdd/spec/prev/PREV_<spec-file>_$(date +%Y%m%d_%H%M%S).md"
   ```

2. **Review Inputs**
   - Implementation logs
   - Git history
   - User feedback
   - Code analysis

3. **Plan Changes**
   - List sections to update
   - Identify dependencies
   - Estimate scope

### During Update

1. **Preserve Structure**
   - Keep existing organization
   - Maintain formatting conventions
   - Follow established patterns

2. **Update Content**
   - Be precise and accurate
   - Include code references
   - Test examples

3. **Track Changes**
   - Note what changed
   - Document reasoning
   - Flag uncertainties

### Post-Update

1. **Validate**
   - All links work
   - Examples run
   - Cross-references valid

2. **Version**
   - Update version number
   - Update date
   - Add changelog entry

3. **Review**
   - Self-review changes
   - User review if significant
   - Address feedback

---

## Changelog Format

### Standard Entry
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature X in Component Y

### Changed
- Updated API endpoint from /old to /new
- Modified default value for config Z

### Deprecated
- Feature A (use B instead)

### Removed
- Unused component C

### Fixed
- Corrected example in section D
- Fixed broken link to E

### Security
- Updated dependency F for CVE-XXXX
```

### Compact Entry
```markdown
## [X.Y.Z] - YYYY-MM-DD
- Updated Python requirement to 3.11+
- Added new `--verbose` flag documentation
- Fixed example in Usage section
```

---

## Handling Conflicts

### Spec vs Code Conflict

**Scenario:** Spec says X, code does Y

**Resolution Options:**
1. **Update Spec** - If code is correct/intended
2. **File Bug** - If spec is correct, code is wrong
3. **Ask User** - If intent is unclear

### Spec vs User Feedback Conflict

**Scenario:** User says X, spec says Y

**Resolution Options:**
1. **Clarify** - Understand user's actual need
2. **Update Spec** - If user identified error
3. **Explain** - If spec is correct but unclear

### Multiple Sources Conflict

**Scenario:** Implementation log says X, code shows Y, user wants Z

**Resolution:**
1. Code is truth for "what is"
2. User input is truth for "what should be"
3. Logs are history for "what was planned"
4. Document current state, note planned changes

---

## Quality Checklist

### Accuracy
- [ ] All statements verifiable in code
- [ ] Examples produce documented output
- [ ] Version numbers match reality
- [ ] File paths exist

### Completeness
- [ ] All public APIs documented
- [ ] All config options listed
- [ ] All components described
- [ ] All known issues noted

### Clarity
- [ ] No ambiguous statements
- [ ] Technical terms defined
- [ ] Examples for complex features
- [ ] Clear section hierarchy

### Maintainability
- [ ] Consistent formatting
- [ ] Modular structure
- [ ] Clear update process
- [ ] Version history maintained
