# Progress Log — RSIMC / DARSI-CS

## Current Verified State

- Repository root: `RSIMC/`
- Standard startup: `docker compose up -d` (from RSIMC/) or `.\scripts\start-dev.ps1` on Windows
- Verification path: health `GET /health`, frontend `npm run build`, kiosk flow with demo patient
- Current highest-priority unfinished feature: full Docker stack end-to-end (blocked when Docker Desktop is off)
- Current blocker: Docker Desktop daemon not running on dev machine during session 2026-07-01

## Session Log

### Session 2026-07-01

- Date: 2026-07-01
- Goal: Continue RSIMC — read docs, fix runnability
- Completed:
  - Fixed backend requirements.txt (invalid PyJWT/sqlalchemy lines)
  - Fixed async SQLAlchemy session setup (`async_sessionmaker`)
  - Added demo seed data (admin, node, patient, triage rules)
  - Added `/api/biometrics/verify-nik` and demo shortcuts for fingerprint/face
  - Fixed docker-compose (nginx optional profile, DEBUG dev mode, healthchecks)
  - Fixed frontends: Tailwind/postcss, duplicate session-store, AuthScreen imports, admin API URL
  - Both Next.js apps build successfully; backend imports verified
- Verification run:
  - `npm run build` — kiosk-ui ✓, admin-dashboard ✓
  - `python -c "from main import app"` — ✓
  - `docker compose build` — blocked (Docker daemon not running)
- Evidence captured: build output in terminal logs
- Commits: none (user did not request)
- Files updated: backend/, kiosk-ui/, admin-dashboard/, docker-compose.yml, GETTING_STARTED.md, scripts/start-dev.ps1
- Known risk: Docker Desktop must be running for one-command startup; Ollama optional (fallback triage rules work)
- Next best step: Start Docker Desktop → `docker compose up -d --build` → test kiosk flow with demo NIK `3573010101010001`
