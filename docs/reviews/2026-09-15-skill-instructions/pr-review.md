# pr-review 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/pr-review/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/pr-review/SKILL.md)
- 판정 요약: 수정 필요 7 / 정리 후보 0 / 실행 검증 필요 0

## 역할과 유지할 계약

PR head의 코드·spec을 기준으로 메인 루프가 correctness를 직접 리뷰하고, simplicity leaf가 전체 변경을 4차원으로 한 번 검토한다. 메인 루프만 통합 리포트를 작성하며 verdict는 인간 리뷰를 돕는 권고다. spec 읽기 전용, leaf 읽기 전용·재위임 금지, reference 전문 전달, 실행 증거 없는 테스트 판정의 `UNTESTED`, 30초 표적 검증 예산을 유지한다. 아래 제안은 simplicity leaf 구조를 바꾸지 않는다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | pr-review-01·02·03: head 이름, 변경 목록, 읽기 실패를 각각 정확한 baseline·spec 존재 여부의 대리값으로 사용한다. |
| 2. 충돌과 우선순위 | pr-review-03·05·07: spec 부재와 실패의 구분, degraded report와 AC, ledger와 출력 형식 사이 계약이 맞지 않는다. |
| 3. 확인·승인 경계 | pr-review-04: Claude는 정상적인 다중 spec 구조에도 무조건 선택 질문을 요구한다. |
| 4. 중복과 소유권 | 수정 필요 없음: simplicity의 소유자는 sibling reference이며 verdict는 본문 한 곳이 소유한다. runtime mirror 자체는 결함이 아니다. |
| 5. 완료·복구 조건 | pr-review-05·06: 복구 불가능한 leaf 누락의 종료 조건과 같은 날 리포트 충돌 처리가 빠졌다. |
| 6. 절차의 필요성 | pr-review-01·04: 정확성을 보장하지 못하는 branch 이름 제한과 결과에 영향 없는 spec 선택 질문을 줄일 여지가 있다. 고정 leaf와 자체 검증은 보존한다. |

## Findings

### pr-review-01 — branch 이름 일치로 PR head의 코드·spec 동일성을 보장하지 못함 [수정 필요]

- 기준: 1, 6. Runtime: Claude·Codex.
- 근거: [Claude SKILL](../../../.claude/skills/pr-review/SKILL.md) 46–53행, 75행; [Codex SKILL](../../../plugins/sdd-skills-codex/skills/pr-review/SKILL.md) 91–98행, 119–125행.
- 원문: “현재 브랜치 ≠ `headRefName` → … **즉시 종료**한다.” / “현재 checkout이 PR head면 working tree의 `_sdd/spec/`”. Claude는 `git show origin/[headRefName]:_sdd/spec/main.md`를 지시한다.
- 문제 상황: 로컬 branch 이름은 같지만 원격 PR보다 뒤처졌거나 로컬 수정이 남아 있다. Step 0은 통과하고 원격 PR diff와 다른 로컬 코드·spec·로컬 테스트 결과가 합쳐진다. 반대로 이름이 다른 checkout 또는 detached HEAD가 정확히 `headRefOid`를 가리켜도 즉시 종료된다.
- 예상 영향: 리포트의 PR SHA와 실제 판정한 파일·실행 증거의 버전이 달라질 수 있다. 이름 제한 때문에 정확한 읽기 경로가 있는 작업도 중단된다.
- 최소 수정안: baseline을 수집한 `headRefOid`로 고정하고 실제 읽기·검증 대상의 동일성을 확인한다. local validation에는 HEAD와 관련 working tree 상태를 확인한다. 다르면 기존 작업을 건드리지 않는 해당 SHA 읽기/격리 checkout 경로로 진행하고, 같은 버전의 실행 증거를 확보하지 못하면 해당 테스트 판정을 `UNTESTED`로 둔다. branch 이름 불일치만으로 종료하지 않는다.
- 유지할 계약: from-branch 기준, 기존 사용자 작업 보존, 증거 없는 MET 금지.
- 소유자: pr-review 양 runtime의 Step 0–2·Fresh Verification. 기본 결정 변경은 불필요하며 baseline 집행 보강이다.
- 검증 상태: 지시의 확인 항목과 데이터 경로 정적 대조. stale checkout에서 실제 오판하는지는 실행하지 않았다.

### pr-review-02 — Claude가 spec 변경이 없는 PR의 기존 spec을 찾지 못하는 경로 [수정 필요]

- 기준: 1, 2. Runtime: Claude.
- 근거: [Claude SKILL](../../../.claude/skills/pr-review/SKILL.md) 72–76행. 비교: [Codex SKILL](../../../plugins/sdd-skills-codex/skills/pr-review/SKILL.md) 119–127행.
- 원문: “`gh pr diff [PR] --name-only`에서 `_sdd/spec/` 경로 파일 확인” → “존재하면 … from-branch spec 읽기”.
- 문제 상황: 저장소의 `_sdd/spec/main.md`와 하위 spec은 그대로 있고 PR은 구현 파일만 변경했다. Claude Step 2에는 변경 목록에 spec이 없을 때 head 트리에서 기존 spec을 찾는 단계가 없다.
- 예상 영향: spec 기반 리뷰가 필요한 일반적인 구현 PR에서 baseline 탐색이 닫히지 않거나 code-only로 잘못 흐를 수 있다. Codex는 이 경우를 명시적으로 처리한다.
- 최소 수정안: Codex Step 2의 “PR diff에 spec 변경이 없더라도” head 트리 확인과 index·하위 spec 읽기를 Claude에 맞게 반영한다. SHA 결속은 pr-review-01과 함께 적용한다.
- 유지할 계약: 실제 from-branch spec이 없는 경우에만 정상 code-only 모드, runtime-local 실행 방식.
- 소유자: pr-review Claude Step 2 및 같은 흐름을 보여주는 [Claude 예제](../../../.claude/skills/pr-review/examples/sample-review.md) 25–28행. cross-skill 변경 없음.
- 검증 상태: 양 runtime의 동일 입력 처리 경로를 정적 비교했다. 실제 PR 조회는 하지 않았다.

### pr-review-03 — spec 읽기 실패를 spec 부재와 같은 code-only로 처리 [수정 필요]

- 기준: 1, 2, 5. Runtime: Claude·Codex.
- 근거: [Claude SKILL](../../../.claude/skills/pr-review/SKILL.md) 238행, 170행; [Codex SKILL](../../../plugins/sdd-skills-codex/skills/pr-review/SKILL.md) 127행, 215행, 283행.
- 원문: “from-branch spec 읽기 실패 | code-only mode로 fallback”; Codex Step 2는 “spec 파일이 전혀 없을 때만 → **code-only 모드**”.
- 문제 상황: spec 파일 존재는 확인했지만 ref 미확보, 권한 또는 읽기 오류로 내용을 가져오지 못했다. Error Handling은 code-only 전환을 지시하고 Output의 spec 상태는 Found/Not Found 두 종류뿐이다.
- 예상 영향: 확인하지 못한 spec을 없는 것으로 표시하고 spec compliance가 빠진 상태에서 정상 code-only 승인 기준을 적용할 수 있다.
- 최소 수정안: `ABSENT`와 `UNREADABLE`을 분리한다. 후자는 가능한 동등 읽기 경로를 사용한 뒤에도 실패하면 correctness 중 검토 가능한 부분을 보고하되 spec 판정 미검증과 원인을 표시하고 `NEEDS DISCUSSION`으로 닫는다. 정상 code-only는 부재 확인 때만 허용한다.
- 유지할 계약: spec 읽기 전용, 가능한 리뷰 결과 보존, evidence 없는 완료 승격 금지.
- 소유자: pr-review 양 runtime Error Handling·Output·Verdict. 다른 spec 스킬로 해결을 위임할 필요 없음.
- 검증 상태: Codex 본문 내부의 조건 충돌과 양 runtime 출력 상태를 정적 확인했다.

### pr-review-04 — Claude의 다중 spec 선택 질문이 모호성 여부와 무관하게 발동 [수정 필요]

- 기준: 3, 6. Runtime: Claude.
- 근거: [Claude SKILL](../../../.claude/skills/pr-review/SKILL.md) 226행; [Codex SKILL](../../../plugins/sdd-skills-codex/skills/pr-review/SKILL.md) 271행. [global spec](../../../_sdd/spec/main.md) 10행은 main과 supporting 문서 구조를 설명한다.
- 원문: “Multiple spec files in from-branch | AskUserQuestion으로 선택”.
- 문제 상황: `main.md`가 명백한 index이고 여러 하위 spec을 링크하는 정상 구조다. 파일이 여러 개라는 이유만으로 이미 정해진 진입점을 다시 선택하게 한다.
- 예상 영향: 실제 리뷰 판단에 필요하지 않은 사용자 응답을 기다리며 진행을 멈춘다.
- 최소 수정안: Codex처럼 canonical index를 우선하고, 그 뒤에도 verdict에 영향을 주는 선택이 남을 때만 짧게 질문한다. 하위 spec은 선택 경쟁자가 아니라 index의 구성으로 읽는다.
- 유지할 계약: 실질적 범위 모호성은 사용자에게 확인하고 선택 가정을 기록한다.
- 소유자: pr-review Claude Edge Cases. cross-skill 변경 없음.
- 검증 상태: 명시적 질문 발동 조건을 정적 확인했다. 실제 질문 발생 횟수는 측정하지 않았다.

### pr-review-05 — 누락 렌즈 fallback과 무조건 AC 복귀가 서로 다른 종료를 요구 [수정 필요]

- 기준: 2, 5. Runtime: Claude·Codex.
- 근거: [Claude SKILL](../../../.claude/skills/pr-review/SKILL.md) 16–19행, 239행, 249행; [Codex SKILL](../../../plugins/sdd-skills-codex/skills/pr-review/SKILL.md) 16–19행, 38행, 284행, 293행.
- 원문: “simplicity 반환 실패 | correctness 렌즈로 통합 리포트를 작성하되 누락 렌즈를 명시하고 재실행을 안내”; “미충족 항목이 있으면 해당 단계로 돌아가 수정한다.”
- 문제 상황: Codex lifecycle schema가 불완전하거나 simplicity 반환이 실패했다. 명시된 fallback 리포트는 작성할 수 있지만 AC2·AC4·AC5의 두 렌즈 조건은 만족시킬 수 없다. Final Check에는 이 상태를 미완료로 보고하고 종료하는 분기가 없다.
- 예상 영향: 동일 blocker에서 반복 dispatch를 시도하거나, fallback을 완료로 잘못 표시하거나, 보고 후 재실행 안내와 실제 내부 재시도 중 어느 것을 수행할지 흔들린다.
- 최소 수정안: 자체 검증은 유지하되 수정 가능한 산출물 누락만 복구한다. 외부 blocker·확정된 렌즈 실패는 미충족 AC와 원인을 남긴 제한 리포트로 종료하며 정상 완료를 선언하지 않도록 Final Check에 명시한다. 누락 렌즈가 있는 verdict는 제한된 권고임을 표시한다.
- 유지할 계약: mandatory simplicity dispatch를 임의 inline으로 대체하지 않음, fail-closed lifecycle 선택, AC 자체 점검, 잔여 이슈 보고.
- 소유자: pr-review 양 runtime Final Check·Error Handling·Codex Runtime Adapter. 공통 AC 규범 변경까지 요구하는 제안은 아니다.
- 검증 상태: 정상 AC와 명시된 실패 경로의 만족 가능성을 정적 대조했다. 반복 실행 현상은 관측하지 않았다.

### pr-review-06 — 날짜와 slug가 같은 재리뷰의 파일 충돌을 배제할 근거가 없음 [수정 필요]

- 기준: 5. Runtime: Claude·Codex.
- 근거: [Claude SKILL](../../../.claude/skills/pr-review/SKILL.md) 157행, 227행; [Codex SKILL](../../../plugins/sdd-skills-codex/skills/pr-review/SKILL.md) 202행, 272행.
- 원문: “Existing review file | 날짜+slug로 구분되므로 별도 처리 불필요”.
- 문제 상황: 같은 날 같은 PR을 수정 후 다시 리뷰한다. 동일한 PR 의미에서 같은 slug를 선택하면 두 실행은 정확히 같은 `_sdd/pr/<date>_pr_review_<slug>.md`를 가리킨다.
- 예상 영향: 이전 리뷰를 의도 없이 덮어쓰거나 기존 내용과 새 verdict가 섞일 수 있다. 현재 문구는 충돌 검사를 생략하도록 지시한다.
- 최소 수정안: 생성 전 존재 여부를 확인하고 기본적으로 slug에 짧은 순번 등 구별자를 붙여 새 파일을 만든다. 사용자가 기존 리포트 갱신을 명시했을 때만 그 지시를 따른다.
- 유지할 계약: lowercase dated slug 경로, 실행당 통합 리포트 한 파일, 이전 사용자 산출물 보존.
- 소유자: pr-review 양 runtime Step 1·Edge Cases. cross-skill 변경 없음.
- 검증 상태: 파일명 구성의 충돌 가능성 정적 확인. 기존 파일을 만들거나 덮어쓰는 실행은 하지 않았다.

### pr-review-07 — 문제 AC ledger의 출력 의무가 리포트 skeleton에 연결되지 않음 [수정 필요]

- 기준: 2, 5. Runtime: Claude·Codex.
- 근거: [Claude SKILL](../../../.claude/skills/pr-review/SKILL.md) 134행, 157행, 207–209행; [Codex SKILL](../../../plugins/sdd-skills-codex/skills/pr-review/SKILL.md) 179행, 202행, 252–254행.
- 원문: “문제 있는 verdict(NOT MET·PARTIAL·UNTESTED·FAIL)만 행으로 낸다 — `| # | Criterion | Implementation | Test | Status | Evidence |`”; “AC 검증 요지·차원 판정은 §3(확인된 것)에 산문으로 요약”; §3은 “표·퍼센트 없음”.
- 문제 상황: 여러 inferred/spec AC 가운데 일부가 `UNTESTED` 또는 `PARTIAL`이다. correctness 절은 증거 행을 출력하라고 하지만 단일 통합 리포트 skeleton에는 그 위치가 없고, AC를 놓는 §3은 산문만 허용한다. 예제 리포트도 문제 AC ledger를 생략한다.
- 예상 영향: skeleton을 그대로 따르면 요구된 criterion별 증거 행이 빠지고, ledger를 넣으면 선언된 출력 형식의 어디에 귀속할지 실행자가 새로 결정해야 한다.
- 최소 수정안: 같은 리포트 안에 문제 AC ledger의 명시적 slot을 추가하고 정상 AC는 기존 MET 접기를 유지한다. §3의 산문 요약과 중복 전사는 피한다. 문제 AC ledger 자체를 삭제하려면 [global spec](../../../_sdd/spec/main.md) 85행의 현행 반환 계약에 대한 spec 결정이 먼저 필요하다.
- 유지할 계약: 통계 표 금지, 문제 AC 증거 행과 MET 접기, 단일 작성자·단일 리포트, 행동 대상 finding 전문.
- 소유자: pr-review 양 runtime Output Format·예제. ledger 삭제 대안을 선택할 경우에만 global spec 소유자와 결정 필요.
- 검증 상태: 출력 의무와 fenced skeleton·예제를 정적 대조했다. 실제 출력 누락은 관측하지 않았다.

## 런타임 차이와 의존성

- Claude `Agent`와 Codex active-schema lifecycle·model/effort 처리는 정당한 runtime 차이다. 현재 노출 도구만으로 영구 지원 범위나 특정 model 허용 여부를 판정하지 않았다. override enum 유무 자체는 이번 finding으로 삼지 않았다.
- Codex의 spec head 트리 탐색과 canonical index 선택은 Claude보다 구체적이다. pr-review-02·04는 이 업무 계약 차이를 다룬다. 배포 mirror를 제거하자는 제안은 아니다.
- 양 runtime의 [simplicity reference](../../../plugins/sdd-skills-codex/skills/implementation-review/references/simplicity-contract.md) 전문을 읽었고 byte 차이가 없음을 확인했다. 이 reference의 자체 rubric 결함 여부는 `implementation-review` 소유자가 통합 판정한다. pr-review는 계약 전달·합류 경계만 소유한다.
- 양 runtime의 [review-checklist](../../../plugins/sdd-skills-codex/skills/pr-review/references/review-checklist.md)와 [sample-review](../../../plugins/sdd-skills-codex/skills/pr-review/examples/sample-review.md), Claude 전용 [gh-commands](../../../.claude/skills/pr-review/references/gh-commands.md)를 읽었다. 체크리스트는 verdict 기준을 본문으로 가리킨다. 예제·gh reference의 과거 명칭이나 설명 차이는 현행 본문을 뒤집는 독립 실행 의무로 보지 않아 별도 finding을 만들지 않았다.
- 미검토: `implementation-review` 전체 SKILL 실행 계약, GitHub CLI 실환경/API 응답, 설치본 프롬프트의 실제 dispatch·모델 행동. 이 리뷰는 repo 문면을 검토했으며 설치된 피리뷰 스킬을 호출하지 않았다.

## 권장 처리 순서와 검증

1. pr-review-01·02·03을 함께 고쳐 리뷰 대상 SHA와 spec 존재/실패 상태를 먼저 닫는다. spec 변경 없는 PR, stale local branch, dirty tree, spec 읽기 실패를 각각 입력 사례로 대조한다.
2. pr-review-04·05·06의 질문·종료·충돌 분기를 보완한다. 명확한 다중 spec index에는 질문하지 않고, leaf blocker는 미완료 리포트로 유한 종료하며, 같은 날짜·slug의 이전 결과가 보존되는지 확인한다.
3. pr-review-07의 ledger slot을 skeleton과 예제에 반영하고 문제 AC 한 건·통과 AC 한 건의 리포트에서 각 정보가 한 곳에만 남는지 확인한다. `git diff --check`, runtime 짝 diff, 상대 링크 검사를 수행한 뒤 필요하면 별도 실제 PR 리뷰 세션으로 동작을 검증한다.

이번 작업은 지시 정적 리뷰와 이 문서 작성만 수행했다. 제안한 수정·PR 조회·테스트·simplicity dispatch는 실행하지 않았다.
