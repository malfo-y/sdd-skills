# pr-review 목적·경계·결과물 중심 리뷰

- 날짜 / 모델: 2026-09-15 KST / gpt-6-astra
- 기준: `b34b2cb6466c85b5800878310a4304124b3c64d1`, Claude 267행 / Codex 305행.
- 상태: 정적 리뷰. 설계 변경 후보 2건, 출력 명료화 후보 1건, 표현 정리 후보 1건. 스킬·PR 수정이나 실제 리뷰 실행은 하지 않았다.

## 결론

SHA 고정·사용자 작업 보존·실행 증거 검증은 길어도 필요한 계약이다. 우선 줄일 대상은 판정을 담당하지 않는 leaf에 전달하는 정보, 파일 수만으로 읽기 방식을 바꾸는 규칙, 보고 형식의 모호한 집계다. 전체 길이를 줄이려고 매번 읽어야 하는 계약을 reference로 옮기는 것은 권하지 않는다.

## 검토 범위와 기준

[Claude 본문](../../../.claude/skills/pr-review/SKILL.md), [Codex 본문](../../../plugins/sdd-skills-codex/skills/pr-review/SKILL.md), 양쪽 [simplicity 계약](../../../plugins/sdd-skills-codex/skills/implementation-review/references/simplicity-contract.md)을 대조했다. PR 예제의 payload·Signals 관련 부분은 검색으로 확인했다. human reference의 gh 명령 모음·체크리스트 전체 감사와 외부 GitHub 동작 검증은 하지 않았다.

[제작 규범](../../SKILL_AUTHORING_NORMS.md)과 [설계 이력](../../../_sdd/spec/decision_log.md)의 2026-07-30 읽기 범위 결정, 2026-08-12 반환 다이어트, 2026-08-17 correctness 직접 수행, 2026-08-18 계약 주입 전환을 참고했다. PR 리뷰는 충분한 검토를 우선한다는 기존 결정을 유지하며 새로운 시간·읽기 예산은 제안하지 않는다.

## Findings

### PR-P01 — simplicity 입력이 역할보다 넓다 [설계 변경 후보]

- **위치 / 근거:** Claude 30–40 / Codex 75–85행의 `PR Review Input`은 7필드를 필수 전달한다. Spec Context는 baseline spec bundle이고, Validation Evidence와 Report Slug도 포함한다. simplicity 계약 Step 1은 Changed Files·PR Diff로 범위를 정하고 나머지는 맥락으로만 쓰며, 테스트 판정·파일 작성은 맡지 않는다.
- **문제 상황:** 큰 spec bundle과 검증 자료를 수집한 메인 루프가 이를 형태 품질만 보는 leaf에도 전달한다. 이것이 항상 잘못된 리뷰를 만든다는 증거는 없지만, leaf의 판단에 필요하지 않은 정보까지 필수 인터페이스에 결합돼 있다.
- **권고:** 메인은 현재 수집 책임을 유지한다. leaf에는 diff·변경 파일·같은 SHA의 읽기 경로와 동작 보존을 이해하는 데 필요한 제약/대화 맥락을 전달하는 안을 검토한다. Report Slug·검증 결과 전문·전체 spec의 필수 전달은 실제 소비 여부로 결정한다. PR 배경을 전부 제거하는 제안은 아니다.
- **유지 / 손실 위험:** baseline 동일성, read-only, 계약 전문 주입, 외형상 중복이 의도된 경우를 설명할 맥락은 유지한다. 입력 축소가 동등성 오판을 늘리는지 봐야 한다.
- **검증 시나리오:** 의도적으로 분리된 유사 코드와 불필요한 wrapper를 함께 둔 PR에서 두 경우를 구별하는지 비교한다. 전송량 감소만으로 성공 판정하지 않는다.

### PR-P02 — 50파일 기준이 위험보다 파일 수를 우선한다 [설계 변경 후보]

- **위치 / 근거:** Claude 95·245 / Codex 134·284행. 50+ files면 디렉토리/컴포넌트 수준으로 축약하고 spec 관련 파일에 집중한다.
- **문제 상황:** 60개 문서 경로 변경과 그중 한 파일의 권한 검사 변경은 파일 수가 같아도 필요한 검토가 다르다. 문면의 숫자는 어떤 파일에 깊이를 써야 하는지 설명하지 못한다. 해당 규칙이 검토 생략을 무조건 허용한다고 단정하지는 않는다.
- **권고:** 반복적인 동등 변경은 묶어 설명하되, 실행 동작·권한·데이터 경계·통합 위험이 있는 변경에는 필요한 깊이를 유지한다. 축약은 보고와 반복 분석에 적용하고 미검토 범위는 명시한다. 신규 파일 수·시간 상한을 만들지 않는다.
- **유지 / 손실 위험:** Changed Files 기준, 모든 관련 AC 판정, 큰 PR의 정직한 범위·한계 보고. 재량 확대가 고위험 변경 누락으로 이어지는지 비교한다.
- **검증 시나리오:** 다수 기계적 변경에 작은 보안 결함을 섞고, 파일 수가 적지만 복잡한 상태 전이 변경과 함께 검토한다.

### PR-P03 — 필수 test pass 비율의 분모가 정의돼 있지 않다 [출력 명료화 후보]

- **위치 / 근거:** Claude 183 / Codex 222행의 Signals는 `test pass F% (또는 UNTESTED)`를 요구한다. Fresh Verification은 유효한 CI/local output을 요구하지만 테스트 케이스·suite·명령 중 어떤 단위를 집계할지는 정의하지 않는다.
- **문제 상황:** exit 0만 출력하는 검사 1개와 100개 케이스를 보고하는 suite를 함께 실행하면 단일 퍼센트의 의미가 불명확하다. 알려진 검사만 통과한 것을 전체 검증의 100%로 오독할 여지도 있다.
- **권고:** 기본은 실제 실행한 검사와 PASS/FAIL/UNTESTED 및 증거 위치로 보고한다. 비율은 분모와 범위가 실행 출력에서 명확하고 의사결정에 도움이 될 때만 표시한다. 별도 집계 체계는 만들지 않는다.
- **유지 / 손실 위험:** 실행 evidence 없는 APPROVE 방지, 실패 finding과 AC ledger의 연결. 보고를 줄여 실패 검사나 누락 범위를 숨기면 안 된다.
- **검증 시나리오:** exit-code 검사만 있는 PR, 여러 suite 일부 실패, 실행 evidence 부재를 넣어 분모를 창작하지 않고 상태를 전달하는지 확인한다.

### PR-P04 — Codex adapter가 설명·예시·재천명으로 같은 동작을 반복한다 [표현 정리 후보]

- **위치 / 근거:** Codex 30–73행은 lifecycle 선택, optional role, model override, 두 호출 예시, message framing을 정의한다. implementation-review에도 거의 같은 runtime 골격이 있다.
- **권고:** 각 본문에서 선택 조건·필수 인자·실패 경계를 한 번씩만 정의한다. 예시는 산문으로 설명되지 않는 차이를 보여줄 때만 남긴다. 독립 배포용 미러를 결함으로 보거나 전역 runtime 프레임워크를 새로 만들지 않는다.
- **유지 / 손실 위험:** active schema로 선택, 미지원 사용자 override 보고, role selector 선택성, 완료 수거, framed payload, 제한 종료는 유지한다. 예시 삭제로 필수 필드가 사라지는지 역검증해야 한다.
- **검증 시나리오:** mailbox / legacy target-close / 불완전 schema / role 필드 부재를 정적으로 대조하고, 이후 지원 런타임에서 실행 확인한다. 이 항목은 [IR-P04](./implementation-review-purpose-review.md)의 공유 원인이다.

## 유지할 계약과 후속 범위

baseline 코드·spec·증거 결속, dirty 보존, spec 부재와 읽기 실패 구분, 두 렌즈의 역할, 사람이 판단하는 verdict, 위치·문제·수정이 자족적인 finding, 제한 리뷰의 정직한 종료는 유지한다. 보고서의 긴 skeleton 자체는 결함으로 채택하지 않았다. 인간 리뷰어가 소비하는 결과물이며 항상 필요한 내용을 파일로 옮겨도 총 읽기·작성 부담이 줄지는 않는다.

수정 시 양쪽 본문·sample report, 공유 simplicity 입력 계약, global spec의 7필드/보고/범위 설명을 함께 확인한다. PR-P01·02는 정책 변경이며 이번 리뷰만으로 적용하지 않는다. 실제 PR 판정의 품질·시간 개선은 미검증이다.
