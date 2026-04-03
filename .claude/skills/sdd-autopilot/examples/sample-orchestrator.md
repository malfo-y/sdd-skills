# Sample Orchestrator

이 파일은 autopilot이 생성하는 오케스트레이터의 품질 기준 예시다.
완전한 장문 스펙이 아니라, reasoning과 파이프라인 구조가 어떻게 보여야 하는지 빠르게 감 잡기 위한 샘플만 남긴다.

---

## Example A: 중규모 기본형

사용자 요청: `/autopilot JWT 기반 인증 시스템 구현`

```markdown
# Orchestrator: JWT 인증 시스템

**생성일**: 2026-04-04T14:30:00
**규모**: 중규모
**생성자**: autopilot

## 기능 설명

JWT 기반 인증 시스템을 구현한다. 로그인, 로그아웃, 토큰 갱신 기능을 포함한다.

### 구체화된 요구사항
- JWT 기반 Bearer 토큰 인증
- 로그인/로그아웃/토큰 갱신 엔드포인트
- Access token 1시간, Refresh token 7일
- bcrypt 비밀번호 해싱

### 제약 조건
- 기존 Express.js 프레임워크 사용
- 기존 User 모델 확장
- 기존 미들웨어 패턴 유지

## Acceptance Criteria
- [ ] 로그인 성공 시 access/refresh token이 발급된다.
- [ ] refresh token 갱신이 동작하고 만료 정책이 적용된다.
- [ ] 로그아웃 시 refresh token이 무효화된다.
- [ ] 관련 검증이 테스트 또는 리뷰 evidence와 연결된다.

## Reasoning Trace

- 기존 global spec이 존재하므로 spec-first 전제 조건을 만족한다.
- 영향 범위가 4-10파일 수준이라 중규모로 판단했다.
- `feature-draft`가 temporary spec과 기본 implementation plan을 함께 제공하므로 별도 `implementation-plan`은 생략했다.
- 인증 로직은 contract와 failure guarantee가 중요하므로 review-fix 사이클을 포함했다.
- 테스트는 짧은 API/서비스 검증 중심이라 인라인 테스트 전략을 선택했다.

## Pipeline Steps

### Step 1: feature-draft
**Claude subagent_type**: `feature-draft`
**입력 파일**: `_sdd/spec/main.md`
**출력 파일**: `_sdd/drafts/feature_draft_jwt_auth.md`

**프롬프트**:
JWT 기반 인증 시스템에 대한 feature draft를 작성하세요.
Part 1에는 temporary spec 7섹션을 포함하고, `Contract/Invariant Delta`와 `Validation Plan`을 ID로 연결하세요.
Part 2에는 Target Files 기반 implementation plan을 작성하세요.

### Step 2: implementation
**Claude subagent_type**: `implementation`
**입력 파일**: `_sdd/drafts/feature_draft_jwt_auth.md`, `_sdd/spec/main.md`
**출력 파일**:
- `src/middleware/auth.js`
- `src/routes/auth.js`
- `src/services/auth-service.js`
- `src/services/token-service.js`
- `src/models/user.js`
- `test/services/auth-service.test.js`

**프롬프트**:
feature draft를 기반으로 구현을 진행하세요.
특히 temporary spec의 `Contract/Invariant Delta`와 `Validation Plan`을 기준으로 TDD 방식으로 진행하세요.

### Step 3: review-fix loop
(autopilot 직접 관리)

### Step 4: spec-update-done
**Claude subagent_type**: `spec-update-done`
**입력 파일**: `_sdd/spec/main.md`, `_sdd/drafts/feature_draft_jwt_auth.md`, 구현된 코드 파일
**출력 파일**: `_sdd/spec/main.md`

**프롬프트**:
JWT 인증 시스템 구현 완료 기준으로 global spec을 실제 코드와 동기화하세요.
temporary spec의 실행 정보는 버리고, 구현되어 검증된 지속 정보만 global spec에 반영하세요.

## Review-Fix Loop

- **최대 반복**: 3회
- **종료 조건**: critical = 0 AND high = 0 AND medium = 0
- **수정 대상**: critical/high/medium/low

## Test Strategy

- **방식**: 인라인 디버깅
- **테스트 명령**: `npm test`
- **근거**: Express.js 테스트는 수 초 내 실행 가능
- **Validation linkage**: V1=token issuance, V2=refresh invalidation

## Error Handling

- **재시도 횟수**: 3회
- **핵심 단계**: `feature-draft`, `implementation`
- **비핵심 단계**: `spec-update-done`
```

### 대응 로그 예시

```markdown
# Pipeline Log: JWT 인증 시스템

## Meta
- **request**: "JWT 기반 인증 시스템 구현해줘. 로그인, 로그아웃, 토큰 갱신 포함."
- **orchestrator**: `_sdd/pipeline/orchestrators/orchestrator_jwt_auth.md`
- **started**: 2026-04-04T14:35:00
- **pipeline**: feature-draft -> implementation -> review-fix -> inline-test -> spec-update-done

## Status
| Step | Agent | Status | Output |
|------|-------|--------|--------|
| 1 | feature-draft | completed | `_sdd/drafts/feature_draft_jwt_auth.md` |
| 2 | implementation | completed | `6 files updated` |
| 3 | spec-update-done | completed | `_sdd/spec/main.md` |

## Execution Log

### feature-draft -- 완료
- **출력**: `_sdd/drafts/feature_draft_jwt_auth.md`
- **핵심 결정사항**:
  - C1: access/refresh token contract 분리
  - I1: refresh token revocation invariant 추가
  - V1/V2로 validation linkage 고정

### review-fix -- Round 1/3
- **리뷰 결과**: critical 0건, high 1건, medium 2건, low 0건
- **수정 대상**: refresh token 무효화 누락
- **수정 결과**: 완료

### review-fix -- Round 2/3
- **리뷰 결과**: critical 0건, high 0건, medium 0건, low 2건
- **수정 결과**: 종료 조건 충족

## 최종 요약
- **실행 결과**: 성공
- **Review 횟수**: 2회
- **테스트 결과**: 통과
- **스펙 동기화**: 완료
```

---

## Example B: 대규모 차이점

사용자 요청: `/autopilot 이미지 분류 모델 fine-tuning 파이프라인 구현`

대규모는 중규모 기본형에서 아래가 추가되면 된다.

### Reasoning Trace 차이

```markdown
## Reasoning Trace

- 기존 global spec은 존재하지만, 이번 기능은 범위와 contract가 크게 바뀌므로 `spec-update-todo`를 선행한다.
- 영향 파일 수와 신규 컴포넌트 수가 모두 커서 대규모 변경으로 판단했다.
- feature draft의 temporary spec을 더 세분화해야 하므로 `implementation-plan`을 포함했다.
- 학습 명령 1회가 장시간이므로 인라인 테스트 대신 `ralph-loop-init` 기반 검증을 선택했다.
- 계약과 invariant가 많아 review-fix 사이클을 필수 단계로 둔다.
```

### Pipeline Steps 차이

```markdown
## Pipeline Steps

### Step 1: feature-draft
### Step 2: spec-update-todo
### Step 3: implementation-plan
### Step 4: implementation
### Step 5: review-fix loop
### Step 6: ralph-loop (Execute -> Verify)
### Step 7: spec-update-done
```

### 대규모에서 추가로 꼭 보여야 하는 계약

```markdown
### Step 2: spec-update-todo

- temporary spec에서 scope delta와 CIV delta를 읽는다
- global spec에는 planned persistent information만 반영한다

### Step 3: implementation-plan

- `Contract/Invariant Delta Coverage` 표를 포함한다
- V1, V2 같은 validation ID를 task에 연결한다
```

---

## Reading Guide

- 중규모는 `feature-draft -> implementation -> review-fix -> spec-update-done`이 기본형이다.
- 대규모는 `spec-update-todo`, `implementation-plan`, `ralph-loop-init`가 추가되는 차이를 본다.
- 좋은 오케스트레이터는 global spec과 temporary spec의 역할을 혼동하지 않는다.
