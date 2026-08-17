# 📝 PROMPT UNTUK REVISI BAB 4 (HASIL DAN PEMBAHASAN)
## Gunakan prompt ini jika ingin meminta bantuan AI (misal: Claude, GPT) untuk merevisi dokumen Word

---

## 📂 **FILE REFERENSI YANG HARUS DIBACA TERLEBIH DAHULU (DALAM URUTAN PRIORITAS)**
1. `RINGKASAN_ANGKA_FINAL_UNTUK_DOKUMEN.md` – File utama, semua angka di sini adalah ACUAN
2. `reports/markdown_notes/PANDUAN_EDIT_DOKUMEN_SKRIPSI.md` – Panduan edit detail bagian demi bagian
3. `reports/markdown_notes/rangkuman_hasil_eksperimen_bab4.md` – Hasil eksperimen terperinci
4. `reports/markdown_notes/PENJELASAN_GAMBAR_BAB_4.md` – Penjelasan paragraf setiap gambar (siap pakai!)
5. `data/processed/TABEL_BAB4_SIAP_PAKAI.txt` – Tabel-tabel dalam format teks siap salin-tempel

---

## 🎯 **TUJUAN UTAMA**
Sesuaikan **seluruh isi Bab 4 (Hasil dan Pembahasan)** agar 100% sesuai dengan data project dan dashboard saat ini (tidak boleh ada angka yang salah!).

---

## 📋 **LANGKAH-LANGKAH REVISI (IKUTI SESUAI URUTAN!)**

### 1. **BACA SEMUA FILE REFERENSI TERLEBIH DAHULU**
Pastikan kamu memahami semua angka dan perubahan yang diperlukan sebelum mulai mengedit dokumen Word.

### 2. **GANTI SEMUA TABEL DI BAB 4**
Ganti tabel-tabel berikut dengan versi terbaru dari file referensi:
- **Tabel 4.9**: Distribusi pseudo-label teacher (gunakan data dari `RINGKASAN_ANGKA_FINAL_UNTUK_DOKUMEN.md`)
- **Tabel 4.10**: Classification Report SVM
- **Tabel 4.11**: Classification Report IndoBERT
- **Tabel 4.12**: Perbandingan performa model
- **Tabel 4.14**: Distribusi sentimen per bulan

### 3. **SESUAIKAN SELURUH NARASI TEKS**
Ubah semua kalimat di Bab 4 yang merujuk ke angka-angka hasil eksperimen agar sesuai dengan data terbaru! Contoh:
- Agreement rate teacher vs rating: **59.95%** (bukan 67.83%!)
- Distribusi pseudo-label teacher: Negatif 19,673, Netral 7,290, Positif 22,522
- Tren sentimen per bulan: Gunakan angka di Tabel 4.14 baru

### 4. **GANTI SEMUA GAMBAR DI BAB 4**
Ganti setiap gambar di Bab 4 dengan gambar baru dari folder `reports/figures/`:
- Gambar 4.9 → `4_9_distribusi_pseudo_label.png`
- Gambar 4.10 → `4_10_confusion_matrix_svm.png`
- Gambar 4.11 & 4.12 → `4_11_4_12_training_indobert.png`
- Gambar 4.13 → `4_13_confusion_matrix_indobert.png`
- Gambar 4.14 → `4_14_perbandingan_model.png`
- Gambar 4.15 → `4_15_tren_jumlah_review.png`
- Gambar 4.16 → `4_16_tren_sentimen_bulanan.png`

### 5. **VERIFIKASI KONSISTENSI**
Setelah selesai mengedit, lakukan pengecekan ulang:
- Semua angka di tabel dan narasi **sama persis** dengan `RINGKASAN_ANGKA_FINAL_UNTUK_DOKUMEN.md`
- Tidak ada angka yang salah atau bertentangan
- Format penulisan angka (pemisah ribuan & desimal) sesuai dengan format Indonesia

---

## 🚨 **PERINGATAN PENTING!**
- **JANGAN PERNAH MENGKARANG ANGKA!** Semua angka harus diambil langsung dari file referensi.
- **Backup dokumen asli** sebelum mengedit!
- Jika ragu, selalu cek kembali file referensi atau jalankan dashboard untuk melihat data asli.
