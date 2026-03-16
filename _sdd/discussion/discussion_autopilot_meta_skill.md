# 토론 요약: SDD 스킬 → 에이전트 전환 & Autopilot 메타스킬 설계

**날짜**: 2026-03-16
**라운드 수**: 10
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)

1. **서브에이전트 호출 가능 여부**: 에이전트 정의에서 `tools`에 `"Agent"`를 포함하면 내부에서 서브에이전트 호출 가능. `write-phased` 에이전트가 이미 이 패턴을 사용 중.
2. **End-to-End 자율 개발 파이프라인**: 사용자가 "~~~ 구현하고 싶어"라고 하면 discussion → feature-draft → implementation → review → fix → test → spec-sync까지 자동으로 수행하는 파이프라인 구상.
3. **사용자 인터랙션 모델**: Phase 1(interactive)에서 discussion을 충분히 진행한 후, Phase 2(autonomous)에서는 중단 없이 자동 실행.
4. **에이전트 간 상태 전달**: `_sdd/` 디렉토리 내 파일 기반으로 각 에이전트가 결과를 저장하고 다음 에이전트가 읽는 방식.
5. **Discussion의 위치**: 에이전트로 전환하지 않고 스킬로 유지. AskUserQuestion이 핵심이므로 메인 컨텍스트에서 실행되어야 함.
6. **Meta-skill 구현 방식**: 스킬 생성형 — 요구사항 분석 후 맞춤형 오케스트레이터 스킬 파일을 동적으로 생성.
7. **적응형 파이프라인**: 규모/복잡도에 따라 필요한 에이전트만 선택하여 최적의 파이프라인 구성.
8. **테스트/디버깅 전략**: iteration이 짧으면 Claude Code 인라인 디버깅, 길면 ralph-loop-init 사용.
9. **에러 핸들링 & Review-Fix 루프**: 실패 시 로그 기록 + 디버깅 + 3회 재시도. 리뷰 루프도 최대 3회.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | 에이전트 내 서브에이전트 호출 가능 | `tools`에 `"Agent"` 포함 시 가능. write-phased가 이미 사용 중 | 1 |
| 2 | 선행 집중형 사용자 인터랙션 | Phase 1에서 discussion 완료 후, Phase 2는 완전 자율 실행 | 3 |
| 3 | Phase 2: 마일스톤 텍스트 출력 + 로그 파일 기록, 중단 없음 | 사용자가 진행 상황을 알 수 있되 흐름이 끊기지 않도록 | 3 |
| 4 | 파일 기반 에이전트 간 상태 전달 (`_sdd/` 활용) | 지속성, 디버깅 용이, 로그 역할 겸함 | 4 |
| 5 | Discussion은 스킬로 유지 (에이전트 전환 불필요) | AskUserQuestion이 메인 컨텍스트에서 실행되어야 자연스러운 대화 가능 | 5 |
| 6 | Meta-skill = 스킬 생성형 (적응형 오케스트레이터 생성) | 규모별 맞춤 파이프라인 생성이 가능. 생성된 파일이 로그/문서 역할도 함 | 6 |
| 7 | 생성된 오케스트레이터는 사용자 확인 후 실행 | discussion에서 합의했더라도 최종 파이프라인 검토 기회 제공 | 6 |
| 8 | 테스트 전략: 짧은 iteration = 인라인, 긴 iteration = ralph-loop-init | ralph-loop-init은 학습/대규모 빌드 등 장시간 디버깅 전용 | 8 |
| 9 | Review-fix 루프: 최대 3회, critical/high = 0이면 종료, minor는 로그만 | 무한 루프 방지 + 실용적 품질 기준 | 9 |
| 10 | 에러 핸들링: 로그 상세 기록 → 디버깅 → 3회 재시도 | 단순 스킵보다 능동적 해결 시도 | 9 |
| 11 | 오케스트레이터 파일 = SKILL.md 표준 포맷 | 기존 인프라 활용, Claude가 자연스럽게 해석 가능 | 6 |
| 12 | 생성된 오케스트레이터 저장 위치 = `.claude/skills/` (프로젝트 스킬) | 재사용 가능, 프로젝트 내 관리 | 6 |
| 13 | Meta-skill 이름 = **autopilot** | 사용자가 방향만 잡으면 나머지 자동이라는 의미 | 7 |
| 14 | 에이전트로 전환된 스킬도 래퍼 스킬로 유지 | write-phased 패턴 적용. 사용자가 슬래시 커맨드로 개별 호출 가능 + autopilot이 에이전트로 호출 가능 | 5, 6 |

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 설명 |
|---|------|---------|------|
| 1 | 파이프라인 필수 스킬들을 에이전트로 전환 | High | feature-draft, implementation-plan, implementation, implementation-review, ralph-loop-init, spec-update-done, spec-update-todo, spec-review |
| 2 | autopilot 메타스킬 구현 | High | 분석 → discussion → 오케스트레이터 생성 → 사용자 확인 → 실행 |
| 3 | 파이프라인 로그 시스템 구현 | Medium | `_sdd/pipeline/` 하위에 마일스톤 로그 파일 기록 |

## 리서치 결과 요약 (Research Findings)

- **코드베이스 탐색**: 20개 스킬 중 6개가 이미 서브에이전트를 사용. `write-phased` 에이전트가 `tools: ["Read", "Write", "Edit", "Glob", "Grep", "Agent"]`로 정의되어 에이전트 내 서브에이전트 호출이 이미 증명됨.

## 아키텍처 설계 (Architecture Design)

### 전체 흐름

```
User: "/autopilot 인증 시스템 구현하고 싶어"
       ↓
Phase 1: Interactive (autopilot 스킬 직접 실행)
  ├─ Discussion (inline) → 요구사항 확정
  ├─ Explore agent → 코드베이스 분석
  ├─ 규모/복잡도 판단
  └─ 오케스트레이터 스킬 파일 생성
       ↓
Phase 1.5: Checkpoint
  ├─ 생성된 파이프라인 사용자에게 제시
  └─ 사용자 확인/수정 후 실행 승인
       ↓
Phase 2: Autonomous Execution
  ├─ feature-draft agent → _sdd/drafts/
  ├─ implementation-plan agent → _sdd/implementation/
  ├─ implementation agent → 코드 생성/수정
  ├─ REVIEW-FIX LOOP (max 3회):
  │   ├─ implementation-review agent → 리뷰
  │   ├─ IF critical/high > 0: implementation agent로 수정
  │   └─ ELSE: BREAK
  ├─ 테스트/디버깅:
  │   ├─ 짧은 iteration → 인라인 디버깅
  │   └─ 긴 iteration → ralph-loop-init agent
  ├─ spec-update-done agent → 스펙 동기화
  └─ 최종 결과 요약 + 로그 파일 완성
```

### 스킬 vs 에이전트 구분

**스킬로 유지 (에이전트 전환 없음):**
- discussion (사용자 인터랙션 필요)
- git (직접 조작)
- sdd-upgrade (유틸리티)
- spec-snapshot (유틸리티)
- autopilot (메타스킬, 사용자 인터랙션 + 오케스트레이션)

**에이전트로 전환 (스킬은 래퍼로 유지):**
- feature-draft
- implementation-plan
- implementation
- implementation-review
- ralph-loop-init
- spec-update-done
- spec-update-todo
- spec-review
- write-phased (이미 완료)

> **스킬 래퍼 패턴**: 에이전트로 전환된 스킬들은 기존 스킬(`.claude/skills/`)을 삭제하지 않고, 에이전트를 호출하는 래퍼(wrapper) 형태로 유지한다. 이는 `write-phased`에서 이미 적용된 패턴으로, 스킬이 `Agent(subagent_type="<agent-name>", prompt="...")` 형태로 에이전트에 위임한다. 이를 통해 사용자는 기존처럼 `/feature-draft`, `/implementation` 등의 슬래시 커맨드로 개별 스킬을 직접 호출할 수 있고, autopilot이 에이전트를 서브에이전트로 호출하는 것도 동시에 가능하다.

### 규모별 파이프라인 예시

| 규모 | 판단 기준 | 파이프라인 |
|------|----------|-----------|
| 소규모 | 파일 1-3개, 스펙 변경 없음 | impl → 인라인 테스트 |
| 중규모 | 파일 4-10개, 스펙 패치 | feature-draft → impl-plan → impl → review → 인라인 테스트 → spec-sync |
| 대규모 | 파일 10개+, 신규 스펙 섹션 | full SDD pipeline (모든 agent 사용) |

### 상태 전달 파일 경로

```
_sdd/discussion/discussion_xxx.md    → feature-draft agent가 Read
_sdd/drafts/feature_xxx.md           → implementation-plan agent가 Read
_sdd/implementation/plan_xxx.md      → implementation agent가 Read
_sdd/pipeline/log_xxx.md             → autopilot이 마일스톤 기록
```

## 토론 흐름 (Discussion Flow)

Round 1: 토론 방향 설정 → 사용자가 end-to-end 자율 개발 파이프라인 비전 제시
Round 2: 사용자 인터랙션 모델 → 선행 집중형 선택
Round 3: Phase 2 체크포인트 → 마일스톤 텍스트 + 로그, 중단 없음
Round 4: 에이전트 간 상태 전달 → 파일 기반
Round 5: 전환 범위 → discussion은 스킬 유지, 파이프라인 필수만 에이전트 전환
Round 6: Meta-skill 설계 → 스킬 생성형 (적응형 오케스트레이터)
Round 7: 테스트 전략 확인 → 인라인 vs ralph-loop-init
Round 8: Review-fix 루프 → 최대 3회, critical 0이면 종료
Round 9: 에러 핸들링 → 로그 + 디버깅 + 3회 재시도 / 오케스트레이터 포맷 → SKILL.md 표준
Round 10: Meta-skill 이름 → autopilot / 저장 위치 → .claude/skills/

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 에이전트 내 서브에이전트 호출이 가능하다는 걸 확인했는데, 어떤 방향으로 더 논의하고 싶으신가요?
**Options**: 1) 전환 전략 2) 아키텍처 설계 3) 스킬 vs 에이전트 경계 4) 토론 종료
**A**: End-to-end 자율 개발 파이프라인 비전 제시 — discussion → feature-draft → implementation → review → fix → test → spec-sync를 한 번에 자동화하는 메타스킬 구상
**Follow-up**: 파이프라인 아키텍처 초안 제시, 핵심 도전 2가지(사용자 인터랙션, 상태 전달) 식별

### Round 2
**Q**: 이 파이프라인에서 가장 핵심적인 도전은 '사용자 인터랙션 처리'와 '에이전트 간 상태 전달'입니다. 어떤 부분을 먼저 논의할까요?
**Options**: 1) 사용자 인터랙션 2) 상태 전달 설계 3) 둘 다 논의 4) 토론 종료
**A**: 사용자 인터랙션
**Follow-up**: 서브에이전트 내 AskUserQuestion 작동 확인. 3가지 핵심 문제 제시.

### Round 3
**Q**: 사용자 인터랙션을 어떻게 처리하고 싶으세요?
**Options**: 1) 선행 집중형 2) 체크포인트형 3) 완전 자동화 4) 토론 종료
**A**: 선행 집중형
**Follow-up**: Phase 1(interactive) / Phase 2(autonomous) 2페이즈 아키텍처 확정

### Round 4
**Q**: Phase 2 자율 실행 중에도 사용자 확인이 필요한 시점이 있을까요?
**Options**: 1) 완전 자동 2) 주요 마일스톤만 보고 3) 핵심 체크포인트 설정 4) 토론 종료
**A**: 주요 마일스톤을 텍스트로 출력하고 중간 log 파일로 기록. 중단 없이 계속 진행.
**Follow-up**: 마일스톤 보고 + 로그 파일 기록 방식 확정

### Round 5
**Q**: 에이전트 간 상태 전달을 어떻게 하고 싶으세요?
**Options**: 1) 파일 기반 2) 프롬프트 전달 3) 하이브리드 4) 토론 종료
**A**: 파일 기반
**Follow-up**: _sdd/ 디렉토리 구조와 맞는 자연스러운 확장 확인

### Round 6
**Q**: 20개 스킬 중 어떤 것들을 에이전트로 전환해야 할까요?
**Options**: 1) 파이프라인 필수만 2) 전체 전환 3) 단계적 전환 4) 토론 종료
**A**: discussion은 agent로 전환 불필요. spec-update-todo, implementation-plan, spec-review 등은 전환 필요.
**Follow-up**: 스킬/에이전트 구분표 작성, meta-skill 설계 방향 논의 시작

### Round 7
**Q**: Meta-skill의 구현 방식을 어떻게 보세요?
**Options**: 1) 조건부 실행형 2) 스킬 생성형 3) 하이브리드 4) 토론 종료
**A**: 스킬 생성형
**Follow-up**: 적응형 오케스트레이터 생성 흐름 설계. 테스트 전략 (인라인 vs ralph-loop-init) 확인.

### Round 8
**Q**: 생성된 오케스트레이터를 사용자가 리뷰한 후 실행할까요?
**Options**: 1) 생성 후 확인 후 실행 2) 자동 실행 3) 규모별 차등 4) 토론 종료
**A**: 생성 후 확인 후 실행
**Follow-up**: Phase 1.5 (사용자 확인 체크포인트) 추가

### Round 9
**Q**: Review-fix 루프의 종료 조건을 어떻게 설정할까요? / 에러 핸들링 / 오케스트레이터 파일 포맷
**A**: 최대 3회 + critical 0 종료 / 로그 + 디버깅 + 3회 재시도 / SKILL.md 표준 포맷
**Follow-up**: 모든 미결 사항 해결 확인

### Round 10
**Q**: Meta-skill 이름 / 생성된 오케스트레이터 저장 위치
**A**: autopilot / .claude/skills/ 프로젝트 스킬로 저장
**Follow-up**: 토론 종료 및 요약 정리
