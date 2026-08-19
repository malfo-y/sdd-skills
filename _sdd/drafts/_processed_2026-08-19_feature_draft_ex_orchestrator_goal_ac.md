# Feature Draft: ex-orchestrator 스킬 4종 Goal + Acceptance Criteria 복원

> 규모 판정: 적격 — 변경 요소는 "Goal+AC 섹션 규약 1건 × 스킬 4종 × 미러 2벌"(8파일) + census 검증으로, 요소↔task 대응이 눈검산된다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

agent→skill 전환(F1~F5) 때 orchestrator의 return-schema 검증과 함께 사라진 완료 계약을 복원한다. ex-orchestrator 스킬 4종(`feature-draft`·`plan-review`·`implementation`·`implementation-review`)의 SKILL.md에 `## Goal`과 `## Acceptance Criteria` 섹션을 추가한다 — 실행자가 스킬 종료 전 자체 검증할 falsifiable 완료 조건으로, 스킬 drift(단계 생략·제멋대로 마감)를 막는다. `.claude/skills/` 원본과 `plugins/sdd-skills-codex/skills/` 미러 모두에 적용한다(미러는 3-way merge — codex 적응 delta 보존, 단순 복사 금지).

**새 invariant**: 모든 SDD 파이프라인 스킬의 SKILL.md는 `## Acceptance Criteria` 섹션을 갖는다(이 4종이 마지막 결손 — `docs/SKILL_AUTHORING_NORMS.md` 체크리스트의 "AC 필수"가 이로써 전 스킬에서 성립). `## Goal` 섹션은 이번 4종에 함께 추가한다(전 스킬 필수는 아님). AC는 기존 완료 신호 섹션(Required Output·반환·마감·보고)이 소유한 상세를 재서술하지 않고 참조로 결속한다.

## Scope
- **In**: 4개 스킬 × 2벌(claude 원본 + codex 미러)의 SKILL.md에 Goal/AC 섹션 추가; 변형 표기 census 검증.
- **Out**: 다른 스킬의 Goal 섹션 보강(spec-sync 등 AC만 있는 9종 — 실드리프트 미관측), 프로세스 본문 변경, spec surface 직접 편집(spec-sync 소관), 훅·구조적 check 신설.
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: feature-draft에 Goal + AC 섹션 추가 (원본 + codex 미러)
전환 lane의 첫 스킬에 섹션 규약을 확립한다 — 이후 task가 이 규약을 참조한다.

**Contracts** — **Goal/AC 섹션 규약** (Task 2~4가 참조):
- 위치: intro 문단(H1 직후 서술) 바로 뒤, 첫 프로세스성 H2 앞에 `## Goal` → `## Acceptance Criteria` 순서.
- `## Goal`: 이 스킬이 무엇을 산출/보장하고 끝나는지 1~3문장 (exemplar: `guide-create`, `goal-init`).
- `## Acceptance Criteria`: 첫 줄에 self-check 지시 blockquote — `> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.` (exemplar: `goal-init`만 보유 — 이 규약 텍스트가 단일 소스) — 이어 `- [ ] ACn:` 체크리스트.
- AC 내용: 기존 완료 신호 섹션(Required Output·반환·마감·보고 등)의 승격이다 — 상세를 재서술하지 않고 해당 섹션을 참조로 결속하며, 각 항목은 이진 판정 가능해야 한다. 새 프로세스 단계를 발명하지 않는다.
- codex 미러: 동일 블록을 3-way merge로 반영 — codex 적응 어휘(dispatch→spawn 등)가 AC 문구에 걸리면 미러 어휘를 따르고, 그 외 delta(Codex Runtime Adapter 절 등)는 보존한다.
- 스킬별 AC가 반드시 결속할 핵심 신호: feature-draft = draft 파일 생성(Required Output 준수)·분할 판정 기록·plan-review 게이트 실행과 fix·surface 1줄.

**Acceptance Criteria**:
- [ ] AC1: 두 파일 모두 `## Goal`·`## Acceptance Criteria` heading이 규약 위치에 존재한다. 평가: `grep -n '^## \(Goal\|Acceptance Criteria\)'` 두 파일 — heading 2종이 각각 1회, `## Process` 이전 줄번호. 증거: grep 출력.
- [ ] AC2: AC 항목들이 위 "핵심 신호" 전부를 커버하고 각각 소유 섹션을 참조한다(상세 재서술 없음). 평가: 2등급 — reviewer가 AC 항목↔핵심 신호 대응과 재서술 부재를 인용으로 판정. 증거: 항목별 인용.
- [ ] AC3: 미러 파일의 기존 codex 적응 delta가 보존됐다. 평가: `git diff`에서 미러 변경이 Goal/AC 블록 추가에 한정됨을 확인. 증거: diff 출력.

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md` -- Goal/AC 섹션 추가
- [M] `plugins/sdd-skills-codex/skills/feature-draft/SKILL.md` -- 동일 블록 3-way merge

### Task 2: plan-review에 Goal + AC 섹션 추가 (원본 + codex 미러)
Task 1의 섹션 규약을 적용한다. 핵심 신호: 5-smell 전수 점검·단일 패스·채팅 반환 형식(Blocker Status+Findings)·review-only(파일 무수정)·대상 부재 시 1줄 반환.

**Acceptance Criteria**:
- [ ] AC1: Task 1 AC1과 동일 평가를 두 파일에 적용해 통과한다(규약 위치는 이 스킬의 첫 프로세스성 H2인 `## Input` 앞). 증거: grep 출력.
- [ ] AC2: Task 1 AC2와 동일 평가 — 위 핵심 신호 커버 + 재서술 부재. 증거: 항목별 인용.
- [ ] AC3: Task 1 AC3과 동일 평가 — codex delta 보존. 증거: diff 출력.

**Target Files**:
- [M] `.claude/skills/plan-review/SKILL.md` -- Goal/AC 섹션 추가
- [M] `plugins/sdd-skills-codex/skills/plan-review/SKILL.md` -- 동일 블록 3-way merge

### Task 3: implementation에 Goal + AC 섹션 추가 (원본 + codex 미러)
Task 1의 섹션 규약을 적용한다. 핵심 신호: task별 Triage→RED→GREEN→커버리지 델타 수행·ledger 생성/갱신·마감 4단계(회귀·AC→증거 테이블·품질 게이트+fix·마감 요약)·작성자 불변식(코드/테스트 위임 금지).

**Acceptance Criteria**:
- [ ] AC1: Task 1 AC1과 동일 평가(규약 위치는 `## 입력` 앞). 증거: grep 출력.
- [ ] AC2: Task 1 AC2와 동일 평가 — 위 핵심 신호 커버 + 재서술 부재. 증거: 항목별 인용.
- [ ] AC3: Task 1 AC3과 동일 평가 — codex delta 보존. 증거: diff 출력.

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- Goal/AC 섹션 추가
- [M] `plugins/sdd-skills-codex/skills/implementation/SKILL.md` -- 동일 블록 3-way merge

### Task 4: implementation-review에 Goal + AC 섹션 추가 (원본 + codex 미러)
Task 1의 섹션 규약을 적용한다. 핵심 신호: simplicity dispatch(미러: spawn) 선행 + correctness 직접 수행·AC verdict 증거 결속(증거 없는 MET 금지)·합산 보고 형식·review-only(파일 무수정).

**Acceptance Criteria**:
- [ ] AC1: Task 1 AC1과 동일 평가(규약 위치는 원본 `## 실행 순서` 앞, 미러는 `## Codex Runtime Adapter` 앞). 증거: grep 출력.
- [ ] AC2: Task 1 AC2와 동일 평가 — 위 핵심 신호 커버 + 재서술 부재, 미러는 spawn 어휘 사용. 증거: 항목별 인용.
- [ ] AC3: Task 1 AC3과 동일 평가 — codex delta(Runtime Adapter 절 등) 보존. 증거: diff 출력.

**Target Files**:
- [M] `.claude/skills/implementation-review/SKILL.md` -- Goal/AC 섹션 추가
- [M] `plugins/sdd-skills-codex/skills/implementation-review/SKILL.md` -- 동일 블록 3-way merge

### Task 5: Goal/AC 커버리지 census 검증 (read-only)
claude·codex 짝 전파 변경이므로 잔존 누락을 전수 grep으로 닫는다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/skills/{feature-draft,plan-review,implementation,implementation-review}/SKILL.md`와 `plugins/sdd-skills-codex/skills/` 동명 4종 — 총 8파일 전부에서 `^## Goal`과 `^## Acceptance Criteria`가 각 1회 검출된다. 평가: 8파일 대상 grep census, 기대 카운트 8×2. 증거: 카운트 포함 grep 출력.
- [ ] AC2: 8파일이 모두 git 추적 대상이며 이번 변경에 포함됐다(gitignore 누락 함정 점검). 평가: `git status --short` + `git ls-files` 교차. 증거: 명령 출력.

**Target Files**:
- 없음 (read-only 검증)
