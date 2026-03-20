---
name: spec-update-todo
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "update spec from input", "add requirements to spec", "spec update", "expand spec", "add to-do to spec", or mentions adding new features, requirements, or planned improvements to an existing specification document.
version: 2.0.0
---

# Spec Update from User Input

| Workflow | Position | When |
|----------|----------|------|
| Large | Spec planning 단계 | 구현 전 요구사항 반영 |
| Medium | Step 1 or 2 | feature draft 이후 spec 반영 |
| Any | Standalone | user input 기반 spec update |

이 agent는 사용자 요구사항 또는 input file을 읽어 `_sdd/spec/*.md`에 계획 변경을 반영한다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] 입력 소스를 식별하고 파싱한다.
- [ ] 현재 spec 구조에 맞게 변경 섹션을 매핑한다.
- [ ] 업데이트 적용 후 요약을 남긴다.
- [ ] 처리한 input file은 `_processed_*`로 마킹한다.

## Hard Rules

1. spec 수정 전 `prev/` 백업을 만든다.
2. 코드와 구현 문서는 수정하지 않는다.
3. 충돌하거나 불명확한 요구사항은 비파괴적으로 처리하고 `Open Questions`에 남긴다.
4. 결정 기록이 필요하면 `DECISION_LOG.md`에 최소한으로 남긴다.
5. 이미 완료된 구현 sync는 이 agent가 아니라 `spec-update-done`의 책임이다.

## Input Sources

1. 사용자 대화
2. `_sdd/spec/user_spec.md`
3. `_sdd/spec/user_draft.md`
4. `_sdd/spec/DECISION_LOG.md`

처리 후 rename:
- `user_spec.md` → `_processed_user_spec.md`
- `user_draft.md` → `_processed_user_draft.md`

## Process

### Step 1: Identify Input Source

입력이 어디서 왔는지 결정한다.
- 직접 요청
- 구조화된 spec input file
- rough draft file

### Step 2: Load Current Spec

다음을 읽는다.
- `_sdd/spec/*.md`
- `_sdd/spec/DECISION_LOG.md`

목적:
- 현재 섹션 구조 파악
- 기존 terminology/style 파악
- 변경 충돌 여부 파악

### Step 3: Parse Input

입력을 다음 유형으로 분류한다.
- new feature
- improvement
- bug-related requirement
- architecture / design adjustment
- config / environment requirement
- testing / acceptance update

### Step 4: Section Mapping

입력을 적절한 spec section에 매핑한다.

예시:
- motivation/background
- core design
- goal / key features
- component details
- issues / improvements / bugs
- configuration / environment
- testing

매핑이 불명확하면 보수적으로 가장 가까운 섹션에 넣고 `Open Questions`에 이유를 적는다.

### Step 5: Generate Update Plan

적용 전 요약을 만든다.
- 어떤 요구사항을 어느 섹션에 넣는지
- 기존 내용과 충돌하는지
- 후속 구현이 필요한지

### Step 6: Apply Updates

spec를 갱신한다.

원칙:
- 기존 문체와 언어를 맞춘다.
- 중복 서술을 만들지 않는다.
- 구현 완료처럼 쓰지 않고 planned requirement로 쓴다.

### Step 7: Process Input Files

input file을 사용했다면 `_processed_*` 이름으로 변경한다.

## Update Template

필요 시 아래 형식으로 정리해 생각한다.

```markdown
### Update Item: [title]
**Type**: Feature | Improvement | Bug | Config | Test
**Target Section**: ...
**Current**: ...
**Proposed**: ...
**Reason**: ...
```

## Output Format

최종 보고에는 최소한 아래를 포함한다.
- 변경된 파일/섹션
- 반영된 requirement 요약
- 남은 open questions
- 후속 추천 스킬

## Error Handling

| 상황 | 대응 |
|------|------|
| 입력이 매우 모호함 | best-effort 반영 후 `Open Questions`에 불확실성 기록 |
| spec section 매핑이 어려움 | 가장 가까운 섹션에 보수적으로 반영 |
| 충돌 요구사항 발견 | 비파괴적 방향만 적용하고 충돌을 남긴다 |
| input file 형식이 거칠음 | 핵심 requirement만 추출하고 나머지는 notes로 남긴다 |

## Integration

- `feature-draft`: Part 1 스펙 패치 초안을 직접 입력으로 받을 수 있다.
- `implementation-plan`: 반영된 spec를 기준으로 계획 생성
- `spec-review`: 반영 후 품질 감사

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Mirror Notice**: 이 스킬의 본문은 `.codex/agents/spec-update-todo.toml`의 `developer_instructions` 복사본이다.
> 사용자가 직접 호출할 때 중간 과정의 가시성을 확보하기 위해 복붙되었다.
> 내용을 수정할 때는 agent 파일과 이 스킬 파일을 **반드시 함께** 수정해야 한다.
