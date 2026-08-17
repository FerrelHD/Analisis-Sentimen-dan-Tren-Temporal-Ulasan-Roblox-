# Rumus-Rumus Penting di Project Analisis Sentimen Roblox

## 1. TF-IDF (Term Frequency-Inverse Document Frequency)
TF-IDF adalah metode statistik untuk mengukur seberapa penting suatu kata dalam sebuah dokumen dibandingkan dengan seluruh corpus.

### Rumus TF (Term Frequency)
Mengukur frekuensi kemunculan kata \( t \) dalam dokumen \( d \):

\[
TF(t, d) = \frac{\text{Jumlah kemunculan kata } t \text{ dalam dokumen } d}{\text{Total kata dalam dokumen } d}
\]

### Rumus IDF (Inverse Document Frequency)
Mengukur seberapa jarang kata \( t \) muncul di seluruh corpus:

\[
IDF(t, D) = \log\left(\frac{\text{Total dokumen } (N)}{\text{Jumlah dokumen yang mengandung kata } t}\right)
\]

### Rumus TF-IDF
Hasil perkalian TF dan IDF:

\[
TFIDF(t, d, D) = TF(t, d) \times IDF(t, D)
\]

---

## 2. Support Vector Machine (SVM) Linear
Model pembelajaran mesin yang mencari hyperplane optimal untuk memisahkan dua kelas data dengan margin terbesar.

### Rumus Fungsi Objektif SVM
Untuk data yang tidak dapat dipisahkan secara linear (dengan slack variable \( \xi_i \) dan parameter regularisasi \( C \)):

\[
\min_{w, b, \xi} \quad \frac{1}{2} \|w\|^2 + C \sum_{i=1}^{n} \xi_i
\]

Dengan batasan:

\[
y_i (w^T x_i + b) \geq 1 - \xi_i \quad \text{dan} \quad \xi_i \geq 0 \quad \forall i
\]

Dimana:
- \( w \): vektor bobot (weight vector)
- \( b \): bias
- \( \xi_i \): slack variable (toleransi kesalahan klasifikasi)
- \( C \): parameter regularisasi (trade-off antara margin lebar dan kesalahan klasifikasi)
- \( x_i \): fitur input (vektor TF-IDF)
- \( y_i \): label kelas (positif, netral, negatif)

---

## 3. Metrik Evaluasi Model
### 3.1 Akurasi (Accuracy)
Persentase prediksi yang benar dari seluruh prediksi:

\[
\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}
\]

### 3.2 Presisi (Precision)
Persentase prediksi positif yang benar-benar positif:

\[
\text{Precision}_i = \frac{TP_i}{TP_i + FP_i}
\]

### 3.3 Recall
Persentase data positif yang benar-benar teridentifikasi:

\[
\text{Recall}_i = \frac{TP_i}{TP_i + FN_i}
\]

### 3.4 F1-Score
Rata-rata harmonik dari precision dan recall:

\[
\text{F1}_i = 2 \times \frac{\text{Precision}_i \times \text{Recall}_i}{\text{Precision}_i + \text{Recall}_i}
\]

### 3.5 Precision Macro, Recall Macro, F1 Macro
Rata-rata dari precision, recall, dan f1-score untuk semua kelas (tanpa mempertimbangkan jumlah data per kelas):

\[
\text{Precision}_{\text{macro}} = \frac{1}{k} \sum_{i=1}^{k} \text{Precision}_i
\]

\[
\text{Recall}_{\text{macro}} = \frac{1}{k} \sum_{i=1}^{k} \text{Recall}_i
\]

\[
\text{F1}_{\text{macro}} = \frac{1}{k} \sum_{i=1}^{k} \text{F1}_i
\]

Dimana \( k \): jumlah kelas (k=3: positif, netral, negatif)

### 3.6 Agreement Rate
Persentase kesesuaian antara label sentimen berbasis rating dan label sentimen berbasis teks (IndoBERT):

\[
\text{Agreement Rate} = \frac{\text{Jumlah prediksi yang sama antara rating dan IndoBERT}}{\text{Total review}} \times 100\%
\]

---

## Keterangan Simbol:
- \( TP \) (True Positive): data positif yang teridentifikasi benar
- \( TN \) (True Negative): data negatif yang teridentifikasi benar
- \( FP \) (False Positive): data negatif yang teridentifikasi sebagai positif (kesalahan)
- \( FN \) (False Negative): data positif yang teridentifikasi sebagai negatif (kesalahan)
- Subskrip \( i \): kelas ke-i (contoh: i=0 untuk negatif, i=1 untuk netral, i=2 untuk positif)
