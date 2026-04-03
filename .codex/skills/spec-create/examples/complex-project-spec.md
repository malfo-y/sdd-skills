# Complex Project Spec Example

Example of a larger global spec under the current SDD canonical model.

---

# E-Commerce Platform

> 멀티벤더 전자상거래 플랫폼

**Version**: 2.0.0
**Last Updated**: 2026-04-04
**Status**: In Review

## 1. Background & High-Level Concept

이 플랫폼은 고객, 벤더, 운영자가 하나의 거래 시스템 위에서 다른 요구를 동시에 만족해야 하는 문제를 다룬다. 상품 탐색은 읽기 중심이고, 주문과 결제는 강한 일관성이 필요하며, 재고는 이벤트 지연에 민감하다.

high-level concept는 "탐색, 거래, 운영을 같은 제품 위에 두되, contract가 다른 경계는 명시적으로 분리한다"는 것이다. 따라서 검색과 카탈로그는 고확장 읽기 경계로, 주문과 결제는 강일관 거래 경계로 취급한다.

## 2. Scope / Non-goals / Guardrails

### In Scope

- 멀티벤더 상품 등록과 카탈로그 탐색
- 주문 생성, 결제 승인, 주문 상태 전이
- 운영자용 기본 관리 기능

### Non-goals

- 오프라인 POS 연동
- B2B 대량 주문
- 구독 결제

### Guardrails

- 주문 확정 경로는 결제/재고 contract 없이 우회되면 안 된다.
- 검색 인덱스 지연은 허용되지만 주문 일관성은 희생하지 않는다.

## 3. 핵심 설계와 주요 결정

플랫폼은 "카탈로그-거래 비대칭"을 전제로 한다. 상품 탐색과 추천은 결국 지연 허용 읽기 경계지만, 주문/결제는 후행 정합성이 아니라 강한 계약이 핵심이다.

| Decision | Why | What Must Stay True |
|----------|-----|---------------------|
| catalog와 order를 다른 경계로 둔다 | 읽기 확장성과 거래 일관성의 요구가 다르기 때문에 | 검색 지연은 허용해도 주문 계약은 약화하지 않는다 |
| payment는 order와 분리된 책임을 가진다 | 외부 승인 흐름과 장애 모델이 다르기 때문에 | order는 payment result contract를 명시적으로 소비한다 |
| inventory sync는 event 기반으로 다룬다 | 실시간 fan-out과 재고 갱신 분리가 필요하기 때문에 | oversell 방지 invariant는 별도 hot path에서 지킨다 |

## 4. Contract / Invariants / Verifiability

### Contract

| ID | Subject | Inputs/Outputs | Preconditions | Postconditions | Failure Guarantees |
|----|---------|----------------|---------------|----------------|--------------------|
| C1 | Order creation | cart + buyer context -> order draft | 재고 검증이 선행된다 | 주문 draft가 생성된다 | 검증 실패 시 partial order를 남기지 않는다 |
| C2 | Payment confirmation | payment intent -> approved order state | payment provider 응답이 유효하다 | 주문 상태가 confirmed로 이동한다 | 승인 실패 시 order state는 rollback-safe 상태를 유지한다 |
| C3 | Catalog query | filters -> product list | 인덱스가 사용 가능하다 | 정렬/필터가 적용된 결과를 반환한다 | 인덱스 지연은 허용하되 잘못된 주문 상태를 만들지 않는다 |

### Invariants

| ID | Scope | Invariant | Why It Matters |
|----|-------|-----------|----------------|
| I1 | Order lifecycle | confirmed order는 유효한 payment confirmation 없이 존재할 수 없다 | 거래 무결성 핵심 |
| I2 | Inventory | reservable stock보다 큰 확정 판매는 발생하면 안 된다 | oversell 방지 |
| I3 | Catalog boundary | catalog 지연은 order consistency invariant를 침범하지 않는다 | 읽기/거래 경계 분리 |

### Verifiability

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I2 | test | stock reservation 및 partial failure 테스트 |
| V2 | C2, I1 | test, review | payment callback과 order transition 리뷰/통합 테스트 |
| V3 | C3, I3 | review | catalog latency가 order contract를 침범하지 않는지 아키텍처 리뷰 |

## 5. 사용 가이드 & 기대 결과

### Scenario: 주문 확정

**Setup**: 고객이 장바구니에 상품을 담고 체크아웃을 시작한다.

**Action**: 주문 생성 후 결제 승인 콜백을 처리한다.

**Expected Result**: 승인 전에는 draft 상태가 유지되고, 승인 후에만 confirmed로 이동한다.

### Scenario: 검색 지연

**Setup**: 상품 가격이 갱신되었지만 인덱스 반영이 아직 끝나지 않았다.

**Action**: 사용자가 검색 결과를 본다.

**Expected Result**: catalog 결과는 잠시 stale할 수 있지만, 주문 확정 경로는 최신 계약을 사용한다.

## 6. Decision-bearing structure

- 시스템 경계: catalog/search, order, payment, inventory, admin 운영 경계를 분리한다.
- ownership: order domain이 거래 lifecycle ownership을 갖고, payment는 승인 결과 ownership을 갖는다.
- cross-component contract: payment result -> order state transition, inventory reservation -> order draft creation
- extension point: recommendation engine, vendor policy engine
- invariant hotspot: order confirmation path, inventory reservation path

## 7. 참조 정보

### Data Models

- Order
- PaymentIntent
- InventoryReservation
- ProductCatalogEntry

### Environment & Dependencies

- React / React Native
- FastAPI services
- PostgreSQL
- Redis
- Elasticsearch
- Kafka

## Appendix A. Strategic Code Map

| Kind | Path / Symbol | Why It Matters |
|------|----------------|----------------|
| Entrypoint | `services/order/src/main.py:create_app` | order 경계 진입점 |
| Invariant Hotspot | `services/order/src/application/confirm_order.py:confirm_order` | payment-confirmed invariant 핵심 |
| Invariant Hotspot | `services/inventory/src/application/reserve.py:reserve_inventory` | oversell 방지 핵심 |
| Extension Point | `services/catalog/src/search/query_builder.py:build_query` | search/filter 확장 지점 |
