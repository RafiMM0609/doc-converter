"""
Unit tests for PDF Merger API
"""

import unittest
import base64
import io
import json
from PyPDF2 import PdfWriter, PdfReader
from app import app


class TestPDFMergeAPI(unittest.TestCase):
    """Test cases for the PDF merge API."""
    
    def setUp(self):
        """Set up test client."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def create_test_pdf(self, page_count=1, text="Test PDF"):
        """Create a simple test PDF in memory."""
        pdf_writer = PdfWriter()
        
        for i in range(page_count):
            # Create a blank page
            pdf_writer.add_blank_page(width=612, height=792)
        
        output = io.BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        return output
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_merge_pdf_success(self):
        """Test successful PDF merge with valid files."""
        pdf1 = self.create_test_pdf(page_count=2)
        pdf2 = self.create_test_pdf(page_count=3)
        
        data = {
            'files': [
                (pdf1, 'test1.pdf'),
                (pdf2, 'test2.pdf')
            ]
        }
        
        response = self.client.post('/merge-pdf', 
                                   data=data,
                                   content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data['success'])
        self.assertIn('merged_pdf', response_data)
        self.assertEqual(response_data['file_count'], 2)
        
        # Verify the merged PDF is valid Base64
        try:
            merged_pdf_bytes = base64.b64decode(response_data['merged_pdf'])
            merged_pdf = PdfReader(io.BytesIO(merged_pdf_bytes))
            # Should have 5 pages total (2 + 3)
            self.assertEqual(len(merged_pdf.pages), 5)
        except Exception as e:
            self.fail(f"Failed to decode or read merged PDF: {str(e)}")
    
    def test_merge_pdf_multiple_files(self):
        """Test merging more than 2 files."""
        pdf1 = self.create_test_pdf(page_count=1)
        pdf2 = self.create_test_pdf(page_count=1)
        pdf3 = self.create_test_pdf(page_count=1)
        
        data = {
            'files': [
                (pdf1, 'test1.pdf'),
                (pdf2, 'test2.pdf'),
                (pdf3, 'test3.pdf')
            ]
        }
        
        response = self.client.post('/merge-pdf',
                                   data=data,
                                   content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['file_count'], 3)
        
        # Verify merged PDF has correct page count
        merged_pdf_bytes = base64.b64decode(response_data['merged_pdf'])
        merged_pdf = PdfReader(io.BytesIO(merged_pdf_bytes))
        self.assertEqual(len(merged_pdf.pages), 3)
    
    def test_merge_pdf_no_files(self):
        """Test merge with no files provided."""
        response = self.client.post('/merge-pdf',
                                   data={},
                                   content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'No files provided')
    
    def test_merge_pdf_single_file(self):
        """Test merge with only one file (should fail)."""
        pdf1 = self.create_test_pdf(page_count=2)
        
        data = {
            'files': [(pdf1, 'test1.pdf')]
        }
        
        response = self.client.post('/merge-pdf',
                                   data=data,
                                   content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertIn('At least 2 PDF files', response_data['message'])
    
    def test_merge_pdf_invalid_extension(self):
        """Test merge with non-PDF file extension."""
        fake_file = io.BytesIO(b"This is not a PDF")
        
        data = {
            'files': [
                (fake_file, 'test1.txt'),
                (fake_file, 'test2.doc')
            ]
        }
        
        response = self.client.post('/merge-pdf',
                                   data=data,
                                   content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertIn('not a PDF', response_data['message'])
    
    def test_merge_pdf_invalid_pdf_content(self):
        """Test merge with invalid PDF content."""
        fake_pdf = io.BytesIO(b"This is not a valid PDF content")
        
        data = {
            'files': [
                (fake_pdf, 'test1.pdf'),
                (fake_pdf, 'test2.pdf')
            ]
        }
        
        response = self.client.post('/merge-pdf',
                                   data=data,
                                   content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertIn('not a valid PDF', response_data['message'])
    
    def test_merge_pdf_empty_filename(self):
        """Test merge with empty filename."""
        pdf1 = self.create_test_pdf()
        
        data = {
            'files': [
                (pdf1, ''),
                (pdf1, 'test2.pdf')
            ]
        }
        
        response = self.client.post('/merge-pdf',
                                   data=data,
                                   content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
    
    def test_not_found_endpoint(self):
        """Test 404 for non-existent endpoint."""
        response = self.client.get('/non-existent')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
    
    def test_method_not_allowed(self):
        """Test wrong HTTP method."""
        response = self.client.get('/merge-pdf')
        self.assertEqual(response.status_code, 405)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)


if __name__ == '__main__':
    unittest.main()
