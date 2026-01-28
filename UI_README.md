# PDF Converter - Complete Application

A modern, full-featured web application for converting PDF files to JPG images and merging multiple PDF documents. Built with FastAPI backend and a responsive web UI.

## Features

### 🔄 Convert PDF to JPG
- Upload a single PDF file
- Convert the first page to a high-quality JPG image
- Preview the converted image
- Download the JPG file

### 📚 Merge PDFs
- Upload multiple PDF files (minimum 2)
- Drag and drop interface for easy file selection
- Merge all PDFs into a single document
- Download the merged PDF

### ✨ UI Features
- **Modern Design**: Clean, intuitive interface with smooth animations
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Drag & Drop**: Easy file upload with drag-and-drop support
- **Real-time Feedback**: Progress indicators and notifications
- **Tab Navigation**: Easy switching between convert and merge features
- **File Management**: Add, remove, and manage uploaded files

## Project Structure

```
doc-converter/
├── main.py                 # FastAPI entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── index.html             # Main UI file
├── static/
│   ├── style.css          # Responsive styling
│   └── app.js             # UI logic and API integration
├── models/
│   └── schemas.py         # Pydantic models
├── services/
│   └── pdf_service.py     # PDF conversion logic
├── routers/
│   └── converter.py       # API endpoints
└── utils/
    └── file_handler.py    # File handling utilities
```

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- poppler-utils (required for PDF processing)

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
Download and install poppler from: https://github.com/oschwartz10612/poppler-windows/releases

### Python Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the application:
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Open in your browser:
```
http://localhost:8000/index.html
```

## Usage Guide

### Convert PDF to JPG

1. **Select Tab**: Click on "Convert to Image" tab
2. **Upload File**: 
   - Click the upload area, or
   - Drag and drop a PDF file
3. **Convert**: Click the "Convert to JPG" button
4. **Preview**: View the converted image
5. **Download**: Click "Download JPG" to save

### Merge PDFs

1. **Select Tab**: Click on "Merge PDFs" tab
2. **Upload Files**:
   - Click the upload area and select multiple PDFs, or
   - Drag and drop multiple PDF files
   - Files appear in a list for easy management
3. **Manage Files**: 
   - Remove individual files with the ✕ button
   - Clear all files with "Clear All" button
4. **Merge**: Click "Merge PDFs" button (enabled when 2+ files selected)
5. **Download**: Click "Download PDF" to save merged document

## API Documentation

### Available Endpoints

#### Convert PDF to JPG
```
POST /api/convert-pdf-to-jpg
Content-Type: multipart/form-data

Body:
- file: PDF file (max 10 MB)

Response: JPG image file
```

#### Merge PDFs
```
POST /api/merge-pdfs
Content-Type: multipart/form-data

Body:
- files: Multiple PDF files (each max 10 MB, minimum 2 files)

Response: Merged PDF file
```

### Interactive API Docs

Once the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Configuration

Edit `config.py` to customize:

```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # Max upload size (10 MB)
MAX_PAGES = 1                      # Pages to convert (1 = first page only)
DPI = 200                          # Resolution for conversion
IMAGE_FORMAT = 'JPEG'              # Output format
CONVERTED_DIR = 'converted'        # Output directory for results
UPLOAD_DIR = 'uploads'             # Temporary upload directory
```

## Browser Compatibility

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## File Size Limits

- **Maximum per file**: 10 MB
- **Convert**: 1 PDF file
- **Merge**: Minimum 2 PDF files, maximum depends on system memory

## Supported File Types

- PDF files only (.pdf extension)

## Error Handling

The application includes comprehensive error handling:
- Invalid file type validation
- File size limit checking
- Network error recovery
- Detailed error messages in notifications
- API error response handling

## Performance

- **Convert Speed**: ~2-5 seconds (depends on PDF complexity and DPI)
- **Merge Speed**: ~1-3 seconds (depends on file sizes)
- **Max File Size**: 10 MB per file
- **Image Quality**: 95% JPEG quality, 200 DPI

## Troubleshooting

### Files fail to upload
- Check file size (max 10 MB)
- Ensure files are valid PDF files
- Try clearing browser cache

### Conversion fails
- Verify poppler-utils is installed
- Check if PDF is not encrypted or corrupted
- Check server logs for detailed errors

### UI doesn't load
- Ensure FastAPI server is running
- Check browser console for JavaScript errors
- Try accessing: http://localhost:8000/index.html directly

### CORS errors
- CORS is already enabled in the application
- Check if API is running on http://localhost:8000

## Development

### Tech Stack
- **Backend**: FastAPI, Python 3.10+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **PDF Processing**: pdf2image, PyPDF2
- **Server**: Uvicorn

### Code Structure
The project follows clean code architecture with:
- Separation of concerns
- Single responsibility principle
- Comprehensive error handling
- Type hints throughout
- Clear documentation

## License

MIT License

## Support

For issues or questions:
1. Check the API documentation at http://localhost:8000/docs
2. Review error messages in the UI
3. Check browser console (F12 → Console tab)
4. Review server logs

## Version History

### v1.0.0
- Initial release
- PDF to JPG conversion
- PDF merge functionality
- Modern responsive UI
- Full API documentation
