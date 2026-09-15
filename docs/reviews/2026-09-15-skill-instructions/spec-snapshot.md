# spec-snapshot 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/spec-snapshot/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/spec-snapshot/SKILL.md)
- 판정 요약: 수정 필요 1 / 정리 후보 0 / 실행 검증 필요 0

## 역할과 유지할 계약

`_sdd/spec/`의 Markdown을 새 timestamp destination에 복사하거나 번역하며 provenance를 기록한다. source read-only, 기존 destination 보존, source pre/post path·SHA-256 manifest exact match를 완료 hard gate로 유지한다. `summary.md`의 reserved marker 충돌 시 생성 전에 종료하고, 원본 summary 유무에 따라 metadata 뒤의 body를 보존하거나 근거 기반 요약을 작성하는 분기도 유지한다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | **spec-snapshot-01**: 일반 snapshot 요청과 명시적 번역 요청이 목표 언어 생략 시 같은 복사 기본값을 쓴다. |
| 2. 충돌과 우선순위 | **spec-snapshot-01**: 번역 요청을 trigger로 받지만 목표 언어가 없으면 source 언어로 복사하도록 정한다. 나머지 same-language/translation 및 summary present/absent 분기는 명확하다. |
| 3. 확인·승인 경계 | 수정 필요 없음. 일반 snapshot에 불필요한 사전 승인을 요구하지 않는다. reserved marker 중단은 원본 body와 metadata 경계를 보호한다. 언어 확인이 필요한 좁은 입력은 01에서 다룬다. |
| 4. 중복과 소유권 | 수정 필요 없음. 별도 reference·helper 없이 공통 SKILL 본문이 파일 세트와 보존 interface를 소유한다. AC·작성·검증의 반복은 완료 조건과 수행·대조 역할이 구분된다. |
| 5. 완료·복구 조건 | 수정 필요 없음. manifest 변경은 완료 불가로 명시되고 destination 충돌은 numeric suffix로 해소한다. Final Check는 source 변경 실패를 완료로 전환하는 예외로 읽지 않는다. |
| 6. 절차의 필요성 | 수정 필요 없음. 5단계는 캡처·작성·metadata·대조·보고의 서로 다른 책임이다. bounded batch 크기는 context에 맡겨 불필요한 고정 수를 강제하지 않는다. |

## Findings

### spec-snapshot-01 — 명시적 번역 요청도 목표 언어가 없으면 복사로 처리한다 [수정 필요]

- **기준 / runtime**: 1, 2 / Claude·Codex 공통.
- **근거**: [Claude](../../../.claude/skills/spec-snapshot/SKILL.md) 3, 34, 45행; [Codex](../../../plugins/sdd-skills-codex/skills/spec-snapshot/SKILL.md) 3, 33, 44행.
- **정확한 원문**: description은 `"translate spec"`와 `"스펙 번역"`을 trigger로 받는다. Step 1은 “표시할 target language는 사용자 지정값을 우선하고, 없으면 source 언어를 사용한다.”, Step 2는 “target language가 source와 같으면 root `summary.md`를 제외한 파일을 byte-exact 복사한다.”라고 정한다.
- **문제 상황**: 한국어 spec에 사용자가 “스펙 번역해줘”라고 요청하고 기존 대화에도 목표 언어가 없다. 문면의 fallback을 따르면 한국어를 target으로 지정하고 same-language snapshot을 만든다. 목표 언어를 알아야 번역 요청을 이행할 수 있지만 해당 입력을 구별하는 분기가 없다.
- **예상 영향**: 파일 보존 AC는 통과해도 요청한 번역을 제공하지 않은 결과를 완료로 보고하는 경로가 생긴다. 이는 문면상 경로이며 실제 실행 재현을 주장하지 않는다.
- **최소 수정안**: Step 1 언어 선택을 “명시값 또는 기존 대화에서 확정한 목표 언어를 사용한다. 명시적 번역 요청인데 목표 언어를 확정할 수 없을 때만 한 번 묻는다. 그 외 snapshot/export 요청은 source 언어를 사용한다.”로 한정한다. 이미 확정된 언어는 다시 묻지 않는다.
- **유지할 계약**: 언어 미지정 일반 snapshot의 무질문 복사, 명시 target 우선, 원본 불변, unused destination, metadata 형식, source pre/post manifest hard gate. global spec의 보존 설계를 변경할 필요는 없다.
- **소유자**: `spec-snapshot` 양 runtime SKILL 본문. cross-skill 변경 없음.
- **검증 상태**: 양 본문 줄·원문 및 분기 정적 대조 완료. 스킬 실행·제안 적용 없음.

## 런타임 차이와 의존성

- Claude frontmatter의 `user_invocable: true` 한 줄만 Codex와 다르다. 본문은 동일하며 이 배포 차이는 finding이 아니다.
- 읽은 계약: [AGENTS.md](../../../AGENTS.md), [global spec](../../../_sdd/spec/main.md)의 Guardrails·document producer output interface(137행), [env](../../../_sdd/env.md), [공통 리뷰 기준](./review-criteria.md), 대상 SKILL 두 파일 전체.
- 대상 스킬에는 직접 참조 reference 파일이 없다. 오류 시 `spec-create`를 권장할 뿐 호출하거나 그 산출물을 재판정하지 않으므로 해당 스킬 내부는 이 리뷰에서 미검토했다.
- 별도 런타임 API·설치본·실제 snapshot 결과·번역 품질은 조사하지 않았다. 도구 지원 여부나 모델 행동 효과에 관한 결론은 내리지 않는다.

## 권장 처리 순서와 검증

1. 양 runtime의 Step 1 언어 선택 한 항목만 위 분기로 맞춘다. 기존 destination·source 규칙은 변경하지 않는다.
2. 후속 실행 검증에서 같은 fixture로 언어 없는 일반 snapshot은 그대로 복사하는지, 목표 언어가 이미 지정된 번역 요청은 재질문하지 않는지, 목표 언어가 전혀 없는 명시적 번역 요청만 질문하는지 확인한다.
3. 각 성공 실행에서 기존 Step 4 전체를 적용해 source manifest exact match 및 summary body/metadata 보존을 확인한다. 이번 리뷰에서는 스킬을 실행하지 않았고 보고서만 작성했다.
