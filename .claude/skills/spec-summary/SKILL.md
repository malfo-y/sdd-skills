---
name: spec-summary
description: This skill should be used when the user asks to "summarize spec", "spec summary", "show spec overview", "스펙 요약", "스펙 개요", "show spec status", "스펙 현황", "project overview", "프로젝트 개요", "what's the current state", "현재 상태는", or wants a reader-facing whitepaper of the current repo/spec with an optional appendix for planned/progress signals.
version: 3.0.0
---

# spec-summary

## Goal

현재 global spec, supporting docs, 그리고 필요한 코드 근거를 읽어 `_sdd/spec/summary.md`에 이 저장소를 설명하는 reader-facing whitepaper를 만든다. 이 문서는 기술 화이트페이퍼처럼 읽혀야 하며, 문제와 배경/동기, 핵심 설계, 코드 근거, 사용 흐름과 기대 결과를 한 번에 설명해야 한다. 더 깊은 supporting surface로 자연스럽게 이어져야 하며, 관련 `_sdd/drafts/` 또는 `_sdd/implementation/` artifact가 있으면 appendix로 계획/진행 상태를 짧게 덧붙일 수 있다. 필요할 때만 `README.md`의 managed block을 갱신해, 짧은 요약과 전체 whitepaper 문서를 연결한다.

## Acceptance Criteria

- [ ] `_sdd/spec/summary.md`를 생성하거나 안전하게 갱신했다.
- [ ] global spec, supporting docs, 필요한 코드 surface를 먼저 식별했다.
- [ ] summary 본문이 `Executive Summary`, `Background / Motivation`, `Core Design`, `Code Grounding`, `Usage / Expected Results`, `Further Reading / References`를 포함한다.
- [ ] `Code Grounding`이 concrete path, module/function anchor, 또는 source table로 핵심 설명을 실제 구현과 연결한다.
- [ ] 본문이 단순 status summary가 아니라, 왜 이 구조를 택했는지와 어떤 결과를 기대해야 하는지를 독자가 설명할 수 있을 정도의 whitepaper 밀도를 가진다.
- [ ] `Usage / Expected Results`가 독자가 어떻게 읽고 쓰며 무엇을 기대해야 하는지 분명히 전달한다.
- [ ] 관련 `_sdd/drafts/` 또는 `_sdd/implementation/` artifact가 있으면 appendix 또는 마지막 보조 섹션으로 planned/progress snapshot을 반영했다.
- [ ] summary가 과거 상태 비교, migration memo, changelog처럼 읽히지 않고 현재 기준 내용만 직접 설명한다.
- [ ] README 갱신은 사용자가 명시적으로 요청한 경우에만 수행했다.

## SDD Lens

- summary는 thin global spec을 대체하지 않는다. thin core를 사람에게 설명 가능한 whitepaper surface로 풀어주는 companion 문서다.
- summary는 status digest나 changelog가 아니라, 문제의식과 설계 이유를 함께 설명하는 기술 화이트페이퍼형 surface다.
- 좋은 summary는 문제와 동기, 핵심 설계, 코드 근거, 사용과 기대 결과를 함께 보여주되, exhaustive reference detail을 복제하지 않는다.
- `Code Grounding`은 필수다. 설명이 실제 코드와 이어지지 않으면 whitepaper는 다시 일반 소개문으로 무너진다.
- guide, README, reference docs, temporary artifact는 summary의 하위 대체물이 아니라 supporting surface다. summary는 이들을 대신하지 않고 연결한다.

## Companion Assets

- `references/summary-template.md`: whitepaper 구조 템플릿
- `examples/summary-output.md`: 완성 예시

## Hard Rules

1. `_sdd/spec/*.md`는 읽기 전용이다. 단, `summary.md`는 생성/갱신할 수 있다.
2. README 갱신은 사용자가 명시적으로 요청한 경우에만 수행한다.
3. README는 전체를 덮어쓰지 않는다. `spec-summary` marker block만 갱신하거나 없으면 안전하게 추가한다.
4. 문서 언어는 기존 스펙/문서를 따른다. 기존 스펙이 없으면 한국어를 기본으로 한다.
5. summary가 길거나 구조적으로 복잡하면 caller가 먼저 skeleton/섹션 헤더를 직접 기록한 뒤, 같은 흐름에서 내용을 채운다.
6. split spec 또는 컴포넌트 수가 많으면 병렬 추출 후 부모가 최종 whitepaper를 통합한다.
7. summary는 과거 상태나 변경 이력을 설명하지 않고, 현재 기준의 계약과 구조를 바로 드러내야 한다.
8. `_sdd/` artifact 경로는 lowercase canonical을 기본으로 하되, 입력을 읽을 때는 legacy uppercase fallback도 허용한다.

## Input Sources

우선순위:

1. 사용자 지정 spec 경로
2. `_sdd/spec/main.md` 또는 프로젝트 index spec
3. `components.md`, `usage-guide.md`, `DECISION_LOG.md`, 관련 supporting surface
4. summary의 `Code Grounding`에 필요한 실제 코드 경로, 모듈, 함수, 명령 surface
5. `_sdd/drafts/*_feature_draft_*.md` (관련 appendix signal이 있을 때만)
6. `_sdd/implementation/*_implementation_progress_*.md`, `_sdd/implementation/*_implementation_review_*.md` (관련 appendix signal이 있을 때만)
7. `README.md` (README sync 요청 시만)
8. `_sdd/env.md` (로컬 검증이 필요할 때만)

## Process

### Step 1: Locate the Spec Set

먼저 index/main spec과 supporting surface를 찾고, summary가 설명해야 할 repo-level 핵심 판단을 식별한다.

### Step 2: Locate Concrete Source Anchors

핵심 설계를 실제 구현과 연결할 수 있도록 concrete path, module/function anchor, command surface, 또는 source table 후보를 고른다.

### Step 3: Locate Optional Appendix Inputs

관련 `_sdd/drafts/` 또는 `_sdd/implementation/` artifact가 있으면, summary 맨 뒤 appendix에 넣을 planned/progress 신호만 고른다.

### Step 4: Extract the Facts

whitepaper 본문에는 아래를 추출한다.

- 프로젝트가 해결하는 문제
- 배경과 동기, 접근 이유
- 대안 대비 왜 이 접근을 택했는가
- 핵심 설계와 주요 결정
- 이를 뒷받침하는 concrete code grounding
- 사용 흐름, 기대 결과, 실패/예외 경계
- 더 깊이 읽을 supporting surface
- 관련 artifact가 있으면 planned / in-progress / blocked / next 신호

### Step 5: Build the Whitepaper Shape

summary 기본 순서:

1. Executive Summary
2. Background / Motivation
3. Core Design
4. Code Grounding
5. Usage / Expected Results
6. Further Reading / References
7. Appendix: Planned / Progress Snapshot (Optional)

### Step 6: Write `summary.md`

`references/summary-template.md`를 기반으로 내용을 채우고 `_sdd/spec/summary.md`를 작성한다.

### Step 7: Optional README Sync

사용자가 명시적으로 요청한 경우에만 수행한다.

### Step 8: Final Check

- summary가 reader-facing whitepaper shape를 가졌는가
- summary가 status memo보다 기술 whitepaper처럼 읽히는가
- 문제, 동기, 설계, 코드 근거, 사용과 기대 결과가 빠지지 않았는가
- `Code Grounding`이 실제 source anchor를 제공하는가
- planned/progress 정보가 appendix나 마지막 보조 섹션에만 머무르는가
- README를 요청하지 않았는데 수정하지 않았는가
- change-history narration 없이 현재 내용만 직접 설명하는가

## Output Contract

기본 산출물:

- `_sdd/spec/summary.md`

조건부 산출물:

- `README.md`의 `spec-summary` managed block

## Error Handling

| 상황 | 대응 |
|------|------|
| spec 없음 | `/spec-create` 먼저 권장 |
| split spec 범위 불명확 | supporting surface를 최소 세트로 좁히고 필요 시 notes에 남긴다 |
| code grounding 근거가 약함 | summary 본문을 확장하기 전에 concrete path 또는 source table anchor를 먼저 확보한다 |
| 구현 문서 없음 | whitepaper 본문만 작성하고 appendix는 생략한다 |
| README 요청이 없는데 README 관련 문서만 있음 | README는 수정하지 않음 |
| 문서가 너무 큼 | caller가 skeleton을 먼저 저장한 뒤 같은 흐름에서 fill 또는 bounded fan-out |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
