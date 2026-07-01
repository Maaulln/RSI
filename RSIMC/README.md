# DARSI-CS (DARSI Customer Service)
## Hospital AI Assistant Kiosk System for RSI A. Yani Surabaya

Complete implementation of an AI-powered hospital customer service system with voice interaction, biometric verification, and avatar guidance.

## Project Structure

```
RSIMC/
├── backend/                  # FastAPI Backend
│   ├── app/
│   ├── services/
│   ├── models/
│   ├── api/
│   ├── config/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── main.py
├── kiosk-ui/                 # Kiosk Frontend (Next.js)
│   ├── app/
│   ├── components/
│   ├── services/
│   ├── styles/
│   ├── package.json
│   └── next.config.js
├── admin-dashboard/          # Admin Dashboard (Next.js)
│   ├── app/
│   ├── components/
│   ├── features/
│   ├── package.json
│   └── next.config.js
├── docker-compose.yml        # Local development setup
├── .env.example              # Environment configuration
└── docs/                     # Documentation
```

## Quick Start

### 1. Clone and Setup
```bash
cd RSIMC
cp .env.example .env
```

### 2. Using Docker Compose
```bash
docker-compose up -d
```

### 3. Manual Development
```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Kiosk Frontend (new terminal)
cd kiosk-ui
npm install
npm run dev

# Admin Dashboard (new terminal)
cd admin-dashboard
npm install
npm run dev
```

## Services

- **Kiosk UI**: http://localhost:3000
- **Admin Dashboard**: http://localhost:3001
- **FastAPI Backend**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Database Schema](docs/DATABASE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## Tech Stack

- **Frontend**: Next.js 14, React, Tailwind CSS
- **Backend**: FastAPI, Python
- **AI Services**: Ollama, Whisper, Coqui TTS
- **Database**: PostgreSQL, Redis
- **Infrastructure**: Docker, Docker Compose, Nginx
- **Monitoring**: Prometheus, Grafana

## Features

- ✅ Biometric Authentication (Fingerprint, Face, OCR KTP)
- ✅ Voice Interaction (STT + LLM + TTS)
- ✅ Avatar Integration
- ✅ Patient Triage Flow
- ✅ Admin Dashboard
- ✅ Real-time Monitoring
- ✅ Integration with Hospital APIs (My eRSIy, SIM RS, BPJS)

## Development Team

- **Backend**: Yardan
- **Kiosk UI**: Bagus
- **Admin Dashboard**: Bagus
- **AI Services**: Irawan

## License

Internal - RSI A. Yani Surabaya
