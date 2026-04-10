# 토론 요약: SDD 아티팩트 파일명 패턴 변경 및 prev/ 백업 제거

**날짜**: 2026-04-10
**라운드 수**: 5
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)

1. **prev/ 백업 불필요**: git이 이미 버전 관리를 하고 있어 prev/ 백업을 실제로 참조하는 일이 없음. 전체 스킬에서 prev/ 로직을 제거하기로 결정.
2. **implementation 아티팩트 파일명 전환**: 덮어쓰기 방식(`implementation_plan.md`)에서 slug 기반 개별 파일로 전환하여 히스토리를 파일 시스템에서도 유지.
3. **파일명 패턴 통일**: `<YYYY-MM-DD>_<filename>_<slug>.md` 패턴으로 feature-draft 포함 slug 기반 스킬 전체 통일.
4. **스킬 간 파일 참조**: slug 기반으로 바뀌어도 기존 메커니즘(오케스트레이터 명시 전달 + 디렉토리 glob)으로 충분히 해결 가능함을 확인.
5. **영향 범위**: 총 17개 스킬이 영향을 받으며, 3개 그룹(slug 쓰기 전환 / 읽기 경로 업데이트 / prev/ 제거만)으로 분류.
6. **적용 범위**: `.claude/skills/`와 `.codex/skills/` 두 곳 모두에 동일하게 적용. `.codex/agents/*.toml`도 해당 시 업데이트.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | 모든 스킬에서 prev/ 백업 로직 완전 제거 | git이 버전 관리를 담당, 실제 prev/ 참조 사례 없음 | 1 |
| 2 | implementation-plan/review/report를 slug 기반으로 전환 | feature-draft와 동일한 패턴으로 일관성 확보 | 2 |
| 3 | pr-review를 slug 기반으로 전환 | 동일 원칙 적용 | 2 |
| 4 | guide-create는 기존 slug 유지, prev/ 제거만 | 이미 slug 기반(`guide_<slug>.md`) | 2 |
| 5 | spec 관련 스킬은 덮어쓰기 유지, prev/ 제거만 | spec은 단일 문서로 관리하는 것이 적합 | 2 |
| 6 | 파일명 패턴: `<YYYY-MM-DD>_<filename>_<slug>.md` | 날짜 + 파일 종류 + 컨텍스트를 모두 표현 | 3 |
| 7 | feature-draft도 새 패턴으로 통일 | 기존 `feature_draft_<name>.md`에서 날짜 prefix 추가 | 3 |
| 8 | `.claude/skills/`와 `.codex/skills/` 양쪽 모두 동일 적용 | 두 플랫폼은 미러 관계이므로 동일 원칙 적용 | 6 |

## 미결 질문 (Open Questions)

- 없음

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 대상 스킬 |
|---|------|---------|----------|
| 1 | slug 기반 쓰기로 전환 | High | feature-draft, implementation-plan, implementation-review, implementation(report), pr-review, guide-create |
| 2 | slug 파일 읽기 경로(glob 패턴) 업데이트 | High | implementation, implementation-review, spec-update-done, spec-summary, sdd-autopilot |
| 3 | prev/ 백업 로직 제거 | High | spec-create, spec-update-todo, spec-update-done, spec-rewrite, spec-upgrade, spec-summary, implementation-review, implementation, pr-review, guide-create |
| 4 | `.claude/agents/` + `.codex/skills/` + `.codex/agents/` 동일 적용 | High | 위 1-3번 항목 전체를 세 플랫폼 네 디렉토리에 동일 반영 |

## 스킬별 변경 상세

### 그룹 ①: slug 기반 쓰기로 전환 (파일명 변경)

| 스킬 | 현재 쓰기 | 변경 후 쓰기 |
|------|----------|-------------|
| feature-draft | `feature_draft_<name>.md` | `<YYYY-MM-DD>_feature_draft_<slug>.md` |
| implementation-plan | `implementation_plan.md` | `<YYYY-MM-DD>_implementation_plan_<slug>.md` |
| implementation-review | `implementation_review.md` | `<YYYY-MM-DD>_implementation_review_<slug>.md` |
| implementation (report) | `implementation_report.md` | `<YYYY-MM-DD>_implementation_report_<slug>.md` |
| pr-review | `pr_review.md` | `<YYYY-MM-DD>_pr_review_<slug>.md` |
| guide-create | `guide_<slug>.md` | `<YYYY-MM-DD>_guide_<slug>.md` |

### 그룹 ②: slug 파일을 읽는 스킬 (읽기 경로 업데이트)

| 스킬 | 읽는 파일 | 영향 |
|------|----------|------|
| implementation | implementation_plan + feature_draft | 두 파일 모두 slug로 변경됨. glob 패턴 업데이트 필요 |
| implementation-review | implementation_plan | glob 패턴 업데이트 필요 |
| spec-update-done | implementation_plan, review, report, feature_draft | 4개 파일 모두 slug로 변경됨. glob 패턴 업데이트 필요 |
| spec-summary | implementation_review | glob 패턴 업데이트 필요 |
| sdd-autopilot | 오케스트레이터가 파일 경로 명시 | 오케스트레이터 생성 시 slug 패턴 반영 필요 |

### 그룹 ③: prev/ 백업 로직 제거만 (파일명은 기존 유지)

| 스킬 | 제거 대상 |
|------|----------|
| spec-create | spec prev/ 백업 로직 |
| spec-update-todo | spec prev/ 백업 로직 |
| spec-update-done | spec prev/ 백업 로직 |
| spec-rewrite | spec prev/ 백업 로직 |
| spec-upgrade | spec prev/ 백업 로직 |
| spec-summary | summary prev/ 백업 로직 |

### 영향 없음 (변경 불필요)

discussion, investigate, ralph-loop-init, second-opinion, write-phased, git, spec-review, spec-snapshot

## 토론 흐름 (Discussion Flow)

Round 1: prev/ 제거 범위 → 전체 제거로 결정
Round 2: 스킬별 파일명 전략 (slug vs 덮어쓰기) → 사용자가 스킬별로 직접 지정
Round 3: 파일명 패턴 확인 → `<YYYY-MM-DD>_<filename>_<slug>.md`로 통일 (feature-draft 포함)
Round 4: 스킬 간 파일 참조 우려 → 기존 메커니즘(오케스트레이터 명시 전달 + glob)으로 충분함 확인
Round 5: 영향받는 스킬 전체 목록 → 17개 스킬, 3개 그룹으로 분류
Round 6: 적용 범위 확인 → `.claude/skills/` + `.codex/skills/` 양쪽 모두 동일 적용

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: prev/ 제거를 implementation과 spec 외에 다른 스킬에도 적용하시겠어요?
**Options**: 1) 전체 제거 2) implementation + spec만 3) 토론 종료
**A**: 전체 제거 (Recommended) 선택

### Round 2
**Q**: 덮어쓰기 스킬들의 파일 저장 방식을 어떻게 할까요?
**A**: 사용자가 직접 지정 — implementation 관련은 slug / spec은 덮어쓰기 / guide는 slug / pr도 slug

### Round 3
**Q**: 파일명 패턴 확인 — `implementation_plan_<slug>.md` 형태?
**A**: `<YYYY-MM-DD>_<filename>_<slug>.md` 패턴으로 변경. feature-draft도 동일 패턴 적용.

### Round 4
**Q**: slug 기반으로 바뀌면 스킬 간 파일 참조는 어떻게?
**A**: 기존에 feature-draft도 slug 기반인데 잘 동작하고 있음. 오케스트레이터 명시 전달 + glob 패턴으로 충분.

### Round 5
**Q**: 영향받는 스킬 전체 목록 확인
**A**: 17개 스킬 3개 그룹으로 분류된 영향 범위 확인 후 정리 요청.

### Round 6
**Q**: (사용자 추가 지적) agent/skill 미러와 .codex/skills 반영 필요
**A**: `.claude/skills/`와 `.codex/skills/` 양쪽 모두 동일하게 적용. `.codex/agents/*.toml`도 해당 시 업데이트.

## 적용 대상 디렉토리

| 위치 | 파일 유형 | 비고 |
|------|----------|------|
| `.claude/skills/<skill>/SKILL.md` | 스킬 정의 | Claude Code 스킬 |
| `.claude/agents/<skill>.md` | 에이전트 정의 | Claude Code 에이전트 (미러 원본) |
| `.codex/skills/<skill>/SKILL.md` | 스킬 정의 | Codex 스킬 (미러) |
| `.codex/skills/<skill>/skill.json` | 스킬 메타데이터 | Codex |
| `.codex/agents/<skill>.toml` | 에이전트 정의 | Codex 에이전트 (미러) |
