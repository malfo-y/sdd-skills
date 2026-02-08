# Spec Rewrite Checklist

Checklist to reduce omissions during spec rewrite work.

## 1) Pre-Check

- [ ] Identify the main target spec file (`_sdd/spec/main.md` or `_sdd/spec/<project>.md`)
- [ ] Collect the list of linked sub-spec files
- [ ] Confirm backup policy (`_sdd/spec/prev/PREV_<filename>_<timestamp>.md`)
- [ ] Confirm with the user before large-scale file splitting

## 2) Prune / Appendix Decision Rules

Prioritize moving these items to appendix:

- Long execution logs or historical records
- Overly long code blocks used only as detailed examples
- Legacy explanation with low impact on current decisions
- Repeated tables or checklists in the main body

Keep these items in the main index:

- Goal, Scope, and Non-Goals
- Core architecture summary
- Primary component responsibilities
- Acceptance or completion criteria
- Link hub for sub-documents

## 3) Hierarchical Split Rules

- [ ] Index file: `_sdd/spec/<project>.md`
- [ ] Sub-directory: `_sdd/spec/<project>/`
- [ ] Consistent filename pattern (`01-overview.md`, `02-architecture.md`, ...)
- [ ] Each sub-file follows single-topic responsibility
- [ ] Every sub-file is reachable from the index
- [ ] Zero broken links

## 4) Ambiguity Detection Checklist

- [ ] Requirements without measurable criteria (for example: "quickly", "appropriately")
- [ ] Conflicting rules or procedures
- [ ] Missing exception or failure scenarios
- [ ] Undefined terms or abbreviations
- [ ] Unclear ownership (team/component responsibility)
- [ ] Missing acceptance criteria

## 5) Report Structure

Include at least the following in `_sdd/spec/REWRITE_REPORT.md`:

- Target document and execution timestamp
- Removed/moved-to-appendix items with rationale
- File split map
- Ambiguities and issues list
- Priority-based recommended resolutions

## 6) Exit Criteria

- [ ] Core decisions are understandable from the main index alone
- [ ] Detailed content is discoverable through topic-based sub-files
- [ ] Cross-document duplication is minimized
- [ ] Unresolved ambiguities remain explicitly documented
