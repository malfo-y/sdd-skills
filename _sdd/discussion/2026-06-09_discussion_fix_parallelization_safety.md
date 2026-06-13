# 토론 요약: 병렬화 책임 재배치와 fix 병렬화 검토

**날짜**: 2026-06-09
**라운드 수**: 7
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)

- **사용자 문제 제기**: SDD 파이프라인이 큰 subagent를 dispatch하는 구조라 병렬화가 제한적이고 느리다고 느낌. 특히 단일 `implementation-agent` call 자체가 느려, 그 안에서 파일별 편집을 병렬화하거나 orchestration 레벨에서 병렬화를 강화하고 싶었음.
- **토론을 시작한 배경**: Claude Code의 `/goal`·Workflow 도구를 살펴보며 "병렬화를 어디서 어떻게 책임질 것인가"를 재설계할 수 있을지 탐색. 형님이 4가지 변경 안건(병렬화를 implementation orchestrator로 집중 → feature-draft/plan에서 제거 → autopilot에서 재처리 → 공용 component로 추출 + Target File 도출까지 흡수)을 제시하며 논의 요청.
- **현재 상태**: 
  - `implementation-plan-agent`가 task 분해 + `Target Files`([C]/[M]/[D]) + `Dependencies`(엣지)를 생성. 명시적 DAG 객체는 없으나 Dependencies가 사실상 DAG 엣지.
  - `implementation` orchestrator가 `deriveGroups`(같은 phase + dependency 없음 + Target Files disjoint → 병렬)로 병렬 그룹 파생. fan-out 직전 file-disjoint set-intersection 가드레일.
  - `sdd-autopilot`은 `deriveGroups`를 자체 구현하지 않고 메타데이터 계약으로 위임. per-group/Checkpoint review-gate 의미론만 소유.
  - review-fix loop가 세 스킬 + autopilot에 항상 내장. fix는 finding 하나씩 **순차** dispatch("별도 fix 분해 기계장치 없음").
- **범위와 제외 범위**: 병렬화 책임의 위치·중복·공용화, fix 병렬화의 타당성·안전성을 다룸. 실제 코드 구현은 하지 않음(review-only 토론).
- **수집한 근거**: `.claude/skills/implementation/SKILL.md`(deriveGroups, fix loop), `.claude/agents/implementation-plan-agent.md`, `.claude/agents/feature-draft-agent.md`, `.claude/skills/sdd-autopilot/SKILL.md`, `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`(§2, line 164).

## 핵심 논점 (Key Discussion Points)

1. **단일 agent 내부 병렬화 불가**: 단일 call의 병목은 파일 I/O가 아니라 LLM 추론(autoregressive·순차). 한 agent 안에서 Edit를 병렬로 내도 추론 시간은 안 줄어듦. 병렬화의 유일한 레버는 일을 잘게 쪼개 여러 agent로 추론을 병렬화하는 것 = orchestration.
2. **"추출할 로직"의 정체**: `deriveGroups`는 결정론적 알고리즘(추출 가능, 이미 한 곳). 반면 Target Files/Dependencies "도출"은 LLM의 의미적 판단이라 task 분해와 한 몸 → 떼어내면 코드 재사용이 아니라 중복 추론만 생김.
3. **중복의 정체**: 병렬화 *로직*은 implementation 한 곳뿐. 여러 곳에 중복된 건 "의미적 충돌→dependency 인코딩" 규약 *설명 prose*(feature-draft ≈ implementation-plan). 해법은 agent 추출이 아니라 문서 중앙화.
4. **autopilot 전제 교정**: autopilot은 `deriveGroups`를 자체 구현하지 않음 → 안건 2("autopilot이 직접 구현하니 재처리 필요")의 전제 약화.
5. **dependency의 두 출처**: 파일 충돌 기반(Target Files로 자동 도출, planner 불필요) vs 의미적 충돌 기반(파일 안 겹쳐도 얽힘, planner만 판단 가능). "관계를 planner가 직접 그릴지 / produce-consume 선언으로 orchestrator가 조립할지"는 설계 선택.
6. **재사용 동기(reviewer)**: 형님 핵심 의도 = "의도→Target Files+DAG" 컴파일러를 planner·reviewer가 공유. review-fix loop가 항상 있으니 두 번째 사용처는 빈도상 실재.
7. **fix는 의도적 순차**: orchestrator-contract.md:164 — "finding 수가 적고 상호작용 가능 → 순차 안전". 미구현이 아니라 설계 결정.
8. **fix 병렬화 안전성의 본질적 난점**: ① finding은 disjoint하게 자를 자유가 없음(문제 위치는 코드가 정함). ② review-fix는 *수렴 루프*라 병렬 fix 충돌 시 라운드가 늘어 총 수렴 시간이 오히려 길어짐.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | **fix 병렬화는 도입하지 않는다. 현재 "finding 순차" 설계 유지.** | 구현 복잡성·충돌 위험 > 속도 이득. review-fix는 수렴 루프라 병렬 fix 충돌이 수렴을 지연시킴 | 7, 8 |
| 2 | 단일 agent 내부 편집 병렬화는 추진하지 않는다 (원리적으로 속도 이득 없음) | LLM 추론은 순차, 파일 I/O는 병목 아님 | 1 |
| 3 | 공용 "DAG/Target Files 도출 agent" 신설(안건 3,4)은 불필요 | 추출할 결정론적 로직 없음(Target Files 도출=LLM 판단+의도와 한 몸), `deriveGroups`는 이미 공용 | 2, 3 |
| 4 | 형님 목표(fix 병렬화)는 "deriveGroups를 fix에 재사용"으로 환원되나 안전성 때문에 보류 | 의미적 충돌을 file-disjoint로 못 잡고, 수렴 루프 특성상 위험 | 5, 8 |

## 미결 질문 (Open Questions)

| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| 1 | "의미적 충돌→dependency 인코딩" 규약 prose의 3중복(feature-draft:219 ≈ implementation-plan:83 ≈ implementation)을 공용 참조 1곳으로 중앙화할 것인가 | deferred-deliberately | fix 병렬화 결정과 무관한 독립적 DRY 개선. 별도 작업으로 다룰 수 있음. 우선순위 낮음 |

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | 코드 변경 없음 — 현행 "fix 순차" 설계 유지 (현상 유지 결정) | — | — |
| 2 | (선택) 규약 prose 3중복을 공용 참조로 중앙화 | Low | 추후 형님 판단 |

## 리서치 결과 요약 (Research Findings)

- **implementation-plan-agent**: task마다 `ID`/`Target Files`([C/M/D])/`Dependencies`(backward-reference 엣지) 생성. 명시적 DAG 객체는 없으나 Dependencies가 위상정렬 가능한 DAG 엣지 역할.
- **implementation/SKILL.md**: `deriveGroups` pseudocode 보유(같은 phase + dependency 없음 + Target Files disjoint → 병렬). fan-out 직전 file-disjoint 가드레일.
- **sdd-autopilot**: `deriveGroups`를 자체 구현하지 않음. orchestrator 메타데이터 계약으로 위임. per-group/Checkpoint review-gate 의미론만 소유(서로 다른 추상화 레벨의 부분 중복).
- **fix dispatch (orchestrator-contract.md:164)**: finding 하나씩 순차. "별도 fix 분해 기계장치는 없으며 ... finding 수가 적고 상호작용 가능 → 순차 안전". `deriveGroups` 재사용 안 함.
- **finding 구조**: severity(Critical/High/Medium/Low) 분류만 명시. 영향 파일은 finding 설명에서 암묵적으로 도출("finding 영향 파일 = 그 leaf의 Target Files").

## 토론 흐름 (Discussion Flow)

- Round 1~2: "공용 컴포넌트로 추출"의 의미 명확화 → "추출할 결정론적 로직이 없다"(Target Files 도출은 LLM 판단)로 정리
- Round 3: dependency의 두 출처(파일 충돌 자동 vs 의미적 충돌 planner) 구분
- Round 4: 형님 진짜 동기 = planner·reviewer 공유 "의도→Target Files+DAG" 컴파일러
- Round 5: fix가 **의도적 순차**임을 코드로 확인 → 형님이 "finding 많고 독립적"으로 도전
- Round 6: 형님 목표가 "deriveGroups를 fix에 재사용"으로 환원됨(새 component 불필요) 확인
- Round 7: fix 병렬화 안전성의 본질적 난점(자를 자유 없음 + 수렴 루프) → **"느려도 안전하게" 결론, fix 병렬화 보류**

## 부록: 대화 로그 (Conversation Log)

### Round 1–2 (문제 본질 / "추출할 로직")
**논의**: planner가 task와 함께 Target Files를 정의하는 건 효율적이나 분리 불가능은 아님. 단 Target Files/Dependencies 도출은 결정론적 알고리즘이 아니라 LLM 판단이라, "공용 agent 추출"이 코드 DRY 이득을 주지 못하고 중복 추론만 추가.
**결론**: 추출 가능한 로직은 `deriveGroups`뿐이고 그건 이미 한 곳. 중복은 규약 prose.

### Round 3 (dependency의 출처)
**논의**: 파일 충돌 dependency는 Target Files로 자동 도출(이미 orchestrator가 함). 의미적 충돌 dependency만 planner가 판단 가능. 관계 인코딩을 produce/consume 선언으로 일반화하는 대안도 존재.

### Round 4 (재사용 동기)
**A**: 형님 — planner뿐 아니라 reviewer가 "수정할 task 덩어리"만 주면 component가 Target Files/DAG를 찾아내는 그림.
**Follow-up**: 재사용 가치는 reviewer 등 두 번째 사용처의 실재성에 달림. reviewer는 Target Files를 모르는 입력원이라 오히려 component 가치가 클 수 있음.

### Round 5 (fix 순차의 정체)
**A**: 형님 — "review→fix loop가 항상 박혀 있으니 finding→병렬 수정이 거의 항상 일어난다."
**Follow-up**: review-fix는 항상 있으나(✅), fix는 **의도적 순차**(orchestrator-contract.md:164). 형님 → "순차 설계에 도전, finding은 많고 독립적이다."

### Round 6 (deriveGroups 재사용으로 환원)
**Follow-up**: 형님 목표는 새 component가 아니라 "기존 `deriveGroups`를 fix 경로에도 적용"으로 환원됨. "공용화"하려던 절반(dependency 계산)은 이미 공용, 나머지(Target Files 도출)는 의도와 한 몸.
**A**: 형님 — "fix 병렬화의 안전성부터" 보자.

### Round 7 (안전성 → 결론)
**Follow-up**: fix 병렬화 안전성의 두 난점 — ① finding은 disjoint하게 자를 자유가 없음, ② review-fix가 수렴 루프라 병렬 fix 충돌 시 수렴 지연(역효과). 안전성 모델 3안(file-disjoint 보수적 / reviewer dependency 인코딩 / worktree 격리) 제시.
**A**: 형님 — "여기까지 하자. 구현 복잡성·위험이 속도 이득보다 크다. 느려도 안전하게 가는 게 낫겠다." → **fix 병렬화 보류 결정.**
