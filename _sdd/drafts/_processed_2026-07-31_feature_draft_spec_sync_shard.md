# Feature Draft: spec-sync의 표면 묶음 분할 dispatch (본문 ∥ 기록)

> 규모 판정: 적격 — 변경 파일 4개(agent 미러 2벌 + SKILL wrapper 미러 2벌) + read-only census 1개, 변경 요소↔task 대응 1:1 눈검산 가능.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

리뷰 3종 병렬화(4.6.21~4.6.23) 후 체인의 최장 단독 구간은 spec-sync다(실측 245~445s — 세션 transcript 구간 계측, work_log에는 445s와 구간 비율만 기록; 분해 = 분석 ~35% / **집필 ~50%** / 리포트 ~12%). 집필 대상 파일이 성격상 둘로 나뉘고 쓰기 집합이 서로소이므로 **표면 묶음 2개로 분할 dispatch**한다. 이는 read-only reviewer가 아닌 **첫 작성자 분할**이다 — 병렬 안전성의 근거가 "파일을 안 쓴다"가 아니라 "쓰기 집합이 서로소다"로 바뀐다.

- **새 contract (agent — 호출자 표면 한정)**: `spec-sync-agent`는 호출자가 표면 묶음을 한정하면 그 묶음의 파일만 쓰고, 반환 Report도 소유 파트만 낸다.
  - **본문 묶음**: live truth 표면(`main.md`·`components.md`·`usage-guide.md` 등 — 기록 파일 제외 전부)의 갱신 + outdated claim 제거 + delta의 evidence 검증·승격(Status Routing의 실행 주체). Report의 Change Summary·Applied Updates·Planned·Open Questions 파트 소유.
  - **기록 묶음**: `decision_log.md`·`logs/changelog.md`의 append-only 신규 entry + input file `_processed_` rename. Report의 Processed Input Files 파트 소유. delta의 사실·분류는 orchestrator digest의 선고정 값을 기록 근거로 쓴다(코드 재검증은 본문 묶음 소유 — 기록은 history이지 truth 승격이 아니다). append-only는 이 계약이 **신규로 명시하는 불변식**이다 — 기존 Hard Rule 11은 "최소 갱신"만 규정했다.
  - **쓰기 서로소 불변식**: 본문 묶음은 기록 파일을 쓰지 않고, 기록 묶음은 live truth 파일을 쓰지 않는다. 이것이 작성자 병렬의 안전 근거다.
  - **read-vs-rename 경합 허용**: 병렬 실행 중 기록 묶음의 `_processed_` rename이 본문 묶음의 input 읽기보다 먼저 닿을 수 있다 — 본문 묶음은 input 파일을 **원 이름과 `_processed_` 이름 양쪽으로 조회**한다(기존 slug glob `*_feature_draft_*`가 양쪽에 매칭되므로 glob 경로는 이미 경합 내성이 있고, 정확 경로 지정 시에만 양쪽 시도가 필요).
  - 자체 검증 AC·Hard Rule의 무조건 문구는 소유 조건화로 **전수** 일반화한다(단일 Report → 소유 파트 Report, `_processed_` 마킹 → 기록 소유, Hard Rule 11 decision_log 갱신 → 기록 소유). 한정 없으면 전체 수행 — 후방 호환.
- **새 contract (SKILL wrapper → orchestrator)**: evidence 있는 implemented sync면 한 메시지에서 두 묶음을 병렬 dispatch한다. 구현 전 planned 경로(쓰기 소량)는 현행 1회 유지.
  - **선고정(공유 사실의 단일 결정자)**: orchestrator가 digest에 고정해 넘긴다 — delta 목록과 대화 기반 분류 근거, **신규 spec 버전 번호**(대화에서 미상이면 `main.md` 헤더 버전만 targeted grep 1회 허용 — "새 분석 read 없음" 원칙의 명시 예외), 결정 제목. 두 shard가 각자 도출하지 않는다.
  - **사후 정합 검사(orchestrator 소유, grep 2종)**: ① `main.md` 헤더 버전 == `changelog.md` 최신 entry 버전, ② `git diff`에서 decision_log·changelog 삭제 줄 0(append-only). 불일치면 relay에 명시하고 fix는 호출자 소관.
  - 병합 relay: 두 부분 Report를 하나의 Spec Sync Report 구조로 합쳐 전달(각 파트가 정확히 한 묶음 소유라 중복 없음).
- **기대값(실측 기반)**: shard ≈ 축소된 분석(선고정으로 재검증 범위 감소) + 반쪽 집필 + 부분 리포트 ≈ ~180~200s vs 245~445s. 집필이 파일 단위로 갈리므로 리포트 분할 메커니즘(3회 검증됨)과 동형.

## Scope

- **In**: `.claude/agents/spec-sync-agent.md` + `.codex/agents/spec-sync-agent.toml`(3-way)의 표면 한정 절, `.claude/skills/spec-sync/SKILL.md` + `.codex/skills/spec-sync/SKILL.md`(3-way — Codex Runtime Adapter 보존)의 orchestrator화.
- **Out**:
  - Status Routing 4분류·Repo-wide Invariant Test·surface 매핑 규칙·Report 구조 무변경 — 소유 배정만 추가.
  - planned 경로(구현 전 호출) 분할 없음 — evidence 있는 implemented sync만 분할.
  - 새 agent·파일 없음. `_sdd/spec/` 문서 자체는 이 feature의 수정 대상 아님(spec-sync 단계 소관).
  - 효과 검증: 이 체인의 마지막 spec-sync 단계가 파일럿(발효 전 수동 2-shard dispatch — 기존 합의 패턴).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: spec-sync-agent 미러 2벌에 호출자 표면 한정 절 추가

**Contracts**:
- 새 절은 Part 1의 묶음 정의(본문/기록)를 단일 소스로 옮긴다 — 재서술 없이. 쓰기 서로소 불변식과 read-vs-rename 경합 허용(본문의 원 이름/`_processed_` 양쪽 조회)을 명시한다.
- 기록 묶음의 근거 규칙: digest 선고정 값(항목 목록은 Part 1 선고정 정의가 canonical)을 기록 근거로 쓰고 코드 재검증을 하지 않는다 — 재검증은 본문 묶음 소유.
- **무조건 문구 전수 조건화**: AC의 `_processed_*`로 마킹(기록 소유)·단일 `Spec Sync Report` 작성(소유 파트로 일반화), Hard Rule 11의 decision_log 갱신(기록 소유), Step 7의 rename(기록 소유), Output Format의 단일 Report(부분 Report 허용 — 한정 시). 구현 중 발견되는 추가 무조건 표면도 같은 방식으로 조건화하고 census에 등재한다.
- 한정 없으면 전체 수행(후방 호환). Status Routing·Invariant Test·Hard Rule 1(대상은 `_sdd/spec/`뿐)·기타 Hard Rules 무변경.

**Acceptance Criteria**:
- [ ] AC1: 양 미러에 표면 한정 절 앵커 — `호출자가 표면 묶음을 한정하면` + `본문 묶음`/`기록 묶음` + 절 안에 본문 소유(live truth 갱신·evidence 검증)와 기록 소유(`decision_log`·`changelog`·`_processed_`) 배정 + 쓰기 서로소 앵커(`쓰지 않는다` 상호 불가침 2문장) + read-vs-rename 경합 앵커(`양쪽으로 조회`).
- [ ] AC2: 한정 미지정 경로 앵커(`한정이 없으면`)가 있고, AC·Hard Rule 11·Step 7의 무조건 문구가 소유 조건화된다 — 조건화 앵커(`기록 묶음 소유` 또는 `소유 파트`)가 해당 위치들에 존재.
- [ ] AC3: codex TOML에 동일 앵커가 있고 `tomllib` 파싱 통과, diff 삭제 줄이 조건화 대상 문구 계열에 한정.
- [ ] AC4: 기존 계약 앵커 보존 — `Status 분류 (Routing)`·`Repo-wide Invariant Test`·`evidence 없으면 승격 금지`·`🚧 Planned`·`Source Pointer`가 양 미러에 남는다.

**Target Files**:
- [M] `.claude/agents/spec-sync-agent.md` -- 표면 한정 절 추가
- [M] `.codex/agents/spec-sync-agent.toml` -- 동일 절 3-way 반영

### Task 2: spec-sync SKILL 미러 2벌 orchestrator화 (본문 ∥ 기록 병렬 dispatch + 선고정 + 사후 정합)

**Contracts**:
- implemented sync(evidence 있음) 판별 시: 한 메시지에서 본문·기록 두 묶음 병렬 dispatch. planned 경로는 현행 1회 — 분기 조건을 문면에 명시.
- **선고정**: digest에 Part 1 선고정 정의의 항목들을 고정(목록은 Part 1이 canonical). 버전이 대화에서 미상이면 `main.md` 헤더 버전만 targeted grep 1회 허용(명시 예외 — 그 외 새 분석 read 없음 유지).
- **사후 정합 검사**: dispatch 완료 후 orchestrator가 grep 2종 수행 — 버전 일치(main.md 헤더 == changelog 최신 entry), append-only(git diff에서 두 기록 파일 삭제 줄 0). 불일치는 relay에 명시(fix는 호출자 소관 — orchestrator는 gating하지 않는다).
- 병합 relay: 두 부분 Report를 단일 Report 구조로 연접(각 파트 정확히 한 묶음 소유). codex는 3-way — Runtime Adapter 블록이 호출·수거·payload 단일 소스(spawn 2, wait targets 2 id).
- 보존: entrypoint 계약·흉내 금지·`> Source:` 포인터(wrapper 쪽 실제 앵커 — agent의 `Source Pointer`와 문면이 다름).

**Acceptance Criteria**:
- [ ] AC1: claude SKILL에 분기 앵커(`evidence` 유무로 implemented/planned 분기 + planned는 `1회`) + `한 메시지` 병렬 dispatch + `본문`/`기록` 묶음 앵커.
- [ ] AC2: 선고정 앵커 — `선고정` + 고정 항목(버전 번호·delta) + targeted grep 예외 문장(`main.md` 헤더 + `1회`)이 있다.
- [ ] AC3: 사후 정합 앵커 — 버전 일치 검사와 append-only(삭제 줄 0) 검사 서술 + `gating하지 않는다`.
- [ ] AC4: codex SKILL에 동일 규칙 앵커 + `spawn_agent` 2회 표현(본문/기록) + `wait_agent` targets 2 id + `Runtime Boundary`·`Input Data` 보존 + 실행 절 call 문법/payload 재기재 0(어댑터 단일 소스).
- [ ] AC5: 병합 relay 앵커 — `각 파트가 정확히 한 묶음 소유` + 부분 Report 연접 서술.

**Target Files**:
- [M] `.claude/skills/spec-sync/SKILL.md` -- orchestrator화
- [M] `.codex/skills/spec-sync/SKILL.md` -- 3-way 반영

### Task 3: 변경 격리·정합 census (read-only 검증)

**Acceptance Criteria**:
- [ ] AC1: `git diff --name-only`가 계획 4파일 + 프로세스 산출물(draft·work_log)만 보인다.
- [ ] AC2: git 추적 파일 census(`grep -F`) — 묶음 이름(`본문 묶음`·`기록 묶음`)이 계획 4파일 밖 0건(spec·drafts·work_log 제외), wrapper 구 단일 dispatch 표현(codex `wait_agent({targets: ["<agent_id>"]` 고정 1-id)이 spec-sync SKILL에 0건, **무조건 문구 잔존 0건** — agent 미러에서 조건화 대상 구 문구(`단일 \`Spec Sync Report\`를 작성했다` 무조건형·무조건 rename 지시·Hard Rule 11 무조건형) 계열이 소유 조건 없이 남지 않는다.
- [ ] AC3: spec 인계 표면 열거 — `_sdd/spec/` live 파일에서 spec-sync를 단일 진입점/wrapper/단일 dispatch로 서술하는 위치(grep 출력)를 spec-sync 인계 목록으로 채팅에 노출.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- **게이트 + 파일럿 (사용자 합의된 패턴)**: 구현 게이트는 발효본 N+2(correctness shard 3 + simplicity 참조∥국소)로 돌고, **이 체인의 마지막 spec-sync 단계를 발효 전 수동 2-shard(본문 ∥ 기록)로 dispatch해 파일럿 실측**한다. 판정: shard 벽시계 ~200s대 + 사후 정합 검사 통과면 지지, ~300s+ 또는 정합 불일치면 머지 전 재고(사용자 보고 후 결정). 사용자 확인 불요.
- **선고정 실패 리스크(정직)**: 기록 묶음이 digest 사실만으로 entry를 쓰므로, digest가 틀리면 기록이 틀린다 — 완화는 사후 정합 검사(버전)와 기존 append-only 규율뿐이고, 내용 오류는 다음 spec-review/체인에서 잡힌다. 이 trade-off는 의도된 것(재검증 중복 제거가 분할 이득의 절반). 사용자 확인 불요.
- **plan-review 2-렌즈 관측 표본 2**: 이 draft의 plan-review 게이트가 두 번째 관측이다 — 밴드 기록. 사용자 확인 불요.
