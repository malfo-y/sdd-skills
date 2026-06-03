# 토론 요약: investigate를 orchestrator(skill)+Explore fan-out으로 재설계

**날짜**: 2026-06-03
**라운드 수**: 4 (방향 고정 → 비판/설계 집중)
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)

- **사용자 문제 제기**: "investigate는 왜 agent에 들어가 있는지 모르겠다. skill로 빼고, 파일들을 살필 때 sub-agent를 fan-out하는 게 훨씬 효율적이지 않나?"
- **토론을 시작한 배경**: 직전에 mirror 스킬 9종을 agent thin wrapper로 전환(머지 완료, spec v4.1.11)하면서 investigate도 wrapper→single-agent로 분류했다. 그런데 investigate는 fan-out이 유익한 스킬인데 census가 "현재 agent 본문이 sub-agent를 안 깐다"만 보고 non-fan-out으로 오분류했고, wrapper화 + Agent 도구 제거로 병렬 잠재력을 오히려 죽였다. 통합 규칙("fan-out→orchestrator+leaf / non-fan-out→wrapper")에 비춰 investigate를 orchestrator로 바로잡는 토론.
- **현재 상태 (코드 확인)**:
  - investigate = thin wrapper(Mode B) → `investigate-agent` 단일 dispatch. agent(86줄)는 Write/Edit/Bash 보유(코드 수정), 현재 Agent 도구 미보유(dispatch되면 fan-out 불가).
  - `investigate-agent` 참조자 = 자기 파일 + skill wrapper + 매니페스트뿐. **autopilot·다른 스킬 dispatch 없음** → 제거 영향 격리(저위험).
  - 원래 investigate Step 3는 "Agent A(가설)/Agent B(독립 탐지) 병렬 교차검증"으로 fan-out 의도가 있었으나 agent 안에 갇혀 실행 불가였음.
  - **Explore agent = read-only**(Edit/Write/Agent 도구 제외) → 병렬 증거 탐색·가설 검증엔 적합하나 fix(write)는 불가.
- **범위와 제외 범위**: investigate 단일 스킬의 orchestrator 재설계 + investigate-agent 제거 + Explore 재사용. 다른 wrapped 스킬 재분류는 제외(review 3종은 사용자가 의도적 순차 결정, planner는 순차 degrade 수용 — investigate가 유일 오분류).
- **수집한 근거**: investigate skill/agent 본문, 매니페스트, autopilot orchestrator-contract(investigate 미참조), Explore agent 도구 범위.

## 핵심 논점 (Key Discussion Points)

1. **오분류 교정**: investigate는 탐색/가설 단계에서 fan-out이 유익 → 통합 규칙상 wrapper가 아니라 orchestrator여야 함. wrapper화가 병렬 잠재력을 죽였음.
2. **read/write 분리**: Explore는 read-only라 fix(write)를 못 함. 탐색만 병렬, 나머지는 인라인이라는 투 트랙이 자연스러운 칼선.
3. **lane 축**: 병렬 Explore를 가설 단위 vs 영역/증거 단위로 쪼갤 수 있음 — 둘 다 유효, 케이스별 선택.
4. **YAGNI/오버헤드**: 디버깅 대부분은 단순 단일파일 버그라 fan-out이 과함 → "넓고·모호할 때만 병렬" 트리거 필요.
5. **codex parity**: claude는 빌트인 Explore, codex는 동등 범용 explore agent가 없을 수 있음 → 런타임 역량 따라 degrade.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | **investigate = orchestrator(skill, 메인 루프)**, `investigate-agent` 제거 | fan-out은 메인 루프에서만 가능(nesting 1단계). 통합 규칙 정합 | 1 |
| 2 | **투 트랙**: 탐색(read-only 증거 수집·가설 검증)만 **Explore 병렬 fan-out**, 그 외 전 단계(문제정의·근본원인 종합·Blast Radius·fix·Fresh Verification)는 **orchestrator 인라인** | Explore는 read-only(write 불가), 단일 fix는 순차라 fan-out 불요 | 2 |
| 3 | **lane 축 = 가설-lane / 영역-lane 둘 다 예시 제시, orchestrator가 케이스별 선택** | 경쟁 가설이면 가설-lane(anti-anchoring, 옛 Agent A/B 부활), 출처 불분명·넓으면 영역-lane. 리지드 machinery 없이 유연(YAGNI) | 3 |
| 4 | **fan-out 트리거 = 기본 인라인 순차, 넓고·모호할 때만(경쟁 가설/출처 불분명/대규모) 병렬** | 단순 버그는 단순하게(현재 agent처럼). implementation "확신 없으면 순차" 철학과 정합 | 4 |
| 5 | **codex parity = claude 빌트인 Explore 병렬 / codex는 동등 read-only explore 있으면 spawn_agent 병렬, 없으면 순차 인라인 graceful degrade** | 정확성은 양쪽 동일, 병렬만 상실 가능. codex 역량은 feature-draft에서 실측 | 5 |
| 6 | **3-Strike·Scope Lock·Blast Radius Gate·Fresh Verification·근본원인 종합은 orchestrator 인라인 소유** | 순차 제어 로직, 단일 스레드 fix loop에 속함 | 2 |
| 7 | **문제정의는 대화 기반**(기존 Mode B 맥락 유지) | investigate 입력(증상·재현·기대 동작·시도 가설)은 대화 태생 | 2 |
| 8 | **spec 재분류**: investigate를 v4.1.11의 "non-fan-out=wrapper" 목록에서 빼고 orchestrator 계열로. 단 leaf=범용 Explore 재사용(custom leaf 아님)이라 implementation과 미세 차이 명시 | 검증된 현재 사실 반영 | 1 |

## 미결 질문 (Open Questions)

| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| 1 | codex 런타임에 claude `Explore` 동등의 범용 read-only explore agent가 존재하는가 | needs-data | feature-draft 단계 codex census로 확인. 결정은 이미 됨(있으면 병렬, 없으면 순차 degrade)이라 비차단 |

> in-scope 미결 0건(Q1은 결정된 degrade로 비차단, feature-draft에서 실측).

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | `/feature-draft`로 investigate orchestrator 재설계 상세 계획(Target Files 포함) 작성 | High | 후속 |
| 2 | investigate SKILL(claude+codex)을 orchestrator로 재작성: 문제정의(대화) → [넓고·모호시] Explore 병렬 fan-out(가설/영역 lane) → 근본원인 종합 → Blast Radius → fix·검증 인라인. 3-Strike·Scope Lock 보존 | High | 구현 |
| 3 | `investigate-agent` 제거 (claude `.md` + codex `.toml`) + 매니페스트 `agents` 목록에서 제외 | High | 구현 |
| 4 | codex 탐색 fan-out: 동등 explore agent 실측 → 있으면 spawn_agent 병렬, 없으면 순차 degrade 명시 | Medium | 구현 |
| 5 | spec(main.md/components.md/DECISION_LOG) investigate 재분류 갱신 — wrapper→orchestrator(Explore 재사용) | Medium | 후속 spec-update-done |

## 리서치 결과 요약 (Research Findings)

- `investigate-agent`는 autopilot·외부 스킬이 dispatch하지 않음 → 제거는 investigate skill + 매니페스트만 건드리는 격리된 변경(저위험).
- Explore agent는 read-only(Edit/Write 불가) → 탐색 lane으로만 적합, fix는 orchestrator 인라인 필수.
- 매니페스트(L51)에 `investigate-agent.md` 등록 → 제거 시 함께 정리.
- 원래 investigate에 fan-out 의도(Agent A/B 교차검증)가 있었으나 agent에 갇혀 사문화 → orchestrator로 올리면 부활.

## 토론 흐름 (Discussion Flow)

- Round 0 (방향 고정): 사용자가 "investigate→orchestrator, 범용 Explore 재사용, investigate-agent 제거"로 방향 명시 → Alternatives Initiation 생략, 비판/설계 집중.
- Round 1 (critical, fix 소유): Explore read-only 제약 제기 → **투 트랙**(탐색만 fan-out, 나머지 인라인) 채택.
- Round 2 (analysis, lane 축): 가설/영역 lane 2안 → **둘 다 예시, orchestrator 선택** 채택.
- Round 3 (critical, YAGNI): 단순 버그 오버헤드 도전 → **기본 인라인, 넓고·모호할 때만 병렬** 채택.
- Round 4 (critical, parity): codex Explore 등가 부재 가능성 → **런타임 역량 따라 degrade** 채택, codex 실측은 feature-draft로.

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: Explore는 read-only라 fix(write) 불가. fix+검증은 누가?
**Options**: orchestrator 직접 수정 / fix만 implementation-agent leaf / 투 트랙(탐색만 fan-out, 나머지 인라인)
**A**: 투 트랙.
**Follow-up**: 탐색=Explore 병렬, 그 외 전 단계=orchestrator 인라인으로 칼선 확정.

### Round 2
**Q**: 병렬 Explore lane을 어떤 축으로?
**Options**: 둘 다 제시 orchestrator 선택(권장) / 가설-lane / 영역-lane
**A**: 둘 다 제시, orchestrator 선택.
**Follow-up**: 가설-lane(anti-anchoring)·영역-lane(broad sweep)을 예시로, 리지드 machinery 없이.

### Round 3
**Q**: 언제 fan-out, 언제 인라인 순차?
**Options**: 기본 인라인·넓고 모호할 때만 병렬(권장) / 기본 병렬·사소할 때만 인라인 / 매번 자율
**A**: 기본 인라인, 넓고·모호할 때만 병렬.
**Follow-up**: 단순 버그는 현재 agent처럼 순차. implementation 보수적 철학과 정합.

### Round 4
**Q**: codex 탐색 fan-out(범용 Explore 등가 부재 가능)?
**Options**: claude=Explore·codex=역량 따라 degrade(권장) / 양쪽 전용 explore leaf 신규 / feature-draft로 이월
**A**: claude=Explore, codex=런타임 역량 따라.
**Follow-up**: 정확성 동일·병렬만 조건부. codex 실측은 feature-draft census로.
