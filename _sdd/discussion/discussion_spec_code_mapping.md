# 토론 요약: SDD 스펙 스킬에 코드 매핑(Source 필드) 기능 추가

**날짜**: 2026-03-09
**라운드 수**: 7
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)
1. **현황 파악**: 현재 스펙 스킬들에는 코드 매핑이 best practice 권장 수준으로만 존재하며, 스펙 섹션 ↔ 소스코드 간 구조적 traceability는 부재
2. **매핑 granularity**: 파일 레벨이 아닌 함수/클래스 레벨까지 매핑 필요
3. **매핑 위치**: 별도 파일/섹션이 아닌, 각 컴포넌트 테이블에 인라인 Source 필드로 기록
4. **적용 스킬 범위**: spec-create + spec-update-done 두 스킬에 핵심 로직 적용
5. **코드 없을 때 처리**: Source 필드 자체를 생략 (TBD 플레이스홀더 대신)
6. **매핑 소스 전략**: 구현 산출물(plan/report) 우선 참조 + 코드 탐색으로 보완하는 혼합 방식
7. **타 스킬 연동**: spec-rewrite/spec-review에는 Source 필드 보존 규칙만 추가

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | 매핑 granularity = 함수/클래스 레벨 | 파일 레벨만으로는 대규모 파일에서 추적이 어려움 | 논점 2 |
| 2 | 매핑 위치 = 인라인 (섹션 내 Source 필드) | 스펙을 읽을 때 바로 코드 위치를 확인할 수 있어 직관적 | 논점 3 |
| 3 | 적용 스킬 = spec-create + spec-update-done | spec-create에서 초기화, spec-update-done에서 갱신하는 자연스러운 흐름 | 논점 4 |
| 4 | 코드 없으면 Source 필드 생략 | 불필요한 TBD 노이즈 방지, spec-update-done에서 추가 | 논점 5 |
| 5 | 매핑 소스 = 혼합 (구현 산출물 우선 + 코드 탐색 보완) | 구현 산출물에 이미 파일 변경 정보가 있으므로 효율적, 누락분만 코드 탐색 | 논점 6 |
| 6 | 포맷 = 파일별 줄바꿈 그룹핑, 백틱으로 파일 경로 표시 | 가독성과 그룹핑 모두 확보 | 논점 3 |
| 7 | 타 스킬에는 Source 필드 보존 규칙만 추가 | 범위를 최소화하고 핵심 스킬에 집중 | 논점 7 |

## 미결 질문 (Open Questions)
- 없음

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | spec-create SKILL.md에 Source 필드 관련 지시사항 추가 (코드 있을 때만 인라인 Source 필드 생성, 포맷 규칙) | High | - |
| 2 | spec-update-done SKILL.md에 Source 필드 갱신 로직 추가 (혼합 방식: 구현 산출물 우선 + 코드 탐색 보완) | High | - |
| 3 | spec-rewrite, spec-review SKILL.md에 "기존 Source 필드 보존" 규칙 추가 | Medium | - |

## 리서치 결과 요약 (Research Findings)
- **스펙 스킬 현황 조사**: 8개 스펙 관련 스킬 확인. `spec-create`와 `spec-rewrite`에 "Link to Code" best practice 존재하나, 구조적 매핑 메커니즘은 부재. `spec-update-done`의 changelog 예시에 파일 경로 참조(`src/module.py:45-89`)가 있으나, 스펙 본문의 섹션별 매핑과는 다른 용도.

## Source 필드 포맷 예시

```markdown
### 토큰 검증

| Aspect | Description |
|--------|-------------|
| **Purpose** | JWT 토큰 검증 |
| **Source** | `src/auth/token.py`: verify_token(), decode_jwt() |
|            | `src/auth/handler.py`: AuthHandler |
| **Input** | Bearer token string |
| **Output** | Decoded payload or error |
```

## 토론 흐름 (Discussion Flow)
Round 1: 매핑 수준 → 함수/클래스 레벨로 결정
Round 2: 매핑 위치 → 인라인 방식 (섹션 내 Source 필드) 결정
Round 3: 적용 스킬 → spec-create + spec-update-done 결정
Round 4: 코드 없을 때 처리 → Source 필드 생략 결정
Round 5: 매핑 소스 → 혼합 방식 (구현 산출물 우선 + 코드 탐색 보완) 결정
Round 6: 포맷 → 파일별 줄바꿈 그룹핑 + 백틱 결정
Round 7: 타 스킬 연동 → Source 필드 보존 규칙만 추가 결정
