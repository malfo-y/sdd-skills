# implementation-review 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/implementation-review/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/implementation-review/SKILL.md)
- 판정 요약: 수정 필요 4 / 정리 후보 0 / 실행 검증 필요 0

## 역할과 유지할 계약

메인 루프가 correctness를 직접 검증하고, 두 simplicity leaf가 각각 전체 변경을 서로 다른 차원으로 검토한다. 리뷰어는 파일을 수정하지 않고 증거에 묶인 합산 보고만 반환한다. 수정과 재게이트 판단은 producer인 `implementation`이 소유한다.

단일 pass, 차원별 전체 변경 범위, reference 전문 주입, 3단 읽기 범위, 위험 시 전문 승격, fresh evidence, 30초 표적 check 예산, slow checkpoint 경계, MET 증거 포인터를 유지한다. 두 runtime 배포 mirror 자체는 중복 결함으로 보지 않았다.

## 기준별 판정

| 기준 | 판정과 근거 |
|---|---|
| 1. 적용 조건 | implementation-review-01: 변경 집합 추출이 staged/untracked 상태를 포함하지 않는다. implementation-review-02: env 문서 유무를 검증 실행 가능성과 동일하게 취급한다. |
| 2. 충돌과 우선순위 | implementation-review-03: reference의 모든 finding에 대한 falsifiability 제한과 주관적 Low 분류가 충돌한다. implementation-review-04: 오류 종료와 무조건 AC 복구가 충돌한다. |
| 3. 확인·승인 경계 | 별도 수정 필요 없음. producer gate 반환은 입력을 기다리지 않고 fix로 복귀한다. Codex의 추가 허가 분기는 현재 런타임 정책이 실제로 요구하는 경우로 한정돼 있으므로 일반적인 재승인 결함으로 단정하지 않았다. |
| 4. 중복과 소유권 | reference가 simplicity 계약을 소유하고 양 호출 스킬은 이를 주입한다. implementation-review-03은 이 소유 문서에서 한 번 해결할 사안이다. producer가 fix와 gate 횟수를 소유하는 경계는 명확하다. |
| 5. 완료·복구 조건 | implementation-review-04: schema blocker 또는 이미 일어난 순서 위반은 해당 단계 재수행으로 원래 실행 이력을 충족시킬 수 없다. |
| 6. 절차의 필요성 | 별도 수정 필요 없음. 두 차원 묶음·전문 주입·fresh verification은 명시적 설계다. 절차를 줄일 실측 근거 없이 제거를 권하지 않는다. env 조건의 불필요한 차단은 implementation-review-02로 기록했다. |

## Findings

### implementation-review-01 — 변경 집합에서 staged·untracked 파일이 빠지는 경로 [수정 필요]

- 기준: 1, 5. 적용 runtime: Claude, Codex.
- 위치: [Claude SKILL](../../../.claude/skills/implementation-review/SKILL.md) 52줄, [Codex SKILL](../../../plugins/sdd-skills-codex/skills/implementation-review/SKILL.md) 97줄.
- 원문: “변경 파일: `git diff --name-only`. 비어 있으면(구현이 이미 커밋된 경우) `git diff --name-only <base>..HEAD` 또는 `git log`로 실측한다.”
- 문제 상황: draft 없는 저장소에서 기존 파일 수정은 모두 stage하고 신규 파일 하나는 untracked로 둔 채 구현 리뷰를 요청한다. 기본 `git diff --name-only`는 두 종류를 모두 놓치며, 빈 결과를 커밋 완료로 해석한 후속 경로도 아직 커밋되지 않은 변경을 되찾지 못한다. unstaged 파일도 함께 있으면 빈 결과 fallback조차 발동하지 않는다.
- 예상 영향: 실제 변경의 일부가 correctness 1단계 범위에 들어오지 않고, 전체 변경 검토라는 요청과 보고의 대상이 달라질 수 있다. 이는 명령·분기 범위의 정적 누락이며 모델 실행에서 누락을 관측했다는 뜻은 아니다.
- 최소 수정안: working tree·index·untracked의 합집합으로 미커밋 변경을 확인하고, 그 집합이 비어 있을 때만 명시한 base 대비 커밋 diff로 내려간다. 예를 들어 `git status --short` 또는 porcelain 상태로 분류하고 각 상태에 맞는 diff/파일 읽기를 선택한다. draft Target Files와 실제 변경 목록의 차이는 범위 가정으로 명시한다.
- 유지할 계약: 리뷰 대상 변경 집합만 읽고, 변경 밖 탐색을 무제한 확대하지 않는다. 파일을 stage하거나 수정하지 않는다.
- 소유자: `implementation-review`의 읽기 범위 절. 별도 global spec 설계 변경은 필요하지 않다.
- 검증 상태: 양 runtime 문면과 명령 범위 대조 완료. 스킬 실행 미검증.

### implementation-review-02 — env.md 부재만으로 실행 가능한 검증까지 차단 [수정 필요]

- 기준: 1, 6. 적용 runtime: Claude, Codex.
- 위치: [Claude SKILL](../../../.claude/skills/implementation-review/SKILL.md) 62줄, [Codex SKILL](../../../plugins/sdd-skills-codex/skills/implementation-review/SKILL.md) 107줄.
- 원문: “`_sdd/env.md`가 있으면 환경 설정을 적용해 테스트를 시도하고, 없으면 코드 분석만 수행하고 `UNTESTED` 표기.”
- 문제 상황: `_sdd/env.md`가 없는 일반 저장소에서 사용자가 정확한 1초 표적 검증 명령과 환경을 이미 제공했다. 또는 plan의 Verification Method가 추가 환경 없이 실행되는 정적 check를 지정했다. 본문은 이 경우에도 코드 분석만 허용한다.
- 예상 영향: 실행 조건이 확보됐는데도 검증이 생략되고 AC가 불필요하게 UNTESTED로 남는다. “기준이 없다고 중단하지 않는다”는 graceful degradation의 의도와도 맞지 않는 부분 차단이다.
- 최소 수정안: “env.md가 있으면 우선 적용한다. 없으면 사용자·기준 문서·확인 가능한 프로젝트 검증 명령을 사용한다. 실행 조건을 확보할 수 없는 AC만 사유와 함께 UNTESTED로 남긴다.”로 조건을 실행 가능성에 연결한다.
- 유지할 계약: 환경·권한을 추측해 실행하지 않으며, 30초 예산·slow checkpoint 제한과 증거 없는 MET 금지를 유지한다. 실행 의존 AC를 코드만 보고 통과시키지 않는다.
- 소유자: `implementation-review` Fresh Verification. `pr-review`의 별도 CI/local validation 우선순위는 이 finding의 수정 범위가 아니다.
- 검증 상태: 양 runtime 동일 문구 확인. 예시 실행 환경을 만든 동작 검증은 하지 않았다.

### implementation-review-03 — simplicity Low advisory가 Hard Rule을 통과할 수 없음 [수정 필요]

- 기준: 2, 4. 적용 runtime: Claude, Codex 공통 reference.
- 위치: [Claude reference](../../../.claude/skills/implementation-review/references/simplicity-contract.md) 25–26, 55–56, 69–71줄. [Codex reference](../../../plugins/sdd-skills-codex/skills/implementation-review/references/simplicity-contract.md) 동일 줄.
- 원문 A: “동작 변화 없이 더 단순한 동등 형태를 **구체적으로 제시하지 못하면 finding을 내지 않는다.**”
- 원문 B: “**Low (advisory)**: **주관적 취향** — naming 호불호처럼 동작-불변 동등 형태를 객관 증거로 제시할 수 없는 것.”
- 원문 C: “후보 finding마다 Hard Rule 4를 적용한다.”
- 문제 상황: naming 호불호처럼 reference가 직접 Low 예시로 든 후보를 얻었다. 모든 후보에 적용하는 Hard Rule은 더 단순한 동등 형태를 제시하도록 요구하지만 Low는 그 객관 근거가 없는 부류다. naming은 정의된 네 차원에도 별도 포함되지 않아 차원 한정 규칙과 경계가 맞지 않는다.
- 예상 영향: 같은 후보를 Low로 반환할지 아예 폐기할지 문면에 따라 갈린다. `implementation`과 `pr-review`는 simplicity Low advisory를 소비하는데 생산 규칙에서는 이 부류가 막혀 있다.
- 최소 수정안: 기존 global spec의 “falsifiable-only gating”을 따라 Medium+에 객관적 동등 형태 증명을 요구하고, Low는 기존 차원 안의 주관적 advisory로만 별도 허용한다. 네 차원 밖 naming 예시는 제거하거나 범위 내 예시로 바꾼다. Low까지 전부 제거하려면 현행 spec의 advisory 정책 변경이므로 별도 결정이 필요하다.
- 유지할 계약: Medium+는 구체적이고 반증 가능한 위반만 허용한다. Low는 비게이팅이며 네 차원 밖 새 리뷰 렌즈를 추가하지 않는다.
- 소유자: `implementation-review/references/simplicity-contract.md`. cross-skill 소비자: `pr-review`, `implementation`. 두 소비자에 서로 다른 falsifiability 규칙을 복제하지 않는다.
- 검증 상태: reference 두 파일은 byte-identical(diff exit 0). 소비자의 Low 처리와 global spec의 falsifiable-only gating 대조 완료. 실제 Low 발생률은 미측정.

### implementation-review-04 — 복구 불가능한 절차 AC와 오류 종료 계약의 충돌 [수정 필요]

- 기준: 2, 5. 적용 runtime: Claude, Codex. schema blocker 사례는 Codex.
- 위치: [Claude SKILL](../../../.claude/skills/implementation-review/SKILL.md) 19–25, 99줄. [Codex SKILL](../../../plugins/sdd-skills-codex/skills/implementation-review/SKILL.md) 17–23, 33, 144줄.
- 원문 A: “미충족 항목은 해당 단계로 돌아가 수정한다.”
- 원문 B: “AC1: 실행 순서를 지켰다 — simplicity spawn을 먼저 띄우고”
- 원문 C: “어느 lifecycle contract도 완전하지 않거나 둘 중 하나로 확정할 수 없으면 spawn하지 않고 **schema blocker**를 보고한 뒤, correctness 직접 리뷰만 수행하고 누락 렌즈를 명시한다.”
- 문제 상황: Codex active schema가 mandatory spawn의 lifecycle 조건을 만족하지 않는다. Adapter와 AC5에 따라 correctness 보고와 누락 설명을 완성해도, AC1의 선행 spawn은 충족할 수 없다. 이미 correctness를 먼저 시작한 순서 위반도 뒤늦은 spawn으로 과거의 순서를 바꿀 수 없다.
- 예상 영향: 정해진 degraded report로 종료하라는 계약과 AC 미충족 단계로 돌아가라는 계약이 동시에 적용된다. 환경 변화 없는 재시도 또는 실제로 충족하지 않은 절차 AC의 완료 표기로 이어질 수 있다.
- 최소 수정안: 자체 검증에서 산출물 누락처럼 복구 가능한 미충족만 보완한다. schema blocker·과거 순서/권한 위반은 재실행으로 감추지 않고 미충족 사실과 영향, 누락 렌즈를 반환한 뒤 종료한다. AC1에는 정상 dispatch 경로의 조건부 적용을 명시한다. 재실행은 blocker 해소 또는 새 호출로 분리한다.
- 유지할 계약: AC 자체 검증을 생략하지 않는다. mandatory dispatch를 임의 inline으로 대체하지 않으며, reviewer는 새 gate를 스스로 호출하지 않는다. producer의 최대 두 번 gate 정책도 유지한다.
- 소유자: `implementation-review` AC/Error Handling. **spec 결정 필요**: [global spec](../../../_sdd/spec/main.md) 92줄도 모든 미충족 항목의 단계 복귀를 일반 계약으로 서술하므로, 복구 가능한 누락과 이미 발생한 위반의 구별을 spec 소유자와 함께 명확히 해야 한다.
- 검증 상태: 정상/오류 분기의 논리 대조 완료. 재시도 루프가 실제 발생했다는 관측은 없다.

## 런타임 차이와 의존성

- Claude는 `Agent(general-purpose)`와 모델 인자를, Codex는 active schema에 맞춘 mailbox 또는 legacy target/close lifecycle과 분리 model/effort 인자를 사용한다. 도구 표기 차이 자체는 정상적인 adapter 차이다.
- Codex의 active schema 검사·없는 lifecycle 도구 검색 금지·선택적 `agent_type`·framed payload는 명시돼 있다. 현재 활성 도구에는 mailbox형 필드가 있지만 이번 작업은 리뷰 스킬 실행이 아니므로 dispatch하지 않았다. 모델/effort 지원의 영구 가용성이나 실제 override 성공 여부도 판정하지 않았다.
- 직접 읽은 문서: 양 runtime `implementation-review/SKILL.md` 전문, 양 runtime `references/simplicity-contract.md` 전문(동일성 비교), `AGENTS.md`, `_sdd/spec/main.md`, `_sdd/env.md`, 공통 리뷰 기준.
- 직접 이웃 대조: Claude `implementation/SKILL.md` 마감 3의 gate/fix/Low 정책(136–143줄), Claude `pr-review/SKILL.md` PR Review Input 및 reference 소비·Low 정책(32–41, 80–86, 149–151줄). `implementation`의 RED→GREEN 전체 실행 규약 및 `pr-review` 전체 리뷰 절차는 이번 담당 범위 밖이다.
- 미검토: `spec-sync` 전체 본문, 소비 저장소의 실제 env/테스트, 설치된 plugin에서의 동작, legacy runtime 실물. 이 범위를 근거로 새 결함을 주장하지 않았다.

## 권장 처리 순서와 검증

1. 변경 집합과 env fallback을 양 runtime 같은 의미로 수정한다. staged-only·untracked-only·mixed 상태와 env 없는 명시적 fast check 사례에서 실제 리뷰 대상 및 AC verdict를 확인한다.
2. simplicity reference에서 gating과 advisory 조건을 분리하고 두 배포 사본의 동일성을 확인한다. 객관적 단순화·범위 내 주관적 advisory·차원 밖 naming 후보를 입력해 각각 Medium/Low/제외 경계가 유지되는지 확인한다.
3. spec 결정 후 복구 가능한 누락과 schema blocker/과거 위반의 종료 경계를 맞춘다. incomplete schema 사례에서 correctness와 누락 렌즈만 반환하고 자동 재spawn·완료 위조가 없는지 확인한다.

이번 리뷰에서는 스킬을 실행하거나 수정하지 않았다. 검증 시에는 검토할 본문이 실제 로드된 설치본인지 먼저 확인하고, 표적 사례별 실행 결과를 수집해야 한다. 문서 확인만으로 모델 행동 개선이나 시간 절감을 주장하지 않는다.
