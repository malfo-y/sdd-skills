# Environment Setup Guide

이 저장소는 애플리케이션 런타임보다 스킬 프롬프트와 문서 자산을 관리하는 저장소에 가깝다.

## Runtime

- 기본 작업 대상: Markdown 문서, `SKILL.md`, `skill.json`, 예시/참고 문서
- 주요 디렉토리: `.codex/skills/`, `.claude/skills/`, `_sdd/`, 루트 문서

## Environment Variables

- 로컬 문서 수정만 할 때 필수 환경 변수는 없다.
- PR 관련 스킬을 실제로 검증할 때만 `gh` 인증 상태가 필요할 수 있다.

## Setup Commands

- 저장소 상태 확인: `git status`
- 스킬 파일 탐색: `rg --files .codex/skills`
- 문서 위생 확인: `git diff --check`
- 구조 확인: `find _sdd/spec -maxdepth 2 -type f | sort`
