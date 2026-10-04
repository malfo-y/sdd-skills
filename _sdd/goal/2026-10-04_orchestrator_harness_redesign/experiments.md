# Experiments

## Pending
- 없음

## Done
- [x] F1 벤치마크 하네스 + 구 경로 기준선 | 검증: `bench/run.sh`·`post.sh`·`review.sh`·`metrics.py`, 구 4회 | 결과: 통과(87 528/543s·M1 154/139k, 88 639/738s·M1 166/188k)
- [x] H1 `--plugin-dir` 격리 | 검증: 마커 플러그인·Base directory 확인 | 결과: 통과(단 marketplace 루트는 실패 → plugin.json 래퍼 `mkplug.sh`)
- [x] H2 headless worker 대기 | 검증: subagent meta `requestShape: foreground` + 결과 수신 | 결과: 통과
- [x] F2 spec 선갱신 | 검증: Feature A draft Part 1 + spec-sync v4.33.0, 최종 v4.34.0 R5 census 0건 | 결과: 통과(별도 feature 대신 draft Part 1·spec-sync로 수행)
- [x] F3 오케스트레이터 스킬 + digest·state(양 runtime) | 검증: R2·R3 | 결과: 통과(5853990)
- [x] F4 worker 계약 | 검증: structural 42/42 + smoke(worker 4, M2 0) | 결과: 통과
- [x] H3 레시피형 digest로 cold start ≤10s | 검증: R4 M3 | 결과: 통과(v3 중앙값 5.1s)
- [x] F5 신 경로 실측 | 검증: R4 | 결과: v1·v2 M1 불합격 → A2·A3 → v3 통과
- [x] F6 교체 + 구 경로 삭제 + spec-sync + PR | 검증: R1·R2·R3·R5 | 결과: 통과(9fa9191, PR #96)
- [x] 다시 읽기 비용이 cold start의 주원인이다 | 검증: PR #87 리뷰 4방식 transcript 구간 분해 → 처음 읽기 약 10초, 방법을 다시 알아내는 턴이 주원인 | 결과: 실패(가설 기각, 2026-10-04 cold start 토론)
- [x] 위치표·결정형 digest(v1)가 cold start를 줄인다 | 검증: 같은 과제 벽시계 비교 → 67초 대 노트 없음 68초 | 결과: 실패
- [x] 레시피형 digest(v2: 검증 명령·환경 함정·결정)가 cold start를 줄인다 | 검증: 같은 과제 → 처음 읽기 약 4초, AC 9개 검사 13초에 완료(fork는 약 24초) | 결과: 통과(표본 1회)
- [x] 맥락을 많이 준 worker도 AC 밖 결함을 찾는다 | 검증: fork·노트 받은 worker 모두 놓침, 새 agent 단독만 `main.md:76`·`:82` stale 참조 발견 | 결과: 실패(표본 1회 — M4 독립 리뷰를 둔 이유)
