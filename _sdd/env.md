# Environment Setup Guide

> ⚠️ 이 파일은 커밋된다 — 비밀값(API 키·토큰·비밀번호)을 적지 말 것. 비밀은 환경변수/secret manager로 관리한다.

이 저장소는 애플리케이션 런타임보다 스킬 프롬프트와 문서 자산을 관리하는 저장소에 가깝다.

## Runtime

- 기본 작업 대상: Markdown 문서, `SKILL.md`, 예시/참고 문서
- 주요 디렉토리: `plugins/sdd-skills-codex/skills/`, `.claude/skills/`, `_sdd/`, 루트 문서
- 조건: `tools/tests`는 pytest가 필요하다(기본 python3 3.14에는 없다).

## Environment Variables

- 로컬 문서 수정만 할 때 필수 환경 변수는 없다.
- PR 관련 스킬을 실제로 검증할 때만 `gh` 인증 상태가 필요할 수 있다.

## Setup Commands

- 저장소 상태 확인: `git status`
- 스킬 파일 탐색: `rg --files plugins/sdd-skills-codex/skills`
- 문서 위생 확인: `git diff --check`
- 구조 확인: `find _sdd/spec -maxdepth 2 -type f | sort`
- 플러그인 manifest 검증: `claude plugin validate .`

## Pitfalls

- git 제외 pathspec은 `':(exclude)_…'`로 쓴다. `':!_…'`는 "Unimplemented pathspec magic" 오류다(이 저장소는 `_sdd/`·`_COMMENTS.md`처럼 `_`로 시작하는 경로가 많다).
- 이 저장소 하네스를 `claude -p --plugin-dir`로 시험할 때 marketplace 루트를 그대로 주면 설치된 `sdd-skills`를 덮어쓰지 못한다. plugin.json + skills symlink 래퍼가 필요하다(`_sdd/goal/2026-10-04_orchestrator_harness_redesign/bench/mkplug.sh`, git 추적 파일).
- claude↔codex 미러 비교는 `/usr/bin/diff`의 hunk 수로 판정한다.
- census·0건 판정은 `/usr/bin/grep`으로 한다. 조건: Claude Code 셸에서는 `grep`·`diff`가 래퍼 함수일 수 있다(ugrep은 재귀 검색에서 gitignore 파일을 건너뛴다).
- 조건: macOS 기본 도구.
  - `/bin/bash`는 3.2다.
  - BSD grep의 `--exclude-dir`는 경로 앞에 둔다.
  - BSD awk는 한글 heading 매칭이 깨진다.
  - 한국어 locale에서 `sort | uniq`가 다른 줄을 묶는다.
