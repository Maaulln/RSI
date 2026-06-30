# DARSI Customer Service (DARSI-CS)

**Sistem AI Assistant berbasis node untuk RSI A. Yani Surabaya**
Tim IT — KP PENS PSDKU Lamongan 2024

<img src="https://skillicons.dev/icons?i=nextjs,tailwind,fastapi,py,postgres,mysql,redis,docker,nginx,githubactions" />

## Tentang Proyek

DARSI-CS adalah ekosistem AI assistant yang tersebar di titik-titik strategis rumah sakit dalam bentuk node fisik (tablet Android). Setiap node menampilkan avatar AI yang memandu pasien secara mandiri — mulai dari pendaftaran, triage gejala, navigasi ke poli, hingga pengambilan obat — menggunakan interaksi suara dan sentuh dalam Bahasa Indonesia, Jawa, dan Madura.

Proyek ini merupakan kelanjutan dari sistem DARSI yang sudah berjalan di [sapadarsi.hcm-lab.id](https://sapadarsi.hcm-lab.id), diadaptasi khusus untuk kebutuhan RSI A. Yani Surabaya.

## Dokumen Utama

| Dokumen | Deskripsi |
|---|---|
| [Notes/PRD.md](Notes/PRD.md) | Product Requirements Document — fitur, personas, acceptance criteria, timeline, risiko |
| [Notes/ARCHITECTURE.md](Notes/ARCHITECTURE.md) | Arsitektur sistem lengkap — diagram, struktur repo, folder, Docker, API contract |
| [Notes/DESIGN-THINKING.md](Notes/DESIGN-THINKING.md) | Proses design thinking — empathize, define, ideate, prototype, test |
| [Notes/tech-stack.md](Notes/tech-stack.md) | Referensi tech stack awal (sudah diupdate di PRD Section 7) |
| [feature_list.json](feature_list.json) | Daftar fitur dengan status pengerjaan per anggota tim |
| [claude-progress.md](claude-progress.md) | Log progres sesi per sesi — dibaca agent setiap sesi baru |

## Struktur Repository Proyek

Repo ini (`RSI/`) adalah **hub dokumentasi**. Kode ada di repo terpisah per anggota tim:

```
GitHub Tim
├── RSI/              ← Repo ini — Dokumentasi, PRD, Architecture
├── darsi-admin/      ← Bagus   — Dashboard Admin (Next.js 14)
├── darsi-kiosk/      ← Bagus   — Kiosk UI (Next.js 14, static export)
├── darsi-backend/    ← Yardan  — FastAPI + PostgreSQL + MySQL + Redis
└── darsi-ai/         ← Irawan  — STT · TTS · OCR · Face · RAG · Dialog
```

## Tech Stack

| Layer | Teknologi |
|---|---|
| Frontend | Next.js 14 (App Router) + Tailwind CSS |
| Backend | FastAPI (Python) + Gunicorn + Uvicorn |
| Voice Pipeline | LiveKit + Whisper Large-v3-Turbo + VITS/MMS Indonesia |
| LLM | Ollama — Sahabat-AI 8B / Qwen3-8B (Q4\_K\_M GGUF) |
| AI/ML | BGE-M3 (RAG) · Chandra (OCR) · InsightFace ArcFace (Face) |
| Database | PostgreSQL (utama) + MySQL (integrasi SIM RS) |
| Cache | Redis |
| Infrastruktur | Docker + Docker Compose · Nginx · GitHub Actions |

Detail lengkap ada di [Notes/ARCHITECTURE.md](Notes/ARCHITECTURE.md).

## Tim

| Nama | Jobdesk | Repo |
|---|---|---|
| Bagus | Dashboard Admin UI · Kiosk Node UI · WebView Android · Admin API support | darsi-admin, darsi-kiosk |
| Irawan | AI Layer — STT · LLM · TTS · OCR · Face Recognition · Dialog Flow | darsi-ai |
| Yardan | Backend FastAPI · Database · Integrasi eksternal (BPJS, SIM RS, My eRSIy) · IoT | darsi-backend |

## Node yang Dibangun

| ID | Lokasi | Peran |
|---|---|---|
| NODE-01 | Area PM / Pendaftaran | Petugas CS — triage & registrasi |
| NODE-02 | Loket BPJS | Asisten operator loket |
| NODE-03 | Lorong PM → Atrium | Penunjuk arah |
| NODE-04 | Depan Poli | Perawat asesmen awal |
| NODE-05 | Lorong Atrium → Apotek | Penunjuk arah |
| NODE-06 | Area Apotek | Petugas farmasi + pemanggil antrian |

## Untuk AI Agent

Jika kamu adalah AI agent yang membaca repo ini:

1. Baca [claude-progress.md](claude-progress.md) untuk mengetahui status terkini
2. Baca [feature_list.json](feature_list.json) untuk memilih fitur yang dikerjakan
3. Baca [Notes/PRD.md](Notes/PRD.md) untuk memahami requirements dan acceptance criteria
4. Baca [Notes/ARCHITECTURE.md](Notes/ARCHITECTURE.md) untuk memahami struktur teknis
5. Ikuti instruksi operasional di [CLAUDE.md](CLAUDE.md) atau [AGENTS.md](AGENTS.md)
6. Jalankan `./init.sh` sebelum memulai pekerjaan apapun
