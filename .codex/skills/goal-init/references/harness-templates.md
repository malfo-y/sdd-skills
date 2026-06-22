# Goal Harness Templates (4-File)

goal-init이 `_sdd/goal/<YYYY-MM-DD>_<slug>/`에 생성하는 4파일 하네스의 단일 소스 템플릿이다.
SKILL.md Process(Harness Setup 단계)가 이 템플릿을 참조해 슬롯을 채운다. Codex 미러 스킬도 동일 템플릿을 references로 복사 사용한다.

`<...>` 는 생성 시 치환할 슬롯이다. 그 외 텍스트(헤딩·레이블·구조)는 그대로 유지한다.

분업 원칙(D10):
- **완료조건**(`DONE WHEN`/`CONSTRAINTS`/`STOP`)은 `/goal` 조건 문자열에 자족 인라인 → 평가자(도구 없는 small fast model)가 transcript만으로 판정한다. 증명은 명령·기대 출력이 대화에 surface되는 형태로 인라인한다 (별도 VERIFY 슬롯 없음).
- **루프 행동(HOW)**은 `goal.md`의 `Loop Protocol` 섹션 → 메인 에이전트가 읽는다. 평가자가 매 턴 HOW 노이즈를 읽지 않도록 조건 문자열과 분리한다.

---

## 1. `goal.md` 템플릿

```markdown
# Goal: <목표 한 줄 제목>

## 목표 서술
<무엇을 달성하려는지 1-2단락. 배경·왜 중요한지 포함.>

## `/goal` 조건 문자열
> 아래 블록을 `/goal <조건>`에 그대로 넣는다. 평가자는 도구 없이 transcript만으로 판정하므로 자족적이어야 한다.

DONE WHEN: <측정 가능한 AC>. 증명: `<검증 명령>` shows `<기대 출력/판정>` in the transcript.
<AC가 여럿이면 줄을 추가. 각 줄에 증명 명령·기대 출력을 인라인한다.>
CONSTRAINTS: <지켜야 할 제약. 없으면 이 줄 삭제.>
STOP: after <N> turns without progress.

## Loop Protocol
매 턴 다음을 수행한다 (이 섹션은 메인 에이전트용 HOW이며 조건 문자열에 넣지 않는다):
1. `experiments.md`의 pending 가설 하나를 골라 시도한다.
2. 해당 가설의 검증 명령을 실행하고 **출력을 대화에 그대로 표시**한다 (평가자가 transcript에서 본다).
3. 시도·검증 결과를 `journal.md`에 append한다.
4. pending 큐가 비었는데 목표 미완이면, 새 가설을 brainstorm해 `experiments.md` pending에 append한다.

## 실행법
<!-- Codex 슬롯은 이 Codex 스킬용으로 채워져 있고, Claude Code 슬롯은 placeholder다. goal-init 실행 시 자기 런타임 슬롯만 최종 산출 goal.md에 반영한다. -->

### Claude Code
<Claude Code에서의 활성화·실행 명령 placeholder>

### Codex
1. goals 기능 활성화: `codex features enable goals` (features.goals).
2. 라이프사이클: `set`(목표 설정)·`status`(진행 확인)·`clear`(종료) + 필요 시 `pause`·`resume`.
3. continuation은 thread-scoped이며 안전 경계 안에서만 이어간다 (evidence-based — 각 턴의 검증 출력을 근거로 진행).
```

---

## 2. `experiments.md` 템플릿

가설 큐. 자동 루프와 사용자 수동 추가가 공용으로 쓴다. 각 항목 = 가설 한 줄 + 검증 방법(명령/판정조건) + 상태.

```markdown
# Experiments

## Pending
- [ ] <가설 한 줄> | 검증: `<명령>` → <판정조건>
- [ ] <가설 한 줄> | 검증: `<명령>` → <판정조건>

## Done
- [x] <시도한 가설> | 검증: `<명령>` → <판정조건> | 결과: <통과/실패/부분>
```

---

## 3. `journal.md` 템플릿

append-only. 새 항목은 항상 파일 끝에 추가한다 (기존 항목 수정·삭제 금지).

```markdown
# Journal (append-only)

## <타임스탬프 또는 턴 N>
- 가설: <이번 턴에 시도한 가설>
- 검증: `<명령>` → <출력 요약>
- 결과: <통과 | 실패 | 부분>
- 다음: <다음 결정 — 다음 가설 / 큐 보충 / 종료>
```

---

## 4. `report.md` 템플릿

conclusion-first. status를 상단에 둔다.

```markdown
# Report

**Status**: <PASS | FAIL | STUCK>

## Summary
<무엇을 달성했고 어디서 막혔는지 한 단락.>

## 시도한 가설
- <가설 1> → <결과>
- <가설 2> → <결과>

## 근거
<journal.md의 어느 항목이 결론을 뒷받침하는지 참조 (턴/타임스탬프).>

## 다음 단계
1. <다음 행동>
2. <다음 행동>
3. <다음 행동>
```
