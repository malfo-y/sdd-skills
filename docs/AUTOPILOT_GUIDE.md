# SDD-Autopilot 사용 가이드

**버전**: 2.0.0
**날짜**: 2026-07-22

SDD 체인을 무승인으로 자동 실행하는 sdd-autopilot 메타스킬 가이드

---

## 1. 개요

**sdd-autopilot**은 기능 요청 하나를 받아 계획, 품질 게이트, 구현, 리뷰, 스펙 동기화까지 **체인**으로 끝까지 실행하는 메타스킬입니다. 별도의 실행 계획서나 승인 단계 없이, 요구사항이 확정되면 곧바로 실행됩니다. 사용자는 초반 요구사항 질문(필요 시)과 draft의 Open Questions에만 답하면 됩니다.

## 2. 체인

```
요청 분석
  → feature-draft      (기능 명세: task별 AC·Target Files, ~1분)
  → plan-review             (단일 패스 게이트, 경량 반환) → finding fix 1회
  → implementation     (메인 루프 직접 RED→GREEN 구현)
  → implementation-review   (correctness ∥ simplicity 2-reviewer, 경량 반환) → fix 1회
  → spec-sync               (persistent 변경이 있을 때만)
  → 최종 응답 요약           (리포트 파일 없음)
```

핵심 원칙:

- **무승인**: 승인 단계가 없습니다. 잘못된 방향은 draft 단계(~1분)에서 싸게 드러나고, plan-review 자동 게이트가 계획 품질을 검사합니다.
- **Fix는 게이트당 1회**: review-fix loop를 돌지 않습니다. 1회 fix로 안 닫히는 finding은 최종 보고에 남고, 반복 재발은 계획 재설계 신호로 취급됩니다.
- **경량 반환**: 리뷰 결과는 리포트 파일 없이 응답으로 돌아옵니다. 산출물은 draft 파일, 코드+테스트, 채팅의 AC→증거 테이블, 갱신된 spec뿐입니다.

## 3. 분할 (규모 초과 대응)

변경이 단일 컨텍스트로 감당되지 않으면 더 큰 파이프라인으로 올리는 대신 **여러 feature로 분할**합니다:

1. draft가 **롤링 분할 draft**가 됩니다 — Part 1 마커에 분할 feature 목록(전체 계획), Part 2에는 첫 feature의 task만.
2. `spec-sync`가 분할 목록을 **feature별 개별 planned todo**로 global spec에 고정합니다.
3. 첫 feature부터 체인을 순차 실행하고, 나머지 feature는 각자 차례에 자기 draft부터 체인을 다시 탑니다.

분할 판정 기준(coverage 눈검산 불가 / 단일 컨텍스트 초과)과 방법의 canonical은 `feature-draft` SKILL이 소유합니다. census형 sweep(rename/전파류)은 분할이 아니라 draft 마지막의 read-only 검증 task로 처리됩니다.

## 4. 사용법

```
/sdd-autopilot <기능 설명>
```

예:

```
/sdd-autopilot JWT 기반 인증 시스템을 구현해줘. 로그인, 로그아웃, 토큰 갱신 포함.
/sdd-autopilot 로그인 버튼 색상을 파란색에서 초록색으로 변경해줘.
```

**트리거 키워드**: `sdd-autopilot`, `autopilot`, `자동 구현`, `end-to-end 구현`, `자동으로 구현해줘`

### 사용자 역할

| 시점 | 사용자가 하는 것 |
|------|----------------|
| 요청 분석 | 부족한 정보에 대한 질문 답변 (1회 1분기, 최대 5회) |
| draft 직후 | Open Questions 중 확인 필요 항목 답변 (없으면 개입 없음) |
| 이후 | 없음 — 최종 보고까지 자율 실행 |

## 5. 산출물

| 산출물 | 위치 |
|--------|------|
| draft | `_sdd/drafts/<날짜>_feature_draft_<slug>.md` (spec-sync 후 `_processed_` 접두로 이동) |
| 코드 + 테스트 | 대상 파일 (draft의 Target Files) |
| AC→증거 테이블 | 최종 응답 (채팅) |
| spec 갱신 | `_sdd/spec/` (spec-sync 경유) |

## 6. FAQ

- **spec이 없는 repo에서도 되나요?** — 됩니다. spec-less mode로 진행하고, 구현 완료 후 `spec-create`를 추천받습니다.
- **예전 orchestrator 기반 full 파이프라인은?** — 제거되었습니다. 복구가 필요하면 git tag `full-lane-final`에 마지막 전체 구현이 보존되어 있습니다.

## 7. 관련 스킬

- `feature-draft` — 기능 명세 + 분할 규칙 canonical
- `plan-review` — draft 품질 게이트 (단일 패스, 경량 반환)
- `implementation` — 메인 루프 직접 RED→GREEN 구현 + 중단·분할 규칙 canonical
- `implementation-review` — correctness ∥ simplicity 2-reviewer (경량 반환)
- `spec-sync` — global spec 동기화 (planned/implemented 적응)
