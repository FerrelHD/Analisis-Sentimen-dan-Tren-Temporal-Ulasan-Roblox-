# 🎓 PANDUAN MENJAWAB SIDANG: TRIANGULASI MANUAL VS OTOMATIS

## 1. Skenario Pertanyaan Penguji
Penguji biasanya akan bertanya dengan nada memancing atau menguji batasan sistem Anda:
* *"Kenapa bagian analisis peristiwa riil ini tidak diotomatisasi saja sekalian oleh sistem?"*
* *"Kalau bagian ini diketik manual, apa bedanya penelitian Anda dengan orang yang membaca ulasan satu per satu?"*
* *"Berarti sistem Anda belum sepenuhnya cerdas ya, karena masih butuh campur tangan manusia?"*

---

## 2. Jawaban Utama (Elevator Pitch - Hafalkan Inti Ini)
**Jawab dengan tenang dan tersenyum:**

> *"Terima kasih atas pertanyaannya, Bapak/Ibu. Betul, bagian triangulasi peristiwa riil memang saya lakukan secara manual (analisis kualitatif). Keputusan ini saya ambil dengan sadar karena fokus utama (scope) skripsi saya adalah mengevaluasi kinerja model **[Sebutkan Model, misal: SVM/IndoBERT]** dalam mengklasifikasikan sentimen dan mengekstrak topik.* 
> 
> *Sistem saya telah berhasil melakukan tugas komputasi beratnya, yaitu secara otomatis menemukan anomali volume dan mengekstrak bigram (kata kunci) dari puluhan ribu data. Peran saya sebagai peneliti di sini adalah memberikan **interpretasi (domain knowledge)** yang tidak dimiliki oleh mesin, untuk menghubungkan kata kunci tersebut dengan konteks peristiwa di dunia nyata."*

---

## 3. Amunisi Tambahan (Gunakan jika penguji mengejar lebih jauh)
Jika penguji masih bertanya mengapa tidak sekalian di-coding saja, gunakan 3 argumen pemungkas ini:

### Argumen 1: Batasan Ruang Lingkup (Scope)
*"Jika saya mengotomatisasi pencocokan peristiwa riil, saya harus membangun arsitektur tambahan seperti Web Scraper untuk Twitter atau API Reddit, serta menggunakan Large Language Model (LLM) untuk pencocokan semantik. Hal tersebut akan memperlebar ruang lingkup penelitian (out of scope) dan menggeser fokus dari evaluasi model sentimen analisis itu sendiri."*

### Argumen 2: Akurasi Konteks Game (Domain Expertise)
*"Mesin statistik klasik memiliki keterbatasan dalam memahami konteks spesifik game. Misalnya, kata kunci 'wajah' atau 'muka'. Sistem otomatis bisa saja gagal memahami bahwa kata tersebut merujuk pada protes spesifik terkait update 'Dynamic Heads' di Roblox. Sebagai peneliti yang memahami konteks (domain expert), saya bisa memberikan kesimpulan yang 100% akurat tanpa risiko halusinasi sistem."*

### Argumen 3: Mixed-Methodology (Kuantitatif + Kualitatif)
*"Pendekatan ini justru merupakan penerapan Mixed-Methods. Sistem bertugas di ranah kuantitatif (menghitung sentimen dan frekuensi kata secara presisi dari big data), sementara saya bertugas di ranah kualitatif (memvalidasi hasil sistem dengan Open Source Intelligence/OSINT). Ini membuktikan bahwa dashboard saya berfungsi dengan baik sebagai Decision Support System (DSS)."*

---

## 4. Simulasi Tanya-Jawab (Roleplay)

**Penguji:** 
*"Jadi kalau besok ada protes baru di Roblox, dashboard Anda tidak bisa tahu otomatis penyebabnya?"*

**Anda (Jawaban):** 
*"Dashboard saya **akan tahu otomatis** kapan protes itu terjadi (terdeteksi dari lonjakan grafik volume negatif) dan **akan tahu otomatis** apa topik yang sedang diprotes (terdeteksi dari tabel ekstraksi Bigram). Namun, untuk merangkai kalimat kesimpulan akhir seperti 'Telah terjadi server down di region A', itu tetap membutuhkan verifikasi saya sebagai analis. Dashboard ini mempercepat pekerjaan analisis dari yang tadinya berhari-hari menjadi hanya beberapa menit."*

---

> **💡 Tips Tambahan saat Sidang:**
> Jangan pernah menggunakan kata *"karena saya tidak bisa codingnya"* atau *"karena waktunya mepet"*. Selalu gunakan alasan metodologis (ruang lingkup, akurasi, dan *domain knowledge*) seperti di atas. Penguji sangat menyukai mahasiswa yang tahu kapan harus menggunakan mesin dan kapan harus menggunakan otak manusia!
