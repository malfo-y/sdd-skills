---
name: spec-summary
description: This skill should be used when the user asks to "summarize spec", "spec summary", "show spec overview", "스펙 요약", "스펙 개요", "show spec status", "스펙 현황", "project overview", "프로젝트 개요", "what's the current state", "현재 상태는", or wants a human-readable summary of the current specification for quick understanding.
version: 1.7.0
---

# spec-summary: Exploration-First Spec Summary

현재 스펙을 빠르게 이해하고, 어디를 봐야 하는지 찾을 수 있게 요약한다.

이 스킬의 목적은 스펙을 다시 길게 설명하는 것이 아니다. 사람과 LLM이 다음 질문에 빠르게 답할 수 있는 요약을 만드는 것이다.

- 이 저장소는 무엇을 하는가?
- 시스템 경계는 어디까지인가?
- 어떤 컴포넌트가 어디에 있는가?
- 특정 변경은 어디서 시작해야 하는가?
- 지금 남아 있는 리스크와 미확인 사항은 무엇인가?

## Output

- 기본 출력: `_sdd/spec/SUMMARY.md`
- 선택 출력: `README.md`의 marker block (`<!-- spec-summary:start --> ... <!-- spec-summary:end -->`)
- 형식: 짧고 스캔 가능한 markdown
- 언어: 기본 한국어, 기존 스펙 언어를 존중

## Hard Rules

1. `_sdd/spec/*.md`는 읽기 전용이다. 이 스킬이 수정하는 스펙 파일은 `SUMMARY.md`뿐이다.
2. `README.md`는 사용자가 명시적으로 요청한 경우에만 갱신한다.
3. 기존 `SUMMARY.md`가 있으면 `_sdd/spec/prev/PREV_SUMMARY_<timestamp>.md`로 백업 후 덮어쓴다.
4. 요약은 `index-first`, `path-first`, `change-first` 원칙을 따라야 한다.
5. 정보가 불충분하면 추정으로 단정하지 말고 `Open Questions`에 남긴다.
6. 구형 분할 규칙(`*_API.md`, `*_COMPONENTS.md`)에 의존하지 말고, 메인 스펙의 링크와 책임 기반 파일 구조를 우선 따른다.
7. 핵심 동작 개요와 설계 의도는 1-2문장으로 짧게 남긴다.

## Input Sources

### Primary

- 메인 스펙: `_sdd/spec/main.md` 또는 `_sdd/spec/<project>.md`
- 메인 스펙에서 링크된 컴포넌트 스펙
- 필요 시 `_sdd/spec/DECISION_LOG.md`

### Secondary

- `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- `_sdd/implementation/IMPLEMENTATION_PROGRESS*.md`
- `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
- `_sdd/env.md`
- `README.md` (README sync 요청 시만)

## Summary Shape

요약은 아래 우선순위를 따른다.

1. `Goal`에서 `Project Snapshot`, `Key Features`, `Non-Goals`
2. `Architecture Overview`에서 `System Boundary`, `Repository Map`, `Runtime Map`
3. `Component Details`에서 `Component Index`, `Overview`
4. `Usage Examples` 또는 동등 섹션에서 `Common Change Paths`
5. 진행 상태가 있다면 간단한 status snapshot
6. `Identified Issues & Improvements`와 `Open Questions`

좋은 요약은 "무엇을 하는가"와 함께 "어디를 보면 되는가"를 보여준다.

## Process

### Step 1: Locate the spec entry point

1. `_sdd/spec/main.md`를 먼저 찾는다.
2. 없으면 `_sdd/spec/<project>.md`를 찾는다.
3. 생성물과 백업 파일은 제외한다.
   - `SUMMARY.md`
   - `SPEC_REVIEW_REPORT.md`
   - `prev/PREV_*.md`
4. 메인 스펙의 링크를 따라 관련 컴포넌트 스펙만 읽는다.
5. 링크가 불명확하면 같은 디렉터리의 책임 기반 파일(`auth.md`, `jobs.md`)을 우선 후보로 삼고, 선택 근거를 `Open Questions`에 적는다.

### Step 2: Extract navigation-critical information

아래를 우선 추출한다.

- 프로젝트 한 문단 요약
- 시스템 경계와 외부 의존
- 중요한 디렉터리/파일 지도
- 주요 런타임 흐름
- 핵심 컴포넌트와 실제 경로
- 자주 하는 변경의 시작 지점
- 현재 상태를 보여주는 marker/implementation 정보
- 리스크, 제약, 미확인 사항

### Step 3: Build the summary

기본 섹션 순서는 아래를 따른다.

1. `Project Snapshot`
2. `System Boundary`
3. `Repository Map`
4. `Runtime Map`
5. `Component Index`
6. `Current Status`
7. `Common Change Paths`
8. `Risks / Improvements`
9. `Open Questions`
10. `Quick Reference`

자세한 narrative보다 탐색 가능한 정보와 실제 경로를 우선한다.

### Step 4: Optional README sync

사용자가 README 갱신을 요청했을 때만 marker block을 갱신한다.

- marker가 있으면 block만 교체
- marker가 없으면 첫 H1 뒤 또는 파일 끝에 안전하게 삽입
- README 본문 전체를 재작성하지 않는다

## Context Management

| 상황 | 전략 |
|------|------|
| 메인 스펙 500줄 이하 | 전체 읽기 |
| 메인 스펙 500줄 초과 | TOC/상위 섹션 먼저, 필요한 컴포넌트만 선택 읽기 |
| 컴포넌트 스펙 다수 | 링크된 파일 우선, 최대 3-5개 핵심 파일만 읽기 |
| 구현 문서 많음 | 최신 진행 문서 1개 + 최신 리뷰 1개만 우선 반영 |

## Output Requirements

요약에는 가능하면 아래가 포함되어야 한다.

- 실제 파일 경로
- 주요 컴포넌트 이름과 책임
- `Runtime Map` 요약
- 주요 컴포넌트의 짧은 동작 개요 또는 설계 의도
- `Common Change Paths`
- 현재 리스크 또는 개선 포인트
- `Open Questions`

진행률 퍼센트나 버전은 스펙이 실제로 제공할 때만 넣는다. 없으면 억지로 만들지 않는다.

## Report Template

상세 형식은 [`references/summary-template.md`](references/summary-template.md)를 따른다.

## Example

예시는 [`examples/summary-output.md`](examples/summary-output.md)를 참고한다.
