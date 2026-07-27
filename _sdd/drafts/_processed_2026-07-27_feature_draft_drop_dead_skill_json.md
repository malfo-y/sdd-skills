# Feature Draft: 죽은 메타데이터 `skill.json` 삭제, SKILL.md frontmatter를 version 단일 소스로

> 규모 판정: 적격 — 변경 요소 3개(37파일 삭제 / version 단일 소스화 / 잔재 서술 정리)와 task가 1:1 대응하고, 삭제는 기계적이며 검증이 grep census로 닫힌다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

`skill.json`은 **두 런타임 어느 쪽도 읽지 않는 죽은 메타데이터**다. 2026-02-14 `48bee08 add skill.json files`로 도입된 이래 한 번도 로드된 적이 없다. 실측 근거:

- **Codex CLI 0.142.5** 네이티브 바이너리(`@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex`) 문자열: `skill.json` **0회**, `SKILL.md` **75회**(+ YAML frontmatter 파서·검증기). `~/.codex/skills/`의 비-repo 스킬 3종(`paper-deep-dive`·`jira_wiki_project`·`daily-time-boxing`)이 `skill.json` 없이 정상 동작한다.
- **Claude Code 2.1.220** 바이너리: `skill.json` **0회**(검출된 2건은 별개 파일명 `.forked-skill.json`), `SKILL.md` **222회**.
- `.claude-plugin/marketplace.json`은 스킬을 **디렉토리 경로**로 등록한다(`"skills": ["./.claude/skills/discussion", ...]`) — `skill.json`을 참조하지 않는다.
- repo 내 스크립트·CI의 `skill.json` 참조 0건. 유일한 live 스크립트인 `tools/install-codex-skill-bundle.py`는 `SKILL.md` 존재만 확인하고(`:284`, `:415`) 디렉토리를 통째로 복사하며 기존 설치는 제거 후 재복사하므로, 삭제로 깨지지 않고 기설치본의 잔재 `skill.json`도 재설치 시 사라진다.
- 이미 `skill.json`이 없는 스킬 3종(`.claude/investigate`, `.claude/spec-snapshot`, `.codex/spec-snapshot`)이 정상 동작 중이다.

읽히지 않으므로 드리프트가 감지되지 않는다. 실제로 40개 스킬 표면 중 **12건**의 version 불일치가 조용히 누적됐다(`discussion` 1.5.0/1.2.0, `implementation-review` 7.0.0/2.1.0·3.0.0, `investigate` 4.0.0/1.0.0, `pr-review` 4.0.0/2.0.0, `spec-create` 1.10.0/1.9.1 등). 값을 맞추는 것은 증상 치료이므로 파일을 없앤다.

새로 고정되는 약속:

- **version 단일 소스 = `SKILL.md` frontmatter의 `version:` 필드**. 스킬 버전을 담는 다른 파일은 없다.
- **"version 4필드 lockstep" 개념 소멸**: 미러 쌍당 검사 대상이 4필드(SKILL.md 2 + skill.json 2)에서 **2필드**(SKILL.md 2)로 줄어든다. 앞으로 draft가 version AC를 쓸 때 4필드를 요구하지 않는다.
- `_sdd/spec/main.md`의 `🚧 Planned` 항목("`implementation-review` version 4필드 불일치")은 이 변경으로 **대상 자체가 사라져** 소멸한다 — 정렬이 아니라 제거로 종결한다. 단 상위 불릿("일부 version metadata 갱신은 문서 편집 discipline에 의존한다")은 여전히 참이고 실재 사례가 남아 있으므로(`guide-create` 2.2.0/2.4.0, `spec-snapshot` 본문 격차), `spec-sync`는 이 항목을 **삭제가 아니라 치환**한다 — 그러지 않으면 repo에 유일하게 남은 live version 드리프트가 spec 어디에도 기록되지 않는다.

## Scope

- **In**: `.claude/skills/*/skill.json` 19개 + `.codex/skills/*/skill.json` 18개 삭제, `.claude/skills/spec-snapshot/SKILL.md`에 `version:` 추가(현재 frontmatter에 없음 — 삭제 후 version 소스가 0이 되는 유일한 스킬), `_sdd/env.md` Runtime 절의 작업 대상 목록에서 `skill.json` 제거, 그리고 위 Change Summary가 요구하는 `_sdd/spec/` 동기화(main.md의 planned 항목 종결 + version 단일 소스 서술). spec 표면은 `spec-sync`가 이 마커를 소비해 반영한다.
- **Out**: `SKILL.md` frontmatter의 다른 키 정리(Codex 번들 검증기의 `allowed_properties = {name, description, license, allowed-tools, metadata}`에 `version`·`argument-hint`가 없지만, 그 검증기는 큐레이션 저장소용 패키징 스크립트이고 런타임 로더가 아니며 현재 스킬이 정상 로드된다 — 별건), `_sdd/` 기록물(`decision_log`·`changelog`·`logs/prev/`의 과거 `skill.json` 언급은 시점 고정 기록이라 갱신 대상 아님), `.claude-plugin/marketplace.json`(경로 등록이라 무변경).
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: `skill.json` 37개 삭제

읽히지 않는 파일을 없애 드리프트가 생길 자리를 제거한다.

**Contracts**: 삭제 후 repo에 `skill.json`이라는 이름의 파일은 존재하지 않는다. 스킬 로딩 표면은 `SKILL.md`(+ `marketplace.json`의 디렉토리 등록)뿐이다.

**Acceptance Criteria**:
- [ ] AC1: `find .claude/skills .codex/skills -name skill.json` 결과가 0건이다(삭제 전 19 + 18 = 37건).
- [ ] AC2: `git status`에서 삭제로 기록된 파일이 정확히 37개이고, 그 외 삭제 파일이 없다.
- [ ] AC3: `.claude-plugin/marketplace.json`이 무변경이고, `skills` 배열의 21개 경로가 모두 실재하는 디렉토리를 가리킨다(각 디렉토리에 `SKILL.md` 존재).

**Target Files**:
- [D] `.claude/skills/*/skill.json` -- 19개 (discussion, feature-draft, git, goal-init, guide-create, implementation, implementation-review, plan-review, pr-review, ralph-loop-init, sdd-autopilot, second-opinion, spec-create, spec-review, spec-rewrite, spec-summary, spec-sync, spec-upgrade, write-phased)
- [D] `.codex/skills/*/skill.json` -- 18개 (claude 목록에서 `git`·`second-opinion` 제외, `investigate` 포함)

---

### Task 2: `spec-snapshot` claude 미러에 `version` 추가

삭제와 무관하게 **이전부터** version 소스가 없던 유일한 스킬을 같은 커밋에서 보정한다 — `.claude/skills/spec-snapshot/`는 `skill.json`도 없고 `SKILL.md` frontmatter에도 `version:`이 없어, 이 변경 전에도 version 소스가 0이었다(codex 짝은 `1.2.0`). frontmatter를 version 단일 소스로 세우는 이번 변경에서 유일한 빈칸이라 함께 채운다(범위 확장 1파일).

**Acceptance Criteria**:
- [ ] AC1: `.claude/skills/spec-snapshot/SKILL.md` frontmatter에 `version: 1.2.0`이 존재한다(codex 짝과 동일 값 — 미러 대칭).
- [ ] AC2: 모든 스킬(claude 21 + codex 19)의 `SKILL.md` frontmatter에 `version:`이 1건씩 존재한다 — version 소스가 0인 스킬 0건.
- [ ] AC3: `spec-snapshot` 미러 쌍의 두 `version`이 `1.2.0`으로 일치한다. (전수 일치는 이번 범위가 아니다 — Open Questions 참조.)

**Target Files**:
- [M] `.claude/skills/spec-snapshot/SKILL.md` -- frontmatter에 `version: 1.2.0` 추가

---

### Task 3: `_sdd/env.md`의 작업 대상 목록에서 `skill.json` 제거

Part 2가 직접 고치는 유일한 live `skill.json` 서술을 없앤다(`_sdd/spec/main.md:150`의 planned 항목도 live지만 그건 `spec-sync` 소관이고, 나머지 언급은 전부 기록물이다).

**Acceptance Criteria**:
- [ ] AC1: `_sdd/env.md`에 `skill.json` 리터럴이 0건이고, Runtime 절의 작업 대상 목록이 나머지 항목(`Markdown 문서`·`SKILL.md`·예시/참고 문서)을 그대로 유지한다.

**Target Files**:
- [M] `_sdd/env.md` -- Runtime 절 작업 대상 목록 1줄

---

### Task 4: `skill.json` 잔재 census 검증 (read-only)

`skill.json`은 파일명·경로·서술 형태로 여러 표면에 흩어질 수 있어, 전수 열거 없이는 잔존이 재발한다. live 표면과 기록물의 경계도 함께 고정한다.

**Acceptance Criteria**:
- [ ] AC1: Part 2가 소유하는 live 표면(`.claude/`·`.codex/`·`.claude-plugin/`·`tools/`·`docs/`·`AGENTS.md`·`CLAUDE.md`·`README.md`·`_sdd/env.md`) 전수 grep에서 `skill.json` 리터럴이 0건이다(대소문자 무시).
- [ ] AC2: 변경 파일 전체가 Task 1~3의 Target Files + 이번 draft의 `_processed_` 마킹뿐이다 — `git diff --name-only ee677ca`(작업 시작 커밋) 출력에 그 밖의 경로가 없다. 여집합 형태라 기록물 경계를 열거하지 않고도 잔재 수정이 검출된다.
- [ ] AC3: `_sdd/spec/main.md`에 남는 `skill.json`·`4필드` 언급은 `:150`의 planned 항목 1줄뿐이며(구현 시점 허용 잔존), 그 소멸은 `spec-sync` 단계에서 확인한다 — Part 2는 이 파일을 수정하지 않는다.
- [ ] AC4: `git diff --check`가 무출력이다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- **`guide-create` 미러 version 격차 (확신도 높음 — 실측 확인)**: `.claude` `2.2.0` vs `.codex` `2.4.0`으로 **SKILL.md 본문 세대가 갈려 있다**(짝 `skill.json`도 같은 값이라 skill.json 드리프트가 아니다). 어느 쪽이 canonical인지는 본문 대조가 선행되어야 해서 이번 범위 밖으로 뒀다. **사용자 확인 필요**: 별건으로 둘지, planned로 고정할지.
- **`spec-snapshot` 미러도 본문 세대가 갈려 있다 (확신도 높음 — 리뷰 게이트 실측)**: claude 135줄 / codex 118줄이고 codex `:28`에만 legacy uppercase(`DECISION_LOG.md`) 대응 규칙이 있다. 이번에 claude 쪽에 codex와 같은 `1.2.0`을 찍었으므로 **version만으로는 이 격차가 보이지 않는다**. 값을 임의로 다르게 정하면 "어느 쪽이 구세대인지"를 근거 없이 단정하게 되므로 값은 그대로 두고 격차를 여기 기록한다 — `guide-create`와 같은 버킷(미러 본문 세대 격차, 본문 대조 선행 필요)이다.
- **`version:` 필드 자체의 소비자가 0 (확신도 중간 — 소비자 census 실측)**: 이번 변경으로 version 소스는 SKILL.md 1곳이 됐으나, 그 값을 읽는 런타임·스크립트·문서가 0이다(두 바이너리 모두 name/description만 사용, `tools/`는 SKILL.md 존재만 확인, `marketplace.json`·`AGENTS.md`·`README.md`·`docs/` 0건). 추적 canonical은 `_sdd/spec/main.md:133`이 이미 git-history-first로 선언한다. **사용자 확인 필요**: `skill.json`과 같은 논법으로 40개 `version:` 줄도 후속 feature에서 없앨지, 사람이 읽는 앵커로 유지할지.
- **Codex frontmatter 허용 키 (확신도 낮음 — 검증기 성격 추정)**: Codex 번들 검증기가 `allowed_properties = {name, description, license, allowed-tools, metadata}`로 제한하는데 우리는 `version`·`argument-hint`를 쓴다. 다만 같은 스크립트에 `Repo path to list (default: skills/.curated)`가 있어 **큐레이션 저장소용 패키징 검증기**로 보이고 런타임 로더가 아니며, 현재 스킬이 정상 로드된다. **사용자 확인 필요**: `version`을 허용 키인 `metadata:` 하위로 옮기는 후속 작업을 planned로 고정할지, 근거가 약하니 무시할지.
