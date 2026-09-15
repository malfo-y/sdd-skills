---
name: pr-review
description: "Use this skill when the user asks to \"review PR\", \"PR review\", \"PR 리뷰\", \"PR 검증\", \"PR spec patch\", \"PR 스펙 패치\", \"PR 리뷰 준비\", or wants to verify a pull request against the specification or codebase."
argument-hint: "[--model <active-model>] [--effort <active-effort>]"
---

# PR Review (직접 correctness + simplicity spawn + Verdict)

이 스킬은 PR 데이터·spec을 수집한 뒤, **correctness 리뷰를 메인 루프가 직접 수행**하고 **clarity 렌즈만** 범용 sub-agent로 spawn한다 (동작-불변 형태 품질 — 계약·차원·severity는 `implementation-review` 스킬의 `references/simplicity-contract.md`가 단일 소스이며, spawn message에 전문을 verbatim 포함한다). 두 렌즈 결과를 합쳐 **verdict**(APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)를 합성해 통합 리뷰 리포트(`_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`) 하나를 작성한다.

> **경계**: 자동 게이트는 도입하지 않는다 — PR review는 인간 리뷰 보조다. verdict는 두 렌즈 신호를 모두 쥔 메인 루프가 합성한다.

## Acceptance Criteria

- [ ] AC1: `_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md` 통합 리뷰 리포트가 Output Format에 맞게 생성되었다
- [ ] AC2: Verdict(APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)가 두 렌즈 요약을 근거로 부여되었다
- [ ] AC3: correctness 검증(코드 품질·에러 처리·테스트·보안, spec 존재 시 spec AC·compliance·gap)을 메인 루프가 Correctness 리뷰 절의 절차대로 직접 수행했다
- [ ] AC4: simplicity 계약(reference 전문 verbatim)을 담은 범용 sub-agent를 PR 변경 파일 컨텍스트(PR Review Input)로 spawn했다
- [ ] AC5: 두 렌즈의 finding이 Step 4 합류 규칙대로 통합 리포트에 합류했다
- [ ] AC6: `--model`/`--effort` 인자가 있으면 simplicity spawn에 적용했다 (correctness는 메인 루프 직접 수행이라 적용 대상이 아니다 — 그 사실을 안내)

## Hard Rules

- `_sdd/spec/` 파일은 **읽기 전용**. 수정이 필요하면 리포트에 기록하고 `$spec-sync` 사용을 안내한다.
- 리뷰 리포트 언어는 읽은 spec 언어를 따른다. Spec 언어를 확인할 수 없으면 한국어.
- PR title/description은 원문 유지.
- **단일 작성자 불변식**: simplicity reviewer는 파일을 쓰지 않는다(경량 반환). 파일 작성은 메인 루프의 통합 리포트(`_sdd/pr/..._pr_review_...`) 하나뿐이다.
- **from-branch 기준**: 코드·spec·실행 증거는 Step 0의 baseline SHA에 결속한다. simplicity leaf도 전달받은 동일 SHA의 읽기 경로만 사용한다. to-branch(base) spec은 검증 기준이 아니며 변경 비교 참고용으로만 읽는다.

## Codex Runtime Adapter (simplicity spawn 전용)

런타임이 skill-internal agent dispatch를 허용하는 경우, 이 스킬의 직접 호출은 simplicity spawn 범위에 대한 사용자 요청으로 처리한다. 현재 런타임 정책이 명시적 sub-agent 허가를 추가로 요구하면, spawn 전에 사용자에게 위임 허가를 요청한다.

spawn 전에 **active tool schema를 직접 확인**하고 아래 두 lifecycle contract 중 정확히 하나만 선택한다. 없는 lifecycle tool을 찾으려고 `tool_search`하지 않으며, 두 contract의 필드나 lifecycle 호출을 섞지 않는다. `agent_type`은 lifecycle 필드가 아니라 **선택적 role selector**다 — active schema가 `"explorer"` 값을 지원할 때만 추가하고, 필드가 없거나 해당 값을 지원하지 않으면 생략한다. 생략해도 simplicity 역할·read-only 경계는 framed `message`의 계약 전문이 부여하므로 blocker가 아니다.

- **Mailbox contract (Desktop/current CLI)**: `spawn_agent`가 `task_name`/`fork_turns`를 요구하거나 `wait_agent`에 `targets`가 없다. invocation마다 짧은 lowercase `run_id`를 만들고, 같은 parent tree의 재실행까지 포함해 고유한 `task_name`에 그 값을 넣는다. spawn에 이 `task_name`, `fork_turns: "none"`, `message`를 전달하고, 지원되는 경우에만 `agent_type: "explorer"`를 추가한다. `wait_agent({timeout_ms: 600000})` mailbox를 반복 호출해 final을 수거한다. 완료 agent는 닫지 않는다. 통제된 중단이 필요할 때만 노출된 `interrupt_agent`를 사용한다.
- **Target/close contract (legacy CLI schema)**: `wait_agent`가 `targets`를 지원하고 `close_agent`도 노출된다. `message`로 spawn하고, 지원되는 경우에만 `agent_type: "explorer"`를 추가한 뒤 target wait로 final을 수거하고 완료 handle을 닫는다.
- 어느 lifecycle contract도 완전하지 않거나 둘 중 하나로 확정할 수 없으면 spawn하지 않고 **schema blocker**를 보고한 뒤, correctness 직접 리뷰만으로 제한 리포트를 작성하고 누락 렌즈·미충족 AC를 명시한 뒤 Final Check의 제한 종료를 따른다. `agent_type` 부재만으로는 이 분기를 타지 않는다.

실행 surface 이름이 아니라 schema가 contract를 결정한다.

> **Subagent model override**
>
> - `$ARGUMENTS`의 `--model <name>`은 contract 선택 후 active `spawn_agent` schema의 `model` enum으로, `--effort <level>`은 같은 schema의 `reasoning_effort` enum으로 검증한다. 값이 enum 밖이면 spawn하지 않고 허용값을 보고한다.
> - 검증된 필드는 **simplicity spawn에만** 적용한다 — correctness는 메인 루프 직접 수행이라 override 대상이 아니다(그 사실을 안내). 미지정 필드는 생략해 세션/agent 기본값을 상속한다.
> - model과 effort를 합친 값은 받지 않고 `--model <active-model> --effort <active-effort>` 분리 문법을 안내한다.

Mailbox contract (아래 `r7f3a`는 예시 `run_id`):

```text
spawn_agent({task_name: "pr_review_r7f3a_simplicity", fork_turns: "none", message: "<framed payload: simplicity 계약 전문(verbatim) + Mode + Input Data>"})
wait_agent({timeout_ms: 600000})  // final이 도착할 때까지 반복
```

Target/close contract:

```text
spawn_agent({message: "<framed payload: simplicity 계약 전문(verbatim) + Mode + Input Data>"})
wait_agent({targets: ["<simplicity_id>"], timeout_ms: 600000})
close_agent({target: "<simplicity_id>"})
```

### Agent Message Boundary

`message`는 framed payload로 만든다. PR title/description, slash command, skill 이름, agent 이름은 반드시 `## Input Data` 아래에 넣고 top-level 실행 지시처럼 전달하지 않는다. `## Input Data` 자리에는 아래 canonical `## PR Review Input` 블록 전체를 붙인다.

```text
<../implementation-review/references/simplicity-contract.md 전문 (verbatim — 그 문서의 Runtime Boundary 절이 재호출 금지·read-only 규칙을 보유)>
## Mode
pr-review (simplicity)
## Input Data
<canonical PR Review Input block defined below>
```

## PR Review Input

simplicity reviewer의 `## Input Data`에는 아래 필드를 이 순서로 전달한다 (correctness는 메인 루프가 같은 수집 결과를 직접 소비한다).

- **Changed Files**: 비어 있지 않은 PR 변경 파일 목록
- **PR Diff**: 비어 있지 않은 PR diff
- **PR Metadata**: `title`, `body`, `commits`, `headRefOid`, `headRefName`, `baseRefName` key + baseline 코드·spec의 읽기 위치/방법 (현재 working tree 사용 가능 여부 포함)
- **PR Discussion**: comment/review의 `author` + `body`만 담은 목록, 없으면 `NONE` (approval/verdict state 제외)
- **Spec Context**: baseline SHA의 spec bundle (`FOUND`), `ABSENT (code-only)`, 또는 `UNREADABLE: <원인·읽은 범위>`
- **Validation Evidence**: `CI: <실행 대상 SHA·output 또는 NONE>; Local: <대상 SHA·clean 상태·output 또는 NOT_RUN>` (status 요약만 있으면 실행 output과 구분)
- **Report Slug**: 비어 있지 않은 소문자 snake_case

## Process

### Step 0: Pin PR Baseline

`gh` 인증과 PR 번호를 확인한다. 번호 미지정 시 현재 브랜치에서 자동 감지하되, 조회할 PR을 찾지 못하면 번호를 요청한다.

```bash
gh auth status
gh pr view --json number --jq '.number'
gh pr view [PR] --json headRefName,headRefOid
git rev-parse HEAD
git status --porcelain
```

수집한 `headRefOid`를 이번 리뷰의 baseline SHA로 고정한다. 브랜치 이름은 동일성 조건이 아니다. 코드·spec은 이 SHA의 `git show`/API 읽기 또는 해당 SHA의 격리 checkout에서 읽는다. 현재 checkout은 `HEAD == headRefOid`이고 관련 코드·spec·검증 의존 파일에 staged/unstaged/untracked 변경이 없음을 확인한 경우에만 사용한다. 상태 영향이 불명확하면 dirty로 취급한다. 기존 사용자 작업을 checkout·reset·stash로 바꾸지 않는다.

### Step 1: Collect PR Data

```bash
gh pr view [PR] --json title,body,author,state,url,additions,deletions,changedFiles,headRefName,headRefOid,baseRefName,commits,statusCheckRollup
gh pr view [PR] --json comments,reviews --jq '{comments: [.comments[] | {author: .author.login, body}], reviews: [.reviews[] | {author: .author.login, body}]}'
gh pr diff [PR]
gh pr diff [PR] --name-only
gh pr view [PR] --json headRefOid --jq '.headRefOid'
```

수집 전후의 head SHA가 baseline과 일치하는지 확인한다. 달라졌으면 새 SHA를 기준으로 데이터 전체를 다시 수집하며, 일관된 snapshot을 확보하지 못하면 혼합 데이터로 판정하지 않고 blocker를 보고한다. 코드·spec 읽기 경로와 검증 대상 SHA를 `PR Review Input`에 함께 전달한다.

`_sdd/pr/` 디렉토리가 없으면 생성한다. 통합 리포트의 `slug`는 소문자 snake_case(영문 소문자, 숫자, `_`)로 정한다. 같은 날짜·slug 파일이 이미 있으면 `_2`, `_3` 등 빈 suffix를 골라 이전 리포트를 보존한다. 기존 리포트 갱신을 사용자가 명시한 경우에만 그 파일을 갱신한다.

### Step 2: Load Spec (baseline SHA)

PR diff에 spec 변경이 없어도 baseline SHA의 `_sdd/spec/` 트리를 확인한다.

1. 로컬 git object가 있으면 `git ls-tree -r --name-only [headRefOid] -- _sdd/spec/`로 목록을 얻고, `git show [headRefOid]:_sdd/spec/main.md` 등으로 내용을 읽는다. object가 없으면 현재 작업을 바꾸지 않는 fetch 또는 해당 SHA를 지정한 API 읽기를 사용한다.
2. spec이 있으면 `main.md` 또는 명시적 index를 먼저 읽고 링크된 하위 spec도 같은 SHA에서 로드한다. 다중 파일만으로 선택 질문을 하지 않는다(Edge Cases 참조).
3. 결과를 구분한다: `FOUND`는 필요한 spec 읽기 성공, `ABSENT`는 트리 조회 성공 후 spec 파일 부재 확인, `UNREADABLE`은 트리 또는 필요한 spec 읽기 실패다.
4. `ABSENT`일 때만 정상 **code-only 모드**로 진행한다. `UNREADABLE`이면 가능한 동등 SHA 읽기 경로를 시도하고, 계속 실패하면 검토 가능한 코드만 리뷰한다. 읽은 spec 범위·실패 원인과 spec 판정 미검증을 남기고 제한 리포트로 종료한다.

### Step 3: Simplicity Spawn + 직접 Correctness

**simplicity spawn을 먼저 띄운다.** spawn/wait/lifecycle 호출은 위 **Codex Runtime Adapter**에서 선택한 contract를 그대로 사용하고, Step 1·2의 결과로 `PR Review Input`을 채워 `message`에 넣는다.

**agent가 도는 동안 메인 루프가 correctness 리뷰를 직접 수행한다** (아래 Correctness 리뷰). final을 수거하면 Step 4 verdict로 간다 — wait가 timeout이면 완료로 간주하지 말고 더 기다리거나, controlled stop/blocked 상태를 사용자에게 보고한 뒤에만 중단 여부를 결정한다. 서로 독립인 파일 읽기·검색은 가능한 한 함께 배칭하고, 검색으로 좌표를 먼저 잡은 뒤 관련 구간만 선택적으로 읽는다.

## Correctness 리뷰 (메인 루프 직접 수행, 단일 패스)

`Changed Files`로 리뷰 범위를 고정한다. discussion은 저자 해명·기지 이슈·리뷰어 우려의 컨텍스트로만 쓴다. 범위가 큰 PR(50+ files)이면 디렉토리/컴포넌트 수준으로 축약하고 spec 관련 파일에 집중하며 가정을 리포트에 적는다.

**표적 경계**: 형태-중복(추출 가능한 동일 로직 반복) 등 동작-불변 형태 품질은 simplicity 소관이다. 단, 정확성-중복(중복된 보안 검증 누락·일관성 깨진 중복 분기 등 로직 버그성)은 correctness에 잔존한다.

**Review Dimensions** — Code-only 항목은 항상, Spec-based 항목은 from-branch spec이 있을 때만.

| Code-only (항상) | 내용 |
|------|------|
| AC 추론 | PR title, body, commit 메시지 + 기존 PR/review 코멘트에서 의도된 변경 사항·기지 이슈·저자 해명을 반영해 AC를 추론 |
| 코드 품질 | 네이밍, 패턴, 프로젝트 컨벤션 (형태-중복은 simplicity 소관) |
| 에러 처리 | 일관된 응답 형식, 로깅, graceful degradation |
| 테스트 | 새 코드에 대한 테스트 존재 여부, 테스트 통과 여부 (CI 또는 로컬) |
| 보안 | OWASP Top 10, hardcoded secrets, 인증/인가 |
| 성능 | N+1 쿼리, 불필요 I/O, async 블로킹 |
| 문서화 | 새 env vars, API 변경, breaking changes 문서화 여부 |

| Spec-based (spec 존재 시 추가) | 내용 |
|------|------|
| Spec AC 검증 | spec의 각 Feature/Improvement/Bug Fix에 대해 구현 + 테스트 확인. MET(✓) / NOT MET(✗) / PARTIAL(△) |
| Spec Compliance | 기존 spec 요구사항 위반 여부, breaking changes, API contract 변경 |
| Gap Analysis | spec에 있으나 미구현 항목, PR에 있으나 spec에 없는 항목 |

존재/범위 확인에 더해 구현된 코드의 correctness(경계·null·에러 경로·동시성 등 로직 결함)를 능동적으로 검토한다.

**Fresh Verification + 증거 결속**:

1. CI 실행 output은 실행 대상이 baseline SHA와 동일한 코드임을 확인한 경우에만 사용한다. 다른 SHA/merge commit의 결과나 status 요약만 있으면 참고로 구분하고 Test/MET 근거로 쓰지 않는다.
2. 일치하는 CI output이 없으면 baseline의 `_sdd/env.md`가 가리키는 local validation을 시도한다. 실행 전 HEAD와 관련 dirty 상태를 재확인한다. 현재 작업이 baseline과 다르면 기존 작업을 보존하는 해당 SHA의 격리 checkout에서만 실행한다. 같은 버전의 실행 환경을 확보하지 못하면 이유를 기록한다.
3. 두 경로 모두 실행 evidence가 없으면 test-dependent criterion과 correctness test signal을 사유 포함 `UNTESTED`로 둔다. Non-test-dependent criterion과 명시적 N/A는 제외한다.
4. Code citation만으로 Test/MET를 만들지 않는다. 실패 output은 해당 finding의 severity와 ledger에 결속한다.
- 표적 test/check는 30초가 지나면 중단한다. Timeout 후에는 test target, fixture, 또는 관련 구현이 바뀌기 전까지 같은 명령을 다시 실행하지 않는다.
- 느리다고 알려진 test는 repo 또는 사용자가 명시한 checkpoint에서만 실행한다. checkpoint evidence가 없는 slow 의존 AC는 임의 실행하지 않고 `UNTESTED`(사유: slow — checkpoint 대기)로 보고한다.

**Findings 분류**:

- **Critical**: 핵심 기능 누락, 실패 테스트, 보안 취약점, 데이터 손실 위험, breaking change
- **High**: 핵심 AC 일부 불충족, 주요 에러 처리 갭, 중요한 통합 깨짐, spec 위반
- **Medium**: 비핵심 테스트 누락, 중간 수준 성능/유지보수성 우려, 후속 수정이 필요한 품질 문제
- **Low**: 문서화, 선택적 엣지 케이스, 추후 개선 권고

권고는 검출된 실제 결함 또는 측정된 위험에 직접 대응해야 한다 — "future-proof / extensible / configurable" 같은 사변적 권고 금지.

**AC 검증 ledger**: 문제 있는 verdict(NOT MET·PARTIAL·UNTESTED·FAIL)만 리포트 §4에 행으로 낸다 — `| # | Criterion | Implementation | Test | Status | Evidence |` (Inferred AC는 항상, Spec AC는 spec-based 모드에서 추가 판정). 통과(MET) AC는 `MET: #1–#N` 꼴 축약 한 줄로 접는다 — 판정은 전 AC 증거 기반으로 수행하되(증거 없는 MET 금지), 통과 증거는 리포트에 전사하지 않는다.

### Step 4: Verdict

두 렌즈 요약을 합쳐 verdict를 합성한다. spec `UNREADABLE` 또는 확정된 렌즈 누락이면 **NEEDS DISCUSSION (제한된 권고)**으로 닫고, 확인된 결함은 그대로 보존한다. 이 제한 분기를 먼저 적용하고 정상 리뷰에는 아래 표를 쓴다.

| Verdict | 조건 |
|---------|------|
| **APPROVE** | 모든 AC 충족 + spec 위반 없음 + 테스트 통과 |
| **REQUEST CHANGES** | Critical AC 미충족 / spec 위반 / 테스트 실패 / 보안 이슈 |
| **NEEDS DISCUSSION** | 의도적 spec 변경 / 설계 트레이드오프 / 범위 모호 / 실행 evidence 부재로 correctness test signal이 `UNTESTED` (non-test-dependent·명시적 N/A 제외) |

**Finding 합류 규칙** (자동 강제 아님 — 인간 리뷰 보조):

- **correctness Critical/High**: REQUEST CHANGES rationale의 주 근거. §1 Pre-merge에 블록 전문으로 귀속.
- **simplicity Medium+ (falsifiable gating)**: REQUEST CHANGES rationale에 **기여**한다 (correctness 신호와 함께 인간 리뷰어가 판단). 단독으로 verdict를 강제하지 않는다. §1 Pre-merge에 블록 전문으로 귀속.
- **correctness Medium**: §2 개선 제안에 블록 전문으로 귀속 (non-blocking이지만 상세히).
- **correctness Low / simplicity Low (주관)**: §2 개선 제안에 위치 포함 한 문장으로 귀속.

PR review는 verdict 권고이지 자동 게이트가 아니다.

### Step 5: Report Generation

`_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`를 Output Format에 맞게 생성한다. 이 통합 리포트만으로 독자가 행동할 수 있어야 한다 — **행동 대상 finding은 Step 4 합류 규칙대로 전문 승격**한다. finding 개수·AC 충족률 통계 표는 만들지 않는다 (분포는 Verdict의 Signals 한 줄로 충분). 일반 확인 결과·차원 판정은 §3에 산문으로 요약하고, AC별 판정은 §4 ledger에만 둔다.

현재 콘텍스트에서 skeleton을 먼저 기록한 뒤, 같은 흐름에서 내용을 채운다.

## Output Format

```markdown
# PR Review Report

**PR**: #<number> - <title>
**PR Author**: <author>
**Review Date**: YYYY-MM-DD
**Reviewer**: Codex (<model>)
**Spec**: FOUND (baseline SHA) / ABSENT (code-only) / UNREADABLE: <원인>
**Review Status**: COMPLETE / LIMITED: <미충족 skill AC·원인·재개 조건>

---

## Verdict

**[APPROVE / REQUEST CHANGES / NEEDS DISCUSSION]**

**Rationale**: <1-2 sentence rationale — 두 렌즈 신호 종합>
**Signals**: correctness Crit N·High N·Med N·Low N / simplicity High N·Med N·Low N (또는 MISSING: <reason>) / test pass F% (또는 UNTESTED: <reason>) — 한 줄, 표 없음

---

## 1. Pre-merge (고쳐야 할 것)

<!-- correctness Critical/High + simplicity Medium+. severity 내림차순. 없으면 "없음." 한 줄 -->

### 1. [<Critical|High|Medium> · <correctness|simplicity>] <finding 제목>
- **위치**: `file:line`
- **문제**: 무엇이 어떻게 잘못됐고 어떤 결과를 낳는가 — 증거 포함 (simplicity면 현재 형태)
- **수정**: 구체적 수정 방향 (simplicity면 더 단순한 동등 형태)

---

## 2. 개선 제안 (non-blocking)

<!-- correctness Medium — §1과 같은 블록 형식으로 상세히 -->
### 1. [Medium · correctness] <finding 제목>
- **위치**: `file:line`
- **문제**: <증거 포함>
- **수정**: <구체적 방향>

<!-- correctness Low + simplicity Low — 위치 포함 한 문장씩 -->
- `file:line` — <finding과 수정 방향 한 문장>

---

## 3. 확인된 것

<!-- 일반 확인 결과·차원 판정을 산문 2-3줄로. §4 AC 판정·증거를 반복하지 않음. 표·퍼센트 없음 -->

---

## 4. AC 검증 ledger

<!-- 문제 AC만 행으로; 없으면 "문제 AC 없음.". finding 전문은 §1·2를 참조 -->
| # | Criterion | Implementation | Test | Status | Evidence |
|---|-----------|----------------|------|--------|----------|
| <ID> | <criterion> | <판정> | <판정> | <NOT MET/PARTIAL/UNTESTED/FAIL> | <파일·실행 output 또는 미검증 사유; 관련 finding 링크> |

MET: <통과 AC ID만 나열 또는 없음>

---

## Metadata

**PR commit SHA**: <sha>
**Spec source**: <baseline SHA·읽은 spec 경로 / ABSENT / UNREADABLE 사유>
**Validation source**: <CI/local 실행 SHA·output 위치 / UNTESTED 사유>
**Generated at**: YYYY-MM-DD HH:MM:SS
```

## Edge Cases

| 상황 | 대응 |
|------|------|
| No spec in baseline SHA | Step 2의 `ABSENT`/`UNREADABLE` 구분을 따른다 |
| No PR / `gh` not authenticated | 설치/인증 안내 |
| Multiple spec files in from-branch | canonical index와 링크된 하위 spec을 읽는다. 그래도 범위 선택이 모호하고 verdict에 영향을 주면 짧게 확인한다. 그 외에는 canonical index로 진행하고 가정을 기록한다 |
| Existing review file | Step 1의 충돌 규칙으로 새 slug를 정한다. 명시적 갱신 요청 없이는 기존 파일 보존 |
| Already merged PR | 허용 (retroactive review). merge 상태 표기 |
| Large PR (50+ files) | 디렉토리/컴포넌트 수준 요약으로 축약 (Correctness 리뷰 절·agent Scope) |

## Error Handling

| 상황 | 대응 |
|------|------|
| `gh` CLI not installed | `brew install gh` 안내 |
| `gh auth` failure | `gh auth login` 안내 |
| Wrong PR number | 에러 메시지, 올바른 번호 요청 |
| baseline spec 읽기 실패 | Step 2 항목 4의 `UNREADABLE` 처리를 따른다 |
| simplicity 확정 실패/dispatch blocker | correctness 결과를 보존한 제한 리포트에 누락 렌즈·미충족 skill AC·재개 조건을 기록하고 종료. inline 대체나 같은 blocker의 반복 dispatch 금지 |

## Additional Resources

- **`references/review-checklist.md`** - PR 리뷰 체크리스트 (human reference)
- **`examples/sample-review.md`** - 통합 `pr-review` 예시 세션

## Final Check

선택한 경로에서 Acceptance Criteria와 Hard Rules를 점검한다. 수정 가능한 리포트 누락은 보완한다. spec 읽기 실패·외부 blocker·확정된 렌즈 실패로 충족할 수 없는 AC는 `Review Status: LIMITED`에 원인과 재개 조건을 기록하고 종료하며 정상 완료를 선언하지 않는다. 실패 dispatch를 소급 충족하거나 같은 blocker에서 반복하지 않는다.

> **Source**: simplicity 계약·4개 차원·falsifiable severity는 `implementation-review` 스킬의 `references/simplicity-contract.md`가 단일 소스로 보유한다. correctness 계약·verdict 합성·통합 리포트는 이 SKILL.md가 단일 소스다.
