# Discussion: Lowercase Artifact Filenames

- Date: 2026-04-02
- Rounds: 1
- Topic: 스킬 산출물과 백업 파일명의 대문자 규칙을 소문자 규칙으로 통일할지 검토

## Core Points

- 현재 저장 규칙은 혼합 상태다.
  - 소문자 예: `discussion_<title>.md`, `guide_<slug>.md`
  - 대문자 예: `IMPLEMENTATION_PLAN.md`, `IMPLEMENTATION_REPORT.md`, `SUMMARY.md`, `SPEC_REVIEW_REPORT.md`, `DECISION_LOG.md`, `PREV_*`
- 방향성 자체는 소문자 통일이 더 낫다.
  - slug 기반 파일명과 더 자연스럽게 맞는다.
  - 산출물 네이밍 규칙이 일관돼진다.
  - OS/도구별 대소문자 혼동을 줄인다.
- 다만 범위는 작지 않다.
  - `_sdd/spec/main.md`
  - `.codex/skills/*`
  - `.claude/skills/*`
  - examples / references / 기존 산출물 문서
  - 실제 `_sdd/` 아래 기존 파일 및 `prev/`, `SYNC_*` 관례

## Decisions

- 파일명 소문자 통일 방향에는 찬성한다.
- 적용 방식은 `점진 전환`이 적절하다.
- 즉시 일괄 rename보다는 다음 원칙이 안전하다.
  - 새로 생성하는 산출물은 소문자 파일명 사용
  - 기존 대문자 파일명은 일정 기간 읽기/참조 호환 대상으로 유지
  - 스킬 계약과 스펙 문서에서 새 canonical 경로를 먼저 선언
  - 실제 rename은 후속 단계에서 묶어서 수행

## Open Questions

- canonical 소문자 규칙을 어디까지 적용할지
  - `implementation_plan.md`, `implementation_report.md`, `implementation_review.md`
  - `summary.md`, `spec_review_report.md`, `decision_log.md`
  - `prev_<filename>_<timestamp>.md`
- 기존 대문자 파일을 얼마나 오래 호환 대상으로 둘지
- `SYNC_*` 같이 타임스탬프 prefix가 붙은 산출물도 함께 소문자화할지
- 백업/아카이브 파일은 rename 대신 신규 규칙만 적용할지

## Action Items

- 1. 현재 대문자 산출물 이름의 canonical 목록을 확정한다.
- 2. 소문자 target 이름 매핑표를 만든다.
- 3. 점진 전환 전략을 문서화한다.
  - 새 출력은 소문자
  - 기존 입력은 대문자/소문자 둘 다 허용
- 4. 영향 범위가 큰 스킬부터 순서대로 바꾼다.
  - `implementation-plan`
  - `implementation`
  - `implementation-review`
  - `spec-summary`
  - `spec-review`
  - `spec-create` / `spec-update-*`
- 5. 마지막 단계에서 실제 파일 rename 및 spec cleanup 여부를 다시 판단한다.

## Research Summary

- 로컬 검색 결과, 대문자 산출물 파일명은 스킬 본문뿐 아니라 `_sdd/spec/main.md`와 기존 산출물 기록 전반에 넓게 퍼져 있다.
- 특히 아래 경로들이 반복적으로 참조된다.
  - `_sdd/implementation/IMPLEMENTATION_PLAN.md`
  - `_sdd/implementation/IMPLEMENTATION_REPORT.md`
  - `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
  - `_sdd/spec/SUMMARY.md`
  - `_sdd/spec/SPEC_REVIEW_REPORT.md`
  - `_sdd/spec/DECISION_LOG.md`
  - `_sdd/spec/prev/PREV_*`
- 따라서 이 변경은 cosmetic rename이 아니라 계약 변경 + 호환성 마이그레이션으로 보는 편이 맞다.

## Sources

- Local search:
  - `rg -n "IMPLEMENTATION_|SUMMARY\.md|PREV_|REWRITE_REPORT|SPEC_REVIEW_REPORT|DECISION_LOG|discussion_" .codex/skills .claude/skills _sdd/spec _sdd/env.md`
  - `find . -path '*/.git' -prune -o -type f \( -name '*[A-Z]*.md' -o -name 'PREV_*' \) -print | sort`

## Discussion Flow

- 사용자 제안: 결과 저장 파일의 대문자 네이밍을 전부 소문자로 바꾸고 싶음
- 초기 판단: 방향은 좋지만 영향 범위가 넓어 단순 rename으로 보기 어려움
- 분기 질문: 점진 전환 vs 즉시 일괄 전환 vs 정리/종료
- 사용자 선택: `점진 전환`
- 최종 결론: 소문자 통일에 찬성하되, 새 산출물부터 소문자로 전환하고 기존 대문자 경로는 한동안 호환 대상으로 유지
