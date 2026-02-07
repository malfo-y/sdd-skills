---
name: spec-draft
description: This skill should be used when the user asks to "draft spec", "create spec draft", "write requirements", "collect requirements", "spec draft", "스펙 초안", "요구사항 수집", or wants to have a conversation to gather and document feature requests, improvements, or bug reports before updating the main spec.
version: 1.0.0
---

# Spec Draft - 사용자 대화 기반 스펙 초안 작성

사용자와의 대화를 통해 요구사항을 수집하고 구조화된 스펙 초안(user_draft.md)을 작성합니다.

## Overview

이 스킬은 사용자와 대화하며 기능 요청, 개선 사항, 버그 리포트 등을 수집하여 `_sdd/spec/user_draft.md` 파일에 구조화된 형식으로 저장합니다. 출력 형식은 `spec-update` 스킬의 입력 형식("Spec Update Input")을 따르므로, 작성된 초안은 바로 `spec-update` 스킬로 메인 스펙에 반영할 수 있습니다.

## When to Use This Skill

- 새로운 기능에 대한 아이디어를 정리할 때
- 사용자 요구사항을 체계적으로 수집할 때
- 버그나 개선사항을 문서화할 때
- `spec-update`를 실행하기 전 입력 파일을 준비할 때

## Input Sources

1. **사용자 대화 (현재 세션)**: 실시간으로 요구사항 수집
2. **사용자가 수정한 코드 (수정된 코드)**: 사용자가 수정한 코드를 분석하여 요구사항 추출
3. **기존 초안 파일 (`_sdd/spec/user_draft.md`)**: 이전에 작성된 내용 로드 및 추가
4. **사용자가 지정한 다른 파일**: 참조 문서나 메모

## Output

**파일 위치**: `_sdd/spec/user_draft.md`

**형식**: "Spec Update Input" 포맷 (spec-update 스킬과 호환)

## Process

### Step 1: 기존 초안 확인

```
1. `_sdd/spec/user_draft.md` 존재 여부 확인
2. 존재하면: 내용 로드, 사용자에게 추가/수정 여부 확인
3. 없으면: 새로 생성 모드로 진행
4. `_sdd/spec/` 디렉토리가 없으면 생성
```

### Step 2: 수정된 코드 확인

```
1. 수정된 코드가 제공되었는지 확인
2. 제공된 경우: 코드를 분석하여 요구사항 추출
3. 추출된 요구사항을 바탕으로 step 3으로 이동
```

### Step 3: 요구사항 유형 확인

AskUserQuestion을 사용하여 추가할 내용의 종류 확인. 이미 추출된 요구사항이 있을 경우 해당 내용을 바탕으로 질문:

- **새 기능 (New Feature)**: 완전히 새로운 기능 추가
- **개선 사항 (Improvement)**: 기존 기능의 향상
- **버그 리포트 (Bug Report)**: 발견된 문제점
- **컴포넌트 변경 (Component Change)**: 새 컴포넌트 추가 또는 기존 컴포넌트 수정
- **설정 변경 (Configuration)**: 환경변수, 설정 파일 관련

### Step 4: 세부 정보 수집

유형별로 필요한 정보를 질문을 통해 수집합니다.

**새 기능 추가 시 질문 가이드**:
1. 기능 이름은 무엇인가요?
2. 우선순위는 어떻게 되나요? (High/Medium/Low)
3. 이 기능이 무엇을 해야 하나요? (설명)
4. 완료 조건은 무엇인가요? (Acceptance Criteria)
5. 어떤 컴포넌트가 관련되나요?
6. 기술적 제약이나 참고사항이 있나요?

**개선 사항 시 질문 가이드**:
1. 현재 상태는 어떤가요?
2. 어떻게 개선하고 싶나요?
3. 개선이 필요한 이유는 무엇인가요?
4. 우선순위는 어떻게 되나요?

**버그 리포트 시 질문 가이드**:
1. 심각도는 어떤가요? (High/Medium/Low)
2. 어디서 발생하나요? (파일:라인)
3. 재현 방법은 무엇인가요?
4. 예상되는 정상 동작은 무엇인가요?
5. 현재 우회 방법이 있나요?

### Step 5: 초안 작성/업데이트

수집된 정보를 "Spec Update Input" 형식으로 구조화하여 저장:

```markdown
# Spec Update Input

**Date**: YYYY-MM-DD
**Author**: [작성자]
**Target Spec**: [대상 스펙 파일]

---

## New Features

### Feature: [기능 이름]
**Priority**: High/Medium/Low
**Category**: [카테고리]
**Target Component**: [대상 컴포넌트]

**Description**:
[기능 설명]

**Acceptance Criteria**:
- [ ] 기준 1
- [ ] 기준 2

**Technical Notes**:
[기술적 참고사항]

**Dependencies**:
[의존성]

---

## Improvements

### Improvement: [개선 이름]
**Priority**: High/Medium/Low
**Current State**: [현재 상태]
**Proposed**: [제안 내용]
**Reason**: [개선 이유]

---

## Bug Reports

### Bug: [버그 이름]
**Severity**: High/Medium/Low
**Location**: [파일:라인]

**Description**:
[버그 설명]

**Reproduction**:
1. 재현 단계 1
2. 재현 단계 2

**Expected Behavior**:
[예상 동작]

**Workaround**:
[우회 방법]

---

## Component Changes

### New Component: [컴포넌트 이름]
**Purpose**: [목적]
**Input**: [입력]
**Output**: [출력]

**Planned Methods**:
- `method_name()` - 설명

### Update Component: [컴포넌트 이름]
**Change Type**: [Enhancement/Refactor/Fix]

**Changes**:
- 변경 사항 1
- 변경 사항 2

---

## Configuration Changes

### New Config: [설정 이름]
**Type**: Environment Variable / Config File
**Required**: Yes/No
**Default**: [기본값]
**Description**: [설명]

---

## Notes

### Context
[추가 컨텍스트]

### Constraints
[제약 사항]

### References
[참조 링크]
```

### Step 6: 확인 및 완료

1. 작성된 초안 내용을 사용자에게 보여줌
2. 수정이 필요한지 확인
3. 추가할 내용이 더 있는지 확인
4. 완료 시 다음 단계 안내: `/spec-update` 실행 권장

## Conversation Flow Example

```
Claude: 기존 user_draft.md가 있습니다. 내용을 추가하시겠습니까, 새로 시작하시겠습니까?
User: 추가할게요

Claude: 어떤 종류의 내용을 추가하시겠습니까?
[선택지: 새 기능 / 개선 사항 / 버그 리포트 / 컴포넌트 변경 / 설정 변경]
User: 새 기능

Claude: 기능 이름은 무엇인가요?
User: 실시간 알림

Claude: 우선순위는 어떻게 되나요?
[선택지: High / Medium / Low]
User: Medium

Claude: 이 기능이 무엇을 해야 하나요?
User: 다운로드 완료 시 Slack으로 알림 전송

Claude: 완료 조건은 무엇인가요? (여러 개 입력 가능)
User: Slack 웹훅 설정 가능, 메시지 템플릿 커스터마이징

Claude: 관련 컴포넌트는 무엇인가요?
User: shared_utils.py

Claude: 초안에 추가했습니다. 더 추가할 내용이 있나요?
User: 아니요

Claude: user_draft.md가 업데이트되었습니다.
        `/spec-update`를 실행하여 메인 스펙에 반영할 수 있습니다.
```

## Priority Levels

| Level | 한국어 | 설명 |
|-------|--------|------|
| High | 높음 | 다음 릴리스에 반드시 포함 |
| Medium | 중간 | 계획된 개선 사항 |
| Low | 낮음 | 있으면 좋은 기능 |

## Category Tags

| Category | 설명 |
|----------|------|
| Core Feature | 핵심 기능 |
| Enhancement | 기존 기능 개선 |
| Bug Fix | 버그 수정 |
| Performance | 성능 개선 |
| Security | 보안 관련 |
| Documentation | 문서 개선 |
| Testing | 테스트 추가 |
| Infrastructure | 인프라/환경 |

## Workflow Integration

```
spec-draft → spec-update → implementation-plan → implementation
     ↑            │
     │            ▼
     └──── user_draft.md
```

1. **spec-draft** (이 스킬): 사용자와 대화하여 `user_draft.md` 생성
2. **spec-update**: `user_draft.md`를 읽어 메인 스펙 업데이트
3. 필요시 `spec-draft`로 돌아가 추가 내용 작성

## Best Practices

### 효과적인 요구사항 수집

- **구체적으로**: 모호한 표현보다 명확한 기준 제시
- **예시 포함**: 가능하면 구체적인 사용 예시 수집
- **우선순위 명시**: 모든 항목에 우선순위 부여
- **맥락 설명**: 왜 필요한지 이유 기록

### 파일 관리

- **증분 저장**: 대화 중에도 주기적으로 파일 업데이트
- **백업 불필요**: 버전 관리로 히스토리 보존
- **처리 후 정리**: `spec-update` 실행 후 파일명 변경됨

## Error Handling

| 상황 | 대응 |
|------|------|
| `_sdd/spec/` 디렉토리 없음 | 자동 생성 |
| 기존 `user_draft.md` 존재 | 추가/덮어쓰기 확인 |
| 불완전한 정보 | 필수 항목 재질문 |
| 사용자가 중단 | 현재까지 내용 저장 |

## Additional Resources

### Reference Files
- **`references/question-guide.md`** - 유형별 상세 질문 가이드

### Example Files
- **`examples/user_draft.md`** - 출력 예시 파일
