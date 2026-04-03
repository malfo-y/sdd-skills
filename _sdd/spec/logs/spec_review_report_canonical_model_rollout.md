# 스펙 리뷰 리포트: SDD Canonical Model Rollout

**리뷰 날짜**: 2026-04-04
**검토 범위**: `docs/SDD_SPEC_DEFINITION.md`, `docs/*.md`, `docs/en/*.md`, `.codex/skills/guide-create/references/template-compact.md`, `.claude/skills/guide-create/references/template-compact.md`, 주요 spec skill surface spot review
**판정**: PASS_WITH_FOLLOW_UP

## 1. 주요 발견사항

### Critical

- 없음.

### High

- 없음.

### Medium

1. **repo-wide 기준으로는 active `_sdd/spec/` 표면에 old vocabulary가 남아 있다.**
   - `rg -n "whitepaper §1-§8|§1-§8|Architecture Details|Component Details" . --glob '!_sdd/spec/logs/**' --glob '!_sdd/spec/prev/**' --glob '!_sdd/implementation/prev/**' --glob '!_sdd/discussion/**'` 결과, `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/DECISION_LOG.md`, 일부 current draft에서 legacy terminology가 계속 발견된다.
   - 이번 rollout plan은 docs/skills/mirror/collateral sync를 범위로 삼았고 `_sdd/spec/main.md` 자체의 대규모 재작성은 out-of-scope였다. 따라서 blocker로 보지는 않지만, vocabulary drift의 재유입 경로가 남아 있다는 뜻이다.

### Low

1. **historical logs, backups, discussion records에는 old wording이 의도적으로 남아 있다.**
   - `_sdd/spec/logs/`, `_sdd/spec/prev/`, `_sdd/discussion/`의 잔존 표현은 기록 보존 성격이 강하므로 이번 rollout의 품질 결함으로 보지 않았다.

## 2. 리뷰 요약

rollout target surface 기준으로는 canonical model 정렬이 성공했다.

- 한국어 docs는 global spec / temporary spec 비대칭 구조, CIV, skills-first sync order를 현재 정의에 맞게 다시 설명한다.
- 영어 미러는 semantic parity를 회복했고 `docs/en/sdd.md`로 self-contained philosophy surface를 추가했다.
- `guide-create` collateral template는 더 이상 old numbered section model을 공유 기준으로 삼지 않고, current canonical language를 기준으로 가이드를 생성하도록 정리되었다.

즉, 이번 작업 범위 안에서는 `docs/SDD_SPEC_DEFINITION.md`와 하위 설명 문서/보조 template 사이의 직접적인 모순이 해소되었다.

## 3. 드리프트 요약

- **정렬된 표면**: `docs/`, `docs/en/`, `guide-create` collateral, 주요 spec skill surface
- **후속 정리 필요 표면**: `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/DECISION_LOG.md`, 일부 current draft
- **기록 보존 표면**: `_sdd/spec/logs/`, `_sdd/spec/prev/`, `_sdd/discussion/`

이번 판정은 "repo 전체가 완전히 canonical vocabulary로 통일되었다"가 아니라, "이번 rollout target surface는 새 model과 정렬되었다"에 가깝다.

## 4. 검증 근거

| Check | Result |
|-------|--------|
| `rg -n "whitepaper §1-§8|§1-§8|Architecture Details|Component Details" docs docs/en .codex/skills/guide-create .claude/skills/guide-create` | PASS (0 hits) |
| `git diff --check -- docs/SDD_WORKFLOW.md docs/SDD_QUICK_START.md docs/SDD_CONCEPT.md docs/sdd.md docs/en/SDD_SPEC_DEFINITION.md docs/en/SDD_WORKFLOW.md docs/en/SDD_QUICK_START.md docs/en/SDD_CONCEPT.md docs/en/sdd.md .codex/skills/guide-create/references/template-compact.md .claude/skills/guide-create/references/template-compact.md` | PASS |
| canonical terms reflected across docs and primary skill surfaces | PASS |
| `.codex/skills/guide-create/references/template-compact.md` vs `.claude/skills/guide-create/references/template-compact.md` | PASS |
| `docs/en/sdd.md` existence | PASS |
| executable tests | `UNTESTED` |

## 5. 권장 후속 조치

1. `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/DECISION_LOG.md`를 별도 spec sync task로 current canonical vocabulary에 맞춘다.
2. current draft 중 재사용 가능성이 높은 문서만 골라 용어를 정리하고, 나머지는 historical artifact로 유지한다.
3. 이후 대규모 canonical migration 때는 `_sdd/spec/` active surfaces를 rollout scope에 명시적으로 포함시키는 편이 안전하다.

## 6. 결론

이번 canonical model rollout은 target surface 기준으로 성공했다. docs, english mirrors, collateral template, 주요 skill 설명 계층은 새 정의와 모순되지 않는다.

다만 repo-wide 기준으로는 active project spec surfaces에 residual legacy wording이 남아 있으므로, 최종 판정은 `PASS_WITH_FOLLOW_UP`가 적절하다.
