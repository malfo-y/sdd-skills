# _COMMENTS

Generated at: 2026-04-09T06:42:14.594Z
Total comments: 5

## Comments

### .claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md:L85-L85

spec-less 모드 지원과 이건 맞지 않음. 수정 필요.

- anchor.hash: 0f9ac942
- anchor.snippet: 없으면
- anchor.before: own, validation 실행 메모, transient risk log는 global spec 본문으로 가지 않는다.
- global spec으로 올라가는 것은 shared scope, guardrails, key decisions, repo-wide invariant note 같은 정보다.

### 1.7 파이프라인 구성 원칙

1. **Spec-first**: global spec이 
- anchor.after:  구현 전에 `spec-create` 선행.
2. **Delta-first for non-trivial changes**: 중규모 이상 변경은 temporary spec 또는 `feature-draft`를 선행.
3. **Review-fix 필수**: review만 하고 끝나지 않는다.
4. **Execute -> Verify**: 에이전트 호출 != 완료. evidence까지 확인해야 한다
- createdAt: 2026-04-09T06:35:22.332Z

---

### .claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md:L86-L86

중규모 이상 변경 -> 추가적인 계획이 필요한 모든 변경

- anchor.hash: f27cf2e3
- anchor.snippet: 중규모
- anchor.before: obal spec으로 올라가는 것은 shared scope, guardrails, key decisions, repo-wide invariant note 같은 정보다.

### 1.7 파이프라인 구성 원칙

1. **Spec-first**: global spec이 없으면 구현 전에 `spec-create` 선행.
2. **Delta-first for non-trivial changes**: 
- anchor.after:  이상 변경은 temporary spec 또는 `feature-draft`를 선행.
3. **Review-fix 필수**: review만 하고 끝나지 않는다.
4. **Execute -> Verify**: 에이전트 호출 != 완료. evidence까지 확인해야 한다.
5. **파일 기반 handoff**: 상태 전달은 artifact 파일 경로 중심.
6. **Global spec 직접 수정
- createdAt: 2026-04-09T06:36:50.089Z

---

### .claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md:L98-L98

spec-create는 optional; (spec-create) -> feature-draft -> ... -> (spec-update-done) 이 spec-less 모드까지 지원하는 데 맞아 보임.

- anchor.hash: 80f97892
- anchor.snippet: create
- anchor.before: 호출 != 완료. evidence까지 확인해야 한다.
5. **파일 기반 handoff**: 상태 전달은 artifact 파일 경로 중심.
6. **Global spec 직접 수정 금지**: spec 변경은 `spec-update-todo` / `spec-update-done`에 위임.

---

## Part 2: 스킬 카탈로그

### 2.1 스킬 의존성 그래프

```text
spec-
- anchor.after:  -> feature-draft -> spec-update-todo -> implementation-plan -> implementation -> implementation-review -> spec-update-done
                                                                                             |  
- createdAt: 2026-04-09T06:37:43.987Z

---

### .claude/skills/sdd-autopilot/SKILL.md:L144-L144

실제 하지는 않고, 사용자에게 만드는 게 좋다고 가이드만.

- anchor.hash: a560caf8
- anchor.snippet: later `spec-create/spec-update-*` 경로를
- anchor.before: 

### Step 4: Reasoning → Orchestrator Generation (추론 → 오케스트레이터 생성)

Step 1 내재화 + Step 2~3 결과를 바탕으로 추론한다.

| 판단 항목 | 내용 |
|-----------|------|
| 스펙 상태 | global spec 존재 여부와 thin-core relevance 분석. 없으면 `_sdd/` bootstrap + 
- anchor.after:  계획 |
| 변경 범위 | temporary spec 필요 여부 / planned global update 필요 여부 |
| 계획 깊이 | 직접 구현 / feature-draft / implementation-plan |
| 검증 수준 | 인라인 테스트 / Ralph / review 포함 여부 |
| 스킬 순서 | 카탈로그 input/output/pre-condition 기반 |
| 특수 
- createdAt: 2026-04-09T06:39:48.576Z

---

### .claude/skills/sdd-autopilot/SKILL.md:L152-L152

실제 배치하지는 않고, 사용자에게 스펙을 만드는 것 추천 가이드.

- anchor.hash: 6805cb19
- anchor.snippet: 으면 `spec-create`를 파이프라인 후반부(구현/리뷰 이후)에 배치한다. 코드가 먼저 존재해야 spec이 실제 구조를 반영할 수 있기 때문이다
- anchor.before: ate 필요 여부 |
| 계획 깊이 | 직접 구현 / feature-draft / implementation-plan |
| 검증 수준 | 인라인 테스트 / Ralph / review 포함 여부 |
| 스킬 순서 | 카탈로그 input/output/pre-condition 기반 |
| 특수 패턴 | 부분 파이프라인, 팬아웃 병렬, 재개 |

spec-less mode 참고:
- spec이 없
- anchor.after: .
- spec-less인 경우에도 feature-draft의 Part 1 temporary spec은 생성할 수 있다. global spec 없이도 delta 기반 reasoning은 가능하다.

오케스트레이터 생성 규칙:
- 의존성 그래프 기반 동적 조합
- `references/orchestrator-contract.md` 계약 준수
- "구체화된 요구사항"에서 기능 수준 Accepta
- createdAt: 2026-04-09T06:40:13.392Z
