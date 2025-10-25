"""
File handling utilities for Scanlytic-ForensicAI.

Provides secure file operations with validation and error handling.
"""

import hashlib
import os
from pathlib import Path
from typing import Dict, Optional

from scanlytic.utils.exceptions import FileAccessError, InvalidFileError
from scanlytic.utils.logger import get_logger

logger = get_logger()


def validate_file_path(file_path: str) -> Path:
    """
    Validate and normalize a file path.

    Args:
        file_path: Path to the file

    Returns:
        Path: Validated Path object

    Raises:
        FileAccessError: If file doesn't exist or is not accessible
        InvalidFileError: If path is a directory or invalid
    """
    try:
        path = Path(file_path).resolve()

        if not path.exists():
            raise FileAccessError(f"File does not exist: {file_path}")

        if not path.is_file():
            raise InvalidFileError(f"Path is not a file: {file_path}")

        if not os.access(path, os.R_OK):
            raise FileAccessError(f"File is not readable: {file_path}")

        return path

    except (OSError, PermissionError) as e:
        raise FileAccessError(f"Cannot access file {file_path}: {str(e)}")


def get_file_size(file_path: Path) -> int:
    """
    Get the size of a file in bytes.

    Args:
        file_path: Path to the file

    Returns:
        int: File size in bytes

    Raises:
        FileAccessError: If file size cannot be determined
    """
    try:
        return file_path.stat().st_size
    except OSError as e:
        raise FileAccessError(
            f"Cannot determine file size for {file_path}: {str(e)}"
        )


def compute_file_hash(file_path: Path, algorithm: str = 'sha256') -> str:
    """
    Compute hash of a file using specified algorithm.

    Note: MD5 and SHA-1 are cryptographically broken and included only for
    legacy compatibility and file identification in forensic contexts.
    Use SHA-256 or stronger algorithms for security-critical applications.

    Args:
        file_path: Path to the file
        algorithm: Hash algorithm (md5, sha1, sha256)

    Returns:
        str: Hexadecimal hash digest

    Raises:
        FileAccessError: If file cannot be read
        ValueError: If algorithm is not supported
    """
    supported_algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256
    }

    if algorithm not in supported_algorithms:
        raise ValueError(
            f"Unsupported hash algorithm: {algorithm}. "
            f"Supported: {', '.join(supported_algorithms.keys())}"
        )

    try:
        hash_obj = supported_algorithms[algorithm]()
        with open(file_path, 'rb') as f:
            # Read in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(8192), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()

    except OSError as e:
        raise FileAccessError(
            f"Cannot read file for hashing {file_path}: {str(e)}"
        )


def compute_file_hashes(file_path: Path) -> Dict[str, str]:
    """
    Compute multiple hashes for a file.

    Note: MD5 and SHA-1 are included for forensic file identification and
    legacy compatibility only. They are cryptographically broken.
    SHA-256 should be used for security verification.

    Args:
        file_path: Path to the file

    Returns:
        Dict[str, str]: Dictionary with hash algorithm as key and
                        hash digest as value
    """
    return {
        'md5': compute_file_hash(file_path, 'md5'),
        'sha1': compute_file_hash(file_path, 'sha1'),
        'sha256': compute_file_hash(file_path, 'sha256')
    }


def safe_read_file(file_path: Path, max_size: Optional[int] = None) -> bytes:
    """
    Safely read a file with size limits.

    Args:
        file_path: Path to the file
        max_size: Maximum file size in bytes (None for no limit)

    Returns:
        bytes: File contents

    Raises:
        FileAccessError: If file cannot be read
        InvalidFileError: If file exceeds size limit
    """
    try:
        file_size = get_file_size(file_path)

        if max_size and file_size > max_size:
            raise InvalidFileError(
                f"File size ({file_size} bytes) exceeds maximum "
                f"allowed size ({max_size} bytes)"
            )

        with open(file_path, 'rb') as f:
            return f.read()

    except OSError as e:
        raise FileAccessError(f"Cannot read file {file_path}: {str(e)}")
