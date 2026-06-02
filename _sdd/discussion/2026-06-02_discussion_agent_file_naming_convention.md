# 토론 요약: `.claude/agents` 파일·식별자에 `-agent` 접미사 도입

**날짜**: 2026-06-02
**라운드 수**: 6
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)
- **사용자 문제 제기**: `.claude/agents/` 아래 파일들의 이름을 전부 `<slug>_agent.md`로 바꿔서 "이게 agent라는 걸 확실히" 하고 싶다. 토론 중 동기가 확장되어, 파일명뿐 아니라 **`subagent_type` 호출 이름 자체도 `<slug>-agent`로** 바꾸고 싶다는 의도가 드러남.
- **토론을 시작한 배경**: 폴더 `agents/`만으로는 agent임이 충분히 드러나지 않는다고 느낌. 특히 `feature-draft`가 skill 이름이자 agent 이름으로 동시에 쓰여 호출 단계에서 모호함.
- **현재 상태**:
  - claude agents: `.claude/agents/<slug>.md` 10개. 호출은 frontmatter `name:` 필드 기반(`Agent(subagent_type=feature-draft)`). **파일명은 resolution에 관여하지 않음.** 컨벤션 = kebab.
  - codex agents: `.codex/agents/<slug>.toml` 10개. `name = "feature_draft"`(snake), `spawn_agent(agent_type="feature_draft")`. 파일명은 kebab이나 내부 name은 snake.
  - Mirror Notice가 claude agent ↔ codex .toml ↔ 각 SKILL.md를 "같은 계약"으로 묶음 — 단 묶이는 것은 **본문(developer_instructions) 계약**이지 식별자 문자열이 아님.
- **범위와 제외 범위**: 이번 토론은 "리네이밍 여부 + 네이밍 규칙 + 안전한 실행 방침"까지. `_sdd/pipeline/*` 과거 기록 갱신은 제외(보존)로 결정.
- **수집한 근거**: `.claude/agents/*.md` frontmatter, `subagent_type=` 호출처 census, `.codex/agents/*.toml`, 각 SKILL.md Mirror Notice, `sdd-autopilot/references/orchestrator-contract.md`(허용 subagent_type 목록 + model 매핑 테이블), `_sdd/pipeline/*` 경로 참조 ~30곳.

## 핵심 논점 (Key Discussion Points)
1. **기능 vs 외형 분리**: 파일명 변경은 cosmetic(호출 무관, doc 경로 ~30곳만), invocation 이름 변경은 functional(호출처·contract·codex 동기화 필요).
2. **stutter 우려**: `subagent_type=feature-draft-agent`는 `subagent_type=` + 폴더 `agents/` + `-agent`로 "agent"가 삼중 중복.
3. **실익 발견**: `feature-draft`가 skill·agent·step개념 3역을 겸해 모호 → invocation 이름 분리가 skill↔agent 모호함을 실제로 해소. stutter라는 비용으로 이 실익을 산다.
4. **codex 대칭의 정체**: 두 진영은 이미 식별자 컨벤션이 다름(claude kebab, codex snake). "대칭"은 본문 계약이지 식별자가 아니므로, 각 진영 자기 컨벤션 안에서 접미사를 붙이면 됨.
5. **분기 규칙(최대 리스크)**: 부분 리네임이 오히려 모호함을 키울 수 있음 → "호출 식별자·파일 경로만 변경, skill·step개념 산문은 `feature-draft` 유지"라는 칼선이 곧 목적 자체.
6. **실행 안전성**: 분기 규칙 때문에 blind find-replace 금지(컨텍스트 앵커링 필수), pilot-then-batch + 검증 게이트.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | **범위 C** — 파일명 + invocation 이름 둘 다 변경 | "agent임을 확실히"가 flat-view뿐 아니라 호출 단계에서도 필요 | 1, 3 |
| 2 | **codex도 함께 리네임** (각 진영 컨벤션 안에서) | Mirror Notice 본문 계약 대칭 유지 | 4 |
| 3 | **네이밍 규칙**: claude 전부 kebab — 파일 `feature-draft-agent.md`, `name: feature-draft-agent`, `subagent_type=feature-draft-agent`. codex — 파일 `feature-draft-agent.toml`, 내부 `name = feature_draft_agent`(snake), `agent_type="feature_draft_agent"` | claude=kebab, codex=snake 기존 컨벤션 보존. `<slug>_agent.md`(혼합 separator) 대신 전부 kebab으로 일관 | 4 |
| 4 | **분기 규칙**: 호출 식별자(`subagent_type=`/`agent_type=`)·`name:` 필드·파일 경로·autopilot 허용목록·model 테이블만 변경. **skill 이름(`.claude/skills/feature-draft/`)·step개념 산문·산출물 파일명(`_sdd/drafts/..._feature_draft_<slug>.md`)은 `feature-draft` 유지** | 이 칼선이 곧 skill↔agent 구분이라는 목적 | 5 |
| 5 | **편집 경계**: live 계약(.claude/.codex의 agents·skills, autopilot references)만 수정. `_sdd/pipeline/*` 과거 리포트/오케스트레이터는 그 시점 스냅샷으로 보존 | churn 최소화(YAGNI) | 5 |
| 6 | **실행 = pilot-then-batch**: `feature-draft` 하나를 file+name+모든 호출처+codex까지 end-to-end로 먼저 → 검증 게이트 통과 → 나머지 9개를 검증된 패턴으로 일괄. 모든 치환은 컨텍스트 앵커링. `git mv`로 히스토리 보존, 브랜치 작업 + 검증 후 커밋 | 이른 롤백 지점 확보 + 누락 호출처(런타임 silent fail) 차단 | 6 |

## 미결 질문 (Open Questions)
없음 (in-scope 0건). 모든 핵심 결정이 수렴됨.

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | 치환 대상 census 작성 (역할별: 호출처/`name:`/파일경로/허용목록/model테이블, claude·codex 분리) | High | (후속 실행) |
| 2 | `feature-draft` pilot: `git mv` → `name:` → 모든 호출처 → Mirror Notice 경로 → codex 동일 적용 | High | (후속 실행) |
| 3 | 검증 게이트: live 영역에 `subagent_type=feature-draft\b`(=-agent 없는 것) 0건 + 모든 `subagent_type=X-agent`에 대응 `name:` 존재 확인 | High | (후속 실행) |
| 4 | 검증 통과 후 나머지 9개 agent 동일 패턴으로 일괄 적용 + 재검증 | High | (후속 실행) |
| 5 | 브랜치 작업, 검증 게이트 통과 시에만 커밋 (롤백 = `git restore`/브랜치 폐기) | Medium | (후속 실행) |

## 리서치 결과 요약 (Research Findings)
- **claude agent resolution은 `name:` frontmatter 기반** — 파일명 변경만으로는 기능 영향 없음. invocation 이름(`name:`) 변경이 functional 부분.
- **호출처 census**: `subagent_type=<name>` 약 10곳(claude live) + autopilot orchestrator-contract의 허용목록·model 테이블. codex는 `spawn_agent(agent_type="...")` 대응.
- **컨벤션 비대칭 사실**: codex `name = "feature_draft"`(snake) vs 파일 `feature-draft.toml`(kebab) — codex는 이미 파일명↔내부명 separator 불일치 존재.
- **substring 충돌 위험**: `feature-draft`가 skill 폴더·draft 산출물 파일명에 substring으로 박혀 있어 전역 치환 시 오염 → 컨텍스트 앵커링 치환 필수.

## 토론 흐름 (Discussion Flow)
- Round 1: 동기 확인 → 폴더만으론 부족 + **subagent_type 이름도 `<slug>-agent`로** 바꾸려는 의도 확장 (깊이 신호: 새 제약 등장)
- Round 2: 대안 A(그대로)/B(파일명만)/C(파일명+invocation) 제시, 권장안 B + stutter 비판 → 사용자 **C 선택**
- Round 3: codex 대칭성 → **codex도 함께 리네임** 결정 + 대칭=본문계약이라는 사실 확인
- Round 4: separator 충돌(`-`/`_` 혼합) → **전부 kebab** (claude), codex 내부는 snake 유지
- Round 5: 분기 규칙(호출 식별자만 변경, skill/개념 유지) → **제안 규칙 그대로** 채택
- Round 6: 편집 경계(`_sdd/pipeline/*` 보존) → **live 계약만**; 실행 단위 → **pilot-then-batch**; 수렴 → 정리

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 리네이밍을 떠올린 실제 트리거가 뭔가요?
**Options**: 1) 에디터 탭/검색에서 헷갈림 2) 폴더만으론 부족 3) codex/skills와 통일 4) 토론 종료
**A**: "폴더만으론 부족하다고 느낌 + subagent_type 이름도 전부 `<slug>-agent`로 바꿔서 agent라는 걸 확실히 하고 싶음."
**Follow-up**: 단순 파일명 변경 → functional(호출 깨짐) 변경으로 범위 확장. blast radius 재조사 트리거.

### Round 2
**Q**: 범위를 어디까지? (A 그대로 / B 파일명만(권장) / C 파일명+invocation / C' suffix 재설계)
**A**: **C** — 파일명 + invocation 이름.
**Follow-up**: stutter 비용 수용, skill↔agent 구분 실익 확인.

### Round 3
**Q**: `.codex/agents/`도 함께 리네임할까요?
**A**: **codex도 같이 리네임**.
**Follow-up**: codex snake / claude kebab 비대칭 발견 → "대칭=본문계약" 재정의.

### Round 4
**Q**: separator를 어떻게 통일? (전부 kebab / 제안대로 `_agent` 혼합 / 먼저 확인)
**A**: **전부 kebab 유지** (claude `feature-draft-agent`, codex 파일 kebab·내부 snake `feature_draft_agent`).

### Round 5
**Q**: 분기 규칙(호출 식별자만 변경, skill·개념 유지)에 동의?
**A**: **제안 규칙 그대로**.

### Round 6
**Q(a)**: `_sdd/pipeline/` 과거 기록도 갱신? → **live 계약만 갱신**.
**Q(b)**: 실행 단위/커밋 구조? → **1개 파일럿 → 검증 → 나머지 일괄**.
**Q(c)**: 정리할까요? → **정리해줘**.
