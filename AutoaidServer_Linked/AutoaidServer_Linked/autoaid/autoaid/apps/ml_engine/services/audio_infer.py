"""
AudioInferenceService — uses audio_v4.keras trained with:
  sr=22050, duration=4s, n_mels=128, n_fft=2048, hop_length=512
  normalisation: (mel_db - mean) / (std + 1e-8)
"""

import os
import json
import logging
from typing import Dict, Any

import numpy as np

logger = logging.getLogger(__name__)

# ── Must match train_audio_v4.py exactly ─────────────────────────────────────
SAMPLE_RATE  = 22050
DURATION     = 4
N_MELS       = 128
N_FFT        = 2048
HOP_LENGTH   = 512


class AudioInferenceService:
    def __init__(self, model_path: str | None):
        self.model_path = model_path
        self.model      = None
        self.labels     = None        # list of class name strings
        self.fault_info = {}          # rich metadata from audio_v4_classes.json

        if not model_path:
            logger.warning('AUDIO_MODEL_PATH not set — audio inference disabled')
            return

        if not os.path.exists(model_path):
            logger.warning('Audio model not found at %s', model_path)
            return

        try:
            os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '3')
            import tensorflow as tf
            self.model = tf.keras.models.load_model(model_path, compile=False)
            logger.info('Loaded audio model: %s', model_path)

            # Load classes JSON — same directory, same stem + _classes.json
            stem        = os.path.splitext(model_path)[0]          # …/audio_v4
            classes_path = stem + '_classes.json'
            if os.path.exists(classes_path):
                data = json.load(open(classes_path, 'r', encoding='utf-8'))
                if isinstance(data, dict):
                    self.labels     = data.get('classes', [])
                    self.fault_info = data.get('fault_info', {})
                elif isinstance(data, list):
                    self.labels = data
                logger.info('Loaded %d audio classes', len(self.labels))
            else:
                logger.warning('Classes file not found: %s', classes_path)

        except Exception as e:
            logger.exception('Failed to load audio model: %s', e)
            self.model = None

    # ── Feature extraction — must match train_audio_v4.py ────────────────────
    def _extract_mel(self, wav_path: str) -> np.ndarray:
        import librosa
        y, sr = librosa.load(wav_path, sr=SAMPLE_RATE, duration=DURATION, mono=True)
        target = SAMPLE_RATE * DURATION
        if len(y) < target:
            y = np.pad(y, (0, target - len(y)))
        y = y[:target]

        mel    = librosa.feature.melspectrogram(
                    y=y, sr=sr, n_mels=N_MELS, n_fft=N_FFT, hop_length=HOP_LENGTH)
        mel_db = librosa.power_to_db(mel, ref=np.max)

        # Standardise — same as training
        mel_std = (mel_db - mel_db.mean()) / (mel_db.std() + 1e-8)
        return mel_std.astype(np.float32)   # shape: (128, 173)

    def predict(self, wav_path: str) -> Dict[str, Any]:
        if not self.model:
            return {
                'top_label':      None,
                'top_confidence': 0.0,
                'probs':          {},
                'explanation':    {'note': 'Audio model not loaded'},
            }

        try:
            feat = self._extract_mel(wav_path)           # (128, 173)
            # Keras CNN expects (batch, height, width, channels)
            x    = feat[np.newaxis, :, :, np.newaxis]    # (1, 128, 173, 1)

            probs = self.model.predict(x, verbose=0)[0]  # (n_classes,)

            idx       = int(np.argmax(probs))
            top_prob  = float(probs[idx])
            top_label = self._label(idx)

            top3_idx = np.argsort(-probs)[:3].tolist()
            top3     = [{'label': self._label(i), 'confidence': float(probs[i])}
                        for i in top3_idx]

            # Attach rich fault metadata if available
            fault_meta = self.fault_info.get(top_label, {})

            return {
                'top_label':      top_label,
                'top_confidence': top_prob,
                'probs':          {self._label(i): float(probs[i])
                                   for i in range(len(probs))},
                'fault_meta':     fault_meta,
                'explanation':    {
                    'top3': top3,
                    'feature': {
                        'type':      'mel_spectrogram',
                        'sr':         SAMPLE_RATE,
                        'seconds':    DURATION,
                        'n_mels':     N_MELS,
                    },
                },
            }

        except Exception as e:
            logger.exception('Audio inference failed: %s', e)
            return {
                'top_label':      None,
                'top_confidence': 0.0,
                'probs':          {},
                'explanation':    {'error': str(e)},
            }

    def _label(self, idx: int) -> str:
        if self.labels and idx < len(self.labels):
            return self.labels[idx]
        return str(idx)