"""Templates initialization module."""
import os
import datetime
from fastapi.templating import Jinja2Templates

# Define the template directory
TEMPLATES_DIR = os.path.dirname(os.path.abspath(__file__))

# Create templates object for use throughout the app
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Add custom Jinja2 filters/functions
templates.env.globals.update({
    "now": lambda fmt="%Y-%m-%d %H:%M:%S": datetime.datetime.now().strftime(fmt),
}) 