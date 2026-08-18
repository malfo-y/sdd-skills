# Feature Draft: Codex 플러그인 레이아웃 공존 — .codex/skills를 plugins/sdd-skills-codex로 이사

> 규모 판정: 적격 — 변경 요소가 디렉토리 이동 1건·manifest 2개 신설·경로 참조 갱신·census로 유한 열거되고 요소↔task 대응이 눈검산 가능

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
Codex 플러그인 배포 레이아웃(발견 위치 `skills/` 고정)과 클코 플러그인 배포(경로 자유)를 한 repo에 공존시킨다. (1) `.codex/skills/`(19개)를 `plugins/sdd-skills-codex/skills/`로 전체 이동 — 콘텐츠·미러 관리 방식(3-way 적응) 불변, 위치만 이동. (2) Codex manifest 2개 신설: `.agents/plugins/marketplace.json`(마켓 이름 `sdd-skills-codex`)과 `plugins/sdd-skills-codex/.codex-plugin/plugin.json`(플러그인 이름 `sdd-skills-codex`) — Codex가 `.claude-plugin/marketplace.json`을 legacy로도 읽을 수 있어 클코 마켓 이름(`sdd-skills`)과 반드시 다르게 둔다. (3) 클코 배포(`.claude-plugin/` + `.claude/skills/`)와 repo dogfooding(`.claude/hooks/`·`.codex/hooks.json`)은 불변. (4) `tools/install-codex-skill-bundle.py`의 skills root를 새 경로로 갱신(구 경로 수동 설치 사용자의 설치 경로 연속성 유지). (5) README·spec 표면의 `.codex/skills` 경로 참조 전수 갱신.

새 contract: **Codex 스킬 미러의 canonical 위치는 `plugins/sdd-skills-codex/skills/`이며, Codex 플러그인/마켓 이름은 클코 마켓 이름과 충돌하지 않는 `sdd-skills-codex`다.** `.codex/` 디렉토리는 repo dogfooding용 `hooks.json`만 보유한다.

## Scope
- **In**: `.codex/skills/` → `plugins/sdd-skills-codex/skills/` git mv, Codex manifest 2개 신설, installer skills root, README Installation 절, spec 표면(main.md In Scope·components.md Primary Source/코드 지도 경로) — spec 갱신은 spec-sync 단계에서 수행
- **Out**: 스킬 본문 내용 변경, 클코 배포 구조 변경, `.codex/hooks.json`, Codex 훅의 플러그인 번들링(위치 규약 미실측 — 별도 판단), claude/codex 스킬 단일화
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: 스킬 디렉토리를 이동한다

**Contracts**: `git mv .codex/skills plugins/sdd-skills-codex/skills` — 19개 스킬 디렉토리 전체가 rename으로 추적되고 내용 byte 불변. `.codex/`에는 `hooks.json`만 남는다. 스킬 내부 상대 참조(`../implementation-review/references/simplicity-contract.md` 등)는 skills 루트가 통째로 움직여 그대로 동작한다.

**Acceptance Criteria**:
- [ ] AC1: `plugins/sdd-skills-codex/skills/`에 SKILL.md 19개가 존재하고 `.codex/skills/`는 존재하지 않는다. 평가: `find ... -name SKILL.md | wc -l` = 19 + `ls .codex/skills` exit ≠ 0. (1등급)
- [ ] AC2: git이 전량 rename으로 기록한다(내용 불변 증명). 평가: `git status --short`에 R 마커, `git diff --cached --stat`에 rename 표기. (1등급)
- [ ] AC3: sibling reference 상대 경로가 새 위치에서 해석된다. 평가: `test -f plugins/sdd-skills-codex/skills/pr-review/../implementation-review/references/simplicity-contract.md` exit 0. (1등급)

**Target Files**:
- [M] `.codex/skills/**` → `plugins/sdd-skills-codex/skills/**` -- 전체 이동(rename)

### Task 2: Codex manifest 2개를 신설한다

**Contracts**: ① `.agents/plugins/marketplace.json` — `name: "sdd-skills-codex"`, owner, plugins 배열 1항목(`name: "sdd-skills-codex"`, `source: "./plugins/sdd-skills-codex"`), 스킬 개별 등록 없음(발견 위치 `skills/` 고정 규약에 의존). ② `plugins/sdd-skills-codex/.codex-plugin/plugin.json` — name·description·version. 두 파일 모두 유효 JSON.

**Acceptance Criteria**:
- [ ] AC1: 두 파일이 존재하고 `python3 -m json.tool` 통과. 평가: exit 0. (1등급)
- [ ] AC2: 두 manifest의 name이 `sdd-skills-codex`이고, repo 내 어떤 marketplace/plugin manifest에도 이름 충돌이 없다(클코 `sdd-skills`와 상이). 평가: grep 대조. (1등급)
- [ ] AC3: marketplace의 source 경로가 실재 디렉토리를 가리키고 그 아래 `skills/`가 있다. 평가: test -d. (1등급)

**Target Files**:
- [C] `.agents/plugins/marketplace.json` -- Codex 마켓 manifest(신규 표면이라 생성 필수)
- [C] `plugins/sdd-skills-codex/.codex-plugin/plugin.json` -- Codex 플러그인 manifest(동상)

### Task 3: installer의 skills root를 갱신한다

**Contracts**: `tools/install-codex-skill-bundle.py`의 `DEFAULT_SKILLS_ROOT = ".codex/skills"` → `"plugins/sdd-skills-codex/skills"`. 그 외 로직(비교·덮어쓰기·prune·agents 부재 허용) 불변. docstring의 경로 서술 동기화.

**Acceptance Criteria**:
- [ ] AC1: `_discover_skills(repo_root, DEFAULT_SKILLS_ROOT)`가 로컬 트리에서 19개를 발견한다. 평가: 함수 실행 출력. (1등급)
- [ ] AC2: `.codex/skills` 리터럴이 스크립트에 0건(주석 포함). 평가: grep 무히트. (1등급)

**Target Files**:
- [M] `tools/install-codex-skill-bundle.py` -- skills root 상수·docstring

### Task 4: README 경로 참조를 갱신한다

**Contracts**: Installation 절의 repo 내 소스 경로 4곳(`.codex/skills/` 서술 3곳 + LobeHub 프롬프트의 tree URL) → `plugins/sdd-skills-codex/skills/`. 설치 대상 경로(`~/.codex/skills`)는 불변이므로 건드리지 않는다. 개요에 Codex 플러그인 배포 1문장 추가(마켓 `.agents/plugins/marketplace.json`, 이름 `sdd-skills-codex`).

**Acceptance Criteria**:
- [ ] AC1: README에서 repo 소스로서의 `.codex/skills` 언급 0건(설치 대상 `~/.codex/skills`·`$CODEX_HOME/skills`는 잔존 허용). 평가: grep 검토. (1등급)
- [ ] AC2: `sdd-skills-codex` 이름과 새 경로가 README에 존재한다. 평가: grep. (1등급)

**Target Files**:
- [M] `README.md` -- Installation·개요

### Task 5: 이동 census (read-only)

**Acceptance Criteria**:
- [ ] AC1: `\.codex/skills` 변형(슬래시·글롭 포함)을 `.claude 스킬셋·plugins·.claude-plugin·.agents·AGENTS.md·CLAUDE.md·README.md·docs/·tools/`에 전수 grep — 잔존은 설치 대상 경로(`~/.codex/skills`·`$CODEX_HOME`) 등 의도 명시분 외 0건. spec(`_sdd/spec/*`) 잔존은 spec-sync 몫으로 별도 카운트만 보고. 평가: grep 출력 전수 검토. (1등급)

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- 플러그인 디렉토리명을 manifest 이름과 동일한 `plugins/sdd-skills-codex/`로 결정(사용자 트리 예시는 `plugins/sdd-skills/`였으나 이름 분리 지시가 후행하므로 디렉토리도 일치시킴 — 불일치 시 혼동 표면). 사용자 확인 불필요(합리 해석, 이견 시 rename 1회로 복구 가능).
- Codex 훅 번들링(플러그인 내 훅 위치 규약)은 Out — 위치 규약 실측 후 별도 feature. 확인 불필요.
- manifest는 사용자가 전달한 Codex 요구 구조(`.codex-plugin/plugin.json`)만 생성하고, Agent Plugins 1.0 표준의 플러그인 root `plugin.json` 병설은 만들지 않는다 — Codex 0.147 설치 실측에서 필요가 확인되면 별도 1파일 추가(추측으로 파일을 늘리지 않음, plan-review gate 1 Medium 반영). 확인 불필요.
