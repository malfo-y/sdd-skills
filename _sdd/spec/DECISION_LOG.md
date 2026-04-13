# Decision Log

## 2026-04-13 - Position spec-summary as reader-facing whitepaper surface (v4.1.6 -> v4.1.7 spec revision)

### Context

`spec-summary`는 `_sdd/spec/summary.md`를 만드는 surface이지만, active `_sdd/spec/` supporting docs에는 여전히 canonical overview 중심 설명이 남아 있었다. 이 표현은 현재 skill/docs 쪽에서 이미 정렬된 whitepaper contract와 어긋난다. 이 저장소에서 `summary.md`는 thin global spec을 다시 두껍게 복제하는 문서가 아니라, 문제의식과 배경/동기, 핵심 설계, 코드 근거, 사용 흐름과 기대 결과를 사람이 한 문서로 읽게 하는 reader-facing whitepaper여야 한다.

### Decision

1. **`spec-summary`를 whitepaper surface로 고정**: `_sdd/spec/summary.md`는 repo/spec를 설명하는 reader-facing whitepaper로 본다.
2. **필수 section spine 고정**: `Executive Summary`, `Background / Motivation`, `Core Design`, `Code Grounding`, `Usage / Expected Results`, `Further Reading / References`를 기본 본문 구조로 사용한다.
3. **`Code Grounding` 필수화**: summary는 concrete path, symbol, source table 같은 anchor로 설명을 실제 구현과 연결해야 한다.
4. **planned/progress는 appendix로만 허용**: 관련 draft/implementation artifact가 있을 때만 마지막 보조 섹션으로 짧게 붙인다.
5. **history narration 분리 유지**: summary surface 자체는 현재 기준 내용만 직접 설명하고, 과거 판단과 변경 이력은 `DECISION_LOG.md`와 `logs/changelog.md`에서 추적한다.

### Rationale

- `summary.md`의 핵심 가치는 "빠른 상태표"보다 "왜 이런 구조인지와 실제 근거가 무엇인지"를 이해시키는 데 있다.
- global spec이 thin core를 유지하더라도, 사람은 배경/동기/설계/사용 서사를 한 문서에서 읽을 whitepaper surface가 필요하다.
- `Code Grounding`이 없는 whitepaper는 일반 소개문으로 무너지기 쉽고, 반대로 appendix-only planned/progress rule이 없으면 본문이 다시 status memo로 오염된다.
- history narration을 summary 본문에서 분리하면 summary surface는 설명 문서로 남고, history surface는 change-tracking 역할에 집중할 수 있다.

### Changes

- `_sdd/spec/components.md` -- `spec-summary`를 reader-facing whitepaper surface로 설명
- `_sdd/spec/usage-guide.md` -- `/spec-summary` expected result를 whitepaper section spine으로 정렬
- `_sdd/spec/logs/changelog.md` -- v4.1.7 이력 추가

### References

- feature draft: `_sdd/drafts/2026-04-13_feature_draft_spec_summary_whitepaper_surface.md`
- implementation progress: `_sdd/implementation/2026-04-13_implementation_progress_spec_summary_whitepaper_surface.md`
- implementation report: `_sdd/implementation/2026-04-13_implementation_report_spec_summary_whitepaper_surface.md`
- implementation review: `_sdd/implementation/2026-04-13_implementation_review_spec_summary_whitepaper_surface.md`
- orchestrator: `_sdd/pipeline/orchestrators/orchestrator_spec_summary_whitepaper_surface.md`

## 2026-04-13 - Reframe spec-summary as canonical overview with optional planned/progress snapshot (v4.1.5 -> v4.1.6 spec revision)

### Context

`spec-summary`는 이미 `_sdd/spec/summary.md`를 만드는 human-readable summary surface였지만, active skill contract와 supporting docs에는 여전히 "현재 스펙 상태"와 `global/temporary spec 요약` 관점이 남아 있었다. 이 표현은 `summary.md`를 사람용 canonical overview로 보려는 현재 thin global 철학과 맞물릴 때 역할이 흐려졌다. global spec은 장기적 판단 기준을 고정하고, 세부 설명은 supporting surface로 내리는 방향인데, `summary.md`가 다시 status sheet나 temporary summary처럼 읽히면 목적/경계/핵심 결정/다음 surface를 빠르게 잡아주는 역할이 약해진다.

### Decision

1. **`spec-summary`의 1차 역할을 canonical overview로 고정**: `_sdd/spec/summary.md`는 global spec과 supporting surface를 읽는 사람에게 목적, 경계, 핵심 결정, 다음에 읽을 surface를 빠르게 전달하는 문서로 본다.
2. **temporary summary 독립 모드는 제거**: `spec-summary`는 temporary spec 자체를 별도 summary mode로 다루지 않는다.
3. **planned/progress snapshot은 보조 정보로만 허용**: 관련 `_sdd/drafts/` 또는 `_sdd/implementation/` artifact가 있을 때만 `Planned / In Progress / Blocked / Next` 수준의 짧은 snapshot을 뒤쪽에 덧붙인다.
4. **navigation naming 고정**: summary의 navigation 섹션 명칭은 `Where Details Live`를 사용한다.
5. **history narration 금지**: `spec-summary` 본문과 template/example은 migration memo처럼 과거와 현재를 비교하지 않고, 현재 기준의 계약과 output shape만 직접 서술한다.
6. **history docs는 역할 분리 유지**: semantic shift의 판단 근거는 `DECISION_LOG.md`, 변경 파일/버전 이력은 `logs/changelog.md`에 남긴다.

### Rationale

- 사람이 `summary.md`에서 얻어야 할 가치는 "상태 표"보다 "이 repo를 어떤 기준으로 읽고 어디를 더 보면 되는가"에 가깝다.
- temporary spec은 실행 청사진이라 draft/implementation artifact 자체가 주 문맥이므로, `spec-summary`가 이를 다시 독립 summary surface로 복제할 이유가 약하다.
- optional planned/progress snapshot만 남기면 overview의 선명함을 유지하면서도 현재 진행 상태를 빠르게 붙일 수 있다.
- `Where Details Live`는 `How to Read This Spec`보다 덜 메타적이고, `Reading Map`보다 직관적으로 다음 탐색 경로를 설명한다.
- `spec-summary` 본문에 변경 이력 서술을 넣지 않고 final form만 남기면 summary surface 자체가 다시 history-heavy 문서로 오염되는 것을 막을 수 있다.

### Changes

- `.codex/skills/spec-summary/SKILL.md` -- canonical overview + optional planned/progress snapshot 계약으로 재작성
- `.claude/skills/spec-summary/SKILL.md` -- mirror contract 동기화
- `.codex/skills/spec-summary/skill.json` -- version/description를 `2.0.0` semantics로 정렬
- `.claude/skills/spec-summary/skill.json` -- version/description를 `2.0.0` semantics로 정렬
- `.codex/skills/spec-summary/references/summary-template.md` -- `Where Details Live` + optional snapshot 구조로 재배치
- `.claude/skills/spec-summary/references/summary-template.md` -- mirror template sync
- `.codex/skills/spec-summary/examples/summary-output.md` -- overview-first example로 갱신
- `.claude/skills/spec-summary/examples/summary-output.md` -- mirror example sync
- `_sdd/spec/components.md` -- `spec-summary` 목적/이유/notes를 canonical overview 기준으로 보정
- `_sdd/spec/usage-guide.md` -- `/spec-summary` expected result를 overview-first wording으로 보정
- `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md` -- `spec-summary` semantics 보정
- `docs/en/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_WORKFLOW.md` -- 영문 mirror sync
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- downstream taxonomy 보정
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- downstream taxonomy 보정
- `_sdd/spec/logs/changelog.md` -- v4.1.6 이력 추가

### References

- 구현 draft: `_sdd/drafts/2026-04-13_feature_draft_spec_summary_canonical_overview_alignment.md`
- implementation review: `_sdd/implementation/2026-04-13_implementation_review_spec_summary_canonical_overview_alignment.md`
- orchestrator: `_sdd/pipeline/orchestrators/orchestrator_spec_summary_canonical_overview_alignment.md`

## 2026-04-10 - Sync autopilot planning semantics and artifact naming invariants into global spec (v4.1.4 -> v4.1.5 spec revision)

### Context

2026-04-10 커밋들에서 `sdd-autopilot`, `implementation-plan`, `discussion`, `spec-update-done` 주변 계약이 크게 정리됐다. non-trivial change의 기본 planning entry를 `feature-draft`로 고정하고, `implementation-plan`을 후속 확장 단계로 재정의했으며, multi-phase plan은 실제 execution gate로 소비되어 `per-phase` review-fix와 `final integration review`를 강제하게 됐다. 동시에 skill-defined output artifact naming은 date-prefixed slug 규칙으로 정렬되고, `prev/` 백업 체인 대신 append-only artifact + git history를 기본 추적 방식으로 사용하는 방향이 굳어졌다.

하지만 active `_sdd/spec/` surface에는 이 운영 규칙들이 아직 직접 반영되지 않아, `_sdd/spec/usage-guide.md`에는 여전히 오래된 autopilot 실행 경로와 단순화된 planning path가 남아 있었고, global main body에도 새 artifact naming / phase gate semantics가 빠져 있었다.

### Decision

1. **planning precedence를 global rule로 승격**: non-trivial change의 기본 planning entry는 `feature-draft`이며, `implementation-plan`은 Part 2만으로 부족하거나 phase/task 세분화가 필요할 때만 붙는 후속 확장 단계로 정리한다.
2. **multi-phase plan을 execution gate로 고정**: multi-phase plan이 생성되면 `per-phase` review-fix와 phase exit 검증, 마지막 `final integration review`를 repo-wide 운영 규칙으로 본다.
3. **artifact naming/history invariant 명시**: 신규 temporary artifact는 lowercase canonical 경로를 기본으로 사용하고, skill-defined output surface는 dated slug 경로를 따른다. `prev/` 백업 체인 대신 append-only artifact + git history를 기본 추적 방식으로 삼는다.
4. **reader fallback 원칙 유지**: skill/agent reader는 legacy uppercase/fixed-name artifact를 fallback으로 읽을 수 있어야 한다.
5. **autopilot authoritative path 정렬**: 실행 중 활성 오케스트레이터의 기준 경로는 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`로 본다.

### Rationale

- planning precedence가 global spec에 없으면 `feature-draft`와 `implementation-plan`이 다시 peer choice처럼 해석돼 pipeline selection이 흔들린다.
- multi-phase plan을 단순 문서로 두면 phase boundary에서 defect containment가 무너지고 review-fix loop가 늦게 작동한다.
- skill-defined output surface의 dated slug naming은 여러 skill이 공통으로 사용하는 경로 추론 규칙이라, global spec 차원에서 묶어야 repo-level reasoning과 review 판단이 일관된다.
- `prev/` 백업 체인을 canonical rule로 남겨 두면 실제 skill contract와 global spec이 다시 drift한다.
- active orchestrator 경로가 global usage surface와 실제 guide 문서에서 다르면 autopilot 재개/검증 흐름을 잘못 이해하게 된다.

### Changes

- `_sdd/spec/main.md` -- planning precedence, phase-gated execution, artifact naming/history invariant, mirror sync 운영 제약 반영
- `_sdd/spec/components.md` -- `sdd-autopilot`, `implementation-plan`, `spec-update-done`, `discussion`, platform artifact-path note 보강
- `_sdd/spec/usage-guide.md` -- manual/autopilot scenario를 optional expansion + per-phase gate semantics로 정렬, active orchestrator 경로 수정
- `_sdd/spec/logs/changelog.md` -- v4.1.5 이력 추가

### References

- 구현 draft: `_sdd/drafts/2026-04-10_feature_draft_autopilot_planning_phase_gates.md`
- implementation review: `_sdd/implementation/2026-04-10_implementation_review_autopilot_planning_phase_gates.md`
- implementation report: `_sdd/implementation/2026-04-10_implementation_report_autopilot_planning_phase_gates.md`
- review fix report: `_sdd/implementation/2026-04-10_implementation_report_autopilot_planning_phase_gates_review_fixes.md`
- commits: `ee4e1cd`, `d32686a`, `aa92c83`, `0725c25`

## 2026-04-04 - Compact components reference surface (v4.1.0 -> v4.1.1 spec revision)

### Context

`_sdd/spec/components.md`는 이미 `main.md`에서 분리된 supporting surface였지만, 각 컴포넌트마다 Input/Output/Process/Dependencies/완료 이력을 길게 재서술하면서 reference 문서라기보다 mini-spec catalog에 가까워져 있었다. global main body를 얇게 줄인 뒤에도 `components.md`가 너무 두꺼우면, 결국 active spec surface 전체의 탐색 비용이 다시 커진다.

### Decision

1. **`components.md`를 compact reference catalog로 재작성**: 카테고리별 table에서 각 컴포넌트의 `Purpose / Why / Primary Source / Notes`만 유지
2. **runtime 차이는 최소 note로만 보존**: wrapper -> agent, full skill, Claude-only 같은 탐색용 차이만 남김
3. **상세 재복제 제거**: Input/Output/Process/Dependencies/완료 이력은 각 `SKILL.md`, agent 정의, 관련 artifact에서 찾도록 정리
4. **strategic code map 유지**: 전수형 inventory 대신 navigation-critical path appendix는 계속 유지

### Rationale

- supporting surface는 main의 decision-bearing truth를 보조해야지, 또 다른 두꺼운 본문이 되면 안 된다
- 컴포넌트별로 truly reference value가 높은 것은 `무엇을 하는가`, `왜 필요한가`, `어디를 먼저 봐야 하는가`다
- 세부 step과 artifact shape는 원문 skill 문서가 authoritative source이므로, `components.md`에서 다시 길게 복제할 이유가 약하다
- compact catalog는 신규 사용자와 유지보수자 모두에게 탐색 속도를 높여 준다

### Changes

- `_sdd/spec/main.md` -- v4.1.1로 version bump
- `_sdd/spec/components.md` -- 284줄 -> 71줄 compact catalog로 재작성
- `_sdd/spec/logs/spec-rewrite-plan.md` -- components compact rewrite addendum 추가
- `_sdd/spec/logs/rewrite_report.md` -- 2차 리라이트 결과 반영
- `_sdd/spec/logs/changelog.md` -- v4.1.1 이력 추가
- `_sdd/spec/prev/prev_components_20260404_130827.md` -- 백업
- `_sdd/spec/prev/prev_spec-rewrite-plan_20260404_130827.md` -- 백업
- `_sdd/spec/prev/prev_rewrite_report_20260404_130827.md` -- 백업
- `_sdd/spec/prev/prev_DECISION_LOG_20260404_130827.md` -- 백업
- `_sdd/spec/prev/prev_changelog_20260404_130827.md` -- 백업

### References

- 리라이트 계획: `_sdd/spec/logs/spec-rewrite-plan.md`
- 리라이트 결과: `_sdd/spec/logs/rewrite_report.md`
- component source surface: `.claude/skills/`, `.claude/agents/`, `.codex/skills/`, `.codex/agents/`

## 2026-04-04 - Rewrite global spec to thin mandatory core (v4.0.1 -> v4.1.0 spec revision)

### Context

`_sdd/spec/main.md`는 이미 current canonical model을 반영한 상태였지만, global main body가 다시 두꺼워진 상태였다. standalone `Contract / Invariants / Verifiability` 표, usage summary, decision-bearing structure 대형 표, reference/code-map appendix가 한 문서 안에 함께 들어오면서, definition 문서가 말하는 `개념 + 경계 + 결정` 중심의 thin global core보다 넓은 책임을 다시 떠안고 있었다.

### Decision

1. **`main.md`를 3개 mandatory core 중심으로 재압축**: `Background`, `Scope / Non-goals / Guardrails`, `Core Design and Key Decisions`만 numbered main body로 유지
2. **repo-wide invariant는 별도 CIV 표 대신 guardrails/key decisions에 흡수**: global spec에 남아야 할 운영 규칙만 문장형으로 유지
3. **usage/reference/detail surface는 supporting file로 명시적 하향**: `components.md`, `usage-guide.md`, `DECISION_LOG.md`, `logs/changelog.md`를 thin main 바깥의 supporting surface로 재정의
4. **supporting file 도입부 정합성 보정**: 더 이상 존재하지 않는 `§5`, `§7`, appendix 참조를 제거
5. **backup rule 유지**: rewrite 전 `prev_main_20260404_130259.md`, `prev_components_20260404_130259.md`, `prev_usage-guide_20260404_130259.md`, `prev_DECISION_LOG_20260404_130259.md`를 생성

### Rationale

- `docs/SDD_SPEC_DEFINITION.md`는 global spec의 mandatory core를 3개 섹션으로 제한하고, usage/reference/CIV/code-map을 기본 코어 밖 surface로 내리라고 정의한다
- `docs/SDD_WORKFLOW.md` 역시 global spec은 모든 detail의 저장소가 아니라고 못 박고, feature/task/validation detail은 temporary 또는 supporting surface에서 다루도록 정리한다
- 현재 저장소에서 truly repo-wide한 판단은 이미 충분히 정리돼 있으므로, 새 내용을 추가하는 것보다 main responsibility를 줄이는 편이 canonical fit에 더 가깝다
- 구조 판단을 잃지 않으면서도 main token cost를 줄이면 사람과 AI 모두 기준 문서를 더 빠르게 읽을 수 있다

### Changes

- `_sdd/spec/main.md` -- v4.1.0 thin global spec으로 재작성 (257줄 -> 111줄)
- `_sdd/spec/components.md` -- supporting surface 역할 문구 보정
- `_sdd/spec/usage-guide.md` -- supporting surface 역할 문구 보정
- `_sdd/spec/logs/spec-rewrite-plan.md` -- thin rewrite 계획 갱신
- `_sdd/spec/logs/rewrite_report.md` -- 실행 결과 기록
- `_sdd/spec/logs/changelog.md` -- v4.1.0 이력 추가
- `_sdd/spec/prev/prev_main_20260404_130259.md` -- 백업
- `_sdd/spec/prev/prev_components_20260404_130259.md` -- 백업
- `_sdd/spec/prev/prev_usage-guide_20260404_130259.md` -- 백업
- `_sdd/spec/prev/prev_DECISION_LOG_20260404_130259.md` -- 백업

### References

- 정의 문서: `docs/SDD_SPEC_DEFINITION.md`
- 워크플로우 문서: `docs/SDD_WORKFLOW.md`
- 리라이트 계획: `_sdd/spec/logs/spec-rewrite-plan.md`
- 리라이트 결과: `_sdd/spec/logs/rewrite_report.md`

## 2026-04-04 - Upgrade global spec to current canonical SDD model (v3.9.1 -> v4.0.0 spec revision)

### Context

`_sdd/spec/main.md`는 이미 멀티파일 구조로 분리돼 있었지만, 본문 구조가 여전히 `Background / Core Design / Architecture / Component Details / Usage Guide` 중심의 legacy section map에 가까웠다. 특히 current canonical model이 요구하는 `Scope / Non-goals / Guardrails`, `Contract / Invariants / Verifiability`, `Decision-bearing structure`가 독립 section으로 고정돼 있지 않았고, component inventory와 code reference index가 본문/부록에서 과도하게 큰 비중을 차지했다.

### Decision

1. **`main.md`를 canonical global spec으로 재구성**: section 1~7과 appendix 구조를 current SDD spec definition에 맞춰 재배치
2. **CIV 명시 복구**: `Contract`, `Invariants`, `Verifiability`를 독립 표 구조로 추가하고, `_sdd/` artifact contract, wrapper/agent split, autopilot verification semantics를 연결
3. **Decision-bearing structure 분리**: 시스템 경계, ownership, cross-component contract, extension point, invariant hotspot을 별도 section으로 승격
4. **supporting file 역할 재정의**: `components.md`는 reference-only supporting file로 유지하고, 전수형 code reference index는 strategic code map으로 축약
5. **usage guide 정렬**: `usage-guide.md`를 section 5 보조 문서로 명시하고 expected result를 current canonical model 기준으로 보정
6. **legacy path 보존**: `DECISION_LOG.md` uppercase 경로는 기존 링크와 이력 보존을 위해 유지

### Rationale

- current canonical model은 global spec을 thin decision document로 유지하고 inventory-heavy detail을 supporting reference로 내릴 것을 요구한다
- 이 저장소는 코드보다 skill contract와 docs alignment가 핵심이므로, explicit CIV와 decision-bearing structure가 없으면 `spec-review`, `spec-update-*`, `sdd-autopilot` semantics가 다시 암묵화된다
- 멀티파일 구조 자체는 이미 충분히 유효하므로, 이번 작업은 `spec-rewrite`가 아니라 in-place `spec-upgrade`가 적절했다
- exhaustive code/file listing은 appendix-level strategic navigation hint로 축소하는 편이 current SDD definition과 더 잘 맞는다

### Changes

- `_sdd/spec/main.md` -- current canonical global spec structure로 전면 재작성
- `_sdd/spec/components.md` -- reference-only 역할 명시, `spec-upgrade` 설명 갱신, strategic code map으로 축약
- `_sdd/spec/usage-guide.md` -- section 5 보조 문서 역할과 expected result 정렬
- `_sdd/spec/prev/prev_main_20260404_015836.md` -- 백업
- `_sdd/spec/prev/prev_components_20260404_015836.md` -- 백업
- `_sdd/spec/prev/prev_usage-guide_20260404_015836.md` -- 백업
- `_sdd/spec/prev/prev_DECISION_LOG_20260404_015836.md` -- 백업

### References

- 정의 문서: `docs/SDD_SPEC_DEFINITION.md`
- 워크플로우 문서: `docs/SDD_WORKFLOW.md`
- 업그레이드 스킬: `.codex/skills/spec-upgrade/SKILL.md`

## 2026-04-03 - Spec rewrite: single-file to index + sub-file structure (v3.8.2 → v3.9.0)

### Context

main.md가 1206줄(32,933 토큰)으로 비대해져 AI 에이전트의 컨텍스트 로드와 사용자의 정보 탐색 모두 비효율적이었다. 8개 핵심 metric 진단 결과 Component Separation과 Findability가 2점(3점 만점)으로, 구조적 개선이 필요했다. Whitepaper 핵심 narrative(§1-§3)는 양호하나 Component Details, Usage Guide, Changelog가 본문에 포함되어 불필요한 길이를 차지하고 있었다.

### Decision

1. **main.md를 인덱스로 전환**: §1-§3(Background, Core Design, Architecture)은 인라인 유지, §4 상세/§5/Changelog는 별도 파일로 분리
2. **신규 파일 3개 생성**: `components.md`(§4 + Code Reference Index), `usage-guide.md`(§5), `logs/changelog.md`(Changelog 이동)
3. **해결 완료 이슈 삭제**: #1-4, #8-16번을 본문에서 제거 (changelog에서 이미 추적 가능)
4. **§4 요약 테이블 + 에이전트 목록은 main에 유지**: 컴포넌트 탐색 진입점 역할

### Rationale

- template-compact.md 기준 중규모(500-1500줄) 스펙은 인덱스 + 컴포넌트 파일 구조가 권장됨
- main.md 경량화로 AI 에이전트의 컨텍스트 효율이 향상됨 (668줄, 45% 감축)
- whitepaper 핵심 narrative(§1, §2, §5)는 모두 보존됨 — §5는 별도 파일이지만 1-hop 접근 가능
- 모든 컴포넌트의 Why 필드, Design Rationale 테이블, Source 매핑이 원본 그대로 보존됨

### Changes

- `_sdd/spec/main.md` — v3.8.2 → v3.9.0 (1206줄 → 668줄)
- `_sdd/spec/components.md` — 신규 생성 (303줄)
- `_sdd/spec/usage-guide.md` — 신규 생성 (84줄)
- `_sdd/spec/logs/changelog.md` — 신규 생성 (Changelog 이동)
- `_sdd/spec/logs/spec-rewrite-plan.md` — 진단 및 계획
- `_sdd/spec/logs/rewrite_report.md` — 실행 결과 리포트
- `_sdd/spec/prev/prev_main.md_20260403_000930.md` — 백업

### References

- 진단/계획: `_sdd/spec/logs/spec-rewrite-plan.md`
- 실행 리포트: `_sdd/spec/logs/rewrite_report.md`

## 2026-04-01 - Tighten implementation review loop exit criteria and retry handoff

### Context

Codex `implementation`에 iteration review loop를 도입한 뒤 첫 implementation-review에서 세 가지 후속 문제가 드러났다. 첫째, `_sdd/env.md`가 없을 때 `UNTESTED`만으로도 PASS가 가능해 검증되지 않은 구현이 종료될 수 있었다. 둘째, `IMPLEMENTATION_REPORT.md` 생성과 `UNTESTED` 근거 기록 요구가 loop 종료 조건과 느슨하게 연결되어 있었다. 셋째, Step 7.4에 retry context를 반드시 다음 worker/sub-agent에 전달하라는 계약이 부족했다. Claude 구현도 같은 review loop semantics를 공유하고 있어 동일한 함정을 갖고 있었다.

### Decision

1. **`UNTESTED` 허용 범위 축소**: `UNTESTED`는 단순 "테스트 못 돌림"이 아니라, 테스트 불가 사유와 코드 분석 근거를 리포트에 명시할 수 있을 때만 허용
2. **PASS 게이트 강화**: 종료 조건은 "모든 AC가 `MET`이거나, `UNTESTED` 항목마다 근거와 사유가 기록되어 있고 `Critical/High == 0`"으로 고정
3. **Report requirement 명시**: `implementation` Acceptance Criteria와 Step 8 Report에 `IMPLEMENTATION_REPORT.md` 생성 및 `UNTESTED` 근거 기록 요구를 반영
4. **Retry handoff contract 필수화**: iteration 재실행 prompt에는 `failed_ac`, `failure_reason`, `open_critical_high_issues`를 반드시 포함하고, worker/sub-agent는 이전 실패를 어떻게 해소했는지 보고
5. **Claude/Codex parity 유지**: 위 보정을 `.claude`와 `.codex` 양쪽 `implementation` 문서에 동일하게 반영

### Rationale

- raw `UNTESTED` PASS는 검증되지 않은 구현을 조용히 성공 처리하는 위험이 있었다
- `UNTESTED`를 예외적 상태로 좁혀야 Verification Gate 철학과 iteration review loop가 일관된다
- retry context가 빠지면 loop가 "같은 작업을 다시 해 본다" 수준으로 약해져 실패 원인 교정 능력이 떨어진다
- review loop semantics가 런타임마다 갈라지면 spec과 운영 기준이 다시 쉽게 drift한다

### Changes

- `.codex/skills/implementation/SKILL.md` -- `UNTESTED` 판정/종료 조건/Step 7.4 retry handoff/Report requirement 보정
- `.codex/agents/implementation.toml` -- custom agent mirror 동기화
- `.claude/skills/implementation/SKILL.md` -- retry context block 추가, `UNTESTED` 종료 기준 보정
- `.claude/agents/implementation.md` -- sub-agent prompt 및 review loop semantics 동기화
- `_sdd/spec/main.md` -- implementation component details, changelog 갱신

### References

- 구현 리뷰: `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
- 구현 리포트: `_sdd/implementation/IMPLEMENTATION_REPORT.md`

## 2026-04-01 - Remove write_skeleton and adopt producer-owned inline 2-phase writing

### Context

`write_skeleton` helper agent는 skeleton-first writing 품질을 높이려는 의도로 도입되었지만, 실제 운영에서는 caller가 부모 콘텍스트를 다시 말아 전달해야 하는 비용이 컸다. 특히 skeleton 생성은 현재 호출자의 문맥, 직전 판단, 참고 파일 해석에 강하게 의존하여 `fork_context`, handoff contract, 반환 해석 규칙이 늘어나는 문제가 있었다.

### Decision

1. **`write_skeleton` 완전 제거**: `.claude/agents/write-skeleton.md`, `.codex/agents/write-skeleton.toml` 삭제
2. **Producer-Owned Inline 2-Phase Writing 채택**: 장문 문서/리포트/패치 초안은 caller가 현재 콘텍스트에서 skeleton → fill → finalize를 같은 흐름에서 직접 수행
3. **`write-phased` 재정의**: helper orchestrator가 아니라 공용 inline writing contract로 유지
4. **Caller 문구 정리**: Claude/Codex의 `feature-draft`, `implementation-plan`, `implementation-review`, `spec-create`, `guide-create`, `pr-review`, `pr-spec-patch`, `spec-summary`, `spec-upgrade` 등 writing producer 문서에서 helper 호출 전제를 제거
5. **Spec sync**: `_sdd/spec/main.md`의 agent inventory, directory structure, design pattern, runtime guidance를 현재 구조에 맞게 동기화

### Rationale

- skeleton 생성은 helper 분리보다 부모 콘텍스트 보존이 더 중요했다
- helper layer는 실제로 handoff complexity와 사용성 비용을 증가시켰다
- inline 2-phase writing은 중간 구조를 드러내면서도 context re-packaging 없이 품질을 유지한다
- 플랫폼별 subagent 문법 차이를 줄여 Claude/Codex parity를 단순화할 수 있다

### Changes

- `.claude/agents/write-skeleton.md` -- 삭제
- `.codex/agents/write-skeleton.toml` -- 삭제
- `.claude/skills/write-phased/`, `.codex/skills/write-phased/` -- inline 2-phase writing contract로 재작성
- `.claude/agents/`, `.claude/skills/`, `.codex/agents/`, `.codex/skills/`의 writing producer 문구 -- helper 호출에서 caller-owned skeleton 작성 규칙으로 치환
- `_sdd/spec/main.md` -- version bump, counts 갱신, Producer-Owned Inline 2-Phase Writing 패턴 반영

### References

- 드래프트: `_sdd/drafts/feature_draft_remove_write_skeleton_inline_writing.md`
- 토론: `_sdd/discussion/discussion_write_skeleton_removal_and_inline_writing.md`

## 2026-03-20 - AC-First + Self-Contained 전면 리팩토링 (v3.5.0 -> v3.6.0)

### Context

v3.0에서 도입된 Agent Wrapper 패턴에서, 5개 agent가 skill 디렉토리의 `references/`를 명시적으로 참조하지만 subagent로 실행 시 해당 파일에 접근 불가. Plugin 환경에서도 동일. 또한 agent/skill 파일이 비대하여(agent 9개 합계 4,365줄, full skill 11개 합계 5,042줄) 핵심 로직이 Best Practices, Context Management 등 bloat에 묻혀 있었다.

### Decision

1. **AC-First 구조 전면 적용**: 모든 9개 Claude agent, 11개 Claude full skill, 9개 Codex agent, 10개 Codex full skill에 Acceptance Criteria + 자체 검증 지시(blockquote) + Final Check 추가
2. **Self-Contained Agent**: 핵심 reference 내용을 agent 파일에 인라인 (원본 대비 70%+ 압축), 외부 reference 의존성 완전 제거
3. **공통 bloat 제거**: Best Practices, Context Management, When to Use, Version History, Integration with Other Skills 등 공통 섹션 삭제
4. **래퍼 스킬 정리**: Claude 9개 + Codex 8개 wrapper skill에서 미사용 references/examples 총 48개 파일 삭제
5. **Codex 통일**: Final Smoke Check 제거, Final Check으로 통일
6. **ralph-loop-init 범용화**: "ML 트레이닝 디버그" -> "장기 실행 프로세스(ML, e2e, 빌드 등)"
7. **SDD workflow 세부**: implementation-plan Target Files 충돌 규칙 수정, spec-update-todo 기본 상태 마커 📋 명시, implementation-plan/implementation-review 리팩토링 메타 AC 삭제

### Rationale

- Agent가 subagent로 실행 시 skill 디렉토리 접근 불가 -- self-contained가 유일한 해결책
- AC-First로 실행 결과가 명확히 측정 가능하고, Final Check으로 자체 품질 보장
- Bloat 제거로 LLM 컨텍스트 윈도우 효율 극대화 (Claude agent 55%, full skill 46% 감축)
- 4개 커밋으로 일관된 구조 적용 완료 (7141c70, a751c11, 0ce7fcc, 675ce75)

### Changes

- `.claude/agents/*.md` -- 9개 agent AC-First + self-contained 재작성 (4,365줄 -> 1,961줄)
- `.claude/skills/*/SKILL.md` -- 11개 full skill AC-First 정제 (5,042줄 -> 2,718줄)
- `.codex/agents/*.toml` -- 9개 agent AC-First 정비
- `.codex/skills/*/SKILL.md` -- 10개 full skill AC-First 정제
- `.claude/skills/*/references/`, `.claude/skills/*/examples/` -- 래퍼 스킬 48개 파일 삭제
- `.codex/skills/*/references/`, `.codex/skills/*/examples/` -- Codex 래퍼 스킬 파일 삭제
- `_sdd/spec/main.md` -- v3.5.0 -> v3.6.0

### References

- 드래프트: `_sdd/drafts/feature_draft_agent_self_containment.md`
- 드래프트: `_sdd/drafts/feature_draft_agent_self_containment_phase2.md`
- 드래프트: `_sdd/drafts/feature_draft_full_skills_ac_first.md`
- 드래프트: `_sdd/drafts/feature_draft_codex_agent_wrapper_diet.md`
- 드래프트: `_sdd/drafts/feature_draft_codex_full_skills_ac_first.md`

## 2026-03-19 - sdd-autopilot v2.0.0 Reasoning-Based Rewrite (v3.4.1 -> v3.5.0)

### Context

sdd-autopilot v1.0.0은 규모별 템플릿 매칭(소/중/대 3가지 경로)으로 파이프라인을 구성했다. 이 방식은 3가지 고정 경로만 가능하여 유연성이 제한적이었다. harness 철학에서 영감을 받아, SDD 철학을 이해하고 상황에 맞게 스킬을 동적으로 조합하는 reasoning 기반 오케스트레이션으로 전환하기로 결정했다.

### Decision

1. **SKILL.md 전면 리라이트**: 규모별 템플릿 매칭 -> SDD reference 기반 reasoning + 동적 파이프라인 구성
2. **Reference 문서 통합**: `references/pipeline-templates.md` + `references/scale-assessment.md` 삭제, `references/sdd-reasoning-reference.md` 신규 생성 (docs/ 4개 문서를 ~310줄로 압축, SDD 철학 + 스킬 카탈로그)
3. **Step 구조 변경**: Step 1(Reference Loading), Step 4(Reasoning -> Orchestrator), Step 5(Verification) 신규 추가
4. **Orchestrator Verification**: Producer-Reviewer 패턴으로 구조 6항목 + 철학 6항목 = 12항목 자동 검증
5. **Hard Rule #10 추가**: Execute -> Verify 필수
6. **비오케스트레이션 스킬 재분류**: spec-create, discussion, guide-create는 autopilot 파이프라인에 넣지 않는 스킬로 명시
7. **Dependencies 변경**: 글로벌 스펙 존재 필수 (없으면 /spec-create 안내)

### Rationale

- 규모별 3가지 고정 경로에서 상황 맞춤 무한 조합으로 유연성 확대
- Reference 문서를 Step 1에서 Read하여 reasoning의 기반으로 사용 -- "사람이 docs를 읽고 reasoning하듯이 autopilot도 동일 과정"
- Producer-Reviewer 패턴으로 동적 생성의 리스크를 관리 (구조 의존성 + SDD 철학 정합성 검증)
- Hard Rules(#9 review-fix, #10 execute-verify)와 파일 기반 상태 전달 등 검증된 규칙은 보존

### Changes

- `.claude/skills/sdd-autopilot/SKILL.md` -- v1.0.0 -> v2.0.0 전면 리라이트
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- 신규 생성
- `.claude/skills/sdd-autopilot/references/pipeline-templates.md` -- 삭제 (reference에 흡수)
- `.claude/skills/sdd-autopilot/references/scale-assessment.md` -- 삭제 (reference에 흡수)
- `.claude/skills/sdd-autopilot/skill.json` -- v2.0.0으로 업데이트
- `.codex/skills/sdd-autopilot/SKILL.md` -- v2.0.1 동일 아키텍처 동기화 (Codex 차이점 보존)
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- 신규 생성
- `_sdd/spec/main.md` -- v3.4.1 -> v3.5.0

### References

- 토론: `_sdd/discussion/discussion_autopilot_reasoning_harness.md`

## 2026-03-17 - Codex Autopilot Parity Restoration and Validation Guide Consolidation

### Context

Codex custom agent backbone과 `sdd-autopilot` 구조는 도입되었지만, Codex 쪽 autopilot 문서 세트가 Claude 원본보다 과도하게 축약되어 있었다. 특히 main skill, scale assessment, pipeline templates, sample orchestrator에서 review-fix, test strategy, error handling, final report artifact 같은 실행 계약이 충분히 드러나지 않았다. 또한 Codex dry-run 체크리스트가 `docs/CODEX_AGENT_VALIDATION.md`로 분리되어 있어 운영 가이드와 검증 가이드가 분산되어 있었다.

### Decision

1. **Codex autopilot parity 복원**: `.codex/skills/sdd-autopilot/`의 main skill, references, example을 Claude 원본 대비 의미 보존 수준으로 확장
2. **Final report artifact 명시**: Codex autopilot 산출물 계약에 `_sdd/pipeline/report_<topic>_<timestamp>.md`를 포함
3. **Validation guide 통합**: Codex dry-run 체크리스트를 `docs/AUTOPILOT_GUIDE.md`의 "Codex 검증 체크리스트" 섹션으로 흡수하고 별도 `docs/CODEX_AGENT_VALIDATION.md`는 제거
4. **Spec sync**: `_sdd/spec/main.md`에서도 Codex wrapper -> custom agent 실행 모델, autopilot report artifact, validation guide 위치를 최신 상태로 반영

### Rationale

- Codex 쪽도 실행 계약이 충분히 구체적이어야 generated orchestrator 품질과 운영 가이드를 신뢰할 수 있다
- final report artifact가 문서/예시/가이드에 모두 명시돼야 autopilot completion contract가 일관된다
- validation 체크리스트는 사용자-facing 운영 가이드 안에 있을 때 찾기 쉽고 유지보수 포인트가 줄어든다

### Changes

- `.codex/skills/sdd-autopilot/SKILL.md` -- use/do-not-use, richer execution/test/error handling, final report contract 복원
- `.codex/skills/sdd-autopilot/references/pipeline-templates.md` -- generated orchestrator minimum contract 복원
- `.codex/skills/sdd-autopilot/references/scale-assessment.md` -- 판단 프로세스, 경계 사례, examples 복원
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- review-fix, test, error handling, final report 예시 복원
- `docs/AUTOPILOT_GUIDE.md` -- Codex 검증 체크리스트 섹션 추가, validation guide 흡수
- `_sdd/spec/main.md` -- Codex wrapper/custom-agent 실행 모델, final report artifact, validation guide 위치 동기화

### References

- 드래프트: `_sdd/drafts/feature_draft_autopilot_parity_review.md`
- 드래프트: `_sdd/drafts/feature_draft_codex_agent_backbone_autopilot_parity.md`
- 구현 리포트: `_sdd/implementation/features/autopilot-parity-review/SYNC_20260317_230000_IMPLEMENTATION_REPORT.md`

## 2026-03-17 - Codex Custom Agent Backbone and Autopilot Spawn Model

### Context

초기 Codex 정렬 작업으로 `sdd-autopilot`, generated orchestration skill, `write-phased` utility 설명은 추가되었지만, 실제로 generated orchestrator가 spawn할 repo-local custom agent 레이어가 없었다. 이 상태에서는 "오케스트레이터가 실행 단위를 재사용한다"는 설명은 가능했지만, Claude Code의 `wrapper -> agent -> nested write-phased` 구조와 동등한 실행 backbone은 비어 있었다.

### Decision

1. **Codex custom agent layer 도입**: `.codex/agents/` 아래에 기존 SDD 핵심 역할 8개와 `write_phased`를 custom agent로 정의
2. **wrapper parity 채택**: `.codex/skills/*/SKILL.md`는 사용자 진입점과 handoff contract를 유지하고, 실제 spawned execution unit은 `.codex/agents/*.toml`이 담당
3. **Autopilot spawn 모델 명시**: generated orchestration skill은 skill이 아니라 custom agent를 직접 spawn
4. **nested `write_phased` 1차 범위 확정**: `feature_draft`, `implementation_plan`, `implementation_review`, `spec_review`가 장문 산출물 생성 시 `write_phased`를 nested 사용
5. **Pre-flight 확장**: `_sdd/env.md`와 `.codex/config.toml`을 함께 읽고, 최소 `agents.max_depth >= 2`를 확인

### Rationale

- custom agent 레이어가 있어야 Codex autopilot이 실제로 end-to-end 파이프라인을 실행할 수 있다
- wrapper skill을 유지해야 기존 사용자 호출 인터페이스를 깨지 않으면서 agent spawn 모델을 도입할 수 있다
- planning/review 계열은 long-form writing 품질 이득이 커서 nested `write_phased`의 우선 대상이다
- config 기반 pre-flight가 없으면 nested spawn 구조가 환경에 따라 조용히 실패할 수 있다

### Changes

- `.codex/config.toml` -- agent execution config 신규 추가
- `.codex/agents/` -- 9개 custom agent 정의 신규 추가
- `.codex/skills/feature-draft/`, `.codex/skills/implementation-plan/`, `.codex/skills/implementation/`, `.codex/skills/implementation-review/`, `.codex/skills/spec-update-done/`, `.codex/skills/spec-update-todo/`, `.codex/skills/spec-review/`, `.codex/skills/ralph-loop-init/`, `.codex/skills/write-phased/` -- wrapper/custom-agent parity 반영
- `.codex/skills/sdd-autopilot/` -- custom agent spawn 모델과 pre-flight 반영
- `_sdd/spec/main.md`, `docs/AUTOPILOT_GUIDE.md`, `docs/SDD_QUICK_START.md`, `docs/SDD_WORKFLOW.md` -- custom agent 구조 반영

### References

- 드래프트: `_sdd/drafts/feature_draft_codex_agent_backbone_autopilot_parity.md`
- 드래프트: `_sdd/drafts/feature_draft_autopilot_meta_skill.md`
- 토론: `_sdd/discussion/discussion_autopilot_meta_skill.md`
- 토론: `_sdd/discussion/discussion_write_phased_skill_design.md`

## 2026-03-17 - Codex Autopilot Orchestration and Write-Phased Utility Alignment

### Context

Claude Code용 autopilot 메타스킬과 래퍼/에이전트 구조는 이미 정리되어 있었지만, Codex 쪽에는 대응되는 `sdd-autopilot` 메타스킬과 orchestration contract가 없었다. 또한 `write-phased`는 Claude에서는 에이전트 중심 전략으로 쓰였지만, Codex에서는 공용 long-form writing utility로 어떤 스킬들이 활용해야 하는지 명확히 정리되지 않았다.

### Decision

1. **Codex `sdd-autopilot` 지원 추가**: `.codex/skills/sdd-autopilot/`를 추가하여 기존 execution skill들을 재사용하는 generated orchestration skill 패턴을 지원
2. **오케스트레이터 라이프사이클 하이브리드 정책**: 실행 중에는 `.codex/skills/orchestrator_<topic>/SKILL.md`에 활성 상태로 유지하고, 완료 후에는 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`로 아카이브
3. **Codex binding 책임 분리**: repo는 wrapper/orchestration contract만 정의하고, 실제 wrapper/agent binding은 Codex 런타임/환경 레이어 책임으로 둔다
4. **`write-phased` 승격**: Codex `write-phased`를 `spec-create`, `guide-create`, `pr-spec-patch`, `pr-review`, `spec-summary`, `spec-upgrade`, `sdd-autopilot`이 재사용하는 공용 long-form writing utility로 정의
5. **범위 제한**: `feature-draft -> write-phased` 직접 연동은 후속 최적화로 미루고 이번 결정 범위에서는 제외 **> Superseded by 2026-03-17 custom agent backbone decision: nested write_phased parity를 1차 범위에 포함**

### Rationale

- 기존에 정의한 SDD execution unit들을 유지하면서 Codex에서도 autopilot 메타스킬을 도입하는 편이 가장 낮은 전환 비용으로 구조적 일관성을 확보한다
- 활성 스킬 디렉토리와 아카이브 디렉토리를 분리하면 resume 가능성과 active skill 공간 관리 사이의 균형을 맞출 수 있다
- Codex는 Claude와 다른 orchestration/runtime 모델을 가지므로, repo-local binding까지 고정하는 것보다 contract만 명세하는 편이 유지보수성이 높다
- 긴 문서/대형 코드 출력은 write-phased의 skeleton → fill 전략을 공용 유틸리티로 재사용하는 것이 품질과 안정성에 유리하다

### Changes

- `.codex/skills/sdd-autopilot/` -- 메타스킬 신규 추가
- `.codex/skills/write-phased/` -- 공용 long-form writing utility로 역할 재정의
- `.codex/skills/feature-draft/`, `.codex/skills/implementation-plan/`, `.codex/skills/implementation/`, `.codex/skills/implementation-review/`, `.codex/skills/spec-update-done/`, `.codex/skills/spec-update-todo/`, `.codex/skills/spec-review/`, `.codex/skills/ralph-loop-init/` -- orchestration mode guidance 추가
- `.codex/skills/spec-create/`, `.codex/skills/guide-create/`, `.codex/skills/pr-spec-patch/`, `.codex/skills/pr-review/`, `.codex/skills/spec-summary/`, `.codex/skills/spec-upgrade/` -- long-form writing strategy 반영
- `docs/AUTOPILOT_GUIDE.md`, `docs/SDD_WORKFLOW.md`, `docs/SDD_QUICK_START.md`, `_sdd/spec/main.md` -- Codex autopilot/orchestrator/write-phased 설명 동기화

### References

- 드래프트: `_sdd/drafts/feature_draft_codex_autopilot_orchestration.md`
- 토론: `_sdd/discussion/discussion_autopilot_meta_skill.md`
- 토론: `_sdd/discussion/discussion_autopilot_open_questions.md`
- 토론: `_sdd/discussion/discussion_autopilot_resume_and_partial_execution.md`

## 2026-03-09 - Exploration-first spec adopted for the SDD skills repo

### Context

이 저장소는 스킬 프롬프트와 문서를 다루기 때문에, 코드 설명서보다 "어디를 보고 무엇을 함께 바꿔야 하는지"가 더 중요하다.

### Decision

이 저장소의 스펙도 일반 코드베이스와 같은 탐색형 기준을 적용한다. 메인 문서는 entry point 역할을 하고, 상세는 그룹 스펙으로 분리한다.

### Rationale

스킬 간 계약, 앵커 섹션, spec sync 분류 같은 공통 규칙은 코드보다 문서 사이의 연결을 더 잘 보여줘야 안전하게 바뀔 수 있다.

## 2026-03-09 - Grouped component specs preferred over per-skill specs

### Context

`.codex/skills/`에는 13개의 Codex 스킬이 있고, 이를 곧바로 13개 컴포넌트 스펙으로 쪼개면 메인 스펙보다 탐색 비용이 커질 수 있다.

### Decision

초기 스펙은 `spec lifecycle`, `implementation lifecycle`, `PR lifecycle`의 3개 그룹 스펙으로 시작한다.

### Rationale

이 저장소의 핵심 변경 축은 개별 스킬보다 "workflow group" 단위로 움직이는 경우가 많다. 그룹 스펙이 현재 탐색성과 유지보수성의 균형이 더 좋다.

## 2026-03-09 - Codex skill tree treated as the primary spec target

### Context

최근 정렬 작업과 버전 보강은 `.codex/skills/`를 기준으로 진행되었고, `.claude/skills/`는 평행 구조이지만 완전 동기화 기준은 아직 문서로 확정되지 않았다.

### Decision

현재 저장소 스펙은 `.codex/skills/`를 주 기준으로 설명하고, `.claude/skills/`는 배포/변형 레이어로 다룬다.

### Rationale

현재 실제 정렬 작업과 품질 기준이 Codex 쪽에 집중되어 있으므로, 메인 스펙의 기준선도 여기에 두는 편이 더 명확하다. 플랫폼 parity의 범위는 `Open Questions`로 남긴다.

> **⚠️ Superseded by 2026-03-13 decision below**

## 2026-03-13 - Platform primary target reassessment (.claude/ as source of truth)

### Context

2026-03-09 결정에서 `.codex/skills/`를 주 기준으로 설정했으나, 이후 모든 스킬 변경이 양 플랫폼 동시 적용되고 Claude Code가 더 많은 스킬을 보유(19 vs 17)하게 되었다. 스펙 자체도 `.claude/` 경로를 기준으로 기술하고 있어 실제 운영과 이전 결정이 불일치.

### Decision

`.claude/skills/`를 원본(source of truth)으로, `.codex/skills/`를 파생본으로 정의한다. 동기화 방향은 `.claude/` → `.codex/`.

### Rationale

Claude Code가 기능 상위 집합(19개 vs 17개)이고, Claude Code 전용 스킬(git, sdd-upgrade, discussion)이 존재하며, 스펙과 커밋 히스토리 모두 `.claude/` 기준으로 운영되고 있다.

## 2026-03-13 - Spec Upgrade to Whitepaper Format (v1.1.0 → v2.0.0)

### Context

기존 스펙(`main.md` v1.1.0, 598줄)이 whitepaper §1-§8 구조에 근접했으나 완전히 준수하지 않았다. 서사 섹션(§1 Background & Motivation, §2 Core Design)이 부족하고, 컴포넌트별 Why/Source 필드가 없었으며, Code Reference Index가 없었다.

### Decision

- 기존 멀티파일 구조(main.md + 3 서브 스펙)에서 단일 파일 구조로 이미 통합된 상태를 유지
- 기존 내용을 §1-§8에 재배치: 목표→§1, 공통 패턴→§2, 워크플로우/아티팩트 맵→§3, 플랫폼 차이/설치→§8
- 모든 16개 컴포넌트에 Why와 Source 필드 추가
- Code Reference Index 부록 신규 생성 (16개 SKILL.md 파일 매핑)
- 2-Phase Generation 패턴을 §2 Core Design에 추가 (신규 도입된 패턴)
- 스킬 수 14→16 업데이트 (spec-upgrade, guide-create 반영)

### Rationale

SDD_SPEC_DEFINITION.md 기준 whitepaper 형식 준수. spec-upgrade 스킬의 2-phase 전략 적용 (598줄 >= 300줄 threshold). 기존 내용 최대 보존 원칙에 따라 삭제 없이 재배치.

### Changes

- `_sdd/spec/main.md` — v1.1.0 → v2.0.0 (598줄 → 672줄)
- `_sdd/spec/prev/PREV_sdd_skills_20260313_120859.md` — 백업 생성

## 2026-03-16 - Dual Architecture: Skill + Agent Layer (v2.1.0 → v3.0.0)

### Context

기존 SDD Skills는 스킬 전용(skills-only) 아키텍처로, 20개 스킬이 `.claude/skills/*/SKILL.md`에 전체 로직을 포함하고 있었다. 사용자가 대규모 기능을 구현하려면 6-7개 스킬을 수동으로 순서대로 호출해야 하며, 중간에 맥락이 유실되거나 단계를 빠뜨릴 위험이 있었다. `write-phased` 에이전트가 `tools: ["Agent"]`로 서브에이전트 호출이 가능함을 증명하였다.

### Decision

1. **스킬 + 에이전트 이중 아키텍처 도입**: 8개 파이프라인 필수 스킬을 `.claude/agents/*.md` 에이전트 정의로 분리하고, 기존 SKILL.md는 Agent Wrapper 래퍼로 전환
2. **sdd-autopilot 메타스킬 추가**: 적응형 오케스트레이터를 생성하여 에이전트 파이프라인을 end-to-end 자율 실행
3. **오케스트레이터 저장 위치**: `_sdd/pipeline/`에 저장 (초기 토론에서 `.claude/skills/`로 결정했으나, 후속 토론에서 변경 — 일회성 실행 계획이므로 스킬 디렉토리 오염 방지) **> Superseded by 2026-03-17 decision: `.claude/skills/orchestrator_<topic>/SKILL.md`로 원복 (재사용성 + 재개 기능)**
4. **Codex는 기존 유지**: Agent 도구 제한으로 래퍼 패턴 불가. Codex 동기화는 별도 후속 작업 **> Superseded by 2026-03-17 decision: Codex `sdd-autopilot` + orchestration contract 지원 추가**

### Rationale

- 사용자 인터페이스(`/스킬명`) 하위 호환성 유지가 필수 → 래퍼 스킬 유지
- sdd-autopilot의 서브에이전트 호출을 위해 에이전트 레이어 필요 → Agent Wrapper 패턴
- 선행 집중형 사용자 인터랙션(Phase 1 interactive, Phase 2 autonomous) → 2-Phase Orchestration 패턴
- Discussion은 AskUserQuestion이 핵심이므로 에이전트 전환 불필요 → 스킬 유지

### Changes

- `_sdd/spec/main.md` — v2.1.0 → v3.0.0
- `.claude/agents/` — 8개 에이전트 정의 신규 생성
- `.claude/skills/*/SKILL.md` — 8개 래퍼 전환
- `.claude/skills/sdd-autopilot/` — 메타스킬 신규 생성
- `_sdd/spec/prev/PREV_main_20260316_120000.md` — 백업 생성

### References

- 토론: `_sdd/discussion/discussion_autopilot_meta_skill.md`
- 후속 토론: `_sdd/discussion/discussion_autopilot_open_questions.md`
- Feature Draft: `_sdd/drafts/feature_draft_autopilot_meta_skill.md`

## 2026-03-17 - Autopilot Resume, Partial Execution, and Enhanced Pipeline Log (v3.1.0 → v3.2.0)

### Context

sdd-autopilot이 e2e 전제로 설계되어 있어, 기존 미완료 파이프라인 재개, 기존 산출물 활용(중간 진입), 파이프라인 일부만 실행하는 시나리오가 불가능했다. 또한 오케스트레이터가 `_sdd/pipeline/`에 저장되어 스킬로서 재사용이 불가능하고, 파이프라인 로그에 구조화된 상태 추적이 없었다.

### Decision

1. **Step 0 (Pipeline State Detection) 추가**: autopilot 시작 시 `_sdd/pipeline/log_*.md`를 스캔하여 미완료 파이프라인을 감지하고, 사용자에게 재개/새로 시작 선택을 제시
2. **Step 1.4 (산출물 스캔 + 시작점/종료점 감지) 추가**: 사용자 요청에서 시작/종료 힌트를 파싱하고, `_sdd/` 기존 산출물과의 관련성을 판단하여 파이프라인 범위 조절
3. **Pipeline Log Format 강화**: Meta 섹션(request, orchestrator 참조, scale, started, pipeline) + Status 테이블(5개 상태값: pending/in_progress/completed/failed/skipped) 추가
4. **오케스트레이터 저장 위치 변경**: `_sdd/pipeline/` → `.claude/skills/orchestrator_<topic>/SKILL.md` (변경 이력: `.claude/skills/` → `_sdd/pipeline/` → `.claude/skills/`)

### Rationale

- 오케스트레이터를 `.claude/skills/`에 저장하면 스킬로서 재사용 가능하고, 재개 시 파이프라인 정의 역할을 수행할 수 있다
- 로그의 Status 테이블로 재개 시 첫 번째 미완료 스텝을 빠르게 찾을 수 있다
- 산출물 스캔으로 기존 작업 결과를 활용하여 불필요한 반복을 방지한다
- 자동 감지 + 사용자 선택 방식으로 재개를 구현하여, Phase 1이 이미 interactive이므로 질문 추가 비용이 낮다

### Changes

- `.claude/skills/sdd-autopilot/SKILL.md` -- Step 0, Step 1.4, Pipeline Log Format 강화, 오케스트레이터 경로 변경
- `_sdd/drafts/feature_draft_autopilot_meta_skill.md` -- Acceptance Criteria 추가 (재개, 부분 실행, 산출물 스캔, 로그 메타데이터)
- `_sdd/spec/main.md` -- v3.1.0 → v3.2.0

### References

- 토론: `_sdd/discussion/discussion_autopilot_resume_and_partial_execution.md`
- 후속 반영: `_sdd/discussion/discussion_autopilot_open_questions.md` (오케스트레이터 위치 결정 변경)

## 2026-03-17 - Agent Non-Interactive Conversion (AskUserQuestion 제거) (v3.0.0 → v3.1.0)

### Context

v3.0에서 8개 스킬을 에이전트로 전환했으나, 에이전트 정의 내에 AskUserQuestion 호출이 남아 있었다. sdd-autopilot의 Phase 2에서 서브에이전트로 호출할 때 사용자 인터랙션이 발생하면 파이프라인이 중단되어 자율 실행이 불가능했다.

### Decision

8개 파이프라인 에이전트(feature-draft, implementation-plan, implementation, implementation-review, ralph-loop-init, spec-review, spec-update-done, spec-update-todo)에서 AskUserQuestion을 완전 제거하고, **Autonomous Decision-Making 패턴**으로 대체한다.

### Rationale

- 서브에이전트는 부모 에이전트(sdd-autopilot)의 컨텍스트 내에서 실행되며, 사용자와 직접 인터랙션할 수 없다
- 모호한 상황에서는 가용 정보로 최선 추론 → 판단 근거를 출력에 기록 → 추론 불가 항목은 Open Questions에 남기는 3단계 전략 적용
- discussion, sdd-autopilot은 풀 스킬이므로 AskUserQuestion 유지 (사용자 인터랙션이 핵심 기능)
- 래퍼 스킬 경유 호출 시에도 에이전트가 non-interactive로 동작하지만, 부모 세션에서 사용자가 결과를 확인할 수 있으므로 문제 없음

### Changes

- `.claude/agents/feature-draft.md` -- AskUserQuestion → 자율 판단 로직
- `.claude/agents/implementation-plan.md` -- AskUserQuestion → 자율 판단 로직
- `.claude/agents/implementation-review.md` -- Tools에서 AskUserQuestion 제거
- `.claude/agents/ralph-loop-init.md` -- AskUserQuestion → 자동 선택/오류 보고
- `.claude/agents/spec-review.md` -- Tools에서 AskUserQuestion 제거
- `.claude/agents/spec-update-done.md` -- AskUserQuestion → 자동 선택/Quick Sync 전환
- `.claude-plugin/marketplace.json` -- sdd-autopilot 스킬 + 8개 에이전트 등록
- `_sdd/spec/main.md` -- v3.0.0 → v3.1.0

## 2026-03-17 - Mandatory Review-Fix Cycle (Hard Rule #9) (v3.2.0 → v3.3.0)

### Context

sdd-autopilot의 review-fix 루프가 선택적으로 동작하여, 리뷰만 실행하고 수정 없이 파이프라인이 종료되는 경우가 발생할 수 있었다. 특히 부분 파이프라인("리뷰만 해줘")이나 재개 시나리오에서 review → fix → re-review 사이클이 보장되지 않았다. 또한 `implementation-review`가 비핵심 단계로 분류되어 있어, 리뷰 실패 시 건너뛸 수 있었다.

### Decision

1. **Hard Rule #9 (Review-Fix 사이클 필수)**: 파이프라인에 review 단계가 포함되면 review → fix → re-review 사이클을 필수 실행. 전체/부분/재개 파이프라인 모두 적용
2. **implementation-review 조건부 핵심 단계 승격**: review가 포함된 파이프라인에서 `implementation-review`는 핵심 단계로 취급하며, 실패 시 건너뛸 수 없음 (최대 3회 재시도 후 실패 시 파이프라인 중단)

### Rationale

- 리뷰 없이 수정을 건너뛰면 발견된 이슈가 방치되어 품질 리스크가 누적된다
- 부분 파이프라인에서도 동일한 품질 기준을 적용하여 일관성 확보
- `implementation-review`가 비핵심이면 리뷰-수정 사이클 자체가 무력화될 수 있다

### Changes

- `.claude/skills/sdd-autopilot/SKILL.md` -- Hard Rule #9 추가, Review-Fix 루프 필수 사이클 강화, implementation-review 조건부 핵심 단계
- `.claude/skills/sdd-autopilot/references/pipeline-templates.md` -- 모든 템플릿에 Hard Rule #9 적용, 핵심 단계에 implementation-review 추가
- `_sdd/spec/main.md` -- v3.2.0 → v3.3.0
