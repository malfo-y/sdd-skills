# Upgraded Global Spec (After)

## 1. Background and High-Level Concept
이 repo는 여러 feature를 공통 운영 규칙 아래에서 다루기 위한 thin global decision layer를 제공한다.

## 2. Scope / Non-goals / Guardrails
- global은 repo-wide 경계만 다룬다.
- feature execution detail은 temporary spec 또는 guide로 보낸다.

## 3. Core Design and Key Decisions
- core decision: global spec은 `개념 + 경계 + 결정`만 기본 코어로 유지한다.
- repo-wide invariant가 필요하면 guardrail wording으로 남긴다.

## Optional Supporting Notes
- supporting references: docs/README
- guide links: feature-specific companion docs
