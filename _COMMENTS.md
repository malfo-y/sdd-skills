# _COMMENTS

Generated at: 2026-03-19T09:53:53.106Z
Total comments: 1

## Comments

### docs/SDD_WORKFLOW.md:L328-L328

sdd-autopilot 사용 시 자동으로 적절한 경로를 선택합니다.

- anchor.hash: ce6ff8d2
- anchor.snippet: 황에 따라 경로를 선택합니다:
- anchor.before: 트 초안

## 목표
사용자 인증이 있는 작업 관리 API 구축

## 필요한 기능
- JWT 기반 로그인/회원가입
- 작업 CRUD
- 마감일 알림

## 기술 스택
- Python + FastAPI
- PostgreSQL
```

**적합한 경우:**
- PM/기획자가 요구사항 제공
- 새 프로젝트 시작
- 명확한 요구사항이 있을 때

---

### 구현 경로 선택

기능의 복잡도와 상
- anchor.after: 

```mermaid
flowchart LR
    Start(["규모별 경로 선택"]):::start

    %% 대규모
    subgraph L["대규모"]
        direction TB
        L1["feature-draft<br/>패치 초안 + 구현 계획"]:::large
        L2["spec-update-todo<br/>스펙 사전 반영"]:::large

- createdAt: 2026-03-19T09:53:21.915Z
