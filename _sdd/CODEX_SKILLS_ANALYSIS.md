# Codex Skills & Agents 전체 분석

**생성일**: 2026-03-19
**대상**: `.codex/skills/` + `.codex/agents/`

---

## 1. 아키텍처 개요

### 1.1 Wrapper-Agent 패턴

이 프로젝트의 Codex 계열 자산은 **Thin Wrapper Skill + Custom Agent + Full Skill + Meta Skill** 구조로 정리되어 있다.

- **Thin Wrapper Skill (9개)**: `feature-draft`, `implementation-plan`, `implementation`, `implementation-review`, `ralph-loop-init`, `spec-review`, `spec-update-done`, `spec-update-todo`, `write-phased`
- **Full Skill (9개)**: `discussion`, `guide-create`, `pr-review`, `pr-spec-patch`, `spec-create`, `spec-rewrite`, `spec-snapshot`, `spec-summary`, `spec-upgrade`
- **Meta Skill (1개)**: `sdd-autopilot`
- **Custom Agent (9개)**: `.codex/agents/` 아래 `feature_draft`, `implementation_plan`, `implementation`, `implementation_review`, `ralph_loop_init`, `spec_review`, `spec_update_done`, `spec_update_todo`, `write_phased`

핵심 분리 원칙은 `.codex/agents/README.md`에 명시되어 있다.

- **wrapper skill**: 사용자 진입점과 handoff contract 담당
- **custom agent**: 실제 workflow 본문과 실행 backbone 담당
- **generated orchestrator**: wrapper가 아니라 custom agent를 직접 spawn하는 구조를 전제

즉, `.codex/skills/<skill>/SKILL.md`는 트리거와 handoff를 정의하고, 실제 실행 세부 로직은 `.codex/agents/*.toml`의 `developer_instructions`에 모으는 방향이다.

### 1.2 Codex 기준에서의 구조적 특징

Claude 계열 분석 문서와 비슷한 목적을 가지지만, Codex 버전은 다음 특징이 더 두드러진다.

1. **custom agent registry가 명시적이다**  
   `.codex/agents/*.toml`이 분리되어 있어 wrapper와 실행 backbone의 책임 구분이 더 선명하다.

2. **실제 `spawn_agent(...)` 예시는 `sdd-autopilot`에 집중되어 있다**  
   전체 skill/agent 중 tool-level orchestration이 가장 명확하게 드러난 곳은 `sdd-autopilot`이다.

3. **일부 문서는 아직 Claude 스타일 pseudo syntax를 유지한다**  
   예를 들어 `guide-create`는 `Agent(subagent_type="write-phased")`, `implementation` agent는 `Task(subagent_type="general-purpose")` 같은 예시를 사용한다. 이는 개념적으로는 맞지만 Codex 런타임 계약으로는 불완전하다.

4. **Codex식 병렬화는 두 층으로 나뉜다**
   - 읽기/탐색 병렬화: `multi_tool_use.parallel`
   - 실행 병렬화: custom agent fan-out 또는 `spawn_agent`

5. **현재는 downstream parallel-ready 설계가 강하고, 실제 runtime fan-out은 제한적이다**
   `feature-draft`와 `implementation-plan`은 `Target Files`를 강제해 downstream 병렬 실행 준비는 잘 되어 있지만, 실제 Codex-native worker dispatch 규약은 `implementation`과 `sdd-autopilot`에 상대적으로 집중되어 있다.

---

## 2. 스킬 상세 카탈로그

### 2.1 스펙 관리 계열

| # | 스킬 | 유형 | 목적 | sub-agent 활용 | 병렬화 수준 | Codex 관점 평가 |
|---|------|------|------|----------------|-------------|------------------|
| 1 | **spec-create** | Full Skill | `_sdd/spec/` 신규 생성 및 부트스트랩 | `$write-phased` 전략 사용 | `multi_tool_use.parallel`로 탐색 병렬화 가능 | **중간** - 읽기 병렬화는 있으나 작성 fan-out은 약함 |
| 2 | **spec-update-todo** | Thin Wrapper | 구현 전 계획 변경을 스펙에 반영 | `spec_update_todo` agent 위임 | 순차 | **낮음** - sub-agent는 wrapper 수준 |
| 3 | **spec-update-done** | Thin Wrapper | 구현 완료 후 스펙 동기화 | `spec_update_done` agent 위임 | 순차 | **낮음** - drift 유형별 병렬화 없음 |
| 4 | **spec-review** | Thin Wrapper | 스펙 품질/드리프트 감사 | `spec_review` agent, 필요 시 nested `write_phased` | 순차 감사 | **중간** - 리뷰 깊이는 좋지만 fan-out 없음 |
| 5 | **spec-summary** | Full Skill | `SUMMARY.md` 생성 | `$write-phased` 전략 | 순차 | **낮음~중간** - 장문 작성 전략은 있으나 병렬 증거 수집이 없음 |
| 6 | **spec-snapshot** | Full Skill | 스펙 전체 스냅샷/번역 | 없음 | 순차 멀티파일 처리 | **낮음** - 파일 단위 병렬화 여지가 큼 |
| 7 | **spec-upgrade** | Full Skill | 기존 스펙을 whitepaper 형식으로 보강 | `$write-phased` + `multi_tool_use.parallel` | 부분적 | **중간** - gap 탐색 병렬화는 있으나 파일 생성 fan-out이 약함 |
| 8 | **spec-rewrite** | Full Skill | 장문 스펙 구조 재편 | 명시적 sub-agent 없음 | 순차 | **낮음** - split/rewrite 자체는 병렬 가능한데 현재는 수동 순차 흐름 |

### 2.2 기획/구현 계열

| # | 스킬 | 유형 | 목적 | sub-agent 활용 | 병렬화 수준 | Codex 관점 평가 |
|---|------|------|------|----------------|-------------|------------------|
| 9 | **feature-draft** | Thin Wrapper | 스펙 패치 초안 + 병렬 준비형 구현 계획 생성 | `feature_draft` agent 위임, nested `write_phased` 지원 | downstream 병렬화 지원 | **중간~높음** - 직접 fan-out은 약하지만 `Target Files` 설계가 강함 |
| 10 | **implementation-plan** | Thin Wrapper | 독립 실행 가능한 구현 계획 생성 | `implementation_plan` agent 위임, nested `write_phased` 지원 | downstream 병렬화 지원 | **중간~높음** - 병렬 실행 준비 품질이 높음 |
| 11 | **implementation** | Thin Wrapper | TDD 기반 구현 실행 | `implementation` agent 위임, 병렬 sub-agent 디스패치 지향 | **핵심 병렬화 포인트** | **높음** - conflict-aware 병렬화가 가장 구체적임 |
| 12 | **implementation-review** | Thin Wrapper | 계획/스펙 대비 구현 리뷰 | `implementation_review` agent 위임, nested `write_phased` | 순차 리뷰 | **중간** - severity 기반 review loop는 좋지만 리뷰 fan-out은 없음 |
| 13 | **guide-create** | Full Skill | 기능 가이드/기술 보고서 생성 | `write-phased` 위임 예시 존재 | related files 수에 따라 2-페이즈 | **중간** - 문서 생성 위임은 있으나 Codex-native syntax 보강 필요 |

### 2.3 PR 워크플로우 계열

| # | 스킬 | 유형 | 목적 | sub-agent 활용 | 병렬화 수준 | Codex 관점 평가 |
|---|------|------|------|----------------|-------------|------------------|
| 14 | **pr-spec-patch** | Full Skill | PR diff를 스펙 패치 초안으로 정리 | `$write-phased` 전략 | 순차 | **낮음~중간** - evidence 수집과 문서 작성이 단일 흐름 |
| 15 | **pr-review** | Full Skill | 스펙 기준 PR 검증 및 verdict 작성 | `$write-phased` 전략 | 순차 | **낮음~중간** - 검증 관점은 풍부하나 병렬 로딩/검증이 없음 |

### 2.4 보조/유틸리티 계열

| # | 스킬 | 유형 | 목적 | sub-agent 활용 | 병렬화 수준 | Codex 관점 평가 |
|---|------|------|------|----------------|-------------|------------------|
| 16 | **discussion** | Full Skill | 구조화된 토론 + 조사 | sub-agent 직접 호출 없음 | `multi_tool_use.parallel` 기반 읽기/리서치 병렬화 | **중간** - Codex의 병렬 read/research 사용이 가장 명확한 full skill |
| 17 | **write-phased** | Thin Wrapper | skeleton → fill 작성 전략 | `write_phased` agent 위임 | 독립 섹션/다중 파일에서 부분 병렬화 | **중간~높음** - 문서/코드 생성 backbone 역할 |
| 18 | **ralph-loop-init** | Thin Wrapper | 장시간 디버깅 루프 scaffold 생성 | `ralph_loop_init` agent 위임 | 순차 | **낮음** - setup 성격상 순차이나 검증 fan-out도 없음 |
| 19 | **sdd-autopilot** | Meta Skill | end-to-end SDD 파이프라인 오케스트레이션 | **직접 `spawn_agent(...)` 사용** | 부분 병렬화 + 전체는 순차 오케스트레이션 | **높음** - 실제 Codex orchestration 예시가 가장 많음 |

---

## 3. 에이전트 상세 카탈로그

| # | 에이전트 | 주요 기능 | nested sub-agent | 병렬 실행 메커니즘 | Codex 정합성 평가 |
|---|----------|-----------|------------------|-------------------|--------------------|
| 1 | **write_phased** | skeleton-first 장문 작성 | 없음 | 독립 섹션 초안 준비 병렬화 가능 | **중간~높음** - 생성 backbone은 좋고 설명도 명확함 |
| 2 | **implementation** | conflict-aware TDD 구현 | 일반 sub-agent fan-out 지향 | phase → parallel group → verify | **높음 / 단, syntax caveat** |
| 3 | **feature_draft** | 스펙 패치 + 병렬 준비형 계획 생성 | `write_phased` nested spawn 명시 | `Target Files`로 downstream 병렬화 지원 | **중간~높음** |
| 4 | **implementation_plan** | `Target Files` 기반 계획 생성 | `write_phased` nested spawn 명시 | downstream 병렬화 지원 | **중간~높음** |
| 5 | **implementation_review** | 3-tier 구현 리뷰 | `write_phased` nested spawn 명시 | 순차 리뷰 | **중간** |
| 6 | **spec_review** | 스펙 품질/드리프트 감사 | `write_phased` nested spawn 명시 | 순차 감사 | **중간** |
| 7 | **spec_update_todo** | 구현 전 계획 스펙 반영 | 없음 | 순차 | **낮음** |
| 8 | **spec_update_done** | 구현 후 스펙 동기화 | 없음 | 순차 | **낮음** |
| 9 | **ralph_loop_init** | ralph loop scaffold 생성 | 없음 | 순차 | **낮음** |

에이전트 계층에서 눈에 띄는 점은 다음과 같다.

- `implementation`이 **유일하게 병렬 worker execution contract를 가장 상세히 서술**한다.
- `feature_draft`, `implementation_plan`, `implementation_review`, `spec_review`는 모두 **nested `write_phased`**를 언급해 장문 산출물 일관성을 확보한다.
- `spec_update_todo`, `spec_update_done`, `ralph_loop_init`은 **전담 agent는 있지만 내부 분해 전략은 약하다**.

---

## 4. Sub-Agent / 병렬화 성숙도 분석

### 4.1 강점

1. **wrapper와 execution backbone이 분리되어 있다**  
   `.codex/agents/README.md`가 wrapper/custom agent/generated orchestrator의 역할을 명확히 구분한다. 이 덕분에 사용자-facing trigger와 실행 본문을 분리하기 쉽다.

2. **`implementation` agent의 병렬화 설계가 가장 성숙하다**  
   conflict graph, parallel groups, Target Files 경계, `UNPLANNED_DEPENDENCY` 보고, group 후 검증까지 포함한다. 단순 “병렬 가능” 수준이 아니라 **병렬 실행 후 통합 절차**까지 정의되어 있다.

3. **`feature-draft`와 `implementation-plan`이 downstream parallelization을 잘 준비한다**  
   모든 task에 `Target Files`를 요구해 실제 구현 단계에서 충돌 여부를 판단할 수 있게 한다. 즉, 직접 병렬화하지 않아도 병렬화 친화적 입력을 만든다.

4. **`discussion`, `spec-create`, `spec-upgrade`는 읽기/탐색 병렬화를 이미 받아들였다**  
   `multi_tool_use.parallel`를 활용해 로컬 탐색, 코드베이스 확인, 외부 리서치를 분리할 수 있도록 설계되어 있다.

5. **`sdd-autopilot`은 Codex에서 가장 실전적인 orchestration 예시다**  
   `spawn_agent(...)` 호출, review-fix loop, execute-verify, pre-flight check, pipeline log 등을 정의한다. skill 집합 전체를 엮는 메타 스킬 역할이 분명하다.

### 4.2 한계와 리스크

| 위치 | 현재 상태 | 리스크 | 개선 방향 |
|------|-----------|--------|-----------|
| **전반** | explicit `spawn_agent` 사용이 `sdd-autopilot`에 집중 | 다른 skill/agent는 “위임 개념”은 있지만 runtime contract가 약함 | 공통 호출 계약 문서화 |
| **implementation agent** | `Task(subagent_type="general-purpose")` 예시 사용 | Codex-native API와 1:1 대응이 모호함 | `spawn_agent`/`wait_agent` 기준 예시로 교체 |
| **guide-create** | `Agent(subagent_type="write-phased")` 예시 사용 | pseudo syntax 의존 | custom agent 호출 계약 명시 |
| **전체 skill set** | `wait_agent`, `send_input` 사용 예시 없음 | 장시간 작업/결과 수집/후속 보완 흐름이 불명확 | spawn 이후 lifecycle 패턴 추가 |
| **review/sync 계열** | 순차 리뷰/동기화 중심 | 대형 프로젝트에서 느리고 근거 수집 편향 가능 | 모듈/드리프트 유형별 fan-out |
| **multi-file writing 계열** | `write-phased`를 단일 writer로 사용하는 경향 | 긴 문서/다중 파일에서 병목 | component/file 단위 fan-out 후 merge |
| **spec-snapshot** | 파일별 번역을 순차 처리 | 가장 쉬운 병렬화 기회를 놓침 | 파일 manifest 후 병렬 번역 |

정리하면, **병렬화 아이디어는 충분하지만 실제 Codex 런타임 계약은 일부 파일에만 구체적**이다.

### 4.3 Codex 런타임 정합성 관점

Codex 기준으로 보면 현재 문서는 세 단계로 나뉜다.

#### A. Codex-native에 가까운 영역

- `sdd-autopilot`의 `spawn_agent(...)`
- `discussion`, `spec-create`, `spec-upgrade`의 `multi_tool_use.parallel`
- `implementation`의 Target Files 기반 write boundary

#### B. 개념은 맞지만 실행 계약이 모호한 영역

- `guide-create`의 `Agent(subagent_type="write-phased")`
- `implementation`의 `Task(subagent_type="general-purpose")`
- 여러 agent의 “nested spawn” 서술형 설명

#### C. 아직 Codex 병렬화와 거의 연결되지 않은 영역

- `spec-snapshot`, `spec-rewrite`, `spec-update-done`, `spec-update-todo`, `ralph-loop-init`
- `pr-review`, `pr-spec-patch`, `spec-summary`의 단일 writer 흐름

핵심 관찰은 다음과 같다.

1. **Codex에는 이미 explorer/worker/custom agent 개념이 있는데, 현재 문서는 이를 일관된 실행 문법으로 통일하지 못했다.**
2. **병렬화 설계가 "계획 출력물" 차원에서는 강하지만, "도구 호출" 차원에서는 일부만 구체적이다.**
3. **`wait_agent`가 전혀 언급되지 않아, spawned task의 완료 수집과 merge 규칙이 명문화되어 있지 않다.**
4. **worker ownership 지침은 `implementation`에 일부 있지만, 다른 skill에는 거의 전파되지 않았다.**

---

## 5. 개선 우선순위

### 5.1 P0 - 실행 계약 정합성 정리

가장 먼저 해야 할 일은 **“실제로 어떻게 sub-agent를 부를 것인가”를 Codex 기준으로 통일하는 것**이다.

우선 수정 대상:

- `.codex/agents/README.md`
- `.codex/agents/implementation.toml`
- `.codex/skills/guide-create/SKILL.md`
- `.codex/skills/sdd-autopilot/SKILL.md`

권장 변경:

1. `Agent(...)`, `Task(...)` 예시를 **Codex-native contract**로 교체한다.  
   최소한 아래 중 하나는 명시해야 한다.
   - 실제 `spawn_agent`/`wait_agent`/`send_input` 흐름
   - 또는 “이 구문은 pseudo example이며 실제 호출은 orchestrator layer가 수행”한다는 선언

2. **worker ownership template**를 공통화한다.  
   `implementation`의 Target Files 경계 규칙을 다른 fan-out 가능한 skill에도 재사용한다.

3. **spawn 이후 수집 절차**를 넣는다.  
   `sdd-autopilot`과 `implementation`에 “spawn → wait → verify → integrate” 순서를 명문화해야 한다.

4. **role mapping 표준화**를 문서화한다.  
   언제 custom agent를 쓰고, 언제 `explorer`/`worker`/`write_phased`를 쓰는지 기준을 분명히 한다.

### 5.2 P1 - 실제 병렬화 확장

ROI가 큰 병렬화 후보는 다음과 같다.

| 대상 | 현재 | 권장 확장 | 예상 효과 |
|------|------|-----------|-----------|
| **sdd-autopilot Step 3** | explorer 1회 중심 | 구조/패턴/테스트/스펙 상태를 병렬 explorer로 분리 | 초기 분석 시간 단축 |
| **sdd-autopilot Pre-flight** | 리소스 추정/대조 순차 | 런타임/환경변수/외부서비스/테스트를 병렬 점검 | 사전 점검 속도 향상 |
| **implementation-review** | 단일 리뷰 패스 | 모듈별 또는 severity pre-pass 병렬화 | 대규모 코드 리뷰 효율 상승 |
| **spec-review** | 순차 감사 | architecture/API/config drift를 병렬 감사 | 드리프트 감지 속도 향상 |
| **spec-update-done** | 순차 동기화 | spec file 또는 drift type 단위 fan-out | 스펙 동기화 시간 단축 |
| **spec-snapshot** | 파일별 순차 번역 | 파일 manifest 후 병렬 번역 worker fan-out | 가장 직접적인 속도 개선 |

특히 `spec-snapshot`은 의존성 충돌이 거의 없는 멀티파일 작업이라 **가장 쉽게 병렬화 이득을 얻을 수 있는 후보**다.

### 5.3 P2 - 문서형/리뷰형 스킬의 fan-out 강화

현재 `write-phased`는 backbone 역할을 잘 하지만, 호출부가 대부분 **단일 writer bottleneck**으로 남아 있다. 아래처럼 호출하는 쪽에서 fan-out을 만들어 주는 편이 효율적이다.

| 호출처 | 현재 | 권장 fan-out |
|--------|------|--------------|
| **spec-create** | 단일 또는 순차 작성 | `main.md` 인덱스 후 컴포넌트 spec 병렬 생성 |
| **spec-upgrade** | gap 분석 후 순차 작성 | §1~§8 보강 대상 파일/섹션별 병렬 작성 |
| **spec-rewrite** | 사용자 승인 후 순차 이동/재작성 | split map 기준 파일별 재작성 병렬화 |
| **guide-create** | guide 1개 단위 중심 | 복수 기능/복수 섹션 초안을 병렬 준비 |
| **pr-spec-patch** | spec + diff + report 순차 | 스펙 로딩, diff 분석, acceptance check 병렬 수집 |
| **pr-review** | verdict 보고서 단일 패스 | evidence 수집과 finding 초안 분리 |
| **spec-summary** | 단일 SUMMARY 생성 | 컴포넌트 요약 초안 병렬 생성 후 summary merge |

원칙은 단순하다.

- **`write-phased` 자체는 유지**
- **호출하는 skill/agent가 멀티파일/멀티섹션일 때 fan-out**
- **최종 patch/merge는 충돌 없이 순차 반영**

---

## 6. 권장 실행 로드맵

### Phase 1. 실행 계약 정리

- `.codex/agents/README.md`에 **Codex sub-agent invocation contract** 섹션 추가
- `.codex/agents/implementation.toml`의 `Task(...)` 예시를 Codex 기준으로 재작성
- `.codex/skills/guide-create/SKILL.md`의 `Agent(...)` 예시를 custom agent contract로 정리
- `.codex/skills/sdd-autopilot/SKILL.md`에 `wait_agent`/integration 규칙 보강

### Phase 2. 병렬화 고도화

- `spec-snapshot` 파일 단위 병렬 번역
- `spec-review` / `implementation-review`의 모듈별 리뷰 fan-out
- `spec-update-done`의 drift 유형별 병렬 수집
- `sdd-autopilot` 초기 exploration / pre-flight 병렬 분해

### Phase 3. writer fan-out 체계화

- `spec-create`, `spec-upgrade`, `spec-rewrite`에 multi-file write orchestration 도입
- `guide-create`, `pr-review`, `pr-spec-patch`, `spec-summary`의 증거 수집과 작성 단계를 분리
- `write_phased`를 nested backbone으로 유지하되, 호출부가 component/file ownership을 명시

### 최종 평가

현재 `.codex` 자산은 **구조 분리와 downstream parallel-ready 설계는 매우 좋다.**  
반면 **실제 Codex-native sub-agent 호출 계약과 lifecycle 관리가 균일하지 않다.**

따라서 우선순위는 다음 순서를 권장한다.

1. **문법/계약 통일**
2. **쉬운 멀티파일 작업부터 실제 병렬화**
3. **리뷰/문서 스킬로 fan-out 확장**

이 세 단계를 거치면 `.claude` 분석 문서에서 정리한 개선 방향을 Codex 런타임에 더 직접적으로 이식할 수 있다.

후속 검증은 `_sdd/CODEX_SKILLS_VERIFICATION_CHECKLIST.md`를 기준으로 진행한다.
