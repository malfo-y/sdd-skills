# Feature Draft: Codex investigate intent boundary

> 규모 판정: 적격 — Codex investigate 단일 스킬의 mode 분기·조건부 AC·리포트 계약을 한 task에서 눈검산하고 read-only smoke로 검증할 수 있다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

Codex `investigate`는 사용자 요청을 diagnose-only와 fix로 구분한다. 명시적 수정 권한이 없는 `diagnose`·`why is this failing`·근본원인 분석 요청은 증거·근본원인·영향 범위·권고까지만 반환하고 파일을 쓰지 않는다. fix/repair/patch/수정 요청 또는 후속 승인 때만 기존 Fix & Verify 경로로 진입한다.

## Scope

- **In**: `.codex/skills/investigate/SKILL.md`의 intent classification, 조건부 AC/Hard Rules/Process/Report, diagnose-only runtime smoke, current truth 동기화
- **Out**: `.claude/skills/investigate`, 다른 review 스킬의 write policy, generic Codex host policy, 실제 제품 버그 수정
<!-- spec-update-todo-input-end -->

## Decisions and Assumptions

- **Safe default**: `debug`·`investigate`처럼 수정 의도가 불명확한 표현은 diagnose-only로 분류한다. 대안은 이를 관례적 fix 요청으로 해석하는 것이지만, Codex의 최소 권한 task contract와 이번 audit 목적(무단 scope 확대 제거)에 반하므로 배제한다. 제품·소스 write 권한은 `fix`·`repair`·`patch`·`수정해줘`·`고쳐줘`처럼 조사 대상의 수정을 명시할 때만 인정한다. 진단 보고서·분석 산출물 작성 요청은 제품 fix 권한이 아니다. 확신도 high, 구현 전 사용자 확인 불필요.
- **Mode transition**: diagnose-only 중 사용자가 후속으로 fix를 승인하면 기존 evidence/root cause를 재사용해 blast radius gate 뒤 Fix & Verify로 전환한다. 승인이 없으면 권고가 있어도 쓰지 않는다.
- **Non-mutating verification**: diagnose-only도 재현 명령, 로그/테스트 조회 같은 read-only 검증은 수행할 수 있다. 제품·소스·spec fix와 회귀 테스트 추가는 금지하지만, 상위 저장소 규칙이 명시적으로 강제하는 work-log 같은 governance 기록은 허용하고 최종 보고에 공개한다. 예외 쓰기도 그 규칙의 최소 대상·연산 의미를 보존한다(append 요구이면 기존 내용 보존). “Fresh Verification”의 수정 후 회귀 의미는 fix mode에만 적용한다.
- **Platform scope**: 대안은 Claude mirror까지 함께 맞추는 것이지만, 이번 요청은 Codex 전수검사 findings의 순차 교정이고 Claude 동작은 검증 범위 밖이므로 `.codex`만 수정한다. 확신도 high, 구현 전 사용자 확인 불필요. cross-platform parity 여부는 별도 항목이다.

# Part 2: Tasks

### Task 1: Make investigate honor diagnose-only intent

Step 1에서 mode를 잠가 사용자 권한 확대를 막는다.

**Contracts**: 조사 대상 제품·소스의 명시적 수정 요청이 없으면 `diagnose-only`; 진단 보고서·분석 산출물 작성 요청만으로는 fix mode가 되지 않는다. 이 mode에서는 제품·소스·spec fix와 회귀 테스트 추가가 금지된다. 상위 repo 규칙이 명시적으로 강제하는 governance 기록만 예외이며 보고에 공개한다. fix mode만 blast radius gate 후 수정과 fresh verification을 수행한다. 양 mode 모두 root cause evidence, scope lock, 조건부 fan-out 규칙을 유지한다.

**Acceptance Criteria**:

- [ ] AC1: Step 1이 diagnose-only/fix 분류 기준과 safe default, 후속 승인 전환을 명시한다.
- [ ] AC2: Acceptance Criteria와 Hard Rules가 diagnose-only의 제품 fix 금지·governance 예외 공개·evidence report와 fix mode의 blast-radius/fresh-verification을 각각 falsifiable하게 요구한다.
- [ ] AC3: Process에서 diagnose-only는 Root Cause Synthesis와 영향 범위 분석 뒤 Fix & Verify를 건너뛰며, fix mode만 write 단계에 진입한다.
- [ ] AC4: Investigation Report가 Mode와 `Fix: Not applied (diagnose-only)`를 구분하고, 양 mode의 Verification 의미를 설명한다.
- [ ] AC5: 기존 runtime adapter, conditional explorer fan-out, 3-Strike, scope lock, spec 불가침 계약은 보존된다.

**Target Files**:

- [M] `.codex/skills/investigate/SKILL.md` -- intent-aware diagnose/fix workflow

### Task 2: Verify diagnose-only causes no workspace mutation

정적 계약 검사와 격리된 representative Codex CLI invocation으로 제품 fix 금지 경계를 확인한다.

**Acceptance Criteria**:

- [ ] AC1: diagnose-only·explicit fix·mode transition·제품 fix 금지·governance 예외 공개·conditional verification 구조 검사가 모두 통과한다.
- [ ] AC2: post-change 자산을 담은 격리 임시 복사본에서 `codex-cli 0.146.0 --sandbox workspace-write`로 명시적 diagnose-only fixture를 실행한다. 출력 파일은 복사본 밖에 두고, 실행 전후 `.git`과 상위 규칙이 강제하는 `_sdd/work_log/`만 제외한 전체 파일 목록+content hash가 동일하며, 리포트가 공백 정규화 후 `Mode: diagnose-only`·`Fix: Not applied (diagnose-only)`를 반환한다. work-log는 별도 before/after manifest로 비교해 변경이 없으면 `Governance Writes: None`, 변경이 있으면 허용된 날짜별 log만 바뀌고 기존 내용의 바이트 prefix가 보존된 append-only 변경이며 보고 내용이 실제 diff와 일치하는지 확인한다.
- [ ] AC3: fix mode 문면에는 Blast Radius Gate→Fix & Verify 순서와 fresh verification이 남아 있다.
- [ ] AC4: `git diff --check`, Markdown local link, SKILL direct reference, agent TOML 5/5 parse/name 검사가 통과한다.

**Target Files**:

- 없음 (read-only 검증)
