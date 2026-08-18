# Sample Discussion Session

이 예제는 "API 인증 방식 선택" 토픽에 대한 Codex discussion 스킬 실행 세션을 보여준다.

언어 규칙:
- 아래 예시는 한국어 세션이다.
- 사용자가 영어로 "Let's discuss JWT vs session auth"처럼 시작하면 질문, 중간 요약, 최종 저장 파일도 영어로 작성한다.
- 사용자가 토론 중 다른 언어로 전환하면 이후 대화와 저장 파일도 그 언어를 따른다.

## Session Flow

### 1. 토픽 선택

```text
User: discussion으로 API 인증 방식을 같이 검토하자

Assistant: 구조화된 토론으로 진행합니다. 먼저 범위를 좁히겠습니다.

request_user_input
- header: focus
- question: "이번 토론에서 먼저 정할 축은 무엇인가요?"
- options:
  1. "구조 선택" - JWT vs Session의 구조적 차이를 먼저 본다
  2. "전환 비용" - 현재 코드에서 마이그레이션 비용을 먼저 본다
  3. "정리/종료" - 지금까지 전제로 바로 정리한다

User: 구조 선택
```

### 2. 맥락 수집

```text
Assistant:
관련 맥락을 수집 중입니다...

- 로컬 코드베이스에서 현재 인증 관련 파일 탐색
- 공식 문서/1차 자료 기준으로 JWT vs Session 비교

## 수집된 맥락
| 항목 | 내용 |
|------|------|
| 현재 인증 | Session 기반 |
| 관련 파일 | 3개 식별 |
| 외부 참고 | JWT/Session 비교 자료 확보 |
| 확인이 필요한 쟁점 | 토큰 무효화 전략 |
```

### 3. 반복 토론

```text
Assistant:
request_user_input
- header: reason
- question: "JWT 전환을 고려하는 가장 큰 이유는 무엇인가요?"
- options:
  1. "확장성" - 서버 다중화나 서비스 분리를 대비한다
  2. "클라이언트 다양성" - 모바일 앱/외부 클라이언트 대응이 필요하다
  3. "정리/종료" - 지금까지 논의만 정리한다

User: 확장성

Assistant:
request_user_input
- header: timing
- question: "확장성 요구가 현실화되는 시점은 언제에 가깝나요?"
- options:
  1. "단기" - 6개월 내 다중 서버 전환이 예상된다
  2. "중장기" - 아직 계획 단계라 당장 전환은 이르다
  3. "정리/종료" - 여기서 정리한다

User: 단기

Assistant:
request_user_input
- header: risk
- question: "지금 판단이 틀릴 수 있는 가장 큰 실패 시나리오는 무엇에 가깝나요?"
- options:
  1. "전환 시점 오판" - 다중 서버 전환이 늦어져 JWT 전환이 오버엔지니어링이 된다
  2. "운영 복잡도 증가" - 토큰 무효화/보안 운영이 예상보다 부담된다
  3. "정리/종료" - 여기까지 정리한다

User: 운영 복잡도 증가

Assistant:
현재까지 기준이면 확장성 필요는 명확하지만, 운영 복잡도에 대한 새 결정 정보는 아직 늘지 않았습니다.

request_user_input
- header: stall
- question: "새 정보가 크게 늘지 않고 있습니다. 어떻게 진행할까요?"
- options:
  1. "지금까지 정리" - 현재 결정과 미결 질문을 문서로 남긴다
  2. "미결 1개만 더 논의" - 마이그레이션 전략 하나만 더 본다
  3. "정리/종료" - 바로 여기서 끝낸다

User: 지금까지 정리
```

### 4. 토론 요약

```markdown
# 토론 요약: API 인증 방식 선택 (JWT vs Session)

**날짜**: 2026-03-10
**라운드 수**: 4
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)
1. JWT 전환 동기: 확장성 확보
2. 현재 상황: Session 기반이며 단기 확장 계획 존재
3. 비판적 검토: 운영 복잡도와 토큰 무효화 부담이 핵심 리스크
4. 후속 결정 필요: JWT 패턴과 마이그레이션 전략

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | JWT 전환 검토를 우선 과제로 둔다 | 단기 확장 계획이 존재하고, 주요 리스크는 운영 복잡도로 식별됨 | 논점 1, 2, 3 |

## 미결 질문 (Open Questions)
- [ ] JWT 구현 패턴
- [ ] 마이그레이션 순서

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | JWT 패턴 결정 | High | - |
| 2 | 마이그레이션 계획 수립 | Medium | - |

## 리서치 결과 요약 (Research Findings)
- 코드베이스 인증: Session 기반, 관련 파일 3개 식별
- JWT vs Session 비교: 확장성 측면에서 JWT가 유리하나 토큰 무효화 전략이 추가 쟁점으로 남음

## 토론 흐름 (Discussion Flow)
Round 1: JWT 전환 이유 확인 -> 확장성
Round 2: 확장성 요구 시점 확인 -> 단기 전환 가능성
Round 3: 비판적 검토 -> 운영 복잡도 증가가 핵심 리스크
Round 4: stagnation 감지 후 종료 유도 -> 현재까지 정리
```
