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
- [ ] `AGENTS.md`가 하네스 템플릿(§0~§5) 기준으로 존재한다 (부재/부분존재 시 SDD-HARNESS 마커 멱등 병합으로 생성/보강).
- [ ] `CLAUDE.md`가 `→ AGENTS.md 참조` 마커 포인터 블록을 가진다 (부재 시 생성, 기존 파일이면 prepend).
- [ ] 병합 결과 `AGENTS.md`·`CLAUDE.md`에 하네스와 별개의 중복 `## SDD란` 블록이 남지 않는다 (기존 산출물 흡수·제거, SDD 무관 사용자 내용은 보존).
- [ ] `.gitignore`에 `SDD-WORKSPACE` 마커 블록이 존재한다 (부재/부분존재 시 process artifact ignore를 멱등 병합).

## SDD Lens

- global spec은 얇은 기준 문서다.
- temporary spec은 별도의 실행 청사진이다.
- repo-wide invariant가 진짜 필요하면 guardrails 또는 key decisions로 남긴다.
- feature-level usage, validation, current-form CIV는 기본 global core가 아니다.
- legacy inventory는 decision-bearing truth, navigation-critical hint, stale/exhaustive detail로 먼저 분류한다.
- 구조 재편이 더 큰 문제라면 Step 1 경계 판정에 따라 `spec-rewrite`로 분기한다.

## Companion Assets

- `references/spec-format.md`
- `references/template-compact.md`
- `references/template-full.md`
- `references/upgrade-mapping.md`
- `references/agents-harness-template.md`
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
- legacy code map이나 architecture inventory 중 `Strategic Code Map`으로 보존할 navigation-critical hint가 있는지
- supporting surface로 내릴 수 있는 정보
- temporary spec 성격의 내용이 글로벌 스펙에 섞였는지 여부

### Step 3: Evidence Collection

코드베이스가 있으면 아래 근거를 수집한다.

- README / docs / git history -> background / concept / scope
- 핵심 엔트리포인트 / 주요 로직 -> core design, key decisions
- usage docs / examples -> guide 또는 support doc 후보
- validation notes / temp artifacts -> temporary spec 후보
- entrypoint / contract source / invariant hotspot / extension point / validation surface -> `Strategic Code Map` 후보

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
- truly useful guide/reference/Strategic Code Map만 조건부로 남김
- stale하거나 exhaustive한 file tree / component catalog는 global 본문으로 보존하지 않음

### Step 6: Harness Merge (AGENTS.md / CLAUDE.md / .gitignore)

작업 하네스(`AGENTS.md`)가 하네스 템플릿(`references/agents-harness-template.md`) 기준으로 존재하도록 SDD-HARNESS 마커 기반 멱등 병합을 적용한다. spec-upgrade 자체에는 `## SDD란` 같은 삽입 로직이 없다. 여기서 만나는 기존 `## SDD란` 블록은 spec-upgrade가 만든 게 아니라 **과거 spec-create 부트스트랩으로 생긴 소비 repo의 산출물**이며, 이 step은 그것을 삭제 로직 제거가 아니라 **병합 시 하네스 슬롯으로 흡수**한다.

> **하네스 블록은 항상 verbatim 복사다.** 아래 병합 규칙에서 쓰는 '마커 블록'은 매번 `references/agents-harness-template.md`를 **Read**해 `SDD-HARNESS:START`~`SDD-HARNESS:END`를 **글자 그대로 복사**한 것이다(상단 관리용 주석만 제외). `<…>` 꺾쇠 슬롯만 repo 값으로 치환하고, 그 외 어떤 줄도 추가·삭제·재배열·요약하지 않는다. 기억이나 이 SKILL 본문으로 **재구성하지 않는다** — 재구성하면 템플릿 변경(새 §·경고 줄 등)이 산출물에 누락된다.

`AGENTS.md` 병합 규칙:

- **부재** → 위 마커 블록을 **verbatim 복사**해 새 `AGENTS.md`로 쓰고, §0~§5 `<…>` 슬롯만 repo 맥락(`<repo-name>`, `<test command>`, `<lint command>`, spec §`<…>` 등)으로 치환한다.
- **존재(마커 없음)** → 마커 블록을 파일 **맨 위에 prepend**한다. 마커 밖 기존 내용은 아래에 그대로 보존한다.
- **마커 블록 존재** → **그 마커 블록만 교체**한다(마커-only 교체). 마커 밖 내용은 건드리지 않는다. 재실행해도 블록이 중복 적층되지 않는다(멱등).
- **중복 흡수**: 기존 `AGENTS.md`에 하네스 슬롯과 겹치는 항목(테스트 명령 등)이나 과거 spec-create 부트스트랩으로 생긴 legacy `## SDD란` 블록이 있으면, 그 정보를 하네스 슬롯(§2 검증 표준 / §3 워크플로우 / §4 판단 기준)으로 흡수하고 마커 밖 중복본은 제거한다. SDD와 무관한 사용자 고유 내용은 보존한다.

`CLAUDE.md` 병합 규칙:

- 부재면 아래 한 줄 포인터를 SDD-HARNESS 마커 블록으로 감싸 생성하고, 존재하면 그 마커 포인터 블록을 맨 위 prepend한다(마커 블록이 이미 있으면 그 블록만 교체). 포인터 본문은 `> 이 repo의 작업 하네스는 \`AGENTS.md\` 단일 소스다. 작업 전 \`AGENTS.md\`를 먼저 읽는다.`로 spec-create와 동일하게 한다.
- 기존 `CLAUDE.md`에 과거 spec-create 부트스트랩으로 생긴 legacy `## SDD란` 블록이 있으면 AGENTS.md 하네스로 일원화하여 흡수·제거한다. SDD와 무관한 사용자 고유 내용은 보존한다.

병합 후 `AGENTS.md`·`CLAUDE.md` 어디에도 하네스와 별개의 중복 `## SDD란` 블록이 남지 않아야 한다.

`.gitignore` 병합 규칙:

process artifact 디렉토리는 커밋하지 않는다(커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`). `.gitignore`에 아래 `SDD-WORKSPACE` 마커 블록을 멱등 병합한다 — 부재면 생성, 마커 없으면 파일 끝에 append(기존 규칙 보존), 마커 블록 존재면 그 블록만 교체(멱등). 마커 밖 사용자 규칙은 건드리지 않는다.

```gitignore
# SDD-WORKSPACE:START — process artifact는 로컬 전용(커밋 제외)
_sdd/discussion/
_sdd/drafts/
_sdd/implementation/
_sdd/pipeline/
_sdd/pr/
_sdd/work_log/
# SDD-WORKSPACE:END
```

env.md 비밀값 경고는 하네스 §2에 포함돼 있어 AGENTS.md 병합으로 함께 반영된다(별도 처리 불필요).

### Step 7: Validate

아래를 확인한다.

- global spec core가 유지되는가
- 기존 정보가 불필요하게 소실되지 않았는가
- feature-level detail을 global 본문에서 걷어냈는가
- implementation inventory를 그대로 옮겨 적지 않았는가
- Step 1 경계 판정을 어기고 rewrite 문제를 upgrade로 덮지 않았는가
- `AGENTS.md`가 하네스(§0~§5) 마커 블록을 가지고, `CLAUDE.md`가 포인터 마커 블록을 가지며, 하네스와 별개의 중복 `## SDD란` 블록이 남지 않았는가
- `.gitignore`가 `SDD-WORKSPACE` 마커 블록으로 process artifact를 ignore하는가

## Output Contract

최종 보고에는 아래가 포함되어야 한다.

- 업그레이드 대상 파일
- rewrite boundary judgment와 근거
- thin global model gap과 조치
- global에 남긴 판단과 밖으로 내린 정보
- 축약 또는 supporting surface 이동된 old inventory 항목
- 하네스 병합 결과(AGENTS.md/CLAUDE.md/.gitignore 생성·prepend·마커 교체 여부, 흡수·제거된 legacy `## SDD란`/중복 항목)
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
