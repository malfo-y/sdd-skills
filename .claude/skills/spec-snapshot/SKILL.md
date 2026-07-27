---
name: spec-snapshot
description: |
  Create a translated snapshot of the current spec.
  Copies _sdd/spec/ to _sdd/snapshots/<timestamp>_<lang>/ with optional translation.
  Trigger phrases: "spec snapshot", "스펙 스냅샷", "snapshot spec", "translate spec", "스펙 번역", "export spec"
user_invocable: true
---

# Spec Snapshot — 스펙 스냅샷 생성 및 번역

현재 `_sdd/spec/` 전체를 특정 언어로 번역하여 타임스탬프 디렉토리에 저장한다.
번역 없이 원본 언어 그대로 스냅샷을 찍는 용도로도 사용할 수 있다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: `_sdd/snapshots/<timestamp>_<lang>/` 디렉토리가 생성되었다
- [ ] AC2: 원본 `_sdd/spec/`의 모든 `.md` 파일이 번역되어 스냅샷에 포함되었다
- [ ] AC3: 스냅샷 디렉토리 루트에 `summary.md`가 생성되었다
- [ ] AC4: 원본 `_sdd/spec/` 파일이 수정되지 않았다

**사용 예시**: `/sdd-skills:spec-snapshot en` (영어) · `ja` (일본어) · `ko` (한국어 원본) · 미지정 시 원본 언어 그대로

## Hard Rules

1. **구현 코드 수정 금지**: `src/`, `tests/` 등 구현 코드 파일은 수정하지 않는다.
2. **원본 스펙 수정 금지**: `_sdd/spec/` 원본 파일은 절대 수정하지 않는다. 읽기만 한다.
3. **전체 복사 + 구조 보존**: `_sdd/spec/` 아래 모든 `.md` 파일을 스냅샷에 포함하고, 원본 디렉토리 구조를 그대로 유지한다.
4. **summary.md 생성**: 스냅샷 디렉토리 루트에 `summary.md`를 생성한다.
5. **번역 일관성**: 한 스냅샷 내 모든 파일은 동일한 대상 언어로 번역한다.
6. **도메인 용어 보존**: 코드 경로, 심볼명, 명령어, 설정 키 등 코드 관련 용어는 번역하지 않고 원문 그대로 유지한다.

## Output Structure

```
_sdd/snapshots/
└── 2026-03-09T14-30_en/
    ├── summary.md                    # 번역된 스펙 요약 (자동 생성)
    ├── main.md                       # 번역된 메인 스펙
    ├── decision_log.md               # 번역된 결정 로그
    ├── auth.md                       # 번역된 컴포넌트 스펙 (플랫 구조)
    ├── billing/                      # subdirectory 구조 보존
    │   ├── billing.md
    │   └── subscription.md
    └── ...
```

- 타임스탬프 형식: `YYYY-MM-DDTHH-MM` (로컬 시간)
- 언어 코드: ISO 639-1 (`en`, `ja`, `zh`, `ko`, `es`, `de`, `fr` 등)

## Process

### Step 1: 준비

**Tools**: `Glob`, `Read`, `Bash`

1. `_sdd/spec/` 존재 여부 확인. 없으면 에러 보고 후 종료.
2. 대상 언어 결정:
   - 사용자가 언어 코드를 지정하면 해당 언어 사용
   - 미지정 시 원본 스펙의 언어를 감지하여 그대로 사용 (번역 없이 복사)
3. 타임스탬프 생성: `date +%Y-%m-%dT%H-%M` (로컬 시간)
4. 스냅샷 디렉토리 생성: `mkdir -p _sdd/snapshots/<timestamp>_<lang>/`
5. `_sdd/spec/` 아래 모든 `.md` 파일 목록 수집
6. 각 스펙 파일의 내용을 Read로 미리 읽어 둔다 (Step 2 병렬 디스패치 준비)

### Step 2: 스펙 파일 번역 및 저장

**Tools**: `Read`, `Write`, `Edit`

각 스펙 파일의 번역은 현재 콘텍스트에서 먼저 skeleton/섹션 구조를 유지한 채 직접 기록하고, 같은 흐름에서 Edit으로 내용을 채운다.
- 독립 섹션 2개+ → 병렬 Agent dispatch 가능
- 의존 섹션 → 순서대로 Edit
- 완료 후 TODO/Phase 마커 제거

번역 규칙 (각 Agent 호출에 포함):
- 마크다운 구조(헤딩, 테이블, 코드블록, 링크)는 그대로 유지
- 코드블록 내용은 번역하지 않음
- 파일 경로, 심볼명, 명령어는 번역하지 않음
- 섹션 헤딩은 번역하되, 앵커 링크가 깨지지 않도록 주의

독립 파일 2개 이상이면 병렬 디스패치. summary.md는 Step 3에서 순차 생성.

### Step 3: summary.md 생성

**Tools**: `Write`

스냅샷 디렉토리 루트에 `summary.md` 생성. 내용:

```markdown
# Spec Snapshot Summary
- **Source**: `_sdd/spec/`
- **Snapshot**: `_sdd/snapshots/<timestamp>_<lang>/`
- **Language**: <대상 언어>  |  **Created**: <날짜 시간>  |  **Source Commit**: <short hash>

## Project Overview
<메인 스펙의 Goal 섹션 요약 — 2-3문장>

## Components
| Component | File | Description |
|-----------|------|-------------|
| ... | ... | ... |

## Open Questions
<Open Questions 섹션 요약>
```

### Step 4: 완료 보고

| 항목 | 내용 |
|------|------|
| 스냅샷 경로 | `_sdd/snapshots/<timestamp>_<lang>/` |
| 대상 언어 | (언어명) |
| 파일 수 | N개 |
| 원본 커밋 | (short hash) |

## Error Handling

| 상황 | 대응 |
|------|------|
| `_sdd/spec/` 미존재 | 에러: "`spec-create`를 먼저 실행하세요." |
| `_sdd/snapshots/` 미존재 | `mkdir -p`로 자동 생성 |
| 동일 타임스탬프 디렉토리 존재 | 덮어쓰기 |
| 빈 스펙 파일 | 빈 파일 그대로 복사 |
| 번역 중 불확실한 용어 | 원문을 괄호로 병기: "invariant (불변 조건)" |

## Integration

`spec-create`(원본 생성) → **spec-snapshot**(번역 스냅샷) → `spec-summary`(요약 참고)

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
