"""
train_indobert.py
====================
Tahap 5b (revisi pipeline): fine-tuning IndoBERT — model utama.

Input: content_raw_clean (teks natural, hasil Tahap 2) — BUKAN
cleaned_content (hasil praproses penuh khusus SVM di Tahap 5a).
Target label: label_final (hasil Tahap 4 — gabungan RoBERTa + manual).

Split test set 80/20 (random_state=42, stratify) WAJIB identik dengan
Tahap 5a (train_svm.py) — syarat apple-to-apple di Tahap 6. Validation
set (buat plot training curve) diambil dari bagian train, tidak
mengganggu index test set.

Jalankan HANYA kalau torch.cuda.is_available() True (cek dulu manual
sebelum run kalau ragu) — CPU-only gak realistis buat 5 epoch/49k baris.

Output:
  - models/indobert_sentiment/best_model_hybrid/   (model + tokenizer)
  - models/indobert_sentiment/metrics_indobert.json
  - models/indobert_sentiment/confusion_matrix_indobert.png
  - data/processed/training_history.csv            (epoch, loss, acc)
  - data/processed/indobert_training_curve.png      (wajib buat Bab 4.5.2)
"""
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch
from torch.cuda.amp import autocast, GradScaler
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer

DATA_FILE = "data/processed/roblox_sentiment.csv"
OUTPUT_DIR = "models/indobert_sentiment/best_model_hybrid"
METRICS_FILE = "models/indobert_sentiment/metrics_indobert.json"
CM_FILE = "models/indobert_sentiment/confusion_matrix_indobert.png"
HISTORY_FILE = "data/processed/training_history.csv"
CURVE_FILE = "data/processed/indobert_training_curve.png"

MODEL_NAME = "indobenchmark/indobert-base-p1"
LABEL_MAP = {"negatif": 0, "netral": 1, "positif": 2}
LABEL_NAMES = ["negatif", "netral", "positif"]

RANDOM_STATE = 42       # harus sama persis dengan train_svm.py
TEST_SIZE = 0.20        # harus sama persis dengan train_svm.py
VAL_SIZE_IN_TRAIN = 0.1  # carve-out dari train, tidak sentuh test set
MAX_LENGTH = 128
BATCH_SIZE = 32
EPOCHS = 5
LR = 2e-5


class SentimentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=MAX_LENGTH):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        enc = self.tokenizer(
            str(self.texts[idx]),
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt',
        )
        return {
            'input_ids': enc['input_ids'].flatten(),
            'attention_mask': enc['attention_mask'].flatten(),
            'labels': torch.tensor(self.labels[idx], dtype=torch.long),
        }


def run_eval(model, loader, device):
    model.eval()
    preds, labels, losses = [], [], []
    loss_fn = torch.nn.CrossEntropyLoss()
    use_amp = device.type == 'cuda'
    with torch.no_grad():
        for batch in loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels_batch = batch['labels'].to(device)
            with autocast(enabled=use_amp):
                out = model(input_ids=input_ids, attention_mask=attention_mask)
                loss = loss_fn(out.logits, labels_batch)
            losses.append(loss.item())
            preds.extend(torch.argmax(out.logits, dim=1).cpu().tolist())
            labels.extend(labels_batch.cpu().tolist())
    acc = accuracy_score(labels, preds)
    return float(np.mean(losses)), acc, preds, labels


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    if device.type == 'cpu':
        print("PERINGATAN: CPU-only. 5 epoch/49k baris gak realistis di CPU (lihat panduan revisi).")
        print("Lanjut? Ctrl+C buat batalin dalam 10 detik...")
        import time
        time.sleep(10)

    df = pd.read_csv(DATA_FILE)
    assert 'label_final' in df.columns, "Tahap 4 belum jalan (label_final belum ada)."
    assert 'content_raw_clean' in df.columns, "Tahap 2 belum jalan (content_raw_clean belum ada)."

    df = df[['content_raw_clean', 'label_final']].dropna().copy()
    df['content_raw_clean'] = df['content_raw_clean'].astype(str).str.strip()
    df = df[df['content_raw_clean'].str.len() > 0].reset_index(drop=True)
    df['label'] = df['label_final'].map(LABEL_MAP)
    df = df.dropna(subset=['label'])
    df['label'] = df['label'].astype(int)
    print(f"Total baris dipakai: {len(df)}")
    print(df['label_final'].value_counts())

    texts = df['content_raw_clean'].tolist()
    labels = df['label'].tolist()

    # split test IDENTIK dengan train_svm.py (random_state, test_size, stratify)
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=labels
    )
    # val diambil dari train saja - test set di atas tetap utuh/identik dgn SVM
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        train_texts, train_labels, test_size=VAL_SIZE_IN_TRAIN, random_state=RANDOM_STATE, stratify=train_labels
    )
    print(f"Train: {len(train_texts)} | Val: {len(val_texts)} | Test: {len(test_texts)}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=3, ignore_mismatched_sizes=True
    )
    # tanpa ini, config.json kesave id2label generik ("LABEL_0" dst) - siapa pun
    # yang load model ini nanti dan percaya config.json bakal salah baca label.
    model.config.id2label = {v: k for k, v in LABEL_MAP.items()}
    model.config.label2id = dict(LABEL_MAP)
    model.to(device)

    train_ds = SentimentDataset(train_texts, train_labels, tokenizer)
    val_ds = SentimentDataset(val_texts, val_labels, tokenizer)
    test_ds = SentimentDataset(test_texts, test_labels, tokenizer)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False)

    class_weights = torch.tensor(
        compute_class_weight('balanced', classes=np.unique(train_labels), y=train_labels),
        dtype=torch.float,
    ).to(device)
    loss_fn = torch.nn.CrossEntropyLoss(weight=class_weights)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)

    # fp16 mixed precision - batch 32/seq128 di VRAM 6GB (RTX 2060) butuh ini,
    # gak dipakai kalau CPU (autocast+scaler no-op saat enabled=False).
    use_amp = device.type == 'cuda'
    scaler = GradScaler(enabled=use_amp)
    print(f"Mixed precision (fp16): {use_amp}")

    history = []
    best_val_acc = 0.0

    for epoch in range(1, EPOCHS + 1):
        model.train()
        train_losses, train_preds, train_true = [], [], []
        for batch in tqdm(train_loader, desc=f"Epoch {epoch}/{EPOCHS}"):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels_batch = batch['labels'].to(device)

            optimizer.zero_grad()
            with autocast(enabled=use_amp):
                out = model(input_ids=input_ids, attention_mask=attention_mask)
                loss = loss_fn(out.logits, labels_batch)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            train_losses.append(loss.item())
            train_preds.extend(torch.argmax(out.logits, dim=1).detach().cpu().tolist())
            train_true.extend(labels_batch.cpu().tolist())

        train_loss = float(np.mean(train_losses))
        train_acc = accuracy_score(train_true, train_preds)
        val_loss, val_acc, _, _ = run_eval(model, val_loader, device)

        print(f"Epoch {epoch}: train_loss={train_loss:.4f} train_acc={train_acc:.4f} "
              f"val_loss={val_loss:.4f} val_acc={val_acc:.4f}")

        history.append({
            'epoch': epoch, 'train_loss': train_loss, 'val_loss': val_loss,
            'train_acc': train_acc, 'val_acc': val_acc,
        })

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            print(f"  val_acc membaik ({best_val_acc:.4f}), simpan model...")
            model.save_pretrained(OUTPUT_DIR)
            tokenizer.save_pretrained(OUTPUT_DIR)

    history_df = pd.DataFrame(history)
    history_df.to_csv(HISTORY_FILE, index=False)
    print(f"\nTraining history disimpan: {HISTORY_FILE}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(history_df['epoch'], history_df['train_loss'], label='Train Loss')
    axes[0].plot(history_df['epoch'], history_df['val_loss'], label='Validation Loss')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    axes[0].set_title('Training vs Validation Loss')

    axes[1].plot(history_df['epoch'], history_df['train_acc'], label='Train Accuracy')
    axes[1].plot(history_df['epoch'], history_df['val_acc'], label='Validation Accuracy')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy')
    axes[1].legend()
    axes[1].set_title('Training vs Validation Accuracy')

    plt.tight_layout()
    plt.savefig(CURVE_FILE, dpi=150)
    plt.close()
    print(f"Training curve disimpan: {CURVE_FILE} (wajib buat Bab 4.5.2)")

    # evaluasi final pakai model TERBAIK (val_acc tertinggi), bukan checkpoint terakhir
    print("\nEvaluasi test set pakai best model (val_acc tertinggi)...")
    best_model = AutoModelForSequenceClassification.from_pretrained(OUTPUT_DIR).to(device)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False)
    _, test_acc, test_preds, test_true = run_eval(best_model, test_loader, device)

    best_model.eval()
    all_probs = []
    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            with autocast(enabled=use_amp):
                out = best_model(input_ids=input_ids, attention_mask=attention_mask)
            probs = torch.softmax(out.logits.float(), dim=1).cpu().numpy()
            all_probs.append(probs)
    all_probs = np.concatenate(all_probs, axis=0)

    from sklearn.metrics import roc_auc_score
    auc = roc_auc_score(test_true, all_probs, multi_class='ovr', average='macro')

    prec_mac, rec_mac, f1_mac, _ = precision_recall_fscore_support(
        test_true, test_preds, average='macro', zero_division=0
    )
    prec_arr, rec_arr, f1_arr, sup_arr = precision_recall_fscore_support(
        test_true, test_preds, labels=[0, 1, 2], average=None, zero_division=0
    )
    report = classification_report(test_true, test_preds, target_names=LABEL_NAMES, digits=4)
    cm = confusion_matrix(test_true, test_preds)

    print(f"Test Accuracy: {test_acc*100:.2f}%")
    print(f"AUC-ROC (OvR macro): {auc*100:.2f}%")
    print("\n" + report)

    plt.figure(figsize=(7, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges',
                xticklabels=LABEL_NAMES, yticklabels=LABEL_NAMES)
    plt.title('Confusion Matrix - IndoBERT (label_final, hybrid)')
    plt.ylabel('Label Aktual')
    plt.xlabel('Label Prediksi')
    plt.tight_layout()
    plt.savefig(CM_FILE, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Confusion matrix disimpan: {CM_FILE}")

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
        "model": f"IndoBERT ({MODEL_NAME}, fine-tuned {EPOCHS} epoch)",
        "label_source": "label_final (hybrid: RoBERTa + manual, Tahap 4)",
        "split": f"{int((1-TEST_SIZE)*100)}/{int(TEST_SIZE*100)}, random_state={RANDOM_STATE}, stratify=True (identik train_svm.py)",
        "test_accuracy": float(test_acc),
        "precision_macro": float(prec_mac),
        "recall_macro": float(rec_mac),
        "f1_macro": float(f1_mac),
        "auc_roc_ovr_macro": float(auc),
        "per_class": per_class,
        "confusion_matrix": cm.tolist(),
        "classification_report": report,
        "best_val_accuracy": float(best_val_acc),
    }
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    print(f"\nMetrics tersimpan: {METRICS_FILE}")
    print(f"Model tersimpan: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
