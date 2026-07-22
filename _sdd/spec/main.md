# SDD Skills

> Markdown 기반 skill bundle로 AI 에이전트의 Spec-Driven Development 워크플로우를 Claude Code와 Codex에서 공통 계약으로 실행한다.

**Spec Version**: 4.6.5
**Last Updated**: 2026-07-22
**Status**: Approved
**Canonical Role**: current thin global spec

이 문서는 repo-wide `개념 + 경계 + 결정`만 고정하는 thin global spec이다. 상세 component reference는 [components.md](./components.md), 사용 시나리오와 기대 결과는 [usage-guide.md](./usage-guide.md), 구조 변경 이력은 [decision_log.md](./decision_log.md), 릴리스/문서 변경 이력은 [logs/changelog.md](./logs/changelog.md), 환경과 실행 제약은 [../env.md](../env.md)에서 확인한다.

## 1. 배경 및 high-level concept

### 문제 정의

AI 코딩 에이전트는 강한 생성 능력을 갖고 있지만, 프로젝트의 문제 정의, 설계 경계, 검증 기준이 고정돼 있지 않으면 같은 저장소에서도 매번 다른 추론을 하게 된다. 기존 개발 방법론은 사람 중심 운영을 전제로 하므로, 에이전트가 스펙을 읽고 구현하고 검증하고 다시 스펙을 갱신하는 루프를 직접 실행하기에는 계약이 느슨하다.

### high-level concept

SDD Skills는 이 문제를 `SKILL.md = 실행 가능한 프롬프트`라는 관점으로 푼다.

- global spec은 얇은 기준 문서로 남기고, 변경 실행에는 temporary spec과 implementation artifact를 분리한다
- 사용자 진입점은 skill layer에 유지하고, 재사용 가능한 execution unit은 agent layer로 분리한다
- 스킬 간 persistent handoff는 숨겨진 메모리가 아니라 `_sdd/` 파일 아티팩트에 남긴다
- 검증은 부가 옵션이 아니라 workflow contract의 일부로 취급한다

### 왜 이 접근을 택하는가

| 접근 | 장점 | 한계 | 판정 |
|------|------|------|------|
| SDD skill bundle | 스펙을 Single Source of Truth로 유지하고, 사람과 AI가 같은 파일 기반 계약을 공유한다 | 스킬/문서 유지 비용이 있다 | 채택 |
| 프롬프트 라이브러리 | 시작이 빠르다 | 스킬 간 연결과 산출물 계약이 약하다 | 비채택 |
| 코드 중심 자동화만 사용 | 익숙한 CI/CD 자산을 활용할 수 있다 | 자연어 기반 계획, spec sync, decision capture가 약하다 | 비채택 |

### 이 repo를 읽는 관점

이 저장소는 Claude Code와 Codex에서 공통으로 사용할 수 있는 SDD workflow bundle이다. 사용자는 `/spec-create`, `/feature-draft-lite`, `/implementation-lite`, `/sdd-autopilot` 같은 명시적 skill entrypoint로 워크플로우를 시작하고, 저장소는 그 과정을 `_sdd/` 산출물과 문서 계약으로 추적 가능하게 만든다.

## 2. Scope / Non-goals / Guardrails

### In Scope

- `.claude/skills/`, `.codex/skills/`의 사용자 진입점과 workflow contract
- `.claude/agents/`, `.codex/agents/`의 재사용 가능한 planning/review/implementation unit
- global spec, temporary spec, `_sdd/` artifact layout, decision log, changelog
- README와 `docs/`의 개념/정의/워크플로우/가이드 문서
- Claude plugin 구조와 Codex bundle/config 배포 규약

### Non-goals

- Claude Code나 Codex의 호스트 런타임 자체를 대체하지 않는다
- 애플리케이션 런타임이나 서비스 배포 파이프라인을 제공하지 않는다
- exhaustive inventory를 global spec 본문에 유지하지 않는다
- 모든 플랫폼 기능을 완전 동등하게 추상화하지 않는다

### Guardrails

- global spec은 thin decision document로 유지하고, execution detail은 `_sdd/drafts/`, `_sdd/implementation/`, `_sdd/pipeline/` 같은 temporary surface로 분리한다
- 사용자 entrypoint는 skill layer에, 재사용 execution unit은 agent layer에 둔다. dispatch된 agent는 sub-agent를 다시 spawn하지 않는다(nesting 1단계 제한)
  - leaf dispatch가 필요한 execution은 `orchestrator(skill) + leaf/producer(agent)` 형태로 둔다(메인 루프 skill/autopilot만 dispatch, agent는 단일 단위/단일 산출물만 처리)
  - dispatch가 없는 단순 위임 execution만 `wrapper-backed skill + single-source agent` 형태로 둔다
- persistent handoff는 `_sdd/spec/`, `_sdd/drafts/`, `_sdd/implementation/`, `_sdd/pipeline/`, `_sdd/discussion/`의 canonical 경로를 통해 이뤄진다
- 새 temporary artifact는 가능한 한 lowercase canonical 경로를 사용하고, skill contract가 dated slug 패턴을 정의한 output surface는 그 형식을 따라야 한다. reader는 legacy uppercase/fixed-name artifact를 fallback으로 읽을 수 있어야 한다
- 소비 repo에서 커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`·`drafts/`·`work_log/`이고(`drafts/`·`work_log/`는 구현 로그 자산), 나머지 process artifact(`_sdd/{discussion,implementation,pipeline,pr}/`)는 `.gitignore`(`SDD-WORKSPACE` 마커 블록)로 로컬 전용이다. `_sdd/env.md`는 커밋되므로 비밀값(API 키·토큰·비밀번호)을 적지 않는다. 단 이 sdd_skills repo는 스킬 개발 메타 repo라 process artifact를 history 가치로 계속 커밋하는 예외다(소비 repo 정책과 별개)
- wrapper-backed skill은 사용자 entrypoint와 artifact contract를 유지해야 하며, 지원하지 않는 동작을 조용히 흉내내지 않는다
  - wrapper는 thin entrypoint로 두고 전체 계약·프로세스는 agent를 단일 소스로 유지한다
  - 입력이 대화에서 태어나는 wrapper는 그 대화 맥락을 agent에 forwarding해야 한다(agent는 파일은 read하지만 대화는 읽지 못한다)
- review나 validation이 포함된 workflow는 review-only로 닫지 않고 fix 또는 명시적 잔여 이슈 보고로 마무리한다
  - 리뷰는 단일 패스가 유일하다 — re-review·iteration 기계장치는 없으며, finding 반영은 호출자 fix 1회다(lite 체인의 `plan-review` gate·`implementation-review` gate 모두 gate당 단일 패스 + fix 1회). full producer 스킬 3종이 소유하던 review→fix→re-review loop(공통 loop 정책)는 F2에서 full 레인과 함께 삭제됐고, reviewer 표면의 잔존(리포트 파일 mode·re-review mode·`plan-review-agent`의 full Tier rubric)도 F3에서 삭제돼 경량 반환 단일 패스가 유일 mode다. 구 "Tier 2-lite" 명칭은 소멸했다(유일 mode라 이름 불요)
  - simplicity finding은 falsifiable-only gating을 따른다: 동작 변화 없이 더 단순한 동등 형태를 구체적으로 제시할 수 있는 객관적 위반만 Medium 이상(gating)이고, 주관적 취향은 Low(advisory)다. gating을 falsifiable finding으로 한정하는 규칙이 수렴성의 핵심이다. simplicity 렌즈는 `spec-review`로 확장하지 않는다(코드 형태 품질이라 spec 문서 품질에 부적합)
  - 직교 2-렌즈 review의 현재 적용 지점은 PR review(`pr-review` 스킬)다 — `pr-review`는 correctness(`pr-review-agent`) ∥ simplicity(`simplicity-review-agent`) 두 read-only leaf reviewer를 병렬 dispatch하고 두 요약을 합쳐 verdict를 합성하는 orchestrator다. correctness 검증도 자체 inline이 아니라 dispatched agent이므로 `--model` override가 두 렌즈에 균일하게 적용된다. 표적은 disjoint하다(correctness=PR/spec 정합·AC·보안·테스트 + 정확성-중복, simplicity=동작-불변 형태 + 형태-중복). 두 reviewer는 파일을 쓰지 않고 경량 반환(finding별 위치·문제·수정 제안)으로 응답하며, orchestrator(스킬 메인 루프)가 통합 verdict 리포트(`_sdd/pr/..._pr_review_...`) 1파일만 write한다(단일 작성자 — 구 3파일 구조에서 축소, 반환이 통합 리포트의 유일 소스). 통합 리포트는 통계 표(metrics/severity 카운트) 없이 행동 대상 finding을 위치·문제·수정 블록 전문으로 싣는다 — correctness Critical/High와 simplicity falsifiable gating finding(Medium+, REQUEST CHANGES rationale 기여, verdict 자동 강제 없음)은 Pre-merge 섹션에, correctness Medium은 non-blocking 상세 블록으로, 주관(Low)은 위치 포함 한 문장으로 흐른다 — pr-review는 인간 리뷰 보조이므로 합집합 자동 exit를 적용하지 않는다. Medium=gating/Low=advisory 분류는 위 falsifiable-only gating 규칙을 그대로 재사용한다
  - reviewer agent 4종(`plan-review-agent`·`implementation-review-agent`·`simplicity-review-agent`·`pr-review-agent`)은 판정만 반환하는 read-only leaf다 — tools에 `Write`가 없고(correctness 계열 2종만 테스트 실행용 `Bash` 유지) 리포트 파일 작성은 호출자 소관이다(작성자 불변식의 reviewer 적용). orchestrator 스킬은 산출물을 직접 rewrite하지 않으며(산출물 단일 작성자), fix는 산출물 작성자(lite 체인에서는 메인 루프)가 수행한다
- 구현의 test-first는 `implementation-lite`가 메인 루프에서 직접 집행하는 실행 규율이다: task별 3-way triage — (a) test: 실패하는 테스트 작성 가능, (b) structural-check: 프레임워크 부재 자산이라도 grep·diff·exit code로 실질 구조를 판정 가능, (c) test-free: 동어반복 check뿐인 non-falsifiable task(분류 근거 1줄 기록 필수, "간단한 구현이라서"는 (c) 자격이 아니며 경계 애매하면 (b)로 보수 분류) — 이후 (a)/(b)는 RED 실패 관찰 전 구현 금지 → 최소 구현 GREEN → 마감 시 AC→증거 테이블(증거 없는 AC는 "충족" 금지). triage와 규칙의 canonical surface는 `implementation-lite` SKILL이다
  - 테스트 불변 규칙: RED 관찰 후에는 테스트를 통과시키기 위해 테스트를 약화·수정하지 않는다. 계약이 틀렸다고 판단되면 선언을 남기고 테스트 수정 → 재-RED 후 구현으로 돌아가며, 같은 task에서 선언이 반복되면 구현 중단 + draft 복귀다
  - 출제자·응시자 leaf 분리(`test-author-agent` 테스트 전용 / `implementation-agent` GREEN→REFACTOR 전용)와 orchestrator 소유 RED 게이트는 F2에서 full 레인과 함께 삭제됐다. 대체 안전장치는 위 테스트 불변 규칙 + `implementation-review`의 Fresh Verification(자기보고가 아닌 외부 재검증)이다
- skill의 agent invocation은 canonical 이름만 사용한다
  - Codex와 Claude 모두 kebab-case agent invocation을 canonical으로 사용한다(Codex `plan-review-agent`, Claude `sdd-skills:<agent>-agent`)
  - Legacy alias와 Codex underscore custom agent ID는 canonical이 아니며 normalize하지 않는다
- `sdd-autopilot`(v3.0.0)은 lite 체인 전용이다: orchestrator·pipeline artifact·승인 checkpoint 없이 메인 루프에서 `feature-draft-lite → plan-review`(단일 패스 경량 반환) `→ implementation-lite → implementation-review → spec-sync` 체인을 실행한다(Step 0 상태 확인 → Step 1 요청 분석 → Step L). full 레인(generated orchestrator 파이프라인)은 autopilot 표면에서 제거됐다 — SKILL 쌍 lite 전용 재작성, 부속 references/examples/scripts 삭제, `docs/AUTOPILOT_GUIDE.md`(ko·en) 2.0.0 재작성. 복구 경로는 git tag `full-lane-final`이고, legacy `_sdd/pipeline/` 산출물은 기록물로 무시한다
  - 규모 초과의 해소 수단은 오케스트레이션(full 전환)이 아니라 분할이다. lite 표면들은 full 전환을 안내하지 않으며, 단일 컨텍스트를 넘는 변경은 여러 lite feature로 분할한다 — 분할 draft는 롤링 형태(Part 1 마커 내부에 분할 feature 목록, Part 2는 첫 feature의 task만)로 작성하고, 분할 목록은 `spec-sync`(planned)가 feature별 개별 `🚧 Planned` todo로 global spec에 고정한 뒤 첫 feature부터 lite 체인을 순차 실행한다
  - census형 sweep(같은 대상의 변형 표기가 여러 파일에 흩어진 rename/전파류)은 분할 신호가 아니라 검증 대상이다 — 해당 draft는 마지막 read-only 검증 task(변형 표기 전수 grep census를 AC로)를 필수로 둔다
  - 분할 판정의 canonical은 lite 표면이 소유한다(`feature-draft-lite` 분할 규칙 / `implementation-lite` 중단·분할 규칙 / `plan-review` Lite 적격 검사). autopilot은 신호를 소비만 하고 재정의하지 않는다
- full 전용 실행 유닛은 삭제 완료다(F2): agent 쌍 4종(`feature-draft-agent`·`task-ordering-agent`·`test-author-agent`·`implementation-agent`)과 스킬 쌍 3종(`feature-draft`·`implementation`·`implementation-plan`)은 존재하지 않으며, 등록 표면(marketplace.json skills 21·agents 7, `.codex/agents/README.md`, 루트 README Subagent Model Override 목록)은 lite 체인 기준이다. 일반 구현 요청 트리거("implement the plan"·"start implementation"·"execute the plan"·"구현해줘" 계열)는 `implementation-lite`(v1.2.0)가 유일 수신 경로로 흡수했고 "병렬 구현" 계열 트리거는 폐기됐다
- full 레인 실체 삭제는 완결됐다(F1~F4 — 롤링 분할 draft `_sdd/drafts/2026-07-22_feature_draft_lite_full_lane_removal.md` 순차 실행). F4에서 잔재 정리와 최종 census를 마쳤다: `_sdd/tests/` check 스크립트·무의미화된 test-free triage 확대 draft 폐기, F1~F3 이월 advisory sweep(spec-sync·spec-review agent 입력/감사 계약의 lite 기준 재서술 포함), repo 전체 full 어휘 census — live 표면(`.claude/`·`.codex/`·`.claude-plugin/`·`docs/`·`README.md`·`AGENTS.md`)의 full 고유 식별자 잔존 0(허용 예외: `_sdd/` 기록물, AUTOPILOT_GUIDE tag 복구 안내, `docs/SDD_SPEC_DEFINITION.md` = F5 소관). 복구 보험은 git tag `full-lane-final`. 근거 요약: lite 품질이 full 대비 동등하면서 훨씬 빠르고, full급 복잡도는 분할로 해소하며, 분기 제거로 하네스 전파 표면이 준다(상세는 decision_log 2026-07-22 entry)
  - 🚧 Planned F5: `-lite` 개명 — 이름+개념 전부(사용자 확정, F2의 이름 충돌 해소로 가능해짐). 스킬 `feature-draft-lite`→`feature-draft`·`implementation-lite`→`implementation`(디렉토리·name 필드·marketplace·전체 호출 참조), 개념 어휘 교체("lite 체인"→"SDD 체인"·"lite draft"→"draft"·`> Lite 적격:` 마커 재명명), `docs/SDD_SPEC_DEFINITION.md` 정합, `_sdd/spec/`의 잔여 full 서술·lite 개념 어휘 트림, 기존 draft 파일명 glob 양쪽 호환 유지, 자체 개명 census
  - 삭제 범위 밖(불변): lite 체인 자체의 기능 변경, 레인 무관 스킬(spec 파이프라인·pr-review·ralph·discussion 등)
- subagent를 dispatch하는 review 계열 스킬(`plan-review`·`implementation-review`·`pr-review`)의 subagent 모델 override는 런타임별 explicit per-call option으로만 취급한다. 옵션을 생략하면 세션/agent 기본값을 상속하며, persistent custom agent 정의를 수정하지 않는다. lite 구현·planning 스킬은 메인 루프 직접 작성이라 override 비대상이다
  - Claude Code는 `--model <sonnet|opus|haiku|fable>`로 `Agent(...)` 호출의 model만 override한다
  - Codex는 `--model <gpt-5.5|gpt-5.4|gpt-5.4-mini>`와 `--effort <low|medium|high|xhigh>`를 분리해 `spawn_agent(...)`의 `model` / `reasoning_effort`를 override한다. `gpt-5.5-high` 같은 결합형 값은 canonical syntax가 아니다
- non-trivial planning은 `feature-draft-lite`에서 시작한다. 후속 phase/task 확장 스킬은 없다 — 단일 컨텍스트 초과는 분할 규칙으로 해소한다
- 구현 전 계획 품질 점검이 필요하면 `plan-review`를 review-only gate로 사용한다. 이 gate는 plan을 직접 수정하지 않고 경량 반환으로만 응답하며(리포트 파일 없음), Critical/High finding만 implementation blocker로 표시한다
- skill-defined output artifact의 이력 관리는 `prev/` 백업 체인보다 append-only artifact와 git history를 기본으로 사용한다
- spec mutation은 target file을 식별한 뒤에만 수행한다
- current spec model과 workflow semantics의 기준은 [docs/SDD_SPEC_DEFINITION.md](../../docs/SDD_SPEC_DEFINITION.md)와 [docs/SDD_WORKFLOW.md](../../docs/SDD_WORKFLOW.md)에 둔다
- 환경 및 실행 제약은 [../env.md](../env.md)를 authoritative source로 본다
- `Strategic Code Map`은 agentic coding을 위한 optional navigation hint로만 사용한다. 전체 파일 트리, 컴포넌트 카탈로그, API reference, 구현 narrative로 확장하지 않으며, temporary `Touchpoints`는 검증된 persistent entrypoint / extension point / invariant hotspot / validation surface가 된 경우에만 global supporting surface로 승격한다

## 3. 핵심 설계와 주요 결정

### 핵심 설계

SDD Skills의 설계는 다음 층으로 나뉜다.

1. Skill layer: 사용자가 직접 호출하는 entrypoint
2. Agent layer: 재사용 가능한 execution unit
3. Artifact layer: `_sdd/` 아래의 persistent handoff contract
4. Reference layer: README, `docs/`, global spec이 유지하는 설명과 경계

이 위에 별도의 **Harness layer(`AGENTS.md`)** 가 놓인다. harness는 repo 작업 진입점이자 작업 규약(how) 레이어로, global spec(이해 = what/why) 위에서 작업 시작 시 먼저 읽는 surface다. global spec 본문을 키우지 않는 별도 레이어이며(둘은 같은 정보를 중복 보유하지 않는다), 작업 원칙·읽는 순서·검증 표준·워크플로우 단계 순서·판단 기준 포인터만 담는다. repo-specific 행동 트리거와 핵심 결정은 여전히 global spec Guardrails가 단일 소스다. layer model과 사용 시점의 기준은 [docs/SDD_CONCEPT.md](../../docs/SDD_CONCEPT.md)와 [docs/SDD_WORKFLOW.md](../../docs/SDD_WORKFLOW.md)에 둔다.

### 유지해야 할 주요 결정

| 결정 | 현재 선택 | 유지 이유 |
|------|-----------|-----------|
| Skill 정의 형식 | Markdown `SKILL.md` | AI 에이전트가 직접 읽고 실행 규약을 추론하기 쉽다 |
| 런타임 구조 | Claude/Codex dual bundle | 동일한 SDD 철학을 유지하면서 플랫폼별 실행 차이를 흡수한다 |
| 실행 분리 | skill entrypoint + reusable agent. leaf dispatch가 필요한 execution(`pr-review` 2-렌즈 병렬, `investigate` 조건부 explore fan-out)은 `orchestrator skill + leaf agent`, 단순 위임 execution은 `wrapper skill + single-source agent`, lite 구현·planning은 메인 루프 직접 작성 | direct invocation 재사용성을 확보하면서 nesting 1단계 제한 안에서 dispatch를 메인 루프 skill로 올린다 |
| 상태 전달 | `_sdd/` 파일 아티팩트 중심 | 세션 메모리 의존을 줄이고 재현성과 git 추적성을 높인다 |
| 품질 게이트 | AC-First + explicit verification | "should work" 식 추측을 줄이고 종료 조건을 명확히 한다 |
| 장문 산출물 작성 | producer-owned inline 2-phase writing | skeleton/fill/finalize를 같은 문맥에서 처리해 품질 저하를 줄인다 |
| 오케스트레이션 | reasoning-based `sdd-autopilot` v3.0.0 — lite 체인 전용(메인 루프 스킬 체인, orchestrator·pipeline artifact 없음). generated orchestrator full 레인과 full 전용 agent·스킬은 제거됨 — 잔재 정리·census까지 완결(F1~F4, 복구는 git tag `full-lane-final`; `-lite` 개명은 §2 분할 todo F5 🚧 Planned) | 소규모~단일 컨텍스트 변경이 지배적인 흐름에서 orchestrator 생성 비용을 없애고, 규모 초과는 full 승격이 아니라 분할로 해소한다 |
| lite 레인 규모 초과 대응 | 승격이 아니라 분할 — lite 표면들은 full 전환을 안내하지 않고, 단일 컨텍스트 초과는 롤링 분할 draft + `spec-sync` planned todo 고정 + feature별 순차 lite 체인으로 해소한다. 분할 판정 canonical은 lite 표면 소유(autopilot은 신호 소비만) | 규모 초과를 더 큰 파이프라인으로 올리면 full 레인 의존이 재생산된다. 분할은 lite의 "단일 컨텍스트 = 품질 전제"를 유지하는 해소 수단이며 full 레인 삭제(F1~F4 완료)의 선행 조각이었다 |
| planning precedence | `feature-draft-lite`가 유일 planning entry. 후속 확장 스킬 없음 — 규모 초과는 분할 | non-trivial 변경에서 peer-choice 혼선을 없애고 "단일 컨텍스트 = 품질 전제"를 유지한다 |
| plan quality gate | optional `plan-review` review-only gate — 단일 패스 경량 반환(리포트 파일 없음) | 구현 전 Target Files, task boundary, verification weakness, overengineering smell을 findings-first로 드러내되 plan 자체는 수정하지 않는다 |
| implementation test-first | `implementation-lite` 메인 루프가 직접 집행: task별 (a) test / (b) structural-check / (c) test-free triage → (a)/(b)는 RED 관찰 전 구현 금지 → 최소 구현 GREEN → 테스트 불변 규칙(약화·수정 금지, 계약 오류는 선언 후 재-RED) → AC→증거 테이블 마감. leaf 분리(test-author/implementation agent)와 orchestrator RED 게이트는 F2에서 삭제됨 — 대체 안전장치는 테스트 불변 규칙 + `implementation-review` Fresh Verification | 소규모 구현에서 dispatch 오버헤드 없이 test-first 규율과 falsifiability를 유지하고, 증거 없는 "충족" 보고와 테스트 약화 퇴화를 차단한다 |
| 직교 2-렌즈 review 렌즈 | correctness(`pr-review-agent`) ∥ simplicity(`simplicity-review-agent`) 직교 2-reviewer 병렬 dispatch — 현재 적용 지점은 PR review. orchestrator가 verdict 합성, 자동 강제 없이 correctness Critical/High → blocker·simplicity Medium+ → REQUEST CHANGES rationale 기여. 두 렌즈가 dispatched agent라 subagent model override가 균일 적용되고 simplicity는 falsifiable-only gating (implementation gate 적용분은 F2에서 full 레인과 함께 제거) | 정확성과 동작-불변 형태 품질을 disjoint 표적으로 분리해 한 reviewer에 과부하 없이 검출 범위를 넓히고, 벽시계는 병렬로 유지하면서 falsifiable 한정으로 수렴성을 보장한다. PR review는 인간 보조라 합집합 자동 exit 대신 rationale 기여로 합류시킨다 |
| subagent model override | review 계열 스킬(`plan-review`·`implementation-review`·`pr-review`)의 subagent 호출은 필요할 때만 런타임별 per-call option으로 모델/추론 강도를 override한다. Claude는 `--model` 단일 옵션, Codex는 `--model`과 `--effort` 분리 옵션을 canonical로 둔다 | 기본 세션/agent 설정 상속을 보존하면서 특정 실행만 강도·비용·속도에 맞게 조절할 수 있고, 플랫폼별 tool schema 차이를 숨기지 않아 잘못된 결합형 모델 ID 파싱을 피한다 |
| spec 구조 | thin global spec + execution-focused temporary spec | 장기 기준과 일회성 실행 정보를 분리해 drift를 줄인다 |
| spec sync 진입점 | 단일 `spec-sync` 스킬 + `spec-sync-agent`. 구현 전/후 구분은 별도 스킬이 아니라 evidence-driven status 분류로 처리 | 두 진입점(`spec-update-todo`/`spec-update-done`) 이분 진입을 제거해 운영 표면을 줄이면서, 코드+validation evidence 유무로 동작이 자동 적응한다 |
| Strategic Code Map | optional compact navigation surface | global spec을 inventory로 되돌리지 않으면서 사람과 LLM agent가 entrypoint, contract source, invariant hotspot, extension point, validation surface를 빠르게 찾게 한다 |
| artifact naming/history | lowercase canonical artifact를 기본으로 하고, skill contract가 정의한 output surface는 dated slug naming과 git-history-first 추적을 따른다 | 산출물 경로 추론을 단순화하고 legacy fixed-name drift를 줄인다 |
| canonical rollout 순서 | `definition -> generators/transformers -> consumers/planners -> docs -> english mirrors/examples -> audit` | definition, skill behavior, human docs drift를 줄인다 |

### 운영상 반드시 유지할 구조적 판단

- draft/plan/review skill chain은 `_sdd/` 산출물을 다음 단계 입력 계약으로 사용한다
- temporary delta는 global truth를 반복 복사하지 않고, 변경 범위와 검증 정보만 다룬다
- skill-defined output artifact는 dated slug + glob-based discovery를 canonical로 사용하고, legacy uppercase/fixed-name artifact는 transition fallback으로만 읽는다
- canonical model 변경은 definition 문서와 workflow 문서에서 먼저 선언하고, 이후 generator/consumer/docs가 따라간다
- supporting docs는 global decision-bearing truth를 복제하지 않고, reference 역할만 수행한다
- spec lifecycle skill은 `Strategic Code Map`을 현재 코드 탐색의 출발점으로만 사용해야 한다. `feature-draft-lite` planning의 `Target Files`는 항상 현재 코드 실측으로 확인한다
- `spec-sync`는 코드+validation evidence가 있는 항목만 현재 사실로 승격하고, evidence 없는 항목은 기본적으로 `🚧 Planned` 또는 보류로 둔다. verified truth와 planned truth를 같은 문단·불릿에 무표식으로 섞지 않는다(미구현·미검증을 완료 사실로 기록하지 않는 안전 불변식)

### 현재 운영 제약

- Claude와 Codex 문서/skill parity는 아직 완전 자동 동기화가 아니라 유지보수자의 관리가 필요하다. wrapper-backed skill에서는 agent가 단일 소스이므로 "skill 본문과 agent 본문을 함께 미러링"하는 의무는 대부분 해소됐고, 유지보수는 agent 본문과 thin wrapper의 entrypoint/dispatch 정합으로 좁혀졌다(claude/codex 양 플랫폼 parity는 여전히 수동 관리)
- 일부 version metadata 갱신은 여전히 문서 편집 discipline에 의존한다
- 이 저장소는 전통적인 테스트 프레임워크보다 실제 skill invocation과 리뷰 기반 검증에 크게 의존한다

## Supporting Surfaces

- [components.md](./components.md): component reference와 탐색용 code/navigation hint
- [usage-guide.md](./usage-guide.md): scenario-oriented usage guide와 expected result surface
- [decision_log.md](./decision_log.md): 구조 변경과 주요 spec 판단 이력
- [logs/changelog.md](./logs/changelog.md): 릴리스 및 문서 변경 이력
- [README.md](../../README.md), [docs/SDD_SPEC_DEFINITION.md](../../docs/SDD_SPEC_DEFINITION.md), [docs/SDD_WORKFLOW.md](../../docs/SDD_WORKFLOW.md): 설치, canonical model, workflow semantics 기준 문서
