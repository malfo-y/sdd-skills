# Example: Changelog Entries

Examples of well-formatted changelog entries for spec document updates.

---

## Full Changelog Entry (Major Update)

```markdown
## [2.0.0] - 2024-01-20

### Overview
Major update reflecting architecture changes and new video processing capabilities.

### Added
- **Video Processor Component**: New component for downloading videos and reels
  - Quality selection (high, medium, low)
  - Automatic retry on failure
  - Progress tracking
- **Proxy Rotation**: Automatic proxy rotation for reliability
  - Configurable rotation interval
  - Health checking for proxy pool
  - Fallback to direct connection
- **Excel Export**: Added .xlsx export format alongside JSON and CSV
- **Date Organization**: Image organizer now supports date-based folder structure
- **Thumbnail Generation**: Automatic thumbnail creation for previews

### Changed
- **Rate Limiting**: Reduced from 30 to 20 requests/minute for stability
  - Added burst limit of 5 requests
  - Added automatic retry on 429 responses
- **Installation**: Migrated from requirements.txt to pyproject.toml
- **Image Organizer**: Extended to support multiple organization strategies

### Deprecated
- `--output-format txt` flag (use `--output-format json` instead)

### Removed
- Legacy `config.ini` support (use environment variables or config.yaml)

### Fixed
- Memory leak in long-running processes (BUG-001)
- Unicode character handling in filenames (BUG-002)
- Incorrect timestamp parsing for posts older than 1 year

### Security
- Updated requests library to 2.31.0 (CVE-2023-XXXXX)

### Known Issues
- Carousel posts limited to first 10 images
- Video downloads may fail for private accounts

### Migration Guide
See [Migration from v1.x to v2.0](./MIGRATION.md)
```

---

## Standard Changelog Entry (Minor Update)

```markdown
## [1.3.0] - 2024-01-15

### Added
- Video download support via `--include-videos` flag
- Proxy configuration options in config.yaml
- New usage examples in documentation

### Changed
- Updated rate limit from 30 to 20 requests/minute
- Image organizer now supports date-based organization

### Fixed
- Memory leak in long-running sessions
- Unicode filename handling

### Documentation
- Added Video Processor component section
- Updated installation instructions for pyproject.toml
- Added proxy configuration examples
```

---

## Minimal Changelog Entry (Patch Update)

```markdown
## [1.2.1] - 2024-01-10

- Fixed typo in configuration example
- Updated Python version requirement to 3.11+
- Corrected API endpoint path in usage section
```

---

## Changelog Entry with Code References

```markdown
## [1.4.0] - 2024-01-25

### Added
- **Batch Processing** (`src/batch_processor.py`)
  - Process multiple profiles in single run
  - Configurable concurrency limit
  - Progress reporting

### Changed
- **Extractor** (`src/extractors/profile_extractor.py:45-89`)
  - Improved error handling for rate limits
  - Added exponential backoff

### Fixed
- **Image Organizer** (`src/image_organizer.py:123`)
  - Fixed race condition in parallel mode
  - Related: Issue #42, PR #45
```

---

## Changelog Entry with Breaking Changes Highlight

```markdown
## [3.0.0] - 2024-02-01

### ⚠️ Breaking Changes

1. **API Endpoint Changes**
   - `/api/extract` → `/api/v2/extract`
   - Response format changed (see Migration Guide)

2. **Configuration Format**
   - `config.ini` no longer supported
   - Must use `config.yaml` or environment variables

3. **Python Version**
   - Minimum Python version now 3.11 (was 3.9)

### Migration Required
Users upgrading from v2.x must:
1. Update configuration files
2. Modify API client code
3. Ensure Python 3.11+ installed

See [MIGRATION.md](./MIGRATION.md) for detailed steps.

### Added
- GraphQL API support
- Real-time progress webhooks
- Multi-account session management

### Removed
- Legacy REST API v1 endpoints
- INI configuration support
- Python 3.9 and 3.10 support
```

---

## Changelog Best Practices

### DO:
- Use consistent date format (YYYY-MM-DD)
- Group changes by type (Added, Changed, Fixed, etc.)
- Include issue/PR references where relevant
- Highlight breaking changes prominently
- Provide migration guidance for major versions

### DON'T:
- Include internal refactoring details
- List every commit message
- Use vague descriptions ("various fixes")
- Forget to update the version number
- Mix multiple versions in one entry

### Categories (Keep This Order):
1. **Added** - New features
2. **Changed** - Changes in existing functionality
3. **Deprecated** - Soon-to-be removed features
4. **Removed** - Removed features
5. **Fixed** - Bug fixes
6. **Security** - Vulnerability fixes
7. **Documentation** - Doc-only changes (optional)
8. **Known Issues** - New known issues (optional)

---

## Changelog Entry with Source Field Updates

```markdown
## [1.5.0] - 2024-02-10

### Source Field Updates
- **Auth Module** (`src/auth/`)
  - Added Source field: `src/auth/handler.py`: AuthHandler, login(), logout()
  - Added Source field: `src/auth/token.py`: TokenManager, verify_token()
- **Database Layer** (`src/db/`)
  - Updated Source field: `src/db/connection.py`: ConnectionPool → ConnectionManager (renamed)
  - Added new function to Source: `src/db/queries.py`: batch_insert()
- **API Layer** (`src/api/`)
  - Added Source field: `src/api/router.py`: APIRouter, register_routes()
  - Removed from Source: `src/api/legacy.py` (file deleted)

### Added
- **Auth Module** (`src/auth/`)
  - Token-based authentication with JWT support
  - | **Source** | `src/auth/token.py`: verify_token(), decode_jwt() |
  - |            | `src/auth/handler.py`: AuthHandler |

### Changed
- **Database Layer** (`src/db/`)
  - Renamed ConnectionPool to ConnectionManager for clarity
  - | **Source** | `src/db/connection.py`: ConnectionManager, get_pool(), release() |
  - |            | `src/db/queries.py`: execute_query(), batch_insert() |

### Documentation
- Updated all affected spec components with Source fields
- Added Source field to 4 previously undocumented components
```

---

## Linking Changelog to Spec

In the main spec document, reference the changelog:

```markdown
## Changelog

For detailed version history, see [CHANGELOG.md](./CHANGELOG.md).

### Recent Changes (v1.3.0)
- Added video download support
- Improved proxy handling
- Fixed memory leak issues

[View full changelog →](./CHANGELOG.md)
```
