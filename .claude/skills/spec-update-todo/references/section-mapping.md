# Section Mapping Guide

How to map user input categories to spec document sections.

---

## Quick Reference

| Input Type | Spec Section (Korean) | Spec Section (English) |
|------------|----------------------|------------------------|
| New Feature (Core) | 목표 > 주요 기능 | Goal > Key Features |
| New Feature (Component) | 컴포넌트 상세 | Component Details |
| Component Overview | 컴포넌트 상세 > [컴포넌트] > 개요 | Component Details > [Component] > Overview |
| Enhancement | 개선 필요사항 > 개선 제안 | Issues > Improvements |
| Bug Report | 발견된 이슈 > 버그 | Issues > Bugs |
| Performance | 개선 필요사항 > 성능 | Issues > Performance |
| Security | 보안 고려사항 | Security Considerations |
| Config Change | 설정 | Configuration |
| Dependency | 환경 및 의존성 | Environment & Dependencies |
| API Change | API 레퍼런스 | API Reference |
| Test Addition | 테스트 | Testing |

---

## Detailed Mapping Rules

### 1. New Features

**When input describes new functionality:**

```
Input: Feature with clear purpose
↓
Target: 목표 > 주요 기능 (numbered list)
```

**Example:**
```markdown
# Input
### Feature: 스케줄러 통합
**Description**: 정해진 시간에 자동 실행

# Maps to Spec
## 목표
### 주요 기능
6. **스케줄러 통합**: 정해진 시간에 자동으로 데이터 수집 실행 📋
```

**When feature requires new component:**

```
Input: Feature with implementation details
↓
Target: 컴포넌트 상세 (new subsection)
```

**Example:**
```markdown
# Input
### Feature: 알림 서비스
**Planned Methods**: send_slack(), send_discord()

# Maps to Spec
## 컴포넌트 상세
### 컴포넌트: NotificationService 📋 계획됨

#### 개요
[Description]

| 항목 | 설명 |
|------|------|
| **목적** | 작업 완료/실패 알림 전송 |
| **상태** | 📋 계획됨 |
```

### 2. Improvements

**General improvements:**

```
Input: Improvement suggestion
↓
Target: 발견된 이슈 및 개선 필요사항 > 개선 제안
```

**Example:**
```markdown
# Input
### Improvement: 다운로드 속도 최적화
**Current**: 2 concurrent
**Proposed**: 10 concurrent

# Maps to Spec
## 발견된 이슈 및 개선 필요사항
### 개선 제안
4. **다운로드 속도 최적화** (우선순위: 높음) 📋
   - 현재: 동시 2개 다운로드
   - 제안: 동시 10개 다운로드 + 연결 풀링
   - 이유: 대용량 처리 시 시간 단축
```

### 3. Bug Reports

**Bug reports:**

```
Input: Bug description
↓
Target: 발견된 이슈 및 개선 필요사항 > 버그
       또는 컴포넌트 상세 > [Component] > 알려진 이슈
```

**Example (General Bug):**
```markdown
# Input
### Bug: 유니코드 파일명 오류
**Location**: ig_post_image_downloader.py:145

# Maps to Spec
## 발견된 이슈 및 개선 필요사항
### 버그
- [ ] **BUG-003**: 유니코드 파일명 오류
  - 위치: `ig_post_image_downloader.py:145`
  - 영향도: High
  - 상태: 조사 중
```

**Example (Component-Specific Bug):**
```markdown
# Maps to Component Section
### 컴포넌트: ig_post_image_downloader.py
#### 알려진 이슈
- **유니코드 파일명**: 이모지 포함 시 오류 (해결 예정)
```

### 4. Configuration Changes

**New environment variables:**

```
Input: New config option
↓
Target: 설정 > 환경 변수
```

**Example:**
```markdown
# Input
### New Config: NOTIFICATION_WEBHOOK
**Type**: Environment Variable
**Default**: None

# Maps to Spec
## 설정
### 환경 변수
| 변수 | 필수 | 설명 |
|------|------|------|
| `APIFY_TOKEN` | 예 | ... |
| `NOTIFICATION_WEBHOOK` | 아니오 | 알림 웹훅 URL 📋 |
```

**New config file options:**

```
Input: Config file changes
↓
Target: 설정 > [Config File Section]
```

### 5. Component Changes

**Updating existing component:**

```
Input: Changes to existing component
↓
Target: 컴포넌트 상세 > [Component Name]
```

**Adding methods/functions:**
```markdown
# Input
### Update Component: shared_utils.py
**New Functions**: setup_logger(), log_to_json()

# Maps to Spec (add to existing section)
### 컴포넌트: shared_utils.py
#### 핵심 기능
...existing functions...

**로깅 유틸리티** 📋 계획됨
```python
def setup_logger(name: str, level: str, format: str) -> Logger
def log_to_json(event: str, data: dict) -> str
```

### 6. API Changes

**New endpoints:**

```
Input: New API endpoint
↓
Target: API 레퍼런스 (if exists) or 사용 예제
```

**Example:**
```markdown
# Input
### New API: GET /status
**Description**: Check pipeline status

# Maps to Spec (if API section exists)
## API 레퍼런스
### GET /status 📋 계획됨
**설명**: 파이프라인 실행 상태 조회
```

### 7. Dependencies

**New dependencies:**

```
Input: New library requirement
↓
Target: 환경 및 의존성 > 의존성
```

**Example:**
```markdown
# Input
Add library: APScheduler for scheduling

# Maps to Spec
## 환경 및 의존성
### 의존성
**런타임 의존성:**
```
apify_client
requests
apscheduler          # 스케줄링 지원 📋 추가 예정
```

---

## Status Markers

When adding items, use status markers:

| Marker | Meaning | When to Use |
|--------|---------|-------------|
| 📋 | 계획됨 (Planned) | New features not yet implemented |
| 📋 계획됨 | Full status | Component or major feature |
| 📋 추가 예정 | To be added | Dependencies, config |
| (우선순위: X) | Priority indicator | Improvements |

---

## Section Creation Rules

### When to Create New Sections

1. **New top-level concern**: Security, Performance, Monitoring
2. **New component type**: Services, Integrations, Plugins
3. **Grouped features**: If 3+ related features, create subsection

### When to Add to Existing Sections

1. **Single feature**: Add to list
2. **Related improvement**: Add to existing improvements
3. **Component update**: Add to component section

---

## Language Consistency

### If Spec is in Korean

- Add content in Korean
- Use Korean section headers
- Translate technical terms when appropriate

### If Spec is in English

- Add content in English
- Match existing terminology
- Keep code identifiers in English

### Mixed Language

- Follow existing pattern
- Code names always in English
- Descriptions in spec's primary language

---

## Version Impact

| Change Type | Version Impact |
|-------------|---------------|
| New major feature | Minor bump (1.0.0 → 1.1.0) |
| Multiple features | Minor bump |
| Single feature | Patch bump (1.0.0 → 1.0.1) |
| Improvements only | Patch bump |
| Bug reports only | Patch bump |
| Documentation only | Patch bump |

---

## Changelog Integration

Always add changelog entry:

```markdown
## 변경 로그

### [1.0.1] - 2026-02-04

#### 추가됨 (Planned)
- 스케줄러 통합 기능 (📋 계획)
- 알림 서비스 컴포넌트 (📋 계획)

#### 개선 예정
- 다운로드 병렬화 10개로 증가
- 진행률 바 추가

#### 버그 보고됨
- BUG-003: 유니코드 파일명 오류
```
