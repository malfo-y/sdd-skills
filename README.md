# SDD Skills

Spec-Driven Development (SDD) workflow skills for Claude Code and Codex.

Codex bundle: 19 skills + 9 custom agents + config defaults. Claude bundle: 21 skills + 9 agents.

## Documentation

설치 후 SDD를 사용하기 위한 문서들입니다. 읽는 순서대로 정리되어 있습니다.

| 문서 | 내용 | 언제 읽나 |
|------|------|----------|
| [SDD_QUICK_START.md](docs/SDD_QUICK_START.md) | 빠른 시작 가이드. 스킬 목록과 시나리오별 사용법 | **처음 시작할 때** — 이것만 읽어도 바로 사용 가능 |
| [SDD_WORKFLOW.md](docs/SDD_WORKFLOW.md) | 전체 워크플로우 상세 가이드. 스킬별 좋은/나쁜 입력 예시 포함 | 스킬을 더 효과적으로 쓰고 싶을 때 |
| [sdd.md](docs/sdd.md) | SDD 철학과 문제의식 — 왜 스펙 기반 개발인가 | SDD의 배경과 동기가 궁금할 때 |
| [SDD_CONCEPT.md](docs/SDD_CONCEPT.md) | 핵심 컨셉: 글로벌 스펙 vs 임시 스펙의 두 단계 구조 | 스펙 구조를 이해하고 싶을 때 |
| [SDD_SPEC_DEFINITION.md](docs/SDD_SPEC_DEFINITION.md) | 스펙의 정의 — 단순 문서가 아닌 화이트페이퍼형 기준 문서 | 스펙 작성 기준이 필요할 때 |
| [AUTOPILOT_GUIDE.md](docs/AUTOPILOT_GUIDE.md) | sdd-autopilot 메타스킬 사용 가이드 | 전체 파이프라인을 자동화하고 싶을 때 |

> 영문 문서: `docs/en/` 디렉토리에 일부 문서의 영문 버전이 있습니다.

## Installation

### Claude Code (Plugin)

```
/plugin marketplace add malfo-y/sdd-skills
/plugin install sdd-skills@sdd-skills
```

> **Note**: 플러그인 설치 후 스킬을 활성화하려면 Claude Code를 재시작해야 합니다.

### Codex

#### Option A: 번들 설치 스크립트 사용 (권장)

이 저장소에는 `.codex/skills/`, `.codex/agents/`, `.codex/config.toml`을 한 번에 설치하는 번들 스크립트가 포함되어 있다.

```bash
python3 tools/install-codex-skill-bundle.py
```

기본값:

- 기본 repo: `malfo-y/sdd-skills`
- 기본 ref: `main`
- 기본 설치 경로: `~/.codex/skills` (`agents`는 `~/.codex/agents`, config는 `~/.codex/config.toml`)
- 기존에 같은 이름의 스킬/에이전트가 있으면 내용을 비교
- 내용이 같으면 건너뜀, 다르면 자동으로 덮어씀
- 기존 `config.toml`이 있으면 `[agents]` 섹션만 안전하게 병합

자주 쓰는 예시:

```bash
# 설치 예정 항목만 확인
python3 tools/install-codex-skill-bundle.py --dry-run

# 이미 설치된 스킬/에이전트를 내용과 상관없이 전부 교체
python3 tools/install-codex-skill-bundle.py --force

# 다른 포크/브랜치에서 설치
python3 tools/install-codex-skill-bundle.py --repo <owner>/<repo> --ref <branch-or-tag>

# CODEX_HOME 루트를 직접 지정
python3 tools/install-codex-skill-bundle.py --dest ~/.codex
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

`.codex/skills/`는 `$CODEX_HOME/skills/`, `.codex/agents/`는 `$CODEX_HOME/agents/`에 복사하고, `.codex/config.toml`의 `[agents]` 설정도 `$CODEX_HOME/config.toml`에 반영한다. (`$CODEX_HOME` 기본값: `~/.codex`)

#### Codex discussion 스킬 사용 조건

`discussion` 스킬은 `request_user_input`에 의존하는 interactive skill이다. 따라서 Codex를 아래처럼 실행해 `default_mode_request_user_input`를 활성화해야 한다.

```bash
codex --enable default_mode_request_user_input
```
