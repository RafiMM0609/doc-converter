# PDF Converter API

Simple FastAPI backend service for converting PDF files and merging multiple PDFs.

## Features

- Convert PDF to JPG (first page only)
- Merge multiple PDF files into a single PDF
- Clean code architecture with separated concerns
- File validation and error handling
- RESTful API with automatic documentation
- CORS enabled for cross-origin requests

## Project Structure

```
doc-converter/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Project dependencies
├── models/
│   ├── __init__.py
│   └── schemas.py        # Pydantic models for request/response
├── services/
│   ├── __init__.py
│   └── pdf_service.py    # PDF to JPG conversion logic
├── routers/
│   ├── __init__.py
│   └── converter.py      # API endpoints
└── utils/
    ├── __init__.py
    └── file_handler.py   # File handling utilities
```

## Requirements

- Python 3.10 or higher
- poppler-utils (for PDF processing)

## Installation

### 1. Install System Dependencies

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

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Start the Server

```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### API Endpoints

#### Root Endpoint
- **GET** `/`
- Returns API information

#### Health Check
- **GET** `/health`
- Returns service health status

#### Convert PDF to JPG
- **POST** `/api/convert-pdf-to-jpg`
- Upload a PDF file and receive a JPG image of the first page
- **Parameters:**
  - `file`: PDF file (multipart/form-data)
- **Response:** JPG image file

#### Merge PDFs
- **POST** `/api/merge-pdfs`
- Upload multiple PDF files and receive a single merged PDF
- **Parameters:**
  - `files`: List of PDF files (multipart/form-data, minimum 2 files)
- **Response:** Merged PDF file

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example Usage

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/convert-pdf-to-jpg" \
  -H "accept: image/jpeg" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf" \
  --output converted.jpg
```

### Using Python Requests

```python
import requests

url = "http://localhost:8000/api/convert-pdf-to-jpg"
files = {'file': open('document.pdf', 'rb')}

response = requests.post(url, files=files)

if response.status_code == 200:
    with open('converted.jpg', 'wb') as f:
        f.write(response.content)
    print("Conversion successful!")
else:
    print(f"Error: {response.status_code}")
```

### Using JavaScript Fetch

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/convert-pdf-to-jpg', {
  method: 'POST',
  body: formData
})
.then(response => response.blob())
.then(blob => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'converted.jpg';
  a.click();
});
```

### Merge PDFs

#### Using cURL

```bash
curl -X POST "http://localhost:8000/api/merge-pdfs" \
  -H "accept: application/pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@/path/to/first.pdf" \
  -F "files=@/path/to/second.pdf" \
  -F "files=@/path/to/third.pdf" \
  --output merged.pdf
```

#### Using Python Requests

```python
import requests

url = "http://localhost:8000/api/merge-pdfs"
files = [
    ('files', open('first.pdf', 'rb')),
    ('files', open('second.pdf', 'rb')),
    ('files', open('third.pdf', 'rb'))
]

response = requests.post(url, files=files)

if response.status_code == 200:
    with open('merged.pdf', 'wb') as f:
        f.write(response.content)
    print("Merge successful!")
else:
    print(f"Error: {response.status_code}")
```

#### Using JavaScript Fetch

```javascript
const formData = new FormData();
formData.append('files', fileInput1.files[0]);
formData.append('files', fileInput2.files[0]);
formData.append('files', fileInput3.files[0]);

fetch('http://localhost:8000/api/merge-pdfs', {
  method: 'POST',
  body: formData
})
.then(response => response.blob())
.then(blob => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'merged.pdf';
  a.click();
});
```

## Configuration

Edit `config.py` to customize:
- `MAX_FILE_SIZE`: Maximum upload file size (default: 10 MB)
- `MAX_PAGES`: Number of pages to convert (default: 1)
- `DPI`: Resolution for conversion (default: 200)
- `IMAGE_FORMAT`: Output format (default: JPEG)

## Clean Code Principles

The project follows clean code architecture:

1. **Separation of Concerns**: Code is organized into distinct modules
   - `models/`: Data models and schemas
   - `services/`: Business logic
   - `routers/`: API endpoints
   - `utils/`: Utility functions

2. **Single Responsibility**: Each module has a specific purpose
   - `pdf_service.py`: PDF conversion and merging logic only
   - `file_handler.py`: File operations only
   - `converter.py`: API routing only

3. **Dependency Injection**: Dependencies are injected through function parameters

4. **Error Handling**: Comprehensive error handling with meaningful messages

5. **Documentation**: Clear docstrings and type hints throughout

## License

MIT
