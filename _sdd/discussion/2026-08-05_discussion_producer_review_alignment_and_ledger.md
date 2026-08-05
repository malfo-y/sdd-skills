# 토론 요약: producer-review 계약 정렬과 implementation ledger

**날짜**: 2026-08-05
**라운드 수**: 11
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)

- **사용자 문제 제기**: Claude Code Opus 5가 `feature-draft`·`implementation`을 수행할 때 리뷰에서 많은 실수가 잡히며, 앞선 진단의 개선안 1~3을 적용할 가치가 있는지 판단하고자 했다.
- **토론을 시작한 배경**: 진단에서 producer↔reviewer 계약 비대칭, 전파 표면 탐색 격차, implementation의 자연어 상태 관리 부담이 구조적 원인으로 확인됐다. 후속 feature-draft가 바로 소비할 수 있도록 적용 범위와 최소 계약을 닫을 필요가 있었다.
- **현재 상태**: `feature-draft`의 Open Questions 산출 계약은 `plan-review-agent`의 decision/assumption 요구보다 좁다. census 검증 task는 rename/전파류에 초점이 있고, `implementation`은 task별 RED→GREEN·coverage delta 상태를 별도 artifact 없이 유지한다. `_sdd/implementation/`은 로컬 process artifact의 canonical surface다.
- **범위와 제외 범위**: 중요 결정 계약 정렬, 조건부 propagation 표, 최소 implementation ledger를 다뤘다. 실제 Opus 5 finding 감소율 측정, 리뷰 dedup·자동 재리뷰 변경, 스킬·spec 구현은 제외했다.
- **수집한 근거**: `.claude/skills/feature-draft/SKILL.md`, `.claude/skills/implementation/SKILL.md`, `.claude/skills/implementation-review/SKILL.md`, `.claude/agents/plan-review-agent.md`, `.claude/agents/implementation-review-agent.md`, `_sdd/spec/main.md`, 최근 `_sdd/work_log/` finding 사례.

## 핵심 논점 (Key Discussion Points)

1. **적용 단위**: 1·2는 draft producer-review 계약 문제이고, 3은 implementation 실행 상태 문제라 한 feature로 묶으면 범위와 효과 원인이 섞인다.
2. **계약 정렬의 밀도**: reviewer 요구를 모든 결정에 강제하면 사소한 초안에도 형식 노동이 생긴다. 결과 방향을 바꿀 수 있는 중요 결정만 명시 대상으로 좁혀야 한다.
3. **전파와 일반 다중파일 변경의 구분**: 모든 Target Files를 다시 표로 만들면 중복이다. 동일 변경 요소가 미러·등록·템플릿·문서 등 둘 이상의 동기화 표면에 걸칠 때만 propagation 표가 필요하다.
4. **ledger의 목적**: 감사 로그가 아니라 compact 이후 다음 행동을 결정하기 위한 resume pointer여야 한다. 출력 전문과 서술형 진행기는 제외한다.
5. **적용 강제성**: 복잡할 때만 ledger를 만드는 조건은 모델의 복잡도 과소평가에 취약하다. 모든 implementation 실행에 동일한 작은 계약을 적용한다.
6. **효과 판정 경계**: 이번 변경은 구조 검증까지만 닫고, 실제 finding 감소율은 주장하거나 측정하지 않는다.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| 1 | Feature A(계약 정렬+전파표)와 Feature B(ledger)를 분리하고 A를 먼저 수행한다. | 서로 다른 실패 원인과 변경 표면을 분리해야 범위가 작고 검증이 닫힌다 (`사용자 판단`) | 1 |
| 2 | producer와 reviewer는 결과 방향을 바꿀 수 있는 중요 결정에만 가정·근거·기각 대안·확신도·사용자 확인 여부를 요구하도록 동일하게 맞춘다. | 현 producer 산출 계약보다 reviewer 요구가 넓다는 직접 대조 (`코드 확인`) | 2 |
| 3 | 동일 변경 요소가 둘 이상의 동기화 표면에 전파될 때만 draft 전역 `Propagation Surfaces` 표를 만들고, 각 행을 단일 owner task에 연결한다. | 일반 다중파일 작업의 Target Files 복제를 피하면서 누락 표면을 계획 시점에 노출한다 (`사용자 판단`) | 3 |
| 4 | 전파표 열은 `ID / Change element / Required surfaces / Discovery evidence / Owner task`로 두고, owner task의 Target Files·AC가 실행과 검증을 소유한다. | 전파 요소→실측 근거→실행 task의 추적 사슬을 한 행에서 눈검산할 수 있다 (`사용자 판단`) | 3 |
| 5 | 변형 표기 전수 제거가 필요할 때만 기존 census read-only verification task를 추가한다. | propagation 표와 census의 역할을 분리해 모든 전파 변경에 별도 검증 task가 생기는 것을 막는다 (`코드 확인`) | 3 |
| 6 | 모든 `implementation` 실행은 `_sdd/implementation/`의 단일 로컬 ledger를 생성한다. | 조건부 생성은 복잡도 과소평가 시 보호가 사라지고, 이 경로는 기존 process artifact 경계와 맞는다 (`사용자 판단`) | 4, 5 |
| 7 | task 상태는 `READY → RED_CONFIRMED → GREEN_CONFIRMED → DELTA_CLOSED` 네 단계만 사용한다. | 현재 implementation의 재개 판단에 필요한 최소 단계와 직접 대응한다 (`코드 확인`) | 4 |
| 8 | ledger에는 source, initial dirty paths, 전체 status, task별 triage·target files·contract correction count·RED/GREEN 명령과 판정 신호·target 밖 변경·coverage delta만 기록한다. 명령 출력 전문과 진행 서술은 금지한다. | resume pointer에 필요하지 않은 감사 정보를 제거해 반복 기록 비용을 억제한다 (`사용자 판단`) | 4 |
| 9 | 단계 성공 직후 상태를 갱신하고, ledger와 현재 diff가 모순되면 상태를 추정하지 않고 해당 테스트/check를 fresh 실행한다. 리뷰 fix는 마지막 `Review fix delta` 블록 하나로 기록한다. | stale ledger를 사실로 신뢰하는 새 실패 모드를 막는다 (`사용자 판단`) | 4 |
| 10 | 완료 기준은 구조 검증으로 한정하고 실제 3회 finding 관찰은 하지 않는다. 따라서 실제 Opus 5 오류 감소 효과는 주장하지 않는다. | 사용자가 빠른 구조적 정합 검증을 선택했다 (`사용자 판단`) | 6 |

### 기각한 대안

- **1~3을 한 feature로 구현**: 변경 원인과 검증 표면이 섞이고 ledger 도입이 draft 계약 변경을 불필요하게 막을 수 있어 기각.
- **reviewer 기준만 현 draft 수준으로 완화**: 실제로 가치 있는 중요 결정의 가정·대안 노출까지 잃으므로 기각.
- **모든 다중파일 변경에 propagation 표 적용**: 일반 Target Files의 중복 미러가 되어 형식 비용이 커지므로 기각.
- **draft 체크박스를 실행 ledger로 사용**: 계획 문서와 실행 상태가 섞이고 커밋 표면을 오염시키므로 기각.
- **복잡한 구현이나 다중 task에만 ledger 적용**: 복잡도 오판과 단일 task 다중파일 변경을 보호하지 못해 기각.
- **명령 출력·결정 이력을 포함한 감사형 ledger**: 재개에 불필요한 기록 비용이 task마다 누적되므로 기각.
- **구조 검증 후 실제 3회 finding 관찰**: 효과 판정에는 유리하지만 이번 적용 범위를 빠르게 닫기 위해 사용자가 기각.

## 미결 질문 (Open Questions)

인스코프 미결 질문 없음.

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | Feature A의 `feature-draft` 작성: 중요 결정 계약 정렬 + 조건부 propagation 표 | High | 후속 `feature-draft` 메인 루프 |
| 2 | Feature A를 plan-review 게이트 후 구현·implementation-review·spec-sync까지 수행 | High | 후속 SDD 체인 |
| 3 | Feature B의 `feature-draft` 작성: resume-only implementation ledger | High | Feature A 완료 후 메인 루프 |
| 4 | Feature B를 구현하고 네 상태 전이·fresh recovery·최소 필드 계약을 구조 검증 | High | 후속 SDD 체인 |

### 후속 핸드오프 (Handoff)

- **목표**: 두 독립 feature로 producer-review 요구 비대칭과 implementation 상태 유실 통로를 닫는다. Feature A 완료 시 중요 결정 조건과 reviewer 판정 조건이 동일하고, 조건을 만족하는 전파 변경이 surface→owner task→AC로 추적돼야 한다. Feature B 완료 시 모든 implementation 실행이 네 상태 ledger로 재개 가능해야 한다.
- **변경 금지 제약**: reviewer의 기존 6-smell 범위, implementation RED→GREEN·coverage delta 의미론, 단일 패스+fix 1회, 리뷰 finding dedup·재리뷰 정책, 실제 효과 관찰 계약은 바꾸지 않는다. Feature A와 B를 한 draft로 합치지 않는다.
- **검증**: Claude↔Codex 미러 diff, producer/reviewer 조건 리터럴의 양방향 구조 검사, propagation 조건의 positive/negative fixture와 owner-task 연접 검사, ledger 4상태 전이 및 stale ledger↔diff 모순 시 fresh verification을 요구하는 변이 검사, `git diff --check`.
- **중단 조건**: 중요 결정의 조건을 reviewer와 producer에서 동일하게 표현할 수 없거나, propagation 표가 일반 Target Files를 중복하는 형태로 커지거나, ledger가 명령 출력 전문·서술형 일지로 팽창하면 구현을 중단하고 draft를 재설계한다.

## 리서치 결과 요약 (Research Findings)

- producer의 Open Questions 계약과 reviewer의 Decision and Assumption 계약 사이에 실제 필드 비대칭이 있다.
- reviewer는 producer보다 인접 표면을 넓게 탐색하므로 propagation 누락이 리뷰 단계에서 뒤늦게 드러나는 구조다.
- 현재 implementation에는 task 상태를 compact 이후 복원할 별도 artifact가 없다.
- `_sdd/implementation/`은 소비 repo에서 로컬 process artifact로 취급되는 기존 canonical 경계다.

## 토론 흐름 (Discussion Flow)

Round 1: 적용 순서 → Feature A(1·2)와 Feature B(3)의 2단계 분리 채택.

Round 2: producer-review 계약 정렬 → 결과 방향을 바꾸는 중요 결정만 기록.

Round 3: propagation 형식 → draft 전역 표와 owner task 연결 채택.

Round 4: ledger 저장 위치 → `_sdd/implementation/` 로컬 단일 파일 채택.

Round 5: ledger 적용 범위 → 모든 implementation 실행에 강제.

Round 6: 효과 판정 → 구조 검증만 수행, 3회 관찰 기각.

Round 7: 추가 논의 선택 → 형식 세부화를 계속하기로 함.

Round 8: 상세 주제 선택 → ledger 필드를 먼저 구체화.

Round 9: ledger 밀도 → resume-only 최소 schema 채택.

Round 10: propagation 조건 → 동일 요소의 둘 이상 동기화 표면일 때만 표 생성.

Round 11: 미결 0건 확인 → 토론 종료 및 handoff 저장.

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 1~3번의 적용 단위를 어떻게 잡을까?
**Options**: 두 단계 분리 / 한 번에 적용 / 정리·종료
**A**: 두 단계 분리.
**Follow-up**: 1·2는 draft 계약, 3은 실행 상태라 독립 feature로 분리.

### Round 2
**Q**: producer↔reviewer 계약을 어느 방향으로 맞출까?
**Options**: 중요 결정만 기록 / 리뷰 기준 완화 / 정리·종료
**A**: 중요 결정만 기록.
**Follow-up**: 사소한 결정의 형식 노동을 막는 조건부 계약으로 한정.

### Round 3
**Q**: propagation surface를 어디에 기록할까?
**Options**: 전역 표+Task 연결 / Task별 직접 기재 / 정리·종료
**A**: 전역 표+Task 연결.
**Follow-up**: 중복을 줄이고 change element→owner task 연결을 눈검산하도록 설계.

### Round 4
**Q**: 최소 ledger를 어디에 둘까?
**Options**: 로컬 단일 파일 / draft 체크 갱신 / 정리·종료
**A**: 로컬 단일 파일.
**Follow-up**: `_sdd/implementation/` process artifact 경계를 사용.

### Round 5
**Q**: ledger 생성은 언제 강제할까?
**Options**: 모든 구현 / 다중 task만 / 정리·종료
**A**: 모든 구현.
**Follow-up**: 복잡도 오판으로 조건부 보호가 빠지는 위험을 제거.

### Round 6
**Q**: 적용 효과를 어느 수준까지 확인할까?
**Options**: 구조검증+3회 관찰 / 구조검증만 / 정리·종료
**A**: 구조검증만.
**Follow-up**: 실제 finding 감소 효과는 주장하지 않는 경계 확정.

### Round 7
**Q**: 현재 결정으로 토론을 정리할까?
**Options**: 정리·종료 / 추가 논의
**A**: 추가 논의.
**Follow-up**: ledger와 propagation 형식을 더 구체화.

### Round 8
**Q**: 어느 형식을 먼저 구체화할까?
**Options**: Ledger 필드 / 전파표 필드 / 정리·종료
**A**: Ledger 필드.
**Follow-up**: 반복 기록 비용이 있는 ledger를 우선 설계.

### Round 9
**Q**: resume-only 최소 schema를 채택할까?
**Options**: 최소 schema / 감사 정보 확대 / 정리·종료
**A**: 최소 schema.
**Follow-up**: 네 상태와 재개 포인터만 남기고 출력 전문을 제외.

### Round 10
**Q**: 조건부 propagation 표 계약을 채택할까?
**Options**: 조건부 표 / 모든 다중파일 / 정리·종료
**A**: 조건부 표.
**Follow-up**: 동일 변경 요소가 둘 이상의 동기화 표면에 전파될 때만 생성.

### Round 11
**Q**: 토론 요약과 후속 handoff를 저장할까?
**Options**: 정리·종료 / 추가 논의
**A**: 정리·종료.
**Follow-up**: in-scope 미결 없이 두 feature의 handoff를 확정.
