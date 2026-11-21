# SDD Skills

> Markdown 기반 skill bundle로 AI 에이전트의 Spec-Driven Development 워크플로우를 Claude Code와 Codex에서 공통 계약으로 실행한다.

**Spec Version**: 6.1.0
**Last Updated**: 2026-11-21
**Status**: Approved
**Canonical Role**: current thin global spec

이 문서는 repo-wide `개념 + 경계 + 결정`만 고정하는 thin global spec이다. 상세 component reference는 [components.md](./components.md), 사용 시나리오와 기대 결과는 [usage-guide.md](./usage-guide.md), 구조 변경 이력은 [decision_log.md](./decision_log.md), 릴리스/문서 변경 이력은 [logs/changelog.md](./logs/changelog.md), 환경과 실행 제약은 [../env.md](../env.md)에서 확인한다.

## 1. 배경 및 high-level concept

### 문제 정의

AI 코딩 에이전트는 강한 생성 능력을 갖고 있지만, 프로젝트의 문제 정의, 설계 경계, 검증 기준이 고정돼 있지 않으면 같은 저장소에서도 매번 다른 추론을 하게 된다. 기존 개발 방법론은 사람 중심 운영을 전제로 하므로, 에이전트가 스펙을 읽고 구현하고 검증하고 다시 스펙을 갱신하는 루프를 직접 실행하기에는 계약이 느슨하다.

### high-level concept

SDD Skills는 이 문제를 `SKILL.md = 실행 가능한 프롬프트`라는 관점으로 푼다.

- global spec은 얇은 기준 문서로 남기고, 변경 실행에는 temporary spec과 implementation artifact를 분리한다
- 사용자 진입점은 skill layer에 유지하고, 재사용 가능한 실행 계약은 스킬 `references/` 문서로 분리해 프롬프트로 주입한다
- 스킬 간 persistent handoff는 숨겨진 메모리가 아니라 `_sdd/` 파일 아티팩트에 남긴다
- 검증은 부가 옵션이 아니라 workflow contract의 일부로 취급한다

### 왜 이 접근을 택하는가

| 접근 | 장점 | 한계 | 판정 |
|------|------|------|------|
| SDD skill bundle | 스펙을 Single Source of Truth로 유지하고, 사람과 AI가 같은 파일 기반 계약을 공유한다 | 스킬/문서 유지 비용이 있다 | 채택 |
| 프롬프트 라이브러리 | 시작이 빠르다 | 스킬 간 연결과 산출물 계약이 약하다 | 비채택 |
| 코드 중심 자동화만 사용 | 익숙한 CI/CD 자산을 활용할 수 있다 | 자연어 기반 계획, spec sync, decision capture가 약하다 | 비채택 |

### 이 repo를 읽는 관점

이 저장소는 Claude Code와 Codex에서 공통으로 사용할 수 있는 SDD workflow bundle이다. 사용자는 `/spec-create`, `/sdd-orchestrator`, `/sdd-autopilot` 같은 명시적 skill entrypoint로 워크플로우를 시작하고, 저장소는 그 과정을 `_sdd/` 산출물과 문서 계약으로 추적 가능하게 만든다.

## 2. Scope / Non-goals / Guardrails

### In Scope

- `.claude/skills/`, `plugins/sdd-skills-codex/skills/`의 사용자 진입점과 workflow contract
- 스킬 `references/`의 재사용 계약 문서 (예: spec 반영 규약 `sdd-orchestrator/references/spec-sync.md`, simplicity 계약 `pr-review/references/simplicity-contract.md`)
- global spec, temporary spec, `_sdd/` artifact layout, decision log, changelog
- README와 `docs/`의 개념/정의/워크플로우/가이드 문서
- Claude plugin 구조(`.claude-plugin/`, 마켓 `sdd-skills`)와 Codex plugin 구조(`.agents/plugins/marketplace.json` + `plugins/sdd-skills-codex/`, 마켓·플러그인 `sdd-skills-codex` — Codex가 `.claude-plugin`을 legacy marketplace로도 읽으므로 이름을 분리) 및 bundle/config 배포 규약

### Non-goals

- Claude Code나 Codex의 호스트 런타임 자체를 대체하지 않는다
- 애플리케이션 런타임이나 서비스 배포 파이프라인을 제공하지 않는다
- exhaustive inventory를 global spec 본문에 유지하지 않는다
- 모든 플랫폼 기능을 완전 동등하게 추상화하지 않는다

### Guardrails

- global spec은 thin decision document로 유지하고, execution detail은 `_sdd/drafts/`, `_sdd/implementation/`, `_sdd/pipeline/` 같은 temporary surface로 분리한다
- test/check 시간 규약은 두 층이다. 하네스 §2(10초 이상 걸리는 테스트는 분리해 기본 실행에서 제외하고 꼭 필요할 때만 실행)가 모든 작업에 적용되고, 구현 단계의 회귀는 이번 변경 관련 표적 check와 fast 회귀이며 무거운 test·전체 suite는 실행하지 않는다. `pr-review` correctness 계약은 여기에 targeted 명령 30초 wall-clock 예산을 더한다 — 30초가 지나면 중단하고, timeout된 같은 명령은 test target·fixture·관련 구현이 바뀌기 전까지 재실행하지 않으며, 느리다고 알려진 test는 repo 또는 사용자가 명시한 checkpoint에서만 실행하고, checkpoint evidence 없는 slow 의존 AC는 임의 실행하지 않고 `UNTESTED`(사유: slow — checkpoint 대기)로 보고한다. 실행 중 무겁게 드러난 테스트는 보고와 함께 **분리·리팩토링을 적극 권고**하고, 본질적으로 느리다는 근거가 있을 때만 checkpoint 한정 실행으로 등록한다(slow 분류를 escape hatch로 쓰지 않는다). 정형 fast/slow lane 스키마는 비도입한다
- 사용자 entrypoint는 skill layer에 두고, 재사용 execution 계약은 스킬 `references/` 문서가 소유한다(dispatch는 런타임 내장 agent type에 계약을 프롬프트로 주입 — custom agent 없음). dispatch된 agent는 sub-agent를 다시 spawn하지 않는다(nesting 1단계 제한)
  - leaf dispatch가 필요한 execution은 `orchestrator(skill) + leaf(계약 주입 범용 agent)` 형태로 둔다(orchestrator skill만 dispatch하고, leaf는 단일 단위/단일 산출물만 처리)
  - **실행 경제 — 해소 수단은 턴 접기(배칭)와 1단계 leaf fan-out이다**: 체감 지연의 지배 성분은 dispatch 왕복이 아니라 턴 수만큼 반복되는 추론과 최종 리포트 생성이다. 중첩 fan-out은 비대상이고, 병렬 분해는 메인 루프의 1단계 leaf dispatch로만 한다 — 기본형은 read-only leaf, 파일을 쓰는 leaf의 병렬은 **쓰기 집합이 서로소로 증명된 작성자 분할**에 한해 허용한다(안전성의 근거는 "안 쓴다"가 아니라 "서로소다"). dispatch되는 review 계약(`pr-review`)은 **서로 의존하지 않는 read-only 호출의 한 메시지 배칭을 지시형으로 요구한다** — 앞 결과를 봐야 대상이 정해지는 호출만 다음 턴, 쓰기·상태 변경 호출은 배칭 비대상, **배칭은 읽을 대상을 늘리지 않는다**. 규칙 문면은 런타임별 tool 이름에 의존하지 않는다
- persistent handoff는 `_sdd/spec/`, `_sdd/drafts/`, `_sdd/implementation/`, `_sdd/pipeline/`, `_sdd/discussion/`의 canonical 경로를 통해 이뤄진다
- 새 temporary artifact는 가능한 한 lowercase canonical 경로를 사용하고, skill contract가 dated slug 패턴을 정의한 output surface는 그 형식을 따라야 한다. reader는 legacy uppercase/fixed-name artifact를 fallback으로 읽을 수 있어야 한다
- 소비 repo에서 커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`·`drafts/`·`work_log/`이고(`drafts/`·`work_log/`는 구현 로그 자산), 나머지 process artifact(`_sdd/{discussion,implementation,pipeline,pr}/`)는 `.gitignore`(`SDD-WORKSPACE` 마커 블록)로 로컬 전용이다. `_sdd/env.md`는 커밋되므로 비밀값(API 키·토큰·비밀번호)을 적지 않는다. 단 이 sdd_skills repo는 스킬 개발 메타 repo라 process artifact를 history 가치로 계속 커밋하는 예외다(소비 repo 정책과 별개)
- 하네스 설치는 문서 산출물(`AGENTS.md`·`CLAUDE.md`·`.gitignore`)과 **공용** 훅 bundle을 동일 조건에 묶어 함께 수행한다 — 훅은 별도 opt-in이 아니다. 공용 실행 경로는 호환성을 위해 `.claude/hooks/`에 유지하며, work log 커밋 게이트·세션 컨텍스트 주입·컨텍스트 소실 후 하네스 재주입·subagent 장기실행 watchdog nudge의 스크립트 4개를 self-host 사본과 `spec-create`/`spec-upgrade`의 Claude/Codex reference surface에 byte-identical하게 유지한다
  - 훅 event/matcher·설정 병합·trust·검증·보고 계약의 authoring canonical은 `.claude/skills/spec-create/references/hook-installation.md`이고, 나머지 세 package의 동명 reference는 exact 배포 mirror다(각 skill은 자기 local 사본만 읽어 독립 배포 유지). 두 runtime 설정(`.claude/settings.json`·`.codex/hooks.json`)은 독립 parse/merge unit으로 함께 등록하되 non-SDD handler를 보존하고, 한쪽이 깨져도 반대 runtime 설치를 계속하며 재실행은 멱등이다. 강제 자산은 파서 부재 시 fail-open + 세션 시작 경고, advisory watchdog은 조용한 fail-open 허용. Codex project hook은 사용자가 `/hooks`에서 검토·신뢰하기 전에 acceptance 완료로 보지 않으며 trust 자동 승인·user-global 설정 수정·bypass는 금지다(상세 계약은 canonical reference가 소유)
- dispatch되는 leaf에는 입력이 대화에서 태어난 맥락을 digest로 forwarding해야 한다(leaf는 파일은 read하지만 대화는 읽지 못한다). 지원하지 않는 동작을 조용히 흉내내지 않는다
- Codex multi-agent dispatch는 Desktop/CLI 같은 surface 이름이 아니라 **활성 tool schema만으로 lifecycle contract를 선택**한다. mailbox schema는 invocation별 parent-tree 고유 `task_name`·`fork_turns: "none"`·target 없는 mailbox wait를 사용하고 완료 agent를 닫지 않는다. target wait와 `close_agent`가 함께 노출된 legacy schema에서만 target/close contract를 유지한다. schema가 불완전하거나 모호하면 mandatory dispatch는 fail closed, optional helper는 inline fallback하며, 없는 lifecycle tool을 검색하거나 두 contract를 섞지 않는다. `agent_type` 같은 role selector는 지원될 때만 추가하는 선택 필드이며, 없으면 framed `message` 계약으로 범용 sub-agent 역할을 부여한다(부재만으로 blocker가 아님). 사용자가 요청한 model·reasoning override가 미지원이면 dispatch를 막는다
- review나 validation이 포함된 workflow는 review-only로 닫지 않고 fix 또는 명시적 잔여 이슈 보고로 마무리한다
  - **계획 리뷰와 구현 리뷰는 `sdd-orchestrator`가 순서 안에서 직접 수행한다**: 같은 세션이 한 번씩 검토하고 찾은 것을 그 자리에서 고친다(독립 리뷰 agent·두 번째 리뷰 없음). 사용자가 리뷰 단계만 지정하면 찾은 것만 보고하고 고치지 않는다. 하네스 §3 체인 리터럴은 SDD **단계** 순서로 유지하되 두 리뷰 단계는 `sdd-orchestrator`가 순서 안에서 직접 수행하므로 별도로 호출하지 않는다고 명시한다 — 전파 표면은 `AGENTS.md` §3 + 하네스 템플릿 4미러 = 5곳(누락 시 소비 repo에 이중 호출이 남는다)
  - simplicity finding은 falsifiable-only gating을 따른다: 동작 변화 없이 더 단순한 동등 형태를 구체적으로 제시할 수 있는 객관적 위반만 Medium 이상(gating)이고, 주관적 취향은 Low(advisory)다. gating을 falsifiable finding으로 한정하는 규칙이 수렴성의 핵심이다. simplicity 렌즈는 `spec-upgrade`의 spec 점검으로 확장하지 않는다(코드 형태 품질이라 spec 문서 품질에 부적합)
  - 직교 2-렌즈 review의 적용 지점·dispatch 구조·전환 근거의 결정 캐노니컬은 §3 비교표 `직교 2-렌즈 review 렌즈` 행이다. 여기는 집행 규칙만 둔다: simplicity 계약의 단일 소스는 `pr-review/references/simplicity-contract.md`(claude/codex 동일본)이고 `pr-review`는 dispatch prompt에 전문을 verbatim 포함한다. `pr-review` correctness 계약의 단일 소스는 `pr-review/references/correctness-contract.md`(claude/codex 동일본)이고 correctness worker가 그 경로를 읽는다. read-only·재호출 금지는 agent 정의가 아니라 계약 문면의 프롬프트 규칙이다. 스킬 호출 자체가 그 스킬의 dispatch(`pr-review` correctness·simplicity)에 대한 **사용자의 명시적 요청**이다 — 런타임 규범("Agent는 사용자가 명시적으로 요청할 때만")과의 충돌은 이 문장이 해소하며 dispatch 생략·직접 수행 대체는 허용되지 않는다(문면은 각 SKILL이 소유, codex 미러의 Runtime 절 첫 문장이 짝). `pr-review`는 메인 루프가 작은 `PR Review Input`(`PR`·`Baseline`·`Changed Files`·`Spec Status`·`Relevant Context` 5필드, 정의 단일 소스는 pr-review SKILL; PR 번호·`headRefOid`·변경 파일 목록·spec 존재 상태(`git ls-tree` 판정)·title/body 요약만 담고 diff·spec 본문·comments·테스트 실행은 메인이 하지 않는다)만 모아 correctness·simplicity worker 둘을 한 메시지로 dispatch한다. 두 worker가 같은 SHA로 `gh pr diff`·코드·spec을 직접 읽고 `headRefOid` 불일치면 BLOCKED(correctness)·Assumptions blocker(simplicity)로 반환하며, 메인은 새 SHA로 1회 다시 dispatch하고 또 불일치면 제한 리포트(NEEDS DISCUSSION, LIMITED)로 닫는다. correctness worker는 CI → `_sdd/env.md` local validation → 사유 병기 `UNTESTED` 순서로 검증한다 — 실행 evidence 없는 test-dependent `UNTESTED`는 자동 `APPROVE`가 아니라 `NEEDS DISCUSSION`으로 흐른다(non-test-dependent·명시적 N/A 제외). verdict는 메인 루프가 두 worker 반환으로 합성해 통합 리포트(`_sdd/pr/..._pr_review_...`) 1파일만 write하고(단일 작성자 불변식 — 두 worker는 리포트를 쓰지 않는다), 리포트는 통계 표 없이 행동 대상 finding을 블록 전문으로 싣는다(Pre-merge=correctness Crit/High + simplicity gating Medium+ · non-blocking=correctness Medium · 주관 Low=위치 포함 한 문장). 인간 리뷰 보조이므로 합집합 자동 exit는 없다. 표적 disjoint(correctness=정합·AC·보안·테스트+정확성-중복 ∥ simplicity=동작-불변 형태+형태-중복)와 Medium=gating/Low=advisory 분류는 falsifiable-only gating 규칙을 재사용한다. 리뷰 깊이는 파일 수보다 변경 위험·관련 AC로 정하고, 검사 결과는 실행 범위와 PASS/FAIL/UNTESTED로 보고한다
  - 양 번들은 skills-only이고 custom agent를 번들하지 않는다(Codex 플러그인/Agent Plugins 1.0 표준이 custom agent를 번들하지 못하는 배포 제약). `pr-review`의 두 reviewer는 런타임 내장 범용 agent가 계약을 읽거나 주입받아 맡는 역할이며, 경계(사용자 질문·git 쓰기·파일 쓰기·하위 agent 금지)의 강제는 tools 제한이 아니라 계약 문면이다. reviewer는 파일을 쓰지 않는다(리포트 파일 작성은 호출자 소관)
    - reviewer 반환에는 **실제 소비자가 있는 항목만** 둔다 — 같은 반환의 다른 항목에서 도출되는 요약 섹션은 두지 않고, 유지/삭제는 소비 실측으로 판정한다
    - 판정 표를 가진 reviewer 반환은 **문제 있는 항목만 개별 행으로 내고 나머지는 `PASS: <이름 나열>` 한 줄로 접는다**(현재 대상: simplicity 계약 4 차원). 점검·스캔 의무는 그대로이고 출력 의무만 완화된다 — 완전성 불변식(전 항목이 개별 행 또는 PASS 접기 중 정확히 하나에 귀속)은 계약 문서의 **AC 절 한 곳**이 소유하고 반환 형식 절에는 재서술하지 않는다
    - reviewer 반환에는 **finding이 아닌 확인 결과를 열거하지 않는다** — 대조 결과는 판정에 기여하지 않고 `Findings`(+ `simplicity-review`의 `차원 판정` 표, PASS 접기 포함)가 전부다. 반환은 명시된 항목이 전부이며 규칙은 **무조건**이다. 줄이는 것은 **출력이지 대조·스캔 범위가 아니다**(점검 의무는 그대로 — 근거: 리뷰 벽시계의 지배 성분은 리포트 작성량). 적용 대상은 simplicity 계약의 반환 절이고, 소유자는 반환 형식 절 1문장 + 준수를 흡수한 자체 검증 AC다. correctness 계열은 Verification ledger가 반환 계약이라 PASS 접기 대상이 아니며 아래 **통과 증거 다이어트**가 같은 다이어트를 ledger 형식에 적용한다
    - **통과 증거 다이어트**(소유자: `pr-review` correctness 계약 reference): 문제 있는 verdict(NOT MET·UNTESTED·PARTIAL·FAIL)만 증거 행으로 내고, 통과(MET)는 `MET: #1–#N` 꼴 축약 한 줄로 접는다. 판정-측 "증거 없는 MET 금지"는 보존하고 증거 본문 전사만 줄인다
- 구현의 test-first는 `sdd-orchestrator` SKILL.md `단계`의 구현 항목이 정한다: 끝나는 조건마다 실패하는 검사를 먼저 만들어 실패를 확인한 뒤 가장 작은 변경으로 통과시킨다. 검사는 테스트이거나, 테스트 프레임워크가 없는 자산이면 검색·diff·종료 코드로 판정하는 검사이고, 판정 가치가 없는 검사는 만들지 않는다. 검사의 종류와 강도(일부러 틀리게 바꿔 검사가 잡는지 보는 확인 등)는 모델이 위험에 맞게 정한다. 증거 없는 조건은 충족으로 적지 않는다
  - 검사가 닿지 않는 동작은 구현 리뷰가 본다: 검사가 통과하면 전체 diff를 처음부터 다시 읽어 요구사항 미구현, 검사가 통과해도 틀리게 동작할 수 있는 곳, 이 환경에서 실행해 보지 못한 조건, 요청에 없는 코드와 중복을 찾아 고치고 관련 검사만 다시 돌린다
- 마감은 계획 파일 `진행`에 조건별 판정과 증거를 적고 채팅에 보고한다. 보고 항목은 수행한 단계, 조건별 결과, 두 리뷰에서 찾아 고친 것, **실행으로 확인하지 못한 것**, 사용자 결정이 필요했던 지점과 고른 안, 남은 분할 기능이다. 계획이 기능을 나누면 첫 기능만 정한 종점까지 진행하고 멈춘다(남은 기능 자동 연속 없음)
  - 계획과 진행 상태는 계획 파일 하나가 가진다 — `_sdd/drafts/<YYYY-MM-DD>_feature_draft_<slug>.md`의 `진행` 절이 재개 지점이고, 충족으로 적히지 않은 조건은 재개 시 다시 판정한다. digest·state 인계 파일은 만들지 않으며, `_sdd/implementation/`의 예전 산출물은 spec 반영의 입력으로만 읽는다. 환경 함정은 spec 반영 단계가 저장소 작업에 반복 적용되는 사실만 `_sdd/env.md`로 올린다(기준의 단일 소스는 `sdd-orchestrator/references/spec-sync.md`). 문서 표면은 `docs/SDD_SPEC_DEFINITION.md` §6 증거 기록처 문장과 `docs/AUTOPILOT_GUIDE.md` 산출물 목록(각 ko·en)이다
  - 검사를 통과시키려고 검사를 약하게 고치지 않는다. 검사의 전제가 틀렸으면 무엇이 왜 틀렸는지 계획 파일에 적고 고친다
- 번들 내 leaf dispatch는 런타임 내장 범용 agent(Claude `general-purpose`, Codex 범용 sub-agent — read-only leaf는 active schema가 지원할 때만 `agent_type: "explorer"`)를 사용한다. custom agent를 번들에 추가하거나 중첩 spawn을 허용하지 않는다
- 모든 SDD 파이프라인 스킬의 SKILL.md는 실행 종료 전 자체 검증하는 `## Acceptance Criteria` 섹션을 갖는다 — 선택한 실행 경로에 적용되는 AC를 종료 전에 점검한다. 보완 가능한 산출물 누락은 수정하고, 비대상·이관·외부 blocker·이미 발생한 절차 위반은 해당 경로의 한계와 미충족을 보고한다. 과거 준수를 소급하거나 실패를 성공으로 표시하지 않으며 기존 재시도 상한을 넘지 않는다(`## Goal`은 권장 표면). AC는 그 스킬의 완료 신호 섹션(Required Output·반환·마감·보고 등)을 참조로 결속하고 상세를 재서술하지 않으며, 작성 체크리스트 canonical은 [docs/SKILL_AUTHORING_NORMS.md](../../docs/SKILL_AUTHORING_NORMS.md)다
- goal setup은 목표·권한·검증 기준·하네스 완성을 고정하고 대화 순서는 상황에 맡긴다. 이미 확정한 정보를 재수집하거나 최소 가설 수를 채우지 않는다.
- `sdd-autopilot`은 existing `goal-init(preset=sdd)`를 호출하는 setup-only thin entrypoint다. 사용자 목표와 관련 context를 runtime별 canonical 방식(Claude plugin-prefixed invocation / Codex active installed skill catalog)으로 전달하고, `goal-init`이 만든 자족적 조건 문자열·runtime 실행법·4파일 경로를 relay한 뒤 사용자 activation 경계에서 종료한다
  - setup에서는 `sdd-orchestrator`나 initial feature를 실행하지 않고 native goal을 활성화하지 않는다. current goal status도 조회하지 않으며 existing goal을 set·clear·pause·resume·replace·merge하거나 active goal 때문에 setup을 차단하지 않는다
  - SDD preset은 generic `goal-init`의 결과 중심 판단 기준, condition self-check, `goal.md`·`experiments.md`·`journal.md`·`report.md` 4파일 계약, 작성 뒤 하네스 리뷰를 그대로 재사용하고 `goal.md`의 `Loop Protocol` payload만 바꾼다. `goal.md`는 조건 문자열(outcome 수준 DONE WHEN + 위조 어려운 anchor + 표준 레시피 참조 문구 + drift 가드·위임 CONSTRAINT) / 검증 레시피(브리틀 검증 디테일 — goal 재설정 없이 수정 가능) / 자율 수행 위임(루프 중 행동에 대한 사용자의 durable authorization — 수준 `unattended`|`attended`, 사전 승인·항상 확인 목록, 질문 대체 규칙; 하류 스킬·런타임 규범의 "실행 전 확인"은 사전 승인 범위에서 이 섹션으로 충족되며 `git` 스킬의 `승인` 규칙이 이를 인정한다) / Loop Protocol(HOW)의 4분할 계약이다. 자율 수준은 setup의 Decision Criteria에 따라 확정한다 — 이미 정한 수준·범위는 재사용하고, 수준이 미정이면 원문의 "알아서/무인" 신호로 `unattended`, 수준·신호 모두 없으면 1회 질문. 루프 중 확인 요청은 사용자가 답할 수 없어 무진척과 같다는 것이 근거다
  - 사용자가 native goal을 활성화한 뒤에는 미충족 `DONE WHEN` 또는 실패한 final integration proof gap에서 가장 작은 next feature를 골라 `sdd-orchestrator`로 진행(reviewed draft가 없으면 계획 단계부터, 있으면 구현 단계부터 구현 리뷰까지, persistent 변경이 있으면 spec-sync 단계까지) → evidence·gap 기록 → final integration proof로 수렴한다. draft가 분할되면 current goal 안에서 smallest next unit을 계속 선택하며 nested `goal-init`은 만들지 않는다
  - formal Goal Contract·scope ID·Initial Feature Queue·status manifest·goal-level reviewer는 도입하지 않고, 조건·하네스 shape·loop payload의 단일 소스는 `goal-init`에 둔다
- SDD 체인 진입은 **사용자 요청이 판정한다**(하네스 §3 canonical): SDD는 사용자의 직간접 요청 — 스킬 호출(`discussion`·`sdd-orchestrator` 등) 또는 "SDD로 구현/작업하자" 류 지시 — 으로 적용된다. 요청이 없더라도 구현할 기능이 크거나 복잡하거나 스펙에 상당한 영향을 주는 작업이면 **SDD 적용 여부를 사용자에게 질문**하고, 그 외에는 비대상으로 보고 SDD 없이 바로 수행한다. 비적용 경로에서도 §2 작업 규약·검증 표준은 그대로 지키며, 스펙 변경이 생기면 `sdd-orchestrator`의 spec-sync 단계 실행 여부를 사용자에게 확인받는다. canonical은 하네스 §3이고 전파 표면은 `AGENTS.md` + `spec-create`·`spec-upgrade` 하네스 템플릿 4미러 = 5곳이라, 두 스킬이 초기화하는 모든 소비 repo의 하네스에 적용된다
- SDD 체인(feature-draft → plan-review → implementation → implementation-review → spec-sync)의 기본이자 유일한 실행 경로는 `sdd-orchestrator`(Claude·Codex)이고, **메인 세션이 모든 단계를 직접 수행한다** — 단계 worker·리뷰 전용 agent·인계 파일·단계별 모델 옵션을 두지 않는다. 스킬은 단계 순서와 모델이 추론할 수 없는 저장소 규약(계획 파일 경로와 마커, 사용자 결정 처리, 증거 없는 충족 금지, spec 반영 규약)만 정하고, 단계의 방법·깊이·검증 강도는 모델이 작업 크기와 위험에 맞게 정한다. 독립 리뷰는 PR 시점의 `pr-review`가 선택 수단이다. 양 runtime의 `sdd-orchestrator` 디렉터리는 동일본이다(`SKILL.md` + `references/spec-sync.md`). 구 단계 스킬 이름 5개는 호환 별칭 스킬(Claude·Codex)로 남는다 — 별칭 본문은 로직 없이 `../sdd-orchestrator/SKILL.md`를 읽어 호출 이름으로 따르고, 예전 스킬 범위(`feature-draft`=계획+계획 리뷰까지, `plan-review`·`implementation-review`=리뷰만 수정 없음, `implementation`=구현+구현 리뷰까지, `spec-sync`=spec 반영만)는 `sdd-orchestrator` `단계와 진입`의 호출 이름 표가 단일 소스로 정한다. 자연어 요청(기능 초안·계획, 구현 실행, 구현 리뷰, spec 동기화)은 계속 `sdd-orchestrator` description의 트리거가 받는다. 명령 진입은 Claude `/sdd-skills:sdd-orchestrator`, Codex `$sdd-orchestrator`다. 요청만 있으면 계획부터, 계획 파일이 있으면 그 `진행`이 가리키는 곳부터(진행 기록이 없으면 계획 리뷰부터) 시작하고, 사용자가 단계·종점을 지정하면 그 범위만 실행한다(기본 종점은 spec 반영). discussion은 `discussion` 스킬이 맡고 그 요약 파일은 입력 포인터로만 쓴다. 계획 파일명 glob은 `*_feature_draft_*`이고, 고정 구조는 `spec-update-todo-input` 마커 쌍으로 감싼 `Spec Delta`와 `계획`·`진행` 세 절 제목뿐이다(단일 소스는 SKILL `계획 파일` 절, 예전 `Part 1`/`Part 2` 형식 파일도 입력으로 받는다)
  - 사용자 결정은 답에 따라 구조·범위·바꿀 자리가 달라지는 것만 한 번에 하나씩 묻고, 이미 승인된 결정과 일상적인 선택은 다시 묻지 않는다. 무인 실행을 맡았으면 묻지 않고 가장 합당한 안으로 진행해 그 지점과 고른 안을 마감 보고에 적는다. git 쓰기는 사용자가 요청했거나 미리 승인했을 때만 한다
- subagent 모델 override는 `pr-review`의 correctness·simplicity worker에 있는 런타임별 option이다. 호출 지정이 없으면 `_sdd/env.md` `## Worker Model Defaults`의 현재 runtime 표 `pr-review` 행을 쓰고(두 worker에 같게 적용), 적용값이 없으면 런타임 기본 동작을 따른다
  - `pr-review` — Claude Code는 `--model <sonnet|opus|haiku|fable>`로 두 worker `Agent(...)` 호출의 model만 override한다
  - `pr-review` — Codex는 `--model`과 `--effort`를 분리해 각각 선택된 active `spawn_agent` schema의 `model`·`reasoning_effort` enum으로 검증하고 해당 필드를 override한다. 두 spawn 모두에 적용되며 `pr-review`는 고정 allowlist를 소유하지 않고, 요청 필드가 없거나 값이 enum 밖이면 dispatch 전에 schema가 노출한 허용값과 함께 blocker를 보고한다. 문서의 구체 모델·effort 값은 현재 예시일 뿐 persistent contract가 아니다
- non-trivial planning은 `sdd-orchestrator`의 계획 단계에서 시작한다. 후속 phase/task 확장 스킬은 없다 — 바꿀 자리와 끝나는 조건의 대응을 한눈에 검산할 수 없을 만큼 크면 기능 단위로 나눈다
- skill-defined output artifact의 이력 관리는 `prev/` 백업 체인보다 append-only artifact와 git history를 기본으로 사용한다
- spec mutation은 target file을 식별한 뒤에만 수행한다
- current spec model과 workflow semantics의 기준은 [docs/SDD_SPEC_DEFINITION.md](../../docs/SDD_SPEC_DEFINITION.md)와 [docs/SDD_WORKFLOW.md](../../docs/SDD_WORKFLOW.md)에 둔다
- 환경 및 실행 제약은 [../env.md](../env.md)를 authoritative source로 본다
- `Strategic Code Map`은 agentic coding을 위한 optional navigation hint로만 사용한다. 전체 파일 트리, 컴포넌트 카탈로그, API reference, 구현 narrative로 확장하지 않으며, temporary `Touchpoints`는 검증된 persistent entrypoint / extension point / invariant hotspot / validation surface가 된 경우에만 global supporting surface로 승격한다

## 3. 핵심 설계와 주요 결정

### 핵심 설계

SDD Skills의 설계는 다음 층으로 나뉜다.

1. Skill layer: 사용자가 직접 호출하는 entrypoint — 계약의 단일 소스(`SKILL.md` + `references/` 계약 문서; dispatch는 런타임 내장 agent에 계약을 프롬프트로 주입)
2. Artifact layer: `_sdd/` 아래의 persistent handoff contract
3. Reference layer: README, `docs/`, global spec이 유지하는 설명과 경계

이 위에 별도의 **Harness layer(`AGENTS.md`)** 가 놓인다. harness는 repo 작업 진입점이자 작업 규약(how) 레이어로, global spec(이해 = what/why)과 같은 정보를 중복 보유하지 않는다 — repo-specific 행동 트리거와 핵심 결정은 여전히 Guardrails가 단일 소스다. harness는 산문 규약과 그 규약을 실행하는 자산(훅)을 함께 포함하며, 자산은 규약을 **강제**하거나(work log 커밋 게이트) 컨텍스트에서 사라진 규약을 **되돌려 놓는다**(compact 후 SessionStart 재주입 — "읽으라는 지시"가 아니라 내용 주입: 지시는 재량이 남아 실패 모드를 재생산하고 Read 왕복 대비 비용 이점도 없다). 둘 다 모델 재량으로 건너뛸 수 없는 층이다(advisory watchdog은 강제 층 밖 보조 자산). §0은 SDD 고유 불변식 3종만 배포한다 — `Separate Truth by Lifetime`·`Evidence Before Promotion`(AC 검증이 current truth 승격 조건 — 자동 spec-sync·사람 승인 의무 아님)·`Persist Outcomes, Not Process`(간결한 결정·결과·evidence·pointer 보존, 단계별 실행 서술 제외). 일반 agent 원칙은 배포 계약이 아니다([docs/agentic_coding_principle.md](../../docs/agentic_coding_principle.md)는 참고 자산). layer model 기준은 [docs/SDD_CONCEPT.md](../../docs/SDD_CONCEPT.md)와 [docs/SDD_WORKFLOW.md](../../docs/SDD_WORKFLOW.md)에 둔다.

### 유지해야 할 주요 결정

| 결정 | 현재 선택 | 유지 이유 |
|------|-----------|-----------|
| Skill 정의 형식 | Markdown `SKILL.md` 단일 파일 — frontmatter가 name/description(+ 런타임이 읽는 선택 키) 등 스킬 메타데이터의 단일 소스이고, 스킬 버전을 담는 필드·파일은 두지 않는다(스킬 변경 이력 = git history) | AI 에이전트가 직접 읽고 실행 규약을 추론하기 쉽다. 런타임이 읽지 않는 메타데이터는 사이드카 파일(구 `skill.json`)이든 frontmatter 필드(구 `version:`)든 드리프트가 감지되지 않는 채 누적되므로, 소비자가 없는 값은 두지 않고 버전 lockstep 검사 대상을 0으로 유지한다 |
| 런타임 구조 | Claude/Codex dual bundle | 동일한 SDD 철학을 유지하면서 플랫폼별 실행 차이를 흡수한다 |
| Codex/Claude hook parity and dual-setting runtime acceptance | 공용 script 4개는 `.claude/hooks/` 실행 경로를 공유하고, `spec-create`·`spec-upgrade`는 `.claude/settings.json`과 `.codex/hooks.json`을 독립·멱등 병합한다. 구조 parity만으로 완료 처리하지 않고 Codex trust boundary와 양 runtime lifecycle acceptance까지 검증한다 | 기존 Claude 경로와 소비 repo 호환성을 유지하면서 실행 bytes를 한 벌로 공유하고, 한쪽 설정 손상이 다른 runtime 설치를 막지 않게 한다. 사용자 설정 보존·명시적 trust·실제 lifecycle 증거를 완료 조건에 포함해 등록만 된 무발동 상태나 위험한 trust 우회를 parity로 오인하지 않는다 |
| Codex multi-agent runtime adapter | active tool schema로 mailbox 또는 legacy target/close contract 중 정확히 하나를 선택한다. `agent_type` 같은 role selector는 지원될 때만 추가하고, 없으면 framed `message` 계약을 주입한 범용 sub-agent를 사용한다. legacy target/close는 target wait와 close lifecycle이 함께 노출될 때만 사용한다 | runtime 이름을 capability의 대리값으로 쓰지 않아 schema 세대 차이를 안전하게 흡수하고, 선택적 role selector의 부재를 lifecycle blocker로 오인하지 않으면서 존재하지 않는 lifecycle 호출·혼합 contract·지원되지 않는 사용자 요청 override 전달은 차단한다 |
| 실행 분리 | skill과 그 `references/` 계약이 단일 소스이고 번들에 custom agent를 두지 않는다. SDD 체인은 `sdd-orchestrator`가 메인 세션에서 직접 수행하고, 번들에서 agent를 띄우는 스킬은 `pr-review`뿐이며 그 correctness·simplicity 렌즈가 `orchestrator skill + 계약 경로·주입 범용 leaf agent`다 | 계약을 스킬 표면 한 곳에 모아 번들 배포(skills-only)와 nesting 1단계 제한을 함께 만족한다. SDD 체인을 worker로 나누면 받는 쪽이 같은 코드를 다시 읽어 벽시계가 단계·agent 수에 비례해 늘었고, 한 세션 직접 수행이 같은 기능을 약 1/3 시간에 같은 계약 결과로 끝냈다(실측 근거는 decision_log 2026-11-17, 2026-10-04 worker 구조를 대체) |
| 상태 전달 | `_sdd/` 파일 아티팩트 중심 | 세션 메모리 의존을 줄이고 재현성과 git 추적성을 높인다 |
| 품질 게이트 | AC-First + explicit verification | "should work" 식 추측을 줄이고 종료 조건을 명확히 한다 |
| 장문 산출물 작성 | producer-owned inline 2-phase writing | skeleton/fill/finalize를 같은 문맥에서 처리해 품질 저하를 줄인다 |
| spec template load interface | `spec-create` Step 4는 compact를 기본으로 하되 source의 project motivation·evaluated-alternative rationale를 compact의 named slot에 의미 손실 없이 보존할 수 없을 때만 full을 고르고, 작성 직전에 선택한 runtime-local template 하나의 전체 skeleton을 verbatim 적용한다. Claude template pair가 authoring canonical이고 Codex pair는 runtime invocation token만 다른 distribution mirror다. `spec-upgrade`는 고치기 직전에 package-local `references/spec-format.md` 하나를 읽는다. 이 파일이 목표 구조, compact·full skeleton과 선택 기준(`spec-create`와 같은 기준), 예전 내용을 내릴 자리를 함께 소유하며 양 runtime 동일본이다 | rich reference를 실제 소비 시점에만 읽고 template·temporary shape의 소유자를 하나로 유지해, stale 복제와 memory reconstruction drift를 막는다 |
| document producer output interface | `guide-create`는 작성 직전에 runtime-local rich reference(`references/output-format.md`)의 fenced skeleton을 verbatim 복사하며, reference가 명시한 슬롯 치환·반복 행·조건부 생략 외에는 어떤 줄도 추가·삭제·재배열·요약하지 않는다. 사용자 지정 언어에 맞춘 표시 제목·label 번역은 계층·순서·필드 의미를 유지하는 범위에서 허용하며, output shape·rubric은 그 reference 한 곳만 소유한다. main loop가 skeleton을 직접 작성·검증하며 runtime helper lifecycle이나 완성 example로 같은 계약을 재소유하지 않는다 | 실제 산출물 interface를 한 곳에서 기계적으로 소비하면 설명·예시·runtime mirror 사이의 format drift를 줄인다 |
| SDD goal 실행 경계 | `sdd-autopilot`은 `goal-init(preset=sdd)` setup adapter이고, 실제 반복 실행은 사용자가 활성화한 native goal의 SDD Loop Protocol이 소유한다. setup은 `sdd-orchestrator` 실행·goal status 조회·goal mutation을 하지 않는다 | harness 준비와 실행 activation을 분리해 existing goal에 대한 숨은 상태 변경을 막고, generic goal 계약을 재사용하면서 여러 SDD unit의 수렴은 native goal lifecycle에 맡긴다 |
| 규모 초과 대응 | 승격이 아니라 분할 — 분할 필요 판정(coverage 눈검산 불가)은 롤링 분할 draft + spec-sync 단계의 planned todo 고정 + feature별 순차 체인으로 해소한다. active SDD goal에서는 current goal이 smallest next unit을 계속 선택하고 nested `goal-init`을 만들지 않는다 | 규모 초과를 더 큰 파이프라인이나 nested goal로 올리면 실행 상태가 분산된다. 분할은 "단일 컨텍스트 = 품질 전제"를 유지하면서 하나의 goal이 integration proof까지 수렴하게 한다 |
| planning precedence | `sdd-orchestrator`의 계획 단계가 유일 planning entry. 후속 확장 스킬 없음 — 규모 초과는 분할 | non-trivial 변경에서 peer-choice 혼선을 없애고 "단일 컨텍스트 = 품질 전제"를 유지한다 |
| 리뷰 수행 주체 | 메인 세션 자기 리뷰 — `sdd-orchestrator`가 계획 리뷰와 구현 리뷰를 같은 세션에서 한 번씩 하고 찾은 것을 그 자리에서 고친다. 독립 리뷰 agent·두 번째 리뷰·심각도별 fix 정책은 두지 않고, 실행으로 확인하지 못한 것을 마감 보고에 남긴다. 독립 리뷰는 PR 시점의 `pr-review`(선택)다 | 재현 실측에서 시간은 단계·agent 수(모델 생성 시간)가 결정했고, 한 세션 자기 리뷰가 독립 리뷰가 잡던 자리를 처리했다(decision_log 2026-11-17). 작성자가 자기 맹점을 놓칠 위험은 실행 미확인 목록과 PR 시점 독립 리뷰로 보완한다 |
| implementation test-first | 메인 세션이 끝나는 조건마다 실패하는 검사를 먼저 만들어 실패를 확인한 뒤 가장 작은 변경으로 통과시킨다. 검사의 종류와 강도는 모델이 위험에 맞게 정하고, 검사를 약하게 고쳐 통과시키지 않는다(문면은 SKILL `단계`가 소유) | test-first 규율과 falsifiability를 유지하고, 증거 없는 "충족" 보고와 테스트 약화 퇴화를 차단한다. 검사가 닿지 않는 동작은 구현 리뷰가 diff를 다시 읽어 본다 |
| 직교 2-렌즈 review 렌즈 | correctness ∥ simplicity(계약 `pr-review/references/simplicity-contract.md`) — 적용 지점은 PR review다(`pr-review`: correctness worker(계약 경로 Read) + simplicity worker(전체 4차원 1회, 계약 verbatim 주입)를 한 메시지로 동시에 dispatch하고 메인 루프는 verdict 합성·리포트만, `--model`·`--effort`와 env.md `pr-review` 행은 두 worker에 같게 적용). simplicity는 falsifiable-only gating | 정확성과 동작-불변 형태 품질을 disjoint 표적으로 분리해 검출 범위를 넓히고, 벽시계는 병렬 렌즈의 max가 결정한다. `pr-review` correctness도 worker로 옮겨 메인 맥락을 보호하고 작성(메인 리포트)/리뷰(worker)를 분리한다(2026-10-05 사용자 결정) |
| subagent model override | `pr-review`가 correctness·simplicity 두 worker에 같게, 호출 지정 > `_sdd/env.md` `## Worker Model Defaults`의 `pr-review` 행 > 런타임 기본 동작 순으로 적용한다. Claude는 model만, Codex는 model·effort를 독립 지정한다 | 선택 모델에 맞게 effort를 별도로 조절한다. 기본값은 커밋 파일 `_sdd/env.md`에 두어 매 호출 지정 없이 저장소별로 유지하고, 허용값은 repo allowlist 없이 활성 런타임의 지원 범위로 검증한다 |
| spec 구조 | thin global spec + execution-focused temporary spec | 장기 기준과 일회성 실행 정보를 분리해 drift를 줄인다 |
| spec sync 진입점 | `sdd-orchestrator`의 spec-sync 단계 — 메인 세션이 `references/spec-sync.md` 규약을 수행한다. 구현 전/후 구분은 별도 진입점이 아니라 evidence-driven status 분류로 처리 | 두 진입점(`spec-update-todo`/`spec-update-done`) 이분 진입을 제거해 운영 표면을 줄이면서, 코드+validation evidence 유무로 동작이 자동 적응한다 |
| spec lifecycle 진입점 | spec을 처음 만드는 일은 `spec-create`, 이미 있는 spec의 점검·정리·형식 이행·하네스 갱신은 `spec-upgrade` 하나가 맡는다. `spec-upgrade`는 요청이 점검이면 spec과 하네스를 고치지 않고(요청받은 보고서 파일만 쓴다), 요청이 분명하지 않거나 인자 없이 부르면 점검만 하며, 그 밖에는 고친 뒤 하네스를 갱신한다. 대상은 `_sdd/spec/`이며 계획 파일의 검토는 `sdd-orchestrator`의 계획 리뷰가 맡는다. 예전 이름(`spec-review`·`spec-rewrite`)의 별칭 스킬은 두지 않고 `spec-upgrade` description의 trigger 문구가 받는다 | 점검·정리·형식 이행은 같은 판단 기준 4개와 같은 첫 단계(점검)를 쓴다. 스킬을 나누면 어느 스킬인지 가르는 단계와 중복 참조 파일이 생긴다(decision_log 2026-11-18) |
| spec 점검 판정 인터페이스 | `spec-upgrade`의 점검은 근거가 약한 발견을 `UNTESTED`로 두고 심각도를 올리지 않으며, 접근 실패나 탐색 미완을 부재로 판정하지 않는다(필요한 범위를 다 찾았고 한쪽에만 없을 때만 누락). 결론은 spec 수정 필요 / 수정 불필요 / 논의 필요 중 하나이고, 코드가 spec과 다르고 spec이 옳으면 spec 수정이 아니라 구현 쪽 조치로 보고한다 | 불충분 evidence를 부재로 오판하거나 구현 측 drift를 spec 변경으로 잘못 라우팅하는 일을 막는다 |
| Strategic Code Map | optional compact navigation surface | global spec을 inventory로 되돌리지 않으면서 사람과 LLM agent가 entrypoint, contract source, invariant hotspot, extension point, validation surface를 빠르게 찾게 한다 |
| artifact naming/history | lowercase canonical artifact를 기본으로 하고, skill contract가 정의한 output surface는 dated slug naming과 git-history-first 추적을 따른다 | 산출물 경로 추론을 단순화하고 legacy fixed-name drift를 줄인다 |
| canonical rollout 순서 | `definition -> generators/transformers -> consumers/planners -> docs -> english mirrors/examples -> audit` | definition, skill behavior, human docs drift를 줄인다 |

### 운영상 반드시 유지할 구조적 판단

- SDD 체인 단계는 `_sdd/` 산출물을 다음 단계 입력 계약으로 사용한다
- temporary delta는 global truth를 반복 복사하지 않고, 변경 범위와 검증 정보만 다룬다
- skill-defined output artifact는 dated slug + glob-based discovery를 canonical로 사용하고, legacy uppercase/fixed-name artifact는 transition fallback으로만 읽는다
- canonical model 변경은 definition 문서와 workflow 문서에서 먼저 선언하고, 이후 generator/consumer/docs가 따라간다
- supporting docs는 global decision-bearing truth를 복제하지 않고, reference 역할만 수행한다
- spec lifecycle skill은 `Strategic Code Map`을 현재 코드 탐색의 출발점으로만 사용해야 한다. 계획 단계의 바꿀 자리는 항상 현재 코드 실측으로 확인한다
- spec-sync 단계는 코드+validation evidence가 있는 항목만 현재 사실로 승격하고, evidence 없는 항목은 기본적으로 `🚧 Planned` 또는 보류로 둔다. verified truth와 planned truth를 같은 문단·불릿에 무표식으로 섞지 않는다(미구현·미검증을 완료 사실로 기록하지 않는 안전 불변식)

### 현재 운영 제약

- 🚧 Planned / 미검증: 실제 Astra/Fable의 스킬 선택·대화·도구 사용 효과는 별도 실행 관측이 필요하다. 이번 변경은 저장소 소스에 한정하며 설치된 plugin cache·외부 adapter는 갱신하지 않았다.

- Claude와 Codex 문서/skill parity는 완전 자동 동기화가 아니라 유지보수자의 수동 관리다 — SKILL.md 짝과 references 계약 문서 짝의 3-way 적응 미러링이 유지보수 단위다
- 이 저장소는 전통적인 테스트 프레임워크보다 실제 skill invocation과 리뷰 기반 검증에 크게 의존한다
- dispatch되는 agent/skill은 작업트리가 아니라 **plugin 설치본**(`~/.claude/plugins/cache/<marketplace>/<plugin>/<pushed SHA>/`)에서 로드된다 — 방금 편집한 agent 본문은 커밋·푸시로 플러그인이 갱신되기 전까지 그 세션의 dispatch에 발효되지 않는다(실측: 설치본에 당일 편집한 규칙 0/5, 전날 머지분은 존재). 따라서 **같은 세션의 마감 게이트로 자기 변경의 효과를 계측하는 설계는 구조적으로 무효**이고, agent 행동 계측은 (a) 커밋·푸시 후 플러그인 갱신 + (b) 검증 대상 개념을 호출자 digest에 넣지 않은 새 세션을 전제조건으로 갖는다. 규칙이 로드되지 않은 실행은 그 규칙의 반증이 아니다. 같은 이유로 **동시 A/B 대조는 불가능하다** — 활성 설치본은 시점당 하나뿐이라 처치군과 대조군을 같은 시각에 돌릴 수 없다. 따라서 agent 행동 변경의 효과 확인은 도입 전후의 **누적 관측**으로만 설계할 수 있고, 대조군 회차 자체에 변동이 있으므로(같은 지표에서 회차별로 다른 값이 나온다) n=1 arm 비교로 결론내지 않는다
- agent 행동을 transcript로 계측할 때는 지표를 먼저 검증한다 — subagent transcript(JSONL)는 content 블록을 줄 단위로 쪼개 기록하므로 "메시지당 tool_use 수"는 배칭을 탐지하지 못하고, 유효 지표는 **연속 실행 길이**이며 양성 대조로 판별력을 확인한 뒤 쓴다. 자기 행동 보고는 transcript 계수로 교차검증하고, **tool 호출 수는 배칭 여지의 대리지표가 아니다** — 셸로 엮이는 작업은 이미 복합 명령 한 호출로 접혀 있어 호출 내용까지 봐야 여지를 과대 추정하지 않는다
- 🚧 Planned: tool call 배칭 규칙의 **행동 효과**는 미검증이다 — 전제조건을 갖춘 첫 처치군 관측 2회차가 음성(최대 연속 실행 길이 1, 지표 판별력은 양성 대조 완료). 규칙을 되돌리지도 강화하지도 않고 **배칭과 무관한 과제 2~3건을 더 쌓아** 연속 1이 고정인지 확인한 뒤 판정한다(지금 되돌리면 n=1 음성 결론, 지금 강화하면 효과 미확인 상태의 규칙 비대). 벽시계 절감 폭은 어떤 표본으로도 주장하지 않는다(회차 상세는 decision_log)
- `docs/` ko 본문과 `docs/en/` 미러의 세대 정합도 수동 관리다 — canonical rollout 순서의 `english mirrors` 단계가 가장 누락되기 쉬운 지점이고, 레이어·섹션 추가를 ko에만 반영하고 닫으면 en 짝이 한 세대 뒤처진다(하네스 레이어 추가가 en `SDD_WORKFLOW`·`SDD_CONCEPT`에 전파되지 않아 §2 Harness 누락 + 삭제된 full 레인 어휘 잔존으로 드러난 전례). ko/en 짝을 건드리는 변경은 대칭 마감을 검증 대상으로 둔다

## Supporting Surfaces

- [components.md](./components.md): component reference와 탐색용 code/navigation hint
- [usage-guide.md](./usage-guide.md): scenario-oriented usage guide와 expected result surface
- [decision_log.md](./decision_log.md): 구조 변경과 주요 spec 판단 이력
- [logs/changelog.md](./logs/changelog.md): 릴리스 및 문서 변경 이력
- [README.md](../../README.md), [docs/SDD_SPEC_DEFINITION.md](../../docs/SDD_SPEC_DEFINITION.md), [docs/SDD_WORKFLOW.md](../../docs/SDD_WORKFLOW.md): 설치, canonical model, workflow semantics 기준 문서
- [docs/SKILL_AUTHORING_NORMS.md](../../docs/SKILL_AUTHORING_NORMS.md): 스킬·agent·하네스 문서를 작성/수정할 때 점검하는 Claude 5 세대 제작 규범 체크리스트(런타임 참조 문서 아님 — [docs/agentic_coding_principle.md](../../docs/agentic_coding_principle.md)와 같은 참고 자산 계층)
