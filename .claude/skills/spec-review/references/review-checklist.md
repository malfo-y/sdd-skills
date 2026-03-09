# Spec Review Checklist (Strict) / 스펙 리뷰 체크리스트 (Strict)

Use this checklist for review-only spec validation.
This checklist does not authorize direct spec edits.

## 1) Scope Setup / 범위 설정

- [ ] Main spec index identified (`_sdd/spec/<project>.md` or `_sdd/spec/main.md`)
- [ ] Linked sub-spec files identified
- [ ] Generated/backup files excluded (`SUMMARY.md`, `prev/PREV_*.md`)
- [ ] `_sdd/spec/DECISION_LOG.md` loaded if present
- [ ] Review scope declared (Spec-only or Spec+Code)
- [ ] If local runtime/test checks are planned, `_sdd/env.md` is checked and setup is applied first

## 2) Entry Point Quality / 진입점 품질

- [ ] `Goal`이 프로젝트 목적을 한 단락 이내로 빠르게 설명하는가
- [ ] `System Boundary`가 시스템 경계와 외부 의존을 명확히 구분하는가
- [ ] 메인 스펙이 너무 장황하지 않은가 (5분 entry point 역할 가능 여부)
- [ ] `MUST` 정보만으로도 프로젝트 맥락 파악이 가능한가
- [ ] Terms and abbreviations are defined where needed

## 3) Navigation Quality / 탐색 품질

- [ ] `Repository Map`이 존재하고 실제 디렉토리 구조와 일치하는가
- [ ] `Runtime Map`이 존재하고 주요 요청/이벤트/데이터 흐름을 보여주는가
- [ ] `Component Index`가 존재하고 컴포넌트별 책임/비책임/경로가 있는가
- [ ] 컴포넌트 스펙에 Overview 섹션(동작 개요 + 설계 의도)이 있는가 **(MUST — High if missing)**
- [ ] Overview가 코드 구현 복사가 아닌, 사용자 관점의 동작 설명과 설계 근거를 담고 있는가
- [ ] 실제 경로와 심볼이 정확히 연결되는가 (깨진 참조 없음)
- [ ] Section flow is navigable and cross-links are valid

## 4) Changeability / 변경 용이성

- [ ] `Common Change Paths` 또는 동등 정보가 있는가
- [ ] 변경 시 같이 봐야 할 테스트/로그/디버깅 포인트가 보이는가
- [ ] 컴포넌트 책임과 비책임이 구분되어 안전한 편집 범위를 판단할 수 있는가
- [ ] 변경 영향 범위(blast radius)를 스펙만으로 추정할 수 있는가

## 5) Drift Checks / 드리프트 검증

### Code-Linked Drift
- [ ] Architecture claims match current code structure
- [ ] Feature behavior claims match implementation
- [ ] API endpoints/methods/schemas match runtime behavior
- [ ] Config/env/dependency claims match actual project state
- [ ] Issue status in spec reflects implementation/test reality
- [ ] Decision-log assumptions/rationale still match implementation behavior

### Navigation Drift
- [ ] 새 컴포넌트가 구현에만 존재하고 Component Index에 빠져 있지 않은가
- [ ] 런타임 흐름이 바뀌었는데 Runtime Map이 낡지 않았는가
- [ ] 소유 경로가 달라졌는데 Component Index가 낡지 않았는가
- [ ] 운영/디버깅 경로가 바뀌었는데 Common Change Paths에 반영되었는가
- [ ] 이미 해결된 질문이 Open Questions에 남아 있지 않은가
- [ ] 새로 생긴 미결 사항이 Open Questions에 추가되었는가

### Drift Summary Presentation
- [ ] Drift findings summarized in category x severity table before proceeding to severity classification
- [ ] Table covers: Architecture, Feature, API, Config, Issue, Decision-log, Navigation drift categories

## 6) Evidence Quality / 근거 품질

- [ ] Each high/medium finding has concrete evidence (`path:line`, test, diff, commit)
- [ ] Unknowns are explicitly marked as unknown
- [ ] Inference vs direct evidence is clearly distinguished

## 7) Decision Rule / 판정 기준

Choose one:

- [ ] `SPEC_OK`
  - No high findings
  - No unresolved medium findings that block planning/release

- [ ] `SYNC_REQUIRED`
  - At least one high finding, or multiple medium findings requiring spec correction

- [ ] `NEEDS_DISCUSSION`
  - Core ambiguity/trade-off unresolved by available evidence

## 8) Report Completeness / 리포트 완성도

- [ ] Executive summary included
- [ ] Findings grouped by severity
- [ ] Entry Point / Navigation notes included
- [ ] Changeability notes included
- [ ] Spec-to-code drift notes included
- [ ] LLM Efficiency notes included
- [ ] Open questions included
- [ ] Prioritized next actions included
- [ ] Decision-log follow-up proposals included when rationale drift is found
- [ ] Handoff instructions included when `SYNC_REQUIRED`

## 9) Strict Mode Validation / Strict 모드 검증

- [ ] No spec file under `_sdd/spec/` was edited (other than report file)
- [ ] `_sdd/spec/DECISION_LOG.md` was not edited directly in this skill
- [ ] Report saved to `_sdd/spec/SPEC_REVIEW_REPORT.md`
- [ ] Existing report archived as `_sdd/spec/prev/PREV_SPEC_REVIEW_REPORT_<timestamp>.md` if overwritten
- [ ] `MUST` 섹션과 `OPT` 섹션이 구분되어 평가됨; 선택 섹션 누락만으로 약한 스펙이라고 단정하지 않음
