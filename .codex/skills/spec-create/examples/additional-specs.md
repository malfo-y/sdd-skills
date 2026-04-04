# Additional Spec Notes

## When to Add Supporting Files

다음 중 하나면 supporting file이나 guide를 고려한다.

- 특정 feature의 사용 흐름이 반복적으로 리뷰 맥락에 필요함
- 환경/설정/운영 상세가 global 본문을 오염시킴
- code map이 수동 탐색 힌트로 실제 가치가 있음

## Repo-wide Invariant Test

다음 3가지를 모두 만족할 때만 global core의 invariant note 후보가 된다.

- code-obvious detail이 아니다
- 여러 feature/module/workflow에 공통 적용된다
- 틀리게 가정하면 repo-level reasoning이 어긋난다

## What Should Not Return to the Global Core

- feature-level expected results
- per-feature contract and validation detail
- exhaustive architecture inventory
- README나 guide가 더 적절한 supporting info
