# SDD Skills

Spec-Driven Development (SDD) workflow skills for Claude Code and Codex.

15 skills: spec-create, spec-review, spec-rewrite, spec-summary, spec-update-done, spec-update-todo, implementation-plan, implementation, implementation-review, feature-draft, pr-review, pr-spec-patch, discussion, ralph-loop-init, sdd-upgrade

## Installation

### Claude Code (Plugin)

```
/plugin marketplace add malfo-y/sdd-skills
/plugin install sdd-skills@sdd-skills
```

> **Note**: 플러그인 설치 후 스킬을 활성화하려면 Claude Code를 재시작해야 합니다.

## Upgrade

Claude Code에서 아래 명령어로 최신 버전으로 업데이트할 수 있습니다:

```
/sdd-skills:sdd-upgrade
```

> 업데이트 후 Claude Code를 재시작해야 변경사항이 적용됩니다.

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
