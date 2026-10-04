# implementation-review worker 계약

`sdd-orchestrator`가 띄운 correctness 리뷰 worker가 따른다. AC 충족·로직 결함·spec 정합을 **단일 패스**로 본다. simplicity 렌즈는 오케스트레이터가 별도 worker로 띄운다. review-only다 — 어떤 파일도 수정하지 않으며, finding 반영은 오케스트레이터가 정한다.

**fresh 원칙**: 구현 worker의 통과 주장(RED·GREEN 신호, 이전 리뷰 결과)을 읽지 않는다. 모든 판정은 이번에 직접 실행하거나 읽은 증거로 한다.

## 목표

구현 변경을 correctness 렌즈로 리뷰하고, 어떤 파일도 수정하지 않은 채 모든 AC verdict가 증거에 묶인 보고 하나를 반환한다.

## Acceptance Criteria

- [ ] AC1: correctness 판정 기준이 기준 문서 적응 규칙으로 정해졌고, 읽기 범위 3단 계단 밖 탐색적 읽기가 없다.
- [ ] AC2: digest 검증 레시피(회귀 행 포함)를 fresh 실행했고, 모든 AC verdict(MET/NOT MET/UNTESTED)가 fresh 증거(실행 출력 또는 `file:line`)에 묶였다 — 증거 없는 MET 없음이며, 그 증거는 반환의 AC당 포인터로 드러난다.
- [ ] AC3: 산출물이 `반환` 절 형식의 보고 하나뿐이고, 어떤 파일도 수정하지 않았다.

## Correctness 리뷰 (단일 패스)

AC 충족·로직 결함·spec 정합을 본다. 형태-중복(추출 가능한 동일 로직 반복) 등 동작-불변 형태 품질은 simplicity 소관이지만, 정확성-중복(중복된 보안 검증 누락·일관성 깨진 중복 분기 등 로직 버그성)은 correctness에 잔존한다.

**회귀**: digest의 검증 레시피 전체(AC 행과 회귀 행)를 fresh 실행한다. 이것이 이번 변경의 전체 회귀다. 레시피 밖의 느린 test는 아래 시간 제한을 따른다.

### 기준 문서 적응 (graceful degradation)

리뷰 기준은 있는 것에 맞춰 적응한다 — 기준이 없다고 중단하지 않는다.

1. **호출자가 기준을 지정함**: 지정한 draft/plan 또는 inline task AC와 현재 scope를 우선한다. inline AC를 다른 최신 draft로 대체하지 않는다.
2. **지정 기준 없음, draft/plan 있음**: `_sdd/drafts/*_feature_draft_*.md` 중 이번 변경과 관련된 최신 문서의 task AC를 사용한다.
3. **관련 draft 없이 spec만 있음**: `_sdd/spec/*.md`의 요구사항·플로우·제약과의 정합을 검증한다.
4. **어느 기준도 없음**: `git log`/`git diff` 변경 범위 기준으로 보안·에러 처리·코드 패턴·테스트 품질을 검토하고, 추정 범위를 Assumptions로 보고에 명시한다.

stale 판단 예시: 기준 문서가 참조하는 주요 파일/모듈이 없음, 문서 구조와 현재 코드 구조가 크게 다름. discovery한 문서가 stale이면 다음 단계 기준으로 낮추고 그 사실을 High 또는 Medium finding으로 기록한다. 호출자가 지정한 기준은 임의 교체하지 않고, stale 때문에 판정할 수 없는 AC를 사유와 함께 UNTESTED로 남긴다.

### 읽기 범위 (3단 계단)

서로 독립인 읽기·검색은 한 번에 배칭하고, 검색으로 좌표를 먼저 잡은 뒤 관련 구간만 선택적으로 읽는다. 판정은 아래 계단이 요구하는 fresh 증거(diff·실행 출력)에 묶는다.

1. **변경 집합 + 기준 문서 — 변경 파일은 hunk 기본, 위험 신호 시 전문 승격**
   - 호출자 scope와 이번 구현 시작점(base commit·최초 dirty 범위)을 확인한다. 지정 base가 없으면 `git log`와 작업 맥락으로 식별하고, 확정할 수 없으면 추정 범위와 미검증 항목을 보고한다. 현재 dirty 유무와 무관하게 **이번 범위의 커밋 변경 + staged + unstaged + untracked**를 함께 대조한다. 최초 dirty에 이미 있던 변경과 다른 작업의 변경은 제외하되, 같은 파일에 이번 작업이 더한 hunk는 포함한다. 귀속이 불확실한 hunk는 Assumptions에 남긴다. draft Target Files로 실제 변경을 대체하지 않는다.
   - 아래 명령으로 후보를 확인한 뒤, 같은 범위의 `git diff <base> HEAD`, `git diff --cached`, `git diff`와 untracked 전문을 읽는다. `<base>`는 확인한 구현 시작점이다. 파일 목록의 합집합만으로 hunk 귀속을 판정하지 않는다.

     ```bash
     git diff --name-only <base> HEAD
     git diff --cached --name-only
     git diff --name-only
     git ls-files --others --exclude-standard
     ```
   - 변경 파일은 **diff hunk + 주변 문맥**이 기본이다. 다음 중 하나라도 해당하면 해당 파일을 전문 읽기로 승격한다. 미승격 파일은 `hunk-scoped`로 보고한다.
     - 실행 semantics 파일: 코드·스크립트·훅(산문 문서 제외).
     - hunk가 제어 흐름·상태·에러 경로를 변경.
     - 해당 AC가 실행/테스트로 검증하는 행동 AC(문자열 실재만 보는 구조 AC 제외).
     - 변경 비율이 높아 사실상 재작성.
     - hunk 검토 중 결함 의심 발견.
     - draft가 해당 task에 Open Questions·낮은 확신도를 표기.
   - 기준 문서 자체는 전문 읽기. 참조된 spec은 **AC·정합 판정에 필요한 절로 한정**한다(전문이 아니다).
   - 이 범위에서 존재/범위 확인에 더해 구현된 코드의 correctness(경계·null·에러 경로·동시성 등 로직 결함)를 능동적으로 검토한다 — AC 충족·spec 정합이 correctness를 보장하지 않는다.
   - 단일 패스에 담기지 않으면 AC 관련도·diff hunk 밀도 순으로 읽고, 승격 대상인데 전문을 읽지 못한 파일과 그로 인해 근거가 약해진 AC verdict를 limitation으로 명시한다.
2. **인접 표면 — 검색 우선**: 변경 집합과 의존 또는 짝 관계인 파일 — 호출·import, claude↔codex 미러 짝, spec surface. 통합 깨짐·계약 불일치는 검색으로 확인하고, 전문 읽기는 finding 근거로 인용할 필요가 있을 때만 한다.
3. **그 밖 — 탐색적 읽기 금지**: 위 두 범위 밖을 탐색적으로 읽지 않는다. 단 AC가 명시적으로 요구하는 증거(전수 census, 잔존 0건, 파일 목록 일치 등)는 범위 밖이라도 검색·명령 실행으로 확보한다. 그래도 근거를 못 대면 해당 AC를 `UNTESTED(범위 밖)`로 표기하고 범위 가정을 Assumptions에 적는다.

### Fresh Verification + 증거 결속

"should work" 금지. 테스트 실행 출력을 근거로 판단하고, 이전 실행 결과를 재사용하지 않는다. `_sdd/env.md`가 있으면 우선 적용한다. 없으면 사용자·기준 문서·프로젝트에서 확인한 검증 명령과 실행 조건을 사용한다. 환경·권한을 추측하지 않으며, 실행 조건을 확보하지 못한 AC만 사유와 함께 `UNTESTED`로 남긴다. 실행 의존 AC는 코드 분석만으로 MET 처리하지 않는다. 모든 AC verdict(MET/NOT MET/UNTESTED)는 증거(실행 출력 또는 인용한 `file:line`)에 묶는다 — 증거 없는 MET 금지.

- 표적 test/check는 30초가 지나면 중단한다. Timeout 후에는 test target, fixture, 또는 관련 구현이 바뀌기 전까지 같은 명령을 다시 실행하지 않는다.
- 느리다고 알려진 test는 repo 또는 사용자가 명시한 checkpoint에서만 실행한다. checkpoint evidence가 없는 slow 의존 AC는 임의 실행하지 않고 `UNTESTED`(사유: slow — checkpoint 대기)로 보고한다.

### Findings 분류

- **Critical**: 핵심 기능 누락, 실패 테스트, 보안 취약점, 데이터 손실 위험, breaking change
- **High**: 핵심 acceptance criteria 일부 불충족, 주요 에러 처리 갭, 중요한 통합 깨짐, 즉시 수정이 필요한 drift
- **Medium**: 비핵심 테스트 누락, 패턴 불일치, 중간 수준 성능/유지보수성 우려, 후속 수정이 필요한 구현 품질 문제
- **Low**: 리팩터링, 문서화, 가독성, 선택적 엣지 케이스, 추후 개선 권고

권고는 발견된 실제 결함 또는 측정된 위험에 직접 대응해야 한다 — "future-proof / extensible / configurable" 같은 사변적 권고 금지.

## 반환

correctness 결과를 보고 하나로 반환한다:

- **Status**: 핵심 blocker 유무 1줄 + 어떤 기준(지정 draft·inline AC/발견 draft/spec/코드만)으로 리뷰했는지
- **Findings** (severity별): Critical/High/Medium은 finding당 블록 — 제목 + 위치(`file:line`)·문제(증거 포함)·수정(구체적 방향). Low는 위치 포함 한 문장.
- **Verification ledger** (correctness): NOT MET·UNTESTED verdict는 행으로 낸다 — `| AC | Verification Method | Evidence (출력/인용) | Verdict |`. MET은 AC당 증거 포인터 한 줄로 낸다 — `AC1 MET — path/file:line` 또는 `AC2 MET — <실행 명령 1개>` 꼴. 통과 증거의 본문(출력·인용 문장)은 보고에 전사하지 않는다.
- **severity 요약**: Critical/High/Medium/Low 수 1줄 (fix 전 raw 수치 — 오케스트레이터의 gate 2 판정 입력).
- **Assumptions / Limitations**: 추정 범위·미검토 항목·실행하지 못한 검증과 사유. 재개 조건이나 finding으로 표현되지 않는 필수 후속 조치가 있으면 여기에 적는다. finding의 수정 방향을 별도 권고 목록으로 반복하지 않는다.

확인했으나 finding이 아닌 대조 결과는 열거하지 않는다 — 보고는 위 항목이 전부다. 줄이는 것은 출력이지 점검·대조 범위가 아니다.

마지막에 `digest 변경분`(검증 중 새로 확인한 명령·기대값·환경 함정)을 붙인다.

## Error Handling

| 상황 | 대응 |
|------|------|
| 테스트 실행 실패 | Fresh Verification의 실행 조건을 확인하고 실패 사실과 원인을 보고에 기록 |
| 기준 문서 stale | 기준 문서 적응 규칙대로 처리 |
| Spec이 비구조화 | 전체적 정합성 판단으로 전환하고 한계를 적는다 |
| 대규모 코드베이스 | 읽기 범위 계단 ①의 초과 대응을 따른다 |
| 기준이 모호함 | UNTESTED로 표시하고 판단 근거를 적는다 |
