# 토론 요약: Autopilot Feature Draft Open Questions 해결

**날짜**: 2026-03-16
**라운드 수**: 6
**참여 방식**: 구조화된 토론 (discussion skill)
**관련 문서**: `_sdd/drafts/feature_draft_autopilot_meta_skill.md`

## 핵심 논점 (Key Discussion Points)

1. **Codex 스킬 동기화**: `.codex/skills/`에 래퍼 패턴을 적용할지 여부
2. **Agent 정의에 references/examples 포함 방식**: 인라인 vs Read 참조
3. **래퍼 스킬 버전 관리**: 전환 시 version 변경 여부
4. **오케스트레이터 생성 위치**: `.claude/skills/` vs `_sdd/pipeline/`
5. **대규모 파이프라인 컨텍스트 관리**: 10개+ 에이전트 순차 호출 시 전략
6. **파이프라인 실행 로그**: 각 에이전트의 핵심 결정사항 기록 방식

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | Codex는 기존 유지 (풀 SKILL.md) | Codex는 Agent 도구를 제한적으로 지원하므로 래퍼 패턴이 동일하게 동작하지 않음. 에이전트 전환은 Claude Code 전용 | 1 |
| 2 | references/examples는 Read로 참조 | 에이전트 본문에는 SKILL.md 로직만 포함. references/examples는 기존 `.claude/skills/<name>/references/` 경로에서 Read로 읽도록 지시. 컨텍스트 효율적 | 2 |
| 3 | 래퍼 전환 시 Minor 버전 업 (1.0.0 → 1.1.0) | 기능은 동일하지만 구조가 변경되었음을 표시. skill.json도 함께 업데이트 | 3 |
| 4 | 오케스트레이터는 `_sdd/pipeline/`에 저장 | 일회성 실행 계획이므로 스킬 디렉토리를 오염시키지 않음. 로그와 함께 관리. **이전 토론 결정 #12 변경** (기존: `.claude/skills/` → 변경: `_sdd/pipeline/`) | 4 |
| 5 | 파일 기반 전달로 컨텍스트 관리 충분 | 부모(autopilot)는 각 에이전트에 파일 경로만 전달. 에이전트는 자체 컨텍스트에서 파일을 Read. 부모 컨텍스트 누적 최소화 | 5 |
| 6 | 공유 로그 파일 방식으로 실행 로그 기록 | autopilot이 `_sdd/pipeline/log_<topic>_<timestamp>.md`를 생성하고, 각 에이전트 결과를 받을 때마다 핵심 결정사항을 추출하여 로그에 추가. 에이전트는 로그를 모름 | 6 |

## 미결 질문 (Open Questions)

없음 — 모든 Open Questions 해결 완료.

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 설명 |
|---|------|---------|------|
| 1 | feature draft Open Questions 업데이트 | High | `_sdd/drafts/feature_draft_autopilot_meta_skill.md`의 Open Questions 섹션을 결정 사항으로 교체 |
| 2 | 이전 토론 결정 #12 수정 | Medium | `_sdd/discussion/discussion_autopilot_meta_skill.md`의 결정 사항 #12를 `_sdd/pipeline/`로 업데이트 |

## 토론 흐름 (Discussion Flow)

Round 1: Codex 동기화 → Codex는 기존 유지
Round 2: references/examples 포함 방식 → Read로 참조
Round 3: 래퍼 스킬 버전 관리 → Minor 버전 업
Round 4: 오케스트레이터 생성 위치 → `_sdd/pipeline/`
Round 5: 컨텍스트 관리 → 파일 기반 전달로 충분
Round 6: 파이프라인 실행 로그 → 공유 로그 파일, autopilot이 결정사항 추출

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: Codex 스킬 동기화. `.codex/skills/`에도 래퍼 패턴을 적용할까요?
**Options**: 1) Codex는 기존 유지 2) Codex도 래퍼 적용 3) Codex 지원 중단 4) 토론 종료
**A**: Codex는 기존 유지
**Follow-up**: Codex는 Agent 도구 제한으로 래퍼 동일 동작 불가. Claude Code 전용 전환으로 결정.

### Round 2
**Q**: Agent 정의에 references/examples 포함 방식?
**Options**: 1) 에이전트 본문에 인라인 2) Read로 참조 3) 하이브리드 4) 토론 종료
**A**: Read로 참조
**Follow-up**: 에이전트 본문은 SKILL.md 로직만 포함. references/examples는 기존 경로에서 Read.

### Round 3
**Q**: 래퍼 스킬 버전 관리?
**Options**: 1) Major 버전 업 2) 버전 유지 3) Minor 버전 업 4) 토론 종료
**A**: Minor 버전 업
**Follow-up**: 1.0.0 → 1.1.0. 기능 동일, 구조 변경 표시.

### Round 4
**Q**: 오케스트레이터 생성 위치?
**Options**: 1) _sdd/pipeline/ 2) .claude/skills/generated/ 3) 둘 다 4) 토론 종료
**A**: _sdd/pipeline/
**Follow-up**: 이전 토론 결정 #12 (.claude/skills/) 변경. 일회성 실행 계획이므로 _sdd/pipeline/이 적절.

### Round 5
**Q**: 대규모 파이프라인 컨텍스트 관리?
**Options**: 1) 파일 기반 전달로 충분 2) 요약 체인 3) 컨텍스트 윈도우 제한 4) 토론 종료
**A**: 파일 기반 전달로 충분
**Follow-up**: 부모는 파일 경로만 전달, 에이전트는 자체 컨텍스트에서 Read.

### Round 6
**Q**: 파이프라인 실행 로그 구현 방식?
**Options**: 1) 공유 로그 파일 2) 에이전트가 직접 기록 3) 에이전트별 개별 로그 4) 토론 종료
**A**: 공유 로그 파일
**Follow-up**: autopilot이 로그 생성 + 에이전트 결과에서 결정사항 추출하여 추가. 에이전트는 로그를 모름.
