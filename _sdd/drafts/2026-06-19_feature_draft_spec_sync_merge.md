# Feature Draft: spec-update-todo + spec-update-done를 통합 status 분류 sync 스킬 `spec-sync`로 머지

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

SDD 파이프라인의 두 spec-sync 스킬을 단일 `spec-sync` 스킬/`spec-sync-agent`로 통합한다. 현재는 구현 전 planned delta 반영(`spec-update-todo`)과 구현 후 검증 사실 승격(`spec-update-done`)이 별도 스킬로 분리돼 있으나, 두 스킬은 공유 substrate(Repo-wide Invariant Test, main/supporting/history surface 매핑, Strategic Code Map 보수 반영 규율, `🚧 Planned` 표식 규율, sub-spec 링크 규율, 내레이션 억제)를 거의 동일하게 중복 보유한다.

통합의 핵심은 **단일 status 분류기가 파이프라인 위치에 자동 적응**한다는 점이다. 분류 축을 "코드 evidence 유무" 하나로 통일하면, 구현 전 호출은 evidence 부재로 모든 delta가 planned로 degrade되어 기존 todo 동작이 되고, 구현 후 호출은 코드 대조로 검증 사실을 승격하면서 잔여 planned를 분리해 기존 done 동작이 된다. 두 진입점(`spec-update-todo`/`spec-update-done`)을 별도 스킬로 유지할 필요가 없어진다.

global spec(`_sdd/spec/`)에 남길 persistent implication은 "어떤 코드를 거쳤는가"가 아니라 "spec sync 단계가 어떤 안전·승격 규율을 단일 진입점으로 보장하는가"다.

## Scope Delta

**In-scope:**
- 단일 진입점 `spec-sync`(스킬) + `spec-sync-agent`(agent)가 spec-sync 책임을 보유한다. 이전의 todo/done 이분 진입은 제거되고, evidence-driven status 분류가 그 둘을 흡수한다.
- spec-sync는 항목별로 status를 분류해 routing한다: 코드+validation evidence가 있는 항목만 현재 사실로 승격하고, evidence가 없는 항목은 `🚧 Planned`로 남기며, evidence가 약한 항목은 보류해 `Open Questions`로 노출한다.
- 단일 진입점으로도 두 안전 불변식(evidence 없으면 승격 금지, verified/planned 무표식 혼합 금지)이 유지된다.

**Out-of-scope (의도적 보존):**
- global spec의 thin-core 원칙, surface 매핑 규율, Repo-wide Invariant Test, Strategic Code Map 보수 반영 규율은 그대로 유지한다(통합 스킬이 한 번만 보유할 뿐 의미 변경 없음).
- 코드/구현 문서 직접 수정 금지(spec-sync 대상은 `_sdd/spec/`뿐)는 유지한다.
- feature draft `Part 1: Spec Delta` 마커·3섹션 형식은 변경하지 않는다(spec-sync의 입력 계약일 뿐).

**Guardrail delta:**
- spec sync 진입점은 단일 `spec-sync`로 수렴한다. global spec 수정은 `spec-sync-agent` 출력으로만 발생해야 한다(이전의 `spec-update-todo`/`spec-update-done` 이중 진입 가드레일을 단일 진입 가드레일로 대체).
- spec-sync는 evidence 없는 항목을 절대 완료 사실로 승격하지 않는다(기본값 = planned 또는 보류).

## Persistent Spec Implications

> 아래는 global spec에 남을 수 있는 repo-wide candidate다. 각 항목은 Repo-wide Invariant Test와 surface-fit 판단을 거쳐 guardrails / key decisions / navigation hint로 반영된다.

- **단일 spec-sync 진입점 (key decision 후보)**: global spec과 코드/계획의 동기화는 단일 `spec-sync` 스킬이 담당하며, 구현 전/후 구분은 별도 스킬이 아니라 evidence-driven status 분류로 처리한다. repo-wide operating rule이므로 `_sdd/` artifact handoff 규칙과 같은 surface에 속한다.
- **evidence-driven 승격 불변식 (guardrail 후보)**: spec sync는 코드+validation evidence가 있는 항목만 현재 사실로 승격하고, evidence 없는 항목은 기본적으로 `🚧 Planned` 또는 보류로 둔다. 미구현·미검증을 완료 사실로 쓰지 않는다는 이 안전성은 두 구 스킬에서 통합 스킬로 그대로 이전된다.
- **무표식 혼합 금지 불변식 (guardrail 후보)**: verified truth와 planned truth를 같은 문단·불릿에 표식 없이 섞지 않는다.
- **파이프라인 단계 명칭 갱신 (navigation hint)**: SDD 단계 순서에서 `spec sync todo`/`spec sync done` 두 단계는 단일 `spec-sync` 단계로 표기한다. 같은 스킬이 구현 전/후 어느 시점에 호출돼도 evidence로 적응한다.

<!-- spec-update-todo-input-end -->

# Part 2: Implementation and Validation Plan

## Overview

이 plan은 Part 1의 단일 `spec-sync` 진입점 결정을 실제 파일 변경으로 전개한다. 작업은 (1) 통합 agent 본문 생성, (2) claude/codex 양 진영 wrapper·skill.json 생성, (3) 두 구 스킬 트리의 hard-delete, (4) agent 등록 surface 갱신, (5) orchestrator·docs·교차 참조 갱신으로 나뉜다.

용어: 본 draft에서 "evidence-driven status 분류"는 각 delta 항목을 코드+validation evidence 유무로 IMPLEMENTED/VERIFIED·PARTIAL·PLANNED/NOT_IMPLEMENTED·UNVERIFIED 중 하나로 판정해 routing하는 메커니즘을 가리킨다(Part 1 Change Summary에서 도입한 개념). "두 안전 불변식"은 Part 1 Persistent Spec Implications의 evidence-driven 승격 불변식과 무표식 혼합 금지 불변식을 가리킨다.

## Scope

In-scope는 Part 1 Scope Delta의 In-scope를 실행 파일 단위로 전개한 것이다. 추가로, 통합 agent는 두 구 agent의 Input Sources 합집합(코드 변경 + `_sdd/implementation/*` + feature draft Part 1·Part 2 + user input + `_sdd/spec/user_spec.md`·`user_draft.md` + `_sdd/spec/decision_log.md`)을 입력으로 받고, 산출물로 `_processed_*` 마킹(구 todo 유래)과 단일 `Spec Sync Report`(구 done 유래, status 분류 컬럼 포함)를 모두 보존한다.

Out-of-scope: spec-sync agent 본문의 surface 매핑 규율·Repo-wide Invariant Test·Strategic Code Map 규율 자체의 재설계(기존 문구를 통합 보유만 하고 의미는 보존).

## Contract/Invariant Delta and Coverage

| ID | Type | Change | Covered By | Validated By |
|----|------|--------|------------|--------------|
| C1 | Add | 단일 `spec-sync-agent`가 evidence-driven status 분류로 구현 전/후 sync를 모두 수행한다 | T1 | V1 |
| C2 | Add | spec-sync agent는 항목별 status를 IMPLEMENTED·PARTIAL·PLANNED·UNVERIFIED 4분류로 routing하고, 도구는 Read·Write·Edit·Glob·Grep·Bash superset을 갖는다 | T1 | V1 |
| C3 | Add | spec-sync 산출물은 `_processed_*` 마킹과 단일 `Spec Sync Report`(status 컬럼 포함)를 모두 보존한다 | T1 | V2 |
| C4 | Add | claude·codex 양 진영에 `spec-sync` wrapper(SKILL.md+skill.json)가 존재하고 통합 description으로 구 트리거 문구를 흡수한다 | T2, T3 | V3 |
| C5 | Delete | `spec-update-todo`/`spec-update-done`의 skill·agent·codex mirror·skill.json은 완전히 제거된다(deprecated alias 미보존) | T4 | V4 |
| C6 | Modify | `spec-sync-agent`가 모든 agent 등록 surface(marketplace.json agents 배열, codex agents README, orchestrator-contract 허용목록)에 등록되고 구 agent 2개는 제거된다 | T5 | V5 |
| C7 | Modify | orchestrator·docs·교차 참조의 `spec-update-todo`/`spec-update-done` 언급이 단일 `spec-sync`로 갱신된다 | T6, T7 | V6 |
| I1 | Add | spec-sync는 코드+validation evidence가 있는 항목만 현재 사실로 승격하고, evidence 없는 항목은 기본 `🚧 Planned`/보류로 둔다 | T1 | V7 |
| I2 | Add | spec-sync는 verified truth와 planned truth를 같은 문단·불릿에 무표식으로 섞지 않는다 | T1 | V7 |
| I3 | Add | 모든 `subagent_type`/`agent_type` 호출값과 등록 목록에 dangling `spec-update-todo-agent`/`spec-update-done-agent` 참조가 0이고, `spec-sync-agent` 참조가 양 진영에서 일관된다 | T4, T5, T6 | V5 |

## Touchpoints

> 모두 현재 코드(2026-06-19) census로 재확인함. agent별 독립 vs 공유 파일을 구분한다. `Strategic Code Map`이 아니라 직접 grep으로 확인한 현재 surface다.

**A. 통합 agent 단일 소스 (신규 생성):**
- `.claude/agents/spec-sync-agent.md` — 두 구 agent의 공유 substrate를 한 번만 보유 + evidence-driven 분류 routing. claude agent 본문 단일 소스.
- `.codex/agents/spec-sync-agent.toml` — 위 본문의 codex mirror. 기존 `spec-update-done-agent.toml`의 `## Codex Agent Boundary` framing과 `name`/`description`/`developer_instructions` 구조를 따른다.

**B. wrapper + skill.json (신규 생성, claude/codex 각 1쌍):**
- `.claude/skills/spec-sync/SKILL.md` — claude entrypoint wrapper(`Agent(subagent_type="sdd-skills:spec-sync-agent")` dispatch). 기존 두 wrapper의 "계약 유지·흉내 금지" 구조를 따른다.
- `.claude/skills/spec-sync/skill.json` — `name`/`description`/`instruction_file`/`version`.
- `.codex/skills/spec-sync/SKILL.md` — codex entrypoint wrapper(`spawn_agent`/`wait_agent`/`close_agent` + Runtime Boundary framed payload). 기존 `.codex/skills/spec-update-done/SKILL.md`의 Codex Runtime Adapter 구조를 따른다.
- `.codex/skills/spec-sync/skill.json` — codex skill.json.

**C. 구 스킬 트리 hard-delete:**
- `.claude/skills/spec-update-todo/` (SKILL.md + skill.json), `.claude/skills/spec-update-done/` (SKILL.md + skill.json)
- `.claude/agents/spec-update-todo-agent.md`, `.claude/agents/spec-update-done-agent.md`
- `.codex/skills/spec-update-todo/` (SKILL.md + skill.json), `.codex/skills/spec-update-done/` (SKILL.md + skill.json)
- `.codex/agents/spec-update-todo-agent.toml`, `.codex/agents/spec-update-done-agent.toml`

**D. 등록 surface (공유 파일, 순차 편집):**
- `.claude-plugin/marketplace.json` — `skills` 배열(구 2개 제거 + `spec-sync` 추가), `agents` 배열(구 2개 제거 + `spec-sync-agent.md` 추가). 등록 누락 사고 이력(simplicity-review-agent) 있으므로 명시 처리.
- `.codex/agents/README.md` — agent 목록에서 구 2개 제거 + `spec-sync-agent` 추가.

**E. orchestrator 계약/참조 (공유 파일, 순차 편집):**
- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` — 허용 subagent_type 목록(L48,L54)·spec sync ordering·acceptance 섹션(L102, L203-210)에서 구 2개 → `spec-sync-agent`.
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` — §1.6, 파이프라인 다이어그램(L104,L119), 단계 설명(L161,L175).
- `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` — Step 3/Step 4/Step 7의 spec-update-todo/done 단계와 subagent_type 값.
- `.claude/skills/sdd-autopilot/SKILL.md` — AC7(L23), Hard Rule 1·13·14(L53,L65,L66), L163(조건부 추가 규칙), Step closing(L305).
- `.claude/skills/sdd-autopilot/scripts/validate_orchestrator.py` — 허용 agent 이름 목록(있으면).
- `.codex/skills/sdd-autopilot/` 대응 미러(`SKILL.md`, `references/orchestrator-contract.md`, `references/sdd-reasoning-reference.md`, `examples/sample-orchestrator.md`, `scripts/validate_orchestrator.py`).
- `AGENTS.md` §3 (L22-23) — `(spec sync todo)`/`spec sync done` → 단일 `spec-sync`.
- 다른 producer/reviewer agent 본문의 downstream skill-name 참조 (claude `.md` + codex `.toml` 쌍, T6 소유): `spec-review-agent`(claude L181-182·L240-241 / codex 동일 라인) "계획 변경 전 반영: `spec-update-todo`"·"구현 완료 후 동기화: `spec-update-done`"·Integration 목록; `implementation-agent`(claude/codex L39) "호출자가 `spec-update-todo`로 처리"; `implementation-plan-agent`(claude/codex L43·L385/L390) "spec 변경 시 `spec-update-todo` 후속 제안"·Integration; `implementation-review-agent`(claude L204 / codex L200) "`spec-update-todo` / `spec-update-done` 후속 안내". 모두 downstream skill 명칭 참조라 단일 `spec-sync`로 rename(마커 토큰 없음 — 보존 대상 아님).
- `AGENTS.md` harness 정본 template 4부(`spec-create`/`spec-upgrade` × claude/codex의 `references/agents-harness-template.md` L30-31) — `## 3. SDD 워크플로우` 단계 순서의 `(spec sync todo)`/`spec sync done` 파이프라인 단계 라벨. 4부는 byte-identical 미러(components.md L78이 명시)이므로 동일 rename을 4부에 일괄 적용한다(`spec-create`의 claude 본문이 정본, 나머지 3부는 그 미러). 단계 라벨이 SDD 단계 명칭(`feature-draft`·`implementation-plan` 등 실제 스킬 단계와 나란히 나열됨)을 가리키므로 `spec-sync`로 통일. T6 소유.

**F. 비-autopilot 참조 (공유 파일, 순차 편집):**
- `docs/SDD_WORKFLOW.md`, `docs/en/SDD_WORKFLOW.md` — spec-update-todo/done 언급.
- `docs/AUTOPILOT_GUIDE.md`, `docs/en/AUTOPILOT_GUIDE.md` — 파이프라인 표·다이어그램·slash command 표·codex 디렉토리 트리.
- `.claude/skills/implementation/SKILL.md` — spec drift 안내 문구(L25)에서 `spec-update-todo` → `spec-sync`. `spec-update-done` 소비 호환 언급(L87,L227)은 산출물 형식 보존이므로 명칭만 갱신.
- `.codex/skills/implementation/SKILL.md` — 위 대응.
- `.claude/skills/pr-review/SKILL.md`, `.codex/skills/pr-review/SKILL.md`, `.claude/skills/pr-review/examples/sample-review.md`, `.codex/skills/pr-review/examples/sample-review.md` — `/spec-update-todo`(`$spec-update-todo`) 안내. SKILL.md·예시 모두 claude/codex 짝 대칭 편입.
- `.claude/skills/guide-create/references/tool-and-gates.md`, `.codex/skills/guide-create/references/tool-and-gates.md` — `spec-update-todo` 선택지 문구(L60).
- `_sdd/spec/usage-guide.md` — slash command 카탈로그 `/spec-update-todo`(L37)·`/spec-update-done`(L42) + Scenario 2 Expected Result 산문(L62)의 bare `spec-update-todo`/`spec-update-done`. spec 본문이 아닌 사용자 대상 운영 카탈로그라 T7이 직접 명칭 rename(dead-link 정리). 파일 단위 0건으로 처리(라인 열거 대신).
- `_sdd/spec/components.md` — Strategic Code Map dangling 행: L16 `spec-update-todo` 행·L17 `spec-update-done` 행(Primary Source가 T4 삭제 대상 skill/agent 파일을 가리킴)·L80 `Spec sync map promotion` 행(Source가 `spec-update-done-agent.md`/`.toml`을 가리킴). T4 hard-delete 후 세 행은 존재하지 않는 파일을 가리키는 dead-link가 된다. usage-guide.md와 동일 성격의 dead-link 정리(구 component 2개 entry → `spec-sync` 단일 entry, L80은 `spec-sync-agent`로)로 T7이 소유한다 — 이는 contract/invariant 본문(normative truth는 main.md) 의미 변경이 아니라 reference-only supporting surface(L3-4가 명시: "normative decision-bearing truth는 main.md에 두고 여기에는 navigation note만")의 stale source pointer 정리다.
- `.claude/agents/feature-draft-agent.md`, `.codex/agents/feature-draft-agent.toml` — Integration의 downstream skill 명칭 참조(rename 대상)와 input 마커 토큰(보존 대상)이 공존. 명칭만 갱신, 마커 보존(T6 소유).

## Implementation Phases

- **Phase 1 — 통합 소스 작성**: T1(agent 본문). 모든 wrapper·등록·참조가 의존하는 단일 소스이므로 선행한다.
- **Phase 2 — wrapper·등록·삭제**: T2(claude wrapper), T3(codex wrapper), T4(구 트리 삭제), T5(등록 surface). T2/T3는 파일 disjoint이나 모두 T1의 agent name 계약을 소비하므로 T1에 의존. T4는 T5와 dangling 참조 mutex 관계(삭제 후 등록 목록에 구 agent가 남으면 안 됨)이므로 T5가 T4에 의존.
- **Phase 3 — orchestrator·docs 참조 갱신**: T6(autopilot 계약/참조 + AGENTS.md + producer/reviewer agent 4쌍 + harness template 4부), T7(docs + 비-autopilot 스킬 + usage-guide·components.md). 둘 다 새 `spec-sync` 이름 계약(T1·T2·T3 확정)에 의존. T6(`.claude/agents`·`.codex/agents`·autopilot·harness template)와 T7(docs·implementation·pr-review·guide-create·`_sdd/spec`)은 파일 disjoint이며 병렬 가능.

## Task Details

### Task T1: 통합 `spec-sync-agent` 본문을 claude/codex 양 진영에 작성
**Priority**: P0
**Type**: Feature

**Description**: 두 구 agent(`spec-update-todo-agent`, `spec-update-done-agent`)의 공유 substrate를 한 번만 보유하고, evidence-driven status 분류로 구현 전/후 sync를 모두 수행하는 단일 agent 본문을 작성한다. `.claude/agents/spec-sync-agent.md`를 단일 소스로 작성하고 `.codex/agents/spec-sync-agent.toml`을 그 본문의 codex mirror(`## Codex Agent Boundary` framing + `name`/`description`/`developer_instructions`)로 작성한다.

본문 구성:
- **Input Sources**: 두 구 agent의 합집합 — 실제 코드 변경, `_sdd/implementation/*`(plan/progress/review/report glob), feature draft Part 1 `Persistent Spec Implications`·Part 2 `Contract/Invariant Delta and Coverage`, user 대화, `_sdd/spec/user_spec.md`·`user_draft.md`, `_sdd/spec/decision_log.md`.
- **Status 분류 routing** (C2): 각 delta 항목을 코드+validation evidence 기준으로 분류 — IMPLEMENTED/VERIFIED(evidence 있음) → 현재 사실로 무표식 승격, PARTIAL → 구현분=사실/잔여=`🚧 Planned` 분리, PLANNED/NOT_IMPLEMENTED(evidence 없음) → `🚧 Planned` 표식, UNVERIFIED(코드 있으나 검증 약함) → 보류 → `Open Questions`.
- **파이프라인 위치 자동 적응**: 구현 전 호출은 evidence 부재로 모든 항목이 PLANNED로 degrade(구 todo 동작), 구현 후 호출은 코드 대조로 IMPLEMENTED 승격 + 잔여 PLANNED 혼합 처리(구 done 동작)임을 본문에 명시한다.
- **공유 substrate**(두 구 agent에서 글자 단위 동일한 부분을 한 번만): Repo-wide Invariant Test, main/supporting/history surface 매핑, Strategic Code Map 보수 반영 규율, `🚧 Planned` 표식 규율, sub-spec 링크 규율(고아 파일 금지), 내레이션 억제.
- **안전 Hard Rule** (I1, I2): evidence 없으면 승격 금지(기본값 PLANNED/보류); verified와 planned를 같은 문단·불릿에 무표식 혼합 금지. 이 두 규칙을 Hard Rule로 명시한다.
- **산출물**(C3): 처리한 input file `_processed_*` 마킹 + 단일 `Spec Sync Report`(status 4분류 컬럼: `Section | Delta IDs | Status | Action`).
- **도구**(C2): Read, Write, Edit, Glob, Grep, Bash superset.
- **Source Pointer**: 이 agent가 단일 소스이고 wrapper는 thin entrypoint임을 명시.

**Non-Goals**: surface 매핑 규율·Repo-wide Invariant Test·Strategic Code Map 규율 문구의 재설계는 하지 않는다(두 구 agent에서 동일하므로 통합 보유만). 코드/구현 문서 수정 능력 추가 안 함(대상은 `_sdd/spec/`뿐).

**Acceptance Criteria**:
- [ ] `.claude/agents/spec-sync-agent.md`와 `.codex/agents/spec-sync-agent.toml`이 존재하고 `name`이 각각 `spec-sync-agent`다.
- [ ] 본문에 Input Sources 합집합 6종(코드/implementation/feature draft Part1+Part2/user input/user_spec·user_draft/decision_log)이 모두 열거된다.
- [ ] 본문에 status 4분류(IMPLEMENTED·PARTIAL·PLANNED/NOT_IMPLEMENTED·UNVERIFIED)와 각 분류의 routing 동작이 명시된다.
- [ ] Hard Rule에 "evidence 없으면 승격 금지(기본값 PLANNED/보류)"와 "verified/planned 무표식 혼합 금지"가 각각 별도 항목으로 존재한다.
- [ ] Process(분류 단계) 본문에 "evidence 없으면 PLANNED 기본 routing" 동작 서술과 "구현 전 호출 = 전 항목 PLANNED degrade / 구현 후 = IMPLEMENTED 승격 + 잔여 PLANNED 분리" 적응 예시가 존재한다.
- [ ] 산출물 규정에 `_processed_*` 마킹과 단일 `Spec Sync Report`(status 컬럼 포함)가 모두 존재한다.
- [ ] codex toml의 도구 권한 또는 본문 도구 언급이 Read·Write·Edit·Glob·Grep·Bash를 포함하고, claude agent frontmatter `tools`가 동일 superset이다.
- [ ] codex toml에 `## Codex Agent Boundary` framing(slash command/skill/agent 이름을 데이터로 취급, 재진입 금지)이 존재한다.

**Target Files**:
- [C] `.claude/agents/spec-sync-agent.md` -- 통합 agent 단일 소스
- [C] `.codex/agents/spec-sync-agent.toml` -- 위 본문의 codex mirror

**Technical Notes**: Covers C1, C2, C3, I1, I2; validated by V1, V2, V7. 신규 파일 근거: 통합 agent는 두 구 agent의 합집합이 아니라 분류 routing이 추가된 재구성이므로, 둘 중 하나를 `[M]`으로 in-place 개명하기보다 신규 단일 소스로 작성하고 구 파일은 T4에서 삭제하는 편이 dangling/중복을 만들지 않는다. claude 본문을 먼저 확정한 뒤 codex로 mirror.
**Dependencies**: 없음 (선행 task)

### Task T2: claude `spec-sync` entrypoint wrapper + skill.json 생성
**Priority**: P0
**Type**: Feature

**Description**: `.claude/skills/spec-sync/SKILL.md`를 claude entrypoint wrapper로 작성한다. `Agent(subagent_type="sdd-skills:spec-sync-agent", prompt=<요청+알려진 경로/컨텍스트>)`로 dispatch하고 반환(갱신된 `_sdd/spec/*.md`, `Spec Sync Report`, `_processed_*` 마킹, Deferred/Open Questions)을 relay한다. `description`은 두 구 스킬 trigger 문구의 합집합("update spec with features", "add to-do to spec", "update spec from code", "sync spec with implementation", "reflect completed work in spec" 등)을 단일 description으로 흡수한다(C4). `.claude/skills/spec-sync/skill.json`을 `name`=`spec-sync`, `instruction_file`=`SKILL.md`로 작성한다.

**Acceptance Criteria**:
- [ ] `.claude/skills/spec-sync/SKILL.md`가 `sdd-skills:spec-sync-agent`를 dispatch 대상으로 지정한다.
- [ ] frontmatter `description`이 구 todo 트리거 문구와 구 done 트리거 문구를 모두 포함한다(미구현 계획 반영 + 구현 완료 sync 양쪽 호출이 이 스킬로 라우팅된다).
- [ ] `.claude/skills/spec-sync/skill.json`의 `name`이 `spec-sync`이고 `instruction_file`이 `SKILL.md`다.
- [ ] wrapper가 `_processed_*` 마킹과 `Spec Sync Report` relay를 명시한다.

**Target Files**:
- [C] `.claude/skills/spec-sync/SKILL.md` -- claude wrapper
- [C] `.claude/skills/spec-sync/skill.json` -- claude skill metadata

**Technical Notes**: Covers C4; validated by V3. 기존 `.claude/skills/spec-update-*/SKILL.md`의 "계약(entrypoint·artifact 유지, 흉내 금지)" 구조를 따른다.
**Dependencies**: T1 (agent name 계약 소비)

### Task T3: codex `spec-sync` entrypoint wrapper + skill.json 생성
**Priority**: P0
**Type**: Feature

**Description**: `.codex/skills/spec-sync/SKILL.md`를 codex entrypoint wrapper로 작성한다. 기존 `.codex/skills/spec-update-done/SKILL.md`의 Codex Runtime Adapter 구조(`tool_search`로 multi-agent tools 로드 → `spawn_agent`/`wait_agent`/`close_agent`, framed payload `## Runtime Boundary`/`## Mode`/`## Input Data`)를 따르되 `agent_type`을 `spec-sync-agent`로, Mode를 통합 단일 모드(예: `spec-sync`)로 설정한다. `.codex/skills/spec-sync/skill.json`을 claude skill.json과 동일 `name`/`description`/`instruction_file`로 작성한다.

**Acceptance Criteria**:
- [ ] `.codex/skills/spec-sync/SKILL.md`가 `spawn_agent({agent_type: "spec-sync-agent", ...})`를 dispatch 대상으로 지정한다.
- [ ] framed payload `## Runtime Boundary`/`## Mode`/`## Input Data` 구조가 존재하고 Mode가 단일 통합 모드다.
- [ ] `description`이 T2 claude wrapper와 동일한 통합 트리거 문구 집합을 포함한다.
- [ ] `.codex/skills/spec-sync/skill.json`의 `name`이 `spec-sync`다.

**Target Files**:
- [C] `.codex/skills/spec-sync/SKILL.md` -- codex wrapper
- [C] `.codex/skills/spec-sync/skill.json` -- codex skill metadata

**Technical Notes**: Covers C4; validated by V3. claude/codex wrapper의 description 문구가 일치해야 trigger 동치성이 보장된다.
**Dependencies**: T1 (agent name 계약 소비)

### Task T4: 구 spec-update-todo/done 트리 hard-delete
**Priority**: P0
**Type**: Refactor

**Description**: 두 구 스킬의 claude/codex skill 트리, claude/codex agent 파일을 완전히 제거한다. deprecated alias는 남기지 않는다(내부 dogfooding repo, alias 가치 낮음). 구 트리거 문구는 T2·T3의 통합 description이 이미 흡수했다.

**Acceptance Criteria**:
- [ ] 아래 8개 경로가 모두 삭제된다: `.claude/skills/spec-update-todo/`, `.claude/skills/spec-update-done/`, `.claude/agents/spec-update-todo-agent.md`, `.claude/agents/spec-update-done-agent.md`, `.codex/skills/spec-update-todo/`, `.codex/skills/spec-update-done/`, `.codex/agents/spec-update-todo-agent.toml`, `.codex/agents/spec-update-done-agent.toml`.
- [ ] 삭제 후 리포지토리에 `spec-update-todo`/`spec-update-done` skill 폴더나 agent 파일이 남지 않는다.

**Target Files**:
- [D] `.claude/skills/spec-update-todo/SKILL.md`
- [D] `.claude/skills/spec-update-todo/skill.json`
- [D] `.claude/skills/spec-update-done/SKILL.md`
- [D] `.claude/skills/spec-update-done/skill.json`
- [D] `.claude/agents/spec-update-todo-agent.md`
- [D] `.claude/agents/spec-update-done-agent.md`
- [D] `.codex/skills/spec-update-todo/SKILL.md`
- [D] `.codex/skills/spec-update-todo/skill.json`
- [D] `.codex/skills/spec-update-done/SKILL.md`
- [D] `.codex/skills/spec-update-done/skill.json`
- [D] `.codex/agents/spec-update-todo-agent.toml`
- [D] `.codex/agents/spec-update-done-agent.toml`

**Technical Notes**: Covers C5; validated by V4. T2/T3가 통합 description으로 트리거를 흡수한 뒤 삭제해야 trigger 공백이 생기지 않으므로 T2·T3에 의존. 통합 agent 본문(T1) 작성 시 구 agent 본문을 참조 소스로 읽으므로 T1 이후 삭제.
**Dependencies**: T1, T2, T3

### Task T5: agent/skill 등록 surface에서 구 2개 제거 + spec-sync 등록
**Priority**: P0
**Type**: Infrastructure

**Description**: 모든 등록 surface를 갱신한다. `.claude-plugin/marketplace.json`의 `skills` 배열에서 `./.claude/skills/spec-update-todo`·`./.claude/skills/spec-update-done`를 제거하고 `./.claude/skills/spec-sync`를 추가, `agents` 배열에서 `./.claude/agents/spec-update-todo-agent.md`·`./.claude/agents/spec-update-done-agent.md`를 제거하고 `./.claude/agents/spec-sync-agent.md`를 추가한다. `.codex/agents/README.md`의 agent 목록에서 구 2개를 제거하고 `spec-sync-agent`를 추가한다.

**Acceptance Criteria**:
- [ ] `marketplace.json` `skills` 배열에 `./.claude/skills/spec-sync`가 있고 구 2개 entry가 없다.
- [ ] `marketplace.json` `agents` 배열에 `./.claude/agents/spec-sync-agent.md`가 있고 구 2개 entry가 없다.
- [ ] `.codex/agents/README.md`에 `spec-sync-agent`가 있고 `spec-update-todo-agent`/`spec-update-done-agent`가 없다.

**Target Files**:
- [M] `.claude-plugin/marketplace.json` -- skills+agents 배열 갱신
- [M] `.codex/agents/README.md` -- agent 목록 갱신

**Technical Notes**: Covers C6, I3; validated by V5. 등록 누락 사고 이력(simplicity-review-agent가 marketplace.json agents 배열에 빠졌던 사례) 때문에 marketplace.json `agents` 배열 갱신을 명시 AC로 둔다. 삭제(T4)와 mutex: 등록 목록에 구 agent가 남은 채 파일만 삭제되면 dangling이므로 T4 완료 후 처리.
**Dependencies**: T1, T4

### Task T6: autopilot 계약/참조 + AGENTS.md를 단일 spec-sync로 갱신
**Priority**: P1
**Type**: Refactor

**Description**: sdd-autopilot의 orchestrator 계약·참조·예시·SKILL과 AGENTS.md §3, 그리고 다른 producer/reviewer agent 본문·harness template의 downstream skill-name 참조에서 `spec-update-todo`/`spec-update-done` 언급을 단일 `spec-sync`(agent: `spec-sync-agent`)로 갱신한다. 두 단계로 호출되던 흐름(구현 전 todo, 구현 후 done)은 단일 스킬이 evidence로 적응하므로, orchestrator가 동일 `spec-sync`를 호출 시점에 따라 두 번 호출할 수 있음을 명시한다(구현 전 planned 반영 시 1회, 구현 완료 후 sync 시 1회 — 같은 진입점, evidence 차이로 동작 적응). 허용 subagent_type/agent_type 목록에서 구 2개를 `spec-sync-agent`로 교체한다.

추가로 다음 downstream skill-name 참조도 갱신한다(census로 확정한 dangling 표면, 모두 단순 명칭 rename이며 input 마커 토큰 없음): (a) producer/reviewer agent 4쌍 — `spec-review-agent`(claude/codex), `implementation-agent`(claude/codex), `implementation-plan-agent`(claude/codex), `implementation-review-agent`(claude/codex)의 "후속 spec sync 스킬" 안내·Integration 목록; (b) harness 정본 template 4부(`spec-create`/`spec-upgrade` × claude/codex의 `references/agents-harness-template.md`)의 `## 3. SDD 워크플로우` 단계 라벨 `(spec sync todo)`/`spec sync done` → 단일 `spec-sync` 단계. harness template 4부는 byte-identical 미러이므로 4부가 동일 결과가 되도록 일괄 적용한다.

**Acceptance Criteria**:
- [ ] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`의 허용 agent 목록·spec sync ordering·acceptance 섹션에 `spec-update-todo-agent`/`spec-update-done-agent`가 없고 `spec-sync-agent`가 있다.
- [ ] `sdd-reasoning-reference.md`·`sample-orchestrator.md`·`sdd-autopilot/SKILL.md`(AC7·Hard Rules 포함)의 구 2개 언급이 `spec-sync`/`spec-sync-agent`로 갱신된다.
- [ ] 동일 `spec-sync`가 구현 전/후 시점에 따라 두 번 호출될 수 있다는 설명이 orchestrator 참조 중 한 곳에 명시된다.
- [ ] `.codex/skills/sdd-autopilot/` 대응 미러 파일들이 동일하게 갱신된다.
- [ ] `validate_orchestrator.py`(claude+codex)의 `ALLOWED_BASE_AGENTS` set에 `spec-sync-agent`가 **추가**되고 `spec-update-todo-agent`·`spec-update-done-agent`가 **제거**된다(구 이름 삭제만이 아니라 새 이름 등록까지 양방향 — 미등록 시 orchestrator step이 validator에서 reject됨).
- [ ] `AGENTS.md` §3 단계 순서에서 `(spec sync todo)`/`spec sync done`이 단일 `spec-sync`로 표기된다.
- [ ] `.claude/agents/feature-draft-agent.md`·`.codex/agents/feature-draft-agent.toml`의 downstream skill 참조(Integration의 `spec-update-todo`/`spec-update-done` 명칭)가 `spec-sync`로 갱신되되, input 마커 토큰 `spec-update-todo-input-start`/`spec-update-todo-input-end`는 글자 그대로 보존된다(V6 역검증으로 마커 1건 이상 확인).
- [ ] producer/reviewer agent 4쌍(`spec-review-agent`·`implementation-agent`·`implementation-plan-agent`·`implementation-review-agent`의 claude `.md` + codex `.toml`)에 `spec-update-todo`/`spec-update-done` 참조가 없고 후속 spec sync 안내·Integration 항목이 `spec-sync`를 가리킨다.
- [ ] harness 정본 template 4부(`.claude/skills/spec-create/references/agents-harness-template.md`·`.claude/skills/spec-upgrade/references/agents-harness-template.md`·`.codex/skills/spec-create/references/agents-harness-template.md`·`.codex/skills/spec-upgrade/references/agents-harness-template.md`)의 `## 3. SDD 워크플로우` 단계 라벨에서 `spec sync todo`/`spec sync done`이 단일 `spec-sync`로 갱신되고, 4부가 byte-identical을 유지한다.

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.claude/skills/sdd-autopilot/SKILL.md`
- [M] `.claude/skills/sdd-autopilot/scripts/validate_orchestrator.py`
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.codex/skills/sdd-autopilot/SKILL.md`
- [M] `.codex/skills/sdd-autopilot/scripts/validate_orchestrator.py`
- [M] `AGENTS.md`
- [M] `.claude/agents/feature-draft-agent.md` -- Integration·Process의 downstream skill 참조(`spec-update-todo`/`spec-update-done`) 명칭만 `spec-sync`로; **input 마커 토큰 `spec-update-todo-input-start`/`-end`는 보존**
- [M] `.codex/agents/feature-draft-agent.toml` -- 위 대응(`Part 1: spec-update-todo 호환 spec delta` 등 skill 명칭 참조 갱신, input 마커 토큰 보존)
- [M] `.claude/agents/spec-review-agent.md` -- downstream spec sync 안내(L181-182)·Integration(L240-241) 명칭 rename (마커 없음)
- [M] `.codex/agents/spec-review-agent.toml` -- 위 대응
- [M] `.claude/agents/implementation-agent.md` -- spec drift 안내(L39) "호출자가 `spec-update-todo`로 처리" → `spec-sync`
- [M] `.codex/agents/implementation-agent.toml` -- 위 대응
- [M] `.claude/agents/implementation-plan-agent.md` -- spec gap 후속 제안(L43)·Integration(L385) 명칭 rename
- [M] `.codex/agents/implementation-plan-agent.toml` -- 위 대응(L43, L390)
- [M] `.claude/agents/implementation-review-agent.md` -- 후속 안내(L204) `spec-update-todo`/`spec-update-done` → `spec-sync`
- [M] `.codex/agents/implementation-review-agent.toml` -- 위 대응(L200)
- [M] `.claude/skills/spec-create/references/agents-harness-template.md` -- §3 워크플로우 단계 라벨(L30-31) `spec sync todo`/`spec sync done` → `spec-sync` (정본; 나머지 3부 미러의 source)
- [M] `.claude/skills/spec-upgrade/references/agents-harness-template.md` -- 위 정본의 byte-identical 미러
- [M] `.codex/skills/spec-create/references/agents-harness-template.md` -- 위 정본의 byte-identical 미러
- [M] `.codex/skills/spec-upgrade/references/agents-harness-template.md` -- 위 정본의 byte-identical 미러

**Technical Notes**: Covers C7, I3; validated by V5, V6. 단일 task 목적은 "오케스트레이션·agent·harness 계약의 spec-sync 명칭 정합"이며, 파일이 많지만 모두 동일 rename 의미(downstream skill/단계 명칭 참조 갱신)라 분리하지 않는다. 새 이름 계약(T1·T2·T3)이 확정돼야 참조 대상이 존재하므로 의존. **full-repo census 확정(2026-06-19)**: live 운영 surface(`_sdd/drafts`·`_sdd/discussion`·`_sdd/pipeline`·`_sdd/spec/logs`·`_sdd/spec/prev`·`.sdd-workbench` 제외)에서 `spec-update-todo|spec-update-done|spec sync todo|spec sync done|/spec-update`를 가진 갱신 대상은: autopilot 5쌍(claude+codex), AGENTS.md, marketplace.json, codex README, feature-draft-agent 2개, producer/reviewer agent 4쌍(spec-review/implementation/implementation-plan/implementation-review), harness template 4부, 그리고 비-autopilot 스킬(T7 소유: implementation·pr-review·guide-create·docs·usage-guide·components.md). 위 모두가 T6 또는 T7 Target Files에 편입됨 — Target Files에 없으면서 갱신 대상인 live surface는 없음. **codex census 확정**: `rg -l "spec-update-todo|spec-update-done" .codex/skills/sdd-autopilot` = 5개 파일(orchestrator-contract.md, SKILL.md, validate_orchestrator.py, sdd-reasoning-reference.md, sample-orchestrator.md)로 모두 위 Target Files에 포함. `execution-profile-policy.md`에는 구 agent 키가 없어 추가 surface 없음. feature-draft-agent 두 파일은 input 마커와 skill 명칭 참조가 같은 파일에 공존하므로 마커 라인은 그대로 두고 skill 명칭 참조만 surgical 갱신한다(V6 역검증이 마커 보존을 확인). harness template 4부는 byte-identical 미러이므로 동일 결과를 4부에 적용한다.
**Dependencies**: T1, T2, T3

### Task T7: docs + 비-autopilot 스킬 참조를 단일 spec-sync로 갱신
**Priority**: P1
**Type**: Refactor

**Description**: docs(en+ko)와 비-autopilot 스킬(implementation, pr-review, guide-create)의 `spec-update-todo`/`spec-update-done` 참조를 단일 `spec-sync`로 갱신한다. docs의 파이프라인 표·다이어그램·slash command 표·codex 디렉토리 트리(`spec-update-todo.toml`/`spec-update-done.toml` 항목)를 갱신한다. implementation SKILL의 spec drift 안내 문구(`spec-update-todo` → `spec-sync`)와 progress/report 소비 호환 언급(`spec-update-done` → `spec-sync`, 산출물 형식은 보존)을 갱신한다. pr-review의 `/spec-update-todo` 안내(SKILL.md claude+codex, 예시 `examples/sample-review.md` claude+codex 양쪽), guide-create의 `spec-update-todo` 선택지 문구를 갱신한다. 추가로 `_sdd/spec/usage-guide.md`(slash command 카탈로그 + Scenario 2 산문 bare 참조)와 `_sdd/spec/components.md`(Strategic Code Map dangling 행)의 `spec-update-todo`/`spec-update-done` 참조를 단일 `spec-sync`로 갱신해 T4 hard-delete 후 dangling 참조·dead-link가 남지 않게 한다.

**Acceptance Criteria**:
- [ ] `docs/SDD_WORKFLOW.md`·`docs/en/SDD_WORKFLOW.md`·`docs/AUTOPILOT_GUIDE.md`·`docs/en/AUTOPILOT_GUIDE.md`에 `spec-update-todo`/`spec-update-done`가 없고 `spec-sync`로 갱신된다(파이프라인 표·다이어그램·slash command 표·codex 트리 포함).
- [ ] `.claude/skills/implementation/SKILL.md`·`.codex/skills/implementation/SKILL.md`의 spec drift 안내가 `spec-sync`를 가리키고, progress/report 소비 호환 언급의 명칭이 `spec-sync`로 갱신된다(canonical 산출물 형식 자체는 변경 없음).
- [ ] `.claude/skills/pr-review/SKILL.md`·`.codex/skills/pr-review/SKILL.md`·`.claude/skills/pr-review/examples/sample-review.md`·`.codex/skills/pr-review/examples/sample-review.md`의 `/spec-update-todo`(`$spec-update-todo`) 안내가 `/spec-sync`(`$spec-sync`)로 갱신된다(예시 파일은 claude+codex 양쪽 0건).
- [ ] `.claude/skills/guide-create/references/tool-and-gates.md`·`.codex/skills/guide-create/references/tool-and-gates.md`의 `spec-update-todo` 선택지가 `spec-sync`로 갱신된다.
- [ ] `_sdd/spec/usage-guide.md` 파일 전체에 `spec-update-todo`/`spec-update-done`(slash `/`·`$` 형태와 bare 형태 모두, Scenario 2 산문 L62 포함)가 없고 `spec-sync`/`/spec-sync`로 갱신된다(라인 고정 아닌 파일 단위 0건).
- [ ] `_sdd/spec/components.md`의 Strategic Code Map에서 구 `spec-update-todo`/`spec-update-done` 행(L16·L17)이 `spec-sync` 단일 component entry로, `Spec sync map promotion` 행(L80) Source가 `spec-sync-agent.md`/`.toml`로 갱신돼 T4 삭제 대상 파일을 가리키는 dead-link가 0건이 된다.

**Target Files**:
- [M] `docs/SDD_WORKFLOW.md`
- [M] `docs/en/SDD_WORKFLOW.md`
- [M] `docs/AUTOPILOT_GUIDE.md`
- [M] `docs/en/AUTOPILOT_GUIDE.md`
- [M] `.claude/skills/implementation/SKILL.md`
- [M] `.codex/skills/implementation/SKILL.md`
- [M] `.claude/skills/pr-review/SKILL.md`
- [M] `.codex/skills/pr-review/SKILL.md`
- [M] `.claude/skills/pr-review/examples/sample-review.md` -- claude pr-review 예시의 `/spec-update-todo` 안내(L5·L325·L413)
- [M] `.codex/skills/pr-review/examples/sample-review.md` -- codex pr-review 예시의 `$spec-update-todo` 안내
- [M] `.claude/skills/guide-create/references/tool-and-gates.md`
- [M] `.codex/skills/guide-create/references/tool-and-gates.md`
- [M] `_sdd/spec/usage-guide.md` -- slash command 카탈로그(L37,L42)와 Scenario 2 산문(L62 bare 참조)의 `spec-update-todo`/`spec-update-done` → `spec-sync` (파일 단위 0건)
- [M] `_sdd/spec/components.md` -- Strategic Code Map dangling 행(L16·L17 구 component 2개 → `spec-sync` 단일 entry, L80 Source → `spec-sync-agent`) dead-link 정리

**Technical Notes**: Covers C7; validated by V6. T6와 파일 disjoint이며 병렬 가능. 새 이름 계약(T1·T2·T3) 확정에 의존. `usage-guide.md`·`components.md`는 `_sdd/spec/` 아래에 있으나 contract/invariant 본문(normative truth는 main.md)이 아니라 각각 사용자 대상 slash command 운영 카탈로그·reference-only supporting surface(components.md L3-4가 "여기에는 navigation note만"이라 명시)다. T4 hard-delete로 dangling이 되는 명칭·dead-link 정리를 이 task가 직접 소유한다(spec-sync agent의 evidence 분류 대상이 아닌 단순 명칭 rename/stale source pointer 정리). 안전 불변식("`_sdd/spec/`는 spec-sync agent만 수정")은 normative spec 본문(main.md 등 decision-bearing truth) 수정을 가리키며, 두 파일의 dead-link 정리는 본문 의미 변경이 아니므로 충돌하지 않는다.
**Dependencies**: T1, T2, T3

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, C2 | 2등급 (정성 rubric 판정형) | 리뷰어가 `spec-sync-agent.md`/`.toml` 본문을 읽어 (a) status 4분류와 routing, (b) 구현 전 evidence 부재→PLANNED degrade / 구현 후 IMPLEMENTED 승격 적응 서술, (c) 도구 superset(Read·Write·Edit·Glob·Grep·Bash)이 모두 존재하는지 확인한다. 셋 중 하나라도 누락 사례를 지목하면 미충족, 지목 못 하면 충족. 증거: 인용한 본문 라인. |
| V2 | C3 | 2등급 (정성 rubric 판정형) | 리뷰어가 agent 본문 산출물 규정에서 `_processed_*` 마킹과 단일 `Spec Sync Report`(status 컬럼) 두 산출물이 모두 명시됐는지 확인한다. 하나라도 빠진 곳을 지목하면 미충족. 증거: 인용한 산출물 규정 라인. |
| V3 | C4 | 1등급 (정량 측정형) | `rg -l "spec-sync-agent" .claude/skills/spec-sync .codex/skills/spec-sync`로 양 진영 wrapper 2개가 모두 dispatch 대상을 지정함을 확인(=2 파일). `jq '.name' .claude/skills/spec-sync/skill.json .codex/skills/spec-sync/skill.json`가 모두 `"spec-sync"`. claude/codex wrapper description의 트리거 문구 집합이 동일(diff로 문구 집합 비교). 증거: 명령 출력. |
| V4 | C5 | 1등급 (정량 측정형) | `ls .claude/skills/spec-update-todo .claude/skills/spec-update-done .codex/skills/spec-update-todo .codex/skills/spec-update-done .claude/agents/spec-update-*-agent.md .codex/agents/spec-update-*-agent.toml` 모두 not found. 증거: ls 종료코드·출력. |
| V5 | C6, I3 | 1등급 (정량 측정형) | **(구 이름 부재)** `rg "spec-update-todo-agent\|spec-update-done-agent" .claude-plugin/marketplace.json .codex/agents/README.md .claude/skills/sdd-autopilot .codex/skills/sdd-autopilot` 결과 0건. **(새 이름 포함 — 양방향)** `jq '.plugins[0].agents' .claude-plugin/marketplace.json`에 `spec-sync-agent.md` 포함·구 2개 미포함; `jq '.plugins[0].skills'`에 `spec-sync` 포함·구 2개 미포함; `rg "spec-sync-agent" .codex/agents/README.md` 1건 이상; **`rg "spec-sync-agent" .claude/skills/sdd-autopilot/scripts/validate_orchestrator.py .codex/skills/sdd-autopilot/scripts/validate_orchestrator.py` 양쪽 각 1건 이상**(둘 다의 `ALLOWED_BASE_AGENTS`에 새 agent가 등록됐고 구 2개는 부재 — 새 이름 미등록 시 생성될 orchestrator의 `spec-sync-agent` step이 validator에서 reject되는 회귀를 잡는다). 어느 한 검사라도 실패하면 미충족. 증거: 명령 출력. |
| V6 | C7 | 1등급 (정량 측정형) | **구 *스킬 진입점/agent 이름/파이프라인 단계 라벨* 참조만** 0건 대상으로 하고, feature-draft Part 1 input 마커 `spec-update-todo-input-*`는 보존 대상이므로 명시 제외한다. 검증식(PCRE2 negative-lookahead로 `-input` 후속 토큰만 제외해 bare 참조까지 포착, scope는 census로 확정한 live 운영 surface 전체): `rg -P 'spec-update-(todo\|done)(?!-input)\|spec sync todo\|spec sync done' docs .claude/skills .codex/skills .claude/agents/feature-draft-agent.md .codex/agents/feature-draft-agent.toml .claude/agents/spec-review-agent.md .codex/agents/spec-review-agent.toml .claude/agents/implementation-agent.md .codex/agents/implementation-agent.toml .claude/agents/implementation-plan-agent.md .codex/agents/implementation-plan-agent.toml .claude/agents/implementation-review-agent.md .codex/agents/implementation-review-agent.toml _sdd/spec/usage-guide.md _sdd/spec/components.md AGENTS.md` 결과 0건. (scope 안에 harness template 4부가 `.claude/skills`·`.codex/skills` 경로로 포함되므로 그 §3 단계 라벨 `spec sync todo`/`done`도 0건 대상에 자동 편입된다.) **역검증(마커 보존)**: `rg 'spec-update-todo-input' .claude/agents/feature-draft-agent.md .codex/agents/feature-draft-agent.toml .claude/skills/sdd-autopilot/references/orchestrator-contract.md .codex/skills/sdd-autopilot/references/orchestrator-contract.md .claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md .codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` 결과 1건 이상. 전자에 잔존 매치가 있거나 후자가 0건이면 미충족. 증거: 두 rg 출력. Notes: `spec-update-todo`/`done`를 bare로 grep하면 보존 대상 input 마커(`spec-update-todo-input-*`)가 함께 잡혀 0건이 영구 불가능하므로 `(?!-input)` lookahead로 마커 토큰만 빼고, Integration의 bare 참조(`` `spec-update-todo` ``)·slash command(`/spec-update-todo`)·디렉토리 경로(`skills/spec-update-done`)·파이프라인 단계 라벨(`spec sync todo`/`done`)은 모두 0건 대상에 포함된다. **rg 스코프 ↔ Target Files 커버리지 규율**: V6 rg scope의 모든 매치 경로는 Target Files(T4 삭제분 또는 T5/T6/T7 갱신분)에 존재해야 한다(누락 0). 그리고 census는 claude/codex 짝을 **대칭으로** 수행한다 — 한 진영(`.claude/skills/...`) 파일이 잡히면 codex 짝(`.codex/skills/...` 동일 상대경로)도 함께 census해 양쪽 모두 Target Files에 편입한다(한쪽만 편입 금지). 이 0건 scope의 모든 경로는 T6/T7 Target Files에 `[M]`로 존재하며, pr-review `examples/sample-review.md`는 claude·codex 양쪽이 T7 Target Files에 편입돼 있다(이번 census가 확정 — scope엔 들어오나 Target Files엔 없는 surface 0개, claude/codex 비대칭 0건). |
| V7 | I1, I2 | 2등급 (정성 rubric 판정형) | 리뷰어가 다음 3개를 인용으로 확인한다: (a) agent **Hard Rule** 섹션에 "evidence 없으면 승격 금지, 기본값 PLANNED/보류"가 별도 항목으로 존재, (b) Hard Rule에 "verified/planned 무표식 혼합 금지"가 별도 항목으로 존재, (c) agent **Process(분류 단계)** 본문에 "evidence 없으면 PLANNED 기본 routing" 동작 서술과 "구현 전 호출 = 전 항목 PLANNED degrade / 구현 후 = IMPLEMENTED 승격 + 잔여 PLANNED 분리" 적응 예시 서술이 존재. 셋 중 하나라도 누락·식별 불가하면 미충족. 증거: 인용한 Hard Rule 항목 번호·문구 + Process 단계 라인. Notes: 안전 불변식의 *런타임 동작* 정량 테스트는 이 repo에 테스트 프레임워크가 없어 out-of-scope이며, 텍스트 증거(규칙 명시 + 동작 routing 서술 존재)로 한정한다. |

## Parallel Execution Summary

- **Phase 1**: T1 단독(선행 단일 소스).
- **Phase 2**: T2·T3는 Target Files disjoint이나 둘 다 T1 의존 → T1 완료 후 T2·T3 병렬 가능. T4는 T1·T2·T3 의존(트리거 흡수·본문 참조 후 삭제). T5는 T1·T4 의존(삭제와 등록 mutex). 따라서 Phase 2 내부 순서: (T2 ∥ T3) → T4 → T5.
- **Phase 3**: T6·T7은 Target Files disjoint, 의미적 충돌 없음(autopilot 트리 vs docs+비-autopilot 스킬), 둘 다 T1·T2·T3 의존 → T2·T3 완료 후 T6 ∥ T7 병렬 가능.
- mutex 인코딩: T4(삭제)↔T5(등록)는 방향 없는 상호배제지만 "삭제 후 등록 정리" 순서로 T5→depends-on→T4로 흡수. T1은 모든 이름 계약의 생산자이므로 전 task의 공통 선행.

# Risks/Mitigations and Open Questions

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| marketplace.json `agents` 배열 갱신 누락 (simplicity-review-agent 사고 재현) | `spec-sync-agent`가 plugin에 등록되지 않아 런타임 dispatch silent fail | T5 AC에 marketplace.json agents 배열 명시 검증 + V5에서 `jq`로 등록 확인 |
| 구 트리 삭제(T4)가 등록(T5)보다 먼저 완료돼 dangling 참조 잔존 | orchestrator 허용목록·marketplace에 없는 파일을 가리킴 | T5→T4 의존으로 순서 강제 + V5 rg 0건 검증 |
| 트리거 문구 흡수 누락 — 구 done 트리거("sync spec with implementation")가 통합 description에 빠짐 | "구현 완료 sync" 요청이 spec-sync로 라우팅 안 됨 | T2/T3 AC에서 todo+done 트리거 합집합 포함 명시 + V3 description 문구 집합 비교 |
| evidence-driven 분류가 구현 전 호출에서 과승격 (planned를 IMPLEMENTED로) | 미구현을 완료 사실로 spec에 기록 → 안전 불변식 위반 | I1을 agent Hard Rule로 명시(기본값 PLANNED/보류) + V7 리뷰 판정 |
| 단일 스킬화로 orchestrator가 "언제 호출하나" 모호 (구현 전 1회 vs 후 1회) | autopilot이 spec-sync를 적절 시점에 호출 못 함 | T6에서 동일 진입점 2회 호출 가능(evidence로 적응)을 orchestrator 참조에 명시 |
| codex/claude 본문 mirror 비동기 | 한 진영만 갱신돼 계약 drift | T1에서 claude 단일 소스 확정 후 codex mirror, Source Pointer로 단일 소스 명문화 |

## Open Questions

### Q1. 통합 후에도 orchestrator는 spec-sync를 구현 전·후 2회 호출하는가, 1회로 줄이는가
- **Decision taken**: 동일 `spec-sync` 진입점을 호출 시점에 따라 최대 2회 호출 유지(구현 전 planned 반영 1회 — 조건부, 구현 완료 후 sync 1회). 단일 스킬이 evidence로 동작을 적응하므로 진입점만 통합하고 호출 시점/횟수는 기존 파이프라인 구조를 보존한다.
- **Alternatives considered**: (a) 구현 후 1회로 통합 — 구현 전 planned global alignment(대규모 변경에서 조건부 필요)를 잃어 기존 todo의 사전 반영 가치가 사라짐. (b) evidence 자동 감지로 호출 횟수까지 orchestrator가 추론 — 추가 추론 부담·오판 위험, 현재 조건부 규칙으로 충분.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

### Q2. 통합 스킬의 Mode 필드(codex framed payload)를 단일값으로 둘지 두 모드로 유지할지
- **Decision taken**: 단일 통합 Mode(`spec-sync`)로 둔다. status 분류가 evidence로 적응하므로 `planned-spec-update`/`implemented-spec-sync` 두 모드를 명시할 필요가 없다.
- **Alternatives considered**: 두 모드 유지로 호출자가 의도(전/후)를 힌트로 전달 — agent가 evidence로 이미 판정하므로 모드 힌트는 잉여이고, 잘못된 모드 힌트가 evidence 판정과 충돌할 위험.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

### Q3. `spec-sync` skill `description`이 너무 길어 trigger 정밀도가 떨어질 위험
- **Decision taken**: 두 구 트리거 문구의 합집합을 그대로 통합 description에 넣는다(흡수 누락 방지 우선).
- **Alternatives considered**: 대표 문구만 추려 짧게 — 흡수 누락 시 일부 호출 표현이 라우팅 안 되는 회귀 위험이 더 크다고 판단.
- **Confidence**: MEDIUM
- **User confirmation needed**: No
