# Output Contract

기본 출력 파일은 회의별 마크다운 문서다.

기본 경로:

- 사용자 지정 디렉토리
- 없으면 `_sdd/meeting-analysis/meeting_<slug>_<yyyy_mm_dd>.md`

## Required Structure

```markdown
# Meeting Analysis: <title>

## Original Source Links
- Wiki:
- Calendar:
- Docs/Drive:
- Meet:

## Meeting Identity
- Title:
- Date/Time:
- Timezone:
- Confidence:

## Source Mapping
- Wiki:
- Calendar:
- Docs/Drive:
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

## Published To Wiki Child
- Parent Wiki:
- Child Page Title:
- Child Page URL:
- Publish Status:
```

## Default Analysis Scope

기본 출력에는 아래가 포함된다.

- 핵심 요약
- 액션 아이템
- 결정 사항
- 열린 질문
- 비평
- 다음 액션 제안

wiki child page 발행이 수행된 경우에는 아래도 추가한다.

- parent wiki 링크
- child page 제목/URL
- publish 성공 여부 또는 실패 사유

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

## Source Link Placement Rule

- 전체 분석 문서를 저장할 때는 `Original Source Links`를 제목 바로 아래에 둔다.
- `Original Source Links`에는 가능하면 원본 URL을 그대로 적는다.
- `Wiki`, `Calendar`, `Docs/Drive`는 값이 있으면 항상 채우고, `Meet`는 보조 링크로 유지한다.
- 같은 링크를 아래 `Source Mapping`과 `Sources`에서 다시 참조해도 괜찮지만, 상단 링크 블록은 빠른 접근용 canonical shortcut으로 취급한다.

## Wiki Child Publish Rule

- wiki 입력이 있고 사용자가 명시적으로 발행을 요청한 경우에만 child page를 만든다.
- child page 본문은 로컬 분석 결과와 의미상 동일해야 한다.
- 발행 실패 시 로컬 분석 파일은 유지하고, `Published To Wiki Child` 섹션에 실패 사유를 남긴다.
