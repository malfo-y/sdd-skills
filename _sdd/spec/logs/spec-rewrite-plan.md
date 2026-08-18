# Spec Rewrite Plan — main.md 다이어트 (2026-08-18)

## 진단 요약 (canonical-fit rationale)

- main.md 197줄 / 80KB. 자칭 thin global spec이나 §2 Guardrails와 §3 비교표가 스킬 계약 상세·폐지 구조 서사·실측 내러티브를 본문에 보유해 Canonical Fit 위반.
- Scorecard: Thinness 2/5 · Decision-bearing 4/5 · Anti-dup 2/5 · Nav/surface 3/5 · Component Separation 4/5 · Findability 2/5 · Boundary Clarity 4/5 · Canonical Fit 2/5.
- 3대 비대 원인: ① §2↔§3 이중 서술(같은 결정을 Guardrail 산문과 비교표 행이 각각 보유) ② 폐지 구조의 전체 서사 잔존(gather phase 3세대 서사·Claim Manifest·2-렌즈 철회·1+N shard — 결정은 "폐지 + 재제안 금지"인데 도입~폐지 내러티브 전체가 본문) ③ 스킬 계약 상세 재서술(승격 트리거 6종 열거·7필드 열거·ledger 필드 구성·PROMPT 규칙 등 — SKILL/components.md가 이미 단일 소스 선언됨).

## main에 남길 것 (보존 원칙)

- §1 전체(문제 정의·컨셉·대안 표) — 무변경.
- §2: 각 Guardrail의 **행동 규칙 + 결정 1~3문장 + 재제안 금지 가드 + 소유자 포인터**. 모든 재제안 금지 조항(2-렌즈 재분할·Claim Manifest·사실 선고정 축·규모 판정 reviewer 복귀 금지 등)은 문장 단위로 보존한다.
- §3 비교표: 결정·이유의 캐노니컬 표면으로 유지(행 압축은 §2와의 중복 해소분만).
- 운영 제약: 관측 상태(Planned/종결/음성 n=1 등 판정 상태)와 판정 기준은 유지, 회차별 수치 내러티브는 압축.
- Hard Rule 2 대상(Source·Why·inline citation) 전부 유지.

## 이동/압축할 것 (placement rule)

- **§2↔§3 중복**: 결정+이유는 §3 비교표가 소유, §2는 행동 규칙(집행 문면)만 소유 — 동일 명제 이중 서술 제거. 게이트 정책·test-first·2-렌즈·override 4주제.
- **폐지 구조 서사**: gather phase(:83)·Claim Manifest(:90)·1+N shard·2-렌즈 철회(:82,:182)의 도입~폐지 내러티브는 "폐지됨 + 근거 요약 1문장 + 재제안 금지 + decision_log 날짜 포인터"로 압축. 서사 원문은 이미 decision_log에 있음(신규 이동 불필요 — 포인터 확인 후 없는 것만 decision_log 신규 entry로 내림).
- **스킬 계약 상세**: 승격 트리거 6종·7필드·ledger 필드·PROMPT 상세 열거는 소유자(SKILL/components.md 행) 포인터로 대체 — main에는 규칙의 존재와 형태(예: "hunk 기본 + 트리거 승격 + hunk-scoped 표기")만.
- **관측 로그(:179-185)**: 판정 상태·기준·다음 행동만 남기고 회차 수치 서사는 decision_log 포인터로.

## Split map

- 파일 분할 없음 — 기존 main/components/usage-guide/기록물 구조 유지(Hard Rule 9). main.md 내부 압축만.

## Ambiguity / Risk

- **최대 위험 = rationale 손실**: 이 spec의 거대 불릿들은 사용자가 의도적으로 축적한 가드·supersede 서사다. 압축 시 "결정·가드·재제안 금지"는 전량 보존하고 "서사·수치"만 내린다. 문장 단위 보존 목록을 실행 중 대조한다.
- decision_log에 대응 entry가 없는 서사가 발견되면 임의 삭제하지 않고 decision_log에 신규 entry로 먼저 내린 뒤 본문을 압축한다(창작 아님 — 이동).
- 목표 규모: main.md 80KB → 40±10KB. 무리한 추가 압축으로 결정을 깎지 않는다.

## 실행 순서 + deviation 규칙

1. §2 Guardrails 불릿별 압축(대응 decision_log entry 확인 → 없으면 이동 entry 작성 → 본문 압축) — 대형 불릿 순(:83, :63, :88, :59, :78-79, :90-92, :94-96).
2. §2↔§3 중복 4주제 해소.
3. 운영 제약 압축.
4. 링크·앵커 검증, version bump + changelog, rewrite_report 작성.
- deviation은 rewrite_report에 plan 대비 항목별 기록.

## 대상 파일

- `_sdd/spec/main.md` (본문 압축) / `_sdd/spec/decision_log.md` (append-only 이동 entry, 필요분만) / `_sdd/spec/logs/changelog.md` (version entry) / `_sdd/spec/logs/rewrite_report.md` (신규 갱신)
- components.md·usage-guide.md는 이번 범위 밖(components 행 비대는 "상세 reference" 역할 내 — 차기 검토 warning으로만 남김).

## Warning으로만 남길 것

- components.md row 29(implementation-review)가 3KB+로 행 단위 가독 한계 — 이번엔 미조정.
- usage-guide.md 미진단 — 차기.
