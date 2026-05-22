# Implementation Review: Strategic Code Map Spec Skills

**Review Date**: 2026-05-22
**Review Mode**: Tier 1
**Reference**: _sdd/drafts/2026-05-22_feature_draft_strategic_code_map_spec_skills.md

## 1. Findings

### Critical

- 없음.

### High

- `.claude/skills/feature-draft/SKILL.md`와 `.claude/agents/feature-draft.md`가 `Strategic Code Map` 검증 계약을 동일하게 공유하지 않는다. Agent에는 `Touchpoints` 재검증, `Target Files` 현재 코드 확인, stale hint 최종 점검 문장이 들어 있지만 skill에는 빠져 있다. 이는 draft의 C6/C7, "agent <-> skill mirror parity" 요구를 직접 깨뜨린다.
  - Missing from skill vs present in agent:
    - `.claude/agents/feature-draft.md:158`: `Touchpoints`가 code map을 참고했더라도 현재 코드로 재확인한다.
    - `.claude/agents/feature-draft.md:216`: code map 경로도 현재 코드 존재성과 변경 관련성을 확인한 뒤 Target Files에 넣는다.
    - `.claude/agents/feature-draft.md:240`: stale hint를 그대로 옮기지 않았는지 최종 점검한다.
  - 대응: 위 세 문장을 `.claude/skills/feature-draft/SKILL.md`의 대응 위치에 복사하거나, skill 본문을 agent 본문으로 재동기화한다.

### Medium

- Codex와 Claude의 `feature-draft` skill은 같은 기능을 가리키지만 Hard Rule 번호 체계가 다르다. Codex는 `Strategic Code Map`을 Rule 6, Self-Contained Authoring을 Rule 11, Minimum-Code Mandate를 Rule 12로 둔다. Claude는 Self-Contained Authoring을 Rule 9, Minimum-Code Mandate를 Rule 10, `Strategic Code Map`을 Rule 11로 둔다. 본문 내부 참조는 각 파일 안에서는 대체로 맞지만, 같은 스킬을 양 플랫폼에 mirror한다는 운영 목표에는 취약하다.
  - 예: `.codex/skills/feature-draft/SKILL.md:43`, `.codex/skills/feature-draft/SKILL.md:48`, `.codex/skills/feature-draft/SKILL.md:54`
  - 예: `.claude/skills/feature-draft/SKILL.md:36`, `.claude/skills/feature-draft/SKILL.md:39`, `.claude/skills/feature-draft/SKILL.md:44`
  - 대응: rule 번호를 양쪽에서 맞추거나, cross-platform 유지보수 대상 문장에서는 번호 대신 `Self-Contained Authoring`, `Minimum-Code Mandate`, `Strategic Code Map as hint` 같은 명명된 rule label을 사용한다.

- `.codex/skills/feature-draft/SKILL.md`와 `.codex/agents/feature-draft.toml`은 normalized body 기준으로도 완전 동일하지 않다. 의미 차이는 작지만, final checklist에서 `Strategic Code Map` 검증 항목의 순서가 다르다. 현재는 실행 계약 차이를 만들 가능성은 낮지만, "본문은 agent developer_instructions 복사본"이라는 notice와는 맞지 않는다.
  - Skill: `.codex/skills/feature-draft/SKILL.md:264-267`
  - Agent: `.codex/agents/feature-draft.toml:261-264`
  - 대응: 한쪽 순서를 다른 쪽에 맞춰 기계적으로 동일하게 만든다.

### Low

- `.codex/skills/spec-create/SKILL.md`의 Structure Decision 표는 `분할 축` 열에 `small repo | main.md appendix`를 넣는다. 실제로 small repo는 분할하지 않고 appendices 배치만 결정하므로, 열 이름이 약간 어긋난다. 기능상 문제는 아니지만 "스펙이 작으면 파일 하나" 원칙과 `Strategic Code Map` 배치 원칙을 처음 읽는 사람이 혼동할 수 있다.
  - Location: `.codex/skills/spec-create/SKILL.md:88-95`
  - 대응: 열 이름을 `navigation axis / placement`로 바꾸거나, small repo case를 표 밖의 placement rule로 분리한다.

- `feature-draft`의 context gathering 문장 `summary/reference surface 등`은 discovery 기준이 약간 느슨하다. `_sdd/spec/*.md`를 모두 읽는 규칙이 바로 앞에 있으므로 큰 문제는 아니지만, LLM이 어떤 supporting surface를 우선 탐색해야 하는지 애매할 수 있다.
  - Codex: `.codex/skills/feature-draft/SKILL.md:160-162`
  - Claude: `.claude/skills/feature-draft/SKILL.md:95-98`
  - 대응: `main.md`, `components.md`, `code-map.md`, 그리고 `Strategic Code Map` heading을 가진 `_sdd/spec/*.md` 순서로 찾는다고 명시한다.

- `Strategic Code Map`은 hint일 뿐 현재 코드로 재확인해야 한다는 문장이 여러 층위에 반복된다. 반복 자체는 안전장치로 볼 수 있으나, 이번처럼 skill/agent 중 일부 위치만 갱신되는 drift를 만들기 쉽다.
  - 대응: 필수 규칙 1곳을 canonical sentence로 두고, 나머지는 "Hard Rule N/label 참조"로 줄인다. 단, rule 번호를 쓸 경우 위 Medium finding의 번호 불일치부터 해결해야 한다.

## 2. Progress Overview

Draft 명세의 큰 축은 대부분 구현됐다.

- `docs/SDD_SPEC_DEFINITION.md`와 `docs/en/SDD_SPEC_DEFINITION.md`에 `Strategic Code Map` 정의와 thin global spec과의 관계가 추가됐다.
- `spec-create`는 single-file default를 유지하면서 compact appendix vs supporting file 배치 기준을 갖게 됐다.
- `spec-review`, `spec-rewrite`, `spec-upgrade`, `spec-summary`는 Codex/Claude skill 파일이 byte-level 동일하다.
- `spec-update-todo`, `spec-update-done`, `spec-review`의 agent <-> skill은 frontmatter와 mirror notice를 제외한 normalized body 기준으로 일치한다.
- `feature-draft`는 `Strategic Code Map`을 hint로만 쓰고 `Touchpoints`/`Target Files`를 현재 코드로 재검증해야 한다는 방향이 Codex에는 잘 반영됐고, Claude agent에도 반영됐다. 다만 Claude skill 누락 때문에 mirror 요구는 부분 미충족이다.

## 3. Verification Summary

검증한 항목:

- `git diff --check`: PASS
- `.codex/agents/*.toml` Python TOML parse: PASS
- `rg "Strategic Code Map|primary navigation axis|exhaustive inventory|Target Files" docs .codex .claude`: 기대 키워드 반영 확인
- Codex/Claude skill byte compare:
  - SAME: `spec-create`, `spec-review`, `spec-rewrite`, `spec-upgrade`, `spec-summary`
  - DIFF: `spec-update-todo`, `spec-update-done`, `feature-draft`
- Normalized skill-agent compare(frontmatter와 mirror notice 제외):
  - SAME: `spec-review`, `spec-update-todo`, `spec-update-done` for both Codex and Claude
  - DIFF: `feature-draft` for both Codex and Claude

`spec-update-todo`와 `spec-update-done`의 Codex/Claude skill 차이는 기존 host-specific 문구와 legacy fallback 차이가 섞여 있으며, 이번 `Strategic Code Map` 변경 자체의 핵심 계약 차이로 보이지 않는다. 반면 `feature-draft`는 이번 변경의 핵심 문장이 일부 mirror 대상에 빠져 있어 실제 수정 대상이다.

## 4. Recommendations

### Must

1. `.claude/agents/feature-draft.md`의 세 Strategic Code Map 검증 문장을 `.claude/skills/feature-draft/SKILL.md`에 반영한다.
2. `.codex/skills/feature-draft/SKILL.md`와 `.codex/agents/feature-draft.toml`의 final checklist 순서를 동일하게 맞춘다.

### Should

1. Codex/Claude `feature-draft`의 Hard Rule 번호 체계를 맞춘다. 번호 정렬이 부담이면 번호 참조를 명명된 label 참조로 바꾼다.
2. `feature-draft`의 supporting surface discovery 문장을 더 구체화한다.
3. `spec-create`의 Structure Decision 표 열 이름 또는 small repo row를 다듬는다.

### Could

1. mirror 검증용 스크립트를 추가한다. 최소 기능은 skill frontmatter와 agent wrapper를 제거한 뒤 normalized body를 비교하는 것이다. 이번처럼 "거의 같은데 핵심 한 줄 누락"인 상태를 빠르게 잡을 수 있다.

## 5. Conclusion

전체 구현 방향은 draft 명세와 잘 맞는다. 특히 `spec-create`와 주요 review/rewrite/upgrade 계열은 `Strategic Code Map`을 thin global spec의 보조 navigation surface로 다루도록 잘 업데이트됐다.

다만 `feature-draft` mirror가 아직 깨져 있다. Claude skill에는 핵심 재검증 문장 3개가 빠졌고, Codex skill-agent도 순서 차이 때문에 "복사본" notice와 완전히 일치하지 않는다. 다음 수정은 코드 로직보다 문서 동기화 작업에 가깝고, 범위는 작다.
