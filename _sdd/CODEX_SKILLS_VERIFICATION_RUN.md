# Codex Skills Verification Run

**Date**: 2026-03-19
**Reviewer**: Codex
**Workspace**: `/Users/hyunjoonlee/github/sdd_skills`

## Scope

이번 러닝은 `_sdd/CODEX_SKILLS_VERIFICATION_CHECKLIST.md` 기준의 **1차 검증**이다.

- 대상: `.codex/agents/`, `.codex/skills/`, `_sdd/`
- 목적: P0 계약 정리, P1 병렬화 확장, P2 writer fan-out 반영 상태 점검
- 범위: 정적 체크 전수 실행 + 런타임 스모크 테스트 가능성 평가

## Static Checks

- Pseudo syntax: **PASS (with documented exception)**
- Diff check: **PASS**
- Contract consistency: **PASS**

### 1. Pseudo Syntax Scan

실행 명령:

```bash
rg -n "Agent\(|Task\(|AskUserQuestion|subagent_type=\"general-purpose\"|general-purpose" .codex/agents .codex/skills
```

결과:

- `.codex/agents/README.md`에서만 `Agent(...)`, `Task(...)`, `subagent_type="general-purpose"`가 검색되었다.
- 이 항목들은 active execution contract가 아니라 **“더 이상 권장하지 않는 표현” 예시**로 남아 있는 것이다.
- `.codex/skills/` 및 `.codex/agents/*.toml`의 실행 본문에는 위 금지 표현이 남아 있지 않았다.

판정:

- **PASS**
- 단, 체크리스트 실행 시 README 예외를 알고 있어야 한다.

### 2. Contract Scan

실행 명령:

```bash
rg -n "spawn_agent|wait_agent|send_input|request_user_input|multi_tool_use\.parallel|Ownership Rules|Invocation Contract|spawn -> wait -> verify -> integrate" .codex/agents .codex/skills
```

확인된 핵심 항목:

- `.codex/agents/README.md`: Invocation Contract, Ownership Rules 존재
- `.codex/agents/implementation.toml`: `worker` fan-out + `wait_agent(ids=task_agent_ids, ...)` 존재
- `.codex/skills/sdd-autopilot/SKILL.md`: lifecycle contract + step별 `spawn_agent`/`wait_agent` 존재
- `.codex/agents/spec-review.toml`: drift lane 병렬 조사 계약 존재
- `.codex/agents/spec-update-done.toml`: parallel drift collection 존재
- `.codex/skills/spec-snapshot/SKILL.md`: batch fan-out 존재
- `.codex/skills/spec-create/SKILL.md`, `.codex/skills/spec-upgrade/SKILL.md`, `.codex/skills/spec-rewrite/SKILL.md`: writer fan-out 계약 존재
- `.codex/skills/pr-review/SKILL.md`, `.codex/skills/pr-spec-patch/SKILL.md`, `.codex/skills/spec-summary/SKILL.md`: evidence/summary/report writer fan-out 계약 존재

판정:

- **PASS**

### 3. Diff Check

실행 명령:

```bash
git diff --check -- .codex/agents .codex/skills _sdd
```

결과:

- 출력 없음

판정:

- **PASS**

## Checklist Coverage

### P0 계약 정리

- [x] 공통 Invocation Contract 추가
- [x] `implementation`의 pseudo `Task(...)` 제거
- [x] `guide-create`의 pseudo `Agent(...)` 제거
- [x] `sdd-autopilot`에 `wait_agent` 수집 절차 반영

### P1 병렬화 확장

- [x] `spec-snapshot` batch 병렬 규칙 추가
- [x] `spec-review` lane 병렬 조사 규칙 추가
- [x] `implementation-review` lane 병렬 계약 추가
- [x] `spec-update-done` parallel drift collection 규칙 추가

### P2 writer fan-out

- [x] `spec-create` writer fan-out 규칙 추가
- [x] `spec-upgrade` writer fan-out 규칙 추가
- [x] `spec-rewrite` writer fan-out 규칙 추가
- [x] `pr-review` / `pr-spec-patch` / `spec-summary` fan-out 규칙 추가

## Smoke Tests

| Scenario | Result | Notes |
|----------|--------|------|
| spec-snapshot | NOT RUN | 현재 세션에서는 Codex skill dispatcher 자체를 직접 호출할 수 없음 |
| spec-review | NOT RUN | 실제 Codex 실행 환경에서 skill invocation 필요 |
| implementation-review | NOT RUN | 실제 Codex 실행 환경에서 skill invocation 필요 |
| spec-update-done | NOT RUN | 실제 Codex 실행 환경에서 skill invocation 필요 |
| spec-create | NOT RUN | 실제 Codex 실행 환경에서 skill invocation 필요 |
| pr-review | NOT RUN | `gh` 상태 + Codex skill invocation 필요 |
| sdd-autopilot | NOT RUN | 실제 multi-agent 런타임 실행 필요 |

### Smoke Test Limitation

이번 세션에서는 문서/프롬프트 정의와 로컬 파일만 직접 조작할 수 있었고, Codex 앱의 실제 slash-skill dispatcher를 shell에서 바로 호출하는 테스트 harness는 제공되지 않았다.

따라서 이번 러닝은 다음 수준까지만 완료했다.

- 문서 계약 정합성 검증
- 금지 표현 잔존 여부 확인
- 포맷/문법 위생 확인

실제 런타임 스모크 테스트는 Codex 앱에서 아래 프롬프트로 별도 수행해야 한다.

- `spec snapshot en`
- `review spec`
- `what's the status?`
- `sync spec with implementation`
- `create a spec`
- `review PR`
- `sdd-autopilot`

## Findings

### Finding 1

`README.md`의 deprecated expression 예시는 체크리스트의 단순 `rg`에 걸린다.  
즉, 체크리스트 2.1의 “예외는 README 설명뿐” 문구를 함께 봐야 오탐(false positive)을 피할 수 있다.

권장 후속:

- 체크리스트 실행자에게 README 예외를 반드시 안내
- 또는 향후에는 정적 점검 명령을 “README 제외” 버전과 “README 포함” 버전으로 이원화

## Overall Result

**1차 정적 검증: PASS**

해석:

- P0/P1/P2 문서 반영은 정적 기준에서 일관되게 적용되었다.
- active execution docs 기준으로는 Claude-style pseudo syntax가 제거되었다.
- `spawn_agent` / `wait_agent` / fan-out 계약이 핵심 대상 파일에 반영되었다.
- 다만 실제 런타임 스모크 테스트는 아직 별도 실행이 필요하다.

## Recommended Next Step

1. Codex 앱에서 체크리스트 6장의 스모크 테스트 프롬프트를 실제로 순서대로 실행한다.
2. 결과를 이 문서 하단에 추가하거나 새 러닝 문서로 남긴다.
