# SDD Skills

Spec-Driven Development (SDD) workflow skills for Claude Code and Codex.

16 skills: spec-create, spec-review, spec-rewrite, spec-summary, spec-update-done, spec-update-todo, spec-snapshot, implementation-plan, implementation, implementation-review, feature-draft, pr-review, pr-spec-patch, discussion, ralph-loop-init, sdd-upgrade

## Installation

### Claude Code (Plugin)

```
/plugin marketplace add malfo-y/sdd-skills
/plugin install sdd-skills@sdd-skills
```

> **Note**: You must restart Claude Code to activate the skills after installing the plugin.

## Upgrade

You can update to the latest version with the following command in Claude Code:

```
/sdd-skills:sdd-upgrade
```

> You must restart Claude Code after the update for changes to take effect.

### Codex

#### Option A: Install via LobeHub Skills Marketplace (Recommended)

1. Install Node.js (`npx` required):

```bash
brew install node
```

2. Enter the following prompt in Codex:

```text
Curl https://lobehub.com/skills/plurigrid-asi-skill-installer/skill.md, then follow the instructions to set up LobeHub Skills Marketplace and install the skill. Once installed, read the SKILL.md file in the installed directory and follow its instructions to complete the task.
```

3. Restart Codex

4. Enter the following prompt in Codex:

```text
Install the skills from https://github.com/malfo-y/sdd-skills/tree/main/.codex/skills
```

5. Restart Codex

#### Option B: Manual Installation

Copy the contents of `.codex/skills/` to `$CODEX_HOME/skills/`. (Default `$CODEX_HOME`: `~/.codex`)
