---
name: implementation-review
description: Use this skill to review implementation progress against the plan, verify acceptance criteria, identify issues, and determine next steps. Triggered by "review implementation", "check progress", "verify implementation", "what's done", "implementation status", or "audit the code". Works with or without a draft/plan (graceful degradation).
argument-hint: "[--model <active-model>] [--effort <active-effort>]"
---

# Implementation Review (직접 correctness + simplicity spawn, Review-only)

이 스킬의 **correctness 렌즈는 메인 루프가 직접 수행**하고, **clarity 렌즈만** 범용 sub-agent로 spawn한다. spawn message에는 `references/simplicity-contract.md`(이 스킬 디렉토리)를 Read해 **계약 전문을 verbatim 포함**한다 — 요약·재구성 금지, 계약·차원·severity는 그 reference가 단일 소스다. review-only다 — 어떤 파일도 수정하지 않으며, finding 반영·마감 판정은 호출자 소관이다.

## Codex Runtime Adapter (simplicity spawn 전용)

런타임이 skill-internal agent dispatch를 허용하는 경우, 이 스킬의 직접 호출은 simplicity spawn 범위에 대한 사용자 요청으로 처리한다. 현재 런타임 정책이 명시적 sub-agent 허가를 추가로 요구하면, spawn 전에 사용자에게 위임 허가를 요청한다.

spawn 전에 **active tool schema를 직접 확인**하고 아래 두 lifecycle contract 중 정확히 하나만 선택한다. 없는 lifecycle tool을 찾으려고 `tool_search`하지 않으며, 두 contract의 필드나 lifecycle 호출을 섞지 않는다. `agent_type`은 lifecycle 필드가 아니라 **선택적 role selector**다 — active schema가 `"explorer"` 값을 지원할 때만 추가하고, 필드가 없거나 해당 값을 지원하지 않으면 생략한다. 생략해도 simplicity 역할·read-only 경계는 framed `message`의 계약 전문이 부여하므로 blocker가 아니다.

- **Mailbox contract (Desktop/current CLI)**: `spawn_agent`가 `task_name`/`fork_turns`를 요구하거나 `wait_agent`에 `targets`가 없다. invocation마다 짧은 lowercase `run_id`를 만들고, 같은 parent tree의 재실행까지 포함해 고유한 `task_name`에 그 값을 넣는다. 각 spawn에 이 `task_name`, `fork_turns: "none"`, `message`를 전달하고, 지원되는 경우에만 `agent_type: "explorer"`를 추가한다. `wait_agent({timeout_ms: 600000})` mailbox를 반복 호출해 남은 task final을 모두 수거한다. 완료 agent는 닫지 않는다. 통제된 중단이 필요할 때만 노출된 `interrupt_agent`를 사용한다.
- **Target/close contract (legacy CLI schema)**: `wait_agent`가 `targets`를 지원하고 `close_agent`도 노출된다. `message`로 spawn하고, 지원되는 경우에만 `agent_type: "explorer"`를 추가한 뒤 target wait로 final을 수거하고 완료 handle을 닫는다.
- 어느 lifecycle contract도 완전하지 않거나 둘 중 하나로 확정할 수 없으면 spawn하지 않고 **schema blocker**를 보고한 뒤, correctness 직접 리뷰만 수행하고 누락 렌즈를 명시한다. `agent_type` 부재만으로는 이 분기를 타지 않는다.

실행 surface 이름이 아니라 schema가 contract를 결정한다.

> **Subagent model override**
>
> - `$ARGUMENTS`의 `--model <name>`은 contract 선택 후 active `spawn_agent` schema의 `model` enum으로, `--effort <level>`은 같은 schema의 `reasoning_effort` enum으로 검증한다. 값이 enum 밖이면 spawn하지 않고 허용값을 보고한다.
> - 검증된 필드는 **simplicity spawn에만** 적용한다 — correctness는 메인 루프 직접 수행이라 override 대상이 아니다(그 사실을 안내). 미지정 필드는 생략해 세션/agent 기본값을 상속한다.
> - model과 effort를 합친 값은 받지 않고 `--model <active-model> --effort <active-effort>` 분리 문법을 안내한다.

Mailbox contract (아래 `r7f3a`는 예시 `run_id`):

```text
spawn_agent({task_name: "implementation_review_r7f3a_simplicity_reference", fork_turns: "none", message: "<framed payload: simplicity 계약 전문(verbatim) + Mode + Input Data(+ 참조 묶음 한정)>"})
spawn_agent({task_name: "implementation_review_r7f3a_simplicity_local", fork_turns: "none", message: "<framed payload: simplicity 계약 전문(verbatim) + Mode + Input Data(+ 국소 묶음 한정)>"})
wait_agent({timeout_ms: 600000})  // 남은 task의 final이 모두 도착할 때까지 반복
```

Target/close contract:

```text
spawn_agent({message: "<framed payload: simplicity 계약 전문(verbatim) + ... (+ 참조 묶음 한정)>"})
spawn_agent({message: "<framed payload: simplicity 계약 전문(verbatim) + ... (+ 국소 묶음 한정)>"})
wait_agent({targets: [<simplicity_묶음_id...>], timeout_ms: 600000})
close_agent({target: <각 완료 id>})
```

### Agent Message Boundary

모든 `message`는 framed payload로 만든다. 맨 앞에 `references/simplicity-contract.md` 전문을 verbatim으로 싣고(그 문서의 Runtime Boundary 절이 재호출 금지·read-only 규칙을 보유한다), 사용자 원문·slash command·skill 이름은 `## Input Data` 아래에 넣어 top-level 실행 지시처럼 전달하지 않는다.

```text
<references/simplicity-contract.md 전문 (verbatim)>
## Mode
review
## Input Data
<user request as data, target paths, conversation digest, 차원 묶음 한정>
```

## 실행 순서

1. **simplicity spawn을 먼저 띄운다** — 차원 **묶음마다 1회**(참조 ∥ 국소), 한 번에 동시 spawn. 각 spawn은 **전체 변경 대상**이다(묶음 정의·범위 불변 근거는 reference의 `호출자 차원 한정` 절이 단일 소스). Input Data에는 요청·경로와 **대화에만 있는 맥락 digest**를 담는다 — plan이 있으면 경로와 필요한 맥락만 짧게, 없으면 이번 세션에서 무엇을·왜 구현했는지와 리뷰 범위(agent는 이번 세션 대화를 직접 읽지 못한다). 대상 경로가 불명확하면 agent가 자체 Input 우선순위로 탐색하도록 위임한다.
2. **agent가 도는 동안 메인 루프가 correctness 리뷰를 직접 수행한다** (아래 Correctness 리뷰).
3. final을 위 Runtime Adapter로 전부 수거한 뒤 **합산 보고**한다 (아래 보고). wait가 timeout이면 완료로 간주하지 말고 더 기다리거나, controlled stop/blocked 상태를 사용자에게 보고한 뒤에만 중단 여부를 결정한다.

## Correctness 리뷰 (메인 루프 직접 수행, 단일 패스)

AC 충족·로직 결함·spec 정합을 본다. 형태-중복(추출 가능한 동일 로직 반복) 등 동작-불변 형태 품질은 simplicity 소관이지만, 정확성-중복(중복된 보안 검증 누락·일관성 깨진 중복 분기 등 로직 버그성)은 correctness에 잔존한다.

### 기준 문서 적응 (graceful degradation)

리뷰 기준은 있는 것에 맞춰 적응한다 — 기준이 없다고 중단하지 않는다.

1. **draft/plan 있음**: 호출자 지정 경로 또는 `_sdd/drafts/*_feature_draft_*.md` 최신. 각 task의 AC가 검증 기준이다.
2. **spec만 있음**: `_sdd/spec/*.md`의 요구사항·플로우·제약과의 정합을 검증한다.
3. **둘 다 없음**: `git log`/`git diff` 변경 범위 기준으로 보안·에러 처리·코드 패턴·테스트 품질을 검토하고, 추정 범위를 Assumptions로 보고에 명시한다.

stale 판단 예시: 기준 문서가 참조하는 주요 파일/모듈이 없음, 문서 구조와 현재 코드 구조가 크게 다름. stale이면 다음 단계 기준으로 낮추고 그 사실을 High 또는 Medium finding으로 기록한다.

### 읽기 범위 (3단 계단)

서로 독립인 파일 읽기·검색은 가능한 한 함께 배칭하고, 검색으로 좌표를 먼저 잡은 뒤 관련 구간만 선택적으로 읽는다. 이 스킬을 `implementation` 마감 게이트로 수행하는 경우 메인 루프가 방금 구현한 파일 내용을 이미 보유한다 — 보유한 내용은 재독하지 않고, 판정은 아래 계단이 요구하는 fresh 증거(diff·실행 출력)에 묶는다.

1. **변경 집합 + 기준 문서 — 변경 파일은 hunk 기본, 위험 신호 시 전문 승격**
   - 변경 파일: `git diff --name-only`. 비어 있으면(구현이 이미 커밋된 경우) `git diff --name-only <base>..HEAD` 또는 `git log`로 실측한다. draft/plan이 있으면 그 `Target Files`.
   - 변경 파일 읽기는 **diff hunk + 주변 문맥을 기본**으로 한다. 아래 승격 트리거에 하나라도 해당하면 그 파일은 전문 읽기로 승격한다: ① 실행 semantics 파일(스크립트·훅·코드 — 산문 문서 제외) ② hunk가 제어 흐름·상태·에러 경로를 만짐 ③ 해당 AC가 행동 AC(실행/테스트로 검증하는 유형 — 문자열 실재만 보는 구조 AC는 hunk로 충분) ④ 파일 대비 변경 비율이 높음(사실상 재작성 — 전문이 오히려 싸다) ⑤ hunk 검토 중 결함 의심 발견 ⑥ draft가 해당 task에 Open Questions·낮은 확신도를 표기. **승격하지 않은 파일은 보고에 `hunk-scoped`로 표기한다.**
   - 기준 문서 자체는 전문 읽기. 참조된 spec은 **AC·정합 판정에 필요한 절로 한정**한다(전문이 아니다).
   - 이 범위에서 존재/범위 확인에 더해 구현된 코드의 correctness(경계·null·에러 경로·동시성 등 로직 결함)를 능동적으로 검토한다 — AC 충족·spec 정합이 correctness를 보장하지 않는다.
   - 단일 패스에 담기지 않으면 AC 관련도·diff hunk 밀도 순으로 읽고, 승격 대상인데 전문 읽기하지 못한 파일과 그로 인해 근거가 약해진 AC verdict를 limitation으로 명시한다.
2. **인접 표면 — 검색 우선**: 변경 집합과 의존 또는 짝 관계인 파일 — 호출·import, claude↔codex 미러 짝, spec surface. 통합 깨짐·계약 불일치는 검색으로 확인하고, 전문 읽기는 finding 근거로 인용할 필요가 있을 때만 한다.
3. **그 밖 — 탐색적 읽기 금지**: 위 두 범위 밖을 탐색적으로 읽지 않는다. 단 AC가 명시적으로 요구하는 증거(전수 census, 잔존 0건, 파일 목록 일치 등)는 범위 밖이라도 검색·명령 실행으로 확보한다. 그래도 근거를 못 대면 해당 AC를 `UNTESTED(범위 밖)`로 표기하고 범위 가정을 Assumptions에 적는다.

### Fresh Verification + 증거 결속

"should work" 금지. 테스트 실행 출력을 근거로 판단하고, 이전 실행 결과를 재사용하지 않는다. `_sdd/env.md`가 있으면 환경 설정을 적용해 테스트를 시도하고, 없으면 코드 분석만 수행하고 `UNTESTED` 표기. 모든 AC verdict(MET/NOT MET/UNTESTED)는 증거(실행 출력 또는 인용한 `file:line`)에 묶는다 — 증거 없는 MET 금지.

- 표적 test/check는 30초가 지나면 중단한다. Timeout 후에는 test target, fixture, 또는 관련 구현이 바뀌기 전까지 같은 명령을 다시 실행하지 않는다.
- 느리다고 알려진 test는 repo 또는 사용자가 명시한 checkpoint에서만 실행한다. checkpoint evidence가 없는 slow 의존 AC는 임의 실행하지 않고 `UNTESTED`(사유: slow — checkpoint 대기)로 보고한다.

### Findings 분류

- **Critical**: 핵심 기능 누락, 실패 테스트, 보안 취약점, 데이터 손실 위험, breaking change
- **High**: 핵심 acceptance criteria 일부 불충족, 주요 에러 처리 갭, 중요한 통합 깨짐, 즉시 수정이 필요한 drift
- **Medium**: 비핵심 테스트 누락, 패턴 불일치, 중간 수준 성능/유지보수성 우려, 후속 수정이 필요한 구현 품질 문제
- **Low**: 리팩터링, 문서화, 가독성, 선택적 엣지 케이스, 추후 개선 권고

`Critical / High / Medium`은 호출자의 fix 대상, `Low`는 선택적 fix 또는 후속 권고 대상이다. 권고는 발견된 실제 결함 또는 측정된 위험에 직접 대응해야 한다 — "future-proof / extensible / configurable" 같은 사변적 권고 금지.

## 보고

두 렌즈 결과를 하나로 모아 보고한다 (correctness 항목은 직접 수행 결과, simplicity 항목은 agent 반환 relay):

- **Status**: 핵심 blocker 유무 1줄 + 어떤 기준(draft/spec/코드만)으로 리뷰했는지
- **Findings** (렌즈·severity별): Critical/High/Medium은 finding당 블록 — 제목 + 위치(`file:line`)·문제(증거 포함)·수정(구체적 방향). Low는 위치 포함 한 문장.
- **Verification ledger** (correctness): NOT MET·UNTESTED verdict만 행으로 낸다 — `| AC | Verification Method | Evidence (출력/인용) | Verdict |`. MET은 `MET: AC1–AC5` 꼴 축약 한 줄로 접는다 — 판정은 전 AC 증거 기반으로 수행하되(증거 없는 MET 금지), 통과 증거는 보고에 전사하지 않는다.
- **simplicity 차원 판정**: 두 묶음 반환의 합집합 (각 차원 정확히 한 묶음 소유라 중복 없음)
- **합산 severity 요약**: 두 렌즈의 Critical/High/Medium findings를 합쳐 한눈에 보이게 정리한다 (판정은 하지 않고 합산만 — 합집합 exit 판정은 하지 않는다).
- **Recommendations**: finding ID 참조로 갈음한다(`Must: C1` 식). finding에 대응되지 않는 신규 권고만 본문 1줄.
- **Assumptions**: 기준 문서 없이 리뷰한 경우의 추정 범위.

확인했으나 finding이 아닌 대조 결과는 열거하지 않는다 — 보고는 위 항목이 전부다. 줄이는 것은 출력이지 점검·대조 범위가 아니다.

## Error Handling

| 상황 | 대응 |
|------|------|
| 테스트 실행 실패 | `_sdd/env.md` 확인 후 실패 사실과 원인을 보고에 기록 |
| 기준 문서 stale | 기준 문서 적응 규칙대로 강등 + finding 기록 |
| Spec이 비구조화 | 전체적 정합성 판단으로 전환하고 한계를 적는다 |
| 대규모 코드베이스 | 읽기 범위 계단 ①의 초과 대응을 따른다 |
| 기준이 모호함 | UNTESTED로 표시하고 판단 근거를 적는다 |
| simplicity 반환 실패 | correctness 결과로 보고를 작성하되 누락 렌즈를 명시하고 재실행을 안내 |

## Integration

- `implementation`: 주 리뷰 대상이자 호출 주체 — 마감 품질 게이트로 이 리뷰를 수행하며, finding 반영은 호출자 소관. 게이트로 호출된 경우 이 리뷰의 보고는 중간 산출물이다 — 보고 직후 사용자 입력을 기다리지 않고 호출 스킬의 fix 단계로 복귀한다.
- `references/simplicity-contract.md`: clarity 렌즈 계약의 단일 소스 — spawn message에 verbatim 포함되며, `pr-review`도 sibling 경로로 같은 파일을 소비한다
- `spec-sync`: 리뷰 결과상 스펙 변경이 필요할 때 후속 스킬로 안내
