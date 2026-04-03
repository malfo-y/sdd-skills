# 스펙 리뷰 리포트

**리뷰 날짜**: 2026-04-03
**검토 대상 스펙**: `docs/SDD_SPEC_DEFINITION.md`
**판정**: NEEDS_DISCUSSION

## 1. 주요 발견사항

### Critical

1. **개정된 정의는 아직 SDD 시스템의 나머지 부분과 충돌하고 있어서, 안정적인 canonical definition이라고 보기 어렵다.**
   - 검토 대상 문서는 스펙을 `high-level concept + scope/non-goals/guardrails + key decisions + selective code map` 중심으로 재정의하고, 권장 구조에서 `전략적 Code Map`도 선택 요소로 둔다. 참조: [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L44), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L107), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L153), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L200)
   - 하지만 주변 문서와 툴링은 여전히 canonical spec을 `whitepaper §1-§8` 전체 구조와 아키텍처/컴포넌트 상세를 포함하는 더 두꺼운 문서로 가정하고 있다. 참조: [SDD_WORKFLOW.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_WORKFLOW.md#L61), [SDD_WORKFLOW.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_WORKFLOW.md#L32), [SDD_QUICK_START.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_QUICK_START.md#L9), [SDD_QUICK_START.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_QUICK_START.md#L30), [SDD_CONCEPT.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_CONCEPT.md#L9), [SDD_CONCEPT.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_CONCEPT.md#L24), [spec-upgrade/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-upgrade/SKILL.md#L3), [spec-upgrade/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-upgrade/SKILL.md#L11), [spec-upgrade/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-upgrade/SKILL.md#L122)
   - 영어 미러 문서도 아직 옛 정의를 유지하고 있다. 참조: [en/SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/en/SDD_SPEC_DEFINITION.md#L44), [en/SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/en/SDD_SPEC_DEFINITION.md#L127)
   - 따라서 이 문서는 철학적으로는 개선되었을 수 있지만, 아직 이 repo 안에서 운영적으로 참이라고 말할 수는 없다.

### Quality

2. **문서는 구현 디테일의 비중을 낮추었지만, 그 빈자리를 실행 가능한 계약을 1급 필수 요소로 올리는 방식으로 채우지 않았다.**
   - 개정된 정의는 concept, scope, guardrails, navigation hint를 강하게 강조하지만, `I/O`, `preconditions`, `postconditions`, `invariants`를 명시적인 필수 섹션 또는 필수 하위 내용으로 승격하지는 않는다. 참조: [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L44), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L98), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L217)
   - 이건 실제 결손이다. SDD의 상위 철학은 스펙을 계약으로 보고, I/O, preconditions, postconditions, invariants를 통해 검증 가능성을 정의하기 때문이다. 참조: [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L60), [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L68), [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L78), [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L97), [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L107), [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L185)
   - 이 축이 없으면, 새 정의는 더 얇은 방향 안내 문서일 수는 있어도 실행 가능한 스펙이 되기 어렵다.

3. **문서는 아직 해결되지 않은 설계 선택을 이미 확정된 것처럼 굳혀 버린다.**
   - 토론 기록은 전략적 code map을 어디에 둘지, 그리고 아키텍처/컴포넌트 상세를 지속 스펙에 얼마나 남길지를 명시적으로 open question으로 남겨 두었다. 참조: [discussion_whitepaper_for_humans_vs_llms.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_whitepaper_for_humans_vs_llms.md#L29), [discussion_whitepaper_for_humans_vs_llms.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_whitepaper_for_humans_vs_llms.md#L31)
   - 그런데 검토 대상 문서는 이미 권장 구조에서 `전략적 Code Map`을 `§4`로 고정하고, 아키텍처/컴포넌트 상세는 선택적 참조 정보나 별도 문서 쪽으로 밀어 넣고 있다. 참조: [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L153), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L166)
   - 이것은 성급한 specification이다. 명시적인 decision log나 migration rule 없이 open question을 규범적 구조로 바꾸고 있다.

4. **`Implementation Details`를 `strategic code map / navigation hint`로 매핑한 것은 지나치고, 개념적으로도 부정확하다.**
   - 논문 요소 매핑 표에서 `Implementation Details`는 이제 “필요한 경우에만 남기는 전략적 code map / navigation hint”로 매핑된다. 참조: [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L87)
   - 하지만 navigation hint는 implementation detail과 같은 것이 아니다. navigation hint는 코드를 어디서 볼지 알려 주고, implementation detail은 중요한 설계 구조를 설명한다.
   - 문서의 다른 부분이 “핵심 설계와 주요 결정”을 유지함으로써 일부 보완하고는 있지만, 매핑 표 자체는 여전히 잘못된 추상화를 가르치고 있다.

5. **글로벌 스펙과 임시 스펙의 구분이, 이번 리비전의 핵심 주장에 비해 여전히 너무 약하다.**
   - 이번 수정의 핵심 동기는 지속적인 사람용 스펙은 더 얇아져야 하고, LLM은 필요할 때 상세를 복원할 수 있다는 것이다.
   - 그런데 “이 정의는 글로벌/임시 스펙 모두에 적용된다”는 절은 임시 스펙이 “더 구현 지향적인 정보를 담을 수 있다”고만 말한다. 참조: [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L193), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L208)
   - 이 정도로는 운영 규칙이 부족하다. 독자는 글로벌 스펙에서 무엇이 필수인지, 무엇이 선택적인지, 무엇이 임시 스펙에서 강하게 기대되는지 여전히 알 수 없다.

### Improvements

6. **정의 문서 치고는 용어 통제가 약하다.**
   - 문서는 `high-level concept`, `scope`, `guardrails`, `navigation hint`, `code map` 같은 한국어/영어 혼합 용어를 쓰면서도 작은 용어집이나 정식 한국어 대응을 제공하지 않는다. 참조: [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L44), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L100), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L123)
   - 치명적인 문제는 아니지만, canonical definition 문서라면 용어 드리프트를 빠르게 템플릿과 스킬로 퍼뜨릴 위험이 있다.

## 2. 스펙 품질 요약

개정된 문서는 방향성 자체는 강하다. 사람과 LLM이 같은 정보 밀도를 필요로 하지 않는다는 토론의 핵심 통찰을 잘 포착했고, 지속 스펙은 코드베이스를 복제하기보다 방향성, scope 경계, guardrail을 강조해야 한다는 관점도 잘 반영했다. 특히 `scope`를 다시 정의한 부분은 분명히 좋아졌고, 문서 품질을 실질적으로 개선한다.

하지만 canonical definition으로 보기에는 아직 성숙하지 않았다. 현재 문서는 세 가지 구조적 약점을 갖고 있다.

- repo의 다른 문서와 툴링과 일치하지 않는다
- 구현 디테일을 낮춘 뒤 그 자리를 실행 가능한 계약으로 복구하지 못했다
- 아직 열려 있는 구조적 선택들을 규범적 가이드로 너무 일찍 굳혔다

따라서 이 문서는 철학적으로는 유망하지만, 시스템 수준에서는 아직 시기상조다.

## 3. 드리프트 요약

- **최신 토론과는 정렬되어 있다**: 지속 스펙을 더 얇게 가져가고, scope를 경계 개념으로 보고, 선택적 code map을 두자는 최신 논의와는 잘 맞는다. 참조: [discussion_whitepaper_for_humans_vs_llms.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_whitepaper_for_humans_vs_llms.md#L20), [discussion_whitepaper_for_humans_vs_llms.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_whitepaper_for_humans_vs_llms.md#L22), [discussion_whitepaper_for_humans_vs_llms.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_whitepaper_for_humans_vs_llms.md#L23), [discussion_whitepaper_for_humans_vs_llms.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_whitepaper_for_humans_vs_llms.md#L25)
- **주변 문서와 스킬과는 드리프트가 있다**: 주변 문서들은 여전히 `whitepaper §1-§8 + 아키텍처/컴포넌트 상세` 모델을 전제한다. 참조: [SDD_WORKFLOW.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_WORKFLOW.md#L61), [SDD_QUICK_START.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_QUICK_START.md#L30), [spec-upgrade/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-upgrade/SKILL.md#L18)
- **더 넓은 SDD 철학과도 부분적 드리프트가 있다**: [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L97)에서는 contract/verifiability가 중심인데, 이번 정의에서는 그것이 1급 요소로 남아 있지 않다.

## 4. 코드 분석 메트릭

| Metric | Value | Notes |
|--------|-------|-------|
| Top Hotspots | `spec-create` (41), `spec-rewrite` (33), `spec-review` (27), `_sdd/spec/main.md` (24), `SDD_WORKFLOW.md` (22) | 최근 변경이 스펙 생성/워크플로우 자산에 집중되어 있어, 정의 드리프트를 방치하면 빠르게 퍼질 가능성이 높다. |
| Focus Score | N/A | 이번 리뷰는 정의 문서 대상이었고, 특정 기능 slice의 구현 파일 리뷰가 아니었다. |
| Test Coverage | N/A | 문서 전용 리뷰라 실행 가능한 테스트 표면은 없다. |

## 5. 권장 후속 조치

1. 이 문서가 지금부터 새로운 canonical model인지, 아니면 아직 탐색적 thesis인지 먼저 결정한다. canonical이라면 [SDD_WORKFLOW.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_WORKFLOW.md), [SDD_QUICK_START.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_QUICK_START.md), [SDD_CONCEPT.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_CONCEPT.md), 영어 미러, 그리고 `spec-upgrade`/`spec-create` 템플릿까지 같은 변경 셋에서 함께 맞춰야 한다.
2. 더 얇은 새 모델이 단순 개요 문서로 붕괴하지 않도록, 정의 문서에 `Contract / Invariants / Verifiability` 요구사항을 명시적으로 추가한다.
3. 권장 레이아웃을 표준화하기 전에 남아 있는 구조적 open question을 먼저 해소한다.
   - `전략적 Code Map`을 본문에 둘지, 부록에 둘지, 별도 artifact로 둘지
   - `Architecture Details` / `Component Details`를 선택 섹션으로 둘지, appendix material로 둘지, 아니면 temporary-spec-only material로 둘지
4. 논문 요소 매핑 표를 다시 써서 `Implementation Details`가 `navigation hint`로 붕괴하지 않게 한다.
5. `global spec` vs `temporary spec` 절을 강화해서, 각각에서 기대되는 정보 밀도와 필수 섹션을 더 명시적으로 구분한다.
