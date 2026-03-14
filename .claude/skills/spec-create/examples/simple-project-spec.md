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

| Aspect | Description |
|--------|-------------|
| **Purpose** | Generate and resolve short URLs |
| **Why** | Core service encapsulating URL generation, resolution, and tracking in one place — separated from API layer to allow reuse across REST/CLI interfaces and independent testing of shortening logic |
| **Input** | Long URL or short code |
| **Output** | Short URL or redirect target |

**Source:**

- `src/services/url_service.py`: generate_short_code(), resolve_url(), track_click()
- `src/models/url.py`: URLModel, URLCreate

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
