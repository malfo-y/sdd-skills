# Feature Draft: plan-review 읽기 다이어트 — digest 신뢰 격상 + spec 읽기 한정

> 규모 판정: 적격 — 변경 요소 3개(digest 신뢰·spec 한정·기록물 금독)가 한 읽기 규칙 블록에 귀속, task 2개로 coverage 눈검산 가능

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
gather phase 발효 후 첫 소비 repo 실측(사용자 관측, 원격 GPU 서버)에서 역효과 2종이 드러났다: ① 판정 agent가 digest를 받고도 **원본 코드를 처음부터 재독** — 현행 문면 "Critical/High evidence는 원본 파일 residual read로 확정한다"가 전면 재검증 지시로 읽혀 gather 비용 + 재독 비용의 순손실 ② spec이 커질수록 **draft가 인용하지 않은 spec 표면까지 로밍** — 스펙 대조 비용이 변경 크기가 아니라 스펙 크기(실측 main.md 78K·decision_log 441K)에 비례.

새 contract/invariant (plan-review-agent 읽기 규칙 개정):
- **digest 신뢰 격상**: digest 발췌는 `경로:줄범위` 앵커가 붙은 verbatim이므로 **원본 인용과 동급 evidence다** — Critical/High 포함 모든 severity의 evidence로 그대로 인용하며, 발췌가 이미 담은 구간을 원본에서 다시 읽지 않는다. residual read는 두 경우만: 판정에 필요한 구간이 digest에 좌표로만 남았을 때(발췌 상한 초과분), 발췌 범위 밖 문맥 없이는 판정이 닫히지 않을 때. (기존 "원본 residual read로 확정" 의무 문면을 대체 — false CLEAR 방어는 gatherer의 verbatim·앵커 계약이 담당)
- **spec 읽기 anchor 한정**: spec surface(`_sdd/spec/*`)는 draft가 명시 인용한 파일·섹션만 읽는다. 인용 없는 spec 대조는 수행하지 않고 그로 인한 finding도 만들지 않는다 — 전 스펙 대비 어긋남 감시는 `spec-review` 소관.
- **기록물 금독**: `decision_log.md`·`logs/`·`prev/`는 리뷰 입력이 아니다.
- Claim Manifest 재제안 금지와 무관 — producer ceremony 추가 없이 reviewer 읽기 범위만 규정.

## Scope
- **In**: plan-review-agent 읽기 규칙(claude .md + codex .toml 3-way), 문구 census
- **Out**: gatherer·orchestrator(SKILL.md) 계약 변경, implementation-review/pr-review 이식, spec 자체 다이어트(별도 트랙)
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: plan-review-agent 읽기 규칙 개정 (claude + codex 3-way)
Step 3의 digest bullet 문면을 교체하고 spec 한정·기록물 금독 bullet을 추가한다. codex는 적응 delta(TOML·"일괄 read" 어휘) 보존 3-way.

**Contracts**: Step 3 읽기 규칙이 Part 1의 3개 invariant를 소유한다(다른 절·Hard Rule에 복제하지 않음 — 판정 주체 1곳). 기존 최소 읽기 규칙·"근거 부족하면 finding 안 만든다"·Input의 digest optional·미제공 하위 호환은 불변.

**Acceptance Criteria**:
- [ ] AC1 (1등급): 구 문면 `원본 파일 residual read로 확정` 이 2벌에서 0건. 평가: `grep -c '원본 파일 residual read로 확정' .claude/agents/plan-review-agent.md .codex/agents/plan-review-agent.toml` 각 0.
- [ ] AC2 (1등급): anchor `동급 evidence`·`리뷰 입력이 아니다`·`명시 인용한` 이 2벌 각 ≥ 1. 평가: grep 각 파일별 hit.
- [ ] AC3 (2등급): 새 문면이 Part 1 invariant 3개(digest 동급 evidence + residual read 2조건 한정, spec anchor 한정 + spec-review 소관 이관, 기록물 금독)를 모두 담고 기존 불변 계약과 모순 없다. 평가: reviewer 인용.

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- Step 3 읽기 규칙 교체·추가
- [M] `.codex/agents/plan-review-agent.toml` -- 3-way 동일 의미 반영

### Task 2: 문구 census 검증
**Acceptance Criteria**:
- [ ] AC1 (1등급): live 표면(`_sdd`·`.git` 제외)에서 `원본 파일 residual read로 확정` 잔존 0, `동급 evidence` hit가 정확히 Task 1의 2파일. 평가: `grep -rn` 출력 대조.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- spec 표면(main.md v4.16.0 불릿의 "residual read 확정" 서술)도 이번에 갱신할지: **spec-sync가 소유** — draft task로 두지 않음(spec 수정은 spec-sync 소관). 확인 불필요.
