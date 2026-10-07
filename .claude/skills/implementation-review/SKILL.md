---
name: implementation-review
description: "sdd-orchestrator의 호환 별칭. 예전 단계 스킬 이름 \"implementation-review\"으로 부를 때 사용한다 — sdd-orchestrator를 호출 이름 implementation-review 범위로 실행한다."
---

# implementation-review (sdd-orchestrator 별칭)

이 이름은 `sdd-orchestrator`의 호환 별칭이다. 단계 규칙과 범위는 `sdd-orchestrator`가 단일 소스이고 이 파일에는 없다.

1. 사용자에게 한 줄 알린다: "`implementation-review`은 `sdd-orchestrator`의 별칭이다 — 호출 이름 `implementation-review` 범위로 실행한다."
2. 이 스킬 디렉터리의 형제 경로 `../sdd-orchestrator/SKILL.md`를 읽고, 호출 이름 = `implementation-review`으로 그 스킬의 `단계와 진입` 호출 이름 표 행을 그대로 따른다. 그 스킬이 말하는 "이 스킬 디렉터리"(base directory)는 `../sdd-orchestrator/`다. 사용자의 요청·인자(draft 경로, `--model` 등)는 그대로 넘긴다. 다른 스킬을 호출하지 않는다.
