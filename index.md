# Indeks Dokumen — DARSI-CS

Repo ini adalah hub dokumentasi untuk proyek DARSI Customer Service.
Semua dokumen penting dapat diakses dari halaman ini.

## Dokumen Perencanaan

| File | Isi |
|---|---|
| [Notes/PRD.md](Notes/PRD.md) | Product Requirements Document v1.2 — problem statement, personas, fitur P0/P1/P2, tech stack, timeline, risiko, open questions |
| [Notes/ARCHITECTURE.md](Notes/ARCHITECTURE.md) | Arsitektur teknis lengkap — diagram Mermaid, peta port, struktur folder per repo, Docker Compose, env variables, API contract draft |
| [Notes/DESIGN-THINKING.md](Notes/DESIGN-THINKING.md) | Proses design thinking proyek — empathize, define, ideate, prototype, test |
| [Notes/tech-stack.md](Notes/tech-stack.md) | Dokumen referensi tech stack awal (catatan: versi final ada di PRD Section 7) |

## Dokumen Operasional Agent

| File | Isi |
|---|---|
| [CLAUDE.md](CLAUDE.md) | Instruksi operasional untuk Claude Code — operating loop, rules, required files |
| [AGENTS.md](AGENTS.md) | Instruksi operasional untuk AI agent umum — startup workflow, working rules, definition of done |
| [claude-progress.md](claude-progress.md) | Log progres per sesi — dibaca pertama kali di setiap sesi baru |
| [feature_list.json](feature_list.json) | Daftar fitur dengan prioritas dan status pengerjaan |
| [session-handoff.md](session-handoff.md) | Handoff ringkas antar sesi — state terkini, next step |
| [init.sh](init.sh) | Script startup — install deps, verifikasi, jalankan server |

## Dokumen Kualitas

| File | Isi |
|---|---|
| [clean-state-checklist.md](clean-state-checklist.md) | Checklist sebelum menutup sesi — pastikan repo bersih |
| [evaluator-rubric.md](evaluator-rubric.md) | Rubrik evaluasi output agent — 6 dimensi, skor 0-2 |
| [quality-document.md](quality-document.md) | Snapshot kesehatan codebase per domain dan layer |

## Ringkasan Proyek

**DARSI-CS** adalah ekosistem AI assistant berbasis node untuk RSI A. Yani Surabaya.
Sistem memandu pasien secara mandiri dari pendaftaran hingga pengambilan obat via interaksi suara dan sentuh.

**Tim IT:**
- Bagus — Dashboard Admin UI, Kiosk Node UI, WebView Android
- Irawan — AI Layer (STT, LLM, TTS, OCR, Face Recognition)
- Yardan — Backend FastAPI, Database, Integrasi eksternal

**Status dokumentasi:** PRD v1.2 ✅ · ARCHITECTURE v1.0 ✅ · Kode belum dimulai
