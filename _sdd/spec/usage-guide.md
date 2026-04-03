# Usage Guide & Expected Results

> 이 문서는 SDD Skills의 대표 사용 시나리오와 기대 결과를 정리한다.
> 메인 스펙: [main.md](./main.md)

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
- `_sdd/spec/<project>.md` 생성 — 프로젝트 코드를 분석하여 §1~§8 구조의 스펙 문서 자동 생성
- `_sdd/env.md` 생성 — 환경 설정/실행 방법 가이드
- `CLAUDE.md` 생성 또는 업데이트 — 워크스페이스 안내에 `_sdd/` 경로 추가
- 사용자에게 요약 테이블 제시 후 전체 스펙 출력

### Scenario 2: 대규모 기능 추가 (수동 Full SDD Workflow)

**Action:**
```bash
/feature-draft           # Part 1: 스펙 패치 초안 + Part 2: 구현 계획
/spec-update-todo        # 스펙에 새 기능 반영
/implementation-plan     # Phase별 구현 계획 수립
/implementation          # TDD 기반 코드 작성
/implementation-review   # 계획 대비 검증
/spec-update-done        # 코드 변경사항을 스펙에 동기화
```

**Expected Result:**
- `_sdd/drafts/feature_draft_<name>.md` — 스펙 패치 초안 + 구현 태스크 리스트
- `_sdd/spec/<project>.md` 업데이트 — 새 기능 반영
- `_sdd/implementation/implementation_plan.md` — Target Files 기반 병렬 실행 계획
- 구현 완료 후 스펙과 코드 간 드리프트 0 상태

### Scenario 2b: 대규모 기능 추가 (sdd-autopilot 자동 실행)

**Action:**
```bash
/sdd-autopilot "인증 시스템 구현 — JWT 기반, 로그인/로그아웃/토큰 갱신"
```

**Expected Result:**
- Phase 1: sdd-autopilot이 SDD reference를 로딩하고, 인라인 discussion으로 요구사항을 구체화하고, 코드베이스를 탐색한 뒤, reasoning 기반으로 오케스트레이터를 생성하고 구조/철학 12항목을 자동 검증
- Phase 1.5: 검증된 오케스트레이터 + Pre-flight Check 결과를 사용자에게 제시 → 확인 후 실행
- Phase 2: feature-draft → implementation-plan → implementation → implementation-review (review-fix loop, **필수 사이클** -- Hard Rule #9에 따라 이슈 발견 시 fix → re-review 반드시 실행) → 인라인 테스트 → spec-update-done을 자율 실행
- `.claude/skills/orchestrator_auth_system/SKILL.md` 또는 `.codex/skills/orchestrator_auth_system/SKILL.md` — 실행 중 활성 오케스트레이터 (스킬로 재사용/재개 가능)
- `_sdd/pipeline/log_auth_system_<ts>.md` — 파이프라인 실행 로그 (Meta + Status 테이블 + 각 에이전트 시작/완료, 결정사항, 에러)
- `_sdd/pipeline/orchestrators/auth_system_<ts>/` — 완료된 오케스트레이터 아카이브
- 구현 완료 + 스펙 동기화 완료

### Scenario 3: PR 기반 스펙 동기화

**Action:**
```bash
/pr-review               # PR 코드 품질 검증 + spec 존재 시 spec 기반 추가 검증 → APPROVE / REQUEST CHANGES
```

**Expected Result:**
- `_sdd/pr/pr_review.md` — 코드 품질 + 스펙 준수 여부 판정 + 구체적 피드백

### Scenario 3b: 스펙 현황 파악 및 의사결정

**Action:**
```bash
/spec-summary            # 현재 프로젝트 상태 요약
/discussion              # 기술 선택, 아키텍처 결정 등 구조화된 토론
```

**Expected Result:**
- `_sdd/spec/summary.md` — Executive Summary + 기능 대시보드 + 권장 다음 단계
- 토론 결과 — 결정사항/미결/실행항목 정리 (최대 10라운드)
