# SDD Skills

Spec-Driven Development (SDD) workflow skills for Claude Code and Codex.

16 skills: spec-create, spec-review, spec-rewrite, spec-upgrade, spec-summary, spec-update-done, spec-update-todo, implementation-plan, implementation, implementation-review, feature-draft, pr-review, pr-spec-patch, discussion, ralph-loop-init, guide-create

## Installation

### Claude Code (Plugin)

```
/plugin marketplace add malfo-y/sdd-skills
/plugin install sdd-skills@sdd-skills
```

> **Note**: 플러그인 설치 후 스킬을 활성화하려면 Claude Code를 재시작해야 합니다.

### Codex

#### Option A: LobeHub Skills Marketplace 경유 설치 (권장)

1. Node.js 설치 (`npx` 필요):

```bash
brew install node
```

2. Codex에 아래 프롬프트 입력:

```text
Curl https://lobehub.com/skills/plurigrid-asi-skill-installer/skill.md, then follow the instructions to set up LobeHub Skills Marketplace and install the skill. Once installed, read the SKILL.md file in the installed directory and follow its instructions to complete the task.
```

3. Codex 재시작

4. Codex에 아래 프롬프트 입력:

```text
https://github.com/malfo-y/sdd-skills/tree/main/.codex/skills 에 있는 스킬들을 설치해 줘
```

5. Codex 재시작

#### Option B: 수동 설치

`.codex/skills/` 내용을 `$CODEX_HOME/skills/`에 복사합니다. (`$CODEX_HOME` 기본값: `~/.codex`)

#### Codex discussion 스킬 사용 조건

`discussion` 스킬은 `request_user_input`에 의존하는 interactive skill이다. 따라서 Codex를 아래처럼 실행해 `default_mode_request_user_input`를 활성화해야 한다.

```bash
codex --enable default_mode_request_user_input
```
