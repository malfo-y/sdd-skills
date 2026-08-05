# Feature Draft: Decisions and Assumptions 5필드 계약 제거 (산문 복귀)

> 규모 판정: 적격 — 변경 요소 3개(producer 템플릿·reviewer 계약·정의 문서)가 task 3개에 1:1 대응하고 총 6파일로 단일 컨텍스트에 담긴다. 제거/전파류라 census형 신호 있음 → Part 2 마지막에 read-only 검증 task 예약.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

v4.6.33(커밋 99a6bd5)이 도입한 두 계약 중 `Decisions and Assumptions` 조건부 5필드 계약만 제거하고 producer·reviewer를 커밋 이전 산문 수준으로 복귀한다. `Propagation Surfaces` 계약은 유지한다. 근거: D&A는 실패 이력 없는 곳에 형식을 추가한 것으로, 유용한 알맹이(사용자 확인 필요 결정의 구현 전 노출)는 기존 `Open Questions` 표면이 이미 담당한다. 5필드 구조는 형식 준수 검사로 퇴화하기 쉽다(산문 규칙 > 의사코드 관측과 정합).

- 제거되는 계약: feature draft의 조건부 `Decisions and Assumptions` 섹션(5필드: `Decision / Assumption`·`Evidence`·`Rejected alternatives`·`Confidence`·`User confirmation needed`)과 plan-review의 동일 조건·필드 검사.
- 복귀되는 계약(신규 아님, 99a6bd5^ 원문 복원): plan-review Hard Rule 7은 산문 규칙 — "결과 방향을 바꿀 수 있는 모호성·Target Files 선택·task boundary 결정은 draft 안에서 가정·대안·확신도·사용자 확인 필요 여부가 드러나야 한다. 숨은 결정은 `Verification Weakness` 또는 별도 finding."
- global spec 반영(spec-sync 소관): `_sdd/spec/main.md` Guardrail의 producer↔reviewer 계약 항목에서 decision 절반 제거(propagation 절반 유지) + 버전 bump. `_sdd/spec/components.md`의 `feature-draft`·`plan-review` 행에서 "중요 결정 조건부 5필드" 문구 제거(propagation 문구 유지). decision_log·changelog entry 추가.

## Scope
- **In**: `Decisions and Assumptions` 템플릿·Hard Rule·reviewer 검사 항목의 제거와 산문 복귀 — producer SKILL 2벌, plan-review-agent 2벌, SDD_SPEC_DEFINITION 한·영.
- **Out**: `Propagation Surfaces` 계약 일체(템플릿·producer Hard Rule·reviewer Hard Rule 8·Step 2/3의 propagation 추출·검증), plan-review 2-렌즈 구조, Verification Weakness 행의 propagation 검사 문구, 과거 기록물(`_sdd/implementation/`·`_sdd/discussion/`·decision_log·changelog 기존 entry).
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | producer D&A 템플릿·Hard Rule 제거 + Process 1 문장 복귀 | `.claude/skills/feature-draft/SKILL.md`, `.codex/skills/feature-draft/SKILL.md` | `grep -l 'Decisions and Assumptions' .claude/skills/feature-draft/SKILL.md .codex/skills/feature-draft/SKILL.md` → 현재 2파일, 완료 후 0파일 (두 파일은 byte-identical 미러 — `diff -q` 무출력 실측) | Task 1 |
| P2 | reviewer AC3·smell 7·Step 2·Step 4 산문 복귀 | `.claude/agents/plan-review-agent.md`, `.codex/agents/plan-review-agent.toml` | `grep -l '5필드' <두 파일>` → 현재 2파일, 완료 후 0파일 | Task 2 |
| P3 | draft canonical 구조 정의에서 D&A 항목·스켈레톤 제거 | `docs/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_SPEC_DEFINITION.md` | ko: `grep -l 'Decisions and Assumptions' docs/SDD_SPEC_DEFINITION.md`, en: `grep -l 'five fields' docs/en/SDD_SPEC_DEFINITION.md` → 현재 각 1파일, 완료 후 0파일 | Task 3 |

# Part 2: Tasks

### Task 1: producer(feature-draft SKILL) D&A 제거

두 SKILL.md 미러에서 D&A 템플릿·Hard Rule을 제거하고 Process 1 문장에서 중요 결정 식별 절을 걷어낸다(propagation 식별 절은 유지).

**Acceptance Criteria**:
- [ ] AC1: 두 파일 모두에서 `# Decisions and Assumptions` 헤더, `Rejected alternatives`, `**중요 결정만 기록**` 리터럴이 grep 0건이다.
- [ ] AC2: 두 파일 모두 Process 1이 "동일 change element가 둘 이상의 동기화 표면에 걸리는지 함께 식별한다."로 끝나고("~도" 제거) "중요 결정" 리터럴은 0건이다.
- [ ] AC3: 두 파일 모두 `# Propagation Surfaces` 템플릿과 `**조건부 propagation 표**` Hard Rule이 잔존한다(grep 각 1건 이상).
- [ ] AC4: 두 파일이 byte-identical이다 (`diff -q` 무출력 — 현재 상태와 동일한 parity 유지).

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md` -- D&A 템플릿 블록·Hard Rule 제거, Process 1 복귀
- [M] `.codex/skills/feature-draft/SKILL.md` -- 동일 (byte-identical 미러)

### Task 2: reviewer(plan-review-agent) 산문 복귀

두 agent 미러에서 AC3·Hard Rule 7·Step 2·Step 4를 99a6bd5^ 산문으로 복귀한다. Step 2의 propagation 추출 절과 Hard Rule 8, Step 3 계단의 propagation 검증, Verification Weakness 행의 propagation 문구는 유지한다. codex TOML은 3-way 적응 원칙을 따르되 이번 대상 줄은 .md와 동일 한국어 본문이므로 같은 텍스트 치환을 적용하고 TOML 프레이밍은 건드리지 않는다.

**Acceptance Criteria**:
- [ ] AC1: 두 파일 모두 AC3이 원문 "Decision and Assumption 점검(Step 4)을 수행했다."이고, `5필드` 리터럴이 grep 0건이다.
- [ ] AC2: 두 파일 모두 Hard Rule 7이 원문 산문("결과 방향을 바꿀 수 있는 모호성, Target Files 선택, task boundary 결정은 draft 안에서 가정·대안·확신도·사용자 확인 필요 여부가 드러나야 한다." 포함)이다.
- [ ] AC3: 두 파일 모두 Step 2가 `decision markers(가정·대안·확신도·사용자 확인 필요)`를 포함하고 `` `Propagation Surfaces` 5열·owner 연접`` 추출 절을 유지하며, backtick `` `Decisions and Assumptions` `` 리터럴은 0건이다(Step 4 헤딩 "Review Decisions and Assumptions"는 원문 그대로 잔존 허용).
- [ ] AC4: 두 파일 모두 Step 4 항목이 원문 4개 불릿("Target Files 선택 근거가 드러나는가"로 시작)이다.
- [ ] AC5: 두 파일 모두 Hard Rule 8 `Propagation Surface Coverage`가 잔존하고, `.codex/agents/plan-review-agent.toml`이 `python3 -c "import tomllib; tomllib.load(open(...,'rb'))"` 파싱을 통과한다.

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- AC3·Hard Rule 7·Step 2·Step 4 산문 복귀
- [M] `.codex/agents/plan-review-agent.toml` -- 동일 치환 (TOML 프레이밍 무변경)

### Task 3: SDD_SPEC_DEFINITION 한·영 canonical 구조 복귀

한·영 정의서의 canonical 구조 목록에서 D&A 항목을 제거해 재번호(Propagation Surfaces=3, Part 2=4, Open Questions=5)하고, 스켈레톤 예시에서 `# Decisions and Assumptions` 2줄을 제거한다.

**Acceptance Criteria**:
- [ ] AC1: ko 파일에서 `Decisions and Assumptions` grep 0건, canonical 구조가 ``3. `Propagation Surfaces``` · ``4. `Part 2: Tasks``` · ``5. `Open Questions``` 순으로 잔존한다.
- [ ] AC2: en 파일에서 `Decisions and Assumptions`·`five fields` grep 0건, `five-column`(Propagation 표) 리터럴은 잔존한다.
- [ ] AC3: 두 파일 모두 스켈레톤 예시에 `# Propagation Surfaces` 줄이 잔존한다.

**Target Files**:
- [M] `docs/SDD_SPEC_DEFINITION.md` -- 항목 3 제거·재번호, 스켈레톤 2줄 제거
- [M] `docs/en/SDD_SPEC_DEFINITION.md` -- 동일 (영문)

### Task 4: D&A 잔존 census 검증 (read-only)

제거 대상 변형 표기가 live 표면에 잔존하지 않음을 전수 grep으로 검증한다. 범위는 `.claude/ .codex/ docs/`(spec 표면 `_sdd/spec/`은 spec-sync 소관이라 제외, 과거 기록물 `_sdd/implementation|discussion|drafts|work_log` 제외).

**Acceptance Criteria**:
- [ ] AC1: `.claude/ .codex/ docs/` 전체에서 계약 고유 리터럴 census grep — `` `Decisions and Assumptions` ``(backtick 참조형), `Decision / Assumption`, `Rejected alternatives`, `User confirmation needed`, `5필드`, `five fields` — 합계 0건이다. 유일 허용 예외: plan-review-agent 2벌의 Step 4 헤딩 리터럴 `Review Decisions and Assumptions`(99a6bd5^ 원문). 일반 산문 표현 `중요 결정`은 6개 대상 파일(P1·P2·P3 표면) 한정으로 0건이다(현재 분포 실측이 이 6파일 + spec/기록물뿐이므로 전 범위 단언 대신 대상 한정).
- [ ] AC2: 유지 계약 앵커 census — `Propagation Surfaces` 리터럴이 6개 대상 파일(P1·P2·P3 표면) 전부에 잔존한다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
[없음 — 방향·범위는 사용자가 대화에서 확정(Propagation 유지, D&A 산문 복귀, 풀 체인 진행).]
