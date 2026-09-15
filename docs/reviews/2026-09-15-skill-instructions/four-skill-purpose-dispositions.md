# 네 스킬 목적 중심 개선 적용 기록

- 모델: gpt-6-astra; 기준 b34b2cb; 브랜치 refactor/four-skill-outcome-guidance.
- 사용자 승인: “넷 다 수정해줘”. 스킬 원문에 적용했고 연결된 reference/example/spec을 동기화했다.
- 상태: 소스 검증·implementation-review gate 1·fix 검증·spec-sync 완료. 실제 설치본/외부 goal·PR·모델 행동 효과는 미검증.

| 리뷰 항목 | 적용 결과 | 소유 표면 |
|---|---|---|
| GI-P01·02·03 | 대화 고정 단계·최소 가설 수 해제, 조건 self-check 단일화 | goal-init 본문·하네스 template·example, sdd-autopilot 포인터 |
| PR-P01 | leaf 입력 4필드; 메인 metadata/spec/validation 수집 유지 | pr-review PR Review Input, simplicity Scope |
| PR-P02·03 | 파일 수 대신 위험/AC 기준, 검사 상태 기본·의미 있는 비율만 허용 | pr-review correctness·Signals·example |
| PR-P04·IR-P04 | schema 선택 표와 override/실패 경계로 중복 예시 정리 | Codex 두 review adapter |
| IM-P01 | 변이 미수행에 대한 일반화 제거, 변이 검증 의무 유지 | implementation 델타 절 |
| IM-P02 | resume 필수 정보와 발생 예외 구분; task별 블록 허용; 조건부 채팅 | implementation ledger·마감 2 |
| IM-P03 | gate 1/2 공통 fix 정책 단일화, 임계·Low·fix 검증·상한 보존 | implementation 마감 3 |
| IR-P01 | 커밋+staged+unstaged+untracked 후보와 hunk 귀속 대조 | implementation-review 읽기 범위, implementation 시작점 기록 |
| IR-P02·03 | 6승격 조건 그대로 목록화, 중복 Recommendations를 한계/재개 조치와 분리 | implementation-review 읽기·보고 |

## 검증

- 원문 YAML 10개(대상 8 + sdd-autopilot 2) 파싱 통과. quick_validate의 기존 argument-hint 미지원 때문에 해당 필드만 임시 사본에서 제외해 검사했으며 원문 필드는 보존했다.
- 실제 git 후보 수집 명령을 양 runtime에서 추출해 격리 repo의 전부 미커밋/전부 커밋/혼합/커밋+무관한 dirty 4경우 통과. 마지막 경우 후보에는 무관한 dirty도 포함되며, 실제 scope/hunk 귀속은 agent가 판단할 의무다. 이 fixture는 agent의 판단 성공을 증명하지 않는다.
- 양쪽 implementation 본문, goal template, simplicity reference byte parity 확인. 로컬 링크·0644·git diff --check와 사용자 dirty/기존 리뷰/기록 보존 확인.

## 정적 정책 시나리오

| 경우 | 소스가 요구하는 결과 |
|---|---|
| 목표·접근·권한·검증이 충분 | 재수집·가설 수 채우기 없이 self-check와 하네스 완성 |
| 원인 탐색 필요 | 구별되는 가설·검증법·trade-off 비교 |
| 권한 미확정 / 단발 / 판정 불가 | 필요한 확인 또는 비대상·미완료 보고, goal 비발동 |
| PR 동작 보존 맥락 필요 | 관련 spec/저자 설명과 동일 SHA 경로 전달; 메인이 검증 소유 |
| 다수 기계적 변경 속 보안 경계 | 파일 수로 검토 축소하지 않고 위험/AC 검토 |
| test 결과 분모 불명 / 실행 evidence 없음 | 비율 창작 없이 검사 상태·증거/UNTESTED |
| RED 후 재개 / GREEN 후 델타 미완료 | ledger에 상태·신호 남기고 미완료 task fresh 판정 |
| gate 1 임계 미달 / 도달 | fix 검증 후 각각 종료 / gate 2 |
| 문서만 고친 fix / gate 2도 임계 도달 | fix 재검증 / 표적 검증 후 잔여와 수동 후속 권고 |
| 코드·제어 흐름·행동 AC·재작성·의심·질문 각각 | 어느 조건 하나라도 전문 읽기, 무신호 산문은 hunk-scoped |
| mailbox / legacy / 미지원 schema·override | 각각 맞는 lifecycle / 제한 보고, 두 leaf와 no-inline 경계 보존 |

이 표는 원문 의미 대조다. 실제 입력으로 스킬을 실행한 행동 평가가 아니다.

## 품질 게이트

- 설치된 implementation-review와 설치된 simplicity 계약 전문을 사용했다. 메인이 correctness를 수행하고 참조/국소 simplicity leaf를 먼저 띄워 병행했다. 변경 중인 source skill을 설치본의 행동 효과로 평가한 것이 아니다.
- Gate 1 (gpt-6-astra): correctness C0/H0/M2/L0, simplicity 참조 C0/H0/M0/L0, 국소 C0/H0/M0/L0. 두 묶음의 4개 차원 모두 PASS. raw 합산 C0/H0/M2/L0으로 gate 2 조건(C+H≥3 또는 M≥5) 미달.
- C1 Medium: goal-init의 자율 수준 문구가 일반적인 정보 재사용 기준과 달리 이미 확정한 attended 수준에도 재질문으로 읽힐 수 있었다. 기존 수준·승인 범위 우선 재사용을 명시했다.
- C2 Medium: implementation-review의 “최초 dirty 제외”가 같은 파일의 새 작업 hunk까지 제외하는 것으로 읽힐 수 있었다. 기존 변경만 제외하고 이번 hunk를 포함하도록 범위를 명시했다.
- Fix delta: 두 수정은 기존 A1·A4의 의미 명료화이며 신규 실행 기능/옵션 없음. 양 runtime와 해당 spec 설명을 함께 수정하고 정적 시나리오·fresh 구조/recipe 검증을 다시 확인했다. 이미 정한 attended 권한을 재사용하고, 같은 dirty 파일에서도 작업별 hunk 귀속을 구분한다.
- 미해결 correctness/simplicity finding 없음. 실제 native goal 실행·PR 리뷰 동작·모델 처리 시간/탐지율은 검증 범위 밖이다.


## 최종 AC와 증거

| AC | 판정 | 증거 |
|---|---|---|
| A1 | MET (소스 계약) | goal-init Decision Criteria / Condition Self-check / Harness Setup / Handoff, 연결 template·example·sdd-autopilot |
| A2 | MET (소스 계약) | pr-review PR Review Input 4필드 / Correctness / Signals, simplicity Scope·PR example |
| A3 | MET (소스 계약) | implementation ledger / 델타 / 마감; TDD·변이·Low·재검증·2회 상한 유지 |
| A4 | MET (소스 + 명령 recipe) | implementation-review 읽기 범위·6개 승격 조건·보고·adapter, 격리 git fixture 4/4 |
| A5 | MET (문서 정합성) | spec 4.32.0, components/usage, ko/en AUTOPILOT_GUIDE, append-only decision/changelog |
| A6 | MET (검증 실행) | 원문 YAML/정규화 validator 10개, mirror 3쌍, 상대 경로·권한·diff check, git fixture 4경우; gate 1/fix |

실행 artifact는 로컬 `/tmp/four-skill-outcomes-path`가 가리키는 임시 디렉토리의 `scope-results.json`에 있다. 재현용 로컬 checker는 `/tmp/verify_four_skills.py`다. 임시 파일은 배포 자산이 아니며 소스·시나리오와 검증 범위는 이 문서에 남긴다.

## 본문 크기 변화

줄 수에는 frontmatter·공백·코드 블록이 포함되며 references는 제외한다. 크기는 성능 측정이 아니다. 구현 리뷰의 Claude 본문은 범위 수집 명령과 승격 조건을 풀어 써서 늘었다.

| 스킬 | Claude | Codex |
|---|---:|---:|
| goal-init | 131 → 63 | 131 → 63 |
| pr-review | 267 → 264 | 305 → 286 |
| implementation | 153 → 148 | 153 → 148 |
| implementation-review | 108 → 121 | 153 → 148 |
