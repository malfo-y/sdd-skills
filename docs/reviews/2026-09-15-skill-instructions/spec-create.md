# spec-create 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/spec-create/SKILL.md), [Codex](../../../plugins/sdd-skills-codex/skills/spec-create/SKILL.md)
- 판정 요약: 수정 필요 5 / 정리 후보 1 / 실행 검증 필요 1

## 역할과 유지할 계약

요구사항·코드·기존 문서에서 thin global spec을 만들고, 필요한 경우 작업 하네스를 함께 부트스트랩한다. compact 기본값, source evidence에 따른 full 선택, runtime-local template 직접 읽기, 구현 코드 불변, 마커 멱등 병합과 사용자 내용 보존을 유지한다. 하네스 설치 시 양 runtime 훅을 함께 설치하며, 사용자 trust를 자동 승인하거나 user-global 설정을 수정하지 않는다. 검증 없이 완료 사실로 승격하지 않는다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | spec-create-01: 선택적 부트스트랩과 무조건 생성 지시의 조건이 다르다. spec-create-07: 단순 언급 트리거의 실제 라우팅을 확인해야 한다. |
| 2. 충돌과 우선순위 | spec-create-02: 허용 슬롯 목록에 실제 branch 슬롯이 없다. spec-create-03: 마커 밖 불변과 legacy 제거가 충돌한다. |
| 3. 확인·승인 경계 | spec-create-05: trust 승인 금지는 명확하지만 acceptance 보류가 완료 검사에 연결되지 않는다. 기존 설정 보존과 실제 trust 경계는 유지해야 한다. |
| 4. 중복과 소유권 | spec-create-06: canonical template의 원칙 수를 본문이 재소유해 낡았다. runtime 배포 mirror 자체는 결함이 아니다. |
| 5. 완료·복구 조건 | spec-create-04: malformed 설정 skip을 허용하지만 최종 검사는 양쪽 exact match를 요구한다. spec-create-05: 설치 검사와 runtime acceptance가 구별되지 않는다. |
| 6. 절차의 필요성 | 수정 필요 없음. template 선택·직접 읽기·멱등 확인은 구체적인 산출물 계약을 집행한다. 단계 수나 파일 길이만으로 비용 결함을 주장하지 않는다. |

## Findings

### spec-create-01 — 선택적 부트스트랩이 Hard Rules와 검증에서 무조건 작업이 됨 [수정 필요]

- 기준: 1, 2, 6. Runtime: Claude/Codex 공통.
- 근거: [Claude SKILL](../../../.claude/skills/spec-create/SKILL.md), [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-create/SKILL.md), 동일 줄 24, 73, 151, 265–268. 원문: “필요한 경우에만”, “`AGENTS.md`, `CLAUDE.md`는 없을 때 SDD-HARNESS 마커 블록으로 생성하고”, “`AGENTS.md`가 하네스 §0~§5 슬롯을 채워 생성/병합되었고”.
- 문제 상황: 기존 spec만 갱신하면 되고 bootstrap 필요가 없는 저장소에서도 Hard Rule 4와 Step 5를 문자 그대로 충족하려면 하네스를 생성/병합해야 한다. 이 작업은 Step 3e의 양 runtime 훅 설치도 연쇄 발동한다.
- 예상 영향: 조건부 산출물이 사실상 필수가 되거나, 필요한 spec 작성만 끝낸 실행이 검증 실패로 되돌아간다. 실제 발생 여부는 미관측이다.
- 최소 수정안: Hard Rule 4와 Step 5의 bootstrap 검사에 “Step 3에서 생성/보강 대상으로 선택한 경우”를 붙이고 미선택 항목은 비대상으로 검증한다. 선택된 하네스에 대한 훅 설치 의무는 그대로 둔다.
- 유지할 계약: bootstrap 최소 범위, 하네스↔훅 동일 trigger, AC 자체 검증. spec 결정 필요 없음.
- 소유자: spec-create SKILL 양 runtime.
- 검증 상태: 문면 대조 완료, 실행 미검증.

### spec-create-02 — 치환 허용 목록에서 실제 branch 슬롯이 빠짐 [수정 필요]

- 기준: 2, 4, 5. Runtime: Claude/Codex 공통.
- 근거: [Claude SKILL](../../../.claude/skills/spec-create/SKILL.md), [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-create/SKILL.md), 동일 줄 161–169. 원문: “그다음 아래 `<…>` 꺾쇠 슬롯만 repo 맥락으로 치환한다”. [하네스 template](../../../.claude/skills/spec-create/references/agents-harness-template.md) 줄 24: “`<브랜치 규칙, 예: main에서 feature/fix/exp/... 브랜치>`”.
- 문제 상황: 실제 template은 branch 규칙 슬롯을 포함하지만 SKILL의 닫힌 허용 목록은 repo-name, test, lint, commit/PR, spec 절만 나열한다. 목록을 따르면 branch placeholder가 남고, 채우면 “아래 … 슬롯만”을 벗어난다.
- 예상 영향: 소비 repo에 미치환 행동 규칙이 배포되거나 실행자가 임의로 예외를 정한다.
- 최소 수정안: 허용 치환 목록에 branch 슬롯을 추가한다. 장기적으로 슬롯 목록을 template 한 곳이 소유하게 바꾸려면 work-log 형식의 `<제목>` 같은 문자까지 잘못 치환하지 않도록 bootstrap 변수 범위를 명시해야 한다.
- 유지할 계약: 비슬롯 줄 verbatim 보존, repo branch 규칙 반영. spec 결정 필요 없음.
- 소유자: spec-create SKILL 양 runtime. template 수정은 불필요하다.
- 검증 상태: 실제 template 슬롯과 허용 목록 정적 대조 완료, 생성 실행 미검증.

### spec-create-03 — 마커 밖 legacy 블록을 보존하면서 제거해야 함 [수정 필요]

- 기준: 2, 3, 5. Runtime: Claude/Codex 공통.
- 근거: [Claude SKILL](../../../.claude/skills/spec-create/SKILL.md), [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-create/SKILL.md), 동일 줄 191, 266. 원문: “그 마커 블록만 교체”, “마커 밖 내용은 건드리지 않는다”, “하네스와 별개의 중복 `## SDD란` 블록이 남지 않았는가”.
- 문제 상황: 파일에 SDD-HARNESS 마커와 마커 밖 legacy `## SDD란` 블록이 함께 있다. Step 3c는 legacy를 건드릴 수 없게 하지만 AC와 Step 5는 제거를 요구한다. 마커 없는 경로에는 legacy 예외가 쓰여 있으나 이 경로에는 없다.
- 예상 영향: 보존 위반 또는 AC 미충족 중 하나를 고르게 된다. 제목만으로 사용자 고유 내용을 legacy로 오인해 삭제할 위험도 있어 무제한 삭제 예외는 적절하지 않다.
- 최소 수정안: 마커 밖 보존 원칙의 유일 예외로 “과거 SDD 부트스트랩 생성물임이 확인되고 하네스로 내용이 흡수된 중복 블록”을 명시한다. 출처나 경계가 불확실하면 원문을 보존하고 잔여 항목으로 보고한다.
- 유지할 계약: 사용자 고유 내용 보존, 확인된 legacy 흡수, 멱등성, 파괴적 동작의 승인 경계. spec 결정 필요 없음.
- 소유자: spec-create SKILL. [spec-upgrade](../../../.claude/skills/spec-upgrade/SKILL.md) 줄 142–150에도 같은 보존/흡수 경계가 있어 공동 정합 확인이 필요하다.
- 검증 상태: 두 입력 조건의 지시 대조 완료, 실제 병합 미검증.

### spec-create-04 — malformed 설정을 skip한 정상 복구 경로가 완료 검사에서 닫히지 않음 [수정 필요]

- 기준: 2, 5. Runtime: 설치 대상 양 runtime; 호출 runtime과 무관.
- 근거: [hook-installation canonical](../../../.claude/skills/spec-create/references/hook-installation.md) 줄 63: “preserve its bytes and skip registration for that runtime”; 줄 152: “Each runtime's SDD hook groups exactly match its complete `Runtime Definition`.” [Claude SKILL](../../../.claude/skills/spec-create/SKILL.md), [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-create/SKILL.md) 줄 269, 306: “`Verify` checklist를 모두 만족”, “미충족 항목이 있으면 해당 단계로 돌아가 수정한다”.
- 문제 상황: `.codex/hooks.json`이 malformed이고 Claude 설정은 정상이다. reference대로 Codex bytes를 보존하고 Claude 등록을 완료해 partial 보고를 준비해도 모든 runtime의 canonical group exact match 검사는 만족할 수 없다.
- 예상 영향: 같은 손상 파일을 불필요하게 재시도하거나, 완료를 맞추려고 사용자 설정을 복구/덮어쓰는 잘못된 경로가 생긴다. 후자는 현재 보존 계약상 금지다.
- 최소 수정안: Verify를 runtime별 “등록 성공이면 exact match / skipped이면 bytes 보존·원인 보고”로 분기하고, SKILL에 외부 복구가 필요한 partial 상태는 재시도 없이 미완료 항목을 보고하고 종료한다고 연결한다. partial을 완전 설치로 표시하지 않는다.
- 유지할 계약: 한쪽 실패가 반대쪽 설치를 막지 않음, 손상 bytes 보존, 사용자 설정 보존, AC 정직성. spec 결정 필요 없음.
- 소유자: hook-installation authoring canonical은 spec-create. spec-create/spec-upgrade의 4개 reference 배포 mirror와 두 caller의 마감 문구에 전파한다.
- 검증 상태: malformed 복구 규칙과 완료 검사 문면 대조 완료, 설정 변경/실행 미검증.

### spec-create-05 — trust 안내가 acceptance 미완료 상태로 연결되지 않음 [수정 필요]

- 기준: 3, 5. Runtime: Codex hook acceptance; Claude에서 호출해도 Codex 등록 대상에 적용.
- 근거: [global spec](../../../_sdd/spec/main.md) 줄 67: “사용자가 `/hooks`에서 검토·신뢰하기 전에 acceptance 완료로 보지 않으며”. [hook-installation canonical](../../../.claude/skills/spec-create/references/hook-installation.md) 줄 145: “Do not approve trust automatically”; 줄 151–154의 Verify는 bytes·정의·보존·멱등만 검사하고, 줄 168–171은 trust 요구사항을 notices로 보고한다. [Claude SKILL](../../../.claude/skills/spec-create/SKILL.md), [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-create/SKILL.md) 줄 269는 이 Verify checklist의 만족을 검사한다.
- 문제 상황: 새 Codex project definition을 생성해 구조 검사를 모두 통과했으나 사용자가 아직 `/hooks`에서 신뢰하지 않았다. local reference는 요구사항을 안내하도록 하지만 acceptance를 pending으로 남기는 판정·보고 필드가 없다.
- 예상 영향: 설치 파일은 준비됐지만 실행 승인 전인 상태를 hook acceptance 완료로 보고할 수 있다. 자동 trust 승인 금지는 충분히 명시돼 있으며 이를 완화할 이유는 없다.
- 최소 수정안: 설치 결과와 runtime acceptance를 분리하고, 신뢰 증거가 없으면 `pending user trust`로 보고하며 완료로 승격하지 않는 규칙을 Verify/Report에 연결한다. 문서·등록 준비와 안전한 검증을 모두 끝낸 후 사용자의 `/hooks` 검토를 남은 행동으로 안내한다.
- 유지할 계약: trust 자동 승인·user-global 수정·bypass 금지, 구조 parity만으로 acceptance 완료 금지. 기존 spec 결정의 집행 보완이며 spec 결정 필요 없음.
- 소유자: hook-installation authoring canonical(spec-create), spec-upgrade 포함 4개 local 배포 mirror.
- 검증 상태: global spec과 local 완료 계약 대조 완료. Codex API/버전 지원이나 실제 lifecycle 발동은 조사·판정하지 않았다.

### spec-create-06 — canonical template의 원칙 수를 잘못 재서술함 [정리 후보]

- 기준: 4. Runtime: Claude/Codex 공통.
- 근거: [Claude SKILL](../../../.claude/skills/spec-create/SKILL.md), [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-create/SKILL.md), 동일 줄 171: “§0 작업 원칙 4개는 영어 원문 그대로 유지한다.” [하네스 template](../../../.claude/skills/spec-create/references/agents-harness-template.md) 줄 11–13에는 3개만 있다.
- 문제 상황: template을 verbatim 복사하면 3개인데 후속 지시가 4개를 요구한다. 다만 실제 원문 복사 지시가 충분히 강해 네 번째 원칙이 생성된다고 단정할 근거는 없다.
- 예상 영향: 불필요한 해석 혼선. 행동·성능 저하 실측 주장은 하지 않는다.
- 최소 수정안: “§0 작업 원칙은 영어 원문 그대로 유지한다”로 숫자를 삭제한다.
- 유지할 계약: 영어 원문·순서·내용 불변, canonical template 단일 소유. spec 결정 필요 없음.
- 소유자: spec-create SKILL 양 runtime.
- 검증 상태: 수량 대조 완료, 동등한 최소 문구 제안; 행동 미검증.

### spec-create-07 — `_sdd` 단순 언급의 생성 스킬 라우팅 여부 [실행 검증 필요]

- 기준: 1. Runtime: Claude/Codex 공통.
- 근거: [Claude SKILL](../../../.claude/skills/spec-create/SKILL.md), [Codex SKILL](../../../plugins/sdd-skills-codex/skills/spec-create/SKILL.md), 동일 줄 3: “or mentions "_sdd" directory, specification documents, or project documentation needs.”
- 문제 상황: “`_sdd` 디렉터리 역할만 설명해 줘”처럼 읽기 요청에도 description의 문면상 trigger가 성립한다. 실제 스킬 선택과 mutation까지 이어지는지는 호출 runtime과 상위 지시 해석에 달려 있어 이번 정적 리뷰로 확정할 수 없다.
- 예상 영향: read-only 질문에 생성 workflow가 불필요하게 선택될 가능성.
- 최소 수정안: 실행에서 오라우팅이 확인되면 description을 global spec 생성·초기화 의도로 한정하고 단순 언급·설명·기존 spec review는 제외한다.
- 유지할 계약: 명시적인 spec-create 호출과 생성 요청은 정상 수신, 현재 사용자 요청 우선.
- 소유자: spec-create description 양 runtime. 다른 spec lifecycle skill의 trigger 변경은 이 finding의 범위 밖이다.
- 검증 상태: 위험 가설만 확인; 실제 routing/파일 변경 미검증.

## 런타임 차이와 의존성

- 두 `SKILL.md`는 byte-identical이다. 두 package의 디렉터리 비교에서 compact/full template의 `/guide-create`와 `$guide-create` 호출 token만 달랐으며 정당한 runtime 차이다. hook reference·harness template·hook script bytes와 examples는 해당 runtime 짝과 동일했다.
- 전문을 읽은 직접 reference: `references/agents-harness-template.md`, `references/hook-installation.md`, `references/template-compact.md`, `references/template-full.md`. Codex 짝은 파일 비교와 template diff로 대조했다.
- 직접 이웃 검토: spec-upgrade의 Harness Merge/Hook Assets와 해당 완료 검사 부분. 같은 legacy 경계와 hook canonical 연결 확인에 한정했다.
- 미검토 범위: `examples/*.md` 내용 품질, `references/hooks/*.sh` 내부 구현·보안·실행 동작, 실제 runtime hook API와 버전 지원, spec-upgrade의 나머지 절. scripts/examples의 runtime parity 비교는 내부 동작 검토를 뜻하지 않는다.
- spec-create-04/05는 공용 reference 한 곳에서 고친 뒤 4개 package에 배포할 항목이다. 같은 문제를 spec-upgrade의 독립 수정으로 중복 집계하지 않는 편이 적절하다.

## 권장 처리 순서와 검증

1. spec-create-02/06의 슬롯·원칙 수 참조를 바로잡고 실제 template과 대조한다.
2. spec-create-01/03의 조건을 명시한다. 격리 fixture에서 bootstrap 비대상, 기존 마커+확인된 legacy, 기존 마커+사용자 고유 동명 섹션을 각각 대조한다. 사용자 내용 보존과 두 번째 실행의 무변경을 확인한다.
3. spec-create-04/05를 공용 hook reference에서 고치고 4미러에 전파한다. 한쪽 malformed JSON fixture에서 손상 bytes 보존·반대쪽 설치·partial 종료를 확인하고, trust 전에는 acceptance pending인지 검사한다. 실제 사용자 trust는 자동화하지 않는다.
4. 새 검증 세션에서 read-only `_sdd` 설명 요청과 명시적 spec 생성 요청을 비교해 spec-create-07을 판정한다. 이 리뷰에서는 스킬 실제 실행·설치·trust 변경을 하지 않았다.
