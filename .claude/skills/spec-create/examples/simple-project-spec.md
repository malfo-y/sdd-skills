# Simple Project Spec Example

Use this template for small projects with 1-3 components.

---

# URL Shortener

## Goal

Create a simple URL shortening service that converts long URLs into short, shareable links.

### Key Features
1. Generate short URLs from long URLs
2. Redirect short URLs to original destination
3. Track click counts
4. API-first design

### Target Users
- Developers needing programmatic URL shortening
- Content creators sharing links on social media

## Architecture Overview

```
┌──────────┐     ┌─────────────┐     ┌──────────┐
│  Client  │────▶│   FastAPI   │────▶│  SQLite  │
└──────────┘     └─────────────┘     └──────────┘
                       │
                       ▼
                 ┌──────────┐
                 │  Redis   │
                 │ (Cache)  │
                 └──────────┘
```

**Technology Stack:**
- Python 3.11
- FastAPI
- SQLite (production: PostgreSQL)
- Redis for caching

## Component Details

### Component: URL Service

#### Overview

사용자가 긴 URL을 제출하면 Base62 인코딩으로 6자리 단축 코드를 생성하고 SQLite에 저장한다. 단축 URL로 접속하면 Redis 캐시를 먼저 확인하고, 캐시 미스 시 DB에서 원본 URL을 조회하여 301 리다이렉트한다. 동시에 클릭 카운트를 비동기로 증가시킨다.

캐시 우선(cache-first) 전략을 채택한 이유는 읽기(리다이렉트)가 쓰기(생성)보다 압도적으로 많은 트래픽 패턴 때문이다. Repository 패턴으로 저장소를 분리하여 SQLite에서 PostgreSQL로의 전환을 용이하게 했다.

| Aspect | Description |
|--------|-------------|
| **Purpose** | Generate and resolve short URLs |
| **Input** | Long URL or short code |
| **Output** | Short URL or redirect target |

**Key Files:**
- `src/services/url_service.py` - Core logic
- `src/models/url.py` - URL model

**Implementation:**
- Uses base62 encoding for short codes
- Collision detection with retry
- Cache-through pattern for lookups

## Environment & Dependencies

### Directory Structure
```
url-shortener/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── models/
│   └── services/
├── tests/
├── .env.example
└── requirements.txt
```

### Dependencies
```
fastapi>=0.100.0
uvicorn>=0.23.0
sqlalchemy>=2.0.0
redis>=4.6.0
```

### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| DATABASE_URL | Yes | Database connection |
| REDIS_URL | No | Redis for caching |
| BASE_URL | Yes | Base URL for short links |

## Identified Issues & Improvements

### Missing Features
- [ ] Custom short codes
- [ ] Link expiration
- [ ] Analytics dashboard

### Technical Debt
- [ ] Add rate limiting
- [ ] Implement proper error responses

## Usage Examples

### Create Short URL
```bash
curl -X POST http://localhost:8000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very/long/path"}'

# Response: {"short_url": "http://localhost:8000/abc123"}
```

### Redirect
```bash
curl -L http://localhost:8000/abc123
# Redirects to original URL
```
