Quick Start Guide
=================

This guide will help you get started with Scanlytic-ForensicAI quickly.

Installation
------------

Prerequisites
~~~~~~~~~~~~~

* Python 3.8 or higher
* pip (Python package manager)
* 4GB RAM (8GB recommended)
* 2GB free disk space

From Source
~~~~~~~~~~~

.. code-block:: bash

    git clone https://github.com/rohteemie/Scanlytic-Forensic-AI.git
    cd Scanlytic-ForensicAI
    pip install -r requirements.txt
    pip install -r requirements-dev.txt  # Optional, for development
    pip install -e .

Verify Installation
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    scanlytic --version
    pytest tests/  # Run tests

Basic Usage
-----------

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

Analyze a single file:

.. code-block:: bash

    scanlytic analyze /path/to/file.exe

Analyze a directory:

.. code-block:: bash

    scanlytic analyze /path/to/directory --recursive

Generate a JSON report:

.. code-block:: bash

    scanlytic analyze file.exe -o report.json -f json

Python API
~~~~~~~~~~

.. code-block:: python

    from scanlytic.core.analyzer import ForensicAnalyzer

    # Initialize analyzer
    analyzer = ForensicAnalyzer()

    # Analyze file
    result = analyzer.analyze_file('/path/to/file.exe')

    # Print results
    print(f"File: {result['file_name']}")
    print(f"Type: {result['classification']['category']}")
    print(f"Score: {result['scoring']['score']:.2f}")
    print(f"Risk: {result['scoring']['risk_level']}")

Understanding Results
---------------------

Risk Levels
~~~~~~~~~~~

* **Low (0-25)**: Benign files with no suspicious indicators
* **Medium (25-50)**: Some suspicious characteristics, likely benign
* **High (50-75)**: Multiple suspicious indicators, investigate further
* **Critical (75-100)**: Strong malicious indicators, quarantine recommended

Scoring Factors
~~~~~~~~~~~~~~~

Files are scored based on:

* **Entropy** (20%): High entropy suggests encryption/packing
* **Suspicious Strings** (25%): Malicious keywords and patterns
* **File Type** (20%): Executables and scripts are riskier
* **File Size** (10%): Unusual sizes flagged
* **Extension Mismatch** (15%): Disguised file types
* **Hidden Attributes** (10%): Hidden files are suspicious

Next Steps
----------

* Read the :doc:`api/index` for detailed API documentation
* Learn about :doc:`database` for storing analysis results
* Check :doc:`security` for security best practices
* See :doc:`contributing` to contribute to the project
