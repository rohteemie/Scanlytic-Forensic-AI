"""
CRUD operations for database models.

This module provides Create, Read, Update, Delete operations for all models.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from scanlytic.database.models import (
    File,
    Classification,
    Score,
    Feature,
    AnalysisRun
)


# AnalysisRun CRUD operations
def create_analysis_run(
    db: Session,
    name: Optional[str] = None,
    description: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None
) -> AnalysisRun:
    """
    Create a new analysis run.

    Args:
        db: Database session
        name: Optional name for the analysis run
        description: Optional description
        config: Optional configuration dictionary

    Returns:
        Created AnalysisRun object
    """
    analysis_run = AnalysisRun(
        name=name,
        description=description,
        config=config
    )
    db.add(analysis_run)
    db.commit()
    db.refresh(analysis_run)
    return analysis_run


def get_analysis_run(db: Session, run_id: int) -> Optional[AnalysisRun]:
    """
    Get analysis run by ID.

    Args:
        db: Database session
        run_id: Analysis run ID

    Returns:
        AnalysisRun object or None if not found
    """
    return db.query(AnalysisRun).filter(
        AnalysisRun.id == run_id
    ).first()


def update_analysis_run(
    db: Session,
    run_id: int,
    **kwargs
) -> Optional[AnalysisRun]:
    """
    Update analysis run.

    Args:
        db: Database session
        run_id: Analysis run ID
        **kwargs: Fields to update

    Returns:
        Updated AnalysisRun object or None if not found
    """
    analysis_run = get_analysis_run(db, run_id)
    if analysis_run:
        for key, value in kwargs.items():
            if hasattr(analysis_run, key):
                setattr(analysis_run, key, value)
        db.commit()
        db.refresh(analysis_run)
    return analysis_run


def complete_analysis_run(db: Session, run_id: int) -> Optional[AnalysisRun]:
    """
    Mark analysis run as completed.

    Args:
        db: Database session
        run_id: Analysis run ID

    Returns:
        Updated AnalysisRun object or None if not found
    """
    return update_analysis_run(
        db,
        run_id,
        status='completed',
        completed_at=datetime.utcnow()
    )


# File CRUD operations
def create_file(
    db: Session,
    file_path: str,
    file_name: str,
    file_size: int,
    file_type: Optional[str] = None,
    md5: Optional[str] = None,
    sha1: Optional[str] = None,
    sha256: Optional[str] = None,
    analysis_run_id: Optional[int] = None
) -> File:
    """
    Create a new file record.

    Args:
        db: Database session
        file_path: Path to the file
        file_name: Name of the file
        file_size: Size of the file in bytes
        file_type: Detected file type
        md5: MD5 hash
        sha1: SHA-1 hash
        sha256: SHA-256 hash
        analysis_run_id: Optional analysis run ID

    Returns:
        Created File object
    """
    file_obj = File(
        file_path=file_path,
        file_name=file_name,
        file_size=file_size,
        file_type=file_type,
        md5=md5,
        sha1=sha1,
        sha256=sha256,
        analysis_run_id=analysis_run_id
    )
    db.add(file_obj)
    db.commit()
    db.refresh(file_obj)
    return file_obj


def get_file(db: Session, file_id: int) -> Optional[File]:
    """
    Get file by ID.

    Args:
        db: Database session
        file_id: File ID

    Returns:
        File object or None if not found
    """
    return db.query(File).filter(File.id == file_id).first()


def get_file_by_hash(
    db: Session,
    hash_value: str,
    hash_type: str = 'sha256'
) -> Optional[File]:
    """
    Get file by hash.

    Args:
        db: Database session
        hash_value: Hash value to search for
        hash_type: Type of hash (md5, sha1, sha256)

    Returns:
        File object or None if not found
    """
    if hash_type == 'md5':
        return db.query(File).filter(File.md5 == hash_value).first()
    elif hash_type == 'sha1':
        return db.query(File).filter(File.sha1 == hash_value).first()
    else:  # sha256
        return db.query(File).filter(File.sha256 == hash_value).first()


def update_file(db: Session, file_id: int, **kwargs) -> Optional[File]:
    """
    Update file record.

    Args:
        db: Database session
        file_id: File ID
        **kwargs: Fields to update

    Returns:
        Updated File object or None if not found
    """
    file_obj = get_file(db, file_id)
    if file_obj:
        for key, value in kwargs.items():
            if hasattr(file_obj, key):
                setattr(file_obj, key, value)
        db.commit()
        db.refresh(file_obj)
    return file_obj


def delete_file(db: Session, file_id: int) -> bool:
    """
    Delete file record.

    Args:
        db: Database session
        file_id: File ID

    Returns:
        True if deleted, False if not found
    """
    file_obj = get_file(db, file_id)
    if file_obj:
        db.delete(file_obj)
        db.commit()
        return True
    return False


# Classification CRUD operations
def create_classification(
    db: Session,
    file_id: int,
    category: str,
    file_type: Optional[str] = None,
    mime_type: Optional[str] = None,
    confidence: Optional[float] = None
) -> Classification:
    """
    Create classification for a file.

    Args:
        db: Database session
        file_id: File ID
        category: Classification category
        file_type: File type
        mime_type: MIME type
        confidence: Classification confidence

    Returns:
        Created Classification object
    """
    classification = Classification(
        file_id=file_id,
        category=category,
        file_type=file_type,
        mime_type=mime_type,
        confidence=confidence
    )
    db.add(classification)
    db.commit()
    db.refresh(classification)
    return classification


def get_classification(
    db: Session,
    file_id: int
) -> Optional[Classification]:
    """
    Get classification for a file.

    Args:
        db: Database session
        file_id: File ID

    Returns:
        Classification object or None if not found
    """
    return db.query(Classification).filter(
        Classification.file_id == file_id
    ).first()


# Score CRUD operations
def create_score(
    db: Session,
    file_id: int,
    score: float,
    risk_level: str,
    explanation: Optional[Dict[str, Any]] = None
) -> Score:
    """
    Create score for a file.

    Args:
        db: Database session
        file_id: File ID
        score: Malicious score
        risk_level: Risk level
        explanation: Optional score explanation

    Returns:
        Created Score object
    """
    score_obj = Score(
        file_id=file_id,
        score=score,
        risk_level=risk_level,
        explanation=explanation
    )
    db.add(score_obj)
    db.commit()
    db.refresh(score_obj)
    return score_obj


def get_score(db: Session, file_id: int) -> Optional[Score]:
    """
    Get score for a file.

    Args:
        db: Database session
        file_id: File ID

    Returns:
        Score object or None if not found
    """
    return db.query(Score).filter(Score.file_id == file_id).first()


# Feature CRUD operations
def create_feature(
    db: Session,
    file_id: int,
    feature_name: str,
    feature_value: Optional[str] = None,
    feature_type: Optional[str] = None
) -> Feature:
    """
    Create feature for a file.

    Args:
        db: Database session
        file_id: File ID
        feature_name: Name of the feature
        feature_value: Value of the feature
        feature_type: Type of the feature

    Returns:
        Created Feature object
    """
    feature = Feature(
        file_id=file_id,
        feature_name=feature_name,
        feature_value=feature_value,
        feature_type=feature_type
    )
    db.add(feature)
    db.commit()
    db.refresh(feature)
    return feature


def get_features(db: Session, file_id: int) -> List[Feature]:
    """
    Get all features for a file.

    Args:
        db: Database session
        file_id: File ID

    Returns:
        List of Feature objects
    """
    return db.query(Feature).filter(Feature.file_id == file_id).all()


# Bulk operations
def create_analysis_with_files(
    db: Session,
    files_data: List[Dict[str, Any]],
    run_name: Optional[str] = None,
    run_description: Optional[str] = None
) -> AnalysisRun:
    """
    Create analysis run with multiple files.

    Args:
        db: Database session
        files_data: List of file data dictionaries
        run_name: Optional run name
        run_description: Optional run description

    Returns:
        Created AnalysisRun object with files
    """
    # Create analysis run
    analysis_run = create_analysis_run(
        db,
        name=run_name,
        description=run_description
    )

    # Create files
    for file_data in files_data:
        file_data['analysis_run_id'] = analysis_run.id
        create_file(db, **file_data)

    # Update total files count
    update_analysis_run(
        db,
        analysis_run.id,
        total_files=len(files_data)
    )

    return analysis_run
