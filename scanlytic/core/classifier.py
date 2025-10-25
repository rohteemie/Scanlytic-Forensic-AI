"""
File classifier for Scanlytic-ForensicAI.

Provides file type classification based on magic numbers, extensions,
and content analysis.
"""

import mimetypes
import os
from pathlib import Path
from typing import Dict, Optional

from scanlytic.utils.exceptions import ClassificationError
from scanlytic.utils.file_utils import safe_read_file, validate_file_path
from scanlytic.utils.logger import get_logger

logger = get_logger()


class FileClassifier:
    """
    Classifier for determining file types and categories.

    Uses magic numbers, MIME types, and file extensions to classify
    files into categories relevant for forensic analysis.
    """

    # File signatures (magic numbers) for common file types
    MAGIC_SIGNATURES = {
        # Executables
        b'MZ': 'executable',  # PE/DOS executable
        b'\x7fELF': 'executable',  # ELF executable
        b'\xcf\xfa\xed\xfe': 'executable',  # Mach-O (32-bit)
        b'\xfe\xed\xfa\xce': 'executable',  # Mach-O (32-bit, reverse)
        b'\xcf\xfa\xed\xfe': 'executable',  # Mach-O (64-bit)

        # Archives
        b'PK\x03\x04': 'archive',  # ZIP
        b'PK\x05\x06': 'archive',  # ZIP (empty)
        b'PK\x07\x08': 'archive',  # ZIP (spanned)
        b'Rar!\x1a\x07': 'archive',  # RAR
        b'\x1f\x8b': 'archive',  # GZIP
        b'BZh': 'archive',  # BZIP2
        b'7z\xbc\xaf\x27\x1c': 'archive',  # 7-Zip

        # Documents
        b'%PDF': 'document',  # PDF
        b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1': 'document',  # MS Office
        b'PK\x03\x04': 'document',  # Office Open XML (overlaps with ZIP)

        # Images
        b'\xff\xd8\xff': 'image',  # JPEG
        b'\x89PNG\r\n\x1a\n': 'image',  # PNG
        b'GIF87a': 'image',  # GIF87a
        b'GIF89a': 'image',  # GIF89a
        b'BM': 'image',  # BMP
        b'II*\x00': 'image',  # TIFF (little-endian)
        b'MM\x00*': 'image',  # TIFF (big-endian)

        # Scripts
        b'#!/': 'script',  # Shebang
    }

    # Extension to category mapping
    EXTENSION_CATEGORIES = {
        # Executables
        'exe': 'executable',
        'dll': 'executable',
        'so': 'executable',
        'dylib': 'executable',
        'com': 'executable',
        'bat': 'script',
        'cmd': 'script',
        'sh': 'script',
        'ps1': 'script',

        # Documents
        'pdf': 'document',
        'doc': 'document',
        'docx': 'document',
        'xls': 'document',
        'xlsx': 'document',
        'ppt': 'document',
        'pptx': 'document',
        'txt': 'document',
        'rtf': 'document',
        'odt': 'document',

        # Archives
        'zip': 'archive',
        'rar': 'archive',
        'tar': 'archive',
        'gz': 'archive',
        'bz2': 'archive',
        '7z': 'archive',
        'tgz': 'archive',

        # Images
        'jpg': 'image',
        'jpeg': 'image',
        'png': 'image',
        'gif': 'image',
        'bmp': 'image',
        'tiff': 'image',
        'ico': 'image',
        'svg': 'image',

        # Scripts
        'py': 'script',
        'js': 'script',
        'rb': 'script',
        'pl': 'script',
        'php': 'script',
        'vbs': 'script',

        # Media
        'mp3': 'media',
        'mp4': 'media',
        'avi': 'media',
        'mov': 'media',
        'wmv': 'media',
        'wav': 'media',
        'flac': 'media',
    }

    def __init__(self):
        """Initialize the file classifier."""
        mimetypes.init()

    def classify(self, file_path: str) -> Dict[str, str]:
        """
        Classify a file by type and category.

        Args:
            file_path: Path to the file to classify

        Returns:
            Dict[str, str]: Classification results with keys:
                - category: File category (executable, document, etc.)
                - file_type: Specific file type
                - mime_type: MIME type
                - extension: File extension

        Raises:
            ClassificationError: If classification fails
        """
        try:
            path = validate_file_path(file_path)

            # Get basic file info
            extension = path.suffix.lstrip('.').lower()
            mime_type, _ = mimetypes.guess_type(str(path))

            # Try magic number classification first
            category = self._classify_by_magic(path)

            # Fall back to extension-based classification
            if category == 'unknown':
                category = self._classify_by_extension(extension)

            # Determine specific file type
            file_type = self._determine_file_type(path, category, extension)

            result = {
                'category': category,
                'file_type': file_type,
                'mime_type': mime_type or 'unknown',
                'extension': extension or 'none'
            }

            logger.debug(f"Classified {path.name}: {result}")
            return result

        except Exception as e:
            logger.error(f"Classification failed for {file_path}: {str(e)}")
            raise ClassificationError(
                f"Failed to classify file {file_path}: {str(e)}"
            )

    def _classify_by_magic(self, path: Path) -> str:
        """
        Classify file by magic number.

        Args:
            path: Path to the file

        Returns:
            str: File category or 'unknown'
        """
        try:
            # Read first 16 bytes for magic number
            header = safe_read_file(path, max_size=16)

            for magic, category in self.MAGIC_SIGNATURES.items():
                if header.startswith(magic):
                    return category

        except Exception as e:
            logger.debug(f"Magic number detection failed: {str(e)}")

        return 'unknown'

    def _classify_by_extension(self, extension: str) -> str:
        """
        Classify file by extension.

        Args:
            extension: File extension (without dot)

        Returns:
            str: File category or 'unknown'
        """
        return self.EXTENSION_CATEGORIES.get(extension, 'unknown')

    def _determine_file_type(self, path: Path, category: str,
                             extension: str) -> str:
        """
        Determine specific file type.

        Args:
            path: Path to the file
            category: File category
            extension: File extension

        Returns:
            str: Specific file type description
        """
        if category == 'executable':
            return self._identify_executable_type(path)
        elif category == 'document':
            return f"{extension.upper()} document" if extension else "Document"
        elif category == 'archive':
            return f"{extension.upper()} archive" if extension else "Archive"
        elif category == 'image':
            return f"{extension.upper()} image" if extension else "Image"
        elif category == 'script':
            return f"{extension.upper()} script" if extension else "Script"
        elif category == 'media':
            return f"{extension.upper()} media" if extension else "Media"
        else:
            return "Unknown file type"

    def _identify_executable_type(self, path: Path) -> str:
        """
        Identify specific executable type.

        Args:
            path: Path to the executable

        Returns:
            str: Executable type description
        """
        try:
            header = safe_read_file(path, max_size=64)

            if header.startswith(b'MZ'):
                return "PE executable (Windows)"
            elif header.startswith(b'\x7fELF'):
                return "ELF executable (Linux/Unix)"
            elif header[0:4] in [b'\xcf\xfa\xed\xfe', b'\xfe\xed\xfa\xce']:
                return "Mach-O executable (macOS)"

        except Exception:
            pass

        return "Unknown executable"
