# Complex Project Spec Example

Use this template for larger projects with multiple components, integrations, and teams.

---

# E-Commerce Platform

**Version**: 2.0.0
**Last Updated**: 2024-01-15
**Status**: In Development

## Goal

Build a scalable e-commerce platform supporting multi-vendor marketplace operations with real-time inventory, order management, and payment processing.

### Key Features
1. Multi-vendor marketplace with vendor onboarding
2. Real-time inventory synchronization
3. Multi-currency payment processing
4. Order lifecycle management
5. Customer reviews and ratings
6. Search with faceted filtering
7. Recommendation engine
8. Admin dashboard

### Target Users

| User Type | Use Case |
|-----------|----------|
| Customers | Browse, purchase, track orders |
| Vendors | List products, manage inventory, fulfill orders |
| Admins | Platform management, analytics, support |

### Success Criteria
- [ ] Handle 10,000 concurrent users
- [ ] 99.9% uptime SLA
- [ ] <200ms API response time (p95)
- [ ] PCI-DSS compliance for payments

### Non-Goals
- Physical store POS integration
- B2B wholesale features
- Subscription/recurring billing

## Architecture Overview

### System Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Client Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Web App    │  │  Mobile App  │  │  Vendor App  │              │
│  │   (React)    │  │   (React     │  │   (React)    │              │
│  │              │  │    Native)   │  │              │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
└─────────┼─────────────────┼─────────────────┼───────────────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────────┐
│                           ▼                                          │
│  ┌─────────────────────────────────────────────────────┐            │
│  │              API Gateway (Kong)                      │            │
│  │    Rate Limiting │ Auth │ Load Balancing            │            │
│  └─────────────────────────────────────────────────────┘            │
│                           │                                          │
│            ┌──────────────┼──────────────┐                          │
│            ▼              ▼              ▼                          │
│     ┌────────────┐ ┌────────────┐ ┌────────────┐                   │
│     │  Product   │ │   Order    │ │   User     │                   │
│     │  Service   │ │  Service   │ │  Service   │                   │
│     │  (Python)  │ │  (Python)  │ │  (Python)  │                   │
│     └─────┬──────┘ └─────┬──────┘ └─────┬──────┘                   │
│           │              │              │                           │
│     ┌─────┴──────┐ ┌─────┴──────┐ ┌─────┴──────┐                   │
│     │  Payment   │ │ Inventory  │ │Notification│                   │
│     │  Service   │ │  Service   │ │  Service   │                   │
│     │  (Python)  │ │  (Python)  │ │  (Python)  │                   │
│     └────────────┘ └────────────┘ └────────────┘                   │
└─────────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────────┐
│                           ▼                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ PostgreSQL │  │   Redis    │  │Elasticsearch│ │    S3      │   │
│  │  (Orders,  │  │  (Cache,   │  │  (Search)   │ │  (Media)   │   │
│  │   Users)   │  │  Sessions) │  │             │ │            │   │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
│                                                                      │
│  ┌────────────┐  ┌────────────┐                                     │
│  │   Kafka    │  │ TimescaleDB│                                     │
│  │  (Events)  │  │ (Analytics)│                                     │
│  └────────────┘  └────────────┘                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Service Communication

| Source | Destination | Protocol | Purpose |
|--------|-------------|----------|---------|
| Gateway | All Services | REST/gRPC | API requests |
| Services | Kafka | Async | Event publishing |
| Services | Redis | TCP | Caching, sessions |
| Order | Payment | gRPC | Payment processing |

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Frontend | React | 18.x | Web application |
| Mobile | React Native | 0.72 | iOS/Android apps |
| Gateway | Kong | 3.x | API management |
| Backend | Python/FastAPI | 3.11/0.100 | Microservices |
| Database | PostgreSQL | 15 | Primary data store |
| Cache | Redis | 7.x | Caching, sessions |
| Search | Elasticsearch | 8.x | Product search |
| Queue | Kafka | 3.x | Event streaming |
| Storage | S3 | - | Media files |

## Component Details

### Component: Product Service

#### Overview
Manages product catalog, categories, and vendor listings.

#### Responsibilities
- CRUD operations for products
- Category management
- Vendor product association
- Price and inventory sync triggers

#### Interface

**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| GET | /products | List products (paginated) |
| POST | /products | Create product |
| GET | /products/{id} | Get product details |
| PUT | /products/{id} | Update product |
| DELETE | /products/{id} | Delete product |
| GET | /products/search | Search products |
| POST | /products/{id}/images | Upload images |

**Events Published:**
- `product.created` - New product added
- `product.updated` - Product modified
- `product.deleted` - Product removed
- `product.price_changed` - Price update

#### Implementation Details

**Key Files:**
- `services/product/src/main.py` - FastAPI app
- `services/product/src/models/` - SQLAlchemy models
- `services/product/src/api/` - Route handlers
- `services/product/src/events/` - Kafka publishers

**Design Patterns:**
- Repository pattern for data access
- CQRS for read/write separation
- Event sourcing for audit trail

#### Dependencies

| Service | Type | Purpose |
|---------|------|---------|
| PostgreSQL | Database | Product storage |
| Elasticsearch | Search | Full-text search |
| S3 | Storage | Product images |
| Kafka | Queue | Event publishing |
| Inventory Service | Internal | Stock levels |

#### Error Handling

| Error | HTTP | Handling |
|-------|------|----------|
| ProductNotFound | 404 | Return error with ID |
| ValidationError | 400 | Return field errors |
| DuplicateSKU | 409 | Conflict response |

---

### Component: Order Service

#### Overview (MUST — prose 권장)

주문이 생성되면 Order Service는 Saga 패턴을 통해 재고 예약 → 결제 처리 → 주문 확정 → 판매자 알림의 4단계를 순차 실행한다. 어느 단계에서든 실패하면 이전 단계를 역순으로 보상(compensate)하여 데이터 정합성을 보장한다. 주문 상태는 Draft → Pending → Confirmed → Shipped → Delivered의 상태 머신으로 관리되며, 각 전이마다 Kafka 이벤트를 발행해 다른 서비스(Inventory, Notification)가 비동기로 반응할 수 있게 한다.

이 설계를 선택한 이유는 두 가지다. 첫째, 마이크로서비스 간 분산 트랜잭션에서 2PC(Two-Phase Commit)는 성능 병목과 단일 장애점을 만들지만, Saga는 각 서비스가 독립적으로 커밋/롤백할 수 있어 가용성을 유지한다. 둘째, 상태 머신 기반 관리는 유효하지 않은 상태 전이를 컴파일/런타임에 차단하여, "결제 완료 전 배송" 같은 논리적 오류를 구조적으로 방지한다.

#### Responsibilities
- Order creation and validation
- Payment orchestration
- Fulfillment coordination
- Refund processing

#### Order State Machine

```
┌────────┐    ┌─────────┐    ┌───────────┐    ┌─────────┐
│ Draft  │───▶│ Pending │───▶│ Confirmed │───▶│ Shipped │
└────────┘    └─────────┘    └───────────┘    └─────────┘
                  │                │               │
                  ▼                ▼               ▼
              ┌────────┐    ┌───────────┐   ┌───────────┐
              │Cancelled│   │  Failed   │   │ Delivered │
              └────────┘    └───────────┘   └───────────┘
```

#### Implementation Details

**Saga Pattern for Order Creation:**
1. Reserve inventory
2. Process payment
3. Confirm order
4. Notify vendor
5. (Compensate on failure)

---

### Component: Payment Service

#### Overview
PCI-DSS compliant payment processing with multiple gateway support.

#### Supported Gateways
- Stripe (primary)
- PayPal
- Local payment methods (region-specific)

#### Security Measures
- No card data stored (tokenization)
- All PCI data in isolated subnet
- Audit logging for all transactions
- 3D Secure for high-risk transactions

---

## Data Models

### Product

```python
class Product(Base):
    __tablename__ = "products"

    id: UUID = Column(UUID, primary_key=True)
    vendor_id: UUID = Column(UUID, ForeignKey("vendors.id"))
    sku: str = Column(String(50), unique=True)
    name: str = Column(String(255))
    description: str = Column(Text)
    base_price: Decimal = Column(Numeric(10, 2))
    currency: str = Column(String(3), default="USD")
    status: str = Column(String(20))  # draft, active, archived
    created_at: datetime = Column(DateTime, default=utcnow)
    updated_at: datetime = Column(DateTime, onupdate=utcnow)

    # Relationships
    vendor: Vendor = relationship("Vendor")
    categories: List[Category] = relationship(secondary="product_categories")
    variants: List[ProductVariant] = relationship("ProductVariant")
    images: List[ProductImage] = relationship("ProductImage")
```

### Order

```python
class Order(Base):
    __tablename__ = "orders"

    id: UUID = Column(UUID, primary_key=True)
    customer_id: UUID = Column(UUID, ForeignKey("users.id"))
    status: str = Column(String(20))
    subtotal: Decimal = Column(Numeric(10, 2))
    tax: Decimal = Column(Numeric(10, 2))
    shipping: Decimal = Column(Numeric(10, 2))
    total: Decimal = Column(Numeric(10, 2))
    currency: str = Column(String(3))

    # Relationships
    items: List[OrderItem] = relationship("OrderItem")
    shipping_address: Address = relationship("Address")
    payments: List[Payment] = relationship("Payment")
```

---

## Environment & Dependencies

### Directory Structure

```
ecommerce-platform/
├── services/
│   ├── product/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── pyproject.toml
│   ├── order/
│   ├── user/
│   ├── payment/
│   ├── inventory/
│   └── notification/
├── shared/
│   ├── proto/           # gRPC definitions
│   ├── events/          # Event schemas
│   └── libs/            # Shared libraries
├── infra/
│   ├── k8s/             # Kubernetes manifests
│   ├── terraform/       # Infrastructure as code
│   └── docker-compose/  # Local development
├── gateway/
│   └── kong.yaml        # API gateway config
└── docs/
    └── api/             # OpenAPI specs
```

### Environment Variables

| Variable | Service | Description |
|----------|---------|-------------|
| DATABASE_URL | All | PostgreSQL connection |
| REDIS_URL | All | Redis connection |
| KAFKA_BROKERS | All | Kafka broker list |
| STRIPE_SECRET_KEY | Payment | Stripe API key |
| AWS_ACCESS_KEY_ID | Product | S3 access |
| ELASTICSEARCH_URL | Product | Search cluster |

---

## Identified Issues & Improvements

### Critical Bugs
- [ ] **BUG-142**: Race condition in inventory reservation
  - Location: `services/inventory/src/services/reservation.py:89`
  - Impact: Overselling during flash sales
  - Status: Fix in review

### Code Quality
- [ ] Inconsistent error response formats across services
- [ ] Missing OpenTelemetry instrumentation in payment service
- [ ] Test coverage below 70% in order service

### Missing Features
- [ ] Wishlist functionality
- [ ] Product comparison
- [ ] Multi-language support
- [ ] Guest checkout

### Performance
- [ ] Add read replicas for product queries
- [ ] Implement GraphQL for mobile app
- [ ] Add CDN for product images

### Technical Debt
- [ ] Migrate from REST to gRPC for inter-service calls
- [ ] Implement circuit breakers
- [ ] Add distributed tracing

---

## Usage Examples

### Local Development

```bash
# Start all services
docker-compose up -d

# Run migrations
make migrate-all

# Seed test data
make seed-dev

# Run tests
make test
```

### API Examples

**Create Product:**
```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Headphones",
    "sku": "WH-001",
    "base_price": 99.99,
    "category_ids": ["cat_electronics", "cat_audio"]
  }'
```

**Create Order:**
```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"product_id": "prod_123", "variant_id": "var_456", "quantity": 2}
    ],
    "shipping_address_id": "addr_789",
    "payment_method_id": "pm_stripe_abc"
  }'
```

---

## Testing

### Test Pyramid

| Level | Coverage Target | Run Time |
|-------|----------------|----------|
| Unit | 80% | <5 min |
| Integration | 60% | <15 min |
| E2E | Critical paths | <30 min |

### Running Tests

```bash
# Unit tests
pytest services/product/tests/unit/

# Integration tests (requires Docker)
pytest services/product/tests/integration/

# E2E tests
pytest tests/e2e/
```

---

## Deployment

### Environments

| Environment | Purpose | URL |
|-------------|---------|-----|
| Development | Local testing | localhost:8000 |
| Staging | Pre-production | staging.example.com |
| Production | Live | api.example.com |

### Deployment Pipeline

```
┌─────────┐   ┌──────┐   ┌─────────┐   ┌────────┐   ┌──────────┐
│  Push   │──▶│Build │──▶│  Test   │──▶│ Deploy │──▶│Production│
│ to main │   │Image │   │(staging)│   │(canary)│   │(100%)    │
└─────────┘   └──────┘   └─────────┘   └────────┘   └──────────┘
```

---

## Changelog

### [2.0.0] - 2024-01-15
- Added multi-vendor marketplace support
- Migrated to microservices architecture
- Implemented event-driven inventory sync

### [1.5.0] - 2023-09-01
- Added Elasticsearch for product search
- Implemented real-time order tracking
- Added mobile app API support
