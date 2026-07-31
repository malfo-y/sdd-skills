# Feature Draft: simplicity reviewer의 차원 묶음 분할 dispatch (참조 ∥ 국소)

> 규모 판정: 적격 — 변경 파일 4개(agent 미러 2벌 + implementation-review SKILL 미러 2벌) + read-only census 1개, 변경 요소↔task 대응 1:1 눈검산 가능.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

correctness task-shard(4.6.21)와 plan-review 2-렌즈(4.6.22)로 게이트의 다른 구간이 내려간 지금, simplicity(실측 107~252s, 시간의 56~96%가 리포트 — 출처: 이 세션 transcript 구간 계측, `_sdd/work_log/2026-07-31.md`의 리뷰 시간 분해 기록; spec에는 107s·120s만 기록됨)가 implementation-review 게이트의 임계 경로가 될 차례다. simplicity를 **차원 묶음 2개로 분할 dispatch**한다 — 분할 축은 task가 아니라 **차원**이다.

- **task 축 반대 논거의 지위 (supersede 아님, 공존)**: 4.6.21의 "simplicity는 task로 자르지 않는다 — 중복 탐지는 두 지점을 같이 봐야 한다"는 여전히 유효하다. 차원 분할은 그 논거를 위반하지 않는다: **한정되는 것은 차원이지 범위가 아니므로 각 shard가 전체 변경을 본다** — 중복 렌즈를 소유한 shard는 여전히 모든 지점을 동시에 관찰한다.
- **새 contract (agent — 호출자 차원 한정)**: `simplicity-review-agent`는 호출자가 차원 묶음을 한정하면 그 묶음만 스캔하고 반환의 차원 판정도 소유 차원만 낸다.
  - **참조 묶음**: 중복 코드 + 죽은 코드 + 단일 사용처 추상화 — 셋 다 사용처/복제 추적형(Grep 무거움: 복제 지점·호출처 유무·사용처 수).
  - **국소 묶음**: 도달 불가 에러 처리 + 과잉압축 — 코드 자리 판독형.
  - 어느 묶음이든 **리뷰 범위는 전체 변경**이다(한정은 차원이지 범위가 아니다). 자체 검증 AC1의 "5개 차원" 문구는 "소유한 차원"으로 일반화한다(다른 자체 검증 AC는 차원-중립이라 무변경 — plan-review 2-렌즈 게이트에서 잡힌 무조건 문구 모순의 재발 방지를 설계 시점에 반영).
  - 차원 한정이 없으면 전체(5개 차원) 수행 — 후방 호환. `pr-review`는 이 경로로 무변경 동작한다.
- **새 contract (implementation-review orchestrator)**: simplicity를 묶음마다 1회, 총 2회 dispatch한다(참조 ∥ 국소, 각각 전체 변경 대상) — correctness shard들과 합쳐 **한 메시지 N+2 병렬**. relay의 차원 판정은 두 반환의 합집합(각 차원이 정확히 한 묶음 소유 — 중복 없음), 합산 severity는 모든 반환 대상(기존 문면 그대로).
- **기대값(실측 기반)**: simplicity 시간의 지배분이 리포트(56~96%)이고 finding이 차원별로 갈리므로, 리포트 분할 메커니즘(4.6.21·4.6.22에서 2회 검증됨)이 그대로 적용된다 — shard당 ~70~140s, 게이트 벽시계는 max(correctness shard, simplicity shard)로 수렴.

## Scope

- **In**: `.claude/agents/simplicity-review-agent.md` + `.codex/agents/simplicity-review-agent.toml`(3-way — codex 적응 delta 보존)의 차원 한정 절, `.claude/skills/implementation-review/SKILL.md` + `.codex/skills/implementation-review/SKILL.md`(3-way — Runtime Adapter 단일 소스 유지)의 simplicity 2-shard dispatch 문면.
- **Out**:
  - 새 agent·5개 차원 정의·Severity Rules·Falsifiable-only 규칙 무변경 — 소유 묶음 배정만 추가.
  - `pr-review` SKILL 2벌 무변경 — 차원 한정 없는 호출은 전체 5차원 후방 호환 경로.
  - correctness shard 계약(4.6.21)·plan-review 2-렌즈(4.6.22) 무변경.
  - 효과(벽시계) 검증은 범위 밖 — 이 feature의 구현 게이트 자체가 첫 실측이다(발효 전이므로 메인 루프가 수동으로 simplicity×2를 포함해 dispatch).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: simplicity-review-agent 미러 2벌에 호출자 차원 한정 절 추가

**Contracts**:
- 새 절은 Part 1의 묶음 정의(참조/국소)를 그대로 계약으로 옮긴다 — 재서술 없이 단일 소스 참조. 두 묶음의 합집합 = 정확히 5개 차원(누락·중복 배정 없음).
- **범위 불변 명시**: 차원 한정 dispatch도 리뷰 범위는 전체 변경이다 — 한정은 차원이지 범위가 아니다.
- 자체 검증 AC1은 "소유한 차원(한정 시 그 묶음, 한정 없으면 5개 전부)"으로 일반화. 차원 판정 반환도 소유 차원만.
- **무조건 "5개" 문면 전수 일반화**: 자체 검증 밖의 무조건 문구 3곳 — Hard Rule 3(`정확히 Review Dimensions의 5개`), Review Dimensions 도입부(`정확히 아래 5개 차원으로만`), Step 2(`5개 차원 각각을 스캔`) — 도 소유 차원 조건화로 일반화한다(그 외 차원 finding 금지 취지는 유지: "소유하지 않은 차원으로 finding을 내지 않는다"). Integration의 pr-review 서술(`호출자 무관 단일 계약`)은 "차원 한정 없는 호출은 전체 5차원" 후방 호환 서술로 갱신. 반환 형식·Severity Rules·그 외 Hard Rules 무변경.
- 한정 없으면 전체 5차원 수행(후방 호환 — pr-review 경로).

**Acceptance Criteria**:
- [ ] AC1: claude agent에 차원 한정 절 앵커가 있다 — `호출자가 차원 묶음을 한정하면` + `참조 묶음`/`국소 묶음` + 참조 소유 3차원(`중복 코드`·`죽은 코드`·`단일 사용처 추상화`)과 국소 소유 2차원(`도달 불가 에러 처리`·`과잉압축`)이 절 안에 배정 + `한정은 차원이지 범위가 아니다` 범위 불변 앵커.
- [ ] AC2: 한정 미지정 경로 앵커(`한정이 없으면`)가 있고, 자체 검증 AC1이 `소유한 차원`으로 일반화되며 무조건 문구 계열이 잔존 0건 — `5개 차원을 **각각 능동 스캔**했고, 5개 전부가`·`정확히 Review Dimensions의 5개`·`정확히 아래 5개 차원으로만`·`5개 차원 각각을 스캔`·`호출자 무관 단일 계약` 전부.
- [ ] AC3: codex TOML에 AC1·AC2와 동일 앵커가 있고 `tomllib` 파싱이 통과하며, diff 삭제 줄이 일반화 대상 문구 계열(`5개` 또는 `호출자 무관`)에 한정된다.
- [ ] AC4: 기존 계약 앵커 보존 — `표적 disjoint`·`Falsifiable-only`·5개 차원 이름 전부·`Source Pointer`·`단일 패스`가 양 미러에 남는다.

**Target Files**:
- [M] `.claude/agents/simplicity-review-agent.md` -- 차원 한정 절 추가
- [M] `.codex/agents/simplicity-review-agent.toml` -- 동일 절 3-way 반영

### Task 2: implementation-review SKILL 미러 2벌에 simplicity 2-shard dispatch 반영

**Contracts**:
- 실행 2의 simplicity 문면을 교체한다: "분할하지 않고 전체 변경 대상으로 1회" → 묶음마다 1회(참조 ∥ 국소), **각 dispatch는 전체 변경 대상**(중복 렌즈의 두 지점 동시 관찰 유지 — 기존 근거 문장을 이 형태로 계승). correctness shard들과 같은 한 메시지에 낸다(N+2).
- relay: 차원 판정은 두 simplicity 반환의 합집합(각 차원 정확히 한 묶음 소유). 합산 severity "모든 반환" 문면은 이미 N+2를 포섭하므로 무변경.
- codex는 3-way — Runtime Adapter 블록이 문법 단일 소스인 구조 유지. spawn 예시에 simplicity 묶음 슬롯 반영, **wait 예시의 simplicity id도 복수화**(`<simplicity_id>` 단수 placeholder → 묶음 복수 표현; correctness 슬롯만 가변인 현행 실측과 불일치했던 지점).
- 보존: correctness 분할표·비분할 경로·review-only 경계·병렬 안전성(read-only leaf — simplicity shard 수와 무관 서술로 자연 확장).

**Acceptance Criteria**:
- [ ] AC1: claude SKILL에 simplicity 묶음 dispatch 앵커가 있다 — `참조`·`국소` + `묶음마다 1회` + `각 dispatch는 전체 변경 대상` + 구 문면(`simplicity는 분할하지 않고`) 잔존 0건.
- [ ] AC2: relay 문면에 전체 구절 앵커 `각 차원 정확히 한 묶음 소유`가 있고(기존 문장 "합집합 exit 판정은 하지 않는다"가 이미 있어 `합집합` 단독 앵커는 pre-change에도 매치되는 위장 앵커 — 사용 금지), correctness ledger 연접·`모든 반환` 합산·dedup 호출자 소관 앵커가 보존된다.
- [ ] AC3: codex SKILL에 동일 앵커가 있고, Runtime Adapter 블록의 spawn 예시가 simplicity 묶음을 표현하며 wait 예시의 simplicity id가 복수화된다. `동시 spawn`(codex — `한 메시지`는 codex에 부재한 리터럴이라 앵커로 쓰지 않는다)·`Runtime Boundary`·`Input Data` 앵커 보존. 실행 절에 call 문법 재기재 0(어댑터 단일 소스 유지).
- [ ] AC4: 경계 앵커 보존 — `relay만 한다`·`합산 요약은 relay이지 gating이 아니다`·`read-only leaf`가 양 미러에 남는다.

**Target Files**:
- [M] `.claude/skills/implementation-review/SKILL.md` -- simplicity 2-shard dispatch
- [M] `.codex/skills/implementation-review/SKILL.md` -- 3-way 반영

### Task 3: 변경 격리·정합 census (read-only 검증)

**Acceptance Criteria**:
- [ ] AC1: `git diff --name-only`가 계획 4파일 + 프로세스 산출물(draft·work_log)만 보인다 — `pr-review` SKILL 2벌·다른 agent 파일 diff 0.
- [ ] AC2: git 추적 파일 대상 census(`grep -F`) — 묶음 이름(`참조 묶음`·`국소 묶음`)이 계획 4파일 밖 0건(spec·drafts·work_log·append-only 로그 제외), 구 문면(`simplicity는 분할하지 않고`)이 repo 전체 0건(spec은 spec-sync 인계로 제외).
- [ ] AC3: spec 인계 표면이 라인 번호로 열거된다 — `_sdd/spec/` live 파일에서 simplicity 통짜/비분할을 서술하는 위치(grep 출력)를 spec-sync 인계 목록으로 채팅에 노출.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- **게이트 = 첫 실측 (사용자 합의된 패턴)**: 이 feature의 구현 게이트에서 발효 전이지만 메인 루프가 수동으로 correctness shard N + simplicity×2(참조/국소)를 한 메시지 dispatch해 실측한다. 판정: simplicity shard 벽시계가 통짜 실측(107~252s) 유의미 하회 + finding 품질 유지(차원 합집합 누락 0)면 지지. 사용자 확인 불요.
- **묶음 불균형 리스크(정직)**: 역대 simplicity finding이 중복 차원에 몰려 참조 shard 리포트가 클 수 있다 — 그 경우 이득이 리포트 반분 가정보다 작다. 재배분은 실측 후 별건. 사용자 확인 불요.
- **이 draft의 plan-review 게이트가 2-렌즈 첫 실측**이다(4.6.22 발효 후 첫 draft) — 판정 밴드 max(렌즈 shard) ≤ ~220s 지지 / ~300s+ 재고를 이 게이트에서 관측해 기록한다. 사용자 확인 불요.
