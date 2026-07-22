# Feature Draft (Lite): `-lite` 개명 — 이름+개념 전부 (F5)

> Lite 적격: 적격 — rename census 대상이 41파일/약 250건으로 실측 열거됐고 치환 매핑이 1:1 눈검산 가능, 단일 세션 규모. rename 자체가 census형이므로 마지막 검증 task(Task 4)가 변형형(-lite/_lite_/Lite/라이트) 전수 census다. (분할 계획 원본: `_sdd/drafts/2026-07-22_feature_draft_lite_full_lane_removal.md`의 F5 — 사용자 확정: 이름+개념 전부)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
full 레인이 사라져 무의미해진 `-lite` 구분자를 이름과 개념 어휘에서 전부 제거한다 (사용자 확정). 스킬 `feature-draft-lite`→`feature-draft`, `implementation-lite`→`implementation`으로 개명하고, 개념 어휘("lite 체인"→"SDD 체인", "lite draft"→"draft" 등)와 마커·라벨(`> Lite 적격:`→`> 규모 판정:`, autopilot Step L→Step 2·AC-L→AC)을 교체한다. F2에서 full 동명 스킬이 삭제돼 이름 충돌 없음.

- **호환 계약**: draft 파일명 glob은 `*_feature_draft_*`로 통일 — 기존 `*_feature_draft_lite_*` 파일명을 substring으로 계속 매칭한다(기록물 호환). 새 draft 파일명은 `<YYYY-MM-DD>_feature_draft_<slug>.md`.
- lite 계열 트리거 별칭("라이트 구현", "lite draft" 등)도 제거한다 — 어휘 전부 제거가 사용자 확정 범위.
- `_sdd/spec/`의 lite 어휘 트림은 이 feature의 post-implementation spec-sync가 수행한다 (직접 수정 금지 불변식).

## Scope
- **In**: 스킬 2종 개명(디렉토리·name 필드·marketplace), live 표면 41파일의 호출 참조·개념 어휘 치환, `docs/SDD_SPEC_DEFINITION.md` ko·en 현행(draft = Part 1 마커 + Part 2 Tasks) 정합, 개명 census
- **Out**: 기록물(`_sdd/drafts/`·`_sdd/work_log/` 등)의 과거 파일명·어휘, git 히스토리, 체인 동작 변경
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: 스킬 2종 개명 — 디렉토리·name 필드·등록
`git mv`로 4개 디렉토리를 옮기고 name 필드·marketplace 경로를 갱신한다. 개명은 major 변경 — 두 스킬 버전 2.0.0.

**Acceptance Criteria**:
- [ ] AC1: `.claude/.codex`에 `skills/feature-draft`·`skills/implementation` 디렉토리가 존재하고 `-lite` 디렉토리는 부재한다.
- [ ] AC2: SKILL frontmatter `name:`·skill.json `name`이 새 이름이고 버전 2.0.0 동기, marketplace.json 경로가 새 이름이며 JSON 유효.

**Target Files**:
- [M] `.claude/skills/feature-draft-lite/` → `feature-draft/` (git mv, SKILL.md·skill.json)
- [M] `.claude/skills/implementation-lite/` → `implementation/` (동일)
- [M] `.codex/skills/feature-draft-lite/` → `feature-draft/` / [M] `.codex/skills/implementation-lite/` → `implementation/`
- [M] `.claude-plugin/marketplace.json`

### Task 2: 호출 참조·개념 어휘 전면 치환 (41파일)
recon 매핑대로 치환한다: `sdd-skills:feature-draft-lite`→`sdd-skills:feature-draft`, `feature-draft-lite`→`feature-draft`, `implementation-lite`→`implementation`, "lite feature draft"/"lite draft"→"feature draft"/"draft", "SDD lite 체인"→"SDD 체인"(최장일치 우선 — 이중어 방지, plan-review L1), "lite 체인"→"SDD 체인"(고유명 문맥) 또는 "체인"(문중), "Lite 체인"(autopilot Step L 제목)→"체인", Step L→**Step 2**(0→1→2 연속화), AC-L1~L6→AC1~AC6, `> Lite 적격:`→`> 규모 판정:`(값 "적격"/"분할 필요 — 분할 계획 포함"), plan-review "Lite 적격 검사"→"규모 판정 검사", draft 템플릿 제목 `# Feature Draft (Lite):`→`# Feature Draft:`, glob `*_feature_draft_lite_*`→`*_feature_draft_*`, lite 트리거 별칭 제거("라이트 구현"·"lite implementation" 등), "Lite fast-path"·"lite fast-path" 잔존 서술→"fast-path" 또는 문맥 재서술.

**Acceptance Criteria**:
- [ ] AC1: 치환 후 각 파일이 문맥 정합하다 — 특히 autopilot 쌍(Step 2 renumber·AC 라벨), plan-review-agent 쌍(검사명·마커·Input glob), 두 개명 스킬 본문(자기 지칭·상호 참조).
- [ ] AC2: 미러 정합 — 개명 스킬 2쌍은 identical copy, agent 쌍·autopilot 쌍은 기존 적응 delta만.

**Target Files**: Task 4 census와 동일 패턴 집합의 grep으로 재도출한 실측 41파일 — 범위 `.claude/`·`.codex/`·`.claude-plugin/`·`docs/`·`README.md`·`AGENTS.md` (기록물 `_sdd/`·`.sdd-workbench/` 제외; 도출 명령이 목록의 단일 소스 — plan-review M1)

### Task 3: SDD_SPEC_DEFINITION ko·en 현행 정합
temporary spec 서술을 현행 draft 형식(Part 1 `spec-update-todo-input` 마커 + Part 2 Tasks: 의도·Contracts·falsifiable AC·Target Files)으로 갱신한다. 검증 rubric 사슬(목표→AC falsifiable→평가방법 2등급→증거)은 유지하되, full 시대 구조(V* 매핑·coverage index·Touchpoints·7섹션) 서술은 legacy 기록물 형식으로 한정하거나 제거한다.

**Acceptance Criteria**:
- [ ] AC1: ko·en 문서의 temporary spec 정의가 현행 draft 형식과 일치한다 (마커·Part 2 Tasks·AC falsifiability).
- [ ] AC2: full 구조 어휘(V*·coverage index·Touchpoints·canonical 7섹션)가 무한정 서술로 잔존하지 않는다 (legacy 한정 표기는 허용).

**Target Files**:
- [M] `docs/SDD_SPEC_DEFINITION.md` / [M] `docs/en/SDD_SPEC_DEFINITION.md`

### Task 4: 잔존 검증 (read-only) — 개명 census
Task 1~3 완료 후. python lookahead, 변형형 포함 (F4 교훈: 소문자·탈락형 기본 포함).

**Acceptance Criteria**:
- [ ] AC1: live 표면(`.claude/`·`.codex/`·`.claude-plugin/`·`docs/`·`README.md`·`AGENTS.md`)에서 "feature-draft-lite|implementation-lite|_feature_draft_lite_|lite 체인|lite draft|Lite 적격|Step L|AC-L" 잔존 0, 단독 출현 `\blite\b`는 **case-insensitive**(Lite 포함) 개별 판정으로 lite 개념 지칭 0, "라이트"는 개별 판정("리라이트·하이라이트" 등 합성어 제외 — plan-review M2 오탐 실측 반영). 허용 예외: ① 기록물(`_sdd/drafts/`·`_sdd/work_log/`·`_sdd/discussion/`·`_sdd/implementation/`·`.sdd-workbench/`) ② `_sdd/spec/`(이 feature의 spec-sync가 트림 — census는 sync 후 spec 3파일 재확인으로 보완).
- [ ] AC2: grep 명령·결과가 마감 증거 테이블에 남았다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- 마커 새 이름 `> 규모 판정:` — "Lite 적격"의 의미(단일 draft 적합/분할 필요 판정)를 lite 없이 표현. 소비자 3곳(fdl 템플릿·plan-review 검사·autopilot AC1) 동시 교체로 호환 문제 없음. 확인 불요로 판단.
- lite 트리거 별칭 제거 — 사용자 확정("이름+개념 전부")의 자연 귀결로 판단. 기존 습관 사용자는 "구현해줘"류 일반 트리거로 커버. 확인 불요.
- autopilot Step L→Step 2 renumber — 외부 소비자 없음(F1에서 Step 번호 참조 정리됨). 확인 불요.
