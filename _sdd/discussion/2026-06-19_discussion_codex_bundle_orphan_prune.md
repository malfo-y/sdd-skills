# 토론 요약: codex 번들 설치 스크립트의 orphan 정리(delete 부재) 해결

**날짜**: 2026-06-19
**라운드 수**: 3
**참여 방식**: 구조화된 토론 (discussion skill)

## 토론 배경 및 초기 콘텍스트 (Background / Initial Context)
- **사용자 문제 제기**: `tools/install-codex-skill-bundle.py`가 codex 스킬/agent를 add/replace만 하고 **delete를 못 한다**. spec-update-todo/done → spec-sync 머지처럼 스킬을 제거/rename하면, 구 스킬이 `~/.codex/skills`·`~/.codex/agents` 아래 orphan으로 영구 잔존한다.
- **토론을 시작한 배경**: 직전에 완료한 spec-sync 머지(spec-update-todo/done 삭제)가 marketplace plugin에는 반영됐으나, codex 번들 설치 경로에는 구 스킬을 지울 메커니즘이 없어 후속 정리 설계가 필요해짐.
- **현재 상태(코드 확인)**: 스크립트는 매 설치 때 source repo의 `.codex/skills/<name>/SKILL.md` 전부와 `.codex/agents/*.toml` 전부를 `_discover_skills`/`_discover_agents`로 발견해 dest에 copy/replace한다. dest에만 있고 source에 없는 항목은 절대 건드리지 않는다. `--dry-run`·`--force` 플래그는 이미 존재. → **매 설치 시 "설치해야 할 권위 목록"이 이미 계산된다**는 점이 핵심.
- **범위**: install 스크립트의 orphan 정리(prune) 설계. **제외**: marketplace plugin 경로(이미 별도 해결), 구현 자체(이 토론은 설계까지).
- **수집한 근거**: 스크립트 전문 정독, repo `.codex/skills/*`·`.codex/agents/*` 키워드 census.

## 핵심 논점 (Key Discussion Points)
1. **Ownership 식별 모델**: "삭제해도 안전한 대상(번들 소유)"을 무엇으로 식별하나 — 키워드 / manifest / retired-list.
2. **키워드 휴리스틱의 실측 위험**: false-negative(키워드 없는 번들 스킬)·false-positive(사용자 자작 SDD-언급 스킬).
3. **Bootstrap**: manifest가 아직 없는 첫 설치에서 이미 orphan된 spec-update-todo/done을 어떻게 정리하나.

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 (유형) | 관련 논점 |
|---|------|------------|----------|
| 1 | **prune 메커니즘은 설치 manifest 정확 추적**. 설치 시 번들이 설치한 이름을 dest manifest에 기록 → prune = (이전 manifest) − (이번 source). 키워드는 false-positive 안전필터로 강등 | `사용자 판단` (Q2). 변경 이력: 초기 Q1에서 "키워드를 ownership 모델로" 선택했으나, write-phased false-negative 실측 후 manifest로 **supersede**됨 | 1, 2 |
| 2 | **false-negative는 manifest가 정확 추적으로 해소**. 키워드 없는 번들 스킬(write-phased류)도 manifest에 기록되므로 제거 시 정확히 잡힘 | `사용자 판단` (Q2) + `코드 확인`(write-phased가 `_sdd`/`SDD` 키워드 없음을 grep으로 확인) | 2 |
| 3 | **Bootstrap = 키워드 1회 채택 + 이후 manifest**. 첫 실행(manifest 없음)은 키워드+source-absence로 SDD orphan 후보 제시 → 확인 삭제 + manifest 생성. 이후부터 manifest가 정확 인계 | `사용자 판단` (Q3). 키워드를 "딱 한 번, 확인과 함께"만 쓰는 가장 안전한 지점 | 3 |

> 근거 유형: `코드 확인`/`외부 자료`/`사용자 판단`/`미검증 가정`. 결정 1은 Q1(키워드)→Q2(manifest) 재방문(3.3.1)으로 변경됨 — write-phased 실측이 키워드 단독의 전제를 무너뜨림.

### 합의된 설계 세부 (맥락에서 도출한 sensible default — 구현 시 확정)
- prune 후보 규칙: `dest에 있음 AND 이번 source에 없음 AND (manifest 기록 OR [bootstrap 시] 키워드 매치)`.
- prune은 **기본 활성**(`사용자 판단`, 2026-06-19 추가 결정). opt-out `--no-prune` 제공.
- **확인 게이트 필수**(삭제 전 후보 목록 제시) + 기존 `--dry-run`과 통합.
- **비대화형(non-tty) 가드**: stdin이 tty가 아니면(CI·파이프) 확인을 못 받으므로 prune을 자동 보류하고 경고한다(또는 `--prune-yes` 명시 요구). 기본 활성이 무인 환경에서 무확인 삭제로 가지 않게 하는 안전장치.
- manifest 위치: `CODEX_HOME`(`~/.codex/`) 아래. 스킬 dir 이름 + agent toml 이름 기록.
- 실패 방향은 안전하게: 불확실하면 삭제하지 않고 잔존(오삭제 < 잔존).

## 기각한 대안
- **순수 키워드 휴리스틱(Q1 초안)**: false-negative(write-phased 실증)·false-positive 위험으로 ownership 모델 자리에서 manifest에 밀림. 단 **bootstrap 1회용**으로는 채택(결정 3).
- **repo retired-list**: 명시적·정확하나 제거 시마다 maintainer 수동 등록 규율 필요. manifest가 자기유지(self-maintaining)라 우선. bootstrap 대안으로도 키워드 채택에 밀림.

## 미결 질문 (Open Questions)
| # | 질문 | 카테고리 | 맥락 / 의존 |
|---|------|----------|-------------|
| 1 | manifest 정확 파일명·포맷(JSON 키 구조) | deferred-deliberately | 구현 시 확정. 설계 방향은 합의됨 |
| 2 | `--prune` 플래그 이름·확인 UX 세부 문구 | deferred-deliberately | 구현 시 확정 |
| 3 | 여러 SDD 번들 공존 시 manifest 네임스페이싱 | out-of-scope | 현재 단일 번들. 다번들은 별도 토론 |

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | `install-codex-skill-bundle.py`에 manifest 추적 기반 prune 구현(키워드 bootstrap + 확인 게이트 + `--prune` opt-in + `--dry-run` 연동) | High | 후속 구현 |
| 2 | 첫 prune 실행으로 현재 orphan(spec-update-todo/done) `~/.codex` 정리 | Medium | 위 구현 후 |

### 후속 핸드오프 (Handoff)
- **목표**: codex 번들 설치 시 source에서 제거된 스킬/agent가 `~/.codex`에 orphan으로 남지 않는다. 첫 실행은 키워드+확인으로 기존 orphan을 정리하고 manifest를 생성하며, 이후 설치는 manifest diff로 정확히 prune한다.
- **변경 금지 제약**: 기존 add/replace 동작·`--dry-run`·`--force` 의미 보존. prune은 opt-in이라 기본 동작 불변. 번들 소유가 아닌(manifest·키워드 미해당) 사용자 스킬은 절대 삭제 금지.
- **검증**: dry-run으로 후보 목록 확인 → 확인 게이트 → 삭제 후 manifest 갱신 확인. spec-update-todo/done이 `~/.codex`에서 제거되고 무관 스킬은 잔존하는지 수동 시나리오.
- **중단 조건**: 후보에 번들 무관으로 보이는 사용자 스킬이 다수 잡히면 중단·보고(키워드 오탐 신호).

## 리서치 결과 요약 (Research Findings)
- `코드 확인`: 스크립트는 매 설치 때 권위 source 목록(`discovered`)을 이미 계산 → orphan 판정에 키워드 불필요, source-difference로 정확.
- `코드 확인`: repo `.codex/skills/` 19개 중 **write-phased만 `_sdd`/`SDD` 키워드 없음** → 키워드 단독의 false-negative가 실재함을 실증(결정 1·2의 근거).

## 토론 흐름 (Discussion Flow)
- Round 1 (Q1): ownership 모델 → 키워드 휴리스틱 선택 (이후 supersede됨)
- Round 2 (Q2, 비판적 검토): write-phased false-negative 실측 제시 → **manifest 정확 추적**으로 전환
- Round 3 (Q3): bootstrap 처리 → **키워드 1회 채택 + 이후 manifest**로 수렴

## 부록: 대화 로그 (Conversation Log)
### Round 1
**Q**: 삭제 안전 대상(번들 소유) 식별 — 어느 ownership 모델?
**Options**: 1) 로컬 manifest 2) repo retired-list 3) 키워드 휴리스틱 / 토론 종료
**A**: 키워드 휴리스틱(형님 초안)
**Follow-up**: 키워드 false-negative 실측 필요 → 비판적 검토로 진행

### Round 2
**Q**: write-phased가 드러낸 false-negative를 어떻게 처리?
**Options**: 1) retired-list 백스톱 2) 키워드만 누락 감수 3) 설치 manifest 정확 추적 / 토론 종료
**A**: 설치 manifest로 정확 추적 → 결정 1 재방문(키워드 supersede)
**Follow-up**: manifest의 bootstrap 갭이 마지막 쟁점으로 부상

### Round 3
**Q**: manifest 없는 첫 설치에서 기존 orphan(spec-update-todo/done) 처리?
**Options**: 1) 키워드 1회 채택+이후 manifest 2) retired-list 1회 3) 수동 rm 1회 / 토론 종료
**A**: 키워드 1회 채택 + 이후 manifest
**Follow-up**: 핵심 3결정 수렴 → API 에러 보고로 토론 정리
