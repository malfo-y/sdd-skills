# 토론 요약: SDD 방법론에 "작업 하네스(AGENTS.md)" 레이어 도입

**날짜**: 2026-06-12
**라운드 수**: 7
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)

- **사용자 문제 제기**: global spec(예: `unified_model_evaluation`, `ft-gemma4-unsloth`의 `_sdd/spec/main.md`)이 구현자에게 실제로 쓸모가 있는지 의문에서 출발. 이어 "global spec의 역할을 키워서 이 repo에서 작업할 때의 전체 가이드라인/하네스로 만들 수 있나"로 확장.
- **토론을 시작한 배경**: SDD 방법론 저자가 global spec 레이어의 역할을 재고. 선행 진단(아래)에서 이어짐. 후속으로 스킬 구현(spec-create/spec-upgrade 수정, 방법론 문서 갱신)으로 연결될 예정.
- **현재 상태**:
  - `AGENTS.md` / `CLAUDE.md`가 4줄짜리 빈 workspace guidance로 사실상 비어 있음.
  - global spec = repo 이해(what/why/scope/guardrails) 레이어. `docs/SDD_*.md` = 방법론 메타 문서.
  - `spec-create`는 `references/`·`examples/` 폴더를 이미 보유하고, Output Contract에 `AGENTS.md`·`CLAUDE.md` bootstrap 로직이 이미 있음(현재는 빈 4줄만 생성).
  - 여러 스킬(spec-rewrite/upgrade)이 동일 template 파일을 각자 `references/`에 복사하는 미러 관례 존재. `.claude`/`.codex` 미러는 구조 동일, 내용 각자 최적화.
- **범위와 제외 범위**:
  - 다룸: 하네스(AGENTS.md) 레이어를 SDD 정식 산출물로 도입하는 상세 설계.
  - 제외: global spec의 fat 톱니(축적 편향) 문제 — **주기적 spec-review/rewrite로 관리하기로 별도 합의**. repo-specific 행동 트리거 — global spec Guardrails가 담당(하네스는 링크만).
- **수집한 근거**: `docs/SDD_CONCEPT.md`, `docs/SDD_WORKFLOW.md`, `spec-update-done/todo-agent.md`, `spec-create` 폴더 구조(Explore 조사).

### 선행 진단 (이 토론의 전제)
- global spec의 환원 불가능한 가치는 네 종류: negative constraints(guardrails), 의도(why), 함정(gotcha), tribal knowledge. 코드 grep으로 복구 가능한 것(파일 목록·시그니처·dense한 동작 서술)은 가치 낮고 drift 부채만 쌓임.
- UME main.md는 거의 이상적 thin, gemma main.md는 thin을 자칭하나 fat. gemma는 rewrite(2026-05-09, 188줄→thin)를 거쳤으나 이후 feature 누적으로 258줄로 재팽창 = **fat 톱니(sawtooth)**.
- 원인: thin은 1회성·수동(rewrite), fat은 연속·자동(매 feature의 update-todo/done). 시스템에 thin을 유지하는 메커니즘 부재. 설계·스킬 규칙은 옳으나 누적/정리 주기가 비대칭.

## 핵심 논점 (Key Discussion Points)

1. **"키운다"의 의미**: global spec 본문을 키우면 fat 톱니 재발. 내용이 아니라 **역할(능동적 작업 계약)**을 키우는 것 → 별도 하네스 레이어.
2. **레이어 분리**: 이해(what/why, 느림, 수동 참조) vs 작업 규약(how, 빠름, 능동 적용)은 변화 속도·성격이 다르므로 한 문서에 섞지 않는다.
3. **하네스 위치**: Claude Code=CLAUDE.md, Codex=AGENTS.md 자동 로드. 에이전트 중립 + 단일 소스를 위해 AGENTS.md 본체 + CLAUDE.md 포인터.
4. **라우팅 깊이**: 에이전트는 설치된 SDD 스킬 description을 이미 컨텍스트에 보유 → 스킬 카탈로그를 하네스에 박으면 중복 + 스킬셋 변경 시 전 repo stale. 워크플로우 순서만 박고 스킬명은 가리킨다.
5. **생성/backfill 메커니즘**: 신규=spec-create, 기존=spec-upgrade(legacy→current 마이그레이션의 일부로 하네스 부재를 채움).
6. **템플릿 공유**: 플러그인 배포 시 스킬은 자기 폴더 자산만 안정 접근 → 양 스킬 references/에 미러(기존 관례 부합).
7. **작업 원칙 포함**: `~/.claude/CLAUDE.md`의 behavior guideline 4개를 §0 공통 골격으로 포함(user 레벨 글로벌과 repo 레벨 하네스는 스코프가 달라 공존).
8. **누수 방지**: repo-specific 트리거가 하네스로 새지 않게 템플릿에 경계 문구를 박는다.
9. **기존 파일 병합**: 이미 AGENTS.md/CLAUDE.md가 있는 repo는 덮어쓰기 금지. 마커로 감싼 하네스 블록을 맨 위에 prepend해 멱등 병합(재실행 중복·기존 항목 중복 방지).

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| 1 | global spec은 thin understanding anchor로 유지하고, 하네스는 **별도 레이어**로 둔다(내용이 아니라 역할 확장). | `사용자 판단` | 1, 2 |
| 2 | 하네스 본체 = `AGENTS.md`, `CLAUDE.md` = `→ AGENTS.md 참조` 한 줄 포인터. | `사용자 판단` | 3 |
| 3 | §2 SDD 워크플로우는 **단계 순서만** 담고, 구체 스킬은 "설치된 SDD 스킬 사용"으로 가리킨다(카탈로그 복사 금지). | `사용자 판단` (비판적 개입 후) | 4 |
| 4 | 신규 repo = `spec-create`가 하네스 생성, 기존 repo = `spec-upgrade`가 하네스 추가. | `사용자 판단` | 5 |
| 5 | 하네스 템플릿은 `spec-create`·`spec-upgrade`의 `references/`에 미러(`.claude`/`.codex` 합쳐 4곳). | `코드 확인`(관례) + `사용자 판단` | 6 |
| 6 | §0 "작업 원칙"에 `~/.claude/CLAUDE.md` behavior guideline 4개를 **영어 원문**으로 정적 공통 포함. | `사용자 판단` | 7 |
| 7 | 누수 방지: repo-specific 주의·불변 규칙은 하네스에 적지 않고 spec Guardrails가 단일 소스. 템플릿 §4에 ⚠️ 경계 문구 명시. | `사용자 판단` | 8 |
| 8 | `spec-create`는 이미 `AGENTS.md`를 bootstrap하므로, 빈 4줄을 하네스 템플릿 기반으로 **격상**(새 통합 아님). | `코드 확인` | 5 |
| 9 | 기존 `AGENTS.md`/`CLAUDE.md`가 있으면 덮어쓰지 않고 **마커 기반 멱등 병합**: `<!-- SDD-HARNESS:START/END -->`로 감싼 하네스 블록을 맨 위에 prepend, 기존 내용은 아래 보존. 재실행 시 마커 블록만 교체(멱등). 기존 중복 항목(테스트 명령 등)은 하네스 슬롯으로 흡수. `CLAUDE.md`는 기존 내용 보존 + 포인터를 마커로 prepend. | `사용자 판단` | 9 |

### 기각한 대안
- **위치**: `CLAUDE.md`=본체(에이전트 중립성 약화) / 양쪽 동일 미러(중복·미러 동기화 부담).
- **라우팅**: 라우팅 표 전체 박기(스킬셋 변경 시 전 repo stale + 에이전트가 이미 아는 것 중복) / 순서+스킬명 절충(잔여 중복).
- **템플릿 공유**: `spec-create`에만 두고 `spec-upgrade`가 크로스 참조(플러그인 배포에서 경로 의존 깨질 위험).
- **backfill**: 신규만(활발한 기존 repo가 혜택 못 봄) / 전체 일괄 소급(안 쓸 repo에도 만드는 YAGNI). → 대신 spec-upgrade 트리거로 재정의.
- **원칙 표현**: 한국어 의역(→ 의미 보존 위해 영어 원문 유지).
- **기존 파일 병합**: 순수 prepend(재실행 중복·기존 항목 중복 미처리) / 자동 병합 없이 수동 안내만(자동화 가치 저하).
- **fat 톱니 능동 해결**(update-done에 다이어트 책임 이관 등): 이번엔 채택 않고 주기적 review/rewrite로 관리(선행 합의).

## 미결 질문 (Open Questions)

없음 (in-scope 0건).

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | 하네스 표준 템플릿(AGENTS.md) 작성 — §0~§4 골격(아래), §0 영어 원문 원칙, repo 변수 슬롯, §4 ⚠️ 경계 문구, `SDD-HARNESS` 마커 컨벤션 | High | - |
| 2 | `spec-create`: AGENTS.md bootstrap을 템플릿 기반으로 격상 + CLAUDE.md 포인터 생성. 기존 파일 있으면 마커 멱등 병합. SKILL.md Output Contract·Companion Assets 갱신 | High | - |
| 3 | `spec-upgrade`: 하네스 부재/부분 존재 시 마커 기반 멱등 병합(맨 위 prepend, 기존 보존, 재실행 시 블록만 교체) + references/ 템플릿 미러 | High | - |
| 4 | 템플릿을 `spec-create`·`spec-upgrade`의 references/에 미러 (`.claude`/`.codex` 4곳) | High | - |
| 5 | `SDD_CONCEPT.md` 레이어 표 + `SDD_WORKFLOW.md`에 하네스 레이어(Global spec 위, "repo 작업 규약/진입") 추가 | Medium | - |
| 6 | (선택) `spec-update-done`에 테스트 표준 drift 가벼운 체크 추가 | Low | - |

### 후속 핸드오프 (Handoff)
- **목표**: 하네스 레이어를 SDD 산출물로 구현. 완료 기준 — 신규 repo는 spec-create로, 기존 repo는 spec-upgrade로 §0~§4 하네스 `AGENTS.md`가 생성/추가되고 `CLAUDE.md` 포인터가 생긴다. 템플릿이 4곳에 미러된다.
- **변경 금지 제약**: global spec 본문을 키우지 않는다(thin 유지). 하네스에 스킬 카탈로그·repo-specific 트리거를 박지 않는다. 기존 references 미러 관례와 `.claude`/`.codex` 동기화를 유지한다.
- **검증**: spec-create/upgrade 산출물에 `AGENTS.md`(§0~§4)·`CLAUDE.md` 포인터 생성 확인(수동 시나리오). 기존 파일 있는 repo에서 **멱등성 확인**(두 번 돌려도 하네스 블록 중복 안 쌓임, 기존 내용 보존). 템플릿 4곳 미러 일치(diff). 방법론 문서 정합(grep).
- **중단 조건**: 하네스가 global spec과 내용 중복을 일으키거나 단일 소스 원칙과 충돌하면 중단·보고.

## 리서치 결과 요약 (Research Findings)

- `spec-create`는 `references/`(template-compact·full)·`examples/` 폴더를 이미 보유. SKILL.md 본문 직접 실행(wrapper 아님).
- spec-create Output Contract에 `AGENTS.md`·`CLAUDE.md`·`_sdd/env.md` bootstrap 항목이 이미 존재.
- spec-rewrite/upgrade 등이 동일 template 파일을 각자 references/에 복사 보유 = 미러 관례.
- `.claude`/`.codex` 미러: 구조 동일, references 내용은 각자 최적화. 참조 표기는 "Companion Assets" 섹션 + 상대경로 백틱.

## 합의된 하네스 템플릿 골격 (산출물)

```markdown
# AGENTS.md — <repo-name> 작업 하네스

> 작업 규약(how). repo의 이해(what/why)·scope·guardrail은 여기 말고 `_sdd/spec/`.

## 0. 작업 원칙 (모든 작업에 우선)
- **Think Before Coding**: Don't assume. Don't hide confusion. Surface tradeoffs.
- **Simplicity First**: Minimum code that solves the problem. Nothing speculative.
- **Surgical Changes**: Touch only what you must. Clean up only your own mess.
- **Goal-Driven Execution**: Define success criteria. Loop until verified.

## 1. 작업 시작 시 읽는 순서
1. 이 파일 → 2. `_sdd/spec/main.md` → 3. `_sdd/env.md` → 4. 진행 중이면 관련 temporary spec

## 2. 작업 규약 / 검증 표준
- 테스트: `<test command>` · 린트: `<lint command>` (repo 변수)
- Execute → Verify 필수 (문서/스킬 변경은 diff·grep·review)
- 커밋/PR: `<규칙>` · 코드가 spec과 어긋나면 spec부터 갱신

## 3. SDD 워크플로우
discussion → feature-draft → implementation-plan → implementation → review-fix → verify → spec sync
(구체 스킬은 설치된 SDD 스킬 사용 — 카탈로그 복사 금지)

## 4. 판단 기준 (가리키기, 복사 금지)
- scope → spec §<…> · 결정의 '왜' → spec §<…>
- ⚠️ repo-specific 주의·불변 규칙은 여기 말고 spec Guardrails (단일 소스)
```
(§0은 영어 원문 유지. §1·§2·§4의 `<…>`는 spec-create/upgrade가 repo 맥락으로 채우는 변수 슬롯.)

## 토론 흐름 (Discussion Flow)

- 선행: global spec 무용론 의문 → thin core 가치 진단 → fat 톱니(축적 편향) 진단 → 주기적 review/rewrite로 관리 합의 → 역할 확장(하네스) 논의로 전환
- Round 1: 하네스 위치 → AGENTS.md 본체, CLAUDE.md 포인터
- Round 2: 라우팅 깊이 → 워크플로우 순서만, 스킬명 가리키기 (비판적 개입: 카탈로그 복사 = 중복+drift)
- Round 3: backfill → spec-upgrade가 담당 (사용자 재정의)
- Round 4: 템플릿 공유 → 양 스킬 references/ 미러
- Round 5: 마무리 방향 → 골격 초안 요청
- Round 6: 골격 검토 → behavior guideline §0 추가
- Round 7: 원칙 표현 → 영어 원문 유지, 정리

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 하네스 본체를 AGENTS.md/CLAUDE.md 중 어디 두고 나머지는?
**A**: AGENTS.md=본체, CLAUDE.md=포인터 (권장안 채택)

### Round 2
**Q**: SDD 스킬 라우팅을 하네스에 얼마나 담을까? (전제: 에이전트가 스킬 description 이미 보유)
**A**: 워크플로우 순서만, 스킬명은 가리키기 (권장안 채택)

### Round 3
**Q**: 기존 repo backfill 방식? (온디맨드/신규만/일괄)
**A**: (재정의) spec-upgrade에 하네스 추가 로직을 넣어 기존 repo 처리, 신규는 spec-create

### Round 4
**Q**: 템플릿을 spec-create·spec-upgrade가 어떻게 공유?
**A**: 양 스킬 references/에 미러 (권장안 채택)

### Round 5
**Q**: 마무리 vs 더 논의?
**A**: 하네스 템플릿 실제 골격을 같이 초안

### Round 6
**Q**: 골격 검토, 손볼 곳?
**A**: ~/.claude/CLAUDE.md의 behavior guideline 포함 요청 → §0 작업 원칙으로 반영

### Round 7
**Q**: §0 원칙 표현(한국어 의역 vs 영어 원문)?
**A**: 영어 원문 유지 → 정리
