# Example Request Flow

## Example A: Meet Link Only

### User Input

```text
회의 제목: 데모 및 API 관련
일시: 2026-02-06 14:30-15:00
시간대: Asia/Seoul
Meet 링크: https://meet.google.com/xyq-kzop-gta
```

### Expected Flow

1. Meet 코드 `xyq-kzop-gta` 추출
2. Calendar에서 같은 시간대 이벤트 식별
3. Drive에서 관련 Gemini 회의록 문서 연결
4. 위키 회의록이 있으면 추가 연결
5. evidence pack 병합 후 통합 요약/비평/다음 액션 생성

## Example B: Wiki + Docs

### User Input

```text
위키: https://wiki.daumkakao.com/pages/viewpage.action?pageId=123456789
문서: https://docs.google.com/document/d/abc123/edit
이 회의 정리해줘. 서로 다른 내용이 있으면 같이 보여줘.
```

### Expected Flow

1. 위키와 문서를 각각 읽는다.
2. 제목/시간/작성 시각으로 같은 회의인지 판단한다.
3. 공통 사실과 충돌 사실을 분리한다.
4. 충돌은 출처별 병렬 표기로 남긴다.
5. 회의별 파일로 저장한다.

## Example C: Ambiguous Match

### User Input

```text
https://docs.google.com/document/d/abc123/edit
이거 관련 회의록이랑 같이 보고 정리해줘.
```

### Expected Flow

1. 문서 제목과 작성 시각을 읽는다.
2. Calendar/Drive/위키 후보를 찾는다.
3. 후보가 여러 개면 상위 2-3개와 근거를 제시한다.
4. 사용자 확인 후 최종 병합을 진행한다.

## Example D: Existence Check Only

### User Input

```text
이 Meet 링크에 대응하는 Gemini 회의록이 있는지만 확인해줘.
https://meet.google.com/xyq-kzop-gta
```

### Expected Flow

1. Meet 링크에서 이벤트와 관련 문서를 찾는다.
2. 존재 여부와 후보 링크만 짧게 보고한다.
3. 사용자가 요약을 추가로 요청하지 않으면 전체 분석 파일은 만들지 않는다.

## Example E: Drive File URL Only

### User Input

```text
https://drive.google.com/file/d/1AbCdEfGhIjKlMnOp/view
이 회의 기록 기준으로 관련 자료 연결해서 정리해줘.
```

### Expected Flow

1. Drive 파일 ID와 파일 유형을 식별한다.
2. 메타데이터와 가능한 본문 텍스트를 읽는다.
3. 제목/수정 시각/본문 단서로 Calendar와 위키를 역추적한다.
4. 연결 confidence를 표시하면서 통합 요약을 만든다.
