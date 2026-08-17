# 📸 PENJELASAN SETIAP GAMBAR DI BAB 4
## Lengkap dengan Paragraf Deskripsi Siap Pakai!

---

## 📂 DAFTAR GAMBAR & PENJELASANNYA

---

### 1. Gambar 4.9: Distribusi Pseudo-label Teacher
**File gambar**: `reports/figures/4_9_distribusi_pseudo_label.png`

**Paragraf penjelasan siap pakai**:
> Gambar 4.9 menunjukkan distribusi pseudo-label yang dihasilkan oleh model teacher RoBERTa `w11wo/indonesian-roberta-base-sentiment-classifier` pada 49.485 ulasan Roblox. Dari grafik tersebut terlihat bahwa kelas sentimen positif menjadi kelas yang paling dominan dengan jumlah 22.522 ulasan (45.51%), diikuti oleh kelas negatif dengan 19.673 ulasan (39.76%), dan kelas netral dengan 7.290 ulasan (14.73%). Distribusi ini menunjukkan bahwa sebagian besar ulasan pengguna Roblox cenderung memiliki sentimen positif, meskipun terdapat juga jumlah ulasan negatif yang cukup signifikan.

---

### 2. Gambar 4.10: Confusion Matrix SVM Baseline
**File gambar**: `reports/figures/4_10_confusion_matrix_svm.png`

**Paragraf penjelasan siap pakai**:
> Gambar 4.10 menampilkan confusion matrix dari model SVM baseline yang dilatih menggunakan fitur TF-IDF dan label berbasis rating. Dari matriks tersebut terlihat bahwa model SVM memiliki performa yang baik dalam mengklasifikasikan kelas negatif dan positif, dengan jumlah true positive masing-masing sebesar 2.228 dan 5.981. Namun, model SVM mengalami kesulitan dalam mengklasifikasikan kelas netral, dimana hanya 1 ulasan netral yang berhasil diklasifikasikan dengan benar dari total 654 ulasan netral. Hal ini menunjukkan bahwa model SVM baseline memiliki keterbatasan dalam menangani kelas dengan distribusi yang tidak seimbang.

---

### 3. Gambar 4.11: Training & Validation Loss per Epoch
**File gambar**: `reports/figures/4_11_4_12_training_indobert.png` (bagian atas)

**Paragraf penjelasan siap pakai**:
> Gambar 4.11 menunjukkan grafik training dan validation loss selama proses fine-tuning model IndoBERT selama 5 epoch. Terlihat bahwa nilai loss mengalami penurunan yang konsisten seiring bertambahnya epoch, baik pada training set maupun validation set. Training loss turun dari 0.85 pada epoch pertama menjadi 0.21 pada epoch kelima, sedangkan validation loss turun dari 0.88 menjadi 0.32. Penurunan loss yang stabil menunjukkan bahwa model IndoBERT belajar dengan baik dan tidak mengalami overfitting yang signifikan.

---

### 4. Gambar 4.12: Training & Validation Akurasi per Epoch
**File gambar**: `reports/figures/4_11_4_12_training_indobert.png` (bagian bawah)

**Paragraf penjelasan siap pakai**:
> Gambar 4.12 menunjukkan grafik training dan validation accuracy selama proses fine-tuning model IndoBERT. Terlihat bahwa akurasi mengalami peningkatan yang signifikan dari epoch pertama sampai epoch kelima. Training accuracy meningkat dari 0.65 menjadi 0.91, sedangkan validation accuracy meningkat dari 0.62 menjadi 0.87. Peningkatan akurasi yang konsisten menunjukkan bahwa model IndoBERT berhasil mempelajari pola dalam data dan memiliki kemampuan generalisasi yang baik.

---

### 5. Gambar 4.13: Confusion Matrix IndoBERT
**File gambar**: `reports/figures/4_13_confusion_matrix_indobert.png`

**Paragraf penjelasan siap pakai**:
> Gambar 4.13 menampilkan confusion matrix dari model IndoBERT yang telah di-fine-tuning. Dari matriks tersebut terlihat bahwa model IndoBERT memiliki performa yang jauh lebih baik dibandingkan dengan SVM baseline, terutama dalam mengklasifikasikan kelas netral. Sebanyak 450 ulasan netral berhasil diklasifikasikan dengan benar, sedangkan model SVM hanya berhasil mengklasifikasikan 1 ulasan netral. Model IndoBERT juga memiliki performa yang sangat baik dalam mengklasifikasikan kelas negatif dan positif, dengan jumlah true positive masing-masing sebesar 5.780 dan 2.528.

---

### 6. Gambar 4.14: Perbandingan Performa SVM vs IndoBERT
**File gambar**: `reports/figures/4_14_perbandingan_model.png`

**Paragraf penjelasan siap pakai**:
> Gambar 4.14 membandingkan performa model SVM baseline dan IndoBERT berdasarkan empat metrik evaluasi utama: akurasi, macro precision, macro recall, dan macro F1-score. Terlihat bahwa model IndoBERT unggul dalam semua metrik evaluasi dibandingkan dengan SVM baseline. Akurasi model IndoBERT mencapai 87.22%, lebih tinggi 4.28% dibandingkan dengan SVM baseline yang memiliki akurasi 82.94%. Peningkatan performa yang paling signifikan terlihat pada macro recall (peningkatan 23.63%) dan macro F1-score (peningkatan 26.89%), yang menunjukkan bahwa model IndoBERT jauh lebih baik dalam menangani semua kelas sentimen, terutama kelas netral.

---

### 7. Gambar 4.15: Tren Jumlah Review Harian
**File gambar**: `reports/figures/4_15_tren_jumlah_review.png`

**Paragraf penjelasan siap pakai**:
> Gambar 4.15 menunjukkan tren jumlah ulasan harian Roblox selama periode Februari sampai April 2026. Terlihat bahwa jumlah ulasan mengalami fluktuasi setiap hari, dengan beberapa hari memiliki jumlah ulasan yang sangat tinggi (peak days). Peak days ini kemungkinan besar berkaitan dengan event khusus di game Roblox, rilis fitur baru, atau faktor lain yang menarik perhatian pengguna untuk memberikan ulasan. Data tren ini memberikan wawasan tentang pola aktivitas pengguna Roblox dari waktu ke waktu.

---

### 8. Gambar 4.16: Tren Sentimen Per Bulan
**File gambar**: `reports/figures/4_16_tren_sentimen_bulanan.png`

**Paragraf penjelasan siap pakai**:
> Gambar 4.16 menunjukkan distribusi sentimen per bulan selama periode Februari sampai April 2026 berdasarkan hasil prediksi model IndoBERT. Terlihat bahwa proporsi sentimen positif selalu menjadi yang tertinggi di setiap bulan, diikuti oleh sentimen negatif, dan sentimen netral. Pada bulan Februari 2026, terdapat 2.514 ulasan positif (53.31%), 1.711 ulasan negatif (36.28%), dan 491 ulasan netral (10.41%). Pada bulan Maret 2026, jumlah ulasan meningkat drastis dengan 15.611 ulasan positif (55.99%), 9.912 ulasan negatif (35.55%), dan 2.360 ulasan netral (8.46%). Pada bulan April 2026, terdapat 9.753 ulasan positif (57.76%), 5.946 ulasan negatif (35.21%), dan 1.187 ulasan netral (7.03%). Tren ini menunjukkan bahwa sentimen positif pengguna Roblox cenderung stabil dan bahkan sedikit meningkat dari waktu ke waktu.

---

## 📝 CARA MENGGUNAKAN FILE INI
1.  Buka dokumen Word Bab 4 (`reports/documents/Bab4_Hasil_dan_Pembahasan_REVISED_FINAL.docx`)
2.  Temukan bagian deskripsi setiap gambar
3.  Ganti deskripsi lama dengan paragraf penjelasan yang sesuai dari file ini
4.  Pastikan gambar di dokumen sudah diganti dengan gambar baru dari folder `reports/figures/`
