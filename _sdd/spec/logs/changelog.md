# Changelog

> 이 파일은 `_sdd/spec/main.md`의 **본문이 바뀐 버전만** 기록한다 — 본문 무변경 sync(헤더 날짜만 갱신)는 entry를 남기지 않으므로 버전 번호에 결번이 생길 수 있다.

#### v4.7.0 (2026-08-10)

- **sdd-autopilot을 goal-init SDD instance로 전환 (post-implementation sync)**: `sdd-autopilot`을 독립 end-to-end runner에서 existing `goal-init(preset=sdd)`를 호출하는 setup-only thin entrypoint로 전환했다. `goal-init`은 기존 5단계·condition self-check·4-file harness를 보존하면서, native goal 활성화 뒤 unmet DONE WHEN 또는 failed final integration-proof gap에서 최소 next unit을 선택해 `feature-draft → implementation → persistent spec-sync → evidence 기록 → final integration proof`로 수렴하는 6-step SDD Loop Protocol payload를 제공한다. setup은 initial producer 실행·native goal 활성화·current goal status 조회·기존 goal mutation/block을 하지 않고 activation은 사용자가 결정한다. rolling split은 current goal 안에서 계속하며 nested goal-init, formal Goal Contract/queue schema/goal-level reviewer는 도입하지 않는다. Claude는 plugin-prefixed invocation, Codex는 active installed skill catalog를 사용한다.
- **문서·검증 evidence**: 한·영 AUTOPILOT_GUIDE, README, `_sdd/env.md`를 setup/activation/native-goal-loop 모델로 정렬하고 obsolete pre-flight를 제거했다. draft AC1–AC20 MET, exact live target 10/10, excluded surface 무변경, stale runner/blocker census 0, template payload parity, `git diff --check` PASS를 확인했다. implementation-review gate 1 `C2 H1 M2 L0`와 gate 2 `C0 H0 M3 L0` finding을 모두 수정했고 gate 3 임계값에는 도달하지 않았다.

#### v4.6.57 (2026-08-10)

- **Bounded conditional second quality-gate pass (post-implementation sync)**: `feature-draft`와 `implementation` producer는 gate 1/fix 1을 항상 수행하고, gate-1 fix 전 raw finding이 `Critical+High ≥ 3` 또는 `Medium ≥ 5`일 때만 같은 gate를 한 번 더 호출해 fix 2와 producer별 표적 검증을 수행한다. Low는 임계값에서 제외하고 `implementation-review` shard는 dedup 없는 raw 합계를 유지한다. 기본 경로는 1회, 임계값 경로는 최대 2회이며 gate 3은 없다. gate-2 raw finding도 같은 임계값이면 producer는 세 번째 호출 대신 수동 follow-up review 1회를 권고한다. 사용자와 `sdd-autopilot`은 gate를 재호출하거나 fix하지 않고 reviewer/orchestrator는 호출당 single-pass 계약을 유지한다. v4.6.30의 advisory-only 동작을 supersede했다.
- **문서·검증 evidence**: 한·영 `SDD_WORKFLOW`·`AUTOPILOT_GUIDE`를 기본 1회/조건부 최대 2회, ownership, 호출별 최종 보고, no-third 의미로 정렬했다. exact 8개 구현·문서 표면, 구조적 RED→GREEN, AC 14/14, stale contract 0, runtime mirror parity, reviewer surface 무변경, `git diff --check`가 통과했다. 최초 implementation-review `C0 H0 M1 L0`의 M1 수정과 회귀를 완료했고 후속 advisory 변경 검토는 `C0 H0 M0 L0`이었다.

#### v4.6.56 (2026-08-08)

- **AGENTS.md 하네스 규범 다이어트 (post-implementation sync)**: `docs/SKILL_AUTHORING_NORMS.md` §3 체크리스트를 하네스 자신 — `AGENTS.md` 인스턴스와 정본 템플릿 `agents-harness-template.md`(미러 4 byte-identical) — 에 적용했다. §2 유효 검증 정의 이중 서술을 단일 문장으로 통합(F1, 인스턴스 한정 — 두 번째 문장은 템플릿 부재·repo 채움 유래 실측), §3 spec-sync 내부 로직 재서술을 제거하고 "계획·구현 반영의 단일 진입점" 수준만 유지(F2), work log 의무를 §5 단일 홈으로 두고 §2는 포인터화(F3), §0에 원칙 상세 홈 포인터 `docs/agentic_coding_principle.md` 추가(F4, 인스턴스 한정), §3·§4 복사 금지 negative 2건에 방지 실패 근거 병기(F5). §0~§5 헤더·SDD-HARNESS 마커·`<…>` 슬롯·repo 채움 값은 불변이며 SKILL.md "§0~§5" 리터럴 12곳 census는 비발동이다.
- **검증 evidence**: plan-review CLEAR(실측 M2 L2 + 판단 M1 L1 반영), implementation-review C0 H0 M0 (L2 advisory), 전 AC MET. implementation ledger DONE — 삭제 문구 변형형 5파일 전수 grep 잔존 0, 템플릿 4 md5 단일(e3b6a9e), 인스턴스 delta 유입 0, §헤더 6:6, `git diff --check` PASS.

#### v4.6.55 (2026-08-07)

- **document producer single-home interfaces and deterministic snapshot preservation (post-implementation sync)**: `spec-summary`는 runtime-local `summary-template.md`를 fenced whitepaper shape의 단일 홈으로 두고 완성 example을 제거했다. `guide-create`는 `output-format.md`에 section·citation/evidence·confidence rubric을 모으고 compact/tool-gate reference와 confidence example을 제거했다. 두 producer는 작성 직전 fenced skeleton을 verbatim/slot-only로 적용하며 main loop가 skeleton-first로 직접 작성한다. `spec-snapshot`은 source 사전/사후 manifest exact match, safe slug·direct-parent confinement·collision suffix, exact metadata marker, source summary present/absent 분기로 read-only 보존을 결정적으로 닫았다. Claude의 `user_invocable: true`만 runtime allowlist delta로 보존했다.
- **검증 evidence**: implementation ledger `REVIEW_PASSED`, AC1–AC16 GREEN. implementation-review raw `C2 H8 M10`, unique `C1 H5 M5`를 fix 1회로 해소해 잔여 C/H/M 0이다. final `M10+D12`, SKILL/reference parity, deleted asset 12/12, stale runtime zero 6/6, official validator 5/5 + Claude schema, snapshot fixture·read-only hard gate, `NORMS_PASS 14/14`, `git diff --check` 모두 PASS했다.

#### v4.6.54 (2026-08-07)

- **spec template selection and point-of-use load interface (post-implementation sync)**: `spec-create`는 compact default와 semantic-loss 기반 full criterion을 사용하고, Step 4 직전에 선택한 template 전체 skeleton만 읽어 verbatim 적용한다. Claude template은 authoring canonical, Codex template은 runtime invocation token만 다른 distribution mirror다. `spec-upgrade`는 mapping → global format/same-runtime `feature-draft` producer → selected fenced template을 실제 Step 1/2/5 소비 지점의 단일 path home으로 두고 verbatim/slot-only로 적용한다. `spec-format`의 stale temporary-spec 설명은 제거했으며 temporary shape는 `feature-draft` `Required Output`이 단독 소유한다. `spec-template-load-interface`를 current truth로 승격해 P1 2/2를 완료했다.
- **검증 evidence**: implementation ledger `REVIEW_PASSED`, AC1–AC10 GREEN. implementation-review raw `C0 H3 M3`, unique `C0 H3 M2`를 fix 1회로 해소해 잔여 C/H/M 0이다. normalized SKILL 4/4, asset path 14/14, protected template/reference 8/8 + hook/harness 24/24, validator 4/4, Claude/Codex parity와 `git diff --check`가 모두 PASS했다.

#### v4.6.53 (2026-08-07)

- **spec-rewrite point-of-use references and single-home template (post-implementation sync)**: Claude/Codex `spec-rewrite`는 shape 판별·rewrite 진입·target 재구성의 실제 소비 시점에서만 `spec-format`·`rewrite-checklist`·`template-compact`를 조건부로 읽고, no-rewrite에서는 후속 단계와 asset load를 종료한다. `template-compact`가 current temporary-spec fenced skeleton을 단독 소유하고 verbatim/slot-only 적용을 강제하며, format/checklist는 pointer-only로 유지한다. SKILL의 plan/report producer를 재구현하던 단일 사용 example 네 파일은 제거했다. `spec-rewrite-reference-interface`는 current truth로 승격했고 `spec-template-load-interface`는 `🚧 Planned`로 유지했다.
- **검증 evidence**: implementation ledger `REVIEW_PASSED`, AC1–AC16 GREEN, final 8 `M` + 4 `D`, `+106/-140`, exact producer template, conditional load·no-rewrite exit·verbatim apply·example removal PASS. implementation-review raw `C0 H4 M8`, unique `C0 H4 M7`을 fix 1회로 해소해 잔여 Critical/High/Medium 0이다.

#### v4.6.52 (2026-08-07)

- **spec-review deterministic status and disposition interface (post-implementation sync)**: Claude/Codex `spec-review`의 drift status를 evidence 충분성 → 확인된 한쪽 부재 → 양쪽 비교의 ordered route와 `ALIGNED | DRIFT | MISSING | UNTESTED` allowed set으로 고정했다. spec disposition은 material uncertainty → verified spec-side drift → otherwise 순서로 `NEEDS_DISCUSSION | SYNC_REQUIRED | SPEC_OK`를 선택한다. Output은 producer를 가리키고 enum을 재복제하지 않으며, revision/history/change-set 분석은 scope나 finding을 실제로 뒷받침할 때만 bounded evidence로 남긴다. `spec-review-deterministic-interface`는 current truth로 승격했고 `spec-rewrite-reference-interface`와 `spec-template-load-interface`는 각각 `🚧 Planned`로 유지했다.
- **검증 evidence**: implementation ledger `REVIEW_PASSED`, AC1–AC10 GREEN, Claude/Codex exact mirror, validator 2/2, baseline normalization, scoped target set, report path와 `git diff --check` PASS. implementation-review raw `C0 H0 M2`, unique `C0 H0 M1`을 fix 1회로 해소해 잔여 Critical/High/Medium 0이다.

#### v4.6.51 (2026-08-07)

- **spec quality interface 3-feature 분할 (pre-implementation planned sync)**: P1 2/2 `spec-quality-interface` umbrella todo를 `spec-review-deterministic-interface` → `spec-rewrite-reference-interface` → `spec-template-load-interface` 순서의 세 개별 `🚧 Planned` 항목으로 교체했다. task/AC 상세는 feature draft에만 남겼고 `components.md`·`usage-guide.md`는 변경하지 않았다.
- **Status/evidence**: 첫 feature의 Claude/Codex `spec-review` target diff 0, 관련 implementation ledger 0이므로 세 delta 모두 `PLANNED / NOT_IMPLEMENTED`다. 입력 draft는 process/rename 없이 원래 경로에 보존했다.

#### v4.6.50 (2026-08-07)

- **spec bootstrap hook contract progressive disclosure (post-implementation sync)**: `spec-create`·`spec-upgrade` 네 package에 local `references/hook-installation.md`를 두고, Claude `spec-create` 사본을 authoring canonical, 나머지 세 사본을 exact distribution mirror로 고정했다. `spec-create`는 top-level AC·Hard Rule·Step 3e·Validation·Output에 trigger·pointer만 남겼고, `spec-upgrade`는 자기 local reference를 읽으며 partial/legacy repair·dual-runtime 보완·재실행 diff 제거를 소유해 cross-skill 의존을 없앤다. P1 1/2는 완료, P1 2/2 `spec-quality-interface`는 `🚧 Planned`다.
- **검증 evidence**: SKILL 4면 net `-202`, literal target 8개, official validator 4/4, protected asset 28개 exact match. implementation-review `C0 H2 M5`를 fix 1회로 해소했고 잔여 C/H/M 0, final structural·mirror·target census·protected manifest·`git diff --check` 모두 PASS했다.

#### v4.6.49 (2026-08-07)

- **spec lifecycle P1 두-feature 롤링 계획 고정 (pre-implementation planned sync)**: `spec-bootstrap-disclosure` → `spec-quality-interface`를 두 개의 독립 `🚧 Planned` todo로 추가했다. 첫 feature는 `spec-create`·`spec-upgrade`의 hook 설치 상세를 package-local rich reference로 옮기고 Claude `spec-create` reference를 authoring canonical, 나머지 세 사본을 exact 배포 mirror로 유지한다. 둘째 feature는 `spec-review` criterion·status/decision enum과 `spec-create`·`spec-rewrite`·`spec-upgrade`의 template/reference/example 선택·load·output interface를 완결하고 legacy 7-section temporary-spec 설명을 current producer shape로 갱신한다.
- **Status/evidence**: 신규 hook reference 0개, 네 current skill target diff 0개, 관련 implementation artifact 0개다. 두 feature 모두 `PLANNED / NOT_IMPLEMENTED`이며 current truth 승격은 없다. 입력 draft는 다음 implementation을 위해 원래 경로와 내용으로 보존했다.

#### v4.6.48 (2026-08-07)

- **implementation producer·review pair 규범 다이어트 (post-implementation sync)**: Claude/Codex `implementation`을 gate 단일 패스·Critical/High/Medium fix 1회와 Low 판단의 단일 홈으로 두고, 규모 초과 시 `feature-draft`의 `분할 방법 (롤링)`을 가리키도록 했다. ledger에는 source task 변경·새 edge case의 이유와 처리를 기록하는 `계획 이탈·발견`을 계약 오류 필드와 분리해 추가했다. `implementation-review` wrapper는 review-only/no-plan digest ownership을 통합하면서 두 렌즈·shard relay·runtime adapter를 보존했고, agent는 no-file/no-spawn 경계를 단일화하고 producer fix-count 재천명을 제거했으며 Step 3을 `Fresh Verification` canonical home으로 연결했다. P0 5/5가 모두 구현됐다.
- **검증 evidence**: 6개 target surface, AC1–AC15 MET, RED→GREEN. implementation-review `C0 H0 M8`(7개 고유 원인)을 fix 1회로 해소해 잔여 C/H/M 0. runtime reviewer 3+1 deviation을 기록했고, 최종 `+41/-29`, mirror/core/TOML/Source/runtime/frontmatter/validator/status/diff 및 `git diff --check` 모두 PASS.

#### v4.6.47 (2026-08-07)

- **feature-draft producer·plan-review verifier 규범 다이어트 (post-implementation sync)**: Claude/Codex `feature-draft`는 로컬로 해소되지 않고 답이 architecture·scope·Target Files를 바꾸는 unknown만 한 번에 하나씩 영향 순으로 묻고, 무인 실행은 가정·근거를 기록한다. inline `Required Output`은 verbatim 출발 skeleton으로 쓰되 placeholder 치환·필요 row/block 반복·조건부 section 삭제를 허용한다. AC evidence는 재현 가능 check 또는 rubric+reviewer+인용의 2등급으로 닫고 이진·외부·반박 가능 기준을 공유하며, minimum code는 요청 동작/관측 위험에 직접 추적되는 최소 변경이다. `plan-review-agent`는 세부 계약 복제 대신 current producer contract을 조건부로 읽고, source 부재는 `Verification Weakness=UNKNOWN`으로 닫으며 evidence/minimum-code를 smallest-change 규칙 하나로 합쳤다. plan-review wrapper 2면은 thin entrypoint로 감사해 `NO_CHANGE`로 유지했고 P0 5/5는 `🚧 Planned`다.
- **검증 evidence**: 변경 target 4면 + wrapper `NO_CHANGE` 2면, AC1–AC15 MET. checker deviation T1 2건·T2 1건 교정 및 HEAD re-RED, implementation-review `C1 H0 M2` fix 1회 후 잔여 C/H/M 0. exact feature mirror, normalized agent core parity, TOML parse, wrapper diff 0, `quick_validate.py` 2면, `git diff --check` 모두 PASS.

#### v4.6.46 (2026-08-07)

- **pr-review 입력·UNTESTED 경계 다이어트 (post-implementation sync)**: Claude/Codex `pr-review` wrapper와 correctness/simplicity reviewer의 공통 payload를 `Changed Files`·`PR Diff`·`PR Metadata`·`PR Discussion`·`Spec Context`·`Validation Evidence`·`Report Slug` 순서의 정확한 7필드 `PR Review Input`으로 통일했다. wrapper는 PR·CI/local evidence 수집·redaction과 통합 verdict/report만 소유하고 agent 반환 계약을 소비한다. correctness reviewer는 read-only 및 CI → local → 사유 있는 `UNTESTED` 검증 경계를 소유하며, test-dependent evidence 부재는 non-test/N/A 예외를 제외하고 `NEEDS DISCUSSION`으로 흐른다. simplicity reviewer는 Changed Files/PR Diff만 범위 판단에 쓰고 validation을 재판정하지 않으며, checklist는 wrapper Step 4를 canonical verdict 기준으로 가리킨다. 두 reviewer의 병렬 dispatch와 wrapper 단일 작성자 경계는 유지했고 P0 4/5~5/5는 계속 `🚧 Planned`다.
- **검증 evidence**: 8개 target surface, AC1–AC17 MET. implementation-review aggregate `C0 H1 M2`를 fix 1회로 해소해 잔여 C/H/M 0. 6-surface input exact parity, checklist pointer 2면, TOML 2개 parse, normalized agent core parity, target census, `git diff --check` 모두 PASS.

#### v4.6.45 (2026-08-07)

- **spec-sync digest interface and single-home agent rules (post-implementation sync)**: Claude/Codex `spec-sync` wrapper와 `spec-sync-agent` 사이 implemented sync digest를 `Delta List`·`Classification Basis`·SemVer `Spec Version`·`Decision Title`의 비어 있지 않은 고정 4필드 producer/consumer 계약으로 통일했다. 두 분할 호출은 같은 digest를 사용한다. agent의 status routing, legacy input discovery, `_processed_` 묶음 소유 규칙은 각각 `Status 분류 (Routing)`·`Input Sources`·`호출자 표면 한정` 한 곳만 canonical home으로 남겼다. 기존 status 의미·evidence 승격·dispatch topology·report contract는 유지하며 P0 3/5~5/5는 계속 `🚧 Planned`다.
- **검증 evidence**: T1/T2/T3 structural RED exit 1 → GREEN exit 0, AC1–AC12 MET, correctness shard finding 0. simplicity Medium 3건 fix 1회 반영 뒤 digest census, single-home, agent mirror semantics, TOML parse, `git diff --check` 모두 PASS.

#### v4.6.44 (2026-08-07)

- **SKILL_AUTHORING_NORMS P0 1/5 autopilot-simplicity 규범 다이어트 완료 (post-implementation sync)**: Claude/Codex `sdd-autopilot`은 Workflow Position 다이어그램, producer 내부 알고리즘 재서술, 형식 리터럴과 수치형 질문 knob를 제거하면서 chain order·no-approval·spec-sync-only write 경계와 플랫폼별 runtime delta를 보존했다. Claude/Codex `simplicity-review-agent`는 correctness/read-only/falsifiability 반복을 축약하면서 5개 차원, severity·return·path 계약과 플랫폼별 실행 경계를 유지했다. 4파일 diff는 28 insertions / 74 deletions, 현재 line count는 71/70/92/93이다. P0 2/5~5/5는 계속 `🚧 Planned`다.
- **검증 evidence**: 3개 task structural RED→GREEN, 14/14 AC MET, TOML parse와 `git diff --check` PASS. implementation-review correctness 전부 MET, simplicity Medium 3건 fix 1회 반영, post-fix regression PASS, 잔여 Critical/High/Medium 0.

#### v4.6.43 (2026-08-07)

- **SKILL_AUTHORING_NORMS P0 나머지 5쌍 롤링 분할 고정 (pre-implementation planned sync)**: `autopilot-simplicity-diet` → `spec-sync-agent-diet` → `pr-review-diet` → `feature-draft-pair-diet` → `implementation-pair-diet`를 개별 `🚧 Planned` todo로 추가했다. 공통 방향은 지시·판단 주체 단일 홈화, 근거 없는 수치·방어 규칙의 기준화, 하드 게이트 존치 근거 유지이며 `Propagation Surfaces` 계약은 `feature-draft` 소유로 단일 홈화한다. Final Check 1줄은 유지하고 discussion 쌍과 하네스는 범위에서 제외한다.
- **Status/evidence**: 첫 feature의 plan-review는 완료됐지만 구현 코드·validation evidence는 없다. 5개 전부 PLANNED이며 current truth 승격은 없다. 입력 draft는 `_processed_`로 표시하되 Part 2를 보존해 다음 implementation 단계에서 계속 검색 가능하다.

#### v4.6.42 (2026-08-07)

- **discussion 스킬 쌍 규범 다이어트 — SKILL_AUTHORING_NORMS 적용 1호 (post-implementation sync)**: v4.6.41의 규범 문서를 실제 스킬에 적용한 첫 사례. SKILL_AUTHORING_NORMS 리뷰 finding F1~F9를 discussion 스킬 쌍에 반영 — claude SKILL.md 436→320줄, codex 400→275줄. 신규 contract: **요약 템플릿 단일 소스 = `references/summary-template.md`(claude·codex 양쪽)**, Step 4는 Read+verbatim 복사(`[...]` 슬롯만 치환)로 소비. 그 외: 파일 생성 규칙 Hard Rules 1곳 단일화 + work log 규약 예외 명시(AGENTS.md §5 충돌 해소, "호출 환경의 work log 규약" 일반화), 수치 노브 4건(연속 2라운드 비판 금지·매 3라운드 요약·stagnation 2회·재방문 1회) 기준화, 3.1/3.2 의사코드 산문화, 예시 표 상세는 question-guide 위임(깊이 신호 예시 표 신설로 정보 보존), 질문 선택 전략에 아키텍처-변경 질문 우선 기준 추가. 행동 로직(커버리지·게이트·카테고리 4종·근거 유형 4종 enum·Gate 구조)은 의미 변경 없음. Final Check 삭제 계열 finding은 d903052 존치 결정으로 기각. codex 미러는 3-way merge로 고유 delta(interactive-only·request_user_input·최신성 HR) 보존.
- **검증 evidence**: 게이트 plan-review CLEAR(M2 L2 반영), implementation-review 전 AC MET, 합산 M6 L5 → fix 1회 반영, fix 후 census 재실행 전건 통과(변형형 grep 잔존 0·헤더 대응 5:5·템플릿 쌍 identical). 재리뷰 임계(M≥5) 도달로 추가 리뷰 권장은 advisory로 기록.

#### v4.6.41 (2026-08-07)

- **Claude 5 세대 스킬 제작 규범 문서 추가 (post-implementation sync, 경량 경로)**: `docs/SKILL_AUTHORING_NORMS.md` 신규 추가(82줄, 한국어) — Claude 5 세대 모델 대상 스킬/agent/하네스 제작 규범 체크리스트. Anthropic 블로그 2편("The New Rules of Context Engineering for Claude 5 Generation Models" + "A Field Guide to Claude Fable: Finding Your Unknowns") 증류. 구성: §1 배경(80% 프롬프트 제거, 규칙→judgment) / §2 Then→Now 전환 표 / §3 제작 체크리스트(본문·구조 progressive disclosure·rich reference·인터페이스) / §4 Unknowns 실천법→SDD 단계 매핑 표 / §5 기존 repo 규범과의 관계(부합점 + 하드 게이트 유지 조건 "걷어낼 자격은 실측이 준다"). 배경: 기존 docs 문서 병합 안을 검토했으나 사용자가 신규 문서로 지시. 경량 경로 근거: 순수 참고 문서 — 계약·스킬 로직·미러 전파 없음(신규 파일 조건은 형식상 걸리나 전파 표면 부재).
- **검증 evidence**: TODO/TBD grep 0건, `git diff --check` 통과.

#### v4.6.40 (2026-08-07)

- **Codex/Claude hook parity and dual-setting runtime acceptance (post-implementation sync)**: Feature 1~3을 하나의 runtime parity 계약으로 완결했다. 훅 4종(`worklog-gate.sh`, `worklog-context.sh`, `harness-context.sh`, `agent-watchdog.sh`)은 self-host + `spec-create`/`spec-upgrade` Claude·Codex reference surface 5곳에서 같은 실행 자산으로 유지되고, `SessionStart`는 cross-runtime `hookSpecificOutput.additionalContext` JSON, `PreToolUse`는 work-log gate, `PostToolUse`는 advisory watchdog을 제공한다. 두 설치 스킬은 `.claude/settings.json`과 `.codex/hooks.json`을 독립 병합해 비-SDD handler·top-level key를 보존하며, 한 runtime 설정이 손상돼도 반대 runtime 설치를 계속하고 반복 실행 멱등성을 지킨다. acceptance는 실제 격리 Codex skill invocation fixture의 trust boundary와 `SessionStart`/clear/`PreToolUse`/watchdog lifecycle, Claude Code smoke, manifest 안정성, no-bypass까지 포함한다.
- **검증 evidence**: scripts 4×5 byte parity + `bash -n`, SKILL mirror byte parity, JSON canonical map, isolated manifest 안정성, Codex 0.146.0·Claude 2.1.223 실제 lifecycle, current-repo hook trust 정확 범위 승인, global config SHA1 `e9bbd36054cbd784565c250e277c9d9c40851de4`, trust bypass 0. 세 feature draft AC 전부 체크, implementation-review C2/H8/M4 fix pass 완료.

#### v4.6.39 (2026-08-06)

- **리뷰 게이트 Low finding 선택적 fix (correctness/plan-review 3조건 · simplicity Low advisory 유지) (post-implementation sync)**: 리뷰 게이트 Low finding을 무조건 advisory에서 **3조건 AND 게이트** 기반 선택적 fix로 전환. correctness 렌즈 Low(`implementation-review-agent`)와 plan-review Low(`feature-draft` 게이트)는 **저비용 AND 명백히 이득 AND 현재 change scope 내** 세 조건을 모두 만족할 때만 조건부 fix/반영하고, 아니면 advisory 유지. simplicity 렌즈 Low는 주관적 취향이라 churn 방지로 선택 fix 대상에서 제외하고 advisory 유지. 배경: 사용자 요청 "판단해서 고칠만한건 고치게" — Low여도 값싸고 명백히 이득이면 같은 change scope 안에서 고치도록. 3조건 AND에서 `현재 scope 내`가 load-bearing conjunct로 scope creep을 차단해 단일 패스·fix 1회·gating exit(`critical=high=medium=0`) 불변식을 보존한다. 이 정책은 기존 "Low는 무조건 advisory" 단언(decision_log의 review-fix severity boundary·falsifiable-only gating의 categorical 서술)을 supersede하되 Critical/High/Medium fix 1회 계약은 무변경. 구현 표면 6파일(claude+codex 미러 3쌍): `implementation/SKILL.md` L109, `feature-draft/SKILL.md` L89, `implementation-review-agent` L77.
- **검증 evidence**: structural check grep/diff로 **12 AC MET**, implementation-review 2렌즈 Blocker CLEAR·Medium 2·Low 1, review-fix로 `implementation/SKILL.md` L109·`feature-draft/SKILL.md` L89 중첩 bullet 재구성.

#### v4.6.38 (2026-08-05)

- **Agent Watchdog 훅 — 하네스 훅 자산 4호 (advisory) (post-implementation sync)**: 하네스 훅 자산 4호 `agent-watchdog.sh`(PostToolUse) 추가 — subagent 장기실행(첫 tool call 후 300s+) 시 자기점검 nudge(시간 도둑 자평·캐시/재사용 전환)를 전달, cooldown 300s, advisory·fail-open, jq→python3 fallback. 배경: review agent가 20분씩 도는 원인(예: `uv run --with torch` 반복 재설치)을 사용자가 매번 알 수 없어 5분 초과 agent의 자기점검·전환 훅을 요청, 2026-08-05 실험 1·2(work log 항목 11·12)로 성립 조건 검증(훅은 subagent tool call에 발동·agent_id는 subagent payload에만·PostToolUse decision:block reason이 subagent 모델에 전문 전달·지시 수행). 구현 표면: 스크립트 5경로(정본+미러3+dogfooding, md5 5-way) + spec-create/spec-upgrade SKILL 4파일 설치 계약(개수 리터럴 3→4, census 확장 패턴 `세 스크립트|스크립트 3개|세 훅|훅 3개|셋 다|두 항목` 잔존 0) + `.claude/settings.json` PostToolUse 등록. 새 contract 2건: ① 하네스 훅 자산 목록 3→4개 ② watchdog은 advisory 자산 — "조용히 무력화되지 않는다" guardrail의 경고 의무는 강제 자산(게이트)에 한정(worklog-context.sh 경고 확장 기각 — 5미러 표면 확대 대비 이득 미미). 알려진 한계: nudge는 tool call 경계에서만(단일 장시간 명령 중간 개입 불가 — 후속 PreToolUse 패턴 차단 레버 후보로 스코프 아웃).
- **검증 evidence**: structural check RED 12 → GREEN **28/28**, 변이 7종 전량 kill, implementation-review(correctness 5 shard + simplicity 2묶음) fix 전 C/H 0 · M 1(도달 불가 줄바꿈 이스케이프 no-op → fix) · L 5 advisory.

#### v4.6.37 (2026-08-05)

- **work log 모델명 병기를 전 항목으로 일반화 (post-implementation sync)**: 같은 날 v4.6.36의 "리뷰 게이트 수치에만 실행 모델명 병기" 규칙을 모든 work log 항목으로 확대(사용자 제안, supersede가 아니라 일반화) — 항목 형식을 `## <순번/HH:MM> <제목> (<실행 모델명>)`로 확장하고, 게이트 한정 bullet은 "모델명은 모든 항목 제목에 병기하고, 게이트를 다른 모델로 돌렸으면 그 수치 옆에도 적는다(예: `plan-review (opus-5): H2 M2`) — 모델별 finding 밀도 비교용"으로 대체. 배경: 게이트 수치만 태그하면 draft 작성·구현 등 producer 단계의 모델 귀속이 여전히 유실되며, 항목 제목 병기는 비용 동일하면서 모든 SDD 단계 산출물이 모델별로 추적된다. 게이트 병기 예시는 모델 override 시 규칙으로 존치. 적용 표면 5곳 전수(파일당 +2/-2): `AGENTS.md` + `{.claude,.codex}/skills/{spec-create,spec-upgrade}/references/agents-harness-template.md` 4벌.
- **검증 evidence**: git diff(브랜치 chore/worklog-model-tag, 미커밋) 5표면 동일 문면, §5 블록 md5 일치 검증 완료.

#### v4.6.36 (2026-08-05)

- **work log 게이트 수치에 실행 모델명 병기 (post-implementation sync, 경량 경로)**: 하네스 §5 work log 규약에 bullet 1줄 추가 — 리뷰 게이트(plan-review·implementation-review) 결과 수치를 기록할 때 실행 모델명을 병기한다(예: `plan-review (opus-5): H2 M2`) — 모델별 finding 밀도 비교용. 배경: 모델 회귀 가설이 2026-08-05 진단에서 UNCONFIRMED로 남은 원인이 work log 게이트 기록에 실행 모델 표본 부재였고, 대안(별도 계측 파일·A/B 실험)보다 비용이 사실상 0인 기록 규약 확장을 채택. 적용 표면 5곳 전수: `AGENTS.md` + `{.claude,.codex}/skills/{spec-create,spec-upgrade}/references/agents-harness-template.md` 4벌(동일 문면) — 템플릿 포함이므로 소비 repo 하네스에도 적용된다. 경량 경로 근거: 새 contract/invariant 없음 · 신규 파일 없음 · 전파 표면 5곳 전수 열거 + md5/diff 검증.
- **검증 evidence**: git diff(브랜치 chore/worklog-model-tag) 5표면 동일 문면 추가, §5 블록 md5 일치 검증 완료.

#### v4.6.35 (2026-08-05)

- **resume-only implementation ledger 도입 (post-implementation sync)**: `implementation` SKILL 2벌에 `## Implementation Ledger (resume pointer)` 절 신설 — 모든 실행이 `_sdd/implementation/<YYYY-MM-DD>_implementation_ledger_<slug>.md`를 생성하고, 같은 slug 기존 ledger는 이어쓴다(분열 금지). 목적은 감사가 아니라 compact/세션 재개 후 다음 행동을 결정하는 resume pointer이며, 기록 기준 = **재실행으로 복원할 수 없는 사실만**(출력 전문·서술형 진행기 금지) — 재실행으로 복원 가능한 영역은 (b) structural-check 구현의 무상태 복원력이 담당하므로 중복하지 않는다. task당 4상태 `READY → RED_CONFIRMED → GREEN_CONFIRMED → DELTA_CLOSED`((c) test-free task는 `READY → DELTA_CLOSED` 직행), 재개 시 미완료 task는 무조건 fresh 재판정·DELTA_CLOSED는 diff 모순 시만 재확인. 마감 AC→증거 테이블의 기록처를 ledger로 통합(채팅 노출 유지, 이중 기록 제거), 게이트 fix는 `Review fix delta` 단일 블록. SDD_SPEC_DEFINITION 한·영 §6에 구현 기록처로 implementation ledger 명시, AUTOPILOT_GUIDE 한·영 산출물 목록에 ledger 추가. 도입 관측 exit 조건(스킬 계약 아님): 수 회의 구현에서 실제 재개에 읽히지 않으면 회수를 재검토한다.
- **검증 evidence**: structural check RED **24 FAIL** → GREEN, post-fix 회귀 **35/35 pass**(exit 0), 변이 확인 **3회 kill**, 미러 byte parity, implementation-review 6 reviewer(correctness 3 shard + simplicity 2 묶음) Medium 3 전부 fix 반영·Low 5 advisory 잔존(전체 status 갱신 시점·증거 발췌 수준·en 글롭 비대칭·AUTOPILOT_GUIDE 헤더 날짜 stale·ko 글롭 밀도).

#### v4.6.34 (2026-08-05)

- **feature-draft D&A(Decisions and Assumptions) 5필드 계약 제거 — 산문 복귀 (post-implementation sync)**: v4.6.33(같은 날, 커밋 99a6bd5)이 도입한 두 계약 중 D&A 5필드만 제거한다(사용자 확정 결정) — 실패 이력 없는 곳에 형식을 추가한 것으로, 알맹이(사용자 확인 필요 결정의 구현 전 노출)는 기존 `Open Questions` 표면이 이미 담당하고 5필드 구조는 형식 준수 검사로 퇴화하기 쉽다(산문 규칙 > 의사코드). producer(feature-draft SKILL 2벌)에서 조건부 5필드 템플릿·`중요 결정만 기록` Hard Rule 제거(Process 1은 propagation 식별만 유지), reviewer(plan-review-agent 2벌)의 AC3·Hard Rule 7·Step 2·Step 4를 99a6bd5^ 산문(숨은 결정 surfacing 산문 규칙 + Step 4 4불릿 + decision markers 추출)으로 복귀, SDD_SPEC_DEFINITION 한·영 canonical 구조에서 D&A 항목 제거·재번호(3=Propagation Surfaces, 4=Part 2, 5=Open Questions) + 스켈레톤 D&A 2줄 제거. 실측 실패 이력(다중 표면 누락 재발) 기반인 `Propagation Surfaces` 계약 — Hard Rule 8·Step 3 계단 propagation 검증·Verification Weakness propagation 문구 — 은 유지한다.
- **검증 evidence**: structural check **70/70 pass**(RED 45 FAIL → GREEN, exit 0), 커버리지 델타 변이 확인 **1/1 kill**, producer 미러 byte parity, TOML 파싱 통과, census 계약 고유 리터럴 **0건**(허용 예외: plan-review-agent 2벌 Step 4 헤딩 `Review Decisions and Assumptions`), implementation-review 6 reviewer(correctness 4 shard + simplicity 2 묶음) finding **0**.

#### v4.6.33 (2026-08-05)

- **feature-draft producer-review contract alignment (post-implementation sync)**: 모든 feature draft에서 결과 방향·Target Files·task boundary를 바꿀 수 있는 중요 결정만 조건부 `Decisions and Assumptions` 5필드로 기록하고, 중요 결정이 없으면 섹션 부재를 허용한다. 동일 change element가 둘 이상의 동기화 표면에 걸릴 때만 `Propagation Surfaces` 5열 표를 만들고 각 행을 정확히 한 owner task의 Target Files·AC에 연결한다. 일반 다중파일은 비발동이며 변형 표기 전수 제거만 별도 census task로 닫는다. `plan-review`는 같은 decision 조건과 propagation의 발동·required surface 실측·discovery 기대 집합·단일 owner·task 연접을 새 smell 없이 기존 `Verification Weakness`와 Glob→Grep→Read 계단에서 검사한다.
- **검증 evidence**: 구현 6파일, RED→GREEN, canonical assertions **12/12**, 동일 checker mutant **12/12 killed**, producer byte parity, TOML parse, exact census, post-fix regression 통과, implementation-review finding fix 완료. producer·reviewer·정의 문서에 공통 적용되고 누락 시 repo-level planning/review 판단이 어긋나는 지속 계약이라 Repo-wide Invariant Test를 통과했다.

#### v4.6.31 (2026-08-03)

- **SDD 체인에 경량 경로(light path) 명문화 — 성질 3조건 + 하네스 템플릿 4벌 전파 (post-implementation sync)**: 하네스 §3 말미(repo `AGENTS.md` + `{.claude,.codex}/skills/{spec-create,spec-upgrade}/references/agents-harness-template.md` 4벌, verbatim 동일 각 +2줄)에 경량 경로 규칙 문단 추가 — 성질 3조건(① 새 contract/invariant 없음 ② 신규 파일 없음(work log 제외) ③ 전파 표면 전수 열거 + diff/grep 검증) 전부 충족 시 풀 체인 대신 직접 구현→검증→spec-sync 허용. 하나라도 아니거나 애매하면 풀 체인 기본값이고, 새 계약·agent 반환 형식·dispatch 구조 변경·rename/전파류(census)·신규 skill/agent는 항상 풀 체인이다. 경량이어도 브랜치·Execute→Verify·spec-sync·work log 생략 불가 + 판정 근거 1줄 work log 기록. 템플릿 4벌 포함으로 앞으로 `spec-create`/`spec-upgrade`가 초기화하는 모든 소비 repo의 하네스에 적용된다. `main.md` §2 Guardrails에 결정 승격(v4.6.30 회차의 ad-hoc 관행을 명문화).
- **검증 evidence**: git diff 5표면 +10줄(각 +2, 삭제 0, §3 구간 내부 한정, 문면 verbatim 동일 — diff 3쌍 무출력 + §3 구간 추출 비교); structural check `check_lightpath.sh` RED(T1-AC1 12요소 + T3-AC3 의도표면 5 누락 FAIL) → GREEN **11 PASS**, 변이 5종(구간밖 편집·미러 단어 변경·목록밖 잔존·새 §섹션·hook 임베딩) 전량 검출; plan-review 게이트(3-dispatch) 검증 131s ∥ 전제 149s ∥ 판단 71s(벽시계 ~149s) — High 1(census allowlist가 PR #42 spec 이력 표면 누락)·Low 2 전량 반영; implementation-review 게이트(N+2=5) correctness 3-shard 72/67/113s 전 AC MET ∥ simplicity 참조 53s·국소 71s — C/H/M **0**, Low 1(census 패턴 `lightpath` 붙임 변형 미커버, 실질 영향 0, advisory 잔존). **simplicity 반환 다이어트 첫 관측(n=1)**: 시간 대폭 감소(참조 279→53s·국소 147→71s), 비-finding 열거 단락 잔존 — 2기준 중 1개 충족, 판정 유보·누적 계속(🚧 Planned 항목 갱신).

#### v4.6.30 (2026-08-03)

- **게이트 finding 과다 시 재리뷰 권고 메시지 (post-implementation sync, 경량 경로)**: `feature-draft`·`implementation` 품질 게이트에 advisory-only 권고 규칙 추가 — finding 반영 후, 게이트 반환의 합산 finding(fix 전 기준; `implementation-review`는 shard 합산 요약 그대로 dedup 없음; Low 제외)이 **Critical+High ≥ 3 또는 Medium ≥ 5**였으면 마감 메시지에 수치와 함께 해당 게이트(`plan-review`/`implementation-review`) 1회 추가 실행 권고 1줄을 출력한다. 권고 출력만 하고 추가 리뷰를 자체 실행하지 않는다 — 단일 패스·fix 1회·무승인 불변식 불변, 셈·출력 주체는 producer SKILL 메인 루프(reviewer agent 계약 무변경).
- **검증 evidence**: git diff 4파일 +4/-2(`.claude`/`.codex` × `feature-draft`/`implementation` SKILL.md), 미러 문면 동일 diff 확인. draft 없는 경량 경로(사용자 합의) — advisory 문구 몇 줄이라 draft/게이트 생략.

#### v4.6.29 (2026-08-01)

- **simplicity 반환 다이어트 — plan-review 울타리 규칙 이식 (post-implementation sync)**: `simplicity-review-agent` 미러 2벌(각 +3/-1)의 Step 4 반환에 울타리 규칙 1문장 추가 — **확인했으나 finding이 아닌 스캔 결과는 열거하지 않는다, 반환은 위 항목이 전부다**. 차원 한정 여부와 무관한 무조건 규칙이며, 줄이는 것은 출력이지 Step 2 스캔 범위가 아니다. 규칙 준수는 새 AC 대신 기존 자체 검증 `AC3`에 흡수했다(범위 한정어 "Step 4 항목 밖에"). 채택 근거: simplicity는 반환 구조가 plan-review와 동형(`Findings` + 차원 판정 PASS 접기 + `Assumptions`)인데 울타리가 없었고, 이번 implementation-review 게이트에서 구계약 reviewer들이 실제로 "스캔 요지" 비-finding 단락을 반환에 실어 습성의 실재가 확인됐다. `implementation-review-agent`·`pr-review-agent`는 Verification ledger(MET 행 증거 결속) 계약이라 제외 — ledger 예외 문장이 필요한 별도 feature로 파킹(사용자 결정).
- **검증 evidence**: structural check RED 4 FAIL → GREEN 9 PASS, 변이 7종 전량 검출; implementation-review 게이트 finding 0 (correctness 97s ∥ simplicity 참조 55s ∥ 국소 57s). **부수 실측 — plan-review 다이어트 첫 관측(발효 후 첫 게이트)**: 실측 렌즈 114s ∥ 판단 72s, 실측 절대값 역대 최저, 열거 섹션 소멸(압축 요약 1문장 잔존) — 긍정 신호, n=1 누적 계속. **simplicity 다이어트 자체 효과는 미관측(발효 전)** — 첫 관측은 머지 + 플러그인 갱신 후 다음 implementation-review 게이트다.

#### v4.6.28 (2026-08-01)

- **plan-review 반환 다이어트 (post-implementation sync)**: `plan-review-agent` 미러 2벌의 `Step 6: Return`이 **확인했으나 finding이 아닌 대조 결과를 열거하지 않는다** — 반환은 명시된 4개 항목(`Blocker Status`·`Findings`·`규모 판정 검사 결과`·`Smell 판정`)이 전부다. 호출자 렌즈 한정 여부와 무관한 무조건 규칙이며, 줄이는 것은 출력이지 `Step 3` 대조 범위가 아니다. 규칙 준수는 새 AC 대신 기존 자체 검증 `AC5`에 흡수했다. 렌즈 구조(실측 ∥ 판단 2-렌즈)·6-smell rubric·severity·`plan-review` SKILL 미러 4벌은 무변경이다.
- **채택 근거**: 게이트 시간의 54~68%가 반환 작성이고 그 상당 부분이 판정 무기여 확인 목록이었다. 같은 목표를 실측 렌즈 묶음 분할(검증 ∥ 전제, 3-dispatch)로 치려던 대안은 구현 완료 후 **커밋 전 전량 되돌렸다** — 벽시계 353s(재고 밴드), shard 합 738s로 총량 보존 첫 붕괴, 검출 품질 개선 근거 없음, 계약 표면만 증가. 부풀림의 원인은 분할이 아니라 반환 습성이었다.
- **검증 evidence**: plan-review 게이트(다이어트 미적용 대조 표본 4) 실측 131s ∥ 판단 93s, 벽시계 131s; 구현 게이트 correctness 221s ∥ simplicity 126s ∥ 79s, 벽시계 221s, Critical·High 0 / Medium 1 fix(AC5 범위 한정어 보강); structural check RED 4 FAIL → GREEN 9 PASS, 변이 7종 전량 검출. **다이어트 효과 자체는 미관측** — 첫 관측은 발효 후 다음 feature의 plan-review 게이트다.

#### v4.6.27 (2026-07-31)

- **Codex investigate intent boundary (post-implementation sync)**: 모호한 `investigate`·`debug`·`diagnose` 요청은 diagnose-only로 잠그고, 조사 대상 제품·소스의 fix·repair·patch·수정 명시 또는 후속 승인 때만 fix mode로 전환한다. 진단 보고서·분석 산출물 작성은 제품 fix 권한이 아니다. diagnose-only는 Fix & Verify를 건너뛰며 제품·소스·spec fix와 회귀 테스트 추가를 금지한다. mandatory governance write만 정확한 대상·append semantics를 지키고 보고하는 예외다. fix mode의 blast-radius/fresh-verification과 기존 runtime/fan-out guard는 유지한다. **Codex-only 변경이며 Claude mirror parity는 주장하지 않는다.**
- **검증 evidence**: implementation review finding Critical 1 + High 2 + Medium 1을 fix 1회로 해소; runtime fixture work-log replacement 발견 후 append-only exception 강화; fresh isolated Codex CLI 0.146.0 smoke exit 0, product manifest·other work-log 불변, current work-log byte-prefix append-only, exact markers/governance report status 0.

#### v4.6.26 (2026-07-31)

- **Codex subagent dynamic model override (post-implementation sync)**: `plan-review`, `implementation-review`, `pr-review` 3종이 `--model`·`--effort`를 고정 repository allowlist가 아니라 선택된 active `spawn_agent` schema의 model·reasoning-effort enum으로 검증한다. 요청 field가 없거나 값이 unsupported면 dispatch 전에 차단하고 노출된 허용값을 보고한다. 유효 override는 모든 reviewer에 균일 적용하며, 생략값 상속과 model/effort 분리 계약을 유지한다. `gpt-5.6-sol`·`gpt-5.6-terra`, effort `low`·`max`·`ultra`는 현재 관측 예시이지 persistent contract가 아니다.
- **검증 evidence**: Desktop model·effort edge combinations 완료; CLI 0.146 smoke exit 0 + `CLI_OVERRIDE_SMOKE_DONE` + model/effort markers; stale live values **0**, dynamic **3/3**, mutation **3/3**, hygiene pass.

#### v4.6.25 (2026-07-31)

- **Codex multi-agent dual-runtime adapter (post-implementation sync)**: Desktop/CLI surface 이름이 아니라 활성 tool schema가 lifecycle을 선택하도록 `.codex` dispatch 표면을 정렬했다. mailbox schema(Desktop·현재 CLI 0.146.0)는 invocation별 parent-tree 고유 `task_name` + `fork_turns: "none"` + target 없는 wait + no-close를 사용하고, legacy target/close schema는 target wait와 `close_agent`가 함께 노출된 경우에만 유지한다. schema가 없거나 모호하면 mandatory dispatch는 fail closed, optional helper는 inline fallback하며, 없는 lifecycle tool은 검색하지 않는다. 요청된 model/effort field를 활성 spawn schema가 지원하지 않으면 dispatch를 차단한다.
- **검증 evidence**: Desktop 2-reviewer plan-review 완료; CLI 0.146.0 mailbox plan-review exit 0 + `CLI_PLAN_REVIEW_DONE`; static census **12/12**, stale pattern **0**, TOML **5/5**, links/refs clean, mutation **4/4**.

#### v4.6.24 (2026-07-31)

- **spec-sync 표면 묶음 분할 dispatch — 본문 ∥ 기록, 첫 작성자 분할 (post-implementation sync)**: 리뷰 3종 병렬화(v4.6.21~v4.6.23) 후 최장 단독 구간인 spec-sync(실측 245~445s, 집필 ~50%)를 표면 묶음 2개로 분할했다. `spec-sync-agent` 미러 2벌에 `호출자 표면 한정` 절 — **본문 묶음**(live truth 갱신 + evidence 검증·승격) ∥ **기록 묶음**(`decision_log`·`changelog` append-only entry + `_processed_` rename). read-only reviewer가 아닌 **첫 작성자 분할**이며 안전 근거는 **쓰기 집합 서로소**(reviewer들의 "파일 안 씀"과 다른 새 근거). read-vs-rename 경합은 본문의 원/`_processed_` 양쪽 조회로 흡수. `spec-sync` SKILL 미러 2벌은 orchestrator화 — implemented sync면 한 메시지 2 묶음 병렬 dispatch, 공유 사실(버전·delta·결정 제목)은 orchestrator **선고정**(두 shard가 각자 도출하지 않음), 사후 정합 grep 2종(버전 일치·append-only 삭제 줄 0, 비gating), 부분 Report 병합 relay(각 파트 정확히 한 묶음 소유). 기록 묶음은 digest 선고정 값 기반·코드 재검증 없음(재검증 중복 제거가 분할 이득의 절반 — 의도된 trade-off, 내용 오류는 후속 spec-review가 그물). 무조건 문구 전수 조건화 + 후방 호환(planned 경로 현행 1회·직접 호출 — pr-review 경로 아님).
- **적용 surface 검증 evidence**: structural check RED 선관찰 → GREEN **21 PASS / 0 FAIL**, 변이 9종 전량 검출. 게이트(N+2) 실측: correctness shard 185/87/181s + simplicity 참조 145s ∥ 국소 134s — 벽시계 **185s**. 게이트 finding High 1(rename 블록 무조건형 잔존 — census 단일 패턴이 '마킹한다' 변형을 놓친 위장 PASS) + Medium 4, 전량 fix. plan-review 2-렌즈 표본 2 = max 178s(지지 밴드). 벽시계 효과 첫 관측은 이 체인의 spec-sync 파일럿(수동 2-shard) — 결과 수치는 다음 sync에서 기록.

#### v4.6.23 (2026-07-31)

- **simplicity reviewer 차원 묶음 분할 dispatch — 참조 ∥ 국소, N+2 (post-implementation sync)**: 게이트의 다른 구간이 내려간 뒤 simplicity(실측 107~252s, 리포트 56~96%)가 임계 경로 후보 → 분할 축을 task가 아닌 **차원**으로 잡았다. `simplicity-review-agent` 미러 2벌에 `호출자 차원 한정` 절(참조 = 중복 코드·죽은 코드·단일 사용처 추상화 — 사용처/복제 추적형 / 국소 = 도달 불가 에러 처리·과잉압축 — 코드 자리 판독형, 합집합 = 정확히 5차원). **한정은 차원이지 범위가 아니다** — 각 shard가 전체 변경을 봐 중복 렌즈의 두 지점 동시 관찰이 유지되고 v4.6.21의 task 축 반대 논거와 공존한다(supersede 아님). 무조건 "5개" 문면 4곳(자체 검증 AC1·Hard Rule 3·Review Dimensions 도입부·Step 2)을 "소유한 차원"으로 일반화, Integration의 pr-review 서술은 "차원 한정 없는 호출 — 전체 5차원 후방 호환 경로"로 갱신(`pr-review` 무변경 동작). `implementation-review` SKILL 미러 2벌은 simplicity를 묶음마다 1회(총 2회) dispatch — correctness shard들과 한 메시지 **N+2** 병렬, relay 차원 판정 = 두 묶음 반환의 합집합(각 차원 정확히 한 묶음 소유). 게이트 fix로 근거 문장·payload bullet의 SKILL 재기재 제거(단일 소스 = agent 절/Runtime Adapter 블록).
- **stale 표면 정정**: `main.md` §2 implementation-review 불릿·직교 2-렌즈 결정 행의 "simplicity는 (항상/양쪽 모두) 통짜 1회" → 차원 묶음 2회 + pr-review 전체 5차원 1회(후방 호환) 구분 서술, relay (N+1)→(N+2)·차원 합집합 추가, 비분할 경로 (1+1)→(1+2). `components.md` implementation-review 행·Claude skill/agent split 행 동일 갱신.
- **적용 surface 검증 evidence**: structural check 게이트 fix 후 **20 PASS / 0 FAIL**(RED→GREEN), 변이 8종 전량 검출. 게이트 = N+2 완전체 첫 런: correctness 103/85/110s + simplicity 참조 164s ∥ 국소 91s — 벽시계 **164s**, simplicity 합 255s ≈ 동급 통짜 252s(총량 보존). 묶음 불균형 실측(중복 차원 집중 → 참조 shard 우세, 재배분은 실측 누적 후 별건). 🚧 Planned 갱신: plan-review 2-렌즈 첫 관측(실측 320s ∥ 판단 86s — max 320s, 재고 밴드 해당, n=1)을 기록하되 판정은 사용자 보고 후 결정 대기.

#### v4.6.22 (2026-07-31)

- **plan-review 2-렌즈 분할 dispatch — 실측 ∥ 판단 (post-implementation sync)**: plan-review는 유일한 무병렬 단독 리뷰 단계였고(5회차 실측 평균 ~294s, 최종 리포트 54~68%) finding이 섹션 교차·repo 대조형이라 task 축이 불성립(실측 9건 중 task 내부 닫힘 0건) → 분할 축을 렌즈로 잡았다. `plan-review-agent` 미러 2벌에 `호출자 렌즈 한정` 절(실측 = Step 3 계단 + `Verification Weakness` + draft 사실 주장 repo 대조·판단 렌즈 소유 smell의 사실 전제 포함 / 판단 = 나머지 5 smell + 규모 판정 검사 + Step 4, Step 3 미수행·draft 내부 근거·UNKNOWN 금지, 자체 검증 AC2·AC3은 판단 렌즈에만 적용, 미지정 시 6 smell 후방 호환). `plan-review` SKILL 미러 2벌은 thin wrapper → 2-렌즈 orchestrator(한 메시지 2회 병렬 dispatch + 병합 relay: 하나라도 BLOCKED면 BLOCKED·findings 합산·smell 판정 합집합·규모 판정 = 판단 렌즈, codex는 Runtime Adapter 블록 단일 소스). 단일 패스 불변(렌즈 2개 = 한 패스의 병렬 분해), 새 agent 없음.
- **실행 경제 guardrail fan-out 배제 supersede**: `main.md` §2 "해소 수단은 fan-out이 아니라 턴 접기다"를 "턴 접기(배칭)와 read-only reviewer fan-out"으로 정정 — 리포트-분할 메커니즘 검증(v4.6.21 1+N, 본 건)으로 read-only leaf reviewer 병렬 분해가 채택 레버가 됐다. 중첩 fan-out(nesting 1단계 제한)과 배칭 지시는 유지.
- **stale 표면 정정**: `components.md` plan-review 행 "wrapper -> agent" → orchestrator + 2-렌즈 서술, 잔존 wrapper-backed 목록 `spec-sync`만으로 축소. `main.md` 실행 분리·품질 게이트 소유권·2-렌즈 결정 행 갱신(1+N 첫 정식 런 벽시계 122s evidence 포함), 단일 패스 항 병렬 분해 단서, subagent model override 균일 적용 명시. `usage-guide.md` Scenario 2 게이트 문장 2-렌즈 병합 명시. 🚧 Planned: 벽시계 효과(기대 ~294s → ~200s)는 미관측 — 머지+플러그인 갱신 후 다음 draft의 plan-review 게이트가 첫 관측 지점.
- **적용 surface 검증 evidence**: structural check RED 11 FAIL → 게이트 fix 후 **21 PASS / 0 FAIL**, 변이 9종 전량 검출, 게이트(1+N 첫 정식 런) finding fix 2건(correctness Medium 1 + simplicity Medium 1), shard 2·3 finding 0.

#### v4.6.21 (2026-07-31)

- **implementation-review correctness task-shard 분할 dispatch — 1+N (post-implementation sync)**: 게이트 벽시계가 correctness 단독으로 결정되고(실측 214~430s, simplicity는 병렬 그늘) correctness 시간 분해(검증 루프 65~80% + 리포트 19~35%)가 task 경계로 나뉜다는 실측을 근거로, `implementation-review` orchestrator SKILL 미러 2벌에 분할 계약을 넣었다 — 기준 draft의 Part 2 task가 **2개 이상이면 correctness를 task별 shard로 분할 dispatch**(shard k digest = 공통 digest + Task k의 AC·Target Files 한정), simplicity는 통짜 1회(중복 탐지 렌즈는 두 지점을 같이 봐야 함), 전부 한 메시지 병렬, 비분할 경로(task 1개/draft 없음 → 1+1) 유지, 분할 상한 없음(YAGNI). relay는 correctness AC ledger의 shard 연접 + 모든 반환(N+1) 합산 severity, shard 간 중복 finding dedup은 fix 주체(호출자) 소관. codex는 3-way 적응(spawn_agent 어댑터 보존, 게이트 fix로 call 문법을 Runtime Adapter 블록 단일 소스화). reviewer agent 본문 무변경. **파일럿 실측(게이트 겸용)**: shard A 70s ∥ shard B 143s ∥ simplicity 120s — 벽시계 **143s**, shard 합 213s ≈ 동급 단독 correctness 214s(비례 분배 지지 밴드 통과).
- **stale 2-렌즈 서술 정정**: `main.md` §2 "직교 2-렌즈 review의 현재 적용 지점은 PR review"를 두 곳(PR review + implementation 마감 게이트)으로 정정하고 implementation-review의 1+N 계약 불릿 추가, 실행 분리·2-렌즈 결정 행에 implementation-review orchestrator 반영("(implementation gate 적용분은 F2에서 제거)" 잔존 서술 제거). `components.md` — implementation-review 행 "wrapper -> agent" → orchestrator + 1+N 서술, Claude skill/agent split 행의 wrapper-backed 목록에서 implementation-review를 orchestrator 목록으로 이동. `docs/AUTOPILOT_GUIDE.md` ko/en "2-reviewer" → "correctness shard N ∥ simplicity"(feature 직접 소유분). `usage-guide.md` 무변경.
- **적용 surface 검증 evidence**: structural check RED 17 FAIL → fix 후 **18 PASS / 0 FAIL**, 변이 7종 전량 검출, repo-wide 고정 표기 census(git 추적 파일) 정당 잔존 목록 밖 0건, 게이트 finding: correctness shard 0 + simplicity Medium 1 → fix 1, 전 AC MET.

#### v4.6.20 (2026-07-31)

- **커버리지 델타 절 후속 정정 4건 (post-implementation sync)**: 머지된 커버리지 델타(v4.6.17) 사후 감사에서 나온 정합 갭 4건을 `implementation` SKILL 미러 2벌에서 고쳤다. 규칙 방향은 유지하고 문면만 정정했다. ① **순서 절을 §4 → 마감 §3으로 이동**(추가 아님) — §4는 **적용 대상**만 소유하고 `fix → 델타 → 회귀 재실행` **순서**는 그 순서를 집행하는 마감 절이 소유한다. 순서를 서술만 하는 절에 두면 마감을 순차 집행하는 메인 루프에 §4로 되돌아갈 트리거가 없다. ② **폐기된 `(c)` 기준선 교체** — `(c) 근거가 덮지 못하는 동작`은 정의되지 않은 척도였다(§1의 `(c) 근거`는 분류 근거 1줄이지 커버리지 척도가 아니다). `(c)로 분류한 task도 이 단계를 건너뛰지 않는다 — 도달 테스트/check가 0개이므로 diff 동작 전량이 열거 대상`으로 교체(오해 부정 + 열거 기준 동봉). ③ **삭제 경로 재검증 신설** — 삭제했으면 **(a)/(b) task는** 그 task의 테스트/check를 다시 실행해 통과를 재확인하고 출력을 갱신 캡처한다(증거 테이블의 GREEN 증거 = 삭제 이후 출력, 재확인 실패면 삭제를 되돌려 남기기 경로로 닫음). 테스트 추가 경로만 변이 확인으로 판별력을 강제하던 비대칭을 닫으며, 안전망인 마감 회귀는 조건부라 (b) structural-check task를 덮지 못한다. (a)/(b) 한정이 핵심 — (c)는 실행할 테스트가 없어 무범위면 공허한 의무가 된다. ④ **§4 첫 문단 불릿화** — 주 지시문(diff 실행, 동사형)은 불릿 밖, 부속 규칙 4개를 각 한 줄로 분리(§2 RED·§3 GREEN과 동형). 문장 삭제 없음.
- **회귀 의무 범위 정정 (구현 중 결함 → 게이트에서 재정정)**: 마감 §3에서 회귀 재실행 의무가 `fix로 구현이 바뀌었으면` 조건에 갇혀 문서·테스트만 고친 fix가 회귀를 건너뛰는 협소화가 생겼고(§4 커버리지 델타가 잡음 — 그 절의 두 번째 실사용), 게이트에서 그 정정 문장의 역참조(`재실행하고 … 그 전에`)가 다시 지적돼 **선형 한 문장**으로 재배치했다 — `fix가 있었으면 그 fix diff에 §4 커버리지 델타를 먼저 적용한 뒤 회귀를 1회 재실행하고, 증거가 바뀐 AC는 증거 테이블을 갱신한다`. 델타 선행은 fix diff 한정, 회귀는 fix 전체에 걸린다.
- **적용 surface**: `main.md` — 헤더 4.6.20, §2 커버리지 델타 하위 항목(삭제 재검증 + 소유권 분할 + `(c)` 기준선 폐기)과 마감 순서 항(델타 선행 단계 + 회귀 범위 + 순서 명제 단일 소유자). `components.md` — `implementation` 행의 폐기된 `(c)` 기준선 교체 + 삭제 재검증 + 마감 계약 열거의 델타 선행. `usage-guide.md` 무변경. 검증 evidence: structural check RED 11 FAIL → GREEN **19 PASS / 0 FAIL**, 변이 누적 10건 전량 검출 후 복구·재실행 통과, `git diff --check` clean, 미러 `diff` exit 0, 게이트 1회(correctness Medium 2 + simplicity Medium 2 → fix 4, Blocker 0).

#### v4.6.19 (2026-07-31)

- **배칭 규칙 첫 처치군 관측(음성) — 행동 효과는 계속 미검증 (계측 sync, 코드 변경 0)**: `f1c2fbd` 머지로 플러그인이 갱신돼 규칙이 발효된 상태(설치본 5/5)에서, 배칭과 무관한 대상(커버리지 델타 PR#32 사후 감사)으로 게이트 2종을 돌려 첫 처치군 데이터를 얻었다 — v4.6.18이 명문화한 계측 전제조건(푸시 후 갱신 + 배칭 개념이 digest에 없는 새 세션)을 처음 충족한 회차다. 결과: **규칙 ON에서도 최대 연속 실행 길이 1**로 OFF 회차와 동일(OFF 4회차 1 / `plan-review` OFF 회차만 2). 지표는 양성 대조로 재검증했다(`plan-review`의 연속 2는 같은 assistant 메시지에서 `Glob` 2개가 나가고 결과가 함께 돌아온 진짜 배칭). draft AC의 비대칭(양성=정합 / 음성=반증)대로 음성은 n=1에서도 반증력이 있어 **규칙이 문면으로만 남았을 가능성**을 기록하되, 되돌리지도 강화하지도 않고 무관한 과제 2~3건을 더 쌓아 판정한다.
- **도입 근거 정정 (실측 반증, 이 단위의 핵심)**: correctness agent의 `Bash` 호출은 규칙 OFF·ON 양쪽 모두 **100% 복합 명령**(`&&`·`;`·`|`)이었다(12/12·16/16, 첫 호출부터 `git status --short && git log --oneline -3 && git diff --stat`). 즉 agent는 이미 셸 체이닝으로 압축하고 있었고 multi-tool 배칭의 실제 여지는 셸로 엮을 수 없는 `Read` 5회뿐 — 28~35턴 중 4턴 남짓이다. v4.6.18 도입 근거의 "앞 9개가 서로 독립인데 한 개씩 냈다"와 "17콜 → 5~6라운드" 추정은 **호출 수만 세고 호출 안의 내용을 보지 않은 판단**이었다. 일반화: *tool 호출 수는 배칭 여지의 대리지표가 아니다*. append-only 원칙에 따라 v4.6.18 entry는 수정하지 않고 신규 entry가 참조·정정한다.
- **A/B 불가 확정 → 누적 관측이 유일 설계**: 활성 플러그인 설치본이 시점당 하나뿐이라 처치군·대조군 동시 실행이 원리적으로 불가능하고, 대조군 회차 자체에 변동이 있어 n=1 arm 비교는 무의미하다. 이 제약은 배칭 feature 전용이 아니라 agent 행동 변경 일반에 걸린다.
- **적용 surface**: `main.md` — 헤더 4.6.19, §3 현재 운영 제약 **3개 항목만 수정**(plugin 캐시 지연 항목에 A/B 불가·누적 관측 / transcript 지표 항목에 호출 내용 계수 규칙과 정정 사실 / `🚧 Planned` 항목에 첫 처치군 음성 관측과 판정 설계). §2 Guardrails 배칭 하위 항목 **무변경** — 규칙 문면과 4요소는 그대로 발효 중이고 정정 대상은 규칙이 아니라 도입 시 추정한 여지의 크기다. `components.md`·`usage-guide.md` 무변경. agent·skill 자산 무변경.
- **미승격 (정직)**: 🚧 행동 효과는 여전히 미검증이며 `🚧 Planned`를 닫지 않았다. 절감 수치는 어디에도 기록하지 않으며, 이번 단위는 오히려 **초기 추정이 과장이었다는 정정**을 남긴다. 문면 강화 후보(추상 원칙 → "읽기 범위 계단 ①의 파일 `Read`는 한 메시지에" 같은 상황 지목형)는 효과 확인 전 착수 금지라 planned todo로 올리지 않고 decision_log Follow-up으로만 둔다.

#### v4.6.18 (2026-07-31)

- **agent tool call 배칭 — 병목은 dispatch 왕복이 아니라 턴 수만큼 반복되는 추론 (post-implementation sync)**: 2026-07-30 게이트 1회의 subagent transcript 계수(correctness 430s/17콜/31턴, simplicity 177s/3콜/7턴, **배칭 0회**)로 지연의 정체를 특정하고, agent 5종 × claude md/codex toml 10파일에 `tool call 배칭` Hard Rule 1개씩을 전파했다(번호는 파일마다 다르다 — 9/9/9/11/14). 필수 4요소 — (i) 서로 의존하지 않는 read-only 호출은 한 메시지에서 함께 낸다(**지시형**: repo 기존 배칭 문장이 전부 허가형이라 어미가 판정 조건이다), (ii) 앞 결과에 의존하는 호출만 다음 턴, (iii) 쓰기·상태 변경 호출은 배칭하지 않는다, (iv) **배칭은 읽을 대상을 늘리지 않는다**(v4.6.15·v4.6.16 입력 상한 잠식 차단). 주문장은 tool 이름 비의존이고 codex 미러만 `multi_tool_use.parallel`을 **조건형** 예시로 덧붙인다. `plan-review-agent` 짝에만 Step 3 도구 계단 절(4항목 뒤)에 "배칭은 같은 단 안에서만 한다" 1문장 — 계단 소유권을 계단 자신에 두고 Hard Rule에 복제하지 않는다. draft 범위 밖 확장 1건(사용자 지시): `implementation` SKILL `## 입력`의 한 문장이 재량(task 병렬)과 항상-이득(tool call 배칭)을 섞고 있어 둘로 분리했다 — 배칭은 지시형, task 병렬은 허가형 유지, `각 task 안에서는 RED→GREEN` 불변식 보존. 변경 12파일. 검증 evidence: structural check RED 23 FAIL → **73 PASS / 0 FAIL**, 변이 누적 12건 전량 검출 후 복구·재실행 통과, codex TOML `tomllib` 5/5, agent 10파일 삭제 라인 0, `git diff --check` clean, `implementation-review` 게이트 1회(correctness High 1 + Medium 1, simplicity Medium 1 → fix 3).
- **방법론 사실 2건(이 단위의 최대 수확) — 운영 제약 승격**: ① **plugin 캐시 지연** — dispatch되는 agent/skill은 작업트리가 아니라 plugin 설치본(pushed SHA)에서 로드된다(실측: 설치본 `fc8f1c9`에 이번 규칙 0/5, 전날 머지분은 1건 존재). 따라서 같은 세션의 마감 게이트로 자기 변경 효과를 계측하는 설계는 구조적으로 무효이며, 계측은 커밋·푸시 후 갱신 + 검증 대상 개념이 digest에 없는 새 세션을 전제조건으로 갖는다. ② **transcript 계측 지표** — JSONL은 한 메시지의 content 블록을 줄 단위로 쪼개 기록해 "메시지당 tool_use 수"가 항상 1이 되고 배칭을 원리적으로 탐지하지 못한다(15개 transcript 전량 max=1). 유효 지표는 **연속 실행 길이**이며 양성 대조(`plan-review` 회차 최대 2)로 검증했다. 같은 게이트에서 리뷰어 자기보고("한 메시지에 최대 4개")가 실측 1로 반증돼, 자기 행동 보고는 transcript 계수로 교차검증한다는 규칙도 함께 남겼다.
- **적용 surface**: `main.md` — 헤더 4.6.18, §2 Guardrails nesting 불릿에 하위 항목 **1개 추가**(턴 접기 · 배칭 지시형 4요소 · 읽을 대상 불증가 · 재량/항상-이득 분리 · tool 이름 비의존), §3 현재 운영 제약에 **3개 추가**(plugin 캐시 지연 / transcript 지표·자기보고 교차검증 / `🚧 Planned` 행동 효과 미검증). 새 guardrail 불릿·새 결정 테이블 행 없음. `components.md` — `plan-review` 행에 계단×배칭 제약 note 추가(단일 agent 계약 → `Repo-wide Invariant Test` #2 미통과라 reference surface). `usage-guide.md` 무변경.
- **미승격 (정직)**: 🚧 배칭 규칙의 **행동 효과는 미검증**이다. Task 3(행동 계측)은 위 plugin 캐시 지연으로 `UNTESTED`로 닫혔다 — 규칙이 로드되지 않은 실행은 규칙의 반증이 아니다. 절감 수치는 어디에도 기록하지 않으며, 전제조건을 갖춘 다음 회차에서 연속 실행 길이 ≥ 2로 확인한다.
- **기각·배제**: 모델·effort 티어 강등(사용자 실측 무효과, 재제안 금지), lite reviewer 신설(v4.6.15에서 기각 완료), 출력 다이어트 추가(1% 미만으로 측정 종료), 입력 상한 추가(배칭과 직교), 계측용 별도 재dispatch, `sdd-autopilot`·wrapper 스킬 본문(배칭 주체는 agent 자신), 도구 계단·읽기 범위 계단의 내용 변경.

#### v4.6.17 (2026-07-30)

- **`implementation` 커버리지 델타 — 테스트 집합을 AC의 함수에서 diff의 함수로 (post-implementation sync)**: "RED→GREEN으로 채우고 나면 빠진 테스트가 종종 보인다"는 문제의 원인이 체인 전체의 AC 앵커링(테스트 집합 = AC의 함수)으로 특정돼, `implementation` Process에 `### 4. 커버리지 델타`를 신설했다(기존 `테스트 불변 규칙`은 4→5 번호만 이동, 본문·`## 마감` 절 무변경). 규칙 6개 — ① GREEN 직후 이번 task가 변경한 diff를 **실제로 실행해 읽고** 통과시킨 테스트가 도달하지 않는 동작을 열거(기준점 = task 시작 시점, 커밋 경계 없으면 이번 task hunk 한정, (c) task는 (c) 근거가 기준선), ② AC도 요구하지 않고 기존 동작 유지에도 불필요하면 **삭제 1순위**(GREEN 최소성 — triage는 테스트 가능성만 묻고 존재 당위를 묻지 않아 §3 위반 코드가 테스트를 달고 고착되는 경로를 차단), 남는 항목만 기존 triage로 닫음, ③ RED 불가한 델타 테스트는 **변이 확인**(파괴 → 실패 관찰 → 복구 → 통과 재확인)으로 판별력 증명, ④ 테스트 불변 규칙 동일 적용 + "RED 재관찰"은 변이 확인 재수행으로 대체(대체 규칙 소유자는 델타 절), ⑤ 델타 테스트는 증거 테이블에 AC 유래 행과 같은 형식으로 싣되 **델타 0건이면 무출력**(형식적 통과 문구 표면을 만들지 않는 선택), ⑥ **마감 게이트 fix diff에도 적용**(draft AC 범위 밖 확장). 변경 2파일(claude/codex SKILL 미러 identical). 검증 evidence: structural check C0~C4 RED(C1 FAIL 헤딩 4개) → GREEN 전량 PASS, 변이 4건 전량 검출 후 복구·재실행 통과 재확인, `git diff --check` clean, 미러 `diff` exit 0, 게이트 1회(correctness Blocker 0 / Must 5 → fix 5 — §5 구제 경로 실행 불가·revision base 부재·fix 순서와 예산·§3 위반 코드 고착·(c) task 기준선 공집합, simplicity Medium 2 → fix 2 — negative 재천명 삭제·vacuous qualifier 제거).
- **실효 실증**: 직전 feature 커밋 `134854f`(AC 유래 check 47건)에 신설 절차를 회고 적용해 델타 2건(`git diff --name-only` 공집합 시 fallback, "참조된 spec은 필요한 절로 한정")을 열거했고 check 커버는 0건이었다. **둘 다 `implementation-review` fix로 들어온 동작** — AC 확정 뒤 태어나 AC 유래 테스트가 구조적으로 없는 부류이며, 이것이 규칙 ⑥의 근거다.
- **적용 surface**: `main.md` — 헤더 4.6.17, §2 test-first 불릿의 순서 열거를 `triage → RED → GREEN → 커버리지 델타 → 마감`으로 갱신 + 하위 항목 **1개 추가**(단계 정의·삭제 1순위·변이 확인·fix diff 적용·무출력 trade-off·GREEN 직후 위치 근거), 테스트 불변 규칙 하위 항목에 델타 적용과 RED 재관찰 대체 추가, §3 결정 표 `implementation test-first` 행 갱신(현재 선택 + 유지 이유). `components.md` — `implementation` 컴포넌트 행에 델타 mechanics note, Strategic Code Map `Implementation contract` 행 열거 갱신(이 행이 전파 표면에서 누락돼 있던 것을 plan gate가 발견). `usage-guide.md` 무변경 — `RED→GREEN`은 축약 표기라 델타 추가 후에도 참이다.
- **기각·배제**: 중단·분할 규칙에 "델타가 반복적으로 크다 = 계획 문제" 신호 추가(YAGNI — 미관측 실패 모드 + 기존 규칙 2가 이미 커버), `## 마감` 절 편집(증거 테이블 스키마 무변경 → 신설 절 1문장으로 수용, 편집 표면 최소화), `implementation-review`에 델타 렌즈 얹기(v4.6.16 읽기 범위 계단 원칙과 정면 충돌 + fix 1회 타이밍이 늦음), 마감으로 미루기(전체 GREEN 후라 코드 보고 짜맞춘 테스트가 됨), 새 agent·파일·artifact.
- **accepted trade-off (정직)**: 무출력 설계의 대가로 이 단계의 **스킵과 0건이 사후 구분되지 않는다** — 수행 흔적이 없고 `implementation-review`도 AC ledger 기반이라 수행 여부를 볼 수 없다. 강제력은 diff 실행 행위 의무와 델타 발견 시 증거 테이블 노출에만 의존한다.

#### v4.6.16 (2026-07-30)

- **`implementation-review` 읽기 범위 계단 — 입력 상한의 형태를 렌즈에 맞춘다 (post-implementation sync)**: 직전 단위의 계측(최종 리포트 = 전체 토큰의 4% → 출력 다이어트 절감 1% 미만, 일의 양을 깎는 레버는 입력 상한뿐)에 따라 상한을 `implementation-review-agent`로 확장했다. 단 `plan-review`의 `Glob`→`Grep`→`Read`→`UNKNOWN` 도구 계단을 이식하지 않고 **읽기 범위 계단**을 세웠다 — correctness 렌즈는 코드 본문 `Read`가 로직 결함 탐지의 핵심 수단이라 도구 순서를 제한하면 검출력이 깎이므로, 도구가 아니라 무엇을 읽을지의 **범위**를 제한한다. ① 변경 집합(`git diff --name-only`, 워킹트리가 비면 `<base>..HEAD`/`git log`) + draft/plan `Target Files` + 기준 문서(참조 spec은 AC·정합 판정에 필요한 절로 한정)는 전문 Read 상한 없음 + 로직 결함 능동 검토 결속 + 단일 패스 초과 시 우선순위 읽기와 limitation 명시, ② 인접 표면(호출·import, claude↔codex 미러 짝, wrapper↔agent 포인터, spec surface)은 `Grep` 우선, ③ 그 밖은 탐색적 읽기 금지(단 AC가 명시적으로 요구하는 증거는 범위 밖이라도 확보, 못 대면 `UNTESTED(범위 밖)`). Error Handling `대규모 코드베이스` 행은 ①의 초과 대응 포인터로 축약됐고 기존 degradation 능력은 삭제가 아니라 ①로 **이전**됐다. 변경 2파일(claude md + codex toml, payload 동일). 검증 evidence: structural check 47 PASS/0 FAIL(RED 34건 관찰), 변이 테스트 12건으로 check 판별력 증명, `implementation-review` 게이트 1회(Blocker 0 / Medium 4 → fix 4 — 모드 커버리지 갭·spec 범위 무한정으로 인한 목적 역행·커밋 후 ① 공집합·위장 PASS 4건) + `simplicity-review` Medium 5 → fix 3·반려 2, fix 후 회귀 47 PASS + 변이 전량 재검출, `git diff --check` 무출력, codex TOML `tomllib` 파싱 + `Codex Agent Boundary` delta 보존.
- **적용 surface**: `main.md` — 헤더 4.6.16, §2 Guardrails reviewer 불릿에 하위 항목 **1개 추가**(입력 상한은 걸되 형태는 렌즈에 맞춘다 / 상한은 검토 의무를 낮추지 않는다 / 규칙 소유자는 각 agent Step 3 / `pr-review` 비대상·`simplicity-review` 미적용). 계단 **상세**는 본문이 아니라 `components.md` `implementation-review` 행 note에 두었고(단일 agent 계약 → `Repo-wide Invariant Test` #2 미통과), 같은 행 Primary Source에 누락됐던 codex 짝 2개(`.codex/agents/implementation-review-agent.toml`·`.codex/skills/implementation-review/SKILL.md`)를 추가했다. `usage-guide.md` 무변경. 직전 v4.6.15는 도구 계단을 `components.md`에만 두었는데, 이번 두 번째 적용으로 "형태를 렌즈에 맞춘다"는 판단이 reviewer 2종에 걸쳐 #2를 통과해 형태 일반화만 본문으로 올라갔다(계단 mechanics는 여전히 reference surface).
- **기각·배제**: `pr-review` 상한 추가(사용자 명시 — 인간 리뷰 보조라 시간을 들이는 편이 낫다), `simplicity-review` 상한(요청 범위 밖), **검증 예산(깊이) 제한**(판별력과의 직접 맞교환 — 이번에 잡힌 위장 PASS 4건이 깊이 판 대가라 별도 판단 필요), model/effort 티어 변경(사용자 실측 무효과, 재제안 금지), `plan-review` 도구 계단 재작성(직전 단위 완료). agent AC 절·Hard Rules·`기준 문서 적응`·Findings Classification·반환 형식(ledger 포함)·tools frontmatter는 불변이다(보호 섹션 sha256 대조로 증명).
- **효과 기록(정직)**: 이 단위의 확정 효과는 절감 수치가 아니라 "무제한 재량을 상한으로 대체"다. ②③ 억제의 절감 규모는 **미측정**이며 다음 `implementation-review` 1회의 tool call 구성으로 사후 실측한다.

#### v4.6.15 (2026-07-30)

- **reviewer 반환 출력 다이어트 + `plan-review` 읽기 입력 상한 (post-implementation sync)**: 체감 지연의 지배 요인이 subagent 호출이 아니라 리포트 **작성(추론)** 이라는 실측에 따라, 계약·rubric·severity는 불변으로 두고 정보를 더하지 않는 출력과 무제한으로 열려 있던 입력만 걷어냈다. (1) `implementation-review-agent` 반환에서 task/AC 상태 요약(`Progress Overview`)을 삭제 — `Verification ledger`에서 도출되고 relay 소비자도 없다(반환 항목 6 → 5). (2) `plan-review-agent` 6 smell·`simplicity-review-agent` 5 차원의 판정 표를 "문제 있는 항목만 개별 행 + 나머지는 `PASS: <이름 나열>` 한 줄 접기"로 교체(점검·스캔 의무 유지, 출력 의무만 완화). (3) `plan-review-agent`의 "필요한 범위만 읽는다" 재량을 `Glob`→`Grep`→`Read`→`UNKNOWN` 도구 계단 + 정지 규칙으로 대체하고 규칙 소유를 Step 3 한 곳으로 모았다. 변경 10파일(agent 3종 × claude md/codex toml + wrapper SKILL 4벌). 검증 evidence: structural check 66 PASS/0 FAIL(초기 28 FAIL RED 관찰), census 5종 전부 0건(`6행`·`5행`·`Progress Overview`·`필요한 범위만 읽는다`·`어느 쪽에도 없는`), 미러 3쌍 payload 동일 + codex TOML `tomllib` 파싱 및 적응 delta 보존, `git diff --check` 무출력, `implementation-review` 게이트 1회 + fix(correctness Blocker 0 / Medium 4 → fix 4, simplicity Medium 2 → fix 2).
- **적용 surface**: `main.md` — 헤더 4.6.15, §2 Guardrails reviewer 불릿에 하위 항목 **2개 추가**(반환 항목은 wrapper relay 소비 실측으로 유지/삭제를 판정한다 + 판정 표는 PASS 접기로 내고 완전성 불변식은 각 agent AC 절 한 곳이 소유한다). 새 guardrail 불릿·새 결정 테이블 행 없음 — reviewer 반환 계약의 판정 주체가 이미 그 불릿이다. `components.md` — `plan-review` 행에 읽기 계단 입력 상한 note 추가(단일 agent 계약이라 `Repo-wide Invariant Test` #2 미통과 → 본문 아닌 reference surface). `usage-guide.md` 무변경(반환 항목을 열거하지 않는다).
- **선행 결정 부분 대체**: 2026-07-10 결정 #6의 "`implementation-review-agent` §2 `Progress Overview`를 task/AC 상태로 **제약**" 조항은 이번 단위의 **삭제**로 대체됐다 — 제약된 형태에서도 `Verification ledger`와 정보가 겹치고 relay 소비자가 없다는 사실이 그때 확인되지 않았다. 같은 결정의 finding ID 블록화·Recommendations ID 갈음·Conclusion 삭제 조항은 유효·무변경이다.
- **기각·불변**: lite review agent 신설(계약 복제 → claude/codex 짝 propagation 부담으로 환전, 이 repo의 반복 실패 모드), model/effort 티어 강등(사용자 실측 무효과, 재제안 금지), Medium finding 블록 강등(메인 루프 fix 1회의 입력이라 fix 정확도 손실 — reviewer 4종 모두 현행 유지), `Read` 전면 금지(`Verification Weakness` smell 판별력 소실 → 금지가 아닌 계단). `pr-review-agent`는 본문 무변경이고 `Correctness 신호`는 통합 리포트 `Signals` 줄이 소비하므로 유지 대상이다. 6 smell/5 차원 정의·severity 기준도 무변경이다.

#### v4.6.14 (2026-07-29)

- **하네스 실행 자산에 재주입 방향 추가 — 훅 자산 2개 → 3개 (post-implementation sync)**: `harness-context.sh`(SessionStart, `matcher: "clear|compact"`)가 기존 `worklog-gate.sh`·`worklog-context.sh`와 같은 설치 계약(verbatim 복사 + `settings.json` 키 수준 멱등 병합 + 하네스 설치와 동일 조건, opt-in 아님) 아래 편입됐다. compact·clear 뒤 `CLAUDE.md` 포인터만 재주입되고 하네스 본문이 사라지던 실패 모드를 실행 층으로 닫는다 — 재주입은 "읽으라는 지시"가 아니라 `AGENTS.md` 전문의 내용 주입이다. 설치 지시는 `spec-create` §3e / `spec-upgrade` Step 6에서 work log 전용 → 훅 자산 일반으로 확장됐다(별도 절 신설 없음 — 병합 규칙 판정 주체 단일 유지). 검증 evidence: structural check 29 PASS/0 FAIL + 변이 테스트 4건 전부 검출, **런타임 발동 관찰**(픽스처 repo 트랜스크립트에 `hook_success`/`hookName:"SessionStart:clear"`·`"SessionStart:compact"` + content에 픽스처 sentinel = 본문 전체 주입, `startup` 음성 대조 발동 0건, 리뷰어 독립 재현), `implementation-review` 게이트 1회 + fix 1회(correctness Blocker 0, 합산 Medium 7건 반영), 미러 md5(세 스크립트 각 4벌 1종, 두 SKILL.md claude↔codex 바이트 동일), `git diff --check` 무출력.
- **적용 surface**: `main.md` — 헤더 4.6.14, §2 Guardrails 하네스 설치 불릿 **확장**(훅 자산 3개 + 역할 열거로 개수 리터럴 갱신 / 계약이 훅 자산 일반에 적용 / SessionStart matcher가 스크립트별로 다르고 미지원 런타임에서 무증상 미발동할 수 있다는 announce 조항 — 새 guardrail·결정 행 없음), §3 핵심 설계 harness 문단에 실행 자산의 **두 방향**(강제 / 사라진 규약 복구)과 "지시가 아니라 내용 주입" 근거 추가. `components.md` — Platform Notes 훅 3개·재주입 비대칭, Strategic Code Map `references/hooks/` 행에 `harness-context.sh` 역할 추가. `usage-guide.md` — Scenario 1 훅 산출물 불릿 세 스크립트화 + 관찰 결과에 clear/compact 재주입·`startup`/`resume`/`fork` 미발동 명시.
- **선행 planned 종결**: v4.6.13이 `🚧 Planned`로 고정한 `docs/SDD_CONCEPT.md` §1(ko·en) drift는 이번 feature Task 5에서 레이어 표 행 + 문단 양쪽이 ko/en 대칭으로 갱신돼 종결됐다(잔여 planned 없음).
- **불변**: 하네스 템플릿·`AGENTS.md` 무수정(훅 리드 1줄이 이미 "다시 읽지 말고 이대로 따른다"를 전달 — 템플릿에 중복 문장 금지), `§0~§5` 리터럴 변경 없음.

#### v4.6.13 (2026-07-29)

- **하네스를 문서 규약에서 실행 게이트로 확장 — work log 훅을 4번째 산출물군으로 편입 (post-implementation sync)**: `spec-create`·`spec-upgrade`가 소비 repo에 설치하는 하네스 산출물이 `AGENTS.md`·`CLAUDE.md`·`.gitignore` 3종에서 훅 자산군(`.claude/hooks/worklog-gate.sh`·`worklog-context.sh` + `.claude/settings.json` 등록)을 더한 4종이 됐다. 훅 설치는 하네스 설치와 동일 조건에 묶이며 opt-in이 아니다. 검증 evidence: 자체 structural check 29 PASS/0 FAIL(`jq`/`python3` 강제 마스킹으로 12케이스 × 2파서 = 24판정 동일, fail-open + 경고, exec bit 비의존, 하위 디렉토리 cwd 루트 고정), `implementation-review` 게이트 1회 + fix 1회(correctness Blocker 0 / AC 26 전부 MET, 합산 Medium 6건 반영) 후 회귀 29/29 유지, 미러 md5 실측(훅 4벌 + dogfooding 사본, 템플릿 4벌, SKILL.md claude↔codex 바이트 동일), `git diff --check` 무출력.
- **적용 surface**: `main.md` — 헤더 4.6.13, §2 Guardrails에 하네스 설치 계약 **새 불릿 1개**(4종 동일 조건 설치 / 커밋되는 `settings.json`이라 announce 필수 / 파서 부재 시 fail-open + 세션 경고로 조용한 무력화 금지 / 병합 규칙 canonical은 두 SKILL), §3 핵심 설계 harness 문단에 "규약 + 규약을 강제하는 실행 자산" 확장과 §0 네 원칙 이름이 `plan-review`의 `Principle Link` 앵커라는 사실 추가. 새 결정 테이블 행·중복 guardrail 없음(기존 workspace commit 경계 불릿과 판정 주체 분리). `usage-guide.md` Scenario 1에 훅 산출물 불릿(관찰 결과 + announce), `components.md` Platform Notes에 Codex 비대칭 행 + Strategic Code Map에 `references/hooks/` 정본 행.
- **하네스 템플릿 §0 교체(draft Part 1 밖 추가 delta)**: 개인 global CLAUDE.md 유래 산문 5줄 → 명명된 4원칙(`Think Before Coding`·`Simplicity First`·`Surgical Changes`·`Goal-Driven Execution`) + 흡수 조항 2개. 근거는 `plan-review-agent`가 인용하는 이름이 구 §0에 존재하지 않았고(`Goal-Driven Execution` 축 부재) 개인 협업 어투가 소비 repo로 배포됐다는 점이다. §5에는 게이트 존재·발동 시점·우회법 1줄만 추가해 섹션 수 §0~§5를 유지했다(`§0~§5` 리터럴 18건 무변경).
- **보류**: `docs/SDD_CONCEPT.md` §1(ko·en)이 하네스를 문서 규약 레이어로만 서술하는 drift는 `🚧 Planned`로 고정했다 — spec sync 대상은 `_sdd/spec/`뿐이며 ko·en 대칭 마감이 필요하다.

#### v4.6.12 (2026-07-27)

- **`SKILL.md` frontmatter `version:` 필드 삭제, 스킬 버전 소스를 0으로 (post-implementation sync)**: 직전 sync(v4.6.11)가 Open Question으로 남긴 "필드 자체 폐지"를 사용자가 판정해 실행했다 — `version:`의 소비자가 0이기 때문이다(두 런타임 바이너리 모두 `name`·`description`만 사용, `tools/install-codex-skill-bundle.py`는 `SKILL.md` 존재만 확인 후 디렉토리 통째 교체, `marketplace.json`은 디렉토리 경로 등록, `AGENTS.md`·`README.md`·`docs/`·agent 파일 참조 0건). `.claude/skills/*/SKILL.md` 21 + `.codex/skills/*/SKILL.md` 19 = 40파일에서 frontmatter `version:` 줄만 삭제(각 diff `+0/-1`). 잔존 키는 `name`·`description` + 런타임이 읽는 선택 키(`argument-hint`·`user_invocable`). structural check 8 PASS/0 FAIL + 회귀 13/0·77/0·39/0 + 40개 frontmatter 전수 파싱 실패 0 + live 표면 `^version:` 0건, 리뷰 게이트(correctness ∥ simplicity) 1회 + fix 1회(Critical/High 0).
- **적용 surface**: `main.md` — 헤더 4.6.12, §3 결정 테이블 `Skill 정의 형식` 행을 "스킬 버전을 담는 필드·파일은 두지 않는다(스킬 변경 이력 = git history)"로 **교체**(직전 sync가 고정한 같은 행을 다시 바꿈 — 새 결정 행·guardrail 없음), 유지 이유를 "사이드카든 frontmatter 필드든 소비자 없는 값은 두지 않는다"로 일반화하고 version lockstep 검사 대상 0을 명시. `현재 운영 제약`의 version 단일 소스 불릿은 **소멸**(치환이 아니라 삭제 — 대변하던 사실 자체가 사라짐), 하위 `🚧 Planned`(미러 본문 세대 격차)는 유지하되 version 재료를 걷어내고 본문 실측으로 재서술 + 최상위로 승격.
- **산문 참조 정리(판정 규칙)**: live spec 3파일의 스킬 버전 10줄 11토큰을 정리했다 — (i) 현재 계약 표기는 괄호째 삭제(`sdd-autopilot`(v4.0.0) → `sdd-autopilot`), (ii) 역사 앵커는 feature/사건 앵커로 치환(`v2.0.0에서 개명(F5)` → `F5에서 개명`, `v3.0.0에서 …가 됐다` → 현재형 계약 서술). 문서 자체 버전(`Spec Version`, AUTOPILOT_GUIDE `2.1.0`, marketplace 플러그인 `1.0.0`)과 `SKILL.md` 본문 보존 2건(`guide-create` 생성 템플릿, `git` 충돌 산문)은 범위 밖이다.
- **보류**: `user_invocable`은 삭제 대상이 아니다 — Claude Code 2.1.220 바이너리가 실제로 읽는다(문자열 2건 실측). 미러 본문 세대 격차의 canonical 방향은 여전히 미정(`🚧 Planned` 유지).

#### v4.6.11 (2026-07-27)

- **죽은 사이드카 메타데이터 `skill.json` 삭제, `SKILL.md` frontmatter를 version 단일 소스로 (post-implementation sync)**: 두 런타임 어느 쪽도 읽지 않던 `skill.json` 37개(`.claude` 19 + `.codex` 18)를 삭제했다 — 바이너리 문자열 실측에서 Codex CLI 0.142.5·Claude Code 2.1.220 모두 `skill.json` 0회 / `SKILL.md` 75회·222회. 읽히지 않아 감지되지 않던 version 불일치가 삭제 직전 12건 누적돼 있었고, 값 정렬(증상)이 아니라 파일 삭제(원인)로 종결했다. 함께 `.claude/skills/spec-snapshot/SKILL.md`에 `version: 1.2.0` 추가(삭제 전에도 version 소스가 0이던 유일 스킬), `_sdd/env.md` Runtime 절 작업 대상 목록에서 `skill.json` 제거. 변경 39파일. structural check 14 PASS/0 FAIL + 회귀 `check_gates.py` 79/0·`check_en_docs.py` 39/0 + 40개 SKILL.md frontmatter 전수 파싱 실패 0, 리뷰 게이트(correctness ∥ simplicity) 1회 + fix 1회(Critical/High 0).
- **적용 surface**: `main.md` — 헤더 4.6.11, §3 결정 테이블 `Skill 정의 형식` 행을 "frontmatter가 메타데이터 단일 소스, 사이드카 파일 없음"으로 확장(새 결정 행 없음 — 기존 결정의 실체 확정), `현재 운영 제약`의 version 불릿을 version 단일 소스 서술로 재작성하고 하위 `🚧 Planned`("`implementation-review` 4필드 불일치")를 **미러 본문 세대 격차**로 치환. `components.md`·`usage-guide.md` 무변경(`skill.json` 리터럴 0건).
- **planned 치환**: 지목 대상(`skill.json` `2.1.0`/`3.0.0`)은 소멸했으나 상위 사실("version 갱신이 편집 discipline 의존")은 유효하고 실례가 남아 있어 삭제가 아니라 치환으로 닫았다 — 미러 쌍 전수 대조상 live version 드리프트는 `guide-create`(`2.2.0`/`2.4.0`) 1건이고, `guide-create`·`spec-snapshot`은 본문 세대까지 갈려 있다(176/159줄, 135/118줄).
- **보류**: `version:` 필드 자체의 폐지(소비자 census 0)는 이번 sync가 고정한 "frontmatter = version 단일 소스"와 정면 충돌해 planned로 고정하지 않고 Open Question으로 남겼다. Codex 번들 검증기 허용 키 이슈도 근거가 추정 수준이라 동일 처리.

#### v4.6.10 (2026-07-26)

- **`docs/en` 미러 세대 drift 해소 (post-implementation sync)**: v4.6.9가 planned로 고정한 en drift를 종결했다. 단일 원인은 2026-06-12 하네스 레이어 도입의 en 미전파 — en `SDD_WORKFLOW`에 §2 "When the harness is used" 신설 + 기존 §2~§9 → §3~§10 재번호 + §1 flow를 producer 게이트 2행으로 + §4 temporary spec 3항목화, en `SDD_CONCEPT` §1에 `Harness (AGENTS.md)` 행·경계 문단 추가. 함께 CONCEPT ko·en temporary spec 행을 현행 draft 구조 어휘로(correctness M1), `temporary spec 또는/or feature draft` alternation 6곳을 canonical 등가 표기로(simplicity M3), QUICK_START ko·en의 죽은 `implementation plan` 참조를 `feature draft`로 정리. 변경 6파일(ko 3 + en 3, 전부 `docs/`). structural check 35 PASS/0 FAIL + 회귀 79 PASS/0 FAIL, 리뷰 게이트 1회 + fix 1회(Critical/High 0).
- **적용 surface**: `main.md` — 헤더 4.6.10, `현재 운영 제약`의 en drift `🚧 Planned` bullet을 ko/en 미러 대칭 마감 운영 제약 1줄로 대체(새 guardrail 없음 — canonical rollout 순서 결정의 enforcement로만 표현). `components.md`·`usage-guide.md` 무변경.
- **보류**: simplicity M1/M2(supporting doc 산문 중복·긴장)와 Low 3건은 repo-wide invariant 기준 미통과로 global spec에 planned 고정하지 않고 `decision_log`에만 남겼다.

#### v4.6.9 (2026-07-26)

- **SDD 체인 품질 게이트를 producer 스킬 소유로 고정 (post-implementation sync)**: `implementation`(v3.0.0)이 `implementation-review`를 "선택 — 강제 아님" 권유가 아니라 마감 강제 게이트로 소유한다(회귀 1회 → AC→증거 테이블 → 게이트 1회 + C/H/M fix 1회 + fix 후 회귀 재실행 → 게이트 finding·fix 내역을 실은 마감 요약, Low는 advisory). `sdd-autopilot`(v4.0.0) Step 2는 6항목 → 4항목(Draft / 구현 / Spec sync / 최종 보고)으로 축소돼 게이트를 재호출하지 않고 producer 반환을 최종 보고로 모은다. `plan-review-agent` 미러 2벌의 호출 주체를 `feature-draft`로 정정, 하네스 §3 5곳(`AGENTS.md` + `spec-create`·`spec-upgrade` 템플릿 claude/codex 4미러)에 게이트 예외 1줄 추가(체인 리터럴은 무변경), `docs/AUTOPILOT_GUIDE.md` ko/en 2.1.0. structural check 79 PASS/0 FAIL, 리뷰 게이트 통과(plan-review 1회 + implementation-review 1회 + fix 1회).
- **적용 surface**: `main.md` §2 Guardrails(게이트 소유권 불변식 + 전파 표면 5곳·`implementation` 마감 순서·autopilot v4.0.0 체인·분할 canonical 목록에서 `plan-review` 제외·plan gate optional 서술 정정) / §3 결정 테이블(`plan quality gate` → `품질 게이트 소유권`, 오케스트레이션·implementation test-first 행) / 현재 운영 제약(planned 2건 등록). `components.md` — `sdd-autopilot`·`implementation`·`plan-review`·`implementation-review` 행. `usage-guide.md` — Scenario 2 커맨드 목록·기대 결과, Scenario 2b Step 2.
- **planned 등록**: `docs/en/SDD_WORKFLOW.md`의 ko 대비 한 세대 drift(§2 누락 + full 레인 어휘 5곳), `implementation-review` version 4필드 불일치(`2.1.0`/`3.0.0` vs `7.0.0`).

#### v4.6.6 (2026-07-22)

- **F5 완료 — `-lite` 개명 승격, F1~F5 전체 완결 (post-implementation sync)**: 스킬 `feature-draft-lite`→`feature-draft`·`implementation-lite`→`implementation`(git mv 4디렉토리, name·version 2.0.0, marketplace 갱신, 미러 identical), 개념 어휘 ~40파일 교체("lite 체인"→"SDD 체인", `> Lite 적격:`→`> 규모 판정:` 소비자 3곳 동시, autopilot Step L→Step 2·AC-L→AC, lite 트리거 별칭 제거), draft 파일명 glob `*_feature_draft_*` 통일(구 lite 파일명 substring 호환), `docs/SDD_SPEC_DEFINITION.md` ko·en 현행 draft 형식 재작성(검증 rubric 사슬 유지, full 구조 어휘 legacy 한정). 개명 census live 표면 잔존 0, 리뷰 게이트 통과(correctness 전 AC MET, simplicity M2 fix).
- **적용 surface**: `main.md` §1~§3 — F5 todo 완결 승격 + lite 어휘·구명 전면 트림(F2 서술은 "당시 이름"으로 동명 현행 스킬과 구분). `components.md` — 개명 행·Strategic Code Map 경로·마커 앵커 갱신. `usage-guide.md` — Scenario 2/2b 커맨드·체인 서술 개명. F5 draft·분할 계획 원본 draft `_processed_` 마감.

#### v4.6.5 (2026-07-22)

- **F4 완료 — full 레인 삭제 완결을 current truth로 승격 + F5 개명 planned 등록 (post-implementation sync)**: 잔재 폐기(`_sdd/tests/` 20 check 스크립트, test-free triage 확대 draft), 이월 advisory sweep(fdl 쌍 description v1.2.0, impl-review description, AGENTS+하네스 템플릿 4미러 spec-sync 문장 5곳 동일, implementation-review-agent 쌍 Quick Review 섹션 소거, spec-sync·spec-review agent 쌍 입력/감사 계약 lite 기준 재서술 + legacy full 구조는 기록물 fallback 한정), codex pr-review sample 2-reviewer spawn 흐름 재작성, repo 전체 full 어휘 census 2계층(엄격 계층 live 표면 잔존 0 — AGENTS.md:17 re-review 잔재 적발·즉시 fix / 판정 계층 35파일 spot 판정). 리뷰 게이트 통과(correctness H1+M3·simplicity M3 합집합 fix). F5(`-lite` 개명 — 이름+개념 전부, 사용자 확정)를 새 🚧 Planned todo로 등록 — 구현 evidence 없음, PLANNED만.
- **적용 surface**: `main.md` §2 — F4 todo 소거·완결 승격, 🚧 Planned F5 신설, 개명 유보 문구 해소. §3 — 오케스트레이션·lite 규모 초과 대응 행 갱신. `components.md` — autopilot 행 F4 참조 소거, spec-sync·spec-review 행 lite 기준 계약 반영. `usage-guide.md` 변경 없음.

#### v4.6.4 (2026-07-22)

- **F3 완료 — reviewer 경량 반환 유일화를 current truth로 승격 (post-implementation sync)**: reviewer 4종 쌍(plan-review·implementation-review·simplicity-review·pr-review agent) 경량 반환 유일 mode 재작성(파일 mode·re-review·Tier·Output 파일 템플릿 삭제, tools `Write` 제거 — correctness·pr만 테스트용 Bash 유지), plan-review-agent full rubric 삭제(구 Tier 2-lite 내용이 유일 rubric, 명칭 소멸) + SKILL 쌍 3.0.0, implementation-review SKILL 쌍 7.0.0(경량/파일 분기 제거), pr-review 재설계 4.0.0(agent 경량 반환 + 스킬이 통합 리포트 `_sdd/pr/*_pr_review_*` 1파일만 작성 — 3파일→1파일), autopilot 쌍·GUIDE ko/en "Tier 2-lite" 소비자 정리. census(확장 패턴, 20파일) 잔존 0, 리뷰 게이트 통과(correctness C/H 0·M1, simplicity M6 fix 완료). F4 todo는 🚧 Planned 유지.
- **적용 surface**: `main.md` §2 — 단일 패스 invariant·reviewer read-only leaf invariant 승격, review guardrail "fix/re-review" 표현 정리, pr-review 2-렌즈 per-agent 리포트 경로 소거, F3 todo 소거(umbrella F4 갱신), plan-review gate 경량 반환 명시. §3 — 오케스트레이션·분할·plan quality gate 행 갱신. `components.md` — reviewer 3행 경량 반환 계약 재서술 + autopilot·feature-draft-lite 행 정리. `usage-guide.md` — plan_review 리포트 파일 서술 교체 + Tier 2-lite 표기 치환.

#### v4.6.3 (2026-07-22)

- **F2 완료 — full 전용 agent·스킬 삭제를 current truth로 승격 (post-implementation sync)**: agent 쌍 4종(`feature-draft-agent`·`task-ordering-agent`·`test-author-agent`·`implementation-agent`) 8파일 + 스킬 쌍 3종(`feature-draft`·`implementation`·`implementation-plan`) 6디렉토리 삭제, 등록 표면 lite 기준 정리(marketplace.json skills 21/agents 7, `.codex/agents/README.md`, README Subagent Model Override 목록 3종 축소), `implementation-lite` v1.2.0 일반 구현 트리거 흡수("병렬 구현" 폐기), AGENTS.md + 하네스 템플릿 4미러 SDD 흐름 lite 체인 갱신, `docs/en/AUTOPILOT_GUIDE.md` 2.0.0 재작성, dangling 참조 정리. census 잔존 = F3 소관 reviewer 쌍 + `SDD_SPEC_DEFINITION.md`(F4). 리뷰 게이트 통과(correctness 전 AC MET, simplicity fix 반영). F3~F4 todo는 🚧 Planned 유지.
- **적용 surface**: `main.md` §1 entrypoint 예시 / §2 F2 todo 소거·producer loop·test-first·2-렌즈·multi-phase ordering·feature-draft Part 2 guardrail lite 기준 재서술(test-first canonical = `implementation-lite` SKILL, 대체 안전장치 = 테스트 불변 규칙 + implementation-review Fresh Verification) / §3 삭제 컴포넌트 행 제거·갱신. `components.md` 삭제 행 4개 제거 + Code Map 재지정. `usage-guide.md` Scenario 2 수동 lite 체인 재작성.

#### v4.6.2 (2026-07-22)

- **F1 완료 — `sdd-autopilot` full 파트 제거를 current truth로 승격 (post-implementation sync)**: autopilot SKILL 쌍 v3.0.0 lite 체인 전용 재작성(Step 0 상태 확인 → Step 1 요청 분석 → Step L, orchestrator·Lane 판정·full 레인 서술 0, skill.json 쌍 동일), 부속 references/examples/scripts 쌍 삭제, `docs/AUTOPILOT_GUIDE.md` 2.0.0 재작성, 복구 보험 git tag `full-lane-final`(407e08e) 생성. census: autopilot 표면 full 어휘 잔존 0(허용 예외: GUIDE의 tag 복구 안내 1회), 삭제 자산 참조 잔존은 F2·F3 예정 표면 8파일 + 기록물뿐. 리뷰 게이트 통과(correctness C/H/M 0 전 AC MET, simplicity M2 fix 반영). F2~F4 todo는 🚧 Planned 유지.
- **적용 surface**: `main.md` §2 — autopilot bullet을 lite 체인 전용 current truth로 갱신, generated orchestrator guardrail 소거(plan-review handoff gate 삭제, canonical agent invocation은 skill 일반 규칙으로 재프레임), 공통 loop 정책 출처를 삭제된 `orchestrator-contract.md` §6에서 guardrail 본문 단일 소스로 이관, 🚧 Planned F1 항목 소거(umbrella todo는 F2~F4 잔여로 갱신). §3 — 오케스트레이션 행 갱신, "autopilot producer handoff gate" 행·generated orchestrator `implementation-dispatch-controller` 구조 판단 제거. `components.md` — `sdd-autopilot` 행 lite 전용 재작성, Code Map의 삭제 파일 2행(orchestrator contract·planning graph reference) 제거, stale autopilot 참조 2건 교정(implementation-plan gate source·test-author 호출 주체). `usage-guide.md` — Scenario 2b를 lite 체인 기준으로 재작성(full Expected Result·`_sdd/pipeline/` 산출물 서술 제거).

#### v4.6.1 (2026-07-22)

- **full 레인 삭제 확정 — 4-feature 분할 todo 고정 (pre-implementation planned sync)**: v4.6.0의 "🚧 Planned: full 레인 실체 삭제 — 다음 슬라이스" 단일 항목을 롤링 분할 draft(`2026-07-22_feature_draft_lite_full_lane_removal`) 기반의 개별 🚧 Planned todo F1~F4(F1 autopilot full 파트 제거 / F2 full 전용 agent·스킬 삭제+등록 정리 / F3 reviewer full 기계장치 트림 / F4 잔재 정리+최종 census)로 구체화·대체. 복구 보험은 삭제 직전 git tag `full-lane-final`. 구현 evidence 없음 — 전 항목 PLANNED, 승격 없음.
- **적용 surface**: §2 Guardrails 분할 todo 블록 신설, §3 오케스트레이션 행 marker 갱신, `components.md`·`usage-guide.md` marker를 §2 todo 참조로 갱신, decision_log entry 신설.

#### v4.6.0 (2026-07-22)

- **lite 레인 이탈 신호를 "full 승격"에서 "분할"로 교체 (post-implementation sync)**: `sdd-autopilot` 기본 레인이 lite fast-path(`feature-draft-lite` → `plan-review` Tier 2-lite → `implementation-lite` → `implementation-review` → `spec-sync` 메인 루프 체인)임을 spec에 최초 반영. 규모 초과의 해소 수단은 오케스트레이션이 아니라 분할이다 — lite 표면들은 full 전환을 안내하지 않고, 단일 컨텍스트 초과는 롤링 분할 draft + `spec-sync` planned todo(feature별 개별 `🚧 Planned`) + feature별 순차 lite 체인으로 해소한다. 분할 판정 canonical은 lite 표면 소유(autopilot은 신호 소비만), census형 sweep은 분할 신호가 아니라 마지막 read-only 검증 task로 흡수. full 직행은 사용자 명시 요청만 한시 잔존하며 full 레인 실체 삭제는 🚧 Planned(다음 슬라이스).
- **적용 surface**: §2 Guardrails lite 레인 bullet 신설, §3 오케스트레이션 행 갱신 + "lite 레인 규모 초과 대응" 행 신설, `components.md` lite 스킬 2행 신설·`sdd-autopilot` Notes 갱신, `usage-guide.md` Scenario 2b 노트. 구현은 draft `2026-07-22_feature_draft_lite_escalation_to_split`로 선행 완료(correctness review AC 전부 MET, 승격 어휘 grep census 잔존 0).
- 버전 참고: v4.5.9는 decision_log에만 기록되고 main.md 헤더·본 changelog 반영이 누락됐었다. v4.6.0에서 헤더를 정정한다.

#### v4.5.8 (2026-07-14)

- **RED 게이트를 2-way에서 3-way triage로 확장**: `implementation` 스킬(및 `sdd-autopilot` 동형 게이트)의 test-first 불변식을 갱신했다. RED 게이트가 wave의 Stage A dispatch 직전에 task AC 성격을 (a) test / (b) structural-check / (c) test-free 3-way로 triage하며, (c) non-falsifiable content(산문·설명 문서·주석)는 Stage A 스킵·RED artifact 면제로 동어반복 acceptance check 강제를 제거한다. (c)는 오직 falsifiable 관찰 대상이 없을 때만 허용("간단한 구현이라서"는 자격 아님)하고, 명시 근거를 RED 증거와 동일한 progress 홈에 기록해 Step 6 리뷰 dispatch 입력에 전달하며(무근거 강등 금지), test만 면제되고 Step 5 회귀 스윕·Step 6 리뷰 게이트는 불면제다. (a)/(b)의 falsifiable 집행 성격은 불변(test-after 차단). graceful-degradation 분기 기준의 canonical surface(`implementation` 스킬 RED 게이트 서술)를 3-way triage 기준까지 포괄하도록 확장.
- **적용 surface**: §2 Guardrails test-first 불변식 bullet + §3 결정 테이블 "implementation test-first" 행. 구현 코드(6개 미러 짝: `implementation` SKILL·`test-author-agent`·`implementation-agent`·`sdd-autopilot` orchestrator-contract·SKILL·sample-orchestrator, claude·codex)는 draft `2026-07-13_feature_draft_red_gate_test_free_triage`로 선행 구현 완료(구현 report READY, acceptance check 10개 GREEN). 본 엔트리는 그 구현을 spec으로 동기화(post-implementation sync).

#### v4.5.7 (2026-07-13)

- **task-ordering을 transient ordering overlay로 축소**: `task-ordering-agent`가 full implementation-plan을 생성·저장하던 계약을 폐기하고, feature draft를 read-only로 읽어 `Status·Source·Mode·Execution·Dependencies·Checkpoints·Notes`만 담은 짧은 Markdown을 부모 orchestrator에 직접 반환하는 얇은 overlay로 환원했다. `_sdd/implementation/*_implementation_plan_*.md` artifact를 더 이상 만들지 않는다 — ordering은 원본 task-set에서 재계산 가능한 파생값이므로 독립 persistent artifact로 복제하지 않는다. agent tools `["Read","Write","Glob"]`→`["Read"]`, 본문 177/178줄→70/67줄. task 정의 전사·6-field phase metadata·`Parallel Execution Summary` artifact·review loop 서술을 제거했다.
- **Checkpoint 모델 변경**: phase별 `Checkpoint: true/false` 필드 → transient response의 별도 `Checkpoints` 목록(중간 review boundary만 기재, 마지막 phase는 implicit checkpoint). §2 Guardrails·결정 테이블·§Constraints 반영.
- **적용 surface**: `task-ordering-agent` claude md+codex toml, 소비자 `implementation` SKILL(v3.6.0→3.7.0) claude+codex, `sdd-autopilot` SKILL·`orchestrator-contract.md`·`sdd-reasoning-reference.md`·`examples/sample-orchestrator.md`·`scripts/validate_orchestrator.py` 각 claude+codex 미러, `plan-review-agent`(표현 정정 1줄) md+toml, codex `agents/README.md`(Inline Writing 목록에서 제거). validator에 `출력 파일=없음 (transient final response)`·`Phase Source==task_ordering.response`·controller↔ordering step 짝 검사를 추가하고 양쪽 실행 PASS 확인.

#### v4.5.6 (2026-07-13)

- **하네스 §3 화살표에서 implementation-plan 제거**: planning precedence 결정(feature-draft 기본, implementation-plan은 phase/task 세분화 필요시 follow-up)을 하네스에 반영. 화살표를 `feature-draft → (spec-sync) → implementation`로 정리하고, 괄호 optional 설명·"단계 = 동명 스킬" 규칙 예시에서도 implementation-plan을 뺐다. 모델이 implementation-plan을 default planning으로 오인하고 feature-draft를 건너뛰던 여지 차단이 목적. 하네스 §3은 얇은 기본 흐름만 소유하고 조건부 상세는 spec이 소유하는 계층 분리라, spec의 "필요시 붙인다" 결정과 모순 아님.
- **적용 surface**: 하네스 템플릿 4개 미러(claude·codex × spec-create·spec-upgrade references) byte-identical + 이 repo dogfooding `AGENTS.md` §3. `implementation-plan` 스킬(version 5.0.0)·planning precedence 결정·정책 무변경.

#### v4.5.5 (2026-07-13)

- **하네스 §3에 "단계 = 동명 SDD 스킬 호출" 규칙 추가**: AGENTS.md 템플릿 §3의 `discussion → feature-draft → … → implementation` 화살표 각 단계 이름이 동명 SDD 스킬이며, 진입 시 그 스킬을 호출하고 직접 재구현하지 않는다(미설치 환경에서만 수동)는 규칙을 추가했다. 소비 repo에서 모델이 `feature-draft` 등을 스킬 대신 자작하던 문제 차단이 목적. 스킬 카탈로그는 여전히 비복사(rename·추가 시 stale 회피) — 매핑 테이블 대신 행동 규칙 한 줄.
- **적용 surface**: 하네스 템플릿 4개 미러(claude·codex × spec-create·spec-upgrade references) byte-identical + 이 repo dogfooding `AGENTS.md` §3. 단계 순서·optional·정책 무변경.

#### v4.5.4 (2026-07-10)

- **pr-review 통합 리포트를 finding-본문 중심으로 재설계**: 통계 표(Metrics Summary·렌즈별 severity 카운트 표)와 Recommendations 표를 제거하고, 행동 대상 finding을 위치(`file:line`)·문제·수정 블록 전문으로 통합 리포트에 승격한다. 표 셀 압축으로 "뭘 고쳐야 하는지"가 소실되던 문제의 해소가 목적. 배치: correctness Critical/High + simplicity Medium+ → §1 Pre-merge 블록, correctness Medium → §2 non-blocking 상세 블록, Low → §2 위치 포함 한 문장. 분포는 Verdict `Signals` 한 줄로 대체, 통과 신호는 §3 산문 2-3줄.
- **승격 재료 반환 계약**: `pr-review-agent`는 Critical~Medium finding을 각각 위치·문제·수정 블록으로 반환(Step 5)하고, simplicity 레인은 dispatch message로 동일 상세를 요구한다(agent 무변경). 부족하면 orchestrator가 detail 리포트 §1을 Read해 보충. 2026-07-08 결정 #3("통합 리포트 = 요약 + 경로 참조")을 부분 대체 — 검증 ledger·차원별 스캔·iteration history는 여전히 detail 참조.
- **pr-review-agent detail 리포트 §1 Findings 블록화**: `- [finding]` 한 줄 불릿 → ID(C#/H#/M#/L#)·제목 + 위치·문제·수정 블록(Low는 한 문장). Iteration History delta가 참조하던 finding ID가 이로써 실제 정의됨.
- **적용 surface**: `pr-review` claude+codex SKILL v3.2.1→3.3.0, `pr-review-agent` claude md+codex toml, codex `examples/sample-review.md` 2개 예시 재작성. verdict 정책(자동 강제 없음)·단일 작성자 불변식은 무변경.
- **동일 원칙을 plan/implementation review로 확장**: `implementation-review-agent` §1 Findings를 같은 ID 블록(C#/H#/M# = 위치·문제·수정, Low = 한 문장)으로 교체(review-fix loop의 fix task 변환 재료), §4 Recommendations는 finding ID 참조 갈음, §5 Conclusion 삭제(Current Status와 중복), §2 Progress Overview는 task/AC 상태로 제약. `plan-review-agent`는 finding ID 부여 + Low 한 문장 축약만(이미 블록·재진술 금지 보유). 각 claude md+codex toml 4개 surface.
- **simplicity·implementation report 확장**: `simplicity-review-agent` §1도 ID 블록(H#/M#=차원·위치·현재 형태·제안 형태, Low=한 문장)으로 통일(차원·falsifiable severity 정책 무변경). `implementation` SKILL(v3.5.0→3.6.0) 최종 implementation_report의 Quality Assessment/Cross-Phase Review/Issues Found 표를 Review Gates 한 줄 ledger + Open Issues(잔존분만, reviewer finding ID 참조 + 위치 포함 한 문장)로 교체, Recommendations ID 참조 갈음, Conclusion은 verdict+한 문장 근거 유지(`spec-sync`·`spec-summary` 경로/글롭 소비 호환).

#### v4.5.3 (2026-07-08)

- **pr-review correctness를 dispatched agent로 추출**: `pr-review`가 자체 inline으로 수행하던 correctness 검증을 신규 `pr-review-agent`(read-only leaf)로 분리했다. `pr-review`는 이제 correctness(`pr-review-agent`) ∥ simplicity(`simplicity-review-agent`) 두 렌즈를 병렬 dispatch하고 verdict를 합성하는 orchestrator이며, `implementation-review` 2-reviewer 구조와 동형이다.
- **model override 균일화**: correctness가 inline이 아닌 agent로 이동해 subagent model override(`--model`, Codex `--effort`)가 correctness·simplicity 두 렌즈에 균일 적용된다(기존 비대칭 해소).
- **대칭 리포트 형태**: correctness도 simplicity처럼 자기 리포트(`_sdd/pr/..._pr_correctness_<slug>.md`)를 write하고, orchestrator 통합 리포트(`_sdd/pr/..._pr_review_<slug>.md`)는 두 렌즈 요약 + 두 detail 경로 참조 + verdict를 담는다. 세 리포트는 공유 slug로 정렬. 단일 작성자 불변식 유지.
- **spec surface 반영**: guardrail sub-bullet(PR review 직교 2-렌즈), 결정 테이블 `직교 2-렌즈 review 렌즈` 행, `components.md` `pr-review` 행을 "correctness=`pr-review-agent` dispatch"로 갱신. `pr-review-agent`를 claude marketplace.json + codex agents README에 등록.
- **정책 무변경 재사용**: 표적 disjoint, Medium=gating/Low=advisory falsifiable 분류, verdict 자동 강제 없음, fix→re-review loop 미도입, `simplicity-review-agent`는 그대로. `pr-review` claude+codex SKILL v3.1.0→3.2.0.

#### v4.5.2 (2026-07-01)

- **`drafts/`·`work_log/`를 소비 repo 커밋 자산으로 승격**: feature draft가 사실상 구현 로그 역할을 하고 work_log도 같은 진행 기록 성격이라, 두 디렉토리를 로컬 전용 process artifact에서 커밋 자산으로 옮겼다. 소비 repo에서 커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`·`drafts/`·`work_log/`가 되고, 로컬 전용 process artifact는 4종(`_sdd/{discussion,implementation,pipeline,pr}/`)으로 좁혀졌다.
- **`SDD-WORKSPACE` 마커 블록에서 두 줄 제거**: spec-create(3d)·spec-upgrade(Step 6)의 gitignore marker block과 harness 템플릿 §2 문구에서 `_sdd/drafts/`·`_sdd/work_log/`를 제거했다. 멱등 병합 메커니즘은 불변이라 재실행 시 마커 블록만 새 4종으로 교체된다. harness 템플릿 4개 미러는 byte-identical 유지.
- **메타 repo 예외 불변**: 본 sdd_skills repo는 여전히 process artifact 전부를 커밋하는 예외이며, 이 repo의 `.gitignore`는 변경 대상이 아니다.
- **정책 대체 관계**: 이 변경으로 2026-06-20 결정 #1(커밋 경계)이 2026-07-01 결정으로 대체된다(같은 entry의 멱등 병합·env.md 경고·메타 예외는 유효).

#### v4.5.1 (2026-07-01)

- **planning/implementation skill group subagent model override 반영**: Claude Code 쪽 `feature-draft` / `implementation-plan` / `implementation-review` / `implementation` / `plan-review` / `pr-review`는 `--model <sonnet|opus|haiku|fable>`로 `Agent(...)` 호출 model을 override하고, Codex matching skill 6개는 `--model <gpt-5.5|gpt-5.4|gpt-5.4-mini>`와 `--effort <low|medium|high|xhigh>` 분리 옵션으로 `spawn_agent(...)`의 `model` / `reasoning_effort`를 override한다.
- **기본값 상속 규칙 명시**: model/effort 옵션을 생략하면 세션/agent 기본값을 상속하고 persistent custom agent 정의를 수정하지 않는 per-call override로 고정했다. Codex에서는 `gpt-5.5-high` 같은 결합형 값을 canonical syntax로 받지 않고 `--model gpt-5.5 --effort high` 형태를 사용한다.
- **README 사용법 추가**: 설치 섹션 뒤에 플랫폼별 subagent model override 예시와 적용 대상 스킬 목록을 추가했다.
- **범위 경계**: 구현 surface는 이미 커밋됨(commit `67c6b99`, `5b40460`). 본 sync는 global spec과 README surface lag만 보정하며 개별 `spawn_agent` / `Agent` 호출 예시 전체를 중복 확장하지 않는다.

#### v4.5.0 (2026-06-23)

- **test-first를 falsifiable 실행 불변식으로 Guardrails에 반영**: implementation-scoped 구현의 test-first가 leaf 자기보고가 아니라 orchestrator가 집행하는 실행 불변식임을 review/validation guardrail에 새 불릿 그룹으로 명시. 테스트 작성(`test-author-agent`)과 구현(`implementation-agent` GREEN→REFACTOR 전용)을 분리하고 그 사이에 orchestrator 소유 RED 게이트(실패 증거 캡처 + falsifiability 점검)를 닫은 뒤에만 구현을 dispatch함을 담음. RED 증거는 orchestrator가 캡처한 외부 산출물(자기보고 TDD표 아님). falsifiability 관찰 규칙(assertion/check 단계 실패만 유효 RED, import/collection-only 실패는 미충족→재작성), 테스트 고정 + `CONTRACT_MISMATCH`(약한 테스트 통과 퇴화 방지), 상류 결정/하류 실행 분리, wave 내부 파이프라인·wave 간 순차(cross-wave 중첩 없음), graceful degradation canonical surface(=`implementation` SKILL RED 게이트)를 thin하게 고정.
- **review-fix gate fix 정책 명시**: correctness finding(동작 버그)=test-first, simplicity/refactor finding=직접 fix로 처리(모든 finding을 test-first 파이프라인에 강제하지 않음)를 기존 fix 경로 불릿에 추가.
- **결정 테이블 `implementation test-first` 행 신설**: test-author/impl 분리 + orchestrator 소유 RED 게이트 + 테스트 고정(CONTRACT_MISMATCH) + wave 파이프라인을 유지 결정으로 고정.
- **dispatch controller 서술 1급 Step kind로 갱신**: generated orchestrator 구현 step을 `implementation-dispatch-controller` 1급 Step kind로 선언(subagent_type 오버로드 아님)하고 wave별 3단계(test-author 병렬 → RED 게이트 → impl 병렬)로 fan out함을 "운영상 반드시 유지할 구조적 판단"에 반영.
- **supporting surface 갱신**: `components.md` — `test-author-agent` 행 신설, `implementation` 행을 2-stage + RED/GREEN 게이트(v3.4.0)로, `sdd-autopilot` 행을 dispatch-controller Step kind로 갱신, Strategic Code Map의 Implementation orchestrator/leaf 행과 Platform Notes split을 2-stage로 정렬.
- **decision_log 신규 entry**: "test-first를 orchestrator 소유 RED 게이트로 falsifiable 실행 불변식화" 결정 기록(6개 결정·근거). 과거 entry는 무손상 보존.
- **범위 경계**: 구현 surface(`test-author-agent` 신규 + `implementation-agent` GREEN 전용 재정의 + `implementation` SKILL v3.4.0 + autopilot 계약/SKILL/sample + marketplace registry, claude/codex 6쌍 미러)는 이미 머지됨(commit `aa9c328`/`6cdbb48`, report READY V1~V9 MET, 코드 직접 확인). 본 sync는 global spec surface lag만 보정하며 RED 게이트 판정 규칙 상세·Stage 입력 필드 같은 feature-level execution detail은 SKILL/agent 원문에 두고 main 본문은 thin 유지(canonical surface 단일성 유지).
- 입력: `_sdd/drafts/2026-06-23_feature_draft_test_first_group_pipeline.md` Part 1(`spec-update-todo-input` 마커), `_sdd/implementation/2026-06-23_implementation_report_test_first_group_pipeline.md`(evidence), 코드 직접 확인(commit `aa9c328`/`6cdbb48`).

#### v4.3.3 (2026-06-22)

- **신규 스킬 `goal-init`을 컴포넌트 카탈로그에 동기화**: `components.md` Discussion & Utilities 테이블에 `goal-init` 행을 신설(discussion 행 바로 뒤). Purpose/Why/Source/Notes에 계약·불변식만 compact하게 반영 — discussion식 대화형 단일 스킬(신규 agent 없음), 산출물 경로 `_sdd/goal/<YYYY-MM-DD>_<slug>/` 4파일(`goal.md`/`experiments.md`/`journal.md`/`report.md`), 평가자 자족성(완료부 transcript-only 판정·4,000자 이하, HOW는 `goal.md` Loop Protocol 분리), 비발동(스킬은 `/goal` 직접 발동 안 함), 런타임 분리, ralph 잔재 부재(bash 루프/run.sh/state머신/컨테이너 없음), ralph-loop 대체 deferred. feature-level execution detail(조건 슬롯 포맷·하네스 필드·self-check 절차)은 SKILL.md/references 원문에 두고 카탈로그엔 옮기지 않음(thin 유지).
- **main 본문·Guardrail 무변경**: 단일 스킬 추가는 Repo-wide Invariant Test(2+ feature 공통·코드로 복구 불가·repo-level reasoning 오류 유발)를 통과하지 못하므로 Guardrails/Key Decisions에 반영하지 않고 카탈로그 surface에만 등재. `agents` 배열 불변이라 nesting/dispatch 모델 서술도 무변경.
- **decision_log 신규 entry**: "`goal-init` 스킬 추가(`/goal` 조건 + 4파일 실행 하네스 생성기)" 결정 기록(존재·산출물 경로 계약·4불변식·ralph 정신만 차용·ralph 대체 deferred). 과거 entry는 무손상 보존.
- **범위 경계**: 구현 surface(8 신규 + 1 수정 파일: Claude/Codex SKILL.md·skill.json·references·examples + `marketplace.json` 등록)는 이미 working tree에 적용됨(evidence: implementation report V1~V6 전부 MET, 코드 직접 확인). 본 sync는 global spec surface lag만 보정한다.
- 입력: `_sdd/drafts/2026-06-22_feature_draft_goal_init_skill.md` Part 1(`spec-update-todo-input` 마커), `_sdd/implementation/2026-06-22_implementation_report_goal_init_skill.md`(evidence), 코드 직접 확인.

#### v4.3.2 (2026-06-20)

- **소비 repo 워크스페이스 commit 정책을 spec surface에 동기화**: 부트스트랩 스킬(spec-create / spec-upgrade)이 소비 repo `.gitignore`에 `SDD-WORKSPACE` 마커 블록을 멱등 병합해 process artifact 6종(`_sdd/{discussion,drafts,implementation,pipeline,pr,work_log}/`)을 로컬 전용으로 두고, 커밋되는 `_sdd`를 `spec/`·`guides/`·`env.md`로 좁히며, `_sdd/env.md`에 비밀값 금지 경고를 다는 변경(이미 working tree에 적용됨)을 spec surface에 반영.
- **main.md guardrail 신설(Repo-wide Invariant Test 통과)**: artifact-path guardrail 뒤에 commit-vs-ignore 경계 + env.md 비밀값 금지 + 이 sdd_skills repo의 메타 repo 예외를 한 줄 guardrail로 추가. feature-level 멱등 병합 detail(마커 교체 규칙 등)은 supporting surface와 SKILL 본문에만 두고 main 본문은 thin 유지.
- **supporting surface 갱신**: `components.md` — spec-create 행 Notes에 `.gitignore` 멱등 병합·env.md 경고 추가, Platform Notes에 "Workspace commit 정책(소비 repo)" 행 신설. `usage-guide.md` Scenario 1 expected result에 `.gitignore` 생성/멱등 병합과 env.md 비밀값 경고 헤더 추가.
- **decision_log 신규 entry**: "소비 repo 워크스페이스 commit 정책(process artifact gitignore + env.md 비밀값 경고)" 결정 기록. 과거 entry는 무손상 보존.
- **범위 경계**: 구현 surface(하네스 템플릿 4곳 §2 미러 + 이 repo `AGENTS.md`·`_sdd/env.md` 인라인, spec-create/spec-upgrade SKILL.md ×(claude/codex))는 이미 working tree에 적용됨(evidence: `git diff`). 본 sync는 global spec surface lag만 보정한다.
- 입력: working tree diff(spec-create/spec-upgrade SKILL.md, 하네스 템플릿 4곳, `AGENTS.md`, `_sdd/env.md`), 사용자 동기화 지침.

#### v4.3.1 (2026-06-20)

- **Harness §5 작업 기록(work log) 레이어를 supporting surface에 동기화**: harness 템플릿이 §0~§4 → §0~§5로 확장(§5 = `_sdd/work_log/<yyyy-mm-dd>.md`에 작업 단위를 append하는 on-demand 포렌식 규약, §1 읽기 순서 미포함, `_sdd/pipeline/log_*.md` autopilot 트랙과 별개)된 것을 spec surface에 반영. `components.md` Strategic Code Map의 Harness layer template 행을 §0~§5로, `usage-guide.md` Scenario 1의 AGENTS.md expected result를 §0~§5(+§5 work log 설명)로 갱신.
- **decision_log 신규 entry**: "Harness(`AGENTS.md`)에 §5 작업 기록(work log) 레이어 추가" 결정 기록. 과거 §0~§4 고정 결정 entry(L105/L118)와 v4.1.16 changelog는 당시 사실로 무손상 보존(역사 왜곡 금지).
- **범위 경계**: 구현 surface(harness 템플릿 4곳 미러 + 이 repo `AGENTS.md`에 §5 인라인 추가, SKILL.md 14곳 §0~§4→§0~§5)는 이미 working tree에 적용됨(evidence). 본 sync는 global spec surface lag만 보정하며 work log 항목 포맷 detail을 main 본문에 옮기지 않는다(thin 유지). main.md L103 harness layer 서술은 section 수를 열거하지 않아 무변경. 별도 `_sdd/work_log/TEMPLATE.md`는 만들지 않음(복사 금지).
- 입력: working tree diff(`AGENTS.md`, 하네스 템플릿 4곳, SKILL.md 4곳), `_sdd/discussion/2026-06-20_discussion_agents_md_work_log_harness.md`, 사용자 동기화 지침.

#### v4.3.0 (2026-06-17)

- **직교 2-렌즈 review를 PR review 진입점으로 확장(surgical 절 추가)**: review/validation guardrail에, simplicity 렌즈가 implementation-scoped review-gate에 더해 PR review(`pr-review` 스킬)에도 적용됨을 새 sub-bullet으로 명시. `pr-review`는 자체 correctness 검증 ∥ `simplicity-review-agent` 병렬 dispatch의 PR 차원 직교 2-렌즈 review이며, 표적 disjoint(correctness=PR/spec 정합·보안·테스트·verdict + 정확성-중복, simplicity=동작-불변 형태 + 형태-중복), 단일 작성자 경로 분리(pr-review→`_sdd/pr/`, simplicity→`_sdd/implementation/`)를 담음. 기존 L71 `spec-review` 비확장 종속 절은 무손상 유지(교체·재작성 없음).
- **PR verdict 통합 정책 명시**: simplicity finding은 verdict를 자동 강제하지 않고 falsifiable gating finding(Medium+) → REQUEST CHANGES rationale 기여, 주관(Low) → Suggested Improvements. pr-review는 인간 리뷰 보조이므로 implementation gate의 합집합 자동 exit(`critical=high=medium=0`)를 적용하지 않음을 명시. Medium=gating/Low=advisory 분류는 기존 falsifiable-only gating 규칙을 재사용(신규 계약 복제 없음).
- **결정 테이블 정합**: 기존 `implementation review 렌즈` 행을 `직교 2-렌즈 review 렌즈` 행으로 확장해 implementation review-gate와 PR review 두 진입점에 같은 패턴이 적용됨을 한 결정으로 고정.
- **범위 경계**: 구현 surface(`pr-review` claude+codex SKILL 2개 — dispatch 레인·표적 disjoint·verdict 정책·Output Format Simplicity 섹션, v2.0.0→3.0.0)는 이미 머지됨(report READY, 2-reviewer gate 통과, gating finding 0). 본 sync는 global spec surface lag만 보정하며 pr-review Process step / Output Format 같은 feature-level dispatch detail을 main 본문에 옮기지 않는다(thin 유지). `simplicity-review-agent`는 단일 소스 read-only 재사용이라 무변경.
- 입력: `_sdd/drafts/2026-06-17_feature_draft_pr_review_simplicity_lens.md` Part 1, `_sdd/implementation/2026-06-17_implementation_report_pr_review_simplicity_lens.md` (READY).

#### v4.2.0 (2026-06-17)

- **직교 2-렌즈 병렬 review 계약을 Guardrails에 반영**: review/validation guardrail에, implementation-scoped review-gate(`implementation` 스킬 phase/final gate, autopilot global/per-group/final-integration gate)가 단일 reviewer가 아니라 표적이 disjoint한 두 read-only leaf reviewer(`implementation-review-agent` correctness ∥ `simplicity-review-agent`)를 병렬 dispatch하고 gating exit가 두 report 합집합 `critical=high=medium=0`임을 명시. simplicity 렌즈는 `spec-review`로 확장하지 않음을 못박음.
- **falsifiable-only gating 불변식 명시**: simplicity finding은 더 단순한 동등 형태를 구체적으로 제시할 수 있는 객관적 위반만 Medium 이상(gating), 주관적 취향은 Low(advisory)라는 수렴성 닻을 guardrail에 반영.
- **fix 경로 단일성 보강**: 두 reviewer finding이 합산돼 기존 단일 fix 경로(`implementation-agent` 순차 재dispatch)로 처리되며 simplicity reviewer도 산출물을 직접 수정하지 않음(단일 작성자 불변식)을 명시.
- **결정 테이블에 `implementation review 렌즈` 행 추가**: correctness ∥ simplicity 직교 2-reviewer 병렬, 합집합 exit, falsifiable-only gating을 유지 결정으로 고정.
- **DECISION_LOG**: "Orthogonal 2-lens parallel review for implementation gates" 결정 기록 추가.
- **범위 경계**: 6+개 구현 surface(reviewer agent 신규/경량화, producer orchestration, autopilot 매핑, `validate_orchestrator.py` 게이트키퍼, contract §6, sample)는 이미 머지됨. 본 sync는 global spec surface lag만 보정하며 feature-level dispatch detail이나 canonical agent 전체 열거를 main 본문에 옮기지 않는다(thin 유지 — agent set 열거는 contract가 단일 소스).
- 입력: `_sdd/drafts/2026-06-17_feature_draft_simplicity_reviewer.md` Part 1, `_sdd/implementation/2026-06-17_implementation_report_simplicity_reviewer.md` (READY).

#### v4.1.16 (2026-06-12)

- **Harness(AGENTS.md) 레이어를 global 설계 모델에 반영**: `main.md` 핵심 설계의 layer 서술이 Skill/Agent/Artifact/Reference 4-layer 단정에 더해, 그 위에 놓이는 별도 Harness layer(`AGENTS.md` = 작업 진입·작업 규약 how)를 명시하도록 보정했다. canonical 문서(`docs/SDD_CONCEPT.md`, `docs/SDD_WORKFLOW.md`)가 도입한 harness layer와의 모순을 제거. harness는 global spec 본문을 키우지 않는 별도 레이어이며 repo-specific 트리거·핵심 결정은 여전히 global spec Guardrails가 단일 소스다(I1·I2 보존).
- **usage-guide AGENTS.md expected result 동기화**: `spec-create`의 AGENTS.md 산출 기술을 legacy "동일 안내 유지"에서 harness 템플릿(§0~§4) 기반 생성 + `SDD-HARNESS` 마커 멱등 병합으로 갱신. CLAUDE.md는 `→ AGENTS.md 참조` 포인터로 정정.
- **version metadata 정합**: header를 changelog 최신과 정렬(v4.1.14 → v4.1.16).
- **범위 경계**: harness 구현(템플릿 4곳 미러·`spec-create`/`spec-upgrade` SKILL 격상)은 commit `e5ad765`에서 이미 머지됨. 본 sync는 global spec surface lag만 보정하며 guardrails/decision 테이블에 harness 작업 규약 detail을 옮기지 않는다(thin 유지).
- 입력: commit `e5ad765`, `_sdd/drafts/2026-06-12_feature_draft_agents_md_harness_layer.md`, `_sdd/implementation/2026-06-12_implementation_report_agents_md_harness_layer.md` (READY), `_sdd/spec/logs/spec_review_report.md` (SYNC_REQUIRED, C-1/Q-1/Q-2)

#### v4.1.15 (2026-06-09)

- **Codex custom agent canonical ID kebab-case 전환**: `.codex/agents/*.toml`의 `name` 필드를 파일 stem과 같은 kebab-case `*-agent` ID로 정렬했다. Codex runtime은 TOML `name`을 `agent_type`으로 resolve하므로 파일명과 호출명이 같은 형태가 된다.
- **Codex wrapper dispatch 정렬**: `feature-draft`, `implementation-plan`, `implementation`, review/spec/ralph wrapper의 `spawn_agent(agent_type=...)` 참조를 kebab-case custom agent ID로 갱신했다.
- **sdd-autopilot generated orchestrator contract 정렬**: 허용 `agent_type` 목록, producer gate, review-fix loop mapping, dispatch controller, sample orchestrator/reference 문서가 kebab-case custom agent ID만 canonical으로 사용한다. underscore custom agent ID와 suffix 없는 skill 이름은 legacy alias로 reject/regenerate 대상이다.
- **current spec/docs sync**: `_sdd/spec/main.md`, `_sdd/spec/components.md`, `.codex/agents/README.md`에 Codex/Claude 모두 kebab-case invocation을 canonical으로 쓰는 정책을 반영했다.
- **검증**: stale exact underscore custom agent ID grep PASS, Codex agent `name = ".*_agent"` grep PASS, `git diff --check` PASS, fresh `codex exec` smoke에서 `feature-draft-agent` resolve PASS.
- 입력: `_sdd/drafts/2026-06-09_feature_draft_codex_agent_kebab_names.md`, `_sdd/implementation/2026-06-09_plan_review_codex_agent_kebab_names.md` (CLEAR), `_sdd/implementation/2026-06-09_implementation_report_codex_agent_kebab_names.md`

#### v4.1.14 (2026-06-03)

- **sdd-autopilot generated orchestrator contract hardening 반영**: generated orchestrator가 `feature_draft_agent` / `implementation_plan_agent` output을 downstream 소비 전 `plan_review_agent` gate로 검증하도록 global spec에 반영
- **implementation dispatch controller 고정**: generated orchestrator의 `implementation_agent` / `sdd-skills:implementation-agent` step은 feature/phase 전체 leaf call이 아니라 task-level leaf fan-out을 파생하는 dispatch controller임을 명시
- **canonical-only invocation rule 반영**: Codex `_agent` names, Claude `sdd-skills:<agent>-agent` names만 generated invocation으로 허용하고 legacy alias normalization은 추가하지 않는 결정 기록
- **review-fix severity 및 Checkpoint schema 정렬**: Critical/High/Medium은 gate blocker, Low는 advisory/logged follow-up으로 정리. missing non-final `Checkpoint` metadata는 single late gate fallback이 아니라 plan schema violation으로 reject/regenerate
- **Strategic Code Map 보강**: `sdd-autopilot` contract/reference entrypoint(`orchestrator-contract.md`, `sdd-reasoning-reference.md`)만 navigation hint로 추가하고 temporary Touchpoints는 복구하지 않음
- 입력: commit `7c0f99e`, `_sdd/drafts/2026-06-03_feature_draft_sdd_autopilot_contract_hardening.md`, `_sdd/implementation/2026-06-03_implementation_report_sdd_autopilot_contract_hardening.md`, `_sdd/implementation/2026-06-03_implementation_review_sdd_autopilot_contract_hardening.md` (CLEAR), `_sdd/implementation/test_results/test_results_sdd_autopilot_contract_hardening.md`

#### v4.1.13 (2026-06-03)

- **세 producer 스킬에 review-fix loop 내장**: `implementation`/`feature-draft`/`implementation-plan`이 autopilot 없이 직접 호출되는 경로에서도 review→fix→re-review loop를 자체 소유한다. 공통 정책(exit `critical=high=medium=0`·MAX 3·loop 범위 전체 재리뷰·MAX 분기)을 autopilot orchestrator-contract §6에서 차용, 각 스킬 인라인 보유(공유 파일 미생성)
- **`implementation` Step 6 외부 loop 교체**: 인라인 경량 self-review 제거 → 외부 `implementation-review-agent` review→fix→re-review. fix=`implementation-agent` finding 순차 재dispatch(leaf는 fix mode 별도 계약 없이 task 처리, I3). loop scope=phase 단위 1 gate(autopilot global/per-group 미차용). SKILL 2종 v3.0.0→3.1.0
- **`feature-draft`/`implementation-plan` wrapper→orchestrator 승격**: 두 thin wrapper를 loop-owning orchestrator로 재작성. producer 생성 dispatch 직후 `plan-review-agent` loop 소유. feature-draft는 Mode B digest를 생성·fix 라운드 모두 유지, implementation-plan은 Mode A(digest 없음). Role Pointer 재정의. SKILL 4종 v3.0.0→4.0.0
- **producer-agent fix mode 추가**: `feature-draft-agent`/`implementation-plan-agent`(claude .md + codex .toml)에 fix mode 입력 계약(리포트+산출물+findings 모두→fix, 입력 존재가 신호) 추가. surgical 수정·산출물 단일 작성자(I1) 보존. codex feature-draft `spec-update-todo-input` 마커 보존
- **범위 경계**: autopilot·`orchestrator-contract.md`·`implementation-agent`/reviewer agent 본문 미변경(실행 경로 비중첩, 재사용만)
- **supporting/history sync**: `main.md`(실행 분리·guardrail·결정 행), `components.md`(feature-draft/implementation-plan 재분류·implementation Step 6·Platform Notes), `DECISION_LOG.md` 갱신
- **잔여(미검증)**: V6 reload smoke(trigger resolve + multi-phase gate 1회 종료)는 self-referential 제약상 DEFERRED. 정적 게이트 V1~V5/V7 전부 PASS
- 입력: `_sdd/drafts/2026-06-03_feature_draft_skills_embed_review_fix_loop.md`, `_sdd/implementation/2026-06-03_implementation_report_skills_embed_review_fix_loop.md`, `_sdd/implementation/2026-06-03_plan_review_skills_embed_review_fix_loop.md` (CLEAR), branch `refactor/skills-embed-review-fix-loop` (`52a4c7f`)

#### v4.1.12 (2026-06-03)

- **investigate 재분류**: v4.1.11에서 census 오분류로 wrapper(Mode B)+`investigate-agent`로 전환됐던 `investigate`를 orchestrator(skill)로 재분류. 전체 디버깅 계약을 메인 루프 skill이 인라인 소유하고, 탐색이 넓고·모호할 때만 빌트인 범용 read-only explore 역할(claude `Explore`, codex `spawn_agent(agent_type="explorer")`)을 병렬 fan-out한다(custom leaf 미신설). investigate SKILL 2종 v4.0.0
- **investigate-agent 제거**: `.claude/agents/investigate-agent.md`, `.codex/agents/investigate-agent.toml` 삭제 및 `marketplace.json` `agents` 목록에서 제외(skill 항목 유지). 참조자가 wrapper+매니페스트뿐이라 제거 격리
- **supporting/history sync**: `components.md` investigate 행 정정, `DECISION_LOG.md`에 reclassification entry 추가 + v4.1.11 entry의 investigate 분류 3곳(비-fan-out 목록·Mode B 목록·`Agent` 도구 제거 목록)에 정정 마커
- 입력: `_sdd/drafts/2026-06-03_feature_draft_investigate_orchestrator.md`, `_sdd/implementation/2026-06-03_plan_review_investigate_orchestrator.md` (CLEAR), implementation review READY (branch `refactor/investigate-orchestrator`)

#### v4.1.11 (2026-06-03)

- **orchestrator/leaf 실행 형태 고정**: fan-out이 필요한 `implementation`을 orchestrator(skill) + leaf(agent)로 분리. skill이 task-set 확보·dependency 기반 그룹 파생·leaf fan-out·통합/회귀/phase review/report를 소유하고, `implementation-agent` leaf는 단일 task TDD만 수행한다(sub-agent spawn 없음). nesting 1단계 제한 아래 fan-out을 메인 루프로 올림
- **wrapper-backed skill 형태 고정**: fan-out이 없는 9종(`feature-draft`, `implementation-plan`, `plan-review`, `implementation-review`, `ralph-loop-init`, `spec-review`, `spec-update-done`, `spec-update-todo`, `investigate`) SKILL을 thin entrypoint wrapper로 전환하고 agent를 단일 소스로 둠. full 본문 중복 4벌→2벌(실측 약 -4,700줄)
- **wrapper 2-모드**: 파일+직접 요청 입력은 pass-through(Mode A), 대화 태생 입력(`feature-draft`·`investigate`·`implementation-review`)은 대화 맥락 digest forwarding(Mode B). 원리 "agent는 파일은 read하나 대화는 못 읽는다"
- **planner dependency 인코딩 정식화**: `feature-draft`/`implementation-plan`이 의미적 충돌 5패턴을 명시적 dependency로 인코딩(무방향 mutex 임의 방향 흡수), orchestrator는 trivial 규칙으로 그룹 파생
- **autopilot dispatch granularity**: 초기 구현=group 병렬 leaf fan-out / fix=finding 순차 leaf 재dispatch / progress·report 소유=실행 주체(canonical 경로 보존). orchestrator-contract §2 신설
- **mirror sync 의무 해소**: wrapper-backed skill은 agent가 단일 소스 — "skill·agent 본문 함께 미러링" 의무 대부분 해소, dead `Agent` 도구 5종 제거, Mirror/Sync Notice → Source/Role Pointer
- **supporting docs sync**: `main.md`, `components.md`, `usage-guide.md`를 검증된 구현 evidence 기준으로 갱신. Strategic Code Map 경로 freshness 보정(`-agent` suffix 정합)
- 입력: `_sdd/drafts/2026-06-03_feature_draft_implementation_orchestrator_leaf_split.md`, `_sdd/drafts/2026-06-03_feature_draft_skills_as_agent_wrappers.md`, `_sdd/implementation/2026-06-03_implementation_report_implementation_orchestrator_leaf_split.md`, `_sdd/implementation/2026-06-03_implementation_report_skills_as_agent_wrappers.md`, `_sdd/implementation/2026-06-03_implementation_review_implementation_orchestrator_leaf_split.md`, `_sdd/implementation/2026-06-03_implementation_review_skills_as_agent_wrappers.md`

#### v4.1.10 (2026-05-22)

- **Strategic Code Map 표준화**: `Strategic Code Map`을 optional compact navigation surface로 정의하고, exhaustive file tree / component catalog / API reference / 구현 narrative로 확장하지 않는 guardrail을 고정
- **spec-create 생성 규칙 정렬**: primary navigation axis를 하나 선택하고, 짧은 map은 `main.md` appendix, 긴 map은 `components.md` 또는 `code-map.md` 같은 supporting surface로 분리하도록 Codex/Claude skill과 template/example 갱신
- **planning/sync 소비 규칙 정렬**: `feature-draft`는 code map을 hint로만 읽고 `Touchpoints`/`Target Files`를 현재 코드로 재확인하며, `spec-update-*`는 temporary touchpoint 통복사 대신 verified persistent navigation 변화만 승격
- **mirror parity 보정**: `feature-draft`, `spec-review`, `spec-update-todo`, `spec-update-done`의 Codex/Claude skill-agent normalized body 일치 확인
- **supporting docs sync**: `main.md`, `components.md`, `usage-guide.md`, `DECISION_LOG.md`를 새 code map semantics와 구현 evidence 기준으로 갱신
- 입력: `_sdd/drafts/2026-05-22_feature_draft_strategic_code_map_spec_skills.md`, `_sdd/implementation/2026-05-22_implementation_report_strategic_code_map_spec_skills.md`, `_sdd/implementation/2026-05-22_implementation_review_strategic_code_map_spec_skills.md`, `b994366`

#### v4.1.9 (2026-04-29)

- **multi-phase quality gate를 per-phase에서 per-group으로 전환**: `implementation-plan` schema에 6번째 필드 `Checkpoint: true/false`를 추가해 group boundary owner를 plan에 두고, autopilot은 `Checkpoint=true` phase 직후에만 review-fix gate를 닫는다. 마지막 phase는 implicit `Checkpoint=true`. `Checkpoint=true` phase에는 `Checkpoint Reason` 한 줄을 동반.
- **Mid-group emergency 추가**: group 내 phase의 light validation에서 `critical` 이슈를 잡으면 group boundary forced early로 즉시 review-fix gate 트리거.
- **Adaptive final integration review**: group 1개면 마지막 group gate가 final을 겸하고, 2개 이상이면 마지막 group gate 후 cross-group regression 전용 1회 추가.
- **Multi-phase ⇒ implementation-plan 의무 (Phase Source invariant)**: multi-phase 실행 시 `implementation-plan` step을 반드시 포함하고, `Phase Source`는 그 output만 가리키도록 강제. 위반 시 autopilot이 reject하고 `feature-draft` 직후에 `implementation-plan` step을 삽입한다.
- **Backward compat**: `Checkpoint` 필드가 없는 기존 plan은 단일 group 동작(마지막 phase 1회 gate)과 동등하게 처리.
- **supporting docs sync**: `components.md`, `usage-guide.md`를 per-group + adaptive 표현으로 갱신.
- 입력: `_sdd/discussion/2026-04-29_discussion_phase_grouped_review_fix_gate.md`, `_sdd/drafts/2026-04-29_feature_draft_phase_grouped_review_fix_gate.md`, `_sdd/implementation/2026-04-29_implementation_review_phase_grouped_review_fix_gate.md`, `_sdd/implementation/2026-04-29_implementation_review_phase_grouped_review_fix_gate_pass2.md`

#### v4.1.8 (2026-04-13)

- **spec lifecycle shared-core sync**: `spec-create`, `spec-review`, `spec-rewrite`, `spec-upgrade`의 공통 코어 4축과 스킬별 1차 추가 축을 supporting surface 설명에 반영
- **`spec-create` expected result 보정**: `/spec-create` expected result를 thin global core + single-file default 기준으로 정리하고 old canonical(`CIV`, `usage`, `decision-bearing structure`) wording 제거
- **component notes 보정**: `spec-review`에 rubric separation + evidence strictness, `spec-rewrite`에 rationale preservation + body/log placement, `spec-upgrade`에 rewrite boundary judgment를 반영
- 입력: `_sdd/drafts/2026-04-13_feature_draft_spec_lifecycle_core_checklist_alignment.md`, `_sdd/implementation/2026-04-13_implementation_review_spec_lifecycle_core_checklist_alignment.md`

#### v4.1.7 (2026-04-13)

- **spec-summary whitepaper 정렬**: `spec-summary`를 `summary.md`용 reader-facing whitepaper surface로 정리
- **section spine 반영**: `Executive Summary`, `Background / Motivation`, `Core Design`, `Code Grounding`, `Usage / Expected Results`, `Further Reading / References`를 expected result 기준으로 반영
- **appendix rule 고정**: planned/progress 정보는 관련 artifact가 있을 때만 appendix로 짧게 유지
- **supporting docs sync**: `components.md`, `usage-guide.md`, `DECISION_LOG.md`를 whitepaper semantics에 맞게 동기화
- 입력: `_sdd/drafts/2026-04-13_feature_draft_spec_summary_whitepaper_surface.md`, `_sdd/implementation/2026-04-13_implementation_review_spec_summary_whitepaper_surface.md`

#### v4.1.6 (2026-04-13)

- **spec-summary canonical overview 정렬**: `spec-summary`를 global/temporary 요약기보다 `global overview + optional planned/progress snapshot` surface로 재정의
- **summary output shape 갱신**: template/example에 `Where Details Live`를 도입하고 planned/progress snapshot을 보조 섹션으로 정리
- **supporting docs sync**: `components.md`, `usage-guide.md`, definition/workflow 문서, autopilot reasoning reference에 새 semantics 반영
- **metadata sync**: `.claude` / `.codex` `spec-summary` `skill.json` 버전을 `2.0.0`으로 정렬
- 입력: `_sdd/drafts/2026-04-13_feature_draft_spec_summary_canonical_overview_alignment.md`, `_sdd/implementation/2026-04-13_implementation_review_spec_summary_canonical_overview_alignment.md`

#### v4.1.5 (2026-04-10)

- **autopilot planning semantics sync**: non-trivial planning entry를 `feature-draft` 기본값으로, `implementation-plan`을 후속 확장 단계로 global spec에 반영
- **phase-gated execution rule 반영**: multi-phase plan을 `per-phase` review-fix + `final integration review` 실행 게이트로 정리
- **artifact naming/history invariant 반영**: lowercase canonical artifact, skill-defined dated slug output, legacy fallback read, git-history-first 추적 규칙을 global surface에 추가
- **usage guide 정렬**: autopilot active orchestrator 경로를 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`로 갱신하고 manual/auto scenario의 optional expansion path를 보정
- 입력: `ee4e1cd`, `d32686a`, `aa92c83`, `0725c25`, `_sdd/implementation/2026-04-10_implementation_review_autopilot_planning_phase_gates.md`

#### v4.1.4 (2026-04-07)

- **externalized skill cleanup**: 현재 저장소에서 제거된 독립 관리 스킬 참조를 active spec surface에서 제거
- **current surface 정리**: `main.md`, `components.md`, `usage-guide.md`가 이 저장소가 직접 관리하는 skill/workflow만 설명하도록 정리
- 백업: `_sdd/spec/prev/prev_main_20260407_184001.md`, `_sdd/spec/prev/prev_components_20260407_184001.md`, `_sdd/spec/prev/prev_usage-guide_20260407_184001.md`, `_sdd/spec/prev/prev_changelog_20260407_184001.md`
- 입력: workspace 현재 상태

#### v4.1.3 (2026-04-07)

- **Codex connector workflow output path 변경**: 외부 connector 기반 분석 workflow의 기본 저장 경로를 작업 디렉토리 기준으로 정렬
- **artifact path sync**: 관련 persistent handoff canonical path와 supporting surface의 기본 산출물 경로를 새 위치로 정렬
- 백업: `_sdd/spec/prev/prev_main_20260407_182819.md`, `_sdd/spec/prev/prev_components_20260407_182819.md`, `_sdd/spec/prev/prev_usage-guide_20260407_182819.md`, `_sdd/spec/prev/prev_changelog_20260407_182819.md`
- 입력: Codex connector workflow source

#### v4.1.2 (2026-04-07)

- **Codex connector workflow spec sync**: 새 외부 connector 기반 분석 workflow를 spec surface에 반영
- **artifact path 반영**: 관련 persistent handoff canonical path와 supporting surface reference를 확장
- **component/usage reference 확장**: component catalog와 usage scenario에 connector-backed 분석 흐름을 추가
- 백업: `_sdd/spec/prev/prev_main_20260407_180017.md`, `_sdd/spec/prev/prev_components_20260407_180017.md`, `_sdd/spec/prev/prev_usage-guide_20260407_180017.md`, `_sdd/spec/prev/prev_changelog_20260407_180017.md`
- 입력: Codex connector workflow source

#### v4.1.1 (2026-04-04)

- **components compact rewrite**: `components.md`를 category-based compact catalog로 재작성 (`284줄 -> 71줄`)
- **reference density 축소**: component별 Input/Output/Process/완료 이력 재복제를 제거하고 `Purpose / Why / Primary Source / Notes`만 유지
- **platform note 분리**: wrapper/agent split, full-skill 예외, Claude-only feature를 별도 `Platform Notes` table로 정리
- **strategic code map 유지**: 전수형 inventory는 늘리지 않고 navigation-critical appendix만 유지
- 백업: `_sdd/spec/prev/prev_components_20260404_130827.md`, `_sdd/spec/prev/prev_spec-rewrite-plan_20260404_130827.md`, `_sdd/spec/prev/prev_rewrite_report_20260404_130827.md`, `_sdd/spec/prev/prev_DECISION_LOG_20260404_130827.md`, `_sdd/spec/prev/prev_changelog_20260404_130827.md`
- 입력: `_sdd/spec/main.md`, `_sdd/spec/logs/spec-rewrite-plan.md`

#### v4.1.0 (2026-04-04)

- **global thin rewrite**: `main.md`를 3개 mandatory core 중심으로 재압축 (`257줄 -> 111줄`)
- **standalone 상세 제거**: `Contract / Invariants / Verifiability`, usage summary, decision-bearing structure 대형 표, reference/code-map appendix를 main body에서 제거
- **판단 기준 흡수 유지**: repo-wide invariant와 구조 판단은 `Guardrails`, `핵심 설계`, `주요 결정`에 압축 보존
- **supporting surface 정합성 보정**: `components.md`, `usage-guide.md` 도입부에서 legacy `§5`, `§7`, appendix 참조 제거
- 백업: `_sdd/spec/prev/prev_main_20260404_130259.md`, `_sdd/spec/prev/prev_components_20260404_130259.md`, `_sdd/spec/prev/prev_usage-guide_20260404_130259.md`, `_sdd/spec/prev/prev_DECISION_LOG_20260404_130259.md`
- 입력: `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md`, `_sdd/spec/logs/spec-rewrite-plan.md`

#### v4.0.1 (2026-04-04)

- **canonical rollout 후속 spec sync 반영**: `FD-05`~`FD-07` 구현 완료 사실을 active `_sdd/spec/` surface에 동기화
- **운영 규칙 명시**: canonical rollout/update order를 `definition -> generators/transformers -> consumers/planners -> docs -> english mirrors/examples -> audit`로 global spec에 고정
- **reference surface 확장**: `docs/en/` semantic mirror layer와 `guide-create` compact template pair를 main spec reference에 추가
- **component sync**: `spec-update-done`를 delta status 분류 + change report 기반 sync agent로, `guide-create`를 current canonical language를 재사용하는 guide generator로 설명 보정
- 백업: `_sdd/spec/prev/prev_main_20260404_021113.md`, `_sdd/spec/prev/prev_components_20260404_021113.md`, `_sdd/spec/prev/prev_changelog_20260404_021113.md`
- 입력: `_sdd/implementation/IMPLEMENTATION_PLAN.md`, `_sdd/implementation/IMPLEMENTATION_REPORT.md`, `_sdd/implementation/implementation_review.md`, `_sdd/spec/logs/spec_review_report_canonical_model_rollout.md`

#### v4.0.0 (2026-04-04)

- **current canonical global spec model로 업그레이드**: `main.md`를 canonical 1~7 + appendix 구조로 재작성
- **CIV 복구**: `Contract / Invariants / Verifiability`를 독립 표 구조로 추가하고 `_sdd/` artifact contract, wrapper/agent split, verification semantics를 명시
- **Decision-bearing structure 분리**: 시스템 경계, ownership, cross-component contract, extension point, invariant hotspot을 별도 section으로 승격
- **supporting file 역할 정리**: `components.md`를 reference-only 보조 문서로 명시하고, 전수형 code reference index를 strategic code map으로 축약
- **usage guide 정렬**: `usage-guide.md`를 section 5 보조 문서로 재정렬하고 expected result를 current model 기준으로 보정
- 백업: `_sdd/spec/prev/prev_main_20260404_015836.md`, `_sdd/spec/prev/prev_components_20260404_015836.md`, `_sdd/spec/prev/prev_usage-guide_20260404_015836.md`, `_sdd/spec/prev/prev_DECISION_LOG_20260404_015836.md`, `_sdd/spec/prev/prev_changelog_20260404_015836.md`
- 입력: `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md`

#### v3.9.1 (2026-04-03)

- **pr-spec-patch → pr-review 통합 반영**: pr-spec-patch 관련 잔존 참조 12+건 제거 (Category Overview, Artifact Map, PR 워크플로우, Directory Structure, Design Patterns, components.md, usage-guide.md, Code Reference Index)
- **second-opinion 스킬 문서화**: Claude Code 전용 second-opinion 스킬을 Category Overview, components.md, Directory Structure, Code Reference Index에 추가
- **Codex 스킬 수 수정**: 20개 → 19개 (pr-spec-patch 삭제 반영)
- **pr-review 컴포넌트 갱신**: v2.0.0 Unified PR Verification — code-only + spec-based 통합 검증으로 설명 갱신
- 백업: `_sdd/spec/prev/prev_main_20260403_103801.md`, `_sdd/spec/prev/prev_components_20260403_103801.md`, `_sdd/spec/prev/prev_usage-guide_20260403_103801.md`
- 입력: `_sdd/spec/logs/spec_review_report.md`

#### v3.9.0 (2026-04-03)

- **spec-rewrite 실행: 단일 파일 → 인덱스 + 서브 파일 구조로 전환**: main.md 1206줄을 668줄 인덱스로 경량화
- **신규 파일 3개 생성**: `components.md` (§4 Component Details + Code Reference Index, 303줄), `usage-guide.md` (§5 Usage Guide, 84줄), `logs/changelog.md` (Changelog 이동, 152줄)
- **해결 완료 이슈 정리**: #1-4, #8-16번 해결 완료 항목을 본문에서 제거 (changelog에서 추적 가능)
- **Directory Structure 갱신**: 새 파일 구조 반영
- **metric 개선**: Component Separation 2→3, Findability 2→3
- 백업: `_sdd/spec/prev/prev_main.md_20260403_000930.md`
- 진단/계획: `_sdd/spec/logs/spec-rewrite-plan.md`, `_sdd/spec/logs/rewrite_report.md`

#### v3.8.2 (2026-04-02)

- **spec-rewrite 품질 진단 강화**: `spec-rewrite`를 단순 prune/split 도구에서 8개 핵심 metric 기반 진단 후 재작성하는 스킬로 설명 갱신
- **question-style rubric 반영**: component 분리, 탐색성, 레포 목적 이해도, 아키텍처 이해도, 사용법 완결성, 환경 재현성, 모호성 통제, Why/decision 보존도를 기준 축으로 명시
- **spec-as-whitepaper 정렬**: `docs/SDD_SPEC_DEFINITION.md`를 상위 평가 기준으로 반영하고, missing whitepaper narrative는 `spec-rewrite`가 자동 생성하지 않고 경고만 남긴다는 경계 추가
- **artifact path 수정**: `rewrite_report` 경로를 `_sdd/spec/logs/rewrite_report.md`로 정정
- 백업: `_sdd/spec/prev/PREV_main_20260402_210232.md`
- 입력: `_sdd/implementation/IMPLEMENTATION_REPORT.md`, `_sdd/drafts/feature_draft_spec_rewrite_quality_rubric.md`

#### v3.8.1 (2026-04-01)

- **implementation review loop gate 보정**: `UNTESTED`를 raw PASS 상태로 두지 않고, 테스트 불가 사유 + 코드 분석 근거가 리포트에 기록된 경우에만 종료 조건에 포함되도록 정리
- **retry handoff contract 강화**: iteration 재실행 시 `failed_ac`, `failure_reason`, `open_critical_high_issues`를 다음 worker/sub-agent prompt에 필수 전달
- **Claude/Codex parity sync**: `.claude/skills/implementation/`, `.claude/agents/implementation.md`, `.codex/skills/implementation/`, `.codex/agents/implementation.toml`에 동일 review loop semantics 반영
- 백업: `_sdd/spec/prev/PREV_main_20260401_164618.md`, `_sdd/spec/prev/PREV_DECISION_LOG_20260401_164618.md`
- 입력: `_sdd/implementation/IMPLEMENTATION_REPORT.md`, `_sdd/implementation/IMPLEMENTATION_REVIEW.md`

#### v3.8.0 (2026-04-01)

- **write_skeleton 완전 제거**: `.claude/agents/write-skeleton.md`, `.codex/agents/write-skeleton.toml` 삭제
- **write-phased 재정의**: helper orchestrator가 아니라 producer-owned inline 2-phase writing contract로 역할 변경
- **current runtime 동기화**: writing helper를 전제하던 Claude/Codex caller 문구를 "직접 skeleton 작성 -> fill -> finalize" 규칙으로 치환
- **spec/runtime 정합성 수정**: 에이전트 수 10+10 -> 9+9, utility agent 설명 제거, directory structure와 component inventory를 현재 파일 구조에 맞게 갱신
- 백업: `_sdd/implementation/prev/PREV_IMPLEMENTATION_REPORT_20260401_153552.md`
- 입력: `_sdd/drafts/feature_draft_remove_write_skeleton_inline_writing.md`, `_sdd/discussion/discussion_write_skeleton_removal_and_inline_writing.md`

#### v3.7.0 (2026-03-24)

- **gstack Patterns 구현 완료 (spec-update-done)**: v3.6.1에서 계획(📋)으로 반영된 9개 결정 사항이 모두 구현되어 완료(✅)로 갱신
- **investigate 스킬 구현 완료**: `.claude/agents/investigate.md` (AC-First + self-contained, 6단계 프로세스) + `.claude/skills/investigate/SKILL.md` (래퍼) 생성. 근본원인 우선(Iron Law), 3-strike 에스컬레이션, scope lock, blast radius gate, fresh verification, Agent A/B 교차 검증 포함
- **기존 스킬 기능 구현 완료** (8개):
  - implementation: Verification Gate Iron Rule + Regression Iron Rule (Hard Rules 추가)
  - implementation-review: Fresh Verification (Hard Rule #8 추가)
  - feature-draft: Failure Modes 테이블 (Part 1 템플릿에 섹션 추가)
  - implementation-plan: Test Coverage Mapping (Step 3 뒤 조건부 하위 단계)
  - pr-review: Scope Drift Detection (Step 2.5) + Code Quality Fix-First (Step 5.5)
  - spec-review: Code Analysis Metrics (Step 3.5 + Output Format 지표 테이블)
  - sdd-autopilot: Audit Trail (Step 7.2) + Taste Decision (Step 8.2)
- **Mirror Notice 동기화 완료**: 5개 래퍼 스킬(implementation, implementation-review, feature-draft, implementation-plan, spec-review)의 SKILL.md에 에이전트 변경사항 반영
- **Identified Issues 8-16번 해결 완료로 이동**
- **investigate Component Details 상세 업데이트**: 실제 구현(6단계 프로세스, Agent A/B 교차 검증, Investigation Report 출력 형식)에 맞게 반영
- 백업: `_sdd/spec/prev/prev_main_20260324_180000.md`
- 입력: `_sdd/implementation/implementation_plan.md`, `_sdd/implementation/implementation_report.md`, `_sdd/drafts/feature_draft_gstack_patterns.md`

#### v3.6.1 (2026-03-24)

- **gstack Patterns 스펙 사전 반영 (spec-update-todo)**: feature_draft_gstack_patterns.md Part 1의 9개 결정 사항을 계획(📋) 상태로 스펙에 반영
- **신규 스킬 계획**: investigate (범용 체계적 디버깅 에이전트 + 래퍼 스킬) -- Component Details, Category Overview, Agent 목록, Directory Structure, Code Reference Index에 추가
- **기존 스킬 계획된 기능 추가** (9개):
  - sdd-autopilot: Audit Trail + Taste Decision (P1-High)
  - feature-draft: Failure Modes 테이블 (P2-Medium)
  - implementation-plan: Test Coverage Mapping (P2-Medium)
  - implementation: Verification Gate Iron Rule (P1-High), Regression Iron Rule (P2-Medium)
  - implementation-review: Fresh Verification (P1-High)
  - pr-review: Scope Drift Detection (P2-Medium), Code Quality Fix-First (P1-High)
  - spec-review: Code Analysis Metrics (P3-Low)
- **Identified Issues 섹션에 계획됨 목록 추가**: 8-16번 항목 (gstack patterns 전체)
- 백업: `_sdd/spec/prev/prev_main_20260324_120000.md`
- 입력: `_sdd/drafts/feature_draft_gstack_patterns.md` (Part 1)

#### v3.6.0 (2026-03-20)

- **AC-First + Self-Contained 전면 리팩토링**: 모든 9개 Claude agent + 11개 Claude full skill + 9개 Codex agent + 10개 Codex full skill을 AC-First 구조로 전면 재작성
  - Agent: AC 섹션 + 자체 검증 지시 + Final Check 추가, 핵심 reference 인라인 (self-contained)
  - Full Skill: AC 섹션 + 자체 검증 지시 + Final Check 추가, Best Practices/Context Management/When to Use 등 공통 bloat 제거
  - Claude agent: 4,365줄 -> 1,961줄 (55% 감축), Full skill: 5,042줄 -> 2,718줄 (46% 감축)
- **래퍼 스킬 references/examples 삭제**: Claude 9개 + Codex 8개 wrapper skill에서 미사용 references/examples 총 48개 파일 삭제
- **신규 디자인 패턴 2개**: AC-First 패턴 (AC + 자체 검증 + Final Check), Self-Contained 패턴 (핵심 reference 인라인)
- **ralph-loop-init 범용화**: "ML 트레이닝 디버그 루프" -> "장기 실행 프로세스(ML, e2e, 빌드 등) 자동화 디버그 루프"
- **SDD workflow 세부 변경**: implementation-plan Target Files 충돌 규칙 수정 (동일 파일 참조 시 마커 종류 무관하게 충돌), spec-update-todo 새 항목 기본 상태 마커 📋 명시, implementation-plan/implementation-review 리팩토링 메타 AC 삭제
- **Codex Smoke Check/Final Check 통일**: 기존 Final Smoke Check 제거, Final Check으로 통일
- **sdd-upgrade 스킬 제거 반영**: 이전에 삭제된 `sdd-upgrade` 스킬의 잔존 스펙 참조 정리 (21개 -> 20개 스킬)
- 백업: `_sdd/spec/prev/prev_main_20260320_120000.md`
- 드래프트: `_sdd/drafts/feature_draft_agent_self_containment.md`, `feature_draft_agent_self_containment_phase2.md`, `feature_draft_full_skills_ac_first.md`

#### v3.5.0 (2026-03-19)

- **sdd-autopilot v2.0.0 reasoning 리라이트**: 규모별 템플릿 매칭에서 SDD 철학 기반 reasoning + 동적 파이프라인 구성으로 전면 교체
- **Reference 파일 교체**: `references/pipeline-templates.md`, `references/scale-assessment.md` 삭제 -> `references/sdd-reasoning-reference.md` 신규 생성 (SDD 철학 + 스킬 카탈로그를 ~310줄로 압축)
- **Step 구조 변경**: Step 1(Reference Loading), Step 4(Reasoning -> Orchestrator Generation), Step 5(Orchestrator Verification) 신규 추가
- **Hard Rule #10 추가**: Execute -> Verify 필수 -- 모든 파이프라인 단계에 실행 + 검증 두 페이즈 필수
- **비오케스트레이션 스킬 재분류**: spec-create, discussion, guide-create를 autopilot 오케스트레이터 파이프라인에 넣지 않는 스킬로 명시
- **Orchestrator Template에 Reasoning Trace 섹션 추가**: 스킬 선택 근거, 순서 결정, 적용된 SDD 원칙을 기록
- **Dependencies 변경**: "스펙 없어도 실행 가능" -> "글로벌 스펙 존재 필수, 없으면 /spec-create 안내"
- **Codex 동기화**: `.codex/skills/sdd-autopilot/SKILL.md` (v2.0.1)도 동일 reasoning 아키텍처로 동기화 (Codex 차이점 보존)
- **변경**: 2-Phase Orchestration 패턴, sdd-autopilot Component Details, Design Rationale, Success Criteria, Scenario 2b, Code Reference Index 업데이트
- 백업: `_sdd/spec/prev/prev_main_20260319_120000.md`
- 토론: `_sdd/discussion/discussion_autopilot_reasoning_harness.md`

#### v3.4.1 (2026-03-17)

- **Codex autopilot parity 복원**: `.codex/skills/sdd-autopilot/`의 main skill, pipeline templates, scale assessment, sample orchestrator에 Claude 기준 실행 계약 복원
- **autopilot report artifact 명시**: `_sdd/pipeline/report_<topic>_<ts>.md`를 Artifact Map과 sdd-autopilot output contract에 반영
- **validation guide 통합**: 별도 `docs/CODEX_AGENT_VALIDATION.md` 대신 `docs/AUTOPILOT_GUIDE.md`의 "Codex 검증 체크리스트" 섹션을 운영 기준으로 사용
- **스펙 드리프트 수정**: Codex wrapper -> custom agent 실행 모델 설명과 상단 버전/산출물 설명을 최신 구조와 일치시킴

#### v3.4.0 (2026-03-17)

- **Codex custom agent backbone 도입**: `.codex/agents/`에 9개 custom agent 정의 추가 (feature_draft, implementation_plan, implementation, implementation_review, spec_update_todo, spec_update_done, spec_review, ralph_loop_init, write_phased)
- **Codex wrapper parity 강화**: 핵심 pipeline skill을 user entry wrapper로 명시하고, generated orchestrator가 custom agents를 직접 spawn하도록 모델 전환
- **nested write-phased parity**: `feature_draft`, `implementation_plan`, `implementation_review`, `spec_review`가 장문 산출물 생성 시 `write_phased`를 nested 사용하도록 구조 반영
- **Pre-flight 확장**: `_sdd/env.md`와 `.codex/config.toml`을 함께 읽어 `agents.max_depth`, `agents.max_threads` 등 실행 가능성을 점검
- **문서 갱신**: Platform Differences, Architecture Overview, AUTOPILOT_GUIDE, QUICK_START, WORKFLOW를 custom agent spawn 모델 기준으로 갱신
- 백업: 없음 (문서/구조 정렬)

#### v3.3.0 (2026-03-17)

- **Hard Rule #9 (Review-Fix 사이클 필수) 반영**: sdd-autopilot에 추가된 Hard Rule #9을 스펙에 반영 -- review 포함 파이프라인에서 review → fix → re-review 사이클 필수, 리뷰만 하고 끝나는 것 불허
- **implementation-review 단계 재분류**: "비핵심 단계"에서 "조건부 핵심 단계"로 승격 (review 포함 파이프라인에서는 핵심 단계로 취급, 실패 시 건너뛸 수 없음)
- **변경**: Common Hard Rules에 sdd-autopilot 전용 Hard Rule #9 추가, 2-Phase Orchestration 패턴 설명 보강, sdd-autopilot Process 필드 업데이트, Scenario 2b 설명 보강
- 백업: `_sdd/spec/prev/prev_main_20260317_180000.md`

#### v3.2.0 (2026-03-17)

- **sdd-autopilot 재개/부분 실행**: Step 0 (Pipeline State Detection) 추가 -- 기존 미완료 파이프라인 감지 및 재개/새로 시작 선택 지원
- **산출물 스캔 및 시작점/종료점 감지**: Step 1.4 추가 -- 사용자 요청에서 시작/종료 힌트 파싱, `_sdd/` 기존 산출물 관련성 판단으로 파이프라인 범위 조절
- **Pipeline Log Format 강화**: Meta 섹션(request, orchestrator 참조, scale, started, pipeline) + Status 테이블(5개 상태값: pending/in_progress/completed/failed/skipped) 추가
- **오케스트레이터 저장 위치 변경**: `_sdd/pipeline/` -> `.claude/skills/orchestrator_<topic>/SKILL.md` (재사용성 + 재개 기능 위해)
- **변경**: Artifact Map, Data Flow, Scenario 2b, Directory Structure 등 오케스트레이터 경로 일괄 업데이트
- 백업: `_sdd/spec/prev/prev_main_20260317_150000.md`

#### v3.1.0 (2026-03-17)

- **에이전트 non-interactive 전환**: 8개 파이프라인 에이전트에서 AskUserQuestion 완전 제거, Autonomous Decision-Making 패턴으로 대체
- **신규 디자인 패턴**: Autonomous Decision-Making 패턴 추가 (Core Design > Design Patterns)
- **변경**: 에이전트가 모호한 상황에서 자율 판단 후 근거를 출력에 기록하고, 추론 불가 항목은 Open Questions에 기록
- **변경**: marketplace.json에 sdd-autopilot 스킬 1개 + 에이전트 8개 등록
- **변경**: 스킬 디렉토리명 `autopilot` -> `sdd-autopilot` 리네임
- **변경**: Platform Differences 테이블에서 AskUserQuestion이 풀 스킬에서만 사용됨을 명시
- 백업: `_sdd/spec/prev/prev_main_20260317_120000.md`

#### v3.0.0 (2026-03-16)

- **아키텍처 변경**: 스킬 전용 → 스킬 + 에이전트 이중 아키텍처(dual architecture) 전환
- **신규**: sdd-autopilot 적응형 오케스트레이터 메타스킬 추가 (`.claude/skills/sdd-autopilot/`)
- **신규**: 8개 에이전트 정의 파일 생성 (`.claude/agents/`)
- **변경**: 8개 스킬을 Agent Wrapper 래퍼로 전환 (feature-draft, implementation-plan, implementation, implementation-review, ralph-loop-init, spec-review, spec-update-done, spec-update-todo)
- **신규**: `_sdd/pipeline/` 오케스트레이터 + 파이프라인 로그 시스템 설계
- **신규**: `docs/AUTOPILOT_GUIDE.md` sdd-autopilot 사용 가이드 추가
- **신규**: `_sdd/env.md`에 SDD-Autopilot Resources 섹션 추가
- **신규 디자인 패턴**: Agent Wrapper 패턴, 2-Phase Orchestration 패턴 추가
- 스킬 수: 19 → 20 (sdd-autopilot 추가), 에이전트 수: 1 → 9 (8개 파이프라인 에이전트 + write-phased)
- 백업: `_sdd/spec/prev/prev_main_20260316_120000.md`

#### v2.1.0 (2026-03-13)

- spec-create, spec-rewrite, spec-upgrade에 2-Phase Generation 패턴 추가
- 3개 미문서 스킬 추가 (spec-snapshot, guide-create, write-phased)
