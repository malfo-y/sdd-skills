# SDD Skills

## Goal

### Project Snapshot

- 이 저장소는 Spec-Driven Development(SDD) 워크플로우를 Codex와 Claude 환경에서 재사용 가능한 스킬 묶음으로 제공한다.
- 핵심 목적은 사람이든 LLM이든 탐색형 스펙을 기준으로 기능 초안, 구현 계획, 구현, 리뷰, 스펙 동기화를 일관되게 수행하도록 돕는 것이다.
- 코드 생성 도구 자체를 만드는 저장소라기보다, 스킬 프롬프트와 레퍼런스 문서를 통해 개발 절차를 표준화하는 저장소다.

### Key Features

1. 탐색형 스펙 생성/재작성/요약/리뷰/동기화 스킬 제공
2. 기능 초안부터 구현 계획, 구현, 구현 리뷰까지 이어지는 실행 스킬 제공
3. PR 기반 스펙 패치와 PR 리뷰 스킬 제공
4. Codex용 `.codex/skills/`와 Claude용 `.claude/skills/`를 함께 유지하는 다중 플랫폼 스킬 저장소 제공
5. SDD 개념, 워크플로우, 요구사항 문서를 함께 관리

### Non-Goals

- 사용자 프로젝트의 실제 애플리케이션 코드를 빌드하거나 실행하는 런타임을 제공하지 않는다.
- 모든 스킬 실행을 자동화하는 중앙 오케스트레이터를 제공하지 않는다.
- 현재 기준으로 `.codex/skills/`와 `.claude/skills/`의 완전 자동 동기화는 보장하지 않는다.

## Architecture Overview

### System Boundary

이 저장소가 책임지는 것:
- SDD 워크플로우를 위한 스킬 정의, 예시, 참조 문서
- SDD 철학과 문서 구조를 설명하는 루트 문서
- 내부적으로 사용한 구현 계획/리뷰/토론 메모

이 저장소가 책임지지 않는 것:
- 각 사용자 프로젝트의 실제 소스 코드와 런타임
- Codex/Claude 자체의 모델 실행 환경
- GitHub PR 데이터 자체의 저장과 제공

외부 시스템/도구:
- Codex와 Claude Code 런타임
- GitHub / `gh` CLI (PR 관련 스킬 검증 시)
- 사용자가 이 스킬을 설치해 사용할 대상 프로젝트 저장소

### Repository Map

| 경로 | 역할 | 메모 |
|------|------|------|
| `.codex/skills/` | Codex용 스킬 정의 | 현재 13개 Codex 스킬 보유 |
| `.claude/skills/` | Claude/Claude Code용 스킬 정의 | `discussion` 포함, 일부 문구/버전은 Codex와 드리프트 가능 |
| `_sdd/spec/` | 이 저장소 자체의 탐색형 스펙 | 메인 스펙과 그룹 스펙 위치 |
| `_sdd/implementation/` | 이 저장소를 정리할 때 사용한 계획/리뷰 문서 | 스킬 정렬 기록 포함 |
| `_sdd/discussion/` | 개념 토론 메모 | spec 철학과 구조 논의 |
| `README.md` | 설치/개요 진입점 | 플랫폼별 설치 안내 포함 |
| `docs/SDD_WORKFLOW.md` | SDD 전체 워크플로우 설명 | 스킬 관계와 규모별 경로 정리 |
| `docs/SDD_CONCEPT.md` | 두 단계 스펙 구조 개념 설명 | 글로벌/임시 스펙 개념 |
| `docs/SDD_SPEC_REQUIREMENTS.md` | 현재 스펙 문서 요구사항 기준 | 탐색형 스펙의 canonical 요구사항 |
| `docs/sdd.md` | SDD 배경과 철학 설명 | AI 에이전트 시대의 문제 정의 |

### Runtime Map

#### Consumer Workflow

1. 사용자는 `.codex/skills/` 또는 `.claude/skills/`를 설치한다.
2. `spec-create` 또는 기존 스펙을 기준으로 프로젝트의 entry-point spec을 만든다.
3. `feature-draft` 또는 `implementation-plan`으로 구현 단위를 정리한다.
4. `implementation`과 `implementation-review`로 코드 작업을 진행한다.
5. `pr-spec-patch`, `pr-review`, `spec-update-done`으로 문서와 구현을 다시 맞춘다.

#### Repository Maintenance Flow

1. 철학/요구사항 변경은 주로 `docs/SDD_SPEC_REQUIREMENTS.md`, `docs/SDD_WORKFLOW.md`, `docs/SDD_CONCEPT.md`에서 먼저 정의된다.
2. 변경 영향이 있는 스킬 그룹을 찾아 `.codex/skills/<skill>/`와 `.claude/skills/<skill>/`의 대응 파일을 함께 점검한다.
3. 한 플랫폼에만 존재하는 스킬은 해당 플랫폼 경로만 수정하되, `README.md`와 `docs/SDD_WORKFLOW.md`의 인벤토리 설명도 같이 확인한다.
4. 변경 후 `git diff --check`, `rg`, `git status`로 구조적 드리프트를 확인한다.

> 이 저장소는 서비스 요청을 처리하는 애플리케이션이 아니라, “문서화된 워크플로우 자산”을 유지하는 저장소다. 따라서 Runtime Map은 코드 실행 흐름보다 스킬 사용/유지보수 흐름에 가깝다.

## Component Details

### Component Index

| 컴포넌트 | 책임 | 주요 경로 | 관련 스펙 |
|---------|------|----------|----------|
| Spec Lifecycle Skills | 스펙 생성, 재작성, 요약, 리뷰, 계획 반영, 구현 반영 | `.codex/skills/spec-*/`, `.claude/skills/spec-*/` | [`spec-lifecycle.md`](spec-lifecycle.md) |
| Delivery Lifecycle Skills | 기능 초안, 구현 계획, 구현, 구현 리뷰 | `.codex/skills/feature-draft/`, `.claude/skills/feature-draft/`, `.codex/skills/implementation*/`, `.claude/skills/implementation*/` | [`implementation-lifecycle.md`](implementation-lifecycle.md) |
| PR Lifecycle Skills | PR 변화의 스펙 패치 초안화와 구현 검증 | `.codex/skills/pr-*/`, `.claude/skills/pr-*/`, `_sdd/pr/` | [`pr-lifecycle.md`](pr-lifecycle.md) |
| Misc Skills | `discussion`, `ralph-loop-init` 같은 비핵심 보조 스킬 관리 | `.claude/skills/discussion/`, `.codex/skills/ralph-loop-init/`, `.claude/skills/ralph-loop-init/` | [`misc-skills.md`](misc-skills.md) |
| Platform Distribution | Codex/Claude 배포 구조와 설치 문서 유지 | `.codex/skills/`, `.claude/skills/`, `README.md` | 이 문서 내 상세 메모 |

### Main-only Components

#### Platform Distribution

- `.codex/skills/`와 `.claude/skills/`는 모두 사용자에게 노출되는 실제 배포 타깃이다.
- 대부분의 핵심 SDD 스킬은 두 트리에 모두 존재하지만, `discussion`처럼 Claude 전용 스킬도 있다.
- 현재는 두 트리의 정렬이 수동이어서, 같은 이름의 스킬이라도 버전/문구/예시가 완전히 같지 않을 수 있다.
- `README.md`와 `docs/SDD_WORKFLOW.md`는 사용자에게 보이는 설치/워크플로우 진입점이므로, 스킬 구성 변경 시 함께 점검해야 한다.

## Environment & Dependencies

### Local Authoring Environment

- 이 저장소는 문서와 프롬프트 자산 위주라서 별도 앱 런타임은 없다.
- 자주 쓰는 도구는 `git`, `rg`, `find`, `sed`, `jq`다.
- PR 관련 스킬을 실제로 검증할 때만 `gh auth status` 같은 외부 CLI 상태가 중요하다.

### Common Validation Commands

- 구조 확인: `find .codex/skills .claude/skills -maxdepth 2 \\( -name "SKILL.md" -o -name "skill.json" \\) | sort`
- 위생 확인: `git diff --check`
- 문구 정렬 확인: `rg "MUST update|NO update|CONSIDER|Open Questions" .codex/skills .claude/skills`

## Identified Issues & Improvements

- `.claude/skills/`와 `.codex/skills/`의 정렬은 아직 수동 작업이다.
- 플랫폼별 스킬 인벤토리가 다르다. 현재 `discussion`은 `.claude/skills/`에만 있고, `ralph-loop-init`은 양쪽에 있다.
- 루트 문서와 실제 스킬 디렉터리 구조 사이의 일관성을 자동 검증하는 스크립트는 아직 없다.
- 버전 업데이트와 예시/참조 문서 정렬도 여전히 수동이다.

## Usage Examples

### Common Change Paths

#### 스펙 철학을 바꿀 때

- 먼저 볼 곳: `docs/SDD_SPEC_REQUIREMENTS.md`
- 같이 확인할 곳: `.codex/skills/spec-*/`, `.claude/skills/spec-*/`, `feature-draft`, `implementation*`, `pr*` 대응 스킬
- 검증 포인트: 양쪽 플랫폼 스킬의 예시와 참조 템플릿까지 같이 바뀌었는지, 소비자 스킬이 같은 앵커를 읽는지

#### 특정 스킬을 바꿀 때

- 먼저 볼 곳: 존재하는 플랫폼의 `<platform>/skills/<skill>/SKILL.md`
- 같이 확인할 곳: 같은 이름의 반대 플랫폼 스킬, 같은 디렉터리의 `references/`, `examples/`, `skill.json`
- 검증 포인트: 출력 포맷, 관련 상위 워크플로우 문서, 플랫폼 간 드리프트 여부, 인접 스킬과의 계약

#### 배포 구조와 설치 안내를 바꿀 때

- 먼저 볼 곳: `README.md`
- 같이 확인할 곳: `docs/SDD_WORKFLOW.md`, `.codex/skills/`, `.claude/skills/`
- 검증 포인트: 실제 존재하는 스킬 목록과 문서상의 목록이 일치하는지

## Open Questions

1. `.codex/skills/`와 `.claude/skills/` 중 어느 쪽을 canonical authoring surface로 명시할지 아직 확정되지 않았다.
2. `discussion` 스킬을 Codex 쪽에도 둘지, Claude 전용으로 유지할지 기준이 문서에 충분히 고정되어 있지 않다.
3. 루트 문서와 실제 스킬 인벤토리의 정합성을 자동 점검하는 스크립트가 필요한지 결정이 필요하다.
