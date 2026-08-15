# 토론 요약: goal-init 조건 문자열 고도(altitude) — outcome 조건 / 검증 레시피 분리

**날짜**: 2026-08-14
**라운드 수**: 4
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)
- **사용자 문제 제기**: goal-init이 만드는 `/goal` 조건 문자열이 너무 디테일하다. 조건에 검증 디테일이 인라인돼 있어 현실과 살짝 어긋나면(필드명·수치·허용 델타) goal 자체를 다시 세워야 하는 일이 반복된다. 조건은 high-level 목표+AC로 올리고 구체는 goal.md가 들게 하자.
- **토론을 시작한 배경**: goal-init을 자주 사용 중이며, dancepdd에서 실제 goal 재설정 비용이 발생했다. 후속으로 goal-init SKILL.md·harness-templates.md 개정(feature-draft → implementation)이 예정된다.
- **현재 상태**: harness-templates.md의 분업 원칙 D10은 2분법 — 완료조건(`DONE WHEN`/`CONSTRAINTS`/`STOP`)은 조건 문자열에 자족 인라인, HOW는 `goal.md` Loop Protocol. 평가자는 도구 없이 transcript만으로 판정(4,000자 상한, Hard Rule I1). 이 "자족 인라인" 압력이 조건 비대화의 구조적 원인.
- **범위와 제외 범위**: 범위 = goal-init SKILL.md Step 3·harness-templates.md(D10·goal.md 템플릿)·Codex 미러·spec surface. 제외 = 네이티브 `/goal` 평가자 자체의 동작 변경(불가), ralph-loop-init, 기존에 생성된 dancepdd goal들의 소급 수정.
- **수집한 근거**: `.claude/skills/goal-init/SKILL.md`(Hard Rule I1·Step 3 self-check 3항목), `.claude/skills/goal-init/references/harness-templates.md`(D10·템플릿), 실측 사례 `~/github/dancepdd/_sdd/goal/2026-08-13_pdd_lmax16_ablation/goal.md`(조건 2,331자: manifest 전체 스키마 jq predicate, 허용 코드 델타 ①~⑥ 전수 열거 — ⑥은 실행 중 사용자 승인으로 goal을 이미 한 번 수정한 흔적, baseline 8값 하드코딩), `_sdd/spec/components.md`·`main.md`·decision_log 2026-08-10 entry.

## 핵심 논점 (Key Discussion Points)
1. **순수 포인터 방식의 함정**: 조건을 "goal.md를 만족한다"로 바꾸면 평가자(도구 없음)가 원본 AC를 볼 수 없어 에이전트 자기 보고의 고무도장이 된다. 따라서 "고도 상향"이지 "간접화 전면 전환"이 아니다.
2. **goal drift 리스크**: 레시피가 mutable한 goal.md로 내려가면 에이전트가 루프 중 검사 항목을 약화시키고 PASS를 보고할 수 있다.
3. **인라인 vs 하강 판별 기준**: 무엇이 조건에 남아야 하는지의 원칙적 기준이 필요하다.
4. **평가자 판정력 보존**: 레시피 전면 하강 시 평가자는 "PASS 주장"만 보게 됨 — 위조 어려운 최소 anchor가 조건에 남아야 한다.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| 1 | D10을 2분법에서 **3분법**으로 개정: 조건 문자열 = outcome 수준 DONE WHEN + 최소 anchor / 검증 레시피(브리틀 디테일) = `goal.md` 신설 "검증 레시피" 섹션 / HOW = Loop Protocol (유지) | 조건 비대화의 원인이 자족 인라인 압력임을 실측 사례로 확인 (`코드 확인`) | 1, 3 |
| 2 | drift 가드 = 조건 문자열의 표준 **CONSTRAINT 한 줄**: "레시피 변경 시 변경 diff·사유를 transcript에 표시, 판정 약화는 사용자 승인 필요". immutable 고정은 유연성 목적을 죽이므로 기각 | 평가자가 transcript에서 위반을 볼 수 있고 비용 최소 (`사용자 판단`) | 2 |
| 3 | 인라인/하강 판별 기준 = **재설정 litmus**: "이 디테일이 현실과 어긋나면 goal을 다시 세우는 게 마땅한가?" Yes(목표가 바뀜) → 인라인, No(검증 방법만 바뀜) → 레시피 | 카테고리 고정 목록은 유지비용, 글자수 상한은 임의적 압축이라 기각 (`사용자 판단`) | 3 |
| 4 | 조건 문자열에 **최소 anchor 1-2개 유지**(산출물 절대경로·테스트 exit 0 등 위조 어렵고 안정적인 사실) + 표준 문구 "goal.md 검증 레시피의 명령 실제 출력이 매 턴 surface되고 전 항목 PASS" | 순수 outcome만이면 평가자가 사실상 승인기가 됨 (`사용자 판단`) | 4 |
| 5 | 재설정 litmus·브리틀 디테일 점검은 Step 3 **지침(Key Principle 수준)으로만** 추가하고 self-check hard gate 항목으로 추가하지 않는다 (기존 3항목 gate 유지) | gate 과적재 회피 (`사용자 판단`) | 3 |

### 기각한 대안
- **순수 goal.md 포인터 조건**: 평가자가 원본 AC를 볼 수 없어 고무도장화 — `/goal`이 막으려는 "적당히 done 선언" 실패 모드 재도입.
- **레시피 섹션 immutable(append-only)**: drift는 막지만 "사소한 불일치에 유연"이라는 이번 개선의 목적 자체를 무효화.
- **drift 가드 없이 SDD 리뷰에 위임**: generic preset(리뷰 없는 루프)에서 무방비.
- **카테고리 고정 목록 판별**: 경계 사례마다 목록이 자라는 유지비용.
- **글자수 상한 판별**: 무엇을 내릴지 알려주지 않는 임의적 압축.
- **핵심 predicate 축소판 인라인**: 판정력은 최강이지만 수치가 곧 브리틀 지점이라 재설정 문제 부분 재발.

## 미결 질문 (Open Questions)
(없음)

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | feature-draft: ① harness-templates.md D10 3분법 개정 + goal.md 템플릿 "검증 레시피" 섹션·drift CONSTRAINT 표준 문구·anchor 슬롯 ② SKILL.md Step 3 재설정 litmus 지침(비-gate) ③ Codex 미러 2벌 ④ spec-sync | High | 본 세션 |

### 후속 핸드오프 (Handoff)
- **목표**: goal-init이 생성하는 조건 문자열이 outcome 수준 DONE WHEN + 최소 anchor + 표준 레시피 참조 문구 + drift CONSTRAINT로 구성되고, 브리틀 검증 디테일은 goal.md "검증 레시피" 섹션으로 내려간 템플릿·스킬 지침이 Claude/Codex 양쪽에 반영된다.
- **변경 금지 제약**: 5단계 프로세스·4파일 계약·self-check hard gate 3항목(도구 없이 판정·evidence surface·4,000자)·비발동(I2)·setup 불변식은 불변. 네이티브 `/goal` 평가자 동작 가정을 바꾸지 않는다. ralph-loop-init 불간섭.
- **검증**: 템플릿·SKILL.md diff 검토 + Codex 미러 parity grep + (가능하면) 샘플 목표로 조건 문자열을 드라이런 생성해 재설정 litmus 적용 결과 확인.
- **중단 조건**: 구현 중 self-check gate 구조를 바꿔야만 성립하는 설계가 나오면(결정 5와 모순) 중단·보고.

## 리서치 결과 요약 (Research Findings)
- lmax16 goal.md 실측: 조건 2,331자 중 재설정 litmus로 인라인 잔류 대상은 "ablation 1회 완주·manifest 존재(절대경로)·gate 이진 판정 제시·테스트 green·SDD 단계 닫힘" 수준. jq 스키마 predicate·허용 델타 전수 열거·baseline 8값은 전부 레시피 하강 대상.
- 허용 델타 ⑥이 "2026-08-13 사용자 승인"으로 조건에 추가된 흔적 = 디테일 인라인이 실제로 goal 수정을 유발한 직접 증거.

## 토론 흐름 (Discussion Flow)
Round 1: goal drift 가드 → CONSTRAINT 한 줄 + diff surface (immutable·무가드 기각)
Round 2: 인라인/하강 판별 기준 → 재설정 litmus (카테고리 목록·글자수 상한 기각)
Round 3 (비판적 검토): 평가자 판정력 약화 → 최소 anchor 1-2개 유지 + 표준 레시피 참조 문구
Round 4: 델타 범위 확정 → 4개 델타, 단 litmus는 지침만(hard gate 추가 없음)

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 레시피가 goal.md로 내려가면 에이전트가 루프 중 약화 가능(goal drift). 어떻게 막을까?
**Options**: 1) CONSTRAINT 한 줄 + diff surface (Recommended) 2) 레시피 섹션 immutable 3) 가드 없이 SDD 리뷰 위임 4) 토론 종료
**A**: CONSTRAINT 한 줄 + diff surface
**Follow-up**: 평가자가 transcript에서 위반 관찰 가능, 레시피 적응은 goal 재설정 없이 가능 — 비용 최소.

### Round 2
**Q**: 조건 인라인 vs 레시피 하강의 판별 기준은?
**Options**: 1) 재설정 litmus (Recommended) 2) 카테고리 고정 목록 3) 글자수 상한 4) 토론 종료
**A**: 재설정 litmus
**Follow-up**: "어긋났을 때 goal을 다시 세우는 게 마땅한가"로 판별 — lmax16 사례에 적용해 잔류/하강 목록 도출.

### Round 3
**Q**: (비판적 검토) 레시피 전면 하강 시 평가자는 "PASS 주장"만 보게 됨. 판정력 약화를 어디까지 수용?
**Options**: 1) 최소 anchor 유지 (Recommended) 2) 순수 outcome만 3) 핵심 predicate 축소판 인라인 4) 토론 종료
**A**: 최소 anchor 유지
**Follow-up**: 위조 어려운 안정적 사실(절대경로·exit 0)만 인라인 + 표준 레시피 참조 문구로 판정력과 유연성 균형.

### Round 4
**Q**: 델타 범위 확인 — ① 템플릿 D10 3분법+레시피 섹션 ② SKILL.md Step 3 litmus+self-check 항목 ③ Codex 미러 ④ spec-sync?
**Options**: 1) 그 범위로 확정(항목은 hard gate) (Recommended) 2) self-check는 지침만 3) 범위 수정 필요
**A**: self-check는 지침만 (gate 아님)
**Follow-up**: litmus는 Step 3 판단 지침으로만 추가, hard gate 3항목은 불변으로 확정.
