# Simple Project Spec Example

Use this example for a small project where one main spec file is enough.

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

### Target Users / Use Cases
| 사용자 | 사용 사례 | 우선순위 |
|--------|-----------|----------|
| 백엔드 개발자 | 다른 서비스에서 단축 URL 생성 API 호출 | High |
| 콘텐츠 운영자 | 공유 링크 추적 | Medium |

### Success Criteria
- [ ] 중복 없는 짧은 코드 생성
- [ ] 리다이렉트 성공률 유지
- [ ] 기본 조회 API 응답 제공

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

### Technology Stack
| Layer | Technology | Purpose |
|-------|------------|---------|
| Runtime | Python 3.11 | 서비스 구현 |
| Framework | FastAPI | HTTP API |
| Storage | SQLite | 기본 영속화 |
| Cache | Redis | 조회 캐시 |

### Cross-Cutting Invariants
- 단축 코드는 한 번 발급되면 재사용 규칙이 명확해야 한다.
- 리다이렉트 응답은 원본 URL 검증 규칙을 우회하면 안 된다.

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

#### Overview

##### 동작 개요
사용자가 긴 URL을 전달하면 고유한 단축 코드를 생성하여 저장하고,
짧은 URL을 반환한다. 이후 단축 코드로 접근하면 원본 URL로
리다이렉트하며, 이 과정에서 클릭 수를 자동으로 집계한다.
조회 시에는 Redis 캐시를 먼저 확인하고, 캐시 미스 시 DB에서
조회한 뒤 캐시를 갱신한다.

##### 설계 의도
- 캐시 우선 조회: 리다이렉트는 읽기 빈도가 쓰기보다 압도적으로 높으므로,
  Redis 캐시를 앞단에 두어 DB 부하를 줄인다.
- 저장소 분리: `URLRepository`를 별도 계층으로 분리하여
  SQLite에서 다른 DB로 교체할 때 서비스 로직 변경 없이 저장소만
  교체할 수 있도록 한다.

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

## Environment & Dependencies

### Directory Structure
```text
url-shortener/
├── src/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── repositories/
│   └── models/
├── tests/
└── requirements.txt
```

### Runtime / Tooling
- Python 3.11
- pip
- Redis (optional in local dev)

### Setup Commands
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### Test Commands
```bash
pytest
pytest tests/test_url_service.py
```

### Configuration / Secrets
| 항목 | 필수 여부 | 설명 |
|------|-----------|------|
| `DATABASE_URL` | Yes | DB 연결 |
| `REDIS_URL` | No | 조회 캐시 |
| `BASE_URL` | Yes | 생성 URL의 호스트 |

## Identified Issues & Improvements

### Current Risks
- [ ] 단축 코드 충돌 처리 정책이 문서로 명확하지 않다.

### Technical Debt
- [ ] 저장소 계층과 서비스 계층의 에러 구분이 약하다.

### Missing Coverage / Unknowns
- [ ] 캐시 비활성화 환경 테스트가 부족하다.

### Planned Improvements
- [ ] 만료 링크
- [ ] 커스텀 단축 코드

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
