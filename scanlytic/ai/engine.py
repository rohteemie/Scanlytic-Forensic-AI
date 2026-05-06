"""
AI engine for Scanlytic-ForensicAI.

Handles local model inference and returns normalized AI scoring metadata.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import joblib

from scanlytic.utils.logger import get_logger

logger = get_logger()


class AIEngine:
    """
    Optional AI inference engine.

    Supports local model inference and safe fallbacks when disabled or
    model assets are missing.
    """

    def __init__(
        self,
        enabled: bool = False,
        backend: str = 'local',
        model_path: Optional[str] = None,
        confidence_threshold: float = 0.6
    ) -> None:
        self.enabled = enabled
        self.backend = backend
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self._model = None

        if self.enabled:
            self._load_model()

    def _load_model(self) -> None:
        """Load local model if configured and available."""
        if self.backend != 'local':
            logger.warning(
                "AI backend '%s' not supported yet", self.backend
            )
            return

        if not self.model_path:
            logger.info("AI enabled but no model_path provided")
            return

        model_file = Path(self.model_path)
        if not model_file.exists():
            logger.warning("AI model not found: %s", model_file)
            return

        try:
            self._model = joblib.load(model_file)
            logger.info("AI model loaded from %s", model_file)
        except Exception as exc:
            logger.warning("Failed to load AI model: %s", exc)
            self._model = None

    def score(self, features: Dict[str, Any],
              classification: Dict[str, str]) -> Dict[str, Any]:
        """
        Produce AI scoring results.

        Returns:
            Dict[str, Any]: AI scoring metadata. If disabled or unavailable,
            status describes why no score was produced.
        """
        if not self.enabled:
            return {
                'status': 'disabled',
                'backend': self.backend,
                'score': None,
                'label': None,
                'confidence': None
            }

        if self.backend != 'local':
            return {
                'status': 'unsupported_backend',
                'backend': self.backend,
                'score': None,
                'label': None,
                'confidence': None
            }

        if self._model is None:
            return {
                'status': 'model_unavailable',
                'backend': self.backend,
                'score': None,
                'label': None,
                'confidence': None
            }

        vector = self._build_feature_vector(features, classification)

        try:
            score, label, confidence = self._predict(vector)
        except Exception as exc:
            logger.warning("AI inference failed: %s", exc)
            return {
                'status': 'inference_failed',
                'backend': self.backend,
                'score': None,
                'label': None,
                'confidence': None
            }

        return {
            'status': 'ok',
            'backend': self.backend,
            'score': score,
            'label': label,
            'confidence': confidence
        }

    def _build_feature_vector(
        self,
        features: Dict[str, Any],
        classification: Dict[str, str]
    ) -> Dict[str, Any]:
        """Build a minimal feature vector for local models."""
        strings = features.get('strings', {})
        return {
            'file_size': features.get('file_size', 0),
            'entropy': features.get('entropy', 0.0),
            'suspicious_strings': strings.get('suspicious_count', 0),
            'is_hidden': 1 if features.get('is_hidden', False) else 0,
            'category': classification.get('category', 'unknown'),
            'extension': features.get('extension', 'none')
        }

    def _predict(self, vector: Dict[str, Any]) -> tuple:
        """
        Run prediction using the loaded model.

        Returns:
            (score, label, confidence)
        """
        if hasattr(self._model, 'predict_proba'):
            proba = self._model.predict_proba([vector])[0]
            confidence = max(proba)
            label_idx = int(proba.argmax())
            label = str(self._model.classes_[label_idx])
            score = round(confidence * 100, 2)
        else:
            label = str(self._model.predict([vector])[0])
            confidence = None
            score = 0.0

        return score, label, confidence
