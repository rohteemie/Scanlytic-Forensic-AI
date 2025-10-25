"""
Scanlytic-ForensicAI: Automated File Classification and Malicious Intent
Scoring for Digital Forensic Triage.

This package provides tools for analyzing files and scoring their potential
malicious intent to aid in digital forensic investigations.

Copyright (c) 2025 Rotimi Owolabi
Licensed under the MIT License
"""

__version__ = "0.1.0"
__author__ = "Rotimi Owolabi"
__license__ = "MIT"

from scanlytic.core.analyzer import ForensicAnalyzer
from scanlytic.core.classifier import FileClassifier
from scanlytic.features.extractor import FeatureExtractor
from scanlytic.scoring.scorer import MaliciousScorer

__all__ = [
    'ForensicAnalyzer',
    'FileClassifier',
    'FeatureExtractor',
    'MaliciousScorer',
]
