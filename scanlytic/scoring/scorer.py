"""
Malicious intent scorer for Scanlytic-ForensicAI.

Calculates a risk score (0-100) based on file features, classification,
and behavioral indicators.
"""

from typing import Dict, Any

from scanlytic.utils.exceptions import ScoringError
from scanlytic.utils.logger import get_logger

logger = get_logger()


class MaliciousScorer:
    """
    Calculates malicious intent score for files.

    Uses a rule-based scoring system that considers multiple factors
    including file type, entropy, suspicious patterns, and metadata.
    """

    # Scoring weights for different factors
    WEIGHTS = {
        'entropy': 20,
        'suspicious_strings': 25,
        'file_type': 20,
        'file_size': 10,
        'extension_mismatch': 15,
        'hidden_file': 10
    }

    # Risk level thresholds
    RISK_LEVELS = {
        'low': (0, 25),
        'medium': (25, 50),
        'high': (50, 75),
        'critical': (75, 100)
    }

    def __init__(self, malicious_threshold: int = 50,
                 high_risk_threshold: int = 75):
        """
        Initialize the malicious scorer.

        Args:
            malicious_threshold: Threshold for malicious classification
            high_risk_threshold: Threshold for high-risk classification
        """
        self.malicious_threshold = malicious_threshold
        self.high_risk_threshold = high_risk_threshold

    def score(self, features: Dict[str, Any],
              classification: Dict[str, str]) -> Dict[str, Any]:
        """
        Calculate malicious intent score for a file.

        Args:
            features: Extracted file features
            classification: File classification results

        Returns:
            Dict[str, Any]: Scoring results with keys:
                - score: Malicious intent score (0-100)
                - risk_level: Risk level (low, medium, high, critical)
                - factors: Contributing factors and their scores
                - is_malicious: Boolean flag if above threshold

        Raises:
            ScoringError: If scoring fails
        """
        try:
            scores = {}

            # Score entropy (high entropy suggests encryption/packing)
            scores['entropy'] = self._score_entropy(features.get('entropy', 0))

            # Score suspicious strings
            scores['suspicious_strings'] = self._score_suspicious_strings(
                features.get('strings', {})
            )

            # Score file type
            scores['file_type'] = self._score_file_type(
                classification.get('category', 'unknown')
            )

            # Score file size
            scores['file_size'] = self._score_file_size(
                features.get('file_size', 0)
            )

            # Score extension mismatch
            scores['extension_mismatch'] = self._score_extension_mismatch(
                features, classification
            )

            # Score hidden file
            scores['hidden_file'] = self._score_hidden_file(
                features.get('is_hidden', False)
            )

            # Calculate weighted total score
            total_score = self._calculate_total_score(scores)

            # Determine risk level
            risk_level = self._determine_risk_level(total_score)

            result = {
                'score': round(total_score, 2),
                'risk_level': risk_level,
                'factors': scores,
                'is_malicious': total_score >= self.malicious_threshold,
                'is_high_risk': total_score >= self.high_risk_threshold
            }

            logger.debug(
                f"Calculated score {total_score:.2f} "
                f"(risk: {risk_level})"
            )
            return result

        except Exception as e:
            logger.error(f"Scoring failed: {str(e)}")
            raise ScoringError(f"Failed to calculate score: {str(e)}")

    def _score_entropy(self, entropy: float) -> float:
        """
        Score based on file entropy.

        Args:
            entropy: File entropy (0-8)

        Returns:
            float: Entropy score (0-100)
        """
        # High entropy (>7.0) suggests encryption/packing
        if entropy > 7.5:
            return 100
        elif entropy > 7.0:
            return 80
        elif entropy > 6.5:
            return 60
        elif entropy > 6.0:
            return 40
        elif entropy > 5.5:
            return 20
        else:
            return 0

    def _score_suspicious_strings(self, strings_data: Dict) -> float:
        """
        Score based on suspicious strings found.

        Args:
            strings_data: String extraction results

        Returns:
            float: Suspicious strings score (0-100)
        """
        suspicious_count = strings_data.get('suspicious_count', 0)

        if suspicious_count >= 10:
            return 100
        elif suspicious_count >= 7:
            return 80
        elif suspicious_count >= 5:
            return 60
        elif suspicious_count >= 3:
            return 40
        elif suspicious_count >= 1:
            return 20
        else:
            return 0

    def _score_file_type(self, category: str) -> float:
        """
        Score based on file type category.

        Args:
            category: File category

        Returns:
            float: File type score (0-100)
        """
        # Executables and scripts are inherently riskier
        risk_scores = {
            'executable': 60,
            'script': 50,
            'document': 30,  # Can contain macros
            'archive': 40,  # Can contain malware
            'image': 10,
            'media': 10,
            'unknown': 20
        }

        return risk_scores.get(category, 20)

    def _score_file_size(self, size: int) -> float:
        """
        Score based on file size.

        Args:
            size: File size in bytes

        Returns:
            float: File size score (0-100)
        """
        # Very small executables can be suspicious
        # Very large files might be data dumps
        if size < 1024:  # < 1KB
            return 30
        elif size < 10240:  # < 10KB
            return 20
        elif size > 100 * 1024 * 1024:  # > 100MB
            return 30
        else:
            return 0

    def _score_extension_mismatch(self, features: Dict,
                                  classification: Dict) -> float:
        """
        Score based on extension/type mismatch.

        Args:
            features: File features
            classification: Classification results

        Returns:
            float: Extension mismatch score (0-100)
        """
        extension = features.get('extension', 'none')
        category = classification.get('category', 'unknown')

        # Check for common mismatches
        if extension == 'txt' and category == 'executable':
            return 100
        elif extension == 'jpg' and category == 'executable':
            return 100
        elif extension == 'pdf' and category == 'executable':
            return 100
        elif extension in ['doc', 'docx', 'xls', 'xlsx'] and \
                category == 'executable':
            return 80
        elif extension == 'none' and category == 'executable':
            return 60

        return 0

    def _score_hidden_file(self, is_hidden: bool) -> float:
        """
        Score based on hidden file attribute.

        Args:
            is_hidden: Whether file is hidden

        Returns:
            float: Hidden file score (0-100)
        """
        return 40 if is_hidden else 0

    def _calculate_total_score(self, scores: Dict[str, float]) -> float:
        """
        Calculate weighted total score.

        Args:
            scores: Individual factor scores

        Returns:
            float: Total weighted score (0-100)
        """
        total = 0
        total_weight = 0

        for factor, score in scores.items():
            weight = self.WEIGHTS.get(factor, 0)
            total += score * (weight / 100)
            total_weight += weight

        if total_weight == 0:
            return 0

        # Normalize to 0-100 range
        normalized_score = (total / total_weight) * 100
        return min(100, max(0, normalized_score))

    def _determine_risk_level(self, score: float) -> str:
        """
        Determine risk level from score.

        Args:
            score: Malicious intent score

        Returns:
            str: Risk level
        """
        for level, (min_score, max_score) in self.RISK_LEVELS.items():
            if min_score <= score < max_score:
                return level

        return 'critical'  # >= 75

    def get_score_explanation(self, scoring_result: Dict[str, Any]) -> str:
        """
        Generate human-readable explanation of score.

        Args:
            scoring_result: Scoring results

        Returns:
            str: Score explanation
        """
        score = scoring_result['score']
        risk_level = scoring_result['risk_level']
        factors = scoring_result['factors']

        explanation = f"Malicious Intent Score: {score:.2f}/100\n"
        explanation += f"Risk Level: {risk_level.upper()}\n\n"
        explanation += "Contributing Factors:\n"

        for factor, factor_score in factors.items():
            weight = self.WEIGHTS.get(factor, 0)
            if factor_score > 0:
                explanation += (
                    f"  - {factor.replace('_', ' ').title()}: "
                    f"{factor_score:.1f} (weight: {weight}%)\n"
                )

        return explanation
