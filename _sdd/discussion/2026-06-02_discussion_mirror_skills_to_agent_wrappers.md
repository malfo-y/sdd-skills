# 토론 요약: mirror 스킬을 agent thin wrapper로 전환

**날짜**: 2026-06-02
**라운드 수**: 5
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)
- **사용자 문제 제기**: agent의 mirror로 존재하는 스킬들을 전부 "해당 agent를 필요한 context와 함께 호출하는 thin wrapper"로 바꾸고 싶다.
- **토론을 시작한 배경**: 직전에 agent 식별자 `-agent` rename 작업을 끝낸 직후. 그 과정에서 스킬↔agent 본문이 Mirror Notice로 강제 동기화되는 중복 구조가 드러났고, 이를 정리하려는 후속 작업. 목표는 (1) 코드 중복 제거(DRY), (2) 스킬 호출로 인한 메인 컨텍스트 윈도우 절약.
- **현재 상태 (코드 확인)**:
  - mirror 스킬 10종(feature-draft, implementation, implementation-plan, implementation-review, investigate, plan-review, ralph-loop-init, spec-review, spec-update-done, spec-update-todo)이 `.claude/skills/<slug>/SKILL.md` + `.codex/skills/<slug>/SKILL.md`에 존재.
  - 각 스킬 본문이 대응 agent(`.claude/agents/<slug>-agent.md`, `.codex/agents/<slug>-agent.toml`)와 **거의 동일**(예: feature-draft 270 vs 271줄). claude ~2,700줄 + codex ~2,700줄 ≈ 5,400줄 중복.
  - Mirror Notice가 "사용자가 직접 호출할 때 중간 과정의 가시성을 확보하기 위해 복붙되었다"고 명시 — 중복의 *원래 이유*가 직접 호출 시 가시성.
  - **agent들은 이미 non-interactive 설계**(예: feature-draft-agent Hard Rule 4 "사용자에게 inline 질문을 던지지 않으며"). 모두 best-effort 후 끝에 surface.
  - **agent tools에 Skill 도구 없음** → agent는 다른 스킬을 호출하지 않음. `write-phased` 등 참조는 dispatch가 아닌 개념적 계약.
- **범위**: mirror 스킬 10종 × claude/codex 양쪽. 비대상 = agent가 없는 standalone 스킬(discussion, spec-create, spec-rewrite, spec-summary, spec-snapshot, spec-upgrade, guide-create, pr-review, write-phased, second-opinion, sdd-autopilot, git).
- **수집한 근거**: 스킬/agent 본문 줄 수 비교, SKILL.md frontmatter 구조, agent tools 목록, 스킬→스킬 dispatch 참조 grep, codex 스킬 frontmatter.

## 핵심 논점 (Key Discussion Points)
1. **트레이드오프의 실체**: 원래 mirror가 존재한 이유는 "직접 호출 시 가시성". wrapping하면 직접 호출이 격리된 sub-agent 실행이 됨. 그러나 agent가 이미 non-interactive라 **잃는 인터랙션은 없고**, 잃는 건 "단계별 라이브 가시성"뿐(결과물·리포트는 그대로 수신). → 트레이드오프가 예상보다 약함.
2. **wrapper 템플릿 = 무엇을 하느냐**: pure pass-through(A) vs context-prep(B). 선언적 alias(C)는 Claude Code 스킬에 agent-alias 필드가 없어 불가 → 실질 A로 귀결.
3. **A의 정밀화 (A1 vs A2)**: literal pass-through(A1)는 sub-agent가 대화 맥락을 못 봐 "방금 논의한 plan" 같은 지시를 잃음. context-prep(B)는 메인에서 파일을 직접 read·resolve해 **컨텍스트 절약 목표를 상쇄 + agent의 input 로직 중복**. 정답은 A2 = pass-through + 대화 맥락 forwarding(새 read 없이 이미 아는 경로·산출물·결정만 전달). A2는 **autopilot orchestrator가 이미 agent들을 부르는 검증된 패턴**.
4. **유지보수 모델**: wrapping 후 본문 중복 소멸 → Mirror Notice 동기화 의무 소멸. agent가 단일 canonical.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | **mirror 스킬 10종 × claude/codex 전부 wrap** | agent가 이미 non-interactive라 인터랙션 손실 0, 잃는 건 라이브 가시성뿐 | 1 |
| 2 | **wrapper = A2 (pass-through + 대화 맥락 forwarding)** | 사용자 요청 + 대화에서 이미 established된 참조 경로·이전 산출물·결정을 verbatim 전달. wrapper는 **새 파일 read·input 탐색 안 함**(agent의 Step 1이 담당). orchestrator와 동일한 검증된 호출 패턴. B는 컨텍스트 절약 상쇄 + input 로직 중복이라 기각, A1은 대화 맥락 소실이라 기각 | 2, 3 |
| 3 | **Mirror Notice 제거 → "이 스킬은 X-agent의 wrapper" 1줄 포인터** | agent 단일 canonical, sync 의무 소멸 | 4 |
| 4 | codex wrapper = `spawn_agent(agent_type=X_agent)` + `wait_agent` + 결과 relay | codex 실행 lifecycle 규칙 준수 | 2 |
| 5 | autopilot·sibling 스킬 참조는 무영향 (수정 불필요) | orchestrator는 agent를 직접 호출, sibling 참조는 wrapper가 여전히 트리거됨 | — |
| 6 | wrapper frontmatter(name/description/version) 유지 | 스킬 auto-trigger 매칭에 필요 | 2 |

## 미결 질문 (Open Questions)
없음 (in-scope 0건). 모든 핵심 설계 결정 수렴.

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | wrapper 템플릿 초안 확정 (thin SKILL.md 본문: A2 전달 규칙 + dispatch + relay) — claude/codex 각각 | High | feature-draft 후속 |
| 2 | **pilot 검증**: codex 스킬 직접 호출 시 본문 `spawn_agent`가 실제 dispatch되는지 1개로 확인(rename 때 V4와 동일 접근). claude도 wrapper 1개 dispatch 확인 | High | 구현 시 |
| 3 | 10종 × 2 스킬 본문을 wrapper로 교체, Mirror Notice → 포인터 | High | 구현 |
| 4 | 검증: 직접 호출 → agent dispatch → 결과 relay 동작, 컨텍스트 절약 확인 | High | 구현 |

## 리서치 결과 요약 (Research Findings)
- **DRY 규모**: 스킬 본문이 agent와 near-identical(줄 수 차 1) → claude ~2,700 + codex ~2,700 ≈ 5,400줄 중복 제거.
- **컨텍스트 이득**: 직접 호출 시 200~600줄 본문이 메인에 로드되던 것이 thin wrapper ~10줄로. 무거운 작업은 agent 자체 context.
- **agent non-interactive**: inline AskUserQuestion 없음 → wrapping 시 인터랙션 손실 없음.
- **agent에 Skill 도구 없음**: 다른 스킬을 호출하지 않음 → wrapping 시 깨질 내부 indirection 없음(스킬→agent 1단계뿐).
- **A2 = orchestrator 패턴**: autopilot이 이미 focused 프롬프트 + 산출물 경로를 넘기고 agent가 self-discover하게 함 → A2가 검증된 패턴임을 뒷받침.

## 토론 흐름 (Discussion Flow)
- Round 0(진입): 사용자가 wrapping 방향 고정 → 가시성 트레이드오프·nesting·indirection 사전 점검 후 discussion 진입.
- Round 1: non-interactive 발견 공유 → "잃는 건 라이브 가시성뿐" → **10개 전부 wrap** 결정.
- Round 2: wrapper 템플릿 A/B/C 제시 → **A(pass-through)** 선택.
- Round 3: Mirror Notice 처리 → **제거 + 1줄 포인터**.
- Round 4(수렴 시도): 사용자가 "pass-through 괜찮나? context-prep이 낫나?" 재검토(깊이 신호) → A1/A2/B 재분해, **A2** 채택(B는 목표 상쇄, A1은 맥락 소실).
- Round 5: 수렴 확인 → 정리.

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: agent가 non-interactive면 10개 전부 wrap할까, 일부는 스킬로 남길까?
**A**: 10개 전부 wrap (권장).

### Round 2
**Q**: wrapper 템플릿 — A(pass-through) / B(context-prep) / C(선언적 alias)?
**A**: A: pure pass-through.
**Follow-up**: A의 약점(verbatim 전달 의존)을 비판적으로 명시.

### Round 3
**Q**: Mirror Notice 처리 — 제거+포인터 / 완전 제거 / agent 역-포인터?
**A**: 제거 + 1줄 포인터로 교체.

### Round 4
**User 재검토**: "pass-through 괜찮을까? context-prep이 더 나으려나?" (깊이 신호)
**AI 분석**: A1(literal)은 대화 맥락 소실로 위험, B는 컨텍스트 절약 상쇄+input 중복으로 과함. A2(pass-through + 맥락 forwarding)가 정답이며 orchestrator의 검증된 패턴.
**Q**: A2 / B / 더 논의?
**A**: A2: pass-through + 맥락 forwarding.

### Round 5
**Q**: 수렴, 정리할까?
**A**: 정리해줘.
