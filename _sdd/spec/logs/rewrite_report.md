# Rewrite Report — main.md 다이어트 (2026-08-18, v4.23.0)

## Metric Scorecard (전 → 후)

| 축 | 전 | 후 | 근거 |
|---|---|---|---|
| Thinness | 2/5 | 4/5 | 80KB → 61.7KB(-23%), 2500B 초과 줄 7 → 0 |
| Decision-bearing truth | 4/5 | 4/5 | 결정·가드·재제안 금지 조항 전량 보존, 서사만 decision_log 포인터화 |
| Anti-duplication | 2/5 | 4/5 | §2↔§3 이중 서술 4주제 해소, 훅 설치·ledger·승격 트리거 상세는 소유자 포인터로 |
| Navigation + surface fit | 3/5 | 4/5 | 불릿당 규모 축소로 §2 스캔 가능성 회복, 인덱스·Supporting Surfaces 불변 |
| Component Separation | 4/5 | 4/5 | 파일 구조 불변 |
| Findability | 2/5 | 4/5 | 거대 불릿 해체 |
| Boundary Clarity | 4/5 | 4/5 | 불변 |
| Canonical Fit | 2/5 | 4/5 | feature-level 상세가 SKILL/components/reference 포인터로 하강 |

## Canonical-fit 평가

- global spec은 `개념 + 경계 + 결정` 중심으로 복원됐다. §2 = 집행 문면(행동 규칙+가드), §3 비교표 = 결정+이유 캐노니컬로 역할 분리.
- 폐지 구조 서사는 "폐지 + 근거 1~2문장 + 재제안 금지 + decision_log 날짜 포인터" 형태로 통일. 압축 전 전 서사의 decision_log entry 실재를 grep으로 확인(2026-08-12/13/14/15/18, 2026-07-22) — 신규 이동 entry 필요 없음.

## Plan 대비 deviation

1. **목표 규모 미달**: plan 40±10KB 대비 61.7KB에서 중지 — 잔여 질량이 결정·가드 본문이라 추가 압축은 rationale 손실 위험(plan의 "무리한 추가 압축 금지" 원칙 우선). 의도적 중지.
2. **drift 수정 추가 수행**(plan 밖): 당일 v4.22.0(custom agent 폐지)이 못 미친 stale 표면 5곳(§1 agent layer 어휘·wrapper-backed guardrail·§3 실행 분리 행·핵심 설계 layer 목록·parity 제약)을 현재 truth로 갱신 — 창작이 아니라 기존 결정(v4.22.0)의 반영.
3. §2↔§3 dedup 4주제 중 override 주제는 §2=런타임 문법, §3=결정으로 이미 역할이 갈려 있어 무변경(중복 아님 판정).

## 보존 검증

- 재제안 금지 조항 6건 전량 잔존 확인(grep): 렌즈/task 재분할·수집 agent 재도입·Claim Manifest 축·사실 선고정 축·규모 판정 reviewer 복귀·2-렌즈.
- Source·Why·inline citation·링크 무결(스크립트 검증 broken links 0).
- append-only 검증: decision_log·changelog 삭제 줄 0.

## Unresolved / Warnings

- components.md row 29(implementation-review)가 3KB+ — "상세 reference" 역할 내이나 행 단위 가독 한계. 차기 검토 후보.
- usage-guide.md 미진단 — 차기.
- 목표 밴드(40±10KB) 대비 잔여 20KB는 §3 비교표(23행)와 §2 잔여 규칙이 보유 — 추가 다이어트는 결정 자체의 하강(예: 비교표 행의 supporting surface 분리)이 필요해 별도 판단 사안.
