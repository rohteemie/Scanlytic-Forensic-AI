Security
========

Security is a top priority for Scanlytic-ForensicAI. This document outlines
security considerations and best practices.

Security Features
-----------------

Path Traversal Prevention
~~~~~~~~~~~~~~~~~~~~~~~~~

All file paths are validated and resolved to prevent path traversal attacks:

.. code-block:: python

    from scanlytic.utils.file_utils import validate_file_path

    # This will raise an exception for malicious paths
    validate_file_path("../../../../etc/passwd")

Input Validation
~~~~~~~~~~~~~~~~

All user inputs are sanitized and validated before processing.

File Size Limits
~~~~~~~~~~~~~~~~

Configurable file size limits prevent resource exhaustion:

.. code-block:: yaml

    analysis:
      max_file_size: 104857600  # 100MB

Safe File Handling
~~~~~~~~~~~~~~~~~~

* Files are never executed
* Read-only operations only
* Temporary files are securely cleaned up
* File permissions are validated

Cryptographic Hashes
~~~~~~~~~~~~~~~~~~~~

Multiple hash algorithms supported for file identification:

* MD5 (legacy compatibility only, not for security)
* SHA-1 (legacy compatibility only, not for security)
* SHA-256 (recommended for security purposes)

**Important:** MD5 and SHA-1 are cryptographically broken. They are included
only for compatibility with legacy forensic databases. Always use SHA-256
for security-critical operations.

GDPR Compliance
---------------

Data Minimization
~~~~~~~~~~~~~~~~~

* Only essential file metadata is collected
* No personal data is processed or stored
* Users have full control over data retention

Local Processing
~~~~~~~~~~~~~~~~

* All analysis is performed locally
* No data is sent to external services (unless explicitly configured)
* User has complete control over data

Data Portability
~~~~~~~~~~~~~~~~

* Standard export formats (JSON, CSV)
* Easy data migration and extraction
* No vendor lock-in

Reporting Security Issues
--------------------------

**DO NOT** open public issues for security vulnerabilities.

Instead:

1. Email security details privately (see GitHub security advisories)
2. Allow time for fixes before public disclosure
3. Follow responsible disclosure practices

Security Best Practices
-----------------------

For Users
~~~~~~~~~

1. Keep Scanlytic-ForensicAI updated
2. Use strong database passwords
3. Limit file analysis to trusted sources
4. Review analysis results before taking action
5. Maintain proper access controls

For Developers
~~~~~~~~~~~~~~

1. Validate all inputs
2. Follow secure coding practices
3. Keep dependencies updated
4. Run security scans (bandit, safety)
5. Review code for vulnerabilities

Security Scanning
-----------------

The CI/CD pipeline includes automated security scans:

.. code-block:: bash

    # Check for known vulnerabilities in dependencies
    safety check

    # Static security analysis
    bandit -r scanlytic/

Acknowledgments
---------------

We thank the security research community for their contributions to
making Scanlytic-ForensicAI more secure.
