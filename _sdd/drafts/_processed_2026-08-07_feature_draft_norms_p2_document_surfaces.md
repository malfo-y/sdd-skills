# Feature Draft: norms P2 document surfaces

> 규모 판정: 적격 — 세 독립 document producer를 task별로 수정하고 마지막 22-path census로 묶는다. 실제 수정은 SKILL 6개·rich reference 4개이며 나머지 12개는 중복 asset 삭제라 단일 컨텍스트에서 검증 가능하다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

**norms-p2-document-surfaces (current)** — `spec-summary`와 `guide-create`는 실제 output template/reference 한 곳만 format을 소유하고 작성 직전에 읽어 기계적으로 적용한다. `spec-snapshot`은 두 runtime 계약을 하나로 맞추고 source manifest·destination collision·source `summary.md` 병합 규칙으로 보존 경계를 결정적으로 만든다. 세 스킬의 runtime helper lifecycle·임의 size threshold·중복 example/schema를 제거하고 main loop가 직접 작성·검증한다.

판단 근거: 세 스킬은 모두 문서 산출 producer이고, 문제는 output shape의 이중 홈과 runtime별 orchestration 설명 drift다. 새 helper나 reference를 만들지 않고 existing rich reference를 단독 홈으로 남기며, snapshot은 reference가 없어 본문의 짧은 interface를 정본으로 둔다.

## Scope

- **In**: Claude/Codex `spec-summary`·`spec-snapshot`·`guide-create`; summary/guide point-of-use template load; duplicate examples/reference deletion; snapshot source/destination manifest and collision rules; runtime semantic parity; validator/norms census
- **Out**: 실제 summary/snapshot/guide 생성, output-format 대규모 재설계, 번역 엔진·언어 감지 구현, README content 변경, P0/P1 skill 변경
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | summary output shape single home | `.claude/skills/spec-summary/SKILL.md`<br>`.codex/skills/spec-summary/SKILL.md`<br>`.claude/skills/spec-summary/references/summary-template.md`<br>`.codex/skills/spec-summary/references/summary-template.md`<br>`.claude/skills/spec-summary/examples/summary-output.md`<br>`.codex/skills/spec-summary/examples/summary-output.md` | `rg -n 'references/summary-template\.md|examples/summary-output\.md' <two SKILLs>` → template 4, example 2; current template has fence 0 and literal management heading `# Summary Template` | Task 1 |
| P2 | snapshot preservation interface | `.claude/skills/spec-snapshot/SKILL.md`<br>`.codex/skills/spec-snapshot/SKILL.md`<br>consumer branch `_sdd/spec/summary.md` present/absent | `diff -u <Claude> <Codex>` → semantic diff; `rg -n 'user_invocable|동일 타임스탬프|summary\.md|모든 .*\.md' <two SKILLs>` exposes runtime metadata, overwrite/collision, and copy-all claims | Task 2 |
| P3 | guide format single home | `.claude/skills/guide-create/SKILL.md`<br>`.codex/skills/guide-create/SKILL.md`<br>`.claude/skills/guide-create/references/{output-format,template-compact,tool-and-gates}.md`<br>`.codex/skills/guide-create/references/{output-format,template-compact,tool-and-gates}.md`<br>`.claude/skills/guide-create/examples/feature-guide-example{,-high,-low}.md`<br>`.codex/skills/guide-create/examples/feature-guide-example{,-high,-low}.md` | `wc -l <six examples>` → physical 1,714 lines / semantic unique trio 857; `rg -n '§4 Verification Notes|§4 API 레퍼런스|template-compact|AskUserQuestion|request_user_input' <guide surfaces>` proves schema/tool drift | Task 3 |
| P4 | runtime/parity and deletion census | exact M10+D12 target list in Tasks 1–3 | `git rev-parse HEAD` → `8679235`; pre-draft status clean, implementation-start full status is goal journal/work log `M` + this draft `??`; all six SKILL pairs differ before normalization, guide format and summary template pairs are exact | Task 4 |

# Part 2: Tasks

### Task 1: spec-summary의 whitepaper shape를 template 한 곳으로 모은다

`summary-template.md`를 output structure의 단독 정본으로 유지하고 SKILL은 입력·판단·load/apply 계약만 소유한다.

**Contracts**:

- Step 6 작성 직전에 runtime-local `references/summary-template.md`를 Read하고 fenced output skeleton만 verbatim 복사해 title/heading/order를 유지한다. 확인한 evidence로 slot을 채우고 관련 current artifact가 없으면 optional appendix를 제거한다.
- SKILL은 canonical section 목록을 다시 열거하지 않고 template을 가리킨다. 완성 example은 interface를 재소유하므로 두 runtime에서 삭제한다.
- summary는 current whitepaper이며 change history는 본문에 넣지 않는다. planned/progress는 관련 current draft/ledger가 있을 때만 appendix에 둔다.
- lowercase `decision_log.md`가 canonical이고 uppercase는 read-only fallback이다. current implementation evidence glob은 `*_implementation_ledger_*.md`를 사용한다.
- README는 명시 요청 때만 managed block을 수정한다. 본 스킬의 작성은 main loop가 직접 수행하고 runtime helper lifecycle을 정의하지 않는다. 장문이면 main loop가 fenced skeleton을 먼저 저장하고 section slot을 하나씩 채운 뒤 placeholder를 제거해 finalize한다.

**Acceptance Criteria**:

- [ ] AC1: 두 SKILL이 byte-exact이고 `references/summary-template.md` path는 Step 6에 각 1건, 다른 section에 0건이다. template pair는 byte-exact이고 fenced block 1개·output title slot 1개·six required heading + optional appendix 순서를 포함한다.
- [ ] AC2: 두 SKILL은 six section-name canonical list·`Bounded Helper Lifecycle|Mailbox \(Desktop|Target/close|tool_search`를 0건 포함하고, point-of-use Read·fenced-skeleton verbatim·evidence slot fill·optional appendix condition·main-loop skeleton-first를 각 1회 소유한다.
- [ ] AC3: lowercase decision log + uppercase fallback, current draft/implementation ledger appendix input, README explicit-only, current-not-history criterion을 section-aware assertion한다.
- [ ] AC4: two `examples/summary-output.md`가 삭제되고 SKILL/reference 어디에도 그 path가 남지 않는다.

**Target Files**:

- [M] `.claude/skills/spec-summary/SKILL.md` — concise producer owner
- [M] `.codex/skills/spec-summary/SKILL.md` — exact mirror
- [M] `.claude/skills/spec-summary/references/summary-template.md` — fenced output interface canonical
- [M] `.codex/skills/spec-summary/references/summary-template.md` — exact mirror
- [D] `.claude/skills/spec-summary/examples/summary-output.md` — duplicate example
- [D] `.codex/skills/spec-summary/examples/summary-output.md` — duplicate mirror

### Task 2: spec-snapshot의 source 보존과 output collision을 닫는다

두 runtime을 한 계약으로 맞추고 snapshot 전후를 source/destination manifest로 검증한다.

**Contracts**:

- 시작 시 `_sdd/spec/` 아래 sorted relative `.md` path + SHA-256 manifest를 기록하고, 완료 후 source manifest exact match를 hard gate로 확인한다.
- 표시 언어와 filesystem `lang-slug`를 분리한다. slug는 lowercase ASCII 영문·숫자와 단일 `_`만 허용하고 빈 결과는 `lang`으로 fallback한다. destination은 local `YYYY-MM-DDTHH-MM_<lang-slug>`을 쓰되 이미 존재하면 `-02`, `-03` 순의 첫 unused suffix를 고르며, resolved parent가 resolved `_sdd/snapshots/`와 exact match해야 한다.
- 모든 source `.md` relative path를 destination에 보존한다. 대상 언어가 같으면 root `summary.md`를 제외한 파일은 bytes를 복사한다. 번역은 Markdown structure/code/path/symbol/command/config token과 함께 target-language coverage·source-to-target semantic fidelity·material omission/addition 없음으로 검증한다.
- destination `summary.md`는 아래 exact marker block을 파일 맨 앞에 1개 소유한다. source에 `summary.md`가 있으면 end marker 뒤 `\n\n` 다음 body가 same-language에서는 source bytes와 exact match하고, translation에서는 source heading/code/path 구조를 보존한 translated body다. source summary에 reserved start/end delimiter가 이미 있으면 destination 생성 전에 실패한다. source summary가 없으면 marker 뒤에 Project Overview/Components/Open Questions를 생성한다.

```markdown
<!-- SPEC-SNAPSHOT-METADATA:START -->
- **Source**: `_sdd/spec/`
- **Snapshot**: `<destination>`
- **Language**: `<lang>`
- **Created**: `<local timestamp>`
- **Source Commit**: `<short hash>`
<!-- SPEC-SNAPSHOT-METADATA:END -->
```
- main loop가 file list를 bounded batch로 직접 처리한다. runtime helper lifecycle, tool schema, arbitrary batch-count instruction은 두 SKILL에 두지 않는다.

**Acceptance Criteria**:

- [ ] AC5: 두 SKILL은 common frontmatter+body normalization 후 exact다. Claude의 `user_invocable: true`만 runtime allowlist delta로 보존하고 Codex에는 0건이며, 그 밖의 frontmatter/body delta와 runtime helper schema는 0건이다.
- [ ] AC6: source pre/post manifest hard gate와 destination relative-path coverage를 assertion한다. same-language에서 root summary 외 파일은 byte-exact이고, source summary present branch는 exact marker를 제거한 body SHA-256이 source와 일치하며, translation branch는 structure/token + target-language coverage + semantic fidelity rubric으로 닫힌다.
- [ ] AC7: safe `lang-slug` regex와 resolved direct-parent confinement, directory collision suffix, source-summary present/absent 두 branch가 disjoint/exhaustive다. exact metadata marker pair·고정 5필드·blank-line delimiter의 occurrence/count, reserved-marker preflight failure, body preservation checker를 명시한다.
- [ ] AC8: `Bounded Helper Lifecycle|Mailbox \(Desktop|Target/close|tool_search|2-4개 batch|독립 파일 2개 이상이면 병렬` census가 두 파일에서 0건이고, duplicate Hard Rule/AC/Output restatement 없이 process owner가 한 곳이다.

**Target Files**:

- [M] `.claude/skills/spec-snapshot/SKILL.md` — preservation interface canonical mirror
- [M] `.codex/skills/spec-snapshot/SKILL.md` — exact mirror

### Task 3: guide-create의 output-format만 rich reference로 남긴다

`output-format.md`가 schema·section rubric·confidence를 단독 소유하고 SKILL은 언제 읽고 어떻게 적용할지만 남긴다.

**Contracts**:

- Step 5 작성 직전에 runtime-local `references/output-format.md`를 Read한다. fenced required structure를 verbatim 복사하고 source evidence로 slot을 채우며 근거 없는 optional appendix는 제거한다.
- output-format은 자신에게 없는 `template-compact` Writing Rules pointer를 제거하고, citation/evidence/unsupported-claim 원칙을 자기 `Writing Rules`에 직접 고정한다.
- SKILL에서 §1–§5 schema, confidence rubric, citation excerpt detail을 재열거하지 않는다. output path와 feature/scope question criterion만 남긴다.
- `template-compact`, `tool-and-gates`, High/Medium/Low examples는 stale·pseudo-code·format duplicate라 두 runtime에서 삭제한다. arbitrary `related_files` threshold와 helper tool schema도 제거한다.
- usable spec/code evidence가 부족해 target feature 또는 guide scope가 바뀔 때만 질문 1회를 요청하고, 그 외에는 assumption/unknown을 표시해 계속한다.
- 장문 guide는 main loop가 output-format skeleton을 먼저 저장하고 section slot을 순차 fill한 뒤 placeholder를 제거한다. 복수 feature는 파일별로 하나를 finalize한 다음 다음 파일로 간다.

**Acceptance Criteria**:

- [ ] AC9: 두 SKILL exact mirror; `references/output-format.md` path는 Step 5에 각 1건이고 Companion/References/Output에 0건이다. required section literal·confidence enum·citation detail은 SKILL에서 0건이고 output-format pair에만 존재한다.
- [ ] AC10: 두 output-format이 byte-exact이며 `template-compact.md` pointer 0, `Writing Rules`에 source-grounded citation·unsupported claim/assumption·verbatim skeleton apply 기준을 포함한다. section rubric은 최소 excerpt와 evidence-conditional scenario criterion을 소유하고 고정 line-count·scenario-count recipe는 0건이다.
- [ ] AC11: 두 SKILL은 target/scope-changing ambiguity question criterion, per-feature sequential output, spec/code read-only, evidence gathering, point-of-use Read, verbatim/slot-only apply, main-loop skeleton-first를 포함하고 `related_files|AskUserQuestion|request_user_input|Bounded Helper Lifecycle|Mailbox \(Desktop|Target/close|tool_search`는 0건이다.
- [ ] AC12: two `template-compact.md`, two `tool-and-gates.md`, six example files가 삭제되고 exact four surviving guide files(two SKILL + two output-format)에서 deleted path/basename 잔존이 0건이다. baseline은 physical 10 deleted paths = reference 260 lines + example 1,714 lines로 기록한다.

**Target Files**:

- [M] `.claude/skills/guide-create/SKILL.md` — concise producer owner
- [M] `.codex/skills/guide-create/SKILL.md` — exact mirror
- [M] `.claude/skills/guide-create/references/output-format.md` — sole rich output interface
- [M] `.codex/skills/guide-create/references/output-format.md` — exact mirror
- [D] `.claude/skills/guide-create/references/template-compact.md` — stale schema owner
- [D] `.codex/skills/guide-create/references/template-compact.md` — stale mirror
- [D] `.claude/skills/guide-create/references/tool-and-gates.md` — duplicated pseudo gates
- [D] `.codex/skills/guide-create/references/tool-and-gates.md` — duplicated mirror
- [D] `.claude/skills/guide-create/examples/feature-guide-example.md` — duplicate output example
- [D] `.codex/skills/guide-create/examples/feature-guide-example.md` — duplicate mirror
- [D] `.claude/skills/guide-create/examples/feature-guide-example-high.md` — duplicate confidence example
- [D] `.codex/skills/guide-create/examples/feature-guide-example-high.md` — duplicate mirror
- [D] `.claude/skills/guide-create/examples/feature-guide-example-low.md` — duplicate confidence example
- [D] `.codex/skills/guide-create/examples/feature-guide-example-low.md` — duplicate mirror

### Task 4: P2 target·mirror·norms를 read-only로 검증한다

**Acceptance Criteria**:

- [ ] AC13: ledger가 base `8679235`, pre-draft clean evidence, implementation-start full status exact set(goal journal/work log `M` 2건 + draft `??` 1건), six SKILL pre-hash, guide output-format pair raw pre-hash, deleted guide asset 10개 line census를 기록한다. post-minus-initial status가 exact M10+D12 target paths이고 whole-worktree 추가분은 그 22개뿐이다.
- [ ] AC14: exact command `/Users/hyunjoonlee/miniconda3/bin/python3 /Users/hyunjoonlee/.codex/skills/.system/skill-creator/scripts/quick_validate.py <dir>`가 Claude snapshot을 제외한 five dirs에서 5/5 `Skill is valid!`; Claude snapshot은 YAML parser로 common keys + `user_invocable: true` delta와 normalized-body parity를 확인해 `CLAUDE_SNAPSHOT_SCHEMA_PASS`를 출력한다. summary/guide SKILL exact 2/2, snapshot normalized 1/1, summary template exact, guide output-format exact, deleted asset 12/12를 함께 출력한다.
- [ ] AC15: reviewer가 norms §3.1 six rows + §3.2 three rows + §3.3 three rows + §3.4 two rows, 총 14개 checklist item 각각에 target citation과 `MET|NOT MET`를 반환해 `NORMS_PASS 14/14`를 출력한다. 별도 hard-gate row는 snapshot manifest와 read-only preservation을 검증한다. NOT MET는 unresolved AC다.
- [ ] AC16: Python zero-match checker가 exact six SKILL array에서 `Bounded Helper Lifecycle|Mailbox \(Desktop|Target/close|tool_search|related_files` count 0을 `P2_STALE_RUNTIME_ZERO_PASS 6/6`으로 출력하고 `git diff --check`가 exit 0이다. raw `rg` exit 1은 zero-match 성공으로 해석한다.

**Target Files**:

- 없음 (read-only 검증)
