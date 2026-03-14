# Example: After Upgrade (Whitepaper 형식 스펙)

이 예시는 `before-upgrade.md`의 구 형식 스펙을 whitepaper §1-§8 구조로 변환한 결과입니다.
서사 섹션(§1, §2, §5)이 추가되고, 코드 citation이 삽입되었습니다.

---

# TaskRunner

> CLI 기반 태스크 자동화 도구 — YAML 정의 파일로 의존성 있는 태스크를 병렬 실행

**Version**: 1.0.0
**Last Updated**: 2026-03-13
**Status**: Approved

## Table of Contents

- [Background & Motivation](#background--motivation)
- [Core Design](#core-design)
- [Architecture Overview](#architecture-overview)
- [Component Details](#component-details)
- [Usage Guide & Expected Results](#usage-guide--expected-results)
- [Data Models](#data-models)
- [Environment & Dependencies](#environment--dependencies)
- [Appendix: Code Reference Index](#appendix-code-reference-index)

---

## Background & Motivation

### Problem Statement

소프트웨어 프로젝트에서 빌드, 테스트, 배포 등 반복 태스크는 서로 의존 관계를 가진다. 기존 Makefile이나 쉘 스크립트로 이를 관리하면 의존성이 암묵적이고, 병렬 실행이 어렵고, 실행 결과 추적이 불편하다.

### Why This Approach

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| TaskRunner (YAML + DAG) | 선언적 정의, 자동 병렬화, 실행 로그 | 학습 비용 | **Chosen** |
| Makefile | 범용, 설치 불필요 | 의존성 암묵적, 병렬 제어 어려움 | Rejected: 복잡한 의존성 표현 한계 |
| Shell script | 단순, 직관적 | 의존성 관리 불가, 로깅 수동 | Rejected: 확장성 부족 |

### Core Value Proposition

TaskRunner는 태스크 간 의존성을 YAML로 선언하면, DAG 기반 위상 정렬로 실행 순서를 자동 결정하고, asyncio 병렬 실행으로 최적 처리 시간을 달성한다. 실행 결과는 구조화된 로그로 자동 추적된다.

### Primary Objective

YAML 파일 하나로 복잡한 태스크 의존성을 정의하고, 안전하게 병렬 실행하며, 결과를 추적할 수 있는 CLI 도구 제공.

### Key Features

1. **YAML 기반 태스크 정의**: 선언적으로 태스크와 의존 관계를 기술
2. **병렬 태스크 실행**: asyncio 기반으로 독립 태스크를 동시 실행
3. **의존성 그래프 해석**: DAG 위상 정렬로 안전한 실행 순서 보장
4. **실행 로그 관리**: 태스크별 실행 결과, 소요 시간, 오류를 구조화 기록

---

## Core Design

### Key Idea

TaskRunner의 핵심 아이디어는 태스크 실행을 "선언 → 정렬 → 실행 → 기록"의 4단계 파이프라인으로 분리하는 것이다.

사용자가 YAML로 태스크와 의존성을 선언하면, Parser가 이를 DAG(Directed Acyclic Graph)로 변환한다. Scheduler는 이 DAG를 위상 정렬하여 실행 순서를 결정하되, 의존성이 없는 태스크들을 병렬 실행 가능한 그룹으로 묶는다. Executor는 각 그룹 내 태스크를 asyncio로 동시 실행하고, Logger가 결과를 구조화하여 기록한다.

이 분리 덕분에 각 단계를 독립적으로 테스트하고 교체할 수 있다. 예를 들어 Scheduler의 정렬 알고리즘을 바꿔도 Parser나 Executor에 영향이 없다.

### Algorithm / Logic Flow

핵심 실행 흐름은 CLI 진입점 `[src/cli.py:run]`에서 시작한다:

```python
# [src/cli.py:run]
@click.command()
@click.argument('taskfile', type=click.Path(exists=True))
def run(taskfile: str):
    """Execute tasks defined in YAML file."""
    graph = Parser.parse(taskfile)
    schedule = Scheduler.topological_sort(graph)
    result = asyncio.run(Executor.execute(schedule))
    Logger.log(result)
```

Scheduler의 위상 정렬 `[src/scheduler.py:topological_sort]`이 핵심 알고리즘이다. Kahn's algorithm을 사용하여 O(V+E) 시간 복잡도로 실행 순서를 결정하면서, 동시 실행 가능한 태스크를 그룹으로 묶는다:

```python
# [src/scheduler.py:topological_sort]
@staticmethod
def topological_sort(graph: TaskGraph) -> List[List[Task]]:
    """Return execution groups in dependency order."""
    in_degree = {t: 0 for t in graph.tasks}
    for src, dst in graph.edges:
        in_degree[dst] += 1

    groups = []
    ready = [t for t, d in in_degree.items() if d == 0]

    while ready:
        groups.append([graph.tasks[t] for t in ready])
        next_ready = []
        for t in ready:
            for src, dst in graph.edges:
                if src == t:
                    in_degree[dst] -= 1
                    if in_degree[dst] == 0:
                        next_ready.append(dst)
        ready = next_ready

    return groups
```

### Design Rationale

| Design Choice | Rationale | Alternatives Considered |
|---------------|-----------|------------------------|
| 4단계 파이프라인 분리 | 각 단계 독립 테스트/교체 가능 | 단일 함수 (rejected: 테스트 어려움) |
| Kahn's algorithm | 그룹 단위 병렬화에 적합 | DFS (rejected: 그룹 추출 불편) |
| asyncio 병렬 실행 | 단일 프로세스로 충분한 I/O 병렬성 | multiprocessing (rejected: 오버헤드) |

---

## Architecture Overview

### System Diagram

```
┌────────┐     ┌─────────┐     ┌───────────┐     ┌──────────┐     ┌────────┐
│  CLI   │────▶│ Parser  │────▶│ Scheduler │────▶│ Executor │────▶│ Logger │
│        │     │         │     │           │     │          │     │        │
│ Click  │     │ YAML→   │     │ DAG→      │     │ async    │     │ file   │
│ args   │     │ TaskGraph│     │ Groups    │     │ execute  │     │ output │
└────────┘     └─────────┘     └───────────┘     └──────────┘     └────────┘
```

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Runtime | Python | 3.11+ | Primary language, asyncio support |
| CLI | Click | 8.0+ | Command-line interface framework |
| Config | PyYAML | 6.0+ | YAML task definition parsing |
| Async | asyncio | stdlib | Parallel task execution |

---

## Component Details

### Component: Parser

#### Overview

YAML 파일을 파싱하여 TaskGraph 객체를 생성한다.

#### Why

태스크 정의(YAML)와 실행 로직(Scheduler/Executor)을 분리하여, 입력 형식을 독립적으로 검증하고 변경할 수 있도록 했다. 향후 TOML이나 JSON 입력을 추가할 때 Parser만 교체하면 된다.

#### Responsibility

- Primary: YAML 파일을 읽어 TaskGraph로 변환
- Secondary: 스키마 유효성 검증, 순환 의존성 사전 탐지

#### Source

- `src/parser.py`: Parser.parse(), validate_schema()

#### Dependencies

| Dependency | Type | Purpose | Why |
|------------|------|---------|-----|
| PyYAML | External | YAML 파싱 | YAML은 사람이 읽기 편한 태스크 정의 형식이므로 |

---

### Component: Scheduler

#### Overview

TaskGraph를 위상 정렬하여 병렬 실행 가능한 그룹 순서를 결정한다.

#### Why

의존성 해석과 실행을 분리하여, 스케줄링 알고리즘을 독립적으로 테스트하고 최적화할 수 있도록 했다. 또한 dry-run 모드에서 실행 없이 실행 계획만 보여줄 수 있다.

#### Responsibility

- Primary: DAG 위상 정렬, 병렬 그룹 생성
- Secondary: 순환 의존성 탐지, 실행 계획 출력

#### Source

- `src/scheduler.py`: Scheduler.topological_sort(), detect_cycles()

#### Dependencies

| Dependency | Type | Purpose | Why |
|------------|------|---------|-----|
| Parser | Internal | TaskGraph 입력 | 파싱된 DAG를 받아 정렬하기 위해 |

---

### Component: Executor

#### Overview

Scheduler가 결정한 순서대로 태스크를 asyncio 기반으로 병렬 실행한다.

#### Why

실행 엔진을 분리하여, 동기/비동기 실행 전략을 교체할 수 있도록 했다. 또한 실행 제한(timeout, max_parallel)을 Executor 내부에서 일괄 관리한다.

#### Responsibility

- Primary: 태스크 그룹 병렬 실행, timeout 관리
- Secondary: 실패 시 중단/계속 정책 적용

#### Source

- `src/executor.py`: Executor.execute(), run_task(), handle_timeout()

#### Dependencies

| Dependency | Type | Purpose | Why |
|------------|------|---------|-----|
| Scheduler | Internal | 실행 순서 입력 | 정렬된 그룹 순서대로 실행하기 위해 |
| asyncio | Stdlib | 비동기 실행 | 단일 프로세스로 I/O 병렬성 확보 |

---

### Component: Logger

#### Overview

실행 결과를 구조화된 로그 파일로 기록한다.

#### Why

실행 결과 추적을 별도 컴포넌트로 분리하여, 로그 형식(JSON, 텍스트 등)을 독립적으로 변경할 수 있도록 했다. 또한 Executor가 로깅 로직에 의존하지 않는다.

#### Responsibility

- Primary: 태스크별 실행 결과, 소요 시간, 오류 기록
- Secondary: 로그 로테이션, 요약 출력

#### Source

- `src/logger.py`: Logger.log(), format_result(), rotate_logs()

---

## Usage Guide & Expected Results

### Scenario 1: Basic Task Execution

**Setup:**
```bash
pip install taskrunner
```

태스크 파일 `tasks.yaml` 작성:
```yaml
tasks:
  lint:
    command: "ruff check src/"
  test:
    command: "pytest tests/"
    depends_on: [lint]
  build:
    command: "python -m build"
    depends_on: [test]
```

**Action:**
```bash
taskrunner run tasks.yaml
```

**Expected Result:**
```
[Group 1] Running: lint
  ✓ lint (2.3s)
[Group 2] Running: test
  ✓ test (5.1s)
[Group 3] Running: build
  ✓ build (1.8s)

All 3 tasks completed successfully (9.2s)
```

lint → test → build 순서로 순차 실행. 각 태스크의 실행 시간과 성공 여부가 출력된다.

### Scenario 2: Parallel Execution

**Setup:**

```yaml
tasks:
  lint:
    command: "ruff check src/"
  typecheck:
    command: "mypy src/"
  test:
    command: "pytest tests/"
    depends_on: [lint, typecheck]
```

**Action:**
```bash
taskrunner run tasks.yaml
```

**Expected Result:**
```
[Group 1] Running: lint, typecheck (parallel)
  ✓ lint (2.3s)
  ✓ typecheck (4.5s)
[Group 2] Running: test
  ✓ test (5.1s)

All 3 tasks completed successfully (9.6s)
```

lint과 typecheck는 의존성이 없으므로 Group 1에서 병렬 실행. test는 둘 다 완료 후 실행. 전체 시간은 순차(11.9s) 대비 단축(9.6s).

---

## Data Models

### Model: Task

```python
class Task:
    name: str
    command: str
    depends_on: List[str]
    timeout: Optional[int]
```

**Constraints:**
- `name`은 태스크 파일 내에서 고유
- `depends_on`의 참조 대상은 같은 파일 내 존재해야 함
- `timeout` 미지정 시 무제한

### Model: TaskGraph

```python
class TaskGraph:
    tasks: Dict[str, Task]
    edges: List[Tuple[str, str]]
```

**Constraints:**
- 순환 의존성(cycle)이 존재하면 파싱 시 오류 발생

---

## Environment & Dependencies

### Directory Structure

```
taskrunner/
├── src/
│   ├── __init__.py
│   ├── cli.py           # CLI 진입점 (Click)
│   ├── parser.py        # YAML → TaskGraph 변환
│   ├── scheduler.py     # DAG 위상 정렬
│   ├── executor.py      # asyncio 병렬 실행
│   └── logger.py        # 실행 결과 로깅
├── tests/
│   ├── test_parser.py
│   ├── test_scheduler.py
│   └── test_executor.py
├── pyproject.toml
└── README.md
```

### Dependencies

**Runtime:**
```toml
[project.dependencies]
click = "^8.0"
pyyaml = "^6.0"
```

### Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| TASKRUNNER_LOG_DIR | No | ./logs | 로그 파일 저장 디렉토리 |
| TASKRUNNER_MAX_PARALLEL | No | 4 | 최대 병렬 실행 태스크 수 |

---

## Appendix: Code Reference Index

| File | Functions / Classes | Referenced In |
|------|---------------------|---------------|
| `src/cli.py` | run() | Core Design |
| `src/parser.py` | Parser.parse(), validate_schema() | Component Details |
| `src/scheduler.py` | Scheduler.topological_sort(), detect_cycles() | Core Design, Component Details |
| `src/executor.py` | Executor.execute(), run_task(), handle_timeout() | Component Details |
| `src/logger.py` | Logger.log(), format_result(), rotate_logs() | Component Details |
