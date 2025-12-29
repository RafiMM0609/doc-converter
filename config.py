"""
Configuration settings for the PDF to JPG converter service
"""

import os

# File upload settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".pdf"}

# Conversion settings
MAX_PAGES = 1  # Only convert first page
DPI = 200  # Resolution for converted image
IMAGE_FORMAT = "JPEG"

# Directory settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
CONVERTED_DIR = os.path.join(BASE_DIR, "converted")

# Create directories if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CONVERTED_DIR, exist_ok=True)
