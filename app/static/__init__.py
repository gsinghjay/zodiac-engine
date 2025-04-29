"""Static files initialization."""
import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Define path to static files
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)

def initialize_static_dirs():
    """Ensure all required static directories exist."""
    # Create svg directory if it doesn't exist
    svg_dir = os.path.join(STATIC_DIR, "images", "svg")
    if not os.path.exists(svg_dir):
        logger.info(f"Creating directory: {svg_dir}")
        os.makedirs(svg_dir, exist_ok=True)
        logger.info(f"SVG directory created at {svg_dir}")
    else:
        logger.info(f"SVG directory already exists at {svg_dir}")

def mount_static_files(app: FastAPI) -> None:
    """Mount static files to the FastAPI application."""
    # Ensure directories exist
    initialize_static_dirs()
    
    # Mount static directory
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    logger.info(f"Static files mounted from {STATIC_DIR}") 