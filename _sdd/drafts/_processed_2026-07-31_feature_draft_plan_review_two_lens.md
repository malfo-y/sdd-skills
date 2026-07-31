# Feature Draft: plan-review 2-렌즈 분할 dispatch (실측 ∥ 판단)

> 규모 판정: 적격 — 변경 파일 4개(agent 미러 2벌 + SKILL wrapper 미러 2벌) + read-only census 1개, 변경 요소↔task 대응 1:1 눈검산 가능.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

plan-review는 체인에서 유일하게 병렬 파트너가 없는 단독 리뷰 단계다(실측 5회차 257~347s, 평균 ~294s). 시간 분해(transcript 실측): 최종 리포트 54~68%(166~216s) + 중반 추론 49~92s + 실측 도구 작업 15~25%. correctness task-shard 파일럿(spec 4.6.21)이 "finding이 나뉘면 리포트 생성이 나뉘어 벽시계가 준다"는 메커니즘을 검증했으므로, 같은 패턴을 plan-review에 적용한다 — 단 분할 축은 task가 아니라 **렌즈**다: plan-review의 가치 있는 finding은 섹션 교차·repo 대조형이라 task 축이 성립하지 않는다(배칭 draft 리뷰의 finding 9건 중 task 내부로 닫히는 것 0건 실측).

- **새 contract (agent — 호출자 렌즈 한정)**: `plan-review-agent`는 호출자가 렌즈를 한정하면 그 렌즈 소유분만 수행한다.
  - **실측 렌즈**: Step 3 supporting context 계단 + `Verification Weakness` smell + draft 사실 주장의 repo 대조. 도구 무거운 쪽.
  - **판단 렌즈**: 나머지 5 smell(Scope Creep·New File Justification·Single-use Abstraction·Task Boundary Drift·DRY Risk) + 규모 판정 검사 + Step 4(Decision and Assumption). draft 내부 근거(Hard Rule 5의 draft 섹션·task·AC 인용)로만 판정하고 Step 3 계단을 밟지 않는다 — repo 실측이 필요한 검증은 실측 렌즈 소유.
  - 렌즈 한정이 없으면 현행 전체(6 smell) 그대로 — 후방 호환. AC1의 "6개 smell"은 "소유한 smell 전부"로 일반화된다.
- **새 contract (wrapper → orchestrator)**: `plan-review` SKILL은 한 메시지에서 두 렌즈를 병렬 dispatch하고 반환을 병합 relay한다 — Blocker Status는 둘 중 하나라도 BLOCKED면 BLOCKED, findings는 합산, smell 판정은 합집합(각 smell이 정확히 한 렌즈에 소유되므로 중복 없음), 규모 판정 검사 결과는 판단 렌즈 반환에서 온다. 리뷰는 여전히 단일 패스다(렌즈 2개 = 한 패스의 병렬 분해이지 loop가 아님).
- **불변**: 새 agent 없음(동일 agent 2회 dispatch — 신규 agent 등록 census 리스크 회피), read-only leaf 병렬 안전성 동일, finding 반영은 호출자 소관, 리포트 파일 없음.
- **기대값(실측 기반)**: 판단 shard ≈ 추론 70~90s + 반쪽 리포트 ~110s ≈ ~200s, 실측 shard ≈ 도구 60~80s + 반쪽 리포트 ~100s ≈ ~170s → max ~200s vs 294s, **약 30% 절감**. 렌즈 간 finding 비중이 불균형하면(역대 finding이 Verification Weakness에 몰림) 이득이 이보다 작을 수 있다 — 효과 실측은 다음 feature 체인의 plan-review 게이트가 첫 관측 지점(머지+플러그인 갱신 후).

## Scope

- **In**: `.claude/agents/plan-review-agent.md` + `.codex/agents/plan-review-agent.toml`(3-way — codex 적응 delta 보존)의 렌즈 한정 절, `.claude/skills/plan-review/SKILL.md` + `.codex/skills/plan-review/SKILL.md`(3-way — Codex Runtime Adapter·framed payload 보존)의 orchestrator화.
- **Out**:
  - 새 agent 파일·marketplace 등록 변경 없음.
  - 6-smell rubric·severity·Blocker Policy·규모 판정 검사 내용 무변경 — 소유 렌즈 배정만 추가.
  - `feature-draft` SKILL(호출 주체) 무변경 — "plan-review 스킬 1회" 문면은 orchestrator 내부 분해와 무충돌.
  - simplicity 차원 분할은 별건 feature(다음 체인).
  - 효과(벽시계) 검증은 범위 밖 — 다음 체인의 plan-review 게이트에서 실측.
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: plan-review-agent 미러 2벌에 호출자 렌즈 한정 절 추가

agent가 렌즈 한정 dispatch를 계약으로 수용하게 한다. codex TOML은 단순 복사 금지 — 3-way(기존 codex 적응 delta 위에 절만 얹기).

**Contracts**:
- 새 절은 Part 1의 렌즈 정의(실측/판단 소유 목록)를 그대로 계약으로 옮긴다 — 재서술하지 않고 Part 1 정의를 단일 소스로 참조한다.
- **소유 경계 닫힘**: 실측 렌즈의 "draft 사실 주장 repo 대조" 소유는 판단 렌즈 소유 smell의 **사실 전제**(기존 파일의 수정 수용 가능성, 기존 로직/중복의 실재 여부 등)를 포함한다. 판단 렌즈는 그 전제를 draft 문면 기준으로 가정 판정하고 UNKNOWN을 내지 않는다 — repo 근거가 필요한 반증은 실측 렌즈 반환에서 온다.
- 렌즈 한정이 없으면 전체(6 smell) 수행 — 기존 경로 문자 단위 보존이 아니라 의미 보존(AC1 문구는 "소유한 smell 전부"로 일반화 허용).
- 반환 형식·severity·Blocker Policy·Hard Rules 무변경.

**Acceptance Criteria**:
- [ ] AC1: claude agent에 렌즈 한정 절이 있다 — 앵커 `호출자가 렌즈를 한정하면` + `실측`/`판단` 렌즈 이름 + 실측 소유(`Verification Weakness`와 Step 3 지시) + 판단 소유(`규모 판정 검사`와 Step 4 지시, `Step 3` 미수행 명시).
- [ ] AC2: 렌즈 미지정 경로가 명시된다 — `한정이 없으면` 전체 수행 앵커. AC1(자체 검증 절)의 smell 전수 문구가 렌즈 한정과 모순되지 않게 일반화된다(`소유` 앵커).
- [ ] AC3: codex TOML에 동일 규칙 앵커(AC1·AC2의 앵커)가 있고, `tomllib` 파싱이 통과하며, diff의 삭제 줄이 **AC2 일반화 대상 문구(smell 전수 문구) 계열에 한정**된다 — 그 외 기존 codex 적응 표면 삭제 0줄.
- [ ] AC4: 기존 계약 앵커 보존 — `단일 패스`·`Blocker Policy`·6-smell 표(smell 이름 6개 전부)·`Source Pointer`가 양 미러에 그대로 남는다.

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- 렌즈 한정 절 추가
- [M] `.codex/agents/plan-review-agent.toml` -- 동일 절 3-way 반영

### Task 2: plan-review SKILL 미러 2벌 orchestrator화 (2-렌즈 병렬 dispatch + 병합 relay)

thin wrapper(1 dispatch)를 2-렌즈 orchestrator로 바꾼다. codex는 어댑터(spawn_agent/wait_agent/close_agent·framed payload) 보존 3-way.

**Contracts**:
- claude: 한 메시지에서 같은 `plan-review-agent`를 렌즈 지정 digest로 2회 병렬 dispatch(실측·판단). codex: spawn 2회 + `wait_agent` targets 2개 id.
- 병합 relay: Blocker Status는 하나라도 BLOCKED면 BLOCKED, findings 합산, smell 판정 합집합(각 smell 정확히 한 렌즈 소유 — 중복 없음), 규모 판정 검사 결과는 판단 렌즈 반환.
- 보존: `wrapper는 새 분석 read를 하지 않는다`(orchestrator도 동일), 단일 패스, 흉내 금지 경계, Model override(모든 dispatch에 적용으로 일반화), Source Pointer.

**Acceptance Criteria**:
- [ ] AC1: claude SKILL에 `한 메시지` + 두 렌즈 dispatch(`실측`·`판단` 앵커 각 1회 이상) + 병합 규칙 앵커(`하나라도 BLOCKED`·`합집합`·`정확히 한 렌즈`)가 있다.
- [ ] AC2: codex SKILL에 동일 병합 규칙 앵커가 있고, `spawn_agent`가 렌즈 2회를 표현하며 `wait_agent` targets가 2개 id를 수거한다. `Runtime Boundary`·`Input Data` 앵커 보존.
- [ ] AC3: 경계 앵커 보존 — `새 분석 read를 하지 않는다`·`단일 패스`·`흉내내지 않는다`·`Model override`(적용 대상이 모든 dispatch로 일반화된 형태)가 양 미러에 남는다.

**Target Files**:
- [M] `.claude/skills/plan-review/SKILL.md` -- orchestrator화
- [M] `.codex/skills/plan-review/SKILL.md` -- 3-way 반영

### Task 3: 변경 격리·정합 census (read-only 검증)

**Acceptance Criteria**:
- [ ] AC1: `git diff --name-only`가 계획 4파일 + 프로세스 산출물(draft·work_log)만 보인다 — 다른 skill/agent 파일 diff 0.
- [ ] AC2: git 추적 파일 대상 정합 census — 렌즈 이름(`실측 렌즈`·`판단 렌즈`)이 계획 4파일 밖에 0건(spec·drafts·work_log·append-only 로그 제외), wrapper의 구 단일 dispatch 잔존 표현(`wait_agent({targets: ["<agent_id>"]` 고정 1-id)이 codex plan-review SKILL에 0건. census 패턴은 regex 메타문자(`{`·`[`)를 포함하므로 **fixed-string 검색(`grep -F`)으로 수행**한다.
- [ ] AC3: spec 인계 표면이 라인 번호로 열거된다 — `_sdd/spec/` live 파일에서 plan-review를 wrapper/단일 dispatch로 서술하는 위치(grep 출력)를 spec-sync 인계 목록으로 채팅에 노출.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- **효과 실측은 다음 체인 소관**: plan-review SKILL은 메인 루프가 플러그인 설치본에서 로드하므로(plugin cache lag) 이 세션에서 발효 검증 불가. 머지+플러그인 갱신 후 **다음 feature(simplicity 차원 분할)의 plan-review 게이트가 첫 관측 지점**이다. 판정 밴드: max(렌즈 shard) ≤ ~220s면 지지, ~300s+면 리포트 불균형/고정비 지배로 재고(사용자 보고 후 결정). 사용자 확인 불요(방향 합의됨).
- **렌즈 균형 리스크(정직)**: 역대 finding이 Verification Weakness에 몰리는 경향이 있어 실측 shard의 리포트가 반보다 클 수 있다 — 그 경우 이득이 30%보다 작다. 렌즈 재배분은 실측 후 별건. 사용자 확인 불요.
- **이 draft의 게이트는 1+N 첫 정식 런**: 이번 구현 게이트는 방금 발효된 implementation-review 1+N이 draft task 3개로 correctness shard 3개를 만드는 첫 실전이다 — 파일럿 재현 데이터를 겸한다. 사용자 확인 불요.
