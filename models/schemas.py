"""
Pydantic models for request and response validation
"""

from pydantic import BaseModel, Field


class ConversionResponse(BaseModel):
    """Response model for PDF to JPG conversion"""
    success: bool = Field(..., description="Whether the conversion was successful")
    message: str = Field(..., description="Response message")
    filename: str | None = Field(None, description="Name of the converted file")
    file_size: int | None = Field(None, description="Size of the converted file in bytes")
