# 기능 기술 보고서: 결제 승인

**Version**: 1.0.0
**Status**: Draft
**생성일**: 2026-03-12
**입력 소스**: mixed (conversation + spec + code)
**대상 기능**: 결제 승인
**신뢰도**: Medium

## §1 배경 및 동기

결제 승인은 사용자가 결제 의사를 최종 확정했을 때 거래를 승인 상태로 전환하고, 후속 주문 처리 흐름을 시작하기 위한 핵심 기능이다.

이 기능이 해결하는 문제:
- 결제 결과를 예측 가능하게 만들어 사용자에게 명확한 피드백을 제공
- 주문/영수증/재고 반영 같은 후속 단계가 중복 없이 한 번만 실행되도록 보장
- 외부 결제 게이트웨이 응답을 내부 도메인 모델로 안전하게 변환

외부 게이트웨이의 상태를 그대로 노출하는 대신, 내부 상태 모델로 변환하는 접근을 택한 이유는 게이트웨이 벤더 교체 시 영향 범위를 최소화하고, 도메인 로직이 외부 의존성에 직접 결합되는 것을 방지하기 위함이다.

## §2 핵심 설계

결제 승인의 핵심 설계는 **상태 머신 기반 전이**와 **멱등성 보장**이다.

- 결제는 `pending → approved | rejected` 상태 전이만 허용한다. `expired`, `cancelled` 상태에서는 승인이 불가능하다.
- 멱등성 키를 기반으로 동일 요청의 중복 처리를 방지한다. 이미 승인된 결제에 대한 재요청은 기존 결과를 반환한다.
- 외부 게이트웨이 응답은 `PaymentGatewayAdapter`를 통해 내부 도메인 상태로 변환된다.

관련 코드:
- `[src/payments/payment_service.ts:confirmPayment]` — 승인 진입점. 상태 검증 → 게이트웨이 호출 → 상태 전이 → 이벤트 발행
- `[src/payments/payment_repository.ts:markApproved]` — 상태 전이 및 영속화

```typescript
// [src/payments/payment_service.ts:confirmPayment]
async confirmPayment(paymentId: string, idempotencyKey: string) {
  const payment = await this.repo.findById(paymentId);
  if (payment.status !== 'pending') throw new InvalidStateError();
  const existing = await this.repo.findByIdempotencyKey(idempotencyKey);
  if (existing) return existing.result;
  const gwResult = await this.gateway.confirm(payment);
  const domainStatus = this.adapter.toDomainStatus(gwResult);
  await this.repo.markApproved(paymentId, domainStatus);
  await this.events.publish('payment.approved', { paymentId });
}
```

## §3 사용 시나리오 가이드

### 시나리오 1: 정상 결제 승인

**전제 조건**: 결제가 `pending` 상태이며, 유효한 결제 수단이 등록되어 있다.

**입력**:
```json
POST /payments/confirm
{
  "payment_id": "pay_abc123",
  "idempotency_key": "idem_xyz789"
}
```

**처리 흐름**:
1. `payment_id`로 결제 조회 `[src/payments/payment_service.ts:confirmPayment]`
2. 상태가 `pending`인지 확인 `[src/payments/payment_service.ts:confirmPayment]`
3. `idempotency_key`로 기존 처리 이력 확인 → 없음 `[src/payments/payment_repository.ts:findByIdempotencyKey]`
4. 외부 게이트웨이에 승인 요청 `[src/payments/payment_service.ts:confirmPayment]`
5. 게이트웨이 응답을 도메인 상태(`approved`)로 변환 `[src/payments/gateway_adapter.ts:toDomainStatus]`
6. DB에 상태 전이 기록 `[src/payments/payment_repository.ts:markApproved]`
7. `payment.approved` 이벤트 발행 `[src/payments/payment_service.ts:confirmPayment]`

**기대 결과**:
```json
{
  "status": "approved",
  "payment_id": "pay_abc123",
  "approved_at": "2026-03-12T10:30:00Z",
  "transaction_id": "txn_gw_456"
}
```

### 시나리오 2: 중복 승인 요청 (멱등성)

**전제 조건**: 동일 `idempotency_key`로 이미 승인이 완료된 상태.

**입력**: 시나리오 1과 동일한 요청

**처리 흐름**:
1. `payment_id`로 결제 조회 `[src/payments/payment_service.ts:confirmPayment]`
2. `idempotency_key`로 기존 처리 이력 확인 → 존재 `[src/payments/payment_repository.ts:findByIdempotencyKey]`
3. 기존 승인 결과를 그대로 반환 (게이트웨이 재호출 없음) `[src/payments/payment_service.ts:confirmPayment]`

**기대 결과**: 시나리오 1과 동일한 응답 (새 트랜잭션 생성 없음)

### 시나리오 3: 만료된 결제 승인 시도

**전제 조건**: 결제가 `expired` 상태.

**입력**:
```json
POST /payments/confirm
{
  "payment_id": "pay_expired999",
  "idempotency_key": "idem_new001"
}
```

**처리 흐름**:
1. `payment_id`로 결제 조회 `[src/payments/payment_service.ts:confirmPayment]`
2. 상태가 `expired` → 승인 불가 판정 `[src/payments/payment_service.ts:confirmPayment]`

**기대 결과**:
```json
{
  "error": "INVALID_PAYMENT_STATE",
  "message": "결제가 만료되었습니다. 새 결제를 생성해 주세요.",
  "payment_id": "pay_expired999",
  "current_status": "expired"
}
```
HTTP 상태: 409 Conflict

### 시나리오 4: 게이트웨이 타임아웃

**전제 조건**: 결제가 `pending` 상태이나 외부 게이트웨이가 응답하지 않음.

**처리 흐름**:
1. 상태 검증 통과 `[src/payments/payment_service.ts:confirmPayment]`
2. 게이트웨이 호출 → 타임아웃 발생 `[src/payments/payment_service.ts:confirmPayment]`
3. 결제 상태를 `pending` 유지 (변경하지 않음)
4. 에러 로그에 추적 식별자 기록

**기대 결과**:
```json
{
  "error": "GATEWAY_TIMEOUT",
  "message": "결제 처리 중 일시적 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.",
  "retry_after_seconds": 30
}
```
HTTP 상태: 502 Bad Gateway

## §4 API 레퍼런스

### POST /payments/confirm

**구현 소스**: `[src/payments/payment_service.ts:confirmPayment]`

결제를 최종 승인한다.

**파라미터**:

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `payment_id` | string | 필수 | 승인할 결제의 고유 식별자 |
| `idempotency_key` | string | 필수 | 멱등성 보장을 위한 고유 키. 동일 키로 재요청 시 기존 결과 반환 |

**성공 응답** (200 OK):

| 필드 | 타입 | 설명 |
|------|------|------|
| `status` | string | `"approved"` |
| `payment_id` | string | 결제 식별자 |
| `approved_at` | string (ISO 8601) | 승인 시각 |
| `transaction_id` | string | 게이트웨이 트랜잭션 ID |

**에러 응답**:

| HTTP 상태 | 에러 코드 | 상황 |
|-----------|----------|------|
| 404 | `PAYMENT_NOT_FOUND` | 존재하지 않는 `payment_id` |
| 409 | `INVALID_PAYMENT_STATE` | `pending`이 아닌 상태에서 승인 시도 |
| 422 | `VALIDATION_ERROR` | 필수 필드 누락 또는 형식 오류 |
| 502 | `GATEWAY_TIMEOUT` | 외부 게이트웨이 응답 없음 |
| 502 | `GATEWAY_ERROR` | 외부 게이트웨이 오류 응답 |

**호출 예시**:

```bash
curl -X POST /api/v1/payments/confirm \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "payment_id": "pay_abc123",
    "idempotency_key": "idem_xyz789"
  }'
```

## §5 구현 가이드

### 핵심 규칙

1. 승인 요청은 이미 만료되었거나 취소된 결제에 대해 성공으로 처리하면 안 된다. `[src/payments/payment_service.ts:confirmPayment]`
2. 동일 결제에 대한 중복 승인 요청은 멱등적으로 다루어야 한다. `[src/payments/payment_repository.ts:findByIdempotencyKey]`
3. 외부 게이트웨이 응답을 내부 상태 모델에 바로 노출하지 말고 도메인 상태로 변환한다. `[src/payments/gateway_adapter.ts:toDomainStatus]`
4. 승인 성공 후 이벤트 발행 시, 중복 부작용을 막는 식별자를 함께 남긴다.
5. 에러 메시지는 사용자용과 내부 진단용을 분리한다.
6. 금액, 통화, 결제 수단 등 핵심 필드는 승인 전에 다시 검증한다.

### 체크리스트

**구현 전**:
- [ ] 스펙에서 결제 상태 전이 규칙을 확인했다.
- [ ] 승인 API 또는 서비스 진입점이 어디인지 확인했다.
- [ ] 중복 승인 시 기대 동작을 코드 또는 스펙에서 확인했다.

**구현 중**:
- [ ] 승인 가능 상태가 아닌 경우 실패 분기가 존재한다.
- [ ] 외부 응답을 내부 도메인 모델로 정규화한다.
- [ ] 멱등성 키 또는 중복 방지 장치가 존재한다.
- [ ] 성공/실패 로그에 추적 가능한 식별자가 포함된다.

**완료/리뷰 전**:
- [ ] 정상 승인 케이스 테스트가 있다.
- [ ] 중복 승인 요청 테스트가 있다.
- [ ] 만료/취소 결제 실패 케이스 테스트가 있다.
- [ ] 후속 이벤트가 중복 실행되지 않는지 점검했다.

### 안티패턴

- 외부 게이트웨이의 상태 문자열을 그대로 DB에 저장하는 방식 — 벤더 교체 시 전체 상태 로직 수정 필요 (올바른 방식: `[src/payments/gateway_adapter.ts:toDomainStatus]`로 변환)
- 이미 `approved` 상태인 결제에 대해 매번 새 주문 생성 로직을 다시 실행하는 방식 — 중복 주문 발생 (올바른 방식: `[src/payments/payment_repository.ts:findByIdempotencyKey]`로 중복 검사)
- 사용자 응답에 내부 예외 메시지나 스택트레이스를 그대로 노출하는 방식 — 보안 위험

## 부록

### 관련 스펙 레퍼런스

- `_sdd/spec/payments.md` → `목표 > 결제 승인`
- `_sdd/spec/payments_API.md` → `API Reference > POST /payments/confirm`

### 관련 코드 레퍼런스

- `src/payments/payment_service.ts` → `confirmPayment`
- `src/payments/payment_repository.ts` → `markApproved`
- `tests/payments/test_confirm_payment.py` → `test_confirm_payment_is_idempotent`

### 가정 및 미확정 사항

- 결제 승인 타임아웃은 스펙에서 직접 확인되지 않아 별도 운영 정책이 있다고 가정했다.
- 주문 생성은 비동기 이벤트 기반일 가능성이 높지만, 정확한 큐 이름이나 전달 스키마는 코드 근거가 없어서 확정하지 않았다.
