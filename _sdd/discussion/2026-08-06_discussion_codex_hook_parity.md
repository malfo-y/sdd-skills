# 토론 요약: SDD 하네스의 Codex hook parity

**날짜**: 2026-08-06
**라운드 수**: 10
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)

- **사용자 문제 제기**: `spec-create`·`spec-upgrade`가 Claude Code용 `.claude/hooks/`와 `.claude/settings.json`만 설치해, 같은 SDD 하네스 규약이 Codex에서는 실행 계층으로 강제·복원되지 않는 문제를 제기했다.
- **토론을 시작한 배경**: Codex도 lifecycle hook과 평문 context 주입을 지원하는지 확인되었고, 사용자가 네 훅 전체를 Codex에도 반영하는 후속 SDD 체인을 시작하기로 했다.
- **현재 상태**: Claude/Codex의 `spec-create`·`spec-upgrade` SKILL 본문은 각각 byte-identical이지만, 두 미러 모두 Claude 전용 경로와 `$CLAUDE_PROJECT_DIR`를 사용한다. 현재 소비 계약은 네 hook script의 verbatim 복사, `.claude/settings.json` 키 수준 멱등 병합, 설치 사실 및 무발동 조건 announce다. 저장소에는 프로젝트 `.codex/hooks.json`이 없다.
- **범위와 제외 범위**: work log 커밋 게이트, work log SessionStart context, compact/clear 후 `AGENTS.md` 재주입, subagent watchdog의 네 훅 전체를 Claude/Codex에서 동작시키는 범위다. 플러그인 배포 전환, 공용 실행 자산의 중립 디렉터리 이동, 사용자 전역 Codex 설정 수정, hook 자동 신뢰 우회는 제외한다.
- **수집한 근거**: `_sdd/spec/main.md`, 두 런타임의 `spec-create`·`spec-upgrade` SKILL과 hook reference 4미러, `.claude/settings.json`, `.claude/hooks/*.sh`, Codex CLI 0.146.0의 feature 상태, OpenAI Codex Hooks 문서와 0.124.0 릴리스, Anthropic Claude Code Hooks 문서를 확인했다.

## 핵심 논점 (Key Discussion Points)

1. **Capability gap이 아니라 설치 계약 gap**: Codex hooks는 stable이고 필요한 이벤트를 제공하지만, 현재 Codex SKILL 미러도 Claude 설정만 생성한다.
2. **호환 경로와 공용 실행 자산의 경계**: 기존 소비 repo의 `.claude/hooks` 경로는 유지하되, script 자체가 두 런타임의 프로젝트 루트와 payload를 처리하게 해야 한다.
3. **동일한 스킬의 결정적 산출물**: 어느 런타임에서 스킬을 호출하든 `.claude/settings.json`과 `.codex/hooks.json`을 함께 설치해야 dual bundle 결과가 갈라지지 않는다.
4. **Codex trust는 설치와 별도인 사용자 로컬 상태**: project hook은 등록만으로 실행되지 않으며 `/hooks`에서 exact definition을 신뢰해야 한다. 자동 우회하지 않고 강하게 안내한다.
5. **watchdog 출력 의미의 런타임 차이**: 현재 `PostToolUse`의 `decision: "block"`은 Claude에서는 원래 tool 결과를 보존하지만 Codex에서는 결과를 feedback으로 교체한다. advisory nudge 목적에는 양쪽이 지원하는 `additionalContext`가 맞다.
6. **지원 버전과 실패 정책**: Codex hooks가 stable이 된 0.124.0 이상을 요구 버전으로 안내하되 구버전 때문에 spec 작업 전체를 중단하지 않는다. 두 설정 파일의 병합 실패도 런타임별로 독립 처리한다.
7. **검증 수준**: 정적 JSON·미러·멱등성 검사만으로 닫지 않고 실제 Codex hook 호출에서 root/subdir, gate, context 복원, watchdog을 검증해야 한다.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| 1 | 네 훅 전체를 이번 변경 범위로 둔다 | 사용자가 부분 도입보다 전체 parity를 선택 (`사용자 판단`) | 1 |
| 2 | 기존 소비 경로와 재실행 동작의 무중단 호환을 최우선 제약으로 둔다 | 기존 하네스가 이미 커밋되는 실행 계약이고 소비 repo가 존재함 (`사용자 판단`, `코드 확인`) | 2 |
| 3 | `.claude/hooks` 설치 경로는 유지하고 네 script 자체를 dual-runtime으로 공용화한다 | 설정 command에 호환 어댑터를 숨기는 것보다 실행 자산이 자체 root resolution을 소유하는 편이 책임과 테스트 경계가 명확함 (`사용자 판단`, `코드 확인`) | 2 |
| 4 | Codex hook 등록을 설치 완료로 보되, `/hooks` 신뢰 전에는 비활성이라는 사실과 확인법을 반드시 보고한다 | Codex는 non-managed hook의 exact definition hash별 신뢰를 요구함 (`외부 자료`, `사용자 판단`) | 4 |
| 5 | 어느 런타임에서 `spec-create`·`spec-upgrade`를 호출하든 Claude와 Codex hook 설정을 항상 함께 설치한다 | 현재 두 runtime SKILL이 byte-identical인 dual bundle이고 산출물 분기를 피해야 함 (`코드 확인`, `사용자 판단`) | 3 |
| 6 | watchdog의 `PostToolUse` 출력은 `hookSpecificOutput.additionalContext`로 통일한다 | 두 런타임에서 원래 tool 결과를 보존하면서 advisory context를 추가하는 공통 의미임 (`외부 자료`, `사용자 판단`) | 5 |
| 7 | Codex 0.124.0+를 stable hook 요구 버전으로 안내하되, 구버전에서는 설치 자체를 중단하지 않는다 | OpenAI 0.124.0 릴리스가 hooks stable을 명시함 (`외부 자료`, `사용자 판단`) | 6 |
| 8 | `.claude/settings.json`과 `.codex/hooks.json`은 독립적으로 파싱·병합한다. 깨진 파일은 보존하고 해당 runtime 등록만 건너뛴 뒤 부분 실패를 보고한다 | 사용자 설정 손실 방지와 가용한 runtime까지 불필요하게 막지 않는 fail-open 원칙 (`사용자 판단`, `코드 확인`) | 6 |
| 9 | 완료 게이트는 구조 검증과 실제 Codex hook 호출을 모두 요구한다 | lifecycle·trust·cwd·출력 의미는 파일 검사만으로 증명되지 않음 (`사용자 판단`, `코드 확인`) | 7 |
| 10 | 이 결론을 확정하고 `feature-draft` 단계에 handoff한다 | 사용자의 최종 수렴 선택 (`사용자 판단`) | 전체 |

### 기각한 대안

- **watchdog을 제외한 3개 훅만 우선 반영**: 사용자가 네 훅 전체 parity를 선택했다.
- **실행 자산을 `.sdd/hooks` 같은 중립 경로로 이동**: 이름은 깨끗하지만 기존 소비 경로와 설치 계약을 불필요하게 깨므로 이번 범위에서 제외했다.
- **`.codex/hooks.json` command가 `CLAUDE_PROJECT_DIR`를 합성하는 설정 어댑터**: diff는 작지만 runtime 호환성이 긴 command 문자열에 숨고 script 설명·테스트 경계가 계속 Claude 전용으로 남는다.
- **hook 신뢰 승인까지 spec 작업 완료를 차단**: trust는 사용자 로컬 상태이며 저장소 파일 생성과 분리해야 한다. 대신 미승인 무발동을 강하게 알린다.
- **호출한 런타임의 설정만 설치**: 동일한 SKILL의 산출물이 런타임에 따라 달라져 dual bundle parity와 재실행 예측 가능성을 해친다.
- **watchdog의 기존 `decision: "block"` 유지**: Codex에서 원래 tool 결과가 대체되어 advisory nudge가 결과 손실을 만들 수 있다.
- **Codex 구버전에서 전체 설치 중단**: 다른 기여자의 버전을 설치 시점에 대표할 수 없고 Claude 하네스 생성까지 막을 이유가 없다.
- **한쪽 설정 파싱 실패 시 양쪽 등록 중단**: 정상 설정까지 불필요하게 무력화한다.
- **구조 검증만 필수, 실제 호출은 후속 관측**: 이번 변경의 핵심이 runtime parity이므로 실제 lifecycle 증거 없이 완료할 수 없다.

## 미결 질문 (Open Questions)

현재 in-scope 미결 질문은 없다. 실제 호출 과정에서 공식 문서와 다른 runtime 동작이 발견되면 구현을 강행하지 않고 토론 결정을 재검토한다.

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | 이 토론 요약을 입력으로 `feature-draft`를 작성하고 전파 표면·Target Files·falsifiable AC를 확정한다 | High | 후속 SDD 단계 |
| 2 | draft와 내장 plan-review gate를 통과한 뒤 `implementation`으로 공용 script·Codex 등록·문서 안내를 구현한다 | High | 후속 SDD 단계 |
| 3 | 실제 Claude/Codex 호출 증거를 확보하고 implementation-review gate를 통과한다 | High | 후속 SDD 단계 |
| 4 | 구현 증거를 바탕으로 `spec-sync`에서 global spec·decision log·changelog를 현재 사실로 동기화한다 | Medium | 후속 SDD 단계 |

### 후속 핸드오프 (Handoff)

- **목표**: `spec-create` 또는 `spec-upgrade`를 어느 지원 runtime에서 실행해도 소비 repo에 Claude/Codex hook 등록이 함께 멱등 설치되고, 네 하네스 동작이 Codex 0.124.0+에서 실제로 관찰된다.
- **변경 금지 제약**: 기존 `.claude/hooks` 소비 경로와 Claude 동작을 깨지 않는다. 사용자 설정의 다른 hook·top-level key를 덮어쓰지 않는다. 사용자 전역 `~/.codex/config.toml`을 수정하거나 hook trust를 자동 우회하지 않는다. 이번 변경을 plugin packaging 또는 중립 디렉터리 migration으로 확대하지 않는다.
- **검증**: script/reference byte parity, 두 JSON 설정의 parse·멱등 merge·사용자 항목 보존·독립 실패를 구조 검사한다. root와 하위 디렉터리에서 SessionStart context, compact/clear 후 `AGENTS.md` 재주입, worklog 없는 첫 commit deny와 우회, 5분 경과 watchdog `additionalContext` 및 원래 tool 결과 보존을 payload simulation과 실제 Codex 호출로 검증한다. Codex 0.124.0+ 요구와 `/hooks` trust 안내도 output contract에서 검증한다.
- **중단 조건**: 실제 Codex 0.124.0+ 호출이 공식 release behavior와 다르거나, `additionalContext`가 두 runtime에서 원래 결과를 보존하지 않거나, 사용자 설정 보존과 멱등 병합을 함께 만족할 수 없는 충돌이 발견되면 구현을 멈추고 결정을 재논의한다.

## 리서치 결과 요약 (Research Findings)

- **Codex hook capability**: `SessionStart`, `PreToolUse`, `PostToolUse`, subagent/compact/stop 계열 event와 project-local `.codex/hooks.json`을 지원한다. SessionStart 평문 stdout은 추가 developer context로 주입된다.
- **Codex trust**: project-local non-managed command hook은 exact definition을 사용자가 `/hooks`에서 검토·신뢰해야 하며 변경 시 다시 검토 대상이 된다.
- **Codex stable 기준**: OpenAI Codex 0.124.0 릴리스에서 hooks가 stable이 되었고 `config.toml`/managed config, MCP, apply_patch, long-running Bash 관찰 지원이 명시됐다.
- **Claude/Codex PostToolUse 차이**: Claude의 top-level block feedback은 원래 tool 결과를 보존하지만 Codex는 원래 결과를 feedback으로 대체한다. `additionalContext`는 양쪽에서 원래 결과 옆에 모델-visible context를 추가하는 공통 계약이다.
- **로컬 cwd 실측**: 현재 `harness-context.sh`는 Codex 방식으로 `$CLAUDE_PROJECT_DIR` 없이 실행할 때 repo root에서는 5,867 bytes를 출력하지만 `docs/` 하위 디렉터리에서는 0 bytes였다. 공용 root resolution이 필수다.
- **로컬 미러 상태**: Claude/Codex `spec-create` SKILL은 서로 동일하고 `spec-upgrade`도 동일하다. 네 hook script는 설치본과 네 reference mirror가 각각 동일 hash다.

## Sources

- 로컬: `_sdd/spec/main.md`
- 로컬: `.claude/skills/spec-create/SKILL.md`, `.codex/skills/spec-create/SKILL.md`
- 로컬: `.claude/skills/spec-upgrade/SKILL.md`, `.codex/skills/spec-upgrade/SKILL.md`
- 로컬: `.claude/hooks/*.sh`, `.claude/settings.json`
- OpenAI: [Codex Hooks](https://learn.chatgpt.com/docs/hooks)
- OpenAI: [Codex 0.124.0 release](https://github.com/openai/codex/releases/tag/rust-v0.124.0)
- OpenAI: [PostToolUse generated input schema](https://github.com/openai/codex/blob/main/codex-rs/hooks/schema/generated/post-tool-use.command.input.schema.json)
- Anthropic: [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks)

## 토론 흐름 (Discussion Flow)

Round 1: 후속 범위 선택 → 네 훅 전체 parity.

Round 2: 최우선 제약 선택 → 기존 경로와 재실행 동작의 무중단 호환.

Round 3: 호환 로직 배치 대안 비교 → 설정 어댑터 대신 script 공용화.

Round 4: Codex trust 약점 검토 → 등록과 신뢰 승인을 분리하고 필수 안내.

Round 5: runtime별 산출물 분기 검토 → 호출 runtime과 무관하게 두 설정 동시 설치.

Round 6: watchdog 출력 의미 검증 → `additionalContext`로 통일.

Round 7: stable 지원 버전 조사 → 0.124.0+ 안내, 구버전으로 전체 작업 중단 금지.

Round 8: 설정 파싱 실패 정책 → runtime별 독립 처리.

Round 9: 완료 검증 강도 → 구조 검사와 실제 Codex 호출 모두 필수.

Round 10: 최종 수렴 → 결론 확정 및 `feature-draft` handoff.

## 부록: 대화 로그 (Conversation Log)

### Round 1

**Q**: 이번 토론과 후속 구현에서 Codex hook 반영 범위를 어디까지 닫을까요?

**Options**: 1) 4개 훅 전체 2) 강제·복원만 우선 3) 정리/종료

**A**: 4개 훅 전체.

**Follow-up**: 전체 parity를 atomic scope로 확정했다.

### Round 2

**Q**: Codex hook을 추가할 때 가장 우선해서 지킬 제약은 무엇인가요?

**Options**: 1) 무중단 호환성 2) 중립 구조 정리 3) 정리/종료

**A**: 무중단 호환성.

**Follow-up**: 경로 migration보다 기존 소비 계약 보존을 우선했다.

### Round 3

**Q**: Codex 호환 로직을 어느 층에 둘까요?

**Options**: 1) 스크립트 공용화 2) 설정 어댑터 3) 정리/종료

**A**: 스크립트 공용화.

**Follow-up**: script가 root resolution과 runtime-neutral contract를 소유하게 했다.

### Round 4

**Q**: Codex hook 신뢰 승인을 설치 완료 조건으로 어떻게 다룰까요?

**Options**: 1) 등록 후 명시 안내 2) 승인까지 완료 조건 3) 정리/종료

**A**: 등록 후 명시 안내.

**Follow-up**: 사용자 로컬 trust를 자동 우회하거나 repository 작업 완료와 결합하지 않기로 했다.

### Round 5

**Q**: `spec-create`·`spec-upgrade`는 어느 런타임에서 호출하든 두 런타임의 hook 설정을 모두 설치할까요?

**Options**: 1) 항상 둘 다 설치 2) 호출 런타임만 설치 3) 정리/종료

**A**: 항상 둘 다 설치.

**Follow-up**: dual bundle의 동일 산출물과 미러 parity를 유지했다.

### Round 6

**Q**: watchdog의 PostToolUse 반환 의미를 어떻게 통일할까요?

**Options**: 1) additionalContext 통일 2) 기존 block 유지 3) 정리/종료

**A**: additionalContext 통일.

**Follow-up**: advisory nudge가 원래 tool 결과를 잃지 않도록 공통 계약을 선택했다.

### Round 7

**Q**: Codex 0.124.0 미만 사용자를 hook 설치 계약에서 어떻게 다룰까요?

**Options**: 1) 설치 후 요구 버전 안내 2) 구버전이면 설치 중단 3) 정리/종료

**A**: 설치 후 요구 버전 안내.

**Follow-up**: stable 버전 요구는 알리되 다른 runtime의 하네스 설치까지 막지 않기로 했다.

### Round 8

**Q**: `.claude/settings.json` 또는 `.codex/hooks.json` 중 하나가 파싱 불가일 때 어떻게 진행할까요?

**Options**: 1) 런타임별 독립 처리 2) 전체 등록 중단 3) 정리/종료

**A**: 런타임별 독립 처리.

**Follow-up**: 깨진 사용자 설정은 보존하고 정상 runtime 등록은 계속한다.

### Round 9

**Q**: 후속 구현을 완료로 닫기 위한 검증 게이트를 어디까지 요구할까요?

**Options**: 1) 구조+실호출 모두 2) 구조 검증 우선 3) 정리/종료

**A**: 구조+실호출 모두.

**Follow-up**: lifecycle parity를 실제 runtime 증거로 닫기로 했다.

### Round 10

**Q**: 이 결론으로 토론을 닫고 `feature-draft`에 넘겨도 될까요?

**Options**: 1) 결론 확정 2) 공용 경로 재논의 3) 정리/종료

**A**: 결론 확정.

**Follow-up**: in-scope 미결 없이 `feature-draft` handoff를 승인했다.
