# Handoff Templates

아래 두 fenced template을 출발 구조로 쓴다. 담을 것과 넣지 않을 것의 규칙은 `SKILL.md`의 `인계 파일` 절이 소유한다. 슬롯(`<...>`)을 실제 값으로 바꾸고, 표 행은 필요한 만큼 반복한다. 해당 항목이 없으면 `없음` 한 줄로 둔다.

## digest.md

```markdown
# Digest: <slug>

## 출처
- draft: <경로 또는 없음>
- discussion: <경로 또는 없음>

## 결정·제약
- <대화에서만 나온 결정·선호·계획 이탈 — 이유 1줄>

## 환경 함정
- <다시 알아내려면 시행착오가 드는 환경 사실 — 예: 셸 함수가 덮어쓴 명령, 느린 테스트, 필요한 플래그>

## 검증 레시피
| AC | 명령 | 기대값 |
|----|------|--------|
| <Task n AC m> | <실행 명령> | <통과로 판정하는 출력·exit code> |
| 회귀 | <fast 회귀 명령> | <기대값> |
```

## state.md

```markdown
# State: <slug>

- 출처: <draft 경로 또는 요청 요약>
- base: <구현 시작 commit> / 시작 시 dirty: <파일 목록 또는 없음>
- 단계: <feature-draft | plan-review | implementation | implementation-review | spec-sync | done>
- 종점: <spec-sync | 사용자가 지정한 단계>

## Tasks
| Task | 담당 | 상태 | triage | RED·GREEN 명령과 신호 | 계약 오류 선언 |
|------|------|------|--------|----------------------|----------------|
| <Task n> | <worker 차수> | <READY / DELTA_CLOSED / BLOCKED> | <(a)/(b)/(c)/read-only + 근거> | <명령 → 신호> | <횟수와 이유> |

## Gates
| 게이트 | 호출 | fix 전 raw C/H/M/L | fix | 검증 |
|--------|------|-------------------|-----|------|
| <계획 / 구현> | <1 / 2> | <수> | <반영·미반영> | <재실행 증거 포인터> |

## 계획 이탈·발견
- <Task n>: <내용> → <이유> → <처리>

## AC → 증거
| Task | AC | 판정 | 증거 |
|------|----|------|------|
| <Task n> | <AC m> | <MET / NOT MET / UNTESTED> | <리뷰 worker verdict 포인터 또는 fix 재실행 증거> |
```
