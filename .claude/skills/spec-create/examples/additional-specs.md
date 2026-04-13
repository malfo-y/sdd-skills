# Additional Spec Notes

## Default Shape First

기본값은 `_sdd/spec/main.md` 단일 파일이다.

먼저 묻는다.

- single-file로도 concept, boundaries, decisions를 충분히 찾을 수 있는가
- supporting info를 본문 밖으로 내리면 main body가 얇고 읽기 쉬워지는가

둘 다 yes면 multi-file split을 만들지 않는다.

## When to Add Supporting Files

다음 중 하나면 supporting file이나 guide를 고려한다.

- 특정 feature의 사용 흐름이 반복적으로 리뷰 맥락에 필요함
- 환경/설정/운영 상세가 global 본문을 오염시킴
- code map이 수동 탐색 힌트로 실제 가치가 있음

supporting file은 global 본문의 thinness를 지키기 위한 분리이지, core body를 대체하기 위한 분리가 아니다.

## When Multi-file Split Is Justified

다음이 함께 성립할 때만 split rationale이 충분하다.

- single-file 상태에서 navigation cost가 실제로 커졌다
- domain 또는 topic으로 나누면 reader가 더 빨리 repo-wide 결정을 찾을 수 있다
- 각 추가 파일에도 feature-level validation이나 expected result가 아니라 global-level 판단만 담을 수 있다

## What Should Not Return to the Global Core

- feature-level expected results
- per-feature contract and validation detail
- exhaustive architecture inventory
- README나 guide가 더 적절한 supporting info
