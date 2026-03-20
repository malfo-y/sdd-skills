---
name: spec-update-todo
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "update spec from input", "add requirements to spec", "spec update", "expand spec", "add to-do to spec", or mentions adding new features, requirements, or planned improvements to an existing specification document.
version: 2.1.0
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
- [ ] 분할 스펙에서 각 항목이 의미적으로 적합한 파일에 배치되고, 신규 파일 생성 시 main.md 인덱스에 링크 추가됨.

## Hard Rules

1. spec 수정 전 `prev/` 백업을 만든다.
2. 코드와 구현 문서는 수정하지 않는다.
3. 충돌하거나 불명확한 요구사항은 비파괴적으로 처리하고 `Open Questions`에 남긴다.
4. 결정 기록이 필요하면 `DECISION_LOG.md`에 최소한으로 남긴다.
5. 이미 완료된 구현 sync는 이 agent가 아니라 `spec-update-done`의 책임이다.
6. 새 sub-spec 파일 생성 시 반드시 main.md 인덱스에 링크를 추가한다. 고아 파일 금지.
7. 기존 파일 분할 구조를 변경하지 않는다. 파일 추가만 허용, 기존 구조 재편성 금지.

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
- 분할 스펙이면: main.md 인덱스에서 링크된 sub-spec 파일 목록 구성, 각 파일의 주제·섹션 구조 파악

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

#### File Placement Decision (분할 스펙 전용)

단일 파일 스펙이면 건너뛴다.

1. **기존 파일 매칭**: 항목의 컴포넌트/기능이 기존 sub-spec 파일과 일치 → 해당 파일에 배치
2. **Cross-cutting 항목**: 환경변수, 글로벌 설정 등은 해당 §이 위치한 파일에 배치
3. **신규 파일 생성**: 매칭 없으면 새 파일 생성 (파일명 = 컴포넌트명, 예: `proxy.md`). main.md 인덱스에 링크 필수
4. **소규모 병합**: 생성될 내용이 50줄 미만이면 가장 관련도 높은 기존 파일에 병합 (소규모 = 잘못된 분할)

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
- 신규 sub-spec 파일 생성 시: 파일 생성 → main.md 인덱스에 링크 추가.

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
| 파일 배치 판단 모호 | 가장 관련도 높은 기존 파일에 보수적 배치, Update Plan에 근거 기록 |

## Integration

- `feature-draft`: Part 1 스펙 패치 초안을 직접 입력으로 받을 수 있다.
- `implementation-plan`: 반영된 spec를 기준으로 계획 생성
- `spec-review`: 반영 후 품질 감사

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Mirror Notice**: 이 스킬의 본문은 `.codex/agents/spec-update-todo.toml`의 `developer_instructions` 복사본이다.
> 사용자가 직접 호출할 때 중간 과정의 가시성을 확보하기 위해 복붙되었다.
> 내용을 수정할 때는 agent 파일과 이 스킬 파일을 **반드시 함께** 수정해야 한다.
