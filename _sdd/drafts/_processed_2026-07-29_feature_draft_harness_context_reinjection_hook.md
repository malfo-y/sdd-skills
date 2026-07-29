# Feature Draft: 하네스 재주입 훅(harness-context.sh)을 하네스 자산으로 추가

> 규모 판정: 적격 — 신규 자산 1개 + 기존 훅 자산 계약의 "2개 → 3개" 확장이며, 변경 요소(자산 4벌 · SKILL.md 4벌 · dogfooding · docs 후행)와 task의 대응이 1:1로 눈검산된다. census형 신호가 있어 Part 2 마지막에 read-only 검증 task를 둔다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

compact·clear로 컨텍스트가 소실되면 `CLAUDE.md` 포인터("작업 전 `AGENTS.md`를 먼저 읽는다")만 재주입되고 하네스 본문은 사라진다. 포인터를 따라 읽을지는 모델 재량이라 실제로 누락된다. 이는 work log 규약이 산문만으로 안 지켜져 커밋 게이트를 도입한 것과 **같은 실패 모드**다 — 해소 수단도 같다: 실행 층으로 옮긴다.

- **하네스 훅 자산이 2개 → 3개로 확장된다.** 기존 `worklog-gate.sh`(PreToolUse)·`worklog-context.sh`(SessionStart 전 소스)에 `harness-context.sh`(SessionStart, `matcher: "clear|compact"`)가 더해진다. 세 스크립트는 하나의 설치 계약(스크립트 verbatim 복사 + `settings.json` 키 수준 멱등 병합) 아래 있으며, 하네스 설치와 동일 조건에 묶인다(별도 opt-in 아님).
- **새 contract — 하네스 재주입은 "읽으라는 지시"가 아니라 "내용 주입"이다.** `harness-context.sh`는 `AGENTS.md` 전문을 stdout으로 내보내 컨텍스트에 직접 넣는다. 지시 방식은 모델 재량이 남아 이번에 닫으려는 실패 모드를 그대로 재생산하며, 모델이 순순히 읽어도 Read 왕복으로 같은 분량이 들어오므로 비용 이점도 없다.
- **새 contract — 훅 자산 설치 지시는 work log 전용이 아니라 훅 자산 일반의 계약이다.** `spec-create` §3e와 `spec-upgrade` Step 6은 "work log 훅 자산" 한정에서 "훅 자산" 일반으로 넓어진다. 세 번째 스크립트를 위해 별도 절을 만들지 않는다 — `settings.json` 병합 규칙의 판정 주체가 둘로 갈리기 때문이다.
- **새 invariant — SessionStart 등록 형태는 스크립트별로 matcher가 다르다.** `worklog-context.sh`는 matcher 없음(전 소스), `harness-context.sh`는 `"clear|compact"`. 근거: `startup`은 `CLAUDE.md` 포인터를 보고 첫 턴에 읽는 것이 정상 동작이고 `resume`·`fork`는 컨텍스트가 복원되므로, "컨텍스트가 소실됐는데 포인터만 남는" 상황은 `clear`·`compact` 둘뿐이다.
- Codex 비대칭은 기존 두 훅과 동일하게 수용한다 — `.codex` 레인도 `.claude/hooks/`를 설치하지만 Codex 자신은 훅을 실행하지 않는다.

## 가정과 확신도 (구현 전 명시)

1. **matcher 문법은 Claude Code 2.1.220 실측 기준이다.** 바이너리에서 SessionStart의 `matcherMetadata`가 `{fieldToMatch: "source", values: ["startup","resume","clear","compact","fork"]}`이고, 매칭 함수 `BFy`가 패턴이 `/^[a-zA-Z0-9_|]+$/`이면 `|`로 split해 정확 일치 비교함을 확인했다. **이 문법을 지원하지 않는 버전에서는 훅이 오류 없이 조용히 미발동한다(무증상 실패).** 정적 근거만으로 계약을 닫지 않기 위해 Task 4에 런타임 관찰 AC를 둔다.
2. **주입 대상은 `AGENTS.md` 전문이며 크기는 repo마다 다르다.** 소비 repo에서 `spec-create`/`spec-upgrade`는 기존 `AGENTS.md`를 보존한 채 `SDD-HARNESS` 마커 블록을 맨 위에 prepend하므로 `AGENTS.md` ⊋ 하네스 블록이다. 그럼에도 마커 블록만 주입하지 않고 전문을 주입한다 — 마커 밖 내용은 그 repo가 직접 쓴 작업 규약이고, 재주입의 목적("작업 규약을 다시 보게 한다")에 정확히 해당한다. 마커 블록만 넣으면 SDD 자기 하네스는 살리고 그 repo 고유 규약은 버리는 셈이 된다. (이 repo는 `AGENTS.md` 전체가 마커 블록이라 dogfooding으로는 이 차이가 드러나지 않는다 — 근거를 dogfooding 환경에 기대지 않는다는 뜻으로 여기 기록한다.)

## Scope

- **In**: `references/hooks/harness-context.sh` 정본 신설 + 4벌 미러 / `spec-create` §3e·`spec-upgrade` Step 6의 훅 자산 계약 일반화(claude·codex 2벌씩) / 두 SKILL.md의 스크립트 개수 리터럴 census 갱신 / 이 repo dogfooding / `docs/SDD_CONCEPT.md` ko·en 후행 갱신
- **Out**:
  - 하네스 템플릿(`agents-harness-template.md`) 변경 — 훅의 리드 1줄이 "다시 읽지 말고 이대로 따른다"를 이미 전달한다. `AGENTS.md`에 같은 말을 또 적으면 주입 블록 안에서 메시지가 두 번 나온다.
  - `_sdd/spec/main.md` 등 하네스 외 문서의 주입 — `AGENTS.md` §1(읽는 순서)이 재주입되면 spec을 읽을 경로가 복구되므로, 지금 필요한 최소는 하네스 전문이다.
  - 주입량 상한·요약 등 크기 제어 — 위 가정 2 참조. 자르면 무엇이 잘렸는지 모델이 알 수 없어 부분 규약을 전체로 오인하는 더 나쁜 실패를 만든다. 실측된 문제가 생기면 그때 별도 feature로 다룬다.
  - `PreCompact` 훅 — compact **이후** 상태를 복구하는 것이 목적이므로 SessionStart로 충분하다.
  - `_sdd/spec/*.md` 직접 수정 — global spec 반영은 `spec-sync` 소관이다. 이 feature는 갱신이 필요한 지점 목록을 인계 산출물로 남긴다(Task 6 AC4).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: `harness-context.sh` 정본 작성 + 4벌 미러 동기화

컨텍스트 소실 후 `AGENTS.md` 전문을 주입하는 SessionStart 훅 스크립트를 만들고, 기존 훅 자산과 동일한 정본/미러 규율로 4곳에 놓는다.

**Contracts**:
- 스크립트는 `cd "${CLAUDE_PROJECT_DIR:-.}"`로 프로젝트 루트에 고정한 뒤 동작한다(하위 디렉토리에서 세션이 시작돼도 동일 결과). `cd` 실패는 `exit 0`(fail-silent).
- `AGENTS.md`가 없으면 아무것도 출력하지 않고 `exit 0` — 하네스가 없는 repo에서 잡음을 만들지 않는다.
- 출력은 `[harness]` 리드 1줄 + `AGENTS.md` 전문. 리드 줄을 제외한 나머지는 `AGENTS.md`와 **바이트 동일**하다(요약·발췌 금지).
- 헤더 주석에 정본 경로와 미러 3곳을 명시한다(기존 두 스크립트와 동일 규율).
- 정본은 `.claude/skills/spec-create/references/hooks/harness-context.sh`, 나머지 3곳은 미러이며 4벌이 바이트 동일하다.

**Acceptance Criteria**:
- [ ] AC1: 이 repo를 `CLAUDE_PROJECT_DIR`로 주어 실행하면 stdout 첫 줄이 `[harness]`로 시작하고, `tail -n +2` 출력이 `AGENTS.md`와 `diff` 무출력이다.
- [ ] AC2: `AGENTS.md`가 없는 빈 임시 디렉토리를 `CLAUDE_PROJECT_DIR`로 주면 stdout이 비어 있고 exit code가 0이다.
- [ ] AC3: cwd를 repo 하위 디렉토리(`_sdd/`)로 바꾼 채 실행해도 AC1과 동일한 stdout을 낸다 — `worklog-gate.sh`에서 실측된 프로젝트 루트 미고정 버그의 재발 방지.
- [ ] AC4: `AGENTS.md`가 마커 블록 + 마커 밖 내용으로 구성된 픽스처(마커 밖에 고유 문장 1줄 추가)에서 실행하면, 그 마커 밖 문장이 stdout에 포함된다 — 전문 주입임을 반증 가능하게 확인한다(가정 2).
- [ ] AC5: `{.claude,.codex}/skills/{spec-create,spec-upgrade}/references/hooks/harness-context.sh` 4개의 md5가 1종이다.

**Target Files**:
- [C] `.claude/skills/spec-create/references/hooks/harness-context.sh` -- 정본
- [C] `.codex/skills/spec-create/references/hooks/harness-context.sh` -- 미러
- [C] `.claude/skills/spec-upgrade/references/hooks/harness-context.sh` -- 미러
- [C] `.codex/skills/spec-upgrade/references/hooks/harness-context.sh` -- 미러

---

### Task 2: `spec-create` §3e를 훅 자산 일반 계약으로 확장

§3e가 work log 전용 절이라 세 번째 스크립트를 받을 자리가 없다. 절을 훅 자산 일반으로 넓히고 세 스크립트를 하나의 병합 계약 아래 둔다.

**Contracts**:
- 절 제목과 본문에서 "work log 훅 자산" 한정을 걷고, 세 스크립트를 (스크립트, 이벤트, matcher) 대응이 보이는 형태로 열거한다. 별도 절(§3f)을 신설하지 않는다 — `settings.json` 병합 규칙의 판정 주체가 둘로 갈린다.
- verbatim 복사 지시·`settings.json` 키 수준 멱등 병합 규칙·파싱 불가 시 미덮어쓰기 조항은 **문구를 유지**한 채 대상만 세 스크립트로 넓힌다(재작성 금지 — 이 문구들은 직전 리뷰에서 실측 보정된 것이다).
- JSON 예시의 `hooks.SessionStart` 배열은 그룹 객체 2개를 갖는다: matcher 없는 `worklog-context.sh` 그룹과 `"matcher": "clear|compact"`인 `harness-context.sh` 그룹.
- 멱등 판정 키는 기존과 동일하게 "`command` 문자열이 해당 스크립트 경로를 포함하는 항목"이다 — 스크립트가 셋으로 늘어도 각 그룹이 독립적으로 판정된다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/skills/spec-create/SKILL.md`의 §3e 섹션 본문에 `harness-context.sh`와 `clear|compact` 리터럴이 모두 등장한다.
- [ ] AC2: `#### 3e` 헤더부터 다음 `### ` 또는 `#### ` 헤더 직전까지를 구간으로 잘라 그 안의 유일한 ` ```json ` 펜스 블록을 파일로 추출한 뒤 `python3 -c "import json,sys; d=json.load(open(sys.argv[1])); s=d['hooks']['SessionStart']; assert len(s)==2; assert sum(1 for g in s if g.get('matcher')=='clear|compact')==1; assert sum(1 for g in s if 'matcher' not in g)==1"` 가 exit 0으로 통과한다. (구간 추출기는 펜스 안의 `#` 시작 줄을 헤더로 오인하지 않도록 코드블록을 추적한다 — 직전 feature에서 실측된 함정이다.)
- [ ] AC3: 파일 전체에서 `두 스크립트`·`스크립트 2개`·`두 훅`·`훅 2개` 리터럴 히트가 0건이다.
- [ ] AC4: `## Companion Assets` 목록에 `references/hooks/harness-context.sh` 항목이 있다.
- [ ] AC5: `.claude/skills/spec-create/SKILL.md`와 `.codex/skills/spec-create/SKILL.md`의 md5가 동일하다.

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md` -- §3e 일반화, Companion Assets, 착수 체크리스트, Hard Rules #4, Step 3 도입부, Step 5 검증, Output Contract
- [M] `.codex/skills/spec-create/SKILL.md` -- 위와 바이트 동일 미러

---

### Task 3: `spec-upgrade` Step 6을 훅 자산 일반 계약으로 확장

Step 6의 훅 병합 규칙도 같은 이유로 넓힌다. 계약 형태의 canonical은 `spec-create` §3e라는 기존 참조 관계를 유지한다.

**Contracts**:
- Step 6 제목의 `work log 훅 자산` 표기와 본문의 "work log 훅 자산 병합 규칙" 소제목을 훅 자산 일반으로 바꾼다.
- "그 스킬이 없는 환경이면 아래 구조를 쓴다"의 인라인 fallback 구조에 `harness-context.sh` 그룹(`{"matcher": "clear|compact", …}`)을 추가한다 — 이 인라인은 `spec-create` 부재 시 유일한 계약 소스이므로 누락되면 그 환경에서 세 번째 훅이 등록되지 않는다.
- 등록 형태 서술에 SessionStart의 matcher가 스크립트별로 다르다는 점(전 소스 vs `clear|compact`)을 명시한다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/skills/spec-upgrade/SKILL.md`에 `harness-context.sh`와 `clear|compact` 리터럴이 모두 등장하고, 그중 `clear|compact`가 Step 6의 인라인 fallback 구조 서술 안에도 등장한다.
- [ ] AC2: 파일 전체에서 `두 스크립트`·`스크립트 2개`·`두 훅`·`훅 2개` 리터럴 히트가 0건이다.
- [ ] AC3: `## Companion Assets` 목록에 `references/hooks/harness-context.sh` 항목이 있다.
- [ ] AC4: Step 7 검증 항목과 Output Contract 항목 **양쪽 모두**에 `harness-context.sh` 리터럴이 등장한다.
- [ ] AC5: `.claude/skills/spec-upgrade/SKILL.md`와 `.codex/skills/spec-upgrade/SKILL.md`의 md5가 동일하다.

**Target Files**:
- [M] `.claude/skills/spec-upgrade/SKILL.md` -- Step 6 제목·훅 병합 규칙, 착수 체크리스트, Companion Assets, Step 7, Output Contract
- [M] `.codex/skills/spec-upgrade/SKILL.md` -- 위와 바이트 동일 미러

---

### Task 4: 이 repo에 dogfooding 설치 + 런타임 발동 관찰

이 repo는 자기 스킬의 산출물을 dogfooding한다. 세 번째 훅도 `spec-create` §3e의 계약대로 설치하고, **matcher가 실제로 발동하는지를 런타임에서 관찰한다** — 등록 문자열이 틀려도 훅은 오류 없이 미발동하므로 정적 검사만으로는 계약이 닫히지 않는다.

**Contracts**:
- `.claude/hooks/harness-context.sh`는 정본의 verbatim 사본이다.
- `.claude/settings.json`의 `hooks.SessionStart`는 기존 `worklog-context.sh` 그룹을 보존한 채 `harness-context.sh` 그룹을 추가한다. 기존 `PreToolUse` 그룹은 변경하지 않는다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/hooks/harness-context.sh`의 md5가 정본과 동일하다.
- [ ] AC2: `.claude/settings.json`이 파싱되고, `hooks.SessionStart` 길이가 2이며 각 그룹의 `command`가 `worklog-context.sh`·`harness-context.sh`를 각각 하나씩 가리킨다. `git diff -- .claude/settings.json` 의 변경 hunk가 `SessionStart` 구간에만 있고 `PreToolUse` 구간에는 없다.
- [ ] AC3: 설치된 `.claude/hooks/harness-context.sh`를 이 repo에서 실행하면 Task 1 AC1과 동일한 출력을 낸다(복사본이 실제로 동작함).
- [ ] AC4: **런타임 발동 관찰** — `source`가 `clear` 또는 `compact`인 SessionStart에서 이 훅이 실제로 실행되어 `[harness]` 리드 줄이 모델 컨텍스트에 들어왔음을 관찰한 증거가 있다. 관찰 수단은 구현 시 결정한다(헤드리스 세션을 픽스처 repo에서 구동해 compact/clear를 유발하는 방법을 먼저 시도한다). **관찰 증거를 못 대면 이 AC를 "충족"으로 적지 않고 미충족으로 보고한다** — 정적 근거(가정 1)만으로는 무증상 미발동을 배제할 수 없다.

**Target Files**:
- [C] `.claude/hooks/harness-context.sh` -- dogfooding 설치본
- [M] `.claude/settings.json` -- SessionStart 그룹 추가

---

### Task 5: `docs/SDD_CONCEPT.md` 후행 갱신 (ko·en)

훅 자산 계약이 넓어졌으므로 하네스 레이어 설명이 실행 자산의 예로 커밋 게이트 하나만 들지 않게 한다 — 실행 자산이 "강제"뿐 아니라 "컨텍스트 복구"도 포함한다는 점이 레이어 설명의 핵심이다.

**Acceptance Criteria**:
- [ ] AC1: `docs/SDD_CONCEPT.md`와 `docs/en/SDD_CONCEPT.md`의 §1 하네스 문단이 실행 자산의 예로 커밋 게이트와 하네스 재주입을 모두 든다.
- [ ] AC2: 두 파일의 변경이 서로 대응한다 — ko 추가 문장 수와 en 추가 문장 수가 같고, 각 ko 문장에 대응하는 en 문장을 1:1로 지목할 수 있다(`git diff`의 추가 줄을 나란히 놓고 확인).

**Target Files**:
- [M] `docs/SDD_CONCEPT.md` -- §1 하네스 문단
- [M] `docs/en/SDD_CONCEPT.md` -- 위의 영문 대응

---

### Task 6: 훅 자산 census 검증 (read-only, 마지막)

훅 스크립트 개수는 여러 문서에 리터럴로 흩어져 있어 전수 열거 없이는 잔존이 재발한다. **이 feature가 소유한 표면**에 대해 수정 잔존을 grep census + omission 대조로 확인하고, 소유하지 않은 표면(`_sdd/spec/`)은 `spec-sync` 인계 목록으로 남긴다.

**Contracts**: 없음 (read-only 검증)

**Acceptance Criteria**:
- [ ] AC1: **omission 대조** — `.claude/skills/spec-create/references/hooks/`의 실제 파일 목록을 기준으로, 이 feature가 소유한 열거 지점(두 SKILL.md × 2레인의 Companion Assets·설치 지시·검증 항목·Output Contract)에서 빠진 스크립트가 0건이다. 단순 `harness-context` grep 히트 수로 대체하지 않는다 — 열거 지점을 먼저 나열하고 각각에 대해 세 스크립트의 유무를 표로 판정한다.
- [ ] AC2: 개수 리터럴 변형 전수 grep — `두 스크립트`, `스크립트 2개`, `훅 2개`, `두 훅`, `훅 자산 2` 를 **`.claude/skills/`·`.codex/skills/`·`docs/`·`AGENTS.md`** 범위에서 검색해 히트가 0건이다. (`_sdd/spec/`는 `spec-sync` 소관이라 대상 밖, `_sdd/work_log/`·`_sdd/drafts/_processed_*`는 append-only 이력이라 대상 밖.)
- [ ] AC3: 4벌 미러 md5 — `references/hooks/`의 세 스크립트가 각각 4곳에서 1종의 md5를 갖는다(총 3종). 두 SKILL.md도 각각 claude↔codex 바이트 동일이다.
- [ ] AC4: **`spec-sync` 인계 목록 산출** — 훅 스크립트 개수를 서술하지만 이 feature가 고치지 않은 `_sdd/spec/` 지점을 파일:줄 단위로 열거한 목록이 마감 보고에 있다(현재 실측: `main.md:65`, `components.md:52`, `usage-guide.md:32`). 열거는 AC2와 같은 변형 패턴을 `_sdd/spec/`에 적용해 얻는다.
- [ ] AC5: `git status --porcelain -- _sdd/spec/` 무출력 — 이 feature가 global spec을 직접 건드리지 않았다.
- [ ] AC6: `git diff --check` 무출력.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- `_sdd/spec/usage-guide.md`에는 아직 `spec-upgrade` 시나리오 절이 없어(직전 feature에서 surface됨) 훅 자산의 업그레이드 경로가 문서화되지 않는다. 이번 범위 밖으로 두고 `spec-sync`가 usage-guide의 산출물 열거를 갱신하는 선에서 닫는다 — 별도 feature로 다룰지 사용자 확인 필요.
