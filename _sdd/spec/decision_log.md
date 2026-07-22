# Decision Log

## 2026-07-22 - F4 완료: full 레인 삭제 완결 승격 + F5 개명 planned 등록 (v4.6.4 → v4.6.5, post-implementation sync)

### Context

분할 todo F4(자체 draft: `_sdd/drafts/2026-07-22_feature_draft_lite_residue_cleanup.md`)가 구현·리뷰 게이트(correctness H1+M3·simplicity M3 — 합집합 fix 완료)를 통과했다. 실측: `_sdd/tests/` 20 스크립트·test-free triage 확대 draft 부재, 이월 advisory sweep(fdl 쌍 description v1.2.0·impl-review description·AGENTS+템플릿 4미러 spec-sync 문장 5곳 동일·Quick Review 섹션 소거·spec-sync/spec-review agent 쌍 lite 기준 재서술) grep 확인, codex pr-review sample 2-reviewer spawn 흐름 재작성, census 2계층 — 엄격 계층 live 표면 full 고유 식별자 잔존 0(AGENTS.md:17 re-review 잔재 1건 적발·즉시 fix), 판정 계층 35파일 spot 판정 완료. 동시에 분할 계획 원본 Part 1 마커에 F5(개명)가 사용자 확정으로 추가됐다 — 미구현.

### Decision

1. **full 레인 실체 삭제 완결을 current truth로 승격**: F1~F4 전부 구현·sync 완료. 🚧 Planned F4 todo(umbrella 포함)를 소거하고 완결 서술로 대체한다. census 허용 예외는 `_sdd/` 기록물·AUTOPILOT_GUIDE tag 복구 안내·`docs/SDD_SPEC_DEFINITION.md`(F5 소관)다.
2. **F5 개명을 새 🚧 Planned todo로 등록 (사용자 확정)**: v4.6.1에서 "삭제 완료 후 별도 판단"으로 유보했던 `-lite` 접미사 개명이 이름+개념 전부 교체로 확정됐다 — 스킬 `feature-draft-lite`→`feature-draft`·`implementation-lite`→`implementation`, 개념 어휘("lite 체인"→"SDD 체인"·"lite draft"→"draft"·`> Lite 적격:` 마커), `docs/SDD_SPEC_DEFINITION.md` 정합, `_sdd/spec/` 잔여 full 서술·lite 개념 어휘 트림, draft 파일명 glob 양쪽 호환, 자체 census. 구현 evidence 없음 — PLANNED로만 반영.
3. **spec-sync·spec-review 입력/감사 계약의 lite 기준화 승격**: 입력 draft는 lite 구조(Part 1 마커 + task AC) 기준이고, full draft 구조(coverage index·`Covered By`·`Touchpoints` census)는 legacy 기록물 fallback/감사 시에만 적용된다.

### Changes

- `main.md` 4.6.5 — §2: 🚧 Planned F4 블록을 완결 서술로 승격·소거, 🚧 Planned F5 신설, "삭제 범위 밖"에서 개명 유보 문구 해소. §3: 오케스트레이션 행(F1~F4 완결 + F5 planned)·lite 규모 초과 대응 행(F1~F4 완료) 갱신
- `components.md` — `sdd-autopilot` 행의 "잔여 full 표면 정리 todo F4" 참조 소거, `spec-sync`·`spec-review` 행에 lite 기준 입력/감사 계약 반영
- `usage-guide.md` — 무효화 서술 없음(변경 없음)
- F4 draft `_processed_` 이동. 분할 계획 원본은 F5 입력으로 유지(F5 완료 시 처리)

### Context

분할 todo F3(자체 draft: `_sdd/drafts/2026-07-22_feature_draft_lite_reviewer_trim.md`)가 구현·리뷰 게이트(correctness C/H 0·M1, simplicity M6 — 합집합 fix 완료)를 통과했다. 실측: reviewer 4종 쌍 + plan-review 3.0.0·implementation-review 7.0.0·pr-review 4.0.0 SKILL 쌍 + autopilot 쌍·GUIDE ko/en 계 22파일 working tree 변경, full 기계장치 어휘 census(Tier·re-review·Iteration·리포트 저장·`_pr_correctness_` 등, 20파일 대상) 잔존 0, 4 agent tools에 `Write` 부재 확인.

### Decision

1. **새 invariant — reviewer read-only leaf**: reviewer agent 4종(`plan-review-agent`·`implementation-review-agent`·`simplicity-review-agent`·`pr-review-agent`)은 판정만 반환하며 tools에 `Write`가 없다(correctness 계열 2종만 테스트 실행용 `Bash` 유지). 리포트 파일 작성은 호출자 소관이다(작성자 불변식의 reviewer 적용).
2. **새 invariant — 단일 패스 유일**: 리뷰에 re-review·iteration 기계장치는 없고, finding 반영은 호출자 fix 1회다. v4.6.3에서 F3 판정으로 미뤄 둔 "공통 loop 정책의 reviewer-side 잔존"은 삭제로 판정 완료.
3. **plan-review full rubric 삭제**: Tier 체계·coverage index·V* 1:1·Touchpoints census·Orchestrator Review Mode 전부 삭제, 구 Tier 2-lite 내용(AC falsifiability·Target Files 실측·task boundary·6-smell·Lite 적격 검사·분할 권고)이 유일 rubric으로 승격. "Tier 2-lite" 명칭은 소멸(유일 mode라 이름 불요), 구 Tier 3 input-readiness report는 "대상 없음 + 안내 1줄"로 대체.
4. **pr-review 재설계 (사용자 확정)**: 두 reviewer는 경량 반환(finding별 위치·문제·수정 제안 — 통합 리포트의 유일 소스)으로 응답하고, pr-review 스킬(메인 루프)이 통합 리포트 `_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md` 1파일만 직접 작성한다(구 3파일 구조에서 축소, 통합 리포트가 finding 전문 게재).

### Changes

- `main.md` 4.6.4 — §2: review guardrail을 "fix 또는 명시적 잔여 이슈 보고"로 조정하고 단일 패스 invariant·reviewer read-only leaf invariant를 승격(orchestrator 단일 작성자 guardrail과 병합), pr-review 2-렌즈 서술에서 per-agent 리포트 경로(`_pr_correctness_`·`_simplicity_review_`) 소거, "Tier 2-lite" 명칭 2곳 치환, plan-review gate에 경량 반환 명시, 🚧 Planned F3 todo 소거(umbrella는 F4 잔여로 갱신). §3: 오케스트레이션·분할·plan quality gate 행 갱신
- `components.md` — `plan-review`·`implementation-review`·`pr-review` 행을 경량 반환 계약으로 재서술, autopilot·feature-draft-lite 행의 Tier 2-lite/F3 참조 정리
- `usage-guide.md` — Scenario 2의 plan_review 리포트 파일 산출 서술을 경량 반환으로 교체, Tier 2-lite 표기 2곳 치환
- F3 draft `_processed_` 이동. 분할 계획 원본은 F4 입력으로 유지

## 2026-07-22 - F2 완료: full 전용 agent·스킬 삭제를 current truth로 승격 (v4.6.2 → v4.6.3, post-implementation sync)

### Context

분할 todo F2(자체 draft: `_sdd/drafts/2026-07-22_feature_draft_lite_full_surfaces_removal.md`)가 구현·리뷰 게이트(correctness 전 AC MET, simplicity fix 반영)를 통과했다. 실측: agent 4종 쌍 8파일·스킬 3종 쌍 6디렉토리 부재, marketplace.json skills 21/agents 7(JSON 유효), implementation-lite v1.2.0 트리거 흡수, AGENTS.md + 하네스 템플릿 4미러 lite 체인, census 잔존은 F3 소관 reviewer 쌍 + `SDD_SPEC_DEFINITION.md`(F4)뿐.

### Decision

1. **full 전용 실행 유닛 부재를 current truth로 승격**: `feature-draft-agent`·`task-ordering-agent`·`test-author-agent`·`implementation-agent` 쌍과 `feature-draft`·`implementation`·`implementation-plan` 스킬 쌍은 존재하지 않는다. 등록 표면은 lite 체인 기준이다.
2. **트리거 흡수 (사용자 확정)**: 일반 구현 요청 트리거("implement the plan"·"start implementation"·"execute the plan"·"구현해줘" 계열)는 `implementation-lite`가 유일 수신 경로다. "병렬 구현" 계열 트리거는 폐기.
3. **출제자·응시자 분리의 대체 안전장치**: test-author leaf 분리 + orchestrator RED 게이트 대신, implementation-lite의 테스트 불변 규칙(RED 후 테스트 약화·수정 금지, 계약 오류는 선언 후 재-RED) + implementation-review Fresh Verification이 test-first 퇴화를 막는다.
4. reviewer 표면의 full 기계장치 서술(plan-review-agent full Tier 등)은 F3에서 판정하므로 이번 sync에서 보존한다.

### Changes

- `main.md` 4.6.3 — §1 entrypoint 예시 lite 치환. §2: F2 todo 소거(승격 서술로 대체, umbrella는 F3~F4로 갱신), producer 스킬 review-fix loop guardrail을 lite gate(단일 패스 + fix 1회) 기준으로 재서술, implementation 2-reviewer gate·test-author/RED 게이트·multi-phase ordering(`Checkpoints`)·feature-draft Part 2 배치 guardrail을 삭제/lite 기준 재서술(test-first canonical surface = `implementation-lite` SKILL), 직교 2-렌즈 적용 지점을 pr-review로 한정, model override 대상을 review 계열 3종으로 축소. §3: task ordering handoff·producer 품질 gate·multi-phase quality gate 행 제거, 실행 분리·오케스트레이션·planning precedence·test-first·2-렌즈·override 행 lite 기준 갱신
- `components.md` — `feature-draft`·`implementation-plan`·`implementation`·`test-author-agent` 행 제거, `implementation-lite` 행에 트리거 흡수 반영, Platform Notes skill/agent split 재서술, Code Map의 Implementation orchestrator/leaf 행 → Lite implementation contract, Feature planning map consumer 행 → feature-draft-lite 재지정
- `usage-guide.md` — Scenario 2를 수동 lite 체인으로 재작성
- F2 draft `_processed_` 이동. 분할 계획 원본은 F3·F4 입력으로 유지

## 2026-07-22 - full 레인 삭제 확정 및 4-feature 분할 todo 고정 (v4.6.0 → v4.6.1, pre-implementation planned sync)

### Context

v4.6.0에서 "full 레인 실체 삭제 — 다음 슬라이스"로 예고된 삭제가 롤링 분할 draft(`_sdd/drafts/2026-07-22_feature_draft_lite_full_lane_removal.md`)로 확정됐다. 구현 전 planned sync — 코드/삭제 evidence는 아직 없다.

### Decision

1. **full 레인(generated orchestrator 파이프라인)을 삭제하고 lite 체인을 유일 실행 경로로 만든다.** 근거: lite 품질이 full 대비 동등한데 훨씬 빠름 / full급 복잡도는 분할로 해소하는 것이 더 안전 / 분기 제거로 하네스 단순화·전파 표면 축소. 복구 보험은 삭제 직전 git tag `full-lane-final`.
2. **단일 planned 항목을 4-feature 순차 todo로 대체 고정한다**: F1 `sdd-autopilot` full 파트 제거 / F2 full 전용 agent 4종·스킬 3종 쌍 삭제 + 등록 표면 정리 / F3 reviewer full 기계장치 트림 / F4 잔재 정리 + 최종 census. 각 feature는 자기 차례에 lite draft를 새로 만들고, 구현·sync되면 해당 todo만 승격·소거한다.
3. **Out 고정**: lite 체인 자체의 기능 변경, 레인 무관 스킬(spec 파이프라인·pr-review·ralph·discussion 등), `-lite` 접미사 개명(삭제 완료 후 별도 판단)은 이 삭제 범위 밖이다.

### Changes

- `main.md` §2 Guardrails에 🚧 Planned F1~F4 분할 todo 블록 신설(기존 "다음 슬라이스" 단일 표기 대체), §3 오케스트레이션 행 marker 갱신, 헤더 4.6.1
- `components.md` `sdd-autopilot` Notes·`usage-guide.md` Scenario 2b의 planned marker를 main.md §2 todo 참조로 갱신
- 구현 없음 — 전 항목 PLANNED. draft 파일은 F1 구현 입력으로 유지되므로 `_processed_` 이동하지 않음(post-implementation sync 때 처리)

## 2026-07-22 - lite 레인 이탈 신호를 "full 승격"에서 "분할"로 교체 (v4.5.9 → v4.6.0)

### Context

lite 레인(feature-draft-lite → plan-review Tier 2-lite → implementation-lite)이 autopilot 기본 레인이 되면서, 규모 초과 시 "full 파이프라인 승격"을 안내하는 이탈 신호가 full 레인 의존을 재생산하는 문제가 드러났다. full 레인(generated orchestrator 파이프라인)은 다음 슬라이스에서 삭제 예정이다.

### Decision

1. **규모 초과의 해소 수단은 오케스트레이션이 아니라 분할이다**: lite 표면들은 full 전환을 안내하지 않는다. 단일 컨텍스트를 넘는 변경은 롤링 분할 draft(Part 1 마커에 분할 feature 목록, Part 2는 첫 feature task만) + `spec-sync` planned todo 고정(feature별 개별 `🚧 Planned`) + feature별 순차 lite 체인으로 해소한다. full 직행은 사용자 명시 요청만 한시 잔존한다(full 레인 삭제의 선행 조각).
2. **분할 판정의 canonical은 lite 표면 소유**: feature-draft-lite 분할 규칙 / implementation-lite 중단·분할 규칙(단일 세션 초과=잔여 분할 마감, 계약 오류 반복=draft 복귀) / plan-review Tier 2-lite Lite 적격 검사(분할 권고). autopilot은 신호를 소비만 한다.
3. **census형 sweep은 분할 신호에서 제외**: 변형 표기 산개형 변경은 마지막 read-only 검증 task(전수 grep census AC)로 흡수한다.

### Rationale

- 규모 초과를 더 큰 파이프라인으로 올리면 "단일 컨텍스트 = 품질 전제"라는 lite의 근거가 무력화되고 full 레인 삭제가 막힌다. 분할은 그 전제를 유지하는 유일한 해소 수단이다.
- 계약이 흔들리는 것은 구현 문제가 아니라 계획 문제이므로 해결 장소는 full 전환이 아니라 draft 복귀다(남는 안전장치: 테스트 불변 규칙 + implementation-review Fresh Verification).

### Changes

- 구현(선행 완료, correctness review Task 1~5 AC 전부 MET, 승격 어휘 grep census 잔존 0): `feature-draft-lite`·`implementation-lite` SKILL/skill.json(+codex identical), `plan-review-agent` 쌍(Tier 2-lite 분할 권고), `sdd-autopilot` 쌍 v2.7.0(Lane 판정 축소·Step L 분할 규칙), `spec-sync-agent` 쌍(분할 feature 목록 → feature별 개별 planned todo), `docs/AUTOPILOT_GUIDE.md`
- `_sdd/spec/main.md` §2 Guardrails lite 레인 bullet 신설 + §3 오케스트레이션 행 갱신·"lite 레인 규모 초과 대응" 행 신설 (v4.6.0)
- `_sdd/spec/components.md` — `sdd-autopilot` Notes 갱신, `feature-draft-lite`·`implementation-lite` 행 신설
- `_sdd/spec/usage-guide.md` — Scenario 2b에 기본 레인(lite) 노트 추가, orchestrator 흐름을 full 명시 요청 한정으로 표기
- 참고: 직전 엔트리(v4.5.9)의 main.md 헤더 반영이 누락돼 헤더가 4.5.8에 머물러 있었다. 본 엔트리에서 4.6.0으로 정정한다.

## 2026-07-14 - feature-draft Part 2를 "상세는 task, 문서 전역은 index"로 재배치 (v4.5.8 → v4.5.9)

### Context

feature-draft Part 2의 `Contract/Invariant Delta and Coverage`·`Touchpoints`·`Validation Plan`이 문서 전역 섹션이라, task를 읽다가 C#/V# ID를 표로 점프하는 간접참조와 관계의 양방향 이중 저장(표의 Covered By/Validated By ↔ task Technical Notes의 "Covers.../validated by...")이 작성 비용·읽기 동선을 해쳤다. exemplar 실측(2026-07-09 task_ordering draft)에서 V1~V7이 T1~T7과 1:1이었고, global 섹션이 있는데도 Description이 census를 재열거하는 등 global↔per-task 재진술이 반복됐다. 구조화 토론(`_sdd/discussion/2026-07-14_discussion_feature_draft_output_diet.md`, 6라운드 D1~D6)으로 재배치를 확정했다.

### Decision

1. **상세의 단일 홈 = task**: 각 task에 `Contracts` 필드(구현/보존하는 C/I 계약 실체 — test-author "계약 발명 금지"의 앵커)와 `Validation` 블록(AC 바로 아래 1:1 병치, 등급/판정조건/증거형태) 신설. 문서 전역 `Validation Plan` 표는 삭제.
2. **문서 전역 = thin index**: `Contract/Invariant Delta and Coverage`는 `ID|1줄 요약|Covered By`만 — 고아 delta(task를 못 받은 계약) 감사 자리이자 spec-sync delta 입력. delta↔task 관계는 index가 단방향 소유(task Technical Notes의 역방향 기록 삭제).
3. **Touchpoints 역할 축소**: 둘 이상 task가 참조하는 공유 census·전역 변형형 census 전용(line number 유일 허용처 유지). task-국소 탐색 근거는 Target Files `-- 사유` 주석으로.
4. **cross-cutting 이원화**: 분해형 invariant는 각 task Validation이 자기 슬라이스 커버(index가 coverers 나열). sweep형 검증(parity census류)은 마지막 검증 task(Type: Test, Target Files `없음 (read-only 검증)`)로 승격 — task-ordering이 마지막 배치, RED 게이트 structural-check 분기가 실행. 기존 기계 재사용으로 신규 소비 계약 불필요.

기각: 전면 병합(coverage 감사 소실 — 빠진 delta 반증 불가), 구조 유지+셀 다이어트(읽기 동선 미개선), 계약의 Description 흡수(단일 홈 규칙 충돌·test-author 앵커 약화), sweep V의 index 실체 유지(신규 소비 계약 필요).

### Rationale

- 병합 자체는 내용을 이동시킬 뿐 — 절감은 ID 배관(전역 V 정의·양방향 관계 기록)과 재진술(V셀의 AC 재진술·census 재열거) 삭제에서 나온다.
- coverage index를 남긴 유일한 이유는 감사 가능성: per-task로 흩어지면 task를 못 받은 delta는 어디에도 존재하지 않아 plan-review가 scope hole을 잡을 수 없다.
- AC 작성 위계(목표→AC→평가방법)·falsifiability·2등급 rubric·1:1 대응의 rubric 사슬은 불가침 — 거처만 이동(닻: SDD_SPEC_DEFINITION §6).
- 미검증 가정: "thin index만으로 orphan delta 감사가 현행과 동등하게 동작한다"는 구현 후 실측 대상.

### Changes

- `docs/SDD_SPEC_DEFINITION.md` §6 — 검증 정의 지점의 실행 단위 병치 + task 단위 배치 규칙 선언 (definition-first)
- `_sdd/spec/main.md` §2 Guardrails 단일 홈 배치 bullet 갱신 (v4.5.8 → v4.5.9)
- producer: `feature-draft-agent` claude·codex 짝 / consumers: `implementation` SKILL(dispatch 슬라이스), `spec-sync-agent`(Input Sources), `plan-review-agent`(Verification Weakness·DRY Risk), `task-ordering-agent`(sweep task 마지막 배치), `spec-review-agent`(temporary rubric), autopilot 표면(orchestrator-contract·sdd-reasoning-reference·sample-orchestrator) — 각 claude·codex 짝

## 2026-07-14 - RED 게이트를 2-way에서 non-falsifiable content의 test-free 예외를 포함한 3-way triage로 확장 (v4.5.7 → v4.5.8)

### Context

`implementation` 스킬(및 `sdd-autopilot`의 동형 RED 게이트)의 test-first 파이프라인은 모든 task를 무조건 2-stage(Stage A test-author → RED 게이트 → Stage B impl)로 태웠다. 테스트 프레임워크 부재 자산의 graceful degradation도 면제가 아니라 형태 변경(grep/구조 acceptance check)이라, 문서 산문·설명·주석 같은 non-falsifiable content 작업에도 "파일에 이 문구 있나" 수준의 동어반복(tautology) grep 체크를 RED artifact로 억지 생성하게 됐다 — 검증 가치는 낮고 파이프라인만 무거웠다. 이 repo는 문서/스킬 자산이 지배적이라 이 마찰이 반복 발생했다.

### Decision

1. **3-way triage 확장**: RED 게이트가 task AC 성격을 (a) test(관찰 가능한 코드 동작 → 실패 테스트), (b) structural-check(함수·심볼·config 키·계약 토큰 등 실질 구조·존재 → grep/구조 acceptance check, 기존 graceful degradation의 명명), (c) test-free(non-falsifiable content → Stage A 스킵·RED artifact 없음) 3분기로 판정한다.
2. **(c) 자격 제한 + 안전망**: (c)는 오직 falsifiable하게 검증할 관찰 대상이 실제로 없을 때만 허용한다("간단한 구현이라서"는 자격 아님 — 간단 opt-out은 `should work` 자기보고 차단이라는 RED 게이트 존재 이유를 침식). (c) 분류는 명시 근거(왜 non-falsifiable인지)를 RED 증거와 동일한 orchestrator 소유 progress 홈에 기록하고 Step 6 checkpoint 리뷰 dispatch 입력에 전달해야 한다(무근거 강등 금지). test만 면제되고 Step 5 회귀 스윕·Step 6 리뷰 게이트(correctness ∥ simplicity)는 불면제다.
3. **판정 주체 = 런타임 RED 게이트**: triage는 이미 falsifiability를 판정하는 RED 게이트의 자연 확장이다. feature-draft task별 Verification 필드 안(스키마 팽창+남발 위험)과 사용자 `--no-tdd` 플래그 안(원칙 부재 opt-out)은 기각했다. (a)/(b)의 기존 falsifiability 집행 성격은 불변(test-after 새는 경로 차단).

### Rationale

- non-falsifiable content에 강제되던 동어반복 acceptance check는 검증 가치 없이 파이프라인만 무겁게 만든다 — 이를 제거하되, 판정을 런타임 게이트에 두어 무원칙 opt-out과 test-after 재개방을 동시에 막는다.
- (c) 근거 기록·리뷰 게이트 불면제·"간단한 구현" 자격 부정을 falsifiable 문장으로 못박아 (c) 남용으로 RED 게이트가 침식되는 것을 방지한다.
- graceful-degradation 분기 기준의 canonical surface(`implementation` 스킬 RED 게이트 서술)를 단일 소스로 유지하고 나머지 표면은 참조만 두어 경계 기준 drift를 막는다.

### Changes

- `_sdd/spec/main.md` -- §2 Guardrails test-first 불변식 bullet + §3 결정 테이블 "implementation test-first" 행을 2-way→3-way triage로 갱신 (v4.5.7 → v4.5.8)
- 구현 코드(선행 완료, 본 결정의 evidence): 6개 미러 짝 claude·codex — `.claude/.codex/skills/implementation/SKILL.md`(canonical), `test-author-agent`, `implementation-agent`, `sdd-autopilot` orchestrator-contract·SKILL·examples/sample-orchestrator. draft `2026-07-13_feature_draft_red_gate_test_free_triage`, 구현 report READY(acceptance check 10개 GREEN)

## 2026-07-13 - task-ordering을 persistent implementation-plan에서 transient ordering overlay로 축소

### Context

`task-ordering-agent`는 `feature-draft`의 flat task-set을 dependency·phase·Checkpoint·병렬 wave가 포함된 ordered plan으로 변환하는 ordering step이다. 그러나 이 agent가 최초 커밋부터 177/178줄로 비대했다(work_log 2026-07-13 항목4 진단). 원인은 삭제된 `implementation-plan-agent`의 dependency·phase strategy·6-field phase metadata·Checkpoint·full-plan artifact 계약을 "기존 서술 이동" 명목으로 보존 이관하면서 ordering overlay가 full implementation-plan 재생성기로 바뀐 것 + AC/Hard Rules/Process 반복을 house style로 인정한 리뷰가 중복 제거를 막은 것이다. 또한 ordering 결과를 별도 `_sdd/implementation/*_implementation_plan_*.md`로 저장했으나, 이는 부모 orchestrator가 agent 완료 직후 즉시 소비하고 원본 task-set에서 재계산 가능한 control data라 persistent artifact가 불필요했다.

### Decision

1. **transient handoff로 축소**: agent 책임을 지정된 feature draft read → dependency·parallel wave·phase·checkpoint 판단 → 고정 Markdown 응답(`Status·Source·Mode·Execution·Dependencies·Checkpoints·Notes`) 반환으로 제한한다. 파일 write·task 정의 전사·full plan schema·phase 6-field metadata·validation/risk 복사·review loop를 제거한다. 입력 부재/판정 불가만 `BLOCKED`로 반환한다. tools `["Read","Write","Glob"]`→`["Read"]`.
2. **artifact 미생성**: `_sdd/implementation/*_implementation_plan_*.md`를 만들지 않는다. 부모가 `Source` feature draft의 task 본문과 응답을 결합해 실행하고, 영속 실행 이력은 기존 progress/report의 단일 작성자인 orchestrator가 소유한다. autopilot은 final Markdown을 `task_ordering.response`로 보존해 downstream `implementation-dispatch-controller`에 hand-off한다.
3. **Checkpoint 모델 단순화**: phase별 `Checkpoint: true/false` 필드를 폐기하고 transient response의 별도 `Checkpoints` 목록(중간 review boundary만, 마지막 phase implicit)으로 통일한다. legacy `implementation-plan` 입력은 phase `Checkpoint` 필드를 같은 의미로 해석하는 compatibility fallback으로만 남긴다.

### Consequences

- `task-ordering-agent`(md+toml)·소비자(`implementation` SKILL v3.6.0→3.7.0, `sdd-autopilot` SKILL·contract·reasoning·sample)·validator를 각 claude+codex 미러로 동기화, spec v4.5.6→4.5.7.
- validator가 transient 계약(`출력 파일=없음`, `Phase Source==task_ordering.response`, controller↔ordering step 짝)을 강제 — 양쪽 실행 PASS.
- late-binding 이득(전체 조망 기반 ordering)은 보존. task 정의 품질 검증은 `plan-review`(feature-draft Part 2 대상) 소관 그대로.

## 2026-07-13 - 하네스 §3 화살표에서 implementation-plan 제거 (planning precedence 반영)

### Context

2026-07-13 planning precedence 결정(main.md §Decisions)으로 `feature-draft`가 기본 planning entry가 되고 `implementation-plan`은 "phase/task 세분화가 필요할 때만 follow-up expansion"으로 격하됐다. 그러나 AGENTS.md 하네스 §3 화살표는 여전히 `feature-draft → (spec-sync) → (implementation-plan) → implementation`로 implementation-plan을 feature-draft 뒤 순차 optional 단계처럼 나열해, 모델이 "planning = implementation-plan 호출"로 오해하고 feature-draft를 건너뛸 여지가 있었다(사용자 관찰). 직전 커밋에서 §3에 추가한 "단계 = 동명 스킬 호출" 규칙 예시에도 implementation-plan이 포함돼 이 오해를 강화했다.

### Decision

1. **화살표에서 제거**: §3 단계 순서 화살표에서 `(implementation-plan)`을 뺀다 — `discussion → feature-draft / temporary spec → (spec-sync) → implementation → review-fix → verify → spec-sync`. 괄호 optional 단계 설명도 `(spec-sync)`만 남기고, 규칙 예시 나열에서도 implementation-plan을 제거한다.
2. **계층 분리 근거**: 하네스 §3은 얇은 기본 흐름만 소유하고 조건부 상세(implementation-plan을 언제 붙이는지)는 spec이 소유한다(§4가 "판단 기준은 spec 참조"로 명시). 따라서 화살표 제거는 spec의 "필요시 붙인다" 결정과 모순이 아니라 계층 분리다. `implementation-plan` 스킬 자체는 무변경 유지(version 5.0.0, spec 결정·autopilot Checkpoint gate에서 1급).

### Consequences

- 하네스 템플릿 4개 미러(claude·codex × spec-create·spec-upgrade references) byte-identical 갱신, 이 repo dogfooding `AGENTS.md` §3 동반 갱신.
- 소비 repo가 생성하는 AGENTS.md의 기본 워크플로우가 feature-draft를 planning entry로 제시 → implementation-plan을 default로 오인하지 않는다.
- spec planning precedence 결정·implementation-plan 스킬·정책은 무변경.

## 2026-07-13 - 하네스 §3에 "단계 이름 = 동명 SDD 스킬 호출" 규칙 추가

### Context

AGENTS.md 하네스 템플릿 §3(SDD 워크플로우)이 `discussion → feature-draft → … → implementation` 화살표 체인을 단계(phase) 이름으로만 제시하고, "각 단계의 구체 스킬은 설치된 SDD 스킬을 사용한다"는 추상 지시만 두었다. 단계 이름이 동명 스킬의 호출이라는 연결과 "직접 재구현 금지"가 명시되지 않아, 소비 repo에서 모델이 `feature-draft` 등을 스킬이 아니라 자기가 수행할 작업으로 읽고 자작하는 사례가 발생했다(사용자 관찰).

### Decision

1. **규칙 한 줄 추가**: §3에 "화살표의 각 단계 이름(discussion·feature-draft·implementation-plan·implementation·spec-sync 등)은 동명의 SDD 스킬이며, 해당 단계 진입 시 그 스킬을 **호출**하고 로직을 직접 재구현하지 않는다(스킬이 단일 소스). 스킬 미설치 환경에서만 SDD 개념으로 수동 수행"을 추가한다.
2. **카탈로그-비복사 원칙 유지**: 스킬 목록/설명을 나열하지 않고 "동명 스킬 호출" 행동 규칙만 얹는다 — 스킬 추가·rename 시 stale 되지 않고, "최신 스킬셋이 단일 소스" 설계와 정합. 매핑 테이블 대신 규칙 한 줄을 택한 이유다.

### Consequences

- 하네스 템플릿 4개 미러(claude·codex × spec-create·spec-upgrade references) byte-identical 갱신, 이 repo dogfooding `AGENTS.md` §3 동반 갱신.
- 소비 repo가 생성하는 모든 AGENTS.md가 단계별 스킬 호출을 명시적으로 지시 → 자작 재발 차단.
- 단계 순서·optional 규칙·정책은 무변경.

## 2026-07-10 - pr-review 통합 리포트를 통계 표에서 finding-본문 중심으로 재설계

### Context

`pr-review` 통합 리포트가 Metrics Summary(AC 충족 %·finding 개수 분포)·렌즈별 severity 카운트 표·Recommendations 표로 구성돼, 같은 finding이 세 곳(Key Findings 불릿·severity 표 셀·Recommendations 행)에 한 줄씩 중복 등장하면서 정작 "어디가, 왜, 어떻게 고쳐야 하는지"는 어디에도 온전히 실리지 않았다. 2026-07-08 결정 #3("통합 리포트 = 두 렌즈 요약 + detail 경로 참조, 재작성 금지")이 실행 가능한 내용이 통합 리포트에 실릴 수 없는 구조를 만든 원인이었다.

### Decision

1. **finding이 1급 단위**: 통합 리포트는 행동 대상 finding을 위치(`file:line`)·문제(증거)·수정(구체 방향) 블록 전문으로 싣는다. 상세도는 severity 계단을 따른다 — Pre-merge(correctness Critical/High + simplicity Medium+)와 correctness Medium은 블록 전문, Low는 위치 포함 한 문장.
2. **통계 제거**: Metrics Summary·렌즈별 severity 카운트 표·Recommendations 표·Next Steps 보일러플레이트를 삭제한다. 분포는 Verdict `Signals` 한 줄, 통과 신호는 §3 "확인된 것" 산문 2-3줄로 대체한다.
3. **2026-07-08 결정 #3 부분 대체**: "재작성 금지"를 "행동 대상 finding은 승격 복사, 검증 ledger·차원별 스캔·iteration history는 detail 경로 참조"로 완화한다. blocker는 통상 0~5개라 이중 작성 비용이 낮고 사용성 이득이 크다.
4. **승격 재료 공급**: `pr-review-agent`는 Step 5 반환에 Critical~Medium finding당 위치·문제·수정 블록을 포함하고, 리포트 §1도 같은 블록 형식(ID C#/H#/M#/L#)으로 바꾼다. simplicity 레인은 공유 agent를 수정하는 대신 dispatch message에 동일 상세 반환을 명시한다(리포트 §1이 이미 해당 필드를 요구). 반환이 부족하면 orchestrator가 detail 리포트 §1을 Read해 보충한다.
5. **정책 무변경**: verdict 합성 규칙(자동 강제 없음)·표적 disjoint·단일 작성자 불변식·simplicity 차원/falsifiable severity 정책은 그대로다.
6. **동일 원칙을 나머지 review detail 리포트에 확장**: `implementation-review-agent`는 §1 Findings를 같은 ID 블록(C#/H#/M# = 위치·문제·수정, Low = 한 문장)으로 교체하고 — finding이 review-fix loop에서 fix task로 변환되므로 승격 재료가 직접 필요 — §4 Recommendations를 finding ID 참조 갈음으로(plan-review §5 규칙 이식), §5 Conclusion을 삭제(Current Status와 중복), §2 Progress Overview를 task/AC 상태로 제약한다. `plan-review-agent`는 이미 finding 블록·재진술 금지 규칙을 갖춰 finding ID 부여(C#/H#/M#/L# — Current Status·§2/§5·Iteration History가 참조만 하고 정의가 없던 갭 해소)와 Low 한 문장 축약만 반영한다. reviewer들의 Current Status `Open findings` 표기도 ID 체계로 통일.
7. **simplicity §1 블록화 + implementation_report 재설계**: `simplicity-review-agent`도 High/Medium을 ID 블록(H#/M# = 차원·위치·현재 형태·제안 형태), Low를 한 문장으로 통일한다(차원·severity 정책 무변경). `implementation` SKILL의 최종 implementation_report는 Quality Assessment/Cross-Phase Review/Issues Found 표를 **Review Gates**(gate당 한 줄: iteration·exit/MAX·reviewer 리포트 경로)와 **Open Issues**(review-fix loop 후 잔존분만, reviewer finding ID 참조 + 위치 포함 한 문장)로 교체하고, Recommendations는 ID 참조 갈음, Conclusion은 verdict + 한 문장 근거로 유지한다 (`spec-sync`·`spec-summary`는 경로/글롭 소비라 호환).

### Consequences

- `pr-review` claude+codex SKILL v3.2.1→3.3.0, `implementation` claude+codex SKILL v3.5.0→3.6.0, reviewer agent 4종(pr-review·plan-review·implementation-review·simplicity-review) claude md + codex toml 8개 surface, codex/claude `examples/sample-review.md` 갱신. global spec guardrail sub-bullet의 finding 흐름 서술을 새 배치로 교체.
- 리포트 독자는 통합/detail 리포트만으로 수정 작업을 시작할 수 있고, Iteration History·Current Status가 참조하던 finding ID가 네 reviewer 모두에서 실제 정의된다.
- 출력 토큰도 감소한다(표 3개 + 중복 3중 게재 + Conclusion 사족 제거) — 출력 다이어트 방향과 정합.

## 2026-07-08 - pr-review correctness를 dispatched agent로 추출(model override가 두 렌즈에 균일 적용)

### Context

2026-06-17 결정으로 `pr-review`는 자체 correctness 검증(inline) ∥ `simplicity-review-agent` 병렬 dispatch의 PR 차원 직교 2-렌즈 review가 됐다. 그러나 correctness가 메인 스킬 inline이라 subagent model override(`--model`, Codex `--effort`)가 simplicity 레인에만 걸리고, 정작 무게가 실리는 correctness 검증은 세션 기본 모델로 고정되는 비대칭이 있었다. `implementation-review`(correctness=`implementation-review-agent` ∥ simplicity 둘 다 agent)와도 구조가 어긋났다.

### Decision

1. **`pr-review-agent` 신설**: PR correctness review 계약(code-only 검증 + spec 존재 시 spec-based 검증)을 보유하는 read-only leaf agent를 신설한다(claude `.claude/agents/pr-review-agent.md`, codex `.codex/agents/pr-review-agent.toml`). `simplicity-review-agent`의 형제로 표적 disjoint를 유지하고, verdict는 내지 않고 correctness 신호만 반환한다.
2. **`pr-review` orchestrator 전환**: 스킬은 PR 데이터·spec 수집 → 두 reviewer 병렬 dispatch → verdict 합성 → 통합 리포트만 소유한다. `implementation-review` 2-reviewer orchestrator와 동형이되, PR review는 통합 verdict 리포트가 존재 이유라 relay가 아닌 synthesis를 추가로 소유한다.
3. **대칭 리포트 형태**: correctness도 simplicity처럼 자기 리포트(`_sdd/pr/..._pr_correctness_<slug>.md`)를 직접 write하고, orchestrator 통합 리포트(`_sdd/pr/..._pr_review_<slug>.md`)는 두 렌즈 요약 + 두 detail 리포트 경로 참조 + verdict를 담는다. 단일 작성자 불변식 유지, correctness 내용 이중 작성(출력 낭비) 회피. 세 리포트는 공유 slug로 정렬한다.
4. **model override 균일화**: `--model`(Codex `--effort` 포함)이 correctness·simplicity 두 dispatch 모두에 적용된다 — inline이던 correctness 검증이 agent로 이동해 override가 무게 실리는 검증에 닿는다.
5. **정책 재사용(무변경)**: 표적 disjoint(correctness=정확성-중복 잔존, simplicity=형태-중복 위임), Medium=gating/Low=advisory falsifiable 분류, verdict 자동 강제 없음(correctness Critical/High→blocker, simplicity Medium+→rationale 기여), fix→re-review loop 미도입은 기존 계약 그대로다. `simplicity-review-agent`는 무변경.

### Consequences

- `pr-review-agent`는 claude marketplace.json agents 배열 + codex `.codex/agents/README.md`(Agent Set·Inline Writing) 양쪽에 등록됐다([[plugin-agent-registration-gap]] 회피).
- `pr-review` claude+codex SKILL 두 surface가 동형 orchestrator로 전환되고 v3.1.0→3.2.0 bump됐다.
- global spec은 이 변경을 guardrail sub-bullet + 결정 테이블 `직교 2-렌즈 review 렌즈` 행 + components.md `pr-review` 행에 반영했다("자체 correctness" → "correctness=`pr-review-agent` dispatch, model override 균일").
- 사용자 대면 산출물이 통합 verdict 리포트 1개 → verdict 리포트 + correctness detail + simplicity detail 3개 참조 구조로 바뀐다(simplicity가 이미 별도 리포트를 참조하던 것과 대칭).

## 2026-07-01 - drafts/work_log를 소비 repo 커밋 자산으로 승격(process artifact 6종→4종)

### Context

2026-06-20 정책은 `_sdd/drafts/`(feature draft)와 `_sdd/work_log/`를 process artifact로 묶어 `.gitignore`로 로컬 전용에 뒀다. 그러나 운영 중 feature draft가 사실상 소비 repo의 구현 로그(무엇을·왜 바꿨는지의 영속 기록) 역할을 하는 것이 관찰됐고, work_log도 같은 진행 기록 성격이라 로컬에만 두면 이력 가치가 소실된다.

### Decision

1. **커밋 경계 재조정**: 소비 repo에서 커밋되는 `_sdd`를 `spec/`·`guides/`·`env.md`에 더해 `drafts/`·`work_log/`까지로 넓힌다. 로컬 전용 process artifact는 4종(`_sdd/{discussion,implementation,pipeline,pr}/`)으로 좁힌다.
2. **`SDD-WORKSPACE` 마커 블록 갱신**: 두 부트스트랩 스킬(spec-create 3d / spec-upgrade Step 6)과 harness 템플릿 §2의 marker block에서 `_sdd/drafts/`·`_sdd/work_log/` 줄을 제거한다. 멱등 병합 메커니즘 자체는 불변이라, 재실행 시 마커 블록만 새 4종으로 교체된다.
3. **메타 repo 예외 유지**: 본 sdd_skills repo는 여전히 process artifact 전부를 history 가치로 커밋하는 예외다(소비 repo 정책과 별개).
4. **2026-06-20 결정 #1 대체**: 커밋 경계 재조정으로 2026-06-20 결정 #1을 본 entry가 대체한다(같은 entry의 #2 멱등 병합·#3 env.md 경고·#4 메타 repo 예외는 그대로 유효).

### Consequences

- 소비 repo의 feature draft/work log가 영속 이력으로 남아 구현 근거 추적이 가능해진다.
- env.md 비밀값 경고(2026-06-20 #3)와 멱등 병합 규칙(#2)은 그대로 유효하다.
- harness 템플릿 4개 미러가 byte-identical을 유지하도록 §2 한 줄을 동일 편집했다.

## 2026-06-23 - test-first를 orchestrator 소유 RED 게이트로 falsifiable 실행 불변식화(test-author/impl 분리 + group-pipeline)

### Context

`implementation` 경로는 문서상 100% test-first(RED→GREEN→REFACTOR)를 지시했지만, 유일한 hard-gate인 Verification Gate가 "코드 변경 후 테스트 재실행+통과 출력"에만 걸려 있어 test-after로도 완벽히 통과됐다. RED 단계의 실패 증거를 아무도 요구하지 않았고, leaf의 TDD표는 자기보고라 구현 완료 후 backfill 가능했다. 결과적으로 test-first가 falsifiable 산출물로 못박혀 있지 않아 모델이 저항 최소 경로(구현→테스트→통과→TDD표 backfill)로 새어나갔다.

### Decision

1. **test/impl 분리 + orchestrator 소유 RED 게이트**: 테스트 작성과 구현을 별도 leaf로 분리한다 — 신규 `test-author-agent`(테스트만)와 GREEN 전용으로 재정의된 `implementation-agent`(고정 실패 테스트를 최소코드로 통과, RED 자체 수행 안 함). 그 사이에 orchestrator가 소유하는 RED 게이트(새 테스트 실행→실패 확인→RED 증거 캡처 + falsifiability 점검)를 강제로 끼워 test-first를 검증 가능한 실행 불변식으로 만든다. RED 증거는 leaf 자기보고 TDD표가 아니라 orchestrator가 캡처한 외부 산출물이다(I1 집행 지점).
2. **상류 결정/하류 실행 분리**: 설계 결정(Contract/Invariant Delta·Validation Plan `V*`)은 plan에서 상류로 확정되고, test-author와 impl-agent는 같은 pinned 계약을 실행만 한다. plan 포맷은 무변경(test-author가 기존 산출물을 입력으로 소비하고 테스트 경로는 자체 추론).
3. **테스트는 impl에 대해 고정 + CONTRACT_MISMATCH**: impl-agent는 고정 실패 테스트를 수정하지 않고, 가정 계약이 틀렸다고 보면 `CONTRACT_MISMATCH: {test} - {문제} - {제안 계약}`으로 보고하며 orchestrator가 test-author 재dispatch를 판정한다(기존 `UNPLANNED_DEPENDENCY` 보고 구조 차용, 새 메커니즘 미도입). 약한 테스트 통과로 퇴화하는 것을 막는 안전장치. 입력에 고정 테스트/RED 증거가 없으면 자체 RED 작성을 금지하고 `BLOCKED`로 보고(orchestrated-only, test-after 재개방 방지).
4. **RED 게이트 falsifiability 관찰 규칙**: AC 관찰 동작에 대한 assertion/check 단계 실패만 유효한 RED로 인정하고, 순수 import/collection/syntax 단계 실패로만 빨간 테스트는 RED 미충족으로 test-author 재작성으로 돌린다. 구분 불가 언어/프레임워크는 그 사실을 RED 증거에 기록하고 리뷰 판정으로 강등.
5. **wave 내부 파이프라인, wave 간 순차**: 2-stage 파이프라인은 wave 내부에 한정하고 cross-wave 중첩은 도입하지 않는다(prose orchestration 스케줄러 복잡도 회피 — YAGNI 기각). graceful degradation의 canonical surface는 `implementation` SKILL RED 게이트 서술이며 다른 surface는 이를 참조한다(I4 drift 방지).
6. **agent 등록 + autopilot 1급 Step kind**: canonical agent set에 `test-author-agent`를 추가(`implementation-agent`는 GREEN 전용)하고, autopilot 구현 step을 1급 Step kind `implementation-dispatch-controller`로 선언한다(subagent_type 오버로드 아님). controller는 wave별 3단계(test-author 병렬 → RED 게이트 → impl 병렬)로 fan out한다. review-fix gate fix 정책은 correctness finding=test-first, simplicity/refactor finding=직접 fix.

### Consequences

- global spec main.md Guardrails에 test-first 실행 불변식·RED 게이트·테스트 고정·CONTRACT_MISMATCH·wave 파이프라인·graceful degradation이 thin하게 고정되고, 결정 테이블에 `implementation test-first` 행이 추가됐다. dispatch controller 서술이 1급 Step kind로 갱신됐다(v4.4.1→4.5.0).
- components.md에 `test-author-agent` 행 신설, `implementation` 행이 2-stage + RED/GREEN 게이트로, `sdd-autopilot` 행이 dispatch-controller Step kind로 갱신됐고 Strategic Code Map/Platform Notes가 정렬됐다.
- claude/codex 6쌍 미러 정합, autopilot 계약 정합, marketplace agents 9→10 등록 완료.

### References

- feature draft: `_sdd/drafts/2026-06-23_feature_draft_test_first_group_pipeline.md` (Part 1)
- implementation report: `_sdd/implementation/2026-06-23_implementation_report_test_first_group_pipeline.md` (READY — 10 task, V1~V9 MET, 2-reviewer gate 통과)
- commit: `aa9c328` "feat(skills): test-first group-pipeline orchestration", `6cdbb48` "refactor(implementation): deriveGroups 의사코드를 규칙 지시문으로 슬림화"
- validation: 코드 직접 확인 — `test-author-agent`(.md/.toml) 존재, `implementation-agent` GREEN 전용(RED 자체수행 0건), `implementation/SKILL.md` v3.4.0 RED 게이트, autopilot orchestrator-contract `implementation-dispatch-controller` Step kind, marketplace agents=10

## 2026-06-22 - `goal-init` 스킬 추가(`/goal` 조건 + 4파일 실행 하네스 생성기)

### Context

네이티브 `/goal` 루프(조건 충족까지 매 턴 자동 반복하는 평가자 기반 루프)를 잘 쓰려면 (1) 도구 없이 transcript만으로 판정 가능한 자족적 완료조건, (2) 가설 발산·실험·검증 메커니즘, (3) 검증 흔적을 대화에 surface, (4) 종료 후 회고가 필요한데 사용자가 수동으로 갖추기 어려웠다. 가장 가까운 선례 `ralph-loop-init`은 외부 bash `while-true` 루프 + 컨테이너 격리 + exit-code 머신 판정 모델이라 `/goal`의 네이티브 턴 루프와 실행 모델이 근본적으로 다르다.

### Decision

1. **신규 스킬 `goal-init` 추가**: discussion식 대화형 단일 스킬(신규 agent 없음)로 Claude(`.claude/skills/goal-init/`)·Codex(`.codex/skills/goal-init/`) 두 디렉토리에 작성하고 `marketplace.json` `plugins[0].skills` 배열에 Claude 경로를 등록한다(`agents` 배열 불변).
2. **산출물 경로 계약**: 실행 시 `_sdd/goal/<YYYY-MM-DD>_<slug>/`에 4파일(`goal.md`/`experiments.md`/`journal.md`/`report.md`)을 생성하고, 사용자가 검토 후 직접 걸 조건 문자열을 제시한다.
3. **불변식 고정**: (a) 평가자 자족성 — 조건 완료부(`DONE WHEN`/`CONSTRAINTS`/`STOP`)는 도구 없이 transcript만으로 판정 가능·4,000자 이하, 루프 행동(HOW)은 `goal.md`의 `Loop Protocol`로 분리, (b) 비발동 — 스킬은 `/goal`을 직접 발동하지 않는다, (c) 런타임 분리 — 조건 본문은 런타임 독립이고 실행법만 각 스킬이 자기 런타임 것을 기재(구조까지만 미러, 실행법 미러 강제 없음), (d) ralph 잔재 부재 — 하네스에 bash 루프/`run.sh`/state phase머신/컨테이너/별도 verification 파일이 없다(`/goal` 네이티브 턴 루프 스코프).
4. **ralph 정신만 차용**: append-only journal·conclusion-first report·적합성 hard gate 정신만 차용하고 bash 루프·`run.sh`·컨테이너 격리는 차용하지 않는다. `ralph-loop-init`은 건드리지 않는다.
5. **ralph-loop 대체 deferred**: `/goal` 기반 ralph 대체는 v1 스코프 밖 장기 과제로 보류한다(`/goal`은 턴 기반·평가자 도구 미사용이라 컨테이너 장시간 비대화형 머신검증을 메커니즘상 대체하기 어렵다).

### Consequences

- 사용자가 `/goal`에 걸 자족적 조건과 실행 하네스를 한 번의 대화로 셋업할 수 있어 무인 루프 토큰 낭비(영원히 미충족 판정) 위험이 줄어든다.
- 신규 agent가 없어 `agents` 배열·nesting 모델은 불변이고, 카탈로그 표면만 한 항목 늘어난다.
- ralph 실행 모델을 차용하지 않으므로 `ralph-loop-init`과 독립적으로 유지되며, 둘의 대체/브리지는 별도 결정으로 남는다.

## 2026-06-20 - 소비 repo 워크스페이스 commit 정책(process artifact gitignore + env.md 비밀값 경고)

### Context

부트스트랩 스킬(spec-create / spec-upgrade)이 만든 소비 repo의 `_sdd` 트리에는 spec/guides 같은 영속 자산과 discussion/drafts/implementation/pipeline/pr/work_log 같은 process artifact가 섞여 있었고, 무엇을 커밋하고 무엇을 로컬 전용으로 둘지에 대한 명시 정책이 없었다. 또한 `_sdd/env.md`는 커밋되는 파일임에도 비밀값 작성 위험에 대한 경고가 없었다.

### Decision

1. **워크스페이스 commit 경계 고정**: 소비 repo에서 커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`뿐이고, process artifact 6종(`_sdd/{discussion,drafts,implementation,pipeline,pr,work_log}/`)은 `.gitignore`로 로컬 전용이다. *(2026-07-01 결정으로 대체됨: `drafts/`·`work_log/`는 커밋 자산으로 승격, process artifact는 4종으로 축소.)*
2. **`.gitignore` 멱등 보강**: 두 부트스트랩 스킬이 소비 repo `.gitignore`에 `SDD-WORKSPACE` 마커 블록을 멱등 병합한다 — 부재→생성, 마커 없음→파일 끝 append(기존 규칙 보존), 마커 블록 존재→그 블록만 교체. 마커 밖 사용자 규칙은 건드리지 않는다.
3. **env.md 비밀값 금지**: `_sdd/env.md`는 커밋되므로 비밀값(API 키·토큰·비밀번호)을 적지 않는다(환경변수/secret manager로 관리). 하네스 템플릿 §2에 경고 1줄을 추가하고 spec-create는 env.md 생성 시 상단에 경고 헤더를 포함한다(spec-upgrade는 하네스 §2 병합으로 자동 반영).
4. **이 sdd_skills repo 예외**: 본 repo는 스킬 개발 메타 repo라 process artifact를 history 가치로 계속 커밋한다. 위 정책은 소비 repo 생성물 대상이며 본 repo에는 적용하지 않는다.

### Consequences

- 소비 repo는 노이즈/비밀 누출 위험이 줄고, 커밋되는 `_sdd` 표면이 영속 자산으로 좁혀진다.
- 마커 기반 멱등 병합이라 spec-create 부트스트랩과 spec-upgrade 마이그레이션이 동일 정책으로 수렴하며 재실행이 안전하다.
- 메타 repo 예외를 명시했으므로 본 repo에 process artifact가 커밋돼 있는 사실이 정책 위반으로 오인되지 않는다.

## 2026-06-20 - Harness(`AGENTS.md`)에 §5 작업 기록(work log) 레이어 추가

### Context

harness 템플릿은 §0~§4(작업 원칙 / 읽는 순서 / 작업 규약·검증 표준 / SDD 워크플로우 순서 / 판단 기준)로 고정돼 있었고, "언제 무엇을 했는지"의 사후 포렌식 추적 surface가 없었다. `_sdd/pipeline/log_*.md`는 sdd-autopilot 자동 실행 전용이라 수동 작업 이력은 어디에도 누적되지 않았다.

### Decision

1. **§5 작업 기록(work log) 슬롯 신설**: 의미 있는 작업 단위 종료 시 `_sdd/work_log/<yyyy-mm-dd>.md`에 항목을 append한다(그날 파일 없으면 생성). 항목 포맷은 `## <순번/HH:MM> <제목>` 아래 `무엇/왜` · `결과` · `포인터`(관련 커밋·문서·decision log 링크) · `요약`(따로 남은 게 없을 때만 인라인, 포인터로 충분하면 생략)이다.
2. **on-demand 포렌식 트랙으로 한정**: work log는 §1 읽기 순서에 포함하지 않는다(관리/조회 대상 아님, 필요할 때만 조회). `_sdd/pipeline/log_*.md`(autopilot 전용)와 별개 트랙으로, 수동 작업도 포함한다.
3. **인라인 단일화(별도 TEMPLATE 없음)**: 포맷을 §5 인라인으로 단일화하고 별도 `_sdd/work_log/TEMPLATE.md`는 만들지 않는다(복사 금지 원칙).

### Consequences

- harness 정본 템플릿 4곳 byte-identical 미러(`spec-create`/`spec-upgrade` × `.claude`/`.codex`)와 이 repo의 `AGENTS.md`에 §5가 인라인 추가됐다. SKILL.md 14곳의 하네스 범위 표현이 §0~§4 → §0~§5로 갱신됐다.
- global spec surface(components.md Strategic Code Map, usage-guide.md Scenario 1 expected result)가 §0~§5로 정렬됐다. main.md L103 harness layer 서술은 section 수를 열거하지 않는 thin 서술이라 무변경.
- 과거 §0~§4 entry(이 파일 §0~§4 고정 결정, changelog v4.1.16)는 당시 사실로 보존했다(역사 왜곡 금지).

## 2026-06-19 - spec-update-todo + spec-update-done 단일 `spec-sync` 진입점으로 통합

### Context

spec sync는 구현 전 planned delta 반영(`spec-update-todo`)과 구현 후 검증 사실 승격(`spec-update-done`)이 별도 스킬/agent로 분리돼 있었다. 두 스킬은 공유 substrate(Repo-wide Invariant Test, main/supporting/history surface 매핑, Strategic Code Map 보수 반영 규율, `🚧 Planned` 표식 규율, sub-spec 링크 규율, 내레이션 억제)를 거의 글자 단위로 중복 보유해, claude/codex × skill/agent 4벌 미러 동기화 부담과 "언제 어느 스킬을 부르나" 진입점 혼선을 유발했다.

### Decision

1. **단일 진입점으로 통합**: spec sync 책임을 단일 `spec-sync` 스킬 + `spec-sync-agent`가 보유한다. 구 `spec-update-todo`/`spec-update-done`의 skill·agent·codex mirror·skill.json 12파일은 hard-delete하고 deprecated alias는 남기지 않는다(내부 dogfooding repo).
2. **evidence-driven status 분류가 파이프라인 위치에 자동 적응**: 분류 축을 "코드 evidence 유무" 하나로 통일한다. 각 delta를 IMPLEMENTED/VERIFIED·PARTIAL·PLANNED/NOT_IMPLEMENTED·UNVERIFIED 4분류로 routing한다. 구현 전 호출은 evidence 부재로 전 항목이 PLANNED로 degrade(구 todo 동작)되고, 구현 후 호출은 코드 대조로 IMPLEMENTED를 승격하면서 잔여 PLANNED를 분리한다(구 done 동작). 두 동작이 한 sync에 혼합될 수 있다.
3. **안전 불변식 2개 보존**: evidence 없으면 승격 금지(기본값 PLANNED/보류), verified/planned 무표식 혼합 금지를 통합 agent Hard Rule로 유지한다. 미구현·미검증을 완료 사실로 기록하지 않는 안전성이 두 구 스킬에서 그대로 이전된다.
4. **호출 시점/횟수 보존**: 진입점만 통합하고, orchestrator는 동일 `spec-sync`를 호출 시점에 따라 최대 2회(구현 전 planned 반영 1회 조건부, 구현 완료 후 sync 1회) 호출한다. codex framed payload Mode는 단일 통합 모드로 둔다(evidence가 판정하므로 모드 힌트 잉여). (대안 기각: 구현 후 1회 통합은 대규모 변경의 사전 planned alignment 가치를 잃음; evidence 자동 감지로 호출 횟수까지 추론은 오판 위험.)

### Consequences

- global spec main.md §3 결정 테이블에 `spec sync 진입점` 행, "운영상 반드시 유지할 구조적 판단"에 evidence-driven 승격·무표식 혼합 금지 불변식이 thin하게 고정된다.
- 신규 4파일(`spec-sync-agent` .md/.toml, `spec-sync` wrapper×2 + skill.json), 삭제 12파일, 수정 46파일. autopilot 5쌍·AGENTS.md §3·harness template 4부·producer/reviewer agent 4쌍·docs en/ko·components.md/usage-guide.md dead-link가 단일 `spec-sync` 명칭으로 정렬됐다(V1~V7 + 외부 2-reviewer gate 통과, critical/high/medium 0).

## 2026-06-17 - Orthogonal 2-lens review extended to PR review (human-assist verdict integration)

### Context

직교 2-렌즈 병렬 review 패턴(correctness ∥ simplicity, 표적 disjoint, falsifiable-only gating)이 implementation review-gate에 정착한 뒤, 두 번째 진입점인 PR review(`pr-review`)에도 같은 검출 가치가 필요했다. 단, `pr-review`는 자동 수렴 gate가 아니라 인간 리뷰 보조라서 implementation gate의 합집합 자동 exit(`critical=high=medium=0`)를 그대로 옮기면 simplicity finding(동작-불변 형태)이 merge를 false-block할 위험이 있었다.

### Decision

1. **PR review에 simplicity 렌즈 추가**: `pr-review`가 자체 correctness 검증(PR/spec 정합·보안·테스트·verdict)을 유지하면서 `simplicity-review-agent`(read-only leaf, 동작-불변 형태)를 병렬 dispatch하는 PR 차원 직교 2-렌즈 review로 승격한다. simplicity 차원을 자체 복제하지 않고 단일 소스 agent를 재사용(DRY).
2. **verdict 통합 = rationale 기여(자동 강제 아님)**: simplicity finding은 verdict를 자동 강제하지 않는다. falsifiable gating finding(Medium+)은 REQUEST CHANGES rationale에 기여하고 주관(Low)은 Suggested Improvements로 흐른다. implementation gate의 합집합 자동 exit는 PR에 적용하지 않으며 최종 판단은 인간 리뷰어가 한다. (대안 기각: Medium+ 자동 REQUEST CHANGES는 인간 보조 성격과 충돌 + false-block 위험; verdict 완전 분리는 Medium+ 위반의 검출 가치 저하.)
3. **계약 재사용**: 표적 disjoint(correctness=정확성-중복 잔존, simplicity=형태-중복 위임), Medium=gating/Low=advisory falsifiable 분류, 단일 작성자 경로 분리(pr-review→`_sdd/pr/`, simplicity→`_sdd/implementation/`)는 기존 simplicity reviewer 계약을 그대로 소비한다(신규 계약 복제 없음). `simplicity-review-agent`는 무변경.
4. **범위 한정**: `spec-review` 비확장 제약은 유지한다. pr-review에 fix → re-review loop는 도입하지 않는다(verdict + 리포트로 닫는 인간 보조).

### Consequences

- `pr-review` claude+codex SKILL 두 surface에 dispatch 레인·표적 disjoint·verdict 정책·Output Format Simplicity 섹션이 동형 반영되고 v2.0.0→3.0.0 bump됐다(report READY, 2-reviewer gate 통과).
- global spec은 이 패턴이 두 진입점(implementation gate, PR review)에 적용됨을 guardrail sub-bullet + 결정 테이블 `직교 2-렌즈 review 렌즈` 행으로 thin하게 고정한다.

## 2026-06-17 - Orthogonal 2-lens parallel review for implementation gates

### Context

implementation review-gate는 단일 reviewer(`implementation-review-agent`)가 정확성과 코드 형태 품질을 함께 점검했다. 이는 (a) 한 reviewer에 이질적 표적(정확성 vs 동작-불변 형태)을 과부하시키고, (b) "단순화" 차원이 correctness finding에 묻혀 일관되게 검출되지 않는 문제가 있었다. 앤트로픽 pr-review-toolkit의 code-simplifier(코드를 직접 고치는 reviewer-editor)는 이 repo의 단일 작성자 불변식(reviewer는 자기 리포트만 쓰고 code/plan/spec을 수정하지 않는다)과 충돌해 그대로 차용할 수 없었다.

### Decision

1. **직교 2-렌즈 병렬 review**: implementation-scoped review-gate(`implementation` 스킬 phase/final gate, autopilot global/per-group/final-integration gate)는 표적이 disjoint한 두 read-only leaf reviewer를 병렬 dispatch한다 — correctness(`implementation-review-agent`: 정확성/AC/버그/보안/spec drift)와 simplicity(`simplicity-review-agent`: 동작-불변 형태 — 중복·죽은 코드·단일 사용처 추상화·도달 불가 에러 처리·과잉압축). `Speculative Code` 차원은 correctness에서 simplicity로 이관해 disjoint를 강제한다.
2. **gating exit는 두 report 합집합** `critical=high=medium=0`.
3. **falsifiable-only gating**: 동작 변화 없이 더 단순한 동등 형태를 구체적으로 제시할 수 있는 객관적 위반만 Medium 이상(gating), 주관적 취향은 Low(advisory). 병렬화는 벽시계만 줄이고 수렴은 보장하지 않으므로 이 한정이 수렴성의 닻이다.
4. **fix 경로 무변경**: 두 reviewer finding은 합산되어 기존 단일 fix 경로(`implementation-agent` 순차 재dispatch)로 처리된다. simplicity reviewer는 코드를 직접 고치지 않는다(단일 작성자 불변식).
5. **범위 한정**: simplicity 렌즈는 `spec-review`로 확장하지 않는다(코드 형태 품질이라 spec 문서 품질에 부적합). autopilot canonical agent set에 `simplicity-review-agent`를 추가하고, 결정적 게이트키퍼 `validate_orchestrator.py`가 2-reviewer 매핑을 강제(단일 reviewer 매핑을 FAIL)한다.

### Rationale

- 이질적 표적을 disjoint 렌즈로 분리하면 한 reviewer 과부하 없이 검출 범위가 넓어지고, 중복 finding이 방지된다.
- 두 reviewer가 read-only leaf라 동시 dispatch가 안전하고, 벽시계는 max(둘)≈1 reviewer로 유지된다(토큰 비용만 증가 — 사용자 명시 수용).
- code-simplifier의 "직접 수정" 대신 "리뷰만" 형제 agent로 번역해 단일 작성자 불변식과 nesting 1단계 제한을 보존한다.

### Status

구현 완료(`_sdd/implementation/2026-06-17_implementation_report_simplicity_reviewer.md`, READY — 10 task, 4 review-fix gate 통과, `validate_orchestrator.py` PASS/FAIL fixture 실행 검증). 입력: `_sdd/drafts/2026-06-17_feature_draft_simplicity_reviewer.md` Part 1.

## 2026-06-13 - AC-first validation rubric across the plan/review chain

### Context

plan이 task의 How를 상세 명세하지 않는 방향으로 가면 검증(AC + `Validation Plan`)이 통제의 유일한 닻이 된다. 기존 구조에서는 (a) `Validation Plan`의 평가방법이 `review, test` 수준으로 희석되고, (b) implementation-plan이 feature-draft의 `Validation Plan`을 `V*` ID 참조로만 들고 내려가 plan 단독으로 "무엇을 어떻게 검증하는가"를 알 수 없었으며, (c) AC를 metric-first로 좁히면 품질·가독성이 AC에 진입하지 못하는 문제가 있었다.

### Decision

1. **목표 → AC → 평가방법 → 증거 사슬을 SDD 규범으로 고정**: 검증 정의의 닻은 `docs/SDD_SPEC_DEFINITION.md` §6 `Validation Plan`이고, planning/implementation/review 스킬이 이를 구현한다.
2. **AC falsifiability**: 모든 AC는 충족/미충족이 증거로 닫혀야 한다 ("미충족"을 말할 증거가 없는 AC 금지).
3. **평가방법 2등급**: 기준은 "측정 가능"이 아니라 "증거 기반 판정 가능". 1등급(정량 측정형) / 2등급(정성 rubric 판정형) 모두 이진 판정·외부 증거 결착·제3자 반박 가능을 요구한다. 품질·가독성은 2등급으로 받는다.
4. **AC↔`V*` 완전 대응 + Validation Plan 전사**: 평가방법 없는 AC·AC 없는 `V*` 금지. implementation-plan은 feature-draft의 `Validation Plan`을 plan에 독립 섹션으로 전사한다 (dangling V 참조 제거, Self-Contained Authoring 귀결).
5. **증거 기반 결과 기록**: implementation-review는 각 AC/`V*`의 verdict를 증거에 묶어 Verification Summary ledger에 기록한다 (증거 없는 MET 금지).

### Rationale

- How를 위임하는 만큼 검증을 강화해야 통제 총량이 보존된다.
- AC가 metric의 부모(목표 분해)이고 metric은 AC의 자식(확인 수단)이다. AC-first여야 측정 어려운 품질도 목표로 진입하고, falsifiability + 평가방법 완전대응이 "측정 불가 소망 목록"을 막는다.
- 검증 정의를 plan에 전사하면 구현자가 plan 한 장만으로 "무엇을 어떻게 검증하는가"를 안다.

### Changes

- `docs/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_SPEC_DEFINITION.md` §6 -- `Validation Plan` rubric 규범(falsifiability, 2등급, 완전대응, 증거 기반 결과) 추가.
- `.codex`/`.claude` `feature-draft-agent` -- 평가방법 원천으로서 AC-first 위계·2등급·완전대응 정의.
- `.codex`/`.claude` `implementation-plan-agent` -- `Validation Plan` 전사(독립 섹션) + Step 4 AC-first 재배선.
- `.codex`/`.claude` `plan-review-agent` -- AC↔`V*`·falsifiability·등급·전사 위반을 Verification Weakness로 검출.
- `.codex`/`.claude` `implementation-review-agent` -- Verification Summary에 증거-판정 ledger 추가.

### References

- design 합의: 이 turn의 설계 토론 (목표→AC→평가방법→증거 위계, metric-first 과교정 교정)
- commit: `46a9e14` "feat(agents): enforce AC-first validation rubric across SDD plan/review chain" (agent 8개 파일)
- validation: 8개 agent 파일 codex/claude 미러 키워드 짝 일치, `git diff --check` clean (grep/diff/review evidence — 마크다운 자산 repo)

## 2026-06-12 - Introduce the work harness (AGENTS.md) as a separate layer

### Context

global spec 본문을 키우면 "fat 톱니(sawtooth)" 재팽창이 재발한다. 변화 속도·성격이 다른 두 종류의 정보가 한 문서에 섞이는 것이 원인이었다: "이해(what/why, 느림·수동 참조)"와 "작업 규약(how, 빠름·능동 적용)". global spec은 thin understanding anchor로 유지하면서 작업 규약을 어디에 둘지가 미정이었다.

### Decision

1. **작업 규약을 별도 Harness 레이어(`AGENTS.md`)로 분리**: harness는 global spec 위에 놓이는 작업 진입·작업 규약(how) 레이어로, 작업 원칙·읽는 순서·검증 표준·워크플로우 단계 순서·판단 기준 포인터만 담는다. §0~§4 표준 템플릿으로 형태를 고정한다.
2. **global spec 본문 thinness 불변(I1)**: harness 도입으로 global spec 본문은 한 줄도 두꺼워지지 않는다. harness와 global spec은 같은 정보를 중복 보유하지 않는다(단일 소스, I3).
3. **누수 차단(I2)**: harness에는 스킬 카탈로그·라우팅 표를 박지 않고(설치된 SDD 스킬을 가리킨다), repo-specific 행동 트리거도 적지 않는다(이는 global spec Guardrails가 단일 소스).
4. **멱등 병합**: 모든 harness 블록은 `<!-- SDD-HARNESS:START -->`...`<!-- SDD-HARNESS:END -->` 마커로 감싸, `spec-create`/`spec-upgrade` 재실행 시 마커 블록만 교체(마커 밖 기존 내용 보존)로 멱등하게 갱신한다.

### Rationale

- 키우는 것은 내용이 아니라 역할이다. 변화 속도가 다른 정보를 같은 문서에 두면 thin spec이 다시 fat해진다.
- harness는 repo에 배포되는 산출물이라 user-level `~/.claude/CLAUDE.md`가 없는 협업자에게도 작업 원칙이 전달된다.
- 마커 멱등 병합은 별도 실행 스크립트 없이 자연어 절차만으로 재실행 안전성을 확보해 미러·배포 부담을 늘리지 않는다.

### Changes

- `.claude`/`.codex` × `spec-create`/`spec-upgrade`의 `references/agents-harness-template.md` -- §0~§4 정본 템플릿 4곳 byte-identical 미러 신규.
- `.claude`/`.codex` `spec-create/SKILL.md` -- AGENTS.md bootstrap을 harness 템플릿 기반으로 격상, legacy `## SDD란` 삽입 제거, CLAUDE.md 포인터화, 마커 멱등 병합.
- `.claude`/`.codex` `spec-upgrade/SKILL.md` -- harness 부재/부분존재 시 마커 멱등 병합 step 추가, 소비 repo legacy 산출물 흡수.
- `docs/SDD_CONCEPT.md`, `docs/SDD_WORKFLOW.md` -- harness 레이어를 layer 표·workflow에 도입(canonical model).
- `_sdd/spec/main.md`, `_sdd/spec/usage-guide.md`, `_sdd/spec/components.md`, `_sdd/spec/logs/changelog.md` -- global spec surface sync(설계 모델 layer 서술 보정, AGENTS.md expected result, navigation hint, version metadata).

### References

- discussion: `_sdd/discussion/2026-06-12_discussion_agents_md_harness_layer.md` (결정 9건)
- feature draft: `_sdd/drafts/2026-06-12_feature_draft_agents_md_harness_layer.md`
- implementation report: `_sdd/implementation/2026-06-12_implementation_report_agents_md_harness_layer.md` (READY, Blocker 없음)
- spec review: `_sdd/spec/logs/spec_review_report.md` (SYNC_REQUIRED, C-1/Q-1/Q-2)
- commit: `e5ad765` "Introduce AGENTS.md work harness layer"
- validation: harness 템플릿 4곳 md5 `7e85521b08a0b758142c2cfdc9495d54` 동일, spec-create SKILL harness 참조 18건, docs 2종 layer 도입 확인 (grep/diff/review evidence — 마크다운 자산 repo)

## 2026-06-09 - Use kebab-case Codex custom agent names

### Context

Codex custom agent files already used kebab-case filenames such as `feature-draft-agent.toml`, but the TOML `name` fields and wrapper dispatch examples used underscore IDs such as `feature_draft_agent`. Codex resolves runtime custom agents by the TOML `name`, so the mismatch made skill instructions and actual file names look like different identities. A pilot confirmed kebab-case custom agent names are supported in a fresh Codex process, while the current session's agent registry does not hot-reload renamed agents.

### Decision

1. **Codex custom agent IDs use kebab-case**: managed `.codex/agents/*.toml` files now set `name` to the kebab-case file stem, including the `-agent` suffix.
2. **Wrapper dispatch uses the same ID**: Codex `spawn_agent(agent_type=...)` examples and contracts use the kebab-case custom agent IDs.
3. **Legacy underscore IDs are rejected, not normalized**: sdd-autopilot generated orchestrators must use canonical kebab-case IDs. Underscore custom agent IDs and suffix-less skill names remain unsupported legacy aliases.
4. **Historical artifacts are not rewritten**: old decision/changelog text remains historical. Current spec surfaces and new history entries record the canonical naming change.

### Rationale

- Matching file stem and TOML `name` removes the mental split between "agent file" and "agent_type" without adding alias logic.
- Kebab-case names are already the visible convention for skill and agent files.
- Rejecting legacy aliases keeps generated orchestrator validation simple and avoids a compatibility layer that would keep the old mismatch alive.

### Changes

- `.codex/agents/*.toml` -- `name` fields renamed to kebab-case custom agent IDs.
- `.codex/skills/*/SKILL.md` and sdd-autopilot references/examples -- dispatch and canonical contract references updated.
- `.codex/agents/README.md` -- naming rule and managed agent inventory updated.
- `.claude/skills/implementation/SKILL.md` -- Codex-side cross-reference updated where it mentions Codex agent IDs.
- `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/logs/changelog.md` -- current global spec sync.

### References

- feature draft: `_sdd/drafts/2026-06-09_feature_draft_codex_agent_kebab_names.md`
- plan review: `_sdd/implementation/2026-06-09_plan_review_codex_agent_kebab_names.md` (CLEAR)
- implementation progress: `_sdd/implementation/2026-06-09_implementation_progress_codex_agent_kebab_names.md`
- implementation report: `_sdd/implementation/2026-06-09_implementation_report_codex_agent_kebab_names.md`
- validation: static grep gates PASS, `git diff --check` PASS, fresh `codex exec` smoke for `feature-draft-agent` PASS

## 2026-06-03 - Harden sdd-autopilot generated orchestrator contract

### Context

`sdd-autopilot` generated orchestrator는 wrapper skill이 아니라 custom agent를 직접 호출한다. producer skill 직접 호출 경로가 review-fix loop를 소유하도록 강화된 뒤에도, autopilot-generated path에는 같은 planning producer gate가 명시적으로 필요했다. 동시에 `implementation_agent`가 단일 task leaf로 축소된 상태에서 generated orchestrator가 feature/phase 전체를 한 leaf에게 넘기면 nesting 제한과 leaf 계약을 위반할 수 있었다.

### Decision

1. **planning producer output gate**: `feature_draft_agent` / `implementation_plan_agent` output은 downstream 소비 전에 `plan_review_agent` gate를 통과해야 한다. 실패 시 finding을 implementation fix task로 normalize하지 않고 producer output을 reject/regenerate한다.
2. **implementation dispatch controller**: generated orchestrator의 `implementation_agent` / `sdd-skills:implementation-agent` step은 feature/phase 전체 leaf call이 아니라 autopilot이 task-level leaf calls로 fan out하는 dispatch controller다.
3. **canonical invocation names only**: Codex generated orchestrator는 `_agent` names, Claude generated orchestrator는 `sdd-skills:<agent>-agent` names만 사용한다. legacy alias는 normalize하지 않고 verification에서 reject/regenerate한다.
4. **review-fix severity boundary**: Critical/High/Medium은 review-fix blocker이고 Low는 advisory/logged follow-up이다.
5. **missing non-final `Checkpoint` rejection**: multi-phase plan에서 마지막 phase가 아닌 phase의 `Checkpoint` metadata가 없으면 plan schema violation으로 보고, single late gate fallback 대신 producer review/Step 5 verification에서 reject/regenerate한다.

### Rationale

- generated orchestrator가 wrapper skill을 우회하더라도 직접 호출 경로와 같은 planning quality gate를 유지해야 한다.
- fan-out 책임은 nesting 1단계 제한 때문에 parent autopilot orchestrator가 가져야 하며, implementation leaf는 단일 task TDD executor로 남아야 한다.
- canonical-only rule은 오래된 pipeline artifact 호환 레이어를 새 contract에 끌고 오지 않기 위한 단순화다.
- Low advisory 정책은 loop 종료 조건(`critical=high=medium=0`)과 fix 대상 범위를 일치시킨다.
- `Checkpoint`는 execution gate boundary metadata이므로, 누락을 fallback으로 처리하면 per-group review model이 조용히 약화된다.

### Changes

- `.claude/skills/sdd-autopilot/SKILL.md`, `.codex/skills/sdd-autopilot/SKILL.md` -- generation/verification/execution semantics 강화.
- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`, `.codex/skills/sdd-autopilot/references/orchestrator-contract.md` -- canonical agent names, producer gate, implementation dispatch controller, Low advisory, missing-Checkpoint rejection 반영.
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`, `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- planning graph에 `plan-review` producer gate와 현재 per-group execution policy 반영.
- `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`, `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- hardened contract 예시 반영.
- `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`, `_sdd/spec/logs/changelog.md` -- verified persistent truth 기준 global spec sync.

### References

- commit: `7c0f99e Harden sdd-autopilot orchestrator contract`
- feature draft: `_sdd/drafts/2026-06-03_feature_draft_sdd_autopilot_contract_hardening.md`
- implementation report: `_sdd/implementation/2026-06-03_implementation_report_sdd_autopilot_contract_hardening.md`
- implementation review: `_sdd/implementation/2026-06-03_implementation_review_sdd_autopilot_contract_hardening.md` (CLEAR)
- test results: `_sdd/implementation/test_results/test_results_sdd_autopilot_contract_hardening.md` (PASS after review-fix updates)

## 2026-06-03 - Embed review-fix loop in three producer skills; promote feature-draft/implementation-plan to loop-owning orchestrators

### Context

세 entrypoint 스킬(`implementation`, `feature-draft`, `implementation-plan`)을 autopilot 없이 직접 호출하는 경로에는 산출물 품질 gate가 일관되게 없었다. `implementation`만 Step 6에 인라인 경량 self-review(orchestrator가 직접 품질 판정 후 Critical만 leaf 재dispatch)를 가졌고 외부 reviewer를 쓰지 않았으며, `feature-draft`/`implementation-plan`은 thin entrypoint wrapper라 review gate가 전혀 없었다. autopilot 경로는 reviewer-fix gate를 갖지만, autopilot은 스킬이 아니라 `*-agent` leaf를 직접 dispatch하므로 직접 호출 경로는 그 gate를 공유하지 못했다.

### Decision

1. **`implementation` Step 6 = 외부 review-fix loop**: 인라인 경량 self-review를 제거하고 외부 `implementation-review-agent` review→fix→re-review loop로 교체한다. fix는 `implementation-agent` leaf를 finding 하나씩 순차 재dispatch(finding 영향 파일 = 그 leaf의 Target Files)한다. loop scope는 실행분(phase) 단위 1 gate로 단순화하고 autopilot의 global/per-group·Checkpoint 메타 개념은 도입하지 않는다(직접 호출 경로엔 Checkpoint 신호를 줄 상위 오케스트레이터가 없음). `implementation-agent`는 fix mode 별도 계약 없이 finding을 task로 받아 기존 TDD 계약으로 처리한다(I3 — leaf는 단일 task 실행자라 finding이 곧 task로 매핑). version 3.0.0→3.1.0.
2. **`feature-draft`/`implementation-plan` wrapper → orchestrator 승격**: 두 thin wrapper를 loop-owning orchestrator로 재작성한다. producer-agent 생성 dispatch 직후 `plan-review-agent` review→fix→re-review loop를 메인 루프(스킬)가 직접 소유한다. producer/reviewer agent는 sub-agent를 spawn하지 못하므로 loop orchestration은 반드시 메인 루프(스킬)가 소유해야 하고, 이것이 wrapper→orchestrator 승격을 강제한다. `feature-draft`는 Mode B 대화 맥락 digest를 생성·fix 라운드 모두에 유지하고, `implementation-plan`은 Mode A(파일/경로 입력)라 digest forwarding이 없다. version 3.0.0→4.0.0.
3. **producer-agent fix mode 입력 계약 추가**: `feature-draft-agent`/`implementation-plan-agent`에 fix mode를 추가한다. dispatch 입력에 (a) review 리포트 경로, (b) 기존 산출물 경로, (c) 대상 findings가 **모두** 있으면 fix mode, 하나라도 없으면 생성 mode로 분기한다(별도 플래그 토큰 없음 — 입력 존재가 결정적 신호). fix mode는 기존 산출물을 Read해 finding 부분만 surgical 수정하고 전체 재생성하지 않는다(I1 산출물 단일 작성자). Source Pointer는 "producer 단일 소스 + skill=loop orchestrator"로 재정의한다.
4. **공통 loop 정책 통일**: 세 loop 모두 exit `critical=high=medium=0`, MAX 기본 3회, 매 라운드 loop 범위 전체 재리뷰, MAX 도달 시 critical/high 잔존→중단·보고·medium만 잔존→로그 후 진행. 별도 공유 정책 파일을 만들지 않고 각 스킬이 인라인 보유한다(autopilot `orchestrator-contract.md` §6 차용·재진술).

### Rationale

- 직접 호출 경로도 reviewer gate를 통과해야 산출물 품질이 호출 경로에 무관하게 보장된다.
- nesting 1단계 제한 아래에서 producer/reviewer agent는 leaf라 loop를 spawn할 수 없으므로, loop 소유 주체는 메인 루프 스킬일 수밖에 없다 — 이 제약이 ②③ 승격을 강제한다. 검증된 선례는 `implementation`(orchestrator가 loop 소유 + fix를 leaf 재dispatch)이다.
- 산출물 단일 작성자(I1)를 유지하려면 fix도 producer 재dispatch여야 하며, orchestrator 스킬은 loop만 소유하고 산출물을 직접 rewrite하지 않는다.
- autopilot은 실행 경로가 비중첩(스킬이 아니라 `*-agent` leaf를 직접 dispatch)이므로 본 변경에서 건드리지 않는다(개념적 유사 ≠ 이중 실행).

### Changes

- `.claude/skills/implementation/SKILL.md`, `.codex/skills/implementation/SKILL.md` -- Step 6 인라인 self-review → 외부 `implementation-review-agent` review-fix loop. v3.0.0→3.1.0
- `.claude/skills/feature-draft/SKILL.md`, `.codex/skills/feature-draft/SKILL.md` -- wrapper → orchestrator(loop 소유), Role Pointer 재정의. v3.0.0→4.0.0
- `.claude/skills/implementation-plan/SKILL.md`, `.codex/skills/implementation-plan/SKILL.md` -- wrapper → orchestrator(loop 소유), Role Pointer 재정의. v3.0.0→4.0.0
- `.claude/agents/feature-draft-agent.md`, `.codex/agents/feature-draft-agent.toml` -- fix mode 입력 계약 추가, Source Pointer 보강. codex `spec-update-todo-input` 마커 보존
- `.claude/agents/implementation-plan-agent.md`, `.codex/agents/implementation-plan-agent.toml` -- fix mode 입력 계약 추가, Source Pointer 보강
- `_sdd/spec/main.md` -- 실행 분리 결정·guardrail에 orchestrator-owned review-fix loop 반영, producer 스킬 품질 gate 결정 행 추가, v4.1.12→4.1.13
- `_sdd/spec/components.md` -- feature-draft/implementation-plan을 orchestrator+loop로 재분류, implementation Step 6 외부 loop 반영, Platform Notes split 갱신
- `_sdd/spec/DECISION_LOG.md`, `_sdd/spec/logs/changelog.md` -- 본 entry 추가

### Scope Boundary

- **autopilot 미변경**: autopilot 오케스트레이터·`orchestrator-contract.md`는 건드리지 않았다(실행 경로 비중첩). `implementation-agent`(leaf TDD)·`plan-review-agent`·`implementation-review-agent` 본문 review/TDD 계약도 재사용만 했다.

### Deferred / Unverified

- **V6 reload smoke**: 플러그인 reload 후 `/implementation`·`/feature-draft`·`/implementation-plan` trigger resolve + dispatch 표기 유효성 + multi-phase phase별 gate 1회 종료 확인은 self-referential 제약상 미실행(DEFERRED). 정적 게이트(V1~V5/V7 grep/diff)는 전부 PASS.

### References

- feature draft: `_sdd/drafts/2026-06-03_feature_draft_skills_embed_review_fix_loop.md`
- implementation report: `_sdd/implementation/2026-06-03_implementation_report_skills_embed_review_fix_loop.md` (READY, 정적 게이트 기준)
- plan review: `_sdd/implementation/2026-06-03_plan_review_skills_embed_review_fix_loop.md` (CLEAR)
- branch: `refactor/skills-embed-review-fix-loop` (`52a4c7f`)

## 2026-06-03 - Reclassify investigate as orchestrator with reused generic Explore fan-out (investigate-agent removed)

### Context

직전 v4.1.11 라운드는 `investigate`를 비-fan-out 9종에 포함해 wrapper(Mode B) + single-source `investigate-agent` 구조로 전환했다. 이 분류는 census 오판("현재 agent 본문이 sub-agent를 안 깐다 → non-fan-out → wrapper")에서 나왔다. 그러나 investigate는 탐색·가설 검증 단계에서 read-only sub-agent fan-out이 실제로 유익한 스킬이고, 통합 규칙(`fan-out이 필요한 execution → orchestrator(skill) + leaf`)에 비추면 orchestrator여야 한다. wrapper화는 investigate의 병렬 잠재력을 죽였다.

### Decision

1. **investigate를 orchestrator(skill)로 재분류**: 전체 디버깅 계약(문제정의·근본원인 종합·Blast Radius·fix·Fresh Verification·Investigation Report)을 메인 루프 skill이 인라인 소유한다. 더 이상 wrapper도, single-source agent dispatch도 아니다.
2. **fan-out 단위 = 빌트인 범용 read-only explore 역할 재사용**: custom leaf agent를 신설하지 않고 런타임 빌트인 역할을 재사용한다 — claude `Explore`, codex `spawn_agent(agent_type="explorer")`+`wait_agent`. 탐색이 넓고·모호할 때만 병렬 fan-out하고, 단순 버그·fix·검증·종합은 orchestrator가 인라인 수행한다(fix는 write 필요라 read-only explore 불가).
3. **`investigate-agent` 제거**: `.claude/agents/investigate-agent.md`, `.codex/agents/investigate-agent.toml`을 삭제하고 `.claude-plugin/marketplace.json` `agents` 목록에서 제외한다. 참조자가 자기 파일 + wrapper + 매니페스트뿐이고 autopilot·타 스킬 dispatch가 0건이라 제거가 격리됐다. `marketplace.json`의 investigate **skill** 항목은 유지된다(orchestrator도 사용자 진입점 skill).
4. **v4.1.11 entry의 investigate 분류 3곳을 대체**: 비-fan-out 목록은 실질 8종, Mode B wrapper 목록은 `feature-draft`/`implementation-review` 2종, `Agent` 도구 제거 목록의 investigate는 agent 파일 자체 제거로 흡수된다.

### Rationale

- nesting 1단계 제한 아래에서 fan-out이 유익한 execution은 메인 루프 orchestrator로 둬야 leaf를 안전하게 병렬화할 수 있다. investigate가 그 케이스다.
- 빌트인 범용 explore 역할을 재사용하면 custom leaf 신설 없이(YAGNI) read-only 병렬을 얻고, fix/검증은 단일 스레드 인라인으로 read/write 경계를 지킨다.
- 디버깅 안전성 계약(근본원인 우선, Scope Lock, Blast Radius Gate, Fresh Verification, Investigation Report 6필드)은 소유 위치만 agent→skill로 이동했을 뿐 의미는 보존됐다.

### Changes

- `.claude/skills/investigate/SKILL.md`, `.codex/skills/investigate/SKILL.md` -- wrapper → orchestrator(v4.0.0)로 재작성. 조건부 explore fan-out + fix·검증·종합 인라인. dispatch pointer → Role Pointer
- `.claude/agents/investigate-agent.md`, `.codex/agents/investigate-agent.toml` -- 삭제
- `.claude-plugin/marketplace.json` -- `agents` 목록에서 investigate-agent 제외(skill 항목 유지)
- `_sdd/spec/components.md` -- investigate 행을 orchestrator(빌트인 explore 재사용, investigate-agent 제거)로 정정
- `_sdd/spec/DECISION_LOG.md` -- v4.1.11 entry의 investigate 분류 3곳에 정정 마커 + 본 entry 추가
- `_sdd/spec/main.md` -- v4.1.11 → v4.1.12 version bump

### References

- feature draft: `_sdd/drafts/2026-06-03_feature_draft_investigate_orchestrator.md`
- plan review: `_sdd/implementation/2026-06-03_plan_review_investigate_orchestrator.md` (CLEAR)
- implementation review: READY (branch `refactor/investigate-orchestrator`)

## 2026-06-03 - Split execution into orchestrator/leaf vs wrapper-backed shapes under the nesting limit (v4.1.10 -> v4.1.11 spec revision)

### Context

`skill entrypoint + reusable agent`라는 기존 실행 분리 결정은 dispatch된 agent가 sub-agent를 다시 spawn할 수 없다는 플랫폼 제약(nesting 1단계)을 만나면서 두 가지 결이 갈렸다. `implementation`은 skill과 agent가 동일 본문(병렬 TDD 전체)을 mirror해, agent가 dispatch되는 경로(autopilot 등)에서는 병렬 dispatch 지시가 실행 불가능한 죽은 코드가 됐다. 반대로 fan-out이 없는 9종(`feature-draft`, `implementation-plan`, `plan-review`, `implementation-review`, `ralph-loop-init`, `spec-review`, `spec-update-done`, `spec-update-todo`, `investigate`)은 skill과 agent가 full 본문을 4벌(claude/codex × skill/agent) 중복 유지해 "함께 수정" 동기화 부담이 컸다.

> **2026-06-03 정정**: 이 entry의 investigate 분류 3곳(위 비-fan-out 9종 목록, 아래 Decision 3의 Mode B wrapper 목록, Changes의 `Agent` 도구 제거 5종 목록)은 census 오분류였다. investigate는 탐색 단계에서 read-only fan-out이 유익한 orchestrator로 재분류됐고 custom investigate-agent는 제거됐다. 아래 "2026-06-03 - Reclassify investigate as orchestrator with reused generic Explore fan-out" entry가 이 3곳을 대체한다(비-fan-out은 실질 8종, Mode B wrapper는 `feature-draft`/`implementation-review` 2종).

### Decision

1. **fan-out execution = orchestrator(skill) + leaf(agent)**: 메인 루프 skill(또는 autopilot)만 fan-out하고, leaf agent는 단일 단위만 실행하며 sub-agent를 spawn하지 않는다. `implementation`이 이 형태로 전환됐다 — skill이 task-set 확보(plan 파싱 / no-plan 경량 분해), dependency 기반 그룹 파생("dependency edge 없음 + Target Files disjoint → 병렬") + file-disjoint 가드레일, leaf fan-out, 통합/회귀/phase review/report를 소유하고, `implementation-agent` leaf는 단일 task TDD만 수행한다.
2. **non-fan-out execution = wrapper(skill) + single-source agent**: 9종 skill을 thin entrypoint wrapper로 전환하고 전체 계약·프로세스는 agent를 단일 소스로 보유한다. wrapper는 entrypoint(trigger)·artifact 경로 계약을 유지하고 결과를 relay한다.
3. **wrapper 2-모드**: 입력이 파일+직접 요청인 wrapper는 pass-through(Mode A)로, 입력이 대화에서 태어나는 wrapper(`feature-draft`, `investigate`, `implementation-review`)는 대화 맥락을 digest로 forwarding(Mode B)한다. 원리는 "agent는 파일은 read하지만 대화는 읽지 못한다".
4. **planner가 그룹화 두뇌를 소유**: `feature-draft`/`implementation-plan`이 의미적 충돌(모델 import, 동시 마이그레이션, 동일 config, API 생산-소비, 상수 충돌)을 명시적 dependency로 인코딩(무방향 mutex는 임의 방향으로 흡수)하고, orchestrator는 그 dependency로 trivial하게 그룹을 파생한다.
5. **autopilot dispatch granularity 고정**: 초기 구현 = group 단위 병렬 leaf fan-out, fix = review finding 단위 순차 leaf 재dispatch. progress/report 소유는 실행 주체(skill 또는 autopilot)이며 canonical 경로·소비 필드를 보존한다(downstream `spec-update-done`·`spec-summary` 호환). orchestrator-contract §2 "Implementation Dispatch Granularity"에 명시.
6. **mirror sync 의무 해소**: wrapper-backed skill에서 agent가 단일 소스이므로 "skill 본문과 agent 본문을 함께 미러링"하는 의무는 대부분 사라졌다. 유지보수는 agent 본문과 thin wrapper의 entrypoint/dispatch 정합 + claude/codex parity로 좁혀졌다.

### Rationale

- nesting 1단계 제한 아래에서 fan-out을 안전하게 두려면 fan-out 책임을 메인 루프(orchestrator)로 올리고 leaf는 더 쪼갤 것 없는 단위로 두어야 한다.
- TDD 로직을 leaf 단일 소스로 두면 DRY가 강화되고, 직접 `/implementation` 호출도 병렬성을 얻는다(병렬은 최적화 토글, 불가하면 동일 흐름으로 순차).
- 그룹화 판단을 planner의 dependency 인코딩에 두면 orchestrator는 dumb한 trivial 규칙만 적용하면 되고, 구식 plan은 file-disjoint 가드레일 + "확신 없으면 순차"로 안전하게 덜 병렬화될 뿐 오작동하지 않는다.
- non-fan-out skill을 wrapper+single-source agent로 두면 full 본문 중복이 4벌에서 2벌로 줄고(실측 약 -4,700줄), "조용한 흉내 금지"(지원 못 하는 fan-out을 wrapper가 흉내내지 않음) 원칙과도 맞는다.
- 이 결정은 main.md L59(skill=entrypoint, agent=reusable unit)·L62(wrapper-backed)·L90이 이미 선언한 모델의 구체적 실현이며, 새 모델 도입이 아니라 검증된 사실 반영이다.

### Changes

- `.claude/agents/implementation-agent.md`, `.codex/agents/implementation-agent.toml` -- 단일 task TDD leaf로 축소, `Agent` 도구 제거, 그룹화/phase review/report 섹션 삭제
- `.claude/skills/implementation/SKILL.md`, `.codex/skills/implementation/SKILL.md` -- orchestrator(v3)로 재작성(task-set 확보·그룹 파생·leaf fan-out·통합/report 소유)
- `.claude/skills/sdd-autopilot/SKILL.md` 및 `references/orchestrator-contract.md`, `examples/sample-orchestrator.md` (claude/codex) -- §2 Implementation Dispatch Granularity 신설(초기=병렬 그룹/fix=finding 순차/report 소유)
- `feature-draft`, `implementation-plan`의 skill+agent (claude/codex 8파일) -- 의미적 충돌 → 명시적 dependency 인코딩(B1 포함) 정식화
- 9종 mirror skill의 SKILL(claude/codex 18파일) -- thin wrapper로 전환, dispatch 참조(claude `sdd-skills:<name>-agent` / codex `spawn_agent(<name>_agent)`+`wait_agent`)
- 미사용 `Agent` 도구 제거 5종(`feature-draft`, `plan-review`, `spec-review`, `investigate`, `implementation-plan`), Mirror/Sync Notice → Source/Role Pointer
- `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`, `_sdd/spec/logs/changelog.md` -- 검증된 구현 evidence 기준 global spec surface 동기화

### References

- feature drafts: `_sdd/drafts/2026-06-03_feature_draft_implementation_orchestrator_leaf_split.md`, `_sdd/drafts/2026-06-03_feature_draft_skills_as_agent_wrappers.md`
- implementation reports: `_sdd/implementation/2026-06-03_implementation_report_implementation_orchestrator_leaf_split.md`, `_sdd/implementation/2026-06-03_implementation_report_skills_as_agent_wrappers.md`
- implementation reviews: `_sdd/implementation/2026-06-03_implementation_review_implementation_orchestrator_leaf_split.md` (READY), `_sdd/implementation/2026-06-03_implementation_review_skills_as_agent_wrappers.md` (READY)

## 2026-05-22 - Standardize Strategic Code Map as optional navigation surface (v4.1.9 -> v4.1.10 spec revision)

### Context

`spec-create`는 thin global spec을 기본으로 유지하도록 정렬돼 있었지만, 사람이 코드를 파악하는 navigator 역할과 LLM agent가 구현 중 참고하는 index 역할을 동시에 만족시키기에는 코드 탐색 좌표가 약했다. 기존 `_sdd/spec/components.md`에는 strategic code map appendix가 있었지만, `spec-create`, `feature-draft`, `spec-review`, `spec-update-*` 계열이 이를 어떤 surface로 생성·소비·검증해야 하는지 명시적 계약은 부족했다.

이번 라운드에서는 `Strategic Code Map`을 전체 파일 inventory가 아니라 optional compact navigation surface로 표준화하고, 작은 repo에서는 `main.md` appendix, 큰 repo에서는 `components.md` 또는 `code-map.md` 같은 supporting surface로 배치하는 규칙을 canonical docs, Codex/Claude skills, wrapper-backed agents에 반영했다.

### Decision

1. **`Strategic Code Map`을 optional navigation surface로 고정**: entrypoint, contract source, invariant hotspot, extension point, change hotspot, validation surface, supporting reference만 담는다. 전체 파일 트리, component catalog, API reference, 구현 narrative는 금지한다.
2. **primary navigation axis 하나를 선택**: app/service/product는 feature/domain/change-path, library/framework/compiler는 module/layer, workflow/tooling repo는 entrypoint/workflow, small repo는 `main.md` appendix를 기본 후보로 본다. secondary axis는 cross-reference로만 둔다.
3. **single-file default와 배치 기준 유지**: 기본값은 `_sdd/spec/main.md` 단일 파일이다. 5-10개 row 수준의 짧은 map은 appendix로 허용하고, row가 많거나 per-path 설명이 필요하면 supporting surface로 분리한다.
4. **planning에서는 hint로만 사용**: `feature-draft`와 implementation planning은 code map을 context gathering 출발점으로만 사용하고, 실제 `Touchpoints`와 `Target Files`는 현재 코드 탐색으로 재확인한다.
5. **sync에서는 persistent navigation 변화만 승격**: `spec-update-todo`와 `spec-update-done`은 temporary `Touchpoints`를 통째로 복사하지 않는다. 구현으로 검증된 장기 entrypoint, extension point, invariant hotspot, validation surface만 code map 후보로 본다.
6. **Codex/Claude skill과 agent mirror parity 유지**: 변경된 spec lifecycle skill은 `.claude/skills` counterpart와 wrapper-backed `.codex/agents` / `.claude/agents` mirror에 같은 normative rule을 담아야 한다.

### Rationale

- thin global spec을 유지하면서도 agentic coding에는 코드 탐색의 시작 좌표가 필요하다.
- 전수형 file inventory는 빠르게 stale해지고 global spec을 다시 두껍게 만든다.
- 작은 repo에서는 별도 파일이 오히려 탐색 비용을 늘리므로 compact appendix가 적합하다.
- 큰 repo나 설명이 필요한 map은 supporting surface에 둘 때 main body의 decision density가 유지된다.
- `Strategic Code Map`이 stale할 수 있으므로 planning/implementation은 항상 현재 코드 탐색으로 target files를 확정해야 한다.

### Changes

- `docs/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_SPEC_DEFINITION.md` -- `Strategic Code Map` 정의, 허용 정보, 배치 기준 추가
- `.claude/skills/spec-create/SKILL.md`, `.codex/skills/spec-create/SKILL.md` 및 template/example -- primary navigation axis와 appendix/supporting surface 생성 규칙 추가
- `spec-review`, `spec-rewrite`, `spec-upgrade`, `spec-summary`, `spec-update-todo`, `spec-update-done`, `feature-draft` Codex/Claude skill pairs -- code map freshness, exhaustive inventory 구분, temporary touchpoint 통복사 금지 반영
- `.claude/agents/feature-draft.md`, `.codex/agents/feature-draft.toml`, `.claude/agents/spec-review.md`, `.codex/agents/spec-review.toml`, `.claude/agents/spec-update-todo.md`, `.codex/agents/spec-update-todo.toml`, `.claude/agents/spec-update-done.md`, `.codex/agents/spec-update-done.toml` -- wrapper-backed mirror sync
- `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`, `_sdd/spec/logs/changelog.md` -- completed implementation evidence 기준으로 global spec surface 동기화

### References

- feature draft: `_sdd/drafts/2026-05-22_feature_draft_strategic_code_map_spec_skills.md`
- implementation report: `_sdd/implementation/2026-05-22_implementation_report_strategic_code_map_spec_skills.md`
- implementation review: `_sdd/implementation/2026-05-22_implementation_review_strategic_code_map_spec_skills.md`
- commit: `b994366`

## 2026-04-29 - Phase-grouped review-fix gate with adaptive final integration review (v4.1.8 -> v4.1.9 spec revision)

### Context

기존 multi-phase quality gate는 `per-phase` review-fix를 모든 phase에 강제했다. 8 phase 같은 큰 plan에서는 review/fix 횟수가 그대로 phase 수에 비례해 늘어나면서, 같은 의존 관계 안에서 같은 코드를 여러 번 다른 시점에 review하는 비효율이 누적됐다. 사용자는 phase들을 의미 있는 단위로 묶어 그 단위가 끝날 때만 review-fix gate가 닫히는 방식을 제안했다.

이번 라운드에서는 (a) implementation-plan output의 각 phase에 group boundary 결정용 필드(`Checkpoint`)를 추가하고, (b) autopilot이 그 boundary를 읽어 `per-group` gate를 집행하도록 contract를 정렬했으며, (c) 그룹 수에 따라 final integration review를 adaptive하게 처리하도록 했다. 동시에 `phase exit/phase gate/cross-phase` 같은 기존 표현을 group equivalent로 일괄 갱신했다.

### Decision

1. **`implementation-plan` schema에 `Checkpoint: true/false` 필드 추가**: 각 phase가 group의 마지막인지 표시하는 6번째 필드를 6필드 schema(goal, task set/dep, validation, exit criteria, carry-over, **checkpoint**)로 정착. `Checkpoint=true`이면 그 phase 직후 review-fix gate를 닫는다. `Checkpoint=true` phase에는 이유를 기록하는 `Checkpoint Reason` 한 줄을 동반한다. 기본값 `Checkpoint=false`이고 마지막 phase는 explicit 값과 무관하게 implicit `Checkpoint=true`로 처리한다.
2. **review-fix gate scope를 `per-phase`에서 `per-group`으로 전환**: group은 연속된 `Checkpoint=false` phase들 + 그것을 닫는 `Checkpoint=true` phase의 묶음이다. group 내 phase는 light validation(test/typecheck/exit criteria)만 수행하고, group의 마지막에서만 full review-fix-validation gate를 닫는다.
3. **Mid-group emergency**: group 내 phase의 light validation에서 `critical` 이슈가 잡히면 group boundary를 forced early로 즉시 review-fix gate를 트리거한다.
4. **Adaptive final integration review**: 전체 plan에서 group이 1개면 마지막 group gate가 final integration review를 겸한다. group이 2개 이상이면 마지막 group gate 후 cross-group regression 전용으로 final integration review를 1회 추가 실행한다.
5. **Multi-phase ⇒ implementation-plan 의무 (Phase Source invariant)**: multi-phase 실행이 필요하면 반드시 `implementation-plan` step을 포함하고, downstream `implementation`의 `Phase Source`는 `implementation-plan` output을 가리킨다 (`feature-draft` 산출물 사용 금지).
6. **Backward compatibility**: 기존 plan에 `Checkpoint` 필드가 없으면 모든 phase를 `Checkpoint=false`로 간주하고 마지막 phase의 implicit `Checkpoint=true` 1회만 gate를 닫는다 — 단일 group 동작과 동등.

### Rationale

- 의존 관계가 강한 phase 묶음을 한 번에 평가하면 review-fix 횟수와 latency가 크게 줄어들면서도, group 단위로 리뷰 깊이가 상승해 같은 commit-set 안에서 cross-cutting 결함을 잡기 쉽다.
- group 경계 결정은 plan을 작성하는 시점에서 가장 잘 알 수 있다. 따라서 boundary metadata는 autopilot 추론이 아니라 `implementation-plan` output에 owner를 둔다.
- `Checkpoint Reason`은 사후 디버깅·tracing에서 group 경계가 왜 거기에 있는지를 즉시 회수하기 위한 최소 trace다.
- 1개 그룹에서 final integration review를 별도로 두면 마지막 group gate와 100% 중복되므로 adaptive 처리가 필요하다.
- multi-phase에서 `feature-draft` Part 2를 직접 `Phase Source`로 쓰면 phase boundary 해석이 흔들리므로, `implementation-plan` output을 single source of truth로 고정한다.

### Changes

- `.claude/skills/implementation-plan/SKILL.md`, `.codex/skills/implementation-plan/SKILL.md`, `.claude/agents/implementation-plan.md`, `.codex/agents/implementation-plan.toml` -- 6필드 schema + Checkpoint Reason 의무 추가
- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`, `.codex/skills/sdd-autopilot/references/orchestrator-contract.md` -- per-group rule, group boundary, mid-group emergency, adaptive final, invocation contract 일반화, Section 8 Checkpoint Reason 의무
- `.claude/skills/sdd-autopilot/SKILL.md`, `.codex/skills/sdd-autopilot/SKILL.md` -- Step 4/5/7.2/7.3 갱신, backward compat 안내, Phase Source insertion 위치 명시
- `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`, `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- per-group 시나리오로 전면 재작성, Step 3 prompt에 `checkpoint` 필드 포함, AC/Step 5/Test Strategy를 group 표현으로 갱신
- `_sdd/spec/main.md` -- guardrail (line 65) + multi-phase quality gate 결정 (line 94) 갱신, 버전 4.1.9
- `_sdd/spec/components.md` -- `sdd-autopilot` Notes를 per-group + adaptive로 갱신
- `_sdd/spec/usage-guide.md` -- Phase 2 expected result를 per-group + adaptive로 갱신
- `_sdd/spec/logs/changelog.md` -- v4.1.9 이력 추가

### References

- discussion: `_sdd/discussion/2026-04-29_discussion_phase_grouped_review_fix_gate.md`
- feature draft: `_sdd/drafts/2026-04-29_feature_draft_phase_grouped_review_fix_gate.md`
- implementation report: `_sdd/implementation/2026-04-29_implementation_report_phase_grouped_review_fix_gate.md`
- implementation reviews (Pass 1+Pass 2):
  - `_sdd/implementation/2026-04-29_implementation_review_phase_grouped_review_fix_gate.md`
  - `_sdd/implementation/2026-04-29_implementation_review_phase_grouped_review_fix_gate_pass2.md`

## 2026-04-13 - Align spec lifecycle skills around shared core checklist (v4.1.7 -> v4.1.8 spec revision)

### Context

`spec-summary`를 whitepaper surface로 정리한 뒤에도, 나머지 spec lifecycle 스킬(`spec-create`, `spec-review`, `spec-rewrite`, `spec-upgrade`)은 공통 철학과 스킬별 추가 축이 문서 surface에 일관되게 드러나지 않는 상태였다. 특히 `_sdd/spec/components.md`와 `_sdd/spec/usage-guide.md`에는 각 스킬의 현재 contract보다 오래된 설명이 남아 있었고, `/spec-create` expected result에는 여전히 old canonical(`CIV`, `usage`, `decision-bearing structure`) wording이 남아 있었다.

이번 구현에서는 definition/workflow 문서와 실제 skill contract를 먼저 정렬했고, 그 결과를 global supporting surface와 history surface에 반영할 필요가 생겼다.

### Decision

1. **공통 코어 4축을 spec lifecycle 공통 기준선으로 고정**: `Thinness`, `Decision-bearing truth`, `Anti-duplication`, `Navigation + surface fit`을 definition 문서 기준선으로 본다.
2. **각 스킬의 1차 추가 축을 supporting surface에도 반영**:
   - `spec-create`: structure rationale + `single-file default`
   - `spec-review`: rubric separation + evidence strictness
   - `spec-rewrite`: rationale preservation + body/log placement
   - `spec-upgrade`: rewrite boundary judgment
3. **`usage-guide`의 stale wording 제거**: `/spec-create` expected result에서 old canonical(`CIV`, `usage`, `decision-bearing structure`) 표현을 제거하고 thin global 기준으로 정리한다.
4. **history 역할 분리 유지**: 판단 근거는 `DECISION_LOG.md`, 파일/버전 이력은 `logs/changelog.md`에 남긴다.

### Rationale

- 공통 코어가 definition 문서에만 있고 supporting surface가 예전 의미를 반복하면, 사용자와 에이전트가 읽는 operational surface가 다시 drift한다.
- `spec-review`의 핵심 가치는 더 많이 지적하는 것이 아니라, 맞는 rubric과 evidence 기준으로 오탐을 줄이는 것이다.
- `spec-create`의 기본값을 single-file로 명시하지 않으면 premature multi-file split이 다시 기본 경로처럼 읽힐 수 있다.
- `spec-rewrite`와 `spec-upgrade`는 둘 다 global spec을 얇게 만들지만, 하나는 구조 개선이고 다른 하나는 migration이므로 boundary를 supporting docs에서도 드러내는 편이 안전하다.

### Changes

- `_sdd/spec/components.md` -- `spec-create`, `spec-review`, `spec-rewrite`, `spec-upgrade` 설명을 현재 contract에 맞게 보정
- `_sdd/spec/usage-guide.md` -- `/spec-create` expected result를 thin global + single-file default 기준으로 정리
- `_sdd/spec/logs/changelog.md` -- v4.1.8 이력 추가

### References

- feature draft: `_sdd/drafts/2026-04-13_feature_draft_spec_lifecycle_core_checklist_alignment.md`
- implementation report: `_sdd/implementation/2026-04-13_implementation_report_spec_lifecycle_core_checklist_alignment.md`
- implementation review: `_sdd/implementation/2026-04-13_implementation_review_spec_lifecycle_core_checklist_alignment.md`

## 2026-04-13 - Position spec-summary as reader-facing whitepaper surface (v4.1.6 -> v4.1.7 spec revision)

### Context

`spec-summary`는 `_sdd/spec/summary.md`를 만드는 surface이지만, active `_sdd/spec/` supporting docs에는 여전히 canonical overview 중심 설명이 남아 있었다. 이 표현은 현재 skill/docs 쪽에서 이미 정렬된 whitepaper contract와 어긋난다. 이 저장소에서 `summary.md`는 thin global spec을 다시 두껍게 복제하는 문서가 아니라, 문제의식과 배경/동기, 핵심 설계, 코드 근거, 사용 흐름과 기대 결과를 사람이 한 문서로 읽게 하는 reader-facing whitepaper여야 한다.

### Decision

1. **`spec-summary`를 whitepaper surface로 고정**: `_sdd/spec/summary.md`는 repo/spec를 설명하는 reader-facing whitepaper로 본다.
2. **필수 section spine 고정**: `Executive Summary`, `Background / Motivation`, `Core Design`, `Code Grounding`, `Usage / Expected Results`, `Further Reading / References`를 기본 본문 구조로 사용한다.
3. **`Code Grounding` 필수화**: summary는 concrete path, symbol, source table 같은 anchor로 설명을 실제 구현과 연결해야 한다.
4. **planned/progress는 appendix로만 허용**: 관련 draft/implementation artifact가 있을 때만 마지막 보조 섹션으로 짧게 붙인다.
5. **history narration 분리 유지**: summary surface 자체는 현재 기준 내용만 직접 설명하고, 과거 판단과 변경 이력은 `DECISION_LOG.md`와 `logs/changelog.md`에서 추적한다.

### Rationale

- `summary.md`의 핵심 가치는 "빠른 상태표"보다 "왜 이런 구조인지와 실제 근거가 무엇인지"를 이해시키는 데 있다.
- global spec이 thin core를 유지하더라도, 사람은 배경/동기/설계/사용 서사를 한 문서에서 읽을 whitepaper surface가 필요하다.
- `Code Grounding`이 없는 whitepaper는 일반 소개문으로 무너지기 쉽고, 반대로 appendix-only planned/progress rule이 없으면 본문이 다시 status memo로 오염된다.
- history narration을 summary 본문에서 분리하면 summary surface는 설명 문서로 남고, history surface는 change-tracking 역할에 집중할 수 있다.

### Changes

- `_sdd/spec/components.md` -- `spec-summary`를 reader-facing whitepaper surface로 설명
- `_sdd/spec/usage-guide.md` -- `/spec-summary` expected result를 whitepaper section spine으로 정렬
- `_sdd/spec/logs/changelog.md` -- v4.1.7 이력 추가

### References

- feature draft: `_sdd/drafts/2026-04-13_feature_draft_spec_summary_whitepaper_surface.md`
- implementation progress: `_sdd/implementation/2026-04-13_implementation_progress_spec_summary_whitepaper_surface.md`
- implementation report: `_sdd/implementation/2026-04-13_implementation_report_spec_summary_whitepaper_surface.md`
- implementation review: `_sdd/implementation/2026-04-13_implementation_review_spec_summary_whitepaper_surface.md`
- orchestrator: `_sdd/pipeline/orchestrators/orchestrator_spec_summary_whitepaper_surface.md`

## 2026-04-13 - Reframe spec-summary as canonical overview with optional planned/progress snapshot (v4.1.5 -> v4.1.6 spec revision)

### Context

`spec-summary`는 이미 `_sdd/spec/summary.md`를 만드는 human-readable summary surface였지만, active skill contract와 supporting docs에는 여전히 "현재 스펙 상태"와 `global/temporary spec 요약` 관점이 남아 있었다. 이 표현은 `summary.md`를 사람용 canonical overview로 보려는 현재 thin global 철학과 맞물릴 때 역할이 흐려졌다. global spec은 장기적 판단 기준을 고정하고, 세부 설명은 supporting surface로 내리는 방향인데, `summary.md`가 다시 status sheet나 temporary summary처럼 읽히면 목적/경계/핵심 결정/다음 surface를 빠르게 잡아주는 역할이 약해진다.

### Decision

1. **`spec-summary`의 1차 역할을 canonical overview로 고정**: `_sdd/spec/summary.md`는 global spec과 supporting surface를 읽는 사람에게 목적, 경계, 핵심 결정, 다음에 읽을 surface를 빠르게 전달하는 문서로 본다.
2. **temporary summary 독립 모드는 제거**: `spec-summary`는 temporary spec 자체를 별도 summary mode로 다루지 않는다.
3. **planned/progress snapshot은 보조 정보로만 허용**: 관련 `_sdd/drafts/` 또는 `_sdd/implementation/` artifact가 있을 때만 `Planned / In Progress / Blocked / Next` 수준의 짧은 snapshot을 뒤쪽에 덧붙인다.
4. **navigation naming 고정**: summary의 navigation 섹션 명칭은 `Where Details Live`를 사용한다.
5. **history narration 금지**: `spec-summary` 본문과 template/example은 migration memo처럼 과거와 현재를 비교하지 않고, 현재 기준의 계약과 output shape만 직접 서술한다.
6. **history docs는 역할 분리 유지**: semantic shift의 판단 근거는 `DECISION_LOG.md`, 변경 파일/버전 이력은 `logs/changelog.md`에 남긴다.

### Rationale

- 사람이 `summary.md`에서 얻어야 할 가치는 "상태 표"보다 "이 repo를 어떤 기준으로 읽고 어디를 더 보면 되는가"에 가깝다.
- temporary spec은 실행 청사진이라 draft/implementation artifact 자체가 주 문맥이므로, `spec-summary`가 이를 다시 독립 summary surface로 복제할 이유가 약하다.
- optional planned/progress snapshot만 남기면 overview의 선명함을 유지하면서도 현재 진행 상태를 빠르게 붙일 수 있다.
- `Where Details Live`는 `How to Read This Spec`보다 덜 메타적이고, `Reading Map`보다 직관적으로 다음 탐색 경로를 설명한다.
- `spec-summary` 본문에 변경 이력 서술을 넣지 않고 final form만 남기면 summary surface 자체가 다시 history-heavy 문서로 오염되는 것을 막을 수 있다.

### Changes

- `.codex/skills/spec-summary/SKILL.md` -- canonical overview + optional planned/progress snapshot 계약으로 재작성
- `.claude/skills/spec-summary/SKILL.md` -- mirror contract 동기화
- `.codex/skills/spec-summary/skill.json` -- version/description를 `2.0.0` semantics로 정렬
- `.claude/skills/spec-summary/skill.json` -- version/description를 `2.0.0` semantics로 정렬
- `.codex/skills/spec-summary/references/summary-template.md` -- `Where Details Live` + optional snapshot 구조로 재배치
- `.claude/skills/spec-summary/references/summary-template.md` -- mirror template sync
- `.codex/skills/spec-summary/examples/summary-output.md` -- overview-first example로 갱신
- `.claude/skills/spec-summary/examples/summary-output.md` -- mirror example sync
- `_sdd/spec/components.md` -- `spec-summary` 목적/이유/notes를 canonical overview 기준으로 보정
- `_sdd/spec/usage-guide.md` -- `/spec-summary` expected result를 overview-first wording으로 보정
- `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md` -- `spec-summary` semantics 보정
- `docs/en/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_WORKFLOW.md` -- 영문 mirror sync
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- downstream taxonomy 보정
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- downstream taxonomy 보정
- `_sdd/spec/logs/changelog.md` -- v4.1.6 이력 추가

### References

- 구현 draft: `_sdd/drafts/2026-04-13_feature_draft_spec_summary_canonical_overview_alignment.md`
- implementation review: `_sdd/implementation/2026-04-13_implementation_review_spec_summary_canonical_overview_alignment.md`
- orchestrator: `_sdd/pipeline/orchestrators/orchestrator_spec_summary_canonical_overview_alignment.md`

## 2026-04-10 - Sync autopilot planning semantics and artifact naming invariants into global spec (v4.1.4 -> v4.1.5 spec revision)

### Context

2026-04-10 커밋들에서 `sdd-autopilot`, `implementation-plan`, `discussion`, `spec-update-done` 주변 계약이 크게 정리됐다. non-trivial change의 기본 planning entry를 `feature-draft`로 고정하고, `implementation-plan`을 후속 확장 단계로 재정의했으며, multi-phase plan은 실제 execution gate로 소비되어 `per-phase` review-fix와 `final integration review`를 강제하게 됐다. 동시에 skill-defined output artifact naming은 date-prefixed slug 규칙으로 정렬되고, `prev/` 백업 체인 대신 append-only artifact + git history를 기본 추적 방식으로 사용하는 방향이 굳어졌다.

하지만 active `_sdd/spec/` surface에는 이 운영 규칙들이 아직 직접 반영되지 않아, `_sdd/spec/usage-guide.md`에는 여전히 오래된 autopilot 실행 경로와 단순화된 planning path가 남아 있었고, global main body에도 새 artifact naming / phase gate semantics가 빠져 있었다.

### Decision

1. **planning precedence를 global rule로 승격**: non-trivial change의 기본 planning entry는 `feature-draft`이며, `implementation-plan`은 Part 2만으로 부족하거나 phase/task 세분화가 필요할 때만 붙는 후속 확장 단계로 정리한다.
2. **multi-phase plan을 execution gate로 고정**: multi-phase plan이 생성되면 `per-phase` review-fix와 phase exit 검증, 마지막 `final integration review`를 repo-wide 운영 규칙으로 본다.
3. **artifact naming/history invariant 명시**: 신규 temporary artifact는 lowercase canonical 경로를 기본으로 사용하고, skill-defined output surface는 dated slug 경로를 따른다. `prev/` 백업 체인 대신 append-only artifact + git history를 기본 추적 방식으로 삼는다.
4. **reader fallback 원칙 유지**: skill/agent reader는 legacy uppercase/fixed-name artifact를 fallback으로 읽을 수 있어야 한다.
5. **autopilot authoritative path 정렬**: 실행 중 활성 오케스트레이터의 기준 경로는 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`로 본다.

### Rationale

- planning precedence가 global spec에 없으면 `feature-draft`와 `implementation-plan`이 다시 peer choice처럼 해석돼 pipeline selection이 흔들린다.
- multi-phase plan을 단순 문서로 두면 phase boundary에서 defect containment가 무너지고 review-fix loop가 늦게 작동한다.
- skill-defined output surface의 dated slug naming은 여러 skill이 공통으로 사용하는 경로 추론 규칙이라, global spec 차원에서 묶어야 repo-level reasoning과 review 판단이 일관된다.
- `prev/` 백업 체인을 canonical rule로 남겨 두면 실제 skill contract와 global spec이 다시 drift한다.
- active orchestrator 경로가 global usage surface와 실제 guide 문서에서 다르면 autopilot 재개/검증 흐름을 잘못 이해하게 된다.

### Changes

- `_sdd/spec/main.md` -- planning precedence, phase-gated execution, artifact naming/history invariant, mirror sync 운영 제약 반영
- `_sdd/spec/components.md` -- `sdd-autopilot`, `implementation-plan`, `spec-update-done`, `discussion`, platform artifact-path note 보강
- `_sdd/spec/usage-guide.md` -- manual/autopilot scenario를 optional expansion + per-phase gate semantics로 정렬, active orchestrator 경로 수정
- `_sdd/spec/logs/changelog.md` -- v4.1.5 이력 추가

### References

- 구현 draft: `_sdd/drafts/2026-04-10_feature_draft_autopilot_planning_phase_gates.md`
- implementation review: `_sdd/implementation/2026-04-10_implementation_review_autopilot_planning_phase_gates.md`
- implementation report: `_sdd/implementation/2026-04-10_implementation_report_autopilot_planning_phase_gates.md`
- review fix report: `_sdd/implementation/2026-04-10_implementation_report_autopilot_planning_phase_gates_review_fixes.md`
- commits: `ee4e1cd`, `d32686a`, `aa92c83`, `0725c25`

## 2026-04-04 - Compact components reference surface (v4.1.0 -> v4.1.1 spec revision)

### Context

`_sdd/spec/components.md`는 이미 `main.md`에서 분리된 supporting surface였지만, 각 컴포넌트마다 Input/Output/Process/Dependencies/완료 이력을 길게 재서술하면서 reference 문서라기보다 mini-spec catalog에 가까워져 있었다. global main body를 얇게 줄인 뒤에도 `components.md`가 너무 두꺼우면, 결국 active spec surface 전체의 탐색 비용이 다시 커진다.

### Decision

1. **`components.md`를 compact reference catalog로 재작성**: 카테고리별 table에서 각 컴포넌트의 `Purpose / Why / Primary Source / Notes`만 유지
2. **runtime 차이는 최소 note로만 보존**: wrapper -> agent, full skill, Claude-only 같은 탐색용 차이만 남김
3. **상세 재복제 제거**: Input/Output/Process/Dependencies/완료 이력은 각 `SKILL.md`, agent 정의, 관련 artifact에서 찾도록 정리
4. **strategic code map 유지**: 전수형 inventory 대신 navigation-critical path appendix는 계속 유지

### Rationale

- supporting surface는 main의 decision-bearing truth를 보조해야지, 또 다른 두꺼운 본문이 되면 안 된다
- 컴포넌트별로 truly reference value가 높은 것은 `무엇을 하는가`, `왜 필요한가`, `어디를 먼저 봐야 하는가`다
- 세부 step과 artifact shape는 원문 skill 문서가 authoritative source이므로, `components.md`에서 다시 길게 복제할 이유가 약하다
- compact catalog는 신규 사용자와 유지보수자 모두에게 탐색 속도를 높여 준다

### Changes

- `_sdd/spec/main.md` -- v4.1.1로 version bump
- `_sdd/spec/components.md` -- 284줄 -> 71줄 compact catalog로 재작성
- `_sdd/spec/logs/spec-rewrite-plan.md` -- components compact rewrite addendum 추가
- `_sdd/spec/logs/rewrite_report.md` -- 2차 리라이트 결과 반영
- `_sdd/spec/logs/changelog.md` -- v4.1.1 이력 추가
- `_sdd/spec/prev/prev_components_20260404_130827.md` -- 백업
- `_sdd/spec/prev/prev_spec-rewrite-plan_20260404_130827.md` -- 백업
- `_sdd/spec/prev/prev_rewrite_report_20260404_130827.md` -- 백업
- `_sdd/spec/prev/prev_DECISION_LOG_20260404_130827.md` -- 백업
- `_sdd/spec/prev/prev_changelog_20260404_130827.md` -- 백업

### References

- 리라이트 계획: `_sdd/spec/logs/spec-rewrite-plan.md`
- 리라이트 결과: `_sdd/spec/logs/rewrite_report.md`
- component source surface: `.claude/skills/`, `.claude/agents/`, `.codex/skills/`, `.codex/agents/`

## 2026-04-04 - Rewrite global spec to thin mandatory core (v4.0.1 -> v4.1.0 spec revision)

### Context

`_sdd/spec/main.md`는 이미 current canonical model을 반영한 상태였지만, global main body가 다시 두꺼워진 상태였다. standalone `Contract / Invariants / Verifiability` 표, usage summary, decision-bearing structure 대형 표, reference/code-map appendix가 한 문서 안에 함께 들어오면서, definition 문서가 말하는 `개념 + 경계 + 결정` 중심의 thin global core보다 넓은 책임을 다시 떠안고 있었다.

### Decision

1. **`main.md`를 3개 mandatory core 중심으로 재압축**: `Background`, `Scope / Non-goals / Guardrails`, `Core Design and Key Decisions`만 numbered main body로 유지
2. **repo-wide invariant는 별도 CIV 표 대신 guardrails/key decisions에 흡수**: global spec에 남아야 할 운영 규칙만 문장형으로 유지
3. **usage/reference/detail surface는 supporting file로 명시적 하향**: `components.md`, `usage-guide.md`, `DECISION_LOG.md`, `logs/changelog.md`를 thin main 바깥의 supporting surface로 재정의
4. **supporting file 도입부 정합성 보정**: 더 이상 존재하지 않는 `§5`, `§7`, appendix 참조를 제거
5. **backup rule 유지**: rewrite 전 `prev_main_20260404_130259.md`, `prev_components_20260404_130259.md`, `prev_usage-guide_20260404_130259.md`, `prev_DECISION_LOG_20260404_130259.md`를 생성

### Rationale

- `docs/SDD_SPEC_DEFINITION.md`는 global spec의 mandatory core를 3개 섹션으로 제한하고, usage/reference/CIV/code-map을 기본 코어 밖 surface로 내리라고 정의한다
- `docs/SDD_WORKFLOW.md` 역시 global spec은 모든 detail의 저장소가 아니라고 못 박고, feature/task/validation detail은 temporary 또는 supporting surface에서 다루도록 정리한다
- 현재 저장소에서 truly repo-wide한 판단은 이미 충분히 정리돼 있으므로, 새 내용을 추가하는 것보다 main responsibility를 줄이는 편이 canonical fit에 더 가깝다
- 구조 판단을 잃지 않으면서도 main token cost를 줄이면 사람과 AI 모두 기준 문서를 더 빠르게 읽을 수 있다

### Changes

- `_sdd/spec/main.md` -- v4.1.0 thin global spec으로 재작성 (257줄 -> 111줄)
- `_sdd/spec/components.md` -- supporting surface 역할 문구 보정
- `_sdd/spec/usage-guide.md` -- supporting surface 역할 문구 보정
- `_sdd/spec/logs/spec-rewrite-plan.md` -- thin rewrite 계획 갱신
- `_sdd/spec/logs/rewrite_report.md` -- 실행 결과 기록
- `_sdd/spec/logs/changelog.md` -- v4.1.0 이력 추가
- `_sdd/spec/prev/prev_main_20260404_130259.md` -- 백업
- `_sdd/spec/prev/prev_components_20260404_130259.md` -- 백업
- `_sdd/spec/prev/prev_usage-guide_20260404_130259.md` -- 백업
- `_sdd/spec/prev/prev_DECISION_LOG_20260404_130259.md` -- 백업

### References

- 정의 문서: `docs/SDD_SPEC_DEFINITION.md`
- 워크플로우 문서: `docs/SDD_WORKFLOW.md`
- 리라이트 계획: `_sdd/spec/logs/spec-rewrite-plan.md`
- 리라이트 결과: `_sdd/spec/logs/rewrite_report.md`

## 2026-04-04 - Upgrade global spec to current canonical SDD model (v3.9.1 -> v4.0.0 spec revision)

### Context

`_sdd/spec/main.md`는 이미 멀티파일 구조로 분리돼 있었지만, 본문 구조가 여전히 `Background / Core Design / Architecture / Component Details / Usage Guide` 중심의 legacy section map에 가까웠다. 특히 current canonical model이 요구하는 `Scope / Non-goals / Guardrails`, `Contract / Invariants / Verifiability`, `Decision-bearing structure`가 독립 section으로 고정돼 있지 않았고, component inventory와 code reference index가 본문/부록에서 과도하게 큰 비중을 차지했다.

### Decision

1. **`main.md`를 canonical global spec으로 재구성**: section 1~7과 appendix 구조를 current SDD spec definition에 맞춰 재배치
2. **CIV 명시 복구**: `Contract`, `Invariants`, `Verifiability`를 독립 표 구조로 추가하고, `_sdd/` artifact contract, wrapper/agent split, autopilot verification semantics를 연결
3. **Decision-bearing structure 분리**: 시스템 경계, ownership, cross-component contract, extension point, invariant hotspot을 별도 section으로 승격
4. **supporting file 역할 재정의**: `components.md`는 reference-only supporting file로 유지하고, 전수형 code reference index는 strategic code map으로 축약
5. **usage guide 정렬**: `usage-guide.md`를 section 5 보조 문서로 명시하고 expected result를 current canonical model 기준으로 보정
6. **legacy path 보존**: `DECISION_LOG.md` uppercase 경로는 기존 링크와 이력 보존을 위해 유지

### Rationale

- current canonical model은 global spec을 thin decision document로 유지하고 inventory-heavy detail을 supporting reference로 내릴 것을 요구한다
- 이 저장소는 코드보다 skill contract와 docs alignment가 핵심이므로, explicit CIV와 decision-bearing structure가 없으면 `spec-review`, `spec-update-*`, `sdd-autopilot` semantics가 다시 암묵화된다
- 멀티파일 구조 자체는 이미 충분히 유효하므로, 이번 작업은 `spec-rewrite`가 아니라 in-place `spec-upgrade`가 적절했다
- exhaustive code/file listing은 appendix-level strategic navigation hint로 축소하는 편이 current SDD definition과 더 잘 맞는다

### Changes

- `_sdd/spec/main.md` -- current canonical global spec structure로 전면 재작성
- `_sdd/spec/components.md` -- reference-only 역할 명시, `spec-upgrade` 설명 갱신, strategic code map으로 축약
- `_sdd/spec/usage-guide.md` -- section 5 보조 문서 역할과 expected result 정렬
- `_sdd/spec/prev/prev_main_20260404_015836.md` -- 백업
- `_sdd/spec/prev/prev_components_20260404_015836.md` -- 백업
- `_sdd/spec/prev/prev_usage-guide_20260404_015836.md` -- 백업
- `_sdd/spec/prev/prev_DECISION_LOG_20260404_015836.md` -- 백업

### References

- 정의 문서: `docs/SDD_SPEC_DEFINITION.md`
- 워크플로우 문서: `docs/SDD_WORKFLOW.md`
- 업그레이드 스킬: `.codex/skills/spec-upgrade/SKILL.md`

## 2026-04-03 - Spec rewrite: single-file to index + sub-file structure (v3.8.2 → v3.9.0)

### Context

main.md가 1206줄(32,933 토큰)으로 비대해져 AI 에이전트의 컨텍스트 로드와 사용자의 정보 탐색 모두 비효율적이었다. 8개 핵심 metric 진단 결과 Component Separation과 Findability가 2점(3점 만점)으로, 구조적 개선이 필요했다. Whitepaper 핵심 narrative(§1-§3)는 양호하나 Component Details, Usage Guide, Changelog가 본문에 포함되어 불필요한 길이를 차지하고 있었다.

### Decision

1. **main.md를 인덱스로 전환**: §1-§3(Background, Core Design, Architecture)은 인라인 유지, §4 상세/§5/Changelog는 별도 파일로 분리
2. **신규 파일 3개 생성**: `components.md`(§4 + Code Reference Index), `usage-guide.md`(§5), `logs/changelog.md`(Changelog 이동)
3. **해결 완료 이슈 삭제**: #1-4, #8-16번을 본문에서 제거 (changelog에서 이미 추적 가능)
4. **§4 요약 테이블 + 에이전트 목록은 main에 유지**: 컴포넌트 탐색 진입점 역할

### Rationale

- template-compact.md 기준 중규모(500-1500줄) 스펙은 인덱스 + 컴포넌트 파일 구조가 권장됨
- main.md 경량화로 AI 에이전트의 컨텍스트 효율이 향상됨 (668줄, 45% 감축)
- whitepaper 핵심 narrative(§1, §2, §5)는 모두 보존됨 — §5는 별도 파일이지만 1-hop 접근 가능
- 모든 컴포넌트의 Why 필드, Design Rationale 테이블, Source 매핑이 원본 그대로 보존됨

### Changes

- `_sdd/spec/main.md` — v3.8.2 → v3.9.0 (1206줄 → 668줄)
- `_sdd/spec/components.md` — 신규 생성 (303줄)
- `_sdd/spec/usage-guide.md` — 신규 생성 (84줄)
- `_sdd/spec/logs/changelog.md` — 신규 생성 (Changelog 이동)
- `_sdd/spec/logs/spec-rewrite-plan.md` — 진단 및 계획
- `_sdd/spec/logs/rewrite_report.md` — 실행 결과 리포트
- `_sdd/spec/prev/prev_main.md_20260403_000930.md` — 백업

### References

- 진단/계획: `_sdd/spec/logs/spec-rewrite-plan.md`
- 실행 리포트: `_sdd/spec/logs/rewrite_report.md`

## 2026-04-01 - Tighten implementation review loop exit criteria and retry handoff

### Context

Codex `implementation`에 iteration review loop를 도입한 뒤 첫 implementation-review에서 세 가지 후속 문제가 드러났다. 첫째, `_sdd/env.md`가 없을 때 `UNTESTED`만으로도 PASS가 가능해 검증되지 않은 구현이 종료될 수 있었다. 둘째, `IMPLEMENTATION_REPORT.md` 생성과 `UNTESTED` 근거 기록 요구가 loop 종료 조건과 느슨하게 연결되어 있었다. 셋째, Step 7.4에 retry context를 반드시 다음 worker/sub-agent에 전달하라는 계약이 부족했다. Claude 구현도 같은 review loop semantics를 공유하고 있어 동일한 함정을 갖고 있었다.

### Decision

1. **`UNTESTED` 허용 범위 축소**: `UNTESTED`는 단순 "테스트 못 돌림"이 아니라, 테스트 불가 사유와 코드 분석 근거를 리포트에 명시할 수 있을 때만 허용
2. **PASS 게이트 강화**: 종료 조건은 "모든 AC가 `MET`이거나, `UNTESTED` 항목마다 근거와 사유가 기록되어 있고 `Critical/High == 0`"으로 고정
3. **Report requirement 명시**: `implementation` Acceptance Criteria와 Step 8 Report에 `IMPLEMENTATION_REPORT.md` 생성 및 `UNTESTED` 근거 기록 요구를 반영
4. **Retry handoff contract 필수화**: iteration 재실행 prompt에는 `failed_ac`, `failure_reason`, `open_critical_high_issues`를 반드시 포함하고, worker/sub-agent는 이전 실패를 어떻게 해소했는지 보고
5. **Claude/Codex parity 유지**: 위 보정을 `.claude`와 `.codex` 양쪽 `implementation` 문서에 동일하게 반영

### Rationale

- raw `UNTESTED` PASS는 검증되지 않은 구현을 조용히 성공 처리하는 위험이 있었다
- `UNTESTED`를 예외적 상태로 좁혀야 Verification Gate 철학과 iteration review loop가 일관된다
- retry context가 빠지면 loop가 "같은 작업을 다시 해 본다" 수준으로 약해져 실패 원인 교정 능력이 떨어진다
- review loop semantics가 런타임마다 갈라지면 spec과 운영 기준이 다시 쉽게 drift한다

### Changes

- `.codex/skills/implementation/SKILL.md` -- `UNTESTED` 판정/종료 조건/Step 7.4 retry handoff/Report requirement 보정
- `.codex/agents/implementation.toml` -- custom agent mirror 동기화
- `.claude/skills/implementation/SKILL.md` -- retry context block 추가, `UNTESTED` 종료 기준 보정
- `.claude/agents/implementation.md` -- sub-agent prompt 및 review loop semantics 동기화
- `_sdd/spec/main.md` -- implementation component details, changelog 갱신

### References

- 구현 리뷰: `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
- 구현 리포트: `_sdd/implementation/IMPLEMENTATION_REPORT.md`

## 2026-04-01 - Remove write_skeleton and adopt producer-owned inline 2-phase writing

### Context

`write_skeleton` helper agent는 skeleton-first writing 품질을 높이려는 의도로 도입되었지만, 실제 운영에서는 caller가 부모 콘텍스트를 다시 말아 전달해야 하는 비용이 컸다. 특히 skeleton 생성은 현재 호출자의 문맥, 직전 판단, 참고 파일 해석에 강하게 의존하여 `fork_context`, handoff contract, 반환 해석 규칙이 늘어나는 문제가 있었다.

### Decision

1. **`write_skeleton` 완전 제거**: `.claude/agents/write-skeleton.md`, `.codex/agents/write-skeleton.toml` 삭제
2. **Producer-Owned Inline 2-Phase Writing 채택**: 장문 문서/리포트/패치 초안은 caller가 현재 콘텍스트에서 skeleton → fill → finalize를 같은 흐름에서 직접 수행
3. **`write-phased` 재정의**: helper orchestrator가 아니라 공용 inline writing contract로 유지
4. **Caller 문구 정리**: Claude/Codex의 `feature-draft`, `implementation-plan`, `implementation-review`, `spec-create`, `guide-create`, `pr-review`, `pr-spec-patch`, `spec-summary`, `spec-upgrade` 등 writing producer 문서에서 helper 호출 전제를 제거
5. **Spec sync**: `_sdd/spec/main.md`의 agent inventory, directory structure, design pattern, runtime guidance를 현재 구조에 맞게 동기화

### Rationale

- skeleton 생성은 helper 분리보다 부모 콘텍스트 보존이 더 중요했다
- helper layer는 실제로 handoff complexity와 사용성 비용을 증가시켰다
- inline 2-phase writing은 중간 구조를 드러내면서도 context re-packaging 없이 품질을 유지한다
- 플랫폼별 subagent 문법 차이를 줄여 Claude/Codex parity를 단순화할 수 있다

### Changes

- `.claude/agents/write-skeleton.md` -- 삭제
- `.codex/agents/write-skeleton.toml` -- 삭제
- `.claude/skills/write-phased/`, `.codex/skills/write-phased/` -- inline 2-phase writing contract로 재작성
- `.claude/agents/`, `.claude/skills/`, `.codex/agents/`, `.codex/skills/`의 writing producer 문구 -- helper 호출에서 caller-owned skeleton 작성 규칙으로 치환
- `_sdd/spec/main.md` -- version bump, counts 갱신, Producer-Owned Inline 2-Phase Writing 패턴 반영

### References

- 드래프트: `_sdd/drafts/feature_draft_remove_write_skeleton_inline_writing.md`
- 토론: `_sdd/discussion/discussion_write_skeleton_removal_and_inline_writing.md`

## 2026-03-20 - AC-First + Self-Contained 전면 리팩토링 (v3.5.0 -> v3.6.0)

### Context

v3.0에서 도입된 Agent Wrapper 패턴에서, 5개 agent가 skill 디렉토리의 `references/`를 명시적으로 참조하지만 subagent로 실행 시 해당 파일에 접근 불가. Plugin 환경에서도 동일. 또한 agent/skill 파일이 비대하여(agent 9개 합계 4,365줄, full skill 11개 합계 5,042줄) 핵심 로직이 Best Practices, Context Management 등 bloat에 묻혀 있었다.

### Decision

1. **AC-First 구조 전면 적용**: 모든 9개 Claude agent, 11개 Claude full skill, 9개 Codex agent, 10개 Codex full skill에 Acceptance Criteria + 자체 검증 지시(blockquote) + Final Check 추가
2. **Self-Contained Agent**: 핵심 reference 내용을 agent 파일에 인라인 (원본 대비 70%+ 압축), 외부 reference 의존성 완전 제거
3. **공통 bloat 제거**: Best Practices, Context Management, When to Use, Version History, Integration with Other Skills 등 공통 섹션 삭제
4. **래퍼 스킬 정리**: Claude 9개 + Codex 8개 wrapper skill에서 미사용 references/examples 총 48개 파일 삭제
5. **Codex 통일**: Final Smoke Check 제거, Final Check으로 통일
6. **ralph-loop-init 범용화**: "ML 트레이닝 디버그" -> "장기 실행 프로세스(ML, e2e, 빌드 등)"
7. **SDD workflow 세부**: implementation-plan Target Files 충돌 규칙 수정, spec-update-todo 기본 상태 마커 📋 명시, implementation-plan/implementation-review 리팩토링 메타 AC 삭제

### Rationale

- Agent가 subagent로 실행 시 skill 디렉토리 접근 불가 -- self-contained가 유일한 해결책
- AC-First로 실행 결과가 명확히 측정 가능하고, Final Check으로 자체 품질 보장
- Bloat 제거로 LLM 컨텍스트 윈도우 효율 극대화 (Claude agent 55%, full skill 46% 감축)
- 4개 커밋으로 일관된 구조 적용 완료 (7141c70, a751c11, 0ce7fcc, 675ce75)

### Changes

- `.claude/agents/*.md` -- 9개 agent AC-First + self-contained 재작성 (4,365줄 -> 1,961줄)
- `.claude/skills/*/SKILL.md` -- 11개 full skill AC-First 정제 (5,042줄 -> 2,718줄)
- `.codex/agents/*.toml` -- 9개 agent AC-First 정비
- `.codex/skills/*/SKILL.md` -- 10개 full skill AC-First 정제
- `.claude/skills/*/references/`, `.claude/skills/*/examples/` -- 래퍼 스킬 48개 파일 삭제
- `.codex/skills/*/references/`, `.codex/skills/*/examples/` -- Codex 래퍼 스킬 파일 삭제
- `_sdd/spec/main.md` -- v3.5.0 -> v3.6.0

### References

- 드래프트: `_sdd/drafts/feature_draft_agent_self_containment.md`
- 드래프트: `_sdd/drafts/feature_draft_agent_self_containment_phase2.md`
- 드래프트: `_sdd/drafts/feature_draft_full_skills_ac_first.md`
- 드래프트: `_sdd/drafts/feature_draft_codex_agent_wrapper_diet.md`
- 드래프트: `_sdd/drafts/feature_draft_codex_full_skills_ac_first.md`

## 2026-03-19 - sdd-autopilot v2.0.0 Reasoning-Based Rewrite (v3.4.1 -> v3.5.0)

### Context

sdd-autopilot v1.0.0은 규모별 템플릿 매칭(소/중/대 3가지 경로)으로 파이프라인을 구성했다. 이 방식은 3가지 고정 경로만 가능하여 유연성이 제한적이었다. harness 철학에서 영감을 받아, SDD 철학을 이해하고 상황에 맞게 스킬을 동적으로 조합하는 reasoning 기반 오케스트레이션으로 전환하기로 결정했다.

### Decision

1. **SKILL.md 전면 리라이트**: 규모별 템플릿 매칭 -> SDD reference 기반 reasoning + 동적 파이프라인 구성
2. **Reference 문서 통합**: `references/pipeline-templates.md` + `references/scale-assessment.md` 삭제, `references/sdd-reasoning-reference.md` 신규 생성 (docs/ 4개 문서를 ~310줄로 압축, SDD 철학 + 스킬 카탈로그)
3. **Step 구조 변경**: Step 1(Reference Loading), Step 4(Reasoning -> Orchestrator), Step 5(Verification) 신규 추가
4. **Orchestrator Verification**: Producer-Reviewer 패턴으로 구조 6항목 + 철학 6항목 = 12항목 자동 검증
5. **Hard Rule #10 추가**: Execute -> Verify 필수
6. **비오케스트레이션 스킬 재분류**: spec-create, discussion, guide-create는 autopilot 파이프라인에 넣지 않는 스킬로 명시
7. **Dependencies 변경**: 글로벌 스펙 존재 필수 (없으면 /spec-create 안내)

### Rationale

- 규모별 3가지 고정 경로에서 상황 맞춤 무한 조합으로 유연성 확대
- Reference 문서를 Step 1에서 Read하여 reasoning의 기반으로 사용 -- "사람이 docs를 읽고 reasoning하듯이 autopilot도 동일 과정"
- Producer-Reviewer 패턴으로 동적 생성의 리스크를 관리 (구조 의존성 + SDD 철학 정합성 검증)
- Hard Rules(#9 review-fix, #10 execute-verify)와 파일 기반 상태 전달 등 검증된 규칙은 보존

### Changes

- `.claude/skills/sdd-autopilot/SKILL.md` -- v1.0.0 -> v2.0.0 전면 리라이트
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- 신규 생성
- `.claude/skills/sdd-autopilot/references/pipeline-templates.md` -- 삭제 (reference에 흡수)
- `.claude/skills/sdd-autopilot/references/scale-assessment.md` -- 삭제 (reference에 흡수)
- `.claude/skills/sdd-autopilot/skill.json` -- v2.0.0으로 업데이트
- `.codex/skills/sdd-autopilot/SKILL.md` -- v2.0.1 동일 아키텍처 동기화 (Codex 차이점 보존)
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- 신규 생성
- `_sdd/spec/main.md` -- v3.4.1 -> v3.5.0

### References

- 토론: `_sdd/discussion/discussion_autopilot_reasoning_harness.md`

## 2026-03-17 - Codex Autopilot Parity Restoration and Validation Guide Consolidation

### Context

Codex custom agent backbone과 `sdd-autopilot` 구조는 도입되었지만, Codex 쪽 autopilot 문서 세트가 Claude 원본보다 과도하게 축약되어 있었다. 특히 main skill, scale assessment, pipeline templates, sample orchestrator에서 review-fix, test strategy, error handling, final report artifact 같은 실행 계약이 충분히 드러나지 않았다. 또한 Codex dry-run 체크리스트가 `docs/CODEX_AGENT_VALIDATION.md`로 분리되어 있어 운영 가이드와 검증 가이드가 분산되어 있었다.

### Decision

1. **Codex autopilot parity 복원**: `.codex/skills/sdd-autopilot/`의 main skill, references, example을 Claude 원본 대비 의미 보존 수준으로 확장
2. **Final report artifact 명시**: Codex autopilot 산출물 계약에 `_sdd/pipeline/report_<topic>_<timestamp>.md`를 포함
3. **Validation guide 통합**: Codex dry-run 체크리스트를 `docs/AUTOPILOT_GUIDE.md`의 "Codex 검증 체크리스트" 섹션으로 흡수하고 별도 `docs/CODEX_AGENT_VALIDATION.md`는 제거
4. **Spec sync**: `_sdd/spec/main.md`에서도 Codex wrapper -> custom agent 실행 모델, autopilot report artifact, validation guide 위치를 최신 상태로 반영

### Rationale

- Codex 쪽도 실행 계약이 충분히 구체적이어야 generated orchestrator 품질과 운영 가이드를 신뢰할 수 있다
- final report artifact가 문서/예시/가이드에 모두 명시돼야 autopilot completion contract가 일관된다
- validation 체크리스트는 사용자-facing 운영 가이드 안에 있을 때 찾기 쉽고 유지보수 포인트가 줄어든다

### Changes

- `.codex/skills/sdd-autopilot/SKILL.md` -- use/do-not-use, richer execution/test/error handling, final report contract 복원
- `.codex/skills/sdd-autopilot/references/pipeline-templates.md` -- generated orchestrator minimum contract 복원
- `.codex/skills/sdd-autopilot/references/scale-assessment.md` -- 판단 프로세스, 경계 사례, examples 복원
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- review-fix, test, error handling, final report 예시 복원
- `docs/AUTOPILOT_GUIDE.md` -- Codex 검증 체크리스트 섹션 추가, validation guide 흡수
- `_sdd/spec/main.md` -- Codex wrapper/custom-agent 실행 모델, final report artifact, validation guide 위치 동기화

### References

- 드래프트: `_sdd/drafts/feature_draft_autopilot_parity_review.md`
- 드래프트: `_sdd/drafts/feature_draft_codex_agent_backbone_autopilot_parity.md`
- 구현 리포트: `_sdd/implementation/features/autopilot-parity-review/SYNC_20260317_230000_IMPLEMENTATION_REPORT.md`

## 2026-03-17 - Codex Custom Agent Backbone and Autopilot Spawn Model

### Context

초기 Codex 정렬 작업으로 `sdd-autopilot`, generated orchestration skill, `write-phased` utility 설명은 추가되었지만, 실제로 generated orchestrator가 spawn할 repo-local custom agent 레이어가 없었다. 이 상태에서는 "오케스트레이터가 실행 단위를 재사용한다"는 설명은 가능했지만, Claude Code의 `wrapper -> agent -> nested write-phased` 구조와 동등한 실행 backbone은 비어 있었다.

### Decision

1. **Codex custom agent layer 도입**: `.codex/agents/` 아래에 기존 SDD 핵심 역할 8개와 `write_phased`를 custom agent로 정의
2. **wrapper parity 채택**: `.codex/skills/*/SKILL.md`는 사용자 진입점과 handoff contract를 유지하고, 실제 spawned execution unit은 `.codex/agents/*.toml`이 담당
3. **Autopilot spawn 모델 명시**: generated orchestration skill은 skill이 아니라 custom agent를 직접 spawn
4. **nested `write_phased` 1차 범위 확정**: `feature_draft`, `implementation_plan`, `implementation_review`, `spec_review`가 장문 산출물 생성 시 `write_phased`를 nested 사용
5. **Pre-flight 확장**: `_sdd/env.md`와 `.codex/config.toml`을 함께 읽고, 최소 `agents.max_depth >= 2`를 확인

### Rationale

- custom agent 레이어가 있어야 Codex autopilot이 실제로 end-to-end 파이프라인을 실행할 수 있다
- wrapper skill을 유지해야 기존 사용자 호출 인터페이스를 깨지 않으면서 agent spawn 모델을 도입할 수 있다
- planning/review 계열은 long-form writing 품질 이득이 커서 nested `write_phased`의 우선 대상이다
- config 기반 pre-flight가 없으면 nested spawn 구조가 환경에 따라 조용히 실패할 수 있다

### Changes

- `.codex/config.toml` -- agent execution config 신규 추가
- `.codex/agents/` -- 9개 custom agent 정의 신규 추가
- `.codex/skills/feature-draft/`, `.codex/skills/implementation-plan/`, `.codex/skills/implementation/`, `.codex/skills/implementation-review/`, `.codex/skills/spec-update-done/`, `.codex/skills/spec-update-todo/`, `.codex/skills/spec-review/`, `.codex/skills/ralph-loop-init/`, `.codex/skills/write-phased/` -- wrapper/custom-agent parity 반영
- `.codex/skills/sdd-autopilot/` -- custom agent spawn 모델과 pre-flight 반영
- `_sdd/spec/main.md`, `docs/AUTOPILOT_GUIDE.md`, `docs/SDD_QUICK_START.md`, `docs/SDD_WORKFLOW.md` -- custom agent 구조 반영

### References

- 드래프트: `_sdd/drafts/feature_draft_codex_agent_backbone_autopilot_parity.md`
- 드래프트: `_sdd/drafts/feature_draft_autopilot_meta_skill.md`
- 토론: `_sdd/discussion/discussion_autopilot_meta_skill.md`
- 토론: `_sdd/discussion/discussion_write_phased_skill_design.md`

## 2026-03-17 - Codex Autopilot Orchestration and Write-Phased Utility Alignment

### Context

Claude Code용 autopilot 메타스킬과 래퍼/에이전트 구조는 이미 정리되어 있었지만, Codex 쪽에는 대응되는 `sdd-autopilot` 메타스킬과 orchestration contract가 없었다. 또한 `write-phased`는 Claude에서는 에이전트 중심 전략으로 쓰였지만, Codex에서는 공용 long-form writing utility로 어떤 스킬들이 활용해야 하는지 명확히 정리되지 않았다.

### Decision

1. **Codex `sdd-autopilot` 지원 추가**: `.codex/skills/sdd-autopilot/`를 추가하여 기존 execution skill들을 재사용하는 generated orchestration skill 패턴을 지원
2. **오케스트레이터 라이프사이클 하이브리드 정책**: 실행 중에는 `.codex/skills/orchestrator_<topic>/SKILL.md`에 활성 상태로 유지하고, 완료 후에는 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`로 아카이브
3. **Codex binding 책임 분리**: repo는 wrapper/orchestration contract만 정의하고, 실제 wrapper/agent binding은 Codex 런타임/환경 레이어 책임으로 둔다
4. **`write-phased` 승격**: Codex `write-phased`를 `spec-create`, `guide-create`, `pr-spec-patch`, `pr-review`, `spec-summary`, `spec-upgrade`, `sdd-autopilot`이 재사용하는 공용 long-form writing utility로 정의
5. **범위 제한**: `feature-draft -> write-phased` 직접 연동은 후속 최적화로 미루고 이번 결정 범위에서는 제외 **> Superseded by 2026-03-17 custom agent backbone decision: nested write_phased parity를 1차 범위에 포함**

### Rationale

- 기존에 정의한 SDD execution unit들을 유지하면서 Codex에서도 autopilot 메타스킬을 도입하는 편이 가장 낮은 전환 비용으로 구조적 일관성을 확보한다
- 활성 스킬 디렉토리와 아카이브 디렉토리를 분리하면 resume 가능성과 active skill 공간 관리 사이의 균형을 맞출 수 있다
- Codex는 Claude와 다른 orchestration/runtime 모델을 가지므로, repo-local binding까지 고정하는 것보다 contract만 명세하는 편이 유지보수성이 높다
- 긴 문서/대형 코드 출력은 write-phased의 skeleton → fill 전략을 공용 유틸리티로 재사용하는 것이 품질과 안정성에 유리하다

### Changes

- `.codex/skills/sdd-autopilot/` -- 메타스킬 신규 추가
- `.codex/skills/write-phased/` -- 공용 long-form writing utility로 역할 재정의
- `.codex/skills/feature-draft/`, `.codex/skills/implementation-plan/`, `.codex/skills/implementation/`, `.codex/skills/implementation-review/`, `.codex/skills/spec-update-done/`, `.codex/skills/spec-update-todo/`, `.codex/skills/spec-review/`, `.codex/skills/ralph-loop-init/` -- orchestration mode guidance 추가
- `.codex/skills/spec-create/`, `.codex/skills/guide-create/`, `.codex/skills/pr-spec-patch/`, `.codex/skills/pr-review/`, `.codex/skills/spec-summary/`, `.codex/skills/spec-upgrade/` -- long-form writing strategy 반영
- `docs/AUTOPILOT_GUIDE.md`, `docs/SDD_WORKFLOW.md`, `docs/SDD_QUICK_START.md`, `_sdd/spec/main.md` -- Codex autopilot/orchestrator/write-phased 설명 동기화

### References

- 드래프트: `_sdd/drafts/feature_draft_codex_autopilot_orchestration.md`
- 토론: `_sdd/discussion/discussion_autopilot_meta_skill.md`
- 토론: `_sdd/discussion/discussion_autopilot_open_questions.md`
- 토론: `_sdd/discussion/discussion_autopilot_resume_and_partial_execution.md`

## 2026-03-09 - Exploration-first spec adopted for the SDD skills repo

### Context

이 저장소는 스킬 프롬프트와 문서를 다루기 때문에, 코드 설명서보다 "어디를 보고 무엇을 함께 바꿔야 하는지"가 더 중요하다.

### Decision

이 저장소의 스펙도 일반 코드베이스와 같은 탐색형 기준을 적용한다. 메인 문서는 entry point 역할을 하고, 상세는 그룹 스펙으로 분리한다.

### Rationale

스킬 간 계약, 앵커 섹션, spec sync 분류 같은 공통 규칙은 코드보다 문서 사이의 연결을 더 잘 보여줘야 안전하게 바뀔 수 있다.

## 2026-03-09 - Grouped component specs preferred over per-skill specs

### Context

`.codex/skills/`에는 13개의 Codex 스킬이 있고, 이를 곧바로 13개 컴포넌트 스펙으로 쪼개면 메인 스펙보다 탐색 비용이 커질 수 있다.

### Decision

초기 스펙은 `spec lifecycle`, `implementation lifecycle`, `PR lifecycle`의 3개 그룹 스펙으로 시작한다.

### Rationale

이 저장소의 핵심 변경 축은 개별 스킬보다 "workflow group" 단위로 움직이는 경우가 많다. 그룹 스펙이 현재 탐색성과 유지보수성의 균형이 더 좋다.

## 2026-03-09 - Codex skill tree treated as the primary spec target

### Context

최근 정렬 작업과 버전 보강은 `.codex/skills/`를 기준으로 진행되었고, `.claude/skills/`는 평행 구조이지만 완전 동기화 기준은 아직 문서로 확정되지 않았다.

### Decision

현재 저장소 스펙은 `.codex/skills/`를 주 기준으로 설명하고, `.claude/skills/`는 배포/변형 레이어로 다룬다.

### Rationale

현재 실제 정렬 작업과 품질 기준이 Codex 쪽에 집중되어 있으므로, 메인 스펙의 기준선도 여기에 두는 편이 더 명확하다. 플랫폼 parity의 범위는 `Open Questions`로 남긴다.

> **⚠️ Superseded by 2026-03-13 decision below**

## 2026-03-13 - Platform primary target reassessment (.claude/ as source of truth)

### Context

2026-03-09 결정에서 `.codex/skills/`를 주 기준으로 설정했으나, 이후 모든 스킬 변경이 양 플랫폼 동시 적용되고 Claude Code가 더 많은 스킬을 보유(19 vs 17)하게 되었다. 스펙 자체도 `.claude/` 경로를 기준으로 기술하고 있어 실제 운영과 이전 결정이 불일치.

### Decision

`.claude/skills/`를 원본(source of truth)으로, `.codex/skills/`를 파생본으로 정의한다. 동기화 방향은 `.claude/` → `.codex/`.

### Rationale

Claude Code가 기능 상위 집합(19개 vs 17개)이고, Claude Code 전용 스킬(git, sdd-upgrade, discussion)이 존재하며, 스펙과 커밋 히스토리 모두 `.claude/` 기준으로 운영되고 있다.

## 2026-03-13 - Spec Upgrade to Whitepaper Format (v1.1.0 → v2.0.0)

### Context

기존 스펙(`main.md` v1.1.0, 598줄)이 whitepaper §1-§8 구조에 근접했으나 완전히 준수하지 않았다. 서사 섹션(§1 Background & Motivation, §2 Core Design)이 부족하고, 컴포넌트별 Why/Source 필드가 없었으며, Code Reference Index가 없었다.

### Decision

- 기존 멀티파일 구조(main.md + 3 서브 스펙)에서 단일 파일 구조로 이미 통합된 상태를 유지
- 기존 내용을 §1-§8에 재배치: 목표→§1, 공통 패턴→§2, 워크플로우/아티팩트 맵→§3, 플랫폼 차이/설치→§8
- 모든 16개 컴포넌트에 Why와 Source 필드 추가
- Code Reference Index 부록 신규 생성 (16개 SKILL.md 파일 매핑)
- 2-Phase Generation 패턴을 §2 Core Design에 추가 (신규 도입된 패턴)
- 스킬 수 14→16 업데이트 (spec-upgrade, guide-create 반영)

### Rationale

SDD_SPEC_DEFINITION.md 기준 whitepaper 형식 준수. spec-upgrade 스킬의 2-phase 전략 적용 (598줄 >= 300줄 threshold). 기존 내용 최대 보존 원칙에 따라 삭제 없이 재배치.

### Changes

- `_sdd/spec/main.md` — v1.1.0 → v2.0.0 (598줄 → 672줄)
- `_sdd/spec/prev/PREV_sdd_skills_20260313_120859.md` — 백업 생성

## 2026-03-16 - Dual Architecture: Skill + Agent Layer (v2.1.0 → v3.0.0)

### Context

기존 SDD Skills는 스킬 전용(skills-only) 아키텍처로, 20개 스킬이 `.claude/skills/*/SKILL.md`에 전체 로직을 포함하고 있었다. 사용자가 대규모 기능을 구현하려면 6-7개 스킬을 수동으로 순서대로 호출해야 하며, 중간에 맥락이 유실되거나 단계를 빠뜨릴 위험이 있었다. `write-phased` 에이전트가 `tools: ["Agent"]`로 서브에이전트 호출이 가능함을 증명하였다.

### Decision

1. **스킬 + 에이전트 이중 아키텍처 도입**: 8개 파이프라인 필수 스킬을 `.claude/agents/*.md` 에이전트 정의로 분리하고, 기존 SKILL.md는 Agent Wrapper 래퍼로 전환
2. **sdd-autopilot 메타스킬 추가**: 적응형 오케스트레이터를 생성하여 에이전트 파이프라인을 end-to-end 자율 실행
3. **오케스트레이터 저장 위치**: `_sdd/pipeline/`에 저장 (초기 토론에서 `.claude/skills/`로 결정했으나, 후속 토론에서 변경 — 일회성 실행 계획이므로 스킬 디렉토리 오염 방지) **> Superseded by 2026-03-17 decision: `.claude/skills/orchestrator_<topic>/SKILL.md`로 원복 (재사용성 + 재개 기능)**
4. **Codex는 기존 유지**: Agent 도구 제한으로 래퍼 패턴 불가. Codex 동기화는 별도 후속 작업 **> Superseded by 2026-03-17 decision: Codex `sdd-autopilot` + orchestration contract 지원 추가**

### Rationale

- 사용자 인터페이스(`/스킬명`) 하위 호환성 유지가 필수 → 래퍼 스킬 유지
- sdd-autopilot의 서브에이전트 호출을 위해 에이전트 레이어 필요 → Agent Wrapper 패턴
- 선행 집중형 사용자 인터랙션(Phase 1 interactive, Phase 2 autonomous) → 2-Phase Orchestration 패턴
- Discussion은 AskUserQuestion이 핵심이므로 에이전트 전환 불필요 → 스킬 유지

### Changes

- `_sdd/spec/main.md` — v2.1.0 → v3.0.0
- `.claude/agents/` — 8개 에이전트 정의 신규 생성
- `.claude/skills/*/SKILL.md` — 8개 래퍼 전환
- `.claude/skills/sdd-autopilot/` — 메타스킬 신규 생성
- `_sdd/spec/prev/PREV_main_20260316_120000.md` — 백업 생성

### References

- 토론: `_sdd/discussion/discussion_autopilot_meta_skill.md`
- 후속 토론: `_sdd/discussion/discussion_autopilot_open_questions.md`
- Feature Draft: `_sdd/drafts/feature_draft_autopilot_meta_skill.md`

## 2026-03-17 - Autopilot Resume, Partial Execution, and Enhanced Pipeline Log (v3.1.0 → v3.2.0)

### Context

sdd-autopilot이 e2e 전제로 설계되어 있어, 기존 미완료 파이프라인 재개, 기존 산출물 활용(중간 진입), 파이프라인 일부만 실행하는 시나리오가 불가능했다. 또한 오케스트레이터가 `_sdd/pipeline/`에 저장되어 스킬로서 재사용이 불가능하고, 파이프라인 로그에 구조화된 상태 추적이 없었다.

### Decision

1. **Step 0 (Pipeline State Detection) 추가**: autopilot 시작 시 `_sdd/pipeline/log_*.md`를 스캔하여 미완료 파이프라인을 감지하고, 사용자에게 재개/새로 시작 선택을 제시
2. **Step 1.4 (산출물 스캔 + 시작점/종료점 감지) 추가**: 사용자 요청에서 시작/종료 힌트를 파싱하고, `_sdd/` 기존 산출물과의 관련성을 판단하여 파이프라인 범위 조절
3. **Pipeline Log Format 강화**: Meta 섹션(request, orchestrator 참조, scale, started, pipeline) + Status 테이블(5개 상태값: pending/in_progress/completed/failed/skipped) 추가
4. **오케스트레이터 저장 위치 변경**: `_sdd/pipeline/` → `.claude/skills/orchestrator_<topic>/SKILL.md` (변경 이력: `.claude/skills/` → `_sdd/pipeline/` → `.claude/skills/`)

### Rationale

- 오케스트레이터를 `.claude/skills/`에 저장하면 스킬로서 재사용 가능하고, 재개 시 파이프라인 정의 역할을 수행할 수 있다
- 로그의 Status 테이블로 재개 시 첫 번째 미완료 스텝을 빠르게 찾을 수 있다
- 산출물 스캔으로 기존 작업 결과를 활용하여 불필요한 반복을 방지한다
- 자동 감지 + 사용자 선택 방식으로 재개를 구현하여, Phase 1이 이미 interactive이므로 질문 추가 비용이 낮다

### Changes

- `.claude/skills/sdd-autopilot/SKILL.md` -- Step 0, Step 1.4, Pipeline Log Format 강화, 오케스트레이터 경로 변경
- `_sdd/drafts/feature_draft_autopilot_meta_skill.md` -- Acceptance Criteria 추가 (재개, 부분 실행, 산출물 스캔, 로그 메타데이터)
- `_sdd/spec/main.md` -- v3.1.0 → v3.2.0

### References

- 토론: `_sdd/discussion/discussion_autopilot_resume_and_partial_execution.md`
- 후속 반영: `_sdd/discussion/discussion_autopilot_open_questions.md` (오케스트레이터 위치 결정 변경)

## 2026-03-17 - Agent Non-Interactive Conversion (AskUserQuestion 제거) (v3.0.0 → v3.1.0)

### Context

v3.0에서 8개 스킬을 에이전트로 전환했으나, 에이전트 정의 내에 AskUserQuestion 호출이 남아 있었다. sdd-autopilot의 Phase 2에서 서브에이전트로 호출할 때 사용자 인터랙션이 발생하면 파이프라인이 중단되어 자율 실행이 불가능했다.

### Decision

8개 파이프라인 에이전트(feature-draft, implementation-plan, implementation, implementation-review, ralph-loop-init, spec-review, spec-update-done, spec-update-todo)에서 AskUserQuestion을 완전 제거하고, **Autonomous Decision-Making 패턴**으로 대체한다.

### Rationale

- 서브에이전트는 부모 에이전트(sdd-autopilot)의 컨텍스트 내에서 실행되며, 사용자와 직접 인터랙션할 수 없다
- 모호한 상황에서는 가용 정보로 최선 추론 → 판단 근거를 출력에 기록 → 추론 불가 항목은 Open Questions에 남기는 3단계 전략 적용
- discussion, sdd-autopilot은 풀 스킬이므로 AskUserQuestion 유지 (사용자 인터랙션이 핵심 기능)
- 래퍼 스킬 경유 호출 시에도 에이전트가 non-interactive로 동작하지만, 부모 세션에서 사용자가 결과를 확인할 수 있으므로 문제 없음

### Changes

- `.claude/agents/feature-draft.md` -- AskUserQuestion → 자율 판단 로직
- `.claude/agents/implementation-plan.md` -- AskUserQuestion → 자율 판단 로직
- `.claude/agents/implementation-review.md` -- Tools에서 AskUserQuestion 제거
- `.claude/agents/ralph-loop-init.md` -- AskUserQuestion → 자동 선택/오류 보고
- `.claude/agents/spec-review.md` -- Tools에서 AskUserQuestion 제거
- `.claude/agents/spec-update-done.md` -- AskUserQuestion → 자동 선택/Quick Sync 전환
- `.claude-plugin/marketplace.json` -- sdd-autopilot 스킬 + 8개 에이전트 등록
- `_sdd/spec/main.md` -- v3.0.0 → v3.1.0

## 2026-03-17 - Mandatory Review-Fix Cycle (Hard Rule #9) (v3.2.0 → v3.3.0)

### Context

sdd-autopilot의 review-fix 루프가 선택적으로 동작하여, 리뷰만 실행하고 수정 없이 파이프라인이 종료되는 경우가 발생할 수 있었다. 특히 부분 파이프라인("리뷰만 해줘")이나 재개 시나리오에서 review → fix → re-review 사이클이 보장되지 않았다. 또한 `implementation-review`가 비핵심 단계로 분류되어 있어, 리뷰 실패 시 건너뛸 수 있었다.

### Decision

1. **Hard Rule #9 (Review-Fix 사이클 필수)**: 파이프라인에 review 단계가 포함되면 review → fix → re-review 사이클을 필수 실행. 전체/부분/재개 파이프라인 모두 적용
2. **implementation-review 조건부 핵심 단계 승격**: review가 포함된 파이프라인에서 `implementation-review`는 핵심 단계로 취급하며, 실패 시 건너뛸 수 없음 (최대 3회 재시도 후 실패 시 파이프라인 중단)

### Rationale

- 리뷰 없이 수정을 건너뛰면 발견된 이슈가 방치되어 품질 리스크가 누적된다
- 부분 파이프라인에서도 동일한 품질 기준을 적용하여 일관성 확보
- `implementation-review`가 비핵심이면 리뷰-수정 사이클 자체가 무력화될 수 있다

### Changes

- `.claude/skills/sdd-autopilot/SKILL.md` -- Hard Rule #9 추가, Review-Fix 루프 필수 사이클 강화, implementation-review 조건부 핵심 단계
- `.claude/skills/sdd-autopilot/references/pipeline-templates.md` -- 모든 템플릿에 Hard Rule #9 적용, 핵심 단계에 implementation-review 추가
- `_sdd/spec/main.md` -- v3.2.0 → v3.3.0
