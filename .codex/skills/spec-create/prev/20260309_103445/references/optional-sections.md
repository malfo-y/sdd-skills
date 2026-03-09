# Optional Spec Sections

Add these sections only when they are materially relevant to the repository.
The default spec should stay lean and navigation-friendly.

## Data Models

Use when shared schemas or persistence rules are central to the project.

```markdown
## Data Models

### Model: <Name>
- 목적
- 핵심 필드
- 제약 조건
- 관련 경로
```

## API Surface

Use when the repository's primary contract is an external API.

```markdown
## API Surface

### Endpoint / Contract: `<method> <path>`
- 목적
- 입력
- 출력
- 실패 조건
- 관련 경로
```

## Security Considerations

Use when auth, secrets, tenancy, or sensitive data handling meaningfully shape implementation choices.

```markdown
## Security Considerations
- 인증/인가 방식
- 비밀정보 취급 규칙
- 감사 또는 추적 요구사항
```

## Performance Considerations

Use when latency, throughput, concurrency, or cost are first-order concerns.

```markdown
## Performance Considerations
- 병목 지점
- 현재 보호장치
- 주의해야 할 확장 한계
```

## Deployment / Operations

Use when deployment topology or runbook knowledge is required for safe changes.

```markdown
## Deployment / Operations
- 실행 환경
- 배포 파이프라인
- 운영 체크포인트
```
