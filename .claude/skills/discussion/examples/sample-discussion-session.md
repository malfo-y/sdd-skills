# Sample Discussion Session

이 예제는 "API 인증 방식 선택" 토픽에 대한 discussion 스킬 실행 세션을 보여줍니다.

## Session Flow

### 1. 토픽 선택

```
User: /discussion

Claude: 구조화된 토론을 시작합니다.

어떤 주제에 대해 토론하고 싶으신가요?
1. 코드베이스 관련 (구조, 패턴, 리팩토링 등)
2. 아키텍처 설계 (시스템 설계, 컴포넌트 구조 등)
3. 기술 선택 (라이브러리, 프레임워크, 도구 비교)
4. Other (직접 입력)

User: 3 (기술 선택)

Claude: 기술 선택에서 구체적으로 어떤 부분을 논의하고 싶으신가요?

User: API 인증 방식을 JWT vs Session 중 어떤 걸 쓸지 고민이에요
```

### 2. 맥락 수집

```
Claude:
관련 맥락을 수집 중입니다...

[Sub-agent: Explore] 코드베이스에서 현재 인증 관련 코드 탐색 중...
[Sub-agent: general-purpose] JWT vs Session 인증 비교 자료 수집 중...

## 수집된 맥락
| 항목 | 내용 |
|------|------|
| 현재 인증 | Session 기반 (Express + express-session) |
| 관련 파일 | 3개 식별 (auth.js, middleware/auth.js, config/session.js) |
| 외부 참고 | JWT/Session 비교 (보안, 확장성, 구현 복잡도) |
```

### 3. 반복 토론

```
Claude:
[Round 1] 현재 Session 기반 인증을 사용하고 계시네요.
JWT로 전환을 고려하는 주된 이유가 무엇인가요?

1. "확장성 (서버 다중화, 마이크로서비스)"
2. "모바일 앱 지원 필요"
3. "현재 Session 방식에 문제가 있어서"
4. "토론 종료 / 정리해줘"

User: 1 (확장성)

Claude:
[Round 2] 확장성이 핵심이군요. 현재 서버 구조와 향후 계획을 고려할 때:

1. "현재 단일 서버, 향후 다중 서버 예정"
2. "이미 다중 서버, Session 공유가 어려움"
3. "마이크로서비스 전환 계획 있음"
4. "토론 종료 / 정리해줘"

User: 1 (현재 단일, 향후 다중)

Claude:
[Round 3] 그렇다면 몇 가지 트레이드오프를 살펴보겠습니다.

JWT 장점: 서버 무상태, 수평 확장 용이, 별도 세션 저장소 불필요
JWT 단점: 토큰 무효화 어려움, 토큰 크기, 보안 관리 복잡

현재 단일 서버 상황에서 JWT가 즉시 필요할까요?

1. "당장은 아니지만 미리 준비하고 싶다"
2. "6개월 내 다중 서버 전환 예정"
3. "JWT의 다른 장점(모바일 등)도 필요"
4. "토론 종료 / 정리해줘"

User: 2 (6개월 내 전환)

Claude:
[Round 4] 6개월 내 전환이면 지금 JWT로 전환하는 것이 합리적일 수 있습니다.
구현 방식에 대해 논의해 볼까요?

1. "Access Token + Refresh Token 패턴"
2. "Redis 기반 토큰 블랙리스트 추가"
3. "점진적 마이그레이션 (Session → JWT)"
4. "토론 종료 / 정리해줘"

User: 4 (토론 종료)
```

### 4. 토론 요약

```
# 토론 요약: API 인증 방식 선택 (JWT vs Session)

**날짜**: 2026-03-04
**라운드 수**: 4
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)
1. JWT 전환 동기: 확장성 (서버 다중화 대비)
2. 현재 상황: 단일 서버 + express-session, 6개월 내 다중 서버 전환 예정
3. 트레이드오프: JWT(무상태/확장성) vs Session(단순성/즉시 무효화)

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | JWT 전환 진행 | 6개월 내 다중 서버 전환 예정이므로 선제 대응 | 논점 1, 2 |

## 미결 질문 (Open Questions)
- [ ] JWT 구현 패턴 (Access+Refresh vs 블랙리스트)
- [ ] 마이그레이션 전략 (빅뱅 vs 점진적)

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | JWT 구현 패턴 결정 (별도 토론 or feature-draft) | High | - |
| 2 | 마이그레이션 계획 수립 | Medium | - |

## 리서치 결과 요약 (Research Findings)
- 코드베이스 인증: Session 기반 (express-session), 3개 파일
- JWT vs Session 비교: 확장성에서 JWT 우위, 보안 관리 복잡도 증가

## 토론 흐름 (Discussion Flow)
Round 1: JWT 전환 동기 확인 → 확장성
Round 2: 현재 서버 구조 확인 → 단일, 향후 다중 예정
Round 3: 트레이드오프 분석 → 6개월 내 전환 계획
Round 4: 구현 방식 논의 → 토론 종료 (미결로 남김)
```
