# Feature Draft: 리뷰 읽기 다이어트 1 — 주장 manifest

> 규모 판정: 분할 필요 — 분할 계획 포함 (리뷰 속도 개선 3종이 서로소 파일군 2개에 걸침 — feature 2개로 분할, 이 draft는 Feature 1 task만. 각 feature 단독은 눈검산 가능한 소수 파일 변경)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

리뷰 벽시계는 pole 작성자의 "읽고 확인할 양"이 결정한다(병렬화는 완결). 품질 선별 타협 3종을 feature 2개로 나눠 적용한다. 기각된 대안: reviewer model 강등(과거 실측 효과 없음), 표본 검증(확인 항목 누락 방식 거부), 존재 확인 스크립트화(위장 PASS 위험).

**분할 계획 (롤링)**:

- **Feature 1 (이 draft) — 주장 manifest**: feature-draft producer가 repo 대조가 필요한 사실 주장을 기계 가독 manifest 한 곳에 모으고 산문 재서술을 금지한다. plan-review 실측 렌즈는 산문 전체에서 주장을 발굴하는 대신 manifest 행을 순회 대조한다. scope: `feature-draft` SKILL(claude·codex) + `plan-review-agent`(claude·codex).
- **Feature 2 — 위험 적응형 읽기 + ledger MET 접기**: implementation-review-agent Step 3 ①을 "diff hunk+주변 문맥 기본, 승격 트리거(실행 semantics 파일·제어 흐름/상태/에러 경로 접촉·행동 AC·고밀도 변경·결함 의심 발견·draft 위험 표기) 시 파일 전문" 계단으로 개편하고 미승격 파일은 `hunk-scoped` 표기. + Verification ledger를 "NOT MET/UNTESTED만 증거 블록, MET은 축약 한 줄"로 다이어트 — implementation-review-agent와 pr-review-agent(AC 검증 ledger 동일 구조) 양쪽. scope: 두 agent(claude·codex).

**새 contract — Claim Manifest 계약** (Feature 1): draft의 repo 대조 필요 사실 주장(AC content anchor 실재, 기존 로직·중복 실재 등 사실 전제)은 `# Claim Manifest` 표가 단일 소스다. AC 평가방법·산문은 `CM<n>` ID로 참조하고 재서술하지 않는다. Target Files·Propagation `Discovery evidence`는 기존 구조가 계속 소유한다(manifest에 중복 수록 금지). plan-review 실측 렌즈의 repo 대조는 manifest 행 전수 순회를 기준으로 하며(표본 아님), manifest 없는 legacy draft는 현행 산문 발굴 방식으로 fallback한다.

## Scope

- **In** (Feature 1): `feature-draft` template·규칙에 Claim Manifest 계약 추가, `plan-review-agent` 실측 렌즈 대조 기준을 manifest 순회로 개편, codex 미러 2종 전파(3-way merge).
- **Out**: Feature 2 전체(별도 draft), implementation-review·pr-review 변경, 판단 렌즈·6-smell rubric·severity 변경, spec-sync 소비 계약 변경, 속도 실측(플러그인 캐시 지연으로 같은 세션 계측 불가 — 구조 AC만).
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | Claim Manifest 계약(template 섹션+단일 소스 규칙)의 codex 미러 반영 | `.codex/skills/feature-draft/SKILL.md` | `grep -l "Claim Manifest" .claude/skills/feature-draft/SKILL.md .codex/skills/feature-draft/SKILL.md` → 2 files (현재 0) | Task 3 |
| P2 | 실측 렌즈 manifest 대조 기준의 codex 미러 반영 | `.codex/agents/plan-review-agent.toml` | `grep -l "Claim Manifest" .claude/agents/plan-review-agent.md .codex/agents/plan-review-agent.toml` → 2 files (현재 0) | Task 3 |

(claude 측 원 변경은 Task 1·2의 Target Files가 소유한다 — 이 표는 미러 전파 표면만 담고, Discovery evidence는 짝 전체의 동기화를 검증한다.)

# Part 2: Tasks

### Task 1: feature-draft SKILL.md에 Claim Manifest 계약 추가

리뷰가 읽는 양은 draft가 주장하는 양에 비례한다 — 대조 필요 주장을 표 하나로 모아 실측 렌즈의 발굴 작업을 제거한다.

**Contracts**: Claim Manifest 계약은 Part 1 서술이 canonical — 여기는 추가분만 적는다: `# Claim Manifest` 섹션 위치는 `# Propagation Surfaces` 뒤·`# Part 2` 앞, 표 헤더 `| ID | Claim | Query | Expected |`, 행 ID `CM<n>`, 대조 필요 주장이 없으면 `없음 (대조 필요 주장 없음)` 1줄로 대체.

**Acceptance Criteria**:
- [ ] AC1: template에 `# Claim Manifest` 섹션과 표 헤더 `| ID | Claim | Query | Expected |`가 존재하고 위치가 Propagation Surfaces와 Part 2 사이다. 평가(1등급): `grep -n "Claim Manifest\|# Part 2: Tasks\|# Propagation Surfaces" .claude/skills/feature-draft/SKILL.md` 출력의 행 번호 순서로 판정.
- [ ] AC2: 규칙 절에 단일 소스 규칙 4요소(주장은 manifest 소유 · `CM<n>` ID 참조 · 재서술 금지 · Target Files/Discovery evidence 중복 수록 금지)가 존재한다. 평가(2등급): reviewer가 규칙 절을 인용해 4요소 각각의 실재를 이진 판정.
- [ ] AC3: `spec-update-todo-input` 마커 쌍이 보존됐다. 평가(1등급): `grep -c "spec-update-todo-input-start"`와 `grep -c "spec-update-todo-input-end"`가 각각 변경 전과 동일(각 1).

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md` -- template에 Claim Manifest 섹션, 규칙 절에 단일 소스 규칙 추가

### Task 2: plan-review-agent 실측 렌즈를 manifest 순회 대조로 개편

실측 렌즈의 비용은 산문에서 주장을 발굴해 하나씩 repo 대조하는 데 있다 — 대조 대상 열거를 producer가 끝냈으므로 렌즈는 행 순회만 한다.

**Contracts**: 실측 렌즈 대조 기준 — (1) manifest 있는 draft: Target Files·Required surfaces의 Glob 실재 확인은 현행 유지, content anchor·사실 전제 대조는 manifest 행 전수 순회(각 행 Query 재실행 → Expected 대조)로 수행한다. 산문에서 새 대조 대상을 발굴하지 않는다. (2) 산문에 `CM<n>` 참조 없는 repo-사실 주장이 보이면 repo 대조 없이 producer 계약 위반으로 `Verification Weakness`에 귀속한다(주장 누락 탐지 구멍 봉합 — draft 문면 검사만, 비용 저렴). (3) manifest 없는 draft: 현행 산문 발굴 방식 fallback. (4) Step 2 Inventory 추출 목록에 Claim Manifest를 포함한다 — 순회 대상 파악은 Step 2, 대조 실행은 Step 3. 렌즈의 출력 계약·smell 소유·"출력이 아니라 대조 범위" 원칙은 불변.

**Acceptance Criteria**:
- [ ] AC1: `호출자 렌즈 한정` 절의 실측 렌즈 정의에 manifest 순회 대조 기준과 legacy fallback이 명시됐다. 평가(1등급): `grep -n "Claim Manifest" .claude/agents/plan-review-agent.md` ≥ 1 hit이 해당 절 범위에 있고, fallback 문구가 함께 있다.
- [ ] AC2: Step 3 계단에 manifest 행 순회(Query 재실행·Expected 대조)가 들어가고, CM 참조 없는 산문 주장의 `Verification Weakness` 귀속 규칙이 존재한다. 평가(2등급): reviewer가 Step 3 절을 인용해 세 요소(순회·fallback·귀속) 실재를 판정.
- [ ] AC3: 판단 렌즈 정의·5-smell rubric 표·severity 표는 변경되지 않았다. 평가(1등급): `git diff`에서 해당 절의 행이 `+`/`-` 변경 라인으로 나타나지 않음을 확인(인접 절 수정에 따른 문맥 행 포함은 무방).

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- 실측 렌즈 정의(호출자 렌즈 한정 절)와 Step 3 계단 개편

### Task 3: codex 미러 전파 (3-way merge)

claude 측 변경을 codex 적응 delta(Codex Agent Boundary 절, spawn_agent 어휘 등)를 보존하며 미러에 재적용한다 — 단순 복사 금지.

**Acceptance Criteria**:
- [ ] AC1: P1·P2 Discovery evidence query가 기대 surface 집합(각 2 files)을 반환한다. 평가(1등급): 두 grep 실행 출력.
- [ ] AC2: codex 고유 적응이 보존됐다 — `.codex/agents/plan-review-agent.toml`에 `Codex Agent Boundary` 절과 `spawn_agent` 어휘가 잔존. 평가(1등급): `grep -n "Codex Agent Boundary\|spawn_agent" .codex/agents/plan-review-agent.toml` ≥ 2 hits.
- [ ] AC3: codex 측 본문이 claude 측과 동등 내용(Claim Manifest 섹션·단일 소스 규칙·실측 렌즈 순회·fallback)을 담는다. 평가(2등급): reviewer가 4개 anchor의 codex 파일 내 실재를 인용해 판정.

**Target Files**:
- [M] `.codex/skills/feature-draft/SKILL.md` -- Task 1 변경의 미러 재적용
- [M] `.codex/agents/plan-review-agent.toml` -- Task 2 변경의 미러 재적용

# Open Questions

- pr-review-agent ledger 포함 여부: **Feature 2에 포함으로 결정** (`pr-review-agent.md:101`에 동일 구조 ledger 실측). 사용자 확인: 채팅에서 질의·답변 완료.
- manifest 필수 여부: **조건부로 결정** — 대조 필요 주장이 없으면 `없음` 1줄. legacy fallback이 어차피 필요하므로 분기 비용 증가 없음. 확인 불필요.
- 판단 렌즈는 불변: 사실 전제를 draft 문면 기준으로 가정 판정하는 현행 규칙이 manifest와 그대로 호환(문면이 곧 manifest). 확인 불필요.
