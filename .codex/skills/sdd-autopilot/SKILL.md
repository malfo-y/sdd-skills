---
name: sdd-autopilot
description: "적응형 오케스트레이터 메타스킬. /sdd-autopilot으로 호출하여 요구사항 분석부터 스펙 동기화까지 end-to-end SDD 파이프라인을 자율 실행한다."
version: 2.3.0
---

# SDD Autopilot

## Goal

사용자 요청을 SDD 파이프라인으로 해석하고, 적절한 오케스트레이터를 만든 뒤 실행과 검증까지 끝내는 최상위 메타스킬이다. global spec은 장기적 SoT로, temporary spec은 실행 청사진으로 취급하며 `_sdd/` 아티팩트를 중심으로 discussion, planning, implementation, review, spec sync를 연결한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: 8-step pipeline(Step 0~8)이 순서대로 실행 완료되었다 (부분 파이프라인은 해당 범위 내 완료)
- [ ] AC2: `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`에 generated orchestrator를 저장하고 검증을 통과했다
- [ ] AC3: orchestrator 기반 Phase 2 자율 실행이 완료되었다 (에이전트 호출 + Exit Criteria 검증)
- [ ] AC4: review 포함 파이프라인에서 review-fix loop가 정상 동작했다
- [ ] AC5: E2E 테스트/검증이 실제로 실행되었다 (인라인 또는 ralph-loop). Execute → Verify 패턴 준수. 결과가 사용자가 볼 수 있는 형태로 저장되었다 (`_sdd/implementation/test_results/` 또는 `ralph/state.md`). 테스트 건너뛰기 금지 — 실행 불가 시 사유와 수동 검증 방법을 보고서에 명시해야 한다.
- [ ] AC6: 테스트/검증 결과가 사용자에게 명시적으로 보고되었다 (통과/실패 건수, 실패 시 원인 요약, 수동 확인 필요 항목)
- [ ] AC7: 최종 결과와 후속 조치를 `_sdd/pipeline/report_<topic>_<timestamp>.md`에 정리했다
- [ ] AC8: `_sdd/spec/` 직접 수정은 `spec_update_done` 또는 `spec_update_todo` 에이전트에만 위임했다
- [ ] AC9: Phase 2 진입 전에 Step 6 checkpoint에서 pre-flight 결과를 공유하고 explicit approval을 받았다

## Workflow Position

```text
User Request
    |
    v
[sdd-autopilot] -----> Phase 1 (Interactive)
    |                 |- Reference Loading
    |                 |- Task Analysis + Inline Discussion
    |                 |- Explore agent / local exploration
    |                 |- Reasoning -> Orchestrator Generation
    |                 `- Orchestrator Verification
    |
    v
[sdd-autopilot] -----> Phase 1.5 (Checkpoint)
    |                 `- 검증 결과 + 파이프라인 요약 + pre-flight -> 사용자 확인
    |
    v
[sdd-autopilot] -----> Phase 2 (Autonomous Execution)
                      |- 파이프라인 단계 순차 실행
                      |- review-fix loop
                      |- 테스트 (인라인 or Ralph)
                      `- 최종 요약 + 보고
```

## Hard Rules

1. **Discussion 인라인 실행 + `_sdd/spec/` 직접 수정 금지**: Step 2 대화는 autopilot 본문에서 직접 수행한다. global spec 수정은 반드시 `spec_update_done` / `spec_update_todo` 에이전트에 위임한다.
2. **Phase 2 무중단 + 파일 기반 상태 전달**: Phase 2 진입 후 `request_user_input` 금지. 에이전트에는 파일 경로만 전달하며, 전체 출력을 부모 컨텍스트에 누적하지 않는다.
3. **오케스트레이터 저장 + 공유 로그 필수**: 오케스트레이터는 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`에 저장한다. 실행 시 `_sdd/pipeline/log_<topic>_<timestamp>.md`를 생성하고 각 단계 완료 후 핵심 결정사항을 기록한다.
4. **에이전트 호출 시 원문 전달**: 사용자의 원래 요청과 관련 컨텍스트 파일 경로를 포함한다. 의미를 잃을 정도로 축약하지 않는다.
5. **Review-Fix 사이클 필수**: review 포함 파이프라인에서는 review → fix → re-review 사이클을 실행해야 한다. 리뷰만 하고 끝나는 것은 불허한다.
6. **Execute → Verify 필수**: 모든 단계는 실행(Execute) + 검증(Verify) 두 페이즈를 거친다. 에이전트 호출만으로 완료 간주 금지. Exit Criteria 미충족 시 다음 단계 진행 불가.
7. **Pre-flight + approval 필수**: Phase 2 진입 전 `_sdd/env.md`와 `.codex/config.toml`을 읽고 실행 가능성을 점검한 뒤 explicit approval을 받아야 한다.
8. **Agent lifecycle 수집 필수**: `spawn_agent(...)`로 시작한 실행 단위는 `wait_agent(...)`로 반드시 수집하고, 필요 시 `send_input(...)` 또는 재-spawn으로 보완한다.
9. **로그 기반 상태 관리**: 오케스트레이터는 `_sdd/pipeline/orchestrators/`에 유지. 활성/완료 구분은 로그 파일 status로 판단한다.
10. 한국어를 기본으로 하되 사용자 언어를 따른다.
11. spec-less repo에서도 중단하지 않는다. `_sdd/spec/`가 없으면 `_sdd/` workspace bootstrap + code-first fallback reasoning으로 계속 진행하고, 적절한 시점에 `spec-create` 또는 spec sync 단계를 파이프라인에 포함한다.

## Process

### Step 0: Pipeline State Detection (파이프라인 상태 감지)

autopilot 호출 시 기존 파이프라인 상태를 확인한다.

| 체크 | 동작 |
|------|------|
| `_sdd/pipeline/log_*.md` 스캔 | 미완료 스텝(`pending`/`in_progress`/`failed`) 필터링 |
| `_sdd/spec/*.md` 존재 확인 | 없으면 spec-less mode로 계속 진행하고, `_sdd/` bootstrap 및 `spec-create`/spec sync 필요성을 오케스트레이터에 기록 |
| `_sdd/drafts/`, `_sdd/implementation/` 스캔 | 기존 산출물 활용 여부 판단 |

상태별 분기:
- 미완료 로그 0건 + `_sdd/spec/` 없음 → spec-less mode로 Step 1
- 미완료 로그 0건 + 산출물 없음 → Step 1
- 미완료 로그 1건 → 재개 후보 제시
- 미완료 로그 2건 이상 → 목록 제시 + 선택
- 미완료 로그 0건 + 산출물 있음 → Step 1에서 활용 여부 판단

### Step 1: Reference Loading (레퍼런스 로딩)

아래 companion asset을 읽고 내재화한다.

- `references/sdd-reasoning-reference.md`
- `references/orchestrator-contract.md`
- `examples/sample-orchestrator.md`

내재화 대상:
- SDD 원칙 3개
- 스킬 의존성 그래프
- 파이프라인 구성 가이드라인
- 테스트 전략 판단 기준
- review-fix 및 final report 규칙

Gate 1→2: reference 로딩 성공 시 Step 2 진행.

### Step 2: Task Analysis + Inline Discussion (요청 분석 + 인라인 토론)

요청에서 다음을 추출하고, 부족한 정보만 `request_user_input`으로 보완한다.

- 기능 설명
- 기술 키워드
- 제약 조건
- 기존 코드와의 관계
- 시작점/종료점 힌트
- 테스트 요구사항
- 스펙 변경 여부

질문 원칙:
- 1회에 1개 핵심 분기만 묻는다
- 선택지는 2-3개로 제한한다
- 항상 `충분합니다 -- 진행해주세요` 옵션을 둔다
- 최대 5회 이내로 정리한다

Gate 2→3: 핵심 요구사항이 확정되면 Step 3.

### Step 3: Codebase Exploration (코드베이스 탐색)

`explorer` 에이전트 또는 로컬 탐색으로 다음을 수집한다.

- 프로젝트 구조
- 관련 파일/모듈
- 기존 패턴
- 테스트 구조
- `_sdd/spec/` 현황
- 수정 범위와 예상 리스크

필요하면 구조/도메인/테스트 관점으로 explorer를 병렬 호출한다. 결과는 전체 로그가 아니라 핵심 사실만 요약한다.

Gate 3→4: 프로젝트 구조와 관련 파일 식별 완료 → Step 4.

### Step 4: Reasoning → Orchestrator Generation (추론 → 오케스트레이터 생성)

Step 1 내재화 + Step 2~3 결과를 바탕으로 추론한다.

| 판단 항목 | 내용 |
|-----------|------|
| 스펙 상태 | global spec 존재 여부와 thin-core relevance 분석. 없으면 `_sdd/` bootstrap + later `spec-create/spec-update-*` 경로를 계획 |
| 변경 범위 | temporary spec 필요 여부 / planned global update 필요 여부 |
| 계획 깊이 | 직접 구현 / feature-draft / implementation-plan |
| 검증 수준 | 인라인 테스트 / Ralph / review 포함 여부 |
| 스킬 순서 | 카탈로그 input/output/pre-condition 기반 |
| 특수 패턴 | 부분 파이프라인, 팬아웃 병렬, 재개 |

오케스트레이터 생성 규칙:
- 의존성 그래프 기반 동적 조합
- `references/orchestrator-contract.md` 계약 준수
- "구체화된 요구사항"에서 기능 수준 Acceptance Criteria 도출
- temporary spec이 예상되면 `Contract/Invariant Delta`와 `Validation Plan` linkage를 pipeline reasoning에 반영
- Reasoning Trace 3-6 bullet 간결 작성
- 저장 경로: `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`

Pre-flight Check:
- `_sdd/env.md`와 대조하여 테스트/리소스 갭 분석
- `.codex/config.toml`에서 `agents.max_depth`, `agents.max_threads` 확인
- nested writing / 병렬 fan-out 가능 여부 점검

Gate 4→5: 오케스트레이터 저장 완료 → Step 5.

### Step 5: Orchestrator Verification (오케스트레이터 검증)

Producer-Reviewer 패턴으로 검증한다.

구조 검증 (6항목):
- 유효 `agent_type` 참조
- step별 `agent_type` / 입출력 / 프롬프트 존재
- 산출물 handoff 정합성
- `Review-Fix Loop` section/contract 존재
- test strategy 존재
- error handling 존재

철학 검증 (6항목):
- Spec-first
- 드리프트 방지
- Review-fix 완전성
- Execute → Verify Exit Criteria
- 파일 기반 handoff
- 스펙 직접 수정 금지

결과 분기:
- 12/12 통과 → Step 6
- 구조 이슈 → 자동 수정(최대 2회) 후 재검증
- 철학 위반 → Step 4로 돌아가 reasoning 재실행(최대 1회)
- 재시도 후 실패 → Step 6에서 경고 표시

### Step 6: User Checkpoint (사용자 확인)

Phase 1 마지막 단계다. 아래를 사용자에게 짧게 공유한다.

- 기능 / 파이프라인 요약
- 시작점 / 종료점
- 주요 산출물
- 검증 결과
- pre-flight 결과 (`_sdd/env.md`, `.codex/config.toml`, 테스트/리소스 갭)
- 주된 리스크나 가정

확인 규칙:
- `request_user_input` 또는 동등한 단일 승인 질문으로 `승인 후 실행`, `파이프라인 수정`, `중단` 중 하나를 받는다
- `승인 후 실행`일 때만 Step 7로 진행한다
- `파이프라인 수정`이면 Step 4 또는 5로 돌아가 오케스트레이터를 조정한 뒤 Step 6을 다시 수행한다
- `중단`이면 active orchestrator를 유지하고 현재 상태를 로그에 남긴 뒤 종료한다

### Step 7: Autonomous Execution (자율 실행)

Phase 2 진입 후 `request_user_input`은 호출하지 않는다. 마일스톤 텍스트와 로그만 남긴다.

#### 7.1 파이프라인 초기화

1. `_sdd/pipeline/log_<topic>_<timestamp>.md` 생성
2. 오케스트레이터를 다시 읽고 파이프라인 단계 확인
3. 상태 테이블과 step 목록 기록

#### 7.2 파이프라인 실행

`_sdd/pipeline/orchestrators/orchestrator_<topic>.md`를 다시 읽고, 정의된 `Pipeline Steps`를 순서대로 실행한다.

각 step은 `Execute -> Collect -> Verify -> Record` 순서를 따른다.

- custom-agent step이면 오케스트레이터에 적힌 Codex `agent_type`으로 호출한다.
- 로컬 step이면 오케스트레이터에 적힌 skill 또는 명령을 실행한다.
- step별 필드, 허용 `agent_type`, Exit Criteria, Acceptance Criteria는 오케스트레이터 본문과 `references/orchestrator-contract.md`를 그대로 따른다.

#### 7.3 Review-Fix Loop + 테스트 실행

오케스트레이터에 `Review-Fix Loop`와 `Test Strategy` section이 있으면, autopilot은 그 선언을 그대로 집행한다.
이 섹션에서 별도 loop 규칙이나 테스트 규칙을 다시 정의하지 않는다.

#### 7.4 에러 핸들링

에러 처리는 오케스트레이터의 `Error Handling` section과 `references/orchestrator-contract.md`를 따른다.
재시도, 중단, 건너뛰기 결정은 모두 로그에 남긴다.

#### 7.5 마일스톤 보고 + 로그 관리

실행 중에는 마일스톤 텍스트를 출력하고, 상태와 결과를 `_sdd/pipeline/log_<topic>_<timestamp>.md`에 기록한다.
실행이 끝나면 `_sdd/pipeline/report_<topic>_<timestamp>.md`에 최종 결과를 정리한다.
로그와 보고서 schema는 오케스트레이터 본문과 `references/orchestrator-contract.md`를 따른다.

### Step 8: Final Summary (최종 요약)

최종 산출물을 점검하고 `_sdd/pipeline/report_<topic>_<timestamp>.md`를 작성한다.

필수 항목:
1. 뭘 했는가: 실행 단계, 에이전트 목록, 산출물 경로, review-fix 횟수, 테스트 여부
2. 어떻게 나왔는가: 각 단계 성공/실패, 이슈 해결 상태, 테스트 통과율, 스펙 동기화
3. 뭘 더 해야 하는가: 미완료 단계, 제한사항/리스크, 후속 작업 제안
4. Taste Decisions: 파이프라인 중 taste decision으로 분류된 자동 결정 목록
5. 오케스트레이터 경로 및 상태 확인 (로그 기반)
6. spec-less로 시작했다면 `spec-create` 또는 spec sync가 완료되었는지, 아니면 후속 작업으로 남는지 명시

## Reference Files

- `references/sdd-reasoning-reference.md`: SDD 철학, skill catalog, reasoning 기준
- `references/orchestrator-contract.md`: 오케스트레이터/로그 최소 계약
- `examples/sample-orchestrator.md`: 중규모 기본형 + 대규모 차이점 예시

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
