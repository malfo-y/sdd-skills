# Report

**Status**: PASS — 보정 계측기로 v3 M2 재계측: 확정 0·unknown 0

## Summary
SDD 체인을 `sdd-orchestrator`(메인 루프 = 지휘, 단계 작업 = 계약을 읽는 범용 worker, digest·state 2파일 인계)로 실행하는 신 경로를 구 경로 옆에 만들고, 같은 기능 2개(PR #87 `review_evidence_floor`, PR #88 `goal_autonomy_grant`)를 base commit worktree에서 `claude -p`로 신·구 각각 실행해 비교했다. 신 경로는 3차례 다듬었다(v1 5853990 → v2 b83fbcd 맥락 다이어트 → v3 65a5bc4 dispatch 다이어트). 성능 측정 대상은 당시 하네스 v3(65a5bc4)다. 2026-10-05 현재 head의 보정된 계측기로 기존 transcript의 M2만 정정했다. 현재 head 하네스의 성능을 실행 검증한 결과는 아니다.

## 측정 표 (R4)
계측: `bench/metrics.py`(transcript jq 대체 파이썬, 메시지 id로 중복 제거). M1 = 메인 세션 (마지막 − 첫) input+cache_read+cache_creation. M2 확정 = 메인 세션의 대상 worktree 쓰기(Edit·Write·NotebookEdit + 쓰기를 확인한 Bash 호출 수), M2 unknown = 실행 효과나 쓰기 표적을 확정하지 못한 호출 수. 대상 밖 scratch·기존 허용 handoff/log 경로는 제외하고 `/tmp` 내부 대상은 포함한다. 확정 > 0이면 FAIL, 확정 0 + unknown > 0이면 UNVERIFIED, 둘 다 0일 때만 PASS다. 한 호출이 확정과 unknown에 모두 포함될 수 있다. M3 = worker 시작 → 첫 실질 tool_use(계약·digest·draft 읽기 제외) 중앙값. M4 = 하네스 없는 독립 리뷰(`bench/review.sh`, 고정 지시문, JSON schema)의 AC 판정과 Critical/High 수. M5 = 메인+worker 전체 토큰, 벽시계 = `claude -p` 시작~끝.

| run | 하네스 | 벽시계(s) | M1 증가 | M2 확정 | M2 unknown | M2 판정 | worker | M3 중앙값(s) | 총 토큰 | M4 AC | M4 C/H |
|-----|--------|-----------|---------|---------|------------|---------|--------|--------------|---------|-------|--------|
| 87-old-1 | 구 | 528 | 154.0k | 15 | 14 | FAIL | 2 | 1.5 | 5.63M | 9/9 MET | 0/0 |
| 87-old-2 | 구 | 543 | 138.7k | 10 | 13 | FAIL | 2 | 1.55 | 5.11M | 9/9 MET | 0/0 |
| 88-old-1 | 구 | 639 | 165.8k | 3 | 20 | FAIL | 2 | 2.5 | 6.37M | 15/15 MET | 0/0 |
| 88-old-2 | 구 | 738 | 188.3k | 7 | 22 | FAIL | 2 | 1.6 | 7.39M | 15/15 MET | 0/0 |
| 87-new-1 | v1 | 700 | 77.3k | 0 | 4 | UNVERIFIED | 7 | 7.7 | 6.47M | 9/9 MET | 0/0 |
| 87-new-2 | v1 | 912 | 92.9k | 0 | 1 | UNVERIFIED | 10 | 10.3 | 7.80M | 9/9 MET | 0/0 |
| 88-new-1 | v1 | 1185 | 91.9k | 0 | 2 | UNVERIFIED | 11 | 7.8 | 10.79M | 9/9 MET | 0/0 |
| 88-new-2 | v1 | 1197 | 97.8k | 0 | 0 | PASS | 11 | 6.0 | 9.21M | 9/9 MET | 0/0 |
| 87-new-3 | v2 | 597 | 62.1k | 0 | 0 | PASS | 8 | 5.7 | 4.84M | 10/10 MET | 0/0 |
| 87-new-4 | v2 | 574 | 59.0k | 0 | 0 | PASS | 7 | 1.6 | 4.81M | 9/9 MET | 0/0 |
| 88-new-3 | v2 | 1011 | 87.9k | 0 | 0 | PASS | 12 | 6.65 | 8.65M | 14/14 MET | 0/0 |
| 88-new-4 | v2 | 1158 | 95.6k | 0 | 0 | PASS | 13 | 6.1 | 9.46M | 14/14 MET | 0/0 |
| 87-new-5 | v3 | 637 | 53.6k | 0 | 0 | PASS | 7 | 6.3 | 3.88M | 9/9 MET | 0/0 |
| 87-new-6 | v3 | 656 | 53.3k | 0 | 0 | PASS | 7 | 6.5 | 4.27M | 9/9 MET | 0/0 |
| 88-new-5 | v3 | 1039 | 66.0k | 0 | 0 | PASS | 10 | 1.65 | 7.10M | 14/14 MET | 0/0 |
| 88-new-6 | v3 | 1220 | 80.3k | 0 | 0 | PASS | 12 | 5.1 | 7.06M | 15/15 MET | 0/0 |

88-new-2의 기존 M2 2건(auto-memory 쓰기)은 대상 worktree 밖이므로 확정 쓰기에서 제외했다. unknown은 쓰기를 입증한 수가 아니라 계측기가 실행 효과를 판별하지 못한 호출 수다. v1에 남은 unknown은 `for` 루프·`type`·`$(...)` 같은 환경 탐색 명령과 `sys.argv` 경로다. 새 모델 실행은 하지 않았다.

## 판정 (v3 기준, 경로별 중앙값) — R4 PASS
| 지표 | 구(4회) | 신 v3(4회) | 기준 | 판정 |
|------|---------|------------|------|------|
| M1 메인 맥락 증가 | 159.9k (87 146.4k / 88 177.0k) | 59.8k (87 53.5k / 88 73.2k) | 신 ≤ 구 × 0.5 → 0.37 (87 0.37 / 88 0.41) | PASS |
| M2 오케스트레이터 대상 쓰기 | 확정 15·10·3·7 / unknown 14·13·20·22 | 확정 0·0·0·0 / unknown 0·0·0·0 | 확정 0 및 unknown 0 (각 run) | PASS |
| M3 worker cold start | — | 중앙값 5.1s (worker 36개, 최대 80s 1건) | ≤ 10s | PASS |
| M4 품질 | AC 전부 MET, C/H 0 | AC 9/9·9/9·14/14·15/15 MET, C/H 0 | 둘 다 충족 | PASS |
| M5 총 토큰 (보고) | 6.00M | 5.66M | — | 0.94배 (87 0.76 / 88 1.03) |
| M5 체인 벽시계 (보고) | 591s | 848s | — | 1.43배 (87 1.21 / 88 1.64) |

벽시계는 늘었다. 원인(v1~v3 transcript 분해): 단계 직렬 구간(task 묶음 → read-only 검증 → 리뷰 3 worker → fix 묶음 → spec-sync), worker마다 대상 파일·검증 명령을 다시 확인하는 시간, 구현 게이트 fix가 있으면 한 바퀴가 더 돈다(88은 fix 3 task). 이번 두 기능은 task 3~5개의 작은 변경이라 병렬 이득(87은 Task 1∥2, 88은 2개씩)이 직렬 비용보다 작았다.

## 시도한 가설
- H1 `--plugin-dir`로 신·구 격리: marketplace 루트는 설치본을 덮어쓰지 못함 → plugin.json + skills symlink 래퍼(`bench/mkplug.sh`)로 성립. 구 경로 run은 설치 캐시 bee82a5(= main)로 실행.
- H2 headless에서 worker 대기: 성립(foreground 실행, 메인이 결과를 받은 뒤 진행).
- H3 레시피형 digest로 cold start ≤10s: v1부터 성립(중앙값 1.6~10.3s, v3 1.65~6.3s).
- v1 M1 근소 불합격 원인: 메인 루프의 worker 계약 읽기·환경 탐색·긴 반환·state 통째 재작성 → A2. v2 88 불합격 원인: 백그라운드 dispatch 안내문·알림 포장, dispatch마다 공통 경계 반복 → A3.

## 근거 (검증 레시피)
- R1: 브랜치 `refactor/orchestrator-harness`, PR https://github.daumkakao.com/vcga/malfo_sdd_skills/pull/96 (OPEN).
- R2: `sdd-orchestrator` SKILL·references 9개 파일 양 runtime 존재, 구 단계 스킬 디렉터리 10개 부재, marketplace 구 항목 0, census 리터럴 14개 0건.
- R3: `git diff --check main...HEAD` rc=0, `claude plugin validate` Validation passed, 미러 hunk 기준선 일치(orchestrator 1 = Runtime 절 141행, references 동일본, AGENTS 템플릿 4개 동일).
- R4: 위 측정 표(v3 판정 PASS). M1·M3·M4·M5와 벽시계는 과거 측정값을 보존했다. M2의 v3 순서는 87-new-5·87-new-6·88-new-5·88-new-6이다.
- R5: Spec Version 4.32.0(main) → 4.34.0, 구 Guardrail 리터럴 4종 0건.

### M2 재계측 입력·실행 근거 (2026-10-05)

- 입력: 벤치마크 scratch 디렉터리(`BENCH_DIR`, 세션 로컬)의 `logs/runs.tsv`와 각 sid의 transcript `~/.claude/projects/*/<sid>.jsonl`. 삭제된 worktree도 `BENCH_DIR/t-<run>` 경로를 기준으로 판별했다.
- 실행 명령(repo 루트): `python3 _sdd/goal/2026-10-04_orchestrator_harness_redesign/bench/metrics.py <BENCH_DIR> 87-old-1 87-old-2 88-old-1 88-old-2 87-new-1 87-new-2 88-new-1 88-new-2 87-new-3 87-new-4 88-new-3 88-new-4 87-new-5 87-new-6 88-new-5 88-new-6` → exit 0, 0.27초, 16개 결과. 계측기는 이 보고를 커밋한 시점의 `bench/metrics.py`다.
- 남은 unknown의 `tool_index`(메인 tool_use 1-based): 87-new-1 `6,7,13,29`; 87-new-2 `42`; 88-new-1 `4,5`. 신 경로 v2·v3는 unknown 0이다. 지원하지 않는 shell 문법·명령 치환·동적 경로·allowlist 밖 Python 호출은 unknown으로 남는다.
- stderr에는 transcript의 Python 분석 중 `SyntaxWarning: invalid escape sequence` 1건이 있었다. 실행은 정상 종료했다.

## 남은 일·주의
- 벽시계 1.43배 증가는 합격 기준 밖(보고만)이다. 작은 기능에서는 단계 직렬 구간 비용이 병렬 이득보다 크다. 개선 후보: 리뷰와 spec-sync 병행, fix 묶음 축소, 작은 draft는 리뷰 worker 수 축소.
- 벤치마크 세션 하나(88-new-2)가 사용자 프로젝트 메모리에 `bash-grep-ugrep-gitignore.md`를 썼다(내용은 사실, 보존). 필요 없으면 지워도 된다.
- Codex는 정적 검사만 했다(실측 안 함).
- PR merge는 사용자 확인 사항이다.
