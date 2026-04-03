# 토론 요약: 오케스트레이터 저장 위치 변경

**날짜**: 2026-04-03
**라운드 수**: 4
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)

1. **스킬 등록의 불필요성**: sdd-autopilot이 생성하는 오케스트레이터가 `.claude/skills/`에 저장되면서 스킬로 자동 등록되지만, 실제 재사용 사례가 없고 스킬 목록만 오염시킴
2. **아카이브 라이프사이클 복잡도**: 활성(`.claude/skills/`) → 완료 후 아카이브(`_sdd/pipeline/orchestrators/`) 2단계 관리가 불필요하게 복잡
3. **resume 기능 유지 방안**: 스킬 등록 없이도 로그 파일 기반으로 resume 가능
4. **파일 형식 단순화**: 스킬에서 빠져나오면 skill.json + SKILL.md 디렉토리 구조가 불필요

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | 오케스트레이터 저장 경로를 `.claude/skills/orchestrator_<topic>/SKILL.md` → `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`로 변경 | 스킬 목록 오염 방지, 관리 단순화 | 1, 2 |
| 2 | resume 기능은 유지하되 경로만 변경 | 로그 파일의 status 필드로 활성/완료 판단 가능 | 3 |
| 3 | 활성/완료 아카이브 구분 제거 — 로그로 판단 | 같은 디렉토리에 두고 `_sdd/pipeline/log_*.md`의 status로 판단. 별도 아카이브 이동 단계 불필요 | 2 |
| 4 | 파일 형식을 플랫 파일(단일 .md)로 변경 | skill.json + SKILL.md 디렉토리 구조는 스킬 등록용이었으므로 불필요 | 4 |
| 5 | `.codex/skills/` 쪽도 동일 적용 | 양쪽 플랫폼 모두 `_sdd/pipeline/orchestrators/`로 통일 | 전체 |

## 미결 질문 (Open Questions)

- (없음)

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | `SKILL.md` Step 4, 5, 7, 8 경로/로직 수정 — 생성·검증·실행·완료 경로를 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`로 변경 | High | - |
| 2 | `orchestrator-contract.md` 저장 경로 계약 수정 | High | - |
| 3 | Hard Rule #3 (Orchestrator Save) 경로 변경 | High | - |
| 4 | Hard Rule #8 (Archive Mandatory) 아카이브 이동 단계 제거, 로그 기반 상태 판단으로 변경 | High | - |
| 5 | `sdd-reasoning-reference.md` 오케스트레이터 참조 경로 수정 | Medium | - |
| 6 | `sample-orchestrator.md` 예시 경로 수정 | Medium | - |
| 7 | `_sdd/spec/main.md` 오케스트레이터 경로 참조 수정 | Medium | - |
| 8 | `.codex/skills/sdd-autopilot/` 쪽 동일 변경 적용 | Medium | - |
| 9 | Step 0 (resume) 로직: `.claude/skills/` 스캔 대신 `_sdd/pipeline/orchestrators/` + 로그 status 기반으로 수정 | High | - |

## 리서치 결과 요약 (Research Findings)

- **현재 구조**: 오케스트레이터는 `.claude/skills/orchestrator_<topic>/SKILL.md`에 생성되어 암묵적으로 스킬 등록됨. 완료 후 `_sdd/pipeline/orchestrators/<topic>_<ts>/`로 아카이브
- **resume 메커니즘**: Step 0에서 `_sdd/pipeline/log_*.md` 스캔 → 미완료 단계 발견 시 재개 제안. 오케스트레이터 파일 자체의 위치와 독립적으로 동작 가능
- **영향 범위**: SKILL.md(377줄), orchestrator-contract.md, sdd-reasoning-reference.md, sample-orchestrator.md, spec/main.md, Hard Rule #3/#8. .codex/ 쪽 병렬 구조도 동일 수정 필요

## 토론 흐름 (Discussion Flow)

Round 1: 페인포인트 확인 → 스킬 목록 오염 + resume 미사용 + 관리 복잡도 세 가지 모두 해당
Round 2: resume 처리 방향 → 완전 폐기가 아닌 경로만 변경하여 유지
Round 3: 활성/완료 구분 방법 → 별도 디렉토리 대신 로그 파일 status로 판단 / 파일 형식 → 플랫 파일로 단순화 / Codex 쪽 → 동일 적용
Round 4: 후속 작업 → 결정 사항만 정리, 구현은 별도 진행

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 오케스트레이터를 .claude/skills/에 두면서 겪은 구체적인 불편함이 어떤 건가요?
**Options**: 1) 스킬 목록 오염 2) resume 미사용 3) 관리 복잡도 4) 토론 종료
**A**: 세 가지 모두 선택 (스킬 목록 오염, resume 미사용, 관리 복잡도)

### Round 2
**Q**: 옮기면 resume 기능을 완전히 포기하는 건데, 괜찮으신가요?
**Options**: 1) 완전 폐기 2) 경로만 변경 3) 토론 종료
**A**: 경로만 변경 — resume 기능은 유지하되 _sdd 경로에서 동작하도록 수정

### Round 3-a
**Q**: 활성/완료 구분을 어떻게 하면 좋을까요?
**Options**: 1) 로그로 판단 2) active/ 서브디렉토리 3) 타임스탬프 suffix 4) 토론 종료
**A**: 로그로 판단 — 별도 구분 없이 로그 파일 status 활용

### Round 3-b
**Q**: 오케스트레이터 파일 형식도 바꿀까요?
**Options**: 1) 플랫 파일로 변경 2) SKILL.md 형식 유지 3) 토론 종료
**A**: 플랫 파일로 변경 — 단일 .md 파일, 디렉토리 구조 제거

### Round 3-c
**Q**: .codex/skills/ 쪽도 동일하게 변경할까요?
**Options**: 1) 동일 적용 2) Codex는 기존 유지 3) 토론 종료
**A**: 동일 적용 — 양쪽 플랫폼 모두 _sdd/pipeline/orchestrators/로 통일

### Round 4
**Q**: 토론 결과를 바로 구현까지 가실 건가요?
**Options**: 1) 결정만 정리 2) 토론 후 바로 구현 3) 토론 종료
**A**: 결정만 정리
