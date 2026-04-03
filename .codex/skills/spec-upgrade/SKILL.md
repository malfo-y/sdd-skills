---
name: spec-upgrade
description: This skill should be used when the user asks to "upgrade spec", "migrate spec format", "modernize spec structure", "spec upgrade", "스펙 업그레이드", "스펙 변환", "스펙 마이그레이션", or wants to convert old-format spec documents to the current canonical SDD spec model defined in SDD_SPEC_DEFINITION.md.
version: 1.8.0
---

# spec-upgrade

## Goal

기존 구형 스펙을 현재 SDD canonical global spec model로 마이그레이션한다. 기존의 유효한 내용은 최대한 보존하되, old section-map 및 inventory-heavy 가정을 제거하고, 얇은 글로벌 스펙 + explicit CIV + decision-bearing structure + appendix-level strategic code map 모델로 재구성한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: canonical spec과 업그레이드 대상 파일 집합을 확정했다.
- [ ] AC2: 현재 문서를 새 canonical model 기준으로 gap 분석하고 결과를 먼저 보고했다.
- [ ] AC3: 기존 내용을 보존 가능한 범위에서 새 global spec structure로 재배치/보강했다.
- [ ] AC4: 업그레이드 전 백업을 만들었다.
- [ ] AC5: `Contract / Invariants / Verifiability`, `Decision-bearing structure`, `Usage Guide & Expected Results`가 필요한 수준으로 추가 또는 보강되었다.
- [ ] AC6: 단순 implementation inventory는 줄이고, 정말 필요한 경우에만 appendix-level strategic code map으로 남겼다.
- [ ] AC7: 멀티파일 spec이면 index와 supporting file의 역할이 더 명확해졌다.
- [ ] AC8: `AGENTS.md`, `CLAUDE.md`가 존재한다 (미존재 시 생성)

## SDD Lens

- spec-upgrade는 old section map을 current canonical model로 옮기는 마이그레이션이다.
- global spec은 얇은 기준 문서다. temporary spec은 별도의 실행 청사진이다.
- `Contract / Invariants / Verifiability`는 명시적으로 복구해야 하는 필수 축이다.
- architecture/component detail은 decision-bearing structure 또는 reference information으로 재배치한다.
- strategic code map은 manual curated appendix가 기본값이다.
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
3. 기존 내용을 최대한 보존하고, 삭제 또는 축약이 필요하면 이유를 명시한다.
4. 업그레이드 전 `_sdd/spec/prev/prev_<filename>_<timestamp>.md`로 백업한다.
5. canonical file 결정이 불안정하지 않다면 불필요한 checkpoint로 멈추지 않는다.
6. 결과는 기존 파일 경로에 in-place로 반영한다. 구조 재편이 너무 크면 `spec-rewrite` 후보로 보고한다.
7. `decision_log.md`가 있으면 보존하고, 주요 업그레이드 판단을 추가 기록할 수 있다.
8. 장문 업그레이드는 caller가 먼저 skeleton/섹션 헤더를 직접 기록한 뒤, 같은 흐름에서 내용을 채운다.
9. strategic code map은 appendix-level hint로만 추가한다. 전수형 파일 inventory를 만들지 않는다.

## Process

### Step 1: Legacy-to-Canonical Gap Analysis

기존 스펙을 읽고 아래를 진단한다.

- canonical spec 후보
- split spec 여부
- 새 global spec core 존재/부족 상태
- CIV 부재 여부
- implementation inventory 과잉 여부
- appendix로 내릴 수 있는 참조 정보
- temporary spec 성격의 내용이 글로벌 스펙에 잘못 섞여 있는지 여부

### Step 2: Evidence Collection

코드베이스가 있으면 빠진 섹션을 보강하기 위한 근거를 수집한다.

- README / docs / git history -> background / concept / scope
- 핵심 엔트리포인트 / 주요 로직 -> core design, decision-bearing structure
- 테스트 / examples / usage docs -> usage guide, expected results
- 주요 파일/심볼 -> strategic code map candidates

코드가 없으면 기존 문서와 프로젝트 설명만으로 계속 진행한다.

### Step 3: Migration Checkpoint

아래를 먼저 정리한다.

- 기존 스펙 현황
- 새 canonical model gap 분석
- 보강 방향
- 구조 재편 필요 여부

canonical file 결정이 약하거나 rewrite가 더 적절해 보일 때만 짧게 확인한다.

### Step 4: Backup and Migrate

- 대상 파일 백업
- 기존 내용을 새 global spec structure로 재배치
- missing CIV를 보강
- usage / expected results를 보강
- implementation inventory를 decision-bearing structure 또는 reference information으로 정리
- truly useful code navigation만 appendix strategic code map으로 남김

장문 업그레이드는 다음 순서를 따른다.

1. 대상 파일 skeleton/섹션 헤더를 직접 작성
2. 같은 흐름에서 변환 내용을 채움
3. TODO/placeholder를 제거하고 finalize
4. 의존 섹션은 `default`, 독립 파일/섹션은 `worker`로 채운다

멀티파일일 때:

- top-level canonical spec을 먼저 업그레이드
- supporting files는 reference information 또는 domain reference 역할로 재배치
- 부모가 cross-file link와 section responsibility를 정리

#### 4.5 Workspace Guidance 파일 보충

구 버전 SDD에서는 `CLAUDE.md`, `AGENTS.md`가 없을 수 있다. 미존재 시 생성:

1. `AGENTS.md` 미존재 -> 생성:
   ```markdown
   # Workspace Guidance
   - 프로젝트 스펙 문서는 `_sdd/spec/`를 기준으로 확인합니다. 프로젝트 내 기능이나 구현을 확인하고 수정할 때는 관련된 스펙 문서를 함께 읽고 참조합니다.
   - 환경 관련 설정/실행 방법은 `_sdd/env.md`를 기준으로 확인합니다. 의존성 설치, 테스트 스크립트 실행 등의 작업 시 이 파일을 참조합니다.
   ```
2. `CLAUDE.md` 미존재 -> 동일 문구로 생성
3. 이미 존재하면 스킵

### Step 5: Validate

아래를 확인한다.

- global spec core가 유지되는가
- 기존 정보가 불필요하게 소실되지 않았는가
- CIV와 사용 시나리오가 실제 근거를 가지는가
- implementation inventory를 그대로 옮겨 적지 않았는가
- strategic code map이 appendix-level hint로 유지되는가
- rewrite가 필요한 구조적 문제를 잘못 업그레이드로 덮지 않았는가

## Output Contract

기본 산출물:

- upgraded spec files in place

조건부 산출물:

- `_sdd/spec/decision_log.md` 업데이트

최종 보고에는 아래가 포함되어야 한다.

- 업그레이드 대상 파일
- current canonical model gap과 조치
- 추가/보강된 CIV / decision-bearing structure / usage 영역
- 축약 또는 appendix 이동된 old implementation inventory 항목
- 남은 구조 문제와 후속 추천

## Error Handling

| 상황 | 대응 |
|------|------|
| spec 없음 | `/spec-create` 먼저 권장 |
| 이미 current canonical model에 가까움 | 부족한 항목만 보강 |
| canonical 후보 다수 | migration checkpoint에서 확인 |
| 코드베이스 없음 | 문서 기반 업그레이드로 진행하고 근거 수준을 명시 |
| 구조 재편이 핵심 문제 | `spec-rewrite` 후보로 보고 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
