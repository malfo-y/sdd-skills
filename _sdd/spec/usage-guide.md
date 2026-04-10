# Usage Guide & Expected Results

> 이 문서는 [main.md](./main.md)에서 분리된 scenario-oriented supporting surface다.
> 각 시나리오는 "어떤 entrypoint로 시작하고, 어떤 artifact와 observable result가 남아야 하는가"를 기준으로 정리한다.
> 메인 스펙의 thin core를 보조하며, usage/expected result detail은 여기서 다룬다.

---

### Scenario 1: 새 프로젝트 스펙 생성 (처음 시작)

**Setup:**
```bash
# 프로젝트 디렉토리에서 SDD Skills 플러그인 설치
/plugin marketplace add malfo-y/sdd-skills
/plugin install sdd-skills@sdd-skills
```

**Action:**
```bash
/spec-create
```

**Expected Result:**
- `_sdd/spec/<project>.md` 생성 — current canonical global spec core(배경, scope, 핵심 설계, CIV, usage, decision-bearing structure)를 갖춘 문서 생성
- `_sdd/env.md` 생성 — 환경 설정/실행 방법 가이드
- `CLAUDE.md` 생성 또는 업데이트 — 워크스페이스 안내에 `_sdd/` 경로 추가
- `AGENTS.md` 생성 또는 업데이트 — 동일한 워크스페이스 안내 유지
- 사용자에게 요약 테이블 제시 후 전체 스펙 출력

### Scenario 2: 대규모 기능 추가 (수동 Full SDD Workflow)

**Action:**
```bash
/feature-draft           # non-trivial change의 기본 planning entry
/spec-update-todo        # planned persistent truth가 실제로 필요할 때만
/implementation-plan     # Part 2만으로 부족하거나 phase/task breakdown이 필요할 때만
/implementation          # TDD 기반 코드 작성
/implementation-review   # 계획 대비 검증
/spec-update-done        # 코드 변경사항을 스펙에 동기화
```

**Expected Result:**
- `_sdd/drafts/<YYYY-MM-DD>_feature_draft_<slug>.md` — 스펙 패치 초안 + 구현 태스크 리스트
- `_sdd/spec/<project>.md` 업데이트 — planned persistent truth 반영
- `_sdd/implementation/<YYYY-MM-DD>_implementation_plan_<slug>.md` — 필요한 경우 생성되는 Target Files 기반 phase/task 실행 계획
- 구현 완료 후 구현 리뷰와 spec sync까지 연결돼 스펙과 코드 간 드리프트가 설명 가능한 상태

### Scenario 2b: 대규모 기능 추가 (sdd-autopilot 자동 실행)

**Action:**
```bash
/sdd-autopilot "인증 시스템 구현 — JWT 기반, 로그인/로그아웃/토큰 갱신"
```

**Expected Result:**
- Phase 1: sdd-autopilot이 SDD reference를 로딩하고, 인라인 discussion으로 요구사항을 구체화하고, 코드베이스를 탐색한 뒤, reasoning 기반으로 오케스트레이터를 생성하고 구조/철학 12항목을 자동 검증
- Phase 1.5: 검증된 오케스트레이터 + Pre-flight Check 결과를 사용자에게 제시 → 확인 후 실행
- Phase 2: `feature-draft`를 기본 planning entry로 사용하고, 필요 시 `(optional) spec-update-todo -> (optional) implementation-plan`으로 확장한다. multi-phase plan이면 phase별 `implementation -> review -> fix -> validation` gate를 닫고 마지막에 `final integration review`를 1회 더 수행한 뒤 인라인 테스트와 `spec-update-done`까지 자율 실행한다
- `_sdd/pipeline/orchestrators/orchestrator_<topic>.md` — 실행 중 authoritative orchestrator contract
- `_sdd/pipeline/log_<topic>_<ts>.md` — 파이프라인 실행 로그 (Meta + Status 테이블 + 각 에이전트 시작/완료, 결정사항, 에러)
- `_sdd/pipeline/report_<topic>_<ts>.md` — 최종 실행/검증 요약과 잔여 이슈 보고
- 구현 완료 + 스펙 동기화 완료

### Scenario 3: PR 기반 스펙 동기화

**Action:**
```bash
/pr-review               # PR 코드 품질 검증 + spec 존재 시 spec 기반 추가 검증 → APPROVE / REQUEST CHANGES
```

**Expected Result:**
- `_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md` — findings-first 코드 품질 검증 + spec 존재 시 spec 준수 여부 판정 + 구체적 피드백

### Scenario 3b: 스펙 현황 파악 및 의사결정

**Action:**
```bash
/spec-summary            # 현재 프로젝트 상태 요약
/discussion              # 기술 선택, 아키텍처 결정 등 구조화된 토론
```

**Expected Result:**
- `_sdd/spec/summary.md` — Executive Summary + 기능 대시보드 + 권장 다음 단계
- `_sdd/discussion/<YYYY-MM-DD>_discussion_<slug>.md` — 토론 결과와 결정사항/미결/실행항목 정리 (최대 10라운드)
