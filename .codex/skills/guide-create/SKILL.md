---
name: guide-create
description: This skill should be used when the user asks to "guide create", "create guide", "feature guide", "write guide", "가이드 작성", "기능 가이드", "가이드 문서 만들어줘", or wants to generate an implementation/review guide document for a specific feature from spec and code context.
version: 2.4.0
---

# guide-create

## Goal

특정 기능에 대한 deep-dive 기술 가이드를 `_sdd/guides/guide_<slug>.md`에 만든다. 글로벌 스펙이 프로젝트 전체 SSOT라면, guide는 기능 단위의 usage scenario, API reference, implementation guidance를 더 구체적으로 풀어내는 companion document다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: 대상 feature를 확정하고 output slug를 결정했다.
- [ ] AC2: `_sdd/spec/`에서 feature 관련 근거를 수집했다.
- [ ] AC3: 코드 evidence와 citation index를 모아 guide의 근거를 만들었다.
- [ ] AC4: `_sdd/guides/guide_<slug>.md`를 생성하거나 갱신했다.
- [ ] AC5: guide에 §1~§5 required sections가 포함되고, spec/code가 read-only로 유지되었다.
- [ ] AC6: example/template 자산은 유지되고, 본문은 guide 생성 계약을 concise하게 설명한다.

## SDD Lens

- guide는 스펙을 대체하지 않는다. 스펙을 바탕으로 특정 기능을 더 자세히 설명하는 파생 문서다.
- spec-first로 작성하되, 코드는 naming, evidence, symbol reference를 구체화하는 데 사용한다.
- unsupported behavior는 확정 사실처럼 쓰지 않고 assumption/unknown으로 남긴다.

## Companion Assets

- `references/output-format.md`
- `references/template-compact.md`
- `references/tool-and-gates.md`
- `examples/feature-guide-example.md`
- `examples/feature-guide-example-high.md`
- `examples/feature-guide-example-low.md`

## Hard Rules

1. `_sdd/spec/`, 코드, 설정, 테스트는 읽기 전용이다.
2. 생성 가능한 파일은 `_sdd/guides/guide_<slug>.md`와 그 backup뿐이다.
3. feature-only 스킬이다. 여러 feature가 감지되면 feature별로 guide를 나눈다.
4. 기본은 non-interactive다. 방향이 크게 달라지는 ambiguity가 아니면 deterministic default로 계속 진행한다.
5. spec를 primary source로 사용하고, 코드는 citation과 구현 디테일 보강에 사용한다.
6. 확정할 수 없는 정보는 assumption/unknown으로 표시한다.
7. 기존 guide를 덮어쓸 때는 `_sdd/guides/prev/PREV_guide_<slug>_<timestamp>.md`로 백업한다.
8. 장문 guide는 먼저 `write_skeleton` agent로 skeleton을 만든다. 반환값이 `SKELETON_ONLY`이면 이 skill이 `default` 또는 `worker` agent로 남은 섹션을 채운다.

## Input Sources

1. 사용자 요청
2. `_sdd/spec/main.md` 또는 대표 spec
3. linked / split sub-spec
4. 관련 코드, 테스트, 인터페이스, 스키마
5. `_sdd/env.md` (실행/검증 맥락이 필요할 때만)

## Process

### Step 1: Identify the Feature

- feature 후보를 추출
- output slug를 영문으로 정규화
- 다중 feature면 파일을 나눌 계획을 세움

### Step 2: Gather Spec Context

다음을 수집한다.

- feature description
- 관련 제약과 acceptance-style wording
- 아키텍처 맥락
- related scenarios and interfaces

usable spec가 없으면:

- spec-create 실행 또는 low-confidence 진행 중 하나를 선택하게 할 수 있다

### Step 3: Gather Code Evidence

다음을 찾는다.

- 관련 구현 파일
- 테스트
- 인터페이스 / 타입 / 스키마
- 핵심 함수 / 메서드 / 컴포넌트

그 후 `[filepath:symbol]` 형식 citation index를 만든다.

### Step 4: Resolve Gaps Conservatively

정보가 부족하면 아래 원칙을 따른다.

- feature name unclear → spec heading / user phrase에서 도출
- user value unclear → spec의 goal/problem에서 요약
- implementation rule unclear → 코드베이스 컨벤션 우선
- unsupported behavior → confirmed 사실처럼 쓰지 않음

### Step 5: Write the Guide

guide는 아래 required sections를 가진다.

- §1 Background & Motivation
- §2 Core Design
- §3 Usage Scenario Guide
- §4 API Reference
- §5 Implementation Guide

optional appendix:

- spec references
- code references
- assumptions / open points

코드 근거가 있으면 본문에 `[filepath:symbol]` 인라인 citation을 사용한다.

guide가 길면 다음 순서를 따른다.

1. `write_skeleton` agent로 guide skeleton 생성
2. 반환값이 `COMPLETE`면 그대로 사용
3. 반환값이 `SKELETON_ONLY`면 이 skill이 `Sections Remaining`을 기준으로 fill 수행
4. 의존 섹션은 `default`, 독립 시나리오/API 섹션은 `worker`로 채운다

### Step 6: Save with Backup Semantics

- `_sdd/guides/` 준비
- 기존 guide가 있으면 backup 생성
- 새 guide 저장
- 생성 경로를 사용자에게 보고

## Output Contract

기본 산출물:

- `_sdd/guides/guide_<slug>.md`

required sections:

- §1 배경 및 동기
- §2 핵심 설계
- §3 사용 시나리오 가이드
- §4 API 레퍼런스
- §5 구현 가이드

guide는 spec보다 더 actionable해야 하며, 구현자/리뷰어가 바로 사용할 수 있어야 한다.

## Error Handling

| 상황 | 대응 |
|------|------|
| usable spec 없음 | spec-create 권장 또는 low-confidence guide로 진행 |
| feature가 여러 개 | feature별 guide 분리 |
| 코드 근거 부족 | low-confidence / unknown 표시 |
| citation 후보 부족 | best-effort references만 남기고 한계를 명시 |
| 문서가 너무 김 | `write_skeleton` 사용 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
