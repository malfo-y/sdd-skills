# Feature Draft: SDD 체인 품질 게이트를 producer 스킬 소유로 정리

> 규모 판정: 적격 — 변경 요소 3개(implementation 마감 계약 / autopilot 체인 구성 / 사용자 문서)와 task가 1:1 대응하고, 수정 표면이 스킬 미러 2쌍 + docs 2파일이라 coverage 눈검산이 가능하다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

SDD 체인의 두 품질 게이트(`plan-review`·`implementation-review`)는 지금 **소유자가 어긋나 있다**. `feature-draft`는 `plan-review`를 강제 게이트로 소유하는데(`품질 게이트` 규칙), `implementation`은 `implementation-review`를 "선택 — 강제 아님"으로만 권유한다. 동시에 `sdd-autopilot` Step 2는 두 게이트를 **자기가 다시 호출**해, producer가 이미 소유한 게이트와 중복된다. 반면 `docs/SDD_WORKFLOW.md:9-11`은 이미 "feature draft (plan-review 게이트 + fix 1회) / implementation (implementation-review 게이트 + fix 1회)"로 **producer 소유 모델을 문서화**하고 있다 — 즉 이 변경은 새 설계가 아니라 스킬 본문·autopilot이 문서 모델을 따라잡는 drift 정리다.

새로 고정되는 약속:

- **게이트 소유권 불변식**: SDD 체인의 품질 게이트는 그 산출물을 만든 producer 스킬이 소유한다 — `feature-draft`가 `plan-review`를, `implementation`이 `implementation-review`를 각각 단일 패스 1회 + fix 1회로 수행한다. 호출자(autopilot·사용자)는 게이트를 별도로 호출하지 않는다.
- **`implementation` 마감 반환 계약**: `implementation`의 마감 산출물은 게이트 수행 사실·finding·fix 내역·fix 후 회귀 결과를 포함한다. 이 계약은 `implementation`에만 적용한다 — `feature-draft`는 마감 노출을 Open Questions로 제한하는 출력 다이어트가 의도된 설계이고, plan gate finding의 잔여 이슈 보고 의무는 이미 spec Guardrail("review-only로 닫지 않고 fix 또는 명시적 잔여 이슈 보고로 마무리")과 `feature-draft` 품질 게이트 규칙이 소유한다.
- **`implementation` 마감 계약**: 마감은 회귀 1회 → AC→증거 테이블 → `implementation-review` 게이트 1회 + Critical/High/Medium fix 1회(fix가 있었으면 회귀 재실행) → 마감 요약 순서다. "선택" 해치는 없다.
- **`sdd-autopilot` 체인 구성**: Step 2는 `feature-draft → implementation → (persistent 변경 시) spec-sync` 3스킬이다. 게이트는 앞 두 스킬 내부에서 돈다.
- **하네스 §3은 체인 리터럴을 유지하되 호출 주체를 정정한다**: 체인 리터럴 `discussion → feature-draft → plan-review → implementation → implementation-review → spec-sync`는 SDD **단계** 순서라 그대로 두지만, 바로 뒤 문장이 "해당 단계 진입 시 그 스킬을 **호출**한다"로 호출 주체까지 명령하므로 게이트 두 단계는 예외임을 1줄로 명시한다 — `plan-review`·`implementation-review` 단계는 각각 `feature-draft`·`implementation`이 내부 게이트로 수행하며 별도 호출하지 않는다. AGENTS.md §3 + spec-create·spec-upgrade 하네스 템플릿 4미러 = 5곳에 동일 적용(전파 표면이라 누락 시 소비 repo에 이중 호출이 남는다).

## Scope

- **In**: `implementation` 스킬 미러 2벌 + skill.json 2개(마감 §4 강제 게이트화, Integration 줄, version), `sdd-autopilot` 미러 2벌 + skill.json 2개(Goal·Workflow Position·Step 2·AC2·규칙, version), `plan-review-agent` 미러 2벌(Integration의 호출 주체 1줄), `docs/AUTOPILOT_GUIDE.md` ko/en, 하네스 §3 5곳(`AGENTS.md` + spec-create·spec-upgrade 템플릿 4미러 — 게이트 예외 1줄), 그리고 위 Change Summary가 요구하는 `_sdd/spec/` 동기화 — main.md 리뷰 bullet·autopilot bullet·분할 canonical 목록(`:82`의 `plan-review 규모 판정 검사`)·plan 게이트를 optional로 적은 서술(`:91`·`:124`), components.md `sdd-autopilot`·`implementation` 행, usage-guide.md Scenario 2/2b. spec 표면은 `spec-sync`가 이 마커를 소비해 반영한다.
- **Out**: `feature-draft` 본문(이미 게이트를 강제 소유하고, 반환 계약은 위 bullet에서 `implementation` 한정으로 확정), reviewer 스킬·agent의 **review-only 계약 서술**(경량 반환·"호출자 소관"·rubric은 호출 주체가 바뀌어도 그대로 참 — 단 호출 주체를 명시한 Integration 줄은 In), 하네스 체인 리터럴 자체(단계 이름 순서는 무변경 — Task 4 AC2가 검증), `docs/en/SDD_WORKFLOW.md`(ko 짝과 어긋난 선행 drift — 별도 이슈), `README.md`(모델 override 예시는 직접 호출 경로라 유효), `docs/SDD_WORKFLOW.md`(이미 producer 소유 모델), `implementation-review` skill.json version 드리프트(별도 이슈 — Open Questions).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: `implementation` 마감을 강제 게이트 계약으로 전환

"선택 — 강제 아님" 권유를 `feature-draft`와 대칭인 강제 품질 게이트로 바꾸고, 게이트 결과를 마감 산출물에 싣는다 — autopilot이 게이트를 직접 돌지 않게 되므로 finding/fix 내역의 유일 소스가 이 반환이 된다.

**Contracts**: `implementation` 마감 순서는 (1) 회귀 1회 → (2) AC→증거 테이블 → (3) `implementation-review` 스킬 1회(단일 패스) + Critical/High/Medium finding fix 1회 + fix가 있었으면 회귀 재실행 → (4) 마감 요약(계약 오류 선언·대상 파일 밖 수정 + 게이트 finding/fix 내역)이다. Low finding은 advisory로 보고에만 남긴다. review loop는 돌지 않는다.

**Acceptance Criteria**:
- [ ] AC1: 두 미러 SKILL.md에서 `선택 — 강제 아님` 리터럴이 0건이고, 마감 절에 `**품질 게이트**` 로 시작하는 항목이 각 1건 존재한다.
- [ ] AC2: 마감 게이트 항목이 계약 4요소를 각각 1회 이상 명시한다 — grep으로 `implementation-review`(호출), `fix 1회`, `회귀`(fix 후 재실행), `Low`(advisory) 4개 문자열이 그 항목 범위 안에서 확인된다.
- [ ] AC3: 마감 요약 항목의 서술에 게이트 `finding`과 `fix` 내역 포함이 명시된다(두 리터럴이 요약 항목 안에 존재).
- [ ] AC4: Integration 절의 `implementation-review` 줄에 `선택적` 리터럴이 0건이고 마감 게이트로 서술된다.
- [ ] AC5: version 4필드(`.claude`/`.codex` SKILL.md frontmatter + 각 skill.json)가 모두 `3.0.0`이다.
- [ ] AC6: `diff .claude/skills/implementation/SKILL.md .codex/skills/implementation/SKILL.md`가 무출력이다(변경 전 두 미러가 완전 동일 — codex 적응 delta 없음).

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- 마감 §4 강제 게이트화 + 마감 요약 항목 + Integration 줄 + version
- [M] `.codex/skills/implementation/SKILL.md` -- 동일 반영(현재 claude 미러와 byte-identical)
- [M] `.claude/skills/implementation/skill.json` -- version lockstep
- [M] `.codex/skills/implementation/skill.json` -- version lockstep

---

### Task 2: `sdd-autopilot` Step 2를 3스킬 체인으로 축소

게이트가 producer 소유가 됐으므로 autopilot이 `plan-review`·`implementation-review`를 다시 호출하는 두 단계를 제거하고, autopilot의 역할을 "producer 3스킬 순차 호출 + 반환 종합 보고"로 재서술한다.

**Contracts**: autopilot Step 2 = `feature-draft` → `implementation` → (persistent 변경 시) `spec-sync` → 최종 보고. autopilot은 게이트를 호출하지 않고 fix도 수행하지 않는다 — 게이트 수행·fix·회귀는 producer 스킬 반환에서 수거해 최종 보고에 싣는다.

**Acceptance Criteria**:
- [ ] AC1: 두 미러 Step 2 번호 목록이 4항목(Draft / 구현 / Spec sync / 최종 보고)이고, `plan-review` 스킬을 실행·호출한다는 항목과 `implementation-review` 스킬을 실행·호출한다는 항목이 각각 0건이다.
- [ ] AC2: Workflow Position 다이어그램에서 `plan-review`·`implementation-review` 독립 행이 0건이고, `feature-draft`·`implementation` 행에 내부 게이트 + fix 1회 서술이 붙는다.
- [ ] AC3: Goal 문단의 체인 괄호 서술 `(draft → 게이트 → 구현 → 게이트 → spec sync)`가 producer 소유 표현으로 교체된다(해당 리터럴 0건).
- [ ] AC4: autopilot AC2가 "두 게이트가 각 producer 스킬 내부에서 수행되었고, Critical/High/Medium finding이 fix 1회로 반영되었거나 잔존 finding이 최종 보고에 남았다" 판정으로 재작성된다 — 기존의 `plan-review 단일 패스와 implementation-review(경량 반환)가 각각 수행되었고` 리터럴이 0건이다.
- [ ] AC5: 규칙 절에 `Fix는 게이트당 1회다` 항목이 0건이고, 그 자리에 게이트·fix가 producer 스킬 소유임을 가리키는 항목이 1건 존재한다(`게이트`와 `producer` 또는 두 producer 스킬 이름이 같은 항목에 등장).
- [ ] AC6: version 4필드(`.claude`/`.codex` SKILL.md frontmatter + 각 skill.json)가 모두 `4.0.0`이다.
- [ ] AC7: codex 미러의 Codex 적응 delta가 보존된다 — `spawn_agent`/`wait_agent`/`close_agent`(Hard Rule 4), framed payload 서술(Hard Rule 2), `.codex/skills/<name>/SKILL.md` 본문 로드 서술, bare-name 스킬 호출(`sdd-skills:` prefix 부재)이 변경 후에도 각각 grep으로 확인된다. 3-way merge로 반영하고 claude 미러를 복사하지 않는다.
- [ ] AC8: `plan-review-agent` 미러 2벌의 Integration 줄이 호출 주체를 `feature-draft`로 서술하고, `sdd-autopilot`을 plan gate 호출자로 명시하는 서술이 두 파일에서 0건이다(`.codex` TOML은 3-way merge — claude 미러 복사 금지).

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md` -- Goal·AC2·Workflow Position·Step 2·규칙·version
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- 동일 변경을 codex delta 보존 merge로 반영
- [M] `.claude/skills/sdd-autopilot/skill.json` -- version lockstep
- [M] `.codex/skills/sdd-autopilot/skill.json` -- version lockstep
- [M] `.claude/agents/plan-review-agent.md` -- `:109` Integration 줄의 호출 주체를 autopilot → `feature-draft`
- [M] `.codex/agents/plan-review-agent.toml` -- 동일 1줄(TOML 미러, merge 반영)

---

### Task 3: `AUTOPILOT_GUIDE` ko/en을 새 체인으로 동기화

사용자 문서의 체인 다이어그램·원칙·관련 스킬 목록이 autopilot 본문과 어긋나지 않게 맞춘다.

**Acceptance Criteria**:
- [ ] AC1: ko/en 두 파일의 체인 코드블록에서 `plan-review`·`implementation-review` 독립 화살표 행이 0건이고, `feature-draft`·`implementation` 행에 내부 게이트 서술이 포함된다.
- [ ] AC2: 두 파일의 핵심 원칙에서 게이트 수행 주체가 producer 스킬로 서술된다 — autopilot이 게이트를 돌린다는 서술(ko `plan-review 자동 게이트가`, en `the plan-review gate checks`)이 0건이다.
- [ ] AC3: 두 파일 §7(관련 스킬) 목록에서 `plan-review`·`implementation-review` 항목이 producer 스킬 내부 게이트로 재서술된다.
- [ ] AC4: 두 파일 헤더의 버전이 `2.1.0`, 날짜가 `2026-07-26`이다.
- [ ] AC5: ko/en 체인 코드블록의 행 수가 서로 같다(구조 동형).

**Target Files**:
- [M] `docs/AUTOPILOT_GUIDE.md` -- 체인 블록·원칙·§7·헤더
- [M] `docs/en/AUTOPILOT_GUIDE.md` -- 동일 반영(영문)

---

### Task 4: 게이트 소유권 census 검증 (read-only)

"게이트를 누가 호출하는가" 서술은 스킬·문서·spec에 변형 표기로 흩어져 있어, 전수 grep 없이는 잔존 서술이 재발한다. 무변경이어야 할 표면(하네스 체인 리터럴)도 함께 고정한다.

**Acceptance Criteria**:
- [ ] AC1: census를 두 갈래로 판정한다(대소문자 무시 `grep -rniE`) — **(A)** live 표면(`.claude/`·`.codex/`·`docs/` + root `README.md`·`.claude-plugin/marketplace.json`) 전역에서 게이트 호출자 표기 `plan gate`·`impl gate`·`이 agent를 호출`·`gate로 이 agent` 4종이 0건, **(B)** autopilot 표면 4곳(스킬 미러 2 + 가이드 ko/en)에서 백틱-관용 게이트 스킬 호출 표기 `(plan-review|implementation-review)`?\s*(스킬|skill)`가 0건. producer 스킬이 자기 게이트를 호출하는 서술은 이제 정당하므로 (B)는 autopilot 표면에 한정하고, 이 패턴의 매치력은 변경 전 autopilot 본문(`540f1d5`)에서 2건 이상 검출됨으로 검증한다.
- [ ] AC2: 하네스 §3 5곳(`AGENTS.md`, spec-create·spec-upgrade `agents-harness-template.md`의 claude/codex 미러 4개)이 (a) 체인 리터럴 `discussion → feature-draft → plan-review → implementation → implementation-review → spec-sync`를 그대로 1건씩 보유하고, (b) 게이트 예외 1줄(`feature-draft`·`implementation`이 내부 게이트로 수행하므로 별도 호출하지 않는다)을 각 1건씩 보유한다.
- [ ] AC3: `docs/SDD_WORKFLOW.md:9-11`의 producer 소유 서술이 무변경이고 새 서술과 모순되지 않는다(같은 `git diff --name-only 540f1d5` 출력에 해당 파일이 없다).
- [ ] AC4: version lockstep 8필드가 확인된다 — `implementation` 4필드 `3.0.0`, `sdd-autopilot` 4필드 `4.0.0`.
- [ ] AC5: `git diff --check`가 무출력이다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- `implementation-review` skill.json version 드리프트를 발견했다 — `.claude` `2.1.0` / `.codex` `3.0.0` 인데 두 SKILL.md frontmatter는 모두 `7.0.0`이다. 이번 변경은 그 스킬 본문을 건드리지 않으므로 범위 밖으로 두었다. **사용자 확인 필요**: 별도 이슈로 처리할지, 이번 draft에 task로 끼워 넣을지.
- 사용자가 `/implementation`을 단독 호출해도 게이트가 자동으로 붙는다(의도한 동작 — "선택" 해치를 없애는 게 이번 변경의 목적). 확인 불요.
