# 토론 요약: plan-review 스킬 설계

**날짜**: 2026-06-02
**라운드 수**: 7
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)

- **사용자 문제 제기**: 에이전틱 코딩에서 간단한 기능도 과도한 설정, 추상화, 새 파일, 복잡한 구조로 부풀거나 반대로 한 파일에 기능을 욱여넣어 중복과 sloppy code가 생기는 문제가 있다.
- **토론을 시작한 배경**: `feature-draft`와 `implementation-plan`은 이미 `Target Files`, `Touchpoints`, `Contract/Invariant Delta`, `Validation Plan`, `Minimum-Code Mandate`로 계획 단계의 범위 제어를 시도하고 있다. 사용자는 `implementation-review`처럼 구현 전 계획 자체를 리뷰하는 `plan-review` 스킬을 추가하는 방안을 논의하고자 했다.
- **현재 상태**:
  - `.codex/skills/feature-draft/SKILL.md`는 Part 2 task에 `Target Files`를 강제하고, `Strategic Code Map`을 현재 코드로 재검증하며, 요청되지 않은 추상화/옵션/설정/에러 처리를 금지한다.
  - `.codex/skills/implementation-plan/SKILL.md`는 task/phase/dependency/validation linkage를 명시하고, 작은 delta는 compact linkage만 유지하도록 하며, 사변적 phase 분리를 금지한다.
  - `.codex/skills/implementation-review/SKILL.md`는 구현 후 상태를 findings-first로 검증하고, speculative code를 별도 assessment/finding 기준으로 다룬다.
  - 외부 `CLAUDE.md`는 Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution을 통해 가정 명시, 최소 코드, 외과적 변경, 검증 가능한 성공 기준을 강조한다.
- **범위와 제외 범위**:
  - 범위: 구현 전 implementation plan 또는 feature draft Part 2를 리뷰하는 독립 `plan-review` 스킬의 역할, 출력 방식, 게이트 강도, 루브릭, 저장 경로.
  - 제외 범위: 실제 스킬 파일 생성, agent mirror 작성, autopilot 통합 구현, 기존 스펙/스킬 수정.
- **수집한 근거**:
  - `.codex/skills/feature-draft/SKILL.md`
  - `.codex/skills/implementation-plan/SKILL.md`
  - `.codex/skills/implementation-review/SKILL.md`
  - `_sdd/spec/usage-guide.md`
  - `_sdd/spec/logs/changelog.md`
  - GitHub: `https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md`

## 핵심 논점 (Key Discussion Points)

1. **plan-review의 책임 경계**: 구현 결과가 아니라 구현 전 계획을 검토하는 review-only 스킬로 설계한다.
2. **리뷰 출력 방식**: 점수표보다 findings-first가 더 적합하다. 실제 수정해야 할 계획 결함을 severity별로 먼저 보여주고, 각 finding을 KISS/YAGNI/DRY/CLAUDE.md 원칙과 연결한다.
3. **게이트 강도**: 스킬 자체가 과잉 절차가 되지 않도록 Critical/High만 구현 전 차단한다. Medium/Low는 권고 또는 후속 개선으로 둔다.
4. **리뷰 축**: 원칙명 중심 섹션보다 작업 표면 중심이 실용적이다. Scope, Target Files, Task Boundaries, Validation 같은 plan 필드를 먼저 보고, 원칙은 finding의 근거로 사용한다.
5. **산출물 경로**: `_sdd/logs` 신설안도 검토했으나, 현재 repo에는 top-level `_sdd/logs`가 없고 `_sdd/spec/logs`는 spec 영역 전용이다. plan-review는 implementation plan을 검토하므로 `_sdd/implementation` 아래가 가장 일관적이다.
6. **세부 루브릭 형태**: 4개 CLAUDE 축을 그대로 섹션화하기보다 6개 smell 체크로 변환한다.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | `plan-review`는 독립 review-only 스킬로 설계한다. | `implementation-review`가 구현 후 검증을 담당하므로, 계획 단계의 과잉 설계와 범위 드리프트를 별도 게이트로 잡는 역할이 비어 있다. | 1 |
| 2 | 출력은 findings-first 구조를 사용한다. | 계획 결함은 구현자가 바로 고칠 수 있는 finding으로 제시되어야 하며, 점수표만으로는 구체적 수정 행동이 약해질 수 있다. | 2 |
| 3 | Critical/High finding만 구현 전 차단한다. | plan-review 자체가 작은 작업의 절차 비용을 키우면 YAGNI에 어긋난다. 명백한 위험만 차단하고 나머지는 권고로 둔다. | 3 |
| 4 | 리뷰 축은 작업 표면 중심으로 둔다. | `Target Files`, task boundary, validation linkage 같은 계획 필드를 직접 점검해야 sloppy implementation을 실제로 줄일 수 있다. | 4 |
| 5 | 기본 저장 경로는 `_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md`로 둔다. | 현재 top-level `_sdd/logs` 관례가 없고, `implementation-review`도 `_sdd/implementation` 아래에 저장된다. | 5 |
| 6 | 세부 루브릭은 6개 smell 체크를 기본으로 한다. | KISS/YAGNI/DRY/CLAUDE.md를 원칙명으로만 나열하면 추상적 리뷰가 되기 쉽다. smell 기반이면 수정 가능한 finding으로 이어진다. | 6 |

## 제안 루브릭 초안

| Smell | 점검 질문 | 연결 원칙 |
|-------|-----------|----------|
| Scope Creep | 계획에 사용자 요청, spec delta, AC에서 직접 나오지 않는 기능이 포함됐는가? | YAGNI, Simplicity First |
| New File Justification | `[C]` Target File이 기존 파일 수정으로 충분한데도 새 파일로 분리됐는가? 새 파일 생성 이유가 명시됐는가? | KISS, Surgical Changes |
| Single-use Abstraction | 한 곳에서만 쓰이는 helper, layer, config, interface가 생겼는가? | KISS, YAGNI |
| Task Boundary Drift | task가 하나의 명확한 목적을 넘어서거나, 서로 같은 파일/계약을 충돌되게 수정하는가? | Surgical Changes, DRY |
| DRY Risk | 같은 로직이나 상수를 여러 task/file에 중복 구현하도록 계획했는가? 반대로 중복이 작고 일회성인데 과한 추상화를 요구하는가? | DRY, KISS |
| Verification Weakness | success criteria와 validation이 C/I/V 또는 AC에 연결되지 않거나, “make it work” 수준으로 약한가? | Goal-Driven Execution |

## Severity 초안

| Severity | 기준 |
|----------|------|
| Critical | 계획대로 구현하면 핵심 요구사항을 잘못 구현하거나, 명백한 보안/데이터 손실/호환성 위험을 만든다. |
| High | Target Files, task boundary, validation이 잘못되어 구현 전에 계획 수정이 필요하다. 요청되지 않은 큰 추상화나 새 설정 체계도 여기에 포함될 수 있다. |
| Medium | 단일 사용처 추상화, 불필요한 새 파일, 애매한 AC 등 구현 품질을 떨어뜨릴 가능성이 크지만 즉시 차단까지는 필요하지 않다. |
| Low | 표현, 문서화, minor cleanup 수준의 계획 개선 제안이다. |

## 미결 질문 (Open Questions)

| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| 1 | `plan-review`를 autopilot 파이프라인에 자동 게이트로 넣을지, 수동 호출 스킬로 먼저 둘지 | deferred-deliberately | 이번 토론은 리뷰 전용 스킬의 기본 설계에 집중했고, 파이프라인 통합은 후속 feature draft에서 결정한다. |
| 2 | `.codex/agents/plan-review.toml` 및 `.claude` mirror까지 동시에 만들지 | deferred-deliberately | 실제 구현 단계에서 기존 mirror convention과 plugin/agent 구조를 확인한 뒤 결정한다. |

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | `plan-review` 스킬 생성을 위한 feature draft를 작성한다. | High | Codex |
| 2 | feature draft에 `New File Justification` 필드를 명시적으로 포함한다. | High | Codex |
| 3 | plan-review의 output contract를 findings-first + 6개 smell 체크 + severity 기준으로 설계한다. | High | Codex |
| 4 | autopilot 통합 여부는 별도 논의 또는 feature draft의 Risks/Open Questions로 남긴다. | Medium | Codex |

## 리서치 결과 요약 (Research Findings)

- **기존 plan 계열 스킬**: `feature-draft`와 `implementation-plan`은 이미 Minimum-Code Mandate, Target Files, C/I/V linkage, dependency/parallelism 판단을 통해 계획 단계의 범위 제어를 수행한다.
- **기존 review 계열 스킬**: `implementation-review`는 구현 후 findings-first 검증을 담당한다. plan-review는 이 구조를 차용하되, 대상은 코드가 아니라 구현 전 계획이어야 한다.
- **CLAUDE.md 원칙**: 가정 명시, 최소 코드, 불필요한 flexibility/configurability 금지, 변경 라인의 요청 추적성, 검증 가능한 성공 기준이 plan-review 루브릭의 근거로 적합하다.
- **경로 관례**: 현재 repo에는 top-level `_sdd/logs`가 없고, `_sdd/spec/logs`는 spec 영역에서 사용된다. implementation plan 검토 리포트는 `_sdd/implementation` 아래가 더 일관적이다.

## 토론 흐름 (Discussion Flow)

Round 1: 토론 범위 선택 -> `plan-review`를 리뷰 전용 독립 스킬로 우선 설계하기로 함.

Round 2: 리뷰 방식 선택 -> findings-first 구조를 채택.

Round 3: 게이트 강도 선택 -> Critical/High만 구현 전 차단하고 Medium/Low는 권고로 둠.

Round 4: 리뷰 축 선택 -> 원칙명 중심보다 작업 표면 중심으로 설계.

Round 5: 산출물 위치 논의 -> `_sdd/logs` 가능성을 검토했으나 `_sdd/implementation`을 채택.

Round 6: 세부 루브릭 다듬기 여부 -> smell 체크 루브릭을 한 라운드 더 논의.

Round 7: 루브릭 형태 선택 -> 6개 smell 체크를 채택.

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: `plan-review` 스킬 논의에서 우선 어느 범위를 중심으로 잡을까요?
**Options**: 1) 리뷰 전용 설계 2) 워크플로우 통합 3) 정리/종료
**A**: 리뷰 전용 설계
**Follow-up**: 독립 스킬로 보고 기존 스킬과 외부 원칙을 확인하기로 함.

### Round 2
**Q**: `plan-review`의 기본 판정 방식을 어떤 형태로 잡는 게 좋을까요?
**Options**: 1) Findings-first 2) Scorecard 중심 3) 정리/종료
**A**: Findings-first
**Follow-up**: severity별 finding을 KISS/YAGNI/DRY/CLAUDE 원칙과 연결하는 방향으로 정리.

### Round 3
**Q**: `plan-review`가 발견한 문제를 후속 구현 전에 어느 정도까지 막아야 할까요?
**Options**: 1) Critical/High만 차단 2) Medium까지 차단 3) 정리/종료
**A**: Critical/High만 차단
**Follow-up**: plan-review 자체가 절차 과잉이 되지 않도록 게이트를 가볍게 유지.

### Round 4
**Q**: `plan-review`의 리뷰 축은 어떤 구조가 가장 실용적일까요?
**Options**: 1) 작업 표면 중심 2) 원칙명 중심 3) 정리/종료
**A**: 작업 표면 중심
**Follow-up**: 실제 plan 필드를 기준으로 보고 원칙은 finding 근거로 연결.

### Round 5
**Q**: `plan-review` 리포트는 어디에 저장하는 게 자연스러울까요?
**Options**: 1) `_sdd/implementation` 2) `_sdd/review` 3) 정리/종료
**A**: `_sdd/logs` 가능성을 제안
**Follow-up**: repo 관례를 확인한 뒤 top-level `_sdd/logs`는 없고 `_sdd/spec/logs`만 있음을 확인.

### Round 5-2
**Q**: 이 관례를 기준으로 `plan-review` 경로를 어떻게 잡는 게 좋을까요?
**Options**: 1) `_sdd/implementation` 2) `_sdd/logs` 신설 3) 정리/종료
**A**: `_sdd/implementation`
**Follow-up**: plan-review 리포트는 implementation plan 검토 산출물로 `_sdd/implementation`에 둠.

### Round 6
**Q**: 이제 토론을 정리할까요, 아니면 `plan-review`의 세부 루브릭을 한 라운드 더 다듬을까요?
**Options**: 1) 세부 루브릭 다듬기 2) 정리/종료
**A**: 세부 루브릭 다듬기
**Follow-up**: 원칙명을 직접 섹션화할지, smell 체크로 변환할지 논의.

### Round 7
**Q**: 세부 루브릭은 어떤 형태가 가장 좋을까요?
**Options**: 1) 6개 smell 체크 2) 4개 CLAUDE 축 3) 정리/종료
**A**: 6개 smell 체크
**Follow-up**: Scope Creep, New File Justification, Single-use Abstraction, Task Boundary, DRY Risk, Verification Weakness를 기본 smell로 정리.

### 종료
**Q**: 지금 합의한 내용으로 토론 요약 문서를 저장할까요?
**Options**: 1) 정리/종료 2) 한 라운드 더
**A**: 정리/종료
**Follow-up**: 본 문서를 생성.
