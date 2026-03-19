# _COMMENTS

Generated at: 2026-03-19T09:48:52.609Z
Total comments: 3

## Comments

### docs/SDD_QUICK_START.md:L75-L75

/discussion 이후 /sdd-autopilot을 호출하면 된다고 설명하는 게 더 나아 보인다.

- anchor.hash: 5967db81
- anchor.snippet: 대부분의 기능 구현은 `/sdd-autopilot`으로 시작하면 됩니다. autopilo
- anchor.before: C0,stroke-width:2px,color:#0D47A1;
    classDef action fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20;
    classDef output fill:#F5F5F5,stroke:#616161,stroke-width:1.5px,color:#212121;
```

---

## 구현 경로 선택


- anchor.after: t이 규모를 자동 판단하고 적절한 스킬을 순차 호출합니다.

```bash
/sdd-autopilot 이 기능 구현해줘: [기능 설명]
```

개별 스킬을 수동으로 조합하고 싶다면 아래 규모별 경로를 사용합니다:

| 규모 | 워크플로우 |
|------|-----------|
| **대규모** | feature-draft → spec-update-todo → implementation-p
- createdAt: 2026-03-19T09:47:52.201Z

---

### docs/SDD_WORKFLOW.md:L72-L72

이거 이제 코덱스에서도 지원함. 삭제해도 됨.

- anchor.hash: 4c1c4642
- anchor.snippet: ssion` 스킬은 Claude Code에서만 지원합니다.
- anchor.before:  + 선택지 비교 + 결정/미결/실행항목 정리 |
| **guide-create** | "가이드 작성", "기능 가이드", "guide create" | 스펙+코드 기반 기능별 구현/리뷰 가이드 문서 생성 |
| **sdd-autopilot** | "autopilot", "자동 구현", "전체 파이프라인" | 전체 SDD 파이프라인을 자율 오케스트레이션 |

> (caveat) `/discu
- anchor.after: 

### 자동 오케스트레이션 (sdd-autopilot) — 추천 경로

대부분의 기능 구현은 `/sdd-autopilot`으로 시작하면 됩니다. autopilot이 요구사항을 분석하고, 규모에 맞는 스킬 조합을 자동으로 구성하여 전체 파이프라인을 자율 실행합니다. 사용자는 초반 요구사항 확인과 파이프라인 승인만 참여하면 됩니다.

```bash
/sdd-autopilot 이 기능 구현해줘
- createdAt: 2026-03-19T09:48:31.399Z

---

### docs/SDD_WORKFLOW.md:L76-L76

/discussion 이후 /sdd-autopilot

- anchor.hash: f70c74e6
- anchor.snippet: 기능 구현은 `/sdd-autopilot`으로 시작
- anchor.before: ate" | 스펙+코드 기반 기능별 구현/리뷰 가이드 문서 생성 |
| **sdd-autopilot** | "autopilot", "자동 구현", "전체 파이프라인" | 전체 SDD 파이프라인을 자율 오케스트레이션 |

> (caveat) `/discussion` 스킬은 Claude Code에서만 지원합니다.

### 자동 오케스트레이션 (sdd-autopilot) — 추천 경로

대부분의 
- anchor.after: 하면 됩니다. autopilot이 요구사항을 분석하고, 규모에 맞는 스킬 조합을 자동으로 구성하여 전체 파이프라인을 자율 실행합니다. 사용자는 초반 요구사항 확인과 파이프라인 승인만 참여하면 됩니다.

```bash
/sdd-autopilot 이 기능 구현해줘: [기능 설명]
```

> 상세 가이드: [AUTOPILOT_GUIDE.md](AUTOPILOT_GUIDE.md)

### 규모별 
- createdAt: 2026-03-19T09:48:42.422Z
