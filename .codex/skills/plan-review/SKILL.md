---
name: plan-review
description: Use this skill to review a feature draft before coding, identify overengineering and sloppy-code risks, and return a findings-first verdict. Triggered by "plan review", "review plan", "draft review", "계획 리뷰", "플랜 리뷰", "구현 계획 리뷰", or when the user wants to check a draft for requirement fit, overengineering, hidden decisions, and weak verification before implementation.
---

# Plan Review (직접 실행, Review-only)

이 스킬은 **메인 루프가 직접 수행**한다 — feature draft를 5-smell rubric으로 **단일 패스** 감사하고 결과를 채팅 반환 하나로 낸다. custom agent를 spawn하지 않고, 리포트 파일을 만들지 않으며, 대상 draft·코드를 수정하지 않는다 — finding 반영은 producer(draft 작성자) 소관이다. `--model`·`--effort` 류 인자가 오면 적용 대상(spawn되는 agent)이 없음을 1줄 안내하고 무시한다.

## Input

1. 사용자/호출자 지정 draft 경로
2. 지정이 없으면 `_sdd/drafts/*_feature_draft_*.md` 최신 파일

대상 draft가 없으면 검토를 만들어내지 않는다 — "리뷰 대상 없음 — `feature-draft`로 draft를 먼저 작성하라" 1줄만 반환한다.

## 읽기 지침

- 서로 독립인 파일 읽기·검색은 가능한 한 함께 배칭한다 — 앞 결과를 봐야 대상이 정해지는 호출만 다음 턴이다.
- 검색으로 좌표를 먼저 잡고 관련 구간만 선택적으로 읽는다 — 파일 전문 읽기는 판정에 전문이 필요할 때만.
- spec surface(`_sdd/spec/*`)는 draft가 **명시 인용한** 파일·섹션만 읽는다. 인용 없는 spec 대조는 수행하지 않는다 — 전 스펙 대비 어긋남 감시는 `spec-review` 소관이다. 기록물(`decision_log.md`·`logs/`·`prev/`)은 읽지 않는다.
- 근거가 부족하면 읽기를 확장하지 않고 그 smell의 finding을 만들지 않는다.

## Review Rubric: 5 Plan Smells

각 smell을 **각각 점검**한다 (finding 0이어도 점검은 수행).

- Requirement Fit
  - 사용자 요청·spec delta가 task와 AC로 빠짐없이 옮겨졌는가? 반대로 요청에서 직접 나오지 않는 기능이 들어가지는 않았는가?
  - 모든 변경이 요청으로 추적 가능한가?
- Task Boundary Drift
  - task가 하나의 명확한 목적을 넘는가?
  - task가 자기 AC만으로 완료 판정이 닫히는가?
- Hidden Decision
  - `Open Questions`가 있다면 항목별 결정과 확인 필요 여부가 적혔고, 확인 필요 항목이 구현 전 확인 대상으로 드러나는가?
  - 남은 숨은 가정이 있는가?
- Over-engineering
  - 같은 로직/상수/계약을 여러 task/file에 중복 구현하도록 계획했는가?
  - 작은 중복에 과한 추상화를 요구하거나, 한 곳에서만 쓰이는 helper, layer, config, interface를 만들도록 계획하는가?
  - `[C]` Target File이 기존 파일 수정으로 충분한데 새 파일로 분리됐거나 생성 이유가 없는가?
  - draft 자체가 같은 정보를 여러 섹션에 재서술하는가 — Description이 AC·Contracts를 산문으로 미러링하는가?
- Verification Weakness
  - 각 AC가 평가방법과 기대 evidence를 갖고 이진 판정으로 닫히는가? 그 evidence가 재현 가능한 출력 또는 content anchor(줄 번호가 아니라 파일·인용 문자열처럼 변경에 흔들리지 않는 앵커)로 적혔는가?
  - Target Files가 실측인가?

> producer 계약의 상세(AC 등급 구분·작성 형식 등)는 재검사하지 않는다 — rubric은 판정 축만 보유하고 상세는 `feature-draft`가 단독 소유한다.

## Severity

| Severity | Meaning |
|----------|---------|
| Critical | 계획대로 구현하면 핵심 요구사항을 잘못 구현하거나 명백한 보안/데이터 손실/호환성 위험을 만든다. |
| High | Target Files, task boundary, 검증이 잘못되어 구현 전에 계획 수정이 필요하다. 요청되지 않은 큰 추상화나 새 설정 체계도 포함될 수 있다. |
| Medium | 구현 품질을 떨어뜨릴 가능성이 큰 단일 사용처 추상화, 불필요한 새 파일, 애매한 AC 등. |
| Low | 표현, 문서화, minor cleanup 수준의 계획 개선 제안. |

**Blocker Policy**: Critical/High findings만 implementation blocker다. Medium/Low는 advisory다. `Recommended Plan Change`는 인용한 draft/code evidence를 해소하는 가장 작은 plan change여야 하며, 새 capability는 current requirement 또는 measured risk에 직접 추적될 때만 권고한다.

## 반환

채팅 반환 하나가 전부다:

- **Blocker Status**: BLOCKED(Critical/High 존재) | CLEAR
- **Findings** (severity별): Critical/High/Medium은 finding당 블록 — `[Smell] 제목` + Evidence·Affected Plan Surface·Recommended Plan Change·Implementation Blocker 여부. Low는 affected surface 포함 한 문장.

확인했으나 finding이 아닌 대조 결과(실재가 확인된 Target Files·content anchor, 반증되지 않은 사실 전제 등)는 열거하지 않는다 — 반환은 위 항목이 전부다. 줄이는 것은 출력이지 점검·대조 범위가 아니다.

## Error Handling

Target Files가 불명확하면 `Verification Weakness` 또는 `Task Boundary Drift` smell로 검토한다.

## Integration

- `feature-draft`: 리뷰 대상이자 호출 주체 — 자기 품질 게이트로 이 리뷰를 수행하고, finding 반영은 작성자 소관
- `implementation`: Critical/High blocker가 없을 때 후속 실행
