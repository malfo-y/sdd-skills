---
name: spec-update-done
description: This skill should be used when the user asks to "update spec from code", "sync spec with implementation", "apply implementation changes to spec", "reflect completed work in spec", "refresh spec after implementation", "implementation done sync", or mentions spec document maintenance tied to completed code changes.
version: 2.2.0
---

# Spec Sync and Update

| Workflow | Position | When |
|----------|----------|------|
| Large | Step 6 of 6 | 구현 완료 후 global spec 동기화 |
| Medium | Final | 구현 반영 마무리 |
| Any | Standalone | code-to-spec sync |

이 agent는 구현 결과와 temporary spec을 읽고 `_sdd/spec/*.md`를 동기화한다. 핵심 원칙은 **temporary execution detail은 버리고, 구현되어 검증된 지속 정보만 global spec에 올린다**는 것이다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] 구현 산출물 기준으로 spec drift를 식별한다.
- [ ] temporary spec delta와 실제 구현 상태를 비교한다.
- [ ] Change Report를 작성하고 반영 내용을 요약한다.
- [ ] 필요한 global spec 업데이트를 적용한다.
- [ ] 검증되지 않았거나 미구현인 planned change를 완료된 사실처럼 쓰지 않는다.

## Hard Rules

1. 변경 적용 전 Change Report를 먼저 정리한다.
2. 스펙 파일 수정 전 `prev/` 백업을 만든다.
3. 구현되지 않았거나 검증되지 않은 계획을 global spec에 완료된 사실처럼 쓰지 않는다.
4. temporary spec의 `Touchpoints`, `Implementation Plan`, `Validation Plan`, transient risk log를 global spec 본문에 그대로 남기지 않는다.
5. 코드/구현 문서를 직접 수정하지 않는다. 이 agent의 대상은 global spec이다.
6. 새 sub-spec 파일 생성 시 반드시 main.md 인덱스에 링크를 추가한다. 고아 파일 금지.
7. 기존 파일 분할 구조를 변경하지 않는다. 파일 추가만 허용, 기존 구조 재편성 금지.
8. rationale 변화가 실제로 발생했을 때만 `decision_log.md`를 업데이트한다.

## Input Sources

우선순위:

1. 실제 코드 변경
2. `_sdd/drafts/feature_draft_<name>.md`
3. `_sdd/implementation/implementation_plan.md`
4. `_sdd/implementation/implementation_progress.md`
5. `_sdd/implementation/implementation_review.md`
6. `_sdd/implementation/implementation_report*.md`
7. `_sdd/spec/*.md`
8. `_sdd/spec/decision_log.md`

## Drift Types

다음 drift를 기본적으로 본다.

- Scope drift
- Contract drift
- Invariant drift
- Verifiability drift
- Usage / expected-result drift
- Decision-bearing structure drift
- Config / environment drift
- Reference / code-map drift

## Process

### Step 1: Gather Context

다음을 읽는다.

- 현재 global spec
- feature draft의 Part 1 temporary spec
- 구현 관련 `_sdd/implementation/*`
- 실제 코드/테스트/설정

목적:

- 완료된 구현 범위 파악
- delta ID별 구현 및 검증 상태 파악
- global spec와 다른 지속 정보 파악
- 분할 스펙이면 main.md 인덱스와 sub-spec 관계 파악

### Step 2: Compare Delta to Reality

temporary spec의 각 delta 항목을 아래 중 하나로 분류한다.

- `IMPLEMENTED`
- `PARTIAL`
- `NOT_IMPLEMENTED`
- `UNVERIFIED`

중요 기준:

- 실제 코드와 evidence가 있는 항목만 global spec에 반영한다.
- `Validation Plan`과 implementation evidence가 연결되지 않으면 `UNVERIFIED`로 남긴다.
- 임시 실행 메모는 반영 대상이 아니다.

#### File Placement Decision (분할 스펙 전용)

단일 파일 스펙이면 건너뛴다.

1. 기존 파일 매칭: 드리프트 항목의 컴포넌트/기능이 기존 sub-spec 파일과 일치 → 해당 파일에 반영
2. Cross-cutting 항목: 환경변수, 글로벌 설정 등은 해당 section이 위치한 파일에 반영
3. 신규 파일 생성: 새 지속 개념이 생겼으나 매칭 없으면 새 파일 생성 후 main.md 인덱스에 링크 추가
4. 소규모 병합: 생성될 내용이 작으면 가장 관련도 높은 기존 파일에 병합

### Step 3: Generate Change Report

변경 전 요약을 만든다.

포함 내용:

- 어떤 global spec section이 바뀌는지
- 어떤 delta ID가 반영되는지
- 어떤 delta ID는 미구현/미검증이라 보류되는지
- drift type
- 적용 action

### Step 4: Apply Updates

global spec 문서를 수정한다.

적용 원칙:

- outdated claim 제거
- 구현 완료되고 검증된 사실 반영
- `Contract/Invariant Delta`가 반영될 때는 canonical CIV 표를 갱신
- user-visible behavior 변화는 `사용 가이드 & 기대 결과`를 갱신
- structural change는 `Decision-bearing structure`를 갱신
- manual curated `Strategic Code Map`이 필요할 때만 appendix를 갱신
- 신규 sub-spec 파일 생성 시 파일 생성 후 main.md 인덱스에 링크 추가

### Step 5: Validate Updates

수정 후 확인한다.

- path / reference / code map이 최신 코드와 맞는가
- 구현되지 않은 내용이 완료된 것처럼 남지 않았는가
- CIV와 usage가 실제 구현과 모순되지 않는가
- (분할 스펙) 신규 파일이 main.md 인덱스에 링크되는가

### Step 6: Archive Implementation Artifacts (Copy-only)

필요 시 구현 산출물을 feature 기준으로 copy-only 아카이브한다.

- 원본은 수정하지 않는다.
- spec sync 근거를 남기기 위한 보조 아카이브다.

## Output Format

변경 요약은 최소한 아래 내용을 포함한다.

```markdown
## Spec Sync Report

**Reviewed**: YYYY-MM-DD
**Code State**: [summary]

### Change Summary
| Section | Delta IDs | Status | Action |

### Applied Updates
- ...

### Deferred Items
- ...

### Open Questions
- ...
```

## Error Handling

| 상황 | 대응 |
|------|------|
| 구현 상태가 불분명 | 미확정 내용은 반영하지 않고 `Open Questions`에 남긴다 |
| spec와 코드가 크게 다름 | drift를 명시하고 보수적으로 sync한다 |
| 백업 경로 없음 | `prev/`를 생성하고 진행한다 |
| 결정 근거가 애매함 | `decision_log.md`에 최소 기록만 남긴다 |
| 파일 배치 판단 모호 | 가장 관련도 높은 기존 파일에 보수적 배치, Change Report에 근거 기록 |

## Integration

- `implementation-review`: 검증된 findings를 sync 근거로 사용
- `spec-review`: sync 후 품질 점검
- `spec-update-todo`: 아직 구현되지 않은 계획 요구사항은 여기로 넘긴다

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Mirror Notice**: 이 스킬의 본문은 `.claude/agents/spec-update-done.md`의 복사본이다.
> 사용자가 직접 호출할 때 중간 과정의 가시성을 확보하기 위해 복붙되었다.
> 내용을 수정할 때는 agent 파일과 이 스킬 파일을 **반드시 함께** 수정해야 한다.
