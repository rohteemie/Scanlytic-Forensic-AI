"""Unit tests for malicious scorer."""

import pytest

from scanlytic.scoring.scorer import MaliciousScorer


class TestMaliciousScorer:
    """Test cases for malicious intent scorer."""

    def setup_method(self):
        """Set up test fixtures."""
        self.scorer = MaliciousScorer()

    def test_score_benign_file(self):
        """Test scoring of benign file."""
        features = {
            'file_size': 1024,
            'entropy': 4.5,
            'is_hidden': False,
            'extension': 'txt',
            'strings': {
                'count': 10,
                'suspicious_count': 0
            }
        }
        classification = {
            'category': 'document',
            'file_type': 'TXT document'
        }

        result = self.scorer.score(features, classification)

        assert 'score' in result
        assert 'risk_level' in result
        assert 0 <= result['score'] <= 100
        assert result['risk_level'] in ['low', 'medium', 'high', 'critical']
        # Benign file should have lower score
        assert result['score'] < 50

    def test_score_suspicious_file(self):
        """Test scoring of suspicious file."""
        features = {
            'file_size': 1024,
            'entropy': 7.8,  # High entropy
            'is_hidden': True,
            'extension': 'txt',
            'strings': {
                'count': 20,
                'suspicious_count': 5  # Suspicious strings
            }
        }
        classification = {
            'category': 'executable',  # Risky category
            'file_type': 'PE executable'
        }

        result = self.scorer.score(features, classification)

        assert result['score'] > 50
        assert result['is_malicious'] is True

    def test_score_extension_mismatch(self):
        """Test scoring with extension mismatch."""
        features = {
            'file_size': 2048,
            'entropy': 5.0,
            'is_hidden': False,
            'extension': 'txt',
            'strings': {
                'count': 5,
                'suspicious_count': 0
            }
        }
        classification = {
            'category': 'executable',  # Mismatch!
            'file_type': 'PE executable'
        }

        result = self.scorer.score(features, classification)

        # Extension mismatch should increase score significantly
        assert result['score'] > 25
        assert 'extension_mismatch' in result['factors']
        # Should detect the mismatch
        assert result['factors']['extension_mismatch'] > 0

    def test_risk_level_thresholds(self):
        """Test risk level determination."""
        test_cases = [
            (10, 'low'),
            (30, 'medium'),
            (60, 'high'),
            (85, 'critical')
        ]

        for score, expected_level in test_cases:
            level = self.scorer._determine_risk_level(score)
            assert level == expected_level

    def test_get_score_explanation(self):
        """Test score explanation generation."""
        scoring_result = {
            'score': 65.5,
            'risk_level': 'high',
            'factors': {
                'entropy': 80,
                'suspicious_strings': 40,
                'file_type': 60
            }
        }

        explanation = self.scorer.get_score_explanation(scoring_result)

        assert 'Malicious Intent Score' in explanation
        assert '65.5' in explanation
        assert 'high' in explanation.lower()
