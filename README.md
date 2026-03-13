# SDD Skills

Spec-Driven Development (SDD) workflow skills for Claude Code and Codex.

Codex 17 skills: spec-create, spec-review, spec-rewrite, spec-upgrade, spec-summary, spec-update-done, spec-update-todo, implementation-plan, implementation, implementation-review, feature-draft, pr-review, pr-spec-patch, discussion, ralph-loop-init, guide-create, spec-snapshot

## Installation

### Claude Code (Plugin)

```
/plugin marketplace add malfo-y/sdd-skills
/plugin install sdd-skills@sdd-skills
```

> **Note**: 플러그인 설치 후 스킬을 활성화하려면 Claude Code를 재시작해야 합니다.

### Codex

#### Option A: 번들 설치 스크립트 사용 (권장)

이 저장소에는 `.codex/skills/` 아래 스킬들을 한 번에 `~/.codex/skills`로 설치하는 래퍼 스크립트가 포함되어 있다.

```bash
python3 tools/install-codex-skill-bundle.py
```

기본값:

- 기본 repo: `malfo-y/sdd-skills`
- 기본 ref: `main`
- 기본 설치 경로: `~/.codex/skills`
- 기존에 같은 이름의 스킬이 있으면 기본적으로 건너뜀

자주 쓰는 예시:

```bash
# 설치 예정 항목만 확인
python3 tools/install-codex-skill-bundle.py --dry-run

# 이미 설치된 스킬도 전부 교체
python3 tools/install-codex-skill-bundle.py --force

# 다른 포크/브랜치에서 설치
python3 tools/install-codex-skill-bundle.py --repo <owner>/<repo> --ref <branch-or-tag>
```

설치 후에는 Codex를 재시작해야 새 스킬을 인식한다.

#### Option B: LobeHub Skills Marketplace 경유 설치

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

#### Option C: 수동 설치

`.codex/skills/` 내용을 `$CODEX_HOME/skills/`에 복사한다. (`$CODEX_HOME` 기본값: `~/.codex`)

#### Codex discussion 스킬 사용 조건

`discussion` 스킬은 `request_user_input`에 의존하는 interactive skill이다. 따라서 Codex를 아래처럼 실행해 `default_mode_request_user_input`를 활성화해야 한다.

```bash
codex --enable default_mode_request_user_input
```
