# Complex Project Spec Example

Use this example for a large project where the main spec acts as an index and
component files would usually hold the deeper details.

---

# E-Commerce Platform

> 상품 탐색, 주문, 결제를 처리하는 멀티서비스 전자상거래 플랫폼

## Goal

### Project Snapshot
- 사용자가 상품을 탐색하고 주문을 생성하며 결제를 완료할 수 있게 한다.
- 운영자는 카탈로그, 주문 상태, 결제 이슈를 관리한다.
- 여러 서비스가 분리되어 있지만 main spec에서 전체 흐름을 빠르게 파악할 수 있어야 한다.

### Key Features
1. 상품 카탈로그 조회와 검색
2. 장바구니 및 주문 생성
3. 결제 승인과 실패 처리
4. 재고 차감 및 주문 상태 전이
5. 운영자용 주문/환불 관리

### Target Users / Use Cases
| 사용자 | 사용 사례 | 우선순위 |
|--------|-----------|----------|
| 구매자 | 상품 탐색, 주문, 결제 | High |
| 운영자 | 주문 문제 처리, 환불, 재고 확인 | High |
| 내부 개발자 | 서비스별 기능 확장 | Medium |

### Success Criteria
- [ ] 주문 생성부터 결제 완료까지의 주요 흐름이 문서에서 한 번에 보인다.
- [ ] 신규 기능 담당자가 관련 서비스 시작 지점을 찾을 수 있다.
- [ ] 주문 상태 전이와 재고 차감 계약이 문서에 명시된다.

### Non-Goals (Out of Scope)
- 마켓플레이스 셀러 정산
- 개인화 추천 모델 설명

## Architecture Overview

### System Boundary
| In Scope | Out of Scope | Notes |
|----------|--------------|-------|
| 상품, 주문, 결제, 재고, 운영자 워크플로우 | 외부 PG 내부 동작, 물류 시스템 구현 | 외부 시스템과의 계약만 문서화 |

### Repository Map
| 경로 | 역할 | 변경 시 왜 중요한가 |
|------|------|--------------------|
| `services/catalog/` | 상품 조회와 검색 | 검색/정렬 변경 시작점 |
| `services/order/` | 주문 생성과 상태 전이 | 비즈니스 규칙 핵심 |
| `services/payment/` | 결제 승인/실패 처리 | 외부 PG 계약과 연결 |
| `services/inventory/` | 재고 예약과 차감 | 주문 성공 조건과 연결 |
| `libs/contracts/` | 서비스 간 DTO/이벤트 | 계약 변경 영향 범위 큼 |
| `ops/` | 배포/운영 스크립트 | 장애 대응과 운영 흐름 |
| `tests/` | 통합/E2E 검증 | 회귀 검증 기준 |

### Runtime Map

#### Primary Flow
```text
Buyer -> API Gateway -> Catalog -> Order -> Payment -> Inventory -> Order status update
```

#### Secondary / Batch Flows
- 결제 실패 재시도 작업이 스케줄러에서 실행된다.
- 재고 정합성 점검 배치가 주기적으로 실행된다.
- 주문 상태 변경 이벤트가 운영자 알림으로 전달된다.

### Technology Stack
| Layer | Technology | Purpose |
|-------|------------|---------|
| Services | Python / FastAPI | 서비스 구현 |
| Messaging | Kafka | 이벤트 전달 |
| Storage | PostgreSQL | 주문/카탈로그 저장 |
| Cache | Redis | 조회 성능 및 세션 |
| Operations | Kubernetes | 배포 및 운영 |

### Cross-Cutting Invariants
- 주문은 결제가 승인되기 전 `paid` 상태가 되면 안 된다.
- 재고 차감은 주문 승인 흐름과 원자적으로 맞물려야 한다.
- 서비스 간 이벤트 스키마는 `libs/contracts/`와 일치해야 한다.

## Component Details

### Component Index
| 컴포넌트 | 책임 | 주요 경로 | 핵심 심볼 / 진입점 | 관련 스펙 |
|---------|------|----------|--------------------|----------|
| Catalog | 상품 조회/검색 | `services/catalog/` | `catalog_router`, `CatalogService` | `catalog.md` |
| Order | 주문 생성/상태 전이 | `services/order/` | `OrderService`, `OrderStateMachine` | `order.md` |
| Payment | 결제 승인/실패 처리 | `services/payment/` | `PaymentService`, `PGClient` | `payment.md` |
| Inventory | 재고 예약/차감 | `services/inventory/` | `InventoryService` | `inventory.md` |
| Shared Contracts | DTO/이벤트 정의 | `libs/contracts/` | `OrderCreated`, `PaymentApproved` | main only |

### Component: Order

#### Responsibility
- 주문 생성, 상태 전이, 주문 조회를 담당한다.
- 결제 결과와 재고 결과를 받아 최종 상태를 확정한다.

#### Overview

##### 동작 개요
구매자가 주문을 생성하면 `pending` 상태로 시작하고,
결제 승인과 재고 확보 결과를 이벤트로 수신하여 상태를 전이한다.
결제와 재고 모두 성공하면 `confirmed`로, 어느 하나라도 실패하면
보상 로직을 거쳐 `cancelled`로 전이한다.
운영자는 주문 상태를 조회하고 수동으로 예외 처리를 수행할 수 있다.

##### 설계 의도
- 상태 머신 패턴: 주문 상태 전이를 `OrderStateMachine`으로 캡슐화하여
  허용되지 않는 전이(예: `shipped` → `pending`)를 코드 수준에서 차단한다.
  상태 규칙이 서비스 로직에 흩어지지 않아 전이 정책을 한 곳에서 관리할 수 있다.
- 이벤트 기반 협력: 결제/재고 서비스와 직접 호출 대신 Kafka 이벤트로
  통신하여 서비스 간 결합도를 낮춘다. 이벤트 소비 실패 시 DLQ를 통해
  운영자가 재처리할 수 있도록 한다.

#### Owned Paths
- `services/order/app/`
- `services/order/domain/`
- `services/order/tests/`
- `libs/contracts/order/`

#### Key Symbols / Entry Points
- `OrderService.create_order()`
- `OrderService.mark_paid()`
- `OrderStateMachine.transition()`
- `POST /orders`

#### Interfaces / Contracts
**Inputs**
- 구매자 주문 요청
- `PaymentApproved`, `PaymentFailed`
- `InventoryReserved`, `InventoryRejected`

**Outputs**
- 주문 레코드 생성
- 주문 상태 변경 이벤트 발행

**External Surfaces**
- 주문 생성/조회 API
- Kafka 주문 상태 이벤트

#### Dependencies
| Dependency | Direction | Why it matters |
|------------|-----------|----------------|
| Catalog | upstream | 상품 정보 검증 |
| Payment | downstream | 결제 결과에 따라 상태 전이 |
| Inventory | downstream | 재고 확보 실패 시 주문 취소 |
| `libs/contracts/` | shared | 이벤트/DTO 계약 유지 |

#### Change Recipes
##### 새로운 기능 추가
- 주문 요청 필드를 추가하면 `libs/contracts/` -> API 스키마 -> `OrderService` -> 통합 테스트 순서로 본다.

##### 기존 동작 변경
- 상태 전이 규칙을 바꾸면 `OrderStateMachine`과 결제/재고 이벤트 처리, 운영자 화면 의존성을 함께 본다.

##### 장애 추적
- 주문이 `pending`에서 멈추면 상태 전이 로그, 결제 이벤트 소비 상태, 재고 이벤트 수신 여부를 순서대로 확인한다.

#### Tests / Observability
- `services/order/tests/unit/`
- `services/order/tests/integration/`
- 주문 상태 전이 로그, 이벤트 컨슈머 lag, 실패 DLQ를 운영 지표로 본다.

#### Risks / Invariants
- 중복 결제 승인 이벤트가 와도 주문 상태는 한 번만 확정되어야 한다.
- 재고 실패 후 결제 성공 보상 로직이 누락되면 정합성이 깨진다.

#### Known Issues
- 주문 생성 API의 멱등성 정책이 문서로 완전히 정리되어 있지 않다.
- 일부 운영자 수동 처리 흐름이 코드와 문서에서 분산되어 있다.

## Environment & Dependencies

### Directory Structure
```text
ecommerce/
├── services/
│   ├── catalog/
│   ├── order/
│   ├── payment/
│   └── inventory/
├── libs/
│   └── contracts/
├── ops/
└── tests/
```

### Runtime / Tooling
- Python 3.11
- Poetry
- PostgreSQL
- Redis
- Kafka
- Kubernetes

### Setup Commands
```bash
poetry install
docker compose up -d postgres redis kafka
make dev
```

### Test Commands
```bash
make test-unit
make test-integration
make test-e2e
```

### Configuration / Secrets
| 항목 | 필수 여부 | 설명 |
|------|-----------|------|
| `DATABASE_URL` | Yes | 주문/카탈로그 DB |
| `KAFKA_BROKERS` | Yes | 이벤트 브로커 |
| `PG_API_KEY` | Yes | 외부 PG 인증 |
| `REDIS_URL` | Yes | 캐시/세션 |

## Identified Issues & Improvements

### Current Risks
- [ ] 주문/결제/재고 간 보상 흐름이 한 문단에 요약되어 있지만 세부 runbook은 분리 필요하다.
- [ ] 일부 이벤트 스키마 변경 이력이 `DECISION_LOG.md` 없이 PR에만 남아 있다.

### Technical Debt
- [ ] 서비스 간 계약 테스트가 부분적으로만 자동화되어 있다.
- [ ] 운영자 수동 복구 절차가 `ops/`와 위키에 분산되어 있다.

### Missing Coverage / Unknowns
- [ ] 주문 멱등성 정책의 서비스별 구현 차이가 완전히 정리되지 않았다.
- [ ] PG 장애 시 재시도 한계와 운영 개입 기준이 명확하지 않다.

### Planned Improvements
- [ ] `order.md`, `payment.md`, `inventory.md`로 컴포넌트 스펙 분리
- [ ] 공통 이벤트 계약과 상태 전이 표를 자동 생성

## Usage Examples

### Running the Project
```bash
make dev
```

### Common Operations
- 로컬에서 전체 서비스 기동
- 계약 테스트 실행
- 특정 서비스만 재시작

### Common Change Paths
- 새 주문 필드를 추가할 때: `libs/contracts/` -> `services/order/` -> `services/payment/` -> 통합 테스트
- 결제 실패 정책을 바꿀 때: `services/payment/` -> `services/order/` 상태 전이 -> 운영자 처리 흐름 -> E2E 테스트
- 재고 불일치 장애를 볼 때: `services/inventory/` 로그 -> 주문 이벤트 -> 보상 처리 -> 배치 정합성 점검 순서 확인

## Open Questions
- 주문 멱등성 키의 표준 저장 위치가 서비스별로 통일되어 있는지 확인이 더 필요하다.
- 운영자 수동 환불 절차를 main spec에 둘지 `payment.md`로 분리할지 결정이 필요하다.
