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

#### Why
Separated as an independent service because product catalog operations (search, browse, CRUD) have fundamentally different scaling and caching requirements from order/payment flows. Decoupling allows Elasticsearch indexing and S3 media handling without impacting transactional services.

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

#### Source

- `services/product/src/main.py`: create_app(), configure_routes()
- `services/product/src/api/products.py`: list_products(), create_product(), get_product(), update_product(), delete_product()
- `services/product/src/api/search.py`: search_products(), build_query()
- `services/product/src/models/product.py`: Product, ProductVariant, ProductImage
- `services/product/src/events/publishers.py`: publish_product_event()

#### Dependencies

| Service | Type | Purpose | Why |
|---------|------|---------|-----|
| PostgreSQL | Database | Product storage | ACID compliance needed for catalog consistency; JSON column support for flexible attributes |
| Elasticsearch | Search | Full-text search | Relational DB full-text too slow at scale; ES provides faceted filtering and relevance scoring |
| S3 | Storage | Product images | Object storage for cost-effective, CDN-friendly media serving |
| Kafka | Queue | Event publishing | Async event propagation to decouple services; chosen over RabbitMQ for replay and partition support |
| Inventory Service | Internal | Stock levels | Inventory has its own consistency domain; direct DB access would break service boundaries |

#### Error Handling

| Error | HTTP | Handling |
|-------|------|----------|
| ProductNotFound | 404 | Return error with ID |
| ValidationError | 400 | Return field errors |
| DuplicateSKU | 409 | Conflict response |

---

### Component: Order Service

#### Overview
Handles order lifecycle from creation to fulfillment.

#### Why
Order processing requires strong consistency guarantees (saga pattern, compensating transactions) that conflict with the eventual-consistency model used in product/search. Isolated as a service to enforce transactional boundaries and enable independent failure handling.

#### Responsibilities
- Order creation and validation
- Payment orchestration
- Fulfillment coordination
- Refund processing

#### Source

- `services/order/src/api/orders.py`: create_order(), cancel_order(), get_order_status()
- `services/order/src/services/saga.py`: OrderCreationSaga, compensate()
- `services/order/src/services/fulfillment.py`: FulfillmentCoordinator, process_refund()
- `services/order/src/models/order.py`: Order, OrderItem, OrderStatus

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

#### Why
PCI-DSS compliance requires strict network isolation and audit logging. Separating payment into its own service confines the compliance boundary — only this service handles tokenized card data, reducing the PCI scope for the rest of the platform.

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
