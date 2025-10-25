"""
Logging configuration and utilities for Scanlytic-ForensicAI.

Provides structured logging with configurable levels and output formats,
ensuring proper audit trail for forensic analysis.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


class ScanalyticLogger:
    """
    Centralized logger for Scanlytic-ForensicAI.

    Provides structured logging with security and privacy considerations
    for forensic analysis workflows.
    """

    _instance = None

    def __new__(cls):
        """Implement singleton pattern for logger."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize logger if not already initialized."""
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.logger = logging.getLogger('scanlytic')
            self._setup_logger()

    def _setup_logger(self, level: str = 'INFO',
                      log_file: Optional[Path] = None) -> None:
        """
        Configure the logger with handlers and formatters.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional path to log file
        """
        self.logger.setLevel(getattr(logging, level.upper()))

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

        # File handler if log file specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - '
                '%(filename)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """
        Get the configured logger instance.

        Returns:
            logging.Logger: Configured logger
        """
        return self.logger


def get_logger() -> logging.Logger:
    """
    Get the Scanlytic logger instance.

    Returns:
        logging.Logger: Configured logger instance
    """
    return ScanalyticLogger().get_logger()
