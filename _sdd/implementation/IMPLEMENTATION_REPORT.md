# Implementation Report: Codex Implementation Review Loop Follow-up Fixes

## Progress Summary

- Total Tasks: 6
- Completed: 6
- Files Modified: 4
- Verification: `git diff --check` PASS, Codex/Claude mirror wording check PASS

## Completed Tasks

- [x] Codex `implementation` Acceptance Criteria에 `IMPLEMENTATION_REPORT.md` 생성과 `UNTESTED` 근거 기록 요구를 명시
- [x] Codex Step 7 PASS 조건을 `근거 없는 UNTESTED`가 통과되지 않도록 보정
- [x] Codex Step 7.4에 retry context 필수 전달 규칙을 명시
- [x] Claude `implementation`에도 동일한 `UNTESTED` PASS 기준과 retry context 규칙을 반영
- [x] Claude sub-agent prompt에 retry context / retry fix summary를 추가
- [x] Codex/Claude implementation mirror 문서를 동기화

## Files Changed

- `.codex/skills/implementation/SKILL.md`
- `.codex/agents/implementation.toml`
- `.claude/skills/implementation/SKILL.md`
- `.claude/agents/implementation.md`
- `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`
- `_sdd/implementation/IMPLEMENTATION_REPORT.md`

## Key Design Choices

- `implementation-review` 스킬은 독립적으로 유지하고, `implementation` 내부에는 Skeptical Evaluator + AC 검증 loop만 내장했다.
- `UNTESTED`는 더 이상 raw PASS가 아니라, 테스트 불가 사유와 코드 분석 근거가 리포트에 명시된 예외로만 허용한다.
- `"Plan AC"` 같은 모호한 표현은 쓰지 않고 `"Plan의 각 Task별 Acceptance Criteria"`로 고정했다.
- Step 7.3에 `AC -> Task` 역추적 규칙을 명시하고, Step 7.4에는 `failed_ac`, `failure_reason`, `open_critical_high_issues` 재전달을 의무화했다.
- Claude runtime에도 같은 기준을 맞춰 Codex/Claude 사이의 review loop semantics가 다시 벌어지지 않게 했다.

## Verification

- `rg -n "UNTESTED|retry context|Retry Context|Retry Fix Summary|IMPLEMENTATION_REPORT.md" .codex/skills/implementation/SKILL.md .codex/agents/implementation.toml .claude/skills/implementation/SKILL.md .claude/agents/implementation.md`
  - `UNTESTED` 게이트 강화, retry context, report requirements가 Codex/Claude 양쪽에 반영되었는지 확인
- 수동 mirror 확인
  - Codex skill/agent, Claude skill/agent 각각 Step 7 및 retry prompt contract 구조 일치 확인
- `git diff --check`
  - PASS

## Notes

- 기존 구현 리포트와 진행 파일은 `prev/`에 백업했다.
- `_sdd/drafts/feature_draft_codex_implementation_review_loop.md`는 구현 입력으로 사용했다.
- `_sdd/drafts/feature_draft_implementation_inline_orchestration.md`는 unrelated draft로 그대로 유지했다.

## Conclusion

**READY** -- Codex `implementation`의 review-fix loop에서 지적된 PASS gate / report requirement / retry handoff 문제를 보정했고, Claude `implementation`에도 같은 함정을 막는 동일 기준을 반영했다.
