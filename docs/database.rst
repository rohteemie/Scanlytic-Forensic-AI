Database Layer
==============

Scanlytic-ForensicAI uses SQLAlchemy for database persistence of analysis results.

Configuration
-------------

By default, Scanlytic uses SQLite with the database stored at ``data/scanlytic.db``.

You can configure a different database using the environment variable:

.. code-block:: bash

    export SCANLYTIC_DATABASE_URL="postgresql://user:pass@localhost/scanlytic"

Database Models
---------------

.. automodule:: scanlytic.database.models
   :members:
   :undoc-members:
   :show-inheritance:

CRUD Operations
---------------

.. automodule:: scanlytic.database.crud
   :members:
   :undoc-members:
   :show-inheritance:

Database Setup
--------------

Initialize Database
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from scanlytic.database.base import init_db

    # Create all tables
    init_db()

Run Migrations
~~~~~~~~~~~~~~

.. code-block:: bash

    # Apply migrations
    alembic upgrade head

    # Create new migration
    alembic revision --autogenerate -m "Description"

Using the Database
------------------

Basic Example
~~~~~~~~~~~~~

.. code-block:: python

    from scanlytic.database.base import SessionLocal
    from scanlytic.database import crud

    # Create session
    db = SessionLocal()

    try:
        # Create file record
        file_obj = crud.create_file(
            db,
            file_path="/path/to/file.exe",
            file_name="file.exe",
            file_size=1024,
            sha256="abc123..."
        )

        # Create classification
        classification = crud.create_classification(
            db,
            file_id=file_obj.id,
            category="executable",
            confidence=0.95
        )

        # Create score
        score = crud.create_score(
            db,
            file_id=file_obj.id,
            score=75.5,
            risk_level="high"
        )

    finally:
        db.close()

Schema Overview
---------------

The database consists of the following tables:

**analysis_runs**
    Stores information about analysis sessions

**files**
    Stores file metadata and hashes

**classifications**
    Stores file classification results

**scores**
    Stores malicious intent scores

**features**
    Stores extracted features from files
