---
name: spec-upgrade
description: This skill should be used when the user asks to "upgrade spec", "migrate spec format", "modernize spec structure", "spec upgrade", "스펙 업그레이드", "스펙 변환", "스펙 마이그레이션", or wants to convert old-format spec documents to the current canonical SDD spec model defined in SDD_SPEC_DEFINITION.md.
---

# spec-upgrade

## Goal

기존 구형 스펙을 현재 thinner SDD global spec model로 마이그레이션한다. 목표는 old inventory-heavy 또는 section-heavy structure를 `개념 + 경계 + 결정` 중심 구조로 줄이는 것이다.

유효한 내용은 최대한 보존하되, feature-level usage, validation, exhaustive reference, current-form CIV는 global 기본 본문에서 내린다.

## Acceptance Criteria

아래는 Step 1에서 upgrade로 판정해 migration을 수행하는 경로에 적용한다. 이관/비대상 종료에는 Step 1의 보고만 적용한다.

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
- [ ] `AGENTS.md`·`CLAUDE.md`의 legacy 처리가 Step 6의 보존/흡수 규칙을 따른다.
- [ ] `.gitignore`에 `SDD-WORKSPACE` 마커 블록이 존재한다 (부재/부분존재 시 process artifact ignore를 멱등 병합).
- [ ] 하네스를 병합했으면 Step 6의 local hook installation contract를 적용하고 runtime별 등록·검증·acceptance 상태를 구분했다.

## SDD Lens

- global spec은 얇은 기준 문서다.
- temporary spec은 별도의 실행 청사진이다.
- repo-wide invariant가 진짜 필요하면 guardrails 또는 key decisions로 남긴다.
- feature-level usage, validation, current-form CIV는 기본 global core가 아니다.
- legacy inventory는 decision-bearing truth, navigation-critical hint, stale/exhaustive detail로 먼저 분류한다.
- 구조 재편이 더 큰 문제라면 Step 1 경계 판정에 따라 `spec-rewrite`로 분기한다.

## Companion Assets

- `references/agents-harness-template.md`
- `references/hook-installation.md`
- `references/hooks/worklog-gate.sh`
- `references/hooks/worklog-context.sh`
- `references/hooks/harness-context.sh`
- `references/hooks/agent-watchdog.sh`
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

먼저 업그레이드할 기존 spec이 있는지 확인한다. 없으면 `spec-create`를 권장하고 **비대상으로 종료**한다. spec이 있으면 아래를 본다.

- 현재 작업의 핵심이 legacy-to-canonical migration인가
- 아니면 구조 재설계, 대규모 분할, 역할 재정의, log/history 분리 같은 rewrite 성격이 더 강한가

판정 규칙:

- section-heavy 또는 inventory-heavy 문서를 current model로 줄이는 것이 주된 작업이면 `spec-upgrade`
- domain/topic 재분할, 문서군 재배치, rationale rescue 중심 pruning이면 `spec-rewrite`

`spec-rewrite` 판정이면 대상·근거·후속 스킬을 보고하고 **이관으로 종료**한다. 이관/비대상 경로에서는 Step 2–7의 migration·하네스·훅을 실행하지 않는다. 사용자 요청에 후속 스킬 실행까지 포함돼 있으면 이 결과를 넘겨 해당 스킬로 계속한다.

#### Asset Load: Upgrade Mapping

위 기준만으로 upgrade↔rewrite boundary 또는 legacy section의 current destination이 닫히지 않을 때만 `references/upgrade-mapping.md`를 **Read**한다.

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

#### Asset Load: Current Format

exact current global shape와 비교할 때는 `references/spec-format.md`를, global에 섞인 temporary portion을 판정할 때는 current runtime의 `../feature-draft/SKILL.md` `Required Output`을 **Read**한다.

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

#### Template Selection and Load

| Selection | Closed criterion | Read exactly this asset |
|---|---|---|
| Compact | 기본값 | `references/template-compact.md` |
| Full | source input에 project motivation 또는 evaluated-alternative rationale가 명시돼 있고, compact의 existing named slot에 그 고유한 rationale 역할을 보존할 수 없을 때만 선택한다. | `references/template-full.md` |

migration 작성 직전에 선택한 runtime-local asset만 **Read**한다. 선택한 파일의 fenced skeleton을 verbatim 복사해 heading·field order를 보존하고, source evidence로 placeholder를 치환하며 evidence가 없는 optional block은 제거한다. reference 내용을 기억이나 이 SKILL 본문으로 대체하지 않는다.

### Step 6: Harness Merge (AGENTS.md / CLAUDE.md / .gitignore / 훅 자산)

작업 하네스(`AGENTS.md`)가 하네스 템플릿(`references/agents-harness-template.md`) 기준으로 존재하도록 SDD-HARNESS 마커 기반 멱등 병합을 적용한다. legacy `## SDD란` 블록은 새로 생성하지 않으며, 기존 블록에는 아래 보존/흡수 규칙을 적용한다.

> **하네스 블록은 항상 verbatim 복사다.** 아래 병합 규칙에서 쓰는 '마커 블록'은 매번 `references/agents-harness-template.md`를 **Read**해 `SDD-HARNESS:START`~`SDD-HARNESS:END`를 **글자 그대로 복사**한 것이다(상단 관리용 주석만 제외). repo 변수 슬롯만 치환하고, reference가 명시한 test/lint 부재 시 조건부 삭제만 허용한다. §5의 날짜·제목·모델명 등 향후 work-log 작성용 슬롯은 그대로 둔다. 그 외 어떤 줄도 추가·삭제·재배열·요약하지 않는다. 기억이나 이 SKILL 본문으로 **재구성하지 않는다** — 재구성하면 템플릿 변경(새 §·경고 줄 등)이 산출물에 누락된다.

`AGENTS.md` 병합 규칙:

- **부재** → 위 복사·치환 규칙으로 새 `AGENTS.md`를 쓴다.
- **존재(마커 없음)** → 마커 블록을 파일 **맨 위에 prepend**한다.
- **마커 블록 존재** → **그 마커 블록만 교체**한다. 재실행해도 블록이 중복 적층되지 않는다(멱등).

`CLAUDE.md` 병합 규칙:

- 부재면 아래 한 줄 포인터를 SDD-HARNESS 마커 블록으로 감싸 생성하고, 존재하면 그 마커 포인터 블록을 맨 위 prepend한다(마커 블록이 이미 있으면 그 블록만 교체). 포인터 본문은 `> 이 repo의 작업 하네스는 \`AGENTS.md\` 단일 소스다. 작업 전 \`AGENTS.md\`를 먼저 읽는다.`로 spec-create와 동일하게 한다.

**보존/흡수 규칙** (`AGENTS.md`·`CLAUDE.md` 공통): 마커 밖 원문을 보존한다. 유일한 제거 예외는 **과거 SDD 부트스트랩 생성물로 식별되고 내용이 하네스에 전부 흡수된 중복 블록**이다. `## SDD란`이라는 제목이나 테스트/커밋 규칙의 중복만으로는 제거하지 않는다. 출처·경계가 불명확하거나 사용자 고유 수정이 섞였으면 원문을 보존하고 잔여 중복을 보고한다. 사용자 내용 삭제가 기존 승인 범위에 없으면 승인을 받는다.

`.gitignore` 병합 규칙:

커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`·`drafts/`·`work_log/`다(`drafts/`·`work_log/`는 구현 로그 자산). 나머지 process artifact 디렉토리는 커밋하지 않으므로 `.gitignore`에 아래 `SDD-WORKSPACE` 마커 블록을 멱등 병합한다 — 부재면 생성, 마커 없으면 파일 끝에 append(기존 규칙 보존), 마커 블록 존재면 그 블록만 교체(멱등). 마커 밖 사용자 규칙은 건드리지 않는다.

```gitignore
# SDD-WORKSPACE:START — process artifact는 로컬 전용(커밋 제외)
_sdd/discussion/
_sdd/implementation/
_sdd/pipeline/
_sdd/pr/
# SDD-WORKSPACE:END
```

env.md 비밀값 경고는 하네스 §2에 포함돼 있어 AGENTS.md 병합으로 함께 반영된다(별도 처리 불필요).

#### Hook Assets

훅 설치는 `AGENTS.md` 하네스 병합과 동일 조건이다. 하네스를 병합하면 Claude Code와 Codex 등록을 함께 설치하며 별도 opt-in으로 다루지 않는다.

1. 호출 중인 skill package의 `references/hook-installation.md`를 **Read**하고 전부 적용한다.
2. Claude-only·Codex-only·과거 command/matcher 같은 partial 또는 legacy 설치를 reference의 current 두 runtime 정의로 보완한다. malformed 설정의 skip과 보존은 reference를 따른다.
3. reference의 `Verification and Report`로 멱등성을 검증하고 runtime별 결과를 알린다.

upgrade가 소유하는 것은 부분 설치의 repair 판단이다. hook event·matcher·settings merge·runtime definition·trust 계약은 local reference를 따르며 `spec-create`의 존재에 의존하거나 이 본문에서 fallback을 재구성하지 않는다.

### Step 7: Validate

아래를 확인한다.

- global spec core가 유지되는가
- 기존 정보가 불필요하게 소실되지 않았는가
- feature-level detail을 global 본문에서 걷어냈는가
- implementation inventory를 그대로 옮겨 적지 않았는가
- Step 1 경계 판정을 어기고 rewrite 문제를 upgrade로 덮지 않았는가
- `AGENTS.md`가 하네스(§0~§5) 마커 블록을 가지고, `CLAUDE.md`가 포인터 마커 블록을 가지며, Step 6의 보존/흡수 규칙을 따르는가
- `.gitignore`가 `SDD-WORKSPACE` 마커 블록으로 process artifact를 ignore하는가
- 하네스를 병합했다면 local `references/hook-installation.md`의 `Verification and Report`에 따라 runtime별 등록·검증·acceptance 상태를 구분했는가

## Output Contract

이관/비대상 보고는 Step 1을 따른다. migration을 수행했다면 최종 보고에 아래를 포함한다.

- 업그레이드 대상 파일
- rewrite boundary judgment와 근거
- thin global model gap과 조치
- global에 남긴 판단과 밖으로 내린 정보
- 축약 또는 supporting surface 이동된 old inventory 항목
- 하네스 병합 결과(AGENTS.md/CLAUDE.md/.gitignore 생성·prepend·마커 교체 여부, 흡수·제거된 legacy `## SDD란`/중복 항목)
- 훅 설치 결과 — local `references/hook-installation.md`의 `Report` 계약대로 알린다
- 남은 구조 문제와 후속 추천

## Error Handling

| 상황 | 대응 |
|------|------|
| spec 없음 | Step 1의 비대상 종료 |
| 이미 thin model에 가까움 | 부족한 항목만 보강 |
| canonical 후보 다수 | migration checkpoint에서 확인 |
| 코드베이스 없음 | 문서 기반 업그레이드로 진행하고 근거 수준을 명시 |
| 구조 재편이 핵심 문제 | Step 1의 이관 종료 |

## Final Check

선택한 경로의 Acceptance Criteria를 검증하고, 현재 입력과 권한으로 보완할 수 있는 누락은 해당 단계에서 수정한다. hook의 skipped/partial 또는 trust 대기는 local `references/hook-installation.md`의 종료·보고 규칙을 따른다. 그 밖에 외부 입력이 필요한 잔여 항목도 원문을 보존하고 제한 결과로 종료하며, 완전 완료로 보고하지 않는다.
