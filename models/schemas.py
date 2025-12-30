"""
Pydantic models for request and response validation
"""

from typing import List
from pydantic import BaseModel, Field


class ConversionResponse(BaseModel):
    """Response model for PDF to JPG conversion"""
    success: bool = Field(..., description="Whether the conversion was successful")
    message: str = Field(..., description="Response message")
    filename: str | None = Field(None, description="Name of the converted file")
    file_size: int | None = Field(None, description="Size of the converted file in bytes")


class SplitFileInfo(BaseModel):
    """Information about a split PDF file"""
    filename: str = Field(..., description="Name of the split file")
    page_number: int = Field(..., description="Page number from original PDF")
    file_size: int = Field(..., description="Size of the file in bytes")
    file_path: str = Field(..., description="Relative path to access the file")


class SplitPdfResponse(BaseModel):
    """Response model for PDF split operation"""
    success: bool = Field(..., description="Whether the split was successful")
    message: str = Field(..., description="Response message")
    total_pages: int = Field(..., description="Total number of pages split")
    files: List[SplitFileInfo] = Field(..., description="List of split PDF files")
