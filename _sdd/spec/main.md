# SDD Skills

> Markdown 기반 스킬 시스템으로 AI 에이전트의 Spec-Driven Development 워크플로우를 구조화한다.

**Version**: 3.9.1
**Last Updated**: 2026-04-03
**Status**: Approved

## Table of Contents

- [Background & Motivation](#background--motivation)
- [Core Design](#core-design)
- [Architecture Overview](#architecture-overview)
- [Component Details](#component-details) — 요약 + [상세](./components.md)
- [Usage Guide & Expected Results](./usage-guide.md)
- [Environment & Dependencies](#environment--dependencies)
- [Identified Issues & Improvements](#identified-issues--improvements)
- [Changelog](./logs/changelog.md)

---

## Background & Motivation

### Problem Statement

AI 코딩 에이전트(Claude Code, Codex)는 강력한 코드 생성 능력을 가지고 있지만, 프로젝트의 요구사항과 설계가 체계적으로 문서화되지 않으면 맥락을 잃고 일관성 없는 결과를 생산한다. 기존 소프트웨어 개발 방법론(Agile, Waterfall)은 인간 개발자를 전제로 설계되었으며, AI 에이전트가 스펙을 읽고 → 구현하고 → 검증하는 루프에 최적화되어 있지 않다.

### Why This Approach

| 접근 | 장점 | 단점 | 판정 |
|------|------|------|------|
| SDD 스킬 기반 | 스펙 = Single Source of Truth, AI가 직접 참조/업데이트 가능, `/스킬명` 한 줄로 실행 | 스킬 설계/유지 비용 | **채택** |
| 프롬프트 라이브러리 | 간단, 빠른 시작 | 스킬 간 연결/데이터 흐름 없음, 맥락 유실 | 거부: 확장성 부족 |
| 코드 기반 자동화 (CI/CD) | 검증된 인프라 | AI 에이전트의 유연성과 맞지 않음, 자연어 지시 불가 | 거부: AI 워크플로우에 부적합 |

### Core Value Proposition

마크다운 기반 스킬 시스템으로 소프트웨어 개발 생명주기 전체를 구조화한다. 각 스킬은 독립적이면서도 `_sdd/` 아티팩트를 통해 유기적으로 연결되며, 사용자는 `/스킬명` 한 줄로 복잡한 개발 워크플로우(스펙 작성 → 구현 → 검증 → 리뷰)를 AI 에이전트에게 위임할 수 있다.

### Primary Objective

Claude Code와 Codex에서 **Spec-Driven Development(SDD) 워크플로우**를 실행하기 위한 스킬 모음을 제공한다. 스펙 문서를 Single Source of Truth로 삼아 요구사항 정의 → 구현 → 검증 → 유지보수 전 과정을 AI 에이전트가 체계적으로 수행할 수 있도록 한다.

### Key Features

- **21개 스킬 + 18개 에이전트**: 스킬은 사용자 인터페이스(`/스킬명`), 에이전트는 플랫폼별로 spawn 가능한 자동화 파이프라인 실행 단위 (Claude 9 + Codex 9). 모든 agent와 full skill은 **AC-First 구조**(Acceptance Criteria + 자체 검증 + Final Check)로 통일
- **sdd-autopilot 메타스킬**: reasoning 기반 적응형 파이프라인을 자동 생성하고 end-to-end 자율 실행
- **듀얼 플랫폼**: Claude Code (`.claude/skills/`) + Codex (`.codex/skills/`) 동시 지원
- **Plugin 배포**: Claude Code Plugin Marketplace를 통한 원클릭 설치
- **규모별 워크플로우**: 대규모(6단계) / 중규모(3단계) / 소규모(1단계) 분리, sdd-autopilot이 reasoning 기반으로 자동 판단 및 실행 가능

### Target Users / Use Cases

| 사용자 유형 | 사용 사례 | 우선순위 |
|------------|----------|----------|
| AI 에이전트 활용 개발자 | Claude Code/Codex로 소프트웨어 개발 | High |
| 팀 리더 | 스펙 기반 체계적 AI 코딩 워크플로우 구축 | Medium |

### Success Criteria

- 모든 21개 스킬이 Claude Code에서 `/스킬명`으로 정상 호출 및 실행
- 9개 래퍼 스킬이 대응하는 에이전트에 올바르게 위임
- Claude 9개 에이전트와 Codex 9개 custom agent가 각 플랫폼 실행 모델에 맞게 정상 동작 (모두 AC-First + Self-Contained 구조)
- sdd-autopilot이 reasoning 기반 파이프라인을 생성하고 end-to-end 자율 실행 완료 (재개/부분 실행 지원)
- Codex에서 19개 스킬(discussion 포함, git/second-opinion 제외)이 정상 동작
- Codex에서 9개 custom agent가 wrapper skill 및 generated orchestrator를 통해 정상 호출됨
- 스킬 간 워크플로우 연결이 끊김 없이 동작 (e.g., spec-create → feature-draft → implementation)

---

## Core Design

### Key Idea

SDD Skills의 중심 설계 원리는 **"SKILL.md = 실행 가능한 프롬프트"**이다. Claude Code는 v3.0부터 **스킬 + 에이전트 이중 아키텍처(dual architecture)**를 채택하여, 파이프라인 필수 스킬 8개는 에이전트 정의(`.claude/agents/*.md`)로 전체 로직을 분리하고, 기존 스킬은 에이전트에 위임하는 래퍼(wrapper)로 전환하였다. v3.1에서 8개 에이전트의 `AskUserQuestion`을 모두 제거하고 **Autonomous Decision-Making 패턴**으로 대체하여, sdd-autopilot 파이프라인 내에서 완전 non-interactive 실행이 가능해졌다. v3.6에서 모든 agent와 full skill을 **AC-First + Self-Contained** 구조로 전면 재작성하여, 각 agent는 외부 reference 없이 단독 실행 가능하며, AC 섹션 + 자체 검증 지시 + Final Check로 품질을 보장한다. Codex도 동일한 역할 분리와 AC-First 구조를 채택하되, 실행 레이어는 `.codex/agents/*.toml` custom agents로 구현한다. Wrapper skill은 사용자 진입점으로 유지되고, generated orchestration skill은 custom agents만 직접 spawn한다. 이를 통해:

1. **사용자는 기존처럼 `/스킬명`으로 개별 호출** 가능 (래퍼 스킬)
2. **sdd-autopilot이나 generated orchestration skill이 실행 단위를 재사용** 가능 (Claude는 `.claude/agents/*.md`, Codex는 `.codex/agents/*.toml`)
3. **플랫폼별 실행 레이어 차이를 유지하면서도 `_sdd/` handoff 계약을 공유** (단일 책임)

스킬 간 데이터 흐름은 코드가 아닌 `_sdd/` 디렉토리의 마크다운 아티팩트(스펙, 드래프트, 구현 계획, 리뷰 리포트)를 통해 연결된다.

```
# 실행 흐름 A: 사용자 직접 호출 (래퍼 경유)
[사용자: /feature-draft]
    → 래퍼 SKILL.md 로드
    → Claude: Agent(subagent_type="feature-draft", prompt="...")
    → Codex: wrapper skill이 custom agent `feature_draft` 실행 contract로 위임
    → 실행 단위가 Step 1~7 실행
    → 출력: _sdd/drafts/feature_draft_<name>.md

# 실행 흐름 B: sdd-autopilot 자동 호출 (플랫폼별 에이전트 직접 재사용)
[sdd-autopilot Phase 2]
    → Claude: Agent(subagent_type="feature-draft", prompt="...")
    → Codex: generated orchestration skill이 custom agent `feature_draft` spawn
    → 실행 단위가 Step 1~7 실행
    → 출력: _sdd/drafts/feature_draft_<name>.md

# 실행 흐름 C: 래퍼 없는 스킬 (직접 실행)
[사용자: /spec-create]
    → SKILL.md 로드
    → Step 1~3 순차 실행
    → 출력: _sdd/spec/<project>.md
```

### SKILL.md / Agent 정의 공통 구조

**풀 스킬** (에이전트 전환되지 않은 스킬)은 **AC-First 구조**를 따른다 [`.claude/skills/*/SKILL.md`]:

```markdown
---
name: <skill-name>
description: <trigger description>
version: <semver>
---

# <Skill Title>

## Acceptance Criteria     # AC + 자체 검증 지시 (blockquote)
## Hard Rules              # 절대 위반 불가 규칙
## Process (Step 1~N)      # 단계별 실행 프로세스
  - Decision Gates         # 단계 간 전환 조건
## Output Format           # 출력 형식 정의
## Error Handling           # 예외 처리
## Final Check             # AC 만족 검증
```

**에이전트 정의** (`.claude/agents/<name>.md`): **AC-First + Self-Contained** 구조. 외부 reference 없이 단독 실행 가능하며, 핵심 reference 내용을 인라인으로 포함한다:

```markdown
---
name: <agent-name>
description: "<when to use this agent>"
tools: ["Read", "Write", "Edit", "Glob", "Grep", ...]
model: inherit
---

# <Agent Title>
[1-2문장 Goal]

## Acceptance Criteria     # AC + 자체 검증 지시 (blockquote)
## Hard Rules
## Process (Step 1~N)      # 핵심 reference 내용 인라인 포함
## Output Format
## Final Check             # AC 만족 검증
```

**래퍼 스킬** (`.claude/skills/<name>/SKILL.md`, `.codex/skills/<name>/SKILL.md`): 에이전트로 전환된 스킬의 래퍼:

```markdown
---
name: <skill-name>
description: "<기존 트리거 설명 유지>"
version: <minor 버전 업>
---

# <Skill Title> (Wrapper)
이 스킬은 `<agent-name>` 실행 단위에 작업을 위임합니다.

## Hard Rules
1. 직접 파일 작성 금지
2. 원문 전달
3. 결과 보고

## Execution
- Claude: `Agent(subagent_type="<agent-name>", prompt="[사용자의 원래 요청 전문]")`
- Codex: 대응 custom agent(`<agent_name>`)에 동일한 요청과 artifact contract를 전달
```

### Design Patterns

**Decision Gate 패턴**: 각 Step 사이에 조건을 두어 잘못된 상태에서 다음 단계 진행을 방지한다. 무조건 순차 실행 방식은 에러 전파 위험이 있어 거부되었다.

**Progressive Disclosure 패턴**: 모든 스킬에서 최종 출력 시 공통 적용한다.
1. 요약 테이블 먼저 제시 (사용자 확인을 기다리지 않음)
2. 전체 상세 내용 출력
3. 파일 저장

**Target Files 패턴**: `feature-draft` [`.claude/skills/feature-draft/SKILL.md`], `implementation-plan`, `implementation`에서 사용하는 병렬 실행 지원 메커니즘:

```markdown
**Target Files**:
- [C] `src/new_file.py` -- 새 파일 생성
- [M] `src/existing.py` -- 기존 파일 수정
- [D] `src/deprecated.py` -- 파일 삭제
```

- `[C]` Create, `[M]` Modify, `[D]` Delete
- 동일 파일에 `[M]` 마커가 있는 태스크 쌍 → Sequential (conflict)
- 겹치지 않는 태스크 → Parallel 실행 가능

**Producer-Owned Inline 2-Phase Writing 패턴**: `write-phased` [`.claude/skills/write-phased/SKILL.md`], `spec-create`, `spec-rewrite`, `spec-upgrade`, `guide-create`, `spec-summary`, `pr-review`에서 사용. helper agent에 skeleton 생성을 위임하지 않고, caller가 현재 콘텍스트에서 먼저 골조(skeleton) → 내용 채우기(fill) → finalize를 같은 흐름에서 수행한다. 이를 통해 handoff contract와 context re-packaging 비용을 줄이고 후반부 품질 저하를 방지한다.

**Agent Wrapper 패턴**: 스킬을 에이전트로 전환할 때 적용한다. Claude에서는 전체 로직을 `.claude/agents/<name>.md` 에이전트 정의로 이동하고, 기존 `.claude/skills/<name>/SKILL.md`는 에이전트에 위임하는 최소한의 래퍼로 전환한다. Codex에서는 같은 역할 분리를 `.codex/agents/<name>.toml` custom agent와 `.codex/skills/<name>/SKILL.md` wrapper로 구현한다. 이를 통해 사용자의 `/스킬명` 호출 인터페이스를 유지하면서 플랫폼별 실행 단위를 재사용할 수 있다. v3.0 이후 핵심 파이프라인 스킬에 확대 적용하였고, 현재 래퍼 스킬은 **Mirror 패턴**(아래)으로 구현되어 있다.

**Mirror 패턴**: Agent Wrapper 패턴의 구현 방식. 래퍼 스킬의 SKILL.md에 에이전트 본문을 전체 복사하고, 파일 하단에 Mirror Notice(`> **Mirror Notice**: 이 스킬의 본문은 <에이전트 파일>의 복사본이다.`)를 추가한다. 사용자가 `/스킬명`으로 직접 호출할 때 중간 과정의 가시성을 확보하기 위한 설계이다. 수정 시 에이전트 파일과 SKILL.md를 **반드시 함께** 수정해야 한다. thin wrapper(Agent() 호출만 포함)에 비해 파일 중복이 발생하지만, 사용자 직접 호출 시 전체 프로세스가 컨텍스트에 로드되어 실행 품질이 높아지는 이점이 있다.

**Autonomous Decision-Making 패턴**: 에이전트가 서브에이전트로 호출될 때 적용한다. AskUserQuestion 대신 가용 정보에서 최선의 추론을 수행하고, 판단 근거를 출력에 기록하며, 추론 불가 항목은 Open Questions에 남긴다. 이를 통해 에이전트가 사용자 인터랙션 없이 non-interactive하게 파이프라인 내에서 실행될 수 있다. v3.1에서 8개 파이프라인 에이전트 전체에 적용하였다.

**AC-First 패턴**: 모든 agent와 full skill에 적용한다 (v3.6). 파일 상단에 Acceptance Criteria를 정의하고, 자체 검증 지시(blockquote)를 포함하며, 파일 마지막에 Final Check 섹션으로 AC 만족 여부를 재확인한다. 이를 통해 실행 결과의 품질을 agent/skill 내부에서 자체 보장한다. 기존 Best Practices, Context Management, When to Use 등 공통 bloat 섹션은 제거하고 AC와 Hard Rules로 통합하였다.

**Self-Contained 패턴**: 모든 에이전트 정의에 적용한다 (v3.6). 에이전트가 서브에이전트로 실행될 때 skill 디렉토리의 `references/`에 접근 불가능한 문제를 해결하기 위해, 핵심 reference 내용을 에이전트 파일에 인라인으로 포함한다. 원본 reference 대비 70%+ 압축 (테이블/체크리스트 위주)하여 컨텍스트 효율을 유지한다. 래퍼 스킬의 `references/`, `examples/` 디렉토리는 삭제하였다.

**2-Phase Orchestration 패턴**: `sdd-autopilot` 메타스킬에서 사용한다. 사용자 인터랙션을 전반부에 집중하고, 후반부는 완전 자율 실행한다. v2.0.0에서 규모별 템플릿 매칭을 reasoning 기반 동적 파이프라인 구성으로 전면 교체하였다.
- Step 0 (Pipeline State Detection): 기존 미완료 파이프라인 로그를 스캔하여 재개/새로 시작 선택을 사용자에게 제시
- Phase 1 (Interactive): Reference Loading(SDD 철학 + 스킬 카탈로그) → 사용자와 인라인 discussion → 코드베이스 탐색 → Reasoning 기반 오케스트레이터 생성 → Orchestrator Verification(구조 + 철학 검증). 시작점/종료점 감지를 통해 기존 산출물을 활용하거나 파이프라인 범위를 조절
- Phase 1.5 (Checkpoint): 검증된 오케스트레이터 + Pre-flight Check 결과를 사용자에게 제시 → 확인/수정 → 실행 승인
- Phase 2 (Autonomous): 승인된 오케스트레이터가 에이전트 파이프라인을 자율 실행 → 마일스톤 텍스트 출력 + `_sdd/pipeline/` 로그 기록 (Meta + Status 테이블 포함)
- 종료 조건: review-fix 루프 최대 3회, critical/high/medium = 0이면 종료하며 low는 로그/후속 권고로 남길 수 있다. 에러 시 3회 재시도. **Hard Rule #9**: review가 포함된 파이프라인에서는 review → fix → re-review 사이클이 필수이며, 리뷰만 하고 끝나는 것은 허용하지 않는다. 부분 파이프라인/재개에서도 동일 적용. `implementation-review`는 review 포함 시 조건부 핵심 단계로 취급된다. **Hard Rule #10**: 모든 파이프라인 단계는 Execute + Verify 두 페이즈를 반드시 거쳐야 한다.
- 재개: Status 테이블에서 첫 번째 미완료 스텝을 찾아 해당 스텝부터 실행 재개

### Common Hard Rules

1. **스펙 직접 수정 금지** (spec-update-todo, spec-update-done 제외): 대부분의 스킬은 스펙을 읽기 전용으로 참조
2. **_sdd/env.md 참조 필수**: 로컬 명령 실행 전 환경 설정 확인
3. **기존 파일 백업**: 덮어쓰기 전 `prev/prev_<filename>_<timestamp>.md`로 아카이브
4. **한국어 기본**: 사용자와의 커뮤니케이션은 한국어 (스킬 내부 정의는 영어)

**sdd-autopilot 전용 Hard Rules** (위 공통 규칙에 추가):

5. **Review-Fix 사이클 필수** (Hard Rule #9): 파이프라인에 review 단계(implementation-review 또는 모든 형태의 코드 리뷰)가 포함되면, 반드시 review → fix → re-review 사이클을 실행해야 한다. 리뷰만 하고 끝나는 것은 허용하지 않는다. 이 규칙은 전체 파이프라인, 부분 파이프라인, 중간부터 시작하는 파이프라인, 재개(resume) 모두에 적용된다. review가 포함된 파이프라인에서 `implementation-review`는 조건부 핵심 단계로 취급하며, 실패 시 건너뛸 수 없다.

6. **Execute -> Verify 필수** (Hard Rule #10): 모든 파이프라인 단계는 반드시 (1) 실행(Execute)과 (2) 검증(Verify) 두 페이즈를 거쳐야 한다. 에이전트를 호출한 것만으로 완료로 간주하지 않는다. 검증 페이즈에서 Exit Criteria를 만족하는지 확인하고, 만족하지 않으면 다음 단계로 넘어가지 않는다. 이 규칙은 생성 에이전트(ralph-loop-init 등)에도 동일하게 적용된다.

### Design Rationale

| 설계 결정 | 근거 | 대안 |
|-----------|------|------|
| 마크다운 기반 스킬 정의 | 코드 배포 없이 텍스트 편집만으로 스킬 수정 가능. AI 에이전트가 자연어를 직접 해석 | 코드 기반 플러그인 (거부: 수정 시 빌드/배포 필요) |
| `_sdd/` 아티팩트를 통한 스킬 간 연결 | 파일 기반이므로 플랫폼 독립적. git으로 버전 관리 가능 | API/메모리 기반 (거부: 플랫폼 종속, 세션 간 유실) |
| Decision Gate 패턴 | 각 Step 사이에 조건을 두어 잘못된 상태에서 다음 단계 진행 방지 | 무조건 순차 실행 (거부: 에러 전파 위험) |
| Progressive Disclosure | 요약 먼저 → 상세 나중. 사용자가 대량 출력에 압도되지 않음 | 전체 출력 한번에 (거부: 가독성 저하) |
| Agent Wrapper 패턴 | 스킬 인터페이스 유지 + 플랫폼별 실행 단위 재사용 가능 | 스킬 완전 제거 (거부: 사용자 `/스킬명` 호출 불가) |
| 2-Phase Orchestration | Phase 1에서 충분히 논의 후 Phase 2는 중단 없이 자율 실행. 파이프라인 효율 극대화. Step 0에서 재개 지원. v2.0.0에서 reasoning 기반 동적 파이프라인 구성으로 전환 | 매 단계 사용자 확인 (거부: 중간 중단이 효율 저하), 규모별 템플릿 매칭 (거부: 유연성 부족) |
| 스킬 + 에이전트 이중 아키텍처 | 사용자 직접 호출과 자동화 파이프라인 호출을 동시 지원 | 에이전트 전용 (거부: 기존 사용자 워크플로우 깨짐) |
| Autonomous Decision-Making | 에이전트가 non-interactive로 파이프라인 실행 가능. 판단 근거를 출력에 기록하여 추적성 확보 | AskUserQuestion 유지 (거부: 서브에이전트 호출 시 사용자 인터랙션 불가) |
| AC-First 구조 | 각 agent/skill이 자체 품질 검증 가능. AC 기반으로 실행 결과가 명확히 측정됨. 공통 bloat(Best Practices, Context Management 등) 제거로 55% 이상 줄수 감축 | 기존 verbose 구조 유지 (거부: 핵심 로직이 bloat에 묻힘, 컨텍스트 비효율) |
| Self-Contained 에이전트 | 서브에이전트 실행 시 외부 reference 접근 불가 문제 해결. Plugin 환경에서도 정상 동작 | reference 파일 유지 + 경로 전달 (거부: subagent/plugin 환경에서 접근 불가) |

---

## Architecture Overview

### System Diagram

```
사용자 ──→ Claude Code / Codex
              │
              ├── Skill Loader
              │     ├── .claude/skills/  (Claude Code 스킬 21개)
              │     │     ├── 풀 스킬 (11개) ─── SKILL.md에 AC-First 구조 전체 로직 포함
              │     │     ├── 래퍼 스킬 (9개) ─── Agent()로 에이전트에 위임
              │     │     └── 메타스킬 (1개) ─── sdd-autopilot (오케스트레이터 생성)
              │     └── .codex/skills/   (Codex 스킬 19개)
              │           ├── 래퍼/직접 스킬 (18개) ─── user entry + workflow contract
              │           ├── 유틸리티 스킬 (1개) ─── write-phased
              │           └── 메타스킬 (1개) ─── sdd-autopilot (오케스트레이터 생성)
              │
              ├── Agent Layer
              │     ├── Claude: .claude/agents/ (9개)
              │     └── 파이프라인/리뷰 에이전트 ─── 래퍼 스킬에서 위임받아 실행
              │
              ├── Codex Agent Layer
              │     ├── .codex/agents/  (Codex custom agent 9개)
              │     └── 파이프라인/리뷰 에이전트 ─── wrapper skill과 orchestrator가 직접 spawn
              │
              └── SDD Workflow Engine
                    ├── 스펙 관리 (Create / Review / Rewrite / Summary / Update / Upgrade)
                    ├── 구현 (Draft / Plan / Implement / Review)
                    ├── PR (Patch / Review)
                    ├── 보조 (Discussion / Ralph Loop / Guide)
                    ├── 유틸리티 (Git / SDD Upgrade / Spec Snapshot / Write-Phased)
                    └── 메타 (SDD-Autopilot)
```

### Skill & Agent Loading Structure

각 스킬은 독립적인 디렉토리로 구성되며, 플랫폼(Claude Code / Codex)이 `SKILL.md`를 컨텍스트에 로드하여 실행한다 [`.claude/skills/*/`]:

```
# 풀 스킬 (에이전트 전환 안 됨)
<skill-name>/
├── SKILL.md          # 메인 프롬프트 (전체 로직 포함)
├── skill.json        # 메타데이터 (이름, 설명, 버전)
├── references/       # 보조 참조 문서
│   └── *.md
└── examples/         # 실행 예시
    └── *.md

# 래퍼 스킬 (에이전트로 전환됨)
<skill-name>/
├── SKILL.md          # 래퍼 (Agent() 호출만)
└── skill.json        # 메타데이터 (기존 유지)
# references/, examples/ 삭제됨 (v3.6) — 에이전트가 self-contained

# 에이전트 정의 (.claude/agents/)
<agent-name>.md       # frontmatter + 전체 스킬 로직

# Codex custom agent 정의 (.codex/agents/)
<agent-name>.toml     # name + description + developer_instructions
```

### Data Flow

```
[사용자 요청]
    │
    ▼
[Skill Dispatch] ─── skill.json의 description으로 매칭
    │
    ├── [풀 스킬] ─── SKILL.md 직접 실행
    │     ├── references/*.md 참조 (필요 시)
    │     └── examples/*.md 참조 (포맷 가이드)
    │
    ├── [래퍼 스킬] ─── 플랫폼별 실행 단위에 위임
    │     ├── Claude: Agent()로 .claude/agents/<name>.md 실행
    │     │     └── 필요 시 inline writing contract 또는 bounded helper 사용 가능
    │     │     # agent는 self-contained: 핵심 reference 인라인 포함
    │     └── Codex: 대응 .codex/agents/<name>.toml custom agent 실행
    │           └── generated orchestrator는 skill이 아니라 custom agent 이름을 사용
    │
    └── [sdd-autopilot] ─── 오케스트레이터 생성 후 플랫폼별 에이전트 파이프라인 실행
          ├── Step 0: 기존 파이프라인 상태 감지 (재개/새로 시작)
          ├── Phase 1: 사용자 인터랙션 (인라인) + 산출물 스캔
          ├── Phase 1.5: 오케스트레이터 확인 + pre-flight
          └── Phase 2: Claude/Codex 에이전트 자율 파이프라인 실행
    │
    ▼
[_sdd/ 아티팩트 생성/수정]
    ├── _sdd/spec/           (스펙 문서)
    ├── _sdd/drafts/         (피처 드래프트)
    ├── _sdd/implementation/  (구현 계획/리포트)
    ├── _sdd/pr/             (PR 리뷰/패치)
    └── _sdd/pipeline/       (파이프라인 실행 로그 + 완료 오케스트레이터 아카이브)
    │
    ▼
[.claude/skills/orchestrator_<topic>/ or .codex/skills/orchestrator_<topic>/]  (활성 오케스트레이터)
```

### Workflow

#### 규모별 워크플로우

**수동 호출** (개별 `/스킬명` 사용):

```
┌─────────────────────────────────────────────────────┐
│ 대규모 (Large) - 6단계                               │
│ discussion? → spec-create → feature-draft            │
│   → spec-update-todo → implementation-plan           │
│   → implementation → implementation-review           │
│   → spec-update-done                                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 중규모 (Medium) - 3단계                              │
│ spec-create → feature-draft → implementation         │
│   → spec-update-done                                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 소규모 (Small) - 1단계                               │
│ feature-draft (spec patch + plan 한 번에)            │
└─────────────────────────────────────────────────────┘
```

**자동 호출** (`/sdd-autopilot` 사용):

```
┌─────────────────────────────────────────────────────┐
│ sdd-autopilot: 적응형 파이프라인 자율 실행                  │
│                                                       │
│ Step 0 (Pipeline State Detection):                    │
│   기존 미완료 파이프라인 감지 → 재개/새로 시작 선택     │
│                                                       │
│ Phase 1 (Interactive):                                │
│   인라인 discussion → 코드베이스 탐색 → 규모 판단      │
│   산출물 스캔 → 시작점/종료점 감지                      │
│                                                       │
│ Phase 1.5 (Checkpoint):                               │
│   오케스트레이터 생성 → 사용자 확인                     │
│                                                       │
│ Phase 2 (Autonomous):                                 │
│   규모별 에이전트 파이프라인 자율 실행                   │
│   ├── 소: impl → inline test                          │
│   ├── 중: draft → plan → impl → review → test → sync │
│   └── 대: full SDD pipeline (모든 에이전트)            │
└─────────────────────────────────────────────────────┘
```

#### PR 프로세스

```
PR 생성 → pr-review → (merge 후) spec-update-done
```

#### 스펙 유지보수

```
코드 변경 감지 → spec-review → (SYNC_REQUIRED 시) spec-update-done
스펙 복잡도 증가 → spec-rewrite
현황 파악 → spec-summary
레거시 스펙 → spec-upgrade
```

### _sdd/ Artifact Map

Artifact naming policy:

- canonical 결과 파일명은 소문자 `snake_case`를 사용한다.
- 새 산출물은 canonical lowercase 경로에 저장한다.
- transition 기간 동안 reader는 lowercase canonical 경로를 먼저 확인하고, 파일이 없으면 legacy uppercase 경로를 fallback으로 확인한다.
- historical artifact와 changelog에 남은 uppercase 파일명은 당시 실제 경로를 보존할 수 있다.
- 신규 백업 파일명은 `prev_<filename>_<timestamp>.md`를 canonical로 사용한다.

| 경로 | 생성 스킬 | 설명 |
|------|----------|------|
| `_sdd/spec/<project>.md` | spec-create | 메인 스펙 문서 |
| `_sdd/spec/summary.md` | spec-summary | 스펙 요약 |
| `_sdd/spec/logs/spec_review_report.md` | spec-review | 리뷰 리포트 |
| `_sdd/spec/logs/rewrite_report.md` | spec-rewrite | 리라이트 리포트 |
| `_sdd/spec/decision_log.md` | spec-create, feature-draft | 의사결정 로그 |
| `_sdd/drafts/feature_draft_*.md` | feature-draft | 피처 드래프트 |
| `_sdd/guides/guide_*.md` | guide-create | 기능별 가이드 |
| `_sdd/implementation/implementation_plan.md` | implementation-plan | 구현 계획 |
| `_sdd/implementation/implementation_report*.md` | implementation | 구현 리포트 |
| `_sdd/implementation/implementation_review.md` | implementation-review | 구현 검증 |
| `_sdd/pr/pr_review.md` | pr-review | PR 리뷰 (spec 존재 시 spec-patch 기능 포함) |
| `.claude/skills/orchestrator_<topic>/SKILL.md` 또는 `.codex/skills/orchestrator_<topic>/SKILL.md` | sdd-autopilot | 실행 중 활성 오케스트레이터 (스킬로 재사용/재개 가능) |
| `_sdd/pipeline/log_<topic>_<ts>.md` | sdd-autopilot | 파이프라인 실행 로그 (Meta + Status 테이블 + Execution Log) |
| `_sdd/pipeline/report_<topic>_<ts>.md` | sdd-autopilot | 파이프라인 최종 요약 리포트 (실행 결과, 리뷰 결과, 잔여 이슈) |
| `_sdd/pipeline/orchestrators/<topic>_<ts>/` | sdd-autopilot | 완료된 오케스트레이터 아카이브 |
| `ralph/` | ralph-loop-init | 장기 실행 프로세스 자동화 디버그 루프 |

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| 스킬 정의 형식 | Markdown (SKILL.md) | AI 에이전트가 직접 해석 가능한 스킬 정의 |
| 메타데이터 | JSON (skill.json) | 스킬 매칭, 버전 관리 |
| 배포 | Claude Code Plugin Marketplace, Codex LobeHub | 원클릭 설치 |
| 실행 환경 | Claude Code CLI, Codex CLI | AI 에이전트 실행 플랫폼 |

---

## Component Details

### Skill & Agent Category Overview

| 카테고리 | 스킬 | 실행 형태 | 역할 |
|----------|------|-----------|------|
| **메타** | sdd-autopilot | 풀 스킬 | reasoning 기반 적응형 오케스트레이터 생성 + end-to-end 자율 파이프라인 실행 |
| **스펙 생성/관리** | spec-create | 풀 스킬 | 코드 분석 또는 초안에서 스펙 문서 생성 |
| | spec-review | 래퍼 → 에이전트 | 스펙 품질 및 코드-스펙 드리프트 검증 (read-only) |
| | spec-rewrite | 풀 스킬 | 과도하게 긴/복잡한 스펙 구조 재정리 |
| | spec-summary | 풀 스킬 | 스펙 요약본 생성 (현황 파악, 온보딩용) |
| | spec-update-todo | 래퍼 → 에이전트 | 새 기능/요구사항을 스펙에 사전 반영 |
| | spec-update-done | 래퍼 → 에이전트 | 구현 완료 후 코드와 스펙 동기화 |
| | spec-upgrade | 풀 스킬 | 구 형식 스펙을 whitepaper §1-§8로 변환 |
| | guide-create | 풀 스킬 | 스펙에서 기능별 구현/리뷰 가이드 생성 |
| **구현** | feature-draft | 래퍼 → 에이전트 | 스펙 패치 초안 + 구현 계획을 한 번에 생성 |
| | implementation-plan | 래퍼 → 에이전트 | Phase별 구현 계획 수립 (Target Files 포함) |
| | implementation | 래퍼 → 에이전트 | TDD 기반 병렬 구현 실행 |
| | implementation-review | 래퍼 → 에이전트 | 계획 대비 구현 진행 검증 |
| **PR 프로세스** | pr-review | 풀 스킬 | PR 코드 품질 검증 + spec 존재 시 spec 기반 추가 검증 및 판정 |
| **보조** | discussion | 풀 스킬 | 구조화된 의사결정 토론 (Claude Code + Codex 지원) |
| | ralph-loop-init | 래퍼 → 에이전트 | 장기 실행 프로세스(ML, e2e, 빌드 등) 자동화 디버그 루프 생성 |
| | investigate | 래퍼 → 에이전트 | 범용 체계적 디버깅 (근본원인 우선, 3-strike 에스컬레이션, scope lock, blast radius gate, fresh verification, 독립 Agent 교차 검증) |
| **유틸리티** | git | 풀 스킬 | 스마트 Git 워크플로우 자동화 (커밋, 브랜치, 리베이스) |
| | second-opinion | 풀 스킬 | Codex를 통한 독립적 second opinion 분석 (Claude Code 전용) |
| | spec-snapshot | 풀 스킬 | 스펙 번역 스냅샷 생성 |
| | write-phased | 유틸리티 스킬 | helper agent 없이 caller가 skeleton → fill → finalize를 수행하도록 돕는 공용 inline writing contract |

> Codex parity note: wrapper-backed 핵심 단계는 `.codex/skills/<name>/` 아래 사용자 진입점을 유지하고, 실제 spawned execution unit은 `.codex/agents/<name>.toml` custom agent가 맡는다.

**Claude 에이전트 목록** (`.claude/agents/`):

모든 Claude 에이전트(9개)는 **non-interactive**로 동작한다. AskUserQuestion을 사용하지 않으며, 모호한 상황에서는 Autonomous Decision-Making 패턴에 따라 자율 판단하고 근거를 출력에 기록한다.

| 에이전트 | tools | 호출 경로 |
|----------|-------|-----------|
| feature-draft | Read, Write, Edit, Glob, Grep, Agent | 래퍼 스킬, sdd-autopilot, 또는 generated orchestration skill |
| implementation-plan | Read, Write, Edit, Glob, Grep, Agent | 래퍼 스킬, sdd-autopilot, 또는 generated orchestration skill |
| implementation | Read, Write, Edit, Glob, Grep, Bash, Agent | 래퍼 스킬, sdd-autopilot, 또는 generated orchestration skill |
| implementation-review | Read, Glob, Grep, Agent | 래퍼 스킬, sdd-autopilot, 또는 generated orchestration skill |
| ralph-loop-init | Read, Write, Edit, Glob, Grep, Bash | 래퍼 스킬, sdd-autopilot, 또는 generated orchestration skill |
| spec-review | Read, Glob, Grep, Agent | 래퍼 스킬, sdd-autopilot, 또는 generated orchestration skill |
| spec-update-done | Read, Write, Edit, Glob, Grep, Bash | 래퍼 스킬, sdd-autopilot, 또는 generated orchestration skill |
| spec-update-todo | Read, Write, Edit, Glob, Grep | 래퍼 스킬, sdd-autopilot, 또는 generated orchestration skill |
| investigate | Read, Write, Edit, Glob, Grep, Bash, Agent | 래퍼 스킬, sdd-autopilot, 또는 직접 호출 |

**Codex custom agent 목록** (`.codex/agents/`):

| Agent | 역할 | Spawn 경로 |
|-------|------|-----------|
| feature_draft | 스펙 패치 초안 + 구현 계획 생성 | wrapper skill 또는 generated orchestrator |
| implementation_plan | 상세 구현 계획 생성 | wrapper skill 또는 generated orchestrator |
| implementation | TDD 기반 구현 실행 | wrapper skill 또는 generated orchestrator |
| implementation_review | findings-first 구현 검증 | wrapper skill 또는 generated orchestrator |
| spec_update_todo | planned spec patch 반영 | wrapper skill 또는 generated orchestrator |
| spec_update_done | 구현 결과 기반 spec sync | wrapper skill 또는 generated orchestrator |
| spec_review | review-only spec audit | wrapper skill 또는 generated orchestrator |
| ralph_loop_init | 장시간 debug/training loop 생성 | wrapper skill 또는 generated orchestrator |
| investigate | 범용 체계적 디버깅 | wrapper skill 또는 직접 호출 |

> 각 스킬/에이전트의 Purpose, Why, Source, Process 등 상세 정보는 [components.md](./components.md)를 참고한다.

---

## Usage Guide & Expected Results

> 상세 시나리오는 [usage-guide.md](./usage-guide.md)를 참고한다.

대표 시나리오: 새 프로젝트 스펙 생성(`/spec-create`), 대규모 기능 수동 추가(6단계), sdd-autopilot 자동 실행, PR 기반 스펙 동기화, 스펙 현황 파악 및 의사결정.

---

## Environment & Dependencies

### Directory Structure

```
sdd_skills/
├── README.md                    # 프로젝트 소개 + 설치 가이드
├── CLAUDE.md                    # Claude Code 워크스페이스 안내
│
├── docs/
│   ├── SDD_CONCEPT.md           # SDD 핵심 개념 설명
│   ├── SDD_QUICK_START.md       # 빠른 참조 가이드
│   ├── SDD_WORKFLOW.md          # 종합 워크플로우 가이드
│   └── AUTOPILOT_GUIDE.md       # sdd-autopilot 메타스킬 사용 가이드
│
├── .claude/
│   ├── agents/                  # 에이전트 정의 (9개)
│   │   ├── feature-draft.md
│   │   ├── implementation-plan.md
│   │   ├── implementation.md
│   │   ├── implementation-review.md
│   │   ├── ralph-loop-init.md
│   │   ├── investigate.md
│   │   ├── spec-review.md
│   │   ├── spec-update-done.md
│   │   └── spec-update-todo.md
│   │
│   └── skills/                  # Claude Code 스킬 (20개)
│       ├── sdd-autopilot/       # 적응형 오케스트레이터 메타스킬
│       ├── discussion/
│       ├── feature-draft/       # [래퍼] → agents/feature-draft.md (references/ 삭제)
│       ├── git/
│       ├── guide-create/
│       ├── implementation/      # [래퍼] → agents/implementation.md (references/ 삭제)
│       ├── implementation-plan/ # [래퍼] → agents/implementation-plan.md (references/ 삭제)
│       ├── implementation-review/ # [래퍼] → agents/implementation-review.md (references/ 삭제)
│       ├── investigate/         # [래퍼] → agents/investigate.md
│       ├── pr-review/
│       ├── ralph-loop-init/     # [래퍼] → agents/ralph-loop-init.md (references/ 삭제)
│       ├── second-opinion/      # Codex 독립 분석 (Claude Code 전용)
│       ├── spec-create/
│       ├── spec-review/         # [래퍼] → agents/spec-review.md (references/ 삭제)
│       ├── spec-rewrite/
│       ├── spec-snapshot/
│       ├── spec-summary/
│       ├── spec-update-done/    # [래퍼] → agents/spec-update-done.md (references/ 삭제)
│       ├── spec-update-todo/    # [래퍼] → agents/spec-update-todo.md (references/ 삭제)
│       ├── spec-upgrade/
│       └── write-phased/        # 공용 inline writing contract
│
├── .codex/
│   ├── config.toml              # Codex custom agent 실행 설정
│   ├── agents/                  # Codex custom agent 정의 (9개)
│   │   ├── feature-draft.toml
│   │   ├── implementation-plan.toml
│   │   ├── implementation.toml
│   │   ├── implementation-review.toml
│   │   ├── investigate.toml
│   │   ├── ralph-loop-init.toml
│   │   ├── spec-review.toml
│   │   ├── spec-update-done.toml
│   │   └── spec-update-todo.toml
│   └── skills/                  # Codex 스킬 (19개, git/second-opinion 제외)
│       ├── sdd-autopilot/       # Codex 메타스킬
│       ├── write-phased/        # 공용 long-form writing utility
│       └── (wrapper/direct skill layer)
│
├── .claude-plugin/              # Claude Code Plugin 설정
│
├── scripts/
│   ├── generate_sdd_seminar_ppt.py
│   ├── generate_sdd_skills_keynote_60.py
│   └── sdd_seminar_ko.pptx
│
└── _sdd/
    ├── spec/
    │   ├── main.md              # 이 스펙 문서 (인덱스)
    │   ├── components.md        # §4 컴포넌트 상세 + Code Reference Index
    │   ├── usage-guide.md       # §5 사용 가이드 & 기대 결과
    │   ├── DECISION_LOG.md      # 의사결정 로그
    │   └── logs/
    │       └── changelog.md     # 버전별 변경 기록
    ├── discussion/              # 토론 기록
    ├── drafts/                  # 피처 드래프트
    ├── implementation/          # 구현 계획/리포트
    └── pipeline/                # [신규] sdd-autopilot 파이프라인 실행 로그 + 완료 오케스트레이터 아카이브
```

### Platform Differences

| 항목 | Claude Code | Codex |
|------|------------|-------|
| 스킬 경로 | `.claude/skills/` | `.codex/skills/` |
| 에이전트 경로 | `.claude/agents/` | `.codex/agents/` |
| 설치 방법 | Plugin Marketplace | LobeHub / 수동 복사 |
| 스킬 수 | 21개 (래퍼 9 + 풀 11 + 메타 1) | 19개 (wrapper/direct 17 + utility 1 + 메타 1) |
| 에이전트 수 | 9개 | 9개 |
| AskUserQuestion | 풀 스킬에서만 사용 (에이전트는 non-interactive) | `request_user_input` 기반 대화형 처리 |
| Agent tool | 지원 (서브에이전트 호출) | 지원 (custom agent spawn) |
| SKILL.md 차이 | 래퍼 또는 풀 | wrapper/direct skill + custom agent + generated orchestration skill |
| sdd-autopilot | 지원 | 지원 |

**Codex 제한 사항:**
- `AskUserQuestion` 도구 미지원 → `request_user_input` 기반으로 대화형 단계를 처리
- 활성 오케스트레이터는 `.codex/skills/orchestrator_<topic>/`에 두고, 완료 후 `_sdd/pipeline/orchestrators/<topic>_<ts>/`로 이동한다
- `git`은 Claude Code 전용이며, 나머지 핵심 워크플로우 스킬은 Codex에서도 지원한다

### Installation

**Claude Code (Plugin):**
```
/plugin marketplace add malfo-y/sdd-skills
/plugin install sdd-skills@sdd-skills
```

**Codex:**
- **Option A**: LobeHub Skills Marketplace 경유 (README.md 참조)
- **Option B**: `.codex/skills/` 내용을 `$CODEX_HOME/skills/`에 수동 복사

---

## Identified Issues & Improvements

> 해결 완료 이슈(#1-4, #8-16)는 [changelog.md](./logs/changelog.md)에서 확인 가능.

### 중간 우선순위

5. **Codex 스킬 동기화 수동 프로세스**
   - 현황: `.claude/skills/`를 수정하면 `.codex/skills/`도 수동으로 동기화 필요
   - 제안: 동기화 스크립트 작성 또는 빌드 프로세스 도입

6. **스킬 버전 관리 미흡**
   - 현황: v3.6 리팩토링으로 다수 skill.json이 갱신되었으나, 일부 여전히 고정
   - 제안: SKILL.md 변경 시 semver 업데이트 규칙 정립

### 낮은 우선순위

7. **docs/sdd.md가 독립 개념서**
   - 현황: SDD 개념 설명 문서이나 스킬과 직접 연결되지 않음
   - 제안: docs/SDD_WORKFLOW.md에서 참조 링크 추가

---

## Appendix

- [Component Details + Code Reference Index](./components.md)
- [Usage Guide & Expected Results](./usage-guide.md)
- [Changelog](./logs/changelog.md)
- [Decision Log](./DECISION_LOG.md)
- Platform primary target을 `.claude/skills/`로 재설정
