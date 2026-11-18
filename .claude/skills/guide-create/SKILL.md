---
name: guide-create
description: This skill should be used when the user asks to "guide create", "create guide", "feature guide", "write guide", "가이드 작성", "기능 가이드", "가이드 문서 만들어줘", or wants to generate an implementation/review guide document for a specific feature from spec and code context.
---

# guide-create

기능 하나를 깊이 설명하는 기술 가이드를 spec과 코드 근거로 써서 `_sdd/guides/<YYYY-MM-DD>_guide_<slug>.md`에 저장한다. guide는 global spec을 대신하지 않는 보조 문서다. 사용 시나리오, 인터페이스, 구현·리뷰 판단을 기능 단위로 구체화한다.

## Acceptance Criteria

- [ ] 대상 기능과 범위를 정했고, 기능마다 파일 하나를 만들었다.
- [ ] 본문의 주장마다 source citation이 있고, 확인하지 못한 것은 가정이나 미확인으로 구분했다.
- [ ] 문서가 `references/output-format.md`의 구조와 규칙을 따른다.
- [ ] `_sdd/spec/`, 코드, 설정, 테스트를 고치지 않았다.

## 규칙

1. **대상**: 요청에서 기능과 경계를 정한다. 기능이나 범위가 달라지는 모호함이 남으면 한 번 물어 닫는다. 기능이 여럿이면 기능별 출력 경로를 먼저 나열하고, 한 파일을 확인까지 끝낸 뒤 다음 파일로 간다.
2. **근거**: spec은 목적·경계·결정의 출처이고, 코드·테스트·인터페이스·타입은 실제 동작의 출처다. 쓸 만한 spec이 없으면 그 한계를 알리고, 가정을 명시해 진행하거나 spec 작성을 권한다. 실행·검증 맥락이 필요할 때만 `_sdd/env.md`를 읽는다.
3. **확인되지 않은 것**: 근거가 없는 API, 에러, 시나리오, 불변 규칙은 쓰지 않는다. 필요한 빈 곳은 가정이나 미확인으로 표시한다.
4. **형식**: 쓰기 직전에 `references/output-format.md`를 **Read**하고, 그 fenced skeleton을 복사해 채운다. 그 파일이 허용한 번역과 생략 밖에서는 제목과 순서를 바꾸지 않는다. 형식을 기억이나 이 본문으로 재구성하지 않는다.
5. **저장**: 같은 날짜·slug의 파일이 있으면 덮어쓰지 않고 더 구체적인 slug를 쓴다. 문서 언어는 사용자 지정이 우선이고, 없으면 기존 spec·문서의 언어를 따른다.
6. **범위**: 이 스킬이 만드는 것은 guide 파일뿐이다. 상위 하네스의 작업 기록 의무는 따로 따른다.

## Final Check

Acceptance Criteria를 한 번 대조한다. 보완할 수 있는 누락은 고치고, 근거가 부족해 제한한 내용과 끝내지 못한 항목은 만든 경로와 함께 보고한다.
