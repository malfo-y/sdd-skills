# 스펙 기반 개발(SDD) 워크플로우 가이드

**버전**: 2.0.0
**날짜**: 2026-04-04

이 문서는 현재 SDD canonical model과 실제 skill behavior를 기준으로, 스펙이 어떻게 생성되고 읽히고 검증되고 동기화되는지 설명한다.

관련 문서:
- [SDD_SPEC_DEFINITION.md](SDD_SPEC_DEFINITION.md)
- [SDD_CONCEPT.md](SDD_CONCEPT.md)
- [SDD_QUICK_START.md](SDD_QUICK_START.md)
- [sdd.md](sdd.md)

---

## 1. 핵심 모델

SDD는 하나의 문서 형식을 모든 상황에 강요하지 않는다. 대신 공통 코어를 공유하는 두 종류의 스펙을 사용한다.

### 글로벌 스펙

글로벌 스펙은 프로젝트의 장기적 Single Source of Truth다. 구현 inventory를 전부 적는 문서가 아니라, 사람과 AI가 같은 기준으로 판단하도록 만드는 얇은 기준 문서다.

핵심 본문:
- 배경 및 high-level concept
- Scope / Non-goals / Guardrails
- 핵심 설계와 주요 결정
- Contract / Invariants / Verifiability
- 사용 가이드 & 기대 결과
- Decision-bearing structure

선택적 보조 영역:
- 데이터 모델 / API / 환경 및 설정
- Strategic Code Map appendix
- 관련 문서 및 코드 레퍼런스

### Temporary Spec

temporary spec은 글로벌 스펙의 축약 복사본이 아니라, 변경을 실행하기 위한 청사진이다. `feature-draft`, `implementation-plan`, `spec-update-todo`, `spec-update-done`, `sdd-autopilot`은 이 구조를 전제로 동작한다.

canonical 7섹션:
- Change Summary
- Scope Delta
- Contract/Invariant Delta
- Touchpoints
- Implementation Plan
- Validation Plan
- Risks / Open Questions

### CIV는 공통 품질 게이트다

SDD의 공통 코어는 `Contract / Invariants / Verifiability`다.

- 글로벌 스펙은 독립 섹션으로 `Contract`, `Invariants`, `Verifiability`를 가진다.
- temporary spec은 `Contract/Invariant Delta`와 `Validation Plan`으로 같은 의미를 표현한다.
- ID(`C1`, `I1`, `V1`)와 verification enum(`test`, `review`, `runtime-check`, `manual-check`)은 추적성과 검증 연결의 기준이다.

---

## 2. 문서 갱신 순서

canonical model이 바뀌면 아래 순서를 따른다.

1. definition 문서 갱신
2. generator / transformer skill 갱신
3. consumer / planner / updater / orchestrator skill 갱신
4. human-facing docs 갱신
5. english mirror / example / collateral sync

이 순서를 지키는 이유는 단순하다. 설명 문서가 실제 skill output보다 앞서가면 시스템이 split-brain 상태가 되기 때문이다.

---

## 3. 시작점 선택

### 기본 경로

대부분의 기능 구현은 `/sdd-autopilot`으로 시작한다.

```bash
/sdd-autopilot 이 기능 구현해줘: [기능 설명]
```

### 방향이 모호할 때

요구사항이나 설계 방향이 불명확하면 `/discussion`으로 먼저 결정한다.

```bash
/discussion
실시간 알림을 SSE로 할지 WebSocket으로 할지 결정해야 해.
```

### 스펙이 없을 때

프로젝트를 문서화해야 하면 `/spec-create`를 사용한다.

### 구형 스펙이 남아 있을 때

legacy spec을 현재 canonical global spec model로 옮겨야 하면 `/spec-upgrade`를 사용한다. 이 스킬은 더 이상 과거의 numbered whitepaper converter가 아니다.

---

## 4. 규모별 워크플로우

| 규모 | 권장 경로 | 설명 |
|------|-----------|------|
| 대규모 | `feature-draft → spec-update-todo → implementation-plan → implementation → implementation-review → spec-update-done` | 장기 작업. temporary spec과 plan을 먼저 고정하고 phase 단위로 검증한다. |
| 중규모 | `feature-draft → implementation → spec-update-done` | temporary spec과 구현 계획을 한 파일로 만들고 바로 구현한다. |
| 소규모 | 직접 구현 → 필요 시 `implementation-review` / `spec-update-done` | 변경 범위가 작고 delta가 명확할 때 사용한다. |

보조 경로:
- `/spec-review`: strict review report가 필요할 때만 사용한다.
- `/spec-summary`: 현재 spec 상태를 빠르게 파악할 때 사용한다.
- `/spec-rewrite`: 스펙 구조 자체가 비대해져 정리가 필요할 때 사용한다.
- `/guide-create`: 특정 기능 deep-dive guide가 필요할 때 사용한다.

---

## 5. 스킬 역할

| 스킬 | 역할 |
|------|------|
| `/spec-create` | 코드/초안에서 current canonical global spec 생성 |
| `/spec-upgrade` | legacy spec을 current canonical global spec model로 마이그레이션 |
| `/feature-draft` | temporary spec draft + implementation plan 생성 |
| `/spec-update-todo` | planned persistent information을 글로벌 스펙에 사전 반영 |
| `/implementation-plan` | large-scale 작업을 phase/task로 분해 |
| `/implementation` | plan 또는 draft 기반 구현 실행 |
| `/implementation-review` | plan 대비 구현 상태와 acceptance criteria 검증 |
| `/spec-update-done` | implemented + verified persistent truth를 글로벌 스펙에 반영 |
| `/spec-review` | 스펙 품질, drift, CIV 충실도, global/temporary 정합성 리뷰 |
| `/spec-summary` | global spec과 temporary spec을 다른 방식으로 요약 |
| `/spec-rewrite` | 지나치게 두꺼운 스펙을 canonical model 기준으로 재구성 |
| `/discussion` | 구조화된 결정 토론 |
| `/guide-create` | 기능별 implementation/review guide 생성 |
| `/sdd-autopilot` | end-to-end 오케스트레이션 |
| `/ralph-loop-init` | 장시간 실행 디버그 루프 초기화 |

---

## 6. 좋은 입력의 기준

스킬은 마법이 아니라 구조화된 워크플로우다. 입력이 약하면 산출물도 약해진다.

최소 입력 원칙:
- What: 무엇을 바꾸는가
- Why: 왜 이 변경이 필요한가
- Constraints: 어떤 경계와 제약이 있는가

좋은 입력 예시:

```text
/feature-draft
CSV 업로드 후 자동 파싱하여 users 테이블에 bulk insert하는 기능.
- 최대 10MB
- 컬럼 매핑은 UI에서 수동 지정
- 에러 행은 건너뛰고 리포트 생성
- 수동 입력이 너무 느려서 대량 등록용으로 필요
```

부족한 정보는 skill이 best-effort로 보완할 수 있지만, 불확실성은 `Risks / Open Questions`로 남는다.

---

## 7. 아티팩트 배치

주요 디렉토리:

```text
_sdd/
├── spec/              # 글로벌 스펙과 supporting spec
├── drafts/            # feature-draft 산출물
├── implementation/    # plan, progress, report, review
├── discussion/        # discussion handoff와 기록
├── guides/            # guide-create 산출물
└── env.md             # 환경/검증 힌트
```

운영 원칙:
- 글로벌 스펙은 `_sdd/spec/`에서 관리한다.
- temporary spec과 구현 계획은 `_sdd/drafts/`, `_sdd/implementation/`에서 순환한다.
- 환경 및 실행 제약은 `_sdd/env.md`를 기준으로 본다.

---

## 8. 워크플로우 요약

```mermaid
flowchart LR
    Req["요구사항"] --> Draft["Temporary Spec / Plan"]
    Draft --> Impl["구현"]
    Impl --> Review["검증"]
    Review --> Sync["Global Spec Sync"]
    Sync -.-> Ref["Global Spec"]
    Ref -.-> Draft
```

한 문장으로 요약하면 이렇다.

> 글로벌 스펙은 장기 기준을 고정하고, temporary spec은 변경 실행을 안내하며, skillchain은 둘 사이의 계약과 검증 연결을 유지한다.
