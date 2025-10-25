"""Unit tests for file utilities."""

import os
import tempfile
from pathlib import Path

import pytest

from scanlytic.utils.file_utils import (
    validate_file_path,
    get_file_size,
    compute_file_hash,
    compute_file_hashes,
    safe_read_file
)
from scanlytic.utils.exceptions import FileAccessError, InvalidFileError


class TestFileUtils:
    """Test cases for file utility functions."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create temporary test file
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.txt"
        self.test_content = b"This is test content for hashing.\n"
        self.test_file.write_bytes(self.test_content)

    def teardown_method(self):
        """Clean up test fixtures."""
        if self.test_file.exists():
            self.test_file.unlink()
        if Path(self.temp_dir).exists():
            os.rmdir(self.temp_dir)

    def test_validate_file_path_success(self):
        """Test successful file path validation."""
        result = validate_file_path(str(self.test_file))
        assert result.exists()
        assert result.is_file()

    def test_validate_file_path_not_exists(self):
        """Test validation of non-existent file."""
        with pytest.raises(FileAccessError):
            validate_file_path("/nonexistent/path/file.txt")

    def test_validate_file_path_is_directory(self):
        """Test validation fails for directory."""
        with pytest.raises(InvalidFileError):
            validate_file_path(self.temp_dir)

    def test_get_file_size(self):
        """Test file size retrieval."""
        size = get_file_size(self.test_file)
        assert size == len(self.test_content)

    def test_compute_file_hash_md5(self):
        """Test MD5 hash computation."""
        hash_value = compute_file_hash(self.test_file, 'md5')
        assert isinstance(hash_value, str)
        assert len(hash_value) == 32  # MD5 is 32 hex characters

    def test_compute_file_hash_sha256(self):
        """Test SHA256 hash computation."""
        hash_value = compute_file_hash(self.test_file, 'sha256')
        assert isinstance(hash_value, str)
        assert len(hash_value) == 64  # SHA256 is 64 hex characters

    def test_compute_file_hash_invalid_algorithm(self):
        """Test invalid hash algorithm."""
        with pytest.raises(ValueError):
            compute_file_hash(self.test_file, 'invalid')

    def test_compute_file_hashes(self):
        """Test computing multiple hashes."""
        hashes = compute_file_hashes(self.test_file)
        assert 'md5' in hashes
        assert 'sha1' in hashes
        assert 'sha256' in hashes
        assert len(hashes['md5']) == 32
        assert len(hashes['sha1']) == 40
        assert len(hashes['sha256']) == 64

    def test_safe_read_file(self):
        """Test safe file reading."""
        content = safe_read_file(self.test_file)
        assert content == self.test_content

    def test_safe_read_file_size_limit(self):
        """Test file reading with size limit."""
        with pytest.raises(InvalidFileError):
            safe_read_file(self.test_file, max_size=10)
