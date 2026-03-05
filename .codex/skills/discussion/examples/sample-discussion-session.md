# Sample Discussion Session (Codex Plan Mode)

이 예제는 "API 인증 방식 선택" 토픽에 대한 discussion 스킬 실행 세션 예시다.

## Session Flow

### 0) 모드 확인

```text
User: /discussion

Codex: discussion 스킬은 Plan mode 전용입니다.
Shift+Tab으로 Plan mode로 전환 후 다시 실행해 주세요.
```

(Plan mode 전환 후 재실행)

### 1) 토픽 선택

```text
User: /discussion

Codex:
어떤 관점으로 토론할지 선택해 주세요.
1. 코드베이스 중심 (구조/패턴/리팩토링)
2. 설계/기술 선택 중심 (아키텍처/도구 비교)
3. 토론 종료 / 정리

User: 2 (설계/기술 선택 중심)

Codex:
이번 토론의 목표를 선택해 주세요.
1. JWT vs Session 중 의사결정
2. 결론은 보류하고 비교 기준만 정리
3. 토론 종료 / 정리

User: 1 (의사결정)
```

### 2) 맥락 수집 (로컬 우선 + 선택적 웹)

```text
Codex:
토픽 관련 맥락을 수집합니다.
- 로컬 코드 탐색: rg/Glob/Read로 auth 관련 파일 확인
- 선택적 웹 리서치: JWT/Session 최신 권장 패턴 확인

## 수집된 맥락
| 항목 | 내용 |
|------|------|
| 관련 파일 | 3개 식별 (auth.js, middleware/auth.js, config/session.js) |
| 현재 인증 | Session 기반 (express-session) |
| 확인된 제약 | 6개월 내 다중 서버 전환 계획 |
| 외부 참고 | JWT/Session 비교: 확장성 vs 무효화 복잡도 |
```

### 3) 반복 토론

```text
Codex [Round 1]:
우선 검증할 관점을 선택해 주세요.
1. 리스크 우선 (보안/운영 복잡도)
2. 가치 우선 (확장성/배포 단순화)
3. 토론 종료 / 정리

User: 2

Codex [Round 2]:
다중 서버 전환 일정 기준으로 어떤 방향이 더 현실적인가요?
1. 지금 JWT로 점진 전환
2. 당장은 Session 유지, 전환 시점에 재평가
3. 토론 종료 / 정리

User: 1

Codex [Round 3]:
구현 방식은 어떤 쪽을 우선 검토할까요?
1. Access + Refresh Token 기반
2. Session 유지 + Redis 공유 세션
3. 토론 종료 / 정리

User: 3
```

### 4) 토론 요약

```markdown
# 토론 요약: API 인증 방식 선택 (JWT vs Session)

**날짜**: 2026-03-04
**라운드 수**: 3
**참여 방식**: Structured Discussion (Codex Plan mode)

## 핵심 논점 (Key Discussion Points)
1. 6개월 내 다중 서버 전환 계획 존재
2. Session은 즉시 단순하지만 수평 확장 시 제약
3. JWT는 확장성 장점이 있으나 운영/보안 관리 복잡도 증가

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | JWT 점진 전환 방향 채택 | 전환 일정과 확장성 요구가 명확 | 논점 1, 2, 3 |

## 미결 질문 (Open Questions)
- [ ] Refresh Token 저장/회전 정책
- [ ] 토큰 무효화 전략 (블랙리스트/만료 단축)

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | JWT 전환 기술안 초안 작성 (`feature-draft`) | High | - |
| 2 | 인증 마이그레이션 phase 계획 수립 (`implementation-plan`) | Medium | - |

## 리서치 결과 요약 (Research Findings)
- 로컬 코드 근거: 현재 인증은 express-session 기반
- 외부 리서치: 확장성은 JWT 우위, 운영 복잡도는 Session 우위

## 토론 흐름 (Discussion Flow)
Round 1: 우선 기준 선택 -> 가치 우선
Round 2: 전환 시점 논의 -> 지금 JWT 점진 전환
Round 3: 구현 방식 탐색 -> 종료 및 요약
```

### 5) 저장 핸드오프 (선택)

```text
Codex:
토론 요약을 파일로 저장할까요?
1. 저장하지 않음
2. 기본 경로로 저장 준비
3. 경로 지정 후 저장 준비

User: 2

Codex:
## Save Handoff (Plan mode -> Default mode)
- target_path: _sdd/discussion/DISCUSSION_api-auth-choice_20260305.md
- overwrite_policy: backup-and-replace
- content_source: Step 4 토론 요약 전체

다음 단계:
1) Plan mode를 종료한다.
2) 아래 요청을 실행한다.
"방금 discussion 요약을 _sdd/discussion/DISCUSSION_api-auth-choice_20260305.md에 저장해 줘. 파일이 있으면 prev 백업 후 덮어써."
```
