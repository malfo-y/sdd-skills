# _COMMENTS

Generated at: 2026-08-12T07:45:24.198Z
Total comments: 6

## Comments

### .claude/agents/plan-review-agent.md:L50

> 결과 방향을 바꿀 수 있는 모호성, Target Files 선택, task boundary 결정에 가정·대안·확신도·사용자 확인 필요 여부가 드러나는가?

이 문장이 필요한가?

---

### .claude/agents/plan-review-agent.md:L77

> # Claim Manifest`가 있으면 **manifest 행을 전수 순회**해 각 Query를 재실행하고 Expected와 대조한다(표본 아님). 

feature-draft에서 없앨 예정

---

### .claude/skills/feature-draft/SKILL.md:L15 (~L17)

> 2. **단일 컨텍스트 초과**: 작업 총량이 한 세션에서 품질 저하 없이 끝날 규모를 넘는다.

이건 평가하지 말자. 애초에 제대로 평가가 가능한 영역이 아님.

---

### .claude/skills/feature-draft/SKILL.md:L17

> "머리 하나에 다 안 담기는가?"** 담기면 단일 draft, 안 담기면 쪼갠다

무슨 소린지 모르겠다.

---

### .claude/skills/feature-draft/SKILL.md:L36

> task는 단일 의도를 가지고 자기 AC만으로 완료 판정이 닫히는 실행 단위다.

task의 정의를 좀 더 명확히 드러나게 하기.

---

### .claude/skills/feature-draft/SKILL.md:L102

> Claim Manifest 단일 소스**: repo 대조가 필요한 사실 주장(AC content anchor 실재, 기존 로직·중복 실재 등 사실 전제)은 `# Claim Manifest` 표가 단일 소스다. AC 평가방법·Description·Contracts 산문은 그 주장을 `CM<n>` ID로 참조하고 query·expected를 재서술하지 않는다. Target Files·Propagation `Discovery evidence`는 기존 구조가 소유한다 — manifest에 중복 수록하지 않는다.

이거 없애자. 내가 해보니까 plan review 시간 단축 등에는 쓸모가 없다.
