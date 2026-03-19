# Write-Phased 병렬 호출 적용 검증

**Date**: 2026-03-19
**Reviewer**: Claude Code
**Workspace**: `/Users/hyunjoonlee/github/sdd_skills`

## Scope

`_sdd/SDD_SKILLS_ANALYSIS.md` 섹션 7 전략 2+3에 따라, write-phased를 호출하는 6개 스킬/에이전트에 멀티파일 병렬 디스패치를 추가한 변경의 검증.

- 대상: `.claude/skills/{spec-create,spec-rewrite,spec-upgrade,guide-create,spec-snapshot}`, `.claude/agents/implementation-plan.md`
- 목적: 단일/멀티파일 분기가 올바르게 추가되었는지, 기존 단일 파일 동작이 보존되었는지 점검
- 범위: 정적 체크 전수 실행

## Static Checks

- 분기 구조 삽입: **PASS**
- 인덱스-먼저 패턴 일관성: **PASS**
- 기존 단일 파일 보존: **PASS**
- 병렬 디스패치 표기: **PASS**
- Diff whitespace check: **PASS**

---

### 1. 분기 구조 삽입 확인

실행 명령:

```bash
rg "단일 파일|멀티파일|단일 기능|복수 기능|단일 문서|Phase별 분할" .claude/skills .claude/agents
```

결과:

| 파일 | 단일 분기 | 멀티/병렬 분기 |
|------|----------|--------------|
| `spec-create/SKILL.md` | `##### 단일 파일 (소규모, 스펙 500줄 이하)` (L257) | `##### 멀티파일 (중규모 500-1500줄 / 대규모 1500줄+)` (L270) |
| `spec-rewrite/SKILL.md` | (소규모 fallback 문구 L223) | `#### 멀티파일 write-phased 위임` (L200) |
| `spec-upgrade/SKILL.md` | `#### 단일 파일 스펙` (L197) | `#### 멀티파일 스펙 (main.md + 서브 파일)` (L210) |
| `guide-create/SKILL.md` | `#### 단일 기능` (L178) | `#### 복수 기능 (Hard Rule #7: per-feature output)` (L192) |
| `spec-snapshot/SKILL.md` | `#### 단일 파일 스펙` (L79) | `#### 멀티파일 스펙 (2개 이상)` (L87) |
| `implementation-plan.md` | `#### 단일 문서 (total_tasks <= 25)` (L272) | `#### Phase별 분할 문서 (total_tasks > 25)` (L279) |

판정: **PASS** — 6개 파일 모두 단일/멀티 분기 쌍이 존재한다.

---

### 2. 인덱스-먼저 패턴 일관성

실행 명령:

```bash
rg "인덱스-먼저 패턴" .claude/skills .claude/agents
```

결과 (5건 — guide-create 제외):

| 파일 | 인덱스-먼저 패턴 | 순차→병렬 Step 쌍 |
|------|-----------------|------------------|
| `spec-create/SKILL.md` | L272 | Step 3-B-1 (순차) → Step 3-B-2 (병렬) |
| `spec-rewrite/SKILL.md` | L202 | Step 5-1 (순차) → Step 5-2 (병렬) |
| `spec-upgrade/SKILL.md` | L212 | Step 4.3-1 (순차) → Step 4.3-2 (병렬) |
| `spec-snapshot/SKILL.md` | — (전체 병렬) | 파일 간 의존 없음 → 인덱스-먼저 불필요 |
| `guide-create/SKILL.md` | L194 (불필요 명시) | 파일 간 의존 없음 → 전체 병렬 |
| `implementation-plan.md` | L281 | Step 6-1 (순차) → Step 6-2 (병렬) |

판정: **PASS**

- 인덱스-먼저가 필요한 4개 파일 (spec-create, spec-rewrite, spec-upgrade, implementation-plan)에 모두 순차→병렬 Step 쌍 존재
- 인덱스-먼저가 불필요한 2개 파일 (guide-create, spec-snapshot)에 전체 병렬 패턴 사용, guide-create는 "인덱스-먼저 패턴 불필요" 명시

---

### 3. 기존 단일 파일 시나리오 보존

실행 명령:

```bash
rg 'subagent_type="write-phased"' .claude/skills .claude/agents
```

결과 (10건, 이 중 6건이 기존 단일 파일 호출):

| 파일 | 기존 단일 Agent 호출 | 보존 여부 |
|------|-------------------|----------|
| `spec-create/SKILL.md` L261 | `subagent_type="write-phased"` (단일 파일 분기 내부) | ✅ 보존 |
| `spec-upgrade/SKILL.md` L201 | `subagent_type="write-phased"` (단일 파일 분기 내부) | ✅ 보존 |
| `guide-create/SKILL.md` L182 | `subagent_type="write-phased"` (단일 기능 분기 내부) | ✅ 보존 |
| `spec-snapshot/SKILL.md` L82 | `subagent_type="write-phased"` (단일 파일 분기 내부) | ✅ 신규 (기존 Read+Write에서 전환) |
| `spec-rewrite/SKILL.md` L207 | 멀티파일 전용 (기존 Step 3 파일 작성 위임이 단일 담당) | ✅ 기존 구조 유지 |
| `implementation-plan.md` L275 | `subagent_type="write-phased"` (단일 문서 분기 내부) | ✅ 보존 |

판정: **PASS** — 기존 단일 파일 Agent 호출 코드 블록이 모두 그대로 유지된다.

---

### 4. 병렬 디스패치 표기 일관성

실행 명령:

```bash
rg "병렬 디스패치" .claude/skills .claude/agents
```

결과 (수정 대상 6개 파일에서 각 1건씩):

| 파일 | 표기 |
|------|------|
| `spec-create/SKILL.md` L292 | `> 독립 컴포넌트 2개 이상이면 병렬 디스패치.` |
| `spec-rewrite/SKILL.md` L221 | `> 독립 컴포넌트 2개 이상이면 병렬 디스패치.` |
| `spec-upgrade/SKILL.md` L230 | `> 독립 서브 파일 2개 이상이면 병렬 디스패치.` |
| `guide-create/SKILL.md` L204 | `> 독립 기능 가이드 2개 이상이면 병렬 디스패치.` |
| `spec-snapshot/SKILL.md` L98 | `> 독립 파일 2개 이상이면 병렬 디스패치.` |
| `implementation-plan.md` L301 | `> 독립 Phase 파일 2개 이상이면 병렬 디스패치.` |

판정: **PASS** — 6개 파일 모두 blockquote 형식의 병렬 조건 명시가 일관되게 적용.

---

### 5. 병렬 시각적 표기 (─┐ ─┤ ─┘) 일관성

실행 명령:

```bash
rg "─┐|─┤|─┘" .claude/skills .claude/agents (examples/ 제외)
```

결과 (수정 대상 파일만 필터):

| 파일 | ─┐ (시작) | ─┤ (중간) | ─┘ (끝) |
|------|----------|----------|---------|
| `spec-create/SKILL.md` | L287 | L288 | L289 |
| `spec-rewrite/SKILL.md` | L217 | L218 | — (2줄이므로 끝 생략) |
| `spec-upgrade/SKILL.md` | L226 | L227 | — (2줄이므로 끝 생략) |
| `guide-create/SKILL.md` | L199 | L200 | L201 |
| `spec-snapshot/SKILL.md` | L93 | L94 | L95 |
| `implementation-plan.md` | L296 | L297 | L298 |

판정: **PASS** — 3줄 이상이면 ─┐/─┤/─┘ 완전 세트, 2줄이면 ─┐/─┤ 사용. 일관된 패턴.

---

### 6. Diff Whitespace Check

실행 명령:

```bash
git diff --check -- .claude/skills .claude/agents
```

결과: 출력 없음 (whitespace 에러 없음)

판정: **PASS**

---

### 7. 프롬프트 필수 포함 사항 확인

각 병렬 Agent 호출 pseudo-syntax에 필수 맥락이 포함되어 있는지 확인:

| 파일 | 파일 경로 | 분석 맥락 | 템플릿 | 스타일/언어 | 인덱스 구조 |
|------|----------|----------|--------|-----------|-----------|
| `spec-create` | ✅ `_sdd/spec/<comp_N>.md` | ✅ 컴포넌트 분석 | ✅ §4 템플릿 | ✅ 스타일 | ✅ main.md 링크 구조 (L284) |
| `spec-rewrite` | ✅ `_sdd/spec/<comp_N>.md` | ✅ 기존 내용 + 정리 방향 | ✅ (Output Format 참조) | ✅ (L214 맥락) | ✅ main.md 구조 (L214) |
| `spec-upgrade` | ✅ `_sdd/spec/<sub_N>.md` | ✅ 기존 내용 + Gap 분석 | ✅ 템플릿 | ✅ (L223 맥락) | ✅ main.md 구조 (L223) |
| `guide-create` | ✅ `guide_<slug>.md` | ✅ 스펙 컨텍스트 + 코드 증거 | ✅ §1-§5 | ✅ 스타일 | — (인덱스 불필요) |
| `spec-snapshot` | ✅ `<ts>_<lang>/<comp>.md` | ✅ 원본 내용 | — (번역이므로 불필요) | ✅ 대상 언어 (L73 규칙) | — (인덱스 불필요) |
| `implementation-plan` | ✅ `IMPL_PLAN_PHASE_N.md` | ✅ Phase 태스크 + Target Files | ✅ (Output Format 참조) | ✅ (L293 맥락) | ✅ 인덱스 링크 (L283) |

판정: **PASS** — 모든 병렬 Agent 호출에 필수 맥락 정보가 포함되어 있다.

---

### 8. 교차 참조 확인

| 파일 | 참조 | 참조 대상 존재 |
|------|------|--------------|
| `spec-rewrite/SKILL.md` L129 | "Step 5 '멀티파일 write-phased 위임' 참조" | ✅ L200에 존재 |
| `spec-rewrite/SKILL.md` L223 | "Step 3의 단일 write-phased 호출로 처리" | ✅ L127 파일 작성 위임 섹션 |
| `spec-snapshot/SKILL.md` L65 | "Step 2 병렬 디스패치 준비" | ✅ L67 Step 2에 병렬 디스패치 존재 |
| `spec-snapshot/SKILL.md` L100 | "SUMMARY.md는 Step 3에서 모든 번역 완료 후 순차 생성" | ✅ L102 Step 3 존재 |

판정: **PASS**

---

## Diff Summary

```
 .claude/agents/implementation-plan.md | 31 +++++++++++++++++++++
 .claude/skills/guide-create/SKILL.md  | 16 +++++++++++
 .claude/skills/spec-create/SKILL.md   | 28 +++++++++++++++++++-
 .claude/skills/spec-rewrite/SKILL.md  | 27 +++++++++++++++++++-
 .claude/skills/spec-snapshot/SKILL.md | 43 ++++++++++++++++++++---------
 .claude/skills/spec-upgrade/SKILL.md  | 24 +++++++++++++++
 6 files changed, 154 insertions(+), 15 deletions(-)
```

## Checklist Coverage

### 기본 검증

- [x] 6개 파일 모두 단일/멀티 분기 삽입 완료
- [x] 기존 단일 파일 Agent 호출 코드 그대로 보존
- [x] 인덱스-먼저 패턴 필요한 4개 파일에 순차→병렬 Step 쌍 존재
- [x] 인덱스-먼저 불필요한 2개 파일에 전체 병렬 패턴 사용
- [x] 6개 파일 모두 "N개 이상이면 병렬 디스패치" 조건 명시
- [x] 병렬 시각적 표기 (─┐─┤─┘) 일관
- [x] Whitespace 에러 없음

### 변경 원칙 준수

- [x] write-phased agent 자체는 변경하지 않음 (확인: `.claude/skills/write-phased/SKILL.md` 미변경)
- [x] 단일 파일 시나리오는 기존 동작 그대로 유지
- [x] 병렬 조건은 계획서에 명시된 조건만 적용 (500줄+, 2개+, >25 tasks 등)
- [x] 프롬프트 필수 포함 사항 (파일 경로, 맥락, 템플릿, 스타일, 인덱스 구조) 누락 없음

### 파일별 세부 확인

- [x] `spec-create`: Step 3-B에 `##### 단일 파일` + `##### 멀티파일` 추가, `> note`가 분기 전으로 이동
- [x] `spec-rewrite`: Step 5 뒤에 `#### 멀티파일 write-phased 위임` 삽입 + Step 3 교차 참조 추가
- [x] `spec-upgrade`: `### 파일 작성 위임`에 `#### 단일 파일 스펙` + `#### 멀티파일 스펙` 추가
- [x] `guide-create`: `### 파일 작성 위임`에 `#### 단일 기능` + `#### 복수 기능` 추가 (인덱스-먼저 불필요 명시)
- [x] `spec-snapshot`: Step 2를 Read+Write → write-phased 위임으로 전환, Step 1에 사전 Read 추가
- [x] `implementation-plan`: `### 파일 작성 위임`에 `#### 단일 문서` + `#### Phase별 분할 문서` 추가

## Smoke Tests

| Scenario | Result | Notes |
|----------|--------|-------|
| spec-create (소규모) | NOT RUN | 실제 프로젝트에서 500줄 이하 스펙 생성 시 단일 파일 경로 확인 필요 |
| spec-create (중/대규모) | NOT RUN | 500줄+ 프로젝트에서 멀티파일 병렬 디스패치 확인 필요 |
| spec-rewrite (중/대규모) | NOT RUN | 분할 리라이트 시 인덱스-먼저 병렬 확인 필요 |
| spec-upgrade (멀티파일) | NOT RUN | main.md + 서브 파일 업그레이드 시 병렬 확인 필요 |
| guide-create (복수 기능) | NOT RUN | 2개+ 기능 가이드 생성 시 전체 병렬 확인 필요 |
| spec-snapshot (멀티파일) | NOT RUN | 2개+ 스펙 파일 번역 시 병렬 확인 필요 |
| implementation-plan (>25 tasks) | NOT RUN | 25+ 태스크 플랜에서 Phase별 병렬 확인 필요 |

### Smoke Test Limitation

정적 검증만 수행하였으며, 실제 Claude Code 세션에서 각 스킬의 멀티파일 시나리오를 직접 트리거하는 런타임 테스트는 별도 수행이 필요하다.

## Overall Result

**정적 검증: PASS**

해석:

- 6개 파일 모두 계획서대로 단일/멀티 분기가 삽입되었다.
- 기존 단일 파일 동작은 모든 파일에서 보존되었다.
- 인덱스-먼저 패턴이 필요한 4개 파일에서 순차→병렬 순서가 명확하다.
- 전체 병렬이 적합한 2개 파일(guide-create, spec-snapshot)에서 올바른 패턴을 사용한다.
- write-phased agent 자체(`write-phased/SKILL.md`)는 변경되지 않았다.
- 154 insertions, 15 deletions — 기존 내용 대부분 보존, 새 분기만 추가.

## Recommended Next Step

1. 중규모+ 프로젝트에서 `spec-create`를 실행하여 멀티파일 병렬 디스패치가 실제로 트리거되는지 확인
2. `guide-create`에서 복수 기능 요청 시 per-feature 병렬 생성 확인
3. `spec-snapshot`에서 멀티파일 스펙 번역 시 병렬 디스패치 확인
