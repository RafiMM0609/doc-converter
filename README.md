# PDF Converter API

A Flask-based REST API for merging multiple PDF files and returning the result as a Base64-encoded stream.

## Features

- Merge multiple PDF files in a single request
- PDF format validation
- Base64-encoded output for easy integration
- Comprehensive error handling
- RESTful API design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RafiMM0609/doc-converter.git
cd doc-converter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

Run the Flask application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

### API Endpoints

#### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "PDF Converter API is running"
}
```

#### Merge PDFs
```
POST /merge-pdf
```

**Request:**
- Content-Type: `multipart/form-data`
- Field name: `files` (multiple files)

**Example using cURL:**
```bash
curl -X POST http://localhost:5000/merge-pdf \
  -F "files=@document1.pdf" \
  -F "files=@document2.pdf" \
  -F "files=@document3.pdf"
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "PDFs merged successfully",
  "merged_pdf": "JVBERi0xLjQKJeLjz9MKMyAwIG9iago8P...",
  "file_count": 3
}
```

**Error Response (400):**
```json
{
  "error": "Invalid file type",
  "message": "File \"document.txt\" is not a PDF"
}
```

### Decoding the Base64 Output

To save the merged PDF from the Base64 response:

**Python:**
```python
import base64
import json
import requests

# Make the request
files = [
    ('files', open('doc1.pdf', 'rb')),
    ('files', open('doc2.pdf', 'rb'))
]
response = requests.post('http://localhost:5000/merge-pdf', files=files)

# Decode and save
if response.status_code == 200:
    data = response.json()
    pdf_bytes = base64.b64decode(data['merged_pdf'])
    with open('merged_output.pdf', 'wb') as f:
        f.write(pdf_bytes)
```

**JavaScript:**
```javascript
// After receiving the response
const base64Data = response.merged_pdf;
const binaryData = atob(base64Data);
const bytes = new Uint8Array(binaryData.length);
for (let i = 0; i < binaryData.length; i++) {
    bytes[i] = binaryData.charCodeAt(i);
}
const blob = new Blob([bytes], { type: 'application/pdf' });
const url = URL.createObjectURL(blob);

// Trigger download
const a = document.createElement('a');
a.href = url;
a.download = 'merged.pdf';
a.click();
```

## Testing

Run the unit tests:
```bash
python -m pytest test_app.py -v
```

Or using unittest:
```bash
python -m unittest test_app.py -v
```

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success - PDFs merged successfully |
| 400 | Bad Request - Invalid input (wrong format, insufficient files, etc.) |
| 404 | Not Found - Endpoint does not exist |
| 405 | Method Not Allowed - Wrong HTTP method |
| 413 | Payload Too Large - Files exceed 50MB limit |
| 500 | Internal Server Error - Processing error |

## Requirements

- Python 3.7+
- Flask 3.0.0
- PyPDF2 3.0.1
- Werkzeug 3.0.1

## Configuration

Maximum file size: 50MB (configurable in `app.py`)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
