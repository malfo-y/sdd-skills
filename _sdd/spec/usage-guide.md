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
- `_sdd/spec/main.md` 생성 또는 갱신 — current canonical global spec core(배경, Scope / Non-goals / Guardrails, 핵심 설계와 주요 결정)를 갖춘 thin global spec 생성
- 필요할 때만 supporting file 또는 appendix 분리 — 기본값은 single-file이며, multi-file은 structure rationale이 있을 때만 연다
- 코드베이스가 있으면 optional `Strategic Code Map` 생성 — 짧으면 `main.md` appendix, 길거나 설명이 필요하면 `components.md` 또는 `code-map.md` 같은 supporting surface에 둔다
- `_sdd/env.md` 생성 — 환경 설정/실행 방법 가이드. 상단에 비밀값 금지 경고 헤더 포함(커밋되는 파일이므로 API 키·토큰·비밀번호 금지)
- `.gitignore` 생성 또는 멱등 병합 — `SDD-WORKSPACE` 마커 블록으로 process artifact(`_sdd/{discussion,implementation,pipeline,pr}/`)를 ignore한다. 커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`·`drafts/`·`work_log/`이다(`drafts/`·`work_log/`는 구현 로그 자산).
  - 병합: 부재면 생성 / 마커 없으면 파일 끝에 append(기존 규칙 보존) / 마커 블록 존재면 그 블록만 교체(멱등)
- `AGENTS.md` 생성 또는 멱등 병합 — harness 템플릿(§0~§5: 작업 원칙 / 읽는 순서 / 작업 규약·검증 표준 / SDD 워크플로우 순서 / 판단 기준 / 작업 기록(work log)) 기반으로 작업 진입·작업 규약 레이어를 생성한다. §5 work log는 `_sdd/work_log/<yyyy-mm-dd>.md`에 작업 단위를 append하는 on-demand 포렌식 규약이며 §1 읽기 순서에는 포함되지 않는다. 기존 파일이 있으면 `SDD-HARNESS` 마커 블록만 멱등 교체하고 마커 밖 내용은 보존한다
- `CLAUDE.md` 생성 또는 업데이트 — `→ AGENTS.md 참조` 포인터로 harness를 단일 소스로 가리킨다
- 사용자에게 요약 테이블 제시 후 전체 스펙 출력

### Scenario 2: 기능 추가 (수동 SDD Workflow — lite 체인)

**Action:**
```bash
/feature-draft-lite      # planning entry — task + Target Files(실측) + AC 중심 lite draft
/spec-sync               # (구현 전) 분할 draft planned todo 고정 또는 planned persistent truth가 실제로 필요할 때만
/plan-review             # optional: 구현 전 계획 품질/과잉 설계 점검 (단일 패스 경량 반환)
/implementation-lite     # 메인 루프 직접 RED→GREEN test-first 구현
/implementation-review   # 계획 대비 fresh verification
/spec-sync               # (구현 후) 코드 변경사항을 스펙에 동기화
```

**Expected Result:**
- `_sdd/drafts/<YYYY-MM-DD>_feature_draft_<slug>.md` — 스펙 패치 초안(Part 1 마커) + 구현 태스크 리스트(Part 2)
- `_sdd/spec/<project>.md` 업데이트 — planned persistent truth 반영(조건부)
- optional 구현 전 계획 리뷰(`plan-review`)는 리포트 파일 없이 경량 반환으로 finding을 응답 — Critical/High finding이 있으면 구현 전 blocker로 취급하고 fix는 메인 루프가 1회 수행
- 구현은 메인 루프가 직접 작성하고 AC→증거 테이블로 마감(별도 plan artifact 없음). 단일 컨텍스트 초과면 분할 규칙(롤링 draft + planned todo 고정 + feature별 순차 체인)으로 해소한다
- 구현 완료 후 구현 리뷰와 spec sync까지 연결돼 스펙과 코드 간 드리프트가 설명 가능한 상태

### Scenario 2b: 대규모 기능 추가 (sdd-autopilot 자동 실행)

> autopilot(v3.0.0)은 lite 체인 전용이다. 규모 초과는 lite feature 분할(분할 목록 `spec-sync` planned todo 고정 후 feature별 순차 lite 체인)로 해소한다. 구 orchestrator 기반 full 파이프라인은 제거됐다 — 복구는 git tag `full-lane-final`, legacy `_sdd/pipeline/` 산출물은 기록물이다.

**Action:**
```bash
/sdd-autopilot "인증 시스템 구현 — JWT 기반, 로그인/로그아웃/토큰 갱신"
```

**Expected Result:**
- Step 0~1: 기존 `_sdd/drafts/` 산출물 재활용·spec 유무를 확인하고 요청을 분석한다(부족한 정보만 인라인 질문, 승인 게이트 없음)
- Step L: `feature-draft-lite → plan-review(단일 패스 경량 반환) → fix 1회 → implementation-lite → implementation-review(경량 반환) → fix 1회 → (persistent 변경 시) spec-sync` 체인을 무승인으로 실행한다. 분할 신호가 뜨면 분할 규칙(롤링 draft + planned todo 고정 + feature별 순차 체인)으로 처리한다
- `_sdd/drafts/<YYYY-MM-DD>_feature_draft_<slug>.md` — 실행 청사진이 되는 lite draft
- report 파일 없이 최종 응답 요약 — 수행 단계, finding/fix 내역, 테스트 결과, spec sync 여부, 잔존 항목
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
/spec-summary            # 현재 repo/spec를 설명하는 reader-facing whitepaper
/discussion              # 기술 선택, 아키텍처 결정 등 구조화된 토론
```

**Expected Result:**
- `_sdd/spec/summary.md` — Executive Summary, Background / Motivation, Core Design, Code Grounding, Usage / Expected Results, Further Reading / References, 그리고 필요한 경우 appendix 형태의 Planned / Progress Snapshot
- `_sdd/discussion/<YYYY-MM-DD>_discussion_<slug>.md` — 토론 결과와 결정사항/미결/실행항목 정리 (최대 10라운드)
