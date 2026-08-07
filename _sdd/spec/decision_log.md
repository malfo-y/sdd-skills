# Decision Log

## 2026-08-07 - document producer single-home interfaces and deterministic snapshot preservation (v4.6.54 → v4.6.55, post-implementation sync)

### Context

`spec-summary`·`guide-create`·`spec-snapshot` 문서 producer의 runtime 미러와 output 자산을 감사했다. `spec-summary`와 `guide-create`는 output shape·schema·example이 SKILL 본문과 여러 reference/example에 중복돼 있었고, `spec-snapshot`은 source 보존·destination collision·root `summary.md` 병합 계약이 runtime별로 드리프해 결과의 결정성과 read-only 보장이 약했다.

### Decision

1. `spec-summary`는 runtime-local `references/summary-template.md`를 whitepaper output shape의 단일 홈으로 두고, 작성 직전 fenced skeleton을 verbatim으로 적용한다. SKILL은 input·current-evidence 판단·point-of-use load만 소유하며 output을 재소유하던 완성 example은 제거한다.
2. `guide-create`는 runtime-local `references/output-format.md`를 section schema·evidence/citation·confidence rubric의 단일 rich interface로 두고, 작성 직전 fenced structure를 verbatim/slot-only로 적용한다. 이 계약을 중복하던 compact/tool-gate reference와 confidence example은 제거한다.
3. `spec-snapshot`은 source 사전/사후 sorted path+SHA-256 manifest exact match를 read-only hard gate로 삼고, safe language slug·resolved direct-parent confinement·unused collision suffix로 destination을 결정한다. 모든 source Markdown relative path를 보존하며, exact metadata marker와 source `summary.md` present/absent 분기를 분리한다. Claude의 `user_invocable: true`만 runtime allowlist delta로 남기고 common 본문은 Codex와 맞춘다.
4. 세 producer는 runtime helper lifecycle을 정의하지 않고 main loop가 skeleton-first로 직접 작성·검증한다. `docs/SKILL_AUTHORING_NORMS.md` 14개 rubric은 각 target 인용으로 검증하되 임시 task 상세를 global spec에 복제하지 않는다.

### Rationale / Evidence

- implementation ledger는 `REVIEW_PASSED`이며 AC1–AC16이 모두 GREEN이다. implementation-review는 raw `C2 H8 M10`, duplicate-normalized `C1 H5 M5`였고 fix 1회 후 잔여 Critical/High/Medium은 0이다.
- 최종 검증은 SKILL 미러, summary/guide rich reference, snapshot schema·fixture·read-only hard gate, official validator 5/5 + Claude schema, 정확한 target `M10+D12`, stale runtime census 6/6, `NORMS_PASS 14/14`, `git diff --check`를 모두 통과했다.

### Changes

- `.claude/skills/spec-summary/`, `.codex/skills/spec-summary/` — concise producer + fenced whitepaper interface; duplicate example 제거
- `.claude/skills/spec-snapshot/SKILL.md`, `.codex/skills/spec-snapshot/SKILL.md` — deterministic preservation/collision/summary contract와 runtime allowlist parity
- `.claude/skills/guide-create/`, `.codex/skills/guide-create/` — output-format single home; duplicate/stale reference·example 제거
- `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md` — v4.6.55 current truth 승격 (본문 묶음 소유)
- `_sdd/drafts/_processed_2026-08-07_feature_draft_norms_p2_document_surfaces.md`, `_sdd/implementation/_processed_2026-08-07_implementation_ledger_norms_p2_document_surfaces.md` — 사용 input 처리 표시

## 2026-08-07 - spec template selection and point-of-use load interface (v4.6.53 → v4.6.54, post-implementation sync)

### Context

v4.6.53에서 `🚧 Planned`로 남긴 `spec-template-load-interface`를 구현했다. 기존 spec lifecycle producer는 compact/full 선택을 구조 분할과 명확히 분리하지 않았고, reference path와 temporary-spec shape 설명이 startup asset 목록·단계별 소비 지점·format reference에 중복돼 drift 위험이 있었다.

### Decision

1. `spec-create`와 `spec-upgrade`의 compact/full 선택은 파일 분할과 독립된 semantic-loss 기준을 사용한다. compact가 기본이며, 입력에 project motivation 또는 evaluated-alternative rationale가 있고 compact의 named slot이 그 고유 역할을 보존하지 못할 때만 full을 고른다.
2. 선택·load interface와 local path map은 실제 소비 단계가 단독 소유한다. `spec-create`는 Step 4 직전에 선택한 template 전체 skeleton만 읽어 verbatim 적용하고, Claude template을 authoring canonical, Codex template을 runtime invocation token만 다른 distribution mirror로 유지한다.
3. `spec-upgrade`는 Step 1의 conditional upgrade mapping, Step 2의 global format과 same-runtime `feature-draft` producer, Step 5의 selected template을 stage-local single home으로 둔다. migration은 선택한 fenced template만 verbatim/slot-only로 적용한다.
4. temporary-spec shape의 direct producer는 same-runtime `feature-draft`의 `Required Output`이다. `spec-format`의 stale `Temporary Spec Reference` 설명은 제거하고 global format만 소유하게 한다.

### Rationale / Evidence

- 예시 단어가 아니라 보존해야 할 의미 역할로 full 선택을 닫아 template heading 변화와 producer criterion의 결합을 줄이고, compact default를 결정적으로 유지한다.
- implementation ledger는 `REVIEW_PASSED`이며 AC1–AC10이 모두 GREEN이다. implementation-review는 raw `C0 H3 M3`, duplicate-normalized `C0 H3 M2`였고 fix 1회 후 잔여 Critical/High/Medium은 0이다.
- 최종 검증은 normalized SKILL 4/4, asset path 14/14, protected template/reference 8/8, protected hook/harness 24/24, validator 4/4와 Claude/Codex parity·`git diff --check`를 모두 통과했다.

### Changes

- `.claude/skills/spec-create/SKILL.md`, `.codex/skills/spec-create/SKILL.md` — compact default, semantic-loss criterion, selected whole-template verbatim load
- `.codex/skills/spec-create/references/{template-compact.md,template-full.md}` — Claude authoring canonical의 runtime-token distribution mirror
- `.claude/skills/spec-upgrade/SKILL.md`, `.codex/skills/spec-upgrade/SKILL.md` — mapping/global-format/same-runtime producer/selected-template stage-local load
- `.claude/skills/spec-upgrade/references/spec-format.md`, `.codex/skills/spec-upgrade/references/spec-format.md` — global format only; stale temporary-spec 설명 제거
- `_sdd/spec/main.md`, `_sdd/spec/components.md` — v4.6.54 current truth 승격 (본문 묶음 소유)
- `_sdd/drafts/_processed_2026-08-07_feature_draft_spec_template_load_interface.md`, `_sdd/implementation/_processed_2026-08-07_implementation_ledger_spec_template_load_interface.md` — 사용 input 처리 표시

## 2026-08-07 - spec-rewrite point-of-use references and single-home template (v4.6.52 → v4.6.53, post-implementation sync)

### Context

v4.6.52에서 `🚧 Planned`로 남겨 둔 P1 2/2의 둘째 slice `spec-rewrite-reference-interface`를 구현했다. 기존 `spec-rewrite`는 format·checklist·target template의 load 시점이 실제 소비 단계와 연결되지 않았고, temporary-spec schema와 plan/report producer interface가 reference와 단일 사용 example에 중복돼 있었다.

### Decision

1. `spec-rewrite`는 global/temporary/target shape 판별에 필요할 때만 `spec-format`, rewrite를 실행해 Step 2에 진입할 때만 `rewrite-checklist`, Step 3에서 target shape를 재구성할 때만 `template-compact`를 읽는 point-of-use interface를 사용한다. rewrite가 필요 없으면 Steps 2–4와 관련 asset을 읽지 않고 종료한다.
2. `template-compact`를 current temporary-spec exact skeleton의 단일 홈으로 두고 fenced skeleton을 verbatim 적용한다. 허용 변경은 placeholder 치환, 필요 row/task 반복, 조건부 block 제거로 한정하며 heading·marker·field order를 보존한다. `spec-format`과 `rewrite-checklist`는 자기 고유 역할과 template pointer만 소유한다.
3. SKILL Step 2·4가 plan/report producer interface의 단일 소스다. 이를 단일 사용처에서 재구현하던 Claude/Codex `rewrite-plan.md`·`rewrite-report.md` example 네 파일은 제거한다.
4. `spec-rewrite-reference-interface`만 current truth로 승격한다. `spec-template-load-interface`는 구현·검증 evidence가 없으므로 `🚧 Planned`로 유지한다.

### Rationale / Evidence

- implementation ledger는 `REVIEW_PASSED`이고 AC1–AC16이 모두 GREEN이다. 최종 변경 집합은 surviving reference/SKILL 8 `M` + redundant example 4 `D`, `+106/-140`이며, exact producer template·conditional load·no-rewrite exit·verbatim 적용·example 제거가 모두 검증됐다.
- implementation-review는 raw `C0 H4 M8`, duplicate-normalized `C0 H4 M7`이었고 fix 1회 후 잔여 Critical/High/Medium은 0이다.
- `spec-template-load-interface`는 이번 draft의 planned scope이지만 ledger의 구현·validation 대상이 아니므로 evidence 없이 승격하지 않는다.

### Changes

- `.claude/skills/spec-rewrite/SKILL.md`, `.codex/skills/spec-rewrite/SKILL.md` — conditional point-of-use load, no-rewrite exit, verbatim/slot-only target reshape
- `.claude/skills/spec-rewrite/references/{rewrite-checklist.md,spec-format.md,template-compact.md}`, `.codex/skills/spec-rewrite/references/{rewrite-checklist.md,spec-format.md,template-compact.md}` — exact temporary-spec skeleton single-home과 pointer-only supporting references
- `.claude/skills/spec-rewrite/examples/{rewrite-plan.md,rewrite-report.md}`, `.codex/skills/spec-rewrite/examples/{rewrite-plan.md,rewrite-report.md}` — 단일 사용 producer 재구현 example 제거
- `_sdd/spec/main.md`, `_sdd/spec/components.md` — v4.6.53 current truth 승격과 `spec-template-load-interface` planned 유지 (본문 묶음 소유)
- `_sdd/drafts/_processed_2026-08-07_feature_draft_spec_rewrite_reference_interface.md`, `_sdd/implementation/_processed_2026-08-07_implementation_ledger_spec_rewrite_reference_interface.md` — 사용 input 처리 표시

## 2026-08-07 - spec-review deterministic status and disposition interface (v4.6.51 → v4.6.52, post-implementation sync)

### Context

v4.6.51에서 세 feature로 분할해 `🚧 Planned`로 둔 P1 2/2 중 첫 slice `spec-review-deterministic-interface`를 구현했다. 기존 `spec-review`는 drift status와 spec disposition decision을 예시 중심으로 설명하고, 고정 code-analysis metrics와 output의 값 재열거가 producer 판정과 report consumer 사이에 중복돼 있었다.

### Decision

1. drift status는 evidence 충분성 → 한쪽 surface의 확인된 부재 → 양쪽 비교 순서로 판정하고 `ALIGNED | DRIFT | MISSING | UNTESTED` 중 정확히 하나를 고른다. `MISSING`만 `SPEC_MISSING | IMPLEMENTATION_MISSING` direction을 사용하며 그 외 direction은 `N/A`다.
2. spec disposition은 material uncertainty를 먼저 `NEEDS_DISCUSSION`으로 라우팅하고, 검증된 spec-side drift만 `SYNC_REQUIRED`, 그 밖에는 `SPEC_OK`로 둔다. implementation-only drift는 `SPEC_OK`와 implementation next action으로 분리한다.
3. Output의 Drift Summary와 Decision은 각각 status/decision producer를 가리키며 enum을 다시 복제하지 않는다. revision/history/change-set 분석은 scope 선택이나 finding을 실제로 뒷받침할 때만 bounded evidence로 기록하고, 사용하지 않으면 생략한다.
4. `spec-review-deterministic-interface`만 current truth로 승격한다. `spec-rewrite-reference-interface`와 `spec-template-load-interface`는 구현 evidence가 없으므로 각각 `🚧 Planned`로 유지한다.

### Rationale / Evidence

- implementation ledger는 `REVIEW_PASSED`이고 AC1–AC10이 모두 GREEN이다. Claude/Codex mirror exact parity, validator 2/2, baseline 허용 블록 normalization, scoped target set, report path, `git diff --check`가 모두 PASS했다.
- implementation-review는 raw `C0 H0 M2`, duplicate-normalized `C0 H0 M1`이었고 single-home fix 1회 후 잔여 Critical/High/Medium은 0이다.
- 나머지 두 slice는 이번 implementation ledger의 대상이 아니므로 evidence 없는 planned truth를 승격하지 않는다.

### Changes

- `.claude/skills/spec-review/SKILL.md`, `.codex/skills/spec-review/SKILL.md` — ordered drift status·decision interface, producer pointer 기반 output, 조건부 code-analysis evidence
- `_sdd/spec/main.md` — v4.6.52, 첫 slice current truth 승격과 나머지 두 slice의 개별 `🚧 Planned` 유지 (본문 묶음 소유)
- `_sdd/drafts/_processed_2026-08-07_feature_draft_spec_quality_interface.md`, `_sdd/implementation/_processed_2026-08-07_implementation_ledger_spec_review_interface.md` — 사용 input 처리 표시

## 2026-08-07 - spec quality interface를 세 feature로 분할 (v4.6.50 → v4.6.51, pre-implementation planned sync)

### Context

P1 2/2 `spec-quality-interface`는 review verdict 판정, rewrite reference 소비, template 선택·load라는 서로 다른 producer/consumer interface를 하나의 todo로 묶고 있었다. 현재 input은 feature draft뿐이고, 첫 feature의 두 `spec-review` target에는 diff가 없으며 신규 implementation ledger도 없다.

### Decision

1. umbrella todo를 `spec-review-deterministic-interface` → `spec-rewrite-reference-interface` → `spec-template-load-interface` 순서의 세 개별 `🚧 Planned` 항목으로 분할한다.
2. draft의 `current`는 실행 순서일 뿐 구현 status가 아니므로, 코드와 validation evidence가 생기기 전에는 세 항목 모두 `PLANNED / NOT_IMPLEMENTED`로 유지한다.
3. task별 contract·AC·Target Files는 draft에만 두고 global spec에 복제하지 않는다. 이 분할은 repo-wide invariant나 persistent navigation을 바꾸지 않으므로 `components.md`·`usage-guide.md`는 건드리지 않는다.

### Rationale / Evidence

- verdict enum, rewrite 산출물, template load는 change element·target set·검증면이 독립적이라 순차 구현·검증이 가능한 단위로 나누는 편이 더 명확하다.
- `.claude/skills/spec-review/SKILL.md`·`.codex/skills/spec-review/SKILL.md` target diff는 0이고, `spec_quality_interface` 관련 implementation ledger는 없다. 따라서 완료 승격은 없다.

### Changes

- `_sdd/spec/main.md` — v4.6.51, P1 2/2 umbrella todo를 세 개의 ordered `🚧 Planned` todo로 교체
- `_sdd/drafts/2026-08-07_feature_draft_spec_quality_interface.md` — 다음 implementation 입력으로 원래 경로와 내용을 유지하며 process/rename하지 않음

## 2026-08-07 - spec bootstrap hook contract progressive disclosure (v4.6.49 → v4.6.50, post-implementation sync)

### Context

v4.6.49에서 `🚧 Planned`로 남긴 P1 1/2 `spec-bootstrap-disclosure`를 구현했다. `spec-create`·`spec-upgrade`의 상시 로드 본문에 hook event·matcher, settings merge case, runtime JSON, trust, validation/report 세부가 흩어져 있어, 하네스를 생성·보완하지 않는 호출도 모든 설치 계약을 부담하고 single-home drift 위험이 있었다.

### Decision

1. 훅 설치의 rich contract는 package-local `references/hook-installation.md`로 옮긴다. `.claude/skills/spec-create/references/hook-installation.md`를 authoring canonical로 두고, Claude `spec-upgrade`와 Codex `spec-create`·`spec-upgrade`의 세 사본은 exact distribution mirror로 유지한다.
2. `spec-create`는 top-level AC·Hard Rule·Step 3e·Validation·Output에 하네스 생성/병합 시 local reference를 읽고 전부 적용하는 trigger와 verification/report pointer만 남기며, event/matcher·merge·runtime·trust 세부는 reference가 소유한다.
3. `spec-upgrade`는 자기 package의 local reference를 직접 읽고 partial/legacy 설치를 current dual-runtime 상태로 보완하며 재실행 diff를 없애는 upgrade-only repair 판단을 본문에 남긴다. `spec-create`의 존재나 cross-skill reference에 의존하지 않는다.
4. P1 1/2 `spec-bootstrap-disclosure`는 current truth로 승격하고, P1 2/2 `spec-quality-interface`는 별도 `🚧 Planned`로 유지한다.

### Rationale / Evidence

- 하나의 authoring home과 세 package-local exact mirror를 사용해 작성 기준을 단일화하면서도 각 skill의 독립 배포를 보존했다.
- 최종 SKILL 4면은 합계 `+48/-250`(net `-202`)이고, literal target 8개·official validator 4/4·protected asset 28개 SHA-256 exact match를 확인했다.
- implementation-review gate `C0 H2 M5`를 fix 1회로 해소했다. watchdog original-result 보존, unsupported Claude version no-fire/no-error, non-SDD handler·malformed runtime continuation, single-home 잔존 세부를 복원·정리한 후 잔여 Critical/High/Medium은 0이다.

### Changes

- `.claude/skills/spec-create/{SKILL.md,references/hook-installation.md}`, `.codex/skills/spec-create/{SKILL.md,references/hook-installation.md}` — authoring canonical + distribution mirror, top-level trigger/pointer 전환
- `.claude/skills/spec-upgrade/{SKILL.md,references/hook-installation.md}`, `.codex/skills/spec-upgrade/{SKILL.md,references/hook-installation.md}` — local reference + partial/legacy repair ownership, cross-skill 의존 없음
- `_sdd/spec/main.md`, `_sdd/spec/components.md` — v4.6.50 current truth, P1 1/2 완료·P1 2/2 planned 반영 (본문 묶음 소유)
- `_sdd/drafts/_processed_2026-08-07_feature_draft_norms_p1_spec_lifecycle.md`, `_sdd/implementation/_processed_2026-08-07_implementation_ledger_norms_p1_spec_lifecycle.md` — 사용 input 처리 표시

## 2026-08-07 - spec lifecycle P1을 두 feature로 분리 (v4.6.48 → v4.6.49, pre-implementation planned sync)

### Context

`docs/SKILL_AUTHORING_NORMS.md`의 P1 적용 대상에는 hook 설치 상세의 progressive disclosure와 spec lifecycle skill의 deterministic quality interface가 함께 있었지만, 두 변경은 change element·검증면·구현 target이 겹치지 않는다. 현재 입력은 feature draft뿐이며 target code diff, 신규 hook reference, implementation artifact가 없어 구현 완료로 승격할 evidence가 없다.

### Decision

1. P1을 `spec-bootstrap-disclosure` → `spec-quality-interface` 순서의 두 독립 feature로 나누고 각각 별도 `🚧 Planned` todo로 유지한다. draft에서 첫 feature가 `current`로 지칭돼도 이는 실행 순서일 뿐 구현 status가 아니며, evidence가 생기기 전에는 current truth로 승격하지 않는다.
2. `spec-bootstrap-disclosure`는 `spec-create`·`spec-upgrade`의 hook 설치 상세를 조건부 package-local rich reference로 옮긴다. Claude `spec-create` reference 하나를 authoring canonical로 두고 나머지 세 사본을 exact 배포 mirror로 유지해 각 skill의 독립 배포를 보존한다. skill 본문에는 trigger, upgrade-only repair ownership, reference pointer만 남긴다.
3. `spec-quality-interface`는 `spec-review`의 criterion·status/decision enum과 spec lifecycle producer들의 template/reference/example 선택·load·output interface를 완결한다. legacy 7-section temporary-spec reference는 현재 producer shape로 고친 뒤에만 load한다.
4. 구현 전 global surface에는 두 planned item과 그 rationale만 남긴다. task별 AC·Target Files·reference section 상세는 temporary draft가 소유하며 `components.md`·`usage-guide.md`에 복제하지 않는다.

### Rationale / Evidence

- hook 설치 상세는 하네스 생성·병합 때만 필요하고 100줄 이상이라 조건부 rich reference가 맞지만, 실행 trigger와 upgrade 고유 repair 책임은 항상 읽는 skill 본문에 남아야 한다.
- cross-skill 단일 reference는 독립 배포를 깨므로 authoring canonical 1개 + package-local exact mirror 3개를 선택한다.
- `references/hook-installation.md` 0개, 네 current skill target diff 0개, 관련 implementation artifact 0개를 확인했다. 따라서 두 delta의 status는 모두 `PLANNED / NOT_IMPLEMENTED`다.

### Changes

- `_sdd/spec/main.md` — v4.6.48 → v4.6.49, `spec-bootstrap-disclosure`와 `spec-quality-interface`를 별도 `🚧 Planned` todo로 추가
- `_sdd/drafts/2026-08-07_feature_draft_norms_p1_spec_lifecycle.md` — 구현 입력으로 원래 경로와 내용을 유지하며 이번 sync에서 process/rename하지 않음

## 2026-08-07 - implementation producer·review pair 규범 다이어트 (v4.6.47 → v4.6.48, post-implementation sync)

### Context

v4.6.47에서 `🚧 Planned`로 남긴 P0 5/5 `implementation-pair-diet`를 구현했다. post-review fix 시점·횟수와 실행 중 분할 handoff는 실제 코드를 쓰는 `implementation`이 소비하지만 review wrapper·agent도 같은 정책을 다시 설명했고, reviewer의 no-file·Fresh Verification 경계와 plan 없는 호출의 대화 digest도 여러 절에 흩어져 drift 위험이 있었다.

### Decision

1. `implementation`을 post-review fix 정책의 단일 홈으로 둔다. gate 단일 패스와 Critical/High/Medium fix 1회, Low 판단을 producer가 소유하며 review pair는 finding 분류·relay만 담당한다. 실행 중 규모 초과 신호는 `feature-draft`의 `분할 방법 (롤링)`을 가리키고 draft 형식을 복제하지 않는다.
2. implementation ledger에는 source task에서 달라진 판단이나 새 edge case를 이유·처리와 함께 남기는 `계획 이탈·발견` 필드를 추가한다. 테스트/check 가정 오류를 세는 `계약 오류 선언 횟수`와 분리해 compact 뒤에도 두 원인을 구별한다.
3. `implementation-review` wrapper는 review-only 경계와 plan 없는 호출의 대화 digest ownership을 한 곳으로 합치되 correctness/simplicity 두 렌즈, shard relay topology, Claude/Codex runtime adapter를 유지한다.
4. `implementation-review-agent`는 no-file/no-spawn 경계를 단일 홈으로 합치고 producer의 fix 횟수를 재서술하지 않는다. Step 3은 Hard Rule의 `Fresh Verification` canonical home을 가리키며, Codex의 bounded helper 예외를 제거해 no-spawn 계약 충돌을 해소한다.

### Rationale / Evidence

- 6개 target surface에서 AC1–AC15가 모두 MET였고 structural checks는 RED에서 GREEN으로 전환됐다.
- implementation-review aggregate `C0 H0 M8`은 7개 고유 원인으로 정리해 fix 1회에 반영했고 잔여 Critical/High/Medium은 0이다. root 포함 concurrency 4 제한에 따른 runtime reviewer 3+1 dispatch deviation은 ledger에 기록했다.
- 최종 target diff는 `+41/-29`이며 mirror/core parity, TOML parse, Source Pointer, runtime/frontmatter, validator, status census, `git diff --check`가 모두 PASS했다.

### Changes

- `.claude/skills/implementation/SKILL.md`, `.codex/skills/implementation/SKILL.md` — fix 정책 canonical home, rolling split pointer, `계획 이탈·발견` ledger 필드
- `.claude/skills/implementation-review/SKILL.md`, `.codex/skills/implementation-review/SKILL.md` — review-only/no-plan digest ownership 통합, 두 렌즈·relay·runtime adapter 보존
- `.claude/agents/implementation-review-agent.md`, `.codex/agents/implementation-review-agent.toml` — no-file/no-spawn 단일 홈, fix-count 재천명 제거, Fresh Verification pointer
- `_sdd/spec/main.md`, `_sdd/spec/components.md` — v4.6.48 current truth와 P0 5/5 완료 반영 (본문 묶음 소유)
- `_sdd/drafts/_processed_2026-08-07_feature_draft_implementation_pair_diet.md`, `_sdd/implementation/_processed_2026-08-07_implementation_ledger_implementation_pair_diet.md` — 사용 input 처리 표시

## 2026-08-07 - feature-draft producer·plan-review verifier 규범 다이어트 (v4.6.46 → v4.6.47, post-implementation sync)

### Context

v4.6.46에서 `🚧 Planned`로 남긴 P0 4/5 `feature-draft-pair-diet`를 구현했다. `feature-draft`에는 질문·output template·AC evidence·minimum-code 판단이 있었고, `plan-review-agent`는 producer가 소유한 Propagation·평가 세부 계약과 evidence/minimum-code 권고를 다시 설명해 drift 위험이 있었다.

### Decision

1. `feature-draft`의 질문은 로컬 탐색으로 해소되지 않았고 답이 아키텍처·범위·Target Files를 바꾸는 unknown에만 발동한다. 한 번에 한 질문씩 영향이 큰 순서로 묻고, 무인 실행은 합리적 가정과 근거를 `Open Questions`에 기록한다.
2. inline `Required Output` fenced template을 output structure의 단일 소스로 유지한다. 작성 단계는 이를 verbatim 출발 skeleton으로 사용해 heading·marker·field order를 보존하되, placeholder 치환과 필요한 Propagation row·task block·AC·Target File row/block 반복, producer 규칙이 허용한 조건부 section 삭제는 허용한다.
3. AC evidence는 재현 가능한 test/check 출력인 1등급 또는 명시 rubric·reviewer 판정·인용 근거를 갖춘 2등급으로 닫는다. 두 등급은 모두 이진 판정·외부 증거·제3자 반박 가능성을 만족해야 하며, minimum code는 요청 동작 또는 관측 위험에 직접 추적되는 최소 변경으로 판단한다.
4. `plan-review-agent`는 Propagation/평가 세부를 복제하지 않고, 해당 판정이 필요할 때 current `feature-draft` producer contract을 읽어 검증한다. source를 읽을 수 없으면 기억으로 재구성하지 않고 `Verification Weakness=UNKNOWN`과 limitation을 반환하며, evidence/minimum-code 권고는 인용된 근거를 해결하는 가장 작은 plan change 규칙 하나로 합친다.
5. Claude/Codex `plan-review` wrapper는 2-lens single-pass dispatch·merge relay·runtime adapter만 소유하는 thin entrypoint로 감사했고 `NO_CHANGE`로 닫았다. P0 5/5 `implementation-pair-diet`는 `🚧 Planned`로 유지한다.

### Rationale / Evidence

- 변경 target 4면과 `NO_CHANGE` wrapper 2면을 검증했고 AC1–AC15가 모두 MET다.
- checker contract deviation은 T1 2건·T2 1건을 명시적으로 교정한 뒤 HEAD에서 RED를 다시 확인했다. implementation-review aggregate `C1 H0 M2`는 fix 1회로 해소했고 잔여 Critical/High/Medium은 0이다.
- feature-draft exact mirror, 정규화 plan-review-agent core parity, Codex TOML parse, wrapper diff 0, `quick_validate.py` 2면, `git diff --check`가 모두 PASS했다.

### Changes

- `.claude/skills/feature-draft/SKILL.md`, `.codex/skills/feature-draft/SKILL.md` — 질문 발동·무인 가정, inline template 소비, AC evidence 2등급, minimum-code 추적성
- `.claude/agents/plan-review-agent.md`, `.codex/agents/plan-review-agent.toml` — current producer contract 검증 pointer, source 부재 `UNKNOWN`, smallest-change 규칙 단일화
- `.claude/skills/plan-review/SKILL.md`, `.codex/skills/plan-review/SKILL.md` — thin wrapper 감사 `NO_CHANGE`
- `_sdd/spec/main.md` — v4.6.46 → v4.6.47, P0 4/5 승격 및 P0 5/5 planned 유지 (본문 묶음 소유)
- `_sdd/drafts/_processed_2026-08-07_feature_draft_feature_draft_pair_diet.md`, `_sdd/implementation/_processed_2026-08-07_implementation_ledger_feature_draft_pair_diet.md` — 사용 input 처리 표시

## 2026-08-07 - pr-review 입력·UNTESTED 경계 다이어트 (v4.6.45 → v4.6.46, post-implementation sync)

### Context

v4.6.45에서 `🚧 Planned`로 남긴 P0 3/5 `pr-review-diet`를 구현했다. 기존 `pr-review`의 두 reviewer 입력은 공통 정보가 자유 산문으로 전달됐고, wrapper가 agent 반환 계약과 read-only 경계를 다시 설명했으며, 실제 test execution evidence가 없을 때의 `UNTESTED` 신호가 통합 verdict까지 닫히지 않았다.

### Decision

1. `pr-review` wrapper와 correctness/simplicity reviewer가 공유하는 입력을 `Changed Files`, `PR Diff`, `PR Metadata`, `PR Discussion`, `Spec Context`, `Validation Evidence`, `Report Slug` 순서의 정확한 7필드 `PR Review Input`으로 고정한다.
2. wrapper는 PR·CI/local validation evidence를 수집·redact해 공통 입력을 생산하고, reviewer별 반환 형식은 재정의하지 않고 각 agent가 소유한 계약을 소비한다. 두 read-only reviewer의 병렬 dispatch와 wrapper 단일 작성자 경계는 유지한다.
3. correctness reviewer가 read-only 경계와 Fresh Verification을 소유한다. 검증은 CI evidence → `_sdd/env.md`가 가리키는 실행 가능한 local validation → 사유가 있는 `UNTESTED` 순서로 판정하고, code citation만으로 test status를 `MET`로 만들지 않는다. test-dependent 항목에 실행 evidence가 없으면 wrapper는 `UNTESTED`를 자동 승인이나 실패로 해석하지 않고 `NEEDS DISCUSSION`으로 라우팅하며, non-test-dependent·명시적 N/A 항목은 이 신호에서 제외한다.
4. simplicity reviewer는 `Changed Files`와 `PR Diff`로 범위를 고정하되 validation status를 재판정하지 않는다. checklist의 verdict 복제 기준은 제거하고 runtime별 wrapper Step 4를 canonical verdict 기준으로 가리킨다.
5. P0 4/5 `feature-draft-pair-diet`와 P0 5/5 `implementation-pair-diet`는 계속 `🚧 Planned`로 유지한다.

### Rationale / Evidence

- wrapper 2면, checklist 2면, correctness agent 2면, simplicity agent 2면의 8개 target surface에서 구현을 검증했고 AC1–AC17이 모두 MET다.
- implementation-review aggregate는 fix 전 `C0 H1 M2`였으며 fix 1회 뒤 잔여 Critical/High/Medium은 0이다.
- 6개 producer/consumer surface의 7필드 입력 exact parity, checklist pointer 2면, Codex TOML 2개 parse, 정규화 agent core parity, target census, `git diff --check`가 모두 PASS했다.

### Changes

- `.claude/skills/pr-review/SKILL.md`, `.codex/skills/pr-review/SKILL.md` — 7필드 입력 producer, evidence 수집·redaction, agent-owned 반환 소비, `UNTESTED` verdict 경계
- `.claude/skills/pr-review/references/review-checklist.md`, `.codex/skills/pr-review/references/review-checklist.md` — verdict 복제 제거 및 runtime wrapper Step 4 포인터
- `.claude/agents/pr-review-agent.md`, `.codex/agents/pr-review-agent.toml` — 7필드 correctness consumer와 read-only/Fresh Verification canonical 경계
- `.claude/agents/simplicity-review-agent.md`, `.codex/agents/simplicity-review-agent.toml` — 공통 입력 consumer와 validation 비판정 경계
- `_sdd/spec/main.md` — v4.6.45 → v4.6.46, P0 3/5 승격 및 P0 4/5~5/5 planned 유지 (본문 묶음 소유)
- `_sdd/drafts/_processed_2026-08-07_feature_draft_pr_review_diet.md`, `_sdd/implementation/_processed_2026-08-07_implementation_ledger_pr_review_diet.md` — 사용 input 처리 표시

## 2026-08-07 - spec-sync digest interface and single-home agent rules (v4.6.44 → v4.6.45, post-implementation sync)

### Context

v4.6.44에서 `🚧 Planned`로 남긴 P0 2/5 `spec-sync-agent-diet`를 구현했다. implemented sync의 본문·기록 분할 dispatch는 같은 사실·분류·버전·결정 정보를 소비하지만, wrapper와 agent 사이 digest 형식이 자유 산문이었고 status routing, legacy input fallback, processed-input 소유 규칙이 agent 여러 절에 반복돼 계약 drift 위험이 있었다.

### Decision

1. implemented sync digest의 producer/consumer 계약을 `## Implemented Sync Digest` 아래 `Delta List`, `Classification Basis`, `Spec Version`, `Decision Title`의 비어 있지 않은 네 필드로 고정한다. 두 wrapper는 같은 digest를 본문·기록 호출에 전달하고, 두 agent는 같은 형식으로 소비한다.
2. agent의 status 4분류는 `Status 분류 (Routing)`, legacy input discovery는 `Input Sources`, `_processed_` rename의 본문·기록 묶음 소유권은 `호출자 표면 한정`을 각각 canonical home으로 사용한다. 다른 절은 해당 heading을 참조하고 판정 목록이나 소유 규칙을 재서술하지 않는다.
3. status enum의 의미, evidence 기반 승격, 본문/기록 표면 분할, dispatch lifecycle, report 필드는 변경하지 않는다. P0 3/5 `pr-review-diet`, 4/5 `feature-draft-pair-diet`, 5/5 `implementation-pair-diet`는 계속 `🚧 Planned`로 유지한다.

### Rationale / Evidence

- T1/T2/T3 structural 검사는 RED exit 1에서 GREEN exit 0으로 전환됐고 AC1–AC12가 모두 MET다.
- implementation-review correctness shard finding은 0건이었다. simplicity Medium 3건은 fix 1회로 반영했고, 최종 digest census, single-home 검사, agent mirror semantics, TOML parse, `git diff --check`가 모두 PASS했다.

### Changes

- `.claude/skills/spec-sync/SKILL.md`, `.codex/skills/spec-sync/SKILL.md` — 고정 4필드 digest producer 계약
- `.claude/agents/spec-sync-agent.md`, `.codex/agents/spec-sync-agent.toml` — digest consumer 계약과 status·fallback·processed-input 규칙의 canonical home 정리
- `_sdd/spec/main.md` — v4.6.44 → v4.6.45, P0 2/5 승격 및 P0 3/5~5/5 planned 유지 (본문 묶음 소유)
- `_sdd/drafts/_processed_2026-08-07_feature_draft_spec_sync_agent_diet.md`, `_sdd/implementation/_processed_2026-08-07_implementation_ledger_spec_sync_agent_diet.md` — 사용 input 처리 표시

## 2026-08-07 - SKILL_AUTHORING_NORMS P0 1/5 autopilot-simplicity 규범 다이어트 완료 (v4.6.43 → v4.6.44, post-implementation sync)

### Context

v4.6.43에서 `🚧 Planned`로 고정한 5개 롤링 feature 중 첫 번째 `autopilot-simplicity-diet`를 구현했다. 대상은 Claude/Codex `sdd-autopilot`과 `simplicity-review-agent` 4파일이며, orchestration·review 계약은 유지하면서 producer 내부 알고리즘 재서술과 공통 방어 규칙의 중복을 줄이는 작업이다.

### Decision

1. `autopilot-simplicity-diet`를 current truth로 승격한다. `sdd-autopilot`은 chain order, no-approval, `_sdd/spec/` 쓰기의 spec-sync 위임, 플랫폼별 runtime delta를 유지하고 Workflow Position 다이어그램·producer 내부 알고리즘 재서술·형식 리터럴·수치형 질문 knob를 제거한다.
2. `simplicity-review-agent`는 5개 차원, severity·return·path 계약과 플랫폼별 실행 경계를 유지하고 correctness/read-only/falsifiability의 반복 재서술을 축약한다.
3. P0 2/5 `spec-sync-agent-diet`, 3/5 `pr-review-diet`, 4/5 `feature-draft-pair-diet`, 5/5 `implementation-pair-diet`는 계속 `🚧 Planned`로 유지한다.

### Rationale / Evidence

- 3개 task의 structural RED→GREEN을 완료했고 14/14 AC가 모두 MET다.
- TOML parse와 `git diff --check`가 PASS했고, implementation-review correctness는 전부 MET다. simplicity Medium 3건은 fix 1회로 반영했으며 post-fix regression 뒤 Critical/High/Medium 잔여는 0이다.
- 4파일 diff는 28 insertions / 74 deletions이고, 현재 line count는 Claude/Codex autopilot 71/70줄, Claude/Codex simplicity reviewer 92/93줄이다.

### Changes

- `.claude/skills/sdd-autopilot/SKILL.md`, `.codex/skills/sdd-autopilot/SKILL.md` — orchestration 고유 계약과 runtime delta만 남도록 다이어트
- `.claude/agents/simplicity-review-agent.md`, `.codex/agents/simplicity-review-agent.toml` — 공통 재천명 축약, 플랫폼별 경계 보존
- `_sdd/spec/main.md` — v4.6.43 → v4.6.44, P0 1/5 승격 및 P0 2/5~5/5 planned 유지 (본문 묶음 소유)
- `_sdd/implementation/_processed_2026-08-07_implementation_ledger_norms_diet_remaining_pairs.md` — post-implementation evidence 처리 표시

## 2026-08-07 - SKILL_AUTHORING_NORMS P0 나머지 5쌍 롤링 분할 고정 (v4.6.42 → v4.6.43, pre-implementation planned sync)

### Context

discussion 쌍의 규범 다이어트는 v4.6.42에서 완료됐다. 나머지 핵심 spec/implementation 스킬과 agent를 한 번에 수정하면 단일 컨텍스트를 넘으므로, feature draft의 Part 1 분할 목록을 P0 롤링 작업으로 고정한다. 첫 feature `autopilot-simplicity-diet`는 plan-review를 마쳤지만 구현 산출물과 validation evidence는 없다.

### Decision

1. 🚧 Planned: P0는 `autopilot-simplicity-diet` → `spec-sync-agent-diet` → `pr-review-diet` → `feature-draft-pair-diet` → `implementation-pair-diet`의 5개 feature를 순차 실행한다. 각 feature는 구현·검증된 뒤 해당 todo만 current truth로 승격한다.
2. 🚧 Planned: `Propagation Surfaces` 계약은 `feature-draft`를 canonical home으로 두고, `plan-review`는 복제하지 않고 검증만 한다.
3. 🚧 Planned: 공통 다이어트 기준은 지시·판단 주체의 단일 홈화, 근거 없는 수치·방어 규칙의 기준화, 하드 게이트 존치 시 근거 병기다. Final Check 1줄은 유지하고 완료된 discussion 쌍과 하네스 변경은 범위에서 제외한다.

### Rationale / Evidence

- 구현 코드와 `_sdd/implementation/` validation evidence가 없으므로 5개 항목 모두 PLANNED다. plan-review 완료는 구현 승격 evidence로 사용하지 않는다.
- 쌍 단위 분할은 각 feature가 독립적으로 검증·승격될 수 있게 하며, 미구현 항목을 current contract와 섞지 않는다.

### Changes

- `_sdd/spec/main.md` — v4.6.42 → v4.6.43, P0 5개 todo를 개별 `🚧 Planned` 항목으로 추가
- `_sdd/drafts/_processed_2026-08-07_feature_draft_norms_diet_remaining_pairs.md` — planned sync 처리 표시; 첫 feature의 Part 2 task를 보존해 다음 implementation 입력으로 계속 검색 가능

## 2026-08-07 - discussion 스킬 쌍 규범 다이어트 (SKILL_AUTHORING_NORMS 적용 1호) (v4.6.41 → v4.6.42, post-implementation sync)

### Context

v4.6.41에서 추가한 `docs/SKILL_AUTHORING_NORMS.md`(Claude 5 세대 제작 규범 체크리스트)를 실제 스킬에 적용한 사례가 없었다. discussion 스킬 쌍(claude+codex 미러)을 규범 리뷰한 결과 finding F1~F9 — 파일 생성 규칙 반복 서술, AGENTS.md §5 work log 규약과의 충돌, 인라인 요약 템플릿(재구성 위험), 무근거 수치 노브, 의사코드 블록, 과잉 예시 표, 질문 우선순위 기준 부재 등 — 가 나왔다.

### Decision

discussion 스킬 쌍을 규범 다이어트하는 적용 1호로 삼는다 (claude SKILL.md 436→320줄, codex 400→275줄).

1. **요약 템플릿 단일 소스화**: discussion 요약 템플릿의 단일 소스는 `references/summary-template.md`(claude·codex 양쪽)이고, Step 4는 이를 Read 후 verbatim 복사(`[...]` 슬롯만 치환)로 소비한다 — 신규 contract.
2. **파일 규칙 단일화 + work log 규약 예외**: 파일 생성 제한 규칙을 Hard Rules 1곳으로 통합하고, "호출 환경의 work log 규약에 따른 기록은 예외" 문구로 AGENTS.md §5 충돌을 해소한다 (직접 인용 대신 일반화 — 플러그인 이식성).
3. **수치 노브 4건 기준화**: 연속 2라운드 비판 금지·매 3라운드 요약·stagnation 2회·재방문 1회를 기준 서술로 전환하거나 근거 병기.
4. **의사코드 산문화 + 예시 표 question-guide 위임**: 3.1/3.2 의사코드 블록을 산문으로 대체하고, 깊이 신호·비판 유형·수렴 신호 표의 상세 예시는 question-guide 참조로 위임 (깊이 신호 예시 표를 question-guide에 신설해 정보 보존).
5. **아키텍처-변경 질문 우선 기준 추가**: 질문 선택 전략에 "답이 아키텍처(구조·범위·후속 작업 방향)를 바꾸는 질문 우선" 기준 추가 (field-guide 반영).

### Alternatives

- Final Check 삭제 계열 finding은 d903052 존치 결정(하드 게이트는 실측 근거가 있을 때만 걷어냄)으로 기각.
- work log 예외 문구를 AGENTS.md 직접 인용으로 쓰는 안은 플러그인 이식성 저하로 기각 — "호출 환경의 work log 규약"으로 일반화.

### Rationale / Evidence

- 행동 로직(커버리지·게이트·카테고리 4종·근거 유형 4종 enum·Gate 구조)은 의미 변경 없음 — 다이어트는 서술 층위에 한정.
- 게이트: plan-review CLEAR(M2 L2 반영), implementation-review 전 AC MET, 합산 M6 L5 → fix 1회 반영(깊이 신호 예시 question-guide 표 신설, Step 4 템플릿 위임으로 codex sources 불일치 동시 해소 등). 재리뷰 임계(M≥5) 도달로 추가 리뷰 권장은 advisory로 기록.
- fix 후 census 재실행 전건 통과(변형형 grep 잔존 0·헤더 대응 5:5·템플릿 쌍 identical). codex 미러는 3-way merge로 고유 delta(interactive-only·request_user_input·최신성 HR) 보존.

### Changes

- `.claude/skills/discussion/SKILL.md` — 436→320줄 (F1·F2·F5~F9 + Step 4 verbatim 소비 지시)
- `.claude/skills/discussion/references/summary-template.md` — 신규 (템플릿 단일 소스)
- `.claude/skills/discussion/references/discussion-question-guide.md` — 깊이 신호 예시 표 신설
- `.codex/skills/discussion/SKILL.md` — 400→275줄 (3-way merge 전파)
- `.codex/skills/discussion/references/summary-template.md` — 신규 (템플릿 미러)
- `.codex/skills/discussion/references/discussion-question-guide.md` — 미러 전파
- `_sdd/spec/main.md` — v4.6.41 → v4.6.42 (본문 묶음 소유)

## 2026-08-07 - Claude 5 세대 스킬 제작 규범 문서 추가 (docs/SKILL_AUTHORING_NORMS.md) (v4.6.40 → v4.6.41, post-implementation sync)

### Context

Claude 5 세대 모델 대상 스킬/agent/하네스 제작에 적용할 규범이 repo 안에 정리돼 있지 않았다. Anthropic 블로그 2편 — "The New Rules of Context Engineering for Claude 5 Generation Models"와 "A Field Guide to Claude Fable: Finding Your Unknowns" — 이 담고 있는 규범(80% 프롬프트 제거, 규칙→judgment 전환, progressive disclosure, unknowns 실천법)을 이 repo의 제작 체크리스트로 증류하기로 했다.

### Decision

`docs/SKILL_AUTHORING_NORMS.md` 신규 문서(82줄, 한국어)를 추가한다. 구성: §1 배경(80% 프롬프트 제거, 규칙→judgment) / §2 Then→Now 전환 표 / §3 제작 체크리스트(본문·구조 progressive disclosure·rich reference·인터페이스) / §4 Unknowns 실천법→SDD 단계 매핑 표 / §5 기존 repo 규범과의 관계(부합점 + 하드 게이트 유지 조건 "걷어낼 자격은 실측이 준다"). 순수 참고 문서로, 계약·스킬 로직·미러 전파 표면은 없다.

### Alternatives

기존 docs 문서에 병합하는 안을 검토했으나 사용자가 신규 문서로 지시해 기각했다.

### Rationale / Evidence

- 문서 완성 상태 검증: TODO/TBD grep 0건, `git diff --check` 통과.
- 경량 경로 채택 근거: 순수 참고 문서로 계약·스킬 로직·미러 전파 없음 — 신규 파일 조건은 형식상 걸리나 전파 표면 부재로 경량 경로가 타당하다고 판단.
- §5는 기존 repo 규범(하드 게이트·structural check 등)과의 부합점을 명시하고, 게이트 제거는 실측 근거가 있을 때만 허용한다는 조건을 남긴다.

### Changes

- `docs/SKILL_AUTHORING_NORMS.md` — 신규 (Claude 5 세대 제작 규범 체크리스트)
- `_sdd/spec/main.md` — v4.6.40 → v4.6.41 (본문 묶음 소유)

## 2026-08-07 - Codex/Claude hook parity and dual-setting runtime acceptance (v4.6.39 → v4.6.40, post-implementation sync)

### Context

하네스 훅은 Claude 설정과 실행 경로에만 집중돼 있어 Codex 소비 repo에서 같은 work-log gate, context 주입, watchdog 계약을 설치·실행·검증할 수 없었다. 또한 한 runtime의 설정 파일이 손상됐을 때 다른 runtime까지 함께 실패하거나, 비-SDD 설정을 덮어쓰지 않으면서 두 설정을 독립적으로 병합한다는 영속 계약이 없었다.

### Decision

1. 하네스 훅 4종(`worklog-gate.sh`, `worklog-context.sh`, `harness-context.sh`, `agent-watchdog.sh`)은 self-host와 `spec-create`/`spec-upgrade`의 Claude·Codex reference surface를 동일 실행 자산으로 유지한다. `SessionStart`는 runtime별 `hookSpecificOutput.additionalContext` JSON을 내고, `PreToolUse`는 work-log gate, `PostToolUse`는 advisory watchdog을 담당한다.
2. `spec-create`와 `spec-upgrade`는 `.claude/settings.json`과 `.codex/hooks.json`을 각각 독립 병합한다. 비-SDD handler와 top-level key를 보존하고, 한 runtime 파일이 손상되면 그 파일만 건너뛰어 반대 runtime 설치는 계속하며, 반복 실행은 멱등이어야 한다.
3. runtime acceptance는 정적 parity만으로 닫지 않는다. 격리된 실제 Codex skill invocation fixture와 Claude Code smoke에서 trust boundary, `SessionStart`/clear/`PreToolUse`/watchdog lifecycle, manifest 안정성, bypass 부재를 검증한다.

### Alternatives

Claude 설정만 canonical로 유지하고 Codex를 문서상 호환으로만 취급하거나, 두 runtime 설정을 단일 all-or-nothing 설치로 묶는 방안을 기각했다. 전자는 실제 Codex lifecycle을 보장하지 못하고, 후자는 한쪽의 손상으로 정상인 반대 runtime까지 설치하지 못하게 한다.

### Rationale / Evidence

- 스크립트 4종 × 5 surface가 byte-identical이고 `bash -n`을 통과했으며, SKILL mirror와 JSON canonical map도 동일성을 확인했다.
- 격리 fixture의 manifest가 안정적으로 유지됐고 Codex 0.146.0과 Claude 2.1.223에서 실제 lifecycle을 검증했다. current-repo Codex hook trust는 정확한 repo 범위로 승인됐으며 trust bypass는 없었다.
- global config 최종 SHA1은 `e9bbd36054cbd784565c250e277c9d9c40851de4`다. 세 feature draft의 AC가 모두 체크됐고 implementation-review C2/H8/M4 fix pass를 완료했다.

### Changes

- Feature 1 — 공용 `.claude/hooks` 실행 경로와 Claude/Codex reference surface의 훅 4종 parity, runtime별 SessionStart JSON·PreToolUse gate·PostToolUse advisory 계약
- Feature 2 — `.claude/settings.json` + `.codex/hooks.json` dual installation, 독립 merge·보존·손상 격리·멱등 계약과 Codex self-host 설정
- Feature 3 — 격리 Codex invocation fixture, Codex trust/lifecycle acceptance, Claude smoke, parity·manifest·no-bypass 검증
- `_sdd/spec/main.md` — v4.6.39 → v4.6.40 (본문 묶음 소유)
- 입력 draft 3개와 runtime-acceptance implementation ledger를 `_processed_`로 마킹

## 2026-08-06 - 리뷰 게이트 Low finding 선택적 fix (correctness/plan-review 렌즈 3조건 · simplicity Low advisory 유지) (v4.6.38 → v4.6.39, post-implementation sync)

### Context

기존 리뷰 게이트 정책은 Low finding을 무조건 advisory/logged follow-up으로만 처리했다(과거 단언: line 1231 `주관적 취향은 Low(advisory)`, line 1361 `review-fix severity boundary: Critical/High/Medium은 review-fix blocker이고 Low는 advisory/logged follow-up이다`, line 1369 `Low advisory 정책은 loop 종료 조건과 fix 대상 범위를 일치시킨다`). 사용자가 "판단해서 고칠만한건 고치게" — Low여도 값싸고 명백히 이득이면 같은 change scope 안에서 고치도록 요청했다.

### Decision

리뷰 게이트 Low finding을 무조건 advisory에서 **3조건 AND 게이트 기반 선택적 fix**로 전환한다.

1. **correctness 렌즈 Low**(`implementation-review-agent`): **저비용 AND 명백히 이득 AND 현재 change scope 내** 세 조건을 모두 만족할 때만 조건부 fix, 아니면 advisory 유지. 최종 fix/후속 권고 여부의 기준은 호출 스킬 소관.
2. **plan-review Low**(`feature-draft` 게이트): 동일 3조건(현재 draft scope 내)을 모두 만족할 때만 조건부 반영.
3. **simplicity 렌즈 Low**: 선택적 fix 대상에서 **제외** — 주관적 취향이라 churn 방지 목적으로 advisory 유지.

### Alternatives

simplicity Low까지 선택 fix에 포함하는 안을 검토했으나 기각 — simplicity Low는 객관적 위반이 아닌 주관적 취향이라(line 1231의 falsifiable-only gating 닻과 일관), fix 대상에 넣으면 취향 기반 churn을 유발한다.

### Rationale / Evidence

- 3조건 AND 게이트에서 `현재 scope 내`가 **load-bearing conjunct**다 — 이 conjunct가 scope creep(별건 리팩터로의 확장)을 차단해 단일 패스·fix 1회 불변식과 loop 수렴을 보존한다. 저비용·명백한 이득만으로는 범위를 넘는 fix를 허용하지 않는다.
- 범위 한정: plan-review Low + implementation-review correctness Low만 선택 fix 대상이고, simplicity Low는 advisory 유지 → gating exit 조건(`critical=high=medium=0`)은 무변경, Low는 여전히 loop 종료를 막지 않는다.
- 검증: 구현 완료(git diff 6파일, structural check grep/diff로 **12 AC MET**), implementation-review 2렌즈 Blocker CLEAR·Medium 2·Low 1, review-fix로 `implementation/SKILL.md` L109·`feature-draft/SKILL.md` L89 중첩 bullet 재구성.

### Supersedes

이 결정은 기존 "Low는 무조건 advisory" 단언을 **supersede**한다 — 구체적으로 line 1231(`주관적 취향은 Low(advisory)`는 simplicity 렌즈에 한정 존치되고 correctness/plan-review Low는 3조건 선택 fix로 갈린다), line 1361(`Low는 advisory/logged follow-up이다`의 categorical 서술), line 1369(`Low advisory 정책`)의 무조건성을 제한한다. 기존 줄은 수정하지 않으며 이 entry가 최신 상태를 정의한다. Critical/High/Medium fix 1회·단일 패스·gating exit 불변식은 그대로다.

### Changes

- `.claude/skills/implementation/SKILL.md` / `.codex/skills/implementation/SKILL.md` L109 -- correctness 렌즈 Low 3조건 조건부 fix, simplicity 렌즈 Low advisory 유지
- `.claude/skills/feature-draft/SKILL.md` / `.codex/skills/feature-draft/SKILL.md` L89 -- plan-review Low 3조건(현재 draft scope 내) 조건부 반영
- `.claude/agents/implementation-review-agent.md` / `.codex/agents/implementation-review-agent.toml` L77 -- Low = 호출자의 선택적 fix/후속 권고(기준은 호출 스킬 소관)
- `_sdd/spec/main.md` -- v4.6.38 → v4.6.39 (본문 묶음 소유)
- 입력: `_sdd/drafts/2026-08-06_feature_draft_review_low_selective_fix.md` → `_processed_` 마킹

## 2026-08-05 - Agent Watchdog 훅 — 하네스 훅 자산 4호 (advisory) (v4.6.37 → v4.6.38, post-implementation sync)

### Context

review agent가 20분씩 도는 원인(예: `uv run --with torch` 반복 재설치)을 사용자가 매번 알 수 없어, 5분 초과 agent에게 스스로 점검·전환하게 하는 훅을 사용자가 요청했다. 2026-08-05 실험 1·2(work log 항목 11·12)로 성립 조건이 검증됐다 — 훅은 subagent tool call에 발동하고, agent_id는 subagent payload에만 존재하며, PostToolUse decision:block reason이 subagent 모델에 전문 전달·지시 수행된다.

### Decision

하네스 훅 자산 4호 `agent-watchdog.sh`(PostToolUse)를 추가한다 — subagent 장기실행(첫 tool call 후 300s+) 시 자기점검 nudge(시간 도둑 자평·캐시/재사용 전환)를 전달하고, cooldown 300s, advisory·fail-open, jq→python3 fallback. 새 contract 2건: ① 하네스 훅 자산 목록 3→4개 ② watchdog은 advisory 자산 — "조용히 무력화되지 않는다" guardrail의 경고 의무는 강제 자산(게이트)에 한정한다.

### Alternatives

worklog-context.sh 경고 확장(경고 의무를 watchdog까지 확대)을 검토했으나 기각 — 5미러 표면 확대 대비 이득이 미미하다.

### Rationale / Evidence

- 실험 1·2(work log 항목 11·12)로 성립 조건 3건(subagent 발동·agent_id 키·block reason 전문 전달) 검증 완료.
- 알려진 한계: nudge는 tool call 경계에서만 전달된다 — 단일 장시간 명령 중간 개입은 불가하며, 후속 PreToolUse 패턴 차단 레버 후보로 스코프 아웃.
- 검증: structural check RED 12 → GREEN **28/28**, 변이 7종 전량 kill, implementation-review(correctness 5 shard + simplicity 2묶음) fix 전 C/H 0 · M 1(도달 불가 줄바꿈 이스케이프 no-op → fix) · L 5 advisory.

### Changes

- 스크립트 5경로(정본 + 미러 3 + dogfooding, md5 5-way 일치) -- `agent-watchdog.sh` 추가
- spec-create/spec-upgrade SKILL 4파일 -- 설치 계약 갱신(훅 자산 개수 리터럴 3→4, census 확장 패턴 `세 스크립트|스크립트 3개|세 훅|훅 3개|셋 다|두 항목` 잔존 0)
- `.claude/settings.json` -- PostToolUse 등록
- `_sdd/spec/main.md` -- v4.6.37 → v4.6.38 (본문 묶음 소유)
- 입력: `_sdd/drafts/2026-08-05_feature_draft_agent_watchdog_hook.md` → `_processed_` 마킹

## 2026-08-05 - work log 모델명 병기를 전 항목으로 일반화 (v4.6.36 → v4.6.37, post-implementation sync)

### Context

같은 날 v4.6.36이 도입한 하네스 §5 "리뷰 게이트 수치에만 실행 모델명 병기" 규칙의 범위 확대 — supersede가 아니라 일반화이며, 게이트 병기 예시는 모델 override 시 규칙으로 존치한다. 게이트 수치만 태그하면 draft 작성·구현 등 producer 단계의 모델 귀속이 여전히 유실된다.

### Decision

§5 work log 항목 형식을 `## <순번/HH:MM> <제목> (<실행 모델명>)`로 확장해 모든 항목 제목에 실행 모델명을 병기한다. 게이트 한정 bullet은 다음으로 대체한다 — "모델명은 모든 항목 제목에 병기하고, 게이트를 다른 모델로 돌렸으면 그 수치 옆에도 적는다(예: `plan-review (opus-5): H2 M2`) — 모델별 finding 밀도 비교용".

### Alternatives

게이트 수치 한정 병기(v4.6.36 원안) 유지를 검토했으나, 항목 제목 병기는 비용이 동일하면서 모든 SDD 단계 산출물이 모델별로 추적되므로 사용자 제안으로 범위를 확대했다.

### Rationale / Evidence

- 게이트만 태그하면 producer 단계(draft 작성·구현)의 모델 귀속이 유실된다 — 제목 병기로 전 단계 산출물의 모델별 추적이 가능해진다.
- 검증: git diff(브랜치 chore/worklog-model-tag, 미커밋) 기준 적용 표면 5곳 전수(파일당 +2/-2), §5 블록 md5 일치 검증 완료.

### Changes

- `AGENTS.md` -- §5 work log 항목 형식을 `## <순번/HH:MM> <제목> (<실행 모델명>)`로 확장, 게이트 한정 bullet을 전 항목 병기 규칙으로 대체
- `.claude/skills/spec-create/references/agents-harness-template.md`, `.claude/skills/spec-upgrade/references/agents-harness-template.md`, `.codex/skills/spec-create/references/agents-harness-template.md`, `.codex/skills/spec-upgrade/references/agents-harness-template.md` -- 동일 문면 전파
- `_sdd/spec/main.md` -- v4.6.36 → v4.6.37 (본문 묶음 소유)

## 2026-08-05 - work log 게이트 수치에 실행 모델명 병기 (v4.6.35 → v4.6.36, post-implementation sync, 경량 경로)

### Context

모델 회귀 가설(예: "Opus 5가 잔실수가 많다")이 2026-08-05 진단에서 UNCONFIRMED로 남았다 — 원인은 work log의 게이트 기록에 실행 모델 표본이 없어 모델별 finding 밀도를 사후 비교할 수 없었기 때문이다.

### Decision

하네스 §5 work log 규약에 bullet 1줄을 추가한다 — 리뷰 게이트(plan-review·implementation-review) 결과 수치를 기록할 때는 실행 모델명을 병기한다(예: `plan-review (opus-5): H2 M2`). 태그 누적으로 모델별 finding 밀도를 사후 비교 가능하게 만든다.

### Alternatives

별도 계측 파일 신설, A/B 실험 설계를 검토했으나, 비용이 사실상 0인 기록 규약 확장(기존 work log bullet 1줄)을 채택했다.

### Rationale / Evidence

- 경량 경로 판정: 새 contract/invariant 없음 · 신규 파일 없음 · 전파 표면 5곳 전수 열거 + md5/diff 검증 — 성질 3조건 전부 충족.
- 검증: git diff(브랜치 chore/worklog-model-tag) 기준 5개 표면 동일 문면 추가, §5 블록 md5 일치 확인.

### Changes

- `AGENTS.md` -- §5 work log 규약에 실행 모델명 병기 bullet 추가
- `.claude/skills/spec-create/references/agents-harness-template.md`, `.claude/skills/spec-upgrade/references/agents-harness-template.md`, `.codex/skills/spec-create/references/agents-harness-template.md`, `.codex/skills/spec-upgrade/references/agents-harness-template.md` -- 동일 문면 전파 (템플릿 포함이므로 소비 repo 하네스에도 적용)
- `_sdd/spec/main.md` -- v4.6.35 → v4.6.36 (본문 묶음 소유)

## 2026-08-05 - resume-only implementation ledger 도입 (v4.6.34 → v4.6.35, post-implementation sync)

### Context

긴 구현 중 컨텍스트 요약(compact)으로 task 상태가 유실되는 통로가 있었다(2026-08-05 토론 결정 6~9). 이를 닫되 감사 로그가 아닌 **resume pointer**로 한정한다 — 재실행으로 복원 가능한 정보는 기록 대상에서 제외해 (b) structural-check 구현의 무상태 복원력과 중복되지 않게 한다.

### Decision

1. `implementation` SKILL 2벌에 `## Implementation Ledger (resume pointer)` 절을 신설한다 — 모든 실행이 `_sdd/implementation/<YYYY-MM-DD>_implementation_ledger_<slug>.md`를 생성하고, 같은 slug의 기존 ledger가 있으면 새로 만들지 않고 이어쓴다(분열 금지). 기록 기준 = **재실행으로 복원할 수 없는 사실만**(출력 전문·서술형 진행기 금지). task당 4상태 `READY → RED_CONFIRMED → GREEN_CONFIRMED → DELTA_CLOSED`만 사용하며 (c) test-free task는 `READY → DELTA_CLOSED`로 직행한다. 재개 시 미완료 task는 stale 상태를 신뢰하지 않고 무조건 fresh 재판정하고, DELTA_CLOSED task는 현재 diff와 모순이 보일 때만 fresh 재확인한다. 마감 AC→증거 테이블의 기록처를 ledger로 통합하고(채팅 노출 유지), 게이트 fix는 `Review fix delta` 단일 블록으로 기록한다.
2. SDD_SPEC_DEFINITION 한·영 §6에 구현 측 기록처로 implementation ledger를 명시한다.
3. AUTOPILOT_GUIDE 한·영 산출물 목록에 ledger를 추가한다.

사용자 조정 2건: ① ledger = 마감 AC→증거 테이블의 점진 작성본(이중 기록 제거) ② 재개 시 미완료 task는 stale 상태 신뢰 없이 무조건 fresh 재판정.

### Rationale / Evidence

- 긴 구현 중 compact로 task 상태가 유실되는 통로를 닫는다(토론 결정 6~9). resume pointer 한정으로 기록 범위를 재실행 불가 사실로 좁혀, 재실행으로 복원 가능한 영역을 담당하는 (b) structural-check 구현의 무상태 복원력과 역할이 겹치지 않는다.
- **도입 관측 exit 조건**: 도입 후 수 회의 구현에서 ledger가 실제 재개에 읽힌 적이 있는지 관측하고, 전혀 사용되지 않으면 회수를 재검토한다(같은 날 D&A 5필드 회수 사례와 동일 기준 — 실사용 증거 없는 형식은 유지하지 않는다).
- 검증: structural check RED **24 FAIL** → GREEN, post-fix 회귀 **35/35 pass**(exit 0), 변이 확인 **3회 kill**, 미러 byte parity, implementation-review 6 reviewer(correctness 3 shard + simplicity 2 묶음) Medium 3 전부 fix 반영·Low 5 advisory 잔존(전체 status 갱신 시점·증거 발췌 수준·en 글롭 비대칭·AUTOPILOT_GUIDE 헤더 날짜 stale·ko 글롭 밀도).

### Changes

- `.claude/skills/implementation/SKILL.md`, `.codex/skills/implementation/SKILL.md` -- `## Implementation Ledger (resume pointer)` 절 신설 + 마감 증거 테이블 기록처 통합 (byte-identical 미러)
- `docs/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_SPEC_DEFINITION.md` -- §6 구현 기록처로 implementation ledger 명시
- `docs/AUTOPILOT_GUIDE.md`, `docs/en/AUTOPILOT_GUIDE.md` -- 산출물 목록에 ledger 추가
- `_sdd/spec/main.md` -- v4.6.34 → v4.6.35
- 입력: `_sdd/drafts/2026-08-05_feature_draft_implementation_ledger.md` → `_processed_` 마킹

## 2026-08-05 - feature-draft D&A(Decisions and Assumptions) 5필드 계약 제거 — 산문 복귀 (v4.6.33 → v4.6.34, post-implementation sync)

### Context

v4.6.33(같은 날, 커밋 99a6bd5)이 producer-reviewer 정렬로 두 계약을 도입했다 — 조건부 `Decisions and Assumptions` 5필드와 조건부 `Propagation Surfaces` 5열 표. 이 중 D&A 5필드는 실패 이력이 없는 곳에 형식을 추가한 것이었다: 유용한 알맹이(사용자 확인이 필요한 결정의 구현 전 노출)는 기존 `Open Questions` 표면이 이미 담당하고, 5필드 구조는 형식 준수 검사로 퇴화하기 쉽다(산문 규칙 > 의사코드 관측). 반면 `Propagation Surfaces` 계약은 실측 실패 이력(다중 표면 누락 재발) 기반이다.

### Decision

사용자 확정 결정으로 D&A 5필드 계약만 제거하고 산문으로 복귀한다. `Propagation Surfaces` 계약은 유지한다.

1. producer(feature-draft SKILL 2벌)에서 조건부 `Decisions and Assumptions` 5필드 템플릿과 `중요 결정만 기록` Hard Rule을 제거한다. Process 1은 propagation 식별만 유지한다.
2. reviewer(plan-review-agent 2벌)의 AC3·Hard Rule 7·Step 2·Step 4를 99a6bd5^ 산문(숨은 결정 surfacing 산문 규칙 + Step 4 4불릿 + decision markers 추출)으로 복귀한다. Hard Rule 8(Propagation Surface Coverage)·Step 3 계단 propagation 검증·Verification Weakness propagation 문구는 유지한다.
3. SDD_SPEC_DEFINITION 한·영 canonical 구조에서 D&A 항목을 제거하고 재번호한다(3=Propagation Surfaces, 4=Part 2, 5=Open Questions). 스켈레톤 D&A 2줄을 제거한다.

### Rationale / Evidence

- D&A 5필드는 실패 이력 없는 곳에 추가된 형식이며, 알맹이는 기존 `Open Questions`가 담당하고 구조는 형식 준수 검사로 퇴화하기 쉽다(산문 규칙 > 의사코드). `Propagation Surfaces`는 실측 실패 이력 기반이라 유지 — 두 계약의 근거 비대칭이 결정의 축이다.
- structural check **70/70 pass**(RED 45 FAIL → GREEN, exit 0), 커버리지 델타 변이 확인 **1/1 kill**, producer 미러 byte parity, TOML 파싱 통과, census 계약 고유 리터럴 **0건**(허용 예외: plan-review-agent 2벌 Step 4 헤딩 `Review Decisions and Assumptions`), implementation-review 6 reviewer(correctness 4 shard + simplicity 2 묶음) finding **0**.

### Changes

- producer(feature-draft SKILL 2벌)·reviewer(plan-review-agent 2벌)·SDD_SPEC_DEFINITION 한·영에서 D&A 5필드 계약 제거·산문 복귀, `Propagation Surfaces` 계약은 유지
- `_sdd/spec/main.md` -- v4.6.33 → v4.6.34
- 입력: `_sdd/drafts/2026-08-05_feature_draft_decisions_assumptions_contract_removal.md` → `_processed_` 마킹

## 2026-08-05 - feature-draft producer-review contract alignment (v4.6.32 → v4.6.33, post-implementation sync)

### Context

`feature-draft` producer가 중요한 설계 판단과 여러 동기화 표면에 걸친 변경을 명시적으로 연결하지 않으면, `plan-review`가 결정 근거·필수 전파 표면·task 소유권을 같은 기준으로 검증할 수 없다. 반대로 모든 결정과 일반 다중파일 변경에 추가 표를 강제하면 실행 상세가 늘고 Target Files를 중복하게 된다.

### Decision

1. 결과 방향·Target Files·task boundary를 바꿀 수 있는 중요 결정만 조건부 `Decisions and Assumptions` 5필드로 기록하고, 중요 결정이 없으면 섹션을 생략한다. `plan-review`는 같은 조건과 필드를 검사한다.
2. 동일 change element가 둘 이상의 동기화 표면에 걸릴 때만 조건부 `Propagation Surfaces` 5열 표를 만들고, 각 행을 정확히 한 owner task의 Target Files·AC에 연결한다. 일반 다중파일은 발동 조건이 아니며, 변형 표기 전수 제거만 별도 census task로 닫는다.
3. `plan-review`는 발동 여부·required surface 실측·discovery 기대 집합·단일 owner·task 연접 오류를 새 smell 없이 기존 `Verification Weakness`와 Glob→Grep→Read 계단에서 검사한다.

### Rationale / Evidence

- 두 계약은 한두 구현 파일만 읽어서는 안정적으로 복구되지 않고, producer·reviewer·정의 문서 등 둘 이상의 workflow surface에 공통 적용되며, 누락 시 repo-level planning과 review 판단이 어긋나므로 Repo-wide Invariant Test를 통과한다.
- 조건부 발동은 중요한 판단과 실제 전파 의무만 드러내면서 일반 다중파일 변경의 ceremony와 Target Files 중복을 피한다. 기존 smell과 도구 계단에 검사를 흡수해 reviewer 분류 체계도 늘리지 않는다.
- 구현 6파일과 RED→GREEN, canonical assertions **12/12**, 동일 checker mutant **12/12 killed**, producer byte parity, TOML parse, exact census, post-fix regression을 확인했고 implementation-review finding fix까지 완료했다.

### Changes

- producer·reviewer 계약과 한·영 draft 정의를 조건부 decision/propagation 규칙으로 정렬
- `_sdd/spec/main.md` -- v4.6.32 → v4.6.33
- 입력: `_sdd/drafts/2026-08-05_feature_draft_producer_review_contract_alignment.md` → `_processed_` 마킹

## 2026-08-03 - SDD 체인에 경량 경로(light path) 명문화 — 성질 3조건 + 하네스 템플릿 4벌 전파 (v4.6.30 → v4.6.31, post-implementation sync)

### Context

직전 회차(v4.6.30 재리뷰 권고)에서 사용자 합의로 풀 체인을 생략한 "경량 경로"가 ad-hoc 관행으로 처음 등장했다. 판정 기준이 문서화돼 있지 않으면 경로 선택이 회차마다 재협상되고, 소비 repo의 하네스에는 이 관행이 아예 전파되지 않는다. 이 feature는 그 관행을 성질 기준으로 명문화해 하네스 §3의 계약으로 승격한다.

### Decision

1. **경량 경로 적격 판정 기준**: 성질 3조건 — ① 새 contract/invariant 없음 ② 신규 파일 없음(work log 제외) ③ 전파 표면(미러·섹션 리터럴·등록 목록) 전수 열거 + 각각 diff/grep 검증 — 을 **모두** 충족하는 소규모 변경은 풀 체인 대신 직접 구현 → 검증 → spec-sync로 처리할 수 있다.
2. **보수 기본값**: 하나라도 아니거나 판정이 애매하면 풀 체인이 기본값이다. 새 계약·agent 반환 형식·dispatch 구조 변경·rename/전파류(census 필요)·신규 skill/agent 추가는 항상 풀 체인이다.
3. **경량 경로 불변식**: 경량이어도 브랜치·Execute→Verify·spec-sync·work log는 생략 불가이며, 채택 시 판정 근거 1줄을 work log에 남긴다.
4. **전파**: 규칙 문면은 repo `AGENTS.md` §3 + 하네스 템플릿 4벌(`{.claude,.codex}/skills/{spec-create,spec-upgrade}/references/agents-harness-template.md`) §3에 verbatim 동일하게 들어간다 — 앞으로 두 스킬이 초기화하는 모든 repo의 하네스에 적용된다. 전파 표면 5곳은 체인 리터럴 예외 문장과 같은 전파 규율이다.

### Rationale / Evidence

- 직전 feature(게이트 재리뷰 권고, PR #42)를 이 경로로 처리한 실측이 근거다 — 규칙은 관행의 사후 명문화이며, 경로 선택 소관은 스킬이 아니라 하네스다(SDD 스킬 본문 무변경).
- 구현 검증: git diff 5표면 각 +2줄(삭제 0, §3 구간 내부 한정), verbatim 동일성은 diff 3쌍 무출력 + §3 구간 추출 문자열 비교로 확인. structural check RED(12요소 + 의도표면 5 누락 FAIL) → GREEN 11 PASS, 변이 5종 전량 검출.
- 게이트: plan-review(3-dispatch, 벽시계 ~149s) High 1(census allowlist가 PR #42 spec 이력 표면 누락)·Low 2 전량 반영; implementation-review(N+2=5) 전 AC MET, C/H/M 0, Low 1(census 패턴 `lightpath` 붙임 변형 미커버 — 실질 영향 0, advisory 잔존).

### Changes

- `AGENTS.md` §3 말미 + 하네스 템플릿 4벌 §3 -- 경량 경로 규칙 문단 verbatim 추가 (각 +2줄)
- `_sdd/spec/main.md` -- v4.6.30 → v4.6.31 (§2 Guardrails에 경량 경로 결정 승격; §3 현재 운영 제약의 simplicity 반환 다이어트 🚧 Planned 항목에 첫 관측 n=1 반영 — 판정 유보; 융합돼 있던 `spec-sync` 2-shard 벽시계 항목을 별도 불릿으로 분리 복원)
- `_sdd/spec/logs/changelog.md` -- v4.6.31 entry 추가
- 입력: `_sdd/drafts/2026-08-03_feature_draft_light_path_harness.md` → `_processed_` 마킹

## 2026-08-03 - 게이트 finding 과다 시 재리뷰 권고 메시지 (Critical+High ≥ 3 또는 Medium ≥ 5, advisory-only) (v4.6.29 → v4.6.30, post-implementation sync)

### Context

체인 게이트는 단일 패스 + fix 1회로 닫히므로, finding이 유난히 많았던 회차에서도 fix 후 재검증 없이 마감된다. 재리뷰 loop 재도입은 기각된 방향이라(무승인·단일 패스 불변식), finding 과다를 사용자에게 알리고 재실행 판단을 넘기는 최소 장치가 필요했다.

### Decision

1. **advisory 재리뷰 권고 메시지**: `feature-draft`·`implementation` 품질 게이트에서 finding 반영 후, 게이트 반환의 합산 finding(fix 전 기준)이 **Critical+High ≥ 3 또는 Medium ≥ 5**였으면 마감 메시지에 수치와 함께 해당 게이트(`plan-review`/`implementation-review`) 1회 추가 실행을 권장하는 1줄을 출력한다 — 권고 출력만 하고 추가 리뷰를 자체 실행하지 않는다(단일 패스 유지, 실행 여부는 사용자 판단).
2. **셈 기준**: fix 전 게이트 반환의 합산 severity — `implementation-review`는 shard 합산 요약 그대로(dedup 없음), Low는 advisory라 셈에서 제외.
3. **소유 주체**: 셈과 출력은 반환을 합산하는 producer SKILL 메인 루프 소유 — reviewer agent 계약 무변경.

### Rationale / Evidence

- 체인 불변식(무승인·review 단일 패스·fix 1회)은 유지된다 — advisory는 계약을 바꾸지 않고 메시지만 추가하며, 게이트는 relay만 한다는 기존 설계와 일관.
- 경량 경로 채택(사용자 합의): 4파일 몇 줄짜리 advisory 문구라 draft/게이트를 생략했다. 미러 동일성은 diff로 검증됨(4파일 +4/-2, claude/codex 문면 동일).

### Changes

- `.claude/skills/feature-draft/SKILL.md` · `.codex/skills/feature-draft/SKILL.md` -- §품질 게이트 bullet에 권고 규칙 추가 (문면 동일 미러)
- `.claude/skills/implementation/SKILL.md` · `.codex/skills/implementation/SKILL.md` -- 마감 §3 품질 게이트 bullet 목록에 1줄 추가 (문면 동일 미러)
- `_sdd/spec/main.md` -- v4.6.29 → v4.6.30 (§2 단일 패스 계약 불릿에 advisory 규칙 반영)
- `_sdd/spec/components.md` · `_sdd/spec/usage-guide.md` -- 마감 재서술 표면에 임계값 복제 없는 짧은 참조 추가
- 입력: draft 없음(경량 경로) — `_processed_` 마킹 대상 없음

## 2026-08-01 - simplicity-review-agent 반환 다이어트 — plan-review 울타리 규칙 이식 (v4.6.28 → v4.6.29, post-implementation sync)

### Context

plan-review 반환 다이어트(v4.6.28)의 전파 판단이 Follow-up으로 남아 있었다. `simplicity-review-agent`는 반환 구조가 plan-review와 동형(`Findings` + 차원 판정 PASS 접기 + `Assumptions`)인데 울타리 규칙이 없었고, 이번 feature의 `implementation-review` 게이트에서 구계약 reviewer들이 실제로 "스캔 요지" 비-finding 단락을 반환에 실어 열거 습성의 실재가 확인됐다. 진단은 v4.6.28과 동일하다 — 시간은 "적어야 할 양"이 결정한다.

### Decision

1. **반환은 Step 4 항목이 전부다**: `simplicity-review-agent` 미러 2벌(각 +3/-1)의 Step 4 반환에 울타리 규칙 1문장을 추가한다 — 확인했으나 finding이 아닌 스캔 결과는 열거하지 않는다, 반환은 위 항목이 전부다, 차원 한정 여부와 무관하며, 줄이는 것은 출력이지 Step 2 스캔 범위가 아니다.
2. **자체 검증은 새 항목을 만들지 않는다**: 규칙 준수를 기존 자체 검증 `AC3`에 흡수한다(범위 한정어 "Step 4 항목 밖에").
3. **전파 범위 결정 — reviewer 2종 제외 (사용자 결정)**: `implementation-review-agent`·`pr-review-agent`는 Verification ledger(MET 행 증거 결속) 계약이라 이번 범위에서 제외한다. ledger 예외 문장이 필요한 별도 feature로 파킹한다.

### Rationale / Evidence

- **습성의 실재**: 이번 implementation-review 게이트에서 구계약 reviewer들이 "스캔 요지" 비-finding 단락을 반환에 실었다 — 울타리 부재가 실제 출력 부풀림으로 나타남을 관측했다.
- **검증**: structural check RED 4 FAIL → GREEN 9 PASS, 변이 7종 전량 검출. implementation-review 게이트 finding 0 (correctness 97s ∥ simplicity 참조 55s ∥ 국소 57s).
- **부수 실측 — plan-review 다이어트 첫 관측 (발효 후 첫 게이트)**: 실측 렌즈 114s ∥ 판단 72s. 실측 렌즈 절대값 역대 최저이고 열거 섹션이 소멸했다(압축 요약 1문장 잔존). 긍정 신호이며 n=1로 누적을 계속한다.
- **simplicity 다이어트 자체 효과는 미관측 (발효 전)**: 첫 관측은 머지 + 플러그인 갱신 후 다음 implementation-review 게이트다.

### Changes

- `.claude/agents/simplicity-review-agent.md` -- Step 4 반환에 울타리 규칙 1문장, 자체 검증 `AC3`에 준수 흡수
- `.codex/agents/simplicity-review-agent.toml` -- 같은 두 지점의 codex 미러 반영
- `_sdd/spec/main.md` -- v4.6.28 → v4.6.29
- 입력: `_sdd/drafts/2026-08-01_feature_draft_simplicity_return_diet.md`

### Follow-up

- `implementation-review-agent`·`pr-review-agent`로의 전파는 Verification ledger 예외 문장이 필요한 **별도 feature로 파킹**됐다 — 이번 범위에서 다루지 않았다.
- simplicity 다이어트 효과의 첫 관측은 발효 후 다음 implementation-review 게이트에서 수행한다.

## 2026-08-01 - plan-review 반환 다이어트 — finding이 아닌 확인 결과 비열거 (v4.6.27 → v4.6.28, post-implementation sync)

### Context

`plan-review` 게이트의 벽시계는 리포트 작성량이 결정한다 — 실측에서 게이트 시간의 **54~68%**가 반환 작성이었다. 그 작성량의 상당 부분은 판정에 기여하지 않는 **확인 결과의 열거**였다: 실재가 확인된 Target Files·content anchor 목록, 대조했으나 반증되지 않은(지지된) 사실 전제 목록이 반환 하단에 통째로 실린다. 판정 결과는 이미 `Findings`와 `Smell 판정`(PASS 접기 포함)이 전부 담으므로 이 목록은 중복이다. 이 습성은 특정 렌즈나 dispatch 형태에 매인 것이 아니라 실측 계열 dispatch 전반에서 관측됐다.

### Decision

1. **반환은 `Step 6`에 명시된 항목이 전부다**: `plan-review-agent` 미러 2벌의 `Step 6: Return`에 비열거 규칙 1문장을 추가한다 — 확인했으나 finding이 아닌 대조 결과는 열거하지 않는다. 기존 4개 반환 항목(`Blocker Status`·`Findings`·`규모 판정 검사 결과`·`Smell 판정`)은 축소하지 않는다.
2. **무조건 규칙이다**: 호출자 렌즈 한정 여부와 무관하게 모든 dispatch에 적용된다. 같은 파일의 `호출자 렌즈 한정` 절이 일부 자체 검증 항목을 렌즈별로 조건화하고 있어, 무조건성을 명시하지 않으면 실측 렌즈 dispatch가 이 규칙도 조건부로 오독한다.
3. **줄이는 것은 출력이지 검증이 아니다**: `Step 3` 대조 범위(읽기 범위 계단)는 불변이다. 검출력은 그대로 두고 출력량만 줄인다.
4. **자체 검증은 새 항목을 만들지 않는다**: 규칙 준수를 기존 `AC5`(산출물 형태)에 흡수한다("Step 6 항목 밖에 …"). 새 AC·Hard Rule·섹션은 추가하지 않았고, 렌즈 구조(실측 ∥ 판단 2-렌즈)·6-smell rubric·severity·`plan-review` SKILL 미러 4벌은 무변경이다.

### Rationale / Evidence

- **되돌린 대안 (핵심 음성 결과)**: 같은 목적을 **실측 렌즈 묶음 분할**(검증 ∥ 전제, 3-dispatch)로 치려다 끝까지 구현한 뒤 **커밋 전 전량 되돌렸다**. (a) 벽시계 353s로 재고 밴드, (b) shard 합 738s — **총량 보존이 4회 재현 끝에 처음 붕괴**, (c) 검출 품질 개선 근거 없음(잡힌 High 2가 전부 구 실측 렌즈도 소유하던 종류), (d) 계약 표면만 증가(비대칭 반환·PASS 접기 보정 2개 불변식 신설 → 그 자리에서 구멍 3개 발생: 상위 조항 소실, `PASS` 접기 줄 미차단, 반증 smell의 status 공백). 결론: **부풀림의 원인은 분할이 아니라 반환 습성이다** — 전제 묶음뿐 아니라 검증 묶음 반환에도 확인 목록이 실렸다. 나눠서 양을 분배하는 것보다 **덜 쓰게 하는 편**이 계약 표면을 늘리지 않고 같은 목표를 친다. 커밋 전 되돌림이라 이력 흔적은 0이며 supersede 기록은 두지 않는다.
- **게이트 실측**: 이 draft의 `plan-review` 게이트는 다이어트 **미적용** 상태로 돌아 2-렌즈 대조 표본 4가 됐다 — 실측 131s ∥ 판단 93s, 벽시계 131s. 구현 게이트는 correctness 221s ∥ simplicity 126s ∥ 79s, 벽시계 221s, Critical·High 0 / Medium 1 fix(AC5 범위 한정어 유실 → "Step 6 항목 밖에" 추가). structural check RED 4 FAIL → GREEN 9 PASS, 변이 7종 전량 검출.
- **효과는 아직 미관측**: 다이어트 효과의 첫 관측은 플러그인 발효 후 **다음 feature의 `plan-review` 게이트**다. 판정은 실측 렌즈 시간과 반환에 확인 목록이 실렸는지를 함께 본다.
- **선고정 방법 교훈**: 직전 회차에서 sync 선고정 버전을 세션 기억으로 정해 stale(4.6.24)했고 두 묶음이 각자 잡아 수렴했다. 이번에는 `main.md` 헤더 grep 1회로 실측 확정했다.

### Changes

- `.claude/agents/plan-review-agent.md` -- `Step 6: Return`에 비열거 규칙 1문장, 자체 검증 `AC5`에 준수 흡수
- `.codex/agents/plan-review-agent.toml` -- 같은 두 지점의 codex 미러 반영
- `_sdd/spec/main.md` -- v4.6.27 → v4.6.28

### Follow-up

- 같은 열거 습성이 다른 reviewer agent(`implementation-review-agent`·`simplicity-review-agent`·`pr-review-agent`)에도 있는지, 이 규칙을 전파할지는 **효과 관측 후 별건**으로 판단한다. 이번 범위에서는 확인하지 않았다.

## 2026-07-31 - Codex investigate separates diagnose-only from explicitly authorized product fix (v4.6.26 → v4.6.27, post-implementation sync)

### Context

Codex `investigate`가 `investigate`·`debug`·`diagnose` 같은 모호한 요청을 관례적 수정 요청으로 넓히면, 사용자가 승인하지 않은 제품·소스 변경과 회귀 테스트 추가까지 수행할 수 있었다. 진단 보고서나 분석 산출물 작성 요청도 제품 fix 권한으로 오인하지 않도록 intent 경계를 명시적으로 분리했다.

### Decision

1. **모호한 조사 요청의 기본값은 diagnose-only다**: 조사 대상 제품·소스의 fix·repair·patch·수정을 명시적으로 요청하거나 사용자가 후속 승인한 경우에만 fix mode로 진입한다. 진단 보고서·분석 산출물 작성 요청은 제품 fix 권한이 아니다.
2. **diagnose-only는 제품 변경 단계를 건너뛴다**: 근본원인과 영향 범위, evidence, 권고를 반환하되 Fix & Verify를 수행하지 않고 제품·소스·spec fix와 회귀 테스트 추가를 금지한다.
3. **mandatory governance write만 유일한 쓰기 예외다**: 상위 저장소 규칙이 강제한 기록만 정확한 대상·연산 의미로 수행할 수 있다. append 요구는 기존 내용을 보존해야 하며, 실제 governance write는 최종 보고에 공개한다.
4. **fix mode의 기존 안전 계약은 유지한다**: blast-radius gate 뒤에만 수정하고 fresh verification을 수행한다. runtime adapter, 조건부 fan-out, 3-Strike, scope lock도 유지한다.
5. **이번 결정은 Codex-only다**: `.codex/skills/investigate/SKILL.md`만 적용 대상이며 Claude mirror는 의도적으로 변경하지 않았다. cross-platform parity를 주장하지 않는다.

### Rationale / Evidence

- implementation review가 intent ambiguity **High 1**, 실패하는 marker oracle **Critical 1**, governance oracle gap **High 1**, report compression **Medium 1**을 발견했고 모두 fix 1회에 반영됐다.
- runtime smoke가 fixture work-log replacement를 추가로 드러내 append-only governance exception을 강화했다.
- fresh isolated Codex CLI 0.146.0 smoke가 exit 0으로 완료됐다. product manifest와 다른 work-log는 불변이고, current work-log는 기존 byte prefix를 보존한 append-only 변경이었다. exact mode/fix marker와 governance report 검증도 모두 status 0이었다.

### Changes

- `.codex/skills/investigate/SKILL.md` — intent classification, mode별 금지/허용 경계, 조건부 Fix & Verify, governance write 보고 계약 정렬
- 입력: `_sdd/drafts/_processed_2026-07-31_feature_draft_codex_investigate_intent_boundary.md`

## 2026-07-31 - Codex subagent model overrides follow active spawn schema enums (v4.6.25 → v4.6.26, post-implementation sync)

### Context

Codex review subagent의 model·effort override를 저장소의 고정 allowlist로 검증하면 runtime schema가 바뀔 때 유효한 값을 거부하거나 stale 값을 계약처럼 남길 수 있다. 세 review skill의 override 검증 기준을 선택된 active `spawn_agent` schema로 정렬했다.

### Decision

1. **active spawn schema enum이 단일 검증 근거다**: `plan-review`, `implementation-review`, `pr-review`는 `--model`과 `--effort`를 각각 선택된 active `spawn_agent` schema의 model·reasoning-effort enum으로 검증한다.
2. **미지원·누락 요청은 dispatch 전에 차단한다**: 요청 field가 없거나 값이 enum 밖이면 dispatch하지 않고 schema가 노출한 허용값을 보고한다.
3. **override 적용 계약은 유지한다**: 유효한 override는 모든 reviewer에 균일하게 적용하고, 생략한 값은 기본값을 상속하며, model과 effort는 별도 옵션으로 유지한다.
4. **현재 값은 예시이지 persistent contract가 아니다**: `gpt-5.6-sol`·`gpt-5.6-terra`와 effort `low`·`max`·`ultra`는 관측 예시이며 미래 실행에서는 active schema enum이 우선한다.

### Rationale / Evidence

- Desktop에서 model·effort 경계 조합이 모두 완료됐다.
- Codex CLI 0.146 smoke가 exit 0, `CLI_OVERRIDE_SMOKE_DONE`, model·effort marker 모두를 확인했다.
- static stale live values **0**, dynamic contract **3/3**, mutation **3/3**, hygiene 검증이 통과했다.

### Changes

- Codex review skill 3종의 model·effort 검증을 active schema enum 기반으로 전환
- 현재 모델·effort 값은 usage example로만 유지
- 입력: `_sdd/drafts/_processed_2026-07-31_feature_draft_codex_dynamic_model_override.md`

## 2026-07-31 - Codex multi-agent dispatch adopts schema-selected mailbox/target-close contracts (v4.6.24 → v4.6.25, post-implementation sync)

### Context

Codex의 활성 multi-agent lifecycle schema가 Desktop과 CLI 환경에서 서로 다를 수 있는데도 surface 이름이나 legacy 호출 형태에 기대면, 지원되지 않는 field·target wait·close를 섞어 dispatch가 실패할 수 있었다. 이번 변경은 `.codex`의 mandatory orchestrator, optional helper, lifecycle 문서 표면을 활성 tool schema 기반 adapter 계약으로 정렬했다.

### Decision

1. **surface 이름이 아니라 활성 tool schema가 lifecycle을 선택한다**: Desktop과 현재 CLI 0.146.0이 노출하는 mailbox schema는 invocation별로 고유한 parent-tree `task_name`, `fork_turns: "none"`, target 없는 wait를 사용하고 완료 agent를 별도 close하지 않는다.
2. **legacy target/close 경로는 완결된 schema에서만 유지한다**: target형 wait와 `close_agent`가 둘 다 노출된 경우에만 기존 target wait → close lifecycle을 사용한다. 두 schema의 field나 lifecycle을 한 실행에 섞지 않는다.
3. **불완전하거나 모호한 schema는 fail closed한다**: mandatory dispatch는 blocker로 종료하고 optional helper는 inline 경로로 fallback한다. 노출되지 않은 lifecycle tool을 검색해 복구하지 않는다.
4. **model/effort override는 spawn schema capability다**: 요청된 model 또는 effort field를 활성 spawn schema가 지원하지 않으면 조용히 생략하지 않고 dispatch를 차단한다.

### Rationale / Evidence

- Desktop에서 2-reviewer `plan-review`가 mailbox lifecycle로 완료됐다.
- Codex CLI 0.146.0 mailbox `plan-review`가 exit 0과 `CLI_PLAN_REVIEW_DONE`으로 완료됐다.
- static census **12/12**, stale pattern **0**, agent TOML **5/5**, local link/reference 검증 clean, mutation **4/4**를 확인했다.

### Changes

- `.codex` mandatory review/spec-sync orchestrator와 optional helper lifecycle을 schema-selected adapter 계약으로 정렬
- `.codex/agents/README.md`, `sdd-autopilot`, PR review example의 dual-runtime 설명 정합화
- 입력: `_sdd/drafts/_processed_2026-07-31_feature_draft_codex_dual_runtime_adapter.md`

## 2026-07-31 - spec-sync 표면 묶음 분할(본문 ∥ 기록) — 첫 작성자 분할 (v4.6.23 → v4.6.24, post-implementation sync)

### Context

리뷰 3종 병렬화(v4.6.21~v4.6.23) 후 체인의 최장 단독 구간은 spec-sync였다(실측 245~445s, 시간의 ~50%가 집필). 집필 대상 파일이 성격상 둘로 나뉘고 쓰기 집합이 서로소라는 점을 근거로 분할 축을 **표면 묶음**으로 잡았다. 변경 4파일 — `.claude/agents/spec-sync-agent.md` + `.codex/agents/spec-sync-agent.toml`(3-way) + `.claude/skills/spec-sync/SKILL.md` + `.codex/skills/spec-sync/SKILL.md`(3-way).

### Decision

1. **표면 묶음 2 분할 (agent — 호출자 표면 한정 절)**: implemented sync를 **본문 묶음**(live truth 갱신 + delta의 evidence 검증·승격) ∥ **기록 묶음**(`decision_log.md`·`changelog.md` append-only 신규 entry + input `_processed_` rename)으로 병렬 dispatch한다. 이는 read-only reviewer가 아닌 **첫 작성자 분할**이며, 병렬 안전 근거는 reviewer들의 "파일을 안 쓴다"와 다른 새 근거인 **쓰기 집합 서로소**다(본문은 기록 파일을 쓰지 않고 기록은 live truth 파일을 쓰지 않는다).
2. **read-vs-rename 경합 흡수**: 기록 묶음의 `_processed_` rename이 본문 묶음의 input 읽기보다 먼저 닿을 수 있어, 본문 묶음은 input 파일을 원 이름과 `_processed_` 이름 양쪽으로 조회한다.
3. **공유 사실은 orchestrator 선고정**: 신규 spec 버전·delta 목록·결정 제목은 orchestrator가 digest에 고정해 넘기고 두 shard가 각자 도출하지 않는다.
4. **사후 정합 검사 (orchestrator, 비gating)**: grep 2종 — ① `main.md` 헤더 버전 == changelog 최신 entry 버전, ② git diff에서 두 기록 파일 삭제 줄 0(append-only). 불일치는 relay에 명시, fix는 호출자 소관.
5. **기록 묶음은 digest 선고정 값 기반 — 코드 재검증 없음**: 재검증 중복 제거가 분할 이득의 절반이라 의도된 trade-off다. digest가 틀리면 기록이 틀리는 리스크는 사후 정합 검사와 append-only 규율로 완화하고, 내용 오류는 후속 spec-review가 그물이다.
6. **무조건 문구 전수 조건화 + 후방 호환**: agent AC·Hard Rule 11·Step 7·Output Format의 무조건 문구를 소유 조건화했고, 한정 없는 호출은 전체 수행이다. planned 경로(구현 전 호출)는 분할하지 않고 현행 1회 유지 — 후방 호환 경로는 pr-review가 아니라 planned 경로·직접 호출이다.

### Rationale / Evidence

- structural check RED 선관찰 → GREEN **21 PASS / 0 FAIL**, 변이 9종 전량 검출.
- 게이트(N+2) 실측: correctness shard 185/87/181s + simplicity 참조 145s ∥ 국소 134s — 벽시계 **185s**.
- 게이트 finding **High 1 + Medium 4, 전량 fix**. High = rename 블록 무조건형 잔존 — census 단일 패턴이 '마킹한다' 변형을 놓친 위장 PASS.
- plan-review 2-렌즈 관측 표본 2 = max 178s, 지지 밴드.

### Follow-up

- 본 feature의 벽시계 효과 실측은 이 체인의 spec-sync 파일럿(발효 전 수동 2-shard dispatch — 지금 이 sync)이 첫 관측이다 — 결과 수치는 다음 sync에서 기록한다.

## 2026-07-31 - simplicity reviewer 차원 묶음 분할 dispatch (참조 ∥ 국소, N+2) (v4.6.22 → v4.6.23, post-implementation sync)

### Context

correctness task-shard(v4.6.21)와 plan-review 2-렌즈(v4.6.22)로 게이트의 다른 구간이 내려간 뒤, simplicity(실측 107~252s, 시간의 56~96%가 리포트 — 세션 transcript 계측, `_sdd/work_log/2026-07-31.md`)가 implementation-review 게이트의 임계 경로 후보가 됐다. v4.6.21은 "simplicity는 task로 자르지 않는다 — 중복 탐지는 두 지점을 같이 봐야 한다"로 task 축 분할을 배제했는데, 이번 분할 축은 task가 아니라 **차원**이다. 변경 4파일 — `simplicity-review-agent` 미러 2벌(codex 3-way) + `implementation-review` SKILL 미러 2벌.

### Decision

1. **차원 묶음 분할 (agent — 호출자 차원 한정 절)**: 호출자가 차원 묶음을 한정하면 그 묶음만 스캔하고 반환의 차원 판정도 소유 차원만 낸다. **참조 묶음** = 중복 코드 + 죽은 코드 + 단일 사용처 추상화(사용처/복제 추적형 — Grep 무거움), **국소 묶음** = 도달 불가 에러 처리 + 과잉압축(코드 자리 판독형). 두 묶음의 합집합 = 정확히 5개 차원(누락·중복 배정 없음).
2. **한정은 차원이지 범위가 아니다 (task 축 반대 논거와 공존, supersede 아님)**: 어느 묶음이든 리뷰 범위는 전체 변경이다 — 중복 렌즈를 소유한 shard가 여전히 모든 지점을 동시에 관찰하므로 v4.6.21의 반대 논거를 위반하지 않는다.
3. **무조건 "5개" 문면 전수 일반화**: 자체 검증 AC1·Hard Rule 3·Review Dimensions 도입부·Step 2의 무조건 "5개" 문구를 "소유한 차원"으로 조건화했다(소유하지 않은 차원 finding 금지 취지는 유지). Integration의 pr-review 서술은 "차원 한정 없는 호출 — 전체 5차원 후방 호환 경로"로 갱신 — `pr-review`는 이 경로로 무변경 동작한다.
4. **orchestrator 계약 (implementation-review SKILL)**: simplicity를 묶음마다 1회, 총 2회 dispatch한다(참조 ∥ 국소, 각각 전체 변경 대상) — correctness shard들과 합쳐 **한 메시지 N+2 병렬**. relay의 차원 판정은 두 반환의 합집합(각 차원 정확히 한 묶음 소유 — 중복 없음), 합산 severity "모든 반환" 문면은 N+2를 그대로 포섭. codex는 3-way — spawn 예시에 묶음 슬롯 반영, wait 예시의 simplicity id 복수화. 게이트 fix로 근거 문장·payload bullet의 SKILL 재기재를 제거했다(단일 소스 = agent `호출자 차원 한정` 절/Runtime Adapter 블록).
5. **stale 표면 정리 (이 sync)**: `main.md` §2 implementation-review 불릿·2-렌즈 결정 행의 "simplicity는 (항상/양쪽 모두) 통짜 1회"를 차원 묶음 2회 + pr-review 전체 5차원 1회(후방 호환) 구분 서술로 교체, relay 문면 (N+1)→(N+2)·차원 합집합 추가. `components.md` implementation-review 행·Claude skill/agent split 행 동일 갱신.

### Rationale / Evidence

- structural check RED → GREEN 18 → 게이트 fix 후 **20 PASS / 0 FAIL**, 변이 8종 전량 검출.
- **게이트 = N+2 완전체 첫 런 (첫 실측)**: correctness shard 103/85/110s + simplicity 참조 164s ∥ 국소 91s — 게이트 벽시계 **164s**. simplicity 합 255s ≈ 동급 통짜 실측 252s(총량 보존 3번째 재현). finding: 참조 Medium 2(근거 문장 4벌 복제·codex payload bullet 이중 기재) → 단일 소스화 fix, 국소·correctness shard 2·3 finding 0.
- **묶음 불균형 실측(정직)**: finding이 중복 차원에 집중돼 참조 shard가 시간·리포트 우세 — 이득이 리포트 반분 가정보다 작다. 재배분은 실측 누적 후 별건.

### Follow-up

- 묶음 재배분(참조 shard 우세 해소)은 실측 누적 후 별건 후보로 남긴다.
- plan-review 2-렌즈 벽시계 효과의 첫 관측이 이 draft의 plan-review 게이트에서 나왔다 — 실측 렌즈 320s ∥ 판단 렌즈 86s, max 320s로 재고 밴드(~300s+) 해당(n=1, repo 대조 밀도 높은 draft). 판정은 확정하지 않고 사용자 보고 후 결정 대기로 main.md 🚧 Planned 항목에 기록했다.

## 2026-07-31 - plan-review 2-렌즈 분할 dispatch (실측 ∥ 판단) + 실행 경제 guardrail의 fan-out 배제 supersede (v4.6.21 → v4.6.22, post-implementation sync)

### Context

`plan-review`는 체인에서 유일하게 병렬 파트너가 없는 단독 리뷰 단계였다(5회차 실측 257~347s, 평균 ~294s; 시간 분해 = 최종 리포트 54~68% + 중반 추론 + 도구 15~25%). correctness task-shard 파일럿(v4.6.21)이 "finding이 나뉘면 리포트 생성이 나뉘어 벽시계가 준다"는 메커니즘을 검증했으나, plan-review의 finding은 섹션 교차·repo 대조형이라 task 축이 성립하지 않는다(실측 finding 9건 중 task 내부로 닫힌 것 0건). 변경 4파일 — `plan-review-agent` 미러 2벌 + `plan-review` SKILL 미러 2벌(codex는 3-way 적응).

### Decision

1. **렌즈 축 분할 (agent — 호출자 렌즈 한정 절)**: 호출자가 렌즈를 한정하면 그 소유분만 수행한다. 실측 렌즈 = Step 3 도구 계단 + `Verification Weakness` smell + draft 사실 주장의 repo 대조(판단 렌즈 소유 smell의 사실 전제 — 기존 파일의 수정 수용 가능성, 기존 로직/중복의 실재 여부 — 포함). 판단 렌즈 = 나머지 5 smell + 규모 판정 검사 + Step 4 — Step 3 계단을 밟지 않고 draft 내부 근거로만 판정하며 사실 전제에 UNKNOWN을 내지 않는다(repo 반증은 실측 렌즈 반환). agent 자체 검증의 규모 판정(AC2)·Step 4(AC3) 항목은 소유 렌즈(판단)에만 적용된다(게이트 fix로 명시). 렌즈 미지정 시 전체 6 smell 후방 호환.
2. **SKILL orchestrator화**: thin wrapper(1 dispatch) → 한 메시지 2회 병렬 dispatch + 병합 relay — Blocker Status는 하나라도 BLOCKED면 BLOCKED, findings 합산, smell 판정 합집합(각 smell 정확히 한 렌즈 소유), 규모 판정 = 판단 렌즈 반환. codex는 Runtime Adapter 블록이 호출·수거·payload 스펙의 단일 소스다(게이트 fix로 실행 절 재기재 제거). 단일 패스 불변(렌즈 2개 = 한 패스의 병렬 분해). 새 agent 없음(동일 agent 2회 — 등록 census 리스크 회피).
3. **guardrail supersede**: `main.md` §2 "해소 수단은 fan-out이 아니라 턴 접기다" 문면이 fan-out 계열 결정(v4.6.21 1+N, 본 건)과 모순돼 "턴 접기(배칭)와 read-only reviewer fan-out"으로 정정했다. 여전히 비대상: 중첩 fan-out — nesting 1단계 제한과 배칭 지시는 유지되고, 병렬 분해는 메인 루프 orchestrator의 1단계 read-only leaf dispatch에 한정된다.
4. **stale 표면 정리 (이 sync)**: `components.md` plan-review 행 "wrapper -> agent" → orchestrator + 2-렌즈 서술, Claude skill/agent split 행의 잔존 wrapper-backed 목록은 `spec-sync`만으로 축소·orchestrator 목록에 plan-review 추가. `main.md` 실행 분리·품질 게이트 소유권 결정 행 갱신, 단일 패스 항에 병렬 분해 단서, 입력 상한 "도구 계단"에 실측 렌즈 소유 단서, 2-렌즈 결정 행에 1+N 첫 정식 런 evidence(벽시계 122s). `usage-guide.md` Scenario 2 게이트 문장에 2-렌즈 병합 명시.

### Rationale / Evidence

- structural check RED 11 FAIL → GREEN 18 → 게이트 fix 후 **21 PASS / 0 FAIL**, 변이 9종 전량 검출. 게이트(implementation-review 1+N 첫 정식 런): correctness shard 122s ∥ 81s ∥ 101s + simplicity 107s — 벽시계 **122s**(shard 합 304s, 파일럿 143s 재현+개선). finding fix 2건: correctness Medium(자체 검증 AC2/AC3 무조건 문구 ↔ 렌즈 절 내부 모순) + simplicity Medium(codex payload 스펙 이중 기재) 반영, shard 2·3 finding 0.
- 벽시계 효과(기대 ~294s → ~200s, 약 30%)는 **미관측** — 플러그인 발효 후 다음 draft의 plan-review 게이트가 첫 관측 지점이다(main.md 🚧 Planned로 고정, 판정 밴드 max(렌즈 shard) ≤ ~220s 지지 / ~300s+ 재고).

### Follow-up

- plan-review 게이트의 simplicity 차원 분할은 별건 feature 후보로 남긴다(이번 범위 밖).
- 렌즈 불균형 리스크: 역대 finding이 `Verification Weakness`에 몰리는 경향이라 이득이 30%보다 작을 수 있다 — 렌즈 재배분은 효과 실측 후 별건.

## 2026-07-31 - implementation-review correctness task-shard 분할 dispatch (1+N) (v4.6.20 → v4.6.21, post-implementation sync)

### Context

`implementation-review` 게이트의 벽시계는 correctness reviewer 단독이 결정한다(5회차 실측 214~430s; simplicity 177~252s는 병렬 그늘 안). correctness의 시간 분해(transcript 실측)는 검증 루프(AC 단위 tool 턴) 65~80% + 최종 리포트 19~35%로 둘 다 task 경계로 나뉜다. 직전 레버였던 배칭 발화 시점 feature는 폐기됐고(병목은 I/O가 아니라 분석의 직렬성), 남은 레버가 correctness의 task 단위 분할이었다. 변경 4파일 — orchestrator SKILL 미러 2벌(`.claude/`·`.codex/skills/implementation-review/SKILL.md`, codex는 3-way 적응) + `docs/AUTOPILOT_GUIDE.md` ko/en 각 1줄. reviewer agent 본문 무변경.

### Decision

1. **correctness task-shard 분할 dispatch (1+N)**: 기준 draft의 Part 2 task가 2개 이상이면 correctness를 task별 shard로 분할 dispatch한다. shard k의 digest = 공통 digest + Task k의 AC·Target Files 범위 한정(해당 task의 AC만 검증). 전부 한 메시지에서 병렬 dispatch. task 1개이거나 draft 없이 대화 digest 기반이면 현행 비분할(1+1) 유지. 분할 축이 task인 근거는 기존 불변식 재사용이다 — feature-draft 규칙이 "task는 자기 AC만으로 완료 판정이 닫히는 실행 단위"를 보증하고 plan-review가 그 경계를 감시한다.
2. **simplicity는 분할하지 않는다**: (1) 병렬 그늘 안이라 벽시계 이득 0, (2) 중복 탐지 렌즈는 두 지점을 같이 봐야 해서 task 분할이 렌즈 본질을 자른다. **분할 상한도 두지 않는다** — draft 분할 규칙이 task 수를 소수로 유지하고 simplicity가 자연 바닥이라 상한 문면은 사변적이다(YAGNI).
3. **relay 계약**: correctness AC ledger는 shard 반환의 연접이다(task별 AC 집합이 서로소라 누락 없이 합쳐진다). 합산 severity 요약은 N+1개 반환 전부를 합산한다. task들이 같은 파일을 만져 shard 간 중복 finding이 나와도 orchestrator는 dedup하지 않고 전부 relay한다 — dedup은 fix 주체(호출자)가 자연 흡수한다.
4. **reviewer agent 본문 무변경**: shard 범위는 digest의 "호출자 지정" 경로로 기존 계약(기준 문서 적응)에 이미 들어온다. review-only 경계·병렬 안전성 근거(read-only leaf — shard 수와 무관하게 동시 dispatch 안전)·Model override(모든 reviewer 호출로 일반화, 동작 불변)는 보존. codex는 게이트 fix로 spawn/wait/close 호출 문법을 Codex Runtime Adapter 블록 단일 소스로 정리했다(실행 절의 이중 기재가 따옴표 drift를 실증해 제거).
5. **stale spec 표면 정리 (이 sync)**: `main.md` §2의 "직교 2-렌즈 review의 현재 적용 지점은 PR review" 문장을 두 곳(PR review + implementation 마감 게이트)으로 정정하고 implementation-review의 1+N 계약을 형제 불릿으로 추가. 실행 분리·2-렌즈 결정 행에 implementation-review를 orchestrator로 반영(2-렌즈 결정 행의 "(implementation gate 적용분은 F2에서 제거)" 잔존 서술 제거). `components.md` implementation-review 행을 "wrapper -> agent"에서 orchestrator + 1+N 서술로 교체하고, Claude skill/agent split 행의 wrapper-backed 목록에서 implementation-review를 orchestrator 목록으로 이동. `docs/AUTOPILOT_GUIDE.md` ko/en의 "2-reviewer" 리터럴은 feature가 직접 갱신했다("correctness shard N ∥ simplicity").

### Rationale

- **파일럿 실측이 비례 분배를 지지한다**: 게이트 = 파일럿(사용자 합의)으로 메인 루프가 수동 1+N dispatch — correctness shard A(T1+T3) 70s ∥ shard B(T2+T4) 143s ∥ simplicity 120s, 게이트 벽시계 **143s**, shard 합 213s ≈ 동급 단독 correctness 214s. 일의 총량이 보존되면서 벽시계만 줄었다(지지 밴드 ~220s 통과, 고정비 지배 아님 → 머지 재고 조건 미발동).
- 검증 evidence: structural check RED 17 FAIL → GREEN 17 PASS → fix 후 **18 PASS / 0 FAIL**(델타 check 1 포함), 변이 7종 전량 검출(고정 표기 재도입·연접 제거·고정 2-id 복원·docs 원복·분할 조건 약화·docs 초과 수정·call 문법 재기재), repo-wide 고정 표기 census(git 추적 파일) 정당 잔존 목록 밖 0건, 게이트 finding: shard A/B 0 + simplicity Medium 1(codex call 문법 이중 기재) → fix 1, correctness Low 1(따옴표 불일치)은 fix에 흡수, 전 AC MET.

### Follow-up

- `plan-review`의 2-렌즈 분할(기대값 ~30%)은 별건 후보로 남긴다 — 이번 범위 밖.
- shard 분할의 누적 효과(다양한 task 수·규모에서의 비례 분배 유지 여부)는 이후 게이트 회차에서 자연 관측된다.

## 2026-07-31 - 커버리지 델타 절 후속 정정 4건 — 순서 명제의 소유자는 집행 주체, 삭제 경로도 재검증 대상 (v4.6.19 → v4.6.20, post-implementation sync)

> 이 entry는 `2026-07-30 - implementation 커버리지 델타`(v4.6.17) entry의 **후속 정정**이다. 그 entry는 append-only 원칙에 따라 수정하지 않으며, 아래 결정 2가 그 Decision 1에 적힌 `(c)` 기준선을 폐기한다.

### Context

머지된 커버리지 델타 절(v4.6.17)을 사후 감사한 결과 정합 갭 4건이 나왔다(직전 entry Follow-up의 "별건"). 규칙의 방향은 유지하고 문면만 고쳤다. 변경 2파일 — `.claude`·`.codex` `skills/implementation/SKILL.md` 미러 2벌. 검증 evidence: structural check RED 11 FAIL → GREEN **19 PASS / 0 FAIL**, 변이 누적 10건 전량 검출 후 복구·재실행 통과, `git diff --check` clean, 미러 `diff` exit 0, `implementation-review` 게이트 1회(correctness Medium 2 + simplicity Medium 2 → fix 4, Blocker 0).

### Decision

1. **순서 명제의 소유자는 서술 표면이 아니라 집행 주체다**: §4 말미의 순서 절(`적용은 fix 직후이고, 마감의 회귀 재실행은 델타 처리까지 끝낸 뒤 1회 돈다`)을 마감 §3으로 **이동**했다(추가가 아니라 이동 — 서술 지점은 계속 1곳). §4는 **적용 대상**(fix diff에도 적용된다 + 근거)만 소유한다. 순서를 서술만 하는 절에 두면 마감을 순차 집행하는 메인 루프에 §4로 되돌아갈 트리거가 없고, 포인터를 덧붙이는 초안대로 갔으면 같은 순서 명제가 §4·마감 §3·spec 세 곳에 남았다(plan gate 지적으로 draft 단계에서 이동으로 전환).
2. **`(c)` 기준선 `(c) 근거가 덮지 못하는 동작`을 폐기한다**: v4.6.17이 도입한 이 표현은 정의되지 않은 척도였다 — §1의 `(c) 근거`는 **분류 근거 1줄**이지 커버리지 척도가 아니다. 실제 산출은 일반 규칙과 같은 곳(도달 테스트 0개 → diff 동작 전량)으로 합류하므로, 그 절이 실제로 막는 오해("테스트가 없으니 이 단계는 N/A")만 남기고 척도를 버렸다 — `§1에서 (c)로 분류한 task도 이 단계를 건너뛰지 않는다 — 도달하는 테스트/check가 0개이므로 diff의 동작 전량이 열거 대상이다`. 오해 부정만 남기면 (c) 실행자가 열거 기준을 문면에서 잃으므로 기준까지 담았다.
3. **삭제 경로에도 재검증을 건다 ((a)/(b) 한정)**: `삭제했으면 (a)/(b) task는 §3에서 통과시킨 그 task의 테스트/check를 다시 실행해 통과를 재확인하고 출력을 갱신 캡처한다 — 증거 테이블에 싣는 GREEN 증거는 삭제 이후 출력이다. 재확인이 실패하면 그 항목은 불필요분이 아니므로 삭제를 되돌리고 남기기 경로로 닫는다.` 기존 구조는 GREEN 증거가 삭제 **이전** 출력이라 삭제로 GREEN이 깨져도 증거 테이블이 통과 상태로 남았고, 안전망인 마감 회귀는 "전체 suite가 있으면"이라 조건부여서 이 repo가 다수 다루는 (b) structural-check task를 덮지 못한다. 테스트 **추가** 경로만 변이 확인으로 판별력을 강제하던 비대칭을 닫는다. **(a)/(b) 한정이 핵심** — (c)에는 실행할 테스트가 없어 무범위로 두면 공허한 의무가 되고, 결정 2가 고치는 "미정의 적용 범위" 결함을 새 조항에 다시 심는 셈이다.
4. **§4 첫 문단을 형제 절과 동형화한다**: 6개 의무를 한 산문 블록에 압축하던 것을 주 지시문(diff 실행, 동사형)은 불릿 밖에 두고 부속 규칙 4개를 각각 한 줄 불릿으로 분리했다(§2 RED·§3 GREEN과 동형). **문장 삭제 없이 배치만** 바꿨고 앵커 6개 보존을 AC로 강제했다. 4건 중 유일한 순수 형태 개선이며 효과는 미측정이다.
5. **회귀 의무는 fix 전체에 걸고 델타 적용만 선행 단계로 분리한다 (구현 중 결함 정정)**: 구현 중 마감 §3에서 회귀 재실행 의무가 `fix로 구현이 바뀌었으면` 조건 안에 갇혀 **문서·테스트만 고친 fix가 회귀를 건너뛰는** 협소화가 생겼다. 이 조건 이동은 리터럴 앵커 존재만 보는 AC로는 잡히지 않았고 §4 커버리지 델타가 잡았다(그 절의 두 번째 실사용). 게이트에서 다시 지적된 것은 그 정정 문장이 `재실행하고 … 그 전에`라는 **역참조**여서 순차 집행자가 회귀를 먼저 돌 여지(회귀 1회 규약상 옛 상태를 측정)가 있었다는 점이다 → **선형 한 문장**으로 재배치했다: `fix가 있었으면 그 fix diff에 §4 커버리지 델타를 먼저 적용한 뒤 회귀를 1회 재실행하고, 증거가 바뀐 AC는 위 증거 테이블을 갱신한다.` 동시에 적용 명제가 §4와 마감에 복제돼 있던 것도 마감 쪽을 줄여 해소했다.
6. **착지 표면**: `main.md` — 헤더 4.6.20, §2 커버리지 델타 하위 항목(삭제 재검증 + 소유권 분할 + (c) 기준선 폐기)과 마감 순서 항(델타 선행 단계 + 회귀 범위 + 순서 단일 소유자 명시). `components.md` — `implementation` 행의 폐기된 `(c)` 기준선 교체 + 삭제 재검증 + 마감 계약 열거의 델타 선행. `decision_log.md`·`logs/changelog.md`의 구 표현은 append-only 이력이라 수정하지 않고 이 신규 entry로 갈음한다. `usage-guide.md` 무변경. 배칭 관련 `🚧 Planned` 항목은 이 단위와 무관해 무변경이다.

### Rationale

- 같은 명제를 여러 표면에 두면 복제가 아니라 **소유권 분할**로 푼다. 판정 주체가 하나여야 한다는 이 repo의 기존 규칙(읽기 상한 = agent Step 3, 완전성 불변식 = AC 절 한 곳)과 같은 계열이고, 이번엔 축이 "판정"이 아니라 "집행"이었다.
- 규칙을 새로 쓸 때 반복되는 실패 모드는 **정의되지 않은 척도를 슬쩍 도입하는 것**이다(결정 2). 척도를 버리고 그 절이 막으려던 오해만 남기면 문면이 짧아지면서 판정 가능해진다.
- 대칭성 점검이 결함을 찾는다: 추가 경로에 검증이 있고 삭제 경로에 없으면 그 비대칭 자체가 결함 신호다(결정 3).
- 조건절의 위치는 의무의 범위다(결정 5). 앵커 리터럴 존재만 보는 AC는 조건 이동을 못 보므로, 문면 변경 task의 AC는 "무엇이 있는가"뿐 아니라 "무엇에 걸리는가"를 물어야 한다.

### Follow-up

- 델타 행의 `AC` 열 표기 관례는 여전히 미정이다(첫 실사용에서 굳히는 기존 계획 유지).
- 새 structural check의 앵커는 기존 본문 grep으로 **유일성부터** 확인한다 — 이번 RED 단계에서 위장 통과 성분 2건(`다시 실행해 통과를 재확인`이 변이 확인 문장에, `(a)/(b)`가 기존 Triage 문장에 이미 존재)이 나왔다.
- check은 문면(`한 문단 = 한 줄`)이 아니라 의도를 검사하도록 쓴다 — 게이트 fix 중 이 전제가 깨져 계약 오류 선언 1회 후 RED를 재관찰했다.

## 2026-07-31 - 배칭 규칙 첫 처치군 관측(음성) + 도입 근거 정정 — 호출 수는 배칭 여지의 대리지표가 아니다 (v4.6.18 → v4.6.19, 계측 sync / 코드 변경 0)

> 이 entry는 바로 아래 `2026-07-31 - agent tool call 배칭` entry의 **후속 정정**이다. 그 entry는 append-only 원칙에 따라 수정하지 않으며, 아래 결정 2가 그 Context/Decision 1에 적힌 근거 일부를 실측으로 정정한다.

### Context

`f1c2fbd` 머지로 플러그인이 갱신돼 배칭 Hard Rule이 설치본에 5/5 존재하는 상태(= 규칙 발효)에서 첫 처치군 데이터를 얻었다. 관측 대상은 배칭과 무관한 과제(커버리지 델타 PR#32 사후 감사)의 게이트 2종이고, 호출자 digest에 배칭을 언급하지 않았다 — 직전 entry가 명문화한 계측 전제조건을 처음으로 충족한 회차다. 지표는 **연속 실행 길이**(user `tool_result`가 끼지 않고 이어지는 assistant `tool_use` 줄 수)이며, 양성 대조로 재검증했다(`plan-review` 회차의 "연속 2"는 같은 assistant 메시지에서 `Glob` 2개가 나가고 두 결과가 함께 돌아온 진짜 배칭이지 아티팩트가 아니다). 코드·agent·skill 변경은 0이다.

| 회차 | 규칙 | 턴 | tool_use | 최대 연속 실행 |
|---|---|---|---|---|
| 7/30 correctness | OFF | 31 | 17 | 1 |
| 7/30 simplicity | OFF | 7 | 3 | 1 |
| 7/31 correctness | OFF | 28 | 17 | 1 |
| 7/31 simplicity | OFF | 21 | 13 | 1 |
| 7/31 plan-review | OFF | 23 | 12 | **2** |
| 7/31 correctness | **ON** | 35 | 21 | **1** |
| 7/31 simplicity | **ON** | 8 | 4 | **1** |

### Decision

1. **행동 효과는 계속 `🚧 Planned`로 둔다 — 첫 처치군 관측은 음성이다**: 규칙 ON에서도 최대 연속 실행이 1로 OFF 회차와 같다. draft AC가 못박은 비대칭(양성=정합 관측 / 음성=반증)대로 음성은 n=1에서도 반증력이 있으므로, 규칙이 **문면으로만 남았을 가능성이 크다**는 사실을 spec에 반영하되 미검증 표식은 유지한다. 절감 수치는 여전히 어디에도 기록하지 않는다.
2. **도입 근거 정정 (실측 반증, 이 단위의 핵심)**: correctness agent의 `Bash` 호출은 규칙 OFF·ON 양쪽 모두 **100% 복합 명령**(`&&`·`;`·`|`)이었다(12/12, 16/16). 첫 호출부터 `git status --short && git log --oneline -3 && git diff --stat` 형태다. 즉 **agent는 이미 셸 체이닝으로 압축하고 있었고**, multi-tool 배칭의 실제 여지는 셸로 엮을 수 없는 `Read` 5회뿐 — 28~35턴 중 4턴 남짓이다. 직전 entry Context의 "앞 9개는 서로 의존하지 않는데 한 개씩 냈다"와 "17콜 → 5~6라운드"라는 벽시계 추정은 **호출 수만 세고 호출 안의 내용을 보지 않은 판단**이었다. 일반화하면 *tool 호출 수는 배칭 여지의 대리지표가 아니다*이고, 이 교훈은 계측 방법론이라 §3 현재 운영 제약의 transcript 지표 항목에 붙였다(직전 entry의 지표 교정과 같은 슬롯).
3. **A/B는 불가로 확정, 비교 설계는 누적 관측이다 (사용자 결정)**: 활성 플러그인 설치본이 시점당 하나뿐이라 처치군·대조군 동시 실행이 원리적으로 불가능하고, 대조군 자체에 회차 간 변동이 있다(`plan-review`는 규칙 없이 2). 따라서 n=1 arm 비교는 무의미하며 도입 전후 **누적 관측**만이 가능한 설계다. 이 제약은 이 feature 전용이 아니라 agent 행동 변경 일반에 걸리므로 §3 plugin 캐시 지연 항목에 함께 붙였다.
4. **되돌리지도, 강화하지도 않는다**: 지금 되돌리면 n=1 음성으로 결론내는 셈이고, 지금 문면을 강화하면 효과 미확인 상태에서 규칙만 키우는 셈이다. 배칭과 무관한 과제 **2~3건**을 더 쌓아 연속 1이 고정인지 확인한 뒤 판정한다.
5. **문면 강화 후보는 착수하지 않는다 (Follow-up 수준 기록만)**: 현 규칙 문면은 "서로 의존하지 않는 read-only 호출"이라는 **추상 원칙**이라 매 호출마다 독립성 판정을 요구한다. 여지가 `Read`에 몰려 있다는 결정 2를 감안하면 "읽기 범위 계단 ①의 파일 `Read`는 한 메시지에 모은다"처럼 **상황을 지목하는** 형태가 후보다. 효과 확인 전에 착수하면 미검증 규칙 위에 규칙을 쌓는 것이므로 planned todo로 올리지 않는다.
6. **착지 표면**: `main.md` §3 현재 운영 제약 3개 항목만 수정했다 — plugin 캐시 지연 항목에 A/B 불가·누적 관측 설계, transcript 지표 항목에 호출 내용 계수 규칙과 정정 사실, `🚧 Planned` 항목에 첫 처치군 음성 관측과 누적 판정 설계. §2 Guardrails의 배칭 하위 항목은 **무변경**이다(규칙 문면과 4요소는 그대로 발효 중이고 정정 대상은 그 규칙이 아니라 도입 시 추정한 여지의 크기다). `components.md`·`usage-guide.md` 무변경.

### Rationale

- 음성 결과를 침묵으로 처리하면 spec은 "규칙을 넣었다"만 남고 "넣었는데 안 바뀌었다"는 더 값진 사실을 잃는다. 미검증 표식을 유지하는 것과 관측 결과를 기록하는 것은 배타적이지 않다.
- 계측에서 반복되는 실패 모드는 **대리지표를 실체로 착각하는 것**이다. 이 repo는 같은 feature에서 두 번 밟았다 — 첫 번째는 "메시지당 tool_use 수"(항상 1이라 배칭을 못 봄), 두 번째는 "호출 수"(내용이 이미 접혀 있어 여지를 과대 추정). 지표는 쓰기 전에 반드시 반대 방향으로 한 번 의심한다.
- 여지의 크기를 먼저 재지 않고 규칙부터 넣으면, 효과가 없을 때 "규칙이 안 먹혔다"와 "먹힐 여지가 애초에 작았다"가 구별되지 않는다. 이번 정정은 두 번째 가능성을 처음으로 무대에 올린다.

### Follow-up

- 누적 관측: 배칭과 무관한 과제 2~3건 추가 계측 후 판정(연속 1 고정 여부). 판정 전까지 규칙 문면 변경·롤백 모두 보류.
- 미채택 후보(위 결정 5): 상황 지목형 문면(`읽기 범위 계단 ①의 파일 Read를 한 메시지에`) — 효과 확인 후 재검토.
- 직전 entry의 Follow-up 2건(codex 미러 5파일 검증 경로 0 / `plan-review` 1↔2단 배칭 여지 · 쓰기 없는 2종의 요소 (iii) 도달 불가)은 여전히 미해소다.
- 별건 — 커버리지 델타 feature(v4.6.17) 사후 감사에서 correctness Medium 2(마감 §3 → §4 델타 역참조 포인터 부재 / "삭제 1순위" 경로에 삭제 후 재검증 의무 부재)와 simplicity Medium 2(§4 첫 문단이 6개 의무를 산문에 압축 / `(c) task` 예외절이 미정의 척도 도입)가 나왔다. 이번 계측 단위에서는 미처리이며 해당 feature 후속으로 다룬다.

## 2026-07-31 - agent tool call 배칭 — 병목은 dispatch 왕복이 아니라 턴 수만큼 반복되는 추론 (v4.6.17 → v4.6.18, post-implementation sync)

### Context

사용자 질문("리뷰가 느린데 subagent라서 그런가")에서 출발했다. 2026-07-30 게이트 1회의 subagent transcript를 계수한 결과 `implementation-review-agent` 430s / 17콜 / 31턴, `simplicity-review-agent` 177s / 3콜 / 7턴이었고 **배칭은 0회**, 완전 직렬이었다. correctness 17콜 중 앞 9개는 호출자 digest만 보고 대상이 정해지는 것들로 서로 의존하지 않았다 — 읽기 범위 계단 ①이 "전문 Read 보장"으로 선언해둔 파일들을 한 개씩 꺼내 읽고 있었다. 10파일 전량 grep에서 배칭 문면은 0건이었다(런타임은 지원하는데 지시가 없었다). 이미 소진된 레버는 모델·effort 강등(재제안 금지), lite reviewer 신설(propagation 부담으로 환전), 출력 다이어트(전체의 1% 미만으로 측정 종료), 입력 상한 추가(읽기 범위 계단이 이미 `Read`를 5회로 억제)다. 변경 12파일 — agent 5종 × claude md/codex toml 10파일 + `implementation` SKILL 미러 2벌. 검증 evidence: structural check RED 23 FAIL → GREEN **73 PASS / 0 FAIL**, 변이 누적 12건 전량 검출 후 복구·재실행 통과(허가형 어미·계단 제약 복제·기존 규칙 삭제·codex만 요소 제거·TOML 파괴·계단 제약 위치·codex 문구 claude 누출·1파일 오타·L3 허가형 되돌림·불변식 삭제·미러 비대칭·불릿 절 이동), codex TOML `tomllib` 5/5, agent 10파일 삭제 라인 0, `git diff --check` clean, `implementation-review` 게이트 1회(correctness High 1 + Medium 1, simplicity Medium 1 → fix 3).

### Decision

1. **해소 수단은 fan-out이 아니라 턴 접기다 (current truth 승격)**: 이 계열의 지연은 subagent dispatch 왕복도 입력 읽기량도 아니라 **턴 수만큼 반복되는 추론**이다. nesting 1단계 제한은 원인이 아니며, 설령 허용돼도 파일 몇 개 읽자고 자식을 띄우면 컨텍스트 적재가 배칭보다 비싸다. 착지 지점은 §2 Guardrails의 기존 nesting 불릿 **하위 항목 1개**다 — 새 guardrail 불릿도 새 결정 테이블 행도 만들지 않았다(같은 판정 주체 아래 둔다). 이 배치는 "nesting 제한 때문에 느리다"는 오인이 바로 그 불릿을 읽는 사람에게서 나오기 때문이기도 하다.
2. **배칭 지시는 지시형이어야 한다**: repo의 기존 배칭 문장이 전부 허가형("배칭해 병렬로 실행해도 된다")이었고, 허가형으로 렌더링되면 문면 검사는 통과하는데 행동은 바뀌지 않는다. 필수 4요소는 (i) 서로 의존하지 않는 read-only 호출은 한 메시지에서 함께 낸다(지시형), (ii) 앞 결과에 의존하는 호출만 다음 턴, (iii) 쓰기·상태 변경 호출은 배칭하지 않는다, (iv) 배칭은 읽을 대상을 늘리지 않는다이며, agent 10파일에 동일 문면(claude 5는 바이트 동일, codex 5는 예시 1문장 추가)으로 전파했다. 번호는 파일마다 다르다(9/9/9/11/14) — "모든 agent가 Hard Rule 8을 공유한다"는 draft 전제가 plan gate에서 실측으로 뒤집힌 결과다.
3. **요소 (iv)는 장식이 아니라 상한 보호 조항이다**: 배칭 지시는 "이왕 하는 김에 미리 다 읽어두자"로 번지기 쉽고, 그렇게 되면 읽기량을 줄이려고 세운 도구 계단·읽기 범위 계단(v4.6.15·v4.6.16)을 이 feature가 잠식한다. 배칭은 "무엇을 읽는가"가 아니라 "몇 턴에 나눠 읽는가"만 바꾼다.
4. **계단 제약의 소유자는 Hard Rule이 아니라 계단 자신이다**: `plan-review`의 도구 계단은 조기 종료가 본질이라 다음 단을 미리 당겨 호출하면 계단이 무력화된다. 그래서 "배칭은 같은 단 안에서만 한다" 1문장을 `plan-review-agent` 짝의 Step 3 계단 절(계단 4항목 **뒤**)에만 두고 Hard Rule에는 복제하지 않았다 — 복제하면 계단 판정 주체가 두 곳으로 갈린다. `implementation-review`의 읽기 **범위** 계단은 순서가 아니라 범위를 규정해 배칭과 직교하므로 예외 조항이 필요 없다. 계단 상세와 마찬가지로 이 제약도 단일 agent 계약이라 `components.md` `plan-review` 행 note에 두었다(`Repo-wide Invariant Test` #2 미통과).
5. **주문장은 tool 이름에 의존하지 않는다**: 주문장을 `multi_tool_use.parallel`에 걸면 런타임이 그 이름을 노출하지 않을 때 규칙이 "없는 도구를 부르라"는 실패하는 호출 지시가 된다. codex 미러에서만 `codex 런타임이 ...을 제공하면 그것으로 표현한다`는 **조건형** 예시로 덧붙였다(게이트 correctness M1 fix — 최초 구현은 지시형이었다).
6. **재량과 항상-이득을 한 문장에 섞지 않는다 (draft 범위 밖 확장, 사용자 지시)**: `implementation` SKILL `## 입력`의 "서로 독립인 task들은 tool call을 배칭해 병렬로 실행해도 된다"가 판단이 필요한 재량(task 병렬)과 항상 이득인 규칙(tool call 배칭)을 한 문장에 묶고 있었다. 둘로 쪼개 배칭만 지시형으로 올리고 task 병렬은 허가형으로 남겼으며(강제하면 안 되는 판단), `각 task 안에서는 RED→GREEN 순서를 지킨다` 불변식은 후자에 그대로 보존했다. 이 구분 자체가 재사용 가능한 판단이라 §2 하위 항목에 함께 올렸다.
7. **행동 효과는 승격하지 않는다 — Task 3은 `UNTESTED`로 닫았다**: 문면 존재는 동작을 증명하지 않는다. 도입 회차의 계측은 아래 #8 때문에 무효였고, 규칙이 로드되지 않은 실행은 규칙의 반증이 아니므로 미충족이 아니라 `UNTESTED`다. spec에는 `🚧 Planned`로 남기고 절감 수치는 어디에도 적지 않는다.
8. **plugin 캐시 지연 (이번 세션 최대 수확, 운영 제약 승격)**: dispatch되는 agent/skill은 작업트리가 아니라 **plugin 설치본**(`~/.claude/plugins/cache/sdd-skills/sdd-skills/<pushed SHA>/`)에서 로드된다. 실측 — 현 설치본 `fc8f1c9`에 이번 배칭 규칙은 **0/5**인 반면 전날 머지된 커버리지 델타는 1건 존재했다. 즉 오늘 편집한 본문은 커밋·푸시·플러그인 갱신 전까지 발효되지 않고, 마감 게이트는 구 본문으로 돌았다. 따라서 **같은 세션의 마감 게이트로 자기 규칙의 효과를 계측하는 설계는 구조적으로 무효**다. 이 사실은 계측을 넘어 "방금 고친 agent를 dispatch해도 구 본문이 돈다"는 일반 제약이라 §3 현재 운영 제약으로 올렸다.
9. **transcript 계측 지표를 교정했다 (내 오류, 실측으로 반증)**: 최초 계수 규칙("메시지당 tool_use 수")은 무효였다 — transcript JSONL은 한 메시지의 content 블록을 **줄 단위로 쪼개** 기록하므로(같은 assistant 메시지의 `text`와 `tool_use`가 별도 줄) 이 값은 항상 1이 되어 배칭을 원리적으로 탐지하지 못한다(15개 transcript 전량 max=1이 그 증거다). 유효 지표는 **연속 실행 길이**이고 양성 대조(`plan-review` 회차 최대 연속 2)로 검증했다. 지표를 바꿔도 원래 전제("배칭 0")는 살아남았다.
10. **자기 행동 보고는 transcript로 교차검증한다**: 게이트에서 correctness가 "이번 세션에 한 메시지에 2·2·4·2·2개를 냈다(최대 4)"고 보고했으나 자기 transcript 실측은 최대 1이었고, 그 위에 세운 "규칙 없이도 배칭이 나온다"는 논거를 기각했다. agent의 자기보고는 논거의 근거가 되기 전에 계수로 확인해야 한다.
11. **기각·배제**: (a) 모델·effort 티어 강등 — 사용자 실측 무효과, **재제안 금지**. (b) lite reviewer 신설 — v4.6.15에서 기각 완료. (c) 출력 다이어트 추가 — 전체의 1% 미만으로 측정 종료. (d) 입력 상한 추가 — 읽기 범위 계단이 이미 억제 중이고 배칭과 직교. (e) 계측용 별도 재dispatch — 마감이 어차피 돌리는 게이트를 관측 대상으로 삼아 중복 실행 7분을 제거했다(결과적으로 #8로 무효화됐지만 비용은 0이었다). (f) `sdd-autopilot`·wrapper 스킬 본문 — 배칭 주체는 agent 자신이다. (g) 도구 계단·읽기 범위 계단의 내용 변경.

### Rationale

- 지연 레버를 고를 때는 "무엇이 반복되는가"를 먼저 계수해야 한다. 이 repo는 dispatch 왕복과 읽기량을 차례로 의심했고 둘 다 계측으로 탈락했다 — 남은 것이 턴 수였고, 그 순간 해법이 fan-out(더 많은 dispatch)의 반대 방향으로 뒤집힌다.
- 문면 규칙의 실패 모드는 "없음"이 아니라 **허가형으로 존재함**이다. 존재 검사만 하는 AC는 이 실패 모드를 통과시키므로 어미까지 판정 조건에 넣어야 한다(plan gate M1이 잡은 것이 정확히 이것이다).
- 실행 경제 규칙을 추가할 때는 그 규칙이 기존 상한을 잠식하지 않는지 역검해야 한다. v4.6.16에서 상한 신설이 읽기 의무를 늘릴 뻔했던 것과 같은 계열의 위험이 반대 방향(배칭 → 선행 읽기 팽창)으로 재현된다.
- 자기 변경을 자기 세션에서 계측하려는 설계는 편의상 매력적이지만, 로딩 경로가 작업트리가 아니면 관측 대상이 애초에 존재하지 않는다. 계측 설계는 "무엇을 재는가" 전에 "재려는 것이 그 실행에 로드되는가"를 확인해야 한다.
- 지표는 도구가 아니라 가설의 일부다. 양성 대조 없이 얻은 "전량 0"은 부재의 증거가 아니라 지표 무능의 증거일 수 있다.

### Follow-up

- `pr-review`·`spec-sync`는 문면 전파만 있고 행동 실측 경로가 없으며, **codex 미러 5파일은 이번 feature에서 검증 경로가 0이다** — 다음 codex 실행 시 사후 확인 대상.
- 잔존 advisory 2건: `plan-review` 1↔2단은 서로 독립이라 Hard Rule만 보면 묶일 여지가 있다(대체안이 계단 소유권·미러 바이트 동일성을 깨서 인지만 한다) / 쓰기 없는 reviewer 2종에서는 요소 (iii)이 도달 불가 조항이다(10파일 동일 문면 계약상 유지).

## 2026-07-30 - `implementation` 커버리지 델타 — 테스트 집합을 AC의 함수에서 diff의 함수로 (v4.6.16 → v4.6.17, post-implementation sync)

### Context

사용자 문제 제기가 출발점이다 — "RED→GREEN으로 구현을 채우고 나면 빠진 테스트가 종종 보인다". 진단 결과 체인 전체가 AC에 앵커되어 **테스트 집합이 AC의 함수**였다. RED는 AC가 요구하는 동작의 미충족만 관찰하고, GREEN에서 코드가 AC보다 넓어진 부분(요구되지 않은 분기·경계값·에러 경로·기존 호출부 적응)은 어떤 테스트도 고정하지 않는다. 마감 증거 테이블은 AC 단위라 그 확장분이 등장조차 하지 않고, `implementation-review-agent`는 AC verdict ledger + 읽기 범위 계단(AC 밖 탐색적 읽기 금지)이라 구조적 사각지대였다. 변경 2파일(`.claude/skills/implementation/SKILL.md`·`.codex/skills/implementation/SKILL.md`, identical 미러) — `### 4. 커버리지 델타` 신설 + 기존 `테스트 불변 규칙` 번호만 4→5 이동, `## 마감` 절 무변경. 검증 evidence: structural check C0~C4 RED(C1 FAIL 헤딩 4개) → GREEN 전량 PASS, 변이 4건 전량 검출 후 복구·재실행 통과 재확인, `git diff --check` clean, 미러 `diff` exit 0, `implementation-review` 게이트 1회(correctness Blocker 0 / Must 5 → fix 5, simplicity Medium 2 → fix 2).

### Decision

1. **커버리지 델타 단계를 GREEN 직후에 둔다**: 각 task의 GREEN 통과 직후 그 task가 변경한 diff를 **실제로 실행해 읽고**, 방금 통과시킨 테스트/check가 도달하지 않는 동작을 열거한다. 근거는 diff 출력이지 기억이나 AC 재독이 아니다 — 이 스킬에서 RED가 작동하는 이유가 "실제 실행해 관찰한다"는 행위 의무 + 아티팩트 형태였으므로 델타도 명사형 근거 규정이 아니라 동사형 행위 지시로 둔다. 기준점은 task 시작 시점이고 커밋 경계가 없으면 이번 task가 만진 hunk로 한정한다(다중·병렬 task에서 앞 task hunk 혼입 방지). (c) test-free task는 비교할 테스트가 공집합이라 델타 = diff 전량으로 퇴화하므로, (c) 근거가 덮지 못하는 동작을 기준선으로 삼는다.
2. **삭제가 1순위다**: §3 GREEN이 금지한 "요청되지 않은 옵션·설정·추상화·에러 처리"는 이 단계가 지목하는 전형적 델타와 **같은 목록**인데, triage는 테스트 가능성만 판정하고 "그 코드가 존재해야 하는가"를 묻지 않는다. 그대로 두면 GREEN 최소성 위반 코드가 테스트까지 달고 고착된다. 그래서 AC도 요구하지 않고 기존 동작 유지에도 불필요한 항목은 삭제를 먼저 검토하고, 남기기로 한 항목만 기존 triage 기준으로 닫는다(기준을 재정의하지 않는다).
3. **델타 테스트의 판별력은 변이 확인으로 증명한다**: 코드가 이미 존재해 RED 관찰이 불가하므로, 대상 동작을 일시적으로 깨서 실패를 관찰하고 되돌린 뒤 재실행해 통과를 재확인한다. 이 절차가 없으면 델타 테스트는 코드를 보고 짜맞춘 무조건 통과 테스트로 퇴화한다. 나아가 테스트 불변 규칙의 트리거가 "RED 관찰 후"라 델타 테스트는 문면상 보호 밖이었고(가장 약화되기 쉬운 부류가 정작 무보호), 구제 절차 2단계도 "RED를 다시 관찰"이라 **실행 불가**였다. 두 구멍 모두 델타 절이 닫는다 — 동일 적용 + "RED 재관찰은 변이 확인 재수행으로 대체". 대체 규칙의 소유자는 델타 절이고 불변 규칙 본문은 무변경이다(판정 주체를 둘로 갈지 않는다).
4. **마감 게이트 fix diff에도 적용한다 (draft AC 범위 밖 확장)**: Task 2의 회고 실효 관찰이 근거다 — 직전 feature 커밋 `134854f`(AC 유래 check 47건)에 절차를 돌려 델타 2건(`git diff --name-only` 공집합 시 fallback, "참조된 spec은 필요한 절로 한정")을 열거했고 check 커버는 0건이었는데, **둘 다 `implementation-review` fix로 들어온 동작**이었다. fix 산출물은 AC가 확정된 뒤 태어나 AC 유래 테스트가 구조적으로 없는 부류다. 적용은 fix 직후이고 마감의 회귀 재실행은 델타 처리까지 끝낸 뒤 1회 돈다(델타 산출물은 게이트 fix가 아니라 자기 재트리거가 불가하므로 무한 후퇴는 없다). 이 조항은 draft Contracts 5요소 밖의 6번째이며, `## 마감` 절이 아니라 델타 절 안에 둔 이유는 델타 규칙의 소유자가 그 절이기 때문이다.
5. **"델타 없음" 통과 문구를 두지 않는다**: 델타가 없으면 아무것도 적지 않는다 — 형식적 통과 문구로 전락할 표면 자체를 만들지 않는 의도적 선택이다(출력 다이어트 방향과도 일치). 대가는 이 단계의 **스킵과 0건이 사후 구분되지 않는다**는 것이다(RED의 실패 출력 캡처, 계약 오류의 선언 아티팩트와 달리 수행 흔적이 없고 `implementation-review`도 AC ledger 기반이라 수행 여부를 못 본다). 강제력은 diff 실행 행위 의무와 델타 발견 시 증거 테이블 노출에만 의존하며, 이 한계를 accepted trade-off로 명시 수용한다.
6. **착지 표면 — 순서를 열거하는 spec 표면 전량 갱신**: `main.md` §2 test-first 불릿의 순서 열거에 커버리지 델타를 넣고 하위 항목 1개를 추가했으며, 테스트 불변 규칙 하위 항목에 델타 적용·RED 재관찰 대체를 덧붙였다. §3 결정 표 `implementation test-first` 행, `components.md`의 `implementation` 컴포넌트 행과 Strategic Code Map `Implementation contract` 행도 같은 이유로 갱신했다(전부 단계를 전수 열거하는 서술이라 절이 늘면 stale해진다). `usage-guide.md`의 `RED→GREEN`은 축약 표기라 델타 추가 후에도 여전히 참이므로 무변경이다.

### Rationale

- **왜 GREEN 직후인가**: (B) 마감으로 미루면 전체 GREEN 통과 후라 코드를 보고 짜맞춘 테스트가 되어 RED 관찰의 가치가 소멸한다. (C) `implementation-review`에 얹으면 AC 밖 탐색을 금지한 읽기 범위 계단 원칙과 정면 충돌하고(v4.6.16 결정) fix 1회 타이밍이라 늦다. 델타는 코드를 방금 쓴 주체가 구현 시점에 닫는 것이 가장 싸다.
- **왜 리뷰 렌즈를 넓히지 않았나**: 상한을 세운 직후에 같은 agent의 범위를 다시 열면 v4.6.16 결정이 무효화된다. 사각지대의 해소 지점을 리뷰가 아니라 구현 단계로 고정하는 편이 두 결정 모두를 보존한다.
- **기각**: 중단·분할 규칙에 "델타가 반복적으로 크다 = 계획 문제" 신호 추가(YAGNI — 아직 관측되지 않은 실패 모드이고 기존 규칙 2(계약 오류 반복)로 계획 문제를 이미 잡는다), `## 마감` 절 편집(증거 테이블 스키마 무변경이라 델타 행 수용은 신설 절 1문장으로 충분 — 편집 표면 최소화), `implementation-review`/reviewer agent 변경, 새 agent·파일·artifact.
- **재발 함정 기록**: 첫 check 실행이 macOS bash 3.2의 `mapfile` 부재로 죽었는데 `set -uo pipefail`만으로는 fail 플래그가 서지 않아 **ALL PASS + exit 0**을 보고했다(portable read loop로 교체). check 하네스 자체의 첫 실행 결과는 항상 의심 대상이라는 사실이 이 repo에서 다시 재현됐다.

### Changes

- `.claude/skills/implementation/SKILL.md`·`.codex/skills/implementation/SKILL.md` -- `### 4. 커버리지 델타` 신설, 기존 `테스트 불변 규칙` 4→5 번호 이동(본문 무변경), `## 마감` 무변경
- `_sdd/spec/main.md` -- 헤더 4.6.17, §2 test-first 불릿 순서 열거 + 하위 항목 1개 추가, 테스트 불변 규칙 하위 항목에 델타 적용·RED 재관찰 대체 추가, §3 결정 표 `implementation test-first` 행 갱신
- `_sdd/spec/components.md` -- `implementation` 컴포넌트 행에 커버리지 델타 note 추가, Strategic Code Map `Implementation contract` 행 열거 갱신
- `_sdd/spec/logs/changelog.md` -- v4.6.17 entry

## 2026-07-30 - `implementation-review` 읽기 범위 계단 — 입력 상한의 형태는 렌즈에 맞춘다 (v4.6.15 → v4.6.16, post-implementation sync)

### Context

직전 단위(같은 날 아래 entry)의 정직한 계측이 출발점이다 — 리뷰 1회 소비에서 최종 리포트는 2~3k 토큰(전체의 4% 안팎)이고 나머지는 파일 읽기 + 중간 추론이었다. 따라서 출력 다이어트의 절감은 1% 미만이고 일의 양을 실제로 깎는 레버는 입력 상한뿐이다. 그 상한을 `implementation-review-agent`로 확장했다. 변경 2파일(`.claude/agents/implementation-review-agent.md`, `.codex/agents/implementation-review-agent.toml`, payload 동일). 검증 evidence: structural check 47 PASS / 0 FAIL(RED 34건 관찰 후 GREEN), 변이 테스트 12건(단일 미러 6 + 양쪽 미러 동시 5 + 재확인)으로 각 check의 판별력 증명, `implementation-review` 게이트 1회(correctness Blocker 0 / Medium 4 → fix 4) + `simplicity-review`(Medium 5 → fix 3, 반려 2), fix 후 회귀 47 PASS + 변이 5건 전량 재검출, `git diff --check` 무출력, codex TOML `tomllib` 파싱 + `Codex Agent Boundary` delta 보존.

### Decision

1. **입력 상한의 형태는 렌즈에 따라 다르다 (재사용 가능한 결정)**: 직전 단위가 `plan-review-agent`에 세운 `Glob`→`Grep`→`Read`→`UNKNOWN` **도구 계단**을 `implementation-review-agent`에 이식하지 않는다. draft 문서를 보는 리뷰는 `Read`를 후순위로 밀어도 판별력이 유지되지만, correctness 렌즈는 경계·null·에러 경로·동시성 같은 로직 결함 탐지가 본업이라 **코드 본문 Read가 그 렌즈의 핵심 수단**이다(이 agent가 직전 단위에서 변이 테스트 12건으로 검증 스크립트의 위장 PASS 3건을 잡은 것이 실증이다). 그래서 도구 순서 대신 **무엇을 읽을지의 범위**를 제한하는 **읽기 범위 계단**을 세웠다 — ① 변경 집합 + 기준 문서는 전문 Read에 상한을 걸지 않고, ② 인접 표면은 `Grep` 우선, ③ 그 밖은 탐색적 읽기 금지다. 같은 목적(무제한 재량 → 상한)이 렌즈에 따라 다른 형태를 갖는다는 이 구분 자체가 다음 reviewer로 확장할 때 재사용되는 결정이다.
2. **착지 표면 — 형태 일반화는 `main.md`, 계단 상세는 `components.md`**: 직전 단위는 도구 계단을 `Repo-wide Invariant Test` #2(2개 이상 표면 공통) 미통과로 판정해 `components.md` `plan-review` 행에만 두었다. 계단 **상세**는 이번에도 agent 한 곳 계약이라 `components.md` `implementation-review` 행 note로 내렸다. 다만 "상한을 렌즈에 맞춘 형태로 세운다 + `pr-review`는 대상이 아니다"라는 **형태 판단**은 이번 두 번째 적용으로 reviewer 2종에 걸쳤고(#2 통과), 한두 파일 읽기로는 왜 형태가 다른지·왜 `pr-review`가 빠졌는지가 복구되지 않으며(#1), 틀리게 가정하면 다음 feature가 도구 계단을 그대로 복사하는 정확히 그 실수를 한다(#3). 그래서 §2 Guardrails의 기존 reviewer 불릿 **하위 항목 1개**로만 올렸다 — 새 guardrail 불릿도 새 결정 테이블 행도 만들지 않았다(reviewer 계약의 판정 주체를 둘로 갈지 않는다). 선례(`simplicity 렌즈는 spec-review로 확장하지 않는다`)와 같은 슬롯이다.
3. **초과 대응은 삭제가 아니라 이전이다**: Error Handling `대규모 코드베이스` 행("핵심 컴포넌트 중심으로 범위를 줄이고 가정을 적는다")을 `Step 3 읽기 범위 계단 ①의 초과 대응을 따른다`로 축약하면서, 그 행이 담고 있던 degradation 능력은 ①로 옮겼다(단일 패스 초과 시 AC 관련도·diff hunk 밀도 순 읽기 + 못 읽은 파일과 약해진 AC verdict를 limitation으로 명시). "무엇을 읽는가(범위)"와 "담기지 않을 때 무엇을 포기하는가(초과 대응)"는 다른 규칙이므로 포인터 축약이 능력 손실이 되지 않게 이전을 명시했다. 이 이전은 사용자가 배제한 검증 예산 제한이 아니다.
4. **③은 "읽지 않음"이 아니라 "탐색하지 않음"이다**: AC가 명시적으로 요구하는 증거(전수 census, 잔존 0건, 파일 목록 일치)는 범위 밖이라도 `Grep`/`Bash`로 확보한다. 이 예외가 없으면 이 repo가 반복해 앓은 census 잔존·미러 누락 표면이 그대로 `UNTESTED`로 새고, 상한이 검출력 손실로 환전된다.
5. **`UNTESTED`는 사유를 병기한다**: Hard Rule 5의 "테스트 실행 불가"와 ③의 "범위 밖"이 같은 토큰으로 뭉치면 미달의 원인이 구별되지 않는다. `UNTESTED(범위 밖)` 형태로 사유를 병기하되 반환 ledger 표 형식은 불변이다.
6. **`components.md` `implementation-review` 행 Primary Source 누락 보정**: `plan-review` 행은 claude/codex 짝 4개를 열거하는데 이 행은 claude 2개만 갖고 있었다. draft delta는 `.codex/agents/implementation-review-agent.toml`을 지목했고, 실측에서 `.codex/skills/implementation-review/SKILL.md`도 존재해 인용된 비대칭("codex 짝 2개")을 닫는 쪽으로 둘 다 추가했다. 같은 누락 패턴이 다른 행(`spec-sync` 등)에도 있으나 이번 단위 범위가 아니다.
7. **기각·배제**: (a) `pr-review`에 상한 추가 — 사용자 명시 판정("PR 리뷰는 충분히 시간을 들이는 게 좋다"), 인간 리뷰 보조라 벽시계보다 검출력이 우선이다. (b) `simplicity-review` 상한 — 요청 범위 밖. (c) **검증 예산(깊이) 제한** — 변이 테스트 횟수·반복 검증 상한은 판별력과의 직접 맞교환이라 별도 판단이 필요하다(이번에 잡힌 위장 PASS 4건이 깊이 판 대가였다). (d) model/effort 티어 변경 — 사용자 실측 무효과, **재제안 금지**. (e) `plan-review` 도구 계단 재작성 — 직전 단위에서 완료.
8. **게이트가 잡은 것은 자기 계약의 경계 결함이다**: correctness Medium 4 전량이 신설 문면의 실질 결함이었다 — (M1) ①의 기준 문서 열거가 "호출자 지정 draft/plan"에 앵커돼 `기준 문서 적응` mode 2·3에서 기준 문서가 ②로 떨어짐 → 모드 판정을 Step 1/`기준 문서 적응`에 위임하고 ①은 재열거하지 않는다, (M2 **목적 역행**) "참조한 spec 범위"에 한정 술어가 없어 1,700줄대 `decision_log.md`까지 무상한 ①에 들어가고, 변경 전 Step 3에는 spec 읽기 지시가 아예 없었으므로 이 조항이 상한이 아니라 **신규 읽기 의무**로 작동할 수 있었다 → `AC·정합 판정에 필요한 절로 한정`, (M3) `git diff --name-only` 단일 수단이라 커밋 후 호출 시 ①이 공집합이 되고 변경 파일이 ③에 걸림 → `<base>..HEAD`/`git log` fallback, (M4) check 4건의 위장 PASS → 보호 섹션 sha256 대조·문장 단위 앵커로 교체. simplicity Medium 2건은 근거를 대고 반려했다 — correctness 지시 3중 서술은 선재 중복이라 `Surgical Changes` 범위 밖이고, Error Handling 행 삭제는 그 표가 *상황→규칙* 라우팅 표면이라 `대규모 코드베이스` 상황이 표에서 사라진다.
9. **효과는 절감 수치가 아니라 "무제한 재량을 상한으로 대체"다 (정직한 기록)**: 동기가 된 실측(363s / 79k)에 ①/②/③별 읽기 비중 원자료가 없어 ②③ 억제의 절감 규모는 **미측정**이다. 리뷰어가 현재도 사실상 ①만 읽고 있다면 절감은 0에 가까울 수 있다. 벤치마크는 문서 자산에 과한 비용이라 이번 범위에 넣지 않았고, 다음 `implementation-review` 1회의 tool call 구성으로 사후 실측한다.

### Rationale

- 상한을 세울 때 옮겨야 하는 것은 계단의 **모양**이 아니라 "무제한 재량을 없앤다"는 **목적**이다. 모양을 복사하면 렌즈의 핵심 수단을 후순위로 밀어 상한이 곧 검출력 손실이 된다 — 도구 계단을 correctness 렌즈에 이식하는 것이 정확히 그 사고였다.
- 상한 신설은 팽창 여지도 함께 만든다. ①에 "기준 문서"를 넣는 순간, 한정 술어가 없으면 변경 전에 없던 읽기 의무가 생겨 읽기량을 줄이려는 feature가 읽기량을 늘린다(M2). 상한 문면은 항상 "변경 전 대비 무엇이 늘었는가"로 역검해야 한다.
- 포인터 축약은 규칙 소유자를 1곳으로 모으는 좋은 수단이지만, 축약 대상이 담고 있던 **능력**이 포인터 대상에 실제로 존재하는지 확인해야 한다. 범위 규칙과 초과 대응은 다른 규칙이라 후자를 명시 이전하지 않으면 축약이 삭제가 된다(plan-review H3).
- 상한의 예외(AC 요구 증거)는 선택적 완화가 아니라 상한이 성립하기 위한 조건이다. 예외가 없으면 이 repo의 지배적 실패 모드(census 잔존·미러 누락)가 상한 도입만으로 미검출로 전환된다.
- 효과를 수치로 주장하지 않고 "재량 → 상한"으로만 기록해 두면, 다음 레버(검증 예산)를 고를 때 잘못된 성공 신호에 근거하지 않는다.

### Follow-up

- (선재 smell, 이번 범위 아님) correctness 능동 검토 지시가 agent 헤더·AC1·Step 3 세 곳에 서술돼 있다. 판정 주체 1곳 규범에 어긋나므로 별건으로 정리한다.
- correctness Low 3 잔존: Step 6 `Assumptions` 정의가 "기준 문서 없이 리뷰한 경우"로 한정돼 범위 밖 가정의 귀속이 문면상 모순(반환 형식이 이번 Scope Out) / `UNTESTED` 사유 병기가 편면적이라 무표기 UNTESTED는 여전히 모호 / (이 entry로 해소) `components.md` spec surface.

## 2026-07-30 - reviewer 반환 출력 다이어트 + `plan-review` 읽기 입력 상한 (v4.6.14 → v4.6.15, post-implementation sync)

### Context

review 게이트의 체감 지연을 줄이려는 요구에서 출발했다. 사용자가 먼저 검토한 안은 "lite review agent 신설"이었으나 실측에서 agent 본문은 80~115줄로 이미 작았고, 지배 요인은 본문 길이도 subagent 호출 왕복도 아니라 **리포트 작성(추론)** 이었다. 그래서 계약·rubric·severity는 손대지 않고 (a) 정보를 더하지 않는 출력, (b) 무제한으로 열려 있던 입력만 걷어냈다. 변경 10파일 — agent 3종 각 claude md + codex toml(`plan-review-agent`·`implementation-review-agent`·`simplicity-review-agent`) + wrapper SKILL 4벌(`plan-review`·`pr-review` × claude/codex). 검증 evidence: 프레임워크 부재 자산이라 structural check으로 RED→GREEN(초기 28 FAIL → 최종 66 PASS / 0 FAIL), census 5종 전부 0건(`6행`·`5행`·`Progress Overview`·`필요한 범위만 읽는다`·`어느 쪽에도 없는`), 미러 3쌍의 변경 payload diff 동일 + codex TOML 3종 `tomllib` 파싱 성공 및 codex 적응 delta(`Codex Agent Boundary`·`spawn_agent`·gpt 모델 허용값) 보존, `git diff --check` 무출력, `implementation-review` 게이트 1회(correctness Blocker 0 / Medium 4 → fix 4) + `simplicity-review` Medium 2 → fix 2.

### Decision

1. **소비자 없는 반환 항목은 제거한다 (current truth 승격)**: `implementation-review-agent` 반환에서 `Progress Overview`(task/AC 단위 상태 요약)를 삭제해 반환 항목이 6 → 5개(`Status`·`Findings`·`Verification ledger`·`Recommendations`·`Assumptions`)가 됐다. 근거는 도출 가능성 + 소비 실측 둘이다 — 같은 반환의 `Verification ledger`가 AC별 verdict+증거를 보유해 task 상태는 그로부터 도출되고, `implementation-review` SKILL의 relay 목록(`AC verdict ledger, findings 요약, blocker`)에 이 섹션의 소비자가 없다. 착지 지점은 §2 Guardrails의 기존 reviewer 불릿 하위 항목이다 — reviewer 반환 계약의 판정 주체가 이미 그 불릿이라 새 guardrail도 새 결정 테이블 행도 만들지 않았다.
2. **2026-07-10 결정 #6의 `Progress Overview` 조항을 대체한다**: 그 결정은 같은 섹션을 "task/AC 상태로 **제약**"했다(중복 서술을 줄이되 섹션은 유지). 이번 단위는 제약이 아니라 **삭제**다 — 제약된 형태에서도 `Verification ledger`와 정보가 겹치고 relay 소비자가 없다는 사실이 그때 확인되지 않았기 때문이다. 같은 결정의 나머지 조항(finding ID 블록화·Recommendations ID 참조 갈음·Conclusion 삭제)은 유효하고 무변경이다.
3. **판정 표는 문제 있는 항목만 개별 행으로 내고 나머지는 접는다**: `plan-review-agent`의 6 smell과 `simplicity-review-agent`의 5 차원에서 `WARN`/`FAIL`/`UNKNOWN`(또는 finding 있는 차원)만 개별 행으로 내고 나머지는 `PASS: <이름 나열>` 한 줄로 접는다. 점검·스캔 의무는 유지하고 출력 의무만 완화한다 — 무정보 행(전부 PASS인 6행/5행)은 판정을 담지 않으면서 매 리뷰마다 생성 비용을 낸다.
4. **완전성 불변식의 소유자는 각 agent의 AC1 절 한 곳이다 (draft 계약 정정)**: 점검 대상 전량이 개별 행 또는 PASS 접기 한 줄 중 **정확히 하나**에 귀속돼야 한다는 명제는 AC1 positive 1회만 적는다. draft Task 2/4 AC1은 원래 이 불변식이 AC 절과 반환 형식 절 **양쪽** 문면에 있어야 한다고 가정했는데, 그 가정이 이 repo 규범(판정 주체 1곳)과 정면으로 어긋났다 — 반환 형식 절의 "나머지는"이 분할을 이미 완결하므로 뒤 문장은 함의이고, 부정형 대우("어느 쪽에도 없는 항목은 점검 누락이다")는 positive의 재천명이다. 출력 다이어트가 목적인 변경이 같은 명제를 3번 적는 자기모순이라 draft AC를 "반환 형식 절에는 재서술하지 않는다"로 뒤집고 check을 '부재가 PASS'로 반전해 RED(10건) → fix → GREEN을 다시 관찰했다.
5. **`plan-review-agent`의 읽기 재량을 도구 계단으로 대체한다**: "필요한 범위만 읽는다"는 상한이 아니라 재량이라 read 비용이 무제한으로 열려 있었다. `Glob`(경로 존재) → `Grep`(AC가 지목한 content anchor) → `Read`(Grep으로 판정이 닫히지 않는 파일 한정) → `UNKNOWN`(+limitation 1줄, 읽기 확장 금지) 계단 + "상위 단계로 판정이 닫히면 하위 단계로 내려가지 않는다" 정지 규칙으로 바꿨다. 규칙의 단일 소유자는 Step 3이고 Input 절 중복 서술은 삭제, Error Handling 행은 Step 3 포인터로 축약했다. 이 계약은 agent 한 곳에만 적용돼 `Repo-wide Invariant Test` #2(2개 이상 표면 공통)를 통과하지 못하므로 global spec 본문이 아니라 `components.md` `plan-review` 행의 reference note로 내렸다.
6. **`Read` 전면 금지는 기각한다**: 초안은 Target File 본문 Read를 금지했으나 `plan-review` 자신이 반례였다 — 이 draft의 AC들(잔여 반환 항목 5개, rubric 6행 유지, relay 목록 확인)은 본문을 읽어야 판정이 갈린다. 금지는 `Verification Weakness` smell(AC가 falsifiable한가·기존 구조와 충돌하는가)의 판별력을 없애고, 게다가 agent가 이미 보유한 `Grep`이 초안 어디에도 없어 금지만 있고 대체 수단이 비어 있었다. 상한은 금지가 아니라 **더 싼 수단을 먼저 쓰게 하는 계단**이어야 한다.
7. **`pr-review-agent`의 `Correctness 신호`는 유지한다**: 제거 후보였으나 `pr-review` orchestrator가 통합 리포트 `Signals` 줄(`AC MET X of N / test pass F%`)에서 실제 소비한다. `pr-review-agent` 본문은 이번 단위에서 무변경이며, 이 agent에는 판정행 표도 없다. "소비자 실측으로 판정한다"는 규칙이 삭제와 유지를 같은 기준으로 가른 사례다.
8. **lite review agent 신설은 기각한다**: 계약을 복제해 claude md ↔ codex toml 짝 propagation 부담으로 환전하는 셈이고, 이 repo가 반복해서 앓은 실패 모드다. 계약은 계속 agent 하나가 단일 소스로 보유한다.
9. **model/effort 티어 강등은 재제안하지 않는다**: 사용자가 이미 시도해 효과 없음을 확인했다.
10. **Medium finding 블록 강등은 기각한다**: `implementation-review`·`simplicity-review`의 Medium은 메인 루프 fix 1회의 입력이라 블록(위치·문제·수정)을 줄이면 fix 정확도가 떨어진다. reviewer 4종 모두 현행 Medium 블록을 유지한다.
11. **wrapper relay 문구는 지칭만 고친다**: `smell 6행 판정` → `smell 판정`, `차원 5행 판정` → `차원 판정`(`plan-review`·`pr-review` 각 claude/codex 4벌). `implementation-review` SKILL의 `simplicity: 5개 차원 판정`은 새 형식(개별 행 + PASS 접기로 5개 전량 귀속)과 의미가 일치해 미변경으로 판정했다. 이 리터럴들은 global spec 어느 표면에도 등장하지 않아 spec 반영 대상이 아니다.

### Rationale

- 체감 지연의 지배 요인이 작성(추론)이면 레버는 "무엇을 쓰게 하느냐"이고, 계약·rubric·severity를 건드리지 않고도 당길 수 있다. 반대로 agent를 쪼개거나 모델 티어를 낮추는 레버는 검출력이나 유지 비용을 지불한다.
- 삭제 판정 기준을 "중복처럼 보인다"가 아니라 **relay 소비 실측**으로 두면 같은 기준이 유지 판정(`Correctness 신호`)에도 대칭으로 적용돼, 다음 다이어트에서 소비자 있는 항목을 잘라내는 사고를 막는다.
- 완전성 불변식을 여러 곳에 적는 것은 검출력을 늘리지 않는다 — 판정 주체가 둘 이상이면 한쪽만 갱신되는 드리프트가 생기고, 출력 다이어트 변경이 스스로 사족을 낳는다. 이 repo에서 반복 확인된 규범(판정 주체 1곳)이라 draft AC보다 규범이 우선한다.
- 입력 상한을 금지가 아니라 계단으로 세운 덕에 rubric(6 smell)은 무변경으로 남는다. 금지는 rubric의 일부를 사실상 무력화하는 숨은 rubric 변경이었다.

## 2026-07-29 - 하네스 실행 자산에 재주입 방향 추가 (`harness-context.sh`, 훅 자산 2개 → 3개, v4.6.13 → v4.6.14, post-implementation sync)

### Context

직전 단위(v4.6.13)가 하네스를 실행 층으로 확장했지만 그 층은 "강제" 한 방향뿐이었다. compact·clear로 컨텍스트가 소실되면 `CLAUDE.md` 포인터("작업 전 `AGENTS.md`를 먼저 읽는다")만 재주입되고 하네스 본문은 사라지며, 포인터를 따라 읽을지는 모델 재량이라 실제로 누락된다 — work log 규약이 산문만으로 안 지켜져 커밋 게이트를 도입한 것과 같은 실패 모드이고 해소 수단도 같다. 변경 범위: `harness-context.sh` 정본 신설 + 4벌 미러, `spec-create` §3e·`spec-upgrade` Step 6의 훅 자산 계약을 work log 전용에서 훅 자산 일반으로 확장(claude·codex 2벌씩), 이 repo dogfooding(`.claude/hooks/` 사본 + `settings.json` SessionStart 그룹 추가), `docs/SDD_CONCEPT.md` ko·en §1 후행 갱신. 검증 evidence: 자체 structural check 29 PASS/0 FAIL + 변이 테스트 4건 전부 검출, **런타임 발동 관찰**(픽스처 repo 트랜스크립트에 `hook_success`/`hookName:"SessionStart:clear"`·`"SessionStart:compact"` 기록 + content에 픽스처 sentinel 포함 = 리드 줄만이 아니라 본문 전체 주입, 음성 대조로 `startup` 발동 0건, 리뷰어가 자기 sentinel로 clear leg 독립 재현), `implementation-review` 게이트 1회(correctness Blocker 0 / simplicity Medium 5 — 합산 Medium 7건 fix 1회 반영), 미러 실측(`references/hooks/` 세 스크립트 각 4벌 md5 1종, 두 SKILL.md claude↔codex 바이트 동일), `git diff --check` 무출력.

### Decision

1. **훅 자산 계약을 2개 → 3개로 넓히되 착지 지점은 기존 불릿 하나다 (current truth 승격)**: `harness-context.sh`(SessionStart, `matcher: "clear|compact"`)를 기존 두 스크립트와 같은 설치 계약(verbatim 복사 + `settings.json` 키 수준 멱등 병합 + 하네스 설치와 동일 조건, opt-in 아님) 아래 둔다. v4.6.13이 만든 §2 Guardrails 하네스 설치 불릿이 이미 이 계약의 판정 주체이므로 새 guardrail 행도 새 결정 테이블 행도 만들지 않고 그 불릿을 확장했다 — 새 행을 세우면 "하네스 설치가 무엇을 함께 설치하나"의 판정 주체가 둘로 갈린다.
2. **재주입은 "읽으라는 지시"가 아니라 내용 주입이다**: `harness-context.sh`는 `AGENTS.md` 전문을 stdout으로 내보내 컨텍스트에 직접 넣는다. 지시 방식(예: "AGENTS.md를 읽어라" 한 줄 주입)은 모델 재량이 남아 이번에 닫으려는 실패 모드를 그대로 재생산하고, 모델이 순순히 읽어도 Read 왕복으로 같은 분량이 들어오므로 비용 이점도 없다. 이 판단은 §3 핵심 설계의 harness 산문에 실었다 — 하네스 레이어의 canonical이 그 산문이고, "실행 자산이 무엇을 하는 층인가"의 정의에 해당한다.
3. **실행 자산의 성격을 두 방향으로 확정한다**: 실행 자산은 규약을 **강제**할 뿐 아니라 컨텍스트에서 사라진 규약을 **되돌려 놓는다**. v4.6.13의 §3 산문은 "강제"만 서술했고, 그 서술로는 재주입 자산이 같은 층에 속하는 근거가 설명되지 않는다. 산문으로만 적힌 규약은 지켜지지 않고, 컨텍스트에서 사라진 규약은 존재하지 않는 것과 같다 — 두 관찰이 같은 레이어의 두 방향이다.
4. **설치 지시를 훅 자산 일반으로 넓히고 별도 절을 만들지 않는다**: `spec-create` §3e / `spec-upgrade` Step 6의 "work log 훅 자산" 한정을 걷었다. 세 번째 스크립트용 §3f를 신설하면 `settings.json` 병합 규칙의 판정 주체가 둘로 갈린다. verbatim 복사 지시·멱등 병합 규칙·파싱 불가 시 미덮어쓰기 조항은 문구를 유지한 채 대상만 넓혔다(직전 리뷰에서 실측 보정된 문구라 재작성 금지).
5. **SessionStart matcher는 스크립트별로 다르고, 미지원 런타임에서는 무증상으로 죽는다**: `worklog-context.sh`는 matcher 없음(전 소스), `harness-context.sh`는 `"clear|compact"`. `startup`은 포인터를 보고 첫 턴에 읽는 것이 정상 동작이고 `resume`·`fork`는 컨텍스트가 복원되므로, "컨텍스트가 소실됐는데 포인터만 남는" source는 `clear`·`compact` 둘뿐이다. matcher 값 집합(`startup`/`resume`/`clear`/`compact`/`fork`)과 `|` split 매칭은 Claude Code 2.1.220 바이너리 실측이며, 이 문법을 지원하지 않는 버전에서는 훅이 오류 없이 조용히 미발동한다. 이 무증상 실패 가능성은 v4.6.13이 세운 "조용한 무력화 금지" 판단의 같은 갈래라 새 항목이 아니라 그 불릿의 announce 조항에 합류시켰다(두 스킬 Output Contract가 실행 표면).
6. **matcher 문법을 정적 근거만으로 닫지 않았다**: 등록 문자열이 틀려도 훅은 오류 없이 미발동하므로 structural check만으로는 계약이 닫히지 않는다. 픽스처 repo에서 헤드리스 세션을 구동해 `clear`·`compact` 양쪽의 `hook_success` 기록과 주입 본문(sentinel)을 관찰했고, `startup` 음성 대조로 matcher가 실제로 좁게 걸림을 확인했다. 관찰 수단과 실행 메모는 임시 실행 정보라 global spec에 올리지 않는다.
7. **주입 단위는 마커 블록이 아니라 `AGENTS.md` 전문이다**: 소비 repo에서 `AGENTS.md` ⊋ `SDD-HARNESS` 마커 블록이고, 마커 밖 내용은 그 repo가 직접 쓴 작업 규약이라 재주입 목적("작업 규약을 다시 보게 한다")에 정확히 해당한다. 마커 블록만 넣으면 SDD 자기 하네스는 살리고 그 repo 고유 규약은 버리는 셈이 된다. 이 repo는 `AGENTS.md` 전체가 마커 블록이라 dogfooding으로는 차이가 드러나지 않아, 픽스처 AC로 반증 가능하게 확인했다. 크기 상한·요약은 두지 않는다 — 자르면 무엇이 잘렸는지 모델이 알 수 없어 부분 규약을 전체로 오인하는 더 나쁜 실패가 된다.
8. **Codex 비대칭은 기존 두 훅과 동일하게 수용한다**: `.codex` 레인도 `.claude/hooks/`를 설치하지만 Codex 자신은 훅을 실행하지 않아 게이트의 강제도 하네스 재주입도 받지 않는다. 플랫폼 특성이라 `components.md` Platform Notes가 계속 소유한다.
9. **v4.6.13의 `docs/SDD_CONCEPT.md` planned 항목은 이번 구현으로 종결됐다**: 레이어 표 행과 §1 문단이 ko·en 양쪽에서 실행 자산의 두 방향을 서술하도록 갱신됐다(이 feature Task 5, ko/en 대칭 마감 검증 포함). planned 잔여로 남기지 않는다.
10. **§ 범위 리터럴은 이번에도 불변이다**: 하네스 템플릿과 `AGENTS.md`를 건드리지 않았다(draft Scope Out의 의도된 결정 — 훅의 리드 1줄이 "다시 읽지 말고 이대로 따른다"를 이미 전달하므로 템플릿에 같은 말을 또 넣으면 주입 블록 안에서 메시지가 두 번 나온다). `§0~§5` 리터럴은 변경 대상이 아니다.

### Rationale

- 하네스 레이어에 자산을 하나 더 얹는 대신 "실행 자산이 하는 일"의 정의를 한 방향에서 두 방향으로 넓히는 쪽이 표면 증가가 적다. 자산이 더 늘어도(예: 다른 규약의 복구) 같은 정의 안에서 설명된다.
- 개수 리터럴("스크립트 2개")은 자산이 늘 때마다 여러 표면에서 동시에 낡는다. 이번 census에서 이 feature 소유 표면은 개수 표기 자체를 걷어냈고(`_sdd/spec/`는 sync 소관이라 여기서 3으로 갱신), 이후에도 개수보다 역할 열거가 낡지 않는 표기임이 재확인됐다.
- 정적 근거만으로 훅 계약을 닫으면 "등록은 됐는데 발동하지 않는" 상태가 규약이 지켜지는 것처럼 보인다. v4.6.13의 fail-open 가시성 판단과 같은 문제이므로 런타임 관찰을 AC로 강제한 것이 맞다.

## 2026-07-29 - 하네스를 문서 규약에서 실행 게이트로 확장 (work log 훅을 4번째 산출물군으로 편입, v4.6.12 → v4.6.13, post-implementation sync)

### Context

하네스 §5("작업 단위 종료 시 예외 없이 work log append")는 산문 규약뿐이라 준수가 모델 재량에 달려 있었고 실제로 누락됐다. 훅은 Claude Code가 직접 실행하는 셸 명령이라 모델이 건너뛸 수 없다 — 이 차이를 이용해 §5를 실행되는 게이트로 승격했다. 변경 범위: 훅 자산 정본 2파일(`worklog-gate.sh` 5.6K / `worklog-context.sh` 1.5K) + 4벌 미러 배포, `spec-create`(신설 `#### 3e` + 5개 섹션 반영)·`spec-upgrade`(`Step 6` 확장 + 4개 섹션 반영) 각 claude·codex 2벌, 하네스 템플릿 §5 게이트 1줄(4벌) 및 §0 교체(4벌), 이 repo dogfooding 3파일 + `AGENTS.md` §5. 검증 evidence: 자체 structural check 29 PASS/0 FAIL(통제 PATH로 `jq`/`python3`를 강제 마스킹해 12 케이스 × 2파서 = 24판정 동일 + fail-open + exec bit 비의존 + 하위 디렉토리 cwd 루트 고정), fix 후 회귀 재실행 29/29 유지, `implementation-review` 게이트 1회(correctness Blocker 0 / AC 26건 전부 MET, simplicity Medium 3 — 합산 Medium 6건 fix 1회 반영), 미러 실측(`references/hooks/*.sh` 4벌 + 이 repo `.claude/hooks/` 사본까지 파일당 md5 고유해시 1종, `agents-harness-template.md` 4벌 1종, `spec-create`·`spec-upgrade` SKILL.md 각 claude↔codex 바이트 동일), `git diff --check` 무출력.

### Decision

1. **하네스 산출물 계약을 3종 → 4종으로 확장한다 (current truth 승격)**: `AGENTS.md`·`CLAUDE.md`·`.gitignore`에 훅 자산군(`.claude/hooks/` 스크립트 2개 + `.claude/settings.json` 등록)을 더한다. 착지 지점은 §2 Guardrails의 **새 불릿 1개**다 — 기존 workspace commit 경계 불릿은 "무엇을 커밋하나"를 판정하므로 "하네스 설치가 무엇을 함께 설치하나"를 겹쳐 실으면 한 불릿이 두 판정 주체가 된다. 새 결정 테이블 행은 만들지 않았다(하네스 레이어의 canonical은 §3 핵심 설계 산문이고, 그 산문을 확장하는 것이 anti-duplication에 맞다).
2. **훅은 하네스 설치와 동일 조건에 묶인다 — opt-in 없음**: 조건부 설치를 허용하면 "규약은 깔렸는데 강제는 안 깔린 repo"가 생겨 §5의 강제성이 다시 모델 재량으로 회귀한다. 설치 조건 = `AGENTS.md` 마커 블록 생성/병합 수행 여부 하나다.
3. **대상은 커밋되는 `.claude/settings.json`이고 announce가 계약이다**: 하네스는 repo 규약이라 팀 전체에 적용되어야 하므로 개인용 `settings.local.json`이 아니다. 부수 효과로 SDD를 쓰지 않는 기여자까지 커밋 게이트를 받으므로, 스킬 최종 보고의 announce(적용 범위 + 세션 첫 커밋 발동 + `SDD_SKIP_WORKLOG=1` 우회)를 산출물 계약의 일부로 고정했다.
4. **조용한 무력화 금지**: 게이트는 JSON 파서를 `jq` → `python3` 순으로 쓰고 둘 다 없으면 fail-open하되, SessionStart 훅이 "게이트 비활성"을 경고한다. 강제 자산이 침묵으로 죽으면 규약이 지켜지는 것처럼 보이는 상태가 되므로, fail-open 자체보다 가시성이 계약이다.
5. **병합 메커니즘 상세는 global spec에 올리지 않는다**: 스크립트 verbatim 복사 / `settings.json` 키 수준 멱등 병합(교체 단위 = 매칭된 `command`를 담은 **바깥 그룹 객체 전체**) / 등록 형태(PreToolUse `matcher: "Bash"`, SessionStart matcher 없음, command `bash <path>`)는 두 SKILL이 canonical이다. global에는 "동일 조건 + announce + 무력화 금지"라는 지속 판단만 남기고 포인터로 위임했다 — `Repo-wide Invariant Test` #1을 통과하지 못한다(SKILL 한 파일을 열면 규칙 전체가 보인다).
6. **JSON은 마커 블록 방식이 아니다**: `.gitignore`·`AGENTS.md`의 `SDD-HARNESS`/`SDD-WORKSPACE` 마커 규율을 `settings.json`에 확장할 수 없다(JSON에 주석 불가). 멱등 판정 키를 "`command` 문자열이 해당 스크립트 경로를 포함하는 항목"으로 두고 그룹 객체째 교체하는 방식이 대체다 — 안쪽 `{type, command}`만 갈아끼우면 `matcher`가 빠져 있던 과거 설치를 정정하지 못한다.
7. **Codex 비대칭을 수용한다**: Codex에는 훅 메커니즘이 없어 `.codex/` 레인 스킬도 `.claude/hooks/`를 설치하지만 Codex 자신은 게이트의 강제를 받지 않는다. 산출물은 대상 repo의 것이고 그 repo는 Claude Code로도 열린다는 근거다. 이 사실은 플랫폼 특성이라 `components.md` Platform Notes가 소유한다.
8. **하네스 템플릿 §0을 개인 산문 5줄에서 명명된 4원칙으로 교체한다 (draft Part 1 밖의 추가 delta)**: `plan-review-agent`(claude·codex)가 finding의 `Principle Link` 값으로 `Goal-Driven Execution` 등 원칙 **이름**을 인용하는데, 구 §0에는 그 축이 아예 없고 라벨도 없어 인용 대상이 존재하지 않았다. 또 "with me"·"please don't hesitate" 같은 개인 협업 어투가 소비 repo로 배포됐다. 교체 후 §0 = `docs/agentic_coding_principle.md`의 4축과 같은 이름 + 흡수 조항 2개(무인 실행 시 가정 기록 후 진행 / 개선 제안 장려)다. "이름을 바꾸면 인용이 끊긴다"는 사실을 §3 핵심 설계 산문에 고정했다 — 세 표면(하네스 템플릿 4벌 · `plan-review-agent` 2벌 · 원칙 문서)에 걸친 이름 결합이라 `Repo-wide Invariant Test`를 통과한다.
9. **§ 범위 리터럴은 불변이다**: 게이트 문장을 새 § 섹션이 아니라 §5 안의 불릿으로 넣어 템플릿 섹션 수를 §0~§5로 유지했다. `§0~§5` 리터럴 히트 18건은 변경 대상이 아니다 — 과거 실측에서 § 범위 문자열 전파가 반복적으로 샜다.
10. **`docs/SDD_CONCEPT.md`는 `🚧 Planned`로 고정한다**: §1 레이어 표가 하네스를 "문서 규약(how)"으로만 서술해 실행 자산 편입이 반영되지 않았다. spec sync의 대상은 `_sdd/spec/`뿐이라 이번 단위에서 문서를 고치지 않고, ko·en 짝 갱신을 planned 항목으로 남겼다(ko만 고치고 닫으면 en 세대 격차가 재발한다는 v4.6.10 운영 제약 적용).

### Rationale

- 규약을 지키게 만드는 수단이 "더 강한 문장"이면 준수는 계속 확률적이다. 실행 층(훅)으로 옮기면 강제가 결정적이 되고, 하네스는 그 층을 소비 repo에 배달할 유일한 기존 경로였다 — 새 배포 메커니즘을 만들지 않고 기존 산출물 계약을 넓히는 쪽이 표면 증가가 적다.
- 정본/미러 규율을 새로 발명하지 않고 `agents-harness-template.md`의 4벌 byte-identical 규율을 그대로 재사용했다. 자산 종류가 늘어도 동기화 판정 규칙이 하나면 census 방식이 바뀌지 않는다.
- 훅 자산을 `.md` 코드블록으로 감싸는 대안은 폐기했다 — `tools/install-codex-skill-bundle.py`가 `SKILL.md` 존재만 확인한 뒤 `shutil.copytree`로 디렉토리를 통째 복사하고 파일 형식 검증기가 없으며, `marketplace.json`이 스킬을 디렉토리 경로로 등록한다는 실측으로 `.sh` 원본 배치가 안전함이 확인됐다.
- 설치 지시를 "생성한다/사용한다"가 아니라 "Read + verbatim 복사, 재구성 금지"로 쓴 것은 과거 실측(모델이 reference를 재구성해 변경이 산출물에 누락됨)의 반영이다. 파서 fallback·판정 규칙이 재구성으로 증발하면 게이트가 조용히 약해진다.

## 2026-07-27 - `SKILL.md` frontmatter `version:` 필드 삭제, 스킬 버전 소스를 0으로 (v4.6.11 → v4.6.12, post-implementation sync)

### Context

직전 단위(v4.6.11, `skill.json` 37개 삭제)가 planned로 고정하지 않고 Open Question으로 남긴 항목 (a)를 사용자가 "지우자"로 판정해 실행했다. 그 sync는 "frontmatter `version:`이 version 단일 소스"를 고정했는데, 같은 census가 **그 단일 소스의 소비자도 0**임을 이미 보여주고 있었다 — Codex CLI 0.142.5·Claude Code 2.1.220 두 바이너리 모두 frontmatter에서 `name`·`description`만 사용하고, `tools/install-codex-skill-bundle.py`는 `SKILL.md` 존재만 확인한 뒤 디렉토리를 통째 교체하며, `.claude-plugin/marketplace.json`은 스킬을 디렉토리 경로로 등록하고, `AGENTS.md`·`README.md`·`docs/`·agent 파일(claude `.md` 5 + codex `.toml` 5)의 스킬 version 참조는 0건이다. 남은 유지 근거는 "사람이 읽는 앵커" 하나였고 그 비용은 실측된 드리프트(`guide-create` `.claude` 2.2.0 / `.codex` 2.4.0)로 계상돼 있었다. 변경 41파일 — `.claude/skills/*/SKILL.md` 21 + `.codex/skills/*/SKILL.md` 19에서 frontmatter `version:` 줄만 삭제(각 파일 diff `+0/-1`, YAML 재직렬화 없음) + `_sdd/work_log/2026-07-27.md`. 검증 evidence: structural check 8 PASS/0 FAIL, 회귀 `check_skill_json.py` 13/0·`check_gates.py` 77/0·`check_en_docs.py` 39/0, 40개 frontmatter PyYAML 전수 파싱 실패 0(잔존 키 = `name`·`description` + 선택 키), live 표면 전수에서 `^version:` 0건, `git diff --check` 무출력, 리뷰 게이트(correctness ∥ simplicity) 1회 + fix 1회(Critical/High 0, Medium 8 중 6건 반영·1건 실측 기각). correctness reviewer가 installer·marketplace·심볼릭 링크 경로를 독립 재검증해 깨지는 경로 0건을 확인했다.

### Decision

1. **직전 sync가 고정한 결정 행을 같은 자리에서 다시 바꾼다 (current truth 승격)**: §3 결정 테이블 `Skill 정의 형식` 행을 "frontmatter가 name/description(+ 런타임이 읽는 선택 키) 등 메타데이터의 단일 소스이고, **스킬 버전을 담는 필드·파일은 두지 않는다(스킬 변경 이력 = git history)**"로 교체했다. 새 결정 행도 새 guardrail도 만들지 않았다 — v4.6.11이 쓴 anti-duplication 논법과 동일하게, 이 사실은 "Markdown `SKILL.md`가 스킬 정의 형식"이라는 기존 결정의 실체 확정이므로 착지 지점은 이 행 하나다. Repo-wide Invariant Test #1도 미통과다(`SKILL.md` 하나를 열면 frontmatter 전체가 보인다).
2. **논법의 일반화 — 사이드카냐 필드냐가 아니라 소비자 유무다**: v4.6.11의 유지 이유는 "런타임이 읽지 않는 **사이드카**를 두면 드리프트가 누적된다"였으나, 이번 census는 같은 병이 **frontmatter 필드**에도 성립함을 보였다(읽히지 않는 `version:` 값이 실제로 갈렸다). 유지 이유를 "사이드카 파일(구 `skill.json`)이든 frontmatter 필드(구 `version:`)든 소비자가 없는 값은 두지 않는다"로 일반화해, 다음에 같은 부류의 필드가 제안될 때 판정 기준이 파일 형태가 아니라 소비자 census가 되게 했다.
3. **"version lockstep" 개념 완전 소멸**: 미러 쌍당 version 검사 대상이 4필드(SKILL.md 2 + skill.json 2) → 2필드(v4.6.11) → **0필드**가 됐다. 앞으로 draft는 version AC를 쓰지 않는다. 이 사실도 별도 항목이 아니라 결정 행 유지 이유의 마지막 절로만 표현했다.
4. **운영 제약 1줄은 소멸시킨다**: "스킬 version의 단일 소스는 frontmatter의 `version:` 필드다" 불릿은 지목 대상이 물리적으로 사라졌고, v4.6.11의 치환 판정 기준("그 항목이 대변하던 지속 사실이 남았나")을 적용하면 이번에는 **사실 자체가 소멸**한다 — version 갱신 discipline도, 값 드리프트도 대상이 없다. 따라서 치환이 아니라 삭제가 맞다.
5. **하위 `🚧 Planned`(미러 본문 세대 격차)는 남기되 version 재료를 걷어내고 재서술한다**: 격차 자체는 미해소이므로 planned 유지가 맞으나, 근거였던 version 값(`guide-create` 2.2.0/2.4.0, `spec-snapshot` 1.2.0)이 사라졌다. 재서술 재료는 본문 실측이다 — `guide-create` 175 / 158줄이고 **codex 쪽에는 claude 본문의 생성 가이드 템플릿 블록(`**Version**: X.Y.Z` 필드 줄)이 아예 없으며**, `spec-snapshot` 134 / 117줄이고 codex 쪽에만 legacy uppercase(`DECISION_LOG.md`) 대응 규칙이 있다. 또한 "버전 값 비교라는 우회 신호가 이제 없다"는 점을 명시해, 앞으로 미러 세대 판정이 본문 대조로만 가능함을 기록했다. `spec-snapshot` codex 쪽 규칙의 줄 번호는 이번 삭제로 밀렸으므로(`:28`→`:27`) 포인터를 줄 번호 대신 규칙 내용으로 고정했다.
6. **산문 참조 정리는 열거가 아니라 판정 규칙으로 수행한다**: live spec 3파일에서 `v?\d+\.\d+\.\d+` 전수 대조 후 **스킬 버전만** 정리했다(10줄 / 11토큰: `main.md` 5줄, `components.md` 4줄 5토큰, `usage-guide.md` 1줄). rewrite는 두 갈래다 — **(i) 현재 계약 표기**는 괄호째 삭제(`` `sdd-autopilot`(v4.0.0)은 `` → `` `sdd-autopilot`은 ``), **(ii) 역사 앵커 서술**은 버전을 feature/사건 앵커로 치환(`v2.0.0에서 개명(F5)` → `F5에서 개명`). 토큰만 지우면 `에서 …가 개명(F5)`처럼 문장이 깨진다. `components.md`의 `v3.0.0에서 마감이 강제 게이트 계약이 됐다`는 대응 feature ID가 없으므로 현재형 계약 서술(`마감은 강제 게이트 계약이다`)로 바꿔 (ii)를 해소했다. 열거로 처리하면 재드리프트한다 — 실제로 draft 초안이 `components.md` 2줄을 빠뜨렸다.
7. **문서 자체의 버전은 정리 대상이 아니다**: `main.md`의 `Spec Version`, `docs/AUTOPILOT_GUIDE.md`·`docs/en/`의 `2.1.0`, `.claude-plugin/marketplace.json`의 플러그인 metadata `1.0.0`은 스킬 버전이 아니라 그 문서/플러그인의 개정 번호다. `main.md`의 `sdd-autopilot` 불릿은 한 줄에 스킬 버전 `v4.0.0`과 문서 버전 `2.1.0`이 공존해 부분 편집으로 처리했다. `SKILL.md` 본문 보존 대상 2건(`guide-create`의 생성 가이드 템플릿 `**Version**: X.Y.Z`, `git`의 충돌 산문 `Which version?`)도 잔존을 검증 대상으로 뒀다.
8. **`user_invocable`은 같은 부류가 아니다**: simplicity reviewer가 2라운드 연속 "소비자 0인 같은 부류"로 삭제를 제안했으나 Claude Code 2.1.220 바이너리가 `user_invocable`·`user-invocable`을 실제로 읽는다(문자열 2건 실측, Codex 바이너리는 0건이라 codex 짝에 없는 것도 설명된다). 재census 방지를 위해 근거를 draft Scope Out에 고정했고, 결정 행의 "런타임이 읽는 선택 키"가 이 부류(`argument-hint`·`user_invocable`)를 가리킨다. Codex 번들 검증기의 `allowed_properties`에 이들이 없다는 점은 그 검증기가 큐레이션 패키징용이라 런타임 근거가 아니며 별건이다.

### Rationale

- 같은 결정 행을 이틀 연속 뒤집는 것은 드리프트가 아니라 **census가 결론을 앞질러 나온 순서 문제**였다. v4.6.11은 사이드카 삭제라는 변경 범위 안에서 "남은 소스는 frontmatter"까지만 확정할 수 있었고, 그 sync의 Open Question (a)가 정확히 이 후속을 지목했다. 자기모순을 피하려고 planned 고정을 유보한 판단이 사용자 판정 한 번으로 닫혔으므로, 이번 교체는 예정된 다음 조각이다.
- 삭제의 안전성은 참조 census(소극적 근거)에 더해 **바이너리 문자열 실측 + installer/marketplace/심볼릭 링크 경로의 독립 재검증**(적극적 반증)으로 확인했다. 스킬 로딩은 규약 기반이라 참조 0건만으로는 부족하다.
- 복구 앵커는 별도 tag 없이 `git show 4e9b0c0:<path>`다. 소비자가 0인 값이라 복구 수요 자체가 가설적이고, tag를 두면 없어진 개념에 이름을 다시 부여하게 된다.
- 기록물(`decision_log`·`changelog`·과거 draft·`work_log`)의 version 언급은 시점 고정이라 갱신 대상이 아니다. live 표면만 `^version:` 0건을 요구했다.

## 2026-07-27 - 죽은 사이드카 메타데이터 `skill.json` 삭제, `SKILL.md` frontmatter를 version 단일 소스로 (v4.6.10 → v4.6.11, post-implementation sync)

### Context

`skill.json`은 2026-02-14 `48bee08 add skill.json files`로 도입된 이래 **두 런타임 어느 쪽도 로드한 적이 없다**. 바이너리 문자열 실측: Codex CLI 0.142.5 네이티브 바이너리에서 `skill.json` **0회** / `SKILL.md` **75회**, Claude Code 2.1.220에서 `skill.json` **0회**(검출 2건은 별개 파일명 `.forked-skill.json`) / `SKILL.md` **222회**. `.claude-plugin/marketplace.json`은 스킬을 디렉토리 경로로 등록하고, 유일한 live 스크립트 `tools/install-codex-skill-bundle.py`는 `SKILL.md` 존재만 확인한 뒤 디렉토리를 통째로 재복사한다. 이미 `skill.json` 없이 정상 동작하던 스킬이 repo 내 3종 + `~/.codex/skills/`의 비-repo 스킬 3종 존재했다. 읽히지 않으므로 드리프트가 감지되지 않았고, 실제로 삭제 직전 40개 스킬 표면에 **12건**의 version 불일치가 조용히 누적돼 있었다(`discussion` 1.5.0/1.2.0, `implementation-review` 7.0.0/2.1.0·3.0.0, `investigate` 4.0.0/1.0.0, `pr-review` 4.0.0/2.0.0, `spec-create` 1.10.0/1.9.1 등). 변경 39파일(`.claude` 19 + `.codex` 18 삭제, `.claude/skills/spec-snapshot/SKILL.md`에 `version: 1.2.0` 추가, `_sdd/env.md` 1줄). 검증 evidence: structural check 14 PASS/0 FAIL, 회귀 `check_gates.py` 79 PASS/0 FAIL·`check_en_docs.py` 39 PASS/0 FAIL, 40개 SKILL.md frontmatter PyYAML 전수 파싱 실패 0·`version` 누락 0, `find -name skill.json` 0건, live 표면 전수 grep 0건, `git diff --check` 무출력, implementation-review(correctness ∥ simplicity) 1회 + fix 1회(Critical/High 0, Medium 9 중 4건 반영·1건 실측 기각).

### Decision

1. **값 정렬이 아니라 파일 삭제로 종결한다 (current truth 승격)**: 12건의 version 불일치는 증상이고 원인은 "읽히지 않는 사이드카가 존재한다"는 구조다. 값을 맞추면 다음 편집에서 같은 드리프트가 재발하고, 읽는 주체가 없어 재발이 다시 감지되지 않는다. 드리프트가 생길 자리 자체를 없앤다.
2. **version 단일 소스 = `SKILL.md` frontmatter의 `version:` 필드**: 스킬 메타데이터를 담는 사이드카 파일은 두지 않는다. 이 판단은 새 guardrail이 아니라 §3 결정 테이블 `Skill 정의 형식` 행의 확장으로 표현했다 — "Markdown `SKILL.md`가 스킬 정의 형식"이라는 기존 결정의 실체를 확정한 것이므로, 별도 결정 행을 만들면 판정 주체가 둘로 갈린다(anti-duplication, v4.6.10과 동일 논법).
3. **"version 4필드 lockstep" 개념 소멸**: 미러 쌍당 version 검사 대상이 4필드(SKILL.md 2 + skill.json 2)에서 2필드로 줄었다. 앞으로 draft가 version AC를 쓸 때 4필드를 요구하지 않는다.
4. **`main.md`의 planned 항목은 삭제가 아니라 치환으로 종결한다**: 기존 `🚧 Planned`("`implementation-review` version 4필드 불일치")가 지목한 대상(`skill.json` `2.1.0`/`3.0.0`)은 물리적으로 사라졌고 남은 2필드는 이미 일치(`7.0.0`)라 항목 자체는 소멸이 맞다. 그러나 상위 불릿("일부 version metadata 갱신은 문서 편집 discipline에 의존한다")은 여전히 참이고 실재 사례가 남아 있다 — 미러 쌍 전수 대조 결과 live version 드리프트는 `guide-create`(`2.2.0`/`2.4.0`) 1건이다. 단순 삭제로 닫으면 repo에 유일하게 남은 live 드리프트가 spec 어디에도 기록되지 않으므로, 불릿을 version 단일 소스 서술로 재작성하고 하위 planned를 **미러 본문 세대 격차**로 교체했다.
5. **`spec-snapshot` claude 미러의 `version` 결번을 같은 단위에서 보정한다**: `.claude/skills/spec-snapshot/`은 `skill.json`도 없고 frontmatter에도 `version:`이 없어 이 변경 **전에도** version 소스가 0이던 유일한 스킬이었다. frontmatter를 단일 소스로 세우는 변경에서 유일한 빈칸이라 codex 짝과 같은 `1.2.0`으로 채웠다(범위 확장 1파일).
6. **미러 본문 세대 격차는 planned로 고정하되 canonical 방향은 미정으로 둔다**: `guide-create`(176줄/159줄)와 `spec-snapshot`(135줄/118줄, codex `:28`에만 legacy uppercase 대응 규칙)은 같은 버킷이다 — version 값이 아니라 본문 세대가 갈렸고, 어느 쪽이 구세대인지는 본문 대조가 선행되어야 근거 있게 단정할 수 있다. `spec-snapshot`은 version을 맞춘 탓에 version만으로는 격차가 보이지 않게 됐으므로 명시 기록이 특히 필요하다.
7. **`version:` 필드 자체의 폐지는 planned로 고정하지 않는다**: 이번 census로 `version:` 값을 읽는 런타임·스크립트·문서가 0임이 확인됐고(두 바이너리 모두 name/description만 사용, `tools/`는 `SKILL.md` 존재만 확인, `marketplace.json`·`AGENTS.md`·`README.md`·`docs/` 0건), 추적 canonical은 §3 `artifact naming/history` 행이 이미 git-history-first로 선언한다 — `skill.json`과 같은 논법이 성립한다. 그럼에도 planned로 고정하지 않는 이유는 **이번 결정 2와 정면으로 충돌**하기 때문이다. 같은 sync에서 "frontmatter `version:`이 단일 소스"를 고정하면서 "그 필드를 전부 없앤다"를 planned로 박으면 spec이 자기모순 상태가 된다. 사용자 판정 사항으로 Open Question에만 남긴다.

### Rationale

- 삭제의 안전성은 "참조가 없다"는 소극적 근거가 아니라 **바이너리 문자열 실측 + 무-`skill.json` 스킬 6종의 정상 동작**이라는 적극적 반증으로 확인했다. 참조 census만으로는 네이티브 로더가 규약 기반으로 읽을 가능성을 배제할 수 없다.
- planned 항목의 종결 형태(삭제 vs 치환)는 "지목 대상이 사라졌나"가 아니라 "그 항목이 대변하던 지속 사실이 사라졌나"로 판정했다. 대상은 소멸했지만 사실(version 갱신이 편집 discipline 의존)은 남았고 실례도 남았다.
- 기록물(`decision_log`·`changelog`·`logs/prev/`)의 과거 `skill.json` 언급은 시점 고정 기록이라 갱신 대상이 아니다. live 표면(`.claude/`·`.codex/`·`.claude-plugin/`·`tools/`·`docs/`·`AGENTS.md`·`CLAUDE.md`·`README.md`·`_sdd/env.md`)만 0건을 요구했다.
- Codex 번들 검증기의 `allowed_properties = {name, description, license, allowed-tools, metadata}`에 `version`·`argument-hint`가 없는 점은 이번 범위 밖으로 뒀다 — 같은 스크립트에 `Repo path to list (default: skills/.curated)`가 있어 큐레이션 저장소용 패키징 검증기로 보이고 런타임 로더가 아니며, 현재 스킬이 정상 로드된다. 근거가 추정 수준이라 planned로 고정하지 않는다.

## 2026-07-26 - `docs/en` 미러 세대 drift 해소 + ko/en 대칭 마감을 운영 제약으로 고정 (v4.6.9 → v4.6.10, post-implementation sync)

### Context

v4.6.9 sync가 planned로 고정한 en drift 항목(`docs/en/SDD_WORKFLOW.md`가 ko보다 한 세대 뒤처짐)을 draft 없는 inline task로 처리했다. census 결과 원인은 단일했다 — 2026-06-12 하네스 레이어(`AGENTS.md`) 도입이 en 미러에 전파되지 않아 `SDD_WORKFLOW` §2 Harness와 `SDD_CONCEPT` §1 Harness 행이 동시에 빠졌고, 그 세대에 정리된 full 레인 어휘도 en에만 남았다. 실측(HEAD `c4aabef` 대조): en `SDD_WORKFLOW` 섹션 9 → 10(ko와 동수), full 레인 어휘 HEAD 5곳(L11 `implementation plan`·L13 `review-fix loop`·L43 `touchpoints`·L44 `implementation plan`·L45 `validation plan`) → 0곳, 변경 6파일(ko 3 + en 3, 전부 `docs/`, +29/−25). 검증 evidence: structural check 35 PASS/0 FAIL(섹션 수·줄 수 parity, ko/en 짝 대칭 변경, 변경 파일 6개 한정 포함), 직전 feature 회귀 `check_gates.py` 79 PASS/0 FAIL, `git diff --check` 무출력, implementation-review(correctness ∥ simplicity) 1회 + fix 1회(Critical/High 0, Medium 4건 중 2건 반영).

### Decision

1. **en 미러 세대 drift 해소 (current truth 승격, planned 항목 종결)**: en `SDD_WORKFLOW`에 ko §2 "Harness가 쓰이는 시점" 대응 섹션을 신설하고 기존 §2~§9를 §3~§10으로 재번호했으며, §1 flow를 ko와 같은 producer 게이트 2행으로, §4 temporary spec 구성을 ko의 3항목으로 맞췄다. en `SDD_CONCEPT` §1 레이어 표에 `Harness (AGENTS.md)` 행과 경계 문단을 추가했다. ko/en 6쌍 parity 불일치 0.
2. **ko/en 미러 대칭 마감을 운영 제약으로 고정**: 이 drift는 설계 변경이 아니라 canonical rollout 순서(`... -> docs -> english mirrors/examples -> audit`)의 `english mirrors` 단계 누락이 한 세대 누적된 형태였다. 새 guardrail을 만들지 않고 기존 rollout 결정에 대한 enforcement 제약("ko/en 짝을 건드리는 변경은 대칭 마감을 검증 대상으로 둔다")을 `현재 운영 제약`에 1줄로 남긴다 — 레이어 모델 자체의 단일 소스는 계속 `docs/SDD_CONCEPT.md`·`docs/SDD_WORKFLOW.md`이므로 global spec 본문은 키우지 않는다.
3. **어휘 정렬 2건은 리뷰 게이트 finding 반영분이다**: (a) correctness M1 — CONCEPT ko·en의 temporary spec 행을 구세대 어휘(`delta, touchpoints, validation, plan`)에서 현행 draft 구조(`delta, scope, task별 contract/AC, target files`)로 교체, (b) simplicity M3 — `temporary spec 또는/or feature draft` alternation 6곳을 canonical 등가 표기(`docs/SDD_SPEC_DEFINITION.md:149` "temporary spec(= feature draft)")로 통일. 함께 F2에서 삭제된 `implementation-plan` 스킬 참조를 QUICK_START ko·en에서 `feature draft`로 정리했다.
4. **계약 정정 2건**: (a) inline AC "ko 원본 무변경"은 위 두 finding이 ko·en 대칭 수정을 요구해 폐기하고 "변경 6파일 한정 + ko/en 짝 대칭" 가드로 교체했다(계약 오류가 아니라 사용자 승인 범위 확장). (b) 직전 feature Task 4 AC3의 가드가 `docs/SDD_WORKFLOW.md` **파일 단위** 무변경이라 이번 §4 1줄 변경에 오탐했으므로, 그 AC의 의도(`:9-11` producer 소유 서술 보존)대로 앵커 블록 8줄 대조로 좁혔다 — §1 flow 블록은 `540f1d5`와 byte-identical임을 확인했다.
5. **보류 finding은 global spec에 planned로 고정하지 않는다**: simplicity M1(`SDD_WORKFLOW` §2 둘째 문단이 `SDD_CONCEPT` §1 문단과 소유권 규칙 중복 — 포인터 대체 제안)·M2(§3 "global spec은 모든 단계의 출발점"이 §2 "하네스를 먼저 읽는다"와 긴장 — ko·en 문장 재작성 제안)는 내용 정합은 유지된 supporting doc 산문 품질 이슈로, repo-wide invariant 기준(2개 이상 표면 공통 + 틀리면 repo-level 판단 어긋남)을 통과하지 못한다. Low 잔여(README:14 "예시 포함"이나 예시 0건, README:16 "두 단계 구조"이나 5레이어, `docs/agentic_coding_principle.md` en 미러 부재 — 단 README:18이 부분 커버리지를 이미 명시)도 같은 판정이다. 모두 이 entry와 work_log에만 남긴다.

### Rationale

- planned 항목의 종결 조건은 그 bullet이 명시한 관찰 가능한 두 조건(섹션 수 동수, full 레인 어휘 0)이었고 둘 다 fresh 검증으로 충족됐다. 종결 후 남길 지속 정보는 "무엇이 틀렸었나"가 아니라 "왜 반복되나"이므로 drift 서술을 전례 각주로 압축해 운영 제약으로 옮겼다.
- 새 guardrail 대신 기존 rollout 결정에 enforcement 1줄만 붙인 이유는 anti-duplication이다. `english mirrors` 단계는 이미 결정 테이블에 있으므로, 같은 규칙을 guardrail로 재선언하면 판정 주체가 둘로 갈린다.
- `touchpoints`는 이번에 CONCEPT ko·en까지 정리됐지만 repo 전역 0은 아니다 — `spec-rewrite`/`spec-upgrade` references, `spec-review`·`spec-sync-agent`, `SDD_SPEC_DEFINITION`의 legacy 기록물 서술에는 의도적으로 남아 있다(구형 full draft 형식을 읽을 때의 기준). 이 구분을 흐리면 legacy fallback 계약이 지워진다.

### Changes

- `main.md` — 헤더 4.6.10. `현재 운영 제약`: en drift `🚧 Planned` bullet을 소거하고 ko/en 미러 대칭 마감 운영 제약 1줄로 대체. 레이어 모델·temporary spec 구성·등가 표기는 canonical 문서가 단일 소스라 §1~§3 본문 무변경
- `components.md`·`usage-guide.md` 변경 없음(Strategic Code Map은 ko canonical 경로만 싣는다)
- draft 없음 — inline task 진행. 처리한 input file 없음(HEAD 대조 + 코드 evidence만 사용)

## 2026-07-26 - SDD 체인 품질 게이트를 producer 스킬 소유로 고정 (v4.6.8 → v4.6.9, post-implementation sync)

### Context

게이트 소유자가 표면마다 어긋나 있었다: `feature-draft`는 `plan-review`를 강제 게이트로 소유하는데 `implementation`은 `implementation-review`를 "선택 — 강제 아님"으로만 권유했고, `sdd-autopilot` Step 2는 두 게이트를 자기가 다시 호출했다. 반면 `docs/SDD_WORKFLOW.md:9-11`은 이미 producer 소유 모델을 문서화하고 있었다 — 즉 이 변경은 새 설계가 아니라 스킬 본문·autopilot이 문서 모델을 따라잡는 drift 정리다. 실측: `implementation` 4필드 `3.0.0`, `sdd-autopilot` 4필드 `4.0.0`, 하네스 §3 5곳(`AGENTS.md` + `spec-create`·`spec-upgrade` 템플릿 claude/codex 4미러)에 체인 리터럴 1건 유지 + 게이트 예외 1줄 각 1건, `docs/AUTOPILOT_GUIDE.md` ko/en `2.1.0`. 검증 evidence: structural check 79항목 PASS/0 FAIL(게이트 호출자 census 2갈래 + 패턴 매치력 역검증 포함), plan-review 1회 + implementation-review(correctness ∥ simplicity) 1회 + fix 1회, `git diff --check` 무출력.

### Decision

1. **품질 게이트는 producer 스킬이 소유한다 (current truth 승격)**: `feature-draft`가 `plan-review`를, `implementation`이 `implementation-review`를 각각 자기 마감의 강제 게이트로 단일 패스 1회 수행하고 fix 1회도 producer가 수행한다. 호출자(autopilot·사용자)는 게이트를 별도 호출하지 않고 "선택" 해치도 두지 않는다.
2. **`implementation` 마감은 게이트 계약이다**: 회귀 1회 → AC→증거 테이블 → `implementation-review` 1회 + Critical/High/Medium fix 1회(fix 시 회귀 재실행 + 증거 테이블 갱신, Low는 advisory) → 마감 요약(게이트 finding·fix 내역·잔존 finding 포함). 이 반환 계약은 `implementation`에만 적용한다 — `feature-draft`의 출력 다이어트(마감 노출을 Open Questions로 제한)는 의도된 설계이고 plan gate 잔여 이슈 보고 의무는 기존 review-only 금지 guardrail이 소유한다.
3. **`sdd-autopilot`은 producer 3스킬 순차 호출 + 반환 종합 보고다**: Step 2 = `feature-draft` → `implementation` → (persistent 변경 시) `spec-sync` → 최종 보고 4항목. 분할 판정 canonical 목록에서 `plan-review: 규모 판정 검사`를 빼고 producer 두 스킬만 남긴다(plan gate의 규모 판정은 canonical을 재정의하지 않는 rubric).
4. **하네스 §3은 체인 리터럴을 유지하고 예외를 1줄로 명시한다**: 리터럴은 SDD **단계** 순서라 무변경이되, 뒤 문장이 "해당 단계 진입 시 그 스킬을 호출한다"로 호출 주체까지 명령하므로 게이트 두 단계는 producer 내부 수행이라 별도 호출하지 않는다는 예외를 5곳(전파 표면)에 동일 적용한다.

### Rationale

- 게이트 소유자를 산출물 작성자로 고정하면 진입 경로(직접 호출·autopilot)에 관계없이 같은 품질 계약이 걸린다. "선택 게이트" 해치는 직접 호출 경로만 조용히 품질이 낮아지는 분기를 만든다.
- 호출자가 게이트를 다시 도는 구조는 producer가 이미 소유한 게이트와 중복이고, finding/fix 내역의 소스가 둘로 갈린다. producer 반환을 유일 소스로 두면 autopilot은 종합 보고만 하면 된다.
- 하네스 체인 리터럴 자체를 건드리면 단계 어휘가 흔들리고 소비 repo 전파 표면 5곳이 재작성 대상이 된다. 리터럴 유지 + 예외 1줄이 최소 변경이다.

## 2026-07-26 - `ralph-loop-init` 런타임 안전장치·자체검증 실효화 (v4.6.7 → v4.6.8, post-implementation sync)

### Context

draft `_sdd/drafts/_processed_2026-07-26_feature_draft_ralph_loop_init_hardening.md`(10 task)가 구현·리뷰 게이트를 통과했다. 실측: 두 미러 `SKILL.md` + 두 `skill.json` 4파일 version `4.1.0` 동기, 산출물 목록 6파일(AC1·Step 8 요약 동일), `MAX_RUNTIME_MINUTES`/`MAX_ITERATIONS`/`DEADLINE` 관련 라인 두 미러 대칭(각 16건), `decisions.md` 생성·`tail` 읽기·`--reset` 초기화 존재, 스킬 AC3가 `bash -n` + 실행 권한으로 재작성됨, dead state 필드 3종(`errors`/`last_checkpoint`/`validation_results`)과 리터럴 `<placeholder>` 잔존 0. 검증 evidence: SKILL.md에서 템플릿을 추출한 structural check 80항목 PASS/0 FAIL(`bash -n` 포함), CLI 스텁 기반 기능 검증 5건(iteration backstop / wall-clock deadline / DONE 순서 — 변경 전 템플릿으로 유실 버그 재현해 RED→GREEN 실증 / DONE 재시작 가드 / zero-padded iteration), plan-review 1회 + implementation-review(correctness ∥ simplicity) 1회 + fix 1회.

### Decision

1. **무인 루프에 기계적 상한을 둔다 (current truth 승격)**: 종료 압력을 LLM 자기판단에만 맡기지 않는다. 주 상한은 wall-clock(`MAX_RUNTIME_MINUTES`, 기본 720분, 실행 1회 기준으로 재실행 시 리셋)이고 `MAX_ITERATIONS`(기본 200, 누적)는 폭주 backstop이다. 축을 둘로 나눈 이유: ralph는 iteration당 소요가 5분~6시간으로 편차가 커 iteration 수가 실행 시간의 대리지표가 못 되고, 반대로 LLM이 매번 성공하면서 action.sh를 안 쓰는 무진전 공회전은 시간이 아니라 토큰을 태워 wall-clock으로 안 막힌다. wall-clock 판정은 **soft**다 — iteration 경계에서만 보므로 진행 중인 학습·빌드를 죽이지 않는 대신 총 실행 시간이 마지막 action 길이만큼 예산을 넘을 수 있다. 상한 도달 시 `phase:`를 보존하고 `notes:`만 갱신한 뒤 `exit 1`한다: 무인 실행에서 상한 도달은 정상 완료가 아니므로 비-0이어야 하고, phase를 DONE으로 강제하면 상한을 올려도 결과를 지우는 `--reset` 외엔 재개 수단이 없어진다.
2. **DONE 판정 지점은 2곳이다 (draft 계약 정정)**: 초안은 "판정을 action.sh 실행 뒤로 이동, 판정 1곳"이었으나 구현 리뷰에서 계약 오류로 판정됐다. 이동만 하면 이미 `phase: DONE`인 state로 재실행할 때 변경 전(즉시 break)과 달리 무인 LLM 턴 1회와 그 턴이 쓴 임의 action.sh 실행을 추가로 받는다 — `--dangerously-skip-permissions` 루프에서 이번 변경 주제와 역행한다. 따라서 루프 진입 가드(LLM 호출 전, `exit 0`)와 action 실행 뒤 사후 판정은 역할이 다른 별개 지점이며 복제가 아니다. 확정된 iteration 순서는 `진입 DONE 가드 → 상한 판정 → LLM → state 검증 → action.sh 실행/archive → 사후 DONE 판정`이고, 이로써 DONE으로 전환한 iteration의 action도 실행·archive된다(ANALYZING이 action.sh로 `final_report.md`를 만드는 경로에서 리포트가 유실되던 버그 해소).
3. **init 시점 자체검증을 falsifiable하게 바꾼다**: 리터럴 `<placeholder>` 검사는 실제로 남는 슬롯(`<project name>`·`<main execution command>`)을 못 잡아 실효가 없었다. 검사 기준을 "지정 범위에 미충전 `<...>` 슬롯 0"으로 교체하고 범위의 단일 소스를 스킬 Step 8에 둔다 — `config.sh`·`run.sh`·`state.md`·`CHECKS.md` 전 문면 + `PROMPT.md`의 문서 시작~`## Iteration Protocol` 직전(H1의 `<project name>` 포함) + `## Known Errors`. 그 밖의 `<...>`는 루프 LLM을 향한 서식 지시이므로 검사 대상이 아니다. 함께 `bash -n`(run.sh·config.sh)을 Step 8 절차로 넣고, 루프를 돌리기 전엔 판정 불가였던 스킬 AC2·AC3를 init 시점 관찰로 판정 가능한 문장으로 재작성했다.
4. **`decisions.md`를 6번째 산출물로 승격**: PROMPT.md가 읽고 쓰는데 어떤 Step도 만들지 않던 파일이다. 생성 산출물 목록의 단일 소스는 AC1과 Step 8 요약 출력이며, 읽기는 항상 파일 끝 일부(`tail -n 200`)만 본다(로테이션 메커니즘 없음). state.md의 dead schema 3필드는 제거해 매 iteration LLM이 읽는 표면에서 잡음을 뺐다.
5. **ralph 진입 경계를 스킬이 스스로 선언한다**: `investigate`·`goal-init`은 각자 ralph와의 경계를 선언해 뒀는데 ralph만 침묵했다. 세션 수명 초과·무인 격리 실행·iteration마다 fresh context 필요·단일 실행이 시간 단위일 때만 ralph이고, 세션 안에서 닫히는 반복은 `investigate`(단발 디버깅)와 네이티브 `/goal`(조건·하네스 셋업은 `goal-init`)로 라우팅한다. 이 경계는 컴포넌트 수준 라우팅이라 global guardrail이 아니라 `components.md` reference에 둔다.
6. **범위 밖(불변)**: ralph 상태 머신 phase 구성, Step 1~2 discovery 로직, 생성된 `ralph/`의 실제 런타임 검증(격리 환경 필요). `sdd-autopilot`에 ralph 진입 힌트를 재도입할지는 사용자 결정 대기 항목이다.

### Changes

- `components.md` — `ralph-loop-init` 행을 v4.1.0 계약으로 갱신(5파일→6파일, 고정 루프 제어 변수 4개와 두 상한의 축·soft·phase 보존, iteration 순서, init 시점 `bash -n`+슬롯 0 검사와 범위 단일 소스, 진입 경계). codex CLI flag delta 보존 서술은 유지
- `main.md` — 헤더 4.6.8. 런타임 상한·판정 순서는 단일 스킬 안에서 복구되는 컴포넌트 계약이라 repo-wide invariant 기준을 통과하지 못해 본문 무변경
- draft `_processed_` 이동

## 2026-07-22 - 스탠드얼론 reviewer/generator agent를 직접 실행 skill로 흡수 (`spec-review`·`ralph-loop-init`, v4.6.6 → v4.6.7, post-implementation sync)

### Context

draft `_sdd/drafts/2026-07-22_feature_draft_standalone_agents_to_skills.md`가 구현·리뷰 게이트(verify.py 구조검사 18/18 PASS + correctness/simplicity blocker 0)를 통과했다. 실측: 4개 agent 파일(`.claude/agents/spec-review-agent.md`·`.codex/agents/spec-review-agent.toml`·`.claude/agents/ralph-loop-init-agent.md`·`.codex/agents/ralph-loop-init-agent.toml`) 부재, 잔존 `.claude/agents` 5종·`.codex/agents` 5종(+README), marketplace.json `agents` 배열 5원소(`plan-review`·`implementation-review`·`simplicity-review`·`pr-review`·`spec-sync`), 두 skill 4개 version 필드 모두 `4.0.0`, 흡수 skill 4파일에 wrapper 잔재(`entrypoint wrapper`·`위임`·`subagent_type`·`spawn_agent`·`Codex Runtime Adapter`) grep 0, live 표면(`.claude/`·`.codex/`·`.claude-plugin/`) 삭제 agent 식별자 census 0.

### Decision

1. **스탠드얼론 reviewer/generator agent를 직접 실행 skill로 흡수 (current truth 승격)**: `spec-review`·`ralph-loop-init`은 "thin wrapper skill → agent(계약 보유)" 2홉이 아니라 메인 루프가 본문을 직접 수행하는 직접 실행 skill이다. 계약·프로세스·rubric/상태 머신·출력 형식의 단일 소스는 각 SKILL.md(claude+codex)이며, 두 agent의 claude `.md`·codex `.toml` 4파일은 삭제됐다. 근거: 두 agent는 자기 wrapper만 dispatch하는 스탠드얼론 entrypoint라 프로그래밍적 재사용 대상이 없고, 자동 SDD 체인 소속이 아니라 보호할 host 컨텍스트가 없어 subagent 격리 이득이 0이다. 추가로 ralph-loop-init의 Step 2 대화형 사용자 확인 게이트는 subagent가 실행 중 대화할 수 없어 무력화 상태였는데, skill 전환으로 메인 루프가 직접 수행하며 비로소 작동한다.
2. **등록 agent set 7 → 5**: `plan-review-agent`·`implementation-review-agent`·`simplicity-review-agent`·`pr-review-agent`·`spec-sync-agent`만 남는다.
3. **`spec-sync`는 이 전환에서 제외 (경계 확정)**: autopilot·체인이 프로그래밍적으로 dispatch하는 체인 종결 mutator라 spec 편집 추론을 오케스트레이터 컨텍스트에서 격리하는 이득이 load-bearing이다(plan-review·implementation-review agent 유지 근거와 동일). 따라서 wrapper-backed skill + single-source agent 패턴은 잔존 agent(특히 `plan-review`·`implementation-review`·`spec-sync`)에 대해 여전히 참이다.
4. **불변 계약**: skill trigger·산출물 경로 계약(`_sdd/spec/logs/spec_review_report.md`, `ralph/` 산출물)은 불변. codex `ralph-loop-init`은 run.sh LLM 호출·Security Notice의 CLI flag delta(`--dangerously-bypass-approvals-and-sandbox`)를 보존한다.

### Changes

- `components.md` — `spec-review`·`ralph-loop-init` 행의 Primary Source를 SKILL.md 쌍(claude+codex)으로 교체하고 Notes를 직접 실행 skill 계약으로 재서술(stale "wrapper -> agent 패턴"·삭제된 `.claude/agents/*-agent.md` 경로 제거). Platform Notes `Claude skill/agent split`의 직접 실행/wrapper-backed 분류를 두 skill 흡수 후 상태로 정합
- `main.md` — 헤더 4.6.7. wrapper-backed skill 아키텍처 서술은 spec-review/ralph를 지명하지 않고 잔존 5 agent에 대해 참이라 본문 무변경
- draft `_processed_` 이동

## 2026-07-22 - F5 완료: `-lite` 개명 승격 — F1~F5 전체 완결 (v4.6.5 → v4.6.6, post-implementation sync)

### Context

분할 todo F5(자체 draft: `_sdd/drafts/_processed_2026-07-22_feature_draft_lite_rename_drop_lite.md`)가 구현·리뷰 게이트(correctness C/H/M 0 전 AC MET·simplicity M2 fix 완료)를 통과했다. 실측: 스킬 디렉토리 `feature-draft`·`implementation` 존재(-lite 부재, git mv 4디렉토리), name·version 2.0.0 동기, marketplace JSON 유효 + lite 참조 0, 개명 스킬 미러 identical, live 표면(`.claude/`·`.codex/`·`.claude-plugin/`·`docs/`·`README.md`·`AGENTS.md`) 개명 census 잔존 0, autopilot Step 0→1→2, `> 규모 판정:` 마커 소비자 3곳 교체 확인.

### Decision

1. **F5 개명을 current truth로 승격, F1~F5 전체 완결 기록**: 🚧 Planned F5 todo를 소거하고 완결 서술로 대체한다. full 레인 삭제 + `-lite` 개명이 모두 끝나 분할 계획 원본 draft를 `_processed_` 마감한다.
2. **`_sdd/spec/` 3파일 lite 어휘·구명 트림** (F5 draft가 spec-sync 소관으로 명시): 구명 → 새 스킬명, "lite 체인"→"SDD 체인"/"체인", "lite draft"→"draft", "Lite 적격 검사"→"규모 판정 검사", components.md의 실존하지 않는 `-lite` 경로 → 새 경로. F2 서술의 full 스킬 쌍 3종은 "당시 이름 `feature-draft`·`implementation`·`implementation-plan`"으로 한정해 F5 개명 후 동명 현행 스킬과 구분한다. 구 "Tier 2-lite" 명칭 소멸 서술은 legacy 이름 인용이라 유지한다.
3. **어휘 계약 확정**: 마커 `> Lite 적격:` → `> 규모 판정:`(값 "적격"/"분할 필요 — 분할 계획 포함"), 검사명 "규모 판정 검사", draft 파일명 glob `*_feature_draft_*` 통일(기존 lite 파일명 substring 하위호환), lite 트리거 별칭 제거.

### Changes

- `main.md` 4.6.6 — §1 entrypoint 예시 개명. §2: F5 todo 소거·F1~F5 완결 승격, F2 서술 동명 구분, 체인·마커 어휘 전면 교체. §3: 실행 분리·오케스트레이션·규모 초과 대응·planning precedence·implementation test-first·code map 행 갱신
- `components.md` — `feature-draft`·`implementation` 행 개명(경로·버전 포함), autopilot·plan-review·spec-sync·spec-review 행 어휘 교체, Strategic Code Map 경로 갱신
- `usage-guide.md` — Scenario 2/2b 커맨드·체인 서술 개명
- F5 draft·분할 계획 원본 draft `_processed_` 이동 (F1~F5 완결로 분할 계획 마감)

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
