# SDD Skills

Spec-Driven Development (SDD) workflow skills for Claude Code and Codex.

요구사항을 스펙과 실행 계획으로 정리하고, 구현·검증 결과를 다시 스펙에 반영하는 스킬 모음이다. 장기적으로 유지할 판단은 `_sdd/spec/`에, 변경별 계획은 `_sdd/drafts/`에 남겨 다음 세션에서도 이어서 작업한다.

| 런타임 | 스킬 수 | 소스 |
|--------|---------|------|
| Claude Code | 20 | [`.claude/skills/`](.claude/skills/) — 공통 스킬 + `git`, `second-opinion` |
| Codex | 18 | [`plugins/sdd-skills-codex/skills/`](plugins/sdd-skills-codex/skills/) |

## Quick Start

1. 아래 [Installation](#installation)에서 사용하는 런타임의 플러그인을 설치한다.
2. 작업할 저장소에서 `spec-create`를 호출해 스펙과 작업 하네스를 만든다. 기존 스펙의 구형 포맷을 옮길 때는 `spec-upgrade`를 쓴다.
3. `feature-draft`로 변경을 계획하고, 생성된 draft를 지정해 `implementation`을 실행한다.
4. 검증된 변경을 `spec-sync`로 스펙에 반영한다.

스킬은 이름을 명시한 자연어로 요청할 수 있다. 각 단계가 끝난 뒤 다음 요청을 보낸다.

```text
spec-create 스킬로 이 저장소의 스펙과 작업 하네스를 만들어줘.
feature-draft 스킬로 CSV 내보내기 기능을 계획해줘.
implementation 스킬로 방금 만든 draft를 구현해줘.
spec-sync 스킬로 검증된 변경을 스펙에 반영해줘.
```

`feature-draft`는 `plan-review`와 finding 수정을, `implementation`은 `implementation-review`와 finding 수정을 내부 품질 게이트로 수행한다. 이 흐름에서는 리뷰를 별도 단계로 다시 호출할 필요가 없다.

목표나 범위가 불명확하면 `discussion`부터 시작한다. 여러 기능을 반복 구현할 목표는 `sdd-autopilot`으로 완료 조건·자율 수행 범위·4파일 goal harness를 준비한다. **실행은 사용자가 native goal을 활성화한 뒤 시작한다.** 자세한 절차는 [Autopilot Guide](docs/AUTOPILOT_GUIDE.md)를 따른다.

## Installation

### Claude Code (Plugin)

```
/plugin marketplace add malfo-y/sdd-skills
/plugin install sdd-skills@sdd-skills
```

> **Note**: 플러그인 설치 후 스킬을 활성화하려면 Claude Code를 재시작해야 합니다.

### Codex

#### GitHub 플러그인 설치 (권장)

GitHub 저장소를 Codex marketplace로 등록한 뒤 네이티브 플러그인을 설치한다.

기존 번들·수동 설치에서 옮긴다면 아래 **기존 설치 정리**를 먼저 확인한다.

```bash
codex plugin marketplace add malfo-y/sdd-skills
codex plugin add sdd-skills-codex@sdd-skills-codex
```

설치 상태는 아래 명령으로 확인할 수 있다.

```bash
codex plugin marketplace list
codex plugin list
```

이 플러그인은 skills-only다. 설치만으로 lifecycle 훅이 활성화되지 않으며, 훅은 `spec-create`·`spec-upgrade` 실행 시 대상 저장소에 project-local로 설치한다. 설치 후에는 Codex를 재시작하거나 새 task를 열어 스킬을 로드한다. 하네스 설치 후 Codex의 `/hooks`에서 project hook을 검토·신뢰해야 훅 활성화 검증을 마칠 수 있다.

<details>
<summary>기존 설치 정리 — 번들·수동 설치에서 플러그인으로 전환</summary>

기존 번들 스크립트나 수동 복사 방식으로 설치했다면 먼저 legacy 스킬을 확인하고 제거한다. 기본 실행은 preview-only이며 `--yes`를 붙이면 대상 항목을 `$CODEX_HOME/legacy-sdd-backup-<UTC>`로 옮겨 활성 경로에서 제거한다. 목록에 표시되지 않은 개인 스킬과 Codex 플러그인 캐시는 건드리지 않는다.

```bash
# 삭제 예정 항목 확인
curl -fsSL https://raw.githubusercontent.com/malfo-y/sdd-skills/main/tools/uninstall-codex-skill-bundle.py | python3 -

# 확인한 legacy 스킬 제거
curl -fsSL https://raw.githubusercontent.com/malfo-y/sdd-skills/main/tools/uninstall-codex-skill-bundle.py | python3 - --yes
```

</details>

<details>
<summary>대체 설치 — 번들 스크립트 또는 수동 복사</summary>

#### 번들 설치 스크립트

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
- 기본 설치 경로: `$CODEX_HOME/skills` (`CODEX_HOME` 미설정 시 `~/.codex/skills`)
- 기존 스킬은 내용이 같으면 건너뛰고, 다르면 자동으로 덮어씀
- 사용자 `~/.codex/config.toml`은 수정하지 않음

소스에서 제거된 번들 스킬·agent는 기본 prune 대상이다. 대화형 실행에서는 확인 후 제거하며, 비대화형 실행에서는 `--prune-yes` 없이는 보류한다. `--dry-run`으로 대상만 확인하거나 `--no-prune`으로 정리를 끌 수 있다.

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

#### 수동 설치

`plugins/sdd-skills-codex/skills/`를 `$CODEX_HOME/skills/`에 복사한다. (`$CODEX_HOME` 기본값: `~/.codex`)

</details>

#### Codex discussion 스킬 사용 조건

`discussion` 스킬은 `request_user_input`에 의존하는 interactive skill이다. 현재 세션에 이 도구가 있어야 실행할 수 있다. CLI에서 Default mode의 질문 도구를 켜야 한다면 아래 옵션을 사용한다.

```bash
codex --enable default_mode_request_user_input
```

## Subagent Model Override

리뷰 스킬의 내부 subagent 호출에 모델 override를 줄 수 있다. `implementation-review`·`pr-review`의 `--model`은 **simplicity dispatch에만** 적용된다 — correctness 리뷰는 메인 루프 직접 수행이라 override 대상이 아니다. 옵션을 생략하면 현재 세션/agent 기본값을 그대로 상속한다.

적용 대상:

- `implementation-review` (simplicity dispatch 한정)
- `pr-review` (simplicity dispatch 한정)

Claude Code:

```text
/sdd-skills:implementation-review --model opus
```

Codex:

```text
implementation-review 스킬을 --model gpt-5.6-terra --effort max로 실행해줘.
pr-review 스킬을 --model gpt-5.6-sol --effort ultra로 실행해줘.
```

Codex에서는 model과 effort를 분리해서 쓴다. `gpt-5.6-sol-high` 같은 결합형 값 대신 `--model gpt-5.6-sol --effort high`를 사용한다. 위 값은 호출 예시이며, 실제 허용값은 실행 시 `spawn_agent` 도구가 지원하는 모델·추론 강도를 따른다.

`plan-review`는 subagent 없이 메인 루프가 직접 수행하므로 모델 override 대상이 아니다. `feature-draft`와 `implementation`도 메인 루프가 직접 작성한다.

## Skills

공통 스킬 18개를 목적별로 묶었다. 세부 실행 계약은 각 번들의 `SKILL.md`가 소유한다.

| 목적 | 스킬 |
|------|------|
| 논의·계획 | `discussion`, `feature-draft`, `plan-review` |
| 구현·리뷰·진단 | `implementation`, `implementation-review`, `pr-review`, `investigate` |
| 스펙 생성·유지 | `spec-create`, `spec-sync`, `spec-review`, `spec-rewrite`, `spec-upgrade` |
| 설명·내보내기 | `spec-summary`, `spec-snapshot`, `guide-create` |
| 반복 작업 준비 | `goal-init`, `sdd-autopilot`, `ralph-loop-init` |

Claude Code에는 `git`과 `second-opinion`이 추가된다. 양 번들은 custom agent 없이 스킬로 배포한다. `implementation-review`·`pr-review`는 correctness를 메인 루프에서 검토하고, simplicity를 스킬의 계약을 전달받은 범용 subagent로 검토한다.

## Documentation

개념과 상세 사용법은 아래 문서에서 확인한다.

| 문서 | 내용 | 언제 읽나 |
|------|------|----------|
| [SDD_QUICK_START.md](docs/SDD_QUICK_START.md) | global/temporary spec 구분과 정보 배치 원칙 | 스펙에 무엇을 담을지 정할 때 |
| [SDD_WORKFLOW.md](docs/SDD_WORKFLOW.md) | 전체 워크플로우와 각 문서 레이어가 쓰이는 시점 | 스킬을 더 효과적으로 쓰고 싶을 때 |
| [sdd.md](docs/sdd.md) | SDD 철학과 문제의식 — 왜 스펙 기반 개발인가 | SDD의 배경과 동기가 궁금할 때 |
| [SDD_CONCEPT.md](docs/SDD_CONCEPT.md) | 핵심 컨셉: 하네스 / 글로벌 스펙 / 임시 스펙 / 코드 / 보조 문서의 레이어 구조와 정보 배치 원칙 | 스펙 구조를 이해하고 싶을 때 |
| [SDD_SPEC_DEFINITION.md](docs/SDD_SPEC_DEFINITION.md) | 스펙의 정의 — 단순 문서가 아닌 화이트페이퍼형 기준 문서 | 스펙 작성 기준이 필요할 때 |
| [AUTOPILOT_GUIDE.md](docs/AUTOPILOT_GUIDE.md) | sdd-autopilot SDD goal harness 셋업 가이드 | 큰 목표를 native goal로 활성화해 여러 SDD path로 수렴시키고 싶을 때 |

> 영문 문서: `docs/en/` 디렉토리에 일부 문서의 영문 버전이 있습니다.
