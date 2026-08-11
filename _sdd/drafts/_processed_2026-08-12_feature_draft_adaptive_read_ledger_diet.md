# Feature Draft: 리뷰 읽기 다이어트 2 — 위험 적응형 읽기 + ledger MET 접기

> 규모 판정: 적격 (변경 요소 2개 — 읽기 계단 개편·ledger 다이어트 — 가 agent 2종 짝 4파일에 국한, 눈검산 가능. 구 문면 제거 census 신호 있음 → Part 2 마지막 read-only 검증 task 포함)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

리뷰 읽기 다이어트 롤링 분할의 Feature 2 (Feature 1 = Claim Manifest, 별도 draft로 완료). 사용자 지시로 plan-review 게이트 생략(최소 리뷰 정책).

**바뀌는 contract**:
- **위험 적응형 읽기**: implementation-review-agent Step 3 ①의 변경 파일 읽기를 "전문 Read 상한 없음" → "**diff hunk+주변 문맥 기본, 승격 트리거 시 파일 전문**" 계단으로 개편. 승격 트리거 6종(하나라도 해당 시 전문): ①실행 semantics 파일(스크립트·훅·코드 — 산문 문서 제외) ②hunk가 제어 흐름·상태·에러 경로 접촉 ③해당 AC가 행동 AC(실행/테스트 검증형) ④파일 대비 변경 비율 높음(사실상 재작성) ⑤hunk 검토 중 결함 의심 발견 ⑥draft가 해당 task에 Open Questions·낮은 확신도 표기. 미승격 파일은 반환에 `hunk-scoped` 표기. 기준 문서 전문 Read·spec 절 한정·correctness 능동 검토 결속은 불변.
- **ledger MET 접기**: implementation-review-agent Verification ledger와 pr-review-agent AC 검증 ledger를 "문제 있는 verdict(NOT MET·UNTESTED·PARTIAL·FAIL)만 증거 행, 통과(MET) verdict는 축약 한 줄"로 다이어트. **판정 의무는 불변**(증거 없는 MET 금지 유지) — 통과 증거를 반환에 전사하지 않을 뿐(감사 흔적만 희생, 탐지 보존).

## Scope
- **In**: implementation-review-agent·pr-review-agent 짝 4파일(계약 문면), 구 문면 census.
- **Out**: plan-review·simplicity-review(이미 PASS 접기 적용됨), orchestrator SKILL(ledger 연접 서술은 형식 중립이라 무변경), spec surface(spec-sync 소관), 속도 실측(플러그인 캐시 지연 — 구조 AC만).
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | 두 계약 변경의 codex 미러 반영 | `.codex/agents/implementation-review-agent.toml`, `.codex/agents/pr-review-agent.toml` | CM1~CM3 query의 codex 측 결과가 claude 측과 동형 → Task 3 완료 후 구 문면 0건 | Task 3 |

# Claim Manifest

| ID | Claim | Query | Expected |
|---|---|---|---|
| CM1 | impl-review Step 3 ①이 "전문 Read, 상한을 걸지 않는다"로 시작 | `grep -rn "전문 Read, 상한을 걸지 않는다" .claude .codex` | 2건 (agent 짝) |
| CM2 | impl-review ledger가 "각 AC마다 한 행" + "증거 없는 MET 금지" | `grep -rn "각 AC마다 한 행" .claude/agents/implementation-review-agent.md .codex/agents/implementation-review-agent.toml` | 각 1건 |
| CM3 | pr-review ledger가 "각 AC마다 한 행" + "모든 verdict는 증거에 묶인다" | `grep -rn "각 AC마다 한 행" .claude/agents/pr-review-agent.md .codex/agents/pr-review-agent.toml` | 각 1건 |
| CM4 | `hunk-scoped` 표기는 현재 미존재 | `grep -rn "hunk-scoped" .claude .codex` | 0건 |

# Part 2: Tasks

### Task 1: implementation-review-agent 위험 적응형 읽기 + ledger 접기 (claude)

pole인 correctness shard의 읽기량·작성량을 함께 깎는다 — 별거 아닌 변경(산문·구조 AC·무신호)은 hunk로 닫고, 위험 신호만 전문으로 승격.

**Contracts**: Part 1 서술이 canonical — 추가분만: Step 3 ① 개편 시 기존 overflow 규칙(AC 관련도·diff hunk 밀도 순)과 limitation 표기는 유지하되 대상이 "전문 Read하지 못한 파일"에서 "승격 파일 중 전문 Read하지 못한 파일"로 좁혀진다. ledger 축약 행 형식은 `MET: AC1–AC5` 꼴. AC3(CM2 참조)·Hard Rule 5 문구를 반환-측 다이어트와 정합시키되 판정-측 "증거 없는 MET 금지"는 보존.

**Acceptance Criteria**:
- [ ] AC1: Step 3 ①이 hunk 기본+승격 트리거 6종+`hunk-scoped` 표기 계단이다. 평가(1등급): CM1 query 해당 파일 0건 + `hunk-scoped`·트리거 anchor(`실행 semantics`·`재작성`) grep ≥ 각 1건.
- [ ] AC2: Step 6 ledger가 MET 접기 형식이고 AC3·Hard Rule 5가 정합이다. 평가(2등급): reviewer가 세 절 인용 — 접기 형식·판정 의무 보존·상호 모순 없음 판정.
- [ ] AC3: CM2 query 해당 파일 0건("각 AC마다 한 행" 제거). 평가(1등급): grep 출력.

**Target Files**:
- [M] `.claude/agents/implementation-review-agent.md` -- Step 3 ①·Step 6·AC3·Hard Rule 5

### Task 2: pr-review-agent ledger 접기 (claude)

동일 구조의 AC 검증 ledger에 같은 다이어트 적용 (CM3).

**Contracts**: 축약 행 꼴 `MET: #1–#N`. Status 문제 행(NOT MET·PARTIAL·UNTESTED·FAIL)만 `| # | Criterion | Implementation | Test | Status | Evidence |` 행 유지. AC3(:30)의 "모든 verdict가 증거에 묶였다"는 판정 의무로 보존하고 반환-측 접기와 정합화.

**Acceptance Criteria**:
- [ ] AC1: CM3 query 해당 파일 0건 + MET 축약 문면 실재. 평가(1등급): grep 출력.
- [ ] AC2: AC3·Hard Rule 6.4와 접기 형식이 모순 없다. 평가(2등급): reviewer 인용 판정.

**Target Files**:
- [M] `.claude/agents/pr-review-agent.md` -- Step 4 ledger·AC3

### Task 3: codex 미러 전파 (3-way merge)

**Acceptance Criteria**:
- [ ] AC1: P1 — codex 측 CM1~CM3 구 문면 0건 + `hunk-scoped`·MET 축약 anchor 실재. 평가(1등급): grep 출력.
- [ ] AC2: codex 고유 적응(`Codex Agent Boundary`) 잔존. 평가(1등급): grep ≥ 2건.

**Target Files**:
- [M] `.codex/agents/implementation-review-agent.toml` -- Task 1 미러
- [M] `.codex/agents/pr-review-agent.toml` -- Task 2 미러

### Task 4: 변형형 전수 census 검증 (read-only)

**Acceptance Criteria**:
- [ ] AC1: 구 문면 잔존 0건 — case-insensitive로 `전문 Read, 상한` · `각 AC마다 한 행` 전수 0 (`.claude`·`.codex`). 평가(1등급): grep -i 출력 0건.
- [ ] AC2: 판정 의무 문면(`증거 없는 MET 금지`) 잔존 ≥ 2건(역검증 — 다이어트가 판정 의무까지 지우지 않았음). 평가(1등급): grep 출력.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- plan-review 게이트 생략: 사용자 지시("최소한의 리뷰") — 마감 correctness 단일 dispatch 1회만 수행. 확인 완료.
- orchestrator SKILL의 "correctness AC ledger의 shard 연접" 서술: ledger 형식 중립(축약 행도 연접 가능 — 각 shard가 자기 task AC만 소유)이라 무변경으로 결정. 확인 불필요.
