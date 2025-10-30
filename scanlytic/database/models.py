"""
Database models for Scanlytic-ForensicAI.

This module defines the ORM models for storing file analysis results.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import relationship

from scanlytic.database.base import Base


class AnalysisRun(Base):
    """
    Model for analysis run/session.

    Represents a single analysis session which may include multiple files.
    """

    __tablename__ = 'analysis_runs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), default='running', nullable=False)
    total_files = Column(Integer, default=0)
    config = Column(JSON, nullable=True)

    # Relationships
    files = relationship('File', back_populates='analysis_run')

    def __repr__(self):
        return f"<AnalysisRun(id={self.id}, name={self.name})>"


class File(Base):
    """
    Model for analyzed files.

    Stores file metadata and links to analysis results.
    """

    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    analysis_run_id = Column(
        Integer,
        ForeignKey('analysis_runs.id'),
        nullable=True
    )
    file_path = Column(String(1024), nullable=False)
    file_name = Column(String(255), nullable=False, index=True)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(100), nullable=True)
    md5 = Column(String(32), nullable=True, index=True)
    sha1 = Column(String(40), nullable=True, index=True)
    sha256 = Column(String(64), nullable=True, index=True)
    analyzed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    analysis_run = relationship('AnalysisRun', back_populates='files')
    classification = relationship(
        'Classification',
        back_populates='file',
        uselist=False
    )
    score = relationship('Score', back_populates='file', uselist=False)
    features = relationship('Feature', back_populates='file')

    def __repr__(self):
        return f"<File(id={self.id}, name={self.file_name})>"


class Classification(Base):
    """
    Model for file classification results.

    Stores the classification category and confidence for each file.
    """

    __tablename__ = 'classifications'

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(
        Integer,
        ForeignKey('files.id'),
        nullable=False,
        unique=True
    )
    category = Column(String(100), nullable=False, index=True)
    file_type = Column(String(100), nullable=True)
    mime_type = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=True)
    classified_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    file = relationship('File', back_populates='classification')

    def __repr__(self):
        return f"<Classification(id={self.id}, category={self.category})>"


class Score(Base):
    """
    Model for malicious intent scores.

    Stores the calculated malicious score and risk level for each file.
    """

    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(
        Integer,
        ForeignKey('files.id'),
        nullable=False,
        unique=True
    )
    score = Column(Float, nullable=False, index=True)
    risk_level = Column(String(50), nullable=False, index=True)
    explanation = Column(JSON, nullable=True)
    scored_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    file = relationship('File', back_populates='score')

    def __repr__(self):
        return f"<Score(id={self.id}, score={self.score})>"


class Feature(Base):
    """
    Model for extracted features.

    Stores individual features extracted from files.
    """

    __tablename__ = 'features'

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey('files.id'), nullable=False)
    feature_name = Column(String(100), nullable=False, index=True)
    feature_value = Column(Text, nullable=True)
    feature_type = Column(String(50), nullable=True)
    extracted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    file = relationship('File', back_populates='features')

    def __repr__(self):
        return f"<Feature(id={self.id}, name={self.feature_name})>"
