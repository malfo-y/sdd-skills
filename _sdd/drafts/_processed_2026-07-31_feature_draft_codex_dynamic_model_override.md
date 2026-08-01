# Feature Draft: Codex dynamic subagent model override

> 규모 판정: 적격 — review orchestrator 3개와 사용자 예시 2개에 같은 override 검증 계약을 전파하고 전수 census로 닫는 소규모 변경이다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

Codex review subagent의 `--model`·`--effort` 허용값은 저장소의 고정 목록이 아니라 선택된 active `spawn_agent` schema의 model/reasoning-effort enum을 단일 근거로 검증한다. 문서 예시는 Codex 0.146.0의 현재 값(`gpt-5.6-sol`·`gpt-5.6-terra`, effort `low`~`ultra`)을 보여주되 runtime contract로 고정하지 않는다.

## Scope

- **In**: Codex review skill 3개의 argument hint·override validation, README와 PR sample의 현재 예시, current truth의 override contract
- **Out**: Claude model override, top-level Codex model 설정, agent TOML 기본 모델, runtime adapter lifecycle, model cache/CLI 자체 문제
<!-- spec-update-todo-input-end -->

## Decisions and Assumptions

- **Dynamic validation**: active `spawn_agent` schema가 이미 필드 지원과 enum을 공개하므로 별도 저장소 allowlist를 만들지 않는다. 요청값이 active enum에 없으면 dispatch 전에 허용값과 함께 blocker를 보고한다.
- **Current examples, not contract**: `gpt-5.6-sol`·`gpt-5.6-terra`, `max`·`ultra`는 현재 Desktop schema의 실측 예시다. CLI 0.146.0은 별도 override spawn smoke로 호환성을 확인하며, 미래 schema에서 값이 바뀌면 각 실행의 active enum이 우선한다.
- **Confidence / confirmation**: 현재 Desktop tool schema와 CLI 0.146.0 runtime smoke에 근거한 high-confidence 정정이며 추가 사용자 확인은 필요하지 않다.

# Part 2: Tasks

### Task 1: Replace stale review override allowlists with schema validation

세 review orchestrator가 current/legacy schema 각각의 실제 enum만 받아들이고, 문서 예시가 현재 Codex 모델군을 반영하게 한다.

**Contracts**: `--model`은 active spawn schema의 model enum, `--effort`는 reasoning-effort enum으로 검증한다. 요청 필드 자체가 없거나 요청값이 enum 밖이면 dispatch하지 않고 schema가 노출한 허용값을 보고한다. 옵션을 생략하면 기존처럼 세션/agent 기본값을 상속한다.

**Acceptance Criteria**:

- [ ] AC1: `plan-review`, `implementation-review`, `pr-review`가 고정 model/effort allowlist를 소유하지 않고 active schema enum 검증을 명시한다.
- [ ] AC2: 세 skill의 hint는 특정 버전에 고정된 모델 목록을 canonical contract처럼 제시하지 않는다.
- [ ] AC3: README와 `.codex/skills/pr-review/examples/sample-review.md`는 현재 Codex 예시로 `gpt-5.6-sol`·`gpt-5.6-terra`를 사용하고 구 모델 예시 잔존이 0이며, README는 effort `max`·`ultra`까지 허용 가능함과 active schema 우선 규칙을 설명한다.
- [ ] AC4: model과 effort 분리 문법, 모든 reviewer에 균일 적용, 미지정 시 기본값 상속 계약은 보존된다.

**Target Files**:

- [M] `.codex/skills/plan-review/SKILL.md` -- dynamic override validation
- [M] `.codex/skills/implementation-review/SKILL.md` -- dynamic override validation
- [M] `.codex/skills/pr-review/SKILL.md` -- dynamic override validation
- [M] `README.md` -- current Codex usage examples and schema-first note
- [M] `.codex/skills/pr-review/examples/sample-review.md` -- current reviewer model example

### Task 2: Prove stale executable allowlists are gone

현재 truth와 실행 표면에서 구 model/effort 목록 잔존과 새 enum 누락을 전수 검사한다.

**Acceptance Criteria**:

- [ ] AC1: live `.codex/skills`(PR sample 포함)와 README에서 executable/canonical `gpt-5.5|gpt-5.4|gpt-5.4-mini` allowlist·예시 잔존이 0이다(append-only history 제외).
- [ ] AC2: 세 review skill 모두 active schema enum·unsupported blocker·default inheritance·separate model/effort 문법 검사를 통과한다.
- [ ] AC3: Desktop과 `codex-cli 0.146.0`에서 각각 `gpt-5.6-sol`·`gpt-5.6-terra` override spawn이 완료되고, effort 경계 `low`·`ultra`가 schema validation 오류 없이 수락된다.
- [ ] AC4: `git diff --check`, Markdown local link, SKILL direct reference, agent TOML 5/5 parse/name 검사가 계속 통과한다.

**Target Files**:

- 없음 (read-only 검증)
