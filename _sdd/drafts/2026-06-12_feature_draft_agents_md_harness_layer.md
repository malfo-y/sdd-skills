# Feature Draft: SDD 작업 하네스(AGENTS.md) 레이어 도입

> Source of truth: `_sdd/discussion/2026-06-12_discussion_agents_md_harness_layer.md` (결정 9건, 실행항목 6건, 합의 골격, 기각 대안, 핸드오프).

# Part 1: Temporary Spec Draft

<!-- spec-update-todo-input-start -->

## Change Summary

SDD 방법론에 **작업 하네스(work harness) 레이어**를 정식 산출물로 도입한다. global spec(이해 레이어 = what/why/scope/guardrail)은 thin하게 유지한 채, repo에서 작업할 때의 **작업 규약(how)** 능동 계약을 별도 레이어인 `AGENTS.md`로 분리·정식화한다.

- **왜**: global spec 본문을 키우면 "fat 톱니(sawtooth)" 재팽창이 재발한다. 키우는 것은 내용이 아니라 역할이며, 변화 속도·성격이 다른 "이해(느림·수동 참조)"와 "작업 규약(빠름·능동 적용)"을 한 문서에 섞지 않는다.
- **무엇**: (1) §0~§4 골격을 가진 하네스 표준 템플릿 신규 작성, (2) `spec-create`의 기존 빈 AGENTS.md/CLAUDE.md bootstrap을 이 템플릿 기반으로 격상, (3) `spec-upgrade`에 하네스 부재/부분존재 시 마커 기반 멱등 병합 로직 추가, (4) 템플릿을 4곳(`spec-create`·`spec-upgrade` × `.claude`/`.codex`)의 `references/`에 미러, (5) 방법론 문서(SDD_CONCEPT/SDD_WORKFLOW)에 하네스 레이어 반영.
- 모든 하네스 블록은 `<!-- SDD-HARNESS:START -->` ... `<!-- SDD-HARNESS:END -->` 마커로 감싸 신규 생성·병합·재실행 갱신을 멱등하게 식별한다.

## Scope Delta

### In Scope
- 하네스 §0~§4 표준 템플릿 신규 작성 (§0은 behavior guideline 4개 영어 원문 정적 포함, §1·§2·§4의 `<…>`는 repo 맥락 변수 슬롯, 전체 SDD-HARNESS 마커 래핑).
- `spec-create`: AGENTS.md bootstrap을 템플릿 기반 격상 + CLAUDE.md 포인터 생성. 기존 파일 존재 시 마커 멱등 병합. SKILL.md의 Output Contract·Companion Assets·Process Step 3 갱신.
- `spec-upgrade`: 하네스 부재/부분존재 시 마커 멱등 병합 로직 + references/ 템플릿 미러. SKILL.md의 AC·Companion Assets·Process 갱신.
- 템플릿 4곳 미러 (`.claude`/`.codex` × `spec-create`/`spec-upgrade`).
- `SDD_CONCEPT.md` 레이어 표에 하네스 레이어 행 추가, `SDD_WORKFLOW.md`에 하네스 레이어(진입·작업 규약) 위치 명시.

### Out of Scope
- global spec **본문**을 두껍게 만드는 모든 변경 (thin 유지 불변).
- 하네스에 스킬 카탈로그·라우팅 표를 박는 것 (에이전트가 스킬 description 이미 보유 → 중복·stale).
- 하네스에 repo-specific 행동 트리거(이 모듈 read-only 등)를 적는 것 (global spec Guardrails가 단일 소스).
- fat 톱니 능동 해결(update-done에 다이어트 책임 이관 등) — 주기적 review/rewrite로 관리(선행 합의).
- spec-update-done 테스트표준 drift 체크(구 실행항목 #6)는 이번 범위에서 제외 — 핵심 하네스 도입과 의존 없음, 필요 시 별도 작업.

### Guardrail Delta
- (추가) 하네스 템플릿 §4에 "⚠️ repo-specific 주의·불변 규칙은 여기 말고 spec Guardrails (단일 소스)" 경계 문구를 정적 포함해 누수를 구조적으로 차단한다.
- (유지) global spec 본문 thinness 불변. 하네스가 global spec과 내용을 중복하면 중단·보고(중단 조건).

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Add | 하네스 표준 템플릿은 §0~§4 골격을 가지며, §0은 behavior guideline 4개를 **영어 원문 그대로** 정적 포함하고, §1·§2·§4의 repo 맥락 부분은 `<…>` 변수 슬롯으로 비워 둔다. | 에이전트 작업 규약을 단일 형태로 표준화하고, 의역으로 인한 의미 손실을 막는다. |
| C2 | Add | 모든 하네스 블록은 `<!-- SDD-HARNESS:START -->` ... `<!-- SDD-HARNESS:END -->` 마커로 감싼다(신규 생성 포함). | 마커는 병합 전용이 아니라 모든 하네스에 항상 존재 → spec-upgrade 재실행 시 블록 식별·멱등 갱신 보장. |
| C3 | Modify | `spec-create`는 빈 4줄 AGENTS.md 대신 하네스 템플릿(§0~§4)을 슬롯 채워 생성하고, CLAUDE.md는 `→ AGENTS.md 참조` 한 줄 포인터로 생성한다. 기존 Step 3의 legacy `## SDD란` 참조 블록 삽입 로직은 **신규 생성 경로에서 제거**되며, 그 정보(SDD 개념·워크플로우 안내) 역할은 하네스 §3 워크플로우 + §4 판단기준이 대체한다. | bootstrap 격상(새 산출물 추가가 아니라 기존 산출물 내용 격상). 에이전트 중립 + 단일 소스. legacy SDD 블록과 하네스의 중복 공존 방지. |
| C4 | Add | `spec-create`·`spec-upgrade`가 AGENTS.md/CLAUDE.md 생성/병합 시: 파일 부재면 마커 블록 생성, 파일 존재면 SDD-HARNESS 마커 블록을 **맨 위 prepend**하고 마커 밖 기존 내용은 아래 보존, 마커 블록이 이미 있으면 **그 마커 블록만 교체**(마커-only 교체, 멱등). 기존 파일에 legacy `## SDD란` 블록이 있으면 그 정보는 하네스 슬롯으로 흡수되므로 중복 제거(SDD와 무관한 사용자 고유 내용은 보존). | 덮어쓰기 금지 + 재실행 시 하네스 블록 중복 미적층(신규 경로가 legacy `## SDD란`을 더 이상 만들지 않으므로 재실행에도 중복 미적층) + 기존 내용 손실 방지. |
| C5 | Add | 하네스 템플릿은 4곳(`spec-create`·`spec-upgrade` × `.claude`/`.codex`)의 `references/`에 미러로 존재하며, 4곳은 의미상 동일 계약을 유지한다. | 플러그인 배포 시 각 스킬은 자기 폴더 자산만 안정 접근 가능 → 미러 관례 부합. |
| C6 | Modify | `SDD_CONCEPT.md` 레이어 표에 하네스 레이어 행이 추가되고, `SDD_WORKFLOW.md`에 하네스 레이어(Global spec 위, "repo 작업 규약/진입")가 명시된다. | 방법론 문서가 신규 레이어를 반영해 정합 유지. |
| I1 | Add | global spec 본문은 하네스 도입으로 한 줄도 두꺼워지지 않는다(thin understanding anchor 불변). | 핵심 설계 결정 #1. 위반 시 fat 톱니 재발. |
| I2 | Add | 하네스에는 스킬 카탈로그·라우팅 표·repo-specific 행동 트리거를 적지 않는다. §3은 단계 순서만, repo-specific 규칙은 spec Guardrails 단일 소스. | 결정 #3·#7. 누수 방지 + drift 방지. |
| I3 | Add | 하네스와 global spec은 같은 정보를 중복 보유하지 않는다(단일 소스 원칙). | 중단 조건: 중복 발생 시 작업 중단·보고. |

## Touchpoints

> 아래 경로는 현재 코드 탐색으로 재확인함(Glob/Read). `Strategic Code Map`은 본 repo에 별도 없으며 디렉터리 구조가 source of truth.

- `.claude/skills/spec-create/SKILL.md` (Read 완료): Step 3 "Bootstrap Workspace Guidance"가 현재 SDD 참조 블록(빈 수준)만 삽입. Companion Assets에 references 2개(template-compact/full)만 등재. Output Contract에 AGENTS.md/CLAUDE.md 존재. → 하네스 격상·멱등 병합·신규 reference 등재 지점.
- `.codex/skills/spec-create/SKILL.md` (Read 완료): `.claude`와 본문 동일 미러. 동일 갱신 필요.
- `.claude/skills/spec-upgrade/SKILL.md` (Read 완료): AC에 "AGENTS.md, CLAUDE.md 존재(미존재 시 생성)"만 있고 Process에 멱등 병합 로직 부재. Companion Assets에 references 4개. → 멱등 병합 로직 추가·신규 reference 등재 지점.
- `.codex/skills/spec-upgrade/SKILL.md` (Grep 확인): `.claude`와 동일 미러. 동일 갱신 필요.
- `.claude/skills/spec-create/references/`, `.codex/skills/spec-create/references/`, `.claude/skills/spec-upgrade/references/`, `.codex/skills/spec-upgrade/references/` (Glob 확인): 하네스 템플릿 신규 파일 4곳 미러 추가 위치. 기존 미러 파일명·구조 관례(`template-*.md`) 따름.
- `docs/SDD_CONCEPT.md` (Read 완료): §1 핵심 레이어 표(현재 4행: Global spec/Temporary spec/Code·Test/Guide). → 하네스 레이어 행 추가 지점.
- `docs/SDD_WORKFLOW.md` (Read 완료): §1 기본 흐름, §2 Global Spec 사용 시점. → 하네스 레이어 진입·작업 규약 위치 명시 지점.

## Implementation Plan

1. **하네스 템플릿 작성** (C1·C2): §0~§4 골격, §0 영어 원문 4원칙, `<…>` 슬롯, §4 ⚠️ 경계 문구, SDD-HARNESS 마커. 단일 정본을 먼저 확정.
2. **템플릿 4곳 미러** (C5): 정본을 4 references 경로에 배치. 의미 동일 유지.
3. **spec-create 격상** (C3·C4): SKILL.md Step 3를 하네스 템플릿 기반 bootstrap + CLAUDE.md 포인터 + 멱등 병합으로 갱신. Companion Assets·Output Contract 갱신.
4. **spec-upgrade 멱등 병합** (C4): SKILL.md에 하네스 부재/부분존재 시 마커 멱등 병합 Process·AC·Companion Assets 추가.
5. **방법론 문서 반영** (C6): SDD_CONCEPT 레이어 표 + SDD_WORKFLOW 하네스 레이어 추가.

1·2는 정본→미러 순서 의존. 3·4는 템플릿 미러(2) 완료 후 각 스킬 references를 가리킬 수 있다. 5는 1~4와 의미 의존 없이 병렬 가능.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, C2 | review | 정본 템플릿이 §0~§4 + §0 영어 원문 4개 + `<…>` 슬롯 + §4 ⚠️ 경계 + SDD-HARNESS 마커를 모두 가지는지 육안 검토. |
| V2 | C5 | diff | 4곳 references 템플릿이 의미상 동일한지 diff 비교(`.claude` vs `.codex` 미러 관례상 내용 동일 기대). |
| V3 | C3 | review | spec-create 산출물 시나리오: AGENTS.md가 §0~§4로 생성되고 CLAUDE.md가 포인터 한 줄로 생성되며, legacy `## SDD란` 삽입 로직이 제거되어 하네스와 별개의 중복 `## SDD란` 블록이 남지 않는지 SKILL.md Step 3·Output Contract 검토. |
| V4 | C4 | review, test scenario | 기존 AGENTS.md/CLAUDE.md 있는 repo 시나리오에서 두 번 실행 시 하네스 블록이 중복 적층되지 않고 마커 밖 기존 내용이 보존되며, legacy `## SDD란` 블록이 흡수·제거되어 하네스와 별개의 중복 블록이 남지 않는지(멱등성) 수동 시나리오 검증. spec-create·spec-upgrade 양쪽. |
| V5 | C6 | grep, review | SDD_CONCEPT 레이어 표에 하네스 행, SDD_WORKFLOW에 하네스 레이어 언급이 존재하는지 grep + 정합 검토. |
| V6 | I1, I3 | review | 하네스 템플릿(§0~§4)이 global spec understanding 내용(개념/why/scope/guardrail)을 복제하지 않고 작업 규약(how)·포인터에 한정되는지 review. docs 변경분은 레이어 표 행 추가 수준을 넘지 않는지로 한정. 중복 발견 시 중단·보고. |
| V7 | I2 | grep, review | 하네스 템플릿에 스킬명 카탈로그·라우팅 표·repo-specific 트리거 문구가 없는지 grep + 검토. §3은 단계 순서만. |

## Risks / Open Questions

### Q1. spec-create/spec-upgrade의 멱등 병합 로직을 자연어 절차로 둘지, 별도 실행 스크립트로 둘지
- **Decision taken**: 자연어 절차(SKILL.md Process에 마커 prepend·블록 교체 규칙 명시)로 둔다. 별도 스크립트 산출물은 만들지 않는다.
- **Alternatives considered**: (a) 멱등 병합 셸/파이썬 스크립트를 references에 추가 — 본 스킬셋은 SKILL.md 본문 직접 실행(wrapper/스크립트 의존 아님)이 관례라 새 실행 의존을 들이면 미러·배포 부담↑. (b) global spec에 병합 규칙 기술 — I1/I3 위반.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q2. 하네스 §0 4원칙이 user-level `~/.claude/CLAUDE.md`와 repo-level 하네스에 동시에 존재하는 중복
- **Decision taken**: 그대로 둔다(공존). user-level 글로벌과 repo-level 하네스는 스코프가 달라(개인 전역 vs repo 배포 산출물) 중복이 아니라 의도된 이식성. 토론 결정 #6 그대로 반영.
- **Alternatives considered**: (a) 하네스에서 §0 생략하고 user CLAUDE.md에 위임 — repo 배포 시 user 설정이 없는 협업자에겐 원칙이 전달 안 됨. 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q4. `.codex` SKILL.md 본문이 `.claude`와 완전 동일 미러인지(별도 최적화 여부)
- **Decision taken**: 본 repo 현황상 spec-create/spec-upgrade의 SKILL.md 본문은 `.claude`/`.codex` 동일(Read·Grep로 확인). 따라서 SKILL.md 변경은 양쪽에 동일 적용한다. references 내용도 양쪽 동일 미러로 둔다(토론 리서치: 구조 동일, 내용 각자 최적화 가능하나 현 파일은 동일).
- **Alternatives considered**: (a) `.codex`를 에이전트별로 다르게 최적화 — 현 시점 내용 차이 근거 없음 + 미러 동기화 부담↑. 기각.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

작업 하네스(AGENTS.md) 레이어를 SDD 정식 산출물로 도입하는 구현 계획. 정본 하네스 템플릿을 먼저 확정한 뒤 4곳 references에 미러하고, `spec-create`(bootstrap 격상)·`spec-upgrade`(멱등 병합)를 갱신하고, 방법론 문서를 정합시킨다. 코드 산출물은 없으며 전부 마크다운 산출물(템플릿·SKILL.md·docs) 변경이다.

## Scope

- 포함: 하네스 템플릿 신규 작성·4곳 미러, spec-create SKILL.md 격상, spec-upgrade SKILL.md 멱등 병합 추가, SDD_CONCEPT/SDD_WORKFLOW 반영.
- 제외: global spec 본문 변경(Part 1 I1), 스킬 카탈로그/repo-specific 트리거 삽입(Part 1 I2), 별도 실행 스크립트 산출물(Q1), 실제 대상 repo의 AGENTS.md 생성(이 스킬셋 repo가 아니라 소비 repo에서 일어남).

## Components

| Component | 설명 | 대표 경로 |
|-----------|------|-----------|
| harness-template | §0~§4 하네스 정본 템플릿 + 4곳 미러 | `.claude`/`.codex` × `spec-create`/`spec-upgrade` `references/` |
| spec-create-skill | bootstrap 격상 + 포인터 + 멱등 병합 절차 | `.claude`/`.codex` `spec-create/SKILL.md` |
| spec-upgrade-skill | 멱등 병합 절차 추가 | `.claude`/`.codex` `spec-upgrade/SKILL.md` |
| methodology-docs | 레이어 표·워크플로우 반영 | `docs/SDD_CONCEPT.md`, `docs/SDD_WORKFLOW.md` |

## Contract/Invariant Delta Coverage

| Delta | Task |
|-------|------|
| C1 (§0~§4 골격, §0 영어 원문, 슬롯) | T1 |
| C2 (SDD-HARNESS 마커 항상 래핑) | T1 |
| C5 (4곳 미러 의미 동일) | T2 |
| C3 (spec-create bootstrap 격상 + 포인터) | T3 |
| C4 (마커 멱등 병합) | T3, T4 |
| C6 (방법론 문서 반영) | T5 |
| I1 (global spec thin 불변) | 전 task 공통 제약, V6로 검증 |
| I2 (카탈로그·트리거 누수 금지) | T1, V7로 검증 |
| I3 (단일 소스, 중복 금지) | 전 task 공통 제약, V6로 검증 |

## Implementation Phases

- **Phase 1 — 템플릿 정본·미러** (T1 → T2): T1이 정본을 확정하고 T2가 4곳에 미러. 직렬(정본 의존).
- **Phase 2 — 스킬 갱신** (T3, T4): 둘 다 T2(미러된 references 경로 참조) 완료에 의존. T3·T4는 서로 다른 SKILL.md를 건드려 파일 비중첩이나 C4(멱등 병합 규칙)를 공유 가정하므로 동일 phase 내 병렬 가능(의미 충돌 없음 — 같은 마커 규칙을 각자 자기 스킬에 적용).
- **Phase 3 — 방법론 문서** (T5): T1~T4와 의미 의존 없음. Phase 1~2와 병렬 가능.

## Task Details

### Task T1: 하네스 §0~§4 정본 템플릿 작성
**Component**: harness-template
**Priority**: P0
**Type**: Feature

**Description**: 토론 합의 골격(요약 §"합의된 하네스 템플릿 골격")을 정본 템플릿 파일 하나로 작성한다. 전체를 `<!-- SDD-HARNESS:START -->` ... `<!-- SDD-HARNESS:END -->` 마커로 감싸고, §0은 behavior guideline 4개를 영어 원문 그대로 정적 포함, §1·§2·§4의 repo 맥락 부분은 `<…>` 변수 슬롯으로 비운다. §3은 단계 순서만 담고 구체 스킬명은 "설치된 SDD 스킬 사용"으로 가리킨다(카탈로그 금지). §4에 "⚠️ repo-specific 주의·불변 규칙은 여기 말고 spec Guardrails (단일 소스)" 경계 문구를 포함한다. 정본은 미러 작업(T2)의 source.

**Acceptance Criteria**:
- [ ] 전체가 `SDD-HARNESS:START`/`END` 마커로 감싸여 있다 (Contract C2 반영 — 신규 포함 항상 래핑).
- [ ] §0이 4원칙(Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution)을 영어 원문 그대로 포함한다 (Contract C1).
- [ ] §1 읽는 순서, §2 작업 규약/검증 표준, §3 SDD 워크플로우 단계 순서, §4 판단 기준이 골격대로 존재한다.
- [ ] §번호·제목이 토론 합의 골격(§0 작업 원칙 / §1 작업 시작 시 읽는 순서 / §2 작업 규약·검증 표준 / §3 SDD 워크플로우 / §4 판단 기준)과 1:1 일치한다.
- [ ] §1·§2·§4의 repo 맥락 부분이 `<…>` 슬롯으로 비어 있다(예: `<test command>`, `<lint command>`, `<repo-name>`, spec §`<…>`).
- [ ] §3에 개별 스킬명 카탈로그/라우팅 표가 없다 (Invariant I2).
- [ ] §4에 ⚠️ repo-specific 트리거 경계 문구가 있다 (Invariant I2 누수 차단).
- [ ] 정본 파일 상단에 "정본=spec-create references, 나머지 3곳은 미러; 수정 시 4곳 동기" 주석 1줄을 둔다(별도 동기 검증 스크립트는 만들지 않음 — Minimum-Code, Q1 일관).

**Target Files**:
- [C] `.claude/skills/spec-create/references/agents-harness-template.md` -- 정본 템플릿(이 경로를 정본으로 삼고 T2에서 나머지 3곳에 미러)

**Technical Notes**: Covers C1, C2; I2 누수 차단. Validated by V1, V7. 정본 경로는 spec-create references로 둔다(spec-create가 신규 생성 1차 소비자). 파일명은 기존 `template-*.md` 미러 관례와 구분되도록 `agents-harness-template.md` 사용.
**Dependencies**: 없음

### Task T2: 하네스 템플릿을 4곳 references에 미러
**Component**: harness-template
**Priority**: P0
**Type**: Infrastructure

**Description**: T1 정본 템플릿을 나머지 3곳 references 경로에 동일 내용으로 배치해 4곳 미러를 완성한다(`spec-create`·`spec-upgrade` × `.claude`/`.codex`). 4곳은 의미상 동일 계약을 유지한다(Q4: 현 시점 내용 동일).

**Acceptance Criteria**:
- [ ] 4곳 모두에 하네스 템플릿 파일이 존재한다 (Contract C5).
- [ ] 4곳 내용이 의미상 동일하다(diff 시 내용 차이 없음).
- [ ] 4곳 모두 SDD-HARNESS 마커·§0 영어 원문·`<…>` 슬롯·§4 경계 문구를 동일하게 가진다.

**Target Files**:
- [C] `.codex/skills/spec-create/references/agents-harness-template.md` -- T1 정본 미러
- [C] `.claude/skills/spec-upgrade/references/agents-harness-template.md` -- T1 정본 미러
- [C] `.codex/skills/spec-upgrade/references/agents-harness-template.md` -- T1 정본 미러

**Technical Notes**: Covers C5. Validated by V2 (4곳 diff). T1 정본 1곳 + 본 task 3곳 = 4곳.
**Dependencies**: T1 (정본 확정 후 미러)

### Task T3: spec-create SKILL.md bootstrap 격상 + 포인터 + 멱등 병합
**Component**: spec-create-skill
**Priority**: P0
**Type**: Feature

**Description**: `spec-create`의 Step 3 "Bootstrap Workspace Guidance"를 빈 수준 SDD 참조 블록 대신 하네스 템플릿(references) 기반 AGENTS.md 생성으로 격상한다. 현재 Step 3는 AGENTS.md와 CLAUDE.md 양쪽에 legacy `## SDD란` 참조 블록(SDD 정의·docs 링크)을 삽입하는데, 이 **legacy `## SDD란` 삽입 로직을 신규 생성 경로에서 제거**하고 하네스 템플릿 생성으로 대체한다(그 정보 역할은 하네스 §3 워크플로우 + §4 판단기준이 흡수). AGENTS.md는 §0~§4 슬롯을 repo 맥락으로 채워 생성하고, CLAUDE.md는 `→ AGENTS.md 참조` 한 줄 포인터로 생성한다(legacy `## SDD란`은 더 이상 만들지 않음). 기존 AGENTS.md/CLAUDE.md가 있으면 덮어쓰지 않고 SDD-HARNESS 마커 블록을 맨 위 prepend(마커 밖 기존 내용 아래 보존), 마커 블록이 이미 있으면 **그 마커 블록만 교체**(마커-only 교체, 멱등). 기존 파일의 legacy `## SDD란` 블록은 하네스로 대체되므로 제거(SDD와 무관한 사용자 고유 내용은 보존). Companion Assets에 하네스 템플릿 reference를 등재하고, Output Contract·관련 AC를 하네스 산출로 갱신한다. `.claude`/`.codex` 양쪽 동일 적용(Q4).

**Non-Goals**: global spec 본문에 하네스 내용을 옮기지 않는다(I1). 멱등 병합을 위한 별도 실행 스크립트를 만들지 않는다(Q1, 자연어 절차로 기술).

**Acceptance Criteria**:
- [ ] Step 3가 하네스 템플릿(references) 기반으로 AGENTS.md를 §0~§4 슬롯 채워 생성하도록 기술된다 (Contract C3).
- [ ] CLAUDE.md를 `→ AGENTS.md 참조` 포인터로 생성하도록 기술된다 (Contract C3).
- [ ] Step 3의 legacy `## SDD란` 블록 삽입 로직이 신규 생성 경로에서 제거되고 하네스 템플릿 생성으로 대체된다 (Contract C3·C4).
- [ ] 파일 부재→마커 블록 생성, 존재→맨 위 prepend·마커 밖 기존 보존, 마커 블록 존재→마커 블록만 교체(멱등) 절차가 기술된다 (Contract C4).
- [ ] 생성/병합 결과 AGENTS.md·CLAUDE.md에 하네스와 별개의 중복 `## SDD란` 블록이 남지 않는다(기존 파일의 legacy 블록은 흡수·제거, SDD 무관 사용자 내용은 보존) (Contract C4).
- [ ] Companion Assets에 `references/agents-harness-template.md`가 등재된다.
- [ ] Output Contract·AC가 하네스 AGENTS.md/CLAUDE.md 산출을 반영한다.
- [ ] `.claude`/`.codex` 두 SKILL.md가 의미상 동일하게 갱신된다.

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md` -- Step 3·Companion Assets·Output Contract·AC 갱신
- [M] `.codex/skills/spec-create/SKILL.md` -- 동일 미러 갱신

**Technical Notes**: Covers C3, C4. Validated by V3, V4. 기존 Hard Rule 4("AGENTS.md/CLAUDE.md는 없을 때 생성, 있으면 최소 수정")와 충돌하지 않게 마커 멱등 병합으로 정합. T2가 references 경로를 확정해야 Companion Assets가 그 경로를 가리킬 수 있다.
**Dependencies**: T2 (references 미러 경로 확정 후 Companion Assets 등재)

### Task T4: spec-upgrade SKILL.md 마커 멱등 병합 로직 추가
**Component**: spec-upgrade-skill
**Priority**: P0
**Type**: Feature

**Description**: `spec-upgrade`에 하네스 부재/부분존재 시 SDD-HARNESS 마커 기반 멱등 병합 Process를 추가한다(맨 위 prepend, 마커 밖 기존 내용 보존, 마커 블록 존재 시 그 마커 블록만 교체). 기존 AGENTS.md 중복 항목(테스트 명령 등)과, 대상 repo 파일에 (과거 spec-create 부트스트랩으로) 이미 존재하는 legacy `## SDD란` 블록은 병합 시 하네스 슬롯으로 흡수·제거함을 명시한다 — spec-upgrade가 자체 삽입 로직을 삭제하는 게 아니라(spec-upgrade에는 `## SDD란` 삽입 로직이 없다) 소비 repo의 기존 산출물을 흡수하는 동작이다(SDD 무관 사용자 고유 내용은 보존 = C4의 "기존 중복 항목은 하네스 슬롯으로 흡수"의 적용). CLAUDE.md도 기존 파일에 legacy `## SDD란` 블록이 존재하면 AGENTS.md 하네스로 일원화하여 흡수·제거하고, 마커 포인터 블록만 prepend(SDD 무관 사용자 내용은 보존). Companion Assets에 하네스 템플릿 reference 등재, AC("AGENTS.md/CLAUDE.md 존재")를 하네스(§0~§4) 기준으로 강화. `.claude`/`.codex` 양쪽 동일 적용.

**Non-Goals**: legacy→canonical migration 본 로직을 재설계하지 않는다(하네스 병합 step만 추가). global spec 본문을 키우지 않는다(I1).

**Acceptance Criteria**:
- [ ] 하네스 부재/부분존재 시 마커 멱등 병합 Process step이 추가된다 (Contract C4).
- [ ] 기존 파일 존재 시 prepend·마커 밖 기존 보존·마커 블록만 교체(멱등) 규칙이 기술된다 (Contract C4).
- [ ] CLAUDE.md 포인터를 마커로 prepend하고, 기존 파일에 (과거 spec-create 부트스트랩으로) legacy `## SDD란` 블록이 존재하면 흡수·제거하는 절차가 기술된다(SDD 무관 사용자 내용은 보존).
- [ ] 병합 결과 AGENTS.md·CLAUDE.md에 하네스와 별개의 중복 `## SDD란` 블록이 남지 않는다 (Contract C4).
- [ ] Companion Assets에 `references/agents-harness-template.md`가 등재된다.
- [ ] AC가 하네스(§0~§4) 생성/병합 기준으로 갱신된다.
- [ ] `.claude`/`.codex` 두 SKILL.md가 의미상 동일하게 갱신된다.

**Target Files**:
- [M] `.claude/skills/spec-upgrade/SKILL.md` -- Process 병합 step·Companion Assets·AC 갱신
- [M] `.codex/skills/spec-upgrade/SKILL.md` -- 동일 미러 갱신

**Technical Notes**: Covers C4. Validated by V4. C4 멱등 병합 규칙을 T3와 공유하나 각자 자기 스킬에 적용하므로 의미 충돌 없음 → T3와 병렬 가능. T2가 references 경로를 확정해야 Companion Assets 등재 가능.
**Dependencies**: T2 (references 미러 경로 확정 후 Companion Assets 등재)

### Task T5: 방법론 문서에 하네스 레이어 반영
**Component**: methodology-docs
**Priority**: P1
**Type**: Feature

**Description**: `SDD_CONCEPT.md` §1 핵심 레이어 표에 하네스 레이어 행을 추가하고(역할="repo 작업 규약(how)/작업 진입", 담는 것="작업 원칙, 읽는 순서, 검증 표준, 워크플로우 순서, 판단 기준 포인터", 위치는 Global spec 위 진입점), 하네스가 global spec 본문을 키우지 않고 별도 레이어라는 점을 명시한다. `SDD_WORKFLOW.md`에 하네스 레이어(작업 진입·작업 규약, global spec 위)와 그 사용 시점을 짧게 추가한다. global spec과의 단일 소스 경계(repo-specific 트리거는 spec Guardrails)를 한 줄 명시한다.

**Non-Goals**: 방법론 문서에 하네스 템플릿 전문을 복사하지 않는다(템플릿은 references 단일 소스). 스킬 카탈로그를 docs에 박지 않는다.

**Acceptance Criteria**:
- [ ] SDD_CONCEPT.md §1 레이어 표에 하네스 레이어 행이 추가된다 (Contract C6).
- [ ] SDD_WORKFLOW.md에 하네스 레이어(진입·작업 규약, global spec 위)와 사용 시점이 추가된다 (Contract C6).
- [ ] 하네스가 별도 레이어이며 global spec 본문을 키우지 않는다는 경계가 명시된다 (Invariant I1).
- [ ] repo-specific 트리거는 spec Guardrails 단일 소스라는 경계가 언급된다 (Invariant I2/I3).

**Target Files**:
- [M] `docs/SDD_CONCEPT.md` -- §1 레이어 표 행 추가 + 경계 명시
- [M] `docs/SDD_WORKFLOW.md` -- 하네스 레이어 진입·사용 시점 추가

**Technical Notes**: Covers C6; I1·I2·I3 경계 명시. Validated by V5 (grep), V6. T1~T4와 의미 의존 없어 병렬 가능.
**Dependencies**: 없음

## Parallel Execution Summary

- **T1 → T2**: 직렬. T2는 T1 정본을 미러하므로 정본 확정 후 시작.
- **T3 ∥ T4**: T2 완료 후 병렬. 서로 다른 SKILL.md(spec-create vs spec-upgrade) 4파일을 건드려 Target Files 비중첩. C4 멱등 병합 규칙을 공유 가정하나 각자 자기 스킬에 적용해 의미 충돌 없음. T1이 §0~§4 골격·마커 컨벤션을 확정해야 두 task가 동일 규칙을 참조하므로 T1→(T3,T4) 의존도 성립(T2 의존이 이를 포함).
- **T5**: T1~T4와 의미 의존 없이 전 구간 병렬 가능(docs는 references·SKILL.md와 다른 파일이고 내용 의존 없음). 다만 하네스 레이어 명칭·역할 서술이 T1 골격과 정합하면 더 좋아 T1 이후 진행 권장(엄격 의존 아님).

권장 실행: (1) T1 → (2) T2 → (3) T3 ∥ T4 ∥ T5.

## Risks and Mitigations

- **하네스↔global spec 내용 중복(단일 소스 위반)**: T1 §4 ⚠️ 경계 문구 + T5 docs 경계 명시 + V6 검토로 차단. 중복 발생 시 중단·보고(중단 조건).
- **4곳 미러 drift**: V2 diff로 4곳 동일성 검증. 정본(T1)→미러(T2) 단방향으로 source 명확화.
- **멱등성 회귀(재실행 시 블록 중복 적층)**: C4 "마커 블록 존재 시 블록만 교체" 규칙 + V4 두 번 실행 시나리오로 검증.
- **`.codex` 미러 누락**: T3·T4 Target Files에 `.claude`/`.codex` 양쪽을 명시. 6개 SKILL/docs 변경이 모두 양쪽 반영되는지 점검.

## Open Questions

- 실행을 차단하는 미해결 항목 없음.
