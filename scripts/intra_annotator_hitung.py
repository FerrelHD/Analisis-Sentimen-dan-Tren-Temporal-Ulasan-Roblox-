"""
Hitung Intra-Annotator Agreement
=================================
Jalankan SETELAH mengisi kolom 'label_ulang' di intra_annotator_blind.xlsx
"""

import pandas as pd

# Baca hasil re-label
relabel = pd.read_excel("data/processed/intra_annotator_blind.xlsx")
key = pd.read_csv("data/processed/intra_annotator_key.csv")

# Gabung berdasarkan review_id
merged = relabel.merge(key, on="review_id", how="inner")

# Normalisasi huruf besar/kecil
merged["label_ulang"] = merged["label_ulang"].str.strip().str.capitalize()
merged["label_manual"] = merged["label_manual"].str.strip().str.capitalize()

# Cek apakah sudah diisi semua
kosong = merged["label_ulang"].isna() | (merged["label_ulang"] == "")
if kosong.any():
    print(f"PERINGATAN: {kosong.sum()} sampel belum diisi label_ulang!")
    merged = merged[~kosong]

n = len(merged)
match = (merged["label_ulang"] == merged["label_manual"]).sum()

# 1. Percentage Agreement
pct = match / n * 100
print(f"Jumlah sampel: {n}")
print(f"Cocok: {match}/{n}")
print(f"Percentage Agreement: {pct:.2f}%")
print()

# 2. Cohen's Kappa (manual, tanpa library tambahan)
labels = sorted(merged["label_manual"].unique())
print(f"Kelas: {labels}")

# Observed agreement
po = match / n

# Expected agreement (by chance)
pe = 0
for lbl in labels:
    p1 = (merged["label_manual"] == lbl).sum() / n  # proporsi label awal = lbl
    p2 = (merged["label_ulang"] == lbl).sum() / n   # proporsi label ulang = lbl
    pe += p1 * p2

kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0

print(f"Observed agreement (Po): {po:.4f}")
print(f"Expected agreement (Pe): {pe:.4f}")
print(f"Cohen's Kappa: {kappa:.4f}")
print()

# Interpretasi Kappa (Landis & Koch, 1977)
if kappa < 0:       interp = "Poor"
elif kappa < 0.21:  interp = "Slight"
elif kappa < 0.41:  interp = "Fair"
elif kappa < 0.61:  interp = "Moderate"
elif kappa < 0.81:  interp = "Substantial"
else:               interp = "Almost Perfect"

print(f"Interpretasi: {interp} (Landis & Koch, 1977)")
print()

# Confusion matrix
print("=== Confusion Matrix (Label Awal vs Label Ulang) ===")
ct = pd.crosstab(merged["label_manual"], merged["label_ulang"],
                 rownames=["Label Awal"], colnames=["Label Ulang"], margins=True)
print(ct)

# Per-class agreement
print()
print("=== Per-Class Agreement ===")
for lbl in labels:
    subset = merged[merged["label_manual"] == lbl]
    if len(subset) > 0:
        m = (subset["label_ulang"] == lbl).sum()
        print(f"  {lbl}: {m}/{len(subset)} = {m/len(subset)*100:.1f}%")
