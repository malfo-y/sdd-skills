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

## SDD-Autopilot Resources

> sdd-autopilot 메타스킬의 Pre-flight Check에서 참조하는 섹션.
> 프로젝트에서 sdd-autopilot을 사용하려면 아래 항목을 미리 기록해 둔다.
> sdd-autopilot은 이 섹션과 파이프라인 요구사항을 대조하여 갭을 분석한다.

### 외부 서비스
<!-- 예시:
- DB: PostgreSQL (localhost:5432, test DB: myproject_test)
- Redis: localhost:6379
- S3: localstack (localhost:4566)
-->
- 없음 (이 저장소는 외부 서비스를 사용하지 않음)

### 환경 변수
<!-- 예시:
- OPENAI_API_KEY: .env 파일에 설정됨
- DATABASE_URL: .env 파일에 설정됨
-->
- `gh` 인증: PR 관련 스킬 검증 시에만 필요

### 테스트
<!-- 예시:
- 프레임워크: pytest
- 실행 명령: pytest tests/ -v
- 커버리지: pytest --cov=src tests/
-->
- 이 저장소는 전통적 테스트 프레임워크를 사용하지 않음
- 스킬 검증: 슬래시 커맨드로 실제 호출하여 확인

### 빌드/배포
<!-- 예시:
- 빌드: npm run build
- 린트: eslint src/
- 타입체크: tsc --noEmit
-->
- 빌드 과정 없음 (마크다운 기반)
