# SDD Skills

> Markdown 기반 skill bundle로 AI 에이전트의 Spec-Driven Development 워크플로우를 Claude Code와 Codex에서 공통 계약으로 실행한다.

**Spec Version**: 4.4.1
**Last Updated**: 2026-06-22
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

이 저장소는 Claude Code와 Codex에서 공통으로 사용할 수 있는 SDD workflow bundle이다. 사용자는 `/spec-create`, `/feature-draft`, `/implementation`, `/sdd-autopilot` 같은 명시적 skill entrypoint로 워크플로우를 시작하고, 저장소는 그 과정을 `_sdd/` 산출물과 문서 계약으로 추적 가능하게 만든다.

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
  - 직접 호출 경로에서도 자기 산출물 품질 gate가 필요한 producer 스킬(`feature-draft`, `implementation-plan`, `implementation`)은 review-fix loop를 직접 소유하는 orchestrator다
- persistent handoff는 `_sdd/spec/`, `_sdd/drafts/`, `_sdd/implementation/`, `_sdd/pipeline/`, `_sdd/discussion/`의 canonical 경로를 통해 이뤄진다
- 새 temporary artifact는 가능한 한 lowercase canonical 경로를 사용하고, skill contract가 dated slug 패턴을 정의한 output surface는 그 형식을 따라야 한다. reader는 legacy uppercase/fixed-name artifact를 fallback으로 읽을 수 있어야 한다
- 소비 repo에서 커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`뿐이고, process artifact(`_sdd/{discussion,drafts,implementation,pipeline,pr,work_log}/`)는 `.gitignore`(`SDD-WORKSPACE` 마커 블록)로 로컬 전용이다. `_sdd/env.md`는 커밋되므로 비밀값(API 키·토큰·비밀번호)을 적지 않는다. 단 이 sdd_skills repo는 스킬 개발 메타 repo라 process artifact를 history 가치로 계속 커밋하는 예외다(소비 repo 정책과 별개)
- wrapper-backed skill은 사용자 entrypoint와 artifact contract를 유지해야 하며, 지원하지 않는 동작을 조용히 흉내내지 않는다
  - wrapper는 thin entrypoint로 두고 전체 계약·프로세스는 agent를 단일 소스로 유지한다
  - 입력이 대화에서 태어나는 wrapper는 그 대화 맥락을 agent에 forwarding해야 한다(agent는 파일은 read하지만 대화는 읽지 못한다)
- review나 validation이 포함된 workflow는 review-only로 닫지 않고 fix/re-review 또는 명시적 잔여 이슈 보고로 마무리한다
  - 산출물 producer 스킬(`feature-draft`, `implementation-plan`, `implementation`)은 autopilot 없이 직접 호출되는 경로에서도 외부 reviewer agent를 호출하는 review→fix→re-review loop를 자체 소유한다
  - 공통 loop 정책은 autopilot `orchestrator-contract.md` §6에서 차용한다(exit `critical=high=medium=0`, MAX 기본 3회, 매 라운드 loop 범위 전체 재리뷰, MAX 도달 시 critical/high 잔존이면 중단·보고하고 medium만 잔존이면 로그 후 진행)
  - implementation-scoped review-gate(`implementation` 스킬 phase/final gate, autopilot global/per-group/final-integration gate)는 단일 reviewer가 아니라 표적이 disjoint한 두 read-only leaf reviewer를 병렬 dispatch한다: correctness(`implementation-review-agent` — 정확성/AC/버그/보안/spec drift)와 simplicity(`simplicity-review-agent` — 동작-불변 형태: 중복·죽은 코드·단일 사용처 추상화·도달 불가 에러 처리·과잉압축). gating exit는 두 report의 합집합 `critical=high=medium=0`이다. simplicity 렌즈는 `spec-review`로 확장하지 않는다(코드 형태 품질이라 spec 문서 품질에 부적합)
  - simplicity finding은 falsifiable-only gating을 따른다: 동작 변화 없이 더 단순한 동등 형태를 구체적으로 제시할 수 있는 객관적 위반만 Medium 이상(gating)이고, 주관적 취향은 Low(advisory)다. 병렬화는 벽시계만 줄이고 수렴은 보장하지 않으므로 gating을 falsifiable finding으로 한정하는 규칙이 수렴성의 핵심이다
  - simplicity 렌즈는 implementation-scoped review-gate에 더해 PR review(`pr-review` 스킬)에도 적용한다 — `pr-review`는 자체 correctness 검증 ∥ `simplicity-review-agent` 병렬 dispatch의 PR 차원 직교 2-렌즈 review이며, 표적은 disjoint하다(correctness=PR/spec 정합·보안·테스트·verdict + 정확성-중복, simplicity=동작-불변 형태 + 형태-중복). simplicity reviewer는 read-only leaf로 자기 리포트(`_sdd/implementation/...`)만 write하고 pr-review는 자기 리포트(`_sdd/pr/...`)만 write한다. simplicity finding은 verdict를 자동 강제하지 않고 falsifiable gating finding(Medium+)이 REQUEST CHANGES rationale에 기여하며 주관(Low)은 Suggested Improvements로 흐른다 — pr-review는 인간 리뷰 보조이므로 implementation gate의 합집합 자동 exit를 적용하지 않는다. Medium=gating/Low=advisory 분류는 위 falsifiable-only gating 규칙을 그대로 재사용한다
  - fix는 producer/leaf agent 재dispatch로 수행하고 orchestrator 스킬은 산출물을 직접 rewrite하지 않는다(산출물 단일 작성자). 두 reviewer의 finding은 합산되어 기존 단일 fix 경로(`implementation-agent` 순차 재dispatch)로 처리되며, simplicity reviewer도 코드/리포트 외 산출물을 직접 수정하지 않는다
- `sdd-autopilot`이 생성하는 orchestrator는 planning producer output을 downstream 입력으로 소비하기 전에 `plan-review` gate를 통과시켜야 한다
  - `feature-draft-agent` / `implementation-plan-agent` output이 gate를 통과하지 못하면 finding을 implementation fix task로 변환하지 않고 producer output을 reject/regenerate 대상으로 돌린다
- `sdd-autopilot` 생성 orchestrator의 agent invocation은 canonical 이름만 사용한다
  - Codex와 Claude 모두 kebab-case agent invocation을 canonical으로 사용한다(Codex `feature-draft-agent`, Claude `sdd-skills:<agent>-agent`)
  - Legacy alias와 Codex underscore custom agent ID는 normalize하지 않고 reject/regenerate한다
- non-trivial planning은 기본적으로 `feature-draft`에서 시작하고, `implementation-plan`은 phase/task 세분화가 필요할 때만 follow-up expansion으로 붙인다
- 구현 전 계획 품질 점검이 필요하면 `plan-review`를 review-only gate로 사용한다. 이 gate는 plan을 직접 수정하지 않고 Critical/High finding만 implementation blocker로 표시한다
- multi-phase plan은 문서 장식이 아니라 execution gate다
  - `implementation-plan`의 phase `Checkpoint` 필드가 group boundary를 결정하며, `Checkpoint=true` phase 직후에만 review-fix gate를 닫는다. group 내 phase는 light validation만 수행한다
  - final integration review는 그룹 수에 따라 adaptive하게 처리한다(1개 그룹이면 마지막 group gate가 겸함, 2개+ 이상이면 별도 1회 추가)
  - 마지막 phase를 제외한 phase에 `Checkpoint` metadata가 없으면 schema violation으로 보고 single late gate로 fallback하지 않는다
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
| 실행 분리 | skill entrypoint + reusable agent. leaf dispatch가 필요한 execution(`implementation` fan-out, `feature-draft`/`implementation-plan` review-fix loop)은 `orchestrator skill + producer/leaf agent`, 단순 위임 execution은 `wrapper skill + single-source agent` | direct invocation과 autopilot 재사용성을 확보하면서 nesting 1단계 제한 안에서 dispatch를 메인 루프 skill로 올린다 |
| 상태 전달 | `_sdd/` 파일 아티팩트 중심 | 세션 메모리 의존을 줄이고 재현성과 git 추적성을 높인다 |
| 품질 게이트 | AC-First + explicit verification | "should work" 식 추측을 줄이고 종료 조건을 명확히 한다 |
| 장문 산출물 작성 | producer-owned inline 2-phase writing | skeleton/fill/finalize를 같은 문맥에서 처리해 품질 저하를 줄인다 |
| 오케스트레이션 | reasoning-based `sdd-autopilot` + generated orchestrator contract | 고정 템플릿보다 현재 맥락에 맞는 pipeline을 구성하되, producer review gate와 implementation dispatch controller 같은 실행 불변조건은 생성물에 명시해야 한다 |
| planning precedence | small direct path 외에는 `feature-draft`를 기본 planning entry로 두고 `implementation-plan`은 후속 확장 단계로 사용 | non-trivial 변경에서 peer-choice 혼선을 줄이고 task/phase 분해 기준을 일정하게 유지한다 |
| plan quality gate | optional `plan-review` review-only gate | 구현 전 Target Files, task boundary, verification weakness, overengineering smell을 findings-first로 드러내되 plan 자체는 수정하지 않는다 |
| producer 스킬 자체 품질 gate | `feature-draft`/`implementation-plan`/`implementation`이 review→fix→re-review loop를 직접 소유(orchestrator). fix=producer/leaf agent 재dispatch, 산출물 단일 작성자 | autopilot 없이 직접 호출되는 경로에서도 산출물이 reviewer gate를 통과하도록 보장한다. producer/reviewer agent는 sub-agent를 spawn하지 못하므로 loop orchestration은 메인 루프(스킬)가 소유해야 한다 |
| autopilot producer handoff gate | generated orchestrator가 `feature-draft-agent` / `implementation-plan-agent` output을 `plan-review-agent`로 검증한 뒤 downstream 소비 | autopilot이 wrapper skill을 우회해 custom agent를 직접 호출해도 직접 호출 경로와 같은 planning quality gate를 유지한다 |
| multi-phase quality gate | `per-group` review-fix (Checkpoint boundary) + adaptive `final integration review`; missing non-final `Checkpoint`는 reject/regenerate | 의미 있는 group 단위로 review depth를 높이고, review 비용과 latency를 줄이면서 cross-group regression은 adaptive final review로 커버한다 |
| 직교 2-렌즈 review 렌즈 | correctness ∥ simplicity(`simplicity-review-agent`) 직교 2-reviewer 병렬 dispatch를 두 진입점에 적용: implementation review-gate(correctness=`implementation-review-agent`, gating exit는 두 report 합집합 `critical=high=medium=0`)와 PR review(`pr-review` 자체 correctness 렌즈, verdict 자동 강제 없이 Medium+ → REQUEST CHANGES rationale 기여). 양쪽 모두 simplicity는 falsifiable-only gating | 정확성과 동작-불변 형태 품질을 disjoint 표적으로 분리해 한 reviewer에 과부하 없이 검출 범위를 넓히고, 벽시계는 병렬로 유지하면서 falsifiable 한정으로 수렴성을 보장한다. PR review는 인간 보조라 합집합 자동 exit 대신 rationale 기여로 합류시킨다 |
| spec 구조 | thin global spec + execution-focused temporary spec | 장기 기준과 일회성 실행 정보를 분리해 drift를 줄인다 |
| spec sync 진입점 | 단일 `spec-sync` 스킬 + `spec-sync-agent`. 구현 전/후 구분은 별도 스킬이 아니라 evidence-driven status 분류로 처리 | 두 진입점(`spec-update-todo`/`spec-update-done`) 이분 진입을 제거해 운영 표면을 줄이면서, 코드+validation evidence 유무로 동작이 자동 적응한다 |
| Strategic Code Map | optional compact navigation surface | global spec을 inventory로 되돌리지 않으면서 사람과 LLM agent가 entrypoint, contract source, invariant hotspot, extension point, validation surface를 빠르게 찾게 한다 |
| artifact naming/history | lowercase canonical artifact를 기본으로 하고, skill contract가 정의한 output surface는 dated slug naming과 git-history-first 추적을 따른다 | 산출물 경로 추론을 단순화하고 legacy fixed-name drift를 줄인다 |
| canonical rollout 순서 | `definition -> generators/transformers -> consumers/planners -> docs -> english mirrors/examples -> audit` | definition, skill behavior, human docs drift를 줄인다 |

### 운영상 반드시 유지할 구조적 판단

- draft/plan/review skill chain은 `_sdd/` 산출물을 다음 단계 입력 계약으로 사용한다
- temporary delta는 global truth를 반복 복사하지 않고, 변경 범위와 검증 정보만 다룬다
- multi-phase implementation plan은 review-fix scope와 phase exit 기준을 실제 execution control로 제공해야 한다
- generated orchestrator에서 `implementation-agent` / `sdd-skills:implementation-agent` step은 feature/phase 전체 leaf call이 아니라 autopilot이 task-level leaf calls로 fan out하는 dispatch controller다
- skill-defined output artifact는 dated slug + glob-based discovery를 canonical로 사용하고, legacy uppercase/fixed-name artifact는 transition fallback으로만 읽는다
- canonical model 변경은 definition 문서와 workflow 문서에서 먼저 선언하고, 이후 generator/consumer/docs가 따라간다
- supporting docs는 global decision-bearing truth를 복제하지 않고, reference 역할만 수행한다
- spec lifecycle skill은 `Strategic Code Map`을 현재 코드 탐색의 출발점으로만 사용해야 한다. `feature-draft`와 implementation planning의 `Touchpoints` / `Target Files`는 항상 현재 코드로 재확인한다
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
