# Upgrade Mapping Guide - 구 형식 → Whitepaper 섹션 매핑

구 형식 스펙에서 흔히 발견되는 섹션/패턴을 whitepaper §1-§8 구조로 매핑하는 가이드.

---

## 매핑 테이블

### 기존 섹션 → §1 Background & Motivation

| 구 형식 섹션/패턴 | 매핑 위치 | 비고 |
|-------------------|----------|------|
| Overview / 개요 | §1 Core Value Proposition | 프로젝트 설명 부분 |
| Goals / 목표 | §1 Primary Objective + Key Features | 목표 → 목적, 기능 목록 → 주요 기능 |
| Introduction / 소개 | §1 Problem Statement + Why This Approach | 소개 내 문제 설명과 접근 이유 분리 |
| Scope / 범위 | §1 Non-Goals (Out of Scope) | 범위 밖 항목 → Non-Goals |
| Requirements / 요구사항 | §1 Success Criteria | 기능 요구사항 → 성공 기준 |
| Target Users / 대상 사용자 | §1 Target Users / Use Cases | 그대로 이동 |

### 기존 섹션 → §2 Core Design

| 구 형식 섹션/패턴 | 매핑 위치 | 비고 |
|-------------------|----------|------|
| Design / 설계 | §2 Key Idea + Design Rationale | 설계 설명 → 서사로 보강 |
| Algorithm / 알고리즘 | §2 Algorithm / Logic Flow | 코드 발췌 추가 |
| Flow / 흐름도 | §2 Algorithm / Logic Flow | 텍스트 다이어그램 보존 |
| Patterns / 패턴 | §2 Design Rationale | 사용 패턴 → 설계 근거 |

### 기존 섹션 → §3 Architecture Overview

| 구 형식 섹션/패턴 | 매핑 위치 | 비고 |
|-------------------|----------|------|
| Architecture / 아키텍처 | §3 System Diagram + Design Decisions | 그대로 이동 |
| Tech Stack / 기술 스택 | §3 Technology Stack | 그대로 이동 |
| System Diagram / 시스템 구조 | §3 System Diagram | 그대로 이동 |
| High-level Design | §3 전체 | 그대로 이동 |

### 기존 섹션 → §4 Component Details

| 구 형식 섹션/패턴 | 매핑 위치 | 비고 |
|-------------------|----------|------|
| Components / 컴포넌트 | §4 Component Details | Why 필드 보강 필요 |
| Modules / 모듈 | §4 Component Details | 모듈 → 컴포넌트로 재구성 |
| Services / 서비스 | §4 Component Details | 서비스별 → 컴포넌트별 |
| Classes / 클래스 | §4 Implementation Details | 클래스 설명 → 컴포넌트 내 상세 |
| Functions / 함수 목록 | §4 Key Classes/Functions | 함수 목록 → 컴포넌트 내 핵심 함수 |

### 기존 섹션 → §5 Usage Guide & Expected Results

| 구 형식 섹션/패턴 | 매핑 위치 | 비고 |
|-------------------|----------|------|
| Usage / 사용법 | §5 Scenarios | Setup/Action/Expected Result 형식으로 재구성 |
| Examples / 예제 | §5 Scenarios | 시나리오에 통합 |
| Getting Started / 시작하기 | §5 Installation + Running Locally | 그대로 이동 |
| Quick Start | §5 Scenario 1 (Basic Usage) | 기본 사용법 시나리오로 변환 |
| CLI Reference / CLI 참조 | §5 Common Operations | 명령어별 시나리오로 변환 |
| How to Use / 사용 방법 | §5 전체 | 시나리오 형식으로 재구성 |

### 기존 섹션 → §6-§8

| 구 형식 섹션/패턴 | 매핑 위치 | 비고 |
|-------------------|----------|------|
| Data Model / 데이터 모델 | §6 Data Models | 그대로 이동 |
| Schema / 스키마 | §6 Data Models | 그대로 이동 |
| API / API 문서 | §7 API Reference | 그대로 이동 |
| Endpoints / 엔드포인트 | §7 API Reference | 그대로 이동 |
| Environment / 환경 | §8 Environment & Dependencies | 그대로 이동 |
| Setup / 설정 | §8 Configuration | 그대로 이동 |
| Dependencies / 의존성 | §8 Dependencies | 그대로 이동 |
| Directory Structure / 디렉토리 | §8 Directory Structure | 그대로 이동 |
| Configuration / 설정 | §8 Configuration | 그대로 이동 |

### 기타 섹션 처리

| 구 형식 섹션/패턴 | 처리 방법 |
|-------------------|----------|
| Issues / 이슈 | §4 Known Issues 또는 별도 Identified Issues 섹션 |
| TODO / 할일 | Identified Issues & Improvements 섹션 |
| Changelog / 변경이력 | 문서 하단 Changelog 섹션으로 이동 |
| Testing / 테스트 | §5 내 테스트 시나리오로 통합 또는 별도 유지 |
| Security / 보안 | 별도 Security Considerations 섹션 유지 |
| Performance / 성능 | 별도 Performance Considerations 섹션 유지 |
| Deployment / 배포 | 별도 Deployment 섹션 유지 |

---

## 서사 섹션 생성 가이드

구 형식 스펙에서 보통 빠져있는 서사 섹션을 생성하는 방법.

### §1 Background & Motivation 생성

소스:
- README.md의 첫 문단 → Problem Statement
- 프로젝트 구조와 기술 스택 → Why This Approach
- 기존 스펙의 Goals/Overview → Core Value Proposition

작성 원칙:
- 문제를 먼저 설명하고, 해결 방법을 뒤에 배치
- 대안을 최소 1개 언급하고 현재 접근을 택한 이유 설명
- 핵심 가치를 한 문단으로 요약

### §2 Core Design 생성

소스:
- 핵심 진입점 코드 (main.py, index.ts 등) → Key Idea
- 주요 알고리즘/처리 함수 → Algorithm / Logic Flow
- 기존 스펙의 Design/Architecture 섹션 → Design Rationale

작성 원칙:
- Key Idea는 서사적으로 작성 (단순 목록 아님)
- 핵심 코드 발췌를 포함 (30줄 규칙 적용)
- 인라인 citation `[filepath:functionName]` 사용
- "왜 이 구조인가"를 반드시 포함

### §5 Usage Guide & Expected Results 생성

소스:
- 테스트 코드 → 시나리오 추출
- CLI/API 인터페이스 → 사용법 정리
- README의 Quick Start → 기본 사용 시나리오

작성 원칙:
- 최소 2개 시나리오 (Basic, Advanced)
- 각 시나리오는 Setup → Action → Expected Result 형식
- Expected Result는 구체적 (출력 예시, 상태 변화 등)

---

## 코드 Citation 삽입 가이드

### 인라인 Citation
- 형식: `[filepath:functionName]` 또는 `[filepath:ClassName]`
- 경로: 프로젝트 루트 기준 상대 경로
- 사용 위치: §2 Core Design 서사, §4 Component Details

### 코드 블록 Citation
```python
# [src/core/processor.py:process_data]
def process_data(input: InputModel) -> OutputModel:
    """Core processing logic."""
    validated = validate(input)
    result = transform(validated)
    return OutputModel(result=result)
```

### Source 필드 (§4 Component Details)
```
| **Source** | `src/core/processor.py`: ProcessorClass, process_data() |
|            | `src/core/validator.py`: validate(), ValidationRule     |
```

### Appendix: Code Reference Index
```markdown
| File | Functions / Classes | Referenced In |
|------|---------------------|---------------|
| `src/core/processor.py` | process_data(), transform() | Core Design, Component Details |
| `src/core/validator.py` | validate(), ValidationRule | Core Design |
```
