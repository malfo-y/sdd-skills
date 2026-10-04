# Journal (append-only)

## 2026-10-04 21:00–21:40 — 루프 1턴: F1 착수, H1·H2 통과, Feature A 구현 중
- 브랜치 `refactor/orchestrator-harness` 생성, setup 파일 커밋 64b8641.
- R3 plugin 경로 확정: `claude plugin validate /Users/hyunjoonlee/github/sdd_skills` → `Validation passed`(repo 루트 marketplace manifest).
- H1 PASS: `--plugin-dir <repo 루트 worktree>`가 설치된 sdd-skills 플러그인을 이름으로 덮어쓴다(마커 플러그인 시험: `sdd-skills:zz-marker`만 보이고 설치본 skill 없음). 대상 worktree의 bare 프로젝트 스킬은 `--disallowedTools 'Skill(<이름>),...'`로 막힌다("Skill execution blocked by permission rules"), prefixed는 실행됨.
- H2 PASS: `claude -p`에서 Agent는 `requestShape: foreground`(subagent meta.json)로 실행되고 메인이 결과(`ORCH_GOT=WORKER_DONE_42`)를 받은 뒤 진행한다.
- R4 실행 방식 확정: `bench/run.sh <87|88> <old|new> <rep> <harness>` — base worktree + draft 복사 + `claude -p --model claude-opus-5-5 --plugin-dir <harness> --disallowedTools <bare 스킬 전부> --session-id <uuid> --dangerously-skip-permissions --output-format json`, 이어서 `bench/review.sh`(하네스 없이 `--disable-slash-commands --json-schema`로 독립 리뷰). 계측 `bench/metrics.py`. 구 = `bench/src-old`(main bee82a5 worktree).
- 구 경로 기준선 4회 시작(2 stream 병렬). 87-old-1 528s, 88-old-1 639s 완료.
- Feature A draft `_sdd/drafts/2026-10-04_feature_draft_orchestrator_harness.md`(분할 필요 — Feature A/B 롤링) → plan-review gate 1 (opus-5.5): H2 M4 → fix 1 전부 반영, gate 2 미달.
- implementation 진행: T1~T5·T7 structural 42/42 PASS. T6 smoke GREEN 1차 FAIL: 오케스트레이터가 worker 대신 동명 구 스킬 `sdd-skills:implementation`을 호출하고 메인 루프가 `printf >> notes.md`로 직접 수정 → SKILL.md에 `## 실행 흐름`(번호 절차 + 동명 구 스킬 호출 금지) 추가, smoke 재실행 중.
- 검증 레시피 변경(강화): R4 M2가 Edit·Write에 더해 파일 쓰기 Bash 명령도 센다(`metrics.py` `bash_writes`, 단위 시험 9/9). 사유: 위 smoke에서 Bash 쓰기가 Edit·Write 계수에 안 잡힘. 제외 경로에 `_sdd/implementation/`·`_sdd/work_log/` 명시는 원문 "대상 파일" 한정의 풀어쓰기(동등).
- 다음: smoke GREEN 확인 → implementation-review 게이트 → spec-sync → 신 경로 실측(F5).

## 2026-10-04 21:40–21:55 — Feature A 마감, F5 실측 시작
- H1 정정: `--plugin-dir <marketplace 루트>`는 설치된 sdd-skills(캐시 bee82a5)를 덮어쓰지 못한다(신 skill 미로드, base dir = 캐시). plugin.json + skills symlink 래퍼(`bench/mkplug.sh`)여야 로드된다(base dir = 래퍼 경로 확인). 구 경로 run 4회는 캐시 bee82a5 = main 하네스로 실행됐으므로 기준선 유효.
- bench 결함 2건 수정: `run.sh` pathspec `:!_sdd…` → git이 magic으로 오해석해 patch·리뷰 누락 → `post.sh`로 분리(`:(exclude)`), 이미 끝난 run은 post.sh로 재처리. spec-sync가 draft를 `_processed_`로 rename → review/post의 draft glob을 `*2026-08-26_feature_draft_*`로.
- Feature A 마감: implementation-review gate 1(H1 M7)→fix 1, gate 2(M4)→fix 2. 커밋 5853990. spec-sync v4.33.0 커밋 d4eb1a1(실험 경로 + Feature B 🚧 Planned; changelog에 v4.31·v4.32 항목이 원래 없는 기존 공백 발견 — 미수정).
- 구 기준선(4/4 실행 완료): 87-old 528s/543s, M1 154k/139k, 토큰 5.63M/5.11M, 독립 리뷰 AC 9/9·C/H 0 ×2. 88-old 639s/738s, M1 166k/188k, 토큰 6.37M/7.39M, 독립 리뷰 88-old-1 AC 15/15·C/H 0(88-old-2 진행 중).
- F5 시작: 스냅샷 `bench/src-new`(5853990) + `bench/plug-new` 래퍼로 87-new·88-new 각 2회(2 stream) + smoke 재확인.
- 다음: F5 지표 판정 → 합격이면 Feature B draft(census는 Explore agent 진행 중).

## 2026-10-04 21:55–22:20 — F5 1회차(v1) 판정, Feature A2(맥락 다이어트), Feature B draft
- v1(5853990) 신 경로: 87-new-1 700s·M1 77.3k(합격선 73k FAIL)·M2 0·M3 7.7s·토큰 6.47M·독립 리뷰 AC 9/9 C/H 0(Medium: draft rename 누락). 88-new-1 1185s·M1 91.9k(합격선 88.5k FAIL)·M2 0·M3 7.8s·토큰 10.79M·리뷰 AC 9/9 C/H 0. smoke 최종(v1): worker 4·M2 0·M3 10.1s(동시 5세션 부하).
- M1 원인 분해(transcript): 메인 루프가 worker 계약을 직접 읽음(87: 약 11.7k자, 88: cat/sed), 환경 탐색, worker 반환 평균 약 3k자(88: 12건 35.9k자), digest·state heredoc 통째 재작성(88: Bash 입력 18.5k자). worker 시작은 계약→digest→draft를 턴마다 따로 읽음.
- Feature A2 `_sdd/drafts/2026-10-04_feature_draft_orchestrator_context_diet.md`: plan gate M1→fix, implementation gate 1 correctness M1 L1 · simplicity M2 L2 → 전부 반영(gate 2 미달). 커밋 b83fbcd. spec 수준 계약 변화 없음 → spec-sync 생략.
- v2(b83fbcd, `bench/plug-new2`) 재실측 시작: 87-new-3·4, 88-new-3·4. v1의 87-new-2·88-new-2는 참고용으로 계속 실행.
- Feature B draft `_sdd/drafts/2026-10-04_feature_draft_orchestrator_default_switch.md`(task 9개, census 리터럴 14개 — 모두 docs/reviews 0건 확인) → plan gate (opus-5.5) M4 L2 → fix. 구현은 v2 합격 후.
- 결정: Feature B 구현은 신 경로(`sdd-orchestrator`, 작업 트리의 project skill)로 dogfood한다 — 합격한 기본 경로이고 메인 맥락을 보호하며, 추가 실사용 증거가 된다. Loop Protocol 3단계의 `implementation`은 오케스트레이터의 implementation 단계로 해석.

## 2026-10-04 22:20–22:52 — F5 2회차(v2) 판정, Feature A3, v3 시작
- v2(b83fbcd): 87-new-3 597s·M1 62.1k·M2 0·M3 5.7s·토큰 4.84M·리뷰 AC 10/10 C/H 0 / 87-new-4 574s·M1 59.0k·M2 0·M3 1.6s·4.81M·AC 9/9 C/H 0 → 87 합격. 88-new-3 1011s·M1 87.9k(합격선 88.5k PASS)·M2 0·M3 6.65s·8.65M·AC 14/14 C/H 0 / 88-new-4 1158s·M1 95.6k(FAIL)·M2 0·M3 6.1s·9.46M(worker 13, fix 3) → 88 1:1.
- v1 참고: 87-new-2 912s·M1 92.9k·M2 0, 88-new-2 1197s·M1 97.8k. 88-new-2의 M2 2건은 대상 파일이 아니라 auto-memory 쓰기(`~/.claude/projects/-Users-hyunjoonlee-github-sdd-skills/memory/bash-grep-ugrep-gitignore.md` + MEMORY.md 1줄) — 벤치마크 세션이 git worktree라 사용자 프로젝트 메모리에 썼다. 내용은 사실(grep = ugrep 셸 함수)이라 보존, 최종 보고에 부작용으로 알림.
- 계측기 보정(동등 — 레시피 정의 불변, 탐지 구현만): python 쓰기 대상은 `open(<expr>,'w'|'a')`의 <expr>을 문장 단위 변수 할당까지 따라가 판정, 상대 경로 `work_log/<date>.md`·`implementation/<date>_` 제외 인식. 단위 시험 8/8, 전 run 재계측: 신 경로 9회 M2 0, 구 경로 5~15(판별력).
- 88 M1 원인(v2 88-new-3 분해): worker를 `run_in_background: true`로 띄워 dispatch마다 안내문 약 1.2k자 + 알림 포장(12회 약 18k자), dispatch prompt마다 공통 경계 약 550자 반복(약 6.6k자).
- Feature A3 `_sdd/drafts/2026-10-04_feature_draft_orchestrator_dispatch_diet.md`: 공통 경계 → `references/worker-boundary.md`, Claude worker foreground(schema에 있으면 `run_in_background: false`). plan gate M1→fix, implementation gate 1 correctness M1 · simplicity M2 → fix(gate 2 미달). 커밋 65a5bc4(Feature B draft·bench 보정 포함).
- v3(65a5bc4, `bench/plug-new3`) 실측 시작: 87-new-5·6, 88-new-5·6. v3가 최종 하네스 판정 대상(v1·v2는 참고).

## 2026-10-04 22:52–23:37 — F5 3회차(v3) 판정: R4 PASS
- v3(65a5bc4): 87-new-5 637s·M1 53.6k·M2 0·M3 6.3s·3.88M·AC 9/9 C/H 0 / 87-new-6 656s·53.3k·0·6.5s·4.27M·9/9 C/H 0 / 88-new-5 1039s·66.0k·0·1.65s·7.10M·14/14 C/H 0 / 88-new-6 1220s·80.3k·0·5.1s·7.06M·15/15 C/H 0. worker 전부 `requestShape: foreground`.
- 판정(경로 중앙값): M1 0.37(87 0.37·88 0.41) PASS, M2 0 PASS, M3 5.1s(36 worker) PASS, M4 PASS. M5 토큰 0.94배, 벽시계 1.43배(보고).
- 다음: Feature B를 신 경로(`sdd-orchestrator`)로 실행 → spec-sync 단계 포함 → R1·R2·R3·R5 검증 → PR.

## 2026-10-04 23:37 – 10-05 00:40 — Feature B(신 경로 dogfood), spec-sync, PR
- Feature B를 `sdd-orchestrator`(작업 트리 project skill)로 실행: task 9개(1차 6 동시 → 2차 2 → census), 구현 게이트 gate 1 C0/H0/M2/L4 → fix worker 3개, gate 2 미달. 대화형 환경에서는 `run_in_background: false`여도 Agent가 백그라운드로 돌아 Runtime 절의 fallback(모든 결과 수거 후 진행)대로 진행.
- spec-sync 1차 worker가 Step 6 검증 Bash에서 22분 정지(프로세스 없음, tool 결과 미기록) → TaskStop 후 재개 정보와 함께 1회 재실행 → v4.34.0 완료(R5 census 0건).
- 검증 레시피 변경(동등 기록 + 강화): R2에 스킬 이름·census 목록(삭제 디렉터리·리터럴 14개, 검색 범위에 README.md·AGENTS.md 추가), R3에 validate 경로·미러 기준선 기록. diff는 transcript에 표시.
- R2·R3·R5 실행 결과 전부 PASS(transcript). 커밋 9fa9191, push, PR #96 생성.
