"""
API endpoints for PDF to JPG conversion
"""

import os
from pathlib import Path
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from services.pdf_service import convert_pdf_to_jpg
from utils.file_handler import validate_file, save_upload_file, cleanup_file, get_file_size

router = APIRouter(prefix="/api", tags=["converter"])


@router.post("/convert-pdf-to-jpg")
async def convert_pdf_to_jpg_endpoint(file: UploadFile = File(..., description="PDF file to convert (max 1 page)")):
    """
    Convert PDF file to JPG image
    
    - **file**: PDF file to upload (maximum 1 page will be converted)
    
    Returns the converted JPG file
    """
    pdf_path = None
    jpg_path = None
    
    try:
        # Validate file
        validate_file(file)
        
        # Save uploaded PDF
        pdf_path = save_upload_file(file)
        
        # Convert PDF to JPG
        jpg_path = convert_pdf_to_jpg(pdf_path)
        
        # Get file info
        file_size = get_file_size(jpg_path)
        filename = os.path.basename(jpg_path)
        
        # Return the JPG file
        return FileResponse(
            path=jpg_path,
            media_type="image/jpeg",
            filename=filename,
            headers={
                "X-File-Size": str(file_size),
                "X-Success": "true",
                "X-Message": "PDF converted to JPG successfully"
            }
        )
        
    except Exception as e:
        # Cleanup files on error
        if pdf_path:
            cleanup_file(pdf_path)
        if jpg_path:
            cleanup_file(jpg_path)
        raise
    finally:
        # Cleanup uploaded PDF
        if pdf_path:
            cleanup_file(pdf_path)
