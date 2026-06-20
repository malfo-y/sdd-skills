# 토론 요약: AGENTS.md에 work_log 하네스 추가

**날짜**: 2026-06-20
**라운드 수**: 4
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)
- **사용자 문제 제기**: AGENTS.md에 work log 하네스를 추가하고 싶다. 이 레포에서 하는 작업들을 `_sdd/work_log/<yyyy-mm-dd>.md`에 기록하는 규약.
- **토론을 시작한 배경**: AGENTS.md가 이 repo의 작업 하네스 단일 소스(how). 작업 추적/기록 관습을 하네스에 명문화하려는 것. 나중에 "내가 언제 뭘 했나"를 만약의 상황에서 찾아보기 위한 포렌식 기록이 목적.
- **현재 상태**:
  - AGENTS.md는 29줄, 의도적으로 압축. how(작업 규약)만 담고 what/why·guardrail은 `_sdd/spec/`로 위임. "복사 금지, 가리키기" 원칙.
  - `_sdd/work_log/` 디렉토리 없음 (신규).
  - `_sdd/pipeline/`에 `log_*.md`/`report_*.md`/`orchestrators/`가 **이미 존재** — 단 이는 **sdd-autopilot 오케스트레이터 파이프라인 전용**(per-pipeline, Meta+Status 테이블, autopilot이 재개 감지에 스캔). work_log와는 목적·입도가 다름.
- **범위와 제외 범위**:
  - 포함: work_log 기록 규약을 AGENTS.md에 얇게 추가 + work_log 디렉토리/포맷 정의.
  - 제외: 기존 pipeline log 관습 변경, work_log를 living doc으로 관리하는 프로세스(의도적으로 안 함).
- **수집한 근거**: AGENTS.md 직접 확인(`코드 확인`), `_sdd/pipeline/log_*.md` 포맷 및 spec 내 pipeline 참조 확인(`코드 확인`).

## 핵심 논점 (Key Discussion Points)
1. **동기**: work_log를 따로 두는 이유 → 수동 작업까지 포함한 일일 작업 일지. pipeline log(autopilot 전용)로는 커버 안 됨.
2. **기존 관습과의 관계**: `_sdd/pipeline/log_*.md`는 autopilot 전용·per-pipeline. work_log는 per-day·수동 포함으로 별개 트랙.
3. **기록 트리거**: "의미 있는 작업 단위 종료 시" append. (단위 판단 여지가 넓어 내용 규칙으로 구체화 필요 → 논점 5에서 해소)
4. **AGENTS.md에 담는 방식**: 얇은 규약만 AGENTS.md, 상세 포맷은 `_sdd/work_log/` 템플릿이 단일 소스 (가리키기 원칙 유지).
5. **내용 규칙 / 썩음 위험**: work_log는 포렌식 기록이라 썩는 것을 감수. 고유 가치는 *쓰는 시점*. 포인터 우선 원장으로 설계해 중복 최소화.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| 1 | work_log = 수동 작업 포함 **일일 포렌식 일지**. "언제 뭘 했나" 나중에 찾아보는 용도이지 관리/조회 대상 아님. 썩는 것 감수. | 사용자 판단 | 1, 5 |
| 2 | pipeline log(autopilot 전용)와 **별개 트랙**으로 공존. work_log는 per-day·수동 포함. | 코드 확인 (pipeline log가 autopilot 전용임을 확인) | 2 |
| 3 | 기록 트리거 = **의미 있는 작업 단위 종료 시** append. | 사용자 판단 | 3 |
| 4 | AGENTS.md에는 **얇은 규약(트리거+위치)만**, 상세 포맷은 `_sdd/work_log/`의 템플릿/README가 단일 소스 (방식 A). | 사용자 판단 / 코드 확인 (AGENTS 가리키기 원칙) | 4 |
| 5 | 항목 내용 규칙 = ① 무엇을/왜 했고 어떻게 됐는지 ② 관련 문서·커밋·decision log 있으면 그 지점을 **포인터(링크)** ③ 따로 남은 게 없으면 관련 내용을 **요약해 인라인**(fallback). → 포인터 우선 원장. | 사용자 판단 | 5 |
| 6 | AGENTS.md 통합은 **쓰기 규약만**, §1 "작업 시작 시 읽는 순서"에는 **제외**(포렌식 기록이라 매번 읽을 필요 없음, on-demand 읽기). | 사용자 판단 | 4 |

### 기각한 대안
- **방식 B (AGENTS.md에 규약+포맷 전체 인라인)**: 29줄 minimal 원칙·"복사 금지"와 정면 충돌, bloat 위험.
- **방식 C (규약 본체를 `_sdd/spec/`에)**: work_log는 how(작업 규약)이지 what/why가 아님 → spec에 두면 "how=AGENTS, what/why=spec" 경계가 흐려짐.
- **트리거: 커밋 시점마다 append**: 커밋 안 하는 작업(토론·조사)이 누락됨. 일일 일지 목적과 안 맞음.
- **트리거: 세션 종료 시 일괄**: 세션 경계가 모호하고 중간에 끊기면 유실.
- **내용: 하루 전체 내러티브(커밋 포함 전부)**: git log와 중복, 유지비용 높고 더 빨리 썩음.

## 미결 질문 (Open Questions)
없음 (in-scope 미결 0건).

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | AGENTS.md(SDD-HARNESS 마커 내부, §2 근처)에 얇은 work_log 쓰기 규약 추가. §1 읽기 순서엔 미포함. | High | 후속 |
| 2 | `_sdd/work_log/` 디렉토리 + 항목 포맷 템플릿/README 생성(단일 소스). | High | 후속 |
| 3 | 항목 템플릿 구체 형태 확정(아래 핸드오프의 초안 기준). | Medium | 후속 |

### 후속 핸드오프 (Handoff)
- **목표**: AGENTS.md에 work_log 쓰기 규약을 얇게 추가하고, `_sdd/work_log/`에 포맷 단일 소스(템플릿/README)를 만든다. 완료 기준: (a) AGENTS.md SDD-HARNESS 블록 안에 트리거+위치 2~3줄 규약이 있고 §1 읽기 순서에는 없다, (b) `_sdd/work_log/` 템플릿이 항목 포맷을 정의한다, (c) AGENTS.md는 포맷을 복사하지 않고 템플릿을 가리킨다.
- **AGENTS.md 규약 초안** (방식 A, 가리키기):
  ```
  ## N. 작업 기록 (work log)
  - 의미 있는 작업 단위를 끝낼 때 `_sdd/work_log/<yyyy-mm-dd>.md`에 항목을 append 한다(없으면 그날 파일 생성).
  - 포렌식 기록이다 — 관리/조회용 아님. §1 읽기 대상 아님(필요할 때만 on-demand).
  - 항목 포맷·작성 규칙은 `_sdd/work_log/`의 템플릿이 단일 소스.
  ```
- **항목 템플릿 초안** (`_sdd/work_log/`의 단일 소스가 정의):
  ```
  ## <순번 또는 HH:MM> <한 줄 제목>
  - 무엇/왜: <무엇을 왜 했는지>
  - 결과: <어떻게 됐는지>
  - 포인터: <커밋 해시 / _sdd/... 문서 / decision log §>  (있으면 링크, 인라인 중복 금지)
  - 요약: <따로 남은 문서가 없을 때만 관련 내용 요약 인라인>
  ```
- **변경 금지 제약**: `_sdd/pipeline/log_*.md` 등 autopilot 파이프라인 로그 관습은 건드리지 않는다(별개 트랙). AGENTS.md의 "복사 금지·가리키기" 원칙과 29줄 minimal 기조를 깨지 않는다 — 포맷 본문을 AGENTS.md에 인라인하지 말 것. §1 읽기 순서에 work_log를 넣지 말 것.
- **검증**: AGENTS.md diff가 SDD-HARNESS 마커 안에서만 변경됐는지 확인 + 규약이 포맷을 복사하지 않고 가리키는지 grep. work_log 항목을 1건 시범 작성해 템플릿이 따라 쓰기 쉬운지 확인.
- **중단 조건**: 토론 결정과 모순되는 요구(예: work_log를 §1 읽기 순서에 넣기, AGENTS.md에 포맷 전체 인라인, pipeline log와 통합)가 나오면 멈추고 보고.

## 리서치 결과 요약 (Research Findings)
- **AGENTS.md 구조**: 29줄. §0 작업원칙 / §1 읽는 순서 / §2 작업규약·검증 / §3 SDD 워크플로우 / §4 판단기준 가리키기. SDD-HARNESS:START~END 마커로 감쌈. "복사 금지, 가리키기" 일관 적용. (`코드 확인`)
- **기존 로깅 관습**: `_sdd/pipeline/log_*.md`는 autopilot 오케스트레이터가 per-pipeline로 남기는 상태 추적 로그(Meta+Status 테이블, 5개 상태값). autopilot이 Step 0에서 미완료 파이프라인 재개 감지에 스캔. work_log와 목적·입도 상이 → 별개 트랙으로 결론. (`코드 확인`)

## 토론 흐름 (Discussion Flow)
- Round 1: 동기 탐색 → "수동 작업 포함 일일 작업 일지"로 확정, pipeline log와 분리.
- Round 2: 기록 트리거 → "의미 있는 작업 단위 종료 시".
- Round 3: AGENTS.md에 담는 방식 → 방식 A(얇은 규약 + 템플릿 단일 소스).
- Round 4(비판적 검토): 썩음/중복 위험 제기 → 사용자가 포렌식 목적임을 명확히(썩음 감수), 포인터 우선 내용 규칙 확정. AGENTS 통합은 쓰기 규약만·§1 제외로 결정.

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: work_log를 따로 두려는 핵심 동기가 뭔가요? (이미 pipeline/log_*.md가 있는데)
**Options**: 1) 수동 작업까지 포함한 일일 작업 일지 2) 세션 간 연속성/컨텍스트 인계 3) 감사/추적용 변경 이력 4) 아직 모호함
**A**: 수동 작업까지 포함한 일일 작업 일지.
**Follow-up**: pipeline log(autopilot 전용)와 목적이 다른 별개 트랙으로 확정.

### Round 2
**Q**: work_log 항목이 *언제* 기록되게 할까요?
**Options**: 1) 커밋 시점마다 2) 의미 있는 작업 단위 종료 시 3) 세션 종료 시 4) 수동 호출로만
**A**: 의미 있는 작업 단위 종료 시.
**Follow-up**: "단위" 판단 여지가 넓음 → 내용 규칙으로 구체화 필요 표시.

### Round 3
**Q**: work_log 규약을 AGENTS.md에 어떻게 담을까요?
**Options**: A) 얇은 규약+템플릿 단일소스 B) 전체 인라인 C) spec에 본체
**A**: A (권장안).
**Follow-up**: 가리키기 원칙 유지로 확정.

### Round 4 (비판적 검토)
**Q(비판)**: work_log가 git log·discussion 요약·pipeline log와 중복돼 썩는 산출물이 될 위험. git이 안 보여주는 것만 담아 구별해야 하지 않나?
**A(사용자)**: 썩는 거 안다/감수한다. 목적은 "언제 뭘 했나" 나중에 찾아보는 포렌식. 관리 목적 아님. 내용은 ① 무엇/왜/결과 ② 관련 문서·커밋·decision log 있으면 포인트 ③ 없으면 요약 인라인.
**Follow-up**: 우려 철회. 포인터 우선 원장으로 내용 규칙 확정. AGENTS 통합은 쓰기 규약만·§1 읽기 순서 제외로 결정(포렌식이라 매번 읽을 필요 없음).
