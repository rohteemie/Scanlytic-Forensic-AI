"""
PE (Portable Executable) file feature extractor.

Extracts features from Windows PE files including headers, sections,
imports, exports, and other PE-specific metadata.
"""

from typing import Dict, Any, Optional, List
import os

from scanlytic.utils.logger import get_logger

logger = get_logger()

# Import pefile only when needed to avoid dependency issues
try:
    import pefile
    PEFILE_AVAILABLE = True
except ImportError:
    PEFILE_AVAILABLE = False
    logger.warning("pefile library not available. PE analysis disabled.")


class PEExtractor:
    """
    Extract features from PE (Windows executable) files.

    Provides detailed analysis of PE file structure including headers,
    sections, imports, exports, and other PE-specific characteristics.
    """

    @staticmethod
    def is_pe_file(file_path: str) -> bool:
        """
        Check if file is a valid PE file.

        Args:
            file_path: Path to the file

        Returns:
            True if file is a PE file, False otherwise
        """
        if not PEFILE_AVAILABLE:
            return False

        try:
            with open(file_path, 'rb') as f:
                # Check for MZ header
                header = f.read(2)
                return header == b'MZ'
        except Exception as e:
            logger.debug(f"Error checking PE file: {e}")
            return False

    @staticmethod
    def extract(file_path: str) -> Dict[str, Any]:
        """
        Extract PE file features.

        Args:
            file_path: Path to PE file

        Returns:
            Dictionary containing extracted PE features
        """
        if not PEFILE_AVAILABLE:
            return {'error': 'pefile library not available'}

        if not os.path.exists(file_path):
            return {'error': 'File not found'}

        try:
            pe = pefile.PE(file_path, fast_load=True)

            # Basic PE information
            features = {
                'is_pe': True,
                'machine_type': pe.FILE_HEADER.Machine,
                'is_32bit': pe.FILE_HEADER.Machine == 0x014c,
                'is_64bit': pe.FILE_HEADER.Machine == 0x8664,
                'is_dll': pe.is_dll(),
                'is_exe': pe.is_exe(),
                'is_driver': pe.is_driver(),
                'timestamp': pe.FILE_HEADER.TimeDateStamp,
                'number_of_sections': pe.FILE_HEADER.NumberOfSections,
            }

            # Optional header information
            if hasattr(pe, 'OPTIONAL_HEADER'):
                features.update({
                    'entry_point': pe.OPTIONAL_HEADER.AddressOfEntryPoint,
                    'image_base': pe.OPTIONAL_HEADER.ImageBase,
                    'subsystem': pe.OPTIONAL_HEADER.Subsystem,
                })

            # Section information
            features['sections'] = PEExtractor._extract_sections(pe)

            # Import information
            features['imports'] = PEExtractor._extract_imports(pe)

            # Export information
            features['exports'] = PEExtractor._extract_exports(pe)

            # Suspicious characteristics
            features['suspicious_characteristics'] = \
                PEExtractor._check_suspicious(pe, features)

            pe.close()
            return features

        except pefile.PEFormatError as e:
            logger.debug(f"PE format error: {e}")
            return {'error': 'Invalid PE format', 'is_pe': False}
        except Exception as e:
            logger.error(f"Error extracting PE features: {e}")
            return {'error': str(e), 'is_pe': False}

    @staticmethod
    def _extract_sections(pe) -> List[Dict[str, Any]]:
        """Extract section information."""
        sections = []
        for section in pe.sections:
            try:
                section_info = {
                    'name': section.Name.decode(
                        'utf-8',
                        errors='ignore'
                        ).strip('\x00'),
                    'virtual_address': section.VirtualAddress,
                    'virtual_size': section.Misc_VirtualSize,
                    'raw_size': section.SizeOfRawData,
                    'entropy': section.get_entropy(),
                    'is_executable': bool(
                        section.Characteristics & 0x20000000),
                    'is_writable': bool(section.Characteristics & 0x80000000),
                }
                sections.append(section_info)
            except Exception as e:
                logger.debug(f"Error extracting section: {e}")

        return sections

    @staticmethod
    def _extract_imports(pe) -> Dict[str, List[str]]:
        """Extract import information."""
        imports = {}
        try:
            pe.parse_data_directories(
                directories=[pefile.DIRECTORY_ENTRY[
                    'IMAGE_DIRECTORY_ENTRY_IMPORT'
                    ]]
            )
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    dll_name = entry.dll.decode(
                        'utf-8', errors='ignore'
                        )
                    functions = []
                    for imp in entry.imports:
                        if imp.name:
                            func_name = imp.name.decode('utf-8',
                                                        errors='ignore')
                            functions.append(func_name)
                    imports[dll_name] = functions[:50]  # Limit to 50 funcs
        except Exception as e:
            logger.debug(f"Error extracting imports: {e}")

        return imports

    @staticmethod
    def _extract_exports(pe) -> List[str]:
        """Extract export information."""
        exports = []
        try:
            pe.parse_data_directories(
                directories=[pefile.DIRECTORY_ENTRY[
                    'IMAGE_DIRECTORY_ENTRY_EXPORT'
                    ]]
            )
            if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
                for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                    if exp.name:
                        export_name = exp.name.decode('utf-8',
                                                      errors='ignore')
                        exports.append(export_name)
        except Exception as e:
            logger.debug(f"Error extracting exports: {e}")

        return exports[:100]  # Limit to 100 exports

    @staticmethod
    def _check_suspicious(pe, features: Dict[str, Any]) -> List[str]:
        """Check for suspicious PE characteristics."""
        suspicious = []

        # High entropy sections (packed/encrypted)
        for section in features.get('sections', []):
            if section.get('entropy', 0) > 7.0:
                suspicious.append(
                    f"High entropy section: {section['name']}")

        # Unusual section names
        normal_sections = {'.text', '.data', '.rdata', '.rsrc', '.reloc'}
        for section in features.get('sections', []):
            if section['name'] not in normal_sections and section['name']:
                suspicious.append(
                    f"Unusual section name: {section['name']}")

        # Suspicious imports
        suspicious_dlls = {
            'ws2_32.dll': 'network',
            'wininet.dll': 'internet',
            'advapi32.dll': 'registry/services',
        }
        for dll in features.get('imports', {}).keys():
            dll_lower = dll.lower()
            for sus_dll, reason in suspicious_dlls.items():
                if sus_dll in dll_lower:
                    suspicious.append(f"Suspicious DLL: {dll} ({reason})")

        return suspicious
