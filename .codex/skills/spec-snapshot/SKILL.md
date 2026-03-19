---
name: spec-snapshot
description: This skill should be used when the user asks to "spec snapshot", "snapshot spec", "translate spec", "export spec", "스펙 스냅샷", "스펙 번역", or wants to create a timestamped snapshot of the current spec with optional translation.
version: 1.0.0
---

# Spec Snapshot — 스펙 스냅샷 생성 및 번역

현재 `_sdd/spec/` 전체를 특정 언어로 번역하여 타임스탬프 디렉토리에 저장한다.
번역 없이 원본 언어 그대로 스냅샷을 찍는 용도로도 사용할 수 있다.

## 사용 예시

```text
spec snapshot en          # 영어로 번역 스냅샷
spec snapshot ja          # 일본어로 번역 스냅샷
spec snapshot ko          # 한국어 원본 그대로 스냅샷
spec snapshot             # 원본 언어 그대로 스냅샷 (기본값)
translate spec to en      # 현재 스펙을 영어 스냅샷으로 내보내기
export spec snapshot      # 번역 없이 현재 스펙을 스냅샷으로 보관
```

## Hard Rules

1. **구현 코드 수정 금지**: `src/`, `tests/` 등 구현 코드 파일은 수정하지 않는다.
2. **원본 스펙 수정 금지**: `_sdd/spec/` 원본 파일은 절대 수정하지 않는다. 읽기만 한다.
3. **구조 보존**: 원본 `_sdd/spec/`의 디렉토리 구조(subdirectory 포함)를 스냅샷에 그대로 유지한다.
4. **전체 복사**: `_sdd/spec/` 아래 모든 `.md` 파일을 스냅샷에 포함한다 (`DECISION_LOG.md` 포함, `prev/` 백업 디렉토리 제외).
5. **SUMMARY.md 생성**: 스냅샷 디렉토리 루트에 `SUMMARY.md`를 생성한다.
6. **번역 일관성**: 한 스냅샷 내 모든 파일은 동일한 대상 언어로 번역한다.
7. **도메인 용어 보존**: 코드 경로, 심볼명, 명령어, 설정 키 등 코드 관련 용어는 번역하지 않고 원문 그대로 유지한다.

## Codex Parallel Snapshot Contract

멀티파일 스냅샷은 Codex-native fan-out으로 처리한다.

- 파일 수가 3개 이하이면 순차 처리
- 파일 수가 4개 이상이면 파일 목록을 겹치지 않는 batch로 분할
- 각 batch는 `spawn_agent(agent_type="worker")`로 병렬 처리
- 부모는 `wait_agent(...)`로 모든 batch를 수집한 뒤 누락 파일/경로 보존 여부를 검증한다
- `SUMMARY.md`는 모든 batch 완료 후 부모가 생성하거나 단일 `write_phased` agent에 위임한다

## Output Structure

```text
_sdd/snapshots/
└── 2026-03-09T14-30_en/
    ├── SUMMARY.md
    ├── main.md
    ├── DECISION_LOG.md
    ├── auth.md
    ├── billing/
    │   ├── billing.md
    │   └── subscription.md
    └── ...
```

- 타임스탬프 형식: `YYYY-MM-DDTHH-MM` (로컬 시간)
- 언어 코드: ISO 639-1 (`en`, `ja`, `zh`, `ko`, `es`, `de`, `fr` 등)

## Process

### Step 1: 준비

**Tools**: `Glob`, `Read`, `Bash`

1. `_sdd/spec/` 존재 여부를 확인한다. 없으면 에러 보고 후 종료한다.
2. 대상 언어를 결정한다.
   - 사용자가 언어 코드를 지정하면 해당 언어를 사용한다.
   - 미지정 시 원본 스펙의 언어를 감지하여 그대로 사용한다.
3. 로컬 시간 기준 타임스탬프를 생성한다.
4. 스냅샷 디렉토리 `_sdd/snapshots/<timestamp>_<lang>/`를 생성한다.
5. `_sdd/spec/` 아래 모든 `.md` 파일 목록을 수집한다. 단, `prev/`는 제외한다.

### Step 2: 스펙 파일 번역 및 저장

**Tools**: `Read`, `Write`, `spawn_agent`, `wait_agent`

기본 절차:

1. 원본 파일을 읽는다.
2. 대상 언어로 번역한다. 원본 언어와 동일하면 번역 없이 복사한다.
   - 마크다운 구조(헤딩, 테이블, 코드블록, 링크)는 그대로 유지한다.
   - 코드블록 내용은 번역하지 않는다.
   - 파일 경로, 심볼명, 명령어, 설정 키는 번역하지 않는다.
   - 섹션 헤딩은 번역하되, 문서 탐색이 깨지지 않도록 일관성을 유지한다.
3. 원본과 동일한 상대 경로에 저장한다.

파일 처리 순서:
1. `main.md` 또는 프로젝트 메인 스펙
2. 나머지 컴포넌트 스펙 파일
3. `DECISION_LOG.md`

병렬 처리 규칙:

```text
IF total_spec_files <= 3:
  → 순차 처리
ELSE:
  1. main/index 파일은 먼저 처리한다.
  2. 나머지 파일을 2-4개 batch로 분할한다.
  3. batch별로 worker를 병렬 spawn한다.
  4. wait_agent로 모두 수집한다.
  5. 누락 파일/경로 보존/언어 일관성 검증 후 완료 처리한다.
```

예시:

```text
batch_1 = [api.md, database.md]
batch_2 = [billing/overview.md, billing/subscription.md]

worker_1 = spawn_agent(
  agent_type="worker",
  message="다음 snapshot 파일만 번역/복사하세요: [batch_1 상대 경로 목록]
  출력 루트: _sdd/snapshots/<timestamp>_<lang>/
  구조와 상대 경로는 원본 그대로 유지하세요."
)

worker_2 = spawn_agent(
  agent_type="worker",
  message="다음 snapshot 파일만 번역/복사하세요: [batch_2 상대 경로 목록]
  출력 루트: _sdd/snapshots/<timestamp>_<lang>/
  구조와 상대 경로는 원본 그대로 유지하세요."
)

wait_agent(ids=[worker_1, worker_2], timeout_ms=1800000)
```

### Step 3: SUMMARY.md 생성

**Tools**: `Write`, `Bash`, `spawn_agent`, `wait_agent`

스냅샷 디렉토리 루트에 `SUMMARY.md`를 생성한다. 포함 내용:

```markdown
# Spec Snapshot Summary

- **Source**: `_sdd/spec/`
- **Snapshot**: `_sdd/snapshots/<timestamp>_<lang>/`
- **Language**: <대상 언어>
- **Created**: <날짜 시간>
- **Source Commit**: <git rev-parse --short HEAD 결과>

## Project Overview

<메인 스펙의 Goal 섹션 요약 — 2-3문장>

## Components

| Component | File | Description |
|-----------|------|-------------|
| ... | ... | ... |

## Open Questions

<Open Questions 섹션 요약>
```

`SUMMARY.md`가 장문이 되면 `spawn_agent(agent_type="write_phased")`로 위임하고 `wait_agent`로 수집한다.

### Step 4: 완료 보고

스냅샷 생성 완료 후 아래 정보를 출력한다:

| 항목 | 내용 |
|------|------|
| 스냅샷 경로 | `_sdd/snapshots/<timestamp>_<lang>/` |
| 대상 언어 | (언어명) |
| 파일 수 | N개 |
| 원본 커밋 | (short hash) |

## Error Handling

| 상황 | 대응 |
|------|------|
| `_sdd/spec/` 미존재 | 에러 보고: "스펙이 없습니다. `spec-create`를 먼저 실행하세요." |
| `_sdd/snapshots/` 미존재 | `mkdir -p`로 자동 생성 |
| 동일 타임스탬프 디렉토리 존재 | 덮어쓰기 대신 파일 수집/생성 시각을 다시 확인하고, 필요하면 새 타임스탬프를 생성 |
| 빈 스펙 파일 | 빈 파일 그대로 복사 |
| 번역 중 불확실한 용어 | 원문을 괄호로 병기: `invariant (불변 조건)` |

## Integration with Other Skills

- **spec-summary**: `SUMMARY.md` 생성 시 요약 로직 참고
- **spec-create**: 스냅샷 대상 스펙의 원본 생성 스킬
- **spec-rewrite**: 리라이트 전후 스냅샷 비교에 활용 가능
- **spec-update-done**: 구현 반영 후 기준선 스냅샷 보관에 활용 가능
