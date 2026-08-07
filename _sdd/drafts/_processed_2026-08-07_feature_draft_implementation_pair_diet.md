# Feature Draft: implementation pair diet

> 규모 판정: 적격 — 세 쌍의 기존 Markdown/TOML 표면 6개에서 ownership 중복을 제거하는 단일 contract 변경이며, 수정 Task 1과 마지막 read-only census Task 2의 대응을 눈검산할 수 있다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
`implementation`이 post-review fix 정책과 실행 중 분할 신호의 canonical producer가 되도록 책임을 좁힌다. 롤링 분할의 draft 형식·planned handoff는 `feature-draft`의 `분할 방법 (롤링)`을 가리키고 재서술하지 않는다. resume ledger에는 기존 테스트 계약 오류와 구별되는 `계획 이탈·발견` 필드를 추가해, source task에서 달라진 판단이나 새 edge case의 이유·처리를 compact 뒤에도 복원한다.

`implementation-review` wrapper는 plan 없는 호출의 대화 digest를 실행 Step 1 한 곳에서만 정의하고, `implementation-review-agent`는 no-file 경계를 Hard Rule 한 곳에 둔다. review pair는 finding을 분류·relay할 뿐 fix 횟수·선택 정책을 다시 소유하지 않는다.

판단 근거: fix 시점·횟수는 실제로 코드를 쓰는 producer가 소비하므로 `implementation`, 파일 비변경은 reviewer가 직접 지켜야 하므로 agent Hard Rule, 대화-only context framing은 dispatch 직전 wrapper를 canonical home으로 골랐다. component별 task 분리는 하나의 fix ownership 변경을 여러 task가 공동 소유하게 하므로 기각했고, mirror 원자성과 single-owner 검증을 위해 여섯 파일을 한 수정 task에 둔다. 확신도는 높고 이미 planned P0 5/5가 같은 방향을 고정했으므로 추가 사용자 확인은 필요하지 않다.

## Scope
- **In**: Claude/Codex `implementation` SKILL, `implementation-review` wrapper, `implementation-review-agent`; fix 정책 single-home, split pointer, ledger implementation-notes field, no-plan/no-file 재천명 통합
- **Out**: RED→GREEN·coverage delta·테스트 계약 오류 의미론, reviewer 2-lens topology·severity·Fresh Verification·반환 schema, simplicity reviewer, runtime adapter, 신규 reference/agent/file
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | post-review fix 정책 single-home | `.claude/skills/implementation/SKILL.md`<br>`.codex/skills/implementation/SKILL.md`<br>`.claude/skills/implementation-review/SKILL.md`<br>`.codex/skills/implementation-review/SKILL.md`<br>`.claude/agents/implementation-review-agent.md`<br>`.codex/agents/implementation-review-agent.toml` | `rg -l 'fix 1회' <six exact paths>` → 구현 전 6개 전부, 구현 후 `implementation/SKILL.md` 두 경로만 | Task 1 |
| P2 | split pointer + ledger implementation notes | `.claude/skills/implementation/SKILL.md`<br>`.codex/skills/implementation/SKILL.md` | `rg --files .claude/skills/implementation .codex/skills/implementation -g 'SKILL.md'` → 두 exact path | Task 1 |
| P3 | no-plan digest + no-file 경계 단일 홈 | `.claude/skills/implementation-review/SKILL.md`<br>`.codex/skills/implementation-review/SKILL.md`<br>`.claude/agents/implementation-review-agent.md`<br>`.codex/agents/implementation-review-agent.toml` | `rg --files .claude/skills/implementation-review .codex/skills/implementation-review -g 'SKILL.md'; rg --files .claude/agents .codex/agents -g 'implementation-review-agent.*'` → wrapper 2 + agent 2 exact paths | Task 1 |

# Part 2: Tasks

### Task 1: implementation producer와 review pair의 판단 홈을 정리한다
항상 읽히는 짧은 실행 계약은 inline으로 유지하되, 같은 판단의 owner만 하나로 만든다. 신규 reference는 만들지 않는다.

**Contracts**:
- `implementation`은 post-review 정책의 단일 홈이다: gate 단일 패스, Critical/High/Medium fix 1회, correctness Low 3조건, simplicity Low advisory, finding 과다 재리뷰 권고를 소유한다. wrapper/agent는 finding 분류와 relay 책임만 가진다.
- 실행 중 규모 초과 시 `implementation`은 사유·닫힌 task 경계·잔여 scope를 반환하고 `feature-draft`의 `분할 방법 (롤링)`으로 복귀시킨다. draft marker·planned sync 형식은 producer를 가리키며 복사하지 않는다.
- ledger task row의 `계획 이탈·발견`은 source draft/inline task에서 달라진 판단 또는 새 edge case를 `건수; 내용 → 이유 → 처리`로 기록하고 없으면 `0`으로 닫는다. 테스트/check 가정 오류를 세는 기존 `계약 오류 선언 횟수`와 별도 필드다.
- reviewer agent의 파일 비변경은 Hard Rule 1이 단일 홈이고, AC는 positive output(`최종 응답 하나`)만 검증한다. wrapper의 plan 없는 호출 digest는 실행 Step 1의 단일 bullet이 소유한다.

**Acceptance Criteria**:
- [ ] AC1: `rg --count-matches --include-zero 'fix 1회' <six exact paths>`가 Claude/Codex `implementation/SKILL.md`에 각 `1`, wrapper·agent 네 파일에 각 `0`을 출력한다.
- [ ] AC2: `rg --count-matches --include-zero '단일 패스.*fix|fix.*1회' <four review paths>`가 전부 `0`이고, `rg -n '호출자 소관' <two agent paths>`가 C/H/M·Low의 fix 판단 주체를 각 agent에서 인용한다.
- [ ] AC3: `sed -n '/1\. \*\*단일 세션 초과\*\*/,/2\. \*\*계약 오류 반복\*\*/p' <each implementation>` 출력은 `feature-draft`·`분할 방법 (롤링)`·사유·닫힌 task 경계·잔여 scope를 각 1회 포함하고 `Part 1|마커|planned todo|spec-sync`는 0건이다.
- [ ] AC4: `sed -n '/## Implementation Ledger/,/## Process/p' <each implementation>` 출력은 `계획 이탈·발견`·`이유`·`처리`·`없으면 0`을 포함하고 `계약 오류 선언 횟수`를 별도 field로 유지한다.
- [ ] AC5: `계획 이탈·발견` 정의는 source task의 변경과 새 edge case만 기록하고 명령 출력 전문·서술형 진행기를 금지하는 기존 resume-only 경계를 넓히지 않는다(명시 rubric + reviewer 인용 근거로 MET/NOT MET 판정).
- [ ] AC6: `sed -n '/1\. 다음을 수집한다/,/2\. /p' <each wrapper>` 안에서 `대화에만 있는 맥락 digest`가 각 1건이고, 같은 bullet이 plan 있으면 축약·plan 없으면 구현 의도와 범위 전달을 모두 포함한다.
- [ ] AC7: `rg --count-matches --include-zero '리포트 파일을 만들지|파일을 생성하지' <two agent paths>`가 각 `0`, `rg --count-matches --include-zero '어떤 파일도 생성/수정/삭제하지 않는다'`가 각 `1`이다. `sed -n '/## Acceptance Criteria/,/## Hard Rules/p'`의 AC4는 `최종 응답 하나`만 positive contract로 검증한다.

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- fix 정책 canonical home, split pointer, ledger 필드
- [M] `.codex/skills/implementation/SKILL.md` -- Claude 의미 mirror
- [M] `.claude/skills/implementation-review/SKILL.md` -- no-plan digest 단일 정의, fix 정책 재천명 제거
- [M] `.codex/skills/implementation-review/SKILL.md` -- 동일 의미 + Codex runtime adapter 보존
- [M] `.claude/agents/implementation-review-agent.md` -- no-file Hard Rule 단일 홈, chain fix 횟수 제거
- [M] `.codex/agents/implementation-review-agent.toml` -- 동일 core + Codex agent boundary 보존

### Task 2: target 전수 census와 보호 계약을 read-only로 검증한다
Task 1의 수정과 분리해 변형 문구 잔존, mirror/runtime drift, 신규 surface를 마지막에 전수 검사한다. 파일은 수정하지 않는다.

**Acceptance Criteria**:
- [ ] AC8: `diff -u .claude/skills/implementation/SKILL.md .codex/skills/implementation/SKILL.md`가 exit 0이다. 두 파일 각각에서 `RED를 관찰하기 전`, `READY → RED_CONFIRMED → GREEN_CONFIRMED → DELTA_CLOSED`, `변이 확인`, `2회 이상`, `AC→증거 테이블`, fix 후 `회귀` anchor를 `rg --count-matches --include-zero`로 확인해 전부 1건 이상이다.
- [ ] AC9: Python `tomllib`로 Codex agent를 parse한 뒤 `developer_instructions`를 추출하고, Claude는 첫 frontmatter를 제거한다. Codex의 `## Codex Agent Boundary` 블록과 양쪽 마지막 `Source Pointer` 줄만 제거한 결정적 normalized core를 비교해 exact match를 얻으며, 네 Source Pointer는 별도 AC10·AC12에서 검증한다.
- [ ] AC10: 두 wrapper에서 `correctness 분할표`, simplicity `참조`·`국소`, 모든 reviewer 동시 dispatch, ledger `연접`, `합산 severity`, `dedup하지`, `relay` anchor를 `rg --count-matches --include-zero`로 확인해 각 runtime에서 1건 이상이다. 각 wrapper의 Source 줄은 같은 runtime의 correctness·simplicity agent exact path를 모두 가리킨다.
- [ ] AC11: Claude wrapper에서 `Agent(`·`prompt=`와 `sonnet|opus|haiku|fable`, Codex wrapper에서 `Mailbox contract`·`Target/close contract`·`## Runtime Boundary`·`message`·`reasoning_effort`를 경로별 `rg`로 확인해 전부 1건 이상이다.
- [ ] AC12: 각 agent에서 checkbox 4개, numbered Hard Rule 7개, graceful degradation numbered item 3개, 읽기 범위 numbered item 3개, severity 4개, Return 필드 `Status|Findings|Verification ledger|Recommendations|Assumptions` 5개를 section-boundary Python assertion으로 확인한다. `Fresh Verification`, `## Error Handling`, `## Final Check`도 각 1건이고, Source Pointer는 같은 runtime wrapper exact path를 가리킨다.
- [ ] AC13: 구현 전 ledger header에 여섯 parent surface의 `git status --short` baseline을 기록한다. 구현 후 같은 scoped command의 set difference가 여섯 Target Files의 `M`만 추가하고 관련 directory 아래 새 `??`·`A`·`D`가 0건인지 비교한다. `git diff --name-only -- <six exact paths>`는 literal six-path 집합과 일치한다.
- [ ] AC14: 공식 `quick_validate.py`는 호환되는 Claude/Codex `implementation` 두 directory에서 각각 `Skill is valid!`다. 두 `implementation-review` wrapper는 Python YAML frontmatter parse로 기존 `argument-hint`를 포함해 성공하며 AC11 runtime anchor를 보존한다.
- [ ] AC15: `git diff --check`가 exit 0이고 target diff를 `docs/SKILL_AUTHORING_NORMS.md` §3.1·§3.2·§4 rubric으로 리뷰했을 때 새 판단 복제·항상 읽는 reference 분리·하드 게이트 근거 소실이 없다(명시 rubric + reviewer 인용 근거).

**Target Files**:
- [TBD] 없음 (read-only 검증)
