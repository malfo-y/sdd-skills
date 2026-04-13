# Summary Example

## Reader-Facing Whitepaper

### Executive Summary
이 저장소의 `summary.md`는 SDD를 단순한 문서 집합이 아니라, 토론부터 계획, 구현, 검증, 스펙 동기화까지 이어지는 작업 시스템으로 읽게 해 주는 reader-facing whitepaper다. 독자는 이 문서 하나만 읽어도 왜 이런 구조를 택했는지, 핵심 설계가 무엇인지, 실제 근거가 어디 있는지, 어떤 흐름으로 사용하는지를 빠르게 파악할 수 있어야 한다.

### Background / Motivation
- problem: 스펙, 계획, 구현, 리뷰가 서로 다른 surface에 흩어지면 사람과 에이전트가 같은 판단 기준을 유지하기 어렵다.
- why this matters now: 이 저장소는 여러 skill이 같은 `_sdd/` workflow를 공유하므로, repo-level 의도와 실행 구조를 읽기 쉬운 설명 surface가 필요하다.
- alternatives considered: 하나의 두꺼운 global spec에 모든 설명을 몰아넣거나, 반대로 코드와 개별 guide만으로 탐색을 맡기는 방식도 가능하다. 전자는 유지 부담이 크고 후자는 존재 이유와 설계 맥락을 복원하기 어렵다.
- why this approach: thin global spec은 장기 판단을 고정하고, `summary.md`는 그 판단을 배경/동기/설계/코드 근거/사용 기대 결과까지 확장해 설명하는 whitepaper 역할을 맡는다.

### Core Design
- core idea: SDD는 thin global spec, temporary spec, implementation artifact를 분리해 long-lived truth와 execution truth를 다르게 관리한다.
- logic flow or algorithm spine: discussion으로 방향을 잡고, feature draft로 delta를 고정하고, implementation/review로 evidence를 쌓은 뒤, spec sync와 summary surface가 인간 친화적 설명과 장기 SoT를 각각 닫는다.
- structural decisions:
  - global spec은 repo-wide 판단 기준을 고정한다.
  - feature draft와 implementation artifact는 실행 청사진과 evidence를 담는다.
  - `spec-summary`는 이 구조를 사람 친화적 whitepaper로 풀어쓰고 더 깊은 surface로 연결한다.
- important guardrails or boundaries:
  - summary는 exhaustive inventory를 복제하지 않는다.
  - 핵심 설계 설명에는 concrete code grounding이 들어간다.
  - 계획/진행 상태는 appendix에만 둔다.

### Code Grounding
선호 citation 스타일은 concrete path 또는 `[path:symbol]` 계열 anchor다.

| Topic | Paths / Symbols | Why It Matters |
|---|---|---|
| Global spec anchor | `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md` | repo-level 판단 기준과 supporting surface가 어디에 놓이는지 보여준다 |
| Temporary execution model | `.codex/skills/feature-draft/SKILL.md`, `.codex/skills/implementation/SKILL.md`, `.codex/skills/implementation-review/SKILL.md` | 계획, 실행, 리뷰가 어떤 skill로 이어지는지 드러낸다 |
| Orchestration layer | `.codex/skills/sdd-autopilot/SKILL.md`, `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` | end-to-end 파이프라인이 어떤 규칙으로 조합되는지 설명한다 |
| Summary surface itself | `.codex/skills/spec-summary/SKILL.md`, `.codex/skills/spec-summary/references/summary-template.md` | whitepaper output contract와 section expectation의 직접 근거다 |

### Usage / Expected Results
- how to use or read this project:
  - `/discussion`으로 방향과 개념을 정리한다.
  - `/feature-draft`로 temporary spec과 구현 범위를 고정한다.
  - `/implementation`과 `/implementation-review`로 실행과 검증을 닫는다.
  - `/spec-summary`는 현재 구조를 사람이 읽기 좋은 whitepaper로 정리한다.
- expected result:
  - 독자는 `summary.md`만 읽어도 문제, 동기, 핵심 설계, 코드 근거, 사용 흐름을 연결해서 말할 수 있다.
  - deeper detail이 필요하면 linked guide, docs, `_sdd/drafts/`, `_sdd/implementation/`으로 자연스럽게 내려갈 수 있다.
- guarantees or observable behaviors:
  - summary는 현재 기준의 계약과 구조를 직접 설명한다.
  - 계획/진행 상태는 whitepaper 본문을 침범하지 않고 appendix에만 남는다.
- failure or exception boundary:
  - spec이 부족하거나 code grounding anchor가 약하면 summary는 이를 보강할 surface를 먼저 찾고, 충분한 anchor 없이 일반론으로 채우지 않는다.

### Further Reading / References
- global spec anchor: `_sdd/spec/main.md`
- supporting spec docs: `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`, `_sdd/spec/DECISION_LOG.md`
- canonical docs: `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md`
- execution artifacts: `_sdd/drafts/`, `_sdd/implementation/`

### Appendix: Planned / Progress Snapshot (Optional)
- planned: spec-summary contract와 repo docs를 같은 whitepaper 의미로 정렬
- in progress: downstream reference sync
- next: `_sdd/spec/` supporting docs 반영 및 final review
