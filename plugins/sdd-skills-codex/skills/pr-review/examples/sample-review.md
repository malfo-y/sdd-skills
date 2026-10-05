# Sample PR Review Session

이 예제는 `pr-review`의 정상 모드와 제한 결과를 보여준다.

- baseline SHA에서 spec을 읽었으면 `FOUND`: spec-based verification 포함
- 트리 조회 성공 후 spec 부재를 확인했으면 `ABSENT`: code-only mode
- 트리/spec 읽기가 실패했으면 `UNREADABLE`: 원인을 남긴 제한 리포트

> `pr-review`는 `_sdd/spec/`를 수정하지 않는다. 스펙 반영이 필요하면 리포트에 기록하고 후속으로 `$sdd-orchestrator`로 spec-sync 단계를 실행한다.

## Example A: from-branch spec 기반 리뷰

### 리뷰 시작

```text
User: PR #42 리뷰해 줘

Codex: PR 리뷰를 시작합니다.

## 사전 조건 확인

✓ gh auth status: 인증됨
✓ PR: #42 - 사용자 인증 시스템 구현 및 세션 관리 버그 수정
✓ baseline headRefOid: abc1234
✓ 로컬 HEAD: abc1234, 관련 working tree clean (브랜치 이름은 판정 조건 아님)

## PR 데이터 수집
- 변경 파일: 12개 (gh pr diff --name-only)
- 상태: OPEN
- 수집 전후 headRefOid 일치: abc1234
- 통합 리포트 slug: auth_system (같은 날짜의 기존 파일이 있으면 auth_system_2)

## Spec Status (Step 2)
- git ls-tree -r --name-only abc1234 -- _sdd/spec/로 spec 존재만 판정
- Spec Status: FOUND (_sdd/spec/main.md, auth.md, security.md) — 내용 읽기는 correctness worker 소관
```

### worker 입력의 범위

메인은 PR 번호·Baseline(abc1234와 같은 SHA 읽기 경로)·Changed Files·Spec Status·Relevant Context(인증 경계와 동작 보존에 필요한 저자 설명)·slug만 관리한다. 두 worker에 같은 PR Review Input을 전달하며, diff·spec 본문·comments·테스트 실행은 worker가 직접 한다.

### correctness·simplicity worker spawn과 verdict 합성

```text
Codex:
## Worker Spawn (correctness + simplicity)

Mailbox(Desktop/current CLI): invocation별 run_id가 들어간 parent-tree 고유 task_name + fork_turns: "none" + framed message로 correctness·simplicity spawn 2회 → target 없는 mailbox wait 반복 → close 없음. agent_type: "explorer"는 simplicity spawn에만, active schema가 지원할 때 추가한다(correctness는 생략).
Target/close(legacy CLI schema): 같은 framed message로 spawn 2회 → target wait → final 기록 → 완료 handle close. agent_type: "explorer"는 simplicity spawn에만, active schema가 지원할 때 추가한다(correctness는 생략).
framed message: correctness는 `## Mode: pr-review (correctness)` + 계약 경로(references/correctness-contract.md) 지시 + `## Input Data`의 PR Review Input, simplicity는 계약 전문 verbatim + PR Review Input.
활성 schema가 어느 lifecycle contract인지 확정할 수 없으면 spawn하지 않고 schema blocker를 보고한다. agent_type 부재만으로는 blocker가 아니다.

두 렌즈 결과 요약:
- correctness (worker 반환): spec FOUND (main.md, auth.md, security.md), AC MET 2 / NOT MET 1 / PARTIAL 1, 검증 FAIL: tests/test_auth.py (38/40 통과, Local abc1234 output), High 1·Med 1·Low 1 (finding당 위치·문제·수정 포함)
- simplicity (worker 반환): Medium 1 (위치·현재 형태·제안 형태 포함)

→ Verdict: REQUEST CHANGES (correctness High 1 + simplicity Medium 1이 rationale에 기여)
```

### 생성된 리포트 예시

```markdown
# PR Review Report

**PR**: #42 - 사용자 인증 시스템 구현 및 세션 관리 버그 수정
**PR Author**: developer-kim
**Review Date**: 2026-04-02
**Reviewer**: Codex (gpt-5.6-sol / workers gpt-6.1-sol/high)
**Spec**: FOUND (abc1234)
**Review Status**: COMPLETE

---

## Verdict

**REQUEST CHANGES**

**Rationale**: refresh 토큰 경로의 핵심 acceptance criterion이 미충족이고, 인증 컨텍스트 주입 테스트가 비어 있어 머지 전 보완이 필요하다.
**Signals**: correctness High 1·Med 1·Low 1 / simplicity Med 1 / 검증 FAIL: tests/test_auth.py (38/40 통과, Local abc1234 output)

---

## 1. Pre-merge (고쳐야 할 것)

### 1. [High · correctness] refresh 시 새 만료 시간이 생성되지 않음
- **위치**: `src/services/auth_service.py:89-102`
- **문제**: refresh 분기가 기존 `exp` 클레임을 그대로 복사해 새 토큰이 원 토큰과 같은 시점에 만료된다. spec AC #3 위반이고 `test_refresh_token`이 실패한다.
- **수정**: refresh 시 현재 시각 기준으로 `exp`를 재계산해 토큰을 발급한다.

### 2. [Medium · simplicity] 토큰 검증 로직이 두 곳에 중복
- **위치**: `src/middleware/auth.py:30-45`, `src/services/auth_service.py:70-84`
- **문제**: 서명 검증 + 만료 확인 로직이 미들웨어와 서비스에 동일하게 복제돼 있다 (중복 코드·단일 사용처 추상화 차원).
- **수정**: `verify_token()` 하나로 합치고 두 호출처에서 재사용한다 — 동작 동일.

---

## 2. 개선 제안 (non-blocking)

### 1. [Medium · correctness] 인증 컨텍스트 주입 경로에 테스트 없음
- **위치**: `src/middleware/auth.py:47-55`
- **문제**: spec AC #4의 구현은 있으나 테스트가 없어 회귀를 감지할 수 없다 (PARTIAL).
- **수정**: 미들웨어 통과 후 request context에 user가 실리는지 검증하는 테스트를 추가한다.

- `src/config/cors.py:12` — CORS Authorization 헤더 허용은 spec에 없는 변경이므로 머지 후 `$sdd-orchestrator`의 spec-sync 단계로 spec 반영을 검토한다.

---

## 3. 확인된 것

JWT secret은 환경변수로 관리되며 확인한 보안 요구사항 위반은 없다. simplicity의 중복 차원 finding은 §1에 수록했고, 나머지 세 차원은 통과했다.

---

## 4. AC 검증 ledger

| # | Criterion | Implementation | Test | Status | Evidence |
|---|-----------|----------------|------|--------|----------|
| 3 | refresh 시 새 만료 시간 발급 | NOT MET | FAIL | NOT MET | §1.1; abc1234의 로컬 test_refresh_token 실패 output |
| 4 | 인증 컨텍스트 주입 | MET | UNTESTED | PARTIAL | §2.1; 대응 테스트 없음 |

MET: #1–#2

---

## Metadata

**PR commit SHA**: abc1234
**Spec source**: abc1234:_sdd/spec/main.md, auth.md, security.md
**Validation source**: Local abc1234, clean; tests/test_auth.py 실행 output (40개 중 38개 통과)
**Generated at**: 2026-04-02 17:40:00
```

## Example B: code-only mode

baseline SHA의 트리 조회가 성공하고 `_sdd/spec/`가 없음을 확인한 저장소에서는 code-only mode로 진행한다.

```text
User: 이 PR 승인해도 되는지 봐 줘

Codex:
## Spec Status (Step 2)
- headRefName: fix/password-reset-expiry
- baseline headRefOid: def5678
- git ls-tree -r --name-only def5678 -- _sdd/spec/ 성공, spec 파일 없음 (ABSENT)

→ code-only mode로 진행 (spec 컨텍스트 없이)
- correctness·simplicity worker를 함께 spawn (같은 PR Review Input)
- correctness worker 반환: PR title/body/코멘트에서 추론한 AC 검증, spec ABSENT, Validation source는 Local def5678 clean의 tests/test_token_expiry.py 전체 통과 output
```

### code-only 리포트 예시

```markdown
# PR Review Report

**PR**: #51 - fix: 비밀번호 재설정 토큰 만료 검증 누락
**PR Author**: developer-lee
**Review Date**: 2026-04-02
**Reviewer**: Codex (gpt-5.6-terra / workers gpt-6.1-sol/high)
**Spec**: ABSENT (code-only)
**Review Status**: COMPLETE

---

## Verdict

**APPROVE**

**Rationale**: PR 설명에서 추론한 acceptance criteria가 구현과 테스트로 모두 뒷받침되며, 보안상 명백한 회귀는 보이지 않는다.
**Signals**: correctness Low 1 / simplicity 없음 / 검증 PASS: tests/test_token_expiry.py (Local def5678 output)

---

## 1. Pre-merge (고쳐야 할 것)

없음.

---

## 2. 개선 제안 (non-blocking)

- `src/services/password_service.py:34` — 추후 spec 도입 시 비밀번호 재설정 보안 규칙(토큰 만료 정책)을 문서화하면 운영 추적성이 좋아진다 (`$spec-create` 검토).

---

## 3. 확인된 것

simplicity 4개 차원 스캔에서 finding 없음. 보안 검토에서 명백한 회귀는 확인되지 않았다.

---

## 4. AC 검증 ledger

문제 AC 없음.

MET: #1–#3

---

## Metadata

**PR commit SHA**: def5678
**Spec source**: ABSENT (def5678 트리 조회 성공)
**Validation source**: Local def5678, clean; tests/test_token_expiry.py 통과 output
**Generated at**: 2026-04-02 18:00:00
```

## 제한 결과 예시

- 로컬 HEAD가 baseline과 다르거나 dirty이면 현재 작업을 보존하고 baseline SHA를 직접 읽는다. 동일 SHA의 CI/격리 실행 evidence도 없으면 테스트 판정은 `UNTESTED`다.
- spec 트리 또는 필요한 파일을 읽지 못하고 동등 SHA 읽기도 실패하면 `Spec: UNREADABLE`, `Review Status: LIMITED`와 원인·미충족 skill AC·재개 조건을 기록하고 `NEEDS DISCUSSION (제한된 권고)`으로 종료한다. code-only로 부재를 추정하지 않는다.
- correctness 또는 simplicity dispatch가 blocker로 불가능하거나 확정 실패하면 확보된 렌즈 결과를 보존하고 누락 렌즈와 미충족 AC를 기록한다. `NEEDS DISCUSSION (제한된 권고)`으로 종료하며, 같은 blocker에서 반복 dispatch하거나 inline으로 대신하지 않는다.
- worker의 `headRefOid` 불일치(correctness BLOCKED 또는 simplicity Assumptions blocker)는 렌즈 실패가 아니다. 새 SHA로 Step 0~2를 다시 수행해 PR Review Input(Baseline·Changed Files·Spec Status)을 다시 만든 뒤 두 worker를 1회 다시 띄우고, 또 불일치하면 `LIMITED`로 닫는다.
