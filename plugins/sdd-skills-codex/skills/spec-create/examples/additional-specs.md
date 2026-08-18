# Additional Spec Notes

## Default Shape First

기본값은 `_sdd/spec/main.md` 단일 파일이며, supporting file은 이 기본형이 실제로 부족할 때만 고려한다.

## When to Add Supporting Files

다음 중 하나면 supporting file이나 guide를 고려한다.

- 특정 feature의 사용 흐름이 반복적으로 리뷰 맥락에 필요함
- 환경/설정/운영 상세가 global 본문을 오염시킴
- `Strategic Code Map`이 `main.md` appendix로 담기에는 길거나 per-path 설명이 필요함

supporting file은 global 본문의 thinness를 지키기 위한 분리이지, core body를 대체하기 위한 분리가 아니다.

## Strategic Code Map Placement

작은 repo에서는 `main.md` 끝에 5-10 row 정도의 compact map을 둘 수 있다.

```markdown
### Strategic Code Map

| Change Path / Area | Start Here | Contract / Hotspot | Validation Surface | Why |
|--------------------|------------|--------------------|--------------------|-----|
| CLI flow | `src/cli.ts` | `src/config.ts` | `tests/cli.test.ts` | command parsing과 config contract가 만난다. |
```

다음 중 하나면 `_sdd/spec/components.md` 또는 `_sdd/spec/code-map.md`로 분리한다.

- map이 10-15 row 이상으로 커진다
- 각 row에 read order, invariant, validation note 같은 설명이 필요하다
- domain/module별 supporting surface가 이미 있고 그쪽에 두는 편이 찾기 쉽다

분리해도 map은 exhaustive inventory가 아니다. entrypoint, contract source, invariant hotspot, extension point, change hotspot, validation surface만 남긴다.

## When Multi-file Split Is Justified

다음이 함께 성립할 때만 split rationale이 충분하다.

- single-file 상태에서 navigation cost가 실제로 커졌다
- domain 또는 topic으로 나누면 reader가 더 빨리 repo-wide 결정을 찾을 수 있다
- 각 추가 파일에도 feature-level validation이나 expected result가 아니라 global-level 판단만 담을 수 있다

## What Should Not Return to the Global Core

- feature-level expected results
- per-feature contract and validation detail
- exhaustive architecture inventory
- exhaustive file tree or component catalog
- README나 guide가 더 적절한 supporting info
