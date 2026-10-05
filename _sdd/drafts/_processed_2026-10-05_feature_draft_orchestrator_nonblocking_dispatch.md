# Feature Draft: 오케스트레이터 비차단 dispatch와 리뷰 Medium 정리

> 규모 판정: 적격 — 변경 요소 15개가 task 4개(파일 집합 3개: worker 계약 4종×2 runtime / goal bench 2 / 양 SKILL.md)에 1:N으로 대응해 눈검산 가능, census형 sweep 없음.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
사용자 요청(2026-10-05): 메인 오케스트레이터가 worker를 폴링하며 기다리지 않고, 기다리는 동안 다른 일을 하게 한다. 같은 변경에 fable 전체 리뷰(PR #96)의 Medium 6항목을 반영한다.

새 contract/invariant:
- `sdd-orchestrator`는 worker 반환을 폴링(sleep·until 루프, 출력 파일 감시)으로 기다리지 않는다. 띄운 뒤에는 오케스트레이터 자신의 일을 하거나, 할 일이 없으면 runtime 방식(Claude 완료 알림, Codex wait)으로 다음 반환을 받는다.
- 의존성 기준 dispatch: 시작할 때와 worker 반환 하나마다(반환은 반영·state 갱신 뒤), 선행 task가 모두 DELTA_CLOSED이고 실행 중인 worker 및 함께 띄우는 worker와 Target Files가 서로소이며 그 task들과 `Contracts`를 공유하지 않는 task를 바로 띄운다. "띄운 worker가 모두 반환한 뒤" 묶음 장벽은 없다. 남는 장벽은 셋이다: read-only 검증 task(변경 task가 모두 닫힌 뒤), 구현 게이트(모든 task가 DELTA_CLOSED가 된 뒤), 게이트 fix·gate 2 판정(그 게이트 리뷰 worker가 모두 반환한 뒤 — raw 합산).
- Claude worker는 백그라운드(`run_in_background: true`)로 띄우고 완료 알림마다 처리한다. 2026-10-04 A3의 foreground 결정(dispatch마다 안내문 약 1.2k자 절약)을 대체하는 트레이드오프이며, M1(메인 맥락 ≤ 구×0.5) 재확인은 goal 루프 재실측 소관이다.
- Codex는 mailbox·target/close 두 contract 모두 final을 하나 받을 때마다 처리하고 의존이 풀린 worker를 바로 spawn한다.
- 모델 override Guardrail 예외(사용자 결정: 대체 동작 유지): `sdd-orchestrator` 무인 실행에서 허용값 밖 단계 모델은 세션 모델 상속으로 대체하고 마감 보고에 적는다.

spec 반영 표면(spec-sync 단계 소관):
- `_sdd/spec/main.md` Codex multi-agent dispatch 불릿의 "사용자가 요청한 model·reasoning override가 미지원이면 dispatch를 막는다"에 위 무인 실행 예외를 명시한다.
- `_sdd/spec/main.md` "Claude worker는 foreground로 띄우고(schema에 `run_in_background`가 있으면 `false` …) 동시 worker는 한 메시지의 여러 호출로 낸다" → 백그라운드 dispatch와 완료 알림 단위 처리, 폴링 금지.
- `_sdd/spec/main.md` "Target Files 서로소·`Contracts` 미공유·산출물 의존 없음인 task만 같은 작업 트리에서 동시에 띄운다" → 시작과 반환마다 하는 의존성 기준 dispatch(실행 중인 worker 및 함께 띄우는 worker와 Target Files 서로소·`Contracts` 미공유)와 남는 장벽 셋.
- `_sdd/spec/components.md` `sdd-orchestrator` 행의 "Claude `general-purpose` foreground"와 "리뷰 worker 계약은 state 미열람을 명시한다"(재진술 제거 후에는 공통 경계 `worker-boundary.md`가 명시), `Claude skill/agent split` 행의 "`general-purpose`, foreground".
- `_sdd/spec/decision_log.md` 새 entry 2개: 비차단·의존성 기준 dispatch(foreground 대체 포함), 무인 실행 모델 대체 예외.

## Scope
- **In**: 양 runtime `sdd-orchestrator/SKILL.md`(worker 모델 bullet 구조, 대기·dispatch 규칙, Runtime 절), 양 runtime worker 계약 4종(`feature-draft`·`plan-review`·`implementation`·`implementation-review`)의 공통 경계 재진술 제거, goal bench `metrics.py`·`review.sh`의 동작 불변 정리, 위 spec 반영 표면.
- **Out**: 벤치마크 재실측(M1 재확인 포함 — goal 루프 소관), 구 경로, 단계별 모델 선택 기능 자체 변경, README(대기 방식·foreground 서술이 없음을 실측), `worker-boundary.md`·`handoff-templates.md`·`simplicity-contract.md`·`workers/spec-sync.md`.
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

검증 레시피: `bash /private/tmp/claude-501/-Users-hyunjoonlee-github-sdd-skills/18bd1d97-361d-4d25-9233-2699074f6e25/scratchpad/checks/nonblocking_dispatch.sh [T1|T2|T3|T4]` — 줄마다 `PASS|FAIL <Task.AC.항목>`. 기준 커밋은 `f6377ad`로 고정했다. 아래 AC의 이름은 그 스크립트의 줄 이름이다.

### Task 1: worker 계약에서 공통 경계 재진술 제거
`references/worker-boundary.md`가 소유한 경계 문장을 worker 계약 4종에서 지우고 계약 고유 내용만 남긴다(양 runtime 동일본). 지울 문장:
- `feature-draft.md` Process 2 첫 문장 "사용자에게 질문하지 않는다."
- `plan-review.md` 머리말의 "state.md를 읽지 않는다", AC4의 "하위 worker"·"state.md 읽기"
- `implementation-review.md` fresh 원칙의 "state.md와", AC3의 "state.md를 읽지 않았으며/않았다"
- `implementation.md` AC3 둘째 문장 "필요하면 수정하지 않고 반환에 적었다.", §3 GREEN의 "task의 대상 파일 밖 수정이 필요해지면 …" bullet

남길 것(계약 고유 문구 8종, 각 파일에 1건):
- `feature-draft.md`: "로컬 탐색으로 닫히지 않는 unknown"
- `plan-review.md`: "리포트 파일을 만들지 않고"(머리말), "리포트 파일 생성"(AC4)
- `implementation-review.md`: "구현 worker의 통과 주장"(fresh 원칙), "어떤 파일도 수정하지 않았"(AC3)
- `implementation.md`: "맡은 task의 Target Files 밖을 수정하지 않았다"(AC3), "대상 밖 수정 필요(파일·이유)"(반환 열), "FAIL이면 수정하지 않고"(read-only 검증 task)

**Acceptance Criteria**:
- [ ] AC1: `T1.AC1.*` 4줄이 PASS다 — 지울 문구가 4개 파일에서 0건.
- [ ] AC2: `T1.AC2.*` 9줄이 PASS다 — 위 `남길 것` 8종이 각 1건 남고, 양 runtime `worker-boundary.md`가 `f6377ad` 대비 무변경이다(삭제분의 소유처 유지).
- [ ] AC3: `T1.AC3.mirror`가 PASS다 — 양 runtime `references/` 동일, SKILL.md 차이 hunk 1, `git diff --check` clean.
- [ ] AC4 (2등급): 4개 파일의 `git diff f6377ad`가 위 목록의 삭제와 문장 이음(조사·구두점) 외 의미 변경을 담지 않는다. reviewer가 hunk마다 "지운 문구 ↔ `worker-boundary.md`의 대응 문장"을 인용하고, 대응 문장이 없는 삭제가 하나라도 있으면 NOT MET.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/references/workers/feature-draft.md` -- unknown 처리 첫 문장 삭제
- [M] `.claude/skills/sdd-orchestrator/references/workers/plan-review.md` -- 머리말·AC4의 state.md·하위 worker 삭제
- [M] `.claude/skills/sdd-orchestrator/references/workers/implementation-review.md` -- fresh 원칙·AC3의 state.md 삭제
- [M] `.claude/skills/sdd-orchestrator/references/workers/implementation.md` -- AC3 둘째 문장·§3 대상 밖 bullet 삭제
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/workers/feature-draft.md` -- 동일본 미러
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/workers/plan-review.md` -- 동일본 미러
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/workers/implementation-review.md` -- 동일본 미러
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/workers/implementation.md` -- 동일본 미러

### Task 2: goal bench 스크립트 동작 불변 정리
`metrics.py`의 도달 불가 필터와 한 줄 중첩, `review.sh`의 한 줄 JSON schema를 같은 동작의 읽기 쉬운 형태로 바꾼다.
- `metrics.py` `bash_writes`: `targets = REDIRECT.findall(cmd)`. REDIRECT의 캡처 class `[^\s;&|)]`가 `&`를 제외해 `"&1"`·`"&2"` 필터는 도달 불가다.
- `metrics.py` `_py_write_targets`: `assigns = dict(m.groups() for m in (...) if m)` → 같은 동작(같은 이름은 나중 할당이 이김)의 for 루프.
- `review.sh`: `SCHEMA`를 `SCHEMA=$(cat <<'EOF'` … `EOF` `)` 형태의 여러 줄 heredoc으로 정의한다(`set -euo pipefail` 아래 `read -r -d ''`는 종료 코드 1로 중단된다). `claude`에 넘기는 값은 JSON으로 같다.

**Acceptance Criteria**:
- [ ] AC1: `T2.AC1.redirect`·`T2.AC1.assigns-loop`가 PASS다 — `targets = REDIRECT.findall(cmd)` 1건, `"&1"` 0건, `dict(m.groups()` 0건.
- [ ] AC2: `T2.AC2.runs-identical`·`T2.AC2.unit-identical`이 PASS다 — `f6377ad` 판과 작업 트리 판 `metrics.py`의 scratchpad bench 16 run 출력이 byte 동일하고, edge 명령 9개(`2>&1`·`>&2`·`>>&1`·`&>`·변수 재할당 포함)에서 `bash_writes`·`_py_write_targets` 결과가 같다.
- [ ] AC3: `T2.AC3.multiline`·`T2.AC3.schema-value-identical`이 PASS다 — `SCHEMA='{` 한 줄 정의 0건, `"properties"`를 담은 줄 최대 160자 이하, `bash -n` 통과, stub `claude`가 받은 `--json-schema` 값의 JSON 파싱 결과가 `f6377ad` 판과 같다.

**Target Files**:
- [M] `_sdd/goal/2026-10-04_orchestrator_harness_redesign/bench/metrics.py` -- REDIRECT 필터 제거, assigns for 루프
- [M] `_sdd/goal/2026-10-04_orchestrator_harness_redesign/bench/review.sh` -- SCHEMA 여러 줄 heredoc

### Task 3: worker 모델 규칙을 하위 bullet로 분리
`Worker dispatch` 절 "worker 모델" bullet의 한 단락(규칙 8개)을 부모 줄 "- worker 모델: 기본은 세션 모델을 상속한다(지정하지 않는다)."와 하위 bullet 4개 `  - 지정:` / `  - 범위:` / `  - 확인·기록:` / `  - 허용값 밖:`으로 나눈다. 의미는 그대로이고, 양 runtime 본문이 같다.

**Acceptance Criteria**:
- [ ] AC1: `T3.AC1.subbullets`·`T3.AC1.parent-short`가 PASS다 — `Worker dispatch` 절에 라벨 하위 bullet이 정확히 4줄이고, 부모 줄에 "허용값"이 없다.
- [ ] AC2: `T3.AC2.kept:*` 9줄이 PASS이고, 기존 `checks/model_select.sh` 9줄이 모두 PASS다.
- [ ] AC3: `T3.AC3.mirror`가 PASS다.
- [ ] AC4 (2등급): `git diff f6377ad -- .claude/skills/sdd-orchestrator/SKILL.md`의 해당 hunk에서 기준 판 bullet의 규칙 8개(기본 상속·지정 시 그 단계만·단계 이름·implementation-review는 두 리뷰 worker 모두·fix 재dispatch 같은 모델·허용값 확인·digest 기록과 재개·허용값 밖/무인 처리)가 각각 하위 bullet 하나에 대응하고, 더하거나 뺀 조건이 없다. reviewer가 대응표로 인용한다.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- `Worker dispatch` 절 worker 모델 bullet 분리
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- 같은 본문 미러

### Task 4: 오케스트레이터 대기를 비차단·의존성 기준 dispatch로 바꾼다
메인 오케스트레이터가 worker를 폴링으로 기다리지 않고, 반환 하나마다 의존이 풀린 worker를 띄우게 한다. Claude는 백그라운드 dispatch, Codex는 final 단위 처리로 받친다.

**Contracts**:
- 대기(`Worker dispatch` 절, 양 runtime 공통 본문): worker 결과를 기다리려고 sleep·until 루프나 출력 파일 감시(폴링)를 하지 않는다. 띄운 뒤에는 오케스트레이터 자신의 일(digest·state 갱신, 사용자 대화, 의존이 풀린 worker dispatch)을 하고, 할 일이 없으면 `Runtime: worker dispatch` 절의 방식으로 다음 반환을 받는다. worker의 일은 대신하지 않는다. 기존 "띄운 worker가 모두 반환한 뒤 다음 행동을 정한다"를 대체한다. 폴링 금지 문장은 이 절에만 둔다.
- 반환 단위 처리(`병렬 규칙`): 기존 "Target Files가 서로소이고 … 한 번에 동시에 띄운다. 나머지는 의존 순서대로 띄운다." bullet을 대체한다. 시작할 때, 그리고 worker가 반환할 때마다 그 반환을 `인계 파일`대로 반영한 뒤, 선행 task가 모두 DELTA_CLOSED이고 실행 중인 worker 및 함께 띄우는 worker와 Target Files가 서로소이며 그 task들과 `Contracts`를 공유하지 않는 task를 바로 띄운다. read-only 검증 task 규칙(변경 task가 모두 닫힌 뒤)은 유지한다.
- 게이트 장벽(`품질 게이트`): 구현 게이트는 모든 task가 DELTA_CLOSED가 된 뒤다(유지). 마지막 bullet "게이트 반환은 … 반환 직후 fix와 gate 2 판정을 이어서 한다"를 "게이트 반환은 사용자 입력 대기 지점이 아니다. 그 게이트의 리뷰 worker가 모두 반환하면 바로 fix와 gate 2 판정을 한다(raw 합산이 필요해 먼저 온 반환만으로 판정하지 않는다)"로 바꾼다. 이 문장 하나가 게이트 장벽과 무대기 규칙을 함께 소유한다.
- 변경분 모순(`인계 파일`): "동시에 받은 변경분이 서로 모순되면 둘 다 반영하지 않고…"를 "실행이 겹친 worker의 변경분이 이미 반영한 변경분과 모순되면 나중 변경분을 반영하지 않고 모순을 state에 적은 뒤 해당 task를 다시 계획한다"로 바꾼다.
- `실행 흐름` 3의 "`병렬 규칙`으로 묶어"를 "`병렬 규칙`대로"로 바꾼다.
- Claude `Runtime: worker dispatch`: 도구 schema에 `run_in_background`가 있으면 `run_in_background: true`로 둔다. 동시에 띄울 worker는 한 메시지에 여러 `Agent` 호출로 낸다(유지). 완료 알림은 worker마다 따로 오고, 알림마다 그 반환을 처리한다. 할 일이 없으면 턴을 끝내고 알림을 받는다. `subagent_type`·prompt·`model` 규칙은 그대로다.
- Codex `Runtime: worker dispatch`(contract 선택·spawn message bullet은 그대로):
  - **Mailbox** bullet의 "mailbox wait로 모든 final을 수거하고" → "mailbox wait로 final이 올 때마다 그 반환을 처리하고". 완료 agent는 닫지 않음·interrupt 규칙은 유지.
  - **Target/close** bullet → "spawn 후 실행 중인 worker 전부를 targets로 wait하고, final이 올 때마다 그 반환을 처리하고 그 handle을 닫는다."
  - "동시에 띄울 worker는 연달아 spawn한 뒤 함께 수거한다. …" bullet → "동시에 띄울 worker는 연달아 spawn한다. final이 오는 대로 그 반환을 처리하고, `병렬 규칙`대로 의존이 풀린 worker를 spawn한 뒤 다시 wait한다. spawn이 동시 실행 상한으로 거부되면 final을 하나 받은 뒤 spawn한다."
  - timeout bullet의 "모든 final이 올 때까지 기다리거나" → "실행 중인 worker의 final을 다시 기다리거나". timeout을 완료로 간주하지 않음은 유지.

**Acceptance Criteria**:
- [ ] AC1: `T4.AC1.no-barrier:*` 2줄과 `T4.AC1.polling-ban`이 PASS다 — 양 SKILL.md에 묶음 장벽 문구 8종(`한 번에 동시에` 포함) 0건, `Worker dispatch` 절에 "폴링"·"sleep"이 있다.
- [ ] AC2: `T4.AC2.per-return`·`T4.AC2.gate-barrier`가 PASS다 — `병렬 규칙`에 "반환할 때마다"·"실행 중인 worker"·"함께 띄우는"과 read-only 검증 장벽 1건, `품질 게이트`에 "리뷰 worker가 모두 반환하면 바로" 1건·"반환 직후" 0건과 구현 게이트 장벽 1건.
- [ ] AC3: `T4.AC3.claude-bg`·`T4.AC3.codex-final`이 PASS다 — Claude Runtime 절에 `run_in_background: true` 1건·`false` 0건·"완료 알림" 있음, Codex Runtime 절의 Mailbox·Target/close bullet에 각각 "때마다".
- [ ] AC4: `T4.AC4.mirror`가 PASS다 — 양 SKILL.md 차이는 `Runtime: worker dispatch` 절 hunk 1개뿐이다.
- [ ] AC5 (2등급): reviewer가 양 SKILL.md 줄을 인용해 네 항목을 모두 확인하면 MET이다. (i) 시작과 반환 하나의 처리 순서(`인계 파일`대로 반영 → `병렬 규칙` 판정 → dispatch)가 한 경로로 읽히고, 함께 띄우는 task끼리의 서로소가 명시된다. (ii) 남는 장벽 셋이 각각 명시되고 그 밖의 "모두 반환/수거한 뒤" 대기가 없다. (iii) 폴링 금지가 `Worker dispatch` 한 곳에만 있고 Runtime 절은 알림·wait 수단만 적는다. (iv) Codex 두 contract가 모두 final 단위로 처리하고 timeout을 완료로 세지 않는다.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- 대기·병렬·게이트·인계 파일·실행 흐름 문구와 Claude Runtime 절
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- 같은 본문과 Codex Runtime 절

# Open Questions
- 변경분 모순 규칙: 반환 단위 처리에서는 "동시에 받은" 경우가 없어진다. 실행이 겹친 worker의 나중 변경분을 반영하지 않고 해당 task를 다시 계획하도록 정했다. 사용자 확인 불필요.
- Codex Target/close wait: targets 중 하나가 final에 이르면 wait가 돌아온다고 가정했다(로컬에서 schema 확인 불가). 전부를 기다리는 구현이면 그 contract에서는 묶음 대기로 돌아간다. 사용자 확인 불필요 — 다음 Codex 실행에서 확인.
- `review.sh` "전달 값 불변"은 JSON 값 동일(파싱 결과 동일)로 해석했다. 여러 줄 heredoc은 공백·줄바꿈 바이트가 달라진다. 사용자 확인 불필요.
