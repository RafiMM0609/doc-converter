"""
PDF to JPG conversion service with business logic
"""

import os
import uuid
from pathlib import Path
from typing import List
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
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


def merge_pdfs(pdf_paths: List[str]) -> str:
    """
    Merge multiple PDF files into a single PDF
    
    Args:
        pdf_paths: List of paths to PDF files to merge
        
    Returns:
        Path to the merged PDF file
        
    Raises:
        HTTPException: If merge fails
    """
    try:
        # Validate input
        if not pdf_paths:
            raise HTTPException(status_code=400, detail="No PDF files provided for merging")
        
        if len(pdf_paths) < 2:
            raise HTTPException(status_code=400, detail="At least 2 PDF files are required for merging")
        
        # Verify all files exist
        for pdf_path in pdf_paths:
            if not os.path.exists(pdf_path):
                raise HTTPException(status_code=400, detail=f"PDF file not found: {pdf_path}")
        
        # Generate unique filename for output
        output_filename = f"{uuid.uuid4()}.pdf"
        output_path = os.path.join(CONVERTED_DIR, output_filename)
        
        # Create PDF merger with context manager for proper resource cleanup
        with PdfMerger() as merger:
            # Add all PDFs to merger
            for pdf_path in pdf_paths:
                merger.append(pdf_path)
            
            # Write merged PDF
            merger.write(output_path)
        
        return output_path
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to merge PDFs: {str(e)}")


def split_pdf(pdf_path: str) -> List[str]:
    """
    Split a PDF file into individual pages
    
    Args:
        pdf_path: Path to the PDF file to split
        
    Returns:
        List of paths to the split PDF files (one file per page)
        
    Raises:
        HTTPException: If split fails
    """
    try:
        # Verify file exists
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=400, detail=f"PDF file not found: {pdf_path}")
        
        # Read the PDF
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
        
        if num_pages == 0:
            raise HTTPException(status_code=400, detail="PDF file has no pages")
        
        # List to store paths of split PDFs
        split_paths = []
        
        # Split each page into a separate PDF
        for page_num in range(num_pages):
            # Create a new PDF writer for this page
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])
            
            # Generate unique filename for output
            output_filename = f"{uuid.uuid4()}_page_{page_num + 1}.pdf"
            output_path = os.path.join(CONVERTED_DIR, output_filename)
            
            # Write the single-page PDF
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            
            split_paths.append(output_path)
        
        return split_paths
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to split PDF: {str(e)}")
