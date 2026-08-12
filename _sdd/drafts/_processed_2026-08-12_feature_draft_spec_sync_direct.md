# Feature Draft: spec-sync를 직접 실행 스킬로 — agent 짝·표면 묶음 병렬 dispatch 폐지

> 규모 판정: 적격 — 변경 요소 3개(계약 이관·agent 짝 삭제·등록 목록 정리)가 skill 2벌 + agent 짝 2 + 등록 표면 2에만 걸리고 요소↔task 대응이 눈검산된다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
`spec-sync`는 orchestrator(skill) + leaf(agent) 구조이고, evidence 있는 implemented sync는 본문 ∥ 기록 2-shard 작성자 병렬로 dispatch한다(v4.6.24). 그러나 spec sync는 **메인 루프가 이미 들고 있는 맥락**(delta·분류 근거·버전·결정 제목)을 쓰는 작업이라, agent 경유는 그 맥락을 digest로 선고정해 넘기고 agent가 spec 파일을 다시 읽게 만드는 왕복을 추가한다. 병렬 분할의 벽시계 효과는 여전히 미관측(main.md `🚧 Planned`)이며, 분할 때문에 read-vs-rename 경합 회피·사후 정합 grep 같은 부속 계약이 생겼다. 사용자 판단으로 **agent 경유와 표면 분할을 모두 폐지하고 스킬이 직접 실행**한다.

새 contract/invariant:
- **직접 실행 스킬**: `spec-sync`는 dispatch 없이 메인 루프가 직접 수행한다. `.claude/skills/spec-sync/SKILL.md`(및 codex 짝)가 전체 계약·status 분류·Repo-wide Invariant Test의 **단일 소스**가 된다.
- **agent 짝 폐지**: `spec-sync-agent`(claude md + codex toml)를 삭제하고 등록 표면(`.claude-plugin/marketplace.json` agents 배열, `.codex/agents/README.md` Agent Set)에서도 제거한다. 잔존 SDD agent는 4종(plan-review·implementation-review·simplicity·pr-review).
- **표면 묶음 병렬 폐지**: 본문 ∥ 기록 2-shard 분할, `호출자 표면 한정` 절, `Implemented Sync Digest` 선고정 handoff, read-vs-rename 양쪽 조회 규칙이 함께 사라진다. 단일 작성자가 live truth와 기록을 순서대로 쓴다.
- **기록 책임 보존**: 표면 묶음 절이 소유하던 세 책임 — ① live truth 갱신·outdated claim 제거 ② `decision_log.md`·`logs/changelog.md` **append-only 신규 entry**(기존 entry 수정·삭제 금지) ③ 사용한 input file의 `_processed_` rename — 은 Process 안으로 이관해 유지한다.
- **자체 정합 점검 존치**: 기존 orchestrator 사후 검사 2종(헤더 버전 == changelog 최신 entry 버전 / 기록 파일 삭제 줄 0)은 마지막 검증 단계의 자체 점검으로 남는다.

## Scope
- **In**: `.claude/skills/spec-sync/SKILL.md`, `.codex/skills/spec-sync/SKILL.md`, `.claude/agents/spec-sync-agent.md`(삭제), `.codex/agents/spec-sync-agent.toml`(삭제), `.claude-plugin/marketplace.json`, `.codex/agents/README.md`, `README.md`(agent 5종 → 4종 문구).
- **Out**: sync 로직 자체(status 분류 4종·Hard Rules 술어·Repo-wide Invariant Test·Input Sources 6종·Process 6단계는 문면 이관이지 내용 변경이 아니다), 다른 4개 reviewer agent와 그 orchestrator 구조, spec 표면(`spec-sync` 소관), codex 다른 스킬의 Runtime Adapter 블록.
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | 계약 본문 이관(agent → skill) | `.claude/skills/spec-sync/SKILL.md` | `grep -c "Status 분류 (Routing)" .claude/skills/spec-sync/SKILL.md` → 현재 0, 이관 후 ≥ 2 | Task 1 |
| P2 | codex 짝 동일 이관 | `.codex/skills/spec-sync/SKILL.md` | 위 동일 query를 codex 경로에 적용 → 현재 0, 이관 후 ≥ 2 | Task 2 |
| P3 | agent 짝 삭제 + 등록 해제 | `.claude/agents/spec-sync-agent.md`, `.codex/agents/spec-sync-agent.toml`, `.claude-plugin/marketplace.json`, `.codex/agents/README.md`, `README.md` | `grep -rn "spec-sync-agent" --include="*.md" --include="*.toml" --include="*.json" .`(`_sdd/`·`.sdd-workbench/`·`_COMMENTS.md` 제외) → 현재 19줄/6파일, 처리 후 0. 접미사 없는 표기까지 덮는 계수 census: `grep -rn "agent 5종" --include="*.md" .` → 현재 `README.md:5` 1건, 처리 후 In 표면 0 | Task 3 |

# Claim Manifest

> baseline commit = `277e15c` (이 draft의 base). 아래 `git show <base>:` 참조와 Task AC의 기준선은 모두 이 SHA를 쓴다 — `HEAD`는 task 커밋을 따라 움직여 기준선이 무효가 된다.

| ID | Claim | Query | Expected |
|---|---|---|---|
| CM2 | 이관 대상 계약 절의 전수는 baseline에서 도출한다(하드코딩 열거 금지) | `git show 277e15c:.claude/agents/spec-sync-agent.md \| grep -n "^## \|^### "` | 파이프라인 위치 자동 적응 / 호출자 표면 한정 / Implemented Sync Digest / Acceptance Criteria / Hard Rules / Repo-wide Invariant Test / Input Sources / Status 분류 (Routing) / Process(Step 1~6) / Error Handling / Integration / Final Check |
| CM3 | baseline Hard Rules 번호는 1→3으로 건너뛰어 2가 없다(이관 시 연번 교정 대상) | `git show 277e15c:.claude/agents/spec-sync-agent.md \| grep -n "^[0-9]*\. " \| sed -n '1,12p'` | 49행 `1.` 다음이 50행 `3.` — 11개 항목이 1,3~12로 매겨짐 |
| CM4 | 기록 책임 3종과 read-vs-rename 규칙은 `호출자 표면 한정` 절(23~26행)에만 있고 Hard Rules·Process에는 없다 | `git show 277e15c:.claude/agents/spec-sync-agent.md \| grep -n "_processed_\|append-only\|기록 파일\|read-vs-rename"` | 전부 23~26행 구간에만 매칭, Hard Rules(47~59행)·Process(105~169행) 안에는 없음 |
| CM5 | codex skill의 dispatch 잔재는 두 절보다 넓다(intro·Digest·계약·Source 포인터 포함) | `grep -n "^## \|^### " .codex/skills/spec-sync/SKILL.md` | 8줄 — 10 `Codex Runtime Adapter`, 45 `Agent Message Boundary`, 50/52/54(code fence 내부 텍스트), 58 `Implemented Sync Digest`, 67 `실행`, 77 `계약`. 실제 헤딩은 5개 |

# Part 2: Tasks

### Task 1: `.claude/skills/spec-sync/SKILL.md`를 계약 단일 소스로 재작성

agent 본문을 스킬로 이관하고 dispatch 계층을 걷어낸다. 이 파일이 확정 문면이고 Task 2가 codex로 미러한다.

**Contracts**:
- SKILL.md는 CM2가 열거한 baseline 계약 절을 전부 보유하되, dispatch 전용 3절(`호출자 표면 한정`·`Implemented Sync Digest`·`Source Pointer`)은 제외한다. `호출자 표면 한정` 절이 소유하던 **read-vs-rename 양쪽 조회 규칙도 그 절과 함께 사라진다**(CM4 — 분할 부산물이라 단일 작성자에겐 무의미). 같은 절의 기록 책임 3종만 Process로 옮긴다.
- 기록 책임 3종(CM4)은 Process Step 5(적용)·Step 6(검증)에 이관한다 — live truth 갱신, `decision_log.md`·`logs/changelog.md` append-only 신규 entry, 사용한 input file `_processed_` rename.
- 사후 정합 점검 2종(헤더 버전 == changelog 최신 entry / 기록 파일 삭제 줄 0)은 Step 6 자체 점검 항목으로 둔다.
- Hard Rules는 연번 1~11로 교정한다(CM3의 번호 누락 해소 — 파일을 통째로 다시 쓰는 이관의 부작용 정리이지 별도 기능이 아니다). 술어는 baseline 11개 그대로다.
- 실행 주체 서술은 "메인 루프가 직접 수행한다"이며 `Agent(`·`subagent_type` 호출 문법과 baseline의 self-reference(`이 agent는 …`)는 남기지 않는다.
- baseline 절 순서를 유지한다(Hard Rules 다음이 `Repo-wide Invariant Test`) — AC4의 구간 추출이 이 순서를 가정한다.

**Acceptance Criteria**:
- [ ] AC1: `grep -ci "subagent_type\|Agent(subagent\|orchestrator\|dispatch\|병렬\|이 agent" .claude/skills/spec-sync/SKILL.md` → `0` (대소문자 무시 — baseline 제목의 `Orchestrator` 포함).
- [ ] AC2: CM2가 열거한 baseline 계약 절 중 dispatch 전용 3절을 제외한 전부가 SKILL.md에 헤딩으로 존재한다 — reviewer 판정 + CM2 baseline 열거 인용. `grep -c "^### Step" .claude/skills/spec-sync/SKILL.md` → `6`.
- [ ] AC3: status 분류 4종 라벨이 모두 있다 — `grep -c "IMPLEMENTED / VERIFIED\|PARTIAL\|PLANNED / NOT_IMPLEMENTED\|UNVERIFIED" .claude/skills/spec-sync/SKILL.md` → `4` 이상.
- [ ] AC4: Hard Rules가 연번 1~11로 빠짐없이 매겨졌다 — `awk '/^## Hard Rules/,/^## Repo-wide/' .claude/skills/spec-sync/SKILL.md | grep -o "^[0-9]*\." | tr -d '\n'` → `1.2.3.4.5.6.7.8.9.10.11.`. baseline 11개 술어(CM3 기준선)가 전부 식별된다(reviewer 판정 + 인용).
- [ ] AC5: 기록 책임 3종이 Process 안에 있다 — `awk '/^## Process/,/^## Error Handling/' .claude/skills/spec-sync/SKILL.md`로 잘라낸 구간에서 `grep -c "_processed_"` ≥ 1, `grep -c "append-only"` ≥ 1, live truth 갱신·outdated claim 제거 문구 존재(인용).
- [ ] AC6: 사후 정합 점검 2종이 Step 6에 있다 — 버전 일치·삭제 줄 0 두 항목이 각각 식별된다(reviewer 판정 + 인용).
- [ ] AC7: frontmatter `name: spec-sync`와 `description`의 trigger 문구가 baseline과 동일하다 — `diff <(git show 277e15c:.claude/skills/spec-sync/SKILL.md | sed -n '1,4p') <(sed -n '1,4p' .claude/skills/spec-sync/SKILL.md)` → 빈 출력.

**Target Files**:
- [M] `.claude/skills/spec-sync/SKILL.md` -- 계약 단일 소스로 재작성

### Task 2: codex 짝 미러 반영

Task 1의 확정 문면을 codex SKILL로 미러한다. codex의 dispatch 잔재는 두 절보다 넓으므로(CM5) 절 목록이 아니라 AC2의 **파일 전체 동일성 diff**가 제거를 닫는다. 두 파일의 frontmatter는 현재 이미 byte 동일이라 잔여 codex 델타는 0이다.

**Contracts**: 보존 판정 기준은 하나다 — **spawn/wait 문법과 무관한 경로·네임스페이스 규약만 보존**하고, 보존 시 기존 절 제목(`Codex Runtime Adapter`·`Agent Message Boundary`)은 쓰지 않는다. 그 경우에만 AC2의 완전 일치 기대치를 해당 줄로 한정하며, 판정 근거는 두 절의 실제 문면 인용이다.

**Acceptance Criteria**:
- [ ] AC1: `grep -ci "spawn_agent\|Codex Runtime Adapter\|Agent Message Boundary\|wait_agent\|orchestrator\|dispatch\|병렬" .codex/skills/spec-sync/SKILL.md` → `0`.
- [ ] AC2: `diff .claude/skills/spec-sync/SKILL.md .codex/skills/spec-sync/SKILL.md` → 빈 출력(Contracts의 보존 예외가 발생하면 그 줄만 diff에 남고 근거를 인용한다).
- [ ] AC3: Task 1 AC3(status 4종)·AC5(기록 책임)가 codex 파일에서도 성립한다.

**Target Files**:
- [M] `.codex/skills/spec-sync/SKILL.md` -- 미러 반영 + dispatch 절 삭제

### Task 3: agent 짝 삭제 + 등록 해제

**Acceptance Criteria**:
- [ ] AC1: `.claude/agents/spec-sync-agent.md`·`.codex/agents/spec-sync-agent.toml`이 존재하지 않는다 — `ls` 종료코드 비0 또는 `git status`에 `D` 두 건.
- [ ] AC2: `python3 -c "import json;d=json.load(open('.claude-plugin/marketplace.json'));a=d['plugins'][0]['agents'];print(len(a), any('spec-sync' in x for x in a))"` → `4 False` (JSON parse 성공 포함).
- [ ] AC3: `.codex/agents/README.md` Agent Set 목록이 4항목이고 `spec-sync-agent`가 없다. README 본문의 "custom agent를 spawn하는 스킬" 서술이 남은 4 agent 기준으로 여전히 참이다(인용).
- [ ] AC4: `grep -c "agent 5종" README.md` → `0`이고, 같은 줄이 4종 열거(`plan-review`·`implementation-review`·`simplicity-review`·`pr-review`)로 바뀌었다(인용).

**Target Files**:
- [D] `.claude/agents/spec-sync-agent.md` -- 계약이 SKILL로 이관돼 불필요
- [D] `.codex/agents/spec-sync-agent.toml` -- 동일
- [M] `.claude-plugin/marketplace.json` -- agents 배열에서 제거
- [M] `.codex/agents/README.md` -- Agent Set에서 제거
- [M] `README.md` -- "custom agent 5종" → 4종 문구 정정

### Task 4: 전수 census 검증 (read-only)

agent 삭제와 dispatch 문구 제거는 변형 표기가 흩어지는 sweep이므로 잔존을 전수 grep으로 닫는다. **In 표면 밖(특히 `_sdd/spec/**`)의 히트는 수정하지 않고 `spec-sync` 이관 항목으로 보고하며 census 통과로 간주한다.**

**Acceptance Criteria**:
- [ ] AC1: `grep -rni "spec-sync-agent\|spec_sync_agent\|spec sync agent" --include="*.md" --include="*.toml" --include="*.json" .` 결과에 In 표면 히트가 0건이다(`_sdd/`·`.sdd-workbench/`·`_COMMENTS.md`·spec 표면 제외, 제외분은 이관 목록으로 보고). 접미사 없는 계수 표기도 함께 본다 — `grep -rni "agent 5종\|5 custom agent\|agents.*5종" --include="*.md" .` In 표면 히트 0건.
- [ ] AC2: `grep -rn "표면 묶음\|본문 ∥ 기록\|호출자 표면 한정\|Implemented Sync Digest" --include="*.md" --include="*.toml" .` 결과에 In 표면 히트가 0건이다.
- [ ] AC3: 다른 4 agent의 등록·dispatch는 온전하다 — `grep -c "agents/" .claude-plugin/marketplace.json` → `4`, `grep -rn "subagent_type=\"sdd-skills:" .claude/skills/*/SKILL.md`가 plan-review·implementation-review·pr-review 3 스킬에서 여전히 매칭된다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- 표면 묶음 병렬(v4.6.24)이 가져온다던 벽시계 이득을 포기하는 결정: **폐지로 결정, 확신도 높음**. 근거는 ① 그 효과가 main.md에 `🚧 Planned`(미관측)로 남아 있고 ② 메인 루프가 이미 맥락을 보유해 digest 선고정·재읽기 왕복이 순손실이며 ③ 사용자 명시 지시("agent로 할 이유가 없어")다. agent 경유의 다른 이득인 메인 루프 컨텍스트 격리(spec 파일 읽기가 메인 컨텍스트를 차지하지 않음)도 함께 잃지만 수용한다. 사용자 확인 불필요.
- codex 두 절에서 무엇을 보존할지: **spawn/wait 문법과 무관한 경로·네임스페이스 규약만 보존**으로 결정, 확신도 중. 두 절 문면이 전부 spawn lifecycle·framed payload 규약이면 보존 대상은 0이고 AC2는 완전 일치로 닫힌다. 사용자 확인 불필요(구현 중 문면 인용으로 판정).
- 사후 정합 점검 2종을 함께 없앨지: **존치로 결정, 확신도 중**. 병렬 writer 발산 위험은 사라지지만 단일 작성자도 버전 불일치·기록 파일 실수 수정을 낼 수 있고 비용이 grep 2회뿐이다. 사용자 확인 불필요.
