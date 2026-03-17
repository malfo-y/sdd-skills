# Sample Orchestrator -- 중규모 인증 시스템 + 대규모 ML 파이프라인 예시

이 파일은 `sdd-autopilot`이 생성하는 Codex orchestration skill의 완성도 기준 예시다.
generated orchestrator는 이 정도 밀도로 pipeline step, review-fix, test strategy, error handling, 로그/리포트 계약을 포함해야 한다.

---

## 생성된 오케스트레이터 예시 1 -- 중규모 JWT 인증 시스템

```markdown
# Orchestrator: JWT 인증 시스템

**generated**: 2026-03-17T23:30:00
**scale**: medium
**owner**: sdd-autopilot
**status**: active

## Goal

JWT 기반 인증 시스템을 구현한다. 로그인, 로그아웃, 토큰 갱신 기능을 포함한다.

### Clarified Requirements
- JWT Bearer 인증
- 로그인 엔드포인트 (`email`, `password`)
- 로그아웃 엔드포인트 (토큰 무효화)
- 토큰 갱신 엔드포인트 (refresh token)
- access token 만료: 1시간
- refresh token 만료: 7일
- bcrypt 해시 사용

### Constraints
- 기존 Express.js 프레임워크 사용
- 기존 `User` 모델 확장
- 기존 middleware 패턴 유지

## Pipeline Steps

### Step 1: feature_draft

**agent**: `feature_draft`
**input**: (none)
**output**: `_sdd/drafts/feature_draft_jwt_auth.md`

**prompt**:
Create a feature draft for a JWT-based authentication system.

Requirements:
- login, logout, token refresh
- bcrypt password hashing
- access token 1 hour
- refresh token 7 days

Constraints:
- existing Express.js framework
- extend existing `User` model
- preserve middleware conventions

Original user request: "JWT 기반 인증 시스템 구현해줘. 로그인, 로그아웃, 토큰 갱신 포함."

### Step 2: implementation_plan

**agent**: `implementation_plan`
**input**: `_sdd/drafts/feature_draft_jwt_auth.md`
**output**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

**prompt**:
Turn the feature draft into an implementation plan.

Feature draft: `_sdd/drafts/feature_draft_jwt_auth.md`
Existing spec: `_sdd/spec/main.md`

Requirements:
- identify parallelizable tasks
- keep Target Files explicit
- stay consistent with existing Express.js patterns

Original user request: "JWT 기반 인증 시스템 구현해줘. 로그인, 로그아웃, 토큰 갱신 포함."

### Step 3: implementation

**agent**: `implementation`
**input**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
**output**:
- `src/middleware/auth.js`
- `src/routes/auth.js`
- `src/services/auth-service.js`
- `src/services/token-service.js`
- `src/models/user.js`
- `test/services/auth-service.test.js`
- `test/routes/auth.test.js`

**prompt**:
Execute the implementation plan.

Implementation plan: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

Expectations:
- follow TDD where practical
- keep changes scoped to auth-related files
- preserve existing Express.js conventions

Original user request: "JWT 기반 인증 시스템 구현해줘. 로그인, 로그아웃, 토큰 갱신 포함."

### Step 4: review-fix loop

(managed by autopilot directly -- see Review-Fix Loop below)

### Step 5: spec_update_done

**agent**: `spec_update_done`
**input**: `_sdd/spec/main.md`, implementation outputs
**output**: `_sdd/spec/main.md`

**prompt**:
Synchronize the spec with the completed JWT authentication implementation.

Spec: `_sdd/spec/main.md`
Feature draft: `_sdd/drafts/feature_draft_jwt_auth.md`
Implementation plan: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

Implemented files:
- `src/middleware/auth.js`
- `src/routes/auth.js`
- `src/services/auth-service.js`
- `src/services/token-service.js`
- `src/models/user.js`

## Artifact Handoff

- feature draft: `_sdd/drafts/feature_draft_jwt_auth.md`
- implementation plan: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- pipeline log: `_sdd/pipeline/log_jwt_auth_20260317_233000.md`
- final report: `_sdd/pipeline/report_jwt_auth_20260317_233000.md`

## Review-Fix Loop

- **max rounds**: 3
- **stop condition**: critical = 0 and high = 0
- **fix scope**: critical/high only
- **max rounds reached**: if unresolved critical/high remain, stop the pipeline

### Review Prompt

Review the JWT auth implementation.

Implementation plan: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

Files to review:
- `src/middleware/auth.js`
- `src/routes/auth.js`
- `src/services/auth-service.js`
- `src/services/token-service.js`
- `src/models/user.js`
- `test/services/auth-service.test.js`
- `test/routes/auth.test.js`

Review output must include severity labels: critical / high / medium / low.

### Fix Prompt

If critical/high issues remain, send only those issues back to `implementation`.
Do not broaden the scope beyond the identified review findings.

## Test Strategy

- **strategy**: inline verification
- **commands**:
  - `npm test -- auth`
  - `git diff --check`
- **Exit Criteria**:
  - auth tests pass
  - login / refresh / logout flow is covered
  - working tree has no whitespace errors
- **Execute -> Verify**:
  - execute tests
  - verify exit code and requested auth behavior
  - if Exit Criteria are not met after max retries, stop the pipeline

## Error Handling

- **retry**: 3
- **critical steps**: `feature_draft`, `implementation_plan`, `implementation`, `implementation_review`, selected test stage
- **non-critical steps**: `spec_update_done`
- **fallback**: non-critical failure is logged with manual follow-up guidance
```

## 대응하는 로그 파일 예시 1

```markdown
# Pipeline Log: JWT 인증 시스템

## Meta
- **request**: "JWT 기반 인증 시스템 구현해줘. 로그인, 로그아웃, 토큰 갱신 포함."
- **orchestrator**: `.codex/skills/orchestrator_jwt_auth/SKILL.md`
- **scale**: medium
- **started**: 2026-03-17T23:30:00
- **pipeline**: feature_draft -> implementation_plan -> implementation -> review-fix -> inline verification -> spec_update_done

## Status
| Step | Agent | Status | Output |
|------|-------|--------|--------|
| 1 | feature_draft | completed | `_sdd/drafts/feature_draft_jwt_auth.md` |
| 2 | implementation_plan | completed | `_sdd/implementation/IMPLEMENTATION_PLAN.md` |
| 3 | implementation | completed | 7 files updated |
| 4 | review-fix | completed | round 2 passed |
| 5 | inline verification | completed | auth tests passed |
| 6 | spec_update_done | completed | `_sdd/spec/main.md` |

## Execution Log

### feature_draft -- completed
- **time**: 23:30:00 ~ 23:34:00
- **output**: `_sdd/drafts/feature_draft_jwt_auth.md`
- **key decisions**:
  - access / refresh token split adopted
  - existing `User` model extended instead of adding new auth model
- **issues**: none

### implementation_plan -- completed
- **time**: 23:34:00 ~ 23:38:00
- **output**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- **key decisions**:
  - route/service split
  - auth middleware and token service implemented separately
- **issues**: none

### implementation -- completed
- **time**: 23:38:00 ~ 23:53:00
- **output**: 7 files updated
- **key decisions**:
  - bcrypt hash verification in auth service
  - refresh token invalidation on logout
- **issues**: none

### review-fix -- round 1/3
- **result**: critical 0, high 2, medium 1, low 0
- **critical/high fixes applied**:
  - refresh token rotation bug fixed
  - missing auth middleware branch test added

### review-fix -- round 2/3
- **result**: critical 0, high 0, medium 1, low 0
- **status**: passed

### inline verification -- completed
- **execute**:
  - `npm test -- auth`
  - `git diff --check`
- **verify**:
  - auth tests passed
  - refresh / logout flow covered
  - no whitespace errors

### spec_update_done -- completed
- **time**: 24:00:00 ~ 24:03:00
- **output**: `_sdd/spec/main.md`
- **issues**: none
```

---

## 생성된 오케스트레이터 예시 2 -- 대규모 ML 학습 파이프라인 (`ralph_loop`)

이 예시는 `ralph_loop_init`를 사용할 때 Execute -> Verify가 어떻게 분리되어야 하는지 보여준다.

> `ralph_loop_init`는 설정 생성과 실제 실행+결과 검증이 모두 완료되어야 한다. 설정만 만들고 넘어갈 수 없다.

```markdown
# Orchestrator: 이미지 분류 Fine-tuning 파이프라인

**generated**: 2026-03-18T10:00:00
**scale**: large
**owner**: sdd-autopilot
**status**: active

## Goal

ViT 기반 이미지 분류 fine-tuning 파이프라인을 구현한다. DDP 학습과 WandB 로깅을 포함한다.

### Clarified Requirements
- ViT 기반 이미지 분류 fine-tuning
- DDP multi-GPU training
- WandB logging
- 1 epoch 이상 실행 가능한 학습 엔트리
- validation accuracy 기록

### Constraints
- 기존 PyTorch training stack 재사용
- GPU 없는 테스트 환경에서도 일부 unit test는 실행 가능해야 함
- config-driven training entry 유지

## Pipeline Steps

### Step 1: feature_draft
**agent**: `feature_draft`
**output**: `_sdd/drafts/feature_draft_image_cls_finetune.md`

### Step 2: spec_update_todo
**agent**: `spec_update_todo`
**input**: `_sdd/drafts/feature_draft_image_cls_finetune.md`, `_sdd/spec/main.md`
**output**: `_sdd/spec/main.md`

### Step 3: implementation_plan
**agent**: `implementation_plan`
**input**: `_sdd/drafts/feature_draft_image_cls_finetune.md`
**output**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

### Step 4: implementation
**agent**: `implementation`
**input**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
**output**:
- `src/models/vit_classifier.py`
- `src/data/cls_dataset.py`
- `src/training/trainer.py`
- `src/utils/ddp.py`
- `src/utils/wandb_logger.py`
- `configs/finetune_vit.yaml`
- `scripts/train.py`
- `tests/test_trainer.py`

### Step 5: review-fix loop
(managed by autopilot directly)

### Step 6: ralph_loop (Execute -> Verify)

**Phase A-1: setup generation**

**agent**: `ralph_loop_init`
**input**: implementation outputs, `configs/finetune_vit.yaml`
**output**: `ralph/`

**prompt**:
Set up an automated debug/training loop for the image classification fine-tuning pipeline.

Training command:
`torchrun --nproc_per_node=2 scripts/train.py --config-name=finetune_vit`

Success criteria:
- at least 1 epoch completes
- validation accuracy is recorded

**Phase B-1: setup verification (Exit Criteria)**
- `ralph/` directory exists
- `ralph/run.sh` is executable
- `ralph/state.md` exists

**Phase A-2: actual execution**
- run the ralph loop in background or attached mode according to environment constraints

**Phase B-2: result verification (Exit Criteria)**
- `ralph/state.md` has `phase == DONE`
- at least 1 iteration was executed
- final loss / accuracy is recorded
- if Exit Criteria fail, stop the pipeline

### Step 7: spec_update_done
**agent**: `spec_update_done`
**input**: `_sdd/spec/main.md`, implementation outputs
**output**: `_sdd/spec/main.md`

## Review-Fix Loop

- **max rounds**: 3
- **stop condition**: critical = 0 and high = 0
- **max rounds reached**: if unresolved critical/high remain, stop the pipeline

## Test Strategy

- **strategy**: `ralph_loop_init`
- **reason**: training/debug loop is long-running and unsuitable for short inline verification
- **Exit Criteria**:
  - setup verified
  - `ralph/state.md phase == DONE`
  - training result metrics recorded

## Error Handling

- **retry**: 3
- **critical steps**: `feature_draft`, `implementation_plan`, `implementation`, `implementation_review`, `ralph_loop_init`
- **non-critical steps**: `spec_update_todo`, `spec_update_done`, `spec_review`
- **fallback**: if `ralph_loop_init` setup or execution verification fails after max retries, stop the pipeline and leave active orchestrator in place
```

## 대응하는 로그 파일 예시 2

```markdown
# Pipeline Log: 이미지 분류 Fine-tuning 파이프라인

## Meta
- **request**: "이미지 분류 모델 fine-tuning 파이프라인 구현해줘. ViT 기반으로, DDP 학습, WandB 로깅 포함."
- **orchestrator**: `.codex/skills/orchestrator_image_cls_finetune/SKILL.md`
- **scale**: large
- **started**: 2026-03-18T10:05:00
- **pipeline**: feature_draft -> spec_update_todo -> implementation_plan -> implementation -> review-fix -> ralph_loop -> spec_update_done

## Status
| Step | Agent | Status | Output |
|------|-------|--------|--------|
| 1 | feature_draft | completed | `_sdd/drafts/feature_draft_image_cls_finetune.md` |
| 2 | spec_update_todo | completed | `_sdd/spec/main.md` |
| 3 | implementation_plan | completed | `_sdd/implementation/IMPLEMENTATION_PLAN.md` |
| 4 | implementation | completed | 8 files updated |
| 5 | review-fix | completed | round 2 passed |
| 6 | ralph_loop | completed | `ralph/state.md phase=DONE` |
| 7 | spec_update_done | completed | `_sdd/spec/main.md` |

## Execution Log

### review-fix -- round 1/3
- **result**: critical 1, high 2, medium 3, low 1
- **fix scope**: critical/high only

### review-fix -- round 2/3
- **result**: critical 0, high 0, medium 2, low 1
- **status**: passed

### ralph_loop_init -- completed (Phase A-1, B-1)
- **output**: `ralph/`
- **verify**:
  - `ralph/` exists
  - `ralph/run.sh` executable
  - `ralph/state.md` exists

### ralph_loop execution -- completed (Phase A-2, B-2)
- **iterations**: 3
- **verify**:
  - `ralph/state.md phase == DONE`
  - final `val_accuracy = 0.847`
  - final training loss recorded

### spec_update_done -- completed
- **output**: `_sdd/spec/main.md`
```
