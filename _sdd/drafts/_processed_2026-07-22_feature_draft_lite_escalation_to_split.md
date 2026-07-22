# Feature Draft (Lite): 승격→분할 의미 교체

> Lite 적격: 표면 4종 × 미러 2의 산문 규칙 교체로 대응이 1:1 눈검산 가능, 단일 세션 규모. "승격/full 전환" 변형 표기가 다층 표면(frontmatter·skill.json·docs)에 흩어진 census형 신호가 있어(plan-review H2 실측) 마지막 read-only 검증 task(Task 5)로 대응한다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
lite 레인의 이탈 신호 의미를 교체한다: "full 승격" → **"분할"**. 규모가 단일 컨텍스트를 넘는 변경은 full 파이프라인으로 올리는 대신 여러 lite feature로 쪼개고, 분할 목록을 spec-sync(planned)로 spec todo에 고정한 뒤 feature별 lite 체인을 순차 실행한다. census형 sweep은 이탈 신호에서 제외하고 "마지막 read-only 검증 task(변형 표기 전수 grep census를 AC로)" 필수라는 draft 형태 규칙으로 흡수한다.

- **새 invariant**: 규모 초과의 해소 수단은 오케스트레이션이 아니라 분할이다 — lite 표면들은 full 전환을 안내하지 않는다 (full 레인 삭제의 선행 조각; full 직행은 사용자 명시 요청만 한시 잔존).
- **새 invariant**: 분할 판정의 canonical은 lite 표면 소유(feature-draft-lite 분할 규칙 / implementation-lite 중단·분할 규칙 / plan-review Tier 2-lite 분할 권고), autopilot은 신호를 소비만 한다.

## Scope
- **In**: feature-draft-lite·implementation-lite SKILL(+identical codex 미러), plan-review-agent Tier 2-lite(claude+codex 3-way), sdd-autopilot Step L·Lane 판정(+reasoning-reference lite 문구, AUTOPILOT_GUIDE 상단 노트, codex 3-way)
- **Out**: full 레인 실체 삭제(다음 슬라이스), reviewer full tier 트림, `-lite` 접미사 개명, orchestrator-contract 수정
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: feature-draft-lite — 승격 규칙을 분할 규칙으로 교체
규칙 1·2(눈검산 불가·단일 컨텍스트 초과)는 분할 신호로, 규칙 3(census형)은 검증 task 형태 규칙으로 재정의한다. 해소 장소를 밖(full)이 아니라 안(draft 형태)으로 옮기는 것.

**Contracts**:
- 분할 draft 형태(롤링): 분할 필요 판정 시 이 draft 파일이 곧 분할 계획이다 — Part 1 마커 내부에 분할 feature 목록(각 1줄 의도+scope)을 적어 `spec-sync`(planned)가 todo로 소비하게 하고, Part 2에는 **첫 feature의 task만** 작성한다. 나머지 feature는 각자 차례에 자기 lite draft를 새로 만든다. (구현 시 실측 1건: 분할 목록이 spec에 feature별 개별 todo로 떨어지는지 spec-sync 동작 확인 — plan-review L1)
- `> Lite 적격:` 리터럴 유지(autopilot AC-L1·plan-review 식별과의 호환), 값 확장: "적격" 또는 "분할 필요 — 분할 계획 포함".
- census형 draft는 마지막 read-only 검증 task(변형 표기 kebab/underscore/공백/글롭 전수 grep census를 AC로) 필수.

**Acceptance Criteria**:
- [ ] AC1: 파일 전체(frontmatter description 포함)와 skill.json에 full 전환 안내가 없다 — "feature-draft (full)"·"feature-draft`(full" 등 변형 포괄 grep으로 확인.
- [ ] AC2: 분할 규칙이 위 Contracts 3항(롤링 형태·리터럴 유지·census 검증 task)을 모두 정의한다.
- [ ] AC3: Integration에서 `feature-draft`(full 승격)·`implementation`(full 대안) 항목이 제거됐다.
- [ ] AC4: codex 미러가 identical copy다 (`diff` 무결).

**Target Files**:
- [M] `.claude/skills/feature-draft-lite/SKILL.md` -- 승격 규칙 절·frontmatter description·리트머스 결론·실행 인계 규칙·Integration 교체
- [M] `.claude/skills/feature-draft-lite/skill.json` -- description의 full 안내 문구 제거 (plan-review H1)
- [M] `.codex/skills/feature-draft-lite/SKILL.md` -- identical copy 재동기화
- [M] `.codex/skills/feature-draft-lite/skill.json` -- 동일 문구 제거

### Task 2: implementation-lite — 승격 규칙을 중단·분할 규칙으로 교체
규칙 1(단일 세션 초과) → 완료 범위 마감 + 잔여를 분할 feature로 spec todo 고정. 규칙 2(계약 오류 선언 반복) → 구현 중단 + draft 복귀(계약 재설계, 필요시 분할) — 계약이 흔들리는 건 계획 문제라 해결 장소가 draft다.

**Acceptance Criteria**:
- [ ] AC1: 파일 전체(frontmatter description 포함)와 skill.json에 full 전환 안내가 없다 — "implementation (full)" 변형 포괄 grep으로 확인.
- [ ] AC2: 규칙 2의 대응이 "draft 복귀"로 정의되고, 작성자 불변식의 "승격 규칙을 따른다" 문장이 분할 규칙과 정합이다.
- [ ] AC3: Integration에서 `implementation`(full 승격 대상) 항목이 제거됐다.
- [ ] AC4: codex 미러가 identical copy다.

**Target Files**:
- [M] `.claude/skills/implementation-lite/SKILL.md` -- 승격 규칙 절·frontmatter description·작성자 불변식 문장·Integration 교체
- [M] `.claude/skills/implementation-lite/skill.json` -- description의 full 안내 문구 제거 (plan-review H1)
- [M] `.codex/skills/implementation-lite/SKILL.md` -- identical copy 재동기화
- [M] `.codex/skills/implementation-lite/skill.json` -- 동일 문구 제거

### Task 3: plan-review-agent Tier 2-lite — 승격 권고를 분할 권고로 교체
Lite 적격 검사의 위반 대응을 재정의한다: 눈검산 불가·단일 컨텍스트 초과 신호 강행 → High + **분할 권고**(full 승격 권고 아님). census 신호인데 검증 task 부재 → High + 검증 task 추가 권고. canonical 소유는 lite SKILL 유지.

**Acceptance Criteria**:
- [ ] AC1: Tier 2-lite 절에 "full `feature-draft` 승격 권고" 문구가 없고 분할 권고·검증 task 권고로 대체됐다.
- [ ] AC2: codex TOML 동일 지점이 3-way 적용됐다 (해당 절 parity, 잔여 diff는 기존 적응 delta뿐).

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- Tier 2-lite Lite 적격 검사 문구
- [M] `.codex/agents/plan-review-agent.toml` -- 동일 지점 3-way

### Task 4: sdd-autopilot — Step L 승격 전환을 분할 규칙으로 교체 + Lane 판정 축소
Step L 체인·규칙의 승격 전환 3곳(draft 판정·plan-review 권고·implementation-lite 트리거)을 분할 대응으로 교체하고, Lane 판정에서 규모 기반 full 직행을 제거한다(큰 규모는 draft 분할 판정이 처리; full 직행은 사용자 명시 요청만 한시 잔존 — 삭제 슬라이스까지).

**Acceptance Criteria**:
- [ ] AC1: SKILL.md 전역(파이프라인 다이어그램의 `승격 → Full 레인` 분기·Step L 별표 주석·Step 1 "승격일 때만" 노트·Hard Rules 레인 스코프 노트 포함)에서 lite→full 승격 서술이 없다 — 사용자 명시 요청 full 직행 서술만 예외 (plan-review M1).
- [ ] AC2: Step L에 분할 규칙(spec-sync planned todo 고정 + 첫 feature부터 순차 lite 체인)이 있고, Lane 판정의 full 직행 조건이 "사용자 명시 요청"만 남았다.
- [ ] AC3: reasoning-reference의 lite 그래프 bullet과 AUTOPILOT_GUIDE 상단 노트가 분할 의미와 정합이다 (full 전환 서술 제거).
- [ ] AC4: codex 미러 동일 지점 3-way 적용, parity 확인.

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md` -- Lane 판정·Step L 규칙·다이어그램·Step 1 노트·레인 스코프 노트
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- lite bullet 승격→분할
- [M] `docs/AUTOPILOT_GUIDE.md` -- 상단 노트 1문장 정합
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- 동일 지점 3-way
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- 동일 지점 3-way

### Task 5: 잔존 검증 (read-only) — 승격 어휘 grep census
이 draft가 도입하는 "census형 draft는 검증 task 필수" 규칙의 자기 적용 (plan-review H2). Task 1~4 완료 후 실행한다.

**Acceptance Criteria**:
- [ ] AC1: lite 표면(스킬 SKILL.md·skill.json)·plan-review agent 쌍·autopilot 쌍·docs/AUTOPILOT_GUIDE에서 변형 표기 전수 grep("승격", "full 전환", "full 레인", "(full) instead", "feature-draft (full)", "implementation (full)") 잔존 0이다. 허용 예외: ① 사용자 명시 요청 full 직행 서술(autopilot, 삭제 슬라이스까지 한시), ② "sweep 검증을 마지막 task로 승격"이라는 다른 의미(SDD_SPEC_DEFINITION·feature-draft-agent — 스코프 밖), ③ 기록물(`_sdd/work_log/`·`_sdd/drafts/`·discussion), ④ full 레인 자체 표면(feature-draft·implementation SKILL 등 — 다음 슬라이스 삭제 대상).
- [ ] AC2: grep 명령과 결과가 마감 증거 테이블에 남았다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- 분할 draft 형태를 "롤링"(Part 1 마커에 분할 목록 전체 + Part 2는 첫 feature task만, 이후 feature는 차례마다 새 lite draft)으로 정함 — 분할 목록이 마커를 타고 spec todo가 되는 구조. 사용자 확인 필요.
- 규칙 2(계약 오류 반복)의 대응을 "full 전환"(출제자·응시자 분리 활용)에서 "draft 복귀"로 바꿈 — 남는 안전장치는 테스트 불변 규칙 + implementation-review Fresh Verification. 토론에서 합의된 트레이드의 구현이므로 확인 불요로 판단.
