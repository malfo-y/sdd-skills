---
name: spec-update-done
description: This skill should be used when the user asks to "update spec from code", "sync spec with implementation", "apply implementation changes to spec", "reflect completed work in spec", "refresh spec after implementation", "implementation done sync", or mentions spec document maintenance tied to completed code changes.
version: 2.1.0
---

# Spec Sync and Update

| Workflow | Position | When |
|----------|----------|------|
| Large | Step 6 of 6 | 구현 완료 후 스펙 동기화 |
| Medium | Final | 구현 반영 마무리 |
| Any | Standalone | code-to-spec sync |

이 agent는 구현 결과를 읽고 `_sdd/spec/*.md`와 필요 시 `_sdd/spec/DECISION_LOG.md`를 동기화한다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] 구현 산출물 기준으로 spec drift를 식별한다.
- [ ] Change Report를 작성하고 반영 내용을 요약한다.
- [ ] 필요한 spec 업데이트를 적용한다.
- [ ] 구현 아티팩트를 copy-only 방식으로 보존할 수 있다.
- [ ] 분할 스펙에서 드리프트 항목이 의미적으로 적합한 파일에 반영되고, 신규 파일 생성 시 main.md 인덱스에 링크 추가됨.

## Hard Rules

1. 변경 적용 전 Change Report를 먼저 정리한다.
2. 스펙 파일 수정 전 `prev/` 백업을 만든다.
3. 구현되지 않은 계획을 spec에 완료된 사실처럼 쓰지 않는다.
4. 결정 기록은 필요 시 `DECISION_LOG.md`에만 추가한다.
5. 코드/구현 문서를 직접 수정하지 않는다. 이 agent의 대상은 spec이다.
6. 새 sub-spec 파일 생성 시 반드시 main.md 인덱스에 링크를 추가한다. 고아 파일 금지.
7. 기존 파일 분할 구조를 변경하지 않는다. 파일 추가만 허용, 기존 구조 재편성 금지.

## Input Sources

우선순위:
1. 실제 코드 변경
2. `_sdd/implementation/IMPLEMENTATION_PLAN.md`
3. `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`
4. `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
5. `_sdd/implementation/IMPLEMENTATION_REPORT*.md`
6. `_sdd/spec/*.md`
7. `_sdd/spec/DECISION_LOG.md`

## Drift Types

다음 drift를 기본적으로 본다.
- Architecture drift
- Feature drift
- API drift
- Config / environment drift
- Issue / limitation drift
- Documentation drift
- Decision log drift
- Code snippet / example drift

## Process

### Step 1: Gather Context

다음을 읽는다.
- 현재 spec
- 구현 관련 `_sdd/implementation/*`
- 실제 코드/테스트/설정

목적:
- 완료된 구현 범위 파악
- 계획 대비 실제 완료 상태 파악
- spec와 다른 부분 파악
- 분할 스펙이면: main.md 인덱스에서 링크된 sub-spec 파일 목록 구성, 각 파일의 주제·섹션 구조 파악

### Step 2: Identify Drift

각 spec 항목을 아래 중 하나로 분류한다.
- ADD
- UPDATE
- REMOVE
- KEEP

중요 기준:
- 실제 코드에 없는 계획은 섣불리 반영하지 않는다.
- 실제로 구현되고 검증된 내용 위주로 sync한다.

#### File Placement Decision (분할 스펙 전용)

단일 파일 스펙이면 건너뛴다.

1. **기존 파일 매칭**: 드리프트 항목의 컴포넌트/기능이 기존 sub-spec 파일과 일치 → 해당 파일에 반영
2. **Cross-cutting 항목**: 환경변수, 글로벌 설정 등은 해당 §이 위치한 파일에 반영
3. **신규 파일 생성**: 새 컴포넌트가 코드에 추가되었으나 매칭 없으면 새 파일 생성 (파일명 = 컴포넌트명). main.md 인덱스에 링크 필수
4. **소규모 병합**: 생성될 내용이 50줄 미만이면 가장 관련도 높은 기존 파일에 병합

### Step 3: Generate Change Report

변경 전 요약을 만든다.

포함 내용:
- 어떤 spec section이 바뀌는지
- 현재 서술과 실제 구현의 차이
- drift type
- 적용할 action

### Step 4: Apply Updates

spec 문서를 수정한다.

적용 원칙:
- 기존 섹션 구조를 최대한 유지
- outdated claim 제거
- 구현 완료된 사실 반영
- 신규 sub-spec 파일 생성 시: 파일 생성 → main.md 인덱스에 링크 추가
- rationale 변화가 있으면 `DECISION_LOG.md` 업데이트

### Step 5: Validate Updates

수정 후 확인한다.
- Source / code reference가 최신 코드와 맞는가
- 구현되지 않은 내용이 완료된 것처럼 남지 않았는가
- 섹션 간 모순이 없는가
- (분할 스펙) 신규 파일이 main.md 인덱스에 링크됨

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
| Section | Drift Type | Action |

### Applied Updates
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
| 결정 근거가 애매함 | `DECISION_LOG.md`에 최소 기록만 남긴다 |
| 파일 배치 판단 모호 | 가장 관련도 높은 기존 파일에 보수적 배치, Change Report에 근거 기록 |

## Integration

- `implementation-review`: 검증된 findings를 sync 근거로 사용
- `spec-review`: sync 후 품질 점검
- `spec-update-todo`: 아직 구현되지 않은 계획 요구사항은 여기로 넘긴다

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Mirror Notice**: 이 스킬의 본문은 `.codex/agents/spec-update-done.toml`의 `developer_instructions` 복사본이다.
> 사용자가 직접 호출할 때 중간 과정의 가시성을 확보하기 위해 복붙되었다.
> 내용을 수정할 때는 agent 파일과 이 스킬 파일을 **반드시 함께** 수정해야 한다.
