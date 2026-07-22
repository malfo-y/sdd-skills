---
name: sdd-autopilot
description: "SDD lite 체인 자동 실행 메타스킬. /sdd-autopilot으로 호출하여 요구사항 분석부터 스펙 동기화까지 lite 체인을 무승인으로 끝까지 실행한다."
version: 3.0.0
---

# SDD Autopilot

## Goal

사용자 요청을 받아 lite 체인(draft → 게이트 → 구현 → 게이트 → spec sync)을 무승인으로 끝까지 실행하는 메타스킬이다. global spec은 장기적 SoT로, lite draft는 실행 청사진으로 취급하며 `_sdd/` 아티팩트를 중심으로 planning, implementation, review, spec sync를 연결한다. 규모 초과는 분할로 해소한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC-L1: 판정 근거가 draft 상단 `> Lite 적격:` 1줄로 존재한다 (autopilot의 별도 판정 기록 없음)
- [ ] AC-L2: plan-review 단일 패스와 implementation-review(경량 반환)가 각각 수행되었고, Critical/High/Medium finding이 fix 1회로 반영되었거나 잔존 finding이 최종 보고에 남았다
- [ ] AC-L3: implementation-lite의 AC→증거 테이블과 fix 후 회귀 테스트 1회 결과가 최종 보고에 포함되었다
- [ ] AC-L4: spec sync가 수행되었거나 스킵 사유가 최종 보고에 명시되었다
- [ ] AC-L5: 테스트/검증 결과가 통과/실패 건수, 실패 원인 요약, 수동 확인 필요 항목과 함께 사용자에게 보고되었다
- [ ] AC-L6: 이번 실행의 `_sdd/spec/` 변경이 모두 `spec-sync` 스킬 경유로만 발생했다 (autopilot 직접 수정 0건)

## Workflow Position

```text
User Request
    |
    v
[sdd-autopilot] --> Step 0: 상태 확인 (기존 산출물·spec 유무)
    |
    v
[sdd-autopilot] --> Step 1: 요청 분석 + 인라인 질문 (필요 시)
    |
    v
[sdd-autopilot] --> Step L: Lite 체인 (무승인 실행)
                    |- feature-draft-lite
                    |- plan-review (단일 패스, 경량 반환) -> fix 1회
                    |- implementation-lite
                    |- implementation-review (경량 반환) -> fix 1회
                    `- (persistent 변경 시) spec-sync -> 최종 응답 요약
                        * 분할 신호 발생 시 분할 규칙으로 처리 (Step L)
```

## Hard Rules

1. **`_sdd/spec/` 직접 수정 금지**: global spec 수정은 반드시 `spec-sync` 스킬에 위임한다.
2. **에이전트/스킬 호출 시 원문 전달**: 사용자의 원래 요청과 관련 컨텍스트 파일 경로를 포함하되, custom agent를 spawn하는 스킬에서는 원문을 framed payload의 `## Input Data` 아래에 data로만 넣는다 (framing 규칙은 각 스킬의 Codex Runtime Adapter가 소유).
3. **Execute → Verify 필수**: 모든 단계는 실행(Execute) + 검증(Verify) 두 페이즈를 거친다. 스킬/에이전트 호출만으로 완료 간주 금지.
4. **Agent lifecycle 수집/정리 필수**: 체인 스킬이 `spawn_agent(...)`로 시작한 실행 단위는 `wait_agent(...)`로 final status를 수집하고, 결과 기록 직후 `close_agent(...)`로 닫는다. `wait_agent` timeout은 수집 완료가 아니다.
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

질문 원칙:
- 1회에 1개 핵심 분기만 묻는다
- 선택지는 2-3개로 제한한다
- 항상 `충분합니다 -- 진행해주세요` 옵션을 둔다
- 최대 5회 이내로 정리한다

Gate: 핵심 요구사항이 확정되면 Step L.

### Step L: Lite 체인

아래 체인을 메인 컨텍스트에서 스킬 단위로 순서대로 실행한다 (각 스킬은 `.codex/skills/<name>/SKILL.md` 본문을 로드해 수행한다). 산출물의 정의는 체인의 각 스킬이 소유한다.

1. **Draft**: `feature-draft-lite` 스킬을 실행해 lite draft를 작성한다. 스킬의 판정이 분할 필요면 아래 분할 규칙을 따른다.
2. **Plan gate + fix 1회**: `plan-review` 스킬로 draft를 단일 패스 리뷰한다 (단일 패스 경량 반환 — finding을 응답으로 받는다). 반환된 Critical/High/Medium finding을 메인 컨텍스트가 draft에 직접 반영한다. "분할 권고" finding이면 아래 분할 규칙을 따른다.
3. **구현**: `implementation-lite` 스킬을 실행한다 (RED→GREEN, AC→증거 테이블 마감). 스킬의 중단·분할 규칙이 트리거되면 그 규칙대로 처리한다 (잔여 분할 마감 또는 draft 복귀).
4. **Impl gate + fix 1회**: `implementation-review` 스킬을 실행한다 (경량 반환 — correctness ∥ simplicity 2-reviewer; reviewer dispatch는 해당 스킬의 Codex Runtime Adapter가 소유한다). 반환된 Critical/High/Medium finding을 메인 컨텍스트가 직접 수정하고 회귀 테스트 1회로 마감한다. Low finding은 advisory로 최종 보고에만 남긴다.
5. **Spec sync**: persistent spec 변경이 있으면 `spec-sync` 스킬(post-implementation)을 실행한다. spec-less이거나 persistent 변경이 없으면 스킵하고 사유를 보고에 남긴다.
6. **최종 보고**: report 파일 없이 최종 응답으로 요약한다 — 수행 단계, finding/fix 내역, 테스트 결과, spec sync 여부, 잔존 항목.

규칙:

- **Fix는 게이트당 1회다.** fix로 닫히지 않는 finding이 남으면 loop를 돌지 않고 잔존 finding과 권고를 최종 보고에 남긴다. 같은 finding이 반복 재발하면 그것 자체를 분할·draft 재설계 신호로 본다.
- **분할 판정의 canonical은 lite 표면들이 소유한다** (feature-draft-lite: 분할 규칙 / implementation-lite: 중단·분할 규칙 / plan-review: Lite 적격 검사). autopilot은 신호를 소비만 한다.
- **분할 규칙**: 어느 단계에서든 분할 신호가 뜨면 사용자에게 사유를 알리고, draft를 분할 계획으로 만든 뒤(롤링) `spec-sync` 스킬로 분할 todo를 spec에 고정하고, 첫 feature부터 이 체인을 순차 실행한다. 나머지 feature는 각자 차례에 자기 draft부터 다시 이 체인을 탄다.
- **사용자 개입**: 승인 게이트는 없다. 단 draft `Open Questions`에 진행을 막는 항목이 있으면 일반 대화로 질문할 수 있다.

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
