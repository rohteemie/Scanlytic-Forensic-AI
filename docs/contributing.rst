Contributing to Scanlytic-ForensicAI
=====================================

We welcome contributions! This guide will help you get started.

Development Setup
-----------------

1. Fork the repository on GitHub
2. Clone your fork locally:

.. code-block:: bash

    git clone https://github.com/YOUR_USERNAME/Scanlytic-Forensic-AI.git
    cd Scanlytic-Forensic-AI

3. Install development dependencies:

.. code-block:: bash

    pip install -r requirements-dev.txt

4. Create a feature branch:

.. code-block:: bash

    git checkout -b feature/your-feature-name

Coding Standards
----------------

* Follow PEP 8 style guide
* Maximum line length: 79 characters
* Use Google-style docstrings
* Add type hints where appropriate
* Write tests for new features

Running Tests
-------------

.. code-block:: bash

    # Run all tests
    pytest tests/

    # Run with coverage
    pytest tests/ --cov=scanlytic --cov-report=html

    # Run specific test file
    pytest tests/unit/test_classifier.py

Code Quality Checks
-------------------

.. code-block:: bash

    # Check code style
    pycodestyle scanlytic/ tests/ --max-line-length=79

    # Type checking (if implemented)
    mypy scanlytic/

Submitting Changes
------------------

1. Ensure all tests pass
2. Update documentation if needed
3. Commit your changes:

.. code-block:: bash

    git add .
    git commit -m "Add: brief description of changes"

4. Push to your fork:

.. code-block:: bash

    git push origin feature/your-feature-name

5. Create a Pull Request on GitHub

Pull Request Guidelines
------------------------

* Provide a clear description of the changes
* Reference any related issues
* Ensure CI checks pass
* Update documentation as needed
* Add tests for new features
* Keep PRs focused and atomic

Code of Conduct
---------------

Please be respectful and professional in all interactions. We aim to maintain
a welcoming and inclusive community.
