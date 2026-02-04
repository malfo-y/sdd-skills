# Common Spec Drift Patterns

This document describes common patterns of spec drift and how to detect and resolve them.

---

## 1. Architecture Drift

### Pattern: Undocumented Components

**Detection:**
```bash
# Find new Python modules not in spec
find src -name "*.py" -type f | grep -v __pycache__ | sort > actual_modules.txt
# Compare against spec's component list
```

**Symptoms:**
- New directories in `src/` not mentioned in spec
- Import statements referencing undocumented modules
- New service/class definitions

**Resolution:**
- Add new component section to spec
- Document purpose, interface, dependencies
- Update architecture diagram

### Pattern: Removed Components

**Detection:**
```bash
# Check if documented files still exist
grep -oP 'src/[a-zA-Z_/]+\.py' spec.md | while read f; do
  [ ! -f "$f" ] && echo "Missing: $f"
done
```

**Symptoms:**
- Spec references files that don't exist
- Import errors when following spec
- Dead links in documentation

**Resolution:**
- Remove or archive component section
- Update architecture diagram
- Note removal in changelog

### Pattern: Changed Dependencies

**Detection:**
```bash
# Compare spec dependencies vs actual
diff <(grep -oP '\w+==[\d.]+' spec.md | sort) \
     <(pip freeze | sort)
```

**Symptoms:**
- Version mismatches
- New packages not documented
- Removed packages still listed

**Resolution:**
- Update dependency table
- Note breaking changes
- Document migration if needed

---

## 2. Feature Drift

### Pattern: Implemented but Undocumented

**Detection:**
- Review IMPLEMENTATION_PROGRESS.md for completed tasks
- Check git log for feature commits
- Look for new API endpoints

**Symptoms:**
- Features work but aren't in spec
- Users discover undocumented capabilities
- Test files reference unknown features

**Resolution:**
- Add feature to spec
- Document API/interface
- Add usage examples

### Pattern: Planned but Not Implemented

**Detection:**
- Cross-reference spec features with code
- Check for stub implementations
- Review test coverage

**Symptoms:**
- Spec describes features that don't work
- Tests fail for documented features
- Users report missing functionality

**Resolution:**
- Mark as "Planned" or "Not Implemented"
- Move to "Missing Features" section
- Update status indicators

### Pattern: Behavior Changes

**Detection:**
- Compare spec examples with actual output
- Review test changes
- Check error message changes

**Symptoms:**
- Examples in spec don't work
- Different output format than documented
- Changed error handling

**Resolution:**
- Update examples and descriptions
- Document breaking changes
- Note migration steps if needed

---

## 3. API Drift

### Pattern: Endpoint Changes

**Detection:**
```bash
# Extract routes from code
grep -r "@app\.\(get\|post\|put\|delete\)" src/ | \
  grep -oP '"/[^"]+' | sort
# Compare with spec's API section
```

**Symptoms:**
- 404 errors following spec
- Different URL patterns
- Changed HTTP methods

**Resolution:**
- Update API reference section
- Document old → new mapping
- Note deprecations

### Pattern: Request/Response Schema Changes

**Detection:**
- Compare Pydantic models with spec
- Run API tests against spec examples
- Check OpenAPI/Swagger if available

**Symptoms:**
- Validation errors with spec examples
- Missing required fields
- Changed field types

**Resolution:**
- Update schema documentation
- Provide migration examples
- Version the API if breaking

---

## 4. Configuration Drift

### Pattern: New Environment Variables

**Detection:**
```bash
# Find env var usage in code
grep -rhoP 'os\.environ\[?\.?get\(?"(\w+)"' src/ | sort -u
grep -rhoP 'settings\.(\w+)' src/ | sort -u
# Compare with spec's config section
```

**Symptoms:**
- App fails with missing config
- Undocumented settings affect behavior
- Defaults not matching spec

**Resolution:**
- Add to environment variables table
- Document defaults and valid values
- Update .env.example

### Pattern: Changed Defaults

**Detection:**
- Compare default values in code vs spec
- Review config class definitions
- Check recent commits to config files

**Symptoms:**
- Different behavior than documented
- Users confused by unexpected defaults
- Tests assume wrong values

**Resolution:**
- Update default values in spec
- Note behavioral implications
- Document upgrade path

---

## 5. Issue Drift

### Pattern: Resolved Issues Still Listed

**Detection:**
- Cross-reference issues with git log
- Check PR/commit messages
- Review test additions

**Symptoms:**
- Fixed bugs still in "Known Issues"
- Completed improvements still pending
- Outdated status information

**Resolution:**
- Move to "Resolved" or remove
- Add to changelog
- Update status indicators

### Pattern: New Issues Not Documented

**Detection:**
- Review IMPLEMENTATION_REVIEW.md
- Check TEST_SUMMARY.md for failures
- Look for TODO/FIXME comments

```bash
grep -rn "TODO\|FIXME\|XXX\|HACK" src/
```

**Symptoms:**
- Known problems not in spec
- Test failures not documented
- Technical debt accumulating silently

**Resolution:**
- Add to "Identified Issues" section
- Categorize by severity
- Link to relevant code locations

---

## 6. Documentation Drift

### Pattern: Stale Examples

**Detection:**
- Run examples from spec
- Compare output with expected
- Check file paths still exist

**Symptoms:**
- Examples fail or produce different output
- Referenced files moved or deleted
- Outdated command syntax

**Resolution:**
- Update or replace examples
- Test all code snippets
- Add output verification comments

### Pattern: Broken Links

**Detection:**
```bash
# Find internal links
grep -oP '\[.*?\]\(\.?/?[^)]+\)' spec.md | \
  grep -oP '\([^)]+\)' | tr -d '()' | \
  while read link; do
    [ ! -f "$link" ] && echo "Broken: $link"
  done
```

**Symptoms:**
- 404 when clicking links
- References to moved content
- Outdated cross-references

**Resolution:**
- Fix or remove broken links
- Update paths after restructuring
- Add link validation to CI

---

## Detection Checklist

### Quick Review (5 minutes)
- [ ] `git status` - any uncommitted changes?
- [ ] `git log --oneline -10` - recent changes?
- [ ] Key files exist as documented?
- [ ] Main entry point works?

### Standard Review (30 minutes)
- [ ] All components in spec exist in code
- [ ] All code components documented in spec
- [ ] Dependencies match
- [ ] API endpoints match
- [ ] Config options documented
- [ ] Examples work

### Deep Review (2+ hours)
- [ ] Full architecture comparison
- [ ] All features tested against spec
- [ ] Issue status verified
- [ ] Performance claims validated
- [ ] Security considerations current
- [ ] Deployment docs accurate

---

## Resolution Priority

| Drift Type | User Impact | Priority |
|------------|-------------|----------|
| API breaking changes | High | P0 - Immediate |
| Missing features | High | P1 - Same day |
| Wrong examples | Medium | P2 - This week |
| Config changes | Medium | P2 - This week |
| Resolved issues | Low | P3 - When convenient |
| Style/formatting | Low | P4 - Batch updates |
