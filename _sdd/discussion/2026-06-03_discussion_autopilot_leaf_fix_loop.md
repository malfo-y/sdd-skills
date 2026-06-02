# 토론 요약: H1 — autopilot review-fix 루프의 leaf 재구성

**날짜**: 2026-06-03
**라운드 수**: 3 (analysis 집중)
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)

- **사용자 문제 제기**: plan-review가 H1(High blocker)로 "T5(autopilot)가 미명세 — implementation-agent가 단일 task leaf로 바뀔 때 review-fix 루프의 fix 단계를 어떻게 leaf로 쪼갤지 [TBD]"를 지적. 이를 닫기 위한 미니 토론.
- **토론을 시작한 배경**: `_sdd/drafts/2026-06-03_feature_draft_implementation_orchestrator_leaf_split.md`의 T5가 미명세 상태라 구현 차단. 닫아야 할 3개 질문: (1) fix 분해 단위, (2) M1 orchestration 중복, (3) M2 report 소유.
- **현재 상태 (코드 확인)**:
  - orchestrator-contract L116: **agent_mapping `review=implementation-review`, `fix=implementation`, `re-review=implementation-review`** → fix는 별도 메커니즘이 아니라 "implementation 재호출".
  - review-fix gate는 group/phase 단위(`scope=per-group`, Checkpoint 경계)로 동작(L120-143).
  - autopilot은 **오케스트레이션 instruction 생성기**(메타스킬)이지 하드코딩 실행기가 아님 — orchestrator-contract 규칙에 따라 pipeline instruction을 생성.
  - `spec-update-done`(L68/L70)·`spec-summary`가 `_implementation_progress_`/`_implementation_report_`를 소비.
- **범위와 제외 범위**: H1(autopilot fix-루프 leaf 재구성)만. implementation skill/agent/planner 변경은 상위 draft 소관(여기선 결정 반영 지점만 언급).
- **수집한 근거**: orchestrator-contract.md L100-189(review-fix contract, agent_mapping, Checkpoint), 상위 draft·plan-review 리포트.

## 핵심 논점 (Key Discussion Points)

1. **fix = implementation 재호출**(agent_mapping): "fix를 어떻게 leaf로 쪼개나?"는 "implementation을 어떻게 leaf로 쪼개나?"와 동일 질문 → H1의 질문(1)이 무너짐. review finding → fix-task(영향 파일=Target Files) → 나머지 task와 동일 dispatch.
2. **autopilot = instruction 생성기**: H1은 복잡한 fan-out 코드가 아니라 **orchestrator-contract 문구 수정**으로 해소 → T5가 "코드 작업"에서 "계약 문구 수정"으로 내려가 저위험.
3. **M1 누그러짐**: autopilot은 원래부터 자기 orchestrator-contract를 가진 별도 오케스트레이터. 새 중복이 아니라 **dispatch granularity 변경**(per-phase agent → per-task leaf)일 뿐.
4. **2-group 공존**: A'(초기구현 병렬) 채택 시 "병렬 dispatch 그룹(phase 내부)"과 "Checkpoint 리뷰 그룹(phase 경계)"이 공존 → 중첩 관계로 용어 분리(기존 모델이 이미 암묵적으로 이 구조).
5. **report 소유**: leaf는 결과만 반환, 실행 주체(직접=skill, 파이프라인=autopilot)가 canonical 경로·필드 보존하여 작성.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | **fix = implementation 재호출**, 별도 fix 분해 기계장치 없음. review finding → fix-task → leaf dispatch | agent_mapping `fix=implementation`(L116) | 1 |
| 2 | **fix step**: review finding **하나씩 순차** leaf dispatch | finding 수 적고 상호작용 가능 → 순차 안전 | 1 |
| 3 | **초기 구현 step**: task를 **group 단위 병렬** leaf dispatch (trivial dep 규칙, A') | autopilot도 병렬 확보, instruction 생성기라 비용은 contract 문구(코드 중복 아님) | 3,4 |
| 4 | **2-group 중첩 분리**: 병렬 dispatch 그룹(phase 내부) vs Checkpoint 리뷰 그룹(phase 경계)을 다른 용어로 구분 | 기존 모델이 이미 이 중첩 구조, T5는 구분 문구만 추가 | 4 |
| 5 | **H1은 orchestrator-contract 문구 수정으로 해소** (autopilot=instruction 생성기) | T5를 코드 작업→계약 수정으로 저위험화 | 2,3 |
| 6 | **report/progress 소유**: leaf는 결과만 반환; 실행 주체(skill/autopilot)가 canonical 경로·소비 필드 보존하여 작성 | spec-update-done/spec-summary 소비 호환 | 5 |

## 미결 질문 (Open Questions)

없음 (in-scope 0건). H1의 3개 질문 전부 수렴.

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | 상위 draft T5를 위 결정으로 구체화(미명세 해소): fix=finding 순차 / 초기구현=group 병렬 / 2-group 구분 / report 소유 | High | feature-draft 갱신 |
| 2 | plan-review M1(중복=granularity 변경으로 재서술)·M2(경로 보존 AC)·M4(escape hatch)도 함께 draft 반영 | High | feature-draft 갱신 |
| 3 | orchestrator-contract: agent_mapping fix step을 "finding 단위 leaf 순차", 초기구현 "task group 병렬", 2-group 용어 구분, report 소유 명시 (T5 구현 시) | High | 구현 |
| 4 | plan-review M3(T2 의존성=T1만, T3/T4 enhancer) 반영 | Medium | feature-draft 갱신 |

## 리서치 결과 요약 (Research Findings)

- orchestrator-contract L116: `fix=implementation` → fix는 implementation 재호출. H1 질문(1) 단순화의 핵심 근거.
- review-fix gate는 group/phase 단위(L120-143), Checkpoint 경계. → "병렬 dispatch 그룹"과 별개의 "리뷰 그룹"이 이미 존재.
- autopilot은 instruction 생성 메타스킬 → H1이 계약 문구 수정 수준으로 내려감(T5 저위험화).
- spec-update-done L68/L70·spec-summary가 progress/report 소비 → 경로·포맷 보존 필수(M2).

## 토론 흐름 (Discussion Flow)

- Round 1 (context+analysis): orchestrator-contract 확인 → "fix=implementation 재호출" 발견으로 fix 분해 질문 단순화. autopilot 실행 방식 C(순차) vs A(병렬 inline) 제시.
- (사용자 clarify): "autopilot은 instruction 생성기 — fix loop에서 finding 하나씩 dispatch라고 쓰면 되나?" → 정확. H1을 계약 문구 수정 수준으로 재정의.
- Round 2: 초기구현 dispatch C'(전부 순차) vs A'(초기구현만 group 병렬) → **A'** 채택.
- Round 3 (critical): A'의 2-group 공존 위험 제기 → 중첩 분리로 해소. M2(report 소유) 확정 → 수렴.

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: autopilot이 implementation 단계(fix 포함)를 단일 task leaf로 어떻게 실행하나? (C 순차 / A 병렬 inline)
**A**: (사용자 clarify) autopilot은 instruction 생성 스킬 — "fix loop에서 review 지적사항 하나씩 dispatch"라고 쓰면 되는 것 아닌가?
**Follow-up**: 맞음. fix=implementation 재호출이라 별도 기계장치 불필요, H1은 orchestrator-contract 문구 수정. M1도 누그러짐(autopilot은 원래 별도 contract 소유).

### Round 2
**Q**: 초기 구현 step의 leaf dispatch 단위? (C' 전부 순차 / A' 초기구현만 group 병렬)
**A**: A' (초기구현만 group 병렬).
**Follow-up**: 비판 — A'는 "병렬 dispatch 그룹"과 "Checkpoint 리뷰 그룹" 2개를 공존시킴.

### Round 3
**Q**: 2-group 중첩 분리 + report 소유(실행 주체, 경로 보존) 확정하고 정리?
**A**: 정리해줘.
**Follow-up**: 2-group은 중첩 분리(기존 모델 구조), report는 실행 주체 소유·경로 보존으로 확정. H1 3개 질문 전부 닫힘.
