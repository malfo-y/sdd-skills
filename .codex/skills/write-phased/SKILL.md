---
name: write-phased
description: This skill should be used when the user asks to "write-phased", "문서 작성", "작성해줘", "만들어줘", "코드 작성", "파일 생성", "구현해줘", "write a document", "create a file", "generate code", "implement", or any request to produce a markdown document, code file, config file, or technical writing. Applies a 2-phase strategy: skeleton first, then fill.
version: 1.0.0
---

# write-phased: 2-Phase Writing Strategy

긴 문서나 큰 코드 파일을 한 번에 완성하지 않고, **Phase 1 (Skeleton)** -> **Phase 2 (Fill)** 로 나눠 작성한다. 핵심은 먼저 파일에 골조를 저장하고, 그 다음 섹션/함수 단위로 채워 넣는 것이다.

## When to Use

구조적 복잡도가 높을 때 적용한다. 줄 수보다 구조를 본다.

| 유형 | 적용 기준 |
|------|----------|
| 문서 | 섹션 3개 이상, 하위 섹션이 많음, 표/예시/레퍼런스를 포함한 장문 초안 |
| 코드 | 함수/메서드 5개 이상, 클래스/모듈 2개 이상, 여러 타입/인터페이스와 연결된 신규 파일 |
| 기존 파일 대규모 확장 | 새 섹션/함수 묶음을 크게 추가해야 할 때 |

다음 경우는 보통 이 스킬을 쓰지 않는다:

- 짧은 메모, 간단한 README 수정, 함수 1-2개 추가 같은 소규모 작업
- 이미 거의 완성된 파일의 국소 수정

### Trigger Phrases

- "write-phased"
- "긴 문서 작성"
- "큰 파일 작성"
- "코드 파일 생성"
- "골조부터 작성"
- "skeleton first"
- "이 파일을 먼저 틀 잡고 채워 줘"

## Hard Rules

1. **Phase 1 결과를 실제 파일에 저장**: 골조는 컨텍스트 메모가 아니라 대상 파일의 초안이어야 한다.
2. **Phase 2는 in-place patch 원칙**: Phase 1 이후에는 전체 파일을 다시 쓰지 말고 `apply_patch` 같은 섹션 단위 수정으로 채운다.
3. **자동 진행**: 특별한 위험이 없으면 Phase 1 후 사용자 승인 없이 Phase 2로 바로 진행한다.
4. **마커 정리**: `<!-- Phase 2 -->`, `TODO: Phase 2`, `pass` 같은 임시 마커는 최종본에서 제거하거나 실제 구현으로 대체한다.
5. **언어 규칙**: 사용자 요청 언어를 따른다. 명시가 없으면 주변 문서/코드의 언어를 따른다.
6. **다중 파일도 동일 규칙**: 여러 파일이 필요하면 먼저 모든 파일의 skeleton을 만들고, 이후 의존 순서대로 채운다.

## Process

### Step 1: Decide Whether Phased Writing Is Needed

- 산출물이 구조적으로 큰지 판단한다.
- 관련 파일과 기존 패턴을 읽고 목표 섹션/함수 목록을 잡는다.
- 독립 섹션이 있으면 조사나 초안 메모는 병렬화할 수 있지만, 실제 파일 patch는 충돌 없이 적용한다.

### Step 2: Build the Skeleton

- 제목, 섹션 헤더, 함수 시그니처, 타입/인터페이스, 핵심 TODO만 남긴다.
- 문서 skeleton은 각 섹션의 요약과 다룰 내용을 1-2줄씩 적는다.
- 코드 skeleton은 구조와 계약(interface/signature)을 먼저 고정한다.
- Phase 2 마커를 남겨 나중에 안전하게 치환할 수 있게 한다.

#### Document Skeleton Template

```markdown
## §N [Section Title]

**요약**: [핵심 내용 1-2줄]
**다룰 내용**: [세부 토픽 나열]

<!-- Phase 2 -->
```

#### Code Skeleton Guidelines

- import / type / interface / data model은 Phase 1에서 확정해도 좋다.
- 함수/메서드 시그니처는 최대한 정확히 잡는다.
- 본문은 `pass`, `raise NotImplementedError`, `throw new Error("TODO")`, `// TODO: Phase 2` 등으로 비워 둔다.
- 복잡한 내부 로직은 주석 1-2줄로 의도를 남긴다.

### Step 3: Fill Section by Section

- 저장된 skeleton을 다시 읽고, 섹션/함수 단위로 채운다.
- 앞부분에 의존하는 내용은 순차적으로 작성한다.
- 독립적인 섹션은 초안 준비를 병렬화해도 되지만, 최종 patch는 충돌을 피해서 적용한다.
- 문서는 skeleton의 `요약/다룰 내용`을 실제 설명, 예시, 표, 레퍼런스로 확장한다.
- 코드는 placeholder를 실제 로직, 에러 처리, 테스트 가능한 구조로 바꾼다.

### Step 4: Finalize

- Phase 2 마커가 남지 않았는지 확인한다.
- skeleton만 있고 비어 있는 섹션이 없는지 확인한다.
- 다중 파일이면 파일 간 이름, import, 참조 관계를 마지막에 교차 검증한다.

## Multi-File Strategy

요청이 여러 파일에 걸치면:

1. 모든 대상 파일의 skeleton을 먼저 생성한다.
2. 공통 타입, 기반 모듈, shared helper처럼 선행 의존성이 큰 파일부터 채운다.
3. 의존성이 낮은 파일은 조사나 초안 단계를 병렬화한다.
4. 마지막에 import, 링크, 참조 경로를 한 번에 검증한다.

## Examples

### Document Example

**Phase 1 - skeleton saved to file**

```markdown
# API 인증 가이드

## §1 개요

**요약**: JWT 기반 인증 시스템의 사용법
**다룰 내용**: 인증 흐름, 토큰 구조, 만료 정책

<!-- Phase 2 -->

## §2 빠른 시작

**요약**: 5분 안에 인증 연동하기
**다룰 내용**: 설치, 초기 설정, 첫 토큰 발급

<!-- Phase 2 -->

## §3 API 레퍼런스

**요약**: 인증 엔드포인트 설명
**다룰 내용**: login, logout, refresh, verify

<!-- Phase 2 -->
```

**Phase 2 - fill by patching sections**

- §1을 전체 흐름 설명으로 확장
- §2를 단계별 빠른 시작으로 확장
- §3을 요청/응답 예시와 에러 케이스로 확장

### Code Example

**Phase 1 - skeleton saved to file**

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
        raise NotImplementedError

    def login(self, email: str, password: str) -> Token:
        # TODO: Phase 2
        raise NotImplementedError

    def verify(self, token: str) -> dict:
        # TODO: Phase 2
        raise NotImplementedError
```

**Phase 2 - replace placeholders**

- `__init__`: 설정값 검증 및 내부 상태 초기화
- `login`: 사용자 검증 후 토큰 발급
- `verify`: 토큰 파싱, 만료 검사, claims 반환

## Success Criteria

- Phase 1에서 실제 파일에 skeleton이 저장된다.
- Phase 2에서 섹션/함수 단위 patch로 내용이 채워진다.
- 최종 결과물에 Phase 마커나 placeholder만 남은 블록이 없다.
- 큰 산출물일수록 구조가 먼저 안정되고, 후속 수정 diff가 읽기 쉬워진다.
