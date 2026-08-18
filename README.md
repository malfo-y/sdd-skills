# SDD Skills

Spec-Driven Development (SDD) workflow skills for Claude Code and Codex.

Codex bundle: 19 skills. Claude bundle: 21 skills (`git`·`second-opinion` 추가). custom agent는 없다 — `plan-review`·`implementation-review`·`pr-review`의 correctness 리뷰는 메인 루프가 직접 수행하고, simplicity 리뷰는 스킬 내장 계약(`implementation-review/references/simplicity-contract.md`)을 프롬프트로 주입한 범용 subagent가 수행한다. 그래서 양 번들 모두 skills-only로 배포된다. Claude는 `.claude-plugin/marketplace.json`(`sdd-skills`), Codex는 `.agents/plugins/marketplace.json`(`sdd-skills-codex` — Codex가 `.claude-plugin`을 legacy marketplace로도 읽으므로 이름을 분리)으로 각각 플러그인 배포한다. Codex 스킬 소스는 `plugins/sdd-skills-codex/skills/`다.

## Documentation

설치 후 SDD를 사용하기 위한 문서들입니다. 읽는 순서대로 정리되어 있습니다.

| 문서 | 내용 | 언제 읽나 |
|------|------|----------|
| [SDD_QUICK_START.md](docs/SDD_QUICK_START.md) | 빠른 시작 가이드. 스킬 목록과 시나리오별 사용법 | **처음 시작할 때** — 이것만 읽어도 바로 사용 가능 |
| [SDD_WORKFLOW.md](docs/SDD_WORKFLOW.md) | 전체 워크플로우와 각 문서 레이어가 쓰이는 시점 | 스킬을 더 효과적으로 쓰고 싶을 때 |
| [sdd.md](docs/sdd.md) | SDD 철학과 문제의식 — 왜 스펙 기반 개발인가 | SDD의 배경과 동기가 궁금할 때 |
| [SDD_CONCEPT.md](docs/SDD_CONCEPT.md) | 핵심 컨셉: 하네스 / 글로벌 스펙 / 임시 스펙 / 코드 / 보조 문서의 레이어 구조와 정보 배치 원칙 | 스펙 구조를 이해하고 싶을 때 |
| [SDD_SPEC_DEFINITION.md](docs/SDD_SPEC_DEFINITION.md) | 스펙의 정의 — 단순 문서가 아닌 화이트페이퍼형 기준 문서 | 스펙 작성 기준이 필요할 때 |
| [AUTOPILOT_GUIDE.md](docs/AUTOPILOT_GUIDE.md) | sdd-autopilot SDD goal harness 셋업 가이드 | 큰 목표를 native goal로 활성화해 여러 SDD path로 수렴시키고 싶을 때 |

> 영문 문서: `docs/en/` 디렉토리에 일부 문서의 영문 버전이 있습니다.

## Installation

### Claude Code (Plugin)

```
/plugin marketplace add malfo-y/sdd-skills
/plugin install sdd-skills@sdd-skills
```

> **Note**: 플러그인 설치 후 스킬을 활성화하려면 Claude Code를 재시작해야 합니다.

### Codex

#### Option A: GitHub 플러그인 설치 (권장)

GitHub 저장소를 Codex marketplace로 등록한 뒤 네이티브 플러그인을 설치한다.

기존 번들 스크립트나 수동 복사 방식으로 설치했다면 먼저 legacy 스킬을 확인하고 제거한다. 기본 실행은 preview-only이며 `--yes`를 붙이면 대상 항목을 `$CODEX_HOME/legacy-sdd-backup-<UTC>`로 옮겨 활성 경로에서 제거한다. 목록에 표시되지 않은 개인 스킬과 Codex 플러그인 캐시는 건드리지 않는다.

```bash
# 삭제 예정 항목 확인
curl -fsSL https://raw.githubusercontent.com/malfo-y/sdd-skills/main/tools/uninstall-codex-skill-bundle.py | python3 -

# 확인한 legacy 스킬 제거
curl -fsSL https://raw.githubusercontent.com/malfo-y/sdd-skills/main/tools/uninstall-codex-skill-bundle.py | python3 - --yes
```

```bash
codex plugin marketplace add malfo-y/sdd-skills
codex plugin add sdd-skills-codex@sdd-skills-codex
```

설치 상태는 아래 명령으로 확인할 수 있다.

```bash
codex plugin marketplace list
codex plugin list
```

이 플러그인은 skills-only다. 설치만으로 lifecycle 훅이 활성화되지 않으며, 훅은 `spec-create`·`spec-upgrade` 실행 시 대상 저장소에 project-local로 설치한다. 설치 후에는 Codex를 재시작하거나 새 task를 열어 스킬을 로드한다.

#### Option B: 번들 설치 스크립트 사용 (fallback)

`codex plugin` 명령을 사용할 수 없는 환경에서는 `plugins/sdd-skills-codex/skills/`를 한 번에 설치하는 번들 스크립트를 사용한다. 스크립트가 GitHub에서 직접 받아 설치하므로 **clone 없이 한 줄로 실행**할 수 있다(표준 라이브러리만 사용해 별도 의존성 설치가 필요 없다).

```bash
curl -fsSL https://raw.githubusercontent.com/malfo-y/sdd-skills/main/tools/install-codex-skill-bundle.py | python3 -
```

`uv`를 쓴다면 원격 스크립트를 그대로 실행해도 된다.

```bash
uv run https://raw.githubusercontent.com/malfo-y/sdd-skills/main/tools/install-codex-skill-bundle.py
```

저장소를 clone한 상태라면 로컬 경로로 실행해도 결과는 같다.

```bash
python3 tools/install-codex-skill-bundle.py
```

기본값:

- 기본 repo: `malfo-y/sdd-skills`
- 기본 ref: `main`
- 기본 설치 경로: `~/.codex/skills`
- 기존에 같은 이름의 스킬이 있으면 내용을 비교
- 내용이 같으면 건너뜀, 다르면 자동으로 덮어씀
- 사용자 `~/.codex/config.toml`은 수정하지 않음

자주 쓰는 예시(원격 실행이면 인자를 `python3 -` 뒤에 그대로 붙인다 — 예: `| python3 - --dry-run`):

```bash
# 설치 예정 항목만 확인
python3 tools/install-codex-skill-bundle.py --dry-run

# 이미 설치된 스킬을 내용과 상관없이 전부 교체
python3 tools/install-codex-skill-bundle.py --force

# 다른 포크/브랜치에서 설치
python3 tools/install-codex-skill-bundle.py --repo <owner>/<repo> --ref <branch-or-tag>

# CODEX_HOME 루트를 직접 지정
python3 tools/install-codex-skill-bundle.py --dest ~/.codex
```

설치 후에는 Codex를 재시작해야 새 스킬을 인식한다.

#### Option C: 수동 설치

`plugins/sdd-skills-codex/skills/`를 `$CODEX_HOME/skills/`에 복사한다. (`$CODEX_HOME` 기본값: `~/.codex`)

#### Codex discussion 스킬 사용 조건

`discussion` 스킬은 `request_user_input`에 의존하는 interactive skill이다. 따라서 Codex를 아래처럼 실행해 `default_mode_request_user_input`를 활성화해야 한다.

```bash
codex --enable default_mode_request_user_input
```

## Subagent Model Override

계획/구현 계열 스킬은 내부 subagent 호출에만 모델 override를 줄 수 있다. `implementation-review`·`pr-review`의 `--model`은 **simplicity dispatch에만** 적용된다 — correctness 리뷰는 메인 루프 직접 수행이라 override 대상이 아니다. 옵션을 생략하면 현재 세션/agent 기본값을 그대로 상속한다.

적용 대상:

- `implementation-review` (simplicity dispatch 한정)
- `pr-review` (simplicity dispatch 한정)

Claude Code:

```text
/implementation-review --model opus
```

Codex:

```text
/implementation-review --model gpt-5.6-terra --effort max
/pr-review --model gpt-5.6-sol --effort ultra
```

Codex에서는 model과 effort를 분리해서 쓴다. `gpt-5.6-sol-high` 같은 결합형 값 대신 `--model gpt-5.6-sol --effort high`를 사용한다. 위 모델과 `low`·`max`·`ultra` effort는 현재 Codex 0.146.0/Desktop schema의 예시이며, 실제 허용값은 실행 시 active `spawn_agent` schema가 노출한 enum을 따른다. 옵션을 생략하면 현재 세션/agent 기본값을 상속한다.
