# Feature Draft: 하네스 §3 경량 경로(light path) 규칙 + 템플릿 4벌 전파

> 규모 판정: 적격 — 규칙 문단 하나를 5개 표면(repo AGENTS.md 1 + 하네스 템플릿 미러 4)에 verbatim 추가 + read-only census, task↔표면 대응이 1:1로 눈검산 가능.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

SDD 체인에 **경량 경로(light path)** 를 명문화한다: 성질 기준 3조건(새 contract/invariant 없음 · 신규 파일 없음(work log 제외) · 전파 표면 전수 열거 + diff/grep 검증 가능)에 모두 해당하는 소규모 변경은 풀 체인 대신 **직접 구현 → 검증 → spec-sync**로 처리할 수 있다. 직전 feature(게이트 재리뷰 권고, PR #42)를 이 경로로 처리한 실측이 근거다.

새 contract/invariant:
- **경량 경로 적격 판정 기준**(성질 3조건 + "애매하면 풀 체인" 보수 기본값 + 항상-풀-체인 목록)이 하네스 §3의 계약이 된다 — 이후 모든 작업의 경로 선택이 이 기준에 의지한다.
- **경량 경로 불변식**: 경량이어도 브랜치·Execute→Verify·spec-sync·work log는 생략 불가, 채택 시 판정 근거 1줄을 work log에 기록.
- 전파: 이 규칙은 repo AGENTS.md만이 아니라 spec-create/spec-upgrade의 하네스 템플릿 정본+미러 3벌에도 동일 문면으로 들어간다 — 앞으로 이 스킬이 초기화하는 모든 repo에 적용된다.

## Scope
- **In**: repo `AGENTS.md` §3, 하네스 템플릿 4벌(`{.claude,.codex}/skills/{spec-create,spec-upgrade}/references/agents-harness-template.md`)의 §3, read-only census.
- **Out**: SDD 스킬 본문(feature-draft/implementation 등)의 변경 — 경로 선택은 하네스 소관이지 스킬 소관이 아니다. spec 표면 갱신(spec-sync 소관). worklog-gate 등 hook 변경 없음.
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: repo AGENTS.md §3에 경량 경로 문단 추가

하네스 §3(SDD 워크플로우) 말미에 경량 경로 규칙 문단을 추가한다. 문단은 아래 4요소를 모두 담는다 (확정 문면은 Contracts 참조).

**Contracts**: §3에 추가되는 확정 문면 —

> **경량 경로 (light path)**: 아래 셋에 **모두** 해당하는 소규모 변경은 풀 체인 대신 **직접 구현 → 검증 → spec-sync**로 처리해도 된다 — ① 새 contract/invariant가 없다 ② 신규 파일이 없다(work log 제외) ③ 전파 표면(미러·섹션 리터럴·등록 목록)이 전수 열거되고 각각 diff/grep로 검증된다. 하나라도 아니거나 판정이 애매하면 풀 체인이 기본값이다. 새 계약·agent 반환 형식·dispatch 구조 변경, rename/전파류(census 필요), 신규 skill/agent 추가는 항상 풀 체인이다. 경량 경로에서도 브랜치·Execute→Verify(§2)·spec-sync·work log(§5)는 생략하지 않으며, 채택 시 판정 근거 1줄을 work log 항목에 남긴다.

**Acceptance Criteria**:
- [ ] AC1: `AGENTS.md` §3에 위 문단이 존재하고 4요소를 각각 담는다 — (a) 적격 3조건(①②③), (b) "애매하면 풀 체인" 보수 기본값, (c) 항상-풀-체인 목록(새 계약·반환 형식·dispatch 구조·rename/census·신규 skill/agent), (d) 생략 불가 항목(브랜치·Execute→Verify·spec-sync·work log) + 판정 근거 1줄 기록. 요소별 개별 grep으로 판정한다.
- [ ] AC2: 변경이 §3 구간 내부에 한정된다 — `git diff AGENTS.md`의 변경 줄이 `## 3.` ~ `## 4.` 사이에만 존재.

**Target Files**:
- [M] `AGENTS.md` -- §3에 경량 경로 문단 추가

### Task 2: 하네스 템플릿 4벌에 동일 문단 전파

정본(`.claude/skills/spec-create/references/agents-harness-template.md`)의 §3에 Task 1과 **verbatim 동일** 문단을 추가하고, 미러 3벌은 정본 파일을 그대로 복사해 동기화한다(재타이핑 금지 — verbatim-reference-copy 규범).

**Acceptance Criteria**:
- [ ] AC1: 템플릿 4벌이 파일 전체 문면 동일하다 (`diff` 3쌍 무출력).
- [ ] AC2: 템플릿에 추가된 문단이 repo `AGENTS.md`의 추가 문단과 verbatim 동일하다 (§3 구간 추출 후 문자열 비교).
- [ ] AC3: 템플릿 diff도 §3 구간 내부에 한정된다 (관리 주석·다른 §섹션·변수 슬롯 무변경).

**Target Files**:
- [M] `.claude/skills/spec-create/references/agents-harness-template.md` -- 정본 편집
- [M] `.codex/skills/spec-create/references/agents-harness-template.md` -- 정본 복사
- [M] `.claude/skills/spec-upgrade/references/agents-harness-template.md` -- 정본 복사
- [M] `.codex/skills/spec-upgrade/references/agents-harness-template.md` -- 정본 복사

### Task 3: read-only 전파 census

§3 내부 추가가 다른 전파 표면을 건드리지 않음을 전수 grep으로 확정한다 (harness-section-propagation 함정 이력 대응).

**Acceptance Criteria**:
- [ ] AC1: 새 §섹션이 아님을 확정 — 5개 표면 모두 `^## [0-9]\.` 헤더 수가 변경 전후 동일(템플릿·AGENTS.md 각 6개)하고, spec-create/spec-upgrade SKILL.md 4파일의 섹션 범위 리터럴(`§0`~`§5` 류)이 가리키는 섹션 수와 일치해 갱신 불요.
- [ ] AC2: `harness-context.sh`(hook 미러 포함)가 AGENTS.md/템플릿을 **동적으로 읽는지** 확인 — 하네스 본문을 임베딩한 사본이 없어 추가 전파 표면이 없다.
- [ ] AC3: "경량 경로" 및 변형 표기 "light path" 문자열이 의도 표면에만 존재한다 — repo 전체 grep으로 잔존/누락 없음. 허용 목록(파일명 고정): `AGENTS.md`, 템플릿 4벌, 이 draft, `_sdd/work_log/2026-08-03.md`(구현일이 다르면 그날 로그 추가), 그리고 기존 PR #42 경량 처리 기록과 이후 spec-sync entry가 사는 `_sdd/spec/` 표면(`decision_log.md`·`logs/changelog.md`·`main.md`).

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- 규칙 문면은 사용자와 논의한 기준(성질 3조건·보수 기본값·불변식)을 그대로 문장화했다 — 사용자 확인 불요.
- 이 feature의 implementation-review 게이트는 **simplicity 다이어트(PR #41, 오늘 플러그인 발효)의 첫 관측 표본**이다 — 2기준(simplicity reviewer 실측 시간 + "스캔 요지"류 비-finding 단락 소멸)으로 기록만 하고 판정은 유보(n=1). 기록 주체는 게이트 반환을 relay한 메인 루프, 기록 위치는 `_sdd/work_log/2026-08-03.md`의 게이트 항목이다.
