# 스킬 제작 규범 — Claude 5 세대 (Skill Authoring Norms)

> 이 repo의 스킬(SKILL.md)·agent 본문·하네스 문서를 **작성/수정할 때** 적용하는 제작 규범.
> 런타임에 스킬이 참조하는 문서가 아니라, 스킬을 만드는 사람(모델)이 부합 여부를 점검하는 체크리스트다.
>
> 출처 (Anthropic, 2026):
> - [The New Rules of Context Engineering for Claude 5 Generation Models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)
> - [A Field Guide to Claude Fable: Finding Your Unknowns](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)

---

## 1. 배경: 무엇이 바뀌었나

Anthropic은 Claude 5 세대 모델에서 Claude Code 시스템 프롬프트의 80% 이상을 걷어냈고 코딩 평가에서 측정 가능한 손실이 없었다. 이전 세대에서 필요했던 촘촘한 규칙·예시·반복 지시가 이제는 오히려 비용이다 — 핵심 메커니즘은 **지시 충돌**이다: 시스템 프롬프트·CLAUDE.md·스킬이 한 요청에 겹치면 서로 모순되는 지시("문서화를 남겨라" vs "주석 금지")가 생기고, 모델은 이를 조정하느라 판단력을 소모한다. 규칙 나열보다 **판단 기준과 맥락**을 줄 때 더 잘 일반화한다.

동시에 field guide는 병목이 이동했다고 말한다 — 품질을 가르는 것은 모델의 능력이 아니라 **작성자가 unknowns(암묵 지식·미고려 요소)를 얼마나 드러내 주는가**다. 스킬 제작에서는 이 둘이 합쳐져 하나의 방향이 된다: **지시는 얇게, 맥락과 레퍼런스는 진하게.**

## 2. 핵심 규범: Then → Now

| 이전 세대 (~Claude 4) | 지금 (Claude 5 세대) | 이 repo에서의 의미 |
|---|---|---|
| 명시적 규칙을 나열 | 판단 기준을 주고 judgment에 맡김 | 절차 강제는 "유혹이 실재하는" 지점에만. 나머지는 목적·기준 서술 |
| 사용 예시를 제공 | 인터페이스 자체를 잘 설계 | agent 반환 형식·schema·enum이 예시 나열을 대체 |
| 정보를 front-load | progressive disclosure | SKILL.md는 얇게, 상세는 `references/`로 분리해 필요 시 Read |
| 지시를 반복 | 소비 지점에 가장 가까운 한 곳에 배치 | 규범의 단일 홈 원칙 — 홈은 그 규칙이 소비되는 지점(agent 본문·tool description), canonical 목록 복제 금지 |
| 단순 markdown 설명 | rich reference (코드·목업·템플릿) | 동작을 산문으로 재서술하지 말고 실물 템플릿을 가리켜 verbatim 복사 |

## 3. 제작 체크리스트

### 3.1 본문 (SKILL.md / agent 본문)

- [ ] **규칙보다 기준.** "~하지 마라" 목록 대신 목적과 판단 기준을 서술했는가. 하드 규칙(금지·강제)은 실제로 모델이 반복해서 어기는 유혹이 관측된 지점에만 남긴다. 관측 근거 없는 방어적 금지는 사족이다.
- [ ] **산문 > 의사코드.** 모델이 따라야 할 술어는 산문 규칙으로 쓴다. 의사코드는 분기가 정교해서 산문으로 오히려 모호해지는 절차에만 쓴다.
- [ ] **negative 재천명 금지.** "여기서는 X를 하지 않는다" 류의 재천명은 positive 정의 1회로 대체한다. 단, 실재하는 유혹을 막는 negative(예: plan-review 재진술 금지)는 유지한다.
- [ ] **판단 주체는 1곳.** 같은 판정 로직·canonical 목록을 두 문서에 복제하지 않는다. 한 곳이 홈이고 나머지는 가리킨다.
- [ ] **구체성 눈금 조정.** 너무 구체적이면 pivot이 맞는 상황에서도 지시를 그대로 따르고, 너무 모호하면 이 repo에 안 맞는 업계 관행을 가정한다. 각 지시마다 "이탈이 이로울 수 있는 지점인가(→기준으로), 이탈이 곧 사고인가(→규칙으로)"를 물어 눈금을 정한다. 이것이 §3.1 전체의 판정 기준이다.
- [ ] **지시 충돌 grep.** 새 규칙을 추가할 때 같은 요청에 함께 로드되는 표면(AGENTS.md·인접 스킬·agent 본문)과 모순되지 않는지 확인한다. 충돌하는 두 규칙은 둘 다 약해진다.

### 3.2 구조 (progressive disclosure)

- [ ] **SKILL.md는 진입점.** 트리거 조건·프로세스 골격·AC만 본문에 두고, 긴 템플릿·상세 절차·참고 자료는 스킬 디렉토리의 `references/` 등 별도 파일로 분리했는가.
- [ ] **로드 시점 명시.** 분리한 파일은 "어느 단계에서 Read 하는지"를 본문에 한 줄로 지정한다. 항상 읽어야 하는 내용이면 분리하지 말고 본문에 둔다.
- [ ] **재구성 금지, 복사 지시.** reference를 "생성/사용하라"고 하면 모델이 재구성하며 내용이 유실된다. 전파가 필요한 템플릿은 "Read 후 verbatim 복사, 슬롯만 치환"으로 기계적으로 지시한다.

### 3.3 레퍼런스 (rich references)

- [ ] **실물 > 설명.** 원하는 산출물이 있으면 형식을 산문으로 길게 묘사하지 말고 실제 예시 파일(템플릿·목업·기존 구현)을 가리킨다. "HTML 목업 하나가 디자인 설명 문단보다 낫다."
- [ ] **테스트가 곧 스펙.** 검증 가능한 산출물이면 AC를 산문 나열 대신 실행 가능한 체크(grep·diff·structural check)로 표현할 수 있는지 먼저 검토한다.
- [ ] **취향은 rubric으로.** "좋은 결과물"의 기준이 기계적 체크로 안 잡히면(문서 품질·API 설계 등) rubric을 reference로 두고 verifier agent가 그것으로 판정하게 한다 — 이 repo의 AC-first 검증 rubric 사슬(`docs/SDD_SPEC_DEFINITION.md` §6)이 같은 패턴이다.

### 3.4 인터페이스 (agent 반환·툴 파라미터)

- [ ] **인터페이스가 예시를 대체.** agent 반환 형식을 정의할 때 "예시: ..." 나열보다 필드명·허용값(enum)·필수/선택을 명시한 형식 정의가 우선이다. 좋은 인터페이스는 예시 없이도 의도를 전달한다.
- [ ] **호출 계약은 형식으로.** 스킬↔agent 간 주고받는 데이터는 자유 산문이 아니라 고정 헤더·필드 구조로 계약한다. 계약이 바뀌면 양쪽(claude·codex 미러 포함)을 같은 커밋에서 갱신한다.

## 4. Unknowns 실천법 → SDD 단계 매핑

field guide의 실천법은 "작성자의 unknowns를 드러내는 장치"다. SDD 체인의 대응 지점:

| 실천법 | 내용 | SDD 대응 |
|---|---|---|
| Blind spot pass | 시작 전 "내 맹점이 뭔가"를 명시적으로 질문 | discussion 초입 — 특히 낯선 도메인일 때 |
| 인터뷰 | 1문항씩, **답이 아키텍처를 바꾸는 질문 우선** | discussion / feature-draft의 질문 단계 |
| 브레인스톰·프로토타입 | 본 구현 전 복수 방향·목업으로 싸게 unknowns 노출 | discussion → feature-draft 사이 |
| 구현 계획 | 바뀔 가능성 큰 결정(데이터 모델·인터페이스·사용자 표면)을 강조 | feature-draft의 Target Files·AC |
| Implementation notes | 계획과의 이탈·발견한 엣지케이스 기록 | work_log + implementation temporary spec |
| 퀴즈·explainer | 머지 전 변경 내용을 작성자가 이해했는지 확인 | implementation-review / PR 설명 |

스킬을 고칠 때 이 표에서 대응이 비어 있는 실천법이 보이면, 새 단계를 만들기보다 기존 단계에 질문·기록 한 줄을 얹는 쪽을 먼저 검토한다.

## 5. 기존 repo 규범과의 관계

**이미 부합하는 것** — 이 규범은 repo가 실측으로 도달한 결론들과 대체로 일치한다:

- 산문 규칙 > 의사코드 (deriveGroups 슬림화)
- 방어적 사족·negative 재천명 제거, 판정 주체 단일화
- CLAUDE.md를 AGENTS.md 포인터 한 줄로 유지 (얇은 진입점)
- reference verbatim 복사 지시 (rich reference의 기계적 적용)

**긴장 지점** — 맹목 적용하면 안 되는 곳:

- 이 repo의 하드 게이트(전파 census, §섹션 리터럴 검증, worklog 게이트)는 "관측된 반복 실패"에 근거한 규칙이다. "judgment에 맡겨라"를 이유로 이런 게이트를 걷어내려면, 해당 실패가 더 이상 재현되지 않는다는 증거가 먼저 필요하다.
- progressive disclosure는 로드 시점이 명확할 때만 이득이다. 매 실행마다 읽는 내용을 분리하면 Read 왕복만 늘어난다.

요약하면: **규칙을 걷어내는 방향이 기본값이되, 걷어낼 자격은 실측이 준다.** 새 스킬을 쓰거나 기존 스킬을 다이어트할 때 §3 체크리스트를 통과시키고, 하드 규칙을 남길 때는 그 근거(어떤 실패를 막는가)를 한 줄 병기한다.
