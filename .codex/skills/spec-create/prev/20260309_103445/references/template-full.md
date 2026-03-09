# Exploration-First Spec Template

This template keeps the legacy top-level headings for downstream skill compatibility,
but structures each section as an index for understanding and safe change.

Use Korean for the final spec unless the repository already uses another language.

---

# Main Spec Template

~~~markdown
# <Project Name>

> 이 저장소가 무엇을 하는지 한 줄로 설명

**Version**: X.Y.Z
**Last Updated**: YYYY-MM-DD
**Status**: [Draft | In Review | Approved | Deprecated]

## Goal

### Project Snapshot
- 해결하는 문제
- 주요 사용자 또는 운영자
- 핵심 가치

### Key Features
1. 기능 1
2. 기능 2
3. 기능 3

### Target Users / Use Cases
| 사용자 | 대표 사용 사례 | 우선순위 |
|--------|----------------|----------|
| 개발자 | ... | High |
| 운영자 | ... | Medium |

### Success Criteria
- [ ] 성공 기준 1
- [ ] 성공 기준 2

### Non-Goals (Out of Scope)
- 범위 밖 항목 1
- 범위 밖 항목 2

## Architecture Overview

### System Boundary
| In Scope | Out of Scope | Notes |
|----------|--------------|-------|
| 저장소가 책임지는 것 | 외부 시스템에 맡기는 것 | 경계 메모 |

### Repository Map
| 경로 | 역할 | 변경 시 왜 중요한가 |
|------|------|--------------------|
| `src/app/` | 애플리케이션 진입점 | 요청 흐름 시작 |
| `src/domain/` | 핵심 도메인 로직 | 규칙 변경 영향 큼 |
| `tests/` | 회귀 검증 | 수정 후 우선 확인 |

### Runtime Map

#### Primary Flow
```text
Client -> Router -> Service -> Repository -> DB
```

#### Secondary / Batch Flows
- 배치 작업 또는 이벤트 흐름
- 백그라운드 워커와 외부 연동

### Technology Stack
| Layer | Technology | Purpose |
|-------|------------|---------|
| Runtime | ... | ... |
| Framework | ... | ... |
| Storage | ... | ... |

### Cross-Cutting Invariants
- 항상 지켜야 하는 계약
- 상태 전이 제약
- 외부 API와의 호환 조건

## Component Details

### Component Index
| 컴포넌트 | 책임 | 주요 경로 | 핵심 심볼 / 진입점 | 관련 스펙 |
|---------|------|----------|--------------------|----------|
| Auth | 로그인/세션 | `src/auth/` | `AuthService`, `auth_router` | `auth.md` |
| Billing | 결제 처리 | `src/billing/` | `BillingService` | `billing.md` |

### Component: <Name>

#### Responsibility
- 하는 일
- 하지 않는 일

#### Owned Paths
- `src/...`
- `tests/...`

#### Key Symbols / Entry Points
- `ClassName.method()` - 설명
- `function_name()` - 설명

#### Interfaces / Contracts
**Inputs**
- 입력 데이터 또는 호출 형태

**Outputs**
- 출력 데이터 또는 부작용

**External Surfaces**
- 공개 API
- 이벤트
- 스키마

#### Dependencies
| Dependency | Direction | Why it matters |
|------------|-----------|----------------|
| DB | downstream | 영속화 |
| Auth middleware | upstream | 사용자 컨텍스트 |

#### Change Recipes
##### 새로운 기능 추가
- 보통 여기서 시작
- 함께 확인할 테스트/설정

##### 기존 동작 변경
- 영향 범위 확인 포인트
- 계약이 깨질 수 있는 지점

##### 장애 추적
- 로그/메트릭/재현 시작점

#### Tests / Observability
- 관련 테스트 파일
- 로그/메트릭/트레이싱 포인트

#### Risks / Invariants
- 이 컴포넌트에서 특히 조심할 점

#### Known Issues
- 현재 제한사항
- 예정된 개선

> 프로젝트가 큰 경우 main spec에는 `Component Index`와 짧은 요약만 두고,
> 상세 내용은 별도 컴포넌트 스펙 파일로 분리한다.

## Environment & Dependencies

### Directory Structure
```text
project/
├── src/
├── tests/
├── scripts/
└── ...
```

### Runtime / Tooling
- 런타임 버전
- 패키지 매니저
- 필수 서비스

### Setup Commands
```bash
# install
# bootstrap
```

### Test Commands
```bash
# unit tests
# integration tests
```

### Configuration / Secrets
| 항목 | 필수 여부 | 설명 |
|------|-----------|------|
| `DATABASE_URL` | Yes | DB 연결 |
| `REDIS_URL` | No | 캐시 |

## Identified Issues & Improvements

### Current Risks
- [ ] 현재 운영/구조상 위험

### Technical Debt
- [ ] 리팩터링 필요 지점

### Missing Coverage / Unknowns
- [ ] 테스트/문서 부족 영역

### Planned Improvements
- [ ] 다음 개선 후보

## Usage Examples

### Running the Project
```bash
# dev server
```

### Common Operations
- 자주 수행하는 작업
- 운영자가 자주 쓰는 명령

### Common Change Paths
- 새 API 추가 시: 먼저 볼 디렉토리와 테스트
- 기존 규칙 변경 시: 함께 봐야 하는 계약과 검증 지점
- 장애 분석 시: 로그/메트릭/재현 진입점

## Open Questions
- 확인되지 않은 사항
- 신뢰도가 낮은 추정
- 사용자 확인이 필요한 결정
~~~

---

# Component Spec Template

~~~markdown
# <Component Name>

## Responsibility
- 하는 일
- 하지 않는 일

## Owned Paths
- `src/...`
- `tests/...`

## Key Symbols / Entry Points
- `...`

## Interfaces / Contracts

### Inputs
- ...

### Outputs
- ...

### External Surfaces
- API / 이벤트 / 메시지 / 파일 포맷

## Dependencies
| Dependency | Direction | Why it matters |
|------------|-----------|----------------|
| ... | upstream/downstream | ... |

## Change Recipes

### Add a feature
- 어디서 시작하는가

### Change existing behavior
- 어떤 계약과 테스트를 함께 확인하는가

### Debug a failure
- 로그/메트릭/트레이싱 시작점

## Tests / Observability
- 관련 테스트 경로
- 운영 관측 포인트

## Risks / Invariants
- 깨지면 안 되는 조건

## Known Issues
- 현재 문제점

## Open Questions
- 확인이 필요한 내용
~~~

---

# Optional Extensions

If the project truly needs them, append concise sections from
`references/optional-sections.md`:
- Data Models
- API Surface
- Security
- Performance
- Deployment / Operations
