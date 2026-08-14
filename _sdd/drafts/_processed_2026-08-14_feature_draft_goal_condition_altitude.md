# Feature Draft: goal-init 조건 고도 분리 — outcome 조건 / 검증 레시피 / HOW 3분법

> 규모 판정: 적격 — 변경 요소 5종(D10 원칙·goal.md 템플릿·SKILL.md 지침·샘플 예시·Codex 미러)이 task 5개에 1:1 배정되어 coverage 눈검산 가능.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
goal-init이 만드는 `/goal` 조건 문자열에 브리틀한 검증 디테일(스키마 predicate·허용 델타 전수 열거·baseline 수치)이 인라인되어 사소한 현실 불일치에도 goal 재설정이 필요해지는 문제를 해소한다(근거: `_sdd/discussion/2026-08-14_discussion_goal_condition_altitude.md` 결정 5건, dancepdd lmax16 goal 실측).

- **분업 원칙 D10을 2분법 → 3분법으로 개정** (새 contract): ① 조건 문자열 = outcome 수준 `DONE WHEN` + 위조 어려운 최소 anchor 1-2개(산출물 절대경로·테스트 exit 0류) + 표준 레시피 참조 문구 ② 브리틀 검증 레시피 = `goal.md` 신설 "검증 레시피" 섹션 ③ HOW = Loop Protocol(불변).
- **표준 레시피 참조 문구** (새 contract): 조건 문자열의 DONE WHEN에 "`goal.md` 검증 레시피의 명령 실제 출력이 transcript에 surface되고 전 항목 PASS"를 포함한다.
- **drift 가드 표준 CONSTRAINT** (새 contract): 조건 문자열에 "검증 레시피 변경 시 변경 diff·사유를 transcript에 표시하며, 판정을 약화하는 변경은 사용자 승인 필요"를 포함한다.
- **인라인/하강 판별 기준 = 재설정 litmus** (지침, 비-gate): "이 디테일이 현실과 어긋나면 goal을 다시 세우는 게 마땅한가?" Yes → 인라인, No → 레시피. Step 3 self-check hard gate 3항목(도구 없이 판정·evidence surface·4,000자)은 불변.
- 4파일 계약·5단계 프로세스·비발동(I2)·setup 불변식·ralph 불간섭은 불변. `goal.md` 내부 섹션 구성만 바뀐다(검증 레시피 섹션 신설).
- spec surface: `components.md` goal-init 행 Notes, `main.md` Guardrails의 sdd-autopilot/goal-init 불릿(102-106행, "goal-init이 만든 자족적 조건 문자열" 문구) — "자족적 조건" 서술은 유지되나 D10 3분법을 반영해야 한다.

## Scope
- **In**: goal-init `harness-templates.md`(D10·goal.md 템플릿)·`SKILL.md`(Step 3/4 지침·Key Principles)·`examples/sample-goal-init-session.md`, Codex 미러 3파일, 잔존 census.
- **Out**: 네이티브 `/goal` 평가자 동작 변경(불가), self-check hard gate 구조 변경, `experiments.md`/`journal.md`/`report.md` 템플릿, ralph-loop-init, sdd-autopilot, docs/AUTOPILOT_GUIDE(고수준 서술이라 무영향 — census로 확인), 기존 생성된 goal들의 소급 수정, spec-sync 실행(후속 단계).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: harness-templates.md(Claude) D10 3분법 개정 + goal.md 템플릿에 검증 레시피 섹션 신설
조건 비대화의 구조적 원인인 "완료조건 자족 인라인" 압력을 템플릿 차원에서 해소한다.

**Contracts**:
- D10 분업 원칙(파일 서두)이 3분법으로 서술된다: 조건 문자열(outcome DONE WHEN + 최소 anchor 1-2개 + 표준 레시피 참조 문구 + drift CONSTRAINT) / 검증 레시피(`goal.md` 섹션, 메인 에이전트가 실행하고 출력을 surface) / Loop Protocol(HOW, 불변).
- goal.md 템플릿에 `## 검증 레시피` 섹션이 "`/goal` 조건 문자열" 섹션과 `## Loop Protocol` 사이에 신설되고, 슬롯은 "AC별 검증 명령·기대 출력·수치·허용 델타 열거 등 브리틀 디테일"이다.
- 조건 문자열 슬롯의 `DONE WHEN` 예시 행이 anchor + 표준 레시피 참조 문구 형태로 바뀌고, `CONSTRAINTS` 행은 기존 "없으면 이 줄 삭제" 옵션을 제거하고 drift 가드 표준 문구 + 선택적 추가 제약 슬롯 형태로 상시 유지된다.
- 검증 레시피 슬롯 설명은 1줄로 족하다 — 재설정 litmus 재서술은 넣지 않는다(litmus는 SKILL.md Step 3이 단독 소유, 토론 결정 5).

**Acceptance Criteria**:
- [ ] AC1: `.claude/skills/goal-init/references/harness-templates.md`의 D10 블록이 3분법(조건/검증 레시피/HOW)을 서술하고, "완료조건은 자족 인라인" 단독 서술이 남아 있지 않다. 평가: diff + grep 검토(2등급, 위 Contracts 인용 대조).
- [ ] AC2: goal.md 템플릿 코드블록에 `## 검증 레시피` 헤딩이 조건 문자열 섹션과 Loop Protocol 사이에 존재하고, 조건 문자열 슬롯에 (a) anchor 예시 (b) "검증 레시피 출력 surface + 전 항목 PASS" 표준 문구 (c) drift CONSTRAINT 표준 문구가 모두 존재한다. 평가: `grep -A2 "검증 레시피"` 및 코드블록 육안 대조(2등급).

**Target Files**:
- [M] `.claude/skills/goal-init/references/harness-templates.md` -- D10 개정 + 템플릿 섹션 신설

### Task 2: SKILL.md(Claude) Step 3 재설정 litmus 지침 + 3분법 정합
Condition Crafting이 새 분업을 따르도록 지침을 갱신하되, hard gate는 불변으로 유지한다(토론 결정 5).

**Contracts**:
- Key Principles의 "Condition vs HOW 분리"가 3분법 서술로 확장된다(검증 레시피 축 추가).
- **Step 3 분업형(C3) 서술(79행 "증명: 명령·기대 출력 인라인")을 3분법으로 개정한다** — outcome DONE WHEN + anchor + 레시피 참조 문구가 조건에 남고, 명령·기대 출력·수치 등 브리틀 디테일은 검증 레시피로 하강한다고 서술.
- Step 3에 재설정 litmus가 **판단 지침**으로 추가된다 — self-check hard gate는 기존 3항목 그대로(신규 gate 항목 추가 금지).
- Step 4(Harness Setup)의 `goal.md` 기입 지시에 검증 레시피 섹션 기입이 추가된다.
- Step 2 백로그 서술(70행 "검증 명령·판정조건")과 Error Handling 표(113행 "검증 명령이 명령+판정조건으로 확정되지 않음")의 확정 위치를 검증 레시피와 정합시킨다 — 검증 명령·판정조건은 여전히 확정되어야 하되, 그 귀속처가 조건 문자열이 아니라 검증 레시피임을 명시.

**Acceptance Criteria**:
- [ ] AC1: `.claude/skills/goal-init/SKILL.md` Step 3에 재설정 litmus("현실과 어긋나면 goal을 다시 세우는 게 마땅한가")가 지침으로 존재하고, self-check 항목 수는 여전히 3개(a/b/c)다. 평가: diff + self-check 블록 육안 검산(2등급).
- [ ] AC2: Key Principles와 Step 4에 검증 레시피 축이 반영되고, Hard Rules(I1 자족성·4,000자 포함) 6개는 문구 의미 변경 없이 유지된다(I1은 "outcome+anchor 조건이 자족"으로 성립). 평가: diff 검토(2등급).
- [ ] AC3: Step 3 C3 행·Step 2 백로그·Error Handling 표 어디에도 "조건 문자열에 명령·기대 출력을 인라인"하라는 지시가 남아 있지 않고, 검증 명령 확정 위치가 검증 레시피로 명시된다. 평가: `grep -n "인라인" SKILL.md` 전수 검토(2등급).

**Target Files**:
- [M] `.claude/skills/goal-init/SKILL.md` -- Step 3/4 지침·Key Principles 갱신

### Task 3: 샘플 세션 예시를 새 조건 형태로 갱신
예시가 낡은 2분법 조건(브리틀 인라인)을 시연하면 스킬 본문보다 예시를 따라가는 재발 경로가 된다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/skills/goal-init/examples/sample-goal-init-session.md`의 조건 문자열 예시가 outcome DONE WHEN + anchor + 표준 레시피 참조 문구 + drift CONSTRAINT 형태이고, 하네스 산출 예시에 검증 레시피 섹션이 등장한다. 평가: grep `DONE WHEN`·`검증 레시피` + 육안 대조(2등급).

**Target Files**:
- [M] `.claude/skills/goal-init/examples/sample-goal-init-session.md` -- 예시 정합

### Task 4: Codex 미러 3파일 전파 (전부 3-way)
미러 규약: 세 파일 모두 **3-way 적용** — 먼저 Codex 적응 delta를 카탈로그화(SKILL.md: 12행 "ask 기반"·AC5 "Codex `/goal` 실행법"·Step 4 실행법 슬롯 서술·Step 5 Codex 실행법 4요소·종료 Gate / harness-templates.md: 실행법 섹션·주석 / examples: 실측으로 확인)한 뒤 3분법 변경을 재적용한다. 단순 verbatim 복사는 Codex 런타임 delta를 파괴하므로 금지(codex-mirror-merge 규약).

**Acceptance Criteria**:
- [ ] AC1: `diff .claude/skills/goal-init/SKILL.md .codex/skills/goal-init/SKILL.md` 차이가 위 카탈로그의 기존 런타임 delta 범위로 한정되고, 3분법·litmus·검증 레시피 문구는 양쪽 동일하다. 평가: diff 출력 검토(2등급).
- [ ] AC2: `diff` 결과 `.codex` harness-templates.md의 Claude본 대비 차이가 기존 Codex 실행법 delta 범위(실행법 섹션·주석)로 한정된다 — 신설 검증 레시피 섹션·D10 3분법·표준 문구는 양쪽 동일. 평가: diff 출력 검토(2등급).

**Target Files**:
- [M] `.codex/skills/goal-init/SKILL.md` -- 3-way 적용 (delta 카탈로그 보존)
- [M] `.codex/skills/goal-init/references/harness-templates.md` -- 3-way 적용
- [M] `.codex/skills/goal-init/examples/sample-goal-init-session.md` -- delta 보존 재적용

### Task 5: 잔존 census (read-only 검증)
2분법 재진술·낡은 조건 예시가 다른 표면(sdd-autopilot·docs·spec)에 남으면 매 라운드 재발한다(rename census 실측 규칙).

**Acceptance Criteria**:
- [ ] AC1: `grep -rn "자족 인라인\|자족적\|기대 출력 인라인\|출력 인라인\|인라인" .claude/skills .codex/skills docs _sdd/spec` 결과를 전수 검토해(변형형 포함 — rename census 규칙), D10 2분법을 재진술하거나 브리틀 인라인을 지시하는 잔존이 0건임을 확인하고 검토 결과를 보고한다(고수준 "자족적 완료조건" 서술은 새 설계와 양립하므로 잔존 아님 — 판별 기준: 조건 문자열에 검증 디테일 인라인을 지시하는가). 평가: grep 출력 + 판별 결과 목록(2등급).

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- 검증 레시피 섹션 위치를 조건 문자열 섹션 "뒤"로 결정(조건이 참조하는 대상이 바로 아래 오도록). 사용자 확인 불요 — 템플릿 구조상 자명.
- docs/AUTOPILOT_GUIDE는 고수준 서술만 있어 Target에서 제외하고 Task 5 census로만 커버. 사용자 확인 불요.
