# 토론 요약: feature-draft 산출물 다이어트 — global 3섹션 vs per-task 병합

**날짜**: 2026-07-14
**라운드 수**: 6
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)

- **사용자 문제 제기**: feature-draft 산출물에서 `Contract/Invariant Delta and Coverage`, `Touchpoints`, `Validation Plan`을 굳이 global(top-level) 섹션으로 써야 하는지 의문 — `Task Details`에 per-task로 붙여 쓰면 되지 않나. 비판적 검토 요청.
- **토론을 시작한 배경**: 같은 날 오전 agent 지시문의 방어적 사족 제거(4겹 재진술 → 단일 홈) 작업의 연장선. 다음 다이어트 표적으로 산출물 구조 자체를 검토. 동기는 **작성 비용**(SDD 파이프라인 병목은 작성(추론) — 출력 다이어트가 채택 레버)과 **읽기 동선**(task를 읽다가 C#/V# ID를 표로 점프하는 간접참조).
- **현재 상태**: exemplar = `_sdd/drafts/2026-07-09_feature_draft_task_ordering_late_binding.md` (T1~T7, C1~C7+I1~I5, V1~V8). 세 섹션의 기계 소비자 4곳 확인 — spec-sync(Input Sources #3가 coverage 섹션을 이름으로 읽음), implementation SKILL(dispatch 시 global 표를 task별 슬라이스해 leaf에 전달), plan-review(Verification Weakness rubric이 표 기준 감사), task-ordering(Target Files+contract 생산·소비 관계).
- **범위와 제외 범위**: 다룬 것 — 세 섹션의 거처 설계와 그 근거. 미룬 것 — 실제 전파 census(어느 파일의 어느 문구를 고칠지)는 후속 feature-draft 몫.
- **수집한 근거**: exemplar draft 전문, `.claude/skills/implementation/SKILL.md`(dispatch 템플릿 {validation_plan}/{contract_invariant_delta}), spec-sync·plan-review·task-ordering agent 계약(같은 날 오전 작업으로 컨텍스트 확보).

## 핵심 논점 (Key Discussion Points)

1. **실측: 1:1이 지배적**: V1~V7이 T1~T7과 정확히 1:1 (cross-cutting은 V8 하나). Coverage 12행 중 7행이 task 1:1, multi-task는 I2(T3,T4)·I4(T1~T7)뿐. 사용자 직관에 실측 근거 있음.
2. **이중 저장과 재진술이 진짜 비만**: 관계가 양방향 저장됨(표의 Covered By/Validated By ↔ task Technical Notes의 "Covers.../validated by..."). global 섹션이 있는데도 T5 Description이 Touchpoints census를 재열거, V5 셀이 T5 AC를 재진술. 병합 자체는 내용을 이동시킬 뿐 — 절감은 ID 배관과 재진술 삭제에서 나옴.
3. **Coverage 표의 감사 기능**: coverage 표는 유일하게 "빠진 delta"가 보이는 자리 — per-task로 흩어지면 task를 못 받은 delta는 어디에도 존재하지 않아 plan-review가 scope hole을 잡을 수 없음(반증 불가능). 전면 병합의 최대 비용.
4. **계약의 홈과 test-author 앵커**: 계약 정밀 서술이 Description 프로스에 녹으면 test-author의 "계약 발명 금지" 앵커가 흐려짐 (Description=의도의 홈이지 계약 스펙의 홈이 아님 — 단일 홈 배치 규칙과 충돌).
5. **Touchpoints의 이중 성격**: 공유/전역 census(rename류 — 이 repo의 알려진 실패 클래스)와 line-number 격리 기능은 global이 필요하지만, exemplar의 16줄 중 공유 census는 1~2개뿐이고 나머지는 task-국소.
6. **cross-cutting 검증의 두 종류**: 분해형 invariant(I2 — 각 task가 자기 슬라이스 검증으로 자연 해소)와 sweep형 검증(V8 parity census — 전 task 완료 후 1회 전역 실행)은 거처 문제가 다름.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| D1 | **방향 B 채택**: 상세의 단일 홈을 task로 이동, global은 thin index만 | V1~V7 1:1 실측 + 작성/동선 동기 정합 + coverage 감사 보존 (`코드 확인` + `사용자 판단`) | 1, 2, 3 |
| D2 | task에 **`Contracts` 필드 신설** — 이 task가 구현/보존하는 C/I의 계약 정밀 서술의 단일 홈. Description은 의도만 | test-author "발명 금지" 앵커 보존, dispatch 슬라이싱=task 블록 그대로 (`코드 확인` + `사용자 판단`) | 4 |
| D3 | **Validation Plan 글로벌 표 삭제** → 각 task의 AC 바로 아래 `Validation` 블록(등급/판정조건/증거형태). AC↔V 1:1 대응이 local에서 가시화 | V1~V7 1:1 실측, V셀의 AC 재진술 삭제 가능 (`코드 확인` + `사용자 판단`) | 1, 2 |
| D4 | **Coverage 표 → thin index**: ID + 1줄 요약 + Covered By만 (Change 셀 프로스 금지). task Technical Notes의 "Covers.../validated by..." 역방향 기록 삭제 (index가 관계의 단방향 소유) | 감사 기능(빠진 delta 가시성)과 spec-sync 입력 계약 유지 + 이중 저장 제거 (`사용자 판단`) | 2, 3 |
| D5 | **Touchpoints 역할 축소**: 두 개 이상 task가 참조하는 공유 census·전역 변형형 census만 global에. task-국소 탐색 근거는 해당 task의 Target Files `-- 사유` 주석/Contracts로. line-number는 여전히 Touchpoints에만 허용 | B 철학 일관 적용 + census 완전성 감사·line-number 격리 보존 (`사용자 판단`) | 5 |
| D6 | **cross-cutting 처리 이원화**: 분해형 invariant는 각 task Validation이 자기 슬라이스 커버(index 행이 coverers 나열). sweep형 검증(parity census류)은 **마지막 Type: Test 검증 task로 승격** — invariant 계약 실체는 그 task의 Contracts가 소유, `Target Files: 없음 (read-only 검증)` 허용 1줄 추가 | 기존 기계(task-ordering dependency 배치·RED 게이트 structural check) 재사용, 신규 소비 계약 불필요, index 순수성 유지 (`사용자 판단`) | 6 |

### 기각한 대안

- **A 전면 병합** (세 섹션 삭제, task가 전부 소유): coverage 감사 소실(빠진 delta 반증 불가) + cross-cutting 중복 재유입 + 소비자 계약 대형 전파(8~12파일).
- **C 구조 유지 + 셀 다이어트**: 전파 최소지만 읽기 동선(ID 간접참조) 미개선 — 동기 절반 미충족.
- **계약을 Description이 흡수**: 단일 홈 배치 규칙(Description=의도)과 충돌, test-author 발명 금지 앵커 약화.
- **계약 실체를 index 표에 유지**: 동선 개선이 절반으로 줄어듦 (부분 B).
- **Touchpoints 전면 task 병합**: census 완전성 감사 자리 소실 + line-number가 task 본문(dispatch 입력)으로 전파.
- **sweep V를 index에 실체 유지**: index 순수성 예외 + implementation SKILL에 "최종 Checkpoint에서 cross-cutting V 실행" 신규 소비 계약 필요.
- **sweep V 하이브리드(건수 조건부)**: 규칙 복잡도 증가.

## 미결 질문 (Open Questions)

| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| 1 | thin index만으로 plan-review의 coverage 감사(Verification Weakness rubric)가 현행과 동등하게 동작하는가 — rubric 문구 갱신 후 실측 필요 | deferred-deliberately | 후속 구현의 검증 단계에서 확인 (미검증 가정: "index의 ID+Covered By만으로 orphan delta 감사 충분") |
| 2 | 전파 census 전모 — feature-draft-agent 짝 외에 implementation SKILL dispatch 템플릿·spec-sync Input Sources #3·plan-review rubric·spec definition 문서 중 정확히 어느 문구가 바뀌는지 | deferred-deliberately | 후속 feature-draft의 Touchpoints census 몫 |

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | 이 결정(D1~D6)을 feature-draft로 태워 spec delta + task-set 생성 | High | 사용자 트리거 |
| 2 | 후속 draft에서 소비자 4곳(implementation dispatch·spec-sync·plan-review·task-ordering) 계약 변경 census | High | feature-draft |
| 3 | 구현 후 Open Q1(감사 동등성) 실측 확인 | Medium | implementation-review |

### 후속 핸드오프 (Handoff)

- **목표**: feature-draft Part 2 산출 구조를 D1~D6대로 재편 — global `Validation Plan` 삭제, `Contract/Invariant Delta and Coverage` thin index화, task 템플릿에 `Contracts`·`Validation` 필드 추가, Technical Notes 역방향 기록 제거, Touchpoints 공유 census 전용화, sweep 검증 task 승격 + `Target Files: 없음` 허용. claude·codex 미러 짝 동시 반영.
- **변경 금지 제약**: AC 작성 위계(목표→AC→평가방법, falsifiable, 1:1 대응)의 rubric 사슬 자체는 불가침 — 거처만 이동. Part 1 계약(마커·3섹션)과 spec-sync가 읽는 섹션의 **가독 가능한 delta ID 집합**은 보존. line-number 허용 구역은 Touchpoints 밖으로 확대 금지.
- **검증**: 새 구조로 실제 draft 1건 생성(도그푸딩) 후 — (a) plan-review가 orphan delta를 여전히 잡는지(의도적 결손 주입 테스트), (b) implementation dispatch가 task 블록 슬라이스로 동작하는지, (c) 단어 수가 exemplar 대비 감소하는지.
- **중단 조건**: thin index로 orphan delta 감사가 불가능하다고 판명되면(Open Q1 부정) 중단하고 index 스키마 재논의. 소비자 계약 변경이 8~12파일을 넘어 확산되면 보고.

## 리서치 결과 요약 (Research Findings)

- **소비자 계약 4곳** (코드 확인): spec-sync Input Sources #3(섹션명 직접 참조), implementation SKILL dispatch 템플릿({validation_plan}/{contract_invariant_delta} 슬라이스), plan-review Verification Weakness rubric, task-ordering Rule 1.
- **exemplar 실측**: V1~V7↔T1~T7 1:1 (cross-cutting V8 1개), coverage 12행 중 1:1 7행, 관계 양방향 이중 저장, T5 Description의 census 재열거·V5의 AC 재진술 (global 섹션 존재가 재진술을 막지 못함 — 병의 원인은 구조+규율 양쪽).

## 토론 흐름 (Discussion Flow)

Round 1: 동기 규명 → 작성 비용 + 읽기 동선 (중복 자체·구조 의문은 아님)
Round 2: 대안 3안(A 전면 병합/B 상세→task+thin index/C 구조 유지+셀 다이어트) → B 채택
Round 3: 비판적 검증 — test-author 계약 앵커 문제 → task `Contracts` 필드 신설로 해소
Round 4: Touchpoints 판정 → 공유 census 전용으로 역할 축소
Round 5: 종료 확인 → cross-cutting V 거처 추가 논의 선택
Round 6: sweep형/분해형 이원화 → sweep은 마지막 검증 task 승격

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 세 global 섹션이 거슬리는 지점은? (중복 자체 / 읽기 동선 / 작성 비용 / 구조적 의문, 복수 선택)
**A**: 작성 비용, 읽기 동선
**Follow-up**: 병합은 내용을 이동시킬 뿐 — 절감은 ID 배관+재진술 삭제에서 나옴을 프레이밍. "무엇을 지우나"가 설계 변수.

### Round 2
**Q**: 설계 방향 — B(상세→task, global=index) / A(전면 병합) / C(구조 유지+셀 다이어트)?
**Options**: 프리뷰 포함 3안, B 권장
**A**: B 채택
**Follow-up**: A의 치명 결함(coverage 감사 소실)과 C의 한계(동선 미개선)로 B 권장 근거 제시.

### Round 3
**Q**: (비판적 개입) B에서 C/I 계약 정밀 서술의 거처 — test-author "발명 금지" 앵커가 Description 프로스화로 약해지는 문제
**Options**: task Contracts 필드 신설(권장) / index 표 유지 / Description 흡수
**A**: Contracts 필드 신설
**Follow-up**: Description=의도, Contracts=계약, index=ID+1줄 — 각 정보 정확히 한 곳.

### Round 4
**Q**: Touchpoints — 역할 축소(공유 census만 global, 권장) / global 유지 / 전면 병합?
**A**: 역할 축소
**Follow-up**: line-number 격리 유지, task-국소 근거는 Target Files 주석으로.

### Round 5
**Q**: 정리할까요, 더 논의? (정리 / cross-cutting V 거처 / 전파 범위)
**A**: cross-cutting V 거처 한 라운드 더

### Round 6
**Q**: sweep형 cross-cutting 검증 거처 — 마지막 검증 task 승격(권장) / index 실체 유지 / 건수 조건부 하이브리드?
**A**: 마지막 검증 task 승격
**Follow-up**: 분해형/sweep형 이원화 확정. 기존 기계(ordering·RED 게이트 structural check) 재사용이 결정적 근거.
