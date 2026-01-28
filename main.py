"""
Main FastAPI application entry point for PDF to JPG converter service
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
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

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Root endpoint with UI and API information"""
    return {
        "message": "PDF Converter API",
        "version": "1.0.0",
        "ui": "http://localhost:8000/index.html",
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


@app.get("/index.html")
async def serve_index():
    """Serve index.html"""
    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/html")
    return {"detail": "index.html not found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
