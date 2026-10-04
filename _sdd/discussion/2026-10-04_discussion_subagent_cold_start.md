# 토론 요약: subagent cold start 지연을 어떻게 잡을까 (coordinator-executor 적용 전제)

**날짜**: 2026-10-04
**상태**: 정상 종료
**검증 결과**: 합의 범위였던 "cold start를 어떻게 잡나"는 실측 4가지 방식 비교로 답했다. 단계별 적용 정책과 레시피 출처는 사용자가 정리를 택해 미결로 남겼다. 모든 실측은 방식당 1회이며, fork 방식은 측정 목적을 아는 상태였다.

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)
- **사용자 문제 제기와 배경**: sdd_skills 하네스에 multi-agent(coordinator-executor) 구조를 적용하려 한다. 과거처럼 agent가 cold start에서 시간을 너무 오래 쓰는 문제를 먼저 잡고 싶다.
- **현재 상태**: custom agent 0종, 단계 대부분이 메인 루프 직접 실행이다. 과거 full 레인(30줄 변경에 17분·300k), spec-sync agent(digest + 재독 순손실), plan-review agent(digest 신뢰 규칙 무시, 재독 7분+)가 모두 "메인 루프가 이미 가진 맥락을 다시 파악"하는 비용으로 폐지됐다.
- **범위와 제외 범위**: executor에게 맡길 일은 SDD 거의 전 단계(계획·구현·리뷰·spec-sync)다(사용자 지정). 동기는 메인 맥락 보호와 병렬 벽시계 단축이며, 독립 시선은 동기가 아니다(사용자 지정). 이미 기각된 레버(모델 강등, 도구 호출 배칭, digest 신뢰 규칙)는 다시 다루지 않았다.
- **수집한 근거**:
  - 고정 기동 비용(이 세션 subagent transcript): Explore 2초/첫 턴 18k, claude-code-guide 4초/28k, general-purpose 4초/35k. 일반 subagent는 첫 턴 cache read 0으로 부모 cache를 쓰지 않는다.
  - fork probe: 응답 1.1초, 첫 턴 cache read 98.5k / 새로 쓰기 0.55k. fork는 부모 cache를 재사용한다.
  - Claude Code 문서(code.claude.com/docs/en/sub-agents): 중첩 기본 3층(v2.1.219+), `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, fork는 fork를 띄울 수 없다.
  - Codex: `spawn_agent`에 `fork_turns` 인자가 있고, 현 스킬은 `fork_turns: "none"`(cold)으로 spawn한다(`plugins/sdd-skills-codex/skills/implementation-review/SKILL.md:33` 등). codex-cli 0.160.0, `multi_agent` stable.
  - 이 셸의 `diff`는 래퍼 함수다(`type diff`로 확인).
  - 실측 실험: PR #87(commit `a28b639`, AC 9개) 구현 리뷰를 detached worktree에서 같은 지시문으로 수행했다. 모든 방식이 9/9 MET 판정을 냈다. 모델은 모두 opus 계열이다.

| 방식 | 벽시계 | 처음 읽기 | AC 검사 완료 시점 | AC 밖 작업 | 최종 반환 | coordinator 노트 비용 | AC 밖 결함 발견 |
|---|---|---|---|---|---|---|---|
| ① fork | 29초 | 0초 | 약 24초 (스크립트 1개, 짜는 데 16초) | 0 | 약 6초 | 0 | 0 |
| ② 새 agent + 노트 v1 (위치표·결정) | 67초 | 약 10초 | 약 63초 (`diff` 래퍼 함정에 약 20초) | 0 | 약 7초 | 9초 / 1.0k | 0 |
| ②' 새 agent + 노트 v2 (레시피·환경 함정·결정) | 56초 | 약 4초 | **약 13초** (레시피 1회 실행) | 약 26초 (diff 내용, spec 훑기) | 약 17초 / 1.8k | 12초 / 1.5k | 0 (spec을 보고도 놓침) |
| ③ 새 agent 단독 | 68초 | 약 10초 | 약 37초 | 약 30초 (spec 탐색) | 약 13초 | 0 | Medium 2, Low 1 |

## 핵심 논점 (Key Discussion Points)
1. **cold start의 실체**: 기동 비용(2~4초)은 작다. 비싼 것은 다시 읽기도 아니다(노트·draft 읽기 약 10초). 실제 비용은 "일하는 방법을 다시 알아내는 턴"이다. 새 agent는 확인 → 결과 보기 → 다음 검사로 한 턴씩 나아가며, 턴마다 4~12초가 든다.
2. **fork**: 다시 파악할 것이 없어 cold start가 0이다(29초, 새 agent 대비 2.3배). 대신 coordinator 맥락의 틀에 묶여 AC 밖을 보지 않았다. coordinator가 무거우면 모든 fork가 그 크기를 물려받는다.
3. **digest(인계 노트, 사용자 제안)**: v1은 "무엇을 어디서 읽을지"를 담아 이미 싼 비용만 겨냥했고, 속도 효과가 없었다(67초 대 68초). v2는 "다시 알아내기 비싼 것"(검증 레시피·환경 함정·구현 중 결정)을 담아 AC 검사를 13초에 끝냈다. 이미 짜인 레시피를 받았기 때문에 fork보다도 빨랐다.
4. **cold start 다음 병목**: v2에서도 벽시계는 56초였다. 남은 시간은 agent가 스스로 고른 AC 밖 검토(약 26초)와 긴 반환(약 17초)이다. 이것은 지시문(검토 범위, 반환 길이)이 정하는 별도 레버다.
5. **새 시선의 값**: AC 밖 결함은 ③만 찾았다. 실제 결함으로 확인했다(`_sdd/spec/main.md:76`·`:82`의 stale "ledger MET 접기" 참조, 오늘 HEAD에도 남아 있음). 당시 게이트·fork·노트 받은 agent는 모두 놓쳤다. ②'는 spec을 보고도 놓쳤으므로 탐색 결과는 표본 1회로 판단할 수 없다.
6. **digest는 fork와 cold 사이의 다이얼이다**: 노트가 완전할수록 agent는 fork처럼 빠르지만 틀에 묶인다.
7. **(정리 후 이어진 논의) Codex fork와 업데이트형 digest**: Codex에도 전체 맥락 fork가 있다(`fork_turns` 생략 또는 `"all"`, 바이너리 도구 설명으로 확인. cache 재사용은 미검증). 그래도 사용자는 digest를 전 단계에 쓰기로 했다. 사용자 제안인 "단계마다 새로 쓰지 않고 업데이트하는 digest"에 대해 조건 4개를 제안했다(미확정): 현재 상태만 유지, coordinator 단일 작성자, 리뷰어에게는 방법만 주고 통과 주장은 제외(`main.md:89` fresh verification), draft 내용 복사 금지. ledger와의 관계를 묻는 중에 사용자가 하네스 전면 재편으로 방향을 넓혀, 이 질문은 재편 논의로 넘어갔다.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| 1 | executor 적용 대상은 SDD 거의 전 단계(계획·구현·리뷰·spec-sync)다 | 사용자 지정 (사용자 판단) | 배경 |
| 2 | 적용 동기는 메인 맥락 보호와 병렬 벽시계 단축이다. 독립 시선은 동기가 아니다 | 사용자 선택 (사용자 판단) | 2, 5 |
| 3 | 방식을 정하기 전에 실측부터 한다 | 사용자 선택 (사용자 판단) | 3 |
| 4 | cold start는 "기동"이나 "다시 읽기"가 아니라 "방법을 다시 알아내는 턴"으로 다룬다 | 4가지 방식 실측 (코드 확인, 표본 1회) | 1 |
| 5 | digest 설계 원칙: 다시 알아내기 비싼 것(검증 레시피와 기대값·기준선, 환경 함정, 채팅에서만 나온 결정, 짧은 변경 hunk)을 담고, 다시 읽기 싼 것(위치표, 파일 내용 사본)은 뺀다 | v1·v2 비교 실측 (코드 확인, 표본 1회). 채팅 전용 결정 항목은 이번 과제에 없어 효과 미측정 (미검증 가정) | 3 |
| 6 | 계획·실행·리뷰 전 단계에 digest 방식을 쓰고, digest는 단계마다 새로 쓰지 않고 업데이트한다 | 사용자 지정 (사용자 판단). Codex에도 fork가 있다는 정정 후에도 유지 | 7 |
| 7 | 하네스를 SDD 철학만 남기고 오케스트레이터 기반 multi-agent로 전면 재편하는 방향을 검토한다 | 사용자 지정 (사용자 판단). 재편 설계는 별도 토론에서 다룬다 | 7 |

### 기각한 대안
- 노트 v1 형태(위치표 + 결정, 레시피 없음): 같은 조건에서 노트 없는 새 agent와 속도가 같았다(67초 대 68초). 이미 싼 읽기 비용만 겨냥했다.

## 미결 질문 (Open Questions)
| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| Q1 | 단계별로 어떤 방식을 쓸까? 후보: 실행 단계(구현 task, spec-sync 작성)는 fork, 검증 단계(리뷰)는 레시피 digest + 새 agent | deferred-deliberately (auto-labeled, please review) | 사용자가 이 논의 대신 정리를 택했다. Q3·Q4·Q6 결과가 판단에 영향을 준다 |
| Q2 | 레시피 출처를 구현 단계 부산물(implementation ledger의 AC→증거 테이블 등)로 할까? 업데이트형 digest와 ledger의 관계는? | blocked-by:하네스 재편 토론 | 현 spec(`components.md` implementation 행)의 "reviewer는 ledger를 소비하지 않는다" 결정과 충돌하므로 그 결정의 재검토가 필요하다. 부산물로 남기면 노트 작성 비용(12초)이 거의 0이 된다 |
| Q3 | 표본을 늘려도 순위가 유지되나? | needs-data | 방식당 1회 측정이고, fork는 측정 목적을 알았다. 반복 측정이 필요하다 |
| Q4 | 채팅에서만 나온 맥락이 중요한 단계(spec-sync, 구현 task)에서도 digest가 효과가 있나? | needs-data | 이번 과제는 검사 명령이 draft에 다 있는 절차 중심 과제였다 |
| Q5 | Codex 전체 맥락 fork(`fork_turns` 생략 또는 `"all"`)도 부모 cache를 재사용하나? | needs-data | fork 존재는 바이너리 도구 설명으로 확인했다. cache 재사용과 속도는 미측정이다. 결정 6(digest 전면 사용)으로 우선순위는 낮아졌다 |
| Q6 | AC 밖 탐색을 어떻게 다룰까? (결함 발견 가치 vs 약 30초) | needs-data | ③만 실제 결함 2건을 찾았고 ②'는 spec을 보고도 놓쳤다 |
| Q7 | 검토 범위와 반환 길이를 어떻게 통제할까? | out-of-scope (auto-labeled, please review) | cold start를 없앤 뒤의 병목이다. 별도 레버로 다룬다 |
| Q8 | fork를 N개 병렬로 띄울 때 비용과 rate limit은 어떤가? | needs-data | fork마다 턴당 coordinator 맥락 전체를 cache로 읽는다 |

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | `_sdd/spec/main.md:76`·`:82`의 stale "ledger MET 접기" 참조를 현 이름("ledger 통과 증거 다이어트")과 맞춘다 | Medium | 미정 |
| 2 | 맥락 중심 단계(spec-sync 또는 구현 task)에서 fork / 레시피 digest / 새 agent를 반복 측정한다(Q3·Q4) | Medium | 미정 |
| 3 | Codex `fork_turns` 동작을 확인한다(Q5) | Medium | 미정 |
| 4 | Q1·Q2를 정하는 후속 discussion을 연다 | 미정 | 미정 |
