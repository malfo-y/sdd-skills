# Upgrade Mapping Guide - Legacy Spec -> Current Canonical Model

구 형식 스펙에서 흔히 발견되는 섹션/패턴을 현재 SDD canonical global spec model로 매핑하는 가이드.

---

## Legacy -> Global Spec Mapping

| Legacy Section / Pattern | New Location | Notes |
|--------------------------|-------------|-------|
| Overview / Intro / 개요 | `1. Background & High-Level Concept` | 문제와 개념을 분리해 재서술 |
| Goals / 목표 | `1. Background & High-Level Concept` + `2. Scope / Non-goals / Guardrails` | 목표는 가치/문제와 연결하고, 범위는 별도로 고정 |
| Key Features | `2. Scope / Non-goals / Guardrails` | scope 일부로 편입 |
| Scope / 범위 | `2. Scope / Non-goals / Guardrails` | in-scope와 out-of-scope를 함께 정리 |
| Requirements | `4. Contract / Invariants / Verifiability` 또는 `5. Usage Guide & Expected Results` | 계약성 요구인지 사용 흐름인지 구분 |
| Architecture / System Diagram | `6. Decision-Bearing Structure` 또는 `7. Reference Information` | 구조적 의미가 있으면 6, 단순 참조면 7 |
| Tech Stack | `7. Reference Information` | 본문 핵심 구조로 승격하지 않음 |
| Component Details | `6. Decision-Bearing Structure` 또는 `7. Reference Information` | decision-bearing한 내용만 본문에 남김 |
| API / CLI Reference | `7. Reference Information` | 참조 정보로 유지 |
| Data Models / Schema | `7. Reference Information` | 참조 정보로 유지 |
| Usage / Examples / Quick Start | `5. Usage Guide & Expected Results` | 시나리오 기준으로 재구성 |
| Known Issues / TODO | `3. Core Design & Key Decisions` 또는 별도 appendix/reference | 결정에 영향이 있으면 본문, 단순 backlog면 appendix/reference |
| Code Reference Index | `Appendix B. Related Docs & Code References` | 필요 시 유지 |

## Legacy -> Temporary Spec Mapping

legacy spec 안에 change proposal이나 execution plan이 글로벌 스펙에 섞여 있다면 global body에 남기지 않는다.

| Legacy Pattern | New Temporary Spec Section |
|----------------|---------------------------|
| Proposed changes | `Change Summary` |
| Changed scope | `Scope Delta` |
| Interface change / contract change | `Contract/Invariant Delta` |
| Files to touch | `Touchpoints` |
| Step-by-step plan | `Implementation Plan` |
| Test plan / validation checklist | `Validation Plan` |
| Open questions / risks | `Risks / Open Questions` |

## What To Compress, Move, Or Drop

### Keep in Main Body

- 핵심 설계 결정
- 시스템 경계
- ownership
- cross-component contract
- 중요한 invariant hotspot 설명

### Move to Reference Information or Appendix

- detailed API tables
- data model field inventory
- environment configuration details
- curated strategic code map

### Drop or Compress Aggressively

- file-by-file implementation walkthrough
- class/function lists that simply restate code
- architecture/component sections with no decision-bearing value
- duplicated setup instructions already covered elsewhere

## CIV Recovery Guide

When legacy specs do not have CIV explicitly:

1. extract contract-like statements from requirements, interfaces, and usage
2. identify system/domain invariants that must not be broken
3. connect each item to a verification method

Example:

| Legacy statement | New location |
|------------------|-------------|
| "Only approved payments create confirmed orders" | `I1` invariant |
| "POST /shorten returns a unique code" | `C1` contract |
| "Test payment callback flow" | `V1` verifiability |

## Strategic Code Map Upgrade Rule

If the old spec contains a large code reference appendix:

- keep only navigation-critical entries
- convert them into entrypoint / invariant hotspot / extension point / change hotspot rows
- remove exhaustive inventories that add no decision value
