# Goal Harness Templates (4-File)

goal-init이 `_sdd/goal/<YYYY-MM-DD>_<slug>/`에 생성하는 4파일 하네스의 단일 소스 템플릿이다.
SKILL.md Process(Harness Setup 단계)가 이 템플릿을 참조해 슬롯을 채운다. Codex 미러 스킬도 동일 템플릿을 references로 복사 사용한다.

`<...>` 는 생성 시 치환할 슬롯이다. 그 외 텍스트(헤딩·레이블·구조)는 그대로 유지한다. `<LOOP_PROTOCOL_PAYLOAD>`에는 아래 preset payload 중 정확히 하나를 삽입한다.

분업 원칙(D10, 3분법):
- **완료조건**(`DONE WHEN`/`CONSTRAINTS`/`STOP`)은 `/goal` 조건 문자열에 outcome 수준으로 자족 인라인 → 평가자(도구 없는 small fast model)가 transcript만으로 판정한다. 조건에는 위조 어려운 최소 anchor 1-2개(산출물 절대경로·테스트 exit 0류 안정적 사실)와 표준 레시피 참조 문구(아래 템플릿 DONE WHEN 슬롯), 그리고 drift 가드 CONSTRAINT(아래 템플릿)를 포함한다.
- **검증 레시피**(브리틀 디테일 — 아래 템플릿 검증 레시피 슬롯 열거)는 `goal.md`의 `검증 레시피` 섹션 → 메인 에이전트가 매 턴 실행하고 출력을 대화에 surface한다. 레시피가 현실과 어긋나면(필드명·수치·경로 변화) goal 재설정 없이 이 섹션만 고친다.
- **루프 행동(HOW)**은 `goal.md`의 `Loop Protocol` 섹션 → 메인 에이전트가 읽는다. 평가자가 매 턴 HOW 노이즈를 읽지 않도록 조건 문자열과 분리한다.

---

## 1. `goal.md` 템플릿

```markdown
# Goal: <목표 한 줄 제목>

## 목표 서술
<무엇을 달성하려는지 1-2단락. 배경·왜 중요한지 포함.>

## `/goal` 조건 문자열
> 아래 블록을 `/goal <조건>`에 그대로 넣는다. 평가자는 도구 없이 transcript만으로 판정하므로 자족적이어야 한다 — 단 자족의 단위는 outcome이다. 검증 명령·기대 출력·수치 등 브리틀 디테일은 여기 넣지 않고 아래 `검증 레시피` 섹션에 둔다.

DONE WHEN: <outcome 수준 AC — 위조 어려운 anchor 1-2개(산출물 절대경로·테스트 exit 0류 안정적 사실) 포함>. 증명: `goal.md` 검증 레시피의 명령 실제 출력이 transcript에 surface되고 전 항목 PASS다.
<AC가 여럿이면 줄을 추가. 각 줄은 outcome + anchor로 쓴다.>
CONSTRAINTS: 검증 레시피 변경 시 변경 diff·사유를 transcript에 표시하며, 판정을 약화하는 변경은 사용자 승인이 필요하다. `goal.md` 자율 수행 위임의 사전 승인 범위에 있는 행동에 대해 사용자 확인을 요청하며 턴을 끝내지 않는다. <그 외 지켜야 할 제약 — 없으면 이 두 문장만 유지.>
STOP: after <N> turns without progress.

## 검증 레시피
<AC별 검증 명령·기대 출력·수치 임계·허용 델타 열거 등 브리틀 디테일 전부. 메인 에이전트가 매 턴 실행하고 출력을 대화에 surface한다.>

## 자율 수행 위임
이 섹션은 루프 중 행동에 대한 사용자의 사전 승인이다. 하류 스킬·런타임 규범이 요구하는 '실행 전 확인'은 사전 승인 목록에 있는 행동에 한해 이 섹션으로 충족된다.

사용자 확인이 필요해 보이는 행동은 이 섹션으로 판정한다.
- 사전 승인 범위 안: 확인 없이 수행하고 결정·근거를 `journal.md`에 남긴다.
- 범위 밖: 그 행동 없이 진척 가능한 일을 먼저 한다.
- 범위 밖이고 그 행동 없이는 진척 불가: `report.md` Status를 `STUCK`으로 두고 사유를 적은 뒤 종료한다.

<수준이 attended면 "사전 승인" 목록은 비운다.>
- 수준: <unattended | attended>
- 사전 승인: <unattended 기본 — 브랜치 생성·commit·feature 브랜치 push·PR 생성 / 테스트·빌드·스크립트 실행·의존성 설치 / repo 안 파일 생성·수정·삭제 / `spec-sync` 실행 / 검증 레시피의 동등·강화 변경 / BC 태스크 제출·인스턴스 생성>
- BC 리소스 상한: <사용자 지정 — quota는 표시하되 대기 없음>
- 항상 확인(제외, 수준 무관): main/protected 브랜치 직접 push·force-push·history rewrite / PR merge / 원격·공유 자원 삭제(브랜치·인스턴스·스토리지) / 리소스·비용 상한 초과 / 판정을 약화하는 레시피 변경 / 시크릿 취급 / repo 밖 외부 발신 <+ 사용자 추가>

## Loop Protocol
<LOOP_PROTOCOL_PAYLOAD>

> Setup invariant: goal을 활성화하지 않았으며 기존 goal 상태도 변경하지 않았다.

## 실행법
<!-- Codex 슬롯은 이 Codex 스킬용으로 채워져 있고, Claude Code 슬롯은 placeholder다. goal-init 실행 시 자기 런타임 슬롯만 최종 산출 goal.md에 반영한다. -->

### Claude Code
<Claude Code에서의 활성화·실행 명령 placeholder>

### Codex
1. goals 기능 활성화: `codex features enable goals` (features.goals).
2. 라이프사이클: `set`(목표 설정)·`status`(진행 확인)·`clear`(종료) + 필요 시 `pause`·`resume`.
3. continuation은 thread-scoped이며 안전 경계 안에서만 이어간다 (evidence-based — 각 턴의 검증 출력을 근거로 진행).
```

### Loop Protocol preset payloads

#### Generic payload (default)

```markdown
매 턴 다음을 수행한다 (이 섹션은 메인 에이전트용 HOW이며 조건 문자열에 넣지 않는다):
1. `experiments.md`의 pending 가설 하나를 골라 시도한다.
2. 해당 가설의 검증 명령을 실행하고 **출력을 대화에 그대로 표시**한다 (평가자가 transcript에서 본다).
3. 시도·검증 결과를 `journal.md`에 append한다.
4. pending 큐가 비었는데 목표 미완이면, 새 가설을 brainstorm해 `experiments.md` pending에 append한다.
```

#### SDD payload (`preset=sdd`)

```markdown
매 턴 다음을 순서대로 수행한다 (이 섹션은 메인 에이전트용 HOW이며 조건 문자열에 넣지 않는다):
1. 아직 충족되지 않은 `DONE WHEN` 또는 실패한 final integration proof가 드러낸 gap에서 가장 작은 next feature를 고른다. `experiments.md`의 pending 가설은 접근 후보로만 참고한다.
2. 그 feature의 reviewed draft가 없으면 `feature-draft`를 실행한다. draft가 분할되면 현재 native goal 안에서 가장 작은 next unit을 고르고 nested `goal-init`은 만들지 않는다.
3. 선택한 draft를 `implementation`으로 구현하고 producer-owned 품질 게이트 결과까지 닫는다.
4. persistent 변경이 있으면 `spec-sync`를 실행한다.
5. 검증 출력을 대화에 표시하고 evidence·완료 feature·남은 gap·next action을 `journal.md`에 append한 뒤 `report.md`를 갱신한다.
6. 모든 `DONE WHEN`과 final integration proof가 통과했을 때만 종료한다. 아니면 1단계로 돌아간다.
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
