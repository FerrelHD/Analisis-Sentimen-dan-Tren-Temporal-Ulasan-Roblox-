"""
train_svm.py
=============
Tahap 5a (revisi pipeline): SVM + TF-IDF baseline.

Praproses penuh (case folding, negation handling, stopword removal,
stemming) BARU dipanggil di sini — bukan lagi di awal pipeline. Input:
content_raw_clean (teks natural, Tahap 2). Hasilnya disimpan ke kolom
cleaned_content (menimpa hasil praproses lama).

Target label: label_final (hasil Tahap 4 — gabungan RoBERTa + manual),
BUKAN pseudo_label_teacher/pseudo_label_roberta.

CATATAN PERFORMA: bagian paling lama di script ini adalah stemming
Sastrawi ke seluruh dataset (49k+ baris), bukan training SVM-nya sendiri
(linear kernel + 5000 fitur itu cepat). Kalau dijalankan di PC lain,
percepatannya cuma kerasa kalau CPU-nya lebih kencang — Sastrawi jalan
single-thread, gak kepake GPU.

Output:
  - models/svm_teacher/svm_teacher.pkl
  - models/svm_teacher/tfidf_teacher.pkl
  - models/svm_teacher/metrics_svm_teacher.json
  - models/svm_teacher/confusion_matrix_svm_teacher.png
  - data/processed/ringkasan_hasil_svm.txt (siap paste ke Bab 4)
"""
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from src.preprocessor import clean_text

DATA_FILE = "data/processed/roblox_sentiment.csv"
OUTPUT_DIR = "models/svm_teacher"
REPORT_FILE = "data/processed/ringkasan_hasil_svm.txt"
LABEL_MAP = {"negatif": 0, "netral": 1, "positif": 2}
LABEL_NAMES = ["negatif", "netral", "positif"]
RANDOM_STATE = 42
TEST_SIZE = 0.20
TFIDF_MAX_FEATURES = 5000

os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    print("=" * 70)
    print("TAHAP 5A: SVM + TF-IDF (praproses penuh di sini, label_final)")
    print("=" * 70)

    df = pd.read_csv(DATA_FILE)
    print(f"\n[1] Loaded: {DATA_FILE} ({len(df)} baris)")

    assert 'label_final' in df.columns, "Tahap 4 belum jalan (label_final belum ada)."
    assert 'content_raw_clean' in df.columns, "Tahap 2 belum jalan (content_raw_clean belum ada)."

    dist = df['label_final'].value_counts().reindex(LABEL_NAMES)
    print("\n    Distribusi label_final:")
    for lbl, cnt in dist.items():
        print(f"      {lbl:10s}: {cnt:6d} ({cnt/len(df)*100:.2f}%)")

    # ponytail: skip re-stem kalau cleaned_content udah ada dari run sebelumnya (hemat
    # waktu pas cuma mau ganti hyperparameter kayak class_weight). Diverifikasi dulu
    # (bukan cuma cek kolom ada) - kalau kedeteksi token "neg" nyempil sendiri (Bug #1
    # lama: Sastrawi motong "_NEG" pas stem), berarti cleaned_content stale/dari versi
    # clean_text() lama - paksa stem ulang, jangan percaya buta.
    has_cached = 'cleaned_content' in df.columns and df['cleaned_content'].notna().mean() > 0.9
    stray_neg = False
    if has_cached:
        stray_neg = df['cleaned_content'].fillna('').str.contains(r'(?:^|\s)neg(?:\s|$)', regex=True).any()

    if has_cached and not stray_neg:
        print("\n[2] cleaned_content sudah ada & lolos verifikasi (gak ada token 'neg' nyempil) - skip stemming ulang.")
    else:
        if has_cached and stray_neg:
            print("\n[2] cleaned_content ada TAPI kedeteksi token 'neg' nyempil (Bug #1 lama, stale) - stem ULANG.", flush=True)
        print("\n[2] Praproses penuh content_raw_clean -> cleaned_content (stemming, bisa lama)...", flush=True)
        df['cleaned_content'] = df['content_raw_clean'].apply(clean_text)
        df.to_csv(DATA_FILE, index=False)
        print("    cleaned_content diperbarui & disimpan ke roblox_sentiment.csv")

    # PENTING: filter baris pakai content_raw_clean (BUKAN cleaned_content hasil stem).
    # Ini harus identik persis dengan filter di train_indobert.py, supaya row-set yang
    # masuk train_test_split sama - syarat random_state=42 menghasilkan test split yang
    # benar-benar sama (apple-to-apple, Tahap 6). Kalau filter pakai cleaned_content,
    # baris yang jadi kosong gara-gara stemming/stopword-removal bisa ke-drop di sini
    # tapi tetap ada di dataset IndoBERT -> row-set beda -> split beda diam-diam.
    work = df[['content_raw_clean', 'cleaned_content', 'label_final']].dropna(
        subset=['content_raw_clean', 'label_final']
    ).copy()
    work['content_raw_clean'] = work['content_raw_clean'].astype(str).str.strip()
    work = work[work['content_raw_clean'].str.len() > 0].reset_index(drop=True)
    work['cleaned_content'] = work['cleaned_content'].fillna('').astype(str)
    work['label'] = work['label_final'].map(LABEL_MAP)
    work = work.dropna(subset=['label'])
    work['label'] = work['label'].astype(int)

    n_empty_after_stem = (work['cleaned_content'].str.strip() == '').sum()
    print(f"    Baris dipakai (filter by content_raw_clean, identik train_indobert.py): {len(work)}")
    if n_empty_after_stem:
        print(f"    Catatan: {n_empty_after_stem} baris cleaned_content kosong setelah stemming "
              f"(tetap dipakai sbg dokumen kosong di TF-IDF, TIDAK dibuang - jaga row-set identik)")

    X = np.array(work['cleaned_content'].tolist(), dtype=object)
    y = np.array(work['label'].tolist(), dtype=int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"\n[3] Split 80/20 stratified, random_state={RANDOM_STATE}")
    print(f"    Train: {len(X_train)} | Test: {len(X_test)}")
    print("    (random_state ini WAJIB sama persis dengan Tahap 5b IndoBERT, syarat apple-to-apple)")

    print(f"\n[4] TF-IDF (max_features={TFIDF_MAX_FEATURES})...")
    tfidf = TfidfVectorizer(max_features=TFIDF_MAX_FEATURES)
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    print("\n[5] Training SVM (kernel=linear, C=1.0, class_weight=balanced, probability=True)...")
    # class_weight="balanced" - simetris sama train_indobert.py yang pakai
    # compute_class_weight('balanced') di loss-nya. Tanpa ini, perbandingan SVM vs
    # IndoBERT ke-confound: gap recall netral bisa murni efek rebalancing, bukan arsitektur.
    svm = SVC(kernel="linear", C=1.0, class_weight="balanced", random_state=RANDOM_STATE, probability=True)
    svm.fit(X_train_tfidf, y_train)
    print("    Training selesai.")

    joblib.dump(svm, os.path.join(OUTPUT_DIR, "svm_teacher.pkl"))
    joblib.dump(tfidf, os.path.join(OUTPUT_DIR, "tfidf_teacher.pkl"))

    print("\n[6] Evaluasi pada test set...")
    y_pred = svm.predict(X_test_tfidf)
    y_proba = svm.predict_proba(X_test_tfidf)

    accuracy = accuracy_score(y_test, y_pred)
    prec_mac, rec_mac, f1_mac, _ = precision_recall_fscore_support(
        y_test, y_pred, average="macro", zero_division=0
    )
    auc_svm = roc_auc_score(y_test, y_proba, multi_class="ovr", average="macro")
    prec_arr, rec_arr, f1_arr, sup_arr = precision_recall_fscore_support(
        y_test, y_pred, labels=[0, 1, 2], average=None, zero_division=0
    )
    report_svm = classification_report(y_test, y_pred, target_names=LABEL_NAMES, digits=4)
    cm_svm = confusion_matrix(y_test, y_pred)

    print(f"    Accuracy : {accuracy*100:.2f}%")
    print(f"    Precision (macro): {prec_mac*100:.2f}%")
    print(f"    Recall (macro): {rec_mac*100:.2f}%")
    print(f"    F1 (macro): {f1_mac*100:.2f}%")
    print(f"    AUC-ROC (OvR macro): {auc_svm*100:.2f}%")
    print("\n" + report_svm)

    plt.figure(figsize=(7, 5))
    sns.heatmap(cm_svm, annot=True, fmt="d", cmap="Blues",
                xticklabels=LABEL_NAMES, yticklabels=LABEL_NAMES)
    plt.title("Confusion Matrix - SVM (label_final, hybrid)")
    plt.ylabel("Label Aktual")
    plt.xlabel("Label Prediksi")
    plt.tight_layout()
    cm_path = os.path.join(OUTPUT_DIR, "confusion_matrix_svm_teacher.png")
    plt.savefig(cm_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"    Confusion matrix disimpan: {cm_path}")

    per_class = {
        lbl: {
            "precision": float(prec_arr[i]),
            "recall": float(rec_arr[i]),
            "f1": float(f1_arr[i]),
            "support": int(sup_arr[i]),
        }
        for i, lbl in enumerate(LABEL_NAMES)
    }
    metrics = {
        "model": "SVM (kernel=linear, C=1.0, class_weight=balanced, TF-IDF max_features=5000)",
        "label_source": "label_final (hybrid: RoBERTa + manual, Tahap 4)",
        "split": f"{int((1-TEST_SIZE)*100)}/{int(TEST_SIZE*100)}, random_state={RANDOM_STATE}, stratify=True",
        "test_accuracy": float(accuracy),
        "precision_macro": float(prec_mac),
        "recall_macro": float(rec_mac),
        "f1_macro": float(f1_mac),
        "auc_roc_ovr_macro": float(auc_svm),
        "per_class": per_class,
        "confusion_matrix": cm_svm.tolist(),
        "classification_report": report_svm,
    }
    metrics_path = os.path.join(OUTPUT_DIR, "metrics_svm_teacher.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    print(f"\nMetrics tersimpan: {metrics_path}")
    print(f"Model tersimpan: {OUTPUT_DIR}/svm_teacher.pkl, {OUTPUT_DIR}/tfidf_teacher.pkl")

    lines = [
        "RINGKASAN HASIL SVM (Tahap 5a, label_final hybrid) - untuk Bab 4",
        "=" * 70,
        f"Distribusi label_final (seluruh dataset, {int(dist.sum())} baris):",
    ]
    for lbl, cnt in dist.items():
        lines.append(f"  {lbl:10s}: {int(cnt):6d} ({cnt/dist.sum()*100:.2f}%)")
    lines += [
        "",
        "Classification Report SVM:",
        f"  {'Kelas':<12} {'Precision':>10} {'Recall':>10} {'F1-Score':>10} {'Support':>8}",
    ]
    for i, lbl in enumerate(LABEL_NAMES):
        lines.append(
            f"  {lbl:<12} {prec_arr[i]*100:>9.2f}% {rec_arr[i]*100:>9.2f}% {f1_arr[i]*100:>9.2f}% {int(sup_arr[i]):>7d}"
        )
    lines.append(f"  {'accuracy':<12} {'':>10} {'':>10} {accuracy*100:>9.2f}% {len(y_test):>7d}")
    lines.append(f"  {'macro avg':<12} {prec_mac*100:>9.2f}% {rec_mac*100:>9.2f}% {f1_mac*100:>9.2f}% {len(y_test):>7d}")
    lines.append(f"  AUC-ROC (OvR macro): {auc_svm*100:.2f}%")
    lines.append("")
    lines.append(f"Split: {int((1-TEST_SIZE)*100)}/{int(TEST_SIZE*100)}, random_state={RANDOM_STATE}, stratified, target=label_final")
    lines.append("PENTING: split ini harus identik (random_state sama) dengan Tahap 5b IndoBERT untuk perbandingan apple-to-apple di Tahap 6.")

    report_text = "\n".join(lines)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\nRingkasan siap-paste: {REPORT_FILE}")


if __name__ == "__main__":
    main()
