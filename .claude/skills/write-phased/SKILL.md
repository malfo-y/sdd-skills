---
name: write-phased
description: Use this skill when the user asks to write, create, or generate a long document or code file. Triggers on "write-phased", "긴 문서 작성", "코드 파일 생성", "큰 파일 작성", or when a writing task is structurally complex (3+ sections, 5+ functions). Applies a 2-phase strategy: skeleton first, then fill.
version: 1.0.0
---

# write-phased — 2-Phase Writing Strategy

구조적으로 복잡한 문서나 코드 파일을 작성할 때, 한 번에 전체를 쓰지 않고 **Phase 1 (Skeleton)** → **Phase 2 (Fill)** 2단계로 나누어 작성한다.

## When to Apply

구조적 복잡도가 높을 때 자동 적용한다. 줄 수가 아니라 구조로 판단:

| 유형 | 적용 기준 |
|------|----------|
| 문서 (Markdown 등) | 섹션 3개 이상 또는 전체 분량이 상당할 때 |
| 코드 | 함수/메서드 5개 이상 또는 클래스 2개 이상 |
| 기존 파일 대규모 추가 | 추가할 내용이 위 기준을 충족할 때 |

짧고 단순한 파일은 그냥 Write로 한 번에 작성한다.

## Hard Rules

1. **Phase 1에서 반드시 파일에 저장**: skeleton을 컨텍스트에만 두지 말고, 대상 파일에 Write로 저장한다.
2. **Phase 2는 Edit으로 교체**: skeleton의 각 섹션/TODO를 Edit 도구로 하나씩 채운다. Write로 전체를 덮어쓰지 않는다.
3. **Phase 1 → 2 자동 진행**: skeleton 작성 후 사용자 확인 없이 바로 Phase 2를 시작한다.
4. **마커 정리**: Phase 2 완료 후 모든 `<!-- Phase 2 -->`, `# TODO: Phase 2` 등의 마커를 제거한다.
5. **언어 규칙**: 사용자 요청 언어를 따른다.

## Phase 1: Skeleton

전체 구조를 잡아 파일에 저장한다. 상세 내용은 비워둔다.

### 문서 Skeleton 템플릿

```markdown
## §N [Section Title]

**요약**: [핵심 내용 1-2줄]
**다룰 내용**: [이 섹션에서 상세히 다룰 토픽 나열]

<!-- Phase 2 -->
```

### 코드 Skeleton 가이드라인

언어/맥락에 맞게 유연하게 적용한다. 공통 원칙:

- 함수/메서드 시그니처 (이름, 파라미터, 리턴 타입) 정의
- 클래스/모듈 구조 배치
- 타입, 인터페이스, 데이터 모델은 Phase 1에서 완성해도 좋음
- 함수 본문은 `pass`, `throw new Error("TODO")`, `// TODO: Phase 2` 등으로 비워둠

## Phase 2: Fill

skeleton의 각 섹션을 Edit 도구로 하나씩 채운다.

### 실행 순서

1. **의존 섹션 순차 처리**: 뒤의 섹션이 앞의 내용에 의존하면 순서대로 채운다.
2. **독립 섹션 병렬 가능**: 서로 독립적인 섹션은 Agent 병렬 실행으로 채울 수 있다.

### 다중 파일

요청이 여러 파일을 필요로 하면:
1. 모든 파일의 skeleton을 먼저 작성 (Phase 1)
2. 파일 간 의존 관계를 고려해 Phase 2 순서를 결정
3. 독립적인 파일들은 병렬로 채우기 가능

## Examples

### 문서 예시

**Phase 1** — skeleton 저장:
```markdown
# API 인증 가이드

## §1 개요

**요약**: JWT 기반 인증 시스템의 사용법
**다룰 내용**: 인증 흐름, 토큰 구조, 만료 정책

<!-- Phase 2 -->

## §2 빠른 시작

**요약**: 5분 만에 인증 연동하기
**다룰 내용**: 설치, 초기 설정, 첫 번째 토큰 발급

<!-- Phase 2 -->

## §3 상세 API 레퍼런스

**요약**: 모든 인증 엔드포인트 설명
**다룰 내용**: login, logout, refresh, verify 엔드포인트

<!-- Phase 2 -->
```

**Phase 2** — Edit으로 각 섹션 채우기:
```
Edit(old_string="**다룰 내용**: 인증 흐름, ...\n\n<!-- Phase 2 -->",
     new_string="본 시스템은 JWT 기반 Bearer 인증을 사용합니다.\n\n### 인증 흐름\n...")
```

### 코드 예시

**Phase 1** — skeleton 저장:
```python
from dataclasses import dataclass

@dataclass
class Token:
    access: str
    refresh: str
    expires_at: int

class AuthService:
    """JWT 인증 서비스"""

    def __init__(self, secret: str, expiry: int = 3600):
        # TODO: Phase 2
        pass

    def login(self, email: str, password: str) -> Token:
        # TODO: Phase 2
        pass

    def verify(self, token: str) -> dict:
        # TODO: Phase 2
        pass
```

**Phase 2** — Edit으로 각 함수 채우기:
```
Edit(old_string="    def login(self, email: str, password: str) -> Token:\n        # TODO: Phase 2\n        pass",
     new_string="    def login(self, email: str, password: str) -> Token:\n        user = self._find_user(email)\n        if not user or not user.check_password(password):\n            raise AuthError(\"Invalid credentials\")\n        return self._generate_token(user)")
```
