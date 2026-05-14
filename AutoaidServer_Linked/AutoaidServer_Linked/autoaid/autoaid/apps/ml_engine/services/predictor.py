"""
Predictor — fuses image, audio, and text signals.
Audio model: audio_v4.keras  (13 fault classes, Keras CNN)
Image model: damage_classifier.h5 (5 part classes, MobileNetV2)
"""

import os
import re
import json
import pickle
import logging
from typing import Optional, Dict, Any
from django.conf import settings

from .image_infer import ImageInferenceService
from .audio_infer import AudioInferenceService

logger = logging.getLogger(__name__)

# ── Text keyword priors ───────────────────────────────────────────────────────
KEYWORD_PRIORS = [
    (re.compile(r'brake|squeal|grind',                          re.I), ('Worn Brake Pads \u2014 Metal-on-Metal Contact', 0.75)),
    (re.compile(r'oil\s*leak|low\s*oil|lubric',                re.I), ('Low Engine Oil Level',                          0.75)),
    (re.compile(r'ignition|starter|won.?t\s*start|grinding.*start', re.I), ('Failed Ignition System',                  0.75)),
    (re.compile(r'dead.?battery|weak.?battery|battery.*dead',  re.I), ('Dead or Weak Battery',                          0.80)),
    (re.compile(r'clicking|click.*start|won.?t.*start.*click', re.I), ('Dead or Weak Battery',                          0.75)),
    (re.compile(r'battery',                                    re.I), ('Dead or Weak Battery',                          0.70)),
    (re.compile(r'serpentine|belt\s*squeal',                   re.I), ('Worn or Loose Serpentine Belt',                 0.75)),
    (re.compile(r'power\s*steer|whining|groan',                re.I), ('Power Steering Pump Fault',                     0.75)),
    (re.compile(r'scratch|scrape',                             re.I), ('Body Damage',                                   0.70)),
    (re.compile(r'dent|collision|crash',                       re.I), ('Body Damage',                                   0.70)),
    (re.compile(r'rear|boot|trunk|tail|back',                  re.I), ('Body Damage — Rear Bumper', 0.60)),
]

# ── Fallback metadata ─────────────────────────────────────────────────────────
FALLBACK_META = {
    'Body Damage': {
        'diagnosis':          'Vehicle body damage detected',
        'possible_causes':    ['Collision', 'Scrape', 'Impact damage'],
        'recommended_action': 'Assess structural integrity; visit a body repair shop',
        'requires_mechanic':  True,
        'urgency':            'medium',
    },
    'Body Damage \u2014 Headlamp': {
        'diagnosis':          'Headlamp damage detected',
        'possible_causes':    ['Collision', 'Impact'],
        'recommended_action': 'Replace headlamp assembly',
        'requires_mechanic':  True,
        'urgency':            'medium',
    },
    'Body Damage \u2014 Rear Bumper': {
        'diagnosis':          'Rear bumper damage detected',
        'possible_causes':    ['Rear collision', 'Parking impact'],
        'recommended_action': 'Inspect and replace rear bumper',
        'requires_mechanic':  True,
        'urgency':            'low',
    },
    'Body Damage \u2014 Door': {
        'diagnosis':          'Door damage detected',
        'possible_causes':    ['Side collision', 'Scrape'],
        'recommended_action': 'Panel repair or door replacement required',
        'requires_mechanic':  True,
        'urgency':            'low',
    },
    'Engine / Body Damage \u2014 Hood': {
        'diagnosis':          'Hood / engine bay damage detected',
        'possible_causes':    ['Front collision', 'Impact'],
        'recommended_action': 'Inspect engine bay for damage before driving',
        'requires_mechanic':  True,
        'urgency':            'high',
    },
    'Body Damage \u2014 Front Bumper': {
        'diagnosis':          'Front bumper damage detected',
        'possible_causes':    ['Front collision', 'Parking impact'],
        'recommended_action': 'Inspect front bumper and chassis',
        'requires_mechanic':  True,
        'urgency':            'medium',
    },
}


class Predictor:
    def __init__(self):
        self.image_service = ImageInferenceService(
            getattr(settings, 'IMAGE_MODEL_PATH', None) or os.getenv('IMAGE_MODEL_PATH')
        )
        self.audio_service = AudioInferenceService(
            getattr(settings, 'AUDIO_MODEL_PATH', None) or os.getenv('AUDIO_MODEL_PATH')
        )

        # Load trained text model
        self._text_pipeline = None
        self._text_le       = None
        self._text_classes  = None

        text_model_path = getattr(settings, 'TEXT_MODEL_PATH', None) or os.getenv('TEXT_MODEL_PATH')
        text_le_path    = getattr(settings, 'TEXT_LE_PATH',    None) or os.getenv('TEXT_LE_PATH')
        text_cls_path   = getattr(settings, 'TEXT_CLASSES_PATH', None) or os.getenv('TEXT_CLASSES_PATH')

        try:
            if text_model_path and os.path.exists(text_model_path):
                with open(text_model_path, 'rb') as f:
                    self._text_pipeline = pickle.load(f)
                with open(text_le_path, 'rb') as f:
                    self._text_le = pickle.load(f)
                with open(text_cls_path) as f:
                    self._text_classes = json.load(f)
                logger.info('Text model loaded successfully')
        except Exception as e:
            logger.warning('Failed to load text model: %s', e)

    def predict(
        self,
        *,
        image_path: Optional[str],
        audio_path: Optional[str],
        text: Optional[str],
    ) -> Dict[str, Any]:

        image_out = self.image_service.predict(image_path) if image_path else None
        audio_out = self.audio_service.predict(audio_path) if audio_path else None

        # ── Text: try TF-IDF model first, fall back to keywords ──────────────
        text = (text or '').strip()
        prior_label, prior_conf = None, 0.0

        if text and self._text_pipeline is not None:
            try:
                probs     = self._text_pipeline.predict_proba([text])[0]
                top_idx   = int(probs.argmax())
                top_conf  = float(probs[top_idx])
                top_fault = self._text_le.classes_[top_idx]
                prior_label = top_fault
                prior_conf  = top_conf
                logger.debug('Text model: %s @ %.2f', top_fault, top_conf)
            except Exception as e:
                logger.warning('Text model inference failed: %s', e)

        if not prior_label:
            for rx, (label, conf) in KEYWORD_PRIORS:
                if text and rx.search(text):
                    prior_label, prior_conf = label, conf
                    break

        # ── Build candidate list ──────────────────────────────────────────────
        candidates = []
        if image_out and image_out.get('top_label'):
            img_conf = float(image_out.get('top_confidence', 0.0))
            if img_conf >= 0.15: # lowered threshold to allow more image signals, even if weak
                candidates.append(('image', image_out['top_label'], img_conf))
                #float(image_out.get('top_confidence', 0.0))))
            else:
                logger.info('Image prediction ignored (low confidence: %.2f)', img_conf)
        if audio_out and audio_out.get('top_label'):
            candidates.append(('audio', audio_out['top_label'],
                                float(audio_out.get('top_confidence', 0.0))))
        if prior_label:
            candidates.append(('text', prior_label, float(prior_conf)))

        if not candidates:
            return {
                'diagnosis':          'Insufficient data to diagnose',
                'confidence':         0.0,
                'recommended_action': 'Provide an image, audio recording, or description for diagnosis',
                'possible_causes':    [],
                'requires_mechanic':  False,
                'explanation':        {'reason': 'No model outputs and no text prior matched.'},
            }

        # ── Fusion ────────────────────────────────────────────────────────────
        best_label = None
        fused_conf = 0.0
        evidence   = []
        scores     = {}

        has_image = image_out and image_out.get('top_label')
        has_audio = audio_out and audio_out.get('top_label')
        has_text  = bool(prior_label)

        if has_image and has_audio and has_text:
            weight = {'image': 0.40, 'audio': 0.50, 'text': 0.10}
        elif has_image and has_audio:
            weight = {'image': 0.45, 'audio': 0.55, 'text': 0.00}
        elif has_image and has_text:
            weight = {'image': 0.85, 'audio': 0.00, 'text': 0.15}
        elif has_audio and has_text:
            weight = {'image': 0.00, 'audio': 0.85, 'text': 0.15}
        elif has_image:
            weight = {'image': 1.00, 'audio': 0.00, 'text': 0.00}
        elif has_audio:
            weight = {'image': 0.00, 'audio': 1.00, 'text': 0.00}
        else:
            weight = {'image': 0.00, 'audio': 0.00, 'text': 1.00}
        # High confidence shortcut: if audio or image is very sure, trust it
        for source, label, conf in candidates:
            if source == 'audio' and conf >= 0.85:
                best_label = label
                fused_conf = float(conf)
                evidence   = [{'source': source, 'label': label, 'confidence': conf}]
                scores     = {label: conf}
                logger.info('Audio shortcut fired: %s @ %.2f', label, conf)
                break
            if source == 'image' and conf >= 0.60:
                best_label = label
                fused_conf = float(conf)
                evidence   = [{'source': source, 'label': label, 'confidence': conf}]
                scores     = {label: conf}
                logger.info('Image shortcut fired: %s @ %.2f', label, conf)
                break

        # Weighted fusion fallback
        if best_label is None:
            for source, label, conf in candidates:
                scores[label] = scores.get(label, 0.0) + weight.get(source, 0.1) * conf
                evidence.append({'source': source, 'label': label, 'confidence': conf})
            best_label = max(scores.items(), key=lambda kv: kv[1])[0]
            fused_conf = float(max(0.0, min(1.0, scores[best_label])))
            logger.info('Weighted fusion result: %s @ %.2f', best_label, fused_conf)

        # ── Resolve metadata ──────────────────────────────────────────────────
        audio_fault_info = {}
        if audio_out:
            audio_fault_info = audio_out.get('fault_meta', {})
            if not audio_fault_info and self.audio_service.fault_info:
                audio_fault_info = self.audio_service.fault_info.get(best_label, {})

        if audio_fault_info:
            meta = {
                'diagnosis':          audio_fault_info.get('description', best_label),
                'possible_causes':    _causes_from_fault_info(audio_fault_info),
                'recommended_action': audio_fault_info.get('urgency_label', 'Schedule inspection'),
                'requires_mechanic':  True,
                'urgency':            audio_fault_info.get('urgency', 'medium'),
            }
        elif best_label in FALLBACK_META:
            meta = FALLBACK_META[best_label]
        else:
            meta = {
                'diagnosis':          f'Condition detected: {best_label}',
                'possible_causes':    [],
                'recommended_action': 'Schedule inspection',
                'requires_mechanic':  fused_conf >= getattr(settings, 'CONFIDENCE_THRESHOLD', 0.3),
                'urgency':            'medium',
            }

        # ── Apply confidence threshold ────────────────────────────────────────
        conf_threshold    = getattr(settings, 'CONFIDENCE_THRESHOLD', 0.3)
        requires_mechanic = bool(meta.get('requires_mechanic', True))

        if fused_conf < conf_threshold:
            recommended_action = 'Suggest manual inspection (low confidence)'
            requires_mechanic  = True
        else:
            recommended_action = meta.get('recommended_action', 'Schedule inspection')

        explanation = {
            'fusion': {
                'weights':  weight,
                'scores':   scores,
                'evidence': evidence,
            },
            'image': image_out,
            'audio': audio_out,
            'text_prior': {
                'label':      prior_label,
                'confidence': prior_conf,
                'text':       text[:200],
            },
        }

        return {
            'diagnosis':          meta.get('diagnosis', best_label),
            'confidence':         round(fused_conf, 4),
            'recommended_action': recommended_action,
            'possible_causes':    meta.get('possible_causes', []),
            'requires_mechanic':  requires_mechanic,
            'explanation':        explanation,
        }


def _causes_from_fault_info(info: dict) -> list:
    part  = info.get('part', '')
    spec  = info.get('specialization', '')
    desc  = info.get('description', '')
    causes = []
    if part: causes.append(f'Fault in: {part}')
    if spec: causes.append(f'System: {spec}')
    if desc: causes.append(desc[:120])
    return causes or ['Requires inspection']