<!-- Authoring canonical: .claude/skills/spec-create/references/worker-model-defaults.md; spec-upgrade와 Codex package에는 동일 사본을 배포한다. -->

# Worker Model Defaults Bootstrap

## 적용

- `_sdd/env.md`가 없으면 환경 가이드 제목과 비밀값 금지 경고(API 키·토큰·비밀번호를 적지 않음)를 포함해 만든다. 기존 파일은 내용을 보존하고 경고가 없을 때만 보완한다.
- 아래 블록을 사용해 `Worker Model Defaults` 절을 보강한다. 절이 없으면 추가하고, 있으면 누락된 안내·runtime 표·열·단계 행만 추가한다. 기존 값과 의도적으로 비워 둔 칸은 유지하며, 재실행해도 절·표·행을 중복 추가하지 않는다.
- 새 model·effort 칸은 비워 둔다. 현재 세션 모델이나 다른 저장소의 값을 복사하지 않는다. 두 runtime 표를 모두 제공하며 모델 선택·검증은 이 부트스트랩에서 수행하지 않는다.

## env.md 블록

```markdown
## Worker Model Defaults

`sdd-orchestrator`의 단계별 worker 기본값을 설정하는 선택 항목입니다. 나중에 사용하는 runtime 표에 원하는 모델을, Codex에서는 effort도 채워 넣으세요. 빈 칸은 저장소 기본값 없음이며, 호출에서 지정한 값도 없으면 런타임 기본 동작을 따릅니다. 설정을 비워 두어도 spec 생성·업그레이드를 완료할 수 있습니다.

### Claude Code

| 단계 | model |
|------|-------|
| feature-draft | |
| plan-review | |
| implementation | |
| implementation-review | |
| spec-sync | |

### Codex

| 단계 | model | effort |
|------|-------|--------|
| feature-draft | | |
| plan-review | | |
| implementation | | |
| implementation-review | | |
| spec-sync | | |
```

## 확인·보고

두 runtime 표에 다섯 단계가 중복 없이 있고, 추가한 값 칸은 비어 있으며, 기존 설정과 주변 문서가 보존됐는지 확인한다. 최종 보고에는 `_sdd/env.md`의 표 위치를 가리키고, 빈 칸이 있으면 사용자가 나중에 모델·effort를 선택해 채울 수 있는 선택 항목임을 알린다. 빈 칸을 미완료나 blocker로 보고하지 않는다.
