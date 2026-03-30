# SDD Skills

> Markdown 기반 스킬 시스템으로 AI 에이전트의 Spec-Driven Development 워크플로우를 구조화한다.

**Version**: 3.7.0
**Last Updated**: 2026-03-24
**Status**: Approved

## Table of Contents

- [Background & Motivation](#background--motivation)
- [Core Design](#core-design)
- [Architecture Overview](#architecture-overview)
- [Component Details](#component-details)
- [Usage Guide & Expected Results](#usage-guide--expected-results)
- [Environment & Dependencies](#environment--dependencies)
- [Identified Issues & Improvements](#identified-issues--improvements)
- [Appendix: Code Reference Index](#appendix-code-reference-index)

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

- **21개 스킬 + 20개 에이전트**: 스킬은 사용자 인터페이스(`/스킬명`), 에이전트는 플랫폼별로 spawn 가능한 자동화 파이프라인 실행 단위 (Claude 10 + Codex 10 계획). 모든 agent와 full skill은 **AC-First 구조**(Acceptance Criteria + 자체 검증 + Final Check)로 통일
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
- Claude 10개 에이전트와 Codex 10개 custom agent가 각 플랫폼 실행 모델에 맞게 정상 동작 (모두 AC-First + Self-Contained 구조)
- sdd-autopilot이 reasoning 기반 파이프라인을 생성하고 end-to-end 자율 실행 완료 (재개/부분 실행 지원)
- Codex에서 19개 스킬(discussion 포함, git 제외)이 정상 동작
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

**2-Phase Generation 패턴**: `spec-create` [`.claude/skills/spec-create/SKILL.md`], `spec-rewrite`, `spec-upgrade`에서 사용. 대형 스펙 생성 시 골조(skeleton) → 내용 채우기(fill)로 분리하여 LLM 컨텍스트 윈도우 한계와 후반부 품질 저하를 방지한다.

**Agent Wrapper 패턴**: 스킬을 에이전트로 전환할 때 적용한다. Claude에서는 전체 로직을 `.claude/agents/<name>.md` 에이전트 정의로 이동하고, 기존 `.claude/skills/<name>/SKILL.md`는 에이전트에 위임하는 최소한의 래퍼로 전환한다. Codex에서는 같은 역할 분리를 `.codex/agents/<name>.toml` custom agent와 `.codex/skills/<name>/SKILL.md` wrapper로 구현한다. 이를 통해 사용자의 `/스킬명` 호출 인터페이스를 유지하면서 플랫폼별 실행 단위를 재사용할 수 있다. `write-phased`에서 최초 검증된 패턴이며, v3.0 이후 핵심 파이프라인 스킬에 확대 적용하였다. 현재 래퍼 스킬은 **Mirror 패턴**(아래)으로 구현되어 있다.

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
3. **기존 파일 백업**: 덮어쓰기 전 `prev/PREV_<filename>_<timestamp>.md`로 아카이브
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
| Agent Wrapper 패턴 | 스킬 인터페이스 유지 + 플랫폼별 실행 단위 재사용 가능. write-phased에서 검증됨 | 스킬 완전 제거 (거부: 사용자 `/스킬명` 호출 불가) |
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
              │     └── .codex/skills/   (Codex 스킬 20개)
              │           ├── 래퍼/직접 스킬 (18개) ─── user entry + workflow contract
              │           ├── 유틸리티 스킬 (1개) ─── write-phased
              │           └── 메타스킬 (1개) ─── sdd-autopilot (오케스트레이터 생성)
              │
              ├── Agent Layer
              │     ├── Claude: .claude/agents/
              │     ├── 파이프라인 에이전트 (9개) ─── 래퍼 스킬에서 위임받아 실행
              │     └── 유틸리티 에이전트 (1개) ─── write-phased
              │
              ├── Codex Agent Layer
              │     ├── .codex/agents/  (Codex custom agent 10개)
              │     ├── 파이프라인 에이전트 (9개) ─── wrapper skill과 orchestrator가 직접 spawn
              │     └── 유틸리티 에이전트 (1개) ─── write_phased
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
    │     │     └── 서브에이전트 호출 가능 (write-phased 등)
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
PR 생성 → pr-spec-patch → pr-review → (merge 후) spec-update-done
```

#### 스펙 유지보수

```
코드 변경 감지 → spec-review → (SYNC_REQUIRED 시) spec-update-done
스펙 복잡도 증가 → spec-rewrite
현황 파악 → spec-summary
레거시 스펙 → spec-upgrade
```

### _sdd/ Artifact Map

| 경로 | 생성 스킬 | 설명 |
|------|----------|------|
| `_sdd/spec/<project>.md` | spec-create | 메인 스펙 문서 |
| `_sdd/spec/SUMMARY.md` | spec-summary | 스펙 요약 |
| `_sdd/spec/SPEC_REVIEW_REPORT.md` | spec-review | 리뷰 리포트 |
| `_sdd/spec/REWRITE_REPORT.md` | spec-rewrite | 리라이트 리포트 |
| `_sdd/spec/DECISION_LOG.md` | spec-create, feature-draft | 의사결정 로그 |
| `_sdd/drafts/feature_draft_*.md` | feature-draft | 피처 드래프트 |
| `_sdd/guides/guide_*.md` | guide-create | 기능별 가이드 |
| `_sdd/implementation/IMPLEMENTATION_PLAN.md` | implementation-plan | 구현 계획 |
| `_sdd/implementation/IMPLEMENTATION_REPORT*.md` | implementation | 구현 리포트 |
| `_sdd/implementation/IMPLEMENTATION_REVIEW.md` | implementation-review | 구현 검증 |
| `_sdd/pr/spec_patch_draft.md` | pr-spec-patch | PR 스펙 패치 |
| `_sdd/pr/PR_REVIEW.md` | pr-review | PR 리뷰 |
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
| **PR 프로세스** | pr-spec-patch | 풀 스킬 | PR과 스펙 비교하여 패치 초안 생성 |
| | pr-review | 풀 스킬 | PR을 스펙/패치 초안 대비 검증 및 판정 |
| **보조** | discussion | 풀 스킬 | 구조화된 의사결정 토론 (Claude Code + Codex 지원) |
| | ralph-loop-init | 래퍼 → 에이전트 | 장기 실행 프로세스(ML, e2e, 빌드 등) 자동화 디버그 루프 생성 |
| | investigate | 래퍼 → 에이전트 | 범용 체계적 디버깅 (근본원인 우선, 3-strike 에스컬레이션, scope lock, blast radius gate, fresh verification, 독립 Agent 교차 검증) |
| **유틸리티** | git | 풀 스킬 | 스마트 Git 워크플로우 자동화 (커밋, 브랜치, 리베이스) |
| | spec-snapshot | 풀 스킬 | 스펙 번역 스냅샷 생성 |
| | write-phased | 유틸리티 스킬 | 긴 문서/코드 출력을 skeleton → fill 2단계로 작성하는 공용 writing utility |

> Codex parity note: wrapper-backed 핵심 단계는 `.codex/skills/<name>/` 아래 사용자 진입점을 유지하고, 실제 spawned execution unit은 `.codex/agents/<name>.toml` custom agent가 맡는다.

**Claude 에이전트 목록** (`.claude/agents/`):

모든 파이프라인 에이전트(8개)는 **non-interactive**로 동작한다. AskUserQuestion을 사용하지 않으며, 모호한 상황에서는 Autonomous Decision-Making 패턴에 따라 자율 판단하고 근거를 출력에 기록한다.

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
| write-phased | Read, Write, Edit, Glob, Grep, Agent | 다른 에이전트의 서브에이전트 |

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
| write_phased | skeleton → fill nested writing utility | direct skill 또는 nested custom agent |

### sdd-autopilot

| Aspect | Description |
|--------|-------------|
| **Purpose** | 사용자 요청을 분석하여 reasoning 기반 적응형 오케스트레이터를 생성하고, 플랫폼별 에이전트 파이프라인을 end-to-end 자율 실행 |
| **Why** | 대규모 기능 구현 시 6-7개 스킬을 수동 호출하면 맥락 유실과 단계 누락 위험이 있다. sdd-autopilot이 SDD 철학을 이해하고 상황에 맞는 파이프라인을 동적으로 구성하여 사용자는 요구사항만 전달하면 된다. |
| **Input** | 사용자의 기능 요청 (자연어) |
| **Output** | 구현 완료된 코드 + 동기화된 스펙 + 활성 오케스트레이터(`.claude/skills/orchestrator_<topic>/SKILL.md` 또는 `.codex/skills/orchestrator_<topic>/SKILL.md`) + `_sdd/pipeline/log_<topic>_<ts>.md` + `_sdd/pipeline/report_<topic>_<ts>.md` + 완료 시 `_sdd/pipeline/orchestrators/<topic>_<ts>/` 아카이브 |
| **Source** | `.claude/skills/sdd-autopilot/SKILL.md` (v2.0.0) |
|            | `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`: SDD 철학 + 스킬 카탈로그 (reasoning 기반 파이프라인 구성의 핵심 입력) |
|            | `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`: 오케스트레이터 예시 |
|            | `.codex/skills/sdd-autopilot/SKILL.md` (v2.2.0) |
|            | `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`: Codex용 SDD 철학 + 스킬 카탈로그 |
|            | `docs/AUTOPILOT_GUIDE.md`: 사용 가이드 + Codex 검증 체크리스트 |
| **Process** | Step 0 (Pipeline State Detection): 기존 미완료 파이프라인 감지 → 재개/새로 시작 선택 → Phase 1 (Interactive): Step 1 Reference Loading (SDD 철학 + 스킬 카탈로그 내재화) → Step 2 요청 분석 + 인라인 discussion (시작점/종료점 감지, 산출물 스캔, Review-Fix 사이클 필수 검증) → Step 3 코드베이스 탐색 → Step 4 Reasoning 기반 오케스트레이터 생성 + Pre-flight Check(`_sdd/env.md`) → Step 5 Orchestrator Verification (구조 6항목 + 철학 6항목 = 12항목 검증, Producer-Reviewer 패턴) → Phase 1.5 (Checkpoint): 검증 결과 + 파이프라인 요약 + Pre-flight Check → 사용자 확인 → Phase 2 (Autonomous): Claude는 `.claude/agents/`, Codex는 `.codex/agents/`를 직접 사용해 자율 파이프라인 실행 (Execute -> Verify 루프) + 마일스톤 로그 (Meta + Status 테이블). Codex의 장문 planning/review 단계는 필요 시 nested `write_phased`를 사용한다. 완료 후 오케스트레이터를 `_sdd/pipeline/orchestrators/<topic>_<ts>/`로 아카이브. **Hard Rule #9**: review 포함 시 review -> fix -> re-review 사이클 필수. **Hard Rule #10**: 모든 단계에 Execute -> Verify 필수. `implementation-review`는 조건부 핵심 단계 |
| **Dependencies** | 글로벌 스펙(`_sdd/spec/main.md`) 존재 필수. 스펙이 없으면 오케스트레이터 생성을 중단하고 `/spec-create` 실행을 안내 |
| **실행 형태** | 풀 스킬 (사용자 인터랙션이 핵심이므로 에이전트 전환 불필요). Codex는 generated orchestration skill이 `.codex/agents/` custom agents를 직접 spawn |
| **✅ 완료** | **Audit Trail + Taste Decision**: Step 7.2 실행 루프에서 모든 자동 결정을 로그에 기록 (판단 근거 포함). Taste decision(`[DECISION] <what> -- <why> -- <taste: yes/no>`)은 Step 8 최종 보고서에 표면화. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |

### spec-create

| Aspect | Description |
|--------|-------------|
| **Purpose** | 프로젝트 코드 분석 또는 사용자 초안을 기반으로 SDD 스펙 문서 생성 |
| **Why** | 스펙이 없으면 AI 에이전트가 일관된 코드를 생성할 수 없다. 워크플로우의 시작점으로서 Single Source of Truth를 생성하는 역할을 분리했다. |
| **Input** | 프로젝트 코드베이스, user_draft.md, 사용자 대화 |
| **Output** | `_sdd/spec/<project>.md`, CLAUDE.md, AGENTS.md, _sdd/env.md (부트스트랩) |
| **Source** | `.claude/skills/spec-create/SKILL.md` |
| **Process** | Step 1 정보 수집 → Step 2 분석 → Step 2.5 Checkpoint → Step 2.7 생성 전략 → Step 3 부트스트랩 + 작성 |
| **Dependencies** | 없음 (워크플로우 시작점) |

### feature-draft

| Aspect | Description |
|--------|-------------|
| **Purpose** | 요구사항 수집 → 스펙 패치 초안(Part 1) + 구현 계획(Part 2)을 단일 파일로 생성 |
| **Why** | 스펙 수정과 구현 계획을 별도로 진행하면 반복 작업이 발생한다. 두 산출물을 한 번에 생성하여 워크플로우 효율을 높인다. |
| **Input** | 기존 스펙, 사용자 요구사항, 코드베이스 |
| **Output** | `_sdd/drafts/feature_draft_<name>.md` |
| **Source** | `.claude/agents/feature-draft.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/feature-draft/SKILL.md` (래퍼) |
| **Process** | 7단계: 입력 분석 → 맥락 수집 → 질문 → 설계 → Part 1 → Part 2 → 저장 |
| **Dependencies** | spec-create (스펙이 있어야 Part 1 생성 가능) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |
| **✅ 완료** | **Failure Modes 테이블**: Part 1 스펙 패치에 경량 Failure Modes 테이블 섹션을 항상 포함. 간단하면 N/A 또는 1-2행, 복잡하면 3-5행 (시나리오/실패 시/사용자 가시성/처리 방안). <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |

### spec-update-todo

| Aspect | Description |
|--------|-------------|
| **Purpose** | 새 기능/요구사항을 스펙에 사전 반영 (구현 전 드리프트 방지) |
| **Why** | 구현 후에만 스펙을 업데이트하면 스펙-코드 간 드리프트가 누적된다. 사전 반영으로 스펙이 항상 의도를 정확히 반영하도록 한다. |
| **Input** | user_spec.md 또는 feature-draft Part 1 |
| **Output** | 스펙 파일 직접 수정 + 변경 요약 리포트 |
| **Source** | `.claude/agents/spec-update-todo.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/spec-update-todo/SKILL.md` (래퍼) |
| **Dependencies** | spec-create (스펙 존재 필수) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |

### spec-update-done

| Aspect | Description |
|--------|-------------|
| **Purpose** | 구현 완료 후 코드 변경사항을 스펙에 반영 |
| **Why** | 구현 과정에서 스펙과 다르게 구현된 부분을 감지하고 스펙을 최신 상태로 동기화한다. |
| **Input** | 구현 리포트, 코드 diff, 기존 스펙 |
| **Output** | 스펙 파일 업데이트 + 아카이브 |
| **Source** | `.claude/agents/spec-update-done.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/spec-update-done/SKILL.md` (래퍼) |
| **Dependencies** | implementation 완료 후 실행 |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |

### spec-review

| Aspect | Description |
|--------|-------------|
| **Purpose** | 스펙 품질 검증 + 코드-스펙 드리프트 감지 (read-only) |
| **Why** | 스펙 수정 없이 현재 상태를 객관적으로 진단하는 역할을 분리했다. 수정과 진단을 같은 스킬에서 하면 사용자가 의도치 않은 변경을 받을 위험이 있다. |
| **Input** | 스펙 파일, 코드베이스 |
| **Output** | `_sdd/spec/SPEC_REVIEW_REPORT.md` |
| **Source** | `.claude/agents/spec-review.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/spec-review/SKILL.md` (래퍼) |
| **판정** | SPEC_OK / SYNC_REQUIRED / NEEDS_DISCUSSION 3단계 |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |
| **✅ 완료** | **Code Analysis Metrics**: 핫스팟(자주 변경 파일), Focus Score(변경 집중도), Test Coverage(스펙 기능별 테스트 현황) 지표를 Step 3.5에 추가하여 데이터 기반 리뷰 우선순위 판단. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |

### spec-rewrite

| Aspect | Description |
|--------|-------------|
| **Purpose** | 과도하게 긴/복잡한 스펙을 구조 재정리 (파일 분할, 부록 이동) |
| **Why** | 스펙이 커지면 AI 에이전트가 전체를 컨텍스트에 로드하기 어렵고, 사용자도 관리가 힘들다. 구조 재정리를 별도 스킬로 분리하여 안전하게 수행한다. |
| **Input** | 기존 스펙 파일 |
| **Output** | 재구성된 스펙 파일 + `REWRITE_REPORT.md` |
| **Source** | `.claude/skills/spec-rewrite/SKILL.md` |

### spec-summary

| Aspect | Description |
|--------|-------------|
| **Purpose** | 스펙의 인간 친화적 요약본 생성 |
| **Why** | 전체 스펙을 읽지 않고도 현재 프로젝트 상태를 파악하거나, 새 팀원 온보딩에 활용할 수 있도록 요약을 분리했다. |
| **Input** | 스펙 파일, 구현 진행 현황 |
| **Output** | `_sdd/spec/SUMMARY.md`, 선택적 README 블록 |
| **Source** | `.claude/skills/spec-summary/SKILL.md` |

### spec-upgrade

| Aspect | Description |
|--------|-------------|
| **Purpose** | 구 형식 스펙을 whitepaper §1-§8 구조로 변환 |
| **Why** | SDD_SPEC_DEFINITION 제정 이전에 만든 레거시 스펙을 표준 형식으로 마이그레이션하는 전용 스킬. 업그레이드와 일반 리라이트는 관심사가 다르다. |
| **Input** | 기존 스펙 파일, 코드베이스 |
| **Output** | whitepaper 형식으로 변환된 스펙 파일 |
| **Source** | `.claude/skills/spec-upgrade/SKILL.md` |

### guide-create

| Aspect | Description |
|--------|-------------|
| **Purpose** | 스펙에서 특정 기능의 구현/리뷰 가이드 문서 생성 |
| **Why** | 전체 스펙은 방대하므로, 특정 기능에 집중한 가이드를 생성하여 구현자나 리뷰어가 필요한 정보만 빠르게 참조할 수 있도록 한다. |
| **Input** | 스펙 파일, 기능명 |
| **Output** | `_sdd/guides/guide_<feature>.md` |
| **Source** | `.claude/skills/guide-create/SKILL.md` |

### implementation-plan

| Aspect | Description |
|--------|-------------|
| **Purpose** | 대규모 구현을 위한 Phase별 구현 계획 수립 |
| **Why** | 복잡한 구현을 단일 세션에서 수행하면 맥락 유실과 품질 저하가 발생한다. Target Files 기반 병렬 실행 분석으로 효율적 구현을 계획한다. |
| **Input** | 스펙, feature-draft Part 2, 코드베이스 |
| **Output** | `_sdd/implementation/IMPLEMENTATION_PLAN.md` |
| **Source** | `.claude/agents/implementation-plan.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/implementation-plan/SKILL.md` (래퍼) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |
| **✅ 완료** | **Test Coverage Mapping**: Target Files에 [M] 마커가 있을 때 해당 파일의 기존 테스트 커버리지를 매핑. [C] 전용이면 스킵. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |

### implementation

| Aspect | Description |
|--------|-------------|
| **Purpose** | 구현 계획에 따른 TDD 기반 코드 작성 실행 |
| **Why** | AI 에이전트의 구현 실행을 계획에 따라 체계적으로 수행하고, Target Files 기반 병렬 Agent 실행으로 효율을 높인다. |
| **Input** | 구현 계획, 코드베이스 |
| **Output** | 구현된 코드 + `IMPLEMENTATION_REPORT.md` |
| **Source** | `.claude/agents/implementation.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/implementation/SKILL.md` (래퍼) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |
| **✅ 완료** | **Verification Gate Iron Rule**: "should work" 금지, 코드 변경 후 테스트 재실행 필수, 이전 결과 재사용 금지를 Hard Rule로 추가. env.md 미존재 시 코드 분석 기반 fallback 허용, 리포트에 "UNTESTED" 명시. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |
| **✅ 완료** | **Regression Iron Rule**: 기존 테스트 실패 시 테스트 업데이트 + 회귀 방지 테스트 추가를 필수 단계로 강제. 사용자 확인 없이 자동. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |

### implementation-review

| Aspect | Description |
|--------|-------------|
| **Purpose** | 구현 계획 대비 실제 구현 진행 검증 |
| **Why** | 구현 중간/후에 계획 대비 진행률과 품질을 객관적으로 검증하여, 누락이나 이탈을 조기에 발견한다. |
| **Input** | 구현 계획, 구현 리포트, 코드 |
| **Output** | 검증 리포트 + 다음 단계 제안 |
| **Source** | `.claude/agents/implementation-review.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/implementation-review/SKILL.md` (래퍼) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |
| **✅ 완료** | **Fresh Verification**: 코드를 읽고 "맞다"가 아니라 테스트 실행 출력을 근거로 판단. "should work" 금지. 테스트 실행 불가 시(env.md 미존재) fallback 명시. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |

### pr-spec-patch

| Aspect | Description |
|--------|-------------|
| **Purpose** | PR 변경사항과 스펙을 비교하여 패치 초안 생성 |
| **Why** | PR 리뷰 전에 스펙 관점의 영향 분석을 별도로 수행하여, 리뷰어가 스펙 준수 여부를 판단할 근거를 제공한다. |
| **Input** | PR 번호 (gh CLI), 스펙 파일 |
| **Output** | `_sdd/pr/spec_patch_draft.md` |
| **Source** | `.claude/skills/pr-spec-patch/SKILL.md` |

### pr-review

| Aspect | Description |
|--------|-------------|
| **Purpose** | PR 구현을 스펙 및 패치 초안 대비 검증하여 APPROVE/REQUEST CHANGES 판정 |
| **Why** | 스펙 기반 PR 리뷰를 자동화하여 일관된 품질 기준을 적용한다. |
| **Input** | PR 번호, 스펙, spec_patch_draft.md |
| **Output** | `_sdd/pr/PR_REVIEW.md` |
| **Source** | `.claude/skills/pr-review/SKILL.md` |
| **✅ 완료** | **Scope Drift Detection**: PR diff 변경 파일 vs 스펙 패치 초안 범위를 비교하는 Step 2.5 pre-step 추가. CLEAN/DRIFT/MISSING 판정을 리포트 상단에 표시. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |
| **✅ 완료** | **Code Quality Fix-First**: Step 5.5로 누락된 에러 처리, 타입 불일치, 미사용 import 등을 AUTO-FIX(즉시 수정) / 목록 기록(수정 불가) 분류. 스펙 레이어 verdict(APPROVE/REQUEST CHANGES/NEEDS DISCUSSION)는 유지. <!-- 추가됨: 2026-03-24, 완료됨: 2026-03-24 --> |

### discussion

| Aspect | Description |
|--------|-------------|
| **Purpose** | 구조화된 의사결정 토론 (맥락 수집 + 선택지 비교 + 결정/미결/실행항목 정리) |
| **Why** | 기술 선택, 아키텍처 결정 등 복잡한 의사결정을 구조화된 프로세스로 진행하여 결정의 품질과 추적 가능성을 높인다. |
| **Input** | 토픽, 코드베이스(선택) |
| **Output** | 토론 요약 (터미널 출력 또는 파일 저장) |
| **Source** | `.claude/skills/discussion/SKILL.md`, `.codex/skills/discussion/SKILL.md` |
| **제한** | 듀얼 플랫폼 지원. Claude Code는 `AskUserQuestion`, Codex는 `request_user_input` 기반 반복 토론 사용. discussion은 풀 스킬이므로 AskUserQuestion 유지 (에이전트 전환 대상 아님) |

### ralph-loop-init

| Aspect | Description |
|--------|-------------|
| **Purpose** | 장기 실행 프로세스(ML 트레이닝, e2e 테스트, 빌드 파이프라인, 통합 테스트 등)의 자동화 디버그 루프 디렉토리/파일 생성 |
| **Why** | 장기 실행 프로세스의 반복 디버그 루프를 표준화하여 일관된 실험/테스트 환경을 빠르게 구성한다. |
| **Input** | 프로젝트 코드, 대상 프로세스 스크립트 |
| **Output** | `ralph/` 디렉토리 (`config.sh`, `PROMPT.md`, `run.sh`, `state.md`, `CHECKS.md`) |
| **Source** | `.claude/agents/ralph-loop-init.md` (에이전트 정의, 전체 로직) |
|            | `.claude/skills/ralph-loop-init/SKILL.md` (래퍼) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |

### investigate

| Aspect | Description |
|--------|-------------|
| **Purpose** | 범용 체계적 디버깅 에이전트 (근본원인 우선, 단발성 문제 해결) |
| **Why** | 코드 문제 해결 시 체계적 프로세스 없이 임의 수정을 반복하면 근본원인을 놓치고 시간이 소모된다. 근본원인 우선(Iron Law), 3-strike 에스컬레이션, scope lock, blast radius gate, fresh verification, 독립 Agent 교차 검증을 포함하는 범용 디버깅 에이전트로 체계적 접근을 강제한다. |
| **Input** | 문제 설명, 코드베이스, 에러 로그/스택트레이스 |
| **Output** | Investigation Report (근본원인, 수정 내용, blast radius, 검증 결과, 범위 밖 발견사항) + 수정된 코드 |
| **Source** | `.claude/agents/investigate.md` (에이전트 정의, AC-First + self-contained) |
|            | `.claude/skills/investigate/SKILL.md` (래퍼) |
| **Process** | 6단계: Step 1 Problem Definition (증상/재현조건/기대동작 추출, scope lock 기준 확정) → Step 2 Evidence Collection (에러/스택트레이스/관련 코드/변경 이력 수집) → Step 3 Hypothesis & Cross-Verification (Agent A 가설 기반 + Agent B 독립 탐지 병렬 교차 검증, 단순 문제는 교차 검증 생략 가능) → Step 4 Blast Radius Assessment (변경 파일/의존 모듈/관련 테스트 나열) → Step 5 Fix & Verify (근본원인 수정 + 테스트 재실행 + 회귀 방지) → Step 6 Report |
| **Dependencies** | 없음 (독립 실행 가능) |
| **실행 형태** | 래퍼 → 에이전트 (Agent Wrapper 패턴) |
| **차별점** | ralph-loop-init과 차별화: investigate는 범용/단발 문제 해결, ralph-loop-init은 장시간 반복 프로세스 전용 |

### git

| Aspect | Description |
|--------|-------------|
| **Purpose** | staged/unstaged 변경 분석 → 의미 단위 커밋 자동 생성, 브랜치 관리, 리베이스 |
| **Why** | AI 에이전트가 생성한 다수의 변경사항을 Conventional Commits 규칙에 맞게 논리적으로 묶어 커밋하려면 전용 자동화가 필요하다. |
| **Input** | git 작업 트리 상태, 사용자 지시 |
| **Output** | 커밋, 브랜치, 리베이스 등 git 작업 수행 |
| **Source** | `.claude/skills/git/SKILL.md` |
| **제한** | Claude Code 전용 (Codex 미지원) |

### spec-snapshot

| Aspect | Description |
|--------|-------------|
| **Purpose** | 현재 스펙의 타임스탬프 스냅샷 생성 + 선택적 번역 |
| **Why** | 스펙의 특정 시점 상태를 보존하거나, 다국어 팀을 위해 번역본을 생성할 때 원본 스펙을 변경하지 않고 별도 스냅샷으로 관리한다. |
| **Input** | `_sdd/spec/` 현재 파일, 대상 언어 |
| **Output** | `_sdd/snapshots/<timestamp>_<lang>/` 디렉토리에 스냅샷 복사 |
| **Source** | `.claude/skills/spec-snapshot/SKILL.md` |

---

## Usage Guide & Expected Results

### Scenario 1: 새 프로젝트 스펙 생성 (처음 시작)

**Setup:**
```bash
# 프로젝트 디렉토리에서 SDD Skills 플러그인 설치
/plugin marketplace add malfo-y/sdd-skills
/plugin install sdd-skills@sdd-skills
```

**Action:**
```bash
/spec-create
```

**Expected Result:**
- `_sdd/spec/<project>.md` 생성 — 프로젝트 코드를 분석하여 §1~§8 구조의 스펙 문서 자동 생성
- `_sdd/env.md` 생성 — 환경 설정/실행 방법 가이드
- `CLAUDE.md` 생성 또는 업데이트 — 워크스페이스 안내에 `_sdd/` 경로 추가
- 사용자에게 요약 테이블 제시 후 전체 스펙 출력

### Scenario 2: 대규모 기능 추가 (수동 Full SDD Workflow)

**Action:**
```bash
/feature-draft           # Part 1: 스펙 패치 초안 + Part 2: 구현 계획
/spec-update-todo        # 스펙에 새 기능 반영
/implementation-plan     # Phase별 구현 계획 수립
/implementation          # TDD 기반 코드 작성
/implementation-review   # 계획 대비 검증
/spec-update-done        # 코드 변경사항을 스펙에 동기화
```

**Expected Result:**
- `_sdd/drafts/feature_draft_<name>.md` — 스펙 패치 초안 + 구현 태스크 리스트
- `_sdd/spec/<project>.md` 업데이트 — 새 기능 반영
- `_sdd/implementation/IMPLEMENTATION_PLAN.md` — Target Files 기반 병렬 실행 계획
- 구현 완료 후 스펙과 코드 간 드리프트 0 상태

### Scenario 2b: 대규모 기능 추가 (sdd-autopilot 자동 실행)

**Action:**
```bash
/sdd-autopilot "인증 시스템 구현 — JWT 기반, 로그인/로그아웃/토큰 갱신"
```

**Expected Result:**
- Phase 1: sdd-autopilot이 SDD reference를 로딩하고, 인라인 discussion으로 요구사항을 구체화하고, 코드베이스를 탐색한 뒤, reasoning 기반으로 오케스트레이터를 생성하고 구조/철학 12항목을 자동 검증
- Phase 1.5: 검증된 오케스트레이터 + Pre-flight Check 결과를 사용자에게 제시 → 확인 후 실행
- Phase 2: feature-draft → implementation-plan → implementation → implementation-review (review-fix loop, **필수 사이클** -- Hard Rule #9에 따라 이슈 발견 시 fix → re-review 반드시 실행) → 인라인 테스트 → spec-update-done을 자율 실행
- `.claude/skills/orchestrator_auth_system/SKILL.md` 또는 `.codex/skills/orchestrator_auth_system/SKILL.md` — 실행 중 활성 오케스트레이터 (스킬로 재사용/재개 가능)
- `_sdd/pipeline/log_auth_system_<ts>.md` — 파이프라인 실행 로그 (Meta + Status 테이블 + 각 에이전트 시작/완료, 결정사항, 에러)
- `_sdd/pipeline/orchestrators/auth_system_<ts>/` — 완료된 오케스트레이터 아카이브
- 구현 완료 + 스펙 동기화 완료

### Scenario 3: PR 기반 스펙 동기화

**Action:**
```bash
/pr-spec-patch           # PR 변경사항과 스펙 비교, 패치 초안 생성
/pr-review               # 스펙 대비 PR 검증 → APPROVE / REQUEST CHANGES
```

**Expected Result:**
- `_sdd/pr/spec_patch_draft.md` — PR이 스펙에 미치는 영향 분석
- `_sdd/pr/PR_REVIEW.md` — 스펙 준수 여부 판정 + 구체적 피드백

### Scenario 4: 스펙 현황 파악 및 의사결정

**Action:**
```bash
/spec-summary            # 현재 프로젝트 상태 요약
/discussion              # 기술 선택, 아키텍처 결정 등 구조화된 토론
```

**Expected Result:**
- `_sdd/spec/SUMMARY.md` — Executive Summary + 기능 대시보드 + 권장 다음 단계
- 토론 결과 — 결정사항/미결/실행항목 정리 (최대 10라운드)

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
│   ├── agents/                  # 에이전트 정의 (10개)
│   │   ├── feature-draft.md
│   │   ├── implementation-plan.md
│   │   ├── implementation.md
│   │   ├── implementation-review.md
│   │   ├── ralph-loop-init.md
│   │   ├── investigate.md
│   │   ├── spec-review.md
│   │   ├── spec-update-done.md
│   │   ├── spec-update-todo.md
│   │   └── write-phased.md
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
│       ├── pr-spec-patch/
│       ├── ralph-loop-init/     # [래퍼] → agents/ralph-loop-init.md (references/ 삭제)
│       ├── spec-create/
│       ├── spec-review/         # [래퍼] → agents/spec-review.md (references/ 삭제)
│       ├── spec-rewrite/
│       ├── spec-snapshot/
│       ├── spec-summary/
│       ├── spec-update-done/    # [래퍼] → agents/spec-update-done.md (references/ 삭제)
│       ├── spec-update-todo/    # [래퍼] → agents/spec-update-todo.md (references/ 삭제)
│       ├── spec-upgrade/
│       └── write-phased/        # [래퍼] → agents/write-phased.md (references/ 삭제)
│
├── .codex/
│   ├── config.toml              # Codex custom agent 실행 설정
│   ├── agents/                  # Codex custom agent 정의 (10개)
│   │   ├── feature-draft.toml
│   │   ├── implementation-plan.toml
│   │   ├── implementation.toml
│   │   ├── implementation-review.toml
│   │   ├── investigate.toml
│   │   ├── ralph-loop-init.toml
│   │   ├── spec-review.toml
│   │   ├── spec-update-done.toml
│   │   ├── spec-update-todo.toml
│   │   └── write-phased.toml
│   └── skills/                  # Codex 스킬 (20개, git 제외)
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
    │   └── main.md              # 이 스펙 문서
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
| 스킬 수 | 21개 (래퍼 9 + 풀 11 + 메타 1) | 20개 (wrapper/direct 18 + utility 1 + 메타 1) |
| 에이전트 수 | 10개 | 10개 |
| AskUserQuestion | 풀 스킬에서만 사용 (에이전트는 non-interactive) | `request_user_input` 기반 대화형 처리 |
| Agent tool | 지원 (서브에이전트 호출) | 지원 (custom agent spawn) |
| SKILL.md 차이 | 래퍼 또는 풀 | wrapper/direct skill + custom agent + generated orchestration skill |
| sdd-autopilot | 지원 | 지원 |

**Codex 제한 사항:**
- `AskUserQuestion` 도구 미지원 → `request_user_input` 기반으로 대화형 단계를 처리
- nested `write_phased`를 쓰는 파이프라인은 `.codex/config.toml`의 `agents.max_depth >= 2`가 필요하다
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

### 해결 완료 ✅

1. ~~**implementation 스킬 예시 Step 번호 불일치**~~ (v1.0.1 해결)
   - 예시를 SKILL.md 7단계 (Step 1~7) 구조에 맞게 재구성, Step 2 신규 추가

2. ~~**spec-update-done 참조 파일 불완전**~~ (v1.0.1 해결)
   - drift-patterns.md에 env.md 드리프트 (Section 7) + DECISION_LOG.md 드리프트 (Section 8) 추가

3. ~~**pr-review Mode 2 (Degraded) 예시 부재**~~ (v1.0.1 해결)
   - sample-review.md에 Mode 2 (Degraded) 시나리오 예시 추가

4. ~~**일부 참조 파일 언어 불일치**~~ (v1.0.1 해결)
   - implementation, pr-review, spec-review의 review-checklist.md에 bilingual 헤더 적용

### 중간 우선순위 🟡

5. **Codex 스킬 동기화 수동 프로세스**
   - 현황: `.claude/skills/`를 수정하면 `.codex/skills/`도 수동으로 동기화 필요
   - 제안: 동기화 스크립트 작성 또는 빌드 프로세스 도입

6. **스킬 버전 관리 미흡**
   - 현황: v3.6 리팩토링으로 다수 skill.json이 갱신되었으나, 일부 여전히 고정
   - 제안: SKILL.md 변경 시 semver 업데이트 규칙 정립

### 해결 완료 ✅ (gstack patterns, v3.7.0)

8. ~~**Verification Gate Iron Rule**~~ (v3.7.0 해결): implementation, implementation-review에 "should work" 금지, 코드 변경 후 테스트 재실행 필수, 이전 결과 재사용 금지를 Hard Rule로 추가

9. ~~**Regression Iron Rule**~~ (v3.7.0 해결): implementation에 기존 테스트 실패 시 테스트 업데이트 + 회귀 방지 테스트 추가를 필수 단계로 강제

10. ~~**Audit Trail + Taste Decision**~~ (v3.7.0 해결): sdd-autopilot Step 7.2에서 모든 자동 결정을 로그에 기록, Taste Decision을 Step 8 보고서에 표면화

11. ~~**Failure Modes 테이블 in Feature Draft**~~ (v3.7.0 해결): feature-draft Part 1에 경량 Failure Modes 테이블 섹션을 항상 포함

12. ~~**Test Coverage Mapping in Implementation Plan**~~ (v3.7.0 해결): [M] 마커 대상 파일의 기존 테스트 커버리지를 매핑

13. ~~**Scope Drift Detection in PR Review**~~ (v3.7.0 해결): PR diff 변경 파일 vs 스펙 패치 초안 범위 비교, CLEAN/DRIFT/MISSING 판정

14. ~~**Code Quality Fix-First in PR Review**~~ (v3.7.0 해결): 누락된 에러 처리, 타입 불일치, 미사용 import 등을 AUTO-FIX/목록 기록 분류

15. ~~**Code Analysis Metrics in Spec Review**~~ (v3.7.0 해결): 핫스팟, Focus Score, Test Coverage 지표를 Step 3.5에 추가

16. ~~**investigate 스킬**~~ (v3.7.0 해결): 범용 체계적 디버깅 에이전트(`.claude/agents/investigate.md`) + 래퍼 스킬(`.claude/skills/investigate/SKILL.md`) 생성 완료. 근본원인 우선, 3-strike, scope lock, blast radius gate, fresh verification, 독립 Agent 교차 검증 포함

### 낮은 우선순위 🟢

7. **docs/sdd.md가 독립 개념서**
   - 현황: SDD 개념 설명 문서이나 스킬과 직접 연결되지 않음
   - 제안: docs/SDD_WORKFLOW.md에서 참조 링크 추가

---

## Appendix: Code Reference Index

이 프로젝트의 "코드"는 SKILL.md와 에이전트 정의 파일이다.

### 풀 스킬 (SKILL.md에 전체 로직)

| File | Skill | Referenced In |
|------|-------|---------------|
| `.claude/skills/sdd-autopilot/SKILL.md` | sdd-autopilot | Core Design, Component Details, Workflow |
| `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` | sdd-autopilot (reference) | Component Details (SDD 철학 + 스킬 카탈로그) |
| `.claude/skills/spec-create/SKILL.md` | spec-create | Core Design, Component Details |
| `.claude/skills/spec-rewrite/SKILL.md` | spec-rewrite | Component Details |
| `.claude/skills/spec-summary/SKILL.md` | spec-summary | Component Details |
| `.claude/skills/spec-upgrade/SKILL.md` | spec-upgrade | Component Details |
| `.claude/skills/guide-create/SKILL.md` | guide-create | Component Details |
| `.claude/skills/pr-spec-patch/SKILL.md` | pr-spec-patch | Component Details |
| `.claude/skills/pr-review/SKILL.md` | pr-review | Component Details |
| `.claude/skills/discussion/SKILL.md` | discussion | Component Details |
| `.claude/skills/git/SKILL.md` | git | Component Details |
| `.claude/skills/spec-snapshot/SKILL.md` | spec-snapshot | Component Details |

### 래퍼 스킬 + 에이전트 정의

> v3.6: 모든 래퍼 스킬의 `references/`, `examples/` 디렉토리가 삭제됨. 에이전트가 self-contained로 핵심 내용을 인라인 포함.

| Wrapper (SKILL.md) | Agent Definition | Skill | Referenced In |
|--------------------|------------------|-------|---------------|
| `.claude/skills/feature-draft/SKILL.md` | `.claude/agents/feature-draft.md` | feature-draft | Core Design, Component Details |
| `.claude/skills/implementation-plan/SKILL.md` | `.claude/agents/implementation-plan.md` | implementation-plan | Component Details |
| `.claude/skills/implementation/SKILL.md` | `.claude/agents/implementation.md` | implementation | Component Details |
| `.claude/skills/implementation-review/SKILL.md` | `.claude/agents/implementation-review.md` | implementation-review | Component Details |
| `.claude/skills/ralph-loop-init/SKILL.md` | `.claude/agents/ralph-loop-init.md` | ralph-loop-init | Component Details |
| `.claude/skills/spec-review/SKILL.md` | `.claude/agents/spec-review.md` | spec-review | Component Details |
| `.claude/skills/spec-update-done/SKILL.md` | `.claude/agents/spec-update-done.md` | spec-update-done | Component Details |
| `.claude/skills/spec-update-todo/SKILL.md` | `.claude/agents/spec-update-todo.md` | spec-update-todo | Component Details |
| `.claude/skills/investigate/SKILL.md` | `.claude/agents/investigate.md` | investigate | Component Details |

### 유틸리티 에이전트

| File | Agent | Referenced In |
|------|-------|---------------|
| `.claude/agents/write-phased.md` | write-phased | Component Details |

### Changelog

#### v3.7.0 (2026-03-24)

- **gstack Patterns 구현 완료 (spec-update-done)**: v3.6.1에서 계획(📋)으로 반영된 9개 결정 사항이 모두 구현되어 완료(✅)로 갱신
- **investigate 스킬 구현 완료**: `.claude/agents/investigate.md` (AC-First + self-contained, 6단계 프로세스) + `.claude/skills/investigate/SKILL.md` (래퍼) 생성. 근본원인 우선(Iron Law), 3-strike 에스컬레이션, scope lock, blast radius gate, fresh verification, Agent A/B 교차 검증 포함
- **기존 스킬 기능 구현 완료** (8개):
  - implementation: Verification Gate Iron Rule + Regression Iron Rule (Hard Rules 추가)
  - implementation-review: Fresh Verification (Hard Rule #8 추가)
  - feature-draft: Failure Modes 테이블 (Part 1 템플릿에 섹션 추가)
  - implementation-plan: Test Coverage Mapping (Step 3 뒤 조건부 하위 단계)
  - pr-review: Scope Drift Detection (Step 2.5) + Code Quality Fix-First (Step 5.5)
  - spec-review: Code Analysis Metrics (Step 3.5 + Output Format 지표 테이블)
  - sdd-autopilot: Audit Trail (Step 7.2) + Taste Decision (Step 8.2)
- **Mirror Notice 동기화 완료**: 5개 래퍼 스킬(implementation, implementation-review, feature-draft, implementation-plan, spec-review)의 SKILL.md에 에이전트 변경사항 반영
- **Identified Issues 8-16번 해결 완료로 이동**
- **investigate Component Details 상세 업데이트**: 실제 구현(6단계 프로세스, Agent A/B 교차 검증, Investigation Report 출력 형식)에 맞게 반영
- 백업: `_sdd/spec/prev/PREV_main_20260324_180000.md`
- 입력: `_sdd/implementation/IMPLEMENTATION_PLAN.md`, `_sdd/implementation/IMPLEMENTATION_REPORT.md`, `_sdd/drafts/feature_draft_gstack_patterns.md`

#### v3.6.1 (2026-03-24)

- **gstack Patterns 스펙 사전 반영 (spec-update-todo)**: feature_draft_gstack_patterns.md Part 1의 9개 결정 사항을 계획(📋) 상태로 스펙에 반영
- **신규 스킬 계획**: investigate (범용 체계적 디버깅 에이전트 + 래퍼 스킬) -- Component Details, Category Overview, Agent 목록, Directory Structure, Code Reference Index에 추가
- **기존 스킬 계획된 기능 추가** (9개):
  - sdd-autopilot: Audit Trail + Taste Decision (P1-High)
  - feature-draft: Failure Modes 테이블 (P2-Medium)
  - implementation-plan: Test Coverage Mapping (P2-Medium)
  - implementation: Verification Gate Iron Rule (P1-High), Regression Iron Rule (P2-Medium)
  - implementation-review: Fresh Verification (P1-High)
  - pr-review: Scope Drift Detection (P2-Medium), Code Quality Fix-First (P1-High)
  - spec-review: Code Analysis Metrics (P3-Low)
- **Identified Issues 섹션에 계획됨 목록 추가**: 8-16번 항목 (gstack patterns 전체)
- 백업: `_sdd/spec/prev/PREV_main_20260324_120000.md`
- 입력: `_sdd/drafts/feature_draft_gstack_patterns.md` (Part 1)

#### v3.6.0 (2026-03-20)

- **AC-First + Self-Contained 전면 리팩토링**: 모든 9개 Claude agent + 11개 Claude full skill + 9개 Codex agent + 10개 Codex full skill을 AC-First 구조로 전면 재작성
  - Agent: AC 섹션 + 자체 검증 지시 + Final Check 추가, 핵심 reference 인라인 (self-contained)
  - Full Skill: AC 섹션 + 자체 검증 지시 + Final Check 추가, Best Practices/Context Management/When to Use 등 공통 bloat 제거
  - Claude agent: 4,365줄 -> 1,961줄 (55% 감축), Full skill: 5,042줄 -> 2,718줄 (46% 감축)
- **래퍼 스킬 references/examples 삭제**: Claude 9개 + Codex 8개 wrapper skill에서 미사용 references/examples 총 48개 파일 삭제
- **신규 디자인 패턴 2개**: AC-First 패턴 (AC + 자체 검증 + Final Check), Self-Contained 패턴 (핵심 reference 인라인)
- **ralph-loop-init 범용화**: "ML 트레이닝 디버그 루프" -> "장기 실행 프로세스(ML, e2e, 빌드 등) 자동화 디버그 루프"
- **SDD workflow 세부 변경**: implementation-plan Target Files 충돌 규칙 수정 (동일 파일 참조 시 마커 종류 무관하게 충돌), spec-update-todo 새 항목 기본 상태 마커 📋 명시, implementation-plan/implementation-review 리팩토링 메타 AC 삭제
- **Codex Smoke Check/Final Check 통일**: 기존 Final Smoke Check 제거, Final Check으로 통일
- **sdd-upgrade 스킬 제거 반영**: 이전에 삭제된 `sdd-upgrade` 스킬의 잔존 스펙 참조 정리 (21개 -> 20개 스킬)
- 백업: `_sdd/spec/prev/PREV_main_20260320_120000.md`
- 드래프트: `_sdd/drafts/feature_draft_agent_self_containment.md`, `feature_draft_agent_self_containment_phase2.md`, `feature_draft_full_skills_ac_first.md`

#### v3.5.0 (2026-03-19)

- **sdd-autopilot v2.0.0 reasoning 리라이트**: 규모별 템플릿 매칭에서 SDD 철학 기반 reasoning + 동적 파이프라인 구성으로 전면 교체
- **Reference 파일 교체**: `references/pipeline-templates.md`, `references/scale-assessment.md` 삭제 -> `references/sdd-reasoning-reference.md` 신규 생성 (SDD 철학 + 스킬 카탈로그를 ~310줄로 압축)
- **Step 구조 변경**: Step 1(Reference Loading), Step 4(Reasoning -> Orchestrator Generation), Step 5(Orchestrator Verification) 신규 추가
- **Hard Rule #10 추가**: Execute -> Verify 필수 -- 모든 파이프라인 단계에 실행 + 검증 두 페이즈 필수
- **비오케스트레이션 스킬 재분류**: spec-create, discussion, guide-create를 autopilot 오케스트레이터 파이프라인에 넣지 않는 스킬로 명시
- **Orchestrator Template에 Reasoning Trace 섹션 추가**: 스킬 선택 근거, 순서 결정, 적용된 SDD 원칙을 기록
- **Dependencies 변경**: "스펙 없어도 실행 가능" -> "글로벌 스펙 존재 필수, 없으면 /spec-create 안내"
- **Codex 동기화**: `.codex/skills/sdd-autopilot/SKILL.md` (v2.0.1)도 동일 reasoning 아키텍처로 동기화 (Codex 차이점 보존)
- **변경**: 2-Phase Orchestration 패턴, sdd-autopilot Component Details, Design Rationale, Success Criteria, Scenario 2b, Code Reference Index 업데이트
- 백업: `_sdd/spec/prev/PREV_main_20260319_120000.md`
- 토론: `_sdd/discussion/discussion_autopilot_reasoning_harness.md`

#### v3.4.1 (2026-03-17)

- **Codex autopilot parity 복원**: `.codex/skills/sdd-autopilot/`의 main skill, pipeline templates, scale assessment, sample orchestrator에 Claude 기준 실행 계약 복원
- **autopilot report artifact 명시**: `_sdd/pipeline/report_<topic>_<ts>.md`를 Artifact Map과 sdd-autopilot output contract에 반영
- **validation guide 통합**: 별도 `docs/CODEX_AGENT_VALIDATION.md` 대신 `docs/AUTOPILOT_GUIDE.md`의 "Codex 검증 체크리스트" 섹션을 운영 기준으로 사용
- **스펙 드리프트 수정**: Codex wrapper -> custom agent 실행 모델 설명과 상단 버전/산출물 설명을 최신 구조와 일치시킴

#### v3.4.0 (2026-03-17)

- **Codex custom agent backbone 도입**: `.codex/agents/`에 9개 custom agent 정의 추가 (feature_draft, implementation_plan, implementation, implementation_review, spec_update_todo, spec_update_done, spec_review, ralph_loop_init, write_phased)
- **Codex wrapper parity 강화**: 핵심 pipeline skill을 user entry wrapper로 명시하고, generated orchestrator가 custom agents를 직접 spawn하도록 모델 전환
- **nested write-phased parity**: `feature_draft`, `implementation_plan`, `implementation_review`, `spec_review`가 장문 산출물 생성 시 `write_phased`를 nested 사용하도록 구조 반영
- **Pre-flight 확장**: `_sdd/env.md`와 `.codex/config.toml`을 함께 읽어 `agents.max_depth`, `agents.max_threads` 등 실행 가능성을 점검
- **문서 갱신**: Platform Differences, Architecture Overview, AUTOPILOT_GUIDE, QUICK_START, WORKFLOW를 custom agent spawn 모델 기준으로 갱신
- 백업: 없음 (문서/구조 정렬)

#### v3.3.0 (2026-03-17)

- **Hard Rule #9 (Review-Fix 사이클 필수) 반영**: sdd-autopilot에 추가된 Hard Rule #9을 스펙에 반영 -- review 포함 파이프라인에서 review → fix → re-review 사이클 필수, 리뷰만 하고 끝나는 것 불허
- **implementation-review 단계 재분류**: "비핵심 단계"에서 "조건부 핵심 단계"로 승격 (review 포함 파이프라인에서는 핵심 단계로 취급, 실패 시 건너뛸 수 없음)
- **변경**: Common Hard Rules에 sdd-autopilot 전용 Hard Rule #9 추가, 2-Phase Orchestration 패턴 설명 보강, sdd-autopilot Process 필드 업데이트, Scenario 2b 설명 보강
- 백업: `_sdd/spec/prev/PREV_main_20260317_180000.md`

#### v3.2.0 (2026-03-17)

- **sdd-autopilot 재개/부분 실행**: Step 0 (Pipeline State Detection) 추가 -- 기존 미완료 파이프라인 감지 및 재개/새로 시작 선택 지원
- **산출물 스캔 및 시작점/종료점 감지**: Step 1.4 추가 -- 사용자 요청에서 시작/종료 힌트 파싱, `_sdd/` 기존 산출물 관련성 판단으로 파이프라인 범위 조절
- **Pipeline Log Format 강화**: Meta 섹션(request, orchestrator 참조, scale, started, pipeline) + Status 테이블(5개 상태값: pending/in_progress/completed/failed/skipped) 추가
- **오케스트레이터 저장 위치 변경**: `_sdd/pipeline/` -> `.claude/skills/orchestrator_<topic>/SKILL.md` (재사용성 + 재개 기능 위해)
- **변경**: Artifact Map, Data Flow, Scenario 2b, Directory Structure 등 오케스트레이터 경로 일괄 업데이트
- 백업: `_sdd/spec/prev/PREV_main_20260317_150000.md`

#### v3.1.0 (2026-03-17)

- **에이전트 non-interactive 전환**: 8개 파이프라인 에이전트에서 AskUserQuestion 완전 제거, Autonomous Decision-Making 패턴으로 대체
- **신규 디자인 패턴**: Autonomous Decision-Making 패턴 추가 (Core Design > Design Patterns)
- **변경**: 에이전트가 모호한 상황에서 자율 판단 후 근거를 출력에 기록하고, 추론 불가 항목은 Open Questions에 기록
- **변경**: marketplace.json에 sdd-autopilot 스킬 1개 + 에이전트 8개 등록
- **변경**: 스킬 디렉토리명 `autopilot` -> `sdd-autopilot` 리네임
- **변경**: Platform Differences 테이블에서 AskUserQuestion이 풀 스킬에서만 사용됨을 명시
- 백업: `_sdd/spec/prev/PREV_main_20260317_120000.md`

#### v3.0.0 (2026-03-16)

- **아키텍처 변경**: 스킬 전용 → 스킬 + 에이전트 이중 아키텍처(dual architecture) 전환
- **신규**: sdd-autopilot 적응형 오케스트레이터 메타스킬 추가 (`.claude/skills/sdd-autopilot/`)
- **신규**: 8개 에이전트 정의 파일 생성 (`.claude/agents/`)
- **변경**: 8개 스킬을 Agent Wrapper 래퍼로 전환 (feature-draft, implementation-plan, implementation, implementation-review, ralph-loop-init, spec-review, spec-update-done, spec-update-todo)
- **신규**: `_sdd/pipeline/` 오케스트레이터 + 파이프라인 로그 시스템 설계
- **신규**: `docs/AUTOPILOT_GUIDE.md` sdd-autopilot 사용 가이드 추가
- **신규**: `_sdd/env.md`에 SDD-Autopilot Resources 섹션 추가
- **신규 디자인 패턴**: Agent Wrapper 패턴, 2-Phase Orchestration 패턴 추가
- 스킬 수: 19 → 20 (sdd-autopilot 추가), 에이전트 수: 1 → 9 (8개 파이프라인 에이전트 + write-phased)
- 백업: `_sdd/spec/prev/PREV_main_20260316_120000.md`

#### v2.1.0 (2026-03-13)

- spec-create, spec-rewrite, spec-upgrade에 2-Phase Generation 패턴 추가
- 3개 미문서 스킬 추가 (spec-snapshot, guide-create, write-phased)
- Platform primary target을 `.claude/skills/`로 재설정
