# Evidence Pack Contract

서브에이전트는 긴 원문 대신 아래 구조를 채운 evidence pack을 반환한다.

## Required Fields

```yaml
source_type: wiki | calendar | doc | meet
source_url: string
title: string
event_time:
  raw: string
  normalized: string
key_excerpt: string
extracted_facts:
  - fact: string
    source_anchor: string
confidence_note: string
matching_hints:
  meet_code: string | null
  title_tokens:
    - string
  participants:
    - string
  created_or_updated_at: string | null
```

## Guidance

- `key_excerpt`는 1-3개 핵심 문장 수준으로 짧게 유지한다.
- `extracted_facts`는 메인이 바로 병합할 수 있도록 atomic fact 단위로 적는다.
- 확실하지 않은 추론은 `confidence_note`에 분리한다.
- 원문 전체를 복붙하지 않는다.

## Main Agent Expectations

메인 에이전트는 여러 evidence pack을 합쳐서 아래를 판단한다.

1. 같은 회의인지
2. 공통 사실은 무엇인지
3. 상충하는 사실은 무엇인지
4. 어떤 요약과 비평이 정당한지
