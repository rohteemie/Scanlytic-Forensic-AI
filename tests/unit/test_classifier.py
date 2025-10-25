"""Unit tests for file classifier."""

import tempfile
from pathlib import Path

import pytest

from scanlytic.core.classifier import FileClassifier


class TestFileClassifier:
    """Test cases for file classifier."""

    def setup_method(self):
        """Set up test fixtures."""
        self.classifier = FileClassifier()
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_classify_text_file(self):
        """Test classification of text file."""
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Hello, world!")

        result = self.classifier.classify(str(test_file))
        assert result['extension'] == 'txt'
        assert result['category'] == 'document'

    def test_classify_executable_by_magic(self):
        """Test classification of PE executable by magic number."""
        test_file = Path(self.temp_dir) / "test.exe"
        # Write PE magic number with more complete header
        test_file.write_bytes(b'MZ' + b'\x90\x00' + b'\x00' * 60 +
                              b'\x00\x00\x00\x00' + b'PE\x00\x00')

        result = self.classifier.classify(str(test_file))
        assert result['category'] == 'executable'
        # Check that it's identified as executable
        assert 'executable' in result['file_type'].lower()

    def test_classify_pdf_file(self):
        """Test classification of PDF file."""
        test_file = Path(self.temp_dir) / "test.pdf"
        # Write PDF magic number
        test_file.write_bytes(b'%PDF-1.4\n' + b'test content')

        result = self.classifier.classify(str(test_file))
        assert result['extension'] == 'pdf'
        assert result['category'] == 'document'

    def test_classify_unknown_file(self):
        """Test classification of unknown file type."""
        test_file = Path(self.temp_dir) / "test.xyz"
        test_file.write_bytes(b'random binary data')

        result = self.classifier.classify(str(test_file))
        assert result['extension'] == 'xyz'
        # Should fall back to unknown
        assert result['category'] in ['unknown']
