"""
Feature extractor for Scanlytic-ForensicAI.

Extracts various features from files for analysis and scoring,
including file properties, entropy, hashes, and metadata.
"""

import math
import os
import string
import time
from collections import Counter
from pathlib import Path
from typing import Dict, Any, Optional

from scanlytic.utils.exceptions import FeatureExtractionError
from scanlytic.utils.file_utils import (
    compute_file_hashes,
    get_file_size,
    safe_read_file,
    validate_file_path
)
from scanlytic.utils.logger import get_logger

logger = get_logger()


class FeatureExtractor:
    """
    Extracts features from files for forensic analysis.

    Features include file properties, entropy, hashes, strings,
    and metadata relevant for malicious intent scoring.
    """

    def __init__(self, extract_strings: bool = True,
                 string_min_length: int = 4,
                 calculate_entropy: bool = True):
        """
        Initialize feature extractor.

        Args:
            extract_strings: Whether to extract strings from files
            string_min_length: Minimum length for extracted strings
            calculate_entropy: Whether to calculate file entropy
        """
        self.extract_strings = extract_strings
        self.string_min_length = string_min_length
        self.calculate_entropy = calculate_entropy

    def extract(self, file_path: str) -> Dict[str, Any]:
        """
        Extract all features from a file.

        Args:
            file_path: Path to the file

        Returns:
            Dict[str, Any]: Extracted features

        Raises:
            FeatureExtractionError: If feature extraction fails
        """
        try:
            path = validate_file_path(file_path)

            features = {
                'file_path': str(path),
                'file_name': path.name,
                **self._extract_static_properties(path),
                **self._extract_hashes(path)
            }

            if self.calculate_entropy:
                features['entropy'] = self._calculate_entropy(path)

            if self.extract_strings:
                features['strings'] = self._extract_strings(path)

            logger.debug(f"Extracted features from {path.name}")
            return features

        except Exception as e:
            logger.error(
                f"Feature extraction failed for {file_path}: {str(e)}"
            )
            raise FeatureExtractionError(
                f"Failed to extract features from {file_path}: {str(e)}"
            )

    def _extract_static_properties(self, path: Path) -> Dict[str, Any]:
        """
        Extract static file properties.

        Args:
            path: Path to the file

        Returns:
            Dict[str, Any]: Static properties
        """
        try:
            stat = path.stat()

            return {
                'file_size': stat.st_size,
                'created_time': time.ctime(stat.st_ctime),
                'modified_time': time.ctime(stat.st_mtime),
                'accessed_time': time.ctime(stat.st_atime),
                'permissions': oct(stat.st_mode),
                'is_hidden': path.name.startswith('.'),
                'extension': path.suffix.lstrip('.').lower() or 'none'
            }

        except Exception as e:
            logger.warning(f"Could not extract static properties: {str(e)}")
            return {
                'file_size': 0,
                'created_time': 'unknown',
                'modified_time': 'unknown',
                'accessed_time': 'unknown',
                'permissions': 'unknown',
                'is_hidden': False,
                'extension': 'none'
            }

    def _extract_hashes(self, path: Path) -> Dict[str, str]:
        """
        Extract file hashes.

        Args:
            path: Path to the file

        Returns:
            Dict[str, str]: Hash values
        """
        try:
            hashes = compute_file_hashes(path)
            return {
                'md5': hashes['md5'],
                'sha1': hashes['sha1'],
                'sha256': hashes['sha256']
            }

        except Exception as e:
            logger.warning(f"Could not compute hashes: {str(e)}")
            return {
                'md5': 'error',
                'sha1': 'error',
                'sha256': 'error'
            }

    def _calculate_entropy(self, path: Path) -> float:
        """
        Calculate Shannon entropy of file contents.

        Args:
            path: Path to the file

        Returns:
            float: Entropy value (0-8)
        """
        try:
            # Limit to first 1MB for performance
            max_size = 1024 * 1024
            file_size = get_file_size(path)
            read_size = min(file_size, max_size)

            data = safe_read_file(path, max_size=read_size)

            if not data:
                return 0.0

            # Calculate byte frequency
            byte_counts = Counter(data)
            entropy = 0.0

            for count in byte_counts.values():
                probability = count / len(data)
                entropy -= probability * math.log2(probability)

            return round(entropy, 3)

        except Exception as e:
            logger.warning(f"Could not calculate entropy: {str(e)}")
            return 0.0

    def _extract_strings(self, path: Path,
                         max_strings: int = 100) -> Dict[str, Any]:
        """
        Extract printable strings from file.

        Args:
            path: Path to the file
            max_strings: Maximum number of strings to return

        Returns:
            Dict[str, Any]: Extracted strings and statistics
        """
        try:
            # Limit to first 1MB for performance
            max_size = 1024 * 1024
            file_size = get_file_size(path)
            read_size = min(file_size, max_size)

            data = safe_read_file(path, max_size=read_size)

            # Extract printable ASCII strings
            printable = set(string.printable.encode())
            strings_found = []
            current_string = b''

            for byte in data:
                if bytes([byte]) in printable:
                    current_string += bytes([byte])
                else:
                    if len(current_string) >= self.string_min_length:
                        try:
                            strings_found.append(
                                current_string.decode('ascii')
                            )
                        except UnicodeDecodeError:
                            pass
                    current_string = b''

            # Add last string if any
            if len(current_string) >= self.string_min_length:
                try:
                    strings_found.append(current_string.decode('ascii'))
                except UnicodeDecodeError:
                    pass

            # Limit number of strings
            strings_found = strings_found[:max_strings]

            # Detect suspicious patterns
            suspicious_patterns = self._detect_suspicious_patterns(
                strings_found
            )

            return {
                'count': len(strings_found),
                'samples': strings_found[:10],  # First 10 for report
                'suspicious_count': len(suspicious_patterns),
                'suspicious_patterns': suspicious_patterns
            }

        except Exception as e:
            logger.warning(f"Could not extract strings: {str(e)}")
            return {
                'count': 0,
                'samples': [],
                'suspicious_count': 0,
                'suspicious_patterns': []
            }

    def _detect_suspicious_patterns(self, strings: list) -> list:
        """
        Detect suspicious string patterns.

        Args:
            strings: List of extracted strings

        Returns:
            list: List of suspicious strings
        """
        suspicious = []
        patterns = [
            'cmd.exe', 'powershell', 'sh', 'bash',
            'http://', 'https://',
            'registry', 'regedit',
            'download', 'upload',
            'keylog', 'password', 'credential',
            'encrypt', 'decrypt',
            'admin', 'root',
            'backdoor', 'trojan', 'virus'
        ]

        for s in strings:
            s_lower = s.lower()
            for pattern in patterns:
                if pattern in s_lower:
                    suspicious.append(s)
                    break

        return suspicious[:20]  # Limit to 20 suspicious strings
