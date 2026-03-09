# Spec Document Examples

Use the examples to choose document shape, not to copy every section blindly.

## Which Example to Open

- `examples/simple-project-spec.md`
  - small project
  - 1-3 major components
  - one main spec is enough

- `examples/complex-project-spec.md`
  - larger repository
  - multiple bounded components or services
  - main spec should behave like an index and change map

## What to Learn From the Examples

- how the `Goal` section gives a fast repository summary
- how `Architecture Overview` includes both repository map and runtime map
- how `Component Details` starts with a component index before deeper detail
- how `Usage Examples` includes change/debug entry points, not only run commands
- how `Open Questions` keeps uncertainty explicit

## What Not to Copy

- do not duplicate code structure line by line
- do not include optional sections unless they matter
- do not write long narrative when a path table is clearer
- do not hide weak assumptions; move them to `Open Questions`

## Recommended Reading Order

1. Open the simple example for the baseline structure.
2. Open the complex example to see how index-first specs scale.
3. Use `references/template-full.md` for the actual draft.
4. Use `references/optional-sections.md` only when the project needs extra appendices.

---

## Section Quality: Good vs Bad Examples

Below are concrete examples showing the difference between weak and strong spec writing
for each key section. Use these as a quality reference when drafting.

### Repository Map

**Bad** — 경로 없이 모호한 설명:

~~~
프로젝트는 서비스 레이어, 데이터 레이어, 프레젠테이션 레이어로 구성됩니다.
서비스 레이어에서 비즈니스 로직을 처리하고, 데이터 레이어에서 DB 접근을 합니다.
~~~

**Good** — 실제 경로와 역할을 연결:

~~~
src/
├── api/            # HTTP 엔드포인트 (Express 라우터)
│   ├── routes/     # 라우트 정의
│   └── middleware/  # 인증, 에러 핸들링
├── domain/         # 비즈니스 로직 (프레임워크 무관)
│   ├── order/      # 주문 생성, 상태 전이
│   └── payment/    # 결제 처리, 환불
├── infra/          # 외부 연동
│   ├── db/         # Prisma 스키마, 마이그레이션
│   └── external/   # PG사 API 클라이언트
└── config/         # 환경별 설정
~~~

### Change Recipes

**Bad** — 무엇을 바꾸라는지 알 수 없음:

~~~
새 API를 추가하려면 관련 파일을 수정하세요.
~~~

**Good** — 단계, 경로, 검증 포인트를 구체적으로 제공:

~~~markdown
### 새 REST 엔드포인트 추가

1. `src/api/routes/`에 라우트 파일 추가
2. `src/domain/`에 비즈니스 로직 함수 작성
3. `src/api/routes/index.ts`에 라우트 등록
4. `tests/api/`에 통합 테스트 추가

검증: `npm test -- --grep "새 엔드포인트"` 통과
주의: `src/api/middleware/auth.ts`의 권한 체크 미들웨어 적용 필수
~~~

### Interfaces / Contracts

**Bad** — 구현을 그대로 복사:

~~~
// OrderService 클래스는 createOrder, cancelOrder, getOrderById,
// updateOrderStatus, listOrders, getOrderHistory, validateOrder,
// calculateTotal, applyDiscount, sendConfirmation 메서드를 가집니다.
// createOrder는 userId, items, shippingAddress를 받아서...
// (이하 200줄의 메서드별 설명)
~~~

**Good** — 외부에서 알아야 할 계약만 간결하게:

~~~
OrderService 핵심 계약:
- createOrder(userId, items, address) → Order
  - 불변: items가 비어있으면 거부
  - 불변: 재고 차감은 이 함수 안에서 트랜잭션으로 처리
  - 부작용: 주문 생성 후 `order.created` 이벤트 발행
- cancelOrder(orderId) → void
  - 불변: SHIPPED 이후 상태는 취소 불가
  - 부작용: 재고 복원, `order.cancelled` 이벤트 발행
~~~

### Responsibility

**Bad** — 책임만 있고 비책임이 없음:

~~~
PaymentService는 결제를 처리합니다.
~~~

**Good** — 경계가 명확:

~~~
PaymentService
- 책임: PG사 API 호출, 결제 상태 추적, 환불 처리
- 비책임: 주문 상태 변경(OrderService), 알림 발송(NotificationService)
- 주의: 결제 상태와 주문 상태 동기화는 이벤트 기반. 직접 호출하지 않음.
~~~

### Open Questions

**Bad** — 불확실성을 사실처럼 기술:

~~~
이 시스템은 초당 10,000건의 요청을 처리할 수 있습니다.
~~~

**Good** — 모르는 것을 명시:

~~~
## Open Questions
- 현재 부하 테스트 미실시. 실제 처리량 미확인.
- Redis 캐시 만료 정책이 비즈니스 요구사항과 맞는지 검증 필요.
- `external/pg-client.ts`의 타임아웃 설정 근거 불명 (현재 30초).
~~~
