"""
AI training utilities for Scanlytic-ForensicAI.

Provides baseline and CSV-driven model training helpers.
"""

from pathlib import Path
from typing import Tuple

import joblib
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def build_baseline_training_data() -> Tuple[list, list]:
    """Create a tiny synthetic dataset for the baseline model."""
    data = [
        {
            'file_size': 2048,
            'entropy': 3.2,
            'suspicious_strings': 0,
            'is_hidden': 0,
            'category': 'document',
            'extension': 'txt'
        },
        {
            'file_size': 102400,
            'entropy': 7.4,
            'suspicious_strings': 6,
            'is_hidden': 1,
            'category': 'executable',
            'extension': 'exe'
        },
        {
            'file_size': 5120,
            'entropy': 5.6,
            'suspicious_strings': 2,
            'is_hidden': 0,
            'category': 'script',
            'extension': 'ps1'
        },
        {
            'file_size': 4096,
            'entropy': 4.1,
            'suspicious_strings': 0,
            'is_hidden': 0,
            'category': 'image',
            'extension': 'jpg'
        },
        {
            'file_size': 20480,
            'entropy': 7.9,
            'suspicious_strings': 9,
            'is_hidden': 1,
            'category': 'archive',
            'extension': 'zip'
        }
    ]
    labels = ['benign', 'malicious', 'suspicious', 'benign', 'malicious']
    return data, labels


def train_baseline_model(output_path: str) -> Path:
    """Train and save a baseline model to the output path."""
    data, labels = build_baseline_training_data()
    pipeline = Pipeline([
        ('vectorizer', DictVectorizer(sparse=False)),
        ('clf', LogisticRegression(max_iter=500))
    ])
    pipeline.fit(data, labels)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, output)
    return output


def train_from_csv(csv_path: str, label_column: str,
                   output_path: str) -> Path:
    """Train a model from a CSV dataset and save it to the output path."""
    data_frame = pd.read_csv(csv_path)

    if label_column not in data_frame.columns:
        raise ValueError(
            f"Label column '{label_column}' not found in dataset"
        )

    labels = data_frame[label_column].astype(str).tolist()
    features = data_frame.drop(columns=[label_column]).to_dict(
        orient='records'
    )

    pipeline = Pipeline([
        ('vectorizer', DictVectorizer(sparse=False)),
        ('clf', LogisticRegression(max_iter=500))
    ])
    pipeline.fit(features, labels)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, output)
    return output