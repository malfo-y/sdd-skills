# Spec Review Checklist

탐색형 스펙 기준의 review-only 체크리스트다.

## 1) Scope

- [ ] 메인 스펙 식별
- [ ] 링크된 컴포넌트 스펙 식별
- [ ] 생성물/백업 파일 제외
- [ ] `DECISION_LOG.md` 존재 여부 확인
- [ ] review scope 명시

## 2) Entry Point Quality

- [ ] 프로젝트 목적과 범위가 빠르게 보인다
- [ ] `System Boundary`가 명확하다
- [ ] 메인 스펙이 entry point 역할을 한다

## 3) Navigation Quality

- [ ] `Repository Map`이 있다
- [ ] `Runtime Map`이 있다
- [ ] `Component Index`가 있다
- [ ] 실제 경로 또는 핵심 심볼이 연결되어 있다

## 4) Changeability

- [ ] `Common Change Paths` 또는 동등한 변경 가이드가 있다
- [ ] 변경 시 같이 볼 테스트/로그/디버깅 포인트가 보인다
- [ ] 컴포넌트 책임과 비책임이 구분된다

## 5) Drift

- [ ] 새 컴포넌트/경로/흐름이 구현과 일치한다
- [ ] 오래된 설명이 남아 있지 않다
- [ ] 해결된/새로운 질문이 `Open Questions`에 적절히 반영된다
- [ ] `DECISION_LOG.md` 제안이 필요한 drift를 식별했다

## 6) Evidence

- [ ] High / Medium finding에 구체적 근거가 있다
- [ ] 추론과 직접 근거를 구분했다
- [ ] 확신이 낮은 항목은 `Open Questions`로 남겼다

## 7) Report

- [ ] Executive Summary 포함
- [ ] Findings by Severity 포함
- [ ] Entry Point / Navigation Notes 포함
- [ ] Changeability Notes 포함
- [ ] Spec-to-Code Drift Notes 포함
- [ ] Suggested Next Actions 포함
- [ ] `SPEC_OK` / `SYNC_REQUIRED` / `NEEDS_DISCUSSION` 중 하나 판정
