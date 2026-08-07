---
name: spec-summary
description: This skill should be used when the user asks to "summarize spec", "spec summary", "show spec overview", "스펙 요약", "스펙 개요", "show spec status", "스펙 현황", "project overview", "프로젝트 개요", "what's the current state", "현재 상태는", or wants a reader-facing whitepaper of the current repo/spec with an optional appendix for planned/progress signals.
---

# spec-summary

## Goal

현재 global spec과 필요한 supporting/code evidence를 읽어 `_sdd/spec/summary.md`에 reader-facing whitepaper를 만든다. 독자가 문제와 동기, 설계 이유, 실제 근거, 사용 흐름을 연결해 이해하고 더 깊은 supporting surface로 내려갈 수 있어야 한다.

## Acceptance Criteria

- [ ] `_sdd/spec/summary.md`를 생성하거나 안전하게 갱신했다.
- [ ] global spec, 관련 supporting docs, 필요한 source anchor를 식별했다.
- [ ] runtime-local output template의 required heading과 order를 유지했다.
- [ ] 핵심 설명을 concrete path, symbol, command, 또는 source table과 연결했다.
- [ ] 현재 기준의 설계와 기대 결과를 설명하고 change-history narration은 본문에서 제외했다.
- [ ] Step 3에서 선택한 active draft/ledger가 있을 때만 optional appendix를 포함했다.
- [ ] README optional output은 Step 7 조건과 managed-block 경계를 준수했다.

## SDD Lens

- summary는 thin global spec을 대체하지 않는 설명용 companion 문서다.
- authoritative inventory나 feature detail을 복제하지 않고 근거 surface로 연결한다.
- planned/progress signal은 whitepaper 본문과 분리된 optional appendix에만 둔다.

## Hard Rules

1. 허용된 write는 `_sdd/spec/summary.md`와 Step 7이 활성화한 README managed block뿐이다. 나머지 `_sdd/spec/`·repository surface는 read-only다.
2. 문서 언어는 기존 spec/docs를 따르고, 없으면 한국어를 기본으로 한다.
3. 근거 없는 일반론으로 code claim을 채우지 않는다.

## Input Sources

필요한 범위만 아래 순서로 읽는다.

1. 사용자 지정 spec 경로
2. `_sdd/spec/main.md` 또는 project index
3. 관련 supporting spec과 lowercase canonical `decision_log.md` (legacy uppercase `DECISION_LOG.md`는 read-only fallback)
4. 설명에 필요한 concrete code/config/command surface
5. basename이 `_processed_`로 시작하지 않는 관련 `_sdd/drafts/*_feature_draft_*.md`
6. basename이 `_processed_`로 시작하지 않는 관련 `_sdd/implementation/*_implementation_ledger_*.md`
7. Step 7이 활성화한 경우의 `README.md`

## Process

### Step 1: Locate the Spec Set

main/index와 관련 supporting surface를 찾고 repo-level problem, boundary, decision을 식별한다.

### Step 2: Locate Concrete Evidence

핵심 설명을 뒷받침할 path, symbol, command, test, source table을 현재 repository에서 확인한다.

### Step 3: Select Optional Appendix Inputs

basename이 `_processed_`로 시작하지 않는 active draft/ledger 중 현재 계획/진행 이해에 직접 필요한 파일만 고른다. processed/history artifact는 current signal로 사용하지 않는다. 선택된 신호가 없으면 appendix를 생략한다.

### Step 4: Extract Current Facts

- 해결하는 문제와 동기
- 대안 대비 현재 접근을 택한 이유
- 핵심 설계와 guardrail
- concrete source grounding
- 사용 흐름, 기대 결과, 실패/예외 경계
- 더 깊이 읽을 supporting surface

### Step 5: Check Scope and Evidence

authoritative source를 요약본으로 대체하거나 과거 변경 이력을 본문에 섞지 않았는지 확인한다.

### Step 6: Load the Output Interface and Write

작성 직전에 runtime-local `references/summary-template.md`를 **Read**한다. 그 파일의 fenced output skeleton을 verbatim 복사해 title·heading·order를 유지하고, 확인한 evidence로 slot을 채운다. optional appendix는 Step 3의 선택 결과를 적용한다. reference 내용을 기억이나 이 본문으로 재구성하지 않는다.

장문이면 main loop가 skeleton을 먼저 저장하고 section slot을 순서대로 채운 뒤 placeholder를 제거해 finalize한다.

### Step 7: Optional README Sync

사용자가 README sync를 명시적으로 요청한 경우에만 `spec-summary` managed block을 갱신하고, block 밖 내용은 보존한다.

### Step 8: Verify

Acceptance Criteria와 output file을 직접 대조하고, 미충족 항목을 같은 흐름에서 수정한다.

## Output Contract

- 기본: `_sdd/spec/summary.md`
- 조건부: `README.md`의 `spec-summary` managed block

## Error Handling

| 상황 | 대응 |
|---|---|
| spec 없음 | `spec-create`를 먼저 권장하고 종료 |
| supporting 범위가 큼 | repo-level decision과 직접 연결된 최소 surface로 좁힘 |
| source anchor가 약함 | claim을 확장하지 않고 한계를 명시 |

## Final Check

Acceptance Criteria를 모두 만족하고 `_sdd/spec/summary.md` 외 비요청 surface를 수정하지 않았는지 확인한다.
