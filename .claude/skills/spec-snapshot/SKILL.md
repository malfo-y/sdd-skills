---
name: spec-snapshot
description: This skill should be used when the user asks to "spec snapshot", "snapshot spec", "translate spec", "export spec", "스펙 스냅샷", "스펙 번역", or wants to create a timestamped snapshot of the current spec with optional translation.
user_invocable: true
---

# spec-snapshot

## Goal

현재 `_sdd/spec/`의 모든 Markdown을 원본 구조 그대로 타임스탬프 snapshot에 보존하고, 필요하면 지정 언어로 번역한다. source bytes는 수정하지 않으며 snapshot의 `summary.md`가 provenance를 기록한다.

## Acceptance Criteria

- [ ] source relative-path + SHA-256 manifest를 snapshot 작성 전에 기록했다.
- [ ] unused `_sdd/snapshots/<timestamp>_<lang>[-NN]/` destination을 만들었다.
- [ ] 모든 source `.md` relative path가 destination에 존재한다.
- [ ] same-language copy 또는 translated-structure/token 규칙을 각 파일에 적용했다.
- [ ] destination `summary.md`가 exact metadata marker와 source-summary present/absent branch를 만족한다.
- [ ] 완료 후 source manifest가 시작 manifest와 exact match한다.

## Hard Rules

1. `_sdd/spec/` source는 read-only다.
2. existing destination을 덮어쓰지 않는다.

## Process

### Step 1: Capture Source and Destination

1. `_sdd/spec/` 존재를 확인한다. 없으면 Error Handling으로 종료한다.
2. 모든 source `.md`의 sorted relative path와 SHA-256을 manifest로 기록한다.
3. root `summary.md`에 reserved delimiter `<!-- SPEC-SNAPSHOT-METADATA:START -->` 또는 `<!-- SPEC-SNAPSHOT-METADATA:END -->`가 있으면 destination을 만들기 전에 종료한다.
4. 표시할 target language는 사용자 지정값을 우선하고, 없으면 source 언어를 사용한다.
5. filesystem `lang-slug`는 target language를 lowercase ASCII로 바꾼 영문·숫자를 남기고, 그 밖의 연속 문자를 `_`로 치환한 뒤 앞뒤 `_`를 제거해 만든다. 빈 값은 `lang`을 쓰고 final slug가 `^[a-z0-9]+(?:_[a-z0-9]+)*$`인지 확인한다.
6. local time `YYYY-MM-DDTHH-MM_<lang-slug>`을 기본 destination으로 잡는다.
7. 같은 directory가 있으면 `-02`, `-03` 순으로 첫 unused suffix를 선택한다.
8. destination을 만들기 전에 resolved parent가 resolved `_sdd/snapshots/`와 exact match하는지 확인한다.
9. current source commit short hash를 기록한다. dirty source 상태의 식별은 manifest가 담당한다.

### Step 2: Copy or Translate Source Files

sorted manifest를 main loop가 context에 맞는 bounded batch로 처리하되, 한 batch의 파일을 모두 기록·검증한 뒤 다음 batch로 간다.

- target language가 source와 같으면 root `summary.md`를 제외한 파일을 byte-exact 복사한다.
- translation이면 heading/list/table/link/code-fence structure를 유지하고 code/path/symbol/command/config token을 원문으로 둔다. 모든 natural-language block은 target language에서 원문과 같은 의미를 전달하며 material omission/addition이 없어야 하고, 원문으로 남긴 일반 용어는 번역을 병기한다.
- source와 같은 relative path에 저장한다.
- root `summary.md`는 Step 3이 metadata와 함께 처리한다.

### Step 3: Write Snapshot Metadata

destination `summary.md` 맨 앞에 아래 marker block을 정확히 한 번 쓴다.

```markdown
<!-- SPEC-SNAPSHOT-METADATA:START -->
- **Source**: `_sdd/spec/`
- **Snapshot**: `<destination>`
- **Language**: `<lang>`
- **Created**: `<local timestamp>`
- **Source Commit**: `<short hash>`
<!-- SPEC-SNAPSHOT-METADATA:END -->
```

그다음 branch 하나만 적용한다.

- source `summary.md` 존재: end marker 뒤 blank line 하나를 두고 copied/translated source body 전체를 쓴다. same-language이면 marker와 blank line을 제거한 body SHA-256이 source `summary.md`와 같아야 한다.
- source `summary.md` 부재: end marker 뒤에 source evidence로 Project Overview, Components, Open Questions 요약을 생성한다.

### Step 4: Verify Manifests and Content

1. source manifest를 다시 계산해 시작 manifest와 path/hash 모두 exact 비교한다.
2. 모든 source relative path가 destination에 존재하는지 확인한다.
3. same-language이면 root summary 외 destination hash를 source hash와 비교한다.
4. destination summary marker start/end가 각 1개이고 fixed field 5개가 모두 있는지 확인한다.
5. source summary present branch면 marker 제거 후 body hash/structure를, absent branch면 생성 요약 필드를 확인한다.
6. translation이면 Markdown structure·protected token, target-language coverage, source-to-target semantic fidelity(의미 유지·material omission/addition 없음)를 파일별로 확인한다.
7. resolved destination이 `_sdd/snapshots/`의 direct child이고 `lang-slug`가 허용 regex를 만족하는지 다시 확인한다.

### Step 5: Report Completion

- snapshot path
- language
- source file count
- source commit
- source manifest preservation result

## Output Contract

- `_sdd/snapshots/<timestamp>_<lang-slug>[-NN]/...`
- `_sdd/snapshots/<timestamp>_<lang-slug>[-NN]/summary.md`

## Error Handling

| 상황 | 대응 |
|---|---|
| `_sdd/spec/` 없음 | `spec-create`를 먼저 권장하고 종료 |
| source summary에 reserved metadata delimiter 있음 | destination 생성 전 충돌 경로를 알리고 종료 |
| destination 충돌 | overwrite 없이 다음 numeric suffix 선택 |
| 빈 source file | empty body를 그대로 보존 |
| 번역 용어가 불확실 | protected token은 원문 유지, 일반 용어는 원문 병기 |
| source manifest 변경 | snapshot 완료로 보고하지 않고 변경 경로를 알림 |

## Final Check

Acceptance Criteria와 Step 4를 완료하고 source tree가 수정되지 않았음을 보고한다.
