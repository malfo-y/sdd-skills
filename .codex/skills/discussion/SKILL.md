---
name: discussion
description: This skill should be used when the user asks to "discuss", "discussion", "토론", "토론하자", "let's discuss", "brainstorm", "논의", "의견 나누기", or wants a structured iterative discussion with research support.
version: 1.1.0
---

# discussion

## Goal

구조화된 반복 토론으로 주제를 좁히고, 필요한 맥락을 수집하며, 최종적으로 `_sdd/discussion/discussion_<title>.md`에 토론 요약을 저장한다. 구현이나 스펙 수정은 하지 않고, 후속 스킬이 사용할 수 있는 결정과 open question을 정리하는 데 집중한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: 토론 주제와 범위를 명확히 했다.
- [ ] AC2: 필요한 로컬 맥락 또는 최신 외부 사실을 수집했다.
- [ ] AC3: 반복 토론 중간에 핵심 논점, 결정, 미결 질문을 추적했다.
- [ ] AC4: `_sdd/discussion/discussion_<title>.md`를 생성했다.
- [ ] AC5: 최종 요약에 논점, 결정, open question, action item이 포함되었다.

## Companion Assets

- `references/discussion-question-guide.md`
- `examples/sample-discussion-session.md`

## Hard Rules

1. 이 스킬은 interactive-only다. `request_user_input`을 사용할 수 없으면 즉시 중단한다.
2. 코드, 스펙, 설정 파일은 수정하지 않는다. 생성 가능한 파일은 `_sdd/discussion/discussion_<title>.md` 하나뿐이다.
3. Step 1-3은 읽기 전용 탐색만 사용한다.
4. 모든 질문에는 `정리/종료` 성격의 선택지를 넣는다.
5. 라운드당 질문은 정확히 1개만 한다.
6. 최신성이나 사실 검증이 필요한 내용은 웹 또는 로컬 근거로 먼저 확인한다.
7. 출력 언어와 저장 파일 언어는 사용자의 활성 입력 언어를 따른다.

## Process

### Step 1: Define the Topic

- 사용자 요청에서 토픽이 이미 있으면 재진술 후 범위를 좁히는 질문 1개를 한다.
- 불명확하면 카테고리 수준에서 묻고, 최대 2라운드 안에 범위를 정한다.
- 범위를 정하지 못하면 이유를 설명하고 중단한다.

### Step 2: Gather Context

토픽 유형에 따라 필요한 맥락을 수집한다.

- 코드베이스 관련: 관련 파일, 패턴, 의존성
- 아키텍처/기술 선택: 로컬 구조 + 공식 자료/1차 자료
- 기타 주제: 사용자 맥락 기준으로 탐색

이후 짧은 context summary를 제시한다.

### Step 3: Run Iterative Discussion

각 라운드에서 다음을 반복한다.

1. 핵심 분기 하나를 질문
2. 답변과 수집 맥락을 연결해 정리
3. 논점 / 결정 / 미결 질문 / action item을 갱신

중간 요약은 필요할 때만 짧게 제시한다.

종료 조건:

- 사용자가 `정리/종료`를 선택
- 충분한 방향성이 확보됨
- 최대 라운드 도달

**Gate 3→4**: 미결 질문(open_questions)을 확인한다.
- 0건 → Step 4 진행
- 1건+ → 미결 질문 목록을 제시하고 추가 논의 여부를 확인한다. 추가 논의 선택 시 Step 3 루프 복귀, 그대로 정리 선택 시 Step 4 진행.

### Step 4: Write the Discussion Summary

`_sdd/discussion/discussion_<title>.md`에 아래를 저장한다.

- 핵심 논점
- 결정 사항
- 미결 질문
- 실행 항목
- 리서치 결과 요약
- sources
- 토론 흐름

파일명은 영문 slug를 사용하고, `_sdd/discussion/`가 없으면 생성한다.

## Output Contract

기본 산출물:

- `_sdd/discussion/discussion_<title>.md`

최종 요약에는 최소한 아래가 포함되어야 한다.

- 날짜
- 라운드 수
- 핵심 논점
- 결정 사항
- open questions
- action items
- sources

## Error Handling

| 상황 | 대응 |
|------|------|
| `request_user_input` 불가 | 즉시 중단 |
| 토픽 불명확 | 최대 2라운드 범위 질문 후 중단 |
| 로컬 맥락 부족 | 범위를 좁히거나 현재 정보 기준으로 계속할지 확인 |
| 외부 리서치 실패 | 실패 사실을 밝히고 수집된 맥락만으로 진행 |
| 최대 라운드 도달 | 자동으로 요약 단계로 이동 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

