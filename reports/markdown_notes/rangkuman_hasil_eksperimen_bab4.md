
# RANGKUMAN HASIL EKSPERIMEN BAB IV - ANALISIS SENTIMEN ULASAN ROBLOX

## 1. Scraping &amp; Dataset
- **Total ulasan yang berhasil di-scrape**: 49,485 ulasan
- **Rentang waktu ulasan**: 25 Februari 2026 sampai 22 April 2026
- **Sumber data**: Google Play Store (aplikasi Roblox)
- **Atribut utama**: `content` (teks ulasan), `score` (rating bintang), `at` (tanggal ulasan)

## 2. Hasil Pre-processing
- **Jumlah data sebelum pre-processing**: 50,000 (target scraping)
- **Jumlah data setelah pre-processing**: 49,485
- **Jumlah data yang hilang/dihapus**: 515 data
- **Tahapan pre-processing yang dilakukan**:
  1. Case folding (mengubah ke huruf kecil)
  2. Cleaning (menghapus URL, angka, karakter tidak relevan)
  3. Tokenisasi
  4. Penanganan negasi (contoh: "tidak bagus" → "tidak_NEG bagus")
  5. Penghapusan stopword
  6. Stemming (menggunakan algoritma Nazief-Adriani)

## 3. Teacher-Student Auto Labeling
### Distribusi label pseudo-labeling (Model Teacher: w11wo/indonesian-roberta-base-sentiment-classifier)
| Label       | Jumlah Data | Persentase |
|-------------|-------------|------------|
| **Positif** | 22,522      | 45.51%     |
| **Netral**  | 7,290       | 14.73%     |
| **Negatif** | 19,673      | 39.76%     |
| **Total**   | 49,485      | 100.00%    |

### Agreement Rate (Rating vs Pseudo-label Teacher)
- **Agreement Rate**: 59.95%
- **Data yang sesuai (rating vs model teacher)**: 29,668
- **Data yang tidak sesuai**: 19,817

## 4. Hasil SVM Baseline
### Metrik Evaluasi Model SVM
| Metrik                | Nilai  |
|-----------------------|--------|
| **Test Accuracy**     | 82.94% |
| **Precision (Macro)** | 64.78% |
| **Recall (Macro)**    | 57.52% |
| **F1-Score (Macro)**  | 55.61% |

### Classification Report per Kelas (SVM)
| Kelas     | Precision | Recall | F1-Score | Support |
|-----------|-----------|--------|----------|---------|
| Negatif   | 74.29%    | 79.63% | 76.87%   | 2,798   |
| Netral    | 33.33%    | 0.15%  | 0.30%    | 654     |
| Positif   | 86.73%    | 92.79% | 89.66%   | 6,445   |
| **Total** | **82.94%** | **82.94%**| **82.94%**  | 9,897   |

### Konfigurasi Model SVM
- **Kernel**: Linear
- **Parameter C**: 1.0
- **Feature Extraction**: TF-IDF (max_features=5000)
- **Random State**: 42
- **Split Data**: 80% Train, 20% Test

## 5. Hasil Fine-Tuning IndoBERT
### Metrik Evaluasi Model IndoBERT
| Metrik                | Nilai  |
|-----------------------|--------|
| **Test Accuracy**     | 87.22% |
| **Precision (Macro)** | 84.44% |
| **Recall (Macro)**    | 81.15% |
| **F1-Score (Macro)**  | 82.50% |

### Classification Report per Kelas (IndoBERT)
| Kelas     | Precision | Recall | F1-Score | Support |
|-----------|-----------|--------|----------|---------|
| Negatif   | 82.00%    | 87.00% | 84.00%   | 3,283   |
| Netral    | 79.00%    | 64.00% | 71.00%   | 1,166   |
| Positif   | 92.00%    | 92.00% | 92.00%   | 5,448   |
| **Total** | **87.00%** | **87.00%**| **87.00%**  | 9,897   |

### Perbandingan Model SVM vs IndoBERT
| Metrik                | SVM Baseline | IndoBERT | Peningkatan |
|-----------------------|--------------|----------|-------------|
| **Accuracy**          | 82.94%       | 87.22%   | +4.28%      |
| **Precision (Macro)** | 64.78%       | 84.44%   | +19.66%     |
| **Recall (Macro)**    | 57.52%       | 81.15%   | +23.63%     |
| **F1-Score (Macro)**  | 55.61%       | 82.50%   | +26.89%     |

### Konfigurasi Fine-Tuning IndoBERT
- **Model pre-trained**: `indobenchmark/indobert-base-p1`
- **Jumlah epoch**: 5 epoch
- **Max sequence length**: 128 token
- **Batch size**: 32
- **Optimizer**: AdamW
- **Learning rate**: 2e-5
- **Loss function**: CrossEntropyLoss
- **Split data**: 80% Train, 20% Test (dengan 10% dari train sebagai validasi)

## 6. Implementasi Dashboard Streamlit
Dashboard interaktif telah dibuat dengan fitur-fitur:
1. **🏠 Overview**: Ringkasan eksekutif analisis sentimen
2. **📊 Analisis Sentimen**: Distribusi sentimen dan analisis detail
3. **📈 Tren Temporal**: Tren sentimen dari waktu ke waktu
4. **🔬 Model &amp; Evaluasi**: Perbandingan model SVM dan IndoBERT
5. **⚙️ Scraping &amp; Preprocessing**: Alur pengumpulan dan pembersihan data

Untuk menjalankan dashboard:
```bash
streamlit run app.py
```

---

**Catatan**: Semua hasil eksperimen ini dapat diulangi kembali dengan menjalankan script yang tersedia di repository!

