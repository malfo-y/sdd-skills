# Feature Draft: 리뷰 스킬 correctness 행동 바닥(evidence floor)

> 규모 판정: 적격 — 변경 요소 3종(plan-review 규칙 2줄·implementation-review 보고 1줄) × claude/codex 미러 2짝, 요소↔task 1:1로 눈검산 가능.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
opus-4.8급 모델이 `plan-review`·`implementation-review`의 correctness 리뷰를 사실상 건너뛰는 원인 두 가지를 산문 규칙 수준에서 제거한다.

- `plan-review`: "근거가 부족하면 읽기를 확장하지 않고 finding을 만들지 않는다"가 **아무 대조도 하지 않은 채 CLEAR**를 내는 최저 비용 경로를 보상한다. **새 contract**: draft가 주장하는 외부 사실(Target Files 경로·content anchor·`[C]` 생성 사유의 전제·명시 인용 spec 절)은 전부 검색/읽기로 실재 대조하며, 이 대조가 끝난 뒤에만 근거 부족 판정과 finding 0이 허용된다. 그 대조 호출이 AC2의 판정 흔적이다. 읽기 확장 금지는 유지(대조는 draft가 지목한 대상에 한정 — 확장이 아님).
- `implementation-review`: 통과 AC를 `MET: AC1–AC5`로 접어 "증거 없는 MET 금지"가 외부에서 검증 불가하다. **새 contract**: 통과 AC는 AC당 증거 포인터 한 줄(`AC1 MET — file:line` 또는 실행 명령)로 낸다 — 전사가 아닌 포인터. main.md §3의 "ledger MET 접기" 계약은 implementation-review에 한해 포인터 형으로 완화된다 (`pr-review`의 `MET: #1–#N` 접기는 불변).

원칙: 순종에 기대는 산문(“점검 범위는 줄이지 않는다”)이 아니라 흔적이 남는 행동 바닥. 스크래치 파일·의사코드·새 AC 추가는 하지 않는다(Codex 호환·AC 체크박스 인플레이션 회피).

## Scope
- **In**: `.claude/skills/{plan-review,implementation-review}/SKILL.md` + `plugins/sdd-skills-codex/skills/{plan-review,implementation-review}/SKILL.md` 본문 규칙 개정, 미러 짝 동등성 검증
- **Out**: `pr-review` ledger 접기(인간 리뷰 보조 — 별도 판단), spec surface 갱신(`spec-sync` 단계), `_sdd/pipeline/` 실험 기록물, 효과 계측(플러그인 갱신 후 별도 세션에서만 유효 — [[plugin-cache-lag]])
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: plan-review에 외부 사실 대조 바닥 도입
"근거 부족 → finding 없음" 규칙에 선행 조건(draft가 지목한 외부 사실의 실재 대조)을 붙이고, AC2가 그 흔적을 판정하게 한다. 읽기 확장 금지는 그대로 둔다.

**Contracts**: 외부 사실 대조 = draft가 지목한 대상(Target Files 경로·content anchor·`[C]` 생성 사유의 전제·명시 인용 spec 절)을 검색/읽기로 실재 확인하는 것. 외부 사실에 의존하는 smell(Requirement Fit의 spec delta·Over-engineering의 `[C]`·Verification Weakness의 실측/anchor)은 이 대조 이후에만 finding 0 가능. draft 내부 판정 smell(Task Boundary Drift·Hidden Decision)은 도구 호출 흔적을 요구하지 않는다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): 두 파일 모두에서 `grep -c '근거가 부족하면 읽기를 확장하지 않고'` = 0 이고, 읽기 지침 절에 외부 사실 대조 선행 조건 문장이 존재한다 (`grep -n '외부 사실'` 각 1건 이상).
- [ ] AC2 (1등급): 두 파일의 `AC2:` 줄이 "외부 사실 대조 호출 흔적 + 5 smell 단일 패스"를 판정한다 — `grep -n '^- \[ \] AC2:'` 출력에 "대조" 문자열 포함.
- [ ] AC3 (1등급): claude 본문의 `` `Grep`/`Read` ``를 `검색/읽기`로 정규화한 뒤 codex 짝과 `diff`한 hunk가 기존 3개(서브에이전트/agent spawn 어휘 2곳·배칭/좌표 문장 어휘 1곳)와 같다 — 새 문장은 어휘 규칙만 적용해 동일 의미. (구현 중 계약 오류 선언 1회: 원안 "raw hunk 3개 유지"는 새 문장이 기존 hunk와 인접하지 않아 성립 불가.)

**Target Files**:
- [M] `.claude/skills/plan-review/SKILL.md` -- 읽기 지침 마지막 항목 + AC2
- [M] `plugins/sdd-skills-codex/skills/plan-review/SKILL.md` -- 동일 변경, codex 어휘

### Task 2: implementation-review 통과 AC를 포인터 한 줄로
`MET: AC1–AC5` 접기를 AC당 증거 포인터 한 줄로 바꿔 "증거 없는 MET 금지"를 보고에서 검증 가능하게 한다. 출력 다이어트는 포인터(전사 아님)로 유지.

**Contracts**: Verification ledger의 통과 항목 형식 = `AC<n> MET — <file:line | 실행 명령 1개>` 한 줄/AC. 증거 본문(출력·인용 문장)은 여전히 전사하지 않는다. NOT MET·UNTESTED 행 형식 불변.

**Acceptance Criteria**:
- [ ] AC1 (1등급): 두 파일 모두 `grep -c 'MET: AC1–AC5'` = 0, 보고 절 Verification ledger 항목에 `AC1 MET — ` 형식 예시 포함(`grep -n 'MET — '` 1건 이상).
- [ ] AC2 (2등급): AC3("증거 없는 MET 없음")이 보고의 포인터를 그 검증 근거로 지목한다 — AC3 줄에 "포인터" 문자열 포함(`grep -n '^- \[ \] AC3:.*포인터'`).
- [ ] AC3 (2등급): codex 짝 `diff`가 기존 delta(frontmatter·spawn 어휘·Codex Runtime Adapter 절·도구 어휘) 외 새 차이 없음.

**Target Files**:
- [M] `.claude/skills/implementation-review/SKILL.md` -- AC3 + 보고 절 Verification ledger 줄
- [M] `plugins/sdd-skills-codex/skills/implementation-review/SKILL.md` -- 동일 변경

### Task 3: 잔존 리터럴·미러 동등성 census (read-only)
전파형 변경이라 구 리터럴 잔존과 claude↔codex 어긋남을 전수로 닫는다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `grep -rn -F '근거가 부족하면 읽기를 확장하지 않고' .claude plugins docs` 와 `grep -rn -F 'MET: AC1–AC5' .claude plugins docs` 모두 0건 (`_sdd/`는 spec-sync 소관으로 제외).
- [ ] AC2 (1등급): `git diff --check` 무출력.
- [ ] AC3 (1등급): `diff` hunk 수가 기준선과 같다 — plan-review 3개(Task 1 AC3의 어휘 정규화 기준), implementation-review 14개(raw, 변경 전 실측); 초과 hunk 0.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- `pr-review`의 `MET: #1–#N` 접기도 같은 포인터 형으로 바꿀지 — 이번엔 Out(요청 범위 밖, 인간 보조 리뷰라 문제 관측 없음). 사용자 확인 불필요; 원하면 후속 1커밋.
