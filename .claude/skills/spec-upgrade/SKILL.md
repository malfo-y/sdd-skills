---
name: spec-upgrade
description: "Use this skill to review an existing SDD spec and bring it up to the current spec model: audit spec quality and code-to-spec drift (review only, no edits), rewrite or split an overlong spec, migrate an old-format spec, and refresh the AGENTS.md harness and hooks. Triggered by \"spec-upgrade\", \"upgrade spec\", \"migrate spec format\", \"modernize spec structure\", \"spec-review\", \"review spec\", \"spec drift check\", \"verify spec accuracy\", \"audit spec quality\", \"spec-rewrite\", \"rewrite spec\", \"refactor spec\", \"simplify spec\", \"split spec into files\", \"clean up spec\", \"스펙 업그레이드\", \"스펙 변환\", \"스펙 마이그레이션\", \"스펙 리뷰\", \"스펙 검토\", \"스펙 드리프트 점검\", \"스펙 정리\", \"하네스 갱신\". Not for reflecting a code change in the spec (that is sdd-orchestrator's spec-sync) and not for writing the first spec (that is spec-create)."
---

# spec-upgrade

이미 있는 `_sdd/spec/`을 점검하고, 현재 SDD spec 모델에 맞게 고친다. 점검만 요청받으면 파일을 고치지 않는다. 이 스킬이 정하는 것은 판단 기준과 저장소 규약이다. 어디까지 읽고 얼마나 고칠지는 spec의 상태에 맞게 스스로 정한다.

## Acceptance Criteria

> 종료 전 `Final Check`대로 점검한다.

- [ ] AC1: 요청 범위를 `호출 범위`로 정했고, 점검만 하는 호출이면 spec과 하네스를 고치지 않았다.
- [ ] AC2: spec을 `판단 기준`의 4개 기준(`Thinness`, `Decision-bearing truth`, `Anti-duplication`, `Navigation + surface fit`)으로 읽었고, 발견마다 근거(`file:line`)가 있다. 근거가 약한 발견은 `UNTESTED`로 적었다.
- [ ] AC3: 고쳤다면 판단 근거가 되는 내용을 잃지 않았고, 없는 내용을 지어내지 않았고, 지우거나 줄인 것과 그 이유를 보고했다.
- [ ] AC4: 점검만 하는 호출이 아니면 `하네스 갱신`을 수행하고 runtime별 결과를 보고했다.

## 판단 기준

global spec은 저장소 전체의 판단 기준을 고정하는 얇은 문서다. 본문은 세 절이 중심이다: `배경 및 high-level concept`, `Scope / Non-goals / Guardrails`, `핵심 설계와 주요 결정`.

| 기준 | 묻는 것 |
|---|---|
| `Thinness` | 본문이 개념·경계·결정만 담는가 |
| `Decision-bearing truth` | 저장소 수준의 판단을 바꾸는 진술만 남아 있는가 |
| `Anti-duplication` | guide, README, 계획 파일, 코드에서 바로 보이는 내용을 복제하지 않는가 |
| `Navigation + surface fit` | 보조 정보가 더 맞는 자리에 있고, 독자가 다음에 볼 곳을 찾을 수 있는가 |

- **결함으로 보는 것**: 기능 단위의 사용법·계약·검증 상세가 본문에 있다. 전체 파일 목록이나 컴포넌트 카탈로그가 본문을 채운다. 낡은 경로나 깨진 참조가 독자를 잘못된 곳으로 보낸다. 저장소 전체 사실을 틀리게 적었다. 코드와 spec이 어긋난다.
- **결함으로 보지 않는 것**: 사용법·기대 결과 절이 없다. 참조 정보 절이 없다. code map이 없다. 독립된 계약·불변식·검증 표가 없다. 예전 형식의 절이 없다.
- **code map**: 진입점, 계약의 출처, 불변식이 모이는 곳, 확장 지점, 검증 지점만 `Strategic Code Map`으로 짧게 둔다. 길어지면 보조 문서로 뺀다.
- **대상**: `_sdd/spec/`이다. 계획 파일(`_sdd/drafts/`)의 검토는 `sdd-orchestrator`의 계획 리뷰가 한다. spec 본문에 섞인 실행 상세는 위 기준으로 걸러 계획 파일이나 guide로 내린다.

## 단계

### 1. 점검

`main.md`와 그것이 가리키는 보조 문서 전부, 그리고 코드와의 어긋남을 판정하는 데 필요한 만큼의 코드·테스트·README를 읽는다. `logs/`·`prev/` 같은 과거 기록은 현재 사실로 읽지 않는다. spec이 없으면 `spec-create`를 권하고 끝낸다.

- 발견마다 spec·코드·문서의 `file:line` 근거를 붙인다. 근거가 약하거나 추정이면 `UNTESTED`로 적고 심각도를 올리지 않는다.
- 접근하지 못했거나 끝까지 찾지 못한 것을 "없다"로 적지 않는다. 필요한 범위를 다 찾았고 한쪽에만 없을 때 누락으로 적는다.
- 심각도는 셋이다. `Critical`은 저장소 수준의 판단을 직접 틀리게 만드는 것(틀린 저장소 전체 사실, 핵심 동작의 어긋남), `Quality`는 4개 기준 위반과 중간 수준의 어긋남, `Improvements`는 가독성과 정리다.
- 결론은 하나로 적는다: spec을 고쳐야 한다, 고칠 것이 없다, 논의가 필요하다. 코드가 spec과 다르고 spec이 옳으면 spec을 고칠 일이 아니다. 구현 쪽 조치로 보고한다.

점검만 하는 호출이면 발견을 심각도 순으로 채팅에 보고하고 끝낸다. 사용자가 보고서 파일을 요청했을 때만 `_sdd/spec/logs/spec_review_report.md`에 쓴다. 점검만 하는 호출이 쓰는 파일은 이것뿐이다.

### 2. 고치기

고치기 직전에 `references/spec-format.md`를 읽는다. 목표 구조, compact와 full 중 고르는 기준, 예전 내용을 어디로 내리는지가 거기 있다. 결과 예시는 `examples/after-upgrade.md`다.

- 기존 파일 경로에서 고치고, 기존 spec의 언어를 따른다. 구현 코드는 고치지 않는다.
- 판단 근거(`Why`, `Source`, 인라인 citation, 코드 발췌의 출처 줄)는 남긴다. 지우거나 줄이는 내용은 이유와 함께 보고한다.
- 없는 내용을 지어내지 않는다. 비어 있는 중심 절은 코드·README·git history에 근거가 있을 때만 채우고, 근거가 없으면 비어 있다고 보고한다.
- 이력, 형식 이행 메모, 정리한 이유는 본문에 쓰지 않는다. `decision_log.md`에 새 entry로 덧붙이고 기존 entry는 고치지 않는다.
- 파일을 나누거나 문서 사이로 큰 덩어리를 옮기는 변경은, 고치기 전에 무엇을 어디로 옮기는지 `_sdd/spec/logs/spec-rewrite-plan.md`에 쓰고 사용자 확인을 받는다. 무인 실행이면 확인 없이 진행하고 그 사실을 보고한다.
- 여러 파일로 나눌 때의 축: 독립된 기능이나 endpoint가 여럿이면 domain(`auth.md`, `payments.md`), 기능은 하나에 가깝고 저장소가 크면 topic(`architecture.md`, `data-conventions.md`). 새 파일은 `main.md` 인덱스에 링크한다.

### 3. 하네스 갱신

점검만 하는 호출이 아니면, spec에 고칠 내용이 없었더라도 이 절을 수행한다. 병합은 멱등이다. 점검만 하는 호출이면 수행하지 않고, 하네스가 없거나 낡았으면 그 사실만 보고한다.

작업 하네스(`AGENTS.md`)가 하네스 템플릿(`references/agents-harness-template.md`) 기준으로 존재하도록 SDD-HARNESS 마커 기반 멱등 병합을 적용한다.

> **하네스 블록은 항상 verbatim 복사다.** 아래 병합 규칙의 '마커 블록'은 매번 `references/agents-harness-template.md`를 **Read**해 `SDD-HARNESS:START`~`SDD-HARNESS:END`를 **글자 그대로 복사**한 것이다(상단 관리용 주석만 제외). repo 변수 슬롯만 치환하고, reference가 명시한 test/lint 부재 시 조건부 삭제만 허용한다. §5의 날짜·제목·모델명 등 향후 work-log 작성용 슬롯은 그대로 둔다. 그 외 어떤 줄도 추가·삭제·재배열·요약하지 않는다. 기억이나 이 SKILL 본문으로 **재구성하지 않는다**. 재구성하면 템플릿 변경(새 §·경고 줄 등)이 산출물에서 빠진다.

`AGENTS.md`:

- **없음** → 위 복사·치환 규칙으로 새로 쓴다.
- **있음(마커 없음)** → 마커 블록을 파일 **맨 위에 prepend**한다.
- **마커 블록 있음** → **그 마커 블록만 교체**한다. 다시 실행해도 블록이 겹쳐 쌓이지 않는다.

`CLAUDE.md`: 없으면 아래 한 줄 포인터를 SDD-HARNESS 마커 블록으로 감싸 만든다. 있으면 그 마커 포인터 블록을 맨 위에 prepend하고, 마커 블록이 이미 있으면 그 블록만 교체한다. 포인터 본문은 `> 이 repo의 작업 하네스는 \`AGENTS.md\` 단일 소스다. 작업 전 \`AGENTS.md\`를 먼저 읽는다.`이며 `spec-create`와 같다.

**보존/흡수 규칙** (`AGENTS.md`·`CLAUDE.md` 공통): 마커 밖 원문은 보존한다. 유일한 제거 예외는 **과거 SDD 부트스트랩 생성물로 식별되고 내용이 하네스에 전부 흡수된 중복 블록**이다. `## SDD란`이라는 제목이나 테스트/커밋 규칙의 중복만으로는 지우지 않는다. 출처·경계가 불명확하거나 사용자 고유 수정이 섞였으면 원문을 보존하고 남은 중복을 보고한다. 사용자 내용 삭제가 이미 승인된 범위에 없으면 승인을 받는다. legacy `## SDD란` 블록은 새로 만들지 않는다.

`.gitignore`: 커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`·`drafts/`·`work_log/`다. 나머지 process artifact 디렉터리는 커밋하지 않으므로 아래 `SDD-WORKSPACE` 마커 블록을 멱등 병합한다. 파일이 없으면 만들고, 마커가 없으면 파일 끝에 덧붙이고, 마커 블록이 있으면 그 블록만 교체한다. 마커 밖 사용자 규칙은 건드리지 않는다.

```gitignore
# SDD-WORKSPACE:START — process artifact는 로컬 전용(커밋 제외)
_sdd/discussion/
_sdd/implementation/
_sdd/pipeline/
_sdd/pr/
# SDD-WORKSPACE:END
```

`_sdd/env.md`: 이 skill package의 `references/worker-model-defaults.md`를 **Read**하고 그 적용·확인·보고 규칙대로 만들거나 보강한다.

훅: 하네스를 병합하면 Claude Code와 Codex 등록을 함께 설치한다. 별도 opt-in이 아니다.

1. 이 skill package의 `references/hook-installation.md`를 **Read**하고 전부 적용한다.
2. Claude-only·Codex-only·예전 command/matcher 같은 부분 설치나 legacy 설치는 reference의 현재 두 runtime 정의로 보완한다. malformed 설정의 skip과 보존은 reference를 따른다.
3. reference의 `Verification and Report`로 멱등성을 검증하고 runtime별 결과를 알린다.

hook event·matcher·settings merge·runtime definition·trust 계약은 이 package의 reference를 따른다. `spec-create`가 설치돼 있다고 가정하거나 이 본문으로 fallback을 재구성하지 않는다.

### 4. 확인과 보고

- 링크와 파일 경로가 유효한가. `Strategic Code Map`의 경로가 현재 코드와 맞는가.
- 판단 근거가 사라지지 않았는가. 본문이 다시 두꺼워지지 않았는가.
- `AGENTS.md`의 하네스 마커 블록(§0~§5), `CLAUDE.md`의 포인터 마커 블록, `.gitignore`의 `SDD-WORKSPACE` 블록이 있는가.
- `_sdd/env.md`가 `references/worker-model-defaults.md`의 확인·보고 조건을 채우는가.
- 훅은 `references/hook-installation.md`의 `Verification and Report`대로 runtime별 등록·검증·acceptance 상태를 구분했는가.

보고에는 점검 결론과 발견, 고친 파일, global에 남긴 것과 밖으로 내린 것, 지우거나 줄인 것과 이유, 채우지 못한 절, 하네스 병합 결과(`AGENTS.md`·`CLAUDE.md`·`.gitignore`의 생성·prepend·교체 여부와 흡수한 legacy 블록), `env.md` 결과(`references/worker-model-defaults.md`의 `확인·보고` 규칙), 훅 설치 결과(`references/hook-installation.md`의 `Report` 계약)를 담는다.

## 호출 범위

| 요청 | 범위 |
|---|---|
| 점검·리뷰·drift 확인 ("review spec", "스펙 리뷰") | 1단계만 한다. spec과 하네스를 고치지 않는다. |
| 정리·재작성·분할·형식 이행 ("rewrite spec", "upgrade spec", "스펙 정리") | 1~4단계를 한다. |
| 하네스 갱신 ("하네스 갱신", "훅 다시 설치") | 3단계와 그 확인만 한다. spec 본문은 고치지 않는다. |

요청이 어느 쪽인지 분명하지 않으면 점검만 하고, 고칠지는 보고 끝에서 묻는다. 인자 없이 스킬 이름만 부른 호출도 여기에 든다.

## Final Check

수행한 범위에 해당하는 Acceptance Criteria를 한 번 점검한다. 보완할 수 있는 누락은 고친다. 훅의 skipped·partial 상태나 trust 대기는 `references/hook-installation.md`의 종료·보고 규칙을 따른다. 외부 입력이 필요한 나머지는 원문을 보존한 채 제한된 결과로 보고하고, 완료로 적지 않는다.
