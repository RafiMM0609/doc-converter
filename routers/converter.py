"""
API endpoints for PDF to JPG conversion
"""

import os
from pathlib import Path
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from services.pdf_service import convert_pdf_to_jpg, merge_pdfs
from utils.file_handler import (
    validate_file, 
    save_upload_file, 
    save_multiple_upload_files,
    cleanup_file, 
    cleanup_multiple_files,
    get_file_size
)

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


@router.post("/merge-pdfs")
async def merge_pdfs_endpoint(files: List[UploadFile] = File(..., description="PDF files to merge (minimum 2 files)")):
    """
    Merge multiple PDF files into a single PDF
    
    - **files**: List of PDF files to upload and merge (minimum 2 files required)
    
    Returns the merged PDF file
    """
    pdf_paths = []
    merged_path = None
    
    try:
        # Validate minimum number of files
        if not files or len(files) < 2:
            raise HTTPException(status_code=400, detail="At least 2 PDF files are required for merging")
        
        # Save all uploaded PDFs
        pdf_paths = save_multiple_upload_files(files)
        
        # Merge PDFs
        merged_path = merge_pdfs(pdf_paths)
        
        # Get file info
        file_size = get_file_size(merged_path)
        filename = os.path.basename(merged_path)
        
        # Return the merged PDF file
        return FileResponse(
            path=merged_path,
            media_type="application/pdf",
            filename=filename,
            headers={
                "X-File-Size": str(file_size),
                "X-Success": "true",
                "X-Message": "PDFs merged successfully",
                "X-Files-Merged": str(len(files))
            }
        )
        
    except Exception as e:
        # Cleanup files on error
        if pdf_paths:
            cleanup_multiple_files(pdf_paths)
        if merged_path:
            cleanup_file(merged_path)
        raise
    finally:
        # Cleanup uploaded PDFs
        if pdf_paths:
            cleanup_multiple_files(pdf_paths)
