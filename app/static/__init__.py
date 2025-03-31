"""Static files initialization."""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Define path to static files
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))

def mount_static_files(app: FastAPI) -> None:
    """Mount static files to the FastAPI application."""
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static") 