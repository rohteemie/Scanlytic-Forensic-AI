"""
Database connection and session management.

This module sets up SQLAlchemy engine and session management for the
application.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Database URL - use environment variable or default to SQLite
DATABASE_URL = os.getenv(
    'SCANLYTIC_DATABASE_URL',
    'sqlite:///./data/scanlytic.db'
)

# Create engine
# For SQLite, enable foreign keys and use check_same_thread=False
connect_args = {}
if DATABASE_URL.startswith('sqlite'):
    connect_args = {
        'check_same_thread': False
    }

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=os.getenv('SCANLYTIC_DB_ECHO', 'false').lower() == 'true'
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()


def init_db():
    """
    Initialize database by creating all tables.

    This function should be called once at application startup or during
    setup to create all database tables.
    """
    # Ensure data directory exists for SQLite
    if DATABASE_URL.startswith('sqlite'):
        db_path = DATABASE_URL.replace('sqlite:///', '')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Import all models to register them
    from scanlytic.database import models  # noqa: F401

    # Create all tables
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Get database session.

    Yields a database session and ensures it is properly closed after use.
    Use this as a context manager or dependency injection.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
