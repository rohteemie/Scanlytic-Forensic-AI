"""
Image file feature extractor.

Extracts features from image files including EXIF data, dimensions,
and other image-specific metadata.
"""

from typing import Dict, Any, Optional, List
import os

from scanlytic.utils.logger import get_logger

logger = get_logger()

# Import PIL only when needed to avoid dependency issues
try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logger.warning("Pillow library not available. Image analysis disabled.")


class ImageExtractor:
    """
    Extract features from image files.

    Provides analysis of image properties including dimensions, format,
    EXIF data, and other image-specific characteristics.
    """

    SUPPORTED_FORMATS = {
        'JPEG', 'JPG', 'PNG', 'GIF', 'BMP', 'TIFF', 'WEBP'
    }

    @staticmethod
    def is_image_file(file_path: str) -> bool:
        """
        Check if file is a supported image file.

        Args:
            file_path: Path to the file

        Returns:
            True if file is a supported image, False otherwise
        """
        if not PIL_AVAILABLE:
            return False

        try:
            with Image.open(file_path) as img:
                return img.format in ImageExtractor.SUPPORTED_FORMATS
        except Exception:
            return False

    @staticmethod
    def extract(file_path: str) -> Dict[str, Any]:
        """
        Extract image file features.

        Args:
            file_path: Path to image file

        Returns:
            Dictionary containing extracted image features
        """
        if not PIL_AVAILABLE:
            return {'error': 'Pillow library not available'}

        if not os.path.exists(file_path):
            return {'error': 'File not found'}

        try:
            with Image.open(file_path) as img:
                # Basic image information
                features = {
                    'is_image': True,
                    'format': img.format,
                    'mode': img.mode,
                    'width': img.width,
                    'height': img.height,
                    'size_pixels': img.width * img.height,
                }

                # EXIF data extraction
                features['exif'] = ImageExtractor._extract_exif(img)

                # Suspicious characteristics
                features['suspicious_characteristics'] = \
                    ImageExtractor._check_suspicious(features)

                return features

        except Exception as e:
            logger.error(f"Error extracting image features: {e}")
            return {'error': str(e), 'is_image': False}

    @staticmethod
    def _extract_exif(img) -> Dict[str, Any]:
        """Extract EXIF data from image."""
        exif_data = {}
        try:
            exifdata = img.getexif()
            if exifdata is None:
                return exif_data

            for tag_id, value in exifdata.items():
                tag = TAGS.get(tag_id, tag_id)
                try:
                    # Convert bytes to string if needed
                    if isinstance(value, bytes):
                        value = value.decode('utf-8', errors='ignore')
                    # Limit string length
                    if isinstance(value, str) and len(value) > 200:
                        value = value[:200] + '...'
                    exif_data[tag] = value
                except Exception as e:
                    logger.debug(f"Error processing EXIF tag {tag}: {e}")

        except Exception as e:
            logger.debug(f"Error extracting EXIF: {e}")

        return exif_data

    @staticmethod
    def _check_suspicious(features: Dict[str, Any]) -> List[str]:
        """Check for suspicious image characteristics."""
        suspicious = []

        # Unusually large images
        size_pixels = features.get('size_pixels', 0)
        if size_pixels > 100000000:  # 100 megapixels
            suspicious.append("Unusually large image size")

        # GPS data in EXIF (privacy concern)
        exif = features.get('exif', {})
        if 'GPSInfo' in exif or 'GPS' in str(exif.keys()):
            suspicious.append("Contains GPS location data")

        return suspicious
