"""
ELF (Executable and Linkable Format) file feature extractor.

Extracts features from Linux/Unix ELF files including headers, sections,
segments, and other ELF-specific metadata.
"""

from typing import Dict, Any, Optional, List
import os

from scanlytic.utils.logger import get_logger

logger = get_logger()

# Import elftools only when needed to avoid dependency issues
try:
    from elftools.elf.elffile import ELFFile
    from elftools.common.exceptions import ELFError
    ELFTOOLS_AVAILABLE = True
except ImportError:
    ELFTOOLS_AVAILABLE = False
    logger.warning("pyelftools library not available. ELF analysis disabled.")


class ELFExtractor:
    """
    Extract features from ELF (Linux/Unix executable) files.

    Provides detailed analysis of ELF file structure including headers,
    sections, segments, and other ELF-specific characteristics.
    """

    @staticmethod
    def is_elf_file(file_path: str) -> bool:
        """
        Check if file is a valid ELF file.

        Args:
            file_path: Path to the file

        Returns:
            True if file is an ELF file, False otherwise
        """
        if not ELFTOOLS_AVAILABLE:
            return False

        try:
            with open(file_path, 'rb') as f:
                # Check for ELF magic number
                header = f.read(4)
                return header == b'\x7fELF'
        except Exception as e:
            logger.debug(f"Error checking ELF file: {e}")
            return False

    @staticmethod
    def extract(file_path: str) -> Dict[str, Any]:
        """
        Extract ELF file features.

        Args:
            file_path: Path to ELF file

        Returns:
            Dictionary containing extracted ELF features
        """
        if not ELFTOOLS_AVAILABLE:
            return {'error': 'pyelftools library not available'}

        if not os.path.exists(file_path):
            return {'error': 'File not found'}

        try:
            with open(file_path, 'rb') as f:
                elf = ELFFile(f)

                # Basic ELF information
                features = {
                    'is_elf': True,
                    'class': elf.elfclass,  # 32 or 64-bit
                    'is_32bit': elf.elfclass == 32,
                    'is_64bit': elf.elfclass == 64,
                    'byte_order': elf.little_endian,
                    'machine': elf['e_machine'],
                    'type': elf['e_type'],
                    'is_executable': elf['e_type'] == 'ET_EXEC',
                    'is_shared_object': elf['e_type'] == 'ET_DYN',
                    'entry_point': elf['e_entry'],
                }

                # Section information
                features['sections'] = ELFExtractor._extract_sections(elf)

                # Segment information
                features['segments'] = ELFExtractor._extract_segments(elf)

                # Symbol information
                features['symbols'] = ELFExtractor._extract_symbols(elf)

                # Suspicious characteristics
                features['suspicious_characteristics'] = \
                    ELFExtractor._check_suspicious(features)

                return features

        except Exception as e:
            logger.error(f"Error extracting ELF features: {e}")
            return {'error': str(e), 'is_elf': False}

    @staticmethod
    def _extract_sections(elf) -> List[Dict[str, Any]]:
        """Extract section information."""
        sections = []
        for section in elf.iter_sections():
            try:
                section_info = {
                    'name': section.name,
                    'type': section['sh_type'],
                    'address': section['sh_addr'],
                    'size': section['sh_size'],
                    'is_executable': bool(section['sh_flags'] & 0x4),
                    'is_writable': bool(section['sh_flags'] & 0x1),
                }
                sections.append(section_info)
            except Exception as e:
                logger.debug(f"Error extracting section: {e}")

        return sections

    @staticmethod
    def _extract_segments(elf) -> List[Dict[str, Any]]:
        """Extract segment (program header) information."""
        segments = []
        for segment in elf.iter_segments():
            try:
                segment_info = {
                    'type': segment['p_type'],
                    'vaddr': segment['p_vaddr'],
                    'paddr': segment['p_paddr'],
                    'size': segment['p_filesz'],
                    'mem_size': segment['p_memsz'],
                    'is_executable': bool(segment['p_flags'] & 0x1),
                    'is_writable': bool(segment['p_flags'] & 0x2),
                    'is_readable': bool(segment['p_flags'] & 0x4),
                }
                segments.append(segment_info)
            except Exception as e:
                logger.debug(f"Error extracting segment: {e}")

        return segments

    @staticmethod
    def _extract_symbols(elf) -> List[str]:
        """Extract symbol information."""
        symbols = []
        try:
            symbol_tables = [s for s in elf.iter_sections()
                             if s.name in ['.symtab', '.dynsym']]
            for section in symbol_tables:
                for symbol in section.iter_symbols():
                    if symbol.name:
                        symbols.append(symbol.name)
                        if len(symbols) >= 100:  # Limit to 100 symbols
                            break
                if len(symbols) >= 100:
                    break
        except Exception as e:
            logger.debug(f"Error extracting symbols: {e}")

        return symbols

    @staticmethod
    def _check_suspicious(features: Dict[str, Any]) -> List[str]:
        """Check for suspicious ELF characteristics."""
        suspicious = []

        # Writable and executable segments (potential code injection)
        for segment in features.get('segments', []):
            if segment.get('is_writable') and segment.get('is_executable'):
                suspicious.append("Writable and executable segment found")

        # Unusual sections
        suspicious_sections = ['.init_array', '.fini_array']
        for section in features.get('sections', []):
            if section['name'] in suspicious_sections:
                suspicious.append(
                    f"Suspicious section: {section['name']}")

        return suspicious
