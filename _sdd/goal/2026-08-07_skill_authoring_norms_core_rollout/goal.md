# Goal: SKILL_AUTHORING_NORMS 핵심 스킬 전수 롤아웃

## 목표 서술
discussion을 제외한 SDD 핵심 스펙·구현 스킬과 딸린 agent를 `docs/SKILL_AUTHORING_NORMS.md` 기준으로 전수 감사하고, 우선순위별로 필요한 다이어트를 적용한다. 기존 잔여 5쌍 draft를 P0로 이어서 닫고, 아직 전수 리뷰되지 않은 spec lifecycle 7개를 P1/P2로 감사한다.

대상은 skill 14개와 agent 5개 component의 Claude/Codex 진입 표면 38개 및 finding으로 연결되는 reference다. 완료 상태는 각 component의 감사 disposition, review·검증 증거, spec 동기화, P0/P1/P2 Conventional Commit으로 판정한다.

## `/goal` 조건 문자열
> 아래 블록을 `/goal <조건>`에 그대로 넣는다. 평가자는 도구 없이 transcript만으로 판정하므로 자족적이어야 한다.

DONE WHEN:
1. 우선순위 inventory가 완결된다: P0는 sdd-autopilot, feature-draft, plan-review, implementation, implementation-review, spec-sync, pr-review와 simplicity/plan-review/implementation-review/spec-sync/pr-review agent 5개; P1은 spec-create, spec-review, spec-rewrite, spec-upgrade; P2는 spec-summary, spec-snapshot, guide-create다. discussion은 제외한다. 증명: `rg -n '^\| P[012] \|' _sdd/goal/2026-08-07_skill_authoring_norms_core_rollout/report.md` 출력이 정확히 19개 component 행이며 각 행에 AUDITED와 UPDATED 또는 NO_CHANGE, 근거 경로가 표시된다.
2. P0 12개 component는 기존 잔여 5쌍 draft를 이어 각 feature의 draft→plan-review→implementation→implementation-review→spec-sync 증거로 닫히고, P1/P2 7개 component도 SKILL_AUTHORING_NORMS 전수 감사 후 finding이 있는 표면과 딸린 reference/mirror가 수정된다. 증명: 최종 transcript에 feature별 AC ledger와 review 합산이 표시되고 `rg -n 'UNRESOLVED.*(Critical|High|Medium)' _sdd/goal/2026-08-07_skill_authoring_norms_core_rollout/report.md` 출력이 0건이다.
3. 모든 수정은 docs/SKILL_AUTHORING_NORMS.md의 단일 홈, 기준 중심 지시, progressive disclosure, rich reference, 인터페이스 계약 기준을 충족하며 관측 근거가 있는 hard gate와 Final Check는 보존된다. 증명: `rg -n 'NORM-(HOME|JUDGMENT|DISCLOSURE|REFERENCE|INTERFACE|HARD-GATE).*PASS' _sdd/goal/2026-08-07_skill_authoring_norms_core_rollout/report.md`가 6종 PASS를 보여준다.
4. Claude/Codex 3-way 의미 parity와 runtime-specific delta가 보존되고 agent TOML이 유효하다. 증명: mirror census 결과가 transcript에 PASS로 표시되고 `python3 -c 'import glob,tomllib; fs=glob.glob(".codex/agents/*.toml"); [tomllib.load(open(f,"rb")) for f in fs]; print("TOML_OK",len(fs))'`가 `TOML_OK 5`를 출력한다.
5. global spec·decision log·changelog·work log가 구현 증거와 동기화되고 P0/P1/P2가 각각 Conventional Commit으로 남는다. 증명: `rg -n 'Spec Version|규범.*P[012]' _sdd/spec/main.md _sdd/spec/decision_log.md _sdd/spec/logs/changelog.md _sdd/work_log/*.md`가 동일 최종 버전과 세 우선순위 기록을 보여주고, `git log --format='%s' 0f2d72e..HEAD | rg -c '^(refactor|docs)\(norms-p[012]\):'`가 `3`을 출력한다.
6. 최종 위생 검증이 통과하고 discussion 및 unrelated user changes는 보존된다. 증명: `git diff --check 0f2d72e..HEAD` 출력이 없고, `git diff --name-only 0f2d72e..HEAD -- .claude/skills/discussion .codex/skills/discussion` 출력이 없으며, 최종 transcript가 남은 worktree 항목을 goal-scoped/기존 사용자 변경으로 구분해 표시한다.
CONSTRAINTS: 현재 branch와 기존 커밋을 보존한다. discussion, goal-init, ralph-loop-init, investigate, write-phased, git, second-opinion은 수정하지 않는다. 새 동작을 발명하거나 관측 근거가 있는 hard gate를 약화하지 않는다. 같은 change element의 Claude/Codex/agent/reference 전파를 한 feature에서 닫는다. 리뷰는 각 producer의 단일 패스+fix 1회 계약을 따른다. destructive git, push, PR은 수행하지 않는다.
STOP: after 4 consecutive goal turns with no newly audited component, closed finding, committed priority, or new verification evidence.

## Loop Protocol
매 턴 다음을 수행한다 (이 섹션은 메인 에이전트용 HOW이며 조건 문자열에 넣지 않는다):
1. `experiments.md`의 pending 가설 하나를 골라 시도한다.
2. 해당 가설의 검증 명령을 실행하고 **출력을 대화에 그대로 표시**한다 (평가자가 transcript에서 본다).
3. 시도·검증 결과를 `journal.md`에 append한다.
4. pending 큐가 비었는데 목표 미완이면, 새 가설을 brainstorm해 `experiments.md` pending에 append한다.

## 실행법

### Claude Code
Claude Code 실행법은 Claude용 `goal-init`이 채운다.

### Codex
1. goals 기능 활성화: `codex features enable goals` (`features.goals`).
2. 라이프사이클: `set`(목표 설정)·`status`(진행 확인)·`clear`(종료) + 필요 시 `pause`·`resume`.
3. continuation은 thread-scoped이며 안전 경계 안에서만 이어간다 (evidence-based — 각 턴의 검증 출력을 근거로 진행).
