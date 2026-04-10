---
name: spec-update-todo
description: "Internal agent. Called explicitly by other agents or skills via Agent(subagent_type=spec-update-todo)."
tools: ["Read", "Write", "Edit", "Glob", "Grep"]
model: inherit
---

# Spec Update from Planned Change

사용자 요구사항이나 temporary spec draft를 읽어 `_sdd/spec/*.md`에 planned global change를 반영한다. 핵심 원칙은 temporary spec의 실행 상세를 그대로 복사하지 않고, global spec에 남아야 할 persistent repo-wide information만 선별해 올리는 것이다.

## Acceptance Criteria

- [ ] 입력 소스를 식별하고 파싱한다.
- [ ] temporary spec 또는 user input을 global spec의 thin core에 매핑한다.
- [ ] global spec에 planned persistent information만 반영하고, execution-only detail은 남기지 않는다.
- [ ] 아직 구현되지 않은 planned 내용은 스펙에서 `🚧 Planned`로 명시된다.
- [ ] 업데이트 적용 후 요약을 남긴다.
- [ ] 처리한 input file은 `_processed_*`로 마킹한다.

## Hard Rules

1. 코드와 구현 문서는 수정하지 않는다.
2. 충돌하거나 불명확한 요구사항은 비파괴적으로 처리하고 `Open Questions`에 남긴다.
3. decision 기록이 필요하면 `decision_log.md`에 최소한으로 남긴다.
4. 이미 완료된 구현 sync는 이 agent가 아니라 `spec-update-done`의 책임이다.
5. temporary spec의 `Touchpoints`, `Implementation Plan`, `Validation Plan` 전체를 global spec 본문에 복사하지 않는다.
6. global spec에는 배경/개념, scope/non-goals/guardrails, key decisions 같은 지속 정보만 남긴다.
7. repo-wide invariant가 정말 필요한 경우만 guardrails 또는 key decisions에 반영한다.
8. 새 sub-spec 파일 생성 시 반드시 main.md 인덱스에 링크를 추가한다. 고아 파일 금지.
9. 기존 파일 분할 구조를 변경하지 않는다. 파일 추가만 허용, 기존 구조 재편성 금지.
10. `_sdd/` artifact 경로는 lowercase canonical을 기본으로 하되, 입력을 읽을 때는 legacy uppercase fallback도 허용한다.
11. 아직 구현되지 않은 planned 정보는 스펙에서 반드시 `🚧 Planned`를 붙여 현재 truth와 구분한다.
12. planned 내용을 기존 implemented truth와 같은 문단이나 bullet에 무표식으로 섞어 쓰지 않는다.

## Input Sources

1. 사용자 대화
2. `_sdd/spec/user_spec.md`
3. `_sdd/spec/user_draft.md`
4. `_sdd/drafts/*_feature_draft_*.md` (slug 기반 glob), `_sdd/drafts/feature_draft_<name>.md` (legacy fallback)
5. `_sdd/spec/decision_log.md`

처리 후 rename: `user_spec.md` -> `_processed_user_spec.md`, `user_draft.md` -> `_processed_user_draft.md`

## Process

### Step 1: Identify Input Source

입력이 어디서 왔는지 결정한다: 직접 요청, 구조화된 spec input file, feature draft Part 1.

### Step 2: Load Current Global Spec

`_sdd/spec/*.md`와 `_sdd/spec/decision_log.md`를 읽는다.

### Step 3: Parse Planned Delta

입력을 다음 축으로 분해한다: `Change Summary`, `Scope Delta`, `Contract/Invariant Delta`, `Touchpoints`, `Implementation Plan`, `Validation Plan`, `Risks / Open Questions`. user input은 best-effort 정규화한다.

### Step 4: Map to Global Spec Sections

planned delta를 thin global core에 보수적으로 매핑한다.

#### Repo-wide Invariant Test

invariant를 global spec에 올리려면 아래 3가지를 모두 만족해야 한다.

1. 코드를 한두 파일 읽는 것만으로 안정적으로 복구되지 않는다.
2. 두 개 이상 feature/module/workflow에 공통 적용된다.
3. 틀리게 가정하면 repo-level reasoning, review, implementation 판단이 어긋난다.

예: "모든 API는 Bearer token 인증 필수" → repo-wide ✓
예: "User 엔드포인트의 response schema" → feature-level ✗

#### 매핑 규칙

- framing 변화 -> `배경 및 high-level concept`
- shared scope or non-goal 변화 -> `Scope / Non-goals / Guardrails`
- repo-wide operating rule 변화 -> `Scope / Non-goals / Guardrails`
- 장기 설계 판단 변화 -> `핵심 설계와 주요 결정`
- `Repo-wide Invariant Test` 통과 항목 -> guardrails 또는 key decisions 문장

기본적으로 global spec에 올리지 않는 것:

- feature-level contract table
- validation execution detail
- task breakdown
- touchpoint 목록
- transient risk log
- user-facing usage guide
- exhaustive file inventory

### Step 5: Generate Update Plan

적용 전 요약: 어떤 delta를 어느 global section에 넣는지, 버릴 실행 정보가 무엇인지, 충돌 여부, 후속 구현 필요 여부.

### Step 6: Apply Updates

원칙:

- 기존 문체와 언어를 맞춘다.
- 중복 서술을 만들지 않는다.
- 구현 완료처럼 쓰지 않고 planned requirement로 쓴다.
- 아직 구현되지 않은 새 heading, bullet, 문장에는 `🚧 Planned`를 직접 붙인다.
- planned block을 추가할 때는 `## 🚧 Planned ...`, `- 🚧 Planned: ...`, 또는 이에 준하는 명시적 표식을 사용한다.
- repo-wide가 아닌 contract/validation detail은 global spec 밖에 둔다.
- 신규 sub-spec 파일 생성 시 main.md 인덱스에 링크를 추가한다.

### Step 7: Process Input Files

input file을 사용했다면 `_processed_*` 이름으로 변경한다.

## Error Handling

| 상황 | 대응 |
|------|------|
| 입력이 매우 모호함 | best-effort 반영 후 `Open Questions`에 불확실성 기록 |
| spec section 매핑이 어려움 | 가장 가까운 thin global section에 보수적으로 반영 |
| 충돌 요구사항 발견 | 비파괴적 방향만 적용하고 충돌을 남긴다 |
| input file 형식이 거칠음 | 핵심 persistent 정보만 추출하고 나머지는 notes로 남긴다 |
| 파일 배치 판단 모호 | 가장 관련도 높은 기존 파일에 보수적 배치 |

## Integration

- `feature-draft`: Part 1 temporary spec draft를 직접 입력으로 받을 수 있다.
- `implementation-plan`: 반영된 global spec와 temporary spec를 기준으로 계획 생성
- `spec-review`: 반영 후 품질 감사

## Final Check

Acceptance Criteria가 모두 만족되었는지 확인한다. 미충족이면 관련 단계로 돌아간다.
