"""
Database module for Scanlytic-ForensicAI.

This module provides database connectivity and ORM setup for persistent
storage of analysis results.
"""

from scanlytic.database.base import Base, SessionLocal, engine
from scanlytic.database.models import (
    File,
    Classification,
    Score,
    Feature,
    AnalysisRun
)
from scanlytic.database.crud import (
    create_file,
    get_file,
    update_file,
    delete_file,
    create_analysis_run,
    get_analysis_run
)

__all__ = [
    'Base',
    'SessionLocal',
    'engine',
    'File',
    'Classification',
    'Score',
    'Feature',
    'AnalysisRun',
    'create_file',
    'get_file',
    'update_file',
    'delete_file',
    'create_analysis_run',
    'get_analysis_run'
]
