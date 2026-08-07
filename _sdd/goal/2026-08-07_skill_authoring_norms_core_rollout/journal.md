# Journal (append-only)

## 2026-08-07 Goal init
- 가설: 2단계 전수 범위와 우선순위별 커밋 완료 경계로 evaluator-first 하네스를 구성할 수 있다.
- 검증: 완료조건 self-check → transcript-only 판정 `PASS`, evidence 매 턴 surface `PASS`, 문자열 길이 `2,593/4,000`자 `PASS`
- 결과: 통과
- 다음: 기존 `autopilot-simplicity-diet` draft의 `plan-review`부터 P0 세로 슬라이스를 재개한다.

## 2026-08-07 P0 첫 feature plan-review
- 가설: P0를 component별 세로 슬라이스로 닫으면 mirror 전파와 runtime delta를 한 owner task에서 검증할 수 있다.
- 검증: `plan-review` 실측∥판단 2-렌즈 → `BLOCKED`, 합산 `C0 H3 M0`; fix 후 Propagation discovery가 autopilot 2경로·simplicity agent 2경로를 정확히 출력하고 `git diff --check` 통과
- 결과: 부분 — Propagation 누락, Claude tools 전제의 Codex 오적용, 비실행형 AC를 draft fix 1회로 반영했다. 판단 렌즈의 규모·5-smell은 전부 PASS. `H3`이므로 추가 plan-review 1회 권고 advisory를 보존하되 자동 재리뷰는 하지 않는다.
- 다음: 롤링 분할 목록을 planned spec-sync로 고정한 뒤 첫 feature 구현을 시작한다.

## 2026-08-07 P0 autopilot-simplicity 구현·게이트
- 가설: component별 Claude/Codex task와 runtime별 AC로 구현하면 다이어트와 adapter delta 보존을 동시에 닫을 수 있다.
- 검증: T1/T2/T3 structural RED exit 1 → GREEN exit 0, comprehensive AC assertions 전부 PASS, `TOML_OK`; implementation-review correctness 전 AC MET + simplicity `M3`, fix 후 `FIX-M1/2/3 PASS`와 회귀 PASS
- 결과: 통과 — 네 파일 `26 insertions / 72 deletions`의 최소 구현 후 simplicity 중복 M3을 fix 1회로 닫았다. T3 structural check는 최초 범위 오적용 1회를 선언하고 HEAD RE-RED→worktree GREEN으로 재확인했다.
- 다음: post-implementation spec-sync로 P0 1/5만 current truth로 승격하고 report ledger의 두 component를 갱신한다.

## 2026-08-07 P0 1/5 post-sync
- 가설: 세로 슬라이스마다 verified delta만 current truth로 승격하면 나머지 planned todo와 구현 사실을 섞지 않을 수 있다.
- 검증: `main.md` version `4.6.44` == changelog latest `v4.6.44`; decision/changelog diff `+47/-0`, `+10/-0`; main에는 P0 2/5~5/5만 Planned 잔존
- 결과: 통과 — `sdd-autopilot`과 `simplicity-review-agent`를 report에서 `AUDITED / UPDATED`로 닫고 17개 component를 남겼다.
- 다음: P0 2/5 `spec-sync-agent-diet` feature draft부터 다음 세로 슬라이스를 시작한다.

## 2026-08-07 P0 2/5 spec-sync-agent plan-review
- 가설: digest producer/consumer와 세 single-home 규칙을 task별 단일 owner로 분리하면 네 surface 전파를 구현 전에 기계적으로 닫을 수 있다.
- 검증: `plan-review` 실측∥판단 2-렌즈 → fix 전 `C0 H2 M1`; fix 후 propagation P1/P2/P3 단일 owner, digest block exact-once·status/fallback/processed section-scoped AC, `git diff --check` PASS
- 결과: 통과 — 복수 owner와 false-positive 가능한 존재 검사를 제거하고, 전체 Hard Rules로 번지던 AC5를 이번 scope의 현행 Rule 3·5·11로 제한했다. 규모 판정은 적격을 유지했다.
- 다음: `implementation`으로 structural RED를 관찰한 뒤 네 target surface의 최소 변경과 read-only census를 수행한다.

## 2026-08-07 P0 2/5 spec-sync-agent 구현·게이트
- 가설: 상태·legacy·processed 규칙의 canonical section 포인터와 고정 4필드 interface만 남기면 기존 dispatch·routing 의미를 유지하면서 중복을 줄일 수 있다.
- 검증: T1/T2/T3 RED exit 1 → GREEN exit 0, AC1–AC12 MET; correctness 3-shard finding 0, simplicity `M3`; fix 후 old duplicate/undefined token 0, mirror semantics·TOML·`git diff --check` PASS
- 결과: 통과 — 네 target은 `56 insertions / 36 deletions`; fix 1회로 전달 규칙·records 소비 설명의 중복 2건과 정의 없는 lifecycle 축약 1건을 닫았다. T3 검사 경계 오류 1회는 선언 후 HEAD re-RED→worktree GREEN으로 재확인했다.
- 다음: implemented `spec-sync` 본문∥기록 2-shard로 P0 2/5만 current truth에 승격하고 component ledger 2행을 닫는다.

## 2026-08-07 P0 2/5 post-sync
- 가설: 선고정 4필드 digest로 본문∥기록을 분리하면 구현 사실과 append-only history·input processing을 정합하게 닫을 수 있다.
- 검증: `main.md` version `4.6.45` == changelog latest `v4.6.45`; decision/changelog 누적 diff `+71/-0`, `+15/-0`; P0 3/5~5/5 Planned 유지; processed draft·ledger 경로 존재
- 결과: 통과 — `spec-sync`와 `spec-sync-agent`를 report에서 `AUDITED / UPDATED`로 닫아 전체 4/19, P0 4/12가 완료됐다.
- 다음: P0 3/5 `pr-review-diet`의 독립 feature draft부터 다음 세로 슬라이스를 시작한다.

## 2026-08-07 P0 3/5 pr-review plan-review
- 가설: wrapper 반환 재정의·reviewer read-only 반복을 걷고 dispatch input/UNTESTED 경계를 형식화하면 PR review의 판단 주체를 얇게 만들 수 있다.
- 검증: `plan-review` 실측∥판단 → fix 전 `C0 H3 M2 L1`; fix 후 7필드 interface 6 producer/consumer surface + checklist pointer 2 surface, single owner P1–P6, section-aware AC15–AC17, `git diff --check` PASS
- 결과: 부분 통과 — CI evidence 수집·review state redaction·checklist 전파·simplicity consumer 누락을 fix 1회로 반영했다. `UNTESTED` verdict는 correctness test signal(non-test/N/A 제외)로 닫았다. `H3`이므로 추가 review 1회 권고를 남기되 자동 실행하지 않는다.
- 다음: Task 1–4 structural RED를 관찰하고 8개 target을 최소 수정한다.

## 2026-08-07 P0 3/5 pr-review 구현·게이트
- 가설: wrapper·두 reviewer가 한 7필드 입력 계약을 공유하고 verdict/read-only 판단을 canonical home으로 모으면 기존 두 렌즈 topology를 보존하면서 반복을 줄일 수 있다.
- 검증: T1~T4 RED exit 1 → GREEN exit 0, AC1–AC17 MET; correctness `H1+M1`, simplicity `M2` 중 동일 dispatch 원인을 병합해 aggregate `C0 H1 M2`; fix 후 exact input parity·checklist pointer·TOML 2·normalized core parity·target census·`git diff --check` PASS
- 결과: 통과 — `Signals`가 `UNTESTED: <reason>`을 보존하도록 복구하고, Codex dispatch의 경쟁 field inventory를 canonical pointer로 줄였으며, Fresh Verification을 순차 4단계로 펼쳤다. 첫 post-fix assertion 시도들은 문서 결함이 아니라 검사기의 backtick·heading literal·정규화 공백 가정 오류였고, 구현 변경 없이 검사 계약을 실제 heading/subschema에 맞춘 뒤 AC1–AC17 전체 PASS를 재관찰했다.
- 다음: implemented `spec-sync`로 P0 3/5 verified delta만 current truth에 승격하고 `pr-review`·`pr-review-agent` report 행을 닫는다.

## 2026-08-07 P0 3/5 post-sync
- 가설: 선고정 4필드 digest로 본문∥기록 sync를 분리하면 P0 3/5의 verified delta만 승격하고 나머지 planned 항목과 append-only history를 보존할 수 있다.
- 검증: `main.md` version `4.6.46` == changelog latest `v4.6.46`; decision/changelog 누적 diff `+100/-0`, `+20/-0`; P0 3/5 planned 잔존 0, P0 4/5·5/5 유지; processed draft·ledger 존재; `git diff --check` PASS
- 결과: 통과 — `pr-review`와 `pr-review-agent`를 `AUDITED / UPDATED`로 닫고, P0 1에서 먼저 감사한 `simplicity-review-agent` 행에는 v4.6.46 공통 input consumer 증거를 보강했다. 전체 6/19, P0 6/12 완료다.
- 다음: P0 4/5 `feature-draft-pair-diet`의 feature draft부터 다음 세로 슬라이스를 시작한다.

## 2026-08-07 P0 4/5 feature-draft pair plan-review
- 가설: producer가 template·Propagation·평가 기준을 소유하고 verifier는 이를 읽어 검증하면 single-home과 rich output fidelity를 함께 닫을 수 있다.
- 검증: `plan-review` 실측∥판단 → fix 전 `C0 H2 M1`; 판단 렌즈 규모·5-smell PASS, fix 후 P1–P4 exact path/single owner, six-target clean baseline, explicit 1/2-grade evaluation, `git diff --check` PASS
- 결과: 부분 통과 — 최초의 신규 reference 가설은 “항상 읽는 내용은 분리하지 않는다”는 authoring norm에 반증돼 폐기했다. inline fenced template을 canonical으로 유지하고 verbatim copy만 기계화한다. discovery placeholder·dirty attribution·정규화/보호 의미 판정 gap을 초안 fix 1회로 닫았다.
- 다음: `implementation`으로 Task 1~3 structural RED를 관찰하고 feature-draft SKILL 2면·plan-review-agent 2면만 최소 수정한다. plan-review wrapper 2면은 NO_CHANGE 감사를 수행한다.

## 2026-08-07 P0 4/5 feature-draft pair 구현
- 가설: inline template verbatim 소비와 producer-contract verifier pointer만 추가하면 신규 asset 없이 네 target에서 규범 gap을 닫을 수 있다.
- 검증: T1/T2/T3 RED exit 1 → GREEN; AC1–AC15 structural regression PASS; feature-draft exact mirror; plan-review-agent normalized core parity·TOML; wrapper diff 0; `quick_validate.py` 2면; `git diff --check` PASS
- 결과: 통과 — 네 파일 `+32/-36`, outside target·coverage delta 0. 검사 계약 이탈 3건은 각각 원장에 기록하고 구현 변경 없이 corrected HEAD RED를 재관찰했다. plan-review wrapper는 예상대로 thin entrypoint라 NO_CHANGE 후보로 남았다.
- 다음: implementation-review correctness Task 1~3 + simplicity reference/local gate를 실행하고 C/H/M을 fix 1회로 닫는다.

## 2026-08-07 P0 4/5 feature-draft pair review gate
- 가설: producer/verifier single-home 구현이 correctness와 simplicity 두 관점에서도 실행 가능한 최소 계약으로 닫힌다.
- 검증: correctness T1 `C1`, T2/T3 finding 0; simplicity reference PASS, local `M2`; aggregate `C1 H0 M2`; fix 후 `FIX_C1_M1_T1_PASS`, `FIX_M2_T2_PASS`, AC1–AC15·mirror/core/TOML·wrapper diff0·validator2·diff-check PASS
- 결과: 통과 — slot-only 계약이 variable-cardinality draft를 만들 수 없다는 Critical을 받아 verbatim base + 명시된 row/block 반복으로 정정했다. 질문/template/evaluation과 producer-source fallback은 단계형으로 펼쳤다. 잔존 C/H/M 0, coverage delta 0.
- 다음: v4.6.47 implemented spec-sync로 P0 4/5를 current truth로 승격하고 feature-draft·plan-review-agent는 UPDATED, plan-review wrapper는 NO_CHANGE로 report를 닫는다.

## 2026-08-07 P0 4/5 post-sync
- 가설: verified producer·verifier delta만 승격하면 inline template 정본과 thin wrapper의 NO_CHANGE 판정을 planned P0 5/5와 섞지 않고 기록할 수 있다.
- 검증: `main.md` version `4.6.47` == changelog latest `v4.6.47`; decision/changelog 누적 diff `+128/-0`, `+25/-0`; P0 4/5 planned 잔존 0, P0 5/5 유지; processed draft·ledger 존재; `git diff --check` PASS
- 결과: 통과 — `feature-draft`와 `plan-review-agent`를 `AUDITED / UPDATED`, `plan-review`를 `AUDITED / NO_CHANGE`로 닫았다. 전체 9/19, P0 9/12 완료다.
- 다음: P0 5/5 `implementation-pair-diet`의 독립 feature draft부터 마지막 P0 세로 슬라이스를 시작한다.

## 2026-08-07 P0 5/5 implementation pair plan-review
- 가설: fix 정책 owner·split pointer·implementation notes·review-only 경계를 한 수정 task와 마지막 read-only census로 닫으면 여섯 runtime surface를 작은 단위로 다이어트할 수 있다.
- 검증: `plan-review` 실측∥판단 2-렌즈 → fix 전 `C0 H4 M2`; 판단 렌즈는 census task 부재·single-task 결정 근거·AC13 모호성을, 실측 렌즈는 validator 비호환·six-path 증명 실패·section/normalization/Source Pointer 검증 gap을 검출. fix 후 Task 1 수정 + Task 2 read-only census, exact command/count·baseline set difference·deterministic normalization·runtime별 validation으로 교정했고 `git diff --check` PASS
- 결과: 통과 — 여섯 파일 규모는 단일 컨텍스트 적격이다. `implementation`을 fix 정책 owner로 두는 이유와 대안 기각·확신도·사용자 확인 필요 여부를 기록했다. review 전 target phrase baseline은 여섯 파일 각 1건이고 target diff는 0이다. fix 전 H4이므로 추가 `plan-review` 1회 권고를 advisory로 남기되 단일 패스 계약상 자동 재리뷰하지 않는다.
- 다음: Task 1·2를 structural RED→GREEN으로 실행하고 implementation-review gate에서 correctness와 simplicity를 검증한다.

## 2026-08-07 P0 5/5 implementation pair 구현·게이트
- 가설: fix 정책·split·ledger·review-only ownership을 가장 가까운 소비 지점 한 곳에 두면 기존 RED→GREEN·2-lens reviewer 계약을 보존하면서 반복을 줄일 수 있다.
- 검증: T1 대표 check 5개 RED exit 1, T2 target-set RED empty → AC1–AC15 GREEN; implementation-review correctness 2 shard + simplicity 2묶음 aggregate `C0 H0 M8`, unique 7. fix 후 `POST_FIX_AC1_12_PASS`, validators·frontmatter·mirror/core/TOML/Source/runtime/status/diff PASS
- 결과: 통과 — 여섯 파일 `+41/-29`. boundary ownership 중복 2건·dense 문장 3건·Fresh Verification 재천명·Codex no-spawn 충돌을 fix 1회로 닫아 잔존 C/H/M 0, coverage delta 0. runtime child 상한 때문에 reviewer 동시 4개를 3+1로 수거한 이탈을 새 `계획 이탈·발견` field에 이유·처리와 함께 기록했다.
- 다음: v4.6.48 implemented spec-sync로 P0 5/5 current truth와 세 component report 행을 닫고 P0 commit 전수 게이트로 간다.

## 2026-08-07 P0 5/5 post-sync
- 가설: 본문∥기록 writer 분할로 마지막 P0 delta만 승격하면 5개 feature의 planned 기록과 current truth를 혼동 없이 종결할 수 있다.
- 검증: `main.md` version `4.6.48` == changelog latest `v4.6.48`; decision/changelog 누적 diff `+155/-0`, `+30/-0`; current main의 P0 planned 0; processed draft·ledger 존재; `git diff --check` PASS
- 결과: 통과 — `implementation`·`implementation-review`·`implementation-review-agent`를 `AUDITED / UPDATED`로 닫아 P0 12/12, 전체 12/19 완료다. P0 5개 feature는 v4.6.44~v4.6.48에 순차 승격됐다.
- 다음: P0 전수 mirror/TOML/frontmatter/spec/worklog gate 후 `norms-p0` commit을 만든다.

## 2026-08-07 P0 priority commit
- 가설: 다섯 세로 슬라이스를 priority boundary 하나로 commit하면 P1/P2 변경과 bisect 가능한 경계를 만들 수 있다.
- 검증: staged 38 files, cached diff check PASS; commit subject `refactor(norms-p0): align core SDD skill contracts`
- 결과: 통과 — commit `e42faa3`. push/PR 없음.
- 다음: P1 네 spec lifecycle skill을 norms rubric으로 횡단 감사한다.

## 2026-08-07 P1 spec lifecycle 횡단 감사
- 가설: P1 네 skill의 본문·reference·example·Claude/Codex mirror를 함께 census하면 개별 skill 리뷰가 놓치는 progressive disclosure와 temporary-spec producer drift를 찾을 수 있다.
- 검증: Claude/Codex SKILL 네 쌍 exact match; `spec-create/spec-review/spec-rewrite/spec-upgrade` 각 385/217/145/216줄. `spec-create`·`spec-upgrade` hook/JSON/trust 관련 42건, 세 skill의 reference load timing 누락, `spec-rewrite`·`spec-upgrade`의 legacy 7-section temporary-spec 형식을 확인했다.
- 결과: 지지 — P1을 `spec-bootstrap-disclosure`(create/upgrade)와 `spec-quality-interface`(review/rewrite) 두 feature로 분리한다. hook 설치 상세는 조건부 rich reference 한 곳에서 소비하고, quality pair는 기준·enum·reference load interface와 현재 Part 1/Part 2 temporary-spec 계약을 맞춘다.
- 다음: 롤링 feature draft의 Part 1에 두 feature를 고정하고 Part 2에는 첫 feature만 상세화해 plan-review를 실행한다.

## 2026-08-07 P1 1/2 bootstrap disclosure plan-review
- 가설: hook 상세만 current feature에 두고 quality/load interface를 planned feature로 격리하면 8개 target의 단일 홈 이동을 한 컨텍스트에서 닫을 수 있다.
- 검증: `plan-review` 판단∥실측 2-렌즈. 원시 합산 `C0 H6 M9`(stale `spec-format`·Source pointer·중복 gate 중복 포함), 고유 `C0 H4 M8`. stale reference 선로드, template 선택 기준 부재, 존재하지 않는 Source pointer, untracked 누락을 High로 검출했다.
- 결과: 통과 — 한 batch에서 current scope를 hook extraction으로 축소하고, Step뿐 아니라 Validation/Output 상세도 이동 대상으로 고정했다. authoring canonical 1개+distribution mirror 3개, preservation matrix, 실제 heading, tracked+untracked 합집합, 28 protected asset manifest, 재현 가능한 validator command로 교정했다. 수정 후 author self-check에서 잔존 C/H/M 0, `git diff --check` PASS. 단일 패스 계약상 자동 재리뷰하지 않는다.
- 다음: rolling Part 1의 두 feature를 planned spec-sync로 고정한 뒤 current Task 1·2를 구현한다.

## 2026-08-07 P1 rolling planned sync
- 가설: 두 feature를 별도 planned todo로만 고정하면 current implementation과 후속 quality-interface의 stale reference 교정을 섞지 않을 수 있다.
- 검증: v4.6.49 main/changelog version 일치; main은 version 1줄 + planned 2줄, decision/changelog append-only `+24/-0`·`+5/-0`; target skill diff·new reference·implementation evidence 0; draft 원경로만 존재; `git diff --check` PASS.
- 결과: 통과 — `spec-bootstrap-disclosure`와 `spec-quality-interface`를 각각 `PLANNED / NOT_IMPLEMENTED`로 고정했다. components·usage는 Repo-wide Invariant Test를 통과하지 않아 무변경이다.
- 다음: current feature의 structural RED를 기록하고 8 target을 구현한다.

## 2026-08-07 P1 1/2 bootstrap disclosure 구현
- 가설: hook 실행 상세를 조건부 rich reference로 이동하고 SKILL에 trigger·upgrade repair owner·pointer만 남기면 hard contract를 잃지 않고 기본 context를 줄일 수 있다.
- 검증: RED new reference `0/4`, embedded detail 8건 → GREEN refs 4-way exact, required heading 7/case 4/JSON 2, target union 8, validator 4/4, protected manifest 28 mismatch 0, allowed-diff-only 4, `git diff --check` PASS.
- 결과: 지지 — SKILL 4면은 `+48/-250`(net -202), 조건부 reference는 171줄×4 exact mirror다. authoring canonical 1개와 distribution mirror 3개를 유지하고 hook script/template/harness 28개는 무변경이다.
- 다음: implementation-review correctness 2 + simplicity 2 gate에서 criterion loss와 과잉압축을 검증한다.

## 2026-08-07 P1 1/2 bootstrap disclosure implementation-review
- 가설: reference 구조와 local pointer를 correctness·simplicity로 분리 검토하면 구조 검사가 놓친 의미 손실과 압축 품질을 찾을 수 있다.
- 검증: aggregate `C0 H2 M5`; watchdog original-result/additional-context와 unsupported-version no-error 기준 손실 H2, preservation matrix M1, 본문·reference 중복 M2, mixed/report 과잉압축 M2. fix 1회 후 structural/mirror/validator/allowed-diff/target/protected/diff regression 전부 PASS.
- 결과: 지지 — H2 문장을 복원하고 M5를 single-home·구조형 reference로 정리했다. review가 새로 찾은 top-level AC/Hard Rule pointer 표면은 ledger에 계획 이탈 1건으로 기록하고 draft 허용 surface를 정정했다. 잔존 C/H/M 0.
- 다음: v4.6.50 implemented spec-sync로 P1 1/2만 current truth로 승격하고 P1 2/2 planned를 유지한다.

## 2026-08-07 P1 1/2 bootstrap disclosure post-sync
- 가설: verified hook extraction만 승격하고 quality interface todo를 유지하면 구현 사실과 후속 load-interface 계획이 섞이지 않는다.
- 검증: main/changelog/decision v4.6.50 일치; P1 1/2 current main 잔존 0, P1 2/2 planned 1; body `+9/-6`, records v4.6.49 포함 누적 decision/changelog `+50/-0`·`+10/-0`; processed draft·ledger 2개; `git diff --check` PASS.
- 결과: 통과 — main/components가 hook reference authoring canonical과 package-local mirror/repair ownership을 current truth로 반영했다. usage-guide는 scenario drift가 없어 무변경이다.
- 다음: P1 2/2를 review criterion, rewrite reference, template load의 세 독립 slice로 롤링 분할한다.

## 2026-08-07 P1 2/2a spec-review interface plan-review
- 가설: 기존 metric 3종을 더 정교하게 만들기보다 spec disposition에 직접 쓰이는 status/decision만 ordered routing으로 남기면 작은 deterministic interface가 된다.
- 검증: plan-review 실측∥판단 2-렌즈 원시 `C0 H6 M2`, 중복 정규화 `C0 H5 M1`. decision gap/overlap, report path 오측정, Drift Summary consumer 부재, metric 재현성·의식, AC 실행방법 부재를 검출했다.
- 결과: 통과 — metric 3종과 고정 output table을 제거하고 code analysis를 finding-linked optional evidence로 축소했다. status는 evidence sufficiency→absence→comparison 순서, decision은 material uncertainty→verified spec change→no spec change 순서로 고정했다. Output Drift Summary 4필드와 exact routing 반례, unique path value/occurrence 2, baseline/validator/normalization command를 추가했다. 수정 후 잔존 C/H/M 0, `git diff --check` PASS.
- 다음: umbrella planned todo를 review/rewrite/template 세 slice로 교체 고정하는 planned spec-sync를 실행한다.

## 2026-08-07 P1 2/2 umbrella split planned sync
- 가설: quality-interface umbrella를 세 planned item으로 교체하면 각 change element를 독립 full chain으로 닫으면서 global todo 순서를 유지할 수 있다.
- 검증: v4.6.51 main/changelog 일치; umbrella 0, review/rewrite/template planned 각 1; spec-review target diff 0, implementation ledger 0; main `+4/-2`, decision/changelog append-only `+22/-0`·`+5/-0`; draft 원경로 보존; `git diff --check` PASS.
- 결과: 통과 — 세 item 모두 `PLANNED / NOT_IMPLEMENTED`; components/usage는 새 persistent navigation fact가 없어 무변경이다.
- 다음: first slice spec-review의 RED→GREEN 구현과 implementation-review gate를 수행한다.

## 2026-08-07 P1 2/2a spec-review interface 구현
- 가설: status와 decision의 판정 축을 ordered criterion으로 고정하고 output이 같은 enum을 직접 소비하면 고정 metric 의식 없이도 review 결과가 결정적이다.
- 검증: RED legacy example/metric 18줄, 새 heading/schema 0 → GREEN section-aware routing·output·forbidden assertion PASS; baseline `e42faa3` 허용 블록 밖 diff 0; Claude/Codex exact; validator 2/2; report path 2건/file; scoped two-path M; `git diff --check` PASS.
- 결과: 지지 — 두 mirror `+68/-46`. status는 evidence sufficiency→one-side absence→comparison, decision은 uncertainty→verified spec change→otherwise 순서로 고정했다. fixed metrics는 제거하고 finding-linked optional evidence 4필드만 남겼다.
- 다음: implementation-review correctness·simplicity gate에서 norms §3.1·§3.2·§4와 AC1–AC10을 검증한다.

## 2026-08-07 P1 2/2a spec-review interface implementation-review
- 가설: correctness 2개와 simplicity 2개를 분리하면 판정 완전성과 norms single-home 회귀를 독립적으로 검출할 수 있다.
- 검증: correctness 두 shard `C0 H0 M0`, AC1–AC10·norms §3.1/§3.2/§4 MET. simplicity 두 shard raw `C0 H0 M2`, 동일 중복을 정규화해 unique `C0 H0 M1`. fix 후 single-home assertion·baseline normalization·mirror·validator 2/2·target set·report path·diff PASS.
- 결과: 지지 — Process는 status/decision criterion, Output은 shape만 소유하도록 enum example row·direction·analysis field 중복을 제거했다. draft AC3·AC4를 pointer 기반 검증으로 교정했으며 잔존 C/H/M 0이다.
- 다음: v4.6.52 implemented spec-sync로 review slice만 current truth로 승격하고 rewrite/template 두 planned item을 유지한다.

## 2026-08-07 P1 2/2a spec-review interface post-sync
- 가설: reviewed status/decision interface만 승격하고 후속 두 slice를 planned로 남기면 구현 evidence와 실행 순서를 섞지 않는다.
- 검증: `P1_REVIEW_SPEC_SYNC_PASS v4.6.52 planned=2 processed=2`; main/changelog version 일치; decision/changelog 누적 diff `+97/-0`·`+20/-0`; completed planned 0, remaining planned 2; processed pair 존재·원본 부재; `git diff --check` PASS.
- 결과: 통과 — main/components에 ordered status·spec disposition·producer pointer·finding-linked optional evidence를 current truth로 반영했다. usage는 scenario/navigation 변화가 없어 무변경이다.
- 다음: 남은 첫 planned item `spec-rewrite-reference-interface`의 rolling feature draft와 plan-review를 시작한다.

## 2026-08-07 P1 2/2b spec-rewrite reference interface plan-review
- 가설: point-of-use load, 세 temporary reference, 두 producer example을 한 interface feature로 닫으면 package-local asset drift를 같은 검증 경계에서 제거할 수 있다.
- 검증: plan-review 판단 렌즈 `C0 H0 M0`, 실측 렌즈 `C0 H3 M2`. propagation query 비재현성, table row를 놓치는 legacy regex, normalization/validator 미고정 H3와 example field 오산·항상-read reference M2를 검출했다. reviewer 장기 실행은 추가 탐색을 중단하고 같은 reviewer follow-up으로 기존 evidence만 회수했다.
- 결과: 통과 — exact path/query/expected count, 형식 무관 legacy 6-name census, pinned interpreter+validator, 12-file normalization, explicit producer fields, conditional rich-reference load로 fix 1회 교정했다. author self-check 잔존 C/H/M 0, tasks 4·AC 16·target clean·`git diff --check` PASS. 단일 패스 계약상 자동 재리뷰하지 않는다.
- 다음: implementation ledger를 만들고 Task 1–4를 structural RED→GREEN으로 실행한다.

## 2026-08-07 P1 2/2b spec-rewrite reference interface 구현
- 가설: 조건부 stage-local pointer와 current producer-shaped rich asset을 함께 반영하면 startup preload 없이 rewrite interface를 완결할 수 있다.
- 검증: RED mapping 0·legacy 24·plan/report heading 4/2 → GREEN mapping·legacy 0·producer fields COMPLETE; parity five exact pairs + template runtime delta 1; validator 2/2; asset path 10/10; allowed diff 12/12; scoped 12 M; `git diff --check` PASS.
- 결과: 지지 — 12파일 `+212/-40`. SKILL은 5 asset의 조건부 소비 시점만 소유하고, 세 reference는 current Part 1/Part 2 shape, examples는 plan/report output shape를 소유한다. 첫 checker 실패는 baseline replacement count 오류로 기록·교정했다.
- 다음: implementation-review 4 task correctness + simplicity 2 gate에서 field 의미와 single-home을 검증한다.

## 2026-08-07 P1 2/2b spec-rewrite reference interface implementation-review
- 가설: task별 correctness 4개와 simplicity 2개를 분리하면 producer drift와 중복 rich asset을 함께 검출할 수 있다.
- 검증: correctness `C0 H4 M2`, simplicity `C0 H0 M6`, raw 합 `C0 H4 M8`, 중복 정규화 `C0 H4 M7`. no-rewrite gap, incomplete/non-verbatim template, Contracts optional drift, extra report metrics H4와 schema/list/example duplication·table·rolling intent M7을 검출했다.
- 결과: 지지 — fix 1회로 feature-draft fenced template exact mirror를 단독 정본으로 두고 format/checklist는 pointer-only로 축소했다. Companion local list와 단일 사용처 example 4개를 제거해 final `+106/-140`; routing·schema·verbatim·deletion·parity·validator·allowed-diff·status·diff PASS, 잔존 C/H/M 0.
- 다음: v4.6.53 implemented spec-sync로 rewrite slice를 current truth로 승격하고 template-load 하나만 planned로 유지한다.

## 2026-08-07 P1 2/2b spec-rewrite reference interface post-sync
- 가설: verified rewrite reference diet만 승격하고 template-load를 planned로 유지하면 P1 마지막 feature의 evidence 경계가 선명하다.
- 검증: `P1_REWRITE_SPEC_SYNC_PASS v4.6.53 planned=1 processed=2`; main/changelog version 일치; decision/changelog 누적 `+124/-0`·`+25/-0`; completed planned 0, template planned 1; processed pair; `git diff --check` PASS. 첫 사후 phrase assertion 2회는 components의 동의어 표현을 literal로 가정한 checker defect였고 row semantic anchors로 교정했다.
- 결과: 통과 — main/components에 conditional load·no-rewrite exit·single-home verbatim template·example removal을 current truth로 반영했다. usage는 scenario/navigation 변화가 없어 무변경이다.
- 다음: P1 마지막 `spec-template-load-interface` feature draft와 plan-review를 시작한다.

## 2026-08-07 P1 2/2c spec template load interface plan-review
- 가설: create template 선택/load, upgrade staged reference load/current format, 통합 parity gate를 기존 8개 파일 안에서 닫으면 P1 마지막 규범 gap을 단일 컨텍스트로 해소할 수 있다.
- 검증: plan-review 측정 `C0 H2 M1`, 판단 `C0 H1 M3`, 합산 `C0 H3 M4`. current producer title·규모 판정 누락, dirty SKILL normalizer 비결정성, baseline 순서 역전 H3와 protected manifest 외부 의존, full 선택 술어, Claude canonical 근거, 중복 AC M4를 검출했다.
- 결과: 통과 — 두 구현 task + cross-task gate로 경계를 교정하고 pre-edit baseline precondition, exact anchor normalizer, 24-path protected manifest, current producer 순서, closed full criterion, canonical 대안·확신도, 통합 AC ownership을 한 번의 fix로 반영했다. author self-check tasks 3·AC 10·target 존재·`git diff --check` PASS, 잔존 C/H/M 0. 단일 패스 계약상 자동 재리뷰하지 않는다.
- 다음: ledger에 baseline을 먼저 기록한 뒤 Task 1·2 RED→GREEN과 Task 3 통합 검증을 실행한다.

## 2026-08-07 P1 2/2c spec template load interface 구현
- 가설: compact/full을 closed criterion으로 고르고 단계별 local asset 하나만 읽게 하면 startup preload와 template 재구성을 동시에 막을 수 있다.
- 검증: RED create selection `0/2`, upgrade staged block `0/6`, legacy temporary literal 12 → GREEN. normalized SKILL `4/4`, SKILL parity `2/2`, spec-format `2/2`, create template runtime parity `2/2`, asset path `12/12`, protected template `8/8`, protected hook/harness `24/24`, validator `4/4`, scoped set difference 4, `git diff --check` PASS.
- 결과: 지지 — create는 Structure Decision과 독립인 selected-only verbatim load를 Step 4에, upgrade는 conditional mapping/current-format load와 같은 template criterion을 Step 1/2/5에 둔다. Codex create templates는 Claude authoring canonical의 runtime-token-only mirror가 됐고 두 spec-format은 current producer 순서를 반영한다.
- 다음: correctness 3 + simplicity 2 implementation-review gate에서 AC1–AC10과 norms §3.1–§3.4를 검증한다.

## 2026-08-07 P1 2/2c spec template load interface implementation-review
- 가설: task별 correctness 3개와 interface/reference simplicity 2개를 분리하면 template 실물 drift와 single-home 위반을 함께 잡을 수 있다.
- 검증: correctness `C0 H3 M0`, simplicity `C0 H0 M3`, raw `C0 H3 M3`; heading drift 중복을 정규화해 unique `C0 H3 M2`. create fence 부재, upgrade heading mismatch, Open Questions semantic 축소 H3와 heading literal 이중 소유, defensive negative, temporary producer 설명 이중 홈을 검출했다.
- 결과: 지지 — fix 1회로 선택 기준을 semantic rationale로 바꾸고 create whole-template/upgrade fenced-template 실물 경계를 맞췄다. redundant negative를 제거하고 temporary shape는 same-runtime feature-draft Required Output이 단독 소유한다. post-fix review fix·producer parity·normalizer·asset 14/14·protected 8/8+24/24·validator 4/4·status·diff PASS, 잔존 C/H/M 0.
- 다음: v4.6.54 implemented spec-sync로 template-load를 current truth에 승격하고 P1 planned item을 0으로 만든다.

## 2026-08-07 P1 2/2c spec template load interface post-sync
- 가설: verified template/load interface만 current truth로 승격하면 P1 마지막 planned item을 evidence 기반으로 제거할 수 있다.
- 검증: `P1_TEMPLATE_SPEC_SYNC_PASS v4.6.54 planned=0 processed=2`; main/changelog version 일치; body main/components만 변경, usage 무변경; decision/changelog append-only; processed pair SHA 보존; `git diff --check` PASS.
- 결과: 통과 — main/components가 create selected whole-template, Claude canonical/Codex runtime mirror, upgrade mapping/global/direct-producer/selected-template stage load를 current truth로 반영했다. temporary shape는 feature-draft Required Output이 단독 소유한다.
- 다음: P1 네 component 횡단 parity·validator·report를 검증하고 priority commit을 만든다.

## 2026-08-07 P1 priority verification
- 가설: 네 lifecycle component를 한 번에 횡단 검증하면 feature별 gate가 놓친 mirror/runtime drift를 commit 전에 잡을 수 있다.
- 검증: official validator 8/8; SKILL parity 4/4; hook exact 4/4; create templates runtime parity 2/2; rewrite refs exact 2+runtime 1, examples removed 4/4; upgrade format/mapping/template parity; spec v4.6.54 planned P1 0; report 19 rows/P1 AUDITED 4; norms gate 6종 PASS; `git diff --check` PASS. 첫 rewrite checker는 known `/guide-create`↔`$guide-create` delta를 exact로 오판해 normalization 후 통과했다.
- 결과: 통과 — P1 네 component 모두 UPDATED, 잔존 C/H/M 0이며 commit-ready다.
- 다음: `refactor(norms-p1)` Conventional Commit 후 P2 감사를 시작한다.

## 2026-08-07 P1 priority commit
- 가설: P1 네 lifecycle component와 네 processed draft를 한 priority commit으로 고정하면 P2와 history 경계가 분리된다.
- 검증: staged 37 paths `git diff --cached --check` PASS; commit `8679235 refactor(norms-p1): align spec lifecycle skills`; commit 후 tracked worktree clean.
- 결과: 통과 — P0 `e42faa3`, P1 `8679235` 두 priority boundary가 생겼다.
- 다음: P2 세 document producer를 audit한다.

## 2026-08-07 P2 document surfaces feature-draft·plan-review
- 가설: summary/snapshot/guide를 실물 정본 1개·point-of-use load·runtime-neutral main loop로 함께 정리하면 22-path 변경을 단일 컨텍스트에서 닫을 수 있다.
- 검증: plan-review 측정 `C0 H5 M2`, 판단 `C0 H2 M1`, raw `C0 H7 M3`, collision finding 중복 정규화 unique `C0 H6 M3`. runtime metadata 삭제, summary byte-copy 충돌, dirty baseline, checker/Propagation 비재현성, non-verbatim summary template H6와 bounded writing/census/rubric M3를 검출했다.
- 결과: 통과 — `user_invocable` allowlist delta, exact snapshot marker/body hash, post-minus-initial status, fenced summary template, M10+D12 exact paths, pinned 5+1 validator, output-format normalizer, 14-row norms rubric, main-loop skeleton-first를 fix 1회 반영했다. tasks 4·AC16·target 22·`git diff --check` PASS, 잔존 C/H/M 0. raw C+H ≥3이므로 별도 `plan-review` 1회 실행을 권장하지만 단일 패스 계약상 자동 실행하지 않는다.
- 다음: implementation ledger에 baseline/RED를 기록하고 Task 1–4를 구현한다.

## 2026-08-07 P2 document surfaces 구현
- 가설: summary·snapshot·guide의 rich interface를 point-of-use reference 한 곳에 두고 main loop에 skeleton-first 집행만 남기면 runtime helper 중복을 없앨 수 있다.
- 검증: RED summary fence 0·example 2·snapshot parity 0·guide delete candidate 10·stale pointer 2 → GREEN. SKILL parity 3 pair, summary/guide single-home, snapshot marker·collision·body-hash, deletion 12/12, stale runtime 0, validator 5+Claude schema, target `M10+D12`, `git diff --check` PASS.
- 결과: 지지 — 6 SKILL과 4 rich reference를 갱신하고 중복·stale asset 12개를 제거했다. Claude snapshot의 runtime-only `user_invocable: true`는 allowlist delta로 보존했다.
- 다음: implementation-review correctness 4 + simplicity 2 gate로 AC1–AC16과 norms 14행·snapshot hard gate를 검증한다.

## 2026-08-07 P2 document surfaces implementation-review
- 가설: correctness 4개와 simplicity 2개를 분리하면 보존 계약의 edge case와 남은 단발성 검증 추상화를 함께 찾을 수 있다.
- 검증: raw `C2 H8 M10`, collision 정규화 unique `C1 H5 M5`. safe destination, reserved marker, translation fidelity, processed currentness, unsupported error scenario, normalized-hash gate와 세 producer의 판단 중복·삭제 census·고정 recipe를 검출했다.
- 결과: 지지 — main-loop fix 1회로 safe slug/direct-parent, marker preflight, semantic rubric, active-only summary, evidence-conditional guide, process single owner, raw baseline+census를 반영했다. post-fix mirror/schema/fixture/deletion/stale/status/validator 5+1/diff, `NORMS_PASS 14/14`, snapshot hard gate PASS; 잔존 C/H/M 0.
- 다음: `spec-sync` writer 두 shard로 v4.6.55 current truth와 decision/changelog/processed pair를 동기화한다.
