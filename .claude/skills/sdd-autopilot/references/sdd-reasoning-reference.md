# SDD Reasoning Reference

## Part 1: SDD 철학

### 1.1 핵심 원칙 (3개)

1. **Spec is Source of Truth** -- 코드는 결과물. 스펙이 진실의 공급원.
2. **중요한 결정은 Spec에 남긴다** -- 누가/언제 구현해도 같은 결론에 도달.
3. **검증 기준도 Spec에 둔다** -- 리뷰/테스트의 질문이 "그럴듯한가?"가 아니라 "계약을 지키는가?"

운영 대원칙: **AI가 만든 Spec도 사람 승인 없이는 확정하지 않는다.** (환각이 계약으로 굳는 것이 가장 위험)

### 1.2 AI 실패 패턴과 SDD 처방

| 실패 패턴 | 현상 | SDD 처방 |
|-----------|------|----------|
| 해석의 표류 | 같은 요구인데 구현 결정이 매번 달라짐 | spec에 결정을 고정하여 결정론적 재사용 |
| 컨텍스트 윈도우 한계 | 레포가 커질수록 맥락을 잃고 중복 생성 | spec이 필수 맥락의 압축본 역할 |
| 환각 | 존재하지 않는 API/라이브러리 생성 | I/O, 계약, 제약을 spec에 명시해 검증 가능하게 |

**용어 요약:**
- **계약(Contract)**: 전제조건(Pre), 사후조건(Post), 불변조건(Invariants) -- "맞/틀"을 판정할 수 있는 약속
- **제약(Constraints)**: 구현이 절대 넘으면 안 되는 경계/가드레일 (성능, 보안, 의존성 등)
- **검증 가능(Verifiable)**: 테스트/정적검사/체크리스트로 기계적 변환이 가능한 상태

### 1.3 두 단계 스펙 구조

- **글로벌 스펙** (`_sdd/spec/main.md`): 안정적 SoT. 직접 수정 금지. spec-update-todo/done으로만 변경.
- **임시 스펙** (`feature_draft`, `spec_patch_draft`): 변경의 청사진. Git feature branch처럼 생성->검증->구현->병합->아카이브.

**임시 스펙 생명주기:**
```
생성(feature-draft) -> 검증(사용자 확인) -> 구현(implementation) -> 병합(spec-update-done) -> 아카이브(prev/)
```

**글로벌 스펙 = CLAUDE.md 대체**: CLAUDE.md는 포인터로만 사용하고, 프로젝트의 목표/아키텍처/컴포넌트 상세 등 모든 정보를 글로벌 스펙에 담는다.

**왜 직접 수정 금지인가:**
- 임시 스펙이 구현의 청사진 역할 -> 구현 전에 명확한 기준
- 변경 추적 가능 (무엇이 왜 바뀌었는지)
- 원본 보존 (prev/로 복구 가능)

### 1.4 제어 장치 (Control Plane)

SDD는 "문서화 기법"이 아니라 아키텍처 제어 장치다.

1. **의도(What) vs 구현(How) 분리** -- Spec은 what(Goal/Contract/Invariants), 구현은 how(언어/프레임워크). 기술이 바뀌어도 의도 유지.
2. **표류 감지(Drift detection)** -- Spec<->코드 정합성 모니터링. CI/리뷰에서 지속 확인. "한 번 리뷰하고 끝"이 아님.
3. **가드레일(Guardrails)** -- 금지 패턴/원칙/제약을 Spec에 명시하여 AI 자유도 제한. AI는 패턴 인식/구현에 강하지만 의도 추측에 한계.

### 1.5 스펙 정의 (화이트페이퍼형)

SDD 스펙은 단순 문서가 아니라, 문제/동기/핵심 설계/기대 동작/코드 근거를 함께 담는 화이트페이퍼형 SoT.

**5가지 필수 축:**

1. **배경 및 동기** -- 해결 문제, 왜 지금, 대안 대비 이유
2. **핵심 설계** -- 시스템 핵심 아이디어, 주요 로직 흐름
3. **구현 근거와 코드 매핑** -- 설명<->실제 코드 연결, 인라인 citation (`[filepath:functionName]`)
4. **사용 가이드와 기대 결과** -- 시나리오, 기대 결과, 실패/예외 보장
5. **보조 참조 정보** -- 데이터 모델, API 참조, 환경/설정

**권장 구조 (8 섹션):**

| 섹션 | 내용 |
|------|------|
| 1. Background | 배경/동기/문제 정의 |
| 2. Design | 핵심 설계/아이디어 |
| 3. Architecture | 아키텍처 상세 |
| 4. Components | 컴포넌트 상세 (I/O/의존성) |
| 5. Usage | 사용 가이드/기대 결과 |
| 6. Data | 데이터 모델 |
| 7. API | API 참조 |
| 8. Config | 환경/설정 |

**과잉 스펙 방지**: Spec은 모든 설명이 아니라 결정/계약/제약의 압축본. MUST(검증 대상)와 설명(참고)을 분리. 구현 지시(How)는 금지.

### 1.6 파이프라인 구성 원칙

1. **Spec-first**: 스펙 없으면 구현 전에 spec-create 선행.
2. **드리프트 방지**: 대규모 변경은 spec-update-todo로 사전 등록.
3. **Review-fix 필수**: 리뷰만 하고 끝나지 않음. review -> fix -> re-review 사이클.
4. **Execute->Verify**: 에이전트 호출 != 완료. Exit Criteria 충족 필수.
5. **파일 기반 handoff**: 경로만 전달, 컨텍스트 누적 금지.
6. **스펙 직접 수정 금지**: spec 변경은 spec-update-todo/done으로만.

---

## Part 2: 스킬 카탈로그

### 2.1 스킬 의존성 그래프

```
spec-create -> feature-draft -> spec-update-todo -> impl-plan -> impl -> impl-review -> spec-update-done
                                                                            |  (review-fix loop)
                                                                  ralph-loop-init (장시간 테스트)
```

discussion은 어디서든 선행 가능 (방향 불확실 시).
guide-create, spec-review는 파이프라인 끝에 선택적 추가.
write-skeleton은 다른 스킬의 하위 도구로 skeleton 생성 + 반환.

### 2.2 오케스트레이션 대상 스킬 (8개)

autopilot이 생성한 오케스트레이터 파이프라인에 조합하는 스킬.

> **전제 조건**: 글로벌 스펙(`_sdd/spec/main.md`)이 존재해야 한다. 스펙이 없으면 오케스트레이터 생성을 중단하고, 사용자에게 `/spec-create` 실행을 안내한다.

#### feature-draft

- **Role**: 스펙 패치 초안 + 구현 계획을 한 번에 생성
- **Agent**: `feature-draft`
- **Input**: 사용자 요청 + `_sdd/spec/main.md`
- **Output**: `_sdd/drafts/feature_draft_<topic>.md`
- **Pre-condition**: 글로벌 스펙 존재
- **Post-condition**: feature_draft 파일 존재 + 요구사항/제약조건 섹션 비어있지 않음
- **Reasoning note**: 중규모 이상 기능의 시작점. 스펙 패치와 구현 계획을 통합 생성.

#### spec-update-todo

- **Role**: 계획된 기능을 글로벌 스펙에 사전 반영 (계획됨 상태)
- **Agent**: `spec-update-todo`
- **Input**: `_sdd/drafts/feature_draft_<topic>.md` + `_sdd/spec/main.md`
- **Output**: `_sdd/spec/main.md` (업데이트)
- **Pre-condition**: feature_draft 존재
- **Post-condition**: 스펙에 계획된 항목이 추가됨
- **Reasoning note**: 대규모 구현에서 장기간 구현 중 드리프트 방지. 중규모에서는 생략 가능.

#### spec-update-done

- **Role**: 구현 완료 후 글로벌 스펙 동기화
- **Agent**: `spec-update-done`
- **Input**: `_sdd/spec/main.md` + 구현된 코드 파일
- **Output**: `_sdd/spec/main.md` (업데이트)
- **Pre-condition**: 구현 완료
- **Post-condition**: 스펙이 실제 구현과 정합
- **Reasoning note**: 파이프라인의 마지막(또는 마지막 직전) 단계. 스펙<->코드 동기화.

#### spec-review

- **Role**: 스펙 품질/드리프트 보조 검증 (리포트 전용, 수정 없음)
- **Agent**: `spec-review`
- **Input**: `_sdd/spec/main.md` + 코드
- **Output**: 리뷰 리포트 텍스트
- **Pre-condition**: 스펙 존재
- **Post-condition**: 리뷰 결과가 반환됨 + 드리프트/품질 이슈 분류
- **Reasoning note**: 대규모 업데이트 후 최종 검증. 선택적 단계.

#### implementation-plan

- **Role**: phase별 상세 구현 계획 수립
- **Agent**: `implementation-plan`
- **Input**: `_sdd/drafts/feature_draft_<topic>.md` + `_sdd/spec/main.md`
- **Output**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- **Pre-condition**: feature_draft 존재
- **Post-condition**: 구현 계획 존재 + 태스크 1개 이상 정의
- **Reasoning note**: 대규모 구현에서 phase별 계획 필요 시. 중규모에서는 feature-draft의 Part 2가 대체.

#### implementation

- **Role**: TDD 기반 코드 구현
- **Agent**: `implementation`
- **Input**: `_sdd/implementation/IMPLEMENTATION_PLAN.md` 또는 feature_draft
- **Output**: 코드 파일들
- **Pre-condition**: 구현 계획 또는 feature_draft 존재
- **Post-condition**: 구현 대상 파일 생성/수정 + 구문 에러 없음
- **Reasoning note**: 실제 코드를 생성/수정하는 핵심 단계.

#### implementation-review

- **Role**: 구현 결과를 계획/스펙 대비 리뷰
- **Agent**: `implementation-review`
- **Input**: `_sdd/implementation/` + 코드 파일
- **Output**: 리뷰 리포트 (critical/high/medium/low 심각도 포함)
- **Pre-condition**: 구현 완료
- **Post-condition**: 리뷰 결과에 심각도 분류 포함
- **Reasoning note**: review-fix loop의 일부. 파이프라인에 review 포함 시 핵심 단계.

#### ralph-loop-init

- **Role**: 장시간 자동 디버깅 루프 설정 + 실행
- **Agent**: `ralph-loop-init`
- **Input**: 코드 파일 + 테스트/학습 명령
- **Output**: `ralph/` 디렉토리 (run.sh, state.md, PROMPT.md)
- **Pre-condition**: 구현 완료 + 반복 검증이 필요한 상황
- **Post-condition**: ralph/ 존재 + run.sh 실행 가능 + state.md 존재
- **Reasoning note**: 반복 실행→분석→수정 사이클이 필요한 경우 사용 (ML 학습, E2E 테스트, 빌드 파이프라인, 통합 검증 등).

### 2.3 비오케스트레이션 스킬 (참고용 목록)

autopilot이 오케스트레이터 파이프라인에 넣지 않는 스킬. 사용자가 독립적으로 호출하거나 autopilot이 인라인으로 처리.

| 스킬 | 용도 | 비고 |
|------|------|------|
| spec-create | 글로벌 스펙 최초 생성 | autopilot 전제 조건 — 스펙 없으면 오케스트레이터 생성 중단 후 사용자에게 안내 |
| discussion | 구조화 의사결정 토론 | autopilot Step 2에서 인라인 처리 (에이전트 위임 아님) |
| guide-create | 기능별 구현/리뷰 가이드 생성 | 파이프라인 끝나고 사용자가 독립 실행 |
| write-skeleton | skeleton 생성 + 반환 | 다른 에이전트의 하위 도구로 skeleton 생성 후 반환 |
| git | 커밋/브랜치 자동화 | |
| pr-spec-patch | PR과 스펙 비교하여 패치 초안 생성 | |
| pr-review | PR 구현을 스펙 대비 검증 | |
| spec-summary | 스펙 요약본 생성 | |
| spec-snapshot | 스펙 번역/스냅샷 | |
| spec-rewrite | 긴 스펙 구조 재정리 | |
| spec-upgrade | 구 형식 스펙을 권장 구조로 변환 | |

### 2.4 에이전트 목록 (8개)

오케스트레이터 파이프라인에서 spawn하는 에이전트.

| 에이전트 | subagent_type |
|---------|---------------|
| feature-draft | `sdd-skills:feature-draft` |
| implementation-plan | `sdd-skills:implementation-plan` |
| implementation | `sdd-skills:implementation` |
| implementation-review | `sdd-skills:implementation-review` |
| spec-update-done | `sdd-skills:spec-update-done` |
| spec-update-todo | `sdd-skills:spec-update-todo` |
| spec-review | `sdd-skills:spec-review` |
| ralph-loop-init | `sdd-skills:ralph-loop-init` |

보조 에이전트: `Explore` (코드베이스 탐색), `sdd-skills:write-skeleton` (skeleton 생성 + 반환), `general-purpose` (범용 리서치)

### 2.5 파이프라인 구성 가이드라인

**중요**: 아래는 템플릿이 아니라 가이드라인이다. autopilot은 상황에 맞게 비표준 조합도 가능.

#### 소규모 (1-3파일, 스펙 변경 없음)

```
implementation -> 인라인 테스트
```
- 정량: 영향 파일 1-3개, 신규 컴포넌트 0-1개
- 정성: 단일 함수/클래스 수정, 기존 코드 내 수정
- review 미포함이 기본. 사용자 요청 시 review-fix loop 추가.

#### 중규모 (4-10파일, 스펙 패치)

```
feature-draft -> impl -> review-fix -> spec-update-done
```
- feature-draft가 스펙 패치 + 구현 계획을 통합 생성하므로 별도 impl-plan 불필요
- 정량: 영향 파일 4-10개, 신규 컴포넌트 1-3개
- 정성: 여러 모듈 연동, 새 API 엔드포인트

#### 대규모 (10+파일, 신규 스펙 섹션)

```
feature-draft -> spec-update-todo -> impl-plan -> impl -> review-fix -> test -> spec-update-done
```
- spec-update-todo로 장기 구현 중 드리프트 방지
- impl-plan으로 phase별 상세 계획
- 정량: 영향 파일 10+, 신규 컴포넌트 3+
- 정성: 아키텍처 레벨 변경, 새 시스템 도입

#### 특수 패턴

- **스펙 없음**: spec-create를 가장 먼저 선행
- **방향 불확실**: discussion을 선행 (autopilot에서는 인라인)
- **반복 검증/E2E/장시간 테스트**: ralph-loop-init을 테스트 단계에 배치 (ML 학습뿐 아니라 E2E·통합 검증에도 적극 고려)
- **부분 파이프라인**: 사용자가 시작점/종료점 지정 시 해당 범위만 구성
- **파이프라인 재개**: 기존 로그/산출물 스캔 후 중단점부터 재개

#### 경계 사례 규칙

- 정량/정성 불일치 -> 더 큰 규모 선택
- 확신 없음 -> 중규모 기본값
- "빠르게/간단히" -> 한 단계 낮추기 고려
- 순수 신규 생성 -> 파일 수 기준 한 단계 완화

### 2.6 테스트 전략 판단

| 조건 | 전략 |
|------|------|
| 단순 단위 테스트/린트 + 1회 실행으로 결과 확정 | **인라인 디버깅** |
| 반복 실행→분석→수정 사이클이 필요 / 장시간 실행 / 외부 환경 필요 | **ralph-loop-init** |

#### 힌트 기반 가이드라인

아래는 가이드라인이지 고정 규칙이 아니다. LLM이 프로젝트 특성을 분석하여 자율적으로 판단한다.

**ralph-loop-init 고려 상황:**
- 반복 검증이 필요한 프로세스 (실행 → 분석 → 수정 사이클 3회+ 예상)
- E2E 테스트, 통합 테스트 등 여러 컴포넌트 연동 검증
- 장시간 실행 프로세스 (학습, 대규모 테스트 스위트, 빌드 파이프라인)
- 환경 격리가 필요한 경우 (GPU, 원격 서버, 컨테이너)
- 자율 디버깅이 효과적인 경우 (에러 패턴이 반복적)

**인라인 디버깅 적합 상황:**
- 단순 단위 테스트, 린트 등 1회 실행으로 결과 확정
- 로컬에서 즉시 실행 가능 + 수분 이내 완료
- 반복 수정 사이클이 불필요한 경우
