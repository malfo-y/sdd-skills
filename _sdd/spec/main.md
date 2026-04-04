# SDD Skills

> Markdown 기반 skill bundle로 AI 에이전트의 Spec-Driven Development 워크플로우를 Claude Code와 Codex에서 공통 계약으로 실행한다.

**Spec Version**: 4.0.1
**Last Updated**: 2026-04-04
**Status**: Approved
**Canonical Role**: current global spec index + normative decision document

이 문서는 current canonical global spec이다. 상세 component reference는 [components.md](./components.md), 사용 시나리오 상세는 [usage-guide.md](./usage-guide.md), 운영 이력은 [DECISION_LOG.md](./DECISION_LOG.md)와 [logs/changelog.md](./logs/changelog.md)에서 추적한다.

## 1. 배경 및 high-level concept

### 문제 정의

AI 코딩 에이전트는 강한 생성 능력을 갖고 있지만, 프로젝트의 문제 정의, 설계 경계, 검증 기준이 고정돼 있지 않으면 같은 저장소에서도 매번 다른 추론을 하게 된다. 기존 개발 방법론은 사람 중심 운영을 전제로 하므로, 에이전트가 스펙을 읽고 구현하고 검증하고 다시 스펙을 갱신하는 루프를 직접 실행하기에는 계약이 느슨하다.

### high-level concept

SDD Skills는 이 문제를 "SKILL.md = 실행 가능한 프롬프트"라는 관점으로 푼다.

- 글로벌 스펙은 얇은 기준 문서로 남기고, 변경 실행에는 temporary spec과 implementation artifact를 분리한다.
- 사용자 진입점은 skill layer에 유지하고, 재사용 가능한 실행 단위는 agent layer로 분리한다.
- 스킬 간 handoff는 숨겨진 메모리가 아니라 `_sdd/` 파일 아티팩트로 고정한다.
- 검증은 부가 옵션이 아니라 contract/invariant와 연결된 필수 단계로 취급한다.

### 왜 이 접근을 택하는가

| 접근 | 장점 | 한계 | 판정 |
|------|------|------|------|
| SDD skill bundle | 스펙을 Single Source of Truth로 유지하고, 사람과 AI가 같은 파일 기반 계약을 공유한다 | 스킬/문서 유지 비용이 있다 | 채택 |
| 프롬프트 라이브러리 | 시작이 빠르다 | 스킬 간 연결과 산출물 계약이 약하다 | 비채택 |
| 코드 중심 자동화만 사용 | 익숙한 CI/CD 자산을 활용할 수 있다 | 자연어 기반 계획, spec sync, decision capture가 약하다 | 비채택 |

### 프로젝트가 제공하는 가치

이 저장소는 Claude Code와 Codex에서 공통으로 쓸 수 있는 SDD workflow bundle을 제공한다. 사용자는 `/spec-create`, `/feature-draft`, `/implementation`, `/sdd-autopilot` 같은 명시적 skill entrypoint를 통해 요구사항 정의, 구현, 리뷰, spec sync를 구조화할 수 있고, 저장소는 그 과정을 `_sdd/` 아티팩트와 문서 계약으로 추적 가능하게 만든다.

## 2. Scope / Non-goals / Guardrails

### In Scope

| 영역 | 포함 내용 |
|------|-----------|
| Skill bundle | `.claude/skills/`, `.codex/skills/`에 있는 사용자 진입점과 workflow contract |
| Reusable execution units | `.claude/agents/`, `.codex/agents/`의 재사용 가능한 planning/review/implementation unit |
| Spec system | 글로벌 스펙, temporary spec, `_sdd/` artifact layout, decision log, changelog |
| Human-facing docs | README와 `docs/`의 개념/정의/워크플로우/가이드 문서 |
| Platform packaging | Claude plugin 구조와 Codex bundle/config 배포 규약 |

### Non-goals

- 호스트 런타임 자체를 대체하지 않는다. Claude Code와 Codex의 실행 엔진은 외부 플랫폼 책임이다.
- 애플리케이션 런타임이나 서비스 배포 파이프라인을 제공하지 않는다. 이 저장소의 핵심 산출물은 문서와 skill contract다.
- 코드 전체를 문서로 복제하는 exhaustive inventory를 글로벌 스펙 본문에 유지하지 않는다.
- 모든 플랫폼 기능을 완전 동등하게 추상화하지 않는다. `git`, `second-opinion`처럼 플랫폼 전용 기능은 명시적으로 분리한다.

### Guardrails

- 글로벌 스펙은 얇은 기준 문서여야 하며, 실행 delta는 `_sdd/drafts/`, `_sdd/implementation/`, `_sdd/pipeline/`로 분리한다.
- spec을 바꾸는 흐름은 기존 파일을 먼저 `prev/`에 백업하고, decision-bearing truth만 본문에 남긴다.
- wrapper-backed skill은 사용자 entrypoint를 유지하되, 실제 재사용 execution unit과 artifact contract를 바꾸지 않는다.
- 리뷰가 포함된 workflow는 review-only로 끝나지 않고 fix/re-review 또는 명시적 잔여 이슈 보고로 닫혀야 한다.
- 환경 및 실행 제약은 `_sdd/env.md`를 기준으로 본다.

## 3. 핵심 설계와 주요 결정

### 핵심 설계

SDD Skills의 설계는 네 층으로 나뉜다.

1. Skill layer: 사용자가 직접 호출하는 entrypoint.
2. Agent layer: 재사용 가능한 execution unit.
3. Artifact layer: `_sdd/` 아래의 persistent handoff contract.
4. Reference layer: README, `docs/`, 글로벌 스펙이 유지하는 설명과 경계.

### 유지해야 할 주요 결정

| 결정 | 현재 선택 | 유지 이유 |
|------|-----------|-----------|
| Skill 정의 형식 | Markdown `SKILL.md` | AI 에이전트가 직접 읽고 실행 규약을 추론하기 쉽다 |
| 런타임 구조 | Claude/Codex dual bundle | 동일한 SDD 철학을 유지하면서 플랫폼별 실행 차이를 흡수한다 |
| 실행 분리 | wrapper skill + reusable agent | 사용자 진입점 보존과 autopilot 재사용성을 동시에 확보한다 |
| 상태 전달 | `_sdd/` 파일 아티팩트 중심 | 세션 메모리 의존을 줄이고 재현성과 git 추적성을 높인다 |
| 품질 게이트 | AC-First + explicit verification | "should work" 식 추측을 줄이고 종료 조건을 명확히 한다 |
| 장문 산출물 작성 | producer-owned inline 2-phase writing | skeleton/fill/finalize를 같은 문맥에서 처리해 품질 저하를 줄인다 |
| 오케스트레이션 | reasoning-based `sdd-autopilot` | 고정 템플릿보다 현재 맥락에 맞는 pipeline을 구성할 수 있다 |
| spec 구조 | thin global spec + execution-focused temporary spec | 장기 기준과 일회성 실행 정보를 분리해 drift를 줄인다 |
| canonical rollout 순서 | `definition -> generators/transformers -> consumers/planners -> docs -> english mirrors/examples -> audit` | 설명 문서와 실제 skill behavior가 split-brain 상태로 어긋나는 것을 막는다 |

### 현재 운영 제약

- Claude와 Codex 문서/skill parity는 아직 완전 자동 동기화가 아니라 유지보수자가 의식적으로 맞춰야 한다.
- 일부 version metadata 갱신은 여전히 문서 편집 discipline에 의존한다.
- 이 저장소는 전통적인 테스트 프레임워크보다 실제 skill invocation과 리뷰 기반 검증에 크게 의존한다.

## 4. Contract / Invariants / Verifiability

### Contract

| ID | Subject | Inputs/Outputs | Preconditions | Postconditions | Failure Guarantees |
|----|---------|----------------|---------------|----------------|--------------------|
| C1 | 글로벌 스펙과 workflow artifact 배치 | 입력은 사용자 요청, 기존 글로벌 스펙, 관련 `_sdd/` 산출물이다. 출력은 `_sdd/spec/`, `_sdd/drafts/`, `_sdd/implementation/`, `_sdd/pipeline/`의 canonical 경로에 기록된다 | 관련 skill이 설치돼 있고, 대상 저장소에서 `_sdd/` 구조를 읽거나 생성할 수 있어야 한다 | persistent truth는 `_sdd/` 경로에 남고, 후속 skill이 이를 다시 읽을 수 있다 | prerequisite가 부족하면 경로를 꾸며내지 않고 누락/차단 사유를 보고한다 |
| C2 | wrapper-backed skill 실행 계약 | 입력은 원래 사용자 요청이며, 출력은 Claude/Codex에서 같은 역할의 artifact contract를 따른다 | 대응 wrapper skill과 reusable agent 정의가 존재해야 한다. Codex는 `.codex/config.toml`의 agent depth 조건을 만족해야 한다 | 사용자 entrypoint는 유지되고, 재사용 execution unit은 동일한 handoff semantics로 동작한다 | 플랫폼 전용 기능은 명시적으로 제한하며, 지원하지 않는 동작을 조용히 흉내내지 않는다 |
| C3 | `sdd-autopilot` orchestration | 입력은 기능/작업 요청과 현재 repo 상태다. 출력은 orchestrator, pipeline log, 최종 report, 관련 구현/spec artifact다 | 글로벌 스펙이 존재하거나, 없으면 `spec-create`로 우회해야 한다 | pipeline은 reasoning 기반으로 조합되고, review 포함 시 review-fix-re-review 규칙을 존중한다 | spec 부재, pre-flight 실패, unresolved blocker는 누락 없이 로그/보고서에 남긴다 |
| C4 | spec mutation safety | 입력은 기존 spec 파일과 변경 근거다. 출력은 수정된 spec과 `prev/` 백업이다 | canonical target file이 식별돼야 하고, 변경이 global truth인지 temporary delta인지 구분돼야 한다 | 변경 전 원본이 `prev/prev_<filename>_<timestamp>.md`로 보존된다 | target이 불명확하면 임의 overwrite 대신 discussion 또는 rewrite 후보로 보고한다 |

### Invariants

| ID | Scope | Invariant | Why It Matters |
|----|-------|-----------|----------------|
| I1 | Spec model | 글로벌 스펙은 thin decision document이고, 변경 실행 정보는 temporary spec과 implementation artifact로 분리된다 | 글로벌 스펙이 inventory/backlog로 무거워지면 사람과 AI 모두 기준점을 잃는다 |
| I2 | Artifact flow | 스킬 간 persistent handoff는 `_sdd/` 파일 아티팩트를 통해 이뤄진다 | 플랫폼/세션이 달라도 재현 가능한 workflow를 유지할 수 있다 |
| I3 | Runtime architecture | 사용자 진입점은 skill layer에, 재사용 execution unit은 agent layer에 남는다 | direct invocation과 autopilot 재사용성을 동시에 유지한다 |
| I4 | Verification discipline | review나 validation이 명시된 workflow는 execute 이후 verify를 거쳐야 하며, review-only로 닫히지 않는다 | 검증되지 않은 산출물이 조용히 성공 처리되는 것을 막는다 |
| I5 | Canonical references | `docs/SDD_SPEC_DEFINITION.md`와 `docs/SDD_WORKFLOW.md`는 current spec model과 workflow semantics의 기준 문서다 | definition, skill behavior, human docs가 split-brain 상태로 어긋나는 것을 막는다 |

### Verifiability

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1, I2 | review | [`README.md`](../../README.md), [`docs/SDD_WORKFLOW.md`](../../docs/SDD_WORKFLOW.md), [`_sdd/env.md`](../env.md)로 artifact 경로와 운영 원칙을 교차 확인한다 |
| V2 | C2, I3 | review | `.claude/skills/`, `.claude/agents/`, `.codex/skills/`, `.codex/agents/`의 대응 관계와 [`components.md`](./components.md)를 확인한다 |
| V3 | C2 | runtime-check | [`../../.codex/config.toml`](../../.codex/config.toml)의 `agents.max_depth >= 2`와 `max_threads` 설정은 Codex custom agent spawn의 전제다 |
| V4 | C3, I4 | manual-check | 실제 `/sdd-autopilot`, `/implementation`, `/implementation-review` 실행 시 pipeline log와 final report에 review/verify 루프가 남는지 점검한다 |
| V5 | C4, I5 | review | `prev/` 백업 파일 존재 여부, [`DECISION_LOG.md`](./DECISION_LOG.md), [`docs/SDD_SPEC_DEFINITION.md`](../../docs/SDD_SPEC_DEFINITION.md) 동기화를 확인한다 |

## 5. 사용 가이드 & 기대 결과

상세 시나리오는 [usage-guide.md](./usage-guide.md)에 두고, 글로벌 스펙 본문에는 기대 결과의 기준만 남긴다.

| 시나리오 | 시작점 | 기대 결과 |
|----------|--------|-----------|
| 새 저장소 문서화 | `/spec-create` | `_sdd/spec/`와 `_sdd/env.md`가 bootstrap되고, workspace guidance 파일이 존재한다 |
| 대규모 기능 추가 | `/feature-draft` 또는 `/sdd-autopilot` | temporary spec/plan, 구현, review, global spec sync가 contract 순서대로 연결된다 |
| 구현 검증 | `/implementation-review` 또는 `/pr-review` | findings-first 결과와 검증 근거가 남고, unresolved issue는 숨기지 않는다 |
| 레거시 스펙 정비 | `/spec-upgrade` 또는 `/spec-rewrite` | 글로벌 스펙이 current canonical model로 정리되고, inventory는 supporting reference로 내려간다 |
| 상태 파악 및 의사결정 | `/spec-summary`, `/discussion` | 현재 spec 상태, open questions, next step이 빠르게 드러난다 |

추가 기대 결과:

- 사용자는 README와 docs를 읽고 설치/운영 경로를 선택할 수 있어야 한다.
- supporting spec 파일은 main.md의 section responsibility를 보조해야 하며, main body를 다시 비대하게 만들지 않아야 한다.
- 실패 시나리오는 "조용한 성공"이 아니라 명시적 보고, 로그, 또는 open question으로 표면화돼야 한다.

## 6. Decision-bearing structure

### 시스템 경계와 ownership

| Boundary | Owns | Excludes |
|----------|------|----------|
| User entry layer | `.claude/skills/`, `.codex/skills/`의 slash-command entrypoint와 wrapper/direct skill contract | 실행 플랫폼 내부 엔진 동작 |
| Reusable execution layer | `.claude/agents/`, `.codex/agents/`의 planning/review/implementation unit | 사용자-facing installation docs |
| Persistent artifact layer | `_sdd/spec/`, `_sdd/drafts/`, `_sdd/implementation/`, `_sdd/pipeline/`, `_sdd/discussion/` | 런타임 내부 상태나 비영속 메모리 |
| Reference & policy layer | `README.md`, `docs/`, `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md` | feature별 실행 산출물 |

### Cross-component contracts

| Contract Surface | Contract | Why It Matters |
|------------------|----------|----------------|
| wrapper skill -> agent | 원래 사용자 요청과 artifact contract를 그대로 넘긴다 | direct invocation과 orchestrated execution의 의미 차이를 줄인다 |
| draft/plan/review skill chain | `_sdd/drafts/`와 `_sdd/implementation/` 산출물은 다음 단계의 입력 계약이다 | 단계별 handoff가 끊기면 workflow가 split-brain이 된다 |
| global spec <-> temporary spec | temporary delta는 global truth를 반복 복사하지 않고 필요한 변경/검증 정보만 담는다 | 글로벌 스펙 비대화와 stale duplication을 막는다 |
| definition docs -> skills/docs | canonical model 변경은 definition 문서와 workflow 문서에서 먼저 선언되고, 이후 generator/consumer/human docs가 따라간다 | 문서와 skill behavior drift를 줄인다 |

### Extension points

| Extension Point | Required Preservation |
|-----------------|-----------------------|
| 신규 full skill 추가 | AC-First structure, `_sdd/` artifact contract, docs/skill description alignment를 유지한다 |
| 기존 skill의 wrapper/agent 전환 | 사용자 entrypoint는 유지하고, agent는 self-contained execution unit으로 분리한다 |
| autopilot 확장 | reasoning reference, pre-flight, review-fix, execute-verify 규칙을 깨지 않는다 |
| supporting docs 추가 | global spec의 decision-bearing truth를 복제하지 않고 reference 역할을 분명히 한다 |

### Invariant hotspots

| Hotspot | Risk If Broken | Primary Files |
|---------|----------------|---------------|
| current canonical model | global spec과 skill output이 서로 다른 문법을 쓰게 된다 | `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md`, `_sdd/spec/main.md` |
| wrapper/agent parity | 사용자 entrypoint와 reusable execution unit이 다른 결과를 낸다 | `.claude/skills/*/SKILL.md`, `.claude/agents/*.md`, `.codex/skills/*/SKILL.md`, `.codex/agents/*.toml` |
| artifact naming and placement | 후속 skill이 이전 산출물을 찾지 못한다 | `_sdd/spec/`, `_sdd/drafts/`, `_sdd/implementation/`, `_sdd/pipeline/` |
| environment/pre-flight assumptions | Codex nested agent 실행이나 PR 검증이 조용히 실패한다 | `_sdd/env.md`, `.codex/config.toml`, `README.md` |

## 7. 참조 정보

### Platform reference

| 항목 | Claude Code | Codex |
|------|-------------|-------|
| Skill surface | 21 skills | 19 skills |
| Reusable execution unit | 9 agents | 9 executable custom agents + `README.md` |
| 설치 방식 | plugin marketplace 중심 | bundle script, LobeHub, 수동 복사 |
| 대화형 입력 | full skill에서 platform-native UX 사용 | `request_user_input` 기반 |
| 전용 기능 | `git`, `second-opinion` 포함 | 해당 두 기능 제외 |

### Environment and installation

- 설치와 플랫폼별 실행 방법은 [`README.md`](../../README.md)를 기준으로 본다.
- 환경/검증 제약은 [`_sdd/env.md`](../env.md)를 authoritative source로 본다.
- Codex custom agent 실행 전제는 [`../../.codex/config.toml`](../../.codex/config.toml)의 `[agents]` 설정이다.
- 로컬 문서 작업에는 필수 환경 변수가 없고, PR 관련 skill 검증 시에만 `gh` 인증이 필요할 수 있다.

### Documentation mirrors and collateral

- `docs/en/`은 한국어 `docs/`의 semantic mirror layer다. current canonical model rollout 이후 `docs/en/sdd.md`까지 포함해 self-contained English surface를 제공한다.
- `guide-create`의 compact template는 `.claude/`와 `.codex/` pair에서 semantic parity를 유지해야 한다.
- active spec sync는 docs/skill surface가 먼저 canonical model과 정렬된 뒤 `_sdd/spec/`에 지속 truth를 반영하는 순서를 따른다.

### Supporting spec files

| File | Role |
|------|------|
| [components.md](./components.md) | component reference + appendix-level strategic code map |
| [usage-guide.md](./usage-guide.md) | section 5를 뒷받침하는 scenario-oriented usage guide |
| [DECISION_LOG.md](./DECISION_LOG.md) | 구조 변경과 주요 spec 판단 이력 |
| [logs/changelog.md](./logs/changelog.md) | 릴리스/문서 변경 이력 |

### 유지보수 참고

- legacy uppercase path인 `DECISION_LOG.md`는 기존 링크와 이력을 보존하기 위해 유지한다.
- 신규 canonical backup 파일명은 `prev_<filename>_<timestamp>.md`를 사용한다.

## 부록 A. Strategic Code Map

| Type | Path | Why It Matters |
|------|------|----------------|
| Entrypoint | [`README.md`](../../README.md) | 설치, 플랫폼 차이, bundle 진입점을 가장 먼저 설명한다 |
| Entrypoint | [`docs/SDD_WORKFLOW.md`](../../docs/SDD_WORKFLOW.md) | current workflow semantics와 skill 역할 분담의 기준이다 |
| Invariant hotspot | [`docs/SDD_SPEC_DEFINITION.md`](../../docs/SDD_SPEC_DEFINITION.md) | global spec/temporary spec/CIV shape가 여기서 고정된다 |
| Change hotspot | [`_sdd/spec/main.md`](./main.md) | 글로벌 기준 문서라 supporting file 역할과 section responsibility가 여기서 결정된다 |
| Change hotspot | [`_sdd/spec/components.md`](./components.md) | skill/agent reference와 strategic code map이 유지된다 |
| Extension point | [`../../.claude/skills/`](../../.claude/skills/) | Claude user entrypoint를 추가하거나 wrapper/full skill을 확장하는 위치다 |
| Extension point | [`../../.codex/skills/`](../../.codex/skills/) | Codex user entrypoint와 runtime-specific skill contract를 확장하는 위치다 |
| Reusable execution hotspot | [`../../.claude/agents/`](../../.claude/agents/) | Claude reusable execution unit의 실제 동작이 모인다 |
| Reusable execution hotspot | [`../../.codex/agents/`](../../.codex/agents/) | Codex custom agent 정의와 spawn 대상이 모인다 |
| Runtime prerequisite | [`../../.codex/config.toml`](../../.codex/config.toml) | nested agent depth와 concurrency 전제를 고정한다 |
| Environment hotspot | [`../env.md`](../env.md) | pre-flight, PR verification, local editing assumptions를 요약한다 |

## 부록 B. 관련 문서 및 코드 레퍼런스

- [`README.md`](../../README.md)
- [`docs/sdd.md`](../../docs/sdd.md)
- [`docs/SDD_CONCEPT.md`](../../docs/SDD_CONCEPT.md)
- [`docs/SDD_WORKFLOW.md`](../../docs/SDD_WORKFLOW.md)
- [`docs/SDD_SPEC_DEFINITION.md`](../../docs/SDD_SPEC_DEFINITION.md)
- [`docs/AUTOPILOT_GUIDE.md`](../../docs/AUTOPILOT_GUIDE.md)
- [`docs/en/SDD_SPEC_DEFINITION.md`](../../docs/en/SDD_SPEC_DEFINITION.md)
- [`docs/en/SDD_WORKFLOW.md`](../../docs/en/SDD_WORKFLOW.md)
- [`docs/en/SDD_QUICK_START.md`](../../docs/en/SDD_QUICK_START.md)
- [`docs/en/SDD_CONCEPT.md`](../../docs/en/SDD_CONCEPT.md)
- [`docs/en/sdd.md`](../../docs/en/sdd.md)
- [`../../.claude/skills/guide-create/references/template-compact.md`](../../.claude/skills/guide-create/references/template-compact.md)
- [`../../.codex/skills/guide-create/references/template-compact.md`](../../.codex/skills/guide-create/references/template-compact.md)
- [`components.md`](./components.md)
- [`usage-guide.md`](./usage-guide.md)
- [`DECISION_LOG.md`](./DECISION_LOG.md)
- [`logs/changelog.md`](./logs/changelog.md)
