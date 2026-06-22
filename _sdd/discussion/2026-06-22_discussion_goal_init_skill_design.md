# 토론 요약: goal-init 스킬 설계 (`/goal` 입력 생성기)

**날짜**: 2026-06-22
**라운드 수**: 8
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)

- **사용자 문제 제기**: Claude Code와 Codex의 `/goal` 기능을 잘 쓰려면 "좋은 goal 조건"이 결정적이다. 좋은 조건 = 목표 / 측정 가능한 AC / 증명 방법 / 제약 / 종료 경계. 여기에 더해 brainstorming처럼 목표를 향한 다양한 아이디어를 발산·실험·검증하고, 그 과정을 logging·문서화하는 것까지 잘 되어야 한다. 이 모든 걸 돕는 "사용자 입력(goal 조건)을 생성하는 스킬"을 만들고 싶다.
- **토론을 시작한 배경**: 토론에 앞서 `/goal` 기능 문서 3종(Claude Code goal 페이지, Codex cookbook, Codex follow-goals)을 읽고 두 런타임의 기능을 비교했다. SDD skills repo에 goal 조건 생성 스킬을 신설하려는 의도.
- **현재 상태**:
  - `ralph-loop-init`이 가장 가까운 선례 — 장기 실행 루프용 `ralph/` 디렉토리를 부트스트랩하고 `state.md`/`decisions.md`(append-only)/`results/`/`final_report.md`까지 logging·검증 인프라를 셋업. 단 ralph는 **외부 bash `while-true` 루프**(컨테이너 격리, exit code 머신 판정)이고 `/goal`은 **Claude Code/Codex 네이티브 기능**(매 턴 끝에 평가자 모델이 조건 충족 판정) — 실행 모델이 근본적으로 다름.
  - `discussion`(발산·수렴→요약), `feature-draft`(요구→draft) 등 입력 생성 스킬 존재.
  - 스킬 규약: frontmatter→AC→Hard Rules→Key Principles→Process(Step+Gate)→Error Handling, agent 2-layer, `marketplace.json` skills/agents 배열 + Codex 미러 등록, 출력은 `_sdd/<type>/<YYYY-MM-DD>_<type>_<slug>.md`.
- **범위와 제외 범위**:
  - 범위(v1): 대화형 goal-helper. 조건 생성 + 실행 하네스(4파일) 셋업 + 런타임별 실행법.
  - 제외(deferred): ralph-loop 대체 — 장기 과제로 분리.
- **수집한 근거**: `/goal` 문서 3종(WebFetch), `ralph-loop-init` 스킬/agent 구조 분석(Explore), repo 스킬 제작 규약·`_sdd/` 출력 경로·`marketplace.json` 등록 절차(Explore).

### `/goal` 핵심 메커니즘 (토론 전제)
- 명령은 양쪽 동일: `/goal <조건>`. 조건 충족 시까지 매 턴 자동 반복, 충족 시 자동 해제.
- **Claude Code**: prompt 기반 Stop hook 래퍼. 매 턴 끝에 small fast model(기본 Haiku)이 yes/no 판정. **평가자는 도구를 못 쓰고 "대화에 드러난 것"만 본다.** 조건 최대 4,000자. 라이프사이클 = set/status/`clear`(pause/resume 없음). v2.1.139+, workspace trust + hooks 활성 필요.
- **Codex**: thread-scoped state, 안전 경계(turn 종료/idle/no queued input)서 continuation 체크. evidence-based completion 강조(6요소: Outcome/Verification surface/Constraints/Boundaries/Iteration policy/Blocked conditions). 라이프사이클 = set/status/clear + **pause/resume**. `features.goals` 활성화 필요(`codex features enable goals`).

## 핵심 논점 (Key Discussion Points)

1. **산출물 범위**: 조건 텍스트만? vs 실행 하네스 셋업까지? → "조건 + 실행 하네스 셋업"으로 확정.
2. **해결할 페인**: 조건 작성 난이도 / 아이디어 휘발 / 검증을 대화에 남기기 / 종료 후 회고 — 4개 모두 대상.
3. **아키텍처(발산 시점)**: 셋업 발산(A) vs 루프 중 발산(B) vs 하이브리드(C) → C+B 결합.
4. **스코프(ralph 대체 야망)**: `/goal`은 턴 기반·대화형이라 ralph의 비대화형 장시간 머신검증 작업을 그대로 대체하기 어렵다 → v1은 goal-helper로 한정, ralph 대체는 deferred.
5. **발산 메커니즘**: `experiments.md` 공용 큐 + 조건 내장 자동발산 규칙 + 사용자 수동 추가.
6. **하네스 파일 구조**: 4파일(goal.md/experiments.md/journal.md/report.md), 검증은 매 턴 대화 출력 + journal append.
7. **런타임 차이 흡수**: Claude/Codex 스킬을 각각 작성, 조건 본문은 공통(런타임 독립), 실행법은 각 스킬에 자기 런타임 것만.
8. **Process 흐름**: Intake → Divergence → Condition Crafting → Harness Setup → Handoff(사용자가 직접 `/goal`).

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| D1 | 아키텍처 = **C+B 하이브리드**: 셋업 때 사용자와 1차 발산, 루프 진행 중 자동/사용자 입력으로 추가 발산·실험·검증 | 4개 페인이 셋업/루프 서로 다른 시점의 문제라 한쪽만으론 다 못 푼다 (`사용자 판단`) | 3 |
| D2 | v1 스코프 = **대화형 goal-helper 한정**. ralph-loop 대체는 분리 | `/goal`은 턴 기반·평가자가 도구 못 씀 → 비대화형 장시간 머신검증은 ralph가 적합. 스코프 명확화 (`사용자 판단` + `외부 자료`) | 4 |
| D3 | 발산 메커니즘 = **`experiments.md` 공용 큐(pending/done)** + 조건 내장 "큐 소비·막히면 자동 brainstorm·append" 규칙 + 사용자 수동 추가 | `/goal` 무인 루프를 깨지 않으면서 자동+수동 발산 양립 (`사용자 판단`) | 5 |
| D4 | 하네스 = **4파일**(`goal.md`/`experiments.md`/`journal.md`/`report.md`). 검증 결과는 매 턴 대화 출력 + `journal.md` append (별도 verification 파일 없음) | 평가자가 대화+journal로 읽을 수 있어 별도 파일 불필요, YAGNI (`사용자 판단`) | 6 |
| D5 | 스킬 형태 = **discussion식 대화형 단일 스킬**(신규 agent 없음). 셋업 발산을 대화로 진행 후 4파일+조건 산출 | 셋업이 사용자 상호작용 중심이라 agent 위임보다 단일 대화형이 적합 (`사용자 판단` + `코드 확인`: discussion 패턴) | 1, 8 |
| D6 | 스킬 이름 = **`goal-init`** | ralph-loop-init과 대구되는 init 네이밍 (`사용자 판단`) | — |
| D7 | **Claude용(`.claude/skills/goal-init`)과 Codex용(`.codex/skills/goal-init`) 스킬을 각각 작성.** 조건 본문은 런타임 독립(4,000자 이하·evidence 대화 surface·pause/resume 비의존), 실행법(활성화·명령)은 각 스킬에 자기 런타임 것만. 미러는 스킬 구조까지만, 실행법 내용은 분리 허용 | 두 런타임 스킬이 어차피 따로 존재하므로 실행법까지 미러로 강제할 필요 없음 (`사용자 판단`) | 7 |
| D8 | Step 5 Handoff = **사용자가 조건 검토 후 직접 `/goal` 발동.** 스킬은 발동하지 않음 | 잘못된 조건으로 무인 루프가 도는 토큰 낭비 방지, 조건 최종 검토 보장 (`사용자 판단`) | 8 |
| D9 | Process = **5단계**: ①Goal Intake(목표 수집+`/goal` 적합성 게이트) ②Divergence(접근 2-3개 능동 발산→experiments 백로그) ③Condition Crafting(5요소 응축+평가자 적합성 self-check) ④Harness Setup(4파일 생성+조건에 큐소비·자동발산·검증출력·append 규칙 내장) ⑤Handoff(조건+실행법 제시) | discussion 대화 루프 + ralph 부트스트랩 + feature-draft 단계 구성 차용 (`사용자 판단` + `코드 확인`) | 8 |
| D10 | `goal.md` 조건 슬롯 = **분업형**. 완료조건(`DONE WHEN`/`CONSTRAINTS`/`STOP`)은 조건 문자열에 레이블로 자족 인라인 → 평가자가 도구 없이 transcript만으로 판정. 루프 행동(HOW)은 `goal.md`의 `Loop Protocol` 섹션 참조 → 메인 에이전트가 읽음. 세부: 증명 방법은 `DONE WHEN`에 인라인("`<cmd>` shows … in transcript", 별도 VERIFY 슬롯 없음), `STOP`은 턴 기준 기본 | 평가자(Haiku)는 도구 못 쓰고 "대화에 드러난 것"만 보므로 완료조건은 자족해야 하고, HOW까지 인라인하면 조건이 비대해지고 평가자가 매 턴 노이즈를 읽음 (`사용자 판단` + `외부 자료`: /goal 평가 메커니즘) | Q2(조건 슬롯 부분) |

> 근거 유형: `코드 확인` / `외부 자료` / `사용자 판단` / `미검증 가정`.

### 기각한 대안
- **A안 (셋업 대화 집중형)**: 조건 품질은 최고지만 루프 중 실험 logging이 약해 "아이디어 휘발" 페인이 덜 풀림.
- **단독 B안 (부트스트랩 최소형)**: 루프 중 logging은 강하나 조건 작성 지원이 약해 "조건 작성 난이도" 페인이 덜 풀림.
- **v1에 ralph 대체 결합**: `/goal`이 턴 기반이라 컨테이너 장시간 비대화형 작업 대체가 메커니즘상 어렵고 v1 스코프가 비대해짐.
- **런타임 감지 분기(b안) / 최소공통분모 단일(a안)**: D7(스킬을 각각 작성)로 대체됨 — 분기 로직/이식성 트레이드오프 불필요.
- **5파일(verification 분리) / 3파일 미니멀**: 각각 과설계 / 큐·로그 섞임. 4파일이 YAGNI 최적.
- **Step 5 스킬 직접 발동 / 선택형**: 조건 검토 단계를 생략해 잘못된 무인 루프 위험.
- **조건 슬롯 풀 인라인 레이블형 / 미니멀 자연어형**(D10 관련): 풀 인라인은 EACH TURN(HOW)까지 조건에 넣어 비대 + 평가자가 매 턴 노이즈를 읽음. 미니멀 자연어는 슬롯 채우기·자체검증이 덜 기계적이고 복잡한 목표에 빈약. → 분업형 채택.

## 미결 질문 (Open Questions)

| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| Q1 | ralph-loop를 `/goal` 기반으로 대체할 수 있는가 / 해야 하는가 | deferred-deliberately | 장기 과제. `/goal` 턴 기반 한계 vs ralph bash 무한루프의 메커니즘 격차 검토 필요 |
| Q2 | `experiments`·`journal`·`report` 4파일 각각의 구체 포맷·필드 (※ `goal.md` 조건 슬롯 구조는 D10으로 해소) | deferred-deliberately | 선례(ralph decisions.md/final_report.md, discussion 요약) 기반으로 구현 단계에서 초안 후 review-fix로 확정 |

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | `feature-draft`로 goal-init 스킬 설계를 draft화 (이 요약을 입력으로) | High | 사용자/후속 스킬 |
| 2 | `.claude/skills/goal-init/`(SKILL.md+skill.json+references/examples) 작성 — Process 5단계, 4파일 하네스, Claude 실행법 | High | 구현 |
| 3 | `.codex/skills/goal-init/` 작성 — 동일 구조, Codex 실행법(features.goals 활성화·pause/resume) | High | 구현 |
| 4 | `marketplace.json` `plugins[0].skills` 배열에 goal-init 경로 등록 (신규 agent 없으므로 agents 배열 불변) | Medium | 구현 |
| 5 | README/docs 워크플로우에 goal-init 통합(discussion→goal-init 연계 안내 포함) | Low | 구현 |

### 후속 핸드오프 (Handoff)
- **목표**: 대화형 단일 스킬 `goal-init`을 Claude/Codex 양쪽에 구현. 한 번 돌리면 사용자가 검토 후 바로 `/goal`에 걸 수 있는 조건 문자열 + `_sdd/goal/<date>_<slug>/`의 4파일 하네스가 산출된다.
- **변경 금지 제약**: 기존 스킬 구조 규약(frontmatter/AC/Hard Rules/Key Principles/Process/Error Handling) 준수. `ralph-loop-init`을 건드리지 않음(v1은 독립). 스킬은 `/goal`을 직접 발동하지 않음(D8).
- **검증**: Claude Code에서 실제 `/goal-init`(또는 트리거 문구) 호출 → 4파일이 규약 경로에 생성되고 조건 문자열이 평가자 적합성(도구 없이 대화로 판정 가능·evidence 매 턴 surface·4,000자 이하)을 만족하는지 확인. Codex 미러도 동등 확인.
- **중단 조건**: 구현 중 본 토론 결정(특히 D2 스코프 한정, D8 비발동)과 모순되는 설계 강제가 발견되면 멈추고 보고.

## 리서치 결과 요약 (Research Findings)

- **`/goal` 문서 3종**: Claude Code(Stop hook 래퍼, 평가자 도구 미사용, 4,000자, clear만), Codex(features.goals 활성화, pause/resume, evidence-based 6요소). 공통: `/goal <조건>`, evidence가 대화/아티팩트에 surface돼야 평가.
- **ralph-loop-init**: 5파일(config.sh/PROMPT.md/run.sh/state.md/CHECKS.md) + `results/` 생성. while-true 루프(LLM→action.sh→결과→반복), phase 상태머신(SETUP→…→DONE), append-only decisions.md, conclusion-first final_report.md, 3회 실패 escalation. **컨테이너 격리 전용·bash 무한루프** — `/goal`의 네이티브 턴 루프와 실행 모델이 다름.
- **스킬 규약**: 신규 스킬은 `.claude/skills/<name>/` + `.codex/skills/<name>/`, `marketplace.json` 배열 등록, 산출물은 dated-slug 경로. agent 2-layer(orchestrator+leaf), 대화형 스킬(discussion)은 agent 위임 없이 단일 루프로 동작.

## 토론 흐름 (Discussion Flow)

```
R1 산출물 범위        → "조건 + 실행 하네스 셋업"
R2 핵심 페인          → 4개 전부 (조건 작성/휘발/검증 surface/회고)
R3 하네스 무게        → 구조화된 중량급 (일반 세션, ralph식 격리 아님)
R4 아키텍처(발산 시점) → C+B 하이브리드 (+ ralph 대체 장기 고려 새 정보)
R5 v1 스코프          → goal-helper 한정 (ralph 대체 deferred)  [비판적 개입]
R6 발산 메커니즘      → experiments.md 공용 큐 + 자동/수동
R7 파일 구조          → 4파일 (검증은 대화 출력+journal)
R8 이름/형태          → goal-init, 대화형 단일 스킬, Claude+Codex 미러
R9 런타임 흡수        → 스킬 각각 작성, 조건 공통·실행법 분리
R10 Process/Handoff   → 5단계, 사용자가 검토 후 직접 /goal
```

## 부록: 대화 로그 (Conversation Log)

### Round 1 — 산출물 범위
**Q**: 스킬의 deliverable은? **A**: 조건 + 실행 하네스 셋업.

### Round 2 — 핵심 페인
**Q**: `/goal`을 쓸 때 가장 큰 페인은? (복수) **A**: 조건 작성 어렵다 / 아이디어 휘발 / 검증 대화에 남기기 어렵다 / 종료 후 회고 안 됨 — 4개 전부.

### Round 3 — 하네스 무게
**Q**: 하네스가 도는 맥락/무게? **A**: 구조화된 중량급(일반 세션, 컨테이너 격리 아님).

### Round 4 — 아키텍처
**Q**: brainstorm이 언제 일어나나 (A/B/C)? **A**: C+B 결합 — 초기 발산은 사용자와, 루프 중 자동/사용자 입력으로 추가 발산·실험·검증. ralph 겹쳐도 무방, 장기적으로 ralph 대체도 고려.

### Round 5 — v1 스코프 (비판적 개입)
**Q**(비판): ralph 대체 야망 vs `/goal` 턴 기반 한계 — v1 스코프는? **A**: goal-helper로 한정.

### Round 6 — 발산 메커니즘
**Q**: experiments.md 공용 큐 + 조건 내장 규칙으로? **A**: 공용 큐 + 자동/수동 둘 다.

### Round 7 — 파일 구조
**Q**: 파일 세분화 수준 (3/4/5)? **A**: 4파일.

### Round 8 — 이름/형태
**Q**: 스킬 이름? (형태=대화형 단일, Claude+Codex 미러) **A**: goal-init.

### Round 9 — 런타임 흡수
**Q**: Claude vs Codex 차이 흡수 방식? **A**: 두 스킬을 각각 만들고 실행법은 각자 기재, 실행법 미러는 불필요.

### Round 10 — Process / Handoff
**Q**: Step 5에서 `/goal`을 누가 거나? **A**: 사용자가 검토 후 직접.
