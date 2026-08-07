# Feature Draft: discussion 스킬 규범 다이어트

> 규모 판정: 적격 — 단일 스킬 쌍(claude+codex 미러), 변경 요소 9건(F1~F9)이 task 4개에 1:1~n:1로 눈검산 가능

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
SKILL_AUTHORING_NORMS 리뷰 finding F1~F9를 discussion 스킬 쌍에 반영한다: 반복 지시 통합, AGENTS.md work log 규약과의 충돌 해소, 요약 템플릿의 references/ 분리(verbatim 복사 지시), 수치 노브의 기준화, field-guide "아키텍처를 바꾸는 질문 우선" 기준 추가. 새 contract: **discussion 요약 템플릿은 `references/summary-template.md`가 단일 소스**이고 Step 4는 이를 Read 후 verbatim 복사한다.

## Scope
- **In**: `.claude/skills/discussion/` 본문·references, `.codex/skills/discussion/` 미러(3-way merge), 신규 `references/summary-template.md` 양쪽
- **Out**: discussion-question-guide.md·examples 내용 개편, 다른 스킬 쌍, AGENTS.md 수정
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | 본문 규범 다이어트(F1,2,5~9) | `.claude/skills/discussion/SKILL.md`, `.codex/skills/discussion/SKILL.md` | `find . -path "*/skills/discussion/SKILL.md"` → 정확히 2건 | Task 3 (T1 반영분의 미러 전파) |
| P2 | 요약 템플릿 분리(F3,4) | `.claude/skills/discussion/references/summary-template.md`[C], `.codex/skills/discussion/references/summary-template.md`[C], 양쪽 SKILL.md Step 4 지시 | `grep -l "요약 출력 형식" .claude/skills/discussion/SKILL.md .codex/skills/discussion/SKILL.md` → 인라인 템플릿 보유 정확히 2건 + 양쪽 `references/` 디렉토리 실재 | Task 2·3 |

# Part 2: Tasks

### Task 1: claude 본문 다이어트 (F1·F2·F5~F9)
반복·충돌·과잉 규칙을 규범 체크리스트에 맞춰 정리한다. 행동 로직(커버리지·게이트·카테고리 체계)은 불변.

**Acceptance Criteria**:
- [ ] AC1: 파일 생성 제한 규칙이 Hard Rules 1곳에만 존재한다 — 도입부 굵은 재천명·HR2/HR3 중복이 사라져 `grep -c "파일 생성"` 류 검산으로 규칙 서술이 1회
- [ ] AC2: Hard Rules에 work log 예외가 명시된다("호출 환경의 work log 규약에 따른 기록은 예외") — AGENTS.md §5와의 충돌 해소
- [ ] AC3: 수치 노브 4건(연속 2라운드 비판 금지·매 3라운드 요약·stagnation 2회·재방문 1회)이 각각 기준 서술로 전환되거나 근거 1줄 병기 — 무근거 수치 잔존 0
- [ ] AC4: 3.1/3.2 의사코드 블록이 산문(+내부 상태 필드 열거)으로 대체된다
- [ ] AC5: 깊이 신호·비판 유형·수렴 신호 표의 예시 셀이 기준 열만 남고, 상세 예시는 question-guide 참조 1줄로 대체된다
- [ ] AC6: 질문 선택 전략에 "답이 아키텍처(구조·범위·후속 작업 방향)를 바꾸는 질문 우선" 기준이 존재한다
- [ ] AC7: HR4(언어 따라가기) 삭제 — 잔존 0
- [ ] AC8: AC/게이트/카테고리 4종/근거 유형 4종 enum·Gate 구조는 diff에서 의미 변경 없음

**Target Files**:
- [M] `.claude/skills/discussion/SKILL.md` -- F1·F2·F5~F9 반영

### Task 2: 요약 템플릿 references/ 분리 (F3·F4)
템플릿 단일 소스화 + 로드 시점 명시.

**Contracts**: 요약 형식의 단일 소스는 `references/summary-template.md`. Step 4는 "Read 후 verbatim 복사, `[...]` 슬롯만 치환"으로 소비한다.

**Acceptance Criteria**:
- [ ] AC1: `references/summary-template.md`가 기존 인라인 템플릿과 내용 동일하게 존재하고, SKILL.md 본문에서 템플릿 코드블록이 제거된다
- [ ] AC2: Step 4에 Read+verbatim 복사+슬롯 치환 지시가 존재한다
- [ ] AC3: Additional Resources의 각 파일에 로드 시점 1줄이 병기된다(question-guide: Step 3에서 질문 전략 필요 시 / examples: human reference / summary-template: Step 4 필수 Read)

**Target Files**:
- [C] `.claude/skills/discussion/references/summary-template.md` -- 템플릿 이동
- [M] `.claude/skills/discussion/SKILL.md` -- Step 4 지시 교체·리소스 로드 시점

### Task 3: codex 미러 3-way merge 전파
T1·T2의 delta를 codex 적응 delta(request_user_input, interactive-only 등) 보존하며 재적용한다. 단순 복사 금지.

**Acceptance Criteria**:
- [ ] AC1: codex SKILL.md에 Task 1 AC1~AC7·Task 2 AC1~AC3 각각에 대응하는 변경이 반영된다 (섹션명 매핑: claude `Additional Resources` ↔ codex `Companion Assets`)
- [ ] AC2: codex 고유 delta(HR1 interactive-only, request_user_input 용어, HR6 최신성 검증)가 보존된다
- [ ] AC3: `.codex/skills/discussion/references/summary-template.md` 존재, claude 쪽과 형식 동일

**Target Files**:
- [M] `.codex/skills/discussion/SKILL.md` -- 3-way merge
- [C] `.codex/skills/discussion/references/summary-template.md` -- 템플릿 미러

### Task 4: read-only 전파 census 검증
변형 표기·잔존 grep 전수 검증.

**Acceptance Criteria**:
- [ ] AC1: 양쪽 SKILL.md에서 "요약 출력 형식" 인라인 코드블록 잔존 0, summary-template 참조 각 1회 이상 (grep — T2 AC1·T3 AC3의 post-state 확인)
- [ ] AC2: Task 1 AC1·AC7의 삭제 대상 문구 잔존 0 (grep, kebab/공백 변형 포함) + Task 1 AC4의 의사코드 fence 잔존 0
- [ ] AC3: 이번 변경이 건드리는 섹션(Hard Rules·3.1·3.2·Step 4·리소스 섹션)의 헤더가 양쪽 미러에 각각 존재한다 (구체 grep — 전체 헤더 diff는 기존 적응 차이가 있어 검증 기준이 아님)

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- work log 예외 문구는 AGENTS.md를 직접 인용하지 않고 "호출 환경의 work log 규약"으로 일반화했다(플러그인 이식성) — 결정, 사용자 확인 불요.
