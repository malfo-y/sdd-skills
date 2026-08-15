# 토론 요약: SDD 전용 하네스 작업 원칙

**날짜**: 2026-08-11
**라운드 수**: 6
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)
- **사용자 문제 제기**: 현재 `AGENTS.md` §0의 네 원칙은 SDD 고유 원칙이 아니라 일반적인 agent 작업 원칙이며, 사용자마다 이미 개인 하네스를 가질 수 있는데 SDD bundle이 이를 별도로 배포하는 것이 맞는지 의문을 제기했다.
- **토론을 시작한 배경**: 직전 작업에서 §0 원칙과 `plan-review` 분류 어휘의 인위적 결합을 제거한 뒤, §0 자체가 SDD harness에서 소유할 가치가 있는지 재검토할 필요가 생겼다.
- **현재 상태**: `AGENTS.md`와 네 배포 template은 `Think Before Coding`·`Simplicity First`·`Surgical Changes`·`Goal-Driven Execution`을 모든 작업의 우선 원칙으로 배포한다. 상세 해설은 `docs/agentic_coding_principle.md`가 소유한다. SDD 고유 계약은 global/temporary spec 분리, evidence 기반 truth 승격, `_sdd/` artifact handoff, producer-owned gate와 `spec-sync`에 흩어져 있다.
- **범위와 제외 범위**: §0을 일반 원칙에서 SDD 고유 실패 방지 불변식으로 재설계하는 것만 논의했다. 실제 파일 수정, `plan-review` rubric 변경, 상세 workflow 절차 재설계는 제외했다.
- **수집한 근거**: `AGENTS.md` §0~§3, `_sdd/spec/main.md`, `docs/SDD_CONCEPT.md`, `docs/SDD_WORKFLOW.md`, `docs/SDD_SPEC_DEFINITION.md`, `feature-draft`·`implementation`·`spec-sync` skill 계약의 truth lifecycle·evidence·artifact 관련 문면.

## 핵심 논점 (Key Discussion Points)
1. **하네스 소유권**: 일반 agent 품질 원칙은 개인·조직 하네스와 중복되기 쉽고 SDD bundle이 강제 배포할 고유 계약이 아니다.
2. **원칙의 역할**: 새 §0은 SDD 방법론 설명이나 skill 순서 복제가 아니라, truth 혼합·evidence 없는 승격·handoff 소실/과잉 기록이라는 고유 실패를 막아야 한다.
3. **truth 승격 조건**: `spec-sync`를 구현마다 자동 실행하라는 원칙은 부적절하다. 목표와 AC에 비춰 기대 결과가 검증된 outcome만 current truth로 승격해야 하며, 사람 사용자의 명시적 승인은 필수 조건이 아니다.
4. **artifact 범위**: 모든 사고 과정이나 단계별 진행기를 기록하지 않고, 다음 단계 또는 세션 재개에 필요한 결정과 evidence만 보존해야 한다.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| 1 | §0의 일반 agent 4원칙을 SDD 전용 원칙으로 교체한다. | 개인 하네스와의 중복 우려 및 SDD bundle 소유 경계에 대한 사용자 선택 (`사용자 판단`) | 하네스 소유권 |
| 2 | 새 원칙은 방법론 요약이 아니라 SDD 실패 방지 불변식으로 둔다. | 기존 §2~§5와 skill이 절차를 이미 소유한다는 로컬 문서 확인 (`코드 확인`) | 원칙의 역할 |
| 3 | **Separate Truth by Lifetime** — repo-wide decision은 global spec에, change-specific execution detail은 temporary artifact에 둔다. | global/temporary spec 분리가 SDD 정의와 workflow 전반에 반복되는 경계임을 확인 (`코드 확인`) | truth 혼합 방지 |
| 4 | **Evidence Before Promotion** — goal과 AC가 검증된 outcome만 current truth로 승격하고, 나머지는 planned/unverified로 둔다. | 사용자가 “명시적 사용자 승인”이 아니라 “목표가 기대대로 달성됨”을 조건으로 확정 (`사용자 판단`) | truth 승격 조건 |
| 5 | **Persist Handoffs, Not Process** — 다음 단계나 재개에 필요한 결정·evidence만 기록하고 재현 가능한 과정 서술은 남기지 않는다. | artifact bureaucracy를 막으면서 세션 기억 의존을 제거하는 범위로 사용자가 선택 (`사용자 판단`) | artifact 범위 |

### 기각한 대안
- **일반 원칙 + SDD 원칙의 두 층 병존**: 개인/조직 하네스와 중복되는 일반 원칙을 SDD bundle이 계속 배포하는 문제가 남는다.
- **Traceability + Convergence 2축 압축형**: 간결하지만 global/temporary lifetime 경계와 handoff 범위가 암묵화되어 실패 진단력이 약하다.
- **skill 순서·producer gate 중심 절차 원칙**: §3과 각 skill 계약의 단일 소스를 다시 요약해 drift 표면을 늘린다.
- **Close the Spec Loop를 별도 4번째 원칙으로 유지**: 구현마다 즉시 `spec-sync`하라는 지시로 오독될 수 있고, 검증된 outcome만 승격한다는 두 번째 원칙과 중복된다.

## 미결 질문 (Open Questions)
| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| — | 없음 | — | 토론 범위 안의 결정이 모두 닫힘 |

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | `feature-draft`로 §0 3원칙 교체의 전파면·AC를 계획한다. | High | 후속 SDD 작업 |
| 2 | `AGENTS.md`와 spec-create/spec-upgrade의 Claude·Codex harness template 4벌을 동일하게 갱신한다. | High | 후속 implementation |
| 3 | global spec의 §0 설명을 새 SDD 원칙에 맞추고 과거 일반 원칙 배포 결정을 supersede한다. | High | 후속 spec-sync |

### 후속 핸드오프 (Handoff)
- **목표**: live harness 5개 표면의 §0이 합의한 세 SDD 원칙과 정확히 일치하고, 기존 일반 4원칙 및 그 상세 문서 포인터가 §0에서 제거되며, global current truth가 이를 반영한다.
- **변경 금지 제약**: `plan-review`의 reviewer-local `Principle Link` rubric, §1~§5의 상세 workflow/검증/work-log 계약, 과거 draft·implementation·decision/changelog 이력은 변경하지 않는다.
- **검증**: harness 5표면 hash parity, 기존 4원칙·`docs/agentic_coding_principle.md` §0 포인터 live 잔존 0, 새 3원칙 각 5건, global spec current truth 정합, `git diff --check`.
- **중단 조건**: 새 원칙이 §2~§5의 절차를 재서술해야만 성립하거나, `Evidence Before Promotion`이 구현마다 무조건 implemented `spec-sync`를 요구하는 문면으로 변하면 중단하고 토론 결정을 재확인한다.

## 리서치 결과 요약 (Research Findings)
- `docs/SDD_SPEC_DEFINITION.md`는 global spec을 repo-wide Single Source of Truth, temporary spec을 변경 실행 청사진으로 구분한다.
- `spec-sync` 계약은 evidence가 없는 delta를 planned로, 코드만 있고 검증이 약한 delta를 unverified로 두며, verified outcome만 current truth로 승격한다.
- `_sdd/spec/main.md`는 persistent handoff를 `_sdd/` canonical artifact로 유지하고, implementation ledger는 재실행으로 복원할 수 없는 사실만 기록하도록 제한한다.
- workflow 순서와 gate 소유권은 이미 `AGENTS.md` §3과 각 producer skill이 소유하므로 §0에서 반복할 필요가 없다.

## 토론 흐름 (Discussion Flow)
Round 1: §0 재설계 범위 → 일반 원칙을 SDD 전용 원칙으로 교체
Round 2: 원칙의 우선 역할 → SDD 실패 방지 불변식
Round 3: 4축형과 2축형 비교 → 4축 방향을 선호하되 자동 spec-sync로 읽히는 네 번째 축에 이의 제기
Round 4: 사용자 검증 조건 → 사람의 명시적 승인이 아니라 목표·기대 결과 달성 evidence로 확정
Round 5: artifact 원칙의 과잉 기록 위험 → handoff·resume에 필요한 상태만 기록
Round 6: 최종 3축 문면 → 채택 후 정리

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: §0을 SDD 전용으로 교체할지, 일반 원칙과 병존할지
**Options**: 1) SDD 전용으로 교체 2) 두 층으로 병존 3) 여기서 정리
**A**: SDD 전용으로 교체
**Follow-up**: 현재 SDD 문서에서 고유 불변식 후보를 로컬 탐색

### Round 2
**Q**: 새 원칙이 실패 방지 불변식과 방법론 요약 중 무엇을 우선할지
**Options**: 1) 실패 방지 불변식 2) 방법론 요약 3) 여기서 정리
**A**: 실패 방지 불변식
**Follow-up**: truth lifetime·evidence promotion·artifact handoff·loop closure 후보 제시

### Round 3
**Q**: 4축 불변식과 2축 압축형 중 선택
**Options**: 1) 4축 불변식 2) 2축 압축형 3) 여기서 정리
**A**: 마지막 loop closure는 구현마다 spec-sync하라는 지시로 오독될 수 있으므로 제외하고 나머지는 동의
**Follow-up**: implemented sync의 실제 승격 조건을 재질문

### Round 4
**Q**: implemented sync 전에 사람 사용자의 명시적 수용이 필요한 범위
**Options**: 1) 항상 명시적 수용 2) 사용자 영향 변경만 3) 미결로 정리
**A**: 사람의 명시적 검증은 필수가 아니며 목표가 기대한 대로 달성되면 수행
**Follow-up**: `Evidence Before Promotion`에 goal·AC evidence 조건으로 흡수

### Round 5
**Q**: artifact 기록 범위를 handoff만으로 제한할지 모든 단계에 의무화할지
**Options**: 1) 핸드오프만 기록 2) 단계마다 의무 기록 3) 미결로 정리
**A**: 핸드오프만 기록
**Follow-up**: `Persist Handoffs, Not Process`로 문면 축소

### Round 6
**Q**: 최종 세 원칙을 채택할지 문구를 더 다듬을지
**Options**: 1) 3축 채택 후 정리 2) 문구 더 다듬기 3) 결정 없이 종료
**A**: 3축 채택 후 정리
**Follow-up**: 후속 feature-draft가 소비할 결정과 제약을 확정
