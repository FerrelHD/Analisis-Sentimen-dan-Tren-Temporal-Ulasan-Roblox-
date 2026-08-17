"""
tahap7_predict_full_dataset.py
================================
Tahap 7 (revisi pipeline): infer model IndoBERT hybrid (Tahap 5b) ke SELURUH
dataset (bukan cuma test set) - buat refresh kolom `sentiment_indobert` yang
dipakai app.py & skrip figure tren temporal di mana-mana.

PENTING: input HARUS content_raw_clean, tanpa preprocessing tambahan (BUKAN
preprocess_text() versi lama di src/predict_indobert.py yang lowercase +
buang tanda baca) - model dilatih (train_indobert.py) langsung dari
content_raw_clean apa adanya. Preprocessing tambahan di sini = train/serve
skew, bisa nurunin akurasi real-world walau angka evaluasi Tahap 5b/6 tetap sah
(karena split test itu juga dari content_raw_clean apa adanya).

Kolom sentiment_indobert LAMA (hasil model pra-revisi) disimpan dulu ke
sentiment_indobert_old_pipeline sebelum ditimpa, buat pembanding Bab 4/5.

Output: roblox_sentiment.csv dengan sentiment_indobert ter-refresh.
"""
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

DATA_FILE = "data/processed/roblox_sentiment.csv"
MODEL_DIR = "models/indobert_sentiment/best_model_hybrid"
BATCH_SIZE = 32
MAX_LENGTH = 128
ID2LABEL = {0: "negatif", 1: "netral", 2: "positif"}


def main():
    df = pd.read_csv(DATA_FILE)
    assert 'content_raw_clean' in df.columns, "Tahap 2 belum jalan."
    assert os.path.exists(MODEL_DIR), f"Model tidak ditemukan: {MODEL_DIR} - jalankan train_indobert.py dulu."

    if 'sentiment_indobert' in df.columns and 'sentiment_indobert_old_pipeline' not in df.columns:
        df['sentiment_indobert_old_pipeline'] = df['sentiment_indobert']
        print("Kolom sentiment_indobert lama disimpan ke sentiment_indobert_old_pipeline (pembanding Bab 4/5).")

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    if device.type == 'cpu':
        print("PERINGATAN: CPU-only. Inference 49k baris bisa berjam-jam (RoBERTa Tahap 3b: 3,35 jam).")
        print("Pertimbangkan jalanin ini di PC RTX 2060. Lanjut? Ctrl+C buat batalin dalam 10 detik...")
        time.sleep(10)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.to(device)
    model.eval()

    texts = df['content_raw_clean'].fillna('').astype(str).tolist()
    n = len(texts)
    predictions = [None] * n
    use_amp = device.type == 'cuda'

    start = time.time()
    n_batches = (n + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(0, n, BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        inputs = tokenizer(batch, truncation=True, padding='max_length', max_length=MAX_LENGTH, return_tensors='pt')
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            with torch.cuda.amp.autocast(enabled=use_amp):
                logits = model(**inputs).logits
            batch_pred = torch.argmax(logits, dim=1).cpu().tolist()
        for j, p in enumerate(batch_pred):
            predictions[i + j] = ID2LABEL[p]

        batch_no = i // BATCH_SIZE + 1
        if batch_no % 50 == 0 or batch_no == n_batches:
            elapsed = time.time() - start
            done = min(i + BATCH_SIZE, n)
            rate = done / elapsed
            eta = (n - done) / rate if rate > 0 else 0
            print(f"[{batch_no}/{n_batches}] {done}/{n} baris - {elapsed:.0f}s elapsed - ETA {eta:.0f}s", flush=True)

    df['sentiment_indobert'] = predictions
    df.to_csv(DATA_FILE, index=False)

    print("\nSelesai. Distribusi sentiment_indobert (model hybrid baru):")
    print(df['sentiment_indobert'].value_counts())
    if 'sentiment_indobert_old_pipeline' in df.columns:
        print("\nDistribusi sentiment_indobert_old_pipeline (model lama, pembanding):")
        print(df['sentiment_indobert_old_pipeline'].value_counts())
    print(f"\nTotal waktu: {time.time() - start:.0f}s")


if __name__ == "__main__":
    main()
