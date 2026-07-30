# Feature Draft: implementation-review 읽기 범위 계단

> 규모 판정: 적격 — 변경 요소 2개(Step 3에 범위 계단 신설, Error Handling 행 처리)가 한 파일과 그 codex 미러에만 걸리고 task와 1:1로 대응한다. 미러 짝 전파가 있으므로 마지막에 read-only 검증 task를 둔다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

리뷰 지연의 지배 요인은 리포트 작성이 아니라 **읽기 + 그에 따른 추론**이다(실측: correctness 리뷰 363s / 79k 토큰 중 최종 리포트는 2~3k). 직전 feature에서 `plan-review-agent`에 도구 계단을 넣었고(spec 4.6.15), 이번엔 `implementation-review-agent`에 같은 목적의 상한을 **다른 형태로** 넣는다.

**형태가 달라야 하는 이유**: `plan-review`는 draft 문서를 보므로 `Read`를 후순위로 밀어도 판별력이 유지된다. `implementation-review`는 correctness 렌즈이고 경계·null·에러 경로·동시성 같은 로직 결함 탐지가 본업이라, **코드 본문 Read가 그 렌즈의 핵심 수단**이다. 따라서 도구 순서를 제한하는 대신 **무엇을 읽을지의 범위**를 제한한다.

**새 contract/invariant**

- (신규 불변식) `implementation-review-agent`의 읽기 범위는 3단 계단을 따른다.
  - **① 변경 집합 + 기준 문서 — 전문 Read, 상한 없음**: `git diff --name-only` 실측 변경 파일(구현이 커밋된 뒤면 `<base>..HEAD` 또는 `git log`로 실측 — 워킹트리 diff가 비어도 ①이 공집합이 되지 않는다) ∪ (draft/plan이 있으면 그 Target Files) ∪ **기준 문서 자체**(어느 문서가 기준인지는 Step 1과 `기준 문서 적응`이 정한다 — ①은 그 판정을 재열거하지 않는다. 참조된 spec은 AC·정합 판정에 필요한 **절로 한정**하며 전문이 아니다). 로직 결함(경계·null·에러 경로·동시성) 능동 검토가 이 단에 결속된다. 단일 패스에 담기지 않으면 AC 관련도·diff hunk 밀도 순으로 읽고, 전문 Read하지 못한 파일과 그로 인해 근거가 약해진 AC verdict를 limitation으로 명시한다.
  - **② 인접 표면 — `Grep` 우선**: 변경 집합과 **의존 또는 짝 관계**인 파일(호출·import, claude↔codex 미러 짝, wrapper↔agent 포인터, spec surface). 통합 깨짐·계약 불일치 확인은 `Grep`으로 하고, 전문 Read는 finding 근거 인용이 필요할 때만 한다.
  - **③ 그 밖 — 탐색적 읽기 금지**: 위 두 범위 밖을 탐색적으로 읽지 않는다. 단 **AC가 명시적으로 요구하는 증거**(전수 census, 잔존 0건, 파일 목록 일치 등)는 범위 밖이라도 `Grep`/`Bash`로 확보한다 — ③이 막는 것은 AC가 요구하지 않는 탐색이다. 그래도 근거를 못 대면 해당 AC를 `UNTESTED(범위 밖)`로 표기하고 범위 가정을 Assumptions에 적는다.
- (신규 불변식) 이 계단은 correctness 검토 의무를 **낮추지 않는다** — agent AC1의 로직 결함 검토 의무와 Hard Rule 5(Fresh Verification) 문면은 불변이고, 신설 문면은 그 의무를 조건부·생략 가능으로 만들지 않는다.
- (신규 불변식) `UNTESTED`는 사유를 병기해 두 원인을 구분한다 — Hard Rule 5의 "테스트 실행 불가"와 ③의 "범위 밖". 반환 ledger 형식 자체는 바뀌지 않는다.
- (신규 불변식) 읽기 **범위** 규칙의 단일 소유자는 Step 3이다. 단 "담기지 않을 때 무엇을 포기하는가"(초과 대응)는 범위 규칙과 **다른 규칙**이므로, 기존 Error Handling의 대규모 코드베이스 대응은 삭제가 아니라 ①단계로 **이전**된다.
- (spec surface) `_sdd/spec/components.md`의 `implementation-review` 행에 두 가지를 반영한다 — (a) Notes에 이 계단 1문장, (b) Primary Source 셀에 누락된 `.codex/agents/implementation-review-agent.toml` 추가(`plan-review` 행은 codex 짝 2개를 갖는데 이 행은 claude 2개만 갖는다). `main.md` 본문 승격은 하지 않는다(agent 한 곳에만 적용돼 "2개 이상 표면 공통" 기준 미달).

## Scope

- **In**: `.claude/agents/implementation-review-agent.md`의 Step 3(Verification) 읽기 범위 계단 신설 + Error Handling 대규모 코드베이스 행 처리, 그리고 codex 미러 `.codex/agents/implementation-review-agent.toml`의 동일 변경.
- **Out**:
  - `pr-review-agent`에 상한 추가 — 사용자가 "PR 리뷰는 충분히 시간을 들이는 게 좋다"고 명시했다
  - `simplicity-review-agent`에 상한 추가 (요청 범위 밖)
  - **검증 예산(깊이) 제한** — 변이 테스트 횟수·반복 장토 같은 심화 검증의 상한은 이번 범위가 아니다. ⚠️ ①단계의 초과 대응 문장은 이 배제와 충돌하지 않는다 — 새 상한 신설이 아니라, Error Handling 행에서 삭제될 **기존 degradation 능력의 이전**이다
  - `plan-review-agent`의 기존 도구 계단 재작성 (직전 feature에서 완료)
  - model/effort 티어 변경
  - agent AC 절·Hard Rules·기준 문서 적응 절·Findings Classification·반환 형식(ledger 포함)·tools frontmatter 변경
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: implementation-review-agent Step 3에 읽기 범위 계단 신설 + Error Handling 행 처리

현재 Step 3은 "무엇을 확인하는지"만 서술하고 읽기 범위 규칙이 **없다** — 상한이 아니라 무제한이다. Part 1의 3단 계단을 세우고, 같은 성격의 규칙을 담고 있던 Error Handling 행을 정리한다.

**Contracts**: Part 1의 신규 불변식 4건이 이 task의 계약이다(여기 재서술하지 않는다). 핵심은 ①이 전문 Read를 **보장**하는 단계이지 제한하는 단계가 아니라는 점이다 — 계단은 ②③으로 범위가 번지는 것만 막는다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/agents/implementation-review-agent.md` Step 3에 3단 계단이 번호 목록으로 존재하고, 번호 항목에서 추출한 순서가 정확히 ①변경 집합+기준 문서 / ②인접 표면 / ③그 밖 3단이다. 각 단의 대상과 수단이 문면에 있다.
- [ ] AC2: ①의 대상 집합 3요소가 모두 문면에 있다 — `git diff --name-only` 실측, draft/plan의 Target Files, **기준 문서 자체**(draft/plan + 그것이 참조한 spec 범위). 기준 문서가 ①에 속함이 명시돼 spec 정합 렌즈가 ③으로 떨어지지 않는다.
- [ ] AC3: ①이 전문 Read를 허용/보장하는 문면이다 — "상한을 걸지 않는다" 취지가 명시되고, 로직 결함 능동 검토(경계·null·에러 경로·동시성) 지시가 ①에 결속돼 있다. `Read`를 후순위로 미는 표현이 Step 3에 없다.
- [ ] AC4: ①에 **초과 대응**이 명시됐다 — 단일 패스에 담기지 않을 때의 읽기 우선순위와, 전문 Read하지 못한 파일 + 근거가 약해진 AC verdict를 limitation으로 남기라는 지시가 문면에 있다.
- [ ] AC5: ②의 관계 술어가 코드 콜그래프에 국한되지 않는다 — `claude↔codex 미러 짝`과 `wrapper↔agent 포인터`가 인접 표면의 예로 문면에 등장한다(이 repo의 변경 집합은 대부분 마크다운 자산이라 "호출"만으로는 ②가 공집합이 된다).
- [ ] AC6: ③에 **AC 요구 증거 예외**가 명시됐다 — 전수 census·잔존 0건·파일 목록 일치처럼 AC가 명시적으로 요구하는 증거는 범위 밖이라도 `Grep`/`Bash`로 확보한다는 문장이 있고, ③이 막는 대상이 "탐색적 읽기"로 한정됨이 문면에서 읽힌다.
- [ ] AC7: ③의 미달 표기가 사유를 병기한다 — `UNTESTED(범위 밖)` 형태로 Hard Rule 5의 "테스트 실행 불가" UNTESTED와 구별되고, Step 6 반환 ledger의 표 형식(`| AC | Verification Method | Evidence | Verdict |`)은 바뀌지 않았다.
- [ ] AC8: Error Handling 표의 `대규모 코드베이스` 행이 Step 3을 가리키도록 정리됐고, **능력 손실이 없다** — 기존 행이 담고 있던 초과 대응이 AC4에 의해 ①로 이전됐으므로, 변경 후 "변경 집합이 단일 패스를 넘을 때 무엇을 포기하는가"에 답하는 문장이 파일 안에 존재한다.
- [ ] AC9: 두 Target File **각각**의 diff hunk가 (a) Step 3 계단 신설 (b) Error Handling 행 처리 **두 개뿐**이고, 그 밖의 라인은 바이트 불변이다 — agent AC 절·Hard Rules·기준 문서 적응·Findings Classification·반환 형식·tools frontmatter·Step 1·2·4·5·6이 이 한 판정으로 함께 닫힌다.
- [ ] AC10: 신설된 Step 3 문면이 correctness 능동 검토를 조건부·생략 가능으로 만드는 표현을 포함하지 않는다 — "여유가 있으면", "가능하면", "선택적으로" 류의 완화 수식이 로직 결함 검토 지시에 붙지 않았다.
- [ ] AC11: AC1~AC8의 변경이 `.codex/agents/implementation-review-agent.toml`에 동일 의미로 반영됐다.

**Target Files**:
- [M] `.claude/agents/implementation-review-agent.md` -- Step 3에 읽기 범위 계단 신설 + Error Handling 행 처리
- [M] `.codex/agents/implementation-review-agent.toml` -- codex 미러에 동일 변경 (3-way merge: codex 적응 delta 보존)

---

### Task 2: 미러 정합 + 잔존 검증 (read-only)

claude md ↔ codex toml 짝 전파는 이 repo가 반복해서 놓친 실패 모드다. 변경 payload 동일성과 codex delta 보존, 축약 대상 문구의 잔존 0을 증명한다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/`·`.codex/` 하위(`*.md`,`*.toml`)에서 `핵심 컴포넌트 중심으로 범위를 줄이고` 전수 grep 결과가 0건이다 (변경 전 기준선 2줄: `agents/implementation-review-agent.{md,toml}` 각 `:86`).
- [ ] AC2: 두 파일의 이번 변경 payload(`git diff -U0`의 +/- 라인)가 동일하다 — 미러 간 의미 분기 0건.
- [ ] AC3: `.codex/agents/implementation-review-agent.toml`이 `tomllib`로 파싱되고 키 구성(`name`·`description`·`developer_instructions`)이 보존됐으며, codex 적응 delta(`Codex Agent Boundary` 블록)가 잔존한다.
- [ ] AC4: `git diff --check` 통과 및 자산 변경 파일 목록이 Task 1의 Target Files 2개와 정확히 일치한다 — 계획 밖 자산 변경 0건 (`_sdd/` 프로세스 산출물은 하네스 강제 산출물이므로 이 판정에서 제외하고, 제외 사실을 결과에 명시한다).

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- **②③ 억제의 절감 규모는 미측정이다.** 동기가 된 실측(363s / 79k)의 ①/②/③별 읽기 비중 원자료가 없어, 이번 변경의 확정 효과는 절감 수치가 아니라 **"무제한 재량을 상한으로 대체"** 다. 현재도 리뷰어가 사실상 ①만 읽고 있다면 절감은 0에 가까울 수 있다. 실측 절감은 다음 `implementation-review` 1회의 tool call 구성으로 사후 확인한다 — 벤치마크를 이번 범위에 넣지 않기로 결정했다(문서 자산에 과한 비용). **사용자 확인 필요**: 절감이 0으로 확인되면 다음 레버는 검증 예산(깊이)뿐이며, 그건 판별력과의 맞교환이다.
