import io
import os
import logging
from pathlib import Path
from typing import Dict, Literal, Optional, BinaryIO, Union, Tuple

import cairosvg
from PIL import Image

from app.core.svg_utils import preprocess_svg_for_conversion
from app.core.exceptions import FileConversionError

logger = logging.getLogger(__name__)

# Supported output formats
OutputFormat = Literal["svg", "png", "pdf", "jpg"]

# Content type mapping for HTTP responses
CONTENT_TYPE_MAP: Dict[str, str] = {
    "svg": "image/svg+xml",
    "png": "image/png",
    "pdf": "application/pdf",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg"
}

# File extension mapping (normalized)
FILE_EXTENSION_MAP: Dict[str, str] = {
    "svg": "svg",
    "png": "png",
    "pdf": "pdf",
    "jpg": "jpg",
    "jpeg": "jpg"
}


class FileConversionService:
    """Service for converting files between different formats."""

    def __init__(self):
        """Initialize the FileConversionService."""
        pass

    def convert_svg_to_format(
        self,
        svg_content: Union[str, bytes],
        output_format: OutputFormat,
        dpi: int = 96
    ) -> Tuple[bytes, str]:
        """
        Convert SVG content to the specified format.

        Args:
            svg_content: The SVG content as a string or bytes
            output_format: The desired output format (svg, png, pdf, jpg)
            dpi: The resolution in dots per inch (for raster formats)

        Returns:
            Tuple[bytes, str]: The converted content as bytes and the appropriate content type
        """
        if isinstance(svg_content, bytes):
            svg_content = svg_content.decode("utf-8")

        try:
            # Preprocess SVG to replace CSS variables
            processed_svg = preprocess_svg_for_conversion(svg_content)
            
            if output_format == "svg":
                return processed_svg.encode("utf-8"), CONTENT_TYPE_MAP["svg"]
            
            # Convert to the requested format using CairoSVG
            if output_format == "png":
                output_bytes = cairosvg.svg2png(
                    bytestring=processed_svg.encode("utf-8"),
                    dpi=dpi
                )
                return output_bytes, CONTENT_TYPE_MAP["png"]
            
            elif output_format == "pdf":
                output_bytes = cairosvg.svg2pdf(
                    bytestring=processed_svg.encode("utf-8"),
                    dpi=dpi
                )
                return output_bytes, CONTENT_TYPE_MAP["pdf"]
            
            elif output_format in ("jpg", "jpeg"):
                # CairoSVG doesn't directly support JPEG output,
                # so we convert to PNG first and then to JPEG
                png_bytes = cairosvg.svg2png(
                    bytestring=processed_svg.encode("utf-8"),
                    dpi=dpi
                )
                
                # Use PIL to convert PNG to JPEG
                with Image.open(io.BytesIO(png_bytes)) as img:
                    img = img.convert("RGB")  # Remove alpha channel
                    jpeg_buffer = io.BytesIO()
                    img.save(jpeg_buffer, format="JPEG", quality=90)
                    jpeg_bytes = jpeg_buffer.getvalue()
                
                return jpeg_bytes, CONTENT_TYPE_MAP["jpg"]
            
            else:
                raise FileConversionError(f"Unsupported output format: {output_format}")
            
        except Exception as e:
            logger.error(f"Error converting SVG to {output_format}: {str(e)}", exc_info=True)
            raise FileConversionError(f"Failed to convert SVG to {output_format}: {str(e)}") from e

    def convert_svg_file_to_format(
        self,
        svg_file_path: Union[str, Path],
        output_format: OutputFormat,
        output_file_path: Optional[Union[str, Path]] = None,
        dpi: int = 96
    ) -> Path:
        """
        Convert an SVG file to the specified format.

        Args:
            svg_file_path: Path to the SVG file
            output_format: The desired output format (svg, png, pdf, jpg)
            output_file_path: Optional path for the output file. If not provided,
                            uses the original filename with the new extension.
            dpi: The resolution in dots per inch (for raster formats)

        Returns:
            Path: The path to the converted file
        """
        svg_file_path = Path(svg_file_path)
        
        if not svg_file_path.exists():
            raise FileNotFoundError(f"SVG file not found: {svg_file_path}")
        
        # Determine output file path if not provided
        if output_file_path is None:
            output_ext = FILE_EXTENSION_MAP.get(output_format, output_format)
            output_file_path = svg_file_path.with_suffix(f".{output_ext}")
        else:
            output_file_path = Path(output_file_path)
        
        try:
            # Read SVG file
            with open(svg_file_path, "r", encoding="utf-8") as f:
                svg_content = f.read()
            
            # Convert the SVG
            output_bytes, _ = self.convert_svg_to_format(
                svg_content,
                output_format,
                dpi
            )
            
            # Save the output file
            with open(output_file_path, "wb") as f:
                f.write(output_bytes)
            
            logger.info(f"Successfully converted {svg_file_path} to {output_file_path}")
            return output_file_path
            
        except Exception as e:
            logger.error(f"Error converting SVG file to {output_format}: {str(e)}", exc_info=True)
            raise FileConversionError(f"Failed to convert SVG file to {output_format}: {str(e)}") from e 