# Spec Review Report (Strict)

**Date**: 2026-03-13
**Reviewer**: Claude
**Scope**: Spec+Code
**Spec Files**: `_sdd/spec/main.md`, `_sdd/spec/DECISION_LOG.md`
**Code State**: `c79d2d8` (0 uncommitted changes)
**Decision**: SYNC_REQUIRED

## Executive Summary

스펙이 v2.0.0으로 whitepaper §1-§8 형식 업그레이드 직후 상태이다. 구조와 서사 품질은 양호하나, 최근 추가된 3개 유틸리티 스킬(`git`, `sdd-upgrade`, `spec-snapshot`)이 스펙에 반영되지 않아 "16개 스킬"이라는 수치가 실제 코드베이스(19개)와 불일치한다. DECISION_LOG의 "Codex 기준" 결정도 현재 실제 운영 방식과 맞지 않는다.

## Findings by Severity

### High

1. **3개 스킬 미문서화 — Architecture Drift**
   - Evidence: `.claude/skills/` 19개 디렉토리 존재, 스펙 §Component Details는 16개만 문서화
   - 미문서화 스킬: `git`, `sdd-upgrade`, `spec-snapshot`
   - 스펙 전역에서 "16개 스킬" 반복 명시 (line 46, 60, 550)
   - Codex도 "15개"라 명시(line 569, 593)하지만 실제 17개 존재 (spec-snapshot 포함)
   - Impact: 스펙을 참조하는 사용자/AI가 존재하는 스킬을 인지하지 못함
   - Recommendation: Component Details에 3개 스킬 추가, 전역 수치 19/18로 수정, Code Reference Index에 추가

### Medium

2. **Code Reference Index 불완전 — Source-field Drift**
   - Evidence: `main.md:651-672` — 16개 스킬만 나열, `git`, `sdd-upgrade`, `spec-snapshot` 누락
   - Impact: 코드 추적 가능성 저하
   - Recommendation: 3개 스킬의 SKILL.md 경로를 Index에 추가

3. **Component Details 미비 — Feature Drift**
   - Evidence: `main.md:276-466` — `git`, `sdd-upgrade`, `spec-snapshot`에 대한 Purpose/Why/Source 테이블 없음
   - Impact: 스킬 설계 근거와 의존성이 문서화되지 않음
   - Recommendation: 3개 스킬에 대한 Component Details 서브섹션 추가

4. **DECISION_LOG "Codex 기준" 결정 진부 — Decision-log Drift**
   - Evidence: `DECISION_LOG.md` (2026-03-09) "`.codex/skills/`를 주 기준으로" 결정
   - 현실: 최근 커밋(6c49d40, 01167af, c79d2d8)은 양 플랫폼을 동시에 수정
   - Claude Code가 더 많은 스킬(19 vs 17)을 보유하고 spec 자체도 `.claude/` 경로를 기준으로 기술
   - Impact: Decision Log가 현재 운영 방식과 모순
   - Recommendation: "듀얼 플랫폼 동시 관리, `.claude/`가 원본" 방향으로 결정 업데이트 제안

### Low

5. **skill.json 미생성 — Config Drift**
   - Evidence: `.claude/skills/sdd-upgrade/` — skill.json 없음, `.claude/skills/spec-snapshot/` — skill.json 없음, `.codex/skills/spec-snapshot/` — skill.json 없음
   - Impact: 스킬 매칭 메타데이터 누락 (기능에는 영향 없을 수 있음)
   - Recommendation: 누락 skill.json 생성

## Spec-Only Quality Notes

- **Clarity**: 양호. 한국어 일관 사용, 용어 정의 명확
- **Completeness**: 문서화된 16개 스킬에 대해서는 충분. 미문서화 3개 스킬이 유일한 갭
- **Explainability**: 모든 문서화된 컴포넌트에 Why 필드 존재 ✅
- **Consistency**: "16개 스킬" 수치가 전역에서 반복되나 실제와 불일치
- **Testability**: Success Criteria (line 58-62) 측정 가능. 단, 16→19 수치 조정 필요
- **Navigability**: TOC, 카테고리 테이블, Cross-reference 양호
- **Ownership**: 스킬별 Source 필드로 소유권 명확

## Spec-to-Code Drift Notes

- **Architecture**: 3개 스킬 미반영 (git, sdd-upgrade, spec-snapshot)
- **Features**: 미문서화 스킬의 기능 설명 부재
- **API**: N/A
- **Configuration**: skill.json 2건 미생성
- **Issues/Technical debt**: 스펙 §Identified Issues #5(Codex 동기화), #6(버전 관리) 여전히 미해결

## Open Questions

1. `git`, `sdd-upgrade`, `spec-snapshot`은 "코어 스킬"로 분류할지 "유틸리티 스킬"로 분류할지?
2. Codex 플랫폼을 계속 동시 지원할 것인지, Claude Code에 집중할 것인지?

## Suggested Next Actions

1. `/spec-update-done` 실행 — 3개 미문서화 스킬을 Component Details, Code Reference Index에 추가, 수치 수정
2. DECISION_LOG.md 업데이트 — "Codex 기준" → "듀얼 플랫폼, .claude/ 원본" 결정 반영
3. 누락 skill.json 생성 (sdd-upgrade, spec-snapshot)

## Decision Log Follow-ups (Proposal Only)

- Proposed entry: **Platform primary target reassessment**
  - Context: 2026-03-09 결정에서 `.codex/skills/`를 주 기준으로 설정했으나, 이후 모든 변경이 양 플랫폼 동시 적용되고 Claude Code가 더 많은 스킬을 보유
  - Decision: `.claude/skills/`를 원본으로, `.codex/skills/`를 파생본으로 정의
  - Rationale: Claude Code가 기능 상위 집합(19 vs 17), 스펙도 `.claude/` 경로 기준으로 기술
  - Alternatives considered: 현행 유지 (거부: 실제 운영과 불일치)
  - Impact: 동기화 방향이 `.claude/` → `.codex/`로 명확해짐

## Handoff for Spec Updates (if SYNC_REQUIRED)

- Recommended command: `/spec-update-done`
- Update priorities:
  - P1: Component Details에 git, sdd-upgrade, spec-snapshot 추가 (High finding 해소)
  - P1: 전역 스킬 수 16→19(Claude), 15→17(Codex) 수정
  - P2: Code Reference Index에 3개 스킬 추가
  - P2: DECISION_LOG.md "플랫폼 기준" 결정 업데이트
  - P3: 누락 skill.json 생성
