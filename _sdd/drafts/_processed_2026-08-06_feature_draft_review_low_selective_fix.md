# Feature Draft: 리뷰 후 Low finding 선택적 fix (plan-review · implementation-review correctness)

> 규모 판정: 적격 — 하나의 fix-정책 규칙을 3개 논리 지점(implementation SKILL · feature-draft SKILL · implementation-review-agent)에 적용, 각 지점은 claude+codex 미러 쌍이고 exact-path 전파(변형 표기 census 아님)라 눈검산 가능. 새 contract는 리뷰 fix-정책 1건뿐.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
리뷰 게이트(plan-review / implementation-review) 후 Low finding 처리를 두 게이트에서 일관된 **종단 정책 = "Critical/High/Medium은 항상 fix + Low는 메인 루프가 3조건으로 판단해 고칠만한 것만 선택 fix"**로 정한다. 두 게이트의 **현행 베이스라인은 서로 다르므로** 변화 방향도 다르다:

- **implementation 게이트 (완화)**: 현재 `SKILL.md:109`가 Low를 **무조건 fix하지 않고 advisory**로만 남긴다 → correctness 렌즈 Low에 한해 조건부 fix를 **허용**한다(제약 완화).
- **feature-draft 게이트 (판단 가드 추가·명시화)**: 현재 `SKILL.md:89`는 severity **무구분**으로 "finding은 직접 반영"이라 Low가 제약 없이 반영될 수 있는 암묵 상태다 → C/H/M 직접 반영 + Low는 3조건 조건부 반영으로 **명시화**한다. (blanket 반영에 판단 가드를 씌우는 방향이며, "판단해서 고칠만한 것만"이라는 사용자 의도와 일치.)

- **fix 기준(3조건 AND 게이트)**: Low finding 중 **저비용 AND 명백히 이득 AND 현재 change scope 내** 세 조건을 **모두** 만족하는 것만 fix하고, 나머지는 마감 요약/메시지에 advisory로 남긴다. 두 주관 조건(저비용·명백히 이득)은 게이트를 **좁히기만** 하며, 객관 조건 **`현재 change scope 내`가 churn·scope-creep 방지를 지탱하는 load-bearing conjunct**다 — 이 AND 구조 덕에 최악의 경우도 scope 내 Low를 더 고칠 뿐이라 원래 Low tier 취지가 보존된다. 단일 패스 유지(review loop·재리뷰 없음), scope 확장·사변적 개선은 계속 금지.
- **범위 제외(불변)**: implementation-review의 **simplicity 렌즈** Low는 정의상 "주관적 취향 — 동작-불변 동등 형태를 객관 증거로 제시할 수 없는 것"이라 취향 churn 방지를 위해 **advisory 유지**(변경 없음). `simplicity-review-agent.md:56`은 손대지 않는다.
- **불변 유지**: "finding 많으면 추가 리뷰 권장" 임계(Critical+High ≥ 3 또는 Medium ≥ 5)는 **pre-fix C/H/M** 기준 그대로 — Low 판단·fix는 이 카운트에 영향 없음. plan-review-agent의 Blocker Policy(`Critical/High만 blocker, Medium/Low는 advisory`)도 **차단 정책이지 fix 정책이 아니므로 유지**(Low는 여전히 blocker 아님).
- **기준 소유(단일 소스 아님 — 이중 게이트)**: fix 기준(3조건)은 계획시 fix와 구현시 fix라는 **서로 다른 생명주기의 독립 정책**으로, 각 호출 스킬(implementation·feature-draft SKILL)이 **자기 사본을 소유**한다. 리뷰 agent는 severity **분류만** 하고, fix disposition 문구는 "호출자의 선택적 fix/후속 권고 대상(기준은 호출 스킬 소관)"으로만 두어 기준을 agent에 중복 탑재하지 않는다. 사용처 2곳뿐이라 공유 config/추상화는 신설하지 않는다(YAGNI).

## Scope
- **In**: `implementation/SKILL.md`(Low fix 규칙), `feature-draft/SKILL.md`(Low carve-out 추가), `implementation-review-agent`(Low disposition 문구) — 각각 `.claude`/`.codex` 미러 쌍.
- **Out**: `simplicity-review-agent`(advisory 유지), `plan-review-agent`(Blocker Policy 유지), `implementation-review`·`plan-review` orchestrator SKILL(fix는 호출자 소관이라 이미 중립 — 변경 불필요), "추가 리뷰 권장" 임계 로직.
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | implementation 게이트 Low fix 규칙 | `.claude/skills/implementation/SKILL.md`, `.codex/skills/implementation/SKILL.md` (각 L109) | `grep -rn "Low finding은 fix하지 않고" .claude/skills .codex/skills` → 정확히 위 2개 매치 | Task 1 |
| P2 | feature-draft 게이트 Low fix 규칙 | `.claude/skills/feature-draft/SKILL.md`, `.codex/skills/feature-draft/SKILL.md` (각 L89 품질 게이트 항목) | `grep -rn "review loop는 돌리지 않고 finding은 작성자인 메인 루프가 직접 반영" .claude/skills .codex/skills` → 정확히 위 2개 매치 | Task 2 |
| P3 | impl-review-agent Low disposition 문구 | `.claude/agents/implementation-review-agent.md`, `.codex/agents/implementation-review-agent.toml` (각 L77) | `grep -rn "\`Low\`는 로그/후속 권고 대상이다" .claude/agents .codex/agents` → 정확히 위 2개 매치 | Task 3 |

# Part 2: Tasks

### Task 1: implementation 게이트 Low finding 선택적 fix 규칙으로 교체

**Contracts**: `implementation` 스킬의 품질 게이트(마감 3)에서 반환 Low finding 처리 규칙을 신설한다 — correctness 렌즈 Low는 3조건(저비용 AND 명백히 이득 AND 현재 change scope 내) 모두 충족 시에만 fix, simplicity 렌즈 Low는 advisory 유지. 규칙 문면은 객관 조건 `현재 change scope 내`가 게이트를 좁히는 load-bearing conjunct임을 드러내 두 주관 조건이 게이트를 넓히지 못하게 한다. 단일 패스·기존 fix 위생(§4 커버리지 델타 + 회귀 1회 재실행, 현행 L108)은 그대로 이 Low fix에도 적용된다("fix가 있었으면" 절이 이미 포괄).

**Acceptance Criteria**:
- [ ] AC1: `.claude/skills/implementation/SKILL.md`와 `.codex/skills/implementation/SKILL.md` 둘 다에서 `grep -c "Low finding은 fix하지 않고" <file>`가 `0` (기존 무조건-advisory 문장 제거됨).
- [ ] AC2: 두 파일 모두 새 규칙 문장이 존재하고, 그 문장이 (a) `correctness`(또는 implementation-review) 렌즈 Low의 조건부 fix, (b) 3조건 문구 `저비용`·`명백히 이득`·`현재`+`scope`, (c) `simplicity` 렌즈 Low의 advisory 유지, (d) 단일 패스 유지를 모두 명시한다 — `grep`으로 네 요소 각각 확인 가능.
- [ ] AC3: `Critical/High/Medium`을 fix 대상으로 두는 현행 L107 문장과 "추가 리뷰 권장" 임계(`Critical+High ≥ 3 또는 Medium ≥ 5`) 문장은 diff상 **변경 없음**(`git diff`에 해당 라인 미포함).
- [ ] AC4: `diff <(sed -n '/품질 게이트/,/마감 요약/p' .claude/skills/implementation/SKILL.md) <(sed -n '/품질 게이트/,/마감 요약/p' .codex/skills/implementation/SKILL.md)`가 빈 출력(두 미러의 해당 블록 byte-identical).

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- L109 Low 규칙 문장 교체
- [M] `.codex/skills/implementation/SKILL.md` -- 동일 교체(미러 parity)

### Task 2: feature-draft 게이트에 Low finding 선택적 fix carve-out 추가

**Contracts**: `feature-draft` 스킬의 품질 게이트(`plan-review` 단일 패스) fix 규칙을 severity로 분기한다 — Critical/High/Medium은 현행대로 직접 반영, Low는 3조건 모두 충족 시에만 반영하고 나머지는 마감 메시지에 advisory. 현재는 severity 무구분 "finding은 직접 반영한다"라 Low 처리가 암묵적이었던 것을 명시화한다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/skills/feature-draft/SKILL.md`와 `.codex/skills/feature-draft/SKILL.md` 둘 다 품질 게이트 항목에 Low 처리 문장이 추가되어, (a) Critical/High/Medium 직접 반영, (b) Low는 3조건(`저비용`·`명백히 이득`·`현재`+`scope`) 모두 충족 시에만 반영, (c) 나머지 Low는 advisory, (d) scope 확장·사변적 개선 금지 + 단일 패스 유지를 명시한다 — `grep`으로 각 요소 확인 가능.
- [ ] AC2 (구-blanket 축소 검증): 두 미러 모두에서 severity 무구분 blanket 절이 그대로 잔존하지 않는다 — `grep -c "finding은 작성자인 메인 루프가 직접 반영한다" <file>`가 `0`. (교체 후 문장은 severity를 명시하므로 이 정확 문자열이 사라진다. Task 1 AC1·Task 3 AC1과 대칭으로 구 문구 제거를 falsifiable하게 못박는다.)
- [ ] AC3: "추가 리뷰 권장" 임계(`Critical+High ≥ 3 또는 Medium ≥ 5`) 문장은 diff상 변경 없음.
- [ ] AC4: `diff` 로 `.claude`/`.codex` 두 feature-draft SKILL의 품질 게이트 항목 문장이 byte-identical(미러 parity).

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md` -- L89 품질 게이트 항목에 Low carve-out 추가
- [M] `.codex/skills/feature-draft/SKILL.md` -- 동일 추가(미러 parity)

### Task 3: implementation-review-agent의 Low disposition 문구를 "호출자 선택적 fix/권고"로 갱신

**Contracts**: `implementation-review-agent`는 severity **분류**만 소유하고, Low의 fix 여부·기준은 **호출 스킬**이 소유한다(중복 금지). 따라서 Low disposition 문구를 "로그/후속 권고 대상" → "호출자의 선택적 fix 또는 후속 권고 대상(기준은 호출 스킬이 단일 소스)"로만 갱신한다. Critical/High/Medium fix 대상 문구와 Step 5 severity 분류표(L72–75)는 그대로 둔다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/agents/implementation-review-agent.md`와 `.codex/agents/implementation-review-agent.toml` 둘 다에서 `grep -c "Low\`는 로그/후속 권고 대상이다" <file>`가 `0`.
- [ ] AC2: 두 파일 모두 갱신된 문장이 Low를 **호출자의 선택적 fix** 대상으로 표기하고 **fix 기준은 호출 스킬 소관**임을 명시한다(구체 3조건은 이 파일에 중복 기술하지 않는다 — agent는 기준을 담지 않는다).
- [ ] AC3: `Critical / High / Medium`을 fix 대상으로 두는 같은 문장 앞부분과 L72–75 severity 분류표는 diff상 변경 없음.
- [ ] AC4: 두 미러 파일의 해당 문장이 byte-identical.

**Target Files**:
- [M] `.claude/agents/implementation-review-agent.md` -- L77 Low disposition 문장 갱신
- [M] `.codex/agents/implementation-review-agent.toml` -- 동일 갱신(미러 parity)

# Open Questions
- plan-review-agent.md:26 Blocker Policy("Medium/Low는 advisory다")는 **차단 여부** 정책이라 유지하기로 결정했다(Low는 여전히 blocker 아님, fix 정책은 feature-draft SKILL 소유). 사용자 확인 불필요 — 결정 근거는 Change Summary에 기록.
