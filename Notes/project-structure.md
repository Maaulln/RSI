# Struktur Environment Proyek DARSI-CS

**Terakhir diperbarui:** 30 Juni 2026
**Tim:** IT — KP PENS PSDKU Lamongan 2024

---

## Gambaran Arsitektur Keseluruhan

```
┌─────────────────────────────────────────────────────────────────┐
│                        JARINGAN RS (Private Network)            │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐                    │
│  │  Admin Browser  │    │  Android Tablet  │  (x6 node)        │
│  │  (Desktop/Lap.) │    │  WebView         │                    │
│  └────────┬────────┘    └────────┬─────────┘                   │
│           │                     │                               │
│           │ HTTPS               │ HTTPS / WSS                  │
│           ▼                     ▼                               │
│  ┌─────────────────────────────────────────────────────┐       │
│  │                    Nginx (Reverse Proxy)             │       │
│  │              SSL termination + rate limiting         │       │
│  └───┬──────────────┬────────────────┬─────────────────┘       │
│      │              │                │                          │
│      ▼              ▼                ▼                          │
│  ┌───────┐    ┌──────────┐    ┌──────────────┐                 │
│  │Next.js│    │ Next.js  │    │   FastAPI    │                 │
│  │Admin  │    │ Kiosk UI │    │   Backend    │                 │
│  │:3001  │    │ :3000    │    │   :8000      │                 │
│  └───────┘    └──────────┘    └──────┬───────┘                 │
│                                      │                          │
│              ┌───────────────────────┤                          │
│              │           │           │           │              │
│              ▼           ▼           ▼           ▼              │
│         ┌────────┐ ┌─────────┐ ┌────────┐ ┌────────┐          │
│         │Postgres│ │  MySQL  │ │ Redis  │ │Ollama  │          │
│         │  :5432 │ │  :3306  │ │ :6379  │ │ :11434 │          │
│         └────────┘ └─────────┘ └────────┘ └────────┘          │
│                                                                  │
│         ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│         │ Whisper  │ │   TTS    │ │   OCR    │ │  Face    │   │
│         │  :8001   │ │  :8002   │ │  :8003   │ │  :8004   │   │
│         └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
└─────────────────────────────────────────────────────────────────┘
          │                                          │
          ▼                                          ▼
   ┌─────────────┐                          ┌──────────────┐
   │ My eRSIy API│                          │  API BPJS/JKN│
   │   SIM RS    │                          │              │
   └─────────────┘                          └──────────────┘
```

---

## Struktur Repository

Proyek menggunakan **pendekatan multi-repo** — setiap komponen utama memiliki
repo sendiri sesuai jobdesk masing-masing anggota tim.

```
GitHub Org / Akun Tim
│
├── darsi-admin/          ← Bagus — Dashboard Admin (Next.js)
├── darsi-kiosk/          ← Bagus — Kiosk UI (Next.js)
├── darsi-backend/        ← Yardan — FastAPI + DB + Integrasi
├── darsi-ai/             ← Irawan — STT + LLM + TTS + OCR + Face Recognition
└── RSI/                  ← Tim (repo ini) — Dokumentasi & PRD
```

---

## Detail Tiap Komponen

### 1. `darsi-admin` — Dashboard Admin (Bagus)

**Tech:** Next.js 14, Tailwind CSS, TanStack Query, Zustand, native WebSocket

```
darsi-admin/
├── public/
├── src/
│   ├── app/                        # Next.js App Router
│   │   ├── layout.tsx              # Root layout (sidebar, topbar)
│   │   ├── page.tsx                # Redirect ke /overview
│   │   ├── (auth)/
│   │   │   └── login/page.tsx
│   │   └── (dashboard)/
│   │       ├── overview/page.tsx
│   │       ├── nodes/
│   │       │   ├── page.tsx        # Tabel Manajemen Node
│   │       │   └── [id]/page.tsx   # Detail node
│   │       ├── avatars/page.tsx    # Galeri & upload avatar
│   │       ├── monitoring/page.tsx # Analytics & log
│   │       ├── triage/page.tsx     # Manajemen Triage Rules
│   │       └── pharmacy/page.tsx   # Antrian Obat real-time
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx
│   │   │   └── Topbar.tsx
│   │   └── ui/                     # Komponen reusable (Button, Badge, Modal, dll)
│   ├── features/                   # Logic per fitur (co-locate dengan page)
│   │   ├── nodes/
│   │   │   ├── NodeTable.tsx
│   │   │   ├── NodeEditModal.tsx
│   │   │   ├── nodes.api.ts        # Fetch ke FastAPI
│   │   │   └── nodes.types.ts
│   │   ├── avatars/
│   │   ├── monitoring/
│   │   ├── triage/
│   │   └── pharmacy/
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useNodeStatus.ts        # WebSocket node-status channel
│   │   └── usePharmacyQueue.ts     # WebSocket pharmacy-queue channel
│   ├── lib/
│   │   ├── api.ts                  # Axios/fetch client + base URL
│   │   ├── ws.ts                   # WebSocket manager (reconnect logic)
│   │   └── queryClient.ts
│   ├── store/
│   │   └── authStore.ts            # Zustand — auth token & session
│   └── types/
│       └── index.ts                # Tipe global bersama
├── .env.local                      # NEXT_PUBLIC_API_URL, NEXT_PUBLIC_WS_URL
├── next.config.ts
├── tailwind.config.ts
└── package.json
```

**Endpoint FastAPI yang dibutuhkan:**
| Halaman | Endpoint |
|---|---|
| Overview | `GET /admin/overview`, `WS /ws/node-status` |
| Nodes | `GET /admin/nodes`, `POST /admin/nodes`, `PATCH /admin/nodes/{id}` |
| Avatars | `GET /admin/avatars`, `POST /admin/avatars`, `DELETE /admin/avatars/{id}` |
| Monitoring | `GET /admin/analytics`, `GET /admin/logs` |
| Triage | `GET/POST/PATCH /admin/triage-rules`, `POST /admin/triage-rules/test` |
| Pharmacy | `WS /ws/pharmacy-queue`, `GET /admin/pharmacy-queue/history` |
| Auth | `POST /auth/login`, `POST /auth/logout` |

---

### 2. `darsi-kiosk` — Kiosk UI (Bagus)

**Tech:** Next.js 14 (static export), Tailwind CSS, native WebSocket

```
darsi-kiosk/
├── public/
│   └── assets/                     # Ikon gejala, ilustrasi UI
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Layout kiosk (fullscreen, no nav)
│   │   ├── page.tsx                # Screen idle / standby
│   │   └── session/
│   │       ├── identify/page.tsx   # Fingerprint / Face / OCR KTP
│   │       ├── symptoms/page.tsx   # Input gejala (voice + touch)
│   │       ├── result/page.tsx     # Rekomendasi poli + cetak tiket
│   │       └── navigation/page.tsx # Panduan arah
│   ├── components/
│   │   ├── VoiceInput.tsx          # Mic button + waveform display
│   │   ├── TouchFallback.tsx       # Keyboard on-screen / ikon gejala
│   │   └── CallStaff.tsx           # Tombol Panggil Petugas (selalu visible)
│   ├── hooks/
│   │   ├── useVoice.ts             # Mic recording → kirim ke STT service
│   │   └── useNodeSession.ts       # WebSocket session dengan backend
│   └── lib/
│       ├── api.ts
│       └── ws.ts
├── next.config.ts                  # output: 'export' (static build)
└── package.json
```

**Catatan penting untuk WebView Android:**
- `next.config.ts` harus set `output: 'export'` agar build jadi static HTML/JS
- Tidak boleh menggunakan fitur yang butuh Next.js server (server actions, API routes)
- Semua komunikasi backend lewat FastAPI langsung

---

### 3. `darsi-backend` — FastAPI Backend (Yardan)

```
darsi-backend/
├── app/
│   ├── main.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── admin/
│   │   │   ├── nodes.py
│   │   │   ├── avatars.py
│   │   │   ├── analytics.py
│   │   │   └── triage.py
│   │   └── kiosk/
│   │       ├── session.py
│   │       └── queue.py
│   ├── websocket/
│   │   ├── node_status.py          # Channel: node-status
│   │   └── pharmacy_queue.py       # Channel: pharmacy-queue
│   ├── models/                     # SQLAlchemy ORM models
│   │   ├── postgres/               # PostgreSQL models
│   │   └── mysql/                  # MySQL models (integrasi SIM RS)
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── node_service.py
│   │   └── integration/            # My eRSIy, SIM RS, BPJS
│   └── schemas/                    # Pydantic schemas (request/response)
├── alembic/                        # Migrasi database PostgreSQL
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

### 4. `darsi-ai` — AI Layer (Irawan)

```
darsi-ai/
├── stt/                            # Whisper Large-v3-Turbo via faster-whisper
│   ├── main.py                     # FastAPI wrapper, endpoint /transcribe
│   └── Dockerfile
├── tts/                            # VITS/MMS Indonesia + Chatterbox-ID
│   ├── main.py                     # FastAPI wrapper, endpoint /synthesize
│   └── Dockerfile
├── ocr/                            # Chandra (HF mode dev / vLLM prod)
│   ├── main.py                     # Endpoint /ocr/ktp, /ocr/rujukan
│   └── Dockerfile
├── face/                           # InsightFace ArcFace (CPU)
│   ├── main.py                     # Endpoint /face/verify
│   └── Dockerfile
├── rag/                            # BGE-M3 embedding + vector store
│   ├── main.py
│   └── Dockerfile
├── dialog/                         # Dialog Flow Manager + LiveKit integration
│   ├── main.py
│   └── flows/
│       ├── registration.yaml       # NODE-01
│       ├── navigation.yaml         # NODE-03, NODE-05
│       ├── assessment.yaml         # NODE-04
│       └── pharmacy.yaml           # NODE-06
└── docker-compose.ai.yml
```

---

## Infrastruktur — Docker Compose (Produksi)

File `docker-compose.yml` di `darsi-backend` mengatur semua service:

```yaml
# Gambaran service (bukan file lengkap)
services:
  nginx:          # Reverse proxy + SSL termination
  admin:          # Next.js Admin Dashboard       (port 3001)
  kiosk:          # Next.js Kiosk UI              (port 3000)
  backend:        # FastAPI                       (port 8000)
  postgres:       # PostgreSQL — data utama       (port 5432)
  mysql:          # MySQL — integrasi SIM RS      (port 3306)
  redis:          # Redis — cache + session       (port 6379)
  ollama:         # Ollama LLM server             (port 11434)
  whisper:        # Whisper Large-v3-Turbo STT    (port 8001)
  tts:            # VITS/MMS TTS                  (port 8002)
  ocr:            # Chandra OCR                   (port 8003)
  face:           # InsightFace ArcFace           (port 8004)
  rag:            # BGE-M3 embedding service      (port 8005)
```

---

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
NEXT_PUBLIC_NODE_ID=NODE-01         # Di-set per device fisik
```

### `darsi-backend/.env`
```env
POSTGRES_URL=postgresql://user:pass@postgres:5432/darsi
MYSQL_URL=mysql://user:pass@mysql:3306/simrs
REDIS_URL=redis://redis:6379
OLLAMA_URL=http://ollama:11434
STT_URL=http://whisper:8001
TTS_URL=http://tts:8002
OCR_URL=http://ocr:8003
FACE_URL=http://face:8004
RAG_URL=http://rag:8005
SECRET_KEY=...
```

---

## API Contract (Draft) — Untuk Koordinasi dengan Yardan

### Format WebSocket: `node-status`

Pesan dikirim server ke semua subscriber saat ada perubahan status node:

```json
{
  "event": "node_status_changed",
  "data": {
    "node_id": "NODE-01",
    "status": "online",          // "online" | "offline" | "error"
    "active_session": true,
    "last_seen": "2026-06-30T08:30:00Z"
  }
}
```

### `GET /admin/nodes` — Response

```json
{
  "nodes": [
    {
      "id": "NODE-01",
      "name": "Pendaftaran Utama",
      "location": "Area PM / Lantai 1",
      "status": "online",
      "avatar_id": "avatar-001",
      "avatar_name": "Siti",
      "language": "id",            // "id" | "jv" | "mad"
      "mode": "voice-first",       // "voice-first" | "touch-first"
      "is_active": true,
      "last_seen": "2026-06-30T08:30:00Z",
      "interaction_count_today": 47
    }
  ],
  "total": 6,
  "online": 5,
  "offline": 1
}
```

### `PATCH /admin/nodes/{id}` — Request Body

```json
{
  "name": "Pendaftaran Utama",
  "location": "Area PM / Lantai 1",
  "language": "id",
  "mode": "voice-first",
  "avatar_id": "avatar-002",
  "is_active": true
}
```

### `GET /admin/avatars` — Response

```json
{
  "avatars": [
    {
      "id": "avatar-001",
      "name": "Siti",
      "role": "Petugas Pendaftaran",
      "thumbnail_url": "/avatars/siti-thumb.jpg",
      "vrm_url": "/avatars/siti.vrm",
      "format": "VRM",
      "assigned_nodes": ["NODE-01", "NODE-04"],
      "created_at": "2026-06-01T00:00:00Z"
    }
  ]
}
```

---

## Urutan Pengerjaan yang Disarankan

### Fase 1 — Fondasi (Minggu 1-2)
- [ ] Setup repo `darsi-admin` (Next.js + Tailwind)
- [ ] Halaman Login + auth store (Zustand)
- [ ] Layout sidebar + routing semua halaman (skeleton dulu)
- [ ] Buat mock data / MSW untuk development tanpa backend

### Fase 2 — Fitur Utama Dashboard (Minggu 3-5)
- [ ] **Halaman Manajemen Node** (tabel + WebSocket status + modal edit)
- [ ] **Halaman Manajemen Avatar** (grid galeri + upload form)
- [ ] **Halaman Overview** (statistik cards + chart interaksi)

### Fase 3 — Fitur Lanjutan (Minggu 6-8)
- [ ] **Monitoring & Analytics** (filter + grafik + log tabel)
- [ ] **Triage Rules** (tabel + form + test rule)
- [ ] **Antrian Obat** (real-time WebSocket display)

### Fase 4 — Kiosk UI (Paralel atau setelah Fase 2)
- [ ] Setup repo `darsi-kiosk`
- [ ] Screen idle + voice input component
- [ ] Alur identifikasi (OCR KTP)
- [ ] Alur triage gejala + tampilkan hasil
- [ ] WebView Android wrapper + test di device

### Fase 5 — Integrasi & Polish
- [ ] Integrasi dengan backend Yardan (ganti mock dengan real API)
- [ ] Test WebSocket end-to-end
- [ ] Responsiveness + aksesibilitas (font size, kontras)
- [ ] Demo & dokumentasi KP
