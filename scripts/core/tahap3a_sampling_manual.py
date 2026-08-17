"""
tahap3a_sampling_manual.py
=============================
Tahap 3a (revisi pipeline): sampling manual pakai rumus Cochran,
stratified dari pseudo_label_roberta (hasil Tahap 3b).

n dihitung dari N aktual (bukan hardcode), lalu dialokasikan proporsional
ke 3 kelas biar kelas minoritas (netral) tetap kewakilan.

Output:
  - sample_manual_label.csv (kolom: review_id, content_raw_clean, tanggal,
    label_manual kosong — TANPA rating/prediksi RoBERTa, biar blind)
"""
import math
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd

DATA_FILE = "data/processed/roblox_sentiment.csv"
OUTPUT_FILE = "data/processed/sample_manual_label.csv"
RANDOM_STATE = 42

Z, P, Q, E = 1.96, 0.5, 0.5, 0.05


def cochran_n(N):
    n0 = (Z ** 2 * P * Q) / E ** 2
    n = n0 / (1 + (n0 - 1) / N)
    return math.ceil(n)


def main():
    df = pd.read_csv(DATA_FILE)
    assert 'pseudo_label_roberta' in df.columns, "Jalankan Tahap 3b dulu (pseudo_label_roberta belum ada)."

    N = len(df)
    n = cochran_n(N)
    print(f"N aktual: {N}")
    print(f"n (Cochran, dibulatkan ke atas): {n}")

    props = df['pseudo_label_roberta'].value_counts(normalize=True)
    alloc = (props * n).round().astype(int)
    diff = n - alloc.sum()
    if diff != 0:
        alloc[alloc.idxmax()] += diff  # koreksi pembulatan ke kelas terbesar

    print("\nAlokasi proporsional per kelas:")
    print(alloc)

    parts = [
        df[df['pseudo_label_roberta'] == label].sample(n=count, random_state=RANDOM_STATE)
        for label, count in alloc.items()
    ]
    sample = pd.concat(parts)

    # acak urutan final (hindari urutan per-kelas / kronologis)
    sample = sample.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

    export = sample[['reviewId', 'content_raw_clean', 'at']].rename(
        columns={'reviewId': 'review_id', 'at': 'tanggal'}
    )
    export['label_manual'] = ''

    export.to_csv(OUTPUT_FILE, index=False)
    print(f"\nTersimpan: {OUTPUT_FILE} ({len(export)} baris)")
    print("Kolom:", export.columns.tolist())
    print("\n(review_id dipertahankan biar bisa di-merge balik ke roblox_sentiment.csv di Tahap 4)")


if __name__ == "__main__":
    main()
