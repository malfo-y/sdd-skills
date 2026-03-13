# 기능 기술 보고서: 사용자 초대

**생성일**: 2026-03-12
**입력 소스**: mixed (conversation + spec + code)
**대상 기능**: 사용자 초대
**신뢰도**: High

## 1. 배경 및 동기

사용자 초대 기능은 워크스페이스 관리자가 이메일 주소로 새 멤버를 초대하고, 초대받은 사용자가 링크를 통해 가입/합류하는 흐름이다.

이 기능이 해결하는 문제:
- 관리자가 별도의 계정 생성 과정 없이 팀원을 추가할 수 있음
- 초대 상태를 추적하여 누가 아직 수락하지 않았는지 파악 가능
- 이메일 발송 실패와 토큰 만료를 체계적으로 관리

관리자가 직접 계정을 생성하는 방식 대신 초대 토큰 기반 접근을 택한 이유는, 사용자가 직접 비밀번호를 설정하고 동의 절차를 거치도록 하기 위함이다.

## 2. 핵심 설계

핵심 설계는 **토큰 기반 초대 + 상태 머신**이다.

- 초대는 `pending → accepted | expired` 상태 전이를 따른다. 이메일 발송 실패 시 `pending_email` 상태로 별도 관리한다.
- 초대 토큰은 암호학적 난수로 생성하며, 72시간 만료 정책을 가진다.
- 동일 이메일에 대한 미수락 초대가 존재하면 새 토큰을 생성하지 않고 기존 토큰을 재발송한다.
- 수락 시 기존 계정이 있으면 즉시 멤버 등록, 없으면 가입 흐름으로 전환한다.

관련 코드:
- `[src/workspaces/invitation_service.ts:createInvitation]` — 초대 생성 진입점. 중복 검증 → 토큰 생성 → 이메일 발송
- `[src/workspaces/invitation_service.ts:acceptInvitation]` — 토큰 검증 → 만료 확인 → 멤버 등록
- `[src/auth/token_generator.ts:generateSecureToken]` — 암호학적 난수 기반 토큰 생성

```typescript
// createInvitation 핵심 흐름 (간략)
async createInvitation(workspaceId: string, email: string) {
  if (await this.members.isMember(workspaceId, email)) {
    throw new AlreadyMemberError();
  }
  const existing = await this.repo.findPendingByEmail(workspaceId, email);
  if (existing) return this.resendEmail(existing);
  const token = this.tokenGen.generateSecureToken();
  const invitation = await this.repo.create({
    workspaceId, email, token, expiresAt: now() + 72h, status: 'pending'
  });
  await this.mailer.sendInvitation(email, token);
  return invitation;
}
```

## 3. 사용 시나리오 가이드

### 시나리오 1: 신규 사용자 초대 (정상 흐름)

**전제 조건**: 관리자가 워크스페이스에 로그인되어 있고, 초대 대상 이메일이 기존 멤버가 아님.

**입력**:
```json
POST /workspaces/ws_001/invitations
{
  "email": "alice@example.com"
}
```

**처리 흐름**:
1. 요청자의 관리자 권한 확인
2. `alice@example.com`이 워크스페이스 멤버인지 확인 → 아님
3. 동일 이메일로 미수락 초대가 있는지 확인 → 없음
4. 72시간 만료 토큰 생성 (암호학적 난수)
5. 초대 레코드 생성 (상태: `pending`)
6. 초대 이메일 발송

**기대 결과**:
```json
{
  "invitation_id": "inv_abc123",
  "workspace_id": "ws_001",
  "email": "alice@example.com",
  "status": "pending",
  "expires_at": "2026-03-15T10:30:00Z",
  "created_at": "2026-03-12T10:30:00Z"
}
```
HTTP 상태: 201 Created

### 시나리오 2: 초대 수락 (기존 계정 있음)

**전제 조건**: 초대 토큰이 유효하고 만료되지 않았으며, 사용자가 이미 계정을 보유.

**입력**:
```json
POST /invitations/tok_secure_abc/accept
```

**처리 흐름**:
1. 토큰으로 초대 조회
2. 만료 여부 확인 → 유효
3. 사용자 계정 존재 여부 확인 → 기존 계정 있음
4. 워크스페이스 멤버로 즉시 등록
5. 초대 상태를 `accepted`로 변경

**기대 결과**:
```json
{
  "status": "accepted",
  "workspace_id": "ws_001",
  "member": {
    "user_id": "usr_alice",
    "email": "alice@example.com",
    "joined_at": "2026-03-13T14:00:00Z"
  }
}
```

### 시나리오 3: 초대 수락 (계정 없음 → 가입 전환)

**전제 조건**: 초대 토큰이 유효하지만 사용자가 계정을 보유하지 않음.

**처리 흐름**:
1. 토큰 검증 → 유효
2. 계정 존재 확인 → 없음
3. 가입 페이지로 리다이렉트 (토큰 정보 유지)

**기대 결과**:
```json
{
  "action": "redirect_to_signup",
  "redirect_url": "/signup?invitation_token=tok_secure_abc",
  "email": "alice@example.com"
}
```

### 시나리오 4: 기존 멤버 중복 초대

**전제 조건**: 초대 대상 이메일이 이미 워크스페이스 멤버.

**입력**:
```json
POST /workspaces/ws_001/invitations
{
  "email": "bob@example.com"
}
```

**기대 결과**:
```json
{
  "error": "ALREADY_MEMBER",
  "message": "이미 워크스페이스 멤버입니다.",
  "email": "bob@example.com"
}
```
HTTP 상태: 409 Conflict

### 시나리오 5: 미수락 초대 재발송

**전제 조건**: 동일 이메일로 `pending` 상태의 초대가 이미 존재.

**처리 흐름**: 새 토큰 생성 없이 기존 초대의 이메일을 재발송한다.

**기대 결과**: 시나리오 1과 동일한 응답 구조 (기존 `invitation_id` 유지)

### 시나리오 6: 만료된 토큰으로 수락 시도

**전제 조건**: 초대 토큰의 만료 시간(72시간)이 경과.

**기대 결과**:
```json
{
  "error": "INVITATION_EXPIRED",
  "message": "초대가 만료되었습니다. 관리자에게 재초대를 요청해 주세요.",
  "expired_at": "2026-03-15T10:30:00Z"
}
```
HTTP 상태: 410 Gone

### 시나리오 7: 이메일 발송 실패

**전제 조건**: 초대 생성은 성공했으나 이메일 서비스가 일시적으로 불가.

**처리 흐름**:
1. 초대 레코드 생성 (롤백하지 않음)
2. 상태를 `pending_email`로 기록
3. 관리자에게 발송 실패 알림

**기대 결과**: 초대 레코드는 유지되며, 관리자가 재발송을 트리거할 수 있다.

## 4. API 레퍼런스

### POST /workspaces/:workspace_id/invitations

워크스페이스에 새 멤버를 초대한다.

**URL 파라미터**:

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `workspace_id` | string | 필수 | 대상 워크스페이스 ID |

**요청 본문**:

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `email` | string | 필수 | 초대할 사용자의 이메일 주소 |

**성공 응답** (201 Created):

| 필드 | 타입 | 설명 |
|------|------|------|
| `invitation_id` | string | 초대 고유 식별자 |
| `workspace_id` | string | 워크스페이스 ID |
| `email` | string | 초대 대상 이메일 |
| `status` | string | `"pending"` 또는 `"pending_email"` |
| `expires_at` | string (ISO 8601) | 만료 시각 (생성 시점 + 72시간) |
| `created_at` | string (ISO 8601) | 생성 시각 |

**에러 응답**:

| HTTP 상태 | 에러 코드 | 상황 |
|-----------|----------|------|
| 403 | `FORBIDDEN` | 관리자 권한 없음 |
| 404 | `WORKSPACE_NOT_FOUND` | 존재하지 않는 워크스페이스 |
| 409 | `ALREADY_MEMBER` | 이미 멤버인 사용자 |
| 422 | `INVALID_EMAIL` | 이메일 형식 오류 |

---

### POST /invitations/:token/accept

초대를 수락하고 워크스페이스에 합류한다.

**URL 파라미터**:

| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `token` | string | 필수 | 초대 토큰 |

**성공 응답** (200 OK):

| 필드 | 타입 | 설명 |
|------|------|------|
| `status` | string | `"accepted"` 또는 `"redirect_to_signup"` |
| `workspace_id` | string | 합류한 워크스페이스 ID |
| `member` | object | 멤버 정보 (계정 있는 경우) |
| `redirect_url` | string | 가입 리다이렉트 URL (계정 없는 경우) |

**에러 응답**:

| HTTP 상태 | 에러 코드 | 상황 |
|-----------|----------|------|
| 404 | `INVITATION_NOT_FOUND` | 존재하지 않는 토큰 |
| 410 | `INVITATION_EXPIRED` | 만료된 초대 |

**호출 예시**:

```bash
# 초대 생성
curl -X POST /api/v1/workspaces/ws_001/invitations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <admin_token>" \
  -d '{"email": "alice@example.com"}'

# 초대 수락
curl -X POST /api/v1/invitations/tok_secure_abc/accept \
  -H "Authorization: Bearer <user_token>"
```

## 5. 구현 가이드

### 핵심 규칙

1. 이미 워크스페이스에 속한 사용자에게 중복 초대를 보내면 안 된다.
2. 초대 토큰은 유일하고 예측 불가능해야 하며, 72시간 만료를 가진다.
3. 만료된 토큰으로 수락 요청이 오면 실패 처리하고, 관리자에게 재초대를 안내한다.
4. 동일 이메일에 대한 미수락 초대가 이미 존재하면 기존 초대를 재발송한다.
5. 수락 시 계정 유무에 따라 즉시 등록 또는 가입 전환한다.
6. 이메일 발송 실패는 초대 생성을 롤백하지 않는다.

### 체크리스트

**구현 전**:
- [ ] 스펙에서 초대 상태 모델(`pending`, `pending_email`, `accepted`, `expired`)을 확인했다.
- [ ] 초대 API 엔드포인트를 확인했다.
- [ ] 토큰 생성 방식과 만료 정책(72시간)을 확인했다.

**구현 중**:
- [ ] 기존 멤버 중복 체크가 초대 생성 전에 실행된다.
- [ ] 동일 이메일 미수락 초대 존재 시 재발송 분기가 있다.
- [ ] 토큰 생성에 암호학적 난수를 사용한다.
- [ ] 이메일 발송 실패 시 상태가 `pending_email`로 남는다.
- [ ] 수락 시 만료 여부를 검증한다.

**완료/리뷰 전**:
- [ ] 정상 초대→수락 플로우 테스트가 있다.
- [ ] 중복 이메일 초대 시 재발송 테스트가 있다.
- [ ] 만료 토큰 수락 실패 테스트가 있다.
- [ ] 기존 멤버 초대 차단 테스트가 있다.
- [ ] 이메일 발송 실패 시 상태 확인 테스트가 있다.

### 안티패턴

- 초대 생성과 이메일 발송을 하나의 트랜잭션으로 묶어 발송 실패 시 초대 자체가 롤백되는 방식 — 네트워크 일시 장애로 초대 전체가 실패
- 토큰을 UUID v4가 아닌 순차 ID로 생성하여 예측 가능한 방식 — 토큰 추측 공격 가능
- 만료 검증 없이 토큰 존재 여부만으로 수락을 허용하는 방식 — 무기한 유효한 토큰 위험

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
