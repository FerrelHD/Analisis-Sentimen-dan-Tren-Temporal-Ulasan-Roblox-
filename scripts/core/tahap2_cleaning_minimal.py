"""
tahap2_cleaning_minimal.py
===========================
Tahap 2 (revisi pipeline): cleaning minimal, BUKAN praproses penuh.
Menambah kolom `content_raw_clean` (teks natural, input untuk RoBERTa &
IndoBERT) ke roblox_sentiment.csv. Tidak menyentuh kolom `cleaned_content`
(hasil praproses penuh lama, tetap dipakai khusus untuk SVM di Tahap 5a).
"""
import os
import shutil
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
from src.preprocessor import clean_text_minimal

DATA_FILE = "data/processed/roblox_sentiment.csv"
BACKUP_FILE = "data/processed/roblox_sentiment_backup_pre_hybrid.csv"


def main():
    if not os.path.exists(BACKUP_FILE):
        shutil.copy(DATA_FILE, BACKUP_FILE)
        print(f"Backup dibuat: {BACKUP_FILE}")
    else:
        print(f"Backup sudah ada, skip: {BACKUP_FILE}")

    df = pd.read_csv(DATA_FILE)
    print(f"Total baris: {len(df)}")

    df['content_raw_clean'] = df['content'].apply(clean_text_minimal)

    before = len(df)
    df = df[df['content_raw_clean'].str.strip() != ''].reset_index(drop=True)
    dropped = before - len(df)
    print(f"Baris dibuang (kosong setelah cleaning): {dropped}")

    df.to_csv(DATA_FILE, index=False)
    print(f"Selesai. content_raw_clean ditambahkan. Total baris sekarang: {len(df)}")
    print(df[['content', 'content_raw_clean']].sample(3, random_state=42))


if __name__ == "__main__":
    main()
