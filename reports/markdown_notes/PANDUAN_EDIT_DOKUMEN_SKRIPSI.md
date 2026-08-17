
# 📝 PANDUAN EDIT DOKUMEN SKRIPSI (BAB 1-4)
## Untuk Menyesuaikan dengan Data Project/Dashboard Saat Ini

---

## **File yang Perlu Diedit**
1. `reports/documents/BAB_1_PENDAHULUAN_REVISED.docx`
2. `reports/documents/Bab_2_Tinjauan_Pustaka_REVISED_FINAL.docx`
3. `reports/documents/BAB_III_Metodologi_Penelitian_REVISED_FINAL.docx`
4. `reports/documents/Bab4_Hasil_dan_Pembahasan_REVISED_FINAL.docx`

---

## **1. BAB 4 - BAGIAN YANG PALING BANYAK PERUBAHAN**

### **Perubahan 1: Tabel 4.9 - Distribusi Pseudo-label Teacher**
**Ganti seluruh isi tabel dengan:**

| Kelas Sentimen | Jumlah Ulasan | Persentase |
|----------------|---------------|------------|
| Negatif        | 19,673        | 39.76%     |
| Netral         | 7,290         | 14.73%     |
| Positif        | 22,522        | 45.51%     |
| **Total**      | **49,485**    | **100.00%**|

---

### **Perubahan 2: Tabel 4.10 - Classification Report SVM**
**Ganti seluruh isi tabel dengan:**

| Kelas Sentimen | Precision | Recall | F1-Score | Support |
|----------------|-----------|--------|----------|---------|
| Negatif        | 74.29%    | 79.63% | 76.87%   | 2,798   |
| Netral         | 33.33%    | 0.15%  | 0.30%    | 654     |
| Positif        | 86.73%    | 92.79% | 89.66%   | 6,445   |
| **Accuracy**   |           |        | 82.94%   | 9,897   |
| **Macro Avg**  | 64.78%    | 57.52% | 55.61%   | 9,897   |

---

### **Perubahan 3: Tabel 4.11 - Classification Report IndoBERT**
**Ganti seluruh isi tabel dengan:**

| Kelas Sentimen | Precision | Recall | F1-Score | Support |
|----------------|-----------|--------|----------|---------|
| Negatif        | 82.00%    | 87.00% | 84.00%   | 3,283   |
| Netral         | 79.00%    | 64.00% | 71.00%   | 1,166   |
| Positif        | 92.00%    | 92.00% | 92.00%   | 5,448   |
| **Accuracy**   |           |        | 87.22%   | 9,897   |
| **Macro Avg**  | 84.44%    | 81.15% | 82.50%   | 9,897   |

---

### **Perubahan 4: Tabel 4.12 - Perbandingan Performa Model**
**Ganti seluruh isi tabel dengan:**

| Metrik Evaluasi         | SVM Baseline | IndoBERT | Peningkatan |
|-------------------------|--------------|----------|-------------|
| Accuracy                | 82.94%       | 87.22%   | +4.28%      |
| Precision (Macro)       | 64.78%       | 84.44%   | +19.66%     |
| Recall (Macro)          | 57.52%       | 81.15%   | +23.63%     |
| F1-Score (Macro)        | 55.61%       | 82.50%   | +26.89%     |

---

### **Perubahan 5: Tabel 4.14 - Distribusi Sentimen Per Bulan**
**Ganti seluruh isi tabel dengan:**

| Bulan          | Jml. Negatif | % Negatif | Jml. Netral | % Netral | Jml. Positif | % Positif |
|----------------|--------------|-----------|-------------|----------|--------------|-----------|
| Februari 2026  | 1,711        | 36.28%    | 491         | 10.41%   | 2,514        | 53.31%    |
| Maret 2026     | 9,912        | 35.55%    | 2,360       | 8.46%    | 15,611       | 55.99%    |
| April 2026     | 5,946        | 35.21%    | 1,187       | 7.03%    | 9,753        | 57.76%    |

---

### **Perubahan 6: Narasi Agreement Rate (Teacher vs Rating)**
Pastikan narasi di Bab 4 tentang agreement rate menggunakan angka **59.95%**, bukan 67.83%! (67.83% adalah agreement rate IndoBERT vs rating yang ditampilkan di dashboard).

---

### **Perubahan 7: Narasi Tren Sentimen Per Bulan**
Sesuaikan narasi tentang tren sentimen per bulan dengan angka di Tabel 4.14 yang baru!

---

### **Perubahan 8: Gambar-Gambar di Bab IV**
Ganti semua gambar di Bab IV dengan gambar baru yang sudah di-generate ulang di folder `reports/figures/`:

| Gambar Lama | Gambar Baru di Folder | Keterangan |
|-------------|----------------------|------------|
| Gambar 4.9 | `4_9_distribusi_pseudo_label.png` | Distribusi pseudo-label (sudah sesuai data baru!) |
| Gambar 4.10 | `4_10_confusion_matrix_svm.png` | Confusion matrix SVM |
| Gambar 4.11 & 4.12 | `4_11_4_12_training_indobert.png` | Grafik training & validation IndoBERT |
| Gambar 4.13 | `4_13_confusion_matrix_indobert.png` | Confusion matrix IndoBERT |
| Gambar 4.14 | `4_14_perbandingan_model.png` | Perbandingan performa SVM vs IndoBERT |
| Gambar 4.15 | `4_15_tren_jumlah_review.png` | Tren jumlah review harian |
| Gambar 4.16 | `4_16_tren_sentimen_bulanan.png` | Tren sentimen per bulan (sudah sesuai data baru!) |

---

## **2. CEK KONSISTENSI DI BAB LAINNYA**
Pastikan semua angka di Bab 1, 2, dan 3 (jika ada) yang merujuk ke hasil eksperimen sudah sesuai dengan `RINGKASAN_ANGKA_FINAL_UNTUK_DOKUMEN.md`.

---

## **3. TIPS EDIT DOKUMEN WORD**
1.  **Gunakan "Find and Replace"** untuk mengubah angka-angka yang sama secara cepat.
2.  **Perhatikan format angka**: Pastikan penggunaan titik (.) sebagai pemisah ribuan dan koma (,) sebagai pemisah desimal sesuai dengan format Indonesia.
3.  **Backup dokumen asli** sebelum mengedit!

---

## **4. SUMBER DATA TERPERCAYA**
Jika ragu, selalu cek kembali:
- `RINGKASAN_ANGKA_FINAL_UNTUK_DOKUMEN.md` (file utama)
- `reports/markdown_notes/rangkuman_hasil_eksperimen_bab4.md`
- `reports/markdown_notes/PENJELASAN_GAMBAR_BAB_4.md` (penjelasan paragraf setiap gambar)
- `data/processed/TABEL_BAB4_SIAP_PAKAI.txt`
- Jalankan dashboard untuk melihat visualisasi data asli!

