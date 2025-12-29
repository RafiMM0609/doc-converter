"""
PDF Converter API
A Flask-based API for merging PDF files and returning the result as Base64-encoded stream.
"""

import base64
import io
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_pdf(file_stream):
    """Validate if the file is a valid PDF."""
    try:
        file_stream.seek(0)
        PdfReader(file_stream)
        file_stream.seek(0)
        return True
    except Exception:
        return False


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'PDF Converter API is running'}), 200


@app.route('/merge-pdf', methods=['POST'])
def merge_pdf():
    """
    Merge multiple PDF files and return the result as Base64-encoded stream.
    
    Expected input: Multiple files with key 'files'
    Returns: JSON with Base64-encoded merged PDF
    """
    try:
        # Check if files are present in the request
        if 'files' not in request.files:
            return jsonify({
                'error': 'No files provided',
                'message': 'Please upload PDF files using the "files" field'
            }), 400
        
        files = request.files.getlist('files')
        
        # Validate that at least 2 files are provided
        if len(files) < 2:
            return jsonify({
                'error': 'Insufficient files',
                'message': 'At least 2 PDF files are required for merging'
            }), 400
        
        # Validate file extensions
        for file in files:
            if not file or file.filename == '':
                return jsonify({
                    'error': 'Invalid file',
                    'message': 'One or more files are empty or have no filename'
                }), 400
            
            if not allowed_file(file.filename):
                return jsonify({
                    'error': 'Invalid file type',
                    'message': f'File "{secure_filename(file.filename)}" is not a PDF'
                }), 400
        
        # Create PDF writer for merging
        pdf_writer = PdfWriter()
        
        # Process and merge PDFs
        for idx, file in enumerate(files):
            try:
                # Read file content into BytesIO
                file_content = io.BytesIO(file.read())
                
                # Validate PDF format
                if not validate_pdf(file_content):
                    return jsonify({
                        'error': 'Invalid PDF format',
                        'message': f'File "{secure_filename(file.filename)}" is not a valid PDF'
                    }), 400
                
                # Read PDF and add pages to writer
                pdf_reader = PdfReader(file_content)
                
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
                    
            except Exception as e:
                return jsonify({
                    'error': 'PDF processing error',
                    'message': f'Failed to process file "{secure_filename(file.filename)}": {str(e)}'
                }), 500
        
        # Write merged PDF to BytesIO
        output = io.BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        
        # Encode to Base64
        merged_pdf_base64 = base64.b64encode(output.read()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'message': 'PDFs merged successfully',
            'merged_pdf': merged_pdf_base64,
            'file_count': len(files)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Server error',
            'message': f'An unexpected error occurred: {str(e)}'
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file size exceeding limit."""
    return jsonify({
        'error': 'File too large',
        'message': 'The uploaded files exceed the maximum allowed size of 50MB'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle method not allowed errors."""
    return jsonify({
        'error': 'Method not allowed',
        'message': 'The HTTP method is not allowed for this endpoint'
    }), 405


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
