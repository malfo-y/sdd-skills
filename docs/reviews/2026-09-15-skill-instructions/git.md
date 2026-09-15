# git 지시 리뷰

- 날짜: 2026-09-15 KST
- 모델: gpt-6-astra
- 기준 커밋: be6c5a1f014b3e37d386127966b0bb6de3549587
- 상태: 정적 리뷰 완료 / 제안 미적용 / 동작 미검증
- 대상: [Claude](../../../.claude/skills/git/SKILL.md). Codex 대응 스킬 없음은 배포 범위이며 결함이 아니다.
- 판정 요약: 수정 필요 5 / 정리 후보 2 / 실행 검증 필요 0

## 역할과 유지할 계약

요청한 Git 작업의 상태를 조사하고, 필요할 때 변경을 의미 단위로 묶어 계획을 보여준 뒤 실행 결과를 보고한다. Conventional Commits, 실행 전 구체적인 계획 표시, 기존 변경 보존, protected branch 보호, force-push·history rewrite 등 위험 행동의 승인 경계를 유지한다. 사용자 또는 goal의 사전 승인은 해당 행동과 범위에서만 인정한다.

## 기준별 판정

| 기준 | 판정 |
|---|---|
| 1. 적용 조건 | git-01: 모드별 수행 범위와 무조건 AC·clean-tree 종료 규칙이 충돌한다. git-06: 진행 중 작업 탐지가 `.git` 디렉터리를 전제한다. |
| 2. 충돌과 우선순위 | git-02: 행동별 위임과 goal 예외 조건 불일치. git-05: 절대 금지와 승인 필요조건은 양립하지만 목록 표현을 명료화할 수 있다. |
| 3. 확인·승인 경계 | git-02: 이미 승인된 비파괴적 행동의 재확인을 줄일 수 있다. 위험 작업에 대한 별도 승인·항상 확인 제외는 유지한다. |
| 4. 중복과 소유권 | git-07: 충돌 해결 규칙이 본문과 safety reference 양쪽에 반복되어 있다. |
| 5. 완료·복구 조건 | git-01·03·04·06: 요청 모드 종료, 기존 index 보존, dirty 상태의 rebase 순서, 진행 중 작업 탐지에 구체적인 누락이 있다. |
| 6. 절차의 필요성 | git-01: status·push 전용 요청에도 semantic grouping·CONFIRM 완료를 요구하는 AC를 좁혀야 한다. 전체 workflow 자체나 계획 표시를 삭제할 필요는 없다. |

## Findings

### git-01 — 모드별 실행 범위와 공통 완료 조건·조기 종료 충돌 [수정 필요]

- **기준 / runtime**: 1, 5, 6 / Claude.
- **근거**: [SKILL.md](../../../.claude/skills/git/SKILL.md) 12–15·183·195–204행.
  - AC2: “변경사항을 의미 단위로 semantic grouping 하고”
  - AC3: “커밋 그룹, diff 요약, 브랜치/push 계획을 사용자에게 보여주고 승인”
  - 183행: “Empty working tree” → “`✅ Working tree clean` 표시, 종료”
  - 195행: “`/git`, `/git status`” → “Phase 1 only (dashboard)”
  - 197행: “Check sync + push”; 204행: “Acceptance Criteria가 모두 만족되었나 검증한다.”
- **문제 상황**: `/git status`는 Phase 1에서 끝나야 하지만 공통 AC2·AC3는 계획·승인 단계로 복귀시킨다. 변경 파일은 없고 로컬 commit만 ahead인 `/git push`, 또는 clean 상태의 `/git cleanup`은 183행을 적용하면 필요한 push/rebase 전에 종료한다. [status 예시](../../../.claude/skills/git/examples/sample-status-session.md) 25행도 Phase 1 종료를 명시하고, [cleanup 예시](../../../.claude/skills/git/examples/sample-branch-cleanup-session.md) 19–22·33–39행은 clean 상태에서 rebase·push한다.
- **예상 영향**: 읽기 요청이 불필요한 계획·승인으로 확장되거나, 이미 존재하는 commit의 전송·정리가 누락될 수 있다.
- **최소 수정안**: 진입 시 shorthand mode가 해당 단계와 AC 적용 범위를 결정한다고 명시한다. AC2는 commit 생성 모드, AC3·AC4는 실제 실행 대상 mutation에만 적용한다. clean working tree는 상태 사실로 보고하고, 요청 작업에 필요한 ahead/behind·graph·branch 작업도 없을 때만 종료한다.
- **유지할 계약**: AC 자체 검증, mutation 계획 표시와 필요한 승인, status 읽기 전용, 요청한 push·cleanup 완료.
- **소유자**: `git` 본문. 예시는 수정된 모드 계약을 소비한다.
- **검증 상태**: 정적 충돌 확인. 실제 Git 명령·스킬 미실행.

### git-02 — 승인을 행동별로 판정하지 않고 goal의 commit·push 쌍만 예외로 인정 [수정 필요]

- **기준 / runtime**: 2, 3 / Claude.
- **근거**: [SKILL.md](../../../.claude/skills/git/SKILL.md) 27·107–113행.
  - “Get confirmation unless the Phase 3 goal-delegation exception applies.”
  - “아래 두 조건이 모두 참일 때만 적용한다.”
  - “사전 승인 목록에 commit·push가 있다.”
  - 연결 계약: [goal-init harness template](../../../.claude/skills/goal-init/references/harness-templates.md) 35행은 “사전 승인 목록에 있는 행동에 한해” 확인이 충족된다고 규정하고, 39행은 범위 밖 행동 없이 가능한 진척을 먼저 하도록 한다.
- **문제 상황**: 사용자가 goal에서 commit만 승인하고 push는 제외했는데 이번 작업이 commit뿐인 경우, `commit·push`가 모두 있는 예외 조건은 충족되지 않는다. 일반 세션에서도 사용자가 대상과 비파괴적 작업을 명확히 승인했는데 goal 하네스가 없다는 이유만으로 다시 승인받게 된다. 어느 경우든 승인된 행동의 범위를 개별적으로 판정할 수 있다.
- **예상 영향**: commit-only 위임이 멈추거나, 기존 승인이 있는데도 같은 결정을 재질문할 수 있다. commit 승인에서 push·rebase까지 추론하는 반대 방향의 확장도 막아야 한다.
- **최소 수정안**: 계획 표시는 유지하고, 각 예정 행동에 대해 현재 대화의 명시적 승인 또는 goal의 해당 행동 위임을 확인한다. 승인된 범위만 실행하고, 범위 밖 작업은 제외하거나 실제로 필요한 경우에만 질문한다. goal 예외를 commit과 push의 동시 승인 조건으로 묶지 않는다.
- **유지할 계약**: protected branch·force-push·history rewrite·파괴적 작업의 별도 승인, goal의 “항상 확인” 목록, 계획과 실제 작업 범위 일치. 모든 Git 행동의 무조건 자동 승인은 제안하지 않는다.
- **소유자**: `git` Phase 3. `goal-init`은 행동별 durable authorization의 연결 소유자이며 해당 template 자체의 변경은 불필요하다.
- **검증 상태**: 정적 계약 대조 완료. 일반 세션의 기존 승인 인정은 사용자 승인 우선순위에 맞춘 수정이며, global spec의 goal 위임 계약을 약화하지 않는다.

### git-03 — 기존 index를 보존·분리하지 않는 그룹별 commit 순서 [수정 필요]

- **기준 / runtime**: 5 / Claude.
- **근거**: [SKILL.md](../../../.claude/skills/git/SKILL.md) 69·139–152행.
  - “각 커밋 그룹별: a. git add <files> b. git commit -m”
  - [semantic-grouping.md](../../../.claude/skills/git/references/semantic-grouping.md) 51행: “하나의 커밋에 관련 없는 변경사항을 섞지 않는다”.
- **문제 상황**: index에 A·B 두 기능 변경이 이미 staged되어 있고 계획은 A, B를 별도 commit으로 나눈다. 제시된 순서대로 A에 `git add`를 추가한 뒤 commit하면 index에 남은 B까지 첫 commit에 포함된다. 본문의 “관련 없는 변경 stash”만으로는 두 승인된 그룹 사이의 index 분리를 보장하지 못한다.
- **예상 영향**: 승인된 semantic grouping과 실제 commit 내용이 어긋나며, 두 번째 그룹이 빈 commit 대상이 될 수 있다.
- **최소 수정안**: 시작 시 staged/unstaged 상태를 보존하고, 각 commit 전에 index가 승인된 현재 그룹의 파일·hunk만 포함하는지 확인하도록 한다. 그룹 분리 과정이 기존 사용자 staging을 바꾸면 안전하게 기록·복원한다. 전체 변경을 버리는 reset은 해결책으로 넣지 않는다.
- **유지할 계약**: 의미 단위 commit, partial staging 지원, 기존 변경 보존, 승인된 내용만 commit.
- **소유자**: `git` EXECUTE. grouping reference에 실행 절차를 복제하지 않는다.
- **검증 상태**: 명령 순서와 index 전제의 정적 검토. 임시 repo 재현은 수행하지 않았다.

### git-04 — 커밋할 변경을 남겨 둔 채 rebase를 먼저 실행 [수정 필요]

- **기준 / runtime**: 5 / Claude.
- **근거**: [SKILL.md](../../../.claude/skills/git/SKILL.md) 96–98·142–147행.
  - Behind, with local commits → “`git pull --rebase`”
  - “1. 관련 없는 변경 stash (필요시)” → “2. Graph cleanup (pull/rebase)” → “4. 각 커밋 그룹별”.
- **문제 상황**: remote보다 뒤처진 feature branch에 이번 commit 대상인 tracked 수정이 있다. unrelated 변경만 stash하면 이번 변경은 dirty 상태로 남는데, workflow는 이를 commit하기 전에 rebase하도록 한다. autostash 설정이나 별도 보존 단계는 계약에 없다.
- **예상 영향**: 선택된 정상 workflow가 dirty 상태에서 rebase 단계에 막히고, 이후 복구·재개 순서는 정해져 있지 않다.
- **최소 수정안**: rebase의 작업트리·index 전제조건을 확인하고, 충족하지 않으면 승인된 변경을 먼저 commit하거나 필요한 전체 미커밋 변경을 안전하게 보존·복원하는 순서를 계획에 포함한다. 기존 stash와 이번 작업의 보존 대상을 구분하고, 실패 시 후속 push를 실행하지 않는다.
- **유지할 계약**: 변경 보존, 승인된 rebase만 실행, unrelated 변경을 commit에 섞지 않기, stash 복원.
- **소유자**: `git` PLAN/EXECUTE와 safety reference의 stash 경계.
- **검증 상태**: 정적 전제조건 누락 확인. 특정 repo의 Git 설정이나 실행 실패를 관측했다고 주장하지 않는다.

### git-05 — `--force` 금지와 승인 필요조건 목록의 관계 명료화 [정리 후보]

- **기준 / runtime**: 2, 3 / Claude.
- **근거**: [safety-rules.md](../../../.claude/skills/git/references/safety-rules.md) 14·20–25행.
  - 14행: “`--force-with-lease`만 사용 (절대 `--force` 사용 금지)”
  - 20–25행: “다음 명령은 사용자 확인 없이 실행하지 않는다” 목록에 “`git push --force`”.
- **문제 상황**: `--force`는 절대 금지이면서 사용자 확인 없이 실행하지 않는 명령 목록에도 들어 있다. 후자는 확인을 필요조건으로 둘 뿐, 확인받으면 허용한다는 충분조건은 아니므로 두 규칙은 논리적으로 양립한다. 다만 금지 명령과 승인 후 검토 가능한 명령을 같은 목록으로 읽을 여지가 있어 문구 정리를 제안한다.
- **예상 영향**: 독자가 승인 목록을 허용 목록으로 오독할 여지를 줄일 수 있다. 현재 계약 충돌이나 실제 잘못된 force-push 실행은 확인하지 않았다.
- **최소 수정안**: 파괴적 작업 목록에서 해당 항목을 “force-push는 위 Force Push 규칙을 따른다”로 참조하거나, 승인 대상 명령을 허용된 `--force-with-lease`로 명시한다. protected branch 금지와 사용자 확인 필수는 그대로 둔다.
- **유지할 계약**: `--force` 금지, feature/fix branch rebase 이후의 `--force-with-lease` 한정, 사용자 확인.
- **소유자**: `git/references/safety-rules.md`.
- **검증 상태**: 동일 reference의 원문 대조 완료. 규칙은 양립하며, 동등한 정책을 더 명료하게 표현하는 정리 후보다. force push는 실행하지 않았다.

### git-06 — 진행 중 작업 탐지가 `.git` 디렉터리 고정 경로에 의존 [수정 필요]

- **기준 / runtime**: 1, 5 / Claude.
- **근거**: [SKILL.md](../../../.claude/skills/git/SKILL.md) 42–47행.
  - “`test -d .git/rebase-merge || test -d .git/rebase-apply`”
  - “`test -f .git/MERGE_HEAD`”
  - 수집해야 할 정보는 “in_progress 여부”.
- **문제 상황**: `.git`이 실제 디렉터리 대신 gitdir pointer 파일인 linked worktree에서 작업 중인 경우, 이 경로 검사는 실제 per-worktree Git 상태 디렉터리를 검사하지 않는다. 저장소 하위 디렉터리에서 호출해도 현재 위치의 `.git` 고정 경로는 맞지 않을 수 있다.
- **예상 영향**: 진행 중인 rebase/merge를 놓친 상태에서 새 workflow를 계획할 수 있다. 현재 workspace가 해당 상태라고 주장하지 않는다.
- **최소 수정안**: Git이 해석하는 경로를 조회해 진행 중 상태 파일을 확인한다(예: `git rev-parse --git-path <state-path>`). 진행 중이면 새 cleanup을 시작하지 않고 기존 작업을 다룬다는 분기를 명시한다.
- **유지할 계약**: AC1의 상태 파악, 기존 작업 보존, rebase/merge 중복 시작 방지.
- **소유자**: `git` ASSESS.
- **검증 상태**: 고정 경로의 적용 범위에 대한 정적 확인. linked worktree나 merge/rebase를 만들지 않았다.

### git-07 — 충돌 해결 규칙을 safety reference 한곳으로 모으기 [정리 후보]

- **기준 / runtime**: 4 / Claude.
- **근거**: [SKILL.md](../../../.claude/skills/git/SKILL.md) 154–158행과 [safety-rules.md](../../../.claude/skills/git/references/safety-rules.md) 27–33행.
  - 양쪽 모두 충돌 목록 확인, 한쪽만 의미 있는 변경 선택, 다른 섹션 병합, 같은 줄 사용자 확인을 반복한다.
- **문제 상황**: 향후 동일 줄 충돌의 처리 기준이나 승인 정책을 한쪽에서만 바꾸면 본문과 reference가 다른 행동을 요구하게 된다. 현재는 의미가 같으므로 실행 결함은 아니다.
- **예상 영향**: 유지보수 시 두 위치를 맞춰야 한다. 측정하지 않은 비용 절감은 주장하지 않는다.
- **최소 수정안**: safety reference가 충돌 해결 정책을 소유하고, 본문은 해당 절 참조와 실행 흐름 복귀 지점만 남긴다. 예시와 실제 규칙의 소유권도 이곳으로 고정한다.
- **유지할 계약**: 충돌 확인, 안전한 자동 병합 범위, 의미가 결정되지 않은 충돌에 대한 필요한 사용자 판단.
- **소유자**: `git` 본문·`references/safety-rules.md`.
- **검증 상태**: 동등 문면 대조 완료. 정리 후보이며 현재 동작 실패는 미관측.

## 런타임 차이와 의존성

- Claude 전용 스킬이다. Codex mirror나 adapter 신설을 요구하지 않는다.
- 직접 reference 세 개(`safety-rules.md`, `semantic-grouping.md`, `conventional-commits.md`)를 모두 읽었다. 예시 세 개도 모드·상태·실행 순서 대조에 사용했다. Conventional Commits의 형식은 이번 검토에서 수정 필요를 찾지 못했다.
- `goal-init` 본문의 durable authorization 관련 구간과 `references/harness-templates.md` 34–46행을 읽어 사전 승인·항상 확인·범위 밖 처리 계약을 대조했다. cross-skill 변경의 주 소유자는 git이며 goal template은 행동별 판정 근거다.
- 공통 기준으로 `AGENTS.md`, `_sdd/env.md`, `_sdd/spec/main.md`의 관련 승인·goal 위임·자체 AC·evidence 계약을 적용했다.
- 미검토: Git 설치 버전·repo별 설정·remote 권한·보호 규칙·hook 실제 실행. 이 보고서는 대상 Git 명령이나 스킬을 실행한 결과가 아니다.

## 권장 처리 순서와 검증

1. git-01·02로 요청 모드와 승인 범위를 먼저 닫는다. status-only, clean-but-ahead push, clean-diverged cleanup, commit-only 위임, 명시적으로 제외된 push, 항상 확인인 history rewrite를 각각 대조한다.
2. git-03·04·06은 별도 임시 repo에서 실행 검증한다. 두 그룹 pre-staged 상태의 commit 내용, dirty branch의 승인된 rebase 경로, linked worktree의 진행 중 상태 탐지를 확인하고 작업 전후 파일·index·stash 보존을 비교한다. 이 검증은 현재 리뷰에서는 하지 않았다.
3. git-05의 금지/승인 문구를 단일 정책으로 정리하고 git-07 중복을 접는다. static diff 및 링크 확인 후 `git diff --check`로 문서 위생을 검증한다. 위험 작업을 실제 remote에 실행할 필요는 없다.

강제 AC와 필요한 승인 경계는 보존한다. 제안은 미적용이며 모든 실행 시나리오는 후속 검증 항목이다.
