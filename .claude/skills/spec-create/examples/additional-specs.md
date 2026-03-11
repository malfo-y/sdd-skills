# Additional Spec Examples

Real-world examples of spec documents for different project types.

---

## Example 1: CLI Tool Spec

```markdown
# File Organizer CLI

## Goal

Automate file organization by moving files into categorized folders based on file type, date, or custom rules.

### Key Features
1. Organize by file extension (images, documents, videos)
2. Organize by date (year/month structure)
3. Custom rule support via config file
4. Dry-run mode to preview changes
5. Undo functionality

### Target Users
- Power users managing large download folders
- Photographers organizing photo libraries
- System administrators automating cleanup tasks

## Architecture Overview

```
┌─────────────────────────────────────────┐
│              CLI Interface               │
│         (Click/Typer framework)          │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────┼──────────────────────┐
│                  ▼                       │
│  ┌────────────────────────────────┐     │
│  │        Rule Engine             │     │
│  │  - Extension rules             │     │
│  │  - Date rules                  │     │
│  │  - Custom regex rules          │     │
│  └────────────────────────────────┘     │
│                  │                       │
│  ┌───────────────┼───────────────┐      │
│  ▼               ▼               ▼      │
│ ┌─────┐     ┌─────────┐    ┌────────┐  │
│ │Scan │     │Organize │    │ Undo   │  │
│ │Files│     │ Files   │    │ Stack  │  │
│ └─────┘     └─────────┘    └────────┘  │
└─────────────────────────────────────────┘
```

## Component Details

### Component: Rule Engine

| Aspect | Description |
|--------|-------------|
| **Purpose** | Match files to destination folders |
| **Why** | Separated from file operations to allow rules to be tested, extended, and configured independently. Chain of responsibility pattern enables adding new rule types (regex, size-based) without modifying scanner or mover logic |
| **Input** | File path, configuration rules |
| **Output** | Target folder path or None |

**Implementation:**
- Uses chain of responsibility pattern
- Each rule type is a separate handler
- Rules evaluated in priority order

### Component: File Scanner

| Aspect | Description |
|--------|-------------|
| **Purpose** | Recursively scan directories |
| **Why** | Decoupled from rule engine so scanning can handle symlinks, permission errors, and large directory trees independently. Also allows swapping scan strategies (recursive vs flat) without affecting rule evaluation |
| **Input** | Source directory path |
| **Output** | List of file paths with metadata |

## Environment & Dependencies

### Dependencies
- Python 3.9+
- click (CLI framework)
- pathlib (file operations)

### Configuration
```yaml
# config.yaml
rules:
  - name: images
    extensions: [.jpg, .png, .gif]
    destination: ~/Pictures/Organized
  - name: documents
    extensions: [.pdf, .doc, .docx]
    destination: ~/Documents/Organized
```

## Usage Examples

### Basic Usage
```bash
# Organize downloads folder
file-organizer organize ~/Downloads

# Dry run
file-organizer organize ~/Downloads --dry-run

# Undo last operation
file-organizer undo
```
```

---

## Example 2: Web API Spec

```markdown
# Task Management API

## Goal

RESTful API for managing tasks and projects with team collaboration features.

### Key Features
1. CRUD operations for tasks and projects
2. User authentication and authorization
3. Real-time notifications via WebSocket
4. File attachments support
5. Activity logging

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  API Gateway                     │
│              (Rate limiting, Auth)               │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────┼────────────────────────────┐
│                    ▼                             │
│  ┌──────────────────────────────────────┐       │
│  │           FastAPI Router             │       │
│  │  /tasks  /projects  /users  /auth    │       │
│  └──────────────────────────────────────┘       │
│                    │                             │
│     ┌──────────────┼──────────────┐             │
│     ▼              ▼              ▼             │
│ ┌────────┐   ┌──────────┐   ┌─────────┐        │
│ │ Task   │   │ Project  │   │  User   │        │
│ │Service │   │ Service  │   │ Service │        │
│ └───┬────┘   └────┬─────┘   └────┬────┘        │
└─────┼─────────────┼──────────────┼──────────────┘
      │             │              │
      └─────────────┼──────────────┘
                    │
┌───────────────────┼─────────────────────────────┐
│                   ▼                              │
│  ┌────────────┐  ┌────────────┐  ┌───────────┐ │
│  │ PostgreSQL │  │   Redis    │  │    S3     │ │
│  │  (Data)    │  │  (Cache)   │  │ (Files)   │ │
│  └────────────┘  └────────────┘  └───────────┘ │
└─────────────────────────────────────────────────┘
```

## Component Details

### Component: Task Service

| Aspect | Description |
|--------|-------------|
| **Purpose** | Business logic for task operations |
| **Why** | Extracted from route handlers to keep API layer thin and testable. Centralizes permission checks, validation, and notification triggers so that multiple entry points (REST, WebSocket, CLI) share the same business rules |
| **Input** | Task DTOs, user context |
| **Output** | Task models, validation errors |

**Key Operations:**
- `create_task(data, user)` - Create with validation
- `update_task(id, data, user)` - Update with permissions
- `list_tasks(filters, pagination)` - Filtered listing
- `assign_task(id, assignee)` - Assignment with notification

## API Reference

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/tasks | List tasks |
| POST | /api/v1/tasks | Create task |
| GET | /api/v1/tasks/{id} | Get task |
| PUT | /api/v1/tasks/{id} | Update task |
| DELETE | /api/v1/tasks/{id} | Delete task |

### Example Request
```http
POST /api/v1/tasks
Authorization: Bearer eyJ...
Content-Type: application/json

{
  "title": "Implement login",
  "description": "Add OAuth2 login flow",
  "project_id": "proj_123",
  "priority": "high",
  "due_date": "2024-03-15"
}
```

## Identified Issues & Improvements

### Missing Features
- [ ] Recurring tasks
- [ ] Task templates
- [ ] Bulk operations

### Performance
- [ ] Add query caching for list endpoints
- [ ] Optimize N+1 queries in project listing
```

---

## Example 3: Data Pipeline Spec

```markdown
# Instagram Data Pipeline

## Goal

Extract, transform, and load Instagram profile and post data for analytics.

### Key Features
1. Profile metadata extraction
2. Post/Reel content download
3. Engagement metrics collection
4. Scheduled batch processing
5. Data quality validation

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   Scheduler (Cron)                   │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────┐
│                        ▼                             │
│  ┌────────────────────────────────────────┐         │
│  │            Pipeline Orchestrator        │         │
│  │         (Apify/Prefect/Airflow)         │         │
│  └────────────────────────────────────────┘         │
│                        │                             │
│     ┌──────────────────┼──────────────────┐         │
│     ▼                  ▼                  ▼         │
│ ┌────────┐       ┌──────────┐       ┌─────────┐    │
│ │Extract │──────▶│Transform │──────▶│  Load   │    │
│ │ Stage  │       │  Stage   │       │  Stage  │    │
│ └────────┘       └──────────┘       └─────────┘    │
│     │                  │                  │         │
│     │                  │                  │         │
└─────┼──────────────────┼──────────────────┼─────────┘
      │                  │                  │
      ▼                  ▼                  ▼
┌──────────┐      ┌──────────┐       ┌──────────┐
│Instagram │      │  Local   │       │ Database │
│   API    │      │ Storage  │       │ / Cloud  │
└──────────┘      └──────────┘       └──────────┘
```

## Component Details

### Component: Extractor

| Aspect | Description |
|--------|-------------|
| **Purpose** | Fetch data from Instagram |
| **Why** | Isolated from transform/load stages because extraction involves rate limiting, proxy rotation, and session management — concerns orthogonal to data processing. Separation allows retrying extraction independently without re-processing already-fetched data |
| **Input** | Profile URLs, credentials, config |
| **Output** | Raw JSON data, media files |

**Implementation:**
- Handles rate limiting with exponential backoff
- Proxy rotation for reliability
- Session management for authentication

### Component: Transformer

| Aspect | Description |
|--------|-------------|
| **Purpose** | Clean and structure raw data |
| **Why** | Raw API responses change frequently and contain inconsistent formats. A dedicated transform stage absorbs API schema changes without affecting extraction or loading logic, and provides a single place for data quality validation |
| **Input** | Raw JSON from extractor |
| **Output** | Normalized data models |

**Transformations:**
- Timestamp normalization (UTC)
- Engagement rate calculation
- Media URL validation
- Duplicate detection

## Data Models

### Profile
```python
@dataclass
class Profile:
    username: str
    full_name: str
    bio: str
    follower_count: int
    following_count: int
    post_count: int
    is_verified: bool
    profile_pic_url: str
    extracted_at: datetime
```

### Post
```python
@dataclass
class Post:
    shortcode: str
    profile_username: str
    caption: str
    like_count: int
    comment_count: int
    media_type: str  # image, video, carousel
    media_urls: List[str]
    posted_at: datetime
    extracted_at: datetime
```

## Environment & Dependencies

### Dependencies
- Python 3.10+
- apify-client (data extraction)
- pandas (data transformation)
- sqlalchemy (database operations)

### Configuration
```python
# config.py
PROXY_CONFIG = {
    "enabled": True,
    "rotation_interval": 60,  # seconds
}

RATE_LIMIT = {
    "requests_per_minute": 30,
    "retry_attempts": 3,
}
```

## Identified Issues & Improvements

### Robustness
- [ ] Handle Instagram API changes gracefully
- [ ] Add data validation checksums
- [ ] Implement dead letter queue for failures

### Performance
- [ ] Parallelize media downloads
- [ ] Add incremental extraction mode
```
