"""
PDF to JPG conversion service with business logic
"""

import os
import uuid
from pathlib import Path
from pdf2image import convert_from_path
from fastapi import HTTPException
from config import MAX_PAGES, DPI, IMAGE_FORMAT, CONVERTED_DIR


def convert_pdf_to_jpg(pdf_path: str) -> str:
    """
    Convert PDF file (first page only) to JPG
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Path to the converted JPG file
        
    Raises:
        HTTPException: If conversion fails
    """
    try:
        # Convert first page of PDF to image
        images = convert_from_path(
            pdf_path,
            dpi=DPI,
            first_page=1,
            last_page=MAX_PAGES,
            fmt=IMAGE_FORMAT.lower()
        )
        
        if not images:
            raise HTTPException(status_code=500, detail="Failed to convert PDF - no pages found")
        
        # Get the first page
        image = images[0]
        
        # Generate unique filename for output
        output_filename = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(CONVERTED_DIR, output_filename)
        
        # Save as JPG
        image.save(output_path, IMAGE_FORMAT, quality=95)
        
        return output_path
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert PDF to JPG: {str(e)}")
