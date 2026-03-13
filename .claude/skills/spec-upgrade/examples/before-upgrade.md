# Example: Before Upgrade (구 형식 스펙)

이 예시는 whitepaper 형식 이전에 작성된 전형적인 구 형식 스펙입니다.
서사 섹션(배경/동기, 핵심 설계, 사용 가이드)이 빠져 있고, 코드 citation이 없습니다.

---

# TaskRunner

> CLI 기반 태스크 자동화 도구

## 개요

TaskRunner는 YAML 파일로 태스크를 정의하고 실행하는 CLI 도구입니다.
병렬 실행, 의존성 관리, 로깅을 지원합니다.

## 주요 기능

- YAML 기반 태스크 정의
- 병렬 태스크 실행
- 의존성 그래프 해석
- 실행 로그 관리

## 아키텍처

```
CLI → Parser → Scheduler → Executor → Logger
```

### 기술 스택

- Python 3.11
- Click (CLI 프레임워크)
- PyYAML
- asyncio

## 컴포넌트

### Parser

YAML 파일을 파싱하여 태스크 그래프를 생성합니다.

- 입력: YAML 파일 경로
- 출력: TaskGraph 객체
- 주요 파일: `src/parser.py`

### Scheduler

태스크 실행 순서를 결정합니다. 위상 정렬을 사용합니다.

- 입력: TaskGraph
- 출력: 실행 순서 리스트
- 주요 파일: `src/scheduler.py`

### Executor

태스크를 실행합니다. asyncio 기반 병렬 실행을 지원합니다.

- 입력: 실행 순서 리스트
- 출력: ExecutionResult
- 주요 파일: `src/executor.py`

### Logger

실행 결과를 로그 파일에 기록합니다.

- 입력: ExecutionResult
- 출력: 로그 파일
- 주요 파일: `src/logger.py`

## 데이터 모델

### Task

```python
class Task:
    name: str
    command: str
    depends_on: List[str]
    timeout: Optional[int]
```

### TaskGraph

```python
class TaskGraph:
    tasks: Dict[str, Task]
    edges: List[Tuple[str, str]]
```

## 설정

### 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| TASKRUNNER_LOG_DIR | 로그 디렉토리 | ./logs |
| TASKRUNNER_MAX_PARALLEL | 최대 병렬 수 | 4 |

### 디렉토리 구조

```
taskrunner/
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── parser.py
│   ├── scheduler.py
│   ├── executor.py
│   └── logger.py
├── tests/
│   ├── test_parser.py
│   ├── test_scheduler.py
│   └── test_executor.py
├── pyproject.toml
└── README.md
```

## 의존성

```toml
[project.dependencies]
click = "^8.0"
pyyaml = "^6.0"
```
