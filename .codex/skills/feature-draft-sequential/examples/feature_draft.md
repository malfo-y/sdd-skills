# Feature Draft: Real-Time Notifications

**Date**: 2026-02-14
**Author**: Product Team
**Target Spec**: apify_ig.md
**Status**: Draft

---

# Part 1: Spec Patch Draft

# Spec Update Input

**Date**: 2026-02-14
**Author**: Product Team
**Target Spec**: apify_ig.md

## New Features

### Feature: Real-Time Notifications
**Priority**: Medium
**Category**: Enhancement
**Target Component**: notification_service.py (new)
**Target Section**: `_sdd/spec/apify_ig.md` > `Goal > Key Features`

**Description**:
Send external notifications on download completion, failure, and batch completion. Initial channels are Slack and Discord webhooks.

**Acceptance Criteria**:
- [ ] Slack webhook delivery is supported
- [ ] Discord webhook delivery is supported
- [ ] Message template is configurable
- [ ] Delivery failures retry up to 3 times
- [ ] Notifications can be toggled on/off

**Technical Notes**:
- Use async HTTP calls
- Apply exponential backoff retry
- Isolate notification failures from main pipeline

## Improvements

### Improvement: Structured Logging
**Priority**: Medium
**Target Section**: `_sdd/spec/apify_ig.md` > `Issues & Improvements > Proposals`
**Current State**: Plain text logging only
**Proposed**: JSON structured logs with log levels
**Reason**: Better observability and notification integration

## Configuration Changes

### New Config: NOTIFICATION_WEBHOOK_TIMEOUT
**Target Section**: `_sdd/spec/apify_ig.md` > `Configuration`
**Type**: Environment Variable
**Required**: No
**Default**: `3s`
**Description**: Timeout for webhook requests

## Notes

### Constraints
- Notification pipeline must not block core download flow

---

# Part 2: Implementation Plan

# Implementation Plan: Real-Time Notifications

## Overview
Add non-blocking webhook notifications and related configuration/logging updates.

## Scope
### In Scope
- Slack/Discord webhooks
- Retry policy
- Message template support
- Logging and config updates

### Out of Scope
- Email notifications
- Mobile push notifications

## Components
1. **Notification Service**: event-to-webhook delivery
2. **Event Adapter**: map pipeline events to notification payloads
3. **Config Layer**: webhook timeout/retry settings

## Implementation Phases

### Phase 1: Foundation
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | Add notification config schema | P0 | - | Config Layer |
| 2 | Create notification service skeleton | P0 | 1 | Notification Service |

### Phase 2: Delivery
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 3 | Implement Slack delivery | P1 | 2 | Notification Service |
| 4 | Implement Discord delivery | P1 | 2 | Notification Service |
| 5 | Add retry/backoff logic | P1 | 3,4 | Notification Service |

### Phase 3: Integration & Validation
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 6 | Wire event adapter | P1 | 5 | Event Adapter |
| 7 | Add unit/integration tests | P0 | 6 | All |
| 8 | Update docs and examples | P2 | 7 | Docs |

## Task Details

### Task 7: Add unit/integration tests
**Component**: All
**Priority**: P0
**Type**: Test

**Description**:
Add test coverage for success/failure delivery paths and retry behavior.

**Acceptance Criteria**:
- [ ] delivery success path tested
- [ ] retry on transient failure tested
- [ ] max retry cutoff tested
- [ ] non-blocking behavior tested

**Dependencies**: 6

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Webhook rate limiting | Delivery failures | backoff + rate cap |
| Notification outage affects pipeline | Performance/regression | strict timeout + async isolation |

## Open Questions

- [ ] Should batch mode send per-item notifications or one summary?
- [ ] Which event fields are mandatory in notification payloads?

---

## Next Steps

1. Apply Part 1 via `spec-update-todo`
2. Execute Part 2 via `implementation-sequential`
