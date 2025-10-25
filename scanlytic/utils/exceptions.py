"""
Custom exceptions for Scanlytic-ForensicAI.

Provides a hierarchy of exceptions for different error scenarios
with clear, actionable error messages.
"""


class ScanalyticError(Exception):
    """Base exception for all Scanlytic errors."""

    pass


class FileAnalysisError(ScanalyticError):
    """Raised when file analysis fails."""

    pass


class FileAccessError(ScanalyticError):
    """Raised when file cannot be accessed or read."""

    pass


class InvalidFileError(ScanalyticError):
    """Raised when file is invalid or corrupted."""

    pass


class ClassificationError(ScanalyticError):
    """Raised when file classification fails."""

    pass


class FeatureExtractionError(ScanalyticError):
    """Raised when feature extraction fails."""

    pass


class ScoringError(ScanalyticError):
    """Raised when malicious intent scoring fails."""

    pass


class ConfigurationError(ScanalyticError):
    """Raised when configuration is invalid."""

    pass


class ReportGenerationError(ScanalyticError):
    """Raised when report generation fails."""

    pass
