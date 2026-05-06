Scanlytic Forensic AI Documentation
=====================================

Scanlytic Forensic AI is an open-source forensic triage system that classifies
files and scores malicious intent for rapid investigations.

AI Quickstart
-------------

Enable optional local AI scoring and train a model in minutes.

Train a baseline model:

.. code-block:: bash

   python -m scanlytic train-ai --baseline --output models/ai_baseline.joblib

Analyze with AI enabled:

.. code-block:: bash

   python -m scanlytic analyze /path/to/files \
     --ai-enabled \
     --ai-model models/ai_baseline.joblib \
     --ai-weight 0.3

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   contributing
   database
   security

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
