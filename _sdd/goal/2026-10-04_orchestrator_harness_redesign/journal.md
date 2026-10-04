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
