"""
tahap3b_roberta_autolabel.py
==============================
Tahap 3b (revisi pipeline): auto-labeling pakai model teacher RoBERTa.
Input teks natural (content_raw_clean, hasil Tahap 2) — BUKAN hasil
praproses penuh.

Model: w11wo/indonesian-roberta-base-sentiment-classifier
Output: kolom pseudo_label_roberta di roblox_sentiment.csv
        (positif / netral / negatif)
"""
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

DATA_FILE = "data/processed/roblox_sentiment.csv"
MODEL_NAME = "w11wo/indonesian-roberta-base-sentiment-classifier"
BATCH_SIZE = 32
MAX_LENGTH = 128
LABEL_MAP = {"positive": "positif", "neutral": "netral", "negative": "negatif"}


def main():
    df = pd.read_csv(DATA_FILE)
    assert 'content_raw_clean' in df.columns, "Jalankan Tahap 2 dulu (content_raw_clean belum ada)."
    print(f"Total baris: {len(df)}", flush=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}", flush=True)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.to(device)
    model.eval()

    texts = df['content_raw_clean'].fillna("").astype(str).tolist()
    n = len(texts)
    predictions = [None] * n

    start = time.time()
    n_batches = (n + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(0, n, BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        inputs = tokenizer(batch, padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors='pt')
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            logits = model(**inputs).logits
            batch_pred = torch.argmax(logits, dim=1).cpu().tolist()
        for j, p in enumerate(batch_pred):
            predictions[i + j] = LABEL_MAP[model.config.id2label[p]]

        batch_no = i // BATCH_SIZE + 1
        if batch_no % 50 == 0 or batch_no == n_batches:
            elapsed = time.time() - start
            done = min(i + BATCH_SIZE, n)
            rate = done / elapsed
            eta = (n - done) / rate if rate > 0 else 0
            print(f"[{batch_no}/{n_batches}] {done}/{n} baris - {elapsed:.0f}s elapsed - ETA {eta:.0f}s", flush=True)

    df['pseudo_label_roberta'] = predictions
    df.to_csv(DATA_FILE, index=False)

    print("\nSelesai. Distribusi pseudo_label_roberta:", flush=True)
    print(df['pseudo_label_roberta'].value_counts(), flush=True)
    print(f"\nTotal waktu: {time.time() - start:.0f}s", flush=True)


if __name__ == "__main__":
    main()
