# 토론 요약: 두 단계 스펙 구조 컨셉 설명 방안

**날짜**: 2026-03-06
**라운드 수**: 5
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)
1. **컨셉 프레이밍**: 글로벌 스펙이 CLAUDE.md를 "대체"한다는 표현이 적절한지 → "대체"로 확정
2. **비유 선택**: 두 단계 구조를 외부 사용자에게 설명할 비유 → Git 브랜치 비유 채택
3. **문서 배치**: 독립 문서 vs WORKFLOW 내 서브섹션 → 독립 문서(`SDD_CONCEPT.md`) + WORKFLOW/QUICK_START에 핵심 요약 및 링크

## 결정 사항 (Decisions Made)
| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | 글로벌 스펙 = CLAUDE.md **대체** | CLAUDE.md는 `_sdd/spec/`를 가리키는 포인터 역할만 하고, 글로벌 스펙이 실질적인 프로젝트 설계/아키텍처/요구사항 문서 | 컨셉 프레이밍 |
| 2 | Git 브랜치 비유 사용 | main 브랜치=글로벌 스펙, feature branch=임시 스펙, PR 머지=병합 — 개발자에게 직관적 | 비유 선택 |
| 3 | 독립 문서 `SDD_CONCEPT.md` 생성 | 상세 설명은 독립 문서에, WORKFLOW에는 핵심만 추려서 링크 | 문서 배치 |
| 4 | 문서 구성 4섹션 | SDD란?, 두 단계 구조, 임시 스펙 생명주기, 스펙 파일 구분 | 문서 범위 |
| 5 | 한국어로 작성 | 기존 가이드 문서(WORKFLOW, QUICK_START)와 일관성 유지 | 문서 언어 |

## 미결 질문 (Open Questions)
- (없음)

## 실행 항목 (Action Items)
| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | `SDD_CONCEPT.md` 작성 (4섹션: SDD란?, 두 단계 구조, 생명주기, 파일 구분) | High | - |
| 2 | `SDD_WORKFLOW.md` 1장에 두 단계 구조 핵심 요약 + `SDD_CONCEPT.md` 링크 추가 | High | - |
| 3 | `SDD_QUICK_START.md`에 한 줄 요약 + 링크 추가 | Medium | - |

## 리서치 결과 요약 (Research Findings)
- 현재 두 단계 구조는 기술적으로 잘 구현되어 있으나, "왜 이 구조인가"와 "글로벌 스펙이 CLAUDE.md를 대체한다"는 컨셉이 명시적으로 설명된 곳이 없음
- 임시 스펙의 생명주기 설명이 각 SKILL.md에 분산되어 통합 설명 부재
- feature-draft, spec-update-todo, pr-spec-patch 모두 "스펙 파일은 read-only"라고 명시하지만, 그 이유(변경 추적, 사용자 검증 등)는 설명하지 않음

## 토론 흐름 (Discussion Flow)
Round 1: 토픽 확인 → 컨셉 + 온보딩 양쪽 모두 논의
Round 2: 컨셉 프레이밍 확인 → "대체"가 적절한 표현으로 확정
Round 3: 비유 선택 → Git 브랜치 비유 채택
Round 4: 문서 배치 → 독립 문서 + WORKFLOW 핵심 요약 + 링크
Round 5: 문서 구성 및 언어 → 4섹션, 한국어로 확정
