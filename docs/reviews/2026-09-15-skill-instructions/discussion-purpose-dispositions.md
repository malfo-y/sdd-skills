# discussion 재설계 적용 내역

- 날짜 / 모델: 2026-09-15 KST / gpt-6-astra
- 입력: 사용자 승인한 [목적·경계·결과물 리뷰 DP-01~06](./discussion-purpose-review.md).
- 상태: 소스 반영·검증·implementation review 완료. 리뷰 계약 전달의 절차 제한은 아래 기록했다. 설치 캐시와 실제 모델 행동은 검증 대상에 포함하지 않았다.
- 범위: 양 runtime의 본문·question-guide·summary-template·sample session 8개 파일과 supporting spec·리뷰 기록.

## 적용 결과

| Finding | 적용 | 소유 위치 |
|---|---|---|
| DP-01 | 질문 가이드의 별도 페이즈·필수 설계 질문·리서치 생략 조건을 제거했다. 실행 판단은 본문이 소유하고 가이드는 예시만 제공한다. | 본문 `Discussion Guidance`, question-guide |
| DP-02 | coverage map과 페이즈 게이트를 없애고 결정·범위·다음 행동을 바꾸는 불확실성으로 질문을 고른다. | 본문 `질문과 범위` |
| DP-03 | 중요한 약점·가정·반례 검토는 유지하며 직접 조사와 사용자 판단 질문을 구분한다. 최소 질문·응답 횟수는 요구하지 않는다. | 본문 `근거와 대안` |
| DP-04 | 외부 데이터 대기면 필요한 근거와 다음 행동을 기록하고 정리를 제안한다. 사용자의 종료 요청 뒤에는 라벨·종료 승인을 다시 묻지 않는다. | 본문 `미결과 진행 판단`, `정리와 종료` |
| DP-05 | 여러 영역의 비교·공통 정책·우선순위 결정을 허용한다. 진행이 어려운 독립 논의만 분해를 제안한다. | 본문 `질문과 범위`, sample session |
| DP-06 | 핵심 결과와 근거는 보존하고 전체 대화 로그는 사용자 요청·확인된 감사 요구에 한정한다. 채팅에는 핵심과 링크를 기본으로 보고한다. | 본문 `Output Contract`, summary-template |

소스: [Claude](../../../.claude/skills/discussion/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/discussion/SKILL.md). 두 본문은 Runtime 절을 제외하면 동일하다. 질문 도구·옵션 수와 Claude의 선택적 read-only 조사 위임만 runtime 차이로 남긴다. 두 reference는 byte-identical이며 예시는 도구명만 다르다.

## 유지한 경계와 관련 정리

- 코드·스펙·설정 read-only, dated slug 요약 경로, work log 예외, 사용자 선택과 종료 의사, 사실·가정 구분, 미결 보존, template 실제 로드, 부분 저장과 Final Check를 유지했다.
- 근거 유형 4종과 미결 카테고리 4종의 의미는 template이 소유한다. 분류를 억지로 만들지 않도록 `미확인`을 허용하고, 확인받지 않은 추정은 표시한다. 한 결정에 복수 근거 유형이 있으면 각각 기록한다.
- 고정 조사 dispatch와 범위 확인 횟수는 판단 기준으로 전환했다. 질문 도구 사용 자체와 선택형 질문의 종료 옵션은 유지한다.
- 기존 `토론 흐름` 중복 섹션·라운드 수·참여 방식 메타데이터를 기본 요약에서 제거했다. 조사 결과는 초기 맥락의 근거·발견에 합쳤으며, 결정 변경 이유와 기각 사유는 보존한다.
- 우선순위를 임의로 지정하지 않도록 `미정`을 허용했다. 동명 파일은 같은 토론을 갱신하는 경우 외에는 구별되는 slug를 사용한다.
- supporting usage-guide의 기존 `최대 10라운드` 표기를 소스와 맞췄다. global spec의 새 invariant나 별도 mode·설정은 만들지 않았다. 이전 리뷰·decision log entry는 보존한다.

## 시나리오별 소스 계약 검토

아래는 현재 문면에 대한 정적 판독이다. 실제 모델에 스킬을 실행한 transcript나 A/B 실험 결과가 아니다.

| 입력 상황 | 현재 계약이 요구하는 처리 | 판정 / evidence |
|---|---|---|
| 범위·제약이 이미 주어짐 | 정보를 재사용하고 실제로 빠진 중요 판단만 질문 | MET — 본문 `질문과 범위` |
| 여러 프로젝트의 우선순위 비교 | 공동 의사결정을 유지하며 상세 설계의 무제한 확장은 분리 | MET — 본문 `질문과 범위`, sample 마지막 절 |
| 코드로 반박 가능한 가정 | 직접 확인하고 검토 결과 설명; 별도 비판 질문 횟수 불필요 | MET — 본문 `근거와 대안` |
| 사용자의 허용 손실이 불명확 | 모델이 대신 결정하지 않고 사용자 판단 질문 | MET — 본문 `Boundaries`, `질문과 범위` |
| 수렴 중 새로운 외부 주장 | 검증하거나 남은 불확실성을 표시; 페이즈에 의한 조사 면제 없음 | MET — 본문 `근거와 대안` |
| 실측 데이터 대기만 남음 | 미결·근거·다음 행동을 기록하고 정리 제안 가능 | MET — 본문 `미결과 진행 판단`, sample |
| 사용자가 미결을 남기고 종료 | 추가 승인·분류 질문 없이 저장; 미결을 확정하지 않음 | MET — 본문 `정리와 종료` |
| 질문 도구 부재 또는 응답 단절 | 새 토론을 시작하지 않거나 기존 맥락을 중단·미완료로 저장; 무응답을 동의로 처리하지 않음 | MET — 본문 `Runtime`, `정리와 종료` |
| 일반 요약 / 감사 로그 요청 | 기본 핵심 결과 / 실제 기록이 있는 라운드 로그 포함, 누락은 표시 | MET — summary-template 조건부 규칙 |

## 검증과 implementation review

- 양 runtime YAML·참조 실재·0644, example/template 필수 섹션·표 구조, reference parity, Runtime 외 본문 parity, 도구명 외 example parity, `git diff --check`: PASS.
- 자연어 정책은 test-free triage로 분류했다. 문구 존재 검사를 RED 테스트로 만들지 않고 변경 diff와 위 시나리오의 적용 규칙으로 검토했다.
- skill-creator `quick_validate.py`: 양 runtime 모두 PASS. 링크 85개·기존 사용자 파일·리뷰 원본·main.md 보존 및 history append-only: PASS.
- implementation review gate 1 (gpt-6-astra): 메인 correctness C0/H0/M0/L0, 참조 simplicity C0/H0/M0/L0, 국소 simplicity C0/H0/M0/L0. 소유 차원 4개 모두 PASS. 별도 수정 finding이 없어 fix diff는 없으며 gate 2 임계(C+H ≥ 3 또는 M ≥ 5)에 도달하지 않았다. 본문과 직접 자산은 전문, supporting spec은 변경 hunk를 검토했다.
- **절차 제한:** 첫 참조 leaf에 계약 전문을 전달하면서 AC 도입부 `반환 누락을`을 `반환 누락은`으로, Hard Rule 6의 `legacy uppercase fallback도 허용한다`를 `legacy uppercase fallback으로 사용할 수 있다`로 보냈다. 두 번째 국소 leaf에는 원문을 전달했다. 첫 전달은 installed implementation-review의 ‘계약 전문을 verbatim 포함’ 요구를 충족하지 못했으므로 해당 리뷰 AC1을 NOT MET으로 남긴다. 검토 findings와 소스 AC 판정은 보존하되 전체 절차 준수로 보고하지 않는다. 재dispatch나 추가 gate로 소급 보완하지 않았다.
- 절차 기준: [설치된 implementation-review](/Users/hyunjoonlee/.codex/plugins/cache/sdd-skills-codex/sdd-skills-codex/1.0.1/skills/implementation-review/SKILL.md).
- 실제 Astra/Fable의 질문 수·시간·결정 품질, 설치된 스킬 호출 효과는 미검증이다.

본문 길이는 Claude 297→89행, Codex 271→87행이다. 이는 소스 크기이며 토큰·속도·품질 개선의 측정값이 아니다. 커밋·푸시·설치 캐시 갱신은 수행하지 않았다.
