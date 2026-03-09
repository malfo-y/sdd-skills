# Parallel Execution Algorithm

`implementation` 스킬의 병렬 실행 알고리즘, 충돌 감지 규칙, sub-agent 프로토콜을 정의합니다.

---

## 개요

순차 실행 대비 병렬 실행의 핵심 차이:

```
순차 실행 (implementation):
  Task 1 → Task 2 → Task 3 → Task 4 → ...
  (모든 task를 하나씩 처리)

병렬 실행 (implementation):
  Group 1: [Task 1, Task 2] (동시)  →  Group 2: [Task 3] → Group 3: [Task 4, Task 5] (동시) → ...
  (충돌 없는 task를 묶어서 동시 실행)
```

---

## 병렬화 알고리즘

### Phase 내 Task 병렬화 절차

```
For each phase:
  1. 의존성 그래프에서 unblocked task 식별
     - blockedBy에 pending/in_progress task가 없는 task

  2. Unblocked task 쌍의 Target Files 겹침 확인
     - 모든 unblocked task 쌍에 대해:
       Task A의 Target Files ∩ Task B의 Target Files
       - 교집합 없음 → 병렬 실행 가능
       - 교집합 있음 → 순차 실행 (우선순위 → ID 순)

  3. 병렬 그룹으로 묶기
     - 서로 충돌 없는 task들을 하나의 그룹으로
     - 충돌 있는 task는 별도 그룹 또는 순차 대기열로

  4. Task tool로 동시 spawn
     - 한 그룹의 모든 task를 동시에 Task tool 호출
     - 각 sub-agent에게 담당 task 정보 전달

  5. 모든 sub-agent 완료 후 통합 검증
     - 전체 테스트 실행
     - 충돌/회귀 확인

  6. 다음 그룹으로 이동
     - 완료된 task가 unblock하는 새 task 확인
     - 2단계부터 반복
```

### 그룹화 알고리즘 상세

```
function buildParallelGroups(unblockedTasks):
    groups = []
    remaining = copy(unblockedTasks)

    # 우선순위 순 정렬 (P0 > P1 > P2 > P3), 같으면 ID 순
    sort(remaining, by=[priority DESC, id ASC])

    while remaining is not empty:
        currentGroup = []
        usedFiles = {}  # 이 그룹에서 사용 중인 파일 집합

        for task in remaining:
            taskFiles = task.targetFiles

            # 현재 그룹의 파일과 겹침 확인
            if taskFiles ∩ usedFiles == ∅:
                currentGroup.append(task)
                usedFiles = usedFiles ∪ taskFiles

        groups.append(currentGroup)
        remaining = remaining - currentGroup

    return groups
```

### 예시

```markdown
## Phase 1 병렬화 예시

### Unblocked Tasks:
- Task 1 (P0): Target Files = {config.py, service_a.py, test_a.py}
- Task 2 (P0): Target Files = {service_b.py, test_b.py}
- Task 3 (P1): Target Files = {config.py, service_c.py, test_c.py}
- Task 4 (P1): Target Files = {service_d.py, test_d.py}

### 충돌 분석:
- Task 1 ∩ Task 2 = ∅ → 병렬 가능
- Task 1 ∩ Task 3 = {config.py} → 충돌!
- Task 2 ∩ Task 3 = ∅ → 병렬 가능
- Task 2 ∩ Task 4 = ∅ → 병렬 가능
- Task 3 ∩ Task 4 = ∅ → 병렬 가능

### 병렬 그룹:
- Group 1: [Task 1, Task 2, Task 4] (동시 실행)
- Group 2: [Task 3] (Task 1과 config.py 충돌이므로 Group 1 완료 후)
```

---

## 충돌 감지 규칙

### 1단계: 파일 수준 충돌

같은 파일 경로가 두 task의 Target Files에 모두 등장하면 충돌입니다.
마커 종류와 무관하게 **모든 조합이 충돌**입니다:

| 조합 | 이유 |
|------|------|
| `[C]` + `[C]` | 같은 파일을 두 agent가 동시 생성 |
| `[M]` + `[M]` | 같은 파일을 두 agent가 동시 수정 |
| `[C]` + `[M]` | 생성과 수정의 순서 의존성 |
| `[M]` + `[D]` | 수정 후 삭제 순서 의존성 |
| `[C]` + `[D]` | 생성과 삭제의 순서 의존성 |
| `[D]` + `[D]` | 중복 삭제 |

### 2단계: 의미적 충돌 (Semantic Conflict)

파일 경로가 겹치지 않아도 **의미적으로 충돌**하는 경우가 있습니다.
파일 수준 충돌 판정 후, 추가로 아래 패턴을 확인합니다:

| 패턴 | 예시 | 위험 |
|------|------|------|
| **공유 스키마/모델 의존** | Task A가 User 모델 생성, Task B가 User 모델을 import하는 서비스 생성 | Target Files는 다르지만, Task B는 Task A의 모델 구조에 의존 |
| **공유 설정/환경 변수** | Task A가 `DB_URL` 환경 변수 추가, Task B가 `DB_URL` 형식을 가정한 코드 작성 | 설정 계약(contract)이 암묵적으로 공유됨 |
| **공유 인터페이스/API 계약** | Task A가 `/api/users` 엔드포인트 생성, Task B가 해당 엔드포인트의 응답 형식을 가정 | API 계약 불일치 가능 |
| **공유 타입/상수 정의** | Task A가 상수 파일에 `MAX_RETRIES=3` 추가, Task B가 같은 상수를 다른 값으로 가정 | 타입/상수 충돌 |
| **마이그레이션 순서** | Task A, B 모두 DB 마이그레이션 생성 | 마이그레이션 번호 충돌, 실행 순서 문제 |

**의미적 충돌 감지 방법**:

```
For each pair of non-conflicting (파일 수준) tasks:
  1. Task A의 Acceptance Criteria/Technical Notes에서
     Task B의 Target Files에 대한 의존 언급이 있는지 확인
  2. Task A가 생성하는 모델/타입/상수를 Task B가 사용하는지 확인
  3. 두 task 모두 DB 마이그레이션을 생성하는지 확인
  4. 공유 설정 파일(env, config)에 대한 암묵적 의존이 있는지 확인

IF 의미적 충돌 발견:
  → 해당 task 쌍을 순차 실행으로 전환
  → 또는 사용자에게 확인 후 병렬 허용
```

**중요**: 의미적 충돌은 자동 감지가 불완전할 수 있습니다. 불확실한 경우 순차 실행이 안전합니다.

### 충돌 시 처리

```
충돌 발견 시 (파일 수준 또는 의미적):
  1. 해당 task 쌍 중 우선순위가 높은 task를 먼저 실행
  2. 우선순위가 같으면 ID가 작은 task를 먼저 실행
  3. 나머지 task는 다음 그룹에서 실행
  4. 충돌하지 않는 다른 task들은 여전히 병렬 실행 가능
```

---

## Sub-Agent 프로토콜

### Sub-Agent에게 전달하는 정보

각 sub-agent는 Task tool을 통해 다음 정보를 받습니다:

```markdown
## Task 정보
- Task ID, 제목, 설명
- Acceptance Criteria (전체)
- Technical Notes
- Target Files 목록 (수정 허용 범위)

## TDD 프로토콜
- Red-Green-Refactor 사이클 준수
- 각 Acceptance Criterion마다 테스트 먼저 작성

## 파일 경계 규칙
- Target Files에 명시된 파일만 생성/수정/삭제 가능
- 다른 파일은 읽기(Read)만 가능
- Target Files 외 파일 수정이 필요한 경우:
  → "Unplanned Dependency"로 보고하고 해당 파일은 수정하지 않음

## 환경 설정
- _sdd/env.md 내용 (있는 경우)
- 테스트 프레임워크 정보
- 프로젝트 컨벤션
```

### Sub-Agent 프롬프트 템플릿

```
당신은 구현 sub-agent입니다. 아래 task를 TDD 방식으로 구현하세요.

## 담당 Task
### Task {id}: {title}
**Component**: {component}
**Priority**: {priority}

**Description**:
{description}

**Acceptance Criteria**:
{acceptance_criteria}

**Technical Notes**:
{technical_notes}

## 수정 허용 파일 (Target Files)
{target_files_list}

## 규칙
1. **TDD 필수**: 각 Acceptance Criterion마다 RED → GREEN → REFACTOR
2. **파일 경계 준수**: 위의 Target Files만 생성/수정/삭제 가능
3. **Unplanned Dependency**: Target Files 외 파일 수정이 필요하면,
   수정하지 말고 다음 형식으로 보고:
   ```
   UNPLANNED_DEPENDENCY: {파일경로} - {필요한 변경 설명}
   ```
4. **테스트 실행**: 각 단계 후 테스트 실행
5. **완료 보고**: 모든 Acceptance Criteria 완료 후 결과 요약

## 환경
{env_setup}
{test_framework_info}
```

### Sub-Agent 완료 보고 형식

```markdown
## Task {id} 완료 보고

### 결과: SUCCESS / PARTIAL / FAILED

### TDD 진행 상황
| Criterion | RED | GREEN | REFACTOR | 상태 |
|-----------|-----|-------|----------|------|
| criterion 1 | ✓ | ✓ | ✓ | 완료 |
| criterion 2 | ✓ | ✓ | ✓ | 완료 |

### 생성/수정된 파일
- [C] `src/services/notification.py` (120 lines)
- [C] `tests/test_notification.py` (85 lines)

### 테스트 결과
- 새 테스트: 8개
- 전체 통과: Yes/No

### Unplanned Dependencies (있는 경우)
- UNPLANNED_DEPENDENCY: `src/utils/common.py` - retry_with_backoff 함수 필요

### 발견 사항
- [특이사항이나 주의 필요 사항]
```

---

## 통합 검증 (Post-Group Verification)

각 병렬 그룹 완료 후 메인 agent가 수행:

```
1. 전체 테스트 실행
   - 모든 sub-agent가 추가한 테스트 + 기존 테스트
   - 회귀 테스트 확인

2. Unplanned Dependency 처리
   - 보고된 unplanned dependency 수집
   - 메인 agent가 직접 해결하거나
   - 다음 그룹에 포함하여 처리

3. 충돌 확인
   - sub-agent가 Target Files 외 파일을 수정했는지 확인
   - 수정이 있으면 롤백 후 순차 재실행

4. 결과 통합
   - 각 sub-agent의 결과를 종합
   - Task 상태 업데이트 (completed / needs_retry)
   - 다음 그룹 준비
```

---

## 엣지 케이스 처리

### 1. Target Files 없는 계획

```
IF 계획에 Target Files 필드가 없으면:
  1. 각 task의 Description, Technical Notes에서 파일 경로 추론
  2. 코드베이스를 탐색하여 관련 파일 식별
  3. 추론한 Target Files를 사용자에게 확인 요청
  4. 확인 못 받으면 해당 phase는 순차 실행
```

### 2. Sub-agent 실패

```
IF sub-agent가 실패하면:
  1. 다른 동시 실행 중인 sub-agent에는 영향 없음
  2. 실패한 task는 그룹 완료 후 메인 agent가 순차 재시도
  3. 2번째 시도도 실패 시 사용자에게 보고
```

### 3. 예상 외 파일 필요 (Unplanned Dependency)

```
IF sub-agent가 Unplanned Dependency를 보고하면:
  1. 해당 sub-agent는 가능한 범위까지만 구현
  2. 그룹 완료 후 메인 agent가 unplanned dependency 해결
  3. 해결 후 미완료 부분 재실행 (순차)
```

### 4. 파일 충돌 감지 (런타임)

```
IF 실행 중 예상치 못한 파일 충돌 발생:
  1. 해당 task들만 중단
  2. 나머지 병렬 task는 계속 진행
  3. 중단된 task들은 순차로 재실행
```

### 5. 대규모 Phase (10+ unblocked tasks)

```
IF unblocked task가 10개 이상이면:
  1. 최대 동시 실행 수를 5로 제한
  2. 그룹 크기를 최대 5로 나누어 여러 그룹으로 분할
  3. 각 그룹은 기본 정책대로 "그룹 완료 대기 → 통합 검증 → 다음 그룹" 순서로 실행
  4. 통합 검증 없이 다음 그룹을 시작하지 않음 (회귀 방지)
```

> **Note**: 슬라이딩 윈도우(완료 즉시 다음 task 시작) 방식은 통합 검증을 건너뛰어
> 회귀 위험이 있으므로 사용하지 않습니다. 대신 그룹 크기 제한으로 대규모 phase를 처리합니다.

---

## 성능 최적화 팁

### 병렬화 효과가 큰 경우

- 독립적인 컴포넌트가 많은 Phase (예: 여러 서비스 동시 구현)
- 테스트 작성 task들 (서로 다른 모듈의 테스트)
- [C] 마커가 대부분인 Phase (새 파일 생성 위주)

### 병렬화 효과가 적은 경우

- 대부분의 task가 같은 파일을 수정하는 Phase
- 강한 순서 의존성이 있는 task 체인
- 단일 task만 있는 Phase

### 권장 사항

- Phase 설계 시 task 간 Target Files 중복을 최소화하면 병렬화 효과 극대화
- `feature-draft` 또는 `implementation-plan`에서 Target Files를 잘 설계하면 `implementation`의 병렬화가 자연스럽게 최적화됨
