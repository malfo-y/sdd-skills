# SDD Skills & Agents 전체 분석

**생성일**: 2026-03-19
**대상**: `.claude/skills/` (20개 스킬) + `.claude/agents/` (9개 에이전트)

---

## 1. 아키텍처 개요

### 1.1 Wrapper-Agent 패턴

이 프로젝트는 **Wrapper Skill + Dedicated Agent** 패턴을 사용합니다.

- **Skill (SKILL.md)**: 사용자 대면 진입점. 트리거 키워드 정의, 간단한 wrapper 로직
- **Agent (agents/*.md)**: 실제 로직 수행. 도구 접근 권한, 상세 프로세스 정의

| 패턴 | 스킬 | 설명 |
|------|------|------|
| **Thin Wrapper** | write-phased, feature-draft, implementation-plan, implementation-review, implementation, ralph-loop-init, spec-review, spec-update-done, spec-update-todo | SKILL.md는 3줄짜리 wrapper. `Agent(subagent_type=X)`로 바로 위임 |
| **Full Skill** | discussion, spec-create, spec-summary, spec-snapshot, spec-upgrade, spec-rewrite, guide-create, pr-spec-patch, pr-review, git | SKILL.md에 전체 프로세스 로직 포함. 일부는 write-phased 서브에이전트에 파일 작성만 위임 |
| **Meta Skill** | sdd-autopilot | 다른 에이전트들을 순차 오케스트레이션하는 메타스킬 (900줄+) |

### 1.2 전체 워크플로우

```
사용자 요청
    |
    +-- [신규 프로젝트] spec-create -> feature-draft -> implementation-plan -> implementation -> implementation-review -> spec-update-done
    |
    +-- [기능 추가]    feature-draft -> (spec-update-todo) -> implementation -> implementation-review -> spec-update-done
    |
    +-- [PR 워크플로우] pr-spec-patch -> pr-review -> spec-update-todo
    |
    +-- [자동화]       sdd-autopilot (위 워크플로우를 end-to-end 자율 실행)
    |
    +-- [보조]         discussion, spec-summary, spec-snapshot, spec-upgrade, spec-rewrite, guide-create, git, ralph-loop-init
```

---

## 2. 스킬 상세 카탈로그 (20개)

### 2.1 스펙 관리 계열 (8개)

| # | 스킬 | 유형 | 목적 | 서브에이전트 활용 | 병렬화 |
|---|------|------|------|-------------------|--------|
| 1 | **spec-create** | Full Skill | 스펙 문서 신규 생성 | write-phased (파일 작성) | 순차 탐색 |
| 2 | **spec-update-todo** | Thin Wrapper | 스펙에 요구사항/기능 추가 | spec-update-todo agent | 순차 |
| 3 | **spec-update-done** | Thin Wrapper | 코드->스펙 동기화 | spec-update-done agent | 순차 |
| 4 | **spec-review** | Thin Wrapper | 스펙 품질/드리프트 리뷰 | spec-review agent -> write-phased | 순차 감사 |
| 5 | **spec-summary** | Full Skill | 스펙 요약 SUMMARY.md 생성 | write-phased (파일 작성) | 순차 |
| 6 | **spec-snapshot** | Full Skill | 스펙 번역 스냅샷 생성 | 없음 (직접 실행) | 순차 |
| 7 | **spec-upgrade** | Full Skill | 구형식->whitepaper 변환 | write-phased (파일 작성), Explore (코드 분석, 대형만) | 부분적 (대형 코드베이스에서 Explore 위임) |
| 8 | **spec-rewrite** | Full Skill | 스펙 구조 재편/정리 | write-phased (대규모 재작성) | 순차 |

### 2.2 기획/구현 계열 (5개)

| # | 스킬 | 유형 | 목적 | 서브에이전트 활용 | 병렬화 |
|---|------|------|------|-------------------|--------|
| 9 | **feature-draft** | Thin Wrapper | 스펙 패치 초안 + 구현 계획 통합 | feature-draft agent -> write-phased | 순차 (내부에서 코드 탐색은 직접) |
| 10 | **implementation-plan** | Thin Wrapper | 구현 계획 수립 (Target Files 포함) | impl-plan agent -> write-phased | 순차 |
| 11 | **implementation** | Thin Wrapper | TDD 기반 구현 실행 | impl agent -> **general-purpose 서브에이전트 병렬 디스패치** | **핵심 병렬화** (conflict-aware parallel groups) |
| 12 | **implementation-review** | Thin Wrapper | 구현 결과 리뷰 (3-Tier Graceful Degradation) | impl-review agent -> write-phased | 순차 |
| 13 | **guide-create** | Full Skill | 기능별 기술 보고서 생성 | write-phased (파일 작성) | 부분적 (2-페이즈 시 병렬 가능) |

### 2.3 PR 워크플로우 계열 (2개)

| # | 스킬 | 유형 | 목적 | 서브에이전트 활용 | 병렬화 |
|---|------|------|------|-------------------|--------|
| 14 | **pr-spec-patch** | Full Skill | PR diff -> 스펙 패치 초안 | write-phased (파일 작성) | 순차 |
| 15 | **pr-review** | Full Skill | PR 검증 + 판정 | write-phased (파일 작성) | 순차 |

### 2.4 보조/유틸리티 계열 (5개)

| # | 스킬 | 유형 | 목적 | 서브에이전트 활용 | 병렬화 |
|---|------|------|------|-------------------|--------|
| 16 | **discussion** | Full Skill | 구조화된 토론 + 리서치 | Explore + general-purpose (병렬 디스패치) | **병렬 리서치** |
| 17 | **write-phased** | Thin Wrapper | 2-Phase 문서/코드 작성 | write-phased agent | 부분적 (독립 섹션 병렬 가능) |
| 18 | **git** | Full Skill | Smart Git 워크플로우 자동화 | 없음 (직접 실행) | 순차 |
| 19 | **ralph-loop-init** | Thin Wrapper | ML 학습 자동 디버깅 루프 설정 | ralph-loop-init agent | 순차 |
| 20 | **sdd-autopilot** | Meta Skill | end-to-end SDD 파이프라인 오케스트레이션 | **모든 에이전트를 순차 오케스트레이션** + Explore (Step 3) | 부분적 (Step 3 Explore만, 나머지 순차) |

---

## 3. 에이전트 상세 카탈로그 (9개)

| # | 에이전트 | Tools | 주요 기능 | 서브에이전트 사용 | 병렬 실행 메커니즘 |
|---|---------|-------|----------|------------------|-------------------|
| 1 | **write-phased** | Read, Write, Edit, Glob, Grep, Agent | Skeleton->Fill 2-Phase 작성 | 독립 섹션 병렬 Agent 가능 | Phase 2에서 독립 섹션 병렬 채우기 |
| 2 | **implementation** | Read, Write, Edit, Glob, Grep, Bash, Agent | TDD 기반 병렬 구현 실행 | **general-purpose 서브에이전트** (Task tool) | **conflict graph -> parallel groups -> 동시 Task 디스패치** |
| 3 | **feature-draft** | Read, Write, Edit, Glob, Grep, Agent | 스펙 패치 + 구현 계획 통합 | write-phased (파일 작성) | Target Files로 downstream 병렬화 지원 |
| 4 | **implementation-plan** | Read, Write, Edit, Glob, Grep, Agent | 구현 계획 수립 | write-phased (파일 작성) | Target Files로 downstream 병렬화 지원 |
| 5 | **implementation-review** | Read, Glob, Grep, Agent | 3-Tier 구현 리뷰 | write-phased (리포트 작성) | 순차 |
| 6 | **spec-update-todo** | Read, Write, Edit, Glob, Grep | 스펙에 요구사항 추가 | 없음 | 순차 |
| 7 | **spec-update-done** | Read, Write, Edit, Glob, Grep, Bash | 코드->스펙 동기화 | 없음 | 순차 |
| 8 | **spec-review** | Read, Glob, Grep, Agent | 스펙 품질/드리프트 리뷰 | write-phased (리포트 작성) | 순차 |
| 9 | **ralph-loop-init** | Read, Write, Edit, Glob, Grep, Bash | ML 학습 디버깅 루프 초기화 | 없음 | 순차 |

---

## 4. 병렬화 현황 분석

### 4.1 잘 되어 있는 부분

| 위치 | 메커니즘 | 효과 |
|------|---------|------|
| **implementation agent** | Target Files 기반 conflict graph -> parallel groups -> Task tool 동시 디스패치 | 독립 태스크 동시 구현 (핵심 성능 이점) |
| **feature-draft / impl-plan** | 모든 태스크에 Target Files 포함 | downstream implementation의 병렬화 지원 |
| **discussion skill** | Explore + general-purpose 에이전트 병렬 디스패치 | 코드베이스 탐색 + 외부 리서치 동시 수행 |
| **write-phased agent** | Phase 2에서 독립 섹션 병렬 Agent 실행 가능 | 대규모 문서 작성 시 섹션별 병렬 |

### 4.2 개선 가능한 부분

| 위치 | 현재 | 개선안 | 예상 효과 |
|------|------|--------|---------|
| **sdd-autopilot Step 3** | Explore 에이전트 1개만 호출 | 구조/패턴/테스트 등 축별로 병렬 Explore | 코드베이스 분석 시간 단축 |
| **spec-create Step 2** | Glob+Read 순차 탐색 | 대형 코드베이스에서 Explore 에이전트 위임 | 탐색 효율 향상 |
| **spec-upgrade Step 2** | 코드베이스 존재 시 직접 탐색 또는 단일 Explore | Gap별 병렬 코드 분석 | 분석 시간 단축 |
| **spec-review Step 3** | 순차 drift 감사 | 카테고리별 병렬 감사 (arch/feature/API/config) | 리뷰 시간 단축 |
| **spec-update-done Step 2** | 순차 드리프트 감지 | 드리프트 유형별 병렬 감지 | 동기화 시간 단축 |
| **guide-create Step 3** | 순차 코드 증거 수집 | Explore 에이전트로 코드 탐색 위임 | 증거 수집 효율 향상 |
| **pr-spec-patch Step 3-4** | PR 데이터 수집 + 스펙 읽기 순차 | 스펙 읽기와 PR 데이터 수집을 병렬 | 분석 시간 단축 |
| **pr-review Step 2** | 컨텍스트 로딩 순차 | 스펙 + 패치 드래프트 + PR 데이터를 병렬 로딩 | 로딩 시간 단축 |
| **autopilot Step 4.4** | Pre-flight 리소스 타입별 순차 체크 | 리소스 타입별 병렬 체크 | 사전 점검 시간 단축 |
| **implementation-review** | 단일 패스 전체 리뷰 | 대규모 코드베이스에서 모듈별 병렬 리뷰 | 리뷰 시간 단축 |

---

## 5. 스킬 간 의존 관계

### 5.1 입력/출력 매핑

| 스킬 | 주요 입력 | 주요 출력 | 후속 스킬 |
|------|----------|---------|----------|
| spec-create | 코드베이스, 사용자 입력 | `_sdd/spec/main.md`, CLAUDE.md, AGENTS.md | feature-draft, spec-summary |
| feature-draft | `_sdd/spec/`, 사용자 요청 | `_sdd/drafts/feature_draft_*.md` | spec-update-todo, implementation |
| spec-update-todo | feature_draft 또는 사용자 입력 | `_sdd/spec/*.md` (수정) | implementation-plan |
| implementation-plan | `_sdd/spec/`, feature_draft | `_sdd/implementation/IMPLEMENTATION_PLAN.md` | implementation |
| implementation | IMPLEMENTATION_PLAN.md | 구현 코드 + 테스트 + IMPLEMENTATION_REPORT.md | implementation-review |
| implementation-review | 구현 코드, PLAN.md, spec | `_sdd/implementation/IMPLEMENTATION_REVIEW.md` | implementation (fix), spec-update-done |
| spec-update-done | 구현 코드, git diff, 구현 로그 | `_sdd/spec/*.md` (수정) | spec-summary |
| pr-spec-patch | PR diff, `_sdd/spec/` | `_sdd/pr/spec_patch_draft.md` | pr-review |
| pr-review | spec_patch_draft, PR diff, spec | `_sdd/pr/PR_REVIEW.md` | spec-update-todo |

### 5.2 공유 서브에이전트 사용 현황

| 서브에이전트 | 사용처 | 용도 |
|-------------|--------|------|
| **write-phased** | spec-create, spec-summary, spec-upgrade, spec-rewrite, guide-create, feature-draft, impl-plan, impl-review, spec-review, pr-spec-patch, pr-review | 모든 파일 작성을 위임받는 핵심 서브에이전트 |
| **Explore** | sdd-autopilot (Step 3), discussion (Step 2), spec-upgrade (대형) | 코드베이스 탐색 |
| **general-purpose** | discussion (Step 2), implementation agent (병렬 태스크) | 외부 리서치, TDD 서브에이전트 |

---

## 6. 공통 패턴 및 설계 원칙

### 6.1 공통 패턴

| 패턴 | 설명 | 적용 스킬 |
|------|------|----------|
| **Decision Gate** | 각 Step 사이에 조건 검증 후 진행/재시도 분기 | 모든 스킬 |
| **Progressive Disclosure** | 요약 테이블 -> 상세 -> 파일 저장 (확인 대기 없이 자동 진행) | 대부분의 스킬 |
| **Backup before Edit** | `_sdd/spec/prev/PREV_<filename>_<timestamp>.md` 백업 | spec 계열 전체 |
| **Context Management** | 스펙/코드베이스 크기별 읽기 전략 (전체/TOC+섹션/인덱스만) | 모든 스킬 |
| **Language Rule** | 기존 문서 언어 따름, 새 프로젝트는 한국어 기본 | 모든 스킬 |
| **Hard Rule: Spec Read-Only** | 해당 스킬 범위 외 spec 파일 수정 금지 | implementation, review 계열 |

### 6.2 Autonomous Decision-Making

대부분의 에이전트가 **비대화형 자율 결정** 패턴을 채택:

- **모호한 요구사항** -> 최선 추론 + Open Questions 기록
- **누락 정보** -> 기본값 적용 + 판단 근거 명시
- **충돌** -> 리스크 낮은 쪽 선택 + 근거 기록

### 6.3 파일 작성 위임 패턴

대부분의 스킬이 최종 파일 작성을 `write-phased` 서브에이전트에 위임:

```
[스킬] -> 분석/수집 -> 맥락 정리 -> Agent(subagent_type="write-phased", prompt="파일 경로 + 맥락 + 포맷") -> 파일 생성
```

---

## 7. write-phased 병렬 호출 전략 

> **원칙**: write-phased agent 자체는 수정하지 않는다. 호출하는 스킬/에이전트 쪽에서 멀티파일 시나리오일 때 write-phased를 **병렬로 여러 번 호출**한다.

### 7.1 write-phased 호출처 전체 분류

| # | 호출처 | 위치 | 출력 파일 수 | 병렬 대상 |
|---|--------|------|-------------|----------|
| 1 | **spec-create** | SKILL.md Step 3-B | 1 (소규모) / N (중·대규모 split) | ✅ split 시 |
| 2 | **spec-rewrite** | SKILL.md Step 3-5 | N (분할 결과물) | ✅ 분할 시 |
| 3 | **spec-upgrade** | SKILL.md Step 4.3 | 1 (단일) / N (멀티파일 스펙) | ✅ 멀티파일 시 |
| 4 | **guide-create** | SKILL.md Step 5 | N (기능별 가이드) | ✅ 복수 기능 시 |
| 5 | **spec-snapshot** | SKILL.md Step 2 | N (스펙 파일별 번역) | ✅ 항상 멀티파일 |
| 6 | **implementation-plan** | agent.md Step 6 | 1 (단일) / N (Phase별 분할) | ✅ >25 tasks 시 |
| 7 | spec-summary | SKILL.md Step 5 | 1 (SUMMARY.md) | ❌ 단일 파일 |
| 8 | pr-spec-patch | SKILL.md Step 5 | 1 | ❌ 단일 파일 |
| 9 | pr-review | SKILL.md Step 7 | 1 | ❌ 단일 파일 |
| 10 | feature-draft | agent.md Step 7 | 1 | ❌ 단일 파일 |
| 11 | implementation-review | agent.md Step 5 | 1 | ❌ 단일 파일 |
| 12 | spec-review | agent.md Step 5 | 1 | ❌ 단일 파일 |

### 7.2 대상별 상세 수정 계획

---

#### 7.2.1 spec-create (SKILL.md Step 3-B)

**현재**: write-phased 1회 호출 → 단일 파일 또는 순차 멀티파일

**조건**: 중규모(500-1500줄) 또는 대규모(1500줄+)로 판단되어 split spec이 필요할 때

**변경**:
```
Step 3-B를 두 단계로 분리:

Step 3-B-1: main.md (인덱스) 작성
  Agent(subagent_type="write-phased", prompt="main.md 인덱스 작성.
    목표/아키텍처 요약/컴포넌트 링크만 포함.
    컴포넌트 상세는 별도 파일로 분리될 예정.")

Step 3-B-2: 컴포넌트 파일 병렬 작성
  # 독립적인 컴포넌트 파일들을 동시 디스패치
  Agent(subagent_type="write-phased", prompt="api.md 작성. [컴포넌트 맥락]")     ─┐
  Agent(subagent_type="write-phased", prompt="database.md 작성. [컴포넌트 맥락]") ─┤ 동시
  Agent(subagent_type="write-phased", prompt="frontend.md 작성. [컴포넌트 맥락]") ─┘
```

**주의**: main.md가 먼저 완성되어야 컴포넌트 파일의 링크 구조를 확정할 수 있음 → main.md는 순차, 컴포넌트는 병렬

**프롬프트 최소 포함 정보**:
- 파일 경로
- 해당 컴포넌트의 분석 결과 (Step 2에서 수집)
- 스펙 템플릿 (`references/template-compact.md`)
- main.md의 인덱스 구조 (링크 경로 일관성 보장)

---

#### 7.2.2 spec-rewrite (SKILL.md Step 5: Hierarchical Split)

**현재**: 분할 후 파일들을 순차 작성

**조건**: Step 5에서 중규모/대규모 분할이 결정되었을 때

**변경**:
```
Step 5를 두 단계로 분리:

Step 5-1: main.md (인덱스) 재작성
  Agent(subagent_type="write-phased", prompt="main.md 인덱스 재작성.
    Step 2 리라이트 계획 기반. 컴포넌트 링크 구조 포함.")

Step 5-2: 컴포넌트 파일 병렬 작성
  # 기존 내용 재배치 + 정리된 컴포넌트별 파일
  Agent(subagent_type="write-phased", prompt="api.md 작성. [기존 내용 + 정리 방향]")     ─┐
  Agent(subagent_type="write-phased", prompt="database.md 작성. [기존 내용 + 정리 방향]") ─┤ 동시
  Agent(subagent_type="write-phased", prompt="frontend.md 작성. [기존 내용 + 정리 방향]") ─┘
```

**프롬프트 최소 포함 정보**:
- 파일 경로
- Step 2 리라이트 계획 (Keep/Move/Split 매핑)
- 해당 컴포넌트의 기존 내용 (원본에서 추출)
- `references/template-compact.md` + `references/spec-format.md`

---

#### 7.2.3 spec-upgrade (SKILL.md Step 4.3)

**현재**: 멀티파일 스펙도 write-phased 1회 호출

**조건**: 기존 스펙이 멀티파일 구조 (main.md + 서브 파일)일 때

**변경**:
```
Step 4.3:

IF 단일 파일 스펙 → 기존과 동일 (write-phased 1회)

IF 멀티파일 스펙:
  Step 4.3-1: main.md 업그레이드 (§1, §2, §3, §5, §8 보강)
    Agent(subagent_type="write-phased", prompt="main.md whitepaper 형식 변환.
      [Gap 분석 결과 + 코드 분석 결과]")

  Step 4.3-2: 서브 파일 병렬 업그레이드 (§4 상세 보강)
    Agent(subagent_type="write-phased", prompt="api.md §4 보강. [Gap + 코드 분석]")     ─┐
    Agent(subagent_type="write-phased", prompt="database.md §4 보강. [Gap + 코드 분석]") ─┤ 동시
```

**프롬프트 최소 포함 정보**:
- 파일 경로 + 기존 파일 내용
- Step 1 Gap 분석 결과 (해당 파일 관련)
- Step 2 코드 분석 결과 (해당 컴포넌트 관련)
- `references/template-compact.md` + `references/upgrade-mapping.md`

---

#### 7.2.4 guide-create (SKILL.md Step 5)

**현재**: 복수 기능 시 순차적으로 가이드 생성

**조건**: Step 1에서 복수 기능이 감지되었을 때 (Hard Rule #7: per-feature output)

**변경**:
```
Step 5:

IF 단일 기능 → 기존과 동일 (write-phased 1회)

IF 복수 기능 (features = [A, B, C]):
  # 각 기능의 가이드를 독립적으로 병렬 생성
  Agent(subagent_type="write-phased", prompt="guide_feature_a.md 작성.
    [기능 A 스펙 컨텍스트 + 코드 증거]")                                 ─┐
  Agent(subagent_type="write-phased", prompt="guide_feature_b.md 작성.
    [기능 B 스펙 컨텍스트 + 코드 증거]")                                 ─┤ 동시
  Agent(subagent_type="write-phased", prompt="guide_feature_c.md 작성.
    [기능 C 스펙 컨텍스트 + 코드 증거]")                                 ─┘
```

**프롬프트 최소 포함 정보**:
- 파일 경로 (`_sdd/guides/guide_<slug>.md`)
- 해당 기능의 스펙 컨텍스트 (Step 2에서 추출)
- 해당 기능의 코드 증거 + citation 인덱스 (Step 3에서 수집)
- `references/template-compact.md` + `references/output-format.md`

---

#### 7.2.5 spec-snapshot (SKILL.md Step 2)

**현재**: 각 스펙 파일을 순차 Read → 번역 → Write

**조건**: 항상 (스펙 파일이 2개 이상이면)

**변경**:
```
Step 2:

IF 스펙 파일 1개 → 기존과 동일

IF 스펙 파일 N개:
  # 현재 spec-snapshot은 write-phased를 사용하지 않지만,
  # 번역 작업을 write-phased 병렬 호출로 전환
  Agent(subagent_type="write-phased", prompt="main.md → 영어 번역 후
    _sdd/snapshots/<ts>_en/main.md에 저장")                             ─┐
  Agent(subagent_type="write-phased", prompt="api.md → 영어 번역 후
    _sdd/snapshots/<ts>_en/api.md에 저장")                              ─┤ 동시
  Agent(subagent_type="write-phased", prompt="database.md → 영어 번역 후
    _sdd/snapshots/<ts>_en/database.md에 저장")                         ─┘

  # SUMMARY.md는 전체 번역 완료 후 순차 생성 (Step 3)
```

**주의**: SUMMARY.md는 모든 파일 번역이 끝난 후 생성해야 함 → 컴포넌트 번역은 병렬, SUMMARY.md는 순차

**프롬프트 최소 포함 정보**:
- 원본 파일 경로 + 대상 파일 경로
- 원본 파일 내용
- 대상 언어
- 번역 규칙 (도메인 용어 보존, 코드블록 미번역 등)

---

#### 7.2.6 implementation-plan (agent.md Step 6)

**현재**: >25 tasks 시 Phase별 분할 파일을 순차 작성

**조건**: Step 6에서 `total_tasks > 25`으로 Phase별 개별 문서가 결정되었을 때

**변경**:
```
Step 6:

IF total_tasks <= 25 → 기존과 동일 (write-phased 1회, 단일 IMPLEMENTATION_PLAN.md)

IF total_tasks > 25:
  Step 6-1: 인덱스 파일 작성
    Agent(subagent_type="write-phased", prompt="IMPLEMENTATION_PLAN.md 인덱스 작성.
      Overview/Scope/Components/Phase 요약 + Phase 파일 링크")

  Step 6-2: Phase 파일 병렬 작성
    Agent(subagent_type="write-phased", prompt="IMPLEMENTATION_PLAN_PHASE_1.md 작성.
      [Phase 1 태스크 상세]")                                           ─┐
    Agent(subagent_type="write-phased", prompt="IMPLEMENTATION_PLAN_PHASE_2.md 작성.
      [Phase 2 태스크 상세]")                                           ─┤ 동시
    Agent(subagent_type="write-phased", prompt="IMPLEMENTATION_PLAN_PHASE_3.md 작성.
      [Phase 3 태스크 상세]")                                           ─┘
```

**프롬프트 최소 포함 정보**:
- 파일 경로
- 해당 Phase의 태스크 목록 + Target Files + 의존성
- 전체 컴포넌트 정의 (공유 컨텍스트)
- Parallel Execution Summary 데이터

---

### 7.3 공통 규칙

#### 병렬 디스패치 조건

```
IF 출력 파일이 2개 이상 AND 파일 간 내용이 독립적:
  → 병렬 write-phased 호출
ELSE:
  → 기존 단일 호출 유지
```

#### 인덱스-먼저 패턴

멀티파일에서 인덱스/main 파일이 있으면:
```
1. 인덱스 파일 순차 작성 (링크 구조 확정)
2. 컴포넌트/상세 파일 병렬 작성
```

#### 프롬프트 공통 포함 사항

모든 병렬 write-phased 호출에 반드시 포함:
1. **파일 경로** (절대 경로)
2. **해당 파일의 맥락** (분석 결과 중 해당 부분만)
3. **포맷/템플릿** (references 파일 내용 또는 Output Format)
4. **스타일 기준** (기존 스펙의 언어/스타일)
5. **인덱스 파일 구조** (링크 경로 일관성 보장용, 멀티파일 시)

#### write-phased agent 변경 사항

**없음**. write-phased agent는 현재 그대로 유지. 단일 파일 작성 능력만 있으면 됨.

---

### 7.4 예상 효과

| 대상 | 현재 (순차) | 개선 후 (병렬) | 예상 속도 향상 |
|------|------------|---------------|---------------|
| spec-create (3개 컴포넌트) | 3× write-phased 순차 | 1 순차 + 3 동시 | ~2-3x |
| spec-rewrite (4개 파일 분할) | 4× write-phased 순차 | 1 순차 + 4 동시 | ~2-3x |
| guide-create (3개 기능) | 3× write-phased 순차 | 3 동시 | ~3x |
| spec-snapshot (5개 파일 번역) | 5× Read+Write 순차 | 5 동시 | ~3-5x |
| impl-plan (3 Phase 분할) | 3× write-phased 순차 | 1 순차 + 3 동시 | ~2x |

---

## 8. 요약 통계 (업데이트)

| 항목 | 수치 |
|------|------|
| 총 스킬 수 | 20개 |
| 총 에이전트 수 | 9개 |
| Thin Wrapper 스킬 | 9개 (45%) |
| Full Skill | 10개 (50%) |
| Meta Skill | 1개 (5%) |
| 병렬화 활성화 | 2개 (implementation, discussion) |
| 병렬화 부분적 | 4개 (write-phased, guide-create, spec-upgrade, autopilot) |
| 병렬화 미적용 | 14개 (70%) |
| write-phased 사용 스킬 | 11개 (55%) |
| Explore 에이전트 사용 | 3개 (15%) |
