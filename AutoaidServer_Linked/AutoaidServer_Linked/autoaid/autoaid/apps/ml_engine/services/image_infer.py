"""
ImageInferenceService
Supports two model types automatically:
  1. Old model (damage_classifier.h5) — 5 part classes, sigmoid multi-label
  2. New model (damage_classifier.h5) — 4 severity classes, softmax single-label

Auto-detects which model is loaded based on classes JSON.
"""

import os
import json
import logging
from typing import Dict, Any

import numpy as np

logger = logging.getLogger(__name__)

IMG_SIZE = 224

# Severity → AutoAid fault metadata
SEVERITY_META = {
    'Severe Damage': {
        'fault':             'Severe Vehicle Damage',
        'diagnosis':         'Severe structural or body damage detected',
        'possible_causes':   ['Major collision', 'Rollover', 'Heavy impact'],
        'recommended_action':'Do not drive — immediate inspection required',
        'requires_mechanic': True,
        'urgency':           'high',
    },
    'Minor Damage - Dent': {
        'fault':             'Minor Body Damage — Dent',
        'diagnosis':         'Minor dent or body deformation detected',
        'possible_causes':   ['Parking impact', 'Minor collision', 'Hail damage'],
        'recommended_action':'Schedule panel repair at a body shop',
        'requires_mechanic': True,
        'urgency':           'low',
    },
    'Minor Damage - Scratch': {
        'fault':             'Minor Body Damage — Scratch',
        'diagnosis':         'Surface scratch or paint damage detected',
        'possible_causes':   ['Scrape', 'Keying', 'Brush contact'],
        'recommended_action':'Schedule paint touch-up or panel respray',
        'requires_mechanic': False,
        'urgency':           'low',
    },
    'No Damage': {
        'fault':             'No Visible Damage',
        'diagnosis':         'No significant damage detected in this image',
        'possible_causes':   [],
        'recommended_action':'No immediate action required',
        'requires_mechanic': False,
        'urgency':           'none',
    },
}

# Part classes from old model
PART_META = {
    'headlamp':     {'fault': 'Body Damage — Headlamp',     'urgency': 'medium'},
    'rear_bumper':  {'fault': 'Body Damage — Rear Bumper',  'urgency': 'low'},
    'door':         {'fault': 'Body Damage — Door',         'urgency': 'low'},
    'hood':         {'fault': 'Engine / Body Damage — Hood','urgency': 'high'},
    'front_bumper': {'fault': 'Body Damage — Front Bumper', 'urgency': 'medium'},
}

PART_CONF_THRESHOLD     = 0.15
SEVERITY_CONF_THRESHOLD = 0.15


class ImageInferenceService:
    def __init__(self, model_path: str | None):
        self.model_path  = model_path
        self.model       = None
        self.classes     = None   # list of class name strings
        self.model_type  = None   # 'severity' or 'part'

        if not model_path:
            logger.warning('IMAGE_MODEL_PATH not set — image inference disabled')
            return

        if not os.path.exists(model_path):
            logger.warning('Image model not found at %s', model_path)
            return

        try:
            os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '3')
            import tensorflow as tf
            self.model = tf.keras.models.load_model(model_path, compile=False)
            logger.info('Loaded image model: %s', model_path)

            # Auto-detect classes file
            stem = os.path.splitext(model_path)[0]
            for suffix in ['_classes.json', '.labels.json']:
                classes_path = stem + suffix
                if os.path.exists(classes_path):
                    data = json.load(open(classes_path, 'r', encoding='utf-8'))
                    self.classes = data if isinstance(data, list) else data.get('classes', [])
                    break

            # Detect model type from classes
            if self.classes:
                severity_keywords = {'severe', 'minor', 'scratch', 'dent', 'no damage'}
                if any(any(k in c.lower() for k in severity_keywords) for c in self.classes):
                    self.model_type = 'severity'
                else:
                    self.model_type = 'part'
            else:
                # Guess from output shape
                out_shape = self.model.output_shape[-1]
                self.model_type = 'severity' if out_shape == 4 else 'part'

            logger.info('Image model type: %s, classes: %s', self.model_type, self.classes)

        except Exception as e:
            logger.exception('Failed to load image model: %s', e)
            self.model = None

    def _preprocess(self, image_path: str) -> np.ndarray:
        import cv2
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f'Cannot read image: {image_path}')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        return (img.astype(np.float32) / 255.0)[np.newaxis, ...]

    def predict(self, image_path: str) -> Dict[str, Any]:
        if not self.model:
            return {
                'top_label':      None,
                'top_confidence': 0.0,
                'detections':     [],
                'explanation':    {'note': 'Image model not loaded'},
            }

        try:
            x     = self._preprocess(image_path)
            preds = self.model.predict(x, verbose=0)[0]

            if self.model_type == 'severity':
                return self._predict_severity(preds)
            else:
                return self._predict_parts(preds)

        except Exception as e:
            logger.exception('Image inference failed: %s', e)
            return {
                'top_label':      None,
                'top_confidence': 0.0,
                'detections':     [],
                'explanation':    {'error': str(e)},
            }

    def _predict_severity(self, preds: np.ndarray) -> Dict[str, Any]:
        """Single-label softmax — pick top class."""
        idx       = int(np.argmax(preds))
        top_conf  = float(preds[idx])
        top_label = self.classes[idx] if self.classes and idx < len(self.classes) else str(idx)

        meta = SEVERITY_META.get(top_label, {
            'fault':             f'Damage detected: {top_label}',
            'diagnosis':         top_label,
            'possible_causes':   [],
            'recommended_action':'Schedule inspection',
            'requires_mechanic': True,
            'urgency':           'medium',
        })

        top3_idx = np.argsort(-preds)[:3].tolist()
        top3 = [{'label': self.classes[i] if self.classes else str(i),
                 'confidence': float(preds[i])} for i in top3_idx]

        # Skip if "No Damage" is top and high confidence
        if top_label == 'No Damage' and top_conf >= 0.70:
            return {
                'top_label':      None,
                'top_confidence': top_conf,
                'detections':     [],
                'fault_meta':     meta,
                'explanation':    {'top3': top3, 'note': 'No damage detected'},
            }

        if top_conf < SEVERITY_CONF_THRESHOLD:
            return {
                'top_label':      None,
                'top_confidence': top_conf,
                'detections':     [],
                'explanation':    {'top3': top3, 'note': 'Low confidence'},
            }

        return {
            'top_label':      meta.get('fault', top_label),
            'top_confidence': top_conf,
            'detections':     [{'label': top_label, 'confidence': top_conf}],
            'fault_meta':     meta,
            'all_scores':     {(self.classes[i] if self.classes else str(i)): float(preds[i])
                               for i in range(len(preds))},
            'explanation':    {'top3': top3, 'model_type': 'severity'},
        }

    def _predict_parts(self, preds: np.ndarray) -> Dict[str, Any]:
        """Multi-label sigmoid — any part above threshold."""
        part_names = ['headlamp', 'rear_bumper', 'door', 'hood', 'front_bumper']
        detections = []
        for i, conf in enumerate(preds):
            if float(conf) >= PART_CONF_THRESHOLD and i < len(part_names):
                part = part_names[i]
                meta = PART_META.get(part, {})
                detections.append({
                    'part':       part,
                    'label':      meta.get('fault', part),
                    'confidence': float(conf),
                    'urgency':    meta.get('urgency', 'medium'),
                })

        detections.sort(key=lambda d: d['confidence'], reverse=True)

        if not detections:
            return {
                'top_label':      None,
                'top_confidence': 0.0,
                'detections':     [],
                'explanation':    {'note': 'No parts detected above threshold'},
            }

        top = detections[0]
        return {
            'top_label':      top['label'],
            'top_confidence': top['confidence'],
            'detections':     detections,
            'fault_meta':     PART_META.get(top.get('part', ''), {}),
            'explanation':    {'n_detections': len(detections), 'top3': detections[:3],
                               'model_type': 'part'},
        }