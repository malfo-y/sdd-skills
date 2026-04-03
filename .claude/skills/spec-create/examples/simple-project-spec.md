# Simple Project Spec Example

Example of a small global spec under the current SDD canonical model.

---

# URL Shortener

> 긴 URL을 짧은 링크로 바꾸고 해석하는 API-first 서비스

**Version**: 1.0.0
**Last Updated**: 2026-04-04
**Status**: Draft

## 1. 배경 및 high-level concept

긴 링크는 공유성과 추적성이 떨어진다. 특히 내부 운영 도구나 캠페인 링크는 간단한 생성 API와 클릭 추적을 함께 필요로 한다.

이 프로젝트의 high-level concept는 "짧은 링크 생성과 해석을 하나의 작은 도메인 서비스로 분리해, 생성 규칙과 추적 정책을 중앙에서 고정한다"는 것이다.

## 2. Scope / Non-goals / Guardrails

### In Scope

- 긴 URL을 짧은 코드로 변환
- 짧은 코드를 원본 URL로 해석
- 클릭 수 집계

### Non-goals

- 사용자별 권한 관리
- 마케팅 대시보드
- 커스텀 도메인 호스팅

### Guardrails

- short code 생성 규칙은 결정론적 재시도 정책을 가져야 한다.
- redirect 경로는 해석 실패 시 무한 redirect를 만들면 안 된다.

## 3. 핵심 설계와 주요 결정

짧은 링크 생성 로직은 API 라우터에서 직접 처리하지 않고 `URL Service`에 모은다. 이렇게 해야 REST, CLI, 배치 재생성 작업이 같은 shortening 규칙과 tracking 규칙을 공유할 수 있다.

| Decision | Why | What Must Stay True |
|----------|-----|---------------------|
| shortening logic를 service layer에 둔다 | 재사용성과 테스트성을 확보하기 위해 | API layer는 orchestration만 담당 |
| click tracking은 resolve 경로와 같은 도메인 안에 둔다 | 해석과 추적을 분리하면 누락 위험이 커지기 때문에 | resolve 성공 시 tracking contract가 유지 |

## 4. Contract / Invariants / Verifiability

### Contract

| ID | Subject | Inputs/Outputs | Preconditions | Postconditions | Failure Guarantees |
|----|---------|----------------|---------------|----------------|--------------------|
| C1 | Shorten URL | long URL -> short URL | 입력 URL이 유효해야 한다 | 고유한 short code가 발급된다 | 충돌 시 재시도 후 명시적 실패를 반환한다 |
| C2 | Resolve URL | short code -> target URL | short code가 존재해야 한다 | target URL로 redirect 가능하다 | 존재하지 않으면 fallback error response를 반환한다 |

### Invariants

| ID | Scope | Invariant | Why It Matters |
|----|-------|-----------|----------------|
| I1 | URL mapping | 하나의 short code는 하나의 target URL에만 연결된다 | redirect 의미가 흔들리면 안 된다 |
| I2 | Tracking | resolve 성공 경로는 click tracking과 분리되지 않는다 | 통계 누락을 막아야 한다 |

### Verifiability

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | test | shortening collision과 uniqueness 테스트 |
| V2 | C2, I2 | review, test | resolve + tracking flow 리뷰 및 redirect 테스트 |

## 5. 사용 가이드 & 기대 결과

### Scenario: 기본 링크 생성

**Setup**: 사용자가 긴 URL을 API에 보낸다.

**Action**: `POST /shorten` 호출

**Expected Result**: 짧은 URL이 반환되고 이후 `GET /{code}`에서 원본 URL로 이동한다.

## 6. Decision-bearing structure

- 시스템 경계: 링크 생성/해석/추적까지를 담당하고 대시보드는 포함하지 않는다.
- ownership: API layer는 request handling, service layer는 shortening contract, storage layer는 mapping persistence를 담당한다.
- cross-component contract: API는 service가 반환한 short code와 failure reason을 그대로 노출한다.
- extension point: custom code policy, expiration policy
- invariant hotspot: code generation, resolve path

## 7. 참조 정보

### Environment & Dependencies

- Python 3.11
- FastAPI
- SQLAlchemy
- Redis (optional cache)

## Appendix A. Strategic Code Map

| Kind | Path / Symbol | Why It Matters |
|------|----------------|----------------|
| Entrypoint | `src/main.py:create_app` | API wiring 진입점 |
| Invariant Hotspot | `src/services/url_service.py:generate_short_code` | uniqueness invariant 핵심 |
| Change Hotspot | `src/services/url_service.py:resolve_url` | redirect + tracking contract 핵심 |
