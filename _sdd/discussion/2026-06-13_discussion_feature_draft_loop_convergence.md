# 토론 요약: feature-draft-agent 가속 — review-fix loop 수렴

**날짜**: 2026-06-13
**라운드 수**: 6
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)
- **사용자 문제 제기**: `feature-draft-agent`가 하나의 거대한 단일 agent라 내부 병렬화가 안 된다는 이해가 맞는지 확인하고, 가속 방법을 찾고 싶다.
- **토론을 시작한 배경**: feature-draft 산출(draft 생성)의 wall-clock을 줄이려는 목적. 목표는 명시적으로 **속도/지연 단축**으로 고정됨.
- **현재 상태**: `feature-draft-agent.md`(tools: Read/Write/Edit/Glob/Grep — `Agent` 없음), `feature-draft/SKILL.md`(orchestrator, review-fix loop 소유), `plan-review-agent.md`(6-smell rubric), `implementation/SKILL.md`(병렬 패턴)를 직접 읽어 확인. 실제 산출물 `_sdd/drafts/2026-06-12_feature_draft_agents_md_harness_layer.md`(5 task)를 케이스로 분석.
- **범위와 제외 범위**: 포함 — feature-draft 생성 가속 레버 탐색. 제외 — 출력량 다이어트(사용자가 "크게 의미 없음"으로 배제), 병렬화(분석 후 ROI 음수로 기각).
- **수집한 근거**: 위 4개 agent/skill 파일 + 실제 draft 1건 + 사용자 메모리(병목=작성/추론, 탐색분리 반증, 출력 다이어트 −28%).

## 핵심 논점 (Key Discussion Points)
1. **"내부 병렬화 불가" 정정**: subagent는 `Agent` 도구가 없어 sub-agent fan-out은 불가(사용자 이해 맞음). 단 단일 컨텍스트 내 Read/Grep/Glob **I/O 병렬은 가능**. 못 떼는 건 추론·작성뿐.
2. **병렬화(C안)가 막히는 구조적 이유**: implementation 병렬은 파티션(disjoint Target Files + 충돌의 dependency 인코딩)이 *상위 단계 산출물*이라 가능. feature-draft는 draft 작성 자체가 파티션을 정하는 일 → 닭-달걀. Part 2는 C*/I*/V* ID·linkage가 전역 공유 상태라 분할 시 merge가 직렬 reasoning이 됨.
3. **실제 draft 분석**: 작성 의존 스파인(context→C/I→Touchpoints→T→V→교차표)은 환원 불가능한 직렬이고 추론이 여기 집중. 병렬 가능한 건 Task body(L147~263, ~41%)뿐인데 이건 고출력·저추론 = A안(다이어트)과 같은 대상. 5 task 규모에선 broadcast+merge 오버헤드가 이득을 먹음.
4. **재프레임 — 비용은 생성이 아니라 loop가 곱한다**: 스킬 wall-clock = 생성 1회 + N×(review+fix+re-review), MAX 3. N=2~3이 흔함(사용자 확인) → loop가 multiplier로 지배. 진짜 레버는 생성 최적화가 아니라 N→1 수렴.
5. **producer self-check ↔ reviewer rubric 대조**: producer self-check 목록이 reviewer 6-smell의 **부분집합**. 중복 차원(Verification Weakness/Scope Creep/Single-use Abstraction)은 producer가 이미 충족 → PASS. 갭 차원(New File Justification / Task Boundary Drift / DRY 중복구현)은 self-check 없음 → 매 회차 finding → **N=2~3의 엔진**.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| 1 | feature-draft 병렬화는 접는다 (C/B안 기각) | 파티션 닭-달걀 + 5~8 task 규모 ROI 음수 (`코드 확인`) | 2, 3 |
| 2 | 가속 레버는 **review-fix loop를 N→1 수렴**시키는 것 (multiplier) | N=2~3 흔함, loop가 생성보다 비용 큼 (`사용자 판단` + `코드 확인`) | 4 |
| 3 | 레버 본체는 **L1(갭 3차원을 producer self-check에 내재화/shift-left)**, L2(중복 제거)는 부수 — 중복 차원은 producer가 이미 충족해 loop 안 돌리므로 그대로 둔다 | self-check는 warm context(쌈), loop iteration은 cold respawn ×3(비쌈) → 싼 것 3개 ↔ 비싼 것 1~2회 = 순이득 (`코드 확인`) | 5 |
| 4 | self-check 3문구는 **producer 자기 음성의 독립 점검**으로 쓰고 reviewer rubric명을 박지 않는다 | "가리키기, 복사 금지" + skill/agent 비-mirror 규범, reviewer 변경 시 stale 방지 (`코드 확인`) | 5 |
| 5 | self-check는 **생성 mode 전용**(fix mode는 surgical이라 제외), 통과 흔적 비노출(L238 규범) | fix mode 계약·검증흔적 비노출 규범 정합 (`코드 확인`) | 5 |
| 6 | **앵커안 채택** — Step 6 self-check 3줄 + AC 목록 1줄 + Step 8 저장 체크리스트 1줄(3곳). self-check를 producer AC로 승격해 Final Check가 강제 | 최소안은 self-check가 "권고"로 남아 스킵 위험 → N 수렴이 들쭉날쭉 (`사용자 판단`) | 5 |

### 기각한 대안
- **C안 (Part 2 task별 병렬 producer)**: 파티션 닭-달걀 + 단일 작성자 불변식 위배 + merge가 직렬 reasoning. C-2(scaffold-then-fill)는 큰 draft(15~25 task)에서만 의미 있으나 그 규모는 이미 implementation-plan으로 분리됨.
- **B안 (orchestrator가 context 탐색 선처리)**: 탐색 분리는 사용자 메모리상 이미 반증 + Hard Rule 5/6이 Target Files 재확인 강제 → 이중 작업.
- **출력량 다이어트(A안)를 주 레버로**: 사용자가 "크게 의미 없음"으로 배제. 단 갭 없는 중복 차원은 A안이 이미 덮는 영역.
- **L2(검증 중복 제거)를 본체로**: 중복 차원은 producer가 충족 중이라 제거하면 reviewer가 그 차원을 처음 보게 돼 오히려 위험. 부수로만 둠.
- **최소안 (Step 6에만 3줄)**: AC/Step8에 없어 Final Check가 검증 못 함 → 스킵 위험. 기각.

## 미결 질문 (Open Questions)
| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| 1 | N=2~3을 실제로 유발하는 recurring finding이 갭 3차원(New File Justification/Task Boundary/DRY)이 맞는지 측정되지 않음 | needs-data | 만약 loop가 중복 차원(이미 덮인)이나 다른 원인으로 도는 거면 L1 효과가 underperform. 적용 후 iteration 수·finding 카테고리 로그로 검증 필요 |

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | `feature-draft-agent.md` Step 6에 "계획 품질 self-check" 3문구 추가 (L236~L238 사이) | High | 후속 편집 |
| 2 | 동 파일 Acceptance Criteria 목록(L18~27)에 self-check 1줄 추가 | High | 후속 편집 |
| 3 | 동 파일 Step 8 저장 체크리스트(L276~287)에 self-check 1줄 추가 | High | 후속 편집 |
| 4 | `.codex/agents/feature-draft-agent.toml` 미러 동기 (양쪽 동일 계약) | High | 후속 편집 |
| 5 | 적용 후 review-fix iteration 수 추이 관찰 (미결 Q1 검증) | Medium | 운영 관찰 |

### 후속 핸드오프 (Handoff)
- **목표**: feature-draft 생성 후 첫 draft가 `plan-review-agent` 6-smell을 한 번에 통과하도록 producer가 갭 3차원을 self-check → review-fix loop가 N=1로 수렴. 관찰 가능 완료 기준: 갭 3차원이 첫 review에서 finding으로 안 잡힘.
- **삽입할 문구 (Step 6, L236↔L238 사이)**:
  ```
  이어서 계획 품질 self-check를 수행한다 (생성 단계에서 닫을 수 있는 계획 smell — 통과 흔적은 산출물에 남기지 않는다):
  - 신규 파일 근거: 모든 [C] Target File에 "왜 기존 파일 수정이 아니라 신규 생성인가" 근거가 해당 task description 또는 Technical Notes에 있는가? 없으면 [M]으로 바꾸거나 근거를 추가한다.
  - task 단일 목적: 각 task가 하나의 명확한 목적을 갖는가? 한 task가 독립적 변경 2개 이상을 묶었으면 분리하거나, 묶는 이유를 Technical Notes에 적는다.
  - 중복 구현: 같은 로직·상수·계약을 여러 task가 각자 구현하도록 계획하지 않았는가? 중복이 있으면 shared setup task로 추출하거나 dependency로 연결한다 (단 단일 사용처 추상화는 금지 — Hard Rule 12와 균형).
  ```
- **추가할 AC 1줄 (L18~27)**: `[ ] Part 2의 모든 [C]에 신규파일 근거가 있고, 각 task가 단일 목적이며, task 간 중복 구현이 없음을 self-check했다 (흔적 비노출).`
- **변경 금지 제약**: (1) reviewer 6-smell명을 producer에 박지 말 것(stale 방지). (2) 중복 차원(Verification Weakness/Scope Creep/Single-use Abstraction) self-check를 새로 추가하지 말 것(이미 덮임). (3) 검증 흔적을 draft 산출물에 남기지 말 것(L238 규범). (4) fix mode에 self-check 추가 금지(생성 mode 전용). (5) global spec thin 불변 — 이 변경은 agent 파일 한정.
- **검증**: 적용 후 임의 feature 요청으로 feature-draft 실행 → 첫 review에서 New File Justification/Task Boundary/DRY finding이 안 나오는지 확인. iteration 수가 줄어드는지 추이 관찰.
- **중단 조건**: self-check 3문구가 Hard Rule 12(단일 사용처 추상화 금지)와 충돌하는 권고를 만들면 중단·보고. reviewer rubric 구조가 토론 전제와 다르게 동작하면(예: 갭 차원이 실제로 finding을 안 만들고 있었음) 중단·재검토.

## 리서치 결과 요약 (Research Findings)
- `feature-draft-agent`: 단일 producer, sub-agent spawn 불가, 생성/fix 2-mode.
- `feature-draft/SKILL.md`: orchestrator가 review→fix→re-review loop 소유(exit `critical=high=medium=0`, MAX 3, 전체 재리뷰).
- `plan-review-agent`: 6-smell(Scope Creep / New File Justification / Single-use Abstraction / Task Boundary Drift / DRY Risk / Verification Weakness) + Decision/Assumption Review. Critical/High만 blocker.
- 대조 결과: producer self-check = reviewer rubric의 부분집합. 갭 = New File Justification / Task Boundary Drift / DRY(중복구현 방향).

## 토론 흐름 (Discussion Flow)
- Round 1: "내부 병렬화 불가 맞나?" → 맞음(fan-out 불가), 단 I/O 병렬은 가능. 목표=속도 확정.
- Round 2: 가속 대안 A/B/C 제시 → 병렬화 ROI 의심(병목=작성).
- Round 3: implementation 병렬 패턴 대조 → C안 닭-달걀·단일작성자·merge 직렬로 고위험.
- Round 4: 실제 draft 분석 → 스파인 직렬, 병렬 가능 부위는 저추론 41%, 5 task 규모 ROI 음수. 병렬 접음.
- Round 5: 재프레임(loop=multiplier), N=2~3 흔함 확인 → L1+L2 = 최대 레버.
- Round 6: rubric 대조 → 갭 3차원이 원인. 앵커안으로 self-check 내재화 설계 확정.

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 이 토론으로 실제로 풀려는 문제는? **A**: 속도/지연 단축.
**Follow-up**: "내부 병렬화 불가"는 fan-out에 한해 맞고 I/O 병렬은 가능. 병목은 작성(추론)이라는 과거 결론 환기.

### Round 2
**Q**: 병목 전제를 그대로 쓸까 재측정할까? **A**: implementation 병렬 패턴 보면 C안에 끌린다, 고위험을 더 논의하자.
**Follow-up**: implementation skill 정독 후 비교 준비.

### Round 3~4
**A(사용자)**: feature-draft 읽어보니 쪼갤 구석이 안 보인다. 실제 draft 보며 분석 요청.
**Follow-up**: draft 분석 → 스파인 직렬·저추론 41%·5 task ROI 음수. 병렬 접기로 수렴.

### Round 5
**A(사용자)**: 병렬화 접고 다른 가속법 찾자. 출력량 줄이기는 의미 없음.
**Follow-up**: 재프레임(loop multiplier). **A**: N=2~3 흔하다.

### Round 6
**Follow-up**: producer self-check ↔ reviewer rubric 대조 → 갭 3차원 발견. L1 앵커안 설계. **A**: (2) 설계까지 가자 → 앵커안 좋아.
