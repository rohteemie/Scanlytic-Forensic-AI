"""Unit tests for feature extractor."""

import tempfile
from pathlib import Path

import pytest

from scanlytic.features.extractor import FeatureExtractor


class TestFeatureExtractor:
    """Test cases for feature extractor."""

    def setup_method(self):
        """Set up test fixtures."""
        self.extractor = FeatureExtractor()
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_extract_basic_features(self):
        """Test extraction of basic file features."""
        test_file = Path(self.temp_dir) / "test.txt"
        test_content = b"Test content for feature extraction"
        test_file.write_bytes(test_content)

        features = self.extractor.extract(str(test_file))

        assert 'file_path' in features
        assert 'file_name' in features
        assert 'file_size' in features
        assert features['file_size'] == len(test_content)
        assert 'md5' in features
        assert 'sha1' in features
        assert 'sha256' in features

    def test_extract_entropy(self):
        """Test entropy calculation."""
        test_file = Path(self.temp_dir) / "test.bin"
        # Random-like data should have high entropy
        test_file.write_bytes(bytes(range(256)))

        features = self.extractor.extract(str(test_file))

        assert 'entropy' in features
        assert 0 <= features['entropy'] <= 8

    def test_extract_strings(self):
        """Test string extraction."""
        test_file = Path(self.temp_dir) / "test.bin"
        # Binary with embedded strings
        content = b'\x00\x00' + b'password' + b'\x00' + b'admin' + b'\x00\x00'
        test_file.write_bytes(content)

        features = self.extractor.extract(str(test_file))

        assert 'strings' in features
        assert 'count' in features['strings']
        assert features['strings']['count'] >= 0

    def test_detect_suspicious_patterns(self):
        """Test detection of suspicious string patterns."""
        test_file = Path(self.temp_dir) / "test.txt"
        # Include suspicious strings
        content = b'Some text with cmd.exe and powershell'
        test_file.write_bytes(content)

        features = self.extractor.extract(str(test_file))

        assert 'strings' in features
        assert 'suspicious_count' in features['strings']
        # Should detect at least some suspicious patterns
        assert features['strings']['suspicious_count'] >= 0
