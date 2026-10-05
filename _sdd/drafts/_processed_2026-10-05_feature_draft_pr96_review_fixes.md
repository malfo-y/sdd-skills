# Feature Draft: PR96 리뷰 수정과 Codex 단계별 model·effort 지정

> 규모 판정: 적격 — 실행 계약·계측 코드·과거 측정 보고를 3개 owner task로 나누며, 동일 파일이나 변경 요소를 중복 배정하지 않는다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
PR96 리뷰의 확인 사항 회수 누락, digest 반환 계약 누락, M2 쓰기 오분류, Codex enum 전제를 수정하고 Codex worker의 단계별 model·effort 옵션을 독립적으로 지원한다.

- feature-draft 최초/fix 반환에 새 사용자 확인 사항이 있으면 해당 결정에 의존하는 구현 dispatch 전에 처리한다. 기존 승인·무인 위임·routine 선택은 다시 묻지 않고, 결정에 따른 draft 수정은 계획 worker가 맡는다.
- digest 허용 내용은 leaf와 메인이 읽는 공통 경계가 소유한다. 결정·제약/환경 함정/검증 레시피만 남기고 상태·통과 주장·다음 행동은 state로 분리한다.
- Codex의 `--model <stage>=<model>[,...]`와 `--effort <stage>=<effort>[,...]` 및 동등 자연어 지정은 독립적인 per-call 옵션이다. 단계별 지정과 fix 재dispatch·리뷰 3개 worker의 적용 범위를 유지하고, 활성 schema enum 또는 도구 설명의 지원 목록으로 모델·effort 조합을 검증한다. 미지정 필드는 생략하며 모델만 바꾸면 그 모델 기본 effort가 적용될 수 있다.
- M2는 benchmark 대상 worktree 기준으로 확정 쓰기와 미확정 쓰기를 구분한다. `/tmp` 내부 대상도 포함하고 대상 밖 scratch는 제외한다. 확정 쓰기 0건이어도 미확정이 남으면 무쓰기 PASS로 판정하지 않는다.

## Scope
- **In**: 양 runtime orchestrator SKILL·공통 reference·README, M2의 좁은 반례 수정과 unittest, 기존 transcript 재계측 및 기존 보고의 M2 판정 정정.
- **Out**: shell 전체 문법 지원, 새 설정 파일·고정 Codex 모델 목록, Claude effort 지원 추가, 새 gate/worker 종류, 모델 벤치마크 재실행, commit·push. global spec Planned/verified 반영은 spec-sync worker가 소유하며 아래 구현 Target Files에서 제외한다.
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: 확인 사항·digest·단계별 worker 옵션 계약을 고친다
worker 실행과 인계를 정의하는 동일 문서들을 한 owner가 수정해 중복 수정과 runtime 간 계약 차이를 막는다.

**Contracts**: Part 1의 실행 계약 3개가 이 task의 변경 요소다. 다섯 단계 이름은 기존 `단계와 진입` 표를 사용한다. `implementation-review` 옵션은 correctness 1개와 simplicity 2개, 총 3개 모두에 적용하고 각 단계 fix에도 유지한다. 명시 옵션의 필드 부재, 지원값 미확정, 잘못된 값/조합은 구분해 설명하되 기존 대화형 수정 요청·무인 실행 기본값 fallback 정책을 유지한다. 허용 내용의 canonical은 `worker-boundary.md`, runtime별 호출 매핑은 각 SKILL의 Runtime 절이다.

**Acceptance Criteria**:
- [ ] AC1: reviewer가 최초 draft·fix draft 각각에 대해 ① 미승인 새 구조 결정은 의존 구현 전에 확인 대기 ② 기존 승인/routine 선택은 질문 없이 진행 ③ 무인 위임은 합당한 결정 기록 후 진행의 흐름을 추적해 세 경우 모두 PASS로 판정한다. 근거는 수정된 절 인용이며, digest 반영·계획 worker의 draft 갱신 책임과 일반적인 “게이트 반환은 대기 지점 아님” 규칙의 관계가 명시되어야 한다.
- [ ] AC2: reviewer가 `worker-boundary.md`의 단일 내용 계약, SKILL의 참조·반환 분리 처리, handoff template의 소유권 포인터를 대조한다. “계측 명령과 기대값”은 digest 허용, “완료/통과/다음 조치”는 state, 허용 변경분이 없으면 `없음`인 사례가 모두 문면으로 판정 가능해야 한다. 같은 긴 계약을 각 worker 파일에 복제하지 않는다.
- [ ] AC3: reviewer가 옵션 생략/model만/effort만/둘 다의 호출 인자와 다섯 단계·fix 적용을 문면으로 확인한다. Codex는 지정된 필드만 `model`·`reasoning_effort`에 매핑하며, 선택 모델별 effort 지원 차이도 검증한다. enum 없음+도구 설명 목록 있음은 정상 검증, 둘 다 없음은 미확정, 필드 없음은 미지원으로 구분되고 고정 allowlist가 없어야 한다. 모델만 지정했을 때 부모 effort 상속을 보장하는 문장이 없어야 한다. 근거는 SKILL·README 인용 및 활성 도구 설명과의 대조다.
- [ ] AC4: `/usr/bin/diff -r .claude/skills/sdd-orchestrator/references plugins/sdd-skills-codex/skills/sdd-orchestrator/references`가 무출력 exit 0이다. 두 SKILL의 Runtime 절만 제거한 본문 비교도 동일하고, README에는 Codex 단계별 model·effort 조합 예시와 미지정 동작이 있다. Claude runtime에 새 effort 지원을 주장하지 않는다. 이 검증은 정적 계약 검증이며 실제 옵션 dispatch 실행 완료로 보고하지 않는다.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- 공통 실행·옵션·digest 계약과 Runtime 경계를 유지
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- 공통 계약 미러와 Codex 옵션 검증·매핑
- [M] `.claude/skills/sdd-orchestrator/references/worker-boundary.md` -- leaf와 메인이 공유하는 digest 내용 계약
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/worker-boundary.md` -- 동일 계약 미러
- [M] `.claude/skills/sdd-orchestrator/references/handoff-templates.md` -- digest 내용 소유권 참조를 공통 경계로 변경
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/handoff-templates.md` -- 동일 포인터 미러
- [M] `README.md` -- 단계별 Codex model·effort 사용법과 기본값 설명

### Task 2: M2를 대상 worktree 기준으로 보정하고 반례 unittest를 둔다
관측된 Bash/Python 쓰기 누락과 cp 원본 오탐을 고치되 지원하지 않는 명령을 성공으로 추측하지 않는다.

**Contracts**: `bench/run.sh`의 기존 `WT=$B/t-$RUN` 규약으로 `measure`가 대상 경로를 전달한다. 경로 판별은 worktree 존재 여부에 의존하지 않고 `/tmp`와 `/private/tmp` alias를 정규화한다. 대상 내부의 기존 허용 handoff/log 경로는 유지하되 basename 부분 일치로 임의의 대상 파일을 면제하지 않는다. 지원되는 쓰기 표적은 확정 쓰기/대상 밖 또는 허용 쓰기/미확정으로 구별하며 복합 명령에 미확정 동작이 남으면 별도 표시한다. 기존 `M2_main_edits`는 확정 쓰기 수로 유지하고 `M2_unknown` 수 및 그 명령 근거를 출력한다. M2 판정은 확정 쓰기 > 0이면 FAIL, 0이고 unknown > 0이면 UNVERIFIED, 둘 다 0일 때만 PASS다.

**Acceptance Criteria**:
- [ ] AC1: 새 `unittest`를 먼저 작성해 baseline에서 아래 반례의 RED를 확인한 뒤 동일 명령 `python3 -m unittest discover -s tools/tests -p 'test_orchestrator_metrics.py' -v`가 모두 GREEN이다. 기준 root `/tmp/bench/t-87-new-1`에서 일반/quoted redirect, heredoc 선언 뒤 redirect, 대상 절대경로 redirect, Python literal `open(..., 'w')`는 쓰기다. `cp notes.md /tmp/scratch.md`, 외부 scratch redirect, `git diff -- notes.md`는 대상 쓰기가 아니다. `/private/tmp` alias, 대상 안/밖 직접 Write, 기존 허용 handoff 쓰기도 경계 사례로 포함한다.
- [ ] AC2: 같은 unittest에서 해석할 수 없는 script 호출·동적 경로는 unknown이고, 알려진 쓰기와 unknown을 섞은 명령은 unknown 근거도 잃지 않는다. 합성 transcript를 통한 `measure` 검증에서 확정 0+unknown 1은 UNVERIFIED, 확정 0+unknown 0은 PASS, 확정 1은 FAIL이며 M2 외 지표 계산은 기존 의미를 유지한다. 테스트는 실제 함수/집계 결과를 검증하고 prompt 문구 존재 검사는 만들지 않는다.
- [ ] AC3: reviewer가 diff와 `goal.md` R4의 M2 레시피를 대조해 대상 root 전달, cp 목적지 구분, unknown 보존과 합격 조건을 확인한다. 작은 lexical/표적 추출 수정으로 닫고, 중첩 shell·임의 Python 실행·변수 흐름의 일반 해석은 구현하지 않는다. 해석 불가 문법을 unknown으로 남기는 제한을 레시피에 명시한다.

**Target Files**:
- [M] `_sdd/goal/2026-10-04_orchestrator_harness_redesign/bench/metrics.py` -- root 기준 분류와 미확정 집계
- [C] `tools/tests/test_orchestrator_metrics.py` -- 기존 테스트는 uninstall 기능 전용이므로 독립 metrics 함수·집계 회귀용 표준 라이브러리 unittest 파일 생성
- [M] `_sdd/goal/2026-10-04_orchestrator_harness_redesign/goal.md` -- M2 대상/외부 scratch 구분과 unknown 판정 레시피 정정; 과거 목표의 실행 재개나 범위 확장 아님

### Task 3: 기존 transcript로 M2 보고를 정정한다
Task 2의 확정된 계측을 과거 보고에 적용해 M2=0의 증거 공백을 닫거나 미확정으로 명시한다.

**Contracts**: Task 2의 계측 출력과 판정 규칙을 소비한다. 기존 보고의 16개 run(old 1·2, new 1~6, 각각 87·88)만 다시 계측하고, v3 성능과 현재 head 검증을 구분한다. 원문 transcript의 수작업 전체 탐색이나 새 모델 실행은 하지 않는다.

**Acceptance Criteria**:
- [ ] AC1: `python3 _sdd/goal/2026-10-04_orchestrator_harness_redesign/bench/metrics.py <BENCH_DIR> 87-old-1 87-old-2 88-old-1 88-old-2 87-new-1 87-new-2 88-new-1 88-new-2 87-new-3 87-new-4 88-new-3 88-new-4 87-new-5 87-new-6 88-new-5 88-new-6`를 30초 한도 내 실행한다. 16개 run의 확정 쓰기·unknown·판정 결과를 report에 남기고 실행 명령/입력 포인터를 함께 기록한다. 입력 누락·timeout이면 해당 run을 UNVERIFIED와 사유로 남기며 같은 명령을 무조건 반복하지 않는다.
- [ ] AC2: reviewer가 결과와 report의 측정 표·M2 설명·v3 판정·상단 Status를 대조해 모순이 없음을 확인한다. unknown이 있는 run을 “메인 대상 쓰기 없음 PASS”로 쓰지 않으며, 과거 다른 지표의 유효한 증거는 유지하고 현재 head 성능 증거로 승격하지 않는다. `git diff --check`가 무출력 exit 0이다.

**Target Files**:
- [M] `_sdd/goal/2026-10-04_orchestrator_harness_redesign/report.md` -- 재계측된 M2와 증거 한계 반영

# Open Questions
- 사용자 확인 필요: 없음. Codex effort는 독립 옵션이며 모델별 조합 검증을 사용한다. 옵션 미확정/미지원의 처리 방식은 기존 대화형·무인 실행 정책을 따른다.
- 재계측 입력은 `<BENCH_DIR>=/tmp/claude-501/-Users-hyunjoonlee-github-sdd-skills/18bd1d97-361d-4d25-9233-2699074f6e25/scratchpad/bench`, 인덱스 `logs/runs.tsv`, transcript `~/.claude/projects/*/<sid>.jsonl`이다. 해당 16개 sid의 파일 존재만 확인했고 원문은 읽지 않았다. 기존 대상 worktree는 삭제되어 있으므로 경로 분류에 존재 검사를 요구하지 않는다.
