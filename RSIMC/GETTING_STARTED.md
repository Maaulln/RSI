# Getting Started

## Quick Start (5 minutes)

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone or download the RSIMC folder
cd RSIMC

# 2. Copy environment file
cp .env.example .env

# 3. Start all services
docker-compose up -d

# 4. Open in browser
# Kiosk: http://localhost:3000
# Admin: http://localhost:3001
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:password@localhost:5432/darsi_db
export REDIS_URL=redis://localhost:6379/0
python main.py
```

**Kiosk Frontend:**
```bash
cd kiosk-ui
npm install
npm run dev
# Open http://localhost:3000
```

**Admin Dashboard:**
```bash
cd admin-dashboard
npm install
npm run dev
# Open http://localhost:3001
```

## Key Features to Try

### 1. Kiosk UI (Patient Side)
- **Welcome Screen**: Start button with friendly interface
- **Authentication**: Try all three methods (fingerprint simulation, face, NIK)
- **Triage**: Enter symptoms by voice or text
- **Results**: See recommended department and urgency level

### 2. Admin Dashboard
- Monitor node status in real-time
- View analytics and statistics
- Manage triage rules
- Check pharmacy queue
- Review system health

## Configuration

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `SECRET_KEY` | JWT signing key | Must change |
| `DATABASE_URL` | PostgreSQL connection | localhost:5432 |
| `REDIS_URL` | Redis cache connection | localhost:6379 |
| `OLLAMA_URL` | LLM service URL | localhost:11434 |
| `MY_ERSIY_API_KEY` | Integration API key | Requires setup |
| `BPJS_API_KEY` | Insurance API key | Requires setup |

### Demo Patient (Development)

For testing authentication without real biometric hardware:

| Method | Test Input |
|--------|------------|
| Fingerprint | Auto-verifies on screen (uses `mock_fingerprint_data`) |
| Face | Auto-verifies on screen (uses `mock_face_encoding`) |
| NIK | `3573010101010001` (Budi Santoso) |

### Default Credentials

**Admin User:**
- Email: `admin@darsi.local`
- Password: `admin123` (change in production!)

**System Endpoints:**
- API: http://localhost:8000
- Kiosk: http://localhost:3000
- Admin: http://localhost:3001
- Database: localhost:5432
- Redis: localhost:6379

## Development Workflow

### Making Changes

**Backend (Python/FastAPI):**
```bash
cd backend
# Edit files in app/
# Changes auto-reload in development mode
```

**Frontend (TypeScript/React):**
```bash
cd kiosk-ui
# or
cd admin-dashboard
# Edit files in app/ or components/
# Next.js hot-reloads automatically
```

### Database Migrations

```bash
# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migration
docker-compose exec backend alembic upgrade head
```

## Testing the System

### 1. Test Authentication Flow
1. Open kiosk at http://localhost:3000
2. Click "MULAI KONSULTASI"
3. Try fingerprint verification
4. System should authenticate simulated patient

### 2. Test Triage Assessment
1. After auth, enter complaint: "Saya demam dan batuk"
2. Speak or type symptoms
3. System analyzes and recommends department
4. Check confidence score

### 3. Test Admin Dashboard
1. Open http://localhost:3001
2. View system overview
3. Check node status
4. Review recent activities

### 4. Test API Directly
```bash
# Health check
curl http://localhost:8000/health

# API documentation
curl http://localhost:8000/docs

# List nodes
curl http://localhost:8000/api/nodes
```

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process
lsof -i :3000  # for port 3000
kill -9 <PID>

# Or change ports in docker-compose.yml
```

### Database Connection Error
```bash
# Check PostgreSQL
docker-compose logs postgres

# Reset database
docker-compose exec postgres psql -U darsi_user -d darsi_db
```

### Services Not Starting
```bash
# Check all containers
docker-compose ps

# View specific logs
docker-compose logs <service_name>

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

## Next Steps

1. **Customize Configuration**: Edit `.env` for your environment
2. **Add Triage Rules**: Create rules matching your hospital's protocols
3. **Configure Integrations**: Set up My eRSIy, BPJS, SIM RS connections
4. **Deploy to Production**: Follow [DEPLOYMENT.md](./DEPLOYMENT.md)
5. **Train Staff**: Set up node hardware and train users

## Support & Resources

- **API Documentation**: http://localhost:8000/docs
- **Architecture**: See `docs/ARCHITECTURE.md`
- **Database**: See `docs/DATABASE.md`
- **Deployment**: See `docs/DEPLOYMENT.md`

## System Requirements

### Minimum
- 2 CPU cores
- 4GB RAM
- 20GB storage
- Ubuntu 20.04+

### Recommended
- 4 CPU cores
- 8GB RAM
- 50GB SSD
- Ubuntu 22.04 LTS

## License

This project is proprietary software for RSI A. Yani Surabaya.
