# Spec Review Report

**Review Date**: 2026-06-12
**Reviewed Spec**: `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md` (thin global spec + supporting surfaces)
**Spec Type**: Global
**Decision**: SYNC_REQUIRED

리뷰 범위는 사용자 지정 경로가 없어 자체 결정했다. 우선순위(`_sdd/spec/*`)에 따라 thin global spec 3종을 1차 대상으로 잡고, 현재 브랜치(`feature/agents-md-harness-layer`)에서 최근 머지된 2개 feature stream(AGENTS.md harness layer, feature draft output diet)을 code-linked drift 기준으로 교차 점검했다.

## 1. Findings

### Critical
- **(C-1) global spec 설계 모델이 신규 repo-wide layer를 누락 — 잘못된 repo-wide truth 서술.**
  `main.md:79-84`는 "SDD Skills의 설계는 **네 층**으로 나뉜다 (Skill / Agent / Artifact / Reference)"로 repo-wide 설계를 단정한다. 그러나 2026-06-12 머지된 harness 작업(commit `e5ad765`)이 `docs/SDD_CONCEPT.md:7-15`와 `docs/SDD_WORKFLOW.md:18-22`에 **Harness (AGENTS.md) 레이어를 global spec 위에 놓이는 1급 repo-wide layer**로 정식 도입했다. `main.md:71`은 `SDD_WORKFLOW.md`를 "workflow semantics 기준 문서(canonical)"로 선언하므로, global spec이 가리키는 canonical 문서가 5번째 layer를 정의하는데 global spec 본문은 여전히 4-layer 모델만 단정하는 직접 모순이다. 이는 reader/agent에게 잘못된 repo-wide 구조 truth를 제공한다.
  - Evidence: `_sdd/spec/main.md:79-84`, `docs/SDD_CONCEPT.md:7-15`, `docs/SDD_WORKFLOW.md:18-22`, `main.md:71` (SDD_WORKFLOW canonical 선언), `git log` commit `e5ad765`.

### Quality
- **(Q-1) usage-guide의 AGENTS.md 산출 기술이 stale — code-vs-doc drift.**
  `usage-guide.md:29`는 `spec-create`의 AGENTS.md 산출을 "동일한 워크스페이스 안내 유지"(legacy 빈 bootstrap)로 기술한다. 실제 구현은 `spec-create` SKILL이 harness 템플릿(§0~§4) 기반으로 AGENTS.md를 생성하도록 격상됐다(SKILL.md 내 harness 참조 18건, `agents-harness-template.md` 4곳 byte-identical 미러 `7e85521b...`). usage-guide의 expected result가 현재 실제 산출과 불일치한다.
  - Evidence: `_sdd/spec/usage-guide.md:29`, `.claude/skills/spec-create/SKILL.md`(harness grep count 18), `.claude|.codex × spec-create|spec-upgrade /references/agents-harness-template.md` 4곳 md5 동일.
- **(Q-2) Spec Version metadata lag.**
  `main.md:5`는 `Spec Version 4.1.14 / 2026-06-03`인데 `logs/changelog.md:5`의 최신은 `v4.1.15 (2026-06-09)`다. harness 작업(2026-06-12)은 설계상 global 본문 무변경(I1)이라 버전 갱신 대상이 아닐 수 있으나, v4.1.15 변경분조차 header에 반영되지 않아 metadata가 한 단계 뒤처져 있다.
  - Evidence: `_sdd/spec/main.md:5`, `_sdd/spec/logs/changelog.md:5`.

### Improvements
- **(I-1) harness layer를 supporting surface에 navigation hint로 추가 고려.**
  C-1을 4-layer→harness 포함으로 보정할 때, `components.md`의 spec-create 행(`components.md:14`)이나 `Strategic Code Map`에 harness 템플릿 정본 경로(`.claude/skills/spec-create/references/agents-harness-template.md`)와 SDD_CONCEPT.md를 navigation hint로 추가하면 reader가 신규 layer surface를 찾기 쉬워진다. code map 부재 자체는 defect 아님(optional).
  - Evidence: `_sdd/spec/components.md:14,77`, harness 정본 경로 존재 확인.

## 2. Applied Rubric

**Global rubric** (thin-core model)을 적용했다. 공통 코어 4축 판정:

| 축 | 판정 | 근거 |
|----|------|------|
| Thinness | PASS | 본문은 배경/경계/결정 중심을 유지. inventory 오염 없음 |
| Decision-bearing truth | FAIL (C-1) | 4-layer 설계 단정이 canonical workflow doc의 신규 layer와 모순 → 잘못된 repo-wide truth |
| Anti-duplication | PASS | guide/README/code 무의미 복제 없음 |
| Navigation + surface fit | PARTIAL (Q-1, I-1) | usage-guide expected result가 실제 산출과 불일치, 신규 layer surface로의 navigation 부재 |

global rubric 보호 규칙 준수: old canonical section 부재, usage/`참조 정보`/code-map appendix 부재는 defect로 분류하지 않았다. global 오염류 findings는 기본 `Quality`로 두고, repo-wide 구조 truth를 직접 오도하는 C-1만 `Critical`로 승격했다(Hard Rule 6 기준).

## 3. Evidence Summary

- 모든 finding은 concrete spec/doc/code evidence를 보유. `UNTESTED` 처리한 추정 finding 없음.
- harness 구현 실재 확인: 4곳 미러 md5 `7e85521b08a0b758142c2cfdc9495d54` 동일, spec-create SKILL harness 참조 18건, docs 2종 layer 도입 커밋(`e5ad765`) 확인.
- main.md가 참조하는 외부 경로 8종(`docs/*`, `components.md`, `usage-guide.md`, `DECISION_LOG.md`, `logs/changelog.md`, `env.md`, `README.md`) 전부 resolve — broken reference 없음.

## 4. Spec Quality Summary

thin global spec의 구조 품질 자체는 양호하다. 배경/Scope·Non-goals·Guardrails/핵심 설계와 주요 결정의 3대 축이 분명하고, Guardrails와 결정 테이블이 repo-wide 판단을 잘 고정한다. 단일 결함은 **2026-06-12 harness 도입이 methodology docs·skills·templates에는 반영됐으나 global spec 본문(main.md 설계 모델)과 usage-guide expected result에는 반영되지 않은 surface lag**다. 구현 보고서는 "global 본문 thin 유지(I1)"를 근거로 spec sync 불요라 판단했으나, harness가 단순 feature가 아니라 **repo-wide methodology layer**여서 global 설계 모델의 layer 서술(4 vs 5)과 usage expected result는 동기화 대상이다.

## 5. Drift Summary

| Item | Status | Note |
|------|--------|------|
| main.md 4-layer 설계 모델 vs SDD_CONCEPT/WORKFLOW harness layer | DRIFT | canonical workflow doc이 5번째 layer 정의, 본문은 4-layer 단정 (C-1) |
| usage-guide AGENTS.md 산출 기술 vs spec-create 구현 | DRIFT | "동일 안내 유지" → 실제는 harness 템플릿 생성 (Q-1) |
| harness 템플릿 4곳 미러 정합 | ALIGNED | byte-identical 확인 |
| spec-create/spec-upgrade SKILL harness 멱등 병합 | ALIGNED | SKILL 본문에 harness 절차 반영 확인 |
| feature draft output diet (Part 1/2 재구성) | ALIGNED | global spec은 feature-draft 내부 section 구조를 서술하지 않음 → 본문 drift 없음 |
| Spec Version metadata | DRIFT (minor) | header v4.1.14, changelog v4.1.15 (Q-2) |
| main.md 외부 reference 경로 | ALIGNED | 8종 전부 resolve |

## 6. Code Analysis Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Top Hotspots | `orchestrator-contract.md` (17/16 codex·claude), `sample-orchestrator.md` (16/11), autopilot/feature-draft/implementation-plan SKILL (10~13) | autopilot·planning surface가 변경 집중. `_sdd/spec/components.md`(9)·`main.md`(8)도 상위 → spec 본문이 자주 변하는 thin 문서임 |
| Focus Score | harness stream: spec-create/spec-upgrade × 2플랫폼 + references 4곳 + docs 2종에 100% 집중 (global spec 본문 0% = 설계 의도, 단 그 결과가 C-1 drift) | 변경은 의도대로 harness 컴포넌트에 집중됐으나 global 설계 모델 동기화가 누락됨 |
| Test Coverage | 0/0 (자동 테스트 프레임워크 부재) | 마크다운 자산 repo. 검증=grep/diff/review가 유효 evidence (env 정합). harness V1~V7은 review/diff/grep로 커버, 멱등 V4는 소비 repo 수동 시나리오로 위임 (UNTESTED 성격, 정상) |

## 7. Recommended Next Actions

1. **C-1 / Q-1 보정 (우선)**: `spec-update-done`으로 global spec을 동기화한다. 구체적으로 (a) `main.md:79-84` 설계 모델을 harness layer 포함으로 보정(또는 harness가 별도 methodology layer임을 한 줄로 명시해 4-layer 서술과의 모순 제거), (b) `usage-guide.md:29` AGENTS.md expected result를 harness 템플릿 산출 기준으로 갱신. harness는 verified persistent repo-wide truth이므로 update-done 승격 대상이다.
2. **Q-2**: spec version header를 changelog 최신(v4.1.15+)과 정합시키고, harness 동기화 반영 시 changelog/version 엔트리를 함께 갱신한다.
3. **I-1 (optional)**: 보정 시 `components.md` spec-create 행 또는 `Strategic Code Map`에 harness 템플릿 정본 경로·SDD_CONCEPT.md를 navigation hint로 추가.
4. 이 agent는 review-only다. 위 수정은 직접 수행하지 않으며 `spec-update-done`(구현 후 동기화)으로 위임한다. 구현 자체 재검증이 필요하면 `implementation-review`를 교차 참조한다.
