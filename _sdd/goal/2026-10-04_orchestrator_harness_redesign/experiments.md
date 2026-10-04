# Experiments

## Pending
- [ ] F1 벤치마크 하네스 + 구 경로 기준선: 대상 worktree + `claude -p --plugin-dir`로 구 경로를 PR #87·#88에서 각 2회 실행하고 M1~M5 기준선 표를 만든다 | 검증: `report.md` 측정 표에 구 경로 M1~M5 값이 있고, 각 값이 transcript jq 출력으로 뒷받침된다 → 기준선 확정
- [ ] H1 `--plugin-dir <브랜치 worktree>`로 신 harness를 로드하면 같은 대상 worktree에서 신·구를 격리 실행할 수 있다 | 검증: `claude -p --plugin-dir <wt> "<스킬 목록 질의>"` 출력에 새 오케스트레이터 스킬 이름이 보이고, 대상 worktree의 `.claude/skills`와 섞이지 않는다 → 통과 시 R4 실행 방식 확정
- [ ] H2 headless(`-p`)에서도 오케스트레이터가 worker 완료를 기다린 뒤 다음 단계로 간다 | 검증: 시험 세션 transcript에서 worker 결과 수신 → 다음 dispatch 순서가 보인다 → 실패 시 포그라운드 dispatch로 설계 조정
- [ ] F2 spec 선갱신: 재편과 충돌하는 Guardrail·결정(R5 census 목록)과 `main.md:76`·`:82` stale 참조를 정리한다 | 검증: R5 → census 0건, 버전 상승
- [ ] F3 오케스트레이터 스킬 + digest·state 계약(Claude·Codex 미러) | 검증: R2·R3 → 두 런타임 SKILL.md 존재, 정적 검사 PASS
- [ ] F4 worker 계약: 계획 worker, task별 구현 worker(조건부 병렬), 리뷰 worker(작성자와 분리, 통과 주장 미제공), spec-sync worker | 검증: R3 + 시험 실행 1회에서 각 worker가 digest 변경분을 반환한다
- [ ] H3 레시피형 digest로 worker cold start 중앙값이 10초 이하로 유지된다 | 검증: R4 M3
- [ ] F5 신 경로 실측과 합격 판정 | 검증: R4 M1~M4 전부 PASS, M5 보고
- [ ] F6 교체 + 구 경로 삭제 + spec-sync + PR | 검증: R1·R2·R5 PASS

## Done
- [x] 다시 읽기 비용이 cold start의 주원인이다 | 검증: PR #87 리뷰 4방식 transcript 구간 분해 → 처음 읽기 약 10초, 방법을 다시 알아내는 턴이 주원인 | 결과: 실패(가설 기각, 2026-10-04 cold start 토론)
- [x] 위치표·결정형 digest(v1)가 cold start를 줄인다 | 검증: 같은 과제 벽시계 비교 → 67초 대 노트 없음 68초 | 결과: 실패
- [x] 레시피형 digest(v2: 검증 명령·환경 함정·결정)가 cold start를 줄인다 | 검증: 같은 과제 → 처음 읽기 약 4초, AC 9개 검사 13초에 완료(fork는 약 24초) | 결과: 통과(표본 1회)
- [x] 맥락을 많이 준 worker도 AC 밖 결함을 찾는다 | 검증: fork·노트 받은 worker 모두 놓침, 새 agent 단독만 `main.md:76`·`:82` stale 참조 발견 | 결과: 실패(표본 1회 — M4 독립 리뷰를 둔 이유)
