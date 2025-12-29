"""
Main FastAPI application entry point for PDF to JPG converter service
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import converter

# Create FastAPI application
app = FastAPI(
    title="PDF Converter API",
    description="API to convert PDF files to JPG images and merge multiple PDFs",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(converter.router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "PDF Converter API",
        "version": "1.0.0",
        "endpoints": {
            "convert": "/api/convert-pdf-to-jpg",
            "merge": "/api/merge-pdfs",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
