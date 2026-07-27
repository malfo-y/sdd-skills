# Feature Draft: SKILL.md frontmatter의 `version:` 필드 삭제

> 규모 판정: 적격 — 변경 요소 2개(40줄 삭제 / spec 결정·제약 정리)와 task가 1:1 대응하고, 삭제는 기계적이며 검증이 frontmatter 파싱 + grep census로 닫힌다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

PR #27이 `skill.json`을 삭제한 것과 **동일한 논법**을 `version:` 필드 자체에 적용한다. 그때 version 소스는 4곳에서 1곳(SKILL.md frontmatter)으로 줄었지만, 그 1곳의 **소비자도 0**이라는 사실이 리뷰 게이트 census로 드러났다:

- Codex CLI 0.142.5 / Claude Code 2.1.220 두 바이너리 모두 frontmatter에서 `name`·`description`만 사용한다(#27에서 실측).
- `tools/install-codex-skill-bundle.py`는 `SKILL.md` 존재만 확인하고 디렉토리를 통째 복사한다(`:284`, `:415`).
- `.claude-plugin/marketplace.json`은 스킬을 디렉토리 경로로 등록한다.
- `AGENTS.md`·`README.md`·`docs/`·agent 파일(claude `.md` 5 + codex `.toml` 5)에 스킬 version 참조 0건.

즉 남은 유지 근거는 "사람이 읽는 앵커" 하나였고, 그 비용은 실측된 드리프트(`guide-create` `.claude` 2.2.0 / `.codex` 2.4.0)와 운영 제약 1줄로 계상돼 있었다. 사용자가 삭제를 결정했다.

새로 고정되는 약속:

- **스킬 메타데이터 = `name` + `description`(+ 선택 키 `argument-hint`·`user_invocable`)**. 스킬 버전을 담는 필드·파일은 repo에 존재하지 않으며, 스킬 변경 이력은 git history가 단일 소스다.
- **"version lockstep" 개념 완전 소멸**: #27이 4필드 → 2필드로 줄인 검사 대상이 **0필드**가 된다. 앞으로 draft는 version AC를 쓰지 않는다.
- `_sdd/spec/main.md:149`의 운영 제약("스킬 version의 단일 소스는 frontmatter의 `version:` 필드다")은 대상이 사라져 **소멸**한다.
- `:150`의 `🚧 Planned`(미러 세대 격차)는 **본문 격차만 남기고 축소**된다 — `guide-create`의 version 격차(2.2.0/2.4.0)는 필드와 함께 사라지고, 본문 격차(`guide-create` 176/159줄, `spec-snapshot` 135/118줄 + codex `:28`에만 legacy uppercase 대응)는 그대로 남는다.

## Scope

- **In**: `.claude/skills/*/SKILL.md` 21개 + `.codex/skills/*/SKILL.md` 19개의 frontmatter `version:` 줄 삭제, 그리고 위 Change Summary가 요구하는 `_sdd/spec/` 동기화:
  - §3 결정 행 `Skill 정의 형식`을 `frontmatter가 name/description 등 메타데이터의 단일 소스이고, 스킬 버전을 담는 필드·파일은 두지 않는다(스킬 변경 이력 = git history)`로 **교체**한다. **별도 결정 행·guardrail은 신설하지 않는다** — 새 사실의 착지 지점은 이 행 하나다(v4.6.11이 쓴 anti-duplication 논법과 동일).
  - 운영 제약("스킬 version의 단일 소스는 frontmatter의 `version:` 필드다")은 소멸, `🚧 Planned`(미러 세대 격차)는 본문 격차만 남기고 축소.
  - **스킬 버전 산문 참조 정리는 열거가 아니라 판정 규칙으로 넘긴다**: `main.md`·`components.md`·`usage-guide.md`에서 `v?\d+\.\d+\.\d+` 전수 대조 후 **스킬 버전만** 정리하고 문서 자체 버전은 제외한다. rewrite는 두 갈래다 — **(i) 현재 계약 표기**는 괄호째 삭제(`` `sdd-autopilot`(v4.0.0)은 `` → `` `sdd-autopilot`은 ``), **(ii) 역사 앵커 서술**은 버전을 feature/사건 앵커로 치환(`v2.0.0에서 개명(F5)` → `F5에서 개명`) — 토큰만 지우면 `에서 …가 개명(F5)`처럼 문장이 깨진다. (열거하면 재드리프트한다 — 실제로 초안이 `components.md:15`·`:28`을 빠뜨렸다. `main.md:81`은 한 줄에 스킬 버전 `v4.0.0`과 문서 버전 `2.1.0`이 **공존**하므로 부분 편집이 필요하다.)
  - spec 표면은 `spec-sync`가 이 마커를 소비해 반영한다.
- **Out**: **문서 자체의 버전** — `main.md`의 `Spec Version`, `docs/AUTOPILOT_GUIDE.md`·`docs/en/`의 `2.1.0`, `.claude-plugin/marketplace.json`의 플러그인 metadata `"version": "1.0.0"`. 전부 스킬 버전이 아니라 그 문서/플러그인의 개정 번호다. `SKILL.md` 본문의 version 문자열 2건도 보존 대상이다: `guide-create` SKILL.md의 `**Version**: X.Y.Z`는 **생성될 가이드 문서**의 필드 템플릿이고, `git` SKILL.md의 `Which version?`은 충돌 해결 산문이다. agent 파일(version 필드 0건), `_sdd/` 기록물(과거 draft·work_log·decision_log·changelog의 version 언급은 시점 고정).
- **Out (근거 고정 — 재census 방지)**: `.claude/skills/spec-snapshot/SKILL.md`의 `user_invocable: true`는 `version`과 같은 부류가 **아니다** — Claude Code 2.1.220 바이너리가 `user_invocable`·`user-invocable`을 실제로 읽는다(문자열 2건 실측). Codex 바이너리는 0건이라 codex 짝에 없는 것도 설명된다. `argument-hint`도 두 런타임 표면에 남기며, Codex 번들 검증기의 `allowed_properties`(`{name, description, license, allowed-tools, metadata}`)에 없다는 점은 그 검증기가 큐레이션 패키징용이라 런타임 근거가 아니다 — 별건.
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: 40개 `SKILL.md` frontmatter에서 `version:` 줄 삭제

소비자가 0인 필드를 없애 드리프트가 생길 마지막 자리를 제거한다.

**Contracts**: 어느 `SKILL.md` frontmatter에도 `version` 키가 없다. 스킬 변경 이력의 단일 소스는 git history다.

**Acceptance Criteria**:
- [ ] AC1: 40개 `SKILL.md` 전부에서 frontmatter를 YAML로 파싱했을 때 `version` 키가 0건이다(삭제 전 40건).
- [ ] AC2: 40개 전부 frontmatter 파싱에 성공하고 `name`·`description`이 비어 있지 않다 — 줄 삭제로 YAML이 깨진 파일 0건.
- [ ] AC3: 변경된 각 파일의 diff가 `-version: …` 1줄 삭제뿐이다(추가 라인 0) — frontmatter 밖 본문은 자동으로 무변경이 된다.

**Target Files**:
- [M] `.claude/skills/*/SKILL.md` -- 21개, frontmatter `version:` 줄 삭제
- [M] `.codex/skills/*/SKILL.md` -- 19개, 동일

---

### Task 2: `version` 잔재 census 검증 (read-only)

`version`은 흔한 단어라 무차별 grep이 정당한 용례(문서 자체 버전·생성 템플릿·산문)를 오탐한다. **frontmatter 키**만 겨냥하는 census로 잔재와 보존 대상을 함께 고정한다.

**Acceptance Criteria**:
- [ ] AC1: live 표면(`.claude/`·`.codex/`·`.claude-plugin/`·`tools/`·`docs/`·`AGENTS.md`·`CLAUDE.md`·`README.md`) 전수에서 `^version:`으로 시작하는 줄이 0건이다 — Change Summary의 "소비자 0" 주장이 완료 시점에 falsifiable해진다.
- [ ] AC2: 보존 대상 2건이 실재한다 — `.claude/skills/guide-create/SKILL.md`에 `**Version**: X.Y.Z` 1건, `.claude/skills/git/SKILL.md`에 `Which version?` 1건. (오탐 방지 가드: census가 이들을 지웠다면 실패한다.)
- [ ] AC3: 변경 파일 전체가 Task 1의 Target Files + 이번 draft(및 `_processed_` 마킹)뿐이다 — `git diff --name-only 4e9b0c0`(작업 시작 커밋) 기준 여집합. 범위 밖 문서 버전 무변경도 이 하나로 닫힌다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- **미러 본문 세대 격차 (확신도 높음 — 실측)**: `guide-create` 176/159줄, `spec-snapshot` 135/118줄(codex `:28`에만 legacy uppercase 대응). version 필드가 사라져도 더 강한 신호가 남는다 — `.codex/skills/guide-create/SKILL.md`에는 claude 쪽 본문의 `**Version**: X.Y.Z` 템플릿 줄이 **아예 없다**(grep 0건). `spec-sync`가 `:150` planned를 **본문 줄 수·템플릿 블록 유무·규칙 차이로 재서술**하면 재실측 없이 닫힌다. 어느 쪽이 canonical인지는 본문 대조가 선행되어야 해 이번 범위 밖이다.
