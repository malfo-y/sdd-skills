# SDD Skills

> Markdown 기반 skill bundle로 AI 에이전트의 Spec-Driven Development 워크플로우를 Claude Code와 Codex에서 공통 계약으로 실행한다.

**Spec Version**: 4.25.0
**Last Updated**: 2026-08-18
**Status**: Approved
**Canonical Role**: current thin global spec

이 문서는 repo-wide `개념 + 경계 + 결정`만 고정하는 thin global spec이다. 상세 component reference는 [components.md](./components.md), 사용 시나리오와 기대 결과는 [usage-guide.md](./usage-guide.md), 구조 변경 이력은 [decision_log.md](./decision_log.md), 릴리스/문서 변경 이력은 [logs/changelog.md](./logs/changelog.md), 환경과 실행 제약은 [../env.md](../env.md)에서 확인한다.

## 1. 배경 및 high-level concept

### 문제 정의

AI 코딩 에이전트는 강한 생성 능력을 갖고 있지만, 프로젝트의 문제 정의, 설계 경계, 검증 기준이 고정돼 있지 않으면 같은 저장소에서도 매번 다른 추론을 하게 된다. 기존 개발 방법론은 사람 중심 운영을 전제로 하므로, 에이전트가 스펙을 읽고 구현하고 검증하고 다시 스펙을 갱신하는 루프를 직접 실행하기에는 계약이 느슨하다.

### high-level concept

SDD Skills는 이 문제를 `SKILL.md = 실행 가능한 프롬프트`라는 관점으로 푼다.

- global spec은 얇은 기준 문서로 남기고, 변경 실행에는 temporary spec과 implementation artifact를 분리한다
- 사용자 진입점은 skill layer에 유지하고, 재사용 가능한 실행 계약은 스킬 `references/` 문서로 분리해 프롬프트로 주입한다
- 스킬 간 persistent handoff는 숨겨진 메모리가 아니라 `_sdd/` 파일 아티팩트에 남긴다
- 검증은 부가 옵션이 아니라 workflow contract의 일부로 취급한다

### 왜 이 접근을 택하는가

| 접근 | 장점 | 한계 | 판정 |
|------|------|------|------|
| SDD skill bundle | 스펙을 Single Source of Truth로 유지하고, 사람과 AI가 같은 파일 기반 계약을 공유한다 | 스킬/문서 유지 비용이 있다 | 채택 |
| 프롬프트 라이브러리 | 시작이 빠르다 | 스킬 간 연결과 산출물 계약이 약하다 | 비채택 |
| 코드 중심 자동화만 사용 | 익숙한 CI/CD 자산을 활용할 수 있다 | 자연어 기반 계획, spec sync, decision capture가 약하다 | 비채택 |

### 이 repo를 읽는 관점

이 저장소는 Claude Code와 Codex에서 공통으로 사용할 수 있는 SDD workflow bundle이다. 사용자는 `/spec-create`, `/feature-draft`, `/implementation`, `/sdd-autopilot` 같은 명시적 skill entrypoint로 워크플로우를 시작하고, 저장소는 그 과정을 `_sdd/` 산출물과 문서 계약으로 추적 가능하게 만든다.

## 2. Scope / Non-goals / Guardrails

### In Scope

- `.claude/skills/`, `plugins/sdd-skills-codex/skills/`의 사용자 진입점과 workflow contract
- 스킬 `references/`의 재사용 계약 문서 (예: simplicity 계약 `implementation-review/references/simplicity-contract.md`)
- global spec, temporary spec, `_sdd/` artifact layout, decision log, changelog
- README와 `docs/`의 개념/정의/워크플로우/가이드 문서
- Claude plugin 구조(`.claude-plugin/`, 마켓 `sdd-skills`)와 Codex plugin 구조(`.agents/plugins/marketplace.json` + `plugins/sdd-skills-codex/`, 마켓·플러그인 `sdd-skills-codex` — Codex가 `.claude-plugin`을 legacy marketplace로도 읽으므로 이름을 분리) 및 bundle/config 배포 규약

### Non-goals

- Claude Code나 Codex의 호스트 런타임 자체를 대체하지 않는다
- 애플리케이션 런타임이나 서비스 배포 파이프라인을 제공하지 않는다
- exhaustive inventory를 global spec 본문에 유지하지 않는다
- 모든 플랫폼 기능을 완전 동등하게 추상화하지 않는다

### Guardrails

- global spec은 thin decision document로 유지하고, execution detail은 `_sdd/drafts/`, `_sdd/implementation/`, `_sdd/pipeline/` 같은 temporary surface로 분리한다
- 표적 test/check는 30초가 지나면 중단하고, timeout된 같은 명령은 test target·fixture·관련 구현이 바뀌기 전까지 재실행하지 않으며, 느리다고 알려진 test는 repo 또는 사용자가 명시한 checkpoint에서만 실행한다. ① 리뷰 correctness 수행자는 checkpoint evidence 없는 slow 의존 AC를 임의 실행하지 않고 `UNTESTED`(사유: slow — checkpoint 대기)로 보고한다 ② `implementation` 마감 회귀는 이번 변경 관련 표적 test/check + fast 회귀(무거운 test 제외)만 실행하고, 무거운 test·전체 suite는 실행하지 않는다 ③ 실행 중 무겁게 드러난 테스트는 보고와 함께 **분리·리팩토링을 적극 권고**하고, 본질적으로 느리다는 근거가 있을 때만 checkpoint 한정 실행으로 등록한다(slow 분류를 escape hatch로 쓰지 않는다). 하네스 §2의 10초는 개별 테스트 설계·분리 기준, 30초는 targeted 명령 wall-clock 예산 — 층이 다른 공존 계약이다. 정형 fast/slow lane 스키마는 비도입한다(개별 test 분리 기준과 마감 fast-only 계약으로 실행 경계가 닫힌다)
- 사용자 entrypoint는 skill layer에 두고, 재사용 execution 계약은 스킬 `references/` 문서가 소유한다(dispatch는 런타임 내장 agent type에 계약을 프롬프트로 주입 — custom agent 없음). dispatch된 agent는 sub-agent를 다시 spawn하지 않는다(nesting 1단계 제한)
  - leaf dispatch가 필요한 execution은 `orchestrator(skill) + leaf(계약 주입 범용 agent)` 형태로 둔다(orchestrator skill만 dispatch하고, leaf는 단일 단위/단일 산출물만 처리)
  - **실행 경제 — 해소 수단은 턴 접기(배칭)와 1단계 leaf fan-out이다**: 체감 지연의 지배 성분은 dispatch 왕복이 아니라 턴 수만큼 반복되는 추론과 최종 리포트 생성이다. 중첩 fan-out은 비대상이고, 병렬 분해는 메인 루프의 1단계 leaf dispatch로만 한다 — 기본형은 read-only leaf, 파일을 쓰는 leaf의 병렬은 **쓰기 집합이 서로소로 증명된 작성자 분할**에 한해 허용한다(안전성의 근거는 "안 쓴다"가 아니라 "서로소다"). review·구현 계열 SKILL은 **서로 의존하지 않는 read-only 호출의 한 메시지 배칭을 지시형으로 요구한다** — 앞 결과를 봐야 대상이 정해지는 호출만 다음 턴, 쓰기·상태 변경 호출은 배칭 비대상, **배칭은 읽을 대상을 늘리지 않는다**. 지시형(배칭)과 허가형(독립 task 병렬 진행)은 한 문장에 섞지 않고, task 안의 RED→GREEN 순서는 병렬 여부와 무관하게 유지된다. 규칙 문면은 런타임별 tool 이름에 의존하지 않는다
- persistent handoff는 `_sdd/spec/`, `_sdd/drafts/`, `_sdd/implementation/`, `_sdd/pipeline/`, `_sdd/discussion/`의 canonical 경로를 통해 이뤄진다
- 새 temporary artifact는 가능한 한 lowercase canonical 경로를 사용하고, skill contract가 dated slug 패턴을 정의한 output surface는 그 형식을 따라야 한다. reader는 legacy uppercase/fixed-name artifact를 fallback으로 읽을 수 있어야 한다
- 소비 repo에서 커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`·`drafts/`·`work_log/`이고(`drafts/`·`work_log/`는 구현 로그 자산), 나머지 process artifact(`_sdd/{discussion,implementation,pipeline,pr}/`)는 `.gitignore`(`SDD-WORKSPACE` 마커 블록)로 로컬 전용이다. `_sdd/env.md`는 커밋되므로 비밀값(API 키·토큰·비밀번호)을 적지 않는다. 단 이 sdd_skills repo는 스킬 개발 메타 repo라 process artifact를 history 가치로 계속 커밋하는 예외다(소비 repo 정책과 별개)
- 하네스 설치는 문서 산출물(`AGENTS.md`·`CLAUDE.md`·`.gitignore`)과 **공용** 훅 bundle을 동일 조건에 묶어 함께 수행한다 — 훅은 별도 opt-in이 아니다. 공용 실행 경로는 호환성을 위해 `.claude/hooks/`에 유지하며, work log 커밋 게이트·세션 컨텍스트 주입·컨텍스트 소실 후 하네스 재주입·subagent 장기실행 watchdog nudge의 스크립트 4개를 self-host 사본과 `spec-create`/`spec-upgrade`의 Claude/Codex reference surface에 byte-identical하게 유지한다
  - 훅 event/matcher·설정 병합·trust·검증·보고 계약의 authoring canonical은 `.claude/skills/spec-create/references/hook-installation.md`이고, 나머지 세 package의 동명 reference는 exact 배포 mirror다(각 skill은 자기 local 사본만 읽어 독립 배포 유지). 두 runtime 설정(`.claude/settings.json`·`.codex/hooks.json`)은 독립 parse/merge unit으로 함께 등록하되 non-SDD handler를 보존하고, 한쪽이 깨져도 반대 runtime 설치를 계속하며 재실행은 멱등이다. 강제 자산은 파서 부재 시 fail-open + 세션 시작 경고, advisory watchdog은 조용한 fail-open 허용. Codex project hook은 사용자가 `/hooks`에서 검토·신뢰하기 전에 acceptance 완료로 보지 않으며 trust 자동 승인·user-global 설정 수정·bypass는 금지다(상세 계약은 canonical reference가 소유)
- dispatch되는 leaf에는 입력이 대화에서 태어난 맥락을 digest로 forwarding해야 한다(leaf는 파일은 read하지만 대화는 읽지 못한다). 지원하지 않는 동작을 조용히 흉내내지 않는다
- Codex multi-agent dispatch는 Desktop/CLI 같은 surface 이름이 아니라 **활성 tool schema만으로 lifecycle contract를 선택**한다. mailbox schema(Desktop과 현재 CLI 0.146.0)는 invocation별 parent-tree 고유 `task_name`·`fork_turns: "none"`·target 없는 mailbox wait를 사용하고 완료 agent를 닫지 않는다. target wait와 `close_agent`가 함께 노출된 legacy schema에서만 target/close contract를 유지한다. schema가 불완전하거나 모호하면 mandatory dispatch는 fail closed, optional helper는 inline fallback하며, 없는 lifecycle tool을 검색하거나 두 contract를 섞지 않는다. review override 필드도 active spawn schema가 지원할 때만 추가하고, 요청된 필드가 미지원이면 dispatch를 막는다
- review나 validation이 포함된 workflow는 review-only로 닫지 않고 fix 또는 명시적 잔여 이슈 보고로 마무리한다
  - **품질 게이트는 그 산출물을 만든 producer 스킬이 소유한다**: `feature-draft`→`plan-review`, `implementation`→`implementation-review`를 자기 마감의 강제 게이트로 호출하고 finding fix도 producer가 수행한다(임계·호출 상한·정책의 결정 캐노니컬은 §3 비교표 `품질 게이트 소유권` 행). producer 밖의 호출자는 게이트를 별도 호출하거나 fix하지 않으며, 게이트를 "선택" 권유로 두는 해치도 없다. 하네스 §3 체인 리터럴은 SDD **단계** 순서로 유지하되 게이트 두 단계는 producer 내부 수행 예외를 명시한다 — 전파 표면은 `AGENTS.md` §3 + 하네스 템플릿 4미러 = 5곳(누락 시 소비 repo에 이중 호출이 남는다)
  - **feature planning의 producer↔reviewer 계약은 producer 정본 + verifier pointer로 유지한다**: `feature-draft`가 질문 발동·output 구조·AC evidence·minimum-code의 canonical producer contract를 소유하고, verifier(`plan-review`)는 상세를 복제하지 않는다 — AC 평가방법은 `Verification Weakness`에서 검사하고, 근거가 부족하면 읽기를 확장하지 않고 그 smell의 finding을 만들지 않는다. recommendation은 인용 evidence를 해소하는 가장 작은 plan change만 허용한다. `Hidden Decision` 검사는 Open Questions 항목별 결정·확인 필요 여부와 남은 숨은 가정 2개 술어를 rubric 행 하나가 단독 소유한다
  - reviewer의 호출당 실행은 경량 반환 **단일 패스가 유일 mode**다(병렬 분해는 한 호출의 분해이지 별도 내부 pass가 아니다). producer는 gate 1+fix 1을 항상 수행하고, 임계값 경로에서만 두 번째 호출 후 producer별 표적 검증까지 수행한다 — `feature-draft`는 gate 2 인용 평가조건을 final draft에서 재확인, `implementation`은 fix diff 커버리지 델타 + 회귀 재실행 + 증거 테이블 갱신. 두 번째 호출 결과는 첫 호출과 구분해 보고한다
  - simplicity finding은 falsifiable-only gating을 따른다: 동작 변화 없이 더 단순한 동등 형태를 구체적으로 제시할 수 있는 객관적 위반만 Medium 이상(gating)이고, 주관적 취향은 Low(advisory)다. gating을 falsifiable finding으로 한정하는 규칙이 수렴성의 핵심이다. simplicity 렌즈는 `spec-review`로 확장하지 않는다(코드 형태 품질이라 spec 문서 품질에 부적합)
  - 직교 2-렌즈 review의 적용 지점·dispatch 구조·전환 근거의 결정 캐노니컬은 §3 비교표 `직교 2-렌즈 review 렌즈` 행이다. 여기는 집행 규칙만 둔다: simplicity 계약의 단일 소스는 `implementation-review` 스킬의 `references/simplicity-contract.md`(claude/codex 미러)이고 호출 스킬이 전문을 verbatim 포함하며, read-only·재호출 금지는 agent 정의가 아니라 계약 문면의 프롬프트 규칙이다. `pr-review`는 7필드 `PR Review Input`(정의 단일 소스는 pr-review SKILL; simplicity는 `Changed Files`·`PR Diff`로 범위만 고정하고 validation을 재판정하지 않는다)으로 dispatch하고, correctness를 CI → `_sdd/env.md` local validation → 사유 병기 `UNTESTED` 순서로 직접 수행한다 — 실행 evidence 없는 test-dependent `UNTESTED`는 자동 `APPROVE`가 아니라 `NEEDS DISCUSSION`으로 흐른다(non-test-dependent·명시적 N/A 제외). verdict는 메인 루프가 합성해 통합 리포트(`_sdd/pr/..._pr_review_...`) 1파일만 write하고(단일 작성자 불변식 — simplicity reviewer는 파일을 쓰지 않는다), 리포트는 통계 표 없이 행동 대상 finding을 블록 전문으로 싣는다(Pre-merge=correctness Crit/High + simplicity gating Medium+ · non-blocking=correctness Medium · 주관 Low=위치 포함 한 문장). 인간 리뷰 보조이므로 합집합 자동 exit는 없다. 표적 disjoint(correctness=정합·AC·보안·테스트+정확성-중복 ∥ simplicity=동작-불변 형태+형태-중복)와 Medium=gating/Low=advisory 분류는 falsifiable-only gating 규칙을 재사용한다
  - `implementation-review`도 같은 구조다 — simplicity를 **차원 묶음 2개로 분할 dispatch**하고(참조: 중복 코드·단일 사용처 추상화 + 죽은 코드 ∥ 국소: 도달 불가 에러 처리·과잉압축; 각 dispatch는 전체 변경 대상 — **한정은 차원이지 범위가 아니다**; 묶음 정의는 simplicity 계약 reference의 `호출자 차원 한정` 절이 단일 소스, 한정 없는 호출은 전체 4차원 1회 — `pr-review` 경로), 메인 루프가 correctness(기준 문서 적응·읽기 범위 계단·Fresh Verification·ledger MET 접기 — 단일 소스는 SKILL)를 직접 수행한 뒤 판정 없는 합산 보고한다(합집합 exit 없음). "대화에만 있는 맥락 digest"는 simplicity dispatch prompt에만 필요하다(agent는 세션 대화를 못 읽는다). 게이트 호출 시 메인 루프는 방금 구현한 내용을 보유하므로 재독하지 않고 fresh 증거(diff·실행 출력)로 판정한다
  - `plan-review` 게이트는 **분할하지 않는 유일한 게이트**이고 **직접 실행 스킬**이다 — 판정·수집 모두 메인 루프가 수행하고, SKILL.md가 전체 계약(5-smell rubric·Severity·Blocker Policy·반환 형식·읽기 지침 — 배칭/Grep 선행/spec은 draft 명시 인용 anchor만/기록물 금독)의 단일 소스다. **읽기 통제는 순종이 아니라 구조로** — 읽기 규칙을 dispatch된 agent의 순종에 맡기지 않는다. 셀프 리뷰 편향은 사용자 결정으로 감수한다(검출력의 실적 원천은 rubric+evidence 의무, 독립 시선은 `second-opinion`). 재제안 금지 2종: **렌즈/task 축 재분할**과 **수집 agent(gather phase류) 재도입**은 실측을 뒤집는 새 근거 없이는 재제안 대상이 아니다
  - custom agent는 **0종**이고 양 번들은 skills-only다(Codex 플러그인/Agent Plugins 1.0 표준이 custom agent를 번들하지 못하는 배포 제약). simplicity reviewer는 판정만 반환하는 read-only 역할이며 그 강제는 tools 제한이 아니라 계약 문면(Read/Glob/Grep만·파일 수정 금지·재spawn 금지)이다. 리포트 파일 작성은 호출자 소관이고(작성자 불변식의 reviewer 적용), 테스트 실행은 correctness를 직접 수행하는 메인 루프가 slow-test 규칙 아래서 소유한다. 스킬은 산출물을 직접 rewrite하지 않으며(산출물 단일 작성자), fix는 산출물 작성자가 수행한다
    - reviewer 반환에는 **실제 소비자가 있는 항목만** 둔다 — 같은 반환의 다른 항목에서 도출되는 요약 섹션은 두지 않고, 유지/삭제는 소비 실측으로 판정한다
    - reviewer의 supporting-context 읽기에는 입력 상한을 걸되 **상한의 형태는 리뷰 대상에 맞춘다** — draft 문서를 보는 `plan-review`는 더 싼 수단을 먼저 쓰게 하는 **최소 읽기 규칙**(`Glob`·`Grep`으로 닫히는 판정은 `Read`하지 않고, `Read`를 앞선 도구 호출과 함께 미리 당겨 부르지도 않으며, 그래도 근거가 부족하면 그 smell의 finding을 만들지 않고 읽기를 확장하지 않는다)이고, 코드 correctness를 보는 `implementation-review`는 도구가 아니라 무엇을 읽을지를 제한하는 **읽기 범위 계단**이다(correctness 렌즈는 본문 읽기가 로직 결함 탐지의 핵심 수단이라 도구 제한 형태를 이식하면 검출력이 깎인다 — 직접 실행 전환 후에도 계단은 메인 루프의 읽기 규율로 유지). 어느 형태든 상한은 검토 의무를 낮추지 않는다 — AC가 명시적으로 요구하는 증거는 범위 밖이라도 확보하고, 못 대면 사유를 병기해 미달로 표기한다. 각 상한 규칙의 단일 소유자는 해당 SKILL의 읽기 절이고(다른 절·Error Handling 행은 포인터만) 계단 상세는 [components.md](./components.md)의 해당 컴포넌트 행에 둔다. `pr-review` correctness는 상한 대상이 아니며(인간 리뷰 보조라 충분히 시간을 들이는 편이 낫다는 판단 — `Changed Files` 범위 고정만 적용) `simplicity-review`도 현재 미적용이다
    - 판정 표를 가진 reviewer 반환은 **문제 있는 항목만 개별 행으로 내고 나머지는 `PASS: <이름 나열>` 한 줄로 접는다**(현재 대상: simplicity 계약 4 차원). 점검·스캔 의무는 그대로이고 출력 의무만 완화된다 — 완전성 불변식(전 항목이 개별 행 또는 PASS 접기 중 정확히 하나에 귀속)은 계약 문서의 **AC 절 한 곳**이 소유하고 반환 형식 절에는 재서술하지 않는다
    - reviewer 반환에는 **finding이 아닌 확인 결과를 열거하지 않는다** — 대조 결과는 판정에 기여하지 않고 `Findings`(+ `simplicity-review`의 `차원 판정` 표, PASS 접기 포함)가 전부다. 반환은 명시된 항목이 전부이며 규칙은 **무조건**이다(렌즈/차원 한정 여부와 무관). 줄이는 것은 **출력이지 대조·스캔 범위가 아니다**(점검 의무는 그대로 — 근거: 게이트 벽시계의 지배 성분은 리포트 작성량). 적용 대상은 simplicity 계약과 `plan-review` SKILL 반환 절이고, 소유자는 반환 형식 절 1문장 + 준수를 흡수한 자체 검증 AC다. correctness 계열은 Verification ledger가 반환 계약이라 PASS 접기 대상이 아니며 아래 **ledger MET 접기**가 같은 다이어트를 ledger 형식에 적용한다
  - **리뷰 읽기 다이어트** — 리뷰 벽시계는 병렬화 완결 이후 pole 작성자의 "읽고 확인할 양"이 결정하므로, 품질 선별 타협 2종을 적용한다. 재제안 금지: **사실 주장을 별도 구조에 선고정해 reviewer 대조 범위를 좁히는 축**(구 Claim Manifest — 도입 당일 철회)은 실측을 뒤집는 새 근거 없이는 재제안 대상이 아니다
    - **위험 적응형 읽기**: `implementation-review` 읽기 범위 계단 ①의 변경 파일 읽기는 diff hunk+주변 문맥이 기본이고, 위험 신호 시에만 파일 전문으로 승격하며 미승격 파일은 보고에 `hunk-scoped`로 표기한다(승격 트리거 6종·overflow 규칙의 단일 소스는 SKILL의 Correctness 리뷰 절). 기준 문서 전문 Read·spec 절 한정·correctness 능동 검토 결속은 불변이다
    - **ledger MET 접기**: `implementation-review` Verification ledger와 `pr-review` AC 검증 ledger(현 소유자: 각 SKILL의 correctness 절)는 문제 있는 verdict(NOT MET·UNTESTED·PARTIAL·FAIL)만 증거 행으로 내고, 통과(MET)는 `MET: AC1–AC5`/`MET: #1–#N` 꼴 축약 한 줄로 접는다 — 판정-측 "증거 없는 MET 금지"는 보존하고 반환-측 전사만 다이어트한다(감사 흔적만 희생, 탐지 보존)
- 구현의 test-first는 `implementation` 스킬이 메인 루프에서 직접 집행하는 실행 규율이다: task별 3-way triage — (a) test: 실패하는 테스트 작성 가능, (b) structural-check: 프레임워크 부재 자산이라도 grep·diff·exit code로 실질 구조를 판정 가능, (c) test-free: 동어반복 check뿐인 non-falsifiable task(분류 근거 1줄 기록 필수, "간단한 구현이라서"는 (c) 자격이 아니며 경계 애매하면 (b)로 보수 분류) — 이후 (a)/(b)는 RED 실패 관찰 전 구현 금지 → 최소 구현 GREEN → 커버리지 델타 → 마감 시 AC→증거 테이블(증거 없는 AC는 "충족" 금지). triage와 규칙의 canonical surface는 `implementation` SKILL이다
  - 커버리지 델타: 테스트 집합을 AC의 함수로 두지 않는다 — 각 task의 GREEN 직후 그 task의 diff를 **실제로 실행해 읽고**, 방금 통과시킨 테스트가 도달하지 않는 동작을 열거한다. 불필요분은 **삭제가 1순위**(GREEN 최소성)이고, 삭제 후 (a)/(b)는 테스트/check를 재실행해 통과 재확인·출력 갱신 캡처한다(재확인 실패면 삭제를 되돌려 남기기 경로 — (c)는 실행할 check가 없어 범위 밖). 남기는 항목만 triage 기준으로 닫는다. 델타 테스트는 RED가 불가하므로 **변이 확인**(파괴 → 실패 관찰 → 복구 → 통과 재확인)으로 판별력을 증명한다. 게이트 fix diff에도 적용한다(fix 산출물은 AC 확정 뒤 태어나 AC 유래 테스트가 구조적으로 없다). (c) task도 건너뛰지 않는다(도달 check 0개라 diff 전량이 열거 대상). 델타가 없으면 아무것도 적지 않는다(스킵과 0건의 사후 구분 불가는 accepted trade-off). 소유권: 델타 절=적용 대상, `fix → 델타 → 회귀` 순서=마감 절(순서 명제 복제 금지 — 서술 절에 두면 집행 트리거가 없다). 위치가 GREEN 직후인 이유: 마감으로 미루면 코드를 보고 짜맞춘 테스트가 되고, `implementation-review`로 미루면 읽기 범위 계단과 충돌하며 fix 타이밍이 늦다
- `implementation` 마감 순서는 회귀 1회 → AC→증거 테이블 → gate 1 → fix 1 → (fix 전 raw 합산 finding 임계값 시) gate 2 → fix 2 → 마감 요약이며, **이 순서 항이 순서 명제의 단일 소유자**다. 각 fix는 그 fix diff에 커버리지 델타를 먼저 적용한 뒤 회귀를 재실행한다 — 델타 선행은 fix diff 한정, 회귀 재실행은 fix 전체에 걸린다(회귀 의무를 "구현이 바뀐 fix"로 좁히면 문서·테스트만 고친 fix가 회귀를 건너뛴다). Low fix는 렌즈로 가른다 — correctness Low는 **저비용 AND 명백히 이득 AND 현재 change scope 내** 3조건 충족 시만(마지막 조건이 scope 확장을 막는 load-bearing conjunct), simplicity Low(주관)는 advisory 고정. 마감 요약이 finding/fix 내역의 유일 소스다(호출자는 게이트를 다시 돌지 않는다). 이 마감 반환 계약은 `implementation`에만 적용한다(`feature-draft`는 Open Questions 한정 출력 다이어트가 의도된 설계)
  - 모든 `implementation` 실행은 **resume-only implementation ledger**(`_sdd/implementation/*_implementation_ledger_*.md`, 같은 slug 이어쓰기)를 생성한다 — 목적은 감사 로그가 아니라 compact/세션 재개 후 다음 행동을 결정하는 resume pointer라, 기록 기준은 **재실행으로 복원할 수 없는 사실만**이다(필드 구성·4단계 상태·재개 규칙의 canonical surface는 `implementation` SKILL). 재개 시 미완료 task는 ledger 상태를 신뢰하지 않고 fresh 재판정한다. reviewer들은 ledger를 소비하지 않는다(fresh verification 원칙 불변). 문서 표면은 `docs/SDD_SPEC_DEFINITION.md` §6 증거 기록처 문장과 `docs/AUTOPILOT_GUIDE.md` 산출물 목록(각 ko·en)이다
  - 테스트 불변 규칙: RED 관찰 후에는 테스트를 통과시키기 위해 테스트를 약화·수정하지 않는다. 계약이 틀렸다고 판단되면 선언을 남기고 테스트 수정 → 재-RED 후 구현으로 돌아가며, 같은 task에서 선언이 반복되면 구현 중단 + draft 복귀다. 이 규칙은 델타 테스트에도 동일하게 적용되며, RED가 없는 델타 테스트에서는 구제 절차의 "RED 재관찰"이 변이 확인 재수행으로 대체된다(대체 규칙의 소유자는 커버리지 델타 절이고 불변 규칙 본문은 무변경이다)
- 스킬의 dispatch는 런타임 내장 agent type(Claude `general-purpose`, Codex `explorer`)만 사용한다
- `sdd-autopilot`은 existing `goal-init(preset=sdd)`를 호출하는 setup-only thin entrypoint다. 사용자 목표와 관련 context를 runtime별 canonical 방식(Claude plugin-prefixed invocation / Codex active installed skill catalog)으로 전달하고, `goal-init`이 만든 자족적 조건 문자열·runtime 실행법·4파일 경로를 relay한 뒤 사용자 activation 경계에서 종료한다
  - setup에서는 initial `feature-draft`·`implementation`·`spec-sync`를 실행하지 않고 native goal을 활성화하지 않는다. current goal status도 조회하지 않으며 existing goal을 set·clear·pause·resume·replace·merge하거나 active goal 때문에 setup을 차단하지 않는다
  - SDD preset은 generic `goal-init`의 Goal Intake → Divergence → Condition Crafting → Harness Setup → Handoff 5단계, condition self-check, `goal.md`·`experiments.md`·`journal.md`·`report.md` 4파일 계약을 그대로 재사용하고 `goal.md`의 `Loop Protocol` payload만 바꾼다. `goal.md`는 조건 문자열(outcome 수준 DONE WHEN + 위조 어려운 anchor + 표준 레시피 참조 문구 + drift 가드 CONSTRAINT) / 검증 레시피(브리틀 검증 디테일 — goal 재설정 없이 수정 가능) / Loop Protocol(HOW)의 3분법 계약이다
  - 사용자가 native goal을 활성화한 뒤에는 미충족 `DONE WHEN` 또는 실패한 final integration proof gap에서 가장 작은 next feature를 골라 `feature-draft → implementation → (persistent 변경 시) spec-sync → evidence·gap 기록 → final integration proof`로 수렴한다. draft가 분할되면 current goal 안에서 smallest next unit을 계속 선택하며 nested `goal-init`은 만들지 않는다
  - formal Goal Contract·scope ID·Initial Feature Queue·status manifest·goal-level reviewer는 도입하지 않고, 조건·하네스 shape·loop payload의 단일 소스는 `goal-init`에 둔다
- SDD 체인 진입은 **사용자 요청이 판정한다**(하네스 §3 canonical): SDD는 사용자의 직간접 요청 — 단계 스킬 호출(`discussion`·`feature-draft` 등) 또는 "SDD로 구현/작업하자" 류 지시 — 으로 적용된다. 요청이 없더라도 구현할 기능이 크거나 복잡하거나 스펙에 상당한 영향을 주는 작업이면 **SDD 적용 여부를 사용자에게 질문**하고, 그 외에는 비대상으로 보고 SDD 없이 바로 수행한다. 비적용 경로에서도 §2 작업 규약·검증 표준은 그대로 지키며, 스펙 변경이 생기면 `spec-sync` 호출 여부를 사용자에게 확인받는다. canonical은 하네스 §3이고 전파 표면은 `AGENTS.md` + `spec-create`·`spec-upgrade` 하네스 템플릿 4미러 = 5곳이라, 두 스킬이 초기화하는 모든 소비 repo의 하네스에 적용된다
- SDD 체인은 `feature-draft`·`implementation`이 유일 경로다 — 일반 구현 요청 트리거는 `implementation` 스킬이 유일 수신 경로이고, draft 파일명 glob은 `*_feature_draft_*`다(lite 파일명은 substring 하위호환, full 레인 복구 보험은 git tag `full-lane-final`)
- subagent를 dispatch하는 review 계열 스킬(`plan-review`·`implementation-review`·`pr-review`)의 subagent 모델 override는 런타임별 explicit per-call option으로만 취급하고, 지정 시 그 스킬의 모든 dispatch에 균일 적용된다. 옵션을 생략하면 세션/agent 기본값을 상속한다. 구현·planning 스킬(`implementation`·`feature-draft`)은 메인 루프 직접 작성이라 override 비대상이다
  - Claude Code는 `--model <sonnet|opus|haiku|fable>`로 `Agent(...)` 호출의 model만 override한다
  - Codex는 `--model`과 `--effort`를 분리해 각각 선택된 active `spawn_agent` schema의 `model`·`reasoning_effort` enum으로 검증하고 해당 필드를 override한다. 세 review skill은 고정 allowlist를 소유하지 않으며, 요청 필드가 없거나 값이 enum 밖이면 dispatch 전에 schema가 노출한 허용값과 함께 blocker를 보고한다. 문서의 구체 모델·effort 값은 현재 예시일 뿐 persistent contract가 아니다
- non-trivial planning은 `feature-draft`에서 시작한다. 후속 phase/task 확장 스킬은 없다 — 규모 초과는 분할 규칙으로 해소한다
  - 규모 판정(분할 여부)과 census 검증 task 규칙의 소유자는 `feature-draft` SKILL **단독**이다. 계획 게이트 reviewer는 규모를 재판정하지 않으며, draft 상단 `> 규모 판정:` 마커는 producer 표면일 뿐 reviewer 대조 앵커가 아니다 — 규모 판정 검사를 reviewer rubric·반환 항목으로 되돌리지 않는다(검사 표면을 producer 한 곳으로 모으는 것이 이 결정의 요지다)
- 구현 전 계획 품질 점검은 `feature-draft`가 소유한 review-only gate(`plan-review`)로 수행한다. 이 gate는 plan을 직접 수정하지 않고 경량 반환으로만 응답하며(리포트 파일 없음), Critical/High finding만 implementation blocker로 표시한다. 사용자가 draft 없이 기존 계획만 점검하려는 경우에 한해 `plan-review`를 직접 호출할 수 있다
- skill-defined output artifact의 이력 관리는 `prev/` 백업 체인보다 append-only artifact와 git history를 기본으로 사용한다
- spec mutation은 target file을 식별한 뒤에만 수행한다
- current spec model과 workflow semantics의 기준은 [docs/SDD_SPEC_DEFINITION.md](../../docs/SDD_SPEC_DEFINITION.md)와 [docs/SDD_WORKFLOW.md](../../docs/SDD_WORKFLOW.md)에 둔다
- 환경 및 실행 제약은 [../env.md](../env.md)를 authoritative source로 본다
- `Strategic Code Map`은 agentic coding을 위한 optional navigation hint로만 사용한다. 전체 파일 트리, 컴포넌트 카탈로그, API reference, 구현 narrative로 확장하지 않으며, temporary `Touchpoints`는 검증된 persistent entrypoint / extension point / invariant hotspot / validation surface가 된 경우에만 global supporting surface로 승격한다

## 3. 핵심 설계와 주요 결정

### 핵심 설계

SDD Skills의 설계는 다음 층으로 나뉜다.

1. Skill layer: 사용자가 직접 호출하는 entrypoint — 계약의 단일 소스(`SKILL.md` + `references/` 계약 문서; dispatch는 런타임 내장 agent에 계약을 프롬프트로 주입)
2. Artifact layer: `_sdd/` 아래의 persistent handoff contract
3. Reference layer: README, `docs/`, global spec이 유지하는 설명과 경계

이 위에 별도의 **Harness layer(`AGENTS.md`)** 가 놓인다. harness는 repo 작업 진입점이자 작업 규약(how) 레이어로, global spec(이해 = what/why)과 같은 정보를 중복 보유하지 않는다 — repo-specific 행동 트리거와 핵심 결정은 여전히 Guardrails가 단일 소스다. harness는 산문 규약과 그 규약을 실행하는 자산(훅)을 함께 포함하며, 자산은 규약을 **강제**하거나(work log 커밋 게이트) 컨텍스트에서 사라진 규약을 **되돌려 놓는다**(compact 후 SessionStart 재주입 — "읽으라는 지시"가 아니라 내용 주입: 지시는 재량이 남아 실패 모드를 재생산하고 Read 왕복 대비 비용 이점도 없다). 둘 다 모델 재량으로 건너뛸 수 없는 층이다(advisory watchdog은 강제 층 밖 보조 자산). §0은 SDD 고유 불변식 3종만 배포한다 — `Separate Truth by Lifetime`·`Evidence Before Promotion`(AC 검증이 current truth 승격 조건 — 자동 spec-sync·사람 승인 의무 아님)·`Persist Outcomes, Not Process`(간결한 결정·결과·evidence·pointer 보존, 단계별 실행 서술 제외). 일반 agent 원칙은 배포 계약이 아니다([docs/agentic_coding_principle.md](../../docs/agentic_coding_principle.md)는 참고 자산). layer model 기준은 [docs/SDD_CONCEPT.md](../../docs/SDD_CONCEPT.md)와 [docs/SDD_WORKFLOW.md](../../docs/SDD_WORKFLOW.md)에 둔다.

### 유지해야 할 주요 결정

| 결정 | 현재 선택 | 유지 이유 |
|------|-----------|-----------|
| Skill 정의 형식 | Markdown `SKILL.md` 단일 파일 — frontmatter가 name/description(+ 런타임이 읽는 선택 키) 등 스킬 메타데이터의 단일 소스이고, 스킬 버전을 담는 필드·파일은 두지 않는다(스킬 변경 이력 = git history) | AI 에이전트가 직접 읽고 실행 규약을 추론하기 쉽다. 런타임이 읽지 않는 메타데이터는 사이드카 파일(구 `skill.json`)이든 frontmatter 필드(구 `version:`)든 드리프트가 감지되지 않는 채 누적되므로, 소비자가 없는 값은 두지 않고 버전 lockstep 검사 대상을 0으로 유지한다 |
| 런타임 구조 | Claude/Codex dual bundle | 동일한 SDD 철학을 유지하면서 플랫폼별 실행 차이를 흡수한다 |
| Codex/Claude hook parity and dual-setting runtime acceptance | 공용 script 4개는 `.claude/hooks/` 실행 경로를 공유하고, `spec-create`·`spec-upgrade`는 `.claude/settings.json`과 `.codex/hooks.json`을 독립·멱등 병합한다. 구조 parity만으로 완료 처리하지 않고 Codex trust boundary와 양 runtime lifecycle acceptance까지 검증한다 | 기존 Claude 경로와 소비 repo 호환성을 유지하면서 실행 bytes를 한 벌로 공유하고, 한쪽 설정 손상이 다른 runtime 설치를 막지 않게 한다. 사용자 설정 보존·명시적 trust·실제 lifecycle 증거를 완료 조건에 포함해 등록만 된 무발동 상태나 위험한 trust 우회를 parity로 오인하지 않는다 |
| Codex multi-agent runtime adapter | active tool schema로 mailbox 또는 legacy target/close contract 중 정확히 하나를 선택한다. Desktop과 현재 CLI 0.146.0은 mailbox contract로 수렴하며, legacy target/close는 target wait와 close lifecycle이 함께 노출될 때만 사용한다 | runtime 이름을 capability의 대리값으로 쓰지 않아 schema 세대 차이를 안전하게 흡수하고, 존재하지 않는 lifecycle 호출·혼합 contract·지원되지 않는 override 전달을 차단한다 |
| 실행 분리 | skill이 계약 단일 소스이고 custom agent는 0종. leaf dispatch가 필요한 execution(`implementation-review`·`pr-review`의 simplicity 렌즈, `investigate` 조건부 explore fan-out)은 `orchestrator skill + 계약 주입 범용 leaf agent`, 그 외 리뷰·구현·planning·spec 파이프라인은 메인 루프 직접 실행 | 계약을 스킬 표면 한 곳에 모아 번들 배포(skills-only)와 nesting 1단계 제한을 함께 만족하고, dispatch는 병렬성이 실익일 때만 쓴다 |
| 상태 전달 | `_sdd/` 파일 아티팩트 중심 | 세션 메모리 의존을 줄이고 재현성과 git 추적성을 높인다 |
| 품질 게이트 | AC-First + explicit verification | "should work" 식 추측을 줄이고 종료 조건을 명확히 한다 |
| 장문 산출물 작성 | producer-owned inline 2-phase writing | skeleton/fill/finalize를 같은 문맥에서 처리해 품질 저하를 줄인다 |
| spec template load interface | `spec-create` Step 4는 compact를 기본으로 하되 source의 project motivation·evaluated-alternative rationale를 compact의 named slot에 의미 손실 없이 보존할 수 없을 때만 full을 고르고, 작성 직전에 선택한 runtime-local template 하나의 전체 skeleton을 verbatim 적용한다. Claude template pair가 authoring canonical이고 Codex pair는 runtime invocation token만 다른 distribution mirror다. `spec-upgrade`는 Step 1의 불충분한 경계 판정에 mapping을, Step 2의 exact global 비교에 global-only `spec-format`을, mixed temporary 판정에 same-runtime `feature-draft` `Required Output`을, Step 5 작성에 선택한 fenced template 하나를 읽는다 | rich reference를 실제 소비 시점에만 읽고 template·temporary shape의 소유자를 하나로 유지해, stale 복제와 memory reconstruction drift를 막는다 |
| document producer output interface | `spec-summary`와 `guide-create`는 작성 직전에 runtime-local rich reference의 fenced skeleton을 verbatim 적용하며, output shape·rubric은 그 reference 한 곳만 소유한다. `spec-snapshot`은 별도 reference 없이 양 runtime의 공통 SKILL 본문이 source manifest·destination collision·metadata/body 보존 interface를 소유하고, source pre/post manifest exact match를 완료 hard gate로 둔다. 세 producer는 main loop가 skeleton 또는 file set을 직접 작성·검증하며 runtime helper lifecycle이나 완성 example로 같은 계약을 재소유하지 않는다 | 실제 산출물 interface를 한 곳에서 기계적으로 소비하면 설명·예시·runtime mirror 사이의 format drift를 줄이고, snapshot 원본 read-only와 재현 가능한 보존 경계를 검증할 수 있다 |
| SDD goal 실행 경계 | `sdd-autopilot`은 `goal-init(preset=sdd)` setup adapter이고, 실제 반복 실행은 사용자가 활성화한 native goal의 SDD Loop Protocol이 소유한다. setup은 producer 실행·goal status 조회·goal mutation을 하지 않는다 | harness 준비와 실행 activation을 분리해 existing goal에 대한 숨은 상태 변경을 막고, generic goal 계약을 재사용하면서 여러 SDD unit의 수렴은 native goal lifecycle에 맡긴다 |
| 규모 초과 대응 | 승격이 아니라 분할 — 분할 필요 판정(coverage 눈검산 불가)은 롤링 분할 draft + `spec-sync` planned todo 고정 + feature별 순차 체인으로 해소한다. active SDD goal에서는 current goal이 smallest next unit을 계속 선택하고 nested `goal-init`을 만들지 않는다 | 규모 초과를 더 큰 파이프라인이나 nested goal로 올리면 실행 상태가 분산된다. 분할은 "단일 컨텍스트 = 품질 전제"를 유지하면서 하나의 goal이 integration proof까지 수렴하게 한다 |
| planning precedence | `feature-draft`가 유일 planning entry. 후속 확장 스킬 없음 — 규모 초과는 분할 | non-trivial 변경에서 peer-choice 혼선을 없애고 "단일 컨텍스트 = 품질 전제"를 유지한다 |
| 품질 게이트 소유권 | producer-owned bounded loop — `feature-draft`가 `plan-review`(review-only, 호출당 단일 패스 경량 반환, 리포트 파일 없음)를, `implementation`이 `implementation-review`를 각각 자기 마감의 강제 gate로 호출한다. gate 1+fix 1은 항상 수행하고, fix 전 raw finding이 `Critical+High ≥ 3` 또는 `Medium ≥ 5`일 때만 gate 2+fix 2를 수행한다(Low 제외, implementation shard 합산 dedup 없음). gate 3 대신 gate 2도 임계값이면 수동 후속 review를 권고한다. producer 밖의 호출자는 gate를 별도 호출하거나 fix하지 않으며 "선택" 해치는 없다 | 게이트 소유자를 산출물 작성자로 고정하면 직접 호출과 native goal loop 모두 같은 품질 계약을 거치고, 호출자 중복 없이 finding이 많은 경우에만 한 번 더 검증하면서 실행 상한도 유지한다. plan gate는 findings-first로 요청 정합성·task boundary·숨은 결정·과잉 설계·검증 약점 smell을 드러내되 plan 자체는 수정하지 않는다 |
| implementation test-first | `implementation` 스킬 메인 루프가 직접 집행 — 3-way triage → RED 관찰 전 구현 금지 → 최소 GREEN → 커버리지 델타(변이 확인) → 테스트 불변 규칙 → AC→증거 테이블 + 게이트 마감, resume-only ledger 생성·갱신(집행 문면은 §2 해당 불릿과 `implementation` SKILL이 소유). leaf 분리(test-author/implementation agent)와 orchestrator RED 게이트는 F2에서 삭제 — 대체 안전장치는 테스트 불변 규칙 + `implementation-review` Fresh Verification | 소규모 구현에서 dispatch 오버헤드 없이 test-first 규율과 falsifiability를 유지하고, 증거 없는 "충족" 보고와 테스트 약화 퇴화를 차단한다. 커버리지 델타는 AC의 함수였던 테스트 집합을 diff의 함수로 넓혀, 구현이 AC보다 넓어진 부분이 무테스트로 남던 사각지대(증거 테이블은 AC 단위, `implementation-review`는 AC ledger + 읽기 범위 계단이라 양쪽 모두 볼 수 없다)를 구현 시점에 닫는다 |
| 직교 2-렌즈 review 렌즈 | correctness는 메인 루프 직접 수행 ∥ simplicity는 계약 주입 범용 subagent dispatch — 적용 지점은 PR review(`pr-review`: 직접 correctness + verdict 합성; simplicity는 차원 한정 없는 전체 4차원 1회)와 implementation 마감 게이트(`implementation-review`: 직접 correctness + simplicity 차원 묶음 2회, 각 dispatch 전체 변경). simplicity dispatch를 먼저 띄우고 correctness를 병행 수행하며, `--model` override는 simplicity dispatch에만 적용된다. simplicity는 falsifiable-only gating | 정확성과 동작-불변 형태 품질을 disjoint 표적으로 분리해 검출 범위를 넓힌다. 읽기 통제는 순종이 아니라 구조로 확보하고, 벽시계는 simplicity 병렬 그늘에서 correctness 직접 수행이 결정한다(두 작업의 max). 중복 탐지 렌즈는 두 지점을 같이 봐야 해서 task로 분할하지 않는다. 셀프 리뷰 편향은 사용자 결정으로 감수(rubric+증거 결속이 검출의 실체, 독립 시선은 simplicity dispatch·`second-opinion`) |
| subagent model override | review 계열 스킬(`plan-review`·`implementation-review`·`pr-review`)의 subagent 호출은 필요할 때만 런타임별 per-call option으로 모델/추론 강도를 override한다. Claude는 `--model` 단일 옵션, Codex는 `--model`과 `--effort` 분리 옵션을 canonical로 두되 허용값은 선택된 active `spawn_agent` schema의 각 enum이 결정한다 | 기본 세션/agent 설정 상속을 보존하면서 특정 실행만 강도·비용·속도에 맞게 조절하고, 저장소 allowlist가 runtime schema와 drift하는 일을 막으며, 플랫폼별 tool schema 차이를 숨기지 않는다 |
| spec 구조 | thin global spec + execution-focused temporary spec | 장기 기준과 일회성 실행 정보를 분리해 drift를 줄인다 |
| spec sync 진입점 | 단일 `spec-sync` 스킬의 **직접 실행**(agent 없음 — SKILL.md 짝이 계약 단일 소스). 구현 전/후 구분은 별도 스킬이 아니라 evidence-driven status 분류로 처리 | 두 진입점(`spec-update-todo`/`spec-update-done`) 이분 진입을 제거해 운영 표면을 줄이면서, 코드+validation evidence 유무로 동작이 자동 적응한다 |
| spec review 판정 인터페이스 | `spec-review`의 drift status는 evidence sufficiency → 탐색 완료 후 one-side absence → 양면 비교 순서로, spec disposition은 material uncertainty → verified spec change → otherwise 순서로 각각 하나를 고른다. Output은 이 producer 판정을 pointer로 소비하고, code analysis는 고정 metric 없이 finding에 연결된 optional evidence로만 남긴다 | 불충분 evidence를 부재로 오판하거나 구현 측 drift를 spec 변경으로 잘못 라우팅하는 일을 막고, decision이 소비하지 않는 metric 의식을 제거한다 |
| Strategic Code Map | optional compact navigation surface | global spec을 inventory로 되돌리지 않으면서 사람과 LLM agent가 entrypoint, contract source, invariant hotspot, extension point, validation surface를 빠르게 찾게 한다 |
| artifact naming/history | lowercase canonical artifact를 기본으로 하고, skill contract가 정의한 output surface는 dated slug naming과 git-history-first 추적을 따른다 | 산출물 경로 추론을 단순화하고 legacy fixed-name drift를 줄인다 |
| canonical rollout 순서 | `definition -> generators/transformers -> consumers/planners -> docs -> english mirrors/examples -> audit` | definition, skill behavior, human docs drift를 줄인다 |

### 운영상 반드시 유지할 구조적 판단

- draft/plan/review skill chain은 `_sdd/` 산출물을 다음 단계 입력 계약으로 사용한다
- temporary delta는 global truth를 반복 복사하지 않고, 변경 범위와 검증 정보만 다룬다
- skill-defined output artifact는 dated slug + glob-based discovery를 canonical로 사용하고, legacy uppercase/fixed-name artifact는 transition fallback으로만 읽는다
- canonical model 변경은 definition 문서와 workflow 문서에서 먼저 선언하고, 이후 generator/consumer/docs가 따라간다
- supporting docs는 global decision-bearing truth를 복제하지 않고, reference 역할만 수행한다
- spec lifecycle skill은 `Strategic Code Map`을 현재 코드 탐색의 출발점으로만 사용해야 한다. `feature-draft` planning의 `Target Files`는 항상 현재 코드 실측으로 확인한다
- `spec-sync`는 코드+validation evidence가 있는 항목만 현재 사실로 승격하고, evidence 없는 항목은 기본적으로 `🚧 Planned` 또는 보류로 둔다. verified truth와 planned truth를 같은 문단·불릿에 무표식으로 섞지 않는다(미구현·미검증을 완료 사실로 기록하지 않는 안전 불변식)

### 현재 운영 제약

- Claude와 Codex 문서/skill parity는 완전 자동 동기화가 아니라 유지보수자의 수동 관리다 — SKILL.md 짝과 references 계약 문서 짝의 3-way 적응 미러링이 유지보수 단위다
- 이 저장소는 전통적인 테스트 프레임워크보다 실제 skill invocation과 리뷰 기반 검증에 크게 의존한다
- dispatch되는 agent/skill은 작업트리가 아니라 **plugin 설치본**(`~/.claude/plugins/cache/<marketplace>/<plugin>/<pushed SHA>/`)에서 로드된다 — 방금 편집한 agent 본문은 커밋·푸시로 플러그인이 갱신되기 전까지 그 세션의 dispatch에 발효되지 않는다(실측: 설치본에 당일 편집한 규칙 0/5, 전날 머지분은 존재). 따라서 **같은 세션의 마감 게이트로 자기 변경의 효과를 계측하는 설계는 구조적으로 무효**이고, agent 행동 계측은 (a) 커밋·푸시 후 플러그인 갱신 + (b) 검증 대상 개념을 호출자 digest에 넣지 않은 새 세션을 전제조건으로 갖는다. 규칙이 로드되지 않은 실행은 그 규칙의 반증이 아니다. 같은 이유로 **동시 A/B 대조는 불가능하다** — 활성 설치본은 시점당 하나뿐이라 처치군과 대조군을 같은 시각에 돌릴 수 없다. 따라서 agent 행동 변경의 효과 확인은 도입 전후의 **누적 관측**으로만 설계할 수 있고, 대조군 회차 자체에 변동이 있으므로(같은 지표에서 회차별로 다른 값이 나온다) n=1 arm 비교로 결론내지 않는다
- agent 행동을 transcript로 계측할 때는 지표를 먼저 검증한다 — subagent transcript(JSONL)는 content 블록을 줄 단위로 쪼개 기록하므로 "메시지당 tool_use 수"는 배칭을 탐지하지 못하고, 유효 지표는 **연속 실행 길이**이며 양성 대조로 판별력을 확인한 뒤 쓴다. 자기 행동 보고는 transcript 계수로 교차검증하고, **tool 호출 수는 배칭 여지의 대리지표가 아니다** — 셸로 엮이는 작업은 이미 복합 명령 한 호출로 접혀 있어 호출 내용까지 봐야 여지를 과대 추정하지 않는다
- 🚧 Planned: tool call 배칭 규칙의 **행동 효과**는 미검증이다 — 전제조건을 갖춘 첫 처치군 관측 2회차가 음성(최대 연속 실행 길이 1, 지표 판별력은 양성 대조 완료). 규칙을 되돌리지도 강화하지도 않고 **배칭과 무관한 과제 2~3건을 더 쌓아** 연속 1이 고정인지 확인한 뒤 판정한다(지금 되돌리면 n=1 음성 결론, 지금 강화하면 효과 미확인 상태의 규칙 비대). 벽시계 절감 폭은 어떤 표본으로도 주장하지 않는다(회차 상세는 decision_log)
- 🚧 Planned: reviewer 반환 다이어트(simplicity 반환 — 계약은 2026-08-18부터 reference 문서 소유, 규칙 문면 불변이라 관측 연속성 유지)의 **효과 판정**은 미확정이다 — 첫 관측 1회(발효 후 첫 `implementation-review` 게이트)를 확보했고 누적을 계속한다. 판정은 plan-review 다이어트와 동일한 2-기준(시간 + 반환에 확인 목록이 실렸는지)이다. **첫 관측(n=1)**: 시간 기준은 대폭 감소(참조 279→53s, 국소 147→71s)했으나 비-finding 열거("스캔 근거 요약"·"폐기 근거"·"스캔 범위" 단락)는 잔존했다 — 2기준 중 1개만 충족이라 판정은 유보하고 누적을 계속한다. 부수 관측(도입 회차, 발효 전 게이트): 구계약 simplicity reviewer들이 "스캔 요지"·"폐기 후보 상술" 단락을 반환에 실었다 — 규칙이 막으려는 습성이 실재한다는 증거다
- 🚧 Planned: `plan-review` **게이트 2 발동 임계의 규모 비례화**는 미착수 별도 feature다 — 현행 고정 임계(fix 전 raw `Critical+High ≥ 3` 또는 `Medium ≥ 5`)는 task 4개·AC 25개급 대형 draft에서 사실상 항상 발동해 게이트 2가 상수 비용이 된다. 후보 방향: 임계를 draft 규모에 비례시키거나 재게이트를 blocker task 한정으로 좁힌다
- 🚧 Planned: implementation ledger의 **실사용 관측**은 미확정이다 — 계약 자체는 구현·검증 완료이나(structural check 회귀 35/35·변이 확인 3회 kill·미러 byte parity), 도입 후 수 회의 구현에서 ledger가 실제 재개(compact/세션 단절)에 읽힌 적이 있는지 관측하고 전혀 사용되지 않으면 회수를 재검토한다. 관측 대상은 효용이지 계약 준수가 아니다
- `docs/` ko 본문과 `docs/en/` 미러의 세대 정합도 수동 관리다 — canonical rollout 순서의 `english mirrors` 단계가 가장 누락되기 쉬운 지점이고, 레이어·섹션 추가를 ko에만 반영하고 닫으면 en 짝이 한 세대 뒤처진다(하네스 레이어 추가가 en `SDD_WORKFLOW`·`SDD_CONCEPT`에 전파되지 않아 §2 Harness 누락 + 삭제된 full 레인 어휘 잔존으로 드러난 전례). ko/en 짝을 건드리는 변경은 대칭 마감을 검증 대상으로 둔다

## Supporting Surfaces

- [components.md](./components.md): component reference와 탐색용 code/navigation hint
- [usage-guide.md](./usage-guide.md): scenario-oriented usage guide와 expected result surface
- [decision_log.md](./decision_log.md): 구조 변경과 주요 spec 판단 이력
- [logs/changelog.md](./logs/changelog.md): 릴리스 및 문서 변경 이력
- [README.md](../../README.md), [docs/SDD_SPEC_DEFINITION.md](../../docs/SDD_SPEC_DEFINITION.md), [docs/SDD_WORKFLOW.md](../../docs/SDD_WORKFLOW.md): 설치, canonical model, workflow semantics 기준 문서
- [docs/SKILL_AUTHORING_NORMS.md](../../docs/SKILL_AUTHORING_NORMS.md): 스킬·agent·하네스 문서를 작성/수정할 때 점검하는 Claude 5 세대 제작 규범 체크리스트(런타임 참조 문서 아님 — [docs/agentic_coding_principle.md](../../docs/agentic_coding_principle.md)와 같은 참고 자산 계층)
