"""
File handling utilities for upload and cleanup operations
"""

import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, UPLOAD_DIR, CONVERTED_DIR


def validate_file(file: UploadFile) -> None:
    """
    Validate uploaded file
    
    Args:
        file: Uploaded file object
        
    Raises:
        HTTPException: If file validation fails
    """
    # Check if file has a name
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Only {', '.join(ALLOWED_EXTENSIONS)} files are allowed"
        )


def save_upload_file(file: UploadFile) -> str:
    """
    Save uploaded file to disk with a unique filename
    
    Args:
        file: Uploaded file object
        
    Returns:
        Path to the saved file
        
    Raises:
        HTTPException: If file saving fails
    """
    try:
        # Generate unique filename
        file_ext = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            
            # Check file size
            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400, 
                    detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024 * 1024)} MB"
                )
            
            buffer.write(content)
        
        return file_path
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")


def cleanup_file(file_path: str) -> None:
    """
    Remove file from disk
    
    Args:
        file_path: Path to the file to be removed
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        # Silently fail cleanup
        pass


def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in bytes
    """
    return os.path.getsize(file_path)
