---
name: spec-update-done
description: This skill should be used when the user asks to "update spec from code", "sync spec with implementation", "apply implementation changes to spec", "reflect completed work in spec", "refresh spec after implementation", "implementation done sync", or mentions spec document maintenance tied to completed code changes.
version: 2.3.0
---

# Spec Sync and Update

| Workflow | Position | When |
|----------|----------|------|
| Large | Step 6 of 6 | 구현 완료 후 global spec 동기화 |
| Medium | Final | 구현 반영 마무리 |
| Any | Standalone | code-to-spec sync |

이 agent는 구현 결과와 temporary spec을 읽고 `_sdd/spec/*.md`를 동기화한다. 핵심 원칙은 temporary execution detail은 버리고, 구현되어 검증된 persistent repo-wide information만 global spec에 올리는 것이다.

## Acceptance Criteria

- [ ] 구현 산출물 기준으로 spec drift를 식별한다.
- [ ] temporary spec delta와 실제 구현 상태를 비교한다.
- [ ] Change Report를 작성하고 반영 내용을 요약한다.
- [ ] 필요한 global spec 업데이트를 적용한다.
- [ ] 검증되지 않았거나 미구현인 planned change를 완료된 사실처럼 쓰지 않는다.

## Hard Rules

1. 변경 적용 전 Change Report를 먼저 정리한다.
2. 구현되지 않았거나 검증되지 않은 계획을 global spec에 완료된 사실처럼 쓰지 않는다.
3. temporary spec의 `Touchpoints`, `Implementation Plan`, `Validation Plan`, transient risk log를 global spec 본문에 그대로 남기지 않는다.
4. 코드/구현 문서를 직접 수정하지 않는다. 이 agent의 대상은 global spec이다.
5. 새 sub-spec 파일 생성 시 반드시 main.md 인덱스에 링크를 추가한다. 고아 파일 금지.
6. 기존 파일 분할 구조를 변경하지 않는다. 파일 추가만 허용, 기존 구조 재편성 금지.
7. rationale 변화가 실제로 발생했을 때만 `decision_log.md`를 업데이트한다.
8. `_sdd/` artifact 경로는 lowercase canonical을 기본으로 하되, 입력을 읽을 때는 legacy uppercase fallback도 허용한다.

## Input Sources

우선순위:

1. 실제 코드 변경
2. `_sdd/drafts/*_feature_draft_*.md` (slug 기반 glob), `_sdd/drafts/feature_draft_<name>.md` (legacy fallback)
3. `_sdd/implementation/*_implementation_plan_*.md` (slug 기반 glob), `_sdd/implementation/implementation_plan.md` (legacy fallback)
4. `_sdd/implementation/*_implementation_progress_*.md` (slug 기반 glob), `_sdd/implementation/implementation_progress.md` (legacy fallback)
5. `_sdd/implementation/*_implementation_review_*.md` (slug 기반 glob), `_sdd/implementation/implementation_review.md` (legacy fallback)
6. `_sdd/implementation/*_implementation_report_*.md` (slug 기반 glob), `_sdd/implementation/implementation_report*.md` (legacy fallback)
7. `_sdd/spec/*.md`
8. `_sdd/spec/decision_log.md`

## Drift Types

다음 drift를 기본적으로 본다.

- Scope drift
- Guardrail drift
- Key decision drift
- Repo-wide invariant drift
- Config / environment drift
- Reference link drift

## Process

### Step 1: Gather Context

다음을 읽는다.

- 현재 global spec
- feature draft의 Part 1 temporary spec
- 구현 관련 `_sdd/implementation/*`
- 실제 코드/테스트/설정

### Step 2: Compare Delta to Reality

temporary spec의 각 delta 항목을 아래 중 하나로 분류한다.

- `IMPLEMENTED`
- `PARTIAL`
- `NOT_IMPLEMENTED`
- `UNVERIFIED`

기준:

- 실제 코드와 evidence가 있는 항목만 global spec에 반영한다.
- `Validation Plan`과 implementation evidence가 연결되지 않으면 `UNVERIFIED`로 남긴다.
- 임시 실행 메모는 반영 대상이 아니다.

### Step 3: Generate Change Report

포함 내용:

- 어떤 global spec section이 바뀌는지
- 어떤 delta가 반영되는지
- 어떤 delta는 미구현/미검증이라 보류되는지
- drift type
- 적용 action

### Repo-wide Invariant Test

invariant를 global spec에 올리려면 아래 3가지를 모두 만족해야 한다.

1. 코드를 한두 파일 읽는 것만으로 안정적으로 복구되지 않는다.
2. 두 개 이상 feature/module/workflow에 공통 적용된다.
3. 틀리게 가정하면 repo-level reasoning, review, implementation 판단이 어긋난다.

예: "모든 API는 Bearer token 인증 필수" → repo-wide ✓
예: "User 엔드포인트의 response schema" → feature-level ✗

### Step 4: Apply Updates

global spec 문서를 수정한다.

적용 원칙:

- outdated claim 제거
- 구현 완료되고 검증된 사실 반영
- shared scope/non-goal/guardrail 변화 반영
- 장기 설계 판단 변화 반영
- `Repo-wide Invariant Test`를 통과한 항목만 guardrails 또는 decisions에 반영
- feature-level contract/validation/usage는 global 본문에 복구하지 않음
- 신규 sub-spec 파일 생성 시 파일 생성 후 main.md 인덱스에 링크 추가

### Step 5: Validate Updates

수정 후 확인한다.

- path / reference가 최신 코드와 맞는가
- 구현되지 않은 내용이 완료된 것처럼 남지 않았는가
- global spec이 다시 feature-level detail로 두꺼워지지 않았는가
- 신규 파일이 main.md 인덱스에 링크되는가

## Output Format

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
| 결정 근거가 애매함 | `decision_log.md`에 최소 기록만 남긴다 |
| 파일 배치 판단 모호 | 가장 관련도 높은 기존 파일에 보수적 배치 |

## Integration

- `implementation-review`: 검증된 findings를 sync 근거로 사용
- `spec-review`: sync 후 품질 점검
- `spec-update-todo`: 아직 구현되지 않은 계획 요구사항은 여기로 넘긴다

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Mirror Notice**: 이 스킬은 `.claude/agents/spec-update-done.md`와 동일한 계약을 공유한다.
> 내용을 수정할 때는 agent 파일과 이 스킬 파일을 **반드시 함께** 수정해야 한다.
