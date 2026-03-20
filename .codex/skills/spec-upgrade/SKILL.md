---
name: spec-upgrade
description: This skill should be used when the user asks to "upgrade spec", "convert spec to whitepaper", "migrate spec format", "spec upgrade", "스펙 업그레이드", "스펙 변환", "스펙 마이그레이션", "whitepaper 형식으로 변환", or wants to convert old-format spec documents to the whitepaper-style §1-§8 structure defined in SDD_SPEC_DEFINITION.md.
version: 1.7.0
---

# spec-upgrade

## Goal

기존 구형 스펙을 SDD whitepaper 스타일(§1-§8)로 업그레이드한다. 기존 내용을 최대한 보존하면서, 빠진 서사 섹션과 citation 구조를 보강하고 이후 스킬이 읽기 쉬운 형식으로 맞춘다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: canonical spec과 업그레이드 대상 파일 집합을 확정했다.
- [ ] AC2: §1-§8 gap analysis를 수행하고 결과를 먼저 보고했다.
- [ ] AC3: 기존 내용을 보존한 채 whitepaper 구조로 재배치/보강했다.
- [ ] AC4: 업그레이드 전 백업을 만들었다.
- [ ] AC5: 필요한 경우 code citation, usage guide, core design narrative를 보강했다.
- [ ] AC6: 멀티파일 spec이면 index와 하위 파일 역할이 더 명확해졌다.

## SDD Lens

- spec-upgrade는 “내용 삭제”보다 “형식과 서사 보강”에 가깝다.
- 코드베이스가 있다면 whitepaper의 why/how를 보강하는 근거로 사용한다.
- 구조 재편이 더 큰 문제라면 무리하게 여기서 해결하지 말고 `spec-rewrite` 후보로 돌린다.

## Companion Assets

- `references/spec-format.md`
- `references/template-compact.md`
- `references/template-full.md`
- `references/upgrade-mapping.md`
- `examples/before-upgrade.md`, `examples/after-upgrade.md`

## Hard Rules

1. 구현 코드 파일은 수정하지 않는다.
2. 기존 스펙 언어를 따른다.
3. 기존 내용을 최대한 보존하고, 삭제가 필요하면 이유를 명시한다.
4. 업그레이드 전 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
5. Step 3 checkpoint 없이 바로 덮어쓰지 않는다.
6. 결과는 기존 파일 경로에 in-place로 반영한다. 구조 재편이 필요하면 `spec-rewrite` 후보로 보고한다.
7. `DECISION_LOG.md`가 있으면 보존하고, 주요 업그레이드 판단을 추가 기록할 수 있다.
8. 장문 업그레이드는 먼저 `write_skeleton` agent로 skeleton을 만든다. 반환값이 `SKELETON_ONLY`이면 이 skill이 `default` 또는 `worker` agent로 남은 섹션을 채운다.

## Process

### Step 1: Gap Analysis

기존 스펙을 읽고 아래를 진단한다.

- canonical spec 후보
- split spec 여부
- §1~§8 존재/부족 상태
- whitepaper에 필요한 서사 섹션 부족분
- code citation 존재 여부

### Step 2: Code Analysis

코드베이스가 있으면 빠진 섹션을 보강하기 위한 근거를 수집한다.

- README / docs / git history → background & motivation
- 핵심 엔트리포인트 / 주요 로직 → core design
- 사용 흐름 / API / 테스트 → usage guide, API reference
- 주요 파일/심볼 → citation candidates

코드가 없으면 기존 문서와 프로젝트 설명만으로 계속 진행한다.

### Step 3: Checkpoint

아래를 사용자에게 먼저 보고한다.

- 기존 스펙 현황
- §1~§8 gap 분석
- 보강 방향
- 구조 재편 필요 여부

canonical file 결정이 약하거나 rewrite가 더 적절해 보이면 여기서만 짧게 확인한다.

### Step 4: Backup and Upgrade

- 대상 파일 백업
- 기존 내용을 §1~§8에 재배치
- 빠진 §1, §2, §5 같은 서사 섹션 보강
- 멀티파일이면 index와 서브 파일 역할을 유지하면서 보강
- code citation / reference index를 가능한 범위에서 정리

장문 업그레이드는 다음 순서를 따른다.

1. `write_skeleton` agent로 대상 파일 skeleton 생성
2. 반환값이 `COMPLETE`면 그대로 사용
3. 반환값이 `SKELETON_ONLY`면 이 skill이 `Sections Remaining`을 기준으로 fill 수행
4. 의존 섹션은 `default`, 독립 파일/섹션은 `worker`로 채운다

멀티파일일 때:

- top-level canonical spec을 먼저 업그레이드
- component 파일은 겹치지 않는 범위로 나눠 보강
- 부모가 cross-file link와 citation 일관성을 정리

### Step 5: Validate

아래를 확인한다.

- §1~§8 구조가 유지되는가
- 기존 정보가 불필요하게 소실되지 않았는가
- 보강된 서사와 citation이 근거를 가지는가
- rewrite가 필요한 구조적 문제를 잘못 업그레이드로 덮지 않았는가

## Output Contract

기본 산출물:

- upgraded spec files in place

조건부 산출물:

- `_sdd/spec/DECISION_LOG.md` 업데이트

최종 보고에는 아래가 포함되어야 한다.

- 업그레이드 대상 파일
- §1~§8 gap과 조치
- 추가/보강된 narrative/citation 영역
- 남은 구조 문제와 후속 추천

## Error Handling

| 상황 | 대응 |
|------|------|
| spec 없음 | `/spec-create` 먼저 권장 |
| 이미 whitepaper에 가까움 | 부족한 섹션만 보강 |
| canonical 후보 다수 | checkpoint에서 확인 |
| 코드베이스 없음 | 문서 기반 업그레이드로 진행하고 근거 수준을 명시 |
| 구조 재편이 핵심 문제 | `spec-rewrite` 후보로 보고 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
