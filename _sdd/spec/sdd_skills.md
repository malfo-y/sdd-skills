# SDD Skills

**버전**: 1.0.1
**최종 업데이트**: 2026-03-06

---

## 목표 (Goal)

### 주요 목적

Claude Code와 Codex에서 **Spec-Driven Development(SDD) 워크플로우**를 실행하기 위한 스킬 모음을 제공한다. 스펙 문서를 Single Source of Truth로 삼아 요구사항 정의 → 구현 → 검증 → 유지보수 전 과정을 AI 에이전트가 체계적으로 수행할 수 있도록 한다.

### 핵심 기능

- **14개 스킬**: 스펙 생성부터 PR 리뷰까지 소프트웨어 개발 생명주기 전체를 커버
- **듀얼 플랫폼**: Claude Code (`.claude/skills/`) + Codex (`.codex/skills/`) 동시 지원
- **Plugin 배포**: Claude Code Plugin Marketplace를 통한 원클릭 설치
- **규모별 워크플로우**: 대규모(6단계) / 중규모(3단계) / 소규모(1단계) 분리

### 대상 사용자

- AI 에이전트(Claude Code, Codex)를 활용하여 소프트웨어를 개발하는 개발자
- 스펙 기반으로 체계적인 AI 코딩 워크플로우를 구축하려는 팀

### 성공 기준

- 모든 14개 스킬이 Claude Code에서 `/스킬명`으로 정상 호출 및 실행
- Codex에서 13개 스킬(discussion 제외)이 정상 동작
- 스킬 간 워크플로우 연결이 끊김 없이 동작 (e.g., spec-create → feature-draft → implementation)

---

## 아키텍처 개요 (Architecture Overview)

### 시스템 구조

```
사용자 ──→ Claude Code / Codex
              │
              ├── Skill Loader (SKILL.md 파싱)
              │     ├── .claude/skills/  (Claude Code용)
              │     └── .codex/skills/   (Codex용)
              │
              └── SDD Workflow Engine
                    ├── 스펙 관리 스킬 (Create / Review / Rewrite / Summary / Update)
                    ├── 구현 스킬 (Plan / Implement / Review)
                    ├── PR 스킬 (Patch / Review)
                    └── 보조 스킬 (Discussion / Ralph Loop)
```

### 스킬 로딩 구조

각 스킬은 독립적인 디렉토리로 구성되며, 플랫폼(Claude Code / Codex)이 `SKILL.md`를 컨텍스트에 로드하여 실행한다.

```
<skill-name>/
├── SKILL.md          # 메인 프롬프트 (스킬 정의, 프로세스, 규칙)
├── skill.json        # 메타데이터 (이름, 설명, 버전)
├── references/       # 보조 참조 문서 (체크리스트, 포맷 명세 등)
│   ├── *.md
│   └── ...
└── examples/         # 실행 예시 (세션, 출력물 샘플)
    ├── *.md
    └── ...
```

### 데이터 흐름

```
[사용자 요청]
    │
    ▼
[Skill Dispatch] ─── skill.json의 description으로 매칭
    │
    ▼
[SKILL.md 로드] ─── 프로세스 Step 순서대로 실행
    │                ├── references/*.md 참조 (필요 시)
    │                └── examples/*.md 참조 (포맷 가이드)
    │
    ▼
[_sdd/ 아티팩트 생성/수정]
    ├── _sdd/spec/          (스펙 문서)
    ├── _sdd/drafts/        (피처 드래프트)
    ├── _sdd/implementation/ (구현 계획/리포트)
    └── _sdd/pr/            (PR 리뷰/패치)
```

### 기술 스택

- **스킬 정의 형식**: Markdown (SKILL.md)
- **메타데이터**: JSON (skill.json)
- **배포**: Claude Code Plugin Marketplace, Codex LobeHub / 수동 복사
- **실행 환경**: Claude Code CLI, Codex CLI

---

## 컴포넌트 상세 (Component Details)

### 스킬 카테고리 분류

| 카테고리 | 스킬 | 역할 |
|----------|------|------|
| **스펙 생성/관리** | spec-create | 코드 분석 또는 초안에서 스펙 문서 생성 |
| | spec-review | 스펙 품질 및 코드-스펙 드리프트 검증 (read-only) |
| | spec-rewrite | 과도하게 긴/복잡한 스펙 구조 재정리 |
| | spec-summary | 스펙 요약본 생성 (현황 파악, 온보딩용) |
| | spec-update-todo | 새 기능/요구사항을 스펙에 사전 반영 |
| | spec-update-done | 구현 완료 후 코드와 스펙 동기화 |
| **구현** | feature-draft | 스펙 패치 초안 + 구현 계획을 한 번에 생성 |
| | implementation-plan | Phase별 구현 계획 수립 (Target Files 포함) |
| | implementation | TDD 기반 병렬 구현 실행 |
| | implementation-review | 계획 대비 구현 진행 검증 |
| **PR 프로세스** | pr-spec-patch | PR과 스펙 비교하여 패치 초안 생성 |
| | pr-review | PR을 스펙/패치 초안 대비 검증 및 판정 |
| **보조** | discussion | 구조화된 의사결정 토론 (Claude Code 전용) |
| | ralph-loop-init | ML 자동 트레이닝 디버그 루프 생성 |

### 각 스킬 상세

#### spec-create

| 측면 | 설명 |
|------|------|
| **목적** | 프로젝트 코드 분석 또는 사용자 초안을 기반으로 SDD 스펙 문서 생성 |
| **입력** | 프로젝트 코드베이스, user_draft.md, 사용자 대화 |
| **출력** | `_sdd/spec/<project>.md`, CLAUDE.md, AGENTS.md, _sdd/env.md (부트스트랩) |
| **프로세스** | 3단계 (정보 수집 → 분석 → 작성) |
| **의존** | 없음 (워크플로우 시작점) |

#### feature-draft

| 측면 | 설명 |
|------|------|
| **목적** | 요구사항 수집 → 스펙 패치 초안(Part 1) + 구현 계획(Part 2)을 단일 파일로 생성 |
| **입력** | 기존 스펙, 사용자 요구사항, 코드베이스 |
| **출력** | `_sdd/drafts/feature_draft_<name>.md` |
| **프로세스** | 7단계 (입력 분석 → 맥락 수집 → 질문 → 설계 → Part 1 → Part 2 → 저장) |
| **의존** | spec-create (스펙이 있어야 Part 1 생성 가능) |
| **특징** | spec-update-todo 호환 마커, Target Files 기반 병렬 실행 지원 |

#### spec-update-todo

| 측면 | 설명 |
|------|------|
| **목적** | 새 기능/요구사항을 스펙에 사전 반영 (구현 전 드리프트 방지) |
| **입력** | user_spec.md 또는 feature-draft Part 1 |
| **출력** | 스펙 파일 직접 수정 + 변경 요약 리포트 |
| **의존** | spec-create (스펙 존재 필수) |

#### spec-update-done

| 측면 | 설명 |
|------|------|
| **목적** | 구현 완료 후 코드 변경사항을 스펙에 반영 |
| **입력** | 구현 리포트, 코드 diff, 기존 스펙 |
| **출력** | 스펙 파일 업데이트 + 아카이브 |
| **의존** | implementation 완료 후 실행 |

#### spec-review

| 측면 | 설명 |
|------|------|
| **목적** | 스펙 품질 검증 + 코드-스펙 드리프트 감지 (read-only) |
| **입력** | 스펙 파일, 코드베이스 |
| **출력** | `_sdd/spec/SPEC_REVIEW_REPORT.md` |
| **특징** | SPEC_OK / SYNC_REQUIRED / NEEDS_DISCUSSION 3단계 판정 |

#### spec-rewrite

| 측면 | 설명 |
|------|------|
| **목적** | 과도하게 긴/복잡한 스펙을 구조 재정리 (파일 분할, 부록 이동) |
| **입력** | 기존 스펙 파일 |
| **출력** | 재구성된 스펙 파일 + `REWRITE_REPORT.md` |

#### spec-summary

| 측면 | 설명 |
|------|------|
| **목적** | 스펙의 인간 친화적 요약본 생성 |
| **입력** | 스펙 파일, 구현 진행 현황 |
| **출력** | `_sdd/spec/SUMMARY.md`, 선택적 README 블록 |

#### implementation-plan

| 측면 | 설명 |
|------|------|
| **목적** | 대규모 구현을 위한 Phase별 구현 계획 수립 |
| **입력** | 스펙, feature-draft Part 2, 코드베이스 |
| **출력** | `_sdd/implementation/IMPLEMENTATION_PLAN.md` |
| **특징** | Target Files 기반 병렬 실행 분석, 파일 충돌 감지 |

#### implementation

| 측면 | 설명 |
|------|------|
| **목적** | 구현 계획에 따른 TDD 기반 코드 작성 실행 |
| **입력** | 구현 계획, 코드베이스 |
| **출력** | 구현된 코드 + `IMPLEMENTATION_REPORT.md` |
| **특징** | Target Files 기반 병렬 Agent 실행, Phase별 진행 |

#### implementation-review

| 측면 | 설명 |
|------|------|
| **목적** | 구현 계획 대비 실제 구현 진행 검증 |
| **입력** | 구현 계획, 구현 리포트, 코드 |
| **출력** | 검증 리포트 + 다음 단계 제안 |

#### pr-spec-patch

| 측면 | 설명 |
|------|------|
| **목적** | PR 변경사항과 스펙을 비교하여 패치 초안 생성 |
| **입력** | PR 번호 (gh CLI), 스펙 파일 |
| **출력** | `_sdd/pr/spec_patch_draft.md` |

#### pr-review

| 측면 | 설명 |
|------|------|
| **목적** | PR 구현을 스펙 및 패치 초안 대비 검증하여 APPROVE/REQUEST CHANGES 판정 |
| **입력** | PR 번호, 스펙, spec_patch_draft.md |
| **출력** | `_sdd/pr/PR_REVIEW.md` |

#### discussion

| 측면 | 설명 |
|------|------|
| **목적** | 구조화된 의사결정 토론 (맥락 수집 + 선택지 비교 + 결정/미결/실행항목 정리) |
| **입력** | 토픽, 코드베이스(선택) |
| **출력** | 토론 요약 (터미널 출력 또는 파일 저장) |
| **특징** | Claude Code 전용 (AskUserQuestion 기반 반복 토론) |
| **제한** | 최대 10라운드 |

#### ralph-loop-init

| 측면 | 설명 |
|------|------|
| **목적** | ML 트레이닝 디버그를 위한 자동화 루프 디렉토리/파일 생성 |
| **입력** | 프로젝트 코드, 트레이닝 스크립트 |
| **출력** | `ralph/` 디렉토리 (config.sh, PROMPT.md, run.sh, state.md, CHECKS.md) |

---

## 워크플로우 (Workflow)

### 규모별 워크플로우

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

### PR 프로세스

```
PR 생성 → pr-spec-patch → pr-review → (merge 후) spec-update-done
```

### 스펙 유지보수

```
코드 변경 감지 → spec-review → (SYNC_REQUIRED 시) spec-update-done
스펙 복잡도 증가 → spec-rewrite
현황 파악 → spec-summary
```

---

## 디렉토리 구조 (Directory Structure)

```
sdd_skills/
├── README.md                    # 프로젝트 소개 + 설치 가이드
├── SDD_QUICK_START.md           # 빠른 참조 가이드
├── SDD_WORKFLOW.md              # 종합 워크플로우 가이드 (~992줄)
├── CLAUDE.md                    # Claude Code 워크스페이스 안내
│
├── .claude/
│   └── skills/                  # Claude Code 스킬 (14개)
│       ├── discussion/
│       ├── feature-draft/
│       ├── implementation/
│       ├── implementation-plan/
│       ├── implementation-review/
│       ├── pr-review/
│       ├── pr-spec-patch/
│       ├── ralph-loop-init/
│       ├── spec-create/
│       ├── spec-review/
│       ├── spec-rewrite/
│       ├── spec-summary/
│       ├── spec-update-done/
│       └── spec-update-todo/
│
├── .codex/
│   └── skills/                  # Codex 스킬 (13개, discussion 제외)
│       └── (위와 동일 구조)
│
├── .claude-plugin/              # Claude Code Plugin 설정
│
├── docs/
│   └── sdd.md                   # SDD 개념서 (~615줄)
│
├── scripts/
│   ├── generate_sdd_seminar_ppt.py
│   ├── generate_sdd_skills_keynote_60.py
│   └── sdd_seminar_ko.pptx
│
└── _sdd/
    ├── spec/
    │   └── sdd_skills.md        # 이 스펙 문서
    └── implementation/
        └── IMPLEMENTATION_PLAN.md  # feature-draft 스킬 구현 계획 (레거시)
```

---

## 플랫폼별 차이 (Platform Differences)

| 항목 | Claude Code | Codex |
|------|------------|-------|
| 스킬 경로 | `.claude/skills/` | `.codex/skills/` |
| 설치 방법 | Plugin Marketplace | LobeHub / 수동 복사 |
| 스킬 수 | 14개 | 13개 (discussion 제외) |
| AskUserQuestion | 지원 | 미지원 (사용자 입력이 필요한 단계는 대화로 대체) |
| Agent tool | 지원 (Explore, general-purpose) | 제한적 지원 |
| SKILL.md 차이 | 원본 | AskUserQuestion 관련 부분 대화 방식으로 변형 |

### Codex 제한 사항

- `AskUserQuestion` 도구 미지원 → SKILL.md에서 대화형 질문으로 변환
- `Agent` 도구 제한 → 병렬 Agent 실행 불가
- `discussion` 스킬은 AskUserQuestion 반복 루프에 의존하므로 Codex 미지원

---

## 스킬 설계 공통 패턴 (Common Skill Design Patterns)

### SKILL.md 공통 구조

```markdown
---
name: <skill-name>
description: <trigger description>
version: <semver>
---

# <Skill Title>

## Workflow Position       # 워크플로우 내 위치
## Hard Rules              # 절대 위반 불가 규칙
## Process (Step 1~N)      # 단계별 실행 프로세스
  - Decision Gates         # 단계 간 전환 조건
  - Tools                  # 각 단계에서 사용할 도구
## Output Format           # 출력 형식 정의
## Progressive Disclosure  # 사용자에게 요약 → 상세 순서로 제공
## Edge Cases / Errors     # 예외 처리
## Language Preference     # 언어 설정
```

### 공통 Hard Rules

1. **스펙 직접 수정 금지** (spec-update-todo, spec-update-done 제외): 대부분의 스킬은 스펙을 읽기 전용으로 참조
2. **_sdd/env.md 참조 필수**: 로컬 명령 실행 전 환경 설정 확인
3. **기존 파일 백업**: 덮어쓰기 전 `prev/PREV_<filename>_<timestamp>.md`로 아카이브
4. **한국어 기본**: 사용자와의 커뮤니케이션은 한국어 (스킬 내부 정의는 영어)

### Progressive Disclosure 패턴

모든 스킬에서 최종 출력 시 공통 적용:
1. 요약 테이블 먼저 제시 (사용자 확인을 기다리지 않음)
2. 전체 상세 내용 출력
3. 파일 저장

### Target Files 패턴

`feature-draft`, `implementation-plan`, `implementation`에서 사용하는 병렬 실행 지원 메커니즘:

```markdown
**Target Files**:
- [C] `src/new_file.py` -- 새 파일 생성
- [M] `src/existing.py` -- 기존 파일 수정
- [D] `src/deprecated.py` -- 파일 삭제
```

- `[C]` Create, `[M]` Modify, `[D]` Delete
- 동일 파일에 `[M]` 마커가 있는 태스크 쌍 → Sequential (conflict)
- 겹치지 않는 태스크 → Parallel 실행 가능

---

## _sdd/ 아티팩트 맵 (Artifact Map)

각 스킬이 생성/수정하는 `_sdd/` 하위 파일:

| 경로 | 생성 스킬 | 설명 |
|------|----------|------|
| `_sdd/spec/<project>.md` | spec-create | 메인 스펙 문서 |
| `_sdd/spec/SUMMARY.md` | spec-summary | 스펙 요약 |
| `_sdd/spec/SPEC_REVIEW_REPORT.md` | spec-review | 리뷰 리포트 |
| `_sdd/spec/REWRITE_REPORT.md` | spec-rewrite | 리라이트 리포트 |
| `_sdd/spec/DECISION_LOG.md` | spec-create, feature-draft | 의사결정 로그 |
| `_sdd/drafts/feature_draft_*.md` | feature-draft | 피처 드래프트 |
| `_sdd/implementation/IMPLEMENTATION_PLAN.md` | implementation-plan | 구현 계획 |
| `_sdd/implementation/IMPLEMENTATION_REPORT*.md` | implementation | 구현 리포트 |
| `_sdd/implementation/IMPLEMENTATION_REVIEW.md` | implementation-review | 구현 검증 |
| `_sdd/pr/spec_patch_draft.md` | pr-spec-patch | PR 스펙 패치 |
| `_sdd/pr/PR_REVIEW.md` | pr-review | PR 리뷰 |
| `ralph/` | ralph-loop-init | ML 디버그 루프 |

---

## 발견된 이슈 및 개선 필요사항

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
   - 현황: 대부분 skill.json version이 "1.0.0"으로 고정
   - 제안: SKILL.md 변경 시 semver 업데이트 규칙 정립

### 낮은 우선순위 🟢

7. **docs/sdd.md가 독립 개념서**
   - 현황: SDD 개념 설명 문서이나 스킬과 직접 연결되지 않음
   - 제안: SDD_WORKFLOW.md에서 참조 링크 추가

---

## 사용 예시 (Usage Examples)

### 새 프로젝트에서 시작

```bash
# 1. 스펙 생성
/spec-create

# 2. 기능 추가 (스펙 패치 + 구현 계획)
/feature-draft

# 3. 구현 실행
/implementation

# 4. 스펙 동기화
/spec-update-done
```

### PR 리뷰 프로세스

```bash
# 1. PR에서 스펙 패치 초안 생성
/pr-spec-patch

# 2. PR을 스펙 대비 검증
/pr-review
```

### 의사결정 토론

```bash
# 기술 선택, 아키텍처 결정 등
/discussion
```

---

## 설치 및 배포

### Claude Code (Plugin)

```
/plugin marketplace add malfo-y/sdd-skills
/plugin install sdd-skills@sdd-skills
```

### Codex

- **Option A**: LobeHub Skills Marketplace 경유 (README.md 참조)
- **Option B**: `.codex/skills/` 내용을 `$CODEX_HOME/skills/`에 수동 복사
