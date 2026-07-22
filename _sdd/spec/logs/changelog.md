# Changelog

> 이 파일은 `_sdd/spec/main.md`의 버전별 변경 기록이다.

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
