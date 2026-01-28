# Fix for Static File Serving - "Not Found" Error

## Problem
When accessing `http://localhost:8000/index.html`, getting error:
```json
{"detail": "Not Found"}
```

## Root Cause
The main.py file was only mounting static files from the `/static` directory, but index.html is in the root directory. FastAPI couldn't find the file to serve.

## Solution Applied
Updated `main.py` to add a dedicated route for serving index.html:

```python
@app.get("/index.html")
async def serve_index():
    """Serve index.html"""
    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/html")
    return {"detail": "index.html not found"}
```

## Changes Made
- Added `FileResponse` import from fastapi.responses
- Added `os` import for file path operations
- Added `/index.html` GET endpoint
- Returns index.html with proper HTML media type

## How to Fix Running Application

### Option 1: Restart Docker Container (Recommended)

```bash
# Stop current container
docker-compose down

# Rebuild and start
docker-compose up -d

# Verify it's running
docker-compose ps

# Test the application
curl http://localhost:8000/index.html
# Should see HTML content, not error

# Open in browser
http://localhost:8000/index.html
```

### Option 2: Rebuild Without Down

```bash
# Rebuild and start
docker-compose up --build -d

# Verify
docker-compose ps

# Test
curl http://localhost:8000/index.html
```

### Option 3: Local Python (Without Docker)

```bash
# Stop current Docker container (if running)
docker-compose down

# Install dependencies (if not already done)
pip install -r requirements.txt

# Start application
python main.py

# Test the application
curl http://localhost:8000/index.html

# Open in browser
http://localhost:8000/index.html
```

## Verification Steps

1. **Check if container is healthy**
   ```bash
   docker-compose ps
   # Should show status as "Up (healthy)"
   ```

2. **Test health endpoint**
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status": "healthy"}
   ```

3. **Test API endpoint**
   ```bash
   curl http://localhost:8000/
   # Should return API info JSON
   ```

4. **Test index.html endpoint**
   ```bash
   curl http://localhost:8000/index.html
   # Should return HTML content (not an error)
   ```

5. **Test in browser**
   ```
   http://localhost:8000/index.html
   # Should display PDF Converter UI
   ```

## Troubleshooting

### Still getting "Not Found" error?

1. **Check if index.html exists**
   ```bash
   ls -la index.html
   # Should show the file exists
   ```

2. **Check Docker logs**
   ```bash
   docker-compose logs -f
   # Look for any error messages
   ```

3. **Restart container**
   ```bash
   docker-compose restart
   ```

4. **Rebuild from scratch**
   ```bash
   docker-compose down -v
   docker-compose up --build -d
   ```

### Getting connection refused?

1. **Check if Docker container is running**
   ```bash
   docker-compose ps
   # Should show container as running
   ```

2. **Check if port 8000 is in use**
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Linux/Mac
   lsof -i :8000
   ```

3. **Try a different port**
   - Edit `docker-compose.yaml`
   - Change `ports: - "8000:8000"` to `ports: - "8001:8000"`
   - Run `docker-compose up -d`
   - Visit `http://localhost:8001/index.html`

## File Changes Summary

**File Modified: main.py**

Added imports:
```python
from fastapi.responses import FileResponse
import os
```

Added endpoint:
```python
@app.get("/index.html")
async def serve_index():
    """Serve index.html"""
    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/html")
    return {"detail": "index.html not found"}
```

## What This Does

1. **Creates a route** for `/index.html` requests
2. **Locates index.html** in the application directory
3. **Returns the file** with correct MIME type (text/html)
4. **Gracefully handles** missing files with error message

## Now You Can Access

✅ **Web UI**: http://localhost:8000/index.html  
✅ **API Docs**: http://localhost:8000/docs  
✅ **ReDoc**: http://localhost:8000/redoc  
✅ **Health**: http://localhost:8000/health  
✅ **Root Info**: http://localhost:8000/  

## Next Steps

1. Restart your Docker container with the new code
2. Visit http://localhost:8000/index.html
3. Start converting PDFs!

---

**This fix ensures the web UI is properly served from the FastAPI backend!**
