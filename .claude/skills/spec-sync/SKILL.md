---
name: spec-sync
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "add to-do to spec", "add to-implement to spec", "add requirements to spec", "update spec from input", "spec update", "expand spec", "update spec from code", "sync spec with implementation", "apply implementation changes to spec", "reflect completed work in spec", "refresh spec after implementation", "implementation done sync", or mentions adding new features/requirements/planned improvements to a specification document, or maintaining the spec document tied to completed code changes.
---

# Spec Sync (Planned + Implemented)

메인 루프가 직접 수행하는 스킬이다. 단일 substrate로 구현 전(planned)·구현 후(implemented) global spec sync를 모두 처리하며, 각 delta 항목을 `Status 분류 (Routing)`으로 분류해 검증된 사실만 현재 truth로 승격한다. 핵심 원칙은 temporary execution detail은 버리고, persistent repo-wide information만 가장 맞는 global surface에 보수적으로 반영하는 것이다.

## 파이프라인 위치 자동 적응

실행 시점의 evidence 유무로 동작이 자동 결정된다 (별도 모드 플래그 없음).

- **구현 전 실행** (코드/구현 산출물 없음): evidence 부재로 모든 delta가 PLANNED로 degrade된다. 모든 신규 정보는 `🚧 Planned`로 표식돼 반영된다.
- **구현 후 실행** (코드/구현 산출물 있음): 각 delta를 실제 코드와 대조해 IMPLEMENTED는 현재 사실로 승격하고, 잔여 미구현분은 PLANNED로 분리한다. 동일 sync 안에서 승격분과 PLANNED 잔여가 혼합될 수 있다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준 + Hard Rules 준수를 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] Input Sources를 식별하고 파싱했다.
- [ ] 각 delta 항목에 `Status 분류 (Routing)`을 적용했다.
- [ ] temporary spec 또는 input을 thin global core의 가장 맞는 surface(main / supporting / history)에 보수적으로 매핑했다 — feature-level detail 과복원이나 wrong-surface inflation 없음.

## Hard Rules

1. 코드와 구현 문서를 직접 수정하지 않는다. 이 스킬이 쓰는 대상은 `_sdd/spec/`과 소비한 input file의 rename뿐이다.
2. **evidence 없으면 승격 금지**: 승격 판단은 `Status 분류 (Routing)`을 따른다. 관측 실패: evidence 없는 planned truth가 current truth로 섞이는 drift.
3. **verified와 planned 분리**: 아직 구현되지 않은 새 heading, bullet, 문장에는 반드시 `🚧 Planned`를 붙여 현재 truth와 구분하고(`## 🚧 Planned ...`, `- 🚧 Planned: ...` 또는 이에 준하는 명시 표식), 검증된 current truth와 planned/미검증 truth를 같은 문단·불릿에 표식 없이 섞어 쓰지 않는다.
4. global 반영 범위는 Step 4의 persistence mapping 기준을 따른다. 관측 실패: temporary task breakdown이 global core로 과복원되는 drift.
5. repo-wide invariant는 아래 `Repo-wide Invariant Test`를 통과할 때만 guardrails 또는 key decisions에 반영한다.
6. main / supporting / history surface 중 어디에 둘지 먼저 판단하고, 가장 맞는 global surface에만 보수적으로 반영한다.
7. draft Target Files(및 legacy `Touchpoints`) 중 장기적으로 반복 사용될 entrypoint, extension point, invariant hotspot, validation surface만 `Strategic Code Map` 후보로 본다. 나머지 target file / task-level touchpoint는 global spec에 복구하지 않는다.
8. 새 sub-spec 파일 생성 시 반드시 main.md 인덱스에 링크를 추가한다. 고아 파일 금지.
9. 기존 파일 분할 구조를 변경하지 않는다. 파일 추가만 허용, 기존 구조 재편성 금지.
10. decision input discovery는 `Input Sources`, 기록 표면 쓰기(entry 조건·최소성 포함)는 Step 5를 따른다. 관측 실패: legacy history 부활과 기존 기록 rewrite.
11. 충돌하거나 불명확한 요구사항은 비파괴적으로 처리하고 `Open Questions`에 남긴다.

## Repo-wide Invariant Test

아래 3가지를 모두 만족할 때만 repo-wide invariant candidate로 본다.

1. 코드를 한두 파일 읽는 것만으로 안정적으로 복구되지 않는다.
2. 두 개 이상 feature/module/workflow에 공통 적용된다.
3. 틀리게 가정하면 repo-level reasoning, review, implementation 판단이 어긋난다.

Positive example:

- 전체 API 인증 방식
- 모든 worker가 따라야 하는 retry / backoff 정책
- `_sdd/` artifact handoff 같은 repo-wide operating rule

Negative example:

- 특정 endpoint의 response schema
- 한 컴포넌트 내부 state invariant
- feature 하나에만 필요한 validation detail

## Input Sources

합집합 6종을 입력으로 받는다. 구현 후 실행일수록 위쪽(코드·구현 산출물)을 우선한다.

1. 실제 코드 변경
2. `_sdd/implementation/*` — plan / progress / review / report (slug 기반 glob: `*_implementation_plan_*.md`, `*_implementation_progress_*.md`, `*_implementation_review_*.md`, `*_implementation_report_*.md`; legacy fallback: `implementation_plan.md`, `implementation_progress.md`, `implementation_review.md`, `implementation_report*.md`)
3. feature draft Part 1 마커 내부(Change Summary·invariant·분할 목록) + 각 task의 `Contracts`/AC (slug 기반 glob: `_sdd/drafts/*_feature_draft_*.md`; legacy full draft의 Part 2 coverage index `C*`/`I*`·`Persistent Spec Implications`는 기록물 fallback으로만 읽고, 새 planned input requirement로 승격하지 않는다)
4. 사용자 대화
5. `_sdd/spec/user_spec.md`, `_sdd/spec/user_draft.md`
6. lowercase canonical `_sdd/spec/decision_log.md`, legacy uppercase `_sdd/spec/DECISION_LOG.md` fallback

`_sdd/` artifact 경로는 lowercase canonical을 기본으로 하되, 입력을 읽을 때는 legacy uppercase fallback도 허용한다.

## Status 분류 (Routing)

각 delta 항목(draft Part 1 마커 내부의 항목 — 계약 실체·검증 evidence는 task의 `Contracts`/AC와 구현 산출물에서 확인; 정규화된 user input)을 실제 코드 + validation evidence 기준으로 아래 4분류 중 하나로 라우팅한다. 임시 실행 메모는 반영 대상이 아니며, global spec에 올리지 않을 항목도 명시적으로 제외/보류 판단한다.

- **IMPLEMENTED / VERIFIED** (코드 + evidence 있음): 현재 사실로 **무표식 승격**. 가장 맞는 global surface에 current truth로 반영한다.
- **PARTIAL** (일부 구현 + evidence): 구현·검증된 분은 current 사실로 승격하고, 잔여 미구현분은 `🚧 Planned`로 분리한다.
- **PLANNED / NOT_IMPLEMENTED** (evidence 없음): `🚧 Planned` 표식으로 반영한다. **evidence가 없으면 이것이 기본 routing이다.**
- **UNVERIFIED** (코드는 있으나 검증이 약함 — task AC·구현 산출물 evidence와 연결 안 됨): 승격을 **보류**하고 `Open Questions`에 남긴다.

분할 draft의 마커 내부에 분할 feature 목록이 있으면, feature 하나당 **개별** `🚧 Planned` 항목으로 반영한다 — 단일 todo로 뭉치지 않는다. 이후 각 feature가 구현·sync될 때 해당 항목만 승격/소거된다.

## Process

### Step 1: Identify Input Source and Pipeline Position

입력이 어디서 왔는지, 그리고 코드/구현 산출물이 존재하는지로 실행 시점을 판단한다.

- 직접 user 요청 / 구조화된 spec input file
- feature draft Part 1 `Spec Delta` (+ 구현 후라면 task AC 충족 evidence)
- `_sdd/implementation/*` 산출물 존재 여부 → 구현 전/후 판별

### Step 2: Gather Context

다음을 읽는다.

- 현재 global spec (`_sdd/spec/*.md`)
- feature draft Part 1 마커 내부 + 해당 task의 `Contracts`/AC
- 구현 관련 `_sdd/implementation/*` (있으면)
- 실제 코드/테스트/설정 (있으면)
- `Input Sources`에서 식별한 decision history

### Step 3: Classify Each Delta by Evidence

각 delta 항목에 `Status 분류 (Routing)`을 적용한다.

### Step 4: Map to Global Spec Sections

분류된 delta를 thin global core에 보수적으로 매핑한다. 먼저 이 정보가 `main.md`, supporting surface, history / decision surface, 또는 temporary spec 중 어디에 남아야 하는지 판단한다.

예시:

- framing 변화 -> `배경 및 high-level concept`
- shared scope or non-goal 변화 -> `Scope / Non-goals / Guardrails`
- repo-wide operating rule 변화 -> `Scope / Non-goals / Guardrails`
- 장기 설계 판단 변화 -> `핵심 설계와 주요 결정`
- `Repo-wide Invariant Test`를 통과한 invariant implication -> guardrails 또는 key decisions 문장
- long-lived navigation hint -> `Strategic Code Map` appendix 또는 supporting surface

기본적으로 global spec에 올리지 않는 것:

- feature-level contract table
- validation execution detail
- task breakdown
- touchpoint 목록
- transient risk log
- user-facing usage guide
- exhaustive file inventory
- one-off target files or task-level implementation touchpoints

### Step 5: Apply Updates

세 표면을 순서대로 쓴다.

1. **live truth**: live truth 파일(`_sdd/spec/`에서 기록 파일을 제외한 전부)을 수정한다. 각 delta는 Step 3 분류대로 반영하고 (승격분은 무표식, 잔여는 `🚧 Planned`, 보류는 `Open Questions`), outdated claim은 제거한다.
   - 기존 문체와 언어를 맞추고, 중복 서술을 만들지 않는다.
   - `main.md`의 헤더 밖 문서 몸통이 바뀌었으면 헤더의 `Spec Version`을 SemVer로 올린다.
2. **기록**: 기존 entry는 수정·삭제하지 않고 신규 entry만 **append-only**로 추가한다.
   - `decision_log.md`: rationale 변화가 있을 때만 최소 entry.
   - `logs/changelog.md`: `main.md` 몸통이 바뀐 버전마다 entry(위에서 올린 버전과 동일).
3. **input file 처리**: 이번 sync에 사용한 input file을 `_processed_` prefix로 rename한다.

### Step 6: Validate and Self-check

수정 후 확인한다.

- path / reference가 최신 코드와 맞는가
- evidence 없는 내용이 완료된 것처럼 남지 않았는가, verified와 planned가 무표식으로 섞이지 않았는가
- global spec이 다시 feature-level detail로 두꺼워지지 않았는가 — 두꺼워졌다면 repo-level 판단 가치가 실제로 설명 가능한가
- wrong-surface restoration이나 불필요한 truth duplication이 없는가
- 신규 파일이 main.md 인덱스에 링크되는가

정합 점검 2종(grep):

- `main.md` 몸통을 고쳤다면 헤더 버전과 `logs/changelog.md` 최신 entry 버전이 **일치**하는가
- 기록 파일을 썼다면 `git diff`에서 `decision_log.md`·`logs/changelog.md`의 **삭제 줄이 0**인가 (append-only 위반 탐지)

## Error Handling

| 상황 | 대응 |
|------|------|
| 입력이 매우 모호함 | best-effort 반영 후 `Open Questions`에 불확실성 기록 |
| 구현 상태가 불분명 | 미확정 내용은 승격하지 않고 PLANNED 또는 `Open Questions`에 남긴다 |
| spec와 코드가 크게 다름 | drift를 명시하고 보수적으로 sync한다 |
| spec section 매핑이 어려움 | 가장 가까운 thin global section에 보수적으로 반영 |
| 충돌 요구사항 발견 | 비파괴적 방향만 적용하고 충돌을 남긴다 |
| 결정 근거가 애매함 | `decision_log.md`에 최소 기록만 남긴다 |
| 파일 배치 판단 모호 | 가장 관련도 높은 기존 파일에 보수적 배치 |

## Integration

- `feature-draft`: current `Part 1: Spec Delta`(마커 내부)를 직접 입력으로 받을 수 있다.
- `implementation-review`: 검증된 findings를 sync 근거로 사용
- `spec-review`: sync 후 품질 점검

## Final Check

Acceptance Criteria가 모두 만족되었나 1회 점검한다 (Step 6이 검증 패스다 — 추가 수정이 있었을 때만 재점검). 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
