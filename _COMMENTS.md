# _COMMENTS

Generated at: 2026-03-19T01:14:38.382Z
Total comments: 1

## Comments

### .claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md:L103-L103

8개?

- anchor.hash: 7f6ebc3b
- anchor.snippet: 9개
- anchor.before:                                                    ralph-loop-init (장시간 테스트)
```

discussion은 어디서든 선행 가능 (방향 불확실 시).
guide-create, spec-review는 파이프라인 끝에 선택적 추가.
write-phased는 다른 스킬의 하위 도구로 중첩 호출.

### 2.2 오케스트레이션 대상 스킬 (
- anchor.after: )

autopilot이 생성한 오케스트레이터 파이프라인에 조합하는 스킬.

> **전제 조건**: 글로벌 스펙(`_sdd/spec/main.md`)이 존재해야 한다. 스펙이 없으면 오케스트레이터 생성을 중단하고, 사용자에게 `/spec-create` 실행을 안내한다.

#### feature-draft

- **Role**: 스펙 패치 초안 + 구현 계획을 한 번에 생성
- **Agent*
- createdAt: 2026-03-19T01:13:45.394Z
