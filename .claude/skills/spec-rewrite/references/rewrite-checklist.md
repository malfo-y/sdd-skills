# Spec Rewrite Checklist

Checklist to reduce omissions during spec rewrite work.

## 1) Pre-Check

- [ ] Identify the main target spec file (`_sdd/spec/main.md` or `_sdd/spec/<project>.md`)
- [ ] Collect the list of linked sub-spec files
- [ ] Confirm backup policy (`_sdd/spec/prev/PREV_<filename>_<timestamp>.md`)
- [ ] Load `_sdd/spec/DECISION_LOG.md` if present
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
- **Component-level "Why" fields** (existence reason, design motivation — these are execution-critical, not supplementary rationale)
- Acceptance or completion criteria
- Link hub for sub-documents

## 3) Hierarchical Split Rules

- [ ] Index file: `_sdd/spec/<project>.md`
- [ ] Sub-directory: `_sdd/spec/<project>/`
- [ ] Consistent filename pattern using component/topic names directly (for example `api.md`, `database.md`, or `<component>/overview.md`)
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
- Decision-log additions (when rationale was moved out of main body)

## 5.5) Whitepaper Format Checks

- [ ] §1 Background & Motivation section exists (problem statement, approach rationale, core value)
- [ ] §2 Core Design section exists (key idea narrative, algorithm/logic flow, design rationale)
- [ ] §5 Usage Guide & Expected Results section exists (scenario-based usage with expected outcomes)
- [ ] Inline citations `[filepath:functionName]` are preserved and valid
- [ ] Code blocks with `# [filepath:functionName]` headers are intact
- [ ] Appendix: Code Reference Index is present and up-to-date (if code excerpts exist)
- [ ] If any whitepaper sections are missing, they are flagged in REWRITE_REPORT

## 6) Exit Criteria

- [ ] Core decisions are understandable from the main index alone
- [ ] Detailed content is discoverable through topic-based sub-files
- [ ] Cross-document duplication is minimized
- [ ] Unresolved ambiguities remain explicitly documented
- [ ] Essential rationale is preserved in `_sdd/spec/DECISION_LOG.md` when removed from main spec
- [ ] Component-level Why fields are preserved inline (not moved to DECISION_LOG or appendix)
- [ ] Whitepaper narrative sections (§1, §2, §5) are preserved inline (not pruned to appendix)
- [ ] Inline citations and code excerpt headers are intact after restructuring
