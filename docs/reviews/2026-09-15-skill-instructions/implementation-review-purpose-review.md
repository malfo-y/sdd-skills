# implementation-review 목적·경계·결과물 중심 리뷰

- 날짜 / 모델: 2026-09-15 KST / gpt-6-astra
- 기준: `b34b2cb6466c85b5800878310a4304124b3c64d1`, Claude 108행 / Codex 153행.
- 상태: 정적 리뷰. 범위 정합성 수정 권고 1건, 표현 정리 후보 2건, 출력 정리 후보 1건. 실제 구현 gate·subagent·테스트 실행은 하지 않았다.

## 결론

범위·증거·렌즈 책임은 명확히 고정해야 한다. 먼저 커밋/미커밋 혼합 변경의 범위 규칙을 보완하고, 그다음 읽기 규칙과 보고의 표현을 정리하는 것이 좋다. 2개 simplicity agent나 fresh 검증을 없애는 방향은 권하지 않는다.

## 검토 범위와 기준

[Claude 본문](../../../.claude/skills/implementation-review/SKILL.md), [Codex 본문](../../../plugins/sdd-skills-codex/skills/implementation-review/SKILL.md), 양쪽 [simplicity 계약](../../../plugins/sdd-skills-codex/skills/implementation-review/references/simplicity-contract.md), producer인 implementation과 pr-review의 소비 경계를 대조했다. 공유 reference는 byte-identical이다.

[설계 이력](../../../_sdd/spec/decision_log.md)의 2026-07-30 읽기 범위, 2026-08-12 위험 적응형 읽기, 2026-08-17 직접 correctness, 2026-08-18 계약 주입 전환을 확인했다. 아래 시나리오는 문면 반례이며 관측된 모델 실패가 아니다. [제작 규범](../../SKILL_AUTHORING_NORMS.md) §5에 따라 실측을 근거로 둔 경계를 단순 길이만으로 없애지 않는다.

## Findings

### IR-P01 — 변경 집합의 fallback이 커밋/미커밋 혼합 실행을 충분히 덮지 못한다 [범위 정합성 수정 권고]

- **위치 / 근거:** Claude 55 / Codex 100행은 working tree·index·untracked를 읽고, “미커밋 집합이 비었을 때만” 구현 시작점 대비 `<base>..HEAD` diff를 사용한다. 같은 문단은 호출자 scope와 시작 시 dirty paths로 이번 변경을 구분하도록 한다.
- **문제 상황:** 하나의 구현 범위에서 T1을 커밋하고 T2를 미커밋으로 남긴 뒤 마감 리뷰를 하면, 명시된 diff 수집 분기는 T2만 보여준다. unrelated dirty 파일 하나가 남아 있어도 커밋 diff fallback은 열리지 않는다. scope 명시는 목표를 알려주지만 누락된 커밋 diff를 확보하는 절차를 대체하지 않는다.
- **권고:** 먼저 이번 구현의 시작점·호출자 scope를 정하고, 그 범위의 커밋된 변경과 staged/unstaged/untracked 변경을 함께 대조한다. 최초 dirty와 타 작업은 분리한다. “비었을 때만”이라는 상호 배타 조건 대신 이번 변경의 완전성을 기준으로 삼는다. 관련 없는 커밋 이력 전체를 읽으라는 제안은 아니다.
- **유지 / 손실 위험:** 현재 Target Files 목록으로 실제 변경을 대체하지 않기, dirty 보존, 불확실한 귀속 보고. 범위를 합치며 오래된 작업까지 포함시키지 않도록 기준점을 명시해야 한다.
- **검증 시나리오:** 전부 미커밋, 전부 커밋, T1 커밋+T2 미커밋, 커밋된 작업+무관한 dirty의 네 경우에서 같은 구현 변경을 빠짐없이 포함하고 무관한 변경은 제외해야 한다. 현재 판정은 정적 반례이며 실제 gate 재현은 후속 검증이다.

### IR-P02 — 전문 읽기 조건 여섯 개가 한 문장에 과밀하다 [표현 정리 후보]

- **위치 / 근거:** Claude 56 / Codex 101행. 실행 semantics 파일, 제어 흐름, 행동 AC, 사실상 재작성, 의심 발견, Open Questions의 여섯 조건을 한 긴 불릿에서 OR로 연결한다.
- **권고:** 기본 읽기 범위와 전문 승격 조건을 같은 절에서 짧은 목록이나 표로 나눈다. 여섯 조건의 의미와 OR 관계는 그대로 둔다. 실행 코드에 대한 전문 읽기 조건을 지우고 일반적인 “위험에 따라 알아서”로 대체하지 않는다.
- **유지 / 손실 위험:** code·script·hook은 첫 조건만으로 전문 읽기 대상이라는 현행 의미, hunk-scoped 표시, 기준 문서/참조 spec 구분, 범위 밖이어도 AC 필수 증거 확보, 미검토 한계 보고.
- **검증 시나리오:** 여섯 조건을 각각 단독으로 만족하는 경우와 모두 없는 산문 변경을 비교한다. 짧아진 문면이 전문 읽기 집합을 바꾸면 표현 정리가 아닌 정책 변경으로 재분류한다.

### IR-P03 — Recommendations가 finding의 조치와 별도 출력된다 [출력 정리 후보]

- **위치 / 근거:** Claude 84–89 / Codex 129–134행. finding 블록이 이미 수정 방향을 포함하고, 별도 Recommendations는 finding ID 참조 또는 새로운 권고 한 줄이다. producer implementation은 finding의 렌즈·severity와 개수를 기준으로 fix·다음 gate를 정한다.
- **권고:** 별도 ID 목록이 실제 소비에 도움이 되는지 확인하고, 중복이면 finding의 수정 항목으로 통합한다. 재개 조건이나 검증 불가 조치처럼 finding과 다른 후속 행동은 제한/후속 조치로 유지할 수 있다. 새 권고를 의무적으로 생성하지 않는다.
- **유지 / 손실 위험:** raw severity 합산은 producer가 소비하므로 중복 요약으로 삭제하지 않는다. AC별 증거 포인터와 simplicity 차원 판정도 각각 판정 근거·스캔 완전성 소비가 있어 유지한다.
- **검증 시나리오:** finding 없음, 여러 finding, dispatch 실패를 각각 producer에 인계한다. 수정 대상·재리뷰 판단·미완료 재개 조건이 모두 복원돼야 한다. 모든 외부 소비자의 부재를 확인한 것은 아니다.

### IR-P04 — runtime 설명 중복은 PR 리뷰와 함께 정리한다 [표현 정리 후보, 공유 원인]

- **위치 / 근거:** Codex 25–70행. lifecycle 산문·호출 예시·framing이 반복되는 구조는 [PR-P04](./pr-review-purpose-review.md)와 같다.
- **권고:** PR-P04의 표현 정리를 함께 적용하되, 이 스킬의 2개 차원 묶음·각각 전체 변경 범위·대화 digest·모든 final 수거는 고유 계약으로 보존한다. 독립 배포용 사본을 없애거나 항상 읽을 runtime 문서를 분리하는 것을 목표로 삼지 않는다.
- **검증 시나리오:** PR의 leaf 1개와 implementation의 leaf 2개가 각 schema에서 정확히 유지되는지 확인한다. 실사용 전에 실제 지원 schema와 맞는지 검증한다.

## 유지할 계약과 후속 범위

read-only, correctness 직접 수행과 simplicity 2묶음, 계약 전문 verbatim 주입, 능동 correctness 검토, fresh evidence, 미검증 AC의 정직한 보고, producer로 즉시 fix 인계는 유지한다. 이들은 단순한 진행 취향이 아니라 리뷰 책임과 증거의 경계다.

IR-P01은 현재 스킬의 목적을 충족하기 위한 정합성 보완이며 IR-P02·04는 표현 정리다. IR-P03은 반환 인터페이스 변경 후보이므로 소비자 확인이 선행돼야 한다. 수정 시 양쪽 본문·implementation 입력/범위 설명·global spec의 관련 읽기 계약을 대조한다. 리뷰 탐지율·처리 시간의 개선은 이번에 검증하지 않았다.
