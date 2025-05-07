#!/usr/bin/env python3
"""
Test script for the FileConversionService.
This script converts an SVG file to PNG, PDF, and JPEG formats to verify that the service works correctly.
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path so we can import app modules
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from app.services.file_conversion import FileConversionService

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Path to our test SVG file
    svg_path = project_root / "app" / "static" / "images" / "svg" / "western_31a348f7.svg"
    output_dir = project_root / "cache"
    
    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)
    
    logger.info(f"Testing FileConversionService with SVG file: {svg_path}")
    
    # Initialize the service
    service = FileConversionService()
    
    try:
        # Test SVG to PNG conversion
        png_path = output_dir / "test_conversion.png"
        png_result = service.convert_svg_file_to_format(
            svg_file_path=svg_path,
            output_format="png",
            output_file_path=png_path
        )
        logger.info(f"PNG conversion successful: {png_result}")
        logger.info(f"PNG file size: {png_result.stat().st_size} bytes")
        
        # Test SVG to PDF conversion
        pdf_path = output_dir / "test_conversion.pdf"
        pdf_result = service.convert_svg_file_to_format(
            svg_file_path=svg_path,
            output_format="pdf",
            output_file_path=pdf_path
        )
        logger.info(f"PDF conversion successful: {pdf_result}")
        logger.info(f"PDF file size: {pdf_result.stat().st_size} bytes")
        
        # Test SVG to JPEG conversion
        jpg_path = output_dir / "test_conversion.jpg"
        jpg_result = service.convert_svg_file_to_format(
            svg_file_path=svg_path,
            output_format="jpg",
            output_file_path=jpg_path
        )
        logger.info(f"JPEG conversion successful: {jpg_result}")
        logger.info(f"JPEG file size: {jpg_result.stat().st_size} bytes")
        
        # Test direct content conversion (SVG to PNG)
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
            
        png_bytes, content_type = service.convert_svg_to_format(
            svg_content=svg_content,
            output_format="png"
        )
        logger.info(f"Direct PNG conversion successful, received {len(png_bytes)} bytes with content-type: {content_type}")
        
        logger.info("All conversion tests passed successfully!")
        
    except Exception as e:
        logger.error(f"Error during conversion tests: {e}", exc_info=True)
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main()) 