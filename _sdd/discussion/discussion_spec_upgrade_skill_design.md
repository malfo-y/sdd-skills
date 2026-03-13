# 토론 요약: spec-upgrade 스킬 설계

**날짜**: 2026-03-13
**라운드 수**: 3
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)
1. **스킬 필요성**: `SDD_SPEC_DEFINITION.md` 이전에 만든 구 형식 스펙을 whitepaper §1-§8로 변환하는 migration 스킬이 필요
2. **기존 스킬과의 gap**: `spec-create`는 새 스펙 생성, `spec-rewrite`는 기존 스펙 정리/분할. 구조 변환 전용 스킬이 없음
3. **설계 방향**: 코드 분석 기반 자동 초안 + 사용자 검토 Checkpoint 방식

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | In-place 덮어쓰기 + `prev/` 백업 | spec-rewrite와 동일한 안전 전략. 파일 경로 일관성 유지 | 파일 전략 |
| 2 | 코드 분석 + AI 초안 → Checkpoint | 구 스펙에 빠진 서사 섹션(§1,§2,§5)을 코드에서 추출. 사용자가 Checkpoint에서 검토 | Gap 보충 |
| 3 | 완전 독립 스킬 | spec-rewrite에 모드를 끼우면 프롬프트 복잡도 증가. 역할 분리가 명확 | 스킬 관계 |
| 4 | 멀티파일 → 통합 후 업그레이드 | 분산된 파일을 먼저 합쳐야 §1-§8 재배치 가능. 길면 후속 spec-rewrite로 분리 | 멀티파일 처리 |
| 5 | 전체 코드 매핑 (spec-create 수준) | migration이므로 한 번에 완전한 whitepaper로 변환. 부분 citation은 재작업 유발 | Citation 범위 |
| 6 | 독립 reference 복사본 | upgrade 전용 매핑 가이드 등 특화 자료 추가 가능. 스킬 간 의존성 제거 | Reference 파일 |
| 7 | 이미 whitepaper 형식이면 경고 후 사용자 판단 | 자동 중단은 부분 업그레이드 필요 시 불편. 사용자에게 선택권 제공 | 이미 완료 감지 |
| 8 | 완료 후 후속 스킬 안내만 | 자동 연계는 과도. "spec-rewrite/spec-review 가능" 안내로 충분 | 후속 연계 |

## 미결 질문 (Open Questions)
- [ ] 없음 - 모든 핵심 설계 결정 완료

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | spec-upgrade SKILL.md 작성 | High | Claude |
| 2 | references/ 디렉토리 구성 (spec-format.md, template-full.md, upgrade-mapping.md) | High | Claude |
| 3 | examples/ 디렉토리 구성 (before/after 예시) | Medium | Claude |
| 4 | README 및 workflow 문서에 spec-upgrade 추가 | Low | Claude |

## 확정된 프로세스 설계

```
Step 1: 기존 스펙 진단 (Gap Analysis)
  → 현재 스펙 파일 읽기 (단일/멀티파일 감지)
  → §1-§8 대비 매핑, 빠진 섹션 식별
  → 이미 whitepaper 형식이면 경고 + 사용자 확인
  Gate: gap 식별 완료 AND 사용자 진행 확인

Step 2: 코드베이스 분석 (Context Gathering)
  → Explore agent로 프로젝트 구조/핵심 로직 탐색
  → 빠진 §1(동기), §2(핵심 설계), §5(사용 가이드) 보충 자료 수집
  → 전체 코드 매핑용 진입점/함수/클래스 목록 수집
  Gate: 보충 자료 최소 1개 이상 수집

Step 3: Checkpoint (사용자 확인)
  → Gap 분석 결과 테이블 제시
  → AI가 생성할 서사 섹션 초안 개요 제시
  → 사용자 승인/수정 후 진행
  Gate: 사용자 승인

Step 4: 백업 & 업그레이드 실행
  → prev/PREV_<filename>_<timestamp>.md 백업 생성
  → 멀티파일이면 통합
  → 기존 내용 보존 + 빠진 섹션 생성
  → whitepaper §1-§8 구조로 재배치
  → [filepath:functionName] 코드 citation 삽입

Step 5: 검증 & 완료
  → §1-§8 필수 섹션 존재 확인
  → citation 경로 유효성 검증 (Glob)
  → 완료 요약 + 후속 스킬 안내 (spec-rewrite, spec-review)
```

## 리서치 결과 요약 (Research Findings)
- **spec-create**: 새 스펙을 §1-§8 whitepaper 구조로 생성. template-full.md 기반
- **spec-rewrite**: 기존 스펙 정리/분할. spec-format.md의 preservation rules 준수 (§1,§2,§5 절대 pruning 금지)
- **gap 확인**: 구조 변환(구 형식→whitepaper) 전용 스킬 없음. spec-rewrite는 이미 whitepaper인 스펙만 대상

## 토론 흐름 (Discussion Flow)
Round 1: [핵심 설계 3대 결정] → 파일 전략(in-place), Gap 보충(코드분석+AI), 스킬 관계(독립)
Round 2: [세부 설계 3대 결정] → 멀티파일(통합), Citation(전체매핑), References(독립복사본)
Round 3: [엣지케이스 2대 결정] → 이미 완료 감지(경고+사용자판단), 후속 연계(안내만)

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q1**: 업그레이드 시 기존 스펙 파일을 어떻게 처리할까요?
**Options**: 1) In-place 덮어쓰기 2) 새 파일 생성 3) 병합 방식
**A**: In-place 덮어쓰기 (Recommended)

**Q2**: 빠진 서사 섹션(§1,§2,§5)을 어떻게 채울까요?
**Options**: 1) 코드 분석 + AI 초안 2) 사용자 인터뷰 3) 혼합
**A**: 코드 분석 + AI 초안 (Recommended)

**Q3**: spec-rewrite와의 관계를 어떻게 설정할까요?
**Options**: 1) 완전 독립 2) spec-rewrite 내 모드 3) 파이프라인
**A**: 완전 독립 스킬 (Recommended)

### Round 2
**Q1**: 멀티파일 스펙 처리 방식?
**Options**: 1) 통합 후 업그레이드 2) 파일별 독립 3) main.md 중심
**A**: 통합 후 업그레이드 (Recommended)

**Q2**: 코드 citation 자동 생성 범위?
**Options**: 1) 핵심 진입점만 2) 전체 코드 매핑 3) Citation 생략
**A**: 전체 코드 매핑

**Q3**: Reference 파일 공유 여부?
**Options**: 1) 공유 2) 독립 복사본 3) 공유 + 전용 추가
**A**: 독립 복사본

### Round 3
**Q1**: 이미 whitepaper 형식인 스펙 감지 시?
**Options**: 1) 경고 후 사용자 판단 2) 자동 중단 3) 검사 없이 진행
**A**: 경고 후 사용자 판단 (Recommended)

**Q2**: 완료 후 후속 스킬 연계?
**Options**: 1) 안내만 2) 자동 spec-review 3) 연계 없음
**A**: 안내만 (Recommended)
