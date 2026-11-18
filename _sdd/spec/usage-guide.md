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

### Scenario 2: 기능 추가 (SDD 체인 — sdd-orchestrator)

**Action:**
```bash
# Claude Code (Codex는 같은 요청을 $sdd-orchestrator로 시작)
/sdd-skills:sdd-orchestrator CSV 내보내기 기능을 계획부터 spec 반영까지 진행해줘
/sdd-skills:sdd-orchestrator _sdd/drafts/<계획 파일>.md를 구현 단계부터 진행해줘   # 계획 파일로 진입
/sdd-skills:sdd-orchestrator spec-sync 단계만 실행해줘                          # 단계·종점 지정
/sdd-skills:spec-sync                                                           # 예전 단계 스킬 이름(호환 별칭) — spec-sync만 실행
```

> 메인 세션이 계획 → 계획 리뷰 → 실패하는 검사 먼저 구현 → 구현 리뷰 → spec 반영을 직접 수행하고, 단계 작업을 다른 agent에 넘기지 않는다. 두 리뷰는 같은 세션이 한 번씩 하고 찾은 것을 그 자리에서 고치므로 사용자가 따로 호출하지 않는다. 리뷰 단계만 지정하면 찾은 것만 보고하고 고치지 않는다. 독립 리뷰가 필요하면 PR 시점에 `pr-review`를 쓴다.

**Expected Result:**
- `_sdd/drafts/<YYYY-MM-DD>_feature_draft_<slug>.md` — 계획 파일 하나. `spec-update-todo-input` 마커 쌍으로 감싼 `Spec Delta`(spec 반영의 입력), `계획`(바꿀 자리·끝나는 조건과 판정 방법·계획이 기대는 외부 사실), `진행`(조건별 판정과 증거 — 재개 지점)을 가진다. 별도 인계 파일은 만들지 않는다
- 계획 리뷰: 코드를 고치기 전에 계획이 기대는 외부 사실을 실제와 대조하고, 빠진 수정 지점과 통과해도 결함이 남는 조건을 찾아 계획 파일에 반영한다. 답에 따라 구조·범위·바꿀 자리가 달라지는 결정만 사용자에게 묻고, 무인 위임이면 합당한 안으로 진행해 마감 보고에 적는다
- 구현: 끝나는 조건마다 실패하는 검사를 먼저 만들어 실패를 확인한 뒤 가장 작은 변경으로 통과시킨다. 검사의 종류와 강도는 모델이 위험에 맞게 정한다
- 구현 리뷰: 검사가 통과하면 전체 diff를 다시 읽어 요구사항 미구현, 검사가 통과해도 틀리게 동작할 수 있는 곳, 실행해 보지 못한 조건, 요청에 없는 코드와 중복을 찾아 고치고 관련 검사만 다시 돌린다
- 마감: 계획 파일 `진행`에 조건별 판정과 증거가 남고, 채팅에는 수행한 단계·조건별 결과·두 리뷰에서 찾아 고친 것·실행으로 확인하지 못한 것·사용자 결정 지점·남은 분할 기능이 보고된다. 계획이 기능을 나누면 첫 기능까지만 진행한다
- spec 반영 단계: 검증된 지속 정보만 `_sdd/spec/`에 반영되고, 저장소 작업에 반복 적용되는 환경 사실은 `_sdd/env.md`로 올라간다. 모든 조건이 닫히고 남은 분할 기능이 없는 계획 파일은 `_processed_` prefix로 rename된다. 규모가 커지면 기능 단위 분할(남은 기능은 `🚧 Planned` 항목으로 고정 + 기능별 순차 실행)로 해소한다

### Scenario 2b: 여러 SDD 단위를 native goal로 수렴시키기 (sdd-autopilot setup)

> `sdd-autopilot`은 구현을 즉시 시작하는 runner가 아니라 `goal-init(preset=sdd)` 기반 setup entrypoint다. 실제 반복 실행은 사용자가 native goal을 활성화한 뒤 시작된다.

**Action:**
```bash
/sdd-autopilot "인증 시스템 구현 — JWT 기반, 로그인/로그아웃/토큰 갱신"
```

**Expected Result:**
- `sdd-autopilot`이 사용자 목표와 관련 context를 `goal-init(preset=sdd)`에 전달하고, 목표·권한·접근의 판단 기준과 condition self-check에 따라 `_sdd/goal/<YYYY-MM-DD>_<slug>/` 아래 `goal.md`·`experiments.md`·`journal.md`·`report.md`를 생성한다
- handoff에는 자족적 조건 문자열, runtime 실행법, 네 파일의 개별 경로와 “goal을 활성화하지 않았으며 기존 goal 상태도 변경하지 않았다”는 불변식이 표시된다. 사용자가 내용을 검토하고 native goal activation 여부와 시점을 결정한다
- setup 중 `sdd-orchestrator`나 initial feature는 실행되지 않는다. current goal status를 조회하지 않고 existing goal을 변경하거나 active goal 때문에 setup을 차단하지도 않는다
- activation 뒤 SDD Loop Protocol은 미충족 `DONE WHEN` 또는 실패한 final integration proof gap에서 가장 작은 next feature를 선택하고, 그 feature를 `sdd-orchestrator`로 진행(reviewed draft가 없으면 계획 단계부터, 있으면 구현 단계부터 구현 리뷰까지, persistent 변경 시 spec-sync 단계까지)한 뒤 evidence·완료 feature·남은 gap·next action 기록을 반복한다
- draft가 분할되면 같은 native goal 안에서 smallest next unit을 계속 선택하며 nested `goal-init`을 만들지 않는다. 모든 `DONE WHEN`과 final integration proof 통과는 성공 종료 조건이다. STOP/STUCK은 미완료 사유·다음 행동을 남기고 native lifecycle 규칙에 따라 종료한다
- 계획 리뷰와 구현 리뷰는 `sdd-orchestrator`가 순서 안에서 직접 수행한다. 별도 Goal Contract, Initial Feature Queue, status manifest, goal-level reviewer는 생성하지 않는다

### Scenario 3: PR 기반 스펙 동기화

**Action:**
```bash
/pr-review               # PR 코드 품질 검증 + spec 존재 시 spec 기반 추가 검증 → APPROVE / REQUEST CHANGES
```

**Expected Result:**
- `_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md` — findings-first 코드 품질 검증 + spec 존재 시 spec 준수 여부 판정 + 구체적 피드백

### Scenario 3b: 스펙 점검 및 의사결정

**Action:**
```bash
/spec-upgrade 스펙 리뷰  # spec 품질과 코드와의 어긋남을 점검만 한다(수정 없음)
/discussion              # 기술 선택, 아키텍처 결정 등 구조화된 토론
```

**Expected Result:**
- 채팅 보고 — 판단 기준 4개 위반과 코드와의 어긋남을 심각도 순(`Critical`·`Quality`·`Improvements`)으로, 발견마다 `file:line` 근거와 함께 보고하고 결론(spec 수정 필요 / 수정 불필요 / 논의 필요)을 하나 적는다. 파일을 요청하면 `_sdd/spec/logs/spec_review_report.md`에 쓴다. 고치려면 `/spec-upgrade`를 정리·형식 이행 요청으로 다시 부른다
- `_sdd/discussion/<YYYY-MM-DD>_discussion_<slug>.md` — 토론 배경·결정과 근거·미결·다음 행동을 정리한다. 질문 순서와 라운드 수는 고정하지 않으며, 외부 데이터 대기는 미결로 기록한 뒤 사용자의 선택에 따라 종료할 수 있다. 상세 라운드 로그는 요청 또는 감사 요구가 있을 때만 포함한다.
