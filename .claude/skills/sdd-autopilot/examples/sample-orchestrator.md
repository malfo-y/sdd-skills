# Sample Orchestrator -- 중규모 인증 시스템 예시

이 파일은 autopilot이 생성하는 오케스트레이터의 완성된 예시다.
사용자가 "/autopilot JWT 기반 인증 시스템 구현"을 요청한 경우의 중규모 오케스트레이터이다.

> autopilot은 이 예시를 참조하여 실제 오케스트레이터를 생성한다.

---

## 생성된 오케스트레이터 예시

```markdown
# Orchestrator: JWT 인증 시스템

**생성일**: 2026-03-16T14:30:00
**규모**: 중규모
**생성자**: autopilot

## 기능 설명

JWT 기반 인증 시스템을 구현한다. 로그인, 로그아웃, 토큰 갱신 기능을 포함한다.

### 구체화된 요구사항
- JWT 기반 Bearer 토큰 인증
- 로그인 엔드포인트 (email + password)
- 로그아웃 엔드포인트 (토큰 무효화)
- 토큰 갱신 엔드포인트 (refresh token)
- Access token 만료 시간: 1시간
- Refresh token 만료 시간: 7일
- 비밀번호 해싱 (bcrypt)

### 제약 조건
- 기존 Express.js 프레임워크 사용
- 기존 User 모델 확장 (새 모델 생성하지 않음)
- 기존 미들웨어 패턴을 따를 것

## Pipeline Steps

### Step 1: feature-draft

**에이전트**: feature-draft
**입력 파일**: (없음)
**출력 파일**: `_sdd/drafts/feature_draft_jwt_auth.md`

**프롬프트**:
다음 기능에 대한 feature draft를 작성하세요: JWT 기반 인증 시스템

요구사항:
- JWT 기반 Bearer 토큰 인증
- 로그인 엔드포인트 (email + password)
- 로그아웃 엔드포인트 (토큰 무효화)
- 토큰 갱신 엔드포인트 (refresh token)
- Access token 만료 시간: 1시간
- Refresh token 만료 시간: 7일
- 비밀번호 해싱 (bcrypt)

제약 조건:
- 기존 Express.js 프레임워크 사용
- 기존 User 모델 확장 (새 모델 생성하지 않음)
- 기존 미들웨어 패턴을 따를 것

기존 스펙 문서: `_sdd/spec/main.md`
기존 코드베이스 구조:
```
src/
  models/user.js
  routes/index.js
  middleware/error-handler.js
  config/database.js
test/
  models/user.test.js
```

사용자 원래 요청: "JWT 기반 인증 시스템 구현해줘. 로그인, 로그아웃, 토큰 갱신 포함."

### Step 2: implementation-plan

**에이전트**: implementation-plan
**입력 파일**: `_sdd/drafts/feature_draft_jwt_auth.md`
**출력 파일**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

**프롬프트**:
다음 feature draft를 기반으로 구현 계획을 작성하세요.

Feature draft: `_sdd/drafts/feature_draft_jwt_auth.md`
기존 스펙: `_sdd/spec/main.md`

주의사항:
- 기존 Express.js 패턴을 따르세요
- 기존 User 모델을 확장하세요
- 병렬 실행 가능한 태스크를 식별하고 Target Files를 명시하세요

사용자 원래 요청: "JWT 기반 인증 시스템 구현해줘. 로그인, 로그아웃, 토큰 갱신 포함."

### Step 3: implementation

**에이전트**: implementation
**입력 파일**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
**출력 파일**: 코드 파일 (예상 6-8개)
  - `src/middleware/auth.js` (인증 미들웨어)
  - `src/routes/auth.js` (인증 라우트)
  - `src/services/auth-service.js` (인증 서비스)
  - `src/services/token-service.js` (토큰 관리)
  - `src/models/user.js` (모델 확장)
  - `test/services/auth-service.test.js`
  - `test/routes/auth.test.js`

**프롬프트**:
구현 계획을 실행하세요.

구현 계획: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

TDD 방식으로 진행하세요:
1. 테스트 먼저 작성
2. 코드 구현
3. 테스트 통과 확인

사용자 원래 요청: "JWT 기반 인증 시스템 구현해줘. 로그인, 로그아웃, 토큰 갱신 포함."

### Step 4: review-fix loop

(autopilot이 직접 관리 -- 아래 Review-Fix Loop 섹션 참조)

### Step 5: spec-update-done

**에이전트**: spec-update-done
**입력 파일**: `_sdd/spec/main.md`, 구현된 코드 파일
**출력 파일**: `_sdd/spec/main.md` (업데이트)

**프롬프트**:
JWT 인증 시스템 구현이 완료되었습니다. 스펙 문서를 실제 구현과 동기화하세요.

스펙 문서: `_sdd/spec/main.md`
구현 계획: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
Feature draft: `_sdd/drafts/feature_draft_jwt_auth.md`

구현된 주요 파일:
- `src/middleware/auth.js`
- `src/routes/auth.js`
- `src/services/auth-service.js`
- `src/services/token-service.js`
- `src/models/user.js` (확장)

추가된 기능: JWT 인증 (로그인/로그아웃/토큰갱신)

사용자 원래 요청: "JWT 기반 인증 시스템 구현해줘. 로그인, 로그아웃, 토큰 갱신 포함."

## Review-Fix Loop

- **최대 반복**: 3회
- **종료 조건**: critical = 0 AND high = 0
- **수정 대상**: critical/high만 (medium/low는 로그 기록)

### Review 프롬프트:
구현 결과를 리뷰하세요.

구현 계획: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

리뷰 대상 파일:
- `src/middleware/auth.js`
- `src/routes/auth.js`
- `src/services/auth-service.js`
- `src/services/token-service.js`
- `src/models/user.js`
- `test/services/auth-service.test.js`
- `test/routes/auth.test.js`

특히 확인할 사항:
- 보안 취약점 (토큰 검증, 비밀번호 해싱)
- 에러 핸들링 완전성
- 기존 코드 패턴과의 일관성
- 테스트 커버리지

리뷰 결과에 critical/high/medium/low 심각도를 반드시 포함하세요.

### Fix 프롬프트 (critical/high 이슈 발견 시):
리뷰에서 발견된 critical/high 이슈를 수정하세요.

리뷰 리포트: <리뷰 결과>

수정 대상 이슈:
- <critical/high 이슈 목록>

medium/low 이슈는 무시하세요.

## Test Strategy

- **방식**: 인라인 디버깅
- **테스트 명령**: `npm test`
- **최대 재시도**: 5회
- **근거**: Express.js 단위/통합 테스트는 수 초 내 실행

### 테스트 프롬프트:
구현된 인증 시스템의 테스트를 실행하고, 실패하는 테스트가 있으면 수정하세요.

테스트 명령: `npm test`
테스트 파일:
- `test/services/auth-service.test.js`
- `test/routes/auth.test.js`

테스트 통과까지 수정-재실행 루프를 반복하세요 (최대 5회).

## Error Handling

- **재시도 횟수**: 3회
- **핵심 단계**: feature-draft, implementation-plan, implementation
  - 이 단계가 실패하면 파이프라인을 중단하고 사용자에게 보고
- **비핵심 단계**: spec-update-done
  - 실패 시 건너뛰고 로그에 기록, 사용자에게 수동 스펙 동기화 안내
```

---

## 대응하는 로그 파일 예시

위 오케스트레이터 실행 시 생성되는 로그 파일의 예시:

```markdown
# Pipeline Log: JWT 인증 시스템

**시작**: 2026-03-16T14:35:00
**규모**: 중규모
**파이프라인**: feature-draft -> implementation-plan -> implementation -> review-fix -> inline-test -> spec-update-done
**오케스트레이터**: _sdd/pipeline/orchestrator_jwt_auth_20260316_143000.md

## 실행 로그

### feature-draft -- 완료
- **시간**: 14:35:00 ~ 14:37:30 (2분 30초)
- **출력**: `_sdd/drafts/feature_draft_jwt_auth.md`
- **핵심 결정사항**:
  - JWT 토큰 구조: access token + refresh token 분리
  - 토큰 저장: refresh token은 DB에 저장하여 무효화 지원
  - 비밀번호 해싱: bcrypt (salt rounds: 12)
- **이슈**: 없음

### implementation-plan -- 완료
- **시간**: 14:37:30 ~ 14:39:15 (1분 45초)
- **출력**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- **핵심 결정사항**:
  - 7개 태스크로 분할 (3개 병렬 가능)
  - TDD 방식 채택
  - 기존 User 모델에 password_hash, refresh_token 필드 추가
- **이슈**: 없음

### implementation -- 완료
- **시간**: 14:39:15 ~ 14:48:00 (8분 45초)
- **출력**: 7개 파일 생성/수정
- **핵심 결정사항**:
  - jsonwebtoken 라이브러리 사용
  - 미들웨어 패턴: req.user에 디코딩된 토큰 정보 저장
  - 에러 코드: AUTH_001 ~ AUTH_005 체계
- **이슈**: 없음

### review-fix -- Round 1/3
- **리뷰 결과**: critical 1건, high 1건, medium 2건, low 1건
- **수정 대상**:
  - [critical] refresh token 갱신 시 이전 토큰 무효화 누락
  - [high] 비밀번호 비교 시 timing attack 취약점
- **수정 결과**: 완료

### review-fix -- Round 2/3
- **리뷰 결과**: critical 0건, high 0건, medium 2건, low 1건
- **종료**: critical/high = 0 -> 리뷰 통과
- **로그된 minor 이슈**:
  - [medium] 에러 메시지 국제화 미지원
  - [medium] rate limiting 미적용
  - [low] 로그 레벨 일관성

### 인라인 테스트 -- 완료
- **시간**: 14:52:00 ~ 14:53:30 (1분 30초)
- **테스트 결과**: 18/18 통과
- **재시도**: 1회 (초기 실행 시 2건 실패 -> 수정 후 통과)

### spec-update-done -- 완료
- **시간**: 14:53:30 ~ 14:55:00 (1분 30초)
- **출력**: `_sdd/spec/main.md` 업데이트
- **핵심 결정사항**:
  - Component Details에 "인증 시스템" 섹션 추가
  - API Reference에 auth 엔드포인트 3개 추가
- **이슈**: 없음

## 최종 요약
- **완료 시간**: 2026-03-16T14:55:00
- **총 소요 시간**: 20분
- **실행 결과**: 성공
- **생성/수정 파일 수**: 7개
- **Review 횟수**: 2회 (Round 2에서 통과)
- **테스트 결과**: 통과 18/18
- **스펙 동기화**: 완료
- **잔여 이슈**: medium 2건, low 1건 (로그에 기록)
```
