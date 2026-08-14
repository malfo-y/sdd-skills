# Feature Draft: 느린 테스트 실행 정책 — 표적 기본 + 무거운 전체 실행 사용자 확인 게이트

> 규모 판정: 적격 — 변경 요소 5개(회귀 개정·리뷰어 이관·하네스 정비·parity 복원·census)가 task 4개에 1:1 배정, coverage 눈검산 가능

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
2026-08-11 토론(`_sdd/discussion/2026-08-11_discussion_slow_test_execution_policy.md`) 결정 8건 중 **이번 신규분 — 결정 6·7·8의 리뷰어 slow 이관과 회귀 확인 게이트(fail-closed에 사용자 확인 escape 추가)** — 를 스킬 계약으로 실현하고, 사용자 직접 커밋 `940ab96`(하네스 §2 "10초 이상 테스트 분리" 규칙)을 정비·spec 전파한다. 결정 4·5의 30초 targeted 예산·재실행 금지는 2026-08-12 선행 draft(`_processed_2026-08-12_feature_draft_minimal_slow_test_guard.md`)가 이미 반영한 몫이고, 결정 5 후반의 slow lane 등록 라우팅은 lane 스키마 비도입과 함께 Out이다.

새 contract/invariant:
- **회귀 실행 계약 개정**: `implementation` 마감 회귀는 이번 변경 관련 표적 + fast 회귀(무거운 test 제외)를 기본으로 실행한다. **무거운 test가 포함된 전체 suite는 repo(env.md 등)가 명시한 checkpoint이거나 사용자 확인을 받은 경우에만** 실행한다 — 확인 없는 강행도, 조용한 skip도 금지하며 미실행분은 마감 요약에 보고한다. fix 후 회귀 재실행도 같은 규칙을 상속한다(문면 소유자는 마감 1).
- **리뷰어 slow 이관 계약**: 리뷰어(implementation-review-agent·pr-review-agent)는 느린 test를 재실행하지 않고, checkpoint evidence가 없는 slow 의존 AC는 임의 실행 없이 `UNTESTED`(사유: slow — checkpoint 대기)로 보고한다.
- **하네스 테스트 설계 규칙(사용자 커밋 940ab96 정비)**: "10초 이상 걸리는 테스트는 분리해 두고(fixture·suite 분할 등 수단 자유), 기본 실행에서 제외해 꼭 필요한 경우에만 돌리도록 설계한다" — fixture 단일 수단 강제 문구를 완화(8/11 토론의 변경 금지 제약 준수). 하네스 템플릿 4벌 byte-parity 복원 포함.
- **비도입 결정**: env.md 정형 fast/slow lane 스키마는 도입하지 않는다 — 사용자 확인 게이트가 분류 오류 비용을 "한 번 묻기"로 낮춰 선언 인프라 없이 안전이 닫히고, env.md 자유 서술 참조로 충분(두 번째 사용처 실재 시 재검토).
- 10초(개별 테스트 설계·분리 기준, 하네스)와 30초(targeted 명령 wall-clock 예산, 스킬)는 층이 다른 공존 계약이다.

## Scope
- **In**: implementation 마감 회귀 개정(claude·codex), 리뷰어 2종 slow 이관 문구(claude·codex 4벌), 하네스 규칙 정비 + 템플릿 parity 복원(5벌), 문구 census
- **Out**: env.md 정형 lane 스키마, 프레임워크별 fixture/마커 구현 가이드, CI vendor 설정, 30초 예산 값 변경
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: implementation 마감 회귀를 표적 기본 + 전체 실행 확인 게이트로 개정
유일한 자동 전체 suite 실행 지점(마감 1)을 닫는다 — 40분급 suite가 fix당 회귀 재실행까지 곱해지는 사고 경로의 근원.

**Contracts**: 마감 1 문면을 Part 1 「회귀 실행 계약 개정」대로 교체한다(표적+fast 기본 / 무거운 전체는 checkpoint 또는 사용자 확인 / 강행·조용한 skip 금지 / 미실행분 마감 요약 보고). "무거운"의 판정은 repo 명시(env.md 서술·test 마커)와 알려진 실행시간으로 하되 애매하면 사용자에게 묻는다. 마감 3의 fix 회귀 재실행 문면은 수정하지 않는다(마감 1 규칙 상속 — 재서술 금지). claude·codex SKILL 짝 동일 의미 반영.

**Acceptance Criteria**:
- [ ] AC1 (1등급): 두 SKILL.md에서 `전체 테스트 suite가 있으면 실행한다` 문구가 사라졌다. 평가: `grep -c '전체 테스트 suite가 있으면' .claude/skills/implementation/SKILL.md .codex/skills/implementation/SKILL.md` 각 0.
- [ ] AC2 (2등급): 마감 1이 Contracts의 4요소(표적+fast 기본·checkpoint/사용자 확인 조건·강행/skip 금지·미실행 보고)를 모두 명시하고, 같은 파일 공통 제한의 "느리다고 알려진 test는 … checkpoint에서만" 문구와 모순이 없다(사용자 확인이 "사용자가 명시한 checkpoint"의 한 형태로 읽히는지). 평가: reviewer가 두 파일에서 각 요소 문장 + 무모순 판정 인용.

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- 마감 1 회귀 문면 교체
- [M] `.codex/skills/implementation/SKILL.md` -- 동일 의미 반영

### Task 2: 리뷰어 2종에 slow 의존 AC의 UNTESTED 이관을 명시
"checkpoint에서만" 문구는 있으나 checkpoint evidence 부재 시의 행동(임의 실행 금지 + UNTESTED 라우팅)이 비어 있다 — 8/11 결정 6·8의 미구현분.

**Contracts**: 기존 `느리다고 알려진 test는 repo 또는 사용자가 명시한 checkpoint에서만 실행한다` 직후에 1문장 추가: 「checkpoint evidence가 없는 slow 의존 AC는 임의 실행하지 않고 `UNTESTED`(사유: slow — checkpoint 대기)로 보고한다」. 4벌(claude agent 2 + codex toml 2) 동일 의미. 기존 UNTESTED 처리 경로(evidence 결속·NEEDS DISCUSSION 흐름)는 불변.

**Acceptance Criteria**:
- [ ] AC1 (1등급): 4파일 모두에서 `checkpoint에서만 실행한다` 문구 뒤에 slow UNTESTED 이관 문장이 존재한다. 평가: `grep -c 'checkpoint 대기' <4파일>` 각 ≥ 1.
- [ ] AC2 (2등급): 추가 문장이 기존 Fresh Verification/Validation 우선순위 계약과 모순 없이 결합됐다(fast lane fresh 실행 의무 불변). 평가: reviewer 인용 판정.

**Target Files**:
- [M] `.claude/agents/implementation-review-agent.md` -- Hard Rule 5 실행 제한 블록에 1문장
- [M] `.claude/agents/pr-review-agent.md` -- Hard Rule 6 실행 제한 블록에 1문장
- [M] `.codex/agents/implementation-review-agent.toml` -- 동일
- [M] `.codex/agents/pr-review-agent.toml` -- 동일

### Task 3: 하네스 테스트 설계 규칙 정비와 템플릿 byte-parity 복원
사용자 커밋 `940ab96`의 규칙을 유지하되 fixture 단일 수단 강제를 완화하고(8/11 변경 금지 제약), 커밋이 깨뜨린 템플릿 4벌 동일성을 복원한다(`.claude/spec-create`만 이전 줄 마침표 추가로 md5 상이 실측).

**Contracts**: 5벌(AGENTS.md + 템플릿 4)의 해당 줄을 Part 1 「하네스 테스트 설계 규칙」 문구로 교체한다. 템플릿 4벌은 교체 후 byte-identical이어야 하며, 마침표 drift는 4벌이 같은 쪽으로 정렬되면 방향은 무관하다. AGENTS.md는 placeholder 적응 delta 외 동일 의미.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `fixture를 붙여` 문구가 repo 전체에서 0건이고(기록물 `_sdd` 제외), 새 문구가 5파일에 각 1회 존재한다. 평가: `grep -rc 'fixture를 붙여' --exclude-dir=.git --exclude-dir=_sdd .` 0 + 고정 anchor `분리해 두고` grep 5파일 각 1 (Task 4 census도 같은 anchor 사용).
- [ ] AC2 (1등급): 템플릿 4벌의 md5가 동일하다. 평가: `md5 -q` 4벌 출력 1종.

**Target Files**:
- [M] `AGENTS.md` -- §2 규칙 문구 교체
- [M] `.claude/skills/spec-create/references/agents-harness-template.md` -- 문구 교체 + parity 정렬
- [M] `.claude/skills/spec-upgrade/references/agents-harness-template.md` -- 문구 교체
- [M] `.codex/skills/spec-create/references/agents-harness-template.md` -- 문구 교체
- [M] `.codex/skills/spec-upgrade/references/agents-harness-template.md` -- 문구 교체

### Task 4: 문구 census 검증
교체·삭제 대상 문구의 변형 잔존을 read-only로 전수 확인한다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): live 표면(기록물 `_sdd`·`.git` 제외)에서 `전체 테스트 suite가 있으면`·`fixture를 붙여` 잔존 0, `checkpoint 대기` hit가 정확히 Task 2의 4파일, anchor `분리해 두고` hit가 정확히 Task 3의 5파일. 평가: `grep -rn` 각 패턴 출력 대조.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- 전체 suite 확인 게이트의 발동 주체: 스킬 문면은 "사용자 확인"으로 두고 무인 실행(autopilot/goal loop)에서는 확인 불가 시 미실행+보고로 fail-closed — 8/11 결정 8과 정합. 확인 불필요(자명).
- `940ab96`은 revert하지 않고 이 feature가 문구를 정비·전파한다 — 사용자 지시("돌리거나 고치고")의 '고치기' 선택. 확인 불필요(지시 범위 내).
