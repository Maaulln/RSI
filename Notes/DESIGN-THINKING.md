# Design Thinking

## 1. EMPATHIZE

### Siapa penggunanya?
- **Pasien umum** — Berbagai usia, latar belakang, dan tingkat literasi.
- **Lansia** — Tidak familiar dengan teknologi, mungkin memiliki gangguan visual atau pendengaran.
- **Pendamping pasien** — Keluarga yang panik dan terburu-buru.
- **Staf pendaftaran** — Overload, harus menangani banyak pasien sekaligus.
- **Dokter / perawat poli** — Membutuhkan informasi pasien sebelum pasien datang.

### Pain points yang ditemukan:
- Pasien tidak tahu harus ke poli mana.
- Antrian pendaftaran panjang karena semua proses masih manual.
- Pasien salah poli → kembali ke pendaftaran → antrian ulang.
- Lansia kesulitan membaca papan petunjuk.
- Staf kelelahan karena triage dilakukan secara manual satu per satu.
- Pasien tidak tahu kapan gilirannya dipanggil → duduk terus di ruang tunggu.
- Setelah dari dokter, pasien tidak tahu harus ke apotek atau laboratorium mana.

---

## 2. DEFINE — Rumuskan Masalah

### Problem Statement
> Pasien yang datang ke rumah sakit tidak memiliki informasi yang cukup untuk menavigasi proses pelayanan secara mandiri — mulai dari menentukan poli yang tepat hingga menyelesaikan seluruh rangkaian kunjungan — sehingga bergantung penuh pada staf dan menciptakan bottleneck di pendaftaran.

### How Might We (HMW):
- **HMW** membuat pasien tahu poli yang tepat tanpa harus bertanya kepada staf?
- **HMW** membantu pasien yang tidak bisa membaca atau tidak melek teknologi?
- **HMW** mengurangi beban staf pendaftaran tanpa mengorbankan kualitas layanan?
- **HMW** memastikan pasien tahu langkah berikutnya setelah tiap tahap selesai?

---

## 3. IDEATE — Eksplorasi Solusi

### Ide untuk Input Gejala:
- Form digital dengan ikon bergambar (tanpa teks).
- Voice input — pasien cukup berbicara.
- WhatsApp bot sebelum berangkat ke RS.
- Staf input dengan auto-suggest sistem.

### Ide untuk Diagnosa & Rekomendasi Poli:
- LLM mengekstrak gejala dari input bebas → rule engine menentukan poli.
- Kombinasi symptom checker berbasis keputusan + AI.
- Override manual oleh staf jika sistem tidak yakin.

### Ide untuk Navigasi:
- Tiket fisik dengan peta mini + warna poli.
- Garis warna di lantai.
- Voice announcement di speaker koridor.
- Indoor navigation via QR di tiket.

### Ide untuk Post-Poli:
- Notifikasi WA saat giliran hampir tiba.
- Tiket lanjutan otomatis ke apotek/lab.
- Ringkasan kunjungan dikirim via WA setelah selesai.

---

## 4. PROTOTYPE — Bentuk Solusi

### MVP (Minimum Viable Product):

```text
       [ Kiosk / Tablet Staf ]
                  ↓
Input gejala (voice / touch / assisted)
                  ↓
       Symptom Extractor (LLM)
                  ↓
   Triage Engine (rule-based + LLM)
                  ↓
               Output:
        - Rekomendasi poli
        - Nomor antrian
        - Cetak tiket (nama poli + lantai + warna jalur)
                  ↓
   Notifikasi WA saat giliran dekat
                  ↓
 Setelah dokter → tiket lanjutan ke apotek/lab
```

### Komponen yang dibangun:
- **Backend**: FastAPI + LLM integration.
- **Triage rules**: Dikurasi bersama dokter RS.
- **Kiosk UI**: Touchscreen besar, font besar, ada tombol voice.
- **Tiket**: Cetak thermal printer, ada peta mini + warna.
- **Notifikasi**: WhatsApp Business API / n8n.

---

## 5. TEST — Validasi

### Skenario uji:
- **Lansia 65 tahun tanpa smartphone** → Apakah bisa menggunakan kiosk secara mandiri?
- **Pasien dengan keluhan ambigu** → Apakah triage engine mengarahkan ke poli yang tepat?
- **Pasien salah poli** → Seberapa cepat sistem bisa mengoreksi?
- **Peak hour (pagi hari)** → Apakah sistem tetap responsif dengan 50+ pasien bersamaan?

### Metrik keberhasilan:
- Waktu pendaftaran per pasien turun dari X menit → target < 2 menit.
- Tingkat salah poli < 5%.
- Kepuasan pasien (survey singkat di akhir kunjungan).
- Beban staf pendaftaran berkurang minimal 40%.

### Iterasi:
- Triage rules divalidasi dokter tiap bulan.
- UI kiosk diuji dengan pasien lansia nyata sebelum launch.
- Feedback staf dikumpulkan 2 minggu pertama operasional.

---

## Ringkasan

| Tahap | Output Kunci |
| :--- | :--- |
| **Empathize** | 5 user persona, 7 pain points |
| **Define** | 1 problem statement, 4 HMW questions |
| **Ideate** | 12+ solusi potensial lintas touchpoint |
| **Prototype** | MVP flow + tech stack |
| **Test** | 4 skenario uji + 3 metrik sukses |
