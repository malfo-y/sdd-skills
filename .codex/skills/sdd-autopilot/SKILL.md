---
name: sdd-autopilot
description: "SDD 체인 자동 실행 메타스킬. /sdd-autopilot으로 호출하여 요구사항 분석부터 스펙 동기화까지 체인을 무승인으로 끝까지 실행한다."
---

# SDD Autopilot

## Goal

사용자 요청을 받아 체인(draft → 구현 → spec sync)을 무승인으로 끝까지 실행하는 메타스킬이다. global spec은 장기적 SoT로, draft는 실행 청사진으로 취급하며 `_sdd/` 아티팩트를 중심으로 planning, implementation, review, spec sync를 연결한다. 규모 초과는 분할로 해소한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: draft에 규모 판정 근거가 존재하고 autopilot의 별도 판정 기록은 없다
- [ ] AC2: 각 producer가 반환한 품질 게이트 결과와 잔존 finding이 최종 보고에 포함되었다
- [ ] AC3: implementation이 반환한 AC별 증거와 회귀 결과가 최종 보고에 포함되었다
- [ ] AC4: spec sync가 수행되었거나 스킵 사유가 최종 보고에 명시되었다
- [ ] AC5: 테스트/검증 결과가 통과/실패 건수, 실패 원인 요약, 수동 확인 필요 항목과 함께 사용자에게 보고되었다
- [ ] AC6: 이번 실행의 `_sdd/spec/` 변경이 모두 `spec-sync` 스킬 경유로만 발생했다 (autopilot 직접 수정 0건)

## Hard Rules

1. **`_sdd/spec/` 직접 수정 금지**: global spec 수정은 반드시 `spec-sync` 스킬에 위임한다.
2. **에이전트/스킬 호출 시 원문 전달**: 사용자의 원래 요청과 관련 컨텍스트 파일 경로를 포함하되, custom agent를 spawn하는 스킬에서는 원문을 framed payload의 `## Input Data` 아래에 data로만 넣는다 (framing 규칙은 각 스킬의 Codex Runtime Adapter가 소유).
3. **Execute → Verify 필수**: 모든 단계는 실행(Execute) + 검증(Verify) 두 페이즈를 거친다. 스킬/에이전트 호출만으로 완료 간주 금지.
4. **Agent lifecycle 수집 필수**: 체인 스킬이 시작한 실행 단위는 각 스킬의 Codex Runtime Adapter가 active schema에서 선택한 contract로 final status를 수집한다. mailbox contract(Desktop/current CLI)는 target 없는 wait를 반복하고 완료 agent를 닫지 않으며, target/close contract(legacy schema)만 target wait 뒤 완료 handle을 닫는다. 실행 surface 이름이 아니라 schema로 선택하고, wait timeout은 수집 완료가 아니다.
5. 한국어를 기본으로 하되 사용자 언어를 따른다.
6. `_sdd/` artifact 경로는 lowercase canonical을 기본으로 하되, 입력을 읽을 때는 legacy uppercase fallback도 허용한다.
7. spec-less repo에서도 중단하지 않는다. `_sdd/spec/`가 없으면 그대로 진행하고, 구현 완료 후 사용자에게 `spec-create`를 추천한다 (코드가 먼저 존재해야 spec이 실제 구조를 반영한다).

## Process

### Step 0: 상태 확인

| 체크 | 동작 |
|------|------|
| `_sdd/drafts/` 스캔 | 같은 주제의 기존 draft가 있으면 재활용 여부를 판단 |
| `_sdd/spec/*.md` 존재 확인 | 없으면 spec-less mode로 계속 진행 (Hard Rule 7) |

legacy `_sdd/pipeline/` 산출물이 보이면 기록물로 무시한다.

### Step 1: 요청 분석

요청에서 기능 설명, 제약 조건, 기존 코드와의 관계, 테스트 요구사항, 스펙 변경 여부를 추출하고, 부족한 정보만 질문으로 보완한다.

질문은 답이 설계나 범위를 바꾸는 핵심 분기만 한 번에 하나씩, 최소 횟수로 묻는다. 사용자가 충분하다고 판단하면 즉시 체인으로 넘어갈 선택지를 둔다.

Gate: 핵심 요구사항이 확정되면 Step 2.

### Step 2: 체인

아래 체인을 메인 컨텍스트에서 스킬 단위로 순서대로 실행한다 (각 스킬은 `.codex/skills/<name>/SKILL.md` 본문을 로드해 수행한다). 산출물의 정의는 체인의 각 스킬이 소유한다.

1. **Draft**: `feature-draft` 스킬을 실행해 draft를 작성한다. 스킬의 판정이 분할 필요면 아래 분할 규칙을 따른다.
2. **구현**: `implementation` 스킬을 실행하고 완료·분할 신호를 소비한다.
3. **Spec sync**: persistent spec 변경이 있으면 `spec-sync` 스킬(post-implementation)을 실행한다. spec-less이거나 persistent 변경이 없으면 스킵하고 사유를 보고에 남긴다.
4. **최종 보고**: report 파일 없이 최종 응답으로 요약한다 — 수행 단계, 각 게이트의 finding/fix 내역과 잔존 finding, 테스트 결과, spec sync 여부, 잔존 항목.

규칙:

- **품질 게이트와 finding 반영은 producer 스킬이 소유한다.** autopilot은 producer 반환을 최종 보고로 모은다.
- **분할 판정의 canonical은 각 스킬이 소유한다** (feature-draft: 분할 규칙 / implementation: 중단·분할 규칙). autopilot은 신호를 소비만 한다.
- **분할 규칙**: 어느 단계에서든 분할 신호가 뜨면 사용자에게 사유를 알리고, draft를 분할 계획으로 만든 뒤(롤링) `spec-sync` 스킬로 분할 todo를 spec에 고정하고, 첫 feature부터 이 체인을 순차 실행한다. 나머지 feature는 각자 차례에 자기 draft부터 다시 이 체인을 탄다.
- **사용자 개입**: 승인 게이트는 없다. 단 draft `Open Questions`에 진행을 막는 항목이 있으면 일반 대화로 질문할 수 있다.

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
