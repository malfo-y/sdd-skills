# 기능 가이드: 사용자 초대

**생성일**: 2026-03-12
**입력 소스**: mixed (conversation + spec + code)
**대상 기능**: 사용자 초대
**신뢰도**: High

## 설명

사용자 초대 기능은 워크스페이스 관리자가 이메일 주소로 새 멤버를 초대하고, 초대받은 사용자가 링크를 통해 가입/합류하는 흐름이다. 이 기능의 사용자 가치는 관리자가 별도의 계정 생성 과정 없이 팀원을 추가할 수 있고, 초대 상태를 추적할 수 있다는 데 있다.

이 가이드는 "초대 생성 → 이메일 발송 → 초대 수락 → 멤버 등록"까지를 다룬다. 역할(role) 관리, 초대 거절, 멤버 제거는 범위에 포함하지 않는다.

## 규칙

1. 이미 워크스페이스에 속한 사용자에게 중복 초대를 보내면 안 된다. 기존 멤버 여부를 먼저 확인한다.
2. 초대 토큰은 유일하고 예측 불가능해야 하며, 만료 시간(스펙 기준 72시간)을 가진다.
3. 만료된 초대 토큰으로 수락 요청이 오면 실패 처리하고, 관리자에게 재초대를 안내한다.
4. 동일 이메일에 대한 미수락 초대가 이미 존재하면 새 초대를 생성하지 않고 기존 초대를 재발송한다.
5. 초대 수락 시 사용자 계정이 없으면 가입 흐름으로 전환하고, 계정이 있으면 즉시 멤버로 등록한다.
6. 초대 이메일 발송 실패는 초대 생성 자체를 롤백하지 않고, 초대 상태를 `pending_email`로 기록하여 재시도 가능하게 한다.

## 체크리스트

### 구현 전

- [ ] 스펙에서 초대 상태 모델(`pending`, `pending_email`, `accepted`, `expired`)을 확인했다.
- [ ] 초대 API 엔드포인트(`POST /workspaces/:id/invitations`)를 확인했다.
- [ ] 초대 토큰 생성 방식과 만료 정책(72시간)을 확인했다.

### 구현 중

- [ ] 기존 멤버 중복 체크 로직이 초대 생성 전에 실행된다.
- [ ] 동일 이메일 미수락 초대 존재 시 재발송 분기가 있다.
- [ ] 토큰 생성에 암호학적 난수를 사용한다.
- [ ] 이메일 발송 실패 시 초대 상태가 `pending_email`로 남는다.
- [ ] 수락 시 만료 여부를 토큰 검증 단계에서 확인한다.

### 완료/리뷰 전

- [ ] 정상 초대→수락 플로우 테스트가 있다.
- [ ] 중복 이메일 초대 시 재발송 테스트가 있다.
- [ ] 만료 토큰 수락 실패 테스트가 있다.
- [ ] 기존 멤버 초대 차단 테스트가 있다.
- [ ] 이메일 발송 실패 시 상태 확인 테스트가 있다.

## 예시

### 좋은 예시

관리자가 `alice@example.com`을 초대하면, 서버는 먼저 해당 이메일이 워크스페이스 멤버에 없는지 확인한다. 미수락 초대가 존재하면 기존 토큰을 재사용하여 이메일을 재발송한다. 새 초대라면 72시간 만료의 토큰을 생성하고 초대 레코드를 `pending` 상태로 저장한 뒤 이메일을 발송한다. Alice가 링크를 클릭하면 토큰 유효성과 만료를 검증하고, 계정이 없으면 가입 페이지로, 있으면 즉시 멤버로 등록한다.

### 안티패턴

- 초대 생성과 이메일 발송을 하나의 트랜잭션으로 묶어 발송 실패 시 초대 자체가 롤백되는 방식
- 토큰을 UUID v4가 아닌 순차 ID로 생성하여 예측 가능한 방식
- 만료 검증 없이 토큰 존재 여부만으로 수락을 허용하는 방식

## 부록

### 관련 스펙 레퍼런스

- `_sdd/spec/collaboration.md` → `기능 > 사용자 초대`
- `_sdd/spec/collaboration.md` → `상태 모델 > 초대 상태 전이`
- `_sdd/spec/collaboration_API.md` → `API Reference > POST /workspaces/:id/invitations`
- `_sdd/spec/collaboration_API.md` → `API Reference > POST /invitations/:token/accept`

### 관련 코드 레퍼런스

- `src/workspaces/invitation_service.ts` → `createInvitation`
- `src/workspaces/invitation_service.ts` → `acceptInvitation`
- `src/workspaces/invitation_repository.ts` → `findPendingByEmail`
- `src/auth/token_generator.ts` → `generateSecureToken`
- `tests/workspaces/test_invitation_flow.py` → `test_duplicate_email_resends`
- `tests/workspaces/test_invitation_flow.py` → `test_expired_token_rejected`

### 가정 및 미확정 사항

- 없음. 핵심 규칙과 상태 모델이 스펙과 코드 모두에서 확인됨.
