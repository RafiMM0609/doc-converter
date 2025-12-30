"""
API endpoints for PDF to JPG conversion
"""

import os
from pathlib import Path
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from services.pdf_service import convert_pdf_to_jpg, merge_pdfs, split_pdf
from models.schemas import SplitPdfResponse, SplitFileInfo
from config import CONVERTED_DIR
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


@router.post("/split-pdf", response_model=SplitPdfResponse)
async def split_pdf_endpoint(file: UploadFile = File(..., description="PDF file to split into individual pages")):
    """
    Split a PDF file into individual pages
    
    - **file**: PDF file to upload and split
    
    Returns a JSON response with a list of split PDF files information
    """
    pdf_path = None
    split_paths = []
    
    try:
        # Validate file
        validate_file(file)
        
        # Save uploaded PDF
        pdf_path = save_upload_file(file)
        
        # Split PDF into individual pages
        split_paths = split_pdf(pdf_path)
        
        # Prepare file information for response
        files_info = []
        for idx, split_path in enumerate(split_paths):
            file_size = get_file_size(split_path)
            filename = os.path.basename(split_path)
            
            files_info.append(SplitFileInfo(
                filename=filename,
                page_number=idx + 1,
                file_size=file_size,
                file_path=f"/api/download/{filename}"
            ))
        
        # Return JSON response with file list
        return SplitPdfResponse(
            success=True,
            message=f"PDF split successfully into {len(split_paths)} pages",
            total_pages=len(split_paths),
            files=files_info
        )
        
    except Exception as e:
        # Cleanup files on error
        if pdf_path:
            cleanup_file(pdf_path)
        if split_paths:
            cleanup_multiple_files(split_paths)
        raise
    finally:
        # Cleanup uploaded PDF
        if pdf_path:
            cleanup_file(pdf_path)


@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download a specific file from the converted directory
    
    - **filename**: Name of the file to download
    
    Returns the requested file
    """
    # Validate filename to prevent path traversal attacks
    # Check for path traversal patterns first
    if '..' in filename or '/' in filename or '\\' in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    # Use basename as additional security layer
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(CONVERTED_DIR, safe_filename)
    
    # Ensure the resolved path is still within CONVERTED_DIR using commonpath
    resolved_path = os.path.abspath(file_path)
    converted_dir_abs = os.path.abspath(CONVERTED_DIR)
    try:
        common_path = os.path.commonpath([resolved_path, converted_dir_abs])
        if common_path != converted_dir_abs:
            raise HTTPException(status_code=400, detail="Invalid file path")
    except ValueError:
        # Paths are on different drives (Windows) or other path issues
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    # Check if file exists
    if not os.path.exists(resolved_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine media type based on file extension
    file_ext = Path(safe_filename).suffix.lower()
    media_type_map = {
        '.pdf': 'application/pdf',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png'
    }
    media_type = media_type_map.get(file_ext, 'application/octet-stream')
    
    # Return the file
    return FileResponse(
        path=resolved_path,
        media_type=media_type,
        filename=safe_filename
    )
