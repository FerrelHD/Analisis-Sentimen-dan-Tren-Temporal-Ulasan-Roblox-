"""
tahap4_merge_labels.py
=========================
Tahap 4 (revisi pipeline): merge label_final dari pseudo_label_roberta
(Tahap 3b) + label_manual (Tahap 3a, sample_manual_label.xls).

label_final = pseudo_label_roberta, ditimpa label_manual di baris sampel
manual. label_source menandai asal tiap baris ("roberta" / "manual").
"""
import os
import shutil
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd

DATA_FILE = "data/processed/roblox_sentiment.csv"
BACKUP_FILE = "data/processed/roblox_sentiment_backup_pre_merge.csv"
MANUAL_FILE = "data/processed/sample_manual_label.xls"


def main():
    if not os.path.exists(BACKUP_FILE):
        shutil.copy(DATA_FILE, BACKUP_FILE)
        print(f"Backup dibuat: {BACKUP_FILE}")

    df = pd.read_csv(DATA_FILE)
    manual = pd.read_excel(MANUAL_FILE)

    assert 'pseudo_label_roberta' in df.columns, "Tahap 3b belum jalan."
    assert manual['label_manual'].notna().all(), "Masih ada label_manual kosong di sample_manual_label.xls."

    manual = manual.copy()
    manual['label_manual'] = manual['label_manual'].str.strip().str.lower()

    valid_labels = {'positif', 'netral', 'negatif'}
    bad = set(manual['label_manual'].unique()) - valid_labels
    assert not bad, f"Ada label gak dikenal di label_manual: {bad}"

    n_manual = len(manual)
    print(f"Total baris dataset: {len(df)}")
    print(f"Total baris sampel manual: {n_manual}")

    df['label_final'] = df['pseudo_label_roberta']
    df['label_source'] = 'roberta'

    manual_map = manual.set_index('review_id')['label_manual']
    mask = df['reviewId'].isin(manual_map.index)
    df.loc[mask, 'label_final'] = df.loc[mask, 'reviewId'].map(manual_map)
    df.loc[mask, 'label_source'] = 'manual'

    n_matched = mask.sum()
    print(f"\nBaris ketemu & ditimpa jadi 'manual': {n_matched}")
    if n_matched != n_manual:
        print(f"PERINGATAN: {n_manual - n_matched} review_id di sample_manual_label.xls gak ketemu di roblox_sentiment.csv")

    print("\nDistribusi label_source:")
    print(df['label_source'].value_counts())

    print("\nDistribusi label_final:")
    print(df['label_final'].value_counts())

    print("\nDistribusi pseudo_label_roberta (pembanding, sebelum ditimpa manual):")
    print(df['pseudo_label_roberta'].value_counts())

    df.to_csv(DATA_FILE, index=False)
    print(f"\nTersimpan ke {DATA_FILE}")


if __name__ == "__main__":
    main()
