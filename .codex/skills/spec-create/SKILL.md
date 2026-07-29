---
name: spec-create
description: This skill should be used when the user asks to "create a spec", "write a spec document", "generate SDD", "create software design document", "document the project", "create spec for project", or mentions "_sdd" directory, specification documents, or project documentation needs.
---

# spec-create

## Goal

프로젝트의 요구사항, 코드베이스, 기존 문서를 바탕으로 `_sdd/spec/` 아래에 현재 SDD global model에 맞는 글로벌 스펙을 만든다. 현재 모델에서 global spec은 `개념 + 경계 + 결정` 중심의 얇은 기준 문서다.

필요하면 `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md` 같은 최소 부트스트랩 파일도 함께 정리한다. feature-level execution detail은 temporary spec이나 guide에서 다룬다.

## Acceptance Criteria

- [ ] `_sdd/spec/` 아래에 canonical global spec 파일을 생성했다.
- [ ] 공통 코어 4축(`Thinness`, `Decision-bearing truth`, `Anti-duplication`, `Navigation + surface fit`)을 만족하는 구조를 선택했다.
- [ ] 구조 선택 근거를 명시했다. 기본값은 `_sdd/spec/main.md` 단일 파일로 두고, multi-file이면 왜 single-file default가 충분하지 않은지 설명했다.
- [ ] 글로벌 스펙 본문이 `배경/개념`, `Scope / Non-goals / Guardrails`, `핵심 설계와 주요 결정`을 포함한다.
- [ ] repo-wide invariant가 정말 필요할 때만 guardrails 또는 key decisions에 흡수했다.
- [ ] 코드베이스가 있으면 primary navigation axis를 하나 선택했고, 유용할 때만 compact `Strategic Code Map`을 appendix 또는 supporting file로 배치했다.
- [ ] supporting information은 필요할 때만 appendix 또는 별도 supporting file로 분리했다.
- [ ] 코드베이스가 있으면 스펙이 실제 코드 구조와 naming을 반영한다.
- [ ] 필요한 경우에만 `AGENTS.md`(하네스 템플릿 기반 §0~§5 채움), `CLAUDE.md`(`→ AGENTS.md 참조` 포인터), `_sdd/env.md`(비밀값 금지 경고 포함), `.gitignore`(`SDD-WORKSPACE` 마커로 process artifact ignore)를 최소 범위로 생성/보강했다.
- [ ] `AGENTS.md`·`CLAUDE.md` 생성/보강 시 SDD-HARNESS 마커 멱등 병합을 적용했고(부재→생성, 존재→맨 위 prepend·기존 보존, 마커 블록 존재→블록만 교체), legacy `## SDD란` 블록은 하네스로 흡수·제거했다.
- [ ] 하네스를 생성/병합했으면 work log 훅 자산(`references/hooks/`의 두 스크립트 → `.claude/hooks/`, `.claude/settings.json` 훅 등록)도 함께 설치했고, 설치 사실을 최종 보고에 명시했다(3e).

## SDD Lens

- 글로벌 스펙은 얇은 기준 문서다.
- temporary spec은 delta와 execution을 담는 별도 문서다.
- global 본문 기본 구조는 feature-level usage, validation, contract detail을 담기 위한 것이 아니다.
- architecture/component inventory나 reference detail은 supporting surface가 더 기본값에 가깝다.
- `Strategic Code Map`은 agentic coding용 optional navigation hint다. 전체 파일 목록이 아니라 entrypoint, contract source, invariant hotspot, extension point, change hotspot, validation surface, supporting reference만 압축해 둔다.

## Repo-wide Invariant Test

아래 3가지를 모두 만족할 때만 repo-wide invariant note 또는 guardrail candidate로 본다.

1. 코드를 한두 파일 읽는 것만으로 안정적으로 복구되지 않는다.
2. 두 개 이상 feature/module/workflow에 공통 적용된다.
3. 틀리게 가정하면 repo-level reasoning, review, implementation 판단이 어긋난다.

Positive example:

- 전체 API 인증 방식
- 모든 worker가 따라야 하는 retry / backoff 정책
- `_sdd/` artifact handoff 같은 repo-wide operating rule

Negative example:

- 특정 endpoint의 response schema
- 한 컴포넌트 내부 state invariant
- feature 하나에만 필요한 validation detail

## Companion Assets

- `references/template-compact.md`
- `references/template-full.md`
- `references/agents-harness-template.md`
- `references/hooks/worklog-gate.sh`
- `references/hooks/worklog-context.sh`
- `examples/simple-project-spec.md`
- `examples/complex-project-spec.md`
- `examples/additional-specs.md`

## Hard Rules

1. `src/`, `tests/` 등 구현 코드 파일은 수정하지 않는다.
2. 문서 언어는 기존 스펙/문서를 따른다. 기존 스펙이 없으면 한국어를 기본으로 한다.
3. 스펙 출력은 `_sdd/spec/`에만 저장한다.
4. `AGENTS.md`, `CLAUDE.md`는 없을 때 SDD-HARNESS 마커 블록으로 생성하고, 이미 있으면 마커 멱등 병합(맨 위 prepend·기존 보존, 마커 블록 존재 시 블록만 교체)한다. `_sdd/env.md`는 없을 때 생성하고 이미 있으면 필수 안내 문구가 빠진 경우에만 최소 수정한다. `.claude/hooks/`의 훅 스크립트는 항상 정본으로 덮어쓰고(verbatim), `.claude/settings.json`은 해당 훅 항목만 교체하는 키 수준 병합으로 다룬다(3e).
5. 거버넌스 문서는 기본적으로 lowercase canonical `decision_log.md`까지만 사용한다. legacy uppercase `DECISION_LOG.md`는 read-only fallback으로만 취급한다.
6. global spec을 feature-level usage/validation/reference 문서로 부풀리지 않는다.
7. `Strategic Code Map`을 exhaustive file tree, component catalog, API reference, 구현 narrative로 만들지 않는다.

## Structure Decision

기본값은 `_sdd/spec/main.md` 단일 파일이다.

먼저 아래를 판단한다.

- 현재 프로젝트가 single-file로도 concept, boundaries, decisions를 충분히 찾을 수 있는가
- supporting info를 본문 밖으로 내리면 main body가 충분히 읽기 쉬운가
- multi-file이 실제로 navigation + surface fit을 개선하는가

규모에 따라 아래 중 하나를 선택한다.

- 소규모: `_sdd/spec/main.md` 단일 파일
- 중규모 이상: `_sdd/spec/main.md` + 추가 파일

코드베이스가 있으면 primary navigation axis를 하나 선택한다. secondary axis는 별도 동등 문서 체계가 아니라 cross-reference로만 둔다.

| repo 성격 | 탐색 축 / 배치 | 예시 |
|-----------|----------------|------|
| app / service / product | feature / domain / change-path | `auth.md`, `payments.md`, `checkout.md` |
| library / framework / compiler | module / layer | `parser.md`, `runtime.md`, `adapters.md` |
| workflow / tooling repo | entrypoint / workflow | `cli.md`, `agents.md`, `artifact-flow.md` |
| small repo | `main.md` appendix | `Strategic Code Map` 5-10 row |

어떤 축이든 각 파일에 담는 건 global-level 결정만이다. domain 축의 `payments.md`여도 그 안에 들어가는 건 payments 도메인의 장기 설계 판단이지, feature-level validation이나 API response schema가 아니다.

global spec core는 항상 유지한다.

1. 배경 및 high-level concept
2. Scope / Non-goals / Guardrails
3. 핵심 설계와 주요 결정

필요 시에만 아래를 추가한다.

- supporting reference notes
- compact `Strategic Code Map`
- guide 링크
- repo-wide invariant note

`Strategic Code Map` 배치 기준:

- 5-10개 row 수준의 짧은 navigation hint면 `_sdd/spec/main.md` appendix에 둔다.
- row가 많거나 per-path 설명이 필요하면 `_sdd/spec/components.md` 또는 `_sdd/spec/code-map.md` 같은 supporting file로 분리한다.
- 특정 변경의 touchpoint, target file, validation detail은 temporary spec에 둔다.
- 특정 기능의 상세 구현/리뷰 설명은 guide로 둔다.

## Process

### Step 1: Gather Inputs

다음 입력을 우선순위대로 수집한다.

1. 현재 사용자 요청
2. `_sdd/spec/user_draft.md` 또는 사용자 지정 요구사항 파일
3. 기존 README / docs / config / comments
4. 기존 lowercase canonical `_sdd/spec/decision_log.md`, legacy uppercase `_sdd/spec/DECISION_LOG.md` fallback
5. 코드베이스 구조와 핵심 엔트리포인트

### Step 2: Analyze the Project

다음을 파악한다.

- 프로젝트 목표와 해결하려는 문제
- high-level concept와 핵심 가치
- 주요 경계와 scope / non-goals
- 유지해야 할 설계 결정
- `Repo-wide Invariant Test`를 통과할 수 있는 repo-wide invariant 후보
- primary navigation axis 후보와 `Strategic Code Map` 후보(entrypoint, contract source, invariant hotspot, extension point, change hotspot, validation surface, supporting reference)
- supporting surface나 guide로 내려야 할 정보
- single-file default가 충분한지, 아니라면 split rationale이 실제로 필요한지

### Step 3: Bootstrap Workspace Guidance

필요 시 아래 파일을 보강한다. 단 훅 자산은 재량이 아니다 — `AGENTS.md` 하네스를 생성/병합하면 항상 함께 설치한다(3e).

- `AGENTS.md` — SDD 작업 하네스 본체
- `CLAUDE.md` — `→ AGENTS.md 참조` 포인터
- `_sdd/env.md` — 생성 시 상단에 비밀값 금지 경고를 포함한다(커밋되는 파일이므로 API 키·토큰·비밀번호 금지)
- `.gitignore` — process artifact 디렉토리 ignore (3d)
- `.claude/hooks/`·`.claude/settings.json` — 하네스 §5 work log 규약을 강제하는 훅 자산 (3e)

#### 3a. AGENTS.md 하네스 생성

하네스 템플릿 `references/agents-harness-template.md`를 **Read**한다. `SDD-HARNESS:START`~`SDD-HARNESS:END` 마커 블록을 **글자 그대로(verbatim) 복사**해 `AGENTS.md` 본문으로 쓴다 — 템플릿 상단의 관리용 주석(`<!-- 이 파일은 … -->`)만 제외한다. 블록의 어떤 줄도 추가·삭제·재배열·요약하지 않는다. 기억이나 이 SKILL 본문으로 **재구성하지 않는다** — 재구성하면 템플릿 변경(새 §·경고 줄 등)이 산출물에 누락된다.

그다음 아래 `<…>` 꺾쇠 슬롯만 repo 맥락으로 치환한다(슬롯 없는 줄은 글자 그대로 유지).

- `<repo-name>` — repo 이름
- `<test command>` — 테스트 실행 명령 (없으면 해당 줄 삭제)
- `<lint command>` — 린트/타입체크 명령 (없으면 해당 줄에서 삭제)
- `<커밋·PR 규칙>` — repo의 커밋/PR 규칙
- spec §`<scope 섹션>` / §`<decisions 섹션>` — 작성한 global spec의 실제 섹션 이름

§0 작업 원칙 4개는 영어 원문 그대로 유지한다. §3 워크플로우 단계 순서와 §4 ⚠️ 경계 문구(repo-specific 불변 규칙은 spec Guardrails가 단일 소스)는 그대로 둔다.

legacy `## SDD란` 참조 블록은 생성하지 않는다. 그 정보(SDD 개념·워크플로우 안내) 역할은 하네스 §3 워크플로우 + §4 판단 기준이 흡수한다.

#### 3b. CLAUDE.md 포인터 생성

`CLAUDE.md`는 `→ AGENTS.md 참조` 한 줄 포인터로 생성하고 `SDD-HARNESS:START`~`SDD-HARNESS:END` 마커로 감싼다.

```markdown
<!-- SDD-HARNESS:START -->
> 이 repo의 작업 하네스는 `AGENTS.md` 단일 소스다. 작업 전 `AGENTS.md`를 먼저 읽는다.
<!-- SDD-HARNESS:END -->
```

#### 3c. 마커 멱등 병합

`AGENTS.md`·`CLAUDE.md` 각각에 아래 절차를 적용한다.

- 파일 부재 → SDD-HARNESS 마커 블록만으로 새 파일 생성.
- 파일 존재 + 마커 블록 없음 → 마커 블록을 **파일 맨 위에 prepend**하고, 마커 밖 기존 내용은 아래에 그대로 보존한다. 기존 파일의 legacy `## SDD란` 블록은 하네스가 흡수·대체하므로 제거하고, 기존 테스트/커밋 규칙 등 중복 항목은 하네스 슬롯으로 흡수한다. SDD와 무관한 사용자 고유 내용은 보존한다.
- 파일 존재 + 마커 블록 있음 → **그 마커 블록만 교체**하고 마커 밖 내용은 건드리지 않는다(마커-only 교체 = 멱등, 재실행해도 블록이 중복 누적되지 않는다).

#### 3d. .gitignore 보강

커밋되는 `_sdd`는 `spec/`·`guides/`·`env.md`·`drafts/`·`work_log/`다(`drafts/`(feature draft)·`work_log/`는 구현 로그 자산). 나머지 process artifact 디렉토리는 커밋하지 않으므로, 소비 repo의 `.gitignore`에 `SDD-WORKSPACE` 마커 블록을 멱등 병합한다.

```gitignore
# SDD-WORKSPACE:START — process artifact는 로컬 전용(커밋 제외)
_sdd/discussion/
_sdd/implementation/
_sdd/pipeline/
_sdd/pr/
# SDD-WORKSPACE:END
```

- 파일 부재 → 위 마커 블록만으로 새 `.gitignore` 생성.
- 파일 존재 + 마커 없음 → 마커 블록을 파일 끝에 append하고 기존 규칙은 그대로 보존한다.
- 마커 블록 존재 → **그 블록만 교체**한다(멱등). 마커 밖 사용자 규칙은 건드리지 않는다.
- 사용자가 이미 같은 경로를 ignore하고 있어도 마커 블록은 그대로 둔다(중복 ignore는 무해).

#### 3e. work log 훅 자산 설치

하네스 §5(work log)는 산문 규약만으로는 지켜지지 않는다. 훅은 Claude Code가 직접 실행하는 셸 명령이라 모델 재량으로 건너뛸 수 없으므로, §5를 실행되는 게이트로 만든다. **훅 설치는 `AGENTS.md` 하네스 생성/병합과 동일 조건에 묶인다 — 하네스를 깔면 훅도 깐다. 별도 opt-in이 아니다.**

**스크립트 2개는 verbatim 복사다.** `references/hooks/worklog-gate.sh`와 `references/hooks/worklog-context.sh`를 각각 **Read**해 그 내용을 **글자 그대로** 소비 repo의 `.claude/hooks/` 같은 이름으로 쓴다. 어떤 줄도 추가·삭제·재배열·요약하지 않으며 슬롯 치환도 없다(대상 경로 `_sdd/work_log/<yyyy-mm-dd>.md`는 하네스 §5가 고정한다). 기억이나 이 SKILL 본문으로 **재구성하지 않는다** — 재구성하면 자산 변경(파서 fallback·판정 규칙 등)이 산출물에 누락된다. 이미 있으면 정본 내용으로 덮어쓴다.

`.claude/settings.json` 병합 규칙 — JSON에는 마커 주석을 넣을 수 없으므로 마커 블록이 아니라 **키 수준 멱등 병합**이다.

- **파일 부재** → 아래 두 훅 항목만 담은 `settings.json`을 새로 만든다.
- **파일 존재** → `hooks.PreToolUse`·`hooks.SessionStart` 배열에 항목을 추가한다. 단 `command` 문자열이 해당 스크립트 경로(`worklog-gate.sh` / `worklog-context.sh`)를 포함하는 기존 항목이 있으면, 그 `command`를 담고 있는 **바깥 그룹 객체 전체**(`{matcher, hooks:[…]}`)를 아래 예시의 그룹 객체로 **교체**한다. 안쪽 `{type, command}`만 갈아끼우지 않는다 — 그러면 `matcher`가 빠져 있던 과거 설치를 정정하지 못한다. 그 그룹에 사용자의 다른 `command` 항목이 섞여 있으면 그 항목만 별도 그룹으로 떼어 보존한다. (재실행해도 중복 누적되지 않는다 = 멱등.)
- `permissions` 등 다른 최상위 키와 **사용자의 다른 훅 항목은 그대로 보존**한다.
- **파싱 불가**(깨진 JSON)면 덮어쓰지 않는다 — 통째로 다시 쓰면 사용자 설정이 소실된다. 훅 등록만 건너뛰고 그 사실을 최종 보고에 명시한다(스크립트 복사는 그대로 진행).

등록 형태는 아래를 따른다. PreToolUse 항목은 `matcher`가 `"Bash"`여야 하고(게이트는 Bash 명령만 판정한다), SessionStart 항목에는 `matcher`를 두지 않는다. command는 `bash <path>` 형태로 쓴다 — 복사된 스크립트에 실행 권한이 없을 수 있어 exec bit에 의존하지 않기 위함이며, 그래서 별도 `chmod` 단계도 두지 않는다.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/worklog-gate.sh" }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/worklog-context.sh" }
        ]
      }
    ]
  }
}
```

설치 후 최종 보고에 설치 사실을 명시한다(announce) — 알릴 내용은 `## Output Contract` 참조.

### Step 4: Write the Spec

글로벌 스펙 본문 필수 요소:

- 배경 및 high-level concept
- Scope / Non-goals / Guardrails
- 핵심 설계와 주요 결정

조건부 요소:

- reference notes
- compact `Strategic Code Map`
- guide links
- repo-wide invariant note

작성 원칙:

- scope는 책임 범위와 out-of-scope 경계를 같이 고정한다.
- feature-level usage / expected result / validation detail은 global 기본 본문에 강제하지 않는다.
- implementation inventory는 코드나 supporting surface에 맡긴다.
- `Strategic Code Map`은 구현 inventory가 아니라 탐색 시작점만 담는다.
- `Repo-wide Invariant Test`를 통과하지 못하면 global core에 올리지 않는다.
- split을 택했다면 body thinness보다 navigation + surface fit 개선 근거를 남긴다.

### Step 5: Validate and Save

마지막으로 아래를 점검한다.

- spec 구조가 프로젝트 규모와 navigation need에 맞는가
- multi-file이면 single-file default를 벗어난 이유가 실제로 설명되었는가
- 글로벌 스펙 core가 빠지지 않았는가
- global 본문이 code-obvious detail이나 feature inventory로 오염되지 않았는가
- `Strategic Code Map`이 있다면 compact navigation hint이며 exhaustive inventory로 변질되지 않았는가
- 코드베이스와 naming/경로가 크게 어긋나지 않는가
- `AGENTS.md`가 하네스 §0~§5 슬롯을 채워 생성/병합되었고, `CLAUDE.md`가 포인터인가
- 생성/병합 결과 `AGENTS.md`·`CLAUDE.md`에 하네스와 별개의 중복 `## SDD란` 블록이 남지 않았는가(legacy 흡수·제거, SDD 무관 사용자 내용 보존)
- 마커 블록이 재실행 시 중복 누적 없이 블록만 교체되는가(멱등)
- `.gitignore`가 `SDD-WORKSPACE` 마커 블록으로 process artifact를 ignore하고, `_sdd/env.md`에 비밀값 금지 경고가 있는가
- 하네스를 설치했다면 `.claude/hooks/`의 두 스크립트가 정본과 동일 내용으로 놓였고, `.claude/settings.json`이 PreToolUse(`matcher: "Bash"`)·SessionStart 훅을 중복 없이 등록했는가(재실행 시 항목만 교체되는가)

## Output Contract

기본 산출물:

- `_sdd/spec/main.md`

조건부 산출물:

- `_sdd/spec/components.md`
- `_sdd/spec/code-map.md`
- `_sdd/spec/<domain>.md`
- `_sdd/spec/<domain>/...`
- lowercase canonical `_sdd/spec/decision_log.md`
- `AGENTS.md` — `references/agents-harness-template.md` 기반 §0~§5 하네스(SDD-HARNESS 마커 블록)
- `CLAUDE.md` — `→ AGENTS.md 참조` 포인터(SDD-HARNESS 마커 블록)
- `_sdd/env.md` — 상단에 비밀값 금지 경고 포함
- `.gitignore` — `SDD-WORKSPACE` 마커 블록(process artifact ignore)
- `.claude/hooks/worklog-gate.sh`·`.claude/hooks/worklog-context.sh` — `references/hooks/` 정본의 verbatim 사본(3e)
- `.claude/settings.json` — 위 두 훅 등록(키 수준 멱등 병합)

하네스를 설치했다면 최종 보고에 훅 설치 사실을 명시한다(announce): 대상이 **커밋되는** `.claude/settings.json`이라 이 repo의 모든 Claude Code 사용자에게 적용된다는 점, 게이트는 세션 첫 커밋에서만 발동한다는 점, `SDD_SKIP_WORKLOG=1`로 우회 가능하다는 점.

## Error Handling

| 상황 | 대응 |
|------|------|
| 입력 정보 부족 | `request_user_input`으로 최소 보완 |
| 코드베이스 없음 | greenfield/spec-only 문서로 계속 진행하고 low confidence 영역을 표시 |
| 기존 스펙 존재 | 기존 파일 갱신 |
| canonical 구조 불명확 | 후보를 비교하고 사용자 확인 |
| 환경 정보 부족 | `_sdd/env.md`에 TODO 기반 최소 가이드 생성 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
