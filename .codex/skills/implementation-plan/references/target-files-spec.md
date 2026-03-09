# Target Files Specification

병렬 실행 스킬에서 사용하는 **Target Files** 필드의 상세 스펙입니다.
이 필드는 각 task가 수정하는 파일 목록을 명시하여, 병렬 실행 시 파일 충돌을 사전에 감지합니다.

---

## 목적

1. **충돌 감지**: 병렬 실행 전 task 간 파일 겹침을 확인
2. **Sub-agent 경계 설정**: 각 sub-agent가 수정 가능한 파일을 제한
3. **변경 추적**: 어떤 task가 어떤 파일을 어떻게 변경하는지 명시

---

## 문법

```markdown
**Target Files**:
- [마커] `파일경로` -- 설명
```

### 마커 (Operation Markers)

| 마커 | 의미 | 설명 |
|------|------|------|
| `[C]` | Create | 새로 생성하는 파일 |
| `[M]` | Modify | 기존 파일 수정 |
| `[D]` | Delete | 파일 삭제 |

### 예시

```markdown
**Target Files**:
- [C] `src/services/notification.py` -- NotificationService 클래스
- [M] `src/config/settings.py` -- 알림 설정 추가
- [C] `tests/test_notification.py` -- 단위 테스트
- [D] `src/services/old_notifier.py` -- 레거시 알림 모듈 제거
```

---

## 규칙

### 1. 필수 포함 항목

모든 task에 다음을 포함해야 합니다:

- **소스 파일**: 실제 구현 코드 파일
- **테스트 파일**: 해당 task에서 생성/수정하는 테스트 파일
- **설정 파일**: 변경이 필요한 설정 파일 (있는 경우)

### 2. 경로 형식

- 프로젝트 루트 기준 상대 경로 사용
- 백틱(`` ` ``)으로 감싸기
- 설명은 `--` 구분자 뒤에 작성

### 3. 디렉토리 vs 파일

- **파일 단위**로 명시 (디렉토리 단위 X)
- 파일이 아직 존재하지 않으면 `[C]` 마커 사용
- 와일드카드(`*`) 사용 불가

### 4. 충돌 판정 규칙

두 task의 Target Files가 겹칠 때:

| Task A 마커 | Task B 마커 | 같은 파일 | 충돌 여부 |
|-------------|-------------|-----------|-----------|
| `[C]` | `[C]` | 같은 경로 | **충돌** (둘 다 생성 시도) |
| `[M]` | `[M]` | 같은 경로 | **충돌** (동시 수정) |
| `[C]` | `[M]` | 같은 경로 | **충돌** (생성 vs 수정 의미 불일치) |
| `[M]` | `[D]` | 같은 경로 | **충돌** (수정 vs 삭제) |
| `[C]` | `[D]` | 같은 경로 | **충돌** |
| `[D]` | `[D]` | 같은 경로 | **충돌** (중복 삭제) |
| 아무 마커 | 아무 마커 | **다른 경로** | 충돌 없음 |

**핵심 원칙**: 같은 파일에 대해 어떤 조합이든 동시 접근이 있으면 충돌입니다.

### 5. 읽기 전용 참조

Target Files에 포함되지 않은 파일은 **읽기만 가능**합니다.
Sub-agent는 코드베이스의 다른 파일을 참조(read)할 수 있지만, 수정은 Target Files에 명시된 파일만 가능합니다.

---

## Task 템플릿에서의 위치

```markdown
### Task [ID]: [제목]
**Component**: [컴포넌트]
**Priority**: [P0-P3]
**Type**: [Feature | Bug | Refactor | Research | Infrastructure | Test]

**Description**:
[설명]

**Acceptance Criteria**:
- [ ] [기준 1]
- [ ] [기준 2]

**Target Files**:
- [C] `src/services/new_service.py` -- 새 서비스 클래스
- [M] `src/config/settings.py` -- 설정 항목 추가
- [C] `tests/test_new_service.py` -- 단위 테스트

**Technical Notes**:
- [구현 힌트]

**Dependencies**: [의존 task ID]
```

---

## Target Files가 없는 경우 (하위 호환)

기존 (비-parallel) 계획에는 Target Files가 없을 수 있습니다.

`implementation` 스킬은 이 경우 다음과 같이 처리합니다:

1. **코드베이스에서 추론**: Task의 Description, Technical Notes, Acceptance Criteria를 분석하여 예상 파일 목록 추론
2. **신뢰도 판정**: 추론 결과를 high / low confidence로 나눈다
3. **불확실하면 순차 실행**: low confidence면 해당 task들은 순차로 실행하고 근거를 `Open Questions`나 plan note에 남긴다

```
IF Target Files 존재:
    → 병렬화 알고리즘 적용
ELSE IF 코드베이스에서 추론 가능:
    → high confidence면 병렬화, low confidence면 순차 실행
ELSE:
    → 순차 실행 폴백
```

---

## 좋은 Target Files 작성 가이드

### Good

```markdown
**Target Files**:
- [C] `src/services/notification_service.py` -- NotificationService 클래스
- [M] `src/config/settings.py` -- NOTIFICATION_WEBHOOK_SLACK 설정 추가
- [C] `tests/services/test_notification_service.py` -- 알림 서비스 단위 테스트
```

- 구체적인 파일 경로
- 각 파일이 왜 변경되는지 설명
- 테스트 파일 포함

### Bad

```markdown
**Target Files**:
- [M] `src/` -- 소스 코드 수정
- [C] `tests/` -- 테스트 추가
```

- 디렉토리 단위 (파일 단위여야 함)
- 설명이 모호
- 충돌 감지 불가능
