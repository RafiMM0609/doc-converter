"""
File handling utilities for upload and cleanup operations
"""

import os
import uuid
from pathlib import Path
from typing import List
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
        
        # Save file in chunks and check size
        total_size = 0
        chunk_size = 1024 * 1024  # 1 MB chunks
        
        with open(file_path, "wb") as buffer:
            while True:
                chunk = file.file.read(chunk_size)
                if not chunk:
                    break
                
                total_size += len(chunk)
                
                # Check if size exceeds limit
                if total_size > MAX_FILE_SIZE:
                    # Remove partial file
                    cleanup_file(file_path)
                    raise HTTPException(
                        status_code=400, 
                        detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024 * 1024)} MB"
                    )
                
                buffer.write(chunk)
        
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


def save_multiple_upload_files(files: List[UploadFile]) -> List[str]:
    """
    Save multiple uploaded files to disk with unique filenames
    
    Args:
        files: List of uploaded file objects
        
    Returns:
        List of paths to the saved files
        
    Raises:
        HTTPException: If file saving fails
    """
    saved_paths = []
    
    try:
        for file in files:
            # Validate each file
            validate_file(file)
            
            # Save file
            file_path = save_upload_file(file)
            saved_paths.append(file_path)
        
        return saved_paths
        
    except Exception as e:
        # Cleanup all saved files on error
        for path in saved_paths:
            cleanup_file(path)
        raise


def cleanup_multiple_files(file_paths: List[str]) -> None:
    """
    Remove multiple files from disk
    
    Args:
        file_paths: List of file paths to be removed
    """
    for file_path in file_paths:
        cleanup_file(file_path)
