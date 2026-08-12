# Feature Draft: draft/review 계약 다이어트 — Claim Manifest 폐지 · 분할 판정 축약 · Hidden Decision 잔재 제거

> 규모 판정: 적격 — 변경 요소 4개가 자산 4파일(feature-draft SKILL 짝 · plan-review-agent 짝)에만 걸리고 요소↔task 대응이 1:1로 눈검산된다. 삭제/전파류라 census형 신호 있음 → Part 2 마지막에 read-only 검증 task를 둔다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
draft/review 표면에서 **실사용상 값을 내지 못한 계약과 평가 불가능한 판정 기준, 폐기된 계약의 잔재**를 제거한다.

1. **Claim Manifest 계약 폐지 (계약 제거)**: `feature-draft`의 `# Claim Manifest` 표와 "manifest가 사실 주장의 단일 소스" 규칙, `plan-review` 실측 렌즈의 manifest 행 전수 순회 분기를 모두 제거한다. reviewer의 사실 주장 대조는 산문 발굴 단일 경로로 되돌아간다. 근거: 2026-08-12 v4.8.2 F1로 도입했으나 사용자 실사용에서 plan-review 시간 단축 효과가 관측되지 않았고, producer는 draft마다 표 작성 ceremony를, reviewer는 manifest 유무 이중 분기를 상시 부담했다 — 당일 롤백이며 재제안 금지 대상이다.
2. **분할 판정 기준 축약 (계약 축소)**: 분할 규칙에서 평가 불가능한 2번 기준("단일 컨텍스트 초과")과 리트머스 문장("머리 하나에 다 안 담기는가?")을 삭제하고, 관측 가능한 **coverage 눈검산 불가 단일 기준**으로 닫는다. 기준이 하나가 되므로 도입문 `둘 중 하나에 해당하면`도 단일 기준 문장으로 재작성한다. 분할 메커니즘(롤링 분할·planned todo 고정)과 "단일 컨텍스트 = 품질 전제"라는 *근거* 서술은 불변 — 삭제 대상은 판정 술어뿐이다.
3. **task 정의 승격 (문면 이동)**: task 정의를 Process 4단계 하위 불릿에서 `규칙` 절 최상단 항목으로 올린다. 정의 문면 자체는 불변이고 Process 4에는 반증 테스트만 남는다.
4. **Hidden Decision 잔재 제거 (계약 제거)**: `plan-review-agent` Hidden Decision smell의 첫 검사 술어(모호성·Target Files 선택·task boundary 결정에 가정·대안·확신도가 드러나는가)와 Step 2 inventory의 `decision markers(가정·대안·확신도·사용자 확인 필요)` 항목을 삭제한다. 2026-08-05 decisions/assumptions 계약 제거로 producer 템플릿에 해당 슬롯이 사라졌는데(현재 `확신도` 리터럴 0건, CM3) reviewer만 남아 producer가 생산하지 않는 표면을 요구하고 있었다. 남는 Hidden Decision 술어는 Open Questions 처리 + 남은 숨은 가정 2개다.

새 contract/invariant는 없다 — 네 항목 모두 기존 계약의 제거·축소·이동이다.

## Scope
- **In**: `.claude`/`.codex` 미러 짝의 `feature-draft/SKILL.md` 2벌, `plan-review-agent` 2벌(md/toml). 변형 리터럴 전수 census.
- **Out**: spec 표면 반영은 후속 `spec-sync` 소관 — `_sdd/spec/main.md`(L78 Hidden Decision 술어 서술 · L83 2-렌즈 manifest 분기 서술 · L86 reviewer 입력 상한 서술 · L90 §Claim Manifest 계약 · L115 `단일 컨텍스트 초과는 분할 규칙으로 해소한다`), `_sdd/spec/components.md`(`feature-draft`·`plan-review` 행), `_sdd/spec/usage-guide.md`(L50 Claim Manifest 산출물 서술 · L53 분할 판정 어휘), `decision_log`(당일 롤백을 negative result로 기록) · `changelog` 신규 entry. spec-sync 진입 시 `Claim Manifest`·`가정·대안·확신도`·`단일 컨텍스트 초과` census를 `_sdd/spec` 트리까지 건다(열거 누락 방지 — impl-review Task 1·4 M1).
- **Out**: `implementation-review-agent` 짝의 승격 트리거 ⑥ `낮은 확신도` 문면(CM9). Change Summary 4번이 문제 삼은 잔재와 **다른 부류**다 — 4번은 producer 표면의 *존재*를 전제로 그 기록 여부를 검사하는 술어라 슬롯이 없으면 항상 위반 판정을 내지만, ⑥은 "표기돼 있으면 읽기를 승격한다"는 조건부 트리거라 표기가 없으면 조용히 미발동한다.
- **Out**: 기존 `_sdd/drafts/*` 의 `규모 판정` 이력 문면과 이미 작성된 `# Claim Manifest` 섹션(이 draft 자신 포함) — append-only 기록이라 수정하지 않고, census도 `.claude`/`.codex` 자산 트리에만 건다.
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | Claim Manifest 계약 제거 | `.claude/skills/feature-draft/SKILL.md`, `.codex/skills/feature-draft/SKILL.md`, `.claude/agents/plan-review-agent.md`, `.codex/agents/plan-review-agent.toml` | `grep -rln "Claim Manifest" .claude .codex` → 정확히 이 4파일 (CM2) | Task 1 |
| P2 | 분할 판정 기준 축약 | `.claude/skills/feature-draft/SKILL.md`, `.codex/skills/feature-draft/SKILL.md` | `grep -rln "머리 하나" .claude .codex` → 이 2파일 | Task 2 |
| P3 | task 정의 승격 | `.claude/skills/feature-draft/SKILL.md`, `.codex/skills/feature-draft/SKILL.md` | `grep -rln "완료 판정이 닫히는 실행 단위" .claude .codex` → 이 2파일 (비한정 `자기 AC만으로 완료 판정이 닫히는`은 plan-review-agent 짝의 Task Boundary Drift rubric 술어까지 4파일을 매치하므로 쓰지 않는다) | Task 3 |
| P4 | Hidden Decision 잔재 제거 | `.claude/agents/plan-review-agent.md`, `.codex/agents/plan-review-agent.toml` | `grep -rln "가정·대안·확신도" .claude .codex` → 이 2파일뿐 (CM9) | Task 4 |

# Claim Manifest

| ID | Claim | Query | Expected |
|---|---|---|---|
| CM1 | `feature-draft/SKILL.md` claude·codex 미러는 byte-identical이라 동일 편집을 그대로 적용할 수 있다 | `diff .claude/skills/feature-draft/SKILL.md .codex/skills/feature-draft/SKILL.md` | 출력 없음(rc=0) |
| CM2 | `Claim Manifest` 리터럴은 자산 트리에서 4파일 10건에만 존재한다 | `grep -rn "Claim Manifest" .claude .codex` | 10건 — feature-draft SKILL 짝 각 3건(허용 변형·템플릿 heading·규칙 불릿), plan-review-agent 짝 각 2건(Step 2 inventory·Step 3 사실 주장 대조) |
| CM3 | `feature-draft` producer 템플릿에는 가정·대안·확신도 슬롯이 없다 — Hidden Decision 첫 술어에 대응하는 producer 표면이 실재하지 않는다 | `grep -c "확신도" .claude/skills/feature-draft/SKILL.md` | `0` |
| CM4 | `plan-review` wrapper SKILL 2벌은 thin entrypoint라 rubric·Claim Manifest 문면을 보유하지 않는다(편집 대상 아님) | `grep -n "Hidden Decision\|Claim Manifest" .claude/skills/plan-review/SKILL.md .codex/skills/plan-review/SKILL.md` | 매치 없음(rc=1) |
| CM5 | 사용자 문서(`docs/`)에는 이번 삭제 대상 문면이 없다 | `grep -rn "Claim Manifest\|머리 하나\|단일 컨텍스트" docs` | 매치 없음(0건) |
| CM6 | `plan-review-agent` md/toml 짝은 편집 대상 3개 문면(rubric Hidden Decision 행·Step 2 inventory·Step 3 사실 주장 대조)이 동일하다 | `grep -n "Hidden Decision\|decision markers\|사실 주장 대조" .claude/agents/plan-review-agent.md .codex/agents/plan-review-agent.toml` | 두 파일에서 같은 3개 문면이 각각 1건씩 |
| CM7 | 템플릿 마커 쌍 검사에 쓸 앵커는 start/end 한정 2건이다(비한정 `spec-update-todo-input` 은 규칙 불릿 `마커 보존` 때문에 3건) | `grep -cE "spec-update-todo-input-(start\|end)" .claude/skills/feature-draft/SKILL.md` | `2` |
| CM8 | `둘 중 하나` 리터럴은 feature-draft 짝 밖에서도 정상 사용 중이므로 census를 트리 전역으로 걸 수 없다 | `grep -rn "둘 중 하나" .claude .codex` | 7건 — feature-draft 짝 2건(삭제 대상) + discussion reference 2건·codex implementation-review/pr-review/plan-review SKILL 각 1건(무관) |
| CM9 | `가정·대안·확신도` 리터럴은 plan-review-agent 짝에만 있고 implementation-review-agent 짝은 `낮은 확신도`만 갖는다 | `grep -rnE "가정·대안·확신도\|낮은 확신도" .claude .codex` | 6건 — plan-review 짝 각 2건(`가정·대안·확신도`), implementation-review 짝 각 1건(`낮은 확신도`) |
| CM10 | 대소문자 무시 census 패턴의 추가 매치는 템플릿 예시 행뿐이라 Task 1 삭제로 함께 사라진다 | `grep -rniE "claim[ _-]?manifest\|CM<n>\|CM[0-9]+" .claude .codex` | 12건 — CM2의 10건 + feature-draft 짝 template `\| CM1 \| ... \|` 행 2건 |
| CM11 | `plan-review-agent` 짝의 `Open Questions` 리터럴 baseline은 파일당 2건이다(Step 2 inventory · rubric Hidden Decision 행) | `grep -c "Open Questions" .claude/agents/plan-review-agent.md .codex/agents/plan-review-agent.toml` | 각 `2` |

# Part 2: Tasks

### Task 1: Claim Manifest 계약을 producer·reviewer 양쪽에서 제거

producer 표면(템플릿 섹션·규칙 불릿·허용 변형 문구)과 reviewer 분기(Step 2 inventory 항목·Step 3 manifest 전수 순회)를 함께 제거해 계약을 소멸시킨다. reviewer의 사실 주장 대조는 manifest 이전의 산문 발굴 단일 경로로 되돌린다(CM2).

**Acceptance Criteria**:
- [ ] AC1 (1등급): `grep -rnE "Claim Manifest|CM<n>" .claude .codex` 출력이 0건이다.
- [ ] AC2 (1등급): 템플릿 구조가 manifest heading만 잃고 보존된다 — `grep -n "^# " .claude/skills/feature-draft/SKILL.md` 출력이 `# Feature Draft` / `# Feature Draft: [title]` / `# Part 1: Spec Delta` / `# Propagation Surfaces` / `# Part 2: Tasks` / `# Open Questions` 6줄이고(codex 미러 동일), `grep -c "마커 보존"` 이 각 `1`이다(인접 규칙 불릿 보존).
- [ ] AC3 (1등급): `plan-review-agent` 짝의 Step 3 `사실 주장 대조` 불릿이 manifest·legacy 분기 없는 단일 문장으로 남는다 — `grep -nE "legacy|전수 순회|표본 아님" .claude/agents/plan-review-agent.md .codex/agents/plan-review-agent.toml` 이 0건이고 `grep -c "사실 주장 대조"` 는 각 `1`이다.
- [ ] AC4 (1등급): 템플릿 마커 쌍이 보존된다 — `grep -cE "spec-update-todo-input-(start|end)"` 가 두 SKILL 모두 `2`다 (CM7).

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md` -- 템플릿 섹션·규칙 불릿·허용 변형 문구 제거
- [M] `.codex/skills/feature-draft/SKILL.md` -- 미러 동일 편집(CM1: byte-identical)
- [M] `.claude/agents/plan-review-agent.md` -- Step 2 inventory 항목·Step 3 manifest 분기 제거
- [M] `.codex/agents/plan-review-agent.toml` -- 미러 동일 편집(CM6)

### Task 2: 분할 규칙을 관측 가능한 단일 기준으로 축약

평가 불가능한 판정 술어를 지우고 눈검산 기준 하나만 남긴다. 분할 메커니즘과 근거 서술은 건드리지 않는다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `grep -nE "머리 하나|단일 컨텍스트 초과|둘 중 하나" .claude/skills/feature-draft/SKILL.md .codex/skills/feature-draft/SKILL.md` 출력이 0건이다 — 도입문까지 단일 기준 문장으로 재작성됐음을 함께 닫는다(CM8: 이 패턴은 파일 앵커가 필수).
- [ ] AC2 (2등급 · rubric): 분할 규칙 절이 번호 목록 2개가 아닌 **coverage 눈검산 불가 단일 기준** 서술로 남고, 새 contract/invariant 문장의 load-bearing 내용 2가지(새 계약이 생기는 것 자체는 분할 사유가 아니다 + 해당 task의 `Contracts`에 적는다)와 롤링 분할·census 문단·`> 규모 판정:` 1줄 기록 규칙이 보존됐다. reviewer가 절 전문을 인용해 판정한다. — *fix 1에서 계약 오류 선언 후 갱신: 기준이 하나로 축약된 뒤 원문의 `소수이고 눈검산 가능하면 적격` 앞절은 상위 규칙의 재진술이라 원문 보존 요구를 load-bearing 내용 보존으로 대체했다(simplicity 참조 렌즈 M1).*
- [ ] AC3 (1등급): 스킬 소개 문장과 frontmatter description이 편집 후에도 그대로 실재한다(판정 술어가 아니라 트리거·근거 문면이라 존치) — 두 SKILL 각각에서 `grep -c "단일 컨텍스트로 감당되는 변경의 기본 경로"` 가 `1`, `grep -c "fits in a single context"` 가 `1`이다.

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md` -- 분할 규칙 절 축약
- [M] `.codex/skills/feature-draft/SKILL.md` -- 미러 동일 편집

### Task 3: task 정의를 `규칙` 절 최상단으로 승격

정의가 Process 4 하위 불릿에 파묻혀 읽히지 않는 문제를 위치 이동으로 해소한다. 정의 문면은 그대로 옮기고 새 기준을 더하지 않는다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `규칙` 절 첫 항목이 `- **task의 정의**`로 시작하고 기존 정의 문장(`단일 의도를 가지고 자기 AC만으로 완료 판정이 닫히는 실행 단위`)을 문면 그대로 담는다 — `grep -n "task의 정의" .claude/skills/feature-draft/SKILL.md .codex/skills/feature-draft/SKILL.md` 각 1건.
- [ ] AC2 (1등급): Process 절에 정의 문장이 중복되지 않고 반증 테스트만 남는다 — `sed -n '/^## Process/,/^## Required Output/p' <각 SKILL>` 출력에서 `실행 단위다` 0건, `의도가 두 문장이면 두 task` 1건.
- [ ] AC3 (1등급): fenced template 블록 안에는 정의 산문이 추가되지 않는다(템플릿은 산출물 구조 단일 소스이므로 producer가 draft에 복사할 문면이 늘지 않아야 한다) — `sed -n '/^```markdown$/,/^```$/p' <각 SKILL>` 출력에서 `task의 정의` 0건.

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md` -- 정의 승격 + Process 4 축약
- [M] `.codex/skills/feature-draft/SKILL.md` -- 미러 동일 편집

### Task 4: Hidden Decision smell에서 폐기 계약 잔재 제거

producer가 생산하지 않는 표면(가정·대안·확신도)을 요구하는 검사 술어와 그 inventory 항목을 지운다(CM3).

**Acceptance Criteria**:
- [ ] AC1 (1등급): `grep -n "가정·대안·확신도" .claude/agents/plan-review-agent.md .codex/agents/plan-review-agent.toml` 출력이 0건이다.
- [ ] AC2 (1등급): Hidden Decision rubric 행이 `<br>`로 이어진 술어 **2개**(Open Questions 처리 / 남은 숨은 가정)만 보유한다 — `grep -F "| Hidden Decision |" <각 파일> | grep -o "<br>" | wc -l` 이 두 파일 모두 `1`이고(`^|` 앵커는 이 환경의 regex 엔진에서 alternation으로 해석되므로 `-F` 고정 문자열을 쓴다), 남는 두 술어 리터럴 `확인 필요 항목이 구현 전 확인 대상으로 드러나는가` · `남은 숨은 가정이 있는가` 가 각 `1`건, 행 끝 `Verifiability, Scope Discipline` 이 보존된다.
- [ ] AC3 (1등급): 다른 4 smell 행이 문면 그대로 실재해 rubric이 5행을 유지한다 — `grep -cE "^\| (Requirement Fit\|Task Boundary Drift\|Over-engineering\|Verification Weakness) \|"` 가 두 파일 모두 `4`다.
- [ ] AC4 (1등급): Step 2 inventory에서 `decision markers(...)` 항목만 제거되고 `Open Questions` 는 남는다 — `grep -c "decision markers"` 가 각 `0`, `grep -c "Open Questions"` 가 각 `2`로 baseline 유지(CM11).

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- rubric Hidden Decision 술어 1개 삭제 + Step 2 inventory 정리
- [M] `.codex/agents/plan-review-agent.toml` -- 미러 동일 편집(CM6)

### Task 5: 변형 리터럴 전수 census (read-only 검증)

삭제·전파류 변경이라 변형 표기 잔존이 재발한다. claude·codex 짝을 함께 훑어 잔존 0을 증명한다. 무관한 정상 사용처가 있는 패턴은 파일 앵커로 건다(CM8).

**Acceptance Criteria**:
- [ ] AC1 (1등급): `grep -rniE "claim[ _-]?manifest|CM<n>|CM[0-9]+" .claude .codex` 출력이 0건이다 (baseline 12건 → 0, CM10).
- [ ] AC2 (1등급): `grep -rnE "머리 하나|단일 컨텍스트 초과|리트머스" .claude .codex` 출력이 0건이고, 파일 앵커 패턴 `grep -nE "둘 중 하나" .claude/skills/feature-draft/SKILL.md .codex/skills/feature-draft/SKILL.md` 도 0건이다(트리 전역 `둘 중 하나` 5건은 무관 사용처라 잔존이 정상, CM8).
- [ ] AC3 (1등급): 변형 표기까지 포함해 잔존이 없다 — `grep -rniE "가정.?대안|확신도" .claude .codex` 출력이 `implementation-review-agent` 짝의 승격 트리거 ⑥ `낮은 확신도` 2건뿐이다(Scope Out, CM9). Task 4 AC1이 정확 리터럴만 보는 것과 달리 이 AC는 구분자·대소문자 변형을 덮는다.
- [ ] AC4 (1등급): claude·codex 미러 정합 — `diff .claude/skills/feature-draft/SKILL.md .codex/skills/feature-draft/SKILL.md` 가 출력 없음이고, `plan-review-agent` 짝은 편집한 3개 문면(rubric Hidden Decision 행 · Step 2 inventory · Step 3 사실 주장 대조)이 두 파일에서 동일하다(CM6 재실행).
- [ ] AC5 (1등급): `git diff --check` 출력이 없다(공백 오류 없음).

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- **요청 ①의 삭제 범위(첫 술어 전체 vs marker 열거만)**: 첫 술어 문장을 **통째로** 삭제하기로 결정했다 — 검사 대상 범위(`모호성·Target Files 선택·task boundary 결정`)와 그 술어의 `사용자 확인 필요 여부`까지 함께 사라진다. 근거: 사용자 코멘트가 지목한 단위가 문장 전체("이 문장이 필요한가?")이고, 사라지는 검사 대상은 Target Files=`Verification Weakness`(실측)·`Over-engineering`(`[C]` 정당화), task boundary=`Task Boundary Drift`가 이미 소유하며, 확인 필요 여부는 남는 술어 1(`Open Questions` 항목별 결정·확인 필요 여부)이 그대로 검사한다. marker 열거만 지우는 대안은 근거 없는 검사 대상(가정 슬롯 없는 producer)에 대한 술어를 남긴다. 사용자 확인 불필요.
- **요청 ⑤("task 정의를 좀 더 명확히 드러나게")의 해석**: 위치 승격만 수행하고 정의 문장 자체의 rewrite는 제외하기로 결정했다. 근거: 현 문면("단일 의도 + 자기 AC만으로 완료 판정이 닫히는 실행 단위")은 이미 이진 판정으로 닫히므로 불명확의 원인은 내용이 아니라 Process 하위 불릿이라는 위치이고, 문면을 손대면 `plan-review` Task Boundary Drift 술어와의 정합까지 함께 흔들린다. 사용자 확인 불필요(더 강한 rewrite를 원하면 후속 1줄 요청으로 닫힌다).
- **분할 판정 축약 후 "단일 컨텍스트" 어휘의 잔존 범위**: 판정 술어에서만 제거하고 스킬 소개문·frontmatter description·spec의 근거 서술("단일 컨텍스트 = 품질 전제")은 유지하기로 결정했다. 근거: 사용자 코멘트가 지목한 것은 "평가"이며, 근거 문면까지 지우면 분할 메커니즘의 존재 이유가 사라진다. 사용자 확인 불필요.
- **spec 표면 처리 시점**: Scope Out에 열거한 spec 4파일은 이 draft의 Target Files에 넣지 않고 `spec-sync` 단계에서 처리한다. 근거: 이 repo 체인에서 spec 반영은 spec-sync 단일 진입점이 소유한다. 사용자 확인 불필요.
