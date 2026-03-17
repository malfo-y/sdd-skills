# Scale Assessment - Codex Autopilot

`sdd-autopilot`이 Step 4에서 규모를 판단할 때 참조하는 상세 가이드라인이다.

## Decision Process

```text
1. 정량적 기준으로 초기 규모 산정
2. 정성적 기준으로 보정
3. 경계 사례 규칙 적용
4. 최종 규모 결정
5. 테스트 전략 결정
```

## Quantitative Signals

### Touched Code Files

코드베이스 탐색 결과에서 실제 수정/생성할 코드 파일 수를 기준으로 본다.

| File Count | Scale |
|------------|-------|
| 1-3 | small |
| 4-10 | medium |
| 10+ | large |

Count rules:

- 직접 수정하는 코드 파일만 카운트한다
- 테스트 파일은 별도 카운트하지 않는다
- 자동 생성 파일이나 빌드 산출물은 제외한다
- 문서 전용 저장소라면 `SKILL.md`, reference, example 문서도 "code-like asset"으로 보되 동일 규칙을 일관되게 적용한다

### New Components

새로 생성해야 하는 독립 컴포넌트 수를 본다.

| Component Count | Scale |
|-----------------|-------|
| 0-1 | small |
| 1-3 | medium |
| 3+ | large |

### Spec Change Size

| Spec Change | Scale |
|-------------|-------|
| none | small |
| patch existing sections | medium |
| add new sections | large |

### Estimated Output Size

장문 산출물 규모를 보조 지표로 사용한다.

| Estimated Size | Scale |
|----------------|-------|
| < 200 lines | small |
| 200-1000 lines | medium |
| 1000+ lines | large |

## Qualitative Signals

### Complexity

| Complexity | Scale |
|------------|-------|
| local edit | small |
| multi-module coordination | medium |
| architecture or system-level change | large |

### Dependency Impact

| Dependency Situation | Scale |
|----------------------|-------|
| internal only | small |
| new package/service 1-2 | medium |
| multiple external or infra dependencies | large |

### Risk

| Risk Level | Scale |
|------------|-------|
| low regression risk | small |
| regression needs review | medium |
| cross-system, migration, or lifecycle risk | large |

## Boundary Rules

1. 정량과 정성이 다르면 더 큰 규모를 선택한다.
2. 확신이 없으면 `medium`을 기본값으로 한다.
3. 사용자가 "간단히", "최소한으로"를 강조하면 한 단계 낮춤을 고려한다.
4. 사용자가 "전체적으로", "프로덕션 레벨", "처음부터 끝까지"를 강조하면 한 단계 높임을 고려한다.
5. review 포함 파이프라인은 반드시 review-fix loop를 포함한다.
6. 순수 신규 생성만 있고 기존 자산 수정이 거의 없으면 파일 수 기준을 한 단계 완화할 수 있다.
7. 버그 수정은 영향 범위를 우선 본다.

### Pure-New-File Adjustment

- 5개 신규 파일이더라도 기존 코드 수정이 거의 없고 리스크가 낮으면 `medium`으로 둘 수 있다
- 반대로 파일 수가 적어도 공통 계약이나 architecture를 건드리면 `large`로 올린다

### Bug-Fix Adjustment

- 단일 파일 버그 수정 -> `small`
- 여러 파일에 걸친 버그 수정 -> `medium`
- 설계 결함이나 시스템적 버그 -> `large`

## Examples

### Small

| Request | Why |
|---------|-----|
| validation 문구 수정 | 파일 1개, 국소 수정 |
| wrapper skill 설명 보정 | 파일 1-2개, spec 영향 없음 |
| 테스트 체크리스트 한 줄 보강 | 구조 변화 없음 |

### Medium

| Request | Why |
|---------|-----|
| `sdd-autopilot` medium pipeline 보강 | main skill + refs + example 수정 |
| 새 wrapper/agent 계약 추가 | 여러 문서와 예시가 함께 바뀜 |
| feature draft + implementation plan 연동 조정 | 여러 asset coordination 필요 |

### Large

| Request | Why |
|---------|-----|
| 전체 SDD skill ecosystem parity 이식 | 10개+ 자산, 아키텍처 레벨 영향 |
| custom agent backbone 신규 도입 | 실행 모델 변화 |
| autopilot lifecycle와 spec governance 동시 재설계 | 문서/실행 계약 모두 변경 |

## Test Strategy Hint

### Inline Verification

다음 조건을 모두 만족하면 기본 전략은 inline verification 또는 inline test/debug loop다.

1. 검증 1회 실행이 수 분 이내
2. 로컬에서 완결된다
3. 외부 서비스 의존성이 없거나 mock 가능하다

### `ralph_loop_init`

다음 중 하나라도 해당하면 고려한다.

1. 장시간 실행이 필요하다
2. 외부 루프, 별도 워크스페이스, 장시간 빌드/학습이 필요하다
3. 단발성 inline 검증으로는 신뢰할 수 없다

### Repository Default

이 저장소는 문서/프롬프트 자산 저장소에 가까우므로 기본 전략은 inline verification이다.
