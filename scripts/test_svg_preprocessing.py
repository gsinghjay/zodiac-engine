#!/usr/bin/env python3
"""
Test script for SVG preprocessing functions.
This script loads an SVG file from our project, applies the preprocessing functions,
and saves the processed file for inspection.
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path so we can import app modules
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from app.core.svg_utils import parse_css_variables, substitute_css_variables, preprocess_svg_for_conversion

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Path to our test SVG file
    svg_path = project_root / "app" / "static" / "images" / "svg" / "western_31a348f7.svg"
    output_path = project_root / "app" / "static" / "images" / "svg" / "processed_western_31a348f7.svg"
    
    logger.info(f"Processing SVG file: {svg_path}")
    
    try:
        # Read the SVG file
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
            
        # Extract SVG variables
        variables = parse_css_variables(svg_content)
        logger.info(f"Found {len(variables)} CSS variables")
        
        # Print first 5 variables for inspection
        for i, (key, value) in enumerate(list(variables.items())[:5]):
            logger.info(f"Variable {i+1}: {key} = {value}")
        
        # Preprocess the SVG content
        processed_svg = preprocess_svg_for_conversion(svg_content)
        
        # Save the processed SVG to a new file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(processed_svg)
            
        logger.info(f"Preprocessed SVG saved to: {output_path}")
        
        # Verify the result
        original_var_count = svg_content.count('var(--')
        processed_var_count = processed_svg.count('var(--')
        
        logger.info(f"Original SVG had {original_var_count} var() references")
        logger.info(f"Processed SVG has {processed_var_count} var() references")
        
        if processed_var_count == 0:
            logger.info("SUCCESS: All CSS variables were successfully substituted!")
        else:
            logger.warning(f"WARNING: {processed_var_count} CSS variables were not substituted")
            
    except Exception as e:
        logger.error(f"Error processing SVG: {e}", exc_info=True)
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main()) 