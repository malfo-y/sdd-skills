---
name: spec-snapshot
description: This skill should be used when the user asks to "spec snapshot", "snapshot spec", "translate spec", "export spec", "스펙 스냅샷", "스펙 번역", or wants to create a timestamped snapshot of the current spec with optional translation.
version: 1.2.0
---

# spec-snapshot

## Goal

현재 `_sdd/spec/` 전체를 타임스탬프 디렉토리에 보존하고, 필요하면 지정한 언어로 번역한 snapshot을 만든다. 원본 스펙은 절대 수정하지 않고, snapshot 루트에는 `summary.md`를 함께 생성해 보관본을 빠르게 훑을 수 있게 한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: `_sdd/spec/` 존재 여부를 확인했다.
- [ ] AC2: `_sdd/snapshots/<timestamp>_<lang>/` 아래에 원본 구조를 보존한 snapshot을 만들었다.
- [ ] AC3: 모든 `.md` 파일이 포함되었다.
- [ ] AC4: 대상 언어가 일관되게 적용되었고, 코드 관련 용어는 원문을 유지했다.
- [ ] AC5: snapshot 루트에 `summary.md`를 생성했다.

## Hard Rules

1. `_sdd/spec/` 원본 파일은 수정하지 않는다.
2. snapshot은 원본 디렉토리 구조를 유지한다.
3. snapshot은 `_sdd/spec/` 아래 모든 `.md` 파일을 포함한다.
4. 모든 `.md` 파일을 포함한다. lowercase canonical `decision_log.md`와 legacy uppercase `DECISION_LOG.md`가 있으면 둘 다 포함한다.
5. 한 snapshot 안의 번역 언어는 일관되어야 한다.
6. 코드 블록, 파일 경로, 심볼명, 명령어, 설정 키는 번역하지 않는다.
7. 파일 수가 많으면 batch 단위 병렬 처리 후 부모가 누락 여부를 검증한다.

## Process

### Step 1: Prepare the Snapshot

- `_sdd/spec/` 존재 확인
- 대상 언어 결정: 지정값 우선, 미지정이면 원본 언어
- 로컬 시간 기준 타임스탬프 생성
- `_sdd/snapshots/<timestamp>_<lang>/` 생성
- 대상 `.md` 파일 목록 수집

### Step 2: Copy or Translate Files

각 파일에 대해:

- 원본 읽기
- 대상 언어가 원본과 같으면 그대로 복사
- 다르면 마크다운 구조는 유지한 채 번역
- 동일한 상대 경로로 저장

파일 수가 많으면:

- main/index 파일 먼저 처리
- 나머지는 2-4개 batch로 나눠 병렬 처리
- 부모가 누락 파일, 경로 보존, 언어 일관성을 검증

### Step 3: Create Snapshot `summary.md`

snapshot 루트에 아래 정보를 담은 `summary.md`를 만든다.

- source path
- snapshot path
- language
- created timestamp
- source commit
- project overview
- component list
- open questions summary

장문이면 다음 순서를 따른다.

1. `summary.md` skeleton/섹션 헤더를 직접 작성
2. 같은 흐름에서 요약 내용을 채움
3. TODO/placeholder를 제거하고 finalize
4. 의존 섹션은 `default`, 독립 요약 섹션은 `worker`로 채운다

### Step 4: Report Completion

사용자에게 아래를 보고한다.

- snapshot 경로
- 대상 언어
- 파일 수
- source commit

## Output Contract

기본 산출물:

- `_sdd/snapshots/<timestamp>_<lang>/...`
- `_sdd/snapshots/<timestamp>_<lang>/summary.md`

`summary.md`에는 최소한 아래가 포함되어야 한다.

- Source
- Snapshot
- Language
- Created
- Source Commit
- Project Overview
- Components
- Open Questions

## Error Handling

| 상황 | 대응 |
|------|------|
| `_sdd/spec/` 없음 | `spec-create` 먼저 권장 |
| snapshot 경로 충돌 | 새 타임스탬프 생성 |
| 빈 스펙 파일 | 빈 파일 그대로 복사 |
| 번역이 애매한 용어 | 원문 병기 |
| 파일이 많음 | batch 병렬 처리 후 검증 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
