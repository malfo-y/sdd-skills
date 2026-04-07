# Output Contract

기본 출력 파일은 회의별 마크다운 문서다.

기본 경로:

- 사용자 지정 디렉토리
- 없으면 `_sdd/meeting-analysis/meeting_<slug>_<yyyy_mm_dd>.md`

## Required Structure

```markdown
# Meeting Analysis: <title>

## Meeting Identity
- Title:
- Date/Time:
- Timezone:
- Confidence:

## Source Mapping
- Wiki:
- Calendar:
- Docs:
- Meet:

## Unified Summary
- ...

## Action Items
- [ ] ...

## Decisions
- ...

## Open Questions
- ...

## Critique
- Discussion clarity:
- Evidence quality:
- Missing angles:
- Cross-source consistency:
- Execution readiness:
- Priority judgment:

## Next Actions
- ...

## Conflict Notes
- Topic A:
  - Wiki:
  - Meeting record:
  - Note:

## Sources
- ...
```

## Default Analysis Scope

기본 출력에는 아래가 포함된다.

- 핵심 요약
- 액션 아이템
- 결정 사항
- 열린 질문
- 비평
- 다음 액션 제안

추가 리서치는 기본 포함이 아니다. 사용자가 요청하면 별도 섹션으로 확장한다.

## Critique Checklist

`Critique` 섹션에는 가능하면 아래 항목을 bullet로 채운다.

- `Discussion clarity`: 회의 목표, 결정, 액션 아이템이 명확한지
- `Evidence quality`: 주장/결정이 어떤 근거에 기대는지, 근거가 충분한지
- `Missing angles`: 빠진 리스크, 대안, 검증 계획, 담당자/기한이 있는지
- `Cross-source consistency`: 위키와 미팅 기록이 서로 얼마나 일치하는지
- `Execution readiness`: 지금 상태로 바로 실행 가능한지, 추가 정리가 필요한지
- `Priority judgment`: 지금 바로 해야 할 일과 나중에 검토할 일을 구분했는지

## Narrow Modes

사용자가 명시적으로 아래만 원하면 전체 분석으로 확장하지 않는다.

- 존재 확인만 원함
- 관련 링크/문서 목록만 원함
- 원문 연결만 원함

이 경우 저장은 선택 사항이며, 기본 분석 파일 생성을 생략할 수 있다.
