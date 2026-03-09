# Simple Project Spec Example

Use this example for a small project where one main spec file is enough.
This version stays close to the MUST sections and keeps only one optional
section that materially helps maintenance.

---

# URL Shortener

> 긴 URL을 짧은 공유 링크로 변환하고 조회하는 API 서비스

## Goal

### Project Snapshot
- 긴 URL을 짧은 코드로 변환한다.
- 짧은 코드를 원본 URL로 리다이렉트한다.
- 기본 클릭 수 집계를 제공한다.

### Key Features
1. 긴 URL을 짧은 URL로 생성
2. 짧은 코드 조회 및 리다이렉트
3. 클릭 수 증가 및 조회
4. API 중심 사용 방식

### Non-Goals (Out of Scope)
- 사용자별 대시보드
- 광고 추적 플랫폼 수준의 분석 기능

## Architecture Overview

### System Boundary
| In Scope | Out of Scope | Notes |
|----------|--------------|-------|
| 단축 URL 생성/조회 | 고급 분석, 계정 관리 | 현재는 API 핵심 기능에 집중 |

### Repository Map
| 경로 | 역할 | 변경 시 왜 중요한가 |
|------|------|--------------------|
| `src/main.py` | FastAPI 진입점 | 라우팅 시작점 |
| `src/routes/` | API 엔드포인트 | 요청 계약 변경 지점 |
| `src/services/url_service.py` | 단축/조회 핵심 로직 | 규칙 변경 영향이 큼 |
| `src/models/` | 저장 모델 | 스키마 변경 확인 필요 |
| `tests/` | 회귀 테스트 | 수정 후 우선 확인 |

### Runtime Map

#### Primary Flow
```text
Client -> FastAPI route -> URLService -> URLRepository -> SQLite
```

#### Secondary / Batch Flows
- 조회 시 Redis 캐시가 있으면 먼저 확인하고, 없으면 DB 조회 후 캐시를 갱신한다.

## Component Details

### Component Index
| 컴포넌트 | 책임 | 주요 경로 | 핵심 심볼 / 진입점 | 관련 스펙 |
|---------|------|----------|--------------------|----------|
| API Layer | 요청 수신/검증 | `src/routes/` | `shorten_url`, `redirect_url` | main only |
| URL Service | 단축 코드 생성과 조회 | `src/services/url_service.py` | `URLService` | main only |
| Persistence | URL 저장 및 조회 | `src/models/`, `src/repositories/` | `URLRepository` | main only |

### Component: URL Service

#### Responsibility
- 긴 URL을 받아 단축 코드를 생성한다.
- 짧은 코드를 받아 원본 URL을 조회한다.
- 클릭 수 업데이트를 조정한다.

#### Owned Paths
- `src/services/url_service.py`
- `src/repositories/url_repository.py`
- `tests/test_url_service.py`

#### Key Symbols / Entry Points
- `URLService.create_short_url()`
- `URLService.resolve_short_code()`
- `URLService.increment_click_count()`

#### Interfaces / Contracts
**Inputs**
- 긴 URL 문자열
- 단축 코드 문자열

**Outputs**
- 생성된 짧은 URL
- 리다이렉트 대상 원본 URL

**External Surfaces**
- `POST /api/shorten`
- `GET /{short_code}`

#### Dependencies
| Dependency | Direction | Why it matters |
|------------|-----------|----------------|
| `URLRepository` | downstream | URL 저장/조회 |
| Redis cache | downstream | 조회 성능 |

#### Change Recipes
##### 새로운 기능 추가
- 커스텀 단축 코드가 필요하면 `URLService.create_short_url()`과 충돌 검사를 먼저 확인한다.

##### 기존 동작 변경
- 코드 생성 규칙을 바꾸면 기존 링크 호환성과 저장 스키마를 함께 본다.

##### 장애 추적
- 리다이렉트 실패 시 라우터 입력 검증, 캐시 조회, 저장소 조회 순서로 본다.

#### Tests / Observability
- `tests/test_url_service.py`
- `tests/test_redirect.py`
- 요청 로그에서 `short_code`, `cache_hit` 여부를 우선 확인한다.

#### Risks / Invariants
- 같은 URL이라도 중복 발급 정책이 명확해야 한다.
- 충돌 처리 실패 시 다른 URL이 잘못 연결될 수 있다.

#### Known Issues
- 커스텀 코드 기능이 없다.
- 만료 정책이 없다.

## Usage Examples

### Running the Project
```bash
uvicorn src.main:app --reload
```

### Common Operations
- 새 링크 생성 API 호출
- 특정 단축 코드 조회

### Common Change Paths
- 새 응답 필드를 추가할 때: `src/routes/` -> `URLService` -> 응답 스키마 -> `tests/`
- 코드 생성 규칙을 바꿀 때: `URLService.create_short_url()` -> 충돌 검사 -> 기존 데이터 호환성 테스트
- 리다이렉트 문제를 볼 때: 입력 검증 -> 캐시 조회 -> 저장소 조회 -> 클릭 수 증가 순서 확인

## Open Questions
- 프로덕션에서 SQLite 대신 어떤 DB를 표준으로 사용할지 미정이다.
- 클릭 수 집계를 동기 처리할지 비동기 처리할지 정책이 없다.
