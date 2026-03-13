# 토론 요약: 화이트페이퍼 스타일 스펙 진화 — 미결 질문 해결

**날짜**: 2026-03-13
**라운드 수**: 13
**참여 방식**: 구조화된 토론 (discussion skill)
**선행 토론**: `discussion_spec_as_whitepaper.md`

## 핵심 논점 (Key Discussion Points)

1. **실행 방안**: spec-create v2 직접 진화 vs feature-draft 정식 플로우 vs 하이브리드. 스킬 자체 변경에 정식 플로우는 과하다는 판단.
2. **코드 스니펫 drift 대조**: 기존 8가지 드리프트 패턴에 9번째 "Code Snippet Drift" 추가. 함수명 기반 검색 + 해시 비교.
3. **기존 스펙 마이그레이션**: 강제 변환 없이 spec-update-done 시 자연스럽게 누락 섹션 보강 제안.
4. **코드 발취 깊이**: 30줄 기준 — 이하는 전체 발취, 초과 시 시그니처 + 핵심 로직만.
5. **인라인 citation 형식**: `[filepath:functionName]` — 논문의 `[Author, Year]`에 대응. AI 파싱 가능.
6. **플랫폼 동기화**: .claude와 .codex 동시 적용. template-full.md 동일, SKILL.md는 플랫폼 차이만 반영.
7. **구현 우선순위**: A(spec-create 템플릿 진화) + B(spec-update-done 드리프트 패턴) + C(spec-rewrite 화이트페이퍼 보존) 함께. D(summary-template) + E(예시 스펙)는 후속.
8. **spec-rewrite 기능 결합**: 기존 정리 기능(prune/split/deduplicate) 유지. 정리 과정에서 화이트페이퍼 성질을 깨뜨리지 않도록 보존 규칙 추가.
9. **화이트페이퍼 보호 수준**: 기존 섹션 보존 + 누락 섹션 REWRITE_REPORT 경고. 자동 보강은 하지 않음 (그건 spec-create의 역할).
10. **포맷 정의 위치**: `references/spec-format.md` 새 파일로 화이트페이퍼 포맷 정의 포함. spec-create의 template-full.md와 독립적 self-contained 파일.
11. **spec-format.md 내용 범위**: 섹션 구조(§1~§8) + 보존 규칙(인라인 citation, 코드 발취 30줄 규칙)만. 생성 템플릿이 아닌 체크리스트 성격.
12. **구현 범위 확장**: A+B에서 A+B+C로 확장. spec-create/spec-update-done/spec-rewrite 세 스킬을 한 번에 진화.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | 하이브리드 실행: discussion 결과 기반 직접 수정 + 변경 범위 문서 먼저 작성 | 스킬 자체 변경에 정식 SDD 플로우는 과함. 변경 범위만 문서화하면 충분 | 논점 1 |
| 2 | Code Snippet Drift를 9번째 드리프트 패턴으로 drift-patterns.md에 추가 | 기존 8개 패턴 구조에 자연스럽게 통합. 함수명 기반 검색 + 해시 비교로 구현 | 논점 2 |
| 3 | 점진적 마이그레이션: spec-update-done 시 누락 섹션 보강 제안 | 강제 변환은 리스크. 자연스러운 업데이트 사이클에서 보강이 더 안전 | 논점 3 |
| 4 | 길이 기반 코드 발취 규칙: 30줄 이하 전체, 초과 시 시그니처 + 핵심 로직 | 명확하고 일관적인 기준. 드리프트 관리 부담과 AI 인덱싱 정확도의 균형 | 논점 4 |
| 5 | 인라인 citation: `[filepath:functionName]` 형식 | 논문 `[Author, Year]` 패턴 대응. AI가 직접 파싱하여 코드 위치 추적 가능 | 논점 5 |
| 6 | .claude와 .codex 동시 적용 | template-full.md는 플랫폼 무관 동일. 한쪽만 업데이트하면 divergence 발생 | 논점 6 |
| 7 | 1차 구현 범위: A+B+C (spec-create 진화 + drift 패턴 + spec-rewrite 보존) | 세 스킬이 화이트페이퍼 포맷을 공유하므로 함께 구현이 일관성 있음 | 논점 7, 12 |
| 8 | spec-rewrite: 기존 기능 유지 + 화이트페이퍼 보존 규칙 추가 | 정리 도구의 본질은 유지. 진화가 아닌 보존이 역할 | 논점 8 |
| 9 | spec-rewrite: 누락 섹션은 REWRITE_REPORT에 경고 표기 (자동 보강 안 함) | 자동 보강은 spec-create 역할. spec-rewrite는 보존 + 경고까지만 | 논점 9 |
| 10 | spec-rewrite: references/spec-format.md 새 파일로 포맷 정의 | self-contained 요구사항 충족. spec-create template-full.md와 독립 | 논점 10 |
| 11 | spec-format.md: 섹션 구조 + 보존 규칙만 (체크리스트 성격) | 생성 템플릿이 아닌 "이런 섹션이 있어야 한다"는 참조 문서 | 논점 11 |
| 12 | 구현 범위 A+B → A+B+C 확장 | spec-format.md는 spec-create template-full.md 진화와 연동되므로 함께 | 논점 12 |

## 미결 질문 (Open Questions)

없음. 이전 토론(`discussion_spec_as_whitepaper.md`)의 4개 미결 질문이 모두 해결됨.

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | spec-create 템플릿 진화: template-full.md에 §1 배경/동기, §2 핵심 설계, §5 사용 가이드 & 기대 결과 섹션 추가 + SKILL.md에 코드 발취/인라인 citation 규칙 추가 (.claude + .codex 동시) | High | 즉시 |
| 2 | spec-update-done drift-patterns.md에 9번째 "Code Snippet Drift" 패턴 추가 + SKILL.md에 스니펫 drift 감지 프로세스 반영 (.claude + .codex 동시) | High | 즉시 |
| 3 | spec-rewrite에 화이트페이퍼 보존 규칙 추가: references/spec-format.md 생성 + SKILL.md Step 4에 보존 규칙 추가 + rewrite-checklist.md에 화이트페이퍼 체크 추가 + REWRITE_REPORT에 누락 섹션 경고 (.claude + .codex 동시) | High | 즉시 |
| 4 | summary-template.md 새 섹션 반영 + 예시 스펙 업데이트 | Medium | 후속 |

## 리서치 결과 요약 (Research Findings)

- **spec-create 현재 구조**: 3단계 프로세스 (정보 수집 → 프로젝트 분석 → 부트스트랩 + 스펙 작성). template-full.md에 16개 섹션 있으나 배경/동기, 핵심 설계, 사용 가이드 & 기대 결과 부재.
- **spec-update-done 현재 구조**: 6단계 프로세스 + 8가지 드리프트 패턴. Source 필드 하이브리드 업데이트 있으나 임베디드 코드 스니펫 drift 감지 없음.
- **feature-draft 구조**: 7단계 프로세스, `_sdd/drafts/`에 출력, spec-update-todo 호환 마커 내장.
- **기존 스펙**: `_sdd/spec/sdd_skills.md` (14개 스킬 문서화, 구 포맷).
- **spec-rewrite 현재 구조**: 7단계 프로세스 (진단 → 계획 → 백업 → 정리 → 분할 → 모호성 보고 → 검증). "정리와 재구성" 중심. 이상적 포맷 기준 없이 기존 스펙의 구조만 개선. spec-create의 template-full.md 참조 없음 (완전 독립). references/rewrite-checklist.md + examples/rewrite-report.md 보유.

## 토론 흐름 (Discussion Flow)

Round 1: [실행 방안] → 하이브리드 (discussion 결과 기반 직접 수정 + 변경 범위 문서)
Round 2: [코드 스니펫 drift 대조 방식] → 9번째 드리프트 패턴으로 추가
Round 3: [기존 스펙 마이그레이션 전략] → 점진적 (spec-update-done 시 보강 제안)
Round 4: [코드 발취 깊이 기준] → 30줄 기준 길이 기반 규칙
Round 5: [인라인 citation 형식] → `[filepath:functionName]`
Round 6: [플랫폼 동기화] → .claude + .codex 동시 적용
Round 7: [구현 범위 우선순위] → A+B 먼저 (핵심만)
Round 8: [마무리 확인] → 토론 종료 (미결 질문 해결 완료)
Round 9: [spec-rewrite 기능 결합 방식] → 기존 유지 + 화이트페이퍼 보존 규칙 추가
Round 10: [화이트페이퍼 보호 수준] → 보존 + 누락 경고 (REWRITE_REPORT)
Round 11: [포맷 정의 위치] → references/spec-format.md 새 파일 (self-contained)
Round 12: [spec-format.md 내용 범위] → 섹션 구조 + 보존 규칙만 (체크리스트 성격)
Round 13: [구현 범위 재확인] → A+B+C 함께 → 토론 종료

## 부록: 대화 로그 (Conversation Log)

### Round 1
**Q**: 화이트페이퍼 스타일 스펙 진화를 어떤 방식으로 실행하고 싶으신가요?
**Options**: 1) spec-create 직접 수정 (권장) 2) feature-draft 정식 플로우 3) 하이브리드: discussion 결과로 직접 수정 4) 토론 종료
**A**: 하이브리드: discussion 결과로 직접 수정
**Follow-up**: 토론 결과를 기반으로 직접 수정하되, 변경 전 feature-draft 수준의 변경 범위 문서를 먼저 작성하는 방향 확정

### Round 2
**Q**: 스펙에 임베드된 코드 스니펫과 실제 코드의 드리프트를 어떻게 감지할까요?
**Options**: 1) 함수/클래스명 기반 검색 2) 코드 블록 + 파일경로 매핑 3) 9번째 드리프트 패턴으로 추가 4) 토론 종료
**A**: 9번째 드리프트 패턴으로 추가
**Follow-up**: 기존 drift-patterns.md의 8가지 패턴 구조에 Code Snippet Drift를 자연스럽게 통합. 함수명 기반 검색 + 해시 비교로 변경 감지.

### Round 3
**Q**: 기존 스펙들의 마이그레이션 전략을 어떻게 할까요?
**Options**: 1) 점진적 마이그레이션 (권장) 2) 일괄 마이그레이션 스크립트 3) 무시 (새 스펙만 적용) 4) 토론 종료
**A**: 점진적 마이그레이션
**Follow-up**: 기존 스펙은 그대로 두고, 다음 spec-update-done 시 누락 섹션(§1, §2, §5) 보강 제안. 강제 변환 없음.

### Round 4
**Q**: 스펙에 임베드할 코드 발취의 깊이 기준을 어떻게 정할까요?
**Options**: 1) 시그니처 + 핵심 로직만 2) 함수 전체 발취 3) 길이 기반 규칙 (예: 30줄 이하 전체, 초과 시 요약) 4) 토론 종료
**A**: 길이 기반 규칙 (30줄 이하 전체, 초과 시 요약)
**Follow-up**: 명확하고 일관적 기준. 드리프트 관리 부담과 AI 인덱싱 정확도의 균형점.

### Round 5
**Q**: 스펙 본문에서 코드를 참조할 때 인라인 citation 형식을 어떻게 할까요?
**Options**: 1) 파일경로:함수명 2) 파일경로:라인번호 3) 파일경로:함수명:라인 4) 토론 종료
**A**: 파일경로:함수명
**Follow-up**: `[src/payment/processor.ts:validatePayment]` 형식. 논문 `[Author, Year]` 패턴 대응. 라인번호는 drift 위험이 높아 제외.

### Round 6
**Q**: spec-create의 화이트페이퍼 진화를 .claude와 .codex 양쪽에 동시 적용할까요?
**Options**: 1) 동시 적용 (권장) 2) Claude Code 먼저, Codex 나중에 3) template-full.md만 공유 4) 토론 종료
**A**: 동시 적용
**Follow-up**: template-full.md는 플랫폼 무관 동일. SKILL.md만 각 플랫폼 차이(rg→Grep 등) 반영.

### Round 7
**Q**: 구현 범위를 어떻게 나눌까요?
**Options**: 1) A+B 먼저 (핵심만) 2) A+B+C 함께 3) A+B+C+D 전체 4) 토론 종료
**A**: A+B 먼저 (핵심만)
**Follow-up**: spec-create 템플릿 진화 + spec-update-done 드리프트 패턴 추가가 1차. summary-template과 예시 스펙은 후속.

### Round 8
**Q**: 추가 논의 사항이 있나요?
**Options**: 1) 토론 종료 / 정리해줘 2) 추가 논의 사항 있음 3) 바로 구현으로 넘어가자
**A**: 토론 종료 / 정리해줘

---

### Round 9 (spec-rewrite 추가 토론)
**Q**: spec-rewrite에 화이트페이퍼 포맷 진화 기능을 추가할 때, 기존 "정리" 기능과 어떻게 결합할까요?
**Options**: 1) 통합: 정리 + 진화를 하나로 2) 별도 모드: rewrite --upgrade 3) 새 스킬: spec-upgrade 4) 토론 종료
**A**: 기존 기능 유지 + 정리 과정에서 화이트페이퍼 성질을 깨뜨리지 않도록 보존 규칙 추가
**Follow-up**: spec-rewrite의 본질은 "정리 도구". 화이트페이퍼 진화는 spec-create의 역할. spec-rewrite는 보존만 담당.

### Round 10
**Q**: spec-rewrite가 화이트페이퍼 성질을 보호하는 수준을 어디까지로 할까요?
**Options**: 1) 보존만 (기존 있으면 지키기) 2) 보존 + 누락 경고 (권장) 3) 보존 + 자동 보강 4) 토론 종료
**A**: 보존 + 누락 경고
**Follow-up**: §1/§2/§5 섹션이 존재하면 정리 시 삭제/축소 금지. 누락 시 REWRITE_REPORT에 "누락 섹션" 경고 표기. 자동 생성은 안 함.

### Round 11
**Q**: spec-rewrite가 self-contained이려면, 화이트페이퍼 포맷 정의를 어떤 형태로 넣을까요?
**Options**: 1) references/spec-format.md 새 파일 (권장) 2) SKILL.md에 직접 인라인 3) rewrite-checklist.md 확장 4) 토론 종료
**A**: references/spec-format.md 새 파일
**Follow-up**: 화이트페이퍼 포맷 구조 + 보존 규칙을 별도 reference 파일로. SKILL.md에서 참조. spec-create의 template-full.md와 독립적.

### Round 12
**Q**: spec-format.md의 내용 범위를 어떻게 할까요?
**Options**: 1) 섹션 구조 + 보존 규칙만 (권장) 2) template-full.md 동일 복사 3) 축약 버전 + 누락 감지용 diff 4) 토론 종료
**A**: 섹션 구조 + 보존 규칙만
**Follow-up**: §1~§8 섹션 목록, 각 섹션의 핵심 요소, 인라인 citation `[filepath:functionName]` 형식, 코드 발취 30줄 규칙. 생성 템플릿이 아닌 체크리스트 성격.

### Round 13
**Q**: 이 spec-rewrite 작업을 기존 구현 범위(A+B)에 추가할까요?
**Options**: 1) A+B+C 함께 (권장) 2) A+B 먼저, C는 후속 3) 토론 종료
**A**: A+B+C 함께
**Follow-up**: spec-create/spec-update-done/spec-rewrite 세 스킬을 한 번에 진화. spec-format.md는 spec-create template-full.md 진화와 연동되므로 함께 하는 게 일관성 있음. 토론 종료.
