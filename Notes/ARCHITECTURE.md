# ARCHITECTURE — DARSI Customer Service

**Versi:** 1.0
**Terakhir diperbarui:** 30 Juni 2026
**Tim:** IT — KP PENS PSDKU Lamongan 2024

## Gambaran Arsitektur Keseluruhan

```mermaid
flowchart TD
    subgraph KLIEN["Klien"]
        AB["🖥️ Admin Browser\nDesktop / Laptop"]
        KW["📱 Kiosk Node\nAndroid WebView × 6\nWebcam · Fingerprint · Speaker · Mic"]
    end

    subgraph INFRA["Infrastruktur (Private Network RS)"]
        NGX["Nginx\nReverse Proxy · SSL · Rate Limiting"]

        subgraph FE["Frontend (Next.js 14)"]
            ADM["darsi-admin\n:3001"]
            KSK["darsi-kiosk\n:3000"]
        end

        subgraph BE["darsi-backend (FastAPI :8000)"]
            direction TB
            AUTH2["Auth & Session"]
            ADMINAPI2["Admin API"]
            KIOSKAPI["Kiosk API"]
            WS["WebSocket Manager\nnode-status · pharmacy-queue"]
            INTCLIENT["Integration Client\nMy eRSIy · SIM RS · BPJS"]
            AICLIENT["AI Client\nHTTP ke darsi-ai services"]
        end

        subgraph DB["Database"]
            PG[("PostgreSQL :5432\nsesi · log · triage · user")]
            MY[("MySQL :3306\nintegrasi SIM RS")]
        end

        RD[("Redis :6379\ncache · session state")]

        subgraph AI["darsi-ai (Irawan)"]
            STT["STT\nWhisper Large-v3-Turbo\n:8001"]
            TTS["TTS\nVITS/MMS Indonesia\n:8002"]
            OCR2["OCR\nChandra\n:8003"]
            FACE["Face Recognition\nInsightFace ArcFace\n:8004"]
            RAG["RAG\nBGE-M3\n:8005"]
            DLG["Dialog Flow Manager\nLiveKit Agent\n:8006"]
        end

        LK["LiveKit Server\n:7880"]
        OL["Ollama\nSahabat-AI 8B / Qwen3-8B\n:11434"]
    end

    subgraph EXT["Integrasi Eksternal"]
        ER["My eRSIy API"]
        SR["SIM RS"]
        BJ["BPJS/JKN API"]
    end

    AB -->|"HTTPS"| NGX
    KW -->|"HTTPS / WSS"| NGX
    NGX --> ADM & KSK & BE
    BE --> DB & RD
    BE --> AI
    BE --> OL
    BE --> INTCLIENT
    INTCLIENT --> EXT
    DLG <-->|"WSS"| LK
    KW <-->|"WSS"| LK

    classDef klien fill:#7F77DD,stroke:#534AB7,color:#fff
    classDef fe fill:#1D9E75,stroke:#0F6E56,color:#fff
    classDef be fill:#1D9E75,stroke:#0F6E56,color:#fff
    classDef db fill:#378ADD,stroke:#185FA5,color:#fff
    classDef cache fill:#E24B4A,stroke:#A32D2D,color:#fff
    classDef ai fill:#BA7517,stroke:#854F0B,color:#fff
    classDef ext fill:#888780,stroke:#5F5E5A,color:#fff
    classDef infra fill:#333,stroke:#111,color:#fff

    class AB,KW klien
    class ADM,KSK fe
    class AUTH2,ADMINAPI2,KIOSKAPI,WS,INTCLIENT,AICLIENT be
    class PG,MY db
    class RD cache
    class STT,TTS,OCR2,FACE,RAG,DLG ai
    class ER,SR,BJ ext
    class NGX,LK,OL infra
```

## Peta Port & Service

| Service | Port | Repo | Owner |
|---|---|---|---|
| Nginx | 80 / 443 | darsi-backend | Yardan |
| darsi-admin (Next.js) | 3001 | darsi-admin | Bagus |
| darsi-kiosk (Next.js) | 3000 | darsi-kiosk | Bagus |
| darsi-backend (FastAPI) | 8000 | darsi-backend | Yardan |
| PostgreSQL | 5432 | darsi-backend | Yardan |
| MySQL | 3306 | darsi-backend | Yardan |
| Redis | 6379 | darsi-backend | Yardan |
| Ollama (LLM) | 11434 | darsi-ai | Irawan |
| LiveKit Server | 7880 | darsi-ai | Irawan |
| STT — Whisper Large-v3-Turbo | 8001 | darsi-ai | Irawan |
| TTS — VITS/MMS Indonesia | 8002 | darsi-ai | Irawan |
| OCR — Chandra | 8003 | darsi-ai | Irawan |
| Face Recognition — InsightFace | 8004 | darsi-ai | Irawan |
| RAG — BGE-M3 | 8005 | darsi-ai | Irawan |
| Dialog Flow Manager | 8006 | darsi-ai | Irawan |

## Struktur Repository

Proyek menggunakan pendekatan multi-repo — setiap komponen utama memiliki repo sendiri sesuai jobdesk.

```
GitHub Org / Akun Tim
│
├── darsi-admin/      ← Bagus   — Dashboard Admin (Next.js 14)
├── darsi-kiosk/      ← Bagus   — Kiosk UI (Next.js 14, static export)
├── darsi-backend/    ← Yardan  — FastAPI + PostgreSQL + MySQL + Redis + Integrasi
├── darsi-ai/         ← Irawan  — STT · TTS · OCR · Face · RAG · Dialog · Ollama
└── RSI/              ← Tim     — Dokumentasi, PRD, ARCHITECTURE (repo ini)
```

## Detail Tiap Komponen

### 1. darsi-admin — Dashboard Admin (Bagus)

**Tech:** Next.js 14 App Router, Tailwind CSS, TanStack Query, Zustand, native WebSocket

```
darsi-admin/
├── public/
│   └── favicon.ico
├── src/
│   ├── app/
│   │   ├── layout.tsx                   # Root layout, provider wrapper
│   │   ├── page.tsx                     # Redirect → /overview
│   │   ├── (auth)/
│   │   │   └── login/
│   │   │       └── page.tsx
│   │   └── (dashboard)/
│   │       ├── layout.tsx               # AppShell: Sidebar + Topbar
│   │       ├── overview/
│   │       │   └── page.tsx             # Statistik cards + grafik 24 jam + alert
│   │       ├── nodes/
│   │       │   ├── page.tsx             # Tabel node + real-time status
│   │       │   └── [id]/
│   │       │       └── page.tsx         # Detail & history node
│   │       ├── avatars/
│   │       │   └── page.tsx             # Grid galeri + upload VRM
│   │       ├── monitoring/
│   │       │   └── page.tsx             # Grafik interaksi + log percakapan
│   │       ├── triage/
│   │       │   └── page.tsx             # Tabel rule + form + test panel
│   │       └── pharmacy/
│   │           └── page.tsx             # Antrian obat real-time
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Topbar.tsx
│   │   │   └── AppShell.tsx
│   │   └── ui/
│   │       ├── Badge.tsx                # Status badge (online/offline/error)
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       ├── Modal.tsx
│   │       ├── Table.tsx
│   │       ├── StatusDot.tsx            # Indikator real-time node
│   │       └── Chart.tsx                # Wrapper recharts
│   ├── features/
│   │   ├── nodes/
│   │   │   ├── NodeTable.tsx
│   │   │   ├── NodeEditModal.tsx
│   │   │   ├── NodeStatusBadge.tsx
│   │   │   ├── nodes.api.ts             # GET/POST/PATCH /admin/nodes
│   │   │   └── nodes.types.ts
│   │   ├── avatars/
│   │   │   ├── AvatarGrid.tsx
│   │   │   ├── AvatarUploadModal.tsx
│   │   │   ├── avatars.api.ts           # GET/POST/DELETE /admin/avatars
│   │   │   └── avatars.types.ts
│   │   ├── monitoring/
│   │   │   ├── MetricCards.tsx
│   │   │   ├── InteractionChart.tsx
│   │   │   ├── LogTable.tsx
│   │   │   ├── monitoring.api.ts        # GET /admin/analytics, /admin/logs
│   │   │   └── monitoring.types.ts
│   │   ├── triage/
│   │   │   ├── TriageTable.tsx
│   │   │   ├── TriageRuleModal.tsx
│   │   │   ├── TriageTestPanel.tsx
│   │   │   ├── triage.api.ts            # GET/POST/PATCH /admin/triage-rules
│   │   │   └── triage.types.ts
│   │   └── pharmacy/
│   │       ├── QueueDisplay.tsx
│   │       ├── QueueHistory.tsx
│   │       ├── pharmacy.api.ts          # WS /ws/pharmacy-queue
│   │       └── pharmacy.types.ts
│   ├── hooks/
│   │   ├── useAuth.ts                   # Login, logout, token refresh
│   │   ├── useNodeStatus.ts             # Subscribe WS /ws/node-status
│   │   └── usePharmacyQueue.ts          # Subscribe WS /ws/pharmacy-queue
│   ├── lib/
│   │   ├── api.ts                       # Axios instance + base URL + interceptor
│   │   ├── ws.ts                        # WebSocket manager (auto-reconnect)
│   │   └── queryClient.ts               # TanStack Query client config
│   ├── store/
│   │   └── authStore.ts                 # Zustand — token, user, isAuthenticated
│   └── types/
│       └── index.ts                     # Tipe shared lintas fitur
├── .env.local
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

**Mapping halaman ke endpoint:**

| Halaman | Method | Endpoint |
|---|---|---|
| Login | POST | `/auth/login` |
| Overview | GET | `/admin/overview` |
| Overview (live) | WS | `/ws/node-status` |
| Nodes — list | GET | `/admin/nodes` |
| Nodes — tambah | POST | `/admin/nodes` |
| Nodes — edit | PATCH | `/admin/nodes/{id}` |
| Nodes — toggle aktif | PATCH | `/admin/nodes/{id}` |
| Avatars — list | GET | `/admin/avatars` |
| Avatars — upload | POST | `/admin/avatars` |
| Avatars — hapus | DELETE | `/admin/avatars/{id}` |
| Avatars — assign ke node | PATCH | `/admin/nodes/{id}/avatar` |
| Monitoring — analytics | GET | `/admin/analytics?from=&to=&node_id=` |
| Monitoring — logs | GET | `/admin/logs?page=&node_id=` |
| Triage — list | GET | `/admin/triage-rules` |
| Triage — tambah | POST | `/admin/triage-rules` |
| Triage — edit | PATCH | `/admin/triage-rules/{id}` |
| Triage — test | POST | `/admin/triage-rules/test` |
| Triage — history | GET | `/admin/triage-rules/{id}/history` |
| Pharmacy — live | WS | `/ws/pharmacy-queue` |
| Pharmacy — history | GET | `/admin/pharmacy-queue/history` |

### 2. darsi-kiosk — Kiosk UI (Bagus)

**Tech:** Next.js 14 App Router, Tailwind CSS, native WebSocket
**Build:** `output: 'export'` — dijalankan sebagai static HTML/JS di Android WebView

```
darsi-kiosk/
├── public/
│   └── assets/
│       └── icons/                       # Ikon gejala SVG (untuk touch fallback)
├── src/
│   ├── app/
│   │   ├── layout.tsx                   # Fullscreen layout, no nav
│   │   ├── page.tsx                     # Screen idle / standby
│   │   └── session/
│   │       ├── identify/
│   │       │   └── page.tsx             # Pilih metode: Fingerprint / Face / KTP
│   │       ├── symptoms/
│   │       │   └── page.tsx             # Input gejala — voice utama, touch fallback
│   │       ├── result/
│   │       │   └── page.tsx             # Rekomendasi poli + cetak tiket
│   │       └── navigation/
│   │           └── page.tsx             # Peta arah ke poli / apotek
│   ├── components/
│   │   ├── VoiceInput.tsx               # Mic button + waveform visualizer
│   │   ├── TouchFallback.tsx            # Grid ikon gejala + keyboard layar
│   │   ├── CallStaff.tsx                # Tombol "Panggil Petugas" (always visible)
│   │   ├── CameraCapture.tsx            # Webcam stream untuk OCR / face
│   │   └── QueueDisplay.tsx             # Tampilan antrian besar (NODE-06)
│   ├── hooks/
│   │   ├── useVoice.ts                  # MediaRecorder → POST /ai/stt/transcribe
│   │   └── useNodeSession.ts            # WS session dengan backend
│   └── lib/
│       ├── api.ts                       # Fetch client ke FastAPI
│       └── ws.ts                        # WebSocket manager
├── .env.local
├── next.config.ts                       # output: 'export', basePath jika perlu
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

**Catatan kritis WebView Android:**
- `next.config.ts` wajib set `output: 'export'` — build menghasilkan folder `out/` berisi static HTML/JS/CSS
- Tidak boleh ada `Server Actions`, `API Routes`, atau `next/headers` — semua itu butuh Node.js server
- Semua request ke FastAPI menggunakan `fetch` / `axios` biasa dengan URL dari env
- `NEXT_PUBLIC_NODE_ID` di-set berbeda per device fisik saat deployment

### 3. darsi-backend — FastAPI Backend (Yardan)

**Tech:** FastAPI, SQLAlchemy (PostgreSQL + MySQL), Redis, Pydantic, Alembic, Gunicorn + Uvicorn

```
darsi-backend/
├── app/
│   ├── main.py                          # FastAPI app init, router mounting, CORS
│   ├── config.py                        # Settings via pydantic-settings (baca .env)
│   ├── dependencies.py                  # Shared FastAPI dependencies (get_db, get_current_user)
│   ├── database/
│   │   ├── postgres.py                  # SQLAlchemy engine + SessionLocal (PostgreSQL)
│   │   └── mysql.py                     # SQLAlchemy engine + SessionLocal (MySQL)
│   ├── cache/
│   │   └── redis.py                     # Redis client (aioredis)
│   ├── routers/
│   │   ├── auth.py                      # POST /auth/login, POST /auth/logout
│   │   ├── admin/
│   │   │   ├── nodes.py                 # GET/POST/PATCH /admin/nodes, /admin/nodes/{id}/avatar
│   │   │   ├── avatars.py               # GET/POST/DELETE /admin/avatars
│   │   │   ├── analytics.py             # GET /admin/analytics, /admin/logs
│   │   │   └── triage.py                # CRUD /admin/triage-rules + /test + /{id}/history
│   │   └── kiosk/
│   │       ├── session.py               # POST /kiosk/session/start, /end, /event
│   │       └── queue.py                 # GET /kiosk/queue/status, /admin/pharmacy-queue/history
│   ├── websocket/
│   │   ├── manager.py                   # ConnectionManager (broadcast ke subscribers)
│   │   ├── node_status.py               # WS /ws/node-status
│   │   └── pharmacy_queue.py            # WS /ws/pharmacy-queue
│   ├── models/
│   │   ├── postgres/
│   │   │   ├── user.py                  # Admin user
│   │   │   ├── node.py                  # Node config
│   │   │   ├── avatar.py                # Avatar metadata
│   │   │   ├── session.py               # Kiosk session log
│   │   │   ├── triage_rule.py           # Triage rule + audit trail
│   │   │   └── interaction_log.py       # Log percakapan per interaksi
│   │   └── mysql/
│   │       └── simrs_queue.py           # Read-only mirror antrian SIM RS
│   ├── schemas/
│   │   ├── auth.py                      # LoginRequest, TokenResponse
│   │   ├── node.py                      # NodeResponse, NodeUpdateRequest
│   │   ├── avatar.py                    # AvatarResponse, AvatarCreateRequest
│   │   ├── analytics.py                 # AnalyticsResponse, LogEntry
│   │   └── triage.py                    # TriageRuleResponse, TriageTestRequest
│   └── services/
│       ├── auth_service.py              # JWT encode/decode, hash password
│       ├── node_service.py              # Business logic node
│       ├── ai_client.py                 # HTTP client ke darsi-ai (STT, TTS, OCR, Face, RAG)
│       └── integration/
│           ├── ersimy.py                # My eRSIy API client
│           ├── simrs.py                 # SIM RS API client
│           └── bpjs.py                  # BPJS/JKN API client
├── alembic/
│   ├── versions/                        # File migrasi (auto-generated)
│   └── env.py
├── docker-compose.yml                   # Semua service produksi
├── docker-compose.dev.yml               # Override untuk dev (mount volume, no restart)
├── Dockerfile
├── requirements.txt
└── .env
```

### 4. darsi-ai — AI Layer (Irawan)

**Tech:** FastAPI (wrapper tiap model), faster-whisper, VITS/MMS, Chandra, InsightFace, BGE-M3, Ollama, LiveKit Agents SDK

```
darsi-ai/
├── stt/
│   ├── main.py                          # FastAPI: POST /transcribe
│   │                                    # Body: {audio_base64, language}
│   │                                    # Response: {text, language, confidence}
│   ├── model.py                         # faster-whisper WhisperModel loader
│   ├── requirements.txt                 # faster-whisper, fastapi, uvicorn
│   └── Dockerfile
│
├── tts/
│   ├── main.py                          # FastAPI: POST /synthesize
│   │                                    # Body: {text, language, speed}
│   │                                    # Response: {audio_base64, duration_ms}
│   ├── model.py                         # VITS/MMS model loader
│   ├── requirements.txt                 # TTS, fastapi, uvicorn
│   └── Dockerfile
│
├── ocr/
│   ├── main.py                          # FastAPI: POST /ocr/ktp, POST /ocr/rujukan
│   │                                    # Body: {image_base64}
│   │                                    # Response: {nik, nama, ...} / {nama, poli, tanggal}
│   ├── model.py                         # Chandra model loader (HF mode dev / vLLM prod)
│   ├── requirements.txt                 # transformers, fastapi, uvicorn, pillow
│   └── Dockerfile
│
├── face/
│   ├── main.py                          # FastAPI: POST /face/verify
│   │                                    # Body: {image_base64, reference_image_base64}
│   │                                    # Response: {match, confidence, embedding}
│   ├── model.py                         # InsightFace ArcFace loader (CPU)
│   ├── requirements.txt                 # insightface, fastapi, uvicorn, opencv-python
│   └── Dockerfile
│
├── rag/
│   ├── main.py                          # FastAPI: POST /embed, POST /search
│   │                                    # /embed body: {text} → {embedding: float[]}
│   │                                    # /search body: {query, top_k} → {results}
│   ├── model.py                         # BGE-M3 model loader + vector store (FAISS / ChromaDB)
│   ├── requirements.txt                 # FlagEmbedding, faiss-cpu, fastapi, uvicorn
│   └── Dockerfile
│
├── dialog/
│   ├── main.py                          # FastAPI: POST /dialog/start, /dialog/turn
│   ├── agent.py                         # LiveKit Agents SDK entry point
│   ├── flows/
│   │   ├── base.py                      # Base dialog flow class
│   │   ├── registration.yaml            # Dialog flow NODE-01 (pendaftaran)
│   │   ├── navigation.yaml              # Dialog flow NODE-03, NODE-05 (navigasi)
│   │   ├── assessment.yaml              # Dialog flow NODE-04 (asesmen poli)
│   │   └── pharmacy.yaml                # Dialog flow NODE-06 (apotek)
│   ├── requirements.txt                 # livekit-agents, livekit, fastapi, uvicorn
│   └── Dockerfile
│
└── docker-compose.ai.yml                # Jalankan semua AI service sekaligus (untuk dev)
```

## Infrastruktur — Docker Compose

File `docker-compose.yml` di root `darsi-backend/` mengatur seluruh service produksi.

```yaml
services:

  # ── Reverse Proxy ────────────────────────────────────────────────
  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - admin
      - kiosk
      - backend
    restart: always

  # ── Frontend ─────────────────────────────────────────────────────
  admin:
    build:
      context: ../darsi-admin
      dockerfile: Dockerfile
    ports:
      - "3001:3001"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
      - NEXT_PUBLIC_WS_URL=ws://backend:8000
    restart: always

  kiosk:
    build:
      context: ../darsi-kiosk
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
      - NEXT_PUBLIC_WS_URL=ws://backend:8000
    restart: always

  # ── Backend ──────────────────────────────────────────────────────
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - postgres
      - mysql
      - redis
    restart: always

  # ── Database ─────────────────────────────────────────────────────
  postgres:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: darsi
      POSTGRES_USER: darsi
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  mysql:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      MYSQL_DATABASE: simrs
      MYSQL_USER: darsi
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
    restart: always

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: always

  # ── LLM ──────────────────────────────────────────────────────────
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: always

  # ── LiveKit ──────────────────────────────────────────────────────
  livekit:
    image: livekit/livekit-server:latest
    ports:
      - "7880:7880"
      - "7881:7881"
      - "7882:7882/udp"
    environment:
      - LIVEKIT_CONFIG_FILE=/etc/livekit.yaml
    volumes:
      - ./livekit.yaml:/etc/livekit.yaml:ro
    restart: always

  # ── AI Services ──────────────────────────────────────────────────
  stt:
    build:
      context: ../darsi-ai/stt
    ports:
      - "8001:8001"
    volumes:
      - whisper_models:/app/models
    restart: always

  tts:
    build:
      context: ../darsi-ai/tts
    ports:
      - "8002:8002"
    volumes:
      - tts_models:/app/models
    restart: always

  ocr:
    build:
      context: ../darsi-ai/ocr
    ports:
      - "8003:8003"
    volumes:
      - ocr_models:/app/models
    restart: always

  face:
    build:
      context: ../darsi-ai/face
    ports:
      - "8004:8004"
    volumes:
      - face_models:/app/models
    restart: always

  rag:
    build:
      context: ../darsi-ai/rag
    ports:
      - "8005:8005"
    volumes:
      - rag_models:/app/models
      - rag_index:/app/index
    restart: always

  dialog:
    build:
      context: ../darsi-ai/dialog
    ports:
      - "8006:8006"
    environment:
      - LIVEKIT_URL=ws://livekit:7880
      - LIVEKIT_API_KEY=${LIVEKIT_API_KEY}
      - LIVEKIT_API_SECRET=${LIVEKIT_API_SECRET}
      - STT_URL=http://stt:8001
      - TTS_URL=http://tts:8002
      - OLLAMA_URL=http://ollama:11434
      - RAG_URL=http://rag:8005
    depends_on:
      - livekit
      - stt
      - tts
      - ollama
      - rag
    restart: always

volumes:
  postgres_data:
  mysql_data:
  redis_data:
  ollama_data:
  whisper_models:
  tts_models:
  ocr_models:
  face_models:
  rag_models:
  rag_index:
```

## Environment Variables

### `darsi-admin/.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### `darsi-kiosk/.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_NODE_ID=NODE-01
```

> `NEXT_PUBLIC_NODE_ID` di-set berbeda di tiap device fisik saat deployment (NODE-01 sampai NODE-06).

### `darsi-backend/.env`

```env
# ── Database ─────────────────────────────────────────────────────
POSTGRES_URL=postgresql+asyncpg://darsi:password@postgres:5432/darsi
MYSQL_URL=mysql+aiomysql://darsi:password@mysql:3306/simrs
POSTGRES_PASSWORD=change_in_prod
MYSQL_PASSWORD=change_in_prod
MYSQL_ROOT_PASSWORD=change_in_prod

# ── Cache ─────────────────────────────────────────────────────────
REDIS_URL=redis://redis:6379/0

# ── AI Services ───────────────────────────────────────────────────
STT_URL=http://stt:8001
TTS_URL=http://tts:8002
OCR_URL=http://ocr:8003
FACE_URL=http://face:8004
RAG_URL=http://rag:8005
DIALOG_URL=http://dialog:8006
OLLAMA_URL=http://ollama:11434

# ── LiveKit ───────────────────────────────────────────────────────
LIVEKIT_URL=ws://livekit:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=devsecret

# ── Auth ──────────────────────────────────────────────────────────
SECRET_KEY=ganti-ini-di-produksi-min-32-karakter
ACCESS_TOKEN_EXPIRE_MINUTES=480

# ── Integrasi Eksternal ───────────────────────────────────────────
ERSIMY_BASE_URL=
ERSIMY_API_KEY=

SIMRS_BASE_URL=
SIMRS_API_KEY=

BPJS_BASE_URL=https://apijkn.bpjs-kesehatan.go.id
BPJS_CONS_ID=
BPJS_SECRET_KEY=
BPJS_USER_KEY=
```

## API Contract (Draft)

Draft ini dibuat dari sisi frontend (Bagus) untuk dikoordinasikan dengan backend (Yardan).

### Auth

**POST `/auth/login`**
```json
// Request
{ "username": "admin", "password": "password" }

// Response 200
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 28800
}
```

### Nodes

**GET `/admin/nodes`**
```json
// Response 200
{
  "total": 6,
  "online": 5,
  "offline": 1,
  "nodes": [
    {
      "id": "NODE-01",
      "name": "Pendaftaran Utama",
      "location": "Area PM / Lantai 1",
      "status": "online",
      "is_active": true,
      "language": "id",
      "mode": "voice-first",
      "avatar_id": "avatar-001",
      "avatar_name": "Siti",
      "avatar_thumbnail_url": "/avatars/siti-thumb.jpg",
      "interaction_count_today": 47,
      "last_seen": "2026-06-30T08:30:00Z"
    }
  ]
}
```

**POST `/admin/nodes`**
```json
// Request
{
  "name": "Node Baru",
  "location": "Lantai 2 Koridor B",
  "language": "id",
  "mode": "voice-first",
  "avatar_id": "avatar-001",
  "is_active": true
}

// Response 201
{ "id": "NODE-07", "name": "Node Baru", ... }
```

**PATCH `/admin/nodes/{id}`**
```json
// Request (semua field opsional)
{
  "name": "Pendaftaran Utama",
  "location": "Area PM / Lantai 1",
  "language": "id",
  "mode": "touch-first",
  "avatar_id": "avatar-002",
  "is_active": false
}

// Response 200 — node object lengkap
```

**PATCH `/admin/nodes/{id}/avatar`**
```json
// Request
{ "avatar_id": "avatar-002" }

// Response 200
{ "node_id": "NODE-01", "avatar_id": "avatar-002", "applied_at": "2026-06-30T..." }
```

### Avatars

**GET `/admin/avatars`**
```json
// Response 200
{
  "avatars": [
    {
      "id": "avatar-001",
      "name": "Siti",
      "role": "Petugas Pendaftaran",
      "thumbnail_url": "/avatars/siti-thumb.jpg",
      "vrm_filename": "siti.vrm",
      "format": "VRM",
      "assigned_node_ids": ["NODE-01", "NODE-04"],
      "created_at": "2026-06-01T00:00:00Z"
    }
  ]
}
```

**POST `/admin/avatars`** — multipart/form-data
```
Fields: name, role, vrm_file (file), thumbnail_file (file)
Response 201: avatar object
```

**DELETE `/admin/avatars/{id}`**
```
Response 204: No Content
Error 409: Conflict jika avatar masih ter-assign ke node aktif
```

### Analytics & Logs

**GET `/admin/analytics`**
```
Query params: from (ISO date), to (ISO date), node_id (opsional)

// Response 200
{
  "total_interactions": 342,
  "triage_accuracy_pct": 87.4,
  "stt_error_rate_pct": 4.2,
  "llm_error_rate_pct": 1.8,
  "interactions_by_node": [
    { "node_id": "NODE-01", "count": 120 }
  ],
  "interactions_by_day": [
    { "date": "2026-06-30", "count": 47 }
  ]
}
```

**GET `/admin/logs`**
```
Query params: page (default 1), limit (default 50), node_id, status

// Response 200
{
  "total": 1240,
  "page": 1,
  "limit": 50,
  "logs": [
    {
      "id": "log-uuid",
      "node_id": "NODE-01",
      "timestamp": "2026-06-30T08:15:00Z",
      "stt_input": "perut saya sakit sejak kemarin",
      "triage_output": "Poli Penyakit Dalam",
      "status": "success",
      "duration_ms": 2340
    }
  ]
}
```

### Triage Rules

**GET `/admin/triage-rules`**
```json
// Response 200
{
  "rules": [
    {
      "id": "rule-001",
      "name": "Nyeri Perut Umum",
      "keywords": ["perut sakit", "mual", "kembung"],
      "recommended_poli": "Poli Penyakit Dalam",
      "urgency": "normal",
      "is_active": true,
      "updated_at": "2026-06-28T10:00:00Z",
      "updated_by": "admin"
    }
  ]
}
```

**POST `/admin/triage-rules/test`**
```json
// Request
{ "input_text": "perut saya sakit dan mual sejak tadi pagi" }

// Response 200
{
  "matched_rule_id": "rule-001",
  "matched_rule_name": "Nyeri Perut Umum",
  "recommended_poli": "Poli Penyakit Dalam",
  "confidence": 0.91,
  "matched_keywords": ["perut sakit", "mual"]
}
```

**GET `/admin/triage-rules/{id}/history`**
```json
// Response 200
{
  "rule_id": "rule-001",
  "history": [
    {
      "changed_at": "2026-06-28T10:00:00Z",
      "changed_by": "admin",
      "field": "keywords",
      "old_value": ["perut sakit", "mual"],
      "new_value": ["perut sakit", "mual", "kembung"]
    }
  ]
}
```

### Pharmacy Queue

**GET `/admin/pharmacy-queue/history`**
```json
// Response 200
{
  "history": [
    {
      "queue_number": "A-012",
      "patient_name": "Budi Santoso",
      "type": "non-racik",
      "called_at": "2026-06-30T09:30:00Z",
      "status": "selesai"
    }
  ]
}
```

### WebSocket: `node-status`

Koneksi: `WS /ws/node-status` (header `Authorization: Bearer {token}`)

```json
// Pesan dari server saat ada perubahan
{
  "event": "node_status_changed",
  "data": {
    "node_id": "NODE-01",
    "status": "online",
    "active_session": true,
    "last_seen": "2026-06-30T08:30:00Z"
  }
}

// Pesan dari server saat ada interaksi baru
{
  "event": "node_interaction",
  "data": {
    "node_id": "NODE-01",
    "interaction_count_today": 48
  }
}
```

### WebSocket: `pharmacy-queue`

Koneksi: `WS /ws/pharmacy-queue` (header `Authorization: Bearer {token}`)

```json
// Pesan saat nomor antrian baru dipanggil
{
  "event": "queue_called",
  "data": {
    "queue_number": "A-013",
    "patient_name": "Sari Dewi",
    "type": "racik",
    "loket": "kiri",
    "called_at": "2026-06-30T09:32:00Z"
  }
}

// Pesan saat status antrian berubah
{
  "event": "queue_status_changed",
  "data": {
    "queue_number": "A-013",
    "status": "selesai"
  }
}
```
