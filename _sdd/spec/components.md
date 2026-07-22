# Component Reference & Strategic Code Map

> 이 문서는 [main.md](./main.md)에서 분리된 reference-only supporting surface다.
> normative decision-bearing truth는 `main.md`에 두고, 여기에는 각 컴포넌트의 `Purpose / Why / Source`와 최소한의 navigation note만 남긴다.
> 상세 Input/Output/Process/완료 이력은 각 스킬 원문과 관련 artifact에서 확인한다.

---

## Orchestration & Spec Lifecycle

| Component | Purpose | Why | Primary Source | Notes |
|-----------|---------|-----|----------------|-------|
| `sdd-autopilot` | reasoning 기반으로 SDD 체인을 무승인으로 end-to-end 실행한다 | 수동 handoff와 단계 누락을 줄인다 | `.claude/skills/sdd-autopilot/SKILL.md`<br>`.codex/skills/sdd-autopilot/SKILL.md` | 풀 스킬(v3.0.0, SDD 체인 전용). Step 0 상태 확인(기존 draft 재활용·spec 유무) → Step 1 요청 분석 → Step 2: `feature-draft` → `plan-review`(단일 패스 경량 반환) → fix 1회 → `implementation` → `implementation-review`(경량 반환) → fix 1회 → `spec-sync` → 최종 응답 요약(report 파일 없음). orchestrator·pipeline artifact·승인 checkpoint 없음, 게이트당 fix 1회·re-review 없음. 규모 초과는 분할 규칙으로 처리하며 분할 판정 canonical은 체인 표면이 소유한다(autopilot은 신호 소비만). full 레인(generated orchestrator)은 제거됨(잔재 정리·census 완결) — 복구는 git tag `full-lane-final`, legacy `_sdd/pipeline/` 산출물은 기록물로 무시 |
| `spec-create` | 초기 global spec과 workspace guidance를 부트스트랩한다 | 스펙 부재 상태에서 workflow 시작점을 만들고, thin global 기본 구조를 고정한다 | `.claude/skills/spec-create/SKILL.md` | 워크플로우 시작점. 기본값은 `_sdd/spec/main.md` 단일 파일이며, 코드베이스가 있으면 primary navigation axis를 하나 고른다. 짧은 `Strategic Code Map`은 appendix로, 긴 map은 supporting surface로 둔다. 부트스트랩 산출물에 `.gitignore`(`SDD-WORKSPACE` 마커로 process artifact 4종 ignore)를 멱등 병합하고, `_sdd/env.md` 상단에 비밀값 금지 경고를 포함한다 |
| `feature-draft` | 단일 컨텍스트로 감당되는 변경의 기본 planning 경로 — coverage-index/validation ceremony 없이 task + Target Files + AC 중심 draft를 만든다 | 낮은 ceremony로 planning을 시작하는 SDD 체인 진입점을 제공한다 | `.claude/skills/feature-draft/SKILL.md`<br>`.codex/skills/feature-draft/SKILL.md` | 메인 루프 직접 작성(신규 agent 없음). v2.0.0에서 `feature-draft-lite`가 개명(F5). 분할 규칙의 canonical 소유자: coverage 눈검산 불가·단일 컨텍스트 초과면 롤링 분할(Part 1 마커에 분할 feature 목록 → `spec-sync` planned todo 고정, Part 2는 첫 feature task만)로 해소한다. census형 sweep은 분할 대상이 아니라 마지막 read-only 검증 task(변형 표기 전수 grep census AC)로 흡수한다. `> 규모 판정:` 리터럴이 plan-review 규모 판정 검사의 대조 앵커다 |
| `spec-sync` | 구현 전 planned persistent truth를 사전 반영하거나 구현 후 evidence를 검토해 검증된 지속 정보만 global spec에 올린다 (evidence에 맞춰 적응) | spec-code drift를 사전·사후로 줄이고, 임시 실행 메모와 검증된 truth를 분리한다 | `.claude/agents/spec-sync-agent.md`<br>`.claude/skills/spec-sync/SKILL.md` | wrapper -> agent 패턴. planned touchpoint를 통째로 복사하지 않고 장기 navigation value가 있는 code map 후보만 보수적으로 다룬다. 구현 후에는 delta status 분류 기반 sync로 lowercase canonical artifact를 우선 읽고 verified persistent `Strategic Code Map` 변화만 승격한다. 입력 draft는 현행 draft 구조(Part 1 마커 + task별 AC) 기준이며, full draft 구조(coverage index·`Covered By` 등)는 legacy 기록물 fallback으로만 읽는다 |
| `spec-review` | 스펙 품질과 코드-스펙 drift를 read-only로 진단한다 | 수정 없이 현재 상태를 객관적으로 점검하고, global/temporary rubric을 섞어 오탐하는 것을 줄인다 | `.claude/skills/spec-review/SKILL.md`<br>`.codex/skills/spec-review/SKILL.md` | 직접 실행 skill — 리뷰 계약·프로세스·rubric·리포트 형식(`_sdd/spec/logs/spec_review_report.md`)·review-only 불변식의 단일 소스는 SKILL.md 본문이다(더 이상 wrapper→agent 2홉 아님). rubric separation, evidence strictness, code map freshness를 기준으로 본다. 감사 기준은 현행 draft 구조이며, full draft 구조 검사(coverage index 고아 delta·`Touchpoints` census)는 legacy 기록물을 감사할 때만 적용한다 |
| `spec-rewrite` | 비대한 스펙을 canonical-fit 기준으로 재구성한다 | global/spec surface의 구조적 오염을 줄이되 판단 근거를 잃지 않는다 | `.claude/skills/spec-rewrite/SKILL.md`<br>`.codex/skills/spec-rewrite/SKILL.md` | 계획 파일과 rewrite report를 먼저/함께 남긴다. body에는 최소 rationale만 남기고 정리 메모는 log/report로 내린다 |
| `spec-summary` | global spec, supporting surface, 필요한 code grounding을 엮어 reader-facing whitepaper를 작성한다 | 문제, 동기, 핵심 설계, 코드 근거, 사용/기대 결과를 한 문서에서 이해하게 한다 | `.claude/skills/spec-summary/SKILL.md` | `_sdd/spec/summary.md` 생성용. 관련 draft/implementation artifact가 있으면 planned/progress 신호를 appendix에만 짧게 덧붙일 수 있다 |
| `spec-upgrade` | legacy global spec을 current canonical model로 마이그레이션한다 | 오래된 section-map과 inventory-heavy 구조를 정리하되, rewrite가 필요한 구조 재편은 분리한다 | `.claude/skills/spec-upgrade/SKILL.md`<br>`.codex/skills/spec-upgrade/SKILL.md` | 구조 업그레이드 전용. 시작 시 rewrite boundary를 먼저 판정한다 |
| `guide-create` | 특정 기능의 구현/리뷰용 deep-dive guide를 생성한다 | thin global spec 밖의 세부 설명 surface가 필요하다 | `.claude/skills/guide-create/SKILL.md`<br>`.codex/skills/guide-create/SKILL.md` | compact template pair를 같이 확인한다 |

## Delivery & Review

| Component | Purpose | Why | Primary Source | Notes |
|-----------|---------|-----|----------------|-------|
| `plan-review` | 구현 전 계획을 findings-first로 감사한다 | 과잉 설계, 불필요한 새 파일, 약한 검증 기준이 구현으로 전파되기 전에 드러낸다 | `.claude/agents/plan-review-agent.md`<br>`.claude/skills/plan-review/SKILL.md`<br>`.codex/agents/plan-review-agent.toml`<br>`.codex/skills/plan-review/SKILL.md` | wrapper -> agent. read-only reviewer — feature draft를 단일 패스로 리뷰하고 경량 반환으로만 응답한다(리포트 파일·re-review 없음, tools에 Write 없음). rubric은 AC falsifiability·Target Files 실측·task boundary·6-smell·규모 판정 검사(분할 권고 포함)이며 Critical/High finding은 implementation blocker로 표시한다. finding 반영은 호출자 fix 1회, 리뷰 대상 draft가 없으면 안내 1줄만 반환한다 |
| `implementation` | task set(주로 feature draft)을 메인 루프가 직접 RED→GREEN test-first로 구현한다 — 유일 구현 실행 경로 | 소규모 구현에서 leaf dispatch 오버헤드 없이 test-first 규율을 유지한다 | `.claude/skills/implementation/SKILL.md`<br>`.codex/skills/implementation/SKILL.md` | 작성자 불변식: 코드·테스트는 메인 루프가 직접 작성하고 read-only 보조 agent만 허용한다. v2.0.0에서 `implementation-lite`가 개명(F5). 일반 구현 요청 트리거("implement the plan"·"start implementation"·"execute the plan"·"구현해줘" 계열)의 유일 수신 경로이며 "병렬 구현" 계열은 폐기됐다. 중단·분할 규칙의 canonical 소유자: 단일 세션 초과면 완료 가능한 범위까지 마감하고 잔여를 분할 feature로 draft Part 1 마커 반영 + `spec-sync` planned todo 고정, 계약 오류 선언이 같은 task에서 반복되면 구현 중단 + draft 복귀다 |
| `implementation-review` | 구현 결과를 계획/AC 기준으로 다시 검증한다 | 누락과 품질 이탈을 조기에 드러낸다 | `.claude/agents/implementation-review-agent.md`<br>`.claude/skills/implementation-review/SKILL.md` | wrapper -> agent. fresh verification 중시. 단일 패스 경량 반환 유일(리포트 파일·re-review 없음, tools에 Write 없음 — 테스트 실행용 Bash만). 대화에서 태어나는 입력은 wrapper가 digest로 정리해 forwarding한다 |
| `pr-review` | PR 코드 품질과 spec 준수 여부를 함께 판정한다 | 코드 리뷰와 spec 기반 검증을 한 surface로 묶는다 | `.claude/skills/pr-review/SKILL.md`<br>`.claude/agents/pr-review-agent.md`<br>`.codex/skills/pr-review/SKILL.md`<br>`.codex/agents/pr-review-agent.toml` | orchestrator(skill) + 직교 2-렌즈 병렬 dispatch. correctness(`pr-review-agent`) ∥ simplicity(`simplicity-review-agent`) 두 read-only leaf가 경량 반환(finding별 위치·문제·수정 제안)으로 응답하고, skill이 verdict 합성 + 통합 리포트(`_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`) 1파일만 작성한다. correctness가 inline이 아닌 agent라 `--model` override가 두 렌즈에 균일 적용. findings-first, spec 존재 시 spec-based 추가 검증 |
| `investigate` | 범용 근본원인 분석과 수정/검증을 수행한다 | 임의 수정 반복 대신 root-cause-first 디버깅을 강제한다 | `.claude/skills/investigate/SKILL.md`<br>`.codex/skills/investigate/SKILL.md` | orchestrator(skill). 탐색이 넓고·모호할 때만 빌트인 범용 read-only explore 역할(claude `Explore`, codex `spawn_agent(agent_type="explorer")`)을 병렬 fan-out하고, fix·검증·종합은 인라인 소유한다. custom investigate-agent는 제거됨. blast radius와 fresh verification 포함 |

## Discussion & Utilities

| Component | Purpose | Why | Primary Source | Notes |
|-----------|---------|-----|----------------|-------|
| `discussion` | 구조화된 의사결정 토론을 진행한다 | 설계 선택과 open question을 추적 가능하게 만든다 | `.claude/skills/discussion/SKILL.md`<br>`.codex/skills/discussion/SKILL.md` | 풀 스킬. 양 플랫폼 모두 대화형 입력 사용. 결과는 `_sdd/discussion/<YYYY-MM-DD>_discussion_<slug>.md`에 저장한다 |
| `goal-init` | 네이티브 `/goal` 루프에 걸 자족적 조건 문자열과 4파일 실행 하네스를 한 번의 대화로 셋업한다 | `/goal`을 잘 쓰려면 평가자 자족 완료조건·발산 메커니즘·검증 surface·회고가 필요한데 수동 셋업이 어렵다 | `.claude/skills/goal-init/SKILL.md`<br>`.codex/skills/goal-init/SKILL.md` | discussion식 대화형 단일 스킬(신규 agent 없음). 실행 시 `_sdd/goal/<YYYY-MM-DD>_<slug>/`에 4파일(`goal.md`/`experiments.md`/`journal.md`/`report.md`)을 생성하고 사용자가 검토 후 직접 걸 조건 문자열을 제시한다(스킬은 `/goal`을 직접 발동하지 않음). 조건 완료부(`DONE WHEN`/`CONSTRAINTS`/`STOP`)는 도구 없이 transcript만으로 판정 가능·4,000자 이하이고 루프 행동(HOW)은 `goal.md`의 `Loop Protocol`로 분리한다. 조건 본문은 런타임 독립, 실행법만 각 스킬이 자기 런타임 것을 기재. 하네스에 bash 루프·`run.sh`·state머신·컨테이너는 없다(`/goal` 네이티브 턴 루프 스코프). ralph-loop 대체는 deferred |
| `ralph-loop-init` | 장기 실행 프로세스용 자동화 디버그 루프를 만든다 | 반복 실험/테스트 환경을 표준화한다 | `.claude/skills/ralph-loop-init/SKILL.md`<br>`.codex/skills/ralph-loop-init/SKILL.md` | 직접 실행 skill — discovery·상태 머신·5파일 생성·run.sh 템플릿·CHECKS 자체검증의 단일 소스는 SKILL.md 본문이다(더 이상 wrapper→agent 2홉 아님). Step 2 검증 방법 확정 사용자 확인 게이트를 메인 루프가 직접 수행한다(subagent는 실행 중 대화 불가라 skill 전환으로 비로소 작동). codex는 run.sh LLM 호출·Security Notice의 CLI flag delta(`--dangerously-bypass-approvals-and-sandbox`)를 보존한다 |
| `git` | 변경을 의미 단위로 정리해 커밋/브랜치 작업을 돕는다 | AI가 만든 변경을 의도 단위로 정리해야 한다 | `.claude/skills/git/SKILL.md` | Claude Code 전용 |
| `spec-snapshot` | 스펙 상태를 타임스탬프 스냅샷으로 보존한다 | 원본을 건드리지 않고 특정 시점 상태나 번역본을 관리한다 | `.claude/skills/spec-snapshot/SKILL.md`<br>`.codex/skills/spec-snapshot/SKILL.md` | snapshot/export 성격 |
| `second-opinion` | 관련 맥락을 모아 Codex의 독립 분석을 요청한다 | 단일 에이전트 관점 편향을 줄인다 | `.claude/skills/second-opinion/SKILL.md` | Claude Code 전용, read-only |

## Platform Notes

| Surface | What To Remember | Source |
|---------|------------------|--------|
| Claude skill/agent split | leaf dispatch가 필요한 skill은 orchestrator(skill) + leaf(agent)로 둔다 — `pr-review`(correctness ∥ simplicity 2-렌즈 병렬), `investigate`(조건부 explore fan-out). dispatch가 필요 없는 skill은 메인 루프가 직접 실행하고 SKILL.md가 전체 계약을 단일 소스로 보유한다 — 구현·planning(`implementation`·`feature-draft`)에 더해 스탠드얼론 reviewer/generator(`spec-review`·`ralph-loop-init`)도 직접 실행 skill이다. 잔존 wrapper-backed skill(thin wrapper + single-source agent)은 `plan-review`·`implementation-review`·`spec-sync`이다 | `.claude/skills/`, `.claude/agents/` |
| Codex custom agent runtime | Codex는 `.codex/agents/`의 custom agent를 parent orchestrator가 직접 dispatch한다. agent는 leaf로 동작하며 사용자 전역 config 값을 workflow 전제로 삼지 않는다 | `.codex/agents/` |
| Artifact path convention | 신규 temporary artifact는 lowercase canonical 경로를 기본으로 하고, skill-defined output surface는 dated slug naming을 사용한다. reader는 legacy uppercase/fixed-name path를 fallback으로 읽는다 | 관련 `SKILL.md`, `_sdd/implementation/implementation_progress.md` |
| Workspace commit 정책 (소비 repo) | 소비 repo에서 커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`·`drafts/`·`work_log/`이고(`drafts/`·`work_log/`는 구현 로그 자산), 나머지 process artifact 4종(`_sdd/{discussion,implementation,pipeline,pr}/`)은 `.gitignore`로 로컬 전용이다. `_sdd/env.md`는 커밋되므로 비밀값 금지. 이 sdd_skills repo는 스킬 개발 메타 repo라 process artifact를 history 가치로 계속 커밋하는 예외다 | `.claude/skills/spec-create/SKILL.md` 3d, `.claude/skills/spec-upgrade/SKILL.md` Step 6 |
| Full-skill exceptions | `sdd-autopilot`, `discussion`처럼 사용자 상호작용이 핵심인 surface는 풀 스킬로 유지된다 | 관련 `SKILL.md` |
| Platform-only features | `git`, `second-opinion`은 Claude Code 전용이며, Codex parity 대상이 아니다 | 관련 `SKILL.md` |

---

## Appendix A. Strategic Code Map

전수형 파일 inventory 대신, 변경 시 먼저 봐야 할 navigation-critical path만 남긴다.

| Type | Path | Why Start Here |
|------|------|----------------|
| Canonical model | `docs/SDD_SPEC_DEFINITION.md` | global spec과 temporary spec의 shape를 고정한다 |
| Workflow contract | `docs/SDD_WORKFLOW.md` | 스킬 역할, update order, artifact 배치를 가장 빠르게 확인할 수 있다 |
| Thin global spec | `_sdd/spec/main.md` | repo-wide decision-bearing truth와 supporting surface 책임이 여기서 정해진다 |
| Component reference | `_sdd/spec/components.md` | 개별 컴포넌트의 compact reference를 모아 둔다 |
| Usage scenarios | `_sdd/spec/usage-guide.md` | 실제 사용 흐름과 expected result를 빠르게 확인한다 |
| Claude orchestration hotspot | `.claude/skills/sdd-autopilot/SKILL.md` | SDD 체인 실행 semantics와 hard rules가 모인다 |
| Codex orchestration hotspot | `.codex/skills/sdd-autopilot/SKILL.md` | 동일 체인의 Codex runtime 적응이 모인다 |
| Claude reusable execution | `.claude/agents/` | wrapper-backed skill의 single-source agent 본문을 찾는 위치다 |
| Implementation contract | `.claude/skills/implementation/SKILL.md`<br>`.codex/skills/implementation/SKILL.md` | 메인 루프 직접 test-first의 canonical surface — (a)/(b)/(c) triage, RED 관찰 전 구현 금지, 테스트 불변 규칙, 중단·분할 규칙, AC→증거 테이블 마감이 여기서 정의된다 |
| Codex reusable execution | `.codex/agents/` | custom agent spawn 대상과 parity 확인 지점이다 |
| Codex bundle installer | `tools/install-codex-skill-bundle.py` | skills와 agents만 설치하며 사용자 `~/.codex/config.toml`은 수정하지 않는다 |
| Environment/pre-flight | `_sdd/env.md` | 로컬 작업, PR verification, pre-flight assumption의 기준이다 |
| Spec creation contract | `.claude/skills/spec-create/SKILL.md`<br>`.codex/skills/spec-create/SKILL.md` | primary navigation axis와 `Strategic Code Map` placement rule을 확인한다 |
| Harness layer template | `.claude/skills/spec-create/references/agents-harness-template.md` | `AGENTS.md` 작업 진입·작업 규약 레이어의 정본 §0~§5 골격(§5 = on-demand work log 규약). 4곳(`spec-create`/`spec-upgrade` × `.claude`/`.codex`) byte-identical 미러의 source다 |
| Feature planning map consumer | `.claude/skills/feature-draft/SKILL.md`<br>`.codex/skills/feature-draft/SKILL.md` | code map을 hint로 읽되 `Target Files`를 현재 코드 실측으로만 적는 규칙과 분할·census 규칙을 확인한다 |
| Spec sync map promotion | `.claude/agents/spec-sync-agent.md`<br>`.codex/agents/spec-sync-agent.toml` | temporary touchpoint 중 어떤 항목이 persistent navigation hint로 승격될 수 있는지 확인한다 |
