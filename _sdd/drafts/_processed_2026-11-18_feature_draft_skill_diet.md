# 스킬 정리: spec 스킬 3개 합치기, 3개 삭제, 3개 축소

<!-- spec-update-todo-input-start -->
## Spec Delta

**무엇이 왜 바뀌는가.** 2026-11-17에 SDD 체인을 메인 세션 직접 실행으로 줄였다(v5.0.0). 같은 기준(스킬은 순서와 모델이 추론할 수 없는 규약만 정한다)을 나머지 스킬에 적용한다. 스킬 21개 중 9개가 대상이다.

1. **합치기**: `spec-review`·`spec-rewrite`를 `spec-upgrade`로 합친다. 셋은 같은 판단 기준 4개를 쓰고, 예전 `spec-upgrade`에는 upgrade와 rewrite 중 어느 쪽인지 가르는 단계가 따로 있었다. 합치면 그 단계와 중복 참조 파일이 없어진다. 이름은 `spec-upgrade`를 유지한다.
2. **삭제**: `spec-summary`, `spec-snapshot`, `second-opinion`. 이 저장소에는 두 spec 스킬의 산출물(`_sdd/spec/summary.md`, `_sdd/snapshots/`)이 없다. `second-opinion`은 번들에 없는 외부 adapter가 있어야 동작한다.
3. **축소**: `guide-create`, `investigate`, `git`의 지시문을 줄인다. 모델이 기본으로 하는 일의 설명과 출력 예시를 지우고, 저장소 규약과 승인·안전 규칙만 남긴다.

**새로 의지하게 될 약속.**

- 기존 spec을 점검하거나 고치는 진입점은 `spec-upgrade` 하나다. 요청이 점검이면 파일을 고치지 않고, 그 밖에는 고친 뒤 하네스(AGENTS.md·CLAUDE.md·.gitignore·env.md·훅)를 갱신한다.
- `spec-upgrade`의 대상은 `_sdd/spec/`이다. 계획 파일(`_sdd/drafts/`) 검토는 `sdd-orchestrator`의 계획 리뷰가 맡는다.
- 예전 이름(`spec-review`, `spec-rewrite`)의 별칭 스킬은 만들지 않는다. `spec-upgrade` description의 trigger 문구가 예전 이름을 받는다.
- `investigate`는 탐색 agent 병렬 실행을 지시하지 않는다. 번들에서 agent를 띄우는 스킬은 `pr-review`뿐이다.
- 스킬 수: Claude 11 + 호환 별칭 5, Codex 10 + 호환 별칭 5.

**범위 In.** 스킬 9개(Claude·Codex 양쪽), `.claude-plugin/marketplace.json`, `README.md`, `docs/SDD_WORKFLOW.md`·`docs/SDD_SPEC_DEFINITION.md`와 `docs/en/` 짝, `_sdd/spec/{main,components,usage-guide}.md`·`decision_log.md`·`logs/changelog.md`.

**범위 Out.** `sdd-orchestrator`와 별칭 5개, `pr-review`, `spec-create`, `discussion`, `goal-init`, `sdd-autopilot`, `ralph-loop-init`의 본문. 하네스 템플릿·훅 스크립트·`hook-installation.md`·`worker-model-defaults.md`의 내용(위치와 바이트 그대로). 기록 파일(`decision_log.md` 기존 entry, `changelog.md` 기존 entry, `_sdd/work_log/`, `_sdd/drafts/`, `_sdd/goal/`, `_sdd/spec/prev/`, `_sdd/spec/logs/`, `docs/reviews/`). `tools/uninstall-codex-skill-bundle.py`의 `LEGACY_SKILL_NAMES`(삭제된 스킬을 지우려면 이름이 남아 있어야 한다).
<!-- spec-update-todo-input-end -->

## 계획

### 사용자 결정 (2026-11-18)

| 지점 | 고른 안 | 버린 안 |
|---|---|---|
| 합친 스킬 이름 | `spec-upgrade` 유지 | `spec-update`(구현 결과 반영을 뜻하는 spec-sync와 의미가 겹침), `spec-review` 유지(하네스 설치가 review 이름 아래 들어감) |
| `git`·`second-opinion` | `second-opinion`만 삭제, `git`은 축소 | 둘 다 삭제, 둘 다 축소 |
| 진행 방식 | SDD 순서로 한 번에 | 계획까지만, 둘로 나눠서 |

### 바꿀 자리

**A. 합친 `spec-upgrade`** (양쪽 runtime 동일본)

- `SKILL.md`를 다시 쓴다. 구성: 판단 기준(global spec 세 절, 기준 4개, 결함이 아닌 것) → 단계(점검 → 고치기 → 하네스 갱신 → 확인) → 호출 범위(점검만 / 고치기).
- 점검 규칙은 `spec-review`에서 가져온다: 모든 발견에 근거, 근거가 약하면 `UNTESTED`, 접근 실패를 "없음"으로 판정하지 않음, 구현 쪽 drift는 spec 수정 대상이 아님, 심각도 3단계.
- 고치기 규칙은 `spec-rewrite`·`spec-upgrade`에서 가져온다: in-place, 근거·citation 보존, 없는 내용을 지어내지 않음, 이력은 `decision_log.md`로, 큰 구조 변경은 계획을 `_sdd/spec/logs/spec-rewrite-plan.md`에 먼저 쓰고 확인, 분할 축(domain / topic).
- 하네스 갱신 절(예전 Step 6)은 규칙을 그대로 옮긴다. verbatim 복사, 마커 멱등 병합, 보존/흡수 규칙, `.gitignore` 블록, `env.md`, 훅 설치.
- `references/`: 하네스 자산 4종(`agents-harness-template.md`, `hook-installation.md`, `hooks/`, `worker-model-defaults.md`)은 그대로 둔다. `spec-format.md`·`template-compact.md`·`template-full.md`·`upgrade-mapping.md`와 `spec-rewrite`의 `rewrite-checklist.md`는 `spec-format.md` 하나로 합친다(세 절, compact·full skeleton과 선택 기준, 예전 내용을 어디로 내리는가 표). `examples/after-upgrade.md`는 그대로 둔다.
- 버리는 것: upgrade↔rewrite 경계 판정, rewrite 진단 축 4개(Component Separation 등), `rewrite_report.md` 산출물, drift status·decision 토큰(`SPEC_OK` 등), temporary spec rubric, 코드 분석 evidence 절.

**B. 삭제** (디렉터리째)

- `.claude/skills/{spec-review,spec-rewrite,spec-summary,spec-snapshot,second-opinion}`
- `plugins/sdd-skills-codex/skills/{spec-review,spec-rewrite,spec-summary,spec-snapshot}`
- `.claude-plugin/marketplace.json`의 해당 5줄

**C. 축소**

- `guide-create` (양쪽 동일본): `SKILL.md`를 규칙 위주로 줄인다. `references/output-format.md`는 §3 fenced skeleton을 글자 그대로 두고 그 주변 설명을 줄인다.
- `investigate`: 탐색 agent 병렬 실행 지시와 Codex Runtime Adapter를 지운다. 규칙 6개(범위 고정, 원인 확인 뒤 수정, 3회 실패 시 전략 변경, 영향 범위, 재실행 검증, spec 불가침)와 보고 형식을 남긴다. Codex 쪽은 지금처럼 diagnose-only가 기본이고 수정 요청이 있을 때만 고친다(runtime 간 차이 유지).
- `git` (Claude 전용): `references/` 3개와 `examples/` 3개를 지우고 `SKILL.md` 하나로 만든다. 남기는 것: 호출 범위 표, 상태 파악 규칙(fetch, 진행 중 rebase/merge), 커밋 묶기와 메시지 형식, 브랜치 판단 표, 승인 규칙(goal `자율 수행 위임` 포함), 실행 규칙(index 보존, 커밋 뒤 대조), 안전 규칙 전부. 지우는 것: 대시보드·계획·보고 출력 예시, Conventional Commits type 표, 그룹핑 예시.

**D. 전파**

- `README.md`: 스킬 수 표(L9~10), Skills 표(L172~173), Claude 전용 안내(L186).
- `docs/SDD_WORKFLOW.md`: §5 실무 요약(review·rewrite·upgrade 줄), §6(`spec-summary` 절), §7·§8의 스킬 설명. `docs/en/SDD_WORKFLOW.md` 같은 자리.
- `docs/SDD_SPEC_DEFINITION.md`: §7 표의 summary 행, §8 추가 축 목록, §10 스킬 설명. `docs/en/` 같은 자리.
- `_sdd/spec/`: spec 반영 단계에서 고친다(`main.md` L72·84·125·129·130·140, `components.md` 행, `usage-guide.md` Scenario 3b).

### 끝나는 조건

| ID | 조건 | 판정 방법 |
|---|---|---|
| C1 | 삭제 대상 9개 디렉터리가 없고 `marketplace.json`이 실제 디렉터리와 맞는다 | `ls`로 9개 부재. `marketplace.json`의 경로마다 `SKILL.md`가 있고, `.claude/skills/*/`마다 경로가 등록돼 있다(스크립트로 양방향 대조, 불일치 0) |
| C2 | 삭제한 이름과 산출물 이름이 현재 표면에 남지 않는다 | `/usr/bin/grep -rnE 'spec[-_ ](review|rewrite|summary|snapshot)|second[-_ ]opinion|rewrite_report|SYNC_REQUIRED|SPEC_OK|_sdd/snapshots|spec/summary\.md|upgrade-mapping|template-(compact|full)|rewrite-checklist'`에서 기록 파일(범위 Out)과 허용 목록을 빼고 0건. 허용 목록: ① `tools/uninstall-codex-skill-bundle.py`의 `LEGACY_SKILL_NAMES`, ② `spec-upgrade/SKILL.md` frontmatter `description`의 trigger 문구, ③ `spec-upgrade`의 산출물 경로 `spec-rewrite-plan.md`·`spec_review_report.md`, ④ `spec-create/references/template-{compact,full}.md`와 그것을 가리키는 `spec-create` 본문·spec 문구 |
| C3 | 합친 `spec-upgrade`가 양쪽에서 같고 하네스 자산은 바이트가 그대로다 | `/usr/bin/diff -r .claude/skills/spec-upgrade plugins/sdd-skills-codex/skills/spec-upgrade` 출력 없음. `git diff --stat HEAD`에 하네스 자산 4종 변경 없음. `SKILL.md`가 가리키는 `references/`·`examples/` 경로가 모두 존재(추출 대조, 없는 경로 0). `references/`에 지운 파일 4개 부재 |
| C4 | 합친 `spec-upgrade`가 세 스킬의 규칙을 잃지 않았다 | 유지 목록의 문구를 `SKILL.md`·`references/spec-format.md`에서 검색해 각각 1건 이상: `UNTESTED`, `decision_log`, `spec-rewrite-plan.md`, `Strategic Code Map`, `SDD-HARNESS`, `SDD-WORKSPACE`, `hook-installation.md`, `worker-model-defaults.md`, `agents-harness-template.md`, 기준 4개 이름, 분할 축 `domain`·`topic`, compact·full 선택 기준. 하네스 병합 규칙 문단(AGENTS.md 3분기, CLAUDE.md 포인터 본문, 보존/흡수 규칙, `.gitignore` 블록)은 HEAD 본문과 줄 단위로 대조해 뜻이 같은지 읽어서 확인 |
| C5 | 축소한 세 스킬이 남기기로 한 규칙을 가진다 | `git`: `force-with-lease`, `자율 수행 위임`, `git diff --cached`, `release/*`, `git reset --hard`, stash 규칙, 호출 범위 6행이 `SKILL.md`에 있고 `references/`·`examples/` 부재. `investigate`: 양쪽에 `UNTESTED`, `3`회 규칙, `_sdd/spec/`가 있고 `Explore`·`explorer`·`spawn_agent`·`Runtime Adapter` 0건, Codex 쪽에 `diagnose-only`. `guide-create`: `output-format.md`의 fenced skeleton 블록이 HEAD와 동일(`diff` 출력 없음), `SKILL.md` 양쪽 동일. 크기: `git` ≤ 6KB, `investigate` ≤ 3KB(Claude)·≤ 4KB(Codex), `guide-create` `SKILL.md` ≤ 3KB·`output-format.md` ≤ 4.5KB |
| C6 | README와 docs가 실제 구성과 맞는다 | README 스킬 수가 `ls` 실측과 같다(Claude 11+5, Codex 10+5). `docs/`와 `docs/en/`에서 같은 절을 고쳤다(절 제목 목록 `grep '^## '` 수가 서로 같다) |
| C7 | 배포 검증이 통과한다 | `claude plugin validate .` 통과. `python3 -m unittest discover -s tools/tests -p 'test_*.py'` 통과. `git diff --check` 출력 없음. 새 파일 줄 끝 공백 0 |
| C8 | spec이 바뀐 구성을 현재 사실로 적는다 | `main.md` 헤더 `Spec Version`과 `logs/changelog.md` 최신 entry 버전이 같다. `components.md`에 삭제한 스킬 5개의 행이 없다. `decision_log.md`·`changelog.md`의 `git diff`가 추가 줄뿐이다 |

### 계획이 기대는 외부 사실

- 삭제 대상 스킬을 다른 스킬 본문이 호출하지 않는다(전수 검색 결과: `spec-upgrade`만 `spec-rewrite`를 가리킴).
- `spec-review`·`spec-rewrite`·`spec-summary`·`guide-create`·`spec-upgrade`의 `SKILL.md`는 양쪽 runtime이 같다. `investigate`는 다르다(25곳). `git`·`second-opinion`은 Claude에만 있다.
- 하네스 자산 4종은 `spec-create`와 `spec-upgrade`의 양쪽 runtime에 같은 사본으로 있다(5곳 전파 규약). 이번에 내용을 고치지 않는다.
- `tools/tests`의 테스트는 번들 스킬 이름이 `LEGACY_SKILL_NAMES`의 부분집합인지 본다. 스킬을 지워도 통과한다.
- 스킬 편집은 머지와 플러그인 갱신 뒤에 적용된다. 이 세션에서 새 `spec-upgrade`를 실제로 호출해 볼 수 없다.

### 계획 리뷰에서 찾아 반영한 것

1. `docs/SDD_WORKFLOW.md` §6(`spec-summary` 절)을 지우면 §7~§10이 §6~§9로 당겨진다. 이 절 번호를 가리키는 현재 표면은 없다(검색 0건). §7 제목 "네 개 lifecycle 스킬"은 "두 lifecycle 스킬"(`spec-create`, `spec-upgrade`)로 바꾼다. `docs/en/`도 같다.
2. `docs/SDD_SPEC_DEFINITION.md` L187은 기준 4개가 spec 스킬의 Acceptance Criteria와 Final Check에 들어가야 한다고 정한다. 합친 `spec-upgrade`의 AC에 기준 4개 이름을 둔다(C4에 포함).
3. C2의 검색식은 스킬 이름만 잡는다. docs에는 이름 없이 "upgrade 범위를 넘으면 rewrite로 넘긴다"처럼 예전 구분을 전제한 문장이 있다(`SDD_WORKFLOW.md` L58~61). C6에 판정을 추가한다: `docs/`·`docs/en/`·`README.md`에서 `rewrite`·`review`가 남은 줄을 모두 읽어, 예전 스킬 구분을 전제한 문장이 없음을 확인한다.
4. `investigate`의 탐색 agent 지시를 지우면 `main.md` L84·L125와 `components.md` Platform Notes 두 행이 낡는다. C8에 판정을 추가한다: `_sdd/spec/{main,components}.md`에서 `explore fan-out`·`Explore`·`explorer` 검색 결과가 `pr-review`나 Codex 일반 규칙 문맥뿐이다.
5. 작성 규범(`docs/SKILL_AUTHORING_NORMS.md` §3.2)은 분리한 reference마다 읽는 시점을 본문에 한 줄로 지정하라고 한다. 합친 `spec-upgrade`와 `guide-create`가 reference를 읽는 시점을 본문에 적는다.

## 진행

- 현재 단계: spec 반영까지 완료(2026-11-18). 커밋과 PR은 사용자 요청 대기.

### 조건별 판정

검사 스크립트는 변경 전에 C1~C5가 실패함을 먼저 확인했다(C2 잔존 120건, C3 양쪽 다름, C4 문구 3개 없음, C5 규칙·크기 미달).

| ID | 판정 | 증거 |
|---|---|---|
| C1 | 충족 | 9개 디렉터리 부재. `marketplace.json` 16개 경로와 `.claude/skills/*/` 16개 양방향 대조 불일치 0 |
| C2 | 충족 | 전수 검색 잔존 0건(변경 전 120건). 허용 목록은 계획과 같다 |
| C3 | 충족 | `/usr/bin/diff -r` 양쪽 `spec-upgrade` 출력 없음. 하네스 자산 4종과 `.claude/hooks`의 `git status` 변경 없음. `SKILL.md`가 가리키는 `references/`·`examples/` 경로 모두 존재. 옛 참조 3개 부재 |
| C4 | 충족 | 유지 문구 19개 모두 검색됨. 하네스 병합 문단은 HEAD 본문(예전 Step 6)과 줄 단위로 대조해 읽었다. 3분기·포인터 본문·보존/흡수 규칙·`.gitignore` 블록·훅 3단계의 뜻이 같다 |
| C5 | 충족 | `git`·`investigate`·`guide-create` 유지 규칙 모두 검색됨. `investigate` 양쪽에 `Explore`·`explorer`·`spawn_agent`·`Runtime Adapter` 0건. `guide-create` fenced skeleton이 HEAD와 동일. 크기는 아래 "달라진 결정" 참조 |
| C6 | 충족 | README 11+5, 10+5가 `ls` 실측과 같다. `SDD_WORKFLOW.md` 절 수 ko 9 = en 9, `SDD_SPEC_DEFINITION.md` ko 18 = en 18. docs·README에서 `rewrite`·`review`가 남은 줄을 모두 읽었고 예전 스킬 구분을 전제한 문장은 없다 |
| C7 | 충족 | `claude plugin validate .` 통과, `tools/tests` 통과, `git diff --check` 출력 없음, 새 파일 줄 끝 공백 0 |
| C8 | 충족 | `main.md` 헤더 6.0.0 = changelog 최신 entry 6.0.0. `components.md`에 삭제 스킬 행 0. `decision_log.md`·`changelog.md` diff는 추가 줄뿐(삭제 줄 0). spec의 `explorer`·`fan-out`은 `pr-review`와 Codex 일반 규칙 문맥 3곳뿐 |

### 계획과 달라진 결정

1. **크기 기준 2개를 고쳤다.** `git` ≤ 6KB를 ≤ 9KB로, Codex `investigate` ≤ 4KB를 ≤ 4.5KB로 바꿨다. 처음 기준은 본문을 쓰기 전에 어림한 값이었다. `git`은 참조 파일의 안전 규칙(1.7KB)을 본문에 합치면서 승인 규칙과 안전 규칙만으로 약 4.5KB가 됐고, 이 둘은 남기기로 한 규칙이다. Codex 점검에서 받은 규칙 2개를 복원한 뒤 Codex `investigate`는 4.6KB가 되어 기준을 ≤ 5KB로 한 번 더 고쳤다(복원한 문장은 예전 본문에 있던 수정 권한 경계다). 결과는 `git` 폴더 21.1KB → 8.3KB, Codex `investigate` 11.2KB → 4.6KB다. 유지 규칙과 삭제 대상의 판정(C5의 나머지)은 바꾸지 않았다.
2. **`spec-upgrade`에 하네스만 갱신하는 호출 범위를 더했다.** description의 trigger에 "하네스 갱신"이 있는데 호출 범위 표에 받는 행이 없어, 그 요청이 spec 본문까지 고치는 경로로 갈 수 있었다. 표에 "3단계와 그 확인만 한다" 행을 더했다.
3. **요청이 모호할 때의 처리를 바꿨다.** "점검 결과를 보고하고 고칠지 묻는다"는 무인 실행에서 멈춘다. "점검만 하고, 고칠지는 보고 끝에서 묻는다"로 바꿨다.

### 구현 리뷰에서 찾아 고친 것

- 위 2, 3번.
- `git` 스킬의 예전 단계 이름(`CONFIRM`)을 spec 두 곳(`main.md` goal 계약 줄, `components.md` `git` 행)이 가리켰다. spec 반영에서 `승인` 규칙으로 고쳤다.
- `components.md`의 Workspace commit 정책 행이 `spec-upgrade` "Step 6"을 가리켰다. `하네스 갱신`으로 고쳤다.
- 검사 스크립트의 `$n개`가 macOS bash에서 깨져 출력됐다. `${n}개`로 고치고 `_sdd/env.md` Pitfalls에 올렸다.

### Codex 점검(읽기 전용)에서 받아 고친 것

Codex(gpt 계열, `codex exec -s read-only`)가 새 `spec-upgrade`를 "스펙 리뷰해줘"로 이 저장소에 실제로 수행했고, 범위 판정 → 점검 → 보고까지 막힘 없이 갔다. 지적 5건을 모두 사실로 확인해 고쳤다.

1. `investigate`(양쪽): `_sdd/spec/` 금지에서 "지우지 않는다"가 빠졌다. 복원했다.
2. `investigate`(Codex): fix 요청을 받았어도 원인을 확인하기 전에는 고치지 않는다는 순서가 빠졌다. 규칙 2에 넣었다.
3. `spec-upgrade`: 인자 없이 스킬 이름만 부른 호출의 범위가 정해지지 않았다. "점검만 하고 묻는다"에 든다고 적었다.
4. `spec-upgrade`: 점검만 하는 호출이 "어떤 파일도 고치지 않는다"면서 보고서 파일을 쓰게 했다. "spec과 하네스를 고치지 않는다, 요청받은 보고서 파일만 쓴다"로 바꾸고 spec·docs(ko·en)의 같은 문구를 맞췄다.
5. `README.md` Codex 설치 안내가 `spec-upgrade` 실행 시 항상 훅을 설치한다고 적었다. 점검만 하는 호출은 설치하지 않는다고 고쳤다.

Codex가 "해석이 필요했다"고 한 지점(`_sdd/spec/` 아래 `prev/`·`logs/` 기록을 점검 대상으로 볼지)도 본문에 적었다. 점검 대상은 `main.md`와 그것이 가리키는 보조 문서다.

Codex의 spec 점검에서 나온 발견 중 이번 범위 밖 2건은 고치지 않았다: `components.md`의 `ralph-loop-init` 행이 생성 파일을 6개와 7개로 다르게 적는다. `main.md`의 `pr-review` 항목이 스킬 본문의 입력·재실행 규칙을 중복해 적는다.

### 실행으로 확인하지 못한 것

- 새 `spec-upgrade`·`investigate`·`guide-create`·`git`를 설치본에서 실제로 호출해 보지 않았다. 스킬 편집은 머지와 플러그인 갱신 뒤에 적용된다.
- 예전 형식 spec을 새 `spec-upgrade`로 옮기는 실행, 소비 repo에서 하네스만 갱신하는 실행을 해 보지 않았다.
- Codex runtime에서의 동작은 확인하지 않았다(파일 대조만 했다).
- 예전 이름 trigger("spec-review 해줘")가 `spec-upgrade`의 점검 범위로 가는지는 description 문구로만 뒷받침된다.
