# Codex Skills & Agents 검증 체크리스트

**생성일**: 2026-03-19
**범위**: P0 계약 정리 + P1 병렬화 확장 + P2 writer fan-out
**관련 문서**: `_sdd/CODEX_SKILLS_ANALYSIS.md`

---

## 1. 목적

이 체크리스트는 `.codex/skills/`와 `.codex/agents/`에 반영한 개선이 실제로 다음 목표를 만족하는지 검증하기 위한 것이다.

- Codex-native 실행 계약(`spawn_agent`, `wait_agent`, `send_input`, `request_user_input`)과 용어가 일관적인가
- 병렬화 지침이 문서 수준 선언이 아니라 실제 검증 가능한 절차로 정리되었는가
- multi-file / long-form 작성 스킬이 single writer bottleneck을 피하도록 fan-out 규칙을 갖추었는가
- review/sync/snapshot 계열이 대형 입력에서 lane 분리 또는 batch 분리를 지원하는가

---

## 2. 빠른 정적 점검

### 2.1 금지 표현 잔존 여부

- [ ] `.codex/skills/`와 `.codex/agents/`의 실행 본문에 `Agent(` 가 남아 있지 않다
- [ ] `.codex/skills/`와 `.codex/agents/`의 실행 본문에 `Task(` 가 남아 있지 않다
- [ ] `.codex/skills/`와 `.codex/agents/`의 실행 본문에 `AskUserQuestion` 이 남아 있지 않다
- [ ] `.codex/skills/`와 `.codex/agents/`의 실행 본문에 `subagent_type="general-purpose"` 가 남아 있지 않다
- [ ] `general-purpose` 같은 Claude 스타일 역할명이 active contract에서 사라졌다
- [ ] 예외는 `.codex/agents/README.md`의 “더 이상 권장하지 않는 표현” 설명뿐이다

권장 명령:

```bash
rg -n "Agent\(|Task\(|AskUserQuestion|subagent_type=\"general-purpose\"|general-purpose" .codex/agents .codex/skills
```

### 2.2 Codex-native 계약 존재 여부

- [ ] `spawn_agent(...)` 사용 규칙이 `.codex/agents/README.md`에 있다
- [ ] `wait_agent(...)` barrier 규칙이 `.codex/agents/README.md`에 있다
- [ ] ownership / disjoint scope 규칙이 `.codex/agents/README.md`에 있다
- [ ] `implementation.toml`이 worker fan-out + `wait_agent` 수집 흐름을 명시한다
- [ ] `sdd-autopilot`이 `spawn -> wait -> verify -> integrate` 수명을 명시한다

권장 명령:

```bash
rg -n "spawn_agent|wait_agent|send_input|Ownership Rules|Invocation Contract|spawn -> wait -> verify -> integrate" .codex/agents .codex/skills
```

### 2.3 문서 위생 점검

- [ ] `git diff --check` 가 통과한다
- [ ] 새로 추가된 예시 코드 블록이 문법적으로 닫혀 있다
- [ ] `request_user_input` 명칭이 `guide-create` 본문과 reference에 일관되게 반영되었다

권장 명령:

```bash
git diff --check -- .codex/agents .codex/skills _sdd
```

---

## 3. P0 계약 검증

### 3.1 공통 계약

- [ ] 모든 custom agent 관련 문서는 `spawn_agent`를 시작점으로 설명한다
- [ ] spawned agent 결과 수집은 `wait_agent`로 설명한다
- [ ] 중간 보완이 필요한 경우에만 `send_input`을 허용하는 방향이 유지된다
- [ ] 읽기 전용 병렬화는 `multi_tool_use.parallel` 또는 `explorer` fan-out으로 설명된다

### 3.2 implementation

- [ ] [implementation.toml](/Users/hyunjoonlee/github/sdd_skills/.codex/agents/implementation.toml)에서 병렬 그룹 실행 예시가 `worker` 기준이다
- [ ] task별 파일 ownership이 `Target Files`로 명시된다
- [ ] `wait_agent(ids=task_agent_ids, ...)` barrier가 있다
- [ ] worker에게 “다른 worker 변경을 되돌리지 말라”는 지침이 포함된다
- [ ] 실패한 worker만 순차 fallback 한다는 규칙이 있다

### 3.3 guide-create

- [ ] [guide-create/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/guide-create/SKILL.md)에서 `write_phased` 위임 예시가 `spawn_agent(...message=...)` 형식이다
- [ ] `wait_agent` 수집 예시가 있다
- [ ] 복수 기능/대형 입력에서 파일 단위 fan-out 규칙이 있다

### 3.4 sdd-autopilot

- [ ] [sdd-autopilot/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/sdd-autopilot/SKILL.md)에 spawned agent lifecycle 계약이 있다
- [ ] Step 3 explorer 호출이 병렬 explorer fan-out으로 바뀌었다
- [ ] 각 파이프라인 step이 `spawn_agent` 후 `wait_agent`로 수집된다
- [ ] review-fix loop와 test 실행 예시에도 `wait_agent`가 들어 있다

---

## 4. P1 병렬화 검증

### 4.1 spec-snapshot

- [ ] [spec-snapshot/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-snapshot/SKILL.md)에 batch 단위 병렬 번역 규칙이 있다
- [ ] `main.md` 또는 index는 먼저 처리하고 나머지 파일은 batch fan-out 한다
- [ ] `SUMMARY.md`는 전체 batch 완료 후 생성되도록 되어 있다
- [ ] 경로 보존/누락 파일 검증 규칙이 있다

### 4.2 spec-review

- [ ] [spec-review.toml](/Users/hyunjoonlee/github/sdd_skills/.codex/agents/spec-review.toml)에 lane 기반 drift 조사 계약이 있다
- [ ] architecture / feature/API / config/source-field lane 예시가 있다
- [ ] lane 결과를 `wait_agent`로 수집해 severity를 통합한다고 적혀 있다
- [ ] Source-field drift가 요약 테이블에 포함된다

### 4.3 implementation-review

- [ ] [implementation-review.toml](/Users/hyunjoonlee/github/sdd_skills/.codex/agents/implementation-review.toml)에 parallel review lane 계약이 있다
- [ ] touched files / component 수 기준의 lane 활성화 기준이 있다
- [ ] 장문 리포트를 `write_phased`로 위임할 수 있게 적혀 있다

### 4.4 spec-update-done

- [ ] [spec-update-done.toml](/Users/hyunjoonlee/github/sdd_skills/.codex/agents/spec-update-done.toml)에 병렬 drift collection 섹션이 있다
- [ ] architecture / environment / source drift lane 예시가 있다
- [ ] 실제 spec edit는 부모가 순차 적용한다고 명시되어 있다

---

## 5. P2 writer fan-out 검증

### 5.1 spec 문서 계열

- [ ] [spec-create/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-create/SKILL.md)에 `main.md` 선작성 + component writer 병렬 fan-out 규칙이 있다
- [ ] [spec-upgrade/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-upgrade/SKILL.md)에 canonical spec 우선 + 하위 파일 병렬 보강 규칙이 있다
- [ ] [spec-rewrite/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-rewrite/SKILL.md)에 index 고정 후 파일별 rewrite fan-out 규칙이 있다

### 5.2 PR / 요약 계열

- [ ] [pr-review/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/pr-review/SKILL.md)에 evidence 수집 fan-out과 final report writer 위임 규칙이 있다
- [ ] [pr-spec-patch/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/pr-spec-patch/SKILL.md)에 baseline/spec + PR data 병렬 수집 규칙이 있다
- [ ] [spec-summary/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-summary/SKILL.md)에 component/status 요약 lane과 final merge 규칙이 있다

---

## 6. 런타임 스모크 테스트

아래 테스트는 실제 Codex 환경에서 “문서가 의도한 방식대로 동작하는지”를 보는 최소 검증이다.

### 6.1 준비

- [ ] throwaway workspace 하나를 준비한다
- [ ] `_sdd/spec/`, `_sdd/env.md`, 소규모 코드 파일 몇 개가 있는 테스트 프로젝트를 준비한다
- [ ] split spec 시나리오용으로 `main.md` + 3개 이상 sub-spec 파일을 준비한다
- [ ] large review 시나리오용으로 touched file 10개 이상인 예시를 준비한다

### 6.2 스모크 테스트 프롬프트

#### A. spec-snapshot

- [ ] `spec snapshot en` 으로 실행해 snapshot 디렉토리가 생성된다
- [ ] 파일 수가 많은 경우 batch 병렬화가 적용되는지 로그/행동에서 확인한다
- [ ] `SUMMARY.md`가 마지막에 생성된다

#### B. spec-review

- [ ] split spec + 여러 drift가 있는 프로젝트에서 실행한다
- [ ] lane 분리형 조사 흐름이 나타나는지 확인한다
- [ ] `SPEC_REVIEW_REPORT.md`에 Source-field drift가 반영되는지 확인한다

#### C. implementation-review

- [ ] touched files > 10 인 상태에서 실행한다
- [ ] verification / test / risk 관점이 분리되어 수집되는지 확인한다
- [ ] findings-first 출력이 유지되는지 확인한다

#### D. spec-update-done

- [ ] 구현 변경과 stale citation이 있는 프로젝트에서 실행한다
- [ ] drift lane 수집 후 최종 spec 편집이 순차 반영되는지 확인한다
- [ ] `DECISION_LOG.md` 추가 규칙이 깨지지 않는지 확인한다

#### E. spec-create

- [ ] 중규모 이상 프로젝트에서 실행한다
- [ ] `main.md`를 먼저 만들고 component spec fan-out이 가능한 구조로 안내되는지 확인한다
- [ ] 링크가 유효한지 확인한다

#### F. pr-review / pr-spec-patch

- [ ] changed files가 많은 PR에서 실행한다
- [ ] spec/context/PR diff 로딩이 병렬화 가능한 흐름으로 동작하는지 확인한다
- [ ] 최종 리포트/패치 드래프트가 저장된다

#### G. sdd-autopilot

- [ ] explorer 3-lane fan-out이 작동하는지 확인한다
- [ ] 각 step에서 `spawn_agent` 후 `wait_agent` 수집이 있는지 확인한다
- [ ] review-fix loop에서 review와 fix가 각각 수집되는지 확인한다

---

## 7. 합격 기준

다음 조건을 모두 만족하면 이번 개선은 “문서 기준 검증 완료”로 본다.

- [ ] 정적 점검에서 금지 표현 잔존 이슈가 없다
- [ ] `git diff --check` 가 통과한다
- [ ] P0 항목이 모두 충족된다
- [ ] P1 항목이 모두 충족된다
- [ ] P2 항목이 모두 충족된다
- [ ] 스모크 테스트 7개 중 핵심 시나리오 5개 이상이 기대 동작을 보인다
- [ ] 실패한 항목은 별도 보완 backlog로 남긴다

---

## 8. 기록 템플릿

```markdown
# Codex Skills Verification Run

**Date**:
**Reviewer**:
**Workspace**:

## Static Checks
- Pseudo syntax: PASS / FAIL
- Diff check: PASS / FAIL
- Contract consistency: PASS / FAIL

## Smoke Tests
| Scenario | Result | Notes |
|----------|--------|------|
| spec-snapshot | PASS / FAIL | |
| spec-review | PASS / FAIL | |
| implementation-review | PASS / FAIL | |
| spec-update-done | PASS / FAIL | |
| spec-create | PASS / FAIL | |
| pr-review | PASS / FAIL | |
| sdd-autopilot | PASS / FAIL | |

## Follow-ups
1. ...
2. ...
```
