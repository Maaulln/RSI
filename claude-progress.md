# Progress Log — DARSI-CS

## Current Verified State

- Repository root: `D:\Dev\Projects\RSI`
- Standard startup path: `./init.sh`
- Standard verification path: belum ada (dokumentasi phase, kode belum dimulai)
- Current highest-priority unfinished feature: `dash-001` — Setup repo darsi-admin (Next.js + Tailwind)
- Current blocker: Tidak ada blocker dokumentasi. Untuk coding: perlu koordinasi API contract dengan Yardan sebelum integrasi real.

## Konteks Proyek

Proyek DARSI Customer Service — AI assistant berbasis node untuk RSI A. Yani Surabaya.
Repo ini adalah hub dokumentasi. Kode ada di repo terpisah: darsi-admin, darsi-kiosk, darsi-backend, darsi-ai.

Baca [README.md](README.md) untuk overview lengkap.
Baca [Notes/PRD.md](Notes/PRD.md) untuk requirements dan acceptance criteria.
Baca [Notes/ARCHITECTURE.md](Notes/ARCHITECTURE.md) untuk struktur teknis dan API contract.

## Session Log

### Session 001

- Date: 2026-06-30
- Goal: Menetapkan tech stack, menyusun PRD final, dan membuat arsitektur proyek
- Completed:
  - Tech stack dikonfirmasi: Next.js 14, FastAPI, PostgreSQL + MySQL, Redis, Ollama (Sahabat-AI 8B), Whisper Large-v3-Turbo, VITS/MMS, Chandra OCR, InsightFace ArcFace, BGE-M3
  - PRD diupdate ke v1.2 — ditambah Problem Statement terukur, Goals & KPI, Timeline 7 fase, Risiko & Mitigasi, section Pembagian Jobdesk dipindah ke atas
  - ARCHITECTURE.md dibuat dari nol — diagram Mermaid lengkap, peta 14 service + port, struktur folder 4 repo, Docker Compose lengkap dengan volumes, env variables lengkap, API contract semua endpoint
  - README.md dibuat, index.md diupdate, file-file boilerplate diisi konteks proyek nyata
  - feature_list.json diisi dengan fitur DARSI-CS yang sesungguhnya
- Verification run: tidak ada — sesi ini murni dokumentasi
- Evidence captured: file PRD.md, ARCHITECTURE.md, README.md, index.md, feature_list.json, claude-progress.md, session-handoff.md
- Commits: selesai di-commit
- Files or artifacts updated: Notes/PRD.md, Notes/ARCHITECTURE.md, README.md, index.md, claude-progress.md, feature_list.json, session-handoff.md, Notes/project-structure.md (dihapus)
- Known risk or unresolved issue:
  - API contract masih draft — belum dikonfirmasi Yardan
  - Akses API BPJS/JKN, SIM RS, My eRSIy belum terkonfirmasi (Open Questions #1, #2, #9 di PRD)
  - Spesifikasi hardware tablet belum fix (Open Question #3)
- Next best step: Mulai scaffold repo `darsi-admin` — setup Next.js 14 + Tailwind + routing skeleton + mock data

### Session 002

- Date:
- Goal:
- Completed:
- Verification run:
- Evidence captured:
- Commits:
- Files or artifacts updated:
- Known risk or unresolved issue:
- Next best step:
