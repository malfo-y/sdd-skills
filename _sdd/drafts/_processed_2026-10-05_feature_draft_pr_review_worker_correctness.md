# Feature Draft: pr-review correctness를 worker dispatch로 전환

> 규모 판정: 적격 — 변경 요소 11종이 task 6개에 1:1로 배정되고 전부 문서 편집이다. "메인 루프 직접"류 표기가 claude/codex 짝 5파일에 흩어진 census형 신호가 있어 read-only 검증 task를 마지막에 둔다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

`pr-review`의 correctness 리뷰를 메인 루프 직접 수행에서 범용 worker dispatch로 옮긴다. 메인은 PR 번호·baseline SHA(`headRefOid`)·PR 메타데이터·Changed Files·spec 존재 상태(FOUND/ABSENT/UNREADABLE)·리포트 slug만 모으고, correctness·simplicity worker 둘이 같은 SHA로 PR diff·코드·spec을 직접 읽는다. 메인은 두 반환으로 verdict를 합성하고 통합 리포트 하나를 쓴다(단일 작성자 불변). 기존 결정 "pr-review는 호출 때 지정만"(main.md)과 "correctness는 메인 루프 직접 수행"을 대체한다.

새 contract/invariant:
- correctness 계약의 단일 소스는 `pr-review/references/correctness-contract.md`(claude/codex 동일본)다. worker가 경로를 Read해 따르고 SKILL.md에는 계약을 두지 않는다. simplicity는 기존 `sdd-orchestrator/references/simplicity-contract.md` 전문 verbatim 주입·4차원 worker 1개를 유지한다.
- `PR Review Input` 필드는 `PR`·`Baseline`·`Changed Files`·`Spec Status`·`Relevant Context`다. `PR Diff` 필드는 없다 — 두 worker가 `gh pr diff <PR>`로 직접 수집하고 `headRefOid`가 Baseline과 같음을 재확인한다(불일치면 BLOCKED 반환; 메인은 새 SHA로 다시 고정해 두 worker를 1회 다시 띄우고, 또 불일치면 제한 리포트로 닫는다).
- pr-review worker 모델 결정 순서: 호출 `--model`(Codex는 `--effort`도) > `_sdd/env.md` `## Worker Model Defaults`의 `pr-review` 행 > 런타임 기본. 적용값은 correctness·simplicity 두 dispatch에 같게 적용한다. 검증은 `sdd-orchestrator`와 같다(Claude 허용값 `sonnet`·`opus`·`haiku`·`fable`, Codex는 선택한 spawn schema enum).
- `## Worker Model Defaults` 표는 다섯 단계 행 + `pr-review` 행을 가진다. `sdd-orchestrator`는 다섯 단계 행만 읽고 다른 행은 무시한다. 이 저장소 값: Claude `opus`, Codex `gpt-6.1-sol`/`high`. spec-create·spec-upgrade 부트스트랩 템플릿은 `pr-review` 빈 행을 포함한다.
- Fresh Verification(CI output 결속·local 검증 실행)은 correctness worker 소관이다. 메인은 테스트를 실행하지 않는다.

spec 반영 대상(spec-sync 단계 소유, 이 draft의 Target Files 아님): `_sdd/spec/main.md` — "직교 2-렌즈 review의 적용 지점…" 집행 규칙 bullet(문장 "correctness를 CI → … 직접 수행한다"), "subagent 모델 override는 `pr-review`의 simplicity dispatch와…" bullet과 그 아래 `pr-review` Claude/Codex 하위 bullet 2개, §3 비교표 `실행 분리`·`직교 2-렌즈 review 렌즈`·`subagent model override` 행; `_sdd/spec/components.md` — `pr-review` 컴포넌트 행, `Claude skill/agent split` 행, `Simplicity 계약 reference` 행; `_sdd/spec/decision_log.md`·`_sdd/spec/logs/changelog.md` 신규 entry; `_sdd/spec/usage-guide.md` `/pr-review` 명령 행(문구 현행 유지 확인).

## Scope
- **In**: `.claude/skills/pr-review/` 전체와 Codex 미러, correctness 계약 reference 신설, `sdd-orchestrator/references/simplicity-contract.md` Step 1의 PR Review Input 분기 문장, `sdd-orchestrator/SKILL.md`의 env.md 행 규칙 1문장(양 runtime), `_sdd/env.md` 표, `worker-model-defaults.md` 템플릿 4벌, `README.md` pr-review·모델 설명.
- **Out**: `_sdd/spec/`(spec-sync 소유), simplicity 계약의 차원·severity·반환 형식, sdd-orchestrator 단계·게이트 구조, plugin version bump(marketplace 1.0.0 / codex 1.0.1 유지), `docs/reviews/`·`.sdd-workbench/` 이력 문서, Codex 미러에 없는 `references/gh-commands.md` 비대칭(현행 유지).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: pr-review SKILL.md를 두 worker dispatch 구조로 재구성 (Claude + Codex 미러)
메인을 thin dispatcher로 바꾼다 — 작은 입력 수집, 두 worker 동시 dispatch, verdict 합성, 리포트 작성만 남긴다.

**Contracts**:
- `PR Review Input` 5필드(SKILL.md가 필드 정의 소유): **PR**(번호·URL), **Baseline**(`headRefOid`, 그 SHA의 코드·spec 읽기 방법 — `git show <sha>:<path>`/격리 checkout/API, 현재 checkout 사용 가능 여부), **Changed Files**(`gh pr diff --name-only` 결과), **Spec Status**(`FOUND`+같은 SHA의 spec 경로 목록 / `ABSENT` / `UNREADABLE`+원인), **Relevant Context**(title·body·저자 설명 요약, 없으면 `NONE`). 메인은 diff 본문·spec 본문·comments를 읽지 않는다.
- Step 2는 spec 존재 판정만 한다: `git ls-tree -r --name-only <sha> -- _sdd/spec/`로 FOUND/ABSENT/UNREADABLE을 정하고 경로 목록을 Spec Status에 넣는다. 내용 읽기는 worker가 한다. Step 2는 local object가 없으면 기존 fetch/API fallback을 유지한다. Step 4·리포트의 Spec 상태는 correctness 반환의 spec 모드를 최종값으로 쓴다.
- Step 3 dispatch: correctness worker prompt는 `너는 pr-review가 띄운 correctness worker다. / 계약: <스킬 base directory + references/correctness-contract.md 절대 경로> — 그대로 따른다. / 입력: <PR Review Input>` 형식, simplicity worker prompt는 기존대로 simplicity 계약 전문 verbatim + `PR Review Input`. 두 dispatch를 한 메시지에 낸다. Claude: `Agent(subagent_type="general-purpose")`, schema에 `run_in_background`가 있으면 true, 결과 대기용 sleep·폴링 금지. 사용자의 스킬 호출이 두 dispatch 모두에 대한 명시적 요청이라는 기존 문단은 유지한다.
- 모델 결정: `--model <name>`(Codex는 `--effort`도) > `_sdd/env.md` `## Worker Model Defaults`의 현재 runtime 표 `pr-review` 행 > 생략(런타임 기본). 두 dispatch에 같은 값을 적용한다. Claude 허용값 `sonnet`·`opus`·`haiku`·`fable`, 그 외 값이면 dispatch하지 않고 허용값 안내. Codex는 Runtime Adapter의 schema enum 검증을 두 spawn에 적용한다. 기존 "correctness는 override 대상이 아니다" 안내는 삭제한다.
- AC 재정의: AC3 "correctness 계약 경로를 받은 범용 worker를 PR Review Input으로 dispatch하고 반환을 받았다", AC6 "적용 model(호출 > env.md `pr-review` 행 > 생략)을 두 dispatch에 같게 적용했다". Hard Rule `단일 작성자 불변식`·`from-branch 기준`은 두 worker에 적용되게 문구를 넓힌다 — 단일 작성자 문구는 경계를 재서술하지 않고 "worker의 쓰기 경계·예외는 각 계약의 Runtime Boundary"로 가리킨다. Error Handling의 렌즈 실패 행은 어느 렌즈든 대칭으로 처리한다(확보된 렌즈 결과 보존·제한 리포트·같은 blocker 반복 dispatch 금지).
- 리포트 언어(Hard Rule "리뷰 리포트 언어는 읽은 spec 언어를 따른다…" 유지): 언어의 출처는 correctness 반환 Status의 spec 언어다. 메인은 그 언어로 리포트를 쓰고, 확인할 수 없으면 한국어로 쓴다.
- Error Handling `headRefOid` 불일치 행(correctness BLOCKED 또는 simplicity Assumptions의 baseline 불일치 blocker — 둘 다 렌즈 실패가 아닌 이 행으로 처리): 메인은 `headRefOid`를 새 SHA로 다시 고정하고 두 worker를 1회 다시 띄운다. 또 불일치하면 제한 리포트(NEEDS DISCUSSION, LIMITED)로 닫는다.
- Edge Cases 표의 `Multiple spec files in from-branch` 행은 삭제한다 — spec 범위 선택은 Task 2 계약 `## 수집` 소관이다(사용자 질문 없음).
- Output Format `**Reviewer**` 줄은 `Claude (<메인 model> / workers <적용 model 또는 runtime default>)` 꼴로 한다(Codex 미러는 `Codex`).
- `## Correctness 리뷰` 절(Review Dimensions 표·Fresh Verification·Findings 분류·ledger 규칙)은 SKILL.md에서 제거하고 Task 2의 계약으로 옮긴다. Additional Resources에 `references/correctness-contract.md` 행을 추가하고 하단 `Source` 주석을 두 계약의 단일 소스 위치로 고친다.
- Codex 미러는 3-way merge: 기존 Codex 적응 delta(frontmatter `argument-hint`, `## Codex Runtime Adapter`+`Agent Message Boundary` 절, dispatch↔spawn·`Agent(...)`↔adapter 참조 치환, `/sdd-skills:`↔`$` 접두, `Reviewer: Claude`↔`Codex`, Edit 도구 언급 제거, `gh-commands.md` 리소스 행 부재, `--effort` 언급(Codex만), 모델 검증의 Claude 허용값 4종↔Codex schema enum 검증 교체, Claude 전용 `run_in_background`·sleep/폴링 금지 문구↔Codex wait/timeout 문구("wait가 timeout이면 완료로 간주하지 말고…"), 도구명 `Read`/`Grep`↔"파일 읽기·검색" 치환)만 유지하고 그 밖의 본문은 Claude 판과 동일하게 맞춘다. Runtime Adapter는 두 spawn(correctness·simplicity)에 적용되게 고치고, correctness spawn의 framed message는 `## Mode: pr-review (correctness)` + 계약 경로 지시 + `## Input Data`에 PR Review Input을 둔다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): 두 SKILL.md에서 `/usr/bin/grep -c '메인 루프 직접\|메인 루프가 직접\|직접 correctness\|직접 Correctness\|correctness 리뷰를 직접\|simplicity dispatch에만\|simplicity spawn에만\|simplicity spawn 전용\|simplicity 호출에만\|Multiple spec files\|^## Correctness 리뷰\|^- \*\*PR Diff\*\*'` → 각 `0`.
- [ ] AC2 (1등급): 두 SKILL.md에서 `/usr/bin/grep -c 'references/correctness-contract.md'` ≥ `2`(Step 3 + Additional Resources), `/usr/bin/grep -c 'Worker Model Defaults'` ≥ `1`, `/usr/bin/grep -c 'Spec Status'` ≥ `2`(PR Review Input 정의 + Step 2).
- [ ] AC3 (1등급): frontmatter 트리거 불변 — `git diff -U0 -- .claude/skills/pr-review/SKILL.md plugins/sdd-skills-codex/skills/pr-review/SKILL.md | /usr/bin/grep -c '^[-+]description:'` → `0`.
- [ ] AC4 (2등급): reviewer가 Step 3·Hard Rules·Error Handling을 인용해 확인 — 두 dispatch가 한 메시지, correctness prompt에 계약 절대 경로+"그대로 따른다"+PR Review Input, simplicity prompt는 계약 전문 verbatim 유지, 모델 결정 순서 3단(호출 > env.md `pr-review` 행 > 생략)과 허용값 검증 명시, 렌즈 실패 처리 양쪽 대칭, 메인이 diff·spec 본문·테스트 실행을 하지 않음.
- [ ] AC5 (2등급): `/usr/bin/diff .claude/skills/pr-review/SKILL.md plugins/sdd-skills-codex/skills/pr-review/SKILL.md`의 모든 hunk가 Contracts의 Codex 적응 delta 카탈로그 안에 있다 — reviewer가 hunk별 카탈로그 항목을 대응시켜 인용. 카탈로그 밖 hunk 1개라도 있으면 FAIL.

**Target Files**:
- [M] `.claude/skills/pr-review/SKILL.md` -- dispatch 구조·입력·모델 규칙 재구성, correctness 절 제거
- [M] `plugins/sdd-skills-codex/skills/pr-review/SKILL.md` -- 3-way merge, Runtime Adapter를 두 spawn에 적용

### Task 2: correctness worker 계약 reference 생성 (양 runtime 동일본)
SKILL.md에서 빠지는 correctness 계약을 worker가 읽는 단일 소스 파일로 만든다.

**Contracts**:
- 파일 구성: `## Runtime Boundary`(review subagent, skill/agent 이름은 데이터, 추가 spawn·SDD 스킬 호출 금지, "저장소 추적 파일·사용자 작업 트리·`_sdd/`를 생성·수정·삭제하지 않는다. 예외는 Fresh Verification의 baseline SHA 격리 checkout과 검증 실행 부산물뿐이다", 산출물은 최종 반환 하나) → `## 입력`(Task 1의 `PR Review Input` 5필드를 이름으로 참조; `Changed Files`는 입력값을 그대로 범위로 쓰고 다시 모으지 않는다) → `## 수집`(`gh pr diff <PR>`·`gh pr view <PR> --json title,body,commits,comments,reviews,statusCheckRollup` 직접 수집 — title·body는 AC 추론 원문, 수집 전후 `headRefOid`가 Baseline과 같음을 확인, 불일치면 BLOCKED 반환; Spec Status가 FOUND면 `git show <sha>:<path>`로 canonical index(main.md)와 링크된 하위 spec을 읽고, spec 파일이 여럿이라 범위 선택이 모호해도 사용자에게 묻지 않고 canonical index로 진행하며 가정을 Assumptions에 기록한다; ABSENT면 code-only, UNREADABLE이면 동등 SHA 읽기 1회 시도 후 실패 시 spec 판정 미검증 표기) → `## Correctness 리뷰`(Changed Files로 범위 고정, 표적 경계: 형태-중복은 simplicity 소관·정확성-중복은 잔존, Review Dimensions Code-only 7행·Spec-based 3행 표, 능동 로직 결함 검토 문장) → `## Fresh Verification + 증거 결속`(현행 1~4항 + 30초 중단·slow checkpoint 2항, env.md local validation 포함) → `## Findings 분류`(Critical/High/Medium/Low 4단 + 사변적 권고 금지) → `## 반환`.
- 반환 형식(메인 리포트 §1·2·4에 바로 매핑): **Status**(blocker 유무 1줄, spec 모드 FOUND/ABSENT/UNREADABLE, 읽은 spec 범위, 읽은 spec의 언어 — 확인 불가면 `UNKNOWN`) / **Findings** severity별 — Critical·High·Medium은 제목+위치(`file:line`)·문제(증거)·수정 블록, Low는 위치 포함 한 문장 / **AC 검증 ledger** — 문제 verdict(NOT MET·PARTIAL·UNTESTED·FAIL)만 `| # | Criterion | Implementation | Test | Status | Evidence |` 행, 통과는 `MET: #1–#N` 한 줄(증거 없는 MET 금지) / **Validation source**(CI/local 실행 SHA·output 위치 또는 UNTESTED 사유) / **severity 요약** 1줄(Crit N·High N·Med N·Low N) / **Assumptions / Limitations**. 확인했으나 finding이 아닌 결과는 열거하지 않는다.
- 양 runtime 동일본: Codex 쪽도 같은 파일이다(런타임 분기 문장 없음).

**Acceptance Criteria**:
- [ ] AC1 (1등급): `/usr/bin/diff .claude/skills/pr-review/references/correctness-contract.md plugins/sdd-skills-codex/skills/pr-review/references/correctness-contract.md` → 무출력, exit 0.
- [ ] AC2 (1등급): `.claude/skills/pr-review/references/correctness-contract.md`에서 `/usr/bin/grep -c` 각 패턴 ≥ `1`: `^## Runtime Boundary`, `저장소 추적 파일·사용자 작업 트리`, `격리 checkout과 검증 실행 부산물`, `title,body`, `Spec Compliance`, `Gap Analysis`, `headRefOid`, `gh pr diff`, `canonical index`, `spec의 언어`, `UNTESTED`, `| # | Criterion | Implementation | Test | Status | Evidence |`, `MET:`, `severity 요약`, `30초`.
- [ ] AC3 (2등급): reviewer가 `git show HEAD:.claude/skills/pr-review/SKILL.md`의 `## Correctness 리뷰` 절 항목(Code-only 7행·Spec-based 3행·Fresh Verification 4항+2항·severity 4단·ledger 규칙·표적 경계 문장)마다 계약의 대응 줄을 인용해 누락 0을 확인한다.

**Target Files**:
- [C] `.claude/skills/pr-review/references/correctness-contract.md` -- SKILL.md는 메인 루프 지시문이라 worker가 읽는 계약 파일이 될 수 없고, `sdd-orchestrator/references/workers/implementation-review.md`는 판정 기준(draft task AC·구현 base)이 PR 리뷰(PR AC 추론·baseline SHA·CI 결속)와 달라 공용 불가
- [C] `plugins/sdd-skills-codex/skills/pr-review/references/correctness-contract.md` -- `.claude/skills/`는 Codex 번들 밖이라 동일본 배포 필요

### Task 3: pr-review 예시·체크리스트를 두 worker 구조로 갱신
examples·review-checklist의 "직접 correctness" 서술을 두 worker dispatch 서술로 바꾼다. sample-review.md는 메인 루프가 spec 본문을 읽거나 테스트를 실행하거나 AC를 추론하는 모든 서술도 범위다 — Example A의 `## PR 데이터 수집` "검증 evidence" 줄, `## from-branch spec 로드` 블록(`git show …:_sdd/spec/main.md 로드`·linked sub-spec 로드), `### leaf 입력의 범위` 문단("메인은 위 PR metadata·spec·검증 상태·slug를 관리한다. simplicity에는 Changed Files, PR Diff, …"), Example B의 "메인 루프가 PR title/body/코멘트에서 AC를 추론해 correctness 검증"과 로컬 테스트 실행 줄. 이들은 메인의 Step 2 존재 판정(`git ls-tree`→FOUND/ABSENT) + 두 worker dispatch + correctness worker 반환(spec 모드·읽은 spec 범위·Validation source·AC ledger)으로 귀속해 다시 쓴다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): 4파일(`.claude/skills/pr-review/examples/sample-review.md`, `references/review-checklist.md`, 각 Codex 미러)에서 `/usr/bin/grep -c '메인 루프 직접\|메인 루프가 직접\|직접 correctness\|직접 Correctness\|correctness 리뷰를 직접\|direct correctness\|simplicity dispatch에만\|simplicity spawn에만\|PR Diff\|메인 루프가 PR'` → 각 `0`.
- [ ] AC2 (1등급): `/usr/bin/diff .claude/skills/pr-review/references/review-checklist.md plugins/sdd-skills-codex/skills/pr-review/references/review-checklist.md` → 무출력, exit 0.
- [ ] AC3 (2등급): reviewer가 sample-review.md 두 예시를 인용해 확인 — Step 3 블록(Claude: Agent 2회 한 메시지 / Codex: 선택한 adapter contract로 spawn 2회), 두 렌즈 요약 줄이 모두 "(worker 반환)", 메인 쪽 서술에 spec 본문 로드·테스트 실행·AC 추론·검증 evidence 판정이 없고 그 결과는 correctness worker 반환 항목으로만 등장, `제한 결과 예시`의 렌즈 실패 문장이 어느 렌즈든 대칭. Codex 예시의 Mailbox/Target 서술은 유지한다.

**Target Files**:
- [M] `.claude/skills/pr-review/examples/sample-review.md` -- Step 3·렌즈 요약·제한 결과 서술 갱신, 메인의 spec 로드·검증 evidence·AC 추론 서술을 worker 반환으로 귀속
- [M] `plugins/sdd-skills-codex/skills/pr-review/examples/sample-review.md` -- 같은 갱신, Codex spawn 서술 유지
- [M] `.claude/skills/pr-review/references/review-checklist.md` -- Verdict Criteria 문장 "after direct correctness review" 교체
- [M] `plugins/sdd-skills-codex/skills/pr-review/references/review-checklist.md` -- 동일본 유지

### Task 4: sdd-orchestrator 소유 표면을 새 입력·새 행에 정합
simplicity 계약 Step 1의 `PR Diff` 의존과 SKILL.md의 "행은 다섯 단계 이름이다"가 Task 1·5와 어긋나지 않게 각 1문장만 고친다.

**Contracts**:
- simplicity-contract `### Step 1: Scope` PR Review Input 분기: `Changed Files`로 범위를 고정하고 PR diff는 `PR` 필드의 번호와 Baseline SHA로 직접 수집(`gh pr diff <PR>`, `headRefOid` 재확인)한다. 이 문장에 읽기 전용 `gh` 조회(`gh pr diff`·`gh pr view`)는 Runtime Boundary의 "동등한 읽기 전용 탐색"으로 허용한다고 명시한다. 불일치면 리뷰하지 않고 Assumptions에 baseline 불일치 blocker로 반환한다. 다른 절은 불변(Step 4 반환 형식에 BLOCKED를 새로 두지 않는다 — 기존 Assumptions 항목을 쓴다).
- sdd-orchestrator SKILL.md `Worker dispatch` env.md 기본값 문장: "행은 다섯 단계 이름이다" 뒤에 다른 스킬의 행(`pr-review`)이 있어도 이 스킬은 읽지 않는다는 1문장을 덧붙인다. 양 runtime 동일 변경.

**Acceptance Criteria**:
- [ ] AC1 (1등급): 두 simplicity-contract.md에서 `/usr/bin/grep -c '`Changed Files`와 `PR Diff`로'` → `0`, `/usr/bin/grep -c 'gh pr diff'` → `1`, `/usr/bin/grep -c 'baseline 불일치 blocker'` → `1`, `/usr/bin/grep -c '읽기 전용'` → `2`(현재 1 = Runtime Boundary); `/usr/bin/diff -r .claude/skills/sdd-orchestrator/references plugins/sdd-skills-codex/skills/sdd-orchestrator/references` → 무출력, exit 0.
- [ ] AC2 (1등급): 두 sdd-orchestrator/SKILL.md에서 `/usr/bin/grep -c 'pr-review'` → `1`(현재 0); `/usr/bin/diff .claude/skills/sdd-orchestrator/SKILL.md plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md | /usr/bin/grep -c '^[0-9]'` → `1`.
- [ ] AC3 (1등급): 변경 한정 — `git diff -U0 -- .claude/skills/sdd-orchestrator/references/simplicity-contract.md | /usr/bin/grep -c '^@@'` → `1`, `git diff -U0 -- .claude/skills/sdd-orchestrator/SKILL.md | /usr/bin/grep -c '^@@'` → `1`.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/references/simplicity-contract.md` -- Step 1 PR Review Input 분기 문장
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/simplicity-contract.md` -- 동일본
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- env.md 행 규칙 1문장
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- 동일 변경(미러 hunk 1 유지)

### Task 5: Worker Model Defaults에 `pr-review` 행 추가 (env.md + 부트스트랩 템플릿 4벌)
pr-review worker 기본 모델을 env.md에 두고, spec-create·spec-upgrade가 만드는 템플릿도 같은 행을 갖게 한다.

**Contracts**:
- 안내문 한 벌: `_sdd/env.md` 절 안내문과 템플릿 `## env.md 블록` 안내문은 모두 "`sdd-orchestrator`·`pr-review`가 읽는 worker 기본값"으로 시작한다(템플릿 현행 "`sdd-orchestrator`의 단계별 worker 기본값을 설정하는 선택 항목입니다"를 교체, 나머지 문장은 유지). 템플릿 `## 확인·보고`의 행 수 서술은 "단계 행과 `pr-review` 행이 중복 없이 있고"로 쓴다. 템플릿 `## 적용` bullet "누락된 안내·runtime 표·열·단계 행만 추가한다"는 "누락된 안내·runtime 표·열·단계·`pr-review` 행만 추가한다"로 바꾼다 — 기존 env.md에 빠진 `pr-review` 행 추가를 분명히 덮기 위해서다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `_sdd/env.md`에서 `/usr/bin/grep -c '^| pr-review | opus |$'` → `1`, `/usr/bin/grep -c '^| pr-review | gpt-6.1-sol | high |$'` → `1`, 절 안내문의 `/usr/bin/grep -c 'sdd-orchestrator`·`pr-review`가 읽는'` → `1`.
- [ ] AC2 (1등급): canonical `.claude/skills/spec-create/references/worker-model-defaults.md`에서 `/usr/bin/grep -c '^| pr-review | |$'` → `1`, `/usr/bin/grep -c '^| pr-review | | |$'` → `1`, `/usr/bin/grep -c 'sdd-orchestrator`·`pr-review`가 읽는'` → `1`, `/usr/bin/grep -c '단계 행과 `pr-review` 행'` → `1`, `/usr/bin/grep -c '단계·`pr-review` 행만 추가'` → `1`, `/usr/bin/grep -c '다섯 단계'` → `0`; 나머지 3벌(`spec-upgrade` claude, `spec-create`·`spec-upgrade` codex)과 `/usr/bin/diff` → 각 무출력, exit 0.
- [ ] AC3 (1등급): 비밀값 없음 — `git diff -U0 -- _sdd/env.md | /usr/bin/grep -c '^+.*[A-Za-z0-9_-]\{32,\}'` → `0`.

**Target Files**:
- [M] `_sdd/env.md` -- 두 runtime 표에 `pr-review` 행, 절 안내문
- [M] `.claude/skills/spec-create/references/worker-model-defaults.md` -- 템플릿 행·확인 문구 (authoring canonical)
- [M] `.claude/skills/spec-upgrade/references/worker-model-defaults.md` -- 동일본
- [M] `plugins/sdd-skills-codex/skills/spec-create/references/worker-model-defaults.md` -- 동일본
- [M] `plugins/sdd-skills-codex/skills/spec-upgrade/references/worker-model-defaults.md` -- 동일본

### Task 6: README의 pr-review 모델·구조 설명 갱신
`Subagent Model Override` 절과 Skills 절의 pr-review 문장을 새 구조에 맞춘다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `README.md`에서 `/usr/bin/grep -c '메인 루프 직접\|메인 루프가 직접\|simplicity dispatch에만\|메인 루프에서 검토'` → `0`; `/usr/bin/grep -c 'pr-review' README.md` ≥ 현재 값(`5`).
- [ ] AC2 (2등급): reviewer가 `## Subagent Model Override` 절 전체와 Skills 절의 "`pr-review`는 correctness를 메인 루프에서 검토하고…" 문장(갱신 후 짝)을 인용해 확인 — `--model`(Codex `--effort`)이 correctness·simplicity 두 worker에 같게 적용, env.md `## Worker Model Defaults`의 `pr-review` 행이 기본값, 결정 순서(호출 > env.md > 런타임 기본), pr-review는 두 렌즈를 계약을 받은 범용 worker로 검토한다는 서술. 호출 예시 2개(Claude·Codex)는 유지.

**Target Files**:
- [M] `README.md` -- pr-review 모델 override·구조 설명

### Task 7: 잔존 표기·미러 census 검증 (read-only)
Task 1~6 뒤 변형 표기 잔존과 미러·위생 회귀를 전수 확인한다. FAIL이면 원인 task로 돌려보낸다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `/usr/bin/grep -rn -i '메인 루프 직접\|메인 루프가 직접\|직접 correctness\|direct correctness\|correctness 리뷰를 직접\|simplicity dispatch에만\|simplicity spawn에만\|simplicity spawn 전용\|simplicity 호출에만\|override 대상이 아니\|메인 루프에서 검토' README.md _sdd/env.md .claude/skills/pr-review plugins/sdd-skills-codex/skills/pr-review .claude/skills/sdd-orchestrator/references/simplicity-contract.md plugins/sdd-skills-codex/skills/sdd-orchestrator/references/simplicity-contract.md` → 무출력(pr-review 표면 한정 — `sdd-orchestrator/SKILL.md` "메인 루프가 직접 하는 일:"·`goal-init/SKILL.md`는 범위 밖 정상 문구, 이력 `docs/`·`_sdd/spec/`도 범위 밖).
- [ ] AC2 (1등급): `PR Diff` 필드 잔존 — `/usr/bin/grep -rn '\*\*PR Diff\*\*' .claude/skills plugins/sdd-skills-codex/skills` → 무출력.
- [ ] AC3 (1등급): pr-review 공유 reference 미러 — `for f in correctness-contract.md review-checklist.md; do /usr/bin/diff .claude/skills/pr-review/references/$f plugins/sdd-skills-codex/skills/pr-review/references/$f; done` → 무출력, exit 0; `/usr/bin/diff .claude/skills/pr-review/examples/sample-review.md plugins/sdd-skills-codex/skills/pr-review/examples/sample-review.md | /usr/bin/grep -c '^[0-9]'` ≤ `13`(현재 10 + correctness spawn 적응분 최대 3). 14 이상이면 FAIL.
- [ ] AC4 (1등급): digest 회귀 레시피 4행 전부 기대값 — orchestrator 미러 hunk `1`, references `diff -r` exit 0, `git diff --check` 무출력, `claude plugin validate .` → `Validation passed`.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- `PR Diff`를 PR Review Input에서 빼고 두 worker가 직접 수집 — 결정: 뺀다. "메인은 작은 입력만"의 직접 귀결이며 simplicity 계약은 Step 1 한 문장만 바뀐다(차원·worker 수 불변). 사용자 확인 필요: 아니오.
- comments/reviews(discussion)·Fresh Verification(CI/local 테스트 실행)을 누가 하나 — 결정: correctness worker. 메인은 title·body·저자 설명만 Relevant Context로 넘긴다. 사용자 확인 필요: 아니오.
- `sdd-orchestrator` SKILL "행은 다섯 단계 이름이다"와 새 `pr-review` 행 — 결정: 충돌로 보고 "다른 스킬의 행은 읽지 않는다" 1문장을 덧붙인다(미러 hunk 1 유지). 사용자 확인 필요: 아니오.
- simplicity는 전문 verbatim 주입, correctness는 경로 Read — 두 방식 공존. 결정: digest 결정("simplicity 기존 유지")대로 둔다. 사용자 확인 필요: 아니오.
- plugin version(marketplace 1.0.0 / codex 1.0.1) — 결정: 올리지 않는다(최근 하네스 재편 PR도 미변경). 사용자 확인 필요: 아니오.
