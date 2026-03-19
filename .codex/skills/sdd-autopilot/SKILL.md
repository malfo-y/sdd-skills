---
name: sdd-autopilot
description: "적응형 오케스트레이터 메타스킬. /sdd-autopilot으로 호출하여 요구사항 분석부터 스펙 동기화까지 end-to-end SDD 파이프라인을 자율 실행한다."
version: 2.2.0
---

# SDD Autopilot

## Goal

사용자 요청을 SDD 파이프라인으로 해석하고, 적절한 오케스트레이터를 만든 뒤 실행과 검증까지 끝내는 최상위 메타스킬이다. 스펙과 `_sdd/` 아티팩트를 Single Source of Truth로 삼아 discussion, planning, implementation, review, spec sync를 연결한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: 요구사항과 코드베이스 상태를 바탕으로 유효한 파이프라인 범위와 시작점/종료점을 결정했다.
- [ ] AC2: `.codex/skills/orchestrator_<topic>/SKILL.md`에 generated orchestrator를 저장했다.
- [ ] AC3: `_sdd/pipeline/log_<topic>_<timestamp>.md`에 실행 로그를 남겼다.
- [ ] AC4: review 단계가 포함된 파이프라인이면 review → fix → re-review 사이클을 실제로 수행했다.
- [ ] AC5: 모든 단계가 Execute → Verify 두 페이즈를 거쳤고, exit criteria를 확인했다.
- [ ] AC6: 최종 결과와 후속 조치를 `_sdd/pipeline/report_<topic>_<timestamp>.md`에 정리했다.
- [ ] AC7: `_sdd/spec/` 직접 수정은 `spec_update_done` 또는 `spec_update_todo` 에이전트에만 위임했다.

## SDD Lens

- 스펙과 `_sdd/` 산출물은 handoff contract다. 중간 결정을 파일에 고정하고 다음 단계는 그 파일을 읽어 이어간다.
- 오케스트레이터는 “무엇을 언제 어떤 산출물로 검증할지”를 명시해야 한다.
- 단계 호출만으로 완료로 보지 않는다. 항상 검증까지 통과해야 다음 단계로 진행한다.

## Companion Assets

- `references/sdd-reasoning-reference.md`: SDD 철학, 스킬 카탈로그, 파이프라인 구성 원칙
- `references/orchestrator-contract.md`: generated orchestrator 최소 계약
- `examples/sample-orchestrator.md`: 오케스트레이터 예시

위 파일들은 품질과 일관성을 높이기 위한 companion asset이다. 다만 본문만 읽어도 목표, 핵심 절차, 출력 계약은 이해 가능해야 한다.

## Hard Rules

1. Step 2의 사용자 대화는 인라인으로 수행한다. `discussion` 에이전트로 위임하지 않는다.
2. `_sdd/spec/`는 직접 수정하지 않는다. 스펙 변경은 `spec_update_done` 또는 `spec_update_todo`에 위임한다.
3. Phase 2(자율 실행) 진입 후에는 `request_user_input`을 호출하지 않는다. 마일스톤 텍스트와 로그만 남긴다.
4. 생성된 오케스트레이터는 `.codex/skills/orchestrator_<topic>/SKILL.md`에 저장한다.
5. 각 실행에서는 `_sdd/pipeline/log_<topic>_<timestamp>.md`를 만들고, 단계별 결과와 핵심 결정을 기록한다.
6. 에이전트에 전달할 때는 사용자의 원 요청과 관련 파일 경로를 가능한 한 원문 그대로 전달한다.
7. 에이전트 결과 전체를 부모 컨텍스트에 누적하지 않는다. 출력 파일, 상태, 핵심 결정만 추출한다.
8. review 단계가 들어간 파이프라인은 반드시 review → fix → re-review를 포함해야 한다.
9. 모든 단계는 Execute → Verify를 거친다. 생성형 단계도 실제 실행/결과 검증 없이 완료로 처리하지 않는다.
10. `spawn_agent(...)`로 시작한 실행 단위는 `wait_agent(...)`로 반드시 수집하고, 필요하면 `send_input(...)` 또는 재-spawn으로 보완한다.
11. 한국어를 기본으로 하되 사용자 언어를 따른다.

## Agent Lifecycle Contract

autopilot에서 custom agent 또는 explorer를 호출할 때의 표준 순서:

1. `spawn_agent(...)`로 실행 단위 생성
2. `agent_id` 추적
3. `wait_agent(ids=[...])`로 결과 수집
4. 산출물 파일 경로, severity, 핵심 결정만 추출
5. Verify에서 exit criteria 확인
6. 실패 또는 부족한 결과만 재실행/보완

## Process

### Step 0: Pipeline State Detection

기존 파이프라인과 선행 산출물을 먼저 확인한다.

- `_sdd/spec/main.md` 존재 여부 확인
- `_sdd/pipeline/log_*.md`에서 미완료 파이프라인 확인
- `_sdd/drafts/feature_draft_*.md`, `_sdd/implementation/IMPLEMENTATION_PLAN*.md` 존재 여부 확인

분기:

- 스펙이 없으면 `/spec-create`를 먼저 안내하고 종료
- 미완료 로그가 1개 이상이면 재개 후보를 제시
- 관련 선행 산출물이 있으면 이후 단계에서 활용 여부를 판단

### Step 1: Load SDD References

아래 companion asset을 읽고 내재화한다.

- `references/sdd-reasoning-reference.md`
- `references/orchestrator-contract.md`
- `examples/sample-orchestrator.md`

반드시 확보할 내용:

- SDD 원칙: spec-as-SoT, artifact handoff, verify-first
- skill dependency graph와 산출물 흐름
- generated orchestrator 최소 계약
- 테스트 전략 판단 기준
- review-fix와 final report 규칙

레퍼런스 로딩에 실패하면 오류로 종료한다.

### Step 2: Task Analysis + Inline Discussion

요청에서 다음을 추출하고, 부족한 정보만 `request_user_input`으로 보완한다.

- 기능 설명과 범위
- 기술 키워드와 제약
- 기존 코드와의 관계
- 시작점/종료점 힌트
- 테스트 요구사항
- 스펙 수정 필요 여부

질문 원칙:

- 1회에 1개 핵심 분기만 묻는다
- 선택지는 2-3개로 제한한다
- 항상 “충분합니다 -- 진행해주세요” 옵션을 둔다
- 최대 5회 이내로 정리한다

이 단계는 discussion 에이전트 대신 autopilot 본문에서 직접 수행한다.

### Step 3: Codebase Exploration

`explorer` 에이전트나 로컬 탐색으로 다음을 수집한다.

- 관련 디렉토리/파일 구조
- 핵심 엔트리포인트와 연관 모듈
- 테스트 위치와 실행 방식
- 수정 범위와 예상 리스크

필요하면 구조/도메인/테스트 관점으로 explorer를 병렬 호출한다. 결과는 전체 로그가 아니라 핵심 사실만 요약한다.

### Step 4: Decide Pipeline Shape

수집한 정보로 파이프라인 규모와 범위를 결정한다.

- 소규모: 단일 스킬 또는 짧은 체인
- 중규모: spec/plan/implementation/review 중심
- 대규모: discussion + draft/plan + implementation + review-fix + spec sync

규칙:

- 사용자가 시작/종료 범위를 지정하면 그 범위를 존중한다
- 다만 review 단계가 포함되면 review-fix 완결성은 반드시 보장한다
- 기존 산출물이 유효하면 해당 단계 이후부터 시작할 수 있다

### Step 5: Generate Orchestrator

`.codex/skills/orchestrator_<topic>/SKILL.md`에 generated orchestrator를 작성한다.

오케스트레이터에 반드시 포함할 내용:

- 파이프라인 목표와 범위
- step 목록과 순서
- 각 step의 입력, 실행 단위, 출력 산출물
- review-fix 및 테스트 전략
- 로그/체크포인트/재개 규칙
- exit criteria

오케스트레이터는 “설명문”이 아니라 실행 계약 문서여야 한다.

### Step 6: Verify Orchestrator + Checkpoint

실행 전 아래를 검증한다.

- 구조가 orchestrator contract를 만족하는가
- 각 step의 input/output이 연결되는가
- review-fix, Execute → Verify, test, final report 규칙이 포함되는가
- 시작점/종료점과 기존 산출물 활용이 일관적인가

그 후 사용자에게 아래만 짧게 공유한다.

- 파이프라인 요약
- 시작점과 종료점
- 주요 산출물
- 주된 리스크나 가정

### Step 7: Execute the Pipeline

#### 7.1 Initialize Shared Artifacts

- `_sdd/pipeline/log_<topic>_<timestamp>.md` 생성
- 필요 시 상태 테이블과 step 목록 기록

#### 7.2 Execute → Verify Loop

각 step은 아래 순서를 따른다.

1. Execute: 관련 skill/custom agent 실행
2. Collect: `wait_agent(...)` 또는 로컬 결과 수집
3. Verify: exit criteria, 테스트, 산출물 존재 여부 확인
4. Record: 로그 파일에 상태와 핵심 결정 기록

Verify 실패 시:

- 보완 입력 전송 또는 재실행
- 실패 사실과 원인을 로그에 기록
- critical 이슈면 다음 단계로 진행하지 않음

#### 7.3 Review-Fix Contract

review가 포함된 파이프라인은 아래를 반드시 수행한다.

1. `implementation_review` 또는 리뷰 단계 실행
2. finding을 구현 단계로 반영
3. 필요한 테스트 재실행
4. re-review 수행

critical/high 이슈가 남아 있으면 종료하지 않는다.

#### 7.4 Test Strategy

프로세스 특성에 따라 인라인 테스트 또는 `ralph_loop_init` 기반 장기 실행 루프를 선택한다.

- 빠른 검증 가능: 인라인 테스트/수동 실행
- 장기 실행/불안정/브라우저 의존: `ralph_loop_init`

테스트 단계도 설정 생성만으로 끝내지 않고, 실제 실행과 결과 검증까지 포함한다.

### Step 8: Finalize

최종 산출물을 점검하고 `_sdd/pipeline/report_<topic>_<timestamp>.md`를 작성한다.

포함 내용:

- 요청 요약과 선택된 파이프라인
- 각 단계의 결과와 산출물 경로
- review-fix 수행 여부
- 테스트 결과
- 남은 리스크, open question, 후속 추천

재개가 가능하도록 로그와 보고서가 현재 상태를 충분히 설명해야 한다.

## Output Contract

기본 산출물:

- `.codex/skills/orchestrator_<topic>/SKILL.md`
- `_sdd/pipeline/log_<topic>_<timestamp>.md`
- `_sdd/pipeline/report_<topic>_<timestamp>.md`

조건부 산출물:

- `_sdd/drafts/feature_draft_<name>.md`
- `_sdd/implementation/IMPLEMENTATION_PLAN*.md`
- `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`
- `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
- `_sdd/spec/` 동기화 결과물
- `ralph/` 디렉토리

최종 사용자 보고에는 아래가 포함되어야 한다.

- 무엇을 실행했는가
- 어떤 산출물이 생성/갱신되었는가
- 테스트와 review-fix가 완료되었는가
- 남은 이슈와 다음 권장 단계

## Error Handling

| 상황 | 대응 |
|------|------|
| `_sdd/spec/main.md` 없음 | `/spec-create` 안내 후 종료 |
| reference 파일 누락 | 오케스트레이터 생성 중단, 누락 파일 보고 |
| 재개 후보가 여러 개 | 후보 요약 후 사용자 선택 요청 |
| explorer 결과 부족 | 범위를 좁혀 재탐색하거나 보수적으로 파이프라인 구성 |
| step 검증 실패 | 다음 단계 진행 중단, 보완 후 재검증 |
| review 단계 실패 | fix/re-review 없이 종료하지 않음 |
| 테스트 환경 불명확 | `_sdd/env.md` 확인 후 실패 사실과 제약 기록 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

