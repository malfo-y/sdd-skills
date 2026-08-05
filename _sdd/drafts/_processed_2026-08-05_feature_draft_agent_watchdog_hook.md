# Feature Draft: Agent Watchdog 훅 — 하네스 훅 자산 4호

> 규모 판정: 적격 — 변경 요소 4종(스크립트 신설 · SKILL 설치 계약 2종 · self-host 등록 · 리터럴 census)이 Task 1~5에 1:1 대응해 눈검산 가능, 총량 단일 컨텍스트 이내.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

- 하네스 훅 자산에 4번째 스크립트 `agent-watchdog.sh`(PostToolUse) 추가 — subagent가 첫 tool call 이후 300초 이상 돌면 `decision:block` reason으로 자기점검 nudge(시간 도둑 자평 + 반복 명령 캐시/재사용 전환)를 전달한다. cooldown 300초로 재발동 제어, 메인 루프(payload에 `agent_id` 없음)는 대상 아님.
- **새 contract**: 하네스 훅 자산 목록이 3개 → 4개다 — 설치 계약(`spec-create`·`spec-upgrade` SKILL)과 spec 서술(main.md 하네스 설치 guardrail의 "스크립트 3개", components.md의 "훅 3개"·정본 3종 나열)의 개수·나열이 전부 4개 기준으로 갱신되어야 한다.
- **새 contract**: watchdog은 **advisory 자산**이다(게이트 아님) — 판정 불가 시 fail-open이 조용해도 "실행 자산은 조용히 무력화되지 않는다" guardrail 위반이 아니다. guardrail의 경고 의무는 강제 자산(게이트)에 한정됨을 spec 문구에 구분해 반영한다.
- 근거(검증 완료, 2026-08-05 실험 1·2 — work log 항목 11·12): Pre/PostToolUse 훅은 subagent tool call에 발동, `agent_id`는 subagent payload에만 존재, PostToolUse `decision:block` reason은 subagent 모델에 전문 전달되고 지시가 수행됨.

## Scope

- **In**: `agent-watchdog.sh` 정본+미러 4벌+dogfooding 사본(5경로), `spec-create`·`spec-upgrade` SKILL(claude·codex 4파일)의 설치 계약 갱신, 이 repo `.claude/settings.json` PostToolUse 등록, 훅 개수 리터럴 census.
- **Out**: PreToolUse 알려진 느린 패턴 차단 레버(`uv run --with` 등 — 후속 feature 후보), Codex 런타임 자체의 훅 실행(플랫폼 비대칭 수용은 기존 계약 그대로), `worklog-context.sh` 경고 문구 확장(advisory 판정으로 불필요 — Open Questions #3), nudge 실효(리뷰 시간 단축) 측정, spec 본문 3곳 갱신(spec-sync 소유 — Part 1이 그 입력).
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | `agent-watchdog.sh` 스크립트 본문 | `.claude/skills/spec-create/references/hooks/agent-watchdog.sh`(정본) + `.codex/skills/spec-create/references/hooks/` + `.claude/skills/spec-upgrade/references/hooks/` + `.codex/skills/spec-upgrade/references/hooks/` + `.claude/hooks/`(dogfooding) = 5경로 | `ls` 4개 references/hooks 디렉토리 → 현재 각 3파일(worklog-gate·worklog-context·harness-context); 기대: 각 4파일, 5경로 md5 동일 | Task 1 |
| P2 | 설치 계약(스크립트 목록·3e 등록 서술·settings.json JSON 예시·Final check·announce·개수 리터럴) | `.claude/skills/spec-create/SKILL.md` + `.codex/skills/spec-create/SKILL.md` | `grep -c "세 스크립트\|스크립트 3개\|세 훅\|훅 3개\|셋 다\|두 항목"` → 현재 7·7; 기대: 0 (4개 기준 문구로 대체) + JSON 예시에 `PostToolUse` 그룹 존재 | Task 2 |
| P3 | 동일 change element의 spec-upgrade 판 | `.claude/skills/spec-upgrade/SKILL.md` + `.codex/skills/spec-upgrade/SKILL.md` | 동일 grep → 현재 7·7(수사 변형 `셋 다`:165 포함); 기대: 0 + 등록 형태 서술에 `agent-watchdog.sh`/`PostToolUse` 존재 | Task 3 |
| P4 | self-host 등록 | `.claude/settings.json` | `jq '.hooks | keys'` → 현재 `PreToolUse`·`SessionStart`; 기대: + `PostToolUse` | Task 4 |

# Part 2: Tasks

### Task 1: `agent-watchdog.sh` 정본 작성 + 5경로 배치

실험 2에서 라이브 검증된 프로토타입을 운영 파라미터로 정식화하고, worklog-gate.sh와 같은 정본+미러 규율로 배치한다.

**Contracts**:
- PostToolUse 훅. payload에 `agent_id`가 없으면(메인 루프) 즉시 exit 0.
- 상태: `${TMPDIR:-/tmp}/claude-agent-watchdog/<session_id>/<agent_id>.start`에 최초 목격 epoch 기록. elapsed = now − start.
- 발동: elapsed ≥ 300s이고 직전 nudge 이후 300s 경과 시 `{"decision":"block","reason":"<nudge>"}` 1회 출력. nudge 내용 = (1) 지금 작업이 시간을 과도하게 먹는지 1문장 자평 (2) 반복 명령에 캐시/재사용 여지(예: 매번 환경 재설치 대신 venv 재사용)가 있으면 전환 (3) 이 메시지로 접근을 바꿨으면 최종 응답에 언급(관측용).
- 파서: jq → python3 fallback(worklog-gate.sh와 동일 구조). 파서 부재·파싱 실패·mkdir 실패 등 모든 판정 불가는 exit 0 (fail-open, advisory 자산).

**Acceptance Criteria**:
- [ ] AC1: 오프라인 판정 테스트 — ① agent_id 없음 → 출력 없이 exit 0 ② 최초 목격 → start 파일 기록, 출력 없음 ③ start를 301초 과거로 조작 → `decision:block` JSON 출력(jq 파싱 가능, reason에 자평·전환·언급 3요소) ④ 직후 재호출(cooldown) → 출력 없음 ⑤ PATH에서 jq 제거 시 python3 경로로 ③ 재현 ⑥ jq·python3 모두 제거 시 출력 없이 exit 0 — 각각 실제 실행 결과로 확인.
- [ ] AC2: `bash -n` 통과, 5경로 배치 후 md5 5-way 동일.
- [ ] AC3: 스크립트 헤더 주석에 정본/미러 규율(worklog-gate.sh 헤더와 동일 형식)과 advisory·fail-open 성격 명시.

**Target Files**:
- [C] `.claude/skills/spec-create/references/hooks/agent-watchdog.sh` -- 정본
- [C] `.codex/skills/spec-create/references/hooks/agent-watchdog.sh` -- 미러
- [C] `.claude/skills/spec-upgrade/references/hooks/agent-watchdog.sh` -- 미러
- [C] `.codex/skills/spec-upgrade/references/hooks/agent-watchdog.sh` -- 미러
- [C] `.claude/hooks/agent-watchdog.sh` -- dogfooding 사본 (components.md 78행 기존 규율대로 동기화 대상)

### Task 2: `spec-create` SKILL 설치 계약 갱신 (claude·codex)

설치 대상 스크립트 목록·등록 서술·JSON 예시·마감 체크·announce의 "3개" 기준을 4개로 확장한다.

**Acceptance Criteria**:
- [ ] AC1: 스크립트 목록(현 61~63행 블록)에 `references/hooks/agent-watchdog.sh` 추가, 3e 등록 서술에 `agent-watchdog.sh — PostToolUse, matcher 없음(전 tool). subagent 장기실행 자기점검 nudge(advisory)` 항목 추가.
- [ ] AC2: `settings.json` 병합 JSON 예시에 `PostToolUse` 그룹(`bash "$CLAUDE_PROJECT_DIR"/.claude/hooks/agent-watchdog.sh`) 추가, 병합 규칙 서술의 대상 이벤트 나열에 `hooks.PostToolUse` 포함.
- [ ] AC3: 파일 내 `세 스크립트|스크립트 3개|세 훅|훅 3개` 잔존 0 (개수 언급이 필요한 자리는 "네 스크립트/4개"로, 나열이 필요한 자리는 4종 전부).
- [ ] AC4: claude↔codex 두 파일의 훅 관련 라인(`grep "스크립트\|hooks/\|훅"`) parity diff 동일 유지.

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md` -- 설치 계약 canonical
- [M] `.codex/skills/spec-create/SKILL.md` -- codex 짝 (훅 섹션 현재 byte-parity 실측)

### Task 3: `spec-upgrade` SKILL 설치 계약 갱신 (claude·codex)

Task 2와 동일한 change element의 spec-upgrade 판 — 목록·등록 형태 서술·Step 6/마감·announce의 "3개" 기준 확장.

**Acceptance Criteria**:
- [ ] AC1: 스크립트 목록(현 46~48행 블록)과 등록 형태 서술(현 156~165행)에 `agent-watchdog.sh`/`PostToolUse` 항목 추가 (서술 형식은 기존 세 항목과 동일).
- [ ] AC2: 파일 내 `세 스크립트|스크립트 3개|세 훅|훅 3개` 잔존 0.
- [ ] AC3: claude↔codex 두 파일의 훅 관련 라인 parity diff 동일 유지.

**Target Files**:
- [M] `.claude/skills/spec-upgrade/SKILL.md` -- 설치 계약 (spec-create 3e 참조 구조 유지)
- [M] `.codex/skills/spec-upgrade/SKILL.md` -- codex 짝

### Task 4: self-host 등록 (`.claude/settings.json`)

이 repo도 소비 repo와 동일하게 watchdog을 받는다(dogfooding — 스크립트 배치는 Task 1 소유, 이 task는 등록만).

**Acceptance Criteria**:
- [ ] AC1: `.claude/settings.json`의 `hooks`에 `PostToolUse` 그룹이 Task 2 JSON 예시와 동일 형태로 존재 (`jq '.hooks | keys'`가 3종 반환, `jq` 파싱 통과).
- [ ] AC2: 라이브 발동 검증은 세션 스냅샷 특성상 이 세션에서 불가함을 확인 항목으로 남기지 않는다 — 전달 경로 자체는 실험 2(work log 항목 12)에서 라이브 검증 완료이므로 구조 검증(AC1)으로 닫는다.

**Target Files**:
- [M] `.claude/settings.json` -- PostToolUse 등록 (키 수준 멱등 병합과 동일 결과 형태)

### Task 5: 훅 개수 리터럴 + 누락 표면 census (read-only 검증)

**Acceptance Criteria**:
- [ ] AC1: repo-wide `grep -rn "세 스크립트\|스크립트 3개\|세 훅\|훅 3개\|셋 다\|두 항목\|three (hook )?scripts"` — live 표면(`.claude/`·`.codex/`·`docs/`·`README.md`·`AGENTS.md`) 잔존 0. 허용 예외: `_sdd/` 이력 기록물(work_log·drafts·discussion·decision_log·changelog) 및 `_sdd/spec/` 본문 3곳(main.md 하네스 설치 guardrail, components.md 52·78행 — spec-sync 소유, 이 draft Part 1이 그 입력).
- [ ] AC2: repo-wide `grep -rln "agent-watchdog"` 결과가 정확히 {Task 1의 5경로, Task 2~4의 4 SKILL+settings.json, 이 draft, work log/memory 기록물}에 속한다 — 예상 밖 표면 0, 필요 표면 누락 0.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

1. **THRESHOLD·COOLDOWN 300s**: 사용자가 "5분 이상"을 직접 지정, cooldown은 동일값 채택(5분마다 최대 1회 재-nudge). 대안: cooldown만 600s. 확신도 높음 — 스크립트 상수라 운영 중 조정 용이. 사용자 확인 불필요.
2. **matcher 없음(전 tool)**: Read/Grep 중심 reviewer도 경과 추적에 포함(실험 1에서 Read 발동 확인). 대안: `Bash` 한정. 확신도 높음. 사용자 확인 불필요.
3. **advisory 판정 — worklog-context.sh 미확장**: "조용히 무력화되지 않는다" guardrail의 경고 의무를 강제 자산(게이트)에 한정 해석하고, advisory인 watchdog의 파서 전무 fail-open은 세션 시작 경고 없이 수용한다(jq→python3 fallback으로 실확률도 낮춤). 대안: `worklog-context.sh` 경고 확장(5미러 추가 변경 — 기각: 표면 확대 대비 이득 미미). 확신도 중상. spec-sync에서 guardrail 문구에 강제/advisory 구분을 반영하는 것으로 닫음 — 사용자 확인 불필요.
4. **상태 디렉토리 `${TMPDIR:-/tmp}` 공유 리스크**: 다인 공유 /tmp에서 타 사용자 소유 디렉토리와 충돌 시 mkdir 실패 → fail-open으로 무해. session_id가 UUID라 실충돌 확률 무시 가능. 확신도 높음. 사용자 확인 불필요.
