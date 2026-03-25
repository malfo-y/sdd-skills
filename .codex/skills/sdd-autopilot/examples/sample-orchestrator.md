# Sample Orchestrator

이 파일은 autopilot이 생성하는 오케스트레이터의 품질 기준 예시다.
완전한 장문 스펙이 아니라, reasoning과 파이프라인 구조가 어떻게 보여야 하는지 빠르게 감 잡기 위한 샘플만 남긴다.

---

## Example A: 중규모 기본형

사용자 요청: `/autopilot JWT 기반 인증 시스템 구현`

```markdown
# Orchestrator: JWT 인증 시스템

**생성일**: 2026-03-16T14:30:00
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

## Reasoning Trace

- 기존 글로벌 스펙이 존재하므로 autopilot 전제 조건을 만족한다.
- 영향 범위가 4-10파일 수준이라 중규모로 판단했다.
- `feature_draft`가 스펙 패치 초안과 구현 계획을 함께 제공하므로 `implementation_plan`은 생략했다.
- 인증 로직은 보안 리스크가 있으므로 `review-fix` 사이클을 포함했다.
- 테스트는 짧은 API/서비스 검증 중심이라 인라인 테스트 전략을 선택했다.

## Pipeline Steps

### Step 1: feature_draft
**에이전트**: `feature_draft`
**입력 파일**: (없음)
**출력 파일**: `_sdd/drafts/feature_draft_jwt_auth.md`

**프롬프트**:
JWT 기반 인증 시스템에 대한 feature draft를 작성하세요.
기존 스펙: `_sdd/spec/main.md`
사용자 원래 요청: "JWT 기반 인증 시스템 구현해줘. 로그인, 로그아웃, 토큰 갱신 포함."

### Step 2: implementation
**에이전트**: `implementation`
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
Feature draft: `_sdd/drafts/feature_draft_jwt_auth.md`
기존 스펙: `_sdd/spec/main.md`
TDD 방식으로 진행하세요.

### Step 3: review-fix loop
(autopilot 직접 관리)

### Step 4: spec_update_done
**에이전트**: `spec_update_done`
**입력 파일**: `_sdd/spec/main.md`, 구현된 코드 파일
**출력 파일**: `_sdd/spec/main.md`

**프롬프트**:
JWT 인증 시스템 구현 완료 기준으로 스펙을 실제 코드와 동기화하세요.
Feature draft: `_sdd/drafts/feature_draft_jwt_auth.md`
스펙 문서: `_sdd/spec/main.md`

## Review-Fix Loop

- **최대 반복**: 3회
- **종료 조건**: critical = 0 AND high = 0 AND medium = 0
- **수정 대상**: critical/high/medium

### Review 프롬프트
- 보안 취약점
- 에러 핸들링 완전성
- 기존 코드 패턴 일관성
- 테스트 커버리지
- severity를 critical/high/medium/low로 분류

### Fix 프롬프트
- critical/high/medium 이슈를 수정
- low는 로그 기록만

## Test Strategy

- **방식**: 인라인 디버깅
- **테스트 명령**: `npm test`
- **근거**: Express.js 테스트는 수 초 내 실행

## Error Handling

- **재시도 횟수**: 3회
- **핵심 단계**: `feature_draft`, `implementation`
- **비핵심 단계**: `spec_update_done`
```

### 대응 로그 예시

```markdown
# Pipeline Log: JWT 인증 시스템

## Meta
- **request**: "JWT 기반 인증 시스템 구현해줘. 로그인, 로그아웃, 토큰 갱신 포함."
- **orchestrator**: `.codex/skills/orchestrator_jwt_auth/SKILL.md`
- **started**: 2026-03-16T14:35:00
- **pipeline**: feature_draft -> implementation -> review-fix -> inline-test -> spec_update_done

## Status
| Step | Agent | Status | Output |
|------|-------|--------|--------|
| 1 | feature_draft | completed | `_sdd/drafts/feature_draft_jwt_auth.md` |
| 2 | implementation | completed | `6 files updated` |
| 3 | spec_update_done | completed | `_sdd/spec/main.md` |

## Execution Log

### feature_draft -- 완료
- **출력**: `_sdd/drafts/feature_draft_jwt_auth.md`
- **핵심 결정사항**:
  - access/refresh token 분리
  - 기존 User 모델 확장

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

- 기존 글로벌 스펙은 존재하지만, 이번 기능은 ML 파이프라인의 신규 섹션이 필요해 `spec_update_todo`를 선행한다.
- 영향 파일 수와 신규 컴포넌트 수가 모두 커서 대규모 변경으로 판단했다.
- 데이터/모델/학습 루프가 분리되고 병렬 실행 포인트가 있어 `implementation_plan`을 포함했다.
- 학습 명령 1회가 장시간이므로 인라인 테스트 대신 `ralph_loop_init` 기반 검증을 선택했다.
- 분산학습 회귀 위험이 높아 `review-fix` 사이클을 필수 단계로 둔다.
```

### Pipeline Steps 차이

```markdown
## Pipeline Steps

### Step 1: feature_draft
### Step 2: spec_update_todo
### Step 3: implementation_plan
### Step 4: implementation
### Step 5: review-fix loop
### Step 6: ralph-loop (Execute -> Verify)
### Step 7: spec_update_done
```

### 대규모에서 추가로 꼭 보여야 하는 계약

```markdown
### Step 6: ralph-loop (Execute -> Verify)

**Phase A-1: 설정 생성**
- 에이전트: `ralph_loop_init`
- 출력: `ralph/`

**Phase B-1: 설정 검증**
- `ralph/` 존재
- `ralph/config.sh` 존재
- `ralph/PROMPT.md` 존재
- `ralph/run.sh` 실행 가능
- `ralph/state.md` 존재
- `ralph/CHECKS.md` 존재

**Phase A-2: 실제 실행**
- 학습/디버깅 루프 실행

**Phase B-2: 실행 결과 검증**
- `ralph/state.md`의 phase == `DONE`
- iteration > 0
- 최종 결과 기록
- 실패 시 파이프라인 중단
```

### 대규모 로그에서 추가되는 핵심 엔트리

```markdown
### spec_update_todo -- 완료
- **출력**: `_sdd/spec/main.md`
- **핵심 결정사항**:
  - planned 상태로 ML 파이프라인 섹션 추가

### implementation_plan -- 완료
- **출력**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- **핵심 결정사항**:
  - 12개 태스크
  - 4개 병렬 가능

### ralph_loop_init -- 완료
- **출력**: `ralph/`
- **이슈**: 없음

### ralph-loop 실행 -- 완료
- **핵심 결정사항**:
  - 3 iterations 수행
  - val_accuracy 기록

## 최종 요약
- **Review 횟수**: 2회
- **테스트 결과**: ralph loop 완료
- **스펙 동기화**: 완료
```

---

## Reading Guide

- 중규모는 `feature_draft -> implementation -> review-fix -> spec_update_done`이 기본형이다.
- 대규모는 `spec_update_todo`, `implementation_plan`, `ralph_loop_init`가 추가되는 차이를 본다.
- 프롬프트 전문을 길게 복사하기보다, reasoning과 step contract가 보이면 충분하다.
