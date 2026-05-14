
"""Train an audio classifier on WAV files using mel-spectrograms.

- Input: manifest.csv (path,label)
- Train/val split stratified
- Model: AudioCNN
- Output: best.pt + best.labels.json

Usage:
python train_audio_cnn.py --manifest manifest.csv --out_dir audio_runs --epochs 50
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim

import librosa

# Import from backend code
from autoaid.apps.ml_engine.services.audio_model import AudioCNN


def extract_mel(wav_path: str, sr=16000, seconds=3, n_mels=64):
    y, _ = librosa.load(wav_path, sr=sr, mono=True)
    target = seconds * sr
    if len(y) < target:
        y = np.pad(y, (0, target - len(y)))
    else:
        y = y[:target]
    m = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, n_fft=1024, hop_length=320)
    m = librosa.power_to_db(m, ref=np.max)
    m = (m - m.min()) / (m.max() - m.min() + 1e-6)
    return m.astype(np.float32)


class AudioDataset(Dataset):
    def __init__(self, df, label_to_id):
        self.df = df.reset_index(drop=True)
        self.label_to_id = label_to_id

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        feat = extract_mel(row['path'])
        x = torch.tensor(feat)[None, ...]
        y = torch.tensor(self.label_to_id[row['label']], dtype=torch.long)
        return x, y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--out_dir', required=True)
    ap.add_argument('--epochs', type=int, default=30)
    ap.add_argument('--batch_size', type=int, default=16)
    ap.add_argument('--lr', type=float, default=1e-3)
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.manifest)
    labels = sorted(df['label'].unique().tolist())
    label_to_id = {l: i for i, l in enumerate(labels)}

    tr, va = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])

    train_ds = AudioDataset(tr, label_to_id)
    val_ds = AudioDataset(va, label_to_id)

    train_dl = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=2)
    val_dl = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, num_workers=2)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = AudioCNN(n_classes=len(labels)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    best_acc = 0.0

    for epoch in range(1, args.epochs + 1):
        model.train()
        train_loss = 0.0
        for x, y in train_dl:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            logits = model(x)
            loss = criterion(logits, y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * x.size(0)

        train_loss /= len(train_ds)

        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for x, y in val_dl:
                x, y = x.to(device), y.to(device)
                logits = model(x)
                pred = torch.argmax(logits, dim=1)
                correct += (pred == y).sum().item()
                total += y.numel()

        acc = correct / max(1, total)
        print(f"Epoch {epoch:03d} loss={train_loss:.4f} val_acc={acc:.4f}")

        if acc > best_acc:
            best_acc = acc
            ckpt = {'state_dict': model.state_dict(), 'n_classes': len(labels), 'labels': labels}
            torch.save(ckpt, out_dir / 'best.pt')
            (out_dir / 'best.labels.json').write_text(json.dumps(labels, indent=2), encoding='utf-8')

    print('Best val acc:', best_acc)


if __name__ == '__main__':
    main()
