"""
Main forensic analyzer for Scanlytic-ForensicAI.

Orchestrates file analysis by coordinating classification, feature extraction,
and malicious intent scoring.
"""

from pathlib import Path
from typing import Dict, Any, Optional

from scanlytic.core.classifier import FileClassifier
from scanlytic.features.extractor import FeatureExtractor
from scanlytic.scoring.scorer import MaliciousScorer
from scanlytic.utils.config import Config
from scanlytic.utils.exceptions import FileAnalysisError
from scanlytic.utils.file_utils import validate_file_path
from scanlytic.utils.logger import get_logger

logger = get_logger()


class ForensicAnalyzer:
    """
    Main analyzer for forensic file analysis.

    Coordinates the analysis pipeline: classification -> feature extraction
    -> malicious intent scoring -> reporting.
    """

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the forensic analyzer.

        Args:
            config: Configuration object (uses defaults if not provided)
        """
        self.config = config or Config()

        # Initialize components
        self.classifier = FileClassifier()
        self.feature_extractor = FeatureExtractor(
            extract_strings=self.config.get('features.extract_strings', True),
            string_min_length=self.config.get(
                'features.string_min_length', 4
            ),
            calculate_entropy=self.config.get(
                'features.calculate_entropy', True
            )
        )
        self.scorer = MaliciousScorer(
            malicious_threshold=self.config.get(
                'scoring.malicious_threshold', 50
            ),
            high_risk_threshold=self.config.get(
                'scoring.high_risk_threshold', 75
            )
        )

        logger.info("Forensic analyzer initialized")

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Perform complete analysis on a single file.

        Args:
            file_path: Path to the file to analyze

        Returns:
            Dict[str, Any]: Complete analysis results

        Raises:
            FileAnalysisError: If analysis fails
        """
        try:
            logger.info(f"Starting analysis of {file_path}")

            # Validate file path
            path = validate_file_path(file_path)

            # Classify file
            classification = self.classifier.classify(str(path))
            logger.debug(f"Classification complete: {classification}")

            # Extract features
            features = self.feature_extractor.extract(str(path))
            logger.debug(f"Feature extraction complete")

            # Calculate malicious score
            scoring = self.scorer.score(features, classification)
            logger.debug(f"Scoring complete: {scoring['score']:.2f}")

            # Compile results
            result = {
                'file_path': str(path),
                'file_name': path.name,
                'classification': classification,
                'features': features,
                'scoring': scoring,
                'analysis_version': '0.1.0'
            }

            logger.info(
                f"Analysis complete for {path.name}: "
                f"Score={scoring['score']:.2f}, "
                f"Risk={scoring['risk_level']}"
            )

            return result

        except Exception as e:
            logger.error(f"Analysis failed for {file_path}: {str(e)}")
            raise FileAnalysisError(
                f"Failed to analyze file {file_path}: {str(e)}"
            )

    def analyze_directory(self, directory_path: str,
                          recursive: bool = False) -> Dict[str, Any]:
        """
        Analyze all files in a directory.

        Args:
            directory_path: Path to the directory
            recursive: Whether to recursively analyze subdirectories

        Returns:
            Dict[str, Any]: Aggregated analysis results

        Raises:
            FileAnalysisError: If directory analysis fails
        """
        try:
            dir_path = Path(directory_path)

            if not dir_path.exists():
                raise FileAnalysisError(
                    f"Directory does not exist: {directory_path}"
                )

            if not dir_path.is_dir():
                raise FileAnalysisError(
                    f"Path is not a directory: {directory_path}"
                )

            logger.info(
                f"Starting directory analysis: {directory_path} "
                f"(recursive={recursive})"
            )

            results = []
            errors = []

            # Get files to analyze
            if recursive:
                files = dir_path.rglob('*')
            else:
                files = dir_path.glob('*')

            # Analyze each file
            for file_path in files:
                if file_path.is_file():
                    try:
                        result = self.analyze_file(str(file_path))
                        results.append(result)
                    except Exception as e:
                        error_info = {
                            'file': str(file_path),
                            'error': str(e)
                        }
                        errors.append(error_info)
                        logger.warning(
                            f"Failed to analyze {file_path}: {str(e)}"
                        )

            # Compile summary
            summary = self._generate_summary(results)

            return {
                'directory': str(dir_path),
                'recursive': recursive,
                'total_files': len(results),
                'errors': len(errors),
                'summary': summary,
                'results': results,
                'error_details': errors
            }

        except Exception as e:
            logger.error(
                f"Directory analysis failed for {directory_path}: {str(e)}"
            )
            raise FileAnalysisError(
                f"Failed to analyze directory {directory_path}: {str(e)}"
            )

    def _generate_summary(self, results: list) -> Dict[str, Any]:
        """
        Generate summary statistics from analysis results.

        Args:
            results: List of analysis results

        Returns:
            Dict[str, Any]: Summary statistics
        """
        if not results:
            return {
                'total_files': 0,
                'risk_distribution': {},
                'category_distribution': {},
                'average_score': 0,
                'high_risk_files': 0
            }

        # Calculate statistics
        risk_distribution = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
        category_distribution = {}
        total_score = 0
        high_risk_count = 0

        for result in results:
            # Risk distribution
            risk_level = result['scoring']['risk_level']
            risk_distribution[risk_level] = \
                risk_distribution.get(risk_level, 0) + 1

            # Category distribution
            category = result['classification']['category']
            category_distribution[category] = \
                category_distribution.get(category, 0) + 1

            # Score statistics
            score = result['scoring']['score']
            total_score += score

            if result['scoring']['is_high_risk']:
                high_risk_count += 1

        avg_score = total_score / len(results) if results else 0

        return {
            'total_files': len(results),
            'risk_distribution': risk_distribution,
            'category_distribution': category_distribution,
            'average_score': round(avg_score, 2),
            'high_risk_files': high_risk_count
        }
