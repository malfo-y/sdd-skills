# Sample Orchestrator

이 파일은 autopilot이 생성하는 오케스트레이터의 품질 기준 예시다.

## Example A: 중규모 기본형

사용자 요청: `/autopilot JWT 기반 인증 시스템 구현`

```markdown
# Orchestrator: JWT 인증 시스템

**생성일**: 2026-04-04T14:30:00
**규모**: 중규모
**생성자**: autopilot

## 기능 설명

JWT 기반 인증 시스템을 구현한다. 로그인, 로그아웃, 토큰 갱신 기능을 포함한다.

## Acceptance Criteria
- [ ] 로그인 성공 시 access/refresh token이 발급된다.
- [ ] refresh token 갱신이 동작하고 만료 정책이 적용된다.
- [ ] 로그아웃 시 refresh token이 무효화된다.
- [ ] 관련 검증이 테스트 또는 리뷰 evidence와 연결된다.

## Reasoning Trace

- 기존 global spec이 존재하므로 spec-first 전제 조건을 만족한다.
- global spec은 thin core만 유지하고, 기능 수준 contract/validation은 temporary spec에 둔다.
- 영향 범위가 4-10파일 수준이라 중규모로 판단했다.
- 인증 로직은 review-fix 사이클이 필요하다.
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
temporary spec의 실행 정보는 버리고, 구현되어 검증된 persistent repo-wide information만 global spec에 반영하세요.
```

## Example B: definition/docs overhaul

사용자 요청: `/autopilot docs/와 skill 계약을 thin global model로 재정렬`

```markdown
## Reasoning Trace

- 이번 작업의 대상은 `_sdd/spec/` active global spec이 아니라 docs definition layer와 skill surface다.
- consumer contract를 먼저 잠그고 downstream skill wording을 맞춘다.
- 전통적 테스트 프레임워크가 없으므로 inline diff/grep verification을 사용한다.
- Claude mirror drift를 리뷰 단계에서 강하게 점검한다.
```
