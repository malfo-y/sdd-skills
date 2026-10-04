# 토론 요약: 하네스 전면 재편 — 오케스트레이터 기반 multi-agent

**날짜**: 2026-10-04
**상태**: 정상 종료
**검증 결과**: 제안한 논의 순서 6단계(남길 철학 → 오케스트레이터 형태 → worker 경계 → 인계 계약 → 병렬·쓰기 정책 → 전환 방식)를 모두 다뤘다. 비용 허용치, 지표 임계값, 역할 배치 초안의 명시 확인은 미결이다. 이 토론의 실측 근거는 모두 선행 토론(cold start)에서 나왔고, 방식당 표본은 1회다.

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)
- **사용자 문제 제기와 배경**: 사용자는 지금의 하네스를 SDD 철학만 남기고 오케스트레이터 기반 multi-agent 방식으로 전면 재편하려 한다. 선행 토론 `_sdd/discussion/2026-10-04_discussion_subagent_cold_start.md`에서 확인한 cold start 대응책(fork 0초, 레시피형 digest 약 4초)이 출발점이다.
- **현재 상태**: custom agent 0종이고, 체인(discussion → feature-draft → plan-review → implementation → implementation-review → spec-sync)은 메인 루프 직접 실행이 기본이다. 과거 agent 기반 경로는 "메인 루프가 가진 맥락을 다시 파악하는 비용" 때문에 폐지됐다(full 레인, spec-sync agent, plan-review agent).
- **범위와 제외 범위**: 재편의 구조 결정 6가지를 다뤘다. 구현 상세, spec 문구, 스킬 이름은 다루지 않았다.
- **수집한 근거**:
  - 선행 토론 실측: 일반 subagent 기동 2~4초. fork는 부모 cache를 재사용한다. 레시피형 digest를 받은 worker는 AC 9개 검사를 13초에 끝냈다. 노트를 받은 worker는 AC 밖 결함을 놓쳤고 새 agent 단독만 찾았다(각 1회).
  - Codex: `spawn_agent`의 `fork_turns`를 생략하거나 `"all"`이면 전체 맥락 fork다(codex-cli 0.160.0 도구 설명). 과거 실행에서 "root 포함 동시 4개 제한"이 관측됐다(`_sdd/spec/decision_log.md:843`).
  - goal 하네스: `_sdd/goal/<date>_<slug>/`의 `goal.md`(조건·검증 레시피·자율 수행 위임·Loop Protocol), `experiments.md`, `journal.md`, `report.md`(`.claude/skills/goal-init/SKILL.md:16,42`).
  - implementation ledger: implementation 단계가 자기만 쓰고 읽는 재개용 파일이다. 상태 4단계, RED/GREEN 명령, 계획 이탈·발견, AC→증거 테이블을 담는다(`.claude/skills/implementation/SKILL.md:49-60`). 리뷰어는 읽지 않는다(`_sdd/spec/main.md:89`, fresh verification).
  - spec 정체성: "Claude Code와 Codex에서 공통으로 사용할 수 있는 SDD workflow bundle", 스킬이 진입점, `_sdd/` 파일 인계(`_sdd/spec/main.md` §1).

## 핵심 논점 (Key Discussion Points)
1. **재편이 이번에는 성립할 근거**: 과거 실패의 원인(다시 파악하는 비용)에 대해 실측된 해법이 생겼다. 남는 위험은 다음과 같다: worker당 고정 비용(system prompt 18~35k 토큰), cold start 뒤의 병목(검토 범위·반환 길이), 새 시선과 속도의 교환, 런타임 공통 계약의 제약, 측정은 push와 새 세션에서만 가능하다는 점.
2. **오케스트레이터 형태**: 코드형(Claude Workflow 도구)은 Codex에 없어 공통 계약에 걸린다(Codex 부재는 미검증). 스킬형은 두 런타임 모두 동작하고 단계 중간에 사용자 질문이 가능하다. 대신 "메인 루프가 worker의 일을 직접 하는" 일탈을 구조로 막기 어렵다. 메인 루프의 Read는 막을 수 없으므로, 일탈은 미리 정한 지표로 감시한다.
3. **역할 배치 초안** (기본값으로 제시했고, 사용자의 명시 확인은 없음):
   - discussion은 오케스트레이터가 직접 수행한다(사용자 대화 필요. worker가 사용자에게 직접 물을 수 없다는 전제는 미검증).
   - feature-draft는 계획 worker 1개, plan-review·implementation-review는 작성자와 분리된 리뷰 worker(관점별 병렬 가능), spec-sync는 작성 worker 1개다.
   - 수정 루프는 원래 작성 worker를 digest + findings로 다시 띄운다.
   - 게이트 순서는 각 작성 스킬이 아니라 오케스트레이터가 정한다.
4. **digest 초안** (구조는 사용자 결정, 섹션은 제안):
   - 목표·범위: draft·discussion 포인터만, 복사하지 않는다.
   - 결정·제약: 채팅에서만 나온 결정·선호·계획 이탈, 현재 유효한 것만.
   - 환경 함정, 검증 레시피(AC → 명령 → 기대값).
   - 상태·통과 주장·이력은 넣지 않는다.
   - worker는 반환에 "digest 변경분" 블록을 넣고 오케스트레이터가 반영한다. 병렬 변경분이 모순되면 오케스트레이터가 표시하고 다시 계획한다.
   - 크기는 v2 노트(약 2.5KB) 수준에서 시작해 실측으로 조정한다.
5. **병렬·쓰기 정책 기본값** (질문의 전제로 제시했고 이의 없음):
   - 단일 작성자: digest·state는 오케스트레이터, 코드는 그 task의 worker, draft는 계획 worker, spec은 spec-sync worker.
   - worker는 git 쓰기를 하지 않는다(병렬 커밋의 `index.lock` 충돌 방지). 단계 경계에서 오케스트레이터가 커밋한다.
   - task worker는 자기 task의 RED→GREEN만 한다. 전체 회귀는 리뷰 worker의 레시피 fresh 실행으로 대신한다.
   - worker 실패 시 1회 다시 띄우고, 또 실패하면 멈추고 보고한다.
   - Claude는 기존 watchdog 훅이 적용되고, Codex에는 대응 기능이 없다.
6. **성공 지표 6종** (임계값은 기존 경로 기준선 측정 뒤 정함): 오케스트레이터 맥락 증가량, 체인 벽시계, 품질(게이트 finding·AC 밖 결함), 오케스트레이터 일탈(메인 루프의 코드 Edit 목표 0, Read 횟수), worker cold start 시간, 총 토큰.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| 1 | 재편 후에도 남길 철학: spec 중심 루프와 검증(falsifiable AC, fresh verification), Claude·Codex 공통 계약, 산출물 원칙(§0 3원칙 + `_sdd/` 파일 인계) | 사용자 선택 (사용자 판단) | 1 |
| 2 | 오케스트레이터는 스킬 형태로 만든다. 메인 루프가 지휘하고 digest·state를 소유하며, 무인 모드는 native `/goal` 위에 얹는다 | 사용자 선택 (사용자 판단). 두 런타임 동작과 기존 goal 하네스 존재 (코드 확인) | 2 |
| 3 | implementation은 task별 worker로 한다. Target Files가 서로소이고 계약을 공유하지 않는 task만 병렬로 돌리며, worktree 없이 같은 작업 트리를 쓴다 | 사용자 선택 (사용자 판단) | 3 |
| 4 | 인계는 digest(방법·이유, 모든 worker) + state(단계·task 상태·열린 finding, 오케스트레이터 재개용, 리뷰어에게 주지 않음) 2파일로 나눈다. 기존 implementation ledger는 state로 흡수한다 | 사용자 선택 (사용자 판단). fresh verification 원칙 `main.md:89` (코드 확인) | 4 |
| 5 | 병렬 worker 상한은 두지 않고 런타임에 맡긴다. 나머지 병렬·쓰기 기본값(논점 5)은 이의 없이 유지한다 | 사용자 선택 (사용자 판단) | 5 |
| 6 | 전환은 새 오케스트레이터 경로를 기존 옆에 나란히 만들고, 같은 기능을 신·구로 실측 비교한 뒤 기본 경로를 교체하고 구 경로를 삭제한다 | 사용자 선택 (사용자 판단). 7월 lite→full 삭제 선례 (코드 확인) | 6 |

### 기각한 대안
- 코드형 오케스트레이터(Claude Workflow 도구): Codex에 없어 공통 계약 원칙에 걸린다(Codex 부재는 미검증).
- 외부 스크립트 오케스트레이터(`claude -p` / `codex exec`): 단계 중간 사용자 질문이 불가하고, 단계마다 세션을 새로 띄우는 비용이 들며, 스킬이 진입점이라는 개념에서 벗어난다.
- 구현 worker 1개, 또는 task별 항상 순차: 병렬 이득이 없다.
- digest 1파일 + 리뷰어용 잘라 주기: 리뷰어가 파일을 직접 열면 통과 주장이 보인다. 구조로 막지 못한다.
- goal 하네스를 digest·state로 확장: 무인 모드 개념과 대화형 실행이 섞인다.
- 병렬 상한 공통 3 / 런타임별 상한: 사용자가 런타임 위임을 택했다.
- 단계별 점진 교체: 중간 상태에서 체인이 섞이고 신·구 비교가 어렵다.
- 한 번에 재작성: 실측 없이 전부를 건다(7월과 같은 위험).

## 미결 질문 (Open Questions)
| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| Q1 | 총 토큰 증가를 얼마까지 허용할까? | deferred-deliberately (auto-labeled, please review) | 사용자가 이 결정 전에 정리를 택했다. 기준선 측정(Q2) 뒤 정하는 것이 자연스럽다 |
| Q2 | 성공 지표 6종의 임계값은? | needs-data | 기존 경로로 같은 기능을 돌린 기준선이 필요하다 |
| Q3 | 역할 배치 초안(논점 3)과 digest 섹션 초안(논점 4)을 그대로 확정할까? | deferred-deliberately (auto-labeled, please review) | 기본값으로 제시했고 명시 확인은 없었다. 후속 feature-draft에서 확정한다 |
| Q4 | Codex에서 동시 상한을 넘겨 spawn하면 줄을 서나, 오류가 나나? | needs-data | 결정 5(상한 없음)가 Codex에서 성립하려면 필요하다. 오류라면 오케스트레이터가 다시 띄워야 한다 |
| Q5 | AC 밖 탐색을 리뷰 worker에게 어떻게 맡길까? | needs-data | 선행 토론 Q6과 같다. 새 agent 단독만 실제 결함을 찾았다(1회) |
| Q6 | worker의 검토 범위와 반환 길이를 어떻게 통제할까? | out-of-scope (auto-labeled, please review) | cold start 뒤의 병목이다. 별도 레버다 |
| Q7 | worker(subagent)가 사용자에게 직접 질문할 수 없다는 전제가 맞나? Codex에 코드형 오케스트레이터가 없다는 전제가 맞나? | needs-data | 논점 2·3의 전제다. 둘 다 미검증이다 |

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | 재편과 충돌하는 spec 결정을 목록화하고 spec을 먼저 갱신한다. 대상 예: "코드·테스트는 메인 루프가 직접 작성", "custom agent 0종", "품질 게이트는 producer 소유", "reviewer는 ledger를 소비하지 않는다" | High | 미정 |
| 2 | feature-draft(롤링 분할)로 재편을 시작한다. 첫 기능은 오케스트레이터 스킬 + digest/state 계약 + 기존 경로 기준선 측정 | High | 미정 |
| 3 | Codex 상한 초과 spawn 동작을 확인한다(Q4) | Medium | 미정 |

### 후속 핸드오프 (Handoff)
- **목표**: 새 오케스트레이터 경로가 기존 경로 옆에서 Claude·Codex 모두 동작하고, 같은 기능을 신·구로 실행해 성공 지표 6종을 비교할 수 있다.
- **변경 금지 제약**: 교체 결정 전까지 기존 스킬 경로의 동작과 의미를 바꾸거나 삭제하지 않는다. 결정 1의 철학 3종을 지킨다. 두 런타임 미러를 함께 다룬다. digest에는 상태·통과 주장을 넣지 않는다. worker는 git 쓰기를 하지 않는다.
- **검증**: push와 플러그인 갱신 뒤 새 세션에서 신·구를 같은 기능으로 실행하고 transcript로 지표 6종을 계측한다. 메인 루프의 코드 Edit 횟수를 별도로 센다.
- **중단 조건**: 새 경로가 벽시계나 품질에서 기존보다 나쁘거나, 오케스트레이터 일탈(메인 루프의 코드 Edit)이 반복되거나, Codex에서 공통 계약이 성립하지 않으면 멈추고 보고한다.
