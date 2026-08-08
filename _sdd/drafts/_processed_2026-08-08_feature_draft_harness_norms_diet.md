# Feature Draft: AGENTS.md 하네스 규범 다이어트

> 규모 판정: 적격 — 변경 요소 5건(F1~F5)이 표면 2계층(인스턴스 1 + 템플릿 4 byte-identical)에 매핑, task 3개로 눈검산 가능

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
SKILL_AUTHORING_NORMS §3 체크리스트를 하네스 자신에 적용한다: §2 유효 검증 정의 이중 서술 통합(F1, 인스턴스 — 이중 서술의 두 번째 문장 "검증은 슬래시 커맨드 실제 호출…"은 템플릿에 부재, repo 채움 유래 실측), §3 spec-sync 내부 로직 재서술 제거(F2, 템플릿 공통), §2 work log 의무 포인터화(F3, 템플릿 공통), §0에 원칙 상세 홈 포인터 추가(F4, 인스턴스 — repo 고유 경로), §3·§4 negative 2건 근거 병기(F5, 템플릿 공통). 새 contract 없음 — 기존 계약(§0 원칙 이름, §5 work log 규약, SDD-HARNESS 마커, `<…>` 슬롯)은 전부 불변.

## Scope
- **In**: `AGENTS.md`(인스턴스), `agents-harness-template.md` 정본+미러 3 (spec-create·spec-upgrade × claude·codex)
- **Out**: §섹션 구조 변경(§0~§5 개수·제목 불변 — SKILL.md 4파일의 "§0~§5" 리터럴 12곳 census 비발동), CLAUDE.md, spec-create/spec-upgrade SKILL 본문, 경량 경로 규칙 내용
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | 템플릿 공통 delta(F2·F3·F5) | `AGENTS.md` + `.claude/skills/spec-create/references/agents-harness-template.md`(정본) + 미러 3 (`.codex/skills/spec-create/…`, `.claude/skills/spec-upgrade/…`, `.codex/skills/spec-upgrade/…`) | `grep -rln "planned todo 고정" AGENTS.md .claude/skills/*/references .codex/skills/*/references` → 정확히 5파일(인스턴스 1 + 템플릿 4) 실측; 템플릿 4 md5 동일(4c00412…) | Task 1(인스턴스)·Task 2(템플릿) |

# Part 2: Tasks

### Task 1: 인스턴스 AGENTS.md 수정 (F1~F5 전체)
인스턴스는 템플릿 공통 delta + 인스턴스 한정 delta를 모두 받는다.

**Acceptance Criteria**:
- [ ] AC1 (F1): §2 이중 서술의 두 번째 병렬 문구 "검증은 슬래시 커맨드 실제 호출" 원형 잔존 0, 유효 검증 수단 열거(슬래시 커맨드 호출·`git diff --check`·diff·grep·review)는 단일 문장 1곳에 존재
- [ ] AC2 (F2): §3에서 spec-sync 내부 분기 서술("planned todo 고정(조건부)…evidence 유무로 구분") 잔존 0 — "계획·구현 반영의 단일 진입점" 수준만 잔존
- [ ] AC3 (F3): work log 의무의 완전 서술은 §5에만 존재, §2는 "(§5)" 포인터만 — "예외 없이"가 §5에 1회만 (`grep -c "예외 없이"` = 1)
- [ ] AC4 (F4): §0에 `docs/agentic_coding_principle.md` 포인터 1줄 존재 (원칙 상세·자기점검 질문의 홈)
- [ ] AC5 (F5): §3 카탈로그 복사 금지·§4 복사 금지 negative 각각에 방지 실패 근거가 병기됨
- [ ] AC6: §0~§5 헤더 6개·SDD-HARNESS 마커 쌍·repo 채움 값(브랜치 규칙, 경량 경로, worklog-gate 훅 경로) 불변

**Target Files**:
- [M] `AGENTS.md`

### Task 2: 템플릿 정본+미러 전파 (F2·F3·F5)
정본에 템플릿 공통 delta만 적용하고(관리 주석·`<…>` 슬롯 보존) 미러 3곳에 byte-copy.

**Acceptance Criteria**:
- [ ] AC1: 정본에서 "planned todo 고정…evidence 유무로 구분" 잔존 0(F2), "예외 없이"가 §5에만 1회(F3), §3 카탈로그·§4 복사 금지 negative에 근거 병기(F5); 관리 주석·슬롯(`<repo-name>` 등) 불변
- [ ] AC2: 미러 4곳 md5 동일 (byte-identical 유지)
- [ ] AC3: 인스턴스 한정 delta 미유입 — 템플릿 4곳에서 `agentic_coding_principle` 참조 0, "슬래시 커맨드 실제 호출" 문구 0

**Target Files**:
- [M] `.claude/skills/spec-create/references/agents-harness-template.md`
- [M] `.codex/skills/spec-create/references/agents-harness-template.md`
- [M] `.claude/skills/spec-upgrade/references/agents-harness-template.md`
- [M] `.codex/skills/spec-upgrade/references/agents-harness-template.md`

### Task 3: read-only census 검증
**Acceptance Criteria**:
- [ ] AC1: 삭제 문구 변형형 잔존 0 — "evidence 유무로 구분"·"planned todo 고정" 5파일 전수 grep 0
- [ ] AC2: "§0~§5" 리터럴 소비처(SKILL.md 등) grep — 이번 변경으로 §개수 불변임을 확인 (하네스 헤더 6개 유지)
- [ ] AC3: `git diff --check` PASS

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- F5 근거 문구는 새 관측이 아니라 기존 결정(§4의 존재 이유·스킬 카탈로그 드리프트)에서 인용한다 — 결정, 사용자 확인 불요.
