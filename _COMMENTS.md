# _COMMENTS

Generated at: 2026-03-19T06:26:20.153Z
Total comments: 1

## Comments

### _sdd/discussion/discussion_ralph_generalization.md:L27-L27

LLM이 프로젝트를 분석해서 자유롭게 phase들을 만들되, 일반적으로 이런 phase들이 있다고 hint 정도로 가이드.

- anchor.hash: 3fbc497f
- anchor.snippet: 정. 추가/제거 불필요. LL
- anchor.before: 빈번한 유스케이스이므로 기존 동작이 깨지면 안 됨 | 1 |

## 미결 질문 → 해소 (Resolved Open Questions)

| # | 질문 | 결정 |
|---|------|------|
| 1 | 레퍼런스 phase set 구성 | **SETUP / SMOKE_TEST / EXECUTING / CHECKING / ANALYZING / ADJUSTING / DONE** 7개로 확
- anchor.after: M이 프로젝트에 따라 이 레퍼런스를 참고하여 커스터마이징. |
| 2 | Step 1 프로젝트 타입 자동 감지 기준 | **LLM 판단에 위임**. 고정 파일 패턴 매칭(train*.py 등) 대신 LLM이 프로젝트를 분석해서 적절한 탐색 전략을 직접 결정. |
| 3 | `ralph-loop-concept.md` 범용화 여부 | **그대로 유지**. ML 예시 기반으로 남기되, agent
- createdAt: 2026-03-19T06:25:59.786Z
