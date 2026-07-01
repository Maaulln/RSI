# Architecture Overview

## System Architecture

DARSI-CS is built on a modern microservices architecture with the following components:

```
┌─────────────────────────────────────────────────────────────┐
│                   KIOSK NODES (Android)                     │
│                   - Next.js UI                              │
│                   - Voice Input (STT)                       │
│                   - Biometric Auth                          │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTPS/WSS
┌────────────────▼────────────────────────────────────────────┐
│              NGINX REVERSE PROXY                            │
│              - SSL Termination                              │
│              - Rate Limiting                                │
└────────────────┬────────────────────────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────┐  ┌────────┐  ┌──────────┐
│Kiosk   │  │Admin   │  │FastAPI   │
│UI      │  │Panel   │  │Backend   │
│:3000   │  │:3001   │  │:8000     │
└────────┘  └────────┘  └────┬─────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
    ┌────────┐           ┌────────┐          ┌────────┐
    │Postgres│           │ Redis  │          │Ollama  │
    │ :5432  │           │:6379   │          │:11434  │
    └────────┘           └────────┘          └────────┘

External Integrations:
├── My eRSIy API
├── BPJS/JKN API
├── SIM RS
└── Whisper, TTS, OCR Services
```

## Component Details

### Frontend Layer
- **Kiosk UI** (port 3000): Patient-facing interface with large text and buttons for elderly users
- **Admin Dashboard** (port 3001): System administration and monitoring

### Backend Layer
- **FastAPI** (port 8000): Main API server handling all business logic
- **PostgreSQL** (port 5432): Primary database for persistent data
- **Redis** (port 6379): Cache layer and session management
- **Ollama** (port 11434): Local LLM service for triage and decision-making

### Integration Layer
- **My eRSIy API**: Patient electronic medical records
- **BPJS/JKN API**: Insurance verification
- **SIM RS**: Hospital information system
- **AI Services**: STT, TTS, OCR, Face Recognition

## Data Flow

### Typical Patient Flow
1. Patient arrives at kiosk
2. Biometric authentication (fingerprint, face, or OCR KTP)
3. Voice/text input of symptoms
4. LLM-based triage assessment
5. Department recommendation
6. Confirmation and queue assignment

### Authentication Flow
1. User selects auth method
2. Frontend captures biometric/KTP data
3. Backend verifies against BPJS/My eRSIy
4. JWT token issued for session
5. All subsequent requests include token

## Security

- **Encryption**: AES-256 for sensitive data at rest
- **HTTPS/TLS**: All communications encrypted in transit
- **RBAC**: Role-based access control for different user types
- **Audit Logging**: All data access recorded for compliance
- **Private Network**: Hospital LAN only, no internet exposure

## Scalability

- Stateless backend allows horizontal scaling
- Redis for distributed caching
- PostgreSQL replication ready
- Docker containers for easy deployment
- Can run multiple kiosk nodes independently

## Monitoring & Observability

- Health checks on all services
- Performance metrics via Prometheus
- Distributed tracing with OpenTelemetry
- Error tracking with Sentry
- Admin dashboard with real-time metrics
