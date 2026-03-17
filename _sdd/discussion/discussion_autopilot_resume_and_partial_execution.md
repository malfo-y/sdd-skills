# 토론 요약: Autopilot 재개(Resume) 및 부분 실행 설계

**날짜**: 2026-03-17
**라운드 수**: 7
**참여 방식**: 자유 토론
**관련 문서**: `.claude/skills/sdd-autopilot/SKILL.md`, `_sdd/drafts/feature_draft_autopilot_meta_skill.md`

## 핵심 논점 (Key Discussion Points)

1. **현재 autopilot의 한계**: e2e 전제 설계로 중간 진입, 부분 실행, 재개 불가
2. **오케스트레이터와 로그의 역할 분리**: 파이프라인 정의(스킬) vs 실행 상태(로그)
3. **오케스트레이터 저장 위치 재결정**: `.claude/skills/`로 원복 (이전 토론 결정 변경)
4. **로그의 재개 메타데이터 설계**: Meta + Status 테이블 구조
5. **상태 감지 및 재개 로직**: 자동 감지 + 사용자 선택
6. **시작점/종료점 지정**: 자연어 파싱 + 산출물 스캔, 확신 없을 때만 질문

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | 오케스트레이터는 `.claude/skills/`에 저장 (원복) | 스킬로서 재사용 가능 + 재개 시 파이프라인 정의 역할. **이전 결정 변경**: `.claude/skills/` → `_sdd/pipeline/` → `.claude/skills/` | 2, 3 |
| 2 | 로그는 `_sdd/pipeline/`에 실행 상태만 추적 | 오케스트레이터(정의)와 로그(상태) 역할 분리. 로그에 파이프라인 정의를 포함하지 않음 | 2 |
| 3 | 로그 Meta: request + orchestrator 참조만. 요구사항 상세는 오케스트레이터에서 읽기 | 중복 최소화. 재개 시 오케스트레이터를 읽어야 프롬프트를 알 수 있으므로 로그에 중복 불필요 | 4 |
| 4 | Status 상태값 5개: pending / in_progress / completed / failed / skipped | 단순 유지. retrying 등 세부 상태는 Execution Log에서 추적 | 4 |
| 5 | review-fix는 Status 테이블에서 단일 스텝으로 표현 | 라운드 수가 가변(1-3회)이므로 동적 행 추가보다 단일 스텝이 깔끔. 라운드 상세는 Execution Log | 4 |
| 6 | 재개: 자동 감지 + 사용자 선택 방식 | 미완료 로그 감지 시 사용자에게 "이어서 할까요?" 제시. 자동 재개가 아닌 선택권 제공. Phase 1이 이미 interactive이므로 질문 추가 비용 낮음 | 5 |
| 7 | 시작점/종료점: 자연어 파싱 + 산출물 스캔, 확신 없을 때만 질문 | 불필요한 질문 최소화. 기존 산출물과 현재 요청의 관련성이 높으면 자동 활용, 애매하면 사용자 확인 | 6 |

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 설명 |
|---|------|---------|------|
| 1 | autopilot SKILL.md에 재개 로직 추가 | High | Step 0 (상태 감지) 추가: 로그 스캔 → 미완료 파이프라인 감지 → 사용자 선택 |
| 2 | 로그 포맷에 Meta + Status 섹션 추가 | High | 기존 Execution Log에 구조화된 메타데이터와 상태 테이블 추가 |
| 3 | autopilot SKILL.md에 시작점/종료점 로직 추가 | High | Step 1 (요청 분석)에서 산출물 스캔 + 자연어 파싱으로 파이프라인 범위 결정 |
| 4 | feature draft 업데이트 | Medium | 재개 기능 및 부분 실행 관련 Acceptance Criteria 추가 |
| 5 | 오케스트레이터 저장 위치 관련 문서 업데이트 | Done | discussion_autopilot_open_questions.md, feature_draft, SKILL.md 반영 완료 |

## 설계 상세

### 로그 포맷 (확정)

```markdown
# Pipeline Log: <topic>

## Meta
- **request**: "<사용자 원래 요청>"
- **orchestrator**: .claude/skills/orchestrator_<topic>/SKILL.md
- **scale**: <소/중/대>
- **started**: <timestamp>
- **pipeline**: <agent1> → <agent2> → ...

## Status
| Step | Agent | Status | Output |
|------|-------|--------|--------|
| 1 | feature-draft | completed | _sdd/drafts/... |
| 2 | implementation-plan | completed | _sdd/implementation/... |
| 3 | implementation | in_progress | - |
| 4 | review-fix | pending | - |
| 5 | spec-update-done | pending | - |

## Execution Log
(기존 포맷 유지 — 에이전트별 상세 기록)
```

### 재개 감지 로직 (확정)

```
autopilot 시작 시:
1. _sdd/pipeline/log_*.md 스캔
2. Status 테이블에서 미완료 스텝이 있는 로그 필터링

IF 미완료 로그 == 0:
  → 새 파이프라인 시작 (기존 동작)
IF 미완료 로그 == 1:
  → "이전 파이프라인이 있습니다. 이어서 할까요?" 제시
IF 미완료 로그 > 1:
  → 목록 제시 + "새로 시작" 옵션
IF 사용자가 재개 선택:
  → 오케스트레이터 읽기 → 마지막 completed 다음 스텝부터 실행
```

### 시작점/종료점 로직 (확정)

```
사용자 요청 분석 시:
1. 자연어에서 시작/종료 힌트 추출 ("구현부터", "리뷰까지만" 등)
2. _sdd/ 산출물 스캔 (drafts/, implementation/ 등)
3. 기존 산출물과 현재 요청의 관련성 판단

IF 관련성 높음:
  → 기존 산출물 활용, 해당 스텝 이후부터 오케스트레이터 생성
IF 관련성 불확실:
  → "기존 산출물이 있는데 활용할까요?" 질문
IF 관련성 없음:
  → 새로 시작

종료점은 오케스트레이터 생성 시 반영 → Phase 1.5에서 사용자 확인
```

## 토론 흐름 (Discussion Flow)

Round 1: 현재 autopilot의 한계 제기 → 중간 진입, 부분 실행, 재개 3가지 시나리오 식별
Round 2: 개선 방향 → A(상태 감지 자동 이어하기) + B(명시적 시작점/종료점) 조합
Round 3: 재개를 위한 로그 요구사항 → 사용자 요청, 현재 상태, 파이프라인 정보 필요
Round 4: 오케스트레이터와 로그의 역할 분리 → 오케스트레이터는 스킬(정의), 로그는 상태
Round 5: 오케스트레이터 저장 위치 → `.claude/skills/`로 원복 결정 + 문서 반영
Round 6: 로그 메타데이터 상세 설계 → Meta/Status/상태값/review-fix 표현 확정
Round 7: 시작점/종료점 → 자연어 파싱 + 산출물 스캔, 확신 없을 때만 질문

## 부록: 대화 로그 (Conversation Log)

### Round 1
**주제**: 현재 autopilot의 한계
**제기자**: 사용자
**내용**: autopilot이 e2e 전제로 설계되어 있는데, 실제로는 사용자가 일부 작업을 이미 해 두거나, 파이프라인 일부만 수행하는 등 다양한 상황이 있다.
**결과**: 3가지 시나리오 식별 — 중간 진입(이미 산출물 있음), 부분 실행(일부 스텝만), 재개(중단된 파이프라인 이어하기)

### Round 2
**주제**: 개선 방향
**내용**: A(상태 감지 + 자동 이어하기) + B(명시적 시작점/종료점 지정) 두 접근을 조합하기로 함. 단, 자동 이어하기를 위해 로그에 충분한 상태 정보가 필요.
**결과**: 두 접근 조합 결정. 로그에 원래 사용자 입력, 현재 상태, 파이프라인 정보 필요.

### Round 3
**주제**: 오케스트레이터와 로그의 역할 분리
**제기자**: 사용자
**내용**: 오케스트레이터는 스킬(파이프라인 정의)이고, 로그는 실행 상태. 파이프라인 정의를 로그에 넣는 건 역할 혼동. 오케스트레이터를 `.claude/skills/`에 넣으면 스킬로도 동작 가능.
**결과**: 오케스트레이터(정의)와 로그(상태) 명확 분리. 로그는 오케스트레이터를 참조만 함.

### Round 4
**주제**: 오케스트레이터 저장 위치 재결정
**내용**: 재사용성과 재개 기능을 고려하면 `.claude/skills/`가 적합. 이전 토론에서 `_sdd/pipeline/`로 변경했던 결정을 원복.
**결과**: `.claude/skills/orchestrator_<topic>/SKILL.md`로 확정. 관련 문서 4개 즉시 반영 완료.

### Round 5
**주제**: 로그 메타데이터 상세 설계
**내용**: 3가지 설계 질문 — (Q1) Status 상태값 개수, (Q2) review-fix 루프 표현, (Q3) 사용자 요청 저장 범위. 각각에 대해 의견 교환 후 확정.
**결과**: 상태값 5개, review-fix 단일 스텝, Meta에는 request + orchestrator 참조만 (요구사항 상세는 오케스트레이터에서 읽기).

### Round 6
**주제**: autopilot 시작 시 상태 감지 로직
**내용**: 5가지 시나리오(로그 없음, 미완료 1개, 완료됨, 여러 개, 다른 요청) 분석. 자동 재개가 아닌 감지 + 사용자 선택 방식 제안.
**결과**: 감지 + 사용자 선택 방식 확정.

### Round 7
**주제**: 명시적 시작점/종료점 지정
**내용**: A(자연어 파싱으로 범위 추론) vs B(Phase 1에서 명시적 확인) 논의. 처음에는 B를 제안했으나, 사용자가 자연어 파싱 우선 + 불확실할 때만 질문하는 방식을 선호.
**결과**: 자연어 파싱 + 산출물 스캔 기본, 확신 없을 때만 사용자에게 질문. 종료점은 오케스트레이터 생성 시 반영.
