# 토론 요약: implementation-review 스킬 Graceful Degradation

**날짜**: 2026-03-11
**라운드 수**: 8 + 추가 결정 1건
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)
1. **현재 Hard Dependency 문제**: implementation-review 스킬이 IMPLEMENTATION_PLAN.md 없이는 동작 불가한 구조
2. **Graceful Degradation 전략**: Plan → Spec → Code Quality 3단계 fallback 구조 도입
3. **Tier별 리뷰 기준 정의**: 각 Tier가 무엇을 기준으로 리뷰하는지
4. **Non-interactive 기조 유지**: Tier 3에서도 사용자 입력 없이 자동 진행
5. **리포트 형식 통일**: 동일 형식 + Tier 표시로 일관성 유지
6. **기존 Tier 1 동작 보존**: Plan not found 분기만 변경하여 안전하게 확장
7. **Stale Plan 감지**: Plan 파일이 존재하더라도 실제 구현/스펙과 정합성이 맞지 않으면 이전에 생성된 파일로 간주하고 Tier 2로 fallback

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | Graceful Degradation 3-tier 전략 채택 | Plan 없이도 유용한 리뷰 제공 필요 | 논점 1, 2 |
| 2 | Tier 2: Spec 구조에 따라 적응적 동작 | 구조화된 Spec → 자동 추출, 비구조화 → 대략적 정합성 확인 | 논점 3 |
| 3 | Tier 3: 기본값 "최근 변경 중심 리뷰"로 자동 진행 | Non-interactive 기조 유지, 가정사항은 리포트에 기록 | 논점 3, 4 |
| 4 | 리포트 형식: 기본 형식 유지 + 상단에 `Review Mode: Tier N` 표시 | 일관성 + 투명성 (어떤 모드로 리뷰했는지 명시) | 논점 5 |
| 5 | Tier 판별: 기존 경로 규칙 사용 | Plan: `_sdd/implementation/IMPLEMENTATION_PLAN*.md`, Spec: `_sdd/spec/` 디렉토리 내 파일 존재 여부 | 논점 2 |
| 6 | Tier 1 보존: Plan not found 분기만 fallback으로 변경 | Plan 탐색 로직 자체는 손대지 않아 기존 동작 완전 보존 | 논점 6 |
| 7 | Stale Plan 감지: Plan이 실제 구현/스펙과 불일치 시 Tier 2로 fallback | Plan 파일이 이전에 생성된 것일 수 있으므로, 정합성 검증 후 불일치 시 Spec 기반 리뷰로 전환 | 논점 7 |

## 미결 질문 (Open Questions)
- 없음 (모든 핵심 질문 해결됨)

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | implementation-review 스킬에 Graceful Degradation 로직 구현 | High | 개발자 |

## 리서치 결과 요약 (Research Findings)
- **현재 스킬 구조 분석**: IMPLEMENTATION_PLAN.md가 유일한 Hard Dependency. env.md는 Soft (테스트 실행에만 영향). Spec 파일은 참조용(읽기만). 리포트 출력은 `_sdd/implementation/IMPLEMENTATION_REVIEW.md`로 저장.

## 설계 명세: Graceful Degradation 3-Tier 구조

### Tier 판별 흐름
```
Step 1 시작
  → Plan 탐색 (기존 로직 유지)
    → 발견됨 → Plan 정합성 검증 (실제 구현/스펙과 비교)
      → 정합성 OK → Tier 1 (기존 동작 그대로)
      → 정합성 불일치 (stale plan) → Tier 2로 fallback
    → 미발견 → Spec 탐색 (_sdd/spec/ 내 파일 존재 여부)
      → 발견됨 → Tier 2
      → 미발견 → Tier 3
```

### Stale Plan 감지 기준
- Plan의 Task 목록과 실제 코드베이스 구조/파일이 현저히 불일치
- Plan이 참조하는 Spec 버전과 현재 Spec 내용이 다름
- Plan 생성 시점 이후 코드베이스에 대규모 변경이 발생한 경우
- 감지 시 리포트에 `⚠️ Stale Plan detected — fallback to Tier 2 (Spec-based review)` 기록

### Tier별 동작

| Tier | 기준 소스 | 리뷰 방식 | Interactive |
|------|----------|----------|-------------|
| **Tier 1** | IMPLEMENTATION_PLAN.md | Task/Criteria 목록 기반 전체 검증 (현재 동작) | No |
| **Tier 2** | _sdd/spec/ | Spec 구조에 따라 적응적: 구조화 → 요구사항 자동 추출 후 검증, 비구조화 → 전체적 정합성 확인 | No |
| **Tier 3** | 코드베이스 자체 | 최근 변경 중심 코드 품질 리뷰 (기본값), 가정사항 리포트 기록 | No |

### 리포트 형식
- 기존 IMPLEMENTATION_REVIEW.md 형식 유지
- 상단에 `Review Mode: Tier N (설명)` 추가
- Tier 2/3에서는 해당되지 않는 섹션은 생략 또는 'N/A'
- Tier 3에서는 "가정사항" 섹션 추가 (Open Questions에 기본값 선택 이유 기록)

## 토론 흐름 (Discussion Flow)
Round 1: 토론 방향 확인 → Plan 없이도 동작하게 개선 방향 확정
Round 2: 리뷰 기준 선택 → Graceful Degradation (3-tier fallback) 채택
Round 3: Tier 3 범위 → 사용자 선택 방식 (범용 코드 품질 vs 최근 변경 중심)
Round 4: Tier 2 동작 → Spec 구조에 따라 적응적 동작
Round 5: 리포트 형식 → 기본 형식 + Tier 표시
Round 6: Non-interactive 충돌 → 기본값으로 자동 진행 (non-interactive 유지)
Round 7: Tier 판별 로직 → 기존 경로 규칙 사용
Round 8: Tier 1 보존 → Plan not found 분기만 변경하여 안전 확보
추가: Stale Plan 감지 → Plan 존재해도 구현/스펙과 불일치 시 Tier 2 fallback

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: implementation-review 스킬이 Plan 없이도 동작하게 만들고 싶으신 건가요?
**Options**: 1) Plan 없이도 동작하게 개선 2) 현재 의존성 구조가 적절한지 검토 3) 아예 독립적인 코드 리뷰 스킬이 필요 4) 토론 종료
**A**: Plan 없이도 동작하게 개선
**Follow-up**: 핵심 문제는 "Plan 없으면 무엇을 기준으로 리뷰할 것인가"

### Round 2
**Q**: Plan 없을 때 implementation-review가 무엇을 기준으로 리뷰해야 한다고 생각하세요?
**Options**: 1) Spec 기반 리뷰 2) 코드베이스 자체 품질 리뷰 3) Graceful Degradation 4) 토론 종료
**A**: Graceful Degradation
**Follow-up**: 3단계 fallback 구조 확정: Plan → Spec → Code Quality

### Round 3
**Q**: Tier 3 (코드 품질 리뷰)에서 어떤 항목들을 검증해야 할까요?
**Options**: 1) 범용 코드 품질 검증 2) 최근 변경 중심 리뷰 3) Tier 3는 불필요 4) 토론 종료
**A**: AskUserQuestion으로 범용 코드 품질 / 최근 변경 중심 중에 사용자 선택
**Follow-up**: Tier 3에서 사용자 선택 방식 채택

### Round 4
**Q**: Tier 2 (Spec 기반 리뷰)는 구체적으로 어떻게 동작해야 할까요?
**Options**: 1) Spec에서 자동 추출 2) 대략적 정합성 확인 3) Spec 구조에 따라 다르게 4) 토론 종료
**A**: Spec 구조에 따라 다르게
**Follow-up**: 적응적 동작 - 구조화 Spec은 자동 추출, 비구조화는 정합성 확인

### Round 5
**Q**: 리포트 형식이 Tier별로 달라져야 할까요?
**Options**: 1) 동일 형식, 범위만 다르게 2) Tier별 전용 템플릿 3) 기본 형식 + Tier 표시 4) 토론 종료
**A**: 기본 형식 + Tier 표시
**Follow-up**: 동일 형식 유지 + 상단 Review Mode 표시로 투명성 확보

### Round 6
**Q**: Non-interactive 모드와의 충돌을 어떻게 해결할까요?
**Options**: 1) Tier 판별만 물어보기 2) 기본값으로 자동 진행 3) Interactive 허용 4) 토론 종료
**A**: 기본값으로 자동 진행
**Follow-up**: Tier 3도 non-interactive, 기본값 "최근 변경 중심", 가정사항 리포트 기록

### Round 7
**Q**: Tier 판별 로직을 어떻게 구성할까요?
**Options**: 1) 기존 경로 규칙 사용 2) 경로 + 내용 검증 3) 단순 존재 여부만 4) 토론 종료
**A**: 기존 경로 규칙 사용
**Follow-up**: Plan: _sdd/implementation/IMPLEMENTATION_PLAN*.md, Spec: _sdd/spec/ 내 파일 존재

### Round 8
**Q**: 기존 Tier 1 보존 전략으로 Plan not found 분기만 변경하면 안전할까요?
**Options**: 1) 해당 방식으로 충분 2) 리포트에 Tier 명시하면 충분 3) Fallback 알림 필요 4) 토론 종료
**A**: 해당 방식으로 충분
**Follow-up**: Plan 탐색 로직 자체는 손대지 않아 Tier 1 완전 보존 확인
