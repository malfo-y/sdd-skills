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
- `AGENTS.md` 생성 또는 멱등 병합 — harness 템플릿(§0~§5: 작업 원칙 / 읽는 순서 / 작업 규약·검증 표준 / SDD 워크플로우 순서 / 판단 기준 / 작업 기록(work log)) 기반으로 작업 진입·작업 규약 레이어를 생성한다. §5 work log는 `_sdd/work_log/<yyyy-mm-dd>.md`에 작업 단위를 append하는 on-demand 포렌식 규약이며(아래 커밋 게이트 훅으로 강제된다) §1 읽기 순서에는 포함되지 않는다. 기존 파일이 있으면 `SDD-HARNESS` 마커 블록만 멱등 교체하고 마커 밖 내용은 보존한다
- `CLAUDE.md` 생성 또는 업데이트 — `→ AGENTS.md 참조` 포인터로 harness를 단일 소스로 가리킨다
- `.claude/hooks/worklog-gate.sh`·`worklog-context.sh`·`harness-context.sh`·`agent-watchdog.sh` 공용 script 설치 + `.claude/settings.json`·`.codex/hooks.json` dual-setting 등록 — 하네스 규약을 강제하거나(§5 work log 커밋 게이트) 사라진 규약을 되돌려 놓거나(컨텍스트 소실 후 하네스 재주입) 장기 실행 subagent에 자기점검 nudge를 전달하는(advisory) 실행 자산이다. 호출 runtime과 무관하게 항상 함께 설치되며(별도 opt-in 아님), 스크립트는 스킬 `references/hooks/` 정본의 verbatim 사본이고 두 설정은 각각 키 수준 멱등 병합해 사용자의 non-SDD hook과 다른 top-level key를 보존한다. 한 설정이 깨졌으면 그 파일만 그대로 skip하고 반대 runtime과 script 설치는 계속한다
  - 관찰 결과: 오늘 work log에 미커밋 변경이 없으면 양 runtime의 **세션 첫 `git commit`이 거부**되고(이후 분할 커밋은 통과), `SDD_SKIP_WORKLOG=1 git commit ...`으로 우회한다. 세션 시작 시 오늘 로그 상태가 context로 주입되고, `clear|compact` 뒤에는 `AGENTS.md`가 다시 주입되며, 장기 실행 subagent watchdog은 원래 tool result를 보존한 advisory context를 보낸다
  - 스킬 최종 보고는 커밋되는 두 runtime 설정의 설치 사실과 Codex hook 지원·project trust 조건을 announce한다. Codex에서는 `/hooks`의 exact definition을 사용자가 검토·신뢰해야 하며, 스킬은 trust나 user-global config를 자동 변경하지 않는다
- 사용자에게 요약 테이블 제시 후 전체 스펙 출력

### Scenario 2: 기능 추가 (수동 SDD Workflow — SDD 체인)

**Action:**
```bash
/feature-draft           # planning entry — task + Target Files(실측) + AC 중심 draft (gate+fix 기본 1회, 임계값 시 최대 2회)
/spec-sync               # (구현 전) 분할 draft planned todo 고정 또는 planned persistent truth가 실제로 필요할 때만
/implementation          # 메인 루프 직접 RED→GREEN test-first 구현 (gate+fix 기본 1회, 임계값 시 최대 2회)
/spec-sync               # (구현 후) 코드 변경사항을 스펙에 동기화
```

> 두 품질 게이트(`plan-review`·`implementation-review`)와 fix는 producer 스킬이 소유하므로 위 흐름에서 사용자가 따로 호출하거나 fix하지 않는다. 각 reviewer 호출은 단일 패스이며, producer는 gate 1+fix 1을 항상 수행하고 fix 전 raw finding이 `Critical+High ≥ 3` 또는 `Medium ≥ 5`일 때만 gate 2+fix 2까지 수행한다(Low 제외, implementation shard 합산 dedup 없음). gate 3은 없다. draft 없이 기존 계획만 점검하는 경우에만 `/plan-review`를 직접 호출한다.

**Expected Result:**
- `_sdd/drafts/<YYYY-MM-DD>_feature_draft_<slug>.md` — 스펙 패치 초안(Part 1 마커) + 구현 태스크 리스트(Part 2)
- `_sdd/spec/<project>.md` 업데이트 — planned persistent truth 반영(조건부)
- 구현 전 계획 리뷰(`plan-review`)는 `feature-draft`가 gate 1로 항상 수행하고(한 호출 = agent 1회 dispatch의 경량 반환), fix 전 raw finding이 임계값이면 gate 2를 한 번 더 수행한다. 각 반환은 리포트 파일 없는 경량 finding이며 fix와 평가조건 재확인은 draft 작성자가 맡는다
- 구현은 메인 루프가 직접 작성하고 회귀 → AC→증거 테이블 → `implementation-review` gate 1+fix 1 → 임계값 경로에서만 gate 2+fix 2 → 마감 요약으로 닫는다. 각 fix 뒤 커버리지 델타·회귀 재실행·증거 갱신을 수행한다(별도 plan artifact 없음 — 재개용 resume pointer로 `_sdd/implementation/<YYYY-MM-DD>_implementation_ledger_<slug>.md`만 생성·이어쓰며 AC→증거 테이블의 기록처다, 표는 채팅에도 노출). 규모가 커지면 분할 규칙(롤링 draft + planned todo 고정 + feature별 순차 체인)으로 해소한다
- gate 2 뒤에는 gate 3 없이 종료한다. gate 2의 fix 전 raw finding도 같은 임계값이면 수동 후속 review 1회를 권고하고, 마감 요약은 호출 1/2의 severity·fix·검증·잔존 finding을 구분한다. 이어서 spec sync까지 연결돼 스펙과 코드 간 드리프트가 설명 가능한 상태가 된다

### Scenario 2b: 여러 SDD 단위를 native goal로 수렴시키기 (sdd-autopilot setup)

> `sdd-autopilot`은 구현을 즉시 시작하는 runner가 아니라 `goal-init(preset=sdd)` 기반 setup entrypoint다. 실제 반복 실행은 사용자가 native goal을 활성화한 뒤 시작된다.

**Action:**
```bash
/sdd-autopilot "인증 시스템 구현 — JWT 기반, 로그인/로그아웃/토큰 갱신"
```

**Expected Result:**
- `sdd-autopilot`이 사용자 목표와 관련 context를 `goal-init(preset=sdd)`에 전달하고, 기존 5단계·condition self-check를 거쳐 `_sdd/goal/<YYYY-MM-DD>_<slug>/` 아래 `goal.md`·`experiments.md`·`journal.md`·`report.md`를 생성한다
- handoff에는 자족적 조건 문자열, runtime 실행법, 네 파일의 개별 경로와 “goal을 활성화하지 않았으며 기존 goal 상태도 변경하지 않았다”는 불변식이 표시된다. 사용자가 내용을 검토하고 native goal activation 여부와 시점을 결정한다
- setup 중 initial `feature-draft`·`implementation`·`spec-sync`는 실행되지 않는다. current goal status를 조회하지 않고 existing goal을 변경하거나 active goal 때문에 setup을 차단하지도 않는다
- activation 뒤 SDD Loop Protocol은 미충족 `DONE WHEN` 또는 실패한 final integration proof gap에서 가장 작은 next feature를 선택하고, 필요 시 reviewed `feature-draft`를 만든 뒤 `implementation` → persistent 변경 시 `spec-sync` → evidence·완료 feature·남은 gap·next action 기록을 반복한다
- draft가 분할되면 같은 native goal 안에서 smallest next unit을 계속 선택하며 nested `goal-init`을 만들지 않는다. 모든 `DONE WHEN`과 final integration proof가 통과해야 종료한다
- `feature-draft`와 `implementation`의 품질 게이트는 각 producer가 소유한다. 별도 Goal Contract, Initial Feature Queue, status manifest, goal-level reviewer는 생성하지 않는다

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
