---
name: meeting-analysis
description: This skill should be used when the user wants to gather and analyze meeting materials from VCGA wiki notes, Google Meet links, Google Calendar events, Google Docs meeting records, or Google Drive file URLs, then produce a merged summary, critique, and next actions.
version: 0.1.1
---

# meeting-analysis

## Goal

VCGA 위키 회의록, Google Meet 링크, Google Calendar 이벤트, Google Docs 회의록 문서, Google Drive 파일 URL 중 하나 이상을 입력으로 받아 관련 자료를 연결하고, 필요하면 추가 근거를 수집한 뒤 하나의 분석 결과로 정리한다. 기본 결과물은 회의별 요약 파일이며, 핵심 요약, 액션 아이템, 쟁점, 비평, 다음 액션 제안을 포함한다. 다만 사용자가 존재 확인이나 자료 수집만 명시적으로 요청하면 그 범위에서 멈출 수 있다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: 입력 링크 유형(`wiki`, `meet`, `calendar`, `doc`, `drive`, 복합 입력)을 판별했다.
- [ ] AC2: 관련 회의 자료를 최소 1개 이상 수집했고, 수집 실패 시 실패 사유와 fallback 결과를 기록했다.
- [ ] AC3: 수집 결과를 정규화된 evidence pack으로 정리했다.
- [ ] AC4: 최종 산출물에 통합 요약, 액션 아이템, 비평, 다음 액션 제안, 출처가 포함되었다.
- [ ] AC5: 위키와 미팅 기록이 상충할 경우 출처별 병렬 표기와 판단 보류 원칙을 지켰다.
- [ ] AC6: 결과를 회의별 파일로 저장했거나, 저장 불가 시 그 이유와 수동 저장 위치를 명시했다.

## Companion Assets

- `references/routing-and-matching.md`
- `references/evidence-pack-contract.md`
- `references/output-contract.md`
- `examples/example-request-flow.md`

## Hard Rules

1. 이 스킬은 회의 자료 분석용이다. 위키 페이지나 캘린더 이벤트를 수정하지 않는다.
2. 위키 자료는 [`vcga-wiki`](/Users/hyunjoonlee/.agents/skills/vcga-wiki/SKILL.md)를 통해 가져오고, Google Calendar/Drive 자료는 해당 capability를 우선 사용한다.
3. 단일 입력은 링크 유형별 시작점으로 처리한다. 복합 입력은 먼저 같은 회의 이벤트 축을 고정한 뒤 다른 자료를 연결한다.
4. 기본 매칭은 시간 우선이다. 시간 매칭 실패 시 `Meet 코드 -> 제목 유사도 -> 사용자 확인` 순서로 fallback 한다.
5. 위키와 미팅 기록이 모두 있으면 둘 다 사용한다. 하나를 절대 기준본으로 강제하지 않는다.
6. 원문/증거 수집은 서브에이전트로 분리할 수 있다. 최종 매칭 판단, 병합, 요약, 비평은 메인 에이전트가 담당한다.
7. 서브에이전트는 긴 자유서술 대신 정규화된 evidence pack으로만 결과를 반환한다.
8. 기본 출력은 항상 저장한다. 단, 사용자가 존재 확인 또는 자료 찾기만 명시적으로 요청하면 narrow mode로 처리하고 저장을 생략할 수 있다. 저장 위치는 사용자 지정 디렉토리를 우선하고, 없으면 `_sdd/meeting-analysis/meeting_<slug>_<date>.md`를 기본 경로로 사용한다.
9. 기본 출력에는 비평과 다음 액션 제안까지 포함한다. 추가 리서치는 사용자가 요청할 때만 확장한다.
10. 상충하는 정보가 있으면 판단을 서두르지 않고, 출처별 병렬 표기와 근거를 함께 제시한다.

## Input Sources

1. 사용자 요청
2. VCGA wiki page URL / page identifier
3. Google Meet URL
4. Google Calendar event URL or event metadata
5. Google Docs meeting notes URL
6. Google Drive file URL
7. 이미 저장된 회의 요약 파일이 있으면 그 파일

## Task Mode Detection

먼저 사용자의 요청 모드를 판별한다.

- `existence-check`: 관련 회의록/문서가 있는지만 확인
- `fetch`: 관련 자료를 연결하고 원문/링크만 가져오기
- `summary`: 연결된 자료를 요약
- `compare`: 위키와 미팅 기록의 공통점/차이점 정리
- `critique`: 요약 + 비평 + 다음 액션 제안

명시적 지시가 없으면 `summary` 이상으로 진행하고, 기본값은 `critique`다.

## Routing

상세 규칙은 `references/routing-and-matching.md`를 따른다.

### Single Input

- `wiki` 링크만 들어오면: 위키 페이지를 먼저 읽고, 제목/시간/본문 단서로 관련 이벤트와 문서를 연결한다.
- `meet` 링크만 들어오면: Calendar 이벤트를 먼저 찾고, 그 이벤트 기준으로 Drive 문서와 위키를 연결한다.
- `calendar` 링크만 들어오면: 해당 이벤트를 기준점으로 사용하고, 관련 Drive 문서와 위키를 찾는다.
- `doc` 링크만 들어오면: 문서를 먼저 읽고, 제목/작성 시각으로 Calendar/위키를 역추적한다.
- `drive` 링크만 들어오면: Drive 파일 메타데이터와 본문을 먼저 읽고, 제목/작성 시각/본문 단서로 Calendar/위키를 역추적한다.

### Multiple Inputs

- `wiki + meet/calendar/doc/drive`가 함께 들어오면: 먼저 같은 회의 이벤트를 고정하고, 그에 대응하는 위키와 문서를 붙인다.
- 서로 다른 회의로 보이는 후보가 섞이면: 상위 후보 2-3개와 근거를 제시하고 사용자 확인을 받는다.

## Process

### Step 1: Normalize the Input

- 링크/문자열 입력에서 URL 종류를 판별한다.
- `docs.google.com/...`와 `drive.google.com/...`는 둘 다 Drive-backed document/file 입력으로 처리하되, Docs native 문서인지 일반 Drive 파일인지 구분한다.
- 제목, 날짜, 시간, 시간대, Meet 코드 같은 직접 단서를 분리한다.
- 이미 충분한 식별자가 있으면 후속 탐색 범위를 줄인다.

### Step 2: Collect Evidence

소스별로 필요한 자료를 수집한다.

- `wiki`: `vcga-wiki`로 페이지 가져오기
- `meet`/`calendar`: Calendar capability로 이벤트 식별
- `doc`/`drive`: Google Drive capability로 문서 식별 및 내용 확보

`drive` 입력 처리 원칙:

- 가능한 한 URL에서 파일 ID를 추출해 메타데이터와 본문을 바로 확보한다.
- Google Docs native 문서면 문서 본문을 읽는다.
- 일반 Drive 파일이면 가능한 텍스트 표현을 우선 확보하고, 텍스트 추출이 약하면 그 사실을 confidence에 반영한다.
- Drive 폴더 URL은 직접 입력으로 받더라도 단일 회의록 시작점으로는 취급하지 않고, 필요한 경우 후보 문서 목록 탐색으로만 사용한다.

독립적인 소스 수집이 2건 이상이면 필요 시 서브에이전트를 사용한다.

#### Subagent Rule

- 서브에이전트 책임:
  - 위키 원문/메타데이터 수집
  - 캘린더 이벤트 후보 탐색
  - Drive/Docs 회의록 후보 탐색
- 메인 에이전트 책임:
  - 후보 매칭 확정
  - 출처 간 충돌 해석
  - 최종 요약/비평/다음 액션 생성

### Step 3: Normalize to Evidence Packs

수집한 각 소스를 `references/evidence-pack-contract.md`의 형식으로 정리한다.

최소 필드:
- source_type
- source_url
- title
- event_time
- extracted_facts
- key_excerpt
- confidence_note

### Step 4: Match and Merge

- 시간 기준으로 1차 매칭한다.
- 실패 시 `Meet 코드 -> 제목 유사도 -> 사용자 확인`을 적용한다.
- Docs/Drive 파일의 생성/수정 시각은 독립 fallback 단계가 아니라 제목/시간 판단을 보강하는 힌트로만 사용한다.
- 위키와 미팅 기록이 모두 있으면 공통 사실과 상충 사실을 분리한다.
- 상충 사실은 출처별 병렬 표기로 유지한다.

### Step 5: Analyze

기본 분석 결과는 아래를 포함한다.

- 통합 요약
- 액션 아이템
- 결정 사항
- 열린 질문
- 비평
- 다음 액션 제안

`비평`에는 가능하면 아래 항목을 포함한다.

- 논의의 선명도: 회의 목표, 결정, 액션 아이템이 충분히 명확한지
- 근거의 질: 주장이나 결정이 데이터, 실험, 합의 근거와 연결되는지
- 누락된 관점: 리스크, 대안, 검증 계획, 담당자/기한 등 빠진 요소가 있는지
- 출처 간 일관성: 위키 회의록과 미팅 기록 사이에 충돌이나 해석 차이가 있는지
- 실행 가능성: 지금 회의 결과만으로 실제 다음 행동에 들어갈 수 있는 상태인지
- 우선순위 감각: 지금 당장 할 일과 후속 검토 과제가 구분되어 있는지

추가 리서치는 사용자가 요청할 때만 수행한다.

### Step 6: Save

- 사용자 지정 디렉토리가 있으면 그 위치를 사용한다.
- 없으면 `_sdd/meeting-analysis/`를 생성한다.
- 파일명은 `meeting_<slug>_<yyyy_mm_dd>.md`를 기본으로 사용한다.
- 같은 회의의 기존 파일이 있으면 덮어쓰기보다 갱신/append 여부를 먼저 판단하고, 확신이 낮으면 사용자 확인을 받는다.

## Output Contract

상세 형식은 `references/output-contract.md`를 따른다.

기본 산출물:

- `_sdd/meeting-analysis/meeting_<slug>_<yyyy_mm_dd>.md`

필수 섹션:

1. 회의 식별 정보
2. Source Mapping
3. 통합 요약
4. 액션 아이템
5. 결정 사항 / 열린 질문
6. 비평
7. 다음 액션 제안
8. 충돌/불일치 메모
9. Sources

## Error Handling

| 상황 | 대응 |
|------|------|
| 위키만 있고 시간 정보 부족 | 제목/본문 단서 기반으로 후보를 좁히고, 불확실하면 후보 제시 후 확인 |
| Meet 링크만 있고 Calendar 매칭 실패 | Meet 코드, 제목 유사도 순으로 후보를 찾고, Docs 생성/수정 시각은 보조 힌트로만 사용한다 |
| Docs/Drive 문서는 찾았지만 이벤트를 못 찾음 | 문서 단독 근거로 분석을 진행하고 confidence를 낮춤 |
| Drive URL은 열렸지만 본문 추출이 약함 | 메타데이터와 파일명 중심으로 후보를 연결하고, 본문 신뢰도 저하를 명시 |
| 위키와 미팅 기록이 상충 | 출처별 병렬 표기, 판단 보류, 추가 확인 포인트 제시 |
| 관련 자료가 하나도 없음 | 실패 원인과 시도한 fallback, 사용자가 추가로 줄 수 있는 단서 보고 |
| 저장 위치 생성 실패 | 응답 본문에 동일 내용을 제공하고, 저장 실패 사유를 명시 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
