# Skill Review: Claude Code SDD Pipeline

**Review Date**: 2026-04-04
**Scope**: `.claude/skills/` 전체 파이프라인 — spec-create → feature-draft → implementation-plan → implementation → implementation-review → spec-update-done
**Reviewer**: Claude Opus 4.6 (사용자 요청에 의한 비판적 리뷰)
**Context**: canonical model rollout + global spec diet 이후, 스킬 체인이 실사용에서 좋은 품질의 결과물을 만들 수 있는지 점검

---

## 요약

큰 구조(thin global spec + temporary spec 7섹션 + CIV ID linkage + Target Files 기반 병렬 실행)는 잘 잡혀 있다. 하지만 실제 사용에서 품질을 떨어뜨릴 수 있는 이슈가 7개 발견되었다. 1건은 단순 버그이고 나머지는 설계/가이드 보강이 필요한 항목이다.

---

## Findings

### 1. [Bug] Mirror Notice가 Codex 경로(`.toml`)를 가리킴

**심각도**: Bug — 즉시 수정 필요
**해당 파일**:
- `.claude/skills/feature-draft/SKILL.md:247`
- `.claude/skills/spec-review/SKILL.md:216`
- `.claude/skills/spec-update-done/SKILL.md:160`
- `.claude/skills/spec-update-todo/SKILL.md:159`

**현상**: Mirror Notice가 `.claude/agents/spec-update-todo.toml`처럼 Codex의 `.toml` 형식을 참조한다. Claude Code 에이전트 파일은 `.claude/agents/*.md`다.

**권장**: `.toml` → `.md`로 교정, `developer_instructions` 표현도 Claude Code에 맞게 수정.

---

### 2. [Medium] Thin Global Spec → Feature Draft 정보 단절

**심각도**: Medium
**해당 스킬**: spec-create, feature-draft

**현상**: spec-create가 만드는 global spec은 `개념 + 경계 + 결정` 3섹션으로 매우 얇다(예시 30줄). 이후 feature-draft가 이 global spec을 읽고 temporary spec의 `Touchpoints`와 `Target Files`를 잡아야 하는데, global spec에 아키텍처/컴포넌트 정보가 없으면 코드베이스를 직접 탐색해야 한다.

feature-draft의 Step 2(Context Gathering)가 코드 탐색을 커버하긴 하지만, "global spec이 얇아도 괜찮다"는 메시지와 "delta의 Touchpoints를 정확히 잡아라"는 메시지 사이에 긴장이 있다.

**리스크**: global spec만 읽고 코드 탐색을 건너뛸 경우 Touchpoints와 Target Files가 부정확해진다.

**권장**: feature-draft에 "global spec이 thin core만 가지고 있으면 반드시 코드베이스 탐색(Step 2)을 수행해야 한다"는 조건을 Hard Rule 또는 Step 2 gate에 명시.

---

### 3. [Medium] feature-draft Part 2 vs implementation-plan 역할 중복

**심각도**: Medium
**해당 스킬**: feature-draft, implementation-plan, sdd-autopilot

**현상**: feature-draft가 Part 2에서 implementation plan을 이미 생성한다. implementation-plan도 별도 스킬로 존재한다. sdd-autopilot의 reasoning reference에서 "대규모만 implementation-plan 포함"이라고 하지만, 이 판단 기준이 feature-draft 스킬 자체에는 없다.

사용자 입장에서 `/feature-draft`를 실행한 후 `/implementation-plan`을 또 실행해야 하는지 모호하다.

**리스크**: 불필요한 중복 작업, 또는 반대로 필요한 상세화를 건너뜀.

**권장**: feature-draft에 "Part 2가 충분한 경우(task 25개 이하, phase 구조 명확)에는 별도 implementation-plan이 불필요하다. Part 2가 부족할 때(task 25개 초과, delta coverage가 불완전, phase 전략이 불명확)만 implementation-plan을 후속 사용한다"는 판단 가이드를 Integration 섹션에 추가.

---

### 4. [Medium] 소규모 작업에 CIV ID 시스템 과잉

**심각도**: Medium
**해당 스킬**: feature-draft, implementation-plan

**현상**: C1/I1/V1 같은 ID 기반 Contract/Invariant/Verifiability 추적이 pipeline 전체를 관통한다. 대규모 기능에는 유용하지만, "버튼 하나 추가" 수준의 작업에도 형식적인 CIV 테이블을 만들게 된다.

feature-draft Hard Rule에 "사용자가 모호하게 요청해도 best-effort로 진행"은 있지만, "작은 변경은 CIV를 경량화해도 된다"는 가이드가 없다. LLM은 규칙을 충실히 따르려 해서, 간단한 작업에도 불필요한 ceremony가 생길 수 있다.

**리스크**: 간단한 작업에 불필요한 overhead, 사용자의 "이건 좀 과한데" 반응.

**권장**: feature-draft에 규모별 CIV 가이드 추가. 예: "delta가 1-2개이고 contract 변경이 없으면 CIV 테이블 대신 inline 서술로 대체 가능. 다만 validation linkage는 유지한다."

---

### 5. [Low] Template/Example 빈약

**심각도**: Low
**해당 파일**: spec-create의 companion assets

**현상**: spec-create의 template/example이 매우 sparse하다.
- `template-compact.md`: 45줄, skeleton만
- `template-full.md`: 54줄, compact에 서브헤딩만 추가
- `simple-project-spec.md`: 30줄

"얇은 게 맞다"와 "유용한 정보가 충분하다"는 다른 개념이다. 현재 예시는 전자만 보여주고, 후자(얇지만 충분히 유용한 spec)의 감을 LLM에 주지 못한다.

**리스크**: LLM이 template을 그대로 따라 너무 얇은 spec을 생성. 특히 중/대규모 프로젝트에서 global spec이 의사결정 맥락을 충분히 담지 못함.

**권장**: template-full에 작성 지침(각 섹션에 무엇을 담아야 하는지, 무엇을 담지 말아야 하는지)을 보강. example에 중규모 프로젝트 예시를 추가해 "얇지만 판단에 충분한" 수준을 보여주기.

---

### 6. [Medium] implementation과 feature-draft 간 Target Files 계약 불일치

**심각도**: Medium
**해당 스킬**: feature-draft, implementation

**현상**: implementation 스킬(284줄)은 Target Files 기반 병렬화에 매우 상세한 규칙을 가지고 있다 — 충돌 매트릭스(C+C, M+M, C+M, M+D, C+D, D+D 전부 충돌), 의미적 충돌 5패턴(모델/타입 import, DB 마이그레이션, config 공유, API contract 소비, 상수/타입 가정).

반면 feature-draft의 Target Files Rules는 "5개 이상 task가 있고 파일이 많이 겹치면 phase를 나누라" 정도만 말한다. feature-draft가 의미적 충돌을 고려하지 않고 Target Files를 배정하면, implementation이 런타임에 충돌을 발견하고 순차 fallback해야 한다.

**리스크**: 병렬 실행 효율 저하, 또는 의미적 충돌로 인한 미묘한 버그.

**권장**: feature-draft의 Target Files Rules에 implementation이 체크하는 의미적 충돌 패턴을 요약 수준으로 추가. 최소한 "동일 모델/타입을 정의하고 소비하는 task는 같은 phase에 두거나 의존성을 명시한다" 정도.

---

### 7. [Low] spec-update-todo/done의 "truly repo-wide" 판단 기준 부재

**심각도**: Low
**해당 스킬**: spec-update-todo, spec-update-done

**현상**: 두 스킬 모두 "truly repo-wide invariant가 정말 필요한 경우만" 같은 표현을 쓴다. "정말 필요한"의 판단 기준이 없다.

**리스크**: LLM마다, 프로젝트마다 판단이 달라져 global spec의 두께가 시간이 지나면서 일관되지 않게 변한다. 어떤 LLM은 너무 많이 올리고, 어떤 LLM은 너무 적게 올린다.

**권장**: 판단 기준 예시 추가. 예:
- repo-wide: "모든 모듈이 따라야 하는 retry 정책", "전체 API의 인증 방식"
- feature-level (올리지 않음): "특정 엔드포인트의 response schema", "한 컴포넌트의 내부 invariant"

---

## Findings from Codex Review Cross-Check

> Codex 리뷰(`_sdd/spec/logs/skill_review_codex_sdd_pipeline_2026-04-04.md`)에서 발견된 이슈 중 Claude Code에도 동일하게 적용되는 항목.

### 8. [High] `_sdd/` path contract가 실제 워크스페이스와 어긋난다

**심각도**: High
**출처**: Codex 리뷰 Finding #1

**현상**: 대부분의 스킬이 `decision_log.md`, `implementation_plan.md` 같은 lowercase 경로를 canonical로 사용한다. 하지만 실제 `_sdd/` 파일 구조에는 `DECISION_LOG.md`, `IMPLEMENTATION_PLAN.md` 같은 uppercase 파일이 존재할 수 있다.

`implementation` 스킬만 legacy uppercase fallback을 명시하고 있고, 나머지 스킬(spec-create, spec-update-todo, spec-update-done, feature-draft 등)은 lowercase만 참조한다.

**리스크**: case-sensitive 환경(Linux, CI)에서 artifact를 찾지 못함. 같은 요청이 환경에 따라 성공/실패가 갈림.

**Codex 결정**: `lowercase canonical + legacy fallback`
**권장**: 동일 정책 적용. lowercase를 canonical로 확정하고, artifact를 읽는 스킬에 일관된 fallback 규칙 적용.

---

### 9. [High] `sdd-autopilot`이 spec 없으면 종료한다

**심각도**: High
**출처**: Codex 리뷰 Finding #2

**현상**: `sdd-autopilot` Step 0에서 `_sdd/spec/*.md`가 없으면 `/spec-create` 안내 후 종료한다. 설명은 "end-to-end 파이프라인"을 약속하지만, spec이 없는 repo에서는 최상위 진입점이 작동하지 않는다.

**리스크**: 사용자는 "일단 `/sdd-autopilot`부터"를 기대하는데 greenfield repo에서 바로 막힘.

**Codex 결정**: `code-first fallback entrypoint` — spec 부재 시 `_sdd/` 부트스트랩 후 코드 기반으로 계속 진행, 적절한 시점에 `spec-create` 권고.
**권장**: 동일 정책 적용. autopilot을 spec-less repo에서도 동작하는 진입점으로 확장.

---

### 10. [Medium] best-effort default가 핵심 ambiguity도 넘긴다

**심각도**: Medium
**출처**: Codex 리뷰 Finding #3

**현상**: `feature-draft`, `implementation-plan`이 정보가 부족해도 멈추지 않고 best-effort로 진행한다. 속도는 올리지만, domain terminology가 모호하거나 touchpoint가 불확실한 상태에서 artifact를 만들면 잘못된 가정이 구조화된 문서로 고정된다.

기존 리뷰 #4(CIV 과잉)와는 다른 문제다. #4는 "형식이 과하다"이고, 이 이슈는 "핵심 판단을 잘못 굳힌다"이다.

**Codex 결정**: `One Extra Question` — 결과 품질이나 방향을 실질적으로 바꾸는 ambiguity면 질문 1회 추가. 그 외는 best-effort 유지.
**권장**: 동일 정책 적용. feature-draft, implementation-plan에 "방향이 달라질 수 있는 핵심 ambiguity면 질문 1회를 추가한다" 명시.

---

### 11. [Medium] `implementation-review`의 한국어 강제가 언어 정책과 충돌한다

**심각도**: Medium
**출처**: Codex 리뷰 Finding #4

**현상**: `implementation-review` Hard Rule 2가 "모든 커뮤니케이션과 리포트는 한국어로 작성한다"로 고정되어 있다. 다른 스킬들은 "기존 문서 언어를 따르고, 없으면 한국어 기본"인데 이 스킬만 한국어 강제다.

**리스크**: 영문 프로젝트에서 review artifact만 한국어로 나옴. pipeline 전체의 언어 일관성이 깨짐.

**Codex 결정**: `User Language First` — 사용자 언어 우선, 신호 약하면 기존 review 문서 언어 fallback.
**권장**: Hard Rule 2를 다른 스킬과 동일한 정책으로 변경.

---

## Status

| # | 이슈 | 심각도 | 상태 |
|---|------|--------|------|
| 1 | Mirror Notice `.toml` 참조 | Bug | **Fixed** |
| 2 | thin spec → feature-draft 정보 단절 | Medium | **Won't Fix** |
| 3 | feature-draft vs implementation-plan 역할 중복 | Medium | **Fixed** |
| 4 | 소규모 CIV 과잉 | Medium | **Won't Fix** — CIV 테이블 생성 비용이 낮고, downstream linkage anchor 가치가 있음 |
| 5 | template/example 빈약 | Low | **Fixed** — template-compact/full에 작성 지침 주석 추가 |
| 6 | Target Files 계약 불일치 | Medium | **Fixed** |
| 7 | "truly repo-wide" 판단 기준 부재 | Low | **Won't Fix** — LLM이 맥락으로 판단 가능 |
| 8 | `_sdd/` path contract 불일치 | High | **Fixed** — 10개 스킬 전부 lowercase canonical + legacy uppercase fallback 규칙 반영 |
| 9 | `sdd-autopilot`이 spec 없으면 종료 | High | **Fixed** — code-first fallback entrypoint로 전환 |
| 10 | best-effort default가 핵심 ambiguity도 넘김 | Medium | **Fixed** — feature-draft, implementation-plan에 "핵심 ambiguity면 질문 1회" 추가 |
| 11 | `implementation-review` 한국어 강제 | Medium | **Fixed** — user language first 정책으로 전환 |
