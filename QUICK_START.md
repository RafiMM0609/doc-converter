# Quick Start Guide - PDF Converter UI

## 🚀 Get Started in 5 Minutes

### Step 1: Verify Requirements
```bash
python --version  # Should be 3.10+
```

**Install poppler-utils:**
- Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases
- macOS: `brew install poppler`
- Linux: `sudo apt-get install poppler-utils`

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Start the Application
```bash
python main.py
```

You'll see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Open in Browser
Go to: **http://localhost:8000/index.html**

## 📋 What You Get

### Two Powerful Features in One App:

**1. Convert PDF → JPG**
- Upload a single PDF
- Get a high-quality JPG preview of the first page
- Instant download

**2. Merge Multiple PDFs**
- Upload 2 or more PDF files
- Combine them into one PDF
- Download the merged result

## 🎨 UI Highlights

✅ **Modern Design** - Clean, intuitive interface  
✅ **Responsive** - Works on desktop, tablet, phone  
✅ **Drag & Drop** - Just drop files to upload  
✅ **Real-time Feedback** - Progress bars and notifications  
✅ **File Management** - Easy add/remove of files  

## 📁 File Structure

```
doc-converter/
├── index.html          ← Main UI (open in browser)
├── main.py            ← Start the server
├── static/
│   ├── style.css      ← Styling
│   └── app.js         ← JavaScript logic
└── ... (backend files)
```

## 🔗 Useful Links

- **UI**: http://localhost:8000/index.html
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## ❓ FAQ

**Q: Where do converted files go?**  
A: They're automatically downloaded to your Downloads folder. No files are stored on the server.

**Q: What's the max file size?**  
A: 10 MB per file.

**Q: Can I convert multiple pages?**  
A: Currently only the first page is converted. Edit `config.py` to change `MAX_PAGES`.

**Q: Do you store my files?**  
A: No. Files are deleted immediately after processing.

**Q: What PDF features are supported?**  
A: Text, images, and layouts. Encrypted PDFs may not work.

## 🛠️ Customization

Edit `config.py` to change:
```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # Max file size
DPI = 200                          # Image quality
MAX_PAGES = 1                      # Pages to convert
```

## 📞 Troubleshooting

**Server won't start?**
- Check if port 8000 is available
- Ensure poppler-utils is installed

**Files won't upload?**
- Check file size (max 10 MB)
- Ensure it's a valid PDF
- Try a different browser

**Conversion failing?**
- Check server logs for error messages
- Verify PDF is not corrupted
- Try a simpler PDF file

## 🚀 Advanced Usage

**Test API with cURL:**
```bash
curl -X POST "http://localhost:8000/api/convert-pdf-to-jpg" \
  -F "file=@document.pdf" \
  --output converted.jpg
```

**Merge multiple PDFs:**
```bash
curl -X POST "http://localhost:8000/api/merge-pdfs" \
  -F "files=@file1.pdf" \
  -F "files=@file2.pdf" \
  -F "files=@file3.pdf" \
  --output merged.pdf
```

## 📚 Full Documentation

See `Readme.md` for comprehensive documentation and `UI_README.md` for complete UI features.

---

**Enjoy using PDF Converter! 🎉**
