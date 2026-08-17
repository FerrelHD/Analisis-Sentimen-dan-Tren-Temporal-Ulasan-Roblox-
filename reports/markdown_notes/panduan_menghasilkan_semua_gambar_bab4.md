
# 📚 Panduan Menghasilkan SEMUA Gambar untuk Bab IV

---

## 🚀 Langkah 1: Jalankan Script untuk Hasilkan Grafik Otomatis

1.  Buka terminal, lalu jalankan script Python berikut untuk menghasilkan SEMUA grafik otomatis!

    ```bash
    cd "/Users/Ferrel/Finesser/Skripsi/Analisis Sentimen Review Roblox
    source .venv/bin/activate
    python3 generate_all_images_bab4.py
    ```

    Semua gambar grafik dan tabel praproses akan **otomatis tersimpan di folder `gambar_bab4/`!

---

## 📸 Langkah 2: Panduan Screenshot untuk Gambar yang Butuh Screenshot

Berikut panduan untuk gambar yang perlu Anda screenshot secara manual!

### Bagian 4.1 Hasil Pengumpulan Data
| Gambar | Cara Mendapatkannya |
|--------|-----------------------|
| **Gambar 4.1 Halaman Aplikasi Roblox di Google Play Store | Buka [https://play.google.com/store/apps/details?id=com.roblox.client → Screenshot seluruh halaman aplikasi (pastikan rating 4.7 dan beberapa review teratas terlihat) |
| **Gambar 4.2 Hasil Scraping Dataset Format CSV | Buka `data/raw/roblox_raw.csv di Excel/Google Sheets → Screenshot 10-15 baris pertama (kolom: `content`, `score`, `at`) |

### Bagian 4.2 Hasil Praproses Teks
| Gambar | Cara Mendapatkannya |
|--------|-----------------------|
| **Gambar 4.3-4.8 (Semua Tahap Praproses) | Pakai **tabel yang dihasilkan otomatis (`4_3_sampai_4_8_praproses_tabel.png` di folder `gambar_bab4` |

### Bagian 4.8 Implementasi Dashboard Streamlit
| Gambar | Cara Mendapatkannya |
|--------|-----------------------|
| **Gambar 4.17 Halaman Overview | Jalankan `streamlit run app.py → Buka halaman pertama → Screenshot |
| **Gambar 4.18 Halaman Analisis Sentimen | Klik halaman "Analisis Sentimen" → Screenshot |
| **Gambar 4.19 Halaman Tren Temporal | Klik halaman "Tren Temporal" → Screenshot |
| **Gambar 4.20 Halaman Model & Evaluasi | Klik halaman "Model & Evaluasi" → Screenshot |
| **Gambar 4.21 Halaman Scraping & Praproses | Klik halaman "Scraping & Praproses" → Screenshot |

---

## 📂 Struktur File Hasil Script di `gambar_bab4/`
Setelah script dijalankan, folder `gambar_bab4/` akan berisi file-file berikut:

1.  `4_3_sampai_4_8_praproses_tabel.png - Tabel semua tahap praproses (semua gambar 4.3-4.8 digabung jadi 1!)
2.  `4_9_distribusi_pseudo_label.png - Gambar 4.9
3.  `4_10_confusion_matrix_svm.png - Gambar 4.10
4.  `4_11_4_12_training_indobert.png - Gambar 4.11 dan 4.12 digabung
5.  `4_13_confusion_matrix_indobert.png - Gambar 4.13
6.  `4_14_perbandingan_model.png - Gambar 4.14
7.  `4_15_tren_jumlah_review.png - Gambar 4.15
8.  `4_16_tren_sentimen_bulanan.png - Gambar 4.16

---

## ✅ Tips Penting
- Semua gambar dari script **resolusi 300 DPI (sempurna untuk skripsi!
- Gunakan warna **warna hijau (Positif), kuning (Netral), merah (Negatif) konsisten di semua gambar!
