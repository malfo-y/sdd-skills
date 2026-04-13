---
name: spec-upgrade
description: This skill should be used when the user asks to "upgrade spec", "migrate spec format", "modernize spec structure", "spec upgrade", "스펙 업그레이드", "스펙 변환", "스펙 마이그레이션", or wants to convert old-format spec documents to the current canonical SDD spec model defined in SDD_SPEC_DEFINITION.md.
version: 1.10.1
---

# spec-upgrade

## Goal

기존 구형 스펙을 현재 thinner SDD global spec model로 마이그레이션한다. 목표는 old inventory-heavy 또는 section-heavy structure를 `개념 + 경계 + 결정` 중심 구조로 줄이는 것이다.

유효한 내용은 최대한 보존하되, feature-level usage, validation, exhaustive reference, current-form CIV는 global 기본 본문에서 내린다.

## Acceptance Criteria

- [ ] canonical spec과 업그레이드 대상 파일 집합을 확정했다.
- [ ] 공통 코어 4축(`Thinness`, `Decision-bearing truth`, `Anti-duplication`, `Navigation + surface fit`) 기준으로 현재 문서를 읽었다.
- [ ] migration 시작 전에 이 작업이 upgrade인지 rewrite인지 경계를 판정하고 결과를 먼저 보고했다.
- [ ] 현재 문서를 새 model 기준으로 gap 분석하고 결과를 먼저 보고했다.
- [ ] 기존 내용을 보존 가능한 범위에서 새 global structure로 재배치했다.
- [ ] old feature-level usage/validation/reference/CIV 의존성을 적절한 surface로 내렸다.
- [ ] 단순 implementation inventory는 줄이고, 필요한 supporting note만 남겼다.
- [ ] 멀티파일 spec이면 index와 supporting file의 역할이 더 명확해졌다.
- [ ] `AGENTS.md`, `CLAUDE.md`가 존재한다 (미존재 시 생성)

## SDD Lens

- global spec은 얇은 기준 문서다.
- temporary spec은 별도의 실행 청사진이다.
- repo-wide invariant가 진짜 필요하면 guardrails 또는 key decisions로 남긴다.
- feature-level usage, validation, current-form CIV는 기본 global core가 아니다.
- 구조 재편이 더 큰 문제라면 Step 1 경계 판정에 따라 `spec-rewrite`로 분기한다.

## Companion Assets

- `references/spec-format.md`
- `references/template-compact.md`
- `references/template-full.md`
- `references/upgrade-mapping.md`
- `examples/before-upgrade.md`
- `examples/after-upgrade.md`
- SDD 정의 문서: https://github.com/malfo-y/sdd-skills/tree/main/docs

## Hard Rules

1. 구현 코드 파일은 수정하지 않는다.
2. 기존 스펙 언어를 따른다.
3. 기존 내용을 최대한 보존하고, 삭제 또는 축약이 필요하면 이유를 명시한다.
4. 결과는 기존 파일 경로에 in-place로 반영한다. 구조 재편이 핵심이면 Step 1 판정에 따라 `spec-rewrite`로 분기한다.
5. global spec을 old canonical 섹션으로 다시 두껍게 복구하지 않는다.
6. `decision_log.md`가 있으면 보존하고, 주요 업그레이드 판단을 추가 기록할 수 있다.
7. Step 1 경계 판정에서 rewrite 성격이 우세하면 upgrade로 밀어붙이지 말고 `spec-rewrite`로 분기한다.

## Process

### Step 1: Rewrite Boundary Judgment

먼저 아래를 본다.

- 현재 작업의 핵심이 legacy-to-canonical migration인가
- 아니면 구조 재설계, 대규모 분할, 역할 재정의, log/history 분리 같은 rewrite 성격이 더 강한가

판정 규칙:

- section-heavy 또는 inventory-heavy 문서를 current model로 줄이는 것이 주된 작업이면 `spec-upgrade`
- domain/topic 재분할, 문서군 재배치, rationale rescue 중심 pruning이면 `spec-rewrite`

### Step 2: Legacy-to-Canonical Gap Analysis

진단 대상:

- canonical spec 후보
- split spec 여부
- 새 global core 존재/부족 상태
- feature-level usage/validation/reference/CIV 오염 여부
- implementation inventory 과잉 여부
- supporting surface로 내릴 수 있는 정보
- temporary spec 성격의 내용이 글로벌 스펙에 섞였는지 여부

### Step 3: Evidence Collection

코드베이스가 있으면 아래 근거를 수집한다.

- README / docs / git history -> background / concept / scope
- 핵심 엔트리포인트 / 주요 로직 -> core design, key decisions
- usage docs / examples -> guide 또는 support doc 후보
- validation notes / temp artifacts -> temporary spec 후보

### Step 4: Migration Checkpoint

정리 항목:

- 기존 스펙 현황
- rewrite boundary judgment 결과
- 새 thin global model gap 분석
- 어떤 정보를 global에 남기고 무엇을 내릴지
- 구조 재편 필요 여부

### Step 5: Migrate

- 기존 내용을 새 global structure로 재배치
- repo-wide invariant가 진짜 필요한 경우만 guardrails 또는 decisions로 반영
- feature-level usage / validation / detail inventory는 supporting surface 또는 temp artifact로 재배치
- truly useful guide/reference/code map만 조건부로 남김

### Step 6: Validate

아래를 확인한다.

- global spec core가 유지되는가
- 기존 정보가 불필요하게 소실되지 않았는가
- feature-level detail을 global 본문에서 걷어냈는가
- implementation inventory를 그대로 옮겨 적지 않았는가
- Step 1 경계 판정을 어기고 rewrite 문제를 upgrade로 덮지 않았는가

## Output Contract

최종 보고에는 아래가 포함되어야 한다.

- 업그레이드 대상 파일
- rewrite boundary judgment와 근거
- thin global model gap과 조치
- global에 남긴 판단과 밖으로 내린 정보
- 축약 또는 supporting surface 이동된 old inventory 항목
- 남은 구조 문제와 후속 추천

## Error Handling

| 상황 | 대응 |
|------|------|
| spec 없음 | `/spec-create` 먼저 권장 |
| 이미 thin model에 가까움 | 부족한 항목만 보강 |
| canonical 후보 다수 | migration checkpoint에서 확인 |
| 코드베이스 없음 | 문서 기반 업그레이드로 진행하고 근거 수준을 명시 |
| 구조 재편이 핵심 문제 | `spec-rewrite` 후보로 보고 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
