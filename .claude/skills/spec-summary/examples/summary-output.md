# Task Management - Specification Summary

**Generated**: 2026-04-04 00:40
**Spec Type**: Global Spec
**Spec Version**: 2.1.0

## Executive Summary

Task Management는 팀이 작업을 생성, 할당, 추적, 완료하는 흐름을 하나의 시스템으로 묶는다. 이 글로벌 스펙은 협업 작업의 lifecycle, 접근 제어, 알림, 상태 추적이 어떤 계약과 경계를 가지는지 빠르게 이해하도록 돕는다.

현재 상태는 핵심 task lifecycle은 안정화되었고, 권한과 고급 planning 기능이 확장 중인 단계다. 구현 문서 기준으로 일부 기능은 진행 중이며, 성능과 validation 관련 이슈가 남아 있다.

## Problem & High-Level Concept

- **Problem**: 작업 상태, 책임자, 마감일, 커뮤니케이션이 여러 도구에 흩어져 있으면 팀 coordination 비용이 커진다.
- **High-Level Concept**: task lifecycle과 협업 신호를 하나의 shared workflow에 모아, 생성 -> 실행 -> 완료까지의 책임 흐름을 중앙에서 고정한다.

## Scope Snapshot

### In Scope

- task 생성, 수정, 상태 전이
- assignment, due date, comment, notification
- 팀 단위 협업 흐름

### Non-goals

- ERP급 리소스 계획
- 오프라인 업무 프로세스 통합

### Guardrails

- task lifecycle 상태 전이는 validation 없이 우회되면 안 된다.
- 권한 검사는 UI가 아니라 API contract에서 강제되어야 한다.

## CIV Snapshot

### Key Contracts

- `C1`: 유효한 입력만 task로 생성된다.
- `C2`: 상태 전이는 정의된 lifecycle 규칙을 따른다.

### Key Invariants

- `I1`: 완료된 task는 유효한 완료 상태 전이를 거친다.
- `I2`: assignment와 permission contract는 충돌하면 안 된다.

### Verification

- `V1`: task lifecycle 테스트
- `V2`: permission review + integration test

## Decision-Bearing Structure

- **System Boundary**: task collaboration domain을 다루며, 외부 회계/인사 시스템은 포함하지 않는다.
- **Ownership**: task service가 lifecycle ownership을 가진다.
- **Cross-component Contract**: notification은 task state change를 소비하지만 state source가 되지 않는다.
- **Extension Point**: recurring tasks, dependency planning, advanced permission policies

## Usage & Expected Results

- **Scenario**: 사용자가 task를 생성하고 팀원에게 할당한다.
- **Expected Result**: task가 생성되고 assignee가 확인 가능하며 상태 변경 이력이 남는다.

## Status / Risks / Next Steps

- **Current Status**: 핵심 CRUD 및 협업 흐름은 구현됨, 고급 planning/permission은 진행 중
- **Risks**: 권한 세분화와 query performance
- **Next Steps**: permission contract 강화, planning feature 검증, performance bottleneck 정리
